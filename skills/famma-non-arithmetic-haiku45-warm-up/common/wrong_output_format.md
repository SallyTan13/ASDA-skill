# Analysis of Failure Cases

All three cases demonstrate **wrong_output_format** errors where the model's reasoning is correct but the final answer doesn't match the expected format or contradicts its own analysis.

---

## Pattern: Answer-Explanation Alignment Failure

**Description:** The model generates a correct explanation but produces a final answer that contradicts its own reasoning, or provides an answer in a different format than required (verbose vs. concise, or initial statement vs. corrected statement).

**When to Use:** When answering any question that requires a definitive answer followed by explanation. Trigger: multi-part responses with "Answer:" and "Explanation:" sections, yes/no questions, multiple choice questions.

**Procedure:**
1. **Complete all reasoning first** before writing any answer statement
2. **Extract the conclusion** from your final reasoning step explicitly
3. **Write the answer section** using ONLY the conclusion from step 2
4. **Verify alignment**: Check that the answer statement matches the conclusion (if reasoning says "NOT in the money," answer must be "No")
5. **Match the expected format**: If ground truth is terse (e.g., "No." or "Cleveland Compressor."), provide the minimal answer without elaboration in the answer field
6. **Never self-contradict**: If you write "Answer: Yes" but then explain why the answer is actually "No," revise the answer field to match the correct reasoning

**Example (sanitized):**
> **Scenario:** Question asks "Is the bond trading at a premium?" Stock price is $95, bond converts at $100.
> 
> **Wrong approach:** 
> - Answer: Yes
> - Explanation: Since $95 < $100, the conversion value is below par, so the bond is trading at a discount, not a premium.
> 
> **Correct approach:**
> 1. Calculate: conversion value ($95) vs par ($100)
> 2. Conclude: $95 < $100 means discount
> 3. Write answer matching conclusion: "No" or "No, the bond is trading at a discount"
> 4. Verify: Answer "No" aligns with "discount" conclusion ✓

---

## Pattern: Calculated-vs-Selected Answer Mismatch

**Description:** When performing calculations that lead to a clear numerical result, the model fails to select the corresponding answer option, instead defaulting to an incorrect option due to second-guessing or misalignment between computation and option mapping.

**When to Use:** Multiple choice questions requiring numerical calculations (ratios, returns, alphas, valuations). Trigger: "calculate," "evaluate," "which fund/option/firm," followed by lettered choices.

**Procedure:**
1. **Perform all calculations** for each option/entity completely
2. **Write down results explicitly** with labels (e.g., "Fund A: -2.8%, Fund B: -0.5%, Fund C: +1.8%")
3. **Identify the answer** by applying the question criterion (highest, lowest, positive, etc.) to your calculated results
4. **Map to the option letter** that corresponds to your identified answer
5. **Do not override** your calculation-based conclusion with guesses about "test conventions" or "provided answers"
6. **Final check**: State "My calculations show [X] has the [highest/lowest] value of [Y], therefore the answer is [Option Letter]"

**Example (sanitized):**
> **Scenario:** Three portfolios have Sharpe ratios to calculate. Which has the highest?
> 
> **Wrong approach:**
> - Calculate: Portfolio A = 0.45, Portfolio B = 0.52, Portfolio C = 0.61
> - Think: "C is highest, but that's not option A which is usually correct"
> - Select: A
> 
> **Correct approach:**
> 1. Calculate all three: A = 0.45, B = 0.52, C = 0.61
> 2. Apply criterion: "highest" means maximum value
> 3. Identify: 0.61 is the maximum, which is Portfolio C
> 4. Map: Portfolio C corresponds to option C
> 5. Answer: C
> 6. Verify: "My calculations show Portfolio C has the highest Sharpe ratio of 0.61, therefore the answer is C" ✓

---

## Pattern: Verbosity Mismatch with Ground Truth Format

**Description:** The model provides comprehensive, well-reasoned answers when the expected output format is minimal (single word, name, or letter), causing format-based evaluation failures despite correct content.

**When to Use:** When ground truth examples show terse formats (e.g., "No.", "Company Name.", single letters). Trigger: simple identification questions, yes/no questions, "which firm/fund" questions.

**Procedure:**
1. **Check if reasoning is required** by the question wording ("Why?" or "Explain" → verbose; simple "Which?" or "Is?" → terse)
2. **For terse-expected answers**: Provide only the direct answer matching ground truth format
   - Yes/No questions → "Yes." or "No."
   - Which entity → "Entity Name." (no elaboration)
   - Multiple choice → "Letter" only
3. **For explanation-required answers**: Provide answer + full reasoning
4. **When uncertain about format**: Default to minimal answer first, then add explanation in separate section if needed
5. **Verification**: Compare your answer format to any ground truth examples provided in the question

**Example (sanitized):**
> **Scenario:** "Which company has higher revenue?" Ground truth format: "Acme Corp."
> 
> **Wrong approach:**
> - Answer: "Acme Corp. has higher revenue because their sales are $500M compared to Beta Inc.'s $300M, representing a 67% difference driven by larger market share..."
> 
> **Correct approach:**
> 1. Note question asks "Which" without "Why" or "Explain"
> 2. Calculate/identify: Acme Corp. ($500M) > Beta Inc. ($300M)
> 3. Format answer to match expected terseness: "Acme Corp."
> 4. Stop (do not add explanation unless requested)