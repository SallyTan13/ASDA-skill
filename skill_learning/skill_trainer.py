"""
Skill Trainer - Epoch-based Training Loop with Checkpointing

Implements the outer training loop for skill refinement:
1. Run system on train set, collect RunLog
2. Aggregate evidence (Q+/Q-)
3. Select skills to update
4. Propose refined versions (textual optimizer)
5. Validate on val set
6. Accept/rollback based on validation
7. Save checkpoint
8. Track best checkpoint and early stopping
"""

import os
import json
import re
import shutil
import inspect
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd

from run_logger import RunLogger
from evidence_collector import EvidenceCollector
from skills_router import SkillsRouter, generate_with_progressive_loading
from textual_optimizer import TextualOptimizer, SkillRef
from residual_evidence_collector import (
    ResidualEvidenceCollector,
    UnsolvedCard,
    format_discover_evidence_for_refinement,
    format_gap_evidence_for_new_skill
)
from skill_warming_up import extract_pattern_names
try:
    from skill_learning.config import cfg, is_config_loaded
except ImportError:
    from config import cfg, is_config_loaded

# Attribution prompts for deep analysis
from regression_analysis_prompts import build_attribution_prompt

# Extracted modules
from checkpoint_manager import SkillCheckpoint
from sandbox_verifier import SandboxVerifierMixin
from trainer_utils import TrainerUtilsMixin
from iteration_logger import IterationLogger


class SkillTrainer(SandboxVerifierMixin, TrainerUtilsMixin):
    """Manages epoch-based skill training loop.

    Adapted for the 2-level skill folder structure:
        skill_dir/
          SKILL.md              # Navigation file with file reference table
          common/               # Cross-subfield skills
          {subfield}/           # Subfield-specific skills

    Key design:
    - Users configure SKILLS_DIR in .env (e.g., .claude/skills/famma-non-arithmetic-v1)
    - Working copy lives in checkpoint_dir/working_skills/ (never modifies original)
    - Router uses LLM-based routing via SKILL.md
    - Evidence grouped by specific_skill_file (e.g., "portfolio_management/concept_confusion.md")
    - Reload router from working copy at start of each epoch
    """

    def __init__(
        self,
        skills_dir: Optional[str] = None,  # From env SKILLS_DIR if not provided
        checkpoint_dir: str = None,
        lambda_regress: float = None,  # Regression penalty weight
        M: int = None,  # Top-M files to refine each epoch
        patience: int = None,  # Early stopping patience
        p_min: int = None,  # Minimum Q+ needed for refinement
        r_min: int = None,  # Minimum Q- needed for refinement
        default_P: int = None,  # Default max positives to sample
        default_N: int = None,  # Default max negatives to sample
        skill_P_N_config: Optional[Dict[str, Dict[str, int]]] = None,  # Per-file P/N overrides
        # Residual evidence collection settings
        enable_residual_analysis: bool = None,
        enable_probe_alternatives: bool = None,  # Whether to probe alternative skills
        skills_loading_mode: str = None,  # "router" or "progressive"
        max_probes_per_case: int = None,
        max_residual_cases: int = None,
        enable_residual_diagnosis: bool = None,
        # Sandbox verification settings
        sandbox_enabled: Optional[bool] = None,
        sandbox_solve_threshold: Optional[float] = None,
        sandbox_route_threshold: Optional[float] = None,
        sandbox_q_plus_threshold: Optional[float] = None,
        max_refine_attempts: Optional[int] = None,
        sandbox_max_cases: Optional[int] = None,
        # Progressive mode support
        anthropic_client: Optional[Any] = None,  # Anthropic client for progressive mode
        gen_model: Optional[str] = None,  # Generation model name
        # Parallel refinement settings
        parallel_refine_workers: Optional[int] = None  # Max parallel file refinements (0=disabled)
    ):
        """
        Initialize skill trainer.

        Args:
            skills_dir: Path to source skill set (e.g., ".claude/skills/famma-non-arithmetic-v1").
                        Falls back to SKILLS_DIR env var if not provided.
            checkpoint_dir: Path to checkpoint directory (working copy lives here)
            lambda_regress: Regression penalty weight
            M: Number of skill files to refine per epoch
            patience: Early stopping patience (epochs)
            p_min: Minimum Q+ needed to trigger refinement
            r_min: Minimum Q- needed to trigger refinement
            default_P: Default maximum positive cases to sample
            default_N: Default maximum negative cases to sample
            skill_P_N_config: Per-file P/N overrides
            enable_residual_analysis: Whether to analyze unsolved cases
            enable_probe_alternatives: Whether to probe alternative skills for unsolved cases
            skills_loading_mode: "router" (probe alternatives) or "progressive" (skip probing)
            max_probes_per_case: Maximum alternative skills to probe per unsolved case (router mode only)
            max_residual_cases: Maximum unsolved cases to probe (router mode only)
            enable_residual_diagnosis: Whether to use LLM for root cause diagnosis
            anthropic_client: Anthropic client for progressive mode sandbox verification
            gen_model: Generation model name (for progressive mode sandbox)
        """
        # Apply defaults from config or environment variables
        if checkpoint_dir is None:
            checkpoint_dir = cfg('paths.checkpoint_dir') or os.getenv('CHECKPOINT_DIR', 'skill_learning/checkpoints_api')
        if lambda_regress is None:
            lambda_regress = cfg('training.lambda_regress') or float(os.getenv('LAMBDA_REGRESS', '2.0'))
        if M is None:
            M = cfg('training.M') or int(os.getenv('M', '5'))
        if patience is None:
            patience = cfg('training.patience') or int(os.getenv('PATIENCE', '3'))
        if p_min is None:
            p_min = cfg('evidence.p_min') or int(os.getenv('P_MIN', '5'))
        if r_min is None:
            r_min = cfg('evidence.r_min') or int(os.getenv('R_MIN', '2'))
        if default_P is None:
            default_P = cfg('evidence.evidence_p') or int(os.getenv('EVIDENCE_P', '8'))
        if default_N is None:
            default_N = cfg('evidence.evidence_n') or int(os.getenv('EVIDENCE_N', '8'))
        if enable_residual_analysis is None:
            enable_residual_analysis = cfg('residual.enable_analysis') if cfg('residual.enable_analysis') is not None else os.getenv('ENABLE_RESIDUAL_ANALYSIS', 'true').lower() == 'true'
        if enable_probe_alternatives is None:
            enable_probe_alternatives = cfg('residual.enable_probe_alternatives') if cfg('residual.enable_probe_alternatives') is not None else os.getenv('ENABLE_PROBE_ALTERNATIVES', 'true').lower() == 'true'
        if skills_loading_mode is None:
            skills_loading_mode = cfg('skills.loading_mode') or os.getenv('SKILLS_LOADING_MODE', 'router')
        if max_probes_per_case is None:
            max_probes_per_case = cfg('residual.max_probes_per_case') or int(os.getenv('MAX_PROBES_PER_CASE', '3'))
        if max_residual_cases is None:
            max_residual_cases = cfg('residual.max_cases') or int(os.getenv('MAX_RESIDUAL_CASES', '20'))
        if enable_residual_diagnosis is None:
            enable_residual_diagnosis = cfg('residual.enable_diagnosis') if cfg('residual.enable_diagnosis') is not None else os.getenv('ENABLE_RESIDUAL_DIAGNOSIS', 'true').lower() == 'true'

        # Source skills directory (from arg, config, or env)
        source_dir = skills_dir or cfg('skills.dir') or os.getenv(
            'SKILLS_DIR', '.claude/skills/famma-non-arithmetic-v1'
        )
        self.source_skills_dir = Path(source_dir)
        self.skill_set_name = self.source_skills_dir.name  # e.g., "famma-non-arithmetic-v1"

        # Checkpoint and working directories
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.working_skills_dir = self.checkpoint_dir / "working_skills"

        # Create working copy from source (never modify original .claude/skills/)
        self._init_working_copy()

        self.checkpoint_mgr = SkillCheckpoint(checkpoint_dir)
        self.iteration_logger = IterationLogger(self.checkpoint_dir)
        self.lambda_regress = lambda_regress
        self.M = M
        self.patience = patience
        self.default_P = default_P
        self.default_N = default_N
        self.skill_P_N_config = skill_P_N_config or {}

        # Initialize router on working copy (uses LLM-based routing)
        self.router = SkillsRouter(str(self.working_skills_dir))
        self.logger = RunLogger()

        # SkillRef for passing to TextualOptimizer
        self.skill_ref = SkillRef(
            skill_dir=self.working_skills_dir,
            name=self.skill_set_name
        )

        self.evidence_collector = EvidenceCollector(
            p_min=p_min,
            r_min=r_min,
            default_P=default_P,
            default_N=default_N
        )
        self.textual_optimizer = TextualOptimizer(
            checkpoint_dir=self.checkpoint_dir
        )

        # Residual evidence collector for unsolved cases
        self.enable_residual_analysis = enable_residual_analysis
        self.enable_probe_alternatives = enable_probe_alternatives
        self.skills_loading_mode = skills_loading_mode
        self.max_residual_cases = max_residual_cases
        self.residual_collector = ResidualEvidenceCollector(
            skills_loading_mode=skills_loading_mode,
            max_probes_per_case=max_probes_per_case,
            probe_same_subfield_only=True,
            enable_diagnosis=enable_residual_diagnosis
        ) if enable_residual_analysis else None

        # Sandbox verification config (from args, config, or env)
        self.sandbox_enabled = sandbox_enabled if sandbox_enabled is not None else \
            (cfg('sandbox.enabled') if cfg('sandbox.enabled') is not None else os.getenv('SANDBOX_ENABLED', 'true').lower() == 'true')
        self.sandbox_solve_threshold = sandbox_solve_threshold if sandbox_solve_threshold is not None else \
            (cfg('sandbox.solve_threshold') or float(os.getenv('SANDBOX_SOLVE_THRESHOLD', '0.3')))
        self.sandbox_route_threshold = sandbox_route_threshold if sandbox_route_threshold is not None else \
            (cfg('sandbox.route_threshold') or float(os.getenv('SANDBOX_ROUTE_THRESHOLD', '0.5')))
        self.max_refine_attempts = max_refine_attempts if max_refine_attempts is not None else \
            (cfg('sandbox.max_refine_attempts') or int(os.getenv('MAX_REFINE_ATTEMPTS', '3')))
        self.sandbox_max_cases = sandbox_max_cases if sandbox_max_cases is not None else \
            (cfg('sandbox.max_cases') or int(os.getenv('SANDBOX_MAX_CASES', '10')))

        # Progressive mode support for sandbox verification
        self.anthropic_client = anthropic_client
        self.gen_model = gen_model or cfg('models.gen') or os.getenv('GEN_MODEL', 'claude-3-5-haiku-20241022')

        # Deep analysis / attribution settings
        enable_deep_analysis_config = cfg('enable_deep_analysis')
        self.enable_deep_analysis = enable_deep_analysis_config if enable_deep_analysis_config is not None else True

        # Parallel refinement settings
        self.parallel_refine_workers = parallel_refine_workers if parallel_refine_workers is not None else \
            (cfg('training.parallel_refine_workers') or int(os.getenv('PARALLEL_REFINE_WORKERS', '0')))
        self._skill_md_lock = threading.Lock()  # Lock for SKILL.md updates

        # Training history
        self.history = {
            "epochs": [],
            "train_metrics": [],
            "val_metrics": [],
            "best_epoch": None,
            "best_val_acc": -float('inf')
        }

        # Evidence tracking across epochs (for stability analysis)
        self.prev_epoch_evidence = {}

        print(f"SkillTrainer initialized:")
        print(f"  Source: {self.source_skills_dir}")
        print(f"  Working copy: {self.working_skills_dir}")
        print(f"  Skill set: {self.skill_set_name}")
        print(f"  Skills loading mode: {self.skills_loading_mode}")
        print(f"  Probe alternatives: {'enabled' if self.enable_probe_alternatives else 'disabled'}")
        print(f"  Deep analysis (attribution): {'enabled' if self.enable_deep_analysis else 'disabled'}")
        if self.sandbox_enabled:
            print(f"  Sandbox: enabled (solve={self.sandbox_solve_threshold:.0%}, route={self.sandbox_route_threshold:.0%}, max_attempts={self.max_refine_attempts})")
        if self.parallel_refine_workers > 0:
            print(f"  Parallel refinement: enabled (max_workers={self.parallel_refine_workers})")

    def _init_working_copy(self):
        """Copy source skills to working directory. Called once at init."""
        if self.working_skills_dir.exists():
            shutil.rmtree(self.working_skills_dir)
        shutil.copytree(self.source_skills_dir, self.working_skills_dir)
        print(f"Working copy created: {self.source_skills_dir} -> {self.working_skills_dir}")

    def _reload_router(self):
        """Reload router from working skills directory (call at start of each epoch)."""
        self.router = SkillsRouter(str(self.working_skills_dir))
        # Update SkillRef in case skill_dir changed
        self.skill_ref = SkillRef(
            skill_dir=self.working_skills_dir,
            name=self.skill_set_name
        )
        print(f"Router reloaded from: {self.working_skills_dir}")

    def _validate_skill_md(self, content: str) -> bool:
        """Validate SKILL.md has proper File Index with file entries.

        Prevents accepting almost-empty SKILL.md that breaks routing.

        Args:
            content: SKILL.md content to validate

        Returns:
            True if valid (has File Index with at least one .md file entry)
        """
        if not content:
            return False

        # Must have File Index section
        if "File Index" not in content and "file index" not in content.lower():
            return False

        # Must have at least one .md file reference (not just SKILL.md)
        import re
        file_refs = re.findall(r'`([^`]+\.md)`', content)
        # Filter out SKILL.md itself
        actual_files = [f for f in file_refs if f != 'SKILL.md']

        if len(actual_files) < 1:
            return False

        return True

    def _handle_refinement_result(
        self,
        updated_content: str,
        was_updated: bool,
        skill_file: str,
        cards: list,
        by_action: dict,
        action_name: str
    ) -> int:
        """
        Handle refinement result with NEEDS_NEW_PATTERN detection and reclassification.

        Returns:
            1 if update applied, 0 otherwise
        """
        if updated_content == "NEEDS_NEW_PATTERN":
            # Reclassify these cards as capability_gap/new_pattern -> need_new_skill
            print(f"    🔄 Reclassifying {len(cards)} cards as need_new_skill (new pattern needed)")
            for card in cards:
                card.recommended_action = "need_new_skill"
            # Add to need_new_skill action group
            if "need_new_skill" not in by_action:
                by_action["need_new_skill"] = []
            by_action["need_new_skill"].extend(cards)
            return 0
        elif was_updated and updated_content:
            file_path = self.working_skills_dir / skill_file
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding="utf-8") as f:
                f.write(updated_content)
            # Sync SKILL.md File Index with updated patterns
            if skill_file != "SKILL.md":
                self._sync_skill_md_file_index(skill_file, updated_content)
            print(f"    ✅ Updated {action_name}: {skill_file}")
            return 1
        return 0

    def _sync_skill_md_file_index(self, file_key: str, updated_content: str):
        """
        Synchronize SKILL.md File Index after skill file refinement.

        Extracts patterns from updated skill content and updates the corresponding
        row in SKILL.md's File Index table.

        Args:
            file_key: Skill file path (e.g., "portfolio_management/concept_confusion.md")
            updated_content: Updated skill file content
        """
        # Extract patterns from updated content
        patterns = extract_pattern_names(updated_content)

        if not patterns:
            print(f"    ⚠️  No patterns extracted from {file_key}, SKILL.md not updated")
            return

        # Read current SKILL.md
        skill_md_path = self.working_skills_dir / "SKILL.md"
        if not skill_md_path.exists():
            print(f"    ⚠️  SKILL.md not found, cannot update File Index")
            return

        skill_md_content = skill_md_path.read_text(encoding='utf-8')

        # Update File Index entry for this file
        # Format: | `file_path` | Subfield | Error Type | Key Patterns |
        pattern_list = ", ".join(patterns)  # All patterns

        # Match the table row for this file (using regex to handle variations in spacing)
        row_pattern = rf'\|\s*`{re.escape(file_key)}`\s*\|([^|]*)\|([^|]*)\|([^|]*)\|'

        # First check if the row exists at all
        if not re.search(row_pattern, skill_md_content):
            print(f"    ⚠️  {file_key} not found in SKILL.md File Index (row missing)")
            return

        def replace_patterns(match):
            # Keep first 3 columns (file_path, subfield, error_type), replace 4th (key patterns)
            return f"| `{file_key}` |{match.group(1)}|{match.group(2)}| {pattern_list} |"

        updated_skill_md = re.sub(row_pattern, replace_patterns, skill_md_content)

        # Check if replacement changed anything (patterns might be the same)
        if updated_skill_md == skill_md_content:
            # This is not an error - just means pattern names didn't change
            # (content might have changed but names are the same)
            return

        # Write updated SKILL.md back
        skill_md_path.write_text(updated_skill_md, encoding='utf-8')
        print(f"    ✅ SKILL.md File Index updated for {file_key} ({len(patterns)} patterns)")

    def compute_metrics(self, run_log: List) -> Dict:
        """
        Compute metrics from run log.

        accuracy = skill-only accuracy (how the current skill set performed)
        baseline_accuracy = baseline-only accuracy (without any skill)

        Args:
            run_log: List of RunLogEntry

        Returns:
            Dictionary of metrics
        """
        if not run_log:
            return {}

        total = len(run_log)
        # Skill accuracy: count only skill_score == 1 (the current run's performance)
        skill_correct = sum(1 for e in run_log if e.skill_score == 1)
        baseline_correct = sum(1 for e in run_log if e.baseline_score == 1)
        fixes = sum(1 for e in run_log if e.is_fix)
        regressions = sum(1 for e in run_log if e.is_regress)

        acc = skill_correct / total if total > 0 else 0
        baseline_acc = baseline_correct / total if total > 0 else 0
        fix_rate = fixes / total if total > 0 else 0
        regress_rate = regressions / total if total > 0 else 0

        # Training loss: -acc + λ*regress_rate
        loss = -acc + self.lambda_regress * regress_rate

        return {
            "total": total,
            "accuracy": acc,
            "baseline_accuracy": baseline_acc,
            "fix_count": fixes,
            "fix_rate": fix_rate,
            "regress_count": regressions,
            "regress_rate": regress_rate,
            "loss": loss
        }

    def _group_evidence_by_file(self, Q_plus: List, Q_minus: List) -> Dict[str, Tuple[List, List]]:
        """
        Group evidence by skill file.

        When attribution_result is available (deep analysis enabled), uses
        attributed_files for more accurate grouping. Otherwise falls back
        to specific_skill_file (original behavior).

        Deduplicates by QID within each file to avoid same question appearing
        multiple times (which can happen when same QID was originally in
        multiple files but attribution points them to the same file).

        Args:
            Q_plus: List of positive evidence cards
            Q_minus: List of negative evidence cards

        Returns:
            Dict mapping skill_file -> (Q_plus_for_file, Q_minus_for_file)
        """
        from collections import defaultdict

        # Use dict to track cards by file AND QID for deduplication
        # Structure: {file_key: {'plus': {qid: card}, 'minus': {qid: card}}}
        grouped = defaultdict(lambda: {'plus': {}, 'minus': {}})

        # Group Q+ by attributed_files or specific_skill_file
        for card in Q_plus:
            # Prefer attribution_result if available
            if card.attribution_result and card.attribution_result.get('attributed_files'):
                files_to_use = card.attribution_result['attributed_files']
            else:
                # Fallback to original behavior
                files_to_use = [card.specific_skill_file] if card.specific_skill_file else []

            for file_key in files_to_use:
                if file_key and file_key != "SKILL.md":
                    # Deduplicate by QID - keep first occurrence
                    if card.qid not in grouped[file_key]['plus']:
                        grouped[file_key]['plus'][card.qid] = card

        # Group Q- by attributed_files or specific_skill_file
        for card in Q_minus:
            # Prefer attribution_result if available
            if card.attribution_result and card.attribution_result.get('attributed_files'):
                files_to_use = card.attribution_result['attributed_files']
            else:
                # Fallback to original behavior
                files_to_use = [card.specific_skill_file] if card.specific_skill_file else []

            for file_key in files_to_use:
                if file_key and file_key != "SKILL.md":
                    # Deduplicate by QID - keep first occurrence
                    if card.qid not in grouped[file_key]['minus']:
                        grouped[file_key]['minus'][card.qid] = card

        # Convert to final format: dict with tuples of lists
        result = {}
        for file_key, data in grouped.items():
            plus_list = list(data['plus'].values())
            minus_list = list(data['minus'].values())
            result[file_key] = (plus_list, minus_list)

        return result

    def _perform_batch_attribution(
        self,
        Q_plus: List,
        Q_minus: List,
        pot_mode: bool = None
    ) -> None:
        """
        Perform LLM-based attribution for all evidence cards BEFORE grouping.

        V2: Attribution ALWAYS runs (not conditional on enable_deep_analysis).
        This populates card.attribution_result for accurate file grouping.

        When LLM attribution fails, uses fallback: first non-common file from loaded_files.

        Args:
            Q_plus: List of positive evidence cards (fixes)
            Q_minus: List of negative evidence cards (regressions)
            pot_mode: Whether to use PoT mode templates (auto-detected if None)
        """
        # V2: Attribution always runs (removed early return)

        all_cards = Q_plus + Q_minus
        if not all_cards:
            return

        # Deduplicate by QID - same question should have same attribution
        # Group cards by QID to avoid redundant LLM calls
        cards_by_qid = {}
        for card in all_cards:
            if card.qid not in cards_by_qid:
                cards_by_qid[card.qid] = []
            cards_by_qid[card.qid].append(card)

        unique_qids = list(cards_by_qid.keys())
        print(f"\n  [Attribution] {len(all_cards)} cards → {len(unique_qids)} unique QIDs (deduplicated)")

        # Auto-detect PoT mode from config or first card
        if pot_mode is None:
            pot_mode = cfg('skills.pot_mode') or False

        # Get analyze model from config
        analyze_model = cfg('models.analyze') or 'claude-sonnet-4-5-20250929'
        analyze_provider = cfg('models.analyze_provider') or 'auto'

        # Auto-detect provider from model name if not specified
        if analyze_provider == 'auto':
            if 'claude' in analyze_model.lower():
                analyze_provider = 'anthropic'
            elif 'gpt' in analyze_model.lower() or 'anthropic/' in analyze_model.lower():
                analyze_provider = 'openrouter'
            else:
                analyze_provider = 'anthropic'  # default

        # Initialize LLM client for attribution based on analyze_provider
        import os
        if analyze_provider == 'openrouter':
            from openai import OpenAI
            client = OpenAI(
                api_key=os.getenv('OPENROUTER_API_KEY'),
                base_url="https://openrouter.ai/api/v1"
            )
        elif analyze_provider == 'anthropic':
            import anthropic
            client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        else:
            # Fallback to refine client
            from textual_optimizer import get_refine_client
            client = get_refine_client()

        # Track statistics
        attributed_count = 0
        failed_count = 0
        skipped_count = 0

        for i, qid in enumerate(unique_qids):
            cards_for_qid = cards_by_qid[qid]
            representative_card = cards_for_qid[0]  # Use first card as representative
            is_fix = representative_card in Q_plus

            # Skip if already has attribution_result (both EvidenceCard and UnsolvedCard)
            attr_result = getattr(representative_card, 'attribution_result', None)
            if attr_result and attr_result.get('attributed_files'):
                # Apply existing attribution to all cards with same QID
                for card in cards_for_qid:
                    card.attribution_result = representative_card.attribution_result
                attributed_count += 1
                skipped_count += len(cards_for_qid) - 1
                continue

            # Get loaded files - merge from all cards with same QID for complete picture
            all_loaded_files = set()
            for card in cards_for_qid:
                if card.loaded_files:
                    all_loaded_files.update(card.loaded_files)
                elif card.specific_skill_file:
                    all_loaded_files.add(card.specific_skill_file)

            loaded_files = list(all_loaded_files)
            if not loaded_files:
                # Can't attribute without loaded files
                continue

            # Load skill files content
            skill_files_content = {}
            for file_path in loaded_files:
                full_path = self.working_skills_dir / file_path
                if full_path.exists():
                    with open(full_path, 'r', encoding="utf-8") as f:
                        skill_files_content[file_path] = f.read()

            # Build attribution prompt
            try:
                if pot_mode:
                    # PoT mode: use code
                    skill_code = representative_card.skill_code or ""
                    execution_success = representative_card.skill_k.get('execution_success', None)
                    prompt = build_attribution_prompt(
                        question=representative_card.question,
                        ground_truth=representative_card.ground_truth,
                        baseline_answer=representative_card.baseline.get('answer', 'N/A'),
                        skill_answer=representative_card.skill_k.get('answer', 'N/A'),
                        loaded_files=loaded_files,
                        skill_files_content=skill_files_content,
                        is_fix=is_fix,
                        context=representative_card.context,
                        options=representative_card.options,
                        skill_code=skill_code,
                        execution_success=execution_success
                    )
                else:
                    # Non-PoT mode: use explanation
                    skill_explanation = representative_card.skill_k.get('explanation', '')
                    prompt = build_attribution_prompt(
                        question=representative_card.question,
                        ground_truth=representative_card.ground_truth,
                        baseline_answer=representative_card.baseline.get('answer', 'N/A'),
                        skill_answer=representative_card.skill_k.get('answer', 'N/A'),
                        loaded_files=loaded_files,
                        skill_files_content=skill_files_content,
                        is_fix=is_fix,
                        context=representative_card.context,
                        options=representative_card.options,
                        skill_explanation=skill_explanation
                    )

                # Call LLM for attribution (handle different providers)
                if analyze_provider == 'openrouter':
                    response = client.chat.completions.create(
                        model=analyze_model,
                        max_tokens=1024,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    response_text = response.choices[0].message.content.strip()
                else:
                    response = client.messages.create(
                        model=analyze_model,
                        max_tokens=1024,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    response_text = response.content[0].text.strip()

                # Parse JSON response
                import json as json_module
                # Try to find JSON block in response (handles markdown code blocks too)
                response_clean = response_text
                if '```json' in response_text:
                    # Extract from markdown code block
                    json_start = response_text.find('```json') + 7
                    json_end = response_text.find('```', json_start)
                    if json_end > json_start:
                        response_clean = response_text[json_start:json_end].strip()
                elif '```' in response_text:
                    # Generic code block
                    json_start = response_text.find('```') + 3
                    json_end = response_text.find('```', json_start)
                    if json_end > json_start:
                        response_clean = response_text[json_start:json_end].strip()

                # Try to parse JSON
                try:
                    attribution_result = json_module.loads(response_clean)
                except json_module.JSONDecodeError:
                    # Fallback: extract just the JSON object using brace matching
                    brace_start = response_text.find('{')
                    if brace_start >= 0:
                        depth = 0
                        for i_char, c in enumerate(response_text[brace_start:]):
                            if c == '{':
                                depth += 1
                            elif c == '}':
                                depth -= 1
                                if depth == 0:
                                    json_str = response_text[brace_start:brace_start + i_char + 1]
                                    attribution_result = json_module.loads(json_str)
                                    break
                        else:
                            raise ValueError("No valid JSON found")
                    else:
                        raise ValueError("No JSON object found")

                if attribution_result and attribution_result.get('attributed_files'):
                    # Apply attribution to ALL cards with same QID
                    for card in cards_for_qid:
                        # Safely set attribution_result (works for both EvidenceCard and UnsolvedCard)
                        try:
                            card.attribution_result = attribution_result
                        except AttributeError:
                            pass  # Skip cards that don't support this attribute
                    attributed_count += 1

                    if (i + 1) % 10 == 0:
                        print(f"    Processed {i + 1}/{len(unique_qids)} unique QIDs...")
                else:
                    # Fallback: use first non-common file
                    fallback_file = self._get_first_non_common_file(loaded_files)
                    if fallback_file:
                        fallback_result = {'attributed_files': [fallback_file], 'fallback': True}
                        for card in cards_for_qid:
                            try:
                                card.attribution_result = fallback_result
                            except AttributeError:
                                pass
                        attributed_count += 1
                        print(f"    ⚠️  No attributed_files in LLM response for QID={qid}, using fallback: {fallback_file}")
                    else:
                        failed_count += 1
                        print(f"    ⚠️  No attributed_files and no fallback available for QID={qid}")

            except Exception as e:
                # Fallback: use first non-common file
                fallback_file = self._get_first_non_common_file(loaded_files)
                if fallback_file:
                    fallback_result = {'attributed_files': [fallback_file], 'fallback': True}
                    for card in cards_for_qid:
                        try:
                            card.attribution_result = fallback_result
                        except AttributeError:
                            pass
                    attributed_count += 1
                    print(f"    ⚠️  Attribution failed for QID={qid}: {e}, using fallback: {fallback_file}")
                else:
                    failed_count += 1
                    print(f"    ⚠️  Attribution failed for QID={qid}: {e}, no fallback available")

        total_cards_attributed = sum(len(cards_by_qid[qid]) for qid in unique_qids
                                     if cards_by_qid[qid][0].attribution_result)
        print(f"  ✓ Attribution complete: {attributed_count} unique QIDs → {total_cards_attributed} cards attributed, {failed_count} failed")

        # Show attribution distribution by file
        from collections import defaultdict
        attribution_by_file = defaultdict(lambda: {'q_plus': [], 'q_minus': []})
        for qid in unique_qids:
            cards = cards_by_qid[qid]
            rep_card = cards[0]
            if rep_card.attribution_result and rep_card.attribution_result.get('attributed_files'):
                attr_files = rep_card.attribution_result['attributed_files']
                is_fix = rep_card in Q_plus
                for f in attr_files:
                    if is_fix:
                        attribution_by_file[f]['q_plus'].append(qid)
                    else:
                        attribution_by_file[f]['q_minus'].append(qid)

        if attribution_by_file:
            print(f"\n  Attribution distribution by file:")
            for file_key in sorted(attribution_by_file.keys()):
                data = attribution_by_file[file_key]
                q_plus_count = len(data['q_plus'])
                q_minus_count = len(data['q_minus'])
                print(f"    {file_key}: Q+ {q_plus_count}, Q- {q_minus_count}")

    def compute_skill_stats(self, run_log: List) -> Dict[str, Dict]:
        """
        Compute per-file statistics for selecting update set.

        Groups by specific_skill_file (e.g., "portfolio_management/concept_confusion.md")
        since we have a single skill set with multiple files.

        Args:
            run_log: List of RunLogEntry

        Returns:
            Dictionary mapping specific_skill_file -> stats
        """
        stats = {}

        for entry in run_log:
            # Attribute to ALL files used (not just primary), skip SKILL.md
            files = getattr(entry, 'all_skill_files', None)
            if not files:
                specific = entry.specific_skill_file
                files = [specific] if specific and specific != "SKILL.md" else []

            for file_key in files:
                # Skip SKILL.md - it's always loaded, not a specific skill file
                if file_key == "SKILL.md":
                    continue
                if file_key not in stats:
                    stats[file_key] = {
                        "used": 0,
                        "fixes": 0,
                        "regressions": 0,
                        "net": 0,
                        "local_loss": 0
                    }

                stats[file_key]["used"] += 1
                if entry.is_fix:
                    stats[file_key]["fixes"] += 1
                if entry.is_regress:
                    stats[file_key]["regressions"] += 1

        # Calculate net and local loss
        for file_key, s in stats.items():
            s["net"] = s["fixes"] - self.lambda_regress * s["regressions"]
            if s["used"] > 0:
                s["local_loss"] = -s["net"] / s["used"]
            else:
                s["local_loss"] = 0

        return stats

    def _compute_stats_from_evidence(
        self,
        evidence_by_file: Dict[str, Tuple[List, List]]
    ) -> Dict[str, Dict]:
        """
        Compute per-file statistics from grouped evidence (post-attribution).

        This method computes stats from evidence cards AFTER attribution analysis,
        which provides more accurate file-to-evidence mapping than run_log stats.

        Args:
            evidence_by_file: Dict mapping file -> (Q_plus_list, Q_minus_list)

        Returns:
            Dictionary mapping specific_skill_file -> stats
        """
        stats = {}

        for file_key, (q_plus, q_minus) in evidence_by_file.items():
            if file_key == "SKILL.md":
                continue

            # Count unique QIDs for fixes/regressions to avoid double-counting
            # (same card may appear in multiple files)
            fix_qids = {c.qid for c in q_plus}
            regress_qids = {c.qid for c in q_minus}
            all_qids = fix_qids | regress_qids

            stats[file_key] = {
                "used": len(all_qids),
                "fixes": len(fix_qids),
                "regressions": len(regress_qids),
                "net": 0,
                "local_loss": 0
            }

            # Calculate net and local loss
            s = stats[file_key]
            s["net"] = s["fixes"] - self.lambda_regress * s["regressions"]
            if s["used"] > 0:
                s["local_loss"] = -s["net"] / s["used"]

        return stats

    def select_update_set(self, stats: Dict[str, Dict]) -> List[str]:
        """
        Select top-M skill files to refine based on worst local loss.

        Args:
            stats: Per-file statistics (keyed by specific_skill_file)

        Returns:
            List of specific_skill_file paths to update
        """
        # Filter to files that have regressions (Q-)
        # Files with only fixes (Q+) don't need refinement - they're working well
        files_with_evidence = {
            k: v for k, v in stats.items()
            if v["regressions"] > 0
        }

        if not files_with_evidence:
            print(f"\n✅ No files have regressions - no refinement needed")
            # Log files that only have fixes (for info)
            files_with_only_fixes = [k for k, v in stats.items() if v["fixes"] > 0 and v["regressions"] == 0]
            if files_with_only_fixes:
                print(f"  (Skipped {len(files_with_only_fixes)} files with only fixes, no regressions)")
            return []

        # Sort by local_loss (descending) - worst files first
        sorted_files = sorted(
            files_with_evidence.items(),
            key=lambda x: x[1]["local_loss"],
            reverse=True
        )

        # Take top M
        update_set = [file_key for file_key, _ in sorted_files[:self.M]]

        print(f"\nSelected {len(update_set)} files for refinement (from {len(files_with_evidence)} with evidence):")
        for file_key in update_set:
            s = stats[file_key]
            print(f"  {file_key}: net={s['net']:.2f}, loss={s['local_loss']:.3f}, fixes={s['fixes']}, regress={s['regressions']}")

        # Log skipped files (no evidence)
        skipped = len(stats) - len(files_with_evidence)
        if skipped > 0:
            print(f"  (Skipped {skipped} files with no evidence)")

        return update_set

    def _separate_common_and_subfield_files(self, files: List[str]) -> Tuple[List[str], List[str]]:
        """
        Separate files into common and subfield-specific categories.

        Args:
            files: List of file paths (e.g., ["common/visual_evidence.md", "equity/concept_confusion.md"])

        Returns:
            Tuple of (common_files, subfield_files)
        """
        common_files = []
        subfield_files = []

        for f in files:
            if f.startswith('common/') or '/common/' in f:
                common_files.append(f)
            else:
                subfield_files.append(f)

        return common_files, subfield_files

    def _is_common_file(self, file_path: str) -> bool:
        """Check if a file path is a common file."""
        return file_path.startswith('common/') or '/common/' in file_path

    def _separate_cards_by_file_type(
        self,
        cards: List,
        file_type: str = "common"
    ) -> List:
        """
        Filter cards by file type (common or specific).

        Args:
            cards: List of UnsolvedCard or EvidenceCard
            file_type: "common" or "specific"

        Returns:
            Filtered list of cards
        """
        result = []
        for card in cards:
            # Get file from card (different attributes for different card types)
            if hasattr(card, 'skill_used') and card.skill_used:
                file_path = card.skill_used.get('specific_file', '')
            elif hasattr(card, 'specific_skill_file'):
                file_path = card.specific_skill_file or ''
            else:
                file_path = ''

            is_common = self._is_common_file(file_path)

            if file_type == "common" and is_common:
                result.append(card)
            elif file_type == "specific" and not is_common:
                result.append(card)

        return result

    def _separate_evidence_by_file_type(
        self,
        Q_plus_all: Dict[str, List],
        Q_minus_all: Dict[str, List],
        file_type: str = "common"
    ) -> Tuple[Dict[str, List], Dict[str, List]]:
        """
        Filter evidence dictionaries by file type.

        Args:
            Q_plus_all: Dict mapping file -> Q+ cards
            Q_minus_all: Dict mapping file -> Q- cards
            file_type: "common" or "specific"

        Returns:
            Filtered (Q_plus, Q_minus) dicts
        """
        Q_plus_filtered = {}
        Q_minus_filtered = {}

        for file_key, cards in Q_plus_all.items():
            is_common = self._is_common_file(file_key)
            if (file_type == "common" and is_common) or (file_type == "specific" and not is_common):
                Q_plus_filtered[file_key] = cards

        for file_key, cards in Q_minus_all.items():
            is_common = self._is_common_file(file_key)
            if (file_type == "common" and is_common) or (file_type == "specific" and not is_common):
                Q_minus_filtered[file_key] = cards

        return Q_plus_filtered, Q_minus_filtered

    def _get_first_non_common_file(self, files: List[str]) -> Optional[str]:
        """
        Get first non-common file from list, or first common file if all are common.

        Used as fallback when LLM attribution fails.

        Args:
            files: List of file paths

        Returns:
            First non-common file, or first common file, or None if no valid files
        """
        if not files:
            return None

        # Prefer non-common files
        for f in files:
            if not f.startswith('common/') and '/common/' not in f and f != "SKILL.md":
                return f

        # Fall back to first common file (excluding SKILL.md)
        for f in files:
            if f != "SKILL.md":
                return f

        return None

    def _sample_evidence_by_file(
        self,
        evidence_by_file: Dict[str, Tuple[List, List]],
        P: int = None,
        N: int = None
    ) -> Dict[str, Tuple[List, List]]:
        """
        Sample P positives and N negatives from each file (V2: after grouping).

        Args:
            evidence_by_file: Dict mapping file -> (Q_plus_list, Q_minus_list)
            P: Max positives per file (uses self.default_P if None)
            N: Max negatives per file (uses self.default_N if None)

        Returns:
            Dict mapping file -> (sampled_Q_plus, sampled_Q_minus)
        """
        P = P if P is not None else self.default_P
        N = N if N is not None else self.default_N

        sampled = {}
        for file_key, (q_plus, q_minus) in evidence_by_file.items():
            # Sample positives using diverse sampling
            sampled_plus = self.evidence_collector._sample_diverse(q_plus, P)
            # Sample negatives using prioritized sampling (regressions first)
            sampled_minus = self.evidence_collector._sample_prioritized(q_minus, N)

            sampled[file_key] = (sampled_plus, sampled_minus)

            if len(q_plus) > P or len(q_minus) > N:
                print(f"  [{file_key}] Sampled: {len(sampled_plus)}/{len(q_plus)} Q+, {len(sampled_minus)}/{len(q_minus)} Q-")

        return sampled

    def _filter_evidence_by_qids(
        self,
        Q_plus: List,
        Q_minus: List,
        exclude_qids: set
    ) -> Tuple[List, List]:
        """
        Filter evidence cards, excluding specified QIDs.

        Used to remove already-fixed cases from Phase 2 optimization.

        Args:
            Q_plus: List of positive evidence cards
            Q_minus: List of negative evidence cards
            exclude_qids: Set of QIDs to exclude

        Returns:
            Tuple of (filtered_Q_plus, filtered_Q_minus)
        """
        filtered_plus = [c for c in Q_plus if c.qid not in exclude_qids]
        filtered_minus = [c for c in Q_minus if c.qid not in exclude_qids]
        return filtered_plus, filtered_minus

    def _file_exists(self, skill_file: str) -> bool:
        """Check if a skill file exists in the working skills directory."""
        return (self.working_skills_dir / skill_file).exists()

    def _get_subfield_folder(self, subfield: str) -> str:
        """Convert subfield name to folder name."""
        import re as _re
        name = subfield.lower().strip()
        name = _re.sub(r'[^a-z0-9_\s]', '', name)
        name = _re.sub(r'\s+', '_', name)
        return name

    def _format_gap_cards_for_new_skill(self, cards: list) -> str:
        """
        Format gap cards for new skill creation.

        Creates abstracted evidence without full question text to avoid memorization.

        Args:
            cards: List of UnsolvedCard objects

        Returns:
            Formatted evidence string
        """
        formatted = ["## Capability Gap Evidence\n"]
        formatted.append(f"These {len(cards)} cases reveal a gap in existing skills:\n")

        for i, card in enumerate(cards[:5], 1):  # Limit to 5 cases
            # Abstract the question - only show key concepts, not full text
            question_abstract = card.question[:150] + "..." if len(card.question) > 150 else card.question

            formatted.append(f"""
**Case {i}** (QID: {card.qid})

**Topic**: {card.signature.get('subfield', 'unknown')}
**Question Pattern**: {question_abstract}
**Ground Truth**: {card.ground_truth}

**What Was Tried**: {card.skill_used.get('specific_file', 'N/A')}
**Result**: Incorrect

**Root Cause**: {card.diagnosis_explanation or 'Capability gap - no skill covers this scenario'}

---
""")

        formatted.append("""
**Action Required**: Create a new sub-skill to handle this pattern.
- Focus on the CONCEPT/PATTERN, not specific question text
- Create generalizable procedures
- Avoid copying exact questions (prevents memorization)
""")

        return "\n".join(formatted)

    def _determine_new_skill_path(self, skill_content: str, subfield: str) -> str:
        """
        Determine the relative file path for a newly created skill file.

        Tries to extract from SKILL_MD_ENTRY line in generated content.
        Falls back to {subfield_folder}/new_patterns.md.

        Args:
            skill_content: Generated skill content
            subfield: Subfield name

        Returns:
            Relative path like "portfolio_management/new_patterns.md"
        """
        import re
        import time

        subfield_folder = self._get_subfield_folder(subfield)

        # Try to extract path from SKILL_MD_ENTRY line
        entry_line = self.textual_optimizer.extract_skill_md_entry_from_content(skill_content)
        if entry_line:
            # Parse: | `path/file.md` | ... |
            match = re.search(r'`([^`]+\.md)`', entry_line)
            if match:
                return match.group(1)

        # Fallback: {subfield_folder}/new_patterns_{timestamp}.md
        timestamp = int(time.time()) % 10000
        return f"{subfield_folder}/new_patterns_{timestamp}.md"

    def passes_validation_gate(
        self,
        val_metrics: Dict,
        prev_val_metrics: Optional[Dict]
    ) -> bool:
        """
        Check if new skills pass validation gate.

        Criteria:
        - Δval_regress_rate <= 0 (hard constraint)
        - Δval_acc >= -ε (ε ≈ 0.003)

        Args:
            val_metrics: New validation metrics
            prev_val_metrics: Previous validation metrics

        Returns:
            True if passed, False otherwise
        """
        if prev_val_metrics is None:
            return True  # First epoch always passes

        delta_regress = val_metrics["regress_rate"] - prev_val_metrics["regress_rate"]
        delta_acc = val_metrics["accuracy"] - prev_val_metrics["accuracy"]

        epsilon = 0.003

        # Hard constraints
        passes_regress = delta_regress <= 0
        passes_acc = delta_acc >= -epsilon

        print(f"\nValidation Gate:")
        print(f"  Δregress_rate: {delta_regress:.4f} {'✅' if passes_regress else '❌'} (must be ≤ 0)")
        print(f"  Δaccuracy: {delta_acc:.4f} {'✅' if passes_acc else '❌'} (must be ≥ {-epsilon})")

        return passes_regress and passes_acc

    def _collect_raw_evidence_qids(self, run_log: List) -> Tuple[Dict[str, set], Dict[str, set]]:
        """
        DEPRECATED: Use _collect_evidence_qids_from_grouped instead (V2).

        Collect ALL Q+/Q- QIDs from run log (unsampled), grouped by specific_skill_file.

        Used for stability analysis where sampling noise would cause false signals.

        Args:
            run_log: List of RunLogEntry

        Returns:
            Tuple of (raw_Q_plus, raw_Q_minus) where each is
            Dict[specific_skill_file -> set of qids]
        """
        from collections import defaultdict
        raw_Q_plus = defaultdict(set)
        raw_Q_minus = defaultdict(set)

        for entry in run_log:
            # Attribute to ALL files used (skip SKILL.md - it's always loaded)
            files = getattr(entry, 'all_skill_files', None)
            if not files:
                specific = entry.specific_skill_file
                files = [specific] if specific and specific != "SKILL.md" else []

            for file_key in files:
                # Skip SKILL.md - it's always loaded, not a specific skill file
                if file_key == "SKILL.md":
                    continue
                if entry.is_fix or entry.delta > 0:
                    raw_Q_plus[file_key].add(entry.qid)

                if entry.is_regress or entry.delta < 0:
                    raw_Q_minus[file_key].add(entry.qid)

        return dict(raw_Q_plus), dict(raw_Q_minus)

    def _collect_evidence_qids_from_grouped(
        self,
        evidence_by_file: Dict[str, Tuple[List, List]]
    ) -> Tuple[Dict[str, set], Dict[str, set]]:
        """
        Collect Q+/Q- QIDs from grouped evidence (V2: post-attribution).

        Uses attribution results for accurate file-to-evidence mapping.
        Used for stability analysis after attribution stage.

        Args:
            evidence_by_file: Dict mapping file -> (Q_plus_list, Q_minus_list)
                              Output of _group_evidence_by_file() after attribution

        Returns:
            Tuple of (raw_Q_plus, raw_Q_minus) where each is
            Dict[specific_skill_file -> set of qids]
        """
        from collections import defaultdict
        raw_Q_plus = defaultdict(set)
        raw_Q_minus = defaultdict(set)

        for file_key, (q_plus, q_minus) in evidence_by_file.items():
            if file_key == "SKILL.md":
                continue

            for card in q_plus:
                raw_Q_plus[file_key].add(card.qid)

            for card in q_minus:
                raw_Q_minus[file_key].add(card.qid)

        return dict(raw_Q_plus), dict(raw_Q_minus)

    def analyze_evidence_stability(
        self,
        raw_Q_plus: Dict[str, set],
        raw_Q_minus: Dict[str, set],
        epoch: int
    ):
        """
        Analyze evidence stability across epochs.

        Tracks which Q+/Q- cases remain stable, which are new, and which were converted.

        IMPORTANT: Uses full unsampled QID sets (not sampled evidence cards) to avoid
        false "lost"/"new" signals caused by sampling randomness.

        Args:
            raw_Q_plus: Full Q+ QIDs by specific_skill_file (from _collect_raw_evidence_qids)
            raw_Q_minus: Full Q- QIDs by specific_skill_file (from _collect_raw_evidence_qids)
            epoch: Current epoch number
        """
        print(f"\n[Evidence Stability Analysis - Epoch {epoch}]")

        if epoch == 1 or not self.prev_epoch_evidence:
            print("  First epoch - no previous evidence to compare")
            # Store current evidence for next epoch
            self.prev_epoch_evidence = {
                'Q_plus': raw_Q_plus,
                'Q_minus': raw_Q_minus
            }
            return

        # Current epoch evidence (already sets of qids)
        current_Q_plus = raw_Q_plus
        current_Q_minus = raw_Q_minus

        # Previous epoch evidence
        prev_Q_plus = self.prev_epoch_evidence.get('Q_plus', {})
        prev_Q_minus = self.prev_epoch_evidence.get('Q_minus', {})

        # Analyze for each skill
        all_skills = set(current_Q_plus.keys()) | set(current_Q_minus.keys()) | set(prev_Q_plus.keys()) | set(prev_Q_minus.keys())

        for skill in all_skills:
            curr_plus = current_Q_plus.get(skill, set())
            curr_minus = current_Q_minus.get(skill, set())
            prev_plus = prev_Q_plus.get(skill, set())
            prev_minus = prev_Q_minus.get(skill, set())

            # Calculate stability metrics
            stable_Q_plus = curr_plus & prev_plus  # Still Q+ in both epochs
            new_Q_plus = curr_plus - prev_plus     # Newly Q+ in this epoch
            lost_Q_plus = prev_plus - curr_plus    # Was Q+ but not anymore

            stable_Q_minus = curr_minus & prev_minus  # Still Q- in both epochs
            new_Q_minus = curr_minus - prev_minus     # Newly Q- in this epoch
            lost_Q_minus = prev_minus - curr_minus    # Was Q- but not anymore

            # Special cases: conversions
            Q_minus_to_Q_plus = prev_minus & curr_plus  # Was regression, now fixed!
            Q_plus_to_Q_minus = prev_plus & curr_minus  # Was fixed, now regression!

            # Print report for this skill
            if len(curr_plus) + len(curr_minus) + len(prev_plus) + len(prev_minus) > 0:
                print(f"\n  {skill}:")
                print(f"    Q+ (Fixes):")
                print(f"      Stable (still fixing):  {len(stable_Q_plus)}")
                print(f"      New (newly fixed):      {len(new_Q_plus)}")
                print(f"      Lost (no longer fixed): {len(lost_Q_plus)}")
                if Q_minus_to_Q_plus:
                    print(f"      🎉 Converted from Q-:   {len(Q_minus_to_Q_plus)} (regressions fixed!)")

                print(f"    Q- (Regressions):")
                print(f"      Stable (still breaking): {len(stable_Q_minus)}")
                print(f"      New (new regressions):   {len(new_Q_minus)}")
                print(f"      Lost (no longer break):  {len(lost_Q_minus)}")
                if Q_plus_to_Q_minus:
                    print(f"      ⚠️  Converted from Q+:    {len(Q_plus_to_Q_minus)} (fixes became regressions!)")

        # Store current evidence for next epoch
        self.prev_epoch_evidence = {
            'Q_plus': current_Q_plus,
            'Q_minus': current_Q_minus
        }

    def collect_residual_evidence(
        self,
        run_log: List,
        gen_func=None,  # Function to generate answer with skill
        eval_func=None,  # Function to evaluate answer
        epoch: int = 0
    ) -> Tuple[List[UnsolvedCard], List[UnsolvedCard]]:
        """
        Collect and analyze residual evidence (unsolved cases).

        Unsolved = baseline_wrong AND skill_wrong

        Returns:
            Tuple of (Q_plus_discover, Q_zero_gap)
            - Q_plus_discover: Cases where alternative skill solves it (router/trigger issue)
            - Q_zero_gap: Cases where no skill solves it (capability gap)
        """
        if not self.residual_collector:
            return [], []

        print(f"\n[Residual Evidence Collection - Epoch {epoch}]")

        # Step 1: Collect unsolved cases
        unsolved = self.residual_collector.collect_unsolved(run_log)

        if not unsolved:
            print("  No unsolved cases found")
            return [], []

        # Step 2: Probe alternative skills (if enabled and gen/eval functions provided)
        Q_plus_discover = []
        Q_zero_gap = []

        if self.enable_probe_alternatives and gen_func and eval_func:
            Q_plus_discover, Q_zero_gap = self.residual_collector.probe_alternative_skills(
                unsolved_cards=unsolved,
                router=self.router,
                gen_func=gen_func,
                eval_func=eval_func,
                max_cards=self.max_residual_cases
            )
        elif not self.enable_probe_alternatives:
            # Probing disabled - all unsolved cases go to Q_zero_gap
            # Still apply max_residual_cases limit
            print("  ⚠️  Probe alternative skills disabled (ENABLE_PROBE_ALTERNATIVES=false)")
            if self.max_residual_cases and len(unsolved) > self.max_residual_cases:
                print(f"  Limiting to {self.max_residual_cases} cases (from {len(unsolved)})")
                Q_zero_gap = unsolved[:self.max_residual_cases]
            else:
                Q_zero_gap = unsolved
        else:
            # Without probing, all unsolved cases go to Q_zero_gap
            # Still apply max_residual_cases limit
            print("  ⚠️  No gen/eval functions provided - skipping alternative skill probing")
            if self.max_residual_cases and len(unsolved) > self.max_residual_cases:
                print(f"  Limiting to {self.max_residual_cases} cases (from {len(unsolved)})")
                Q_zero_gap = unsolved[:self.max_residual_cases]
            else:
                Q_zero_gap = unsolved

        # Step 3: Diagnose root causes (pass router for skill content access)
        self.residual_collector.diagnose_unsolved(unsolved, Q_plus_discover, Q_zero_gap, router=self.router)

        # Step 4: Save residual evidence
        checkpoint_dir = self.checkpoint_mgr.checkpoint_dir / f"epoch_{epoch}"
        self.residual_collector.save_residual_evidence(
            Q_plus_discover, Q_zero_gap,
            str(checkpoint_dir),
            epoch
        )

        # Step 5: Print summary by action
        print(f"\n[Residual Evidence Summary]")
        by_action = self.residual_collector.group_by_action(Q_plus_discover, Q_zero_gap)
        for action, cards in by_action.items():
            print(f"  {action}: {len(cards)} cases")

        return Q_plus_discover, Q_zero_gap

    def process_discover_evidence(
        self,
        Q_plus_discover: List[UnsolvedCard],
        epoch: int
    ) -> Dict[str, str]:
        """
        Process Q+_discover evidence to generate trigger refinement suggestions.

        These are cases where the WRONG skill was selected, but another skill
        in the same subfield could solve it.

        Action: Update trigger keywords and "When to Use" sections.

        Args:
            Q_plus_discover: List of discover cards
            epoch: Current epoch

        Returns:
            Dict mapping skill_file -> formatted evidence for refinement
        """
        if not Q_plus_discover:
            return {}

        # Group by solving skill
        by_solving_skill = {}
        for card in Q_plus_discover:
            if card.solving_skill:
                if card.solving_skill not in by_solving_skill:
                    by_solving_skill[card.solving_skill] = []
                by_solving_skill[card.solving_skill].append(card)

        # Format evidence for each skill that needs trigger refinement
        trigger_evidence = {}
        for skill_file, cards in by_solving_skill.items():
            trigger_evidence[skill_file] = format_discover_evidence_for_refinement(
                cards, skill_file, max_cases=5
            )

        print(f"\n[Trigger Refinement Targets]")
        for skill_file, evidence in trigger_evidence.items():
            print(f"  {skill_file}: {len(by_solving_skill[skill_file])} cases need trigger updates")

        return trigger_evidence

    def process_gap_evidence(
        self,
        Q_zero_gap: List[UnsolvedCard],
        epoch: int
    ) -> Dict[str, str]:
        """
        Process Q0_gap evidence to identify capability gaps.

        These are cases where NO skill could solve the problem.

        Action: Add missing procedures/checks or create new sub-skills.

        Args:
            Q_zero_gap: List of gap cards
            epoch: Current epoch

        Returns:
            Dict mapping subfield -> formatted evidence for new skill creation
        """
        if not Q_zero_gap:
            return {}

        # Group by subfield
        by_subfield = self.residual_collector.group_by_subfield_and_skill(Q_zero_gap)

        # Format evidence for each subfield
        gap_evidence = {}
        for subfield, skill_cards in by_subfield.items():
            total_cases = sum(len(cards) for cards in skill_cards.values())
            gap_evidence[subfield] = format_gap_evidence_for_new_skill(
                Q_zero_gap, subfield, max_cases=5
            )

        print(f"\n[Capability Gap Analysis]")
        for subfield, evidence in gap_evidence.items():
            if evidence:
                print(f"  {subfield}: gaps identified")

        return gap_evidence

    def generate_diff_report(
        self,
        update_set: List[str],
        Q_plus_all: Dict,
        Q_minus_all: Dict,
        Q_plus_discover: Optional[List] = None,
        Q_zero_gap: Optional[List] = None
    ) -> str:
        """
        Generate diff report for checkpoint.

        Args:
            update_set: List of updated skill IDs
            Q_plus_all: All positive evidence
            Q_minus_all: All negative evidence
            Q_plus_discover: Discover evidence (optional)
            Q_zero_gap: Gap evidence (optional)

        Returns:
            Markdown diff report
        """
        report = f"# Skill Updates Report\n\n"
        report += f"**Timestamp**: {datetime.now().isoformat()}\n"
        report += f"**Updated Skills**: {len(update_set)}\n\n"

        # Standard Q+/Q- evidence
        report += "## Q+/Q- Evidence\n\n"
        for skill_id in update_set:
            report += f"### {skill_id}\n\n"
            report += f"- Positive evidence (Q+): {len(Q_plus_all.get(skill_id, []))}\n"
            report += f"- Negative evidence (Q-): {len(Q_minus_all.get(skill_id, []))}\n\n"

        # Residual evidence summary
        if Q_plus_discover or Q_zero_gap:
            report += "## Residual Evidence (Unsolved Cases)\n\n"

            if Q_plus_discover:
                report += f"### Q+_discover (Router/Trigger Issues): {len(Q_plus_discover)} cases\n\n"
                report += "These cases were solved by a different skill - need trigger updates.\n\n"

                # Group by solving skill
                by_solving = {}
                for card in Q_plus_discover:
                    solving = card.solving_skill or "unknown"
                    if solving not in by_solving:
                        by_solving[solving] = 0
                    by_solving[solving] += 1

                for skill, count in by_solving.items():
                    report += f"- `{skill}`: {count} cases\n"
                report += "\n"

            if Q_zero_gap:
                report += f"### Q0_gap (Capability Gaps): {len(Q_zero_gap)} cases\n\n"
                report += "These cases could not be solved by any skill - need new procedures or sub-skills.\n\n"

                # Group by diagnosis
                by_diagnosis = {}
                for card in Q_zero_gap:
                    diag = card.diagnosis or "unknown"
                    if diag not in by_diagnosis:
                        by_diagnosis[diag] = 0
                    by_diagnosis[diag] += 1

                for diag, count in by_diagnosis.items():
                    report += f"- `{diag}`: {count} cases\n"
                report += "\n"

        return report

    # ========================================================================
    # SANDBOX VERIFICATION & RETRY METHODS
    # ========================================================================

    def _refine_with_retry(
        self,
        file_key: str,
        Q_plus: List,
        Q_minus: List,
        epoch: int,
        gen_func=None,
        eval_func=None,
        is_common_file: bool = None
    ) -> Tuple[Optional[str], bool, Dict]:
        """
        Refine a skill file with sandbox verification and retry.

        After each refinement attempt, the updated content is tested against
        BOTH Q+ (should remain correct) and Q- (should be fixed) cases.

        If threshold not met after all attempts, accepts the best non-zero
        result instead of skipping entirely.

        Stores iteration logs for each attempt for analysis and recovery.

        For common files (is_common_file=True or auto-detected):
        - Uses combined content testing: updated common file + original specific files
        - Returns fixed_qids for exclusion in Phase 2

        Args:
            file_key: Specific skill file to refine
            Q_plus: Positive evidence cards
            Q_minus: Negative evidence cards
            epoch: Current epoch
            gen_func: Generation function for sandbox
            eval_func: Evaluation function for sandbox
            is_common_file: If True, use combined content testing (auto-detects if None)

        Returns:
            (updated_content, was_updated, iteration_summary)
            iteration_summary contains:
              - attempts: number of attempts made
              - history: list of attempt results
              - accepted_below_threshold: True if accepted with lower score
              - fixed_qids: set of Q- QIDs that were fixed (for common files)
        """
        can_sandbox = (self.sandbox_enabled and gen_func is not None and eval_func is not None)

        # Auto-detect common file if not specified
        if is_common_file is None:
            is_common_file = file_key.startswith('common/') or '/common/' in file_key

        # Minimum acceptable thresholds for Q+ and Q- individually
        # Both must pass their own threshold to be accepted
        MIN_Q_PLUS_RATE = cfg('sandbox.min_q_plus_rate') or float(os.getenv('MIN_Q_PLUS_RATE', '0.5'))
        MIN_Q_MINUS_RATE = cfg('sandbox.min_q_minus_rate') or float(os.getenv('MIN_Q_MINUS_RATE', '0.1'))
        SMALL_SAMPLE_THRESHOLD = 2  # Q+ <= 2 is considered small sample

        def is_acceptable(metrics: dict) -> bool:
            """Check if attempt meets minimum thresholds.

            For small Q+ samples (<=2 cases), we ignore Q+ and only check Q- >= 10%.
            This avoids blocking refinement due to a single noisy Q+ case.
            """
            q_plus_total = metrics.get('q_plus_total', 0)
            q_minus_total = metrics.get('q_minus_total', 0)
            q_plus_rate = metrics.get('q_plus_rate', 1.0)
            q_minus_rate = metrics.get('q_minus_rate', 0.0)

            # Small sample handling: when Q+ has only 1-2 cases, ignore Q+
            if q_plus_total > 0 and q_plus_total <= SMALL_SAMPLE_THRESHOLD:
                # Only check Q- >= 10%, ignore Q+ regression
                q_minus_ok = (q_minus_total == 0) or (q_minus_rate >= MIN_Q_MINUS_RATE)
                return q_minus_ok

            # Normal case: both Q+ and Q- must meet their thresholds
            q_plus_ok = (q_plus_total == 0) or (q_plus_rate >= MIN_Q_PLUS_RATE)
            q_minus_ok = (q_minus_total == 0) or (q_minus_rate >= MIN_Q_MINUS_RATE)

            return q_plus_ok and q_minus_ok

        # Track best attempt across all iterations
        best_content = None
        best_score = 0.0
        best_metrics = {}
        best_is_acceptable = False
        iteration_history = []

        for attempt in range(1, self.max_refine_attempts + 1):
            # Refine
            updated_content, was_updated = self.textual_optimizer.refine_skill(
                skill=self.skill_ref,
                Q_plus=Q_plus,
                Q_minus=Q_minus,
                epoch=epoch,
                specific_skill_file=file_key
            )

            if not was_updated or not updated_content:
                # No content generated, check if we have a best from previous attempts
                if best_content and best_is_acceptable:
                    q_plus_rate = best_metrics.get('q_plus_rate', 1.0)
                    q_minus_rate = best_metrics.get('q_minus_rate', 0.0)
                    print(f"    ⚠️  No new content at attempt {attempt}, using best previous (Q+={q_plus_rate:.0%}, Q-={q_minus_rate:.0%})")
                    return best_content, True, {
                        'attempts': attempt,
                        'history': iteration_history,
                        'accepted_below_threshold': True,
                        **best_metrics
                    }
                return None, False, {'attempts': attempt, 'history': iteration_history, 'skipped': True, 'fixed_qids': []}

            # Sandbox verify (only if gen_func/eval_func provided and sandbox enabled)
            if can_sandbox:
                # Use full sandbox that tests both Q+ and Q-
                # For common files, use combined content testing
                # Pass Q_plus/Q_minus to ensure sandbox uses SAME data as refinement
                passed, metrics, detail = self._sandbox_verify_full(
                    file_key, updated_content, gen_func, eval_func,
                    use_combined_content=is_common_file,
                    q_plus_cards=Q_plus,
                    q_minus_cards=Q_minus
                )

                # Get combined score
                score = metrics.get('combined_score', 0.0)

                # Record attempt
                attempt_record = {
                    'attempt': attempt,
                    'passed': passed,
                    'score': score,
                    'q_plus_rate': metrics.get('q_plus_rate', 0),
                    'q_minus_rate': metrics.get('q_minus_rate', 0),
                    'content_length': len(updated_content)
                }
                iteration_history.append(attempt_record)

                # Save iteration log
                self.iteration_logger.save_iteration_log(
                    file_key=file_key,
                    epoch=epoch,
                    attempt=attempt,
                    content=updated_content,
                    metrics=metrics,
                    passed=passed
                )

                # Track best (even if not passed) - prefer acceptable attempts
                attempt_acceptable = is_acceptable(metrics)
                # Update best if: (1) this is acceptable and previous wasn't, or (2) same acceptability but higher score
                if (attempt_acceptable and not best_is_acceptable) or \
                   (attempt_acceptable == best_is_acceptable and score > best_score):
                    best_score = score
                    best_content = updated_content
                    best_metrics = metrics
                    best_is_acceptable = attempt_acceptable

                if passed:
                    print(f"    ✅ Sandbox passed (attempt {attempt}): {detail}")
                    return updated_content, True, {
                        'attempts': attempt,
                        'history': iteration_history,
                        'accepted_below_threshold': False,
                        **metrics
                    }
                else:
                    print(f"    ❌ Sandbox failed (attempt {attempt}/{self.max_refine_attempts}): {detail}")
                    if attempt < self.max_refine_attempts:
                        print(f"    Retrying refinement...")
                        continue
                    else:
                        # All attempts failed - use best if it meets minimum thresholds
                        if best_content and best_is_acceptable:
                            q_plus_total = best_metrics.get('q_plus_total', 0)
                            q_plus_rate = best_metrics.get('q_plus_rate', 1.0)
                            q_minus_rate = best_metrics.get('q_minus_rate', 0.0)
                            # Show appropriate message based on whether small sample rule was used
                            if q_plus_total > 0 and q_plus_total <= SMALL_SAMPLE_THRESHOLD:
                                print(f"    📊 Using best attempt [small Q+ sample: {q_plus_total}, ignoring Q+] (Q-={q_minus_rate:.0%}>={MIN_Q_MINUS_RATE:.0%})")
                            else:
                                print(f"    📊 Using best attempt (Q+={q_plus_rate:.0%}>={MIN_Q_PLUS_RATE:.0%}, Q-={q_minus_rate:.0%}>={MIN_Q_MINUS_RATE:.0%})")
                            return best_content, True, {
                                'attempts': attempt,
                                'history': iteration_history,
                                'accepted_below_threshold': True,
                                'small_sample_accepted': q_plus_total <= SMALL_SAMPLE_THRESHOLD,
                                **best_metrics
                            }
                        else:
                            q_plus_total = best_metrics.get('q_plus_total', 0) if best_metrics else 0
                            q_plus_rate = best_metrics.get('q_plus_rate', 0) if best_metrics else 0
                            q_minus_rate = best_metrics.get('q_minus_rate', 0) if best_metrics else 0
                            # Show appropriate message based on sample size
                            if q_plus_total > 0 and q_plus_total <= SMALL_SAMPLE_THRESHOLD:
                                print(f"    ⏭️  Skipping {file_key} [small Q+ sample: {q_plus_total}] - Q-={q_minus_rate:.0%}<{MIN_Q_MINUS_RATE:.0%}")
                            else:
                                print(f"    ⏭️  Skipping {file_key} - best attempt below thresholds (Q+={q_plus_rate:.0%}<{MIN_Q_PLUS_RATE:.0%} or Q-={q_minus_rate:.0%}<{MIN_Q_MINUS_RATE:.0%})")
                            return None, False, {
                                'attempts': attempt,
                                'history': iteration_history,
                                'skipped': True,
                                'best_score': best_score,
                                'fixed_qids': []
                            }
            else:
                # No sandbox available, accept as-is
                return updated_content, True, {'attempts': 1, 'history': [], 'no_sandbox': True, 'fixed_qids': []}

        return None, False, {'attempts': self.max_refine_attempts, 'history': iteration_history, 'skipped': True, 'fixed_qids': []}

    def _update_description_procedure_with_retry(
        self,
        file_key: str,
        gap_cards: list,
        epoch: int,
        gen_func=None,
        eval_func=None
    ) -> Tuple[Optional[str], bool]:
        """
        Update Description/Procedure with sandbox verification and retry.

        For Q0_gap cases: if threshold not reached after all attempts,
        keeps the best result (highest non-zero solve_rate) instead of skipping.

        Stores iteration logs for each attempt for analysis and recovery.

        Args:
            file_key: Specific skill file to update
            gap_cards: UnsolvedCards with incomplete_procedure diagnosis
            epoch: Current epoch
            gen_func: Generation function for sandbox
            eval_func: Evaluation function for sandbox

        Returns:
            (updated_content, was_updated)
        """
        can_sandbox = (self.sandbox_enabled and gen_func is not None and eval_func is not None)

        # Track best attempt for Q0_gap (keep best non-zero result if threshold not met)
        best_content = None
        best_solve_rate = 0.0

        for attempt in range(1, self.max_refine_attempts + 1):
            updated_content, was_updated = self.textual_optimizer.update_description_procedure(
                skill=self.skill_ref,
                gap_cards=gap_cards,
                specific_skill_file=file_key,
                epoch=epoch
            )

            if not was_updated or not updated_content:
                # If no update generated, return best so far (if any)
                if best_content and best_solve_rate > 0:
                    print(f"      ⚠️  No new content, using best previous (solve_rate={best_solve_rate:.0%})")
                    return best_content, True
                return None, False

            # Check if LLM returned NEEDS_NEW_PATTERN
            if "NEEDS_NEW_PATTERN" in updated_content:
                print(f"      📋 LLM detected new pattern needed - should create new skill file")
                # Return special marker for caller to handle reclassification
                return "NEEDS_NEW_PATTERN", False

            if can_sandbox:
                passed, solve_rate, detail, gap_details = self._sandbox_verify_gap_update(
                    file_key, updated_content, gap_cards, gen_func, eval_func
                )

                # Track best non-zero result
                if solve_rate > best_solve_rate:
                    best_solve_rate = solve_rate
                    best_content = updated_content

                # Save iteration log with per-question details
                self.iteration_logger.save_iteration_log(
                    file_key=f"{file_key}_desc_proc",
                    epoch=epoch,
                    attempt=attempt,
                    content=updated_content,
                    metrics={
                        'solve_rate': solve_rate,
                        'detail': detail,
                        'type': 'description_procedure',
                        'gap_total': len(gap_details),
                        'gap_solved': sum(1 for d in gap_details if d.get('solved')),
                        'gap_details': gap_details
                    },
                    passed=passed
                )

                if passed:
                    print(f"      ✅ Sandbox passed (attempt {attempt}): {detail}")
                    return updated_content, True
                else:
                    print(f"      ❌ Sandbox failed (attempt {attempt}/{self.max_refine_attempts}): {detail}")
                    if attempt < self.max_refine_attempts:
                        continue
                    else:
                        # All attempts failed - use best non-zero result for Q0_gap
                        if best_content and best_solve_rate > 0:
                            print(f"      📊 Using best attempt (solve_rate={best_solve_rate:.0%}) for Q0_gap")
                            return best_content, True
                        else:
                            print(f"      ⏭️  Skipping update_description_procedure for {file_key} (no improvement)")
                            return None, False
            else:
                return updated_content, True

        return None, False

    def _update_example_with_retry(
        self,
        file_key: str,
        gap_cards: list,
        epoch: int,
        gen_func=None,
        eval_func=None
    ) -> Tuple[Optional[str], bool]:
        """
        Update Example section with sandbox verification and retry.

        For Q0_gap cases: if threshold not reached after all attempts,
        keeps the best result (highest non-zero solve_rate) instead of skipping.

        Stores iteration logs for each attempt for analysis and recovery.

        Args:
            file_key: Specific skill file to update
            gap_cards: UnsolvedCards with weak_example (standard) or weak_procedure_example (PoT) diagnosis
            epoch: Current epoch
            gen_func: Generation function for sandbox
            eval_func: Evaluation function for sandbox

        Returns:
            (updated_content, was_updated)
        """
        can_sandbox = (self.sandbox_enabled and gen_func is not None and eval_func is not None)

        # Track best attempt for Q0_gap (keep best non-zero result if threshold not met)
        best_content = None
        best_solve_rate = 0.0

        for attempt in range(1, self.max_refine_attempts + 1):
            updated_content, was_updated = self.textual_optimizer.update_example(
                skill=self.skill_ref,
                gap_cards=gap_cards,
                specific_skill_file=file_key,
                epoch=epoch
            )

            if not was_updated or not updated_content:
                # If no update generated, return best so far (if any)
                if best_content and best_solve_rate > 0:
                    print(f"      ⚠️  No new content, using best previous (solve_rate={best_solve_rate:.0%})")
                    return best_content, True
                return None, False

            # Check if LLM returned NEEDS_NEW_PATTERN
            if "NEEDS_NEW_PATTERN" in updated_content:
                print(f"      📋 LLM detected new pattern needed - should create new skill file")
                return "NEEDS_NEW_PATTERN", False

            if can_sandbox:
                passed, solve_rate, detail, gap_details = self._sandbox_verify_gap_update(
                    file_key, updated_content, gap_cards, gen_func, eval_func
                )

                # Track best non-zero result
                if solve_rate > best_solve_rate:
                    best_solve_rate = solve_rate
                    best_content = updated_content

                # Save iteration log with per-question details
                self.iteration_logger.save_iteration_log(
                    file_key=f"{file_key}_example",
                    epoch=epoch,
                    attempt=attempt,
                    content=updated_content,
                    metrics={
                        'solve_rate': solve_rate,
                        'detail': detail,
                        'type': 'example',
                        'gap_total': len(gap_details),
                        'gap_solved': sum(1 for d in gap_details if d.get('solved')),
                        'gap_details': gap_details
                    },
                    passed=passed
                )

                if passed:
                    print(f"      ✅ Sandbox passed (attempt {attempt}): {detail}")
                    return updated_content, True
                else:
                    print(f"      ❌ Sandbox failed (attempt {attempt}/{self.max_refine_attempts}): {detail}")
                    if attempt < self.max_refine_attempts:
                        continue
                    else:
                        # All attempts failed - use best non-zero result for Q0_gap
                        if best_content and best_solve_rate > 0:
                            print(f"      📊 Using best attempt (solve_rate={best_solve_rate:.0%}) for Q0_gap")
                            return best_content, True
                        else:
                            print(f"      ⏭️  Skipping update_example for {file_key} (no improvement)")
                            return None, False
            else:
                return updated_content, True

        return None, False

    def _update_when_to_use_with_retry(
        self,
        file_key: str,
        gap_cards: list,
        epoch: int,
        gen_func=None,
        eval_func=None
    ) -> Tuple[Optional[str], bool]:
        """
        Update "When to Use" section with sandbox verification and retry.

        For Q0_gap cases: if threshold not reached after all attempts,
        keeps the best result (highest non-zero solve_rate) instead of skipping.

        Stores iteration logs for each attempt for analysis and recovery.

        Args:
            file_key: Specific skill file to update
            gap_cards: UnsolvedCards with trigger_mismatch diagnosis
            epoch: Current epoch
            gen_func: Generation function for sandbox
            eval_func: Evaluation function for sandbox

        Returns:
            (updated_content, was_updated)
        """
        can_sandbox = (self.sandbox_enabled and gen_func is not None and eval_func is not None)

        # Track best attempt for Q0_gap (keep best non-zero result if threshold not met)
        best_content = None
        best_solve_rate = 0.0

        for attempt in range(1, self.max_refine_attempts + 1):
            updated_content, was_updated = self.textual_optimizer.update_when_to_use(
                skill=self.skill_ref,
                gap_cards=gap_cards,
                specific_skill_file=file_key,
                epoch=epoch
            )

            if not was_updated or not updated_content:
                # If no update generated, return best so far (if any)
                if best_content and best_solve_rate > 0:
                    print(f"      ⚠️  No new content, using best previous (solve_rate={best_solve_rate:.0%})")
                    return best_content, True
                return None, False

            if can_sandbox:
                passed, solve_rate, detail, gap_details = self._sandbox_verify_gap_update(
                    file_key, updated_content, gap_cards, gen_func, eval_func
                )

                # Track best non-zero result
                if solve_rate > best_solve_rate:
                    best_solve_rate = solve_rate
                    best_content = updated_content

                # Save iteration log with per-question details
                self.iteration_logger.save_iteration_log(
                    file_key=f"{file_key}_when_to_use",
                    epoch=epoch,
                    attempt=attempt,
                    content=updated_content,
                    metrics={
                        'solve_rate': solve_rate,
                        'detail': detail,
                        'type': 'when_to_use',
                        'gap_total': len(gap_details),
                        'gap_solved': sum(1 for d in gap_details if d.get('solved')),
                        'gap_details': gap_details
                    },
                    passed=passed
                )

                if passed:
                    print(f"      ✅ Sandbox passed (attempt {attempt}): {detail}")
                    return updated_content, True
                else:
                    print(f"      ❌ Sandbox failed (attempt {attempt}/{self.max_refine_attempts}): {detail}")
                    if attempt < self.max_refine_attempts:
                        continue
                    else:
                        # All attempts failed - use best non-zero result for Q0_gap
                        if best_content and best_solve_rate > 0:
                            print(f"      📊 Using best attempt (solve_rate={best_solve_rate:.0%}) for Q0_gap")
                            return best_content, True
                        else:
                            print(f"      ⏭️  Skipping update_when_to_use for {file_key} (no improvement)")
                            return None, False
            else:
                return updated_content, True

        return None, False

    def _add_checks_and_constraints_with_retry(
        self,
        file_key: str,
        gap_cards: list,
        epoch: int,
        gen_func=None,
        eval_func=None
    ) -> Tuple[Optional[str], bool]:
        """
        Add CHECK steps and Common Bugs with sandbox verification and retry (PoT mode).

        For Q0_gap cases: if threshold not reached after all attempts,
        keeps the best result (highest non-zero solve_rate) instead of skipping.

        Stores iteration logs for each attempt for analysis and recovery.

        Args:
            file_key: Specific skill file to update
            gap_cards: UnsolvedCards with need_checks diagnosis (PoT mode)
            epoch: Current epoch
            gen_func: Generation function for sandbox
            eval_func: Evaluation function for sandbox

        Returns:
            (updated_content, was_updated)
        """
        can_sandbox = (self.sandbox_enabled and gen_func is not None and eval_func is not None)

        # Track best attempt for Q0_gap (keep best non-zero result if threshold not met)
        best_content = None
        best_solve_rate = 0.0

        for attempt in range(1, self.max_refine_attempts + 1):
            updated_content, was_updated = self.textual_optimizer.add_checks_and_constraints(
                skill=self.skill_ref,
                gap_cards=gap_cards,
                specific_skill_file=file_key,
                epoch=epoch
            )

            if not was_updated or not updated_content:
                # If no update generated, return best so far (if any)
                if best_content and best_solve_rate > 0:
                    print(f"      ⚠️  No new content, using best previous (solve_rate={best_solve_rate:.0%})")
                    return best_content, True
                return None, False

            # Check if LLM returned NEEDS_NEW_PATTERN
            if "NEEDS_NEW_PATTERN" in updated_content:
                print(f"      📋 LLM detected new pattern needed - should create new skill file")
                return "NEEDS_NEW_PATTERN", False

            if can_sandbox:
                passed, solve_rate, detail, gap_details = self._sandbox_verify_gap_update(
                    file_key, updated_content, gap_cards, gen_func, eval_func
                )

                # Track best non-zero result
                if solve_rate > best_solve_rate:
                    best_solve_rate = solve_rate
                    best_content = updated_content

                # Save iteration log with per-question details
                self.iteration_logger.save_iteration_log(
                    file_key=f"{file_key}_checks",
                    epoch=epoch,
                    attempt=attempt,
                    content=updated_content,
                    metrics={
                        'solve_rate': solve_rate,
                        'detail': detail,
                        'type': 'add_checks_and_constraints',
                        'gap_total': len(gap_details),
                        'gap_solved': sum(1 for d in gap_details if d.get('solved')),
                        'gap_details': gap_details
                    },
                    passed=passed
                )

                if passed:
                    print(f"      ✅ Sandbox passed (attempt {attempt}): {detail}")
                    return updated_content, True
                else:
                    print(f"      ❌ Sandbox failed (attempt {attempt}/{self.max_refine_attempts}): {detail}")
                    if attempt < self.max_refine_attempts:
                        continue
                    else:
                        # All attempts failed - use best non-zero result for Q0_gap
                        if best_content and best_solve_rate > 0:
                            print(f"      📊 Using best attempt (solve_rate={best_solve_rate:.0%}) for Q0_gap")
                            return best_content, True
                        else:
                            print(f"      ⏭️  Skipping add_checks_and_constraints for {file_key} (no improvement)")
                            return None, False
            else:
                return updated_content, True

        return None, False

    def _coverage_refine_with_retry(
        self,
        file_key: str,
        gap_cards: list,
        diagnosis_type: str,  # Action name: update_description_procedure, update_example, update_when_to_use, add_checks_and_constraints
        epoch: int,
        gen_func=None,
        eval_func=None
    ) -> Tuple[Optional[str], bool, List[str]]:
        """
        Unified coverage refinement with sandbox verification and retry.

        Uses COVERAGE_REFINEMENT_PROMPT with dynamic guidance injection.
        Returns new pattern names for SKILL.md update.

        Args:
            file_key: Specific skill file to update
            gap_cards: UnsolvedCards with the specified action type
            diagnosis_type: Action name - one of:
                Non-PoT: update_description_procedure, update_example, update_when_to_use
                PoT: update_example, add_checks_and_constraints
            epoch: Current epoch
            gen_func: Generation function for sandbox
            eval_func: Evaluation function for sandbox

        Returns:
            (updated_content, was_updated, new_pattern_names)
        """
        can_sandbox = (self.sandbox_enabled and gen_func is not None and eval_func is not None)

        # Track best attempt for Q0_gap (keep best non-zero result if threshold not met)
        best_content = None
        best_solve_rate = 0.0
        best_new_names = []

        for attempt in range(1, self.max_refine_attempts + 1):
            updated_content, was_updated, new_names = self.textual_optimizer.coverage_refine(
                skill=self.skill_ref,
                gap_cards=gap_cards,
                specific_skill_file=file_key,
                diagnosis_type=diagnosis_type,
                epoch=epoch
            )

            if not was_updated or not updated_content:
                # If no update generated, return best so far (if any)
                if best_content and best_solve_rate > 0:
                    print(f"      ⚠️  No new content, using best previous (solve_rate={best_solve_rate:.0%})")
                    return best_content, True, best_new_names
                return None, False, []

            if can_sandbox:
                passed, solve_rate, detail, gap_details = self._sandbox_verify_gap_update(
                    file_key, updated_content, gap_cards, gen_func, eval_func
                )

                # Track best non-zero result
                if solve_rate > best_solve_rate:
                    best_solve_rate = solve_rate
                    best_content = updated_content
                    best_new_names = new_names

                # Save iteration log with per-question details
                self.iteration_logger.save_iteration_log(
                    file_key=f"{file_key}_coverage_{diagnosis_type}",
                    epoch=epoch,
                    attempt=attempt,
                    content=updated_content,
                    metrics={
                        'solve_rate': solve_rate,
                        'detail': detail,
                        'type': f'coverage_{diagnosis_type}',
                        'gap_total': len(gap_details),
                        'gap_solved': sum(1 for d in gap_details if d.get('solved')),
                        'gap_details': gap_details,
                        'new_patterns': new_names
                    },
                    passed=passed
                )

                if passed:
                    print(f"      ✅ Sandbox passed (attempt {attempt}): {detail}")
                    return updated_content, True, new_names
                else:
                    print(f"      ❌ Sandbox failed (attempt {attempt}/{self.max_refine_attempts}): {detail}")
                    if attempt < self.max_refine_attempts:
                        continue
                    else:
                        # All attempts failed - use best non-zero result for Q0_gap
                        if best_content and best_solve_rate > 0:
                            print(f"      📊 Using best attempt (solve_rate={best_solve_rate:.0%}) for Q0_gap")
                            return best_content, True, best_new_names
                        else:
                            print(f"      ⏭️  Skipping coverage refinement for {file_key}/{diagnosis_type} (no improvement)")
                            return None, False, []
            else:
                return updated_content, True, new_names

        return None, False, []

    def _update_skill_md_for_new_patterns(
        self,
        file_key: str,
        new_pattern_names: List[str]
    ) -> bool:
        """
        Update SKILL.md when new patterns are added to an existing file.

        Adds new pattern names to the "Key Patterns" column for the file.
        Thread-safe: uses lock for concurrent access.

        Args:
            file_key: The skill file that received new patterns
            new_pattern_names: List of new pattern names added

        Returns:
            True if SKILL.md was updated successfully
        """
        if not new_pattern_names:
            return False

        skill_md_path = self.working_skills_dir / "SKILL.md"
        if not skill_md_path.exists():
            print(f"      ⚠️  SKILL.md not found, cannot update for new patterns")
            return False

        # Use lock for thread-safe SKILL.md updates
        with self._skill_md_lock:
            try:
                with open(skill_md_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Find the table row for this file and update Key Patterns
                # Pattern: | `file_key` | Subfield | Error Type | Pattern1, Pattern2 |
                file_pattern = re.escape(file_key)
                row_regex = re.compile(
                    rf'(\|\s*`?{file_pattern}`?\s*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
                    re.IGNORECASE
                )

                def add_patterns(match):
                    prefix = match.group(1)
                    existing_patterns = match.group(2).strip()
                    suffix = match.group(3)
                    # Add new patterns
                    new_patterns_str = ", ".join(new_pattern_names)
                    if existing_patterns:
                        updated_patterns = f" {existing_patterns}, {new_patterns_str} "
                    else:
                        updated_patterns = f" {new_patterns_str} "
                    return f"{prefix}{updated_patterns}{suffix}"

                new_content, count = row_regex.subn(add_patterns, content)

                if count > 0:
                    with open(skill_md_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"      ✅ SKILL.md updated with new patterns: {', '.join(new_pattern_names)}")
                    return True
                else:
                    print(f"      ⚠️  Could not find {file_key} in SKILL.md table")
                    return False

            except Exception as e:
                print(f"      ❌ Failed to update SKILL.md: {e}")
                return False

    def train(
        self,
        train_data: List[Dict],  # Training dataset
        val_data: List[Dict],  # Validation dataset
        max_epochs: int = 10,
        run_system_fn=None,  # Function to run system on data
        gen_func=None,  # Function for residual probing: gen_func(question, context, options, skill_content) -> (answer, explanation)
        eval_func=None  # Function for residual probing: eval_func(question, context, answer, explanation, ground_truth) -> score
    ):
        """
        Main training loop.

        Args:
            train_data: Training dataset
            val_data: Validation dataset
            max_epochs: Maximum number of epochs
            run_system_fn: Function that runs the system and returns run log
                          Signature: fn(data, skills_router) -> List[RunLogEntry]
            gen_func: Function for residual skill probing (optional)
                     Signature: fn(question, context, options, skill_content) -> (answer, explanation)
            eval_func: Function for residual evaluation (optional)
                      Signature: fn(question, context, answer, explanation, ground_truth) -> score
        """
        print("="*80)
        print("Skill Training Loop")
        print("="*80)

        prev_val_metrics = None

        for epoch in range(1, max_epochs + 1):
            print(f"\n{'='*80}")
            print(f"Epoch {epoch}/{max_epochs}")
            print(f"{'='*80}")

            # (1) Run TRAIN with current skills
            print("\n[1] Running train set...")
            if run_system_fn:
                # Pass split parameter if function accepts it
                sig = inspect.signature(run_system_fn)
                if 'split' in sig.parameters:
                    self.logger.train_log = run_system_fn(train_data, self.router, split="train")
                else:
                    self.logger.train_log = run_system_fn(train_data, self.router)
            else:
                # Placeholder: In production, this calls actual system
                print("  ⚠️  No run_system_fn provided - using placeholder")
                self.logger.train_log = []

            train_metrics = self.compute_metrics(self.logger.train_log)
            print(f"  Train accuracy: {train_metrics.get('accuracy', 0):.2%}")
            print(f"  Train loss: {train_metrics.get('loss', 0):.4f}")

            # (2) Aggregate evidence
            print("\n[2] Aggregating evidence...")

            skill_stats = self.compute_skill_stats(self.logger.train_log)

            # V2: Collect all raw evidence without grouping or sampling
            # Attribution determines file responsibility AFTER this
            all_Q_plus, all_Q_minus = self.evidence_collector.collect_evidence(
                self.logger.train_log,
                self.skill_set_name
            )

            # (2.5) Attribution analysis ALWAYS runs (V2)
            # Populates card.attribution_result for accurate file grouping
            if all_Q_plus or all_Q_minus:
                print("\n[2.5] Performing attribution analysis...")
                self._perform_batch_attribution(all_Q_plus, all_Q_minus)

            # Group evidence by attributed files (V2: after attribution)
            evidence_by_file = self._group_evidence_by_file(all_Q_plus, all_Q_minus)

            # V2: NO sampling here - sampling moved to before Safety phase
            # This allows coverage_fixed to be added to Q+ before sampling

            # Build Q_plus_all / Q_minus_all keyed by specific_skill_file (unsampled)
            Q_plus_all = {}
            Q_minus_all = {}
            for file_key, (fp, fm) in evidence_by_file.items():
                Q_plus_all[file_key] = fp
                Q_minus_all[file_key] = fm

            # When attribution is enabled, recompute stats from evidence (post-attribution)
            # This ensures file selection uses attributed files, not original files
            if self.enable_deep_analysis and evidence_by_file:
                print("\n  Recomputing stats from attributed evidence...")
                skill_stats = self._compute_stats_from_evidence(evidence_by_file)
                print(f"  Stats for {len(skill_stats)} files (post-attribution)")

            # (2.6) Analyze evidence stability across epochs (V2: uses attribution results)
            # Uses evidence_by_file (post-attribution) for accurate file attribution
            raw_Q_plus, raw_Q_minus = self._collect_evidence_qids_from_grouped(evidence_by_file)
            self.analyze_evidence_stability(raw_Q_plus, raw_Q_minus, epoch)

            # (2.7) Collect residual evidence (unsolved cases)
            Q_plus_discover = []
            Q_zero_gap = []
            trigger_evidence = {}
            gap_evidence = {}

            if self.enable_residual_analysis:
                print("\n[2.7] Collecting residual evidence (unsolved cases)...")
                Q_plus_discover, Q_zero_gap = self.collect_residual_evidence(
                    run_log=self.logger.train_log,
                    gen_func=gen_func,
                    eval_func=eval_func,
                    epoch=epoch
                )

                # Process discover evidence for trigger refinement
                if Q_plus_discover:
                    trigger_evidence = self.process_discover_evidence(Q_plus_discover, epoch)

                # Process gap evidence for new skill creation
                if Q_zero_gap:
                    gap_evidence = self.process_gap_evidence(Q_zero_gap, epoch)

            # (3) Select update set
            print("\n[3] Selecting skills to update...")
            update_set = self.select_update_set(skill_stats)

            # =========================================================================
            # V2 TWO-PHASE REFINEMENT: Common Files First, Then Specific Files
            # Each file type goes through: Coverage (Q0_gap) → Verification → Safety (Q+/Q-)
            # =========================================================================
            print("\n[4] V2 Two-Phase Refinement: Common → Specific")
            updates_applied = 0

            # Store original Q+ for post-coverage verification
            original_Q_plus_flat = []
            for cards in Q_plus_all.values():
                original_Q_plus_flat.extend(cards)

            original_Q_minus_flat = []
            for cards in Q_minus_all.values():
                original_Q_minus_flat.extend(cards)

            # Process common files first (both phases), then specific files (both phases)
            # This ensures common patterns are stabilized before refining specific patterns
            for current_file_type in ["common", "specific"]:
                print(f"\n{'='*60}")
                print(f"  STAGE: {current_file_type.upper()} FILES")
                print(f"{'='*60}")

                # Filter Q0_gap, Q+, Q- for current file type
                Q_zero_gap_filtered = self._separate_cards_by_file_type(Q_zero_gap, current_file_type) if Q_zero_gap else []
                Q_plus_filtered, Q_minus_filtered = self._separate_evidence_by_file_type(
                    Q_plus_all, Q_minus_all, current_file_type
                )

                # Flatten for this stage (deduplicate by QID - same card may appear in multiple files)
                stage_Q_plus_flat = []
                seen_qids = set()
                for cards in Q_plus_filtered.values():
                    for card in cards:
                        if card.qid not in seen_qids:
                            seen_qids.add(card.qid)
                            stage_Q_plus_flat.append(card)

                stage_Q_minus_flat = []
                seen_qids = set()
                for cards in Q_minus_filtered.values():
                    for card in cards:
                        if card.qid not in seen_qids:
                            seen_qids.add(card.qid)
                            stage_Q_minus_flat.append(card)

                print(f"  Q0_gap: {len(Q_zero_gap_filtered)}, Q+: {len(stage_Q_plus_flat)}, Q-: {len(stage_Q_minus_flat)}")

                # ========== PHASE 4.A: Coverage (Q0_gap) ==========
                stage_updates = 0
                modified_files = set()  # Track files modified during Coverage

                if Q_zero_gap_filtered:
                    # Group Q0_gap by action type
                    by_action = {}
                    for card in Q_zero_gap_filtered:
                        action = card.recommended_action or "unknown"
                        if action not in by_action:
                            by_action[action] = []
                        by_action[action].append(card)

                    print(f"    Actions: {', '.join(f'{k}={len(v)}' for k, v in by_action.items())}")

                    # ========== UNIFIED COVERAGE REFINEMENT ==========
                    # Action types that use unified coverage refinement
                    # (need_new_skill is handled separately below)
                    COVERAGE_ACTIONS = [
                        ("update_description_procedure", "i", "Description/Procedure"),
                        ("update_example", "ii", "Example"),
                        ("update_when_to_use", "iii", "'When to Use'"),
                        ("add_checks_and_constraints", "iv", "CHECK steps"),
                    ]

                    # Helper function for processing a single file
                    def process_single_file(skill_file, cards, action_type, action_label):
                        """Process a single file's coverage refinement. Returns (file, update_count, new_names, sandbox_passed)."""
                        print(f"      {skill_file}: {len(cards)} cases")

                        updated_content, was_updated, new_names = self._coverage_refine_with_retry(
                            file_key=skill_file,
                            gap_cards=cards,
                            diagnosis_type=action_type,
                            epoch=epoch,
                            gen_func=gen_func,
                            eval_func=eval_func
                        )

                        update_count = self._handle_refinement_result(
                            updated_content, was_updated, skill_file, cards, by_action, action_label
                        )

                        # was_updated means sandbox verification passed
                        return skill_file, update_count, new_names, was_updated

                    # Process each action type
                    for action_type, step_num, action_label in COVERAGE_ACTIONS:
                        if action_type not in by_action:
                            continue

                        print(f"\n    [4.A.{step_num}] Updating {action_label}...")

                        # Group cards by file
                        cards_by_file = {}
                        for card in by_action[action_type]:
                            skill_file = card.skill_used.get('specific_file') or 'SKILL.md'
                            if skill_file not in cards_by_file:
                                cards_by_file[skill_file] = []
                            cards_by_file[skill_file].append(card)

                        # All files in this stage are already filtered by current_file_type
                        all_files = [(f, c) for f, c in cards_by_file.items()]

                        # Check if parallel processing is enabled
                        if self.parallel_refine_workers > 0 and len(all_files) > 1:
                            # Parallel processing
                            print(f"      📦 Processing {len(all_files)} files in parallel...")
                            with ThreadPoolExecutor(max_workers=self.parallel_refine_workers) as executor:
                                futures = {}
                                for skill_file, cards in all_files:
                                    future = executor.submit(
                                        process_single_file,
                                        skill_file, cards, action_type, action_label
                                    )
                                    futures[future] = skill_file

                                # Collect results
                                for future in as_completed(futures):
                                    try:
                                        skill_file, update_count, new_names, sandbox_passed = future.result()
                                        stage_updates += update_count
                                        if sandbox_passed:
                                            modified_files.add(skill_file)
                                        if new_names:
                                            self._update_skill_md_for_new_patterns(skill_file, new_names)
                                    except Exception as e:
                                        skill_file = futures[future]
                                        print(f"      ❌ Error processing {skill_file}: {e}")
                        else:
                            # Serial processing
                            for skill_file, cards in all_files:
                                skill_file, update_count, new_names, sandbox_passed = process_single_file(
                                    skill_file, cards, action_type, action_label
                                )
                                stage_updates += update_count
                                if sandbox_passed:
                                    modified_files.add(skill_file)
                                if new_names:
                                    self._update_skill_md_for_new_patterns(skill_file, new_names)

                    # Handle need_new_skill (new_pattern / capability_gap)
                    # Note: new skills are always specific (created in subfield folders)
                    # Only process during "specific" stage
                    if current_file_type == "specific" and "need_new_skill" in by_action:
                        print("\n    [4.A.v] Creating new skills...")
                        by_subfield = {}
                        for card in by_action["need_new_skill"]:
                            subfield = card.signature.get('subfield', 'unknown')
                            if subfield not in by_subfield:
                                by_subfield[subfield] = []
                            by_subfield[subfield].append(card)

                        can_sandbox = (self.sandbox_enabled and gen_func is not None and eval_func is not None)

                        for subfield, cards in by_subfield.items():
                            print(f"      Creating new sub-skill for: {subfield} ({len(cards)} cases)")

                            # Build diagnosis summary from cards
                            diagnosis_parts = []
                            for c in cards[:5]:
                                if c.diagnosis_explanation:
                                    diagnosis_parts.append(c.diagnosis_explanation)
                            diagnosis_summary = "; ".join(diagnosis_parts) if diagnosis_parts else "Capability gap identified"

                            # Format evidence for this subfield
                            evidence_text = self._format_gap_cards_for_new_skill(cards)

                            new_skill_accepted = False
                            for attempt in range(1, self.max_refine_attempts + 1):
                                new_content, was_created = self.textual_optimizer.create_new_subskill(
                                    skill=self.skill_ref,
                                    gap_evidence=evidence_text,
                                    subfield=subfield,
                                    diagnosis_summary=diagnosis_summary,
                                    epoch=epoch
                                )

                                if not was_created or not new_content:
                                    print(f"        ⏭️  Skipped (LLM returned nothing)")
                                    break

                                # Determine file path for the new skill
                                new_file = self._determine_new_skill_path(new_content, subfield)

                                # Sandbox check 1: Does the new skill SOLVE the gap cases?
                                if can_sandbox:
                                    passed, solve_rate, detail, gap_details = self._sandbox_verify_gap_update(
                                        new_file, new_content, cards, gen_func, eval_func
                                    )
                                    if not passed:
                                        print(f"        ❌ Solve sandbox failed (attempt {attempt}/{self.max_refine_attempts}): {detail}")
                                        if attempt >= self.max_refine_attempts:
                                            print(f"        ⏭️  Giving up on new skill for {subfield}")
                                        continue
                                    print(f"        ✅ Solve sandbox passed: {detail}")

                                # Write the new skill file
                                file_path = self.working_skills_dir / new_file
                                file_path.parent.mkdir(parents=True, exist_ok=True)
                                with open(file_path, 'w', encoding="utf-8") as f:
                                    f.write(new_content)
                                print(f"        ✅ Created: {new_file}")

                                # Update SKILL.md with new entry
                                entry_line = self.textual_optimizer.extract_skill_md_entry_from_content(new_content)
                                if entry_line:
                                    entry_parts = [p.strip() for p in entry_line.strip('|').split('|')]
                                    if len(entry_parts) >= 4:
                                        entry_path = entry_parts[0].strip('` ')
                                        entry_subfield = entry_parts[1].strip()
                                        entry_error_type = entry_parts[2].strip()
                                        entry_patterns = [p.strip() for p in entry_parts[3].split(',')]
                                        self.textual_optimizer.update_skill_md_add_entry(
                                            skill=self.skill_ref,
                                            new_file_path=entry_path or new_file,
                                            subfield=entry_subfield or subfield,
                                            error_type=entry_error_type or "Capability gap",
                                            key_patterns=entry_patterns
                                        )
                                    else:
                                        self.textual_optimizer.update_skill_md_add_entry(
                                            skill=self.skill_ref,
                                            new_file_path=new_file,
                                            subfield=subfield,
                                            error_type="Capability gap",
                                            key_patterns=["(new patterns)"]
                                        )
                                else:
                                    self.textual_optimizer.update_skill_md_add_entry(
                                        skill=self.skill_ref,
                                        new_file_path=new_file,
                                        subfield=subfield,
                                        error_type="Capability gap",
                                        key_patterns=["(new patterns)"]
                                    )

                                # Reload router so the new file is discoverable
                                self._reload_router()

                                # Sandbox check 2: Does the router now SELECT this new file?
                                if can_sandbox:
                                    route_correct = 0
                                    test_cards = cards[:self.sandbox_max_cases]
                                    for card in test_cards:
                                        try:
                                            selected = self.router.get_llm_selected_files(
                                                question=card.question,
                                                context=card.context,
                                                subfield=card.signature.get('subfield', '')
                                            )
                                            selected_rel = [str(f.relative_to(self.router.skill_dir)) for f in selected]
                                            if new_file in selected_rel:
                                                route_correct += 1
                                        except Exception:
                                            pass

                                    route_rate = route_correct / len(test_cards) if test_cards else 0
                                    print(f"        Routing: {route_correct}/{len(test_cards)} ({route_rate:.0%})")

                                    if route_rate < self.sandbox_route_threshold:
                                        print(f"        ⚠️  Low routing rate")

                                print(f"        ✅ SKILL.md entry added for: {new_file}")
                                new_skill_accepted = True
                                modified_files.add(new_file)  # Track new file as modified
                                stage_updates += 1
                                break

                            if not new_skill_accepted:
                                print(f"        ⏭️  Skipped new skill for {subfield}")

                    # Reload router after Coverage phase (for this file type)
                    if stage_updates > 0:
                        print(f"\n    Reloading router after Coverage ({current_file_type})...")
                        self._reload_router()

                # ========== Build Q+/Q- for Safety Phase (With Verification) ==========
                # After Coverage updates, verify:
                # 1. Which Q0_gap cases are now fixed → add to Q+
                # 2. Which original Q+ (for modified files) are now broken → move to Q-

                if stage_updates > 0 and modified_files and gen_func and eval_func:
                    print(f"\n    [Post-Coverage Verification] Modified files: {sorted(modified_files)}")

                    # --- Part 1: Verify Q0_gap cases ---
                    fixed_q0_gap = []
                    if Q_zero_gap_filtered:
                        print(f"    Testing {len(Q_zero_gap_filtered)} Q0_gap cases...")
                        fixed_q0_gap, unfixed_q0_gap = self._verify_post_coverage_q0_gap(
                            Q_zero_gap_filtered, gen_func, eval_func
                        )
                        print(f"    Q0_gap results: {len(fixed_q0_gap)} fixed, {len(unfixed_q0_gap)} still unfixed")

                    # --- Part 2: Verify original Q+ for modified files ---
                    # Filter Q+ to only those associated with modified files
                    q_plus_to_verify = []
                    q_plus_retained = []
                    for card in stage_Q_plus_flat:
                        card_files = set()
                        if hasattr(card, 'loaded_files') and card.loaded_files:
                            card_files.update(card.loaded_files)
                        if hasattr(card, 'specific_skill_file') and card.specific_skill_file:
                            card_files.add(card.specific_skill_file)
                        # Check if any of card's files were modified
                        if card_files & modified_files:
                            q_plus_to_verify.append(card)
                        else:
                            q_plus_retained.append(card)

                    broken_q_plus = []
                    if q_plus_to_verify:
                        print(f"    Testing {len(q_plus_to_verify)} Q+ cases (associated with modified files)...")
                        retained, broken = self._verify_post_coverage_q_plus(
                            q_plus_to_verify, gen_func, eval_func
                        )
                        q_plus_retained.extend(retained)
                        broken_q_plus = broken
                        print(f"    Q+ results: {len(retained)} retained, {len(broken)} broken (regression)")

                    # Build final Q+/Q- for Safety phase
                    new_Q_plus = q_plus_retained + fixed_q0_gap
                    new_Q_minus = stage_Q_minus_flat + broken_q_plus
                else:
                    # No Coverage updates or no gen/eval functions
                    new_Q_plus = stage_Q_plus_flat
                    new_Q_minus = stage_Q_minus_flat

                # Simple deduplication by QID (Q+ takes precedence)
                q_plus_qids = set()
                deduped_Q_plus = []
                for card in new_Q_plus:
                    if card.qid not in q_plus_qids:
                        q_plus_qids.add(card.qid)
                        deduped_Q_plus.append(card)
                new_Q_plus = deduped_Q_plus

                # Remove Q+ QIDs from Q-, then dedupe Q-
                deduped_Q_minus = []
                seen_qids = set()
                for card in new_Q_minus:
                    if card.qid not in q_plus_qids and card.qid not in seen_qids:
                        seen_qids.add(card.qid)
                        deduped_Q_minus.append(card)
                new_Q_minus = deduped_Q_minus

                print(f"    Safety input: Q+={len(new_Q_plus)}, Q-={len(new_Q_minus)}")

                # Run unified deep analysis on final composition
                if new_Q_plus or new_Q_minus:
                    new_Q_plus, new_Q_minus = self._run_unified_deep_analysis(new_Q_plus, new_Q_minus)

                # ========== PHASE 4.B: Safety (Q+/Q-) ==========
                # Refine skills with Q+ as constraints and Q- as cases to fix
                if new_Q_minus:
                    safety_updates = self._run_safety_phase(
                        new_Q_plus,
                        new_Q_minus,
                        epoch,
                        gen_func,
                        eval_func,
                        file_type=current_file_type
                    )
                    stage_updates += safety_updates

                # Accumulate stage updates to total
                updates_applied += stage_updates
                print(f"\n    Stage ({current_file_type}) updates: {stage_updates}")

            # End of file_type loop
            print(f"\n  Total updates applied (all stages): {updates_applied}")

            # (4.1) Update SKILL.md routing from Q+_discover evidence
            # Q+_discover means the WRONG file was selected but another file solved it.
            # We aggregate all discover evidence and update SKILL.md keywords once.
            if trigger_evidence:
                print(f"\n[4.1] Updating SKILL.md routing (from Q+_discover, {len(trigger_evidence)} files)...")

                # Aggregate all discover evidence into one text block
                all_discover_text = []
                for solving_file, evidence_text in trigger_evidence.items():
                    all_discover_text.append(
                        f"### Solving file: `{solving_file}`\n{evidence_text}"
                    )
                combined_evidence = "\n\n".join(all_discover_text)

                num_discover = sum(
                    len([c for c in Q_plus_discover if c.solving_skill == f])
                    for f in trigger_evidence
                )

                # Track best attempt for Q+_discover (keep best non-zero result if threshold not met)
                best_skill_md = None
                best_route_rate = 0.0

                # Retry loop for routing update
                routing_accepted = False
                skill_md_path = self.working_skills_dir / "SKILL.md"
                # Backup original
                original_skill_md = skill_md_path.read_text() if skill_md_path.exists() else ""

                for attempt in range(1, self.max_refine_attempts + 1):
                    updated_skill_md, was_updated = self.textual_optimizer.update_skill_md_routing(
                        skill=self.skill_ref,
                        trigger_evidence=combined_evidence,
                        num_cases=num_discover,
                        epoch=epoch
                    )

                    if not was_updated or not updated_skill_md:
                        # If no update generated, check if we have a best result to use
                        if best_skill_md and best_route_rate > 0 and self._validate_skill_md(best_skill_md):
                            print(f"    ⚠️  No new content, using best previous (route_rate={best_route_rate:.0%})")
                            skill_md_path.write_text(best_skill_md)
                            self._reload_router()
                            routing_accepted = True
                            updates_applied += 1
                        else:
                            print(f"    ⏭️  SKILL.md routing update skipped")
                        break

                    # Validate SKILL.md has proper File Index before accepting
                    if not self._validate_skill_md(updated_skill_md):
                        print(f"    ⚠️  Invalid SKILL.md (missing File Index), skipping attempt {attempt}")
                        continue

                    # Temporarily write updated SKILL.md and reload router for sandbox check
                    skill_md_path.write_text(updated_skill_md)
                    self._reload_router()

                    # Sandbox: verify routing
                    if self.sandbox_enabled and Q_plus_discover:
                        passed, route_rate, detail = self._sandbox_verify_routing(Q_plus_discover)

                        # Track best non-zero result (only if valid)
                        if route_rate > best_route_rate and self._validate_skill_md(updated_skill_md):
                            best_route_rate = route_rate
                            best_skill_md = updated_skill_md

                        if passed:
                            print(f"    ✅ Routing sandbox passed (attempt {attempt}): {detail}")
                            routing_accepted = True
                            updates_applied += 1
                            break
                        else:
                            print(f"    ❌ Routing sandbox failed (attempt {attempt}/{self.max_refine_attempts}): {detail}")
                            if attempt >= self.max_refine_attempts:
                                # All attempts failed - use best non-zero result for Q+_discover
                                if best_skill_md and best_route_rate > 0 and self._validate_skill_md(best_skill_md):
                                    print(f"    📊 Using best attempt (route_rate={best_route_rate:.0%}) for Q+_discover")
                                    skill_md_path.write_text(best_skill_md)
                                    self._reload_router()
                                    routing_accepted = True
                                    updates_applied += 1
                                else:
                                    # Revert SKILL.md
                                    skill_md_path.write_text(original_skill_md)
                                    self._reload_router()
                                    print(f"    ⏭️  Reverted SKILL.md after {self.max_refine_attempts} failed attempts (no improvement)")
                            else:
                                # Revert for next attempt
                                skill_md_path.write_text(original_skill_md)
                                self._reload_router()
                    else:
                        # No sandbox, accept as-is
                        print(f"    ✅ SKILL.md routing updated")
                        routing_accepted = True
                        updates_applied += 1
                        break

            print(f"\n  Total updates applied: {updates_applied}")

            # Reload router from working skills if any updates were applied
            if updates_applied > 0:
                print("\n[4.5] Reloading router from working skills...")
                self._reload_router()

            # (5) Run VAL for validation
            print("\n[5] Running validation set...")
            if run_system_fn:
                # Pass split parameter if function accepts it
                sig = inspect.signature(run_system_fn)
                if 'split' in sig.parameters:
                    self.logger.val_log = run_system_fn(val_data, self.router, split="val")
                else:
                    self.logger.val_log = run_system_fn(val_data, self.router)
            else:
                print("  ⚠️  No run_system_fn provided - using placeholder")
                self.logger.val_log = []

            val_metrics = self.compute_metrics(self.logger.val_log)
            print(f"  Val accuracy: {val_metrics.get('accuracy', 0):.2%}")
            print(f"  Val loss: {val_metrics.get('loss', 0):.4f}")

            # (6) Validation gate
            print("\n[6] Checking validation gate...")
            accepted = self.passes_validation_gate(val_metrics, prev_val_metrics)

            # (7) Save checkpoint
            print("\n[7] Saving checkpoint...")
            diff_report = self.generate_diff_report(
                update_set, Q_plus_all, Q_minus_all,
                Q_plus_discover=Q_plus_discover,
                Q_zero_gap=Q_zero_gap
            )

            self.checkpoint_mgr.save_checkpoint(
                epoch=epoch,
                skills_dir=self.working_skills_dir,
                run_log_train=self.logger.train_log,
                run_log_val=self.logger.val_log,
                train_metrics=train_metrics,
                val_metrics=val_metrics,
                diff_report=diff_report,
                accepted=accepted
            )

            # Update history
            self.history["epochs"].append(epoch)
            self.history["train_metrics"].append(train_metrics)
            self.history["val_metrics"].append(val_metrics)

            # (8) Track best checkpoint
            val_acc = val_metrics.get("accuracy", 0)
            if val_acc > self.history["best_val_acc"]:
                self.history["best_val_acc"] = val_acc
                self.history["best_epoch"] = epoch
                print(f"\n🏆 New best checkpoint: Epoch {epoch} (val_acc={val_acc:.2%})")

            # (9) Early stopping
            if self._check_early_stopping(epoch):
                print(f"\n⏹️  Early stopping at epoch {epoch} (no improvement for {self.patience} epochs)")
                break

            prev_val_metrics = val_metrics

        print(f"\n{'='*80}")
        print(f"Training Complete")
        print(f"Best checkpoint: Epoch {self.history['best_epoch']} (val_acc={self.history['best_val_acc']:.2%})")
        print(f"{'='*80}")

        return self.history

    # =========================================================================
    # V2 Methods: Two-Phase Refinement (Coverage → Safety)
    # =========================================================================

    def _run_post_coverage_verification(
        self,
        original_Q_plus: List,
        Q_zero_gap: List,
        gen_func,
        eval_func
    ) -> Tuple[List, List, List]:
        """
        Phase 4.A.1: Post-Coverage Verification.

        Re-evaluates original Q+ and Q0_gap questions with refined skills to determine:
        - retained_Q_plus: Original Q+ that still works
        - broken_Q_plus: Original Q+ broken by Coverage → becomes new Q-
        - coverage_fixed: Q0_gap cases fixed by Coverage → becomes new Q+

        Args:
            original_Q_plus: List of original Q+ evidence cards
            Q_zero_gap: List of Q0_gap unsolved cards
            gen_func: Generation function for sandbox
            eval_func: Evaluation function for sandbox

        Returns:
            (retained_Q_plus, broken_Q_plus, coverage_fixed)
        """
        print("\n  [4.A.1] Post-Coverage Verification...")

        retained_Q_plus = []
        broken_Q_plus = []
        coverage_fixed = []

        # Skip if no gen/eval functions
        if gen_func is None or eval_func is None:
            print("    ⚠️  No gen/eval functions, skipping verification")
            return original_Q_plus, [], []

        # 1. Re-evaluate original Q+ questions
        if original_Q_plus:
            print(f"    Verifying {len(original_Q_plus)} original Q+ cases...")
            # Only verify up to sandbox_max_cases, assume rest are retained
            cards_to_verify = original_Q_plus[:self.sandbox_max_cases]
            cards_not_verified = original_Q_plus[self.sandbox_max_cases:]

            for card in cards_to_verify:
                try:
                    # Get skill content for this question
                    skill_content = self._get_skill_content_for_card(card)

                    # Generate answer with refined skill
                    answer, explanation = gen_func(
                        card.question,
                        card.context,
                        getattr(card, 'options', None),
                        skill_content
                    )

                    # Evaluate
                    score = eval_func(
                        card.question,
                        card.context,
                        answer,
                        explanation,
                        card.ground_truth
                    )

                    if score > 0:
                        retained_Q_plus.append(card)
                    else:
                        # Card is broken by Coverage - update for Safety phase:
                        # - baseline becomes the OLD correct skill answer (what worked)
                        # - skill_k becomes the NEW broken answer (what Coverage broke)
                        old_correct_answer = card.skill_k.copy() if isinstance(card.skill_k, dict) else card.skill_k
                        card.baseline = old_correct_answer
                        card.skill_k = {
                            'answer': answer,
                            'score': score,
                            'explanation': explanation,
                            'execution_success': getattr(card, 'execution_success', None)
                        }
                        # Mark as regression for deep analysis
                        card.is_regress = True
                        card.is_fix = False
                        broken_Q_plus.append(card)
                except Exception as e:
                    # On error, assume retained (conservative)
                    retained_Q_plus.append(card)

            # Cards not verified are assumed retained (conservative)
            retained_Q_plus.extend(cards_not_verified)

            print(f"    Q+ verification: {len(retained_Q_plus)} retained, {len(broken_Q_plus)} broken (verified {len(cards_to_verify)}/{len(original_Q_plus)})")

        # 2. Re-evaluate Q0_gap questions
        if Q_zero_gap:
            print(f"    Verifying {len(Q_zero_gap)} Q0_gap cases...")
            # Only verify up to sandbox_max_cases
            cards_to_verify = Q_zero_gap[:self.sandbox_max_cases]

            for card in cards_to_verify:
                try:
                    # Get skill content for this question
                    skill_content = self._get_skill_content_for_card_unsolved(card)

                    # Generate answer with refined skill
                    answer, explanation = gen_func(
                        card.question,
                        card.context,
                        getattr(card, 'options', None),
                        skill_content
                    )

                    # Evaluate
                    score = eval_func(
                        card.question,
                        card.context,
                        answer,
                        explanation,
                        card.ground_truth
                    )

                    if score > 0:
                        # Card is fixed by Coverage - update for Safety phase:
                        # - baseline stays as OLD wrong answer (what didn't work)
                        # - skill_k becomes the NEW correct answer (what Coverage fixed)
                        # Note: UnsolvedCard.baseline is already the no-skill wrong answer
                        # Update skill_used to reflect the new correct answer
                        card.skill_used = card.skill_used or {}
                        card.skill_used['answer'] = answer
                        card.skill_used['score'] = score
                        card.skill_used['explanation'] = explanation
                        # Mark as fix for deep analysis
                        card.is_fix = True
                        card.is_regress = False
                        coverage_fixed.append(card)
                except Exception:
                    pass  # Not fixed

            print(f"    Q0_gap verification: {len(coverage_fixed)} fixed by Coverage (verified {len(cards_to_verify)}/{len(Q_zero_gap)})")

        return retained_Q_plus, broken_Q_plus, coverage_fixed

    def _get_skill_content_for_card(self, card) -> str:
        """Get combined skill content for an evidence card."""
        content_parts = []

        # Get files from card
        files = getattr(card, 'loaded_files', None) or []
        if not files and hasattr(card, 'specific_skill_file') and card.specific_skill_file:
            files = [card.specific_skill_file]

        for file_key in files:
            file_path = self.working_skills_dir / file_key
            if file_path.exists():
                content_parts.append(file_path.read_text())

        return "\n\n---\n\n".join(content_parts) if content_parts else ""

    def _get_skill_content_for_card_unsolved(self, card) -> str:
        """Get combined skill content for an unsolved card."""
        content_parts = []

        # Get files from card.skill_used
        skill_used = getattr(card, 'skill_used', {}) or {}
        files = skill_used.get('all_files', [])
        if not files:
            specific = skill_used.get('specific_file')
            if specific:
                files = [specific]

        for file_key in files:
            file_path = self.working_skills_dir / file_key
            if file_path.exists():
                content_parts.append(file_path.read_text())

        return "\n\n---\n\n".join(content_parts) if content_parts else ""

    def _run_unified_deep_analysis(
        self,
        new_Q_plus: List,
        new_Q_minus: List
    ) -> Tuple[List, List]:
        """
        Phase 4.A.2: Unified Deep Analysis.

        Generate detailed what_went_right/wrong analysis for final Q+/Q- composition.
        This runs AFTER Coverage phase when Q+ composition is final.

        Note: Attribution is NOT performed here because:
        - Original Q+/Q- cards already have attribution_result from earlier in training loop
        - Q0_gap cards (UnsolvedCard) have root_cause_file from diagnosis which serves as attribution

        This method only generates what_went_right_or_wrong deep analysis.

        Args:
            new_Q_plus: Final Q+ cards (retained_Q_plus + coverage_fixed)
            new_Q_minus: Final Q- cards (original_Q_minus + broken_Q_plus)

        Returns:
            (analyzed_Q_plus, analyzed_Q_minus) with what_went_right_or_wrong populated
        """
        print("\n  [4.A.2] Running Unified Deep Analysis...")

        # Use existing deep analysis infrastructure
        if not self.enable_deep_analysis:
            print("    Deep analysis disabled, using simple labels")
            return new_Q_plus, new_Q_minus

        all_cards = new_Q_plus + new_Q_minus
        if not all_cards:
            return new_Q_plus, new_Q_minus

        print(f"    Analyzing {len(new_Q_plus)} Q+ and {len(new_Q_minus)} Q- cards...")

        # For UnsolvedCard (coverage_fixed), map root_cause_file to attribution_result
        # so it's in the same format as EvidenceCard for downstream use
        for card in all_cards:
            if not card.attribution_result:
                # Try root_cause_file first (from diagnosis)
                if hasattr(card, 'root_cause_file') and card.root_cause_file:
                    card.attribution_result = {
                        'attributed_files': [card.root_cause_file],
                        'analysis': f'Diagnosed root cause file: {card.root_cause_file}'
                    }
                # Fallback to specific_skill_file
                elif hasattr(card, 'specific_skill_file') and card.specific_skill_file:
                    card.attribution_result = {
                        'attributed_files': [card.specific_skill_file],
                        'analysis': f'Default skill file: {card.specific_skill_file}'
                    }

        # Generate what_went_right_or_wrong deep analysis
        # Use textual_optimizer's deep analysis method
        self.textual_optimizer._generate_deep_analysis_batch(all_cards)

        return new_Q_plus, new_Q_minus

    def _run_safety_phase(
        self,
        new_Q_plus: List,
        new_Q_minus: List,
        epoch: int,
        gen_func,
        eval_func,
        file_type: str = None  # "common", "specific", or None for all
    ) -> int:
        """
        Phase 4.B: Safety Refinement.

        Refine skills using Q+ as constraints and Q- as cases to fix.
        Uses SAFETY_REFINEMENT_PROMPT with contrastive Q+ constraints.
        Supports parallel processing when parallel_refine_workers > 0.

        Args:
            new_Q_plus: Final Q+ cards with deep analysis (constraints)
            new_Q_minus: Final Q- cards with diagnosis (to fix)
            epoch: Current epoch
            gen_func: Generation function for sandbox
            eval_func: Evaluation function for sandbox
            file_type: "common" to process only common files, "specific" for subfield files,
                      None to process all files

        Returns:
            Number of updates applied
        """
        file_type_label = f" ({file_type} files)" if file_type else ""
        print(f"\n  [4.B] Safety Phase{file_type_label} (Q+ constraints + Q- fixes)...")

        updates_applied = 0

        if not new_Q_minus:
            print("    No Q- cases to fix, skipping Safety phase")
            return 0

        # Group Q- by file (using attribution)
        Q_minus_by_file = self._group_cards_by_file(new_Q_minus)
        Q_plus_by_file = self._group_cards_by_file(new_Q_plus)

        # Debug: Check deep analysis status (must have _deep_analysis_generated=True, not just lazy label)
        q_plus_with_deep = sum(1 for c in new_Q_plus if getattr(c, '_deep_analysis_generated', False))
        q_minus_with_deep = sum(1 for c in new_Q_minus if getattr(c, '_deep_analysis_generated', False))
        print(f"    Deep analysis status: Q+ {q_plus_with_deep}/{len(new_Q_plus)} done, Q- {q_minus_with_deep}/{len(new_Q_minus)} done")

        # Separate common and subfield files
        all_files = set(Q_minus_by_file.keys())
        common_files = [f for f in all_files if self._is_common_file(f)]
        subfield_files = [f for f in all_files if f not in common_files]

        # Filter by file_type if specified
        if file_type == "common":
            files_to_include = common_files
        elif file_type == "specific":
            files_to_include = subfield_files
        else:
            files_to_include = common_files + subfield_files

        # Debug: Print file-level summary before processing
        print(f"    Files to process ({len(files_to_include)}):")
        for f in files_to_include:
            q_plus_count = len(Q_plus_by_file.get(f, []))
            q_minus_count = len(Q_minus_by_file.get(f, []))
            print(f"      - {f}: Q+={q_plus_count}, Q-={q_minus_count}")

        # Helper function for processing a single file (used by both serial and parallel modes)
        def process_single_safety_file(file_key, Q_plus_raw, Q_minus_raw, is_common):
            """Process a single file's safety refinement. Returns (file_key, was_updated, updated_content)."""
            if not Q_minus_raw:
                return file_key, False, None

            # V2: Sample P/N per file (moved from [2.5] to here)
            Q_plus = self.evidence_collector._sample_diverse(Q_plus_raw, self.default_P)
            Q_minus = self.evidence_collector._sample_prioritized(Q_minus_raw, self.default_N)

            print(f"\n    Safety refinement: {file_key}")
            print(f"      Constraints (Q+): {len(Q_plus)}/{len(Q_plus_raw)}, To fix (Q-): {len(Q_minus)}/{len(Q_minus_raw)}")

            # Call safety refinement with retry
            updated_content, was_updated, iteration_summary = self._safety_refine_with_retry(
                file_key=file_key,
                Q_plus=Q_plus,
                Q_minus=Q_minus,
                epoch=epoch,
                gen_func=gen_func,
                eval_func=eval_func,
                is_common_file=is_common
            )

            return file_key, was_updated, updated_content

        # Build list of files to process
        files_to_process = []
        for file_key in files_to_include:
            Q_plus_raw = Q_plus_by_file.get(file_key, [])
            Q_minus_raw = Q_minus_by_file.get(file_key, [])
            if Q_minus_raw:  # Only process files with Q- cases
                is_common = self._is_common_file(file_key)
                files_to_process.append((file_key, Q_plus_raw, Q_minus_raw, is_common))

        if not files_to_process:
            print("    No files with Q- cases to process")
            return 0

        # Check if parallel processing is enabled
        if self.parallel_refine_workers > 0 and len(files_to_process) > 1:
            # Parallel processing
            print(f"    📦 Processing {len(files_to_process)} files in parallel (max_workers={self.parallel_refine_workers})...")
            results = []

            with ThreadPoolExecutor(max_workers=self.parallel_refine_workers) as executor:
                futures = {}
                for file_key, Q_plus_raw, Q_minus_raw, is_common in files_to_process:
                    future = executor.submit(
                        process_single_safety_file,
                        file_key, Q_plus_raw, Q_minus_raw, is_common
                    )
                    futures[future] = file_key

                # Collect results
                for future in as_completed(futures):
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        file_key = futures[future]
                        print(f"    ❌ Error processing {file_key}: {e}")

            # Apply updates (serial to avoid file conflicts)
            for file_key, was_updated, updated_content in results:
                if was_updated and updated_content:
                    # Save updated skill
                    skill_file = self.working_skills_dir / file_key
                    skill_file.parent.mkdir(parents=True, exist_ok=True)
                    with open(skill_file, 'w', encoding="utf-8") as f:
                        f.write(updated_content)

                    # Sync SKILL.md File Index (thread-safe)
                    if file_key and file_key != "SKILL.md":
                        self._sync_skill_md_file_index(file_key, updated_content)

                    print(f"      ✅ Safety update applied: {file_key}")
                    updates_applied += 1
                else:
                    print(f"      ⏭️  Safety update skipped: {file_key}")
        else:
            # Serial processing
            for file_key, Q_plus_raw, Q_minus_raw, is_common in files_to_process:
                file_key, was_updated, updated_content = process_single_safety_file(
                    file_key, Q_plus_raw, Q_minus_raw, is_common
                )

                if was_updated and updated_content:
                    # Save updated skill
                    skill_file = self.working_skills_dir / file_key
                    skill_file.parent.mkdir(parents=True, exist_ok=True)
                    with open(skill_file, 'w', encoding="utf-8") as f:
                        f.write(updated_content)

                    # Sync SKILL.md File Index
                    if file_key and file_key != "SKILL.md":
                        self._sync_skill_md_file_index(file_key, updated_content)

                    print(f"      ✅ Safety update applied: {file_key}")
                    updates_applied += 1
                else:
                    print(f"      ⏭️  Safety update skipped: {file_key}")

        return updates_applied

    def _group_cards_by_file(self, cards: List) -> Dict[str, List]:
        """Group evidence cards by attributed file."""
        by_file = {}
        for card in cards:
            # Get attributed file(s)
            attr_result = getattr(card, 'attribution_result', None)
            if attr_result and 'attributed_files' in attr_result:
                files = attr_result['attributed_files']
            elif hasattr(card, 'specific_skill_file') and card.specific_skill_file:
                files = [card.specific_skill_file]
            elif hasattr(card, 'skill_used'):
                skill_used = card.skill_used or {}
                files = [skill_used.get('specific_file', 'SKILL.md')]
            else:
                files = ['SKILL.md']

            for f in files:
                if f not in by_file:
                    by_file[f] = []
                by_file[f].append(card)

        return by_file

    def _safety_refine_with_retry(
        self,
        file_key: str,
        Q_plus: List,
        Q_minus: List,
        epoch: int,
        gen_func=None,
        eval_func=None,
        is_common_file: bool = False
    ) -> Tuple[Optional[str], bool, Dict]:
        """
        Safety refinement with retry logic.

        Uses SAFETY_REFINEMENT_PROMPT with Q+ as constraints.
        """
        can_sandbox = (self.sandbox_enabled and gen_func is not None and eval_func is not None)

        best_content = None
        best_score = 0.0
        best_summary = {}

        for attempt in range(1, self.max_refine_attempts + 1):
            # Call textual optimizer with safety mode
            updated_content, was_updated = self.textual_optimizer.refine_skill_safety(
                skill=self.skill_ref,
                Q_plus=Q_plus,
                Q_minus=Q_minus,
                specific_skill_file=file_key,
                epoch=epoch
            )

            if not was_updated or not updated_content:
                if best_content and best_score > 0:
                    print(f"      ⚠️  No new content, using best previous (score={best_score:.0%})")
                    return best_content, True, best_summary
                return None, False, {}

            if can_sandbox:
                # Verify: Q+ retention is critical
                passed, metrics, detail = self._sandbox_verify_full(
                    file_key,
                    updated_content,
                    gen_func,
                    eval_func,
                    use_combined_content=is_common_file,
                    q_plus_cards=Q_plus,
                    q_minus_cards=Q_minus
                )

                score = metrics.get('combined_score', 0)
                q_plus_rate = metrics.get('q_plus_rate', 0)

                # Track best attempt
                if score > best_score:
                    best_score = score
                    best_content = updated_content
                    best_summary = {'q_plus_rate': q_plus_rate, 'metrics': metrics}

                # Save iteration log
                self.iteration_logger.save_iteration_log(
                    file_key=f"{file_key}_safety",
                    epoch=epoch,
                    attempt=attempt,
                    content=updated_content,
                    metrics=metrics,
                    passed=passed
                )

                if passed:
                    print(f"      ✅ Safety sandbox passed (attempt {attempt}): {detail}")
                    return updated_content, True, {'metrics': metrics}
                else:
                    print(f"      ❌ Safety sandbox failed (attempt {attempt}/{self.max_refine_attempts}): {detail}")
                    if attempt >= self.max_refine_attempts:
                        # Use best attempt if Q+ rate is acceptable
                        if best_content and best_score > 0:
                            print(f"      📊 Using best safety attempt (score={best_score:.0%})")
                            return best_content, True, best_summary
                        return None, False, {}
            else:
                return updated_content, True, {}

        return None, False, {}

    def _check_early_stopping(self, current_epoch: int) -> bool:
        """Check if early stopping criteria is met."""
        if self.history["best_epoch"] is None:
            return False

        epochs_since_best = current_epoch - self.history["best_epoch"]
        return epochs_since_best >= self.patience


# Example usage
if __name__ == "__main__":
    # Initialize trainer (reads from config or .env if not provided)
    trainer = SkillTrainer(
        skills_dir=cfg('skills.dir') or os.getenv('SKILLS_DIR', '.claude/skills/famma-non-arithmetic-v1'),
        lambda_regress=2.0,
        M=5,
        patience=3
    )

    # Placeholder datasets (in production, load from CSV/parquet)
    train_data = []
    val_data = []

    # Run training loop (with placeholder run_system_fn)
    history = trainer.train(
        train_data=train_data,
        val_data=val_data,
        max_epochs=5,
        run_system_fn=None  # TODO: Implement actual system runner
    )

    print("\nTraining history:")
    print(json.dumps(history, indent=2, default=str))
    