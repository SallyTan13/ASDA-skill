# Derivatives Calculation Patterns for Program of Thought (PoT)

## Pattern: Futures Contract Immunization with Conversion Factor

**Description:** When hedging with futures to immunize interest rate risk, the number of contracts must account for the conversion factor by dividing (not multiplying) the futures BPV by the conversion factor, because the conversion factor adjusts for the difference between the standardized contract and the actual deliverable bond.

**When to Use:** Questions involving immunization, duration matching, hedging with bond futures, or rebalancing portfolios using futures contracts with conversion factors.

**Procedure:**
1. Formula: `Number_of_Contracts = BPV_gap / (BPV_per_contract / Conversion_Factor)`
2. Calculate the BPV gap: `BPV_assets - BPV_liabilities`
3. Adjust futures BPV: `Adjusted_BPV = BPV_per_contract / Conversion_Factor`
4. Determine direction: if BPV_gap > 0 (excess duration in assets), SELL futures; if < 0, BUY futures
5. Calculate number of contracts and round to nearest integer

**Code Example:**

**Scenario:** A portfolio has asset BPV of $52,000 and liability BPV of $28,000. A 10-year T-note futures contract has BPV of $50 per $100,000 notional, with conversion factor 0.85.

**Correct Code:**
```python
# Step 1: Calculate BPV gap
bpv_assets = 52000
bpv_liabilities = 28000
bpv_gap = bpv_assets - bpv_liabilities

# Step 2: Adjust futures BPV for conversion factor
bpv_per_contract = 50.0  # per $100,000 notional
conversion_factor = 0.85
adjusted_bpv = bpv_per_contract / conversion_factor

# Step 3: Calculate number of contracts
num_contracts = bpv_gap / adjusted_bpv

# Step 4: Determine direction (positive gap means sell futures)
direction = "SELL" if bpv_gap > 0 else "BUY"

# Result
round(abs(num_contracts))  # 408 contracts to SELL
```

**Common Bugs to Avoid:**
- Multiplying by conversion factor instead of dividing (reverses the adjustment direction)
- Ignoring the sign of BPV_gap (determines whether to buy or sell)
- Forgetting to scale BPV_per_contract to match the notional amount
- Using print() instead of returning the expression value

---

## Pattern: Option Delta at Expiration (Binary Convergence)

**Description:** At expiration, option delta converges to discrete binary values: 1.0 for in-the-money options and 0.0 for out-of-the-money options. For spreads, calculate the net delta by summing the individual option deltas based on their moneyness, not by interpolating pre-expiration delta values.

**When to Use:** Questions asking for delta "at expiration" or "just before expiration" for options or option spreads (bull spread, bear spread, etc.).

**Procedure:**
1. Formula: `Delta_call_expiration = 1.0 if S >= K else 0.0`
2. Identify each option position in the spread (long/short, strike prices)
3. For each option, determine if ITM or OTM at the given underlying price
4. Assign delta: 1.0 for ITM calls, 0.0 for OTM calls (reverse for puts)
5. Calculate net spread delta: sum of (position_sign × option_delta)

**Code Example:**

**Scenario:** A bull call spread has long call at strike $85 and short call at strike $92. At expiration, the underlying is at $88.

**Correct Code:**
```python
# Bull spread: long lower strike, short higher strike
underlying_price = 88
long_strike = 85
short_strike = 92

# Step 1: Determine delta for each option at expiration
long_call_delta = 1.0 if underlying_price >= long_strike else 0.0
short_call_delta = 1.0 if underlying_price >= short_strike else 0.0

# Step 2: Calculate net spread delta (long +1, short -1)
net_delta = long_call_delta - short_call_delta

# Result: 1.0 - 0.0 = 1.0 (in range 0.80 to 1.00)
net_delta
```

**Common Bugs to Avoid:**
- Using pre-expiration delta values or interpolating between strikes
- Averaging deltas instead of recognizing binary convergence
- Forgetting that spread delta = long_delta - short_delta (sign matters)
- Applying continuous delta models to discrete expiration scenarios

---

## Pattern: Market Value of Debt via Present Value of Cash Flows

**Description:** Market value of debt differs from face value and must be calculated by discounting all future cash flows (coupon payments and principal) at the current market yield, not by simple division or using face value directly.

**When to Use:** Questions asking to "estimate market value of debt" when market yields differ from coupon rates, or when duration information is provided.

**Procedure:**
1. Formula: `Market_Value = Σ(Cash_Flow_t / (1 + yield)^t)`
2. Identify each debt tranche (maturity, face value, coupon rate)
3. For each tranche, calculate annual coupon payments
4. Discount each cash flow (coupons + principal) at the market yield
5. Sum present values across all tranches

**Code Example:**

**Scenario:** A firm has $5 billion debt maturing in 3 years with 4% coupon, and $3 billion maturing in 5 years with 5% coupon. Market yield is 6%.

**Correct Code:**
```python
# Debt tranche 1: $5B, 3 years, 4% coupon
face_1 = 5_000_000_000
coupon_rate_1 = 0.04
maturity_1 = 3

# Debt tranche 2: $3B, 5 years, 5% coupon
face_2 = 3_000_000_000
coupon_rate_2 = 0.05
maturity_2 = 5

market_yield = 0.06

# Calculate PV of tranche 1
pv_1 = sum(face_1 * coupon_rate_1 / (1 + market_yield)**t for t in range(1, maturity_1 + 1))
pv_1 += face_1 / (1 + market_yield)**maturity_1

# Calculate PV of tranche 2
pv_2 = sum(face_2 * coupon_rate_2 / (1 + market_yield)**t for t in range(1, maturity_2 + 1))
pv_2 += face_2 / (1 + market_yield)**maturity_2

# Total market value
total_market_value = pv_1 + pv_2
round(total_market_value / 1_000_000)  # in millions
```

**Common Bugs to Avoid:**
- Dividing face value by (1 + rate) without considering cash flow structure
- Using face value as market value when yields differ from coupon rates
- Forgetting to include both coupon payments and principal repayment
- Not discounting each cash flow to present value

---

## Pattern: CDS Valuation from Protection Buyer Perspective

**Description:** The value of a CDS to the protection buyer equals the present value of expected payoffs (received upon default) minus the present value of premium payments (paid periodically). When market spread exceeds contract spread, the buyer gains positive value.

**When to Use:** Questions asking for CDS value to protection buyer, or comparing contract spread to market spread.

**Procedure:**
1. Formula: `Value_to_Buyer = PV(Expected_Payoffs) - PV(Premium_Payments)`
2. Calculate PV of expected payoffs: `Σ(Probability_default_t × (1 - Recovery_Rate) × Notional × DF_t)`
3. Calculate PV of premium payments: `Contract_Spread × Σ(Survival_Probability_t × DF_t)`
4. Include accrual payment adjustment if default occurs mid-period
5. Subtract premium PV from payoff PV (buyer receives payoffs, pays premiums)

**Code Example:**

**Scenario:** A 3-year CDS has contract spread 120 bps, market spread 180 bps, notional $1, recovery rate 40%, hazard rate 2.5%, risk-free rate 5%.

**Correct Code:**
```python
import math

# Parameters
contract_spread = 0.0120
market_spread = 0.0180
notional = 1.0
recovery_rate = 0.40
hazard_rate = 0.025
risk_free_rate = 0.05
years = 3

# Calculate survival probabilities and default probabilities
survival_probs = [math.exp(-hazard_rate * t) for t in range(1, years + 1)]
default_probs = [math.exp(-hazard_rate * (t-1)) * (1 - math.exp(-hazard_rate)) for t in range(1, years + 1)]

# PV of expected payoffs (what buyer receives)
pv_payoffs = sum(default_probs[t] * (1 - recovery_rate) * notional * math.exp(-risk_free_rate * (t + 0.5)) 
                 for t in range(years))

# PV of premium payments at contract spread (what buyer pays)
pv_premiums = contract_spread * sum(survival_probs[t] * math.exp(-risk_free_rate * (t + 1)) 
                                     for t in range(years))

# Value to protection buyer
value_to_buyer = pv_payoffs - pv_premiums
round(value_to_buyer, 4)
```

**Common Bugs to Avoid:**
- Reversing the sign (calculating seller value instead of buyer value)
- Using market spread instead of contract spread for premium payments
- Forgetting that buyer pays premiums (negative) and receives payoffs (positive)
- Not discounting cash flows to present value

---

## Pattern: Firm Value Volatility from Equity and Debt Volatilities

**Description:** Firm value volatility must be derived from equity and debt volatilities using the portfolio variance formula, incorporating the correlation between equity and debt returns and weighting by market values.

**When to Use:** Questions asking for "implied standard deviation in firm value" given equity volatility, debt volatility, correlation, and debt ratio.

**Procedure:**
1. Formula: `σ²_firm = w²_E × σ²_E + w²_D × σ²_D + 2 × w_E × w_D × ρ × σ_E × σ_D`
2. Calculate market value weights: `w_E = Equity_MV / (Equity_MV + Debt_MV)`, `w_D = 1 - w_E`
3. Or use debt ratio directly: `w_D = Debt_Ratio`, `w_E = 1 - Debt_Ratio`
4. Compute variance using portfolio formula with correlation term
5. Take square root to get firm volatility: `σ_firm = √(σ²_firm)`

**Code Example:**

**Scenario:** Equity volatility is 40%, debt volatility is 12%, correlation is 0.6, and debt ratio is 55%. Calculate firm value volatility.

**Correct Code:**
```python
import math

# Given parameters
sigma_equity = 0.40
sigma_debt = 0.12
correlation = 0.6
debt_ratio = 0.55

# Calculate weights
w_debt = debt_ratio
w_equity = 1 - debt_ratio

# Portfolio variance formula
variance_firm = (w_equity**2 * sigma_equity**2 + 
                 w_debt**2 * sigma_debt**2 + 
                 2 * w_equity * w_debt * correlation * sigma_equity * sigma_debt)

# Firm volatility
sigma_firm = math.sqrt(variance_firm)
round(sigma_firm, 4)  # 0.2089 or 20.89%
```

**Common Bugs to Avoid:**
- Omitting the correlation term (2 × w_E × w_D × ρ × σ_E × σ_D)
- Using simple weighted average instead of portfolio variance formula
- Forgetting to take square root of variance to get standard deviation
- Using book values instead of market values for weights

---

## Pattern: Forward Contract Revaluation After Rate Changes

**Description:** A forward contract's value after rate changes equals the present value of the difference between the original forward price (locked in) and the new forward price (at current rates). This is not a simple bond pricing problem.

**When to Use:** Questions asking for forward contract value "after rates change" or "given these new rates."

**Procedure:**
1. Formula: `Value = (F_original - F_new) × Notional × DF_to_settlement`
2. Calculate original forward price using initial spot rates
3. Calculate new forward price using updated spot rates
4. Find the difference: `F_original - F_new`
5. Discount this difference back to present using current rates

**Code Example:**

**Scenario:** You agreed to buy a 1-year bond in 6 months at forward price $980. After rate changes, the new forward price is $965. Current 6-month rate is 4%.

**Correct Code:**
```python
# Original forward price (locked in)
forward_price_original = 980

# New forward price after rate changes
forward_price_new = 965

# Time to settlement (6 months = 0.5 years)
time_to_settlement = 0.5
current_6m_rate = 0.04

# Discount factor to settlement
discount_factor = 1 / (1 + current_6m_rate)**time_to_settlement

# Value of forward contract (long position)
value_long = (forward_price_original - forward_price_new) * discount_factor

round(value_long, 2)  # Positive value because locked in higher price
```

**Common Bugs to Avoid:**
- Treating as bond pricing problem instead of forward contract valuation
- Forgetting to discount the price difference back to present
- Using wrong sign convention (long benefits when F_original > F_new)
- Not recognizing that forward contracts have zero initial value but non-zero value after rate changes

---

## Pattern: Collar Strategy Profit with Net Premium Accounting

**Description:** A collar strategy's profit at expiration must account for the net premium paid or received upfront. Calculate: (1) stock gain/loss from entry to expiration, (2) add put payoff if stock below put strike, (3) subtract call payoff if stock above call strike, (4) subtract net premium cost (put premium paid minus call premium received). The breakeven is the initial stock price plus net premium.

**When to Use:** Questions about collar strategy profit/loss at expiration, or asking for "breakeven price" of protective put or collar positions involving long stock, long put, and short call.

**Procedure:**
1. Stock_gain = S_T - S_0
2. Put_payoff = max(K_put - S_T, 0) if long put
3. Call_payoff = -max(S_T - K_call, 0) if short call
4. Net_premium = Put_premium_paid - Call_premium_received
5. Total_profit = Stock_gain + Put_payoff + Call_payoff - Net_premium
6. Breakeven = S_0 + Net_premium (for protective put without call)

**Code Example:**

**Scenario:** You own stock purchased at $50, bought a $45 put for $2.50, and sold a $60 call for $1.80. At expiration, the stock is at $48. What is your profit per share? What is the breakeven price for just the protective put (ignoring the call)?

**Correct Code:**
```python
# Position details
S0 = 50  # initial stock price
ST = 48  # stock at expiration
K_put = 45
K_call = 60
put_premium = 2.50
call_premium = 1.80

# Net premium for collar
net_premium = put_premium - call_premium  # 0.70 paid

# Profit calculation
stock_gain = ST - S0
put_payoff = max(K_put - ST, 0)
call_payoff = -max(ST - K_call, 0)
total_profit = stock_gain + put_payoff + call_payoff - net_premium
# Result: -2 + 0 + 0 - 0.70 = -2.70

# Breakeven for protective put only (stock + put, no call)
breakeven_protective_put = S0 + put_premium
# Result: 52.50

total_profit, breakeven_protective_put
```

**Common Bugs to Avoid:**
- Calculating breakeven as strike price minus premium instead of initial stock price plus net premium
- Forgetting to subtract the net premium cost from the final profit
- Using strike price as the reference point instead of initial stock purchase price
- Ignoring the call premium received when calculating net premium for collar

---
## Pattern: Option Intrinsic Value vs. Premium at Expiration

**Description:** At expiration, an option's value equals its intrinsic value (max(S_T - K, 0) for calls), not the premium originally paid. For total investment value, multiply intrinsic value per share by shares per contract and number of contracts.

**When to Use:** Questions asking "how much is your option investment worth" at expiration, given a final stock price.

**Procedure:**
1. Formula (Call): `Intrinsic_Value = max(S_T - K, 0)`
2. Formula (Put): `Intrinsic_Value = max(K - S_T, 0)`
3. Identify option type, strike price, and expiration stock price
4. Calculate intrinsic value per share
5. Multiply by contract size (typically 100 shares) and number of contracts

**Code Example:**

**Scenario:** You own 50 call option contracts with strike $120. At expiration, stock is at $135. Each contract covers 100 shares.

**Correct Code:**
```python
# Option parameters
strike_price = 120
stock_price_at_expiration = 135
num_contracts = 50
shares_per_contract = 100

# Intrinsic value per share at expiration
intrinsic_value_per_share = max(stock_price_at_expiration - strike_price, 0)

# Total investment value
total_value = intrinsic_value_per_share * shares_per_contract * num_contracts

total_value  # $75,000
```

**Common Bugs to Avoid:**
- Using the original premium paid instead of intrinsic value at expiration
- Forgetting to multiply by shares per contract (typically 100)
- Confusing premium (time value + intrinsic value) with expiration value (intrinsic only)
- Not recognizing that out-of-the-money options expire worthless (intrinsic = 0)

---

## Pattern: Option Time Value Decomposition

**Description:** Option time value equals the option premium (market price) minus intrinsic value. Intrinsic value = max(S - K, 0) for calls and max(K - S, 0) for puts. Even out-of-the-money options have positive time value equal to their full premium, since intrinsic value is zero. This is distinct from calculating total option value or net gain.

**When to Use:** Questions explicitly asking to "calculate time value" or "find the time value component" of an option, given current stock price, strike price, and option premium.

**Procedure:**
1. Formula: Time_value = Option_premium - Intrinsic_value
2. Calculate intrinsic value: max(S - K, 0) for calls, max(K - S, 0) for puts
3. Subtract intrinsic value from the quoted premium
4. Return time value (always ≥ 0 for American/European options before expiration)

**Code Example:**

**Scenario:** A call option with strike $80 is trading at $10.50 when the stock is at $83. What is the time value?

**Correct Code:**
```python
# Option details
stock_price = 83
strike_price = 80
call_premium = 10.50

# Intrinsic value for call
intrinsic_value = max(stock_price - strike_price, 0)

# Time value
time_value = call_premium - intrinsic_value
time_value  # Result: 7.50
```

**Common Bugs to Avoid:**
- Returning the Black-Scholes theoretical value instead of decomposing the given market premium
- Confusing time value with total option value (premium)
- Using negative intrinsic values (intrinsic value has a floor of zero)
- Calculating net gain (which subtracts premium) instead of time value (which uses premium as input)

---
## Pattern: Black-Scholes Call Replication via Delta Hedging

**Description:** Replicating a call option requires constructing a portfolio of two positions: (1) buying delta (N(d1)) shares of stock, and (2) borrowing the present value of a portion of the strike price. This is a portfolio specification, not a single value.

**When to Use:** Questions asking "how would you replicate this call" using Black-Scholes inputs, or asking for a replicating portfolio.

**Procedure:**
1. Formula: `Replicating_Portfolio = Δ × S - B`, where `Δ = N(d1)` and `B = K × e^(-rT) × N(d2)`
2. Calculate d1 and d2 from Black-Scholes formula
3. Compute N(d1) using cumulative normal distribution (delta)
4. Compute N(d2) for the borrowing component
5. Specify portfolio: "Buy Δ shares, borrow $B"

**Code Example:**

**Scenario:** A call option has delta (N(d1)) = 0.65, strike $100, risk-free rate 4%, time to expiration 0.5 years, N(d2) = 0.58. Stock price is $98.

**Correct Code:**
```python
import math

# Black-Scholes parameters
delta = 0.65  # N(d1)
n_d2 = 0.58   # N(d2)
stock_price = 98
strike_price = 100
risk_free_rate = 0.04
time_to_expiration = 0.5

# Replicating portfolio components
shares_to_buy = delta
amount_to_borrow = strike_price * math.exp(-risk_free_rate * time_to_expiration) * n_d2

# Verification: portfolio value should equal call value
portfolio_value = shares_to_buy * stock_price - amount_to_borrow

# Return specification as string
f"Buy {round(shares_to_buy, 4)} shares and borrow ${round(amount_to_borrow, 2)}"
```

**Common Bugs to Avoid:**
- Returning a single number instead of portfolio specification
- Forgetting the borrowing component (only specifying delta)
- Using incorrect present value formula for borrowing amount
- Not recognizing this as a two-component portfolio construction problem

---

## Pattern: Butterfly Spread Maximum Profit Calculation

**Description:** A butterfly spread's maximum profit equals (spread width - net premium paid) × multiplier, occurring when the underlying price equals the middle strike at expiration. The spread involves buying 1 low strike, selling 2 middle strikes, buying 1 high strike.

**When to Use:** Questions asking for maximum profit of butterfly spread strategies using call or put options.

**Procedure:**
1. Formula: `Max_Profit = (Strike_Spacing - Net_Premium) × Multiplier × Contracts`
2. Identify the three strikes: low, middle, high (equally spaced)
3. Calculate net premium: `Premium_low + Premium_high - 2 × Premium_middle`
4. Calculate spread width: `Middle_Strike - Low_Strike` (or `High_Strike - Middle_Strike`)
5. Maximum profit occurs at middle strike: `(Spread_Width - Net_Premium) × Multiplier`

**Code Example:**

**Scenario:** Butterfly spread using calls with strikes $50, $55, $60. Premiums are $7.50, $4.20, $2.10. Multiplier is $100, using 10 contracts.

**Correct Code:**
```python
# Butterfly spread strikes and premiums
low_strike = 50
mid_strike = 55
high_strike = 60

premium_low = 7.50
premium_mid = 4.20
premium_high = 2.10

multiplier = 100
num_contracts = 10

# Net premium paid (buy low, sell 2 mid, buy high)
net_premium = premium_low + premium_high - 2 * premium_mid

# Spread width (distance between strikes)
spread_width = mid_strike - low_strike

# Maximum profit per contract
max_profit_per_contract = (spread_width - net_premium) * multiplier

# Total maximum profit
total_max_profit = max_profit_per_contract * num_contracts

total_max_profit  # $31,000
```

**Common Bugs to Avoid:**
- Forgetting to subtract net premium from spread width
- Incorrect premium calculation (not accounting for selling 2 middle strikes)
- Missing the multiplier (typically $100 per point for index options)
- Not multiplying by number of contracts for total profit

## Pattern: Implied Volatility from State-Dependent Future Scenarios

**Description:** When option pricing involves a discrete event that will resolve into multiple future states (each with different stock prices and volatilities), the implied volatility today must be reverse-engineered by: (1) calculating the option's expected value as the probability-weighted average of Black-Scholes values across all future states, and (2) solving iteratively for the single volatility that makes the current Black-Scholes price equal this expected value.

**When to Use:** Questions involving implied volatility calculation when future scenarios are explicitly state-dependent (e.g., lawsuit outcomes, merger announcements, regulatory decisions) with different volatilities and stock prices in each state.

**Procedure:**
1. For each future state i: compute the Black-Scholes option value using state-specific stock price S_i and volatility σ_i
2. Calculate expected option value: E[V] = Σ(p_i × V_i) where p_i is probability of state i
3. Use root-finding (e.g., scipy.optimize) to solve for implied volatility σ_implied such that BS(S_current, σ_implied) = E[V]
4. Return the solved implied volatility as a single scalar value

**Code Example:**

**Scenario:** A stock trades at $100. In 3 months, a binary event occurs: 60% chance stock goes to $110 with future vol 15%, 40% chance stock goes to $90 with future vol 30%. Risk-free rate 5%, no dividends. Find implied vol for a $105 strike call with 6 months to expiration.

**Correct Code:**
```python
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq

def black_scholes_call(S, K, T, r, sigma, q=0):
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return S*np.exp(-q*T)*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)

# Event occurs at t=0.25, option expires at t=0.5
S0 = 100
K = 105
T_total = 0.5
T_event = 0.25
T_remaining = T_total - T_event
r = 0.05

# State 1: favorable (60% prob)
p1 = 0.6
S1 = 110
vol1 = 0.15

# State 2: unfavorable (40% prob)
p2 = 0.4
S2 = 90
vol2 = 0.30

# Calculate option value in each state (after event, before expiration)
V1 = black_scholes_call(S1, K, T_remaining, r, vol1)
V2 = black_scholes_call(S2, K, T_remaining, r, vol2)

# Expected option value today
expected_value = p1 * V1 + p2 * V2

# Solve for implied volatility
def objective(sigma):
    return black_scholes_call(S0, K, T_total, r, sigma) - expected_value

implied_vol = brentq(objective, 0.01, 2.0)
implied_vol  # Result: approximately 0.235 or 23.5%
```

**Common Bugs to Avoid:**
- Returning state-specific volatilities [vol1, vol2] instead of solving for a single implied volatility
- Simple averaging of state volatilities (arithmetic or weighted) without proper option valuation
- Using the full time to expiration for state-specific calculations instead of remaining time after event
- Forgetting to discount or probability-weight the state-specific option values

---

## Pattern: Option Position Net Gain with Contract Multiplier

**Description:** The net gain/loss from an option position at expiration equals (intrinsic_value - premium_paid) × shares_per_contract × number_of_contracts. The intrinsic value depends on moneyness at expiration, the premium is the initial cost per share, and the standard contract multiplier is 100 shares unless stated otherwise.

**When to Use:** Questions asking for "net gain," "profit/loss," or "how much did you make/lose" on option positions at expiration, especially when option quotes show per-share prices but actual positions involve contracts.

**Procedure:**
1. Identify the option purchased (call/put, strike, expiration, premium from table)
2. Calculate intrinsic value at expiration: max(S_T - K, 0) for calls, max(K - S_T, 0) for puts
3. Calculate per-share profit: intrinsic_value - premium_paid
4. Multiply by contract size (typically 100) and number of contracts
5. Return total net gain (positive) or loss (negative)

**Code Example:**

**Scenario:** You bought 2 call option contracts with strike $50 at a premium of $3.20 per share. At expiration, the stock is at $56. What is your net gain?

**Correct Code:**
```python
# Option details
strike = 50
premium_per_share = 3.20
stock_at_expiration = 56
num_contracts = 2
shares_per_contract = 100

# Intrinsic value at expiration (call option)
intrinsic_value = max(stock_at_expiration - strike, 0)

# Per-share profit
profit_per_share = intrinsic_value - premium_per_share

# Total net gain
total_net_gain = profit_per_share * shares_per_contract * num_contracts
total_net_gain  # Result: 560.0
```

**Common Bugs to Avoid:**
- Forgetting the contract multiplier (100 shares per contract) and returning per-share profit
- Calculating only intrinsic value without subtracting the premium paid
- Using negative values incorrectly (net gain should be negative for losses, not absolute value)
- Confusing the premium in the table (per share) with total premium paid (per share × 100 × contracts)

---

## Pattern: Cross-Currency Basis Swap Synthetic Borrowing Cost

**Description:** When creating synthetic foreign currency borrowing through domestic borrowing plus a cross-currency basis swap, the all-in cost equals: domestic_reference_rate + domestic_spread + basis_swap_spread. A negative basis swap spread reduces the total cost. Compare this synthetic cost to direct foreign borrowing to determine savings.

**When to Use:** Questions about effective borrowing costs when using cross-currency basis swaps, comparing synthetic vs. direct foreign currency loans, or evaluating basis swap arbitrage opportunities.

**Procedure:**
1. Formula: Synthetic_FX_cost = Domestic_rate + Domestic_spread + Basis_spread
2. Direct_FX_cost = Foreign_rate + Foreign_spread
3. Savings = Direct_FX_cost - Synthetic_FX_cost
4. Return savings in basis points (multiply by 10000 if needed)

**Code Example:**

**Scenario:** A firm can borrow EUR at EURIBOR + 80 bps or USD at LIBOR + 120 bps. The EUR-USD basis swap is quoted at -15 bps. What is the cost difference if the firm borrows EUR and swaps to USD vs. borrowing USD directly?

**Correct Code:**
```python
# Direct USD borrowing cost (in bps over reference rate)
usd_spread_direct = 120

# Synthetic USD borrowing via EUR loan + basis swap
eur_spread = 80
basis_swap_spread = -15
usd_spread_synthetic = eur_spread + basis_swap_spread

# Cost comparison (positive means synthetic is cheaper)
savings_bps = usd_spread_direct - usd_spread_synthetic
savings_bps  # Result: 55 bps (synthetic is 55 bps cheaper)
```

**Common Bugs to Avoid:**
- Treating negative basis spread as increasing cost instead of decreasing it
- Subtracting basis spread instead of adding it algebraically (which naturally handles the sign)
- Comparing only spreads without considering the reference rate alignment through the swap
- Reversing the comparison direction (synthetic minus direct instead of direct minus synthetic)

---

## Pattern: Binary CDS vs Vanilla CDS Payoff Structure

**Description:** A binary CDS pays a fixed notional amount (typically 1 or 100%) upon default regardless of recovery rate, while a vanilla CDS pays (1 - recovery_rate) × notional. When calculating the CDS spread, the expected payoff for binary CDS is: Σ(default_probability_i × 1.0 × discount_factor_i), not adjusted for recovery.

**When to Use:** Questions explicitly asking about "binary credit default swap" or "binary CDS" pricing, or comparing binary vs. vanilla CDS structures.

**Procedure:**
1. For binary CDS: Expected_payoff = Σ(PD_i × 1.0 × DF_i) where PD_i is default probability at time i
2. For vanilla CDS: Expected_payoff = Σ(PD_i × (1 - R) × DF_i) where R is recovery rate
3. Calculate PV of premium payments (same for both types)
4. Solve for spread: s = Expected_payoff / PV_of_premium_leg
5. Return spread as decimal or basis points

**Code Example:**

**Scenario:** A 2-year binary CDS has default probabilities of 2% at year 1 and 1.5% at year 2. Risk-free rate is 5% (continuous). Recovery rate is 40% (irrelevant for binary). Payments are annual. Calculate the binary CDS spread.

**Correct Code:**
```python
import numpy as np

# Default probabilities
default_probs = [0.02, 0.015]
times = [1, 2]
risk_free_rate = 0.05
recovery_rate = 0.40  # Not used for binary CDS

# Discount factors
discount_factors = [np.exp(-risk_free_rate * t) for t in times]

# Expected payoff for BINARY CDS (payoff = 1.0 regardless of recovery)
expected_payoff_binary = sum(pd * 1.0 * df for pd, df in zip(default_probs, discount_factors))

# Survival probabilities
survival_probs = [1 - sum(default_probs[:i+1]) for i in range(len(times))]

# PV of premium payments (spread s per year)
pv_premiums = sum(surv * df for surv, df in zip(survival_probs, discount_factors))

# Binary CDS spread
binary_spread = expected_payoff_binary / pv_premiums
binary_spread  # Result: approximately 0.0178 or 178 bps
```

**Common Bugs to Avoid:**
- Using (1 - recovery_rate) as the payoff multiplier for binary CDS (this is vanilla CDS)
- Confusing the notional payoff (1.0 for binary) with the loss given default (1 - R for vanilla)
- Applying recovery rate adjustments to binary CDS calculations
- Not recognizing the keyword "binary" as a trigger for different payoff mechanics

---

## Pattern: Interest Rate Swap Duration from Pay-Fixed Perspective

**Description:** The modified duration of an interest rate swap from the pay-fixed perspective equals the duration of the fixed-rate bond leg minus the duration of the floating-rate bond leg. The floating leg duration approximates half the payment period (e.g., 0.25 years for semi-annual). For pay-fixed, the result is negative; for receive-fixed, positive.

**When to Use:** Questions asking for "duration of the swap," "modified duration of swap position," or using swaps to adjust portfolio duration, especially when payment frequency and fixed-rate bond duration are provided.

**Procedure:**
1. Formula: Duration_swap = Duration_fixed_leg - Duration_floating_leg
2. Duration_floating_leg ≈ (payment_period_in_years) / 2
3. For semi-annual payments: Duration_floating ≈ 0.25 years
4. Apply sign: negative for pay-fixed, positive for receive-fixed
5. Return signed duration value

**Code Example:**

**Scenario:** A 3-year interest rate swap with semi-annual payments has a fixed rate of 6%. The duration of a 3-year, 6% coupon bond is 2.75 years. What is the modified duration of the swap from the pay-fixed perspective?

**Correct Code:**
```python
# Given data
duration_fixed_bond = 2.75  # years
payment_frequency = 2  # semi-annual
payment_period = 1.0 / payment_frequency  # 0.5 years

# Floating leg duration (approximation)
duration_floating = payment_period / 2  # 0.25 years

# Swap duration (pay-fixed perspective)
duration_swap_pay_fixed = -(duration_fixed_bond - duration_floating)
duration_swap_pay_fixed  # Result: -2.50 years
```

**Common Bugs to Avoid:**
- Using only the fixed-leg duration without subtracting the floating-leg duration
- Forgetting the negative sign for pay-fixed positions
- Using the full payment period instead of half the payment period for floating duration
- Confusing swap duration with bond duration (they are related but distinct concepts)

---

## Pattern: Correlation-Consistent Joint Variable Movements

**Description:** When two financial variables have a known correlation coefficient, their simultaneous movements must be directionally and magnitude-consistent with that correlation. For positive correlation ρ > 0, variables tend to move in the same direction; for negative correlation, opposite directions. The plausibility of joint movements can be verified by checking if the implied correlation from observed changes is reasonably close to the stated correlation given the volatilities.

**When to Use:** Questions asking to verify or validate whether hypothetical simultaneous changes in two correlated variables (e.g., stock index and exchange rate, two stock prices) are "correct," "plausible," or "consistent" with given correlation and volatility parameters.

**Procedure:**
1. Calculate percentage changes: Δ₁ = (V₁_new - V₁_old) / V₁_old, Δ₂ = (V₂_new - V₂_old) / V₂_old
2. Check directional consistency: sign(Δ₁ × Δ₂) should match sign(ρ)
3. For quantitative check: implied_correlation ≈ (Δ₁ × Δ₂) / (σ₁ × σ₂ × √dt) should be near stated ρ
4. Return True if consistent, False otherwise (with tolerance for sampling variation)

**Code Example:**

**Scenario:** Two stocks have correlation 0.4, with volatilities 25% and 18% respectively. Over one day, stock A rises 1.2% and stock B rises 0.6%. Is this movement consistent with the correlation?

**Correct Code:**
```python
import numpy as np

# Given parameters
correlation = 0.4
vol_A = 0.25  # annual
vol_B = 0.18  # annual
change_A = 0.012  # 1.2%
change_B = 0.006  # 0.6%
dt = 1/252  # one trading day

# Directional consistency check
same_direction = (change_A * change_B) > 0
correlation_positive = correlation > 0
directionally_consistent = (same_direction == correlation_positive)

# Magnitude check (rough approximation)
# Expected covariance of returns over dt: ρ × σ_A × σ_B × dt
expected_product = correlation * vol_A * vol_B * dt
observed_product = change_A * change_B

# Allow wide tolerance due to single observation
magnitude_reasonable = (observed_product >= 0) and (observed_product < 10 * expected_product)

is_consistent = directionally_consistent and magnitude_reasonable
is_consistent  # Result: True
```

**Common Bugs to Avoid:**
- Rejecting plausible movements because they don't exactly match the correlation (correlation describes tendency, not deterministic relationship)
- Ignoring the sign of correlation when checking directional consistency
- Applying overly strict quantitative tests to single observations (correlation is a population parameter)
- Forgetting to scale volatilities by √dt when comparing to short-term changes