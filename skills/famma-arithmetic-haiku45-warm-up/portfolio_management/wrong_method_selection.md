# SKILL PATTERNS FOR PORTFOLIO MANAGEMENT - WRONG METHOD SELECTION

## Pattern: Futures Contract Value Change Calculation

**Description:** Futures position changes must be calculated using the contract multiplier (e.g., $250 per index point for S&P 500 futures), not by applying portfolio beta or percentage changes to portfolio value. The mechanical contract value change is independent of the portfolio's characteristics.

**When to Use:** Questions asking for futures position value changes given index point movements, hedging calculations with futures contracts, or questions mentioning specific futures contracts (S&P 500, bond futures, etc.).

**Procedure:**
1. Formula: `Futures Position Change = Index Point Change × Contract Multiplier × Number of Contracts`
2. Identify the index point change (e.g., 75-point drop in S&P 500)
3. Apply the standard contract multiplier for that futures type (S&P 500 = $250 per point)
4. If number of contracts is not given, assume 1 contract unless hedging calculation is required
5. Return absolute value if question asks "by how much" without directional context

**Code Example:**

**Scenario:** The Nasdaq-100 index drops 120 points. Each Nasdaq-100 futures contract has a multiplier of $20 per index point. Calculate the change in value for 3 futures contracts.

**Correct Code:**
```python
# Given information
index_point_change = 120  # points
contract_multiplier = 20  # dollars per index point
number_of_contracts = 3

# Calculate futures position change
# This is a mechanical calculation based on contract specifications
futures_position_change = index_point_change * contract_multiplier * number_of_contracts

# Result in absolute terms
abs(futures_position_change)
```

**Common Bugs to Avoid:**
- Applying portfolio beta to calculate futures value change (beta is for portfolio exposure, not contract mechanics)
- Using percentage change methodology instead of point-based calculation
- Confusing portfolio hedge ratio calculation with direct futures value change
- Forgetting that contract multiplier is a fixed specification, not derived from portfolio characteristics

---

## Pattern: Information Ratio with CAPM Alpha

**Description:** Information Ratio measures active return (alpha from CAPM) per unit of active risk (residual standard deviation). It requires calculating expected return using CAPM first, then finding alpha as the difference between actual and expected return, not simply excess return over risk-free rate or market return.

**When to Use:** Questions asking for Information Ratio when beta, market return, risk-free rate, and residual standard deviation are provided; performance evaluation of active managers.

**Procedure:**
1. Formula: `Information Ratio = Alpha / Residual Standard Deviation`
2. Calculate expected return using CAPM: `Expected Return = Risk_Free_Rate + Beta × (Market_Return - Risk_Free_Rate)`
3. Calculate alpha: `Alpha = Actual_Return - Expected_Return`
4. Divide alpha by residual standard deviation (tracking error)
5. Return the ratio (can be positive or negative)

**Code Example:**

**Scenario:** A fund has actual return of 18%, beta of 1.5, residual standard deviation of 3%. Market return is 12%, risk-free rate is 4%. Calculate Information Ratio.

**Correct Code:**
```python
# Given information
actual_return = 0.18  # 18%
beta = 1.5
residual_std_dev = 0.03  # 3%
market_return = 0.12  # 12%
risk_free_rate = 0.04  # 4%

# Step 1: Calculate expected return using CAPM
market_risk_premium = market_return - risk_free_rate
expected_return = risk_free_rate + beta * market_risk_premium

# Step 2: Calculate alpha (active return)
alpha = actual_return - expected_return

# Step 3: Calculate Information Ratio
information_ratio = alpha / residual_std_dev

information_ratio
```

**Common Bugs to Avoid:**
- Using `(actual_return - market_return) / residual_std_dev` (ignores beta adjustment)
- Using `(actual_return - risk_free_rate) / residual_std_dev` (this is Sharpe-like, not Information Ratio)
- Confusing residual standard deviation with total standard deviation
- Using total standard deviation instead of residual standard deviation in denominator
- Forgetting that alpha must account for systematic risk via CAPM expected return

---

## Pattern: Bivariate GARCH Correlation Update

**Description:** Updating correlations in GARCH models requires proper bivariate framework. When updating correlation between two assets, you cannot simply apply univariate GARCH parameters to covariance; instead, use correlation persistence formula or specify separate covariance dynamics with appropriate parameters.

**When to Use:** Questions asking to update correlation between two assets using GARCH, multivariate volatility modeling, or when given correlation alongside individual asset GARCH parameters.

**Procedure:**
1. Formula for correlation persistence: `ρ_new = λ × ρ_old + (1 - λ) × (standardized_return_1 × standardized_return_2)`
2. Update each asset's variance using GARCH(1,1): `σ²_new = ω + α × u²_old + β × σ²_old`
3. Calculate standardized returns: `z_i = u_i / σ_i` for each asset
4. Apply correlation update with persistence parameter λ = α + β (common specification)
5. Ensure correlation stays in valid range [-1, 1]

**Code Example:**

**Scenario:** Stock A has volatility 2% yesterday, return today of -1%. Stock B has volatility 1.5% yesterday, return today of 0.5%. Correlation yesterday was 0.75. GARCH parameters: ω=0.000001, α=0.05, β=0.93. Update correlation.

**Correct Code:**
```python
import math

# Asset A information
vol_A_old = 0.02  # 2%
return_A = -0.01  # -1%

# Asset B information
vol_B_old = 0.015  # 1.5%
return_B = 0.005  # 0.5%

# GARCH parameters
omega = 0.000001
alpha = 0.05
beta = 0.93

# Old correlation
correlation_old = 0.75

# Step 1: Update variances using GARCH(1,1)
variance_A_old = vol_A_old ** 2
variance_A_new = omega + alpha * (return_A ** 2) + beta * variance_A_old
vol_A_new = math.sqrt(variance_A_new)

variance_B_old = vol_B_old ** 2
variance_B_new = omega + alpha * (return_B ** 2) + beta * variance_B_old
vol_B_new = math.sqrt(variance_B_new)

# Step 2: Calculate standardized returns (using old volatilities)
z_A = return_A / vol_A_old
z_B = return_B / vol_B_old

# Step 3: Update correlation using persistence formula
# Persistence parameter lambda = alpha + beta
lambda_corr = alpha + beta
correlation_new = lambda_corr * correlation_old + (1 - lambda_corr) * (z_A * z_B)

correlation_new
```

**Common Bugs to Avoid:**
- Applying univariate GARCH parameters directly to covariance without proper bivariate specification
- Calculating `ω_cov = (1 - α - β) × long_run_covariance` and using same α, β for covariance (incorrect assumption)
- Using current volatilities instead of lagged volatilities for standardizing returns
- Forgetting that correlation dynamics may have different persistence than variance dynamics
- Not using standardized returns (z-scores) in the correlation update formula
- Assuming covariance parameters equal variance parameters without justification

---

## Pattern: Contract-Based vs Portfolio-Based Calculations

**Description:** Distinguish between calculations based on contract specifications (mechanical, fixed multipliers) versus portfolio characteristics (beta, value, exposure). Contract value changes use fixed multipliers; hedge ratios use portfolio characteristics.

**When to Use:** Any futures or options question where you must decide whether to use contract specifications or portfolio risk metrics; hedging problems that ask for both position changes and hedge ratios.

**Procedure:**
1. Identify what the question asks: "value change of position" (contract-based) vs "number of contracts to hedge" (portfolio-based)
2. For contract value changes: Use `Point Change × Multiplier × Contracts`
3. For hedge ratios: Use `(Portfolio Value × Beta) / (Index Level × Multiplier)`
4. Never mix the two approaches in a single calculation
5. Verify units: contract calculations yield dollars, hedge ratios yield number of contracts

**Code Example:**

**Scenario:** Portfolio worth $2M with beta 1.2. S&P 500 at 4000. To hedge, you need contracts. If index drops 50 points, what's the hedge position change? (S&P multiplier = $250)

**Correct Code:**
```python
# Portfolio characteristics (for hedge ratio calculation)
portfolio_value = 2_000_000
portfolio_beta = 1.2
index_level = 4000
contract_multiplier = 250

# Calculate number of contracts needed to hedge
# This uses portfolio characteristics
contracts_needed = (portfolio_value * portfolio_beta) / (index_level * contract_multiplier)

# Index movement
index_point_drop = 50

# Calculate hedge position value change
# This uses contract specifications only
hedge_position_change = index_point_drop * contract_multiplier * contracts_needed

hedge_position_change
```

**Common Bugs to Avoid:**
- Using beta in direct futures value change calculations (beta is for determining hedge ratio, not contract value)
- Applying percentage changes to calculate futures position changes
- Confusing "how much does position change" (contract-based) with "how many contracts needed" (portfolio-based)
- Using portfolio value in contract value change formulas
- Forgetting that contract multiplier is independent of portfolio characteristics