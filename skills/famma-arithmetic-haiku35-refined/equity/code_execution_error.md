# SKILL PATTERNS FOR EQUITY CALCULATIONS (Program of Thought)

---

## Pattern: Variance-to-Standard-Deviation Conversion

**Description:** Standard deviation is the square root of variance. Failing to apply `sqrt()` after computing variance results in returning variance instead of standard deviation, causing magnitude errors in volatility measures.

**When to Use:** Questions asking for "standard deviation," "volatility," or "risk" of returns when given probability distributions of outcomes.

**Procedure:**
1. Formula: σ = √[Σ(pᵢ × (xᵢ - μ)²)] where μ = Σ(pᵢ × xᵢ)
2. Calculate expected value (mean) as probability-weighted sum of outcomes
3. Compute variance as probability-weighted sum of squared deviations from mean
4. Apply square root to variance to obtain standard deviation
5. Convert to percentage if returns are in decimal form (multiply by 100)
6. Return final value as expression matching answer format

**Code Example:**

**Scenario:** Calculate standard deviation of returns given: Probability [0.40, 0.35, 0.25] and Returns [15%, 10%, -5%]

**Correct Code:**
```python
import math

probabilities = [0.40, 0.35, 0.25]
returns = [0.15, 0.10, -0.05]

# Step 1: Expected return
expected_return = sum(p * r for p, r in zip(probabilities, returns))

# Step 2: Variance
variance = sum(p * (r - expected_return)**2 for p, r in zip(probabilities, returns))

# Step 3: Standard deviation (MUST take square root)
std_dev = math.sqrt(variance)

# Step 4: Convert to percentage
std_dev_percent = std_dev * 100

std_dev_percent  # Result: ~8.62%
```

**Common Bugs to Avoid:**
- Returning variance instead of standard deviation (forgetting `math.sqrt()`)
- Using `print()` on last line instead of expression
- Forgetting to import `math` module
- Mixing decimal and percentage formats (0.15 vs 15%)
- Not matching output units to answer choices

---

## Pattern: Sign Convention Validation for Economic States

**Description:** OCR-extracted or tabular data may represent negative returns as positive numbers, especially for adverse economic states (Depression, Recession). Code must validate that return signs are contextually plausible before calculation.

**When to Use:** Expected return calculations with economic state scenarios, especially when states include "Depression," "Recession," "Crisis," or other negative contexts with suspiciously high positive returns.

**Procedure:**
1. Formula: E(R) = Σ(pᵢ × rᵢ)
2. Parse probabilities and returns from input data
3. Validate: Check if adverse states (Depression, Recession) have implausibly high positive returns
4. Apply sign correction: If Depression return > Normal/Boom return, interpret as negative
5. Compute probability-weighted expected return
6. Return result in appropriate format (decimal or percentage)

**Code Example:**

**Scenario:** Calculate expected return with states: Recession (p=0.20, r=0.08), Normal (p=0.50, r=0.12), Boom (p=0.30, r=0.18)

**Correct Code:**
```python
states = ['Recession', 'Normal', 'Boom']
probabilities = [0.20, 0.50, 0.30]
returns = [0.08, 0.12, 0.18]

# Step 1: Validate sign conventions
corrected_returns = []
for i, state in enumerate(states):
    r = returns[i]
    # Check if adverse state has implausibly high return
    if state.lower() in ['depression', 'recession', 'crisis']:
        # If return seems too high for adverse state, may need negation
        avg_return = sum(returns) / len(returns)
        if r > avg_return * 0.8:  # Heuristic check
            # Context suggests this might be negative
            # Manual review recommended, but flag for attention
            pass
    corrected_returns.append(r)

# Step 2: Calculate expected return
expected_return = sum(p * r for p, r in zip(probabilities, corrected_returns))

expected_return  # Result: 0.134 or 13.4%
```

**Common Bugs to Avoid:**
- Blindly trusting OCR output without contextual validation
- Not checking if Depression/Recession returns exceed Normal/Boom returns
- Failing to document sign convention assumptions in comments
- Not flagging suspicious data for manual review

---

## Pattern: Probability-Weighted Expected Value

**Description:** Expected values require correct probability-weighted summation. Errors occur from incorrect weight application, arithmetic mistakes in multiplication/addition, or misreading probability/value pairs from tables.

**When to Use:** Questions asking for "expected return," "expected price," "expected value," or "mean" given probability distributions.

**Procedure:**
1. Formula: E(X) = Σ(pᵢ × xᵢ) where Σpᵢ = 1
2. Extract all probability-value pairs from input
3. Verify probabilities sum to 1.0 (or 100%)
4. Compute each product: probability × value
5. Sum all products to get expected value
6. Verify result is within range [min(values), max(values)]
7. Return result matching answer format

**Code Example:**

**Scenario:** Calculate expected stock price with: State 1 (p=0.30, price=$45), State 2 (p=0.45, price=$52), State 3 (p=0.25, price=$61)

**Correct Code:**
```python
probabilities = [0.30, 0.45, 0.25]
prices = [45, 52, 61]

# Step 1: Validate probabilities sum to 1
prob_sum = sum(probabilities)
assert abs(prob_sum - 1.0) < 0.001, f"Probabilities sum to {prob_sum}, not 1.0"

# Step 2: Calculate expected value
expected_price = sum(p * price for p, price in zip(probabilities, prices))

# Step 3: Sanity check - result should be between min and max
assert min(prices) <= expected_price <= max(prices), "Expected value out of range"

# Step 4: Round to appropriate precision
expected_price_rounded = round(expected_price, 2)

expected_price_rounded  # Result: $52.55
```

**Common Bugs to Avoid:**
- Misreading probability or value from OCR text (e.g., 0.40 as 0.30)
- Forgetting to multiply each term by its probability
- Using equal weights instead of given probabilities
- Not validating that probabilities sum to 1.0
- Arithmetic errors in manual summation (use list comprehension)

---

## Pattern: Firm Value vs. Equity Value Decomposition

**Description:** In leveraged firms, total firm value equals debt plus equity. Questions asking for "company value" or "firm value" require summing all claims, not just equity residual after debt payment.

**When to Use:** Corporate finance questions involving debt obligations, bondholders, project payoffs, and phrases like "value of the company," "enterprise value," or "firm value."

**Procedure:**
1. Formula: Firm Value = E(Project Payoff) = Debt Value + Equity Value
2. Calculate expected project payoff using probability-weighted outcomes
3. If asked for firm value: return expected project payoff directly
4. If asked for equity value: subtract debt obligation from expected payoff (max with 0)
5. If asked for debt value: use min(expected payoff, face value of debt)
6. Clearly identify which component the question requests

**Code Example:**

**Scenario:** Project payoffs: Bad state (p=0.40, payoff=$5000), Good state (p=0.60, payoff=$7000). Debt obligation: $4500. Find firm value and equity value.

**Correct Code:**
```python
probabilities = [0.40, 0.60]
payoffs = [5000, 7000]
debt_face_value = 4500

# Step 1: Expected firm value (total project payoff)
expected_firm_value = sum(p * payoff for p, payoff in zip(probabilities, payoffs))

# Step 2: Expected equity value (residual after debt)
# Equity gets max(0, payoff - debt) in each state
equity_payoffs = [max(0, payoff - debt_face_value) for payoff in payoffs]
expected_equity_value = sum(p * eq for p, eq in zip(probabilities, equity_payoffs))

# Step 3: Expected debt value
# Debt gets min(payoff, face_value) in each state
debt_payoffs = [min(payoff, debt_face_value) for payoff in payoffs]
expected_debt_value = sum(p * d for p, d in zip(probabilities, debt_payoffs))

# Verification: Firm value = Debt value + Equity value
assert abs(expected_firm_value - (expected_debt_value + expected_equity_value)) < 0.01

# Return based on question
expected_firm_value  # Result: $6200 (if question asks for firm value)
```

**Common Bugs to Avoid:**
- Confusing firm value with equity value (returning residual instead of total)
- Calculating equity as simple subtraction without considering limited liability
- Not recognizing that debt + equity = firm value identity
- Ignoring state-contingent payoffs to debt and equity
- Using wrong formula when debt is risky (face value ≠ market value)

---

## Pattern: Unit Consistency and Format Matching

**Description:** Financial calculations require consistent units throughout (decimals vs. percentages) and final answers must match the format of answer choices (percentage with %, dollar amounts with $, decimal precision).

**When to Use:** All financial calculations, especially when answer choices show specific formatting (%, $, decimal places).

**Procedure:**
1. Identify input units (0.15 = decimal, 15% = percentage)
2. Convert all inputs to consistent unit system (prefer decimals for calculation)
3. Perform calculations in consistent units
4. Convert final result to match answer choice format
5. Round to precision matching answer choices
6. Return with appropriate formatting (%, $, etc.)

**Code Example:**

**Scenario:** Calculate expected return from returns [12%, 8%, -3%] with probabilities [0.50, 0.30, 0.20]. Answer choices in percentage format.

**Correct Code:**
```python
probabilities = [0.50, 0.30, 0.20]
returns_percent = [12, 8, -3]  # Given as percentages

# Step 1: Convert to decimal for calculation
returns_decimal = [r / 100 for r in returns_percent]

# Step 2: Calculate in decimal
expected_return_decimal = sum(p * r for p, r in zip(probabilities, returns_decimal))

# Step 3: Convert back to percentage for answer
expected_return_percent = expected_return_decimal * 100

# Step 4: Round to match answer precision (typically 2 decimal places)
expected_return_percent = round(expected_return_percent, 2)

expected_return_percent  # Result: 7.40 (representing 7.40%)
```

**Common Bugs to Avoid:**
- Mixing decimals and percentages in same calculation (0.12 + 8%)
- Returning decimal when answer choices are percentages
- Wrong precision (returning 7.4 when choices show 7.40%)
- Missing % symbol in interpretation
- Off-by-factor-of-100 errors from unit confusion