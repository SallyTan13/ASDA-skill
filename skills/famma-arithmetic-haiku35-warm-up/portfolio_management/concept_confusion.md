# SKILL PATTERNS FOR PORTFOLIO MANAGEMENT - CONCEPT CONFUSION ERRORS

## Pattern: Performance Attribution Component Isolation

**Description:** Performance attribution requires isolating specific effects (allocation vs. selection) by holding one dimension constant while varying another. Allocation effect measures impact of weight deviations using benchmark returns; selection effect measures impact of return deviations using actual weights.

**When to Use:** Questions asking for "contribution of asset allocation," "selection effect," or "interaction effect" in performance attribution analysis.

**Procedure:**
1. Formula: Allocation Effect = Σ[(w_actual - w_benchmark) × r_benchmark]
2. Identify actual weights, benchmark weights, actual returns, and benchmark returns for each asset class
3. For each asset, compute (weight difference) × (benchmark return)
4. Sum across all assets to get total allocation contribution
5. Return result as decimal or percentage as requested

**Code Example:**

**Scenario:** A fund has 70% stocks (returned 12%) and 30% bonds (returned 4%). Benchmark is 50% stocks (benchmark return 10%) and 50% bonds (benchmark return 5%). Calculate allocation effect.

**Correct Code:**
```python
# Asset allocation effect calculation
actual_weights = {'stocks': 0.70, 'bonds': 0.30}
benchmark_weights = {'stocks': 0.50, 'bonds': 0.50}
benchmark_returns = {'stocks': 0.10, 'bonds': 0.05}

allocation_effect = sum(
    (actual_weights[asset] - benchmark_weights[asset]) * benchmark_returns[asset]
    for asset in actual_weights
)

# Result: (0.70-0.50)*0.10 + (0.30-0.50)*0.05 = 0.02 - 0.01 = 0.01
allocation_effect  # 0.01 or 1%
```

**Common Bugs to Avoid:**
- Using actual returns instead of benchmark returns (confuses allocation with selection effect)
- Computing only weight differences without multiplying by benchmark returns
- Rounding errors causing option mismatch (0.04 vs 0.039999 should both map to 4%)

---

## Pattern: Real vs. Nominal Return Conversion

**Description:** Real returns adjust nominal returns for inflation to reflect purchasing power changes. The Fisher equation approximation subtracts inflation rate from nominal return; exact formula uses (1+nominal)/(1+inflation)-1.

**When to Use:** Questions explicitly asking for "real returns," "inflation-adjusted returns," or providing an "expected inflation rate" alongside return calculations.

**Procedure:**
1. Formula (Approximation): Real Return ≈ Nominal Return - Inflation Rate
2. Formula (Exact): Real Return = (1 + Nominal Return) / (1 + Inflation Rate) - 1
3. Calculate expected nominal return first (if needed from probability distributions)
4. Subtract inflation rate or apply exact formula
5. Return result in requested format (decimal or percentage)

**Code Example:**

**Scenario:** Portfolio has expected nominal return of 11.2% and inflation is expected to be 3.8%. Calculate real return.

**Correct Code:**
```python
# Real return calculation
nominal_return = 0.112
inflation_rate = 0.038

# Approximation method (acceptable for small rates)
real_return_approx = nominal_return - inflation_rate

# Exact Fisher equation (preferred)
real_return_exact = (1 + nominal_return) / (1 + inflation_rate) - 1

# Result: (1.112 / 1.038) - 1 ≈ 0.0713
real_return_exact  # 0.0713 or 7.13%
```

**Common Bugs to Avoid:**
- Returning nominal return when question asks for real return
- Forgetting to apply inflation adjustment when inflation rate is provided
- Using addition instead of division in exact formula

---

## Pattern: Portfolio Variance with Infinite Diversification

**Description:** As portfolio size approaches infinity with equal weights, idiosyncratic risk (residual variance) diversifies to zero, leaving only systematic risk equal to β² × σ²_market. This applies to single-factor models where returns follow R_i = α + β_i × R_M + ε_i.

**When to Use:** Questions about "infinite number of assets," "fully diversified portfolio," or "systematic risk only" in factor model contexts.

**Procedure:**
1. Formula: Var(infinite portfolio) = β² × Var(market)
2. Identify the asset's beta coefficient
3. Identify market variance (or standard deviation to be squared)
4. Square beta and multiply by market variance
5. Recognize that Var(ε) terms vanish with infinite diversification

**Code Example:**

**Scenario:** Asset D has beta of 1.3, idiosyncratic variance of 0.0196, and market variance is 0.0144. Calculate variance of infinite portfolio of asset D.

**Correct Code:**
```python
# Infinite portfolio variance (systematic risk only)
beta_D = 1.3
var_market = 0.0144
var_idiosyncratic = 0.0196  # This diversifies away

# Only systematic risk remains
var_infinite_portfolio = (beta_D ** 2) * var_market

# Result: (1.3)^2 * 0.0144 = 1.69 * 0.0144 = 0.024336
var_infinite_portfolio  # 0.024336
```

**Common Bugs to Avoid:**
- Returning market variance directly (ignores beta scaling)
- Including idiosyncratic variance in final answer (fails to recognize diversification)
- Forgetting to square beta before multiplying by market variance

---

## Pattern: After-Tax Rebalancing Range Adjustment

**Description:** Capital gains taxes create asymmetric transaction costs that widen rebalancing ranges. Upper bound increases because selling appreciated assets incurs tax; lower bound decreases because buying doesn't trigger tax on that position.

**When to Use:** Questions about "after-tax rebalancing range," "tax-adjusted corridor," or converting pre-tax bands to after-tax bands given capital gains tax rates.

**Procedure:**
1. Formula: Lower_after = Target - (Target - Lower_pre) / (1 - Tax_rate)
2. Formula: Upper_after = Target + (Upper_pre - Target) / (1 - Tax_rate)
3. Identify target allocation, pre-tax range bounds, and tax rate
4. Apply formulas to expand range away from target
5. Verify that after-tax range is wider than pre-tax range

**Code Example:**

**Scenario:** Asset has 10% target allocation, pre-tax range of 6% to 14%, and 25% capital gains tax. Calculate after-tax range.

**Correct Code:**
```python
# After-tax rebalancing range calculation
target = 0.10
lower_pre = 0.06
upper_pre = 0.14
tax_rate = 0.25

# Tax widens the range (makes rebalancing more expensive)
lower_after = target - (target - lower_pre) / (1 - tax_rate)
upper_after = target + (upper_pre - target) / (1 - tax_rate)

# Result: 0.10 - (0.04/0.75) = 0.10 - 0.0533 = 0.0467
# Result: 0.10 + (0.04/0.75) = 0.10 + 0.0533 = 0.1533
(lower_after, upper_after)  # (0.0467, 0.1533) or 4.67% to 15.33%
```

**Common Bugs to Avoid:**
- Narrowing the range instead of widening (using multiplication instead of division)
- Applying tax rate symmetrically to both bounds
- Using (1 + tax_rate) instead of (1 - tax_rate) in denominator

---

## Pattern: Factor Model Systematic Risk Decomposition

**Description:** In factor models, systematic risk refers to return variance explained by factor exposures (β² × σ²_factor), not the immediate return impact from factor surprises. Total variance = systematic variance + idiosyncratic variance.

**When to Use:** Questions asking for "systematic risk," "factor-related variance," or "explained variance" in multi-factor or single-factor model contexts.

**Procedure:**
1. Formula: Systematic Variance = Σ(β_i² × Var(Factor_i)) for independent factors
2. Identify all factor betas and factor variances
3. Square each beta and multiply by corresponding factor variance
4. Sum across all factors if multiple factors exist
5. Return variance (or standard deviation if requested)

**Code Example:**

**Scenario:** Stock has beta of 1.4 to market factor (variance 0.0225) and beta of 0.6 to size factor (variance 0.0100). Factors are independent. Calculate systematic variance.

**Correct Code:**
```python
# Systematic risk calculation in multi-factor model
beta_market = 1.4
var_market = 0.0225
beta_size = 0.6
var_size = 0.0100

# Systematic variance from both factors (assuming independence)
systematic_variance = (beta_market ** 2) * var_market + (beta_size ** 2) * var_size

# Result: (1.4^2 * 0.0225) + (0.6^2 * 0.0100) = 0.0441 + 0.0036 = 0.0477
systematic_variance  # 0.0477
```

**Common Bugs to Avoid:**
- Calculating return surprise (beta × factor_change) instead of variance
- Returning only market variance without beta scaling
- Confusing systematic risk (variance) with systematic return (expected factor contribution)

---

## Pattern: Zero-Variance Portfolio Construction with Perfect Negative Correlation

**Description:** When two assets have perfect negative correlation (ρ=-1), a zero-variance portfolio can be constructed with weights proportional to the inverse of standard deviations. By no-arbitrage, this risk-free portfolio must earn the risk-free rate.

**When to Use:** Questions about "risk-free rate" given two assets with correlation=-1, or "constructing risk-free portfolio" from negatively correlated assets.

**Procedure:**
1. Formula: w_A = σ_B / (σ_A + σ_B), w_B = σ_A / (σ_A + σ_B) when ρ=-1
2. Formula: r_f = w_A × E(R_A) + w_B × E(R_B)
3. Calculate weights that eliminate variance (inverse proportion to std devs)
4. Compute weighted average return of this zero-variance portfolio
5. This return equals the risk-free rate by arbitrage

**Code Example:**

**Scenario:** Stock X has E(R)=12%, σ=8%; Stock Y has E(R)=18%, σ=12%; correlation=-1. Find risk-free rate.

**Correct Code:**
```python
# Risk-free rate from perfect negative correlation
E_R_X = 0.12
sigma_X = 0.08
E_R_Y = 0.18
sigma_Y = 0.12
correlation = -1

# Weights for zero-variance portfolio (inverse to std devs)
w_X = sigma_Y / (sigma_X + sigma_Y)
w_Y = sigma_X / (sigma_X + sigma_Y)

# Risk-free rate = weighted average return
risk_free_rate = w_X * E_R_X + w_Y * E_R_Y

# Result: (12/20)*0.12 + (8/20)*0.18 = 0.072 + 0.072 = 0.144
risk_free_rate  # 0.144 or 14.4%
```

**Common Bugs to Avoid:**
- Using equal weights instead of variance-minimizing weights
- Applying standard portfolio variance formula (unnecessary when ρ=-1)
- Not recognizing that zero-variance portfolio must earn risk-free rate

---

## Pattern: CAPM Mispricing Detection

**Description:** CAPM equilibrium requires E(R_i) = R_f + β_i × [E(R_M) - R_f]. Assets where actual expected return differs from required return are mispriced. Rational investors avoid assets with E(R) < required return (insufficient compensation for risk).

**When to Use:** Questions asking which asset "will not be held," "is overpriced," or "offers insufficient return" given risk-free rate, market return, and asset betas.

**Procedure:**
1. Formula: Required Return = R_f + β × (E(R_M) - R_f)
2. Calculate required return for each asset using CAPM
3. Compare given expected return to required return
4. Asset is mispriced if E(R_actual) ≠ Required Return
5. Underpriced if E(R) > Required; overpriced if E(R) < Required

**Code Example:**

**Scenario:** R_f=4%, E(R_M)=11%. Asset P: β=0.9, E(R)=10.5%. Asset Q: β=1.3, E(R)=12%. Which is mispriced?

**Correct Code:**
```python
# CAPM mispricing detection
R_f = 0.04
E_R_M = 0.11
market_premium = E_R_M - R_f

# Asset P
beta_P = 0.9
E_R_P = 0.105
required_P = R_f + beta_P * market_premium

# Asset Q
beta_Q = 1.3
E_R_Q = 0.12
required_Q = R_f + beta_Q * market_premium

# Check mispricing
mispriced_P = abs(E_R_P - required_P) > 0.001
mispriced_Q = abs(E_R_Q - required_Q) > 0.001

# Result: required_P = 0.04 + 0.9*0.07 = 0.103 (P fairly priced)
# Result: required_Q = 0.04 + 1.3*0.07 = 0.131 (Q underpriced, E(R) < required)
('Q', required_Q, E_R_Q)  # Q will not be held (offers 12% vs 13.1% required)
```

**Common Bugs to Avoid:**
- Comparing returns without calculating CAPM required return
- Confusing beta with expected return
- Not recognizing that E(R) < Required means asset won't be held

---

## Pattern: Arrival Cost Calculation in Trade Execution

**Description:** Arrival cost measures execution quality relative to the decision price (when portfolio manager decided to trade), not the release price or any other benchmark. It captures total implementation shortfall from decision to execution.

**When to Use:** Questions about "arrival cost," "implementation shortfall," or "execution cost" when decision price, execution prices, and shares are provided.

**Procedure:**
1. Formula: Arrival Cost = (Avg Execution Price - Decision Price) / Decision Price
2. Identify decision price (when PM decided to trade)
3. Calculate weighted average execution price across all fills
4. Compute percentage difference from decision price
5. Convert to basis points if requested (multiply by 10,000)

**Code Example:**

**Scenario:** PM decided to buy 2,000 shares at decision price $50.00. Executed: 800 shares at $50.20, 1,200 shares at $50.35. Calculate arrival cost in bp.

**Correct Code:**
```python
# Arrival cost calculation
decision_price = 50.00
executions = [(800, 50.20), (1200, 50.35)]

# Weighted average execution price
total_shares = sum(shares for shares, price in executions)
avg_execution_price = sum(shares * price for shares, price in executions) / total_shares

# Arrival cost (relative to decision price)
arrival_cost_pct = (avg_execution_price - decision_price) / decision_price
arrival_cost_bp = arrival_cost_pct * 10000

# Result: avg = (800*50.20 + 1200*50.35)/2000 = 50.29
# Result: (50.29 - 50.00)/50.00 * 10000 = 58 bp
arrival_cost_bp  # 58 basis points
```

**Common Bugs to Avoid:**
- Using release price or first execution price instead of decision price
- Not weighting execution prices by share quantities
- Forgetting to convert to basis points (multiply by 10,000)

---

## Pattern: Confidence Index Calculation and Interpretation

**Description:** Confidence index = (High-grade bond yield) / (Lower-grade bond yield). A falling index (narrowing spread) paradoxically indicates decreasing investor confidence, as investors demand less premium for risk, often preceding economic weakness.

**When to Use:** Questions asking whether "confidence index is rising or falling" or to "calculate confidence index" given yields on different credit quality bonds.

**Procedure:**
1. Formula: Confidence Index = Yield_high_grade / Yield_lower_grade
2. Calculate index for current period and prior period
3. Compare: falling index means spread narrowing (lower-grade yields falling faster)
4. Interpret: falling index = decreasing confidence (counterintuitive)
5. Return directional statement and/or numeric values

**Code Example:**

**Scenario:** Last year: AAA yield 6%, BBB yield 8%. This year: AAA yield 5.5%, BBB yield 7%. Is confidence rising or falling?

**Correct Code:**
```python
# Confidence index calculation
AAA_last = 0.06
BBB_last = 0.08
AAA_this = 0.055
BBB_this = 0.07

confidence_last = AAA_last / BBB_last
confidence_this = AAA_this / BBB_this

# Determine direction
confidence_change = confidence_this - confidence_last
direction = "rising" if confidence_change > 0 else "falling"

# Result: last = 0.75, this = 0.786, rising
# Interpretation: rising index = increasing confidence
(direction, confidence_this, confidence_last)  # ('rising', 0.786, 0.75)
```

**Common Bugs to Avoid:**
- Inverting the ratio (lower-grade / high-grade)
- Misinterpreting direction (falling index = decreasing confidence)
- Calculating spread instead of ratio

---

## Pattern: Futures Position P&L Calculation

**Description:** Futures position change equals (number of contracts) × (contract multiplier) × (index point change). This is distinct from hedge ratio calculation, which uses portfolio beta to determine how many contracts to trade.

**When to Use:** Questions asking "by how much does the futures position change" given index point movement and contract specifications.

**Procedure:**
1. Formula: P&L = Number_of_Contracts × Multiplier × Point_Change
2. Identify contract multiplier (e.g., $250 for S&P 500 futures)
3. Identify index point change (not percentage)
4. Determine number of contracts (may need to calculate from hedge ratio first)
5. Multiply all three components for total P&L

**Code Example:**

**Scenario:** Investor holds 5 S&P 500 futures contracts (multiplier $250). Index falls 60 points. Calculate position change.

**Correct Code:**
```python
# Futures position P&L
num_contracts = 5
multiplier = 250  # $ per index point for S&P 500
point_change = -60  # negative for decline

# Direct P&L calculation
position_change = num_contracts * multiplier * point_change

# Result: 5 * 250 * (-60) = -75,000
position_change  # -$75,000 (loss)
```

**Common Bugs to Avoid:**
- Confusing hedge ratio calculation with P&L calculation
- Using portfolio value and beta instead of contracts × multiplier × points
- Forgetting negative sign for index declines

---

## Pattern: International Tax Methods - Deduction vs. Credit vs. Exemption

**Description:** Three methods for taxing foreign income: (1) Exemption: no domestic tax on foreign income; (2) Credit: foreign tax credited against domestic tax; (3) Deduction: foreign tax deductible from taxable income before applying domestic rate. Deduction method results in total tax = Foreign_Tax + Domestic_Rate × (Income - Foreign_Tax).

**When to Use:** Questions about "deduction method," "credit method," or "effective tax rate" when taxpayer earns income in foreign jurisdiction with different tax rate.

**Procedure:**
1. Exemption: Total Tax = Foreign_Tax_Rate × Income
2. Credit: Total Tax = max(Domestic_Rate, Foreign_Rate) × Income
3. Deduction: Total Tax = Foreign_Tax + Domestic_Rate × (Income - Foreign_Tax)
4. Identify which method applies from question context
5. Calculate total effective tax rate

**Code Example:**

**Scenario:** Investor earns $100K in Country F (tax rate 18%), resident of Country D (tax rate 12%). Country D uses deduction method. Calculate total tax rate.

**Correct Code:**
```python
# Deduction method tax calculation
income = 100000
foreign_rate = 0.18
domestic_rate = 0.12

# Foreign tax paid
foreign_tax = income * foreign_rate

# Domestic tax on (income - foreign tax paid)
taxable_domestic = income - foreign_tax
domestic_tax = taxable_domestic * domestic_rate

# Total tax and effective rate
total_tax = foreign_tax + domestic_tax
effective_rate = total_tax / income

# Result: 18000 + (82000 * 0.12) = 18000 + 9840 = 27840
# Effective rate: 27.84%
effective_rate  # 0.2784 or 27.84%
```

**Common Bugs to Avoid:**
- Confusing deduction method with credit method (deduction doesn't eliminate double taxation)
- Assuming exemption when deduction method applies
- Calculating foreign_tax × domestic_rate instead of (income - foreign_tax) × domestic_rate

---

## Pattern: Information Ratio Calculation

**Description:** Information Ratio measures active management skill as alpha (excess return above benchmark) divided by tracking error (residual standard deviation). IR = (R_p - R_benchmark) / σ_residual, where benchmark return should match portfolio's systematic risk exposure.

**When to Use:** Questions asking for "information ratio," "risk-adjusted alpha," or "active management skill" when portfolio returns, benchmark returns, beta, and residual risk are provided.

**Procedure:**
1. Formula: IR = (R_portfolio - β × R_benchmark) / σ_residual
2. Calculate alpha = Portfolio Return - (β × Benchmark Return)
3. Identify residual standard deviation (tracking error)
4. Divide alpha by residual standard deviation
5. Do not use total standard deviation or risk-free rate

**Code Example:**

**Scenario:** Portfolio return 16%, beta 1.2, market return 12%, residual std dev 3%. Calculate information ratio.

**Correct Code:**
```python
# Information ratio calculation
R_portfolio = 0.16
beta = 1.2
R_market = 0.12
residual_std = 0.03

# Alpha relative to systematic risk
alpha = R_portfolio - (beta * R_market)

# Information ratio = alpha / tracking error
information_ratio = alpha / residual_std

# Result: (0.16 - 1.2*0.12) / 0.03 = (0.16 - 0.144) / 0.03 = 0.016 / 0.03 = 0.533
information_ratio  # 0.533
```

**Common Bugs to Avoid:**
- Using (Portfolio - Risk_free) / Residual_std (that's not IR)
- Dividing by total standard deviation instead of residual standard deviation
- Not adjusting benchmark return by portfolio beta

## Pattern: Portfolio Insurance via Put Option Delta Hedging

**Description:** Portfolio insurance using put options requires holding (1 - |put delta|) in the risky asset and |put delta| in risk-free securities. The put delta is negative, so the risky asset allocation equals (1 + put_delta), not the delta itself.

**When to Use:** Questions asking for "initial portfolio allocation," "risky asset weight," or "risk-free allocation" when implementing portfolio insurance through put options or dynamic hedging strategies.

**Procedure:**
1. Formula: Risky_Asset_Weight = 1 - |Delta_put| = 1 + Delta_put (since Delta_put < 0)
2. Calculate put option delta using Black-Scholes-Merton formula with dividend yield: Delta_put = e^(-qT) × [N(d1) - 1]
3. Compute d1 = [ln(S0/K) + (r - q + σ²/2)T] / (σ√T)
4. The risky asset allocation is (1 + Delta_put); risk-free allocation is -Delta_put = |Delta_put|
5. Return the risky asset weight as a percentage

**Code Example:**

**Scenario:** A portfolio worth $500 million tracks an index at 2000. Manager wants protection against 8% decline over 9 months. Risk-free rate = 5%, dividend yield = 2%, volatility = 25% per annum.

**Correct Code:**
```python
import math
from scipy.stats import norm

# Portfolio and option parameters
portfolio_value = 500_000_000
index_level = 2000
protection_level = 0.92  # protect against 8% decline
T = 9/12  # 9 months in years
r = 0.05
q = 0.02  # dividend yield
sigma = 0.25

# Strike price for put option
K = index_level * protection_level

# Calculate d1 for BSM with dividend yield
d1 = (math.log(index_level / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))

# Put delta (negative value)
put_delta = math.exp(-q * T) * (norm.cdf(d1) - 1)

# Risky asset allocation = 1 + put_delta (since put_delta is negative)
risky_asset_weight = 1 + put_delta

risky_asset_weight  # Result as decimal (e.g., 0.6523 = 65.23%)
```

**Common Bugs to Avoid:**
- Returning put_delta directly instead of (1 + put_delta) for risky asset weight
- Forgetting that put delta is negative; using (1 - put_delta) would give >100% allocation
- Omitting the e^(-qT) factor when dividend yield is present
- Confusing the question asking for risky vs risk-free allocation

---

## Pattern: GARCH Correlation Update via Covariance

**Description:** Updating correlation in GARCH models requires three steps: (1) update variance for asset 1 using GARCH(1,1), (2) update variance for asset 2 using GARCH(1,1), (3) update covariance using GARCH structure on product of returns, then (4) compute new correlation as cov/(σ1×σ2).

**When to Use:** Questions asking to "update correlation" using GARCH or EWMA models when given previous correlation, volatilities, and new price changes for two assets.

**Procedure:**
1. Formula: σ²_new = ω + α×u²_previous + β×σ²_previous (GARCH variance update)
2. Formula: cov_new = ω_cov + α×(u1×u2)_previous + β×cov_previous (GARCH covariance update)
3. Calculate return for each asset: u = (P_new - P_old) / P_old
4. Update variance for asset 1: σ1²_new = ω + α×u1² + β×σ1²_old
5. Update variance for asset 2: σ2²_new = ω + α×u2² + β×σ2²_old
6. Compute old covariance: cov_old = ρ_old × σ1_old × σ2_old
7. Update covariance: cov_new = ω + α×(u1×u2) + β×cov_old
8. New correlation: ρ_new = cov_new / (√σ1²_new × √σ2²_new)

**Code Example:**

**Scenario:** Asset A priced at $50 (unchanged), volatility 2% per day. Asset B priced at $100 yesterday, $98 today, volatility 1.8% per day. Previous correlation = 0.75. GARCH parameters: ω=0.000003, α=0.05, β=0.93.

**Correct Code:**
```python
import math

# Asset parameters
price_A_old = 50
price_A_new = 50
sigma_A_old = 0.02

price_B_old = 100
price_B_new = 98
sigma_B_old = 0.018

rho_old = 0.75

# GARCH parameters
omega = 0.000003
alpha = 0.05
beta = 0.93

# Calculate returns
u_A = (price_A_new - price_A_old) / price_A_old
u_B = (price_B_new - price_B_old) / price_B_old

# Update variances
var_A_old = sigma_A_old ** 2
var_A_new = omega + alpha * (u_A ** 2) + beta * var_A_old

var_B_old = sigma_B_old ** 2
var_B_new = omega + alpha * (u_B ** 2) + beta * var_B_old

# Update covariance
cov_old = rho_old * sigma_A_old * sigma_B_old
cov_new = omega + alpha * (u_A * u_B) + beta * cov_old

# Calculate new correlation
sigma_A_new = math.sqrt(var_A_new)
sigma_B_new = math.sqrt(var_B_new)
rho_new = cov_new / (sigma_A_new * sigma_B_new)

rho_new  # New correlation coefficient
```

**Common Bugs to Avoid:**
- Applying GARCH formula directly to correlation instead of to variances and covariance separately
- Forgetting to convert old correlation to covariance before updating
- Using ω parameter for covariance update without recognizing it applies to variance scale
- Not squaring volatilities when computing variances for GARCH update

---

## Pattern: Futures-Based Portfolio Insurance Hedge Ratio

**Description:** Portfolio insurance using futures requires calculating the number of contracts based on hedge ratio = (Portfolio_Value × Delta_put) / (Futures_Price × Multiplier), where Delta_put is the put option delta that represents the desired hedge.

**When to Use:** Questions asking for "futures position," "number of contracts," or "initial position" when implementing portfolio insurance using index futures instead of options.

**Procedure:**
1. Calculate the put option delta that represents desired protection (as in put option hedging)
2. Determine futures contract value = Futures_Price × Contract_Multiplier
3. Calculate futures price: F = S × e^((r-q)×T_futures) where T_futures is futures maturity
4. Number of contracts = (Portfolio_Value × |Delta_put|) / Futures_Contract_Value
5. Since we're hedging (buying protection), take short position: negative number of contracts
6. Return the number of contracts (negative for short position)

**Code Example:**

**Scenario:** Portfolio worth $400M tracks index at 1500. Want protection against 6% decline over 6 months using 9-month futures. Risk-free rate = 4%, dividend yield = 2.5%, volatility = 28%. Index futures multiplier = $250.

**Correct Code:**
```python
import math
from scipy.stats import norm

# Portfolio parameters
portfolio_value = 400_000_000
index_level = 1500
protection_level = 0.94  # protect against 6% decline
T_protection = 6/12  # 6 months protection
T_futures = 9/12  # 9 month futures
r = 0.04
q = 0.025
sigma = 0.28
multiplier = 250

# Calculate put delta for desired protection
K = index_level * protection_level
d1 = (math.log(index_level / K) + (r - q + 0.5 * sigma**2) * T_protection) / (sigma * math.sqrt(T_protection))
put_delta = math.exp(-q * T_protection) * (norm.cdf(d1) - 1)

# Calculate futures price
futures_price = index_level * math.exp((r - q) * T_futures)

# Futures contract value
contract_value = futures_price * multiplier

# Number of contracts (negative for short/hedge position)
num_contracts = (portfolio_value * put_delta) / contract_value

# Round to nearest integer (can't trade fractional contracts)
num_contracts_rounded = round(num_contracts)

num_contracts_rounded  # Negative number indicates short position
```

**Common Bugs to Avoid:**
- Using Black-Scholes option pricing formulas instead of hedge ratio calculation
- Forgetting to calculate futures price with cost-of-carry (using spot index level instead)
- Using option maturity instead of futures maturity for futures pricing
- Not recognizing that portfolio insurance requires short futures position (negative contracts)
- Dividing by spot index level instead of futures contract value

---

## Pattern: Trade Execution Cost Components

**Description:** Trading costs in execution analysis consist of commissions plus market impact (execution price - decision price), excluding delay costs and opportunity costs. Total implementation shortfall includes all components, but "trading cost" is a specific subset.

**When to Use:** Questions asking for "trading cost," "execution cost," or cost breakdown when given decision price, execution prices, shares traded, and commissions.

**Procedure:**
1. Formula: Trading_Cost = Commission + Market_Impact
2. Formula: Market_Impact = (Avg_Execution_Price - Decision_Price) × Shares_Executed
3. Identify decision price (when PM decided to trade)
4. Calculate weighted average execution price for executed shares
5. Market impact = (Avg_Execution_Price - Decision_Price) × Shares_Executed
6. Add commissions to get total trading cost
7. If question asks for subset of shares, allocate proportionally

**Code Example:**

**Scenario:** PM decides to buy 4000 shares at decision price $45.00. Executions: 1000 shares at $45.20, 1500 shares at $45.35, 1000 shares at $45.50. Total commissions = $180. Question asks for trading cost of first 2500 shares.

**Correct Code:**
```python
# Trade parameters
decision_price = 45.00
executions = [
    {'shares': 1000, 'price': 45.20},
    {'shares': 1500, 'price': 45.35},
    {'shares': 1000, 'price': 45.50}
]
total_commissions = 180
shares_of_interest = 2500  # First 2500 shares

# Calculate for the shares of interest (first 2500)
relevant_executions = [
    {'shares': 1000, 'price': 45.20},
    {'shares': 1500, 'price': 45.35}
]

# Weighted average execution price for these shares
total_shares = sum(e['shares'] for e in relevant_executions)
weighted_price = sum(e['shares'] * e['price'] for e in relevant_executions) / total_shares

# Market impact cost
market_impact = (weighted_price - decision_price) * total_shares

# Allocate commissions proportionally
total_executed = sum(e['shares'] for e in executions)
allocated_commission = total_commissions * (total_shares / total_executed)

# Total trading cost
trading_cost = market_impact + allocated_commission

trading_cost  # Trading cost for the specified shares
```

**Common Bugs to Avoid:**
- Including delay cost (decision price - release price) in trading cost calculation
- Including opportunity cost of unexecuted shares in trading cost
- Using total implementation shortfall instead of just commission + market impact
- Not allocating commissions proportionally when question asks for subset of shares
- Using release price instead of decision price as the benchmark