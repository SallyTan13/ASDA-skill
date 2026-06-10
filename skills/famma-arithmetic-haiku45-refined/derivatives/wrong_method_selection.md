# DETAILED SKILL PATTERNS FOR DERIVATIVES VALUATION (PoT)

## Pattern: Net Capex Growth Projection in DCF Models

**Description:** When a problem states that "EBIT and net capex are expected to grow at X%", both components grow independently at that rate. Net capex (capex minus depreciation) should be calculated first, then projected separately, not derived by projecting gross capex and depreciation independently.

**When to Use:** DCF valuation problems where growth rates are specified for "net capex" or "EBIT and net cap ex" together; questions involving free cash flow projections with capital expenditure components.

**Procedure:**
1. Formula: FCF = EBIT × (1 - tax_rate) - Net_Capex, where Net_Capex = Capex - Depreciation
2. Calculate base year net capex as a single figure (capex - depreciation)
3. When growth rate applies to "EBIT and net capex", project each independently: EBIT_t = EBIT_0 × (1+g)^t and NetCapex_t = NetCapex_0 × (1+g)^t
4. Calculate FCF for each period using the projected values
5. Do NOT project gross capex and depreciation separately unless explicitly stated

**Code Example:**

**Scenario:** A company has EBIT of $500M, depreciation of $200M, and capex of $280M. EBIT and net capex are expected to grow at 15% annually for 3 years. Tax rate is 30%. Calculate year 1-3 free cash flows.

**Correct Code:**
```python
# Base year values
ebit_base = 500  # million
depreciation_base = 200  # million
capex_base = 280  # million
tax_rate = 0.30
growth_rate = 0.15
years = 3

# Step 1: Calculate base year net capex
net_capex_base = capex_base - depreciation_base  # 80 million

# Step 2: Calculate base year FCF (for verification)
fcf_base = ebit_base * (1 - tax_rate) - net_capex_base

# Step 3: Project FCF for years 1-3
# Both EBIT and net capex grow at the same rate
fcf_projections = []
for year in range(1, years + 1):
    ebit_projected = ebit_base * (1 + growth_rate) ** year
    net_capex_projected = net_capex_base * (1 + growth_rate) ** year
    fcf_year = ebit_projected * (1 - tax_rate) - net_capex_projected
    fcf_projections.append(fcf_year)

# Return year 3 FCF as example
fcf_projections[2]  # Year 3 FCF
```

**Common Bugs to Avoid:**
- Projecting gross capex and depreciation separately when growth rate applies to net capex
- Subtracting gross capex from after-tax EBIT instead of net capex
- Confusing "net capex" with "capex net of depreciation tax shield"
- Using print() instead of expression on last line for PoT execution

---

## Pattern: Merton Model Implied Volatility Inversion

**Description:** In structural credit models, equity is a call option on firm value. The relationship between equity volatility and firm volatility is non-linear: σ_E = (V/E) × N(d1) × σ_V. This requires iterative solving for σ_V, not simple portfolio variance formulas.

**When to Use:** Questions asking for "implied standard deviation in firm value" or "implied firm volatility" given equity volatility, debt levels, and market values; Merton model applications; structural credit risk problems.

**Procedure:**
1. Formula: σ_E = (V/E) × N(d1) × σ_V, where d1 = [ln(V/D) + (r + 0.5×σ_V²)×T] / (σ_V × √T)
2. Calculate market value of equity (E = stock_price × shares_outstanding)
3. Estimate firm value V = E + D (initial approximation)
4. Set up iterative solver to find σ_V that satisfies the Merton relationship
5. Use numerical methods (scipy.optimize) to solve for implied firm volatility
6. Verify result is reasonable (typically σ_V < σ_E for levered firms)

**Code Example:**

**Scenario:** A firm has equity value of $8,000M, debt of $12,000M (face value), equity volatility of 40%, risk-free rate of 4%, and debt maturity of 3 years. Find implied firm volatility.

**Correct Code:**
```python
import scipy.optimize as opt
import math

# Given values
equity_value = 8000  # million
debt_face_value = 12000  # million
equity_volatility = 0.40
risk_free_rate = 0.04
debt_maturity = 3  # years

# Initial estimate of firm value
firm_value_initial = equity_value + debt_face_value

# Define the Merton model equation to solve
def merton_equation(sigma_v):
    V = firm_value_initial  # Use iterative approach for precision
    D = debt_face_value
    T = debt_maturity
    r = risk_free_rate
    
    # Calculate d1
    d1 = (math.log(V / D) + (r + 0.5 * sigma_v**2) * T) / (sigma_v * math.sqrt(T))
    
    # Calculate N(d1) using cumulative normal distribution
    from scipy.stats import norm
    N_d1 = norm.cdf(d1)
    
    # Merton relationship: sigma_E = (V/E) * N(d1) * sigma_V
    implied_equity_vol = (V / equity_value) * N_d1 * sigma_v
    
    # Return difference from observed equity volatility
    return implied_equity_vol - equity_volatility

# Solve for firm volatility using root finding
# Initial guess: firm vol is lower than equity vol
initial_guess = 0.25
result = opt.fsolve(merton_equation, initial_guess)
implied_firm_volatility = result[0]

implied_firm_volatility
```

**Common Bugs to Avoid:**
- Using simple portfolio variance formula: σ_V² = w_E²×σ_E² + w_D²×σ_D² + 2×w_E×w_D×ρ×σ_E×σ_D
- Forgetting to import scipy.stats.norm for cumulative normal distribution
- Not iterating on firm value V (should update V based on Black-Scholes equity value)
- Using linear approximations instead of proper option delta N(d1)
- Missing the leverage effect: (V/E) ratio amplifies volatility

---

## Pattern: Interest Rate Swap Duration Calculation

**Description:** The modified duration of a pay-fixed swap equals the duration of the floating leg minus the duration of the fixed leg. The floating leg duration is approximately the time to next reset divided by 2 (for mid-period approximation), NOT simply the full reset period.

**When to Use:** Questions asking for "duration of interest rate swap", "modified duration of pay-fixed swap", or swap duration for portfolio hedging; problems involving swap-based duration management.

**Procedure:**
1. Formula: Duration_swap = Duration_floating - Duration_fixed (for pay-fixed swap)
2. Calculate fixed leg duration using the given bond duration with same maturity and coupon
3. Calculate floating leg duration ≈ (time_to_next_reset) / 2 for semi-annual payments ≈ 0.25 years
4. For pay-fixed swap: Duration = -Duration_fixed + Duration_floating (negative because paying fixed)
5. Verify sign: pay-fixed swaps have negative duration (lose value when rates fall)

**Code Example:**

**Scenario:** A 5-year pay-fixed interest rate swap with quarterly payments has a fixed rate of 6.5%. A 5-year bond with 6.5% coupon (quarterly) has modified duration of 4.12 years. Calculate swap duration.

**Correct Code:**
```python
# Given values
swap_maturity = 5  # years
payment_frequency = 4  # quarterly
fixed_rate = 0.065
fixed_bond_duration = 4.12  # years (given for equivalent bond)

# Step 1: Calculate floating leg duration
# For floating rate instruments, duration ≈ time to next reset / 2
# With quarterly payments, time to next reset = 1/4 year = 0.25 years
time_to_next_reset = 1 / payment_frequency  # 0.25 years
floating_leg_duration = time_to_next_reset / 2  # Mid-period approximation

# Alternative precise formula for floating leg:
# Duration_float = (1 + r/n) / (2*n) where n is payment frequency per year
# For quarterly: (1 + r/4) / 8 ≈ 0.125 to 0.13 depending on rate
# Using simplified approximation:
floating_leg_duration = 0.25 / 2  # 0.125 years

# Step 2: Calculate swap duration (pay-fixed perspective)
# Pay-fixed swap: short the fixed leg, long the floating leg
# Duration = Duration_floating - Duration_fixed
swap_duration = floating_leg_duration - fixed_bond_duration

# Round to 2 decimal places
swap_duration_rounded = round(swap_duration, 2)

swap_duration_rounded
```

**Common Bugs to Avoid:**
- Using full reset period (0.5 years for semi-annual) instead of half-period (0.25 years)
- Forgetting the negative sign for pay-fixed swaps
- Confusing pay-fixed vs receive-fixed perspectives (signs flip)
- Using zero for floating leg duration (it's small but non-zero)
- Not matching payment frequency between swap and reference bond

---

## Pattern: Notional Principal Calculation for Duration Hedging

**Description:** To adjust portfolio duration using swaps, calculate the required notional principal using the formula: Notional = Portfolio_Value × (Target_Duration - Current_Duration) / Swap_Duration. Sign of swap duration determines pay-fixed vs receive-fixed position.

**When to Use:** Questions involving "reduce portfolio duration using swaps", "duration hedging with interest rate swaps", or "calculate notional amount for duration target"; portfolio immunization problems.

**Procedure:**
1. Formula: Notional_Principal = (Portfolio_Value × Duration_Change) / Swap_Duration
2. Calculate duration change needed: Duration_Change = Target_Duration - Current_Duration
3. Identify swap duration (typically negative for pay-fixed swaps)
4. Calculate notional: if result is positive and swap duration is negative, use pay-fixed swap
5. Verify: New_Duration = Current_Duration + (Notional/Portfolio_Value) × Swap_Duration

**Code Example:**

**Scenario:** A bond portfolio worth $20M has modified duration of 6.8 years. Target duration is 3.5 years. Available pay-fixed swap has duration of -3.2 years. Calculate required notional principal.

**Correct Code:**
```python
# Portfolio characteristics
portfolio_value = 20_000_000  # dollars
current_duration = 6.8  # years
target_duration = 3.5  # years

# Swap characteristics
swap_duration = -3.2  # years (negative for pay-fixed)

# Step 1: Calculate required duration change
duration_change = target_duration - current_duration  # -3.3 years

# Step 2: Calculate required notional principal
# Formula: Notional = Portfolio_Value × (Duration_Change / Swap_Duration)
notional_principal = portfolio_value * (duration_change / swap_duration)

# Step 3: Verify the calculation
# New duration should equal target duration
portfolio_duration_contribution = current_duration
swap_duration_contribution = (notional_principal / portfolio_value) * swap_duration
new_duration = portfolio_duration_contribution + swap_duration_contribution

# Verification check
duration_check = abs(new_duration - target_duration) < 0.01

# Return notional principal in millions
notional_in_millions = notional_principal / 1_000_000

notional_in_millions
```

**Common Bugs to Avoid:**
- Forgetting to account for negative swap duration (sign errors)
- Dividing by duration change instead of swap duration
- Not converting to same units (portfolio value and notional must match)
- Confusing the direction: reducing duration requires pay-fixed (negative duration) swap
- Missing verification step to confirm target duration is achieved

---

## Pattern: Currency Swap All-In Cost Calculation

**Description:** For currency swaps used to convert foreign currency borrowing to domestic currency, calculate the all-in cost by comparing the effective domestic rate (swap fixed rate) plus any basis differential against direct domestic borrowing costs.

**When to Use:** Questions involving "currency swap to convert loan", "effective borrowing cost with currency swap", or "compare direct borrowing vs swap-based borrowing"; cross-currency financing decisions.

**Procedure:**
1. Formula: All_In_Cost = Swap_Pay_Rate + (Foreign_Borrow_Rate - Swap_Receive_Rate)
2. Identify foreign currency borrowing rate
3. Identify swap pay rate (domestic currency) and receive rate (foreign currency)
4. Calculate basis differential: Foreign_Borrow_Rate - Swap_Receive_Rate
5. Add swap pay rate to basis differential for total effective cost
6. Compare to direct domestic borrowing rate

**Code Example:**

**Scenario:** A company can borrow $100M at 8.5% domestically or €80M at 4.2% (at current exchange rate). A 5-year currency swap allows paying 6.8% in dollars and receiving 3.5% in euros. Calculate all-in cost of foreign borrowing with swap.

**Correct Code:**
```python
# Borrowing options
domestic_borrow_rate = 0.085  # 8.5% direct domestic borrowing
foreign_borrow_rate = 0.042  # 4.2% euro borrowing

# Currency swap terms
swap_pay_rate_domestic = 0.068  # 6.8% pay in dollars
swap_receive_rate_foreign = 0.035  # 3.5% receive in euros

# Step 1: Calculate basis differential
# This is the net cost of the foreign borrowing after swap receive leg
basis_differential = foreign_borrow_rate - swap_receive_rate_foreign

# Step 2: Calculate all-in cost
# Total cost = what we pay on swap (domestic) + net foreign cost
all_in_cost = swap_pay_rate_domestic + basis_differential

# Step 3: Calculate savings vs direct domestic borrowing
savings = domestic_borrow_rate - all_in_cost

# Step 4: Convert to basis points for clarity
savings_bps = savings * 10000

# Return all-in cost as percentage
all_in_cost_percentage = all_in_cost * 100

all_in_cost_percentage
```

**Common Bugs to Avoid:**
- Forgetting to add the basis differential (foreign borrow - swap receive)
- Comparing swap pay rate directly to domestic rate (ignores foreign leg)
- Not accounting for exchange rate risk in principal repayment
- Confusing pay and receive legs of the swap
- Missing that swap converts interest payments only, not principal (unless specified)

---

## Pattern: Swaption Valuation for Future Borrowing

**Description:** A payer swaption (right to enter pay-fixed swap) locks in a maximum borrowing rate for future floating-rate loans. The exercise decision depends on comparing the exercise rate to market swap rates at option expiration.

**When to Use:** Questions involving "payer swaption to lock in rate", "buying swaption for future loan", or "hedging future borrowing costs"; forward-starting swap problems.

**Procedure:**
1. Formula: Payer_Swaption_Value = max(0, Swap_Rate_at_Expiry - Exercise_Rate) × PV_Annuity
2. Identify loan amount (notional principal of swaption)
3. Identify exercise rate (fixed rate locked in)
4. Identify option expiration (when loan will be initiated)
5. Identify underlying swap tenor (loan duration)
6. Calculate maximum effective rate = Exercise_Rate (if swaption is exercised)

**Code Example:**

**Scenario:** A company will borrow $75M in 9 months for 3 years at floating rate. Current 3-year swap rate is 5.2%. They buy a payer swaption with exercise rate 5.5%, expiring in 9 months, for a 3-year swap. If swap rate rises to 6.1% at expiration, what is the effective borrowing rate?

**Correct Code:**
```python
# Loan and swaption parameters
notional_principal = 75_000_000  # dollars
loan_tenor = 3  # years
option_expiration = 0.75  # 9 months = 0.75 years
exercise_rate = 0.055  # 5.5% fixed rate
current_swap_rate = 0.052  # 5.2% current market rate

# Scenario: swap rate at option expiration
swap_rate_at_expiry = 0.061  # 6.1%

# Step 1: Determine if swaption will be exercised
# Payer swaption is exercised if market swap rate > exercise rate
will_exercise = swap_rate_at_expiry > exercise_rate

# Step 2: Calculate effective borrowing rate
if will_exercise:
    # Exercise swaption, lock in exercise rate
    effective_fixed_rate = exercise_rate
    # Company borrows at floating, pays fixed via swap, receives floating
    # Net effect: pays fixed at exercise rate
else:
    # Don't exercise, enter swap at market rate (or stay floating)
    effective_fixed_rate = swap_rate_at_expiry

# Step 3: Calculate benefit of swaption
rate_savings = max(0, swap_rate_at_expiry - exercise_rate)

# Return effective rate as percentage
effective_rate_percentage = effective_fixed_rate * 100

effective_rate_percentage
```

**Common Bugs to Avoid:**
- Confusing payer swaption (right to pay fixed) with receiver swaption (right to receive fixed)
- Not recognizing that payer swaption caps borrowing costs (like buying a call on rates)
- Forgetting that option expiration date ≠ swap maturity date (expiration + tenor = total period)
- Comparing exercise rate to current rate instead of rate at expiration
- Missing that swaption premium is sunk cost and doesn't affect exercise decision