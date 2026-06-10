# Skill Patterns for Corporate Finance Concept Confusion

## Pattern: Debt Aggregation in Mergers

**Description:** When two firms with debt merge, the combined firm's total debt obligation equals the sum of both firms' individual debt claims, not just one firm's debt. This aggregated debt must be subtracted from combined firm value to calculate equity value.

**When to Use:** Merger problems involving firms with outstanding debt; keywords: "merge," "combined company," "outstanding debt," "each company has debt"

**Procedure:**
1. Identify each firm's debt face value before the merger
2. Calculate total debt post-merger: sum all individual debt claims from both firms
3. For each state of nature, calculate combined firm value by summing individual firm values in that state
4. Calculate equity value in each state: max(0, Combined Firm Value - Total Debt)
5. Verify that you've used the sum of both debt claims, not just one firm's debt

**Example (sanitized):**
> **Scenario:** Firm A (value $300k, debt $200k) merges with Firm B (value $400k, debt $150k).
> **Wrong approach:** Combined equity = ($300k + $400k) - $200k = $500k (using only one firm's debt)
> **Correct approach:** Total debt = $200k + $150k = $350k; Combined firm value = $700k; Equity value = $700k - $350k = $350k

---

## Pattern: Debt as Contingent Claim with Absolute Priority

**Description:** Debt value in any state equals min(Face Value of All Debt, Total Firm Value in that State). When firm value is insufficient to cover all debt, debtholders receive the entire firm value (absolute priority), leaving equity holders with zero due to limited liability. In merger contexts, debt value refers to the total combined debt of the merged entity unless specifically asked for individual portions. The calculated debt or equity value IS the final answer—do not substitute with face values or other intermediate calculations.

**When to Use:** Questions asking for debt value or equity value in specific states; keywords: "value of debt," "value of stock," "end-of-period," "state," "scenario," "after the merger," "possible value," "debt after the merger," "end-of-period debt"

**When NOT to Use:** When the question asks for expected values across multiple states (use expected value calculations instead); when the question asks about wealth transfer effects (use Wealth Transfer pattern instead)

**Procedure:**
1. Identify total face value of all debt claims (sum all debt from all firms if merger)
2. Calculate total firm value in the specific state being analyzed
3. Apply the debt valuation rule: Debt Value = min(Total Face Value, Firm Value in State)
4. Calculate equity value as the residual: Equity Value = max(0, Firm Value - Total Debt Face Value)
5. Verify: if Firm Value < Total Debt Face Value, then Debt gets entire Firm Value and Equity = $0
6. Verify: if Firm Value ≥ Total Debt Face Value, then Debt gets Face Value and Equity gets the remainder
7. **Determine what the question is asking for:**
   - If "debt value after merger" or "end-of-period debt after merger" → the value from step 3 IS your final answer
   - If "equity value after merger" or "stock value after merger" → the value from step 4 IS your final answer
   - If "debt value" for a single firm (no merger context) → report that firm's debt value from step 3
8. **CRITICAL - Final answer checkpoint:** 
   - The value calculated in step 3 (for debt) or step 4 (for equity) is your FINAL ANSWER
   - DO NOT substitute with debt face values, per-firm portions, or any other intermediate calculations
   - DO NOT revert to individual firm debt face values after calculating combined debt value
   - Your final numerical answer MUST exactly match the value calculated in the relevant step
9. **Final answer verification:** Re-read the question to confirm your answer matches what was asked (total vs. per-firm, debt vs. equity vs. firm value) and that you reported the calculated value, not a face value or intermediate result

**Example (sanitized):**
> **Scenario:** Two firms merge with combined debt face value of $1,200k. In State A, combined firm value = $900k. In State B, combined firm value = $1,500k.
> **Question:** "What is the value of debt after the merger in State A?"
> **Wrong approach #1:** Calculating correctly as $900k but then reporting $600k (one firm's debt face value)
> **Wrong approach #2:** Calculating correctly as $900k but then reporting $1,200k (total debt face value)
> **Correct approach:** 
> - Total debt face value = $1,200k
> - Firm value in State A = $900k
> - Debt value = min($1,200k, $900k) = $900k
> - Question asks for "debt after merger" → the calculated value $900k IS the final answer
> - Report: $900k (do NOT substitute with face value or per-firm amount)
> - Verification: Question asked for debt (not equity), after merger (not single firm), in State A (not expected value) ✓

**Common Mistakes to Avoid:**
- Reporting individual company debt face values instead of calculated total combined debt value when question asks about merged entity
- Calculating the correct combined value but then reverting to face values or single-company perspective in the final answer
- Substituting the calculated debt value with the debt face value when reporting the answer
- Confusing what the question asks for (debt vs. equity vs. firm value)
- Assuming debt always equals face value regardless of firm value in that state

---
## Pattern: Independent State Variables in Mergers

**Description:** When merging firms face independent state variables (e.g., weather in different locations), each joint state combines one outcome from each firm. The combined firm value in a joint state equals the sum of individual firm values in their respective individual states. **CRITICAL: When firms are identical (same state-value mappings), both firms experience the same state simultaneously, and you must use each firm's value in that shared state.** After calculating combined firm value, debt and equity must be valued separately using contingent claims logic when asked for those specific components. The calculated value IS the final answer—do not substitute with other values.

**When to Use:** Merger problems with independent uncertainty; keywords: "independent," "different towns/locations," "State A-State B" notation (e.g., "Rain-Warm"); questions asking for "value of stock," "value of debt," "value of combined company," or "value of firm" in specific states; **also applies when merging identical firms with the same state-value structure**

**When NOT to Use:** When states are not independent (e.g., same economy affects both firms); when the question asks for expected values across all states rather than specific state values

**Procedure:**
1. **Identify if firms are identical or different:**
   - If firms have different state-value mappings → they are different firms
   - If firms have the same state-value mappings → they are identical firms
2. **CRITICAL - Data reading verification for identical firms:**
   - If firms are identical, verify you're reading from a SINGLE value table that applies to BOTH firms
   - Each state should have ONE value that applies to each firm individually
   - Do NOT misread different rows as different firms' values
   - Example: If table shows "Rainy: $230k, Warm: $450k, Hot: $905k" for identical firms, then EACH firm has value $230k in Rainy, $450k in Warm, $905k in Hot
3. **For different firms:** Recognize that "State A-State B" means Firm 1 experiences State A while Firm 2 experiences State B
4. **For identical firms:** Recognize that "State A-State A" means both firms experience State A simultaneously (since they're identical, they face the same states)
5. Look up Firm 1's value in its state from the given data
6. Look up Firm 2's value in its state from the given data (for identical firms, this will be the same state as Firm 1, using the same value from the table)
7. Calculate combined firm value (total assets): Firm 1 Value + Firm 2 Value
8. **Determine what the question is asking for:**
   - If "combined company value" or "combined firm value" → the value from step 7 IS your final answer—STOP HERE and report this value
   - If "equity value" or "stock value" → continue to step 9
   - If "debt value" → continue to step 10
9. **For equity value:** Calculate total debt face value (sum of all debt from both firms), then Equity = max(0, Combined Firm Value - Total Debt Face Value). This calculated equity value IS your final answer.
10. **For debt value:** Calculate total debt face value (sum of all debt from both firms), then Debt = min(Total Debt Face Value, Combined Firm Value). This calculated debt value IS your final answer.
11. **CRITICAL - Answer checkpoint:**
   - If question asks for "combined company value" → report step 7 value directly, do NOT calculate debt/equity
   - If question asks for "equity value" → report step 9 value directly, do NOT report firm value or debt value
   - If question asks for "debt value" → report step 10 value directly, do NOT report face value or per-firm amounts
   - Your final numerical answer MUST exactly match the value calculated in the relevant step
12. **Final answer verification:** Re-read the question to confirm your answer matches what was asked (firm value vs. equity value vs. debt value) and that you reported the calculated value from the correct step
13. Verify you haven't used the same state for both firms unless the firms are identical OR the question specifies identical states

**Example (sanitized):**
> **Scenario A (Different Firms):** Firm X and Firm Y merge. Firm X: Sunny=$800k, Rainy=$300k, debt=$400k. Firm Y: Hot=$700k, Cold=$250k, debt=$350k. States are independent.
> **Question A:** "What is the combined company value in Sunny-Cold?"
> **Correct approach:** Firms are different (different state-value mappings). Combined firm value = Firm X in Sunny + Firm Y in Cold = $800k + $250k = $1,050k. Answer = $1,050k
> 
> **Scenario B (Identical Firms):** Two identical ice cream companies merge. Each company: Hot=$600k, Warm=$450k, Cold=$200k, debt=$300k. States are independent.
> **Question B1:** "What is the combined company value in Warm-Warm?"
> **Wrong approach:** Misreading the data table and thinking one company has Warm=$450k while the other has Warm=$230k, giving $680k
> **Correct approach:** 
> - Firms are identical (same state-value mappings for both)
> - Data reading verification: The table shows ONE set of values that applies to EACH firm
> - In Warm-Warm, BOTH firms experience the Warm state
> - Firm 1 value in Warm = $450k (from the single value table)
> - Firm 2 value in Warm = $450k (same value from the same table, because firms are identical)
> - Combined firm value = $450k + $450k = $900k
> - Question asks for "combined company value" → Answer = $900k
> 
> **Question B2:** "What is the equity value in Hot-Cold?"
> **Correct approach:** 
> - Firm 1 value in Hot = $600k
> - Firm 2 value in Cold = $200k
> - Combined firm value = $600k + $200k = $800k
> - Total debt = $300k + $300k = $600k
> - Equity = max(0, $800k - $600k) = $200k
> - Question asks for "equity value" → Answer = $200k

**Common Mistakes to Avoid:**
- Misinterpreting a single state-value table as showing different values for each company when firms are actually identical
- For identical firms, failing to recognize that both firms have the same value in any given state
- Reading different rows of a value table as different firms' values when the table applies to each identical firm individually
- Calculating combined firm value correctly but then reporting equity or debt value when question asks for "combined company value"
- Calculating combined firm value correctly but failing to subtract debt when question asks for equity value
- Calculating debt value correctly but then reporting face value or per-firm amounts instead
- Reporting per-company values instead of total combined values in merger contexts
- Confusing "combined company value" (total assets) with "equity value" (assets minus debt)
- Using different state values for identical firms in the same state

---
## Pattern: Firm Value vs. Asset Value with Debt

**Description:** A firm's total value equals the market value of its debt plus the market value of its equity. When debt is risky, debt and equity must be valued separately as contingent claims in each state, then aggregated. However, when the question asks for simple "firm value" or "company value" (not decomposing into debt vs equity components), the firm value equals the expected value of its assets. The complex debt/equity decomposition method is only necessary when distinguishing between components or when explicitly asked to calculate firm value through its financing structure. When calculating expected equity value, the final answer is equity value, NOT firm value.

**When to Use:** Questions asking for "firm value" or "company value" when debt is present AND the question requires decomposing value into debt and equity components; questions asking for "expected equity value"; keywords: "value of company," "firm value," "bond outstanding," "debt," "calculate firm value from debt and equity," "expected value of equity"

**Procedure:**
1. **Determine if decomposition is needed:** If question asks only for "firm value" or "company value" without requiring debt/equity breakdown, calculate expected asset value: Σ(Probability × Asset Value in each state) and stop
2. **If decomposition is required OR if question asks for expected equity value:** For each possible state, determine the firm's asset value in that state
3. In each state, calculate debt value: min(Debt Face Value, Asset Value)
4. In each state, calculate equity value: max(0, Asset Value - Debt Face Value)
5. Calculate expected debt value: Σ(Probability × Debt Value in each state)
6. Calculate expected equity value: Σ(Probability × Equity Value in each state)
7. **Determine what the question asks for:**
   - If "firm value" (and decomposition was required) → Firm value = Expected Debt Value + Expected Equity Value
   - If "expected equity value" or "expected value of equity" → Report the value from step 6 as your final answer (do NOT report firm value)
8. **CRITICAL - Final answer checkpoint:**
   - If question asks for "expected equity value" → your answer is the value from step 6, NOT the firm value
   - Do NOT confuse expected firm value (assets) with expected equity value (assets minus debt claims)
   - Your final numerical answer must match what the question specifically asks for
9. Verify this differs from simply taking the expected value of assets when debt is risky

**Example (sanitized):**
> **Scenario:** Firm has debt face value $100k. State 1 (prob 0.6): assets=$150k. State 2 (prob 0.4): assets=$80k.
> **Question Type A:** "What is the firm value?" 
> **Correct approach for Type A:** Firm value = 0.6×$150k + 0.4×$80k = $122k (expected asset value)
> **Question Type B:** "Calculate the firm value by determining the value of debt and equity separately."
> **Correct approach for Type B:** State 1: Debt=$100k, Equity=$50k. State 2: Debt=$80k, Equity=$0. Expected debt = 0.6×$100k + 0.4×$80k = $92k. Expected equity = 0.6×$50k + 0.4×$0 = $30k. Firm value = $92k + $30k = $122k.
> **Question Type C:** "What is the expected value of the company's equity?"
> **Wrong approach for Type C:** Calculating expected equity correctly as $30k but then reporting firm value $122k
> **Correct approach for Type C:** State 1: Equity=$50k. State 2: Equity=$0. Expected equity = 0.6×$50k + 0.4×$0 = $30k. Question asks for "expected equity value" → Answer = $30k (do NOT report firm value)

**Common Mistakes to Avoid:**
- Using complex debt/equity decomposition when the question simply asks for total firm value (use expected asset value instead)
- Confusing "firm value before merger" with "equity value" or "value to shareholders"
- Calculating expected equity value correctly but reporting expected firm value instead when question asks for equity
- Reporting intermediate calculations (like expected firm value) when the question asks for a specific component (equity value)
## Pattern: Wealth Transfer Requires Risky Debt

**Description:** Wealth transfer between bondholders and shareholders in a merger occurs only when debt is risky (i.e., there exists at least one state where firm value is less than debt face value). Risk-free debt (firm value exceeds face value in all states) creates no transfer opportunity regardless of merger structure. When evaluating whether a change in debt level affects wealth transfer, both the original and new debt levels must be evaluated in the SAME context (pre-merger or post-merger) to determine if the change affects transfer possibility.

**When to Use:** Questions about wealth transfer effects or whether debt level changes affect transfers; keywords: "wealth transfer," "affect transfer," "bondholders," "shareholders," "would this affect"

**Procedure:**
1. **Identify the context:** Determine whether the question asks about wealth transfer in a single-firm context or a merged-firm context
2. Identify all possible states and firm values in each state (for the relevant context: single firm or merged firm)
3. **For the original debt level:**
   - Compare firm value to original debt face value in every state
   - If firm value ≥ debt face value in ALL states → debt is risk-free → no wealth transfer possible
   - If firm value < debt face value in ANY state → debt is risky → wealth transfer may occur
4. **When evaluating a change in debt level:**
   - Compare firm value to NEW debt face value in every state (using the SAME context as step 2)
   - If firm value ≥ new debt face value in ALL states → debt is risk-free → no wealth transfer possible
   - If firm value < new debt face value in ANY state → debt is risky → wealth transfer may occur
5. **Determine if the change affects wealth transfer:**
   - If BOTH debt levels are risk-free (in the relevant context) → NO wealth transfer with either level → change does NOT affect transfer
   - If BOTH debt levels are risky (in the relevant context) → wealth transfer possible with both levels → change does NOT affect transfer possibility (though it may affect transfer magnitude)
   - If one debt level is risky and the other is risk-free → change DOES affect transfer (enables or eliminates it)
6. **Critical distinction for merger questions:** If the question involves a merger, evaluate debt risk in the POST-MERGER context (using combined firm values), not the pre-merger single-firm context
7. Verify: only the transition from risky to risk-free (or vice versa) in the relevant context changes whether transfer is possible

**Example (sanitized):**
> **Scenario:** Two firms merge. Firm A has value $150k (boom) or $80k (recession). Firm B has value $200k (boom) or $110k (recession). Combined firm values: $350k (boom) or $190k (recession). Original combined debt: $125k. Proposed combined debt: $90k.
> **Question:** "Would changing debt from $125k to $90k affect wealth transfer?"
> **Wrong approach:** Original debt $125k is risky for Firm A alone ($80k < $125k in recession), so there's wealth transfer. New debt $90k is also risky for Firm A alone ($80k < $90k), so there's still wealth transfer. The change doesn't affect transfer.
> **Correct approach:** 
> - Context: Post-merger (combined firm)
> - Combined firm values: $350k (boom), $190k (recession)
> - Original debt $125k: Compare to combined values. $190k > $125k in both states → risk-free post-merger
> - New debt $90k: Compare to combined values. $190k > $90k in both states → risk-free post-merger
> - Both debt levels are risk-free in the post-merger context
> - Answer: NO, the change does NOT affect wealth transfer (neither level enables transfer in the merged firm)

**Common Mistakes to Avoid:**
- Evaluating debt risk in the wrong context (single-firm values when question asks about post-merger transfer)
- Concluding that any change in debt level affects transfer without checking if both levels have the same risk status
- Failing to recognize that both debt levels being risk-free (or both risky) means the change doesn't affect transfer possibility

---
## Pattern: Cash Flow to Stockholders Formula

**Description:** Cash flow to stockholders represents all net cash flows between the firm and equity holders, calculated as Dividends Paid minus Net New Equity Raised (or plus Net Equity Repurchased). Net new equity equals the change in owners' equity minus additions to retained earnings. Careful attention to signs is critical: negative net new equity (equity repurchase) increases cash flow to stockholders. The calculated value IS the final answer—report it directly without rounding or adjustment.

**When to Use:** Questions asking for "cash flow to stockholders" or "cash flow to equity holders"; keywords: "cash flow to stockholders," "stockholder cash flow"

**Procedure:**
1. Identify dividends paid during the period from the income statement or cash flow data
2. Find beginning and ending owners' equity from balance sheets
3. Find additions to retained earnings from the income statement (or calculate as: Net Income - Dividends)
4. Calculate net new equity raised: (Ending Owners' Equity - Beginning Owners' Equity) - Additions to Retained Earnings
5. **Calculate cash flow to stockholders: Dividends Paid - Net New Equity Raised**
6. **Handle negative net new equity carefully:** If net new equity is negative (equity repurchase), subtracting a negative value means adding: Dividends - (negative value) = Dividends + positive value, which increases cash flow
7. **Arithmetic verification:** 
   - Write out the final calculation explicitly: Dividends - (Net New Equity value with sign)
   - If Net New Equity is negative, verify: Dividends - (-X) = Dividends + X
   - Double-check the arithmetic of the final sum
8. **Reasonableness checks:**
   - If net new equity is negative (equity repurchase), cash flow to stockholders should be greater than dividends alone
   - If net new equity is positive (equity issuance), cash flow to stockholders should be less than dividends alone
   - The final answer should be reasonable relative to the dividend amount
9. **CRITICAL - Final answer:** The value calculated in step 7 IS your final answer. Report this value directly without further rounding, adjustment, or substitution. Do NOT report only the dividend amount or any intermediate calculation.

**Example (sanitized):**
> **Scenario:** Dividends = $800. Beginning equity = $15,000. Ending equity = $15,600. Retained earnings increased by $900.
> **Wrong approach #1:** Cash flow to stockholders = $800 (dividends only, ignoring equity transactions)
> **Wrong approach #2:** Net new equity = ($15,600 - $15,000) - $900 = -$300. Cash flow = $800 - (-$300) = $500 (arithmetic error in final step)
> **Wrong approach #3:** Calculating correctly as $1,100 but then reporting $800 with false rounding justification
> **Correct approach:** 
> - Net new equity = ($15,600 - $15,000) - $900 = $600 - $900 = -$300 (negative means equity was repurchased)
> - Cash flow to stockholders = $800 - (-$300)
> - Arithmetic verification: $800 - (-$300) = $800 + $300 = $1,100 ✓
> - Reasonableness check: Net new equity is negative (repurchase), so cash flow ($1,100) > dividends ($800) ✓
> - The firm paid $800 in dividends AND returned $300 through equity repurchase, totaling $1,100 to stockholders
> - Final answer: $1,100 (report this value directly)

**Common Mistakes to Avoid:**
- Using only dividends and ignoring equity financing transactions
- Making arithmetic errors when subtracting negative net new equity values (forgetting that subtracting a negative equals adding)
- Failing to verify that the sign of net new equity makes sense (negative = repurchase increases cash flow, positive = issuance decreases cash flow)
- Not double-checking the final arithmetic calculation
- Reporting only the dividend amount or applying false rounding after calculating the correct value

---
## Pattern: Expected Firm Value with Identical Expected Assets

**Description:** When comparing projects or strategies with identical expected asset values, they produce identical expected firm values, regardless of volatility differences. Expected firm value equals expected asset value because firm value = debt value + equity value, and these components always sum to total assets. Volatility affects the distribution of value between debt and equity holders, but not the total expected firm value.

**When to Use:** Questions comparing projects/strategies and asking which "maximizes firm value" or "maximizes expected value of the firm"; keywords: "which project," "which strategy," "maximizes firm value," "expected value of the firm"

**Procedure:**
1. Calculate expected asset value for each project/strategy: Σ(Probability × Asset Value in each state)
2. Compare expected asset values across all options
3. **If expected asset values are equal, expected firm values are equal** — the answer is that both strategies produce the same firm value (answer: "Same," "Equal," "Both," or "Neither")
4. If expected asset values differ, the project with higher expected asset value maximizes firm value
5. Note: volatility differences affect risk distribution between debt and equity holders but do not change total expected firm value when expected assets are equal
6. **Do NOT select based on:** "consistency," "downside risk," "meeting debt obligations," "lower volatility," or "higher volatility" when the question asks specifically about firm value maximization and expected asset values are equal

**Example (sanitized):**
> **Scenario:** Firm has $5,000 debt. Project Alpha: 50% chance of $6,000, 50% chance of $4,000. Project Beta: 50% chance of $7,000, 50% chance of $3,000.
> **Wrong approach:** Project Alpha is better because it has less volatility and meets debt obligations in both states
> **Another wrong approach:** Project Beta is better because it has higher upside potential
> **Correct approach:** 
> - Project Alpha expected assets = 0.5×$6,000 + 0.5×$4,000 = $5,000
> - Project Beta expected assets = 0.5×$7,000 + 0.5×$3,000 = $5,000
> - Expected asset values are identical, therefore expected firm values are identical
> - Answer: "Same" or "Both projects maximize firm value equally"
> - Note: Alpha has lower volatility (better for debtholders), Beta has higher volatility (better for equity holders in expectation), but total firm value is the same

**Common Mistakes to Avoid:**
- Selecting based on risk characteristics (volatility, downside protection) when the question asks only about firm value maximization
- Confusing "firm value" with "equity value" or "bondholder value"
- Failing to recognize that expected firm value = expected asset value when comparing projects
- Choosing one project over another when expected asset values are equal

---

## Pattern: Incremental IRR Direction for Mutually Exclusive Projects

**Description:** When using incremental IRR to choose between mutually exclusive projects, the direction of subtraction matters critically. The incremental cash flows should be calculated as (Larger Initial Investment Project - Smaller Initial Investment Project) to evaluate whether the additional investment is justified. If the incremental IRR exceeds the required return, choose the larger investment project; otherwise, choose the smaller investment project.

**When to Use:** Questions about incremental IRR for mutually exclusive projects; keywords: "incremental IRR," "mutually exclusive," "which project should you choose," "scale problem"

**When NOT to Use:** When the question asks about arbitrage strategies or M&M propositions (use arbitrage pattern instead); when projects are not mutually exclusive

**Procedure:**
1. Identify the two mutually exclusive projects and their cash flows
2. Determine which project requires the larger initial investment (more negative Year 0 cash flow)
3. Calculate incremental cash flows: (Larger Investment Project) - (Smaller Investment Project) for each year
4. Verify that Year 0 incremental cash flow is negative (representing the additional investment)
5. Calculate the IRR of the incremental cash flows using the IRR formula or financial calculator
6. **Arithmetic verification:** Double-check your incremental IRR calculation by:
   - Verifying the NPV of incremental cash flows at your calculated IRR equals zero (or very close to zero)
   - Checking that the calculation is reasonable given the cash flow magnitudes
   - If using approximation methods, verify the result makes sense
7. Compare incremental IRR to the required return:
   - If Incremental IRR > Required Return → Choose the larger investment project (the additional investment is worthwhile)
   - If Incremental IRR < Required Return → Choose the smaller investment project (the additional investment is not worthwhile)
8. **Direction verification:** Confirm that your subtraction order produces a negative Year 0 incremental cash flow; if positive, you've subtracted in the wrong direction

**Example (sanitized):**
> **Scenario:** Required return = 10%. Project A: Year 0 = -$100k, Year 1 = $50k, Year 2 = $70k. Project B: Year 0 = -$200k, Year 1 = $110k, Year 2 = $130k.
> **Wrong approach:** Calculating incremental IRR as 25% without verification, when correct value is ~15%
> **Correct approach:** 
> - Larger investment = Project B (Year 0 = -$200k)
> - Incremental = B - A
> - Year 0: -$200k - (-$100k) = -$100k ✓
> - Year 1: $110k - $50k = $60k
> - Year 2: $130k - $70k = $60k
> - Calculate incremental IRR ≈ 13.1%
> - Verification: NPV at 13.1% = -$100k + $60k/1.131 + $60k/1.131² ≈ $0 ✓
> - Since 13.1% > 10%, choose Project B

**Common Mistakes to Avoid:**
- Subtracting in the wrong direction (Smaller - Larger instead of Larger - Smaller)
- Failing to verify that Year 0 incremental cash flow is negative
- Making computational errors in IRR calculation without verification
- Inverting the decision rule after calculating incremental IRR correctly

---

## Pattern: Arbitrage Strategy Selection Under M&M Propositions

**Description:** When comparing investment strategies involving levered and unlevered firms with identical operations (M&M context), investors can create arbitrage opportunities by replicating one firm's payoff structure at lower cost. If two firms have identical operating income but different total firm values, the overvalued firm creates an arbitrage opportunity. Investors will choose the strategy that allows them to achieve the same payoff at lower cost, typically by borrowing personally (homemade leverage) to invest in the undervalued unlevered firm rather than buying the overvalued levered firm.

**When to Use:** Questions asking "which strategy will investors choose" or "which investment will investors prefer" in contexts with levered and unlevered firms with identical operations; keywords: "identical in every respect except," "levered," "unlevered," "investors choose," "investment strategy," "M&M," "Modigliani-Miller"

**When NOT to Use:** When the question asks about firm value maximization (use Expected Firm Value pattern); when firms have different operating characteristics; when the question asks about capital structure decisions from the firm's perspective

**Procedure:**
1. Identify the levered and unlevered firms and their characteristics:
   - Operating income (should be identical)
   - Market value of equity
   - Market value of debt (if any)
   - Interest payments (if any)
2. Calculate total firm value for each:
   - Unlevered firm value = Market value of equity
   - Levered firm value = Market value of equity + Market value of debt
3. **Compare total firm values:**
   - If values are equal → M&M Proposition I holds, investors are indifferent
   - If values differ → arbitrage opportunity exists
4. **Identify the arbitrage opportunity:**
   - If Levered Firm Value > Unlevered Firm Value → Levered firm is overvalued
   - Investors can replicate levered firm returns by borrowing personally and investing in unlevered firm at lower total cost
   - Strategy: Choose unlevered firm with homemade leverage
5. **Verify the arbitrage logic:**
   - Can investors achieve the same payoff structure at lower cost?
   - Does the strategy exploit the price difference between the two firms?
6. **Determine the answer:**
   - If arbitrage exists favoring unlevered firm → Investors choose unlevered firm strategy
   - If arbitrage exists favoring levered firm → Investors choose levered firm strategy
   - If no arbitrage exists → Investors are indifferent

**Example (sanitized):**
> **Scenario:** Company A (unlevered): Operating income = $500k, Stock value = $4M, No debt. Company B (levered): Operating income = $500k, Stock value = $3M, Debt value = $1.2M (6% interest = $72k). No taxes.
> **Question:** "Which investment strategy will investors choose?"
> **Wrong approach:** "Investors are indifferent because M&M Proposition I says firm value is independent of capital structure"
> **Correct approach:**
> - Total firm values: A = $4M, B = $3M + $1.2M = $4.2M
> - Company B is overvalued by $200k
> - Arbitrage opportunity: Investors can borrow $1.2M at 6% ($72k interest) and invest $4M total in Company A
> - This replicates Company B's equity payoff ($500k - $72k = $428k) but costs only $2.8M in personal equity vs $3M for Company B stock
> - Investors save $200k by choosing the unlevered firm strategy with homemade leverage
> - Answer: Investors will choose Company A (unlevered firm strategy)

**Common Mistakes to Avoid:**
- Concluding investors are indifferent when total firm values differ (missing the arbitrage opportunity)
- Applying M&M Proposition I mechanically without checking if market values actually satisfy the proposition
- Focusing on risk differences rather than arbitrage opportunities when the question asks which strategy investors will choose
- Ignoring that investors can create homemade leverage to replicate levered firm payoffs at lower cost