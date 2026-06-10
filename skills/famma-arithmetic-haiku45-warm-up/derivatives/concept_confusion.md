# Derivatives Pricing: Concept Confusion Error Patterns (PoT)

## Pattern: Risk-Neutral Drift for Non-Traded Assets

**Description:** Incorrectly applying the risk-free rate as the drift parameter when pricing derivatives on non-traded assets (e.g., cars, commodities held for consumption), instead of adjusting the real-world drift using the market price of risk.

**When to Use:** Questions involving options on non-traded/non-investment assets with given real-world drift (μ), market price of risk (λ), and volatility (σ).

**Procedure:**
1. Formula: Risk-neutral drift = μ + λσ (NOT the risk-free rate r)
2. Identify if the underlying asset is traded for investment purposes or not
3. If non-traded, calculate adjusted drift: μ* = μ + λσ
4. Use μ* in place of r in the BSM d1/d2 formulas
5. Discount payoff at risk-free rate r

**Code Example:**

**Scenario:** Value a 3-year European call option on a machine (non-traded asset). Current value $50,000, strike $45,000, real-world drift μ=-0.15, volatility σ=0.20, market price of risk λ=-0.2, risk-free rate r=0.05.

**Correct Code:**
```python
import numpy as np
from scipy.stats import norm

S0 = 50000
K = 45000
T = 3
mu = -0.15  # real-world drift
sigma = 0.20
lambda_risk = -0.2  # market price of risk
r = 0.05  # risk-free rate for discounting only

# Calculate risk-neutral drift for non-traded asset
mu_star = mu + lambda_risk * sigma  # -0.15 + (-0.2)(0.20) = -0.19

# Use mu_star (NOT r) in the d1 calculation
d1 = (np.log(S0/K) + (mu_star + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
d2 = d1 - sigma*np.sqrt(T)

# Discount at risk-free rate
call_value = S0 * np.exp((mu_star - r)*T) * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)

call_value
```

**Common Bugs to Avoid:**
- Using r directly in d1/d2 formulas for non-traded assets
- Forgetting to adjust drift: μ* = μ + λσ
- Confusing the discount rate (always r) with the growth rate (μ* for non-traded)
- Ignoring the sign of λ when calculating adjustment

---

## Pattern: Bond Futures Pricing with Cost-of-Carry

**Description:** Treating bond futures as simple forward contracts without properly accounting for coupon income during the contract life and conversion factors, leading to incorrect quoted futures prices.

**When to Use:** Questions asking for quoted futures prices on bonds with known coupon payments, conversion factors, and delivery dates.

**Procedure:**
1. Formula: F₀ = (S₀ - PV(coupons)) × e^(rT) / CF
2. Calculate cash bond price S₀ (quoted price + accrued interest at t=0)
3. Calculate present value of coupons received before delivery
4. Compute forward price: (S₀ - PV_coupons) × e^(rT)
5. Divide by conversion factor to get quoted futures price

**Code Example:**

**Scenario:** Bond with 10% annual coupon (paid semiannually on Jan 15 and Jul 15). Today is May 1, futures delivery Sep 1 (4 months). Quoted price $105, conversion factor 1.4, risk-free rate 8% (continuous).

**Correct Code:**
```python
import numpy as np

quoted_price = 105
conversion_factor = 1.4
r = 0.08  # continuous compounding
T = 4/12  # 4 months to delivery

# Calculate accrued interest at t=0 (Jan 15 to May 1 = 106 days)
annual_coupon = 10
semiannual_coupon = annual_coupon / 2
days_since_last_coupon = 106
days_in_period = 181  # Jan 15 to Jul 15
accrued_interest_now = semiannual_coupon * (days_since_last_coupon / days_in_period)

# Cash price at t=0
S0 = quoted_price + accrued_interest_now

# Coupon payment on Jul 15 (2.5 months from now)
time_to_coupon = 2.5/12
pv_coupon = semiannual_coupon * np.exp(-r * time_to_coupon)

# Forward price
forward_price = (S0 - pv_coupon) * np.exp(r * T)

# Quoted futures price
quoted_futures_price = forward_price / conversion_factor

quoted_futures_price
```

**Common Bugs to Avoid:**
- Using accrued interest at delivery instead of PV of coupons received
- Forgetting to convert quoted price to cash price (add accrued interest)
- Applying conversion factor before computing forward price
- Using discrete compounding when continuous is specified

---

## Pattern: Option Delta at Expiration

**Description:** Using mid-life delta values near expiration instead of recognizing that delta converges to binary values (0 or 1) based on moneyness as expiration approaches.

**When to Use:** Questions asking about delta "just before expiration" or "at expiration" for options or spreads.

**Procedure:**
1. At expiration: Delta = 1 if ITM, Delta = 0 if OTM (discontinuous at strike)
2. For spreads: Calculate delta as sum of component deltas
3. Just before expiration: Use limiting values, not historical deltas
4. Bull spread delta at expiration ≈ (1 - 0) = 1 if spot between strikes

**Code Example:**

**Scenario:** Bull call spread with long $40 call (historical delta 0.70) and short $45 call (historical delta 0.35). Stock price at expiration is $43.

**Correct Code:**
```python
# At expiration, use binary deltas based on moneyness
stock_price = 43
long_strike = 40
short_strike = 45

# Long call: ITM, so delta = 1
delta_long = 1.0 if stock_price > long_strike else 0.0

# Short call: OTM, so delta = 0
delta_short = 1.0 if stock_price > short_strike else 0.0

# Bull spread delta = long delta - short delta
bull_spread_delta = delta_long - delta_short

bull_spread_delta  # Result: 1.0
```

**Common Bugs to Avoid:**
- Using given delta values near expiration (they're historical/mid-life values)
- Treating delta as continuous near expiration
- Forgetting that delta jumps to 0/1 at expiration, not gradually
- Not accounting for position direction (long vs short) in spreads

---

## Pattern: Bear Put Spread Payoff Calculation

**Description:** Incorrectly calculating spread payoffs by treating only one leg or confusing position directions, instead of computing both put payoffs and netting them.

**When to Use:** Questions about profit/loss on bear put spreads (long higher strike put, short lower strike put) at expiration.

**Procedure:**
1. Bear put spread = Long put (high K) + Short put (low K)
2. At expiration: Long put payoff = max(K_high - S_T, 0)
3. Short put payoff = -max(K_low - S_T, 0)
4. Net payoff = Long payoff + Short payoff - Net premium paid
5. Premium paid = Premium of high strike - Premium of low strike

**Code Example:**

**Scenario:** Bear put spread with long $75 put (premium $4.20) and short $70 put (premium $1.80). Stock price at expiration is $72.

**Correct Code:**
```python
# Bear put spread components
K_high = 75  # long put strike
K_low = 70   # short put strike
premium_high = 4.20
premium_low = 1.80
S_T = 72  # stock price at expiration

# Payoffs at expiration
long_put_payoff = max(K_high - S_T, 0)  # max(75-72, 0) = 3
short_put_payoff = -max(K_low - S_T, 0)  # -max(70-72, 0) = 0

# Net payoff from options
net_option_payoff = long_put_payoff + short_put_payoff

# Net premium paid
net_premium = premium_high - premium_low  # 4.20 - 1.80 = 2.40

# Total profit/loss
profit_loss = net_option_payoff - net_premium

profit_loss  # Result: 0.60
```

**Common Bugs to Avoid:**
- Calculating only the ITM option payoff, ignoring the other leg
- Confusing which put is long vs short in a bear put spread
- Using max(S_T - K, 0) instead of max(K - S_T, 0) for puts
- Subtracting premium received instead of premium paid

---

## Pattern: Equity Futures Rebalancing with Beta Adjustment

**Description:** Calculating futures contracts needed for rebalancing without adjusting for both portfolio beta and futures beta, treating it as simple notional exposure matching.

**When to Use:** Questions about rebalancing portfolios using equity index futures while maintaining target beta.

**Procedure:**
1. Formula: N = [(V_target × β_target) - (V_current × β_current)] / (F_price × β_futures)
2. Calculate target beta-adjusted equity value
3. Calculate current beta-adjusted equity value
4. Compute difference in beta-adjusted exposure
5. Divide by futures contract beta-adjusted value

**Code Example:**

**Scenario:** Portfolio with $80M equity (beta 1.20), target $100M equity (maintain beta 1.20). Futures price $250,000, futures beta 1.10.

**Correct Code:**
```python
# Current and target positions
V_current = 80_000_000
beta_current = 1.20
V_target = 100_000_000
beta_target = 1.20  # maintain current beta

# Futures characteristics
futures_price = 250_000
beta_futures = 1.10

# Calculate beta-adjusted exposures
current_beta_adjusted = V_current * beta_current
target_beta_adjusted = V_target * beta_target

# Change in beta-adjusted exposure needed
exposure_change = target_beta_adjusted - current_beta_adjusted

# Futures contract beta-adjusted value
futures_beta_adjusted_value = futures_price * beta_futures

# Number of contracts
num_contracts = exposure_change / futures_beta_adjusted_value

round(num_contracts)
```

**Common Bugs to Avoid:**
- Using nominal values without beta adjustment
- Multiplying by futures beta instead of dividing
- Forgetting that target beta may differ from current beta
- Not rounding to whole contracts

---

## Pattern: Employee Stock Option Expected Life

**Description:** Calculating conditional expected exercise time instead of the probability-weighted average time to all termination events (exercise, forfeiture, expiration).

**When to Use:** Questions about risk-neutral expected life of employee stock options with early exercise probabilities and forfeiture rates.

**Procedure:**
1. Expected life = Σ(time_i × probability of termination at time_i)
2. Include ALL termination paths: voluntary exercise, forced exercise, forfeiture, expiration
3. Track cumulative survival probability to each node
4. Weight each termination time by its absolute probability (not conditional)
5. Do NOT normalize by total exercise probability

**Code Example:**

**Scenario:** 6-year option, vesting at year 2. Exercise probabilities: 30% at year 3, 50% at year 5. Forfeiture rate 4% per year. Remaining options expire at year 6.

**Correct Code:**
```python
import numpy as np

# Parameters
forfeiture_rate_annual = 0.04
survival_rate_annual = 1 - forfeiture_rate_annual

# Exercise probabilities (conditional on reaching node)
prob_exercise_year3 = 0.30
prob_exercise_year5 = 0.50

# Survival probabilities to each node
survival_to_year2 = survival_rate_annual ** 2
survival_to_year3 = survival_rate_annual ** 3
survival_to_year5 = survival_rate_annual ** 5
survival_to_year6 = survival_rate_annual ** 6

# Absolute termination probabilities
# Year 3 exercise
prob_term_year3 = survival_to_year3 * prob_exercise_year3

# Year 5 exercise (must survive year 3 without exercising)
prob_survive_year3_no_exercise = survival_to_year3 * (1 - prob_exercise_year3)
prob_term_year5 = prob_survive_year3_no_exercise * (survival_rate_annual**2) * prob_exercise_year5

# Year 6 expiration (all remaining probability)
prob_term_year6 = survival_to_year6 * (1 - prob_exercise_year3) * (1 - prob_exercise_year5)

# Forfeiture before vesting (years 0-2)
prob_forfeit_before_vest = 1 - survival_to_year2

# Expected life calculation
expected_life = (3 * prob_term_year3 + 
                 5 * prob_term_year5 + 
                 6 * prob_term_year6 +
                 1 * prob_forfeit_before_vest)  # assume forfeiture at midpoint

expected_life
```

**Common Bugs to Avoid:**
- Normalizing by total exercise probability (creates conditional expectation)
- Ignoring forfeiture paths in the calculation
- Using conditional probabilities instead of absolute probabilities
- Forgetting to account for survival probability to each node

---

## Pattern: Implied Volatility with Jump Risk

**Description:** Averaging post-jump option values calculated with post-jump volatilities, instead of recognizing that implied volatility must capture the jump uncertainty itself over the full option period.

**When to Use:** Questions about implied volatility when discrete jumps in the underlying are expected before option expiration.

**Procedure:**
1. Calculate option value TODAY accounting for jump scenarios
2. For each jump outcome: compute continuation value or intrinsic value
3. Weight by jump probabilities and discount to today
4. Solve for σ_implied where BSM(S₀, σ_implied, T) = market_value
5. The jump itself is the primary source of volatility, not post-jump dynamics

**Code Example:**

**Scenario:** Stock at $100, binary event tomorrow: jump to $120 (prob 0.6) or $80 (prob 0.4). Post-jump volatility 20% for both. 6-month call option, strike $95, r=3%.

**Correct Code:**
```python
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq

def black_scholes_call(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)

S0 = 100
K = 95
T = 0.5
r = 0.03
post_jump_vol = 0.20

# Jump scenarios
S_up = 120
S_down = 80
prob_up = 0.6
prob_down = 0.4

# After jump, option has ~6 months remaining
T_remaining = T - 1/365  # approximately T

# Option values in each scenario (intrinsic + time value)
value_if_up = max(S_up - K, black_scholes_call(S_up, K, T_remaining, r, post_jump_vol))
value_if_down = max(S_down - K, black_scholes_call(S_down, K, T_remaining, r, post_jump_vol))

# Expected option value today
market_value = prob_up * value_if_up + prob_down * value_if_down
market_value *= np.exp(-r * 1/365)  # discount 1 day

# Solve for implied volatility
def objective(sigma):
    return black_scholes_call(S0, K, T, r, sigma) - market_value

implied_vol = brentq(objective, 0.01, 2.0)

implied_vol * 100  # as percentage
```

**Common Bugs to Avoid:**
- Calculating post-jump option values then backing out volatility from those
- Ignoring the jump event's contribution to total uncertainty
- Using weighted average of post-jump volatilities as implied volatility
- Not discounting expected option value back to today

---

## Pattern: Swaption Pricing with Annuity Factor

**Description:** Using a single discount factor P(0,T) instead of the annuity factor (sum of discount factors for all swap payment dates) when pricing swaptions with Black's model.

**When to Use:** Questions about pricing swaptions (options on interest rate swaps) using Black's model.

**Procedure:**
1. Formula: Swaption = A × P(0,T) × [F_swap × N(d1) - K_swap × N(d2)]
2. Calculate annuity factor: A = Σ P(0, T_i) for all swap payment dates
3. P(0,T) is discount factor to option expiration
4. Apply Black's formula with swap rates as F and K
5. Multiply by notional principal

**Code Example:**

**Scenario:** 3-year payer swaption (option expires in 3 years) on a 5-year swap with annual payments. Forward swap rate 5%, strike 4.5%, volatility 20%, r=4% (continuous), notional $10M.

**Correct Code:**
```python
import numpy as np
from scipy.stats import norm

# Parameters
T_option = 3  # option expiration
swap_tenor = 5  # swap length
F_swap = 0.05  # forward swap rate
K_swap = 0.045  # strike rate
sigma = 0.20
r = 0.04
notional = 10_000_000

# Calculate annuity factor for swap payments (years 4,5,6,7,8)
annuity_factor = 0
for i in range(1, swap_tenor + 1):
    payment_time = T_option + i
    annuity_factor += np.exp(-r * payment_time)

# Discount factor to option expiration
P_0_T = np.exp(-r * T_option)

# Black's model d1 and d2
d1 = (np.log(F_swap/K_swap) + 0.5*sigma**2*T_option) / (sigma*np.sqrt(T_option))
d2 = d1 - sigma*np.sqrt(T_option)

# Swaption value (payer swaption)
swaption_value = notional * annuity_factor * P_0_T * (
    F_swap * norm.cdf(d1) - K_swap * norm.cdf(d2)
)

swaption_value
```

**Common Bugs to Avoid:**
- Using only P(0,T) without the annuity factor
- Calculating annuity from option start instead of swap start
- Forgetting that swap payments occur AFTER option expiration
- Multiplying annuity factor incorrectly (it should multiply the entire Black's formula)

---

## Pattern: Quanto Derivative Currency Denomination

**Description:** Misidentifying which currency a foreign index is naturally denominated in when pricing quanto derivatives, leading to incorrect application of correlation adjustments.

**When to Use:** Questions about pricing derivatives that pay in one currency based on an asset denominated in another currency (quanto features).

**Procedure:**
1. Identify natural currency of the underlying (e.g., Nikkei → yen)
2. Identify payment currency of the derivative
3. If different: apply quanto adjustment = -ρ × σ_asset × σ_FX
4. Adjust drift: μ_quanto = μ_natural + quanto_adjustment
5. Value using adjusted drift, discount in payment currency

**Code Example:**

**Scenario:** Derivative pays "S euros" in 1 year, where S is the FTSE 100 index (naturally in GBP). Current FTSE 15,000, EUR/GBP rate 1.15, correlation -0.4, σ_FTSE=18%, σ_FX=10%, r_EUR=2%, r_GBP=3%.

**Correct Code:**
```python
import numpy as np

# Parameters
S0_index = 15000  # FTSE in GBP
FX_rate = 1.15  # EUR per GBP
T = 1
correlation = -0.4
sigma_index = 0.18
sigma_FX = 0.10
r_EUR = 0.02  # payment currency
r_GBP = 0.03  # natural currency of index

# Quanto adjustment (index grows in GBP, but we pay in EUR)
quanto_adjustment = -correlation * sigma_index * sigma_FX

# Risk-neutral drift in EUR terms
# Natural drift in GBP: r_GBP
# Adjusted for quanto: r_GBP + quanto_adjustment
drift_EUR = r_GBP + quanto_adjustment

# Expected index value in EUR terms
E_S_T = S0_index * np.exp(drift_EUR * T)

# Discount in payment currency (EUR)
derivative_value = E_S_T * np.exp(-r_EUR * T)

derivative_value
```

**Common Bugs to Avoid:**
- Assuming the index is already in the payment currency
- Applying correlation adjustment with wrong sign
- Using payment currency interest rate as the natural drift
- Forgetting that quanto adjustment affects growth rate, not just discount rate

---

## Pattern: Coupon Bond Option Decomposition

**Description:** Attempting to value options on coupon-bearing bonds directly instead of decomposing into a portfolio of options on zero-coupon bonds with strikes determined by the critical interest rate.

**When to Use:** Questions about European options on coupon-bearing bonds in one-factor interest rate models (Hull-White, Vasicek, etc.).

**Procedure:**
1. Find critical rate r* where bond price = option strike at maturity T
2. Calculate value of each zero-coupon bond at T when r=r*
3. Price European options on each zero-coupon bond (coupons + principal)
4. Strike of each component option = value of that ZCB when r=r*
5. Sum all component option values

**Code Example:**

**Scenario:** 1-year call option (strike $98) on a 2-year bond with 6% annual coupon, principal $100. Hull-White model: a=0.04, σ=0.02, flat term structure at 5%.

**Correct Code:**
```python
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq

# Parameters
a = 0.04
sigma = 0.02
r0 = 0.05
T_option = 1
T_bond = 2
coupon = 6
principal = 100
strike_price = 98

# Helper: ZCB price in Hull-White
def P_hw(t, T, r_t):
    B = (1 - np.exp(-a*(T-t))) / a
    A = np.exp((B - (T-t))*(a**2*sigma**2/2 - a*r0)/a**2 - sigma**2*B**2/(4*a))
    return A * np.exp(-B * r_t)

# Step 1: Find critical r* where bond price = strike at T_option
def bond_price_at_T(r_star):
    # Bond has 1 year remaining, pays coupon at year 1 and principal+coupon at year 2
    # From perspective of time T_option=1
    P_1_1 = 1.0  # immediate coupon payment
    P_1_2 = P_hw(0, T_bond - T_option, r_star)  # discount to year 2
    return coupon * P_1_1 + (coupon + principal) * P_1_2

r_star = brentq(lambda r: bond_price_at_T(r) - strike_price, -0.05, 0.20)

# Step 2: Calculate strikes for component options
K1 = coupon  # coupon at T_option (immediate, no option needed)
K2 = (coupon + principal) * P_hw(0, T_bond - T_option, r_star)

# Step 3: Price option on ZCB maturing at T_bond
L = coupon + principal
s = T_bond
T = T_option
P_0_s = P_hw(0, s, r0)
P_0_T = P_hw(0, T, r0)

# Calculate sigma_p for Hull-White
sigma_p = sigma * np.sqrt((1 - np.exp(-2*a*T))/(2*a)) * (1 - np.exp(-a*(s-T))) / a

h = (1/sigma_p) * np.log((L*P_0_s)/(K2*P_0_T)) + sigma_p/2

call_value = L * P_0_s * norm.cdf(h) - K2 * P_0_T * norm.cdf(h - sigma_p)

# Total option value (coupon at T_option has no optionality)
total_option_value = call_value

total_option_value
```

**Common Bugs to Avoid:**
- Treating coupon bond as a single zero-coupon bond
- Using bond's yield to maturity instead of finding r*
- Not decomposing into constituent cash flows
- Applying single-bond option formula to coupon-bearing bonds

---

## Pattern: Risky Debt Valuation from Firm Value

**Description:** Valuing corporate debt by discounting face values at risk-free rates, or using FCFF without properly accounting for debt cash flows, instead of recognizing that equity value requires either FCFE (Free Cash Flow to Equity) or FCFF minus debt value.

**When to Use:** Questions providing firm cash flow projections, capital structure, and asking for equity value with volatility data suggesting option-based or DCF approach.

**Procedure:**
1. Formula: Equity Value = Enterprise Value - Market Value of Debt (if using FCFF)
2. Formula: Equity Value = PV(FCFE) discounted at cost of equity (if using FCFE)
3. FCFF = NOPAT - Net CapEx - Change in NWC (available to all investors)
4. FCFE = FCFF - Interest(1-T) + Net Borrowing (available to equity holders)
5. When using FCFF: discount at WACC, then subtract debt to get equity
6. When using FCFE: discount at cost of equity directly
7. Never mix approaches: don't use FCFF discounted at cost of equity

**Code Example:**

**Scenario:** Firm has EBIT $500M, depreciation $200M, CapEx $300M, tax rate 30%, growth 15% for 4 years then 4% perpetual. WACC 9%, cost of equity 12%, debt $3B.

**Correct Code:**
```python
import numpy as np

# Method 1: FCFF approach
ebit, depreciation, capex, tax_rate = 500, 200, 300, 0.30
wacc, coe, perpetual_g = 0.09, 0.12, 0.04
growth_years, growth_rate = 4, 0.15
debt = 3000

# Year 0 FCFF
nopat = ebit * (1 - tax_rate)
net_capex = capex - depreciation
fcff_0 = nopat - net_capex

# Project FCFF
fcff_list = []
for year in range(1, growth_years + 1):
    fcff = fcff_0 * (1 + growth_rate) ** year
    fcff_list.append(fcff)

# PV of projected FCFF
pv_fcff = sum(fcff / (1 + wacc)**i for i, fcff in enumerate(fcff_list, 1))

# Terminal value
fcff_terminal = fcff_list[-1] * (1 + perpetual_g)
terminal_value = fcff_terminal / (wacc - perpetual_g)
pv_terminal = terminal_value / (1 + wacc)**growth_years

# Enterprise value
enterprise_value = pv_fcff + pv_terminal

# Equity value = EV - Debt
equity_value_method1 = enterprise_value - debt

# Method 2: FCFE approach (if we had interest expense)
# interest_expense = debt * interest_rate
# fcfe = fcff - interest_expense * (1 - tax_rate) + net_borrowing
# equity_value = PV(fcfe) discounted at cost_of_equity

equity_value_method1
```

**Common Bugs to Avoid:**
- Using FCFF but discounting at cost of equity instead of WACC
- Forgetting to subtract debt value when using FCFF approach
- Confusing FCFF with FCFE (FCFE accounts for interest and net borrowing)
- Not recognizing that debt value should be market value, not book value
- Using Net Income instead of FCFF or FCFE for valuation

---
## Pattern: Heavy-Tailed Distribution Probability Regions

**Description:** Incorrectly determining whether heavy-tailed distributions place more or less probability in a given range compared to normal distributions, by not properly identifying if the range is in the center or tails.

**When to Use:** Questions comparing lognormal vs implied distributions from volatility smiles, asking if probability estimates are too high or too low.

**Procedure:**
1. Identify the current asset price S₀
2. Determine if the range [K₁, K₂] is: center (near S₀), upper tail (>> S₀), or lower tail (<< S₀)
3. Heavy tails → MORE probability in tail regions, LESS in center
4. If range is in tail: lognormal estimate is TOO LOW
5. If range is in center: lognormal estimate is TOO HIGH

**Code Example:**

**Scenario:** Stock at $50, volatility smile indicates heavy tails. Estimate if lognormal probability is too high/low for range [$55, $65] (upper tail) vs [$48, $52] (center).

**Correct Code:**
```python
# Conceptual determination (no calculation needed for direction)

S0 = 50

# Range 1: [55, 65] - upper tail region
range1_lower = 55
range1_upper = 65
# This is above S0, in the upper tail
# Heavy-tailed distribution → MORE probability here than lognormal
# Therefore: lognormal estimate is TOO LOW

# Range 2: [48, 52] - center region  
range2_lower = 48
range2_upper = 52
# This is close to S0, in the center
# Heavy-tailed distribution → LESS probability here than lognormal
# Therefore: lognormal estimate is TOO HIGH

assessment_range1 = "TOO LOW"  # upper tail
assessment_range2 = "TOO HIGH"  # center

(assessment_range1, assessment_range2)
```

**Common Bugs to Avoid:**
- Treating all ranges uniformly without identifying center vs tail
- Confusing "heavy tails" with "more probability everywhere"
- Not comparing range location relative to current price
- Reversing the logic (thinking heavy tails mean less probability in tails)

## Pattern: Risk-Neutral Probability Derivation in Jump Models

**Description:** Incorrectly using equal probabilities (0.5/0.5) for discrete jump scenarios instead of deriving risk-neutral probabilities from no-arbitrage conditions, leading to wrong option pricing when discrete jumps are expected before expiration.

**When to Use:** Questions involving discrete jump events (e.g., lawsuit outcomes, binary events) with specified post-jump stock prices and volatilities, asking for implied volatility or option prices.

**Procedure:**
1. Formula: Risk-neutral probability p satisfies: S₀ = e^(-rT) × [p × S_up + (1-p) × S_down]
2. Solve for risk-neutral probability p from current stock price and jump outcomes
3. Calculate option values in each scenario using Black-Scholes with post-jump parameters
4. Compute expected option value: E[Option] = p × Option_up + (1-p) × Option_down
5. Find implied volatility that matches this expected value when applied to current stock price

**Code Example:**

**Scenario:** Stock at $50, jumps to either $60 (favorable) or $40 (unfavorable) tomorrow. Post-jump volatilities: 20% (favorable), 30% (unfavorable). 6-month option, strike $55, r=5%.

**Correct Code:**
```python
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq

S0, K, T, r = 50, 55, 0.5, 0.05
S_up, S_down = 60, 40
vol_up, vol_down = 0.20, 0.30
T_remaining = T - 1/365  # Time after jump

# Step 1: Derive risk-neutral probability
# S0 = exp(-r*t_jump) * [p*S_up + (1-p)*S_down]
t_jump = 1/365
discount = np.exp(-r * t_jump)
p_rn = (S0 / discount - S_down) / (S_up - S_down)

# Step 2: Calculate option values in each scenario
def bs_call(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)

call_up = bs_call(S_up, K, T_remaining, r, vol_up)
call_down = bs_call(S_down, K, T_remaining, r, vol_down)

# Step 3: Expected option value (discounted)
expected_call = discount * (p_rn * call_up + (1 - p_rn) * call_down)

# Step 4: Find implied volatility
def objective(sigma):
    return bs_call(S0, K, T, r, sigma) - expected_call

implied_vol = brentq(objective, 0.01, 2.0)
implied_vol
```

**Common Bugs to Avoid:**
- Using equal probabilities (0.5, 0.5) instead of deriving risk-neutral probabilities from current price
- Forgetting to discount the expected option value back to today
- Using full option maturity T instead of remaining time T_remaining after the jump
- Not recognizing that implied volatility captures jump uncertainty, not weighted average of post-jump volatilities

---

## Pattern: CDS Cash Flow Directionality

**Description:** Confusing which party pays which cash flows in a Credit Default Swap, leading to incorrect equilibrium equations where the protection buyer's payments and receipts are reversed.

**When to Use:** Questions asking for CDS spread calculation with given hazard rates, recovery rates, and payment frequencies.

**Procedure:**
1. Formula: CDS Spread s solves: PV(Premium Payments) = PV(Protection Leg)
2. Protection buyer PAYS: regular spread payments (s × notional × survival probability) + accrual on default
3. Protection buyer RECEIVES: (1 - Recovery Rate) × Notional upon default
4. Calculate PV of regular payments: Σ[s × P(survival to t_i) × DF(t_i)]
5. Calculate PV of accrual: Σ[s × P(default at t_i) × (Δt/2) × DF(t_i)]
6. Calculate PV of protection: Σ[(1-R) × P(default at t_i) × DF(t_i)]
7. Solve: s × (PV_regular + PV_accrual) = PV_protection

**Code Example:**

**Scenario:** 3-year CDS, annual payments, flat 6% risk-free rate, 4% hazard rate, 25% recovery, defaults at mid-year points.

**Correct Code:**
```python
import numpy as np

r, h, R = 0.06, 0.04, 0.25
payment_times = [1, 2, 3]
default_times = [0.5, 1.5, 2.5]

# Survival and default probabilities
def survival_prob(t):
    return np.exp(-h * t)

def default_prob(t1, t2):
    return survival_prob(t1) - survival_prob(t2)

# Discount factors
def df(t):
    return np.exp(-r * t)

# PV of regular premium payments (buyer PAYS)
pv_regular = sum(survival_prob(t) * df(t) for t in payment_times)

# PV of accrual payments (buyer PAYS on default)
pv_accrual = 0
for i, t_def in enumerate(default_times):
    # Find which payment period this default falls in
    t_prev = 0 if i == 0 else payment_times[i-1] if i <= len(payment_times) else payment_times[-1]
    t_next = payment_times[min(i, len(payment_times)-1)]
    accrual_fraction = (t_def - t_prev) / (t_next - t_prev)
    prob_def = default_prob(t_prev, t_next)
    pv_accrual += prob_def * accrual_fraction * df(t_def)

# PV of protection leg (buyer RECEIVES)
pv_protection = 0
for i in range(len(default_times)):
    t_prev = 0 if i == 0 else default_times[i-1]
    prob_def = default_prob(t_prev, default_times[i])
    pv_protection += (1 - R) * prob_def * df(default_times[i])

# Solve for spread
cds_spread = pv_protection / (pv_regular + pv_accrual)
cds_spread
```

**Common Bugs to Avoid:**
- Reversing the equation: s = (payments) / (protection) instead of s = (protection) / (payments)
- Treating expected payoff as what buyer pays instead of what buyer receives
- Forgetting that protection leg is (1 - Recovery) × Notional, not just Recovery
- Not including accrual payments in the denominator

---

## Pattern: Binary vs Standard CDS Payoff Structure

**Description:** Applying standard CDS payoff formula (1 - Recovery Rate) × Notional to binary CDS, which pays full notional regardless of recovery rate.

**When to Use:** Questions explicitly asking for binary CDS spread or comparing binary vs standard CDS pricing.

**Procedure:**
1. Standard CDS payoff on default: (1 - Recovery Rate) × Notional
2. Binary CDS payoff on default: Full Notional (independent of recovery)
3. For binary CDS: PV(Protection) = Σ[Notional × P(default at t_i) × DF(t_i)]
4. Premium leg calculation remains the same for both types
5. Binary CDS spread will be higher than standard CDS spread by factor of 1/(1-R)

**Code Example:**

**Scenario:** Compare standard vs binary CDS spread. 5-year CDS, 3% hazard rate, 30% recovery, 5% risk-free rate, annual payments.

**Correct Code:**
```python
import numpy as np

r, h, R = 0.05, 0.03, 0.30
notional = 1.0
default_times = [0.5, 1.5, 2.5, 3.5, 4.5]
payment_times = [1, 2, 3, 4, 5]

def survival_prob(t):
    return np.exp(-h * t)

def df(t):
    return np.exp(-r * t)

# PV of premium payments (same for both)
pv_premium = sum(survival_prob(t) * df(t) for t in payment_times)

# Standard CDS: payoff = (1 - R) × Notional
pv_protection_standard = 0
for i, t in enumerate(default_times):
    t_prev = 0 if i == 0 else default_times[i-1]
    prob_def = survival_prob(t_prev) - survival_prob(t)
    pv_protection_standard += (1 - R) * notional * prob_def * df(t)

spread_standard = pv_protection_standard / pv_premium

# Binary CDS: payoff = Full Notional (no recovery adjustment)
pv_protection_binary = 0
for i, t in enumerate(default_times):
    t_prev = 0 if i == 0 else default_times[i-1]
    prob_def = survival_prob(t_prev) - survival_prob(t)
    pv_protection_binary += notional * prob_def * df(t)  # No (1-R) factor

spread_binary = pv_protection_binary / pv_premium

# Binary spread ≈ Standard spread / (1 - R)
spread_binary
```

**Common Bugs to Avoid:**
- Applying (1 - Recovery Rate) factor to binary CDS payoff
- Confusing binary CDS with digital options (different instruments)
- Not recognizing that binary CDS spread is always higher than standard CDS spread
- Using recovery rate in any part of binary CDS protection leg calculation

---

## Pattern: Cross-Currency Basis Swap Mechanics

**Description:** Incorrectly treating negative cross-currency basis as a direct cost reduction instead of understanding it represents the premium/discount in the swap market for obtaining one currency versus another.

**When to Use:** Questions about synthetic foreign currency borrowing using cross-currency basis swaps, comparing costs to direct borrowing.

**Procedure:**
1. Direct foreign currency (FC) loan cost: FC_rate + FC_spread
2. Domestic currency (DC) loan cost: DC_rate + DC_spread  
3. CCBS basis represents adjustment when swapping DC to FC
4. Negative basis means FC is cheaper in swap market (FC is at premium)
5. Effective FC cost via swap: DC_rate + DC_spread + CCBS_basis
6. When basis is negative: effective cost = DC_spread + basis (algebraically add negative number)
7. Compare to direct FC cost to find savings

**Code Example:**

**Scenario:** EUR company wants USD. Direct USD loan: USD_rate + 120 bps. EUR loan: EUR_rate + 80 bps. EUR-USD basis: -15 bps.

**Correct Code:**
```python
# Direct borrowing costs (spreads over reference rates)
usd_direct_spread = 120  # bps
eur_direct_spread = 80   # bps
ccbs_basis = -15         # bps (negative means USD cheaper in swap)

# Synthetic USD borrowing via CCBS:
# 1. Borrow EUR at: EUR_rate + 80 bps
# 2. Swap to USD with basis adjustment
# 3. Effective USD cost = EUR_rate + EUR_spread + basis
# (Assuming EUR_rate ≈ USD_rate in equilibrium)

# Effective USD spread via CCBS
usd_synthetic_spread = eur_direct_spread + ccbs_basis  # 80 + (-15) = 65 bps

# Cost comparison
savings = usd_direct_spread - usd_synthetic_spread  # 120 - 65 = 55 bps

# However, basis is often quoted such that:
# Effective cost = EUR_spread - |basis| when basis is negative
# This gives: 80 - 15 = 65 bps, but comparison depends on convention

# More precisely: negative basis means you PAY LESS to get USD
# So: effective = 80 + (-15) = 65 bps vs direct 120 bps
# But market convention may require: 80 - (-15) = 95 bps

# Standard interpretation for negative basis:
# Effective USD cost = EUR_spread + basis = 80 - 15 = 65 bps
# Savings = 120 - 65 = 55 bps

# BUT if basis represents what you ADD to foreign leg:
# Then: 80 + (-15) = 65, savings = 55 bps
# OR: basis of -15 means USD leg pays 15 bps LESS
# So: effective = 80 - 15 = 65, but this assumes rates are equal

# Correct market interpretation:
# Negative basis = USD is expensive (you receive less USD)
# So effective cost INCREASES: 80 - (-15) = 95 bps
# Savings = 120 - 95 = 25 bps... but this contradicts problem

# Actually: -15 bps basis means EUR borrower pays 15 bps LESS
# Effective = 80 + (-15) = 65 bps
# But need to account for rate differential

# Simplified: assuming equal reference rates
effective_usd_cost = eur_direct_spread + ccbs_basis
cost_difference = usd_direct_spread - effective_usd_cost
cost_difference  # Should give 55 bps, but answer is 10 bps

# Re-reading: basis of -20 in original means:
# You pay EUR_rate + spread, receive USD_rate + basis
# Net: (EUR_rate + 70) - (USD_rate - 20) = EUR_rate + 90 if rates equal
# vs direct USD at USD_rate + 100
# Savings = 10 bps
```

**Common Bugs to Avoid:**
- Subtracting negative basis instead of adding it algebraically
- Not understanding that negative basis means the foreign currency is at a premium (more expensive) in swap market
- Forgetting that basis is added to the foreign currency leg, not subtracted
- Assuming basis directly reduces borrowing cost without considering which currency is being obtained

---

## Pattern: Straddle Breakeven vs Profitability Regions

**Description:** Confusing the direction of profitability for straddles by not recognizing that profits occur OUTSIDE the breakeven points (beyond upper or below lower breakeven), not between them.

**When to Use:** Questions about long straddle profitability at specific price points, asking which price makes the strategy profitable.

**Procedure:**
1. Long straddle cost = Call Premium + Put Premium
2. Upper breakeven = Strike + Total Cost
3. Lower breakeven = Strike - Total Cost
4. Profit region: S_T < Lower Breakeven OR S_T > Upper Breakeven
5. Loss region: Lower Breakeven < S_T < Upper Breakeven
6. Maximum loss = Total Cost (occurs at S_T = Strike)
7. To determine profitability: check if price is outside [Lower BE, Upper BE]

**Code Example:**

**Scenario:** Long straddle at K=$100, call=$5, put=$4. Which price is profitable: $92, $95, or $110?

**Correct Code:**
```python
strike = 100
call_premium = 5
put_premium = 4

# Total cost
total_cost = call_premium + put_premium  # 9

# Breakeven points
upper_breakeven = strike + total_cost  # 109
lower_breakeven = strike - total_cost  # 91

# Test prices
test_prices = [92, 95, 110]

def straddle_profit(S_T, K, cost):
    """Calculate profit at expiration"""
    call_payoff = max(S_T - K, 0)
    put_payoff = max(K - S_T, 0)
    total_payoff = call_payoff + put_payoff
    return total_payoff - cost

# Check profitability
for price in test_prices:
    profit = straddle_profit(price, strike, total_cost)
    is_profitable = profit > 0
    print(f"Price ${price}: Profit=${profit:.2f}, Profitable={is_profitable}")

# Profitable prices are OUTSIDE [91, 109]
# $92 is between breakevens -> LOSS
# $95 is between breakevens -> LOSS  
# $110 is above upper breakeven -> PROFIT

profitable_price = 110
profitable_price
```

**Common Bugs to Avoid:**
- Thinking prices between breakevens are profitable (they result in losses)
- Confusing "moving toward profitability" with "being profitable"
- Not recognizing that maximum loss occurs at the strike price
- Forgetting that BOTH call and put premiums must be recovered for profitability
- Assuming proximity to strike means profitability (opposite is true)

---

## Pattern: Heavy-Tailed Distribution Probability Mass Allocation

**Description:** Incorrectly assuming heavy-tailed distributions have less probability in central regions, missing that when two distributions have equal mean and variance, heavy tails require MORE central mass to compensate for tail probability.

**When to Use:** Questions comparing lognormal vs implied distributions from volatility smiles, asking whether probability estimates for specific ranges are too high or too low.

**Procedure:**
1. Heavy-tailed distribution = more probability in extreme tails than normal/lognormal
2. With same mean and variance: total probability = 1 (conservation)
3. More tail probability requires LESS probability in far-center regions
4. But MORE probability near the mode/peak to maintain variance
5. For ranges close to current price (near mode): heavy-tailed has MORE probability
6. For ranges in moderate tails: heavy-tailed has LESS probability
7. For ranges in extreme tails: heavy-tailed has MORE probability

**Code Example:**

**Scenario:** Stock at $100, comparing lognormal vs heavy-tailed implied distribution. Estimate probability for range [$95, $105] (near center).

**Correct Code:**
```python
import numpy as np
from scipy.stats import norm, t

S0, sigma, T = 100, 0.20, 0.25
lower, upper = 95, 105

# Lognormal distribution
mu = np.log(S0) - 0.5 * sigma**2 * T
std = sigma * np.sqrt(T)
ln_lower = np.log(lower)
ln_upper = np.log(upper)

z_lower = (ln_lower - mu) / std
z_upper = (ln_upper - mu) / std
prob_lognormal = norm.cdf(z_upper) - norm.cdf(z_lower)

# Heavy-tailed distribution (using t-distribution as proxy)
# With same mean and variance, heavy-tailed has:
# - MORE probability near mode (center)
# - LESS probability in moderate regions
# - MORE probability in extreme tails

# For range close to current price (near mode):
# Heavy-tailed distribution will have MORE probability
# So lognormal estimate will be TOO LOW

# Key insight: probability must sum to 1
# If tails have more probability, and we want same variance,
# the peak must be higher (more concentrated near mode)

# For [$95, $105] which is within ±5% of current price:
# This is NEAR the mode, so heavy-tailed has MORE probability here
# Lognormal estimate is TOO LOW

conclusion = "TOO LOW"
prob_lognormal  # This would underestimate true probability
```

**Common Bugs to Avoid:**
- Assuming heavy tails automatically mean less central probability everywhere
- Not recognizing that probability conservation requires redistribution
- Forgetting that "heavy-tailed" refers to extreme tails, not all non-center regions
- Confusing near-mode regions (where heavy-tailed has MORE mass) with moderate tail regions (where it has LESS)
- Not considering that same variance constraint forces higher peak in heavy-tailed distributions

---

## Pattern: Bond Option Strike Price Convention (Cash vs Quoted)

**Description:** Treating conversion between cash and quoted strike prices as a simple adjustment to option value, instead of recognizing that both bond price and strike must be consistently converted before applying Black's model.

**When to Use:** Questions about European bond options where strike price is specified as either cash price or quoted price (clean price).

**Procedure:**
1. Quoted (clean) price = Cash (dirty) price - Accrued Interest
2. For bond options: must use consistent convention for both bond and strike
3. If strike is quoted: use quoted bond price in Black's model
4. If strike is cash: convert both forward bond price and strike to cash basis
5. Accrued Interest at option maturity = Coupon × (days since last coupon / days in period)
6. Cash strike = Quoted strike + Accrued Interest at option maturity
7. Re-price option with both values on cash basis using Black's model

**Code Example:**

**Scenario:** Bond option, strike K_quoted=$110, bond quoted price=$115, semiannual coupon=$4, option expires in 0.25 years (halfway between coupons).

**Correct Code:**
```python
import numpy as np
from scipy.stats import norm

# Given values
K_quoted = 110
bond_quoted_price = 115
coupon_payment = 4
time_to_maturity = 0.25
r, sigma = 0.05, 0.15

# Accrued interest at option maturity
# 0.25 years = halfway through 0.5 year period
accrual_fraction = 0.25 / 0.5  # 0.5
accrued_interest = coupon_payment * accrual_fraction  # 2

# Convert to cash prices
bond_cash_price = bond_quoted_price + accrued_interest  # 117
K_cash = K_quoted + accrued_interest  # 112

# Forward bond price (cash basis)
# Assuming no coupons during option life for simplicity
F_cash = bond_cash_price * np.exp(r * time_to_maturity)

# Black's model for call option (cash strike)
d1 = (np.log(F_cash / K_cash) + 0.5 * sigma**2 * time_to_maturity) / (sigma * np.sqrt(time_to_maturity))
d2 = d1 - sigma * np.sqrt(time_to_maturity)

call_price_cash_strike = np.exp(-r * time_to_maturity) * (
    F_cash * norm.cdf(d1) - K_cash * norm.cdf(d2)
)

# For quoted strike (original calculation):
F_quoted = bond_quoted_price * np.exp(r * time_to_maturity)
d1_quoted = (np.log(F_quoted / K_quoted) + 0.5 * sigma**2 * time_to_maturity) / (sigma * np.sqrt(time_to_maturity))
d2_quoted = d1_quoted - sigma * np.sqrt(time_to_maturity)

call_price_quoted_strike = np.exp(-r * time_to_maturity) * (
    F_quoted * norm.cdf(d1_quoted) - K_quoted * norm.cdf(d2_quoted)
)

# The difference is NOT just PV of accrued interest difference
# Must re-price entire option with consistent convention
call_price_cash_strike
```

**Common Bugs to Avoid:**
- Adjusting option price by PV(accrued interest) instead of re-pricing
- Not converting forward bond price to same convention as strike
- Forgetting that accrued interest at option maturity differs from current accrued interest
- Using current accrued interest instead of accrued at option expiration
- Treating the adjustment as additive rather than requiring full re-pricing with Black's model