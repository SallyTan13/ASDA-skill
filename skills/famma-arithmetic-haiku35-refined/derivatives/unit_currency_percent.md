# SKILL PATTERNS: Derivatives - Unit/Currency/Percent Conversion Errors (PoT)

## Pattern: Financial Rounding and Precision Conventions

**Description:** Financial instruments have market-specific conventions for price quotation precision (e.g., Treasury futures to 2 decimals, currency to 4 decimals, equity options to 2 decimals). Returning excessive computational precision violates market standards and fails answer matching. **However, intermediate calculations should maintain full precision to avoid cumulative rounding errors.**

**When to Use:** Any derivative pricing calculation (options, futures, swaps) where the final answer represents a quoted market price or monetary value.

**When NOT to Use:**
- During intermediate calculation steps (maintain full precision until final result)
- When the calculation is part of a larger multi-step problem (round only the final answer)

**Procedure:**
1. Formula: `rounded_value = round(computed_value, decimal_places)`
2. **Maintain full precision through all intermediate calculations** (d1, d2, combined volatility, present values, etc.)
3. Identify the instrument type from the question context
4. Apply appropriate rounding **only to the final result**: Treasury bonds/futures → 2 decimals, currency → 2-4 decimals, option premiums → 2 decimals
5. Return the rounded value as the final expression

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

# Cost-of-carry futures price (maintain full precision)
futures_price_raw = (spot_price * math.exp(risk_free_rate * time_to_delivery)) / conversion_factor

# Apply Treasury futures market convention: 2 decimal places (ONLY at the end)
futures_price = round(futures_price_raw, 2)

futures_price  # Expression, not print()
```

**Common Bugs to Avoid:**
- Returning raw float with 15+ decimal places (e.g., 110.8878209053838)
- **Rounding intermediate steps like d1, d2, combined volatility** (causes error propagation)
- Using `print()` instead of expression on last line
- Applying wrong precision (e.g., 4 decimals for bond futures)
- Premature rounding that prevents accurate comparison with answer choices
## Pattern: Futures Contract Multiplier Application

**Description:** Futures position value changes require multiplying index point changes by the contract-specific multiplier (e.g., S&P 500 futures: $250/point, S&P MidCap: varies). Omitting the multiplier produces per-point values instead of total dollar exposure. **This pattern applies when calculating the dollar change for an EXISTING futures position with a known or implied number of contracts, not when determining how many contracts are needed for hedging purposes.**

**When to Use:** 
- Questions asking for dollar value change in **existing** futures positions
- Profit/loss calculations on **held** futures contracts
- Questions stating "the futures position" or "a futures contract" (implying position already exists)
- Questions asking "by how much does the position change" without requiring hedge ratio calculations
- **Questions explicitly asking about position value change for a specific point drop/rise in the index**

**When NOT to Use:**
- When determining the **number of contracts needed** for hedging (use Beta-Adjusted Futures Hedge Ratio pattern instead)
- When the question asks "how many contracts" or "calculate the hedge ratio"
- When portfolio beta adjustment is required
- **When the question involves calculating the number of contracts first, then the position change** (this requires two-step calculation)

**Procedure:**
1. **Identify if number of contracts is given or implied:**
   - Explicit: "holds 3 contracts", "a futures position of 5 contracts"
   - Implicit: "the futures position", "a futures contract" (assume 1 contract)
   - **If the question asks about position change but doesn't specify contracts, you may need to calculate contracts first using portfolio value and beta**
2. **If contracts must be calculated:** Use formula `N = (Portfolio_Value × Portfolio_Beta) / (Futures_Price × Multiplier × Futures_Beta)`, round to whole number
3. Formula: `Position_Change = Index_Point_Change × Contract_Multiplier × Number_of_Contracts`
4. Extract the contract multiplier from context (standard values: S&P 500 = $250, E-mini S&P = $50, etc.)
5. Calculate index point change (e.g., 1400 → 1200 = -200 points)
6. Multiply: point_change × multiplier × contracts
7. Return the total dollar value change

**Code Example:**

**Scenario:** A trader holds a single S&P 500 futures contract. The index drops from 4500 to 4425. Calculate the position loss. S&P 500 multiplier is $250 per point.

**Correct Code:**
```python
# Given values
initial_index = 4500
final_index = 4425
num_contracts = 1  # Single contract (implied from "a futures contract")
contract_multiplier = 250  # $ per index point for S&P 500

# Calculate index point change
index_point_change = final_index - initial_index  # -75 points

# Total position change
position_change = index_point_change * contract_multiplier * num_contracts

position_change  # Returns -18750 (loss of $18,750)
```

**Common Bugs to Avoid:**
- **Confusing this with hedging calculations that require determining number of contracts from portfolio value/beta**
- **When contracts aren't specified, failing to calculate them first using portfolio parameters**
- Forgetting the contract multiplier entirely (returning just point change)
- Using portfolio value or beta when question only asks for position change on existing contracts
- Confusing multiplier with contract price (price is multiplier × index level)
- Calculating number of contracts when the question implies they already exist
- Not recognizing that "a futures contract" or "the futures position" means contracts are already held
- **Rounding contracts incorrectly (should round DOWN to avoid over-hedging, not to nearest integer)**

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

**Description:** Adjusting portfolio allocation with futures requires accounting for both the dollar value change AND the beta/duration relationship between the portfolio and futures contract. For equity futures, use beta adjustment. For bond futures, use duration adjustment with proper handling of conversion factors. The conversion factor adjusts the futures contract to a standardized deliverable bond. **For portfolio rebalancing problems, first calculate the target dollar allocation, then determine the futures position needed to bridge the gap.** **When both equity and bond allocations are being adjusted simultaneously, calculate each futures position separately using the appropriate formula for that asset class.**

**When to Use:** Asset allocation rebalancing with futures, beta adjustment strategies, equity/bond mix changes using index futures, duration-based bond portfolio hedging with Treasury futures, **portfolio rebalancing from current allocation to target allocation percentages**, **simultaneous multi-asset rebalancing**.

**When NOT to Use:**
- When the problem asks for forward/futures **pricing** rather than hedging (use cost-of-carry models instead)
- When currency arbitrage is involved requiring full cash flow analysis
- When the question involves option strategies rather than futures hedging

**Procedure:**
1. **For portfolio rebalancing (allocation change):**
   - Formula (equity): `N_futures = (ΔValue × Portfolio_Beta) / (Futures_Price × Futures_Beta)`
   - Formula (bonds): `N_futures = (ΔValue × Portfolio_Duration) / (Futures_Price × Futures_Duration)`
   - Calculate current allocation value and target allocation value
   - Determine the dollar change needed: `ΔValue = Target_Value - Current_Value`
   - **For multi-asset rebalancing: Calculate each asset class separately**

2. **For duration-based hedging (no allocation change):**
   - Formula: `N_futures = (Target_Duration_Dollar - Current_Duration_Dollar) / (CTD_Duration × CTD_Price / Conversion_Factor)`
   - Where Duration_Dollar = Modified_Duration × Portfolio_Value
   - CTD = Cheapest-to-Deliver bond

3. **Calculate target allocation dollar amount** (e.g., 40% of $55B total = $22B)
4. **Calculate current allocation dollar amount** (e.g., current $27.5B in bonds)
5. **For allocation rebalancing:**
   - Compute dollar change needed: `ΔValue = Target - Current` (e.g., $22B - $27.5B = -$5.5B)
   - This negative value means REDUCE bond exposure (sell futures)
6. **For duration hedging:**
   - Compute dollar duration change needed: `ΔDD = Target_DD - Current_DD`
   - Calculate futures dollar duration: `Futures_DD = CTD_Duration × CTD_Price / Conversion_Factor`
   - Number of contracts: `N = ΔDD / Futures_DD`
7. **For bond futures with conversion factors:**
   - **Do NOT multiply by conversion factor** - it goes in the denominator
   - Formula: `N = (ΔValue × Portfolio_Duration) / (Futures_Price × Futures_Duration)`
   - If CTD bond data is provided, use: `Futures_Duration = CTD_Duration / Conversion_Factor`
8. **Round to nearest whole number** (can't trade fractional contracts)
9. **Sign convention:** Positive = long futures, Negative = short futures

**Common Mistakes to Avoid:**
- **Confusing duration adjustment with allocation rebalancing** (allocation changes require calculating target dollar values first)
- **Inventing target duration values not specified in the problem** (if target allocation % is given, calculate target dollar value instead)
- **Multiplying by conversion factor when it should be in the denominator** (critical error for bond futures)
- **For bond futures: Using portfolio duration in the numerator when the formula requires simple notional matching**
- Using futures price instead of CTD bond price in duration calculation
- Omitting beta/duration adjustment (using only dollar change / futures price)
- Not rounding to whole number (fractional contracts impossible)
- Confusing futures contract multiplier with futures price
- Using portfolio beta without dividing by futures beta (equity futures)
- Forgetting that conversion factor adjusts CTD bond to futures standardized deliverable
- **When rebalancing both stocks and bonds, failing to calculate each position separately**

**Example (sanitized):**
> **Scenario:** A pension fund has total assets of $100M with current allocation: 70% bonds ($70M), 30% equity ($30M). Target allocation is 50% bonds, 50% equity. Bond portfolio has duration 5.5. Use bond futures with CTD duration 7.2, CTD price $96,000, conversion factor 1.12. Calculate contracts needed.
>
> **Wrong approach:** Assuming this is a duration adjustment problem
> ```python
> # WRONG: Inventing a target duration
> current_duration = 5.5
> target_duration = 6.0  # INVENTED - not in problem!
> 
> current_dd = 70_000_000 * current_duration
> target_dd = 70_000_000 * target_duration
> delta_dd = target_dd - current_dd
> 
> futures_dd = (7.2 * 96_000) / 1.12
> num_contracts = round(delta_dd / futures_dd)
> ```
>
> **Correct approach:** This is allocation rebalancing, not duration adjustment
> ```python
> # Step 1: Calculate target allocation values
> total_portfolio = 100_000_000
> current_bond_value = 70_000_000  # 70%
> target_bond_allocation = 0.50  # 50%
> target_bond_value = total_portfolio * target_bond_allocation  # $50M
> 
> # Step 2: Calculate dollar change needed
> delta_value = target_bond_value - current_bond_value  # -$20M (reduce bonds)
> 
> # Step 3: Current portfolio duration
> current_duration = 5.5
> 
> # Step 4: Calculate futures parameters
> ctd_duration = 7.2
> ctd_price = 96_000
> conversion_factor = 1.12
> 
> # For allocation rebalancing with bonds, use simple formula:
> # N = ΔValue / Futures_Price (no duration adjustment for allocation changes)
> # OR if duration matching is required:
> # N = (ΔValue × Portfolio_Duration) / (Futures_Price × Futures_Duration)
> 
> futures_price = ctd_price  # Use CTD price as futures price
> num_contracts_raw = delta_value / futures_price
> 
> # Step 5: Round to whole number
> num_contracts = round(num_contracts_raw)  # Negative = sell futures
> abs(num_contracts)  # Return absolute value if question asks "number to sell"
> ```
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

**Description:** When an interest rate call/put option is exercised, the net borrowing/lending rate must account for: (1) whether quoted rates are annual or period rates, (2) the option payoff structure, (3) any spread over the reference rate, and (4) proper annualization of the resulting effective rate. A critical distinction is whether the reference rate (e.g., LIBOR) is quoted as an annual rate or a period-specific rate. **For collar structures, the effective rate is determined by which boundary (cap or floor) is binding, not by calculating option payoffs separately.** **For effective annual rate (EAR) calculations, use compound interest formulas, not simple interest annualization.** **When calculating interest payments for a specific period, use the rate set at the BEGINNING of that period, not the end.**

**When to Use:** Interest rate cap/floor calculations, loan hedging with rate options, effective borrowing cost with option protection, FRA-based loan calculations, zero-cost collar effective rate calculations, **effective annual rate (EAR) calculations for loans with option protection**.

**When NOT to Use:** 
- When the question asks about the interest rate that **sets** the payment (use the rate from the **beginning** of the period, not the end)
- When calculating forward prices that require using **current market prices** rather than original contract prices
- When the problem involves currency arbitrage requiring full cash flow analysis including debt repayment
- **When the problem asks for option premium or option value** (use Black-Scholes or other option pricing models)

**Procedure:**
1. **Identify the relevant period:** For interest "due on" or "for the period ended" on date X, use the rate set at the **beginning** of that period (typically 6 months prior for semiannual payments)
2. **Identify rate convention:** Determine if given rates (LIBOR, strike, spread) are annual rates or period rates
3. **Convert to period rates if needed:** If rates are annual, convert to period rate: `Period_Rate = Annual_Rate × (Days_in_Period / Days_in_Year)`
4. **For collar structures:** Determine effective rate by comparing market rate to cap/floor boundaries:
   - If `Market_Rate > Cap`: Effective rate = `Cap + Spread`
   - If `Market_Rate < Floor`: Effective rate = `Floor + Spread`
   - Otherwise: Effective rate = `Market_Rate + Spread`
5. **For interest rate call options (rate caps):** 
   - If `Market_Rate > Strike`: Effective rate = `Strike + Spread` (option exercised)
   - Otherwise: Effective rate = `Market_Rate + Spread` (option not exercised)
6. **Calculate period interest:** `Interest = Principal × Effective_Period_Rate × (Days_in_Period / Days_in_Year)`
7. **If effective annual rate (EAR) requested:** 
   - Use compound interest: `EAR = (1 + Period_Rate)^(Days_in_Year / Days_in_Period) - 1`
   - Convert to percentage: `EAR_Percent = EAR × 100`
8. **If simple annualized rate requested:** `Annual_Rate = Period_Rate × (Days_in_Year / Days_in_Period)`
9. Return as percentage rounded to 2 decimals or dollar amount as requested

**Common Mistakes to Avoid:**
- **Using the rate from the END of the period instead of the BEGINNING** (e.g., using 30-Dec-13 rate for period ending 31-Dec-13, when 30-Jun-13 rate should be used)
- **Using simple interest annualization when EAR (compound interest) is requested**
- Calculating option payoffs separately for collars instead of directly applying the binding boundary
- Treating annual rates as period rates without adjustment
- Using market rate instead of capped/floored rate when collar boundaries are breached
- Not converting spread to period rate when other rates are converted
- Applying annualization factor when rates are already annual
- Using 360-day year when problem specifies 365 (or vice versa)
- Forgetting to subtract 1 when using compound interest formula for EAR

**Example (sanitized):**
> **Scenario:** A company has a 180-day loan at LIBOR + 0.75% with an interest rate call option (cap) at 2.00%. For the current 180-day period, LIBOR is set at 2.50% (annual). Calculate the effective annual rate (EAR) on a $40 million loan using actual/365 convention.
> 
> **Wrong approach:** Using simple interest annualization or not applying the cap
> ```python
> # WRONG: Not applying the cap and using simple interest
> libor_annual = 0.0250  # 2.50%
> spread_annual = 0.0075  # 0.75%
> 
> # Calculate effective rate without cap
> effective_annual = libor_annual + spread_annual  # 3.25% (WRONG - cap not applied)
> 
> # Simple interest annualization (WRONG for EAR)
> ear_wrong = effective_annual  # Just using annual rate
> ```
>
> **Correct approach:** Apply cap and use compound interest for EAR
> ```python
> # Step 1: Identify rate from beginning of period
> libor_annual = 0.0250  # 2.50% annual
> spread_annual = 0.0075  # 0.75%
> cap_rate = 0.0200  # 2.00% cap
> 
> days_in_period = 180
> days_in_year = 365
> 
> # Step 2: Convert to period rates
> libor_period = libor_annual * (days_in_period / days_in_year)
> spread_period = spread_annual * (days_in_period / days_in_year)
> cap_period = cap_rate * (days_in_period / days_in_year)
> 
> # Step 3: Apply cap logic (LIBOR 2.50% > cap 2.00%, so cap is binding)
> capped_rate_period = cap_period + spread_period  # Cap applies to LIBOR only
> 
> # Step 4: Calculate EAR using compound interest
> ear = (1 + capped_rate_period) ** (days_in_year / days_in_period) - 1
> 
> # Step 5: Convert to percentage
> ear_percent = round(ear * 100, 2)
> ```

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

## Pattern: Convertible Bond Conversion Premium Calculation

**Description:** Convertible bond conversion premium can be expressed as either a dollar amount or a percentage. The dollar-based conversion premium is the difference between the bond's market price and its conversion value. The percentage-based conversion premium is this difference divided by the conversion value. **Bond prices are conventionally quoted as percentages of par value (typically $1,000 for corporate bonds), not absolute dollar amounts.** Questions asking to "calculate the conversion premium" without specifying units typically expect the dollar amount.

**When to Use:** Convertible bond analysis, conversion premium calculations, arbitrage opportunity identification, when comparing bond price to conversion value.

**When NOT to Use:**
- When bond prices are clearly stated in absolute dollars (e.g., "bond price is $925")
- When the problem explicitly provides par value and the bond price appears to be an absolute amount

**Procedure:**
1. **Interpret bond price quotation:**
   - CHECK: If bond price < 200 AND no explicit "$" symbol or "dollars" mentioned, assume it's quoted as percentage of par
   - Convert to absolute dollars: `Bond_Price_Dollars = Bond_Price_Quote × (Par_Value / 100)`
   - Standard par value is $1,000 unless otherwise specified
   - If bond price > 200 OR explicitly stated in dollars, assume it's already in absolute dollars
2. **Calculate conversion value:** `Conversion_Value = Stock_Price × Conversion_Ratio`
3. **Identify the required output format:**
   - If question asks for "conversion premium" without units → dollar amount
   - If question asks for "conversion premium %" or "percentage" → percentage
   - If answer choices show $ symbols → dollar amount
   - If answer choices show % symbols → percentage
4. **Calculate dollar premium:** `Premium_Dollar = Bond_Price_Dollars - Conversion_Value`
5. **If percentage needed:** `Premium_Percent = (Premium_Dollar / Conversion_Value) × 100`
6. **Apply sign convention:** Positive premium means bond trades above conversion value (typical); negative means below
7. Round to 2 decimals and return in requested format

**Example (sanitized):**
> **Scenario:** A convertible bond is quoted at 92.50 (percentage of par). The underlying stock price is $38, and the conversion ratio is 22 shares per bond. Par value is $1,000. Calculate the conversion premium.
>
> **Wrong approach:** Treating quoted price as absolute dollars
> ```python
> stock_price = 38.00
> conversion_ratio = 22
> bond_price = 92.50  # WRONG: treating as absolute dollars
> 
> conversion_value = stock_price * conversion_ratio  # 836.00
> premium_dollar = bond_price - conversion_value  # -743.50 (WRONG)
> ```
>
> **Correct approach:** Convert percentage-of-par to absolute dollars first
> ```python
> stock_price = 38.00
> conversion_ratio = 22
> bond_price_quote = 92.50  # Quoted as percentage of par
> par_value = 1000.00
> 
> # Step 1: CHECK if price needs conversion (92.50 < 200 and no $ symbol, so yes)
> bond_price_dollars = bond_price_quote * (par_value / 100)  # 925.00
> 
> # Step 2: Calculate conversion value
> conversion_value = stock_price * conversion_ratio  # 836.00
> 
> # Step 3: Question asks for "conversion premium" without % → dollar amount
> 
> # Step 4: Calculate dollar premium
> premium_dollar = bond_price_dollars - conversion_value  # 89.00
> 
> # Step 5: Round to 2 decimals
> conversion_premium = round(premium_dollar, 2)  # 89.00
> ```

**Common Mistakes to Avoid:**
- **Treating percentage-of-par quotes as absolute dollar amounts** (most critical error)
- Not checking if bond price < 200 to determine quotation convention
- **Assuming ALL bond prices are percentage-of-par without checking context**
- Returning percentage when dollar amount is expected (or vice versa)
- Using incorrect sign (premium should be positive when bond > conversion value)
- Dividing by bond price instead of conversion value for percentage calculation
- Forgetting to multiply by 100 when converting to percentage
- Not checking answer format hints ($ vs % in options)

---
## Pattern: Currency Futures Pricing with Interest Rate Parity

**Description:** Currency futures prices are determined by interest rate parity, which relates spot exchange rates, domestic and foreign interest rates, and time to maturity. The formula differs based on whether rates are quoted with continuous or discrete compounding. **The key is identifying which currency is "domestic" and which is "foreign" from the perspective of the quoted exchange rate.** For quotations like A$/$ (foreign currency per domestic currency), the domestic currency's rate goes in the numerator when the domestic currency appreciates.

**When to Use:** Currency futures pricing, forward exchange rate calculations, covered interest arbitrage problems, questions asking for futures prices on currency pairs given spot rates and interest rates.

**When NOT to Use:**
- When the problem involves minimum variance hedge ratios for currency exposure (use regression coefficients directly, not interest rate parity)
- When calculating currency hedge amounts based on historical correlation/regression analysis
- When the question asks about hedging existing currency positions rather than pricing new futures contracts

**Procedure:**
1. **Identify the exchange rate quotation:** Determine if rate is quoted as Foreign/Domestic (e.g., A$/$ means Australian dollars per US dollar)
2. **Identify which rate is domestic vs. foreign:**
   - For A$/$ quotation: US is domestic (base currency), Australia is foreign
   - For $/€ quotation: Euro is domestic (base currency), US is foreign
   - **Rule: The currency AFTER the "/" is the domestic/base currency**
3. **Apply interest rate parity formula:**
   - Discrete compounding: `F = S × (1 + r_foreign) / (1 + r_domestic)`
   - Continuous compounding: `F = S × exp((r_foreign - r_domestic) × T)`
   - **Note: Foreign rate in numerator, domestic rate in denominator**
4. **Do NOT round intermediate calculations** (maintain full precision through calculation)
5. **Compare final result to answer choices** (let natural rounding determine the match)
6. Return futures price rounded to appropriate decimal places for currency (typically 3-4 decimals)

**Common Mistakes to Avoid:**
- **Reversing domestic and foreign interest rates in the formula** (most critical error - causes systematic mispricing)
- Confusing this pattern with currency hedging problems that use regression-based hedge ratios
- Premature rounding of intermediate values (causes incorrect option matching)
- Using continuous compounding formula when rates are quoted with discrete compounding
- Applying wrong time period (ensure T matches the contract maturity)
- Rounding to fixed decimals before comparing to answer choices
- **Misidentifying which currency is domestic vs. foreign** (the currency after "/" is domestic)

**Example (sanitized):**
> **Scenario:** Spot rate is 1.45 CAD/USD. Canadian risk-free rate is 3.5%, US risk-free rate is 4.2%, both annual discrete compounding. Calculate 1-year futures price.
>
> **Wrong approach:** Reversed rates
> ```python
> spot = 1.45
> r_canada = 0.035
> r_us = 0.042
> 
> # WRONG: Treating US as foreign when it's domestic for CAD/USD
> futures = spot * (1 + r_us) / (1 + r_canada)
> ```
>
> **Correct approach:** Correct rate identification
> ```python
> # For CAD/USD quotation: USD is domestic (after /), CAD is foreign
> spot = 1.45  # CAD per USD
> r_domestic = 0.042  # US rate (domestic/base)
> r_foreign = 0.035  # Canadian rate (foreign)
> T = 1.0
> 
> # Interest rate parity (discrete): foreign in numerator
> futures_price = spot * (1 + r_foreign) / (1 + r_domestic)
> # Result: 1.4402... (maintain full precision)
> ```

---
## Pattern: Currency Arbitrage Cash Flow Analysis

**Description:** Currency arbitrage problems require tracking complete cash flows including: (1) initial borrowing and conversion, (2) investment returns in foreign currency, (3) forward/futures contract obligations, and (4) repayment of initial debt with interest. **The profit/loss is the net of all cash flows, not just the difference between forward contract and final converted amount.**

**When to Use:** Currency arbitrage strategies, covered interest arbitrage profit calculations, problems involving borrowing in one currency, investing in another, and using forwards/futures to lock in exchange rates.

**Procedure:**
1. **Track initial cash flows:**
   - Amount borrowed in currency A
   - Convert to currency B at spot rate
   - Invest in currency B at foreign risk-free rate
2. **Track forward contract:**
   - Amount to be received/delivered under forward contract
   - Forward rate locked in
3. **Calculate maturity cash flows:**
   - Investment value in currency B: `Initial_Investment × (1 + r_foreign × T)`
   - Convert back to currency A using forward rate
   - Debt repayment in currency A: `Initial_Debt × (1 + r_domestic × T)`
4. **Calculate net profit/loss:**
   - `Profit = Final_Amount_Currency_A - Debt_Repayment_Currency_A`
5. Round to nearest whole unit of currency

**Common Mistakes to Avoid:**
- **Forgetting to include debt repayment with interest** (most critical error)
- Only comparing forward contract amount to final converted amount
- Not accounting for interest accrued on borrowed funds
- Using wrong interest rate for debt repayment calculation
- Confusing which currency the profit should be expressed in

**Example (sanitized):**
> **Scenario:** Borrow 200,000 EUR at 3% annual rate. Convert to USD at spot rate 1.18 USD/EUR. Invest in US at 4% annual rate for 1 year. Enter forward contract to buy 206,000 EUR at 1.16 USD/EUR. Calculate profit in EUR.
>
> **Wrong approach:** Ignoring debt repayment
> ```python
> borrowed = 200_000
> spot_rate = 1.18
> forward_rate = 1.16
> r_us = 0.04
> 
> usd_initial = borrowed * spot_rate  # 236,000 USD
> usd_final = usd_initial * (1 + r_us)  # 245,440 USD
> 
> # WRONG: Comparing to forward contract without debt repayment
> forward_cost = 206_000 * forward_rate  # 239,000 USD
> profit_usd = usd_final - forward_cost  # 6,440 USD (WRONG)
> ```
>
> **Correct approach:** Include all cash flows
> ```python
> # Initial borrowing and conversion
> borrowed_eur = 200_000
> spot_rate = 1.18  # USD/EUR
> r_eur = 0.03  # EUR rate
> r_usd = 0.04  # USD rate
> forward_rate = 1.16  # USD/EUR
> forward_amount_eur = 206_000
> 
> # Convert to USD and invest
> usd_initial = borrowed_eur * spot_rate  # 236,000 USD
> usd_final = usd_initial * (1 + r_usd)  # 245,440 USD
> 
> # Forward contract: buy EUR with USD
> usd_needed_for_forward = forward_amount_eur * forward_rate  # 239,000 USD
> usd_remaining = usd_final - usd_needed_for_forward  # 6,440 USD
> 
> # Convert remaining USD to EUR at forward rate
> eur_from_remaining = usd_remaining / forward_rate  # 5,552 EUR
> 
> # Debt repayment
> debt_repayment = borrowed_eur * (1 + r_eur)  # 206,000 EUR
> 
> # Net profit in EUR
> profit_eur = forward_amount_eur + eur_from_remaining - debt_repayment
> profit_eur = round(profit_eur)  # Final profit
> ```

---

## Pattern: Minimum Variance Currency Hedge Ratio

**Description:** When hedging currency exposure using historical regression analysis, the minimum variance hedge ratio is determined by the regression coefficient (slope) from regressing asset returns against currency changes. This coefficient directly represents the optimal hedge ratio and should be applied to the currency exposure amount without additional conversions or adjustments. **This is distinct from interest rate parity pricing and does not involve exchange rate conversions.**

**When to Use:**
- Questions involving regression analysis of asset returns vs. currency movements
- Problems stating "regression slope coefficient" or "beta of asset returns to currency changes"
- Minimum variance hedge calculations for foreign currency exposure
- Questions asking for the "short position in [currency]" to hedge an investment

**When NOT to Use:**
- Currency futures pricing problems (use Interest Rate Parity pattern)
- Problems involving interest rate differentials without regression data
- Simple currency conversion calculations

**Procedure:**
1. **Identify the regression coefficient:** Extract the slope from regression of asset returns on currency changes (e.g., "regression slope coefficient is +0.80")
2. **Identify the currency exposure:** Determine the notional amount in foreign currency (e.g., JPY 200,000,000)
3. **Apply the hedge ratio directly:** `Hedge_Amount = Currency_Exposure × Regression_Coefficient`
4. **Interpret the result:** The hedge amount is in the SAME currency units as the exposure
5. **No exchange rate conversion needed:** The regression coefficient already captures the relationship
6. Return the hedge amount in the foreign currency

**Code Example:**

**Scenario:** A portfolio holds a JPY 200,000,000 investment in a Japanese company. Historical regression of the investment's USD returns against yen changes yields a slope coefficient of 0.80. Calculate the minimum variance hedge position in yen.

**Correct Code:**
```python
# Given values
currency_exposure = 200_000_000  # JPY exposure
regression_coefficient = 0.80  # From regression analysis

# Minimum variance hedge ratio
# The regression coefficient IS the hedge ratio
hedge_amount = currency_exposure * regression_coefficient

# Result is in JPY (same currency as exposure)
hedge_amount  # Returns 160,000,000 JPY
```

**Common Mistakes to Avoid:**
- **Attempting to convert the hedge amount using arbitrary exchange rates** (the regression coefficient already accounts for the relationship)
- Dividing by exchange rates or scaling factors not present in the problem
- Confusing this with interest rate parity calculations
- Treating the regression coefficient as something other than the direct hedge ratio
- Converting to USD when the question asks for the position in foreign currency
- Over-complicating the calculation with unnecessary conversions

---

## Pattern: Forward Contract Revaluation at Intermediate Time Points

**Description:** When valuing a forward contract at an intermediate point before maturity, the forward price must be recalculated using the **current spot price** and the **remaining time to maturity**, not the original contract parameters. The original forward price is only used if calculating the contract's profit/loss (difference between original and new forward price).

**When to Use:**
- Questions asking "what is the forward price" at a time point after contract initiation
- Problems stating "X months later" or "after Y time has passed"
- Revaluation of existing forward positions
- Questions asking for the "new forward price" or "current forward price"

**When NOT to Use:**
- Initial forward contract pricing at inception
- Calculating profit/loss on a forward position (requires comparing original vs. new forward price)
- Problems asking about the original contract terms

**Procedure:**
1. **Identify the current time point:** Determine how much time has elapsed and how much remains to maturity
2. **Extract current market parameters:**
   - Current spot price (NOT the original spot price)
   - Current risk-free rate (if changed, otherwise use original)
   - Remaining time to maturity: `T_remaining = Original_Maturity - Time_Elapsed`
3. **Apply forward pricing formula with current parameters:**
   - No dividends: `F = S_current × exp(r × T_remaining)`
   - With dividends: `F = S_current × exp((r - q) × T_remaining)`
4. **Do NOT use the original spot price or original time to maturity**
5. Return the recalculated forward price

**Code Example:**

**Scenario:** A 1-year forward contract on a non-dividend stock was initiated when the stock was $40 and the rate was 5%. Six months later, the stock is $45 and the rate is still 5%. Calculate the forward price at this intermediate point.

**Correct Code:**
```python
import math

# Current parameters (6 months after initiation)
S_current = 45.00  # Current stock price (NOT original $40)
r = 0.05  # Risk-free rate (continuous)
T_remaining = 0.5  # Remaining time to maturity (6 months left)

# Forward price formula with current parameters
forward_price = S_current * math.exp(r * T_remaining)

forward_price  # Returns ~46.14
```

**Wrong approach:**
```python
# WRONG: Using original spot price and elapsed time
S_original = 40.00  # WRONG: should use current price
T_elapsed = 0.5  # WRONG: should use remaining time

forward_price = S_original * math.exp(r * T_elapsed)  # Returns ~41.01 (WRONG)
```

**Common Mistakes to Avoid:**
- **Using the original spot price instead of current spot price** (most critical error)
- Using time elapsed instead of time remaining to maturity
- Confusing forward revaluation with profit/loss calculation
- Not recognizing that "X months later" requires recalculation with current parameters
- Treating the problem as if calculating the original forward price

---