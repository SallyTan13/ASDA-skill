# SKILL PATTERNS: Fixed Income Unit/Currency/Percent Conversion Errors (PoT)

## Pattern: Spot Rate vs Forward Rate Discounting

**Description:** Confusing forward rates with spot rates when constructing discount factors for multi-period cash flows. Discount factors must use spot rates (or be bootstrapped from forward rates), not directly compound forward rates.

**When to Use:** Swap valuation, bond pricing, or any multi-period discounting problem where forward rates are given but spot rates are needed for present value calculations.

**Procedure:**
1. **Formula:** Discount factor for year n: `DF_n = 1 / (1 + spot_n)^n` where `spot_n` is the n-year spot rate
2. Bootstrap spot rates from forward rates: `(1 + spot_2)^2 = (1 + spot_1) * (1 + forward_1to2)`
3. Apply correct spot rates to discount each cash flow, not forward rates
4. Verify: spot rates should be derived/bootstrapped before discounting

**Code Example:**

**Scenario:** Value a 2-year swap receiving 5% fixed, paying floating on $50M notional. 1-year spot = 2.5%, 1-to-2 year forward = 3.0%.

**Correct Code:**
```python
# Given data
principal = 50_000_000
fixed_rate = 0.05
spot_1y = 0.025
forward_1to2 = 0.030

# Step 1: Bootstrap the 2-year spot rate from forward rate
# (1 + spot_2)^2 = (1 + spot_1) * (1 + forward_1to2)
spot_2y = ((1 + spot_1y) * (1 + forward_1to2)) ** 0.5 - 1

# Step 2: Calculate net cash flows
fixed_cf_year1 = principal * fixed_rate
fixed_cf_year2 = principal * fixed_rate
floating_cf_year1 = principal * spot_1y
floating_cf_year2 = principal * forward_1to2

net_cf_year1 = fixed_cf_year1 - floating_cf_year1
net_cf_year2 = fixed_cf_year2 - floating_cf_year2

# Step 3: Discount using SPOT rates, not forward rates
df_year1 = 1 / (1 + spot_1y)
df_year2 = 1 / (1 + spot_2y) ** 2

# Step 4: Calculate present value
pv_year1 = net_cf_year1 * df_year1
pv_year2 = net_cf_year2 * df_year2

swap_value = pv_year1 + pv_year2
swap_value
```

**Common Bugs to Avoid:**
- Using `df_year2 = 1 / ((1 + spot_1y) * (1 + forward_1to2))` — this compounds forward rates, not spot rates
- Forgetting to bootstrap spot rates before discounting
- Mixing annualized rates with period counts (ensure rate^period alignment)

---

## Pattern: Coupon Payment Calculation (Par vs Market Price)

**Description:** Misinterpreting coupon payments as a percentage of current market price rather than a fixed dollar amount based on par value. Bond coupons are fixed at issuance based on par value, not variable based on trading price.

**When to Use:** Total return calculations, bond valuation, or any problem involving coupon income where both par value and market price are mentioned.

**Procedure:**
1. **Formula:** `Coupon payment = Par value × Coupon rate × Payment frequency`
2. Identify par value (typically $100 or $1,000 unless stated otherwise)
3. If only market price is given, assume par = 100 unless context indicates otherwise
4. Never multiply coupon rate by current market price to get coupon payment
5. Verify: coupon payments should be constant across periods (unless floating rate)

**Code Example:**

**Scenario:** Calculate 1-year total return for a bond with par=$100, 6% annual coupon (paid semiannually), current price=$98, expected price in 1 year=$99, reinvestment rate=1.5% annual.

**Correct Code:**
```python
# Given data
par_value = 100
coupon_rate_annual = 0.06
current_price = 98
ending_price = 99
reinvestment_rate_annual = 0.015

# Step 1: Calculate coupon payments (based on PAR, not market price)
coupon_per_period = par_value * (coupon_rate_annual / 2)  # Semiannual
num_periods = 2
total_coupons = coupon_per_period * num_periods

# Step 2: Reinvestment income on first coupon
reinvestment_rate_semiannual = reinvestment_rate_annual / 2
reinvestment_income = coupon_per_period * reinvestment_rate_semiannual

# Step 3: Price change
price_change = ending_price - current_price

# Step 4: Total dollar return
total_dollar_return = total_coupons + reinvestment_income + price_change

# Step 5: Total return percentage (based on INITIAL INVESTMENT)
total_return_pct = (total_dollar_return / current_price) * 100

total_return_pct
```

**Common Bugs to Avoid:**
- Using `coupon = current_price * coupon_rate` instead of `par_value * coupon_rate`
- Confusing coupon rate with current yield (current yield = annual coupon / market price)
- Forgetting to divide annual coupon rate by payment frequency (e.g., /2 for semiannual)
- Calculating return on par value instead of initial investment (market price)

---

## Pattern: Dollar Duration Rebalancing Algebra

**Description:** Misunderstanding the algebraic relationship between cash investment and dollar duration contribution. When investing cash C in bonds with duration D, the dollar duration added is C × D, so required cash = Target DD / Duration.

**When to Use:** Portfolio rebalancing problems, immunization strategies, or any scenario requiring matching a target dollar duration through new investments.

**Procedure:**
1. **Formula:** `Dollar Duration = Market Value × Duration`
2. Calculate initial total dollar duration: `DD_initial = Σ(MV_i × D_i)`
3. Calculate current total dollar duration after rate shift: `DD_current = Σ(MV_i' × D_i')`
4. Calculate shortfall: `DD_shortfall = DD_initial - DD_current`
5. Calculate weighted average duration of new investments: `D_avg = Σ(weight_i × D_i)`
6. Solve for cash needed: `Cash = DD_shortfall / D_avg`
7. Verify: `Cash × D_avg` should equal `DD_shortfall`

**Code Example:**

**Scenario:** Portfolio has DD=$200,000 initially. After rates shift, current DD=$180,000. Rebalance by investing equally in 3 bonds with durations 3.0, 5.0, 7.0.

**Correct Code:**
```python
# Given data
initial_dd = 200_000
current_dd = 180_000
bond_durations = [3.0, 5.0, 7.0]
weights = [1/3, 1/3, 1/3]  # Equal proportions

# Step 1: Calculate dollar duration shortfall
dd_shortfall = initial_dd - current_dd

# Step 2: Calculate weighted average duration of new investments
avg_duration = sum(w * d for w, d in zip(weights, bond_durations))

# Step 3: Calculate cash needed
# Cash × avg_duration = dd_shortfall
cash_needed = dd_shortfall / avg_duration

# Step 4: Verification
dd_added = cash_needed * avg_duration
verification_check = abs(dd_added - dd_shortfall) < 0.01

cash_needed
```

**Common Bugs to Avoid:**
- Returning `dd_shortfall` directly instead of `dd_shortfall / avg_duration`
- Forgetting to weight durations by investment proportions
- Using simple average instead of weighted average when proportions are unequal
- Sign errors: ensure shortfall is positive when DD needs to increase

---

## Pattern: Weighted Average Duration of Liabilities

**Description:** Incorrectly calculating weighted average duration by using wrong weights, omitting zero-duration items, or inconsistent rounding between code output and reported answer.

**When to Use:** Asset-liability management, duration matching, or any problem requiring calculation of portfolio/liability duration from component durations.

**Procedure:**
1. **Formula:** `Duration_portfolio = Σ(MV_i × D_i) / Σ(MV_i)`
2. Identify ALL liability items (including zero-duration items like demand deposits)
3. Calculate weighted sum: `numerator = Σ(market_value_i × duration_i)`
4. Calculate total market value: `denominator = Σ(market_value_i)`
5. Compute weighted average and round to 2 decimal places for reporting
6. Verify: check that weights sum to 1.0 and result is within reasonable range

**Code Example:**

**Scenario:** Calculate liability duration for: Demand deposits $500M (duration=0), CDs $300M (duration=2.0), Long-term debt $200M (duration=8.5).

**Correct Code:**
```python
# Given data (all values in millions)
liabilities = [
    {'name': 'Demand deposits', 'mv': 500, 'duration': 0.0},
    {'name': 'CDs', 'mv': 300, 'duration': 2.0},
    {'name': 'Long-term debt', 'mv': 200, 'duration': 8.5}
]

# Step 1: Calculate total market value
total_mv = sum(item['mv'] for item in liabilities)

# Step 2: Calculate weighted duration numerator
weighted_duration_sum = sum(item['mv'] * item['duration'] for item in liabilities)

# Step 3: Calculate weighted average duration
duration_liabilities = weighted_duration_sum / total_mv

# Step 4: Round to 2 decimal places for reporting
duration_liabilities_rounded = round(duration_liabilities, 2)

# Step 5: Verification - check weights sum to 1.0
weights = [item['mv'] / total_mv for item in liabilities]
weights_sum = sum(weights)

duration_liabilities_rounded
```

**Common Bugs to Avoid:**
- Excluding zero-duration items from calculation (they still contribute to total MV)
- Inconsistent rounding between code output and narrative explanation
- Using simple average instead of weighted average
- Reporting raw float output instead of rounded value (standard is 2 decimals for duration)
- Forgetting to verify that computed value matches stated answer in explanation

---

## Pattern: Rate Compounding and Period Alignment

**Description:** Misaligning rate compounding frequency with payment periods, or incorrectly converting between annual and periodic rates when calculating cash flows and reinvestment income.

**When to Use:** Any problem involving periodic payments (semiannual, quarterly) where rates are quoted annually but must be applied to sub-annual periods.

**Procedure:**
1. **Formula:** `Periodic rate = Annual rate / Periods per year` (for simple conversion)
2. Identify payment frequency (annual, semiannual, quarterly, monthly)
3. Convert annual rates to periodic rates: divide by frequency
4. Apply periodic rates to periodic cash flows
5. For reinvestment: use the periodic rate for the actual reinvestment period
6. Verify: total periods × periodic rate should align with annual rate × years

**Code Example:**

**Scenario:** Bond pays 8% annual coupon semiannually on $1,000 par. First coupon reinvested for 6 months at 4% annual rate. Calculate total cash after 1 year.

**Correct Code:**
```python
# Given data
par_value = 1000
annual_coupon_rate = 0.08
annual_reinvestment_rate = 0.04
payment_frequency = 2  # Semiannual

# Step 1: Calculate periodic coupon payment
coupon_per_period = par_value * (annual_coupon_rate / payment_frequency)

# Step 2: Calculate periodic reinvestment rate
periodic_reinvestment_rate = annual_reinvestment_rate / payment_frequency

# Step 3: First coupon reinvested for one period
first_coupon_value = coupon_per_period * (1 + periodic_reinvestment_rate)

# Step 4: Second coupon received at end (no reinvestment)
second_coupon_value = coupon_per_period

# Step 5: Total cash from coupons
total_coupon_cash = first_coupon_value + second_coupon_value

total_coupon_cash
```

**Common Bugs to Avoid:**
- Using annual rate directly on periodic cash flows without dividing by frequency
- Confusing "5% semiannual coupon" (meaning 5% per period) vs "5% annual coupon paid semiannually" (meaning 2.5% per period)
- Applying full annual reinvestment rate to partial-year periods
- Mixing compounding conventions (simple vs compound) without clarification

---

## Pattern: Output Format Verification (PoT-Specific)

**Description:** Ensuring code output matches the required format, units, and precision. In PoT mode, the last line must be an expression (not print), and the value must match the scale/units expected by the answer.

**When to Use:** Every PoT solution, especially when answers involve large numbers (millions), percentages, or specific decimal precision.

**Procedure:**
1. Check if answer should be in dollars, millions, percentages, or basis points
2. Apply appropriate scaling (e.g., divide by 1,000,000 for millions)
3. Round to appropriate precision (typically 2 decimals for percentages, whole numbers for dollars)
4. Ensure last line is a variable expression, not `print()`
5. Add verification comment showing expected units

**Code Example:**

**Scenario:** Calculate portfolio value that should be reported in millions of dollars, rounded to 2 decimal places.

**Correct Code:**
```python
# Given data
bond_values = [12_345_678, 23_456_789, 34_567_890]  # in dollars

# Step 1: Calculate total value in dollars
total_value_dollars = sum(bond_values)

# Step 2: Convert to millions (if answer format requires millions)
total_value_millions = total_value_dollars / 1_000_000

# Step 3: Round to appropriate precision
total_value_millions_rounded = round(total_value_millions, 2)

# Step 4: Return as expression (NOT print statement)
# Expected output: value in millions, 2 decimal places
total_value_millions_rounded
```

**Common Bugs to Avoid:**
- Using `print(result)` instead of `result` on last line (PoT requires expression)
- Returning value in wrong units (dollars vs millions, decimal vs percentage)
- Inconsistent precision between code output and narrative explanation
- Forgetting to scale large numbers (e.g., reporting $70,000,000 instead of $70M)
- Not adding verification comments about expected units/format

<budget:usd>
Estimated cost: $0.15 - $0.25 (using GPT-4 tier pricing for detailed technical analysis)
</budget:usd>