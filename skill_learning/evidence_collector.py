"""
Evidence Collector - Collect Q+/Q- for skill refinement

Collects contrastive evidence for each skill:
- Q+(k): Positive cases where skill fixes baseline failures
- Q-(k): Negative cases where skill causes regressions
- Q-_cf(k): Counterfactual cases where competitors outperform

Evidence is used for skill refinement in the training loop.

Skill Loading Methods:
- progressive: Claude tool_use for on-demand skill file loading (default, Claude only)
- router: LLM-based pre-selection (any model, auto-fallback for non-Claude)

Environment Variables:
    SKILL_METHOD    "progressive" (default) or "router"
    GEN_MODEL       Generation model (auto-fallback to router if not Claude)
"""

import os
import json
import numpy as np
from typing import Dict, List, Tuple, Optional
from pathlib import Path
from dataclasses import dataclass, asdict, field
from sklearn.cluster import KMeans
from collections import defaultdict
from dotenv import load_dotenv

# Import skill loading utilities
from skills_router import (
    SkillsRouter,
    discover_skill_files,
    build_skill_files_tool,
    load_skill_file_content,
    load_skill_md,
    determine_skill_method,
    PROGRESSIVE_PROMPT_TEMPLATE
)
try:
    from skill_learning.config import cfg, is_config_loaded
except ImportError:
    from config import cfg, is_config_loaded

# Load environment
load_dotenv()

# Skill loading configuration (lazy initialization to avoid issues when imported before config is loaded)
# IMPORTANT: Only cache values AFTER config is loaded, otherwise fallback values get stuck
_gen_model = None
_skill_method = None
_skills_dir = None

def reset_config_cache():
    """Reset cached config values. Call this after config is (re)loaded."""
    global _gen_model, _skill_method, _skills_dir
    _gen_model = None
    _skill_method = None
    _skills_dir = None

def get_gen_model():
    """Get generation model (lazy initialization).

    Only caches value after config is loaded to avoid caching fallback 'qwen-flash'.
    """
    global _gen_model
    # Note: is_config_loaded already imported at module level from config

    # If config is loaded, read from config and cache
    if is_config_loaded():
        if _gen_model is None:
            # Use explicit None check to avoid 'or' fallback when config value exists
            config_val = cfg('models.gen', debug=True)
            if config_val is not None:
                _gen_model = config_val
                print(f"  [EvidenceCollector] Using gen model from config: {_gen_model}")
            else:
                _gen_model = os.getenv('GEN_MODEL', 'qwen-flash')
                print(f"  [EvidenceCollector] ⚠️  Using gen model from env/fallback: {_gen_model}")
        return _gen_model
    else:
        # Config not loaded yet - return env var without caching
        fallback = os.getenv('GEN_MODEL', 'qwen-flash')
        print(f"  [EvidenceCollector] ⚠️  Config not loaded, using fallback gen model: {fallback}")
        return fallback

def get_skill_method():
    """Get skill loading method (lazy initialization).

    Only caches value after config is loaded.
    """
    global _skill_method
    # Note: is_config_loaded already imported at module level

    if is_config_loaded():
        if _skill_method is None:
            # Use explicit None check to avoid 'or' fallback when config value exists
            config_method = cfg('skills.method', debug=True)
            if config_method is not None:
                requested_method = config_method
                print(f"  [EvidenceCollector] Using skill method from config: {requested_method}")
            else:
                requested_method = os.getenv('SKILL_METHOD', 'router')
                print(f"  [EvidenceCollector] ⚠️  Using skill method from env/fallback: {requested_method}")
            _skill_method = determine_skill_method(
                get_gen_model(),
                requested_method
            )
        return _skill_method
    else:
        # Config not loaded yet - compute without caching
        fallback = os.getenv('SKILL_METHOD', 'router')
        print(f"  [EvidenceCollector] ⚠️  Config not loaded, using fallback skill method: {fallback}")
        return determine_skill_method(
            get_gen_model(),
            fallback
        )

def get_skills_dir():
    """Get skills directory (lazy initialization).

    Only caches value after config is loaded.
    """
    global _skills_dir
    # Note: is_config_loaded already imported at module level

    if is_config_loaded():
        if _skills_dir is None:
            _skills_dir = cfg('skills.dir') or os.getenv('SKILLS_DIR', '.claude/skills/famma-non-arithmetic-v1')
        return _skills_dir
    else:
        # Config not loaded yet - return env var without caching
        return os.getenv('SKILLS_DIR', '.claude/skills/famma-non-arithmetic-v1')


@dataclass
class EvidenceCard:
    """Comprehensive evidence card for skill refinement."""
    qid: str
    signature: Dict
    question: str
    context: str  # Full context (not truncated)
    ground_truth: str  # Ground truth answer
    baseline: Dict  # {answer, score, explanation}
    skill_k: Dict  # {answer, score, explanation}
    delta: float
    what_went_right_or_wrong: str  # Simple analysis (or placeholder for lazy analysis)
    specific_skill_file: Optional[str] = None  # Which sub-skill file was used
    options: Optional[str] = None  # MC options text (e.g., "A. ... B. ... C. ...")
    skill_method: Optional[str] = None  # "progressive" or "router"
    loaded_files: Optional[List[str]] = None  # Unique files loaded (deduplicated)
    tool_call_sequence: Optional[List[Dict]] = None  # Full sequence with reasons for refinement
    # For lazy deep analysis (populated on-demand)
    _deep_analysis_generated: bool = False  # Whether deep analysis has been run
    is_fix: bool = False  # For lazy analysis context
    is_regress: bool = False  # For lazy analysis context
    # PoT mode: Generated code for analysis
    baseline_code: Optional[str] = None  # Code generated in baseline run (PoT mode)
    skill_code: Optional[str] = None  # Code generated in skill run (PoT mode)
    # Attribution result (populated when deep analysis is enabled)
    attribution_result: Optional[Dict] = None  # {"attributed_files": [...], "analysis": "..."}


class EvidenceCollector:
    """Collects and manages Q+/Q- evidence for skill refinement."""

    def __init__(
        self,
        p_min: int = None,  # Minimum positives for full refine
        r_min: int = None,  # Minimum negatives for safety refine
        default_P: int = None,  # Default number of positives to sample
        default_N: int = None,  # Default number of negatives to sample
        max_context_length: int = None
    ):
        """
        Initialize evidence collector.

        Args:
            p_min: Minimum number of positives for full refinement
            r_min: Minimum number of negatives for safety refinement
            default_P: Default number of positives to sample
            default_N: Default number of negatives to sample
            max_context_length: Maximum context length for evidence cards

        Note:
            Deep analysis is now generated lazily in TextualOptimizer._format_evidence()
            and controlled by ENABLE_DEEP_ANALYSIS env var.
        """
        # Apply defaults from config or environment variables
        self.p_min = p_min if p_min is not None else (cfg('evidence.p_min') or int(os.getenv('P_MIN', '5')))
        self.r_min = r_min if r_min is not None else (cfg('evidence.r_min') or int(os.getenv('R_MIN', '2')))
        self.default_P = default_P if default_P is not None else (cfg('evidence.evidence_p') or int(os.getenv('EVIDENCE_P', '8')))
        self.default_N = default_N if default_N is not None else (cfg('evidence.evidence_n') or int(os.getenv('EVIDENCE_N', '8')))
        self.max_context_length = max_context_length if max_context_length is not None else (cfg('evidence.max_context_length') or int(os.getenv('EVIDENCE_MAX_CONTEXT_LENGTH', '800')))

    def collect_evidence(
        self,
        run_log_entries: List,  # List of RunLogEntry from run_logger
        skill_id: str
    ) -> Tuple[List[EvidenceCard], List[EvidenceCard]]:
        """
        Collect Q+ and Q- evidence for a specific skill.

        Returns ALL raw Q+/Q- cards without grouping or sampling.
        Each card has loaded_files populated for attribution stage.

        Attribution (in skill_trainer.py) determines file responsibility AFTER this.
        Grouping and sampling by attributed files happens AFTER attribution.

        Args:
            run_log_entries: List of RunLogEntry objects
            skill_id: Skill ID to collect evidence for

        Returns:
            Tuple of (Q_plus, Q_minus) evidence cards (raw, ungrouped)
        """
        # Separate positive and negative cases
        Q_plus_raw = []
        Q_minus_raw = []

        for entry in run_log_entries:
            if entry.chosen_skill != skill_id:
                continue

            # Positive: is_fix=1 or delta>0
            if entry.is_fix or entry.delta > 0:
                Q_plus_raw.append(entry)

            # Negative: is_regress=1 (prioritized) or delta<0
            if entry.is_regress or entry.delta < 0:
                Q_minus_raw.append(entry)

        print(f"\nSkill: {skill_id}")
        print(f"  Raw positives: {len(Q_plus_raw)}")
        print(f"  Raw negatives: {len(Q_minus_raw)}")

        # Check eligibility
        if len(Q_plus_raw) < self.p_min and len(Q_minus_raw) < self.r_min:
            print(f"  ⚠️  Insufficient evidence (need {self.p_min} pos or {self.r_min} neg)")
            return [], []

        # Convert all entries to evidence cards with loaded_files populated
        # specific_skill_file will be set by attribution stage later
        Q_plus_cards = [self._to_evidence_card(entry, skill_id, file_key=None) for entry in Q_plus_raw]
        Q_minus_cards = [self._to_evidence_card(entry, skill_id, file_key=None) for entry in Q_minus_raw]

        print(f"  Total raw positives: {len(Q_plus_cards)}")
        print(f"  Total raw negatives: {len(Q_minus_cards)}")

        return Q_plus_cards, Q_minus_cards

    def _group_by_specific_file(self, entries: List) -> Dict[str, List]:
        """
        Group entries by skill files used (deduplicated).

        Each entry is attributed to ALL UNIQUE files it used (via loaded_files
        or all_skill_files), not just the first. This ensures evidence is
        distributed fairly across all files that contributed to the answer.

        For progressive loading, loaded_files may contain duplicates (same file
        requested multiple times). We deduplicate here for grouping, but
        preserve tool_call_sequence in the entry for refinement analysis.

        Args:
            entries: List of RunLogEntry

        Returns:
            Dict mapping specific_skill_file -> list of entries
        """
        grouped = defaultdict(list)

        for entry in entries:
            # Get loaded files from metadata (progressive loading)
            # or all_skill_files (router method)
            files = None

            # Try to get from skill_metadata (progressive loading results)
            skill_metadata = getattr(entry, 'skill_metadata', None)
            if skill_metadata and isinstance(skill_metadata, dict):
                files = skill_metadata.get('loaded_files', None)

            # Fallback to all_skill_files attribute
            if not files:
                files = getattr(entry, 'all_skill_files', None)

            if files:
                # Deduplicate while preserving order
                unique_files = self._deduplicate_files(files)
                for file_key in unique_files:
                    # Skip SKILL.md - it's always loaded, not a specific skill file
                    if file_key == 'SKILL.md':
                        continue
                    grouped[file_key].append(entry)
            else:
                # Fallback to specific_skill_file
                file_key = getattr(entry, 'specific_skill_file', None) or "SKILL.md"
                if file_key != 'SKILL.md':
                    grouped[file_key].append(entry)

        return dict(grouped)

    def _deduplicate_files(self, files: List[str]) -> List[str]:
        """Deduplicate file list while preserving order."""
        seen = set()
        result = []
        for f in files:
            if f not in seen:
                seen.add(f)
                result.append(f)
        return result

    def _sample_diverse(self, entries: List, k: int) -> List:
        """
        Sample k diverse entries using clustering.

        Strategy:
        1. Cluster entries by subfield:error_type signature
        2. Take one from each cluster (ensures diversity)
        3. If clusters < k, fill remaining slots round-robin from unused entries
        4. If clusters > k, random-sample k clusters

        Args:
            entries: List of RunLogEntry
            k: Number to sample

        Returns:
            List of sampled entries
        """
        if len(entries) <= k:
            return entries

        # Cluster by subfield + error_type
        signatures = []
        for entry in entries:
            sig = entry.signature
            subfield = sig.get('subfield', 'unknown')
            error_type = sig.get('error_type', 0)
            signatures.append(f"{subfield}:{error_type}")

        # Group by signature
        groups = defaultdict(list)
        for entry, sig in zip(entries, signatures):
            groups[sig].append(entry)

        # Phase 1: Take one from each group (ensures diversity)
        sampled = []
        remaining_by_group = {}  # leftover entries per group
        for group_key, group_entries in groups.items():
            sampled.append(group_entries[0])
            if len(group_entries) > 1:
                remaining_by_group[group_key] = group_entries[1:]

        # Phase 2: If too many groups, trim to k
        if len(sampled) > k:
            indices = np.random.choice(len(sampled), k, replace=False)
            sampled = [sampled[i] for i in indices]
            return sampled

        # Phase 3: If fewer groups than k, fill remaining slots round-robin
        remaining_slots = k - len(sampled)
        sampled_qids = {e.qid for e in sampled}

        if remaining_slots > 0 and remaining_by_group:
            # Round-robin across groups to maintain diversity
            group_iters = {gk: iter(entries) for gk, entries in remaining_by_group.items()}
            filled = 0
            while filled < remaining_slots:
                added_this_round = False
                for gk in list(group_iters.keys()):
                    if filled >= remaining_slots:
                        break
                    try:
                        candidate = next(group_iters[gk])
                        if candidate.qid not in sampled_qids:
                            sampled.append(candidate)
                            sampled_qids.add(candidate.qid)
                            filled += 1
                            added_this_round = True
                    except StopIteration:
                        del group_iters[gk]
                if not added_this_round:
                    break  # No more entries available

        return sampled

    def _sample_prioritized(self, entries: List, k: int) -> List:
        """
        Sample k entries with priority: is_regress=1 → delta<0.

        Args:
            entries: List of RunLogEntry
            k: Number to sample

        Returns:
            List of sampled entries
        """
        if len(entries) <= k:
            return entries

        # Prioritize regressions
        regressions = [e for e in entries if e.is_regress]
        other_negatives = [e for e in entries if not e.is_regress]

        sampled = []

        # Take regressions first
        if regressions:
            n_regress = min(len(regressions), k)
            sampled.extend(regressions[:n_regress])

        # Fill remaining with other negatives
        remaining = k - len(sampled)
        if remaining > 0 and other_negatives:
            sampled.extend(other_negatives[:remaining])

        return sampled

    def _get_simple_analysis(self, entry) -> str:
        """
        Get simple analysis without LLM call.
        Used during evidence collection (lazy analysis).
        """
        if entry.is_fix:
            return "✅ Fixed baseline failure - skill corrected the answer"
        elif entry.is_regress:
            return "❌ Regression - skill broke a correct baseline answer"
        elif entry.delta > 0:
            return f"✅ Improvement (delta={entry.delta})"
        elif entry.delta < 0:
            return f"❌ Degradation (delta={entry.delta})"
        else:
            return "No change"

    def _to_evidence_card(self, entry, skill_id: str, file_key: str = None) -> EvidenceCard:
        """
        Convert RunLogEntry to compact EvidenceCard.

        Args:
            entry: RunLogEntry
            skill_id: Skill ID
            file_key: The specific file this card is attributed to (from grouping).
                      Overrides entry.specific_skill_file when an entry is shared
                      across multiple file groups.

        Returns:
            EvidenceCard
        """
        # Use simple analysis during collection (lazy deep analysis done later if needed)
        analysis = self._get_simple_analysis(entry)

        # Extract skill loading metadata
        skill_metadata = getattr(entry, 'skill_metadata', None) or {}
        # Try skill_metadata first (progressive mode), then all_skill_files (router mode)
        loaded_files = (
            skill_metadata.get('loaded_files', None) or
            getattr(entry, 'loaded_files', None) or
            getattr(entry, 'all_skill_files', None)  # Router mode stores files here
        )
        tool_call_sequence = skill_metadata.get('tool_call_sequence', None)

        # Deduplicate loaded_files for the card (preserves tool_call_sequence for refinement)
        if loaded_files:
            loaded_files = self._deduplicate_files(loaded_files)

        # Extract PoT code and execution status if available
        baseline_code = getattr(entry, 'baseline_code', None)
        skill_code = getattr(entry, 'skill_code', None)
        skill_execution_success = getattr(entry, 'skill_execution_success', None)

        return EvidenceCard(
            qid=entry.qid,
            signature=entry.signature,
            question=entry.question,  # Full question
            context=entry.context,  # Full context (not truncated)
            ground_truth=entry.ground_truth,
            baseline={
                "answer": entry.baseline_answer,
                "score": entry.baseline_score,
                "explanation": entry.baseline_explanation or ""
            },
            skill_k={
                "answer": entry.skill_answer,
                "score": entry.skill_score,
                "explanation": entry.skill_explanation or "",
                "execution_success": skill_execution_success  # PoT mode: whether code executed successfully
            },
            delta=entry.delta,
            what_went_right_or_wrong=analysis,
            specific_skill_file=file_key or entry.specific_skill_file,
            options=getattr(entry, 'options', None),
            skill_method=skill_metadata.get('method', None) or getattr(entry, 'skill_method', get_skill_method()),
            loaded_files=loaded_files,
            tool_call_sequence=tool_call_sequence,  # Full sequence with reasons for refinement
            is_fix=entry.is_fix,
            is_regress=entry.is_regress,
            baseline_code=baseline_code,  # PoT mode: code from baseline run
            skill_code=skill_code  # PoT mode: code from skill run
        )

    def collect_counterfactual_evidence(
        self,
        run_log_entries: List,
        skill_id: str,
        competitor_results: Dict[str, List]  # skill_id -> list of RunLogEntry
    ) -> List[EvidenceCard]:
        """
        Collect counterfactual evidence Q-_cf(k).

        Cases where skill k underperforms competitors.

        Args:
            run_log_entries: List of RunLogEntry for skill_id
            skill_id: Target skill ID
            competitor_results: Dict mapping competitor skill IDs to their RunLogEntry lists

        Returns:
            List of counterfactual evidence cards
        """
        Q_minus_cf = []

        # For each query where skill_id was used
        for entry in run_log_entries:
            if entry.chosen_skill != skill_id:
                continue

            qid = entry.qid

            # Check if any competitor did better
            for comp_skill_id, comp_entries in competitor_results.items():
                if comp_skill_id == skill_id:
                    continue

                # Find competitor's result for this query
                comp_entry = None
                for comp_e in comp_entries:
                    if comp_e.qid == qid:
                        comp_entry = comp_e
                        break

                if comp_entry is None:
                    continue

                # Check if competitor outperformed by a margin
                margin = 0.5  # Threshold for significant difference
                if comp_entry.skill_score and entry.skill_score:
                    if comp_entry.skill_score - entry.skill_score >= margin:
                        # Competitor did better - this is counterfactual evidence
                        card = self._to_evidence_card(entry, skill_id)
                        card.what_went_right_or_wrong += f" (Competitor {comp_skill_id} scored {comp_entry.skill_score} vs {entry.skill_score})"
                        Q_minus_cf.append(card)
                        break  # Only count once per query

        print(f"  Counterfactual negatives: {len(Q_minus_cf)}")
        return Q_minus_cf

    def save_evidence(
        self,
        skill_id: str,
        Q_plus: List[EvidenceCard],
        Q_minus: List[EvidenceCard],
        output_dir: str = "skill_learning/evidence",
        epoch: int = 0
    ):
        """
        Save evidence to disk.

        Args:
            skill_id: Skill ID
            Q_plus: Positive evidence
            Q_minus: Negative evidence
            output_dir: Output directory
            epoch: Epoch number
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Save as JSON
        evidence = {
            "skill_id": skill_id,
            "epoch": epoch,
            "Q_plus": [asdict(card) for card in Q_plus],
            "Q_minus": [asdict(card) for card in Q_minus],
            "counts": {
                "positives": len(Q_plus),
                "negatives": len(Q_minus)
            }
        }

        output_file = output_path / f"{skill_id}_epoch{epoch}.json"
        with open(output_file, 'w', encoding="utf-8") as f:
            json.dump(evidence, f, indent=2)

        print(f"✓ Saved evidence: {output_file}")


# Example usage
if __name__ == "__main__":
    from run_logger import RunLogger, RunLogEntry

    # Create sample run log
    logger = RunLogger()

    # Add some sample entries
    logger.log_run(
        qid="q1",
        question="Portfolio question 1",
        context="Context 1",
        ground_truth="A",
        baseline_answer="B",
        baseline_score=0.0,
        candidates=["skill1", "skill2"],
        chosen_skill="skill1",
        skill_version="v1",
        skill_answer="A",
        skill_score=1.0,
        signature={"subfield": "portfolio management", "error_type": 3, "modality": "text-only", "required_ops": [], "missed_constraints": False},
        split="train"
    )

    logger.log_run(
        qid="q2",
        question="Portfolio question 2",
        context="Context 2",
        ground_truth="B",
        baseline_answer="B",
        baseline_score=1.0,
        candidates=["skill1", "skill2"],
        chosen_skill="skill1",
        skill_version="v1",
        skill_answer="A",
        skill_score=0.0,
        signature={"subfield": "portfolio management", "error_type": 3, "modality": "text-only", "required_ops": [], "missed_constraints": False},
        split="train"
    )

    # Collect evidence
    collector = EvidenceCollector()
    Q_plus, Q_minus = collector.collect_evidence(logger.train_log, "skill1")

    print(f"\nQ+ cards: {len(Q_plus)}")
    print(f"Q- cards: {len(Q_minus)}")

    if Q_plus:
        print("\nSample Q+ card:")
        print(json.dumps(asdict(Q_plus[0]), indent=2))

    if Q_minus:
        print("\nSample Q- card:")
        print(json.dumps(asdict(Q_minus[0]), indent=2))

    # Save evidence
    collector.save_evidence("skill1", Q_plus, Q_minus, epoch=1)
    