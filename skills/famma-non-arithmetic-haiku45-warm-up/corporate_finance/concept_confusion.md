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