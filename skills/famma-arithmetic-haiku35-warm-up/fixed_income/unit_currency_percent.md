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

**Description:** Pricing a zero-coupon bond requires sequential discounting through each period using the appropriate forward rate for that specific time interval.

**When to Use:** Questions providing forward rate schedules and asking for bond prices at various maturities.

**Procedure:**
1. Formula: `PV = FV / [(1 + f_0) × (1 + f_1) × ... × (1 + f_(n-1))]`
2. Identify the maturity n and face value FV
3. Select forward rates for periods 0 through n-1 (not through n)
4. Compute cumulative discount factor by multiplying all (1 + forward_rate) terms
5. Divide face value by discount factor

**Code Example:**

**Scenario:** Face value $1,000, 4-year maturity. Forward rates: Year 0: 2.5%, Year 1: 3.0%, Year 2: 3.5%, Year 3: 4.0%. Find price.

**Correct Code:**
```python
face_value = 1000
maturity = 4
forward_rates = [0.025, 0.030, 0.035, 0.040]

# Sequential discounting through each period
discount_factor = 1.0
for i in range(maturity):
    discount_factor *= (1 + forward_rates[i])

price = face_value / discount_factor

price  # 873.16
```

**Common Bugs to Avoid:**
- Including the forward rate for year n when pricing an n-year bond (should stop at year n-1)
- Using the wrong sequence of rates (e.g., starting from year 1 instead of year 0)
- Applying rates in wrong order or skipping periods
- Using spot rates instead of forward rates when forward rates are provided

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

**Description:** The yield to maturity of a zero-coupon bond is calculated by solving for the discount rate that equates present value to market price, using the appropriate compounding convention.

**When to Use:** Questions providing zero-coupon bond prices and asking for yields, or requiring bootstrapping of spot rate curves from zero-coupon bond prices.

**Procedure:**
1. Formula (annual compounding): `Price = Face_Value / (1 + YTM)^n`
2. Solve for YTM: `YTM = (Face_Value / Price)^(1/n) - 1`
3. Verify maturity n matches the bond's time to maturity
4. Return as decimal or convert to percentage

**Code Example:**

**Scenario:** 5-year zero-coupon bond, face value $1,000, price $783.50. Calculate YTM.

**Correct Code:**
```python
face_value = 1000
price = 783.50
maturity = 5

# Solve for yield to maturity
ytm = (face_value / price)**(1/maturity) - 1

ytm  # 0.05000 (5.00%)
```

**Common Bugs to Avoid:**
- Using continuous compounding formula when discrete is expected: `ln(FV/P)/n`
- Incorrect exponent: using `n` instead of `1/n` in the power
- Forgetting to subtract 1 after taking the root
- Misidentifying maturity (using issue date instead of remaining time)

---

## Pattern: Percentage vs. Decimal Output Format

**Description:** Financial calculations should maintain values as decimals (0.0525) during computation, but final output format must match the question's expected format (5.25% vs 0.0525) or multiple-choice option format.

**When to Use:** All questions, especially when final answer must be compared to options or when question specifies format like "express as percentage."

**Procedure:**
1. Perform all intermediate calculations in decimal form (0.05 not 5)
2. Before final return, check question for format clues: "%" symbol, option format
3. If options show percentages (5.25%), multiply decimal by 100
4. If options show decimals (0.0525), keep as decimal
5. Ensure final expression returns the correctly formatted value

**Code Example:**

**Scenario:** Calculated yield is 0.06234. Options are: A. 6.15%, B. 6.23%, C. 6.45%.

**Correct Code:**
```python
# Calculation produces decimal
calculated_yield = 0.06234

# Options are in percentage format, so convert
yield_as_percentage = calculated_yield * 100  # 6.234

# For multiple choice matching
options = {'A': 6.15, 'B': 6.23, 'C': 6.45}
# Compare yield_as_percentage to options

# Final answer format
yield_as_percentage  # 6.234 (to match option format)
```

**Common Bugs to Avoid:**
- Returning 0.0623 when options show 6.23%
- Returning 6.23 when options show 0.0623
- Mixing formats during calculation (some steps in %, some in decimal)
- Using print() instead of expression for final value

---

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