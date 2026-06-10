# SKILL PATTERNS FOR CORPORATE FINANCE MULTI-STEP REASONING

## Pattern: NPV of Credit Policy Change with Working Capital Investment

**Description:** Credit policy changes require computing NPV as the present value of incremental perpetual cash flows MINUS the initial investment in accounts receivable (working capital tied up). Many implementations calculate only one component instead of the complete two-part NPV framework.

**When to Use:** Questions involving credit policy changes, terms of sale modifications (e.g., cash-only to net 30 days), or evaluating whether to extend credit to customers.

**Procedure:**
1. Formula: NPV = PV(Incremental Monthly Profit as Perpetuity) - Initial Investment in Receivables
2. Calculate incremental monthly profit: (New Price - New Cost) × New Units - (Old Price - Old Cost) × Old Units
3. Convert to perpetuity PV: Incremental Monthly Profit / Monthly Required Return
4. Calculate initial receivables investment: (New Cost per Unit × New Monthly Units) × (Credit Period / Days per Month)
5. Compute NPV: PV from step 3 minus Investment from step 4
6. Return final NPV value as expression

**Code Example:**

**Scenario:** A company considers changing from cash-only to net 45 days credit. Current: price=$150, cost=$110, units=800/month. New: price=$158, cost=$112, units=850/month. Required return=0.8% per month.

**Correct Code:**
```python
# Current policy parameters
current_price = 150
current_cost = 110
current_units = 800

# New policy parameters
new_price = 158
new_cost = 112
new_units = 850

# Financial parameters
monthly_return = 0.008
credit_period_days = 45
days_per_month = 30

# Step 1: Calculate incremental monthly profit
current_monthly_profit = (current_price - current_cost) * current_units
new_monthly_profit = (new_price - new_cost) * new_units
incremental_monthly_profit = new_monthly_profit - current_monthly_profit

# Step 2: PV of incremental profit perpetuity
pv_incremental_profit = incremental_monthly_profit / monthly_return

# Step 3: Initial investment in accounts receivable
# This is the cost of goods tied up during the credit period
monthly_cost_of_goods = new_cost * new_units
receivables_investment = monthly_cost_of_goods * (credit_period_days / days_per_month)

# Step 4: Calculate NPV
npv = pv_incremental_profit - receivables_investment

npv
```

**Common Bugs to Avoid:**
- Calculating only the incremental profit or only the receivables investment (not both components)
- Using revenue instead of cost for the receivables investment calculation
- Forgetting to convert credit period to monthly fraction (days/30)
- Using print() instead of expression on last line
- Not recognizing this as a capital budgeting problem requiring NPV framework

---

## Pattern: Equity Issuance at Market Price with Book Value Reconciliation

**Description:** When new equity is issued at market price to finance investments, the number of new shares equals investment cost divided by current market price. New book value per share requires adding the investment to old book equity and dividing by total shares (old + new).

**When to Use:** Questions about equity financing, share issuance, book value per share calculations after new equity offerings, or dilution analysis.

**Procedure:**
1. Formula: New BV per Share = (Old Book Equity + Investment) / (Old Shares + New Shares)
2. Calculate old book equity: Total Assets - Total Liabilities
3. Determine new shares issued: Investment Cost / Current Market Price per Share
4. Calculate new total book equity: Old Book Equity + Investment Amount
5. Calculate new total shares: Old Shares + New Shares Issued
6. Compute new book value per share: New Book Equity / New Total Shares

**Code Example:**

**Scenario:** A firm has 50,000 shares at $60 market price, total assets=$6,800,000, total liabilities=$3,200,000. It issues new equity to finance a $1,200,000 investment.

**Correct Code:**
```python
# Current firm parameters
current_shares = 50000
market_price_per_share = 60
total_assets = 6800000
total_liabilities = 3200000

# Investment parameters
investment_cost = 1200000

# Step 1: Calculate old book equity
old_book_equity = total_assets - total_liabilities

# Step 2: Calculate number of new shares issued at market price
new_shares_issued = investment_cost / market_price_per_share

# Step 3: Calculate new book equity (investment adds to book value)
new_book_equity = old_book_equity + investment_cost

# Step 4: Calculate total shares after issuance
total_shares = current_shares + new_shares_issued

# Step 5: Calculate new book value per share
new_book_value_per_share = new_book_equity / total_shares

new_book_value_per_share
```

**Common Bugs to Avoid:**
- Dividing investment by book value per share instead of market price to find new shares
- Forgetting to add the investment amount to book equity
- Using only the investment divided by new shares (ignoring existing equity and shares)
- Incorrectly computing dilution effects by not properly aggregating old and new components
- Rounding errors when shares should be whole numbers

---

## Pattern: Fixed Asset Reconciliation for Capital Spending

**Description:** Cash flow from assets requires reconciling balance sheet changes in net fixed assets with income statement depreciation. The relationship is: Change in NFA = Capital Spending - Depreciation, which must be rearranged to find actual cash spent: Capital Spending = Change in NFA + Depreciation. **Critical distinction: When "purchases" or "capital spending" is explicitly given in the question, it represents GROSS capital spending (actual cash out). When only balance sheet changes are given, use the reconciliation formula.**

**When to Use:** Questions about cash flow from assets, capital expenditures, net capital spending, or reconciling balance sheet and income statement for investment activities.

**Procedure:**
1. **CHECK: Does the question explicitly state "purchased $X in fixed assets" or "capital spending was $X"?**
   - If YES: This is gross capital spending; use this value directly as net capital spending
   - If NO: Calculate using reconciliation formula below
2. Formula (when purchases NOT given): Net Capital Spending = Change in NFA + Depreciation
3. Calculate change in net fixed assets: NFA(end) - NFA(beginning)
4. Extract depreciation from income statement
5. Compute net capital spending: Change in NFA + Depreciation (only if not explicitly given)
6. For cash flow from assets, also calculate: Operating Cash Flow - Net Capital Spending - Change in NWC
7. Return the requested metric (capital spending or full cash flow from assets)

**Example (sanitized):**
> **Scenario A (Reconciliation needed):** Company has NFA of $12,500 (end) and $10,800 (start). Depreciation=$1,950. Calculate net capital spending.
>
> **Scenario B (Purchases given):** Company purchased $3,200 in new fixed assets. NFA increased from $10,800 to $12,050. Depreciation=$1,950. Calculate net capital spending.
>
> **Wrong approach for Scenario B:** Use reconciliation formula when purchases are given
> ```python
> change_in_nfa = 12050 - 10800  # = 1,250
> net_capital_spending = change_in_nfa + depreciation  # = 1,250 + 1,950 = 3,200
> # This happens to match, but ignores the explicit purchase information
> ```
>
> **Correct approach:**
> 
> **For Scenario A (no purchases given):**
> ```python
> nfa_end = 12500
> nfa_start = 10800
> depreciation = 1950
> 
> # Use reconciliation formula
> change_in_nfa = nfa_end - nfa_start
> net_capital_spending = change_in_nfa + depreciation
> 
> net_capital_spending  # = 1,700 + 1,950 = 3,650
> ```
>
> **For Scenario B (purchases explicitly given):**
> ```python
> new_fixed_assets_purchased = 3200  # Given in question
> depreciation = 1950
> 
> # When purchases are stated, use directly
> # This is the actual cash spent on capital investments
> net_capital_spending = new_fixed_assets_purchased
> 
> net_capital_spending  # = 3,200
> ```
> 
> **Key insight:** The reconciliation formula (Change in NFA + Depreciation) and explicit purchases should theoretically match, but when the question provides actual purchase amounts, that represents the true cash outflow and should be used directly.

**Common Mistakes to Avoid:**
- Using only the change in NFA without adding back depreciation when purchases are NOT given (depreciation is non-cash)
- **Calculating change in NFA + depreciation when the question explicitly states the purchase amount**
- Subtracting depreciation instead of adding it when computing capital spending
- Confusing "capital spending" (cash out) with "change in NFA" (book value change)
- **Ignoring explicit "purchased $X in fixed assets" statements and using reconciliation instead**
- Sign errors: capital spending and NWC increases are uses of cash (subtract from OCF)
- Not recognizing the reconciliation identity: Ending NFA = Beginning NFA + Capital Spending - Depreciation
## Pattern: Multi-Component Cash Flow Assembly

**Description:** Complete cash flow calculations require assembling multiple independent components (operating, investing, financing) with correct sign conventions. Each component must be calculated separately before final aggregation. Critical: Use actual tax values from financial statements when provided; only calculate taxes from EBIT × tax_rate when not explicitly given. For project-based cash flows (IRR/NPV analysis), use EBIT-based tax calculations; for historical financial statement analysis, prefer actual taxes paid.

**When to Use:** Questions asking for cash flow from assets, cash flow to creditors, cash flow to stockholders, or statement of cash flows construction from historical financial statements.

**When NOT to Use:** 
- Project evaluation questions (IRR, NPV) that require pro-forma cash flow projections
- Questions involving terminal cash flows with salvage value and NWC recovery
- Multi-year project analysis where EBIT-based taxes are standard practice
- **External Financing Needed (EFN) calculations — these use pro-forma balance sheet projections, not cash flow assembly**
- **Questions about sustainable growth or internal/external financing requirements**
- **Any question asking "what is the external financing needed?" or similar phrasing**

**Procedure:**
1. Formula: CF from Assets = Operating CF - Net Capital Spending - Change in NWC
2. **CHECK: Determine context type:**
   - **Historical financial statement analysis**: Use actual taxes from income statement when provided
   - **Project evaluation (IRR/NPV)**: Calculate taxes as EBIT × tax_rate for each period
3. Calculate operating cash flow: EBIT + Depreciation - Taxes (or NI + Depreciation + Interest)
4. Calculate net capital spending: Change in NFA + Depreciation
5. Calculate change in net working capital: Change in CA - Change in CL
6. Apply correct signs: outflows are negative, inflows are positive
7. Aggregate components according to the specific cash flow identity requested

**Common Mistakes to Avoid:**
- **Using calculated taxes (EBIT × tax_rate) when actual taxes are provided in historical income statements**
- Applying historical financial statement procedures to project evaluation contexts
- **Confusing External Financing Needed (EFN) with cash flow from assets — EFN uses pro-forma balance sheets and retention ratios, not cash flow identities**
- Mixing up sign conventions (increases in assets use cash, increases in liabilities provide cash)
- Calculating only one component when the question requires full cash flow from assets
- Using net income without adding back interest for EBIT-based OCF calculation
- Double-counting depreciation (it appears in both OCF and capital spending calculations)
- Forgetting that change in NWC = change in CA - change in CL (not just change in CA)
- Using print() instead of final expression

**Example (sanitized):**
> **Scenario A (Historical Analysis):** Calculate cash flow from assets for 2023. Income statement shows: Sales=$45,000, COGS=$22,000, Depreciation=$2,100, Interest=$650, **Taxes=$1,850** (explicitly stated). Balance sheet: NFA increased from $18,500 to $20,200. CA increased from $5,400 to $5,900. CL increased from $2,100 to $2,350.
> 
> **Correct approach for historical analysis:** Use actual taxes from income statement
> ```python
> # Income statement data
> sales = 45000
> cogs = 22000
> depreciation = 2100
> interest = 650
> taxes_paid = 1850  # Use ACTUAL value from income statement
> 
> # Balance sheet data
> nfa_end = 20200
> nfa_start = 18500
> ca_end = 5900
> ca_start = 5400
> cl_end = 2350
> cl_start = 2100
> 
> # Calculate EBIT
> ebit = sales - cogs - depreciation
> 
> # Calculate operating cash flow using ACTUAL taxes
> operating_cash_flow = ebit + depreciation - taxes_paid
> 
> # Calculate net capital spending
> change_in_nfa = nfa_end - nfa_start
> net_capital_spending = change_in_nfa + depreciation
> 
> # Calculate change in net working capital
> change_in_ca = ca_end - ca_start
> change_in_cl = cl_end - cl_start
> change_in_nwc = change_in_ca - change_in_cl
> 
> # Calculate cash flow from assets
> cash_flow_from_assets = operating_cash_flow - net_capital_spending - change_in_nwc
> 
> cash_flow_from_assets
> ```
>
> **Scenario B (Project Evaluation - NOT applicable for this pattern):** This pattern should NOT be used for project IRR/NPV calculations. See project-specific patterns instead.
>
> **Scenario C (External Financing Needed - NOT applicable for this pattern):** Questions asking "what is the external financing needed?" require pro-forma balance sheet analysis with retention ratios, NOT cash flow assembly. Do not apply this pattern to EFN questions.

---
## Pattern: Project Cash Flow with Terminal Value and NWC Recovery

**Description:** Project evaluation (IRR/NPV) requires constructing annual cash flows including operating cash flows, NWC investments, and terminal cash flows. Terminal year includes salvage value (net of taxes on gain/loss) and recovery of ALL accumulated net working capital. NWC changes are based on incremental revenue changes, and the final year recovers the cumulative NWC investment.

**When to Use:** 
- IRR or NPV calculations for multi-year projects
- Questions involving equipment salvage value at project end
- Projects with working capital requirements tied to sales/revenue levels
- Capital budgeting decisions with defined project lifespans

**Procedure:**
1. **Calculate annual operating cash flows:**
   - EBIT = Revenue - Variable Costs - Fixed Costs - Depreciation
   - Taxes = EBIT × tax_rate (use max(EBIT, 0) to avoid negative taxes)
   - OCF = EBIT - Taxes + Depreciation (add back non-cash depreciation)

2. **Calculate NWC changes for each year:**
   - Initial NWC investment (Year 0): Given initial requirement
   - Subsequent years: Based on percentage of revenue increase for NEXT year
   - Track cumulative NWC balance, not just changes
   - Annual NWC investment = Change in cumulative NWC balance

3. **Calculate terminal cash flow (final year):**
   - Salvage value: Equipment selling price
   - Book value: Original cost - Accumulated depreciation
   - Tax on salvage: (Salvage - Book Value) × tax_rate if gain; 0 if loss
   - After-tax salvage: Salvage - Tax on salvage
   - **NWC recovery: Return ENTIRE cumulative NWC balance (not just final year change)**
   - Terminal CF = After-tax salvage + Total NWC recovery

4. **Construct complete cash flow array:**
   - Year 0: -(Equipment cost + Initial NWC)
   - Years 1 to N-1: OCF - NWC investment for that year
   - Year N: OCF + Terminal CF (includes salvage and full NWC recovery)

5. **Calculate IRR/NPV:**
   - Use financial functions (npf.irr or npf.npv)
   - Return result in appropriate format (decimal for IRR)

**Common Mistakes to Avoid:**
- Adding only the final year's NWC change instead of recovering the entire cumulative NWC balance
- Calculating NWC changes based on unit increases × price instead of percentage of revenue increase
- Forgetting to account for taxes on salvage value gains
- Using actual taxes from income statements (projects use EBIT-based tax calculations)
- Not tracking cumulative NWC balance separately from annual changes
- Including NWC recovery as a separate cash flow instead of adding it to terminal year
- Calculating book value incorrectly (must sum all depreciation taken, not just final year)

**Example (sanitized):**
> **Scenario:** A 4-year project requires $800,000 equipment (5-year MACRS) and $120,000 initial NWC. Annual NWC investment = 12% of next year's revenue increase. Year 1-4 revenues: $500k, $580k, $620k, $590k. Variable costs = 40% of revenue, fixed costs = $100k/year. Salvage = 25% of original cost. Tax rate = 30%.
>
> **Wrong approach:** Add only final NWC change to terminal cash flow
> ```python
> # ... other calculations ...
> # Year 4 terminal cash flow
> nwc_change_year4 = nwc_balance[4] - nwc_balance[3]  # Only the change
> terminal_cf = after_tax_salvage + nwc_change_year4  # WRONG: Missing prior NWC
> ```
>
> **Correct approach:** Recover entire cumulative NWC
> ```python
> import numpy_financial as npf
> 
> # Project parameters
> equipment_cost = 800000
> initial_nwc = 120000
> revenues = [500000, 580000, 620000, 590000]
> variable_cost_pct = 0.40
> fixed_costs = 100000
> salvage_pct = 0.25
> tax_rate = 0.30
> macrs_5yr = [0.2000, 0.3200, 0.1920, 0.1152, 0.1152]
> 
> # Calculate depreciation
> depreciation = [equipment_cost * macrs_5yr[i] for i in range(4)]
> 
> # Calculate NWC balance (cumulative)
> nwc_balance = [initial_nwc]
> for i in range(len(revenues) - 1):
>     revenue_increase = revenues[i+1] - revenues[i]
>     nwc_investment = 0.12 * revenue_increase if revenue_increase > 0 else 0
>     nwc_balance.append(nwc_balance[-1] + nwc_investment)
> 
> # Calculate operating cash flows
> ocf = []
> for i in range(len(revenues)):
>     ebit = revenues[i] - (revenues[i] * variable_cost_pct) - fixed_costs - depreciation[i]
>     taxes = max(ebit, 0) * tax_rate
>     ocf.append(ebit - taxes + depreciation[i])
> 
> # Calculate terminal cash flow
> salvage_value = equipment_cost * salvage_pct
> book_value = equipment_cost - sum(depreciation)
> tax_on_salvage = max(salvage_value - book_value, 0) * tax_rate
> after_tax_salvage = salvage_value - tax_on_salvage
> total_nwc_recovery = nwc_balance[-1]  # Entire cumulative NWC
> terminal_cf = after_tax_salvage + total_nwc_recovery
> 
> # Construct cash flow array
> cash_flows = [-(equipment_cost + initial_nwc)]
> for i in range(len(revenues)):
>     if i < len(revenues) - 1:
>         nwc_investment = nwc_balance[i+1] - nwc_balance[i]
>         cash_flows.append(ocf[i] - nwc_investment)
>     else:
>         cash_flows.append(ocf[i] + terminal_cf)
> 
> # Calculate IRR
> irr = npf.irr(cash_flows)
> irr
> ```

## Pattern: External Financing Needed (EFN) with Pro-Forma Projections

**Description:** External Financing Needed (EFN) calculates the additional external capital required when projected asset growth exceeds internally generated funds. This requires constructing pro-forma financial statements where assets and costs scale proportionally with sales, while debt and equity require separate analysis. EFN = Increase in Assets - Addition to Retained Earnings - Spontaneous Liability Increases.

**When to Use:** 
- Questions explicitly asking for "external financing needed" or "EFN"
- Pro-forma balance sheet projections with sales growth
- Questions about financing gaps or additional capital requirements
- Scenarios stating "assets and costs are proportional to sales" with projected sales figures

**When NOT to Use:**
- Historical cash flow analysis (use Multi-Component Cash Flow Assembly pattern)
- Project IRR/NPV calculations (use Project Cash Flow pattern)
- Questions asking for "cash flow from assets" or similar cash flow identities

**Procedure:**
1. **Identify proportional relationships:** Determine which items scale with sales (typically assets, costs) and which don't (typically debt, equity unless stated)
2. **Calculate sales growth rate:** (Projected Sales - Current Sales) / Current Sales
3. **Project assets:** New Assets = Current Assets × (1 + Sales Growth Rate)
4. **Calculate increase in assets:** Projected Assets - Current Assets
5. **Project income statement:**
   - New Costs = Current Costs × (1 + Sales Growth Rate)
   - New Net Income = Projected Sales - Projected Costs
6. **Calculate addition to retained earnings:**
   - Retention Ratio = 1 - Dividend Payout Ratio
   - Addition to RE = Projected Net Income × Retention Ratio
7. **Calculate spontaneous liability increases:** If current liabilities are proportional to sales, calculate their increase
8. **Compute EFN:** Increase in Assets - Addition to RE - Spontaneous Liability Increases

**Common Mistakes to Avoid:**
- Confusing EFN with cash flow from assets (different frameworks entirely)
- Scaling net income by sales growth without recalculating from projected sales and costs
- Forgetting that "no dividends" means retention ratio = 1.0 (all earnings retained)
- Not recognizing when liabilities are proportional vs. fixed
- Using cash flow identities (OCF, NCS, NWC changes) instead of pro-forma balance sheet approach
- Applying depreciation adjustments when the problem doesn't mention fixed assets or depreciation

**Example (sanitized):**
> **Scenario:** A company has current sales of $12,000, assets of $25,000, costs of $9,500, and equity of $14,000. Assets and costs are proportional to sales. No dividends are paid. Next year's sales are projected to be $13,800. What is the external financing needed?
> 
> **Wrong approach:** Using cash flow from assets framework
> ```python
> # This is WRONG for EFN questions
> operating_cash_flow = net_income + depreciation - taxes
> efn = operating_cash_flow - capital_spending - change_in_nwc  # Incorrect framework
> ```
>
> **Correct approach:** Pro-forma balance sheet with proportional scaling
> ```python
> # Current financial data
> current_sales = 12000
> current_assets = 25000
> current_costs = 9500
> current_net_income = current_sales - current_costs  # 2,500
> current_equity = 14000
> 
> # Projected sales
> projected_sales = 13800
> 
> # Calculate sales growth rate
> sales_growth = (projected_sales - current_sales) / current_sales
> 
> # Project new assets (proportional to sales)
> projected_assets = current_assets * (1 + sales_growth)
> increase_in_assets = projected_assets - current_assets
> 
> # Project new costs (proportional to sales)
> projected_costs = current_costs * (1 + sales_growth)
> 
> # Calculate projected net income
> projected_net_income = projected_sales - projected_costs
> 
> # Calculate payout ratio (no dividends, so 0)
> payout_ratio = 0
> retention_ratio = 1 - payout_ratio
> 
> # Addition to retained earnings
> addition_to_re = projected_net_income * retention_ratio
> 
> # External financing needed (assuming no spontaneous liability changes)
> efn = increase_in_assets - addition_to_re
> 
> efn
> ```
>
> **Key insight:** EFN focuses on the financing gap between asset growth and internal equity generation, not on cash flow identities. The correct approach projects both sides of the balance sheet and identifies the shortfall.