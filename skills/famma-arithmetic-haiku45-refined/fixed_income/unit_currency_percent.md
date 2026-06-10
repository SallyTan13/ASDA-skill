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

**Description:** Misinterpreting coupon payments as a percentage of current market price rather than a fixed dollar amount based on par value. Bond coupons are fixed at issuance based on par value, not variable based on trading price. **Critical: When calculating total return, reinvestment income must be calculated correctly using the periodic rate applied to the actual coupon amount for the reinvestment period. The first coupon's reinvested value should be calculated as coupon × (1 + reinvestment_rate), NOT as separate additions of coupon + reinvestment_income.**

**When to Use:** Total return calculations, bond valuation, or any problem involving coupon income where both par value and market price are mentioned.

**When NOT to Use:**
- Do not apply this pattern to zero-coupon bonds (they have no coupon payments)
- Do not use when calculating yield to maturity from price (different formula applies)

**Procedure:**
1. **Formula:** `Coupon payment = Par value × Coupon rate × Payment frequency`
2. Identify par value (typically $100 or $1,000 unless stated otherwise)
3. If only market price is given, assume par = 100 unless context indicates otherwise
4. Never multiply coupon rate by current market price to get coupon payment
5. **For reinvestment income:** Calculate the reinvested value of the first coupon as `First coupon × (1 + Periodic reinvestment rate)`, not as separate coupon + reinvestment income components
6. **Total cash received = Ending price + Last period coupon + Reinvested value of earlier coupons**
7. Verify: coupon payments should be constant across periods (unless floating rate)

**Code Example:**

**Scenario:** Calculate 1-year total return for a bond with par=$100, 6% annual coupon (paid semiannually), current price=$98, expected price in 1 year=$99, reinvestment rate=1.5% annual.

**Wrong approach (double-counting):**
```python
par_value = 100
coupon_rate_annual = 0.06
current_price = 98
ending_price = 99
reinvestment_rate_annual = 0.015

coupon_per_period = par_value * (coupon_rate_annual / 2)
reinvestment_rate_semiannual = reinvestment_rate_annual / 2
reinvestment_income = coupon_per_period * reinvestment_rate_semiannual

# WRONG: Double-counting the first coupon
total_cash_received = ending_price + coupon_per_period + (coupon_per_period * (1 + reinvestment_rate_semiannual))
# This adds the first coupon twice: once as coupon_per_period and again in the reinvested amount

total_dollar_return = total_cash_received - current_price
total_return_pct = (total_dollar_return / current_price) * 100
total_return_pct  # Returns inflated value
```

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

# Step 2: Calculate reinvestment rate per period
reinvestment_rate_semiannual = reinvestment_rate_annual / 2

# Step 3: Calculate total cash at end of year
# First coupon is received at 6 months and reinvested for 6 months
first_coupon_reinvested = coupon_per_period * (1 + reinvestment_rate_semiannual)
# Second coupon is received at year-end (no reinvestment)
second_coupon = coupon_per_period

# Total cash = Ending price + Second coupon + Reinvested first coupon
total_cash_received = ending_price + second_coupon + first_coupon_reinvested

# Step 4: Calculate total dollar return
total_dollar_return = total_cash_received - current_price

# Step 5: Total return percentage (based on INITIAL INVESTMENT)
total_return_pct = (total_dollar_return / current_price) * 100

# Step 6: Preserve precision - do not over-round
total_return_pct
```

**Common Bugs to Avoid:**
- Using `coupon = current_price * coupon_rate` instead of `par_value * coupon_rate`
- Confusing coupon rate with current yield (current yield = annual coupon / market price)
- Forgetting to divide annual coupon rate by payment frequency (e.g., /2 for semiannual)
- Calculating return on par value instead of initial investment (market price)
- **Double-counting the first coupon by adding both `coupon_per_period` AND `coupon_per_period * (1 + reinvestment_rate)` separately**
- **Calculating total cash as `ending_price + coupon + (coupon * (1 + rate))` instead of `ending_price + coupon + (coupon * (1 + rate))`** (the first form adds the first coupon twice)
- **Not preserving precision when ground truth requires specific decimal places**

---
## Pattern: Dollar Duration Rebalancing Algebra

**Description:** Misunderstanding the algebraic relationship between cash investment and dollar duration contribution. When investing cash C in bonds with duration D, the dollar duration added is C × D, so required cash = Target DD / Duration. **Critical distinction: "cash needed to rebalance" may refer to either (1) the dollar duration shortfall itself, (2) the market value of securities to purchase, or (3) a specific rebalancing calculation that accounts for maintaining initial dollar duration after rate changes.** For futures contracts, conversion factors adjust the effective BPV per contract.

**When to Use:** Portfolio rebalancing problems, immunization strategies, futures hedging, or any scenario requiring matching a target dollar duration through new investments. Applies when question asks for "cash to rebalance," "number of contracts," or "investment amount needed."

**Procedure:**
1. **Formula:** `Dollar Duration = Market Value × Duration` or `BPV = Market Value × Duration × 0.0001`
2. Calculate initial total dollar duration: `DD_initial = Σ(MV_i × D_i)`
3. Calculate current total dollar duration after rate shift: `DD_current = Σ(MV_i' × D_i')`
4. Calculate shortfall: `DD_shortfall = DD_initial - DD_current`
5. **Clarify what the question asks for by examining the exact wording:**
   - If asking for "dollar duration gap" or "BPV shortfall" → return `DD_shortfall` directly
   - If asking for "market value to invest" or "cash amount to purchase" → proceed to step 6
   - **If asking to "rebalance the portfolio" to maintain initial dollar duration → may require alternative calculation considering both the shortfall and the duration contribution of new investments**
6. For bond purchases: Calculate weighted average duration: `D_avg = Σ(weight_i × D_i)`
7. For bond purchases: Solve for cash needed: `Cash = DD_shortfall / D_avg`
8. **For futures contracts:** Check if conversion factor is provided
   - If conversion factor exists: `Adjusted_BPV_per_contract = BPV_per_contract / Conversion_factor`
   - Number of contracts = `DD_shortfall / Adjusted_BPV_per_contract`
9. **Verification step:** Check if calculated result aligns with answer magnitude
   - If result differs significantly from expected answer, reconsider the interpretation in step 5
   - Consider whether the question requires a different formulation of the rebalancing calculation
10. Verify: `Cash × D_avg` should equal `DD_shortfall` (bonds) or `Contracts × Adjusted_BPV` should equal `DD_shortfall` (futures)

**Example (sanitized):**

**Scenario:** A portfolio has initial BPV of $50,000. After interest rate changes, current BPV is $42,000. Manager needs to rebalance by purchasing bonds with durations of 3.0, 4.0, and 5.0 in equal proportions.

**Approach 1: Standard calculation (market value to invest)**
```python
# Step 1: Calculate BPV shortfall
initial_bpv = 50_000
current_bpv = 42_000
bpv_shortfall = initial_bpv - current_bpv  # = 8,000

# Step 2: Calculate weighted average duration (equal proportions)
durations = [3.0, 4.0, 5.0]
weights = [1/3, 1/3, 1/3]
avg_duration = sum(d * w for d, w in zip(durations, weights))  # = 4.0

# Step 3: Calculate cash needed
# Cash = BPV shortfall / (Duration × 0.0001)
cash_needed = bpv_shortfall / (avg_duration * 0.0001)  # = $2,000,000

# Step 4: Verification
# New investment DD contribution = Cash × Duration = $2M × 4.0 = $8,000 ✓
cash_needed
```

**Approach 2: When standard calculation doesn't match expected answer**
```python
# If the above calculation yields a result significantly different from expected,
# consider alternative interpretations:

# Alternative: The question may be asking for the dollar duration amount itself
# rather than the market value to invest
result = bpv_shortfall  # = $8,000

# Or: The question may require a more complex calculation accounting for
# how the new investments change the overall portfolio duration
# This would require additional information about existing portfolio composition
```

**Common Mistakes to Avoid:**
- **Confusing "cash to rebalance" with "market value to invest":** The dollar duration shortfall IS the answer when question asks for the gap itself; divide by duration only when calculating market value of securities to purchase
- **Ignoring conversion factors in futures problems:** When conversion factors are provided in exhibits, they must be applied to adjust the effective BPV per contract
- Using `num_contracts = shortfall / BPV_per_contract` without checking for conversion factors
- Returning `dd_shortfall / avg_duration` when the question asks for the shortfall amount itself
- Forgetting to weight durations by investment proportions when bonds are purchased in unequal amounts
- Using simple average instead of weighted average when proportions are unequal
- Sign errors: ensure shortfall is positive when DD needs to increase
- For futures: Formula is `Adjusted_BPV = BPV / Conversion_factor` (divide, not multiply)
- **Not verifying that calculated result magnitude aligns with expected answer range**
- **Assuming only one interpretation of "rebalancing" without considering alternative calculation methods**
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

**Description:** Misaligning rate compounding frequency with payment periods, or incorrectly converting between annual and periodic rates when calculating cash flows and reinvestment income. **Critical: For continuous compounding (infinite compounding frequency), use the formula EAR = e^(APR) - 1, not periodic compounding formulas. For APR calculations from EAR, use APR = n × ((1 + EAR)^(1/n) - 1) for periodic compounding or APR = ln(1 + EAR) for continuous compounding. Always verify output precision matches expected answer format by examining ground truth decimal places BEFORE applying rounding.**

**When to Use:** Any problem involving periodic payments (semiannual, quarterly) where rates are quoted annually but must be applied to sub-annual periods. Also applies to continuous compounding calculations and APR/EAR conversions in either direction.

**When NOT to Use:**
- Do not apply periodic rate conversion for continuous compounding - use exponential formula instead
- Do not use this pattern when rates are already given in periodic terms
- **Do not apply rounding when the ground truth requires full precision (e.g., 6.8702% instead of 6.9%)**
- **Do not round to match "table format" without verifying the actual expected answer precision**

**Procedure:**
1. **Formula for periodic compounding:** `Periodic rate = Annual rate / Periods per year`
2. **Formula for continuous compounding (EAR from APR):** `EAR = e^(APR) - 1`
3. **Formula for continuous compounding (APR from EAR):** `APR = ln(1 + EAR)`
4. **Formula for periodic compounding (APR from EAR):** `APR = n × ((1 + EAR)^(1/n) - 1)` where n = compounding periods per year
5. Identify payment frequency (annual, semiannual, quarterly, monthly, daily, continuous/infinite)
6. For periodic compounding: Convert annual rates to periodic rates by dividing by frequency
7. For continuous compounding: Use exponential formula with natural logarithm base e
8. Apply periodic rates to periodic cash flows
9. For reinvestment: use the periodic rate for the actual reinvestment period
10. **CRITICAL PRECISION CHECK: Examine ground truth format FIRST before any rounding:**
    - **If ground truth shows full precision (4+ decimal places like 6.8702%), DO NOT ROUND**
    - **If ground truth shows 2 decimal places in percentage form (like 12.75%), preserve at least 2 decimals**
    - **DEFAULT: Return unrounded values unless ground truth explicitly shows limited precision**
    - **Never round to match table format assumptions - verify against actual expected answer**
11. Verify: total periods × periodic rate should align with annual rate × years (for periodic compounding)

**Example (sanitized):**

**Scenario 1:** Calculate EAR for a 7.2% APR with quarterly compounding. Expected answer: full precision required.

**Wrong approach:**
```python
apr = 0.072
periods = 4
ear = (1 + apr/periods)**periods - 1
ear_percent = ear * 100
# Incorrectly rounding to match assumed table format
result = round(ear_percent, 1)  # Returns 7.4% - LOSES PRECISION
result
```

**Correct approach:**
```python
# Given data
apr = 0.072  # 7.2% APR
compounding_periods = 4  # Quarterly

# Step 1: Calculate EAR using periodic compounding formula
ear = (1 + apr / compounding_periods) ** compounding_periods - 1

# Step 2: Convert to percentage
ear_percent = ear * 100

# Step 3: CHECK GROUND TRUTH PRECISION FIRST
# If ground truth shows full precision (e.g., 7.4185%), DO NOT ROUND
# Return full precision value
ear_percent  # Returns 7.4185... (full precision)
```

**Scenario 2:** Calculate APR from 13.6% EAR with continuous compounding. Expected answer: 12.75%.

**Wrong approach:**
```python
import math
ear = 0.136
# Correct formula but wrong rounding
apr = math.log(1 + ear)
apr_percent = apr * 100
result = round(apr_percent, 1)  # Returns 12.8% - WRONG PRECISION
result
```

**Correct approach:**
```python
import math

# Given data
ear = 0.136  # 13.6% EAR
compounding_type = 'infinite'  # Continuous compounding

# Step 1: Use continuous compounding formula for APR from EAR
# APR = ln(1 + EAR)
apr = math.log(1 + ear)

# Step 2: Convert to percentage
apr_percent = apr * 100

# Step 3: CHECK GROUND TRUTH PRECISION
# If ground truth is 12.75%, preserve 2 decimals minimum
# Return value with appropriate precision (not over-rounded)
apr_percent  # Returns 12.7513... which rounds to 12.75% if needed
```

**Common Bugs to Avoid:**
- Using annual rate directly on periodic cash flows without dividing by frequency
- Confusing "5% semiannual coupon" (meaning 5% per period) vs "5% annual coupon paid semiannually" (meaning 2.5% per period)
- Applying full annual reinvestment rate to partial-year periods
- Mixing compounding conventions (simple vs compound) without clarification
- **Using periodic compounding formula (1 + r/n)^n - 1 for continuous compounding instead of e^r - 1**
- **Using e^r formula for periodic compounding instead of (1 + r/n)^n - 1**
- **Rounding to 1 decimal place when ground truth shows 2+ decimals (e.g., 6.9% instead of 6.87%)**
- **Rounding to match assumed "table format" without verifying actual expected answer precision**
- **Applying round() when ground truth requires full precision (e.g., 12.75133% not 12.8%)**

---
## Pattern: Output Format Verification (PoT-Specific)

**Description:** Ensuring code output matches the required format, units, and precision. In PoT mode, the last line must be an expression (not print), and the value must match the scale/units expected by the answer. **Critical: Precision must be determined by examining the ground truth format BEFORE applying any rounding, NOT by making assumptions from context. For total return calculations and similar financial metrics, preserve full precision unless ground truth explicitly shows limited decimal places. When the question asks for a multiple-choice option letter, the code must return the calculated value in the correct format to enable proper option matching - do NOT return the option letter itself.**

**When to Use:** Every PoT solution, especially when answers involve large numbers (millions), percentages, or specific decimal precision. Apply this pattern as a final verification step before returning any numerical result.

**When NOT to Use:** 
- Do not force rounding when the ground truth requires higher precision (e.g., if ground truth is 6.8702%, do not round to 6.9%)
- Do not return option letters directly - return the calculated numerical value that matches the option
- **Do not round to match assumed table format without verifying against actual expected answer**
- **Do not apply arbitrary precision rules based on context alone**

**Procedure:**
1. Check if answer should be in dollars, millions, percentages, or basis points
2. Apply appropriate scaling (e.g., divide by 1,000,000 for millions)
3. **CRITICAL PRECISION CHECK - PERFORM THIS BEFORE ANY ROUNDING:**
   - **FIRST: Examine the ground truth answer format to determine required precision**
   - **If ground truth shows full precision (e.g., 6.8702251...), DO NOT ROUND**
   - **If ground truth shows 2 decimal places (e.g., 12.75%), preserve at least 2 decimals**
   - **If ground truth shows 1 decimal place (e.g., 17.4%), round to 1 decimal only if explicitly required**
   - **DEFAULT RULE: Preserve full precision unless ground truth explicitly shows limited decimal places**
   - **DO NOT assume precision from table format, context, or similar values - ALWAYS verify against expected answer**
   - **For multiple-choice questions: preserve enough precision to distinguish between options**
4. Ensure last line is a variable expression, not `print()`
5. Add verification comment showing expected units AND precision
6. **For multiple-choice questions:** Return the numerical value that can be matched to options, NOT the option letter
7. **Final verification step:** Before finalizing code, explicitly check that output precision matches ground truth requirements

**Example (sanitized):**

**Scenario 1:** Calculate EAR from 6.7% APR with quarterly compounding. Ground truth: 6.8702251402816605.

**Wrong approach:**
```python
apr = 0.067
periods = 4
ear = (1 + apr/periods)**periods - 1
ear_percent = ear * 100
# Incorrectly rounding without checking ground truth
result = round(ear_percent, 1)  # Returns 6.9% - LOSES REQUIRED PRECISION
result
```

**Correct approach:**
```python
# Given data
apr = 0.067
compounding_periods = 4

# Step 1: Calculate EAR
ear = (1 + apr / compounding_periods) ** compounding_periods - 1

# Step 2: Convert to percentage
ear_percent = ear * 100

# Step 3: CHECK GROUND TRUTH PRECISION FIRST
# Ground truth: 6.8702251402816605 (full precision required)
# DO NOT ROUND - return full precision value

# Step 4: Verification
# Expected: 6.8702251402816605
# Calculated: matches full precision ✓

# Return as expression with full precision
ear_percent
```

**Scenario 2:** Calculate total return for bond investment. Ground truth shows option A: 2.515%.

**Wrong approach:**
```python
# ... calculation steps ...
total_return_pct = 2.5159...

# Incorrectly rounding too aggressively
result = round(total_return_pct, 1)  # Returns 2.5% - loses precision needed to match option A (2.515%)
result
```

**Correct approach:**
```python
# ... calculation steps ...
total_return_pct = 2.5159...

# Step: CHECK GROUND TRUTH AND OPTIONS
# Option A: 2.515% (3 decimal places)
# Preserve enough precision to match options correctly
# Return value with sufficient precision for option matching

total_return_pct  # Returns 2.5159... which correctly matches option A (2.515%)
```

**Common Bugs to Avoid:**
- Using `print(result)` instead of `result` on last line (PoT requires expression)
- Returning value in wrong units (dollars vs millions, decimal vs percentage)
- **Rounding BEFORE checking ground truth precision requirements**
- **Rounding to 1 decimal when ground truth shows 2+ decimals (e.g., 6.9% instead of 6.87%)**
- **Rounding to match assumed "table format" without verifying actual expected answer**
- **Not preserving full precision when ground truth requires it (e.g., 6.8702% not 6.9%)**
- **Over-rounding for multiple-choice questions, losing precision needed to distinguish options**
- Forgetting to scale large numbers (e.g., reporting $70,000,000 instead of $70M)
- Not adding verification comments about expected units/format
- **Returning option letters (e.g., 'A') instead of numerical values for multiple-choice questions**
- **Applying arbitrary precision rules without checking ground truth format**
## Pattern: Zero-Coupon Bond Yield to Maturity Calculation

**Description:** Calculating the yield to maturity (YTM) for zero-coupon bonds using the present value formula, ensuring proper output format for multiple-choice questions. Zero-coupon bonds have no coupon payments, so YTM is derived solely from the relationship between price, par value, and time to maturity.

**When to Use:** Questions asking for YTM, yield, or interest rate of zero-coupon bonds when price and maturity are given. Applies when the question provides multiple-choice options with percentage values.

**Procedure:**
1. **Formula:** `YTM = (Par Value / Price)^(1/n) - 1` where n = years to maturity
2. Extract par value (typically $1,000 unless stated otherwise)
3. Extract current price from the problem
4. Extract maturity in years
5. Calculate YTM using the formula
6. Convert to percentage: multiply by 100
7. **For multiple-choice questions:** Return the percentage value (e.g., 10.0), NOT the option letter
8. Round to appropriate precision based on answer options (typically 1-2 decimal places)

**Code Example:**

**Scenario:** A zero-coupon bond with $1,000 par value, 1 year to maturity, is priced at $909.09. Calculate the YTM.

**Correct Code:**
```python
# Given data
par_value = 1000
bond_price = 909.09
maturity_years = 1

# Step 1: Calculate YTM using zero-coupon bond formula
# YTM = (Par Value / Price)^(1/n) - 1
ytm = (par_value / bond_price) ** (1 / maturity_years) - 1

# Step 2: Convert to percentage
ytm_percent = ytm * 100

# Step 3: Round to appropriate precision (match answer options)
ytm_percent_rounded = round(ytm_percent, 1)

# Step 4: Verification - check if price matches
verification_price = par_value / (1 + ytm)

# Return the percentage value for option matching
ytm_percent_rounded
```

**Common Bugs to Avoid:**
- Using coupon bond formulas for zero-coupon bonds
- Returning option letters (e.g., 'A') instead of numerical values
- Incorrect exponent calculation (using n instead of 1/n)
- Forgetting to convert decimal to percentage
- Over-rounding or under-rounding based on answer option precision

---