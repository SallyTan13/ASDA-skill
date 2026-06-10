"""
Optimizer Prompts for PoT Mode - Prompts for TextualOptimizer (Code-based Skills)

Separated for easy modification and versioning.
Focus on code templates, worked examples, and code constraints.
"""

# ============================================================================
# SKILL REFINEMENT PROMPT - For Q+/Q- evidence-based refinement (PoT Mode)
# ============================================================================
SKILL_REFINEMENT_PROMPT_POT = """You are a code-based skill refinement expert. Your task is to improve a financial calculation skill file based on evidence from actual usage.

**Skill File Being Refined:** `{skill_file}`
**Skill Set:** {skill_set_name}

**Current Skill Content:**
```markdown
{current_skill}
```

**Evidence from Usage:**

**Positive Cases (Q+):** {num_positive} cases where the skill FIXED baseline failures
{positive_evidence}

**Negative Cases (Q-):** {num_negative} cases where the skill CAUSED regressions
{negative_evidence}

**Your Task:**
Compare Q+ and Q- cases: what went right vs what went wrong, and refine the skill from both sides.
- From **Q+ (fixes):** Identify what pattern or procedure helped — consolidate and strengthen these so fixes are more reliable.
- From **Q- (regressions):** Identify what mistake or over-application caused harm — add guards, anti-patterns, or scope limits to reduce regressions.

Refine the skill file to:
1. **Consolidate fixes** — Strengthen and generalize patterns that worked (from Q+)
2. **Reduce regressions** — Add guards, anti-patterns, refine "when to use" or worked examples from Q- evidence
3. **Improve precision** — Make patterns apply only when they truly help (contrast helps avoid over-application)

**CRITICAL GUIDELINES FOR POT MODE:**
1. **Refining existing patterns** — From Q+ and Q- evidence:
   - Strengthen code templates that worked (from Q+)
   - Add CHECK steps, validation logic or Modify worked examples for regressions (from Q-)
   - Refine "When to Use" for better trigger precision
   - Add "Common Bugs to Avoid" section from Q- cases
   - Focus on the output formatting, sometimes the answer is right but output format is not the same as the groundtruth

2. **Adding new patterns** — If evidence reveals a new calculation type and previous patterns cannot solve it:
   - Create a NEW pattern section following the template above
   - Include complete code template with imports
   - Add worked example with actual numbers
   - Add CHECK steps and common bugs section
   - Focus on the general calculation approach, not specific cases

3. **AVOID OVERFITTING:**
   - DO NOT copy specific question text from evidence
   - DO extract general calculation patterns and formulas
   - Worked examples must use DIFFERENT numbers than evidence cases
   - Code templates must work on NEW, UNSEEN questions
   - CHECK steps should be general validation logic, not case-specific
   - Skills should be general and can be transferred to other questions

4. **INFERENCE-TIME CONSTRAINTS:**
   The skill you generate will be used during INFERENCE when **ground truth is NOT available**.
   - DO NOT write patterns that say "check ground truth format" — the model won't have access to it
   - Format decisions must be based on **QUESTION TEXT** and **ANSWER OPTIONS** only
   - Replace "ground truth shows X format" with "answer options show X format" or "question asks for X"
   - For output format patterns:
     - Check if OPTIONS contain % symbols → use percentage format
     - Check if OPTIONS are pure decimals → use decimal format
     - Check if QUESTION explicitly asks for "percentage" or "as a %" → use percentage format
   - The model only has: question, context, and options (for MC questions)

**Output Format:**
Output ONLY the patterns that need changes. Use these markers to distinguish refined vs new:

For patterns that need refinement (based on Q+ or Q- evidence):
```
## REFINED Pattern: {{exact_existing_pattern_name}}

**Description:** {{updated description}}

**When to Use:** {{updated trigger conditions}}

**Procedure:**
1. {{updated step}}
...

**Worked Example:**
**Question:** {{example}}
```python
# Step-by-step calculation with clear variable names
# MUST end with expression (not print)
```

**Common Bugs to Avoid:**
- {{specific bug pattern from Q- evidence}}
- {{another common mistake}}

**CHECK Steps:**
- If {{condition}}, verify {{what to check}}
- Assert {{validation logic}} (e.g., "assert npv >= 0 or explicitly shorting")
```

For new patterns (if evidence reveals new calculation types):
```
## NEW Pattern: {{new_pattern_name}}

**Description:** {{description}}

**When to Use:** {{trigger conditions}}

**Procedure:**
1. {{step}}
...

**Worked Example:**
**Question:** {{example}}
```python
# Step-by-step calculation with clear variable names
# MUST end with expression (not print)
```

**Common Bugs to Avoid:**
- {{specific bug pattern from Q- evidence}}
- {{another common mistake}}

**CHECK Steps:**
- If {{condition}}, verify {{what to check}}
- Assert {{validation logic}} (e.g., "assert npv >= 0 or explicitly shorting")
```

If NO changes are needed:
```
NO_CHANGES
Reason: The current skill already addresses all Q+ and Q- cases effectively.
```

**IMPORTANT:**
- For REFINED patterns, use the EXACT pattern name from the current skill
- Only output patterns that actually need changes
- Unchanged patterns will be preserved automatically

**REMEMBER:** Extract calculation patterns and formulas, NOT specific questions. The skill must generalize to NEW questions.

Now provide the incremental changes:
"""


# ============================================================================
# SAFETY REFINEMENT PROMPT POT - V2 Safety Phase with Contrastive Q+ (PoT Mode)
# ============================================================================
SAFETY_REFINEMENT_PROMPT_POT = """You are a code-based skill refinement expert. Your task is to improve a financial calculation skill file while carefully preserving what already works.

**Skill File Being Refined:** `{skill_file}`
**Skill Set:** {skill_set_name}

**Current Skill Content:**
```markdown
{current_skill}
```

---

## ⚠️ CONSTRAINTS (from Q⁺ - DO NOT BREAK)

These {num_positive} cases currently work correctly with this skill. You MUST preserve this behavior:

{positive_evidence}

**Why they work:** The current code templates and procedures successfully handle these calculations. Any changes you make must NOT break them.

---

## 🔧 REGRESSIONS TO FIX (from Q⁻)

These {num_negative} cases are failing and need to be fixed:

{negative_evidence}

---

## Your Task

Fix the Q⁻ regressions while **preserving Q⁺ correctness**.

**Key Principle:** This is a SAFETY refinement. The goal is to reduce regressions WITHOUT breaking existing fixes.

**Strategy:**
1. **Analyze Q⁺ first** — Understand WHY these calculations work. What code patterns or procedures are helping them?
2. **Analyze Q⁻ next** — Identify what's causing the regressions. Is it a wrong formula? Missing validation? Over-application?
3. **Find safe modifications** — Add CHECK steps, guards, or refine scope that fix Q⁻ WITHOUT affecting Q⁺

**CRITICAL GUIDELINES FOR POT MODE:**
1. **Preserve Q⁺ code patterns** — Do NOT modify code templates that are working for Q⁺ cases
2. **Add CHECK steps for Q⁻** — Add validation logic that catches Q⁻ failure modes
3. **Refine "When to Use"** — Make trigger conditions more precise to exclude Q⁻ failure cases
4. **Add "Common Bugs to Avoid"** — Document the Q⁻ failure patterns explicitly
5. **Adding new patterns** — If evidence reveals a new calculation type and even refined patterns cannot solve completely:
   - Create a NEW pattern section following the template above
   - Include complete code template with imports
   - Add worked example with actual numbers
   - Add CHECK steps and common bugs section
   - Focus on the general calculation approach, not specific cases

5. **INFERENCE-TIME CONSTRAINTS:**
   The skill you generate will be used during INFERENCE when **ground truth is NOT available**.
   - DO NOT write patterns that say "check ground truth format" — the model won't have access to it
   - Format decisions must be based on **QUESTION TEXT** and **ANSWER OPTIONS** only
   - The model only has: question, context, and options (for MC questions)

**AVOID OVERFITTING:**
- DO NOT copy specific question text from evidence
- DO extract general calculation patterns and formulas
- Worked examples must use DIFFERENT numbers than evidence cases
- Code templates must work on NEW, UNSEEN questions
- CHECK steps should be general validation logic, not case-specific
- Skills should be general and can be transferred to other questions

**Output Format:**
Output ONLY the patterns that need changes. Use these markers:

For patterns that need refinement:
```
## REFINED Pattern: {{exact_existing_pattern_name}}

**Description:** {{updated description}}

**When to Use:** {{updated trigger conditions}}

**When NOT to Use:** {{conditions where this pattern should NOT apply — from Q- analysis}}

**Procedure:**
1. {{updated step}}
...

**Worked Example:**
**Question:** {{example}}
```python
# Step-by-step calculation with clear variable names
# MUST end with expression (not print)
```

**Common Bugs to Avoid:**
- {{specific bug pattern from Q- evidence}}
- {{another common mistake}}

**CHECK Steps:**
- If {{condition}}, verify {{what to check}}
- Assert {{validation logic}} (e.g., "assert npv >= 0 or explicitly shorting")
```

For new patterns (if evidence reveals new calculation types):
```
## NEW Pattern: {{new_pattern_name}}

**Description:** {{description}}

**When to Use:** {{trigger conditions}}

**Procedure:**
1. {{step}}
...

**Worked Example:**
**Question:** {{example}}
```python
# Step-by-step calculation with clear variable names
# MUST end with expression (not print)
```

**Common Bugs to Avoid:**
- {{specific bug pattern from Q- evidence}}
- {{another common mistake}}

**CHECK Steps:**
- If {{condition}}, verify {{what to check}}
- Assert {{validation logic}} (e.g., "assert npv >= 0 or explicitly shorting")
```

If NO changes are needed (Q- cases are edge cases that cannot be fixed without breaking Q+):
```
NO_CHANGES
Reason: Fixing Q- cases would require changes that break Q+ cases. The current skill is optimal.
```

**REMEMBER:** Safety first. If you cannot fix Q- without risking Q+, prefer NO_CHANGES. The skill must generalize to NEW questions.

Now provide the incremental changes:
"""


# ============================================================================
# SKILL.MD ROUTING UPDATE PROMPT - For Q+_discover cases (router mismatch)
# ============================================================================
SKILL_MD_ROUTING_PROMPT_POT = """You are a skill routing expert. Your task is to update the SKILL.md navigation file so that the router correctly selects the right code template files.

**Current SKILL.md Content:**
```markdown
{current_skill_md}
```

**Routing Issues (Q+_discover Evidence):**

These cases were solved by a DIFFERENT skill file than the one selected:

{discover_evidence}

**Your Task:**

Update the SKILL.md file to improve routing accuracy. Focus on:

1. **File Index Table** — Update the "When to Use" column for affected files:
   - Add keywords from Q+_discover cases that should trigger this file
   - Make triggers more specific (e.g., "NPV calculation with cash flow series" not just "NPV")
   - Include calculation type keywords (e.g., "geometric return", "risk premium", "merger valuation")

2. **Routing Intelligence Section** — Add guidance for:
   - When to request multiple files (e.g., "For merger questions, request both CORPORATE_FINANCE and VALUATION")
   - How to distinguish between similar calculation types
   - Keywords that indicate specific code templates

3. **Keep Structure** — Maintain the existing format:
   - File Index table with columns: File Path | When to Use
   - Progressive Disclosure Workflow section
   - CODE CONSTRAINTS section (applies to all files)
   - Routing Intelligence section

**CRITICAL RULES:**

- DO NOT add or remove files from the File Index (only update "When to Use" descriptions)
- DO NOT change the CODE CONSTRAINTS section
- DO add specific calculation type keywords from Q+_discover evidence
- DO make routing triggers more precise and distinctive

**Output Format:**

Provide the COMPLETE updated SKILL.md file in markdown format.

Updated SKILL.md:
"""


# ============================================================================
# NEW SKILL CREATION PROMPT - For Q0_gap with new_pattern root cause
# ============================================================================
NEW_SKILL_CREATION_PROMPT_POT = """You are a financial calculation expert. Create a new skill file for a calculation pattern that is NOT covered by existing skills.

**Subfield:** {subfield}
**Gap Evidence:** Cases where no existing pattern and code template could solve the problem

{gap_evidence}

**Diagnosis Summary:** {diagnosis_summary}

**Your Task:**

Create a NEW skill file following the PoT (Program of Thought) pattern structure.

**Structure Required:**

```markdown
# {{Subfield}} — {{Calculation Type}}

## CODE CONSTRAINTS (MANDATORY)

**Your generated code MUST:**
- ✅ End with variable name or expression (for eval() to capture)
- ✅ Include ALL necessary imports at the top
- ✅ Define ALL variables before use
- ✅ Use explicit values from the question

**Your generated code MUST NOT:**
- ❌ Use input() or any interactive functions
- ❌ Use print() as the last line (returns None)
- ❌ Use variables without defining them first

**Available libraries (must import if used):**
- import math
- import numpy as np
- from scipy.stats import norm
- from scipy.optimize import brentq

## Pattern: {{Pattern Name}}

**Description:** {{updated description}}

**When to Use:** {{updated trigger conditions}}

**Procedure:**
1. {{updated step}}
...

**Worked Example:**
**Question:** {{example}}
```python
# Step-by-step calculation with clear variable names
# MUST end with expression (not print)
```

**Common Bugs to Avoid:**
- {{specific bug pattern from Q- evidence}}
- {{another common mistake}}

**CHECK Steps:**
- If {{condition}}, verify {{what to check}}
- Assert {{validation logic}} (e.g., "assert npv >= 0 or explicitly shorting")
```

**CRITICAL GUIDELINES:**

1. **Focus on the calculation pattern** — Extract the general formula/approach from gap evidence
2. **Worked example with actual numbers** — Show step-by-step calculation with concrete values
3. **CHECK steps** — Add validation logic to catch common mistakes
4. **Avoid overfitting** — Use DIFFERENT numbers than gap evidence cases

**For SKILL.md Entry:**
Also provide a SKILL.md table entry at the end, include:
```
SKILL_MD_ENTRY: | `{subfield_folder}/{{filename}}.md` | {{Subfield}} | {{Calculation Type}} | {{Pattern1}}, {{Pattern2}} |
```

**Output Format:**

First, provide the complete skill file content in markdown.
Then, provide the SKILL.md entry line.

New skill file:
"""


# ============================================================================
# PROCEDURE UPDATE PROMPT - For Q0_gap with weak_procedure_example root cause
# ============================================================================
PROCEDURE_UPDATE_PROMPT_POT = """You are a skill refinement expert. A skill's Procedure or Worked Example section needs improvement.

**Skill File:** `{skill_file}`

**Current Skill Content:**
```markdown
{current_skill}
```

**Gap Evidence:** Cases where the pattern matches but procedure is incomplete or lacks worked & checked example

{gap_evidence}

**Root Cause:** weak_procedure_example — Pattern matches but procedure is incomplete or lacks a worked & checked example (step-by-step with actual numbers and verification).

**Your Task:**

Analyze the gap evidence and update ONLY the affected pattern(s). Use incremental refinement format.

**Analysis:**
1. Which patterns need better procedure or worked examples?
2. What calculation steps are missing or unclear?
3. What worked example would demonstrate the correct approach?

**WORKED EXAMPLE Requirements:**

1. **Use actual numbers** — Not variables or placeholders
2. **Show step-by-step calculation** — Break down each intermediate value
3. **Include complete working code** — With imports, all variable definitions, and expression return
4. **Match the code template structure** — Follow the same steps as the template
5. **Use DIFFERENT numbers** — Not from the gap evidence cases

**Output Format:**

For patterns that need better procedure/examples:
```
## REFINED Pattern: {{exact_existing_pattern_name}}

**Description:** {{keep existing or clarify}}

**When to Use:** {{keep existing}}

**Procedure:**
{{improved/clarified procedure steps}}

**Code Example:**

**Worked Example:**
**Question:** {{example}}
```python
# Step-by-step with actual numbers
...
```

**Common Bugs to Avoid:**
- {{specific bugs from gap evidence}}
```

If NO changes are needed:
```
NO_CHANGES
Reason: Current procedure and examples are sufficient.
```

If gap reveals a completely NEW calculation type not covered by any existing pattern:
```
NEEDS_NEW_PATTERN
Reason: {{explain why existing patterns cannot handle this calculation type}}
```

**IMPORTANT**:
- Output ONLY changed patterns (not the entire file)
- ONLY refine existing patterns - do NOT create new patterns
- If gap reveals new calculation type, output NEEDS_NEW_PATTERN
- Use DIFFERENT numbers from gap evidence
"""


# ============================================================================
# CHECKS UPDATE PROMPT - For Q0_gap with need_checks root cause
# ============================================================================
CHECKS_UPDATE_PROMPT_POT = """You are a code validation expert. Update an existing skill file so it has ENOUGH CHECK steps and Common Bugs to Avoid — the pattern matches these questions but the skill is still failing on new ones because checks/constraints are missing or insufficient.

**Skill File:** `{skill_file}`

**Current Skill Content:**
```markdown
{current_skill}
```

**Gap Evidence:** Cases where the pattern matched but the skill failed (insufficient CHECK steps or Common Bugs to Avoid, so it keeps failing on new questions)

{gap_evidence}

**Root Cause:** need_checks — Pattern matches but missing enough CHECK steps or Common Bugs to Avoid, so the skill fails on new questions; and/or missing validation logic or sanity checks in the code.

**Your Task:**

Analyze the gap evidence and update ONLY the affected pattern(s). Use incremental refinement format.

**Analysis:**
1. Which patterns matched but still failed?
2. What validation checks are missing?
3. What bugs from gap evidence should be explicitly avoided?
4. What sanity checks would catch these errors?

**Code Safety (for execution_failed cases):**

If any case has `error_type: execution_failed`, add guards to prevent:
- `ZeroDivisionError` → Check divisor != 0 before division
- `ValueError` (negative sqrt) → Validate value >= 0 before math.sqrt()
- `TypeError` → Add type conversion if needed
- `IndexError` → Add bounds checking
- Missing import → Add to CODE CONSTRAINTS
- `print()` as last line → Use expression instead

**Output Format:**

For patterns that need better checks:
```
## REFINED Pattern: {{exact_existing_pattern_name}}

**Description:** {{keep existing}}

**When to Use:** {{keep existing}}

**Procedure:**
{{keep existing}}

**Code Example:**
{{keep existing}}

**CHECK Steps:**
- If {{condition from gap evidence}}, verify {{what to check}}
- Assert {{validation logic}} (e.g., "assert npv >= 0 or explicitly shorting")
- Sanity check: {{expected relationship}} (e.g., "total weights should sum to 1.0")
- {{add more checks derived from gap evidence}}

**Common Bugs to Avoid:**
- {{specific bug that caused failures in gap evidence}}
- {{other common mistakes for this pattern}}
- {{validation that should be done}}
```

If NO changes are needed:
```
NO_CHANGES
Reason: Current CHECK steps and Common Bugs are sufficient.
```

If gap reveals a completely NEW edge case type not covered by any existing pattern:
```
NEEDS_NEW_PATTERN
Reason: {{explain why existing patterns cannot handle this edge case type}}
```

**IMPORTANT**:
- Output ONLY changed patterns (not the entire file)
- ONLY refine existing patterns - do NOT create new patterns
- If gap reveals new edge case type, output NEEDS_NEW_PATTERN
- Derive checks from actual gap evidence failures
- Be specific about what to validate
"""


# ============================================================================
# COVERAGE REFINEMENT PROMPT POT - Unified prompt for Q0_gap diagnosis types
# ============================================================================

# Diagnosis-specific guidance for PoT mode
# Keys are ACTION names (used by card.recommended_action)
# Root causes: weak_procedure_example, need_checks, new_pattern
DIAGNOSIS_GUIDANCE_POT = {
    "update_example": """**Root Cause:** weak_procedure_example
The pattern's Procedure or Worked Example is incomplete or lacks step-by-step code.
- Identify which procedure steps are vague or incomplete
- Add missing calculation steps with clear formulas
- Improve the Worked Example with step-by-step code
- Include all imports and variable definitions
- Focus on **Procedure** and **Worked Example** sections""",

    "add_checks_and_constraints": """**Root Cause:** need_checks
The pattern lacks CHECK steps, CODE CONSTRAINTS, or validation logic.
- Identify what validation is missing from gap evidence
- Add CHECK steps with specific conditions
- Add "Common Bugs to Avoid" section
- Add code guards (e.g., assert, if-else validation)
- Focus on **CHECK Steps** and **Common Bugs to Avoid** sections""",
}

COVERAGE_REFINEMENT_PROMPT_POT = """You are a code-based skill refinement expert. Your task is to fix capability gaps in a financial calculation skill file.

**Skill File Being Refined:** `{skill_file}`
**Skill Set:** {skill_set_name}

**Current Skill Content:**
```markdown
{current_skill}
```

---

## Current Diagnosis: `{diagnosis_type}`

{diagnosis_guidance}

---

## Gap Evidence ({num_cases} cases)

{gap_evidence}

---

## Your Task

Update the skill to fix these gaps based on the diagnosis above.

## Output Format

**Option 1: REFINED Pattern** — Update an existing pattern

```
## REFINED Pattern: {{exact_existing_pattern_name}}

**Description:** {{updated description}}

**When to Use:** {{updated trigger conditions}}

**Procedure:**
1. {{updated step}}
2. {{updated step}}
...

**Worked Example:**
**Question:** {{example question — DIFFERENT from evidence}}
```python
# Step-by-step calculation with clear variable names
# Include all imports at the top
# MUST end with expression (not print)

import math  # if needed

# Step 1: Extract values
value1 = ...

# Step 2: Calculate
result = ...

# Final answer (expression, not print)
result
```

**Common Bugs to Avoid:**
- {{specific bug from gap evidence}}
- {{another common mistake}}

**CHECK Steps:**
- If {{condition}}, verify {{what to check}}
- Assert {{validation logic}}
```

**Option 2: NEW Pattern** — Add a new pattern to THIS file (when existing patterns cannot handle the calculation type)

```
## NEW Pattern: {{new_pattern_name}}

**Description:** {{what this pattern addresses}}

**When to Use:** {{trigger conditions with keywords}}

**Procedure:**
1. {{step}}
2. {{step}}
...

**Worked Example:**
**Question:** {{example question — DIFFERENT from evidence}}
```python
# Step-by-step calculation
...
result
```

**Common Bugs to Avoid:**
- {{common mistake}}

**CHECK Steps:**
- If {{condition}}, verify {{what to check}}
```

**Option 3: NO_CHANGES** — Current skill already handles these cases

```
NO_CHANGES
Reason: {{explain why no changes are needed}}
```

---

## Critical Guidelines

1. **REFINED vs NEW Pattern:**
   - Use REFINED if an existing pattern can be improved to handle gap cases
   - Use NEW Pattern only if gap cases represent a fundamentally different calculation type

2. **CODE CONSTRAINTS (for PoT mode):**
   - Code MUST end with expression (not print) — for eval() to capture
   - Include ALL necessary imports at the top
   - Define ALL variables before use
   - Use explicit values from the question
   - NO input() or interactive functions
   - NO print() as the last line (returns None)

3. **AVOID OVERFITTING:**
   - DO NOT copy specific question text from evidence
   - DO extract general calculation patterns and formulas
   - Worked examples must use DIFFERENT numbers than evidence cases
   - Code templates must work on NEW, UNSEEN questions
   - CHECK steps should be general validation logic, not case-specific

4. **Focus on the diagnosis:**
   - `incomplete_procedure` → improve **Procedure** and **Worked Example**
   - `weak_example` → improve **Worked Example** with better code
   - `trigger_mismatch` → improve **"When to Use"** keywords
   - `add_checks_and_constraints` → add **CHECK Steps** and **Common Bugs**

5. **Output ONLY changed patterns:**
   - For REFINED patterns, use the EXACT pattern name from current skill
   - Unchanged patterns will be preserved automatically
   - Don't output the entire file

**REMEMBER:** Extract calculation patterns and formulas, NOT specific questions. The skill must generalize to NEW questions.

Now provide the incremental changes:
"""


# ============================================================================
# SYSTEM PROMPTS
# ============================================================================
COVERAGE_SYSTEM_PROMPT_POT = "You are an expert code-based skill refinement assistant. Fix capability gaps in PoT skills based on diagnosis evidence."
