"""
Textual Optimizer - Skill Refinement Engine

Automated LLM-based skill updates using evidence from Q+ (fixes) and Q- (regressions).

Usage:
    optimizer = TextualOptimizer()
    updated_skill, was_updated = optimizer.refine_skill(skill, Q_plus, Q_minus)
"""

import os
import re
import json
from pathlib import Path
from typing import List, Tuple, Optional, Dict
from dataclasses import asdict, dataclass
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
from anthropic import Anthropic

# LangChain for batch processing
try:
    from langchain_anthropic import ChatAnthropic
    from langchain_core.messages import HumanMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

from optimizer_prompts import (
    SKILL_REFINEMENT_PROMPT,
    SAFETY_REFINEMENT_PROMPT,
    SKILL_MD_ROUTING_PROMPT,
    NEW_SKILL_CREATION_PROMPT,
    UPDATE_DESCRIPTION_PROCEDURE_PROMPT,
    UPDATE_EXAMPLE_PROMPT,
    UPDATE_WHEN_TO_USE_PROMPT,
    REFINEMENT_SYSTEM_PROMPT,
    COVERAGE_REFINEMENT_PROMPT,
    DIAGNOSIS_GUIDANCE,
    COVERAGE_SYSTEM_PROMPT
)

# Attribution prompts for deep analysis
from regression_analysis_prompts import (
    build_attribution_prompt,
    ATTRIBUTION_FIX_PROMPT_TEMPLATE,
    ATTRIBUTION_REGRESSION_PROMPT_TEMPLATE
)

# PoT-specific prompts for code-based skills
from optimizer_prompts_pot import (
    SKILL_REFINEMENT_PROMPT_POT,
    SAFETY_REFINEMENT_PROMPT_POT,
    SKILL_MD_ROUTING_PROMPT_POT,
    NEW_SKILL_CREATION_PROMPT_POT,
    PROCEDURE_UPDATE_PROMPT_POT,
    CHECKS_UPDATE_PROMPT_POT,
    COVERAGE_REFINEMENT_PROMPT_POT,
    DIAGNOSIS_GUIDANCE_POT,
    COVERAGE_SYSTEM_PROMPT_POT
)

load_dotenv()

# Import config utilities
try:
    from skill_learning.config import cfg, is_config_loaded
except ImportError:
    from config import cfg, is_config_loaded

# Lazy-loaded refine model, provider, and client
_refine_model_cache = None
_refine_provider_cache = None
_refine_client_cache = None

# Temperature for skill refinement (configurable via .env or config)
REFINE_TEMPERATURE = float(os.getenv('REFINE_TEMPERATURE', '0.3'))

def get_refine_model():
    """Get refine model (lazy initialization from config)."""
    global _refine_model_cache
    if _refine_model_cache is None:
        if is_config_loaded():
            config_val = cfg('models.refine')
            if config_val is not None:
                _refine_model_cache = config_val
                print(f"  [TextualOptimizer] Using refine model from config: {_refine_model_cache}")
            else:
                _refine_model_cache = os.getenv('REFINE_MODEL', 'claude-sonnet-4-5-20250929')
                print(f"  [TextualOptimizer] Using refine model from env/fallback: {_refine_model_cache}")
        else:
            _refine_model_cache = os.getenv('REFINE_MODEL', 'claude-sonnet-4-5-20250929')
    return _refine_model_cache

def get_refine_provider():
    """Get refine provider (lazy initialization from config).

    Returns: 'openrouter', 'anthropic', 'dashscope', or 'auto' (default).
    """
    global _refine_provider_cache
    if _refine_provider_cache is None:
        if is_config_loaded():
            config_val = cfg('models.refine_provider')
            if config_val is not None:
                _refine_provider_cache = config_val
                print(f"  [TextualOptimizer] Using refine provider from config: {_refine_provider_cache}")
            else:
                _refine_provider_cache = os.getenv('REFINE_PROVIDER', 'auto')
        else:
            _refine_provider_cache = os.getenv('REFINE_PROVIDER', 'auto')
    return _refine_provider_cache

def get_refine_client():
    """Get refine client (lazy initialization based on refine model and provider).

    Provider selection:
    1. Explicit provider from config (openrouter, anthropic, dashscope)
    2. Auto-detect from model name when provider is 'auto'
    """
    global _refine_client_cache
    if _refine_client_cache is None:
        refine_model = get_refine_model()
        refine_provider = get_refine_provider()

        # Explicit provider takes precedence
        if refine_provider == 'openrouter':
            openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
            if not openrouter_api_key:
                raise ValueError("OPENROUTER_API_KEY required when refine_provider is 'openrouter'")
            _refine_client_cache = OpenAI(api_key=openrouter_api_key, base_url="https://openrouter.ai/api/v1")
            print(f"  [TextualOptimizer] Refine client: OpenRouter ({refine_model})")
        elif refine_provider == 'anthropic':
            anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
            if not anthropic_api_key:
                raise ValueError("ANTHROPIC_API_KEY required when refine_provider is 'anthropic'")
            anthropic_base_url = os.getenv('ANTHROPIC_API_BASE')
            if anthropic_base_url:
                _refine_client_cache = Anthropic(api_key=anthropic_api_key, base_url=anthropic_base_url)
            else:
                _refine_client_cache = Anthropic(api_key=anthropic_api_key)
            print(f"  [TextualOptimizer] Refine client: Anthropic ({refine_model})")
        elif refine_provider == 'dashscope':
            dashscope_api_key = os.getenv('DASHSCOPE_API_KEY')
            if not dashscope_api_key:
                raise ValueError("DASHSCOPE_API_KEY required when refine_provider is 'dashscope'")
            dashscope_base_url = os.getenv('QWEN_API_BASE', 'https://dashscope.aliyuncs.com/compatible-mode/v1')
            _refine_client_cache = OpenAI(api_key=dashscope_api_key, base_url=dashscope_base_url)
            print(f"  [TextualOptimizer] Refine client: DashScope ({refine_model})")
        else:
            # Auto-detect from model name
            if refine_model.startswith('anthropic/'):
                # OpenRouter model format
                openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
                if not openrouter_api_key:
                    raise ValueError(f"OPENROUTER_API_KEY required for model: {refine_model}")
                _refine_client_cache = OpenAI(api_key=openrouter_api_key, base_url="https://openrouter.ai/api/v1")
                print(f"  [TextualOptimizer] Refine client: OpenRouter (auto-detected)")
            elif refine_model.lower().startswith('claude'):
                # Anthropic client for Claude models
                anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
                if anthropic_api_key:
                    anthropic_base_url = os.getenv('ANTHROPIC_API_BASE')
                    if anthropic_base_url:
                        _refine_client_cache = Anthropic(api_key=anthropic_api_key, base_url=anthropic_base_url)
                    else:
                        _refine_client_cache = Anthropic(api_key=anthropic_api_key)
                    print(f"  [TextualOptimizer] Refine client: Anthropic (auto-detected)")
                else:
                    # Fallback to OpenRouter
                    openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
                    if openrouter_api_key:
                        _refine_client_cache = OpenAI(api_key=openrouter_api_key, base_url="https://openrouter.ai/api/v1")
                        print(f"  [TextualOptimizer] Refine client: OpenRouter (fallback)")
                    else:
                        raise ValueError(f"No API key available for model: {refine_model}")
            elif refine_model.lower().startswith('qwen'):
                # DashScope client for Qwen models
                dashscope_api_key = os.getenv('DASHSCOPE_API_KEY')
                if not dashscope_api_key:
                    raise ValueError(f"DASHSCOPE_API_KEY required for model: {refine_model}")
                dashscope_base_url = os.getenv('QWEN_API_BASE', 'https://dashscope.aliyuncs.com/compatible-mode/v1')
                _refine_client_cache = OpenAI(api_key=dashscope_api_key, base_url=dashscope_base_url)
                print(f"  [TextualOptimizer] Refine client: DashScope (auto-detected)")
            else:
                # Default to Anthropic (legacy behavior)
                anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
                if anthropic_api_key:
                    _refine_client_cache = Anthropic(api_key=anthropic_api_key)
                    print(f"  [TextualOptimizer] Refine client: Anthropic (fallback)")
                else:
                    raise ValueError(f"No API key available for model: {refine_model}")
    return _refine_client_cache

def reset_refine_cache():
    """Reset refine caches. Call this when config changes."""
    global _refine_model_cache, _refine_provider_cache, _refine_client_cache
    _refine_model_cache = None
    _refine_provider_cache = None
    _refine_client_cache = None

def call_refine_llm(messages: list, max_tokens: int = 4096, temperature: float = None, system: str = None):
    """Unified LLM call supporting both Anthropic and OpenAI-compatible clients.

    Args:
        messages: List of message dicts with 'role' and 'content'
        max_tokens: Maximum tokens for response
        temperature: Temperature for sampling (uses REFINE_TEMPERATURE if None)
        system: Optional system message

    Returns:
        Tuple of (response_text, stop_reason)
    """
    refine_client = get_refine_client()
    refine_model = get_refine_model()
    temp = temperature if temperature is not None else REFINE_TEMPERATURE

    if isinstance(refine_client, Anthropic):
        # Anthropic API
        kwargs = {
            "model": refine_model,
            "max_tokens": max_tokens,
            "temperature": temp,
            "messages": messages
        }
        if system:
            kwargs["system"] = system
        response = refine_client.messages.create(**kwargs)
        return response.content[0].text.strip(), response.stop_reason
    else:
        # OpenAI-compatible API (OpenRouter, DashScope)
        openai_messages = []
        if system:
            openai_messages.append({"role": "system", "content": system})
        openai_messages.extend(messages)

        response = refine_client.chat.completions.create(
            model=refine_model,
            max_tokens=max_tokens,
            temperature=temp,
            messages=openai_messages
        )
        finish_reason = response.choices[0].finish_reason
        # Map OpenAI finish_reason to Anthropic-style stop_reason
        stop_reason = "max_tokens" if finish_reason == "length" else finish_reason
        return response.choices[0].message.content.strip(), stop_reason

# For backwards compatibility - these will be set on first use
REFINE_MODEL = None  # Use get_refine_model() instead
client = None  # Use get_refine_client() instead


@dataclass
class SkillRef:
    """Lightweight reference to a skill set directory.

    Replaces the old Skill object. Methods that used skill.name and
    skill.skill_dir can use SkillRef.name and SkillRef.skill_dir instead.

    Attributes:
        skill_dir: Path to the working copy of the skill set
                   (e.g., skill_learning/checkpoints_api/working_skills/)
        name:      Skill set name (e.g., "famma-non-arithmetic-v1")
    """
    skill_dir: Path
    name: str


def _get_refine_max_tokens():
    """Get max_tokens for refinement from config or env."""
    try:
        config_val = cfg('model_params.refine_max_tokens')
        if config_val:
            return int(config_val)
    except:
        pass
    return int(os.getenv('REFINE_MAX_TOKENS', '8192'))


class TextualOptimizer:
    """Refines skills using automated LLM-based refinement."""

    # Default max_tokens for LLM refinement calls.
    # Read from config first, then env, then fallback to 8192.
    DEFAULT_MAX_TOKENS = _get_refine_max_tokens()

    @staticmethod
    def _strip_code_block_wrapper(text: str) -> str:
        """Strip markdown code block wrappers from LLM output.

        Handles both complete (with closing ```) and truncated (no closing ```)
        responses. This is needed because LLMs often wrap output in code blocks
        even when not asked to.
        """
        stripped = text.strip()

        # Try complete code block first: ```markdown\n...\n```
        if "```markdown" in stripped:
            match = re.search(r'```markdown\n(.*?)\n```', stripped, re.DOTALL)
            if match:
                return match.group(1).strip()
            # Truncated: starts with ```markdown but no closing ```
            idx = stripped.find("```markdown")
            return stripped[idx + len("```markdown"):].lstrip('\n').strip()

        # Try ```\n...\n```
        if stripped.startswith("```"):
            match = re.search(r'^```\w*\n(.*?)\n```$', stripped, re.DOTALL)
            if match:
                return match.group(1).strip()
            # Truncated: starts with ``` but no closing ```
            first_newline = stripped.find('\n')
            if first_newline != -1:
                return stripped[first_newline + 1:].strip()

        return stripped

    @staticmethod
    def _has_changes(response: str) -> bool:
        """Check if LLM response contains new or refined patterns (for incremental refinement)."""
        if not response or not response.strip():
            return False
        if "NO_CHANGES" in response or "NO_NEW_PATTERNS" in response:
            return False
        if len(response.strip()) < 50:
            return False
        if ("## REFINED Pattern" in response
                or "## NEW Pattern" in response
                or "## REFINED CONSTRAINTS" in response):
            return True
        return False

    @staticmethod
    def _is_pot_skill(content: str) -> bool:
        """
        Detect if a skill file is PoT (Program-of-Thought) based.

        PoT skills contain CODE CONSTRAINTS section and focus on code templates.

        Args:
            content: Skill file content

        Returns:
            True if PoT skill, False otherwise
        """
        if not content:
            return False
        # Check for CODE CONSTRAINTS section (PoT-specific marker)
        # Covers variations: "## CODE CONSTRAINTS", "CODE CONSTRAINTS (MANDATORY)", "## Critical Code Constraints"
        return ("CODE CONSTRAINTS" in content or
                "Code Constraints" in content or
                "Program of Thought" in content)

    @staticmethod
    def _apply_incremental_changes(content: str, response: str) -> tuple:
        """
        Apply REFINED and NEW patterns from response to content (incremental refinement).

        Returns:
            Tuple of (updated_content, refined_names, new_names)
        """
        refined_names = []
        new_names = []

        # Handle REFINED CONSTRAINTS first (for PoT skills)
        constraints_match = re.search(
            r'## REFINED CONSTRAINTS\s*\n+(.*?)(?=\n## |\Z)',
            response,
            re.DOTALL
        )
        if constraints_match:
            new_constraints = constraints_match.group(1).strip()
            # Replace existing CODE CONSTRAINTS section
            content = re.sub(
                r'(## CODE CONSTRAINTS \(MANDATORY\).*?)(?=\n## |\Z)',
                f"## CODE CONSTRAINTS (MANDATORY)\n\n{new_constraints}",
                content,
                count=1,
                flags=re.DOTALL
            )
            refined_names.append("CODE CONSTRAINTS")

        # SAFETY CHECK: Reject if LLM output contains regular ## Pattern: headers
        # (without REFINED/NEW markers) - these would be incorrectly lost
        regular_pattern_count = len(re.findall(r'^## Pattern:', response, re.MULTILINE))
        refined_new_count = len(re.findall(r'^## (?:REFINED|NEW) Pattern:', response, re.MULTILINE))
        if regular_pattern_count > 0:
            print(f"  ❌ REJECTED: LLM output has {regular_pattern_count} unmarked '## Pattern:' headers "
                  f"(only {refined_new_count} REFINED/NEW markers).")
            print(f"     LLM didn't follow incremental format. Returning original content unchanged.")
            return content, [], []

        # Parse REFINED and NEW patterns
        sections = re.split(r'(## (?:REFINED|NEW) Pattern:\s*.+)', response)

        i = 1
        while i < len(sections):
            header = sections[i].strip()
            body = sections[i + 1].strip() if i + 1 < len(sections) else ""
            i += 2

            if not body:
                continue

            if header.startswith('## REFINED Pattern:'):
                pattern_name = header.replace('## REFINED Pattern:', '').strip()
                replacement = f"## Pattern: {pattern_name}\n\n{body}"

                # Find and replace matching pattern
                pattern_regex = re.compile(
                    rf'## Pattern(?:\s+\d+)?:\s*{re.escape(pattern_name)}.*?(?=\n## |\Z)',
                    re.DOTALL
                )
                if pattern_regex.search(content):
                    # Use lambda to avoid interpreting backslashes in replacement text
                    content = pattern_regex.sub(lambda m: replacement, content, count=1)
                    refined_names.append(pattern_name)
                else:
                    # Pattern not found, append as new
                    content = content.rstrip() + "\n\n" + replacement
                    new_names.append(pattern_name)

            elif header.startswith('## NEW Pattern:'):
                pattern_name = header.replace('## NEW Pattern:', '').strip()
                new_pattern = f"## Pattern: {pattern_name}\n\n{body}"
                content = content.rstrip() + "\n\n" + new_pattern
                new_names.append(pattern_name)

        return content, refined_names, new_names

    def __init__(
        self,
        max_skill_lines: int = None,
        checkpoint_dir: Optional[Path] = None
    ):
        """
        Initialize textual optimizer.

        Args:
            max_skill_lines: Maximum lines for refined skill
            checkpoint_dir: Directory to save evidence JSON
        """
        if max_skill_lines is None:
            max_skill_lines = int(os.getenv('MAX_SKILL_LINES', '500'))
        self.max_skill_lines = max_skill_lines
        self.checkpoint_dir = Path(checkpoint_dir) if checkpoint_dir else None

    def refine_skill(
        self,
        skill: 'SkillRef',  # SkillRef (or legacy Skill object with .name and .skill_dir)
        Q_plus: List,  # Positive evidence cards
        Q_minus: List,  # Negative evidence cards
        epoch: int = 0,
        specific_skill_file: Optional[str] = None  # Relative path: "portfolio_management/concept_confusion.md"
    ) -> Tuple[Optional[str], bool]:
        """
        Refine a skill file based on Q+/Q- evidence using automated LLM refinement.

        Args:
            skill: SkillRef with skill_dir and name
            Q_plus: Positive evidence (fixes)
            Q_minus: Negative evidence (regressions)
            epoch: Current epoch number
            specific_skill_file: Relative path to skill file within skill_dir

        Returns:
            Tuple of (updated_skill_content, was_updated)
        """
        return self._refine_api(skill, Q_plus, Q_minus, specific_skill_file, epoch, self.checkpoint_dir)

    def refine_skill_safety(
        self,
        skill: 'SkillRef',
        Q_plus: List,  # Constraints - DO NOT BREAK
        Q_minus: List,  # Regressions to FIX
        epoch: int = 0,
        specific_skill_file: Optional[str] = None
    ) -> Tuple[Optional[str], bool]:
        """
        V2 Safety Phase: Refine skill with Q+ as constraints and Q- as cases to fix.

        Uses SAFETY_REFINEMENT_PROMPT which frames Q+ as constraints to preserve
        and Q- as regressions to fix.

        Args:
            skill: SkillRef with skill_dir and name
            Q_plus: Positive evidence (constraints - must preserve)
            Q_minus: Negative evidence (regressions to fix)
            epoch: Current epoch number
            specific_skill_file: Relative path to skill file

        Returns:
            Tuple of (updated_skill_content, was_updated)
        """
        return self._refine_safety_api(skill, Q_plus, Q_minus, specific_skill_file, epoch, self.checkpoint_dir)

    def _refine_safety_api(
        self,
        skill: 'SkillRef',
        Q_plus: List,
        Q_minus: List,
        specific_skill_file: Optional[str] = None,
        epoch: int = 0,
        checkpoint_dir: Optional[Path] = None
    ) -> Tuple[Optional[str], bool]:
        """
        Safety refinement using SAFETY_REFINEMENT_PROMPT.

        Key difference from standard refinement:
        - Q+ is framed as CONSTRAINTS (must preserve)
        - Q- is framed as cases TO FIX
        - Safety-first approach: prefer NO_CHANGES if Q- fix risks Q+ breakage
        """
        skill_display_name = f"{skill.name}/{specific_skill_file}" if specific_skill_file else skill.name
        print(f"\n[Safety Mode] Refining skill: {skill_display_name}")
        print(f"  Constraints (Q+): {len(Q_plus)}, To fix (Q-): {len(Q_minus)}")

        # Load the specific skill file content
        if specific_skill_file:
            skill_file_path = skill.skill_dir / specific_skill_file
        else:
            skill_file_path = skill.skill_dir / "SKILL.md"

        current_skill_content = ""
        if skill_file_path.exists():
            with open(skill_file_path, 'r', encoding="utf-8") as f:
                current_skill_content = f.read()
        else:
            print(f"  Skill file not found: {skill_file_path}")
            return None, False

        # Format evidence for prompt
        self._current_skill_dir = skill.skill_dir
        evidence_max_cases = int(os.getenv('EVIDENCE_FORMAT_MAX_CASES', '6'))
        positive_evidence = self._format_evidence(Q_plus, max_cases=evidence_max_cases)
        negative_evidence = self._format_evidence(Q_minus, max_cases=evidence_max_cases)

        # Save evidence JSON
        if checkpoint_dir:
            evidence_folder = checkpoint_dir / f"epoch_{epoch}" / "evidence"
            evidence_folder.mkdir(parents=True, exist_ok=True)

            if specific_skill_file:
                file_basename = specific_skill_file.replace('.md', '').replace('/', '_')
                evidence_filename = f"{file_basename}_safety_evidence.json"
            else:
                evidence_filename = f"{skill.name}_safety_evidence.json"

            evidence_json = {
                "skill_set": skill.name,
                "specific_skill_file": specific_skill_file,
                "epoch": epoch,
                "mode": "safety",
                "Q_plus_constraints": [asdict(card) if hasattr(card, '__dataclass_fields__') else str(card) for card in Q_plus],
                "Q_minus_to_fix": [asdict(card) if hasattr(card, '__dataclass_fields__') else str(card) for card in Q_minus]
            }

            evidence_json_path = evidence_folder / evidence_filename
            with open(evidence_json_path, 'w', encoding="utf-8") as f:
                json.dump(evidence_json, f, indent=2, default=str)

            print(f"  Saved safety evidence to: {evidence_json_path}")

        # Detect if this is a PoT skill and select appropriate prompt
        is_pot = self._is_pot_skill(current_skill_content)
        prompt_template = SAFETY_REFINEMENT_PROMPT_POT if is_pot else SAFETY_REFINEMENT_PROMPT

        if is_pot:
            print(f"  Detected PoT skill - using code-based safety prompts")

        # Build prompt
        prompt = prompt_template.format(
            current_skill=current_skill_content,
            skill_file=specific_skill_file or "SKILL.md",
            skill_set_name=skill.name,
            num_positive=len(Q_plus),
            positive_evidence=positive_evidence,
            num_negative=len(Q_minus),
            negative_evidence=negative_evidence
        )

        try:
            refine_model = get_refine_model()
            print(f"  Calling LLM for safety refinement (model: {refine_model})...")
            llm_response, stop_reason = call_refine_llm(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.DEFAULT_MAX_TOKENS,
                system="You are an expert skill refinement assistant. Fix regressions while preserving what already works."
            )

            # Check for truncation
            if stop_reason == "max_tokens":
                print(f"  ⚠️  WARNING: Response truncated by max_tokens ({self.DEFAULT_MAX_TOKENS})")

            # Strip code block wrappers
            llm_response = self._strip_code_block_wrapper(llm_response)

            # Check if there are any changes
            if not self._has_changes(llm_response):
                print(f"  No changes needed (safety constraint: cannot fix Q- without risking Q+)")
                return None, False

            # Apply incremental changes
            updated_content, refined_names, new_names = self._apply_incremental_changes(
                current_skill_content,
                llm_response
            )

            # Format output message
            n_refined = len(refined_names)
            n_new = len(new_names)
            line_count = len(updated_content.split('\n'))

            if n_refined > 0 or n_new > 0:
                print(f"  Safety refinement complete ({line_count} lines):")
                if n_refined > 0:
                    print(f"    - Refined ({n_refined}): {', '.join(refined_names)}")
                if n_new > 0:
                    print(f"    - New ({n_new}): {', '.join(new_names)}")
            else:
                print(f"  No patterns changed ({line_count} lines)")

            return updated_content, True

        except Exception as e:
            print(f"  Error in safety refinement: {e}")
            return None, False

    def _refine_api(
        self,
        skill: 'SkillRef',
        Q_plus: List,
        Q_minus: List,
        specific_skill_file: Optional[str] = None,
        epoch: int = 0,
        checkpoint_dir: Optional[Path] = None
    ) -> Tuple[Optional[str], bool]:
        """
        Refine skill file using LLM API (automated).

        Args:
            skill: SkillRef with skill_dir and name
            Q_plus: Positive evidence
            Q_minus: Negative evidence
            specific_skill_file: Relative path to skill file (e.g., "portfolio_management/concept_confusion.md")
            epoch: Current epoch number
            checkpoint_dir: Directory to save evidence JSON

        Returns:
            Tuple of (updated_content, was_updated)
        """
        skill_display_name = f"{skill.name}/{specific_skill_file}" if specific_skill_file else skill.name
        print(f"\n[API Mode] Refining skill: {skill_display_name}")
        print(f"  Evidence: {len(Q_plus)} positive, {len(Q_minus)} negative")

        # Load the specific skill file content
        if specific_skill_file:
            skill_file_path = skill.skill_dir / specific_skill_file
        else:
            skill_file_path = skill.skill_dir / "SKILL.md"

        current_skill_content = ""
        if skill_file_path.exists():
            with open(skill_file_path, 'r', encoding="utf-8") as f:
                current_skill_content = f.read()
        else:
            print(f"  Skill file not found: {skill_file_path}")
            return None, False

        # Format evidence for prompt (triggers lazy deep analysis / attribution)
        # Store skill_dir for attribution prompt (used by _generate_deep_analysis_for_card)
        self._current_skill_dir = skill.skill_dir
        evidence_max_cases = int(os.getenv('EVIDENCE_FORMAT_MAX_CASES', '6'))
        positive_evidence = self._format_evidence(Q_plus, max_cases=evidence_max_cases)
        negative_evidence = self._format_evidence(Q_minus, max_cases=evidence_max_cases)

        # Save evidence JSON AFTER formatting (so deep analysis is included)
        if checkpoint_dir:
            evidence_folder = checkpoint_dir / f"epoch_{epoch}" / "evidence"
            evidence_folder.mkdir(parents=True, exist_ok=True)

            if specific_skill_file:
                file_basename = specific_skill_file.replace('.md', '').replace('/', '_')
                evidence_filename = f"{file_basename}_evidence.json"
            else:
                evidence_filename = f"{skill.name}_evidence.json"

            evidence_json = {
                "skill_set": skill.name,
                "specific_skill_file": specific_skill_file,
                "epoch": epoch,
                "Q_plus": [asdict(card) for card in Q_plus],
                "Q_minus": [asdict(card) for card in Q_minus]
            }

            evidence_json_path = evidence_folder / evidence_filename
            with open(evidence_json_path, 'w', encoding="utf-8") as f:
                json.dump(evidence_json, f, indent=2)

            print(f"  Saved evidence to: {evidence_json_path}")

        # Detect if this is a PoT skill and select appropriate prompt
        is_pot = self._is_pot_skill(current_skill_content)
        prompt_template = SKILL_REFINEMENT_PROMPT_POT if is_pot else SKILL_REFINEMENT_PROMPT

        if is_pot:
            print(f"  Detected PoT skill - using code-based refinement prompts")

        # Build prompt with new format
        prompt = prompt_template.format(
            current_skill=current_skill_content,
            skill_file=specific_skill_file or "SKILL.md",
            skill_set_name=skill.name,
            num_positive=len(Q_plus),
            positive_evidence=positive_evidence,
            num_negative=len(Q_minus),
            negative_evidence=negative_evidence
        )

        try:
            refine_model = get_refine_model()
            print(f"  Calling LLM for refinement (model: {refine_model}, temperature: {REFINE_TEMPERATURE})...")
            llm_response, stop_reason = call_refine_llm(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.DEFAULT_MAX_TOKENS,
                system="You are an expert skill refinement assistant. Generate improved skill patterns based on evidence."
            )

            # Check for truncation
            if stop_reason == "max_tokens":
                print(f"  ⚠️  WARNING: Response truncated by max_tokens ({self.DEFAULT_MAX_TOKENS}). Output may be incomplete.")

            # Strip code block wrappers (handles both complete and truncated responses)
            llm_response = self._strip_code_block_wrapper(llm_response)

            # Check if there are any changes
            if not self._has_changes(llm_response):
                print(f"  No changes needed (current skill is already effective)")
                return None, False

            # Apply incremental changes to current skill
            updated_content, refined_names, new_names = self._apply_incremental_changes(
                current_skill_content,
                llm_response
            )

            # Check length (warning only, no truncation)
            line_count = len(updated_content.split('\n'))
            if line_count > self.max_skill_lines:
                print(f"  ⚠️  WARNING: Skill is long ({line_count} lines, threshold: {self.max_skill_lines})")

            # Format output message with pattern names
            n_refined = len(refined_names)
            n_new = len(new_names)

            if n_refined > 0 or n_new > 0:
                print(f"  Skill refined successfully ({line_count} lines):")
                if n_refined > 0:
                    print(f"    - Refined ({n_refined}): {', '.join(refined_names)}")
                if n_new > 0:
                    print(f"    - New ({n_new}): {', '.join(new_names)}")
            else:
                print(f"  No patterns changed ({line_count} lines)")

            return updated_content, True

        except Exception as e:
            print(f"  Error refining skill: {e}")
            return None, False


    def _generate_deep_analysis_for_card(self, card) -> str:
        """
        Generate attribution + deep analysis for an evidence card (lazy analysis).

        When deep analysis is enabled, uses the new attribution prompt which:
        1. Attributes the fix/regression to specific skill file(s)
        2. Analyzes why the skill helped/hurt

        The result is stored in card.attribution_result and card.what_went_right_or_wrong.

        Args:
            card: EvidenceCard

        Returns:
            Deep analysis string
        """
        # Check if already generated
        if getattr(card, '_deep_analysis_generated', False):
            return card.what_went_right_or_wrong

        # Check if deep analysis is enabled
        enable_deep = os.getenv('ENABLE_DEEP_ANALYSIS', 'true').lower() == 'true'
        if not enable_deep:
            return card.what_went_right_or_wrong

        # Get loaded files from card
        loaded_files = card.loaded_files or []
        if not loaded_files and card.specific_skill_file:
            loaded_files = [card.specific_skill_file]

        # Load skill files content from skill_dir
        skill_files_content = {}
        skill_dir = getattr(self, '_current_skill_dir', None)
        if skill_dir and loaded_files:
            for file_path in loaded_files:
                full_path = Path(skill_dir) / file_path
                if full_path.exists():
                    try:
                        with open(full_path, 'r', encoding="utf-8") as f:
                            skill_files_content[file_path] = f.read()
                    except Exception:
                        skill_files_content[file_path] = "(Error reading file)"

        # Determine if this is a fix or regression
        is_fix = getattr(card, 'is_fix', False)

        # Get execution status and explanation for the prompt
        # For PoT mode: use skill_code and execution_success
        # For non-PoT mode: use skill_explanation
        skill_code = card.skill_code or None
        execution_success = card.skill_k.get('execution_success', None)
        skill_explanation = card.skill_k.get('explanation', None)

        # Build attribution prompt (handles both PoT and non-PoT modes)
        attribution_prompt = build_attribution_prompt(
            question=card.question,
            ground_truth=card.ground_truth,
            baseline_answer=card.baseline.get('answer', 'N/A'),
            skill_answer=card.skill_k.get('answer', 'N/A'),
            loaded_files=loaded_files,
            skill_files_content=skill_files_content,
            is_fix=is_fix,
            context=card.context,
            options=card.options,
            # PoT mode parameters
            skill_code=skill_code,
            execution_success=execution_success,
            # Non-PoT mode parameters
            skill_explanation=skill_explanation
        )

        try:
            response, _ = call_refine_llm(
                messages=[{"role": "user", "content": attribution_prompt}],
                max_tokens=500,
                temperature=0.0
            )

            # Parse JSON response
            attribution_result = self._parse_attribution_response(response)

            # Store attribution result in card
            card.attribution_result = attribution_result

            # Extract analysis for display
            analysis = attribution_result.get('analysis', response)

            # Add prefix based on outcome
            if is_fix:
                prefix = "✅ FIX: "
            elif getattr(card, 'is_regress', False):
                prefix = "❌ REGRESSION: "
            else:
                prefix = ""

            result = prefix + analysis

            # Update card (mark as generated)
            card.what_went_right_or_wrong = result
            card._deep_analysis_generated = True

            return result

        except Exception as e:
            # Return existing simple analysis on error
            print(f"  ⚠️  Attribution analysis failed for {card.qid}: {e}")
            return card.what_went_right_or_wrong

    def _parse_attribution_response(self, response: str) -> dict:
        """Parse the JSON response from attribution prompt.

        Args:
            response: LLM response string (may contain JSON)

        Returns:
            Parsed attribution result dict
        """
        # Try to extract JSON from response
        try:
            # Look for JSON block in response
            json_match = re.search(r'\{[^{}]*"attributed_files"[^{}]*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())

            # Try parsing entire response as JSON
            return json.loads(response)
        except (json.JSONDecodeError, AttributeError):
            # If JSON parsing fails, return response as analysis
            return {
                'attributed_files': [],
                'analysis': response
            }

    def _generate_deep_analysis_batch(self, cards: List) -> None:
        """
        Generate deep analysis for multiple cards using LangChain batch processing.

        Updates cards in-place with deep analysis results.

        Args:
            cards: List of EvidenceCard objects
        """
        # Check if deep analysis is enabled
        enable_deep = os.getenv('ENABLE_DEEP_ANALYSIS', 'true').lower() == 'true'
        if not enable_deep:
            return

        # Filter cards that need analysis
        cards_needing_analysis = [
            card for card in cards
            if not getattr(card, '_deep_analysis_generated', False)
        ]

        if not cards_needing_analysis:
            return

        # Get batch size from environment
        batch_size = int(os.getenv('ANALYSIS_BATCH_SIZE', '10'))

        # Use LangChain if available
        if LANGCHAIN_AVAILABLE and batch_size > 0:
            self._generate_deep_analysis_batch_langchain(cards_needing_analysis, batch_size)
        else:
            # Fallback to sequential
            for card in cards_needing_analysis:
                self._generate_deep_analysis_for_card(card)

    def _generate_deep_analysis_batch_langchain(self, cards: List, batch_size: int) -> None:
        """
        Use LangChain's batch() for concurrent deep analysis.

        Args:
            cards: List of EvidenceCard objects needing analysis
            batch_size: Max concurrent requests
        """
        print(f"  Generating deep analysis for {len(cards)} cards (batch_size={batch_size})...")

        refine_model = get_refine_model()
        refine_provider = get_refine_provider()

        # Initialize LangChain client based on provider
        if refine_provider == 'openrouter' or refine_model.startswith('anthropic/'):
            # OpenRouter: use ChatOpenAI with OpenRouter credentials
            try:
                from langchain_openai import ChatOpenAI as LangChainOpenAI
            except ImportError:
                print(f"  ⚠️  langchain-openai not available, falling back to sequential")
                for card in cards:
                    self._generate_deep_analysis_for_card(card)
                return

            api_key = os.getenv('OPENROUTER_API_KEY')
            if not api_key:
                print(f"  ⚠️  OPENROUTER_API_KEY not set, falling back to sequential")
                for card in cards:
                    self._generate_deep_analysis_for_card(card)
                return
            llm = LangChainOpenAI(
                model=refine_model,
                api_key=api_key,
                base_url="https://openrouter.ai/api/v1",
                max_tokens=200,
                temperature=0.0
            )
        elif refine_provider == 'anthropic' or (refine_provider == 'auto' and refine_model.lower().startswith('claude')):
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if not api_key:
                print(f"  ⚠️  ANTHROPIC_API_KEY not set, falling back to sequential")
                for card in cards:
                    self._generate_deep_analysis_for_card(card)
                return
            llm = ChatAnthropic(
                model=refine_model,
                api_key=api_key,
                max_tokens=200,
                temperature=0.0
            )
        else:
            # DashScope/other providers - fall back to sequential
            print(f"  ⚠️  Provider '{refine_provider}' doesn't support batch, falling back to sequential")
            for card in cards:
                self._generate_deep_analysis_for_card(card)
            return

        # Build prompts for all cards
        prompts = []
        for card in cards:
            prompt = self._build_deep_analysis_prompt(card)
            prompts.append([HumanMessage(content=prompt)])

        try:
            # Execute batch
            responses = llm.batch(
                prompts,
                config={"max_concurrency": batch_size}
            )

            # Process results
            for card, response in zip(cards, responses):
                if response:
                    analysis = response.content.strip()

                    # Add prefix based on outcome
                    if getattr(card, 'is_fix', False):
                        prefix = "✅ FIX: "
                    elif getattr(card, 'is_regress', False):
                        prefix = "❌ REGRESSION: "
                    else:
                        prefix = ""

                    card.what_went_right_or_wrong = prefix + analysis
                    card._deep_analysis_generated = True

            print(f"  Deep analysis batch complete")

        except Exception as e:
            print(f"  ⚠️  Batch analysis failed: {e}, falling back to sequential")
            for card in cards:
                self._generate_deep_analysis_for_card(card)

    def _build_deep_analysis_prompt(self, card) -> str:
        """Build deep analysis prompt for a single card."""
        # Extract skill loading context
        tool_call_sequence = card.tool_call_sequence or []
        skills_loaded = ""
        if tool_call_sequence:
            items = [f"- {t['file']}: {t.get('reason', 'N/A')}" for t in tool_call_sequence if not t.get('is_duplicate')]
            if items:
                skills_loaded = "\n**Skills Loaded**:\n" + "\n".join(items) + "\n"

        baseline_explanation = card.baseline.get('explanation', 'N/A')
        skill_explanation = card.skill_k.get('explanation', 'N/A')

        # Include code sections if available (PoT mode)
        baseline_code_section = ""
        if card.baseline_code:
            baseline_code_section = f"\nGenerated Code:\n```python\n{card.baseline_code}\n```\n"

        skill_code_section = ""
        if card.skill_code:
            skill_code_section = f"\nGenerated Code:\n```python\n{card.skill_code}\n```\n"

        # Update analysis instructions based on whether code is present
        analysis_instructions = """Provide a concise analysis (1-2 sentences) explaining:
1. If the skill helped: WHY did it help? What concept/reasoning did it add?
2. If the skill hurt: WHAT went wrong? What mistake did it introduce?
3. What specific knowledge or pattern made the difference?"""

        if card.baseline_code or card.skill_code:
            analysis_instructions = """Provide a concise analysis (1-2 sentences) explaining:
1. If the skill helped: WHY did it help? What concept/reasoning or CODE PATTERN did it add?
2. If the skill hurt: WHAT went wrong? What mistake in REASONING or CODE did it introduce?
3. What specific knowledge, calculation pattern, or code implementation made the difference?
4. If code is present: Did the skill fix/introduce bugs, improve calculation accuracy, or change the algorithm?"""

        options_section = ""
        if card.options:
            options_section = f"**Options**: {card.options}\n"

        return f"""Analyze the impact of adding a skill to the model's reasoning.

**Question**: {card.question}
**Context**: {card.context if card.context else 'None'}
{options_section}
**Ground Truth**: {card.ground_truth}
{skills_loaded}
**Baseline Reasoning** (score: {card.baseline.get('score', 0)}):
Answer: {card.baseline.get('answer', 'N/A')}
Explanation: {baseline_explanation}{baseline_code_section}

**With Skill** (score: {card.skill_k.get('score', 0)}):
Answer: {card.skill_k.get('answer', 'N/A')}
Explanation: {skill_explanation}{skill_code_section}

{analysis_instructions}

Analysis:"""

    def _format_evidence(self, evidence_cards: List, max_cases: int = 6) -> str:
        """
        Format evidence cards for LLM prompt.

        Includes FULL question, context, ground truth, and explanations
        so the refinement model can understand WHY the skill helped/hurt.

        Uses batch processing for deep analysis when multiple cards need analysis.
        """
        if not evidence_cards:
            return "None"

        cards_to_format = evidence_cards[:max_cases]

        # Batch generate deep analysis for all cards that need it
        self._generate_deep_analysis_batch(cards_to_format)

        formatted = []
        for i, card in enumerate(cards_to_format, 1):
            # Deep analysis already generated by batch call
            deep_analysis = card.what_went_right_or_wrong
            # Format baseline explanation
            baseline_explanation = card.baseline.get('explanation', 'N/A')

            # Format skill explanation
            skill_explanation = card.skill_k.get('explanation', 'N/A')

            # Format options if available
            options_section = ""
            if card.options:
                options_section = f"\n**Options**: {card.options}\n"

            # Format PoT code sections if available
            baseline_code_section = ""
            if card.baseline_code:
                baseline_code_section = f"\n- Generated Code:\n```python\n{card.baseline_code}\n```\n"

            skill_code_section = ""
            if card.skill_code:
                skill_code_section = f"\n- Generated Code:\n```python\n{card.skill_code}\n```\n"

            formatted.append(f"""
**Case {i}** (QID: {card.qid})

**Question (FULL)**: {card.question}

**Context**: {card.context if card.context else 'None'}
{options_section}
**Ground Truth**: {card.ground_truth}

**Baseline Performance** (score: {card.baseline.get('score', 0)}):
- Answer: {card.baseline.get('answer', 'N/A')}
- Reasoning: {baseline_explanation}{baseline_code_section}

**With Skill** (score: {card.skill_k.get('score', 0)}):
- Answer: {card.skill_k.get('answer', 'N/A')}
- Reasoning: {skill_explanation}{skill_code_section}

**Delta**: {card.delta}

**Deep Analysis**: {deep_analysis}

**Domain**: {card.signature.get('subfield', 'N/A')}

---
""")

        return "\n".join(formatted)

    def _create_evidence_report(
        self,
        skill,
        Q_plus: List,
        Q_minus: List,
        epoch: int,
        specific_skill_file: Optional[str] = None
    ) -> str:
        """Create human-readable evidence report."""
        skill_title = f"{skill.name}/{specific_skill_file}" if specific_skill_file else skill.name
        report = f"""# Evidence Report: {skill_title}

**Epoch**: {epoch}
**Specific Skill File**: {specific_skill_file or "SKILL.md"}
**Generated**: {datetime.now().isoformat()}

## Summary

- **Positive Cases (Q+)**: {len(Q_plus)} - Skill fixed these baseline failures
- **Negative Cases (Q-)**: {len(Q_minus)} - Skill caused these regressions

## Positive Evidence (Q+) - What the Skill Does Well

"""
        if Q_plus:
            for i, card in enumerate(Q_plus, 1):
                specific_file_info = f"\n**Specific Skill Used**: {card.specific_skill_file}\n" if card.specific_skill_file else ""
                options_info = f"\n**Options**: {card.options}\n" if card.options else ""
                report += f"""
### Q+ Case {i}: {card.qid}

**Question**: {card.question}

**Context**: {card.context}
{options_info}
**Ground Truth**: {card.ground_truth}
{specific_file_info}
**Baseline Performance**:
- Answer: {card.baseline.get('answer', 'N/A')}
- Explanation: {card.baseline.get('explanation', 'N/A')}
- Score: {card.baseline.get('score', 0)}

**With Skill**:
- Answer: {card.skill_k.get('answer', 'N/A')}
- Explanation: {card.skill_k.get('explanation', 'N/A')}
- Score: {card.skill_k.get('score', 0)}

**Delta**: {card.delta}

**Analysis**: {card.what_went_right_or_wrong}

**Signature**:
```json
{json.dumps(card.signature, indent=2)}
```

---
"""
        else:
            report += "\nNo positive cases found.\n"

        report += f"""
## Negative Evidence (Q-) - What Causes Regressions

"""
        if Q_minus:
            for i, card in enumerate(Q_minus, 1):
                specific_file_info = f"\n**Specific Skill Used**: {card.specific_skill_file}\n" if card.specific_skill_file else ""
                options_info = f"\n**Options**: {card.options}\n" if card.options else ""
                report += f"""
### Q- Case {i}: {card.qid}

**Question**: {card.question}

**Context**: {card.context}
{options_info}
**Ground Truth**: {card.ground_truth}
{specific_file_info}
**Baseline Performance**:
- Answer: {card.baseline.get('answer', 'N/A')}
- Explanation: {card.baseline.get('explanation', 'N/A')}
- Score: {card.baseline.get('score', 0)} ✅ **CORRECT**

**With Skill**:
- Answer: {card.skill_k.get('answer', 'N/A')}
- Explanation: {card.skill_k.get('explanation', 'N/A')}
- Score: {card.skill_k.get('score', 0)} ❌ **WRONG**

**Delta**: {card.delta}

**Analysis**: {card.what_went_right_or_wrong}

**Signature**:
```json
{json.dumps(card.signature, indent=2)}
```

**⚠️ IMPORTANT**: This is a regression. The skill broke a correct baseline answer.

---
"""
        else:
            report += "\nNo negative cases found.\n"

        return report

    # ========================================================================
    # NEW METHODS FOR RESIDUAL EVIDENCE (Q+_discover and Q0_gap)
    # ========================================================================

    def _format_discover_evidence(self, cards: List, max_cases: int = None) -> str:
        """Format Q+_discover evidence for trigger refinement prompt."""
        if max_cases is None:
            max_cases = int(os.getenv('DISCOVER_EVIDENCE_MAX_CASES', '5'))
        if not cards:
            return "None"

        formatted = []
        for i, card in enumerate(cards[:max_cases], 1):
            question_text = card.question[:2048] + "..." if len(card.question) > 2048 else card.question
            # Build options section if available
            options_section = f"\n**Options**: {card.options}\n" if getattr(card, 'options', None) else ""
            formatted.append(f"""
**Case {i}** (QID: {card.qid})

**Question**: {question_text}
{options_section}
**Subfield**: {card.signature.get('subfield', 'unknown')}

**What Was Used Instead**: {card.skill_used.get('skill_name')}/{card.skill_used.get('specific_file')}
- Answer (WRONG): {card.skill_used.get('answer', 'N/A')}

**This Skill Could Solve It**: {card.solving_skill}

**Ground Truth**: {card.ground_truth}

**Diagnosis**: {card.diagnosis_explanation or 'N/A'}

---
""")
        return "\n".join(formatted)

    def _format_gap_evidence(self, cards: List, max_cases: int = None) -> str:
        """Format Q0_gap evidence for new skill creation prompt."""
        if max_cases is None:
            max_cases = int(os.getenv('GAP_EVIDENCE_MAX_CASES', '5'))
        if not cards:
            return "None"

        formatted = []
        for i, card in enumerate(cards[:max_cases], 1):
            question_text = card.question[:2048] + "..." if len(card.question) > 2048 else card.question
            context_text = card.context[:2048] + "..." if card.context and len(card.context) > 2048 else (card.context or 'None')
            # Build options section if available
            options_section = f"\n**Options**: {card.options}\n" if getattr(card, 'options', None) else ""
            formatted.append(f"""
**Case {i}** (QID: {card.qid})

**Question**: {question_text}
{options_section}
**Context**: {context_text}

**Ground Truth**: {card.ground_truth}

**Subfield**: {card.signature.get('subfield', 'unknown')}

**Skill Attempted**: {card.skill_used.get('skill_name')}/{card.skill_used.get('specific_file')}
- Answer (WRONG): {card.skill_used.get('answer', 'N/A')}

**Root Cause**: {card.diagnosis}
**Analysis**: {card.diagnosis_explanation or 'N/A'}

---
""")
        return "\n".join(formatted)

    def update_skill_md_routing(
        self,
        skill: 'SkillRef',
        trigger_evidence: str,
        num_cases: int,
        epoch: int
    ) -> Tuple[Optional[str], bool]:
        """
        Update SKILL.md to improve routing for Q+_discover cases.

        These are cases where the WRONG skill file was selected, but another
        file in the skill set could solve it. We update SKILL.md's file reference
        table with better keywords so the router selects correctly.

        Args:
            skill: SkillRef with skill_dir and name
            trigger_evidence: Formatted evidence from Q+_discover cases
            num_cases: Number of evidence cases
            epoch: Current epoch number

        Returns:
            Tuple of (updated_skill_md_content, was_updated)
        """
        skill_md_path = skill.skill_dir / "SKILL.md"
        if not skill_md_path.exists():
            print(f"  SKILL.md not found: {skill_md_path}")
            return None, False

        with open(skill_md_path, 'r', encoding="utf-8") as f:
            current_skill_md = f.read()

        # Detect if this is a PoT skill and select appropriate prompt
        is_pot = self._is_pot_skill(current_skill_md)
        prompt_template = SKILL_MD_ROUTING_PROMPT_POT if is_pot else SKILL_MD_ROUTING_PROMPT

        prompt = prompt_template.format(
            skill_md_content=current_skill_md,
            num_cases=num_cases,
            discover_evidence=trigger_evidence
        )

        return self._call_llm_refine(prompt, skill, epoch, current_skill_md)

    def create_new_subskill(
        self,
        skill: 'SkillRef',
        gap_evidence: str,
        subfield: str,
        diagnosis_summary: str = "",
        epoch: int = 0
    ) -> Tuple[Optional[str], bool]:
        """
        Create a new skill file based on Q0_gap evidence.

        These are cases where NO existing skill could solve the problem.
        Creates a file in the appropriate subfield folder using pattern format.

        Args:
            skill: SkillRef with skill_dir and name
            gap_evidence: Formatted evidence from Q0_gap cases
            subfield: Subfield for the new skill (e.g., "portfolio management")
            diagnosis_summary: Summary of root cause diagnoses
            epoch: Current epoch number

        Returns:
            Tuple of (new_skill_content, was_created)
        """
        # Determine target folder name
        subfield_folder = re.sub(r'[^a-z0-9_\s]', '', subfield.lower().strip())
        subfield_folder = re.sub(r'\s+', '_', subfield_folder)

        # Propose a filename based on common diagnosis
        proposed_filename = "new_patterns"

        num_cases = gap_evidence.count("**Case ")

        # Detect if this is a PoT skill set by checking SKILL.md
        is_pot = False
        skill_md_path = skill.skill_dir / "SKILL.md"
        if skill_md_path.exists():
            with open(skill_md_path, 'r', encoding="utf-8") as f:
                skill_md_content = f.read()
            is_pot = self._is_pot_skill(skill_md_content)

        prompt_template = NEW_SKILL_CREATION_PROMPT_POT if is_pot else NEW_SKILL_CREATION_PROMPT

        prompt = prompt_template.format(
            skill_set_name=skill.name,
            subfield=subfield,
            subfield_folder=subfield_folder,
            proposed_filename=proposed_filename,
            num_cases=num_cases,
            gap_evidence=gap_evidence,
            diagnosis_summary=diagnosis_summary or "Multiple capability gaps identified"
        )

        return self._call_llm_create(prompt, skill, epoch)

    def update_description_procedure(
        self,
        skill: 'SkillRef',
        gap_cards: list,  # List of UnsolvedCard (batched by file)
        specific_skill_file: str,
        epoch: int
    ) -> Tuple[Optional[str], bool]:
        """
        Update Description and Procedure sections based on incomplete_procedure cases.

        Accepts a BATCH of cards for the same file, making one LLM call.

        Args:
            skill: Skill object to update
            gap_cards: List of UnsolvedCard with incomplete_procedure diagnosis
            specific_skill_file: Specific skill file to update
            epoch: Current epoch number

        Returns:
            Tuple of (updated_content, was_updated)
        """
        # Load current skill content
        if specific_skill_file and specific_skill_file != "SKILL.md":
            skill_file = skill.skill_dir / specific_skill_file
        else:
            skill_file = skill.skill_dir / "SKILL.md"

        if not skill_file.exists():
            print(f"  ⚠️  Skill file not found: {skill_file}")
            return None, False

        with open(skill_file, 'r', encoding="utf-8") as f:
            current_skill_content = f.read()

        # Format all gap cases (up to 10)
        cases_text = []
        for i, card in enumerate(gap_cards[:10], 1):
            question_text = card.question[:2048] + "..." if len(card.question) > 2048 else card.question
            explanation_text = card.skill_used.get('explanation', 'N/A')
            if explanation_text and len(explanation_text) > 2048:
                explanation_text = explanation_text[:2048] + "..."
            # Build options section if available
            options_text = f"\n- Options: {card.options}" if getattr(card, 'options', None) else ""
            cases_text.append(f"""**Case {i}:**
- Question: {question_text}{options_text}
- Ground Truth: {card.ground_truth}
- Skill Answer (WRONG): {card.skill_used.get('answer', 'N/A')}
- Skill Reasoning: {explanation_text}
- Root Cause: {card.diagnosis_explanation or 'Description/Procedure incomplete or unclear'}""")

        all_cases = "\n\n".join(cases_text)

        # Detect if this is a PoT skill and select appropriate prompt
        is_pot = self._is_pot_skill(current_skill_content)
        # For PoT skills, use PROCEDURE_UPDATE_PROMPT_POT for adding worked examples
        prompt_template = PROCEDURE_UPDATE_PROMPT_POT if is_pot else UPDATE_DESCRIPTION_PROCEDURE_PROMPT

        # Different parameter names for PoT vs standard prompts
        if is_pot:
            prompt = prompt_template.format(
                skill_file=specific_skill_file or "SKILL.md",
                current_skill=current_skill_content,
                gap_evidence=all_cases
            )
        else:
            prompt = prompt_template.format(
                current_skill_content=current_skill_content,
                num_cases=len(gap_cards),
                cases_text=all_cases
            )

        return self._call_llm_refine(prompt, skill, epoch, current_skill_content)

    def update_example(
        self,
        skill: 'SkillRef',
        gap_cards: list,  # List of UnsolvedCard (batched by file)
        specific_skill_file: str,
        epoch: int
    ) -> Tuple[Optional[str], bool]:
        """
        Update Example section based on weak_example (standard) or weak_procedure_example (PoT) cases.

        Accepts a BATCH of cards for the same file, making one LLM call.

        Args:
            skill: Skill object to update
            gap_cards: List of UnsolvedCard with weak_example or weak_procedure_example diagnosis
            specific_skill_file: Specific skill file to update
            epoch: Current epoch number

        Returns:
            Tuple of (updated_content, was_updated)
        """
        # Load current skill content
        if specific_skill_file and specific_skill_file != "SKILL.md":
            skill_file = skill.skill_dir / specific_skill_file
        else:
            skill_file = skill.skill_dir / "SKILL.md"

        if not skill_file.exists():
            print(f"  ⚠️  Skill file not found: {skill_file}")
            return None, False

        with open(skill_file, 'r', encoding="utf-8") as f:
            current_skill_content = f.read()

        # Format all gap cases (up to 10)
        cases_text = []
        for i, card in enumerate(gap_cards[:10], 1):
            question_text = card.question[:2048] + "..." if len(card.question) > 2048 else card.question
            explanation_text = card.skill_used.get('explanation', 'N/A')
            if explanation_text and len(explanation_text) > 2048:
                explanation_text = explanation_text[:2048] + "..."
            # Build options section if available
            options_text = f"\n- Options: {card.options}" if getattr(card, 'options', None) else ""
            cases_text.append(f"""**Case {i}:**
- Question: {question_text}{options_text}
- Ground Truth: {card.ground_truth}
- Skill Answer (WRONG): {card.skill_used.get('answer', 'N/A')}
- Skill Reasoning: {explanation_text}
- Root Cause: {card.diagnosis_explanation or 'Example does not help with this case type'}""")

        all_cases = "\n\n".join(cases_text)

        # Detect if this is a PoT skill and select appropriate prompt
        is_pot = self._is_pot_skill(current_skill_content)
        # For PoT skills, use PROCEDURE_UPDATE_PROMPT_POT for worked examples
        prompt_template = PROCEDURE_UPDATE_PROMPT_POT if is_pot else UPDATE_EXAMPLE_PROMPT

        # Different parameter names for PoT vs standard prompts
        if is_pot:
            prompt = prompt_template.format(
                skill_file=specific_skill_file or "SKILL.md",
                current_skill=current_skill_content,
                gap_evidence=all_cases
            )
        else:
            prompt = prompt_template.format(
                current_skill_content=current_skill_content,
                num_cases=len(gap_cards),
                cases_text=all_cases
            )

        return self._call_llm_refine(prompt, skill, epoch, current_skill_content)

    def add_checks_and_constraints(
        self,
        skill: 'SkillRef',
        gap_cards: list,  # List of UnsolvedCard (batched by file)
        specific_skill_file: str,
        epoch: int
    ) -> Tuple[Optional[str], bool]:
        """
        Add CHECK steps and Common Bugs based on need_checks cases (PoT mode only).

        Pattern matches but missing enough CHECK steps or Common Bugs to Avoid,
        so the skill fails on new questions; and/or missing validation logic or
        sanity checks in the code.

        Accepts a BATCH of cards for the same file, making one LLM call.

        Args:
            skill: Skill object to update
            gap_cards: List of UnsolvedCard with need_checks diagnosis (PoT mode)
            specific_skill_file: Specific skill file to update
            epoch: Current epoch number

        Returns:
            Tuple of (updated_content, was_updated)
        """
        # Load current skill content
        if specific_skill_file and specific_skill_file != "SKILL.md":
            skill_file = skill.skill_dir / specific_skill_file
        else:
            skill_file = skill.skill_dir / "SKILL.md"

        if not skill_file.exists():
            print(f"  ⚠️  Skill file not found: {skill_file}")
            return None, False

        with open(skill_file, 'r', encoding="utf-8") as f:
            current_skill_content = f.read()

        # Format all gap cases (up to 10)
        cases_text = []
        for i, card in enumerate(gap_cards[:10], 1):
            question_text = card.question[:2048] + "..." if len(card.question) > 2048 else card.question
            explanation_text = card.skill_used.get('explanation', 'N/A')
            if explanation_text and len(explanation_text) > 2048:
                explanation_text = explanation_text[:2048] + "..."
            # Build options section if available
            options_text = f"\n- Options: {card.options}" if getattr(card, 'options', None) else ""
            cases_text.append(f"""**Case {i}:**
- Question: {question_text}{options_text}
- Ground Truth: {card.ground_truth}
- Skill Answer (WRONG): {card.skill_used.get('answer', 'N/A')}
- Skill Reasoning: {explanation_text}
- Root Cause: {card.diagnosis_explanation or 'Pattern matches but missing CHECK steps or validation logic'}""")

        all_cases = "\n\n".join(cases_text)

        # Use CHECKS_UPDATE_PROMPT_POT for PoT mode
        prompt = CHECKS_UPDATE_PROMPT_POT.format(
            skill_file=specific_skill_file or "SKILL.md",
            current_skill=current_skill_content,
            gap_evidence=all_cases
        )

        return self._call_llm_refine(prompt, skill, epoch, current_skill_content)

    def update_when_to_use(
        self,
        skill: 'SkillRef',
        gap_cards: list,  # List of UnsolvedCard (batched by file)
        specific_skill_file: str,
        epoch: int
    ) -> Tuple[Optional[str], bool]:
        """
        Update "When to Use" section based on trigger_mismatch cases.

        Accepts a BATCH of cards for the same file, making one LLM call.

        Args:
            skill: Skill object to update
            gap_cards: List of UnsolvedCard with trigger_mismatch diagnosis
            specific_skill_file: Specific skill file to update
            epoch: Current epoch number

        Returns:
            Tuple of (updated_content, was_updated)
        """
        # Load current skill content
        if specific_skill_file and specific_skill_file != "SKILL.md":
            skill_file = skill.skill_dir / specific_skill_file
        else:
            skill_file = skill.skill_dir / "SKILL.md"

        if not skill_file.exists():
            print(f"  ⚠️  Skill file not found: {skill_file}")
            return None, False

        with open(skill_file, 'r', encoding="utf-8") as f:
            current_skill_content = f.read()

        # Format all gap cases (up to 10)
        cases_text = []
        for i, card in enumerate(gap_cards[:10], 1):
            question_text = card.question[:2048] + "..." if len(card.question) > 2048 else card.question
            explanation_text = card.skill_used.get('explanation', 'N/A')
            if explanation_text and len(explanation_text) > 2048:
                explanation_text = explanation_text[:2048] + "..."
            # Build options section if available
            options_text = f"\n- Options: {card.options}" if getattr(card, 'options', None) else ""
            cases_text.append(f"""**Case {i}:**
- Question: {question_text}{options_text}
- Ground Truth: {card.ground_truth}
- Skill Answer (WRONG): {card.skill_used.get('answer', 'N/A')}
- Skill Reasoning: {explanation_text}
- Root Cause: {card.diagnosis_explanation or 'When to Use section did not match this case'}""")

        all_cases = "\n\n".join(cases_text)

        # Note: UPDATE_WHEN_TO_USE_PROMPT works for both standard and PoT skills
        # (trigger refinement doesn't need code-specific instructions)
        prompt = UPDATE_WHEN_TO_USE_PROMPT.format(
            current_skill_content=current_skill_content,
            num_cases=len(gap_cards),
            cases_text=all_cases
        )

        return self._call_llm_refine(prompt, skill, epoch, current_skill_content)

    def coverage_refine(
        self,
        skill: 'SkillRef',
        gap_cards: list,  # List of UnsolvedCard (batched by file)
        specific_skill_file: str,
        diagnosis_type: str,  # Action name: update_description_procedure, update_example, update_when_to_use, add_checks_and_constraints
        epoch: int
    ) -> Tuple[Optional[str], bool, List[str]]:
        """
        Unified coverage refinement using COVERAGE_REFINEMENT_PROMPT.

        Handles all action types with a single prompt + dynamic guidance injection.
        Returns new pattern names for SKILL.md update.

        Args:
            skill: Skill object to update
            gap_cards: List of UnsolvedCard with the specified action type
            specific_skill_file: Specific skill file to update
            diagnosis_type: Action name - one of:
                Non-PoT: update_description_procedure, update_example, update_when_to_use
                PoT: update_example, add_checks_and_constraints
            epoch: Current epoch number

        Returns:
            Tuple of (updated_content, was_updated, new_pattern_names)
        """
        # Load current skill content
        if specific_skill_file and specific_skill_file != "SKILL.md":
            skill_file = skill.skill_dir / specific_skill_file
        else:
            skill_file = skill.skill_dir / "SKILL.md"

        if not skill_file.exists():
            print(f"  ⚠️  Skill file not found: {skill_file}")
            return None, False, []

        with open(skill_file, 'r', encoding="utf-8") as f:
            current_skill_content = f.read()

        # Format all gap cases (up to 10)
        cases_text = []
        for i, card in enumerate(gap_cards[:10], 1):
            question_text = card.question[:2048] + "..." if len(card.question) > 2048 else card.question
            explanation_text = card.skill_used.get('explanation', 'N/A')
            if explanation_text and len(explanation_text) > 2048:
                explanation_text = explanation_text[:2048] + "..."
            # Build options section if available
            options_text = f"\n- Options: {card.options}" if getattr(card, 'options', None) else ""
            cases_text.append(f"""**Case {i}:**
- Question: {question_text}{options_text}
- Ground Truth: {card.ground_truth}
- Skill Answer (WRONG): {card.skill_used.get('answer', 'N/A')}
- Skill Reasoning: {explanation_text}
- Diagnosis: {card.diagnosis_explanation or diagnosis_type}""")

        all_cases = "\n\n".join(cases_text)

        # Detect if this is a PoT skill and select appropriate prompt/guidance
        is_pot = self._is_pot_skill(current_skill_content)

        if is_pot:
            prompt_template = COVERAGE_REFINEMENT_PROMPT_POT
            guidance_dict = DIAGNOSIS_GUIDANCE_POT
        else:
            prompt_template = COVERAGE_REFINEMENT_PROMPT
            guidance_dict = DIAGNOSIS_GUIDANCE

        # Get diagnosis-specific guidance
        diagnosis_guidance = guidance_dict.get(diagnosis_type, "")

        # Build prompt
        prompt = prompt_template.format(
            skill_file=specific_skill_file or "SKILL.md",
            skill_set_name=skill.skill_set_name if hasattr(skill, 'skill_set_name') else "unknown",
            current_skill=current_skill_content,
            diagnosis_type=diagnosis_type,
            diagnosis_guidance=diagnosis_guidance,
            num_cases=len(gap_cards),
            gap_evidence=all_cases
        )

        # Call LLM and get result with new pattern names
        updated_content, was_updated, new_names = self._call_llm_refine_with_new_patterns(
            prompt, skill, epoch, current_skill_content
        )

        return updated_content, was_updated, new_names

    def _call_llm_refine_with_new_patterns(
        self,
        prompt: str,
        skill: 'SkillRef',
        epoch: int,
        current_skill_content: str
    ) -> Tuple[Optional[str], bool, List[str]]:
        """
        Call LLM to refine a skill and return new pattern names.

        Similar to _call_llm_refine but also returns new_names for SKILL.md update.

        Returns:
            Tuple of (updated_content, was_updated, new_pattern_names)
        """
        try:
            refine_model = get_refine_model()
            print(f"  Calling LLM for coverage refinement (model: {refine_model}, temperature: {REFINE_TEMPERATURE})...")
            llm_response, stop_reason = call_refine_llm(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.DEFAULT_MAX_TOKENS
            )

            # Check for truncation
            if stop_reason == "max_tokens":
                print(f"  ⚠️  WARNING: Response truncated by max_tokens ({self.DEFAULT_MAX_TOKENS}). Output may be incomplete.")

            # Strip code block wrappers
            llm_response = self._strip_code_block_wrapper(llm_response)

            # Check if there are any changes
            if not self._has_changes(llm_response):
                print(f"  No changes needed (current skill is already effective)")
                return None, False, []

            # Apply incremental changes to current skill
            updated_content, refined_names, new_names = self._apply_incremental_changes(
                current_skill_content,
                llm_response
            )

            n_refined = len(refined_names)
            n_new = len(new_names)

            # Format output message with pattern names
            if n_refined > 0 or n_new > 0:
                msg = f"  ✅ Coverage refinement complete"
                if n_refined > 0:
                    msg += f" (refined: {', '.join(refined_names)})"
                if n_new > 0:
                    msg += f" (new: {', '.join(new_names)})"
                print(msg)
            else:
                print(f"  ✅ Coverage refinement complete (no pattern changes)")

            return updated_content, True, new_names

        except Exception as e:
            print(f"  ❌ LLM call failed: {e}")
            return None, False, []

    def update_skill_md_add_entry(
        self,
        skill: 'SkillRef',
        new_file_path: str,
        subfield: str,
        error_type: str,
        key_patterns: List[str]
    ) -> bool:
        """
        Add a new entry to SKILL.md's file reference table.

        Called after creating a new skill file so the router can discover it.

        Args:
            skill: SkillRef with skill_dir
            new_file_path: Relative path to new file (e.g., "equity/new_patterns.md")
            subfield: Display subfield (e.g., "Equity")
            error_type: Error type (e.g., "Concept confusion")
            key_patterns: List of key pattern names

        Returns:
            True if SKILL.md was updated
        """
        skill_md_path = skill.skill_dir / "SKILL.md"
        if not skill_md_path.exists():
            print(f"  SKILL.md not found: {skill_md_path}")
            return False

        with open(skill_md_path, 'r', encoding="utf-8") as f:
            content = f.read()

        # Check if entry already exists (avoid duplicates)
        if f"`{new_file_path}`" in content:
            print(f"  ⏭️  SKILL.md entry already exists: {new_file_path}")
            return False

        # Format the new table row
        patterns_str = ", ".join(key_patterns) if key_patterns else "(new patterns)"
        new_row = f"| `{new_file_path}` | {subfield} | {error_type} | {patterns_str} |"

        # Find the last row of the file reference table and append after it
        lines = content.split('\n')
        insert_idx = None

        for i, line in enumerate(lines):
            stripped = line.strip()
            # Find table rows that contain file paths (backtick-wrapped)
            if stripped.startswith('|') and '`' in stripped and '.md' in stripped:
                insert_idx = i + 1  # Insert after the last data row

        if insert_idx is not None:
            lines.insert(insert_idx, new_row)
            updated_content = '\n'.join(lines)
            with open(skill_md_path, 'w', encoding="utf-8") as f:
                f.write(updated_content)
            print(f"  Added SKILL.md entry: {new_file_path}")
            return True
        else:
            print(f"  Could not find file reference table in SKILL.md")
            return False

    def extract_skill_md_entry_from_content(self, content: str) -> Optional[str]:
        """
        Extract SKILL_MD_ENTRY line from generated skill content.

        The NEW_SKILL_CREATION_PROMPT asks the LLM to include:
        SKILL_MD_ENTRY: | `path` | Subfield | Error Type | Patterns |

        Args:
            content: Generated skill file content

        Returns:
            The table row string, or None
        """
        for line in content.split('\n'):
            if line.strip().startswith('SKILL_MD_ENTRY:'):
                return line.strip().replace('SKILL_MD_ENTRY:', '').strip()
        return None

    def _call_llm_refine(self, prompt: str, skill: 'SkillRef', epoch: int, current_skill_content: str) -> Tuple[Optional[str], bool]:
        """
        Call LLM to refine a skill (API mode) and apply incremental changes.

        Args:
            prompt: The refinement prompt
            skill: SkillRef being refined
            epoch: Current epoch number
            current_skill_content: Current content of the skill file (for incremental refinement)

        Returns:
            Tuple of (updated_content, was_updated)
        """
        try:
            refine_model = get_refine_model()
            print(f"  Calling LLM for refinement (model: {refine_model}, temperature: {REFINE_TEMPERATURE})...")
            llm_response, stop_reason = call_refine_llm(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.DEFAULT_MAX_TOKENS
            )

            # Check for truncation
            if stop_reason == "max_tokens":
                print(f"  ⚠️  WARNING: Response truncated by max_tokens ({self.DEFAULT_MAX_TOKENS}). Output may be incomplete.")

            # Strip code block wrappers (handles both complete and truncated responses)
            llm_response = self._strip_code_block_wrapper(llm_response)

            # Check if there are any changes (incremental refinement format)
            if not self._has_changes(llm_response):
                print(f"  No changes needed (current skill is already effective)")
                return None, False

            # Apply incremental changes to current skill
            updated_content, refined_names, new_names = self._apply_incremental_changes(
                current_skill_content,
                llm_response
            )

            n_refined = len(refined_names)
            n_new = len(new_names)

            # Format output message with pattern names
            if n_refined > 0 or n_new > 0:
                msg = f"  ✅ Refinement complete"
                if n_refined > 0:
                    msg += f" (refined: {', '.join(refined_names)})"
                if n_new > 0:
                    msg += f" (new: {', '.join(new_names)})"
                print(msg)
            else:
                print(f"  ✅ Refinement complete (no changes)")

            return updated_content, True

        except Exception as e:
            print(f"  ❌ LLM call failed: {e}")
            return None, False

    def _call_llm_create(self, prompt: str, skill, epoch: int) -> Tuple[str, bool]:
        """
        Call LLM to create a new skill (API mode).

        Args:
            prompt: The creation prompt
            skill: Parent skill object
            epoch: Current epoch number

        Returns:
            Tuple of (new_skill_content, was_created)
        """
        try:
            refine_model = get_refine_model()
            print(f"  Calling LLM for skill creation (model: {refine_model}, temperature: {REFINE_TEMPERATURE})...")
            new_content, stop_reason = call_refine_llm(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.DEFAULT_MAX_TOKENS
            )

            # Check for truncation
            if stop_reason == "max_tokens":
                print(f"  ⚠️  WARNING: Response truncated by max_tokens ({self.DEFAULT_MAX_TOKENS}). Output may be incomplete.")

            # Strip code block wrappers (handles both complete and truncated responses)
            new_content = self._strip_code_block_wrapper(new_content)

            print(f"  ✅ New skill created")
            return new_content, True

        except Exception as e:
            print(f"  ❌ LLM call failed: {e}")
            return None, False


# Example usage
if __name__ == "__main__":
    from pathlib import Path

    # Create a SkillRef for testing
    skill = SkillRef(
        skill_dir=Path(".claude/skills/famma-non-arithmetic-v1"),
        name="famma-non-arithmetic-v1"
    )

    print("SkillRef created:")
    print(f"  name: {skill.name}")
    print(f"  skill_dir: {skill.skill_dir}")

    # Test optimizer initialization
    optimizer = TextualOptimizer()

    print("\nTextual optimizer ready!")
    print("\nUsage:")
    print("  optimizer = TextualOptimizer()")
    print("\nSkillRef usage:")
    print("  skill = SkillRef(skill_dir=Path('...'), name='skill-set-name')")
    print("  optimizer.refine_skill(skill, Q_plus, Q_minus, specific_skill_file='subfield/file.md')")
