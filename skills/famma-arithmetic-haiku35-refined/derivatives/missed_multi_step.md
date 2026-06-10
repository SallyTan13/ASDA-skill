# SKILL PATTERNS FOR DERIVATIVES - MULTI-STEP REASONING FAILURES (PoT)

## Pattern: Binomial Tree Path Enumeration for Expected Life

**Description:** Computing expected life in employee stock options requires enumerating all possible exit paths through a binomial tree (early exercise, employee departure, or maturity), calculating the time and probability for each path, then computing the probability-weighted average time across all paths.

**When to Use:** Employee stock option valuation questions asking for "expected life" or "average holding period" with binomial trees, early exercise probabilities, and employee turnover rates.

**Procedure:**
1. Formula: Expected Life = Σ(probability_of_path_i × time_of_exit_i) for all paths
2. Enumerate all nodes in the tree chronologically from time 0 to maturity
3. For each node, identify possible exit events: (a) voluntary early exercise with given probability, (b) forced exercise due to employee departure, (c) continuation to next period
4. Track cumulative probability of reaching each node (product of branch probabilities and survival rates)
5. At each potential exit node, calculate: exit_probability = reach_probability × (exercise_prob + (1 - exercise_prob) × departure_prob)
6. Accumulate: total_expected_life += exit_probability × time_at_node
7. Return the sum across all exit scenarios

**Code Example:**

**Scenario:** A 6-year employee stock option with 2-year time steps (3 periods). Employee departure rate is 4% per step. Early exercise probabilities at in-the-money nodes at t=2, t=4 are 50% and 70% respectively. Up probability p=0.52.

**Correct Code:**
```python
import numpy as np

# Tree parameters
time_steps = [0, 2, 4, 6]
p_up = 0.52
p_down = 1 - p_up
departure_rate = 0.04
survival_rate = 1 - departure_rate

# Early exercise probabilities at specific nodes (node_id: prob)
early_exercise_probs = {
    'node_2_up': 0.50,    # at t=2, up state
    'node_4_upup': 0.70   # at t=4, up-up state
}

# Track all exit scenarios: (time, cumulative_probability)
exit_scenarios = []

# Path 1: Exit at t=2, up node, early exercise
prob_reach_2_up = p_up * survival_rate  # survive to t=2
prob_exit_2_up = prob_reach_2_up * early_exercise_probs['node_2_up']
exit_scenarios.append((2, prob_exit_2_up))

# Path 2: Exit at t=2, up node, forced by departure (didn't voluntarily exercise)
prob_exit_2_up_forced = prob_reach_2_up * (1 - early_exercise_probs['node_2_up']) * departure_rate
exit_scenarios.append((2, prob_exit_2_up_forced))

# Path 3: Continue from t=2 up to t=4 up-up, then exit
prob_continue_2_up = prob_reach_2_up * (1 - early_exercise_probs['node_2_up']) * survival_rate
prob_reach_4_upup = prob_continue_2_up * p_up * survival_rate
prob_exit_4_upup = prob_reach_4_upup * early_exercise_probs['node_4_upup']
exit_scenarios.append((4, prob_exit_4_upup))

# Path 4: Reach t=4 up-up, don't exercise, forced departure
prob_exit_4_upup_forced = prob_reach_4_upup * (1 - early_exercise_probs['node_4_upup']) * departure_rate
exit_scenarios.append((4, prob_exit_4_upup_forced))

# Path 5: Continue to maturity from t=4 up-up
prob_continue_4_upup = prob_reach_4_upup * (1 - early_exercise_probs['node_4_upup']) * survival_rate
prob_reach_6_from_upup = prob_continue_4_upup * 1.0  # reaches maturity
exit_scenarios.append((6, prob_reach_6_from_upup))

# Path 6-10: Similar logic for down paths (node_2_down, node_4_updown, etc.)
prob_reach_2_down = p_down * survival_rate
# Assume no early exercise at down nodes (out of money)
prob_continue_2_down = prob_reach_2_down * survival_rate
prob_reach_6_from_down_paths = prob_continue_2_down * survival_rate * 1.0
exit_scenarios.append((6, prob_reach_6_from_down_paths))

# Calculate expected life
expected_life = sum(time * prob for time, prob in exit_scenarios)

expected_life  # Result: weighted average time
```

**Common Bugs to Avoid:**
- Using a simple weighted average formula instead of path enumeration
- Forgetting to multiply by survival_rate at each step
- Not accounting for forced exercise upon departure
- Confusing conditional probabilities (exercise given reach) with joint probabilities
- Missing the distinction between voluntary and forced exits

---

## Pattern: Event-Driven Volatility Regime Option Pricing

**Description:** When option pricing involves uncertain future volatility regimes triggered by discrete events (lawsuits, announcements), compute risk-neutral probabilities from expected stock prices, calculate option values in each regime using regime-specific volatilities, then average using risk-neutral weights to get today's price. Implied volatility is then the single volatility that produces this composite price in Black-Scholes.

**When to Use:** Questions involving options where volatility depends on future discrete events (regulatory decisions, earnings announcements, lawsuits) with different volatility outcomes for each scenario.

**Procedure:**
1. Formula: Option_Price_Today = Σ(q_i × BS(S_i, K, T, σ_i, r)) where q_i are risk-neutral probabilities
2. Calculate risk-neutral probability for each scenario: q = (S_0 × e^(rT) - S_down) / (S_up - S_down)
3. For each scenario, compute option value using Black-Scholes with scenario-specific parameters (stock price after event, volatility)
4. Compute weighted average option price: C_composite = Σ(q_i × C_i)
5. Solve for implied volatility: find σ such that BS(S_0, K, T, σ, r) = C_composite using numerical root-finding
6. Return the implied volatility

**Code Example:**

**Scenario:** Stock at $80, FDA decision tomorrow. Approval: stock jumps to $100, volatility 20%. Rejection: stock drops to $65, volatility 35%. 6-month call option, strike $85, risk-free rate 4%.

**Correct Code:**
```python
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq

def black_scholes_call(S, K, T, sigma, r):
    """Black-Scholes call option price"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# Market parameters
S0 = 80
K = 85
T = 0.5  # 6 months
r = 0.04

# Event scenarios
S_approval = 100
sigma_approval = 0.20
S_rejection = 65
sigma_rejection = 0.35

# Step 1: Calculate risk-neutral probabilities
# Under risk-neutral measure: S0 * exp(r*T) = q * S_approval + (1-q) * S_rejection
forward_price = S0 * np.exp(r * T)
q_approval = (forward_price - S_rejection) / (S_approval - S_rejection)
q_rejection = 1 - q_approval

# Step 2: Calculate option values in each scenario
# Note: After event, time to maturity is still T (event is "tomorrow" ≈ immediate)
C_approval = black_scholes_call(S_approval, K, T, sigma_approval, r)
C_rejection = black_scholes_call(S_rejection, K, T, sigma_rejection, r)

# Step 3: Compute composite option price today
C_composite = q_approval * C_approval + q_rejection * C_rejection

# Step 4: Solve for implied volatility
def objective(sigma):
    return black_scholes_call(S0, K, T, sigma, r) - C_composite

implied_vol = brentq(objective, 0.01, 2.0)

implied_vol  # Result: single volatility matching composite price
```

**Common Bugs to Avoid:**
- Using equal probabilities (0.5, 0.5) instead of risk-neutral probabilities
- Forgetting to adjust time to maturity after the event
- Using arithmetic average of volatilities instead of pricing separately then averaging
- Not importing scipy.optimize for root-finding
- Confusing physical probabilities with risk-neutral probabilities

---

## Pattern: Coupon Bond Option Decomposition in Term Structure Models

**Description:** Pricing options on coupon-bearing bonds in one-factor term structure models requires decomposing the bond into zero-coupon components, finding the critical rate r* where bond price equals strike, computing individual zero-coupon option prices with strikes set at their values when r=r*, then summing all component option values.

**When to Use:** Questions about European options on coupon-bearing bonds in Hull-White, Vasicek, or Ho-Lee models, especially when analytical formulas for zero-coupon bond options are provided.

**Procedure:**
1. Formula: Option_Value = Σ(Option_on_ZCB_i) where each ZCB represents a coupon or principal payment
2. Identify all cash flows from the coupon bond: coupon payments and principal
3. Solve for critical rate r*: find r such that Σ(CF_i × P(T, T_i, r)) = K, where P is zero-coupon bond price
4. For each cash flow at time T_i, compute strike K_i = CF_i × P(T, T_i, r*)
5. Calculate volatility parameter σ_p for each component: σ_p = (σ/a) × [1 - exp(-a(T_i - T))] for Hull-White
6. Price each zero-coupon bond option using analytical formula (e.g., equation 32.10)
7. Sum all component option values and return total

**Code Example:**

**Scenario:** Price a 1.5-year call on a 3-year bond (principal 100, 6% annual coupon paid semiannually). Strike 102. Hull-White model: a=0.08, σ=0.02, flat term structure at 5% continuously compounded.

**Correct Code:**
```python
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq

# Model parameters
a = 0.08
sigma = 0.02
r_flat = 0.05

# Option and bond parameters
T_option = 1.5
T_maturity = 3.0
principal = 100
coupon_rate = 0.06
coupon_freq = 2  # semiannual
K_strike = 102

# Generate cash flows
coupon_payment = principal * coupon_rate / coupon_freq
payment_times = np.arange(0.5, T_maturity + 0.01, 0.5)
cash_flows = [coupon_payment if t < T_maturity else coupon_payment + principal 
              for t in payment_times]

# Zero-coupon bond price function
def zcb_price(t, T, r):
    """Price of zero-coupon bond from t to T given short rate r"""
    return np.exp(-r * (T - t))

# Bond price function given short rate at option maturity
def bond_price_at_T(r_star):
    """Price of coupon bond at T_option given short rate r_star"""
    price = 0
    for cf, t_pay in zip(cash_flows, payment_times):
        if t_pay > T_option:
            price += cf * zcb_price(T_option, t_pay, r_star)
    return price

# Step 1: Find critical rate r*
r_star = brentq(lambda r: bond_price_at_T(r) - K_strike, -0.1, 0.3)

# Step 2: Calculate strikes for each zero-coupon component
component_strikes = []
for cf, t_pay in zip(cash_flows, payment_times):
    if t_pay > T_option:
        K_i = cf * zcb_price(T_option, t_pay, r_star)
        component_strikes.append((cf, t_pay, K_i))

# Step 3: Price each zero-coupon bond option using Hull-White formula
def hw_zcb_call(L, K, T, s, a, sigma, r_flat):
    """Hull-White zero-coupon bond call option price"""
    P_0_T = np.exp(-r_flat * T)
    P_0_s = np.exp(-r_flat * s)
    
    # Volatility parameter
    sigma_p = (sigma / a) * (1 - np.exp(-a * (s - T)))
    
    # Black-like formula
    h = (1 / sigma_p) * np.log(L * P_0_s / (K * P_0_T)) + sigma_p / 2
    
    call_price = L * P_0_s * norm.cdf(h) - K * P_0_T * norm.cdf(h - sigma_p)
    return call_price

# Step 4: Sum all component options
total_option_value = 0
for cf, t_pay, K_i in component_strikes:
    option_value = hw_zcb_call(cf, K_i, T_option, t_pay, a, sigma, r_flat)
    total_option_value += option_value

total_option_value  # Result: sum of all zero-coupon bond options
```

**Common Bugs to Avoid:**
- Forgetting to filter cash flows that occur after option maturity
- Using the wrong volatility formula (must be σ_p, not σ directly)
- Not solving for r* numerically (it's not analytically available)
- Confusing strike K (for coupon bond) with K_i (for each zero-coupon component)
- Missing the principal payment in the final cash flow

---

## Pattern: Quoted vs Cash Price Adjustment for Bond Options

**Description:** Bond options may have strikes specified as quoted prices (clean price) or cash prices (dirty price = clean + accrued interest). When converting between them, calculate accrued interest at the option's maturity date, adjust the strike accordingly, then reprice the option using the modified strike in Black's model.

**When to Use:** Bond option questions that explicitly mention "quoted price" vs "cash price" or "clean price" vs "dirty price", especially when given one price type and asked to compute the other.

**Procedure:**
1. Formula: Cash_Price = Quoted_Price + Accrued_Interest; Option_Cash = Option_Quoted adjusted by strike difference
2. Identify the coupon rate, payment frequency, and time since last coupon payment at option maturity
3. Calculate accrued interest: AI = (Coupon_per_period) × (Days_since_last_payment / Days_in_period)
4. If given quoted strike K_quoted, compute cash strike: K_cash = K_quoted + AI
5. If given option price with quoted strike, reprice with cash strike using Black's model
6. Adjust option value: For calls, higher strike → lower value; for puts, higher strike → higher value
7. Return the adjusted option price

**Code Example:**

**Scenario:** European put on a 8-year bond, principal 100, 7% annual coupon (semiannual payments). Option life 1.75 years, quoted strike 110. Given: option price with quoted strike is $3.20, bond's quoted price is 118.50. Convert to cash strike price option value.

**Correct Code:**
```python
import numpy as np
from scipy.stats import norm

# Bond parameters
principal = 100
coupon_rate = 0.07
payment_freq = 2
coupon_per_period = principal * coupon_rate / payment_freq

# Option parameters
T_option = 1.75
K_quoted = 110
option_price_quoted = 3.20
bond_quoted_price = 118.50

# Step 1: Calculate accrued interest at option maturity
# At T=1.75 years, last coupon was at t=1.5, next at t=2.0
time_since_last_coupon = 1.75 - 1.5  # 0.25 years
period_length = 0.5  # semiannual
accrued_interest = coupon_per_period * (time_since_last_coupon / period_length)

# Step 2: Convert strikes
K_cash = K_quoted + accrued_interest
bond_cash_price = bond_quoted_price + accrued_interest

# Step 3: Adjust option price using Black's model relationship
# For a put: P_cash = P_quoted + (K_cash - K_quoted) * exp(-r*T) * adjustment
# Simplified: the difference in intrinsic value propagates through
# More precisely, reprice using Black's model with both strikes

# Black's model for bond put
def black_bond_put(F, K, T, sigma, r):
    """Black's model for European put on bond"""
    d1 = (np.log(F / K) + 0.5 * sigma**2 * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return K * np.exp(-r * T) * norm.cdf(-d2) - F * np.exp(-r * T) * norm.cdf(-d1)

# Assume we can back out implied volatility from quoted price
# Then reprice with cash strike (simplified approach)
r = 0.05  # given or implied from term structure
forward_bond_price = bond_cash_price * np.exp(r * T_option)

# For demonstration: assume implied vol is 15% (would solve from quoted price)
sigma_implied = 0.15

# Price with quoted strike
put_quoted_check = black_bond_put(forward_bond_price - accrued_interest, 
                                   K_quoted, T_option, sigma_implied, r)

# Price with cash strike
put_cash = black_bond_put(forward_bond_price, K_cash, T_option, sigma_implied, r)

# Adjustment factor (simplified)
strike_adjustment = (K_cash - K_quoted) * np.exp(-r * T_option)
option_price_cash = option_price_quoted - strike_adjustment  # for put, higher strike increases value

option_price_cash  # Result: option value with cash strike
```

**Common Bugs to Avoid:**
- Using accrued interest at current time instead of at option maturity
- Forgetting that accrued interest changes the effective strike, not just the bond price
- Applying the wrong sign for adjustment (puts vs calls behave differently)
- Not accounting for the time value discount factor in the adjustment
- Confusing the bond's quoted price with the option's strike price

---

## Pattern: Multi-Step Numerical Root-Finding for Implicit Parameters

**Description:** Many derivatives problems require solving for implicit parameters (critical rates, implied volatilities, breakeven values) that cannot be isolated algebraically. Use numerical root-finding (scipy.optimize.brentq or newton) with well-chosen bounds, and verify the solution satisfies the original constraint.

**When to Use:** Questions requiring "solve for X such that f(X) = target" where f is a complex pricing formula (Black-Scholes, bond pricing, tree valuation), especially for implied volatility or critical rate calculations.

**Procedure:**
1. Formula: Find x such that f(x) = target using numerical solver
2. Define objective function: obj(x) = f(x) - target
3. Determine reasonable bounds for the parameter (e.g., volatility: [0.01, 3.0], rates: [-0.1, 0.5])
4. Use scipy.optimize.brentq for bracketed root-finding (requires sign change) or newton for faster convergence
5. Verify solution: compute f(x_solution) and check |f(x_solution) - target| < tolerance
6. Handle edge cases: if no root exists in bounds, return boundary value or raise error
7. Return the solved parameter

**Code Example:**

**Scenario:** Find the implied volatility of a call option: S=$55, K=$50, T=0.75 years, r=3%, market price=$8.50.

**Correct Code:**
```python
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq, newton

def black_scholes_call(S, K, T, sigma, r):
    """Black-Scholes call option price"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# Market parameters
S = 55
K = 50
T = 0.75
r = 0.03
market_price = 8.50

# Step 1: Define objective function
def objective(sigma):
    return black_scholes_call(S, K, T, sigma, r) - market_price

# Step 2: Set reasonable bounds for volatility
sigma_lower = 0.01
sigma_upper = 2.0

# Step 3: Solve using brentq (requires sign change at bounds)
try:
    implied_vol = brentq(objective, sigma_lower, sigma_upper)
except ValueError:
    # No sign change - check boundaries
    if abs(objective(sigma_lower)) < 0.01:
        implied_vol = sigma_lower
    elif abs(objective(sigma_upper)) < 0.01:
        implied_vol = sigma_upper
    else:
        raise ValueError("No solution found in bounds")

# Step 4: Verify solution
computed_price = black_scholes_call(S, K, T, implied_vol, r)
error = abs(computed_price - market_price)

# Step 5: Sanity check
assert error < 0.01, f"Solution error too large: {error}"

implied_vol  # Result: volatility that matches market price
```

**Common Bugs to Avoid:**
- Using bounds that don't bracket the root (causing ValueError in brentq)
- Not handling cases where market price is outside model's feasible range
- Forgetting to import scipy.optimize
- Using optimize.fsolve without good initial guess (may not converge)
- Not verifying the solution actually satisfies the constraint
- Confusing tolerance parameters (xtol vs ftol in different solvers)