# DETAILED SKILL PATTERNS FOR EQUITY CALCULATIONS (Program of Thought)

---

## Pattern: Probability-Weighted Variance and Standard Deviation

**Description:** When calculating variance and standard deviation for discrete probability distributions of returns, ensure correct extraction of data from tables and proper application of the probability-weighted variance formula: Var = Σ[P(i) × (R(i) - E(R))²].

**When to Use:** Questions asking for standard deviation, variance, or volatility of stock returns given probability distributions across economic states (recession, normal, boom, etc.).

**Procedure:**
1. **Formula:** 
   - Expected Return: E(R) = Σ[P(i) × R(i)]
   - Variance: Var(R) = Σ[P(i) × (R(i) - E(R))²]
   - Standard Deviation: σ = √Var(R)
2. Extract probabilities and returns for the correct stock/asset from the table
3. Calculate expected return first as a separate variable
4. Calculate variance using probability-weighted squared deviations
5. Take square root of variance for standard deviation
6. Verify: sum of probabilities = 1.0, standard deviation > 0

**Code Example:**

**Scenario:** Calculate standard deviation for a stock with returns: 15% (prob 0.25), 10% (prob 0.50), 5% (prob 0.25)

**Correct Code:**
```python
import math

# Data extraction - verify correct column/row
probabilities = [0.25, 0.50, 0.25]
returns = [0.15, 0.10, 0.05]

# Step 1: Calculate expected return
expected_return = sum(p * r for p, r in zip(probabilities, returns))

# Step 2: Calculate variance using probability weights
variance = sum(p * (r - expected_return)**2 for p, r in zip(probabilities, returns))

# Step 3: Calculate standard deviation
std_dev = math.sqrt(variance)

# Verification check
assert abs(sum(probabilities) - 1.0) < 0.001, "Probabilities must sum to 1"

# Return as decimal (convert to percentage in explanation if needed)
std_dev
```

**Common Bugs to Avoid:**
- Extracting data from wrong column (Stock A vs Stock B)
- Using unweighted variance formula (dividing by n instead of using probabilities)
- Forgetting to take square root of variance
- Inconsistency between code output and manual calculation in explanation
- Not verifying that probabilities sum to 1.0

---

## Pattern: Correlation Coefficient from Probability Distributions

**Description:** When computing correlation between two stocks with discrete probability distributions, apply the formula: ρ = Cov(A,B) / (σ_A × σ_B), ensuring consistent use of probability weights throughout all calculations.

**When to Use:** Questions asking for correlation, covariance, or relationship between returns of two stocks across different economic states.

**Procedure:**
1. **Formula:**
   - Covariance: Cov(A,B) = Σ[P(i) × (R_A(i) - E(R_A)) × (R_B(i) - E(R_B))]
   - Correlation: ρ = Cov(A,B) / (σ_A × σ_B)
2. Calculate expected returns for both stocks separately
3. Calculate standard deviations for both stocks
4. Calculate covariance using probability-weighted cross-products of deviations
5. Divide covariance by product of standard deviations
6. Verify: -1 ≤ ρ ≤ 1

**Code Example:**

**Scenario:** Two stocks with returns in 3 states (equal probability 1/3 each): Stock X [0.08, 0.12, 0.16], Stock Y [0.20, 0.10, 0.05]

**Correct Code:**
```python
import numpy as np

# Data extraction
probabilities = np.array([1/3, 1/3, 1/3])
returns_x = np.array([0.08, 0.12, 0.16])
returns_y = np.array([0.20, 0.10, 0.05])

# Step 1: Expected returns
exp_return_x = np.sum(probabilities * returns_x)
exp_return_y = np.sum(probabilities * returns_y)

# Step 2: Standard deviations
variance_x = np.sum(probabilities * (returns_x - exp_return_x)**2)
variance_y = np.sum(probabilities * (returns_y - exp_return_y)**2)
std_dev_x = np.sqrt(variance_x)
std_dev_y = np.sqrt(variance_y)

# Step 3: Covariance
covariance_xy = np.sum(probabilities * (returns_x - exp_return_x) * (returns_y - exp_return_y))

# Step 4: Correlation
correlation = covariance_xy / (std_dev_x * std_dev_y)

# Verification
assert -1.0 <= correlation <= 1.0, "Correlation must be between -1 and 1"

# Return final result
correlation
```

**Common Bugs to Avoid:**
- Using sample correlation formula (n-1 denominator) instead of probability-weighted formula
- Calculating covariance without probability weights
- Numerical precision issues causing discrepancies between code output and explanation
- Not validating that correlation is within [-1, 1] range
- Mixing up which stock is X vs Y when extracting data

---

## Pattern: Expected Return Calculation with Verification

**Description:** When calculating expected return from probability distributions, implement the weighted sum formula correctly and include verification that intermediate calculations match the final output to catch transcription or variable assignment errors.

**When to Use:** Questions asking for expected return, mean return, or average return given probabilities and returns across different states.

**Procedure:**
1. **Formula:** E(R) = Σ[P(i) × R(i)]
2. Extract probabilities and returns from table/data
3. Calculate weighted products for each state
4. Sum all weighted products
5. Verify: manually check at least one intermediate calculation
6. Ensure code output matches explanation

**Code Example:**

**Scenario:** Calculate expected return for states: Growth (prob 0.40, return 0.15), Stable (prob 0.35, return 0.08), Decline (prob 0.25, return -0.02)

**Correct Code:**
```python
# Data extraction with clear variable names
states = ['Growth', 'Stable', 'Decline']
probabilities = [0.40, 0.35, 0.25]
returns = [0.15, 0.08, -0.02]

# Calculate weighted returns for each state (for verification)
weighted_returns = [p * r for p, r in zip(probabilities, returns)]

# Calculate expected return
expected_return = sum(weighted_returns)

# Verification: check probabilities sum to 1
prob_sum = sum(probabilities)
assert abs(prob_sum - 1.0) < 0.001, f"Probabilities sum to {prob_sum}, not 1.0"

# Verification: print intermediate values for debugging (optional)
# for state, p, r, wr in zip(states, probabilities, returns, weighted_returns):
#     print(f"{state}: {p} × {r} = {wr}")

# Return result as expression (not print)
expected_return
```

**Common Bugs to Avoid:**
- Inconsistency between code variables and explanation values
- Transcription errors when manually writing out intermediate calculations
- Using wrong column from table (confusing different stocks/assets)
- Not verifying that probabilities sum to 1.0
- Using print() instead of returning expression on last line

---

## Pattern: Answer Validation Against Multiple Choice Options

**Description:** When computed results don't closely match any provided multiple choice option (difference > 1-2%), this signals a calculation error requiring investigation rather than selecting the nearest option.

**When to Use:** Multiple choice questions where your calculated answer differs significantly from all options, especially for standard deviation, variance, or correlation calculations.

**Procedure:**
1. Calculate the result using correct formula
2. Compare result to all provided options
3. If minimum difference > 2%, investigate potential errors:
   - Data extraction from wrong row/column
   - Using sample vs population formula
   - Unit conversion issues (decimal vs percentage)
   - Formula implementation bugs
4. Recalculate with verified data and formula
5. Only select nearest option if difference < 2%

**Code Example:**

**Scenario:** Calculated standard deviation is 0.0591 (5.91%), but options are [6.91%, 7.25%, 7.79%, 8.13%, 8.85%]

**Correct Code:**
```python
import math

# Initial calculation
probabilities = [0.30, 0.50, 0.20]
returns = [0.18, 0.12, 0.05]

expected_return = sum(p * r for p, r in zip(probabilities, returns))
variance = sum(p * (r - expected_return)**2 for p, r in zip(probabilities, returns))
std_dev = math.sqrt(variance)
std_dev_pct = std_dev * 100

# Validation against options
options = [6.91, 7.25, 7.79, 8.13, 8.85]
min_diff = min(abs(std_dev_pct - opt) for opt in options)

# If difference > 2%, investigate
if min_diff > 2.0:
    # Check: Are we using the right formula?
    # Check: Did we extract data correctly?
    # Check: Should returns be in different units?
    
    # Re-verify calculation step by step
    print(f"Expected return: {expected_return}")
    print(f"Variance: {variance}")
    print(f"Std dev: {std_dev_pct}%")
    print(f"Closest option: {min(options, key=lambda x: abs(x - std_dev_pct))}%")
    print(f"Difference: {min_diff}%")
    
    # STOP and debug rather than proceeding

# Return result only if validated
std_dev
```

**Common Bugs to Avoid:**
- Selecting nearest option without investigating large discrepancies
- Assuming calculation is correct when it differs significantly from all options
- Not checking if data was extracted from correct table row/column
- Ignoring unit conversion issues (0.0691 vs 6.91%)
- Proceeding with answer despite failed validation checks

---

## Pattern: Numerical Consistency Between Code and Explanation

**Description:** Ensure the numerical output from executed code exactly matches the values cited in the written explanation. Discrepancies indicate variable errors, execution issues, or manual calculation mistakes.

**When to Use:** All PoT questions where you provide both executable code and a narrative explanation with numerical results.

**Procedure:**
1. Execute code and capture output value
2. Store output in clearly named variable
3. Reference this exact variable in explanation
4. If manually computing intermediate steps, verify against code variables
5. Include assertion checks for critical values

**Code Example:**

**Scenario:** Calculate portfolio return with two assets

**Correct Code:**
```python
# Asset allocation and returns
weight_a = 0.60
weight_b = 0.40
return_a = 0.12
return_b = 0.08

# Calculate portfolio return
portfolio_return = weight_a * return_a + weight_b * return_b

# Verification: weights sum to 1
assert abs(weight_a + weight_b - 1.0) < 0.001, "Weights must sum to 1"

# Store intermediate calculations for explanation
contribution_a = weight_a * return_a
contribution_b = weight_b * return_b

# Verification: intermediate values match final result
assert abs(contribution_a + contribution_b - portfolio_return) < 1e-10

# Return final result (this value MUST match explanation)
portfolio_return
```

**Explanation template:**
```
The portfolio return is {portfolio_return:.4f} or {portfolio_return*100:.2f}%

Calculation:
- Asset A contribution: {weight_a} × {return_a} = {contribution_a}
- Asset B contribution: {weight_b} × {return_b} = {contribution_b}
- Total: {portfolio_return}
```

**Common Bugs to Avoid:**
- Code outputs 0.11305 but explanation says 0.11165
- Manually recomputing values in explanation instead of using code output
- Rounding intermediate values differently in code vs explanation
- Not using f-strings or format() to ensure explanation uses actual code variables
- Executing code multiple times with different values without updating explanation