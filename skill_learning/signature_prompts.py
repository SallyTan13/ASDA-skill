"""
Failure Signature Analysis - Prompts and Taxonomy

This module contains the error taxonomy and prompts used for analyzing
failure cases in financial reasoning benchmarks.

Easy to modify without touching the main analysis logic.
"""

# Base error taxonomy (from docs/cases_analysis.md)
# Note: Error type 10 is only included for PoT (arithmetic) questions
_BASE_ERROR_TAXONOMY = {
    "1": "visual evidence",
    "2": "wrong method selection",
    "3": "concept confusion",
    "4": "missed multi-step computation",
    "5": "unit/currency/percent mistakes",
    "6": "missed constraints",
    "7": "wrong targets",
    "8": "wrong output format",
    "9": "others and please specify"
}

# For backward compatibility (includes code execution error by default)
ERROR_TAXONOMY = {
    **_BASE_ERROR_TAXONOMY,
    "10": "code execution error (PoT-specific)"
}


def get_error_taxonomy(pot_mode: bool = True) -> dict:
    """
    Get error taxonomy based on whether PoT is used.

    Args:
        pot_mode: If True, includes error type 10 (code execution error) for PoT questions.
                  If False, excludes it (for non-arithmetic/direct reasoning questions).

    Returns:
        Dictionary of error types
    """
    if pot_mode:
        return ERROR_TAXONOMY
    else:
        return _BASE_ERROR_TAXONOMY

# Base taxonomy descriptions (error types 1-9)
_BASE_TAXONOMY_TEXT = """1. visual evidence: The key evidence was read/located/aligned incorrectly OR not used at all.This includes chart/table/diagram misread and "ignored visual evidence".
2. wrong method selection: Chose the wrong model/formula/procedure pipeline or violated method assumptions. Examples: CAPM vs APT, BSM vs binomial, FCFF vs FCFE, wrong discounting pipeline, assumption mismatch. Use when: Concept is roughly known but the chosen approach is inappropriate.
3. concept confusion: Missing/incorrect finance concept at the definition/intuitive level (directionality/meaning), causing wrong reasoning even without heavy computation. Use when: The model's core concept understanding is wrong.
4. missed multi-step computation: Requires 2+ intermediate reasoning steps (filter -> compute -> compare -> decide), but the chain is incomplete/wrong order/missing a key intermediate. Use when: The failure is primarily due to missing intermediate reasoning rather than wrong concept or wrong method.
5. unit/currency/percent mistakes: Method and evidence are basically correct, but numeric execution OR unit/scale conversion is wrong. Includes bps/%/percent points, currency conversion, million/billion scale, annualization, arithmetic/algebra substitution.
6. missed constraints: Explicit constraints/assumptions in the question were not applied. Use when: The question contains explicit instruction(s) and the answer violates them. ("assume", "ignore", "given")
7. wrong targets: Misread the question wording or answer a different target/answer-space.
8. wrong output format: The reasoning/value is correct (or mostly correct) but the final output is formatted/mapped incorrectly, leading to an evaluation mismatch. Examples: wrong option letter, missing unit, wrong rounding spec, not following required answer format. Use when: The content is right but the final response format is wrong.
9. others and please specify"""

# PoT-specific error type (only for arithmetic questions)
_POT_ERROR_TYPE_TEXT = """10. code execution error (PoT-specific): The conceptual approach is correct but the code implementation has bugs. Examples: last line uses print() instead of expression (returns None), sign convention errors (NPV cash flows, initial investment direction), missing imports (numpy, scipy), variable used before definition, wrong annualization factor (252 vs 365 days), incorrect operator precedence, wrong variable names, off-by-one errors in loops, incorrect indexing. Use when: The right formula/method was chosen but the Python code has implementation errors. **IMPORTANT**: If the explanation contains Python code, carefully examine the code to identify specific bugs. Check code_execution_success field - if False, this is likely an error_type 10 case."""


def get_signature_prompt(pot_mode: bool = True) -> str:
    """
    Get signature analysis prompt based on whether PoT is used.

    Args:
        pot_mode: If True, includes error type 10 (code execution error) for PoT questions.
                  If False, excludes it (for non-arithmetic/direct reasoning questions).

    Returns:
        Prompt template string with placeholders for formatting
    """
    # Build taxonomy text
    if pot_mode:
        taxonomy_text = _BASE_TAXONOMY_TEXT + "\n" + _POT_ERROR_TYPE_TEXT
        error_type_range = "(1-10)"
    else:
        taxonomy_text = _BASE_TAXONOMY_TEXT
        error_type_range = "(1-9)"

    return f"""You are analyzing a failure case from a financial reasoning benchmark. Your task is to identify the ROOT CAUSE - the underlying knowledge gap or reasoning flaw that caused the failure.

**Question Context:**
{{context}}

**Question:**
{{question}}
{{options_section}}
**Ground Truth:**
{{ground_truth}}

**Model's Answer:**
{{generated_answer}}

**Model's Explanation:**
{{generated_explanation}}
{{code_status_section}}
**Error Taxonomy (choose one):**
{taxonomy_text}

Analyze this failure deeply and identify the UNDERLYING knowledge gap:

1. **modality**: Is this text-only, table-based, chart-based, image-based, or mixed?
2. **error_type**: Choose the most appropriate error type number {error_type_range} from the taxonomy above
3. **error_detail**: If error_type is 9 (others), specify the error. Otherwise, provide a brief explanation.
4. **required_ops**: What operations were required? (e.g., "read_chart_value", "unit_conversion", "multi_step_calc", "table_lookup", "financial_concept_application")
5. **root_cause**: Identify the UNDERLYING knowledge gap or reasoning flaw. Focus on WHY, not WHAT:

   ❌ BAD (describes WHAT went wrong): "The model did not correctly calculate the combined firm value"
   ✅ GOOD (explains WHY - knowledge gap): "Lacks understanding that debt value equals the minimum of face value and firm value in bankruptcy scenarios"

   ❌ BAD: "The model failed to apply the financial concept correctly"
   ✅ GOOD: "Confuses correlation with causation when interpreting benchmark tracking data"

   ❌ BAD: "The model misunderstood the interest rate swap"
   ✅ GOOD: "Missing knowledge that pay-fixed swaps hedge against rising rates by converting floating liabilities to fixed"

   Your root cause should be:
   - Specific about the missing knowledge/concept
   - Actionable for skill development
   - About WHY the model failed, not WHAT it calculated wrong

Respond in JSON format:
{{{{
  "modality": "...",
  "error_type": N,
  "error_detail": "...",
  "required_ops": ["op1", "op2", ...],
  "root_cause": "..."
}}}}
"""


# For backward compatibility (includes PoT by default)
SIGNATURE_PROMPT = get_signature_prompt(pot_mode=True)
