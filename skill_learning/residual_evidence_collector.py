"""
Residual Evidence Collector - Handle Unsolved Cases

Collects evidence from cases where baseline is wrong AND skill still doesn't fix it.
These "unsolved" cases reveal:
- Q+_discover(k): Router/trigger mismatches (another skill could solve it)
- Q0_gap: Capability gaps (no skill can solve it)

This complements the standard Q+/Q- evidence for skill refinement.
"""

import os
import json
import time
from tqdm import tqdm
from typing import Dict, List, Tuple, Optional, Any, Callable
from pathlib import Path
from dataclasses import dataclass, asdict, field
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
from openai import OpenAI

# Import prompts
try:
    # When imported as a module
    from .residual_prompts import (
        build_gap_classification_prompt,
        build_discover_explanation_prompt,
        build_gap_explanation_prompt,
        build_full_gap_diagnosis_prompt,
        build_gap_attribution_only_prompt,
    )
except ImportError:
    # When run directly
    from residual_prompts import (
        build_gap_classification_prompt,
        build_discover_explanation_prompt,
        build_gap_explanation_prompt,
        build_full_gap_diagnosis_prompt,
        build_gap_attribution_only_prompt,
    )

# LangChain for batch processing
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage
    LANGCHAIN_OPENAI_AVAILABLE = True
except ImportError:
    LANGCHAIN_OPENAI_AVAILABLE = False

try:
    from langchain_anthropic import ChatAnthropic
    LANGCHAIN_ANTHROPIC_AVAILABLE = True
except ImportError:
    LANGCHAIN_ANTHROPIC_AVAILABLE = False

LANGCHAIN_AVAILABLE = LANGCHAIN_OPENAI_AVAILABLE or LANGCHAIN_ANTHROPIC_AVAILABLE

# Import config
try:
    from .config import cfg, is_config_loaded
except ImportError:
    from skill_learning.config import cfg, is_config_loaded

# Load environment
load_dotenv()
API_KEY = os.getenv('DASHSCOPE_API_KEY') or os.getenv('OPENAI_API_KEY') or os.getenv('ANTHROPIC_API_KEY')
BASE_URL = os.getenv('QWEN_API_BASE', 'https://dashscope.aliyuncs.com/compatible-mode/v1')

# Lazy-loaded model names and provider to avoid caching fallback values before config is loaded
_gen_model_cache = None
_analyze_model_cache = None
_analyze_provider_cache = None
_client_cache = None

def get_gen_model():
    """Get generation model (lazy initialization).

    Only caches value after config is loaded to avoid caching fallback values.
    """
    global _gen_model_cache

    # If config is loaded, read from config and cache
    if is_config_loaded():
        if _gen_model_cache is None:
            config_val = cfg('models.gen')
            if config_val is not None:
                _gen_model_cache = config_val
                print(f"  [ResidualCollector] Using gen model from config: {_gen_model_cache}")
            else:
                _gen_model_cache = os.getenv('GEN_MODEL', os.getenv('MODEL', 'qwen-flash'))
                print(f"  [ResidualCollector] ⚠️  Using gen model from env/fallback: {_gen_model_cache}")
        return _gen_model_cache
    else:
        # Config not loaded yet - return env var without caching
        fallback = os.getenv('GEN_MODEL', os.getenv('MODEL', 'qwen-flash'))
        print(f"  [ResidualCollector] ⚠️  Config not loaded, using fallback gen model: {fallback}")
        return fallback

def get_analyze_model():
    """Get analysis model (lazy initialization).

    Only caches value after config is loaded to avoid caching fallback values.
    """
    global _analyze_model_cache

    # If config is loaded, read from config and cache
    if is_config_loaded():
        if _analyze_model_cache is None:
            config_val = cfg('models.analyze')
            if config_val is not None:
                _analyze_model_cache = config_val
                print(f"  [ResidualCollector] Using analyze model from config: {_analyze_model_cache}")
            else:
                _analyze_model_cache = os.getenv('ANALYZE_MODEL', os.getenv('MODEL', 'qwen-max'))
                print(f"  [ResidualCollector] ⚠️  Using analyze model from env/fallback: {_analyze_model_cache}")
        return _analyze_model_cache
    else:
        # Config not loaded yet - return env var without caching
        fallback = os.getenv('ANALYZE_MODEL', os.getenv('MODEL', 'qwen-max'))
        print(f"  [ResidualCollector] ⚠️  Config not loaded, using fallback analyze model: {fallback}")
        return fallback

def get_analyze_provider():
    """Get analyze provider (lazy initialization from config).

    Returns: 'openrouter', 'anthropic', 'dashscope', or 'auto' (default).
    When 'auto', provider is detected from model name.
    """
    global _analyze_provider_cache
    if _analyze_provider_cache is None:
        if is_config_loaded():
            config_val = cfg('models.analyze_provider')
            if config_val is not None:
                _analyze_provider_cache = config_val
                print(f"  [ResidualCollector] Using analyze provider from config: {_analyze_provider_cache}")
            else:
                _analyze_provider_cache = os.getenv('ANALYZE_PROVIDER', 'auto')
        else:
            _analyze_provider_cache = os.getenv('ANALYZE_PROVIDER', 'auto')
    return _analyze_provider_cache

def get_client():
    """Get analysis client (lazy initialization based on analyze model and provider).

    Provider selection:
    1. Explicit provider from config (openrouter, anthropic, dashscope)
    2. Auto-detect from model name when provider is 'auto':
       - anthropic/* -> OpenRouter
       - claude* -> Anthropic
       - qwen* -> DashScope
    """
    global _client_cache
    if _client_cache is None:
        analyze_model = get_analyze_model()
        analyze_provider = get_analyze_provider()

        # Explicit provider takes precedence
        if analyze_provider == 'openrouter':
            openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
            if openrouter_api_key:
                _client_cache = OpenAI(api_key=openrouter_api_key, base_url="https://openrouter.ai/api/v1")
                print(f"  [ResidualCollector] Analyze client: OpenRouter ({analyze_model})")
            else:
                raise ValueError("OPENROUTER_API_KEY required when analyze_provider is 'openrouter'")
        elif analyze_provider == 'anthropic':
            anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
            if anthropic_api_key:
                from anthropic import Anthropic
                _client_cache = Anthropic(api_key=anthropic_api_key)
                print(f"  [ResidualCollector] Analyze client: Anthropic ({analyze_model})")
            else:
                raise ValueError("ANTHROPIC_API_KEY required when analyze_provider is 'anthropic'")
        elif analyze_provider == 'dashscope':
            if API_KEY:
                _client_cache = OpenAI(api_key=API_KEY, base_url=BASE_URL)
                print(f"  [ResidualCollector] Analyze client: DashScope ({analyze_model})")
            else:
                raise ValueError("DASHSCOPE_API_KEY required when analyze_provider is 'dashscope'")
        else:
            # Auto-detect from model name
            if analyze_model.startswith('anthropic/'):
                # OpenRouter model format
                openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
                if openrouter_api_key:
                    _client_cache = OpenAI(api_key=openrouter_api_key, base_url="https://openrouter.ai/api/v1")
                    print(f"  [ResidualCollector] Analyze client: OpenRouter (auto-detected)")
                else:
                    raise ValueError(f"OPENROUTER_API_KEY required for model: {analyze_model}")
            elif analyze_model.lower().startswith('claude'):
                # Use Anthropic client for Claude models
                anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
                if anthropic_api_key:
                    from anthropic import Anthropic
                    _client_cache = Anthropic(api_key=anthropic_api_key)
                    print(f"  [ResidualCollector] Analyze client: Anthropic (auto-detected)")
                else:
                    # Fallback to OpenRouter
                    openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
                    if openrouter_api_key:
                        _client_cache = OpenAI(api_key=openrouter_api_key, base_url="https://openrouter.ai/api/v1")
                        print(f"  [ResidualCollector] Analyze client: OpenRouter (fallback)")
                    else:
                        print(f"  [ResidualCollector] ⚠️  No API key for Claude model {analyze_model}")
            elif analyze_model.lower().startswith('qwen') or 'gpt' in analyze_model.lower():
                # Use OpenAI-compatible client for Qwen/GPT models
                if API_KEY:
                    _client_cache = OpenAI(api_key=API_KEY, base_url=BASE_URL)
                    print(f"  [ResidualCollector] Analyze client: DashScope (auto-detected)")
            else:
                # Fallback to DashScope
                if API_KEY:
                    _client_cache = OpenAI(api_key=API_KEY, base_url=BASE_URL)
                    print(f"  [ResidualCollector] Analyze client: DashScope (fallback)")
    return _client_cache

def reset_analyze_cache():
    """Reset analyze caches. Call this when config changes."""
    global _analyze_model_cache, _analyze_provider_cache, _client_cache
    _analyze_model_cache = None
    _analyze_provider_cache = None
    _client_cache = None

# For backwards compatibility (deprecated - use functions instead)
client = None  # Use get_client() instead


# Root cause categories for Q0_gap diagnosis (Non-PoT mode)
ROOT_CAUSES = [
    "trigger_mismatch",       # Pattern exists but "When to Use" didn't match
    "incomplete_procedure",   # Pattern's Description/Procedure is incomplete or unclear
    "weak_example",           # Pattern's Example doesn't help with this case type
    "capability_gap"          # No existing pattern covers this case
]

# Recommended actions for each root cause (Non-PoT mode)
ACTIONS = {
    "trigger_mismatch": "update_when_to_use",           # Update "When to Use" keywords
    "incomplete_procedure": "update_description_procedure",  # Update Description/Procedure
    "weak_example": "update_example",                   # Improve Example section
    "capability_gap": "need_new_skill"                  # Create new pattern/skill
}

# Root cause categories for Q0_gap diagnosis (PoT mode)
ROOT_CAUSES_POT = [
    "weak_procedure_example",  # Match pattern but procedure incomplete or lacks worked & checked example
    "need_checks",             # Match pattern but missing CHECK steps or CODE CONSTRAINTS
    "new_pattern",             # No pattern covers this calculation type
    "mc_selection",            # Calculation correct but MC selector chose wrong option
    "context_issue"            # Context/data issue, cannot fix with skills
]

# Error types for PoT mode (pre-classification)
ERROR_TYPES_POT = [
    "mc_selection_error",      # Calculation correct, MC selector wrong
    "context_data_error",      # Context data issue, result doesn't match any option
    "execution_failed",        # Code failed to execute
    "logic_error"              # Code logic is incorrect
]

# Recommended actions for each root cause (PoT mode)
ACTIONS_POT = {
    "weak_procedure_example": "update_example",         # Add/improve procedure and worked & checked example
    "need_checks": "add_checks_and_constraints",        # Add CHECK steps and CODE CONSTRAINTS
    "new_pattern": "need_new_skill",                    # Create new skill file with code template
    "mc_selection": "update_mc_selection_skill",        # Create/update common/mc_selection.md
    "context_issue": "skip"                             # Cannot fix, skip this case
}


@dataclass
class ProbeResult:
    """Result of probing an alternative skill on an unsolved case."""
    skill_name: str
    specific_file: Optional[str]
    answer: str
    score: float
    solved: bool  # True if this probe solved the problem
    explanation: str = ""


@dataclass
class UnsolvedCard:
    """Evidence card for an unsolved case (baseline wrong AND skill wrong)."""
    # Required fields (no defaults) must come first
    qid: str
    signature: Dict
    question: str
    context: str
    ground_truth: str

    # Skill that was used (and failed) - required field
    skill_used: Dict  # {skill_name, specific_file, answer, score, explanation, all_files}

    # Optional fields (with defaults) come after required fields
    options: Optional[str] = None  # MC options text (e.g., "A. ... B. ... C. ...")

    # Baseline performance
    baseline: Dict = field(default_factory=dict)  # {answer, score, explanation}

    # Probe results from alternative skills
    probe_results: List[ProbeResult] = field(default_factory=list)

    # Diagnosis
    diagnosis: Optional[str] = None  # root_cause label
    recommended_action: Optional[str] = None
    diagnosis_explanation: Optional[str] = None
    root_cause_file: Optional[str] = None  # LLM-determined responsible file (from diagnosis)

    # Classification
    is_discoverable: bool = False  # True if some probed skill solved it
    solving_skill: Optional[str] = None  # Which skill solved it (if any)

    # PoT mode specific fields (for code-based skills)
    generated_code: Optional[str] = None  # The Python code that was generated
    execution_success: Optional[bool] = None  # Whether the code executed successfully
    error_type: Optional[str] = None  # Pre-classification: mc_selection_error, context_data_error, execution_failed, logic_error

    # Attribution and analysis (for compatibility with EvidenceCard when joining Q+)
    attribution_result: Optional[Dict] = None  # {"attributed_files": [...], "analysis": "..."}
    what_went_right_or_wrong: Optional[str] = None  # Analysis for Safety phase prompt

    # Computed properties for EvidenceCard compatibility
    @property
    def specific_skill_file(self) -> Optional[str]:
        """Get specific_skill_file from skill_used dict."""
        return self.skill_used.get('specific_file') if self.skill_used else None

    @property
    def loaded_files(self) -> Optional[List[str]]:
        """Get loaded_files from skill_used dict."""
        return self.skill_used.get('all_files', []) if self.skill_used else []

    @property
    def skill_k(self) -> Dict:
        """Get skill answer/score/explanation in EvidenceCard format."""
        if not self.skill_used:
            return {'answer': '', 'score': 0, 'explanation': '', 'execution_success': None}
        return {
            'answer': self.skill_used.get('answer', ''),
            'score': self.skill_used.get('score', 0),
            'explanation': self.skill_used.get('explanation', ''),
            'execution_success': self.execution_success  # Include execution_success for PoT mode
        }

    @property
    def skill_code(self) -> Optional[str]:
        """Get skill code (maps to generated_code for PoT mode)."""
        return self.generated_code

    @property
    def tool_call_sequence(self) -> List:
        """Get tool call sequence (not applicable for router mode, return empty list)."""
        return []

    @property
    def baseline_code(self) -> Optional[str]:
        """Get baseline code (not applicable for unsolved cases, return None)."""
        return None

    @property
    def delta(self) -> float:
        """Compute delta (skill_score - baseline_score) for EvidenceCard compatibility."""
        skill_score = self.skill_used.get('score', 0) if self.skill_used else 0
        baseline_score = self.baseline.get('score', 0) if self.baseline else 0
        return skill_score - baseline_score

    @property
    def is_fix(self) -> bool:
        """
        Check if this case is a 'fix' (skill correct, baseline wrong).

        For UnsolvedCard: Always False by default since both baseline and skill were wrong.
        After Coverage verification, this can be overridden by setting _is_fix_override.
        """
        # Allow override for post-Coverage verification
        if hasattr(self, '_is_fix_override'):
            return self._is_fix_override
        # UnsolvedCard = baseline wrong AND skill wrong, so not a fix
        return False

    @property
    def is_regress(self) -> bool:
        """
        Check if this case is a 'regression' (baseline correct, skill wrong).

        For UnsolvedCard: Always False since baseline was also wrong.
        """
        # UnsolvedCard = baseline wrong AND skill wrong, not a regression
        return False

    def mark_as_fixed(self):
        """Mark this UnsolvedCard as fixed after Coverage verification."""
        self._is_fix_override = True

    def mark_as_unfixed(self):
        """Mark this UnsolvedCard as still unfixed after Coverage verification."""
        self._is_fix_override = False


class ResidualEvidenceCollector:
    """
    Collects and analyzes unsolved cases for skill improvement.

    Unsolved = baseline_wrong AND skill_wrong

    Two categories:
    - Q+_discover: Some OTHER skill solves it (router/trigger mismatch)
    - Q0_gap: NO skill solves it (capability gap)

    Supports two skill loading modes:
    - "router": Pre-selects skill files based on keywords. Probes alternatives to find Q+_discover.
    - "progressive": Model dynamically loads files. Skips probing (no router to fix).
    """

    def __init__(
        self,
        skills_loading_mode: str = None,  # "router" or "progressive"
        max_probes_per_case: int = None,  # Max alternative skills to probe (router mode only)
        probe_same_subfield_only: bool = True,  # Only probe skills in same subfield
        enable_diagnosis: bool = None,  # Enable LLM-based diagnosis (classification + explanation)
        max_context_length: int = None,
        # Batch processing settings (for LLM-based diagnosis only)
        diagnosis_batch_size: int = None,  # Concurrent diagnoses (0=sequential)
        pot_mode: bool = None  # PoT mode: use code-based prompts and root causes
    ):
        """
        Initialize residual evidence collector.

        Args:
            skills_loading_mode: "router" (probe alternatives) or "progressive" (skip probing)
            max_probes_per_case: Maximum alternative skills to test per unsolved case (router mode only)
            probe_same_subfield_only: Only probe skills in the same subfield
            enable_diagnosis: Whether to enable LLM-based diagnosis (both classification and explanation)
                              If False, all Q0_gap cases default to capability_gap → need_new_skill
            max_context_length: Max context length for evidence cards
            diagnosis_batch_size: Number of concurrent diagnosis requests (0=sequential, default from DIAGNOSIS_BATCH_SIZE)
            pot_mode: Whether to use PoT-specific prompts and root causes (default from POT_MODE env var)
        """
        # Apply defaults from config or environment variables
        if skills_loading_mode is None:
            skills_loading_mode = cfg('skills.loading_mode') or os.getenv('SKILLS_LOADING_MODE', 'router')
        if max_probes_per_case is None:
            max_probes_per_case = cfg('residual.max_probes_per_case') or int(os.getenv('MAX_PROBES_PER_CASE', '3'))
        if enable_diagnosis is None:
            enable_diagnosis = cfg('residual.enable_diagnosis') if cfg('residual.enable_diagnosis') is not None else os.getenv('ENABLE_RESIDUAL_DIAGNOSIS', 'true').lower() == 'true'
        if max_context_length is None:
            max_context_length = cfg('residual.max_context_length') or int(os.getenv('RESIDUAL_MAX_CONTEXT_LENGTH', '800'))
        if diagnosis_batch_size is None:
            diagnosis_batch_size = cfg('residual.diagnosis_batch_size') or int(os.getenv('DIAGNOSIS_BATCH_SIZE', '10'))
        if pot_mode is None:
            pot_mode = cfg('skills.pot_mode') if cfg('skills.pot_mode') is not None else os.getenv('POT_MODE', 'false').lower() == 'true'

        if skills_loading_mode not in ("router", "progressive"):
            raise ValueError(f"Invalid skills_loading_mode: {skills_loading_mode}. Use 'router' or 'progressive'")

        self.skills_loading_mode = skills_loading_mode
        self.max_probes_per_case = max_probes_per_case
        self.probe_same_subfield_only = probe_same_subfield_only
        self.enable_diagnosis = enable_diagnosis
        self.max_context_length = max_context_length
        self.diagnosis_batch_size = diagnosis_batch_size
        self.pot_mode = pot_mode
        
        # Select root causes and actions based on pot_mode
        if self.pot_mode:
            self.root_causes = ROOT_CAUSES_POT
            self.actions = ACTIONS_POT
            # Import PoT-specific prompts
            global build_gap_classification_prompt, build_discover_explanation_prompt
            global build_gap_explanation_prompt, build_full_gap_diagnosis_prompt
            global build_gap_attribution_only_prompt
            from residual_prompts_pot import (
                build_gap_classification_prompt,
                build_discover_explanation_prompt,
                build_gap_explanation_prompt,
                build_full_gap_diagnosis_prompt,
                build_gap_attribution_only_prompt,
            )
            print(f"[ResidualEvidenceCollector] Using PoT mode (3 root causes: weak_procedure_example, need_checks, new_pattern)")
        else:
            self.root_causes = ROOT_CAUSES
            self.actions = ACTIONS
            print(f"[ResidualEvidenceCollector] Using standard mode (4 root causes: trigger_mismatch, incomplete_procedure, weak_example, capability_gap)")

    def _call_llm(self, prompt: str, max_tokens: int = 8192) -> str:
        """
        Unified LLM call supporting both OpenAI and Anthropic clients.

        Args:
            prompt: The prompt to send
            max_tokens: Maximum tokens for response (default: 8192)

        Returns:
            Response text
        """
        api_client = get_client()
        analyze_model = get_analyze_model()
        if not api_client:
            return ""

        try:
            if analyze_model.lower().startswith('claude'):
                # Anthropic API
                response = api_client.messages.create(
                    model=analyze_model,
                    max_tokens=max_tokens,
                    temperature=0.0,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text.strip()
            else:
                # OpenAI-compatible API (Qwen, GPT, etc.)
                response = api_client.chat.completions.create(
                    model=analyze_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.0,
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content.strip()
        except Exception as e:
            return f"LLM call failed: {e}"

    def collect_unsolved(
        self,
        run_log_entries: List,  # List of RunLogEntry from run_logger
    ) -> List[UnsolvedCard]:
        """
        Collect unsolved cases from run log.

        Unsolved condition: baseline_score=0 AND skill_score=0

        Args:
            run_log_entries: List of RunLogEntry objects

        Returns:
            List of UnsolvedCard objects
        """
        unsolved_cards = []

        for entry in run_log_entries:
            # Check unsolved condition: baseline wrong AND skill wrong
            baseline_wrong = entry.baseline_score == 0
            skill_wrong = entry.skill_score == 0 or entry.skill_score is None

            if baseline_wrong and skill_wrong:
                # Get all files used (for multi-file attribution)
                files = None
                skill_metadata = getattr(entry, 'skill_metadata', None)
                if skill_metadata and isinstance(skill_metadata, dict):
                    files = skill_metadata.get('loaded_files', None)
                if not files:
                    files = getattr(entry, 'all_skill_files', None)

                # Process files: deduplicate and filter SKILL.md
                if files:
                    unique_files = self._deduplicate_files(files)
                    unique_files = [f for f in unique_files if f != 'SKILL.md']
                else:
                    # Fallback to specific_skill_file
                    specific_file = entry.specific_skill_file
                    unique_files = [specific_file] if specific_file and specific_file != 'SKILL.md' else []

                # Separate common vs non-common files
                non_common_files = [f for f in unique_files if not self._is_common_file(f)]
                common_files = [f for f in unique_files if self._is_common_file(f)]

                # Default attribution strategy:
                # Prefer non-common files; if none, use common files
                # This will be refined later by LLM diagnosis (if enabled)
                if non_common_files:
                    primary_file = non_common_files[0]  # Use first non-common as default
                elif common_files:
                    primary_file = common_files[0]  # Use first common if no non-common
                else:
                    primary_file = entry.specific_skill_file or "SKILL.md"

                card = UnsolvedCard(
                    qid=entry.qid,
                    signature=entry.signature,
                    question=entry.question,
                    context=entry.context or "",
                    ground_truth=entry.ground_truth,
                    options=getattr(entry, 'options', None),  # MC options if available
                    baseline={
                        "answer": entry.baseline_answer,
                        "score": entry.baseline_score,
                        "explanation": entry.baseline_explanation or ""
                    },
                    skill_used={
                        "skill_name": entry.chosen_skill or "none",
                        "specific_file": primary_file,  # Default attribution
                        "all_files": unique_files,  # All files for context and diagnosis
                        "non_common_files": non_common_files,  # For diagnosis reference
                        "common_files": common_files,  # For diagnosis reference
                        "answer": entry.skill_answer or "",
                        "score": entry.skill_score or 0,
                        "explanation": entry.skill_explanation or ""
                    },
                    # PoT mode specific fields (from skill run)
                    generated_code=getattr(entry, 'skill_code', None),  # Use skill_code, not generated_code
                    execution_success=getattr(entry, 'skill_execution_success', None)  # Use skill_execution_success
                )
                unsolved_cards.append(card)

        print(f"\n[Residual Evidence] Found {len(unsolved_cards)} unsolved cases")
        return unsolved_cards

    def _deduplicate_files(self, files: List[str]) -> List[str]:
        """Deduplicate file list while preserving order."""
        seen = set()
        result = []
        for f in files:
            if f not in seen:
                seen.add(f)
                result.append(f)
        return result

    def _is_common_file(self, file_path: str) -> bool:
        """Check if file is in common/ folder."""
        return file_path.startswith('common/') or '/common/' in file_path

    def probe_alternative_skills(
        self,
        unsolved_cards: List[UnsolvedCard],
        router=None,  # SkillsRouter instance (required for router mode, optional for progressive)
        gen_func=None,  # Function to generate answer: gen_func(question, context, options, skill_content) -> (answer, explanation)
        eval_func=None,  # Function to evaluate: eval_func(question, context, answer, explanation, ground_truth) -> score
        max_cards: Optional[int] = None  # Limit cards to probe (for efficiency)
    ) -> Tuple[List[UnsolvedCard], List[UnsolvedCard]]:
        """
        Probe alternative skills on unsolved cases (sequential).

        Behavior depends on skills_loading_mode:
        - "router": Probes alternative skill files to find Q+_discover (router mismatches)
        - "progressive": Skips probing entirely (model already had agency to load any file)

        For router mode, each unsolved case:
        1. Find alternative skills (same subfield, not already used)
        2. Try each alternative skill sequentially
        3. Classify as Q+_discover (some skill solves) or Q0_gap (none solve)

        For progressive mode:
        - All unsolved cases become Q0_gap (no router to fix)
        - Q+_discover is always empty

        Args:
            unsolved_cards: List of UnsolvedCard to probe
            router: SkillsRouter instance for finding alternative skills (router mode only)
            gen_func: Function to generate answers with a skill (router mode only)
            eval_func: Function to evaluate answers (router mode only)
            max_cards: Maximum cards to probe (None = all)

        Returns:
            Tuple of (Q_plus_discover, Q_zero_gap) lists
        """

        if max_cards:
            unsolved_cards = unsolved_cards[:max_cards]

        Q_plus_discover = []  # Cases where alternative skill solves it
        Q_zero_gap = []       # Cases where no skill solves it

        # Progressive mode: skip probing, all unsolved are Q0_gap
        if self.skills_loading_mode == "progressive":
            print(f"\n[Progressive Mode] Skipping alternative skill probing")
            print(f"  Reason: Model already had agency to load any skill file")
            print(f"  All {len(unsolved_cards)} unsolved cases classified as Q0_gap (capability gap)")

            for card in unsolved_cards:
                card.is_discoverable = False
                card.solving_skill = None
                Q_zero_gap.append(card)

            return Q_plus_discover, Q_zero_gap

        # Router mode: validate required arguments
        if router is None or gen_func is None or eval_func is None:
            raise ValueError("router, gen_func, and eval_func are required for router mode")

        print(f"\n[Router Mode] Testing alternative skills on {len(unsolved_cards)} unsolved cases...")

        for card in tqdm(unsolved_cards, desc="Probing alternatives"):
            subfield = card.signature.get('subfield', 'unknown')
            used_skill = card.skill_used.get('skill_name')
            used_file = card.skill_used.get('specific_file')

            # Find alternative skills to probe
            alternatives = self._find_alternative_skills(
                router, subfield, used_skill, used_file, card.question
            )

            # Probe each alternative
            solved = False
            solving_skill = None

            for skill_name, specific_file, skill_content in alternatives[:self.max_probes_per_case]:
                try:
                    answer, explanation = gen_func(
                        card.question, card.context, card.options, skill_content
                    )
                    score = eval_func(
                        card.question, card.context, answer, explanation, card.ground_truth
                    )

                    probe_result = ProbeResult(
                        skill_name=skill_name,
                        specific_file=specific_file,
                        answer=answer,
                        score=score,
                        solved=(score == 1.0),
                        explanation=explanation
                    )
                    card.probe_results.append(probe_result)

                    if score == 1.0:
                        solved = True
                        solving_skill = specific_file or skill_name
                        break

                except Exception as e:
                    print(f"  ⚠️  Probe failed for {skill_name}: {e}")
                    continue

            card.is_discoverable = solved
            card.solving_skill = solving_skill

            if solved:
                Q_plus_discover.append(card)
            else:
                Q_zero_gap.append(card)

        print(f"\n[Router Mode Probe Results]")
        print(f"  Q+_discover (router/trigger issue): {len(Q_plus_discover)}")
        print(f"  Q0_gap (capability gap): {len(Q_zero_gap)}")

        return Q_plus_discover, Q_zero_gap

    def _find_alternative_skills(
        self,
        router,
        subfield: str,
        used_skill: str,
        used_file: Optional[str],
        question: str
    ) -> List[Tuple[str, Optional[str], str]]:
        """
        Find alternative skill files to probe.

        Adapted for the 2-level skill folder structure where router has:
        - router.all_files: Dict[str, Path] (relative_path → absolute Path)
        - router.skill_dir: Path to the skill set root

        Args:
            router: SkillsRouter instance (2-level structure)
            subfield: The subfield of the question
            used_skill: Skill set name that was already used
            used_file: Specific file path that was already used (e.g., "portfolio_management/concept_confusion.md")
            question: The question text

        Returns:
            List of (skill_set_name, relative_file_path, content) tuples
        """
        alternatives = []
        skill_set_name = router.skill_dir.name  # e.g., "famma-non-arithmetic-v1"

        for rel_path, abs_path in router.all_files.items():
            # Skip the file that was already used
            if rel_path == used_file:
                continue

            # Skip README and SKILL.md (index file, always loaded)
            if abs_path.name in ["README.md", "SKILL.md"]:
                continue

            # Subfield filtering: check if the file is in the same subfield folder
            # or in common/ (cross-subfield)
            if self.probe_same_subfield_only and subfield:
                file_folder = rel_path.split('/')[0] if '/' in rel_path else ''
                is_common = file_folder == 'common'
                # Normalize subfield for folder matching
                subfield_lower = subfield.lower().replace(' ', '_')
                folder_matches = (
                    subfield_lower in file_folder.lower()
                    or file_folder.lower() in subfield_lower
                )
                if not is_common and not folder_matches:
                    continue

            try:
                content = abs_path.read_text(encoding='utf-8')
                alternatives.append((skill_set_name, rel_path, content))
            except Exception:
                continue

        return alternatives

    def diagnose_unsolved(
        self,
        unsolved_cards: List[UnsolvedCard],
        Q_plus_discover: List[UnsolvedCard],
        Q_zero_gap: List[UnsolvedCard],
        router=None  # SkillsRouter instance for accessing skill content
    ) -> None:
        """
        Diagnose root cause for each unsolved case.

        Updates cards in-place with diagnosis and recommended_action.

        Mode behavior:
        - Router mode: Q+_discover gets "trigger_mismatch" diagnosis
        - Progressive mode: Q+_discover is always empty (all cases are Q0_gap)

        Q0_gap diagnosis (pattern-based structure):
        - trigger_mismatch: "When to Use" didn't match this case
        - incomplete_procedure: Description/Procedure is incomplete
        - weak_example: Example doesn't help with this case type
        - capability_gap: No pattern covers this case

        Args:
            unsolved_cards: All unsolved cards
            Q_plus_discover: Cards where alternative skill solved it (empty in progressive mode)
            Q_zero_gap: Cards where no skill solved it (all unsolved in progressive mode)
            router: SkillsRouter instance for accessing skill content during diagnosis
        """
        mode_info = f"[{self.skills_loading_mode.capitalize()} Mode]"

        # ===== PHASE 1: Classification =====
        # Q+_discover: Always trigger_mismatch (rule-based, no LLM needed)
        # Q0_gap: Classify via LLM OR default to capability_gap

        print(f"\n{mode_info} Classifying {len(Q_plus_discover)} discover + {len(Q_zero_gap)} gap cases...")

        # Q+_discover classification (always trigger_mismatch in non-PoT, not applicable in PoT)
        for card in Q_plus_discover:
            if self.pot_mode:
                # PoT mode: Q+_discover shouldn't exist (routing handled by SKILL.md)
                # But if it does, treat as routing issue
                card.diagnosis = "routing_mismatch"
                card.recommended_action = "update_skill_md_routing"
            else:
                card.diagnosis = "trigger_mismatch"
                card.recommended_action = self.actions["trigger_mismatch"]

        # Q0_gap classification and explanation (controlled by enable_diagnosis)
        if Q_zero_gap:
            if self.enable_diagnosis:
                # LLM-based classification to determine root cause (also returns explanation)
                if self.diagnosis_batch_size > 0 and len(Q_zero_gap) > 1:
                    self._classify_gap_cases_batch(Q_zero_gap, router)
                else:
                    self._classify_gap_cases_sequential(Q_zero_gap, router)
            else:
                # V2: Diagnosis disabled, but still run attribution to determine responsible file
                default_cause = "new_pattern" if self.pot_mode else "capability_gap"
                print(f"  Diagnosis disabled, running attribution-only for {len(Q_zero_gap)} cases (default: {default_cause})")
                self._attribute_gap_cases_batch(Q_zero_gap, router, default_cause)

        # Q+_discover explanation (also controlled by enable_diagnosis)
        if not self.enable_diagnosis:
            # Set basic explanations without LLM
            for card in Q_plus_discover:
                if not card.diagnosis_explanation:
                    card.diagnosis_explanation = f"Alternative skill '{card.solving_skill}' solved this case"
            return

        # Generate detailed explanations ONLY for cards without explanations
        # (Q0_gap cards already have explanations from classification, only Q+_discover needs them)
        cards_needing_explanation = [card for card in (Q_plus_discover + Q_zero_gap) if not card.diagnosis_explanation]

        if cards_needing_explanation:
            print(f"  Generating explanations for {len(cards_needing_explanation)} cards (skipped {len(Q_plus_discover) + len(Q_zero_gap) - len(cards_needing_explanation)} with existing explanations)")
            if self.diagnosis_batch_size > 0 and len(cards_needing_explanation) > 1:
                self._generate_explanations_batch(cards_needing_explanation)
            else:
                self._generate_explanations_sequential(cards_needing_explanation)
        else:
            print(f"  All cards already have explanations from classification (skipped explanation LLM calls)")

    def _attribute_gap_cases_batch(
        self,
        Q_zero_gap: List[UnsolvedCard],
        router=None,
        default_cause: str = "capability_gap"
    ) -> None:
        """
        V2: Attribution-only for Q0_gap cases when diagnosis is disabled.

        Only determines which file is responsible, without diagnosing root cause.
        All cases default to new_pattern/capability_gap action.

        Args:
            Q_zero_gap: List of unsolved cards to attribute
            router: SkillsRouter for loading skill content
            default_cause: Default diagnosis (new_pattern for PoT, capability_gap otherwise)
        """
        client = get_client()
        if not client:
            # No client - use fallback: first non-common file
            print(f"  No LLM client, using fallback attribution (first non-common file)")
            for card in Q_zero_gap:
                card.diagnosis = default_cause
                card.recommended_action = self.actions[default_cause]
                card.diagnosis_explanation = f"Root cause: {default_cause}"
                # Fallback: first non-common file
                all_files = card.skill_used.get('all_files', [])
                common_files = card.skill_used.get('common_files', [])
                fallback_file = None
                for f in all_files:
                    if f not in common_files and f != "SKILL.md":
                        fallback_file = f
                        break
                if fallback_file:
                    card.root_cause_file = fallback_file
                    card.skill_used['specific_file'] = fallback_file
            return

        print(f"  Running attribution-only for {len(Q_zero_gap)} cards...")

        for card in tqdm(Q_zero_gap, desc="Attributing Q0_gap"):
            # Set default diagnosis (no root cause classification)
            card.diagnosis = default_cause
            card.recommended_action = self.actions[default_cause]

            # Load skill files content
            all_files = card.skill_used.get('all_files', [])
            non_common_files = card.skill_used.get('non_common_files', [])
            common_files = card.skill_used.get('common_files', [])

            all_skill_contents = {}
            if router and all_files:
                for file_path in all_files:
                    full_path = router.skill_dir / file_path
                    if full_path.exists():
                        try:
                            with open(full_path, 'r', encoding='utf-8') as f:
                                all_skill_contents[file_path] = f.read()
                        except Exception:
                            pass

            # Build attribution-only prompt
            prompt_args = {
                'question': card.question,
                'context': card.context or '',
                'ground_truth': card.ground_truth,
                'skill_answer': card.skill_used.get('answer', 'N/A'),
                'all_files': all_files,
                'non_common_files': non_common_files,
                'common_files': common_files,
                'all_skill_contents': all_skill_contents,
                'options': card.options or ''
            }

            # Add PoT-specific arguments if in PoT mode
            if self.pot_mode:
                prompt_args['generated_code'] = card.generated_code or ''
                prompt_args['execution_success'] = card.execution_success if card.execution_success is not None else True

            prompt = build_gap_attribution_only_prompt(**prompt_args)

            # Call LLM
            try:
                result_text = self._call_llm(prompt, max_tokens=1024)

                if result_text and "failed" not in result_text.lower():
                    # Parse JSON response
                    import re
                    json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
                    if json_match:
                        result = json.loads(json_match.group(0))
                        attributed_file = result.get("attributed_file")
                        reasoning = result.get("reasoning", "")

                        if attributed_file and attributed_file in all_files:
                            card.root_cause_file = attributed_file
                            card.skill_used['specific_file'] = attributed_file
                            card.diagnosis_explanation = reasoning or f"Attributed to {attributed_file}"
                            continue

                # Fallback if attribution failed
                fallback_file = None
                for f in all_files:
                    if f not in common_files and f != "SKILL.md":
                        fallback_file = f
                        break
                if fallback_file:
                    card.root_cause_file = fallback_file
                    card.skill_used['specific_file'] = fallback_file
                card.diagnosis_explanation = f"Root cause: {default_cause}"

            except Exception as e:
                print(f"  ⚠️  Attribution failed for {card.qid}: {e}")
                card.diagnosis_explanation = f"Root cause: {default_cause}"

    def _classify_gap_cases_sequential(self, Q_zero_gap: List[UnsolvedCard], router=None) -> None:
        """Sequential classification of Q0_gap cases (determines root cause and explanation)."""
        for card in tqdm(Q_zero_gap, desc="Classifying Q0_gap"):
            diagnosis, action, explanation, root_cause_file = self._diagnose_gap_case(card, router)
            card.diagnosis = diagnosis
            card.recommended_action = action
            card.diagnosis_explanation = explanation  # Save explanation from first LLM call
            card.root_cause_file = root_cause_file  # LLM-determined responsible file

            # Update specific_file based on LLM's judgment (if provided and valid)
            if root_cause_file and root_cause_file in card.skill_used.get('all_files', []):
                card.skill_used['specific_file'] = root_cause_file
                print(f"  [{card.qid}] Attributed to: {root_cause_file} (LLM diagnosis)")
            elif root_cause_file:
                print(f"  [{card.qid}] LLM suggested {root_cause_file} but not in files used, keeping {card.skill_used['specific_file']}")
            else:
                print(f"  [{card.qid}] No file attribution from LLM, keeping default {card.skill_used['specific_file']}")

    def _classify_gap_cases_batch(self, Q_zero_gap: List[UnsolvedCard], router=None) -> None:
        """Batch classification of Q0_gap cases using LangChain (returns diagnosis + explanation in one call)."""
        if not LANGCHAIN_AVAILABLE:
            print(f"  LangChain not available, using sequential classification")
            self._classify_gap_cases_sequential(Q_zero_gap, router)
            return

        print(f"  Using LangChain batch classification (max_concurrency={self.diagnosis_batch_size})")

        # Initialize LangChain client based on analyze_provider (not just model name)
        analyze_model = get_analyze_model()
        analyze_provider = get_analyze_provider()

        # Determine which client to use based on provider
        if analyze_provider == 'openrouter' or analyze_model.startswith('anthropic/'):
            # OpenRouter: use ChatOpenAI with OpenRouter credentials
            if not LANGCHAIN_OPENAI_AVAILABLE:
                print(f"  langchain-openai not available, falling back to sequential")
                self._classify_gap_cases_sequential(Q_zero_gap, router)
                return

            openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
            if not openrouter_api_key:
                print(f"  OPENROUTER_API_KEY not set, falling back to sequential")
                self._classify_gap_cases_sequential(Q_zero_gap, router)
                return

            llm = ChatOpenAI(
                model=analyze_model,
                api_key=openrouter_api_key,
                base_url="https://openrouter.ai/api/v1",
                temperature=0.0,
                max_tokens=8192
            )
        elif analyze_provider == 'anthropic' or analyze_model.lower().startswith('claude'):
            # Anthropic: use ChatAnthropic
            if not LANGCHAIN_ANTHROPIC_AVAILABLE:
                print(f"  langchain-anthropic not available, falling back to sequential")
                self._classify_gap_cases_sequential(Q_zero_gap, router)
                return

            anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
            if not anthropic_api_key:
                print(f"  ANTHROPIC_API_KEY not set, falling back to sequential")
                self._classify_gap_cases_sequential(Q_zero_gap, router)
                return

            llm = ChatAnthropic(
                model=analyze_model,
                api_key=anthropic_api_key,
                temperature=0.0,
                max_tokens=8192
            )
        else:
            # DashScope/Qwen: use ChatOpenAI with DashScope credentials
            if not LANGCHAIN_OPENAI_AVAILABLE:
                print(f"  langchain-openai not available, falling back to sequential")
                self._classify_gap_cases_sequential(Q_zero_gap, router)
                return

            llm = ChatOpenAI(
                model=analyze_model,
                api_key=API_KEY,
                base_url=BASE_URL,
                temperature=0.0,
                max_tokens=8192
            )

        # Build FULL diagnosis prompts (not just classification) to get explanation in one call
        prompts = []
        for card in Q_zero_gap:
            # Use same logic as _diagnose_gap_case to build full diagnosis prompt
            skill_name = card.skill_used.get('skill_name', '')
            specific_file = card.skill_used.get('specific_file', '')
            all_files = card.skill_used.get('all_files', [])
            non_common_files = card.skill_used.get('non_common_files', [])
            common_files = card.skill_used.get('common_files', [])

            # Load ALL skill files' contents (not just specific_file)
            all_skill_contents = {}
            if router and all_files:
                for file_path in all_files:
                    full_path = router.skill_dir / file_path
                    if full_path.exists():
                        try:
                            with open(full_path, 'r', encoding='utf-8') as f:
                                all_skill_contents[file_path] = f.read()
                        except Exception:
                            pass

            # Fallback: if no all_files, try specific_file
            if not all_skill_contents and router and specific_file:
                skill_file_path = router.skill_dir / specific_file
                if skill_file_path.exists():
                    try:
                        with open(skill_file_path, 'r', encoding='utf-8') as f:
                            all_skill_contents[specific_file] = f.read()
                    except Exception:
                        pass

            prompt_args = {
                'question': card.question,
                'context': card.context or '',
                'ground_truth': card.ground_truth,
                'skill_name': skill_name,
                'specific_file': specific_file,
                'skill_answer': card.skill_used.get('answer', 'N/A'),
                'skill_explanation': card.skill_used.get('explanation', 'N/A'),
                'all_skill_contents': all_skill_contents,  # NEW: all files' contents
                'options': card.options or '',
                'all_files': all_files,
                'non_common_files': non_common_files,
                'common_files': common_files
            }

            if self.pot_mode:
                prompt_args['generated_code'] = card.generated_code or ''
                prompt_args['execution_success'] = card.execution_success if card.execution_success is not None else True

            prompt = build_full_gap_diagnosis_prompt(**prompt_args)
            prompts.append([HumanMessage(content=prompt)])

        if not prompts:
            return

        # Execute batch
        try:
            responses = llm.batch(prompts, config={"max_concurrency": self.diagnosis_batch_size})

            # Parse results (JSON format with root_cause and explanation)
            for card, response in zip(Q_zero_gap, responses):
                result_text = response.content.strip() if response else ""

                # Parse JSON response
                import re
                json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
                if json_match:
                    try:
                        result = json.loads(json_match.group(0))
                        root_cause = result.get("root_cause", "capability_gap")
                        explanation = result.get("explanation", "")
                        root_cause_file = result.get("root_cause_file", None)  # Extract file attribution
                        error_type = result.get("error_type", None)  # Extract error type (PoT mode)

                        # Validate root cause
                        if root_cause not in self.root_causes:
                            root_cause = "new_pattern" if self.pot_mode else "capability_gap"

                        # Validate error type (PoT mode only)
                        if self.pot_mode and error_type and error_type not in ERROR_TYPES_POT:
                            error_type = "logic_error"  # Default to logic_error if invalid

                        card.diagnosis = root_cause
                        card.recommended_action = self.actions.get(root_cause, "need_new_skill")
                        card.diagnosis_explanation = explanation  # Save explanation from first LLM call
                        card.root_cause_file = root_cause_file
                        if self.pot_mode:
                            card.error_type = error_type  # Save error type for PoT mode

                        # Update specific_file based on LLM's judgment (same as sequential)
                        all_files = card.skill_used.get('all_files', [])
                        if root_cause_file and all_files and root_cause_file in all_files:
                            card.skill_used['specific_file'] = root_cause_file
                            print(f"  [{card.qid}] error_type={error_type}, Attributed to: {root_cause_file} (LLM batch diagnosis)")
                        elif root_cause_file:
                            print(f"  [{card.qid}] error_type={error_type}, LLM suggested {root_cause_file} but not in files used, keeping default")
                        # No print for None case to avoid spam in batch mode
                    except json.JSONDecodeError:
                        # Fallback to simple parsing if JSON fails
                        diagnosis, action = self._parse_gap_diagnosis(result_text)
                        card.diagnosis = diagnosis
                        card.recommended_action = action
                        card.diagnosis_explanation = result_text
                else:
                    # No JSON found, use simple parsing
                    diagnosis, action = self._parse_gap_diagnosis(result_text)
                    card.diagnosis = diagnosis
                    card.recommended_action = action
                    card.diagnosis_explanation = result_text

            print(f"  Batch classification complete (with explanations)")

        except Exception as e:
            print(f"  Batch classification failed: {e}, falling back to sequential")
            self._classify_gap_cases_sequential(Q_zero_gap, router)

    def _generate_explanations_sequential(self, cards: List[UnsolvedCard]) -> None:
        """Sequential explanation generation for all cards."""
        for card in tqdm(cards, desc="Generating explanations"):
            case_type = "discover" if card.is_discoverable else "gap"
            card.diagnosis_explanation = self._generate_diagnosis_explanation(card, case_type)

    def _generate_explanations_batch(self, cards: List[UnsolvedCard]) -> None:
        """Batch explanation generation using LangChain."""
        if not LANGCHAIN_AVAILABLE:
            print(f"  LangChain not available, using sequential explanation generation")
            self._generate_explanations_sequential(cards)
            return

        print(f"  Using LangChain batch explanation (max_concurrency={self.diagnosis_batch_size})")

        # Initialize LangChain client based on model type
        analyze_model = get_analyze_model()
        if analyze_model.lower().startswith('claude'):
            # Use Anthropic client for Claude models
            if not LANGCHAIN_ANTHROPIC_AVAILABLE:
                print(f"  langchain-anthropic not available, falling back to sequential")
                self._generate_explanations_sequential(cards)
                return

            anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
            if not anthropic_api_key:
                print(f"  ANTHROPIC_API_KEY not set, falling back to sequential")
                self._generate_explanations_sequential(cards)
                return

            llm = ChatAnthropic(
                model=analyze_model,
                api_key=anthropic_api_key,
                temperature=0.0,
                max_tokens=8192
            )
        else:
            # Use OpenAI-compatible client for Qwen/GPT models
            if not LANGCHAIN_OPENAI_AVAILABLE:
                print(f"  langchain-openai not available, falling back to sequential")
                self._generate_explanations_sequential(cards)
                return

            llm = ChatOpenAI(
                model=analyze_model,
                api_key=API_KEY,
                base_url=BASE_URL,
                temperature=0.0,
                max_tokens=8192
            )

        # Build explanation prompts
        prompts = []
        for card in cards:
            case_type = "discover" if card.is_discoverable else "gap"
            prompt = self._build_explanation_prompt(card, case_type)
            prompts.append([HumanMessage(content=prompt)])

        if not prompts:
            return

        # Execute batch
        try:
            responses = llm.batch(prompts, config={"max_concurrency": self.diagnosis_batch_size})

            # Store results
            for card, response in zip(cards, responses):
                card.diagnosis_explanation = response.content.strip() if response else "Explanation generation failed"

            print(f"  Batch explanation generation complete")

        except Exception as e:
            print(f"  Batch explanation failed: {e}, falling back to sequential")
            self._generate_explanations_sequential(cards)

    def _build_explanation_prompt(self, card: UnsolvedCard, case_type: str) -> str:
        """Build explanation prompt for a card using imported prompt functions."""
        if case_type == "discover":
            return build_discover_explanation_prompt(
                question=card.question,
                subfield=card.signature.get('subfield', 'unknown'),
                skill_name=card.skill_used.get('skill_name', ''),
                specific_file=card.skill_used.get('specific_file', ''),
                skill_answer=card.skill_used.get('answer', 'N/A'),
                solving_skill=card.solving_skill or '',
                ground_truth=card.ground_truth,
                options=card.options or ''
            )
        else:
            return build_gap_explanation_prompt(
                question=card.question,
                subfield=card.signature.get('subfield', 'unknown'),
                diagnosis=card.diagnosis or 'capability_gap',
                skill_name=card.skill_used.get('skill_name', ''),
                skill_answer=card.skill_used.get('answer', 'N/A'),
                ground_truth=card.ground_truth,
                options=card.options or ''
            )

    def _build_gap_classification_prompt(self, card: UnsolvedCard, router=None) -> str:
        """Build classification prompt for Q0_gap case using imported prompt function."""
        # Get skill content if available
        skill_content = ""
        skill_name = card.skill_used.get('skill_name', '')
        specific_file = card.skill_used.get('specific_file', '')

        if router and specific_file:
            skill_file_path = router.skill_dir / specific_file
            if skill_file_path.exists():
                try:
                    skill_content = skill_file_path.read_text(encoding='utf-8')
                except Exception:
                    pass

        # Build base arguments
        prompt_args = {
            'question': card.question,
            'ground_truth': card.ground_truth,
            'skill_name': skill_name,
            'specific_file': specific_file,
            'skill_answer': card.skill_used.get('answer', 'N/A'),
            'skill_content': skill_content,
            'options': card.options or ''
        }
        
        # Add PoT-specific arguments if in PoT mode
        if self.pot_mode:
            prompt_args['generated_code'] = card.generated_code or ''
            prompt_args['execution_success'] = card.execution_success if card.execution_success is not None else True
        
        return build_gap_classification_prompt(**prompt_args)

    def _parse_gap_diagnosis(self, response: str) -> Tuple[str, str]:
        """Parse gap diagnosis response to extract root cause."""
        response_lower = response.lower()

        # Check for each root cause (mode-specific)
        for root_cause in self.root_causes:
            if root_cause.replace('_', ' ') in response_lower or root_cause in response_lower:
                action = self.actions.get(root_cause, "need_new_skill")
                return root_cause, action
        
        # Default fallback
        if self.pot_mode:
            return "new_pattern", self.actions["new_pattern"]
        else:
            return "capability_gap", self.actions["capability_gap"]

    def _generate_diagnosis_explanation(self, card: UnsolvedCard, case_type: str) -> str:
        """Generate LLM-based diagnosis explanation using imported prompt functions."""
        if not client:
            return f"Discovered by: {card.solving_skill}" if case_type == "discover" else "Capability gap"

        # Build prompt using imported functions
        if case_type == "discover":
            solving_answer = card.probe_results[-1].answer if card.probe_results else ''
            prompt = build_discover_explanation_prompt(
                question=card.question,
                subfield=card.signature.get('subfield', 'unknown'),
                skill_name=card.skill_used.get('skill_name', ''),
                specific_file=card.skill_used.get('specific_file', ''),
                skill_answer=card.skill_used.get('answer', 'N/A'),
                solving_skill=card.solving_skill or '',
                ground_truth=card.ground_truth,
                solving_answer=solving_answer,  # Optional parameter
                options=card.options or ''
            )
        else:
            prompt = build_gap_explanation_prompt(
                question=card.question,
                subfield=card.signature.get('subfield', 'unknown'),
                skill_name=card.skill_used.get('skill_name', ''),
                skill_answer=card.skill_used.get('answer', 'N/A'),
                ground_truth=card.ground_truth,
                diagnosis=card.diagnosis or '',  # Optional parameter
                options=card.options or ''
            )

        # Use unified LLM call (supports both OpenAI and Anthropic)
        return self._call_llm(prompt, max_tokens=8192)

    def _diagnose_gap_case(self, card: UnsolvedCard, router=None) -> Tuple[str, str, str, Optional[str]]:
        """
        Diagnose a Q0_gap case to determine specific root cause.

        Root causes (pattern-based skill structure):
        - trigger_mismatch: "When to Use" didn't match
        - incomplete_procedure: Description/Procedure incomplete
        - weak_example: Example doesn't help generalization
        - capability_gap: No pattern covers this case

        Args:
            card: The unsolved card to diagnose
            router: SkillsRouter instance for accessing skill content

        Returns:
            (root_cause, action, explanation, root_cause_file)
        """
        if not client:
            default_cause = "new_pattern" if self.pot_mode else "capability_gap"
            return default_cause, self.actions[default_cause], "No skill covers this case", None

        # Get the actual skill content if router is available
        skill_name = card.skill_used.get('skill_name', '')
        specific_file = card.skill_used.get('specific_file', '')
        all_files = card.skill_used.get('all_files', [])
        non_common_files = card.skill_used.get('non_common_files', [])
        common_files = card.skill_used.get('common_files', [])

        # Load ALL skill files' contents (not just specific_file)
        all_skill_contents = {}  # file_path -> content
        if router and all_files:
            for file_path in all_files:
                full_path = router.skill_dir / file_path
                if full_path.exists():
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            all_skill_contents[file_path] = f.read()
                    except Exception:
                        pass

        # Fallback: if no all_files, try specific_file
        if not all_skill_contents and router and specific_file:
            skill_file_path = router.skill_dir / specific_file
            if skill_file_path.exists():
                try:
                    with open(skill_file_path, 'r', encoding='utf-8') as f:
                        all_skill_contents[specific_file] = f.read()
                except Exception:
                    pass

        # Build base arguments
        prompt_args = {
            'question': card.question,
            'context': card.context or '',
            'ground_truth': card.ground_truth,
            'skill_name': skill_name,
            'specific_file': specific_file,
            'skill_answer': card.skill_used.get('answer', 'N/A'),
            'skill_explanation': card.skill_used.get('explanation', 'N/A'),
            'all_skill_contents': all_skill_contents,  # NEW: all files' contents
            'options': card.options or '',
            'all_files': all_files,
            'non_common_files': non_common_files,
            'common_files': common_files
        }
        
        # Add PoT-specific arguments if in PoT mode
        if self.pot_mode:
            prompt_args['generated_code'] = card.generated_code or ''
            prompt_args['execution_success'] = card.execution_success if card.execution_success is not None else True
        
        # Build prompt using imported function
        prompt = build_full_gap_diagnosis_prompt(**prompt_args)

        # Use unified LLM call (supports both OpenAI and Anthropic)
        result_text = self._call_llm(prompt, max_tokens=8192)

        if not result_text or "failed" in result_text.lower():
            default_cause = "new_pattern" if self.pot_mode else "capability_gap"
            return default_cause, self.actions[default_cause], result_text, None

        # Parse JSON response
        import re
        json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
        if json_match:
            try:
                result = json.loads(json_match.group(0))
                root_cause = result.get("root_cause", "capability_gap")
                explanation = result.get("explanation", "")
                root_cause_file = result.get("root_cause_file", None)
                error_type = result.get("error_type", None)  # Extract error type (PoT mode)

                # Validate root cause
                if root_cause not in self.root_causes:
                    root_cause = "new_pattern" if self.pot_mode else "capability_gap"

                # Validate and set error type (PoT mode only)
                if self.pot_mode:
                    if error_type and error_type not in ERROR_TYPES_POT:
                        error_type = "logic_error"  # Default to logic_error if invalid
                    card.error_type = error_type  # Set directly on card

                # Validate root_cause_file is in all_files
                if root_cause_file and all_files and root_cause_file not in all_files:
                    print(f"  ⚠️  LLM returned invalid root_cause_file: {root_cause_file} not in {all_files}")
                    root_cause_file = None

                action = self.actions.get(root_cause, "need_new_skill")
                return root_cause, action, explanation, root_cause_file
            except json.JSONDecodeError:
                pass

        default_cause = "new_pattern" if self.pot_mode else "capability_gap"
        return default_cause, self.actions[default_cause], result_text, None

    def group_by_action(
        self,
        Q_plus_discover: List[UnsolvedCard],
        Q_zero_gap: List[UnsolvedCard]
    ) -> Dict[str, List[UnsolvedCard]]:
        """
        Group unsolved cases by recommended action.

        Args:
            Q_plus_discover: Cards where alternative skill solved it
            Q_zero_gap: Cards where no skill solved it

        Returns:
            Dict mapping action -> list of cards
        """
        grouped = defaultdict(list)

        for card in Q_plus_discover + Q_zero_gap:
            action = card.recommended_action or "unknown"
            grouped[action].append(card)

        return dict(grouped)

    def group_by_subfield_and_skill(
        self,
        cards: List[UnsolvedCard]
    ) -> Dict[str, Dict[str, List[UnsolvedCard]]]:
        """
        Group cards by subfield and then by skill file.

        Useful for identifying which skill files need updates.

        Args:
            cards: List of unsolved cards

        Returns:
            Dict[subfield][skill_file] -> list of cards
        """
        grouped = defaultdict(lambda: defaultdict(list))

        for card in cards:
            subfield = card.signature.get('subfield', 'unknown')
            skill_file = card.skill_used.get('specific_file') or 'SKILL.md'
            grouped[subfield][skill_file].append(card)

        return {k: dict(v) for k, v in grouped.items()}

    def save_residual_evidence(
        self,
        Q_plus_discover: List[UnsolvedCard],
        Q_zero_gap: List[UnsolvedCard],
        output_dir: str,
        epoch: int = 0
    ) -> None:
        """
        Save residual evidence to disk.

        Args:
            Q_plus_discover: Cards where alternative skill solved it
            Q_zero_gap: Cards where no skill solved it
            output_dir: Output directory
            epoch: Epoch number
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Convert to JSON-serializable format
        def card_to_dict(card: UnsolvedCard) -> dict:
            d = asdict(card)
            # Convert ProbeResult objects
            d['probe_results'] = [asdict(pr) for pr in card.probe_results]
            return d

        evidence = {
            "epoch": epoch,
            "skills_loading_mode": self.skills_loading_mode,
            "pot_mode": self.pot_mode,
            "summary": {
                "total_unsolved": len(Q_plus_discover) + len(Q_zero_gap),
                "Q_plus_discover": len(Q_plus_discover),
                "Q_zero_gap": len(Q_zero_gap)
            },
            "Q_plus_discover": [card_to_dict(c) for c in Q_plus_discover],
            "Q_zero_gap": [card_to_dict(c) for c in Q_zero_gap],
            "by_action": {
                action: len([c for c in Q_plus_discover + Q_zero_gap
                           if c.recommended_action == action])
                for action in self.actions.values()
            }
        }

        output_file = output_path / f"residual_evidence_epoch{epoch}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(evidence, f, indent=2, ensure_ascii=False)

        print(f"✓ Saved residual evidence: {output_file}")

        # Also save a summary CSV for quick review
        summary_data = []
        for card in Q_plus_discover:
            summary_data.append({
                "qid": card.qid,
                "subfield": card.signature.get('subfield'),
                "category": "Q+_discover",
                "skill_used": card.skill_used.get('skill_name'),
                "file_used": card.skill_used.get('specific_file'),
                "solving_skill": card.solving_skill,
                "diagnosis": card.diagnosis,
                "action": card.recommended_action
            })
        for card in Q_zero_gap:
            summary_data.append({
                "qid": card.qid,
                "subfield": card.signature.get('subfield'),
                "category": "Q0_gap",
                "skill_used": card.skill_used.get('skill_name'),
                "file_used": card.skill_used.get('specific_file'),
                "solving_skill": None,
                "diagnosis": card.diagnosis,
                "action": card.recommended_action
            })

        if summary_data:
            import pandas as pd
            summary_df = pd.DataFrame(summary_data)
            summary_file = output_path / f"residual_summary_epoch{epoch}.csv"
            summary_df.to_csv(summary_file, index=False)
            print(f"✓ Saved residual summary: {summary_file}")


def format_discover_evidence_for_refinement(
    Q_plus_discover: List[UnsolvedCard],
    target_skill_file: str,
    max_cases: int = 5
) -> str:
    """
    Format Q+_discover evidence for skill refinement.

    These are cases where the target skill SHOULD have been triggered
    but wasn't (or was triggered but a different file should have been used).

    Args:
        Q_plus_discover: List of discover cards
        target_skill_file: The skill file that should be improved
        max_cases: Maximum cases to include

    Returns:
        Formatted string for refinement prompt
    """
    # Filter to cases where the solving skill matches target
    # Debug: show what we're filtering
    print(f"    [DEBUG format_discover] target_skill_file: {target_skill_file}")
    print(f"    [DEBUG format_discover] Q_plus_discover has {len(Q_plus_discover)} cards")
    for c in Q_plus_discover[:3]:
        print(f"      - {c.qid}: solving_skill = {c.solving_skill}")

    relevant = [c for c in Q_plus_discover
                if c.solving_skill and target_skill_file in c.solving_skill]

    print(f"    [DEBUG format_discover] After filter: {len(relevant)} relevant cards")

    if not relevant:
        return ""

    formatted = [f"## Q+_discover Evidence (Router/Trigger Mismatches)\n"]
    formatted.append(f"These {len(relevant[:max_cases])} cases should have used `{target_skill_file}` but didn't:\n")

    for i, card in enumerate(relevant[:max_cases], 1):
        formatted.append(f"""
**Case {i}** (QID: {card.qid})

**Question**: {card.question}

**What Was Used**: {card.skill_used.get('skill_name')}/{card.skill_used.get('specific_file')}
- Answer (WRONG): {card.skill_used.get('answer', 'N/A')}

**What Should Have Been Used**: {card.solving_skill}
- Answer (CORRECT): {card.probe_results[-1].answer if card.probe_results else 'N/A'}

**Ground Truth**: {card.ground_truth}

**Diagnosis**: {card.diagnosis_explanation or 'N/A'}

---
""")

    formatted.append("""
**Action Required**: Update trigger keywords and "When to Use" section to capture these cases.
""")

    return "\n".join(formatted)


def format_gap_evidence_for_new_skill(
    Q_zero_gap: List[UnsolvedCard],
    subfield: str,
    max_cases: int = 5
) -> str:
    """
    Format Q0_gap evidence for creating new sub-skill.

    These are cases where NO skill could solve the problem,
    indicating a capability gap.

    Args:
        Q_zero_gap: List of gap cards
        subfield: Filter to specific subfield
        max_cases: Maximum cases to include

    Returns:
        Formatted string for new skill creation
    """
    # Filter to specific subfield
    relevant = [c for c in Q_zero_gap
                if c.signature.get('subfield', '').lower() == subfield.lower()]

    if not relevant:
        return ""

    # Group by diagnosis
    by_diagnosis = defaultdict(list)
    for card in relevant:
        by_diagnosis[card.diagnosis or "unknown"].append(card)

    formatted = [f"## Q0_gap Evidence (Capability Gaps in {subfield})\n"]
    formatted.append(f"Total: {len(relevant)} cases where no skill could help.\n")

    for diagnosis, cards in by_diagnosis.items():
        formatted.append(f"\n### Root Cause: {diagnosis} ({len(cards)} cases)\n")

        for i, card in enumerate(cards[:max_cases], 1):
            formatted.append(f"""
**Case {i}** (QID: {card.qid})

**Question**: {card.question}...

**Ground Truth**: {card.ground_truth}

**Failed Attempt**: {card.skill_used.get('answer', 'N/A')}

**Gap Analysis**: {card.diagnosis_explanation or 'N/A'}

---
""")

    formatted.append("""
**Action Required**: Create new sub-skill or add missing procedures/checks to existing skills.
""")

    return "\n".join(formatted)


# Example usage
if __name__ == "__main__":
    from run_logger import RunLogger, RunLogEntry

    # Create sample run log with unsolved cases
    print("="*60)
    print("Residual Evidence Collector Test")
    print("="*60)

    # Simulate some entries
    class MockEntry:
        def __init__(self, qid, baseline_score, skill_score, subfield):
            self.qid = qid
            self.baseline_score = baseline_score
            self.skill_score = skill_score
            self.signature = {"subfield": subfield}
            self.question = f"Sample question for {subfield}"
            self.context = "Sample context"
            self.ground_truth = "A"
            self.baseline_answer = "B"
            self.baseline_explanation = "Wrong reasoning"
            self.chosen_skill = "generated-from-failures-v1"
            self.specific_skill_file = f"{subfield.upper().replace(' ', '_')}_CONCEPT_CONFUSION.md"
            self.skill_answer = "C"
            self.skill_explanation = "Still wrong"

    # Create test entries
    entries = [
        MockEntry("q1", 0, 0, "portfolio management"),  # Unsolved
        MockEntry("q2", 0, 1, "portfolio management"),  # Fixed (not unsolved)
        MockEntry("q3", 1, 0, "fixed income"),          # Regression (not unsolved)
        MockEntry("q4", 0, 0, "fixed income"),          # Unsolved
        MockEntry("q5", 0, 0, "derivatives"),           # Unsolved
    ]

    # Collect unsolved
    collector = ResidualEvidenceCollector(enable_diagnosis=False)
    unsolved = collector.collect_unsolved(entries)

    print(f"\nExpected 3 unsolved, got {len(unsolved)}")

    for card in unsolved:
        print(f"  - {card.qid}: {card.signature.get('subfield')}")

    print("\n" + "="*60)
    print("Test Complete")
    print("="*60)
