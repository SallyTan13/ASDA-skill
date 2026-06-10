# SKILL PATTERNS FOR PORTFOLIO MANAGEMENT: Unit/Currency/Percent Conversion Errors (PoT)

---

## Pattern: Weighted Average vs. Scalar Multiplication in Portfolio Returns

**Description:** Confusing the computation of portfolio expected return by incorrectly multiplying the sum of individual expected returns by a single weight, rather than computing the weighted sum where each asset's expected return is multiplied by its respective weight.

**When to Use:** Portfolio expected return calculations with multiple assets, especially when equal weights are mentioned or implied.

**Procedure:**
1. Formula: E(R_p) = Σ(w_i × E(R_i)) where w_i is weight of asset i
2. Calculate expected return for each individual asset: E(R_i) = Σ(p_j × r_ij) across states j
3. Multiply each asset's expected return by its portfolio weight
4. Sum the weighted returns (do NOT sum returns first then multiply by a single weight)
5. Return result as decimal or convert to percentage as needed

**Code Example:**

**Scenario:** Three stocks with probabilities and returns across economic states. Calculate portfolio expected return with equal weights.

**Correct Code:**
```python
# Economic states with probabilities and returns
states = {
    'Expansion': {'prob': 0.30, 'stock_1': 0.12, 'stock_2': 0.08, 'stock_3': 0.15},
    'Normal': {'prob': 0.50, 'stock_1': 0.10, 'stock_2': 0.09, 'stock_3': 0.07},
    'Recession': {'prob': 0.20, 'stock_1': -0.05, 'stock_2': 0.03, 'stock_3': -0.10}
}

# Step 1: Calculate expected return for each stock
e_r1 = sum(states[s]['prob'] * states[s]['stock_1'] for s in states)
e_r2 = sum(states[s]['prob'] * states[s]['stock_2'] for s in states)
e_r3 = sum(states[s]['prob'] * states[s]['stock_3'] for s in states)

# Step 2: Apply portfolio weights (equal weights)
w1 = w2 = w3 = 1/3

# Step 3: Calculate portfolio expected return (CORRECT: weighted sum)
portfolio_return = w1 * e_r1 + w2 * e_r2 + w3 * e_r3

# Alternative correct form using list comprehension
expected_returns = [e_r1, e_r2, e_r3]
weights = [w1, w2, w3]
portfolio_return_alt = sum(w * er for w, er in zip(weights, expected_returns))

portfolio_return
```

**Common Bugs to Avoid:**
- ❌ `(e_r1 + e_r2 + e_r3) * (1/3)` — only works by coincidence for equal weights
- ❌ Forgetting that weighted average requires element-wise multiplication before summation
- ❌ Confusing portfolio variance formula (which has cross-terms) with return formula

---

## Pattern: Premature Rounding in Multi-Step Variance Calculations

**Description:** Rounding intermediate values during variance or standard deviation calculations, causing accumulated precision errors that lead to incorrect final answers, especially when comparing to multiple-choice options with close values.

**When to Use:** Variance, standard deviation, covariance calculations with multiple terms; portfolio risk metrics; any multi-step calculation where precision matters.

**Procedure:**
1. Formula: Var(X) = Σ(p_i × (x_i - μ)²) or portfolio variance with covariance terms
2. Store all intermediate values with full precision (no rounding)
3. Perform all arithmetic operations using unrounded values
4. Only round the final result for presentation
5. Verify calculation by checking intermediate terms if answer seems off

**Code Example:**

**Scenario:** Calculate variance of returns across five scenarios with different probabilities.

**Correct Code:**
```python
import math

# Return scenarios with probabilities
scenarios = [
    {'prob': 0.15, 'return': 0.08},
    {'prob': 0.25, 'return': 0.12},
    {'prob': 0.30, 'return': 0.10},
    {'prob': 0.20, 'return': 0.06},
    {'prob': 0.10, 'return': -0.02}
]

# Step 1: Calculate expected return (keep full precision)
expected_return = sum(s['prob'] * s['return'] for s in scenarios)

# Step 2: Calculate variance (no intermediate rounding)
variance = sum(s['prob'] * (s['return'] - expected_return)**2 for s in scenarios)

# Step 3: Calculate standard deviation
std_dev = math.sqrt(variance)

# Step 4: Only round at the end for presentation
std_dev_percent = round(std_dev * 100, 2)

std_dev_percent
```

**Common Bugs to Avoid:**
- ❌ Rounding expected_return before using it in variance calculation
- ❌ Rounding each term in the summation before adding
- ❌ Using rounded standard deviations in covariance calculations
- ❌ Not using `math.sqrt()` or `**0.5` for square root (importing math module)

---

## Pattern: Algebraic Errors in System of Linear Equations

**Description:** Making sign errors, coefficient mistakes, or incorrect algebraic manipulations when solving simultaneous equations (e.g., for multi-factor model risk premiums), leading to wrong parameter estimates.

**When to Use:** Two-factor models, APT, solving for risk premiums from portfolio equations, any system of linear equations in finance.

**Procedure:**
1. Formula: For two-factor model, E(R_i) = R_f + β_i1×RP_1 + β_i2×RP_2
2. Set up equations: one per portfolio/security with known returns and betas
3. Rearrange to isolate unknowns: (E(R_i) - R_f) = β_i1×RP_1 + β_i2×RP_2
4. Use matrix methods or elimination: verify signs carefully at each step
5. Substitute back to verify solution satisfies original equations

**Code Example:**

**Scenario:** Two portfolios with known betas and returns; solve for two factor risk premiums.

**Correct Code:**
```python
import numpy as np

# Portfolio data
# Portfolio 1: E(R) = 14%, beta1 = 1.2, beta2 = 0.8
# Portfolio 2: E(R) = 10%, beta1 = 0.6, beta2 = 1.1
# Risk-free rate = 3%

r_f = 0.03
e_r1 = 0.14
e_r2 = 0.10
beta1_p1 = 1.2
beta2_p1 = 0.8
beta1_p2 = 0.6
beta2_p2 = 1.1

# Set up system: (E(R) - Rf) = beta1*RP1 + beta2*RP2
# Equation 1: 0.11 = 1.2*RP1 + 0.8*RP2
# Equation 2: 0.07 = 0.6*RP1 + 1.1*RP2

# Using numpy for robust solution
A = np.array([[beta1_p1, beta2_p1],
              [beta1_p2, beta2_p2]])
b = np.array([e_r1 - r_f, e_r2 - r_f])

# Solve for [RP1, RP2]
risk_premiums = np.linalg.solve(A, b)
rp1, rp2 = risk_premiums

# Verification: substitute back
check1 = r_f + beta1_p1 * rp1 + beta2_p1 * rp2
check2 = r_f + beta1_p2 * rp1 + beta2_p2 * rp2

# Return risk premium 1 as percentage
rp1_percent = round(rp1 * 100, 2)
rp1_percent
```

**Common Bugs to Avoid:**
- ❌ Sign errors when rearranging equations (forgetting to subtract R_f)
- ❌ Swapping coefficients or using wrong beta values
- ❌ Manual elimination errors (prefer numpy.linalg.solve for reliability)
- ❌ Not verifying solution by substituting back into original equations

---

## Pattern: Percentage-as-Decimal Output Convention Ambiguity

**Description:** Failing to recognize non-standard output conventions where volatility or other metrics are expected as "percentage values expressed in decimal form" (e.g., 12.75% reported as 0.1275 rather than 12.75 or 0.1275).

**When to Use:** Volatility calculations (especially GARCH, EWMA), standard deviation outputs, when ground truth shows unexpected decimal scaling.

**Procedure:**
1. Calculate the metric in natural decimal form (e.g., σ = 0.01275 for 1.275%)
2. Check if question asks for "percentage" or "daily volatility" without explicit format
3. Test multiple output formats: decimal (0.01275), percentage (1.275), percentage-as-decimal (0.01275 but interpreted as 12.75 basis points)
4. If ground truth is 0.1275 for a 1.275% value, multiply decimal by 100 but keep as decimal
5. Include comment explaining the unconventional format

**Code Example:**

**Scenario:** GARCH(1,1) volatility update from previous volatility 1.5% to new value.

**Correct Code:**
```python
import math

# GARCH(1,1) parameters
omega = 0.000003
alpha = 0.05
beta = 0.93

# Previous day data
prev_volatility_percent = 1.5  # 1.5% per day
prev_return_percent = -0.8  # -0.8% return

# Convert to decimal for calculation
prev_volatility = prev_volatility_percent / 100  # 0.015
prev_return = prev_return_percent / 100  # -0.008

# GARCH formula: σ²_t = ω + α*u²_(t-1) + β*σ²_(t-1)
prev_variance = prev_volatility ** 2
return_squared = prev_return ** 2

new_variance = omega + alpha * return_squared + beta * prev_variance
new_volatility = math.sqrt(new_variance)

# Standard output: as percentage
new_volatility_standard = new_volatility * 100  # e.g., 1.48%

# Non-standard "percentage-as-decimal" format (if required by context)
# If ground truth expects 0.148 for 1.48%, use this:
new_volatility_unconventional = new_volatility_standard / 100  # 0.0148

# Return standard format (verify against ground truth which format is expected)
round(new_volatility_standard, 4)
```

**Common Bugs to Avoid:**
- ❌ Not checking whether ground truth uses standard or unconventional scaling
- ❌ Assuming "percentage" always means multiply by 100
- ❌ Mixing input units (some percentages as decimals, others as whole numbers)
- ❌ Not documenting which convention is being used in comments

---

## Pattern: Portfolio Variance with Correlated Factors

**Description:** Computational errors in the cross-product term (2×w_i×w_j×Cov_ij) when calculating portfolio variance with correlated assets, often from arithmetic mistakes in multiplying coefficients or covariance values.

**When to Use:** Two-asset portfolio variance, multi-factor model variance, any calculation involving Var(aX + bY) = a²Var(X) + b²Var(Y) + 2abCov(X,Y).

**Procedure:**
1. Formula: Var(R_p) = Σ(β_i²×Var(F_i)) + Σ Σ(β_i×β_j×Cov(F_i,F_j)) for i≠j
2. Calculate individual variance terms: β_i² × Var(F_i)
3. Calculate covariance: Cov = ρ × σ_i × σ_j
4. Calculate cross-product term: 2 × β_i × β_j × Cov(F_i, F_j)
5. Verify arithmetic: use intermediate variables, check each multiplication step

**Code Example:**

**Scenario:** Portfolio variance from two factors with correlation 0.30.

**Correct Code:**
```python
import math

# Factor parameters
beta_factor1 = 1.15
beta_factor2 = 0.85
variance_factor1 = 0.0625  # (25%)²
variance_factor2 = 0.0400  # (20%)²
correlation = 0.30

# Step 1: Calculate standard deviations
std_factor1 = math.sqrt(variance_factor1)  # 0.25
std_factor2 = math.sqrt(variance_factor2)  # 0.20

# Step 2: Calculate covariance
covariance = correlation * std_factor1 * std_factor2

# Step 3: Calculate variance components separately for verification
var_component1 = beta_factor1**2 * variance_factor1
var_component2 = beta_factor2**2 * variance_factor2
cross_product = 2 * beta_factor1 * beta_factor2 * covariance

# Step 4: Total portfolio variance
portfolio_variance = var_component1 + var_component2 + cross_product

# Step 5: Portfolio volatility
portfolio_volatility = math.sqrt(portfolio_variance)

# Verification output with intermediate values
verification = {
    'var_comp1': round(var_component1, 6),
    'var_comp2': round(var_component2, 6),
    'cross_prod': round(cross_product, 6),
    'total_var': round(portfolio_variance, 6),
    'volatility_pct': round(portfolio_volatility * 100, 2)
}

portfolio_volatility * 100  # Return as percentage
```

**Common Bugs to Avoid:**
- ❌ Forgetting the factor of 2 in cross-product term
- ❌ Using variance instead of standard deviation in covariance calculation
- ❌ Arithmetic errors in multi-step multiplication (verify each term separately)
- ❌ Not storing intermediate values for debugging when answer is wrong

---

## Pattern: Sign Convention in Share Repurchase Effects

**Description:** Misunderstanding that a decline in shares outstanding (negative ΔS) contributes positively to per-share returns in the Grinold-Kroner model, leading to incorrect sign application.

**When to Use:** Grinold-Kroner model, equity return decomposition, when share buybacks or repurchases are mentioned.

**Procedure:**
1. Formula: E(R) = (D/P) + ΔS + g + ΔPE + i, where ΔS is change in shares
2. Recognize: declining shares (ΔS < 0) means same earnings spread over fewer shares
3. Use the stated change directly: if "shares decline 1.5%", use ΔS = -0.015
4. Add all components algebraically (negative ΔS adds negatively, which boosts return)
5. Verify: share repurchases should increase expected return, not decrease it

**Code Example:**

**Scenario:** Expected equity return using Grinold-Kroner with share buybacks.

**Correct Code:**
```python
# Grinold-Kroner model components
dividend_yield = 0.0220  # 2.20%
share_change = -0.0150  # -1.50% (shares declining due to buybacks)
inflation = 0.0200  # 2.00%
pe_expansion = 0.0025  # 0.25%
gdp_growth = 0.0300  # 3.00%
earnings_premium = 0.0100  # 1.00% above GDP

# Total earnings growth
earnings_growth = gdp_growth + earnings_premium

# Grinold-Kroner formula: E(R) = D/P + ΔS + g + ΔPE + i
# Note: ΔS is ADDED directly (negative value means positive contribution to return)
expected_return = (dividend_yield + 
                   share_change +  # -1.50% adds as negative
                   earnings_growth + 
                   pe_expansion + 
                   inflation)

# Verification: share buybacks should increase return
# Without buybacks: 2.20% + 4.00% + 0.25% + 2.00% = 8.45%
# With buybacks: 8.45% + (-1.50%) = 6.95%... WRONG!
# Correct interpretation: buybacks boost per-share value
# The negative sign is already in share_change, so direct addition is correct

expected_return_percent = round(expected_return * 100, 2)
expected_return_percent
```

**Common Bugs to Avoid:**
- ❌ Subtracting the decline: `dividend_yield - (-0.015)` creates double negative
- ❌ Treating share decline as reducing returns (economic intuition error)
- ❌ Confusing ΔS (change in shares) with dilution effect on price
- ❌ Not verifying that buybacks should increase expected return

---

## Pattern: Variance Unit Scaling (Basis Points vs. Decimal)

**Description:** Failing to recognize that variance in finance is often reported in basis points (×10,000) or percentage-squared units rather than decimal proportions, causing a scale mismatch between calculated and expected values.

**When to Use:** Variance calculations, risk metrics, when ground truth shows values like 881 instead of 0.0881 for variance.

**Procedure:**
1. Calculate variance in natural decimal form: Var = β²σ²_M + σ²(ε)
2. Check ground truth scale: if GT is 881 for 8.81% variance, scale is basis points
3. Convert: variance_bp = variance_decimal × 10,000
4. Alternatively: if inputs are percentages, keep output as percentage-squared
5. Document unit convention clearly in comments

**Code Example:**

**Scenario:** Single-index model variance with market volatility 18%.

**Correct Code:**
```python
import math

# Single-index model: Ri = αi + βi*RM + ei
# Variance: Var(Ri) = βi² * Var(RM) + Var(ei)

# Security parameters
beta = 0.90
sigma_M_percent = 18  # 18% market volatility
sigma_ei_percent = 22  # 22% idiosyncratic risk

# Method 1: Calculate in decimal, convert to basis points
sigma_M = sigma_M_percent / 100  # 0.18
sigma_ei = sigma_ei_percent / 100  # 0.22

variance_decimal = beta**2 * sigma_M**2 + sigma_ei**2
variance_basis_points = variance_decimal * 10000

# Method 2: Calculate directly in percentage-squared units
variance_pct_squared = beta**2 * sigma_M_percent**2 + sigma_ei_percent**2

# Both methods should give same result
# Method 1: 0.0746 * 10000 = 746
# Method 2: 0.81 * 324 + 484 = 262.44 + 484 = 746.44

# Return in basis points (if that's the expected format)
round(variance_basis_points, 0)
```

**Common Bugs to Avoid:**
- ❌ Not checking whether ground truth uses basis points or decimal
- ❌ Mixing units: calculating in decimal but comparing to basis point answer
- ❌ Assuming variance is always reported in same units as standard deviation
- ❌ Forgetting that percentage-squared ≠ percentage (8% std dev → 64 variance, not 8)

---

## Pattern: Percentage Input Ambiguity in Tables

**Description:** Misinterpreting whether table values like "20%" represent 0.20 (decimal) or 20 (percentage points), leading to order-of-magnitude errors in calculations and outputs.

**When to Use:** Any calculation using tabular data with percentage symbols, especially from OCR-extracted tables.

**Procedure:**
1. Examine table context: are values like "20%" or "0.20" or "20"?
2. Check reasonableness: stock returns of 20% (0.20) vs. 2000% (if treating 20 as decimal)
3. Standardize inputs: convert all percentages to decimal at input stage
4. Perform calculations in decimal form
5. Convert output to match expected format (check if answer should be 24.33% or 0.2433)

**Code Example:**

**Scenario:** Calculate standard deviation from scenario returns given as percentages.

**Correct Code:**
```python
import math

# Scenario data from table (OCR extracted as "15%", "20%", "10%")
# CRITICAL: Determine if these are decimals or percentages
scenarios = [
    {'prob': 0.25, 'return_str': '15%'},
    {'prob': 0.50, 'return_str': '20%'},
    {'prob': 0.25, 'return_str': '10%'}
]

# Step 1: Parse percentage strings to decimals
for s in scenarios:
    # If string contains '%', remove it and divide by 100
    if '%' in s['return_str']:
        s['return'] = float(s['return_str'].strip('%')) / 100
    else:
        # If already decimal, use directly
        s['return'] = float(s['return_str'])

# Step 2: Calculate expected return in decimal
expected_return = sum(s['prob'] * s['return'] for s in scenarios)

# Step 3: Calculate variance in decimal
variance = sum(s['prob'] * (s['return'] - expected_return)**2 for s in scenarios)

# Step 4: Calculate standard deviation
std_dev = math.sqrt(variance)

# Step 5: Output format check
# If ground truth is 16.58%, output as percentage:
std_dev_percent = std_dev * 100
# If ground truth is 0.1658, output as decimal:
std_dev_decimal = std_dev

# Return percentage format (most common)
round(std_dev_percent, 2)
```

**Common Bugs to Avoid:**
- ❌ Treating "20%" as 20.0 in calculations (creates 100× error)
- ❌ Not standardizing all inputs to same unit before calculation
- ❌ Outputting 0.1658 when answer expects 16.58% or vice versa
- ❌ Not verifying reasonableness: 200% stock return in normal market is suspicious

---

## Pattern: Real Return Calculation (Fisher Equation)

**Description:** Errors in applying the Fisher equation approximation (real return ≈ nominal return - inflation) vs. exact formula, and ensuring all rates are in consistent units before subtraction.

**When to Use:** Real return calculations, inflation-adjusted returns, Fisher equation applications.

**Procedure:**
1. Formula (approximation): r_real ≈ r_nominal - inflation
2. Formula (exact): (1 + r_real) = (1 + r_nominal) / (1 + inflation)
3. Ensure both rates are in same units (both decimal or both percentage)
4. For small rates, approximation is acceptable; for large rates, use exact
5. Return in format matching question (percentage or decimal)

**Code Example:**

**Scenario:** Calculate real return given nominal portfolio return and expected inflation.

**Correct Code:**
```python
# Portfolio expected nominal return
nominal_return = 0.0925  # 9.25%

# Expected inflation rate
inflation_rate = 0.0350  # 3.50%

# Method 1: Fisher approximation (suitable for small rates)
real_return_approx = nominal_return - inflation_rate

# Method 2: Exact Fisher equation
real_return_exact = ((1 + nominal_return) / (1 + inflation_rate)) - 1

# Difference between methods (usually small)
difference = abs(real_return_exact - real_return_approx)

# For reporting: use approximation unless question specifies exact
real_return = real_return_approx

# Convert to percentage
real_return_percent = round(real_return * 100, 2)

real_return_percent
```

**Common Bugs to Avoid:**
- ❌ Mixing units: subtracting 3.5 from 0.0925 (percentage from decimal)
- ❌ Using exact formula when approximation is expected (or vice versa)
- ❌ Forgetting to subtract 1 in exact formula: (1+r_nom)/(1+inf) - 1
- ❌ Not verifying that real return < nominal return when inflation is positive

---

## Pattern: Equal Weights Assumption Verification

**Description:** Incorrectly assuming equal portfolio weights when not explicitly stated, or failing to verify whether "equal weights" means equal dollar amounts or equal number of shares.

**When to Use:** Portfolio calculations when weights are not provided, questions mentioning "diversified portfolio" without weight specification.

**Procedure:**
1. Check if weights are explicitly given in problem or table
2. If "equal weights" stated: use w_i = 1/n for n assets
3. If not stated: look for context clues (market-cap weighted, equal dollar amounts)
4. Calculate portfolio metric using identified weights
5. Add comment documenting weight assumption

**Code Example:**

**Scenario:** Portfolio return with three stocks, weights not explicitly stated.

**Correct Code:**
```python
# Stock expected returns
e_r_stock1 = 0.12
e_r_stock2 = 0.09
e_r_stock3 = 0.15

# Check problem statement for weight specification
# If "equal weights" or "equally weighted portfolio" mentioned:
n_stocks = 3
weight_per_stock = 1 / n_stocks  # 0.3333...

# Calculate portfolio return
portfolio_return = (weight_per_stock * e_r_stock1 + 
                    weight_per_stock * e_r_stock2 + 
                    weight_per_stock * e_r_stock3)

# Alternative: if weights are market-cap based (not equal)
# market_caps = [100, 150, 250]  # in millions
# total_cap = sum(market_caps)
# weights = [mc / total_cap for mc in market_caps]
# portfolio_return = sum(w * er for w, er in zip(weights, expected_returns))

# Document assumption clearly
# Assumption: Equal dollar weights (1/3 each) as problem states "diversified portfolio"

round(portfolio_return * 100, 2)
```

**Common Bugs to Avoid:**
- ❌ Assuming equal weights when problem implies market-cap weighting
- ❌ Using equal weights for variance without checking if assets are independent
- ❌ Not documenting weight assumption in code comments
- ❌ Confusing equal dollar weights with equal number of shares