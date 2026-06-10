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

**Description:** "Return on Sales" (ROS) can refer to either Net Profit Margin (Net Income / Sales) or Operating Profit Margin (Operating Profit / Sales). When calculated net margin doesn't match any option, try operating margin.

**When to Use:** Questions asking for "return on sales ratio" or "ROS" given an income statement with both Net Income and Operating Profit figures.

**Procedure:**
1. Primary Formula: ROS = Net Income / Sales (net profit margin)
2. Alternative Formula: ROS = Operating Profit / Sales (operating profit margin)
3. Calculate net profit margin first
4. If result doesn't match any provided option, calculate operating profit margin
5. Express as decimal or percentage based on answer format
6. Operating profit margin is typically 1.5-3x higher than net profit margin

**Code Example:**

**Scenario:** Income statement shows Sales $6,000,000, Operating Profit $1,200,000, Net Income $480,000.

**Correct Code:**
```python
# Income statement components
sales = 6_000_000
operating_profit = 1_200_000
net_income = 480_000

# Method 1: Net profit margin (standard ROS)
net_profit_margin = net_income / sales

# Method 2: Operating profit margin (alternative ROS)
operating_profit_margin = operating_profit / sales

# Check which matches answer options
# If options are around 0.20 (20%), use operating margin
# If options are around 0.08 (8%), use net margin

# For this scenario, if options suggest ~20%:
ros = operating_profit_margin  # 0.20 or 20%

ros
```

**Common Bugs to Avoid:**
- Only calculating one definition without checking if it matches options
- Using Gross Profit instead of Operating Profit or Net Income
- Forgetting to convert between decimal and percentage formats
- Not recognizing that answer options indicate which definition is expected
- Selecting "None of the options" when using wrong profit metric

---

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

**Description:** Correctly identify and extract specific balance sheet line items, distinguishing between subtotals (Total Current Assets, Total Liabilities) and individual components (Common Stock, Retained Earnings).

**When to Use:** Any question requiring balance sheet data extraction, especially for equity calculations, leverage ratios, or working capital analysis.

**Procedure:**
1. Identify the specific year requested in the question
2. Locate the exact line items needed (not subtotals unless specified)
3. For Total Equity: sum Common Stock + Retained Earnings (individual line items)
4. Do NOT use "Total liabilities & equity" line as equity (this equals Total Assets)
5. Verify calculations by checking that Assets = Liabilities + Equity
6. Watch for OCR errors in numbers (commas, decimal points)

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

**Common Bugs to Avoid:**
- Using "Total liabilities & equity" as the equity value (it equals Total Assets)
- Forgetting to add Common Stock and Retained Earnings together
- Using wrong year's data when multi-year balance sheets are provided
- Misreading OCR text (e.g., $1.520.000 vs $1,520,000)
- Not verifying that Assets = Liabilities + Equity as sanity check

---

## Pattern: Percentage vs Decimal Format Matching

**Description:** Financial ratios can be expressed as decimals (0.155) or percentages (15.5%). Match the format used in the answer options to avoid selecting wrong answers due to unit mismatch.

**When to Use:** Any ratio calculation where answer options use specific decimal places or percentage symbols.

**Procedure:**
1. Calculate the ratio in decimal form first
2. Examine answer options to determine expected format
3. If options show values like 0.155, 0.146 → use decimal (multiply by 1)
4. If options show values like 15.5%, 14.6% → multiply decimal by 100
5. Match decimal places shown in options (usually 1-3 places)
6. Round appropriately before comparing to options

**Code Example:**

**Scenario:** Calculate profit margin with Net Income $840,000 and Sales $5,600,000. Options are: A. 15.0%, B. 14.5%, C. 15.5%, D. 16.0%

**Correct Code:**
```python
# Financial data
net_income = 840_000
sales = 5_600_000

# Calculate ratio in decimal form
profit_margin_decimal = net_income / sales  # 0.15

# Check option format - they show percentages
profit_margin_percentage = profit_margin_decimal * 100  # 15.0

# Round to match option precision (1 decimal place)
result = round(profit_margin_percentage, 1)

result  # 15.0 (matches option A: 15.0%)
```

**Common Bugs to Avoid:**
- Comparing 0.15 to options showing 15.0% and thinking there's no match
- Over-rounding or under-rounding relative to option precision
- Expressing answer as "15.0%" string instead of numeric 15.0
- Not recognizing that 0.155 and 15.5% are the same value
- Using excessive decimal places (0.15000000001) instead of rounding appropriately

<budget:token_budget>
Tokens used: 6500
Tokens remaining: 193500
</budget:token_budget>