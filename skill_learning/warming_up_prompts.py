"""
Skill Warming Up Prompts - V3

Prompts for generating skills from failure clusters.
Separated for easy modification.
"""

import os

# ============================================================
# Error Type Taxonomy (aligned with v2)
# ============================================================

# For file naming (snake_case)
# Note: Type 10 exists only when PoT is used (see signature_prompts.get_error_taxonomy(pot_mode=True)).
ERROR_TYPE_NAMES = {
    1: "visual_evidence",
    2: "wrong_method_selection",
    3: "concept_confusion",
    4: "missed_multi_step",
    5: "unit_currency_percent",
    6: "missed_constraints",
    7: "wrong_targets",
    8: "wrong_output_format",
    9: "others",
    10: "code_execution_error"
}

# For prompt descriptions (human-readable)
ERROR_TYPE_DESCRIPTIONS = {
    1: "visual evidence misread or not used",
    2: "wrong method/formula/procedure selected",
    3: "concept confusion at definition/intuitive level",
    4: "incomplete multi-step reasoning chain",
    5: "unit/currency/percent conversion errors",
    6: "explicit constraints not applied",
    7: "misread question or answered wrong target",
    8: "correct reasoning but wrong output format",
    9: "other errors",
    10: "code execution error (PoT-specific)"
}

# Error types routed to common/ (cross-subfield procedures). Type 10 is PoT-only.
COMMON_ERROR_TYPES = {1, 6, 8}

# ============================================================
# Skill File Split Strategy
# ============================================================
# Skills are split by file structure during warming up:
# - common/{error_type}.md      → Cross-subfield patterns (COMMON_ERROR_TYPES: 1, 6, 8; type 10 only in PoT)
# - {subfield}/{error_type}.md  → Subfield-specific patterns
#
# This split is FIXED. During learning phase, only content is refined.

# ============================================================
# Skill Generation Prompt (for individual skill files)
# ============================================================
SKILL_GEN_PROMPT = """You are a financial reasoning skills engineer. Your task is to analyze failure \
cases from a financial QA benchmark and produce reusable SKILL PATTERNS that \
prevent these failures in future unseen questions.

## Cluster Info

- Subfield: {subfield}
- Error Type: {error_type} — {error_description}

## Failure Cases (batch of ≤ 10)

{cases_text}

## Instructions

1. Analyze ALL failure cases above.
2. Identify EVERY distinct problem pattern. Do NOT force them into a single pattern.
3. For each pattern, produce a skill section following the format below.
4. Each pattern must be GENERAL — it must help with future unseen questions, \
not just fix the specific cases above.
5. Keep concise and clear. Avoid redundant patterns.

## Required Output Format

(Repeat for each distinct pattern found)

## Pattern: {{concise_pattern_name}}

**Description:** {{1-2 sentence description of the recurring knowledge gap}}

**When to Use:** {{1 sentence description of when to use this, and trigger keywords, concise}}

**Procedure:**
(Tailor steps to the error type:
- Concept confusion → include correct concept definitions, clarify the misconception, and show how to apply the concept to solve questions
- Wrong method selection → specify the correct method/formula, explain why alternatives are wrong, and outline the solution steps
- Missed multi-step → lay out the complete reasoning chain with all intermediate steps in order
- Unit/currency/percent → state exact conversion rules and flag common unit/scale traps
- Visual evidence → describe how to correctly locate and read the relevant data from the source
- Missed constraints → add explicit constraint-checking steps before finalizing the answer
- Wrong targets → describe how to parse the question wording to identify the exact target
- Wrong output format → specify the required output format and mapping rules
- Code execution error (PoT-specific) → specify correct code pattern, highlight common bugs (print() vs expression, missing imports, sign conventions), and show correct implementation)
1. {{step 1}}
2. {{step 2}}
3. {{step 3}}
...

**Example (sanitized):**
> **Scenario:** {{generic scenario with DIFFERENT numbers/names — NOT copied from cases}}
> **Wrong approach:** {{common mistake pattern}}
> **Correct approach:** {{step-by-step correct reasoning}}

## Rules

1. NEVER copy original questions, answers, or explanations verbatim — data leakage.
2. Focus on PROCEDURE. Steps must be concrete enough to follow mechanically.
3. Include verification as the final procedure step(s) to catch known traps.
4. Extract the GENERAL principle from specific failures.
5. Every procedure step must be grounded in failure evidence.
6. If only 1 case supports a pattern, keep it concise.
"""

# ============================================================
# Skill Generation Prompt - PoT Version (Error Type 10)
# ============================================================
SKILL_GEN_PROMPT_POT = """You are a financial reasoning skills engineer. Your task is to analyze failure \
cases from arithmetic financial questions (solved using Program of Thought / Python code) and produce \
reusable SKILL PATTERNS that prevent these failures in future unseen questions. 
Write this as a DETAIL file with calculation patterns, code templates, and worked examples.

## Cluster Info

- Subfield: {subfield}
- Error Type: {error_type} — {error_description}
- **Mode:** Program of Thought (PoT) — questions are solved by generating and executing Python code

## Failure Cases

{cases_text}

## Instructions

1. Analyze ALL failure cases above.
2. Identify EVERY distinct problem pattern. Do NOT force them into a single pattern.
3. For each pattern, produce a skill section following the format below.
4. Each pattern must be GENERAL — it must help with future unseen questions, \
not just fix the specific cases above.
5. **CRITICAL for PoT:** Include PYTHON CODE EXAMPLES showing correct implementations.
6. Keep concise and clear. Avoid redundant patterns.

## Required Output Format

(Repeat for each distinct pattern found)

## Pattern: {{concise_pattern_name}}

**Description:** {{1-2 sentence description of the recurring code error or knowledge gap}}

**When to Use:** {{1 sentence description of when this pattern applies, question types, and trigger keywords, concise}}

**Procedure:**
1. {{Formula: Mathematical formula}}
2. {{step 1 - what to check or compute}}
3. {{step 2 - how to structure the calculation}}
4. {{step 3 - how to return the result}}
...

**Code Example:**

**Scenario:** {{generic arithmetic scenario with DIFFERENT numbers — NOT copied from cases}}
**Correct Code:**
```python
# Step-by-step calculation with clear variable names
# MUST end with expression (not print)
```

**Common Bugs to Avoid:**
- {{Bug 1: e.g., using print() instead of expression on last line}}
- {{Bug 2: e.g., sign convention errors (negative cash flows)}}
- {{Bug 3: e.g., missing imports like math, numpy}}

## Rules

1. NEVER copy original questions, answers, or code verbatim — data leakage.
2. Focus on CODE PATTERNS. Show concrete Python examples for each pattern.
3. Highlight common bugs explicitly (print vs expression, sign errors, unit conversions).
4. Include verification/sanity check steps in the procedure.
5. Extract the GENERAL principle from specific code failures.
6. Every code example must be grounded in failure evidence.
7. If only 1 case supports a pattern, keep it concise.
"""


# ============================================================
# Prompt Selector Function
# ============================================================
def get_skill_gen_prompt(error_type: int) -> str:
    """
    Select the appropriate skill generation prompt based on error type and POT_MODE.

    Args:
        error_type: Error type ID (1-9 for non-PoT; 1-10 for PoT). Type 10 exists only
                    when failure signatures were produced with pot_mode=True (see signature_prompts).

    Returns:
        Appropriate prompt template string

    Usage:
        prompt = get_skill_gen_prompt(error_type).format(
            subfield=subfield,
            error_type=error_name,
            error_description=error_desc,
            cases_text=cases_text
        )

    Environment Variables:
        POT_MODE: If 'true', forces use of PoT prompt for ALL error types
                  (for arithmetic questions that are always solved with code)
    """
    # Check if POT_MODE is enabled (for arithmetic questions)
    pot_mode = os.getenv("POT_MODE", "false").lower() == "true"

    # Use PoT prompt if:
    # 1. POT_MODE=true (all arithmetic questions use code), OR
    # 2. error_type=10 (code execution error specifically)
    if pot_mode or error_type == 10:
        return SKILL_GEN_PROMPT_POT
    else:  # Non-arithmetic (traditional reasoning)
        return SKILL_GEN_PROMPT

# ============================================================
# Skill Split Prompt (Optional - groups similar patterns)
# ============================================================
SPLIT_PROMPT = """You are organizing a skill file by grouping similar patterns together.

## Original Skill File

**File Path:** {file_path}
**Subfield:** {subfield}
**Error Type:** {error_type}

**Content:**
{content}

## Task

Analyze the patterns in this skill file and determine if they should be split into multiple files based on semantic similarity.

### Split Criteria
- Group patterns that address the SAME conceptual area (e.g., risk metrics, return calculations, valuation methods)
- Each group should have 2-5 patterns (if possible)
- Patterns in the same group should be useful together when solving a question
- If all patterns are already cohesive (single topic), output NO_SPLIT

### Output Format

If NO split needed:
```
NO_SPLIT
Reason: [1 sentence explanation]
```

If split IS needed, output each group:
```
## SPLIT_GROUP: {{group_name}}

**Topic:** {{1 sentence description of what this group covers}}

**Patterns:**
[Copy the full pattern content for each pattern in this group]
```

## Rules

1. Preserve ALL pattern content exactly (no modifications)
2. Each pattern must appear in exactly ONE group
3. Group names should be lowercase with underscores (e.g., risk_metrics, return_calculations)
4. Keep groups cohesive - patterns should be related enough to load together
5. If file has ≤3 patterns, prefer NO_SPLIT unless they are clearly unrelated
"""

# ============================================================
# Refinement Prompt (for updating existing skill files)
# ============================================================
REFINEMENT_PROMPT = """You are refining a skill file for {subfield} — {error_type}.

## Existing Patterns (summaries)

{pattern_summaries}

## New Failure Cases (batch {batch_num}, ≤ 10 cases)

{cases_text}

## Instructions

1. For each new case, check if its root cause is addressed by an existing pattern.
2. If a case fits an existing pattern BUT the procedure needs improvement, \
output a REFINED version of that pattern (use "## REFINED Pattern: {{exact name}}").
3. If a case reveals a genuinely NEW knowledge gap, output a NEW pattern \
(use "## NEW Pattern: {{name}}").
4. If ALL cases fit existing patterns with no refinement needed, respond: NO_CHANGES

## Output Format

Use these prefixes to distinguish refined vs new:

## REFINED Pattern: {{exact existing pattern name}}

**Description:** {{1-2 sentence description of the recurring knowledge gap}}

**When to Use:** {{1 sentence description of when to use this, and trigger keywords}}

**Procedure:**
1. {{step 1}}
2. {{step 2}}
3. {{step 3}}
...

**Example (sanitized):**
> **Scenario:** {{generic scenario with DIFFERENT numbers/names}}
> **Wrong approach:** {{common mistake pattern}}
> **Correct approach:** {{step-by-step correct reasoning}}

## NEW Pattern: {{new pattern name}}

(Same format as above: Description, When to Use, Procedure, Example)

## Rules

- Only output patterns that are REFINED or NEW. Do not reproduce unchanged patterns.
- For REFINED patterns, use the EXACT name from the existing patterns list.
- Same format rules as initial generation (no data leakage, general principles, etc.).
"""


# ============================================================
# Refinement Prompt for PoT (for updating existing skill files)
# ============================================================
REFINEMENT_PROMPT_PoT = """You are refining a skill file for {subfield} — {error_type}.
**Mode:** Program of Thought (PoT) — questions are solved by generating and executing Python code.

## Existing Patterns (summaries)

{pattern_summaries}

## New Failure Cases (batch {batch_num})

{cases_text}

## Instructions

1. For each new case, check if its root cause is addressed by an existing pattern.
2. If a case fits an existing pattern BUT the procedure or code example needs improvement, \
output a REFINED version of that pattern (use "## REFINED Pattern: {{exact name}}").
3. If a case reveals a genuinely NEW knowledge gap or code error pattern, output a NEW pattern \
(use "## NEW Pattern: {{name}}").
4. If ALL cases fit existing patterns with no refinement needed, respond: NO_CHANGES
5. **CRITICAL for PoT:** REFINED and NEW patterns must include PYTHON CODE EXAMPLES (correct vs bugs to avoid).

## Output Format

Use these prefixes to distinguish refined vs new:

## REFINED Pattern: {{exact existing pattern name}}

**Description:** {{1-2 sentence description of the recurring code error or knowledge gap}}

**When to Use:** {{1 sentence description of when to use this, question types, and trigger keywords}}

**Procedure:**
1. {{Formula: Mathematical formula if applicable}}
2. {{step 1 - what to check or compute}}
3. {{step 2 - how to structure the calculation}}
4. {{step 3 - how to return the result}}
...

**Code Example:**

**Scenario:** {{generic arithmetic scenario with DIFFERENT numbers — NOT copied from cases}}
**Correct Code:**
```python
# Step-by-step calculation with clear variable names
# MUST end with expression (not print)
```

**Common Bugs to Avoid:**
- {{Bug 1: e.g., using print() instead of expression on last line}}
- {{Bug 2: e.g., sign convention errors (negative cash flows)}}
- {{Bug 3: e.g., missing imports like math, numpy}}

## NEW Pattern: {{new pattern name}}

(Same format as above: Description, When to Use, Procedure, Code Example with Scenario / Correct Code / Common Bugs to Avoid)

## Rules

- Only output patterns that are REFINED or NEW. Do not reproduce unchanged patterns.
- For REFINED patterns, use the EXACT name from the existing patterns list.
- Focus on CODE PATTERNS. Every pattern must have concrete Python examples and Common Bugs to Avoid.
- NEVER copy original questions, answers, or code verbatim — no data leakage.
- Code examples must end with an expression (not print); highlight this in Common Bugs to Avoid when relevant.
"""


# ============================================================
# SKILL.md Navigation File Prompt (V3 - Updated Structure)
# ============================================================
SKILL_MD_PROMPT = """Generate a SKILL.md navigation file for a non-arithmetic financial \
reasoning skill set. The PRIMARY purpose is to provide clear navigation to the right skill file.

## Generated Skill Files

{file_inventory}

## Requirements

1. Start with YAML frontmatter:
```yaml
---
name: famma-non-arithmetic-v1
description: Skills for non-arithmetic financial reasoning covering concept confusion, visual evidence interpretation, and domain-specific patterns
version: 1.0
---
```

2. Add a brief title and 1-2 sentence description.

3. Add the "Available Skill Files" section:
```markdown
## Available Skill Files

You have access to detailed skill files for each financial subfield. **Request files as needed** using the `load_skill_file` tool.
```

4. Add a "File Index" table with this EXACT format:
```markdown
### File Index

| File Path | Subfield | Error Type | Key Patterns |
|-----------|----------|------------|--------------|
| `common/visual_evidence.md` | Cross-subfield | Visual evidence misread | Pattern1, Pattern2, Pattern3 |
| `portfolio_management/concept_confusion.md` | Portfolio management | Concept confusion | Pattern1, Pattern2 |
...
```

For the "Key Patterns" column:
- List the actual pattern names from each skill file

5. Add a "How to Use" section with ONE example:
```markdown
## How to Use

### Step 1: Identify the Question Type
Read the question and determine:
- Which financial subfield? (portfolio management, derivatives, fixed income, etc.)
- What type of error is likely? (concept confusion, visual evidence, etc.)

### Step 2: Request the Relevant Skill File
Use the `load_skill_file` tool to request the appropriate file based on the File Index above.

### Step 3: Apply the Pattern
1. Find the matching pattern in the loaded skill file
2. Follow the reasoning steps provided
3. Verify your answer against the pattern's key insights

### Example

**Question**: "Based on Figure 1, which portfolio lies on the efficient frontier?"

**Step 1**: This is a portfolio management question involving visual evidence (reading a chart).

**Step 2**: Request `common/visual_evidence.md` for chart reading patterns, and `portfolio_management/concept_confusion.md` for efficient frontier concepts.

**Step 3**: Apply the "Systematic Tabular Data Extraction" pattern from visual_evidence.md to correctly read the chart values, then apply the "Mean-Variance Dominance" pattern to identify the efficient frontier.
```

6. Add a brief "When NOT to Use" section (3-5 bullets).

7. Keep the total SKILL.md concisely.

Generate the SKILL.md content now.
"""


# ============================================================
# SKILL.md Navigation File Prompt (PoT)
# ============================================================
SKILL_MD_PROMPT_PoT = """Generate a SKILL.md navigation file for an arithmetic financial reasoning skill set \
(Program of Thought: Python code). The PRIMARY purpose is to help the agent navigate to the right skill file \
and apply code patterns correctly.

## Generated Skill Files (input)

{file_inventory}

## Output Structure

**1. YAML frontmatter** — use this exact structure:
```yaml
---
name: famma-arithmetic-v1
description: Skills for arithmetic financial reasoning (PoT): concept confusion, visual evidence, domain patterns
version: 1.0
---
```

**2. Title and description** — One brief title plus 1–2 sentences describing the skill set.

**3. Available Skill Files** — One short paragraph stating that detailed skill files exist per subfield \
and must be requested via the `load_skill_file` tool.

**4. File Index table** — Use this EXACT table format. For "Key Patterns", list the actual pattern names from each file.
```markdown
### File Index

| File Path | Subfield | Error Type | Key Patterns |
|-----------|----------|------------|--------------|
| `common/visual_evidence.md` | Cross-subfield | Visual evidence misread | Pattern1, Pattern2, Pattern3 |
| `portfolio_management/concept_confusion.md` | Portfolio management | Concept confusion | Pattern1, Pattern2 |
```
(Add one row per generated skill file; Key Patterns = comma-separated pattern names from that file.)

**5. How to Use** — Three steps plus one short example (see below).

**6. Critical Code Constraints** — MUST / MUST NOT / Available Libraries (see below).

**7. When NOT to Use** — 3–5 bullets on when this skill set does not apply.

Keep the whole SKILL.md concise.

---

## How to Use (content to generate)

**Step 1: Identify question type**  
Read the question and determine which financial subfield and error type it matches (e.g. by keywords, \
question format, or domain). Map to one or more entries in the File Index.

**Step 2: Request relevant skill file**  
Use the `load_skill_file` tool with the File Path from the File Index.

**Step 3: Apply pattern from the loaded file**  
1. Find the matching pattern in the skill file  
2. Follow the procedure and copy the code template structure  
3. Replace placeholders with values from the question  
4. Ensure the final line is an expression (not `print()`), so eval() can capture the result  

**Example**  
- *Question:* "Based on Figure 1, which portfolio lies on the efficient frontier?"  
- *Step 1:* Portfolio management + visual evidence (chart).  
- *Step 2:* Request `common/visual_evidence.md` and `portfolio_management/concept_confusion.md`.  
- *Step 3:* Apply "Systematic Tabular Data Extraction" to read the chart, then "Mean-Variance Dominance" for the frontier.

---

## Critical Code Constraints (ALWAYS FOLLOW)

**Your code MUST:**  
- End with a variable name or expression (for eval() to capture)  
- Put all imports at the top (e.g. `import numpy as np`)  
- Define every variable before use  
- Use explicit values from the question  

**Your code MUST NOT:**  
- Use `input()` or other interactive functions  
- Use `print()` as the last line (returns None)  
- Use undefined variables  
- Refer to example values without redefining them in code  

**Available libraries:**  
- `import math` — standard library  
- `import numpy as np` — numerical operations  
- `from scipy.stats import norm` — normal distribution (e.g. Black-Scholes)  
- `from scipy.optimize import brentq` — root finding (e.g. IRR)  

---

Generate the full SKILL.md content now.
"""


# ============================================================
# File Inventory Format (used in SKILL_MD_PROMPT)
# ============================================================
def format_file_inventory(file_info_list: list) -> str:
    """
    Format file information for the SKILL_MD_PROMPT.

    Args:
        file_info_list: List of dicts with keys:
            - file_path: str (e.g., "common/visual_evidence.md")
            - subfield: str
            - error_type: str
            - patterns: list of pattern names
            - case_count: int

    Returns:
        Formatted string for the prompt
    """
    lines = []
    for info in file_info_list:
        patterns = info.get('patterns', [])
        if patterns:
            pattern_str = ", ".join(patterns)  # All patterns, no truncation
        else:
            pattern_str = "Patterns pending"

        lines.append(f"- `{info['file_path']}`: {info['subfield']} / {info['error_type']}")
        lines.append(f"  Patterns: {pattern_str}")
        lines.append(f"  Cases: {info.get('case_count', 0)}")
        lines.append("")

    return "\n".join(lines)
