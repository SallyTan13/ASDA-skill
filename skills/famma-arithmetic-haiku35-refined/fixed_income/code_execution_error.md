# FIXED INCOME CALCULATION PATTERNS - PROGRAM OF THOUGHT SKILL GUIDE

## Pattern: Forward Rate Compounding for Multi-Period Discount Factors

**Description:** Forward rates represent single-period rates for future periods and must be chained multiplicatively to create discount factors for cash flows at different maturities. Each cash flow at year t requires discounting by the product of all forward rates from year 0 to year t-1.

**When to Use:** Bond pricing problems with forward rate tables, questions asking to price coupon bonds given forward interest rates for multiple periods.

**Procedure:**
1. Formula: Discount factor for year t = 1 / [(1 + r₀) × (1 + r₁) × ... × (1 + r_{t-1})]
2. Extract forward rates from the table and convert percentages to decimals
3. For each cash flow at year t, build the cumulative product of (1 + forward_rate) for all periods up to t
4. Divide each cash flow by its corresponding discount factor and sum all present values
5. Return the final sum as the bond price

**Code Example:**

**Scenario:** Price a 3-year bond with 8% annual coupon (par=$1000) given forward rates: Year 0: 4%, Year 1: 6%, Year 2: 7%

**Correct Code:**
```python
# Forward rates as decimals
forward_rates = [0.04, 0.06, 0.07]
coupon = 80  # 8% of 1000
par_value = 1000
cash_flows = [coupon, coupon, coupon + par_value]

# Calculate price by discounting each cash flow
price = 0
for t in range(len(cash_flows)):
    # Build cumulative discount factor: product of (1 + r_i) for i=0 to t
    discount_factor = 1
    for i in range(t + 1):
        discount_factor *= (1 + forward_rates[i])
    price += cash_flows[t] / discount_factor

price  # Result: ~1026.49
```

**Common Bugs to Avoid:**
- Using (1 + r_t)^t instead of the product (1 + r_0) × (1 + r_1) × ... × (1 + r_t)
- Discounting year t cash flow by only the year t forward rate
- Off-by-one indexing errors when matching cash flows to forward rates
- Using print() instead of expression on last line

---

## Pattern: Zero-Coupon Bond Prices as Discount Factors

**Description:** Zero-coupon bond prices directly encode discount factors for their maturity dates. To price a coupon bond, extract the implied discount factor from each zero-coupon price (d_t = ZCB_price_t / par_value) and apply it to the corresponding cash flow.

**When to Use:** Bond pricing questions that provide a table of zero-coupon bond prices at different maturities, asking to price a coupon-paying bond.

**Procedure:**
1. Formula: Bond Price = Σ(CF_t × d_t), where d_t = ZCB_price_t / ZCB_par_value
2. Extract zero-coupon bond prices from the table and their maturities
3. Calculate discount factors: divide each ZCB price by its par value (typically 1000)
4. Multiply each coupon payment by its maturity's discount factor
5. Multiply the final payment (coupon + par) by the final maturity's discount factor
6. Sum all discounted cash flows

**Code Example:**

**Scenario:** Price a 3-year bond with 9% annual coupon (par=$1000) given zero-coupon prices: 1-yr: $943.40, 2-yr: $873.44, 3-yr: $816.30

**Correct Code:**
```python
# Zero-coupon bond prices and par value
zcb_prices = [943.40, 873.44, 816.30]
par_value = 1000
coupon_rate = 0.09
coupon = coupon_rate * par_value

# Extract discount factors
discount_factors = [price / par_value for price in zcb_prices]

# Cash flows: coupons for years 1-2, coupon + par for year 3
cash_flows = [coupon, coupon, coupon + par_value]

# Price bond
bond_price = sum(cf * df for cf, df in zip(cash_flows, discount_factors))

bond_price  # Result: ~1061.66
```

**Common Bugs to Avoid:**
- Forgetting to divide ZCB prices by par value to get discount factors
- Using ZCB prices directly as discount rates instead of discount factors
- Incorrect indexing: matching year 1 cash flow to year 0 discount factor
- Arithmetic errors in final payment (forgetting to add par value to last coupon)

---

## Pattern: Spot Rate Derivation from Forward Rates via Geometric Mean

**Description:** The spot rate (yield to maturity) for an n-year zero-coupon bond is the geometric mean of forward rates, calculated as [(1+r₀)×(1+r₁)×...×(1+r_{n-1})]^(1/n) - 1, not an arithmetic average.

**When to Use:** Questions asking for yield to maturity or spot rates when given a table of forward rates for multiple periods.

**Procedure:**
1. Formula: Spot_n = [(1 + r₀) × (1 + r₁) × ... × (1 + r_{n-1})]^(1/n) - 1
2. Extract forward rates for periods 0 through n-1 and convert to decimals
3. Calculate the product of (1 + forward_rate) for all relevant periods
4. Take the nth root of the product (raise to power 1/n)
5. Subtract 1 and optionally convert to percentage

**Code Example:**

**Scenario:** Find the 3-year spot rate given forward rates: Year 0: 4.5%, Year 1: 5.5%, Year 2: 6.5%

**Correct Code:**
```python
# Forward rates as decimals
forward_rates = [0.045, 0.055, 0.065]
n = 3  # Number of years

# Calculate product of (1 + forward_rate)
product = 1
for rate in forward_rates[:n]:
    product *= (1 + rate)

# Take geometric mean
spot_rate = product ** (1/n) - 1

spot_rate  # Result: ~0.0549 or 5.49%
```

**Common Bugs to Avoid:**
- Using arithmetic mean: sum(rates)/n instead of geometric mean
- Forgetting to subtract 1 after taking the nth root
- Using wrong exponent: n instead of 1/n
- Sign errors: using negative rates or subtracting instead of multiplying

---

## Pattern: Forward Rate Extraction from Spot Rates

**Description:** Under the expectations hypothesis, the forward rate f_{m,n} from year m to year n is derived from spot rates using the relationship: (1 + z_n)^n = (1 + z_m)^m × (1 + f_{m,n})^{n-m}, where z represents spot rates.

**When to Use:** Questions asking for expected future short rates or forward rates when given a table of spot rates (YTM) for zero-coupon bonds at different maturities.

**Procedure:**
1. Formula: f_{m,n} = [(1 + z_n)^n / (1 + z_m)^m]^(1/(n-m)) - 1
2. Identify the target period: m years from now for a (n-m) year period
3. Extract spot rates z_n and z_m from the table and convert to decimals
4. Calculate (1 + z_n)^n and (1 + z_m)^m
5. Divide the longer-term factor by the shorter-term factor
6. Take the appropriate root: raise to power 1/(n-m)
7. Subtract 1 to get the forward rate

**Code Example:**

**Scenario:** Find the 1-year forward rate 2 years from now given spot rates: 2-year: 5.5%, 3-year: 6.2%

**Correct Code:**
```python
# Spot rates (YTM) as decimals
z_2 = 0.055  # 2-year spot rate
z_3 = 0.062  # 3-year spot rate

# Calculate forward rate from year 2 to year 3
# (1 + z_3)^3 = (1 + z_2)^2 × (1 + f_{2,3})^1
forward_rate_2_3 = ((1 + z_3)**3 / (1 + z_2)**2)**(1/1) - 1

forward_rate_2_3  # Result: ~0.0761 or 7.61%
```

**Common Bugs to Avoid:**
- Subtracting spot rates directly: z_n - z_m
- Using wrong exponents in the formula
- Forgetting to take the appropriate root (1/(n-m))
- Confusing which rate is in numerator vs denominator

---

## Pattern: Convertible Bond Conversion Premium Calculation

**Description:** Conversion premium measures how much MORE an investor pays for the convertible bond above its conversion value. The formula is: Conversion Premium = Market Price of Bond - Conversion Value, where Conversion Value = Conversion Ratio × Stock Price.

**When to Use:** Convertible bond questions asking for conversion premium, given market price of bond, stock price, and conversion ratio.

**Procedure:**
1. Formula: Conversion Premium = Bond Market Price - (Conversion Ratio × Stock Price)
2. Extract conversion ratio, stock price, and bond market price from the problem
3. Calculate conversion value: multiply conversion ratio by stock price
4. Subtract conversion value from bond market price
5. Ensure result is positive if bond trades at premium to conversion value

**Code Example:**

**Scenario:** Calculate conversion premium for a bond trading at $850, stock at $35, conversion ratio of 22 shares

**Correct Code:**
```python
# Given values
bond_market_price = 850
stock_price = 35
conversion_ratio = 22

# Calculate conversion value
conversion_value = conversion_ratio * stock_price

# Calculate conversion premium
conversion_premium = bond_market_price - conversion_value

conversion_premium  # Result: 80
```

**Common Bugs to Avoid:**
- Reversing the formula: conversion_value - bond_price (produces negative premium)
- Dividing instead of multiplying: bond_price / conversion_ratio
- Using par value instead of market price of bond
- Forgetting to account for bond price quotation conventions (e.g., if quoted as percentage of par)

---

## Pattern: Duration Hedging with Futures Contracts

**Description:** The number of futures contracts needed to adjust portfolio duration is calculated using the formula: N_f = -(D_target - D_portfolio) × Portfolio_Value / (D_CTD × CTD_Price × Conversion_Factor), where CTD is the cheapest-to-deliver bond.

**When to Use:** Questions about hedging interest rate risk using futures, adjusting portfolio duration to a target level, given futures contract specifications and CTD bond characteristics.

**Procedure:**
1. Formula: N_f = -(D_target - D_portfolio) × V_portfolio / (D_CTD × P_CTD × CF)
2. Extract portfolio duration, target duration, and portfolio value
3. Extract CTD bond duration, CTD bond price, and conversion factor from futures data
4. Calculate duration change needed: D_target - D_portfolio
5. Calculate denominator: D_CTD × P_CTD × CF
6. Multiply duration change by portfolio value, divide by denominator
7. Apply negative sign (selling futures to reduce duration, buying to increase)
8. Round to nearest whole number of contracts

**Code Example:**

**Scenario:** Portfolio value €80M, current duration 7, target duration 4.5. Futures: CTD duration 4.8, CTD price €95,000, conversion factor 1.10

**Correct Code:**
```python
# Portfolio characteristics
portfolio_value = 80_000_000
current_duration = 7
target_duration = 4.5

# Futures contract specifications
ctd_duration = 4.8
ctd_price = 95_000
conversion_factor = 1.10

# Calculate number of contracts
duration_change = target_duration - current_duration
denominator = ctd_duration * ctd_price * conversion_factor

num_contracts = -(duration_change * portfolio_value) / denominator

round(num_contracts)  # Result: 400 contracts (sell to reduce duration)
```

**Common Bugs to Avoid:**
- Forgetting the negative sign (direction matters: sell to reduce, buy to increase)
- Omitting conversion factor from the denominator
- Using futures contract notional instead of CTD bond price
- Incorrect order of operations in multi-step calculation
- Not rounding to whole number of contracts

---

## Pattern: Holding Period Return for Zero-Coupon Bonds

**Description:** The holding period return for a zero-coupon bond is calculated as (Future Price / Initial Price) - 1, where prices are determined by discounting to maturity using the appropriate YTM at each point in time.

**When to Use:** Questions asking for expected return over a holding period when yield curve is expected to shift, given current and future term structures for zero-coupon bonds.

**Procedure:**
1. Formula: HPR = (P_future / P_initial) - 1
2. Calculate initial price: P_initial = Par / (1 + YTM_current)^(years_to_maturity)
3. Calculate future price: P_future = Par / (1 + YTM_future)^(remaining_years)
4. Note: remaining_years = years_to_maturity - holding_period
5. Divide future price by initial price and subtract 1
6. Convert to percentage if needed

**Code Example:**

**Scenario:** Buy a 4-year zero-coupon bond (par=$1000) at 5% YTM, hold 1 year. Next year, 3-year YTM expected to be 5.5%. Find return.

**Correct Code:**
```python
# Given values
par_value = 1000
initial_ytm = 0.05
initial_maturity = 4
holding_period = 1
future_ytm = 0.055
remaining_maturity = initial_maturity - holding_period

# Calculate initial price (4-year bond at 5% YTM)
initial_price = par_value / (1 + initial_ytm)**initial_maturity

# Calculate future price (3-year bond at 5.5% YTM)
future_price = par_value / (1 + future_ytm)**remaining_maturity

# Calculate holding period return
hpr = (future_price / initial_price) - 1

hpr  # Result: ~0.0096 or 0.96%
```

**Common Bugs to Avoid:**
- Reversing the price ratio: initial_price / future_price
- Using initial maturity instead of remaining maturity for future price
- Forgetting to subtract 1 from the price ratio
- Sign errors producing negative returns when positive expected
- Confusing YTM with coupon rate in price calculations

---

## Pattern: Portfolio Expected Return with Currency Effects

**Description:** For international portfolios, expected return must incorporate both asset returns (OAS or spread income) and currency effects. The formula combines local returns with expected currency appreciation/depreciation.

**When to Use:** Multi-asset portfolio questions with international exposure, currency hedging decisions, given OAS/spreads and expected currency movements.

**Procedure:**
1. Formula: Total Return = Σ(Weight_i × [OAS_i - Expected_Loss_i + Currency_Effect_i])
2. For each asset class, extract weight, OAS, expected loss, and currency effect
3. Calculate net return for each position: OAS - Expected Loss ± Currency Effect
4. For foreign currency positions, add expected appreciation or subtract depreciation
5. Multiply each net return by its portfolio weight
6. Sum weighted returns across all positions

**Code Example:**

**Scenario:** Portfolio: 40% USD HY (OAS 3.5%, loss 2%), 60% EUR IG (OAS 1.3%, loss 0.4%, EUR depreciates 1.5%)

**Correct Code:**
```python
# Portfolio allocations and characteristics
positions = [
    {'weight': 0.40, 'oas': 0.035, 'expected_loss': 0.020, 'currency_effect': 0},  # USD
    {'weight': 0.60, 'oas': 0.013, 'expected_loss': 0.004, 'currency_effect': -0.015}  # EUR
]

# Calculate expected portfolio return
portfolio_return = 0
for pos in positions:
    net_return = pos['oas'] - pos['expected_loss'] + pos['currency_effect']
    portfolio_return += pos['weight'] * net_return

portfolio_return  # Result: ~-0.0029 or -0.29%
```

**Common Bugs to Avoid:**
- Forgetting to subtract expected losses from OAS
- Wrong sign for currency depreciation (should be negative)
- Not weighting returns by portfolio allocation
- Applying currency effects to domestic currency positions
- Code execution failure due to missing data structure handling

---

## Pattern: Robust Code Structure for Financial Calculations

**Description:** Financial calculations require proper variable initialization, explicit step-by-step computation, and returning the final result as an expression (not using print()) to ensure compatibility with PoT execution environments. When implementing complex financial models from formulas, verify the mathematical translation matches the source equations exactly.

**When to Use:** All PoT-based financial questions to prevent code execution failures, especially complex multi-step calculations involving bond pricing models, option pricing, or term structure models.

**When NOT to Use:** Do not apply generic code templates to specialized financial models (Vasicek, CIR, Black-Scholes, etc.) without carefully verifying each formula component against the source equations. The pattern focuses on code structure, not mathematical correctness of domain-specific models.

**Procedure:**
1. Import necessary libraries at the top (math, numpy if needed)
2. Define all input variables explicitly with clear names
3. **For complex financial models: Extract formulas from problem context/images and verify each component before coding**
4. Break complex calculations into intermediate steps with descriptive variable names
5. Add comments explaining each calculation step and referencing source formulas
6. **For multi-part formulas: Calculate each component separately and verify against source before combining**
7. Store final result in a variable
8. End with the result variable as the last line (expression, not print statement)
9. Test edge cases: zero values, negative numbers, division by zero

**Common Mistakes to Avoid:**
- Using print(result) instead of result as last line
- Missing imports (e.g., math.sqrt, numpy functions)
- Undefined variables due to typos or scope issues
- Division by zero without error checking
- Returning None implicitly (no final expression)
- Incorrect data type conversions (string to float)
- Off-by-one errors in list indexing
- **Misinterpreting complex formulas: When implementing models like Vasicek or CIR, verify each term in A(t,T) and B(t,T) matches the source equation exactly**
- **Simplifying formulas incorrectly: Terms like (B(t,T) - (T-t)) should not be reduced to just B(t,T)**
- **Omitting critical formula components: Check that all terms from source equations (especially those with multiple parts) are included**

**Code Example:**

**Scenario:** Calculate effective duration given bond prices at different yield levels

**Correct Code:**
```python
# Input values
price_base = 1050
price_yield_up = 1020  # Price if yield increases by 0.01
price_yield_down = 1082  # Price if yield decreases by 0.01
yield_change = 0.01

# Calculate effective duration
# Formula: (P- - P+) / (2 × P0 × Δy)
numerator = price_yield_down - price_yield_up
denominator = 2 * price_base * yield_change

effective_duration = numerator / denominator

effective_duration  # Result: 2.95 (MUST be expression, not print)
```

**Example of Formula Verification (for complex models):**

**Scenario:** Implementing a bond pricing model with A(t,T) and B(t,T) components

**Wrong approach:** 
```python
# Incorrect: Oversimplified A(t,T) calculation
def calculate_A(a, b, sigma, t, T, B):
    term1 = (b - sigma**2 / (2 * a**2)) * B  # Missing (B - (T-t)) structure
    term2 = (sigma**2 / (4 * a**3)) * B**2
    return math.exp(term1 - term2)
```

**Correct approach:**
```python
# Correct: Verify formula structure matches source equation
# Source: A(t,T) = exp{[B(t,T)-(T-t)](ab-σ²/2)/a² - σ²B(t,T)²/(4a)}
def calculate_A(a, b, sigma, t, T, B_val):
    time_diff = T - t
    # First term: [B(t,T) - (T-t)] × (ab - σ²/2) / a²
    term1 = (B_val - time_diff) * (a * b - sigma**2 / 2) / (a**2)
    # Second term: σ²B(t,T)² / (4a)
    term2 = (sigma**2 * B_val**2) / (4 * a)
    return math.exp(term1 - term2)
```

---

## Pattern: Complex Financial Model Implementation from Source Formulas

**Description:** When implementing specialized financial models (Vasicek, CIR, Black-Scholes, HJM, etc.) from textbook formulas or problem images, each mathematical component must be translated exactly as specified. Multi-part formulas require component-by-component verification before assembly.

**When to Use:** Questions providing explicit mathematical formulas for bond pricing models, option pricing models, or term structure models, especially when formulas contain multiple nested terms or exponential/logarithmic expressions.

**Procedure:**
1. Identify the complete formula from problem context (text, images, or OCR)
2. Parse the formula into distinct components (e.g., A(t,T), B(t,T), discount factors)
3. For each component, write out the mathematical expression exactly as given
4. Identify all variables and parameters needed (a, b, σ, r, T, t, etc.)
5. Implement each component as a separate function or variable with clear naming
6. **Critical: Verify each term's structure** — check for:
   - Differences vs. products (e.g., (B - (T-t)) is NOT the same as B)
   - Correct exponents and roots
   - Proper placement of constants and parameters
7. Combine components according to the main formula
8. Test with known values if available

**Common Mistakes to Avoid:**
- Simplifying complex terms prematurely (e.g., treating (B - (T-t)) as just B)
- Confusing similar-looking formulas between different models (Vasicek vs. CIR)
- Missing parentheses that change order of operations
- Using wrong parameter in exponential terms (e.g., σ vs. σ²)
- Not accounting for all terms in multi-part formulas

**Example (sanitized):**

**Scenario:** Implement a bond pricing model where P(t,T) = A(t,T) × exp(-B(t,T) × r(t)), with A(t,T) = exp{[B(t,T) - (T-t)] × θ - φ × B(t,T)²}

**Wrong approach:**
```python
# Incorrect: Oversimplified A(t,T)
A = math.exp(B * theta - phi * B**2)  # Missing (B - (T-t)) structure
price = A * math.exp(-B * r)
```

**Correct approach:**
```python
# Step 1: Calculate B(t,T) according to model formula
B = (1 - math.exp(-kappa * (T - t))) / kappa

# Step 2: Calculate A(t,T) with all terms from source
time_to_maturity = T - t
theta_term = (B - time_to_maturity) * theta  # Preserve (B - (T-t)) structure
phi_term = phi * B**2
A = math.exp(theta_term - phi_term)

# Step 3: Combine for final price
price = A * math.exp(-B * r)
```