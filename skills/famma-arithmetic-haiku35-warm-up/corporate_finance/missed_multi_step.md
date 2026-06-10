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

**Description:** Cash flow from assets requires reconciling balance sheet changes in net fixed assets with income statement depreciation. The relationship is: Change in NFA = Capital Spending - Depreciation, which must be rearranged to find actual cash spent: Capital Spending = Change in NFA + Depreciation.

**When to Use:** Questions about cash flow from assets, capital expenditures, net capital spending, or reconciling balance sheet and income statement for investment activities.

**Procedure:**
1. Formula: Net Capital Spending = Change in Net Fixed Assets + Depreciation
2. Calculate change in net fixed assets: NFA(end) - NFA(beginning)
3. Extract depreciation from income statement
4. Compute net capital spending: Change in NFA + Depreciation
5. For cash flow from assets, also calculate: Operating Cash Flow - Net Capital Spending - Change in NWC
6. Return the requested metric (capital spending or full cash flow from assets)

**Code Example:**

**Scenario:** A company has NFA of $8,200 (2016) and $7,500 (2015). Depreciation=$950. EBIT=$3,400, tax rate=35%, interest=$280. Current assets increased by $180, current liabilities increased by $95.

**Correct Code:**
```python
# Balance sheet data
nfa_end = 8200
nfa_beginning = 7500
current_assets_change = 180
current_liabilities_change = 95

# Income statement data
ebit = 3400
depreciation = 950
interest_paid = 280
tax_rate = 0.35

# Step 1: Calculate change in net fixed assets
change_in_nfa = nfa_end - nfa_beginning

# Step 2: Calculate net capital spending
# Capital Spending = Change in NFA + Depreciation
# (Depreciation reduces NFA but isn't cash outflow; actual spending is higher)
net_capital_spending = change_in_nfa + depreciation

# Step 3: Calculate operating cash flow
# OCF = EBIT + Depreciation - Taxes
taxes = ebit * tax_rate
operating_cash_flow = ebit + depreciation - taxes

# Step 4: Calculate change in net working capital
change_in_nwc = current_assets_change - current_liabilities_change

# Step 5: Calculate cash flow from assets
# CFFA = OCF - Net Capital Spending - Change in NWC
cash_flow_from_assets = operating_cash_flow - net_capital_spending - change_in_nwc

cash_flow_from_assets
```

**Common Bugs to Avoid:**
- Using only the change in NFA without adding back depreciation (depreciation is non-cash)
- Subtracting depreciation instead of adding it when computing capital spending
- Confusing "capital spending" (cash out) with "change in NFA" (book value change)
- Forgetting that given "purchases" in the question may already be gross capital spending
- Sign errors: capital spending and NWC increases are uses of cash (subtract from OCF)
- Not recognizing the reconciliation identity: Ending NFA = Beginning NFA + Capital Spending - Depreciation

---

## Pattern: Multi-Component Cash Flow Assembly

**Description:** Complete cash flow calculations require assembling multiple independent components (operating, investing, financing) with correct sign conventions. Each component must be calculated separately before final aggregation.

**When to Use:** Questions asking for cash flow from assets, cash flow to creditors, cash flow to stockholders, or statement of cash flows construction.

**Procedure:**
1. Formula: CF from Assets = Operating CF - Net Capital Spending - Change in NWC
2. Calculate operating cash flow: EBIT + Depreciation - Taxes (or NI + Depreciation + Interest)
3. Calculate net capital spending: Change in NFA + Depreciation
4. Calculate change in net working capital: Change in CA - Change in CL
5. Apply correct signs: outflows are negative, inflows are positive
6. Aggregate components according to the specific cash flow identity requested

**Code Example:**

**Scenario:** Calculate cash flow from assets. Sales=$18,500, costs=$7,200, depreciation=$1,400, interest=$420, tax rate=38%. NFA: $6,100(end), $5,300(start). CA: $1,850(end), $1,620(start). CL: $680(end), $590(start).

**Correct Code:**
```python
# Income statement data
sales = 18500
costs = 7200
depreciation = 1400
interest_paid = 420
tax_rate = 0.38

# Balance sheet data
nfa_end = 6100
nfa_start = 5300
current_assets_end = 1850
current_assets_start = 1620
current_liabilities_end = 680
current_liabilities_start = 590

# Step 1: Calculate EBIT
ebit = sales - costs - depreciation

# Step 2: Calculate taxes
taxes = ebit * tax_rate

# Step 3: Calculate operating cash flow
# Method 1: EBIT + Depreciation - Taxes
operating_cash_flow = ebit + depreciation - taxes

# Step 4: Calculate net capital spending
change_in_nfa = nfa_end - nfa_start
net_capital_spending = change_in_nfa + depreciation

# Step 5: Calculate change in net working capital
change_in_ca = current_assets_end - current_assets_start
change_in_cl = current_liabilities_end - current_liabilities_start
change_in_nwc = change_in_ca - change_in_cl

# Step 6: Calculate cash flow from assets
# CFFA = OCF - NCS - Change in NWC
cash_flow_from_assets = operating_cash_flow - net_capital_spending - change_in_nwc

cash_flow_from_assets
```

**Common Bugs to Avoid:**
- Mixing up sign conventions (increases in assets use cash, increases in liabilities provide cash)
- Calculating only one component when the question requires full cash flow from assets
- Using net income without adding back interest for EBIT-based OCF calculation
- Double-counting depreciation (it appears in both OCF and capital spending calculations)
- Forgetting that change in NWC = change in CA - change in CL (not just change in CA)
- Using print() instead of final expression