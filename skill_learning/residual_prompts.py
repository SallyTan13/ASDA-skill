"""
Prompts for Residual Evidence Collection and Diagnosis.

This module contains all prompts used by ResidualEvidenceCollector for:
- Q0_gap classification (determining root cause)
- Q+_discover / Q0_gap explanation generation
"""

from typing import Optional, List


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
    options: str = ""
) -> str:
    """
    Build classification prompt for Q0_gap case.

    This prompt focuses on determining the ROOT CAUSE only (no detailed explanation).
    Used in batch classification for efficiency.

    Args:
        question: The question text
        ground_truth: Correct answer
        skill_name: Name of the skill that was used
        specific_file: Specific skill file that was used
        skill_answer: The wrong answer given by the skill
        skill_content: Optional skill file content for analysis
        options: Optional MC options

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

    return f"""Classify why the skill failed on this financial question and why we used this skill, question is still not solved correctly.

**Question**: {question}{options_section}
**Ground Truth**: {ground_truth}

**Skill Used**: {skill_name}/{specific_file}
**Skill Answer (WRONG)**: {skill_answer}
{skill_section}

Classify the root cause as ONE of:
1. **trigger_mismatch** - Pattern exists but "When to Use" didn't match
2. **incomplete_procedure** - Pattern matched but procedure is incomplete/unclear
3. **weak_example** - Procedure correct but example doesn't help
4. **capability_gap** - No pattern covers this topic

Output JSON only: {{"root_cause": "one_of_above"}}"""


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
    Build explanation prompt for Q+_discover case.

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

    return f"""Analyze why the wrong skill was selected for this question.

**Question**: {question}{options_section}
**Subfield**: {subfield}

**Skill Used (FAILED)**: {skill_name}/{specific_file}
- Answer: {skill_answer}

{solving_section}

**Ground Truth**: {ground_truth}

In 1-2 sentences, explain WHY the wrong skill was selected and what trigger keywords should be added.

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
    Build explanation prompt for Q0_gap case.

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

    return f"""Analyze why no skill could solve this question.

**Question**: {question}{options_section}
**Subfield**: {subfield}{diagnosis_line}
**Ground Truth**: {ground_truth}

**Skills Tried**:
- {skill_name}: {skill_answer}

In 1-2 sentences, explain what knowledge or procedure is missing.

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
    all_files: List[str] = None,
    non_common_files: List[str] = None,
    common_files: List[str] = None,
    all_skill_contents: dict = None  # NEW: Dict of file_path -> content for ALL files
) -> str:
    """
    Build full diagnosis prompt for Q0_gap case.

    This prompt does both classification AND explanation in one LLM call.
    Used by _diagnose_gap_case for comprehensive analysis.

    Args:
        question: The question text
        context: Question context
        ground_truth: Correct answer
        skill_name: Name of the skill that was used
        specific_file: Specific skill file that was used (primary attribution)
        skill_answer: The wrong answer given by the skill
        skill_explanation: The skill's explanation
        skill_content: DEPRECATED - single file content (for backward compatibility)
        options: Optional MC options
        all_files: All skill files used (for multi-file cases)
        non_common_files: Non-common (subfield-specific) files used
        common_files: Common (cross-cutting) files used
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
            primary_marker = " (PRIMARY)" if file_path == specific_file else ""
            content_parts.append(f"""
### {file_path} {file_type}{primary_marker}
```markdown
{content}
```""")

        skill_content_section = f"""
**Skill Files Content** ({len(all_skill_contents)} files loaded):
{"".join(content_parts)}

Review each skill file to determine which one is responsible for the failure:
- "When to Use" section matches this question type
- "Description" and "Procedure" sections are complete
- "Example" section helps with this case type
- COMMON files handle cross-cutting concerns (formatting, general patterns)
- SPECIFIC files handle subfield-specific logic (portfolio formulas, corporate finance)
"""
    elif skill_content:
        # Backward compatibility: single file content
        skill_content_section = f"""
**Current Skill Content** ({specific_file or 'SKILL.md'}):
```markdown
{skill_content}
```

Review the skill pattern structure to determine if:
- "When to Use" section matches this question type
- "Description" and "Procedure" sections are complete
- "Example" section helps with this case type
"""
    else:
        skill_content_section = f"""
**Note**: Could not load skill content for {skill_name}/{specific_file}
"""

    options_section = f"\n**Options**: {options}" if options else ""

    # Build files used section
    files_section = ""
    if all_files and len(all_files) > 1:
        files_list = []
        for f in all_files:
            file_type = "COMMON" if (common_files and f in common_files) else "SPECIFIC"
            primary_marker = " (PRIMARY ATTRIBUTION)" if f == specific_file else ""
            files_list.append(f"  - {f} ({file_type}){primary_marker}")
        files_section = f"""
**Skill Files Used**:
{chr(10).join(files_list)}

Note: This question used multiple skill files. You need to determine which file is most responsible for the failure.
"""
    else:
        files_section = f"""
**Skill File Used**: {specific_file}
"""

    return f"""Analyze why the skill failed on this financial question and determine the root cause.

**Question**: {question}{options_section}
**Context**: {context if context else 'None'}
**Ground Truth**: {ground_truth}

**Skill Used**: {skill_name}
{files_section}
**Skill Answer (WRONG)**: {skill_answer}
**Skill Explanation**: {skill_explanation}
{skill_content_section}
Before choosing the root cause, follow this order:

Identify the exact asked target.
- What exactly is the question asking for? Read the question and context carefully.
  Examples: a count, a direction, one option, one expression, one characteristic, one specific loss value, one of multiple legs, etc.
- Read the Skill Answer, Skill Explanation and Skill Used carefully and identify why the skill failed to solve the question.

Based on the skill content and the failed question, classify the root cause as ONE of:

1. **trigger_mismatch** 
   - Use this only if a suitable pattern clearly exists in the loaded files, but it was not the pattern that should have been applied, or the triggering conditions / "When to Use" guidance were too weak to select the right pattern.
   - This means the needed pattern exists in the skill contents, but the model didn't apply it or used the wrong pattern. 

2. **incomplete_procedure** 
   - The pattern was selected but "Description" or "Procedure" sections are missing necessary steps, key constraints, a critical comparison or are too vague. The skill covers the topic but the instructions are incomplete.

3. **weak_example** 
   - The pattern was selected and procedure seems correct, but the "Example" section doesn't help with this case type. A better example would help the model apply the procedure correctly.

4. **capability_gap** 
   - No existing pattern covers this topic/scenario. The question requires knowledge or procedures that are fundamentally different from what any skill provides.

**Decision Guide**:
- If a suitable pattern exists but wasn't matched or used the wrong pattern → trigger_mismatch
- If the pattern was matched but procedure is incomplete/unclear → incomplete_procedure
- If the pattern was matched and procedure is correct but example doesn't help → weak_example
- If no pattern covers this topic at all → capability_gap

Before finalizing, silently verify:
- Your explanation does NOT contradict the ground truth
- Your explanation identifies why question is not solved correctly and what the skill missed
- Your chosen root_cause matches the rules above
- Your chosen root_cause_file is one of the listed files above

**File Attribution** (if multiple files were used):
- Determine which specific file is most responsible for the failure
- Common files handle cross-cutting concerns
- Specific files handle subfield-specific logic
- If the issue is in a common file (e.g., wrong formatting rule, wrong general formula), attribute to that common file
- If the issue is in specific logic (e.g., wrong portfolio formula, wrong NPV calculation), attribute to the specific file

Output format (JSON):
{{"root_cause": "one of the above", "root_cause_file": "filename from the files used above", "explanation": "brief explanation of what's missing or needs improvement and why this file is responsible"}}

Analysis:"""


# =============================================================================
# Attribution-Only Prompt (for Q0_gap when enable_diagnosis=False)
# =============================================================================

def build_gap_attribution_only_prompt(
    question: str,
    context: str,
    ground_truth: str,
    skill_answer: str,
    all_files: List[str] = None,
    non_common_files: List[str] = None,
    common_files: List[str] = None,
    all_skill_contents: dict = None,
    options: str = ""
) -> str:
    """
    Build attribution-only prompt for Q0_gap case (non-PoT mode).

    Used when enable_diagnosis=False. Only determines which file should be
    responsible for fixing this case, without classifying the root cause.
    All cases will default to action='need_new_skill' (capability_gap).

    Args:
        question: The question text
        context: Question context
        ground_truth: Correct answer
        skill_answer: The wrong answer given by the skill
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