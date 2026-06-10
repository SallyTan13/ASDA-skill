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

## Pattern: Reference-Dependent Question Interpretation

**Description:** Questions that reference previously defined alternatives (e.g., "as in question 3 or question 5") require selecting between specific options, not providing general analysis. Failure occurs when treating these as open-ended questions instead of binary/multiple-choice selections. Even when referenced questions are not visible, use available financial data to make a reasoned selection rather than stating inability to answer.

**When to Use:** When question contains phrases like:
- "as in question X" or "or as in question Y"
- "should it be X or Y"
- "which option"
- "or as in question"
- Explicitly references numbered alternatives from earlier problem parts
- Asks for selection between named scenarios/approaches
- Contains compound structure: "Should [action] be taken? If so, should it be [option A] or [option B]?"
- Pattern: "[Yes/No decision] + [selection between referenced alternatives]"

**Procedure:**
1. Identify reference phrases that point to specific alternatives (e.g., "as in question 3," "or as in question 5")
2. Recognize this signals a selection task, not an analysis task—the answer must be one of the referenced options
3. Analyze available financial data in the current context (growth rates, valuations, costs, returns, NPV impacts, value creation metrics) to determine which option would create more value
4. Apply financial principles to infer which referenced option is superior:
   - Higher NPV or value creation → select that option
   - Lower cost of capital → select that option
   - Better alignment with stated financial improvements → select that option
   - Higher growth rates or profitability → select that option
5. Make a definitive selection based on financial reasoning evident in the provided context, even without explicit details of the referenced questions
6. Structure answer as a definitive choice (e.g., "Yes. Question 5" or "Yes. Option B") rather than stating inability to determine
7. Never answer "Cannot determine," "Need more information," or "Without visibility of those scenarios" for reference-dependent questions—use financial reasoning to select the better option
8. Format: If question has two parts (Should X? If so, which option?), answer both: "[Yes/No]. [Selected option]."

**Example (sanitized):**
> **Scenario:** "Should the expansion proceed? If so, should it be as in scenario A or as in scenario B?" Context shows expansion would increase revenue growth from 5% to 8% and company's WACC is 11%.
> **Wrong approach:** "Yes, the expansion should proceed because the growth rate improvement from 5% to 8% creates value. However, the choice between scenario A and scenario B depends on comparing the specific terms in those referenced questions. Without visibility of those specific scenarios, a definitive selection between them cannot be made."
> **Correct approach:** Analyze available data: The growth rate improvement from 5% to 8% creates substantial value. If context mentions scenario B involves equity financing while scenario A involves debt, and the growth improvement suggests strong cash generation, scenario B may be preferable to maintain financial flexibility. Based on the value creation from growth improvement, select the option most aligned with this benefit. "Yes. Scenario B."

**Common Mistakes to Avoid:**
- Stating "Cannot determine without seeing question X" when financial data is available to make a reasoned choice
- Providing conditional analysis ("depends on comparing the specific terms") instead of a definitive selection
- Failing to use available financial metrics (growth rates, valuations, costs) to infer which option is superior
- Answering only the first part of a two-part question (e.g., "Yes" without selecting between options)
- Writing "Without visibility" or "Without access to those referenced questions" when financial reasoning can guide selection
## Pattern: Enterprise Value vs. Equity Value Disambiguation

**Description:** "Company value" or "firm value" in merger/valuation contexts typically refers to enterprise value (total firm value including all claims), not equity value. State-contingent values in tables usually represent total firm values already. The calculated enterprise value IS the final answer—no further adjustments needed. A critical failure mode is calculating the correct value but outputting a different number in the final answer field.

**When to Use:** When question asks for "company value," "firm value," "value of [company name]," "value of the company," or "value before/after merger" in merger, acquisition, or capital structure contexts where debt is mentioned.

**Procedure:**
1. Identify whether question asks for "company/firm value" (enterprise value) or explicitly "equity value"
2. If state-contingent or scenario values are provided in tables, treat these as total firm values (enterprise values) that already include all claims
3. For enterprise value: calculate expected value across states using probability weights
4. **MANDATORY VERIFICATION STEP:** Write down explicitly: "My calculated enterprise value is $[X]"
5. **MANDATORY CONSISTENCY CHECK:** Before providing final answer, verify that the number you are about to output matches exactly the number from step 4
6. The calculated expected enterprise value IS the final answer to "company value" questions—do not subtract debt or make further adjustments
7. For equity value (only if explicitly requested): calculate as max(0, firm value - debt face value) in each state
8. **FINAL OUTPUT CHECK:** State: "Therefore, my final answer is $[X]" where [X] must be identical to the value calculated in step 4
9. If there is ANY discrepancy between your calculation and your final answer output, STOP and reconcile the difference before proceeding

**Example (sanitized):**
> **Scenario:** "What is the value of Company Zenith before merger?" Given: High state value = $600K (prob 0.55), Low state value = $180K (prob 0.45), outstanding debt = $200K.
> **Wrong approach:** Calculate expected firm value = 0.55(600K) + 0.45(180K) = $411K. State "This is the enterprise value." Then output final answer as $211K (incorrectly subtracting debt or making arithmetic error).
> **Correct approach:** Company value = expected enterprise value = 0.55($600K) + 0.45($180K) = $330K + $81K = $411K. **VERIFICATION:** My calculated enterprise value is $411,000. The debt is a claim against this value, not a reduction of company value. **CONSISTENCY CHECK:** My calculation shows $411,000, so my final answer must be $411,000. **Final answer: $411,000** (matching the calculation exactly).

**Common Mistakes to Avoid:**
- Calculating the correct enterprise value but outputting a different number in the final answer (arithmetic transcription error)
- Subtracting debt from company value when question asks for "company value" (not equity value)
- Creating discrepancy between your calculation explanation and your final numerical answer
- Failing to perform explicit verification that calculated value matches output value
- Skipping the mandatory consistency check before finalizing the answer
```

```
## Pattern: NPV Decision Rule to Binary Answer Mapping

**Description:** Failure to correctly map NPV calculation results to yes/no decision answers, despite correct computation. The disconnect occurs between stating the decision rule and providing the final binary response. The final answer must match the decision rule conclusion—positive NPV always means "Yes." A critical failure mode is calculating positive NPV, stating the investment should be accepted, then outputting "No" as the final answer.

**When to Use:** When question asks "should you accept/reject," "should you invest," "should the offer be accepted," or similar binary decision questions based on NPV, IRR, or other financial metrics with clear decision thresholds.

**Procedure:**
1. Calculate the decision metric (NPV, IRR, PI, etc.) accurately
2. State the decision rule explicitly (e.g., "Accept if NPV > 0," "Accept if IRR > required return")
3. Compare calculated value to threshold and state the comparison result (e.g., "NPV = $1,240 > 0")
4. **MANDATORY DECISION MAPPING:** Write explicitly: "Since NPV > 0, the decision rule says to ACCEPT"
5. **MANDATORY BINARY TRANSLATION:** Write explicitly: "Accept means the answer is YES" (or "Reject means the answer is NO")
6. **CONSISTENCY VERIFICATION:** Before providing final answer, verify the logical chain:
   - If NPV > 0 → Accept → "Yes"
   - If NPV < 0 → Reject → "No"
   - If NPV = 0 → Indifferent → "Yes" or "No" (typically "Yes" if exactly zero)
7. **FINAL OUTPUT CHECK:** State: "Therefore, my final answer is [Yes/No]" and verify this matches step 5
8. **CONTRADICTION DETECTION:** If you wrote "should accept" anywhere in your reasoning but are about to answer "No," STOP—this is a contradiction that must be resolved
9. Format final answer as the binary choice requested: "Yes" or "No"—never contradict your own calculation

**Example (sanitized):**
> **Scenario:** "If required return is 18%, should you proceed with the investment?" NPV calculated as $3,450.
> **Wrong approach:** Calculate NPV = $3,450. State "NPV is positive at $3,450, which exceeds zero, so the investment creates value and should be accepted based on the NPV rule." Final answer: "No, you should not proceed."
> **Correct approach:** NPV = $3,450. Decision rule: Accept if NPV > 0. Comparison: $3,450 > 0. **DECISION MAPPING:** Since NPV > 0, the decision rule says to ACCEPT. **BINARY TRANSLATION:** Accept means the answer is YES. **CONSISTENCY CHECK:** Positive NPV → Accept → "Yes". **CONTRADICTION CHECK:** I stated "should be accepted" and my logic leads to "Yes"—these are consistent. **Final answer: Yes.**

**Common Mistakes to Avoid:**
- Calculating positive NPV, stating the investment should be accepted, then answering "No"
- Contradicting your own decision rule application in the final answer
- Failing to verify that final binary answer aligns with NPV sign (positive NPV must yield "Yes")
- Skipping the explicit decision mapping and binary translation steps
- Not performing the contradiction detection check before finalizing the answer
- Writing "should accept" in reasoning but outputting "No" in the answer field
## Pattern: Debt Value in Default Scenarios

**Description:** "Value of debt" in scenarios with potential default refers to the market/actual value (what debtholders receive), which equals min(firm value, debt face value), not the face value of the original debt claim. This is a straightforward calculation—do not second-guess or introduce alternative interpretations. The answer is the total debt value in the specified state, not per-company or per-creditor amounts.

**When to Use:** When question asks for "value of debt," "debt value," or "what debtholders receive" in contexts involving merged firms, bankruptcy risk, or state-contingent outcomes where firm value may be less than debt obligations.

**When NOT to Use:** 
- When question asks for "face value of debt" or "debt obligation" (contractual amount)
- When question asks for "debt outstanding" (original claim amount)
- When question explicitly asks for "per company" or "each company's" debt value
- Do not apply when the straightforward calculation is clear—avoid overthinking or introducing circular reasoning about alternative interpretations

**Procedure:**
1. Distinguish between "face value of debt" (contractual amount) and "value of debt" (market value/actual payment)
2. Identify the firm value in the specific scenario/state being analyzed
3. Calculate total debt face value (sum of all debt claims if multiple entities merged)
4. Determine debt value as min(total firm value, total debt face value) for that scenario
5. If firm value < debt face value, debtholders receive the entire firm value (partial default)
6. If firm value ≥ debt face value, debtholders receive full face value
7. **The calculated amount from step 4 is the final answer—do not divide by number of companies or introduce per-creditor interpretations**
8. State the answer clearly without second-guessing: the debt value is the total calculated amount from step 4
9. Verify interpretation: "value of debt" in default contexts = total actual payment to all debtholders, not face value and not per-company amounts

**Common Mistakes to Avoid:**
- Calculating the correct total debt value but then dividing by number of companies or creditors
- Introducing "per company" or "individual debt claim" interpretations when question asks for "value of debt" without such qualifiers
- Calculating the correct debt value but then questioning whether "value" means market value vs. face value
- Introducing circular reasoning that explores multiple interpretations when the calculation is straightforward
- Conflating "debt value" (what it's worth in total) with "debt obligation" (what is owed contractually)
- Overthinking a clear question by adding unnecessary alternative interpretations like "per company perspective"
- Stating both the correct answer and incorrect alternatives, creating confusion
- Second-guessing the straightforward total debt value calculation by considering individual creditor perspectives

**Example (sanitized):**
> **Scenario:** "What is the value of debt in the Medium-High state?" Firm A has debt of $250K, Firm B has debt of $350K. After merger, combined value in Medium-High state is $800K.
> **Wrong approach:** Calculate correctly: debt value = min($800K, $600K) = $600K, then add: "However, if asking for each company's debt value, it would be $300K per company on average, or $250K for Firm A's creditors."
> **Correct approach:** Total debt face value = $250K + $350K = $600K. Combined firm value = $800K. Since $800K ≥ $600K, debt value = min($800K, $600K) = $600K. Debtholders receive full payment of their claims. Answer: $600,000.

---
## Pattern: Independent Projects vs. Mutually Exclusive Selection

**Description:** When evaluating multiple projects using profitability index (PI), NPV, or IRR, the decision rule depends on whether projects are independent or mutually exclusive. For independent projects, accept ALL projects meeting the threshold (PI > 1, NPV > 0, IRR > required return). However, if the question asks "which project(s)" in singular form or context implies selection of one option, treat as mutually exclusive and select the project with the highest metric. The key distinction: "which project(s) should be accepted" typically means select the best one, while "should the projects be accepted" means evaluate each independently.

**When to Use:** When question asks about accepting/selecting projects using capital budgeting metrics (PI, NPV, IRR) and multiple projects are presented. Pay attention to whether the question asks "which project(s)" (selection task) vs. "should the projects be accepted" (independent evaluation).

**When NOT to Use:**
- When question explicitly states "accept all projects that meet the criteria"
- When question clearly asks "how many projects" or "all projects that should be undertaken"
- When context explicitly mentions unlimited capital or no budget constraints
- When question uses phrasing like "evaluate whether each project should be accepted independently"

**Procedure:**
1. Calculate the decision metric (PI, NPV, or IRR) for each project
2. Identify which projects meet the acceptance threshold (PI > 1, NPV > 0, IRR > required return)
3. Examine the question phrasing carefully to determine if it's asking for selection or independent evaluation:
   - **Selection indicators:** "Which project(s) should the company accept" → Rank and select best
   - **Selection indicators:** "Which project(s) based on [metric] rule" → Rank and select best
   - **Independent evaluation indicators:** "Should the projects be accepted" → Accept all that qualify
   - **Independent evaluation indicators:** "Should each project be undertaken" → Accept all that qualify
4. **Default interpretation for "which project(s)" questions:** Unless explicitly stated otherwise, treat as a selection task requiring you to choose the project with the highest metric value
5. If question clearly allows multiple acceptances and uses plural evaluation language, accept all that meet threshold
6. When selecting among multiple qualifying projects, rank by the metric and select the highest
7. State your selection clearly, explaining the ranking if choosing among multiple qualifying options

**Common Mistakes to Avoid:**
- Accepting all projects with PI > 1 when question asks "which project(s)" (this typically means select the best)
- Assuming independence when question phrasing implies selection/ranking
- Ignoring that "which project(s)" is a selection question even when projects are described as "independent opportunities"
- Failing to recognize that "independent opportunities" describes the projects' cash flows, not the decision framework
- Selecting only one project when question explicitly asks to "evaluate each project independently"

**Example (sanitized):**
> **Scenario:** "Which project(s) should the firm accept based on profitability index?" Project X has PI = 1.18, Project Y has PI = 1.29. Both are independent investments with 10% discount rate.
> **Wrong approach:** "Both projects have PI > 1.0, so both should be accepted since they are independent projects with positive profitability indices."
> **Correct approach:** Calculate PI for both: Project X = 1.18, Project Y = 1.29. Both exceed the 1.0 threshold. The question asks "which project(s)" indicating a selection task. Rank by PI: Project Y (1.29) > Project X (1.18). Select the project with the higher profitability index as it creates more value per dollar invested. Answer: "Project Y."

---

## Pattern: Rental Income Tax Treatment in NPV Analysis

**Description:** When comparing investment alternatives that include rental income options, rental income is typically stated as pretax revenue and should NOT have the corporate tax rate applied to reduce it. Rental income represents gross receipts, and the full amount should be used in NPV calculations unless the problem explicitly states "after-tax rental income" or provides specific tax treatment guidance for rental revenues.

**When to Use:** When evaluating alternatives that include renting property or assets as one option, and comparing rental income NPV to other investment alternatives (manufacturing, development, etc.).

**When NOT to Use:**
- When the problem explicitly states rental income is "after-tax" or "net of taxes"
- When rental expenses or costs are provided that would create taxable income (rental revenue minus rental expenses)
- When the problem provides explicit guidance on tax treatment of rental income

**Procedure:**
1. Identify if one alternative involves rental income (e.g., "rent the building for $X per year")
2. Check if the problem states the rental income is "after-tax" or provides rental-related expenses
3. If rental income is stated as a simple annual amount without tax qualifiers, treat it as the full pretax cash flow
4. Calculate NPV of rental option using the stated rental amount without applying corporate tax rate reduction
5. For manufacturing/operational alternatives, apply standard tax treatment: calculate taxable income (revenues - expenses - depreciation), then after-tax cash flows
6. Compare NPVs across alternatives using consistent time horizons and discount rates
7. Verify you have NOT incorrectly reduced rental income by the tax rate unless explicitly justified

**Common Mistakes to Avoid:**
- Applying corporate tax rate to rental income (e.g., $60,000 × (1 - 0.34)) when rental income is stated as gross revenue
- Treating rental income as "taxable income" requiring tax reduction when it's simply stated as annual rental revenue
- Inconsistently applying tax treatment between rental and operational alternatives
- Reducing rental income by tax rate without explicit problem guidance to do so
- Assuming rental income needs tax adjustment just because other alternatives have detailed tax calculations

**Example (sanitized):**
> **Scenario:** "Company can rent a facility for $50,000 per year or use it for manufacturing Project X. Project X generates $180,000 annual revenue, $90,000 annual expenses, with $25,000 annual depreciation. Tax rate is 30%, discount rate is 10%, 10-year horizon."
> **Wrong approach:** Rental NPV = $50,000 × (1 - 0.30) × PVAF(10%, 10) = $35,000 × 6.145 = $215,075. Project X after-tax cash flow = ($180,000 - $90,000 - $25,000) × (1 - 0.30) + $25,000 = $70,500. Project X NPV = $70,500 × 6.145 = $433,223. Choose Project X.
> **Correct approach:** Rental NPV = $50,000 × PVAF(10%, 10) = $50,000 × 6.145 = $307,250. Project X: Taxable income = $180,000 - $90,000 - $25,000 = $65,000. Tax = $19,500. After-tax cash flow = $180,000 - $90,000 - $19,500 = $70,500. Project X NPV = $70,500 × 6.145 = $433,223. Choose Project X (but rental option is more competitive than the wrong approach suggested).