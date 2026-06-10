# SKILL PATTERNS FOR CORPORATE FINANCE CONCEPT CONFUSION (PoT)

## Pattern: Sign Convention in NPV and Cash Flow Calculations

**Description:** NPV and cash flow metrics are signed values that convey economic meaning (positive = value creation, negative = value destruction). Failing to preserve signs or incorrectly treating inflows/outflows leads to economically meaningless results. CRITICAL: When questions describe cash flows as "payments", "costs", or "must make", ALL such flows are outflows (negative) regardless of OCR formatting or absence of explicit negative signs in the data.

**When to Use:** NPV calculations, cash flow to creditors/stockholders, any metric where direction of cash flow matters (keywords: "NPV", "cash flow to", "net present value", "should accept/reject", "payments", "must make", "costs")

**Procedure:**
1. Formula: NPV = Σ[CFt / (1+r)^t] where CF signs matter: inflows are positive, outflows are negative
2. CHECK: Identify cash flow direction from QUESTION CONTEXT, not just data formatting:
   - Keywords "payments", "must make", "costs", "expenses" → negative (outflows)
   - Keywords "receives", "generates", "revenue", "inflows" → positive (inflows)
   - Initial investment/purchase → negative (outflow)
3. VALIDATE: Ensure ALL cash flows identified as payments/costs have negative signs, even if OCR data lacks explicit negatives
4. For cash flow to creditors: Interest Paid - Net New Borrowing (where borrowing = ending debt - beginning debt)
5. Preserve signs through all calculations; never take absolute value
6. Return the signed result as-is (negative NPV means reject project)

**Example (sanitized):**
> **Scenario:** A company receives $8,000 today but must make the following payments: Year 1: $2,500, Year 2: $3,200, Year 3: $2,800. Discount rate is 9%. What is the NPV?
>
> **Wrong approach:** Treating some payments as positive because data lacks explicit negative signs.
> ```python
> # WRONG: Not applying negative signs to all payments
> cf_0 = 8000  # Initial receipt (positive)
> cf_1 = -2500  # Payment (negative)
> cf_2 = 3200  # WRONG: Should be negative (payment)
> cf_3 = 2800  # WRONG: Should be negative (payment)
> npv = cf_0 + cf_1/1.09 + cf_2/1.09**2 + cf_3/1.09**3
> # Results in positive NPV when it should be negative
> ```
>
> **Correct approach:**
> 1. Identify from context: "receives" = positive inflow, "must make payments" = negative outflows
> 2. Apply negative signs to ALL payments regardless of data formatting
> 3. CF₀ = +$8,000 (receipt), CF₁ = -$2,500, CF₂ = -$3,200, CF₃ = -$2,800
> 4. NPV = 8,000 - 2,500/1.09 - 3,200/1.09² - 2,800/1.09³
>
> ```python
> # Given data
> initial_receipt = 8000  # Positive (receives)
> payment_1 = 2500  # From data
> payment_2 = 3200  # From data
> payment_3 = 2800  # From data
> r = 0.09
> 
> # CRITICAL: Apply negative signs based on question context ("must make payments")
> cf_0 = initial_receipt  # Positive inflow
> cf_1 = -payment_1  # Negative outflow (payment)
> cf_2 = -payment_2  # Negative outflow (payment)
> cf_3 = -payment_3  # Negative outflow (payment)
> 
> # NPV calculation preserving signs
> npv = cf_0 + cf_1/(1+r)**1 + cf_2/(1+r)**2 + cf_3/(1+r)**3
> 
> npv  # Negative value indicates net cost
> ```

**Common Bugs to Avoid:**
- Taking `abs()` of final NPV, destroying economic meaning
- Treating initial investment as positive instead of negative outflow
- **CRITICAL: Inconsistent sign application where some payments are negative and others positive due to OCR formatting**
- **Not validating that ALL cash flows described as "payments" or "costs" are negative**
- Using `print(npv)` instead of expression `npv` on last line
- Reversing sign convention (inflows negative, outflows positive)

---
## Pattern: Cash Flow to Creditors with Net Borrowing

**Description:** Cash flow to creditors represents net cash paid OUT to debt holders, calculated as interest paid MINUS net new borrowing. New borrowing reduces cash flow to creditors because the firm receives cash FROM creditors. Net new borrowing = New debt issued - Debt repaid = Ending debt - Beginning debt (from balance sheet). STANDARD CONVENTION: Use only long-term debt unless the question explicitly mentions short-term borrowing or notes payable in the context of creditor cash flows.

**When to Use:** Questions asking for "cash flow to creditors" or "cash flow to bondholders" given interest paid and debt changes (keywords: "cash flow to creditors", "raised in new long-term debt", "interest paid", "long-term debt" balance sheet changes)

**Procedure:**
1. Formula: Cash_Flow_to_Creditors = Interest_Paid - Net_New_Borrowing
2. Identify which debt to include: STANDARD = long-term debt only
3. Calculate net new borrowing from balance sheet: Ending_LT_Debt - Beginning_LT_Debt
4. Or use given information: New_Debt_Issued - Debt_Repaid
5. Subtract net new borrowing from interest paid (borrowing is cash FROM creditors, reducing net payment TO them)
6. Return the result (can be negative if firm borrowed more than it paid in interest)

**Example (sanitized):**
> **Scenario:** A firm paid $35,000 in interest during the year. Long-term debt was $500,000 at the beginning and $620,000 at the end. Short-term notes payable increased from $80,000 to $95,000. What is the cash flow to creditors?
>
> **Wrong approach:** Including short-term notes payable without explicit guidance in the question.
> ```python
> # WRONG: Including short-term debt without justification
> net_new_borrowing = (620000 - 500000) + (95000 - 80000)  # 135,000
> cash_flow = 35000 - 135000  # -100,000 - Incorrect
> ```
>
> **Correct approach:**
> 1. Standard convention: use long-term debt only (unless question specifies otherwise)
> 2. Net new borrowing = $620,000 - $500,000 = $120,000
> 3. Cash flow to creditors = $35,000 - $120,000 = -$85,000
> 4. Negative means firm received net cash from creditors
>
> ```python
> # Given data
> interest_paid = 35000
> beginning_lt_debt = 500000
> ending_lt_debt = 620000
> # Short-term notes: NOT included unless question specifies
> 
> # Calculate net new borrowing (long-term debt only)
> net_new_borrowing = ending_lt_debt - beginning_lt_debt  # 120000
> 
> # Cash flow to creditors
> cash_flow_to_creditors = interest_paid - net_new_borrowing
> 
> cash_flow_to_creditors  # -85000
> ```

**Common Mistakes to Avoid:**
- Including short-term notes payable when only long-term debt changes should be considered (unless question explicitly includes short-term borrowing)
- Adding net new borrowing instead of subtracting (wrong sign convention)
- Using only interest paid without considering debt changes
- Calculating net new borrowing as beginning minus ending (reversed)
- Treating negative result as an error (negative is valid when firm borrows more than it pays)
- Forgetting that "cash flow TO creditors" means from firm's perspective (outflow)

---
## Pattern: Merger NPV with Acquisition Premium

**Description:** In merger NPV calculations, NPV to the acquirer equals the value created (synergies) minus the premium paid above target's current market value. The cost is only the excess payment over market value, not the total cash paid. Total cost = Premium paid = Cash_Paid - Target_Market_Value. CRITICAL: Ensure all required merger terms (premium, exchange ratio, or cash offer) are explicitly provided before calculation. If premium information is referenced from another question, verify it is available. If required information is missing, the code MUST return an error message and halt calculation.

**When to Use:** Merger/acquisition NPV questions with synergy values and target market prices (keywords: "NPV of merger", "NPV of acquisition", "synergistic benefits", "value of synergies", "acquire for", "bidding firm", "assuming the conditions in question X")

**Procedure:**
1. CHECK: Verify all required information is available:
   - If question references "conditions in question X", check if that information is provided in context
   - If cash offer given, verify amount is specified
   - If premium not explicitly given, verify it can be calculated from available data
2. CRITICAL: If required information missing, code MUST return error and halt:
   ```python
   # MANDATORY validation - code must include this check
   if referenced_info_not_available:
       return "Insufficient information: [specify what's missing, e.g., 'conditions from question 4 not provided']"
   # DO NOT proceed with calculation if this check fails
   # DO NOT make assumptions about exchange ratios, premiums, or other terms
   ```
3. Formula: NPV_to_Acquirer = Synergy_Value - Premium_Paid
4. Calculate target's standalone market value: Target_Shares × Target_Price_per_Share
5. If cash offer given: Premium = Cash_Paid - Target_Market_Value
6. If stock offer given: Cost = Acquirer_Share_Price × Shares_Offered; Premium = Cost - Target_Market_Value
7. VALIDATE: Premium should be non-negative and less than synergy value in typical cases
8. Return NPV (value created minus value transferred to target shareholders)

**Example (sanitized):**
> **Scenario:** Firm A is acquiring Firm B, which has 4,000 shares trading at $25 per share. The synergies from the merger are valued at $15,000. The question states "assuming the conditions in question 3" but question 3's information is NOT provided in the context. What should the code return?
>
> **Wrong approach:** Assuming an exchange ratio or premium without verification.
> ```python
> # WRONG: Making unjustified assumptions
> target_market_value = 4000 * 25  # 100,000
> # Assumes 1:1 exchange or some arbitrary premium
> cost = 4000 * 50  # WRONG: Arbitrary assumption
> npv = 15000 - (cost - target_market_value)  # Incorrect
> ```
>
> **Correct approach:**
> 1. Check if "conditions in question 3" are available in context
> 2. Information NOT found in provided context
> 3. Return error message immediately, do NOT calculate
>
> ```python
> # Given data
> target_shares = 4000
> target_price_per_share = 25
> synergy_value = 15000
> 
> # CRITICAL: Check if referenced information is available
> # Question references "conditions in question 3"
> question_3_info_available = False  # Determined by checking context
> 
> if not question_3_info_available:
>     result = "Insufficient information: conditions from question 3 not provided"
> else:
>     # Only proceed if all required information is available
>     target_market_value = target_shares * target_price_per_share
>     # Extract premium or cost from question 3 conditions
>     premium_paid = ...  # Would be extracted from referenced question
>     npv_to_acquirer = synergy_value - premium_paid
>     result = npv_to_acquirer
> 
> result
> ```

**Common Bugs to Avoid:**
- Returning synergy value as NPV without subtracting premium (ignoring cost to acquirer)
- Using total cash paid instead of premium over market value
- **CRITICAL: Assuming premium equals target market value when information is missing (creates 100% premium assumption)**
- **CRITICAL: Not validating that referenced information (e.g., "conditions in question 4") is actually available**
- **Making arbitrary assumptions about exchange ratios or terms when information is missing**
- Forgetting that target shareholders capture part of synergy value through premium
- Not recognizing that NPV can be negative if premium exceeds synergies
- Confusing total value created (synergies) with value captured by acquirer (NPV)
## Pattern: Stock-for-Stock Merger Post-Merger Share Price

**Description:** In stock mergers with no synergies, post-merger share price equals combined market value divided by total shares outstanding after merger. Must account for dilution from new shares issued. CRITICAL: Exchange ratio must be explicitly provided in the question - if missing, the code MUST return an error message and halt calculation. DO NOT assume any default exchange ratio (especially not 1:1).

**When to Use:** Merger questions asking for "share price after merger" or "EPS after merger" with stock exchange ratios (keywords: "shares of A for shares of B", "post-merger price", "no synergies", "stock exchange", "EPS", "earnings per share")

**Procedure:**
1. CHECK: Verify exchange ratio is explicitly stated (e.g., "1 share of A for every 4 shares of B")
2. CRITICAL: If exchange ratio missing or not explicitly stated:
   ```python
   # MANDATORY validation - code must include this check
   if exchange_ratio_not_provided:
       return "Insufficient information: exchange ratio not specified"
   # DO NOT proceed with calculation if this check fails
   ```
3. Formula: Post-Merger Price = (Market Value A + Market Value B) / Total Shares After Merger
4. Calculate pre-merger market values: Price × Shares for each firm
5. Calculate new shares issued = Target Shares / Exchange Ratio
6. Total shares after = Acquirer Shares + New Shares Issued
7. For share price: Post-merger price = Combined Market Value / Total Shares After
8. For EPS: Post-merger EPS = Combined Earnings / Total Shares After

**Example (sanitized):**
> **Scenario:** Firm A has 2,000 shares at $40/share, earnings $8,000. Firm B has 600 shares at $20/share, earnings $2,400. Question asks for post-merger EPS but does NOT specify exchange ratio. What should the code return?
>
> **Wrong approach:** Assuming 1:1 exchange ratio without verification.
> ```python
> # WRONG: Proceeding without exchange ratio
> total_shares = 2000 + 600  # Assumes 1:1, not justified
> eps = (8000 + 2400) / 2600  # 4.0 - WRONG
> ```
>
> **Correct approach:**
> 1. Check if exchange ratio is provided in question
> 2. Exchange ratio NOT found in question text
> 3. Return error message immediately, do NOT calculate
>
> ```python
> # Given data
> a_shares = 2000
> a_price = 40
> a_earnings = 8000
> b_shares = 600
> b_price = 20
> b_earnings = 2400
> 
> # CRITICAL: Check for exchange ratio in question
> # This should be implemented as actual validation in code
> exchange_ratio_provided = False  # Determined by parsing question
> 
> if not exchange_ratio_provided:
>     result = "Insufficient information: exchange ratio not specified"
> else:
>     # Only proceed if exchange ratio is available
>     exchange_ratio = ...  # Would be extracted from question
>     new_shares_issued = b_shares / exchange_ratio
>     total_shares_after = a_shares + new_shares_issued
>     combined_earnings = a_earnings + b_earnings
>     post_merger_eps = combined_earnings / total_shares_after
>     result = post_merger_eps
> 
> result
> ```

**Common Mistakes to Avoid:**
- **CRITICAL: Assuming 1:1 exchange ratio when not specified (MUST return error instead)**
- **Not implementing validation check as actual code guard before calculation**
- Not validating that exchange ratio is provided before calculating
- Returning exchange ratio instead of share price/EPS
- Forgetting to add new shares issued to denominator
- Using only acquirer's shares in denominator
- Incorrectly calculating new shares (multiplying instead of dividing by exchange ratio)

---
## Pattern: Credit Policy Change with Receivables Buildup

**Description:** Switching from cash to credit sales creates two effects: (1) one-time upfront cost of receivables buildup (PV of one period's sales under new policy), and (2) perpetual incremental profit stream. NPV = PV(perpetual incremental profits) - Initial receivables investment. CRITICAL: The initial receivables must be discounted back one period because it represents cash tied up for one period. The receivables buildup equals the FULL SALES VALUE (price × quantity) for one period under the new policy, not just the cost component.

**When to Use:** Credit policy change questions with cash vs. credit terms, unit sales changes, and required returns (keywords: "change in credit policy", "net one month", "receivables buildup", "switch to credit")

**Procedure:**
1. Formula: NPV = [Incremental Monthly Profit / r] - Initial Receivables Investment
2. Calculate incremental monthly profit = (New Units - Old Units) × (Price - Cost)
3. Calculate initial receivables buildup = (New Units × Price) for one period credit
4. CRITICAL: Discount the receivables by (1+r) because cash is tied up for one period: PV_Receivables = Receivables / (1 + r)
5. Calculate PV of perpetuity = Incremental Profit / r (where r is per-period rate)
6. NPV = PV of perpetuity - PV of initial receivables (discounted)

**Example (sanitized):**
> **Scenario:** Current: 800 units/month cash sales at $60, cost $35. New: 900 units/month, net one month terms. Required return 1.2% per month.
>
> **Wrong approach:** Using cost instead of price for receivables, or not discounting.
> ```python
> # WRONG: Using cost instead of full sales value
> initial_receivables = 900 * 35  # Should use price (60), not cost (35)
> npv = (100 * 25 / 0.012) - 31500  # Incorrect receivables value
> ```
>
> **Correct approach:**
> 1. Incremental profit: (900 - 800) × ($60 - $35) = 100 × $25 = $2,500/month
> 2. PV of perpetual profits: $2,500 / 0.012 = $208,333.33
> 3. Initial receivables (one month of new sales at PRICE): 900 × $60 = $54,000
> 4. DISCOUNT receivables: $54,000 / 1.012 = $53,359.68 (PV of cash tied up)
> 5. NPV: $208,333.33 - $53,359.68 = $154,973.65
>
> ```python
> # Current and new policy data
> price = 60
> cost = 35
> current_units = 800
> new_units = 900
> r_monthly = 0.012
> 
> # Incremental monthly profit (perpetual)
> incremental_units = new_units - current_units
> incremental_profit_monthly = incremental_units * (price - cost)
> 
> # PV of perpetual incremental profits
> pv_perpetuity = incremental_profit_monthly / r_monthly
> 
> # Initial receivables buildup (one month of new sales at PRICE)
> # MUST discount back one period since payment delayed
> initial_receivables = (new_units * price) / (1 + r_monthly)
> 
> # NPV of policy change
> npv_policy = pv_perpetuity - initial_receivables
> 
> npv_policy  # 154,973.65
> ```

**Common Mistakes to Avoid:**
- **Using cost instead of price for receivables buildup (CRITICAL ERROR)** - receivables represent full sales value owed
- NOT discounting initial receivables investment - using face value instead of PV
- Returning only monthly incremental profit, not NPV
- Not recognizing perpetuity structure of ongoing profits
- Forgetting that receivables represent cash tied up for one period, requiring discounting

---
## Pattern: Zero-NPV Acquisition and P/E Ratio Preservation

**Description:** When NPV of acquisition is zero, it means fair value was paid, but the post-merger P/E ratio does NOT simply equal the acquirer's pre-merger P/E. The correct calculation requires accounting for: (1) dilution from new shares issued, (2) combined earnings, and (3) the acquirer's share price remaining constant at fair value. Post-merger P/E = Acquirer_Price / New_EPS, where New_EPS = Combined_Earnings / Total_Shares_After_Merger. CRITICAL: This pattern applies to stock-for-stock mergers where shares are issued. For cash mergers or when no synergies exist, use different valuation approaches.

**When to Use:** Merger questions asking for P/E ratio given NPV=0 condition with stock-for-stock exchanges (keywords: "if NPV is zero", "what P/E ratio", "stock exchange", "shares offered")

**When NOT to Use:** 
- Cash mergers (no share dilution occurs)
- Questions asking for P/E when "no synergies" exist without NPV=0 condition (requires different calculation)
- Questions that don't specify share exchange terms
- Situations where the merger structure is unclear

**Procedure:**
1. VERIFY: Confirm this is a stock-for-stock merger with NPV=0 condition
2. Concept: NPV = 0 means fair value paid, but P/E changes due to share dilution and earnings combination
3. Calculate new shares issued based on exchange terms
4. Calculate total shares after merger = Acquirer Shares + New Shares Issued
5. Calculate combined earnings = Acquirer Earnings + Target Earnings
6. Calculate new EPS = Combined Earnings / Total Shares After Merger
7. Post-merger P/E = Acquirer's Share Price / New EPS (price stays constant at fair value)
8. Return the calculated P/E ratio

**Common Mistakes to Avoid:**
- Returning acquirer's pre-merger P/E without calculation (ignores dilution)
- Using weighted average of P/E ratios (conceptually wrong)
- Using target's P/E ratio
- Not recognizing that share dilution changes EPS even at fair value
- Forgetting that NPV=0 means price stays constant, but P/E changes due to new EPS
- **Applying this pattern to cash mergers where no dilution occurs**
- **Confusing "no synergies" scenarios with "NPV=0" scenarios (they require different approaches)**

**Example (sanitized):**
> **Scenario:** Acquirer has 200,000 shares at $50/share, earnings of $1,200,000 (EPS = $6.00, P/E = 8.33). Target has 80,000 shares, earnings of $400,000. Acquirer offers 30,000 of its shares for all target shares. If NPV = 0, what is post-merger P/E?
>
> **Wrong approach:** Assuming post-merger P/E equals acquirer's pre-merger P/E (8.33) without accounting for dilution.
> ```python
> # WRONG: Simply returning acquirer's P/E
> post_merger_pe = 8.33  # Ignores dilution effect
> ```
>
> **Correct approach:**
> 1. New shares issued: 30,000
> 2. Total shares after: 200,000 + 30,000 = 230,000
> 3. Combined earnings: $1,200,000 + $400,000 = $1,600,000
> 4. New EPS: $1,600,000 / 230,000 = $6.96
> 5. Acquirer's price stays at $50 (fair value)
> 6. Post-merger P/E: $50 / $6.96 = 7.18
>
> ```python
> # Given data
> acquirer_shares = 200000
> acquirer_price = 50
> acquirer_earnings = 1200000
> target_earnings = 400000
> shares_offered = 30000
> 
> # Calculate post-merger metrics
> total_shares_after = acquirer_shares + shares_offered
> combined_earnings = acquirer_earnings + target_earnings
> new_eps = combined_earnings / total_shares_after
> 
> # Post-merger P/E (price constant at fair value)
> post_merger_pe = acquirer_price / new_eps
> 
> post_merger_pe  # 7.18
> ```

---
## Pattern: Gordon Growth Model for Acquisition Valuation

**Description:** Maximum acquisition price per share uses dividend discount model with POST-ACQUISITION growth rate. Value = D1/(r-g) where g is the NEW growth rate acquirer expects to achieve. The required return r must be derived carefully from the target's current market conditions. CRITICAL: When current stock price is not directly given, calculate it as EPS × P/E ratio (NOT Dividend × P/E). When calculating "gain from acquisition", this means value created relative to CURRENT market value, not comparison between alternative growth scenarios.

**When to Use:** Acquisition valuation with dividend growth rates, especially when acquirer expects to change growth rate (keywords: "maximum price", "growth rate will increase to", "willing to pay", "acquisition", "synergies", "cash for each share", "gain from acquisition")

**Procedure:**
1. CHECK: If current stock price not given, calculate from P/E and EPS: Price = EPS × P/E (NOT Dividend × P/E)
2. Calculate current dividend per share: D0 = Total_Dividends / Shares_Outstanding (if needed)
3. Derive target's required return from CURRENT market conditions: r = (D0 × (1 + g_current) / P_current) + g_current
4. This r represents the market's required return and remains constant (it's a function of risk, not growth)
5. Calculate next year's dividend with NEW growth: D1 = D0 × (1 + g_new)
6. Apply Gordon model with new growth: Value_per_share = D1 / (r - g_new)
7. CHECK: Determine what the question asks for:
   - "Maximum price" or "value per share" → return Value_per_share
   - "Gain from acquisition" → return (Value_per_share × Shares) - Current_Market_Value
   - NOT the difference between two growth rate scenarios
8. CHECK UNIT CONSISTENCY:
   - If calculating NPV, ensure both value and cost are in same units (per-share OR total)
   - For per-share NPV: NPV_per_share = Value_per_share - Cash_per_share
   - For total NPV: NPV_total = (Value_per_share × Shares) - (Cash_per_share × Shares)
9. Verify r > g_new for model validity
10. Return the appropriate value (per-share, total, or gain as requested)

**Example (sanitized):**
> **Scenario:** Target Company has 500,000 shares, EPS of $3.00, P/E ratio of 8, pays $1.20 annual dividend per share, with historical 4% growth. Acquirer believes it can achieve 6% growth. Current market value is $12M. What is the acquirer's gain from this acquisition?
>
> **Wrong approach:** Calculating difference between 6% and 4% growth scenarios.
> ```python
> # WRONG: Comparing two growth scenarios
> value_at_6_percent = ...  # $15M
> value_at_4_percent = ...  # $12M
> gain = value_at_6_percent - value_at_4_percent  # $3M - WRONG interpretation
> ```
>
> **Correct approach:**
> 1. Calculate current price: EPS × P/E = $3.00 × 8 = $24.00
> 2. Current market value: 500,000 × $24 = $12M (matches given)
> 3. Derive required return from CURRENT market (4% growth):
>    - D1_current = $1.20 × 1.04 = $1.248
>    - r = ($1.248 / $24.00) + 0.04 = 0.092 (9.2%)
> 4. Value with NEW growth (6%):
>    - D1_new = $1.20 × 1.06 = $1.272
>    - Value_per_share = $1.272 / (0.092 - 0.06) = $39.75
>    - Total value = 500,000 × $39.75 = $19.875M
> 5. Gain from acquisition = New value - Current market value
>    - Gain = $19.875M - $12M = $7.875M
>
> ```python
> # Given data
> shares_outstanding = 500000
> eps = 3.00
> pe_ratio = 8
> current_dividend_per_share = 1.20
> current_growth = 0.04
> new_growth = 0.06
> current_market_value = 12000000  # Given or calculated
> 
> # CRITICAL: Calculate current price from EPS and P/E
> current_price = eps * pe_ratio  # 24.00, NOT dividend * P/E
> 
> # Derive required return from CURRENT market
> d1_current = current_dividend_per_share * (1 + current_growth)
> required_return = (d1_current / current_price) + current_growth
> 
> # Calculate value per share with NEW growth rate
> d1_new = current_dividend_per_share * (1 + new_growth)
> value_per_share_new = d1_new / (required_return - new_growth)
> 
> # Total value with new growth
> total_value_new = value_per_share_new * shares_outstanding
> 
> # CRITICAL: "Gain from acquisition" = New value - Current market value
> gain_from_acquisition = total_value_new - current_market_value
> 
> gain_from_acquisition
> ```

**Common Mistakes to Avoid:**
- **Calculating current price as Dividend × P/E instead of EPS × P/E (CRITICAL ERROR)**
- **Interpreting "gain" as difference between growth scenarios instead of value creation vs current market value**
- Using new growth rate to derive required return (r should come from current market conditions)
- Confusing growth rate changes with discount rate changes (r is constant, based on risk)
- Not recognizing that r represents market's required return for the target's risk level
- Applying old growth rate in final valuation formula
- **CRITICAL: Mixing per-share values with total values in NPV calculation (unit mismatch error)**

---
## Pattern: Investment NPV with Market-to-Book Ratio

**Description:** When a new investment maintains the same P/E and ROE as existing firm, NPV = Investment × (M/B - 1). This reflects that market values each dollar of book equity at M/B ratio, so investing at book creates value of (M/B - 1) per dollar.

**When to Use:** Investment decisions where new project has "same P/E" or "same ROE" as firm, with equity financing (keywords: "same P/E ratio", "same ROE", "new equity issue")

**Procedure:**
1. Formula: NPV = Investment Amount × (Market-to-Book Ratio - 1)
2. Calculate book value of equity = Total Assets - Total Liabilities
3. Calculate market value of equity = Stock Price × Shares Outstanding
4. Calculate M/B ratio = Market Value / Book Value
5. NPV = Investment × (M/B - 1)

**Code Example:**

**Scenario:** Firm has stock price $42, 80,000 shares, total assets $4,200,000, liabilities $1,800,000. Considering $900,000 investment with same P/E and ROE, financed with equity.

**Correct Code:**
```python
# Firm data
stock_price = 42
shares_outstanding = 80000
total_assets = 4200000
total_liabilities = 1800000
investment_amount = 900000

# Book value of equity
book_value_equity = total_assets - total_liabilities

# Market value of equity
market_value_equity = stock_price * shares_outstanding

# Market-to-book ratio
market_to_book = market_value_equity / book_value_equity

# NPV when investment maintains same multiples
npv_investment = investment_amount * (market_to_book - 1)

# Result: 900000 * (3360000/2400000 - 1) = 900000 * 0.4 = 360000
npv_investment
```

**Common Bugs to Avoid:**
- Calculating ROE or P/E explicitly when M/B shortcut applies
- Using market value in denominator of M/B ratio
- Forgetting to subtract 1 from M/B ratio
- Not recognizing when this pattern applies (same multiples condition)

---

## Pattern: Equity as Residual Claim with Limited Liability

**Description:** Equity value in each state equals max(0, Firm_Value - Debt_Face_Value), not simply the difference. Limited liability means equity cannot be negative; shareholders walk away if firm value falls below debt obligations, leaving equity value at zero. This principle applies to ALL equity valuation contexts: state-contingent analysis, merger valuations, project evaluations, and expected value calculations. CRITICAL: Always apply the max(0, ...) constraint when calculating equity values, even in intermediate steps or expected value calculations. **When calculating equity values for MERGED entities in state-contingent scenarios, apply limited liability to EACH FIRM SEPARATELY before combining, not to the merged total.** When a question asks for "equity value" or "values of equity", use context clues to determine output format: (1) If asking for valuation "before merger" or similar single-point-in-time context, return expected equity value (single number), (2) If explicitly asking for "values in each state" or "state-contingent values", return list of state-specific values.

**When to Use:** State-contingent valuation with debt, especially when firm value can fall below debt face value (keywords: "equity value", "stock value", "states of economy", "bond outstanding", "after merger", "limited liability", "expected value", "project payoff", "values of equity")

**When NOT to Use:**
- When calculating total firm/entity value (limited liability only applies to equity claims)
- When debt is explicitly stated to be risk-free or fully covered in all states

**Procedure:**
1. Formula: Equity_Value_in_State = max(0, Firm_Value_in_State - Total_Debt_Face_Value)
2. **CRITICAL FOR MERGERS: If calculating merged equity value, apply limited liability to EACH FIRM SEPARATELY first:**
   - Firm_A_Equity_in_State = max(0, Firm_A_Value_in_State - Firm_A_Debt)
   - Firm_B_Equity_in_State = max(0, Firm_B_Value_in_State - Firm_B_Debt)
   - Merged_Equity_in_State = Firm_A_Equity_in_State + Firm_B_Equity_in_State
3. **DO NOT calculate merged equity as: max(0, (Firm_A_Value + Firm_B_Value) - (Firm_A_Debt + Firm_B_Debt))** — this is incorrect because it allows one firm's positive equity to offset another firm's negative position, violating limited liability
4. For each economic state, calculate firm value minus total debt
5. Apply max(0, ...) wrapper - if result is negative, equity value is zero (limited liability)
6. If result is positive, that is the equity value
7. DETERMINE OUTPUT FORMAT from question context:
   - Single-point valuation context (e.g., "before merger", "value of equity"): return expected value
   - Explicit state-contingent request (e.g., "in each state"): return list of values
   - Default for ambiguous "values of equity": return expected value unless clearly asking for state breakdown
8. For expected equity value, probability-weight across states AFTER applying max(0, ...) to each state
9. VALIDATION: Verify that no equity value is negative in any calculation step
10. Return the equity value(s) in appropriate format (zero or positive, never negative)

**Common Mistakes to Avoid:**
- **CRITICAL: Applying limited liability to merged entity totals instead of to each firm separately before combining (this allows cross-subsidization between firms that violates limited liability principle)**
- Not applying max(0, ...) constraint to equity calculations
- Treating negative equity as valid (violates limited liability)
- Applying limited liability to firm value instead of equity value
- Forgetting that limited liability is applied BEFORE probability-weighting in expected value calculations
- Confusing "equity value" with "firm value" (firm value can be less than debt; equity value cannot be negative)

**Example (sanitized):**
> **Scenario:** Company X has total debt of $800,000. In a boom state (probability 0.65), firm value is $1,200,000. In a recession state (probability 0.35), firm value is $600,000. What is the expected equity value?
>
> **Wrong approach:** Calculating expected firm value first, then subtracting debt.
> ```python
> # WRONG: Not applying limited liability in each state
> expected_firm_value = 0.65 * 1200000 + 0.35 * 600000  # 990,000
> equity_value = expected_firm_value - 800000  # 190,000 - Incorrect
> ```
>
> **Correct approach:**
> 1. Boom state equity: max(0, 1,200,000 - 800,000) = 400,000
> 2. Recession state equity: max(0, 600,000 - 800,000) = 0
> 3. Expected equity: 0.65 × 400,000 + 0.35 × 0 = 260,000
>
> ```python
> # Given data
> debt = 800000
> states = [
>     {'probability': 0.65, 'firm_value': 1200000},  # Boom
>     {'probability': 0.35, 'firm_value': 600000}    # Recession
> ]
> 
> # Apply limited liability in EACH state before weighting
> expected_equity = sum(
>     state['probability'] * max(0, state['firm_value'] - debt)
>     for state in states
> )
> 
> expected_equity  # 260,000
> ```

> **Scenario (Merger Context):** Firm A and Firm B are merging. Each has $450,000 in debt. In a Rain-Rain state, each firm is worth $230,000. What is the merged equity value in this state?
>
> **Wrong approach:** Applying limited liability to merged totals.
> ```python
> # WRONG: Applying limited liability to merged entity
> merged_value = 230000 + 230000  # 460,000
> merged_debt = 450000 + 450000  # 900,000
> merged_equity = max(0, merged_value - merged_debt)  # max(0, -440,000) = 0 - WRONG REASONING
> ```
>
> **Correct approach:**
> 1. Apply limited liability to EACH firm separately:
>    - Firm A equity: max(0, 230,000 - 450,000) = 0
>    - Firm B equity: max(0, 230,000 - 450,000) = 0
> 2. Sum the individual equity values: 0 + 0 = 0
>
> ```python
> # Given data
> firm_a_value = 230000
> firm_a_debt = 450000
> firm_b_value = 230000
> firm_b_debt = 450000
> 
> # CRITICAL: Apply limited liability to EACH firm separately
> firm_a_equity = max(0, firm_a_value - firm_a_debt)  # 0
> firm_b_equity = max(0, firm_b_value - firm_b_debt)  # 0
> 
> # Merged equity is sum of individual equities
> merged_equity = firm_a_equity + firm_b_equity  # 0
> 
> merged_equity
> ```
## Pattern: Risky Debt Valuation in Merger Context

**Description:** When firm value can fall below debt face value, debt value equals the probability-weighted expected value of what bondholders actually receive in each state: min(Firm_Value, Face_Value) in each state. Debt is a contingent claim whose value depends on default risk.

**When to Use:** Debt valuation with state-contingent firm values where firm value may be less than debt face value (keywords: "value of debt", "bond outstanding", "states of economy", "face value", "operate separately")

**Procedure:**
1. Formula: Debt_Value = Σ[Probability_i × min(Firm_Value_i, Face_Value)]
2. For each economic state, determine bondholders' payoff: min(firm value in that state, face value)
3. Multiply each payoff by its probability
4. Sum across all states to get expected debt value
5. Return the total expected value

**Code Example:**

**Scenario:** A firm has debt with face value $200,000. In a boom state (probability 0.60), firm value is $350,000. In a recession state (probability 0.40), firm value is $150,000. What is the debt value?

**Correct Code:**
```python
# Given data
face_value = 200000
states = [
    {'probability': 0.60, 'firm_value': 350000},  # Boom
    {'probability': 0.40, 'firm_value': 150000}   # Recession
]

# Calculate expected debt value considering default risk
debt_value = sum(
    state['probability'] * min(state['firm_value'], face_value)
    for state in states
)

debt_value  # 0.60 * 200000 + 0.40 * 150000 = 180000
```

**Common Bugs to Avoid:**
- Returning face value without considering default risk (assuming debt always pays in full)
- Using max() instead of min() for bondholders' payoff
- Forgetting to probability-weight the payoffs
- Not recognizing that in default states, bondholders receive only the firm value (not face value)

---
## Pattern: Stock-for-Stock Acquisition NPV with Growth Rate Changes

**Description:** NPV of stock acquisition = PV(Target with Synergies) - Market Value of Shares Offered. Must value target using POST-ACQUISITION growth rate and subtract cost based on acquirer's current share price.

**When to Use:** Stock-for-stock mergers with growth rate changes and specific share exchange offers (keywords: "offer X shares", "growth rate will increase", "stock exchange")

**Procedure:**
1. Formula: NPV = [D1_target / (r - g_new)] × Shares_target - (Price_acquirer × Shares_offered)
2. Calculate target's required return from current valuation
3. Value target with NEW growth rate using Gordon model
4. Calculate cost = Acquirer's share price × Shares offered
5. NPV = Target value with synergies - Cost of shares offered

**Code Example:**

**Scenario:** Target: 60,000 shares, $1.20 dividend, $18/share, 3% growth. Acquirer: $55/share, expects to grow target at 4%. Offers 22,000 acquirer shares.

**Correct Code:**
```python
# Target data
target_shares = 60000
target_dividend = 1.20
target_price = 18
target_growth_old = 0.03
target_growth_new = 0.04  # With synergies

# Acquirer data
acquirer_price = 55
shares_offered = 22000

# Target's required return (from current market price)
d1_old = target_dividend * (1 + target_growth_old)
required_return = (d1_old / target_price) + target_growth_old

# Target value with new growth rate
d1_new = target_dividend * (1 + target_growth_new)
value_per_share_new = d1_new / (required_return - target_growth_new)
total_target_value_new = value_per_share_new * target_shares

# Cost of acquisition (market value of shares offered)
cost_of_acquisition = acquirer_price * shares_offered

# NPV of acquisition
npv_acquisition = total_target_value_new - cost_of_acquisition

# Result: (1.248 / 0.0986) * 60000 - (55 * 22000) = 759,635 - 1,210,000 = -450,365
npv_acquisition
```

**Common Bugs to Avoid:**
- Using target's current value instead of value with synergies
- Valuing shares offered at target's price instead of acquirer's price
- Not updating dividend growth rate in valuation
- Confusing number of shares offered with exchange ratio

## Pattern: Ex-Dividend Date Stock Price Calculation

**Description:** Stock price "today" (cum-dividend, before ex-dividend date) includes the value of the declared dividend, while "tomorrow" (ex-dividend date) the price drops by the dividend amount. The current equity value on the balance sheet represents the cum-dividend market value.

**When to Use:** Questions asking for stock price "today" or "before ex-dividend" when a dividend has been declared but not yet paid (keywords: "ex dividend tomorrow", "declared dividend", "stock selling for today", "before ex-dividend")

**Procedure:**
1. Formula: Price_today = Total_Equity_Value / Shares_Outstanding (dividend already reflected in equity value)
2. If asked for ex-dividend price: Price_ex_dividend = Price_today - Dividend_per_share
3. Do NOT add dividend to equity value (it's already included in market value balance sheet)
4. Return the price as a float

**Code Example:**

**Scenario:** A company has total equity market value of $850,000 and 20,000 shares outstanding. It declares a $2.00 per share dividend. The stock goes ex-dividend tomorrow. What is the stock price today?

**Correct Code:**
```python
# Given data
equity_value = 850000  # Market value already includes dividend obligation
shares_outstanding = 20000
dividend_per_share = 2.00

# Today's price (cum-dividend) - equity value already reflects this
price_today = equity_value / shares_outstanding

# If asked for ex-dividend price (tomorrow):
# price_ex_dividend = price_today - dividend_per_share

price_today  # 42.50
```

**Common Bugs to Avoid:**
- Adding dividend to equity value (double-counting: equity value on market balance sheet already reflects cum-dividend price)
- Calculating ex-dividend price when asked for "today" price
- Subtracting dividend from equity value before dividing by shares
- Confusing cum-dividend (before ex-date) with ex-dividend (on/after ex-date) terminology

---

## Pattern: Cash Flow to Investors (Total Distribution)

**Description:** Cash flow to investors represents the total net cash distributed to ALL capital providers (both equity and debt holders). It equals dividends paid plus cash flow to creditors, or equivalently, dividends minus net new borrowing plus interest paid. Proceeds from financing reduce cash flow to investors.

**When to Use:** Questions asking for "cash flows to investors" or "cash flows from the firm to investors" given financing activities and distributions (keywords: "cash flows to investors", "proceeds from borrowing", "proceeds from stock", "payment of dividends")

**Procedure:**
1. Formula: Cash_Flow_to_Investors = Dividends_Paid - Net_New_Borrowing (when interest not given)
2. Or: Cash_Flow_to_Investors = Dividends_Paid + Interest_Paid - Net_New_Borrowing
3. Net new borrowing = Proceeds from debt issuance - Debt repayment
4. Proceeds from stock issuance are NOT cash flows to investors (they're cash FROM investors)
5. Return the net cash outflow to investors (can be negative if firm raised more than it paid out)

**Code Example:**

**Scenario:** A firm paid dividends of $25,000, paid interest of $8,000, issued new long-term debt for $30,000, and repaid $5,000 of existing debt. What is the cash flow to investors?

**Correct Code:**
```python
# Given data
dividends_paid = 25000
interest_paid = 8000
new_debt_issued = 30000
debt_repaid = 5000

# Calculate net new borrowing (cash FROM creditors)
net_new_borrowing = new_debt_issued - debt_repaid  # 25000

# Cash flow to creditors
cash_flow_to_creditors = interest_paid - net_new_borrowing  # 8000 - 25000 = -17000

# Total cash flow to investors
cash_flow_to_investors = dividends_paid + cash_flow_to_creditors  # 25000 - 17000 = 8000

# Alternative direct calculation:
# cash_flow_to_investors = dividends_paid + interest_paid - net_new_borrowing

cash_flow_to_investors  # 8000
```

**Common Bugs to Avoid:**
- Returning only dividends (ignoring cash flows to creditors)
- Adding proceeds from borrowing instead of subtracting (proceeds are cash FROM investors, not TO investors)
- Including proceeds from stock issuance as cash to investors (it's cash FROM equity investors)
- Confusing "to investors" (outflow from firm) with "from investors" (inflow to firm)

---

## Pattern: Gordon Growth Model for Stock Valuation with Required Return Estimation

**Description:** When valuing a stock using the Gordon Growth Model with a changed growth rate, first estimate the required return from current market conditions, then apply the new growth rate. The model is P = D₁/(r - g), where D₁ is next year's dividend, r is required return, and g is growth rate.

**When to Use:** Stock valuation questions with dividend growth rates, especially when growth rate changes or maximum price calculations are needed (keywords: "growth rate", "willing to pay", "maximum price", "constant growth", "dividend")

**Procedure:**
1. Formula: P = D₁ / (r - g), where D₁ = D₀ × (1 + g)
2. Calculate current dividend per share: Total_Dividends / Shares_Outstanding
3. If current price known, solve for required return: r = (D₁ / P₀) + g_current
4. Apply new growth rate with estimated r: P_new = D₀ × (1 + g_new) / (r - g_new)
5. Return the maximum price or valuation

**Code Example:**

**Scenario:** A company has 500,000 shares outstanding, pays total dividends of $280,000, and trades at $45 per share. Current growth rate is 3%. If an acquirer believes it can increase growth to 6%, and uses the current market's required return, what is the maximum price per share to pay?

**Correct Code:**
```python
# Given data
shares_outstanding = 500000
total_dividends = 280000
current_price = 45
current_growth_rate = 0.03
new_growth_rate = 0.06

# Calculate current dividend per share
dividend_per_share = total_dividends / shares_outstanding  # 0.56

# Estimate required return from current market conditions
# P0 = D1 / (r - g), so r = D1/P0 + g
next_dividend_current = dividend_per_share * (1 + current_growth_rate)
required_return = (next_dividend_current / current_price) + current_growth_rate

# Calculate maximum price with new growth rate
next_dividend_new = dividend_per_share * (1 + new_growth_rate)
maximum_price = next_dividend_new / (required_return - new_growth_rate)

maximum_price  # Should be higher than current price due to higher growth
```

**Common Bugs to Avoid:**
- Using current dividend D₀ instead of next dividend D₁ in the numerator
- Applying new growth rate without first estimating required return from current conditions
- Forgetting to convert growth rates to decimals (6% = 0.06)
- Using total dividends instead of per-share dividends
- Not recognizing that r must be greater than g for the model to work

---

## Pattern: Cash Flow from Assets Comprehensive Calculation

**Description:** Cash Flow from Assets (CFFA) equals Operating Cash Flow minus Net Capital Spending minus Change in Net Working Capital. It represents cash generated by assets available to all investors, requiring three distinct components to be calculated and combined.

**When to Use:** Questions asking for "cash flow from assets" or "cash flow from the firm's assets" given income statements and balance sheets (keywords: "cash flow from assets", "CFFA", "calculate cash flow from assets")

**Procedure:**
1. Formula: CFFA = OCF - NCS - Change_in_NWC
2. Calculate OCF = EBIT + Depreciation - Taxes (or Net Income + Interest + Depreciation)
3. Calculate NCS = Ending_Net_Fixed_Assets - Beginning_Net_Fixed_Assets + Depreciation
4. Calculate Change_in_NWC = (Ending_CA - Ending_CL) - (Beginning_CA - Beginning_CL), excluding cash and notes payable
5. Return CFFA (can be negative if reinvestment exceeds cash generation)

**Code Example:**

**Scenario:** A firm has EBIT of $85,000, depreciation of $22,000, taxes of $28,900. Net fixed assets increased from $340,000 to $365,000. Current assets (excluding cash) increased from $95,000 to $108,000. Current liabilities (excluding notes payable) increased from $42,000 to $48,000. Calculate cash flow from assets.

**Correct Code:**
```python
# Given data
ebit = 85000
depreciation = 22000
taxes = 28900
beginning_nfa = 340000
ending_nfa = 365000
beginning_ca_ex_cash = 95000  # Current assets excluding cash
ending_ca_ex_cash = 108000
beginning_cl_ex_notes = 42000  # Current liabilities excluding notes payable
ending_cl_ex_notes = 48000

# Step 1: Operating Cash Flow
ocf = ebit + depreciation - taxes  # 85000 + 22000 - 28900 = 78100

# Step 2: Net Capital Spending
ncs = (ending_nfa - beginning_nfa) + depreciation  # (365000 - 340000) + 22000 = 47000

# Step 3: Change in Net Working Capital
beginning_nwc = beginning_ca_ex_cash - beginning_cl_ex_notes  # 95000 - 42000 = 53000
ending_nwc = ending_ca_ex_cash - ending_cl_ex_notes  # 108000 - 48000 = 60000
change_in_nwc = ending_nwc - beginning_nwc  # 60000 - 53000 = 7000

# Cash Flow from Assets
cffa = ocf - ncs - change_in_nwc  # 78100 - 47000 - 7000 = 24100

cffa  # 24100
```

**Common Bugs to Avoid:**
- Calculating only one component (e.g., OCF) and treating it as CFFA
- Forgetting to add depreciation back in NCS calculation
- Including cash in current assets or notes payable in current liabilities for NWC
- Wrong signs: NCS and Change in NWC should be subtracted (they represent uses of cash)
- Using change in gross fixed assets instead of net fixed assets plus depreciation

---

## Pattern: External Financing Needed with Retained Earnings

**Description:** External Financing Needed (EFN) equals the increase in assets minus the increase in spontaneous liabilities minus retained earnings (additions to equity from profits). Retained earnings are an internal source of financing that reduces external financing requirements.

**When to Use:** Questions asking for "external financing needed" with pro forma projections where no dividends are paid or retention ratio is given (keywords: "external financing needed", "EFN", "no dividends", "projected sales", "proportional to sales")

**Procedure:**
1. Formula: EFN = Increase_in_Assets - Increase_in_Spontaneous_Liabilities - Retained_Earnings
2. Calculate projected assets: Assets × (Projected_Sales / Current_Sales) if proportional
3. Calculate increase in assets: Projected_Assets - Current_Assets
4. Debt typically doesn't change spontaneously (unless stated otherwise)
5. Calculate retained earnings: Projected_Net_Income × (1 - Dividend_Payout_Ratio)
6. If no dividends paid, retained earnings = full projected net income
7. Return EFN

**Code Example:**

**Scenario:** A firm has sales of $12,000, assets of $28,000, costs of $9,500, debt of $13,000, and equity of $15,000. Assets and costs are proportional to sales. Debt and equity are not. No dividends are paid. Next year's sales are projected to be $14,400. What is the external financing needed?

**Correct Code:**
```python
# Given data
current_sales = 12000
current_assets = 28000
current_costs = 9500
current_debt = 13000
current_equity = 15000
projected_sales = 14400
dividend_payout_ratio = 0  # No dividends paid

# Calculate projected values (assets and costs proportional to sales)
sales_growth_factor = projected_sales / current_sales  # 1.2
projected_assets = current_assets * sales_growth_factor  # 28000 * 1.2 = 33600
projected_costs = current_costs * sales_growth_factor  # 9500 * 1.2 = 11400

# Calculate projected net income (no taxes given, so NI = Sales - Costs)
projected_net_income = projected_sales - projected_costs  # 14400 - 11400 = 3000

# Retained earnings (internal financing)
retained_earnings = projected_net_income * (1 - dividend_payout_ratio)  # 3000 * 1 = 3000

# Increase in assets
increase_in_assets = projected_assets - current_assets  # 33600 - 28000 = 5600

# Debt doesn't change spontaneously (stated in problem)
increase_in_debt = 0

# External financing needed
efn = increase_in_assets - increase_in_debt - retained_earnings  # 5600 - 0 - 3000

efn  # 2600
```

**Common Bugs to Avoid:**
- Not subtracting retained earnings from the financing gap (treating all equity growth as external)
- Forgetting that "no dividends" means retention ratio = 100%
- Assuming debt increases proportionally when problem states it doesn't
- Including interest expense without being given interest rate information
- Calculating increase in equity as external financing (equity increases from both retained earnings and external issuance)

---

## Pattern: Merged Company Valuation with Probability-Weighted States

**Description:** When valuing a merged company with state-contingent values, calculate the probability-weighted expected value across all economic states. Merged firm value in each state equals the sum of individual firm values in that state (assuming no synergies).

**When to Use:** Merger valuation questions with multiple economic states and probabilities (keywords: "value of merged company", "states of the economy", "probability", "combined value", "after merger")

**Procedure:**
1. Formula: Merged_Value = Σ[Probability_i × (Firm1_Value_i + Firm2_Value_i)]
2. For each economic state, sum the values of both firms
3. Multiply each combined value by its probability
4. Sum across all states to get expected merged firm value
5. Do NOT subtract debt (debt is a claim on value, not a reduction when valuing the entity)

**Code Example:**

**Scenario:** Firm X and Firm Y are merging. In a boom state (probability 0.70), Firm X is worth $420,000 and Firm Y is worth $310,000. In a recession state (probability 0.30), Firm X is worth $180,000 and Firm Y is worth $120,000. What is the value of the merged company?

**Correct Code:**
```python
# Given data
states = [
    {'probability': 0.70, 'firm_x': 420000, 'firm_y': 310000},  # Boom
    {'probability': 0.30, 'firm_x': 180000, 'firm_y': 120000}   # Recession
]

# Calculate expected value of merged company
merged_value = sum(
    state['probability'] * (state['firm_x'] + state['firm_y'])
    for state in states
)

# Detailed calculation:
# Boom: 0.70 * (420000 + 310000) = 0.70 * 730000 = 511000
# Recession: 0.30 * (180000 + 120000) = 0.30 * 300000 = 90000
# Total: 511000 + 90000 = 601000

merged_value  # 601000
```

**Common Bugs to Avoid:**
- Calculating value for only one state without probability weighting
- Subtracting debt from firm values (debt is a claim, not a reduction of entity value)
- Forgetting to sum both firms' values in each state before weighting
- Using only one firm's value or averaging incorrectly
- Not recognizing that this is an expected value calculation requiring all states

---

## Pattern: Multi-Stage DCF Valuation with Terminal Value

**Description:** Multi-stage DCF valuation requires projecting free cash flows for an explicit forecast period, then calculating terminal value for the perpetual period beyond. Terminal value uses the Gordon Growth formula. CRITICAL: (1) Each growth period may have its own ROC - use the ROC specified for that period to calculate reinvestment rate (Reinv = g / ROC), (2) Do NOT use perpetual period ROC for growth period calculations unless explicitly stated, (3) Terminal value should use the final year's FCF grown by perpetual growth rate, with reinvestment rate adjusted for the perpetual period's ROC, (4) Avoid double-compounding by ensuring FCF projections grow only once per period.

**When to Use:** Firm valuation questions with multi-year projections, terminal value calculations, and specified returns on capital (keywords: "estimate the value of the firm", "terminal value", "return on capital", "perpetual growth", "free cash flow")

**Procedure:**
1. Identify growth periods and their parameters: growth rate (g) and ROC for EACH period
2. For each explicit forecast year:
   - Calculate reinvestment rate using THAT PERIOD'S ROC: Reinv = g / ROC
   - Project EBIT: EBIT_t = EBIT_(t-1) × (1 + g)
   - Calculate FCF: FCF_t = EBIT_t × (1 - Tax_Rate) × (1 - Reinv_Rate)
3. For terminal value at end of forecast period:
   - Use PERPETUAL period's ROC to calculate perpetual reinvestment: Reinv_perpetual = g_perpetual / ROC_perpetual
   - Terminal FCF = Final_Year_FCF × (1 + g_perpetual) / (1 - Reinv_growth_period) × (1 - Reinv_perpetual)
   - OR if final year already at perpetual growth: Terminal FCF = Final_Year_EBIT × (1 + g_perpetual) × (1 - Tax) × (1 - Reinv_perpetual)
   - Terminal Value = Terminal_FCF / (WACC - g_perpetual)
4. Discount all FCFs and TV back to present: PV = Σ[FCF_t / (1 + WACC)^t] + [TV / (1 + WACC)^n]
5. Enterprise Value = PV of all cash flows; Equity Value = Enterprise Value - Net Debt
6. Return the appropriate value (enterprise or equity as requested)

**Example (sanitized):**
> **Scenario:** A firm has current EBIT of $400M, tax rate 25%, WACC 9%. Years 1-2: growth 15% with ROC 25%. Year 3 onward: perpetual growth 4% with ROC 20%. Net debt is $600M. Estimate equity value.
>
> **Wrong approach:** Using perpetual ROC (20%) for growth period calculations, causing incorrect reinvestment rates.
> ```python
> # WRONG: Using perpetual ROC for growth period
> reinv_rate_growth = 0.15 / 0.20  # 0.75 - WRONG, should use 25% ROC
> # This understates reinvestment needs during high-growth phase
> ```
>
> **Correct approach:**
> 1. Growth period (Years 1-2) reinvestment: 15% / 25% = 60%
> 2. Year 1: EBIT = $400M × 1.15 = $460M; FCF = $460M × 0.75 × 0.40 = $138M
> 3. Year 2: EBIT = $460M × 1.15 = $529M; FCF = $529M × 0.75 × 0.40 = $158.7M
> 4. Perpetual reinvestment: 4% / 20% = 20%
> 5. Year 3 EBIT: $529M × 1.04 = $550.16M
> 6. Terminal FCF: $550.16M × 0.75 × (1 - 0.20) = $330.1M
> 7. Terminal Value: $330.1M / (0.09 - 0.04) = $6,602M
> 8. PV of FCFs: $138M/1.09 + $158.7M/1.09² = $260.2M
> 9. PV of TV: $6,602M/1.09² = $5,558.4M
> 10. Enterprise Value: $260.2M + $5,558.4M = $5,818.6M
> 11. Equity Value: $5,818.6M - $600M = $5,218.6M
>
> ```python
> # Given data
> ebit_0 = 400  # millions
> tax_rate = 0.25
> wacc = 0.09
> growth_rate_1_2 = 0.15
> roc_growth = 0.25  # ROC for growth period
> growth_perpetual = 0.04
> roc_perpetual = 0.20  # ROC for perpetual period
> net_debt = 600
> 
> # CRITICAL: Use correct ROC for each period
> reinv_rate_growth = growth_rate_1_2 / roc_growth  # 0.60
> reinv_rate_perpetual = growth_perpetual / roc_perpetual  # 0.20
> 
> # Project FCF for years 1-2 (growth period)
> ebit_1 = ebit_0 * (1 + growth_rate_1_2)
> fcf_1 = ebit_1 * (1 - tax_rate) * (1 - reinv_rate_growth)
> 
> ebit_2 = ebit_1 * (1 + growth_rate_1_2)
> fcf_2 = ebit_2 * (1 - tax_rate) * (1 - reinv_rate_growth)
> 
> # Terminal value calculation
> ebit_3 = ebit_2 * (1 + growth_perpetual)
> fcf_terminal = ebit_3 * (1 - tax_rate) * (1 - reinv_rate_perpetual)
> terminal_value = fcf_terminal / (wacc - growth_perpetual)
> 
> # Discount to present
> pv_fcf_1 = fcf_1 / (1 + wacc)**1
> pv_fcf_2 = fcf_2 / (1 + wacc)**2
> pv_terminal = terminal_value / (1 + wacc)**2
> 
> # Enterprise and equity value
> enterprise_value = pv_fcf_1 + pv_fcf_2 + pv_terminal
> equity_value = enterprise_value - net_debt
> 
> equity_value
> ```

**Common Mistakes to Avoid:**
- **Using perpetual period ROC to calculate reinvestment rate for growth period (CRITICAL ERROR)**
- Using growth period ROC for perpetual period calculations
- Double-compounding FCF (growing EBIT then growing FCF again)
- Not adjusting FCF for different reinvestment rates between growth and perpetual periods
- Forgetting to discount terminal value back to present
- Confusing enterprise value with equity value (must subtract net debt)

---
## Pattern: Homemade Leverage Comparison with Cost Equalization

**Description:** Modigliani-Miller homemade leverage principle states that investors can replicate a levered firm's returns by purchasing an unlevered firm and borrowing personally. To compare strategies, equalize the net initial cost (equity purchase minus personal borrowing), then compare dollar returns. CRITICAL: For levered firms, equity holders receive operating income MINUS interest expense paid to debt holders. The strategy with higher dollar return at equal net cost is superior.

**When to Use:** Questions comparing investment in levered vs unlevered firms with personal borrowing options (keywords: "homemade leverage", "borrow at X percent", "purchase Y percent of equity", "increase dollar return", "same initial cost")

**Procedure:**
1. For levered firm, calculate earnings to equity: Earnings_to_Equity = Operating_Income - Interest_Expense
2. Calculate Strategy 1 (levered firm): Net_Cost_1 = Equity_Stake × Levered_Firm_Equity_Value
3. Calculate Strategy 1 return: Return_1 = Equity_Stake × Earnings_to_Equity (NOT operating income)
4. Calculate Strategy 2 (unlevered + borrow): Equity_Cost_2 = Equity_Stake × Unlevered_Firm_Equity_Value
5. To equalize costs: Personal_Borrowing = Equity_Cost_2 - Net_Cost_1
6. Calculate Strategy 2 return: Return_2 = (Equity_Stake × Unlevered_Operating_Income) - (Personal_Borrowing × Borrowing_Rate)
7. Compare: If Return_2 > Return_1, answer "Yes, can increase returns"
8. Return boolean or comparison statement, NOT just numerical difference

**Example (sanitized):**
> **Scenario:** Levered Firm L has equity value $1,500,000, operating income $400,000, interest expense $60,000. Unlevered Firm U has equity value $2,200,000, operating income $350,000. An investor can borrow at 8% and wants to purchase 6% of either firm's equity. Can the investor increase dollar returns by buying U and borrowing to match L's net cost?
>
> **Wrong approach:** Using operating income instead of earnings to equity for levered firm.
> ```python
> # WRONG: Using operating income for levered firm
> return_L = 0.06 * 400000  # Should subtract interest first
> # This overstates what equity holders actually receive
> ```
>
> **Correct approach:**
> 1. L's earnings to equity: $400,000 - $60,000 = $340,000
> 2. Strategy L cost: 6% × $1,500,000 = $90,000
> 3. Strategy L return: 6% × $340,000 = $20,400
> 4. Strategy U equity cost: 6% × $2,200,000 = $132,000
> 5. Personal borrowing needed: $132,000 - $90,000 = $42,000
> 6. Strategy U return: (6% × $350,000) - ($42,000 × 8%) = $21,000 - $3,360 = $17,640
> 7. Comparison: $17,640 < $20,400, so NO, cannot increase returns
>
> ```python
> # Given data
> levered_equity_value = 1500000
> levered_operating_income = 400000
> levered_interest_expense = 60000
> unlevered_equity_value = 2200000
> unlevered_operating_income = 350000
> borrowing_rate = 0.08
> equity_stake = 0.06
> 
> # CRITICAL: Calculate earnings to equity for levered firm
> levered_earnings_to_equity = levered_operating_income - levered_interest_expense
> 
> # Strategy 1: Buy levered firm
> cost_levered = equity_stake * levered_equity_value
> return_levered = equity_stake * levered_earnings_to_equity
> 
> # Strategy 2: Buy unlevered firm + personal borrowing
> cost_unlevered_equity = equity_stake * unlevered_equity_value
> personal_borrowing = cost_unlevered_equity - cost_levered
> return_unlevered_before_interest = equity_stake * unlevered_operating_income
> interest_on_borrowing = personal_borrowing * borrowing_rate
> return_unlevered_net = return_unlevered_before_interest - interest_on_borrowing
> 
> # Comparison
> can_increase_return = return_unlevered_net > return_levered
> 
> can_increase_return  # True or False
> ```

**Common Mistakes to Avoid:**
- **Using operating income instead of earnings to equity for levered firm (CRITICAL ERROR)**
- Not subtracting interest expense from operating income to get equity holders' share
- Not equalizing initial net costs before comparing returns (invalid comparison)
- Returning numerical difference instead of yes/no answer to the question
- Forgetting to subtract interest expense on personal borrowing from Strategy 2 returns

---
## Pattern: Expected Value Calculations with Debt and Limited Liability

**Description:** When calculating expected firm or project values in the presence of debt, distinguish between: (1) expected FIRM/PROJECT value (simple probability-weighted average of all state values - NO debt adjustment), and (2) expected EQUITY value (probability-weighted average of max(0, Value - Debt) in each state). Firm/project value can be less than debt in some states - this is valid and does NOT require validation checks. Limited liability only applies when calculating equity values, not firm/project values. CRITICAL: Carefully read the question to determine whether it asks for "expected value of the company/project" (firm value) or "expected value of equity/to shareholders" (equity value).

**When to Use:** Questions asking for "expected value of company/project" or "expected value of equity" with state-contingent outcomes and debt present (keywords: "expected value", "project payoff", "states of economy", "bond outstanding", "high-volatility", "low-volatility", "expected value of the company", "expected value of equity")

**When NOT to Use:**
- When the question asks for state-specific values (not expected values)
- When no debt is present (use simple probability weighting)
- When asking for debt value (use different pattern for risky debt valuation)

**Procedure:**
1. Identify what is being asked: expected FIRM/PROJECT value or expected EQUITY value
2. For expected FIRM/PROJECT value:
   - Formula: E[Firm_Value] = Σ[Probability_i × Firm_Value_i]
   - Simply probability-weight all state values
   - DO NOT apply max(0, ...) or debt adjustments
   - DO NOT add validation checks requiring values exceed debt
   - Use proper iteration (zip or indexed loops) to avoid Cartesian products
3. For expected EQUITY value:
   - Formula: E[Equity_Value] = Σ[Probability_i × max(0, Firm_Value_i - Debt)]
   - Apply limited liability (max(0, ...)) in EACH state before weighting
   - Then probability-weight the equity values
4. Return the appropriate expected value

**Example (sanitized):**
> **Scenario:** A company with $5,000 in debt is evaluating a project. In a good state (probability 0.60), the project generates $7,200. In a bad state (probability 0.40), it generates $3,800. What is: (a) the expected project value, and (b) the expected equity value?
>
> **Wrong approach:** Applying limited liability to firm value, or using nested loops creating Cartesian products.
> ```python
> # WRONG: Applying limited liability to firm value
> expected_firm = 0.60 * max(0, 7200 - 5000) + 0.40 * max(0, 3800 - 5000)
> # This calculates equity value, not firm value
> 
> # WRONG: Nested loop creating Cartesian product
> for prob in probabilities:
>     for value in values:  # Creates 4 iterations instead of 2
>         ...
> ```
>
> **Correct approach:**
> 1. Expected project/firm value (no debt adjustment):
>    - E[Firm] = 0.60 × 7,200 + 0.40 × 3,800 = 4,320 + 1,520 = $5,840
> 2. Expected equity value (with limited liability):
>    - Good state equity: max(0, 7,200 - 5,000) = $2,200
>    - Bad state equity: max(0, 3,800 - 5,000) = $0
>    - E[Equity] = 0.60 × 2,200 + 0.40 × 0 = $1,320
>
> ```python
> # Given data
> debt = 5000
> states = [
>     {'probability': 0.60, 'value': 7200},  # Good
>     {'probability': 0.40, 'value': 3800}   # Bad
> ]
> 
> # (a) Expected firm/project value (no debt adjustment)
> # Use proper iteration to avoid Cartesian products
> expected_firm_value = sum(
>     state['probability'] * state['value']
>     for state in states
> )
> # 0.60 * 7200 + 0.40 * 3800 = 5840
> 
> # (b) Expected equity value (with limited liability)
> expected_equity_value = sum(
>     state['probability'] * max(0, state['value'] - debt)
>     for state in states
> )
> # 0.60 * max(0, 2200) + 0.40 * max(0, -1200) = 1320
> 
> # Return appropriate value based on question
> expected_firm_value  # For question (a)
> # expected_equity_value  # For question (b)
> ```

**Common Mistakes to Avoid:**
- Adding validation checks (assert statements) requiring firm/project values to exceed debt
- Applying limited liability (max(0, ...)) when calculating expected firm value (only applies to equity)
- **Using nested loops that create Cartesian products (iterating N×M times instead of N times)**
- Confusing "expected value of company" (firm value) with "expected value to shareholders" (equity value)
- Treating states where value < debt as errors rather than valid scenarios
- **Returning equity value when the question asks for company/project value**
- **Returning firm value when the question asks for equity value**

---
## Pattern: No-Synergy Merger P/E Calculation

**Description:** When two firms merge with no synergies, the post-merger P/E ratio is calculated as the combined market value divided by combined earnings. This differs from the NPV=0 case because it applies to any merger structure (cash or stock) where no value is created. The key insight is that total market capitalization equals the sum of individual market values, and total earnings equals the sum of individual earnings.

**When to Use:** Merger questions asking for P/E ratio when "no synergies" or "no synergy gains" are specified, regardless of payment method (keywords: "no synergies", "no synergy gains", "price-earnings ratio", "P/E ratio after merger")

**Procedure:**
1. Calculate pre-merger market value for each firm: Market_Value = Shares × Price_per_Share
2. Calculate combined market value: Total_Market_Value = Firm_A_Market_Value + Firm_B_Market_Value
3. Calculate combined earnings: Total_Earnings = Firm_A_Earnings + Firm_B_Earnings
4. Post-merger P/E = Total_Market_Value / Total_Earnings
5. Return the P/E ratio

**Code Example:**

**Scenario:** Company X has 1,000 shares at $40/share with earnings of $3,000. Company Y has 500 shares at $20/share with earnings of $1,200. If they merge with no synergies, what is the post-merger P/E ratio?

**Correct Code:**
```python
# Firm X data
x_shares = 1000
x_price = 40
x_earnings = 3000

# Firm Y data
y_shares = 500
y_price = 20
y_earnings = 1200

# Calculate pre-merger market values
x_market_value = x_shares * x_price  # 40,000
y_market_value = y_shares * y_price  # 10,000

# Combined market value (no synergies means simple addition)
combined_market_value = x_market_value + y_market_value  # 50,000

# Combined earnings
combined_earnings = x_earnings + y_earnings  # 4,200

# Post-merger P/E ratio
post_merger_pe = combined_market_value / combined_earnings  # 11.90

post_merger_pe
```

**Common Bugs to Avoid:**
- Using only acquirer's P/E ratio without calculation
- Calculating weighted average of P/E ratios (incorrect methodology)
- Confusing this with NPV=0 stock dilution scenario (different calculation)
- Forgetting to include both firms' market values and earnings
- Assuming P/E stays constant when it actually changes due to different pre-merger P/E ratios

---

## Pattern: Project Abandonment and Optimal Economic Life

**Description:** When evaluating projects with abandonment options, calculate NPV for each possible economic life (1 year, 2 years, etc.) and identify which life maximizes NPV. The question asks for the OPTIMAL ECONOMIC LIFE (number of years), not the NPV value itself. Each abandonment scenario includes: (1) operating cash flows up to abandonment, (2) after-tax salvage value at abandonment, and (3) recovery of net working capital.

**When to Use:** Questions asking for "optimal economic life", "what economic life maximizes value", or "when should the project be abandoned" with multiple possible termination dates (keywords: "abandoned after", "economic life", "maximizes value", "market value of equipment")

**Procedure:**
1. For each possible economic life (1, 2, 3, ... years):
   - Calculate annual operating cash flows: OCF = (Revenue - Costs - Depreciation) × (1 - Tax) + Depreciation
   - Calculate after-tax salvage value: Salvage - (Salvage - Book_Value) × Tax_Rate
   - Add NWC recovery in terminal year
   - Discount all cash flows to present value
2. Compare NPVs across all economic lives
3. Identify the economic life (number of years) that produces maximum NPV
4. CRITICAL: Return the YEAR NUMBER (1, 2, 3, etc.), NOT the NPV value
5. If asked to show NPVs, display them, but final answer must be the optimal year

**Code Example:**

**Scenario:** A project requires $10M initial investment, $800K NWC (recoverable). Annual revenue $8M, costs $3M, 25% tax, 12% discount. Equipment market values: Year 1: $9M, Year 2: $7M, Year 3: $5M. What economic life maximizes value?

**Correct Code:**
```python
# Project parameters
initial_investment = 10_000_000
initial_nwc = 800_000
annual_revenue = 8_000_000
annual_costs = 3_000_000
tax_rate = 0.25
discount_rate = 0.12
project_life = 3  # Maximum possible life

# Market values at each year
market_values = {1: 9_000_000, 2: 7_000_000, 3: 5_000_000}

def calculate_npv(economic_life):
    # Annual depreciation (straight-line)
    annual_depreciation = initial_investment / project_life
    
    # Initial outflow
    cash_flows = [-initial_investment - initial_nwc]
    
    # Operating cash flows
    for year in range(1, economic_life + 1):
        pretax_income = annual_revenue - annual_costs - annual_depreciation
        ocf = pretax_income * (1 - tax_rate) + annual_depreciation
        cash_flows.append(ocf)
    
    # Terminal year adjustments
    book_value = initial_investment - (annual_depreciation * economic_life)
    salvage_value = market_values[economic_life]
    tax_on_salvage = (salvage_value - book_value) * tax_rate
    
    cash_flows[-1] += salvage_value - tax_on_salvage + initial_nwc
    
    # Calculate NPV
    npv = sum(cf / (1 + discount_rate)**t for t, cf in enumerate(cash_flows))
    return npv

# Calculate NPV for each possible life
npvs = {year: calculate_npv(year) for year in range(1, project_life + 1)}

# Find optimal economic life (the YEAR, not the NPV)
optimal_life = max(npvs, key=npvs.get)

# Display results (optional)
for year, npv in npvs.items():
    print(f"NPV ({year} year{'s' if year > 1 else ''}): ${npv:,.2f}")
print(f"Optimal Economic Life: {optimal_life} year{'s' if optimal_life > 1 else ''}")

# CRITICAL: Return the YEAR NUMBER, not the NPV
optimal_life
```

**Common Bugs to Avoid:**
- Returning the NPV value instead of the year number (optimal economic life)
- Not calculating NPV for all possible abandonment dates
- Forgetting to include after-tax salvage value in terminal year
- Not recovering NWC in terminal year
- Using wrong book value for tax calculation on salvage
- Returning intermediate results instead of final answer (the optimal year)

---

## Pattern: Mutually Exclusive Project Selection

**Description:** When comparing multiple projects to select the best one, calculate NPV for each project, identify which has the highest NPV, and return the PROJECT NAME/IDENTIFIER as the answer, not the numerical NPV value. The question typically asks "which project should be chosen/taken" or "which project is better."

**When to Use:** Questions asking for project selection or comparison where the answer should be a project name (keywords: "which project should", "which project is better", "should you choose", "based on NPV which")

**Procedure:**
1. Calculate NPV for each project using proper sign conventions
2. Compare NPVs across all projects
3. Identify the project with the HIGHEST NPV (least negative if all are negative)
4. CRITICAL: Return the PROJECT NAME/IDENTIFIER as a string, not the NPV value
5. Match the project name format from the question context (e.g., "Project A", "deepwater fishing", "dry prepeg")

**Example (sanitized):**
> **Scenario:** Company evaluating two projects. Project Alpha: initial cost $500K, generates $180K/year for 4 years at 10% discount. Project Beta: initial cost $600K, generates $210K/year for 4 years at 10% discount. Which project should be taken?
>
> **Wrong approach:** Returning the numerical NPV value instead of project name.
> ```python
> # Calculate NPVs
> npv_alpha = -500000 + sum(180000 / 1.10**t for t in range(1, 5))
> npv_beta = -600000 + sum(210000 / 1.10**t for t in range(1, 5))
> 
> # WRONG: Returning NPV value
> max(npv_alpha, npv_beta)  # Returns a number, not project name
> ```
>
> **Correct approach:**
> 1. Calculate NPV for Alpha: -$500K + PV($180K annuity) = $70,566
> 2. Calculate NPV for Beta: -$600K + PV($210K annuity) = $65,827
> 3. Compare: Alpha NPV ($70,566) > Beta NPV ($65,827)
> 4. Return project name: "Project Alpha"
>
> ```python
> # Calculate NPVs
> npv_alpha = -500000 + sum(180000 / 1.10**t for t in range(1, 5))
> npv_beta = -600000 + sum(210000 / 1.10**t for t in range(1, 5))
> 
> # Store in dictionary for comparison
> projects = {
>     'Project Alpha': npv_alpha,
>     'Project Beta': npv_beta
> }
> 
> # Find project with highest NPV
> best_project = max(projects, key=projects.get)
> 
> # Return project name as string
> best_project  # 'Project Alpha'
> ```

**Common Mistakes to Avoid:**
- Returning the NPV value instead of the project name
- Returning a boolean (True/False) instead of project identifier
- Not matching the project name format from the question context
- Selecting project with lowest NPV instead of highest (forgetting that less negative is better)

---