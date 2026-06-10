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

**Description:** Debt value in any state equals min(Face Value of All Debt, Total Firm Value in that State). When firm value is insufficient to cover all debt, debtholders receive the entire firm value (absolute priority), leaving equity holders with zero due to limited liability.

**When to Use:** Questions asking for debt value or equity value in specific states; keywords: "value of debt," "value of stock," "end-of-period," "state," "scenario"

**Procedure:**
1. Identify total face value of all debt claims
2. Calculate total firm value in the specific state being analyzed
3. Apply the debt valuation rule: Debt Value = min(Total Face Value, Firm Value in State)
4. Calculate equity value as the residual: Equity Value = max(0, Firm Value - Total Debt Face Value)
5. Verify: if Firm Value < Total Debt Face Value, then Debt gets entire Firm Value and Equity = $0
6. Verify: if Firm Value ≥ Total Debt Face Value, then Debt gets Face Value and Equity gets the remainder

**Example (sanitized):**
> **Scenario:** Combined firm has $800k total debt. In State X, firm value = $600k. In State Y, firm value = $1,000k.
> **Wrong approach:** Debt always equals $800k regardless of firm value.
> **Correct approach:** State X: Debt = min($800k, $600k) = $600k, Equity = $0. State Y: Debt = min($800k, $1,000k) = $800k, Equity = $200k.

---

## Pattern: Independent State Variables in Mergers

**Description:** When merging firms face independent state variables (e.g., weather in different locations), each joint state combines one outcome from each firm. The combined firm value in a joint state equals the sum of individual firm values in their respective individual states.

**When to Use:** Merger problems with independent uncertainty; keywords: "independent," "different towns/locations," "State A-State B" notation (e.g., "Rain-Warm")

**Procedure:**
1. Recognize that "State A-State B" means Firm 1 experiences State A while Firm 2 experiences State B
2. Look up Firm 1's value in State A from the given data
3. Look up Firm 2's value in State B from the given data
4. Calculate combined firm value: Firm 1 Value (State A) + Firm 2 Value (State B)
5. Apply debt/equity valuation rules to this combined value
6. Verify you haven't used the same state for both firms unless the question specifies identical states

**Example (sanitized):**
> **Scenario:** Firm 1 and Firm 2 merge. Firm 1: Good=$500k, Bad=$200k. Firm 2: Good=$600k, Bad=$300k. States are independent.
> **Wrong approach:** Good-Bad state = $200k + $300k = $500k (using Bad for both)
> **Correct approach:** Good-Bad means Firm 1 in Good ($500k) and Firm 2 in Bad ($300k), so combined value = $500k + $300k = $800k

---

## Pattern: Firm Value vs. Asset Value with Debt

**Description:** A firm's total value equals the market value of its debt plus the market value of its equity, not simply the expected value of its assets. When debt is risky, debt and equity must be valued separately as contingent claims in each state, then aggregated.

**When to Use:** Questions asking for "firm value" or "company value" when debt is present; keywords: "value of company," "firm value," "bond outstanding," "debt"

**Procedure:**
1. For each possible state, determine the firm's asset value in that state
2. In each state, calculate debt value: min(Debt Face Value, Asset Value)
3. In each state, calculate equity value: max(0, Asset Value - Debt Face Value)
4. Calculate expected debt value: Σ(Probability × Debt Value in each state)
5. Calculate expected equity value: Σ(Probability × Equity Value in each state)
6. Firm value = Expected Debt Value + Expected Equity Value
7. Verify this differs from simply taking the expected value of assets when debt is risky

**Example (sanitized):**
> **Scenario:** Firm has debt face value $100k. State 1 (prob 0.6): assets=$150k. State 2 (prob 0.4): assets=$80k.
> **Wrong approach:** Firm value = 0.6×$150k + 0.4×$80k = $122k
> **Correct approach:** State 1: Debt=$100k, Equity=$50k. State 2: Debt=$80k, Equity=$0. Expected debt = 0.6×$100k + 0.4×$80k = $92k. Expected equity = 0.6×$50k + 0.4×$0 = $30k. Firm value = $92k + $30k = $122k. (Note: in this case they match, but the method differs and matters when calculating components separately)

---

## Pattern: Wealth Transfer Requires Risky Debt

**Description:** Wealth transfer between bondholders and shareholders in a merger occurs only when debt is risky (i.e., there exists at least one state where firm value is less than debt face value). Risk-free debt (firm value exceeds face value in all states) creates no transfer opportunity regardless of merger structure.

**When to Use:** Questions about wealth transfer effects or whether debt level changes affect transfers; keywords: "wealth transfer," "affect transfer," "bondholders," "shareholders"

**Procedure:**
1. Identify all possible states and firm values in each state
2. Compare firm value to debt face value in every state
3. If firm value ≥ debt face value in ALL states, debt is risk-free → no wealth transfer possible
4. If firm value < debt face value in ANY state, debt is risky → wealth transfer may occur through merger
5. When evaluating a change in debt level, repeat steps 2-4 with the new debt level
6. Verify: only the transition from risky to risk-free (or vice versa) changes whether transfer is possible

**Example (sanitized):**
> **Scenario:** Firm has values $150k (boom) and $120k (recession). Original debt: $130k. Proposed debt: $100k.
> **Wrong approach:** Lowering debt from $130k to $100k affects wealth transfer because debt level changed.
> **Correct approach:** Original debt $130k: recession value $120k < $130k → risky debt. New debt $100k: both states exceed $100k → risk-free debt. Only the original debt level allows wealth transfer; the new level does not. The change matters because it shifts from risky to risk-free.

---

## Pattern: Cash Flow to Stockholders Formula

**Description:** Cash flow to stockholders represents all net cash flows between the firm and equity holders, calculated as Dividends Paid minus Net New Equity Raised (or plus Net Equity Repurchased). Net new equity equals the change in owners' equity minus additions to retained earnings.

**When to Use:** Questions asking for "cash flow to stockholders" or "cash flow to equity holders"; keywords: "cash flow to stockholders," "stockholder cash flow"

**Procedure:**
1. Identify dividends paid during the period from the income statement or cash flow data
2. Find beginning and ending owners' equity from balance sheets
3. Find additions to retained earnings from the income statement
4. Calculate net new equity raised: (Ending Owners' Equity - Beginning Owners' Equity) - Additions to Retained Earnings
5. Calculate cash flow to stockholders: Dividends Paid - Net New Equity Raised
6. Verify: if net new equity is negative (equity repurchase), cash flow to stockholders increases; if positive (equity issuance), it decreases
7. Common trap: dividends alone are insufficient; equity financing transactions must be included

**Example (sanitized):**
> **Scenario:** Dividends = $500. Beginning equity = $10,000. Ending equity = $10,800. Retained earnings increased by $600.
> **Wrong approach:** Cash flow to stockholders = $500 (dividends only)
> **Correct approach:** Net new equity = ($10,800 - $10,000) - $600 = $200. Cash flow to stockholders = $500 - $200 = $300. The firm raised $200 in new equity, reducing net cash to stockholders.