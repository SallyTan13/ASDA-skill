# SKILL PATTERNS FOR PORTFOLIO MANAGEMENT CODE EXECUTION

## Pattern: Time-Weighted Return (TWR) with Cash Flows

**Description:** TWR requires geometric linking of sub-period returns calculated between each cash flow event, not simple averaging or subtraction. Each sub-period return uses the post-cash-flow value from the previous period as the beginning value.

**When to Use:** Questions involving portfolio performance measurement with multiple cash flows (contributions/withdrawals) at different dates, when asked to calculate time-weighted return.

**Procedure:**
1. **Formula:** TWR = [(1 + r₁) × (1 + r₂) × ... × (1 + rₙ)] - 1, where rᵢ = (Ending_Value - Cash_Flow) / Beginning_Value - 1 for each sub-period
2. Identify all cash flow dates to segment the evaluation period into sub-periods
3. For each sub-period: calculate holding period return using market value immediately before cash flow as ending value, and post-cash-flow value from previous period as beginning value
4. Chain-link all sub-period returns using geometric multiplication
5. Return the final result as a decimal (not percentage), ensuring it's an expression not a print statement

**Code Example:**

**Scenario:** Portfolio starts with $50,000. Day 5: $300 contribution, value becomes $52,300. Day 12: $500 withdrawal, value becomes $53,200. Day 20: ending value $54,100.

**Correct Code:**
```python
# Initial value
initial_value = 50000

# Day 5: contribution
day5_contribution = 300
day5_post_cf_value = 52300
day5_pre_cf_value = day5_post_cf_value - day5_contribution  # 52000
r1 = (day5_pre_cf_value / initial_value) - 1  # (52000/50000) - 1

# Day 12: withdrawal
day12_withdrawal = 500
day12_post_cf_value = 53200
day12_pre_cf_value = day12_post_cf_value + day12_withdrawal  # 53700
r2 = (day12_pre_cf_value / day5_post_cf_value) - 1  # (53700/52300) - 1

# Day 20: ending
day20_value = 54100
r3 = (day20_value / day12_post_cf_value) - 1  # (54100/53200) - 1

# Geometric linking
twr = (1 + r1) * (1 + r2) * (1 + r3) - 1
twr  # Must be expression, not print(twr)
```

**Common Bugs to Avoid:**
- Using ending values directly without adjusting for cash flows (must subtract contributions, add withdrawals)
- Arithmetic averaging of returns instead of geometric linking
- Using beginning-of-period values incorrectly (each sub-period begins with post-cash-flow value from previous period)
- Returning -100.0 or None due to logic errors or using print() instead of expression
- Confusing TWR with money-weighted return (IRR)

---

## Pattern: Probability-Weighted Covariance and Correlation

**Description:** Covariance between two securities requires probability-weighted calculation of cross-products of deviations from means. Correlation normalizes covariance by the product of standard deviations.

**When to Use:** Questions providing discrete probability distributions for multiple securities and asking for covariance, correlation coefficient, or related portfolio statistics.

**Procedure:**
1. **Formula:** Cov(X,Y) = Σ pᵢ(xᵢ - μₓ)(yᵢ - μᵧ); Corr(X,Y) = Cov(X,Y) / (σₓ × σᵧ)
2. Calculate expected returns: E[X] = Σ pᵢxᵢ and E[Y] = Σ pᵢyᵢ
3. Calculate variances: Var(X) = Σ pᵢ(xᵢ - E[X])² and Var(Y) = Σ pᵢ(yᵢ - E[Y])²
4. Calculate standard deviations: σₓ = √Var(X), σᵧ = √Var(Y)
5. Calculate covariance: Cov(X,Y) = Σ pᵢ(xᵢ - E[X])(yᵢ - E[Y])
6. For correlation: divide covariance by product of standard deviations
7. Return result as expression with appropriate precision

**Code Example:**

**Scenario:** Two stocks with probability distribution: State 1 (p=0.3, A=8%, B=5%), State 2 (p=0.5, A=12%, B=10%), State 3 (p=0.2, A=15%, B=8%)

**Correct Code:**
```python
import math

# Data
probs = [0.3, 0.5, 0.2]
returns_A = [0.08, 0.12, 0.15]
returns_B = [0.05, 0.10, 0.08]

# Expected returns
E_A = sum(p * r for p, r in zip(probs, returns_A))
E_B = sum(p * r for p, r in zip(probs, returns_B))

# Variances
var_A = sum(p * (r - E_A)**2 for p, r in zip(probs, returns_A))
var_B = sum(p * (r - E_B)**2 for p, r in zip(probs, returns_B))

# Standard deviations
std_A = math.sqrt(var_A)
std_B = math.sqrt(var_B)

# Covariance
cov_AB = sum(p * (rA - E_A) * (rB - E_B) for p, rA, rB in zip(probs, returns_A, returns_B))

# Correlation
corr_AB = cov_AB / (std_A * std_B)

corr_AB  # Expression, not print
```

**Common Bugs to Avoid:**
- Forgetting to weight by probabilities in all calculations
- Using sample formulas (n-1) instead of population formulas for discrete distributions
- Arithmetic errors in manual calculation of deviations
- Incorrect order of operations (must calculate means before deviations)
- Rounding intermediate values too aggressively, causing cumulative errors
- Returning correlation when covariance is asked (or vice versa)

---

## Pattern: Portfolio Standard Deviation from Discrete Distribution

**Description:** Portfolio standard deviation requires calculating the portfolio return in each state, then computing the probability-weighted variance of these portfolio returns, not combining individual security variances directly.

**When to Use:** Questions asking for portfolio standard deviation or variance when given discrete probability distributions for individual securities and portfolio weights.

**Procedure:**
1. **Formula:** σₚ = √[Σ pᵢ(Rₚᵢ - E[Rₚ])²], where Rₚᵢ = Σ wⱼRⱼᵢ
2. For each state i, calculate portfolio return: Rₚᵢ = w₁R₁ᵢ + w₂R₂ᵢ + ... (weighted sum of security returns)
3. Calculate expected portfolio return: E[Rₚ] = Σ pᵢRₚᵢ
4. Calculate portfolio variance: Var(Rₚ) = Σ pᵢ(Rₚᵢ - E[Rₚ])²
5. Calculate portfolio standard deviation: σₚ = √Var(Rₚ)
6. Return as expression (not 0.0 or None from print statement)

**Code Example:**

**Scenario:** Portfolio with 60% in Stock X and 40% in Stock Y. State 1 (p=0.4, X=10%, Y=8%), State 2 (p=0.6, X=15%, Y=12%)

**Correct Code:**
```python
import math

# Portfolio weights
w_X = 0.6
w_Y = 0.4

# Probability distribution
probs = [0.4, 0.6]
returns_X = [0.10, 0.15]
returns_Y = [0.08, 0.12]

# Portfolio returns in each state
portfolio_returns = [w_X * rX + w_Y * rY for rX, rY in zip(returns_X, returns_Y)]

# Expected portfolio return
E_portfolio = sum(p * rp for p, rp in zip(probs, portfolio_returns))

# Portfolio variance
var_portfolio = sum(p * (rp - E_portfolio)**2 for p, rp in zip(probs, portfolio_returns))

# Portfolio standard deviation
std_portfolio = math.sqrt(var_portfolio)

std_portfolio  # Must be expression
```

**Common Bugs to Avoid:**
- Returning 0.0 because of print() statement instead of expression
- Trying to use portfolio variance formula (w²σ² + ...) without covariance when only state-by-state returns are given
- Forgetting to weight returns by portfolio weights in each state
- Not taking square root of variance to get standard deviation
- Missing import of math module for sqrt function

---

## Pattern: Tax Lot Accounting with Capital Gains/Losses

**Description:** Tax lot accounting requires identifying specific shares sold based on the chosen method (HIFO, FIFO, LIFO), calculating gain/loss per share, determining holding period for tax rate, and computing net tax liability or benefit.

**When to Use:** Questions involving sale of securities with multiple purchase lots, tax lot accounting methods (HIFO/FIFO/LIFO), different tax rates for short-term vs long-term holdings, and calculation of tax liability or benefit.

**Procedure:**
1. **Formula:** Tax = (Sale_Price - Cost_Basis) × Shares_Sold × Tax_Rate
2. Parse purchase history into structured data (date, shares, price per share, total cost)
3. Determine holding period for each lot (compare purchase date to sale date)
4. Assign appropriate tax rate based on holding period (short-term vs long-term)
5. Apply tax lot method: HIFO (highest cost first), FIFO (first in first out), LIFO (last in first out)
6. Calculate gain/loss: (Sale_Price - Cost_Basis_Per_Share) × Shares_From_Lot
7. Calculate tax: Gain/Loss × Tax_Rate (negative result = tax benefit)
8. Return result ensuring proper sign convention (loss = negative tax = benefit)

**Code Example:**

**Scenario:** Sell 150 shares at $80/share on Sept 1. Purchases: Jan 15 (100 shares @ $75), June 1 (100 shares @ $85), Aug 1 (50 shares @ $90). Long-term rate 20%, short-term rate 35%. Use HIFO method.

**Correct Code:**
```python
from datetime import datetime

# Sale details
sale_date = datetime(2023, 9, 1)
sale_price = 80
shares_to_sell = 150

# Purchase lots: (date, shares, cost_per_share)
lots = [
    (datetime(2023, 1, 15), 100, 75),
    (datetime(2023, 6, 1), 100, 85),
    (datetime(2023, 8, 1), 50, 90)
]

# Tax rates
long_term_rate = 0.20  # > 6 months
short_term_rate = 0.35  # <= 6 months

# HIFO: sort by cost_per_share descending
lots_sorted = sorted(lots, key=lambda x: x[2], reverse=True)

total_tax = 0
shares_remaining = shares_to_sell

for purchase_date, shares_available, cost_per_share in lots_sorted:
    if shares_remaining <= 0:
        break
    
    # Determine shares from this lot
    shares_from_lot = min(shares_remaining, shares_available)
    
    # Holding period
    days_held = (sale_date - purchase_date).days
    is_long_term = days_held > 180  # 6 months
    
    # Tax rate
    tax_rate = long_term_rate if is_long_term else short_term_rate
    
    # Gain/loss
    gain_loss = (sale_price - cost_per_share) * shares_from_lot
    
    # Tax (negative = benefit)
    tax = gain_loss * tax_rate
    total_tax += tax
    
    shares_remaining -= shares_from_lot

total_tax  # Expression, not print
```

**Common Bugs to Avoid:**
- Code execution failure due to improper data structure handling or missing imports
- Incorrect sorting for HIFO (should be descending by cost basis)
- Wrong holding period calculation (using months instead of days, or incorrect threshold)
- Sign errors: forgetting that losses produce negative tax (tax benefit)
- Not handling partial lot sales (selling fewer shares than available in a lot)
- Using wrong tax rate for holding period

---

## Pattern: EWMA Model Updates for Volatility and Correlation

**Description:** EWMA (Exponentially Weighted Moving Average) updates require applying the recursive formula to variance/covariance, handling zero returns correctly, and using updated volatilities (not old ones) in final correlation calculation.

**When to Use:** Questions involving EWMA or GARCH models for updating volatility estimates, correlation estimates, or covariance between assets given lambda parameter and new return observations.

**Procedure:**
1. **Formula:** σₙ² = λσₙ₋₁² + (1-λ)rₙ₋₁²; Covₙ = λCovₙ₋₁ + (1-λ)rₓ,ₙ₋₁rᵧ,ₙ₋₁; Corrₙ = Covₙ/(σₓ,ₙ × σᵧ,ₙ)
2. Calculate returns from price changes: r = (P_new - P_old) / P_old
3. Update variance for each asset: variance_new = λ × variance_old + (1-λ) × return²
4. Update covariance: covariance_new = λ × covariance_old + (1-λ) × return_x × return_y
5. Calculate new volatilities: volatility_new = √variance_new
6. Calculate new correlation: correlation_new = covariance_new / (volatility_x_new × volatility_y_new)
7. Use updated volatilities in denominator, not old volatilities

**Code Example:**

**Scenario:** Gold: yesterday $500, today $495, old volatility 1.2%/day. Silver: yesterday $25, today $25, old volatility 1.8%/day. Old correlation 0.75. Lambda = 0.94. Update correlation.

**Correct Code:**
```python
import math

# Parameters
lambda_param = 0.94

# Gold
gold_price_old = 500
gold_price_new = 495
gold_vol_old = 0.012  # 1.2% as decimal
gold_return = (gold_price_new - gold_price_old) / gold_price_old

# Silver
silver_price_old = 25
silver_price_new = 25
silver_vol_old = 0.018  # 1.8% as decimal
silver_return = (silver_price_new - silver_price_old) / silver_price_old  # = 0

# Old covariance from old correlation
cov_old = 0.75 * gold_vol_old * silver_vol_old

# Update variances
gold_var_new = lambda_param * (gold_vol_old ** 2) + (1 - lambda_param) * (gold_return ** 2)
silver_var_new = lambda_param * (silver_vol_old ** 2) + (1 - lambda_param) * (silver_return ** 2)

# Update covariance (handles zero return correctly)
cov_new = lambda_param * cov_old + (1 - lambda_param) * gold_return * silver_return

# New volatilities
gold_vol_new = math.sqrt(gold_var_new)
silver_vol_new = math.sqrt(silver_var_new)

# New correlation (using NEW volatilities)
corr_new = cov_new / (gold_vol_new * silver_vol_new)

corr_new  # Expression
```

**Common Bugs to Avoid:**
- Using old volatilities in correlation denominator instead of updated volatilities
- Incorrectly handling zero returns (they still affect variance/covariance updates)
- Forgetting to convert volatility to variance before updating (must square)
- Wrong order of operations (update variances/covariance first, then calculate correlation)
- Not taking square root to convert updated variance back to volatility
- Confusing lambda weighting (old values get λ, new observations get 1-λ)

---

## Pattern: Complete Portfolio Risk Calculation

**Description:** Complete portfolio standard deviation is the weighted standard deviation of the risky portfolio component only, since risk-free assets have zero standard deviation and zero correlation with risky assets.

**When to Use:** Questions involving a complete portfolio consisting of a risky portfolio and risk-free assets (T-Bills, cash), asking for the standard deviation or risk of the complete portfolio.

**Procedure:**
1. **Formula:** σ_complete = w_risky × σ_risky (risk-free assets contribute zero risk)
2. Identify the proportion invested in the risky portfolio (w_risky)
3. Identify the standard deviation of the risky portfolio (σ_risky)
4. Multiply weight by risky portfolio standard deviation
5. Risk-free allocation does NOT require separate calculation (contributes 0 to portfolio risk)
6. Return result as expression, ensuring code executes without errors

**Code Example:**

**Scenario:** Complete portfolio with 75% in risky portfolio (std dev = 18%) and 25% in T-Bills. Calculate complete portfolio standard deviation.

**Correct Code:**
```python
# Portfolio composition
weight_risky = 0.75
weight_risk_free = 0.25  # Not needed for calculation

# Risky portfolio characteristics
std_dev_risky = 0.18  # 18%

# Complete portfolio standard deviation
# Risk-free assets have zero std dev and zero correlation
std_dev_complete = weight_risky * std_dev_risky

std_dev_complete  # Must be expression
```

**Common Bugs to Avoid:**
- Code execution failure due to syntax errors in simple multiplication
- Trying to use full portfolio variance formula unnecessarily
- Forgetting that risk-free assets contribute zero to portfolio risk
- Variable definition errors or missing variable assignments
- Using print() instead of expression for return value
- Incorrect unit conversion (keeping as decimal vs converting to percentage)

---

## Pattern: Robust Data Extraction from Tables

**Description:** Financial calculations from tabular data require careful parsing of table structure, handling of multiple data types, correct indexing, and defensive coding to prevent execution failures.

**When to Use:** Any question providing data in tables (OCR text, exhibits) that must be extracted and used in calculations, especially when code execution failures occur.

**Procedure:**
1. Parse table data into appropriate Python data structures (lists, dictionaries, or named tuples)
2. Use clear variable names that match the problem domain
3. Verify data extraction with intermediate checks (e.g., assert statements or sanity checks)
4. Handle edge cases (missing data, zero values, empty cells)
5. Use try-except blocks for robust error handling if needed
6. Ensure all variables are defined before use
7. Return final result as expression, not print statement

**Code Example:**

**Scenario:** Table with stock returns across states. Extract data and calculate expected return for Stock A.

**Correct Code:**
```python
# Robust table data extraction
# State, Probability, Return_A, Return_B
data = [
    {'state': 1, 'prob': 0.25, 'return_A': 0.08, 'return_B': 0.06},
    {'state': 2, 'prob': 0.40, 'return_A': 0.12, 'return_B': 0.10},
    {'state': 3, 'prob': 0.35, 'return_A': 0.15, 'return_B': 0.14}
]

# Verify probabilities sum to 1 (sanity check)
total_prob = sum(row['prob'] for row in data)
assert abs(total_prob - 1.0) < 0.001, f"Probabilities sum to {total_prob}, not 1.0"

# Calculate expected return for Stock A
expected_return_A = sum(row['prob'] * row['return_A'] for row in data)

# Alternative: using lists
probs = [0.25, 0.40, 0.35]
returns_A = [0.08, 0.12, 0.15]

# Verify same length
assert len(probs) == len(returns_A), "Data length mismatch"

expected_return_A_alt = sum(p * r for p, r in zip(probs, returns_A))

expected_return_A  # Expression
```

**Common Bugs to Avoid:**
- Code execution failure from undefined variables or incorrect indexing
- Hardcoding indices without checking data structure
- Not verifying data integrity (probabilities sum to 1, no missing values)
- Using print() instead of expression for final result
- Inconsistent data types (mixing strings and numbers)
- Off-by-one errors in list indexing
- Not handling None or empty values in parsed data