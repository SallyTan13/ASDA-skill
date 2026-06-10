# SKILL PATTERNS: Financial Statement Analysis - Unit/Currency/Percent Conversion Errors (PoT)

## Pattern: Average Balance Calculation for Period Ratios

**Description:** Financial ratios measuring activity over a period (like collection period, inventory turnover, ROE) require averaging balance sheet accounts (beginning + ending / 2) rather than using only ending balances, since income statement items span the entire period while balance sheet items are point-in-time snapshots.

**When to Use:** When calculating turnover ratios, collection periods, payment periods, ROE, ROA, or any ratio combining income statement (period) data with balance sheet (point-in-time) data. Keywords: "average collection period," "days sales outstanding," "inventory turnover," "return on equity," "return on assets."

**Procedure:**
1. Formula: For collection period: `(Average AR / Sales) × 365` where `Average AR = (Beginning AR + Ending AR) / 2`
2. Identify if the ratio combines period data (income statement) with point-in-time data (balance sheet)
3. Extract both beginning-of-period and end-of-period balance sheet values
4. Calculate the average: `(beginning_value + ending_value) / 2`
5. Apply the ratio formula using the averaged balance sheet value
6. Verify units: days for collection period, percentage for ROE/ROA

**Code Example:**

**Scenario:** Calculate average collection period given Sales = $5,000,000, Beginning AR = $400,000, Ending AR = $600,000

**Correct Code:**
```python
# Financial data
sales = 5_000_000
beginning_ar = 400_000
ending_ar = 600_000

# Step 1: Calculate average accounts receivable
average_ar = (beginning_ar + ending_ar) / 2

# Step 2: Calculate average collection period in days
average_collection_period = (average_ar / sales) * 365

# Result (must be expression, not print)
average_collection_period  # Returns 36.5 days
```

**Common Bugs to Avoid:**
- Using only ending balance instead of average: `(ending_ar / sales) * 365` gives 43.8 days (WRONG)
- Forgetting to divide by 2 when averaging: `(beginning_ar + ending_ar)` gives 73.0 days (WRONG)
- Using 360 days instead of 365 when problem context doesn't specify
- Printing result instead of returning expression in PoT mode

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

**Description:** Equity, assets, and liabilities often require summing multiple line items from balance sheets. Ensure all relevant components are included and correctly identified from OCR text or structured data.

**When to Use:** When calculating total equity, total assets, total current assets, working capital, or any aggregate balance sheet metric. Keywords: "total equity," "shareholders' equity," "total assets," "working capital."

**Procedure:**
1. Identify all components of the target aggregate (e.g., equity = common stock + retained earnings + other equity accounts)
2. Extract each component value, handling OCR errors or formatting issues
3. Sum all components: `total = component1 + component2 + ...`
4. Verify against provided totals if available as a sanity check
5. Use the aggregated value in subsequent ratio calculations

**Code Example:**

**Scenario:** Calculate total equity given Common Stock = $500,000, Preferred Stock = $250,000, Retained Earnings = $3,200,000, Treasury Stock = -$150,000

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

**Common Bugs to Avoid:**
- Missing equity components (e.g., forgetting preferred stock or AOCI)
- Wrong sign for treasury stock (should be negative/contra-equity)
- Using liabilities values instead of equity values due to OCR misalignment
- Not verifying against provided "Total Equity" line when available
- Confusing "Total Liabilities & Equity" with "Total Equity"