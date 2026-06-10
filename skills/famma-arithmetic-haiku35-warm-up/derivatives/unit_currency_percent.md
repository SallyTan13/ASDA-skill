# SKILL PATTERNS: Derivatives - Unit/Currency/Percent Conversion Errors (PoT)

## Pattern: Financial Rounding and Precision Conventions

**Description:** Financial instruments have market-specific conventions for price quotation precision (e.g., Treasury futures to 2 decimals, currency to 4 decimals, equity options to 2 decimals). Returning excessive computational precision violates market standards and fails answer matching.

**When to Use:** Any derivative pricing calculation (options, futures, swaps) where the final answer represents a quoted market price or monetary value.

**Procedure:**
1. Formula: `rounded_value = round(computed_value, decimal_places)`
2. Identify the instrument type from the question context
3. Apply appropriate rounding: Treasury bonds/futures → 2 decimals, currency → 2-4 decimals, option premiums → 2 decimals
4. Return the rounded value as the final expression

**Code Example:**

**Scenario:** Calculate a Treasury bond futures price using cost-of-carry model. Given spot price $125.50, risk-free rate 4%, time to delivery 0.5 years, conversion factor 1.15.

**Correct Code:**
```python
import math

# Given values
spot_price = 125.50
risk_free_rate = 0.04
time_to_delivery = 0.5
conversion_factor = 1.15

# Cost-of-carry futures price
futures_price_raw = (spot_price * math.exp(risk_free_rate * time_to_delivery)) / conversion_factor

# Apply Treasury futures market convention: 2 decimal places
futures_price = round(futures_price_raw, 2)

futures_price  # Expression, not print()
```

**Common Bugs to Avoid:**
- Returning raw float with 15+ decimal places (e.g., 110.8878209053838)
- Using `print()` instead of expression on last line
- Applying wrong precision (e.g., 4 decimals for bond futures)
- Rounding intermediate steps instead of only final result

---

## Pattern: Futures Contract Multiplier Application

**Description:** Futures position value changes require multiplying index point changes by the contract-specific multiplier (e.g., S&P 500 futures: $250/point, S&P MidCap: varies). Omitting the multiplier produces per-point values instead of total dollar exposure.

**When to Use:** Questions asking for dollar value change in futures positions, profit/loss calculations, or hedging with index futures contracts.

**Procedure:**
1. Formula: `Position_Change = Index_Point_Change × Contract_Multiplier × Number_of_Contracts`
2. Extract the contract multiplier from context (standard values: S&P 500 = $250, E-mini S&P = $50, etc.)
3. Calculate index point change (e.g., 1400 → 1200 = -200 points)
4. Multiply: point_change × multiplier (× contracts if multiple)
5. Return the total dollar value change

**Code Example:**

**Scenario:** An investor holds 3 S&P 500 futures contracts. The index drops from 4500 to 4350. Calculate the total position loss. S&P 500 multiplier is $250 per point.

**Correct Code:**
```python
# Given values
initial_index = 4500
final_index = 4350
num_contracts = 3
contract_multiplier = 250  # $ per index point for S&P 500

# Calculate index point change
index_point_change = final_index - initial_index  # -150 points

# Total position change
position_change = index_point_change * contract_multiplier * num_contracts

position_change  # Returns -112500 (loss of $112,500)
```

**Common Bugs to Avoid:**
- Forgetting the contract multiplier entirely (returning just point change)
- Using portfolio value or beta instead of contract multiplier
- Confusing multiplier with contract price (price is multiplier × index level)
- Not accounting for number of contracts when multiple positions exist

---

## Pattern: Contract Notional Scaling for Total Value

**Description:** Option and futures contracts specify a unit size (e.g., 1 million units, 100 shares). The per-unit calculated value must be multiplied by the contract size to obtain total dollar value.

**When to Use:** Questions asking "how much is the option worth" or "total value" when contract specifies quantity (e.g., "option for 1 million units").

**Procedure:**
1. Formula: `Total_Value = Per_Unit_Value × Contract_Size`
2. Calculate the per-unit option/futures value using appropriate model (Black-Scholes, Margrabe, etc.)
3. Extract contract size from question (e.g., "1 million units", "100 ounces")
4. Multiply per-unit value by contract size
5. Return total value (apply rounding convention)

**Code Example:**

**Scenario:** A European call option on copper gives the right to buy 25,000 pounds at $4.00/lb. Using Black-Scholes, the per-pound option value is $0.37. Calculate total option value.

**Correct Code:**
```python
# Given values
per_unit_option_value = 0.37  # $ per pound (from Black-Scholes calculation)
contract_size = 25000  # pounds

# Total option value
total_option_value = per_unit_option_value * contract_size

# Apply currency rounding (2 decimals)
total_option_value = round(total_option_value, 2)

total_option_value  # Returns 9250.00
```

**Common Bugs to Avoid:**
- Returning per-unit value when question asks for total value
- Misreading contract size (e.g., 1 million as 1000 instead of 1,000,000)
- Applying contract size to intermediate calculations instead of final value
- Forgetting to scale when contract specifies "units" or "ounces"

---

## Pattern: Time Period Annualization for Interest Rates

**Description:** Interest rate calculations require consistent time units. Converting between period rates (e.g., 180-day) and annual rates requires proper annualization formulas, not simple multiplication. Continuous vs. discrete compounding must match the problem context.

**When to Use:** Interest rate option payoffs, loan effective rates, put-call parity with non-annual periods, swap calculations.

**Procedure:**
1. Formula (discrete): `Annual_Rate = (1 + Period_Rate)^(365/Days) - 1` or `Period_Rate × (365/Days)` for simple interest
2. Formula (continuous): `Annual_Rate = Period_Rate × (365/Days)` or use `exp(r*T)` conversions
3. Identify the compounding convention (continuous, semi-annual, simple)
4. Calculate the period rate (e.g., 180-day rate from LIBOR + spread)
5. Apply correct annualization formula matching the convention
6. Return annualized rate (often as percentage, rounded to 2 decimals)

**Code Example:**

**Scenario:** A 90-day loan has an effective rate of 0.75% for the period. Calculate the annualized rate using simple interest convention.

**Correct Code:**
```python
# Given values
period_rate = 0.0075  # 0.75% for 90 days
days_in_period = 90
days_in_year = 365

# Simple interest annualization
annual_rate = period_rate * (days_in_year / days_in_period)

# Convert to percentage and round
annual_rate_percent = round(annual_rate * 100, 2)

annual_rate_percent  # Returns 3.04 (approximately 3%)
```

**Common Bugs to Avoid:**
- Using 360-day year when problem specifies 365 (or vice versa)
- Multiplying by 2 for semi-annual when period is not exactly 6 months
- Mixing continuous and discrete compounding formulas
- Forgetting to subtract 1 when using compound interest formula
- Not converting decimal to percentage when answer expects percentage

---

## Pattern: Beta-Adjusted Futures Hedge Ratio

**Description:** Adjusting portfolio allocation with futures requires accounting for both the dollar value change AND the beta relationship between the portfolio and futures contract. The number of contracts depends on target beta, current beta, futures beta, and dollar amounts.

**When to Use:** Asset allocation rebalancing with futures, beta adjustment strategies, equity/bond mix changes using index futures.

**Procedure:**
1. Formula: `N_futures = (Target_Value - Current_Value) × (Portfolio_Beta / Futures_Beta) / Futures_Price`
2. Calculate target allocation dollar amount (e.g., 60% of total portfolio)
3. Calculate current allocation dollar amount
4. Determine the dollar change needed (target - current)
5. Adjust for beta ratio: (portfolio_beta / futures_beta)
6. Divide by futures contract price to get number of contracts
7. Round to nearest whole number (can't trade fractional contracts)

**Code Example:**

**Scenario:** Portfolio has $800M in equity (beta 1.20), target is $900M equity. Use futures with price $400,000 and beta 1.10 to adjust. Calculate contracts needed.

**Correct Code:**
```python
import math

# Given values
current_equity_value = 800_000_000  # $800M
target_equity_value = 900_000_000   # $900M
portfolio_beta = 1.20
futures_beta = 1.10
futures_price = 400_000  # $400,000 per contract

# Dollar change needed
dollar_change = target_equity_value - current_equity_value  # $100M

# Beta-adjusted notional
beta_adjustment = portfolio_beta / futures_beta

# Number of contracts
num_contracts_raw = (dollar_change * beta_adjustment) / futures_price

# Round to nearest whole number
num_contracts = round(num_contracts_raw)

num_contracts  # Returns 273
```

**Common Bugs to Avoid:**
- Omitting beta adjustment (using only dollar change / futures price)
- Using portfolio beta without dividing by futures beta
- Confusing futures price with futures multiplier
- Not rounding to whole number (fractional contracts impossible)
- Using percentage allocation instead of dollar values

---

## Pattern: Accrued Interest in Bond Futures Pricing

**Description:** Bond futures pricing requires calculating accrued interest at both the current date and delivery date, using correct day-count conventions (actual/actual, 30/360). Errors in day counting or coupon period fractions lead to incorrect cost-of-carry calculations.

**When to Use:** Treasury bond futures pricing, cheapest-to-deliver calculations, invoice price computations with semi-annual coupon bonds.

**Procedure:**
1. Formula: `Futures_Price = [(Spot_Price + Accrued_Current - PV_Coupons) × exp(r×T) + Accrued_Delivery] / Conversion_Factor`
2. Identify coupon payment dates and calculate days since last coupon (for current accrued interest)
3. Calculate days from last coupon to delivery (for delivery accrued interest)
4. Compute accrued interest: `(Annual_Coupon / 2) × (Days_Elapsed / Days_In_Period)`
5. Calculate PV of any coupons paid between now and delivery
6. Apply cost-of-carry formula with continuous compounding
7. Divide by conversion factor and round to 2 decimals

**Code Example:**

**Scenario:** Bond with 6% annual coupon (paid March 1, Sept 1). Current date: April 15. Delivery: Sept 30. Spot price $120, rate 4%, conversion factor 1.10. Calculate futures price.

**Correct Code:**
```python
import math

# Given values
spot_price = 120.00
annual_coupon = 6.00  # 6% of par (assume $100 par)
semi_annual_coupon = annual_coupon / 2  # $3.00
risk_free_rate = 0.04
conversion_factor = 1.10

# Date calculations (days)
days_since_march1_to_april15 = 45  # Current accrued
days_in_coupon_period = 184  # March 1 to Sept 1 (actual/actual)
days_march1_to_sept30 = 213  # Delivery accrued
time_to_delivery = 168 / 365  # April 15 to Sept 30

# Accrued interest at current date
accrued_current = semi_annual_coupon * (days_since_march1_to_april15 / days_in_coupon_period)

# Accrued interest at delivery (Sept 30 is after Sept 1 coupon)
days_sept1_to_sept30 = 29
accrued_delivery = semi_annual_coupon * (days_sept1_to_sept30 / days_in_coupon_period)

# PV of Sept 1 coupon (received before delivery)
time_to_sept1 = 139 / 365  # April 15 to Sept 1
pv_coupon = semi_annual_coupon * math.exp(-risk_free_rate * time_to_sept1)

# Futures price calculation
cash_price_current = spot_price + accrued_current
futures_price_raw = ((cash_price_current - pv_coupon) * math.exp(risk_free_rate * time_to_delivery) + accrued_delivery) / conversion_factor

# Round to 2 decimals (Treasury convention)
futures_price = round(futures_price_raw, 2)

futures_price  # Returns quoted futures price
```

**Common Bugs to Avoid:**
- Using 30/360 when problem implies actual/actual (or vice versa)
- Forgetting to subtract PV of coupons paid before delivery
- Not adding accrued interest at delivery date
- Miscounting days between coupon dates
- Using simple interest instead of continuous compounding for cost-of-carry

---

## Pattern: Interest Rate Option Net Effective Rate

**Description:** When an interest rate call/put option is exercised, the net borrowing/lending rate is not simply the market rate minus the strike. Must account for the option payoff structure, any spread over the reference rate, and proper annualization of the resulting effective rate.

**When to Use:** Interest rate cap/floor calculations, loan hedging with rate options, effective borrowing cost with option protection.

**Procedure:**
1. Formula: `Net_Rate = Reference_Rate + Spread - max(0, Reference_Rate - Strike)` for call protection
2. Determine if option is exercised (compare market rate to strike)
3. Calculate option payoff: `max(0, Market_Rate - Strike)` for call
4. Compute net period rate: `(Strike + Spread)` if exercised, else `(Market_Rate + Spread)`
5. Annualize the period rate using appropriate convention
6. Return as percentage rounded to 2 decimals

**Code Example:**

**Scenario:** 180-day loan at LIBOR + 0.75%. Purchased rate call with strike 1.5%. If 180-day LIBOR is 2.5%, calculate effective annual rate (simple interest).

**Correct Code:**
```python
# Given values
libor_rate = 0.025  # 2.5%
strike_rate = 0.015  # 1.5%
spread = 0.0075  # 0.75%
days_in_period = 180
days_in_year = 365

# Option payoff (call is exercised since LIBOR > strike)
option_payoff = max(0, libor_rate - strike_rate)  # 0.01 (1%)

# Net period rate (option offsets rate above strike)
net_period_rate = strike_rate + spread  # 1.5% + 0.75% = 2.25%

# Annualize using simple interest
effective_annual_rate = net_period_rate * (days_in_year / days_in_period)

# Convert to percentage
effective_annual_rate_percent = round(effective_annual_rate * 100, 2)

effective_annual_rate_percent  # Returns 4.56 (or use 2x for semi-annual: 4.50%)
```

**Common Bugs to Avoid:**
- Subtracting option payoff from wrong rate component
- Not accounting for the spread over reference rate
- Using market rate instead of strike rate when option is exercised
- Incorrect annualization (multiplying by 2 when period is not exactly 180 days)
- Forgetting that option premium is sunk cost (not included in effective rate)

---

## Pattern: Combined Volatility in Exchange Options

**Description:** Margrabe exchange option formula requires combined volatility: `σ² = σ_v² + σ_u² - 2ρσ_vσ_u`. Errors in computing this term or premature rounding of d1/d2 values cause cumulative numerical errors in the final option value.

**When to Use:** Exchange options (one asset for another), currency options from foreign investor perspective, stock tender offers, commodity spread options.

**Procedure:**
1. Formula: `σ_combined = sqrt(σ_v² + σ_u² - 2ρσ_vσ_u)`
2. Extract volatilities σ_v, σ_u and correlation ρ from problem
3. Calculate combined volatility (do NOT round intermediate value)
4. Compute d1 and d2 using full precision: `d1 = [ln(V/U) + (q_u - q_v + σ²/2)T] / (σ√T)`
5. Use cumulative normal distribution N(d1), N(d2) with full precision
6. Apply Margrabe formula: `Value = V×exp(-q_v×T)×N(d1) - U×exp(-q_u×T)×N(d2)`
7. Scale by contract size if applicable, then round final result to 2 decimals

**Code Example:**

**Scenario:** Exchange option to give 50 units of asset U for 1 unit of asset V. U=$30, V=$1600, T=1 year, σ_u=25%, σ_v=18%, ρ=0.6, q_u=2%, q_v=1%, r=5%.

**Correct Code:**
```python
import math
from scipy.stats import norm

# Given values
V0 = 1600
U0 = 30
T = 1.0
sigma_v = 0.18
sigma_u = 0.25
rho = 0.6
q_v = 0.01
q_u = 0.02
contract_size = 50  # Exchange 50 units of U for 1 unit of V

# Combined volatility (do NOT round)
sigma_combined_sq = sigma_v**2 + sigma_u**2 - 2*rho*sigma_v*sigma_u
sigma_combined = math.sqrt(sigma_combined_sq)

# Adjust U for contract size
U_total = U0 * contract_size  # $1500

# d1 and d2 (full precision)
d1 = (math.log(V0 / U_total) + (q_u - q_v + sigma_combined_sq / 2) * T) / (sigma_combined * math.sqrt(T))
d2 = d1 - sigma_combined * math.sqrt(T)

# Margrabe formula
option_value_raw = V0 * math.exp(-q_v * T) * norm.cdf(d1) - U_total * math.exp(-q_u * T) * norm.cdf(d2)

# Round final result only
option_value = round(option_value_raw, 2)

option_value  # Returns exchange option value
```

**Common Bugs to Avoid:**
- Rounding combined volatility to 2-3 decimals (causes error propagation)
- Forgetting the correlation term: `-2ρσ_vσ_u`
- Using wrong sign in d1 formula (should be q_u - q_v, not q_v - q_u)
- Not adjusting U for contract size when exchanging multiple units
- Rounding d1/d2 before computing N(d1)/N(d2)

---

## Pattern: Put-Call Parity Time Fraction Consistency

**Description:** Put-call parity requires consistent time measurement for present value calculations. Using inconsistent day-count conventions (e.g., 3/12 vs. 90/365) or mixing annual/semi-annual rates causes discrepancies in the PV(Strike) term.

**When to Use:** Put-call parity calculations, synthetic position creation, option arbitrage detection, converting call prices to put prices.

**Procedure:**
1. Formula: `Put = Call + K×exp(-r×T) - S` (European, continuous compounding)
2. Identify the time period (e.g., "3 months", "90 days")
3. Convert to year fraction consistently: use 3/12 = 0.25 for monthly, or days/365 for exact
4. Ensure interest rate matches compounding convention (continuous: use exp(-r×T), discrete: use 1/(1+r)^T)
5. Calculate PV of strike with full precision
6. Apply put-call parity formula
7. Round final put value to 2 decimals

**Code Example:**

**Scenario:** Call option with 90-day maturity, strike $50, call price $4.20. Stock at $48, annual rate 4% (continuous). Calculate put value.

**Correct Code:**
```python
import math

# Given values
call_price = 4.20
strike = 50.00
stock_price = 48.00
annual_rate = 0.04  # Continuous compounding
days_to_maturity = 90
days_in_year = 365

# Time fraction (consistent with continuous compounding)
T = days_to_maturity / days_in_year  # 0.2466 (do NOT round)

# Present value of strike
pv_strike = strike * math.exp(-annual_rate * T)

# Put-call parity: Put = Call + PV(K) - S
put_price_raw = call_price + pv_strike - stock_price

# Round to 2 decimals
put_price = round(put_price_raw, 2)

put_price  # Returns put option value
```

**Common Bugs to Avoid:**
- Using 3/12 when problem specifies "90 days" (should use 90/365)
- Mixing 360-day and 365-day conventions
- Using discrete discounting (1+r)^T when rate is continuous
- Rounding time fraction T to 2 decimals (e.g., 0.25 instead of 90/365)
- Forgetting to account for dividends if stock pays them (adjust S or add PV(dividends))