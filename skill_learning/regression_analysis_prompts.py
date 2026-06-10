"""
Analysis Prompts for Skill Learning

Contains prompts for:
1. Deep analysis (original) - why skill helped/hurt
2. Attribution analysis (new) - which skill file caused the issue
"""


# =============================================================================
# ORIGINAL DEEP ANALYSIS PROMPT (extracted from textual_optimizer.py)
# =============================================================================

# Analysis instructions for non-PoT (no code) cases
DEEP_ANALYSIS_INSTRUCTIONS_NO_CODE = """Provide a concise analysis (1-2 sentences) explaining:
1. If the skill helped: WHY did it help? What concept/reasoning did it add?
2. If the skill hurt: WHAT went wrong? What mistake did it introduce?
3. What specific knowledge or pattern made the difference?
4. How did the baseline (without skill) get it right, while the skill version got it wrong?"""

# Analysis instructions for PoT (with code) cases
DEEP_ANALYSIS_INSTRUCTIONS_WITH_CODE = """Provide a concise analysis (1-2 sentences) explaining:
1. If the skill helped: WHY did it help? What concept/reasoning or CODE PATTERN did it add?
2. If the skill hurt: WHAT went wrong? What mistake in REASONING or CODE did it introduce?
3. What specific knowledge, calculation pattern, or code implementation made the difference?
4. If code is present: Did the skill fix/introduce bugs, improve calculation accuracy, or change the algorithm? What specific pattern or code implementation caused the error?
5. How did the baseline (without skill) get it right, while the skill version got it wrong?"""


DEEP_ANALYSIS_PROMPT_TEMPLATE = """Analyze the impact of adding a skill to the model's reasoning.

**Question**: {question}
**Context**: {context}
{options_section}
**Ground Truth**: {ground_truth}
{skills_loaded}
**Baseline Reasoning** (score: {baseline_score} , without skill):
Answer: {baseline_answer}
Explanation: {baseline_explanation}{baseline_code_section}

**With Skill** (score: {skill_score}, with skill):
Answer: {skill_answer}
Explanation: {skill_explanation}{skill_code_section}

{analysis_instructions}

Analysis:"""


def build_deep_analysis_prompt(
    question: str,
    context: str,
    options: str,
    ground_truth: str,
    baseline_score: int,
    baseline_answer: str,
    baseline_explanation: str,
    skill_score: int,
    skill_answer: str,
    skill_explanation: str,
    skills_loaded: str = "",
    baseline_code: str = None,
    skill_code: str = None
) -> str:
    """Build the deep analysis prompt.

    Args:
        question: The question text
        ground_truth: Correct answer
        baseline_score: Score without skill
        baseline_answer: Answer without skill
        baseline_explanation: Explanation without skill
        skill_score: Score with skill
        skill_answer: Answer with skill
        skill_explanation: Explanation with skill
        skills_loaded: Formatted string of loaded skill files
        baseline_code: Generated code without skill (PoT mode)
        skill_code: Generated code with skill (PoT mode)

    Returns:
        Formatted prompt string
    """
    # Include options section if available
    options_section = ""
    if options:
        options_section = f"**Options**: {options}\n"

    # Include code sections if available (PoT mode)
    baseline_code_section = ""
    if baseline_code:
        baseline_code_section = f"\nGenerated Code:\n```python\n{baseline_code}\n```\n"

    skill_code_section = ""
    if skill_code:
        skill_code_section = f"\nGenerated Code:\n```python\n{skill_code}\n```\n"

    # Select appropriate analysis instructions
    if baseline_code or skill_code:
        analysis_instructions = DEEP_ANALYSIS_INSTRUCTIONS_WITH_CODE
    else:
        analysis_instructions = DEEP_ANALYSIS_INSTRUCTIONS_NO_CODE

    return DEEP_ANALYSIS_PROMPT_TEMPLATE.format(
        question=question,
        context=context or "None",
        options_section=options_section,
        ground_truth=ground_truth,
        skills_loaded=skills_loaded,
        baseline_score=baseline_score,
        baseline_answer=baseline_answer,
        baseline_explanation=baseline_explanation,
        baseline_code_section=baseline_code_section,
        skill_score=skill_score,
        skill_answer=skill_answer,
        skill_explanation=skill_explanation,
        skill_code_section=skill_code_section,
        analysis_instructions=analysis_instructions
    )


# =============================================================================
# ATTRIBUTION + DEEP ANALYSIS PROMPTS (for both fix and regression)
# Supports both PoT mode (with code) and non-PoT mode (with explanation)
# =============================================================================

# -----------------------------------------------------------------------------
# PoT MODE TEMPLATES (with code and execution status)
# -----------------------------------------------------------------------------

# For REGRESSION cases in PoT mode (skill hurt performance)
ATTRIBUTION_REGRESSION_PROMPT_POT_TEMPLATE = """You are analyzing why adding skill guidance caused the model to produce a wrong answer (regression case).

## Question Information
**Question**: {question}
**Context**: {context}
{options_section}
**Ground Truth**: {ground_truth}
**Baseline Answer** (without skill, was correct): {baseline_answer}
**Skill Answer** (with skill, now wrong): {skill_answer}

## Skill Files Loaded
{loaded_files_list}

## Patterns Extracted from Generated Code
{extracted_patterns_info}

## Skill Files Content
{skill_files_content}

## Generated Code (with skill)
**Execution Status**: {execution_status}
```python
{skill_code}
```

---

## Your Task

### Step 1: Attribution
Determine which skill file(s) most likely caused this regression:
- Which pattern(s) from the skill files did the code follow?
- Did the model apply guidance that doesn't apply to this question?
- Did the skill's guidance lead to incorrect reasoning or wrong assumptions?
- Did the model misinterpret or over-apply the skill's guidance?
{execution_failed_hint}

### Step 2: Analysis
Explain WHY the skill guidance hurt performance. Be specific:
- What mistake in REASONING or CODE did the skill introduce?
- What specific pattern or code implementation caused the error?
- How did the baseline (without skill) get it right, while the skill version got it wrong?

---

## Output Format (JSON)
```json
{{
    "attributed_files": ["file1.md", "file2.md"],
    "analysis": "A concise analysis (2-3 sentences) according to the instructions in step 2."
}}
```

Output:"""


# For FIX cases in PoT mode (skill helped performance)
ATTRIBUTION_FIX_PROMPT_POT_TEMPLATE = """You are analyzing why adding skill guidance helped the model produce the correct answer (fix case).

## Question Information
**Question**: {question}
**Context**: {context}
{options_section}
**Ground Truth**: {ground_truth}
**Baseline Answer** (without skill, was wrong): {baseline_answer}
**Skill Answer** (with skill, now correct): {skill_answer}

## Skill Files Loaded
{loaded_files_list}

## Patterns Extracted from Generated Code
{extracted_patterns_info}

## Skill Files Content
{skill_files_content}

## Generated Code (with skill)
**Execution Status**: {execution_status}
```python
{skill_code}
```

---

## Your Task

### Step 1: Attribution
Determine which skill file(s) most likely caused this fix:
- Which pattern(s) from the skill files did the code follow?
- Did the model apply a pattern that correctly addressed the question's requirements?
- What domain knowledge or calculation pattern from the skill files made the difference?

### Step 2: Analysis
Explain WHY the skill guidance helped. Be specific:
- What concept, reasoning, or CODE PATTERN did the skill add?
- What specific knowledge or calculation pattern made the difference?
- How did the baseline (without skill) fail, and how did the skill guidance correct it?

---

## Output Format (JSON)
```json
{{
    "attributed_files": ["file1.md", "file2.md"],
    "analysis": "A concise analysis (2-3 sentences) according to the instructions in step 2. Which Patterns/Skills help? How they help?"
}}
```

Output:"""


# -----------------------------------------------------------------------------
# NON-POT MODE TEMPLATES (with explanation, no code)
# -----------------------------------------------------------------------------

# For REGRESSION cases in non-PoT mode (skill hurt performance)
ATTRIBUTION_REGRESSION_PROMPT_NO_CODE_TEMPLATE = """You are analyzing why adding skill guidance caused the model to produce a wrong answer (regression case).

## Question Information
**Question**: {question}
**Context**: {context}
{options_section}
**Ground Truth**: {ground_truth}
**Baseline Answer** (without skill, was correct): {baseline_answer}
**Skill Answer** (with skill, now wrong): {skill_answer}

## Skill Files Loaded
{loaded_files_list}

## Skill Files Content
{skill_files_content}

## Model's Explanation (with skill)
{skill_explanation}

---

## Your Task

### Step 1: Attribution
Determine which skill file(s) most likely caused this regression:
- Which guidance or concept from the skill files did the model follow?
- Did the model apply guidance that doesn't apply to this question?
- Did the skill's guidance lead to incorrect reasoning or wrong assumptions?
- Did the model misinterpret or over-apply the skill's guidance?

### Step 2: Analysis
Explain WHY the skill guidance hurt performance. Be specific:
- What mistake in REASONING did the skill introduce?
- What specific concept or guidance from the skill caused the error?
- How did the baseline (without skill) get it right, while the skill version got it wrong?

---

## Output Format (JSON)
```json
{{
    "attributed_files": ["file1.md", "file2.md"],
    "analysis": "A concise analysis (2-3 sentences) according to the instructions in step 2."
}}
```

Output:"""


# For FIX cases in non-PoT mode (skill helped performance)
ATTRIBUTION_FIX_PROMPT_NO_CODE_TEMPLATE = """You are analyzing why adding skill guidance helped the model produce the correct answer (fix case).

## Question Information
**Question**: {question}
**Context**: {context}
{options_section}
**Ground Truth**: {ground_truth}
**Baseline Answer** (without skill, was wrong): {baseline_answer}
**Skill Answer** (with skill, now correct): {skill_answer}

## Skill Files Loaded
{loaded_files_list}

## Skill Files Content
{skill_files_content}

## Model's Explanation (with skill)
{skill_explanation}

---

## Your Task

### Step 1: Attribution
Determine which skill file(s) most likely caused this fix:
- Which guidance or concept from the skill files did the model follow?
- Did the model apply guidance that correctly addressed the question's requirements?
- What domain knowledge or reasoning approach from the skill files made the difference?

### Step 2: Analysis
Explain WHY the skill guidance helped. Be specific:
- What concept or reasoning approach did the skill add?
- What specific knowledge or guidance made the difference?
- How did the baseline (without skill) fail, and how did the skill guidance correct it?

---

## Output Format (JSON)
```json
{{
    "attributed_files": ["file1.md", "file2.md"],
    "analysis": "A concise analysis (2-3 sentences) according to the instructions in step 2. Which guidance/concepts help? How they help?"
}}
```

Output:"""


# -----------------------------------------------------------------------------
# BACKWARD COMPATIBILITY - Keep old template names as aliases
# -----------------------------------------------------------------------------
# These point to the PoT templates for backward compatibility
ATTRIBUTION_REGRESSION_PROMPT_TEMPLATE = ATTRIBUTION_REGRESSION_PROMPT_POT_TEMPLATE
ATTRIBUTION_FIX_PROMPT_TEMPLATE = ATTRIBUTION_FIX_PROMPT_POT_TEMPLATE


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def is_common_file(file_path: str) -> bool:
    """Check if a file path is a common skill file."""
    return file_path.startswith('common/') or '/common/' in file_path


def format_loaded_files_list(loaded_files: list) -> str:
    """Format loaded files as a numbered list with [COMMON] / [SUBFIELD] tags."""
    if not loaded_files:
        return "No skill files loaded."

    lines = []
    for i, f in enumerate(loaded_files):
        tag = "[COMMON]" if is_common_file(f) else "[SUBFIELD]"
        lines.append(f"{i+1}. `{f}` {tag}")
    return "\n".join(lines)


def format_skill_files_content(loaded_files: list, skill_files_content: dict) -> str:
    """Format all loaded skill files with their content.

    Args:
        loaded_files: List of loaded file paths
        skill_files_content: Dict mapping file path -> file content

    Returns:
        Formatted string with content of each file
    """
    if not loaded_files:
        return "No skill files loaded."

    sections = []
    for file_path in loaded_files:
        content = skill_files_content.get(file_path, "(Content not available)")
        tag = "[COMMON]" if is_common_file(file_path) else "[SUBFIELD]"
        sections.append(f"### {file_path} {tag}\n```markdown\n{content}\n```")

    return "\n\n".join(sections)


def format_extracted_patterns(extracted_patterns: list) -> str:
    """Format extracted pattern names from code.

    Args:
        extracted_patterns: List of pattern names extracted from code

    Returns:
        Formatted string listing the patterns
    """
    if not extracted_patterns:
        return "No patterns explicitly referenced in the generated code."

    return "The following patterns were referenced in the code comments:\n" + \
           "\n".join(f"- {p}" for p in extracted_patterns)


def extract_patterns_from_code(skill_code: str) -> list:
    """Extract pattern names from generated code comments.

    Handles various formats found in generated code:
    - # Pattern: XXX
    - # Pattern: XXX (for YYY)
    - # Pattern: XXX - simplified for YYY
    - # - Pattern: XXX (for YYY)
    - # Bond pricing with forward rates (Pattern: XXX)
    - # Domain Knowledge Pattern: XXX
    - # Domain Knowledge: Pattern - XXX
    - # From the domain knowledge pattern: XXX
    - # According to the "XXX" pattern:
    - # Let's look at the pattern: "XXX"
    - # based on pattern: "XXX"
    - # based on the pattern "XXX"

    Args:
        skill_code: Generated Python code

    Returns:
        List of pattern names found in code comments (deduplicated)
    """
    import re

    if not skill_code:
        return []

    patterns_found = []

    # Format 1: # Pattern: XXX or # - Pattern: XXX
    # Captures everything after "Pattern:" until newline, parenthesis qualifier, or dash qualifier
    format1 = re.findall(
        r'#\s*-?\s*Pattern:\s*([^(\n]+?)(?:\s*\(|\s*-\s+|\s*$)',
        skill_code,
        re.IGNORECASE | re.MULTILINE
    )
    patterns_found.extend(format1)

    # Format 2: (Pattern: XXX) - pattern name in parentheses
    format2 = re.findall(
        r'\(Pattern:\s*([^)]+)\)',
        skill_code,
        re.IGNORECASE
    )
    patterns_found.extend(format2)

    # Format 3: Domain Knowledge Pattern: XXX
    format3 = re.findall(
        r'#\s*Domain Knowledge Pattern:\s*([^(\n]+?)(?:\s*\(|\s*$)',
        skill_code,
        re.IGNORECASE | re.MULTILINE
    )
    patterns_found.extend(format3)

    # Format 4: Domain Knowledge: Pattern - XXX
    format4 = re.findall(
        r'#\s*Domain Knowledge:\s*Pattern\s*-\s*([^\n]+)',
        skill_code,
        re.IGNORECASE
    )
    patterns_found.extend(format4)

    # Format 5: From the domain knowledge pattern: XXX
    format5 = re.findall(
        r'#\s*From the domain knowledge pattern:\s*([^\n]+)',
        skill_code,
        re.IGNORECASE
    )
    patterns_found.extend(format5)

    # Format 6: According to the "XXX" pattern or based on pattern: "XXX" or pattern "XXX"
    format6 = re.findall(
        r'(?:According to the|based on(?: the)? pattern:?|look at the pattern:?)\s*["\']([^"\']+)["\']',
        skill_code,
        re.IGNORECASE
    )
    patterns_found.extend(format6)

    # Format 7: the "XXX" pattern (quoted pattern name followed by "pattern")
    format7 = re.findall(
        r'the\s+["\']([^"\']+)["\']\s+pattern',
        skill_code,
        re.IGNORECASE
    )
    patterns_found.extend(format7)

    # Clean up pattern names
    cleaned = []
    for p in patterns_found:
        # Strip whitespace and trailing punctuation
        p = p.strip().rstrip('.:,;')
        # Remove common suffixes that aren't part of the pattern name
        p = re.sub(r'\s*\(PoT\)\s*$', '', p, flags=re.IGNORECASE)
        if p and len(p) > 3:  # Filter out too-short matches
            cleaned.append(p)

    # Deduplicate while preserving order
    seen = set()
    result = []
    for p in cleaned:
        p_lower = p.lower()
        if p_lower not in seen:
            seen.add(p_lower)
            result.append(p)

    return result


def build_attribution_prompt(
    question: str,
    ground_truth: str,
    baseline_answer: str,
    skill_answer: str,
    loaded_files: list,
    skill_files_content: dict,
    is_fix: bool = False,
    # Additional context
    context: str = None,
    options: str = None,
    # PoT mode parameters
    skill_code: str = None,
    execution_success: bool = None,
    # Non-PoT mode parameters
    skill_explanation: str = None
) -> str:
    """Build the attribution + deep analysis prompt.

    Supports both PoT mode (with code) and non-PoT mode (with explanation).

    Args:
        question: The question text
        ground_truth: Correct answer
        baseline_answer: Model's answer without skill
        skill_answer: Model's answer with skill
        loaded_files: List of loaded skill files
        skill_files_content: Dict mapping file path -> file content
        is_fix: True if this is a fix case, False if regression case
        skill_code: Generated code (for PoT mode, None for non-PoT)
        execution_success: Whether code executed successfully (for PoT mode)
        skill_explanation: Model's explanation (for non-PoT mode)

    Returns:
        Formatted prompt string
    """
    # Prepare shared context/options text
    context_text = context or "None"
    options_text = options or ""
    options_section = f"**Options**: {options_text}\n" if options_text else ""

    # Determine if this is PoT mode based on whether code is provided
    is_pot_mode = skill_code is not None and skill_code.strip()

    if is_pot_mode:
        # PoT mode: use code-based templates
        extracted_patterns = extract_patterns_from_code(skill_code)

        # Determine execution status string
        if execution_success is None:
            execution_status = "UNKNOWN"
        elif execution_success:
            execution_status = "SUCCESS"
        else:
            execution_status = "FAILED"

        # Common format args for PoT templates
        format_args = {
            'question': question,
            'context': context_text,
            'options': options_text,
            'options_section': options_section,
            'ground_truth': ground_truth,
            'baseline_answer': baseline_answer,
            'skill_answer': skill_answer,
            'loaded_files_list': format_loaded_files_list(loaded_files),
            'extracted_patterns_info': format_extracted_patterns(extracted_patterns),
            'skill_files_content': format_skill_files_content(loaded_files, skill_files_content),
            'skill_code': skill_code,
            'execution_status': execution_status,
        }

        if is_fix:
            # FIX template doesn't have execution_failed_hint
            return ATTRIBUTION_FIX_PROMPT_POT_TEMPLATE.format(**format_args)
        else:
            # REGRESSION template has execution_failed_hint
            if execution_success is False:
                format_args['execution_failed_hint'] = "- If execution FAILED: Did a pattern's code example cause syntax/runtime errors?"
            else:
                format_args['execution_failed_hint'] = ""
            return ATTRIBUTION_REGRESSION_PROMPT_POT_TEMPLATE.format(**format_args)
    else:
        # Non-PoT mode: use explanation-based templates
        template = ATTRIBUTION_FIX_PROMPT_NO_CODE_TEMPLATE if is_fix else ATTRIBUTION_REGRESSION_PROMPT_NO_CODE_TEMPLATE

        return template.format(
            question=question,
            context=context_text,
            options=options_text,
            options_section=options_section,
            ground_truth=ground_truth,
            baseline_answer=baseline_answer,
            skill_answer=skill_answer,
            loaded_files_list=format_loaded_files_list(loaded_files),
            skill_files_content=format_skill_files_content(loaded_files, skill_files_content),
            skill_explanation=skill_explanation or "N/A"
        )


# =============================================================================
# PATTERN TO FILE MATCHING (for regex-only fallback)
# =============================================================================

# Import extract_pattern_names from skill_warming_up to avoid duplication
try:
    from skill_warming_up import extract_pattern_names
except ImportError:
    from skill_learning.skill_warming_up import extract_pattern_names


def match_patterns_to_files(
    extracted_patterns: list,
    loaded_files: list,
    skill_files_content: dict
) -> dict:
    """Match extracted pattern names to their source skill files.

    Uses fuzzy matching to handle slight variations in pattern names.

    Args:
        extracted_patterns: List of pattern names extracted from code
        loaded_files: List of loaded skill file paths
        skill_files_content: Dict mapping file path -> file content

    Returns:
        Dict mapping pattern_name -> file_path (or None if not found)
    """
    import re
    from difflib import SequenceMatcher

    def normalize(s):
        """Normalize string for comparison."""
        return re.sub(r'[^a-z0-9]', '', s.lower())

    def similarity(a, b):
        """Calculate similarity ratio between two strings."""
        return SequenceMatcher(None, normalize(a), normalize(b)).ratio()

    # Build index of patterns in each file
    file_patterns = {}  # file_path -> list of pattern names
    for file_path in loaded_files:
        content = skill_files_content.get(file_path, "")
        patterns_in_file = extract_pattern_names(content)
        file_patterns[file_path] = patterns_in_file

    # Match each extracted pattern to a file
    matches = {}
    for extracted in extracted_patterns:
        best_match = None
        best_score = 0.0
        best_file = None

        for file_path, patterns_in_file in file_patterns.items():
            for pattern_name in patterns_in_file:
                score = similarity(extracted, pattern_name)
                if score > best_score:
                    best_score = score
                    best_match = pattern_name
                    best_file = file_path

        # Accept match if similarity > 0.7 (70%)
        if best_score > 0.7:
            matches[extracted] = {
                'file': best_file,
                'matched_pattern': best_match,
                'confidence': best_score
            }
        else:
            matches[extracted] = None

    return matches


# =============================================================================
# ATTRIBUTION RESULT HANDLING
# =============================================================================

def attribute_regression_regex_only(
    skill_code: str,
    loaded_files: list,
    skill_files_content: dict
) -> dict:
    """Attribute regression using regex pattern matching only (no LLM).

    Fallback method when deep_analysis is disabled.

    Args:
        skill_code: Generated code (for PoT questions)
        loaded_files: List of loaded skill files
        skill_files_content: Dict of file contents

    Returns:
        Attribution result dict with:
        - attributed_files: List of files attributed to
        - method: "regex"
        - matched_patterns: List of (pattern_name, file_path) tuples
        - fallback_used: Whether fallback to all loaded_files was used
    """
    # Extract patterns from code
    extracted_patterns = extract_patterns_from_code(skill_code) if skill_code else []

    if not extracted_patterns:
        # No patterns found → fallback to original method (all loaded files)
        return {
            'attributed_files': loaded_files.copy(),
            'method': 'regex_fallback',
            'matched_patterns': [],
            'fallback_used': True,
            'reason': 'No patterns extracted from code'
        }

    # Match patterns to files
    matches = match_patterns_to_files(extracted_patterns, loaded_files, skill_files_content)

    # Collect attributed files
    attributed_files = set()
    matched_patterns = []
    for pattern_name, match_info in matches.items():
        if match_info:
            attributed_files.add(match_info['file'])
            matched_patterns.append((pattern_name, match_info['file']))

    if not attributed_files:
        # Patterns extracted but no matches → fallback to all loaded files
        return {
            'attributed_files': loaded_files.copy(),
            'method': 'regex_fallback',
            'matched_patterns': [],
            'fallback_used': True,
            'reason': f'Patterns extracted ({extracted_patterns}) but no file matches found'
        }

    return {
        'attributed_files': list(attributed_files),
        'method': 'regex',
        'matched_patterns': matched_patterns,
        'fallback_used': False,
        'reason': None
    }


def merge_attribution_results(
    llm_attribution: dict,
    regex_attribution: dict
) -> dict:
    """Merge LLM-based and regex-based attribution results.

    Args:
        llm_attribution: Result from LLM attribution (may be None)
        regex_attribution: Result from regex attribution

    Returns:
        Merged attribution result
    """
    if not llm_attribution:
        return regex_attribution

    # Merge attributed files (union)
    llm_files = set(llm_attribution.get('attributed_files', []))
    regex_files = set(regex_attribution.get('attributed_files', []))

    # If regex used fallback, prefer LLM result
    if regex_attribution.get('fallback_used') and llm_files:
        merged_files = llm_files
    else:
        merged_files = llm_files | regex_files

    return {
        'attributed_files': list(merged_files),
        'primary_file': llm_attribution.get('primary_file'),
        'error_category': llm_attribution.get('error_category'),
        'analysis': llm_attribution.get('analysis'),
        'method': 'llm+regex',
        'matched_patterns': regex_attribution.get('matched_patterns', []),
        'llm_files': list(llm_files),
        'regex_files': list(regex_files)
    }


def categorize_by_file_type(attributed_files: list) -> dict:
    """Categorize attributed files into common vs subfield-specific.

    Args:
        attributed_files: List of file paths

    Returns:
        Dict with 'common' and 'subfield' lists
    """
    common = []
    subfield = []

    for f in attributed_files:
        if is_common_file(f):
            common.append(f)
        else:
            subfield.append(f)

    return {
        'common': common,
        'subfield': subfield
    }


def determine_refinement_priority(attribution_result: dict) -> str:
    """Determine refinement priority based on attribution result.

    Priority levels:
    - "common_only": Only common files attributed → highest priority for common refinement
    - "common_and_subfield": Both types → include in common refinement
    - "subfield_only": Only subfield files → skip common refinement, go to subfield phase

    Args:
        attribution_result: Result from attribute_regression

    Returns:
        Priority string
    """
    categorized = categorize_by_file_type(attribution_result.get('attributed_files', []))

    if categorized['common'] and not categorized['subfield']:
        return 'common_only'
    elif categorized['common'] and categorized['subfield']:
        return 'common_and_subfield'
    else:
        return 'subfield_only'
