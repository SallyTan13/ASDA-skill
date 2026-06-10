# Pattern: Earnings_Dilution_vs_Value_Dilution

**Description:** Confusing earnings dilution (mechanical decrease in EPS from new share issuance) with value dilution or investment quality. Dilution occurs whenever EPS decreases after new equity issuance, regardless of whether the investment is fairly priced, maintains ROE/PE ratios, or creates shareholder value.

**When to Use:** Questions asking "does dilution occur?" or "is there dilution?" in contexts involving new equity issuance, share offerings, or investments financed by issuing stock.

**Procedure:**
1. Calculate current EPS = Net Income / Current Shares Outstanding
2. Determine new shares issued = Investment Amount / Current Share Price
3. Calculate incremental earnings from the new investment (using stated ROE, return rate, or earnings projections)
4. Calculate new EPS = (Old Net Income + Incremental Earnings) / (Old Shares + New Shares)
5. Compare new EPS to current EPS: if new EPS < current EPS, dilution occurs; if new EPS ≥ current EPS, no dilution
6. **Critical verification:** Dilution is determined SOLELY by the EPS comparison, NOT by whether the investment maintains PE ratio, ROE, or is "fairly priced" — these factors relate to value creation, not accounting dilution

**Example (sanitized):**
> **Scenario:** A firm with 100,000 shares, $50 share price, and $400,000 net income issues $1,000,000 in new equity for an investment earning the firm's current 16% ROE.
> **Wrong approach:** "No dilution because the investment earns the same ROE and maintains the PE ratio, so shareholder value per dollar is preserved."
> **Correct approach:** Current EPS = $400,000/100,000 = $4.00. New shares = $1,000,000/$50 = 20,000. New earnings = $1,000,000 × 16% = $160,000. New EPS = $560,000/120,000 = $4.67. Since $4.67 > $4.00, no dilution occurs. The answer depends only on whether EPS increased or decreased, not on investment quality.

---

# Pattern: Incremental_IRR_Decision_Rule_Application

**Description:** Failing to correctly apply the incremental IRR decision rule for mutually exclusive projects: when incremental IRR < required return, choose the smaller project; when incremental IRR > required return, choose the larger project. The confusion arises from computing the rule correctly but reversing the logic when selecting the project.

**When to Use:** Questions involving mutually exclusive project selection using incremental IRR analysis, especially when asked "which project should you choose based on incremental IRR?"

**Procedure:**
1. Identify the larger and smaller projects by initial investment
2. Calculate incremental cash flows = Larger Project Cash Flows - Smaller Project Cash Flows (for each period)
3. Compute the IRR of the incremental cash flows
4. Compare incremental IRR to the required return (hurdle rate)
5. **Apply decision rule:** If incremental IRR > required return, the additional investment is justified → choose larger project. If incremental IRR < required return, the additional investment destroys value → choose smaller project
6. Verify: The incremental IRR represents the return on the ADDITIONAL investment; if this return is insufficient, the extra capital should not be deployed

**Example (sanitized):**
> **Scenario:** Project A costs $500,000; Project B costs $1,200,000. Incremental IRR (B-A) = 9%. Required return = 12%.
> **Wrong approach:** "Since we calculated incremental IRR, choose the larger project B because it was part of the analysis."
> **Correct approach:** Incremental IRR (9%) < Required return (12%), meaning the additional $700,000 investment in B earns below the hurdle rate. This destroys value. Choose Project A. The incremental investment is not justified when its return falls short of what investors require.

---

# Pattern: Equity_as_Residual_Claim_in_Leverage

**Description:** Failing to recognize that equity value equals max(0, Firm Value - Debt) and that stockholders receive nothing when total liabilities exceed total assets, regardless of individual scenario contributions. Equity holders are residual claimants who only receive value after all debt obligations are satisfied.

**When to Use:** Questions about stock value, equity value, or stockholder claims in leveraged firms, especially in scenario analysis or merger contexts with debt obligations.

**Procedure:**
1. Calculate total firm value in the given scenario (sum all asset values or scenario-specific firm values)
2. Identify total debt obligations (face value of all debt claims)
3. Apply residual claim formula: Equity Value = max(0, Total Firm Value - Total Debt)
4. If Firm Value ≥ Total Debt: Equity Value = Firm Value - Total Debt
5. If Firm Value < Total Debt: Equity Value = $0 (firm is insolvent; stockholders receive nothing)
6. **Critical verification:** Do NOT confuse individual scenario contributions to firm value with equity claims; equity only has value after debt is fully satisfied

**Example (sanitized):**
> **Scenario:** Merged firm has total value $600,000 in a bad scenario. Total debt from both firms = $850,000.
> **Wrong approach:** "One firm contributed $300,000, so that's the stock value from that scenario."
> **Correct approach:** Equity Value = max(0, $600,000 - $850,000) = max(0, -$250,000) = $0. Since total debt exceeds firm value, the firm is insolvent and stockholders receive nothing. Debtholders have priority and would only recover $600,000 of their $850,000 claim.

---

# Pattern: Debt_Market_Value_in_Distress

**Description:** Confusing the face value (contractual obligation) of debt with its market value (economic recovery value) in distressed or bankruptcy scenarios. When firm value is less than total debt claims, debt market value equals the firm's total value, not the face value of the debt.

**When to Use:** Questions asking for "debt value," "value of debt claim," or "end-of-period debt value" in scenarios where firm value may be insufficient to cover all obligations.

**Procedure:**
1. Identify total debt face value (contractual amount owed)
2. Calculate total firm value in the given scenario
3. Apply debt valuation rule: Debt Market Value = min(Debt Face Value, Total Firm Value)
4. If Firm Value ≥ Debt Face Value: Debt is fully covered → Debt Market Value = Debt Face Value
5. If Firm Value < Debt Face Value: Firm cannot pay in full → Debt Market Value = Total Firm Value (debtholders receive everything, but it's less than owed)
6. **Critical verification:** In distress/bankruptcy, debtholders can only recover what exists; the market value reflects actual recovery, not what is contractually owed

**Example (sanitized):**
> **Scenario:** Merged firm has total value $520,000. Combined debt face value = $1,100,000.
> **Wrong approach:** "The debt value is $1,100,000 because that's what the firm owes."
> **Correct approach:** Debt Market Value = min($1,100,000, $520,000) = $520,000. The firm is insolvent and can only pay $520,000 to debtholders, even though $1,100,000 is owed. The market value of debt reflects actual recovery ($520,000), not the contractual obligation ($1,100,000).

---

# Pattern: Cash_Flow_to_Stockholders_Comprehensive_Measure

**Description:** Treating "cash flow to stockholders" as synonymous with "dividends paid" rather than as the comprehensive net cash flow between the firm and equity holders, which includes both dividends and net equity repurchases/issuances (changes in equity beyond retained earnings).

**When to Use:** Questions asking to "calculate cash flow to stockholders" or "cash flow to equity" when balance sheet data showing owners' equity changes is available.

**Procedure:**
1. Identify dividends paid during the period (from income statement or cash flow statement)
2. Calculate change in owners' equity = Ending OE - Beginning OE
3. Identify additions to retained earnings (from income statement: Net Income - Dividends)
4. Calculate net new equity issued = Change in OE - Additions to RE
5. Apply formula: Cash Flow to Stockholders = Dividends Paid - Net New Equity Issued
6. Alternative formula: Cash Flow to Stockholders = Dividends - (Ending OE - Beginning OE - Additions to RE)
7. **Interpretation:** Positive value = net cash to stockholders; negative value = net cash from stockholders (they invested more than they received)
8. **Critical verification:** Cash flow to stockholders captures ALL cash movements with equity holders, not just dividends; equity buybacks increase it, new issuances decrease it

**Example (sanitized):**
> **Scenario:** Dividends = $800. Beginning OE = $25,000. Ending OE = $26,200. Net Income = $2,000.
> **Wrong approach:** "Cash flow to stockholders = $800 (dividends paid)."
> **Correct approach:** Additions to RE = $2,000 - $800 = $1,200. Change in OE = $26,200 - $25,000 = $1,200. Net new equity = $1,200 - $1,200 = $0. Cash Flow to Stockholders = $800 - $0 = $800. In this case they happen to equal, but if OE changed by more than retained earnings (e.g., $1,500 change), net new equity = $1,500 - $1,200 = $300, so cash flow to stockholders = $800 - $300 = $500.

## Pattern: Earnings_Dilution_vs_Value_Dilution

**Description:** Confusing earnings dilution (mechanical decrease in EPS from new share issuance) with value dilution or investment quality. Dilution occurs whenever EPS decreases after new equity issuance, regardless of whether the investment is fairly priced, maintains ROE/PE ratios, or creates shareholder value. When a question asks "does dilution occur?" or "is there dilution?" without qualifiers like "economic" or "value," it asks about accounting/EPS dilution ONLY.

**When to Use:** Questions asking "does dilution occur?" or "is there dilution?" in contexts involving new equity issuance, share offerings, or investments financed by issuing stock.

**Procedure:**
1. Calculate current EPS = Net Income / Current Shares Outstanding
2. Determine new shares issued = Investment Amount / Current Share Price
3. Calculate incremental earnings from the new investment (using stated ROE, return rate, or earnings projections)
4. Calculate new EPS = (Old Net Income + Incremental Earnings) / (Old Shares + New Shares)
5. Compare new EPS to current EPS numerically
6. **Apply dilution determination rule (MANDATORY):** 
   - If new EPS < current EPS → The ONLY valid answer is: "YES, dilution occurs"
   - If new EPS ≥ current EPS → The ONLY valid answer is: "NO, dilution does not occur"
7. **State your final answer:** Your answer MUST match step 6 exactly. Write: "Answer: [YES/NO], dilution [does/does not] occur."
8. **CRITICAL ENFORCEMENT:** After stating your answer from step 7, STOP. Do NOT:
   - Reverse or contradict your answer based on ROE maintenance, PE ratio preservation, or value creation
   - Add qualifications like "but no economic dilution occurs"
   - Discuss whether the investment is "fairly priced" or "creates shareholder value"
   - These factors are IRRELEVANT to the question unless it explicitly asks about "economic dilution" or "value dilution"
9. **Final verification:** Re-read your answer. If it does not match the result from step 6, you have made an error. Correct it immediately.

**Example (sanitized):**
> **Scenario:** A firm with 50,000 shares, $60 share price, and $250,000 net income issues $600,000 in new equity for an investment earning the firm's current 12% ROE.
> **Wrong approach:** "Current EPS = $5.00, new EPS = $4.64. EPS decreased, so accounting dilution occurs. However, since the investment earns the same ROE and maintains the PE ratio, no economic dilution occurs. Answer: No dilution."
> **Correct approach:** Current EPS = $250,000/50,000 = $5.00. New shares = $600,000/$60 = 10,000. New earnings = $600,000 × 12% = $72,000. New EPS = $322,000/60,000 = $5.37. Since $5.37 > $5.00, Answer: NO, dilution does not occur. [STOP HERE - do not discuss value creation or ROE maintenance]

**Common Mistakes to Avoid:**
- Calculating that new EPS < current EPS but then answering "no dilution" based on ROE maintenance or value creation arguments
- Correctly identifying EPS decreased but qualifying the answer with "only accounting dilution, not economic dilution"
- Reversing the correct answer after initially stating it correctly
- Treating "does dilution occur?" as asking about value dilution when it asks about EPS dilution

---
## Pattern: Incremental_IRR_Decision_Rule_Application

**Description:** Failing to correctly apply the incremental IRR decision rule for mutually exclusive projects. The rule requires: (1) correctly identifying which project is larger by initial investment, (2) computing incremental cash flows as (Larger - Smaller), (3) accurately calculating the incremental IRR, and (4) applying the decision logic: when incremental IRR < required return, choose the smaller project; when incremental IRR > required return, choose the larger project. Common errors include miscalculating the incremental IRR or reversing the decision rule. Critical emphasis must be placed on verifying IRR calculations through multiple methods, as even small calculation errors reverse the final decision.

**When to Use:** Questions involving mutually exclusive project selection using incremental IRR analysis, especially when asked "which project should you choose based on incremental IRR?" or "based on the incremental IRR, which project should be chosen?"

**Procedure:**
1. Identify the larger and smaller projects by comparing initial investment amounts (absolute value)
2. **Verify project ordering:** Explicitly state which project has the larger initial investment and which has the smaller initial investment
3. Calculate incremental cash flows = Larger Project Cash Flows - Smaller Project Cash Flows (for each period, including Year 0)
4. **Compute incremental IRR with MANDATORY multi-method verification:**
   - Method 1: Calculate the IRR of the incremental cash flows using standard IRR formula or financial calculator
   - Method 2: Verify by substituting the calculated IRR back into the NPV equation: NPV = Σ(Incremental CF_t / (1+IRR)^t) should equal approximately zero
   - Method 3: Test boundary conditions - calculate NPV of incremental cash flows at the required return rate to determine if incremental IRR is above or below it
   - **If any verification method contradicts the initial calculation, RECALCULATE using an alternative approach**
   - **Record the verified IRR explicitly:** "Verified Incremental IRR = [X]%"
5. Compare incremental IRR to the required return (hurdle rate)
6. **Apply decision rule with explicit logic check:** 
   - If incremental IRR > required return → the additional investment in the larger project earns above the hurdle rate → choose the LARGER project
   - If incremental IRR < required return → the additional investment earns below the hurdle rate → choose the SMALLER project
   - **State the logic explicitly:** "Since [incremental IRR] [>/< ] [required return], the additional investment [is/is not] justified, so I choose the [LARGER/SMALLER] project."
7. **Cross-check your answer against the decision rule:** 
   - If incremental IRR > required return, verify you chose the LARGER project
   - If incremental IRR < required return, verify you chose the SMALLER project
   - State explicitly: "Since incremental IRR [comparison] required return, I choose [project name], which is the [larger/smaller] project with initial investment of [amount]."
8. **Final verification checklist:**
   - ✓ IRR calculation verified through multiple methods
   - ✓ Comparison to required return is correct
   - ✓ Decision rule applied correctly (larger if IRR > required, smaller if IRR < required)
   - ✓ Final answer matches the size category indicated by the decision rule

**Example (sanitized):**
> **Scenario:** Project Alpha costs $1,200,000 with cash flows $420,000, $480,000, $540,000. Project Beta costs $2,000,000 with cash flows $680,000, $760,000, $840,000. Required return = 11%.
> **Wrong approach:** "Beta is larger. Incremental CF: -$800,000, $260,000, $280,000, $300,000. Quick calculation gives IRR ≈ 9%. Since 9% < 11%, choose Beta because it was in the calculation."
> **Correct approach:** 
> - Beta ($2,000,000) is larger; Alpha ($1,200,000) is smaller
> - Incremental CF (Beta - Alpha): Year 0: -$800,000; Year 1: $260,000; Year 2: $280,000; Year 3: $300,000
> - Method 1: Calculate IRR ≈ 12.8%
> - Method 2: Verify NPV at 12.8%: -$800,000 + $260,000/1.128 + $280,000/1.128² + $300,000/1.128³ ≈ $0 ✓
> - Method 3: NPV at 11% = -$800,000 + $260,000/1.11 + $280,000/1.11² + $300,000/1.11³ ≈ $11,500 > 0, confirming IRR > 11% ✓
> - Verified Incremental IRR = 12.8%
> - Since 12.8% > 11%, the additional investment is justified
> - Choose the larger project: Beta
> - Verification: Beta is the larger project at $2,000,000 ✓
> - Final checklist: IRR verified ✓, comparison correct ✓, decision rule applied ✓, answer matches larger project ✓

**Common Mistakes to Avoid:**
- Miscalculating the incremental IRR without verification through multiple methods
- Correctly calculating that incremental IRR < required return but then choosing the larger project
- Failing to verify the IRR calculation before applying the decision rule
- Assuming the project used as the base in the incremental calculation should automatically be chosen
- **Making arithmetic errors in IRR calculation that reverse the decision (e.g., calculating 8.9% when true IRR is 12%)**
- **Not testing the IRR calculation by computing NPV at the required return to verify which side of the hurdle rate the IRR falls on**
- **Skipping the cross-check between the decision rule outcome and the final project selection**
## Pattern: Cash_Flow_to_Stockholders_Comprehensive_Measure

**Description:** Treating "cash flow to stockholders" as synonymous with "dividends paid" rather than as the comprehensive net cash flow between the firm and equity holders, which includes both dividends and net equity repurchases/issuances (changes in equity beyond retained earnings). Special care is needed when net new equity is negative (representing net repurchases or equity reductions), as subtracting a negative value requires adding the absolute value.

**When to Use:** Questions asking to "calculate cash flow to stockholders" or "cash flow to equity" when balance sheet data showing owners' equity changes is available.

**Procedure:**
1. Identify dividends paid during the period (from income statement or cash flow statement)
2. Calculate change in owners' equity = Ending OE - Beginning OE
3. Identify additions to retained earnings = Net Income - Dividends Paid
4. Calculate net new equity issued = Change in OE - Additions to RE
5. **Interpret net new equity sign:**
   - If positive: firm issued new equity (received cash from stockholders)
   - If negative: firm reduced equity through repurchases or other means (paid cash to stockholders beyond dividends)
6. **Apply formula with explicit arithmetic for negative values:**
   - Formula: Cash Flow to Stockholders = Dividends Paid - Net New Equity Issued
   - If net new equity is POSITIVE (e.g., +$300): CF to Stockholders = Dividends - $300
   - If net new equity is NEGATIVE (e.g., -$500): CF to Stockholders = Dividends - (-$500) = Dividends + $500
7. **Execute the arithmetic carefully:**
   - Write out the substitution: "CF to Stockholders = $[dividends] - ($[net new equity])"
   - If net new equity is negative, explicitly convert: "= $[dividends] - (-$[absolute value]) = $[dividends] + $[absolute value]"
   - Calculate the final sum/difference
8. **Verify the arithmetic:**
   - If net new equity was negative, verify that you ADDED its absolute value to dividends
   - Double-check: Subtracting a negative = Adding a positive
   - Recalculate to confirm the final number
9. **Interpretation:** Positive value = net cash to stockholders; negative value = net cash from stockholders (they invested more than they received)

**Example (sanitized):**
> **Scenario:** Dividends = $900. Beginning OE = $22,000. Ending OE = $22,700. Net Income = $1,800.
> **Wrong approach:** "Additions to RE = $900, Change in OE = $700, Net new equity = -$200. Cash flow = $900 - (-$200) = $700."
> **Correct approach:** 
> - Additions to RE = $1,800 - $900 = $900
> - Change in OE = $22,700 - $22,000 = $700
> - Net new equity = $700 - $900 = -$200 (negative means equity reduction)
> - Cash Flow to Stockholders = $900 - (-$200)
> - Convert negative: = $900 + $200 = $1,100
> - Verify: Net new equity is negative, so I added $200 to dividends ✓
> - Answer: $1,100

**Common Mistakes to Avoid:**
- Reporting only dividends as cash flow to stockholders when equity changes occurred
- Incorrectly handling negative net new equity by subtracting instead of adding
- Writing "Dividends - (-X)" but then calculating "Dividends - X" instead of "Dividends + X"
- Failing to verify the arithmetic when net new equity is negative
- Forgetting that "subtracting a negative" means "adding the positive equivalent"

---
## Pattern: Bond_Covenant_Payment_Indifference_Calculation

**Description:** Determining the bond payment amount in a covenant that makes stockholders indifferent between two projects with different risk profiles. This requires setting up an indifference equation using expected equity values under limited liability (equity = max(project payoff - bond payment, 0)), solving for the covenant payment algebraically, and verifying the solution is consistent with the assumed constraint region. The mathematically derived solution that creates exact indifference is the ONLY valid answer—do not adjust or round the solution based on intuition or "practical" considerations.

**When to Use:** Questions asking for a bond covenant payment that makes stockholders indifferent between high-volatility and low-volatility projects, or questions about what payment would eliminate stockholder incentive to choose a riskier project.

**When NOT to Use:**
- Questions asking for approximate or threshold payments rather than exact indifference
- Scenarios where the question explicitly asks for a "practical" or "rounded" answer
- Cases where multiple constraint regions yield different valid solutions (though this is rare)

**Procedure:**
1. Calculate expected equity value for the baseline project (usually low-volatility) with the original bond payment:
   - For each state: Equity = max(Project Payoff - Bond Payment, 0)
   - Expected Equity = Σ(Probability × Equity in each state)
2. Set up the indifference equation for the alternative project (usually high-volatility) with unknown covenant payment X:
   - For each state: Equity = max(Project Payoff - X, 0)
   - Expected Equity = Σ(Probability × max(Payoff - X, 0))
3. **Identify constraint regions:** Determine the threshold values where limited liability becomes binding (where project payoff = X in any state)
4. **Assume a constraint region:** Start with the most likely region (e.g., if the lowest payoff is $3,000 and original payment is $3,500, assume X > $3,000)
5. Apply the assumed constraint to simplify the indifference equation:
   - States where Payoff < X: Equity = 0
   - States where Payoff ≥ X: Equity = Payoff - X
6. Solve the indifference equation algebraically for X
7. **Record the mathematically derived solution:** Write explicitly: "Mathematical solution: X = $[amount]"
8. **Verify solution consistency:** Check that the solved value of X satisfies the assumed constraint region
   - If X violates the assumption, try a different constraint region and re-solve
   - The correct solution must be mathematically consistent with its constraint assumptions
9. **Verify indifference is achieved:** Substitute X back into the alternative project's expected equity formula and confirm it equals the baseline expected equity
   - Calculate: Σ(Probability × max(Payoff - X, 0)) using the solved X
   - This MUST equal the baseline expected equity from step 1
   - If not equal, you have made an arithmetic error—recalculate
10. **State final answer:** "The covenant payment is $[exact amount from step 7]"
11. **CRITICAL: Output the mathematically exact solution:** After deriving and verifying the solution, that IS the final answer. Do NOT:
    - Adjust the answer to a "rounder" number without mathematical justification
    - Second-guess the solution because it "seems high/low" or is not a round number
    - Change the answer based on intuition, "practical considerations," or "threshold" reasoning
    - Add qualifications like "but $X is the practical answer" after calculating the correct value
    - The mathematically derived and verified solution is the ONLY valid answer
12. **Final arithmetic verification:** Before stating your final answer, recalculate the verification from step 9 one more time to catch any arithmetic errors

**Example (sanitized):**
> **Scenario:** Low-vol project pays $4,200 (bad, p=0.5) or $4,800 (good, p=0.5). High-vol project pays $3,600 (bad) or $5,400 (good). Original bond = $4,200. Find covenant payment X for high-vol creating indifference.
> **Wrong approach:** "Set up equation, solve to get X = $5,000. But that's not a round number, so the practical answer is $5,100 or maybe $4,900."
> **Correct approach:** 
> - Low-vol expected equity: 0.5×max(4,200-4,200,0) + 0.5×max(4,800-4,200,0) = 0.5(0) + 0.5(600) = $300
> - Assume X > 3,600: 0.5×max(3,600-X,0) + 0.5×max(5,400-X,0) = 300
> - If X > 3,600: 0.5(0) + 0.5(5,400-X) = 300 → 5,400-X = 600 → X = $4,800
> - Mathematical solution: X = $4,800
> - Verify: $4,800 > $3,600 ✓ (assumption satisfied)
> - Verify indifference: 0.5×max(3,600-4,800,0) + 0.5×max(5,400-4,800,0) = 0.5(0) + 0.5(600) = $300 ✓
> - The covenant payment is $4,800 [This is the final answer—do NOT adjust]

**Common Mistakes to Avoid:**
- Solving the equation correctly but then arbitrarily adjusting the answer to a "rounder" number
- Calculating the correct solution but then hedging with "but $X is the practical answer"
- Introducing "threshold" or "practical" reasoning after deriving the exact mathematical solution
- Changing the mathematically derived solution based on intuition rather than verification
- Failing to verify that the solution satisfies the constraint assumptions
- Not checking that the solution actually creates exact indifference by substituting back
- Making arithmetic errors in the verification step and not catching them before stating the final answer
- Second-guessing a non-round number solution (e.g., $4,100) in favor of a round number (e.g., $4,000)
## Pattern: Debt_Market_Value_in_Distress

**Description:** Confusing the face value (contractual obligation) of debt with its market value (economic recovery value) in distressed or bankruptcy scenarios. When firm value is less than total debt claims, debt market value equals the firm's total value, not the face value of the debt. In finance, "value of debt" means market value (what it's worth) unless explicitly stated as "face value" or "contractual obligation."

**When to Use:** Questions asking for "debt value," "value of debt claim," or "end-of-period debt value" in scenarios where firm value may be insufficient to cover all obligations.

**When NOT to Use:** 
- Questions explicitly asking for "face value of debt" or "contractual debt obligation"
- Questions asking for "debt owed" rather than "debt value"

**Procedure:**
1. Identify total debt face value (contractual amount owed)
2. Calculate total firm value in the given scenario
3. Apply debt valuation rule: Debt Market Value = min(Debt Face Value, Total Firm Value)
4. If Firm Value ≥ Debt Face Value: Debt is fully covered → Debt Market Value = Debt Face Value
5. If Firm Value < Debt Face Value: Firm cannot pay in full → Debt Market Value = Total Firm Value (debtholders receive everything, but it's less than owed)
6. **Record the calculated debt market value:** Write down explicitly: "Calculated Debt Market Value = $[amount]"
7. **State your final answer directly:** "The value of debt is $[amount from step 6]"
8. **CRITICAL: Do NOT second-guess:** After calculating the debt market value in step 3, that IS the answer. Do NOT:
   - Question whether "value" means market value or face value (it means market value)
   - Explore alternative interpretations
   - Introduce circular reasoning about "what the question really asks"
   - The standard financial convention is clear: "debt value" = market value
9. **Final verification:** Your answer must equal the result from step 3. If you stated the correct calculation but output a different number, you have made an error.

**Example (sanitized):**
> **Scenario:** Firm has total value $400,000. Debt face value = $650,000.
> **Wrong approach:** "Debt market value = min($650,000, $400,000) = $400,000. But maybe 'value' means face value, so the answer could be $650,000..."
> **Correct approach:** Debt face value = $650,000. Firm value = $400,000. Debt Market Value = min($650,000, $400,000) = $400,000. Calculated Debt Market Value = $400,000. The value of debt is $400,000. [STOP - this is the answer]

**Common Mistakes to Avoid:**
- Correctly calculating debt market value but then questioning whether "value" means market value or face value
- Introducing circular reasoning about alternative interpretations after arriving at the correct answer
- Conflating "debt value" (market value = what it's worth) with "debt obligation" (face value = what is owed)
- Outputting face value when the question asks for "value" in a distress scenario

---
## Pattern: Equity_as_Residual_Claim_in_Leverage

**Description:** Failing to recognize that equity value equals max(0, Firm Value - Debt) and that stockholders receive nothing when total liabilities exceed total assets, regardless of individual scenario contributions. Equity holders are residual claimants who only receive value after all debt obligations are satisfied. This pattern also applies when comparing firm values versus equity values - questions asking about "firm value" or "expected value of the firm" require calculating total expected payoffs WITHOUT applying the residual claim formula, while questions about "stock value" or "equity value" require applying the max(0, Firm Value - Debt) formula.

**When to Use:** 
- Questions about stock value, equity value, or stockholder claims in leveraged firms, especially in scenario analysis or merger contexts with debt obligations
- Questions asking "which strategy/project maximizes expected firm value" or "which has higher firm value" when comparing leveraged projects
- Questions comparing firm value versus equity value in contexts where debt obligations exist
- Any question where distinguishing between total firm value and residual equity value is critical

**Procedure:**
1. **Identify what the question asks for:**
   - If asking for "firm value," "expected value of the firm," or "total value": Calculate expected payoffs directly (skip to step 8)
   - If asking for "stock value," "equity value," or "stockholder claims": Continue to step 2
2. Calculate total firm value in the given scenario (sum all asset values or scenario-specific firm values)
3. Identify total debt obligations (face value of all debt claims)
4. Apply residual claim formula: Equity Value = max(0, Total Firm Value - Total Debt)
5. If Firm Value ≥ Total Debt: Equity Value = Firm Value - Total Debt
6. If Firm Value < Total Debt: Equity Value = $0 (firm is insolvent; stockholders receive nothing)
7. **Record the calculated equity value:** Write down explicitly: "Calculated Equity Value = $[amount]"
8. **For firm value comparisons:** Calculate expected firm value = Σ(Probability × Payoff in each state) for each option. The option with higher expected firm value maximizes firm value, regardless of debt levels or equity implications.
9. **Critical verification:** 
   - For equity questions: Verify that your final answer equals the result from step 4/5/6, NOT any individual firm value component
   - For firm value questions: Verify that you compared total expected payoffs, NOT equity values after debt
10. **State final answer:** 
    - For equity: "The stock value is $[amount from step 7]"
    - For firm value: "Project [X] maximizes expected firm value" or "Both have equal expected firm value"

**Example (sanitized):**
> **Scenario 1 (Equity value):** Merged firm has total value $750,000 in scenario A. Total debt from both firms = $950,000.
> **Wrong approach:** "Firm value = $750,000, debt = $950,000, so equity = max(0, -$200,000) = $0. But one firm contributed $400,000, so stock value is $400,000."
> **Correct approach:** Total firm value = $750,000. Total debt = $950,000. Equity Value = max(0, $750,000 - $950,000) = max(0, -$200,000) = $0. Calculated Equity Value = $0. The stock value is $0.

> **Scenario 2 (Firm value comparison):** Project A pays $8,000 (prob 0.4) or $12,000 (prob 0.6). Project B pays $6,000 (prob 0.4) or $14,000 (prob 0.6). Debt = $7,500. Which maximizes expected firm value?
> **Wrong approach:** "Project A equity: 0.4×max(8,000-7,500,0) + 0.6×max(12,000-7,500,0) = $2,900. Project B equity: 0.4×max(6,000-7,500,0) + 0.6×max(14,000-7,500,0) = $3,900. Project B maximizes firm value."
> **Correct approach:** Question asks for firm value, not equity value. Project A expected firm value = 0.4($8,000) + 0.6($12,000) = $10,400. Project B expected firm value = 0.4($6,000) + 0.6($14,000) = $10,800. Project B maximizes expected firm value because $10,800 > $10,400. (Note: Debt is irrelevant when comparing firm values.)

**Common Mistakes to Avoid:**
- Correctly calculating equity = $0 but reporting an individual firm's value as the answer
- Confusing individual scenario contributions to firm value with equity claims
- Outputting intermediate values instead of the final equity calculation result
- Failing to verify that the final answer matches the calculated equity value
- **Applying the residual claim formula when the question asks about firm value rather than equity value**
- **Conflating "maximizing firm value" with "maximizing equity value" - these can differ when debt is present**
- **Considering debt obligations when comparing firm values (debt only matters for equity value calculations)**

---
## Pattern: Bond_Covenant_Payment_Consistency_Verification

**Description:** When solving for a bond covenant payment that creates stockholder indifference between projects, students may correctly set up and solve the indifference equation but then arbitrarily adjust or second-guess the mathematically derived answer without proper justification. The solution must be both mathematically correct AND consistent with the constraint assumptions used during solving.

**When to Use:** Questions asking for a bond covenant payment that makes stockholders indifferent between high-volatility and low-volatility projects, or questions about what payment would eliminate stockholder incentive to choose a riskier project.

**Procedure:**
1. Calculate expected equity value for the baseline project (usually low-volatility) with the original bond payment:
   - For each state: Equity = max(Project Payoff - Bond Payment, 0)
   - Expected Equity = Σ(Probability × Equity in each state)
2. Set up the indifference equation for the alternative project (usually high-volatility) with unknown covenant payment X:
   - For each state: Equity = max(Project Payoff - X, 0)
   - Expected Equity = Σ(Probability × max(Payoff - X, 0))
3. **Identify constraint regions:** Determine the threshold values where limited liability becomes binding (where project payoff = X in any state)
4. **Assume a constraint region:** Start with the most likely region (e.g., if the lowest payoff is $3,000 and original payment is $3,500, assume X > $3,000)
5. Apply the assumed constraint to simplify the indifference equation:
   - States where Payoff < X: Equity = 0
   - States where Payoff ≥ X: Equity = Payoff - X
6. Solve the indifference equation algebraically for X
7. **Record the mathematically derived solution:** Write explicitly: "Mathematical solution: X = $[amount]"
8. **Verify solution consistency:** Check that the solved value of X satisfies the assumed constraint region
   - If X violates the assumption, try a different constraint region and re-solve
   - The correct solution must be mathematically consistent with its constraint assumptions
9. **Verify indifference is achieved:** Substitute X back into the alternative project's expected equity formula and confirm it equals the baseline expected equity
10. **State final answer:** "The covenant payment is $[amount from step 7]"
11. **CRITICAL: Do NOT arbitrarily adjust:** After deriving the mathematical solution and verifying consistency, that IS the answer. Do NOT:
    - Adjust the answer to a "rounder" number without mathematical justification
    - Second-guess the solution because it "seems high/low"
    - Change the answer based on intuition rather than calculation
    - The mathematically derived and verified solution is the ONLY valid answer

**Example (sanitized):**
> **Scenario:** Low-vol project pays $5,000 (bad, p=0.6) or $5,500 (good, p=0.4). High-vol project pays $4,000 (bad) or $6,200 (good). Original bond = $4,800. Find covenant payment X for high-vol creating indifference.
> **Wrong approach:** "Set up equation, solve to get X = $5,300. But that seems high, so adjust to X = $5,000."
> **Correct approach:** 
> - Low-vol expected equity: 0.6×max(5,000-4,800,0) + 0.4×max(5,500-4,800,0) = 0.6(200) + 0.4(700) = $400
> - Assume X > 4,000: 0.6×max(4,000-X,0) + 0.4×max(6,200-X,0) = 400
> - If X > 4,000: 0.6(0) + 0.4(6,200-X) = 400 → 6,200-X = 1,000 → X = $5,200
> - Mathematical solution: X = $5,200
> - Verify: $5,200 > $4,000 ✓ (assumption satisfied)
> - Verify indifference: 0.4(6,200-5,200) = 0.4(1,000) = $400 ✓
> - The covenant payment is $5,200 [Do NOT adjust this answer]

**Common Mistakes to Avoid:**
- Solving the equation correctly but then arbitrarily adjusting the answer
- Changing the mathematically derived solution to a "rounder" number without justification
- Second-guessing the solution based on intuition rather than verification
- Failing to verify that the solution satisfies the constraint assumptions
- Not checking that the solution actually creates indifference by substituting back