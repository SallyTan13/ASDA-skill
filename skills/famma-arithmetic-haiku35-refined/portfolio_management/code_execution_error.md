# SKILL PATTERNS FOR PORTFOLIO MANAGEMENT CODE EXECUTION

## Pattern: Time-Weighted Return (TWR) with Cash Flows

**Description:** TWR requires geometric linking of sub-period returns calculated between each cash flow event. The key principle is that each sub-period return measures the investment performance EXCLUDING the impact of cash flows. To isolate performance, calculate the market value immediately BEFORE each cash flow occurs, then use this pre-cash-flow value as the ending value for that sub-period.

**When to Use:** Questions involving portfolio performance measurement with multiple cash flows (contributions/withdrawals) at different dates, when asked to calculate time-weighted return.

**When NOT to Use:**
- When asked for money-weighted return (IRR/internal rate of return)
- When only a single cash flow exists (use simple return formula)
- When cash flows occur at the beginning or end of the entire period only

**Procedure:**
1. **Formula:** TWR = [(1 + r₁) × (1 + r₂) × ... × (1 + rₙ)] - 1
2. **Key principle:** Each sub-period return = (Ending_MV_before_CF - Beginning_MV_after_CF) / Beginning_MV_after_CF
3. Identify all cash flow dates to segment the evaluation period into sub-periods
4. For each sub-period:
   - Beginning value = market value AFTER previous cash flow (or initial value for first period)
   - Ending value = market value BEFORE current cash flow
   - **CRITICAL:** To find pre-cash-flow value: subtract contributions or add back withdrawals from post-cash-flow value
   - **For contributions:** pre_CF_value = post_CF_value - contribution
   - **For withdrawals:** pre_CF_value = post_CF_value + withdrawal
   - Calculate return: r = (Ending_value / Beginning_value) - 1
5. For the final sub-period (after last cash flow to end date):
   - Beginning value = market value AFTER last cash flow
   - Ending value = final market value (no adjustment needed, no cash flow at end)
6. Chain-link all sub-period returns using geometric multiplication: (1+r₁)×(1+r₂)×...×(1+rₙ) - 1
7. Return the final result as a decimal (not percentage), ensuring it's an expression not a print statement

**Example (sanitized):**
> **Scenario:** Portfolio starts at $500,000 on Jan 1. On Mar 1, $50,000 contribution occurs and value becomes $530,000. On Jun 1, $20,000 withdrawal occurs and value becomes $545,000. On Sep 1, $30,000 contribution occurs and value becomes $590,000. Final value on Dec 31 is $610,000. Calculate TWR.
> 
> **Wrong approach:** Using post-cash-flow values directly as ending values without adjustment:
> - Period 1: r₁ = (530,000 / 500,000) - 1 = 0.06 or 6% ← WRONG! Includes contribution impact
> - Period 2: r₂ = (545,000 / 530,000) - 1 = 0.0283 ← WRONG! Includes withdrawal impact
> - Period 3: r₃ = (590,000 / 545,000) - 1 = 0.0826 ← WRONG! Includes contribution impact
> - Period 4: r₄ = (610,000 / 590,000) - 1 = 0.0339
> - TWR = (1.06)(1.0283)(1.0826)(1.0339) - 1 = 0.2278 or 22.78% ← WRONG!
>
> **Correct approach (step-by-step with explicit pre-CF calculations):**
> - **Period 1 (Jan 1 to Mar 1):**
>   - Beginning: $500,000 (initial value)
>   - Post-CF value: $530,000 (given)
>   - Pre-CF value: $530,000 - $50,000 = $480,000 ← Remove contribution
>   - Ending: $480,000 (pre-CF value)
>   - r₁ = (480,000 / 500,000) - 1 = -0.04 or -4%
> 
> - **Period 2 (Mar 1 to Jun 1):**
>   - Beginning: $530,000 (post-CF value from previous period)
>   - Post-CF value: $545,000 (given)
>   - Pre-CF value: $545,000 + $20,000 = $565,000 ← Add back withdrawal
>   - Ending: $565,000 (pre-CF value)
>   - r₂ = (565,000 / 530,000) - 1 = 0.0660 or 6.60%
> 
> - **Period 3 (Jun 1 to Sep 1):**
>   - Beginning: $545,000 (post-CF value from previous period)
>   - Post-CF value: $590,000 (given)
>   - Pre-CF value: $590,000 - $30,000 = $560,000 ← Remove contribution
>   - Ending: $560,000 (pre-CF value)
>   - r₃ = (560,000 / 545,000) - 1 = 0.0275 or 2.75%
> 
> - **Period 4 (Sep 1 to Dec 31):**
>   - Beginning: $590,000 (post-CF value from previous period)
>   - Ending: $610,000 (final value, no adjustment needed)
>   - r₄ = (610,000 / 590,000) - 1 = 0.0339 or 3.39%
> 
> - **TWR calculation:**
>   - TWR = (1 + (-0.04)) × (1 + 0.0660) × (1 + 0.0275) × (1 + 0.0339) - 1
>   - TWR = (0.96) × (1.0660) × (1.0275) × (1.0339) - 1
>   - TWR = 1.0863 - 1 = 0.0863 or 8.63%

**Common Mistakes to Avoid:**
- **CRITICAL: Confusing pre-cash-flow and post-cash-flow values - the post-CF value includes the cash flow, so you must reverse it to get pre-CF value**
- **Using post-CF values as period endings without adjustment - this is the #1 error in TWR calculations**
- **For contributions: pre_CF_value = post_CF_value - contribution (subtract to remove the contribution)**
- **For withdrawals: pre_CF_value = post_CF_value + withdrawal (add back the withdrawal)**
- Using ending values directly without adjusting for cash flows
- Arithmetic averaging of returns instead of geometric linking
- Using beginning-of-period values incorrectly (each sub-period begins with post-cash-flow value from previous period)
- Forgetting that the final period (after last cash flow) uses the final market value directly with no adjustment
- Returning -100.0 or None due to logic errors or using print() instead of expression
- Confusing TWR with money-weighted return (IRR)
- Incorrectly adding cash flows when they should be subtracted (or vice versa)
- Not clearly labeling which values are pre-CF vs post-CF in code comments
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

**Description:** Portfolio standard deviation requires calculating the portfolio return in each state, then computing the probability-weighted variance of these portfolio returns. This is the ONLY correct approach when given discrete probability distributions. Do NOT attempt to decompose into individual security variances and covariances unless explicitly calculating from the discrete distribution first.

**When to Use:** Questions asking for portfolio standard deviation or variance when given discrete probability distributions for individual securities and portfolio weights.

**When NOT to Use:** 
- When the question provides individual asset variances/standard deviations and asks to calculate them separately (not portfolio level)
- When asked to calculate firm-specific variance or residual variance in a market model context
- When the calculation involves decomposing total variance into systematic and unsystematic components

**Procedure:**
1. **Formula:** σₚ = √[Σ pᵢ(Rₚᵢ - E[Rₚ])²], where Rₚᵢ = Σ wⱼRⱼᵢ
2. For each state i, calculate portfolio return: Rₚᵢ = w₁R₁ᵢ + w₂R₂ᵢ + ... (weighted sum of security returns)
3. Calculate expected portfolio return: E[Rₚ] = Σ pᵢRₚᵢ
4. Calculate portfolio variance: Var(Rₚ) = Σ pᵢ(Rₚᵢ - E[Rₚ])²
5. Calculate portfolio standard deviation: σₚ = √Var(Rₚ)
6. Return as expression (not 0.0 or None from print statement)

**Common Mistakes to Avoid:**
- Returning 0.0 because of print() statement instead of expression
- Trying to use portfolio variance formula (w²σ² + ...) without covariance when only state-by-state returns are given
- **CRITICAL: Do NOT use this pattern to calculate individual asset standard deviations - only for portfolio-level calculations**
- **Do NOT attempt to decompose variance using β² × market_variance when calculating total standard deviation from given variance**
- Forgetting to weight returns by portfolio weights in each state
- Not taking square root of variance to get standard deviation
- Missing import of math module for sqrt function

**Example (sanitized):**
> **Scenario:** Portfolio with 70% in Stock M and 30% in Stock N. State 1 (p=0.3, M=5%, N=7%), State 2 (p=0.7, M=10%, N=12%). Calculate portfolio standard deviation.
> **Wrong approach:** Attempting to use individual asset variances with correlation formulas when state-by-state returns are provided.
> **Correct approach:** Calculate portfolio return in each state (0.7×M + 0.3×N), find expected portfolio return, then calculate variance across states using probability weights.

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

**Description:** EWMA (Exponentially Weighted Moving Average) updates require applying the recursive formula to variance/covariance, handling zero returns correctly, and using the CORRECT volatilities in final correlation calculation. The correlation formula uses OLD volatilities in the denominator: Corrₙ = Covₙ/(σₓ,ₙ₋₁ × σᵧ,ₙ₋₁), NOT the newly updated volatilities.

**When to Use:** Questions involving EWMA or GARCH models for updating volatility estimates, correlation estimates, or covariance between assets given lambda parameter and new return observations.

**When NOT to Use:**
- When calculating correlation from scratch (not updating an existing correlation)
- When the question asks for portfolio-level correlation using discrete probability distributions
- When correlation is given directly and no update is required

**Procedure:**
1. **Formula:** σₙ² = λσₙ₋₁² + (1-λ)rₙ₋₁²; Covₙ = λCovₙ₋₁ + (1-λ)rₓ,ₙ₋₁rᵧ,ₙ₋₁; **Corrₙ = Covₙ/(σₓ,ₙ₋₁ × σᵧ,ₙ₋₁)**
2. Calculate returns from price changes: r = (P_new - P_old) / P_old
3. Update variance for each asset: variance_new = λ × variance_old + (1-λ) × return²
4. Update covariance: covariance_new = λ × covariance_old + (1-λ) × return_x × return_y
5. **CRITICAL:** For correlation calculation, use OLD volatilities (σₙ₋₁), not newly updated volatilities
6. Calculate new correlation: correlation_new = covariance_new / (volatility_x_old × volatility_y_old)
7. **Note:** New volatilities (√variance_new) may be calculated for other purposes, but NOT for the correlation denominator

**Code Example:**

**Scenario:** Stock X: yesterday $100, today $98, old volatility 2%/day. Stock Y: yesterday $50, today $50, old volatility 1.5%/day. Old correlation 0.65. Lambda = 0.95. Update correlation.

**Correct Code:**
```python
import math

# Parameters
lambda_param = 0.95

# Stock X
x_price_old = 100
x_price_new = 98
x_vol_old = 0.02  # 2% as decimal
x_return = (x_price_new - x_price_old) / x_price_old

# Stock Y
y_price_old = 50
y_price_new = 50
y_vol_old = 0.015  # 1.5% as decimal
y_return = (y_price_new - y_price_old) / y_price_old  # = 0

# Old covariance from old correlation
cov_old = 0.65 * x_vol_old * y_vol_old

# Update variances (for completeness, though not needed for correlation)
x_var_new = lambda_param * (x_vol_old ** 2) + (1 - lambda_param) * (x_return ** 2)
y_var_new = lambda_param * (y_vol_old ** 2) + (1 - lambda_param) * (y_return ** 2)

# Update covariance (handles zero return correctly)
cov_new = lambda_param * cov_old + (1 - lambda_param) * x_return * y_return

# CRITICAL: Use OLD volatilities in correlation denominator
corr_new = cov_new / (x_vol_old * y_vol_old)

corr_new  # Expression
```

**Common Mistakes to Avoid:**
- **CRITICAL ERROR: Using NEW updated volatilities in correlation denominator instead of OLD volatilities**
- The correlation update formula requires OLD volatilities: Corrₙ = Covₙ/(σₓ,ₙ₋₁ × σᵧ,ₙ₋₁)
- Calculating new volatilities (√variance_new) and then using them in the correlation formula
- Incorrectly handling zero returns (they still affect variance/covariance updates)
- Forgetting to convert volatility to variance before updating (must square)
- Wrong order of operations (update covariance first, then calculate correlation with OLD volatilities)
- Confusing lambda weighting (old values get λ, new observations get 1-λ)

**Example (sanitized):**
> **Scenario:** Asset A drops 2%, Asset B unchanged. Old volatilities: A=1.8%, B=1.2%. Old correlation=0.70. Lambda=0.94. Update correlation.
> **Wrong approach:** Calculating new volatilities from updated variances, then using corr_new = cov_new / (vol_A_new × vol_B_new). This violates the EWMA correlation formula.
> **Correct approach:** Update covariance using EWMA formula, then divide by the product of OLD volatilities: corr_new = cov_new / (vol_A_old × vol_B_old).
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

## Pattern: Market Model Variance Decomposition

**Description:** In a market model (R = α + βR_M + e), total variance decomposes into systematic variance (β² × Var(R_M)) and firm-specific variance (Var(e)). When given total variance and asked to find standard deviation, use the total variance directly. Do NOT attempt to subtract systematic variance from total variance unless explicitly asked for firm-specific variance.

**When to Use:** Questions involving market models with beta coefficients, market variance, and firm-specific variance, where you need to calculate total standard deviation of an asset.

**Procedure:**
1. **Formula:** Var(R) = β² × Var(R_M) + Var(e); σ(R) = √Var(R)
2. Identify what is being asked: total standard deviation vs. firm-specific variance
3. If total standard deviation is requested and total variance is given, use: σ = √Var(R)
4. If firm-specific variance is requested: Var(e) = Var(R) - β² × Var(R_M)
5. **CRITICAL CHECK:** Before taking square root, verify the value is positive
6. If calculation yields negative variance, re-examine the formula application
7. Return result as expression

**Common Mistakes to Avoid:**
- **CRITICAL: Confusing total variance with firm-specific variance - they are different components**
- Attempting to calculate firm-specific variance by subtracting when total standard deviation is requested
- Taking square root of negative numbers (indicates formula misapplication)
- Using the wrong variance decomposition formula for the question being asked
- Not recognizing that Var(R) is already the total variance including both systematic and firm-specific components

**Example (sanitized):**
> **Scenario:** Asset has β=1.4, market variance=0.01, and given Var(R)=0.025. Calculate standard deviation of returns.
> **Wrong approach:** Calculating Var(e) = 0.025 - 1.4² × 0.01 = -0.0146, then taking √(-0.0146) yielding complex number.
> **Correct approach:** Since total variance is given as 0.025, standard deviation = √0.025 = 0.158 or 15.8%.

---