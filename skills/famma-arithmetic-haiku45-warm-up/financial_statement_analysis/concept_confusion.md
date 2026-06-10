# FINANCIAL STATEMENT ANALYSIS: CONCEPT CONFUSION PATTERNS (PoT)

## Pattern: Ambiguous_Ratio_Terminology_Resolution

**Description:** Financial ratios like "Return on Sales" have multiple valid definitions (net profit margin vs. operating profit margin). Code must systematically test both interpretations against answer options when ambiguity exists.

**When to Use:** Questions asking for "return on sales," "profit margin," or other ratios with multiple standard definitions; when initial calculation doesn't match provided options.

**Procedure:**
1. Formula (Primary): Return on Sales = Net Income / Sales
2. Formula (Alternative): Return on Sales = Operating Profit / Sales
3. Calculate primary interpretation first (net income based)
4. If result doesn't match options within rounding tolerance (±0.5%), calculate alternative interpretation
5. Document which interpretation was used in comments
6. Return the value that matches options, with clear labeling

**Code Example:**

**Scenario:** Company has Sales=$5,000,000, Operating Profit=$900,000, Net Income=$450,000. Calculate return on sales.

**Correct Code:**
```python
# Financial data
sales = 5_000_000
operating_profit = 900_000
net_income = 450_000

# Primary interpretation: Net Profit Margin
ros_net = net_income / sales  # 0.09 or 9%

# Alternative interpretation: Operating Profit Margin
ros_operating = operating_profit / sales  # 0.18 or 18%

# In practice, check which matches answer options
# For this example, if options are around 18%, use operating profit
return_on_sales = ros_operating

return_on_sales
```

**Common Bugs to Avoid:**
- Assuming only one definition exists without checking alternatives
- Using print() instead of returning expression
- Not documenting which interpretation was selected
- Failing to convert to percentage when options are in percentage format

---

## Pattern: Average_vs_Ending_Balance_Selection

**Description:** Financial ratios use different balance sheet conventions: some require ending balances, others require averages of beginning and ending. The choice depends on the specific ratio and context, not a universal rule.

**When to Use:** Questions involving turnover ratios (inventory, receivables, payables), return ratios (ROE, ROA), or any ratio mixing income statement (period) with balance sheet (point-in-time) items.

**Procedure:**
1. Formula (General): Ratio = Income Statement Item / Balance Sheet Item
2. Identify if ratio is a "turnover" or "return" metric
3. For collection period/days calculations: Use ending balance unless "average" is explicitly stated
4. For ROE/ROA: Default to ending equity/assets (standard practice)
5. For turnover ratios: Average is more common but verify against options
6. Calculate both if uncertain, select based on option matching

**Code Example:**

**Scenario:** Calculate accounts receivable collection period. Sales=$3,650,000, AR beginning=$400,000, AR ending=$500,000.

**Correct Code:**
```python
# Financial data
sales = 3_650_000
ar_beginning = 400_000
ar_ending = 500_000
days_in_year = 365

# Method 1: Using ending AR (standard for collection period)
collection_period_ending = (ar_ending / sales) * days_in_year

# Method 2: Using average AR (alternative approach)
ar_average = (ar_beginning + ar_ending) / 2
collection_period_average = (ar_average / sales) * days_in_year

# Standard approach uses ending balance
collection_period = collection_period_ending  # 50 days

collection_period
```

**Common Bugs to Avoid:**
- Always averaging when it's not appropriate (e.g., collection period typically uses ending AR)
- Using beginning balance instead of ending balance
- Not considering that textbook conventions may differ from practice
- Failing to test both methods when answer doesn't match options

---

## Pattern: Accounts_Receivable_Aging_Backward_Calculation

**Description:** When given uncollected AR balances representing specific collection percentages, must work backwards to find original sales, then forward to find specific period collections. Cannot directly apply collection percentages to uncollected balances.

**When to Use:** Cash collection budgets where prior period uncollected balances are given; questions involving collection schedules with multiple time periods.

**Procedure:**
1. Formula: Original Sales = Uncollected Balance / (Sum of Uncollected Percentages)
2. Identify what percentage the uncollected balance represents (100% - already collected %)
3. Divide uncollected balance by this percentage to get original sales
4. Multiply original sales by the target period's collection percentage
5. Sum collections from all relevant periods

**Code Example:**

**Scenario:** December sales collection: 60% in December, 25% in January, 15% in February. Uncollected at end of January = $70,000. Find February collections from December sales.

**Correct Code:**
```python
# Collection schedule
collect_month_0 = 0.60  # Same month
collect_month_1 = 0.25  # Next month
collect_month_2 = 0.15  # Two months later

# Given: Uncollected balance at end of January
uncollected_end_jan = 70_000

# This represents only the 15% to be collected in February
# (60% + 25% already collected = 85% collected)
uncollected_percentage = collect_month_2  # 0.15

# Work backwards to find original December sales
december_sales = uncollected_end_jan / uncollected_percentage

# February collection from December sales
february_collection_from_dec = december_sales * collect_month_2

# Verify: should equal uncollected_end_jan
february_collection_from_dec  # $70,000
```

**Common Bugs to Avoid:**
- Multiplying uncollected balance by collection percentage (double-counting error)
- Treating uncollected balance as original sales
- Not recognizing that uncollected balance already represents a specific percentage
- Forgetting to sum collections from multiple months for total period collections

---

## Pattern: Lockbox_PV_Capitalization_vs_Daily_Benefit

**Description:** Lockbox system PV represents the capitalized value of accelerated cash flows (one-time benefit of having cash sooner) minus the PV of perpetual costs, not a single day's net benefit. Must use perpetuity formula for ongoing costs.

**When to Use:** Questions about lockbox systems, cash management systems, or any investment that accelerates cash collection with ongoing transaction costs.

**Procedure:**
1. Formula: PV = (Daily Payments × Days Saved) - (Daily Cost / Daily Interest Rate)
2. Calculate total daily payment volume (number of payments × average payment)
3. Calculate one-time value of accelerated cash: Daily volume × days saved
4. Calculate PV of perpetual daily costs: Daily cost / daily interest rate
5. Net PV = Accelerated cash value - PV of costs
6. Do NOT calculate daily net benefit and stop there

**Code Example:**

**Scenario:** Lockbox system: 300 payments/day at $1,200 each, saves 2 days, costs $0.40/transaction, daily rate 0.03%.

**Correct Code:**
```python
# System parameters
payments_per_day = 300
avg_payment = 1_200
days_saved = 2
cost_per_transaction = 0.40
daily_rate = 0.0003  # 0.03% as decimal

# Step 1: Daily payment volume
daily_volume = payments_per_day * avg_payment

# Step 2: One-time value of accelerated cash
# Having cash 2 days earlier = 2 days of daily volume available now
accelerated_cash_value = daily_volume * days_saved

# Step 3: Daily cost of system
daily_cost = payments_per_day * cost_per_transaction

# Step 4: PV of perpetual daily costs (perpetuity formula)
pv_of_costs = daily_cost / daily_rate

# Step 5: Net PV of adopting system
pv_lockbox = accelerated_cash_value - pv_of_costs

pv_lockbox  # $320,000
```

**Common Bugs to Avoid:**
- Calculating only daily net benefit instead of capitalizing the value
- Forgetting to use perpetuity formula (Cost / Rate) for ongoing costs
- Multiplying accelerated cash by interest rate (it's already a present value)
- Treating this as an NPV problem requiring discounting future flows

---

## Pattern: Cash_Change_Source_Use_Inversion

**Description:** In sources-and-uses cash flow analysis, a decrease in cash is a SOURCE (cash was released to fund activities), and an increase in cash is a USE (cash absorbed funds). This is counterintuitive but follows the accounting identity that cash is the balancing item.

**When to Use:** Cash flow statement preparation from balance sheets; sources and uses of funds analysis; any question asking whether cash change is a source or use.

**Procedure:**
1. Formula: Cash Change = Ending Cash - Beginning Cash
2. Calculate the change in cash (can be positive or negative)
3. Apply inversion rule: Negative change (decrease) = SOURCE; Positive change (increase) = USE
4. The amount is always the absolute value of the change
5. Remember: We're analyzing what cash DID (funded activities) not what happened TO cash

**Code Example:**

**Scenario:** Cash decreased from $120,000 to $95,000. Classify as source or use.

**Correct Code:**
```python
# Balance sheet data
cash_beginning = 120_000
cash_ending = 95_000

# Calculate change in cash
cash_change = cash_ending - cash_beginning  # -25,000

# Apply source/use classification
# CRITICAL: Decrease in cash = SOURCE (cash released to fund activities)
# Increase in cash = USE (cash absorbed/stored)
if cash_change < 0:
    classification = "Source"
    amount = abs(cash_change)
else:
    classification = "Use"
    amount = cash_change

# Result: Source, $25,000
result = (classification, amount)
result
```

**Common Bugs to Avoid:**
- Using intuitive logic (decrease = use) instead of accounting logic
- Treating cash like other balance sheet items (where decrease = use is correct)
- Forgetting that cash is the dependent variable in the accounting equation
- Not taking absolute value for the amount (reporting negative numbers)

---

## Pattern: Multi_Interpretation_Ratio_Systematic_Testing

**Description:** When a calculated ratio doesn't match any provided option, systematically test alternative numerators/denominators that are contextually valid before concluding an error exists. Document each attempt.

**When to Use:** Any ratio calculation where initial result doesn't match options; questions with ambiguous terminology; standardized test questions with specific expected interpretations.

**Procedure:**
1. Calculate primary/standard interpretation first
2. If no match within ±2% of any option, identify alternative valid interpretations
3. Test alternatives in order of likelihood (operating vs net, ending vs average, etc.)
4. Document each calculation with clear comments
5. Select the interpretation that matches options
6. If still no match, verify data extraction from context

**Code Example:**

**Scenario:** Calculate "profit margin." Sales=$2,000,000, Gross Profit=$800,000, Operating Profit=$500,000, Net Income=$300,000. Options: [15%, 25%, 40%].

**Correct Code:**
```python
# Income statement data
sales = 2_000_000
gross_profit = 800_000
operating_profit = 500_000
net_income = 300_000

# Test 1: Net profit margin (most common interpretation)
net_margin = (net_income / sales) * 100  # 15%

# Test 2: Operating profit margin
operating_margin = (operating_profit / sales) * 100  # 25%

# Test 3: Gross profit margin
gross_margin = (gross_profit / sales) * 100  # 40%

# Compare to options: [15%, 25%, 40%]
# All match! Context determines which is correct.
# If question says "profit margin" without qualifier, default to net margin

profit_margin = net_margin  # 15%

profit_margin
```

**Common Bugs to Avoid:**
- Giving up after first calculation doesn't match
- Not considering that "profit" can mean gross, operating, or net
- Failing to test percentage vs. decimal format
- Not documenting which interpretation was ultimately used

---

## Pattern: Return_On_Equity_Balance_Convention

**Description:** ROE calculation typically uses ending shareholders' equity in standard finance practice, not average equity. Average equity is used in more advanced analysis but not in basic ratio calculations or standardized tests.

**When to Use:** Questions asking for Return on Equity (ROE), Return on Assets (ROA), or similar return ratios; when both beginning and ending balance sheet data are provided.

**Procedure:**
1. Formula: ROE = Net Income / Ending Shareholders' Equity
2. Calculate ending equity: Total Assets - Total Liabilities (ending period)
3. Extract net income from income statement
4. Divide net income by ending equity
5. Convert to percentage if needed
6. Only use average equity if explicitly instructed or if ending-based result doesn't match options

**Code Example:**

**Scenario:** Net Income=$180,000. Total Assets: Beginning=$1,500,000, Ending=$1,800,000. Total Liabilities: Beginning=$900,000, Ending=$1,000,000. Calculate ROE.

**Correct Code:**
```python
# Income statement
net_income = 180_000

# Balance sheet data
total_assets_beginning = 1_500_000
total_assets_ending = 1_800_000
total_liabilities_beginning = 900_000
total_liabilities_ending = 1_000_000

# Calculate ending shareholders' equity
equity_ending = total_assets_ending - total_liabilities_ending

# Standard ROE calculation (using ending equity)
roe = (net_income / equity_ending) * 100

# Alternative (if needed): using average equity
equity_beginning = total_assets_beginning - total_liabilities_beginning
equity_average = (equity_beginning + equity_ending) / 2
roe_average = (net_income / equity_average) * 100

# Use ending equity by default
return_on_equity = roe  # 22.5%

return_on_equity
```

**Common Bugs to Avoid:**
- Automatically averaging equity without checking if it's appropriate
- Using beginning equity instead of ending equity
- Confusing equity with assets in the denominator
- Not extracting equity correctly from balance sheet (Assets - Liabilities)

---

## Pattern: Collection_Period_Direct_vs_Turnover_Method

**Description:** Average collection period can be calculated two ways: (AR / Sales) × 365 (direct) or 365 / AR Turnover (indirect). Both should yield the same result, but the direct method is more straightforward and less prone to rounding errors.

**When to Use:** Questions asking for "average collection period," "days sales outstanding," or "receivables collection period"; any AR efficiency metric.

**Procedure:**
1. Formula (Direct): Collection Period = (Accounts Receivable / Annual Sales) × 365
2. Formula (Indirect): Collection Period = 365 / (Sales / Accounts Receivable)
3. Use direct method as primary approach
4. Identify which AR balance to use (ending vs. average based on context)
5. Ensure sales figure is annual (multiply if given monthly/quarterly)
6. Return result rounded to appropriate decimal places

**Code Example:**

**Scenario:** Annual Sales=$7,300,000, Ending AR=$600,000. Calculate average collection period.

**Correct Code:**
```python
# Financial data
annual_sales = 7_300_000
accounts_receivable_ending = 600_000
days_in_year = 365

# Method 1: Direct calculation (preferred)
collection_period_direct = (accounts_receivable_ending / annual_sales) * days_in_year

# Method 2: Indirect (via turnover ratio)
ar_turnover = annual_sales / accounts_receivable_ending
collection_period_indirect = days_in_year / ar_turnover

# Both methods yield same result: 30 days
# Use direct method for clarity
average_collection_period = collection_period_direct

average_collection_period
```

**Common Bugs to Avoid:**
- Using monthly/quarterly sales without annualizing
- Confusing AR turnover with collection period
- Rounding turnover ratio before calculating days (compounds error)
- Using 360 days when question context suggests 365

---

## Pattern: Operating_vs_Net_Profit_Context_Clues

**Description:** When "return on sales" or "profit margin" is ambiguous, use context clues: if answer options cluster around operating profit margin values, that's the expected interpretation; if around net margin values, use net income.

**When to Use:** Any profitability ratio question with ambiguous terminology; when standard calculation doesn't match options but alternative does.

**Procedure:**
1. Calculate both net profit margin and operating profit margin
2. Compare both results to answer option ranges
3. Select the interpretation where calculated value falls within option range
4. If both match different options, default to net profit margin unless context suggests otherwise
5. Document the interpretation used in comments

**Code Example:**

**Scenario:** Sales=$6,000,000, Operating Profit=$1,200,000, Net Income=$720,000. Question asks for "return on sales." Options: [10%, 12%, 18%, 20%].

**Correct Code:**
```python
# Income statement
sales = 6_000_000
operating_profit = 1_200_000
net_income = 720_000

# Calculate both interpretations
net_profit_margin = (net_income / sales) * 100  # 12%
operating_profit_margin = (operating_profit / sales) * 100  # 20%

# Check against options: [10%, 12%, 18%, 20%]
# Both 12% and 20% are in options
# Net margin (12%) is standard interpretation of "return on sales"
# But if question context emphasizes operations, use 20%

# Default to net profit margin
return_on_sales = net_profit_margin  # 12%

return_on_sales
```

**Common Bugs to Avoid:**
- Not calculating both alternatives when ambiguity exists
- Ignoring answer options as context clues
- Assuming one definition is always correct across all contexts
- Not recognizing that terminology varies by textbook/institution