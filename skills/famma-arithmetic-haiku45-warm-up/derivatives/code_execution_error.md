# DETAILED SKILL PATTERNS FOR DERIVATIVES CALCULATION ERRORS

---

## Pattern: Futures Hedge Ratio with Conversion Factor Adjustment

**Description:** When calculating the number of futures contracts needed for hedging, the conversion factor adjusts the effective BPV of the futures contract. A conversion factor < 1 means the cheapest-to-deliver bond is MORE price-sensitive, requiring FEWER contracts (multiply BPV by conversion factor, not divide).

**When to Use:** Futures hedging problems involving basis point value (BPV), duration matching, or immunization where a conversion factor for the cheapest-to-deliver bond is provided.

**Procedure:**
1. Formula: `Number of Contracts = Net BPV Exposure / (BPV per Contract × Conversion Factor)`
2. Calculate net exposure: `Net BPV = |BPV_assets - BPV_liabilities|`
3. Adjust futures BPV: `Effective BPV = BPV_per_contract × Conversion_Factor`
4. Determine direction: If assets > liabilities, SELL futures; if liabilities > assets, BUY futures
5. Return rounded whole number of contracts

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

round(number_of_contracts)
```

**Common Bugs to Avoid:**
- Dividing by conversion factor instead of multiplying (inverts the adjustment)
- Forgetting to take absolute value when determining hedge size
- Using print() instead of returning the expression
- Not rounding to whole contracts

---

## Pattern: Black-Scholes Option Pricing with Correct Output Alignment

**Description:** When implementing Black-Scholes or Black-76 models, ensure the final computed value from code execution matches the natural language explanation. The code must return the expression value, not print it, and the explanation must reference the actual computed result.

**When to Use:** European option pricing problems using Black-Scholes (equity options), Black-76 (futures options), or Garman-Kohlhagen (FX options) models.

**Procedure:**
1. Formula: `Call = S₀ × N(d₁) - K × e^(-rT) × N(d₂)` where `d₁ = [ln(S₀/K) + (r + σ²/2)T] / (σ√T)` and `d₂ = d₁ - σ√T`
2. Import required libraries: `math`, `scipy.stats.norm`
3. Calculate d₁ and d₂ using natural logarithm and square root functions
4. Compute N(d₁) and N(d₂) using `norm.cdf()`
5. Apply discount factor and return final expression (not print)
6. Verify: Call price should be between 0 and S₀; Put price between 0 and K×e^(-rT)

**Code Example:**

**Scenario:** Stock price $105, strike $100, risk-free rate 3%, volatility 25%, maturity 0.75 years.

**Correct Code:**
```python
import math
from scipy.stats import norm

# Parameters
S0 = 105
K = 100
r = 0.03
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

# Return expression (not print)
round(call_price, 2)
```

**Common Bugs to Avoid:**
- Using `print(call_price)` instead of returning the expression
- Writing explanation with different numbers than code computes
- Forgetting to import `scipy.stats.norm` for CDF calculation
- Using `math.log10()` instead of `math.log()` (natural log)
- Sanity check failure: not verifying 0 < call < S0

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

**Description:** The risk-neutral probability density g(K) is derived from the second derivative of call prices with respect to strike: g(K) = e^(rT) × [C(K-δ) + C(K+δ) - 2C(K)] / δ². This requires three consecutive strike prices. Boundary strikes cannot be computed without extrapolation.

**When to Use:** Implied probability distribution extraction from option prices; volatility smile analysis; questions asking for probability in a strike range.

**Procedure:**
1. Formula: `g(K) = e^(rT) × [C(K-δ) + C(K+δ) - 2C(K)] / δ²`
2. Calculate call prices for all strikes using Black-Scholes with given implied volatilities
3. For each interior strike K (not first or last), compute density using butterfly spread formula
4. To find probability in range [K₁, K₂]: integrate density using trapezoidal rule
5. Handle boundaries: either extrapolate density or note that probability outside computed range is residual
6. Verify: Total probability should be close to 1.0 (within numerical error)

**Code Example:**

**Scenario:** Strikes [80, 85, 90, 95, 100] with implied vols [0.22, 0.20, 0.18, 0.20, 0.22]. Stock $90, rate 5%, maturity 1 year. Find probability between 85 and 95.

**Correct Code:**
```python
import numpy as np
from scipy.stats import norm

# Parameters
S0 = 90
r = 0.05
T = 1.0
strikes = np.array([80, 85, 90, 95, 100])
implied_vols = np.array([0.22, 0.20, 0.18, 0.20, 0.22])
delta = strikes[1] - strikes[0]

# Black-Scholes call price function
def bs_call(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)

# Calculate call prices
call_prices = np.array([bs_call(S0, K, T, r, vol) for K, vol in zip(strikes, implied_vols)])

# Calculate probability densities at interior strikes only
densities = []
interior_strikes = []

for i in range(1, len(strikes) - 1):
    c_minus = call_prices[i-1]
    c_center = call_prices[i]
    c_plus = call_prices[i+1]
    
    # Breeden-Litzenberger formula
    g_K = np.exp(r*T) * (c_minus + c_plus - 2*c_center) / (delta**2)
    densities.append(g_K)
    interior_strikes.append(strikes[i])

densities = np.array(densities)
interior_strikes = np.array(interior_strikes)

# Probability between 85 and 95 (interior strikes: 85, 90, 95)
# Use trapezoidal integration
probability_85_to_95 = np.trapz(densities, interior_strikes)

round(probability_85_to_95, 4)
```

**Common Bugs to Avoid:**
- Attempting to compute density at boundary strikes (first/last) without extrapolation
- Using point densities directly as probabilities (must integrate)
- Incorrect integration: using sum instead of trapezoidal rule
- Forgetting the e^(rT) discount factor in Breeden-Litzenberger formula
- Not verifying that computed densities are non-negative

---

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