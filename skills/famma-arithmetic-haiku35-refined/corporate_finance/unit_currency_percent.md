# SKILL PATTERNS FOR UNIT/CURRENCY/PERCENT CONVERSION ERRORS IN FINANCIAL CALCULATIONS

## Pattern: Percentage-to-Decimal Conversion for Statistical Calculations

**Description:** When computing statistical measures (mean, variance, standard deviation) on financial returns given as percentages, the values must be converted to decimal form (dividing by 100) before calculation to maintain proper units and scale.

**When to Use:** Questions involving variance, standard deviation, correlation, or other statistical measures on returns, rates, or percentages presented in percentage format (e.g., "9%", "12%").

**Procedure:**
1. Formula: For returns r₁%, r₂%, ..., rₙ%, convert to decimals: r₁/100, r₂/100, ..., rₙ/100
2. Identify if input data is in percentage format (look for "%" symbol or values > 1 when returns are expected)
3. Convert all percentage values to decimal form by dividing by 100
4. Apply statistical formulas (variance, mean, etc.) on decimal values
5. Return result in the format requested (decimal or re-convert to percentage if specified)

**Code Example:**

**Scenario:** Calculate variance and mean return for a stock with annual returns: 8%, 15%, -5%, 12%, 10%

**Correct Code:**
```python
import numpy as np

# Returns given as percentages
returns_pct = [8, 15, -5, 12, 10]

# Convert to decimal form
returns_decimal = [r / 100 for r in returns_pct]

# Calculate sample variance (n-1 denominator)
variance = np.var(returns_decimal, ddof=1)

# Calculate arithmetic mean
mean_return = np.mean(returns_decimal)

# Result as tuple (variance in decimal², mean in decimal)
(variance, mean_return)
```

**Common Bugs to Avoid:**
- Calculating variance directly on percentage values (yields results 10,000× too large)
- Using population variance (ddof=0) instead of sample variance (ddof=1) for financial datasets
- Returning variance in percentage-squared units without clarification
- Mixing percentage and decimal formats within the same calculation

---

## Pattern: Arithmetic vs Geometric Mean for Multi-Period Returns

**Description:** Average returns over multiple periods should use arithmetic mean for simple averaging, but the question context may require geometric mean when returns compound over time or when assessing actual realized growth rates.

**When to Use:** Questions asking for "average return" across multiple periods, especially when returns vary significantly or when the context involves compounding growth.

**Procedure:**
1. Formula (Arithmetic): μ = (r₁ + r₂ + ... + rₙ) / n
2. Formula (Geometric): μ_g = [(1+r₁)(1+r₂)...(1+rₙ)]^(1/n) - 1
3. Convert percentage returns to decimal form
4. Determine which mean is appropriate: arithmetic for expected future returns, geometric for historical compound growth
5. For geometric mean: convert returns to growth factors (1+r), multiply, take nth root, subtract 1
6. Return result in requested format (decimal or percentage)

**Code Example:**

**Scenario:** Calculate both arithmetic and geometric average return for returns: 10%, -8%, 15%, 5%

**Correct Code:**
```python
# Returns as percentages
returns_pct = [10, -8, 15, 5]

# Convert to decimal
returns = [r / 100 for r in returns_pct]

# Arithmetic mean
arithmetic_mean = sum(returns) / len(returns)

# Geometric mean
growth_factors = [1 + r for r in returns]
product = 1
for gf in growth_factors:
    product *= gf
geometric_mean = product ** (1 / len(returns)) - 1

# Return both (in decimal form)
(arithmetic_mean, geometric_mean)
```

**Common Bugs to Avoid:**
- Using arithmetic mean when geometric mean is required for compound growth
- Forgetting to convert returns to growth factors (1+r) before multiplication
- Not subtracting 1 after taking the nth root in geometric mean calculation
- Applying geometric mean to percentage values without decimal conversion

---

## Pattern: Market Value vs Book Value in Financial Ratios

**Description:** Financial ratios and weighted calculations must use market values (not book values) when computing market-based metrics like market capitalization, market value of equity, or WACC with market weights.

**When to Use:** Questions involving market capitalization, Altman Z-score, WACC, or any metric requiring "market value of equity" when both stock price/shares and book values are provided.

**Procedure:**
1. Formula: Market Value of Equity = Stock Price × Shares Outstanding
2. Identify whether the question requires market or book values (keywords: "market cap", "Z-score", "market weights")
3. Calculate market value of equity from stock price and shares outstanding
4. Use market values consistently throughout the calculation
5. Verify units match (dollars, not thousands or millions unless specified)

**Code Example:**

**Scenario:** Calculate market value of equity and debt-to-equity ratio (market basis) for a company with stock price $45, 10,000 shares outstanding, book equity $250,000, total assets $800,000, book debt $550,000

**Correct Code:**
```python
# Market value calculation
stock_price = 45  # dollars per share
shares_outstanding = 10000
market_value_equity = stock_price * shares_outstanding

# Book values
book_equity = 250000
total_assets = 800000
book_debt = 550000

# Market-based debt-to-equity ratio (assuming book value of debt approximates market)
market_debt_to_equity = book_debt / market_value_equity

# Result
market_debt_to_equity
```

**Common Bugs to Avoid:**
- Using book value of equity when market value is required
- Confusing total assets with equity value
- Inconsistent units (mixing per-share values with total values)
- Using book value weights when market value weights are specified

---

## Pattern: After-Tax Cost of Debt in WACC Calculations

**Description:** When calculating WACC, the cost of debt must be adjusted for the tax shield by multiplying by (1 - tax_rate), while equity costs remain unadjusted. Target weights must be converted to proportions of total capital.

**When to Use:** Questions asking for WACC, weighted average cost of capital, or blended cost of capital when tax rate is provided.

**Procedure:**
1. Formula: WACC = (E/V)×r_e + (D/V)×r_d×(1-T)
2. Convert target ratios to weights: if D/E = x, then D/V = x/(1+x) and E/V = 1/(1+x)
3. Calculate after-tax cost of debt: r_d × (1 - tax_rate)
4. If multiple debt types exist, compute weighted average of debt costs first
5. Combine: weight_equity × cost_equity + weight_debt × after_tax_cost_debt
6. Return as decimal (not percentage, unless specified)

**Code Example:**

**Scenario:** Calculate WACC with target debt-to-equity ratio 0.5, cost of equity 12%, cost of debt 6%, tax rate 30%

**Correct Code:**
```python
# Given data
debt_to_equity_ratio = 0.5
cost_of_equity = 0.12  # as decimal
cost_of_debt = 0.06    # as decimal
tax_rate = 0.30

# Convert D/E ratio to weights
total_capital_ratio = 1 + debt_to_equity_ratio
weight_debt = debt_to_equity_ratio / total_capital_ratio
weight_equity = 1 / total_capital_ratio

# After-tax cost of debt
after_tax_cost_debt = cost_of_debt * (1 - tax_rate)

# WACC calculation
wacc = (weight_equity * cost_of_equity) + (weight_debt * after_tax_cost_debt)

# Result as decimal
wacc
```

**Common Bugs to Avoid:**
- Applying tax shield to equity cost (only debt gets tax adjustment)
- Using book value weights when target or market weights are specified
- Incorrectly converting debt-to-equity ratio to capital structure weights
- Forgetting to weight multiple debt types before applying overall debt weight
- Returning result in wrong format (percentage vs decimal)

---

## Pattern: Solving for Interest Rate in Time Value of Money

**Description:** When solving for an unknown interest rate given PV, FV, and n, use the compound interest formula rearranged algebraically: r = (FV/PV)^(1/n) - 1, ensuring the result is returned as a decimal rate. This pattern applies to direct time value of money problems, NOT to beta calculations or other financial metrics that may involve similar mathematical operations.

**When to Use:** Questions explicitly asking to "solve for interest rate", "find the rate", or "calculate the unknown rate" given present value, future value, and time periods in a time value of money context.

**When NOT to Use:** 
- Beta calculations (levered/unlevered beta, equity beta, asset beta)
- CAPM or cost of equity calculations
- Any formula where the exponent or root operation is part of a different financial model (not compound interest)
- Questions asking for equity beta, asset beta, or leverage adjustments

**Procedure:**
1. Formula: FV = PV × (1+r)^n, rearranged: r = (FV/PV)^(1/n) - 1
2. Verify this is a time value of money problem (not beta, WACC, or other metric)
3. Identify the known variables: PV, FV, n
4. Compute the ratio FV/PV
5. Take the nth root: raise to the power (1/n)
6. Subtract 1 to get the interest rate
7. Return as decimal (e.g., 0.0698 for 6.98%)

**Common Mistakes to Avoid:**
- Applying this pattern to beta calculations or leverage formulas that have similar mathematical structure
- Computing simple percentage change (FV-PV)/PV without annualizing
- Forgetting to subtract 1 after taking the nth root
- Using logarithms incorrectly (log(FV/PV)/n gives log of growth rate, not rate itself)
- Returning result as percentage (multiplied by 100) when decimal is expected
- Confusing the formula with simple interest instead of compound interest

**Example (sanitized):**
> **Scenario:** Find the interest rate where $5,000 grows to $9,000 in 8 years
> **Wrong approach:** Applying this pattern to a question asking "What is the equity beta?" just because the calculation involves exponents
> **Correct approach:** Verify the question is about interest rates in a time value context. Calculate: r = (9000/5000)^(1/8) - 1 = 0.0738 or 7.38%

---
## Pattern: Multi-Component Weighted Formula Execution

**Description:** Complex formulas with multiple weighted components (like Altman Z-score) require careful step-by-step calculation of each ratio, application of correct coefficients, and proper summation to avoid algebraic errors.

**When to Use:** Questions involving Altman Z-score, multi-factor models, or any formula with 3+ weighted components that must be summed.

**Procedure:**
1. Formula: Z = c₁×X₁ + c₂×X₂ + c₃×X₃ + ... (identify all coefficients and ratios)
2. Calculate each component ratio separately with clear variable names
3. Apply the correct coefficient to each ratio
4. Store intermediate results for verification
5. Sum all weighted components
6. Verify units are consistent across all ratios
7. Return final sum

**Code Example:**

**Scenario:** Calculate a simplified credit score: Score = 2.5×(Current Ratio) + 1.8×(ROA) + 3.0×(Equity/Assets), given current assets $50k, current liabilities $30k, net income $8k, total assets $100k, equity $60k

**Correct Code:**
```python
# Given data
current_assets = 50000
current_liabilities = 30000
net_income = 8000
total_assets = 100000
equity = 60000

# Calculate each ratio
current_ratio = current_assets / current_liabilities
roa = net_income / total_assets
equity_ratio = equity / total_assets

# Apply coefficients
component_1 = 2.5 * current_ratio
component_2 = 1.8 * roa
component_3 = 3.0 * equity_ratio

# Sum all components
credit_score = component_1 + component_2 + component_3

# Result
credit_score
```

**Common Bugs to Avoid:**
- Mixing up coefficients or applying wrong weights to ratios
- Calculating ratios with inconsistent units (e.g., thousands vs dollars)
- Skipping intermediate variable storage, making errors hard to trace
- Forgetting to include all components in the final sum
- Using book values when market values are required for specific ratios

## Pattern: Levered Beta Calculation Using Hamada Formula

**Description:** When calculating equity beta for a levered firm, use the Hamada formula to adjust the unlevered (asset) beta for financial leverage: β_L = β_U × [1 + (1-T) × (D/E)]. This accounts for the amplification of systematic risk due to debt financing. The result should maintain full precision unless the question explicitly requests rounding.

**When to Use:** Questions asking for "equity beta", "levered beta", or "beta of equity" when given unlevered beta, debt-to-equity ratio (or debt and equity values), and tax rate.

**Procedure:**
1. Formula: β_L = β_U × [1 + (1-T) × (D/E)]
2. Identify the unlevered beta (β_U) - may be given directly or as "all-equity beta"
3. Calculate debt-to-equity ratio: D/E = Market Value of Debt / Market Value of Equity
4. Apply tax shield adjustment: (1 - tax_rate)
5. Compute leverage multiplier: [1 + (1-T) × (D/E)]
6. Multiply unlevered beta by leverage multiplier
7. Return result with full precision (do not round unless explicitly requested)

**Common Mistakes to Avoid:**
- Confusing this with time value of money calculations despite similar mathematical operations
- Using book values when market values are provided
- Forgetting the tax adjustment (1-T) in the leverage multiplier
- Rounding intermediate results, which can cause precision mismatches
- Using the wrong formula (e.g., unlevering formula when levering is needed)
- Applying interest rate solving patterns to beta calculations

**Example (sanitized):**
> **Scenario:** Calculate equity beta for a company with unlevered beta 1.25, debt $5M, equity $3M, tax rate 30%
> **Wrong approach:** Treating this as an interest rate problem because it involves multiplication and ratios
> **Correct approach:** Apply Hamada formula: β_L = 1.25 × [1 + (1-0.30) × (5,000,000/3,000,000)] = 1.25 × [1 + 0.70 × 1.667] = 1.25 × 2.167 = 2.708333...

```python
# Given parameters
unlevered_beta = 1.25
debt = 5_000_000
equity = 3_000_000
tax_rate = 0.30

# Calculate debt-to-equity ratio
debt_to_equity = debt / equity

# Apply Hamada formula for levered beta
levered_beta = unlevered_beta * (1 + (1 - tax_rate) * debt_to_equity)

# Return with full precision
levered_beta
```