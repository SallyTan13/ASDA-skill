# SKILL PATTERNS: Unit/Currency/Percent Conversion Errors in Financial Calculations

## Pattern: Variance-to-Standard-Deviation Conversion

**Description:** Computing variance correctly but failing to apply the square root transformation to obtain standard deviation, or confusing which measure is requested.

**When to Use:** Questions asking for "standard deviation" or "volatility" when given probability distributions of returns.

**Procedure:**
1. Formula: σ = √[Σ P(i) × (R(i) - E[R])²]
2. Calculate expected return: E[R] = Σ P(i) × R(i)
3. Calculate variance: σ² = Σ P(i) × (R(i) - E[R])²
4. Apply square root to variance to get standard deviation
5. Verify the result is in the same unit scale as the input returns

**Code Example:**

**Scenario:** Calculate standard deviation for a stock with three states: Recession (prob=0.25, return=0.05), Normal (prob=0.50, return=0.12), Boom (prob=0.25, return=0.22)

**Correct Code:**
```python
import math

# State probabilities and returns
probs = [0.25, 0.50, 0.25]
returns = [0.05, 0.12, 0.22]

# Step 1: Calculate expected return
expected_return = sum(p * r for p, r in zip(probs, returns))

# Step 2: Calculate variance
variance = sum(p * (r - expected_return)**2 for p, r in zip(probs, returns))

# Step 3: Calculate standard deviation (MUST take square root)
std_dev = math.sqrt(variance)

# Return as decimal (e.g., 0.0612 for 6.12%)
std_dev
```

**Common Bugs to Avoid:**
- Returning variance instead of standard deviation (missing `math.sqrt()`)
- Forgetting to import `math` module
- Confusing which measure is requested in the question
- Using `**0.5` without parentheses causing order-of-operations errors

---

## Pattern: Percentage-Squared Units for Variance

**Description:** Computing variance in decimal form but failing to convert to percentage-squared units when the question context and answer options indicate percentage format is expected.

**When to Use:** Questions asking for "variance" where returns are given as percentages and answer options show percentage values.

**Procedure:**
1. Formula: σ² = Σ P(i) × (R(i) - E[R])²
2. Determine input format: are returns given as decimals (0.12) or percentages (12%)?
3. Calculate variance using consistent units throughout
4. Convert final result: if inputs were percentages, variance is in %-squared; if inputs were decimals, multiply by 10000 to get %-squared
5. Match the format of answer options (e.g., 66.04% means 66.04 percentage-squared)

**Code Example:**

**Scenario:** Calculate variance for returns given as percentages: State A (prob=0.30, return=15%), State B (prob=0.50, return=10%), State C (prob=0.20, return=8%)

**Correct Code:**
```python
# Returns given as percentages
probs = [0.30, 0.50, 0.20]
returns_pct = [15, 10, 8]  # Keep as percentage values

# Calculate expected return in percentage terms
expected_return_pct = sum(p * r for p, r in zip(probs, returns_pct))

# Calculate variance in percentage-squared units
variance_pct_sq = sum(p * (r - expected_return_pct)**2 for p, r in zip(probs, returns_pct))

# Result is already in %-squared (e.g., 7.8 means 7.8%-squared)
variance_pct_sq
```

**Alternative if returns are decimals:**
```python
# Returns given as decimals
probs = [0.30, 0.50, 0.20]
returns_dec = [0.15, 0.10, 0.08]

expected_return = sum(p * r for p, r in zip(probs, returns_dec))
variance_dec = sum(p * (r - expected_return)**2 for p, r in zip(probs, returns_dec))

# Convert to percentage-squared by multiplying by 10000
variance_pct_sq = variance_dec * 10000

variance_pct_sq
```

**Common Bugs to Avoid:**
- Mixing decimal and percentage representations in the same calculation
- Converting decimal variance (0.000780) to percentage by multiplying by 100 instead of 10000
- Misinterpreting "66.04%" in options as 0.6604 instead of 66.04 percentage-squared units

---

## Pattern: Sharpe Ratio Unit Consistency

**Description:** Computing Sharpe ratio correctly but misinterpreting the result's scale when numerator and denominator are both in percentage units, leading to incorrect conversion or rounding.

**When to Use:** Questions asking for "Sharpe measure," "Sharpe ratio," or similar risk-adjusted performance metrics.

**Procedure:**
1. Formula: Sharpe Ratio = (R_p - R_f) / σ_p
2. Ensure numerator (excess return) and denominator (std dev) use consistent units
3. If both are percentages: (12% - 4%) / 22% = 8/22 = 0.3636 (dimensionless ratio)
4. Convert to percentage format if answer options show percentages: 0.3636 → 36% (not 36.36%)
5. Apply standard rounding conventions based on answer option precision

**Code Example:**

**Scenario:** Portfolio has 18% average return, 25% standard deviation, risk-free rate is 5%. Calculate Sharpe ratio.

**Correct Code:**
```python
# All inputs as percentages (can work with decimals too)
avg_return_pct = 18
risk_free_pct = 5
std_dev_pct = 25

# Calculate Sharpe ratio (dimensionless)
sharpe_ratio = (avg_return_pct - risk_free_pct) / std_dev_pct

# Result is 0.52 (dimensionless)
# If options show percentages, interpret as 52%
sharpe_ratio
```

**Alternative with decimal inputs:**
```python
avg_return = 0.18
risk_free = 0.05
std_dev = 0.25

sharpe_ratio = (avg_return - risk_free) / std_dev

# Result is 0.52, express as 52% if options require
sharpe_ratio
```

**Common Bugs to Avoid:**
- Dividing percentage by percentage and then multiplying by 100 again (double conversion)
- Reporting excessive precision (0.5454545...) instead of rounding to match option format
- Confusing dimensionless ratio (0.52) with percentage (52%) based on context
- Using decimal for one input and percentage for another

---

## Pattern: Information Ratio with Percentage Inputs

**Description:** Mishandling unit conversions when computing information ratio where alpha and residual standard deviation are given in percentage terms, leading to scale errors.

**When to Use:** Questions asking for "information ratio" or "appraisal ratio" with percentage-based inputs.

**Procedure:**
1. Formula: Information Ratio = Alpha / Residual Standard Deviation
2. Extract alpha (excess return vs benchmark) in consistent units
3. Extract residual standard deviation (unsystematic risk) in same units
4. Divide directly if both are in same format (both % or both decimal)
5. Interpret result based on answer options: ratio of 2.80 may be expressed as 280% in some contexts

**Code Example:**

**Scenario:** Fund has 14% average return, market has 10%, fund beta is 1.2, risk-free rate is 3%, residual std dev is 2.5%. Calculate information ratio.

**Correct Code:**
```python
# Calculate alpha (excess return beyond what beta predicts)
fund_return_pct = 14
market_return_pct = 10
risk_free_pct = 3
beta = 1.2
residual_std_pct = 2.5

# Expected return based on CAPM
expected_return_pct = risk_free_pct + beta * (market_return_pct - risk_free_pct)

# Alpha (actual - expected)
alpha_pct = fund_return_pct - expected_return_pct

# Information ratio
info_ratio = alpha_pct / residual_std_pct

# Result is dimensionless ratio (e.g., 1.52)
# May be expressed as 152% in some contexts
info_ratio
```

**Common Bugs to Avoid:**
- Confusing information ratio with Sharpe ratio (using total std dev instead of residual)
- Mixing percentage and decimal units between numerator and denominator
- Misinterpreting whether answer expects ratio (1.52) or percentage (152%)
- Using wrong alpha calculation (simple excess return vs CAPM-based alpha)

---

## Pattern: Portfolio Expected Return Calculation

**Description:** Making arithmetic errors in multi-step weighted average calculations, either in computing portfolio returns within each state or in computing probability-weighted expected values across states.

**When to Use:** Questions asking for "expected return of portfolio" given individual asset returns, portfolio weights, and state probabilities.

**Procedure:**
1. Formula: E[R_p] = Σ P(state) × [Σ w(i) × R(i, state)]
2. For each economic state, calculate portfolio return: R_p(state) = w_A × R_A(state) + w_B × R_B(state) + ...
3. Verify weights sum to 1.0
4. Calculate expected return: E[R_p] = Σ P(state) × R_p(state)
5. Verify probabilities sum to 1.0

**Code Example:**

**Scenario:** Portfolio with 40% in Stock X, 60% in Stock Y. Three states: Recession (prob=0.20, X=5%, Y=8%), Normal (prob=0.60, X=12%, Y=10%), Boom (prob=0.20, X=20%, Y=15%)

**Correct Code:**
```python
# Portfolio weights
weights = {'X': 0.40, 'Y': 0.60}

# State probabilities and returns
states = [
    {'prob': 0.20, 'X': 0.05, 'Y': 0.08},
    {'prob': 0.60, 'X': 0.12, 'Y': 0.10},
    {'prob': 0.20, 'X': 0.20, 'Y': 0.15}
]

# Step 1: Calculate portfolio return in each state
portfolio_returns = []
for state in states:
    port_return = sum(weights[asset] * state[asset] for asset in ['X', 'Y'])
    portfolio_returns.append(port_return)

# Step 2: Calculate expected portfolio return
expected_return = sum(state['prob'] * port_ret 
                     for state, port_ret in zip(states, portfolio_returns))

# Verify weights and probabilities sum to 1.0
assert abs(sum(weights.values()) - 1.0) < 0.001
assert abs(sum(s['prob'] for s in states) - 1.0) < 0.001

expected_return
```

**Common Bugs to Avoid:**
- Computing E[R_A] and E[R_B] separately then weighting (wrong order of operations)
- Arithmetic errors in multiplication or addition of multiple terms
- Using wrong weights or probabilities due to indexing errors
- Not verifying that weights and probabilities sum to 1.0

---

## Pattern: Covariance and Correlation Precision

**Description:** Accumulating rounding errors or using inconsistent precision in multi-step statistical calculations involving means, deviations, products, and square roots.

**When to Use:** Questions asking for "covariance" or "correlation" between two assets given probability distributions.

**Procedure:**
1. Covariance formula: Cov(A,B) = Σ P(i) × (R_A(i) - E[R_A]) × (R_B(i) - E[R_B])
2. Correlation formula: ρ = Cov(A,B) / (σ_A × σ_B)
3. Calculate expected returns without premature rounding
4. Calculate deviations for each state
5. Compute products and weighted sums maintaining full precision
6. Round only the final result to match expected precision (typically 4 decimal places)

**Code Example:**

**Scenario:** Two stocks with three equally likely states: State 1 (A=10%, B=5%), State 2 (A=15%, B=12%), State 3 (A=8%, B=20%)

**Correct Code:**
```python
import math

# Equal probabilities
probs = [1/3, 1/3, 1/3]
returns_A = [0.10, 0.15, 0.08]
returns_B = [0.05, 0.12, 0.20]

# Calculate expected returns (maintain full precision)
E_A = sum(p * r for p, r in zip(probs, returns_A))
E_B = sum(p * r for p, r in zip(probs, returns_B))

# Calculate covariance
covariance = sum(p * (rA - E_A) * (rB - E_B) 
                for p, rA, rB in zip(probs, returns_A, returns_B))

# Calculate standard deviations
var_A = sum(p * (rA - E_A)**2 for p, rA in zip(probs, returns_A))
var_B = sum(p * (rB - E_B)**2 for p, rB in zip(probs, returns_B))
std_A = math.sqrt(var_A)
std_B = math.sqrt(var_B)

# Calculate correlation
correlation = covariance / (std_A * std_B)

# Round final result appropriately (e.g., 4 decimal places)
round(correlation, 4)
```

**Common Bugs to Avoid:**
- Rounding intermediate values (E[R], deviations) too early
- Using sample formulas (n-1) instead of population formulas with probabilities
- Floating-point accumulation errors from inefficient calculation order
- Reporting excessive precision instead of matching expected format
- Forgetting to take square root when computing standard deviations for correlation denominator

---

## Pattern: Comparison and Selection After Metric Calculation

**Description:** Computing performance metrics correctly but failing in the comparison or selection logic, often due to indexing errors or incorrect mapping between calculated values and answer options.

**When to Use:** Questions asking to identify "which fund has the highest/lowest" metric value from multiple options.

**Procedure:**
1. Calculate the metric for all candidates in a structured format (list or dictionary)
2. Use explicit comparison logic (max/min functions with proper key)
3. Map the result back to the correct label/name
4. Verify the mapping with an assertion or print statement during development
5. Return the answer in the format requested (option letter, fund name, etc.)

**Code Example:**

**Scenario:** Calculate Sharpe ratios for three funds and identify the highest. Fund P (return=20%, std=28%, rf=4%), Fund Q (return=16%, std=18%), Fund R (return=14%, std=12%)

**Correct Code:**
```python
# Fund data
funds = {
    'P': {'return': 0.20, 'std': 0.28},
    'Q': {'return': 0.16, 'std': 0.18},
    'R': {'return': 0.14, 'std': 0.12}
}
risk_free = 0.04

# Calculate Sharpe ratio for each fund
sharpe_ratios = {}
for name, data in funds.items():
    sharpe_ratios[name] = (data['return'] - risk_free) / data['std']

# Find fund with maximum Sharpe ratio
best_fund = max(sharpe_ratios, key=sharpe_ratios.get)

# Verify calculation (optional but recommended)
# print(f"Sharpe ratios: {sharpe_ratios}")
# print(f"Best fund: {best_fund} with Sharpe ratio {sharpe_ratios[best_fund]:.4f}")

# Map to answer option if needed
options = {'P': 'A', 'Q': 'B', 'R': 'C'}
answer = options[best_fund]

answer
```

**Common Bugs to Avoid:**
- Using index-based selection (argmax) but mapping wrong index to fund name
- Comparing values but returning wrong identifier
- Off-by-one errors in list indexing
- Not verifying the mapping between calculated values and final answer
- Using `max()` on values but losing track of which fund they belong to

---

## Pattern: Decimal-Percentage Hybrid Calculations

**Description:** Maintaining consistent representation throughout calculations when some inputs are naturally percentages and others are decimals, ensuring correct interpretation of final results.

**When to Use:** Any calculation mixing rates, returns, and ratios where inputs may be given in mixed formats.

**Procedure:**
1. Identify the format of each input (decimal 0.12 vs percentage 12)
2. Standardize all inputs to one format at the beginning
3. Perform all calculations in the standardized format
4. Convert final result to match answer option format
5. Document the format being used with comments

**Code Example:**

**Scenario:** Calculate excess return where portfolio return is "15%" (percentage), risk-free rate is "0.04" (decimal), and answer options show percentages.

**Correct Code:**
```python
# Standardize inputs to decimal format
portfolio_return = 0.15  # Given as 15%, convert to decimal
risk_free_rate = 0.04    # Already in decimal

# Calculate excess return in decimal
excess_return_decimal = portfolio_return - risk_free_rate

# Convert to percentage for answer matching
excess_return_pct = excess_return_decimal * 100

# Result: 11.0 (meaning 11%)
excess_return_pct
```

**Alternative: work in percentage format**
```python
# Standardize inputs to percentage format
portfolio_return_pct = 15    # Given as 15%
risk_free_rate_pct = 4       # Convert 0.04 to 4%

# Calculate in percentage terms
excess_return_pct = portfolio_return_pct - risk_free_rate_pct

# Result: 11 (meaning 11%)
excess_return_pct
```

**Common Bugs to Avoid:**
- Mixing 0.15 and 4% in the same calculation without conversion
- Converting the same value twice (0.15 → 15 → 1500)
- Forgetting which format is being used mid-calculation
- Misinterpreting answer options (is "11" meant as 11% or 0.11?)
- Not documenting unit assumptions in comments