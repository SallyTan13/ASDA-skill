# SKILL PATTERNS: Financial Statement Analysis - Unit/Currency/Percent Conversion Errors (PoT)

## Pattern: Average Balance Calculation for Period Ratios

**Description:** Financial ratios measuring activity over a period (like collection period, inventory turnover, asset turnover, ROE) require averaging balance sheet accounts (beginning + ending / 2) rather than using only ending balances, since income statement items span the entire period while balance sheet items are point-in-time snapshots.

**When to Use:** When calculating turnover ratios, collection periods, payment periods, ROE, ROA, **asset turnover**, or any ratio combining income statement (period) data with balance sheet (point-in-time) data. Keywords: "average collection period," "days sales outstanding," "inventory turnover," "return on equity," "return on assets," "asset turnover," "calculate the ratio," "what is the [metric]."

**When NOT to Use:** 
- **Budgeting/forecasting problems**: When solving for unknown sales, purchases, or production amounts given collection patterns or payment schedules (these require reverse calculations, not ratio analysis)
- **Cash flow projections**: When calculating expected cash collections or payments from sales/purchases
- **Accounts receivable aging**: When working backward from uncollected amounts to determine original sales
- **Problems asking "compute sales" or "find purchases"**: These are typically budgeting problems, not ratio analysis
- **Stock transaction problems**: When calculating the value or effects of stock dividends, splits, or issuances (these are not ratio calculations)

**Procedure:**
1. **Verify this is a ratio calculation problem**: Confirm you're calculating a known metric (DSO, inventory turnover, asset turnover, etc.), not solving for an unknown transaction amount
2. **Identify the ratio type**: Determine which balance sheet account(s) and income statement item(s) are involved
3. **Check for both period values**: Verify that both beginning-of-period and end-of-period balance sheet values are available
4. Extract both beginning-of-period and end-of-period balance sheet values
5. Calculate the average: `(beginning_value + ending_value) / 2`
6. Apply the ratio formula using the averaged balance sheet value
7. Verify units: days for collection period, times for turnover ratios, percentage for ROE/ROA

**Common Mistakes to Avoid:**
- Using only ending balance instead of average: `(ending_ar / sales) * 365` gives wrong result
- **Using only ending assets for asset turnover**: `sales / ending_assets` ignores the period nature of sales
- Forgetting to divide by 2 when averaging: `(beginning_ar + ending_ar)` gives wrong result
- Using 360 days instead of 365 when problem context doesn't specify
- Printing result instead of returning expression in PoT mode
- **Misapplying to budgeting problems**: Don't use this pattern when the problem asks you to "compute sales" or "find the amount" - those require solving equations, not calculating ratios
- **Misapplying to stock transactions**: Don't use averaging for stock dividend/split calculations

**Code Example:**

**Scenario:** Calculate asset turnover ratio given Sales = $8,000,000, Beginning Total Assets = $5,500,000, Ending Total Assets = $6,440,000

**Correct Code:**
```python
# Income statement data
sales = 8_000_000

# Balance sheet data
beginning_total_assets = 5_500_000
ending_total_assets = 6_440_000

# Step 1: Calculate average total assets
average_total_assets = (beginning_total_assets + ending_total_assets) / 2

# Step 2: Calculate asset turnover ratio
asset_turnover_ratio = sales / average_total_assets

# Round to 2 decimal places for answer matching
asset_turnover_ratio = round(asset_turnover_ratio, 2)

# Result (must be expression, not print)
asset_turnover_ratio  # Returns 1.34
```

**Wrong Approach Example:**
```python
# WRONG: Using only ending assets
sales = 8_000_000
ending_total_assets = 6_440_000
asset_turnover_ratio = sales / ending_total_assets  # Returns 1.24 - INCORRECT
```

---
## Pattern: Return on Equity with Average Equity Base

**Description:** ROE calculation convention requires using average equity (beginning + ending / 2) as the denominator when both period-start and period-end equity values are available, since net income is earned throughout the period.

**When to Use:** When calculating return on equity (ROE), return on assets (ROA), or similar profitability ratios where net income or operating income is divided by a balance sheet equity or asset base. Keywords: "return on equity," "ROE," "return on assets," "ROA."

**Procedure:**
1. Formula: `ROE = Net Income / Average Equity × 100%` where `Average Equity = (Beginning Equity + Ending Equity) / 2`
2. Extract net income from income statement
3. Calculate beginning equity: `Beginning Common Stock + Beginning Retained Earnings`
4. Calculate ending equity: `Ending Common Stock + Ending Retained Earnings`
5. Compute average equity: `(beginning_equity + ending_equity) / 2`
6. Calculate ROE as percentage: `(net_income / average_equity) * 100`

**Code Example:**

**Scenario:** Calculate ROE given Net Income = $450,000, Beginning Equity (CS $200,000 + RE $1,800,000), Ending Equity (CS $200,000 + RE $2,300,000)

**Correct Code:**
```python
# Income statement data
net_income = 450_000

# Balance sheet data - beginning of period
beginning_common_stock = 200_000
beginning_retained_earnings = 1_800_000
beginning_equity = beginning_common_stock + beginning_retained_earnings

# Balance sheet data - end of period
ending_common_stock = 200_000
ending_retained_earnings = 2_300_000
ending_equity = ending_common_stock + ending_retained_earnings

# Calculate average equity
average_equity = (beginning_equity + ending_equity) / 2

# Calculate ROE as percentage
roe_percent = (net_income / average_equity) * 100

# Result
roe_percent  # Returns 20.45%
```

**Common Bugs to Avoid:**
- Using ending equity only: `(450_000 / 2_500_000) * 100` gives 18.0% (WRONG)
- Using beginning equity only: `(450_000 / 2_000_000) * 100` gives 22.5% (WRONG)
- Forgetting to multiply by 100 for percentage: returns 0.2045 instead of 20.45%
- Arithmetic errors in division: ensure proper float division, not integer division
- Missing equity components: forgetting to add common stock and retained earnings

---

## Pattern: Days Formula Standardization

**Description:** Activity ratios expressed in days (collection period, inventory days, payables period) must use consistent day counts (365 vs 360) and proper formula structure: either `(Balance / Annual_Flow) × Days` or `Balance / (Annual_Flow / Days)`.

**When to Use:** When calculating any "days" metric: days sales outstanding (DSO), days inventory outstanding (DIO), days payables outstanding (DPO), cash conversion cycle. Keywords: "collection period," "days," "turnover in days."

**Procedure:**
1. Formula options: `Days = (Average Balance / Annual Flow) × 365` OR `Days = Average Balance / (Annual Flow / 365)`
2. Determine the appropriate balance sheet account (AR, Inventory, AP)
3. Calculate average balance if both beginning and ending available
4. Identify the corresponding annual flow (Sales for AR, COGS for Inventory, Purchases/COGS for AP)
5. Use 365 days unless problem explicitly specifies 360
6. Verify result is reasonable (typically 0-120 days for most metrics)

**Code Example:**

**Scenario:** Calculate days inventory outstanding given Beginning Inventory = $800,000, Ending Inventory = $1,000,000, COGS = $3,600,000

**Correct Code:**
```python
# Balance sheet data
beginning_inventory = 800_000
ending_inventory = 1_000_000

# Income statement data
cogs = 3_600_000

# Calculate average inventory
average_inventory = (beginning_inventory + ending_inventory) / 2

# Method 1: Direct calculation
days_inventory_outstanding_v1 = (average_inventory / cogs) * 365

# Method 2: Using daily COGS (equivalent)
daily_cogs = cogs / 365
days_inventory_outstanding_v2 = average_inventory / daily_cogs

# Both methods yield same result
days_inventory_outstanding_v1  # Returns 91.25 days
```

**Common Bugs to Avoid:**
- Using Sales instead of COGS for inventory calculations
- Mixing 360 and 365 days inconsistently across related metrics
- Wrong formula structure: `(annual_flow / average_balance) * 365` inverts the ratio
- Not averaging when both beginning and ending balances are provided
- Using ending balance when calculating multi-year averages

---

## Pattern: Percentage Conversion and Rounding

**Description:** Financial ratios must be converted to percentages correctly (multiply by 100) and rounded appropriately to match answer choices, while avoiding premature rounding that compounds errors.

**When to Use:** When calculating any ratio expressed as a percentage: profit margins, returns (ROE, ROA, ROI), growth rates, efficiency ratios. Keywords: "percent," "percentage," "%," "ratio."

**Procedure:**
1. Perform all intermediate calculations in decimal form (not percentage)
2. Complete the full calculation before any rounding
3. Convert to percentage by multiplying by 100 at the final step
4. Round to match the precision of answer options (typically 2 decimal places)
5. Verify the result magnitude is reasonable for the metric type

**Code Example:**

**Scenario:** Calculate gross profit margin given Sales = $12,500,000, COGS = $7,800,000

**Correct Code:**
```python
# Income statement data
sales = 12_500_000
cogs = 7_800_000

# Calculate gross profit
gross_profit = sales - cogs

# Calculate margin as decimal first
gross_profit_margin_decimal = gross_profit / sales

# Convert to percentage
gross_profit_margin_percent = gross_profit_margin_decimal * 100

# Round to 2 decimal places for answer matching
gross_profit_margin_percent = round(gross_profit_margin_percent, 2)

# Result
gross_profit_margin_percent  # Returns 37.6%
```

**Common Bugs to Avoid:**
- Forgetting to multiply by 100: returns 0.376 instead of 37.6%
- Premature rounding: rounding intermediate steps compounds errors
- Wrong rounding direction when between answer choices
- Returning print() statement instead of expression value in PoT
- Inconsistent decimal places across related calculations

---

## Pattern: Balance Sheet Account Aggregation

**Description:** Equity, assets, and liabilities often require summing multiple line items from balance sheets for use in financial ratio analysis. This pattern applies when calculating aggregate balances from existing accounts, NOT when accounting for new equity transactions like stock dividends or splits.

**When to Use:** When calculating total equity, total assets, total current assets, working capital, or any aggregate balance sheet metric **for use in financial ratio analysis**. Keywords: "total equity," "shareholders' equity," "total assets," "working capital," "calculate ROE," "calculate ROA," "debt-to-equity ratio."

**When NOT to Use:**
- **Stock dividend/split problems**: When the problem involves issuing new shares through stock dividends or splits (these require transaction accounting at market value, not simple aggregation)
- **Equity transaction problems**: When calculating the effect of stock issuances, repurchases, or dividends on equity accounts
- **Problems asking "what is the value of new stock"**: These require understanding stock transaction accounting at market value (shares × market price), not par value aggregation
- **Corporate finance transactions**: When dealing with changes to equity structure rather than measuring existing balances
- **Questions about "effects on equity accounts" or "distribution" of stock dividends**: These involve recording transactions, not summing existing balances

**Procedure:**
1. **Verify this is a balance sheet aggregation problem**: Confirm you're summing existing account balances for ratio analysis, not accounting for new transactions
2. **Check for transaction keywords**: If the problem mentions "declared," "issued," "distribution," "effects on accounts," or "value of new stock," this pattern does NOT apply
3. Identify all components of the target aggregate (e.g., equity = common stock + retained earnings + other equity accounts)
4. Extract each component value, handling OCR errors or formatting issues
5. Sum all components: `total = component1 + component2 + ...`
6. Verify against provided totals if available as a sanity check
7. Use the aggregated value in subsequent ratio calculations

**Common Mistakes to Avoid:**
- Missing equity components (e.g., forgetting preferred stock or AOCI)
- Wrong sign for treasury stock (should be negative/contra-equity)
- Using liabilities values instead of equity values due to OCR misalignment
- Not verifying against provided "Total Equity" line when available
- Confusing "Total Liabilities & Equity" with "Total Equity"
- **Misapplying to transaction accounting**: Don't use simple aggregation when the problem involves recording stock dividends, splits, or other equity transactions that require market value calculations
- **Confusing par value with market value**: In stock dividend problems, the "value" typically refers to market value (shares × market price), not par value aggregation

**Code Example:**

**Scenario:** Calculate total equity for ROE analysis given Common Stock = $500,000, Preferred Stock = $250,000, Retained Earnings = $3,200,000, Treasury Stock = -$150,000

**Correct Code:**
```python
# Equity components from balance sheet
common_stock = 500_000
preferred_stock = 250_000
retained_earnings = 3_200_000
treasury_stock = -150_000  # Note: treasury stock is negative

# Calculate total equity
total_equity = common_stock + preferred_stock + retained_earnings + treasury_stock

# Sanity check: equity should be positive for healthy company
assert total_equity > 0, "Total equity is negative - check values"

# Result
total_equity  # Returns 3,800,000
```

---

## Pattern: Stock Dividend Market Value Calculation

**Description:** Stock dividends must be recorded at market value, not par value. When a company declares a stock dividend, the value transferred from retained earnings to equity accounts equals the number of new shares issued multiplied by the market price per share, not the par value.

**When to Use:** When calculating the value of stock dividends, effects of stock dividends on equity accounts, or amounts to be recorded for stock dividend distributions. Keywords: "stock dividend," "declared a stock dividend," "value of new common stock," "effects on equity accounts," "distribution of stock dividend."

**When NOT to Use:**
- **Financial ratio calculations**: When computing ROE, ROA, or other performance metrics using existing equity balances
- **Balance sheet aggregation**: When simply summing existing equity account balances
- **Stock splits**: Stock splits are recorded differently (no value transfer, only par value adjustment)
- **Cash dividends**: Cash dividends reduce retained earnings by the cash amount, not market value

**Procedure:**
1. **Identify the stock dividend percentage**: Extract the dividend rate (e.g., 15%, 10%)
2. **Calculate existing shares**: Determine current shares outstanding from common stock balance and par value: `existing_shares = common_stock_balance / par_value_per_share`
3. **Calculate new shares issued**: `new_shares = existing_shares × dividend_rate`
4. **Use market price for valuation**: `value_of_stock_dividend = new_shares × market_price_per_share`
5. **Verify accounting entries**: 
   - Debit Retained Earnings: value_of_stock_dividend
   - Credit Common Stock: new_shares × par_value
   - Credit Capital Surplus: value_of_stock_dividend - (new_shares × par_value)

**Common Mistakes to Avoid:**
- **Using par value instead of market value**: `new_shares × par_value` gives the common stock increase, NOT the total value of the dividend
- **Confusing stock dividend value with common stock increase**: The "value" is the market value; the common stock account only increases by par value
- **Forgetting the capital surplus component**: The difference between market value and par value goes to capital surplus
- **Applying balance sheet aggregation patterns**: Stock dividends require transaction accounting, not simple summation

**Code Example:**

**Scenario:** Calculate the value of a 15% stock dividend when market price is $60 per share, existing common stock is $500,000 at $1 par value

**Correct Code:**
```python
# Given data
common_stock_balance = 500_000
par_value_per_share = 1
stock_dividend_rate = 0.15  # 15%
market_price_per_share = 60

# Step 1: Calculate existing shares
existing_shares = common_stock_balance / par_value_per_share

# Step 2: Calculate new shares issued
new_shares = existing_shares * stock_dividend_rate

# Step 3: Calculate value at MARKET PRICE (not par value)
value_of_stock_dividend = new_shares * market_price_per_share

# Result
value_of_stock_dividend  # Returns 4,500,000

# Accounting breakdown (for verification):
common_stock_increase = new_shares * par_value_per_share  # 75,000
capital_surplus_increase = value_of_stock_dividend - common_stock_increase  # 4,425,000
retained_earnings_decrease = value_of_stock_dividend  # 4,500,000
```

**Wrong Approach:**
```python
# WRONG: Using par value instead of market value
new_shares = 75_000
value_of_stock_dividend = new_shares * par_value_per_share  # Returns 75,000 - INCORRECT
# This only gives the common stock increase, not the total dividend value
```