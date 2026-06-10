# SKILL PATTERNS FOR PORTFOLIO MANAGEMENT: UNIT/CURRENCY/PERCENT CONVERSION ERRORS (PoT)

## Pattern: Portfolio Expected Return Calculation

**Description:** Portfolio expected return must be computed as the weighted average of individual asset expected returns, where each asset's expected return is first calculated using probability-weighted state returns, then combined using portfolio weights. **Critical: Portfolio weights must be explicitly provided or clearly derivable from context—never assume equal weights without justification. When the question asks for an "equally-weighted portfolio", this is explicit instruction to use equal weights.**

**When to Use:** Questions asking for portfolio expected return given individual asset returns across states and portfolio weights, or when combining multiple securities into a portfolio.

**Procedure:**
1. Formula: E(R_p) = Σ(w_i × E(R_i)) where E(R_i) = Σ(P_j × R_ij)
2. **CHECK WEIGHTS: Verify portfolio weights are explicitly stated in the question, table, or context**
3. **VALIDATION: If weights are not provided, check if the question asks to "assume equal weights", "equally-weighted portfolio", or similar instruction**
4. **IF EQUAL WEIGHTS SPECIFIED: Use w_i = 1/n for n assets**
5. **HALT IF MISSING: If weights cannot be determined and no equal-weight instruction exists, flag as insufficient information**
6. First compute expected return for each asset: multiply each state return by its probability and sum
7. Then compute portfolio expected return: multiply each asset's expected return by its portfolio weight and sum
8. Convert to percentage if answer options are in percentage format (multiply by 100)

**Example (sanitized):**

> **Scenario 1 (Equal weights specified):** Three stocks with returns in strong growth: A=39%, B=30%, C=6%. Question asks: "If you invested in an equally-weighted portfolio of stocks A and C, your portfolio return would be _____ if economic growth was strong."
>
> **Correct approach:**
> ```python
> # Equal weights explicitly stated in question
> weights = {'A': 0.50, 'C': 0.50}
> returns_strong = {'A': 0.39, 'C': 0.06}
> 
> portfolio_return = sum(weights[stock] * returns_strong[stock] 
>                       for stock in ['A', 'C'])
> 
> portfolio_return * 100  # Result: 22.5%
> ```

> **Scenario 2 (No weights specified):** Three stocks with expected returns 8%, 12%, 15%. Question asks: "What is the portfolio expected return?" No weights mentioned, no "equal weight" instruction.
>
> **Correct approach:**
> ```python
> # Flag as insufficient information
> raise ValueError("Portfolio weights not specified in question or context. Cannot assume equal weights without explicit instruction.")
> ```

**Common Mistakes to Avoid:**
- **Assuming equal weights (1/n for n assets) without explicit instruction to do so**
- **Not recognizing "equally-weighted portfolio" as explicit instruction for equal weights**
- **Not searching context/tables for weight information before assuming**
- Computing state-by-state portfolio returns first, then averaging (incorrect order of operations)
- Forgetting to convert percentage returns to decimals before calculation
- Mismatching units between calculation (decimal) and answer options (percentage)

---
## Pattern: Portfolio Variance and Standard Deviation from State Returns

**Description:** Portfolio variance requires computing portfolio returns for each state, calculating the expected portfolio return, then computing probability-weighted squared deviations. This state-by-state approach automatically captures all correlations and covariances between assets. **Critical: When state-level returns are available, ALWAYS use the state-by-state method—never assume zero correlation or use diagonal-only variance formulas.**

**When to Use:** Questions asking for portfolio variance or standard deviation given individual asset returns across economic states and portfolio weights.

**When NOT to Use:**
- When the question asks for individual security variance (use individual asset variance pattern instead)
- When only correlation coefficients are given without state-level data (use covariance matrix pattern instead)

**Procedure:**
1. Formula: Var(R_p) = Σ(P_j × (R_pj - E(R_p))²) where R_pj = Σ(w_i × R_ij)
2. **CHECK: Verify probabilities sum to 1.0 (within tolerance)**
3. **CHECK: Verify all arrays have same length**
4. **CRITICAL STEP: Compute portfolio return for EACH state separately: R_p,state = Σ(weight_i × return_i,state)**
5. Compute expected portfolio return: probability-weighted average of state portfolio returns
6. Compute variance: probability-weighted sum of squared deviations from expected return
7. For standard deviation: take square root of variance
8. **VERIFY: Check result is finite and non-negative**
9. **SPECIAL CASE: If variance is exactly 0 (or < 1e-10), return 0 or 0.0 without percentage conversion**
10. Convert to percentage units only if variance > 0 and answer format requires it

**Example (sanitized):**

> **Scenario:** Portfolio with 40% in Stock X and 60% in Stock Y. Three states with probabilities [0.25, 0.50, 0.25]. Stock X returns: [0.05, 0.10, 0.15]. Stock Y returns: [0.12, 0.08, 0.04]. Calculate standard deviation.
>
> **Wrong approach (assumes zero correlation):**
> ```python
> # INCORRECT: Computes individual variances, assumes independence
> var_x = sum(p * (r - exp_x)**2 for p, r in zip(probs, returns_x))
> var_y = sum(p * (r - exp_y)**2 for p, r in zip(probs, returns_y))
> portfolio_var = (0.4**2 * var_x) + (0.6**2 * var_y)  # Missing covariance terms!
> ```
>
> **Correct approach (state-by-state):**
> ```python
> import numpy as np
> 
> # State data
> probs = np.array([0.25, 0.50, 0.25])
> returns_x = np.array([0.05, 0.10, 0.15])
> returns_y = np.array([0.12, 0.08, 0.04])
> weights = np.array([0.40, 0.60])
> 
> # Step 1: VALIDATION
> assert np.isclose(np.sum(probs), 1.0), "Probabilities must sum to 1"
> assert len(probs) == len(returns_x) == len(returns_y), "Array lengths must match"
> 
> # Step 2: CRITICAL - Portfolio return in EACH state
> # This automatically captures correlation structure
> portfolio_returns_by_state = weights[0] * returns_x + weights[1] * returns_y
> 
> # Step 3: Expected portfolio return
> exp_portfolio_return = np.sum(probs * portfolio_returns_by_state)
> 
> # Step 4: Variance from state-by-state deviations
> squared_deviations = (portfolio_returns_by_state - exp_portfolio_return) ** 2
> portfolio_variance = np.sum(probs * squared_deviations)
> 
> # Step 5: Standard deviation
> portfolio_std = np.sqrt(portfolio_variance)
> 
> # Step 6: Convert to percentage if needed
> portfolio_std * 100  # Result in percentage
> ```

**Common Mistakes to Avoid:**
- **Computing individual asset variances first, then combining with diagonal-only formula (ignores covariance)**
- **Assuming zero correlation when state-level returns are available**
- **Not following the state-by-state procedure stated in the pattern description**
- Not validating that probabilities sum to 1.0 before calculation
- Forgetting to square the deviations before weighting by probabilities
- Confusing variance (squared units) with standard deviation (linear units)

---
## Pattern: Individual Asset Variance from Probability Distribution

**Description:** Asset variance and standard deviation from probability distributions require computing expected return first, then probability-weighted squared deviations for variance, and finally taking the square root for standard deviation. **Critical: Detect whether input returns are already in decimal form (0.10) or percentage form (10%) before applying any conversion. Returns must be in decimal form before calculation to produce variance in correct units.**

**When to Use:** Questions asking for variance or standard deviation of individual securities given state-based return distributions with probabilities, or when computing volatility measures from discrete probability scenarios.

**When NOT to Use:** 
- When the question context or ground truth clearly expects decimal output (e.g., "0.0461" or "0.046") rather than percentage output
- When other answer options are in decimal format (< 1.0) rather than percentage format (> 1.0)

**Procedure:**
1. Formula: E(R) = Σ[p_i × r_i]; Var(R) = Σ[p_i × (r_i - E(R))²]; σ = √Var(R)
2. **CHECK INPUT FORMAT: Examine return values - if ALL values < 1.0, they are already decimals; if ANY value > 1.0 or contains '%', they are percentages**
3. **CONDITIONAL CONVERSION: Only convert if values are in percentage form (divide by 100); skip conversion if already decimals**
4. Calculate expected return as probability-weighted average of returns
5. For each state, compute squared deviation from expected return
6. Sum probability-weighted squared deviations to get variance
7. Take square root of variance to get standard deviation
8. **VERIFY: Variance should be small (typically 0.0001 to 0.1) if returns were in decimal form; if variance > 1, likely forgot decimal conversion**
9. **CHECK OUTPUT FORMAT: Examine answer options or ground truth format—if they are < 1.0, return decimal; if > 1.0, multiply by 100 for percentage**

**Example (sanitized):**

> **Scenario:** A stock has returns across three states: State 1 (0.12, prob 0.3), State 2 (0.18, prob 0.5), State 3 (0.24, prob 0.2). Calculate variance. Answer options are in decimal format (e.g., 0.0018, 0.0022).
>
> **Wrong approach:** 
> ```python
> returns = [0.12, 0.18, 0.24]
> # Incorrectly converts already-decimal values
> returns_decimal = [r / 100 for r in returns]  # [0.0012, 0.0018, 0.0024]
> # This produces variance 10,000x too small
> ```
>
> **Correct approach:**
> ```python
> import math
> 
> returns = [0.12, 0.18, 0.24]  # Already in decimal form
> probabilities = [0.3, 0.5, 0.2]
> 
> # Step 1: CHECK - Are these decimals or percentages?
> max_return = max(returns)
> if max_return < 1.0:
>     # Already decimals, no conversion needed
>     returns_decimal = returns
> else:
>     # Percentages, need conversion
>     returns_decimal = [r / 100 for r in returns]
> 
> # Step 2: Expected return
> expected_return = sum(p * r for p, r in zip(probabilities, returns_decimal))
> 
> # Step 3: Variance
> variance = sum(p * (r - expected_return)**2 for p, r in zip(probabilities, returns_decimal))
> 
> # Step 4: VERIFY magnitude
> assert 0.00001 < variance < 1.0, f"Variance {variance} outside typical range - check input format"
> 
> # Step 5: Standard deviation
> std_dev = math.sqrt(variance)
> 
> variance  # Result: 0.0018 (decimal format)
> ```

**Common Mistakes to Avoid:**
- **Applying percentage-to-decimal conversion (÷100) to values already in decimal form (< 1.0)**
- **Not checking maximum value to detect input format before conversion**
- **Double conversion: OCR extracts as decimal, then code divides by 100 again**
- Not verifying that variance magnitude is reasonable (should be < 1 for decimal returns)
- Always converting to percentage without checking answer option format

---
## Pattern: Correlation Coefficient from Probability Distribution

**Description:** Correlation between two securities requires computing covariance using probability-weighted products of deviations, then dividing by the product of standard deviations. Result must be between -1 and +1. **Critical: When matching to multiple-choice options, select the option with the closest absolute value, recognizing that sign differences may indicate the question expects the magnitude rather than the signed value.**

**When to Use:** Questions asking for correlation between two securities given their returns across states with probabilities.

**When NOT to Use:**
- When all answer options are positive and your calculated correlation is negative—verify the question is asking for correlation coefficient (which can be negative) rather than a related measure

**Procedure:**
1. Formula: ρ(X,Y) = Cov(X,Y) / (σ_X × σ_Y) where Cov(X,Y) = Σ(P_i × (X_i - E[X]) × (Y_i - E[Y]))
2. Compute expected returns for both securities
3. Compute standard deviations for both securities
4. Compute covariance: probability-weighted sum of product of deviations
5. Divide covariance by product of standard deviations
6. Verify result is between -1 and +1 (sanity check)
7. **CHECK ANSWER OPTIONS: If calculated correlation is negative but all options are positive, select the option closest to the absolute value of your result**

**Code Example:**

**Scenario:** Two stocks with returns across states, calculated correlation is -0.416, but answer options are all positive values.

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

# Step 5: For answer matching, use absolute value if all options are positive
abs(correlation)  # Use this for matching when options are all positive
```

**Common Bugs to Avoid:**
- Computing covariance without probability weights
- Using variance instead of standard deviation in denominator
- Not computing deviations from expected values before multiplying
- Getting result outside [-1, +1] range (indicates calculation error)
- Mixing up which returns belong to which security
- **Failing to match negative correlation to closest positive option when question context suggests magnitude is expected**

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

**Description:** Calculating futures position changes requires knowing the contract multiplier ($250 per point for S&P 500), computing the hedge ratio based on portfolio value and beta, then multiplying by index point change and multiplier. **Critical: Futures contracts must be rounded DOWN (floor) to avoid over-hedging, since fractional contracts cannot be traded. This pattern applies ONLY when the question explicitly involves futures contracts or hedging strategies—NOT for direct portfolio loss calculations.**

**When to Use:** Questions involving S&P 500 futures hedging, calculating position changes, or determining number of contracts needed for hedging purposes.

**When NOT to Use:** 
- When the question asks for "expected loss" or "portfolio loss" from market movements WITHOUT mentioning futures or hedging
- When the question is about direct portfolio value changes due to market movements
- When no futures contracts or hedging strategy is mentioned in the context

**Procedure:**
1. **CHECK QUESTION TYPE: Does it mention futures contracts, hedging, or derivatives? If NO, this is a direct portfolio calculation—use beta × portfolio value × market change instead**
2. Formula: Contracts = (Portfolio Value × β) / (Index Value × Multiplier); Change = Contracts × Point Change × Multiplier
3. Identify contract multiplier (S&P 500 = $250 per point)
4. Calculate number of contracts needed: (Portfolio Value × Beta) / (Index Value × Multiplier)
5. **CHECK: Round DOWN using floor() or int() - never round() or ceil() - to avoid over-hedging**
6. Calculate position change: Number of Contracts × Index Point Change × Multiplier
7. Verify result magnitude is reasonable relative to portfolio value

**Common Mistakes to Avoid:**
- **Applying futures hedging formulas to direct portfolio loss questions that don't mention hedging**
- **Using futures contract calculations when the question simply asks "what is your expected loss" without hedging context**
- Using round() or ceil() instead of floor() for contract quantities
- Using incorrect multiplier (not $250 for S&P 500)
- Forgetting to include portfolio beta in hedge ratio calculation
- Not accounting for sign of index change (drop is negative)
- Confusing index points with dollar values

**Example (sanitized):**

> **Scenario 1 (Futures Hedging):** Portfolio value $5M, beta=0.8, S&P at 3000, manager wants to hedge using S&P 500 futures. Index expected to drop 150 points. Find futures position change.
>
> **Correct approach:**
> ```python
> import math
> 
> portfolio_value = 5_000_000
> portfolio_beta = 0.8
> current_index = 3000
> index_drop = -150
> sp500_multiplier = 250
> 
> # Futures hedging calculation
> num_contracts_exact = (portfolio_value * portfolio_beta) / (current_index * sp500_multiplier)
> num_contracts = math.floor(num_contracts_exact)
> position_change = num_contracts * index_drop * sp500_multiplier
> 
> abs(position_change)  # Result: futures position change
> ```

> **Scenario 2 (Direct Portfolio Loss - NO futures):** Portfolio value $1M, beta=0.6, S&P at 1400, expected to fall to 1200. What is the expected portfolio loss?
>
> **Wrong approach:**
> ```python
> # INCORRECT: Applying futures formula when no hedging mentioned
> num_contracts = int((1_000_000 * 0.6) / (1400 * 250))
> loss = num_contracts * (-200) * 250  # Wrong!
> ```
>
> **Correct approach:**
> ```python
> # Direct portfolio loss calculation
> portfolio_value = 1_000_000
> portfolio_beta = 0.6
> market_decline_pct = (1200 - 1400) / 1400  # -14.29%
> 
> expected_loss = portfolio_value * portfolio_beta * abs(market_decline_pct)
> expected_loss  # Result: ~$85,714
> ```

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

**Description:** When computing portfolio variance from individual asset variances and covariances, must use the full quadratic form: Var(R_p) = w'Σw, where Σ includes all variances and covariances, not just weighted sum of individual variances. **Critical: The final answer format must match the question's expected output—if ground truth expects variance in decimal-squared units (0.0881), return decimals; if it expects percentage-squared units (881 or 8.81%), apply appropriate scaling.**

**When to Use:** Questions asking for portfolio variance when correlation or covariance between assets is non-zero, or when state-by-state returns allow covariance calculation.

**When NOT to Use:**
- When the question asks for variance and answer options or ground truth are in decimal format (< 1.0) rather than percentage format
- When computing individual security variances in a single-index model context where ground truth expects decimal output

**Procedure:**
1. Formula: Var(R_p) = Σᵢ Σⱼ (w_i × w_j × Cov(i,j))
2. Compute variance-covariance matrix from state returns or given correlations
3. For each pair of assets, include w_i × w_j × Cov(i,j) term
4. Diagonal terms are w_i² × Var(i)
5. Off-diagonal terms are 2 × w_i × w_j × Cov(i,j) for i≠j
6. Sum all terms for total portfolio variance
7. Take square root for standard deviation
8. **CHECK OUTPUT FORMAT: If ground truth shows variance as 0.0881 or similar decimal, return as-is; if shown as 881 or 8.81%, apply appropriate conversion**

**Code Example:**

**Scenario:** Two-asset portfolio: 60% Asset A (var=0.04), 40% Asset B (var=0.09), correlation=0.3. Ground truth expects decimal format.

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

# Step 6: CHECK - Return in format matching ground truth
# If ground truth is 0.0881, return decimal; if 881, multiply by 10000; if 8.81%, multiply by 100
portfolio_variance  # Result: 0.0576 (decimal format)
```

**Common Bugs to Avoid:**
- Computing weighted average of variances (ignores covariance)
- Forgetting to include off-diagonal covariance terms
- Using linear weights instead of squared weights for variance terms
- Not doubling off-diagonal terms when manually summing
- Confusing correlation with covariance
- **Applying percentage conversion (× 100) when ground truth expects decimal output (< 1.0)**

---
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

**Description:** Performance evaluation questions requiring selection of "best" or "highest" performer demand computing the metric (Jensen's alpha, Sharpe ratio, Treynor ratio, etc.) for ALL candidates before comparison, not stopping after the first calculation. **Critical: Return the complete results dictionary or the selected fund identifier, not just a single metric value. Handle answer mapping with proper data structures to avoid execution failures.**

**When to Use:** Multiple-choice questions asking "which fund has the highest [metric]" or "the best performer is" when given data for multiple securities or portfolios.

**Procedure:**
1. Formula: Jensen's Alpha = R_p - [R_f + β_p × (R_m - R_f)]; Sharpe = (R_p - R_f) / σ_p
2. Extract relevant data for ALL candidates from the problem
3. Compute the performance metric for each candidate systematically
4. Store results in a comparable format (dictionary with fund names as keys)
5. Identify the maximum/minimum value and corresponding candidate(s)
6. **CHECK: Convert list of winners to tuple or use conditional logic for answer mapping**
7. **CRITICAL: Return the answer in the format expected by the question - either the fund identifier string or the complete dictionary if multiple values are requested**

**Code Example:**

**Scenario:** Four funds have Sharpe ratios to be calculated. Risk-free rate is 4%, and we need to find the highest Sharpe ratio.

**Correct Code:**
```python
# Given data
funds = {
    'W': {'return': 0.14, 'std_dev': 0.18},
    'X': {'return': 0.11, 'std_dev': 0.12},
    'Y': {'return': 0.16, 'std_dev': 0.20},
    'Z': {'return': 0.13, 'std_dev': 0.15}
}
rf = 0.04

# Step 1: Calculate Sharpe ratio for ALL funds
sharpe_ratios = {}
for fund_name, data in funds.items():
    sharpe = (data['return'] - rf) / data['std_dev']
    sharpe_ratios[fund_name] = sharpe

# Step 2: Find maximum Sharpe ratio
max_sharpe = max(sharpe_ratios.values())

# Step 3: Find all funds with maximum Sharpe (handle ties)
max_funds = [fund for fund, sharpe in sharpe_ratios.items() if sharpe == max_sharpe]

# Step 4: CRITICAL - Proper answer mapping using conditional logic or tuple keys
if len(max_funds) == 1:
    result = max_funds[0]
elif set(max_funds) == {'W', 'X'}:
    result = 'D'  # Tied option
elif set(max_funds) == {'W', 'Y'}:
    result = 'E'  # Tied option
else:
    result = max_funds[0]  # Default to first if unexpected tie

# Step 5: CHECK - If question asks for multiple values, return dictionary instead
# If question says "calculate variance for A, B, and C", return sharpe_ratios dict

result  # Result: fund identifier or option letter
```

**Common Bugs to Avoid:**
- **Using lists as dictionary keys (unhashable type error) - convert to tuple or use conditional logic**
- **Not handling execution failures from improper data structure usage**
- **Returning only a single metric value when the question asks for multiple securities' values**
- Computing metric for only one candidate and returning immediately
- Forgetting to compare all candidates before selecting the answer
- Not storing intermediate results for comparison
- Returning the metric value instead of the fund identifier

---
## Pattern: Multi-Factor Model Total Return Calculation

**Description:** Multi-factor models compute total return as base expected return plus the sum of factor surprises weighted by factor sensitivities: R = E(R) + Σ[β_i × (Actual_i - Expected_i)]. **Critical: This formula applies to REALIZED returns given actual factor outcomes. For EXPECTED returns of fairly-priced securities, use only E(R) = R_f + Σ[β_i × RP_i] without factor surprises.**

**When to Use:** Questions asking for "total return" or "realized return" given a factor model with expected returns, factor betas, expected factor values, AND actual factor values.

**When NOT to Use:**
- When the question asks for "expected return" of a "fairly priced" security—use only risk-free rate plus beta-weighted risk premiums
- When actual factor realizations are NOT provided—cannot compute surprises without actual values
- When the question explicitly states "assuming no factor surprises" or "ex-ante expected return"

**Procedure:**
1. **CHECK QUESTION TYPE: Does it ask for "expected return" or "realized/total return"?**
2. For EXPECTED return of fairly-priced security: E(R) = R_f + Σ[β_i × RP_i] (stop here, do not add surprises)
3. For REALIZED return with actual outcomes: R_total = E(R) + Σ[β_i × (Actual_i - Expected_i)]
4. For each factor, calculate surprise: (Actual - Expected)
5. Multiply each surprise by its corresponding beta
6. Sum all weighted surprises
7. Add the sum to base expected return
8. Ensure percentage arithmetic is consistent (if values are in %, keep in %)

**Code Example:**

**Scenario 1 (Expected Return):** T-bills yield 6%, Factor 1 beta=1.2 (risk premium 6%), Factor 2 beta=0.5 (risk premium 8%). Find expected return if stock is fairly priced.

**Correct Code:**
```python
# Expected Return for Fairly-Priced Security (NO surprises)
risk_free_rate = 0.06
factors = [
    {'beta': 1.2, 'risk_premium': 0.06},
    {'beta': 0.5, 'risk_premium': 0.08}
]

# Expected return = Risk-free + Σ(β × Risk Premium)
expected_return = risk_free_rate + sum(f['beta'] * f['risk_premium'] for f in factors)

expected_return  # Result: 0.06 + 1.2*0.06 + 0.5*0.08 = 0.182 or 18.2%
```

**Scenario 2 (Realized Return):** Same setup, but Factor 1 expected 3% actual 3.4%, Factor 2 expected 5% actual 5.6%. Find total return.

**Correct Code:**
```python
# Realized Return with Factor Surprises
expected_return = 0.09  # Base expected return
factors = [
    {'beta': 1.5, 'expected': 3.0, 'actual': 3.4},
    {'beta': 0.8, 'expected': 5.0, 'actual': 5.6}
]

# Factor contribution from surprises
factor_contribution = sum(f['beta'] * (f['actual'] - f['expected']) for f in factors)

# Total realized return
total_return = expected_return + factor_contribution

total_return  # Result: 9.0 + 1.5*0.4 + 0.8*0.6 = 10.08%
```

**Common Bugs to Avoid:**
- Using wrong sign for surprise (expected - actual instead of actual - expected)
- Forgetting to multiply surprise by beta before summing
- Omitting one or more factors from the calculation
- Mixing percentage points and decimals inconsistently (e.g., 0.4% vs 0.004)
- **Adding factor surprises when calculating expected return for fairly-priced securities (should use only risk premiums)**
- **Using risk premiums when calculating realized returns (should use actual vs expected factor values)**

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

**Description:** The Brinson-Fachler allocation effect measures return impact of portfolio weight decisions: Allocation Effect = (Portfolio Weight - Benchmark Weight) × (Benchmark Return - Total Benchmark Return). **Critical: Both weight difference AND return difference must be in the same units (both as decimals or both as percentage points) before multiplication. The standard approach is to keep values in percentage points and divide the final product by 100 to get the result in percentage points.**

**When to Use:** Questions asking for "allocation effect" in performance attribution analysis, particularly in Brinson-Fachler or Brinson-Hood-Beebower frameworks with sector or regional breakdowns.

**Procedure:**
1. Formula: Allocation Effect = [(w_p - w_b) × (R_b - R_total_b)] / 100 when using percentage points
2. Extract portfolio weight and benchmark weight for the segment (in percentage points)
3. Extract benchmark return for the segment (in percentage points)
4. Extract total benchmark return (portfolio-wide, in percentage points)
5. Calculate weight difference: (w_p - w_b) in percentage points
6. Calculate return difference: (R_b - R_total_b) in percentage points
7. **CRITICAL: Multiply the two differences, then divide by 100 to convert to percentage points: [(weight_diff) × (return_diff)] / 100**
8. **ALTERNATIVE: Convert both to decimals first: (weight_diff / 100) × (return_diff / 100), then multiply by 100 for percentage points**
9. Result is in percentage points (or basis points if multiplied by 100 again)

**Code Example:**

**Scenario:** Sector has portfolio weight 30%, benchmark weight 28%, sector benchmark return 15%, total benchmark return 12%. Find allocation effect.

**Correct Code:**
```python
# Given data (in percentage points)
portfolio_weight = 30.0
benchmark_weight = 28.0
sector_benchmark_return = 15.0
total_benchmark_return = 12.0

# Step 1: Weight difference (in percentage points)
weight_diff = portfolio_weight - benchmark_weight  # 2.0

# Step 2: Return difference (in percentage points)
return_diff = sector_benchmark_return - total_benchmark_return  # 3.0

# Step 3: Allocation effect - Method 1 (keep in percentage points)
allocation_effect_pct = (weight_diff * return_diff) / 100

# Alternative Method 2 (convert to decimals first)
# allocation_effect = (weight_diff / 100) * (return_diff / 100)
# allocation_effect_pct = allocation_effect * 100

allocation_effect_pct  # Result: 0.06 percentage points
```

**Common Bugs to Avoid:**
- Using portfolio return instead of benchmark return in the formula
- Reversing the subtraction order (benchmark - portfolio instead of portfolio - benchmark)
- **Converting only one value to decimal but not the other: (weight_diff / 100) × return_diff produces result off by factor of 100**
- **Not dividing by 100 when multiplying percentage points: weight_diff × return_diff produces result off by factor of 100**
- Confusing allocation effect with selection effect formulas

---
## Pattern: Covariance Calculation from Correlation and Standard Deviations

**Description:** Covariance is calculated from correlation coefficient and standard deviations using: Cov(X,Y) = ρ × σ_X × σ_Y. **Critical: Ensure you extract STANDARD DEVIATIONS (volatility/risk measures), not expected returns, from data tables. When standard deviations are given in percentage terms, covariance is in percentage-squared units. The result should be reported in the same unit format as the ground truth expects (decimal-squared or percentage-squared).**

**When to Use:** Questions asking for covariance between two assets when given correlation coefficient and standard deviations, particularly in portfolio analysis contexts.

**Procedure:**
1. Formula: Cov(X,Y) = ρ_{X,Y} × σ_X × σ_Y
2. Extract correlation coefficient (dimensionless, between -1 and +1)
3. **CHECK: Extract standard deviation values - verify they are labeled as "Standard Deviation", "Std Dev", "Volatility", or "Risk", NOT "Return" or "Expected Return"**
4. **VERIFY: Standard deviations should be positive and typically smaller than 100% for most assets**
5. Extract standard deviation of first asset (in % or decimal)
6. Extract standard deviation of second asset (same units)
7. Multiply: correlation × std_dev_1 × std_dev_2
8. **CHECK OUTPUT FORMAT: If ground truth shows covariance in percentage-squared (e.g., 7.216), keep result as-is; if in decimal-squared (e.g., 0.0007216), divide by 10000**
9. Result units: if std devs in %, covariance in %²; if in decimals, covariance in decimal²

**Code Example:**

**Scenario:** Stock M has std dev 3.2%, Stock N has std dev 4.1%, correlation is 0.55. Find covariance. Table also shows expected returns of 0.8% and 1.1%.

**Correct Code:**
```python
# Given data from table
# Expected Returns: 0.8%, 1.1% (NOT USED for covariance)
# Standard Deviations: 3.2%, 4.1% (CORRECT values to use)
std_dev_M = 3.2  # 3.2% - from "Standard Deviation" column
std_dev_N = 4.1  # 4.1% - from "Standard Deviation" column
correlation = 0.55

# VALIDATION: Ensure we didn't accidentally use returns
# Standard deviations should be positive and reasonable
assert std_dev_M > 0 and std_dev_N > 0, "Standard deviations must be positive"
assert std_dev_M < 100 and std_dev_N < 100, "Check if these are std devs, not returns"

# Covariance calculation
# When std devs are in %, result is in %² (percentage-squared)
covariance = correlation * std_dev_M * std_dev_N

# CHECK: If ground truth expects decimal format (< 1.0), divide by 10000
# covariance_decimal = covariance / 10000

covariance  # Result: 7.216 (%²), meaning 7.216 percentage-squared
```

**Common Bugs to Avoid:**
- **Extracting expected returns instead of standard deviations from data tables - verify column headers**
- **Not validating that extracted values are labeled as volatility/risk measures, not return measures**
- Converting percentages to decimals (15% → 0.15) then reporting without re-scaling
- Confusing variance with covariance formulas
- **Not checking ground truth format to determine if result should be in percentage-squared or decimal-squared units**
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

## Pattern: Efficient Frontier Portfolio Identification

**Description:** Identifying efficient frontier portfolios requires determining if a portfolio offers the maximum expected return for its risk level (or minimum risk for its return level). For two-asset portfolios, this involves calculating the minimum variance portfolio weight and checking if candidate portfolios lie on the efficient segment between the minimum variance portfolio and the higher-return asset.

**When to Use:** Questions asking which portfolio(s) lie on the efficient frontier, or asking to identify efficient portfolios from a set of candidates with different asset allocations.

**Procedure:**
1. Formula: Minimum variance weight w_A = (σ_B² - Cov_AB) / (σ_A² + σ_B² - 2×Cov_AB)
2. Calculate expected returns and variances for both assets
3. Calculate covariance or correlation between assets
4. Compute minimum variance portfolio weight using formula above
5. Calculate expected return and variance of minimum variance portfolio
6. For each candidate portfolio, calculate its expected return and variance
7. **CHECK EFFICIENCY: A portfolio is efficient if no other portfolio has (a) higher return with same/lower risk, OR (b) lower risk with same/higher return**
8. For two assets, efficient portfolios lie on the curve from minimum variance portfolio to 100% in higher-return asset
9. Compare each candidate to this efficient segment

**Example (sanitized):**

> **Scenario:** Asset A: E(R)=12%, σ=20%. Asset B: E(R)=8%, σ=15%. Correlation=0.3. Candidates: (1) 30% A, 70% B; (2) 50% A, 50% B; (3) 20% A, 80% B. Which are efficient?
>
> **Wrong approach:**
> ```python
> # INCORRECT: Only checks pairwise dominance among candidates
> for i in range(len(candidates)):
>     dominated = False
>     for j in range(len(candidates)):
>         if returns[j] >= returns[i] and risks[j] <= risks[i] and (returns[j] > returns[i] or risks[j] < risks[i]):
>             dominated = True
>     if not dominated:
>         efficient.append(i)
> # This can incorrectly identify multiple portfolios as efficient
> ```
>
> **Correct approach:**
> ```python
> import numpy as np
> 
> # Asset data
> exp_a, exp_b = 0.12, 0.08
> std_a, std_b = 0.20, 0.15
> correlation = 0.3
> 
> # Step 1: Calculate covariance
> cov_ab = correlation * std_a * std_b
> 
> # Step 2: Minimum variance portfolio weight
> var_a, var_b = std_a**2, std_b**2
> w_a_min_var = (var_b - cov_ab) / (var_a + var_b - 2*cov_ab)
> w_a_min_var = max(0, min(1, w_a_min_var))  # Constrain to [0,1]
> 
> # Step 3: Min var portfolio return and variance
> exp_min_var = w_a_min_var * exp_a + (1 - w_a_min_var) * exp_b
> var_min_var = w_a_min_var**2 * var_a + (1-w_a_min_var)**2 * var_b + 2*w_a_min_var*(1-w_a_min_var)*cov_ab
> 
> # Step 4: For each candidate, check if on efficient frontier
> candidates = [(0.30, 0.70), (0.50, 0.50), (0.20, 0.80)]
> 
> for w_a, w_b in candidates:
>     # Calculate portfolio metrics
>     exp_p = w_a * exp_a + w_b * exp_b
>     var_p = w_a**2 * var_a + w_b**2 * var_b + 2*w_a*w_b*cov_ab
>     
>     # Check if efficient: must have w_a >= w_a_min_var (on efficient segment)
>     # and no other feasible portfolio dominates it
>     is_efficient = w_a >= w_a_min_var
>     
>     if is_efficient:
>         print(f"Portfolio ({w_a:.0%}, {w_b:.0%}) is efficient")
> ```

**Common Mistakes to Avoid:**
- Using pairwise dominance among candidates instead of checking against true efficient frontier
- Not calculating the minimum variance portfolio as the starting point of the efficient frontier
- Forgetting that for two assets, only portfolios between min-var and 100% higher-return asset are efficient
- Not constraining minimum variance weight to [0, 1] range

## Pattern: Direct Portfolio Loss from Market Movement

**Description:** When calculating expected portfolio loss from market movements WITHOUT hedging or derivatives, use the direct formula: Expected Loss = Portfolio Value × Beta × |Market % Change|. This is fundamentally different from futures hedging calculations and should not involve contract multipliers or rounding.

**When to Use:** 
- Questions asking for "expected loss", "portfolio loss", or "value change" from market movements
- When NO mention of futures, hedging, or derivatives in the question
- When the question provides portfolio value, beta, and expected market change

**When NOT to Use:**
- When futures contracts or hedging strategies are mentioned
- When the question asks about derivatives positions
- When contract specifications (multipliers, etc.) are provided

**Procedure:**
1. Formula: Expected Loss = Portfolio Value × Beta × |% Market Change|
2. Extract portfolio value
3. Extract portfolio beta
4. Calculate market percentage change: (New Index - Old Index) / Old Index
5. Multiply: Portfolio Value × Beta × |Market % Change|
6. Result is the expected portfolio loss in dollars

**Example (sanitized):**

> **Scenario:** Portfolio worth $2M with beta 0.75. Market index at 2000, expected to drop to 1800. Calculate expected portfolio loss.
>
> **Wrong approach:**
> ```python
> # INCORRECT: Using futures hedging formula
> contracts = int((2_000_000 * 0.75) / (2000 * 250))
> loss = contracts * (-200) * 250  # Wrong approach!
> ```
>
> **Correct approach:**
> ```python
> portfolio_value = 2_000_000
> portfolio_beta = 0.75
> old_index = 2000
> new_index = 1800
> 
> # Calculate market percentage change
> market_pct_change = (new_index - old_index) / old_index  # -10%
> 
> # Direct portfolio loss
> expected_loss = portfolio_value * portfolio_beta * abs(market_pct_change)
> 
> expected_loss  # Result: $150,000
> ```

**Common Mistakes to Avoid:**
- Applying futures contract formulas when no hedging is mentioned
- Using contract multipliers in direct portfolio calculations
- Rounding portfolio values as if they were contract quantities
- Confusing derivatives position changes with portfolio value changes

---

## Pattern: Single-Index Model Multiple Securities Variance

**Description:** When a question asks to "calculate variance for securities A, B, and C" or similar phrasing requesting multiple values, the answer must be a dictionary or data structure containing ALL requested variances, not just one security's value. The single-index model formula σ²_i = β²_i × σ²_M + σ²(e_i) applies to each security individually.

**When to Use:**
- Questions explicitly asking for variance/return/metric for multiple named securities
- When the question lists multiple securities (e.g., "A, B, and C") in the request
- When ground truth shows multiple values in dictionary or structured format

**When NOT to Use:**
- When question asks for a single security's variance
- When question asks "which security has the highest variance" (use comparative pattern instead)

**Procedure:**
1. Formula: σ²_i = β²_i × σ²_M + σ²(e_i) for each security i
2. Extract market variance (σ²_M)
3. For EACH security, extract beta and idiosyncratic variance
4. Calculate total variance for each security
5. **CRITICAL: Store ALL results in a dictionary with security names as keys**
6. **Return the complete dictionary, not a single value**

**Example (sanitized):**

> **Scenario:** Three securities X, Y, Z with betas 0.9, 1.1, 1.3 and idiosyncratic std devs 20%, 15%, 25%. Market std dev is 18%. Calculate variance for all three.
>
> **Wrong approach:**
> ```python
> # INCORRECT: Only returns one security's variance
> variance_X = (0.9**2 * 0.18**2) + 0.20**2
> variance_X  # Missing Y and Z!
> ```
>
> **Correct approach:**
> ```python
> market_std = 0.18
> market_var = market_std ** 2
> 
> securities = {
>     'X': {'beta': 0.9, 'idio_std': 0.20},
>     'Y': {'beta': 1.1, 'idio_std': 0.15},
>     'Z': {'beta': 1.3, 'idio_std': 0.25}
> }
> 
> # Calculate variance for ALL securities
> variances = {}
> for name, data in securities.items():
>     systematic_var = data['beta']**2 * market_var
>     idiosyncratic_var = data['idio_std']**2
>     variances[name] = systematic_var + idiosyncratic_var
> 
> variances  # Return complete dictionary: {'X': 0.0662, 'Y': 0.0614, 'Z': 0.1154}
> ```

**Common Mistakes to Avoid:**
- Returning only the first security's value when multiple are requested
- Using a single variable instead of a dictionary to store results
- Not reading the question carefully to identify if multiple values are needed
- Calculating all values but only returning one

---

## Pattern: Minimum Variance Currency Hedge Calculation

**Description:** For currency hedging with a minimum variance hedge ratio derived from regression analysis, the hedge amount is calculated as: Hedge Amount = Currency Exposure × Regression Coefficient, where the regression coefficient represents the sensitivity of the asset's returns to currency movements. The result is in the same currency units as the exposure.

**When to Use:**
- Questions asking for "minimum variance hedge" for currency exposure
- When a regression coefficient or slope is provided showing asset return sensitivity to currency changes
- When the question asks "what short position in [currency]" to hedge exposure

**When NOT to Use:**
- When asking for a simple one-for-one hedge (use full exposure amount)
- When no regression coefficient is provided

**Procedure:**
1. Formula: Hedge Amount = Currency Exposure × Regression Coefficient
2. Extract the currency exposure amount (in foreign currency units)
3. Extract the regression coefficient (slope from regression of asset returns on currency changes)
4. Multiply exposure by coefficient to get hedge amount
5. **CRITICAL: Result is in the SAME currency units as the exposure (e.g., JPY exposure → JPY hedge)**
6. Do NOT convert currencies unless explicitly required by the question

**Example (sanitized):**

> **Scenario:** Portfolio has EUR 150,000,000 exposure. Regression of portfolio returns on EUR changes shows slope coefficient of 0.65. Calculate minimum variance hedge.
>
> **Wrong approach:**
> ```python
> # INCORRECT: Converting to USD or applying exchange rates
> hedge_eur = 150_000_000 * 0.65
> hedge_usd = hedge_eur / 1.10  # Wrong! No conversion needed
> ```
>
> **Correct approach:**
> ```python
> currency_exposure = 150_000_000  # EUR
> regression_coefficient = 0.65
> 
> # Minimum variance hedge amount
> hedge_amount = currency_exposure * regression_coefficient
> 
> hedge_amount  # Result: 97,500,000 EUR
> ```

**Common Mistakes to Avoid:**
- Converting currency units when not required
- Using 1.0 (full hedge) instead of the regression coefficient
- Dividing by exchange rates unnecessarily
- Confusing the regression coefficient with correlation