# DETAILED SKILL PATTERNS FOR DERIVATIVES CALCULATION ERRORS

---

## Pattern: Futures Hedge Ratio with Conversion Factor Adjustment

**Description:** When calculating the number of futures contracts needed for hedging, the conversion factor adjusts the effective BPV of the futures contract. A conversion factor < 1 means the cheapest-to-deliver bond is MORE price-sensitive, requiring FEWER contracts (multiply BPV by conversion factor, not divide). **Return full precision results unless explicitly asked to round.**

**When to Use:** Futures hedging problems involving basis point value (BPV), duration matching, or immunization where a conversion factor for the cheapest-to-deliver bond is provided.

**When NOT to Use:**
- Do NOT apply rounding unless the problem explicitly asks for "number of contracts" or "whole contracts"
- Do NOT round when the problem asks for hedge ratios or fractional positions

**Procedure:**
1. Formula: `Number of Contracts = Net BPV Exposure / (BPV per Contract × Conversion Factor)`
2. Calculate net exposure: `Net BPV = |BPV_assets - BPV_liabilities|`
3. Adjust futures BPV: `Effective BPV = BPV_per_contract × Conversion_Factor`
4. Determine direction: If assets > liabilities, SELL futures; if liabilities > assets, BUY futures
5. **Return full precision unless problem explicitly asks for whole contracts**
6. If rounding is needed, use `round()` only as the final step

**Code Example:**

**Scenario:** A portfolio has asset BPV of 60,000 and liability BPV of 35,000. Treasury futures have BPV of 50 per $100,000 notional and conversion factor of 0.85.

**Correct Code:**
```python
# Portfolio exposure
bpv_assets = 60000
bpv_liabilities = 35000
net_bpv_exposure = bpv_assets - bpv_liabilities

# Futures contract specifications
bpv_per_contract = 50  # per $100,000 notional
conversion_factor = 0.85

# Adjust BPV for conversion factor
# Conversion factor < 1 means CTD bond is MORE sensitive
# So effective BPV is HIGHER: multiply, not divide
effective_bpv_per_contract = bpv_per_contract * conversion_factor

# Calculate number of contracts
number_of_contracts = net_bpv_exposure / effective_bpv_per_contract

# Only round if problem asks for "number of contracts" (whole units)
round(number_of_contracts)
```

**Common Bugs to Avoid:**
- Dividing by conversion factor instead of multiplying (inverts the adjustment)
- Forgetting to take absolute value when determining hedge size
- Using print() instead of returning the expression
- **Rounding when the problem asks for a ratio or doesn't specify whole contracts**
- Not rounding to whole contracts when the problem explicitly asks for "number of contracts"

---
## Pattern: Black-Scholes Option Pricing with Correct Output Alignment

**Description:** When implementing Black-Scholes or Black-76 models, ensure the final computed value from code execution matches the natural language explanation. The code must return the expression value, not print it, and the explanation must reference the actual computed result. **Preserve full numerical precision unless the problem explicitly requests rounding to a specific number of decimal places.** **When the risk-free rate is not explicitly provided in the problem, DO NOT assume a value—this pattern cannot be applied without all required parameters.**

**When to Use:** European option pricing problems using Black-Scholes (equity options), Black-76 (futures options), or Garman-Kohlhagen (FX options) models **where ALL required parameters (S₀, K, r, T, σ) are explicitly provided or can be unambiguously derived from context.**

**When NOT to Use:** 
- Do NOT apply rounding to final results unless the problem explicitly asks for a specific precision (e.g., "round to 2 decimal places")
- Do NOT round intermediate calculations that will be used in subsequent steps
- Do NOT assume currency formatting implies rounding requirement (e.g., "$42.05" may require full precision 42.050843...)
- **Do NOT assume or infer the risk-free rate if it is not explicitly stated in the problem—missing parameters invalidate the calculation**
- **Do NOT use this pattern for time value decomposition if the option price must be calculated first and any parameter is missing**

**Procedure:**
1. **Verify all parameters are provided:** S₀ (spot price), K (strike), r (risk-free rate), T (time to maturity), σ (volatility)
2. **If risk-free rate is missing:** Check if the problem provides it indirectly (e.g., "6% per annum" in context). If not found, this pattern cannot be applied.
3. Formula: `Call = S₀ × N(d₁) - K × e^(-rT) × N(d₂)` where `d₁ = [ln(S₀/K) + (r + σ²/2)T] / (σ√T)` and `d₂ = d₁ - σ√T`
4. Import required libraries: `math`, `scipy.stats.norm`
5. Calculate d₁ and d₂ using natural logarithm and square root functions
6. Compute N(d₁) and N(d₂) using `norm.cdf()`
7. Apply discount factor and return final expression (not print)
8. **Return full precision result** — only round if explicitly requested in the problem
9. Verify: Call price should be between 0 and S₀; Put price between 0 and K×e^(-rT)

**Code Example:**

**Scenario:** Stock price $105, strike $100, risk-free rate 3%, volatility 25%, maturity 0.75 years.

**Correct Code:**
```python
import math
from scipy.stats import norm

# Parameters (all explicitly provided)
S0 = 105
K = 100
r = 0.03  # Explicitly stated
T = 0.75
sigma = 0.25

# Calculate d1 and d2
d1 = (math.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
d2 = d1 - sigma * math.sqrt(T)

# Cumulative normal distribution
N_d1 = norm.cdf(d1)
N_d2 = norm.cdf(d2)

# Call option price
call_price = S0 * N_d1 - K * math.exp(-r * T) * N_d2

# Return full precision (no rounding unless explicitly requested)
call_price
```

**Common Bugs to Avoid:**
- Using `print(call_price)` instead of returning the expression
- Writing explanation with different numbers than code computes
- Forgetting to import `scipy.stats.norm` for CDF calculation
- Using `math.log10()` instead of `math.log()` (natural log)
- **Prematurely rounding results when full precision is needed for comparison**
- **Assuming currency display format (e.g., "$42.05") requires rounding the computed value**
- **Assuming a risk-free rate value (e.g., 6%) when it is not provided in the problem—this invalidates the entire calculation**
- Sanity check failure: not verifying 0 < call < S0

**Example (sanitized):**

> **Scenario:** Problem asks for time value of a call option. Stock = $90, Strike = $85, Volatility = 35%, Maturity = 1 year. Risk-free rate is NOT mentioned.
>
> **Wrong approach:** Assume r = 0.05 or r = 0.06 and proceed with Black-Scholes calculation. This produces an arbitrary result that depends on the assumed rate.
>
> **Correct approach:** Recognize that without the risk-free rate, Black-Scholes cannot be applied. The problem is either missing information or expects a different approach (e.g., using given option prices rather than calculating them).

---
## Pattern: Rolling Futures Hedge Gain/Loss Calculation

**Description:** When calculating gains from rolling futures positions, track each contract period separately. For short positions, gain = (entry price - exit price) × position size. Ensure consistent units (per barrel vs total position) throughout the calculation.

**When to Use:** Stack-and-roll hedge strategies where futures contracts are closed and reopened at different maturities; problems asking for per-unit or total gains from multiple futures positions.

**Procedure:**
1. Formula: `Gain per unit = Σ(Entry_Price_i - Exit_Price_i)` for short positions
2. For each futures contract period, calculate: `Gain_i = (Price_at_entry - Price_at_exit)`
3. Sum all period gains to get total per-unit gain
4. If asked for total gain: multiply by total units (not per-contract units)
5. Verify: Short position profits when price falls; long position profits when price rises

**Code Example:**

**Scenario:** Hedge 50,000 barrels using 50 contracts. Roll through 3 futures: Contract A (entry $52, exit $50), Contract B (entry $50, exit $48.5), Contract C (entry $48.5, exit $47.2).

**Correct Code:**
```python
# Position details
total_barrels = 50000
num_contracts = 50

# Futures price movements (short position)
contract_a_entry = 52.0
contract_a_exit = 50.0

contract_b_entry = 50.0
contract_b_exit = 48.5

contract_c_entry = 48.5
contract_c_exit = 47.2

# Calculate gain per barrel for each contract period
# Short position: gain when price falls
gain_contract_a = contract_a_entry - contract_a_exit
gain_contract_b = contract_b_entry - contract_b_exit
gain_contract_c = contract_c_entry - contract_c_exit

# Total gain per barrel
total_gain_per_barrel = gain_contract_a + gain_contract_b + gain_contract_c

# Verify calculation
total_gain_per_barrel  # Should be 4.8
```

**Common Bugs to Avoid:**
- Calculating per-contract gain then dividing by total barrels (wrong denominator)
- Using `barrels_per_contract` as a multiplier instead of working with totals
- Sign errors: forgetting short positions profit from price decreases
- Mixing per-unit and total position calculations inconsistently

---

## Pattern: CDS Valuation with Premium and Accrual Components

**Description:** Credit default swap valuation requires computing PV of protection leg (expected payoff on default) minus PV of premium leg (regular payments plus accrued premium on default). The value to protection buyer = PV(payoff) - PV(premium payments) - PV(accrual payments).

**When to Use:** CDS pricing problems with given hazard rates, recovery rates, and spread; questions asking for swap value from protection buyer or seller perspective.

**Procedure:**
1. Formula: `Value_to_buyer = PV(Expected Payoff) - [PV(Premium Payments) + PV(Accrual Payments)]`
2. Calculate `PV(Expected Payoff) = (1 - Recovery_Rate) × Σ[P(default_t) × Discount_t]`
3. Calculate `PV(Premium) = Spread × Σ[P(survival_t) × Discount_t]`
4. Calculate `PV(Accrual) = Spread × 0.5 × Σ[P(default_t) × Discount_t]` (assumes mid-period default)
5. Combine: `Value = PV(Payoff) - PV(Premium) - PV(Accrual)`
6. Verify: If spread > fair spread, value to buyer is negative (overpaying)

**Code Example:**

**Scenario:** 5-year CDS, spread 200 bps, recovery 40%, risk-free rate 4%. Given: PV(survival payments coefficient) = 4.5, PV(default probability coefficient) = 0.06, PV(accrual coefficient) = 0.03.

**Correct Code:**
```python
# CDS parameters
spread = 0.02  # 200 basis points
recovery_rate = 0.40
notional = 1.0

# Pre-computed coefficients from probability tables
pv_survival_coefficient = 4.5  # Σ[P(survival_t) × Discount_t]
pv_default_coefficient = 0.06  # Σ[P(default_t) × Discount_t]
pv_accrual_coefficient = 0.03  # Σ[P(default_t) × Discount_t × 0.5]

# PV of protection leg (payoff to buyer on default)
pv_expected_payoff = (1 - recovery_rate) * pv_default_coefficient

# PV of premium leg (payments by buyer)
pv_premium_payments = spread * pv_survival_coefficient
pv_accrual_payments = spread * pv_accrual_coefficient

# Value to protection buyer
value_to_buyer = pv_expected_payoff - pv_premium_payments - pv_accrual_payments

round(value_to_buyer, 4)
```

**Common Bugs to Avoid:**
- Forgetting to include accrual payment component
- Sign error: subtracting payoff instead of subtracting premiums
- Using wrong perspective (buyer vs seller)
- Not recognizing that coefficients already include summation over time periods

---

## Pattern: Breeden-Litzenberger Probability Density from Option Prices

**Description:** The risk-neutral probability density g(K) is derived from the second derivative of call prices with respect to strike: g(K) = e^(rT) × [C(K-δ) + C(K+δ) - 2C(K)] / δ². **For discrete probability calculations, compute densities at interval MIDPOINTS** (between consecutive strikes) and treat each density as representing probability mass over an interval of width δ. Total probability = Σ[g(K_mid) × δ].

**When to Use:** Implied probability distribution extraction from option prices; volatility smile analysis; questions asking for probability in a strike range; problems requiring discrete interval summation rather than continuous integration.

**Procedure:**
1. Formula: `g(K) = e^(rT) × [C(K-δ) + C(K+δ) - 2C(K)] / δ²`
2. Calculate call prices for all strikes using Black-Scholes with given implied volatilities
3. **For discrete probability calculation:** Compute densities at MIDPOINTS between consecutive strikes:
   - For interval [K_i, K_{i+1}], midpoint = (K_i + K_{i+1}) / 2
   - Density at midpoint requires call prices at midpoint ± δ/2
4. **Each density represents probability mass over interval width δ:** P(interval) = g(midpoint) × δ
5. **To find probability in range [K_low, K_high]:** Sum all interval probabilities that overlap the range
6. **Boundary handling:** Include partial intervals at boundaries; if K_low or K_high fall between strikes, include those full intervals
7. Verify: Total probability across all intervals should be close to 1.0 (within numerical error)

**Example (sanitized):**

> **Scenario:** Strikes at [0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4] with spacing δ=0.1. Stock at 1.0, rate 2%, maturity 0.5 years. Find probability between 0.7 and 1.3.
>
> **Wrong approach:** 
> - Computing densities only at interior strikes [0.7, 0.8, ..., 1.3]
> - Using trapezoidal integration over interior strikes
> - This gives probability for a narrower range and misses boundary intervals
>
> **Correct approach:**
> 1. Identify intervals covering [0.7, 1.3]: [0.6-0.7], [0.7-0.8], [0.8-0.9], [0.9-1.0], [1.0-1.1], [1.1-1.2], [1.2-1.3], [1.3-1.4]
> 2. For each interval, compute density at MIDPOINT:
>    - Interval [0.6-0.7]: midpoint = 0.65, need C(0.6), C(0.65), C(0.7)
>    - Interval [0.7-0.8]: midpoint = 0.75, need C(0.7), C(0.75), C(0.8)
>    - Continue for all intervals...
> 3. Calculate density at each midpoint: g(0.65) = e^(rT) × [C(0.6) + C(0.7) - 2×C(0.65)] / (0.05)²
> 4. Probability for each interval: P([0.6-0.7]) = g(0.65) × 0.1
> 5. Sum probabilities for all intervals from 0.7 to 1.3 (inclusive of boundary intervals)
> 6. Total probability = Σ[g(midpoint_i) × δ] for i covering the range

**Code Example:**

```python
import numpy as np
from scipy.stats import norm

# Parameters
S0 = 1.0
r = 0.02
T = 0.5
strikes = np.array([0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4])
implied_vols = np.array([0.25, 0.22, 0.20, 0.18, 0.17, 0.18, 0.20, 0.22, 0.25])
delta = 0.1

# Black-Scholes call price function
def bs_call(S, K, T, r, sigma):
    if K <= 0:
        return S
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)

# Interpolate implied volatility for any strike
def interpolate_vol(K, strikes, vols):
    return np.interp(K, strikes, vols)

# Calculate call price for any strike (including midpoints)
def call_price_at_strike(K):
    vol = interpolate_vol(K, strikes, implied_vols)
    return bs_call(S0, K, T, r, vol)

# Define intervals: midpoints between consecutive strikes
intervals = []
for i in range(len(strikes) - 1):
    midpoint = (strikes[i] + strikes[i+1]) / 2
    intervals.append(midpoint)

# Calculate density at each midpoint
densities = []
for midpoint in intervals:
    # Need call prices at midpoint - delta/2, midpoint, midpoint + delta/2
    # For density calculation, use delta = spacing between original strikes
    c_minus = call_price_at_strike(midpoint - delta/2)
    c_center = call_price_at_strike(midpoint)
    c_plus = call_price_at_strike(midpoint + delta/2)
    
    # Breeden-Litzenberger formula with half-delta spacing
    g_mid = np.exp(r*T) * (c_minus + c_plus - 2*c_center) / ((delta/2)**2)
    densities.append(g_mid)

# Probability for range [0.7, 1.3]
# Include all intervals where midpoint is between 0.65 and 1.35
# (this captures intervals [0.6-0.7] through [1.3-1.4])
total_probability = 0
for midpoint, density in zip(intervals, densities):
    # Include interval if it overlaps with [0.7, 1.3]
    interval_start = midpoint - delta/2
    interval_end = midpoint + delta/2
    
    if interval_end >= 0.7 and interval_start <= 1.3:
        # Probability mass for this interval
        prob_mass = density * delta
        total_probability += prob_mass

round(total_probability, 4)
```

**Common Bugs to Avoid:**
- Computing densities at strike prices instead of interval midpoints
- Using continuous integration (trapezoidal rule) instead of discrete summation
- Excluding boundary intervals that partially overlap the target range
- Forgetting that each density represents probability over interval width δ, not a point probability
- Not interpolating implied volatilities for midpoint strikes
- Using full delta spacing in Breeden-Litzenberger formula when working with midpoints (should use delta/2)
- Forgetting the e^(rT) discount factor in Breeden-Litzenberger formula
- Not verifying that computed densities are non-negative
## Pattern: Vasicek Model Bond Option Pricing

**Description:** Pricing options on coupon bonds in the Vasicek model requires computing the bond price as a function of the short rate at option maturity, then using the known Gaussian distribution of r(T) to evaluate the option payoff expectation. Cannot use Black-Scholes directly.

**When to Use:** Interest rate derivative pricing in Vasicek or other affine term structure models; options on bonds (not just zero-coupon bonds); problems providing mean reversion parameters (a, b, σ).

**Procedure:**
1. Formula: `P(t,T) = A(t,T) × e^(-B(t,T)×r(t))` where `B(t,T) = [1-e^(-a(T-t))]/a`
2. Calculate zero-coupon bond prices for all cash flow dates using Vasicek formula
3. At option maturity T_opt, bond value = Σ[coupon × P(T_opt, T_coupon)] + principal × P(T_opt, T_maturity)
4. Under Vasicek, r(T_opt) ~ Normal(μ, σ²) with known mean and variance
5. Option value = e^(-rT_opt) × E[max(Bond_Price(r(T_opt)) - K, 0)]
6. Use numerical integration or closed-form formula for Gaussian option pricing

**Code Example:**

**Scenario:** 2-year call option on 3-year bond, strike 98. Bond pays 4% annual coupon. Vasicek: a=0.1, b=0.06, σ=0.02, r₀=0.05.

**Correct Code:**
```python
import numpy as np
from scipy.stats import norm
from scipy.integrate import quad

# Vasicek parameters
a = 0.1
b = 0.06
sigma = 0.02
r0 = 0.05

# Option and bond parameters
T_option = 2.0
T_bond = 3.0
strike = 98
coupon_rate = 0.04
principal = 100
coupon_payment = coupon_rate * principal

# Vasicek zero-coupon bond price
def vasicek_zcb(t, T, r, a, b, sigma):
    tau = T - t
    B = (1 - np.exp(-a * tau)) / a
    A = np.exp((b - sigma**2/(2*a**2)) * (B - tau) - (sigma**2/(4*a)) * B**2)
    return A * np.exp(-B * r)

# Bond price at option maturity as function of short rate
def bond_price_at_option(r_T):
    # Remaining cash flows: one coupon at T=3 plus principal
    tau_remaining = T_bond - T_option
    price = (coupon_payment + principal) * vasicek_zcb(T_option, T_bond, r_T, a, b, sigma)
    return price

# Distribution of r(T_option) under Vasicek
# r(T) ~ Normal(mean_r, var_r)
mean_r = r0 * np.exp(-a * T_option) + b * (1 - np.exp(-a * T_option))
var_r = (sigma**2 / (2*a)) * (1 - np.exp(-2*a*T_option))
std_r = np.sqrt(var_r)

# Option payoff integrand
def option_payoff_integrand(r_T):
    bond_price = bond_price_at_option(r_T)
    payoff = max(bond_price - strike, 0)
    probability_density = norm.pdf(r_T, mean_r, std_r)
    return payoff * probability_density

# Integrate over possible r(T) values
integration_range = (mean_r - 4*std_r, mean_r + 4*std_r)
expected_payoff, _ = quad(option_payoff_integrand, *integration_range)

# Discount to present value
discount_factor = vasicek_zcb(0, T_option, r0, a, b, sigma)
option_value = discount_factor * expected_payoff

round(option_value, 4)
```

**Common Bugs to Avoid:**
- Applying Black-Scholes formula directly (wrong model)
- Using ad-hoc volatility adjustments instead of proper distribution
- Forgetting that bond price depends on short rate at option maturity
- Not accounting for all remaining cash flows (coupons + principal)
- Incorrect distribution parameters for r(T) under Vasicek dynamics

---

## Pattern: Option Time Value Decomposition

**Description:** Option value = Intrinsic Value + Time Value. For puts: Intrinsic = max(Strike - Stock, 0). For calls: Intrinsic = max(Stock - Strike, 0). Time value is always non-negative and represents the premium for potential favorable price movement.

**When to Use:** Option valuation problems asking to separate intrinsic and time value components; problems with market prices (bid/ask) requiring mid-market calculation.

**Procedure:**
1. Formula: `Time Value = Option Price - Intrinsic Value`
2. Calculate mid-market price: `Mid = (Bid + Ask) / 2`
3. For puts: `Intrinsic = max(Strike - Current_Stock_Price, 0)`
4. For calls: `Intrinsic = max(Current_Stock_Price - Strike, 0)`
5. Compute: `Time_Value = Mid_Price - Intrinsic_Value`
6. Verify: Time value should be ≥ 0 for all options

**Code Example:**

**Scenario:** Put options with strikes [95, 100, 105, 110]. Stock at $102. Bid/ask: [(2.1, 2.3), (4.5, 4.9), (7.8, 8.2), (12.1, 12.5)].

**Correct Code:**
```python
# Market data
current_stock_price = 102
strikes = [95, 100, 105, 110]
bid_ask_pairs = [(2.1, 2.3), (4.5, 4.9), (7.8, 8.2), (12.1, 12.5)]

# Calculate time values for each strike
time_values = {}

for strike, (bid, ask) in zip(strikes, bid_ask_pairs):
    # Mid-market price
    mid_price = (bid + ask) / 2
    
    # Intrinsic value for put option
    intrinsic_value = max(strike - current_stock_price, 0)
    
    # Time value
    time_value = mid_price - intrinsic_value
    
    time_values[strike] = round(time_value, 2)

time_values
```

**Common Bugs to Avoid:**
- Using wrong intrinsic formula (call formula for puts or vice versa)
- Forgetting to calculate mid-market price (using bid or ask directly)
- Negative time values (indicates calculation error)
- Not using max(0, ...) for intrinsic value calculation

---

## Pattern: Commodity Futures Option Valuation (Black-76 Model)

**Description:** Options on futures use the Black-76 model where the underlying is the futures price (not spot). The formula is: Call = e^(-rT) × [F×N(d₁) - K×N(d₂)] where F is the futures price. Must multiply by contract size for total value.

**When to Use:** Options on commodity futures, index futures, or interest rate futures; problems providing futures price rather than spot price; questions asking for total option value across multiple units.

**Procedure:**
1. Formula: `Call = e^(-rT) × [F×N(d₁) - K×N(d₂)]` where `d₁ = [ln(F/K) + (σ²/2)T] / (σ√T)`
2. Use futures price F (not spot price S) as the underlying
3. Calculate d₁ and d₂ using futures price
4. Apply discount factor e^(-rT) to entire expression
5. Multiply by contract size or number of units for total value
6. Verify: Option value per unit should be reasonable relative to F and K

**Code Example:**

**Scenario:** 4-month call option on gold futures. Futures price $1,850/oz, strike $1,800/oz, volatility 18%, risk-free rate 4%. Contract size: 5,000 oz.

**Correct Code:**
```python
import math
from scipy.stats import norm

# Parameters
F = 1850  # Futures price per oz
K = 1800  # Strike price per oz
T = 4/12  # 4 months in years
r = 0.04  # Risk-free rate
sigma = 0.18  # Volatility
contract_size = 5000  # oz per contract

# Black-76 model for futures options
# d1 = [ln(F/K) + (sigma^2/2)*T] / (sigma*sqrt(T))
d1 = (math.log(F / K) + (sigma**2 / 2) * T) / (sigma * math.sqrt(T))
d2 = d1 - sigma * math.sqrt(T)

# Cumulative normal distribution
N_d1 = norm.cdf(d1)
N_d2 = norm.cdf(d2)

# Call option value per oz (Black-76)
discount_factor = math.exp(-r * T)
call_value_per_oz = discount_factor * (F * N_d1 - K * N_d2)

# Total option value for full contract
total_option_value = call_value_per_oz * contract_size

round(total_option_value, 2)
```

**Common Bugs to Avoid:**
- Using spot price instead of futures price in the formula
- Forgetting the discount factor e^(-rT) on the entire expression
- Not multiplying by contract size when asked for total value
- Using Black-Scholes formula (with drift term) instead of Black-76
- Calculation verification: per-unit value should be between 0 and F

## Pattern: Forward and Futures Pricing with Continuous Compounding

**Description:** For non-dividend-paying assets, the forward price is calculated using the cost-of-carry model: F₀ = S₀ × e^(rT), where continuous compounding is applied. **Preserve full numerical precision in the final result** unless the problem explicitly requests rounding to a specific format.

**When to Use:** Forward contract pricing problems on stocks, commodities, or currencies; problems involving continuous compounding; questions asking for "forward price" or "futures price" with given spot price and risk-free rate.

**When NOT to Use:**
- Do NOT apply this pattern when dividends or storage costs are involved (use cost-of-carry with income/costs)
- Do NOT round the final result unless explicitly requested
- Do NOT confuse with discrete compounding formulas

**Procedure:**
1. Formula: `F₀ = S₀ × e^(rT)` for non-dividend-paying assets
2. Identify: S₀ (current spot price), r (continuously compounded risk-free rate), T (time to maturity)
3. Calculate using `math.exp(r * T)` for the exponential term
4. **Return full precision result** — the mathematical value, not a display-formatted version
5. Verify: Forward price should be close to spot price adjusted for time value (F₀ > S₀ if r > 0)

**Code Example:**

**Scenario:** A 6-month forward contract on a non-dividend-paying stock trading at $85, with a continuously compounded risk-free rate of 4% per annum.

**Correct Code:**
```python
import math

# Given parameters
S0 = 85  # Current spot price
r = 0.04  # Risk-free rate (continuous compounding)
T = 0.5  # Time to maturity (6 months = 0.5 years)

# Forward price formula for non-dividend-paying asset
# F0 = S0 * e^(r*T)
forward_price = S0 * math.exp(r * T)

# Return full precision (no rounding unless explicitly requested)
forward_price
```

**Common Mistakes to Avoid:**
- Using discrete compounding formula `S₀ × (1 + r)^T` instead of continuous `S₀ × e^(rT)`
- **Rounding the result prematurely (e.g., to 2 decimal places) when full precision is needed**
- Confusing forward price with present value (discounting instead of compounding)
- Not recognizing that currency formatting in the answer (e.g., "$42.05") doesn't necessarily mean the computed value should be rounded
- Using `math.log10()` or other incorrect exponential functions

## Pattern: Portfolio Insurance with Index Options - Contract Multiplier Adjustment

**Description:** When hedging a portfolio using index options, the number of contracts needed depends on the index option contract multiplier (typically 100 for equity index options). The formula is: Number of Contracts = Portfolio Value / (Index Level × Contract Multiplier). **Do NOT confuse "index units" with "option contracts"—they differ by the multiplier factor.**

**When to Use:** Portfolio insurance problems using traded index options (puts or calls); hedging strategies where portfolio value is given along with index level; problems asking for insurance cost or number of contracts needed.

**When NOT to Use:**
- Do NOT use when the problem involves custom OTC options without standard contract specifications
- Do NOT apply when hedging with futures (different contract structure)
- Do NOT use if the contract multiplier is explicitly stated as 1 or if working with single-stock options

**Procedure:**
1. **Identify contract multiplier:** For standard equity index options (S&P 500, etc.), multiplier is typically 100. If not stated, use 100 as default for major indices.
2. Formula: `Number of Contracts = Portfolio Value / (Index Level × Contract Multiplier)`
3. Calculate option price per contract using Black-Scholes with dividend yield (if applicable)
4. **Total insurance cost = Option Price per Contract × Number of Contracts**
5. Verify: Number of contracts should be reasonable (typically hundreds to thousands for multi-million portfolios)

**Code Example:**

**Scenario:** Portfolio worth $240 million mirrors an index at 1,500. Manager wants put options for insurance. Index option multiplier is 100. Put option calculated at $45 per index point.

**Correct Code:**
```python
# Portfolio and index parameters
portfolio_value = 240_000_000  # $240 million
index_level = 1500
contract_multiplier = 100  # Standard for equity index options

# Calculate number of contracts needed
# Each contract covers (index_level × multiplier) dollars of exposure
num_contracts = portfolio_value / (index_level * contract_multiplier)

# Option pricing (assume put_price_per_index_point calculated via Black-Scholes)
put_price_per_index_point = 45  # From Black-Scholes calculation

# Total cost per contract
cost_per_contract = put_price_per_index_point * contract_multiplier

# Total insurance cost
total_insurance_cost = cost_per_contract * num_contracts

total_insurance_cost
```

**Common Bugs to Avoid:**
- **Calculating "index units" (portfolio_value / index_level) and treating this as number of contracts—this omits the multiplier and understates contracts by factor of 100**
- Confusing per-index-point pricing with per-contract pricing
- Not recognizing that each option contract covers (index_level × multiplier) dollars of exposure
- Forgetting to multiply option price by contract multiplier when calculating total cost

**Example (sanitized):**

> **Scenario:** $500M portfolio, index at 2,000, put option price $80 per index point, standard multiplier 100.
>
> **Wrong approach:** 
> - Calculate "units" = 500M / 2000 = 250,000
> - Total cost = $80 × 250,000 = $20M (incorrect—treats units as contracts)
>
> **Correct approach:**
> - Contracts needed = 500M / (2000 × 100) = 2,500 contracts
> - Cost per contract = $80 × 100 = $8,000
> - Total cost = $8,000 × 2,500 = $20M (same result, but correct reasoning)
> - Note: In this case the numbers coincidentally match, but the logic matters for verification and when parameters change