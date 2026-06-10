"""
Prompts for Residual Evidence Collection and Diagnosis (PoT Mode)

This module contains PoT-specific prompts for:
- Q0_gap classification (determining root cause for code-based skills)
- Q+_discover / Q0_gap explanation generation
- Focus on code templates, worked examples, and code constraints

PoT Mode Root Causes:
- weak_procedure_example: match pattern but procedure is incomplete or lacks worked & checked example
- need_checks: match pattern but missing CHECK steps or CODE CONSTRAINTS
- new_pattern: no pattern covers this calculation type
"""

from typing import Optional


# =============================================================================
# Classification Prompts (for determining root cause)
# =============================================================================

def build_gap_classification_prompt(
    question: str,
    ground_truth: str,
    skill_name: str,
    specific_file: str,
    skill_answer: str,
    skill_content: str = "",
    options: str = "",
    generated_code: str = "",  # NEW: The code that was generated
    execution_success: bool = True  # NEW: Whether code executed successfully
) -> str:
    """
    Build classification prompt for Q0_gap case (PoT mode).

    This prompt focuses on determining the ROOT CAUSE for code-based skill failures.
    Used in batch classification for efficiency.

    Args:
        question: The question text
        ground_truth: Correct answer
        skill_name: Name of the skill that was used
        specific_file: Specific skill file that was used
        skill_answer: The wrong answer given by the skill (execution result or error)
        skill_content: Optional skill file content for analysis
        options: Optional MC options
        generated_code: The Python code that was generated (PoT mode)
        execution_success: Whether the code executed successfully

    Returns:
        Classification prompt string
    """
    skill_section = ""
    if skill_content:
        truncated = skill_content
        skill_section = f"""
**Current Skill Content** ({specific_file}):
```
{truncated}
```
"""

    options_section = f"\n**Options**: {options}" if options else ""
    
    # Build code execution section
    code_section = ""
    if generated_code:
        execution_status = "✅ Executed successfully" if execution_success else "❌ Execution failed"
        code_section = f"""
**Generated Code**:
```python
{generated_code}
```
**Execution Status**: {execution_status}
"""

    return f"""Classify why the code-based skill failed on this financial calculation question.

**Question**: {question}{options_section}
**Ground Truth**: {ground_truth}

**Skill Used**: {skill_name}/{specific_file}
**Skill Answer (WRONG)**: {skill_answer}
{code_section}
{skill_section}

Review the skill structure and classify the root cause as ONE of:

1. **weak_procedure_example** - Pattern matches this question but the procedure is incomplete or lacks a worked & checked example (step-by-step with actual numbers and verification).

2. **need_checks** - Pattern matches but missing enough CHECK steps or Common Bugs to Avoid so that the skills are failing on new questions, validation logic or sanity checks in the code.

3. **new_pattern** - No pattern covers this calculation type; this is a fundamentally different problem pattern that requires a new skill file for this problem.

**Decision Guide**:
- If pattern matches but procedure incomplete or no worked & checked example → weak_procedure_example
- If pattern matches but missing enough CHECK steps or Common Bugs to Avoid so that the skills are failing on new questions → need_checks
- If no pattern covers this calculation type → new_pattern

Output JSON only: {{"root_cause": "weak_procedure_example" | "need_checks" | "new_pattern"}}"""


# =============================================================================
# Explanation Prompts (for generating detailed explanations)
# =============================================================================

def build_discover_explanation_prompt(
    question: str,
    subfield: str,
    skill_name: str,
    specific_file: str,
    skill_answer: str,
    solving_skill: str,
    ground_truth: str,
    solving_answer: str = "",
    options: str = ""
) -> str:
    """
    Build explanation prompt for Q+_discover case (PoT mode).

    Q+_discover = Another skill solved it (trigger/routing mismatch).

    Args:
        question: The question text
        subfield: Question subfield
        skill_name: Name of the skill that failed
        specific_file: Specific skill file that failed
        skill_answer: The wrong answer
        solving_skill: The skill that correctly solved it
        ground_truth: Correct answer
        solving_answer: Optional - the correct answer from solving skill
        options: Optional MC options

    Returns:
        Explanation prompt string
    """
    options_section = f"\n**Options**: {options}" if options else ""

    # Include solving answer if provided
    solving_section = f"**Alternative Skill (SOLVED)**: {solving_skill}"
    if solving_answer:
        solving_section += f"\n- Answer: {solving_answer}"

    return f"""Analyze why the wrong code template was selected for this calculation question.

**Question**: {question}{options_section}
**Subfield**: {subfield}

**Skill Used (FAILED)**: {skill_name}/{specific_file}
- Answer: {skill_answer}

{solving_section}

**Ground Truth**: {ground_truth}

In 1-2 sentences, explain WHY the wrong code template was selected and what trigger keywords should be added to the "When to Use" section.

Analysis:"""


def build_gap_explanation_prompt(
    question: str,
    subfield: str,
    skill_name: str,
    skill_answer: str,
    ground_truth: str,
    diagnosis: str = "",
    options: str = ""
) -> str:
    """
    Build explanation prompt for Q0_gap case (PoT mode).

    Q0_gap = No skill solved it (capability gap).

    Args:
        question: The question text
        subfield: Question subfield
        skill_name: Name of the skill that was tried
        skill_answer: The wrong answer
        ground_truth: Correct answer
        diagnosis: Optional - the root cause classification
        options: Optional MC options

    Returns:
        Explanation prompt string
    """
    options_section = f"\n**Options**: {options}" if options else ""

    # Include diagnosis if provided
    diagnosis_line = f"\n**Root Cause**: {diagnosis}" if diagnosis else ""

    return f"""Analyze why no code template could solve this calculation question.

**Question**: {question}{options_section}
**Subfield**: {subfield}{diagnosis_line}
**Ground Truth**: {ground_truth}

**Skills Tried**:
- {skill_name}: {skill_answer}

In 1-2 sentences, explain what is missing: procedure/worked & checked example (weak_procedure_example), CHECK steps or CODE CONSTRAINTS (need_checks), or a new pattern for this calculation type (new_pattern).

Analysis:"""


# =============================================================================
# Full Diagnosis Prompt (classification + explanation together)
# =============================================================================

def build_full_gap_diagnosis_prompt(
    question: str,
    context: str,
    ground_truth: str,
    skill_name: str,
    specific_file: str,
    skill_answer: str,
    skill_explanation: str,
    skill_content: str = "",  # DEPRECATED: use all_skill_contents instead
    options: str = "",
    generated_code: str = "",  # The code that was generated
    execution_success: bool = True,  # Whether code executed successfully
    all_files = None,  # All files used
    non_common_files = None,  # Non-common files
    common_files = None,  # Common files
    all_skill_contents: dict = None  # NEW: Dict of file_path -> content for ALL files
) -> str:
    """
    Build full diagnosis prompt for Q0_gap case (PoT mode).

    This prompt does both classification AND explanation in one LLM call.
    Used by _diagnose_gap_case for comprehensive analysis.

    Args:
        question: The question text
        context: Question context
        ground_truth: Correct answer
        skill_name: Name of the skill that was used
        specific_file: Specific skill file that was used
        skill_answer: The wrong answer given by the skill (execution result or error)
        skill_explanation: The skill's explanation
        skill_content: DEPRECATED - single file content (for backward compatibility)
        options: Optional MC options
        generated_code: The Python code that was generated (PoT mode)
        execution_success: Whether the code executed successfully
        all_skill_contents: Dict mapping file_path -> content for ALL loaded files

    Returns:
        Full diagnosis prompt string
    """
    # Build skill content section - show ALL files' contents
    skill_content_section = ""

    # Prefer all_skill_contents (new), fall back to skill_content (deprecated)
    if all_skill_contents:
        content_parts = []
        for file_path, content in all_skill_contents.items():
            # Mark common vs specific files
            file_type = "[COMMON]" if (common_files and file_path in common_files) else "[SPECIFIC]"
            primary_marker = " (PRIMARY)"
            content_parts.append(f"""
### {file_path} {file_type}{primary_marker}
```markdown
{content}
```""")

        skill_content_section = f"""
**Skill Files Content** ({len(all_skill_contents)} files loaded):
{"".join(content_parts)}

Review each skill file to determine which one is responsible for the failure:
- "When to Use" section matches this calculation type
- "Procedure" section is present and complete
- WORKED EXAMPLE section shows step-by-step calculation with actual numbers
- CODE CONSTRAINTS section is present (no input(), no print() as last line, imports)
- CHECK steps or validation logic are included in the code
- COMMON files handle cross-cutting concerns (formatting, general patterns, visual elements read)
- SPECIFIC files handle subfield-specific logic
"""
    elif skill_content:
        # Backward compatibility: single file content
        skill_content_section = f"""
**Current Skill Content** ({specific_file or 'SKILL.md'}):
```markdown
{skill_content}
```

Review the skill structure to determine if:
- "When to Use" section matches this calculation type
- "Procedure" section is present and complete
- WORKED EXAMPLE section shows step-by-step calculation with actual numbers
- CODE CONSTRAINTS section is present (no input(), no print() as last line, imports)
- CHECK steps or validation logic are included in the code
"""
    else:
        skill_content_section = f"""
**Note**: Could not load skill content for {skill_name}/{specific_file}
"""

    options_section = f"\n**Options**: {options}" if options else ""

    # Build files section (for multi-file attribution)
    files_section = ""
    if all_files and len(all_files) > 1:
        files_list = []
        for f in all_files:
            file_type = "COMMON" if (common_files and f in common_files) else "SPECIFIC"
            primary_marker = " (PRIMARY)"
            files_list.append(f"  - {f} ({file_type}){primary_marker}")
        files_section = f"""
**Skill Files Used**:
{chr(10).join(files_list)}

Note: This question used multiple skill files. You need to determine which file is most responsible for the failure.
"""

    # Build code execution section
    code_section = ""
    if generated_code:
        execution_status = "✅ Executed successfully" if execution_success else "❌ Execution failed"
        code_section = f"""
**Generated Code**:
```python
{generated_code}
```
**Execution Status**: {execution_status}
"""

    return f"""Analyze why the code-based skill failed on this financial calculation question.

**Question**: {question}{options_section}
**Context**: {context if context else 'None'}
**Ground Truth**: {ground_truth}

**Skill Used**: {skill_name}/{specific_file}
**Skill Answer (WRONG)**: {skill_answer}
**Skill Explanation**: {skill_explanation}
{code_section}
{files_section}
{skill_content_section}

## CRITICAL INSTRUCTIONS

**READ THE GENERATED CODE CAREFULLY.** Understand the code logic and trace through the calculation step by step.

⚠️ **DO NOT introduce numbers or assumptions not present in the Context, Options, or Generated Code.**
- Only use values explicitly stated in the question/context
- Do not hallucinate intermediate results
- Do not assume values that are not provided

⚠️ **STRICT OCR DATA RULE - DO NOT GUESS OR MODIFY DATA:**
- Use the EXACT numbers as they appear in the Context (OCR output)
- **DO NOT** speculate that a number might be missing:
  - A percent sign (e.g., "5" might actually be "5%")
  - A decimal point (e.g., "50" might actually be "0.50")
  - A negative sign (e.g., "100" might actually be "-100")
  - Any other symbol or digit
- If the calculation using the EXACT OCR values and using the right method and steps don't match the Ground Truth, classify as **context_data_error**
- The skill cannot fix OCR errors - that's a data quality issue, not a skill issue

---

## Step 1: Classify the ERROR TYPE

First, determine what type of error occurred:

1. **mc_selection_error** - The calculation in the code is CORRECT, but the MC selector chose the wrong option.
   - Check: Does the numerical result match one of the options but the wrong one was selected?
   - Check: Is the code logic sound but the final answer mapping failed?

2. **context_data_error** - The calculation using EXACT OCR values is correct, but doesn't match Ground Truth.
   - This happens when OCR data has errors (missing %, wrong decimal, etc.)
   - Check: Is the code logic correct using EXACT context values, but GT seems inconsistent?
   - **IMPORTANT**: If you suspect OCR missed a symbol (%, decimal, negative sign) and the provided OCR data indeed lacks these features, classify this as `context_data_error`
   - DO NOT classify as logic_error just because you think the data "should" have been different

3. **execution_failed** - The code failed to execute (syntax error, runtime error, missing import, etc.)
   - Check: Is execution_status showing "❌ Execution failed"?
   - Identify the specific error: ZeroDivisionError, TypeError, SyntaxError, etc.

4. **logic_error** - The code has incorrect calculation logic.
   - Check: Is there a formula error, wrong variable usage, or incorrect procedure?
   - This is when the code runs but produces wrong results due to flawed logic.

---

## Step 2: Determine ROOT CAUSE (for logic_error and execution_failed only)

If error_type is "logic_error" or "execution_failed", classify the root cause:

1. **weak_procedure_example** - Pattern matches but procedure is incomplete or lacks worked & checked example.

2. **need_checks** - Pattern matches but missing CHECK steps, Common Bugs to Avoid, or code safety guards.
   - For execution_failed: missing guards like division by zero checks, type validation, etc.

3. **new_pattern** - No pattern covers this calculation type; needs a new skill file.

**Decision Guide**:
- mc_selection_error → root_cause should be "mc_selection" (special case, attribute to common/mc_selection.md or FORMATTING.md)
- context_data_error → root_cause should be "context_issue" (skip, cannot fix by skill refinement)
- execution_failed → Usually "need_checks" (add code safety) or "weak_procedure_example" (fix code template)
- logic_error → Use standard classification above (weak_procedure_example or need_checks or new_pattern)

---

## Step 3: File Attribution

Determine which skill file is responsible:
- Common files handle cross-cutting concerns (formatting, general patterns)
- Specific files handle domain-specific logic
- If the issue is in a common file, attribute to that common file
- If the issue is in specific logic, attribute to the specific file
- If unsure or files interact, prefer the specific file

---

Output format (JSON):
{{"error_type": "mc_selection_error" | "context_data_error" | "execution_failed" | "logic_error", "root_cause": "weak_procedure_example" | "need_checks" | "new_pattern" | "mc_selection" | "context_issue", "root_cause_file": "filename responsible for this failure", "explanation": "detailed analysis of what went wrong - trace through the code logic, explain the error, and describe what needs to be fixed in the skill file"}}

Analysis:"""


# =============================================================================
# Attribution-Only Prompt (for Q0_gap when enable_diagnosis=False)
# =============================================================================

def build_gap_attribution_only_prompt(
    question: str,
    context: str,
    ground_truth: str,
    skill_answer: str,
    generated_code: str = "",
    execution_success: bool = True,
    all_files: list = None,
    non_common_files: list = None,
    common_files: list = None,
    all_skill_contents: dict = None,
    options: str = ""
) -> str:
    """
    Build attribution-only prompt for Q0_gap case (PoT mode).

    Used when enable_diagnosis=False. Only determines which file should be
    responsible for fixing this case, without classifying the root cause.
    All cases will default to action='need_new_skill' (new_pattern).

    Args:
        question: The question text
        context: Question context
        ground_truth: Correct answer
        skill_answer: The wrong answer given by the skill
        generated_code: The Python code that was generated
        execution_success: Whether the code executed successfully
        all_files: All files that were loaded
        non_common_files: Non-common files (subfield-specific)
        common_files: Common files (cross-subfield)
        all_skill_contents: Dict mapping file_path -> content for ALL files
        options: Optional MC options

    Returns:
        Attribution-only prompt string
    """
    all_files = all_files or []
    non_common_files = non_common_files or []
    common_files = common_files or []
    all_skill_contents = all_skill_contents or {}

    options_section = f"\n**Options**: {options}" if options else ""

    # Build code execution section
    code_section = ""
    if generated_code:
        execution_status = "✅ Executed successfully" if execution_success else "❌ Execution failed"
        code_section = f"""
**Generated Code**:
```python
{generated_code}
```
**Execution Status**: {execution_status}
"""

    # Build files section
    files_section = ""
    if all_files:
        files_list = []
        for f in all_files:
            file_type = "COMMON" if f in common_files else "SPECIFIC"
            files_list.append(f"  - `{f}` ({file_type})")
        files_section = f"""
**Skill Files Used**:
{chr(10).join(files_list)}
"""

    # Build skill content section - show ALL files' contents
    skill_content_section = ""
    if all_skill_contents:
        content_parts = []
        for file_path, content in all_skill_contents.items():
            file_type = "[COMMON]" if file_path in common_files else "[SPECIFIC]"
            # Truncate content if too long
            truncated = content[:3000] + "..." if len(content) > 3000 else content
            content_parts.append(f"""
### {file_path} {file_type}
```markdown
{truncated}
```""")

        skill_content_section = f"""
**Skill Files Content** ({len(all_skill_contents)} files):
{"".join(content_parts)}
"""

    return f"""Determine which skill file should be responsible for fixing this failed case.

**Question**: {question}{options_section}
**Context**: {context if context else 'None'}
**Ground Truth**: {ground_truth}

**Skill Answer (WRONG)**: {skill_answer}
{code_section}
{files_section}
{skill_content_section}

## Task

Analyze the question and determine which ONE skill file is most responsible for this failure and should be updated to fix it.

**Guidelines**:
- Common files handle cross-cutting concerns (formatting, general patterns)
- Specific files handle domain-specific logic
- If the issue is in a common file, attribute to that common file
- If the issue is in specific logic, attribute to the specific file
- If unsure or files interact, prefer the specific file
- If multiple files are relevant, choose the PRIMARY one that should be fixed first

Output format (JSON only):
{{"attributed_file": "path/to/file.md", "reasoning": "brief explanation of why this file is responsible"}}

Analysis:"""
