# SKILL PATTERNS FOR PORTFOLIO MANAGEMENT: UNIT/CURRENCY/PERCENT CONVERSION ERRORS (PoT)

## Pattern: Portfolio Expected Return Calculation

**Description:** Portfolio expected return must be computed as the weighted average of individual asset expected returns, where each asset's expected return is first calculated using probability-weighted state returns, then combined using portfolio weights.

**When to Use:** Questions asking for portfolio expected return given individual asset returns across states and portfolio weights, or when combining multiple securities into a portfolio.

**Procedure:**
1. Formula: E(R_p) = Σ(w_i × E(R_i)) where E(R_i) = Σ(P_j × R_ij)
2. First compute expected return for each asset: multiply each state return by its probability and sum
3. Then compute portfolio expected return: multiply each asset's expected return by its portfolio weight and sum
4. Convert to percentage if answer options are in percentage format (multiply by 100)

**Code Example:**

**Scenario:** Portfolio with 30% in Asset X (returns: 8% with prob 0.4, 12% with prob 0.6) and 70% in Asset Y (returns: 5% with prob 0.4, 15% with prob 0.6)

**Correct Code:**
```python
import numpy as np

# State probabilities and returns (as decimals)
probs = np.array([0.4, 0.6])
returns_x = np.array([0.08, 0.12])
returns_y = np.array([0.05, 0.15])

# Step 1: Expected return for each asset
exp_return_x = np.sum(probs * returns_x)
exp_return_y = np.sum(probs * returns_y)

# Step 2: Portfolio weights
weights = np.array([0.30, 0.70])

# Step 3: Portfolio expected return
portfolio_exp_return = weights[0] * exp_return_x + weights[1] * exp_return_y

# Convert to percentage for output
portfolio_exp_return_pct = portfolio_exp_return * 100

portfolio_exp_return_pct  # 10.9%
```

**Common Bugs to Avoid:**
- Computing state-by-state portfolio returns first, then averaging (incorrect order of operations)
- Forgetting to convert percentage returns to decimals before calculation
- Using print() instead of expression on last line in PoT
- Mismatching units between calculation (decimal) and answer options (percentage)

---

## Pattern: Portfolio Variance and Standard Deviation from State Returns

**Description:** Portfolio variance requires computing portfolio returns for each state, calculating the expected portfolio return, then computing probability-weighted squared deviations. Standard deviation is the square root of variance.

**When to Use:** Questions asking for portfolio variance or standard deviation given individual asset returns across economic states and portfolio weights.

**Procedure:**
1. Formula: Var(R_p) = Σ(P_j × (R_pj - E(R_p))²) where R_pj = Σ(w_i × R_ij)
2. Compute portfolio return for each state: weighted sum of individual asset returns
3. Compute expected portfolio return: probability-weighted average of state portfolio returns
4. Compute variance: probability-weighted sum of squared deviations from expected return
5. For standard deviation: take square root of variance
6. Convert to percentage units if needed (multiply by 100 for std dev, or express variance in percentage-squared)

**Code Example:**

**Scenario:** Portfolio with 50% in Stock M and 50% in Stock N across three states

**Correct Code:**
```python
import numpy as np

# State data
probs = np.array([0.25, 0.50, 0.25])
returns_m = np.array([0.10, 0.15, 0.20])  # as decimals
returns_n = np.array([0.08, 0.12, 0.18])
weights = np.array([0.50, 0.50])

# Step 1: Portfolio return in each state
portfolio_returns = weights[0] * returns_m + weights[1] * returns_n

# Step 2: Expected portfolio return
exp_portfolio_return = np.sum(probs * portfolio_returns)

# Step 3: Variance calculation
squared_deviations = (portfolio_returns - exp_portfolio_return) ** 2
portfolio_variance = np.sum(probs * squared_deviations)

# Step 4: Standard deviation
portfolio_std = np.sqrt(portfolio_variance)

# Convert to percentage
portfolio_std_pct = portfolio_std * 100

portfolio_std_pct  # Result in percentage
```

**Common Bugs to Avoid:**
- Computing variance of individual assets first, then trying to combine (ignores covariance)
- Forgetting to square the deviations before weighting by probabilities
- Confusing variance (squared units) with standard deviation (linear units)
- Not converting returns from percentages to decimals before calculation
- Returning variance when standard deviation is requested (or vice versa)

---

## Pattern: Individual Asset Variance from Probability Distribution

**Description:** Asset variance and standard deviation from probability distributions require computing expected return first, then probability-weighted squared deviations for variance, and finally taking the square root for standard deviation. Results must maintain proper percentage units throughout (returns in %, standard deviation in %, variance in %²).

**When to Use:** Questions asking for variance or standard deviation of individual securities given state-based return distributions with probabilities, or when computing volatility measures from discrete probability scenarios.

**Procedure:**
1. Formula: E(R) = Σ[p_i × r_i]; Var(R) = Σ[p_i × (r_i - E(R))²]; σ = √Var(R)
2. Calculate expected return as probability-weighted average of returns
3. For each state, compute squared deviation from expected return
4. Sum probability-weighted squared deviations to get variance
5. Take square root of variance to get standard deviation
6. Maintain percentage units: if returns are in %, standard deviation is in %, variance is in %²

**Code Example:**

**Scenario:** A stock has returns of 10%, 15%, and 25% with probabilities 0.3, 0.5, 0.2 respectively. Calculate standard deviation.

**Correct Code:**
```python
import math

# Given data
returns = [10, 15, 25]  # in percentage terms
probabilities = [0.3, 0.5, 0.2]

# Step 1: Expected return
expected_return = sum(p * r for p, r in zip(probabilities, returns))

# Step 2: Variance (in percentage-squared units)
variance = sum(p * (r - expected_return)**2 for p, r in zip(probabilities, returns))

# Step 3: Standard deviation (in percentage units)
std_dev = math.sqrt(variance)

std_dev  # Result: 5.22% (as numeric 5.22)
```

**Common Bugs to Avoid:**
- Converting percentages to decimals (e.g., 10% → 0.10) before calculation, then forgetting to convert back
- Returning variance instead of standard deviation when standard deviation is requested
- Using print() instead of expression on last line
- Incorrect unit labeling (reporting 5.22 as 0.0522 or vice versa)

---
## Pattern: Correlation Coefficient from Probability Distribution

**Description:** Correlation between two securities requires computing covariance using probability-weighted products of deviations, then dividing by the product of standard deviations. Result must be between -1 and +1.

**When to Use:** Questions asking for correlation between two securities given their returns across states with probabilities.

**Procedure:**
1. Formula: ρ(X,Y) = Cov(X,Y) / (σ_X × σ_Y) where Cov(X,Y) = Σ(P_i × (X_i - E[X]) × (Y_i - E[Y]))
2. Compute expected returns for both securities
3. Compute standard deviations for both securities
4. Compute covariance: probability-weighted sum of product of deviations
5. Divide covariance by product of standard deviations
6. Verify result is between -1 and +1 (sanity check)

**Code Example:**

**Scenario:** Two stocks with returns across three states

**Correct Code:**
```python
import numpy as np

# Data
probs = np.array([0.2, 0.5, 0.3])
returns_a = np.array([0.08, 0.12, 0.16])
returns_b = np.array([0.15, 0.10, 0.05])

# Step 1: Expected returns
exp_a = np.sum(probs * returns_a)
exp_b = np.sum(probs * returns_b)

# Step 2: Standard deviations
var_a = np.sum(probs * (returns_a - exp_a) ** 2)
var_b = np.sum(probs * (returns_b - exp_b) ** 2)
std_a = np.sqrt(var_a)
std_b = np.sqrt(var_b)

# Step 3: Covariance
deviations_a = returns_a - exp_a
deviations_b = returns_b - exp_b
covariance = np.sum(probs * deviations_a * deviations_b)

# Step 4: Correlation
correlation = covariance / (std_a * std_b)

# Sanity check
assert -1 <= correlation <= 1, "Correlation must be between -1 and 1"

correlation  # Result between -1 and 1
```

**Common Bugs to Avoid:**
- Computing covariance without probability weights
- Using variance instead of standard deviation in denominator
- Not computing deviations from expected values before multiplying
- Getting result outside [-1, +1] range (indicates calculation error)
- Mixing up which returns belong to which security

---

## Pattern: Portfolio Beta and Systematic Risk

**Description:** Portfolio beta is the weighted average of individual asset betas. Systematic variance is (β_p × σ_market)², and total portfolio variance includes both systematic and firm-specific components.

**When to Use:** Questions involving portfolio beta, systematic risk, or total portfolio variance when individual asset betas and firm-specific risks are given.

**Procedure:**
1. Formula: β_p = Σ(w_i × β_i); Var_systematic = (β_p × σ_market)²; Var_firmspecific = Σ(w_i² × σ_ei²)
2. Compute portfolio beta as weighted average of individual betas
3. Compute systematic variance: square of (portfolio beta × market std dev)
4. Compute firm-specific variance: sum of squared weights times squared firm-specific std devs
5. Total variance = systematic variance + firm-specific variance
6. Total std dev = square root of total variance
7. Convert all percentage inputs to decimals before calculation

**Code Example:**

**Scenario:** Portfolio with 60% in Asset 1 (beta=1.2, firm-specific std=25%) and 40% in Asset 2 (beta=0.8, firm-specific std=30%), market std=20%

**Correct Code:**
```python
import numpy as np

# Inputs as decimals
weights = np.array([0.60, 0.40])
betas = np.array([1.2, 0.8])
firm_specific_stds = np.array([0.25, 0.30])
market_std = 0.20

# Step 1: Portfolio beta
portfolio_beta = np.sum(weights * betas)

# Step 2: Systematic variance
systematic_variance = (portfolio_beta * market_std) ** 2

# Step 3: Firm-specific variance (weights must be squared)
firm_specific_variance = np.sum((weights ** 2) * (firm_specific_stds ** 2))

# Step 4: Total variance
total_variance = systematic_variance + firm_specific_variance

# Step 5: Total standard deviation
total_std = np.sqrt(total_variance)

# Step 6: Firm-specific std dev of portfolio
portfolio_firm_specific_std = np.sqrt(firm_specific_variance)

# Convert to percentages
total_std_pct = total_std * 100
portfolio_firm_specific_std_pct = portfolio_firm_specific_std * 100

total_std_pct  # Result in percentage
```

**Common Bugs to Avoid:**
- Using linear weights instead of squared weights for firm-specific variance aggregation
- Forgetting to square the (beta × market_std) term for systematic variance
- Adding standard deviations instead of variances
- Not converting percentage inputs to decimals
- Confusing total variance with systematic variance only

---

## Pattern: Two-Factor APT Model Risk Premium Calculation

**Description:** In a two-factor APT model, risk premiums for each factor must be solved using a system of simultaneous equations from two portfolios with different factor loadings, using the formula E(R) = R_f + β₁×RP₁ + β₂×RP₂.

**When to Use:** Questions asking for factor risk premiums in multi-factor models given portfolio expected returns, factor loadings (betas), and risk-free rate.

**Procedure:**
1. Formula: E(R_i) = R_f + β_i1 × RP_1 + β_i2 × RP_2 for each portfolio i
2. Set up system of equations: one equation per portfolio
3. Solve simultaneously for RP_1 and RP_2 using linear algebra or substitution
4. Convert all percentage inputs to decimals before calculation
5. Convert final risk premiums back to percentages if needed

**Code Example:**

**Scenario:** Portfolio A: E(R)=15%, β₁=0.9, β₂=1.2; Portfolio B: E(R)=12%, β₁=1.5, β₂=0.3; R_f=4%

**Correct Code:**
```python
import numpy as np

# Inputs as decimals
r_f = 0.04
# Portfolio A
exp_return_a = 0.15
beta_a1 = 0.9
beta_a2 = 1.2
# Portfolio B
exp_return_b = 0.12
beta_b1 = 1.5
beta_b2 = 0.3

# Step 1: Set up system of equations
# E(R_A) - R_f = β_A1 × RP_1 + β_A2 × RP_2
# E(R_B) - R_f = β_B1 × RP_1 + β_B2 × RP_2

# Coefficient matrix (betas)
A = np.array([
    [beta_a1, beta_a2],
    [beta_b1, beta_b2]
])

# Constants (excess returns)
b = np.array([
    exp_return_a - r_f,
    exp_return_b - r_f
])

# Step 2: Solve for risk premiums
risk_premiums = np.linalg.solve(A, b)
rp_1 = risk_premiums[0]
rp_2 = risk_premiums[1]

# Convert to percentages
rp_1_pct = rp_1 * 100
rp_2_pct = rp_2 * 100

rp_1_pct  # Risk premium for factor 1 in percentage
```

**Common Bugs to Avoid:**
- Not subtracting risk-free rate from expected returns before solving
- Setting up coefficient matrix incorrectly (transposing betas)
- Forgetting to convert percentages to decimals before calculation
- Solving for only one risk premium instead of both simultaneously
- Arithmetic errors in manual substitution method

---

## Pattern: S&P 500 Futures Hedge Calculation

**Description:** Calculating futures position changes requires knowing the contract multiplier ($250 per point for S&P 500), computing the hedge ratio based on portfolio value and beta, then multiplying by index point change and multiplier.

**When to Use:** Questions involving S&P 500 futures hedging, calculating position changes, or determining number of contracts needed.

**Procedure:**
1. Formula: Contracts = (Portfolio Value × β) / (Index Value × Multiplier); Change = Contracts × Point Change × Multiplier
2. Identify contract multiplier (S&P 500 = $250 per point)
3. Calculate number of contracts needed: (Portfolio Value × Beta) / (Index Value × Multiplier)
4. Calculate position change: Number of Contracts × Index Point Change × Multiplier
5. Round to nearest answer option if necessary

**Code Example:**

**Scenario:** Portfolio value $2M, beta=0.75, S&P at 1500, expected drop to 1300, find position change

**Correct Code:**
```python
# Inputs
portfolio_value = 2_000_000
portfolio_beta = 0.75
current_index = 1500
expected_index = 1300
sp500_multiplier = 250  # dollars per index point

# Step 1: Calculate number of contracts needed
num_contracts = (portfolio_value * portfolio_beta) / (current_index * sp500_multiplier)

# Step 2: Calculate index point change
index_point_change = expected_index - current_index  # negative for drop

# Step 3: Calculate futures position change
position_change = num_contracts * index_point_change * sp500_multiplier

# Absolute value for magnitude
position_change_magnitude = abs(position_change)

position_change_magnitude  # Result in dollars
```

**Common Bugs to Avoid:**
- Using incorrect multiplier (not $250 for S&P 500)
- Forgetting to include portfolio beta in hedge ratio calculation
- Not accounting for sign of index change (drop is negative)
- Rounding number of contracts too early in calculation
- Confusing index points with dollar values

---

## Pattern: M² (M-Squared) Measure Portfolio Adjustment

**Description:** M² measure requires adjusting portfolio volatility to match market volatility by mixing with T-bills. The weight in T-bills is 1 - (σ_market / σ_portfolio), which is positive when de-leveraging a high-volatility portfolio.

**When to Use:** Questions asking for T-bill allocation to adjust portfolio risk to market risk level for M² performance measure.

**Procedure:**
1. Formula: w_Tbill = 1 - (σ_market / σ_portfolio); w_risky = σ_market / σ_portfolio
2. Convert standard deviations to same units (decimals)
3. Calculate ratio of market std dev to portfolio std dev
4. T-bill weight = 1 - ratio (positive means invest in T-bills, negative means borrow)
5. Verify: if portfolio is riskier than market (σ_p > σ_m), T-bill weight should be positive
6. Convert to percentage for answer

**Code Example:**

**Scenario:** Portfolio std dev = 35%, market std dev = 25%, find T-bill weight

**Correct Code:**
```python
# Inputs as decimals
portfolio_std = 0.35
market_std = 0.25

# Step 1: Calculate ratio of market to portfolio volatility
volatility_ratio = market_std / portfolio_std

# Step 2: Calculate T-bill weight
# To match market volatility, invest (volatility_ratio) in risky portfolio
# and (1 - volatility_ratio) in T-bills
weight_risky_asset = volatility_ratio
weight_tbill = 1 - volatility_ratio

# Step 3: Convert to percentage
weight_tbill_pct = weight_tbill * 100

# Sanity check: if portfolio is riskier, T-bill weight should be positive
assert portfolio_std > market_std and weight_tbill > 0, "Sign check failed"

weight_tbill_pct  # Result in percentage (positive = invest, negative = borrow)
```

**Common Bugs to Avoid:**
- Inverting the ratio (using σ_portfolio / σ_market instead)
- Getting sign wrong (confusing borrowing with lending)
- Not recognizing that higher portfolio volatility requires positive T-bill weight
- Forgetting to convert decimal result to percentage
- Misinterpreting negative weight as the answer when positive is correct

---

## Pattern: Taylor Rule Interest Rate Calculation

**Description:** Taylor rule calculates optimal short-term rate as: Target = Neutral Rate + 0.5×(GDP gap) + 0.5×(Inflation gap), where gaps are forecast minus trend/target values.

**When to Use:** Questions asking for central bank target rate using Taylor rule given GDP forecasts/trends and inflation forecasts/targets.

**Procedure:**
1. Formula: Target Rate = Neutral Rate + 0.5×(GDP_forecast - GDP_trend) + 0.5×(Inflation_forecast - Inflation_target)
2. Identify neutral/equilibrium rate (often given as "appropriate rate assuming no other factors")
3. Calculate GDP gap: forecast minus trend (positive if above trend)
4. Calculate inflation gap: forecast minus target (negative if below target)
5. Apply equal weights (0.5) to each gap unless specified otherwise
6. Sum all components to get target rate
7. Convert to percentage if needed

**Code Example:**

**Scenario:** Neutral rate=3%, GDP forecast=2.5%, GDP trend=2%, Inflation forecast=1.8%, Inflation target=2.5%

**Correct Code:**
```python
# Inputs as decimals
neutral_rate = 0.03
gdp_forecast = 0.025
gdp_trend = 0.020
inflation_forecast = 0.018
inflation_target = 0.025

# Step 1: Calculate gaps
gdp_gap = gdp_forecast - gdp_trend
inflation_gap = inflation_forecast - inflation_target

# Step 2: Apply Taylor rule with equal weights (0.5 each)
weight_gdp = 0.5
weight_inflation = 0.5

target_rate = neutral_rate + weight_gdp * gdp_gap + weight_inflation * inflation_gap

# Convert to percentage
target_rate_pct = target_rate * 100

target_rate_pct  # Result in percentage
```

**Common Bugs to Avoid:**
- Using wrong baseline (current rate instead of neutral rate)
- Calculating gaps incorrectly (trend minus forecast instead of forecast minus trend)
- Not applying the 0.5 weights to gaps
- Forgetting that inflation gap can be negative (below target)
- Misidentifying which rate is the "neutral" rate from problem context

---

## Pattern: Weighted Average Expected Return with Precision

**Description:** Expected return calculations require precise arithmetic: multiply each probability by its corresponding return, sum all products, and maintain sufficient decimal precision throughout to avoid rounding errors.

**When to Use:** Questions asking for expected return of a single asset given probability distribution of returns across states.

**Procedure:**
1. Formula: E(R) = Σ(P_i × R_i)
2. Convert all percentage returns to decimal form
3. Multiply each probability by its corresponding return
4. Sum all products without premature rounding
5. Convert final result to percentage if needed
6. Verify sum of probabilities equals 1.0 (sanity check)

**Code Example:**

**Scenario:** Stock returns: 8% (prob 0.20), 12% (prob 0.50), 18% (prob 0.30)

**Correct Code:**
```python
import numpy as np

# Data as decimals
probabilities = np.array([0.20, 0.50, 0.30])
returns = np.array([0.08, 0.12, 0.18])

# Sanity check: probabilities sum to 1
assert np.isclose(np.sum(probabilities), 1.0), "Probabilities must sum to 1"

# Step 1: Calculate expected return
expected_return = np.sum(probabilities * returns)

# Step 2: Convert to percentage
expected_return_pct = expected_return * 100

expected_return_pct  # Result in percentage
```

**Common Bugs to Avoid:**
- Rounding intermediate products before final sum
- Using percentage values directly without converting to decimals
- Extracting wrong values from tables (OCR errors)
- Not verifying probabilities sum to 1.0
- Premature rounding causing accumulation of errors

---

## Pattern: Portfolio Variance with Covariance Matrix

**Description:** When computing portfolio variance from individual asset variances and covariances, must use the full quadratic form: Var(R_p) = w'Σw, where Σ includes all variances and covariances, not just weighted sum of individual variances.

**When to Use:** Questions asking for portfolio variance when correlation or covariance between assets is non-zero, or when state-by-state returns allow covariance calculation.

**Procedure:**
1. Formula: Var(R_p) = Σᵢ Σⱼ (w_i × w_j × Cov(i,j))
2. Compute variance-covariance matrix from state returns or given correlations
3. For each pair of assets, include w_i × w_j × Cov(i,j) term
4. Diagonal terms are w_i² × Var(i)
5. Off-diagonal terms are 2 × w_i × w_j × Cov(i,j) for i≠j
6. Sum all terms for total portfolio variance
7. Take square root for standard deviation

**Code Example:**

**Scenario:** Two-asset portfolio: 60% Asset A (var=0.04), 40% Asset B (var=0.09), correlation=0.3

**Correct Code:**
```python
import numpy as np

# Inputs
weights = np.array([0.60, 0.40])
variances = np.array([0.04, 0.09])  # variance in decimal-squared
correlation = 0.3

# Step 1: Calculate standard deviations
std_devs = np.sqrt(variances)

# Step 2: Calculate covariance
covariance = correlation * std_devs[0] * std_devs[1]

# Step 3: Build covariance matrix
cov_matrix = np.array([
    [variances[0], covariance],
    [covariance, variances[1]]
])

# Step 4: Calculate portfolio variance using quadratic form
portfolio_variance = weights @ cov_matrix @ weights

# Step 5: Portfolio standard deviation
portfolio_std = np.sqrt(portfolio_variance)

# Convert to percentage
portfolio_std_pct = portfolio_std * 100

portfolio_std_pct  # Result in percentage
```

**Common Bugs to Avoid:**
- Computing weighted average of variances (ignores covariance)
- Forgetting to include off-diagonal covariance terms
- Using linear weights instead of squared weights for variance terms
- Not doubling off-diagonal terms when manually summing
- Confusing correlation with covariance

## Pattern: GARCH Model Variance to Volatility Conversion

**Description:** GARCH(1,1) and similar volatility models output variance (σ²), not volatility (σ). The formula σ²_n = ω + α×u²_{n-1} + β×σ²_{n-1} produces variance; volatility requires taking the square root of this result.

**When to Use:** Questions involving GARCH, EWMA, or other volatility models that ask for "volatility" or "standard deviation" as the final answer, especially when the model formula explicitly produces variance.

**Procedure:**
1. Formula: σ²_n = ω + α×u²_{n-1} + β×σ²_{n-1} (GARCH variance); σ_n = √(σ²_n) (volatility)
2. Calculate the squared return u²_{n-1} from the most recent price change
3. Apply the GARCH formula using previous variance estimate σ²_{n-1}
4. The result is variance (σ²_n)
5. Take square root to obtain volatility (σ_n) if that is what's requested

**Code Example:**

**Scenario:** Previous volatility was 1.5% daily, yesterday's return was -0.8%, GARCH parameters are ω=0.000003, α=0.05, β=0.93. Find new volatility.

**Correct Code:**
```python
import math

# Given data
prev_volatility = 0.015  # 1.5% as decimal
recent_return = -0.008  # -0.8% as decimal
omega = 0.000003
alpha = 0.05
beta = 0.93

# Step 1: Previous variance
prev_variance = prev_volatility ** 2

# Step 2: Squared return
u_squared = recent_return ** 2

# Step 3: GARCH variance formula
new_variance = omega + alpha * u_squared + beta * prev_variance

# Step 4: Convert variance to volatility (CRITICAL STEP)
new_volatility = math.sqrt(new_variance)

new_volatility  # Result in decimal form (e.g., 0.01456 for 1.456%)
```

**Common Bugs to Avoid:**
- Returning variance directly when volatility is requested (forgetting the square root)
- Confusing variance and volatility terminology
- Using volatility instead of variance in the GARCH formula (should use σ²_{n-1}, not σ_{n-1})
- Missing the math.sqrt() import

---

## Pattern: Complete Comparative Performance Metric Analysis

**Description:** Performance evaluation questions requiring selection of "best" or "highest" performer demand computing the metric (Jensen's alpha, Sharpe ratio, Treynor ratio, etc.) for ALL candidates before comparison, not stopping after the first calculation.

**When to Use:** Multiple-choice questions asking "which fund has the highest [metric]" or "the best performer is" when given data for multiple securities or portfolios.

**Procedure:**
1. Formula: Jensen's Alpha = R_p - [R_f + β_p × (R_m - R_f)]
2. Extract relevant data for ALL candidates from the problem
3. Compute the performance metric for each candidate systematically
4. Store results in a comparable format (dictionary or list)
5. Identify the maximum/minimum value and corresponding candidate
6. Return the selected option based on comparison

**Code Example:**

**Scenario:** Three funds have returns of 12%, 14%, 11% with betas 1.1, 1.3, 0.9. Risk-free rate is 3%, market return is 10%. Which has highest Jensen's alpha?

**Correct Code:**
```python
# Given data
funds = {
    'A': {'return': 0.12, 'beta': 1.1},
    'B': {'return': 0.14, 'beta': 1.3},
    'C': {'return': 0.11, 'beta': 0.9}
}
rf = 0.03
rm = 0.10

# Step 1: Calculate Jensen's alpha for ALL funds
alphas = {}
for fund_name, data in funds.items():
    expected_return = rf + data['beta'] * (rm - rf)
    alpha = data['return'] - expected_return
    alphas[fund_name] = alpha

# Step 2: Find the fund with highest alpha
best_fund = max(alphas, key=alphas.get)
best_alpha = alphas[best_fund]

best_fund  # Result: 'C' (or corresponding option letter)
```

**Common Bugs to Avoid:**
- Computing metric for only one candidate and returning immediately
- Forgetting to compare all candidates before selecting the answer
- Not storing intermediate results for comparison
- Returning the metric value instead of the fund identifier

---

## Pattern: Multi-Factor Model Total Return Calculation

**Description:** Multi-factor models compute total return as base expected return plus the sum of factor surprises weighted by factor sensitivities: R = E(R) + Σ[β_i × (Actual_i - Expected_i)]. Each factor contribution is (actual - expected) × beta, and all contributions are added to the base return.

**When to Use:** Questions asking for "total return" or "realized return" given a factor model with expected returns, factor betas, expected factor values, and actual factor values.

**Procedure:**
1. Formula: R_total = E(R) + Σ[β_i × (Actual_i - Expected_i)]
2. Identify base expected return
3. For each factor, calculate surprise: (Actual - Expected)
4. Multiply each surprise by its corresponding beta
5. Sum all weighted surprises
6. Add the sum to base expected return
7. Ensure percentage arithmetic is consistent (if values are in %, keep in %)

**Code Example:**

**Scenario:** Expected return is 9%, Factor 1 beta=1.5 (expected 3%, actual 3.4%), Factor 2 beta=0.8 (expected 5%, actual 5.6%). Find total return.

**Correct Code:**
```python
# Given data
expected_return = 9.0  # in percentage points

factors = [
    {'beta': 1.5, 'expected': 3.0, 'actual': 3.4},
    {'beta': 0.8, 'expected': 5.0, 'actual': 5.6}
]

# Step 1: Calculate factor contributions
factor_contribution = 0
for factor in factors:
    surprise = factor['actual'] - factor['expected']
    contribution = factor['beta'] * surprise
    factor_contribution += contribution

# Step 2: Total return
total_return = expected_return + factor_contribution

total_return  # Result: 9.0 + 1.5*0.4 + 0.8*0.6 = 10.08%
```

**Common Bugs to Avoid:**
- Using wrong sign for surprise (expected - actual instead of actual - expected)
- Forgetting to multiply surprise by beta before summing
- Omitting one or more factors from the calculation
- Mixing percentage points and decimals inconsistently (e.g., 0.4% vs 0.004)

---

## Pattern: Grinold-Kroner Model Component Aggregation

**Description:** The Grinold-Kroner model estimates equity returns as: E(R) ≈ Dividend Yield - ΔShares% + Inflation + Real Earnings Growth + ΔP/E%. Share buybacks (negative ΔShares) contribute positively to per-share returns and must be added with correct sign.

**When to Use:** Questions asking for expected equity market returns using the Grinold-Kroner model, especially when share repurchases or changes in shares outstanding are mentioned.

**Procedure:**
1. Formula: E(R) ≈ D/P - ΔS + i + ΔEG_real + ΔP/E
2. Identify dividend yield (D/P)
3. Identify change in shares outstanding (ΔS); if shares decline, this is negative
4. Note: -ΔS means if shares decline by 1%, this contributes +1% to return
5. Add inflation rate
6. Add real earnings growth (often GDP growth + earnings premium)
7. Add expected change in P/E multiple
8. Sum all components with correct signs

**Code Example:**

**Scenario:** Dividend yield 2.5%, shares decline 0.8%, inflation 2%, GDP growth 3%, earnings premium 1.2%, P/E expansion 0.3%. Find expected return.

**Correct Code:**
```python
# Given data
dividend_yield = 2.5
change_in_shares = -0.8  # negative means decline (buybacks)
inflation = 2.0
gdp_growth = 3.0
earnings_premium = 1.2
pe_change = 0.3

# Step 1: Real earnings growth
real_earnings_growth = gdp_growth + earnings_premium

# Step 2: Grinold-Kroner formula
# Note: -ΔS, so if shares decline (negative), we subtract a negative (add positive)
expected_return = (dividend_yield 
                   - change_in_shares  # subtracting negative = adding
                   + inflation 
                   + real_earnings_growth 
                   + pe_change)

expected_return  # Result: 2.5 - (-0.8) + 2.0 + 4.2 + 0.3 = 9.8%
```

**Common Bugs to Avoid:**
- Incorrect sign handling for share repurchases (subtracting when should add)
- Forgetting to include all five components
- Confusing nominal and real earnings growth
- Missing the earnings premium component when computing real earnings growth

---

## Pattern: Brinson-Fachler Allocation Effect Calculation

**Description:** The Brinson-Fachler allocation effect measures return impact of portfolio weight decisions: Allocation Effect = (Portfolio Weight - Benchmark Weight) × (Benchmark Return - Total Benchmark Return). Calculation requires precise arithmetic with percentage points.

**When to Use:** Questions asking for "allocation effect" in performance attribution analysis, particularly in Brinson-Fachler or Brinson-Hood-Beebower frameworks with sector or regional breakdowns.

**Procedure:**
1. Formula: Allocation Effect = (w_p - w_b) × (R_b - R_total_b)
2. Extract portfolio weight and benchmark weight for the segment
3. Extract benchmark return for the segment
4. Extract total benchmark return (portfolio-wide)
5. Calculate weight difference: (w_p - w_b)
6. Calculate return difference: (R_b - R_total_b)
7. Multiply the two differences
8. Result is in percentage points if inputs are in percentage points

**Code Example:**

**Scenario:** Sector has portfolio weight 25%, benchmark weight 22%, sector benchmark return 18%, total benchmark return 12%. Find allocation effect.

**Correct Code:**
```python
# Given data (in percentage points)
portfolio_weight = 25.0
benchmark_weight = 22.0
sector_benchmark_return = 18.0
total_benchmark_return = 12.0

# Step 1: Weight difference
weight_diff = portfolio_weight - benchmark_weight

# Step 2: Return difference
return_diff = sector_benchmark_return - total_benchmark_return

# Step 3: Allocation effect
allocation_effect = (weight_diff / 100) * return_diff

allocation_effect  # Result: 0.03 * 6.0 = 0.18 percentage points
```

**Common Bugs to Avoid:**
- Using portfolio return instead of benchmark return in the formula
- Reversing the subtraction order (benchmark - portfolio instead of portfolio - benchmark)
- Forgetting to convert percentage weights to decimals when multiplying
- Confusing allocation effect with selection effect formulas

---

## Pattern: Covariance Calculation from Correlation and Standard Deviations

**Description:** Covariance is calculated from correlation coefficient and standard deviations using: Cov(X,Y) = ρ × σ_X × σ_Y. When standard deviations are given in percentage terms, covariance is in percentage-squared units, and the numeric values should be multiplied directly without decimal conversion.

**When to Use:** Questions asking for covariance between two assets when given correlation coefficient and standard deviations, particularly in portfolio analysis contexts.

**Procedure:**
1. Formula: Cov(X,Y) = ρ_{X,Y} × σ_X × σ_Y
2. Extract correlation coefficient (dimensionless, between -1 and +1)
3. Extract standard deviation of first asset (in % or decimal)
4. Extract standard deviation of second asset (same units)
5. Multiply: correlation × std_dev_1 × std_dev_2
6. Result units: if std devs in %, covariance in %²; if in decimals, covariance in decimal²

**Code Example:**

**Scenario:** Stock A has std dev 15%, Stock B has std dev 20%, correlation is 0.35. Find covariance.

**Correct Code:**
```python
# Given data (standard deviations in percentage terms)
std_dev_A = 15.0  # 15%
std_dev_B = 20.0  # 20%
correlation = 0.35

# Covariance calculation
# When std devs are in %, result is in %² (percentage-squared)
covariance = correlation * std_dev_A * std_dev_B

covariance  # Result: 105.0 (%²), meaning 105 percentage-squared
```

**Common Bugs to Avoid:**
- Converting percentages to decimals (15% → 0.15) then reporting without re-scaling
- Confusing variance with covariance formulas
- Incorrect unit interpretation (reporting 1.05 when answer should be 105 in %² units)
- Using correlation formula instead of covariance formula

---

## Pattern: Portfolio Beta Calculation for Multi-Asset Portfolios

**Description:** Portfolio beta for a three-factor model requires computing portfolio-level factor sensitivities as weighted averages: β_p,i = Σ(w_j × β_j,i), then applying the factor model with risk premiums: E(R_p) = R_f + Σ(β_p,i × RP_i).

**When to Use:** Questions asking for expected return of a portfolio in a multi-factor model context, given individual stock factor betas, portfolio weights, risk-free rate, and factor risk premiums.

**Procedure:**
1. Formula: β_p,i = Σ(w_j × β_j,i); E(R_p) = R_f + Σ(β_p,i × RP_i)
2. For each factor, calculate portfolio beta as weighted average of stock betas
3. Multiply each portfolio beta by its corresponding risk premium
4. Sum all factor contributions
5. Add risk-free rate to get expected portfolio return
6. Ensure percentage arithmetic consistency

**Code Example:**

**Scenario:** Portfolio: 30% Stock A (betas: 1.2, 0.8), 70% Stock B (betas: 0.9, 1.1). Risk-free rate 4%, risk premiums 5%, 3%. Find expected return.

**Correct Code:**
```python
# Given data
weights = [0.30, 0.70]
stock_betas = [
    [1.2, 0.8],  # Stock A: factor 1, factor 2
    [0.9, 1.1]   # Stock B: factor 1, factor 2
]
risk_free_rate = 4.0  # in %
risk_premiums = [5.0, 3.0]  # in %

# Step 1: Calculate portfolio betas for each factor
num_factors = len(risk_premiums)
portfolio_betas = []
for factor_idx in range(num_factors):
    portfolio_beta = sum(w * stock_betas[stock_idx][factor_idx] 
                        for stock_idx, w in enumerate(weights))
    portfolio_betas.append(portfolio_beta)

# Step 2: Calculate factor contributions
factor_contribution = sum(beta * rp for beta, rp in zip(portfolio_betas, risk_premiums))

# Step 3: Expected return
expected_return = risk_free_rate + factor_contribution

expected_return  # Result in percentage points
```

**Common Bugs to Avoid:**
- Computing individual stock returns then averaging (wrong order of operations)
- Forgetting to weight betas by portfolio weights
- Applying risk premiums to individual stocks before portfolio aggregation
- Confusing factor betas with portfolio weights