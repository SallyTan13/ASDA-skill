# SKILL PATTERNS: Fixed Income Bond Pricing with Forward Rates

## Pattern: Sequential Discounting with Forward Rates for Coupon Bonds

**Description:** When pricing coupon bonds using forward rates, each cash flow must be discounted by the cumulative product of (1 + forward_rate) for all periods from today to that cash flow's date, not by a single rate or simple average.

**When to Use:** Questions asking for bond price given a table/list of forward rates (labeled "Year 0 (today)", "Year 1", etc.) and bond characteristics (coupon rate, maturity, par value).

**When NOT to Use:** 
- Questions asking for coupon rate needed to issue a bond at par (use YTM = coupon rate principle instead)
- Questions providing only current bond prices and yields without explicit forward rate schedules
- Questions about bond pricing where market yield/YTM is directly stated rather than derived from forward rates

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
- **Applying this pattern to questions asking for coupon rate to issue at par (use coupon = YTM principle instead)**

---
## Pattern: Zero-Coupon Bond Pricing from Forward Rates

**Description:** Zero-coupon bonds must be priced by discounting the par value using the product of (1 + forward_rate) for all periods from today to maturity, which implicitly converts forward rates to the appropriate spot rate. Critical: carefully extract the bond's maturity from the question text and use exactly that many forward rates.

**When to Use:** Questions asking for price of zero-coupon bond given forward rate schedule, or asking for yield-to-maturity (YTM) of zero-coupon bond from forward rates. Question will specify maturity (e.g., "3-year zero-coupon bond," "zero-coupon bond maturing in 5 years").

**Procedure:**
1. **Extract maturity from question:** Parse question text to identify bond term (e.g., "3-year zero-coupon bond" → maturity = 3)
2. **Verify forward rate availability:** Confirm you have at least `maturity` forward rates available (Year 0 through Year maturity-1)
3. Formula: `Price = Par / [(1+f_0) * (1+f_1) * ... * (1+f_{n-1})]` for n-year maturity
4. Compute cumulative discount factor as product of (1 + each forward rate) for exactly n periods
5. Divide par value by cumulative discount factor
6. **Validation check:** Verify `len(forward_rates[:maturity]) == maturity` before calculation

**Example (sanitized):**
> **Scenario:** Given forward rates for Years 0-4 are [3%, 3.5%, 4%, 4.5%, 5%], price a 3-year zero-coupon bond with $1,000 par value.
> 
> **Wrong approach:** Seeing 5 forward rates available and using all 5, or misreading "3-year" as requiring 4 rates (Year 0 through Year 3).
> 
> **Correct approach:**
> 1. Extract maturity: "3-year zero-coupon bond" → maturity = 3
> 2. Select forward rates: Use rates for Year 0, Year 1, Year 2 only (first 3 rates)
> 3. Cumulative discount = (1.03) × (1.035) × (1.04) = 1.1093
> 4. Price = $1,000 / 1.1093 = $901.58
> 5. Validation: Used exactly 3 rates for 3-year bond ✓

**Code Example:**

**Scenario:** Price a 3-year zero-coupon bond with $1,000 par value. Forward rates: Year 0=4%, Year 1=4.5%, Year 2=5%, Year 3=5.5%.

**Correct Code:**
```python
# Bond characteristics - EXTRACT FROM QUESTION
par_value = 1000
maturity = 3  # "3-year zero-coupon bond"

# Forward rates available
forward_rates = [0.04, 0.045, 0.05, 0.055]

# Validation check
assert len(forward_rates) >= maturity, "Insufficient forward rates"

# Calculate cumulative discount factor using EXACTLY maturity rates
cumulative_discount = 1.0
for rate in forward_rates[:maturity]:  # Only first 3 rates
    cumulative_discount *= (1 + rate)

# Price of zero-coupon bond
price = par_value / cumulative_discount

# Optional: Calculate YTM (spot rate)
ytm = cumulative_discount ** (1 / maturity) - 1

price  # Result: approximately 905.95
```

**Common Bugs to Avoid:**
- **Misreading bond maturity from question text** (e.g., seeing 4 forward rates and assuming 4-year bond when question asks for 3-year)
- Using all available forward rates instead of exactly `maturity` rates
- Off-by-one errors: using Year 0 through Year n (n+1 rates) instead of Year 0 through Year n-1 (n rates)
- Not validating that maturity variable matches the question's stated term
- Using only the terminal forward rate instead of all forward rates up to maturity
- Confusing forward rates with spot rates (they require conversion via cumulative product)
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

**Description:** When pricing a bond at a future date (e.g., "one year from now") with forward rates staying the same, you must first extract the implied forward rates from the current spot curve, then use those forward rates to discount the remaining cash flows. The key insight is that "unchanged forward rates" means the forward rates embedded in today's curve become the spot rates for discounting future cash flows.

**When to Use:** Questions asking for bond price at a future date (e.g., "one year from now," "two years from now") given current zero-coupon prices or forward rates, with the condition that "implied forward rates stay the same" or "forward rates remain unchanged."

**Procedure:**
1. Bootstrap spot rates from current zero-coupon prices if not given directly: `s_n = (Par / Price_n)^(1/n) - 1`
2. Extract forward rates from spot curve using: `(1+s_n)^n = (1+s_m)^m × (1+f_{m,n})^{n-m}`, solving for `f_{m,n}`
3. For pricing t years forward, extract forward rates f_{t,t+1}, f_{t,t+2}, ..., f_{t,maturity}
4. Discount remaining cash flows using these forward rates as the new spot curve
5. Sum discounted values to get forward price

**Example (sanitized):**
> **Scenario:** A 5-year bond with 8% annual coupon, $1,000 par. Current zero prices: 1Y=$950, 2Y=$890, 3Y=$820, 4Y=$750, 5Y=$680. Find price in 2 years if forward rates stay the same.
> 
> **Wrong approach:** Using the original 1Y, 2Y, 3Y spot rates directly to discount the 3 remaining payments. This incorrectly assumes spot rates stay constant rather than forward rates staying constant.
> 
> **Correct approach:**
> 1. Bootstrap spot rates: s_1=5.26%, s_2=6.01%, s_3=6.82%, s_4=7.46%, s_5=8.03%
> 2. Extract forward rates for years 2-5:
>    - f_{2,3}: (1.0682)³ / (1.0601)² = 1.0845, so f_{2,3} = 8.45%
>    - f_{2,4}: (1.0746)⁴ / (1.0601)² = (1 + f_{2,4})², so f_{2,4} = 8.93% (annualized)
>    - f_{2,5}: (1.0803)⁵ / (1.0601)² = (1 + f_{2,5})³, so f_{2,5} = 9.06% (annualized)
> 3. These forward rates become the spot curve 2 years forward
> 4. Discount 3 remaining payments:
>    - Year 3 payment: $80 / 1.0845 = $73.78
>    - Year 4 payment: $80 / (1.0845 × 1.0933) = $67.48
>    - Year 5 payment: $1,080 / (1.0845 × 1.0933 × 1.0980) = $830.21
> 5. Price in 2 years = $971.47

**Common Mistakes to Avoid:**
- Using original spot rates directly instead of extracting forward rates first
- Confusing "unchanged forward rates" with "unchanged spot rates" or "unchanged bond price"
- Incorrectly calculating forward rates (forgetting to take proper roots for multi-period forwards)
- Using time from original issue date instead of time from forward pricing date
- Not recognizing that forward rates f_{t,t+k} become the k-period spot rate at time t

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

## Pattern: Holding Period Return with Yield Curve Forecast Change

**Description:** When calculating expected return over a holding period where the yield curve is forecasted to change (e.g., "yield curve will be flat at X%"), you must: (1) price the bond today using current rates, (2) price the bond at horizon using the NEW forecasted rates, (3) calculate return including coupon income received during the period.

**When to Use:** Questions asking for "expected rate of return," "holding period return," or "total return" when a future yield curve scenario is specified (e.g., "yield curve will be flat at 7%," "all rates will shift to X%"), distinct from scenarios where forward rates stay unchanged.

**Procedure:**
1. Calculate current bond price using current spot rates or forward rates
2. Identify cash flows during holding period (coupons received)
3. Calculate bond price at end of holding period using the FORECASTED new yield curve (not current rates)
4. For flat yield curve forecast at rate r, discount all remaining payments by (1+r)^t where t is years from horizon date
5. Calculate holding period return: `HPR = (Price_end + Coupons_received - Price_start) / Price_start`

**Example (sanitized):**
> **Scenario:** You own a 4-year bond with 6% annual coupon, $1,000 par, currently priced at $980. You forecast the yield curve will be flat at 5.5% in 1 year. What is your expected 1-year return?
> 
> **Wrong approach:** Calculating price in 1 year using current forward rates, or incorrectly compounding the flat rate multiple times for the same cash flow.
> 
> **Correct approach:**
> 1. Current price = $980 (given)
> 2. Coupon received during year = $60
> 3. In 1 year, 3 payments remain: $60, $60, $1,060
> 4. Price in 1 year using flat 5.5% curve:
>    - PV = $60/1.055 + $60/(1.055)² + $1,060/(1.055)³
>    - PV = $56.87 + $53.91 + $902.63 = $1,013.41
> 5. HPR = ($1,013.41 + $60 - $980) / $980 = 9.53%
> 
> Key insight: Each remaining payment is discounted from its payment date using the NEW flat rate, not accumulated using the old forward curve.

**Common Mistakes to Avoid:**
- Using unchanged forward rates when question specifies a yield curve forecast change
- Incorrectly initializing discount factors (e.g., starting with 1.055 then multiplying again)
- Forgetting to include coupon income received during the holding period in return calculation
- Confusing "price in 1 year" calculation with "1-year forward price" under unchanged rates
- Using current yield curve instead of forecasted yield curve for horizon price

---

## Pattern: Par Value Bond Issuance - Coupon Equals Yield

**Description:** When a bond is issued at par value (price = 100% of face value), the coupon rate must equal the market's required yield-to-maturity (YTM). This is a fundamental bond pricing principle: par bonds have coupon rates equal to their discount rates.

**When to Use:** Questions asking "what coupon rate would be needed to issue a bond at par" or "what coupon rate for a par value bond" given market yield information from comparable bonds.

**When NOT to Use:**
- Questions asking to price a bond given its coupon rate (use discounting patterns instead)
- Questions about bonds trading above or below par
- Questions requiring forward rate calculations or spot rate bootstrapping

**Procedure:**
1. Identify that question asks for coupon rate to achieve par value issuance
2. Locate the market's required yield (YTM) for bonds of similar maturity and credit quality
3. Extract YTM from comparable bonds in the market (may be explicitly stated or implied from existing bond data)
4. Set coupon rate = YTM (this ensures price = par)
5. Return the YTM as the required coupon rate

**Example (sanitized):**
> **Scenario:** A company has an existing 20-year bond trading at 95% of par with 8% coupon and 8.7% YTM. What coupon rate should a new 15-year bond carry to be issued at par?
> 
> **Wrong approach:** Interpolating between different bond types, using complex forward rate calculations, or averaging existing coupon rates. These ignore the fundamental principle that par bonds have coupon = YTM.
> 
> **Correct approach:**
> 1. Recognize this is a par issuance question (not a pricing question)
> 2. Identify the market's required yield for similar maturity: 8.7% YTM from the 20-year bond
> 3. For a 15-year bond of similar credit quality, use the comparable YTM as approximation
> 4. Set coupon rate = 8.7% (or the closest market-observed YTM for that maturity)
> 5. Result: Coupon rate ≈ 8.7%
> 
> Key insight: Par value bonds always have coupon rate = YTM. No complex discounting needed.

**Code Example:**

**Scenario:** Given an existing 18-year bond with 7.5% coupon trading at 92% of par with 8.4% YTM, determine the coupon rate for a new 12-year bond to be issued at par.

**Correct Code:**
```python
# Market data from comparable bonds
existing_bond_ytm = 0.084  # 8.4% YTM from 18-year bond

# For par issuance: coupon rate = required yield
# Use the market YTM as the required yield for similar credit quality
required_coupon_rate = existing_bond_ytm

# Convert to percentage for readability
required_coupon_rate_percent = required_coupon_rate * 100

required_coupon_rate  # Result: 0.084 or 8.4%
```

**Common Mistakes to Avoid:**
- Using complex forward rate or spot rate calculations when simple YTM = coupon principle applies
- Interpolating yields across different bond types (fixed vs floating) incorrectly
- Attempting to price the bond using discounting when question asks for coupon rate
- Ignoring the fundamental relationship: par bonds have coupon = YTM
- Confusing "issue at par" questions with "price a bond" questions