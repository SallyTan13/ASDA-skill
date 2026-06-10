# SKILL PATTERNS FOR EQUITY CALCULATIONS (Program of Thought)

## Pattern: Beta-Adjusted Futures Contract Calculation

**Description:** When hedging or adjusting portfolio exposure using futures contracts, the number of contracts must account for both the portfolio asset's beta and the futures contract's beta using the ratio (β_portfolio / β_futures), not division by futures beta alone.

**When to Use:** Questions involving futures contracts to adjust equity exposure, hedge positions, or create synthetic positions; keywords: "futures contracts," "exposure," "hedge ratio," "beta adjustment."

**Procedure:**
1. Formula: `N_contracts = (Target_Exposure / Contract_Value) × (β_portfolio / β_futures)`
   - Where Contract_Value = Futures_Price × Multiplier
2. Calculate the notional value of one futures contract (price × multiplier)
3. Determine the target exposure amount to adjust (in dollars)
4. Apply beta adjustment as a RATIO: multiply by (portfolio asset beta / futures beta)
5. Round to nearest whole number of contracts
6. Verify: contracts × contract_value × β_futures should approximately equal target exposure × β_portfolio

**Code Example:**

**Scenario:** A portfolio wants to reduce $50 million exposure to small-cap stocks (beta = 1.5) using small-cap futures (price = $1,200, multiplier = 100, beta = 1.2).

**Correct Code:**
```python
# Given values
target_exposure = 50_000_000  # $50 million to reduce
portfolio_beta = 1.5  # beta of small-cap stocks in portfolio
futures_price = 1_200
futures_multiplier = 100
futures_beta = 1.2

# Step 1: Calculate contract value
contract_value = futures_price * futures_multiplier

# Step 2: Calculate number of contracts with beta adjustment
# Correct formula: (Exposure / Contract_Value) × (β_portfolio / β_futures)
contracts_needed = (target_exposure / contract_value) * (portfolio_beta / futures_beta)

# Step 3: Round to whole number
contracts_final = round(contracts_needed)

# Step 4: Verification
actual_exposure = contracts_final * contract_value * futures_beta
expected_exposure = target_exposure * portfolio_beta

# Return final answer
contracts_final
```

**Common Bugs to Avoid:**
- Dividing by futures beta instead of using the ratio (β_portfolio / β_futures)
- Forgetting to multiply by portfolio beta entirely
- Applying beta adjustment in reverse (β_futures / β_portfolio)
- Not accounting for contract multiplier when calculating contract value
- Using print() instead of expression on last line for PoT execution

---

## Pattern: Decimal-to-Percentage Unit Consistency

**Description:** When reading return or rate values from tables, verify whether values are already in decimal form (0.105 = 10.5%) or need conversion. Maintain consistent units throughout calculations and convert final answer to match expected output format.

**When to Use:** Questions with return data in tables, especially when calculating standard deviation, variance, expected return; keywords: "rate of return," "calculate standard deviation," "expected return."

**Procedure:**
1. Identify the unit format from context (e.g., 0.105 in a returns table typically means 10.5%, already decimal)
2. Use values as-is if already in decimal form; do NOT divide by 100 again
3. Perform all intermediate calculations in decimal form
4. Convert final answer to requested format (e.g., 0.09 → 9.00% or 0.0900)
5. Sanity check: returns typically range 5-20% (0.05-0.20), standard deviations 5-30% (0.05-0.30)

**Code Example:**

**Scenario:** Calculate standard deviation of returns given: Recession (prob=0.4, return=0.08), Normal (prob=0.5, return=0.12), Boom (prob=0.1, return=0.18).

**Correct Code:**
```python
import math

# Data from table (already in decimal form: 0.08 = 8%)
probabilities = [0.4, 0.5, 0.1]
returns = [0.08, 0.12, 0.18]  # Already decimals, NOT percentages

# Step 1: Calculate expected return
expected_return = sum(p * r for p, r in zip(probabilities, returns))

# Step 2: Calculate variance
variance = sum(p * (r - expected_return)**2 for p, r in zip(probabilities, returns))

# Step 3: Calculate standard deviation
std_dev = math.sqrt(variance)

# Step 4: Sanity check (should be between 0.01 and 0.30 for typical returns)
assert 0.01 <= std_dev <= 0.30, f"Unusual std_dev: {std_dev}"

# Return in decimal form (convert to percentage if needed: std_dev * 100)
std_dev
```

**Common Bugs to Avoid:**
- Double-converting percentages (treating 0.105 as 0.105% instead of 10.5%)
- Mixing decimal and percentage formats in same calculation
- Forgetting to import math module for sqrt()
- Not performing sanity checks on magnitude of results
- Reading OCR values incorrectly (e.g., misreading 0.105 as 0.015)

---

## Pattern: Covariance and Correlation Calculation with Equal Probabilities

**Description:** When calculating covariance between two assets with discrete states, correctly compute expected returns first, then apply the covariance formula with proper probability weighting for each state.

**When to Use:** Questions asking for covariance, correlation, or portfolio variance with multiple economic states; keywords: "covariance," "correlation," "equally likely," "state of economy."

**Procedure:**
1. Formula: `Cov(A,B) = Σ[P_i × (R_A,i - E(R_A)) × (R_B,i - E(R_B))]`
2. Calculate expected return for each asset: `E(R) = Σ(P_i × R_i)`
3. For each state, compute deviations: `(R_i - E(R))`
4. Multiply deviations for both assets and weight by probability for each state
5. Sum across all states to get covariance
6. Sanity check: covariance sign should match general co-movement pattern

**Code Example:**

**Scenario:** Calculate covariance for Stock X and Stock Y with three equally likely states: State 1 (X=0.10, Y=0.15), State 2 (X=0.14, Y=0.12), State 3 (X=0.08, Y=0.20).

**Correct Code:**
```python
# Given data
states = 3
probability = 1 / states  # Equally likely
returns_X = [0.10, 0.14, 0.08]
returns_Y = [0.15, 0.12, 0.20]

# Step 1: Calculate expected returns (CORRECT method)
expected_X = sum(r * probability for r in returns_X)
expected_Y = sum(r * probability for r in returns_Y)

# Alternative (equivalent): expected_X = sum(returns_X) / states

# Step 2: Calculate deviations from expected returns
deviations_X = [r - expected_X for r in returns_X]
deviations_Y = [r - expected_Y for r in returns_Y]

# Step 3: Calculate covariance
covariance = sum(deviations_X[i] * deviations_Y[i] * probability 
                 for i in range(states))

# Step 4: Verification - check intermediate values
assert abs(expected_X - sum(returns_X)/states) < 1e-10, "Expected return calculation error"

# Return covariance
covariance
```

**Common Bugs to Avoid:**
- Computing expected return as `sum(returns) * probability` instead of `sum(returns * probability)` or `sum(returns) / n`
- Forgetting to multiply by probability when summing covariance terms
- Using wrong probability values (e.g., 1/3 for 4 states)
- Arithmetic errors in manual deviation calculations
- Not using list comprehension or vectorized operations leading to index errors
- Confusing covariance with correlation (correlation = covariance / (σ_A × σ_B))

---

## Pattern: Financial Result Precision and Format

**Description:** Financial calculations must return results with appropriate precision (typically 4-6 decimal places for rates/returns) and match the expected output format, using expression evaluation rather than print statements.

**When to Use:** All PoT financial calculations; especially important for variance, standard deviation, covariance, and return metrics.

**Procedure:**
1. Perform calculations using full floating-point precision
2. Do NOT round intermediate values (only round final answer if required)
3. Return result as expression on last line (not print statement)
4. For percentages: clarify whether answer should be decimal (0.09) or percentage (9.00%)
5. Include verification step comparing magnitude to expected range

**Code Example:**

**Scenario:** Calculate portfolio variance given weights [0.6, 0.4], returns [0.12, 0.08], and standard deviations [0.15, 0.10], correlation = 0.3.

**Correct Code:**
```python
import math

# Given values
weights = [0.6, 0.4]
std_devs = [0.15, 0.10]
correlation = 0.3

# Step 1: Calculate variance (full precision)
variance = (weights[0]**2 * std_devs[0]**2 + 
            weights[1]**2 * std_devs[1]**2 + 
            2 * weights[0] * weights[1] * std_devs[0] * std_devs[1] * correlation)

# Step 2: Calculate standard deviation
portfolio_std = math.sqrt(variance)

# Step 3: Sanity check
assert 0 < portfolio_std < max(std_devs), "Portfolio std should be between 0 and max individual std"

# Step 4: Return with appropriate precision (expression, not print)
# If answer needs 4 decimals: round(portfolio_std, 4)
# Otherwise return full precision:
portfolio_std
```

**Common Bugs to Avoid:**
- Using print() instead of expression on last line (PoT requires expression evaluation)
- Rounding intermediate calculations causing cumulative errors
- Returning wrong variable (e.g., variance instead of standard deviation)
- Not importing required modules (math, numpy)
- Inconsistent decimal places in final answer
- Missing sanity checks for unrealistic values (negative variance, returns > 100%)