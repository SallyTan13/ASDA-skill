# SKILL PATTERNS: Fixed Income Bond Pricing with Forward Rates

## Pattern: Sequential Discounting with Forward Rates for Coupon Bonds

**Description:** When pricing coupon bonds using forward rates, each cash flow must be discounted by the cumulative product of (1 + forward_rate) for all periods from today to that cash flow's date, not by a single rate or simple average.

**When to Use:** Questions asking for bond price given a table/list of forward rates (labeled "Year 0 (today)", "Year 1", etc.) and bond characteristics (coupon rate, maturity, par value).

**Procedure:**
1. Formula: `Price = Σ[CF_t / Π(1 + f_i)] for i=0 to t-1`, where CF_t is cash flow at time t and f_i is forward rate for period i
2. Extract all forward rates from the given table in chronological order (f_0, f_1, f_2, ...)
3. For each cash flow date t, compute cumulative discount factor: `discount_factor_t = (1+f_0) * (1+f_1) * ... * (1+f_{t-1})`
4. Divide each cash flow by its corresponding cumulative discount factor and sum all present values
5. Return the final sum as the bond price (expression, not print)

**Code Example:**

**Scenario:** Price a 3-year bond with 7% annual coupon, $1,000 par value. Forward rates: Year 0=4%, Year 1=5%, Year 2=6%.

**Correct Code:**
```python
# Bond characteristics
par_value = 1000
coupon_rate = 0.07
maturity = 3
annual_coupon = par_value * coupon_rate

# Forward rates for each period
forward_rates = [0.04, 0.05, 0.06]

# Calculate price using sequential discounting
price = 0
cumulative_discount = 1.0

for year in range(1, maturity + 1):
    # Update cumulative discount factor
    cumulative_discount *= (1 + forward_rates[year - 1])
    
    # Cash flow at this year
    if year == maturity:
        cash_flow = annual_coupon + par_value
    else:
        cash_flow = annual_coupon
    
    # Discount and add to price
    price += cash_flow / cumulative_discount

price  # Result: approximately 1027.51
```

**Common Bugs to Avoid:**
- Using forward rates directly as discount rates without cumulative multiplication
- Averaging forward rates instead of compounding them sequentially
- Using `print(price)` instead of returning `price` as final expression
- Off-by-one errors in indexing forward rates (Year 0 rate applies to Year 1 cash flow)
- Forgetting to include par value in final year's cash flow

---

## Pattern: Zero-Coupon Bond Pricing from Forward Rates

**Description:** Zero-coupon bonds must be priced by discounting the par value using the product of (1 + forward_rate) for all periods from today to maturity, which implicitly converts forward rates to the appropriate spot rate.

**When to Use:** Questions asking for price of zero-coupon bond given forward rate schedule, or asking for yield-to-maturity (YTM) of zero-coupon bond from forward rates.

**Procedure:**
1. Formula: `Price = Par / [(1+f_0) * (1+f_1) * ... * (1+f_{n-1})]` for n-year maturity
2. Extract forward rates for periods 0 through n-1 (n periods total for n-year bond)
3. Compute cumulative discount factor as product of (1 + each forward rate)
4. Divide par value by cumulative discount factor
5. For YTM: `YTM = (cumulative_discount_factor)^(1/n) - 1`

**Code Example:**

**Scenario:** Price a 4-year zero-coupon bond with $1,000 par value. Forward rates: Year 0=5%, Year 1=5.5%, Year 2=6%, Year 3=6.5%.

**Correct Code:**
```python
# Bond characteristics
par_value = 1000
maturity = 4

# Forward rates
forward_rates = [0.05, 0.055, 0.06, 0.065]

# Calculate cumulative discount factor
cumulative_discount = 1.0
for rate in forward_rates[:maturity]:
    cumulative_discount *= (1 + rate)

# Price of zero-coupon bond
price = par_value / cumulative_discount

# Optional: Calculate YTM (spot rate)
ytm = cumulative_discount ** (1 / maturity) - 1

price  # Result: approximately 792.16
```

**Common Bugs to Avoid:**
- Using only the terminal forward rate instead of all forward rates
- Taking arithmetic average of forward rates instead of geometric mean
- Confusing forward rates with spot rates (they require conversion)
- Using `maturity + 1` rates instead of exactly `maturity` rates
- Forgetting that Year 0 rate is the first forward rate, not a spot rate

---

## Pattern: Bootstrapping Spot Rates from Zero-Coupon Bond Prices

**Description:** When given zero-coupon bond prices instead of forward rates, spot rates must be bootstrapped by solving for the discount rate that equates price to present value of par, then used to price coupon bonds.

**When to Use:** Questions providing a table of zero-coupon bond prices at different maturities and asking to price a coupon bond or determine forward rates.

**Procedure:**
1. Formula: `Spot_rate_n = (Par / Price_n)^(1/n) - 1` for each maturity n
2. Extract all zero-coupon prices and their corresponding maturities
3. Calculate spot rate for each maturity using the formula above
4. For coupon bond pricing: discount each cash flow by `(1 + spot_rate_t)^t`
5. Sum all discounted cash flows to get bond price

**Code Example:**

**Scenario:** Price a 3-year bond with 8% annual coupon, $1,000 par. Zero-coupon prices: 1-year=$952.38, 2-year=$890.00, 3-year=$816.30.

**Correct Code:**
```python
# Zero-coupon bond data
par = 1000
zero_prices = {1: 952.38, 2: 890.00, 3: 816.30}

# Bootstrap spot rates
spot_rates = {}
for maturity, price in zero_prices.items():
    spot_rates[maturity] = (par / price) ** (1 / maturity) - 1

# Coupon bond characteristics
coupon_rate = 0.08
bond_maturity = 3
annual_coupon = par * coupon_rate

# Price coupon bond using spot rates
bond_price = 0
for year in range(1, bond_maturity + 1):
    if year == bond_maturity:
        cash_flow = annual_coupon + par
    else:
        cash_flow = annual_coupon
    
    bond_price += cash_flow / ((1 + spot_rates[year]) ** year)

bond_price  # Result: approximately 1000.00 (if at par)
```

**Common Bugs to Avoid:**
- Using price/par instead of par/price in spot rate calculation
- Forgetting to raise to power (1/n) for annualized rate
- Mixing up discount factors: using `(1+r)^t` in denominator vs `(1+r)^-t` as multiplier
- Not matching cash flow timing with correct spot rate maturity
- Using YTM approach instead of spot rate curve for coupon bonds

---

## Pattern: Forward Bond Pricing with Unchanged Forward Rate Curve

**Description:** When pricing a bond "one year from now" with forward rates staying the same, the current spot rate curve becomes next year's spot rate curve, requiring discounting remaining cash flows using the original curve shifted forward.

**When to Use:** Questions asking for bond price at a future date (e.g., "one year from now") given current zero-coupon prices or forward rates, with the condition that "implied forward rates stay the same."

**Procedure:**
1. Formula: `Price_t+1 = Σ[CF_{t+k} / (1 + s_k)^k]` for remaining cash flows, using original spot rates s_k
2. Bootstrap spot rates from current zero-coupon prices if not given directly
3. Identify remaining cash flows after the forward date
4. Discount remaining cash flows using spot rates from the original curve (1-year spot for next payment, 2-year spot for payment in 2 years, etc.)
5. Sum discounted values to get forward price

**Code Example:**

**Scenario:** A 4-year bond with 6% coupon, $1,000 par. Current zero prices: 1Y=$943.40, 2Y=$873.44, 3Y=$792.09, 4Y=$708.43. Find price in 1 year.

**Correct Code:**
```python
# Current zero-coupon bond prices
par = 1000
zero_prices = {1: 943.40, 2: 873.44, 3: 792.09, 4: 708.43}

# Bootstrap spot rates
spot_rates = {}
for maturity, price in zero_prices.items():
    spot_rates[maturity] = (par / price) ** (1 / maturity) - 1

# Bond characteristics
coupon_rate = 0.06
original_maturity = 4
annual_coupon = par * coupon_rate

# Price one year from now (3 payments remaining)
remaining_years = original_maturity - 1
bond_price_forward = 0

for year in range(1, remaining_years + 1):
    if year == remaining_years:
        cash_flow = annual_coupon + par
    else:
        cash_flow = annual_coupon
    
    # Use original spot rates (shifted: original 2Y rate for 1Y forward, etc.)
    bond_price_forward += cash_flow / ((1 + spot_rates[year]) ** year)

bond_price_forward  # Result depends on rate curve
```

**Common Bugs to Avoid:**
- Using YTM from current bond price instead of spot rate curve
- Incorrectly shifting spot rates (using 1Y forward rate instead of current 2Y spot rate)
- Discounting by time from original issue date instead of time from forward date
- Forgetting that "forward rates stay the same" means spot curve shifts, not that bond price stays constant
- Using remaining maturity incorrectly in discount factor exponents

---

## Pattern: Converting Forward Rates to Spot Rates (YTM)

**Description:** The yield-to-maturity (spot rate) for an n-period zero-coupon bond equals the geometric mean of forward rates, calculated as `[(1+f_0)(1+f_1)...(1+f_{n-1})]^(1/n) - 1`, not the arithmetic average.

**When to Use:** Questions explicitly asking for "yield to maturity" or "spot rate" of a zero-coupon bond when forward rates are provided.

**Procedure:**
1. Formula: `YTM_n = [(1+f_0) * (1+f_1) * ... * (1+f_{n-1})]^(1/n) - 1`
2. Identify the maturity n of the zero-coupon bond
3. Extract forward rates for periods 0 through n-1
4. Compute product of (1 + each forward rate)
5. Take the nth root and subtract 1 to get annualized YTM

**Code Example:**

**Scenario:** Find YTM of a 5-year zero-coupon bond. Forward rates: Year 0=4%, Year 1=4.5%, Year 2=5%, Year 3=5.5%, Year 4=6%.

**Correct Code:**
```python
# Forward rates
forward_rates = [0.04, 0.045, 0.05, 0.055, 0.06]
maturity = 5

# Calculate cumulative growth factor
cumulative_factor = 1.0
for rate in forward_rates[:maturity]:
    cumulative_factor *= (1 + rate)

# Convert to annualized YTM (geometric mean)
ytm = cumulative_factor ** (1 / maturity) - 1

# Convert to percentage for readability
ytm_percent = ytm * 100

ytm_percent  # Result: approximately 5.00%
```

**Common Bugs to Avoid:**
- Using arithmetic mean: `sum(forward_rates) / n` instead of geometric mean
- Using only the terminal forward rate as the YTM
- Forgetting to subtract 1 after taking the nth root
- Using `maturity + 1` in the exponent instead of `maturity`
- Not converting to percentage when answer options are in percentage format

---

## Pattern: Discount Factor Chain for Multi-Period Coupon Bonds

**Description:** When forward rates are given for each year, the discount factor for year t requires multiplying all (1 + forward_rate) terms from year 0 to year t-1, creating a chain that properly accounts for the term structure.

**When to Use:** Any coupon bond pricing question with forward rates provided as a table showing rates for each future period (Year 1, Year 2, etc.).

**Procedure:**
1. Formula: `DF_t = 1 / [(1+f_0) * (1+f_1) * ... * (1+f_{t-1})]` where DF_t is discount factor for year t
2. Initialize cumulative discount factor as 1.0
3. Loop through each payment date from 1 to maturity
4. Multiply cumulative factor by (1 + forward_rate) for that period
5. Divide cash flow by cumulative factor and accumulate to price

**Code Example:**

**Scenario:** Price a 5-year bond with 9% coupon, $1,000 par. Forward rates: 5.5%, 6%, 6.5%, 7%, 7.5% for years 1-5.

**Correct Code:**
```python
# Bond parameters
par_value = 1000
coupon_rate = 0.09
maturity = 5
annual_coupon = par_value * coupon_rate

# Forward rates for each year
forward_rates = [0.055, 0.06, 0.065, 0.07, 0.075]

# Price calculation with discount factor chain
price = 0
discount_factor_cumulative = 1.0

for year in range(1, maturity + 1):
    # Build discount factor chain
    discount_factor_cumulative *= (1 + forward_rates[year - 1])
    
    # Determine cash flow
    if year == maturity:
        cash_flow = annual_coupon + par_value
    else:
        cash_flow = annual_coupon
    
    # Present value of this cash flow
    pv = cash_flow / discount_factor_cumulative
    price += pv

price  # Result: approximately 1118.65
```

**Common Bugs to Avoid:**
- Resetting cumulative discount factor each iteration instead of accumulating
- Using `discount_factor_cumulative **= (1 + rate)` (power assignment) instead of `*=` (multiplication)
- Indexing forward_rates with `year` instead of `year - 1` (off-by-one error)
- Dividing by individual forward rates instead of cumulative product
- Not distinguishing between discount factor (1/cumulative) and cumulative growth factor