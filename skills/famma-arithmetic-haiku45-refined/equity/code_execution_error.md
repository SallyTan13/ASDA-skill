# DETAILED SKILL PATTERNS FOR EQUITY CALCULATIONS (Program of Thought)

---

## Pattern: Probability-Weighted Variance and Standard Deviation

**Description:** When calculating variance and standard deviation for discrete probability distributions of returns, ensure correct extraction of data from tables, proper application of the probability-weighted variance formula: Var = Σ[P(i) × (R(i) - E(R))²], and correct unit conversion based on the expected answer format (inferred from options or ground truth format when available).

**When to Use:** Questions asking for standard deviation, variance, or volatility of stock returns given probability distributions across economic states (recession, normal, boom, etc.).

**When NOT to Use:** 
- Sample variance calculations (when given historical data points without probabilities)
- Continuous probability distributions requiring integration
- Portfolio variance calculations involving covariance terms
- Price variance calculations (where values are in currency units, not returns)

**Procedure:**
1. **Formula:** 
   - Expected Return: E(R) = Σ[P(i) × R(i)]
   - Variance: Var(R) = Σ[P(i) × (R(i) - E(R))²]
   - Standard Deviation: σ = √Var(R)
2. Extract probabilities and returns for the correct stock/asset from the table
3. Calculate expected return first as a separate variable
4. Calculate variance using probability-weighted squared deviations
5. **Unit Detection (Critical):**
   - Check if question asks for "variance" or "standard deviation"
   - Check if options are provided and examine their format
   - If options contain "%" symbol → answer expected in percentage form
   - If options are decimal numbers (0.04-0.10 range) → answer expected in decimal form
   - If no options provided → default to decimal form for standard deviation
6. **Unit Conversion Based on Detection:**
   - For variance in %²: multiply variance_decimal² by 10,000
   - For std dev in %: multiply std_dev_decimal by 100
   - For decimal form: use raw calculated values
7. Verify: sum of probabilities = 1.0, standard deviation > 0
8. **Match to options WITHOUT strict assertions** - select closest match even if difference is significant

**Worked Example:**
**Question:** Calculate the variance and standard deviation for a stock with the following probability distribution: Bear market (prob 0.20, return 5%), Normal market (prob 0.50, return 12%), Bull market (prob 0.30, return 18%).

```python
import math

# Step 1: Data extraction - returns in decimal form
probabilities = [0.20, 0.50, 0.30]
returns = [0.05, 0.12, 0.18]  # decimal form

# Step 2: Calculate expected return
expected_return = sum(p * r for p, r in zip(probabilities, returns))

# Step 3: Calculate variance (in decimal² units)
variance_decimal_squared = sum(p * (r - expected_return)**2 for p, r in zip(probabilities, returns))

# Step 4: Calculate standard deviation (in decimal units)
std_dev_decimal = math.sqrt(variance_decimal_squared)

# Step 5: Unit detection - check what format is expected
# If question asks for variance and options show percentages (e.g., "66.04%")
# then convert to percentage squared
# If question asks for std dev and no "%" in context, keep decimal form

# For this example, assume variance in %² is requested
variance_percent_squared = variance_decimal_squared * 10000
std_dev_percent = std_dev_decimal * 100

# Verification checks (non-blocking)
prob_sum = sum(probabilities)
if abs(prob_sum - 1.0) >= 0.001:
    print(f"Warning: Probabilities sum to {prob_sum}, not 1.0")

# Return appropriate format based on question
# For variance questions with % options: variance_percent_squared
# For std dev questions without % indicators: std_dev_decimal
variance_percent_squared
```

**Common Bugs to Avoid:**
- **CRITICAL: Unit conversion error** - Multiplying variance by 100 instead of 10,000 when converting from decimal² to %²
- **CRITICAL: Over-converting to percentage** - Converting to percentage when answer is expected in decimal form (check if options contain "%" or are in 0.01-0.10 range)
- **CRITICAL: Strict validation assertions** - Using assert statements that cause code to fail when calculated values don't match options exactly
- Extracting data from wrong column (Stock A vs Stock B)
- Using unweighted variance formula (dividing by n instead of using probabilities)
- Forgetting to take square root of variance
- Inconsistency between code output and manual calculation in explanation
- Confusing variance units (decimal² vs %²) with standard deviation units (decimal vs %)

**CHECK Steps:**
- **Detect expected format:** If options are provided and contain "%" → convert to percentage; if options are decimals (0.01-0.10) → keep decimal form
- If returns are in decimal form (0.10, 0.15), verify variance conversion: variance_%² = variance_decimal² × 10,000
- If returns are already in percentage form (10, 15), variance conversion: variance_%² = variance_% × 1 (no conversion needed)
- Verify: variance in %² should typically be in range [0.01, 1000] for stock returns
- Verify: standard deviation in % should typically be in range [0.1, 50] for stock returns
- Verify: standard deviation in decimal should typically be in range [0.001, 0.50] for stock returns
- **DO NOT use strict assertions** - calculate values and select closest option even if match is imperfect
- If calculated value differs significantly from all options (>10%), document the discrepancy but still return closest match

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

**Description:** When calculating expected return from probability distributions, implement the weighted sum formula correctly and include non-blocking verification that intermediate calculations are reasonable, without using strict assertions that prevent answer selection. Return the calculated value in the appropriate format based on the question context.

**When to Use:** Questions asking for expected return, mean return, or average return given probabilities and returns across different states.

**When NOT to Use:**
- Historical average returns (arithmetic mean without probabilities)
- Geometric mean returns for multi-period calculations
- Risk-adjusted returns (Sharpe ratio, etc.)
- Expected price calculations (use expected value of prices, not returns)

**Procedure:**
1. **Formula:** E(R) = Σ[P(i) × R(i)]
2. Extract probabilities and returns from table/data
3. Calculate weighted products for each state
4. Sum all weighted products
5. **Format Detection:**
   - If options contain "%" symbol → multiply by 100 to convert to percentage
   - If options are decimal numbers → keep in decimal form
   - If no options → return decimal form and let explanation clarify
6. Verify: manually check at least one intermediate calculation
7. **For multiple choice: calculate value, then find closest option** - do NOT return option letter directly from code
8. Ensure code output matches explanation

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

# Verification: check probabilities sum to 1 (non-blocking)
prob_sum = sum(probabilities)
if abs(prob_sum - 1.0) >= 0.001:
    print(f"Warning: Probabilities sum to {prob_sum}, not 1.0")

# Convert to percentage if options indicate percentage format
expected_return_pct = expected_return * 100

# For multiple choice: find closest option in separate step
# DO NOT return option letter from code - return the calculated value
# Let the explanation handle option matching

# Return result as expression (not print)
# Return decimal form - conversion happens in explanation if needed
expected_return
```

**Common Bugs to Avoid:**
- **CRITICAL: Returning option letter instead of calculated value** - Code should return numerical result, not 'A', 'B', 'C'
- **CRITICAL: Strict assertions that prevent answer selection** - Don't use assert statements that cause code failure when values don't match options
- **CRITICAL: Over-converting to percentage** - Only convert if options clearly show percentage format
- Inconsistency between code variables and explanation values
- Transcription errors when manually writing out intermediate calculations
- Using wrong column from table (confusing different stocks/assets)
- Using print() instead of returning expression on last line
- Blocking code execution with validation checks instead of logging warnings

**CHECK Steps:**
- Verify probabilities sum to approximately 1.0 (warn if not, but continue)
- Check that expected return is within reasonable range for stock returns (-50% to +100%)
- **Return numerical value from code** - do NOT return option letters
- **Check if options contain "%"** - if yes, consider converting to percentage in explanation
- Select closest option from available choices in explanation text, not in code
- Document significant discrepancies in explanation, but still return an answer

---
## Pattern: Answer Validation Against Multiple Choice Options

**Description:** When computed results don't closely match any provided multiple choice option, investigate potential errors but ultimately select the closest available option rather than failing to return an answer.

**When to Use:** Multiple choice questions where your calculated answer differs from provided options, especially for standard deviation, variance, or correlation calculations.

**When NOT to Use:**
- Free-response questions without multiple choice options
- Questions where exact numerical precision is required
- Situations where "none of the above" is an explicit option

**Procedure:**
1. Calculate the result using correct formula
2. Compare result to all provided options
3. If minimum difference > 2%, investigate potential errors:
   - Data extraction from wrong row/column
   - Using sample vs population formula
   - Unit conversion issues (decimal vs percentage)
   - Formula implementation bugs
4. If investigation reveals error, recalculate with corrected approach
5. **Always select closest option** - even if difference is large
6. Document discrepancy in explanation if difference > 5%

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

# Validation against options (non-blocking)
options = [6.91, 7.25, 7.79, 8.13, 8.85]
closest_option = min(options, key=lambda x: abs(x - std_dev_pct))
min_diff = abs(std_dev_pct - closest_option)

# Log investigation if difference is large
if min_diff > 2.0:
    print(f"Note: Calculated {std_dev_pct:.2f}% differs from closest option {closest_option}% by {min_diff:.2f}%")
    print("Possible causes: data extraction error, unit conversion, or question error")
    # Continue anyway - don't block execution

# Find option letter corresponding to closest value
option_letters = ['A', 'B', 'C', 'D', 'E']
option_values = options
closest_index = option_values.index(closest_option)
selected_option = option_letters[closest_index]

# Return result - always provide an answer
selected_option
```

**Common Bugs to Avoid:**
- **CRITICAL: Using assertions that prevent answer selection** - Never use assert statements for option matching
- Failing to return an answer when calculated value doesn't match options well
- Not investigating large discrepancies before selecting answer
- Assuming calculation is wrong just because it differs from options (options may have errors)
- Not documenting significant discrepancies in the explanation

**CHECK Steps:**
- Calculate difference between result and each option
- If min difference > 2%, log warning but continue
- If min difference > 10%, double-check data extraction and unit conversion
- **Always select and return closest option** - never fail without an answer
- Document methodology and any discrepancies in explanation text

---
## Pattern: Numerical Consistency Between Code and Explanation

**Description:** Ensure the numerical output from executed code exactly matches the values cited in the written explanation, while avoiding strict assertions that prevent answer selection when values don't match options perfectly.

**When to Use:** All PoT questions where you provide both executable code and a narrative explanation with numerical results.

**When NOT to Use:**
- Questions requiring only conceptual explanations without calculations
- Cases where code is used only for validation, not primary calculation

**Procedure:**
1. Execute code and capture output value
2. Store output in clearly named variable
3. Reference this exact variable in explanation
4. If manually computing intermediate steps, verify against code variables
5. **Use non-blocking checks** for critical values - log warnings instead of assertions

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

# Verification: weights sum to 1 (non-blocking)
weight_sum = weight_a + weight_b
if abs(weight_sum - 1.0) >= 0.001:
    print(f"Warning: Weights sum to {weight_sum}, not 1.0")

# Store intermediate calculations for explanation
contribution_a = weight_a * return_a
contribution_b = weight_b * return_b

# Verification: intermediate values match final result (non-blocking)
calculated_sum = contribution_a + contribution_b
if abs(calculated_sum - portfolio_return) >= 1e-10:
    print(f"Warning: Sum of contributions {calculated_sum} differs from portfolio_return {portfolio_return}")

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
- **CRITICAL: Blocking assertions that prevent answer return** - Use warnings/logging instead of assert
- Code outputs 0.11305 but explanation says 0.11165
- Manually recomputing values in explanation instead of using code output
- Rounding intermediate values differently in code vs explanation
- Not using f-strings or format() to ensure explanation uses actual code variables
- Executing code multiple times with different values without updating explanation

**CHECK Steps:**
- Verify code output variable is referenced in explanation
- Check that intermediate calculations are stored and reused
- **Use conditional warnings** instead of assertions for validation
- Ensure explanation text uses actual code variables via f-strings
- Test that code executes successfully and returns a value (not None or error)

## Pattern: Expected Value of Prices (Non-Return Calculations)

**Description:** When calculating expected value of prices or other non-return variables (currency amounts, units, etc.), use the standard expected value formula E(X) = Σ[P(i) × X(i)] and return the result in the same units as the input values. Do NOT apply return-based unit conversions.

**When to Use:** 
- Questions asking for expected price, expected value, or mean of currency amounts
- Variance of prices (not returns) where values are in dollars, euros, etc.
- Any expected value calculation where the variable is NOT a percentage return

**When NOT to Use:**
- Expected return calculations (use Expected Return pattern)
- Standard deviation of returns (use Probability-Weighted Variance pattern)
- Questions explicitly about "holding period return" or "rate of return"

**Procedure:**
1. **Formula:** 
   - Expected Value: E(X) = Σ[P(i) × X(i)]
   - Variance: Var(X) = Σ[P(i) × (X(i) - E(X))²]
2. Extract probabilities and values (prices, amounts, etc.) from table
3. Calculate expected value using weighted sum
4. If variance is requested, calculate using probability-weighted squared deviations
5. **Keep units consistent** - if inputs are in dollars, output is in dollars (or dollars²)
6. Do NOT multiply by 100 or 10,000 for unit conversion
7. Verify: sum of probabilities = 1.0

**Worked Example:**
**Question:** Calculate the variance of a stock's price given: State 1 (prob 0.25, price $50), State 2 (prob 0.40, price $60), State 3 (prob 0.35, price $70).

```python
import math

# Step 1: Data extraction - prices in dollar amounts
probabilities = [0.25, 0.40, 0.35]
prices = [50, 60, 70]  # in dollars

# Step 2: Calculate expected price
expected_price = sum(p * x for p, x in zip(probabilities, prices))

# Step 3: Calculate variance (in dollars²)
variance_price = sum(p * (x - expected_price)**2 for p, x in zip(probabilities, prices))

# Step 4: Calculate standard deviation (in dollars)
std_dev_price = math.sqrt(variance_price)

# Verification checks (non-blocking)
prob_sum = sum(probabilities)
if abs(prob_sum - 1.0) >= 0.001:
    print(f"Warning: Probabilities sum to {prob_sum}, not 1.0")

# Return variance in original units (dollars²)
# NO conversion to percentage - these are prices, not returns
variance_price
```

**Common Bugs to Avoid:**
- **CRITICAL: Treating prices as returns** - Do NOT multiply by 100 or 10,000 for unit conversion
- **CRITICAL: Confusing expected price with expected return** - Expected price is in currency units, expected return is dimensionless or percentage
- Applying return-based formulas to price data
- Converting currency amounts to percentages inappropriately

**CHECK Steps:**
- Verify input values are in currency/price units (not percentages or decimals like 0.15)
- Verify question asks for "price", "value", or "amount" (not "return")
- Keep output in same units as input (dollars → dollars, dollars² for variance)
- Do NOT apply percentage conversions (×100 or ×10,000)
- If variance result is in range [10-10,000] for stock prices, likely correct for dollar² units