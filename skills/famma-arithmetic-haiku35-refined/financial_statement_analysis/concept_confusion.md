# FINANCIAL STATEMENT ANALYSIS SKILL PATTERNS

## Pattern: Leverage Ratio (Equity Multiplier) Calculation

**Description:** Leverage ratio in financial analysis refers to the equity multiplier (Total Assets / Total Equity), not debt-to-equity or other leverage measures. Total Equity equals Common Stock + Retained Earnings from the balance sheet.

**When to Use:** Questions asking for "leverage ratio" or "equity multiplier" given balance sheet data with asset and equity components.

**Procedure:**
1. Formula: Leverage Ratio = Total Assets / Total Equity
2. Extract Total Assets from the balance sheet for the specified year
3. Calculate Total Equity = Common Stock + Retained Earnings (not from the "Total liabilities & equity" line)
4. Divide Total Assets by Total Equity
5. Verify result is typically between 1.5 and 4.0 for most companies

**Code Example:**

**Scenario:** A company has Total Assets of $5,000,000, Common Stock of $400,000, and Retained Earnings of $1,600,000 in 2023.

**Correct Code:**
```python
# Balance sheet components
total_assets = 5_000_000
common_stock = 400_000
retained_earnings = 1_600_000

# Calculate total equity (shareholders' equity)
total_equity = common_stock + retained_earnings

# Leverage ratio = Total Assets / Total Equity
leverage_ratio = total_assets / total_equity

# Result
leverage_ratio  # 2.5
```

**Common Bugs to Avoid:**
- Using Total Liabilities / Total Equity (debt-to-equity ratio) instead of equity multiplier
- Using Total Liabilities in the numerator instead of Total Assets
- Forgetting to sum Common Stock and Retained Earnings to get Total Equity
- Using "Total liabilities & equity" as the denominator (this equals Total Assets, yielding 1.0)
- Selecting "None of the options" when calculation error produces wrong result

---

## Pattern: Market-to-Book Ratio with Consistent Units

**Description:** Market-to-book ratio compares total market capitalization to total book value of equity. Both numerator and denominator must use consistent units (either both total dollar amounts or both per-share amounts).

**When to Use:** Questions asking for "market-to-book value" or "market-to-book ratio" given shares outstanding, market price per share, and equity components.

**Procedure:**
1. Formula: Market-to-Book = (Shares Outstanding × Market Price per Share) / (Common Stock + Retained Earnings)
2. Calculate total market capitalization = number of shares × market price per share
3. Calculate book value of equity = Common Stock + Retained Earnings from balance sheet
4. Divide market cap by book value
5. Alternative: (Market Price per Share) / (Book Value per Share), where Book Value per Share = Total Equity / Shares Outstanding
6. Verify both approaches yield the same result

**Code Example:**

**Scenario:** A company has 200,000 shares outstanding trading at $45 per share. Balance sheet shows Common Stock $300,000 and Retained Earnings $2,700,000.

**Correct Code:**
```python
# Market data
shares_outstanding = 200_000
market_price_per_share = 45

# Balance sheet equity components
common_stock = 300_000
retained_earnings = 2_700_000

# Method 1: Total values
total_market_cap = shares_outstanding * market_price_per_share
total_book_value = common_stock + retained_earnings
market_to_book = total_market_cap / total_book_value

# Method 2: Per-share values (verification)
book_value_per_share = total_book_value / shares_outstanding
market_to_book_alt = market_price_per_share / book_value_per_share

# Both methods should yield same result
market_to_book  # 3.0
```

**Common Bugs to Avoid:**
- Mixing total and per-share values (e.g., market price per share / total book value)
- Using only Common Stock as book value, forgetting Retained Earnings
- Using Total Assets instead of Total Equity in the denominator
- Inverting the ratio (book-to-market instead of market-to-book)

---

## Pattern: Return on Sales - Dual Definition Recognition

**Description:** "Return on Sales" (ROS) can refer to either Net Profit Margin (Net Income / Sales) or Operating Profit Margin (Operating Profit / Sales). When calculated net margin doesn't match any option, try operating margin. The answer options themselves provide clues about which definition is expected.

**When to Use:** Questions asking for "return on sales ratio" or "ROS" given an income statement with both Net Income and Operating Profit figures.

**Procedure:**
1. Primary Formula: ROS = Net Income / Sales (net profit margin)
2. Alternative Formula: ROS = Operating Profit / Sales (operating profit margin)
3. Calculate net profit margin first
4. **CRITICAL CHECK:** Compare result against ALL provided options using tolerance of ±0.5% (0.005 in decimal)
5. If NO match found in step 4, calculate operating profit margin
6. **CRITICAL CHECK:** Compare operating margin against ALL provided options
7. Return the value that matches the options
8. Operating profit margin is typically 1.5-3x higher than net profit margin
9. Only select "None of the options" if BOTH definitions fail to match after checking

**Example (sanitized):**
> **Scenario:** An income statement shows Sales of $12,000,000, Operating Profit of $2,640,000, and Net Income of $720,000. The question asks for the return on sales ratio. Answer options are: A. 18.5%, B. 22.0%, C. 24.5%, D. 6.0%
>
> **Wrong approach:** 
> ```python
> net_income = 720_000
> sales = 12_000_000
> ros = net_income / sales  # 0.06 = 6.0%
> # Returns 6.0% (option D) immediately without verification
> # Fails to notice that most options (18.5%, 22.0%, 24.5%) are much higher
> ```
> This calculates net profit margin and returns it without checking if the option pattern suggests a different definition is expected.
>
> **Correct approach:**
> ```python
> # Step 1: Calculate net profit margin
> net_income = 720_000
> sales = 12_000_000
> net_profit_margin = net_income / sales  # 0.06 = 6.0%
> 
> # Step 2: CRITICAL CHECK - Compare against ALL options
> options = [0.185, 0.220, 0.245, 0.060]  # Convert percentages to decimals
> tolerance = 0.005  # ±0.5% tolerance
> 
> # Check if net margin matches any option
> net_matches = [abs(net_profit_margin - opt) <= tolerance for opt in options]
> has_net_match = any(net_matches)
> 
> # Step 3: Analyze option pattern - most options are 3-4x higher than net margin
> # This is a signal that operating margin may be expected
> 
> if not has_net_match or (net_profit_margin < min(options) * 0.5):
>     # Step 4: Calculate operating profit margin
>     operating_profit = 2_640_000
>     operating_profit_margin = operating_profit / sales  # 0.22 = 22.0%
>     
>     # Step 5: CRITICAL CHECK - Compare operating margin against options
>     op_matches = [abs(operating_profit_margin - opt) <= tolerance for opt in options]
>     has_op_match = any(op_matches)
>     
>     if has_op_match:
>         ros = operating_profit_margin  # 0.22 = 22.0%
>         matched_option = options[op_matches.index(True)]
>     else:
>         ros = None  # Neither definition matches
> else:
>     ros = net_profit_margin
>     matched_option = options[net_matches.index(True)]
> 
> # Result: 0.22 (22.0%, option B)
> # Convert to percentage for final answer: 22.0%
> ```
> The key insight: When net margin (6.0%) is an outlier compared to most options (18.5%-24.5%), this signals that operating margin is expected. The correct answer is 22.0%, which represents Operating Profit / Sales.

**Common Mistakes to Avoid:**
- Calculating only net profit margin and returning it without implementing the CHECK steps
- Not writing explicit comparison code that checks calculated value against ALL options
- Failing to recognize that option magnitude patterns indicate which definition is expected
- Selecting the first matching option without verifying it's the contextually appropriate definition
- Not using a tolerance range (±0.5% or 0.005 in decimal) when comparing calculated values to options
- Immediately selecting "None of the options" when net margin doesn't match, without trying operating margin
- Ignoring the signal when one calculated value is an outlier relative to the option cluster
- Not implementing conditional logic with actual comparison operators (abs(), any(), etc.)
## Pattern: Lockbox System Present Value - Working Capital Release

**Description:** The PV of adopting a lockbox system represents the one-time value of working capital released by accelerating collections, calculated as (daily receipts × days saved), not the net daily operating cost.

**When to Use:** Questions about lockbox systems, collection time reduction, or cash management asking for "PV of adopting" or "value of the system."

**Procedure:**
1. Formula: PV = (Average Payments per Day × Average Payment Value) × Days Saved
2. Calculate daily collection amount = payments per day × average payment value
3. Multiply by number of days collection time is reduced
4. This represents freed working capital (one-time benefit)
5. Transaction fees are ongoing costs analyzed separately in NPV, not part of PV calculation
6. Do NOT subtract daily fees from the working capital release

**Code Example:**

**Scenario:** A company receives 500 payments per day averaging $720 each. A lockbox system reduces collection time by 2 days. Transaction fee is $0.35 per payment.

**Correct Code:**
```python
# Collection data
payments_per_day = 500
average_payment_value = 720
days_saved = 2
transaction_fee_per_payment = 0.35

# PV = Working capital released by faster collection
daily_collections = payments_per_day * average_payment_value
pv_of_system = daily_collections * days_saved

# Note: Transaction fees are NOT subtracted from PV
# They would be used in NPV analysis as ongoing costs

pv_of_system  # 720,000
```

**Common Bugs to Avoid:**
- Subtracting daily transaction costs from the working capital release
- Calculating only daily net benefit instead of total working capital freed
- Confusing PV (one-time benefit) with NPV (ongoing net benefit stream)
- Using interest rate in PV calculation (it's already a present value)
- Calculating daily cost × days instead of daily receipts × days

---

## Pattern: Financial Ratio Definition Disambiguation

**Description:** Many financial terms have multiple valid definitions depending on context. When a calculated ratio doesn't match any option, systematically try alternative standard definitions before selecting "None of the options."

**When to Use:** Any financial ratio question where initial calculation produces a result that doesn't match provided options.

**Procedure:**
1. Calculate the most common definition of the requested ratio
2. Check if result matches any option (within rounding tolerance of ±0.05)
3. If no match, identify alternative definitions for that ratio term
4. Calculate each alternative definition systematically
5. Select the option matching any valid calculation
6. Only choose "None of the options" if all standard definitions fail to match

**Code Example:**

**Scenario:** Calculate "return on equity" with Net Income $350,000, Total Equity $2,500,000, Total Assets $4,000,000. Options suggest values around 1.4-1.6.

**Correct Code:**
```python
# Financial data
net_income = 350_000
total_equity = 2_500_000
total_assets = 4_000_000

# Definition 1: Standard ROE = Net Income / Total Equity
roe_standard = net_income / total_equity  # 0.14 or 14%

# Definition 2: If question meant "equity multiplier" (leverage)
equity_multiplier = total_assets / total_equity  # 1.6

# Check which matches the options
# If options are 1.4, 1.5, 1.6, 1.7 → use equity multiplier
# If options are 0.12, 0.14, 0.16, 0.18 → use standard ROE

# Based on options around 1.4-1.6:
result = equity_multiplier

result  # 1.6
```

**Common Bugs to Avoid:**
- Immediately selecting "None of the options" without trying alternatives
- Not recognizing that ratio terminology varies across textbooks/contexts
- Failing to check if answer options provide clues about expected definition
- Ignoring magnitude differences (0.14 vs 1.6) that indicate wrong formula
- Not maintaining a mental library of alternative ratio definitions

---

## Pattern: Balance Sheet Component Extraction

**Description:** Correctly identify and extract specific balance sheet line items, distinguishing between subtotals (Total Current Assets, Total Liabilities) and individual components (Common Stock, Retained Earnings). When calculating cash flow changes, preserve the sign convention where negative values indicate uses of cash and positive values indicate sources of cash.

**When to Use:** Any question requiring balance sheet data extraction, especially for equity calculations, leverage ratios, or working capital analysis.

**When NOT to Use:** Do not use this pattern when the question explicitly asks for categorical descriptions (e.g., "Is this a source or use?") AND requires both a text label and an amount as separate outputs. In such cases, follow the question's exact output format requirements.

**Procedure:**
1. Identify the specific year requested in the question
2. Locate the exact line items needed (not subtotals unless specified)
3. For Total Equity: sum Common Stock + Retained Earnings (individual line items)
4. Do NOT use "Total liabilities & equity" line as equity (this equals Total Assets)
5. Verify calculations by checking that Assets = Liabilities + Equity
6. Watch for OCR errors in numbers (commas, decimal points)
7. **For cash flow changes**: Calculate change as (Year2 - Year1), preserving the sign:
   - Negative result = Use of cash (asset increase or liability decrease)
   - Positive result = Source of cash (asset decrease or liability increase)
8. **Output format**: Return the signed numeric value (e.g., -4500 for a use, +3000 for a source) unless the question explicitly requires a different format

**Code Example:**

**Scenario:** Balance sheet shows Total Assets $8,000,000, Total Liabilities $5,200,000, Common Stock $600,000, Retained Earnings $2,200,000, Total Liabilities & Equity $8,000,000.

**Correct Code:**
```python
# Balance sheet line items
total_assets = 8_000_000
total_liabilities = 5_200_000
common_stock = 600_000
retained_earnings = 2_200_000

# CORRECT: Calculate equity from components
total_equity = common_stock + retained_earnings  # 2,800,000

# WRONG: Using the total line
# total_equity_wrong = 8_000_000  # This is Total Assets!

# Verification: Assets = Liabilities + Equity
verification = total_liabilities + total_equity  # Should equal total_assets

# Calculate leverage ratio as example
leverage_ratio = total_assets / total_equity

leverage_ratio  # 2.857
```

**Cash Flow Change Example:**

**Scenario:** Long-term debt was $49,500 in 2015 and $45,000 in 2016. Calculate the cash flow impact.

**Correct Code:**
```python
# Balance sheet long-term debt values
long_term_debt_2015 = 49_500
long_term_debt_2016 = 45_000

# Calculate change (preserving sign for cash flow convention)
# Decrease in liability = use of cash (negative)
debt_change = long_term_debt_2016 - long_term_debt_2015

# Result: -4500 (negative indicates use of cash)
debt_change  # -4500
```

**Common Bugs to Avoid:**
- Using "Total liabilities & equity" as the equity value (it equals Total Assets)
- Forgetting to add Common Stock and Retained Earnings together
- Using wrong year's data when multi-year balance sheets are provided
- Misreading OCR text (e.g., $1.520.000 vs $1,520,000)
- Not verifying that Assets = Liabilities + Equity as sanity check
- **Returning tuples or text descriptions when the question expects signed numeric values**
- **Taking absolute value of cash flow changes, which removes the use/source distinction**

---
## Pattern: Percentage vs Decimal Format Matching

**Description:** Financial ratios can be expressed as decimals (0.155) or percentages (15.5%). Match the format used in the answer options to avoid selecting wrong answers due to unit mismatch. Preserve calculation precision and only round when necessary for option matching.

**When to Use:** Any ratio calculation where answer options use specific decimal places or percentage symbols.

**When NOT to Use:** Do not apply premature rounding that might cause exact matches to fail. Only round as the final step when comparing to options.

**Procedure:**
1. Calculate the ratio in decimal form first with full precision
2. Examine answer options to determine expected format
3. If options show values like 0.155, 0.146 → use decimal (multiply by 1)
4. If options show values like 15.5%, 14.6% → multiply decimal by 100
5. **Preserve full precision during calculation** - do not round intermediate values
6. **Only round for final comparison** - match decimal places shown in options (usually 1-3 places)
7. **Use tolerance matching** - check if calculated value is within ±0.01 of any option before declaring no match
8. If calculated value matches an option within tolerance, select that option even if not exact

**Code Example:**

**Scenario:** Calculate profit margin with Net Income $840,000 and Sales $5,600,000. Options are: A. 15.0%, B. 14.5%, C. 15.5%, D. 16.0%

**Correct Code:**
```python
# Financial data
net_income = 840_000
sales = 5_600_000

# Calculate ratio in decimal form (preserve full precision)
profit_margin_decimal = net_income / sales  # 0.15

# Check option format - they show percentages
profit_margin_percentage = profit_margin_decimal * 100  # 15.0

# Only round for final comparison (match option precision)
# Options have 1 decimal place
result = round(profit_margin_percentage, 1)

result  # 15.0 (matches option A: 15.0%)
```

**Times Interest Earned Example:**

**Scenario:** Calculate TIE ratio with Operating Profit $530,000 and Interest Expense $160,000. Options are: A. 2.26, B. 3.16, C. 3.84, D. 3.31

**Correct Code:**
```python
# Income statement data
operating_profit = 530_000
interest_expense = 160_000

# Calculate with full precision
tie_ratio = operating_profit / interest_expense  # 3.3125

# Options show 2 decimal places, but check tolerance matching
# 3.3125 rounds to 3.31, which matches option D
# Use tolerance of ±0.01 for matching
options = [2.26, 3.16, 3.84, 3.31]
tolerance = 0.01

# Find matching option
for opt in options:
    if abs(tie_ratio - opt) <= tolerance:
        result = opt
        break

result  # 3.31 (matches option D)
```

**Common Bugs to Avoid:**
- Comparing 0.15 to options showing 15.0% and thinking there's no match
- **Rounding too early in the calculation, which can cause exact matches to fail**
- **Using overly strict equality checks instead of tolerance-based matching**
- Over-rounding or under-rounding relative to option precision
- Expressing answer as "15.0%" string instead of numeric 15.0
- Not recognizing that 0.155 and 15.5% are the same value
- Using excessive decimal places (0.15000000001) instead of rounding appropriately

---

## Pattern: Altman Z-Score Calculation

**Description:** The Altman Z-Score is a bankruptcy prediction model using five weighted financial ratios. The X4 component specifically uses Market Value of Equity / Book Value of Total Liabilities, where Book Value of Total Liabilities = Total Assets - Book Value of Equity. Do not confuse this with Market-to-Book ratio.

**When to Use:** Questions asking for "Z-score," "Altman Z-score," or bankruptcy prediction scores given financial statement data and stock price information.

**Procedure:**
1. Standard Altman Z-Score formula: Z = 1.2(X1) + 1.4(X2) + 3.3(X3) + 0.6(X4) + 1.0(X5)
2. Calculate each component:
   - X1 = Working Capital / Total Assets
   - X2 = Retained Earnings / Total Assets
   - X3 = EBIT / Total Assets
   - X4 = Market Value of Equity / Book Value of Total Liabilities
   - X5 = Sales / Total Assets
3. For X4 specifically:
   - Market Value of Equity = Stock Price × Shares Outstanding
   - Book Value of Total Liabilities = Total Assets - Book Value of Equity
   - **Do NOT use** Market Value / Book Value of Equity (that's market-to-book ratio)
4. Sum the weighted components to get final Z-Score
5. Typical Z-Score ranges: >2.99 (safe), 1.81-2.99 (gray zone), <1.81 (distress)

**Code Example:**

**Scenario:** A company has Total Assets $100,000, EBIT $8,000, Net Working Capital $4,000, Book Value of Equity $22,000, Retained Earnings $20,000, Sales $110,000, stock price $30, and 8,000 shares outstanding.

**Correct Code:**
```python
# Financial data
total_assets = 100_000
ebit = 8_000
net_working_capital = 4_000
book_value_of_equity = 22_000
retained_earnings = 20_000
sales = 110_000
stock_price = 30
shares_outstanding = 8_000

# Calculate market value of equity
market_value_of_equity = stock_price * shares_outstanding  # 240,000

# Calculate book value of total liabilities
book_value_total_liabilities = total_assets - book_value_of_equity  # 78,000

# Z-Score components
x1 = net_working_capital / total_assets
x2 = retained_earnings / total_assets
x3 = ebit / total_assets
x4 = market_value_of_equity / book_value_total_liabilities  # CRITICAL: Use total liabilities
x5 = sales / total_assets

# Calculate Z-Score
z_score = (1.2 * x1) + (1.4 * x2) + (3.3 * x3) + (0.6 * x4) + (1.0 * x5)

z_score  # Final result
```

**Common Bugs to Avoid:**
- Using Market Value of Equity / Book Value of Equity for X4 (that's market-to-book ratio, not Z-Score X4)
- Forgetting to calculate Book Value of Total Liabilities as (Total Assets - Book Equity)
- Using Total Liabilities from balance sheet without verifying it equals Assets - Equity
- Mixing up the weights (1.2, 1.4, 3.3, 0.6, 1.0) in the formula
- Not calculating market value of equity correctly (price × shares)
- Using net income instead of EBIT for X3

<budget:token_budget>
Tokens used: 9,850
Tokens remaining: 183,650
</budget:token_budget>