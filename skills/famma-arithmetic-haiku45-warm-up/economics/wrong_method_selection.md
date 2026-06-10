# SKILL PATTERNS FOR FINANCIAL CALCULATIONS (Program of Thought)

## Pattern: Real Estate Return Decomposition with Cap Rate Changes

**Description:** Real estate expected returns must account for the inverse relationship between capitalization rates and property values. When cap rates decline (compress), property values increase proportionally, requiring percentage-based capital appreciation calculations rather than simple additive adjustments.

**When to Use:** Questions involving real estate return forecasts with changing capitalization rates, NOI growth, and property valuation. Keywords: "cap rate," "NOI growth," "expected return," "industrial/commercial properties."

**Procedure:**
1. **Formula:** Expected Return = Income Return + Capital Return, where:
   - Income Return = Current Cap Rate
   - Capital Return = NOI Growth Rate + (Current Cap Rate - Expected Cap Rate) / Expected Cap Rate
2. Identify current cap rate (income component)
3. Calculate capital appreciation from cap rate compression: percentage change in value = (cap_rate_current - cap_rate_future) / cap_rate_future
4. Add NOI growth rate to capital appreciation component
5. Sum income return and total capital return

**Code Example:**

**Scenario:** A retail property has a current cap rate of 5.2%, expected end-of-period cap rate of 5.0%, and NOI growth rate of 3.0%. Calculate expected return.

**Correct Code:**
```python
# Real estate return with cap rate compression
current_cap_rate = 0.052  # 5.2%
expected_cap_rate = 0.050  # 5.0%
noi_growth_rate = 0.030  # 3.0%

# Income return component
income_return = current_cap_rate

# Capital return component
# Cap rate compression creates capital appreciation
# Property value changes inversely with cap rate
cap_rate_compression_effect = (current_cap_rate - expected_cap_rate) / expected_cap_rate
capital_return = noi_growth_rate + cap_rate_compression_effect

# Total expected return
expected_return = income_return + capital_return
expected_return_percentage = expected_return * 100

expected_return_percentage  # Must be expression, not print
```

**Common Bugs to Avoid:**
- Treating cap rate change as simple additive component (current - expected) without dividing by expected cap rate
- Forgetting the inverse relationship: declining cap rates increase property values
- Using (expected - current) instead of (current - expected) in numerator
- Adding cap rate change directly instead of calculating percentage impact on value

---

## Pattern: Singer-Terhaar Model with Integration Weighting

**Description:** The Singer-Terhaar approach calculates expected returns as a weighted average of fully integrated and fully segmented market scenarios, using the degree of integration as the weighting factor. Segmentation is NOT an additive adjustment but determines the blend between two distinct return calculations.

**When to Use:** Questions about emerging market equity returns, international diversification, or market segmentation analysis. Keywords: "Singer-Terhaar," "degree of integration," "segmentation," "illiquidity premium," "global investable market."

**Procedure:**
1. **Formula:** E(R) = w × R_integrated + (1 - w) × R_segmented + Illiquidity Premium, where:
   - w = Degree of Integration
   - R_integrated = Rf + Beta × (E(R_market) - Rf)
   - R_segmented = Rf + Sharpe_Ratio_Asset × Std_Dev_Asset
   - Beta = Correlation × (Std_Dev_Asset / Std_Dev_Market)
2. Calculate market risk premium from Sharpe ratio: MRP = Sharpe × Std_Dev_Market
3. Compute beta of asset relative to global market
4. Calculate fully integrated return (CAPM-style with beta)
5. Calculate fully segmented return (using asset's own Sharpe ratio and volatility)
6. Weight the two scenarios by degree of integration
7. Add illiquidity premium as final adjustment

**Code Example:**

**Scenario:** An emerging market equity has 28% std dev, 0.75 correlation with global market (std dev 8%, Sharpe 0.30), 70% integration, risk-free rate 3.0%, and 50 bps illiquidity premium. Calculate expected return.

**Correct Code:**
```python
# Singer-Terhaar model parameters
std_dev_asset = 0.28
std_dev_market = 0.08
correlation = 0.75
degree_integration = 0.70
risk_free_rate = 0.030
illiquidity_premium = 0.0050  # 50 bps
sharpe_market = 0.30

# Step 1: Calculate beta
beta = correlation * (std_dev_asset / std_dev_market)

# Step 2: Market risk premium
market_risk_premium = sharpe_market * std_dev_market

# Step 3: Fully integrated return (CAPM)
return_integrated = risk_free_rate + beta * market_risk_premium

# Step 4: Fully segmented return (own risk premium)
# Asset earns its own Sharpe ratio times its own volatility
return_segmented = risk_free_rate + sharpe_market * std_dev_asset

# Step 5: Weighted average based on integration
expected_return = (degree_integration * return_integrated + 
                   (1 - degree_integration) * return_segmented + 
                   illiquidity_premium)

expected_return_percentage = expected_return * 100
expected_return_percentage
```

**Common Bugs to Avoid:**
- Calculating a "segmentation adjustment" and adding it to integrated return (double-counting)
- Using asset's Sharpe ratio when only market Sharpe is given (assume same Sharpe for segmented calculation)
- Forgetting to weight the two scenarios by degree of integration
- Adding illiquidity premium before weighting instead of after
- Confusing beta calculation: must use correlation × (asset_vol / market_vol)

---

## Pattern: Multi-Component Return Decomposition Verification

**Description:** Complex return calculations with multiple additive or multiplicative components require explicit decomposition and verification that each component is calculated correctly and combined using the appropriate mathematical operation (addition vs. multiplication, percentage vs. decimal).

**When to Use:** Any multi-step return calculation including Grinold-Kroner model, real estate returns, fixed income returns with multiple premiums, or equity returns with growth and valuation changes.

**Procedure:**
1. **Formula:** Identify the correct decomposition formula for the asset class
2. Extract each component separately with clear variable names
3. Calculate each component independently before combining
4. Verify units (percentage vs. decimal) are consistent
5. Apply correct combination method (additive for independent components, multiplicative for compounding)
6. Sanity check: does the magnitude make economic sense?

**Code Example:**

**Scenario:** Calculate equity return using Grinold-Kroner: dividend yield 2.5%, buyback yield 1.2%, real earnings growth 3.5%, inflation 2.0%, P/E expansion from 18 to 20 over 5 years.

**Correct Code:**
```python
import math

# Grinold-Kroner components
dividend_yield = 0.025
buyback_yield = 0.012
real_earnings_growth = 0.035
inflation = 0.020
pe_initial = 18
pe_final = 20
years = 5

# Income component
income_return = dividend_yield + buyback_yield

# Nominal earnings growth
nominal_earnings_growth = real_earnings_growth + inflation

# P/E repricing component (annualized)
# Total P/E change over period
pe_change_total = (pe_final - pe_initial) / pe_initial
# Annualize using geometric mean
pe_change_annual = (1 + pe_change_total) ** (1 / years) - 1

# Grinold-Kroner: sum of components
expected_return = income_return + nominal_earnings_growth + pe_change_annual

expected_return_percentage = expected_return * 100
expected_return_percentage
```

**Common Bugs to Avoid:**
- Mixing percentage and decimal formats (e.g., adding 2.5 to 0.012)
- Using simple average for multi-period changes instead of geometric/annualized
- Forgetting to convert P/E changes to annual rates
- Adding real growth and inflation incorrectly (should be additive for small values)
- Not decomposing into clear components before combining
- Using print() instead of returning expression value

---

## Pattern: Basis Points and Percentage Conversion

**Description:** Financial data often mixes basis points (bps), percentages, and decimals. Consistent unit conversion is critical before any arithmetic operations to avoid order-of-magnitude errors.

**When to Use:** Any calculation involving credit spreads, premiums, yields, or rates expressed in basis points. Keywords: "bps," "basis points," "spread," "premium."

**Procedure:**
1. **Formula:** 1 bp = 0.01% = 0.0001 in decimal
2. Identify all inputs and their units (%, bps, decimal)
3. Convert all values to same unit (preferably decimal for calculation)
4. Perform arithmetic operations
5. Convert final result to required output format
6. Document conversion factors in comments

**Code Example:**

**Scenario:** Calculate corporate bond yield: risk-free rate 2.5%, term premium 100 bps, credit spread 85 bps, liquidity premium 65 bps.

**Correct Code:**
```python
# Bond yield calculation with mixed units
risk_free_rate = 0.025  # 2.5% as decimal
term_premium_bps = 100  # basis points
credit_spread_bps = 85  # basis points
liquidity_premium_bps = 65  # basis points

# Convert basis points to decimal (1 bp = 0.0001)
term_premium = term_premium_bps / 10000
credit_spread = credit_spread_bps / 10000
liquidity_premium = liquidity_premium_bps / 10000

# Sum all components
total_yield = (risk_free_rate + term_premium + 
               credit_spread + liquidity_premium)

# Convert to percentage for output
total_yield_percentage = total_yield * 100
total_yield_percentage
```

**Common Bugs to Avoid:**
- Dividing bps by 100 instead of 10000 (confusing with percentage conversion)
- Adding bps values directly to percentage values without conversion
- Using inconsistent conversion factors within same calculation
- Forgetting that 1% = 100 bps, so 85 bps = 0.85%, not 0.0085%
- Not documenting which variables are in which units

---

## Pattern: Beta Calculation from Correlation and Volatility

**Description:** Beta must be calculated from correlation and relative volatilities when covariance is not directly provided. The formula Beta = Correlation × (Std_Dev_Asset / Std_Dev_Market) is fundamental to CAPM and related models.

**When to Use:** Questions involving CAPM, Singer-Terhaar, or any systematic risk calculation where beta is not given but correlation and standard deviations are provided.

**Procedure:**
1. **Formula:** Beta = ρ × (σ_asset / σ_market), where ρ is correlation
2. Extract correlation coefficient between asset and market
3. Extract standard deviation of asset
4. Extract standard deviation of market benchmark
5. Compute ratio of volatilities
6. Multiply by correlation
7. Verify beta is positive if correlation is positive

**Code Example:**

**Scenario:** An asset has 32% volatility, correlation of 0.68 with market that has 12% volatility. Calculate beta.

**Correct Code:**
```python
# Beta calculation from correlation and volatilities
correlation_with_market = 0.68
std_dev_asset = 0.32  # 32%
std_dev_market = 0.12  # 12%

# Beta formula: correlation × (asset vol / market vol)
beta = correlation_with_market * (std_dev_asset / std_dev_market)

# Sanity check: beta should be positive if correlation is positive
assert beta > 0, "Beta should be positive with positive correlation"

beta  # Returns approximately 1.81
```

**Common Bugs to Avoid:**
- Reversing the volatility ratio (market/asset instead of asset/market)
- Forgetting to multiply by correlation (just using volatility ratio)
- Confusing correlation with R-squared (R² = ρ²)
- Using percentage values inconsistently (mixing 32 with 0.12)
- Assuming beta equals correlation (only true if volatilities are equal)

---

## Pattern: Weighted Average vs. Additive Adjustment

**Description:** Many financial models require weighted averages of scenarios (e.g., integration levels, probability-weighted outcomes) rather than calculating one scenario and adding an adjustment. Recognize when weights represent blending of distinct states versus sequential adjustments.

**When to Use:** Models with integration/segmentation, probability scenarios, or partial exposure calculations. Keywords: "degree of," "weighted," "integration," "probability," "scenario."

**Procedure:**
1. **Formula:** Result = w₁ × Scenario₁ + w₂ × Scenario₂ + ... (weights sum to 1)
2. Identify if weights represent distinct scenarios or sequential adjustments
3. Calculate each scenario independently and completely
4. Verify weights sum to 1.0 (or appropriate total)
5. Multiply each scenario by its weight
6. Sum weighted scenarios
7. Add any final adjustments that apply to all scenarios

**Code Example:**

**Scenario:** Expected return with 60% probability of bull market (15% return) and 40% probability of bear market (-5% return), plus a 0.5% management fee that applies in all scenarios.

**Correct Code:**
```python
# Probability-weighted scenario analysis
prob_bull = 0.60
prob_bear = 0.40
return_bull = 0.15  # 15%
return_bear = -0.05  # -5%
management_fee = 0.005  # 0.5% applies to all scenarios

# Verify probabilities sum to 1
assert abs(prob_bull + prob_bear - 1.0) < 0.001, "Probabilities must sum to 1"

# Weighted average of scenarios
expected_return_gross = prob_bull * return_bull + prob_bear * return_bear

# Apply fee that affects all scenarios
expected_return_net = expected_return_gross - management_fee

expected_return_net_percentage = expected_return_net * 100
expected_return_net_percentage
```

**Common Bugs to Avoid:**
- Calculating one scenario and adding a "weighted adjustment" instead of weighting both scenarios
- Forgetting to verify weights sum to 1.0
- Applying adjustments before weighting instead of after (or vice versa, depending on context)
- Treating degree of integration as an adjustment factor rather than a weighting factor
- Confusing weighted average with simple average