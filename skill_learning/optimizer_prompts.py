"""
Optimizer Prompts - Prompts for TextualOptimizer

Separated for easy modification and versioning.
"""

# ============================================================================
# SKILL REFINEMENT PROMPT - For Q+/Q- evidence-based refinement
# ============================================================================
SKILL_REFINEMENT_PROMPT = """You are a skill refinement expert. Your task is to improve a financial reasoning skill file based on evidence from actual usage.

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
2. **Reduce regressions** — Add guards, anti-patterns, or refine "when to use" from Q- evidence
3. **Improve precision** — Make patterns apply only when they truly help (contrast helps avoid over-application)

**CRITICAL GUIDELINES:**
1. **Refining existing patterns** — From Q+ and Q- evidence:
   - Strengthen procedures that worked (from Q+)
   - Add guard steps or "Do NOT" warnings for regressions (from Q-)
   - Refine "When to Use" for better trigger precision

2. **Adding new patterns** — If evidence reveals a new failure type or current patterns and even refined patterns cannot solve completely:
   - Create a NEW pattern section following the template above
   - Focus on the general principle, not specific cases

3. **AVOID OVERFITTING:**
   - DO NOT copy specific questions, contexts, or answers from evidence
   - DO extract general patterns, principles, and reasoning strategies
   - Examples must be SYNTHETIC (different numbers, names, context)
   - The skill must work on NEW, UNSEEN questions
   - Skills should be general and can be transferred to other questions

**Output Format:**
Output ONLY the patterns that need changes. Use these markers to distinguish refined vs new:

For patterns that need refinement (based on Q+ or Q- evidence):
```
## REFINED Pattern: {{exact_existing_pattern_name}}

**Description:** {{updated description}}

**When to Use:** {{updated trigger conditions}}

**Procedure:**
1. {{updated step}}
2. {{updated step}}
...

**Example (sanitized):**
> **Scenario:** {{generic scenario — different from evidence}}
> **Wrong approach:** {{common mistake}}
> **Correct approach:** {{correct reasoning}}
```

For new patterns (if evidence reveals new failure types):
```
## NEW Pattern: {{new_pattern_name}}

**Description:** {{description of new knowledge gap}}

**When to Use:** {{trigger conditions}}

**Procedure:**
1. {{step}}
2. {{step}}
...

**Example (sanitized):**
> **Scenario:** {{generic scenario — different from evidence}}
> **Wrong approach:** {{common mistake}}
> **Correct approach:** {{correct reasoning}}
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

**REMEMBER:** Extract patterns, NOT examples. The skill must generalize to NEW questions.

Now provide the incremental changes:
"""


# ============================================================================
# SAFETY REFINEMENT PROMPT - V2 Safety Phase with Contrastive Q+
# ============================================================================
SAFETY_REFINEMENT_PROMPT = """You are a skill refinement expert. Your task is to improve a financial reasoning skill file while carefully preserving what already works.

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

**Why they work:** The current skill patterns successfully handle these cases. Any changes you make must NOT break them.

---

## 🔧 REGRESSIONS TO FIX (from Q⁻)

These {num_negative} cases are failing and need to be fixed:

{negative_evidence}

---

## Your Task

Fix the Q⁻ regressions while **preserving Q⁺ correctness**.

**Key Principle:** This is a SAFETY refinement. The goal is to reduce regressions WITHOUT breaking existing fixes.

**Strategy:**
1. **Analyze Q⁺ first** — Understand WHY these cases work. What patterns or procedures are helping them?
2. **Analyze Q⁻ next** — Identify what's causing the regressions. Is it over-application? Missing guards? Incorrect procedure?
3. **Find safe modifications** — Add guards, refine scope, or add anti-patterns that fix Q⁻ WITHOUT affecting Q⁺

**CRITICAL GUIDELINES:**
1. **Preserve Q⁺ patterns** — Do NOT modify procedures that are working for Q⁺ cases
2. **Add guards for Q⁻** — Add "Do NOT use when..." or scope limits to prevent regressions
3. **Refine "When to Use"** — Make trigger conditions more precise to exclude Q⁻ failure modes
4. **Add anti-patterns** — Create explicit "Common Mistakes to Avoid" sections
5. **Adding new patterns** — If evidence reveals a new failure type or current patterns and even refined patterns cannot solve completely:
   - Create a NEW pattern section following the template above
   - Focus on the general principle, not specific cases

**AVOID OVERFITTING:**
- DO NOT copy specific questions, contexts, or answers from evidence
- DO extract general patterns, principles, and reasoning strategies
- Examples must be SYNTHETIC (different numbers, names, context)
- The skill must work on NEW, UNSEEN questions

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
2. {{updated step}}
...

**Common Mistakes to Avoid:**
- {{mistake from Q- evidence}}
- {{another mistake}}

**Example (sanitized):**
> **Scenario:** {{generic scenario — different from evidence}}
> **Wrong approach:** {{common mistake from Q-}}
> **Correct approach:** {{correct reasoning that preserves Q+}}
```

For new patterns (if evidence reveals new failure types):
```
## NEW Pattern: {{new_pattern_name}}

**Description:** {{description of new knowledge gap}}

**When to Use:** {{trigger conditions}}

**Procedure:**
1. {{step}}
2. {{step}}
...

**Example (sanitized):**
> **Scenario:** {{generic scenario — different from evidence}}
> **Wrong approach:** {{common mistake}}
> **Correct approach:** {{correct reasoning}}
```

If NO changes are needed (Q- cases are edge cases that cannot be fixed without breaking Q+):
```
NO_CHANGES
Reason: Fixing Q- cases would require changes that break Q+ cases. The current skill is optimal.
```

**IMPORTANT:**
- For REFINED patterns, use the EXACT pattern name from the current skill
- Only output patterns that actually need changes
- Unchanged patterns will be preserved automatically

**REMEMBER:** Safety first. If you cannot fix Q- without risking Q+, prefer NO_CHANGES. The skill must generalize to NEW questions.

Now provide the incremental changes:
"""


# ============================================================================
# SKILL.MD ROUTING UPDATE PROMPT - For Q+_discover cases (router mismatch)
# ============================================================================
SKILL_MD_ROUTING_PROMPT = """You are a skill routing expert. Your task is to update the SKILL.md navigation file so that the router correctly selects the right skill files.

**Problem:** These questions should have used certain skill files, but the router selected the WRONG files. The SKILL.md file reference table needs better keywords so the router can match correctly.

**Current SKILL.md:**
```markdown
{skill_md_content}
```

**Evidence of Routing Mismatches (Q+_discover):**
These {num_cases} cases were solved by a DIFFERENT skill file than the one selected by the router.

{discover_evidence}

**Your Task:**
Update the SKILL.md file reference table to improve routing:

1. **Update "Key Patterns" column** for the target files that SHOULD have been selected:
   - Add keywords extracted from the missed questions
   - Keep existing keywords, just add new relevant ones

2. **Optionally update "When to Use" section** if the missed cases reveal new trigger conditions

3. **DO NOT change file paths, subfield names, or error types** - Only improve keywords

**Rules:**
- Extract GENERAL keywords, not specific question text
- Focus on financial terms, concepts, and action words
- Keep the table format intact

**Output Format:**
Provide the COMPLETE updated SKILL.md file with improved keywords in the file reference table.

Now provide the updated SKILL.md:
"""


# ============================================================================
# NEW SKILL CREATION PROMPT - For Q0_gap cases (capability gap)
# ============================================================================
NEW_SKILL_CREATION_PROMPT = """You are a skill creation expert. Your task is to create a NEW skill file to address capability gaps in a 2-level skill set.

**Problem:** No existing skill can solve these cases. This represents a capability gap in the skill library.

**Skill Set Structure:**
```
{skill_set_name}/
  SKILL.md              # Navigation file with file reference table
  common/               # Cross-subfield skills
  {{subfield}}/           # Subfield-specific skills
```

**Target Subfield:** {subfield}
**Target Folder:** {subfield_folder}/
**Proposed File:** {subfield_folder}/{proposed_filename}

**Evidence of Capability Gap (Q0_gap):**
These {num_cases} cases could not be solved by any existing skill:

{gap_evidence}

**Diagnosis Summary:**
{diagnosis_summary}

**Your Task:**

1. **Identify the Pattern** — What common theme connects these failures?
   - What financial concept is missing?
   - What calculation or reasoning step is needed?

2. **Create the Skill File** — Using the pattern-based format:

```
# {{Subfield}} — {{Error Type}}

## Pattern: {{concise_pattern_name}}

**Description:** {{1-2 sentence description of the knowledge gap}}

**When to Use:** {{trigger conditions and keywords}}

**Procedure:**
1. {{actionable step 1}}
2. {{actionable step 2}}
...

**Example (sanitized):**
> **Scenario:** {{generic scenario — different from evidence}}
> **Wrong approach:** {{common mistake}}
> **Correct approach:** {{correct reasoning}}
```

3. **Also provide a SKILL.md table entry** — At the end, include:
```
SKILL_MD_ENTRY: | `{subfield_folder}/{{filename}}.md` | {{Subfield}} | {{Error Type}} | {{Pattern1}}, {{Pattern2}} |
```

**CRITICAL:**
- DO NOT copy specific questions from evidence
- Create SYNTHETIC examples only
- Focus on the general pattern/concept
- Maximum 500 lines

Now create the new skill file:
"""


# ============================================================================
# UPDATE DESCRIPTION/PROCEDURE PROMPT - For incomplete_procedure cases
# ============================================================================
UPDATE_DESCRIPTION_PROCEDURE_PROMPT = """You are a skill improvement expert. A skill's Description and/or Procedure sections need improvement based on gap evidence.

**Current Skill:**
```markdown
{current_skill_content}
```

**Gap Cases ({num_cases} total, showing up to 10):**
These cases were incorrectly answered because the skill's Description/Procedure is incomplete or unclear.

{cases_text}

**Your Task:**
Analyze the gap cases and update ONLY the affected pattern(s). Use incremental refinement format.

**Analysis:**
1. Which existing pattern(s) need clarification?
2. What missing steps are needed?
3. What vague steps need to be more actionable?
4. Do we need a completely new pattern, or just refine existing ones?

**Output Format:**

For patterns that need refinement:
```
## REFINED Pattern: {{exact_existing_pattern_name}}

**Description:** {{updated description — must be clearer}}

**When to Use:** {{updated trigger conditions}}

**Procedure:**
1. {{updated/clarified step}}
2. {{updated/clarified step}}
...

**Example (sanitized):**
> {{keep existing}}
```

If NO changes are needed:
```
NO_CHANGES
Reason: Current Description/Procedure already addresses all gap cases effectively.
```

If gap reveals a completely NEW case type not covered by any existing pattern:
```
NEEDS_NEW_PATTERN
Reason: {{explain why existing patterns cannot handle this case type}}
```

**IMPORTANT**:
- Output ONLY changed patterns (not the entire file)
- ONLY refine existing patterns - do NOT create new patterns
- If gap reveals new case type which means that it cannot match any patterns, output NEEDS_NEW_PATTERN
- Create GENERALIZED steps that work for similar cases
- DO NOT copy exact question text from evidence
"""


# ============================================================================
# UPDATE EXAMPLE PROMPT - For weak_example cases
# ============================================================================
UPDATE_EXAMPLE_PROMPT = """You are a skill improvement expert. A skill's Example section doesn't help the model apply the procedure correctly.

**Current Skill:**
```markdown
{current_skill_content}
```

**Gap Cases ({num_cases} total, showing up to 10):**
These cases were incorrectly answered. The procedure may be correct, but the Example doesn't help generalize to these case types.

{cases_text}

**Your Task:**
Improve the skill's Example section using incremental refinement:

1. **Analyze the gap**: What makes these cases different from the current example?
2. **Create better example**: Make example more representative of common patterns
3. **Show the reasoning**: Demonstrate how to apply the procedure step-by-step
4. **Add contrast**: Show common mistakes vs correct approach
5. **Handle ALL case types above** — the example should help with similar variations

**Output Format:**

For patterns that need better examples:
```
## REFINED Pattern: {{exact_existing_pattern_name}}

**Description:** {{keep existing or clarify if needed}}

**When to Use:** {{keep existing}}

**Procedure:**
{{keep existing}}

**Example (sanitized):**
> **Scenario:** {{generic scenario — DIFFERENT from evidence cases}}
> **Wrong approach:** {{common mistake the model might make}}
> **Correct approach:** {{step-by-step reasoning using the Procedure}}
```

If NO changes are needed:
```
NO_CHANGES
Reason: Current examples already help with these case types.
```

If gap reveals a completely NEW case type not covered by any existing pattern:
```
NEEDS_NEW_PATTERN
Reason: {{explain why existing patterns cannot handle this case type}}
```

**IMPORTANT**:
- Output ONLY changed patterns (not the entire file)
- ONLY refine existing patterns - do NOT create new patterns
- If gap reveals new case type, output NEEDS_NEW_PATTERN
- Create SYNTHETIC examples only — different numbers, names, context from evidence
- Focus on the REASONING PROCESS, not the specific answer
"""


# ============================================================================
# UPDATE WHEN TO USE PROMPT - For trigger_mismatch cases
# ============================================================================
UPDATE_WHEN_TO_USE_PROMPT = """You are a skill improvement expert. A skill's "When to Use" section isn't matching the right questions.

**Current Skill:**
```markdown
{current_skill_content}
```

**Mismatched Cases ({num_cases} total, showing up to 10):**
These cases SHOULD have matched this skill but didn't because "When to Use" lacks the right keywords.

{cases_text}

**Your Task:**
Update the skill's "When to Use" section:

1. **Identify missing triggers**: What keywords/conditions would match these cases?
2. **Add trigger keywords**: Expand the "When to Use" section
3. **Keep it precise**: Don't make triggers too broad (avoid false positives)
4. **Handle ALL cases above** — find the common patterns that should trigger this skill

**"When to Use" Structure:**
```
**When to Use:**
- Keywords: {{financial terms that should trigger this pattern}}
- Conditions: {{scenarios where this pattern applies}}
- Question types: {{types of questions this handles}}
```

**IMPORTANT**:
- Extract GENERAL keywords, not specific question text
- Focus on financial concepts, actions, and scenario types
- Balance precision (don't match wrong cases) with recall (match all right cases)

**Output:**
Provide the COMPLETE updated skill in markdown format, ready to save.
"""


# ============================================================================
# COVERAGE REFINEMENT PROMPT - Unified prompt for Q0_gap diagnosis types
# ============================================================================

# Diagnosis-specific guidance for Non-PoT mode
# Keys are ACTION names (used by card.recommended_action)
# Root causes: trigger_mismatch, incomplete_procedure, weak_example, capability_gap
DIAGNOSIS_GUIDANCE = {
    "update_description_procedure": """**Root Cause:** incomplete_procedure
The pattern's Description/Procedure section is missing steps or unclear.
- Identify which procedure steps are vague or incomplete
- Add missing calculation/reasoning steps
- Make each step more actionable and specific
- Focus on **Description** and **Procedure** sections""",

    "update_example": """**Root Cause:** weak_example
The pattern's Example doesn't help the model generalize.
- Analyze what makes gap cases different from current example
- Create a better example that covers more variations
- Show step-by-step reasoning using the Procedure
- Include both wrong approach and correct approach
- Focus on **Example** section""",

    "update_when_to_use": """**Root Cause:** trigger_mismatch
The pattern's "When to Use" doesn't match the right questions.
- Identify missing trigger keywords from gap evidence
- Add keywords that would match these cases
- Keep triggers precise (avoid false positives)
- Focus on **"When to Use"** section""",
}

COVERAGE_REFINEMENT_PROMPT = """You are a skill refinement expert. Your task is to fix capability gaps in a financial reasoning skill file.

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

**Example (sanitized):**
> **Scenario:** {{generic scenario — DIFFERENT from evidence}}
> **Wrong approach:** {{common mistake}}
> **Correct approach:** {{step-by-step reasoning}}

**Common Mistakes to Avoid:**
- {{mistake derived from gap evidence}}
```

**Option 2: NEW Pattern** — Add a new pattern to THIS file (when existing patterns cannot handle the case type)

```
## NEW Pattern: {{new_pattern_name}}

**Description:** {{what this pattern addresses}}

**When to Use:** {{trigger conditions}}

**Procedure:**
1. {{step}}
2. {{step}}
...

**Example (sanitized):**
> **Scenario:** {{generic scenario — DIFFERENT from evidence}}
> **Wrong approach:** {{common mistake}}
> **Correct approach:** {{step-by-step reasoning}}
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
   - Use NEW Pattern only if gap cases represent a fundamentally different case type
   - NEW Pattern stays in THIS file — it's not a new file

2. **AVOID OVERFITTING:**
   - DO NOT copy specific questions, contexts, or answers from evidence
   - DO extract general patterns, principles, and reasoning strategies
   - Examples must be SYNTHETIC (different numbers, names, context)
   - The skill must work on NEW, UNSEEN questions

3. **Focus on the diagnosis:**
   - `incomplete_procedure` → improve **Procedure** steps
   - `weak_example` → improve **Example** section
   - `trigger_mismatch` → improve **"When to Use"** triggers
   - `add_checks_and_constraints` → add **validation/checks**

4. **Output ONLY changed patterns:**
   - For REFINED patterns, use the EXACT pattern name from current skill
   - Unchanged patterns will be preserved automatically
   - Don't output the entire file

**REMEMBER:** Extract patterns, NOT examples. The skill must generalize to NEW questions.

Now provide the incremental changes:
"""


# ============================================================================
# SYSTEM PROMPTS
# ============================================================================
REFINEMENT_SYSTEM_PROMPT = "You are an expert skill refinement assistant. Generate improved skill patterns based on evidence."
COVERAGE_SYSTEM_PROMPT = "You are an expert skill refinement assistant. Fix capability gaps in skills based on diagnosis evidence."
