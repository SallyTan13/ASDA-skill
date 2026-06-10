# DERIVATIVES CALCULATION SKILL PATTERNS

## Pattern: Black-Scholes-Merton Option Pricing Implementation

**Description:** Incorrect implementation of the Black-Scholes-Merton formula for European options, particularly errors in time conversion, d1/d2 parameter calculation, and cumulative normal distribution application.

**When to Use:** When calculating European call/put option prices given stock price, strike price, risk-free rate, volatility, and time to maturity.

**Procedure:**
1. Formula: C = S₀N(d₁) - Ke^(-rT)N(d₂), where d₁ = [ln(S₀/K) + (r + σ²/2)T] / (σ√T) and d₂ = d₁ - σ√T
2. Convert all time periods to years (months/12, days/365)
3. Calculate d1 using natural logarithm of S/K, add drift term (r + 0.5*σ²)*T, divide by σ*sqrt(T)
4. Calculate d2 as d1 minus σ*sqrt(T)
5. Apply cumulative standard normal distribution N(d1) and N(d2)
6. Compute call price with discount factor applied to strike price only
7. Return the final value as an expression (not printed)

**Code Example:**

**Scenario:** Calculate a European call option price where S=$100, K=$95, r=5% annual continuous, T=4 months, σ=40% annual
**Correct Code:**
```python
import math
from scipy.stats import norm

# Given parameters
S = 100  # Current stock price
K = 95   # Strike price
r = 0.05  # Risk-free rate (annual, continuous)
T = 4/12  # Time to maturity in years
sigma = 0.40  # Volatility (annual)

# Calculate d1 and d2
d1 = (math.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*math.sqrt(T))
d2 = d1 - sigma*math.sqrt(T)

# Calculate call option price
N_d1 = norm.cdf(d1)
N_d2 = norm.cdf(d2)
call_price = S*N_d1 - K*math.exp(-r*T)*N_d2

call_price  # Result as expression
```

**Common Bugs to Avoid:**
- Using print() instead of expression on last line (causes None return in PoT)
- Forgetting to convert time to years (using T=5 instead of T=5/12 for months)
- Incorrect d1 formula: missing the +0.5*σ² term or using wrong sign
- Applying discount factor to both terms instead of just the strike price term
- Using math.log10() instead of math.log() (natural logarithm)
- Forgetting to import scipy.stats.norm for cumulative distribution
- **Syntax errors like using commas in numbers: `V0 = 1,520` creates tuple instead of 1520**
## Pattern: Breeden-Litzenberger Risk-Neutral Density Extraction

**Description:** Incorrect implementation of extracting risk-neutral probability distributions from option prices using the Breeden-Litzenberger formula, including confusion between probability density and total probability over intervals.

**When to Use:** When extracting implied probability distributions from volatility smiles or calculating total probability over price ranges using butterfly spreads.

**Procedure:**
1. Formula: g(K) = e^(rT) × (c₁ + c₃ - 2c₂) / δ², where c₁, c₂, c₃ are call prices at strikes K-δ, K, K+δ
2. Calculate call option prices at each strike using Black-Scholes with corresponding implied volatilities
3. For each interval [K-δ, K+δ], compute probability density g(K) using the formula
4. Convert density to total probability by multiplying by interval width: P(interval) = g(K) × δ
5. Sum probabilities across multiple intervals for cumulative probability
6. Verify total probability sums to approximately 1.0 (or close, accounting for tail truncation)
7. Return probability as decimal between 0 and 1

**Code Example:**

**Scenario:** Calculate total probability between strikes 8 and 11 given current price=10, r=2%, T=0.5 years, strikes [7,8,9,10,11,12] with implied vols [25%,24%,23%,22%,23%,24%]
**Correct Code:**
```python
import math
from scipy.stats import norm

def black_scholes_call(S, K, r, T, sigma):
    d1 = (math.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*math.sqrt(T))
    d2 = d1 - sigma*math.sqrt(T)
    return S*norm.cdf(d1) - K*math.exp(-r*T)*norm.cdf(d2)

# Parameters
S = 10
r = 0.02
T = 0.5
strikes = [7, 8, 9, 10, 11, 12]
vols = [0.25, 0.24, 0.23, 0.22, 0.23, 0.24]
delta = 1  # Strike spacing

# Calculate call prices
call_prices = [black_scholes_call(S, K, r, T, vol) for K, vol in zip(strikes, vols)]

# Calculate probability densities and total probabilities
total_prob = 0
for i in range(1, len(strikes)-1):
    # Breeden-Litzenberger formula for density
    g_K = math.exp(r*T) * (call_prices[i-1] + call_prices[i+1] - 2*call_prices[i]) / (delta**2)
    # Convert density to probability over interval
    prob_interval = g_K * delta
    # Sum probabilities in range [8, 11]
    if 8 <= strikes[i] <= 11:
        total_prob += prob_interval

total_prob  # Result between 0 and 1
```

**Common Bugs to Avoid:**
- Returning density g(K) instead of total probability g(K)×δ
- Forgetting the discount factor e^(rT) in the Breeden-Litzenberger formula
- Not multiplying by interval width δ when computing total probability
- Returning values >1 or <0 (indicates formula error or missing normalization)
- Using wrong sign in butterfly spread formula (should be c₁ + c₃ - 2c₂)
- Incorrect loop bounds causing index errors when accessing i-1 or i+1

---

## Pattern: Duration-Based Futures Hedging for Fixed Income

**Description:** Incorrect implementation of the duration-adjusted futures hedge ratio formula for rebalancing bond portfolios, including errors in calculating the number of contracts needed and failing to account for conversion factors in Treasury bond futures.

**When to Use:** When rebalancing fixed-income portfolios using bond futures to achieve target duration or allocation, given current and target portfolio values and durations. Also applies when using basis point value (BPV) for immunization strategies with Treasury futures that have conversion factors.

**When NOT to Use:** 
- When conversion factor is not provided (use simple BPV ratio instead)
- When dealing with equity index futures (use beta-adjusted formula instead)
- When the question asks for duration matching without futures

**Procedure:**
1. Identify if using duration-dollar or BPV approach and whether conversion factor applies
2. For duration-dollar: N_f = [(D_target × V_target) - (D_current × V_current)] / (D_futures × P_futures)
3. For BPV with conversion factor: N_f = (Net BPV) / (Futures BPV per contract × Conversion Factor)
4. Calculate target portfolio value based on desired allocation percentage
5. Calculate current portfolio value and duration/BPV
6. Compute duration-dollar or BPV change needed
7. **CRITICAL**: If conversion factor is provided, divide by (Futures BPV × CF), not just Futures BPV
8. Round to nearest integer for number of contracts
9. Negative result means sell futures; positive means buy futures

**Common Mistakes to Avoid:**
- **CRITICAL: Multiplying net BPV by conversion factor instead of dividing futures BPV by it**
- Using simple value ratio without duration adjustment: (V_target - V_current) / P_futures
- Forgetting to multiply duration by value for both current and target portfolios
- Not accounting for cash position duration when present (typically 0.25)
- Sign errors: forgetting that negative result means sell, positive means buy
- Using futures beta instead of duration for bond futures
- Dividing by futures price only, omitting futures duration from denominator
- Confusing BPV per contract with BPV per $100,000 par value (may need scaling)

**Example (sanitized):**
> **Scenario:** An immunizing portfolio needs rebalancing. Current asset BPV is €35,000, liability BPV is €18,000 (net exposure €17,000). Treasury futures have BPV of €52 per €100,000 par value with a conversion factor of 0.75. How many contracts to sell?
> 
> **Wrong approach:** Multiplying net BPV by conversion factor
> ```python
> net_BPV = 35_000 - 18_000  # €17,000
> futures_BPV = 52
> conversion_factor = 0.75
> num_contracts = (net_BPV * conversion_factor) / futures_BPV  # WRONG!
> # This gives 245 contracts but is INCORRECT
> ```
> 
> **Correct approach:** Dividing by (Futures BPV × Conversion Factor)
> ```python
> # Step 1: Calculate net BPV exposure
> asset_BPV = 35_000
> liability_BPV = 18_000
> net_BPV = asset_BPV - liability_BPV  # €17,000
> 
> # Step 2: Identify futures characteristics
> futures_BPV_per_contract = 52  # per €100,000 par
> conversion_factor = 0.75
> 
> # Step 3: Divide by (Futures BPV × CF)
> # Formula: N_f = Net BPV / (Futures BPV × CF)
> denominator = futures_BPV_per_contract * conversion_factor  # 52 × 0.75 = 39
> num_contracts = net_BPV / denominator  # 17,000 / 39 = 435.9
> 
> # Step 4: Round to nearest integer
> num_contracts_rounded = round(num_contracts)  # 436 contracts
> ```
> The conversion factor adjusts the hedge ratio because the cheapest-to-deliver bond differs from the standard futures contract specification.

---
## Pattern: Option Strategy Breakeven and Profitability Analysis

**Description:** Failed to correctly calculate breakeven points and profitability conditions for multi-leg option strategies like straddles, spreads, and butterflies, including errors in extracting option premiums and computing net cost.

**When to Use:** When analyzing long/short straddles, bull/bear spreads, butterfly spreads, or any multi-option strategy to determine breakeven prices or profitability regions.

**Procedure:**
1. Formula (Long Straddle): Breakeven at K ± total_premium; Profitable when |S_T - K| > total_premium
2. Extract option premiums from table/data for all legs of the strategy
3. Calculate net cost/credit: sum of premiums paid minus premiums received
4. For straddles: breakeven_lower = K - net_cost, breakeven_upper = K + net_cost
5. For spreads: breakeven = long_strike ± net_cost (sign depends on bull/bear)
6. Determine profitability region based on strategy type
7. Return the specific value requested (breakeven price, profit at given price, etc.)

**Code Example:**

**Scenario:** Long straddle at strike $50, call premium=$3.20, put premium=$2.80. Find lower breakeven and profit at $42.
**Correct Code:**
```python
# Long straddle parameters
strike = 50
call_premium = 3.20
put_premium = 2.80

# Total cost of strategy
total_premium = call_premium + put_premium

# Breakeven points
breakeven_lower = strike - total_premium
breakeven_upper = strike + total_premium

# Profit at specific price (e.g., $42)
price_at_expiration = 42
if price_at_expiration < strike:
    # Put is in the money
    intrinsic_value = strike - price_at_expiration
else:
    # Call is in the money
    intrinsic_value = price_at_expiration - strike

profit = intrinsic_value - total_premium

# Return requested value
breakeven_lower  # Or profit, depending on question
```

**Common Bugs to Avoid:**
- Using print() instead of returning expression value
- Extracting wrong premium values from tables (confusing call/put or strike prices)
- Forgetting to sum premiums for both legs of straddle
- Incorrect profitability condition: using ≥ instead of > for breakeven
- Sign errors in spread calculations (bull call spread vs bear put spread)
- Not accounting for whether strategy is long (pay premium) or short (receive premium)
- Returning breakeven instead of profit, or vice versa, based on question wording

---

## Pattern: Futures Contract Quantity for Equity Portfolio Rebalancing

**Description:** Incorrect calculation of the number of equity index futures contracts needed to temporarily adjust portfolio beta or allocation without liquidating positions.

**When to Use:** When rebalancing equity portfolios using index futures to achieve target allocation or beta, given current portfolio value, beta, and futures characteristics.

**Procedure:**
1. Formula: N_f = [(β_target × V_target) - (β_current × V_current)] / (β_futures × P_futures)
2. Determine target equity value based on desired allocation (e.g., 60% of total portfolio)
3. Calculate current equity value and beta
4. Compute beta-adjusted value change: Δ(βV) = (β_target × V_target) - (β_current × V_current)
5. Divide by futures beta-value per contract: β_futures × P_futures
6. Round to nearest integer
7. Negative result means sell futures; positive means buy futures

**Code Example:**

**Scenario:** Reduce equity from ¥40B (beta=1.20) to ¥35B (maintain beta=1.20) using futures with beta=1.10 and price=¥2,000,000
**Correct Code:**
```python
import math

# Current equity portfolio
current_equity_value = 40_000_000_000  # ¥40 billion
current_beta = 1.20

# Target equity portfolio
target_equity_value = 35_000_000_000  # ¥35 billion
target_beta = 1.20  # Maintain current beta

# Futures characteristics
futures_beta = 1.10
futures_price = 2_000_000  # ¥2 million per contract

# Calculate beta-adjusted value change
current_beta_value = current_beta * current_equity_value
target_beta_value = target_beta * target_equity_value
delta_beta_value = target_beta_value - current_beta_value

# Calculate number of futures contracts
futures_beta_value_per_contract = futures_beta * futures_price
num_contracts = delta_beta_value / futures_beta_value_per_contract

# Round to nearest integer
num_contracts_rounded = round(num_contracts)

abs(num_contracts_rounded)  # Absolute value if question asks "number to sell"
```

**Common Bugs to Avoid:**
- Using allocation percentage directly instead of converting to value
- Forgetting to multiply beta by value for beta-adjusted calculations
- Using portfolio beta in denominator instead of futures beta
- Not maintaining target beta when rebalancing (assuming beta changes)
- Confusing equity rebalancing formula with bond duration formula
- Code execution failure due to undefined variables or missing calculations

## Pattern: Black-Scholes-Merton with Dividend Yield

**Description:** Incorrect implementation of the Black-Scholes-Merton formula for European options on stocks paying continuous dividend yield, particularly errors in handling the dividend yield adjustment in the d1/d2 formulas and avoiding double-counting.

**When to Use:** When calculating European call/put option prices on stocks or indices that pay continuous dividend yield (q), given stock price, strike price, risk-free rate, dividend yield, volatility, and time to maturity.

**When NOT to Use:**
- When dividends are discrete payments (use dividend-adjusted stock price instead)
- When dealing with American options (requires different approach)
- When no dividend yield is mentioned (use standard Black-Scholes pattern)

**Procedure:**
1. Formula: c = S₀e^(-qT)N(d₁) - Ke^(-rT)N(d₂), where d₁ = [ln(S₀/K) + (r - q + σ²/2)T] / (σ√T) and d₂ = d₁ - σ√T
2. Convert all time periods to years (months/12, days/365)
3. **CRITICAL**: Calculate d1 using ORIGINAL S₀ (not adjusted) in the logarithm
4. In the d1 formula, use (r - q + 0.5*σ²) for the drift term
5. Calculate d2 as d1 minus σ*sqrt(T)
6. Apply cumulative standard normal distribution N(d1) and N(d2)
7. Multiply S₀ term by e^(-qT) and K term by e^(-rT)
8. Return the final value as an expression (not printed)

**Common Mistakes to Avoid:**
- **CRITICAL: Double-counting dividend yield by adjusting S₀ first AND using (r-q) in formula**
- Using S*e^(-qT) in the logarithm AND subtracting q in the drift term
- Forgetting the dividend yield discount on the stock price term
- Using (r + q) instead of (r - q) in the drift term
- Applying e^(-qT) to the strike price term instead of stock price term
- Confusing continuous yield (q) with discrete dividends

**Code Example:**

**Scenario:** Calculate a European put option on an index where S=1200, K=1140, r=6% annual, q=3% annual, T=6 months, σ=30% annual
**Correct Code:**
```python
import math
from scipy.stats import norm

# Given parameters
S = 1200  # Current index level
K = 1140  # Strike price
r = 0.06  # Risk-free rate (annual, continuous)
q = 0.03  # Dividend yield (annual, continuous)
T = 0.5   # Time to maturity in years
sigma = 0.30  # Volatility (annual)

# Calculate d1 and d2 using ORIGINAL S (not adjusted)
d1 = (math.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*math.sqrt(T))
d2 = d1 - sigma*math.sqrt(T)

# Calculate put option price with dividend yield adjustment
N_minus_d1 = norm.cdf(-d1)
N_minus_d2 = norm.cdf(-d2)
put_price = K*math.exp(-r*T)*N_minus_d2 - S*math.exp(-q*T)*N_minus_d1

put_price  # Result as expression
```

---

## Pattern: American Options with Discrete Dividends

**Description:** Calculation of American option prices when discrete dividend payments occur during the option's life. For American calls with dividends, a dividend-adjusted European approximation provides a reasonable lower bound. For precise valuation, numerical methods (binomial trees) are required but are beyond the scope of this pattern.

**When to Use:** When pricing American call options on stocks that pay known discrete dividends at specific future dates during the option's life, and an analytical approximation is acceptable.

**When NOT to Use:**
- When high precision is required (use binomial tree methods instead)
- When dividends are continuous yield (use Black-Scholes with dividend yield pattern)
- When dealing with European options only (use standard Black-Scholes pattern)
- When no dividends are paid during option life (use standard option pricing)
- **When the baseline already produces accurate results (defer to numerical methods)**

**Procedure:**
1. Subtract present value of all dividends from current stock price to get adjusted price
2. Formula: S_adjusted = S₀ - Σ(D_i × e^(-r×t_i)) where D_i are dividend amounts at times t_i
3. Calculate each dividend's present value using risk-free rate
4. Use adjusted stock price in Black-Scholes formula (European approximation)
5. **IMPORTANT**: This gives a lower bound for American call value; actual value may be higher due to early exercise opportunities
6. Return the European value with adjusted stock price
7. **DO NOT** add arbitrary "early exercise premium" formulas without theoretical justification

**Common Mistakes to Avoid:**
- **CRITICAL: Adding incorrect early exercise premium formulas like max(0, K - S*exp(rT))**
- Using future dividend values instead of present values
- Forgetting to discount dividends back to present
- Applying dividend adjustment to European puts (usually not optimal to exercise early)
- Using wrong discount rate for dividend present value
- Subtracting dividends from strike price instead of stock price
- Claiming the result is exact when it's only an approximation

**Code Example:**

**Scenario:** Calculate American call option where S=$100, K=$105, r=6% annual, T=12 months, σ=30%, with dividends of $2.00 at 3 months and 9 months
**Correct Code:**
```python
import math
from scipy.stats import norm

# Given parameters
S = 100     # Current stock price
K = 105     # Strike price
r = 0.06    # Risk-free rate (annual, continuous)
T = 1.0     # Time to maturity in years
sigma = 0.30  # Volatility (annual)

# Discrete dividends
div_amounts = [2.00, 2.00]
div_times = [3/12, 9/12]  # In years

# Calculate present value of dividends
pv_dividends = sum(D * math.exp(-r * t) for D, t in zip(div_amounts, div_times))

# Adjust stock price by subtracting PV of dividends
S_adjusted = S - pv_dividends

# Use Black-Scholes with adjusted stock price
# This provides a lower bound for the American call value
d1 = (math.log(S_adjusted/K) + (r + 0.5*sigma**2)*T) / (sigma*math.sqrt(T))
d2 = d1 - sigma*math.sqrt(T)

call_price = S_adjusted*norm.cdf(d1) - K*math.exp(-r*T)*norm.cdf(d2)

call_price  # European approximation (lower bound for American call)
```

---
## Pattern: Vasicek and CIR Interest Rate Model Bond Pricing

**Description:** Incorrect implementation of zero-coupon bond pricing formulas under Vasicek or Cox-Ingersoll-Ross (CIR) interest rate models, particularly errors in the A(t,T) and B(t,T) functions.

**When to Use:** When pricing zero-coupon bonds using Vasicek or CIR interest rate models, given mean reversion parameters (a, b), volatility (σ), initial short rate (r₀), and time to maturity (T).

**When NOT to Use:**
- When using standard yield curve discounting (use simple e^(-rT) formula)
- When dealing with coupon bonds (requires integration over payment dates)
- When model parameters are not provided

**Procedure:**
1. **Vasicek Model**: P(t,T) = A(t,T) × e^(-B(t,T)×r_t)
2. Calculate B(t,T) = [1 - e^(-a(T-t))] / a
3. Calculate A(t,T) = exp{[B(t,T) - (T-t)] × [ab - σ²/2] / a² - σ²B(t,T)² / (4a)}
4. **CRITICAL**: Use the EXACT formula from the problem context, not simplified versions
5. For CIR model: Use γ = √(a² + 2σ²) and different A(t,T), B(t,T) formulas
6. Multiply A(t,T) by e^(-B(t,T)×r₀) to get bond price
7. Return bond price as decimal (e.g., 0.38 for 38% of par)

**Common Mistakes to Avoid:**
- **CRITICAL: Using simplified A(t,T) formula instead of exact equation from context**
- Confusing Vasicek and CIR formulas (they have different A and B functions)
- Using wrong sign in exponential terms
- Forgetting the σ²B² / (4a) term in Vasicek A(t,T)
- Not extracting σ from the given "standard deviation of short-rate change" information
- Using annual volatility when model requires instantaneous volatility

**Code Example:**

**Scenario:** Calculate Vasicek bond price where a=0.1, b=0.1, r₀=10%, σ=0.02, T=10 years
**Correct Code:**
```python
import math

# Vasicek model parameters
a = 0.1      # Mean reversion rate
b = 0.1      # Long-term mean
r0 = 0.10    # Initial short rate
sigma = 0.02 # Volatility
T = 10       # Time to maturity
t = 0        # Current time

# Calculate B(t,T) using exact formula
tau = T - t
B = (1 - math.exp(-a * tau)) / a

# Calculate A(t,T) using EXACT formula from equation (31.8)
# A(t,T) = exp{[B(t,T) - (T-t)] * [ab - σ²/2] / a² - σ²B² / (4a)}
term1 = (B - tau) * (a*b - sigma**2/2) / (a**2)
term2 = (sigma**2 * B**2) / (4*a)
A = math.exp(term1 - term2)

# Bond price: P(t,T) = A(t,T) * exp(-B(t,T) * r0)
bond_price = A * math.exp(-B * r0)

bond_price  # Result as decimal
```