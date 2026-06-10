# SKILL PATTERNS FOR MISSED CONSTRAINTS IN FINANCIAL CALCULATIONS

## Pattern: Merger Share Count Adjustment

**Description:** Post-merger EPS calculations require explicit merger terms (exchange ratio, acquisition price, or post-merger share count). Cannot assume simple addition of pre-merger shares; acquiring firms typically issue new shares based on acquisition terms.

**When to Use:** Questions about post-merger metrics (EPS, book value per share) where share count changes due to acquisition structure.

**Procedure:**
1. Formula: `Post-Merger EPS = Combined Earnings / Post-Merger Shares Outstanding`
2. Check if exchange ratio or acquisition terms are explicitly provided
3. If stock-for-stock merger: Calculate new shares issued = (Target shares × Exchange ratio)
4. If cash acquisition: Post-merger shares = Acquirer shares only
5. If terms missing: Flag as insufficient information or request clarification
6. Verify that share count reflects economic reality of the transaction

**Code Example:**

**Scenario:** Firm X acquires Firm Y in a stock-for-stock merger. Firm X has earnings of $5,000 and 1,000 shares outstanding. Firm Y has earnings of $2,000 and 400 shares. The exchange ratio is 0.8 shares of X for each share of Y.

**Correct Code:**
```python
# Given data
earnings_x = 5000
shares_x = 1000
earnings_y = 2000
shares_y = 400
exchange_ratio = 0.8  # shares of X per share of Y

# Post-merger calculation
combined_earnings = earnings_x + earnings_y
new_shares_issued = shares_y * exchange_ratio
post_merger_shares = shares_x + new_shares_issued

# Post-merger EPS
post_merger_eps = combined_earnings / post_merger_shares

post_merger_eps  # Result: 5.833...
```

**Common Bugs to Avoid:**
- Assuming post-merger shares = pre-merger shares of both firms added together
- Ignoring exchange ratio when provided in problem context
- Not checking whether acquisition is stock-based, cash-based, or mixed
- Using print() instead of returning expression value

---

## Pattern: Probability-Weighted Expected Value

**Description:** Expected return/value requires probability-weighted averaging of state-contingent outcomes, not simple arithmetic mean. Must identify or assume probability distribution when computing expectations.

**When to Use:** Questions asking for "expected return," "expected value," or similar expectation calculations across multiple states/scenarios.

**Procedure:**
1. Formula: `E[R] = Σ(probability_i × return_i)` for all states i
2. Identify all possible states/outcomes and their returns
3. Check if probabilities are explicitly provided
4. If probabilities missing: Apply equal probability assumption (1/n for n states) OR flag as missing information
5. Multiply each outcome by its probability and sum
6. Verify probabilities sum to 1.0

**Code Example:**

**Scenario:** Calculate expected return for Stock Z with returns in three economic states: Recession (return = -5%), Normal (return = 12%), Boom (return = 25%). Probabilities are 0.25, 0.50, and 0.25 respectively.

**Correct Code:**
```python
# State-contingent returns and probabilities
returns = [-0.05, 0.12, 0.25]
probabilities = [0.25, 0.50, 0.25]

# Verify probabilities sum to 1
assert abs(sum(probabilities) - 1.0) < 1e-6, "Probabilities must sum to 1"

# Expected return calculation
expected_return = sum(p * r for p, r in zip(probabilities, returns))

expected_return  # Result: 0.10 or 10%
```

**Alternative (Equal Probabilities):**
```python
# When probabilities not given, assume equal weighting
returns = [0.08, 0.15, 0.22]
n_states = len(returns)
equal_prob = 1.0 / n_states

expected_return = sum(equal_prob * r for r in returns)
# Equivalent to: expected_return = sum(returns) / len(returns)

expected_return  # Result: 0.15
```

**Common Bugs to Avoid:**
- Computing simple arithmetic mean when probabilities are unequal
- Forgetting to verify probabilities sum to 1.0
- Mixing decimal and percentage formats (0.12 vs 12%)
- Not recognizing "expected" as a keyword requiring probability weighting

---

## Pattern: Beta-Adjusted Hedge Ratio

**Description:** When hedging a portfolio with beta ≠ 1.0 using index derivatives, the number of contracts must be scaled by portfolio beta to account for differential sensitivity to market movements.

**When to Use:** Portfolio hedging problems involving options, futures, or derivatives where the portfolio beta differs from 1.0 and hedge instrument is based on a market index.

**Procedure:**
1. Formula: `Adjusted Hedge Ratio = Portfolio Beta × (Portfolio Value / Index Value per Contract)`
2. Identify portfolio beta relative to the hedge instrument's underlying
3. Calculate base hedge ratio assuming beta = 1.0
4. Multiply base hedge ratio by portfolio beta
5. For protective puts: Number of contracts = (Portfolio Value × Beta) / (Index Level × Contract Multiplier)
6. Verify hedge direction matches risk exposure

**Code Example:**

**Scenario:** A portfolio worth $10,000,000 has beta = 1.8 relative to an index. The index is at 2,500 and each index option contract covers 100 index units. Calculate the number of put contracts needed for full hedge.

**Correct Code:**
```python
import math

# Portfolio and market parameters
portfolio_value = 10_000_000
portfolio_beta = 1.8
index_level = 2500
contract_multiplier = 100

# Value per contract
value_per_contract = index_level * contract_multiplier

# Beta-adjusted hedge calculation
# Base contracts (if beta = 1.0)
base_contracts = portfolio_value / value_per_contract

# Adjust for beta
adjusted_contracts = base_contracts * portfolio_beta

# Round to nearest whole contract
num_contracts = round(adjusted_contracts)

num_contracts  # Result: 72 contracts
```

**With Option Pricing Integration:**
```python
from scipy.stats import norm
import math

# Additional parameters for option pricing
S = 2500  # Index level
K = 2375  # Strike (5% below current)
r = 0.06
q = 0.03  # dividend yield
sigma = 0.30
T = 0.5

# Black-Scholes-Merton for dividend-paying asset
d1 = (math.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*math.sqrt(T))
d2 = d1 - sigma*math.sqrt(T)

put_price = K*math.exp(-r*T)*norm.cdf(-d2) - S*math.exp(-q*T)*norm.cdf(-d1)

# Beta-adjusted contracts
portfolio_value = 10_000_000
portfolio_beta = 1.8
num_contracts = round((portfolio_value * portfolio_beta) / (S * 100))

# Total insurance cost
total_cost = num_contracts * put_price * 100

total_cost  # Insurance cost in dollars
```

**Common Bugs to Avoid:**
- Ignoring portfolio beta when calculating hedge ratios
- Treating beta as a descriptive statistic rather than a scaling factor
- Forgetting contract multiplier (e.g., 100 for index options)
- Not rounding to whole contracts when required
- Confusing beta adjustment direction (multiply, not divide)

---

## Pattern: Constraint Validation and Missing Information Detection

**Description:** Before performing calculations, explicitly validate that all required constraints and parameters are present. Flag missing critical information rather than making unjustified assumptions.

**When to Use:** Any financial calculation where the problem structure requires specific inputs that may not be explicitly stated.

**Procedure:**
1. List all parameters required for the calculation formula
2. Check problem statement and context for each required parameter
3. Identify parameters that are implicit (e.g., equal probabilities) vs. truly missing
4. For missing critical parameters: Return error message or flag uncertainty
5. For reasonable assumptions: Document assumption explicitly in code comments
6. Proceed with calculation only when all constraints are satisfied or reasonably assumed

**Code Example:**

**Scenario:** Calculate portfolio insurance cost, checking for all required Black-Scholes parameters.

**Correct Code:**
```python
def validate_bsm_parameters(params):
    """Validate all required BSM parameters are present"""
    required = ['S', 'K', 'r', 'T', 'sigma', 'q']
    missing = [p for p in required if p not in params or params[p] is None]
    
    if missing:
        raise ValueError(f"Missing required parameters: {missing}")
    
    # Validate ranges
    if params['T'] <= 0:
        raise ValueError("Time to maturity must be positive")
    if params['sigma'] <= 0:
        raise ValueError("Volatility must be positive")
    if params['S'] <= 0:
        raise ValueError("Spot price must be positive")
    
    return True

# Example usage
params = {
    'S': 1200,
    'K': 1140,  # 5% below spot
    'r': 0.06,
    'T': 0.5,
    'sigma': 0.30,
    'q': 0.03
}

validate_bsm_parameters(params)

# Proceed with calculation only after validation
from scipy.stats import norm
import math

S, K, r, T, sigma, q = params['S'], params['K'], params['r'], params['T'], params['sigma'], params['q']

d1 = (math.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*math.sqrt(T))
d2 = d1 - sigma*math.sqrt(T)

put_price = K*math.exp(-r*T)*norm.cdf(-d2) - S*math.exp(-q*T)*norm.cdf(-d1)

put_price  # Result only if all validations pass
```

**For Expected Return with Missing Probabilities:**
```python
def calculate_expected_return(returns, probabilities=None):
    """Calculate expected return with explicit probability handling"""
    
    if probabilities is None:
        # Document assumption
        print("Warning: Probabilities not provided. Assuming equal weighting.")
        probabilities = [1.0/len(returns)] * len(returns)
    
    # Validate
    if len(returns) != len(probabilities):
        raise ValueError("Returns and probabilities must have same length")
    
    if abs(sum(probabilities) - 1.0) > 1e-6:
        raise ValueError(f"Probabilities sum to {sum(probabilities)}, must sum to 1.0")
    
    expected_return = sum(p * r for p, r in zip(probabilities, returns))
    return expected_return

# Usage
returns = [0.10, 0.15, 0.20]
result = calculate_expected_return(returns)  # Assumes equal probabilities

result
```

**Common Bugs to Avoid:**
- Making silent assumptions about missing parameters
- Not validating probability distributions sum to 1.0
- Proceeding with calculations when critical constraints are violated
- Failing to document assumptions in code comments
- Not checking for reasonable parameter ranges (negative prices, etc.)