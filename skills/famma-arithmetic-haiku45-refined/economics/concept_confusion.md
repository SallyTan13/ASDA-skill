# Financial Reasoning Skills: Concept Confusion Error Patterns (PoT)

## Pattern: Labor Force Component Double-Counting in GDP Growth Models

**Description:** Incorrectly adding labor force participation growth to potential labor force growth when calculating GDP growth, failing to recognize that participation changes are typically already reflected in total labor force projections or should modify (not add to) the base growth rate.

**When to Use:** GDP growth forecasting questions using labor-based methods with separate data for potential labor force growth and labor force participation changes.

**Procedure:**
1. Formula: `GDP Growth = Labor Force Growth + Labor Productivity Growth`
2. Identify whether labor force growth is given as a single composite measure or broken into components
3. If both "potential labor force growth" and "labor force participation growth" are provided, use ONLY the potential labor force growth (participation is typically already incorporated)
4. Alternative: If participation is explicitly stated as a rate of change modifier, multiply rather than add: `Effective Labor Force Growth = Potential Growth × (1 + Participation Change)`
5. Verify the result makes economic sense (typical developed economy GDP growth: 2-4%)

**Code Example:**

**Scenario:** Forecasting 10-year GDP growth with potential labor force growth of 1.5%, labor force participation growth of 0.4%, and labor productivity growth of 1.3%.

**Correct Code:**
```python
# GDP Growth Components
potential_labor_force_growth = 0.015  # 1.5%
labor_force_participation_growth = 0.004  # 0.4%
labor_productivity_growth = 0.013  # 1.3%

# Method 1: Use only potential labor force growth (most common)
# Participation is typically already reflected in potential estimates
labor_input_growth = potential_labor_force_growth
gdp_growth = labor_input_growth + labor_productivity_growth

# Convert to percentage
gdp_growth_pct = gdp_growth * 100

gdp_growth_pct  # 2.8%
```

**Common Bugs to Avoid:**
- Adding both potential labor force growth AND participation growth (double-counting labor input)
- Confusing "potential labor force" with "labor force participation rate" (different concepts)
- Ignoring context clues about whether components are independent or nested

---

## Pattern: Dornbusch Overshooting vs Interest Rate Parity Confusion

**Description:** Misapplying the Dornbusch overshooting model as simple interest rate parity or forward rate calculation, when it actually describes dynamic exchange rate adjustment where rates initially overshoot long-run equilibrium due to differential speeds of asset vs goods market adjustment.

**When to Use:** Exchange rate forecasting questions explicitly mentioning "Dornbusch overshooting model" with monetary policy or interest rate differentials.

**Procedure:**
1. Formula: `Overshooting Effect = (i_domestic - i_foreign) / speed_of_adjustment`
2. Identify the short-term interest rate differential (monetary policy stance)
3. Recognize that overshooting occurs when monetary policy changes cause immediate exchange rate jumps
4. Calculate the immediate exchange rate response (overshoot) based on interest differential
5. Do NOT use term premiums, credit premiums, or equity premiums (these are not relevant to monetary overshooting)
6. Apply: `Future Rate = Spot Rate × (1 + i_domestic - i_foreign)` for simplified one-period overshooting

**Code Example:**

**Scenario:** Current spot rate DOM/FOR = 1.4500. Domestic short-term rate = 2.0%, Foreign short-term rate = 3.5%. Forecast one-year rate under Dornbusch overshooting.

**Correct Code:**
```python
# Dornbusch Overshooting Model
spot_rate = 1.4500
domestic_short_rate = 0.020  # 2.0%
foreign_short_rate = 0.035  # 3.5%

# Interest rate differential (key driver in Dornbusch model)
interest_differential = domestic_short_rate - foreign_short_rate

# One-year forward rate under overshooting
# Higher foreign rates → foreign currency appreciation (lower DOM/FOR)
forward_rate = spot_rate * (1 + interest_differential)

round(forward_rate, 4)  # 1.4283
```

**Common Bugs to Avoid:**
- Using total returns (adding term premiums, credit premiums) instead of just short-term rates
- Confusing with covered interest rate parity (which uses forward rates, not overshooting dynamics)
- Applying equity premiums or liquidity premiums (irrelevant to monetary policy overshooting)
- Forgetting that Dornbusch focuses on SHORT-TERM monetary policy shocks, not long-term equilibrium

---

## Pattern: Arbitrage Portfolio Identification from Problem Context

**Description:** Constructing ad-hoc replicating portfolios when the problem context has already defined specific benchmark portfolios for comparison, missing that multi-part questions often establish reference portfolios in earlier parts.

**When to Use:** Arbitrage questions where ground truth references specific portfolio names (e.g., "Portfolio G") not explicitly defined in the immediate question text, suggesting prior context.

**Procedure:**
1. Formula: `Arbitrage Profit = Return_Mispriced - Return_Benchmark` (same beta)
2. Check if the problem references portfolios by name that aren't in the current excerpt
3. If ground truth mentions a specific portfolio for comparison, assume it was defined in earlier problem parts
4. Calculate the Security Market Line (SML) expected return for the target beta
5. Compare actual return vs SML return to identify mispricing
6. State arbitrage as: Long underpriced / Short overpriced vs the SML-equivalent portfolio

**Code Example:**

**Scenario:** Portfolio A: E(r)=10%, β=1.0. Portfolio F: E(r)=4%, β=0.0. Portfolio E: E(r)=7%, β=0.6. Problem context suggests Portfolio G exists with same beta as E.

**Correct Code:**
```python
# Given portfolios
E_r_A = 0.10
beta_A = 1.0
E_r_F = 0.04
beta_F = 0.0

# Portfolio E (potentially mispriced)
E_r_E = 0.07
beta_E = 0.6

# Calculate SML expected return for beta = 0.6
risk_free_rate = E_r_F
market_risk_premium = E_r_A - risk_free_rate
E_r_SML = risk_free_rate + beta_E * market_risk_premium

# Mispricing
mispricing = E_r_E - E_r_SML

# Arbitrage strategy
# If problem mentions "Portfolio G" in ground truth, it's the SML-equivalent
# Strategy: Long G (or SML portfolio), Short E if E is overpriced
arbitrage_profit = abs(mispricing)

{
    'SML_return': round(E_r_SML, 4),
    'actual_return': E_r_E,
    'mispricing': round(mispricing, 4),
    'strategy': 'Long Portfolio G, Short Portfolio E' if mispricing < 0 else 'Long Portfolio E, Short Portfolio G',
    'profit_per_dollar': round(arbitrage_profit, 4)
}
```

**Common Bugs to Avoid:**
- Ignoring portfolio names mentioned in ground truth answers
- Always constructing replicating portfolios from scratch when benchmarks exist
- Missing that CFA/exam questions often have multi-part structures with shared context
- Over-engineering solutions when simple pairwise comparisons are intended

---

## Pattern: Human Capital Discount Rate Selection

**Description:** Incorrectly adding volatility measures to the discount rate when valuing human capital, confusing income volatility (standard deviation) with risk premium adjustments, when standard practice uses risk-free rate for present value calculations.

**When to Use:** Holistic balance sheet calculations requiring present value of future employment income with given volatility and risk-free rate parameters.

**Procedure:**
1. Formula: `Human Capital = Σ [Income_t × Survival_Prob_t] / (1 + r_f)^t`
2. Use the risk-free rate as the discount rate for employment income PV
3. Do NOT add occupational income volatility to the discount rate (volatility ≠ risk premium)
4. Apply survival probabilities to each year's expected income
5. Account for wage growth in projecting future income
6. Sum traditional assets + human capital + pension value for holistic total

**Code Example:**

**Scenario:** Current income $500,000, retiring in 2 years. Wage growth 4%, risk-free rate 3%, occupational volatility 2%. Survival probabilities: Year 1: 99.5%, Year 2: 99.0%. Traditional assets $5M, pension $2M.

**Correct Code:**
```python
# Human capital valuation parameters
current_income = 500_000
wage_growth_rate = 0.04
risk_free_rate = 0.03  # Use this for discounting
occupational_volatility = 0.02  # NOT added to discount rate
years_to_retirement = 2

# Survival probabilities
prob_survive_year_1 = 0.995
prob_survive_year_2 = 0.990

# Calculate PV of future income
income_year_1 = current_income * (1 + wage_growth_rate)
pv_income_year_1 = (income_year_1 * prob_survive_year_1) / (1 + risk_free_rate)

income_year_2 = income_year_1 * (1 + wage_growth_rate)
prob_survive_to_year_2 = prob_survive_year_1 * prob_survive_year_2
pv_income_year_2 = (income_year_2 * prob_survive_to_year_2) / ((1 + risk_free_rate) ** 2)

human_capital = pv_income_year_1 + pv_income_year_2

# Holistic balance sheet
traditional_assets = 5_000_000
pension_value = 2_000_000
total_holistic_assets = traditional_assets + human_capital + pension_value

round(total_holistic_assets, 0)  # 8,013,000
```

**Common Bugs to Avoid:**
- Adding volatility to discount rate (volatility is σ, not a return adjustment)
- Confusing risk premium (compensation for risk) with volatility (measure of uncertainty)
- Using discount_rate = risk_free_rate + volatility (conceptually incorrect)
- Forgetting to apply survival probabilities to each period's income
- Not compounding survival probabilities for multi-year horizons

---

## Pattern: Multi-Component Return Aggregation Context Sensitivity

**Description:** Mechanically summing all available return components (short-term rates, term premiums, credit premiums, equity premiums) without considering which components are relevant to the specific model or question context.

**When to Use:** Questions providing multiple return components across asset classes where only a subset is relevant to the specific calculation framework.

**Procedure:**
1. Identify the economic model or framework explicitly named in the question
2. Determine which return components are theoretically relevant to that framework
3. For interest rate parity / FX models: Use only short-term interest rates
4. For bond yield calculations: Use short-term rate + term premium + credit premium
5. For equity valuation: Use risk-free rate + equity premium
6. Ignore components that don't apply to the specific model context

**Code Example:**

**Scenario:** Calculating expected bond yield for credit risk analysis. Given: short-term rate 1.5%, term premium 0.8%, credit premium 1.2%, equity premium 5.0%, liquidity premium 0.3%.

**Correct Code:**
```python
# Available return components
short_term_rate = 0.015
term_premium = 0.008
credit_premium = 0.012
equity_premium = 0.050  # Not relevant for bond yield
liquidity_premium = 0.003

# Context: Bond yield calculation
# Relevant components: short-term rate + term premium + credit premium
# Exclude: equity premium (for stocks), liquidity premium (if not specified)

bond_yield = short_term_rate + term_premium + credit_premium

bond_yield_pct = bond_yield * 100

round(bond_yield_pct, 2)  # 3.50%
```

**Common Bugs to Avoid:**
- Summing all provided numbers without checking relevance
- Including equity premiums in fixed income calculations
- Using credit premiums in risk-free rate calculations
- Ignoring the model name in the question (e.g., "using Dornbusch overshooting" signals specific methodology)
- Not distinguishing between asset class-specific vs cross-asset components