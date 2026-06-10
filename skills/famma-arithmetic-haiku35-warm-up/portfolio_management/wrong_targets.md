# SKILL PATTERNS FOR PORTFOLIO MANAGEMENT (Program of Thought)

## Pattern: Multi-Part Question Decomposition

**Description:** Questions may contain multiple distinct analytical targets requiring sequential calculations where later parts depend on earlier results or require reverse-engineering from constraints (e.g., "What is X? What is the maximum Y before Z becomes negative?").

**When to Use:** When question contains multiple question marks, conjunctions like "and," "also," or phrases like "what is the highest/lowest," "at what point," "before," indicating multiple deliverables.

**Procedure:**
1. Parse question into distinct sub-questions by identifying all interrogative phrases
2. Determine dependency order: which calculations must precede others
3. For forward calculations: compute metrics directly from given parameters
4. For reverse-engineering problems: set target condition (e.g., NPV=0), solve for intermediate variable (e.g., IRR), then back-solve for requested parameter
5. Return results as a dictionary or tuple with clear labels for each part

**Code Example:**

**Scenario:** A project has initial cost $50M, annual cash flows $12M for 8 years. Risk-free rate is 4%, market return is 11%. If beta is 1.5, what is the NPV? What is the maximum beta before NPV turns negative?

**Correct Code:**
```python
import numpy as np
from scipy.optimize import fsolve

# Part 1: Calculate NPV given beta
initial_cost = 50
annual_cf = 12
years = 8
rf = 0.04
rm = 0.11
beta = 1.5

# CAPM: required return
required_return = rf + beta * (rm - rf)

# NPV calculation
cash_flows = [-initial_cost] + [annual_cf] * years
npv = sum(cf / (1 + required_return)**t for t, cf in enumerate(cash_flows))

# Part 2: Find maximum beta where NPV = 0
# First find IRR (discount rate where NPV = 0)
def npv_func(rate):
    return sum(cf / (1 + rate)**t for t, cf in enumerate(cash_flows))

irr = fsolve(npv_func, 0.1)[0]

# Back-solve for beta using CAPM: IRR = rf + beta_max * (rm - rf)
beta_max = (irr - rf) / (rm - rf)

result = {
    'npv': round(npv, 2),
    'max_beta': round(beta_max, 2)
}
result
```

**Common Bugs to Avoid:**
- Stopping after first calculation when multiple targets exist
- Not recognizing reverse-engineering requirements (setting constraint equations)
- Failing to use root-finding methods (fsolve, brentq) for implicit solutions
- Returning only one value when multiple are requested

---

## Pattern: "Each" Keyword Expansion for Multiple Entities

**Description:** Questions using "each," "respectively," or "for both" require separate calculations for every entity mentioned, not aggregated or single results.

**When to Use:** When question asks about "each stock," "each asset," "both portfolios," or lists multiple entities and requests a metric for all of them individually.

**Procedure:**
1. Identify all distinct entities in the context (stocks, portfolios, assets)
2. Create separate calculation loops or explicit computations for each entity
3. Store results in a dictionary or list with clear entity labels
4. Return all individual results, not averages or single values
5. Verify output count matches entity count

**Code Example:**

**Scenario:** Market return has 60% probability of 8% and 40% probability of 20%. Stock X returns 5% or 30%, Stock Y returns 7% or 18% in these scenarios. What is the expected return on each stock?

**Correct Code:**
```python
# Probabilities
prob_low = 0.6
prob_high = 0.4

# Returns for each stock in each scenario
stock_x_returns = [0.05, 0.30]
stock_y_returns = [0.07, 0.18]

# Calculate expected return for EACH stock separately
expected_return_x = prob_low * stock_x_returns[0] + prob_high * stock_x_returns[1]
expected_return_y = prob_low * stock_y_returns[0] + prob_high * stock_y_returns[1]

# Return as dictionary with clear labels
result = {
    'stock_x': round(expected_return_x, 4),
    'stock_y': round(expected_return_y, 4)
}
result
```

**Common Bugs to Avoid:**
- Averaging across entities when individual values are requested
- Returning single scalar when multiple entities exist
- Confusing "each" with "average" or "total"
- Not labeling which result corresponds to which entity

---

## Pattern: Implicit Portfolio Construction from Context

**Description:** When context presents multiple assets and question refers to "this portfolio" or "the portfolio" without explicit weights, default assumption is equal-weighting across all presented assets unless otherwise specified.

**When to Use:** Questions about "portfolio variance," "portfolio return," "this portfolio" when context shows multiple securities but no explicit allocation is given.

**Procedure:**
1. Formula: Portfolio Return = Σ(w_i × R_i) where w_i = 1/N for equal weighting
2. Identify all assets in the context table/data
3. For each state/scenario, calculate portfolio return as equal-weighted average of all asset returns
4. Calculate portfolio statistics (mean, variance, etc.) using the portfolio return series
5. Verify that weights sum to 1.0

**Code Example:**

**Scenario:** Three stocks with returns across four economic states. State probabilities: Expansion (0.3): Stock 1=15%, Stock 2=20%, Stock 3=10%; Normal (0.5): Stock 1=8%, Stock 2=9%, Stock 3=7%; Recession (0.2): Stock 1=-5%, Stock 2=-8%, Stock 3=2%. What is the portfolio variance?

**Correct Code:**
```python
import numpy as np

# Economic states and probabilities
probabilities = [0.3, 0.5, 0.2]

# Returns for each stock in each state
stock_1_returns = [0.15, 0.08, -0.05]
stock_2_returns = [0.20, 0.09, -0.08]
stock_3_returns = [0.10, 0.07, 0.02]

# Equal-weighted portfolio (implicit assumption)
n_stocks = 3
weights = [1/n_stocks] * n_stocks

# Calculate portfolio return in each state
portfolio_returns = []
for i in range(len(probabilities)):
    port_return = (weights[0] * stock_1_returns[i] + 
                   weights[1] * stock_2_returns[i] + 
                   weights[2] * stock_3_returns[i])
    portfolio_returns.append(port_return)

# Expected portfolio return
expected_return = sum(p * r for p, r in zip(probabilities, portfolio_returns))

# Portfolio variance
variance = sum(p * (r - expected_return)**2 
               for p, r in zip(probabilities, portfolio_returns))

round(variance, 6)
```

**Common Bugs to Avoid:**
- Calculating variance of individual stocks instead of portfolio
- Forgetting to construct portfolio returns first before computing statistics
- Using non-equal weights when no weights are specified
- Computing covariance matrix when state-by-state returns are given (use direct calculation)

---

## Pattern: State-Contingent Portfolio Statistics

**Description:** When returns are given across discrete economic states with probabilities, portfolio variance must be calculated from the probability-weighted squared deviations of portfolio returns, not from individual asset variances.

**When to Use:** Context provides a table with states of economy, probabilities, and asset returns in each state; question asks for portfolio variance or standard deviation.

**Procedure:**
1. Formula: Var(R_p) = Σ[P_i × (R_p,i - E(R_p))²] where R_p,i is portfolio return in state i
2. Construct portfolio return for each state using asset weights
3. Calculate expected portfolio return: E(R_p) = Σ(P_i × R_p,i)
4. Calculate variance as probability-weighted sum of squared deviations
5. For standard deviation, take square root of variance

**Code Example:**

**Scenario:** Two assets with equal weights. Bull market (prob=0.4): Asset A=12%, Asset B=18%; Bear market (prob=0.6): Asset A=4%, Asset B=-2%. What is portfolio variance?

**Correct Code:**
```python
# State probabilities
prob_bull = 0.4
prob_bear = 0.6

# Asset returns in each state
asset_a_returns = [0.12, 0.04]
asset_b_returns = [0.18, -0.02]

# Equal weights
weight_a = 0.5
weight_b = 0.5

# Portfolio returns in each state
port_return_bull = weight_a * asset_a_returns[0] + weight_b * asset_b_returns[0]
port_return_bear = weight_a * asset_a_returns[1] + weight_b * asset_b_returns[1]

portfolio_returns = [port_return_bull, port_return_bear]
probabilities = [prob_bull, prob_bear]

# Expected portfolio return
expected_port_return = sum(p * r for p, r in zip(probabilities, portfolio_returns))

# Portfolio variance (NOT individual asset variances)
portfolio_variance = sum(p * (r - expected_port_return)**2 
                        for p, r in zip(probabilities, portfolio_returns))

round(portfolio_variance, 6)
```

**Common Bugs to Avoid:**
- Computing variance of individual assets then combining (wrong for state-contingent returns)
- Forgetting to calculate portfolio returns first
- Using covariance formula when direct state-by-state calculation is simpler
- Not squaring the deviations from expected return