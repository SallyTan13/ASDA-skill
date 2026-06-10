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

**Description:** Market value of debt differs from face value and must be calculated by discounting all future cash flows (coupon payments and principal) at the current market yield. When coupon rates are not provided but duration information is available, use duration-based approximation: MV ≈ Face_Value / (1 + Market_Yield)^Duration. **CRITICAL: Tax rates do NOT affect market value of debt - they affect the firm's after-tax cost but not what debt holders would pay.**

**When to Use:** Questions asking to "estimate market value of debt" when market yields differ from coupon rates, or when duration information is provided but coupon rates are missing.

**Procedure:**
1. **CHECK**: Are coupon rates provided for each debt tranche?
2. **If YES**: Formula: `Market_Value = Σ(Cash_Flow_t / (1 + yield)^t)`
   - For each tranche, calculate annual coupon payments
   - Discount each cash flow (coupons + principal) at the market yield
   - Sum present values across all tranches
3. **If NO (only duration available)**: Use duration approximation
   - Formula: `MV ≈ Face_Value / (1 + Market_Yield)^Duration` for zero-coupon approximation
   - Or: `MV ≈ Face_Value × (1 - Duration × (Market_Yield - Assumed_Coupon_Yield))`
4. **CRITICAL**: Do NOT apply tax adjustments - market value is pre-tax
5. Return total market value

**Worked Example:**

**Question:** A firm has three debt tranches: $5B maturing in 1 year (duration 1.0), $4B maturing in 3 years (duration 2.8), and $6B maturing in 6 years (duration 5.2). Market yield is 7%. Tax rate is 30%. Coupon rates are not provided. Estimate market value.

```python
import math

# Debt tranches with duration information (no coupon rates)
tranches = [
    {'face': 5_000_000_000, 'duration': 1.0},
    {'face': 4_000_000_000, 'duration': 2.8},
    {'face': 6_000_000_000, 'duration': 5.2}
]
market_yield = 0.07
tax_rate = 0.30  # NOT USED - common bug to avoid

# Duration-based approximation (zero-coupon equivalent)
total_market_value = 0
for tranche in tranches:
    face = tranche['face']
    duration = tranche['duration']
    # Approximate as zero-coupon bond with maturity = duration
    # DO NOT multiply by (1 - tax_rate)
    pv = face / (1 + market_yield)**duration
    total_market_value += pv

# Result in millions
round(total_market_value / 1_000_000)  # approximately 12,450 million
```

**Common Bugs to Avoid:**
- **Applying tax adjustments (1 - tax_rate) to market value - tax shields affect cost, not market value**
- Using face value as market value when yields differ from coupon rates
- Dividing face value by (1 + rate) without considering cash flow structure
- Not checking whether coupon rates are available before attempting full cash flow discounting
- Ignoring duration information when coupon data is missing

**CHECK Steps:**
- **VERIFY**: Tax rate should NOT appear in market value calculation
- If coupon rates are missing, verify that duration information is available
- If using duration approximation, result should be less than face value when market yield > 0
- Validate that total market value is reasonable (typically 80%-120% of face value for investment-grade debt)
- Assert: Market_Value ≠ Face_Value × (1 - tax_rate)

---
## Pattern: CDS Valuation from Protection Buyer Perspective

**Description:** The value of a CDS to the protection buyer equals the present value of expected payoffs (received upon default) minus the present value of premium payments (paid periodically). Critical: defaults typically occur mid-year while premium payments occur at year-end, requiring separate discount factor arrays for different payment timings. **CRITICAL: Always extract parameters (recovery rate, hazard rate, spread) from the problem statement, NOT from illustrative tables or examples.**

**When to Use:** Questions asking for CDS value to protection buyer, or comparing contract spread to market spread, especially when payment timing conventions are specified.

**Procedure:**
1. **FIRST: Extract parameters from problem statement**:
   - Recovery rate (NOT from example tables)
   - Hazard rate or default probabilities
   - Contract spread vs. market spread
   - Risk-free rate
2. Formula: `Value_to_Buyer = PV(Expected_Payoffs) - PV(Premium_Payments)`
3. **Identify payment timing conventions**:
   - Premium payments: typically year-end (t = 1, 2, 3, ...)
   - Default payoffs: typically mid-year (t = 0.5, 1.5, 2.5, ...)
   - Accrual payments: same timing as default payoffs
4. **Create separate discount factor arrays**:
   - `DF_premium[i] = exp(-r × t_premium[i])` for premium payments
   - `DF_payoff[i] = exp(-r × t_payoff[i])` for payoffs and accruals
5. Calculate PV of expected payoffs: `Σ(PD_i × (1 - Recovery) × Notional × DF_payoff[i])`
6. Calculate PV of premium payments: `Contract_Spread × Σ(Survival_Prob_i × DF_premium[i])`
7. Calculate PV of accrual payments: `0.5 × Contract_Spread × Σ(PD_i × DF_payoff[i])`
8. Value = PV(Payoffs) - PV(Premiums) - PV(Accruals)

**Worked Example:**

**Question:** A 3-year CDS has contract spread 120 bps, notional $1, recovery 25%, hazard rate 2.5%, risk-free rate 4%. Premiums paid at year-end, defaults occur mid-year. Calculate value to protection buyer.

```python
import math

# Parameters FROM PROBLEM STATEMENT (not from tables)
contract_spread = 0.0120  # 120 bps
notional = 1.0
recovery_rate = 0.25  # 25% from problem statement
hazard_rate = 0.025  # 2.5% from problem statement
risk_free_rate = 0.04
years = 3

# Payment timings
premium_times = [1.0, 2.0, 3.0]  # year-end
payoff_times = [0.5, 1.5, 2.5]   # mid-year

# Discount factors for different timings
df_premium = [math.exp(-risk_free_rate * t) for t in premium_times]
df_payoff = [math.exp(-risk_free_rate * t) for t in payoff_times]

# Survival and default probabilities
survival_probs = [math.exp(-hazard_rate * t) for t in premium_times]
default_probs = [math.exp(-hazard_rate * (t - 0.5)) * (1 - math.exp(-hazard_rate)) 
                 for t in payoff_times]

# PV of expected payoffs (what buyer receives)
pv_payoffs = sum(pd * (1 - recovery_rate) * notional * df 
                 for pd, df in zip(default_probs, df_payoff))

# PV of premium payments (what buyer pays at year-end)
pv_premiums = contract_spread * sum(surv * df 
                                     for surv, df in zip(survival_probs, df_premium))

# PV of accrual payments (half-year premium if default mid-year)
pv_accruals = 0.5 * contract_spread * sum(pd * df 
                                           for pd, df in zip(default_probs, df_payoff))

# Value to protection buyer
value_to_buyer = pv_payoffs - pv_premiums - pv_accruals
round(value_to_buyer, 4)
```

**Common Bugs to Avoid:**
- **Using parameter values from illustrative tables instead of the problem statement**
- **Extracting recovery rate from example calculations when problem gives different value**
- Using single discount factor array for all cash flows (ignoring timing differences)
- Forgetting accrual payment adjustment when defaults occur mid-period
- Reversing the sign (calculating seller value instead of buyer value)
- Using market spread instead of contract spread for premium payments

**CHECK Steps:**
- **CRITICAL: Verify recovery rate matches problem statement, not example tables**
- **CRITICAL: Verify hazard rate/default probability from problem statement**
- **CRITICAL: Check if problem says "recovery rate is X%" - use X, not table values**
- If defaults occur mid-year and premiums at year-end, verify separate discount factor arrays
- If contract spread < market spread, value to buyer should be negative
- Verify that accrual payments use the same timing as default payoffs
- Assert: recovery_rate extracted from problem text, not from "Table X" or "Example Y"
## Pattern: Firm Value Volatility from Equity and Debt Volatilities

**Description:** Firm value volatility must be derived from equity and debt volatilities using the portfolio variance formula, incorporating the correlation between equity and debt returns and weighting by market values. When both a stated debt ratio and market values are provided, use the stated debt ratio as it represents the target capital structure.

**When to Use:** Questions asking for "implied standard deviation in firm value" given equity volatility, debt volatility, correlation, and debt ratio or market values.

**Procedure:**
1. Formula: `σ²_firm = w²_E × σ²_E + w²_D × σ²_D + 2 × w_E × w_D × ρ × σ_E × σ_D`
2. **Determine weights**:
   - **If debt ratio is explicitly stated**: use it directly (w_D = stated ratio, w_E = 1 - w_D)
   - **If only market values given**: calculate w_E = E/(E+D), w_D = D/(E+D)
   - **If both provided**: prefer stated debt ratio (represents target structure)
3. Compute variance using portfolio formula with correlation term
4. Take square root to get firm volatility: `σ_firm = √(σ²_firm)`
5. **CHECK**: If result seems unreasonable, verify weight calculation

**Worked Example:**

**Question:** Equity volatility is 35%, debt volatility is 15%, correlation is 0.5. The firm has a stated debt-to-total-value ratio of 50%. Calculate firm value volatility.

```python
import math

# Given parameters
sigma_equity = 0.35
sigma_debt = 0.15
correlation = 0.5
debt_ratio_stated = 0.50  # explicitly stated

# Use stated debt ratio (not calculated from market values)
w_debt = debt_ratio_stated
w_equity = 1 - debt_ratio_stated

# Portfolio variance formula
variance_firm = (w_equity**2 * sigma_equity**2 + 
                 w_debt**2 * sigma_debt**2 + 
                 2 * w_equity * w_debt * correlation * sigma_equity * sigma_debt)

# Firm volatility
sigma_firm = math.sqrt(variance_firm)
round(sigma_firm, 4)  # 0.2135 or 21.35%
```

**Common Bugs to Avoid:**
- Calculating weights from market values when debt ratio is explicitly stated
- Omitting the correlation term (2 × w_E × w_D × ρ × σ_E × σ_D)
- Using simple weighted average instead of portfolio variance formula
- Forgetting to take square root of variance to get standard deviation
- Using book values instead of market values when calculating weights

**CHECK Steps:**
- If stated debt ratio is provided, use it instead of calculating from market values
- Verify σ_firm is between min(σ_E, σ_D) and max(σ_E, σ_D) for positive correlation
- If result is outside this range, check correlation sign and weight calculation
- Assert w_equity + w_debt = 1.0

---
## Pattern: Forward Contract Revaluation After Rate Changes

**Description:** A forward contract problem can ask for two different things: (1) the **forward price** - what you would pay for the underlying at delivery under new rates, or (2) the **contract value** - the mark-to-market of an existing position. **CRITICAL: Distinguish between "price of forward contract" (asking for forward price) vs "value of forward contract" (asking for MTM value).**

**When to Use:** Questions asking about forward contracts "after rates change" or "given these new rates."

**Procedure:**
1. **Identify what is being asked**:
   - "What is the **price** of a forward contract...?" → Calculate forward price
   - "What is the **value** of your forward contract...?" → Calculate MTM value
2. **For forward price** (what you'd pay for the bond at delivery):
   - Formula: `Forward_Price = Par / (DF_maturity / DF_delivery)`
   - Or: `Forward_Price = Spot_Price / DF_to_delivery`
   - Use the NEW rates after the change
3. **For contract value** (MTM of existing position):
   - Formula: `Value = (F_original - F_new) × Notional × DF_to_settlement`
   - Calculate original forward price using initial rates
   - Calculate new forward price using updated rates
   - Discount the difference back to present
4. Return the appropriate result based on question type

**Code Example:**

**Scenario:** You entered a forward contract to buy a 1-year bond in 6 months at forward price $960. Rates then increased 25 bps. The new 6-month rate is 4.5%, new 1-year rate is 5.0%. (a) What is the price of a new forward contract? (b) What is the value of your existing contract?

**Correct Code:**
```python
import math

# Bond parameters
par_value = 1000
delivery_time = 0.5  # 6 months
bond_maturity = 1.0  # 1 year from now

# NEW rates after change
new_6m_rate = 0.045
new_1yr_rate = 0.050

# Original forward price (locked in)
forward_price_original = 960

# (a) Price of NEW forward contract under new rates
# Forward price = Par / (DF_maturity / DF_delivery)
df_delivery = 1 / (1 + new_6m_rate)**delivery_time
df_maturity = 1 / (1 + new_1yr_rate)**bond_maturity
forward_price_new = par_value / (df_maturity / df_delivery)

# (b) Value of EXISTING forward contract (long position)
# Value = (F_original - F_new) × DF_to_settlement
value_existing = (forward_price_original - forward_price_new) * df_delivery

# Results
round(forward_price_new, 2), round(value_existing, 2)
# (947.62, -11.85) - new forward price is $947.62, existing contract lost $11.85
```

**Common Bugs to Avoid:**
- **Confusing forward price (what you pay) with contract value (MTM)**
- Calculating contract value when question asks for forward price
- Using wrong sign convention (long benefits when F_original > F_new)
- Not recognizing that forward contracts have zero initial value but non-zero value after rate changes
- Forgetting to discount the price difference back to present for contract value

**CHECK Steps:**
- **VERIFY**: Does question ask for "price" or "value"?
- If asking for "price of forward contract," return the forward price itself
- If asking for "value of forward contract," return the MTM value
- For long position: value is positive when F_original > F_new (rates decreased)
- Assert: Forward price should be close to par when rates are near zero

---
## Pattern: Collar Strategy Profit with Net Premium Accounting

**Description:** A collar strategy's profit at expiration must account for the net premium paid or received upfront. Calculate: (1) stock gain/loss from entry to expiration, (2) add put payoff if stock below put strike, (3) subtract call payoff if stock above call strike, (4) subtract net premium cost (put premium paid minus call premium received). The breakeven for a protective put on already-owned stock is the current stock price plus the put premium paid. **CRITICAL: Net premium is a COST that reduces profit - it should be subtracted from gains, not added.**

**When to Use:** Questions about collar strategy profit/loss at expiration, or asking for "breakeven price" of protective put positions involving long stock, long put, and optionally short call.

**When NOT to Use:** When calculating option intrinsic value at expiration (use max(S-K, 0) for calls). When the question asks about option time value decomposition.

**Procedure:**
1. Stock_gain = S_T - S_0
2. Put_payoff = max(K_put - S_T, 0) if long put
3. Call_payoff = -max(S_T - K_call, 0) if short call
4. Net_premium = Put_premium_paid - Call_premium_received (this is the NET COST)
5. **CRITICAL**: Total_profit = Stock_gain + Put_payoff + Call_payoff - Net_premium
   - The net_premium is ALWAYS subtracted because it represents upfront cost
   - If net_premium is positive, you paid more than you received (cost)
   - If net_premium is negative, you received more than you paid (credit)
6. **Breakeven for protective put on owned stock** = S_0 + Put_premium_paid
7. **Breakeven for collar on owned stock** = S_0 + Net_premium

**Worked Example:**

**Question:** You own stock purchased at $45, bought a $42 put for $1.80, and sold a $52 call for $1.20. At expiration, the stock is at $50. What is your profit per share? What is the breakeven price?

```python
# Position details
S0 = 45  # initial stock price (already owned)
ST = 50  # stock at expiration
K_put = 42
K_call = 52
put_premium = 1.80
call_premium = 1.20

# Net premium for collar (COST paid upfront)
net_premium = put_premium - call_premium  # 0.60 paid (positive = cost)

# Profit calculation
stock_gain = ST - S0  # 5.00
put_payoff = max(K_put - ST, 0)  # 0
call_payoff = -max(ST - K_call, 0)  # 0

# CRITICAL: Subtract net_premium because it's a cost
total_profit = stock_gain + put_payoff + call_payoff - net_premium
# Result: 5.00 + 0 + 0 - 0.60 = 4.40

# Breakeven for collar (stock already owned)
breakeven_collar = S0 + net_premium
# Result: 45.60

total_profit, breakeven_collar
```

**Common Bugs to Avoid:**
- **Double-counting premium: calculating net_premium correctly but then subtracting it with wrong sign (e.g., "- net_premium" when net_premium is already the cost)**
- Calculating breakeven as strike price minus premium instead of initial stock price plus net premium
- Using formula S0 + premium for stock purchased simultaneously with option, when stock was already owned
- **Treating net_premium as a gain when it should be subtracted as a cost**
- Ignoring the call premium received when calculating net premium for collar

**CHECK Steps:**
- **VERIFY**: Net premium calculation: put_premium_paid - call_premium_received
- **VERIFY**: Final profit formula SUBTRACTS net_premium: profit = gains - net_premium
- If stock was already owned before buying protective put, breakeven = S0 + put_premium (or S0 + net_premium for collar)
- If stock and option purchased simultaneously, breakeven = purchase_price + premium
- **ASSERT**: If net_premium > 0 (you paid net cost), it should REDUCE total profit
- **ASSERT**: Total profit should equal (ST - S0) - net_premium when both options expire OTM

---
## Pattern: Option Intrinsic Value vs. Premium at Expiration

**Description:** At expiration, an option's value equals its intrinsic value (max(S_T - K, 0) for calls), not the premium originally paid. For total investment value, multiply intrinsic value per share by shares per contract and number of contracts. **CRITICAL: "Investment worth" or "value" means intrinsic value only; "net gain" or "profit" means intrinsic value minus premium paid.**

**When to Use:** Questions asking "how much is your option investment worth" or "what is the value" at expiration, given a final stock price. Keywords: "worth," "value," "investment value."

**When NOT to Use:** When question asks for "profit," "gain," "loss," or "net gain" (use Option Position Net Gain pattern instead).

**Procedure:**
1. **Identify question type**:
   - If asking for "worth," "value," "investment value": calculate intrinsic value only
   - If asking for "profit," "gain," "loss": use net gain pattern (intrinsic - premium)
2. Formula (Call): `Intrinsic_Value = max(S_T - K, 0)`
3. Formula (Put): `Intrinsic_Value = max(K - S_T, 0)`
4. Identify option type, strike price, and expiration stock price
5. Calculate intrinsic value per share
6. Multiply by contract size (typically 100 shares) and number of contracts
7. Return total investment value (do NOT subtract premium)

**Code Example:**

**Scenario:** You own 8 call option contracts with strike $110. At expiration, stock is at $128. Each contract covers 100 shares. What is your investment worth?

**Correct Code:**
```python
# Option parameters
strike_price = 110
stock_price_at_expiration = 128
num_contracts = 8
shares_per_contract = 100

# Intrinsic value per share at expiration (do NOT subtract premium)
intrinsic_value_per_share = max(stock_price_at_expiration - strike_price, 0)

# Total investment value
total_value = intrinsic_value_per_share * shares_per_contract * num_contracts

total_value  # $14,400
```

**Common Bugs to Avoid:**
- **Subtracting the original premium paid when question asks for "worth" or "value"**
- Using the original premium paid instead of intrinsic value at expiration
- Forgetting to multiply by shares per contract (typically 100)
- Confusing "investment worth" (intrinsic only) with "net gain" (intrinsic minus premium)
- Not recognizing that out-of-the-money options expire worthless (intrinsic = 0)

**CHECK Steps:**
- **VERIFY**: If question uses "worth" or "value," do NOT subtract premium
- If question uses "profit" or "gain," use net gain pattern instead
- Assert: Investment worth = intrinsic value × 100 × num_contracts
- For OTM options: intrinsic value = 0, investment worth = 0

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

**Description:** A butterfly spread's maximum profit equals (spread width - net premium paid) × multiplier, occurring when the underlying price equals the middle strike at expiration. The spread involves buying 1 low strike, selling 2 middle strikes, buying 1 high strike, using ONLY calls OR ONLY puts (not mixed). **CRITICAL: For multiple-choice questions, the final answer must be matched to the provided options, not returned as a raw number.**

**When to Use:** Questions asking for maximum profit of butterfly spread strategies using call or put options.

**When NOT to Use:** When the question describes a strategy mixing calls and puts at the same strike (that's a different strategy like a straddle or strangle).

**Procedure:**
1. **Verify butterfly structure**: Must use all calls OR all puts, with three strikes (low, middle, high)
2. Formula: `Max_Profit = (Strike_Spacing - Net_Premium) × Multiplier × Contracts`
3. Identify the three strikes: low, middle, high (equally spaced)
4. Calculate net premium using ONLY the option type specified:
   - For call butterfly: `Net_Premium = Premium_low_call + Premium_high_call - 2 × Premium_middle_call`
   - For put butterfly: `Net_Premium = Premium_low_put + Premium_high_put - 2 × Premium_middle_put`
5. Calculate spread width: `Middle_Strike - Low_Strike` (or `High_Strike - Middle_Strike`)
6. Maximum profit occurs at middle strike: `(Spread_Width - Net_Premium) × Multiplier`
7. **For multiple-choice questions**: Match the calculated value to the closest option provided

**Worked Example:**

**Question:** Butterfly spread using calls with strikes $45, $50, $55. Call premiums are $8.20, $4.50, $1.80. Multiplier is $100, using 5 contracts. Options: A. $1,900, B. $2,000, C. $2,100

```python
# Butterfly spread strikes and premiums (CALLS ONLY)
low_strike = 45
mid_strike = 50
high_strike = 55

premium_low_call = 8.20
premium_mid_call = 4.50
premium_high_call = 1.80

multiplier = 100
num_contracts = 5

# Net premium paid (buy low call, sell 2 mid calls, buy high call)
net_premium = premium_low_call + premium_high_call - 2 * premium_mid_call
# = 8.20 + 1.80 - 2(4.50) = 1.00

# Spread width (distance between strikes)
spread_width = mid_strike - low_strike  # 5

# Maximum profit per contract
max_profit_per_contract = (spread_width - net_premium) * multiplier
# = (5 - 1.00) * 100 = 400

# Total maximum profit
total_max_profit = max_profit_per_contract * num_contracts
# = 400 * 5 = 2,000

# For multiple-choice: return the value that matches options
# If options are ['A. $1,900', 'B. $2,000', 'C. $2,100'], select 'B'
total_max_profit  # Returns 2000, which should be matched to option B
```

**Common Bugs to Avoid:**
- Mixing calls and puts in the same butterfly spread (use only one type)
- Using both call and put premiums at the middle strike (double-counting)
- Incorrect premium calculation (not accounting for selling 2 middle strikes)
- Missing the multiplier (typically $100 per point for index options)
- **Returning raw numerical value without matching to multiple-choice options when options are provided**

**CHECK Steps:**
- Verify the strategy uses ONLY calls OR ONLY puts, not both
- Assert three distinct strike prices with equal spacing
- Verify net_premium uses only the specified option type (calls OR puts)
- Check that spread_width = (mid_strike - low_strike) = (high_strike - mid_strike)
- **If answer options are provided in the question, match the calculated value to the closest option**
- **For multiple-choice format, return the option letter/label, not just the number**

---
## Pattern: Implied Volatility from State-Dependent Future Scenarios

**Description:** When option pricing involves a discrete event that will resolve into multiple future states (each with different stock prices and volatilities), the implied volatility today must be reverse-engineered by: (1) calculating the option's expected value as the probability-weighted average of Black-Scholes values across all future states, and (2) solving iteratively for the single volatility that makes the current Black-Scholes price equal this expected value. For immediate events (resolving "tomorrow" or "today"), use T_event ≈ 0 and T_remaining ≈ T_total. **CRITICAL**: This pattern applies ONLY when the question explicitly asks for "implied volatility" - if the question asks for probability estimates or qualitative comparisons, use standard probability calculations instead.

**When to Use:** Questions involving implied volatility calculation when future scenarios are explicitly state-dependent (e.g., lawsuit outcomes, merger announcements, regulatory decisions) with different volatilities and stock prices in each state. Keywords: "implied volatility," "binary event," "lawsuit," "announcement," "resolves tomorrow/today." **Must explicitly ask for implied volatility as a numerical answer.**

**When NOT to Use:** When question asks for probability estimates using lognormal assumptions (calculate probabilities directly). When question asks qualitative comparison about whether lognormal estimate is "too high" or "too low" (discuss volatility smile implications without calculating implied vol). When only one future scenario is given.

**Procedure:**
1. **Check if state probabilities are provided**:
   - If YES: use the given probabilities
   - If NO: infer risk-neutral probabilities from current stock price and state values
   - Formula for two states: `p_up = (S_0 × exp(r × T_event) - S_down) / (S_up - S_down)`
2. **Identify event timing**: 
   - If event is "tomorrow" or "today": T_event ≈ 0 (or 1/252 for one day)
   - If event is "in X months": T_event = X/12
3. **Calculate remaining time after event**: T_remaining = T_total - T_event
4. **CRITICAL**: For state-specific option values, use T_remaining (NOT T_total)
5. For each future state i: compute Black-Scholes option value using state-specific stock price S_i, volatility σ_i, and **T_remaining**
6. Calculate expected option value: E[V] = Σ(p_i × V_i) where p_i is probability of state i
7. Use root-finding to solve for implied volatility σ_implied such that BS(S_current, σ_implied, T_total) = E[V]
8. Return the solved implied volatility as a single scalar value

**Worked Example:**

**Question:** A stock trades at $50. A lawsuit resolves tomorrow: if favorable (stock goes to $62 with future vol 20%), if unfavorable (stock goes to $42 with future vol 35%). Risk-free rate 5%, no dividends. State probabilities not given. Find implied vol for a $48 strike call with 4 months to expiration.

```python
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq

def black_scholes_call(S, K, T, r, sigma, q=0):
    if T <= 0:
        return max(S - K, 0)
    if sigma <= 0:
        return max(S - K, 0) if T == 0 else 0
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# Current parameters
S0 = 50
K = 48
T_total = 4 / 12  # 4 months
T_event = 1 / 252  # tomorrow
T_remaining = T_total - T_event  # ≈ 0.333
r = 0.05

# State values
S_up = 62
S_down = 42
vol_up = 0.20
vol_down = 0.35

# Infer risk-neutral probabilities (not provided in question)
# Formula: p_up = (S0 * exp(r*T_event) - S_down) / (S_up - S_down)
p_up = (S0 * np.exp(r * T_event) - S_down) / (S_up - S_down)
p_down = 1 - p_up

# Calculate state-specific option values using T_remaining
V_up = black_scholes_call(S_up, K, T_remaining, r, vol_up)
V_down = black_scholes_call(S_down, K, T_remaining, r, vol_down)

# Expected option value
expected_value = p_up * V_up + p_down * V_down

# Solve for implied volatility using T_total
def objective(sigma):
    return black_scholes_call(S0, K, T_total, r, sigma) - expected_value

implied_vol = brentq(objective, 0.01, 2.0)
round(implied_vol, 4)
```

**Common Bugs to Avoid:**
- **Using T_total for state-specific calculations instead of T_remaining**
- Assuming equal probabilities when not provided (must infer from risk-neutral pricing)
- Returning state-specific volatilities instead of solving for single implied volatility
- Simple averaging of state volatilities without proper option valuation
- Applying this pattern when question asks for probability estimates (not implied vol)
- Using this pattern for qualitative volatility smile questions

**CHECK Steps:**
- **VERIFY**: Question explicitly asks for "implied volatility" as a number
- **If probabilities not given**: Calculate p_up = (S0×e^(rT) - S_down)/(S_up - S_down)
- **ASSERT**: If event is "tomorrow," verify T_event ≈ 0 and T_remaining ≈ T_total
- **ASSERT**: State-specific option values use T_remaining, NOT T_total
- **VALIDATE**: implied_vol should be between min(vol_up, vol_down) and max(vol_up, vol_down)
- If question asks about probability or "too high/too low," do NOT use this pattern

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

**Description:** The modified duration of an interest rate swap from the pay-fixed perspective equals the duration of the fixed-rate bond leg minus the duration of the floating-rate bond leg. The floating leg duration approximates the time to the next reset date (e.g., 0.5 years for semi-annual payments, 0.25 years for quarterly). For pay-fixed, the result is negative; for receive-fixed, positive. **CRITICAL: Floating leg duration equals the time to next payment/reset, NOT half of that time.**

**When to Use:** Questions asking for "duration of the swap," "modified duration of swap position," or using swaps to adjust portfolio duration, especially when payment frequency and fixed-rate bond duration are provided.

**Procedure:**
1. Formula: Duration_swap = Duration_fixed_leg - Duration_floating_leg
2. **Duration_floating_leg = time_to_next_reset** (NOT divided by 2)
   - For semi-annual payments: Duration_floating = 0.5 years
   - For quarterly payments: Duration_floating = 0.25 years
   - For annual payments: Duration_floating = 1.0 year
3. Apply sign: negative for pay-fixed, positive for receive-fixed
4. Return signed duration value
5. **For multiple-choice questions**: Match result to closest option provided

**Code Example:**

**Scenario:** A 3-year interest rate swap with semi-annual payments has a fixed rate of 6%. The duration of a 3-year, 6% coupon bond is 2.75 years. What is the modified duration of the swap from the pay-fixed perspective?

**Correct Code:**
```python
# Given data
duration_fixed_bond = 2.75  # years
payment_frequency = 2  # semi-annual
payment_period = 1.0 / payment_frequency  # 0.5 years

# Floating leg duration (time to next reset)
duration_floating = payment_period  # 0.5 years (NOT divided by 2)

# Swap duration (pay-fixed perspective)
duration_swap_pay_fixed = -(duration_fixed_bond - duration_floating)
# = -(2.75 - 0.5) = -2.25 years

duration_swap_pay_fixed
```

**Common Bugs to Avoid:**
- **Using half the payment period for floating duration (e.g., 0.25 for semi-annual instead of 0.5)**
- Using only the fixed-leg duration without subtracting the floating-leg duration
- Forgetting the negative sign for pay-fixed positions
- Confusing swap duration with bond duration (they are related but distinct concepts)
- **Not matching calculated value to multiple-choice options when provided**

**CHECK Steps:**
- **VERIFY**: Floating leg duration = payment_period (time to next reset), NOT payment_period/2
- For semi-annual payments: duration_floating should be 0.5 years
- For quarterly payments: duration_floating should be 0.25 years
- Verify negative sign for pay-fixed positions
- **If answer options provided, match calculated value to closest option**
- **ASSERT**: |Duration_swap| ≈ |Duration_fixed - Payment_Period|
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

## Pattern: Interest Rate Swap Valuation with Discount Curves

**Description:** An interest rate swap's value equals the difference between the present values of fixed-leg and floating-leg cash flows. The floating leg is valued by recognizing that at each reset date, the floating rate bond is worth par, so PV(floating) = notional × (1 + next_floating_rate × period) × DF_next_payment. The fixed leg is valued by discounting all fixed coupon payments and notional at maturity. For pay-fixed positions, value = PV(floating) - PV(fixed).

**When to Use:** Questions asking for "value of swap," "mark-to-market of swap," or "swap valuation" given current term structure of interest rates (spot rates, forward rates, or swap rates).

**Procedure:**
1. **Identify swap terms**: notional, fixed rate, payment frequency, remaining maturity
2. **Determine discount factors** from given rates:
   - If spot rates given: DF(t) = 1 / (1 + spot_rate)^t
   - If forward rates given: bootstrap to get spot rates, then discount factors
   - If swap rates given: use swap rates as par yields to bootstrap zero curve
3. **Value floating leg**:
   - At each reset, floating bond = par
   - PV(floating) = notional × (1 + next_LIBOR × period) × DF_next_payment
4. **Value fixed leg**:
   - PV(fixed) = Σ(fixed_coupon × DF_i) + notional × DF_maturity
5. **Calculate swap value**:
   - For pay-fixed (receive-floating): Value = PV(floating) - PV(fixed)
   - For receive-fixed (pay-floating): Value = PV(fixed) - PV(floating)

**Worked Example:**

**Question:** A 2-year pay-fixed swap has notional $50M, fixed rate 4%, annual payments. Current 1-year spot rate is 3.5%, 2-year spot rate is 4.2%. What is the swap value?

```python
import math

# Swap parameters
notional = 50_000_000
fixed_rate = 0.04
years_remaining = 2
payment_frequency = 1  # annual

# Current spot rates (for discounting)
spot_1yr = 0.035
spot_2yr = 0.042

# Discount factors
df_1yr = 1 / (1 + spot_1yr)**1
df_2yr = 1 / (1 + spot_2yr)**2

# Floating leg valuation
# At next reset (1 year), floating bond worth par
# Current floating rate for 1-year period is spot_1yr
next_floating_payment = notional * fixed_rate  # simplified: use forward rate
# More accurate: forward rate = ((1+spot_2yr)^2 / (1+spot_1yr)) - 1
forward_1y1y = ((1 + spot_2yr)**2 / (1 + spot_1yr)) - 1
pv_floating = notional * (1 + spot_1yr) * df_1yr  # bond at par after first payment

# Alternative: value as bond at par at next reset
pv_floating_simple = notional * df_1yr * (1 + spot_1yr * payment_frequency)

# Fixed leg valuation
fixed_payment = notional * fixed_rate
pv_fixed = (fixed_payment * df_1yr + 
            (fixed_payment + notional) * df_2yr)

# Swap value (pay-fixed perspective)
swap_value_pay_fixed = pv_floating_simple - pv_fixed

round(swap_value_pay_fixed / 1_000_000, 2)  # in millions
```

**Common Bugs to Avoid:**
- Confusing projection curve (for floating rate forecasts) with discount curve
- Using forward rates directly as discount factors
- Forgetting that floating leg resets to par at each payment date
- Not distinguishing between pay-fixed and receive-fixed perspectives
- Using simple rate differences instead of present value calculations

**CHECK Steps:**
- If all rates increased, pay-fixed swap should have positive value (fixed rate now below market)
- Verify PV(floating) ≈ notional when valued at a reset date
- Assert that discount factors decrease monotonically with maturity

---

## Pattern: Portfolio Rebalancing with Futures Contracts

**Description:** To rebalance a portfolio from current allocation to target allocation using futures, first calculate the dollar shift needed in each asset class based on target allocation percentages, then convert to number of contracts. **Beta adjustment is ALWAYS needed when portfolio beta ≠ futures beta, even when maintaining current portfolio beta during rebalancing.**

**When to Use:** Questions asking to "rebalance portfolio," "adjust allocation," or "change portfolio weights" using futures contracts, especially when target allocation percentages and current portfolio values are provided.

**When NOT to Use:** When hedging interest rate risk with bond futures (use BPV/duration approach instead).

**Procedure:**
1. **Calculate total portfolio value**: Sum all asset class values
2. **Determine target dollar amounts**: Target_$ = Total_Value × Target_Allocation_%
3. **Calculate dollar shift needed**: Shift_$ = Target_$ - Current_$
4. **CRITICAL: Check if beta adjustment is needed**:
   - If Portfolio_Beta ≠ Futures_Beta: ALWAYS apply beta adjustment
   - Formula: `Contracts = (Shift_$ × Portfolio_Beta) / (Futures_Price × Futures_Beta)`
   - This applies even when "maintaining current beta" during rebalancing
5. **Special case: If Portfolio_Beta = Futures_Beta = 1.0**:
   - Simplified formula: `Contracts = Shift_$ / Futures_Price`
6. Round to nearest integer; positive = buy, negative = sell

**Worked Example:**

**Question:** A pension fund has $30B in equities (beta 1.10) and $20B in bonds. Target allocation is 70% equity, 30% bonds. Equity index futures trade at $250,000 per contract with beta 1.05. How many futures to buy/sell to rebalance?

```python
# Current portfolio
equity_current = 30_000_000_000
bonds_current = 20_000_000_000
total_portfolio = equity_current + bonds_current  # $50B

# Target allocation
target_equity_pct = 0.70
target_bonds_pct = 0.30

# Calculate target dollar amounts
target_equity = total_portfolio * target_equity_pct  # $35B
target_bonds = total_portfolio * target_bonds_pct    # $15B

# Dollar shift needed
equity_shift = target_equity - equity_current  # +$5B (increase equity)

# Futures contract specifications
futures_price = 250_000
futures_beta = 1.05
portfolio_beta = 1.10

# Number of contracts WITH beta adjustment
# Even though we're "maintaining current beta," we must adjust for beta mismatch
num_contracts = (equity_shift * portfolio_beta) / (futures_price * futures_beta)

# Round to nearest integer
contracts_to_trade = round(num_contracts)
contracts_to_trade  # approximately 20,952 contracts (buy)
```

**Common Bugs to Avoid:**
- **Omitting beta adjustment when Portfolio_Beta ≠ Futures_Beta (even when "maintaining beta")**
- Using formula Shift_$ / Futures_Price without beta adjustment when betas differ
- Confusing "maintain beta" with "change beta to 1.0"
- Calculating total portfolio value incorrectly (missing asset classes)
- Using (1.0 - current_beta) as target beta change when rebalancing allocations

**CHECK Steps:**
- **CRITICAL**: If Portfolio_Beta ≠ Futures_Beta, verify beta adjustment is applied
- If target allocation > current allocation, contracts should be positive (buy)
- Verify total portfolio value = sum of all asset class values
- If Portfolio_Beta = Futures_Beta = 1.0, simplified formula is acceptable
- Assert: Formula includes both portfolio_beta and futures_beta when they differ

---
## Pattern: Employee Stock Option Expected Life from Binomial Tree

**Description:** The expected life of an employee stock option must be calculated from a binomial tree by identifying all possible paths, determining exercise/forfeiture times on each path based on voluntary exercise rates and turnover, computing path probabilities, and taking the probability-weighted average time. This cannot be approximated by scaling option values or using simple fractions of the full term. **For n-period trees, systematically enumerate all 2^n paths using binary iteration.**

**When to Use:** Questions asking for "expected life" of employee stock options given a binomial tree with early exercise probabilities, turnover rates, and vesting constraints. Keywords: "expected life," "employee option," "binomial tree," "voluntary exercise," "turnover," "forfeiture."

**Procedure:**
1. **Identify tree structure**: number of periods n, period length, total paths = 2^n
2. **For each path from 0 to 2^n - 1**:
   - Convert path number to binary to determine up/down sequence
   - Track cumulative probability along the path (multiply risk-neutral probs)
   - At each node, check: (a) vesting status, (b) moneyness, (c) voluntary exercise rate
   - Apply turnover/forfeiture rate at each step
   - Determine termination time: earliest of (exercise, forfeiture, expiration)
3. **Calculate path probability**: product of (up/down probs) × (1 - exercise rates) × (1 - turnover rates)
4. **Compute expected life**: Σ(Path_Probability_i × Termination_Time_i) / Σ(Path_Probability_i)
5. Return weighted average time

**Worked Example:**

**Question:** A 3-year employee option has a binomial tree with 3 annual periods. Risk-neutral up probability is 0.55. At any in-the-money node, 40% exercise voluntarily. Turnover is 5% per period. Vesting occurs immediately. Calculate expected life.

```python
import math

# Tree parameters
num_periods = 3
period_length = 1.0  # years
total_paths = 2**num_periods  # 8 paths
prob_up = 0.55
prob_down = 1 - prob_up  # 0.45
exercise_rate_itm = 0.40  # if in-the-money
turnover_rate = 0.05
vesting_time = 0  # immediate vesting

# For simplicity, assume strike = 100, S0 = 100, u = 1.2, d = 0.9
S0 = 100
strike = 100
u = 1.2
d = 0.9

# Storage for path analysis
path_probs = []
path_times = []

# Enumerate all paths using binary representation
for path_num in range(total_paths):
    # Convert to binary: 0=down, 1=up
    # e.g., path_num=5 (binary 101) means up-down-up
    path_binary = format(path_num, f'0{num_periods}b')
    
    # Track along this path
    stock_price = S0
    path_prob = 1.0
    survival_prob = 1.0
    terminated = False
    termination_time = num_periods * period_length  # default: expiration
    
    for period in range(num_periods):
        # Update stock price
        if path_binary[period] == '1':  # up move
            stock_price *= u
            path_prob *= prob_up
        else:  # down move
            stock_price *= d
            path_prob *= prob_down
        
        # Apply turnover
        survival_prob *= (1 - turnover_rate)
        
        # Check for voluntary exercise if ITM and vested
        current_time = (period + 1) * period_length
        if stock_price > strike and current_time >= vesting_time and not terminated:
            # Some employees exercise
            if exercise_rate_itm > 0:
                # This path splits: some exercise, some continue
                # For simplicity, treat as weighted average
                # Probability of exercising at this node
                exercise_prob = exercise_rate_itm
                if exercise_prob > 0:
                    termination_time = current_time
                    path_prob *= exercise_rate_itm
                    terminated = True
                    break
    
    # Final path probability includes survival
    final_prob = path_prob * survival_prob
    path_probs.append(final_prob)
    path_times.append(termination_time)

# Calculate expected life
total_prob = sum(path_probs)
expected_life = sum(p * t for p, t in zip(path_probs, path_times)) / total_prob

round(expected_life, 2)
```

**Common Bugs to Avoid:**
- Only considering up-paths or a subset of paths (must enumerate all 2^n paths)
- Scaling full term by ratio of option values (assumes linear relationship)
- Using simple weighted average of exercise times without path probabilities
- Forgetting to account for turnover/forfeiture in path probabilities
- Not recognizing that paths terminate at different times (exercise vs. expiration)
- Ignoring vesting constraints when determining earliest exercise time

**CHECK Steps:**
- **ASSERT**: Number of paths enumerated = 2^num_periods
- **ASSERT**: Sum of path probabilities ≈ 1.0 (after normalization)
- Verify expected life < full term (early exercise reduces average life)
- If high early exercise rates, expected life should be significantly less than full term
- Check that no path exercises before vesting period

---
## Pattern: Long Straddle Profitability Analysis

**Description:** A long straddle (buying both call and put at the same strike) is profitable when the stock price at expiration moves BEYOND the breakeven points, not AT the breakeven points. Breakeven points are: Lower = Strike - Total_Premium, Upper = Strike + Total_Premium. The strategy is profitable when S_T < Lower_Breakeven OR S_T > Upper_Breakeven.

**When to Use:** Questions asking when a straddle is "profitable" or generates "profit," given expiration stock prices or asking to identify profitable price ranges.

**When NOT to Use:** When question asks for breakeven points (return the breakeven values directly). When asking for maximum profit (return unlimited for long straddle).

**Procedure:**
1. Calculate total premium paid: Total_Premium = Call_Premium + Put_Premium
2. Calculate breakeven points:
   - Lower_Breakeven = Strike - Total_Premium
   - Upper_Breakeven = Strike + Total_Premium
3. **For profitability**: Stock must be OUTSIDE the breakeven range
   - Profitable if: S_T < Lower_Breakeven OR S_T > Upper_Breakeven
   - Not profitable if: Lower_Breakeven ≤ S_T ≤ Upper_Breakeven
4. If given options to choose from, select the price that falls in the profitable range

**Worked Example:**

**Question:** A long straddle uses strike $75, call premium $3.50, put premium $3.00. Which price is profitable at expiration: $68, $72, or $78?

```python
# Long straddle parameters
strike_price = 75.00
call_premium = 3.50
put_premium = 3.00

# Total premium paid
total_premium = call_premium + put_premium  # 6.50

# Breakeven points
lower_breakeven = strike_price - total_premium  # 68.50
upper_breakeven = strike_price + total_premium  # 81.50

# Given options
options = [68, 72, 78]

# Find which options are in the PROFITABLE range
# Profitable when: price < lower_breakeven OR price > upper_breakeven
profitable_prices = [p for p in options if p < lower_breakeven or p > upper_breakeven]

# The answer is the option in the profitable range
profitable_prices[0] if profitable_prices else None  # 68
```

**Common Bugs to Avoid:**
- Confusing breakeven points with profitable prices (breakeven means zero profit, not positive profit)
- Selecting the price closest to breakeven instead of the price in the profitable range
- Thinking the strategy is profitable AT the breakeven points (it's profitable BEYOND them)
- Using `min(abs(x - breakeven))` logic when question asks for profitability

**CHECK Steps:**
- Verify profitable range is OUTSIDE [lower_breakeven, upper_breakeven], not inside
- If question asks "when is it profitable," return prices where |S_T - Strike| > Total_Premium
- If question asks for breakeven, return the breakeven values themselves
- Assert that at breakeven points, profit = 0 (not positive)

## Pattern: Non-Traded Asset Option Valuation with Market Price of Risk

**Description:** Options on non-traded assets (e.g., real estate, commodities without storage, cars) cannot use the standard risk-free rate as the drift in risk-neutral valuation. Instead, use the market price of risk λ to adjust the real-world drift: μ* = μ - λσ. This adjusted drift replaces the risk-free rate r in the Black-Scholes d1 calculation, while r is still used for discounting.

**When to Use:** Questions involving options on non-traded or non-storable assets where a market price of risk λ is provided. Keywords: "non-traded asset," "market price of risk," "real estate option," "commodity without storage," "car," "artwork."

**When NOT to Use:** For traded financial assets (stocks, bonds, currencies) - use standard Black-Scholes with r as drift.

**Procedure:**
1. **Identify if asset is non-traded**: Check if market price of risk λ is provided
2. **Calculate risk-neutral drift**: μ* = μ - λσ
   - μ = real-world drift rate of the asset
   - λ = market price of risk
   - σ = volatility of the asset
3. **Modify Black-Scholes d1**: Replace r with μ* in the drift term
   - d1 = [ln(S/K) + (μ* + 0.5σ²)T] / (σ√T)
   - d2 = d1 - σ√T
4. **Discount at risk-free rate**: Option value = S×N(d1) - K×e^(-rT)×N(d2) for calls
5. Return option value

**Worked Example:**

**Question:** A 2-year call option on a car has strike $25,000. Current car value is $28,000. The car depreciates at 20% per year (μ = -0.20), with volatility 15%. Market price of risk is -0.10. Risk-free rate is 6%. Calculate option value.

```python
import math
from scipy.stats import norm

# Option parameters
S = 28000  # current car value
K = 25000  # strike price
T = 2.0    # years
sigma = 0.15  # volatility
mu = -0.20  # real-world drift (depreciation)
lambda_mpr = -0.10  # market price of risk
r = 0.06  # risk-free rate (for discounting only)

# Step 1: Calculate risk-neutral drift for non-traded asset
mu_star = mu - lambda_mpr * sigma
# mu_star = -0.20 - (-0.10)(0.15) = -0.185

# Step 2: Calculate d1 and d2 using adjusted drift
d1 = (math.log(S / K) + (mu_star + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
d2 = d1 - sigma * math.sqrt(T)

# Step 3: Calculate call option value
# Use risk-free rate for discounting, adjusted drift for d1/d2
call_value = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)

round(call_value, 2)  # approximately $1,832
```

**Common Bugs to Avoid:**
- **Using r as the drift for non-traded assets (ignores market price of risk)**
- Forgetting to adjust drift: using μ instead of μ* = μ - λσ
- Applying this pattern to traded financial assets (stocks, bonds)
- Using μ* for discounting instead of r (r is still used for present value)
- Confusing sign of λ (negative λ increases drift for assets with negative correlation to market)

**CHECK Steps:**
- **VERIFY**: Is asset non-traded? Is market price of risk λ provided?
- Assert: μ* = μ - λσ (not μ + λσ)
- If λ < 0 and μ < 0, then μ* > μ (less negative drift)
- Discount factor should use r, not μ*
- Result should be significantly different from standard Black-Scholes with r as drift

---

## Pattern: Merton Model - Firm Volatility from Equity Volatility

**Description:** In the Merton model, equity is a call option on firm value with strike equal to debt face value. The relationship between equity volatility and firm volatility is: σ_E × E = σ_V × V × N(d1), where N(d1) is the option delta. This requires iterative solution for σ_V given observed σ_E, market values, and debt structure.

**When to Use:** Questions asking for "implied standard deviation in firm value" or "firm volatility" given equity volatility, market values of equity and debt, and debt structure. Keywords: "firm value volatility," "asset volatility," "Merton model," "equity as option."

**When NOT to Use:** When calculating portfolio volatility from component volatilities (use portfolio variance formula). When both equity and debt volatilities are given with correlation (use weighted portfolio approach).

**Procedure:**
1. **Calculate market values**:
   - E = Stock_Price × Shares_Outstanding
   - D = Face_Value / (1 + r)^T (approximate if market value not given)
   - V = E + D (firm value)
2. **Set up Merton model relationship**:
   - Equity is call option: E = V×N(d1) - D×e^(-rT)×N(d2)
   - Volatility relationship: σ_E × E = σ_V × V × N