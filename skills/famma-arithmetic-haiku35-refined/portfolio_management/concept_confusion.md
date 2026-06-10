# SKILL PATTERNS FOR PORTFOLIO MANAGEMENT - CONCEPT CONFUSION ERRORS

## Pattern: Performance Attribution Component Isolation

**Description:** Performance attribution requires isolating specific effects (allocation vs. selection) by holding one dimension constant while varying another. Allocation effect measures impact of weight deviations using benchmark returns; selection effect measures impact of return deviations using actual weights. Results must be properly rounded to match multiple-choice options, as floating-point arithmetic can produce values like 3.9999999999999996 instead of 4.0.

**When to Use:** Questions asking for "contribution of asset allocation," "selection effect," or "interaction effect" in performance attribution analysis.

**Procedure:**
1. Formula: Allocation Effect = Σ[(w_actual - w_benchmark) × r_benchmark]
2. Identify actual weights, benchmark weights, actual returns, and benchmark returns for each asset class
3. For each asset, compute (weight difference) × (benchmark return)
4. Sum across all assets to get total allocation contribution
5. **CRITICAL: Round result appropriately before matching to options** - Use `round(result * 100, 1)` for percentages or tolerance-based matching
6. Return result as decimal or percentage as requested

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

# Round to handle floating-point precision before matching to options
allocation_effect_pct = round(allocation_effect * 100, 1)  # 1.0%

allocation_effect_pct  # 1.0 (matches to 1% option)
```

**Common Bugs to Avoid:**
- Using actual returns instead of benchmark returns (confuses allocation with selection effect)
- Computing only weight differences without multiplying by benchmark returns
- **Not rounding before option matching** - Floating-point errors like 3.9999999999999996 should map to 4%, not 3%
- Using simple equality checks instead of tolerance-based matching for floating-point results

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

**When NOT to Use:** 
- When question asks about a specific finite number of assets
- When multiple assets with different characteristics are being combined
- When the question asks about total portfolio variance (not just systematic component)

**Procedure:**
1. **CRITICAL: Identify the correct asset** - Read the question carefully to determine which asset's parameters to use
2. Formula: Var(infinite portfolio) = β² × Var(market)
3. Extract the specified asset's beta coefficient from the data
4. Identify market variance (or standard deviation to be squared)
5. Square beta and multiply by market variance
6. Recognize that Var(ε) terms vanish with infinite diversification

**Common Mistakes to Avoid:**
- **Using wrong asset parameters** - Always verify you're using the asset specified in the question
- Returning market variance directly (ignores beta scaling)
- Including idiosyncratic variance in final answer (fails to recognize diversification)
- Forgetting to square beta before multiplying by market variance
- Confusing Asset A, B, C labels - double-check which asset the question asks about

**Example (sanitized):**
> **Scenario:** Three assets exist: Asset X (beta=0.6, idiosyncratic variance=0.008), Asset Y (beta=1.1, idiosyncratic variance=0.015), Asset Z (beta=1.4, idiosyncratic variance=0.020). Market variance is 0.0100. Calculate variance of infinite portfolio of Asset X.
> 
> **Wrong approach:** Use Asset Z parameters: (1.4)² × 0.0100 = 0.0196
> 
> **Correct approach:**
> 1. Question asks for Asset X specifically
> 2. Use Asset X beta = 0.6
> 3. Systematic variance = (0.6)² × 0.0100 = 0.36 × 0.0100 = 0.0036
> 4. Idiosyncratic variance (0.008) diversifies away with infinite assets

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

**Description:** In factor models, systematic risk refers to return variance explained by factor exposures (β² × σ²_factor), not the immediate return impact from factor surprises. Total variance = systematic variance + idiosyncratic variance. This is fundamentally different from calculating systematic return contribution, which uses β × factor_change. When questions ask for "total volatility" or "portfolio variance" in a factor model context, include both systematic and residual components.

**When to Use:** 
- Questions asking for "systematic risk," "factor-related variance," "explained variance," or "systematic component of variance" → calculate ONLY systematic variance
- Questions asking for "total volatility," "portfolio variance," "asset variance," or "total risk" in factor model context → calculate systematic variance + residual variance
- Do NOT use this pattern when questions ask for "return contribution," "factor impact on return," or "expected return from factors" (those use β × factor_change)

**Procedure:**
1. **Identify what the question is asking for:**
   - Keywords "systematic risk/variance/volatility" → calculate only systematic component
   - Keywords "total risk/variance/volatility," "portfolio variance," "asset variance" → calculate systematic + residual
2. Formula: Systematic Variance = Σ(β_i² × Var(Factor_i)) for independent factors
3. Identify all factor betas and factor variances (NOT factor changes or surprises)
4. Square each beta and multiply by corresponding factor variance
5. Sum across all factors if multiple factors exist
6. **If question asks for total variance:** Add residual/idiosyncratic variance to systematic variance
7. **If question asks for volatility/standard deviation:** Take square root of variance
8. Return variance or standard deviation as requested
9. CRITICAL: Do NOT calculate β × Δfactor (that's return contribution, not risk)

**Example (sanitized):**
> **Scenario 1:** A stock has beta of 0.9 to a market factor (variance 0.0225) and beta of 1.1 to a size factor (variance 0.0144). Factors are independent. The market factor had a surprise of +3% and size factor had a surprise of -2%. Residual variance is 0.0100. Question asks: "What is the systematic risk of the stock?"
> 
> **Wrong approach:** Calculate return contribution: (0.9 × 0.03) + (1.1 × -0.02) = 0.027 - 0.022 = 0.005 or 0.5%. This confuses systematic RETURN with systematic RISK.
> 
> **Correct approach:** 
> 1. Question asks for "systematic risk" → calculate only systematic variance
> 2. Systematic variance = (β_market² × Var_market) + (β_size² × Var_size)
> 3. = (0.9² × 0.0225) + (1.1² × 0.0144)
> 4. = (0.81 × 0.0225) + (1.21 × 0.0144)
> 5. = 0.018225 + 0.017424 = 0.035649 or 3.56%
> 6. Ignore factor surprises and residual variance entirely
>
> **Scenario 2:** Same setup, but question asks: "What is the total volatility of the stock?"
> 
> **Correct approach:**
> 1. Question asks for "total volatility" → calculate systematic + residual variance, then take square root
> 2. Systematic variance = 0.035649 (from above)
> 3. Total variance = systematic + residual = 0.035649 + 0.0100 = 0.045649
> 4. Total volatility = √0.045649 = 0.2137 or 21.37%
> 5. Must include residual variance when asking for "total" risk

**Common Mistakes to Avoid:**
- Calculating return surprise (beta × factor_change) instead of variance (beta² × factor_variance)
- Using factor changes/surprises when calculating systematic risk (factor surprises are for return attribution, not risk)
- Returning only market variance without beta scaling
- Confusing systematic risk (variance) with systematic return (expected factor contribution)
- Using β instead of β² in the calculation
- **Excluding residual variance when question asks for "total" volatility/variance/risk**
- **Including residual variance when question asks specifically for "systematic" component only**
- Not taking square root when question asks for volatility/standard deviation vs variance

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

**Description:** CAPM equilibrium requires E(R_i) = R_f + β_i × [E(R_M) - R_f]. Assets where actual expected return differs from required return are mispriced. When arbitrage opportunities exist, construct a replicating portfolio with the same beta using available assets, then calculate arbitrage profit as the return difference between the mispriced asset and the replicating portfolio. **CRITICAL: This pattern requires ALL CAPM parameters (R_f, E(R_M), betas, and expected returns) to be explicitly provided. If any parameter is missing, use the system of equations pattern instead.**

**When to Use:** Questions asking which asset "will not be held," "is overpriced," or "offers insufficient return" given **explicitly provided** risk-free rate, market return, and asset betas. Also use when questions ask about "arbitrage opportunity," "arbitrage strategy," or "arbitrage profit" involving mispriced portfolios **when all CAPM parameters are given**.

**When NOT to Use:**
- **When risk-free rate OR market return is not explicitly provided** - Use "Solving for CAPM Parameters via System of Equations" pattern instead
- When question asks to calculate market return or risk-free rate from asset data (use system of equations)
- When only two assets are given without explicit risk-free rate or market return
- When question asks "what is the expected return on the market" or "what is the risk-free rate" (these are solving problems, not mispricing detection)

**Procedure:**
1. **CRITICAL: Verify ALL parameters are explicitly given** - Check that R_f, E(R_M), all betas, and all expected returns are provided in the problem
2. **If R_f or E(R_M) is missing:** STOP - Use system of equations pattern instead
3. Formula: Required Return = R_f + β × (E(R_M) - R_f)
4. Calculate required return for each asset using CAPM
5. Compare given expected return to required return
6. Asset is mispriced if E(R_actual) ≠ Required Return
7. Underpriced if E(R) > Required; overpriced if E(R) < Required
8. **Return the asset name/identifier, not a dictionary or intermediate calculation**
9. For arbitrage questions: Construct replicating portfolio with same beta as mispriced asset
10. Replicating portfolio: w_risky × β_risky + w_rf × 0 = β_target, where w_risky + w_rf = 1
11. Replicating return: w_risky × E(R_risky) + w_rf × R_f
12. Arbitrage profit: E(R_mispriced) - E(R_replicating)
13. Strategy: Long underpriced, short replicating (or vice versa)

**Common Mistakes to Avoid:**
- **Using this pattern when R_f or E(R_M) is not given** - This leads to incorrect assumptions or incomplete solutions
- **Attempting to solve for missing parameters within this pattern** - Use dedicated system of equations pattern instead
- Comparing returns without calculating CAPM required return
- Identifying mispricing but not constructing the arbitrage strategy
- **Returning intermediate calculations instead of final answer** - Return asset identifier (e.g., "Asset C"), not dictionary
- Not showing how to replicate the mispriced portfolio's beta
- Confusing beta with expected return in portfolio construction

**Example (sanitized):**
> **Scenario:** Given R_f = 4%, E(R_M) = 11%, three assets: Asset P (β=0.9, E(R)=10%), Asset Q (β=1.3, E(R)=13%), Asset R (β=1.6, E(R)=15%). Which asset will not be held?
> 
> **Wrong approach:** 
> - Notice R_f is given but try to recalculate it, or
> - Return `{'required_return': 0.152, 'expected_return': 0.15, 'difference': -0.002}`
> 
> **Correct approach:**
> 1. Verify all parameters provided: R_f = 4%, E(R_M) = 11% ✓
> 2. Calculate required returns:
>    - Asset P: 4% + 0.9 × (11% - 4%) = 10.3%
>    - Asset Q: 4% + 1.3 × (11% - 4%) = 13.1%
>    - Asset R: 4% + 1.6 × (11% - 4%) = 15.2%
> 3. Compare: Asset R offers 15% < 15.2% required (overpriced)
> 4. Return: "Asset R"

---
## Pattern: Arrival Cost Calculation in Trade Execution

**Description:** Arrival cost measures execution quality relative to the decision price (when portfolio manager decided to trade), not the release price or any other benchmark. It captures market impact from decision to execution, **excluding explicit costs like commissions**. Arrival cost is calculated as the percentage difference between the weighted average execution price and the decision price, expressed in basis points.

**When to Use:** Questions asking specifically for "arrival cost," "arrival price benchmark," or "market impact cost" when decision price, execution prices, and shares are provided.

**When NOT to Use:**
- When question asks for "total trading cost" or "trading cost" (those include commissions and market impact)
- When question asks for "total implementation shortfall" (includes all cost components)
- When question asks for "execution cost breakdown" showing all components separately
- When only asking for commission costs

**Procedure:**
1. Formula: Arrival Cost = [(Avg Execution Price - Decision Price) / Decision Price] × 10,000 (for basis points)
2. Identify decision price (when PM decided to trade)
3. Calculate weighted average execution price across all executed fills
4. Compute percentage difference from decision price
5. Convert to basis points if requested (multiply by 10,000)
6. **CRITICAL: DO NOT include commissions or other explicit costs in arrival cost**
7. Arrival cost measures ONLY the market impact (price movement), not total trading cost

**Common Mistakes to Avoid:**
- Using release price or first execution price instead of decision price
- Not weighting execution prices by share quantities
- **Including commissions in arrival cost calculation** - Arrival cost measures only market impact (price movement), not explicit costs
- **Confusing "arrival cost" with "trading cost"** - Trading cost = arrival cost + commissions; arrival cost excludes commissions
- Forgetting to convert to basis points (multiply by 10,000)
- Confusing arrival cost with total implementation shortfall

**Example (sanitized):**
> **Scenario:** PM decided to buy 5,000 shares at decision price $60.00. Executed: 2,000 shares at $60.30, 3,000 shares at $60.50. Commission = $0.03/share. Calculate arrival cost in bp.
> 
> **Wrong approach:** 
> - Include commission: [(60.42 - 60.00)/60.00 + (0.03 × 5000)/(60.00 × 5000)] × 10000
> - This confuses arrival cost with total trading cost
> 
> **Correct approach:**
> 1. Weighted avg execution = (2000×60.30 + 3000×60.50)/5000 = 60.42
> 2. Arrival cost = (60.42 - 60.00)/60.00 × 10000 = 70 bp
> 3. Commission is NOT part of arrival cost (it's a separate explicit cost)
> 4. If asked for "trading cost," THEN add commission: 70 bp + commission component

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

**Description:** Information Ratio measures active management skill as alpha (excess return above benchmark) divided by tracking error (residual standard deviation). IR = Alpha / σ_residual, where alpha MUST be calculated using Jensen's alpha formula: R_p - [R_f + β × (R_M - R_f)]. This is the complete CAPM-based alpha calculation that accounts for both the risk-free rate and the systematic risk adjustment.

**When to Use:** Questions asking for "information ratio," "risk-adjusted alpha," or "active management skill" when portfolio returns, benchmark returns, beta, risk-free rate, and residual risk are provided.

**When NOT to Use:**
- When residual standard deviation is not provided (cannot calculate IR without tracking error)
- When question asks for Sharpe ratio or Treynor ratio (different metrics)
- When only two assets are given without explicit benchmark or risk-free rate

**Procedure:**
1. Formula: IR = Alpha / σ_residual
2. **CRITICAL: Calculate alpha using complete Jensen's alpha formula:** Alpha = R_portfolio - [R_f + β × (R_market - R_f)]
3. **Alternative equivalent form:** Alpha = (R_portfolio - R_f) - β × (R_market - R_f)
4. **DO NOT use simplified form:** Alpha ≠ R_portfolio - β × R_market (this omits risk-free rate adjustment)
5. Identify residual standard deviation (tracking error)
6. Divide alpha by residual standard deviation
7. Do not use total standard deviation or confuse with Sharpe ratio

**Code Example:**

**Scenario:** Portfolio return 16%, beta 1.15, market return 12%, risk-free rate 4%, residual std dev 1%. Calculate information ratio.

**Correct Code:**
```python
# Information ratio calculation
R_portfolio = 0.16
beta = 1.15
R_market = 0.12
R_f = 0.04
residual_std = 0.01

# Jensen's alpha (COMPLETE formula with risk-free rate)
alpha = R_portfolio - (R_f + beta * (R_market - R_f))
# Equivalent form: alpha = (R_portfolio - R_f) - beta * (R_market - R_f)

# Information ratio = alpha / tracking error
information_ratio = alpha / residual_std

# Result: 0.16 - [0.04 + 1.15*(0.12-0.04)] = 0.16 - 0.132 = 0.028
# IR = 0.028 / 0.01 = 2.80 or 280%
information_ratio  # 2.80 or 280%
```

**Common Bugs to Avoid:**
- **Using (R_portfolio - β × R_market) instead of (R_portfolio - [R_f + β × (R_market - R_f)])** - This is the most common error; it omits the risk-free rate adjustment entirely
- **Using (R_portfolio - R_f) / residual_std** - This calculates a modified Sharpe ratio, not Information Ratio
- Dividing by total standard deviation instead of residual standard deviation
- Not adjusting benchmark return by portfolio beta
- Confusing Information Ratio with Sharpe Ratio or Treynor Ratio
- **Forgetting that alpha must be risk-adjusted using CAPM, not just a simple return difference**

---
## Pattern: Portfolio Insurance via Put Option Delta Hedging

**Description:** Portfolio insurance using put options requires holding (1 - |put delta|) in the risky asset and |put delta| in risk-free securities. The put delta is negative, so the risky asset allocation equals (1 + put_delta), not the delta itself. Questions may ask for risky allocation, risk-free allocation, or dollar amounts - carefully parse the question context to determine which component is being requested.

**When to Use:** Questions asking for "initial portfolio allocation," "risky asset weight," "risk-free allocation," or "initial portfolio" when implementing portfolio insurance through put options or dynamic hedging strategies. Pay attention to whether the answer should be a percentage or dollar amount, and which component (risky vs risk-free) the question is asking for.

**Procedure:**
1. Formula: Risky_Asset_Weight = 1 - |Delta_put| = 1 + Delta_put (since Delta_put < 0)
2. Calculate put option delta using Black-Scholes-Merton formula with dividend yield: Delta_put = e^(-qT) × [N(d1) - 1]
3. Compute d1 = [ln(S0/K) + (r - q + σ²/2)T] / (σ√T)
4. The risky asset allocation is (1 + Delta_put); risk-free allocation is -Delta_put = |Delta_put|
5. **Parse question context carefully to determine which component to return:**
   - Phrases like "keeping part in risk-free," "holding risk-free securities," "insurance by holding risk-free" → return risk-free allocation
   - Phrases like "equity allocation," "risky asset weight," "stock position" → return risky allocation
   - Generic "initial portfolio" without context → default to risky allocation
6. **Determine output format:** Check if question asks for percentage or dollar amount
7. **For percentage:** Return risky_weight × 100 or risk_free_weight × 100 based on what's asked
8. **For dollar amount:** Multiply weight by total portfolio value

**Example (sanitized):**
> **Scenario 1:** A $200M portfolio needs protection. Manager calculates put delta = -0.42. Question asks: "If the manager provides insurance by keeping part of the portfolio in risk-free securities, what should the allocation be?"
> 
> **Wrong approach:** 
> - Calculate risky weight = 1 + (-0.42) = 0.58 or 58%
> - Return 58% (ignoring the contextual clue about "keeping part in risk-free")
> 
> **Correct approach:**
> 1. Calculate both components: risky = 58%, risk-free = 42%
> 2. Parse question: "keeping part in risk-free securities" is a strong signal
> 3. The question is asking about the risk-free component specifically
> 4. Return 42% (the risk-free allocation)
>
> **Scenario 2:** Same setup, but question asks: "What should the initial equity allocation be?"
> 
> **Correct approach:**
> 1. Calculate both components: risky = 58%, risk-free = 42%
> 2. Parse question: "equity allocation" clearly refers to risky assets
> 3. Return 58% (the risky allocation)

**Common Mistakes to Avoid:**
- Returning put_delta directly instead of (1 + put_delta) for risky asset weight
- Forgetting that put delta is negative; using (1 - put_delta) would give >100% allocation
- Omitting the e^(-qT) factor when dividend yield is present
- **Not parsing question context to determine which component (risky vs risk-free) is being asked for**
- **Ignoring contextual clues like "keeping part in risk-free" or "insurance by holding risk-free securities"**
- Returning dollar amounts when percentage is expected (or vice versa)
- Defaulting to risky allocation when question explicitly discusses risk-free component

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

## Pattern: Futures-Based Asset Allocation Rebalancing with Risk Adjustment

**Description:** When rebalancing portfolio allocations using futures contracts, the number of contracts must account for the risk differential (beta for equities, duration for bonds) between the portfolio segment and the futures contract. This is distinct from simple exposure changes or P&L calculations.

**When to Use:** Questions asking to "adjust allocation," "rebalance using futures," or "change exposure" when both portfolio and futures have different betas (for equities) or durations (for bonds). Typically involves moving from one asset class to another.

**Procedure:**
1. For equity futures: N = (ΔValue × Portfolio_Beta) / (Futures_Price × Multiplier × Futures_Beta)
2. For bond futures: N = (ΔValue × Portfolio_Duration) / (Futures_Price × Multiplier × Futures_Duration)
3. Identify the dollar value change needed (target allocation - current allocation)
4. Identify portfolio segment's beta/duration being reduced
5. Identify futures contract beta/duration
6. Apply appropriate formula and round to whole contracts
7. Sell contracts to reduce exposure (negative), buy to increase (positive)

**Example (sanitized):**
> **Scenario:** A $200M portfolio needs to reduce equity exposure by $30M and increase bond exposure by $30M. The equity segment has beta 1.25, equity futures have beta 1.15 and price $125,000 per contract. The bond segment has duration 6.2 years, bond futures have duration 5.8 years and price $95,000 per contract. Calculate contracts needed.
> 
> **Wrong approach:** Simply divide dollar changes by contract values:
> - Equity: -$30M / $125,000 = -240 contracts
> - Bonds: $30M / $95,000 = 316 contracts
> This ignores the beta/duration mismatch between portfolio and futures.
> 
> **Correct approach:**
> 1. Equity contracts = ($30M × 1.25) / ($125,000 × 1.15) = $37.5M / $143,750 = -261 contracts (sell)
> 2. Bond contracts = ($30M × 6.2) / ($95,000 × 5.8) = $186M / $551,000 = 338 contracts (buy)
> 3. The beta/duration adjustment ensures the risk exposure change matches the dollar allocation change
> 4. Without adjustment, you'd under-hedge (if portfolio beta > futures beta) or over-hedge (if portfolio beta < futures beta)

**Common Mistakes to Avoid:**
- Dividing only by futures price without accounting for beta/duration differential
- Using a ratio of betas/durations instead of the full adjustment formula
- Applying equity beta adjustment to bond futures or vice versa
- Forgetting to multiply portfolio value change by portfolio beta/duration
- Not rounding to whole contracts (can't trade fractional contracts)

---

## Pattern: Minimum Variance Hedge Ratio with Regression Coefficient

**Description:** When a regression of asset returns on currency changes provides a slope coefficient, this coefficient IS the minimum variance hedge ratio. It already incorporates the correlation and volatility ratio between asset and currency. No additional adjustments are needed.

**When to Use:** Questions about "minimum variance hedge" when given a regression slope coefficient of asset returns regressed on currency changes.

**When NOT to Use:**
- When no regression coefficient is provided (must calculate from correlation and volatility ratio)
- When question asks for simple one-to-one hedge
- When regression is of something other than asset returns on currency changes

**Procedure:**
1. Identify the regression slope coefficient (β) from asset returns regressed on currency changes
2. **The regression coefficient IS the hedge ratio** - no further calculation needed
3. Hedge amount = Currency Exposure × Regression Coefficient
4. This is the minimum variance hedge (optimal hedge ratio)
5. Do NOT multiply by additional correlation or volatility adjustments

**Common Mistakes to Avoid:**
- **Adding unnecessary correlation adjustment** - The regression coefficient already incorporates correlation
- Multiplying by assumed volatility ratios when regression coefficient is given
- Confusing regression coefficient with beta from CAPM (different contexts)
- Calculating hedge ratio from scratch when regression output is provided

**Example (sanitized):**
> **Scenario:** A portfolio holds JPY 500M in Japanese stocks. Regression of stock returns (in USD) on yen changes yields slope coefficient of 0.65. Calculate minimum variance hedge.
> 
> **Wrong approach:** 
> - Assume correlation = 0.70, then calculate: 500M × 0.70 × 0.65 = 227.5M
> 
> **Correct approach:**
> 1. Regression coefficient = 0.65 is the minimum variance hedge ratio
> 2. Hedge amount = 500M × 0.65 = 325M yen
> 3. The coefficient already incorporates all necessary adjustments
> 4. No additional correlation or volatility factors needed

---

## Pattern: Solving for CAPM Parameters via System of Equations

**Description:** When risk-free rate or market return is not provided but multiple assets with known betas and expected returns are given, solve the system of CAPM equations simultaneously to find the unknown parameters. Do NOT assume values. This pattern is specifically for questions that ask you to FIND a missing CAPM parameter (like "what is the risk-free rate?" or "what is the expected market return?") when given asset data.

**When to Use:** 
- Questions explicitly asking for "risk-free rate" or "market return" or "expected return on the market" when these values are NOT provided
- Given multiple assets (at least 2) with known betas and expected returns
- The unknown parameter must be calculated from the asset data

**When NOT to Use:**
- When risk-free rate AND market return are both explicitly given (use CAPM mispricing detection pattern)
- When only one asset is provided (insufficient information for system of equations)
- When question asks to identify mispriced assets and all CAPM parameters are given (use mispricing detection pattern)
- When question provides one parameter and asks for another with only one asset (use single CAPM equation)

**Procedure:**
1. **Identify what is being asked:** Look for phrases like "what is the risk-free rate" or "calculate the expected market return"
2. Set up CAPM equations for each asset: E(R_i) = R_f + β_i × [E(R_M) - R_f]
3. Rearrange to standard form: E(R_i) = R_f × (1 - β_i) + β_i × E(R_M)
4. With two assets, create two equations with two unknowns (R_f and E(R_M))
5. Solve simultaneously using substitution or elimination:
   - From equation 1: Isolate one variable (e.g., R_f) in terms of the other
   - Substitute into equation 2 to solve for the second variable
   - Back-substitute to find the first variable
6. Verify solution works for all given assets
7. Return the requested parameter (R_f or E(R_M))

**Code Example:**

**Scenario:** Asset J has β=1.2, E(R)=14%. Asset K has β=0.7, E(R)=9.5%. What is the risk-free rate?

**Correct Code:**
```python
# CAPM system of equations solver
# Asset data
assets = [
    {'beta': 1.2, 'expected_return': 0.14},  # Asset J
    {'beta': 0.7, 'expected_return': 0.095}  # Asset K
]

# Set up system: E(R_i) = R_f(1 - β_i) + β_i × E(R_M)
# Asset J: 0.14 = R_f(1 - 1.2) + 1.2 × E(R_M) → 0.14 = -0.2×R_f + 1.2×E(R_M)
# Asset K: 0.095 = R_f(1 - 0.7) + 0.7 × E(R_M) → 0.095 = 0.3×R_f + 0.7×E(R_M)

# Solve using elimination method
# From equation 1: E(R_M) = (0.14 + 0.2×R_f) / 1.2
# Substitute into equation 2:
# 0.095 = 0.3×R_f + 0.7×[(0.14 + 0.2×R_f) / 1.2]
# 0.095 = 0.3×R_f + (0.098 + 0.14×R_f) / 1.2
# 0.114 = 0.36×R_f + 0.098 + 0.14×R_f
# 0.016 = 0.5×R_f
# R_f = 0.032

beta_1, ret_1 = assets[0]['beta'], assets[0]['expected_return']
beta_2, ret_2 = assets[1]['beta'], assets[1]['expected_return']

# Solve for R_f using elimination
# Multiply equation 1 by (1-beta_2) and equation 2 by (1-beta_1), then subtract
numerator = ret_1 * (1 - beta_2) - ret_2 * (1 - beta_1)
denominator = (1 - beta_1) * (1 - beta_2) - beta_1 * (1 - beta_2) + beta_2 * (1 - beta_1)

# Alternative: Direct algebraic solution
# From the two equations, solve for R_f
R_f = (ret_2 * beta_1 - ret_1 * beta_2) / (beta_1 - beta_2 - beta_1 * beta_2 + beta_2)

# Simplified formula for two-asset case:
R_f = (ret_1 - ret_2 - beta_1 * ret_1 + beta_1 * ret_2) / (1 - beta_1 - 1 + beta_2)
R_f = (ret_2 - beta_2 * (ret_1 - ret_2) / (beta_1 - beta_2))

# Most direct approach:
# Solve: (ret_1 - R_f) / (ret_2 - R_f) = beta_1 / beta_2 is NOT correct
# Instead use: ret_1 - ret_2 = (beta_1 - beta_2) × (E(R_M) - R_f)
# And: ret_1 = R_f + beta_1 × (E(R_M) - R_f)

# Calculate market risk premium first
market_risk_premium = (ret_1 - ret_2) / (beta_1 - beta_2)

# Then solve for R_f
R_f = ret_1 - beta_1 * market_risk_premium

R_f  # 0.032 or 3.2%
```

**Common Mistakes to Avoid:**
- **Assuming risk-free rate (e.g., 4%) when not given** - This is the most critical error
- **Using mispricing detection pattern when parameters need to be solved** - Wrong pattern application
- Using only one asset equation when two are available
- Not verifying the solution works for all assets
- Confusing which parameter is being asked for
- **Calculating market risk premium and stopping** - The question asks for R_f or E(R_M), not the premium
- Arithmetic errors in algebraic manipulation

---
## Pattern: Beta Calculation from Covariance Data

**Description:** Beta measures systematic risk as the sensitivity of an asset's returns to market returns. When covariance and market variance are explicitly provided, beta is calculated directly as Beta = Cov(Asset, Market) / Var(Market). This is the fundamental definition of beta. Do NOT use the CAPM expected return equation to back-solve for beta when covariance data is available.

**When to Use:** Questions asking to "calculate beta" when covariance between the asset and market (or a market proxy) and market variance are explicitly provided in tables or exhibits.

**When NOT to Use:**
- When covariance is not provided but correlation and standard deviations are given (use Beta = ρ × σ_asset / σ_market)
- When only expected returns are given (may need to use CAPM to find beta, but verify if this is appropriate)
- When question asks for expected return given beta (use CAPM formula)

**Procedure:**
1. Formula: Beta = Cov(Asset, Market) / Var(Market)
2. Identify covariance between asset and market from provided data
3. Identify market variance (or square market standard deviation if only std dev is given)
4. Divide covariance by market variance
5. Return beta value
6. **Do NOT use CAPM expected return equation** E(R) = R_f + β × (R_M - R_f) to solve for beta when covariance is available

**Example (sanitized):**
> **Scenario:** An exhibit shows: Asset X has covariance with Global Market Index = 0.0084. Global Market Index has variance = 0.0144. Risk-free rate = 3%, Expected return on Asset X = 11%, Expected market return = 9%. Calculate beta for Asset X.
> 
> **Wrong approach:** 
> - Use CAPM: 0.11 = 0.03 + β × (0.09 - 0.03)
> - Solve: β = (0.11 - 0.03) / 0.06 = 1.33
> - This ignores the directly provided covariance data
> 
> **Correct approach:**
> 1. Covariance data is explicitly provided → use fundamental beta definition
> 2. Beta = Cov(Asset, Market) / Var(Market)
> 3. Beta = 0.0084 / 0.0144 = 0.583
> 4. The CAPM equation is for finding expected returns GIVEN beta, not for calculating beta when covariance is available
> 5. Always prefer the covariance-based calculation when data is provided

**Common Mistakes to Avoid:**
- Using CAPM expected return equation to back-solve for beta when covariance is directly available
- Confusing covariance with correlation (correlation is dimensionless, covariance has units)
- Dividing by market standard deviation instead of market variance
- Not recognizing when covariance data is provided in exhibits or tables
- Using correlation × (σ_asset / σ_market) when direct covariance is available (both work, but covariance method is more direct)

---

## Pattern: Portfolio Beta with Risk-Free Asset Allocation

**Description:** When a portfolio contains multiple risky assets and a risk-free asset, portfolio beta equals the weighted average of individual asset betas, where the risk-free asset has beta = 0. Given a target portfolio beta and known allocations to some assets, solve for the unknown allocations using: β_target = Σ(w_i × β_i) + w_RF × 0, subject to Σw_i = 1.

**When to Use:** Questions asking for "risk-free allocation," "investment in risk-free asset," or "dollar amount in risk-free securities" when portfolio beta target is specified, individual asset betas are given, and some (but not all) asset allocations are known.

**Procedure:**
1. Formula: β_portfolio = Σ(w_i × β_i) for all risky assets (risk-free beta = 0)
2. Constraint: Σw_all = 1 (all weights including risk-free must sum to 1)
3. Set up equation: β_target = w_A × β_A + w_B × β_B + ... + w_n × β_n
4. Use constraint: w_RF = 1 - (w_A + w_B + ... + w_n)
5. If some risky asset weights are unknown, set up system of equations
6. Solve for unknown weights (typically risk-free allocation)
7. Convert to dollar amounts if requested: Dollar_RF = w_RF × Total_Portfolio_Value

**Example (sanitized):**
> **Scenario:** A $500,000 portfolio targets beta = 1.10. It holds $150,000 in Stock P (β=1.25) and $120,000 in Stock Q (β=0.90). Stock R (β=1.35) and risk-free asset (β=0) make up the remainder. Find the dollar investment in the risk-free asset.
> 
> **Wrong approach:** 
> - Assume Stock R has zero investment
> - Calculate: w_RF = 1 - (150k/500k) - (120k/500k) = 0.46
> - Return: $230,000 in risk-free
> - This ignores Stock R's contribution to portfolio beta
> 
> **Correct approach:**
> 1. Set up portfolio beta equation: 1.10 = w_P × 1.25 + w_Q × 0.90 + w_R × 1.35 + w_RF × 0
> 2. Known weights: w_P = 150k/500k = 0.30, w_Q = 120k/500k = 0.24
> 3. Constraint: w_P + w_Q + w_R + w_RF = 1 → w_R + w_RF = 0.46
> 4. Substitute into beta equation: 1.10 = 0.30×1.25 + 0.24×0.90 + w_R×1.35
> 5. Solve: 1.10 = 0.375 + 0.216 + 1.35×w_R → 1.10 = 0.591 + 1.35×w_R
> 6. w_R = (1.10 - 0.591) / 1.35 = 0.377
> 7. w_RF = 0.46 - 0.377 = 0.083 or 8.3%
> 8. Dollar amount: $500,000 × 0.083 = $41,500 in risk-free

**Common Mistakes to Avoid:**
- Assuming unlisted risky assets have zero allocation when they appear in the data
- Calculating risk-free weight as simple residual without considering portfolio beta constraint
- Forgetting that risk-free asset has beta = 0 (doesn't contribute to portfolio beta)
- Not setting up the full system of equations when multiple unknowns exist
- Confusing weight (percentage) with dollar amount in the final answer

## Pattern: Residual Variance Calculation with Percentage Units

**Description:** When residual standard deviations are provided in percentage form (e.g., "58%"), residual variance should be calculated by squaring the percentage value directly without converting to decimal form. Financial variance is conventionally reported in percentage-squared units (or basis points squared), not decimal-squared units. A residual standard deviation of 58% yields variance of 58² = 3,364 (percentage-squared), not 0.58² = 0.3364 (decimal-squared).

**When to Use:** Questions involving "residual variance," "idiosyncratic variance," or "unsystematic risk" in factor models when standard deviations are expressed as percentages in the source data. Common in CAPM, APT, and multi-factor model contexts.

**Procedure:**
1. **CHECK: Identify the units of the input standard deviation** - Look for "%" symbol or "Residual Standard Deviation (%)" in tables
2. If standard deviation is in percentage form (e.g., 58%), square the percentage value directly: Variance = 58² = 3,364
3. If standard deviation is in decimal form (e.g., 0.58), square the decimal: Variance = 0.58² = 0.3364
4. **VALIDATION: Check magnitude** - Percentage-squared variance should be in thousands (e.g., 3,364), decimal-squared should be < 1 (e.g., 0.3364)
5. Return variance in the same unit system as the input (percentage-squared if input was percentage)
6. For volatility calculations, take square root preserving the unit system

**Example (sanitized):**
> **Scenario:** A factor model analysis provides residual standard deviations for three portfolios: Portfolio X (σ_e = 45%), Portfolio Y (σ_e = 62%), Portfolio Z (σ_e = 38%). Calculate residual variances.
> 
> **Wrong approach:** 
> - Convert to decimals: 0.45, 0.62, 0.38
> - Square: 0.2025, 0.3844, 0.1444
> - Return: Portfolio X variance = 0.2025
> - This produces decimal-squared units inconsistent with financial reporting conventions
> 
> **Correct approach:**
> 1. Input shows "σ_e = 45%" → percentage units
> 2. Square percentage values directly:
>    - Portfolio X: 45² = 2,025 (percentage-squared)
>    - Portfolio Y: 62² = 3,844 (percentage-squared)
>    - Portfolio Z: 38² = 1,444 (percentage-squared)
> 3. Validation: Magnitudes in thousands confirm percentage-squared units
> 4. Return: Portfolio X variance = 2,025
> 5. If question asks for standard deviation from variance: √2,025 = 45%

**Common Mistakes to Avoid:**
- Converting percentage standard deviations to decimals before squaring (produces wrong magnitude)
- Mixing unit systems (e.g., decimal standard deviation with percentage-squared variance)
- Not validating that variance magnitude matches expected scale (3,364 vs 0.3364 is 10,000x difference)
- Assuming all financial data should be in decimal form (variance is often reported in percentage-squared or basis points squared)
- Forgetting that when standard deviation is 58%, the variance is 3,364 (not 0.3364)

## Pattern: Trade Execution Cost Components

**Description:** Trading costs in execution analysis consist of multiple components that must be distinguished: (1) **Arrival cost** = market impact only (execution price - decision price), excluding commissions; (2) **Trading cost** = market impact + commissions; (3) **Total implementation shortfall** = all costs including delay costs and opportunity costs. The question wording determines which components to include.

**When to Use:** Questions asking for "trading cost," "execution cost," or "total cost" (not just "arrival cost") when given decision price, execution prices, shares traded, and commissions.

**When NOT to Use:**
- When question asks specifically for "arrival cost" only (use Arrival Cost pattern, exclude commissions)
- When question asks for "market impact" only (exclude commissions)
- When no commission data is provided

**Procedure:**
1. **Parse question carefully:** Determine if asking for arrival cost, trading cost, or total implementation shortfall
2. Formula: Trading Cost = Market Impact + Commissions
3. Formula: Market Impact = (Avg Execution Price - Decision Price) × Shares Executed
4. Identify decision price (when PM decided to trade)
5. Calculate weighted average execution price for executed shares
6. Calculate market impact: (Avg Execution Price - Decision Price) × Shares Executed
7. Add commissions to get total trading cost
8. If question asks for subset of shares, allocate costs proportionally
9. Express in dollars or basis points as requested

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

# Total trading cost (NOT arrival cost)
trading_cost = market_impact + allocated_commission

trading_cost  # Trading cost for the specified shares
```

**Common Mistakes to Avoid:**
- **Confusing "trading cost" with "arrival cost"** - Trading cost includes commissions; arrival cost does not
- Including delay cost (decision price - release price) in trading cost calculation
- Including opportunity cost of unexecuted shares in trading cost
- Using total implementation shortfall instead of just commission + market impact
- Not allocating commissions proportionally when question asks for subset of shares
- Using release price instead of decision price as the benchmark
- **Excluding commissions when question asks for "trading cost" or "execution cost"**

**Example (sanitized):**
> **Scenario:** PM decided to buy 3,000 shares at $22.26. Executed at average price $22.47. Commissions = $210. Question asks: "What is the trading cost?"
> 
> **Wrong approach:** 
> - Calculate only arrival cost: (22.47 - 22.26)/22.26 × 10000 = 94 bp
> - Ignore commissions
> 
> **Correct approach:**
> 1. Market impact = (22.47 - 22.26) × 3000 = $630
> 2. Commissions = $210
> 3. Trading cost = $630 + $210 = $840
> 4. Or in bp: ($840 / (22.26 × 3000)) × 10000 ≈ 126 bp
> 5. Must include commissions when asked for "trading cost"