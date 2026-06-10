# FINANCIAL STATEMENT ANALYSIS: CONCEPT CONFUSION PATTERNS (PoT)

## Pattern: Ambiguous_Ratio_Terminology_Resolution

**Description:** Financial ratios like "Return on Sales" have multiple valid definitions (net profit margin vs. operating profit margin). Code must systematically test both interpretations against answer options when ambiguity exists. **CRITICAL: The PRIMARY interpretation of "Return on Sales" is Net Income / Sales (Net Profit Margin). Only use Operating Profit / Sales when the net margin calculation doesn't match ANY provided option.**

**When to Use:** Questions asking for "return on sales," "profit margin," or other ratios with multiple standard definitions; when initial calculation doesn't match provided options.

**When NOT to Use:**
- When the question explicitly specifies "net profit margin" or "operating profit margin" (no ambiguity)
- When the primary interpretation (net margin) matches an available option (don't test alternatives)
- When context clearly indicates which interpretation is expected

**Procedure:**
1. **Formula (Primary - ALWAYS TEST FIRST):** Return on Sales = Net Income / Sales
2. Calculate primary interpretation first (net income based)
3. **Check if result matches any option within rounding tolerance (±0.5%)**
4. **ONLY if primary doesn't match ANY option:** Calculate alternative interpretation
5. Formula (Alternative): Return on Sales = Operating Profit / Sales
6. Document which interpretation was used in comments
7. Return the value that matches options, with clear labeling
8. **If BOTH interpretations match different options, default to Net Income / Sales (standard definition)**

**Common Mistakes to Avoid:**
- **Assuming operating profit margin is correct when net profit margin also matches an option**
- **Not testing the primary (net income) interpretation first**
- Testing alternative interpretations when primary already matches an option
- Assuming only one definition exists without checking alternatives
- Using print() instead of returning expression
- Not documenting which interpretation was selected
- Failing to convert to percentage when options are in percentage format

**Example (sanitized):**

**Scenario:** Company has Sales=$5,000,000, Operating Profit=$900,000, Net Income=$450,000. Calculate return on sales. Options: [A. 8.5%, B. 9.0%, C. 18.0%, D. 20.0%]

**Correct Code:**
```python
# Financial data
sales = 5_000_000
operating_profit = 900_000
net_income = 450_000

# PRIMARY interpretation (ALWAYS TEST FIRST): Net Profit Margin
ros_net = (net_income / sales) * 100  # 9.0%

# Check against options: [8.5%, 9.0%, 18.0%, 20.0%]
# Net margin = 9.0% → EXACT MATCH to option B

# Since primary interpretation matches an option, use it
return_on_sales = ros_net

# Match to options
options = {'A': 8.5, 'B': 9.0, 'C': 18.0, 'D': 20.0}
closest = min(options.items(), key=lambda x: abs(x[1] - return_on_sales))
answer = closest[0]  # 'B'
answer
```

**Alternative Scenario:** Sales=$5,000,000, Operating Profit=$900,000, Net Income=$450,000. Options: [A. 15.0%, B. 18.0%, C. 20.0%, D. 22.0%]

```python
# Financial data
sales = 5_000_000
operating_profit = 900_000
net_income = 450_000

# PRIMARY interpretation: Net Profit Margin
ros_net = (net_income / sales) * 100  # 9.0%

# Check against options: [15.0%, 18.0%, 20.0%, 22.0%]
# Net margin = 9.0% → NO MATCH to any option

# ONLY NOW test alternative: Operating Profit Margin
ros_operating = (operating_profit / sales) * 100  # 18.0%

# Operating margin = 18.0% → EXACT MATCH to option B
# Use alternative interpretation since primary didn't match
return_on_sales = ros_operating

options = {'A': 15.0, 'B': 18.0, 'C': 20.0, 'D': 22.0}
closest = min(options.items(), key=lambda x: abs(x[1] - return_on_sales))
answer = closest[0]  # 'B'
answer
```
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

**Description:** When given uncollected AR balances at a specific point in time representing future collection percentages, must work backwards to find original sales by identifying what percentage remains uncollected at that specific time point, then forward to find specific period collections. **CRITICAL: When total AR balance includes collections from multiple months, must decompose the total to isolate each month's contribution. Each decomposed component ALREADY REPRESENTS the actual collection amount for the target period—do not multiply by collection percentage again (this causes double-counting).**

**When to Use:** Cash collection budgets where prior period uncollected balances are given; questions involving collection schedules with multiple time periods; when you need to determine original sales from remaining receivables.

**When NOT to Use:**
- When AR balance is already broken down by originating month (no decomposition needed)
- When the question provides original sales directly and only asks for collections
- When total AR represents only one month's sales (simple division case)

**Procedure:**
1. **Identify if the uncollected AR balance is for a SINGLE month's sales or MULTIPLE months combined**
2. If SINGLE month (e.g., "uncollected December sales = $87,750"):
   - Identify the TIME POINT when measured (e.g., end of January)
   - Determine what percentage HAS BEEN collected by that time point
   - Calculate uncollected percentage: 100% - (sum of percentages already collected)
   - Formula: Original Sales = Uncollected Balance / Uncollected Percentage
   - Multiply original sales by target period's collection percentage to get collections
3. If MULTIPLE months (e.g., "total AR = $122,800 including December and November"):
   - **STOP: Decompose total AR into components by originating month**
   - For each month component, identify what collection period it represents
   - **CRITICAL: Each decomposed component IS the collection amount for that period**
   - **DO NOT multiply the component by collection percentage again—it's already the final amount**
   - Sum all components to get total collections for target period
4. **Validation check:** If you find yourself multiplying an already-decomposed AR component by a percentage, you're double-counting

**Example (sanitized):**
> **Scenario:** A company collects sales as follows: 60% in month of sale, 30% next month, 10% two months later. At end of February, total AR is $95,000, consisting of: $57,000 from February sales and $38,000 from January sales. Calculate March collections.
>
> **Wrong approach:** Multiplying decomposed AR components by collection percentages
> ```python
> # WRONG: Double-counting error
> ar_from_february = 57_000  # This IS the 40% uncollected from February
> ar_from_january = 38_000   # This IS the 10% uncollected from January
> 
> # ERROR: Multiplying by percentages again
> march_from_february = ar_from_february * 0.30  # WRONG! Double-counting
> march_from_january = ar_from_january * 0.10    # WRONG! Double-counting
> total = march_from_february + march_from_january  # Incorrect result
> ```
>
> **Correct approach:** Recognizing decomposed components are final amounts
> ```python
> # Collection schedule
> collect_month_0 = 0.60  # Same month
> collect_month_1 = 0.30  # Next month
> collect_month_2 = 0.10  # Two months later
> 
> # Given: Total AR at end of February (decomposed by month)
> ar_from_february = 57_000  # Uncollected February sales
> ar_from_january = 38_000   # Uncollected January sales
> 
> # Analysis of what each component represents:
> # - $57,000 from February: This is 40% of Feb sales (30% + 10% uncollected)
> #   In March, we collect the 30% portion = need to work backwards
> # - $38,000 from January: This is 10% of Jan sales (final collection)
> #   In March, we collect this entire amount directly
> 
> # For February sales: Work backwards to find original sales
> february_uncollected_pct = collect_month_1 + collect_month_2  # 0.40
> february_sales = ar_from_february / february_uncollected_pct  # 142,500
> march_from_february = february_sales * collect_month_1  # 42,750
> 
> # For January sales: The $38,000 IS the March collection (no multiplication)
> # This represents the final 10% being collected in March
> march_from_january = ar_from_january  # 38,000 (use directly!)
> 
> # Total March collections
> total_march_collections = march_from_february + march_from_january  # 80,750
> ```
> **Key insight:** When AR is decomposed by originating month, ask "What collection period does this component represent?" If it represents the target period's collection, use it directly. Only work backwards and multiply when the component represents multiple future periods combined.

**Common Mistakes to Avoid:**
- **CRITICAL: Multiplying decomposed AR components by collection percentages (double-counting)**
- Not identifying the specific time point when the uncollected balance is measured
- Incorrectly calculating what percentage has already been collected by that time point
- Treating uncollected balance as original sales
- **Not recognizing that decomposed AR components may already be the final collection amounts**
- **Applying percentage multiplication to AR amounts that already represent specific collection periods**
- Forgetting that collections in one month may come from sales in multiple prior months
- Not asking "Does this AR component represent one collection period or multiple?" before deciding whether to multiply
## Pattern: Lockbox_PV_Capitalization_vs_Daily_Benefit

**Description:** Lockbox system PV calculation represents the capitalized value of accelerated cash flows (one-time benefit of having cash sooner). The question context determines whether to include ongoing costs: if asking for "PV of adopting" or "value of acceleration," report only the benefit; if asking for "net PV" or "should we adopt," subtract the PV of perpetual costs.

**When to Use:** Questions about lockbox systems, cash management systems, or any investment that accelerates cash collection; when determining the value of having cash available sooner.

**Procedure:**
1. Calculate daily payment volume: Number of payments × Average payment amount
2. Calculate one-time value of accelerated cash: Daily volume × Days saved
3. Identify what the question asks for:
   - "PV of adopting" / "value of acceleration" / "benefit" → Stop at step 2
   - "Net PV" / "should adopt" / "net benefit" → Continue to steps 4-5
4. If net calculation needed: Calculate daily cost = Payments per day × Cost per transaction
5. If net calculation needed: Calculate PV of perpetual costs = Daily cost / Daily interest rate
6. If net calculation needed: Net PV = Accelerated cash value - PV of costs

**Example (sanitized):**
> **Scenario:** A lockbox system processes 500 payments per day averaging $800 each, accelerates cash availability by 2 days, costs $0.30 per transaction, and the daily interest rate is 0.025%. Calculate (a) the PV of the acceleration benefit, and (b) the net PV of adopting the system.
>
> **Wrong approach:** Confusing benefit value with net value
> ```python
> # WRONG: Always subtracting costs even when asked only for benefit
> daily_volume = 500 * 800  # 400,000
> accelerated_value = 400_000 * 2  # 800,000
> daily_cost = 500 * 0.30  # 150
> pv_costs = 150 / 0.00025  # 600,000
> answer = 800_000 - 600_000  # 200,000 (but question asked for benefit only!)
> ```
>
> **Correct approach:** Matching calculation to question type
> ```python
> # System parameters
> payments_per_day = 500
> avg_payment = 800
> days_saved = 2
> cost_per_transaction = 0.30
> daily_rate = 0.00025  # 0.025% as decimal
> 
> # Step 1: Daily payment volume
> daily_volume = payments_per_day * avg_payment  # 400,000
> 
> # Step 2: One-time value of accelerated cash
> # Having cash 2 days earlier means 2 days of receipts available now
> pv_acceleration_benefit = daily_volume * days_saved  # 800,000
> 
> # Answer to part (a): PV of acceleration benefit
> answer_a = pv_acceleration_benefit  # $800,000
> 
> # Step 3: For net PV calculation (part b)
> daily_cost = payments_per_day * cost_per_transaction  # 150
> 
> # Step 4: PV of perpetual daily costs (perpetuity formula)
> pv_of_perpetual_costs = daily_cost / daily_rate  # 600,000
> 
> # Step 5: Net PV of adopting system
> net_pv = pv_acceleration_benefit - pv_of_perpetual_costs  # 200,000
> 
> # Answer to part (b): Net PV
> answer_b = net_pv  # $200,000
> ```
> The acceleration benefit ($800,000) is the value of having 2 days of cash flow available immediately. The net PV ($200,000) subtracts the capitalized cost of running the system forever.

**Common Mistakes to Avoid:**
- Always subtracting costs when the question asks only for the benefit/value of acceleration
- Calculating only daily net benefit instead of capitalizing the value
- Forgetting to use perpetuity formula (Cost / Rate) for ongoing costs when net PV is needed
- Multiplying accelerated cash by interest rate (it's already a present value)
- Not recognizing the difference between "PV of benefit" and "net PV after costs"
## Pattern: Cash_Change_Source_Use_Inversion

**Description:** In sources-and-uses cash flow analysis, a decrease in cash is a SOURCE (cash was released to fund activities), and an increase in cash is a USE (cash absorbed funds). This is counterintuitive but follows the accounting identity that cash is the balancing item. **CRITICAL: This inversion logic applies ONLY to the cash account itself, NOT to other balance sheet items like accounts payable, inventory, or receivables.**

**When to Use:** Cash flow statement preparation from balance sheets; sources and uses of funds analysis; questions specifically asking whether **cash change** is a source or use.

**When NOT to Use:** 
- Questions about accounts payable, accounts receivable, inventory, or any non-cash balance sheet items
- Questions about individual asset or liability accounts (these follow normal source/use logic)
- When the question asks about a specific balance sheet item other than cash

**Procedure:**
1. **VERIFY the question is asking about CASH specifically** — if asking about any other account, DO NOT use this pattern
2. Formula: Cash Change = Ending Cash - Beginning Cash
3. Calculate the change in cash (can be positive or negative)
4. Apply inversion rule **FOR CASH ONLY**: Negative change (decrease) = SOURCE; Positive change (increase) = USE
5. The amount is always the absolute value of the change
6. Remember: We're analyzing what cash DID (funded activities) not what happened TO cash

**Code Example:**

**Scenario:** Cash decreased from $120,000 to $95,000. Classify as source or use.

**Correct Code:**
```python
# Balance sheet data
cash_beginning = 120_000
cash_ending = 95_000

# Calculate change in cash
cash_change = cash_ending - cash_beginning  # -25,000

# Apply source/use classification FOR CASH ONLY
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
- **CRITICAL ERROR: Applying cash inversion logic to non-cash accounts** (accounts payable, receivables, inventory follow NORMAL logic: decrease in liability = use of cash, increase in liability = source of cash)
- Using intuitive logic (decrease = use) instead of accounting logic for cash
- Treating cash like other balance sheet items (where decrease = use is correct)
- Forgetting that cash is the dependent variable in the accounting equation
- Not taking absolute value for the amount (reporting negative numbers)
- Not verifying that the question is specifically about cash before applying inversion logic

---
## Pattern: Multi_Interpretation_Ratio_Systematic_Testing

**Description:** When a calculated ratio doesn't match any provided option, systematically test alternative numerators/denominators that are contextually valid before concluding an error exists. This includes testing inverse ratios (e.g., Market-to-Book vs. Book-to-Market) when the magnitude of results suggests the reciprocal interpretation may be expected. Document each attempt.

**When to Use:** Any ratio calculation where initial result doesn't match options; questions with ambiguous terminology; standardized test questions with specific expected interpretations; when calculated ratio magnitude is inconsistent with option ranges (e.g., ratio >1 but all options <1).

**Procedure:**
1. Calculate primary/standard interpretation first
2. If no match within ±2% of any option, check if magnitude suggests inverse ratio:
   - If calculated value >1 and all options <1, test reciprocal (1/ratio)
   - If calculated value <1 and all options >1, test reciprocal (1/ratio)
3. Identify other alternative valid interpretations (operating vs net, ending vs average, etc.)
4. Test alternatives in order of likelihood
5. Document each calculation with clear comments
6. Select the interpretation that matches options
7. If still no match, verify data extraction from context

**Example (sanitized):**
> **Scenario:** Calculate "price-to-book ratio." Stock price=$45, Book value per share=$15. Options: [A. 0.25, B. 0.33, C. 0.50, D. 0.67]
>
> **Wrong approach:** Only calculating standard interpretation
> ```python
> # WRONG: Not testing inverse when magnitude doesn't match options
> stock_price = 45
> book_value_per_share = 15
> price_to_book = stock_price / book_value_per_share  # 3.0
> # Result: 3.0 doesn't match any option, code fails
> ```
>
> **Correct approach:** Testing inverse when magnitude suggests it
> ```python
> stock_price = 45
> book_value_per_share = 15
> 
> # Test 1: Standard interpretation (Price/Book)
> price_to_book_standard = stock_price / book_value_per_share  # 3.0
> 
> # Observation: Result is 3.0 but all options are <1
> # This magnitude mismatch suggests inverse ratio expected
> 
> # Test 2: Inverse interpretation (Book/Price)
> book_to_price = book_value_per_share / stock_price  # 0.33
> 
> # Match to options: [0.25, 0.33, 0.50, 0.67]
> # 0.33 matches option B exactly
> 
> options = {'A': 0.25, 'B': 0.33, 'C': 0.50, 'D': 0.67}
> closest = min(options.items(), key=lambda x: abs(x[1] - book_to_price))
> answer = closest[0]  # 'B'
> ```
> The magnitude check (calculated >1, options <1) immediately signals to test the reciprocal interpretation.

**Common Bugs to Avoid:**
- Giving up after first calculation doesn't match
- Not recognizing magnitude mismatches as signals to test inverse ratios
- Not considering that "profit" can mean gross, operating, or net
- Failing to test percentage vs. decimal format
- Not documenting which interpretation was ultimately used
- Ignoring the pattern that when calculated value and all options are on opposite sides of 1.0, the reciprocal is likely needed

---
## Pattern: Return_On_Equity_Balance_Convention

**Description:** ROE calculation can use either ending shareholders' equity or average shareholders' equity. **When both beginning and ending balance sheet data are provided, the standard practice is to use AVERAGE equity** for more accurate representation of the equity base throughout the period. Use ending equity only when beginning data is unavailable or when the question explicitly specifies "ending equity."

**When to Use:** Questions asking for Return on Equity (ROE), Return on Assets (ROA), or similar return ratios; when both beginning and ending balance sheet data are provided.

**When NOT to Use:**
- When only ending period balance sheet is provided (no beginning data)
- When question explicitly asks for "ROE using ending equity"
- When calculated average equity result doesn't match any provided options (then try ending equity)

**Procedure:**
1. **Check if both beginning and ending balance sheet data are available**
2. If YES: Formula: ROE = Net Income / Average Shareholders' Equity
3. If NO: Formula: ROE = Net Income / Ending Shareholders' Equity
4. Calculate average equity: (Beginning Equity + Ending Equity) / 2
5. Calculate beginning equity: Beginning Total Assets - Beginning Total Liabilities
6. Calculate ending equity: Ending Total Assets - Ending Total Liabilities
7. Extract net income from income statement
8. Divide net income by average equity (or ending if no beginning data)
9. Convert to percentage if needed
10. **Match result to closest answer option if options provided**

**Code Example:**

**Scenario:** Net Income=$180,000. Total Assets: Beginning=$1,500,000, Ending=$1,800,000. Total Liabilities: Beginning=$900,000, Ending=$1,000,000. Calculate ROE. Options: [A. 18.5%, B. 20.0%, C. 22.5%, D. 25.0%]

**Correct Code:**
```python
# Income statement
net_income = 180_000

# Balance sheet data
total_assets_beginning = 1_500_000
total_assets_ending = 1_800_000
total_liabilities_beginning = 900_000
total_liabilities_ending = 1_000_000

# Calculate shareholders' equity for both periods
equity_beginning = total_assets_beginning - total_liabilities_beginning  # 600,000
equity_ending = total_assets_ending - total_liabilities_ending  # 800,000

# STANDARD: Use average equity when both periods available
equity_average = (equity_beginning + equity_ending) / 2  # 700,000
roe_average = (net_income / equity_average) * 100  # 25.71%

# Alternative: Using ending equity only (if needed)
roe_ending = (net_income / equity_ending) * 100  # 22.5%

# Match to options: [18.5%, 20.0%, 22.5%, 25.0%]
# Average equity gives 25.71% → closest to option D (25.0%)
# Ending equity gives 22.5% → exact match to option C

# When both beginning and ending data provided, prefer average equity
return_on_equity = round(roe_average, 2)

# Match to closest option
options = {'A': 18.5, 'B': 20.0, 'C': 22.5, 'D': 25.0}
closest = min(options.items(), key=lambda x: abs(x[1] - return_on_equity))
answer = closest[0]  # 'D'
```

**Common Bugs to Avoid:**
- **Using ending equity when both beginning and ending data are available** (should use average)
- Automatically using ending equity without checking if beginning data exists
- Not calculating average equity when multi-period data is provided
- Confusing equity with assets in the denominator
- Not extracting equity correctly from balance sheet (Assets - Liabilities)
- **Returning raw calculation instead of matching to answer options when provided**

---
## Pattern: Collection_Period_Direct_vs_Turnover_Method

**Description:** Average collection period can be calculated two ways: (AR / Sales) × 365 (direct) or 365 / AR Turnover (indirect). The term "average collection period" refers to the average time to collect, which requires using the AVERAGE of beginning and ending accounts receivable, not the ending balance alone. **After calculating, always match the result to the closest provided answer option.**

**When to Use:** Questions asking for "average collection period," "days sales outstanding," or "receivables collection period"; any AR efficiency metric.

**When NOT to Use:**
- When only ending AR balance is provided (no beginning balance available)
- When the question explicitly asks for "collection period using ending balance"

**Procedure:**
1. Formula (Direct): Collection Period = (Average Accounts Receivable / Annual Sales) × 365
2. Formula (Indirect): Collection Period = 365 / (Sales / Average Accounts Receivable)
3. Calculate average AR: (Beginning AR + Ending AR) / 2
4. Use direct method as primary approach for clarity
5. Ensure sales figure is annual (multiply if given monthly/quarterly)
6. **Round result to 2 decimal places**
7. **Match calculated value to closest answer option (if options provided)**
8. **Return the option letter/value that matches, not just the raw calculation**
9. Note: Despite the name "average collection period," some contexts may use ending AR only - verify against answer options if needed

**Example (sanitized):**
> **Scenario:** A company has annual credit sales of $2,920,000. Beginning accounts receivable is $180,000 and ending accounts receivable is $220,000. Calculate the average collection period. Options: [A. 23.5, B. 25.0, C. 27.5, D. 30.0]
>
> **Wrong approach:** Returning raw calculation without matching to options
> ```python
> ar_average = (180_000 + 220_000) / 2
> collection_period = (ar_average / 2_920_000) * 365  # 25.0 days
> collection_period  # Returns 25.0 but doesn't match to option B
> ```
>
> **Correct approach:** Matching to answer options
> ```python
> # Step 1: Calculate average accounts receivable
> ar_beginning = 180_000
> ar_ending = 220_000
> ar_average = (ar_beginning + ar_ending) / 2  # 200,000
> 
> # Step 2: Calculate collection period using average AR
> annual_sales = 2_920_000
> days_in_year = 365
> collection_period = (ar_average / annual_sales) * days_in_year  # 25.0 days
> 
> # Step 3: Round to 2 decimal places
> collection_period_rounded = round(collection_period, 2)
> 
> # Step 4: Match to closest option
> options = {'A': 23.5, 'B': 25.0, 'C': 27.5, 'D': 30.0}
> closest_option = min(options.items(), key=lambda x: abs(x[1] - collection_period_rounded))
> 
> # Return the option letter
> answer = closest_option[0]  # 'B'
> ```

**Common Mistakes to Avoid:**
- Using ending AR instead of average AR for "average collection period" calculations
- Confusing "average collection period" (which uses average AR) with "collection period using ending balance"
- Not calculating the average when both beginning and ending AR are provided
- Using monthly/quarterly sales without annualizing
- Rounding turnover ratio before calculating days (compounds error)
- **Returning raw numerical calculation instead of matching to provided answer options**
- **Not implementing option-matching logic when multiple choice answers are given**

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

## Pattern: Turnover_Ratio_Option_Matching

**Description:** When calculating turnover ratios (fixed asset turnover, inventory turnover, etc.) that mix income statement items with balance sheet items, the numerical result must be matched to the closest provided answer option. The calculation may be correct but fail to select the corresponding multiple-choice letter/value.

**When to Use:** 
- Any turnover ratio calculation with multiple-choice answer options
- Questions where the calculated value needs to be mapped to option letters (A, B, C, D, E)
- When the code returns a numerical value but the expected answer is an option identifier

**Procedure:**
1. Calculate the turnover ratio using appropriate formula (sales/assets, COGS/inventory, etc.)
2. Determine whether to use ending balance or average balance based on context
3. Round the calculated result to match option precision (typically 2 decimal places)
4. **Implement option-matching logic:**
   - Create dictionary/mapping of option letters to numerical values
   - Find the option with minimum absolute difference from calculated value
   - Return the option LETTER, not just the numerical value
5. Include tolerance check (typically ±0.01 for exact matches)

**Code Example:**

**Scenario:** Calculate fixed asset turnover. Sales=$4,000,000, Fixed Assets Beginning=$1,230,000, Ending=$1,300,000. Options: [A. 2.85, B. 3.08, C. 3.16, D. 3.25]

**Wrong Approach:** Returning numerical value without option matching
```python
sales = 4_000_000
fixed_assets_avg = (1_230_000 + 1_300_000) / 2
turnover = sales / fixed_assets_avg  # 3.16
turnover  # Returns 3.16 but doesn't select option C
```

**Correct Approach:** Matching to answer options
```python
# Calculate turnover ratio
sales = 4_000_000
fixed_assets_beginning = 1_230_000
fixed_assets_ending = 1_300_000
fixed_assets_avg = (fixed_assets_beginning + fixed_assets_ending) / 2

turnover_ratio = sales / fixed_assets_avg
turnover_rounded = round(turnover_ratio, 2)  # 3.16

# Match to provided options
options = {
    'A': 2.85,
    'B': 3.08,
    'C': 3.16,
    'D': 3.25
}

# Find closest match
closest_option = min(options.items(), 
                    key=lambda x: abs(x[1] - turnover_rounded))

# Return the option letter
answer = closest_option[0]  # 'C'
answer
```

**Common Mistakes to Avoid:**
- Returning the numerical calculation without matching to option letters
- Not implementing option-matching logic when multiple-choice answers are provided
- Comparing raw calculations to options without proper rounding
- Forgetting to return the option identifier (letter) instead of the numerical value
- Not handling cases where calculated value falls between two options (choose closest)

## Pattern: Bankruptcy_Liquidation_Priority_Waterfall

**Description:** In bankruptcy liquidation scenarios, assets are distributed to creditors following strict legal priority: secured debt first, then administrative/trade creditors, then unsecured debt by seniority (senior before junior), and finally equity holders. Each class must be paid in full before the next class receives anything. **CRITICAL: Code must include explicit return statement or print() for the final answer - bare variable references will cause execution failure.** **IMPORTANT: When the question asks for the "liquidating value" of a specific claim type, return the CLAIM AMOUNT directly if it represents what creditors will receive, not a complex waterfall calculation.**

**When to Use:** 
- Questions asking for liquidating value, bankruptcy distribution, or creditor recovery amounts **where multiple creditor classes compete for limited assets**
- Scenarios involving asset liquidation with multiple creditor classes **and insufficient assets to pay all claims**
- When determining how much each creditor class receives in bankruptcy **from a common pool of assets**
- Questions with terms like "senior debentures," "junior debentures," "secured debt," "trade creditors" **asking about recovery rates or distribution amounts**

**When NOT to Use:**
- **When the question simply asks for the "liquidating value" of a specific claim and the value is directly stated in the balance sheet** (this is a lookup question, not a distribution calculation)
- When secured creditors have dedicated collateral and the question asks for their claim amount (they receive their collateral value, not a share of general assets)
- When assets exceed total liabilities (all creditors paid in full, no waterfall needed)
- When the question provides only claim amounts without asking about actual distributions or recovery

**Procedure:**
1. **FIRST: Determine if this is a distribution calculation or a simple lookup**
   - If question asks "What is the liquidating value of [specific claim]?" and the value is stated → Return the stated value directly
   - If question asks "How much will [creditor class] receive?" or "What is the recovery rate?" → Proceed with waterfall
2. Identify total liquidation proceeds (asset sale value minus liquidation costs)
3. List all creditor claims in priority order:
   - Secured debt (backed by specific collateral)
   - Administrative expenses and trade creditors
   - Senior unsecured debt (senior debentures/bonds)
   - Junior unsecured debt (subordinated debentures)
   - Preferred equity
   - Common equity
4. Apply waterfall distribution:
   - Start with highest priority class
   - Pay full claim amount if sufficient funds remain
   - If insufficient funds, pay partial amount (all remaining funds)
   - Move to next priority class only after current class fully satisfied
5. Calculate payment for target creditor class based on waterfall position
6. **CRITICAL: Use explicit return statement or print() - do NOT end with bare variable name**

**Common Mistakes to Avoid:**
- **CRITICAL: Applying complex waterfall logic when the question simply asks for a claim amount that's directly stated**
- **Over-engineering simple lookup questions into distribution calculations**
- Ending code with bare variable reference in script context
- Not following strict priority order (paying junior debt before senior debt)
- Distributing funds proportionally instead of using waterfall (each class must be paid in full before next class)
- Forgetting to subtract each payment from remaining funds before processing next class
- Paying more than remaining funds to any class (use min(remaining, claim))
- Not recognizing that equity receives nothing until all debt is satisfied
- Confusing secured vs. unsecured debt priority
- **Misinterpreting "liquidating value" questions that are asking for the claim amount, not the distribution amount**

**Example (sanitized):**
> **Scenario 1 (Simple Lookup):** A company in bankruptcy has the following claims: Secured notes $15,000, Trade credit $8,000, Senior bonds $20,000. What is the liquidating value for secured notes?
>
> **Wrong approach:** Building complex waterfall when answer is stated
> ```python
> # WRONG: Over-complicating a simple lookup
> proceeds = 35_000
> secured = 15_000
> remaining = proceeds - secured
> # ... complex waterfall logic ...
> # The question just asks for the claim amount!
> ```
>
> **Correct approach:** Direct lookup
> ```python
> # The question asks for the liquidating value of secured notes
> # This is directly stated in the claims list
> secured_notes_claim = 15_000
> 
> # Return the claim amount
> answer = secured_notes_claim
> print(answer)  # 15,000
> ```

> **Scenario 2 (Distribution Calculation):** A company has liquidation proceeds of $85,000. Claims are: Secured debt $30,000, Trade creditors $15,000, Senior bonds $25,000, Junior bonds $20,000. What amount do senior bondholders **receive**?
>
> **Correct approach:** Waterfall distribution
> ```python
> # Liquidation proceeds
> total_proceeds = 85_000
> 
> # Claims by priority
> secured_debt_claim = 30_000
> trade_creditors_claim = 15_000
> senior_bonds_claim = 25_000
> junior_bonds_claim = 20_000
> 
> # Waterfall distribution
> remaining_funds = total_proceeds
> 
> # Priority 1: Secured debt
> secured_payment = min(remaining_funds, secured_debt_claim)
> remaining_funds -= secured_payment  # 55,000
> 
> # Priority 2: Trade creditors
> trade_payment = min(remaining_funds, trade_creditors_claim)
> remaining_funds -= trade_payment  # 40,000
> 
> # Priority 3: Senior bonds (our target)
> senior_bonds_payment = min(remaining_funds, senior_bonds_claim)
> remaining_funds -= senior_bonds_payment  # 15,000
> 
> # Return the distribution amount
> answer = senior_bonds_payment  # $25,000
> print(answer)
> ```

---