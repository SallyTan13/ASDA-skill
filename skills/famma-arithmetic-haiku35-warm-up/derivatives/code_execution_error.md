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

---

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

**Description:** Incorrect implementation of the duration-adjusted futures hedge ratio formula for rebalancing bond portfolios, including errors in calculating the number of contracts needed.

**When to Use:** When rebalancing fixed-income portfolios using bond futures to achieve target duration or allocation, given current and target portfolio values and durations.

**Procedure:**
1. Formula: N_f = [(D_target × V_target) - (D_current × V_current)] / (D_futures × P_futures)
2. Calculate target portfolio value based on desired allocation percentage
3. Calculate current portfolio value and duration
4. Compute duration-dollar change needed: ΔDD = (D_target × V_target) - (D_current × V_current)
5. Divide by futures duration-dollar per contract: D_futures × P_futures
6. Round to nearest integer for number of contracts
7. Negative result means sell futures; positive means buy futures

**Code Example:**

**Scenario:** Rebalance bond portfolio from ¥30B (duration 5.0) to target ¥24B (duration 5.0) using futures with duration 7.2 and price ¥5,000,000
**Correct Code:**
```python
import math

# Current portfolio
current_value = 30_000_000_000  # ¥30 billion
current_duration = 5.0

# Target portfolio
target_value = 24_000_000_000  # ¥24 billion
target_duration = 5.0  # Maintain same duration

# Futures characteristics
futures_duration = 7.2
futures_price = 5_000_000  # ¥5 million per contract

# Calculate duration-dollar adjustment needed
current_DD = current_duration * current_value
target_DD = target_duration * target_value
delta_DD = target_DD - current_DD

# Calculate number of futures contracts
futures_DD_per_contract = futures_duration * futures_price
num_contracts = delta_DD / futures_DD_per_contract

# Round to nearest integer
num_contracts_rounded = round(num_contracts)

# Negative means sell futures
abs(num_contracts_rounded)  # Return absolute value if question asks "number to sell"
```

**Common Bugs to Avoid:**
- Using simple value ratio without duration adjustment: (V_target - V_current) / P_futures
- Forgetting to multiply duration by value for both current and target portfolios
- Not accounting for cash position duration when present (typically 0.25)
- Sign errors: forgetting that negative result means sell, positive means buy
- Using futures beta instead of duration for bond futures
- Dividing by futures price only, omitting futures duration from denominator

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