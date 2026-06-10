# Pattern 1: Reference-Dependent Question Interpretation

**Description:** Questions that reference previously defined alternatives (e.g., "as in question 3 or question 5") require selecting between specific options, not providing general analysis. Failure occurs when treating these as open-ended questions instead of binary/multiple-choice selections.

**When to Use:** When question contains phrases like "as in question X," "should it be X or Y," "which option," or explicitly references numbered alternatives from earlier problem parts.

**Procedure:**
1. Identify reference phrases that point to specific alternatives (e.g., "as in question 3," "or as in question 5")
2. Recognize this signals a selection task, not an analysis task—the answer must be one of the referenced options
3. If the referenced questions are not visible in current context, state that the answer depends on comparing the specific terms in those questions
4. Structure answer as a definitive choice (e.g., "Question 5" or "Option A") rather than conditional analysis
5. Avoid providing general recommendations when a specific selection between pre-defined alternatives is requested
6. Verify final answer is in the form of selecting one of the referenced options, not a qualified statement

**Example (sanitized):**
> **Scenario:** "Should the project be funded? If so, should it be as in scenario A or as in scenario B?"
> **Wrong approach:** "Yes, the project should be funded. The decision between A and B depends on risk tolerance and capital availability, but funding appears justified."
> **Correct approach:** First recognize this requires choosing between two specific scenarios (A or B). Without seeing the details of scenarios A and B, I cannot make the selection. If scenario A involves equity financing with 12% cost and scenario B involves debt financing with 8% after-tax cost, and NPV is positive under both, select the one with lower WACC impact: "Yes. Scenario B."

---

# Pattern 2: Qualitative vs. Quantitative Question Targets

**Description:** Questions asking "what is the difference between X" may seek conceptual/methodological distinctions rather than numerical calculations, especially when ground truth is descriptive (e.g., "weighting schemes") rather than numeric.

**When to Use:** When question asks about "difference," "distinction," or "comparison" and context suggests multiple methodological approaches exist (e.g., book vs. market values, different calculation methods).

**Procedure:**
1. Parse whether "difference" refers to a conceptual distinction or numerical gap by examining context clues
2. Check if the question setup presents multiple methodologies or approaches (e.g., different weighting schemes, valuation methods)
3. If ground truth format would be descriptive (e.g., "the weighting approach used"), provide conceptual answer identifying the methodological distinction
4. If ground truth format would be numeric (e.g., "$X" or "Y%"), calculate the quantitative difference
5. Key trigger: if question asks "what is the difference" without specifying "how much" or "calculate," lean toward conceptual interpretation
6. Verify answer type matches question intent: methodology explanation vs. numerical result

**Example (sanitized):**
> **Scenario:** "What is the difference between NPV and IRR?" with context discussing capital budgeting methods.
> **Wrong approach:** Calculate NPV = $50,000 and IRR = 18%, then state "The difference is that NPV is $50,000 while IRR is 18%."
> **Correct approach:** Recognize this asks for conceptual distinction: "NPV measures absolute dollar value added, while IRR measures percentage return rate. NPV assumes reinvestment at the cost of capital, while IRR assumes reinvestment at the IRR itself."

---

# Pattern 3: Enterprise Value vs. Equity Value Disambiguation

**Description:** "Company value" or "firm value" in merger/valuation contexts typically refers to enterprise value (total firm value including all claims), not equity value. State-contingent values in tables usually represent total firm values already.

**When to Use:** When question asks for "company value," "firm value," or "value of [company name]" in merger, acquisition, or capital structure contexts where debt is mentioned.

**Procedure:**
1. Identify whether question asks for "company/firm value" (enterprise value) or explicitly "equity value"
2. If state-contingent or scenario values are provided in tables, treat these as total firm values (enterprise values) that already include all claims
3. For enterprise value: use the given or calculated firm values directly without subtracting debt
4. For equity value: calculate as max(0, firm value - debt face value) in each state
5. Do not subtract debt from company value unless question explicitly asks for equity value or shareholder value
6. Verify that your interpretation aligns with merger context conventions (enterprise value is standard for "company value")

**Example (sanitized):**
> **Scenario:** "What is the value of Company Alpha before merger?" Given: Boom state value = $500K (prob 0.6), Recession value = $200K (prob 0.4), outstanding debt = $150K.
> **Wrong approach:** Expected firm value = 0.6(500K) + 0.4(200K) = $380K. Subtract debt: $380K - $150K = $230K company value.
> **Correct approach:** Company value = expected enterprise value = 0.6($500K) + 0.4($200K) = $380K. The debt is a claim against this value, not a reduction of company value. Answer: $380,000.

---

# Pattern 4: NPV Decision Rule to Binary Answer Mapping

**Description:** Failure to correctly map NPV calculation results to yes/no decision answers, despite correct computation. The disconnect occurs between stating the decision rule and providing the final binary response.

**When to Use:** When question asks "should you accept/reject" or similar binary decision questions based on NPV, IRR, or other financial metrics with clear decision thresholds.

**Procedure:**
1. Calculate the decision metric (NPV, IRR, PI, etc.) accurately
2. State the decision rule explicitly (e.g., "Accept if NPV > 0," "Accept if IRR > required return")
3. Compare calculated value to threshold and state the comparison result (e.g., "NPV = $1,240 > 0")
4. Map to binary decision using the rule (positive NPV → accept → "Yes")
5. Ensure final answer matches the decision rule conclusion—do not contradict your own calculation
6. Format final answer as the binary choice requested: "Yes" or "No," not a qualified statement
7. Verify consistency: trace from calculation → rule application → final answer to ensure no contradictions

**Example (sanitized):**
> **Scenario:** "If required return is 15%, should you invest?" NPV calculated as $2,300.
> **Wrong approach:** Calculate NPV = $2,300. State "NPV is positive, so investment is attractive." Final answer: "No, you should not invest."
> **Correct approach:** NPV = $2,300. Decision rule: Accept if NPV > 0. Since $2,300 > 0, accept the investment. Final answer: "Yes."

---

# Pattern 5: Debt Value in Default Scenarios

**Description:** "Value of debt" in scenarios with potential default refers to the market/actual value (what debtholders receive), which equals min(firm value, debt face value), not the face value of the original debt claim.

**When to Use:** When question asks for "value of debt," "debt value," or "what debtholders receive" in contexts involving merged firms, bankruptcy risk, or state-contingent outcomes where firm value may be less than debt obligations.

**Procedure:**
1. Distinguish between "face value of debt" (contractual amount) and "value of debt" (market value/actual payment)
2. Identify the firm value in the specific scenario/state being analyzed
3. Calculate total debt face value (sum of all debt claims if multiple entities merged)
4. Determine debt value as min(total firm value, total debt face value) for that scenario
5. If firm value < debt face value, debtholders receive the entire firm value (partial default)
6. If firm value ≥ debt face value, debtholders receive full face value
7. Verify interpretation: "value of debt" in default contexts = actual payment to debtholders, not face value

**Example (sanitized):**
> **Scenario:** "What is the value of debt in the Low-Medium state?" Firm A has debt of $300K, Firm B has debt of $400K. After merger, combined value in Low-Medium state is $500K.
> **Wrong approach:** The debt value is $300K from Firm A (or $400K from Firm B, or $700K total face value).
> **Correct approach:** Total debt face value = $300K + $400K = $700K. Combined firm value = $500K. Since $500K < $700K, debt value = min($500K, $700K) = $500K. Debtholders receive the entire firm value. Answer: $500,000.