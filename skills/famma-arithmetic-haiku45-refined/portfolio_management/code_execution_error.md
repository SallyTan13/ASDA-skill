# SKILL PATTERNS FOR PORTFOLIO MANAGEMENT (PoT)

## Pattern: Portfolio Variance and Standard Deviation with Explicit Weights

**Description:** Portfolio variance/standard deviation calculations require explicit portfolio weights, which may be stated in the question, implied by context, or require equal-weight assumption only as a last resort. Failing to identify specified weights leads to incorrect calculations despite correct methodology. **CRITICAL: Weight validation must allow for minor rounding differences (±1%) and should not cause execution failures.**

**When to Use:** Questions asking for portfolio variance, standard deviation, or risk metrics when multiple securities are involved. Keywords: "portfolio variance," "standard deviation," "this portfolio," "your portfolio."

**When NOT to Use:** Single-security risk calculations or when weights are irrelevant to the calculation.

**Procedure:**
1. Formula: Portfolio Variance = Σᵢ wᵢ²σᵢ² + ΣᵢΣⱼ(i≠j) wᵢwⱼCov(i,j)
2. **First**, scan question text for explicit weight specifications (e.g., "40% in A, 60% in B")
3. **Second**, check if "this portfolio" refers to previously defined allocations in context
4. **Third**, only assume equal weights if no information is provided and document this assumption
5. Calculate portfolio return in each state: Rₚ = Σ(wᵢ × Rᵢ)
6. Calculate expected portfolio return: E[Rₚ] = Σ(probability × portfolio_return)
7. Calculate variance: Var = Σ(probability × (Rₚ - E[Rₚ])²)
8. Return standard deviation as sqrt(variance) or variance depending on question
9. **Weight validation:** If validating weights sum to 1.0, use tolerance of ±0.02 to accommodate rounding:
   ```python
   assert abs(sum(weights) - 1.0) < 0.02, "Weights should sum to approximately 1.0"
   ```
10. **Do NOT fail execution if weights sum to 0.98-1.02** - this is acceptable rounding variation

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

# Verify weights sum to approximately 1 (allow rounding tolerance)
weight_sum = sum([weight_X, weight_Y, weight_Z])
assert abs(weight_sum - 1.0) < 0.02, f"Weights sum to {weight_sum}, should be ~1.0"

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
- **CRITICAL**: Using strict weight validation (tolerance < 0.01) that fails on valid rounding differences
- Causing execution failure when weights sum to 0.9875 or 1.0125 (acceptable variation)
- Assuming equal weights without checking question context
- Using individual security variances instead of portfolio return variance
- Forgetting to weight returns before calculating portfolio statistics
- Not documenting when equal-weight assumption is made

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

**Description:** The final line of PoT code must be an expression (variable name or calculation) that evaluates to the answer, not a print statement. **For PoT code, always return numerical values (decimals or percentages as appropriate), never option letters.** Additionally, verify the returned variable matches the question target before submission. For multiple-choice questions, option mapping should be done in post-processing, not in the PoT code itself. **CRITICAL: Assertions must use soft bounds that accommodate valid edge cases, including zero values for perfectly hedged portfolios.**

**When to Use:** All PoT questions. This is a universal pattern for ensuring correct code execution and answer extraction.

**When NOT to Use:** Never skip this pattern - it applies universally, but the specific format requirements vary by question type.

**Procedure:**
1. Assign final calculated result to a descriptive variable (e.g., `portfolio_return`, `correlation_coefficient`)
2. Add sanity check assertions before final return, but **use soft bounds that allow for valid edge cases:**
   - For standard deviations: `assert 0 <= std_dev < 1.0` (allow zero for perfectly hedged portfolios)
   - For correlations: `assert -1.0 <= corr <= 1.0` (allow full range)
   - For returns: `assert -1.0 < return < 3.0` (very wide bounds)
   - **Never use strict lower bounds like `0 <` that exclude zero**
3. **Determine answer format from question:**
   - If numerical with "%" in options: return as percentage (multiply by 100)
   - If numerical as decimal: return as decimal (0.0X format)
   - **CRITICAL**: For multiple-choice, return numerical value, NOT option letter
4. **Final line must be the variable name alone** (not print, not assignment)
5. Verify the variable being returned answers the specific question asked
6. **For questions asking multiple values** (e.g., "expected return and standard deviation"):
   - Return tuple: `(expected_return, std_dev)`
   - Ensure order matches question order
   - Document which value is which: `# Returns: (expected_return, std_dev)`

**Common Mistakes to Avoid:**
- **CRITICAL**: Using strict lower bounds like `assert 0 < value` that exclude zero (valid for perfectly hedged portfolios)
- Using overly strict assertions (e.g., `< 0.05` for equity returns) that cause valid calculations to fail
- Returning decimal (0.1032) when percentage (10.32) is expected, or vice versa
- Returning option letter ('B') instead of numerical value in PoT code
- Adding validation that rejects the correct answer due to format mismatch with options
- Not checking whether ground truth expects percentage or decimal representation
- For multi-value questions, returning only one value or returning in wrong order
- Performing option matching inside PoT code (should be post-processing)

**Example (sanitized):**

> **Scenario:** Calculate portfolio standard deviation for a hedged portfolio that may have zero variance.

> **Wrong approach:** 
> ```python
> portfolio_std_dev = 0.0  # Perfectly hedged portfolio
> 
> # WRONG: Strict lower bound excludes valid zero value
> assert 0 < portfolio_std_dev < 1.0, "Std dev outside range"
> 
> portfolio_std_dev  # Code fails on assertion
> ```

> **Correct approach:**
> ```python
> portfolio_std_dev = 0.0  # Perfectly hedged portfolio
> 
> # CORRECT: Allow zero for perfectly hedged portfolios
> assert 0 <= portfolio_std_dev < 1.0, "Std dev outside valid range"
> 
> portfolio_std_dev  # Returns 0.0 successfully
> ```

---
## Pattern: Table Data Extraction and Column Mapping

**Description:** When extracting data from OCR'd tables, carefully map column headers to variable names, verify alignment between securities mentioned in question and table columns, and validate extracted values are reasonable. **CRITICAL: Extract numerical values EXACTLY as shown in OCR output without semantic interpretation or sign modification based on context clues like state names (e.g., "Bust", "Recession").**

**When to Use:** Questions with tabular data in images, especially when OCR quality may be imperfect. Keywords: "based on the table," "exhibit shows," "following chart."

**When NOT to Use:** When data is provided directly in text format without tables.

**Procedure:**
1. Read table structure: identify row labels (states/scenarios) and column headers (securities)
2. **Critical**: Map question references (e.g., "Security 2") to correct table columns
3. **STRICT OCR DATA RULE**: Extract values row-by-row EXACTLY as OCR shows them:
   - If OCR shows ".50" or "0.50", use positive 0.50
   - If OCR shows "-.50" or "-0.50", use negative -0.50
   - **DO NOT modify signs** based on state names ("Bust", "Bear", "Recession")
   - **DO NOT apply semantic interpretation** (e.g., assuming "Bust" means negative)
4. Add assertion to verify no data transformation occurred:
   ```python
   # Verify OCR values used exactly as extracted
   # Stock C Bust return: OCR shows ".50" → using 0.50 (not -0.50)
   ```
5. Validate extracted data with **soft bounds**: 
   - Check probabilities sum to ~1.0 (tolerance ±0.01)
   - Check returns are reasonable (-100% to +200% for equities)
   - **Do not use overly strict ranges** like (-50% to +100%)
6. Use descriptive variable names that match question terminology
7. Add comment documenting column mapping (e.g., # Security 2 = column 3)

**Example (sanitized):**

> **Scenario:** Table shows returns for three funds across economic states including "Recession" and "Boom". OCR extracts Fund X Recession return as "0.08" (positive 8%).

> **Wrong approach:**
> ```python
> # OCR shows Fund X Recession return: "0.08"
> # WRONG: Modifying based on semantic interpretation
> returns_X = [0.12, -0.08, 0.15]  # Changed to -0.08 because "Recession" sounds negative
> ```

> **Correct approach:**
> ```python
> # OCR shows Fund X Recession return: "0.08"
> # CORRECT: Use exactly as shown, no semantic modification
> returns_X = [0.12, 0.08, 0.15]  # Using +0.08 as OCR shows
> 
> # Document OCR extraction
> # Fund X Recession: OCR shows "0.08" → using 0.08 (positive)
> # State names do not determine sign - only OCR values matter
> 
> # Soft validation
> assert all(-1.0 < r < 3.0 for r in returns_X), "Returns outside reasonable range"
> ```

**Common Mistakes to Avoid:**
- **CRITICAL**: Modifying signs based on state names ("Bust" → negative, "Boom" → positive)
- Applying semantic interpretation to override OCR values
- Off-by-one errors in column indexing (Security 2 might be column 2 or 3)
- Swapping rows and columns when extracting data
- Using strict validation bounds (e.g., `assert all(-0.5 < r < 1.0)`) that reject valid data
- Not validating probabilities sum to 1.0
- Using generic names (x, y) instead of descriptive names matching question
- Ignoring OCR errors (e.g., "0.O5" instead of "0.05")

---
## Pattern: Multiple-Choice Answer Mapping and Validation

**Description:** After computing numerical result, explicitly map it to the closest option and return the option letter. Use reasonable tolerance for matching (typically 5-10% relative error for financial calculations), but do not fail if no perfect match exists - always return the closest option. **CRITICAL: For Information Ratio and similar performance metrics, use the standard benchmark-based formula, not risk-free rate substitutions.**

**When to Use:** Multiple-choice questions where answer must be A/B/C/D/E. Keywords: "Options:", "which of the following," "closest to."

**When NOT to Use:** Questions asking for numerical values without multiple choice options.

**Procedure:**
1. Compute numerical result using standard calculation
2. **For Information Ratio specifically:** Use formula IR = (Portfolio Return - Benchmark Return) / Tracking Error
   - **Do NOT substitute risk-free rate for benchmark return**
   - Benchmark is typically the market portfolio or stated comparison index
3. Extract option values from choices (parse strings like "A. 0.474")
4. Calculate absolute difference between result and each option
5. Identify closest option by minimum difference
6. **Return the option letter** (not the numerical value)
7. Add comment showing mapping: # Result 0.0474 → closest to Option A (0.474)
8. **Do not assert strict error bounds** - if the question provides options, one must be selected even if none are very close

**Common Mistakes to Avoid:**
- **CRITICAL**: Confusing Information Ratio (uses benchmark) with Sharpe Ratio (uses risk-free rate)
- Using risk-free rate instead of benchmark return in Information Ratio calculations
- Returning numerical value instead of option letter for MC questions
- Using assertions that cause code to fail when no option is within arbitrary threshold
- Not handling percentage vs decimal mismatch (0.05 vs 5%) when comparing to options
- Failing to return an answer when the closest option has >5% error (still return it)
- Stating one option in explanation but returning different option in code

**Example (sanitized):**

> **Scenario:** Calculate Information Ratio for a fund with 15% return vs benchmark 10% return, tracking error 3%.

> **Wrong approach:**
> ```python
> portfolio_return = 0.15
> risk_free_rate = 0.02
> tracking_error = 0.03
> 
> # WRONG: Using risk-free rate instead of benchmark
> information_ratio = (portfolio_return - risk_free_rate) / tracking_error
> # = 0.13 / 0.03 = 4.33 (incorrect)
> ```

> **Correct approach:**
> ```python
> portfolio_return = 0.15
> benchmark_return = 0.10  # Market portfolio return
> tracking_error = 0.03
> 
> # CORRECT: Information Ratio uses benchmark, not risk-free rate
> information_ratio = (portfolio_return - benchmark_return) / tracking_error
> # = 0.05 / 0.03 = 1.67 (correct)
> 
> options = {'A': 1.53, 'B': 1.67, 'C': 2.10}
> closest = min(options.items(), key=lambda x: abs(x[1] - information_ratio))
> closest[0]  # Returns 'B'
> ```

---
## Pattern: Answer Format Detection and Conversion

**Description:** Financial calculations can be expressed as decimals (0.1032) or percentages (10.32%), and the expected format must be inferred from the question, ground truth format, or answer options. Mismatched formats cause scoring failures even when calculations are correct. **CRITICAL: For questions requesting multiple values, preserve the detailed output structure that may be expected by the scoring system.**

**When to Use:** All numerical answer questions, especially when:
- Options show "%" symbols or values > 1 for returns/rates
- Question asks for "percentage" or shows example answers with "%"
- Ground truth comparison fails despite correct calculation
- Question asks for multiple related values (e.g., "variance of A, B, and C")

**When NOT to Use:** When output format is unambiguous or explicitly specified.

**Procedure:**
1. Calculate the numerical result in decimal form (standard practice)
2. **Inspect answer options or question format:**
   - If options contain "%" or values like "10.32" for a 10% return → convert to percentage
   - If options are decimals like "0.1032" → keep as decimal
   - If no options given, check if question says "percentage" or "decimal"
3. **Apply conversion if needed:**
   - To percentage: `result * 100`
   - To decimal: keep as-is or `result / 100` if input was percentage
4. **For questions asking multiple values:**
   - Check if ground truth expects simple tuple or detailed dictionary structure
   - If question asks "calculate variance of A, B, and C" → may need dictionary with keys 'A', 'B', 'C'
   - If baseline provides detailed breakdown (systematic/unsystematic components) → preserve this structure
   - Return format: `{'A': value_A, 'B': value_B, 'C': value_C}` or more detailed nested structure
5. For multiple-choice, compare in the same units as options
6. Return in the format that matches expected output

**Common Mistakes to Avoid:**
- Calculating correctly but returning 0.1032 when 10.32 is expected
- Not checking whether options are in percentage or decimal format
- Assuming all financial returns should be percentages (some contexts use decimals)
- Converting twice (e.g., input is 10%, convert to 0.10, then multiply by 100 again)
- **CRITICAL**: Simplifying output structure when detailed breakdown is expected (e.g., removing systematic/unsystematic variance components)
- Returning single values when multiple values are requested
- Using inconsistent keys or structure compared to what scoring system expects

**Example (sanitized):**

> **Scenario:** Calculate variance for three securities A, B, C using single-index model.

> **Wrong approach:**
> ```python
> variance_A = 0.0881
> variance_B = 0.0500
> variance_C = 0.0976
> 
> # WRONG: Oversimplified output when detailed structure expected
> result = {'A': variance_A, 'B': variance_B, 'C': variance_C}
> result
> ```

> **Correct approach:**
> ```python
> # Calculate components for each security
> result = {}
> for security in ['A', 'B', 'C']:
>     systematic_var = beta[security]**2 * market_variance
>     unsystematic_var = idiosyncratic_std[security]**2
>     total_var = systematic_var + unsystematic_var
>     
>     result[security] = {
>         'systematic_variance': systematic_var,
>         'unsystematic_variance': unsystematic_var,
>         'total_variance': total_var,
>         'standard_deviation': total_var ** 0.5
>     }
> 
> result  # Detailed structure preserves all components
> ```
## Pattern: OCR Ambiguity Resolution with Robust Error Handling

**Description:** When OCR produces ambiguous values (e.g., missing data, unclear digits), test candidate interpretations by calculating results for each and comparing against answer options. Requires robust error handling to prevent execution failures when disambiguation or option matching fails.

**When to Use:** Questions where OCR output has missing values, unclear digits (8 vs 9), or formatting ambiguities that affect calculations. Must have answer options available for validation. Keywords: "based on the table," when OCR quality is poor or values are partially illegible.

**When NOT to Use:** When OCR values are clear and unambiguous, or when no answer options are provided for validation.

**Procedure:**
1. Identify ambiguous OCR values (e.g., missing cell, "8%" vs "9%" unclear)
2. Generate 2-3 plausible candidate interpretations based on:
   - Similar-looking digits (8/9, 5/6, 1/7)
   - Reasonable value ranges for the context
   - Pattern consistency with other table values
3. **For each candidate:**
   - Perform complete calculation
   - Store result with candidate identifier
4. **Validation and selection:**
   - Extract numerical values from answer options
   - Calculate distance from each candidate result to each option
   - Select candidate with minimum distance to any option
5. **CHECK: Verify disambiguation succeeded:**
   ```python
   assert best_match is not None, "OCR disambiguation failed - no candidate matches options"
   assert min_distance < threshold, f"Closest match distance {min_distance} exceeds threshold"
   ```
6. **Return numerical result** (expected_return, std_dev, etc.), NOT option letter
7. **Fallback**: If all candidates fail validation, document ambiguity and return best-effort result with warning comment

**Example (sanitized):**

> **Scenario:** Portfolio calculation where Stock B's return in State 3 is unclear (OCR shows "8%" or "9%"). Options for expected return: A. 11.2%, B. 11.8%, C. 12.3%

> **Wrong approach:**
> ```python
> # Test two candidates
> candidates = [0.08, 0.09]
> results = []
> for candidate in candidates:
>     returns_B = [0.15, 0.10, candidate, 0.05]
>     expected_return = calculate_portfolio_return(returns_B)
>     results.append(expected_return)
> 
> # WRONG: No validation that match exists
> options = {'A': 0.112, 'B': 0.118, 'C': 0.123}
> closest = min(options.items(), key=lambda x: abs(x[1] - results[0]))
> selected_option = closest[0]  # May be None if no match
> 
> selected_option  # FAILS: returning option letter instead of numerical value
> ```

> **Correct approach:**
> ```python
> # Test two candidates for ambiguous OCR value
> candidates = {'8%': 0.08, '9%': 0.09}
> results = {}
> 
> for label, candidate in candidates.items():
>     returns_B = [0.15, 0.10, candidate, 0.05]
>     portfolio_return = calculate_portfolio_return(returns_B)
>     results[label] = portfolio_return
> 
> # Extract option values for comparison
> options = {'A': 0.112, 'B': 0.118, 'C': 0.123}
> option_values = list(options.values())
> 
> # Find candidate with minimum distance to any option
> best_candidate = None
> min_distance = float('inf')
> 
> for label, result in results.items():
>     distance = min(abs(result - opt) for opt in option_values)
>     if distance < min_distance:
>         min_distance = distance
>         best_candidate = label
>         best_result = result
> 
> # CHECK: Verify disambiguation succeeded
> assert best_candidate is not None, "OCR disambiguation failed"
> assert min_distance < 0.01, f"Closest match distance {min_distance} too large"
> 
> # Document resolution
> # OCR ambiguity resolved: Stock B State 3 = {best_candidate} (distance: {min_distance:.4f})
> 
> # Return numerical result, not option letter
> expected_return = best_result
> expected_return  # Returns 0.118 (numerical value)
> ```

**Common Mistakes to Avoid:**
- Returning option letter (e.g., 'B') instead of numerical result in PoT code
- Not validating that disambiguation succeeded before proceeding
- Failing to handle case where no candidate matches options within tolerance
- Using first candidate by default without comparing all candidates to options
- Not documenting which candidate was selected and why
- Raising exceptions that halt execution instead of returning best-effort result
- Testing too many candidates (>3) which indicates OCR quality too poor for reliable resolution

---

## Pattern: EWMA Volatility and Covariance Updates

**Description:** The Exponentially Weighted Moving Average (EWMA) model updates volatility and covariance estimates using squared returns and variances, not absolute values or standard deviations. The correct formula works with variance (σ²), not standard deviation (σ), and uses squared returns (u²), not absolute returns (|u|).

**When to Use:** Questions involving EWMA model for updating volatility, variance, or correlation estimates. Keywords: "EWMA model," "exponentially weighted," "update volatility," "update correlation," "λ parameter."

**When NOT to Use:** Simple historical volatility calculations, GARCH models (different formula), or static correlation calculations.

**Procedure:**
1. **CRITICAL FORMULAS:**
   - Variance update: `σₙ² = λ × σₙ₋₁² + (1-λ) × uₙ₋₁²`
   - Covariance update: `Covₙ = λ × Covₙ₋₁ + (1-λ) × uₓ,ₙ₋₁ × uᵧ,ₙ₋₁`
   - Where u represents returns (not absolute values, not standard deviations)
2. Calculate daily returns: `u = (Price_today - Price_yesterday) / Price_yesterday`
3. **For volatility updates:**
   - Start with variance (σ²), not standard deviation (σ)
   - Square the return: `u²`
   - Update variance using formula above
   - Convert to standard deviation at the end: `σ = √(σ²)`
4. **For covariance updates:**
   - Calculate yesterday's covariance from correlation: `Cov = ρ × σₓ × σᵧ`
   - Use actual returns (positive or negative), not absolute values
   - Update covariance using formula above
5. **For correlation updates:**
   - Update both variances and covariance
   - Calculate new correlation: `ρ = Cov / (σₓ × σᵧ)`
6. Verify correlation is in valid range: `assert -1.0 <= ρ <= 1.0`

**Common Mistakes to Avoid:**
- **CRITICAL**: Using `σₙ = λ × σₙ₋₁ + (1-λ) × |uₙ₋₁|` (wrong - uses standard deviation and absolute value)
- Working with standard deviations instead of variances in the update formula
- Taking absolute value of returns instead of squaring them
- Forgetting to convert back to standard deviation after updating variance
- Using the wrong formula for covariance (must use product of returns, not squared returns)

**Example (sanitized):**

> **Scenario:** Stock volatility yesterday was 2% (daily), price dropped from $100 to $98 today. Update volatility using EWMA with λ=0.94.

> **Wrong approach:**
> ```python
> sigma_yesterday = 0.02
> return_today = (98 - 100) / 100  # -0.02
> lambda_param = 0.94
> 
> # WRONG: Using standard deviation and absolute value
> sigma_today = lambda_param * sigma_yesterday + (1 - lambda_param) * abs(return_today)
> # = 0.94 * 0.02 + 0.06 * 0.02 = 0.02 (incorrect)
> ```

> **Correct approach:**
> ```python
> sigma_yesterday = 0.02
> return_today = (98 - 100) / 100  # -0.02
> lambda_param = 0.94
> 
> # CORRECT: Work with variance and squared returns
> variance_yesterday = sigma_yesterday ** 2  # 0.0004
> return_squared = return_today ** 2  # 0.0004
> 
> # Update variance using EWMA formula
> variance_today = lambda_param * variance_yesterday + (1 - lambda_param) * return_squared
> # = 0.94 * 0.0004 + 0.06 * 0.0004 = 0.0004
> 
> # Convert back to standard deviation
> sigma_today = variance_today ** 0.5  # 0.02
> 
> sigma_today
> ```

---