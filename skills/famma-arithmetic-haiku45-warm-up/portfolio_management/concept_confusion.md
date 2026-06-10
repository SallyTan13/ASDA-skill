# Portfolio Management Concept Confusion: Detailed Skill Patterns

## Pattern: Efficient Frontier Identification

**Description:** Efficient frontier portfolios must be verified against the entire feasible set of weight combinations, not just tested for dominance within a limited subset of candidate portfolios. A portfolio is efficient only if no other feasible portfolio offers higher return for the same risk or lower risk for the same return.

**When to Use:** Questions asking to identify portfolios on the efficient frontier, optimal portfolio selection, or mean-variance optimization problems.

**Procedure:**
1. Formula: For portfolio with weights w, return = Σ(w_i × E[R_i]), variance = w'Σw where Σ is covariance matrix
2. Calculate expected returns, variances, and covariances for all assets
3. For each candidate portfolio, compute its return and standard deviation
4. To verify efficiency: either (a) solve for minimum variance portfolio at that return level across all possible weights, or (b) check if portfolio maximizes Sharpe ratio
5. Compare candidate portfolio metrics with the optimal portfolio at same return/risk level

**Code Example:**

**Scenario:** Two assets with returns [12%, 8%], std devs [20%, 15%], correlation 0.3. Test if 40% in asset 1 is efficient.

**Correct Code:**
```python
import numpy as np
from scipy.optimize import minimize

# Asset parameters
returns = np.array([0.12, 0.08])
std_devs = np.array([0.20, 0.15])
correlation = 0.3

# Covariance matrix
cov_matrix = np.array([
    [std_devs[0]**2, correlation * std_devs[0] * std_devs[1]],
    [correlation * std_devs[0] * std_devs[1], std_devs[1]**2]
])

# Candidate portfolio
candidate_weights = np.array([0.40, 0.60])
candidate_return = np.dot(candidate_weights, returns)
candidate_variance = np.dot(candidate_weights, np.dot(cov_matrix, candidate_weights))
candidate_std = np.sqrt(candidate_variance)

# Find minimum variance portfolio with same return
def portfolio_variance(weights, cov_matrix):
    return np.dot(weights, np.dot(cov_matrix, weights))

def portfolio_return(weights, returns):
    return np.dot(weights, returns)

# Constraint: return equals candidate return
constraints = [
    {'type': 'eq', 'fun': lambda w: portfolio_return(w, returns) - candidate_return},
    {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
]
bounds = [(0, 1), (0, 1)]

result = minimize(portfolio_variance, [0.5, 0.5], args=(cov_matrix,),
                  constraints=constraints, bounds=bounds)

optimal_std = np.sqrt(result.fun)

# Portfolio is efficient if candidate_std equals optimal_std (within tolerance)
is_efficient = abs(candidate_std - optimal_std) < 0.0001

is_efficient
```

**Common Bugs to Avoid:**
- Testing dominance only among given options instead of solving optimization problem
- Forgetting that efficient frontier requires global optimality, not local comparison
- Not accounting for covariance when calculating portfolio variance
- Using simple comparison logic instead of mathematical optimization

---

## Pattern: After-Tax Rebalancing Range with Transaction Costs

**Description:** Capital gains taxes create asymmetric transaction costs that widen (not narrow) optimal rebalancing corridors. The tax on embedded gains increases the cost of rebalancing, making it optimal to tolerate larger deviations before trading.

**When to Use:** Questions about rebalancing ranges, corridors, or bands when taxes on capital gains are present; portfolio maintenance with tax considerations.

**Procedure:**
1. Formula: After-tax range = Target ± (σ × √(2 × τ / (1 - τ))) where τ is capital gains tax rate, σ is volatility
2. Identify pre-tax rebalancing range and target allocation
3. Extract capital gains tax rate and asset volatility
4. Calculate the tax adjustment factor that widens the corridor
5. Apply adjustment to both upper and lower bounds from the target

**Code Example:**

**Scenario:** Pre-tax range 8%-12% (target 10%), asset volatility 15%, capital gains tax 25%.

**Correct Code:**
```python
import numpy as np

# Given parameters
pre_tax_lower = 0.08
pre_tax_upper = 0.12
target_allocation = (pre_tax_lower + pre_tax_upper) / 2
volatility = 0.15
capital_gains_tax = 0.25

# Calculate the width adjustment due to taxes
# Taxes increase transaction costs, widening the optimal corridor
tax_adjustment_factor = np.sqrt(2 * capital_gains_tax / (1 - capital_gains_tax))

# Calculate the pre-tax half-width
pre_tax_half_width = (pre_tax_upper - pre_tax_lower) / 2

# After-tax half-width is wider
after_tax_half_width = pre_tax_half_width * (1 + tax_adjustment_factor * volatility)

# Calculate after-tax bounds
after_tax_lower = target_allocation - after_tax_half_width
after_tax_upper = target_allocation + after_tax_half_width

# Express as percentages
(round(after_tax_lower * 100, 2), round(after_tax_upper * 100, 2))
```

**Common Bugs to Avoid:**
- Treating tax rate as a simple discount factor on allocation percentages
- Narrowing the range instead of widening it (taxes make rebalancing more costly)
- Ignoring volatility in the tax adjustment calculation
- Not recognizing that taxes create asymmetric costs for buying vs. selling

---

## Pattern: Futures Position Change with Contract Multiplier

**Description:** Futures contract value changes are calculated using the contract multiplier (typically $250 per point for S&P 500 futures), not by applying portfolio beta to portfolio value. The hedge position depends on the number of contracts needed based on portfolio exposure.

**When to Use:** Questions about hedging with futures, calculating futures position changes, or determining hedge ratios for index futures.

**Procedure:**
1. Formula: Number of contracts = (Portfolio Beta × Portfolio Value) / (Index Level × Multiplier)
2. Calculate number of futures contracts needed for the hedge
3. Determine the point change in the index
4. Calculate position change = Number of contracts × Point change × Multiplier
5. Verify sign convention (short hedge gains when index falls)

**Code Example:**

**Scenario:** Portfolio $2M, beta 0.8, S&P at 1500, 150-point drop expected. Standard multiplier $250.

**Correct Code:**
```python
# Portfolio and market parameters
portfolio_value = 2_000_000
portfolio_beta = 0.8
current_index = 1500
index_drop = 150
contract_multiplier = 250

# Calculate number of futures contracts needed
# For hedging, we need: (beta × portfolio value) / (index × multiplier)
num_contracts = (portfolio_beta * portfolio_value) / (current_index * contract_multiplier)

# Calculate the change in futures position value
# For a SHORT hedge (protection), when index drops, position GAINS
# Position change = contracts × point change × multiplier
futures_position_change = num_contracts * index_drop * contract_multiplier

# Return absolute value of the change
abs(futures_position_change)
```

**Common Bugs to Avoid:**
- Applying beta directly to portfolio value change instead of using futures mechanics
- Forgetting the contract multiplier in calculations
- Confusing portfolio loss with futures position gain/loss
- Not calculating the number of contracts first

---

## Pattern: Diversification and Idiosyncratic Risk Elimination

**Description:** In a well-diversified portfolio with many assets, idiosyncratic (firm-specific) risk diversifies away to zero, leaving only systematic (market) risk. Portfolio variance approaches β² × Var(Market) as the number of assets increases.

**When to Use:** Questions about portfolio variance with infinite or large number of assets, systematic vs. unsystematic risk, or diversification benefits.

**Procedure:**
1. Formula: Var(R_portfolio) = β² × Var(R_market) for well-diversified portfolio
2. Identify asset beta and market variance
3. Recognize that idiosyncratic variance (Var(ε)) disappears with diversification
4. Calculate only the systematic risk component
5. Do not add the asset-specific variance term

**Code Example:**

**Scenario:** Asset with beta 1.3, market variance 0.0144, idiosyncratic variance 0.0200. Calculate variance of portfolio with infinite number of this asset type.

**Correct Code:**
```python
# Asset and market parameters
asset_beta = 1.3
market_variance = 0.0144
idiosyncratic_variance = 0.0200  # This diversifies away

# For a well-diversified portfolio (infinite assets of this type)
# Only systematic risk remains
# Var(R_portfolio) = beta^2 × Var(R_market)
portfolio_variance = asset_beta**2 * market_variance

# Idiosyncratic variance is NOT included because it diversifies to zero
# Individual asset variance would be: beta^2 × market_var + idiosyncratic_var
# But portfolio variance eliminates the idiosyncratic component

portfolio_variance
```

**Common Bugs to Avoid:**
- Including idiosyncratic variance in diversified portfolio calculations
- Confusing individual asset variance with portfolio variance
- Not recognizing that "infinite number of assets" implies full diversification
- Adding Var(ε) when it should be eliminated through diversification

---

## Pattern: Systematic Risk as Variance Component

**Description:** Systematic risk in a factor model refers to the variance (or volatility) of returns attributable to factor exposures, calculated as Σ(β_i² × σ_i²), not the realized surprise return from factor deviations.

**When to Use:** Questions asking for systematic risk, factor-based risk decomposition, or variance attribution in multi-factor models.

**Procedure:**
1. Formula: Var(R_systematic) = Σ(β_i² × Var(Factor_i)) + cross-terms if factors correlated
2. Identify factor betas and factor variances/standard deviations
3. Calculate variance contribution from each factor: β² × σ²
4. Sum all factor variance contributions (add covariance terms if factors not independent)
5. Take square root if standard deviation is requested

**Code Example:**

**Scenario:** Two-factor model with β₁=1.5, β₂=0.8, factor std devs σ₁=0.10, σ₂=0.08, correlation=0.2.

**Correct Code:**
```python
import numpy as np

# Factor model parameters
beta_1 = 1.5
beta_2 = 0.8
factor_std_1 = 0.10
factor_std_2 = 0.08
factor_correlation = 0.2

# Calculate factor variances
factor_var_1 = factor_std_1**2
factor_var_2 = factor_std_2**2

# Calculate covariance between factors
factor_covariance = factor_correlation * factor_std_1 * factor_std_2

# Systematic variance from factor model
# Var(R_sys) = β₁²σ₁² + β₂²σ₂² + 2β₁β₂Cov(F₁,F₂)
systematic_variance = (beta_1**2 * factor_var_1 + 
                       beta_2**2 * factor_var_2 + 
                       2 * beta_1 * beta_2 * factor_covariance)

# Systematic risk (standard deviation)
systematic_risk = np.sqrt(systematic_variance)

systematic_risk
```

**Common Bugs to Avoid:**
- Calculating realized surprise returns (β × factor_surprise) instead of variance
- Treating unexpected return as systematic risk
- Forgetting to square betas when calculating variance contributions
- Ignoring covariance terms when factors are correlated

---

## Pattern: Effective Spread Calculation with Quoted Midpoint

**Description:** Effective spread measures execution cost relative to the quoted midpoint (average of best bid and best ask) at the time of each trade. For buy orders: 2 × (execution price - midpoint); for sell orders: 2 × (midpoint - execution price).

**When to Use:** Questions about trading costs, effective spreads, implementation shortfall components, or transaction cost analysis.

**Procedure:**
1. Formula: Effective Spread (buy) = 2 × (Execution Price - Quoted Midpoint)
2. For each trade, identify execution price, best bid, and best ask at trade time
3. Calculate quoted midpoint = (Best Bid + Best Ask) / 2
4. Calculate effective spread for each trade using formula
5. Compute share-volume-weighted average: Σ(shares_i × spread_i) / Σ(shares_i)

**Code Example:**

**Scenario:** Buy 3,000 shares: Trade 1: 2,000 shares at $50.10 (bid $50.00, ask $50.12); Trade 2: 1,000 shares at $50.15 (bid $50.05, ask $50.18).

**Correct Code:**
```python
# Trade execution details
trades = [
    {'shares': 2000, 'exec_price': 50.10, 'bid': 50.00, 'ask': 50.12},
    {'shares': 1000, 'exec_price': 50.15, 'bid': 50.05, 'ask': 50.18}
]

# Calculate effective spread for each trade
effective_spreads = []
for trade in trades:
    # Quoted midpoint at time of trade
    midpoint = (trade['bid'] + trade['ask']) / 2
    
    # Effective spread for buy order: 2 × (execution - midpoint)
    spread = 2 * (trade['exec_price'] - midpoint)
    
    effective_spreads.append({
        'shares': trade['shares'],
        'spread': spread
    })

# Calculate share-volume-weighted effective spread
total_shares = sum(t['shares'] for t in effective_spreads)
weighted_spread = sum(t['shares'] * t['spread'] for t in effective_spreads) / total_shares

round(weighted_spread, 2)
```

**Common Bugs to Avoid:**
- Using arbitrary bid-ask pairs instead of best bid/ask at trade time
- Forgetting the factor of 2 in effective spread formula
- Not weighting by share volume when averaging multiple trades
- Calculating spread as simple (execution - midpoint) without doubling

---

## Pattern: Capital Allocation Line and Complete Portfolio

**Description:** A client's complete portfolio includes both the risky portfolio and risk-free asset (T-bills). Determining the allocation requires either client risk preferences (risk aversion, target return, or target volatility) or solving for the optimal weight using utility maximization.

**When to Use:** Questions about overall portfolio composition, capital allocation decisions, or determining weights in risky vs. risk-free assets.

**Procedure:**
1. Formula: y = (E[R_p] - R_f) / (A × σ_p²) where y is weight in risky portfolio, A is risk aversion
2. Identify risky portfolio return, std dev, and risk-free rate
3. Determine client's constraint (target return, target std dev, or risk aversion parameter)
4. Solve for y (weight in risky portfolio): if target return given, y = (Target - R_f) / (E[R_p] - R_f)
5. Calculate individual asset weights = y × (weight in risky portfolio)

**Code Example:**

**Scenario:** Risky portfolio: 30% Stock A, 70% Stock B, E[R]=14%, σ=20%. T-bills: 4%. Client wants 11% return.

**Correct Code:**
```python
# Portfolio parameters
risky_return = 0.14
risky_std = 0.20
rf_rate = 0.04
stock_a_weight_in_risky = 0.30
stock_b_weight_in_risky = 0.70

# Client target return
target_return = 0.11

# Calculate weight in risky portfolio (y)
# Target return = y × E[R_risky] + (1-y) × R_f
# Solving for y: y = (Target - R_f) / (E[R_risky] - R_f)
weight_risky = (target_return - rf_rate) / (risky_return - rf_rate)
weight_tbills = 1 - weight_risky

# Calculate weights in individual assets
weight_stock_a = weight_risky * stock_a_weight_in_risky
weight_stock_b = weight_risky * stock_b_weight_in_risky

# Complete portfolio composition
complete_portfolio = {
    'T-bills': round(weight_tbills * 100, 1),
    'Stock A': round(weight_stock_a * 100, 1),
    'Stock B': round(weight_stock_b * 100, 1)
}

complete_portfolio
```

**Common Bugs to Avoid:**
- Assuming client invests 100% in risky portfolio without checking constraints
- Not recognizing this as a capital allocation problem requiring y calculation
- Forgetting to scale risky asset weights by y
- Missing that "overall portfolio" includes both risky and risk-free components

---

## Pattern: Confidence Index as Yield Ratio

**Description:** The Confidence Index is defined as the ratio of high-grade bond yields to lower-grade bond yields. It rises when the ratio increases (spread narrows), indicating increased confidence; it falls when the ratio decreases (spread widens).

**When to Use:** Questions about confidence index, credit spread analysis, or bond market sentiment indicators.

**Procedure:**
1. Formula: Confidence Index = (High-grade yield) / (Lower-grade yield)
2. Calculate confidence index for current period and prior period
3. Compare the two ratios to determine direction
4. Rising index (higher ratio) = narrowing spread = increased confidence
5. Falling index (lower ratio) = widening spread = decreased confidence

**Code Example:**

**Scenario:** Last year: AAA yield 5%, BBB yield 7%. This year: AAA yield 4.5%, BBB yield 7.5%.

**Correct Code:**
```python
# Yield data
high_grade_yield_last_year = 0.05
low_grade_yield_last_year = 0.07
high_grade_yield_this_year = 0.045
low_grade_yield_this_year = 0.075

# Calculate confidence index for each period
confidence_index_last_year = high_grade_yield_last_year / low_grade_yield_last_year
confidence_index_this_year = high_grade_yield_this_year / low_grade_yield_this_year

# Determine direction
index_change = confidence_index_this_year - confidence_index_last_year
is_rising = index_change > 0

# Calculate credit spread for context
spread_last_year = low_grade_yield_last_year - high_grade_yield_last_year
spread_this_year = low_grade_yield_this_year - high_grade_yield_this_year

result = {
    'confidence_index_last_year': round(confidence_index_last_year, 4),
    'confidence_index_this_year': round(confidence_index_this_year, 4),
    'direction': 'RISING' if is_rising else 'FALLING',
    'spread_change': round((spread_this_year - spread_last_year) * 100, 2)
}

result
```

**Common Bugs to Avoid:**
- Using spread change instead of yield ratio
- Inverting the ratio (low-grade / high-grade)
- Qualitative interpretation without calculating the actual index
- Confusing spread widening/narrowing with index direction

---

## Pattern: Deduction Method for Foreign Tax

**Description:** Under the deduction method, foreign taxes paid are deducted from taxable income (reducing the tax base), not credited against tax liability. Effective rate = Domestic rate + Foreign rate - (Domestic rate × Foreign rate).

**When to Use:** Questions about international taxation, foreign tax treatment, deduction vs. credit methods, or cross-border investment taxation.

**Procedure:**
1. Formula: Effective Tax Rate = r_d + r_f - (r_d × r_f) where r_d is domestic rate, r_f is foreign rate
2. Identify domestic tax rate and foreign tax rate
3. Calculate combined effect: both taxes apply, but foreign tax reduces domestic tax base
4. Apply formula to get effective rate
5. Verify: effective rate should be higher than either individual rate but less than their sum

**Code Example:**

**Scenario:** Domestic tax 12%, foreign tax 18%. Calculate effective tax rate under deduction method.

**Correct Code:**
```python
# Tax rates
domestic_tax_rate = 0.12
foreign_tax_rate = 0.18

# Under deduction method:
# Foreign tax is deducted from income before calculating domestic tax
# Tax = Foreign_tax + Domestic_tax_on_remaining_income
# Tax = Income × r_f + (Income - Income × r_f) × r_d
# Tax = Income × [r_f + r_d - (r_f × r_d)]

effective_tax_rate = (domestic_tax_rate + foreign_tax_rate - 
                      (domestic_tax_rate * foreign_tax_rate))

# Convert to percentage
effective_rate_percentage = round(effective_tax_rate * 100, 1)

effective_rate_percentage
```

**Common Bugs to Avoid:**
- Treating deduction method as credit method (subtracting foreign tax from liability)
- Taking the maximum of the two rates instead of calculating combined effect
- Simply adding the two rates without adjustment
- Not recognizing that foreign tax reduces the base for domestic tax

---

## Pattern: Delta-Hedged Portfolio Insurance

**Description:** Portfolio insurance using derivatives requires delta-hedging: holding delta proportion in risky assets and (1-delta) in risk-free, where delta comes from the protective put option. Initial position = put delta × portfolio exposure.

**When to Use:** Questions about portfolio insurance with options or futures, dynamic hedging strategies, or replicating protective puts.

**Procedure:**
1. Formula: Put Delta = e^(-qT) × [N(d₁) - 1], where d₁ from Black-Scholes
2. Calculate d₁ using strike price (protection level), current price, risk-free rate, dividend yield, volatility, time
3. Calculate N(d₁) using cumulative normal distribution
4. Compute put delta (will be negative, between -1 and 0)
5. For futures: Number of contracts = (Portfolio value / Futures price) × |Put Delta|

**Code Example:**

**Scenario:** Portfolio $500M, index 1500, protect against 8% loss over 1 year. r=5%, q=2%, σ=25%. Futures multiplier $250.

**Correct Code:**
```python
import numpy as np
from scipy.stats import norm

# Portfolio and market parameters
portfolio_value = 500_000_000
index_level = 1500
protection_level = 0.08
time_to_maturity = 1.0
risk_free_rate = 0.05
dividend_yield = 0.02
volatility = 0.25
futures_multiplier = 250

# Strike price: protect against 8% loss
strike_index = index_level * (1 - protection_level)

# Calculate d1 for Black-Scholes
d1 = (np.log(index_level / strike_index) + 
      (risk_free_rate - dividend_yield + volatility**2 / 2) * time_to_maturity) / \
     (volatility * np.sqrt(time_to_maturity))

# Calculate N(d1)
N_d1 = norm.cdf(d1)

# Put delta (negative value)
put_delta = np.exp(-dividend_yield * time_to_maturity) * (N_d1 - 1)

# Number of futures contracts for insurance
# Absolute value of put delta gives hedge ratio
futures_price = index_level * futures_multiplier
num_contracts = (portfolio_value / futures_price) * abs(put_delta)

round(num_contracts, 0)
```

**Common Bugs to Avoid:**
- Using full portfolio exposure instead of delta-adjusted position
- Applying naive short hedge without calculating put delta
- Confusing static hedging with dynamic delta-hedging
- Not recognizing that insurance replication requires option Greeks

---

## Pattern: Arrival Cost Benchmark

**Description:** Arrival cost (also called decision price benchmark) measures execution performance relative to the market price at the time the trading decision was made, capturing all market movement and execution costs from decision to completion.

**When to Use:** Questions about trade execution analysis, implementation shortfall components, or performance measurement against decision price.

**Procedure:**
1. Formula: Arrival Cost (bp) = [(Avg Execution Price - Decision Price) / Decision Price] × 10,000
2. Identify the decision price (market price when order was received/decided)
3. Calculate average execution price (volume-weighted across all fills)
4. Include commissions in execution price if specified
5. Express difference as basis points relative to decision price

**Code Example:**

**Scenario:** Decision price $75.00, bought 5,000 shares: 3,000 at $75.30, 2,000 at $75.50. Commission $0.03/share.

**Correct Code:**
```python
# Trade parameters
decision_price = 75.00
commission_per_share = 0.03

# Execution details
trades = [
    {'shares': 3000, 'price': 75.30},
    {'shares': 2000, 'price': 75.50}
]

# Calculate volume-weighted average execution price
total_shares = sum(t['shares'] for t in trades)
total_cost = sum(t['shares'] * t['price'] for t in trades)
avg_execution_price = total_cost / total_shares

# Add commission to get all-in execution price
avg_execution_price_with_commission = avg_execution_price + commission_per_share

# Calculate arrival cost in basis points
# Arrival cost = (Execution price - Decision price) / Decision price × 10,000
arrival_cost_bp = ((avg_execution_price_with_commission - decision_price) / 
                   decision_price) * 10_000

round(arrival_cost_bp, 1)
```

**Common Bugs to Avoid:**
- Using limit price or closing price instead of decision price as benchmark
- Forgetting to include commissions in execution cost
- Not volume-weighting execution prices across multiple fills
- Calculating relative to wrong reference point (arrival = decision time)

## Pattern: Bond-Yield-Plus-Risk-Premium Method for Equity Returns

**Description:** The bond-yield-plus-risk-premium method estimates equity expected return by adding an equity risk premium (typically 3-5%) to the yield on the company's or industry's own debt, NOT by adding the market equity risk premium to a risk-free rate or generic corporate bond yield. The equity risk premium here represents the incremental return equity holders require over the company's debt holders.

**When to Use:** Questions asking to calculate expected equity returns using the bond-yield-plus-risk-premium method, cost of equity estimation, or when given both bond yields and risk premiums for a specific company or industry.

**Procedure:**
1. Formula: Expected Equity Return = Company's Own Bond Yield + Equity Risk Premium over Debt (typically 3-5%)
2. Identify the yield on the company's or industry's own debt (not the risk-free rate)
3. Identify the appropriate equity risk premium over debt (historical average is 3-4%, often given in context)
4. Add the two components together
5. Return the result as a percentage

**Code Example:**

**Scenario:** A retail industry has bonds yielding 5.2%. Historical data shows equity returns exceed bond yields by 3.8% on average. Calculate the expected equity return for the industry.

**Correct Code:**
```python
# Bond-Yield-Plus-Risk-Premium Method
# Step 1: Identify the industry's own bond yield
industry_bond_yield = 5.2  # percent

# Step 2: Identify the equity risk premium OVER the bond yield
# This is NOT the market equity risk premium (equity over risk-free)
# This is the incremental premium of equity over the company's own debt
equity_premium_over_debt = 3.8  # percent

# Step 3: Calculate expected equity return
expected_equity_return = industry_bond_yield + equity_premium_over_debt

expected_equity_return  # Result: 9.0%
```

**Common Bugs to Avoid:**
- Using the market equity risk premium (e.g., 8.4% equity return over risk-free rate) instead of the equity premium over the company's own debt (typically 3-5%)
- Using risk-free rate or generic corporate bond yield instead of the specific company's/industry's own debt yield
- Adding multiple premiums incorrectly (e.g., adding both inflation premium and illiquidity premium when they're already embedded in the bond yield)
- Confusing the base rate: the starting point is the company's bond yield, not the risk-free rate
- Using print() instead of returning an expression on the last line