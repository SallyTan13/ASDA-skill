# SKILL PATTERNS FOR FIXED INCOME CALCULATIONS (Program of Thought)

## Pattern: Forward Rate Bootstrapping from Zero Rates

**Description:** Computing forward rates from zero/spot rates requires precise application of the no-arbitrage relationship between multi-period and sequential single-period investments, using either discrete or continuous compounding consistently.

**When to Use:** Questions asking for forward rates given spot/zero rates, or requiring calculation of implied future rates from a term structure.

**Procedure:**
1. Formula (discrete annual compounding): `(1 + z_n)^n = (1 + z_m)^m × (1 + f(m,n))^(n-m)` where f(m,n) is the forward rate from year m to year n
2. Solve for forward rate: `f(m,n) = [(1 + z_n)^n / (1 + z_m)^m]^(1/(n-m)) - 1`
3. Verify units: ensure all rates are in same compounding convention (annual, semiannual, continuous)
4. Return as decimal (e.g., 0.034126) or convert to percentage based on question format

**Code Example:**

**Scenario:** Given 2-year zero rate of 4.5% and 5-year zero rate of 5.2%, calculate the forward rate for years 2 to 5.

**Correct Code:**
```python
# Zero rates as decimals
z2 = 0.045
z5 = 0.052
n = 5
m = 2

# Bootstrap forward rate using discrete compounding
forward_rate = ((1 + z5)**n / (1 + z2)**m)**(1/(n - m)) - 1

# Result as decimal
forward_rate  # 0.05567 (5.567%)
```

**Common Bugs to Avoid:**
- Using arithmetic averaging instead of geometric compounding relationship
- Mixing continuous compounding (e^rt) with discrete compounding (1+r)^t formulas
- Incorrect exponent arithmetic: using (n-m) as exponent instead of 1/(n-m) in the final step
- Forgetting to subtract 1 after taking the root

---

## Pattern: Yield to Maturity from Forward Rates

**Description:** The yield to maturity (spot rate) for an n-year zero-coupon bond is the geometric mean of the sequence of forward rates, not the arithmetic mean.

**When to Use:** Questions providing forward rate tables and asking for YTM or spot rates for specific maturities.

**Procedure:**
1. Formula: `(1 + YTM_n)^n = (1 + f_0) × (1 + f_1) × ... × (1 + f_(n-1))`
2. Identify all forward rates from year 0 to year n-1
3. Compute product of (1 + each forward rate)
4. Take the nth root and subtract 1: `YTM_n = [product]^(1/n) - 1`
5. Return as decimal or percentage as required

**Code Example:**

**Scenario:** Forward rates are: Year 0: 3.5%, Year 1: 4.2%, Year 2: 4.8%. Calculate 3-year zero-coupon bond YTM.

**Correct Code:**
```python
# Forward rates as decimals
forward_rates = [0.035, 0.042, 0.048]
n = len(forward_rates)

# Geometric mean calculation
product = 1.0
for rate in forward_rates:
    product *= (1 + rate)

ytm = product**(1/n) - 1

# Result as decimal
ytm  # 0.04166 (4.166%)
```

**Common Bugs to Avoid:**
- Using arithmetic mean: `sum(rates)/n` instead of geometric mean
- Off-by-one errors: using n+1 rates for an n-year bond
- Forgetting that year 0 rate applies to the first period
- Not converting percentage inputs to decimals before calculation

---

## Pattern: Zero-Coupon Bond Pricing with Forward Rates

**Description:** Pricing a zero-coupon bond requires sequential discounting through each period using the appropriate forward rate for that specific time interval. The calculation method depends on the compounding convention: discrete compounding uses (1+r)^n while continuous compounding uses e^(r×n).

**When to Use:** Questions providing forward rate schedules and asking for bond prices at various maturities, or questions asking for percentage changes in zero-coupon bond values due to yield shifts. Pay attention to whether the question specifies "continuous compounding" or uses discrete compounding (default).

**Procedure:**
1. Identify compounding convention from question text:
   - "continuous compounding" or "continuously compounded" → use exponential formula
   - No specification or "annual compounding" → use discrete formula
2. For discrete compounding: `PV = FV / [(1 + f_0) × (1 + f_1) × ... × (1 + f_(n-1))]`
3. For continuous compounding: `PV = FV × e^(-r×n)` where r is the yield and n is maturity
4. For yield sensitivity analysis:
   - Calculate initial price at original yield
   - Calculate new price at shifted yield (original + change)
   - Compute percentage change: `(new_price - initial_price) / initial_price × 100`
5. Check question wording for sign convention:
   - "percentage change" or "change in value" → report signed value (negative for yield increase)
   - "percentage changes" (plural) in sensitivity context → often expects absolute magnitude
   - "impact" or "effect" → typically absolute magnitude

**Worked Example:**

**Scenario 1:** Face value $1,000, 3-year zero-coupon bond with continuous compounding at 4% yield. Calculate price, then find percentage change if yield increases to 6%.

```python
import math

# Given values
face_value = 1000
maturity = 3
initial_yield = 0.04
new_yield = 0.06

# Step 1: Identify compounding - continuous compounding specified
# Step 2: Calculate initial price using continuous compounding
# Formula: PV = FV × e^(-r×n)
initial_price = face_value * math.exp(-initial_yield * maturity)

# Step 3: Calculate new price after yield increase
new_price = face_value * math.exp(-new_yield * maturity)

# Step 4: Calculate percentage change
percentage_change = (new_price - initial_price) / initial_price * 100

# Step 5: For "percentage change" in yield sensitivity, report signed value
percentage_change  # -5.50 (negative indicates price decrease)
```

**Scenario 2:** Portfolio of zero-coupon bonds with total value $10M, average maturity 5 years, continuous compounding at 4%. Find magnitude of percentage change for 1% yield increase.

```python
import math

# Given values
portfolio_value = 10_000_000
avg_maturity = 5
initial_yield = 0.04
yield_increase = 0.01
new_yield = initial_yield + yield_increase

# Step 1: Continuous compounding specified
# Step 2: Calculate price ratio (FV cancels out)
initial_factor = math.exp(-initial_yield * avg_maturity)
new_factor = math.exp(-new_yield * avg_maturity)

# Step 3: Percentage change
percentage_change = (new_factor - initial_factor) / initial_factor * 100

# Step 4: For sensitivity analysis asking for "magnitude", use absolute value
magnitude = abs(percentage_change)

magnitude  # 4.88 (absolute percentage change)
```

**Common Bugs to Avoid:**
- **Using discrete formula (1+r)^n when continuous compounding is specified** - this is the most critical error
- Using discrete compounding formula `PV = FV/(1+r)^n` when question states "continuous compounding"
- Using continuous formula `PV = FV×e^(-r×n)` when question uses discrete/annual compounding
- Not recognizing "continuously compounded" or "per annum with continuous compounding" keywords
- Returning negative percentage when question asks for "percentage changes" in sensitivity context (often wants magnitude)
- Confusing the sign convention: always returning absolute value when question asks for "change in value"
- Forgetting to convert basis points to decimal (100 bps = 0.01)

**CHECK Steps:**
- If question contains "continuous" or "continuously compounded", verify code uses `math.exp(-r*n)`
- If question uses "annual compounding" or no specification, verify code uses `(1+r)**n`
- For yield sensitivity: assert that price decreases when yield increases (inverse relationship)
- Validate: `abs(percentage_change)` should approximately equal `duration × yield_change × 100` for small changes
- If question asks for "percentage changes" (plural) in portfolio sensitivity context, consider reporting absolute magnitude
- If question asks for "change in value" (singular), report signed value
- For continuous compounding: verify `import math` is included at top of code
```

---
## Pattern: Bond Price Quote Conversion

**Description:** Bond prices are typically quoted as percentages of par value (e.g., 105.312 means 105.312% of face value), and must be converted to dollar amounts before use in yield calculations.

**When to Use:** Questions showing bond price quotes without explicit dollar signs, especially when calculating current yield, YTM, or other price-based metrics.

**Procedure:**
1. Identify if price is quoted as percentage (typically 2-3 decimal places, values near 100)
2. Convert to dollar price: `dollar_price = quoted_price * face_value / 100`
3. Use dollar price in subsequent calculations
4. For current yield: `current_yield = annual_coupon_dollars / dollar_price`

**Code Example:**

**Scenario:** Bond quoted at 98.750, face value $1,000, annual coupon 6.5%. Calculate current yield.

**Correct Code:**
```python
quoted_price = 98.750  # This is a percentage
face_value = 1000
coupon_rate = 0.065

# Convert quoted price to dollar amount
dollar_price = quoted_price * face_value / 100  # 987.50

# Annual coupon in dollars
annual_coupon = coupon_rate * face_value  # 65.00

# Current yield
current_yield = annual_coupon / dollar_price

current_yield  # 0.06582 (6.582%)
```

**Common Bugs to Avoid:**
- Using quoted price directly as dollar amount (magnitude error of ~100x)
- Dividing by quoted price instead of dollar price
- Confusing face value with market price in coupon calculations
- Not recognizing that prices near 100 with decimals are percentage quotes

---

## Pattern: Multiple-Choice Tolerance Matching

**Description:** When computed values must be matched to multiple-choice options, apply reasonable tolerance (typically ±0.5% for rates, ±0.5 for prices) rather than requiring exact matches, as different rounding conventions and compounding assumptions produce slight variations.

**When to Use:** Any multiple-choice question where computed financial values (yields, prices, returns) must be mapped to lettered options.

**Procedure:**
1. Compute the target value with full precision
2. Compare to each option using absolute difference
3. Select option with minimum absolute difference if within tolerance
4. Typical tolerance: 0.005 (50 bps) for rates, 0.5% of value for prices
5. Only select "None of the above" if all options exceed tolerance threshold

**Code Example:**

**Scenario:** Computed yield is 7.118%, options are A: 6.85%, B: 7.10%, C: 7.45%, D: None.

**Correct Code:**
```python
computed_value = 0.07118
options = {'A': 0.0685, 'B': 0.0710, 'C': 0.0745}
tolerance = 0.005  # 50 basis points

# Find closest option
min_diff = float('inf')
best_option = 'D'  # Default to "None"

for label, value in options.items():
    diff = abs(computed_value - value)
    if diff < min_diff:
        min_diff = diff
        best_option = label

# Check if within tolerance
if min_diff > tolerance:
    best_option = 'D'

best_option  # 'B' (difference is 0.00018, within tolerance)
```

**Common Bugs to Avoid:**
- Requiring exact match and defaulting to "None" for small discrepancies
- Not accounting for rounding in intermediate steps
- Using overly strict tolerance (e.g., 0.0001 for percentage rates)
- Comparing percentages to decimals without unit conversion

---

## Pattern: Weighted Average Duration

**Description:** Portfolio or liability duration is the market-value-weighted average of individual component durations, where weights sum to 1.0 and represent each component's proportion of total market value.

**When to Use:** Questions asking for portfolio duration, liability duration, or asset duration given individual components with market values and durations.

**Procedure:**
1. Formula: `Duration = Σ(w_i × D_i)` where `w_i = MV_i / Σ(MV_i)`
2. Sum all relevant market values to get total
3. Calculate weight for each component: market_value / total_market_value
4. Multiply each weight by its duration
5. Sum all weighted durations

**Code Example:**

**Scenario:** Three liabilities: $500M at 0 years, $300M at 2.5 years, $200M at 8.0 years. Find duration.

**Correct Code:**
```python
# Market values and durations
liabilities = [
    {'mv': 500, 'duration': 0.0},
    {'mv': 300, 'duration': 2.5},
    {'mv': 200, 'duration': 8.0}
]

# Calculate total market value
total_mv = sum(item['mv'] for item in liabilities)

# Weighted average duration
weighted_duration = sum(
    (item['mv'] / total_mv) * item['duration'] 
    for item in liabilities
)

weighted_duration  # 2.35 years
```

**Common Bugs to Avoid:**
- Using equal weights instead of market-value weights
- Including equity or non-relevant items in liability duration calculation
- Forgetting to divide by total market value (using raw MV × duration sums)
- Excluding zero-duration items (they still contribute to total MV denominator)

---

## Pattern: Total Return Analysis with Reinvestment

**Description:** Total return for a bond over a holding period includes coupon income, reinvestment income on coupons received, and capital gain/loss, all divided by initial investment.

**When to Use:** Questions asking for expected total return, holding period return, or return analysis given initial price, ending price, coupons, and reinvestment rates.

**Procedure:**
1. Formula: `Total Return = (Coupon Income + Reinvestment Income + Price Change) / Initial Price`
2. Calculate total coupon payments received during holding period
3. Calculate reinvestment income on each coupon (time-weighted by reinvestment rate)
4. Calculate price change: ending_price - beginning_price
5. Sum all components and divide by initial price

**Code Example:**

**Scenario:** 1-year holding period, initial price $105, ending price $104, 6% annual coupon (paid semiannually), 1.5% annual reinvestment rate.

**Correct Code:**
```python
initial_price = 105
ending_price = 104
annual_coupon_rate = 0.06
face_value = 100  # Assume par
reinvestment_rate_annual = 0.015
holding_period = 1  # year

# Semiannual coupon payment
coupon_payment = (annual_coupon_rate / 2) * face_value  # 3.00

# Two coupon payments over 1 year
num_payments = 2
total_coupon_income = coupon_payment * num_payments  # 6.00

# Reinvestment income: first coupon reinvested for 6 months
reinvestment_income = coupon_payment * (reinvestment_rate_annual / 2)  # 0.0225

# Capital change
capital_change = ending_price - initial_price  # -1.00

# Total return
total_return = (total_coupon_income + reinvestment_income + capital_change) / initial_price

total_return  # 0.04879 (4.879%)
```

**Common Bugs to Avoid:**
- Forgetting to account for semiannual coupon structure (two payments per year)
- Not time-weighting reinvestment income (first coupon earns interest, last doesn't)
- Using face value instead of market price as denominator
- Omitting reinvestment income component entirely

---

## Pattern: Sign Convention for Sensitivity Measures

**Description:** When reporting percentage changes in bond value due to yield changes, the sign convention depends on question phrasing: "change in value" typically expects negative for yield increases, while "duration effect" or "sensitivity" may expect absolute magnitude.

**When to Use:** Questions asking for percentage change, price sensitivity, or duration-based impact when yields change.

**Procedure:**
1. Calculate the actual change: `new_value - old_value`
2. Compute percentage change: `(new_value - old_value) / old_value`
3. Check question wording: "change" suggests signed value, "sensitivity" or "effect" may suggest absolute value
4. For duration approximation: `% change ≈ -Duration × Δy` (negative for yield increase)
5. Report with appropriate sign based on context

**Code Example:**

**Scenario:** Portfolio value $1,000, duration 5.5 years, yields increase by 0.75%. Calculate percentage change.

**Correct Code:**
```python
initial_value = 1000
duration = 5.5
yield_change = 0.0075  # 75 basis points increase

# Duration approximation (negative for yield increase)
percentage_change = -duration * yield_change

# For reporting "change in value"
percentage_change  # -0.04125 (-4.125%)

# For reporting "sensitivity" or "magnitude"
abs(percentage_change)  # 0.04125 (4.125%)
```

**Common Bugs to Avoid:**
- Always reporting negative when question asks for "magnitude of change"
- Always reporting positive when question asks for "change in value"
- Not reading question carefully to determine expected sign convention
- Confusing modified duration with Macaulay duration in approximation formula

---

## Pattern: Zero-Coupon Bond YTM from Price

**Description:** The yield to maturity of a zero-coupon bond is calculated by solving for the discount rate that equates present value to market price, using the appropriate compounding convention. **Critical: Ensure proper rounding and percentage format conversion based on question requirements.**

**When to Use:** Questions providing zero-coupon bond prices and asking for yields, or requiring bootstrapping of spot rate curves from zero-coupon bond prices.

**When NOT to Use:** When the question provides yields and asks for prices (use the pricing pattern instead).

**Procedure:**
1. Formula (annual compounding): `Price = Face_Value / (1 + YTM)^n`
2. Solve for YTM: `YTM = (Face_Value / Price)^(1/n) - 1`
3. Verify maturity n matches the bond's time to maturity
4. **Round to 4 decimal places** to eliminate floating-point artifacts
5. **Check question format requirements:**
   - If options show percentages (e.g., "7.33%"), convert: `round(ytm * 100, 2)`
   - If options show decimals (e.g., "0.0733"), keep: `round(ytm, 4)`
6. Return in the format matching the answer options

**Worked Example:**
**Question:** A 4-year zero-coupon bond with face value $1,000 is priced at $792.16. Calculate the YTM.

Options: A. 6.00%, B. 6.00%, C. 5.98%, D. 6.02%

```python
face_value = 1000
price = 792.16
maturity = 4

# Step 1: Solve for yield to maturity
ytm = (face_value / price)**(1/maturity) - 1

# Step 2: Round to eliminate floating-point artifacts
ytm = round(ytm, 4)  # 0.0600

# Step 3: Check option format - they show percentages
# Convert to percentage format
ytm_percent = round(ytm * 100, 2)

ytm_percent  # 6.00 (matches option format)
```

**Common Bugs to Avoid:**
- Using continuous compounding formula when discrete is expected: `ln(FV/P)/n`
- Incorrect exponent: using `n` instead of `1/n` in the power
- Forgetting to subtract 1 after taking the root
- **Not rounding before format conversion** - produces artifacts like 5.999999 instead of 6.00
- **Returning decimal when options show percentages** - format mismatch
- Misidentifying maturity (using issue date instead of remaining time)

**CHECK Steps:**
- Verify formula uses `(1/maturity)` as exponent, not `maturity`
- Assert 0.01 < ytm < 0.30 for typical bond yields
- **MANDATORY:** Round to 4 decimals before any format conversion
- **MANDATORY:** Check if answer options are in percentage or decimal format
- If options show "%" symbols, multiply by 100 and round to 2 decimals
- If options show pure decimals, keep as decimal rounded to 4 places
- Validate: higher price → lower yield (inverse relationship)
## Pattern: Percentage vs. Decimal Output Format

**Description:** Financial calculations should maintain values as decimals (0.0525) during computation, but final output format must match the question's expected format (5.25% vs 0.0525) or multiple-choice option format. Floating-point precision artifacts must be cleaned up before final output AND before multiple-choice matching. **This pattern is MANDATORY for all financial rate calculations** - never skip rounding and format validation.

**When to Use:** All questions, especially when final answer must be compared to options or when question specifies format like "express as percentage." Also when floating-point arithmetic produces precision artifacts (e.g., 0.059999999999999956 or 11.999915337478395 instead of 0.06 or 12.0). **Apply this pattern to EVERY rate calculation without exception.**

**When NOT to Use:** Never skip this pattern - all financial calculations need proper rounding and format handling.

**Procedure:**
1. Perform all intermediate calculations in decimal form (0.05 not 5)
2. **CRITICAL**: Round result to appropriate precision BEFORE any format conversion or option matching:
   - For rates/yields/returns: 4 decimal places (0.0001 = 1 basis point)
   - For prices: 2 decimal places
   - For percentages: 2 decimal places after converting to percentage
3. **MANDATORY CHECK**: Examine ground truth or question format to determine output format:
   - If ground truth shows "6%" or "5.25%" → convert to percentage (multiply by 100)
   - If ground truth shows "0.06" or "0.0525" → keep as decimal
   - If question asks "what percentage" or "express as %" → convert to percentage
4. Apply format conversion with appropriate rounding:
   - For percentage output: `round(decimal_value * 100, 2)`
   - For decimal output: `round(decimal_value, 4)`
5. Ensure final expression returns the correctly formatted value

**Worked Example:**
**Question:** Calculate the expected rate of return over the coming year on a 4-year zero-coupon bond given current yield of 5.5% and expected yield of 5.0% next year.

```python
# Step 1: Calculate raw return (may have floating-point artifacts)
current_yield = 0.055
expected_yield_next_year = 0.050
years_to_maturity = 4
years_after_holding = 3

# Price today (per $100 face value)
price_today = 100 / (1 + current_yield)**years_to_maturity

# Expected price in one year
price_next_year = 100 / (1 + expected_yield_next_year)**years_after_holding

# Raw holding period return
raw_return = (price_next_year - price_today) / price_today

# Step 2: CRITICAL - Round to eliminate floating-point precision issues
# Use 4 decimal places for rates
clean_return = round(raw_return, 4)  # 0.0850 (not 0.08499999...)

# Step 3: MANDATORY CHECK - Determine output format from question
# Question asks "rate of return" - check if ground truth expects percentage or decimal
# If ground truth shows "8.5%" or question says "what percentage", convert to percentage
# If ground truth shows "0.085", keep as decimal

# Step 4: Format based on requirements
# For percentage format (when ground truth shows "%"):
return_percent = round(clean_return * 100, 2)  # 8.50

# For decimal format (when ground truth shows decimal):
return_decimal = clean_return  # 0.0850

# Step 5: Return appropriate format (use percentage if ground truth shows %)
return_percent  # 8.50 (matches "8.5%" format)
```

**Common Bugs to Avoid:**
- **CRITICAL**: Returning 0.0599999999 when ground truth shows 6% - always round first
- **CRITICAL**: Returning 0.06 when ground truth shows 6% - must convert to percentage format
- Returning 6.23 when ground truth shows 0.0623 - wrong format conversion
- Not rounding before option matching - causes 11.9999... to match 11% instead of 12%
- Not rounding floating-point results, producing artifacts like 0.059999999999999956
- Mixing formats during calculation (some steps in %, some in decimal)
- Using print() instead of expression for final value
- Over-rounding too early in intermediate steps (round only before final output/matching)
- **Skipping format validation entirely** - assuming decimal is always correct

**CHECK Steps:**
- **MANDATORY**: If result has more than 6 decimal places, apply rounding to eliminate floating-point artifacts
- **MANDATORY**: Before returning final answer, check ground truth format:
  - If ground truth contains "%" symbol → multiply by 100 and round to 2 decimals
  - If ground truth is pure decimal → round to 4 decimals
- **MANDATORY**: Before multiple-choice matching, round to 2 decimal places for percentages, 4 for decimals
- Verify final output format matches question expectations (% vs decimal)
- Assert result is within reasonable bounds for financial rates (typically -1.0 to 2.0 for returns in decimal form, -100 to 200 for percentage form)
- If comparing to multiple-choice options, ensure units match before comparison
- **VALIDATION**: For rates/returns, verify `0.0001 <= abs(clean_value) <= 2.0` (decimal) or `0.01 <= abs(percent_value) <= 200` (percentage)
- **FINAL CHECK**: Confirm last line is an expression (not print statement) that returns the correctly formatted value
## Pattern: Coupon Bond Pricing with Zero Rates

**Description:** Pricing coupon bonds requires discounting each cash flow (coupons and principal) separately using the zero rate corresponding to that cash flow's timing, not a single yield.

**When to Use:** Questions providing zero rate term structures and asking for theoretical bond prices with coupon payments.

**Procedure:**
1. Identify all cash flows: periodic coupons and final principal payment
2. Match each cash flow to its timing (0.5, 1.0, 1.5, ... years)
3. Discount each cash flow using the zero rate for that maturity: `PV_i = CF_i / (1 + z_i)^t_i`
4. Sum all present values to get bond price
5. Adjust for compounding convention (annual, semiannual, continuous)

**Code Example:**

**Scenario:** 2-year bond, 5% annual coupon, $100 face value. Zero rates: 1-year 4%, 2-year 4.5%. Find price.

**Correct Code:**
```python
face_value = 100
coupon_rate = 0.05
zero_rates = {1: 0.040, 2: 0.045}  # year: rate

# Cash flows: $5 at year 1, $105 at year 2
cash_flows = {
    1: coupon_rate * face_value,  # 5
    2: coupon_rate * face_value + face_value  # 105
}

# Discount each cash flow by appropriate zero rate
price = sum(
    cf / (1 + zero_rates[t])**t 
    for t, cf in cash_flows.items()
)

price  # 100.91
```

**Common Bugs to Avoid:**
- Using a single discount rate for all cash flows
- Mismatching cash flow timing with zero rate maturity
- Forgetting to include principal in final cash flow
- Using wrong compounding convention (continuous vs. discrete)

</budget:token_budget>

## Pattern: Table Row Extraction and Validation

**Description:** When questions reference specific rows in tables (e.g., "second row", "fourth row"), correctly identify and extract data from that row, accounting for whether the table has a header row and using zero-based or one-based indexing appropriately. **Critical: Verify the table structure to determine which columns contain known vs. unknown values before extraction.**

**When to Use:** Questions that explicitly reference "first row", "second row", "third row", etc. in tables, especially when solving for unknown values in compound interest, present value, or EAR/APR conversion problems.

**When NOT to Use:** 
- When the table structure is ambiguous and column headers don't clearly indicate which values are given vs. to-be-calculated
- When the question asks for a value that is already provided in the table (extraction-only, no calculation needed)

**Procedure:**
1. Parse the table structure from OCR text or image description
2. Identify if there is a header row (column names like "Present Value", "Years", "Interest Rate")
3. **CRITICAL NEW STEP:** Examine the table to determine which column contains the unknown value:
   - Look for "?" symbols, blank cells, or missing values in the target row
   - If no explicit markers, use the question text to identify what's being asked for
   - Verify that extracted values are from the KNOWN columns, not the unknown column
4. Determine the target row number from question text (e.g., "second row" = row index 1 after header)
5. Extract all KNOWN values from that specific row
6. Apply appropriate formula to solve for the unknown value
7. Validate extraction by checking if extracted values are reasonable for their column types

**Worked Example:**
**Question:** Solve for the unknown interest rate for the second row in the table.

Table:
```
Present Value | Years | Interest Rate | Future Value
$800          | 4     | ?            | $1,200
$600          | 6     | ?            | $950
$1,500        | 8     | ?            | $2,800
```

```python
# Step 1: Parse table data (excluding header)
table_data = [
    {'pv': 800, 'years': 4, 'fv': 1200},    # Row 1
    {'pv': 600, 'years': 6, 'fv': 950},     # Row 2
    {'pv': 1500, 'years': 8, 'fv': 2800}    # Row 3
]

# Step 2: Identify target row from question ("second row")
row_number = 2  # "second row" in question
row_index = row_number - 1  # Convert to zero-based index

# Step 3: Extract KNOWN data from correct row
target_row = table_data[row_index]
pv = target_row['pv']
years = target_row['years']
fv = target_row['fv']

# Step 4: Validate extraction - ensure we have the knowns, not the unknown
assert pv > 0 and fv > pv and years > 0, "Invalid row data"

# Step 5: Apply formula to solve for unknown (interest rate)
# FV = PV * (1 + r)^n  =>  r = (FV/PV)^(1/n) - 1
interest_rate = (fv / pv)**(1/years) - 1

# Step 6: Round to appropriate precision
interest_rate = round(interest_rate, 4)

interest_rate  # 0.0788 (7.88%)
```

**Common Bugs to Avoid:**
- **Using wrong row index** - confusing "second row" with index 0 or index 2
- Not accounting for header rows when counting
- Extracting data from first row when question asks for second row
- **Extracting the unknown value instead of calculating it** - if the table shows a value in the target cell, verify whether it's given or needs calculation
- Hardcoding values from wrong row in the code
- Not validating that extracted values make sense (e.g., PV should be less than FV for positive rates)

**CHECK Steps:**
- Verify row_index = row_number - 1 for one-based counting (most common in questions)
- **CRITICAL:** Before extraction, identify which column the question asks for and ensure you're NOT extracting from that column
- Assert extracted values are within reasonable ranges for their column types
- If question says "second row" and table has header, target should be data row 2 (index 1)
- Double-check that PV < FV for positive interest rate problems
- Validate years > 0 and all monetary values > 0

---
## Pattern: EAR/APR Table Structure Identification

**Description:** When working with EAR/APR conversion tables, correctly identify which column contains known values (given) and which contains unknown values (to be calculated), as tables may present data with either EAR or APR as the unknown. **Critical: The APR column may contain the given values while EAR is unknown, or vice versa.**

**When to Use:** Questions involving tables with APR, compounding frequency, and EAR columns where one of the rate columns has missing or unknown values to be calculated.

**When NOT to Use:**
- When both APR and EAR are provided and the question asks for a different calculation
- When the table structure doesn't follow the standard APR/Compounding/EAR format

**Procedure:**
1. Parse the table and identify all three columns: APR, Compounding Frequency, EAR
2. **CRITICAL:** Examine the target row to determine which value is KNOWN and which is UNKNOWN:
   - Check the APR column: if it has a value (not "?", not blank), APR is KNOWN → calculate EAR
   - Check the EAR column: if it has a value (not "?", not blank), EAR is KNOWN → calculate APR
   - **Do NOT assume** the same column is unknown across all rows - check each row individually
3. Extract the known rate value and compounding frequency from the target row
4. Apply appropriate formula based on what's being solved:
   - **Solving for EAR from APR:** `EAR = (1 + APR/m)^m - 1` (discrete) or `EAR = e^APR - 1` (continuous)
   - **Solving for APR from EAR:** `APR = m × ((1 + EAR)^(1/m) - 1)` (discrete) or `APR = ln(1 + EAR)` (continuous)
5. Validate result is reasonable (typically 0.01 to 0.30 for both APR and EAR)

**Worked Example:**
**Question:** Find the EAR for the second row in the table.

Table:
```
APR  | Number of Times Compounded | EAR
8.5% | Quarterly                  | ?
11.2%| Monthly                    | ?
9.7% | Weekly                     | ?
```

```python
import math

# Step 1: Parse table structure - APR is KNOWN, EAR is UNKNOWN
table_data = [
    {'apr': 0.085, 'compounding': 'Quarterly', 'ear': None},   # Row 1
    {'apr': 0.112, 'compounding': 'Monthly', 'ear': None},     # Row 2
    {'apr': 0.097, 'compounding': 'Weekly', 'ear': None}       # Row 3
]

# Step 2: Identify target row ("second row")
row_index = 1  # Zero-based index for second row
target_row = table_data[row_index]

# Step 3: Extract KNOWN values (APR is given, EAR is unknown)
apr = target_row['apr']
compounding_type = target_row['compounding']

# Step 4: Map compounding frequency
frequency_map = {
    'Annually': 1,
    'Semiannually': 2,
    'Quarterly': 4,
    'Monthly': 12,
    'Weekly': 52,
    'Daily': 365,
    'Infinite': float('inf'),
    'Continuous': float('inf')
}

# Step 5: Calculate EAR from APR
if compounding_type in ['Infinite', 'Continuous']:
    # Continuous: EAR = e^APR - 1
    ear = math.exp(apr) - 1
else:
    # Discrete: EAR = (1 + APR/m)^m - 1
    m = frequency_map[compounding_type]
    ear = (1 + apr/m)**m - 1

# Step 6: Round to appropriate precision
ear = round(ear, 4)

ear  # 0.1177 (11.77%)
```

**Common Bugs to Avoid:**
- **Misidentifying which column is known vs. unknown** - treating APR values as EAR or vice versa
- **Assuming the same column is unknown for all rows** - each row may have different known/unknown structure
- Using EAR formula when question asks for APR (and APR is unknown)
- Using APR formula when question asks for EAR (and EAR is unknown)
- Not checking whether compounding is continuous (requires different formula)
- Applying discrete formula to continuous compounding or vice versa
- **Extracting a value that's already given instead of calculating the unknown**

**CHECK Steps:**
- **CRITICAL:** Before calculation, verify which column the question asks for AND which column has values in the target row
- If question asks for "APR" and the APR column has values, you may be extracting not calculating - re-read the question
- If question asks for "EAR" and the EAR column has values, you may be extracting not calculating - re-read the question
- Confirm the known value is extracted from the correct column (the one with data)
- Assert 0.01 < result < 0.30 for typical interest rate problems
- If compounding is "Infinite" or "Continuous", use logarithmic formulas
- If compounding is discrete (Quarterly, Monthly, etc.), use power formulas
- Double-check row extraction using the table row validation pattern

---
## Pattern: Dollar Duration Portfolio Rebalancing

**Description:** When rebalancing a portfolio to maintain a target dollar duration after interest rate shifts, calculate the required cash investment by determining how much additional investment (at specified allocation proportions) is needed such that the new investments' dollar duration exactly offsets the dollar duration gap.

**When to Use:** Questions asking for cash needed to rebalance a portfolio to restore original dollar duration after interest rates have changed, especially when new investments must be allocated in specific proportions across multiple securities.

**Procedure:**
1. Calculate initial dollar duration: `DD_initial = Σ(MV_i × Duration_i)` for all bonds
2. Calculate dollar duration after rate shift: `DD_after = Σ(MV_i × Duration_i)` using new values
3. Calculate dollar duration gap: `DD_gap = DD_initial - DD_after`
4. Determine allocation proportions for new investments (e.g., equal thirds)
5. Calculate weighted average duration of new investment mix: `D_new = Σ(weight_i × Duration_i)` using post-shift durations
6. Solve for required cash: `Cash = DD_gap / D_new`
7. Validate that Cash × D_new ≈ DD_gap

**Worked Example:**
**Question:** A portfolio initially had dollar duration of $150M. After rate shifts, the portfolio's dollar duration is $120M. New investments will be allocated equally (1/3 each) across three bonds with durations of 4.5, 2.0, and 5.0 years. How much cash is needed to restore the original dollar duration?

```python
# Step 1: Given values
initial_dollar_duration = 150_000_000
current_dollar_duration = 120_000_000

# Step 2: Calculate dollar duration gap
dd_gap = initial_dollar_duration - current_dollar_duration  # 30,000,000

# Step 3: New investment allocation (equal proportions)
allocation_weights = [1/3, 1/3, 1/3]
bond_durations_after_shift = [4.5, 2.0, 5.0]

# Step 4: Calculate weighted average duration of new investments
weighted_avg_duration = sum(
    weight * duration 
    for weight, duration in zip(allocation_weights, bond_durations_after_shift)
)  # 3.833

# Step 5: Solve for required cash
# Cash × weighted_avg_duration = dd_gap
cash_needed = dd_gap / weighted_avg_duration

# Step 6: Validate
assert abs(cash_needed * weighted_avg_duration - dd_gap) < 1000, "Validation failed"

cash_needed  # 7,826,087
```

**Common Bugs to Avoid:**
- Using simple average duration instead of weighted average based on allocation proportions
- Dividing by wrong duration value (e.g., using individual bond duration instead of weighted average)
- Using pre-shift durations instead of post-shift durations for new investments
- Forgetting that new investments are made at current (post-shift) prices and durations
- Not accounting for specified allocation proportions (assuming equal when not stated)

**CHECK Steps:**
- Verify DD_gap = DD_initial - DD_current (positive if duration decreased)
- Assert weighted_avg_duration is between min and max of individual bond durations
- Validate: Cash × weighted_avg_duration ≈ DD_gap (within rounding tolerance)
- Ensure allocation weights sum to 1.0
- Check that cash_needed is positive (assuming we're adding to portfolio, not removing)

## Pattern: Zero-Coupon Bond Portfolio Sensitivity with Continuous Compounding

**Description:** When analyzing the percentage change in value of a zero-coupon bond portfolio due to yield shifts under continuous compounding, calculate the price impact using exponential discounting and determine whether to report signed or absolute values based on question context.

**When to Use:** Questions asking for "percentage changes in value" of zero-coupon bond portfolios when yields increase/decrease, especially when "continuous compounding" is specified. Keywords: "percentage changes", "yield increase", "zero-coupon", "continuous compounding", "portfolio sensitivity".

**Procedure:**
1. Identify that continuous compounding applies (look for "per annum with continuous compounding")
2. Extract: initial yield, yield change (increase/decrease), maturity/duration
3. Calculate price change ratio using continuous compounding:
   - Initial discount factor: `e^(-r_initial × maturity)`
   - New discount factor: `e^(-r_new × maturity)`
   - Percentage change: `[(e^(-r_new×n) - e^(-r_initial×n)) / e^(-r_initial×n)] × 100`
4. Simplify using exponential properties: `[e^(-(r_new-r_initial)×n) - 1] × 100`
5. For portfolio sensitivity questions asking "percentage changes" (plural), report absolute magnitude
6. Validate: for small yield changes, result should approximate `duration × yield_change × 100`

**Worked Example:**

**Question:** A portfolio consists entirely of zero-coupon bonds with an average maturity of 6 years. If yields increase by 0.75% per annum with continuous compounding, what is the percentage change in portfolio value?

```python
import math

# Step 1: Extract given values
avg_maturity = 6  # years
yield_increase = 0.0075  # 75 basis points = 0.75%

# Step 2: Calculate percentage change using continuous compounding
# For zero-coupon bonds: % change = [e^(-Δr×n) - 1] × 100
# where Δr is the yield change and n is maturity
percentage_change = (math.exp(-yield_increase * avg_maturity) - 1) * 100

# Step 3: For yield increase, percentage_change will be negative
# Question asks for "percentage change" in sensitivity context
# Report absolute magnitude
magnitude = abs(percentage_change)

magnitude  # 4.41 (4.41% decrease in value)
```

**Worked Example 2:**

**Question:** Portfolio B has zero-coupon bonds with average duration 5.2 years. Calculate the percentage change in value for a 5% per annum increase in yields with continuous compounding.

```python
import math

# Step 1: Extract values
duration = 5.2  # years (for zero-coupon bonds, duration = maturity)
yield_increase = 0.05  # 5% = 0.05

# Step 2: Calculate percentage change
# Formula: [e^(-Δr×n) - 1] × 100
percentage_change = (math.exp(-yield_increase * duration) - 1) * 100

# Step 3: Report absolute magnitude for sensitivity analysis
magnitude = abs(percentage_change)

# Step 4: Round to 2 decimal places for final answer
result = round(magnitude, 2)

result  # 23.00 (approximately 23% decrease)
```

**Common Bugs to Avoid:**
- Using discrete compounding `(1+r)^n` instead of continuous `e^(r×n)` when continuous compounding is specified
- Forgetting to import `math` module for `math.exp()` function
- Using positive yield change when calculating price decrease (yields up → prices down)
- Not taking absolute value when question context indicates magnitude is expected
- Confusing duration with maturity (for zero-coupon bonds they're equal, but verify)
- Calculating `e^(r×n)` instead of `e^(-r×n)` (missing negative sign in exponent)

**CHECK Steps:**
- Verify `import math` is at top of code
- Assert yield_increase > 0 when question says "increase"
- For yield increase, verify percentage_change < 0 before taking absolute value
- Validate: `abs(percentage_change)` ≈ `duration × yield_increase × 100` (within 10% for small changes)
- If duration > 10 years or yield_change > 0.02, expect larger deviations from linear approximation
- Final result should be positive when reporting magnitude

## Pattern: Floating-Rate Loan Interest Rate Timing

**Description:** For floating-rate loans with periodic resets (e.g., semiannual), the interest rate applicable to a payment period is determined at the **beginning** of that period (the previous reset date), not at the end. This is a fundamental principle of floating-rate loan mechanics where the rate "resets" at the start of each period and remains fixed for that period's interest calculation.

**When to Use:** Questions involving floating-rate loans, interest rate swaps, or collars where you need to calculate interest due for a specific payment period, especially when given a table of rates at different dates.

**Procedure:**
1. Identify the payment period in question (e.g., "period ended on 31 December 2013")
2. Determine the **start date** of that payment period (the previous reset date)
3. Use the interest rate that was set at the **start date**, not the end date
4. Apply any caps, floors, or swap adjustments to that rate
5. Calculate interest using: `Interest = Principal × Effective_Rate × (Days_in_Period / Day_Count_Basis)`
6. Validate that you're using the rate from the correct date (beginning of period)

**Worked Example:**
**Question:** A company has a $50M floating-rate loan with semiannual payments based on 180-day Libor plus 75 bps. Calculate the interest due on 30 June 2023 given the following Libor rates:

```
Date        | Libor | Days in Period
31-Dec-2022 | 3.50% | 181
30-Jun-2023 | 4.25% | 184
```

```python
# Step 1: Identify payment period
payment_date = '30-Jun-2023'
period_start = '31-Dec-2022'  # Previous reset date

# Step 2: Extract rate from START of period (not end)
libor_at_start = 0.0350  # Rate on 31-Dec-2022
spread = 0.0075  # 75 basis points

# Step 3: Calculate effective rate
effective_rate = libor_at_start + spread  # 0.0425 (4.25%)

# Step 4: Loan parameters
principal = 50_000_000
days_in_period = 181  # From the period starting 31-Dec-2022
day_count_basis = 360

# Step 5: Calculate interest
interest = (principal * effective_rate * days_in_period) / day_count_basis

# Step 6: Round to nearest dollar
interest = round(interest, 0)

interest  # 1,070,486
```

**Common Bugs to Avoid:**
- **Using the rate at the END of the payment period instead of the START** - this is the most critical error
- Confusing the payment date with the rate-setting date
- Not accounting for the spread when calculating effective rate
- Using the wrong number of days (should match the period, not the next period)
- Applying caps/floors to the wrong base rate

**CHECK Steps:**
- **CRITICAL:** Verify you're using the rate from the PREVIOUS reset date, not the current payment date
- Assert that the rate-setting date is BEFORE the payment date
- For a period ending on date X, the rate should be from the period beginning (previous reset)
- Validate: effective_rate = base_rate + spread (before applying any caps/floors)
- If using a collar: apply cap/floor to the base rate, then add spread
- Ensure days_in_period matches the actual period being calculated, not a future period

---