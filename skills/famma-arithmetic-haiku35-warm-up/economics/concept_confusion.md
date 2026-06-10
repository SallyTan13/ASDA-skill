# SKILL PATTERNS FOR ECONOMICS CONCEPT CONFUSION (PoT)

## Pattern: Dornbusch_Overshooting_Exchange_Rate_Forecast

**Description:** When applying the Dornbusch overshooting model, the model must recognize that capital flows toward markets with higher total returns, causing the foreign currency to appreciate (strengthen) and the exchange rate quoted as DOM/FOR to decrease below the current spot rate.

**When to Use:** Questions involving exchange rate forecasting with interest rate differentials, capital flows, and the Dornbusch overshooting model; keywords include "capital flows," "overshooting," "interest rate differential."

**Procedure:**
1. Formula: Future_Rate = Spot_Rate × [1 - (Total_Return_Foreign - Total_Return_Domestic)]
2. Calculate total expected return in domestic market (sum all premiums and rates)
3. Calculate total expected return in foreign market (sum all premiums and rates)
4. Determine direction: if foreign return > domestic return, capital flows to foreign market → foreign currency strengthens → DOM/FOR decreases
5. Apply the differential to the spot rate with correct sign convention
6. Verify: higher foreign returns should result in lower DOM/FOR rate (appreciation of FOR)

**Code Example:**

**Scenario:** Current spot rate DOM/FOR = 1.4500. Domestic market: short-term rate 1.0%, term premium 0.2%, credit premium 0.8%. Foreign market: short-term rate 2.0%, term premium 0.6%, credit premium 0.5%.

**Correct Code:**
```python
# Step 1: Define inputs
spot_rate = 1.4500
domestic_short_rate = 0.01
domestic_term_premium = 0.002
domestic_credit_premium = 0.008

foreign_short_rate = 0.02
foreign_term_premium = 0.006
foreign_credit_premium = 0.005

# Step 2: Calculate total returns
total_domestic_return = domestic_short_rate + domestic_term_premium + domestic_credit_premium
total_foreign_return = foreign_short_rate + foreign_term_premium + foreign_credit_premium

# Step 3: Calculate return differential
return_differential = total_foreign_return - total_domestic_return

# Step 4: Apply Dornbusch overshooting - capital flows to higher return market
# Higher foreign return → FOR appreciates → DOM/FOR decreases
forecast_rate = spot_rate * (1 - return_differential)

forecast_rate
```

**Common Bugs to Avoid:**
- Reversing the direction: adding the differential instead of subtracting when foreign returns are higher
- Confusing which currency strengthens: higher foreign returns strengthen FOR, not DOM
- Forgetting to sum all components of total return (rates, premiums, spreads)
- Using print() instead of returning the expression value

---

## Pattern: APT_Arbitrage_Synthetic_Portfolio_Construction

**Description:** Under Arbitrage Pricing Theory, portfolios with identical systematic risk (beta) must have identical expected returns. Arbitrage involves creating a synthetic portfolio with the same beta by combining the risk-free asset and market portfolio, then exploiting return differentials.

**When to Use:** Questions about arbitrage opportunities with well-diversified portfolios, beta comparisons, and APT; keywords include "arbitrage opportunity," "well diversified," "beta," "risk-free."

**Procedure:**
1. Formula: E(R_synthetic) = R_f + β_target × [E(R_market) - R_f]
2. Identify the risk-free rate and market portfolio return
3. Calculate expected return of synthetic portfolio (Portfolio G) with target beta using CAPM/APT
4. Compare synthetic portfolio return to actual portfolio return with same beta
5. If returns differ, arbitrage exists: buy underpriced, sell overpriced
6. Calculate arbitrage profit as the return differential

**Code Example:**

**Scenario:** Portfolio A (market proxy): E(r) = 10%, beta = 1.0. Portfolio F (risk-free): E(r) = 4%, beta = 0.0. Portfolio E: E(r) = 7%, beta = 0.5. Check for arbitrage.

**Correct Code:**
```python
# Step 1: Define given portfolios
r_market = 0.10  # Portfolio A
beta_market = 1.0
r_risk_free = 0.04  # Portfolio F
beta_risk_free = 0.0

r_portfolio_e = 0.07
beta_portfolio_e = 0.5

# Step 2: Construct synthetic Portfolio G with same beta as E
# G = weight_rf × F + weight_market × A, where beta_G = beta_E
# beta_G = weight_market × beta_market = 0.5
weight_market = beta_portfolio_e / beta_market
weight_rf = 1 - weight_market

# Step 3: Calculate expected return of synthetic portfolio G
r_synthetic_g = weight_rf * r_risk_free + weight_market * r_market

# Step 4: Compare to Portfolio E - arbitrage profit
arbitrage_profit = r_synthetic_g - r_portfolio_e

# Step 5: Interpretation - positive means buy G, sell E
arbitrage_exists = abs(arbitrage_profit) > 0.0001

arbitrage_profit  # Should be 0.01 or 1%
```

**Common Bugs to Avoid:**
- Calculating only the return differential without constructing the synthetic portfolio
- Forgetting that weights must sum to 1 when combining risk-free and market portfolio
- Not recognizing that identical betas require identical returns in equilibrium
- Returning a boolean instead of the numeric arbitrage profit

---

## Pattern: PPP_Exchange_Rate_Directional_Forecast

**Description:** Purchasing Power Parity (PPP) predicts that currencies with higher inflation will depreciate relative to currencies with lower inflation. For exchange rates quoted as DOM/FOR (domestic per foreign), higher domestic inflation causes the rate to increase.

**When to Use:** Long-term exchange rate forecasting using inflation differentials; keywords include "purchasing power parity," "PPP," "inflation," "exchange rate forecast."

**Procedure:**
1. Formula: Future_Rate = Current_Rate × [(1 + inflation_domestic) / (1 + inflation_foreign)]^n
2. Identify current exchange rate and quote convention (DOM/FOR or FOR/DOM)
3. Identify inflation rates for domestic and foreign countries
4. Determine forecast horizon (n years)
5. Apply relative PPP formula with correct numerator/denominator based on quote convention
6. Verify direction: higher domestic inflation → domestic currency depreciates → DOM/FOR increases

**Code Example:**

**Scenario:** Current rate: 45.20 MXN/USD. Mexico inflation: 4.5% annually. US inflation: 2.0% annually. Forecast 3-year rate.

**Correct Code:**
```python
# Step 1: Define inputs
current_rate_mxn_per_usd = 45.20  # DOM/FOR where DOM=MXN, FOR=USD
inflation_mexico = 0.045  # Domestic (MXN)
inflation_us = 0.020      # Foreign (USD)
years = 3

# Step 2: Apply relative PPP formula
# Higher Mexican inflation → MXN depreciates → MXN/USD increases
future_rate = current_rate_mxn_per_usd * ((1 + inflation_mexico) / (1 + inflation_us)) ** years

# Step 3: Verify direction
inflation_differential = inflation_mexico - inflation_us
# Positive differential means domestic currency depreciates (rate increases)

future_rate  # Should be > 45.20
```

**Common Bugs to Avoid:**
- Inverting the inflation ratio (foreign/domestic instead of domestic/foreign)
- Forgetting to raise to the power of n for multi-year forecasts
- Misidentifying which currency is domestic vs foreign in the quote convention
- Using simple addition of inflation differentials instead of compounding ratios

---

## Pattern: Grinold_Kroner_Equity_Return_Decomposition

**Description:** The Grinold-Kroner model decomposes expected equity returns into dividend yield, earnings growth (which includes real GDP growth plus inflation when there's no change in profit share), and repricing effects (changes in P/E multiples).

**When to Use:** Long-term equity return forecasting using fundamental economic factors; keywords include "equity return," "GDP growth," "dividend yield," "labor productivity," "inflation."

**Procedure:**
1. Formula: E(R_equity) = Dividend_Yield + Earnings_Growth + Repricing_Effect
2. Earnings_Growth = Labor_Input_Growth + Labor_Productivity_Growth + Inflation + ΔProfit_Share
3. Repricing_Effect = ΔP/E_Multiple
4. Sum dividend yield from the data
5. Calculate nominal earnings growth by adding real growth components (labor input, productivity) and inflation
6. Add any changes in profit share or P/E multiples
7. Sum all three components for total expected equity return

**Code Example:**

**Scenario:** Dividend yield: 2.5%. Labor input growth: 1.0%. Labor productivity growth: 1.5%. Inflation: 2.0%. Change in profit share: 0%. Change in P/E: 0%. Calculate expected equity return.

**Correct Code:**
```python
# Step 1: Define components
dividend_yield = 0.025
labor_input_growth = 0.010
labor_productivity_growth = 0.015
inflation = 0.020
change_profit_share = 0.000
change_pe_multiple = 0.000

# Step 2: Calculate earnings growth (nominal)
# Real GDP growth = labor input + labor productivity
real_gdp_growth = labor_input_growth + labor_productivity_growth

# Nominal earnings growth includes inflation
earnings_growth = real_gdp_growth + inflation + change_profit_share

# Step 3: Calculate repricing effect
repricing_effect = change_pe_multiple

# Step 4: Total expected equity return (Grinold-Kroner)
expected_equity_return = dividend_yield + earnings_growth + repricing_effect

expected_equity_return  # Should be 0.07 or 7.0%
```

**Common Bugs to Avoid:**
- Excluding inflation from earnings growth calculation (treating it as separate)
- Forgetting that labor input and productivity are typically real rates, requiring inflation addition
- Omitting dividend yield from total return calculation
- Not recognizing that zero changes in profit share and P/E mean these components are zero, not that they should be excluded

---

## Pattern: Holistic_Balance_Sheet_Human_Capital_Valuation

**Description:** A holistic balance sheet includes human capital (present value of future earnings) alongside traditional financial assets. Human capital must be calculated as probability-weighted present value of future employment income, adjusted for survival probabilities and discounted at an appropriate rate.

**When to Use:** Personal wealth calculations involving total assets, retirement planning, life insurance needs; keywords include "holistic balance sheet," "human capital," "mortality," "future earnings."

**Procedure:**
1. Formula: Human_Capital = Σ [Income_t × (1 + wage_growth)^t × Survival_Prob_t] / (1 + discount_rate)^t
2. Discount_rate = risk_free_rate - occupational_volatility (or + risk premium depending on context)
3. Calculate survival probability for each future year from mortality tables
4. Project future income with wage growth for each year until retirement
5. Discount each year's probability-weighted income to present value
6. Sum human capital with traditional assets (financial + tangible) and pension value
7. Verify: human capital should be substantial for working individuals with years until retirement

**Code Example:**

**Scenario:** Current income: $200,000. Wage growth: 4%. Years to retirement: 3. Risk-free rate: 3%. Occupational volatility: 0.5%. Survival probabilities: Year 1: 0.9950, Year 2: 0.9940, Year 3: 0.9930. Traditional assets: $1,500,000. Pension value: $800,000.

**Correct Code:**
```python
# Step 1: Define inputs
current_income = 200000
wage_growth = 0.04
years_to_retirement = 3
risk_free_rate = 0.03
occupational_volatility = 0.005
traditional_assets = 1500000
pension_value = 800000

# Survival probabilities for each year
survival_probs = [0.9950, 0.9940, 0.9930]

# Step 2: Calculate discount rate
discount_rate = risk_free_rate - occupational_volatility

# Step 3: Calculate human capital (PV of future earnings)
human_capital = 0
for year in range(1, years_to_retirement + 1):
    # Income in future year
    future_income = current_income * (1 + wage_growth) ** year
    
    # Probability-weighted income
    weighted_income = future_income * survival_probs[year - 1]
    
    # Present value
    pv_income = weighted_income / (1 + discount_rate) ** year
    
    human_capital += pv_income

# Step 4: Calculate total holistic assets
total_holistic_assets = traditional_assets + pension_value + human_capital

total_holistic_assets
```

**Common Bugs to Avoid:**
- Forgetting to include human capital in total assets (using only traditional balance sheet)
- Not adjusting income for survival probabilities from mortality tables
- Using wrong discount rate (not adjusting risk-free rate for occupational volatility)
- Calculating income at start of year instead of end of year when specified
- Omitting pension value from total assets calculation

---

## Pattern: Life_Annuity_Income_Yield_Comparison

**Description:** Life annuity income yields vary by age (older purchasers receive higher yields due to shorter life expectancy), gender (females receive lower yields due to longer life expectancy), and options (period certain reduces yield). Immediate vs deferred purchase timing affects yields based on age at purchase.

**When to Use:** Comparing annuity products, longevity risk management, retirement income planning; keywords include "life annuity," "income yield," "period certain," "longevity risk."

**Procedure:**
1. Formula: Annual_Income_Yield = Annual_Payment / Premium_Paid
2. Recognize that yield increases with age at purchase (shorter life expectancy)
3. For same age, males receive higher yields than females (shorter life expectancy)
4. Period certain options reduce yields (guaranteed payments reduce insurance company's mortality credits)
5. Deferred annuities purchased later have higher yields due to older age at purchase
6. Compare yields by standardizing for premium amount and calculating percentage return

**Code Example:**

**Scenario:** Person age 50 purchases immediate annuity for $100,000, receives $6,000/year. Same person at age 60 would receive $8,500/year for same premium. With 10-year period certain at age 50: $5,200/year. Calculate and compare yields.

**Correct Code:**
```python
# Step 1: Define annuity scenarios
premium = 100000

# Scenario A: Immediate annuity at age 50
annual_payment_age_50 = 6000

# Scenario B: Immediate annuity at age 60 (deferred 10 years)
annual_payment_age_60 = 8500

# Scenario C: Immediate annuity at age 50 with 10-year period certain
annual_payment_age_50_period_certain = 5200

# Step 2: Calculate income yields
yield_age_50 = annual_payment_age_50 / premium
yield_age_60 = annual_payment_age_60 / premium
yield_age_50_period_certain = annual_payment_age_50_period_certain / premium

# Step 3: Verify relationships
# yield_age_60 > yield_age_50 (older age = higher yield)
# yield_age_50 > yield_age_50_period_certain (period certain reduces yield)

comparison = {
    'age_50_yield': yield_age_50,
    'age_60_yield': yield_age_60,
    'age_50_period_certain_yield': yield_age_50_period_certain,
    'age_effect': yield_age_60 - yield_age_50,
    'period_certain_cost': yield_age_50 - yield_age_50_period_certain
}

comparison
```

**Common Bugs to Avoid:**
- Assuming same-age individuals receive identical yields regardless of gender
- Not recognizing that deferred purchase (buying at older age) increases yield
- Thinking period certain increases yield (it actually decreases it)
- Comparing absolute payments instead of yields (percentage returns)
- Forgetting that yield calculations require dividing by premium, not just comparing payments

---

## Pattern: Interest_Rate_Linkage_Currency_Peg_Analysis

**Description:** Interest rate linkages between economies depend on currency regimes and capital mobility. Fixed pegs with unrestricted capital flows force interest rate convergence. Currency undervaluation expectations can temporarily suppress yields, while peg-break risk increases yields.

**When to Use:** International bond yield comparisons, currency regime analysis, capital flow assessments; keywords include "interest rate linkage," "currency peg," "capital flows," "bond yields."

**Procedure:**
1. Identify currency regime: fixed peg, floating, or managed
2. Assess capital mobility: restricted or unrestricted
3. For fixed peg + unrestricted capital: yields should converge (covered interest parity)
4. For expected currency appreciation: yields may be temporarily lower (expected FX gain compensates)
5. For peg-break risk: yields increase to compensate for currency risk
6. Compare actual yields to theoretical yields based on regime and expectations

**Code Example:**

**Scenario:** Country A (fixed peg to euro, unrestricted capital): yield 2.5%. Eurozone yield: 2.0%. Country B (expected 3% currency appreciation vs base): yield 1.8%. Base country yield: 5.0%. Assess linkages.

**Correct Code:**
```python
# Step 1: Define scenarios
# Country A: Fixed peg with unrestricted capital
country_a_yield = 0.025
eurozone_yield = 0.020
country_a_peg_risk_premium = country_a_yield - eurozone_yield

# Country B: Expected currency appreciation
country_b_yield = 0.018
base_country_yield = 0.050
expected_fx_appreciation = 0.03

# Step 2: Analyze interest rate linkages
# Country A: Small premium suggests peg credibility, but not perfect convergence
# Theoretical yield if perfect peg = eurozone_yield
country_a_peg_deviation = country_a_yield - eurozone_yield

# Country B: Lower yield compensated by expected FX gain
# Theoretical relationship: domestic_yield ≈ foreign_yield - expected_appreciation
country_b_theoretical_yield = base_country_yield - expected_fx_appreciation
country_b_yield_deviation = country_b_yield - country_b_theoretical_yield

analysis = {
    'country_a_peg_premium': country_a_peg_risk_premium,
    'country_b_fx_adjusted_yield': country_b_yield + expected_fx_appreciation,
    'country_b_vs_base': (country_b_yield + expected_fx_appreciation) - base_country_yield
}

analysis
```

**Common Bugs to Avoid:**
- Assuming fixed pegs always mean identical yields (peg-break risk creates premiums)
- Not adjusting for expected currency movements when comparing yields
- Ignoring capital flow restrictions that prevent interest rate arbitrage
- Reversing the sign on expected appreciation (appreciation allows lower yields, not higher)
- Treating all currency regimes identically regardless of capital mobility

---

## Pattern: Whole_Life_Policy_Cost_Comparison_NPV

**Description:** Comparing whole life insurance policies requires calculating the net present value of all cash flows: premiums (outflows), death benefit (inflow), cash value (inflow), and dividends (inflows). The net cost is the NPV of these flows discounted at an appropriate rate.

**When to Use:** Life insurance policy cost analysis, comparing policies with different structures; keywords include "whole life," "policy cost," "cash value," "dividends," "premiums."

**Procedure:**
1. Formula: NPV_Cost = PV(Premiums) - PV(Cash_Value) - PV(Dividends) - PV(Death_Benefit × Probability)
2. Calculate present value of annual premiums (paid at start of year)
3. Calculate present value of cash value at end of holding period
4. Calculate present value of annual dividends (paid at end of year, may be reinvested)
5. Optionally include probability-weighted death benefit
6. Net cost is outflows minus inflows; lower NPV cost means cheaper policy

**Code Example:**

**Scenario:** Death benefit: $250,000. Holding period: 20 years. Annual premium: $3,000 (start of year). Cash value at year 20: $45,000. Annual dividend: $600 (end of year, reinvested at 5%). Discount rate: 5%.

**Correct Code:**
```python
# Step 1: Define policy parameters
death_benefit = 250000
holding_period = 20
annual_premium = 3000
cash_value_end = 45000
annual_dividend = 600
discount_rate = 0.05
dividend_reinvestment_rate = 0.05

# Step 2: Calculate PV of premiums (annuity due - start of year)
pv_premiums = 0
for year in range(holding_period):
    pv_premiums += annual_premium / (1 + discount_rate) ** year

# Step 3: Calculate PV of cash value (single sum at end)
pv_cash_value = cash_value_end / (1 + discount_rate) ** holding_period

# Step 4: Calculate PV of dividends (ordinary annuity - end of year)
pv_dividends = 0
for year in range(1, holding_period + 1):
    pv_dividends += annual_dividend / (1 + discount_rate) ** year

# Step 5: Calculate net cost (lower is better)
net_cost = pv_premiums - pv_cash_value - pv_dividends

# Alternative: Include future value of reinvested dividends
fv_dividends_reinvested = annual_dividend * (((1 + dividend_reinvestment_rate) ** holding_period - 1) / dividend_reinvestment_rate)
pv_fv_dividends = fv_dividends_reinvested / (1 + discount_rate) ** holding_period

net_cost_with_reinvestment = pv_premiums - pv_cash_value - pv_fv_dividends

net_cost
```

**Common Bugs to Avoid:**
- Treating premiums as end-of-year payments when they're typically start-of-year (annuity due)
- Forgetting to discount cash value and dividends to present value
- Not accounting for dividend reinvestment when specified
- Including death benefit in cost comparison without probability weighting
- Using wrong discount rate (should reflect opportunity cost or policy illustration rate)