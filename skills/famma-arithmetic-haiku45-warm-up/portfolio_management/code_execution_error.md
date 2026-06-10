# SKILL PATTERNS FOR PORTFOLIO MANAGEMENT (PoT)

## Pattern: Portfolio Variance and Standard Deviation with Explicit Weights

**Description:** Portfolio variance/standard deviation calculations require explicit portfolio weights, which may be stated in the question, implied by context, or require equal-weight assumption only as a last resort. Failing to identify specified weights leads to incorrect calculations despite correct methodology.

**When to Use:** Questions asking for portfolio variance, standard deviation, or risk metrics when multiple securities are involved. Keywords: "portfolio variance," "standard deviation," "this portfolio," "your portfolio."

**Procedure:**
1. Formula: Portfolio Variance = Σᵢ wᵢ²σᵢ² + ΣᵢΣⱼ(i≠j) wᵢwⱼCov(i,j)
2. **First**, scan question text for explicit weight specifications (e.g., "40% in A, 60% in B")
3. **Second**, check if "this portfolio" refers to previously defined allocations in context
4. **Third**, only assume equal weights if no information is provided and document this assumption
5. Calculate portfolio return in each state: Rₚ = Σ(wᵢ × Rᵢ)
6. Calculate expected portfolio return: E[Rₚ] = Σ(probability × portfolio_return)
7. Calculate variance: Var = Σ(probability × (Rₚ - E[Rₚ])²)
8. Return standard deviation as sqrt(variance) or variance depending on question

**Code Example:**

**Scenario:** Three stocks with returns in 3 states. Portfolio: 30% Stock X, 50% Stock Y, 20% Stock Z. Calculate portfolio standard deviation.

**Correct Code:**
```python
import numpy as np

# State probabilities and returns
probabilities = [0.3, 0.5, 0.2]
returns_X = [0.12, 0.08, -0.02]
returns_Y = [0.15, 0.10, 0.05]
returns_Z = [0.20, 0.12, -0.05]

# CRITICAL: Extract weights from question (not assumed)
weight_X = 0.30
weight_Y = 0.50
weight_Z = 0.20

# Verify weights sum to 1
assert abs(sum([weight_X, weight_Y, weight_Z]) - 1.0) < 1e-10, "Weights must sum to 1"

# Calculate portfolio return in each state
portfolio_returns = [
    weight_X * returns_X[i] + weight_Y * returns_Y[i] + weight_Z * returns_Z[i]
    for i in range(len(probabilities))
]

# Expected portfolio return
expected_return = sum(p * r for p, r in zip(probabilities, portfolio_returns))

# Portfolio variance
variance = sum(
    probabilities[i] * (portfolio_returns[i] - expected_return)**2
    for i in range(len(probabilities))
)

# Standard deviation
std_dev = np.sqrt(variance)

std_dev  # Return as expression, not print
```

**Common Bugs to Avoid:**
- Assuming equal weights without checking question context
- Using individual security variances instead of portfolio return variance
- Forgetting to weight returns before calculating portfolio statistics
- Not verifying weights sum to 1.0

---

## Pattern: Covariance and Correlation Calculation from Probability Distributions

**Description:** Covariance requires calculating deviations from expected returns for each security in each state, then probability-weighting the product of deviations. Correlation normalizes by standard deviations.

**When to Use:** Questions asking for covariance or correlation between securities given state-contingent returns. Keywords: "covariance between," "correlation coefficient," "relationship between returns."

**Procedure:**
1. Formula: Cov(X,Y) = Σ[P(s) × (Rₓ(s) - E[Rₓ]) × (Rᵧ(s) - E[Rᵧ])]
2. Formula: Corr(X,Y) = Cov(X,Y) / (σₓ × σᵧ)
3. Calculate expected return for each security: E[R] = Σ(probability × return)
4. Calculate deviations from expected return for each state
5. Calculate covariance as probability-weighted sum of deviation products
6. For correlation, calculate standard deviations and divide covariance by their product
7. Return the final metric (covariance or correlation) as a decimal

**Code Example:**

**Scenario:** Two securities with returns in 4 states. Calculate correlation coefficient.

**Correct Code:**
```python
import numpy as np

# State probabilities and returns
probabilities = [0.25, 0.30, 0.25, 0.20]
returns_M = [0.10, 0.15, 0.08, -0.03]
returns_N = [0.12, 0.09, 0.11, 0.05]

# Step 1: Expected returns
expected_M = sum(p * r for p, r in zip(probabilities, returns_M))
expected_N = sum(p * r for p, r in zip(probabilities, returns_N))

# Step 2: Deviations from expected returns
deviations_M = [r - expected_M for r in returns_M]
deviations_N = [r - expected_N for r in returns_N]

# Step 3: Covariance
covariance = sum(
    probabilities[i] * deviations_M[i] * deviations_N[i]
    for i in range(len(probabilities))
)

# Step 4: Standard deviations (for correlation)
variance_M = sum(p * dev**2 for p, dev in zip(probabilities, deviations_M))
variance_N = sum(p * dev**2 for p, dev in zip(probabilities, deviations_N))
std_M = np.sqrt(variance_M)
std_N = np.sqrt(variance_N)

# Step 5: Correlation coefficient
correlation = covariance / (std_M * std_N)

correlation  # Return value, not print
```

**Common Bugs to Avoid:**
- Forgetting to subtract expected returns when calculating deviations
- Using simple averages instead of probability-weighted expected returns
- Dividing by N instead of using probability weights
- Returning intermediate values (like covariance when correlation is asked)

---

## Pattern: Multi-Factor Model Return Attribution

**Description:** Factor models calculate expected/actual returns as risk-free rate plus sum of (beta × factor risk premium) or (beta × factor surprise). Requires careful extraction of betas, expected values, and actual values from tables.

**When to Use:** Questions involving factor models (Fama-French, APT, custom factors) asking for total return, unexpected return, or factor contributions. Keywords: "factor model," "total return," "beta," "risk premium," "factor surprise."

**Procedure:**
1. Formula: R = Rբ + Σ(βᵢ × Factor_Premiumᵢ) or R = E[R] + Σ(βᵢ × Factor_Surpriseᵢ)
2. Extract risk-free rate or expected return from context
3. Extract beta coefficients for each factor from table (careful with OCR errors)
4. Extract factor risk premiums OR calculate factor surprises (actual - expected)
5. Calculate contribution from each factor: βᵢ × (premium or surprise)
6. Sum all contributions to get total return
7. Verify result is reasonable (e.g., within plausible range for equity returns)

**Code Example:**

**Scenario:** Two-factor model with betas [1.2, 0.8], expected return 9%, factor surprises [0.5%, 1.2%]. Calculate total return.

**Correct Code:**
```python
# Factor model parameters
expected_return = 0.09  # 9%

# Factor betas (from table)
beta_factor1 = 1.2
beta_factor2 = 0.8

# Factor surprises (actual - expected)
factor1_expected = 0.03
factor1_actual = 0.035
factor1_surprise = factor1_actual - factor1_expected

factor2_expected = 0.05
factor2_actual = 0.062
factor2_surprise = factor2_actual - factor2_expected

# Calculate unexpected return from each factor
unexpected_return_factor1 = beta_factor1 * factor1_surprise
unexpected_return_factor2 = beta_factor2 * factor2_surprise

# Total unexpected return
total_unexpected_return = unexpected_return_factor1 + unexpected_return_factor2

# Total return = Expected + Unexpected
total_return = expected_return + total_unexpected_return

# Sanity check: verify reasonable magnitude
assert -1.0 < total_return < 2.0, "Return outside reasonable range"

total_return  # Return as decimal (e.g., 0.0954 for 9.54%)
```

**Common Bugs to Avoid:**
- Misreading beta values from OCR'd tables (verify visually if possible)
- Confusing factor risk premiums with factor surprises
- Using percentage values inconsistently (mixing 0.05 and 5%)
- Not extracting the correct columns from multi-column tables

---

## Pattern: Brinson-Fachler Attribution Analysis

**Description:** Allocation effect measures return impact of over/underweighting sectors relative to benchmark, calculated as weight difference times benchmark sector return difference from total benchmark return.

**When to Use:** Performance attribution questions using Brinson-Fachler methodology. Keywords: "allocation effect," "selection effect," "attribution analysis," "sector allocation."

**Procedure:**
1. Formula: Allocation Effect = (Wₚ - Wᵦ) × (Rᵦ,ₛₑctₒᵣ - Rᵦ,tₒtₐₗ)
2. Formula: Selection Effect = Wᵦ × (Rₚ,ₛₑctₒᵣ - Rᵦ,ₛₑctₒᵣ)
3. Extract portfolio weights, benchmark weights, sector returns from table
4. Calculate weight difference for target sector
5. Calculate benchmark sector return minus total benchmark return
6. Multiply weight difference by return difference for allocation effect
7. Verify sign: positive allocation = overweight in outperforming sector

**Code Example:**

**Scenario:** Portfolio 25% in Tech (benchmark 20%), Tech benchmark return 18%, total benchmark return 12%. Calculate allocation effect.

**Correct Code:**
```python
# Sector: Technology
portfolio_weight = 0.25
benchmark_weight = 0.20
sector_benchmark_return = 0.18
total_benchmark_return = 0.12

# Brinson-Fachler Allocation Effect
weight_difference = portfolio_weight - benchmark_weight
return_difference = sector_benchmark_return - total_benchmark_return

allocation_effect = weight_difference * return_difference

# Interpretation check
if allocation_effect > 0:
    interpretation = "Positive: overweight in outperforming sector"
else:
    interpretation = "Negative: overweight in underperforming sector"

allocation_effect  # Return as decimal (e.g., 0.003 for 0.3%)
```

**Common Bugs to Avoid:**
- Using portfolio sector return instead of benchmark sector return in allocation formula
- Confusing allocation effect with selection effect formulas
- Not subtracting total benchmark return from sector benchmark return
- Mixing up weight differences (portfolio - benchmark vs benchmark - portfolio)

---

## Pattern: Black-Scholes-Merton Option Pricing with Dividends

**Description:** BSM formula for dividend-paying assets requires adjusting spot price by e^(-qT) factor. Put option formula uses N(-d₁) and N(-d₂), not N(d₁) and N(d₂). Sign conventions are critical.

**When to Use:** Option pricing questions with continuous dividend yield. Keywords: "dividend yield," "European option," "put option," "call option," "BSM formula."

**Procedure:**
1. Formula (Call): c = S₀e^(-qT)N(d₁) - Ke^(-rT)N(d₂)
2. Formula (Put): p = Ke^(-rT)N(-d₂) - S₀e^(-qT)N(-d₁)
3. Formula (d₁): [ln(S₀/K) + (r - q + σ²/2)T] / (σ√T)
4. Formula (d₂): d₁ - σ√T
5. Extract S₀, K, r, q, σ, T from problem (convert percentages to decimals)
6. Calculate d₁ and d₂ using natural logarithm
7. Use scipy.stats.norm.cdf() for N(·) calculations
8. **Critical**: For puts, use N(-d₁) and N(-d₂), not N(d₁) and N(d₂)
9. Return option price in same units as S₀

**Code Example:**

**Scenario:** Portfolio worth $500M, wants put protection at 95% level. Index 1500, r=5%, q=2%, σ=25%, T=0.5 years.

**Correct Code:**
```python
import math
from scipy.stats import norm

# Parameters
S0 = 500_000_000  # Portfolio value
protection_level = 0.95
K = S0 * protection_level  # Strike at 95% of current value
r = 0.05  # Risk-free rate
q = 0.02  # Dividend yield
sigma = 0.25  # Volatility
T = 0.5  # Time to maturity (6 months)

# Calculate d1 and d2
d1 = (math.log(S0 / K) + (r - q + sigma**2 / 2) * T) / (sigma * math.sqrt(T))
d2 = d1 - sigma * math.sqrt(T)

# European put option price (CRITICAL: use -d1 and -d2 for puts)
put_price = (
    K * math.exp(-r * T) * norm.cdf(-d2) - 
    S0 * math.exp(-q * T) * norm.cdf(-d1)
)

# Sanity check: put price should be positive and less than K
assert 0 < put_price < K, f"Put price {put_price} outside valid range"

put_price  # Insurance cost
```

**Common Bugs to Avoid:**
- Using N(d₁) instead of N(-d₁) in put formula (sign error)
- Forgetting to adjust spot price by e^(-qT) factor
- Using percentage values without converting to decimals (0.05 not 5)
- Incorrect d₁ formula: forgetting (r - q) adjustment for dividend yield
- Using math.log10 instead of math.log (natural logarithm)

---

## Pattern: Variable Return and Answer Verification

**Description:** The final line of PoT code must be an expression (variable name or calculation) that evaluates to the answer, not a print statement. Additionally, verify the returned variable matches the question target before submission.

**When to Use:** All PoT questions. This is a universal pattern for ensuring correct code execution and answer extraction.

**Procedure:**
1. Assign final calculated result to a descriptive variable (e.g., `portfolio_return`, `correlation_coefficient`)
2. Add sanity check assertions before final return (e.g., range validation)
3. **Final line must be the variable name alone** (not print, not assignment)
4. Verify the variable being returned answers the specific question asked
5. For multiple-choice, optionally add comment mapping value to option letter

**Code Example:**

**Scenario:** Calculate portfolio expected return (should be around 10-12%).

**Correct Code:**
```python
import numpy as np

# Calculations...
weights = [0.4, 0.6]
expected_returns = [0.11, 0.09]

# Calculate portfolio expected return
portfolio_expected_return = sum(w * r for w, r in zip(weights, expected_returns))

# Sanity check: verify reasonable range for equity portfolio
assert 0.0 < portfolio_expected_return < 0.5, \
    f"Expected return {portfolio_expected_return} outside reasonable range"

# CORRECT: Return variable as expression (no print, no assignment)
portfolio_expected_return  # Should be ~0.098 or 9.8%
```

**Wrong Code:**
```python
# WRONG: Using print instead of expression
print(portfolio_expected_return)

# WRONG: Returning wrong variable
variance  # Question asked for return, not variance

# WRONG: Assignment on last line (returns None)
result = portfolio_expected_return
```

**Common Bugs to Avoid:**
- Using `print()` on final line (returns None, not the value)
- Returning intermediate calculation instead of final answer variable
- Returning wrong variable (e.g., variance when standard deviation asked)
- Not adding sanity checks to catch calculation errors before return
- Forgetting to convert units if answer expects percentage vs decimal

---

## Pattern: Table Data Extraction and Column Mapping

**Description:** When extracting data from OCR'd tables, carefully map column headers to variable names, verify alignment between securities mentioned in question and table columns, and validate extracted values are reasonable.

**When to Use:** Questions with tabular data in images, especially when OCR quality may be imperfect. Keywords: "based on the table," "exhibit shows," "following chart."

**Procedure:**
1. Read table structure: identify row labels (states/scenarios) and column headers (securities)
2. **Critical**: Map question references (e.g., "Security 2") to correct table columns
3. Extract values row-by-row, maintaining alignment
4. Validate extracted data: check probabilities sum to 1, returns are reasonable
5. Use descriptive variable names that match question terminology
6. Add comment documenting column mapping (e.g., # Security 2 = column 3)

**Code Example:**

**Scenario:** Table with columns [State, Probability, Security_A, Security_B, Security_C]. Question asks about Security_B and Security_C.

**Correct Code:**
```python
import numpy as np

# Table data extraction
# Columns: State | Probability | Security_A | Security_B | Security_C
probabilities = [0.20, 0.30, 0.35, 0.15]

# CRITICAL: Map question terms to correct columns
# Question asks about "Security B" and "Security C"
# These correspond to columns 3 and 4 in the table
security_B_returns = [0.12, 0.08, 0.10, 0.05]  # Column 3
security_C_returns = [0.15, 0.11, 0.09, 0.07]  # Column 4

# Validation: probabilities should sum to 1
assert abs(sum(probabilities) - 1.0) < 1e-6, \
    f"Probabilities sum to {sum(probabilities)}, not 1.0"

# Validation: returns should be reasonable (between -50% and +100%)
for returns in [security_B_returns, security_C_returns]:
    assert all(-0.5 < r < 1.0 for r in returns), \
        "Returns outside reasonable range"

# Calculate covariance between B and C
expected_B = sum(p * r for p, r in zip(probabilities, security_B_returns))
expected_C = sum(p * r for p, r in zip(probabilities, security_C_returns))

covariance_BC = sum(
    probabilities[i] * 
    (security_B_returns[i] - expected_B) * 
    (security_C_returns[i] - expected_C)
    for i in range(len(probabilities))
)

covariance_BC
```

**Common Bugs to Avoid:**
- Off-by-one errors in column indexing (Security 2 might be column 2 or 3)
- Swapping rows and columns when extracting data
- Not validating probabilities sum to 1.0
- Using generic names (x, y) instead of descriptive names matching question
- Ignoring OCR errors (e.g., "0.O5" instead of "0.05")

---

## Pattern: Multiple-Choice Answer Mapping and Validation

**Description:** After computing numerical result, explicitly map it to the closest option, verify the match is reasonable (not just picking nearest), and ensure the final answer variable contains the option letter, not the numerical value.

**When to Use:** Multiple-choice questions where answer must be A/B/C/D/E. Keywords: "Options:", "which of the following," "closest to."

**Procedure:**
1. Compute numerical result using standard calculation
2. Extract option values from choices (parse strings like "A. 0.474")
3. Calculate absolute difference between result and each option
4. Identify closest option, but verify difference is reasonable (< 1% relative error)
5. **Return the option letter** if question asks for choice, or value if question asks for calculation
6. Add comment showing mapping: # Result 0.0474 → closest to Option A (0.474)

**Code Example:**

**Scenario:** Calculated correlation = 0.5895. Options: A. 0.474, B. 0.590, C. 0.612, D. 0.650

**Correct Code:**
```python
import numpy as np

# ... calculation code ...
calculated_correlation = 0.5895

# Multiple choice options (extracted from question)
options = {
    'A': 0.474,
    'B': 0.590,
    'C': 0.612,
    'D': 0.650
}

# Find closest option
differences = {
    letter: abs(calculated_correlation - value)
    for letter, value in options.items()
}
closest_option = min(differences, key=differences.get)
closest_value = options[closest_option]
min_difference = differences[closest_option]

# Validation: difference should be small (< 5% relative error)
relative_error = min_difference / abs(calculated_correlation)
assert relative_error < 0.05, \
    f"Closest option {closest_option} has {relative_error:.1%} error - too large"

# For multiple choice questions, return the LETTER
# Add comment showing the mapping
closest_option  # Calculated 0.5895 → Option B (0.590), error 0.05%
```

**Common Bugs to Avoid:**
- Returning numerical value instead of option letter for MC questions
- Not validating that closest option is actually close (could indicate calculation error)
- Rounding errors causing wrong option selection (use absolute difference, not rounding)
- Stating one option in explanation but returning different option in code
- Not handling percentage vs decimal mismatch (0.05 vs 5%)