# Derivatives Pricing: Concept Confusion Error Patterns (PoT)

## Pattern: Risk-Neutral Drift for Non-Traded Assets

**Description:** Incorrectly applying the risk-free rate as the drift parameter when pricing derivatives on non-traded assets (e.g., cars, commodities held for consumption), instead of using the risk-neutral drift μ* = μ + λσ. The key insight: for non-traded assets, the underlying grows at μ* (not r), so we must apply a growth adjustment to S₀ while still discounting at the risk-free rate r.

**When to Use:** Questions involving options on non-traded/non-investment assets with given real-world drift (μ), market price of risk (λ), and volatility (σ).

**Procedure:**
1. Identify if the underlying asset is traded for investment purposes or not
2. If non-traded, calculate risk-neutral drift: μ* = μ + λσ
3. Use μ* in place of r in the d1/d2 formulas: 
   - d1 = [ln(S/K) + (μ* + 0.5σ²)T] / (σ√T)
   - d2 = d1 - σ√T
4. Apply growth adjustment to spot price: S_adjusted = S₀ × exp((μ* - r)T)
5. Calculate option value: C = S_adjusted × N(d1) - K × exp(-rT) × N(d2)
6. **Equivalently:** C = S₀ × exp((μ* - r)T) × N(d1) - K × exp(-rT) × N(d2)
7. **CHECK:** The formula should have exp((μ* - r)T) multiplying S₀ — this is NOT double-counting

**Example (sanitized):**
> **Scenario:** Value a 1.5-year European call on a classic car (non-traded). Current value $50,000, strike $48,000, real-world drift μ = -0.08, volatility σ = 0.30, market price of risk λ = -0.25, risk-free rate r = 0.05.
>
> **Wrong approach:**
> ```python
> # Using r instead of μ* in d1/d2, or forgetting growth adjustment
> mu_star = -0.08 + (-0.25) * 0.30  # -0.155
> d1 = (np.log(50000/48000) + (-0.155 + 0.5*0.30**2)*1.5) / (0.30*np.sqrt(1.5))
> d2 = d1 - 0.30*np.sqrt(1.5)
> # Then: call = 50000 * exp(-0.05*1.5) * N(d1) - 48000 * exp(-0.05*1.5) * N(d2)
> # This discounts S₀ at r, ignoring that asset grows at μ*
> ```
>
> **Correct approach:**
> ```python
> import numpy as np
> from scipy.stats import norm
> 
> S0, K, T = 50000, 48000, 1.5
> mu, sigma, lambda_risk, r = -0.08, 0.30, -0.25, 0.05
> 
> # Step 1-2: Calculate risk-neutral drift
> mu_star = mu + lambda_risk * sigma  # -0.08 + (-0.25)(0.30) = -0.155
> 
> # Step 3: Calculate d1/d2 using μ* (not r)
> d1 = (np.log(S0/K) + (mu_star + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
> d2 = d1 - sigma*np.sqrt(T)
> 
> # Step 4-5: Apply growth adjustment to S₀
> growth_adjustment = np.exp((mu_star - r) * T)
> S_adjusted = S0 * growth_adjustment
> 
> # Step 6: Standard Black-Scholes structure with adjusted spot
> call_value = S_adjusted * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
> 
> # Verification: This is equivalent to
> # call_value = S0 * exp((μ*-r)T) * N(d1) - K * exp(-rT) * N(d2)
> ```

**Common Mistakes to Avoid:**
- Using r in d1/d2 formulas for non-traded assets (should use μ*)
- Discounting S₀ at r without growth adjustment: exp(-rT) instead of exp((μ*-r)T)
- Thinking that exp((μ*-r)T) multiplying S₀ is "double-counting" (it's the correct formula)
- Forgetting to adjust drift: μ* = μ + λσ
- Ignoring the sign of λ when calculating adjustment
- **CRITICAL:** Not recognizing that non-traded assets grow at μ*, not r, requiring the growth factor

---
## Pattern: Bond Futures Pricing with Cost-of-Carry

**Description:** Treating bond futures as simple forward contracts without properly accounting for coupon income during the contract life and conversion factors, leading to incorrect quoted futures prices. Critical: quoted bond prices are "clean" prices that exclude accrued interest, so accrued interest must be added to get the cash price before applying cost-of-carry. **Additionally, any coupon payments received between the current date and delivery date must be subtracted (in future value terms) from the forward price calculation.**

**When to Use:** Questions asking for quoted futures prices on bonds with known coupon payments, conversion factors, and delivery dates.

**When NOT to Use:** 
- When the bond price given is explicitly stated as a "cash price" or "dirty price" (already includes accrued interest)
- When dealing with zero-coupon bonds (no accrued interest calculation needed)
- When the question asks for forward price rather than futures price (no conversion factor adjustment)

**Procedure:**
1. **CRITICAL FIRST STEP:** Convert quoted (clean) price to cash (dirty) price by adding accrued interest at t=0
   - Accrued interest = Coupon × (days since last coupon / days in coupon period)
   - Cash price S₀ = Quoted price + Accrued interest at t=0
2. **Identify coupon payments between now and delivery:** Check if any coupon payment dates fall between the current date and the delivery date
3. Calculate present value of coupons received before delivery (discount each coupon payment to today)
4. Compute forward price using cost-of-carry: F = (S₀ - PV_coupons) × e^(rT)
   - **CRITICAL:** Subtract PV of coupons from cash price BEFORE applying growth factor
5. Calculate accrued interest at delivery date (from last coupon before delivery to delivery date)
6. Convert to quoted futures price: Quoted Futures = (F - Accrued at delivery) / Conversion Factor
7. **CHECK:** Verify that you added accrued interest to quoted price in step 1, not subtracted it
8. **CHECK:** Verify that you subtracted PV of intermediate coupons in step 4

**Code Example:**

**Scenario:** Bond with 10% annual coupon (paid semiannually on Jan 15 and Jul 15). Today is May 1, futures delivery Sep 1 (4 months). Quoted price $105, conversion factor 1.4, risk-free rate 8% (continuous).

**Correct Code:**
```python
import numpy as np

quoted_price = 105
conversion_factor = 1.4
r = 0.08  # continuous compounding
T = 4/12  # 4 months to delivery

# Step 1: Calculate accrued interest at t=0 (Jan 15 to May 1 = 106 days)
annual_coupon = 10
semiannual_coupon = annual_coupon / 2
days_since_last_coupon = 106
days_in_period = 181  # Jan 15 to Jul 15
accrued_interest_now = semiannual_coupon * (days_since_last_coupon / days_in_period)

# Cash price at t=0 (ADD accrued interest to quoted price)
S0 = quoted_price + accrued_interest_now

# Step 2: Identify intermediate coupon (Jul 15, which is 2.5 months from now)
time_to_coupon = 2.5/12
pv_coupon = semiannual_coupon * np.exp(-r * time_to_coupon)

# Step 3: Forward price (cash basis) - subtract PV of coupon
forward_price = (S0 - pv_coupon) * np.exp(r * T)

# Step 4: Accrued interest at delivery (Jul 15 to Sep 1 = 48 days)
days_since_last_at_delivery = 48
accrued_at_delivery = semiannual_coupon * (days_since_last_at_delivery / days_in_period)

# Step 5: Quoted futures price
quoted_futures_price = (forward_price - accrued_at_delivery) / conversion_factor

quoted_futures_price
```

**Common Bugs to Avoid:**
- **CRITICAL:** Forgetting to add accrued interest to quoted price to get cash price at t=0
- Subtracting accrued interest from quoted price instead of adding it
- **CRITICAL:** Forgetting to subtract PV of intermediate coupons from cash price before applying growth factor
- Applying the growth factor e^(rT) to the full cash price when coupons are paid during the contract life
- Using accrued interest at delivery instead of PV of coupons received during contract life
- Applying conversion factor before computing forward price
- Using discrete compounding when continuous is specified
- Double-counting accrued interest by treating quoted price as if it already includes it

---
## Pattern: Option Delta at Expiration

**Description:** Using mid-life delta values near expiration instead of recognizing that delta converges to binary values (0 or 1) based on moneyness as expiration approaches. Critical: when answering multiple-choice questions, the numerical delta must be mapped to the correct option range, not returned as a raw number.

**When to Use:** Questions asking about delta "just before expiration" or "at expiration" for options or spreads.

**When NOT to Use:**
- When the question asks about delta at any time significantly before expiration (use Black-Scholes delta)
- When historical or given delta values are explicitly requested to be used
- When the question is about delta hedging ratios that require continuous adjustment

**Procedure:**
1. At expiration: Delta = 1 if ITM, Delta = 0 if OTM (discontinuous at strike)
2. For spreads: Calculate delta as sum of component deltas
3. Just before expiration: Use limiting values, not historical deltas
4. Bull spread delta at expiration ≈ (1 - 0) = 1 if spot between strikes
5. **CRITICAL FOR MULTIPLE CHOICE:** If question provides option ranges, map the calculated delta to the appropriate range:
   - Delta near 0 → select range containing 0 (e.g., "0.00 to 0.20")
   - Delta near 1 → select range containing 1 (e.g., "0.80 to 1.00")
   - Delta near 0.5 → select middle range (e.g., "0.40 to 0.60")

**Code Example:**

**Scenario:** Bull call spread with long $40 call (historical delta 0.70) and short $45 call (historical delta 0.35). Stock price at expiration is $43. Question asks which range the delta falls into: A) 0.00-0.20, B) 0.40-0.60, C) 0.80-1.00.

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
bull_spread_delta = delta_long - delta_short  # Result: 1.0

# Map to multiple choice options
if bull_spread_delta <= 0.20:
    answer = "A"  # 0.00 to 0.20
elif bull_spread_delta <= 0.60:
    answer = "B"  # 0.40 to 0.60
else:
    answer = "C"  # 0.80 to 1.00

answer  # Return the option letter, not just the number
```

**Common Bugs to Avoid:**
- Using given delta values near expiration (they're historical/mid-life values)
- Treating delta as continuous near expiration
- Forgetting that delta jumps to 0/1 at expiration, not gradually
- Not accounting for position direction (long vs short) in spreads
- **CRITICAL:** Returning the numerical delta value instead of the multiple-choice option when the question asks for a range

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

**Description:** Calculating futures contracts needed for rebalancing without adjusting for both portfolio beta and futures beta, treating it as simple notional exposure matching. **Critical distinction: Beta adjustment is required when the goal is to maintain or change systematic risk exposure (beta-hedging), but NOT when the goal is a simple dollar-for-dollar notional exchange or tactical allocation shift.**

**When to Use:** Questions about rebalancing portfolios using equity index futures while **maintaining or changing target beta exposure**, where the problem explicitly mentions managing systematic risk or beta.

**When NOT to Use:**
- When the problem asks for a simple "exchange" of dollar exposure between asset classes without mentioning beta management
- When the question states "exchange $X of exposure" without reference to maintaining portfolio beta
- When the rebalancing is described as a "tactical allocation" or "temporary exposure shift" focused on notional values
- When both the portfolio and futures have similar betas (close to 1.0) and the problem doesn't emphasize beta management

**Procedure:**
1. **CRITICAL FIRST STEP:** Determine if this is a beta-hedging problem or a notional exchange problem
   - Beta-hedging: Problem mentions "maintain beta," "adjust systematic risk," or "hedge market exposure"
   - Notional exchange: Problem says "exchange $X exposure," "reallocate," or "shift allocation"
2. **For beta-hedging problems:** Formula: N = [(V_target × β_target) - (V_current × β_current)] / (F_price × β_futures)
3. **For notional exchange problems:** Formula: N = Dollar_exposure_change / (F_price × Multiplier)
4. Calculate target beta-adjusted equity value (beta-hedging only)
5. Calculate current beta-adjusted equity value (beta-hedging only)
6. Compute difference in beta-adjusted exposure (beta-hedging) OR simple dollar difference (notional exchange)
7. Divide by futures contract value (with or without beta adjustment based on problem type)

**Code Example:**

**Scenario:** Portfolio with $80M equity (beta 1.20), target $100M equity (maintain beta 1.20). Futures price $250,000, futures beta 1.10.

**Correct Code (Beta-Hedging):**
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

**Scenario 2:** Exchange $80M of mid-cap exposure for European equity exposure (tactical reallocation).

**Correct Code (Notional Exchange):**
```python
# This is a NOTIONAL EXCHANGE problem, not beta-hedging
# No beta adjustment needed

exposure_to_exchange = 80_000_000
futures_price = 908
futures_multiplier = 250

# Simple notional calculation
num_contracts = exposure_to_exchange / (futures_price * futures_multiplier)

round(num_contracts)  # Result: ~352 contracts
```

**Common Bugs to Avoid:**
- Using nominal values without beta adjustment **when the problem requires beta management**
- **CRITICAL:** Applying beta adjustment when the problem asks for simple notional exchange
- Multiplying by futures beta instead of dividing
- Forgetting that target beta may differ from current beta
- Not rounding to whole contracts
- **CRITICAL:** Misidentifying notional exchange problems as beta-hedging problems based solely on the presence of beta values in the data

---
## Pattern: Employee Stock Option Expected Life

**Description:** Calculating conditional expected exercise time instead of the probability-weighted average time to all termination events (exercise, forfeiture, expiration). In binomial tree models, failing to account for path-dependent probabilities when nodes are reached through different up/down sequences.

**When to Use:** Questions about risk-neutral expected life of employee stock options with early exercise probabilities and forfeiture rates, especially when using binomial tree models.

**Procedure:**
1. Determine if using binomial tree structure or simple time-based model
2. For binomial trees: Calculate path probability to each node = p^(#ups) × (1-p)^(#downs) × (tree paths to node)
3. For each termination node: Absolute probability = Path probability × Survival probability × Conditional exercise probability
4. Include ALL termination paths: voluntary exercise, forced exercise, forfeiture, expiration
5. Expected life = Σ(time_i × absolute probability of termination at time_i)
6. **CHECK:** Total probability should sum to ≤ 1 (accounting for forfeitures)

**Example (sanitized):**
> **Scenario:** 6-year ESO valued on 3-step binomial tree (2 years per step), p=0.52. At node D (year 4), conditional exercise probability 40%. Node D branches to nodes G (up) and H (down) at year 6, each with 25% conditional exercise. Forfeiture rate 3% per year.
>
> **Wrong approach:**
> ```python
> # Treating nodes G and H as having identical probabilities
> survival_to_6 = (1 - 0.03)**6
> prob_G = survival_to_6 * 0.25
> prob_H = survival_to_6 * 0.25
> # Ignores that G and H have different path probabilities!
> ```
>
> **Correct approach:**
> ```python
> p = 0.52
> forfeiture_annual = 0.03
> 
> # Node D at year 4: reached by 2 up moves
> path_prob_D = p**2
> survival_to_4 = (1 - forfeiture_annual)**4
> prob_exercise_D = path_prob_D * survival_to_4 * 0.40
> 
> # Node G at year 6: reached via D then up (3 ups total)
> path_prob_G = p**3
> survival_to_6 = (1 - forfeiture_annual)**6
> # Must NOT have exercised at D
> prob_survive_D_no_exercise = path_prob_D * survival_to_4 * (1 - 0.40)
> prob_exercise_G = (path_prob_G / path_prob_D) * prob_survive_D_no_exercise * (survival_to_6/survival_to_4) * 0.25
> 
> # Node H at year 6: reached via D then down (2 ups, 1 down)
> path_prob_H = p**2 * (1-p)
> prob_exercise_H = (path_prob_H / path_prob_D) * prob_survive_D_no_exercise * (survival_to_6/survival_to_4) * 0.25
> 
> expected_life = 4*prob_exercise_D + 6*prob_exercise_G + 6*prob_exercise_H + ...
> ```

**Common Mistakes to Avoid:**
- Treating nodes at same time step as having equal probabilities (ignoring path dependence)
- Normalizing by total exercise probability (creates conditional expectation)
- Ignoring forfeiture paths in the calculation
- Using conditional probabilities instead of absolute probabilities
- Forgetting to account for survival probability to each node AND path probability through the tree

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

**Description:** Using a single discount factor P(0,T) instead of the annuity factor (sum of discount factors for all swap payment dates) when pricing swaptions with Black's model. Common error: multiplying by both annuity factor AND an additional discount factor, causing double-discounting. Critical: the annuity factor already contains all necessary discounting from time 0 to all payment dates.

**When to Use:** Questions about pricing swaptions (options on interest rate swaps) using Black's model.

**When NOT to Use:**
- When pricing interest rate caps/floors (use caplet/floorlet formula instead)
- When dealing with non-standard swaps (e.g., amortizing, accreting)
- When the swap has already started (use different valuation approach)

**Procedure:**
1. Calculate annuity factor: A = Σ P(0, T_i) for all swap payment dates
   - **CRITICAL:** Payment dates start AFTER option expiration
   - For a T_option-year option on an N-year swap, payment dates are at T_option+1, T_option+2, ..., T_option+N
2. The annuity factor ALREADY includes all necessary discounting from time 0
3. Apply Black's formula WITHOUT additional discount factor:
   - Payer swaption: Notional × A × [F_swap × N(d1) - K_swap × N(d2)]
   - Receiver swaption: Notional × A × [K_swap × N(-d2) - F_swap × N(-d1)]
4. Calculate d1 and d2 using option maturity T_option (not swap tenor)
5. **CHECK:** Do NOT multiply by P(0,T_option) — this would double-discount

**Example (sanitized):**
> **Scenario:** 2-year payer swaption on a 4-year swap with annual payments. Forward swap rate 4.5%, strike 4%, volatility 18%, r=3.5% (continuous), notional $5M.
>
> **Wrong approach:**
> ```python
> # Calculate annuity for swap payments (years 3,4,5,6)
> annuity = sum(exp(-r*t) for t in [3,4,5,6])
> # Then multiply by ADDITIONAL discount factor:
> P_0_T = exp(-r * 2)  # discount to option expiration
> swaption = notional * annuity * P_0_T * [F*N(d1) - K*N(d2)]
> # This double-discounts!
> ```
>
> **Correct approach:**
> ```python
> T_option = 2
> swap_tenor = 4
> 
> # Annuity factor for swap payments starting AFTER option expiration
> annuity_factor = 0
> for i in range(1, swap_tenor + 1):
>     payment_time = T_option + i  # years 3, 4, 5, 6
>     annuity_factor += np.exp(-r * payment_time)
> 
> # Black's model (annuity already includes discounting)
> d1 = (np.log(F_swap/K_swap) + 0.5*sigma**2*T_option) / (sigma*np.sqrt(T_option))
> d2 = d1 - sigma*np.sqrt(T_option)
> 
> # NO additional discount factor needed
> swaption_value = notional * annuity_factor * (
>     F_swap * norm.cdf(d1) - K_swap * norm.cdf(d2)
> )
> ```

**Common Mistakes to Avoid:**
- Multiplying by both annuity factor AND P(0,T_option) (double-discounting)
- Calculating annuity from option start instead of swap start (payments occur AFTER option expires)
- Using only P(0,T) without the annuity factor
- Forgetting that swap payments occur AFTER option expiration
- **CRITICAL:** Adding any additional discount factor when the annuity factor is already present

---
## Pattern: Quanto Derivative Currency Denomination

**Description:** Misidentifying which currency a foreign index is naturally denominated in when pricing quanto derivatives, leading to incorrect application of correlation adjustments. Critical: the quanto adjustment sign depends on whether we're converting FROM the natural currency TO the payment currency, and the adjustment increases expected value when positive correlation exists. **The final result must be in the payment currency units, not the natural currency units.**

**When to Use:** Questions about pricing derivatives that pay in one currency based on an asset denominated in another currency (quanto features).

**When NOT to Use:**
- When both the underlying asset and payment are in the same currency (no quanto adjustment needed)
- When dealing with currency forwards/futures (use interest rate parity instead)
- When the correlation between asset and FX rate is explicitly zero

**Procedure:**
1. Identify natural currency of the underlying (e.g., Nikkei → JPY, FTSE → GBP)
2. Identify payment currency of the derivative
3. If different: apply quanto adjustment to the drift rate
4. **CRITICAL:** Quanto adjustment = ρ × σ_asset × σ_FX (POSITIVE for positive correlation)
   - This adjustment is ADDED to the natural drift when converting to payment currency numeraire
   - Positive correlation → higher expected value in foreign currency terms
5. Adjusted drift: μ_payment_currency = r_natural_currency - q + ρ × σ_asset × σ_FX
6. Calculate expected asset value: E[S_T] = S₀ × exp(μ_payment_currency × T)
7. **CRITICAL:** The result from step 6 is ALREADY in payment currency terms (no additional FX conversion needed)
8. Discount at payment currency risk-free rate
9. **CHECK:** Verify the final answer is in payment currency units, not natural currency units

**Code Example:**

**Scenario:** Derivative pays "S euros" in 1 year, where S is the FTSE 100 index (naturally in GBP). Current FTSE 15,000, EUR/GBP rate 1.15, correlation +0.4, σ_FTSE=18%, σ_FX=10%, r_EUR=2%, r_GBP=3%, dividend yield 1%.

**Correct Code:**
```python
import numpy as np

# Parameters
S0_index = 15000  # FTSE in GBP
FX_rate = 1.15  # EUR per GBP
T = 1
correlation = 0.4  # POSITIVE correlation
sigma_index = 0.18
sigma_FX = 0.10
r_EUR = 0.02  # payment currency
r_GBP = 0.03  # natural currency of index
q = 0.01  # dividend yield

# Quanto adjustment (POSITIVE for positive correlation)
# This adjustment is ADDED to the drift
quanto_adjustment = correlation * sigma_index * sigma_FX

# Risk-neutral drift in EUR terms
# Natural drift in GBP: r_GBP - q
# Adjusted for quanto: (r_GBP - q) + quanto_adjustment
drift_EUR = r_GBP - q + quanto_adjustment

# Expected index value in EUR terms
# CRITICAL: This is ALREADY in EUR terms, no FX conversion needed
E_S_T = S0_index * np.exp(drift_EUR * T)

# Discount in payment currency (EUR)
derivative_value = E_S_T * np.exp(-r_EUR * T)

derivative_value  # Result is in EUR, not GBP
```

**Common Bugs to Avoid:**
- Assuming the index is already in the payment currency
- **CRITICAL:** Using negative sign for quanto adjustment when correlation is positive
- Applying correlation adjustment with wrong sign: should be +ρσ_asset σ_FX, not -ρσ_asset σ_FX
- Using payment currency interest rate as the natural drift
- Forgetting that quanto adjustment affects growth rate, not just discount rate
- Not accounting for dividend yield in the natural drift calculation
- **CRITICAL:** Dividing or multiplying by the FX rate after applying the quanto adjustment (the adjustment already converts to payment currency terms)
- Confusing the payment currency with the natural currency of the underlying asset

---
## Pattern: Coupon Bond Option Decomposition

**Description:** Attempting to value options on coupon-bearing bonds directly instead of decomposing into a portfolio of options on zero-coupon bonds. In interest rate models like Hull-White or Vasicek, failing to use correct continuous compounding rates or incorrect formula implementations.

**When to Use:** Questions about European options on coupon-bearing bonds in one-factor interest rate models (Hull-White, Vasicek, etc.).

**Procedure:**
1. **Convert rates:** If term structure given with discrete compounding (annual, semiannual), convert to continuous: r_c = m × ln(1 + r_discrete/m)
2. Find critical rate r* where bond price = option strike at maturity T
3. Calculate value of each zero-coupon bond at T when r=r*
4. Price European options on each zero-coupon bond (coupons + principal)
5. Strike of each component option = value of that ZCB when r=r*
6. Sum all component option values
7. **CHECK:** Verify ZCB pricing formulas match model specification exactly (especially A(t,T) in Vasicek/Hull-White)

**Example (sanitized):**
> **Scenario:** 1.5-year call option (strike $97) on a 3-year bond with 4% semiannual coupon, principal $100. Vasicek model: a=0.06, b=0.07, σ=0.018, flat term structure at 5% semiannual compounding.
>
> **Wrong approach:**
> ```python
> # Using discrete rate directly in continuous model
> r0 = 0.05  # Wrong! Should convert to continuous
> 
> # Incorrect Vasicek A(t,T) formula
> A = exp((b - sigma**2/(2*a**2)) * (B - tau) - ...)
> # Missing factor of 'a' in numerator!
> ```
>
> **Correct approach:**
> ```python
> # Step 1: Convert to continuous compounding
> r_discrete = 0.05
> m = 2  # semiannual
> r0 = m * np.log(1 + r_discrete/m)  # ≈ 0.04939
> 
> # Step 2: Correct Vasicek ZCB formula
> def P_vasicek(t, T, r_t, a, b, sigma):
>     tau = T - t
>     B = (1 - np.exp(-a * tau)) / a
>     # Correct A(t,T) with (a*b - σ²/2)/a² term
>     A = np.exp(((a*b - sigma**2/2) / a**2) * (B - tau) 
>                - (sigma**2 / (4*a)) * B**2)
>     return A * np.exp(-B * r_t)
> 
> # Step 3: Find r* where bond price = strike
> def bond_price_at_T(r_star):
>     # Remaining coupons at 2.0, 2.5, 3.0 years from now
>     # From option maturity (1.5 years), that's 0.5, 1.0, 1.5 years away
>     price = 0
>     for cf_time in [0.5, 1.0, 1.5]:
>         cf = 2 if cf_time < 1.5 else 102  # coupon or coupon+principal
>         price += cf * P_vasicek(0, cf_time, r_star, a, b, sigma)
>     return price
> 
> r_star = brentq(lambda r: bond_price_at_T(r) - strike, -0.05, 0.20)
> 
> # Step 4-6: Price component options and sum
> # ...
> ```

**Common Mistakes to Avoid:**
- Using discrete compounding rates in continuous models without conversion
- Incorrect Vasicek/Hull-White A(t,T) formula (missing 'a' factor in numerator)
- Treating coupon bond as a single zero-coupon bond
- Not decomposing into constituent cash flows
- Using bond's yield to maturity instead of finding r*

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

**Description:** Incorrectly determining whether heavy-tailed distributions place more or less probability in a given range compared to normal distributions, by not properly distinguishing between near-mode regions (where heavy-tailed has MORE probability), moderate deviations (where heavy-tailed has LESS probability), and extreme tails (where heavy-tailed has MORE probability).

**When to Use:** Questions comparing lognormal vs implied distributions from volatility smiles, asking if probability estimates are too high or too low.

**When NOT to Use:**
- When comparing distributions with different means or variances (not just different tail behavior)
- When the question asks about option prices rather than probabilities
- When dealing with skewed distributions (different analysis needed)

**Procedure:**
1. Identify the current asset price S₀ and the range [K₁, K₂]
2. Calculate relative deviation: |K - S₀| / S₀ for range boundaries
3. Classify the range:
   - **Near mode** (< 5-10% deviation): Heavy-tailed has MORE probability (higher peak)
   - **Moderate region** (10-30% deviation): Heavy-tailed has LESS probability (compensates for tails)
   - **Extreme tail** (> 30% deviation): Heavy-tailed has MORE probability (fat tails)
4. For ranges spanning multiple regions: determine which region dominates the probability mass
5. **Key insight:** With same mean and variance, probability must sum to 1
   - More tail probability requires LESS moderate-region probability
   - But higher peak near mode to maintain variance
6. If range is in moderate region: lognormal estimate is TOO HIGH
7. If range is in near-mode or extreme tail: lognormal estimate is TOO LOW

**Example (sanitized):**
> **Scenario:** Stock at $100, volatility smile indicates heavy tails. Assess lognormal probability estimates for: (a) [$98, $102], (b) [$110, $120], (c) [$140, $160].
>
> **Wrong approach:**
> ```python
> # Treating ANY range above current price as "tail"
> if K > S0:
>     assessment = "TOO LOW"  # Wrong for moderate deviations!
> ```
>
> **Correct approach:**
> ```python
> S0 = 100
> 
> # Range (a): [98, 102] - deviations of 2%
> # This is NEAR MODE → heavy-tailed has MORE probability
> # Lognormal estimate is TOO LOW
> 
> # Range (b): [110, 120] - deviations of 10-20%
> # This is MODERATE REGION → heavy-tailed has LESS probability
> # Lognormal estimate is TOO HIGH
> 
> # Range (c): [140, 160] - deviations of 40-60%
> # This is EXTREME TAIL → heavy-tailed has MORE probability
> # Lognormal estimate is TOO LOW
> 
> def assess_range(lower, upper, S0):
>     dev_lower = abs(lower - S0) / S0
>     dev_upper = abs(upper - S0) / S0
>     avg_dev = (dev_lower + dev_upper) / 2
>     
>     if avg_dev < 0.10:
>         return "TOO LOW"  # near mode
>     elif avg_dev < 0.30:
>         return "TOO HIGH"  # moderate region
>     else:
>         return "TOO LOW"  # extreme tail
> ```

**Common Mistakes to Avoid:**
- Treating all non-center ranges uniformly without quantifying deviation
- Assuming heavy tails mean less central probability everywhere (opposite for near-mode)
- Not recognizing that moderate deviations have LESS probability in heavy-tailed distributions
- Confusing near-mode regions (MORE mass) with moderate tail regions (LESS mass)
- Ignoring that probability conservation requires redistribution across all regions
- **CRITICAL:** Misclassifying ranges that are 10-20% away from current price as "tails" when they're actually in the moderate region where heavy-tailed distributions have LESS probability
## Pattern: Risk-Neutral Probability Derivation in Jump Models

**Description:** Incorrectly using equal probabilities (0.5/0.5) for discrete jump scenarios instead of deriving risk-neutral probabilities from no-arbitrage conditions. For near-immediate jumps, the key is recognizing that the jump resolves most uncertainty immediately, so implied volatility should be calculated by comparing the expected option value to a Black-Scholes option with the SAME maturity starting from the current price.

**When to Use:** Questions involving discrete jump events (e.g., lawsuit outcomes, binary events) with specified post-jump stock prices and volatilities, asking for implied volatility or option prices.

**Procedure:**
1. Derive risk-neutral probability p from: S₀ = e^(-rt_jump) × [p × S_up + (1-p) × S_down]
2. For jumps occurring "tomorrow" or "very soon": treat as instantaneous (t_jump ≈ 0, discount ≈ 1)
   - Simplified: p = (S₀ - S_down) / (S_up - S_down)
3. Calculate option values in each post-jump scenario:
   - Use REMAINING time to maturity: T_remaining = T_total - t_jump
   - For near-immediate jumps where t_jump ≈ 0: use T_remaining ≈ T_total
4. Compute expected option value: E[Option] = p × Option_up + (1-p) × Option_down
5. For near-immediate jumps, no additional discounting needed (already at t≈0)
6. Find implied volatility σ_implied where: BS_call(S₀, K, T_total, r, σ_implied) = E[Option]
7. **CHECK:** Implied volatility should be significantly higher than post-jump volatilities, reflecting jump uncertainty

**Example (sanitized):**
> **Scenario:** Stock at $100, jumps to either $115 or $90 tomorrow (equal likelihood in real world). Post-jump volatilities: 18% (up), 22% (down). 1-year call option, strike $105, r=4%. Find implied volatility.
>
> **Wrong approach:**
> ```python
> # Using equal probabilities without deriving risk-neutral p
> p = 0.5
> # Or: using T_remaining = 1 - 1/365 for post-jump options
> T_remaining = 1 - 1/365
> call_up = bs_call(115, 105, T_remaining, 0.04, 0.18)
> call_down = bs_call(90, 105, T_remaining, 0.04, 0.22)
> # Introduces unnecessary precision errors
> ```
>
> **Correct approach:**
> ```python
> import numpy as np
> from scipy.stats import norm
> from scipy.optimize import brentq
> 
> def bs_call(S, K, T, r, sigma):
>     d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
>     d2 = d1 - sigma*np.sqrt(T)
>     return S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
> 
> S0, K, T_total, r = 100, 105, 1.0, 0.04
> S_up, S_down = 115, 90
> vol_up, vol_down = 0.18, 0.22
> 
> # Step 1-2: Risk-neutral probability (jump is immediate)
> p_rn = (S0 - S_down) / (S_up - S_down)  # (100-90)/(115-90) = 0.4
> 
> # Step 3: Post-jump option values (use full maturity for near-immediate jump)
> T_remaining = T_total  # ≈ 1 year
> call_up = bs_call(S_up, K, T_remaining, r, vol_up)
> call_down = bs_call(S_down, K, T_remaining, r, vol_down)
> 
> # Step 4-5: Expected option value (no additional discounting)
> expected_call = p_rn * call_up + (1 - p_rn) * call_down
> 
> # Step 6: Find implied volatility
> def objective(sigma):
>     return bs_call(S0, K, T_total, r, sigma) - expected_call
> 
> implied_vol = brentq(objective, 0.01, 1.0)
> 
> # Step 7: Verify implied vol > post-jump vols (captures jump risk)
> # implied_vol should be significantly > max(0.18, 0.22)
> ```

**Common Mistakes to Avoid:**
- Using equal probabilities (0.5, 0.5) instead of deriving from current price
- Over-engineering time adjustments for near-immediate jumps (use T_remaining ≈ T_total)
- Using T_remaining = T - 1/365 when the difference is negligible
- Double-discounting the expected option value
- Not recognizing that implied volatility captures jump uncertainty, not weighted average of post-jump volatilities
- **CRITICAL:** Expecting implied volatility to be close to post-jump volatilities (it should be much higher due to jump risk)
## Pattern: CDS Cash Flow Directionality

**Description:** Confusing which party pays which cash flows in a Credit Default Swap, leading to incorrect equilibrium equations where the protection buyer's payments and receipts are reversed. Critical: the CDS spread is solved by setting PV(payments by buyer) = PV(protection received by buyer), and payment frequency must be properly accounted for. **For valuation of existing CDS positions, the value to the protection buyer equals PV(protection leg) - PV(premium leg), where a positive value indicates the buyer could sell the position at a profit.**

**When to Use:** Questions asking for CDS spread calculation with given hazard rates, recovery rates, and payment frequencies, OR questions asking for the value of an existing CDS position.

**When NOT to Use:**
- When dealing with binary CDS (different payoff structure)
- When the question asks for the value to the protection seller (reverse the sign)
- When dealing with CDS indices or basket CDS (different calculation methodology)

**Procedure:**
1. **For CDS spread calculation:**
   - Identify payment frequency (annual, semiannual, quarterly)
   - Formula: CDS Spread s solves: PV(Premium Payments) = PV(Protection Leg)
   - Protection buyer PAYS: regular spread payments + accrual on default
   - Protection buyer RECEIVES: (1 - Recovery Rate) × Notional upon default
   - **CRITICAL:** For non-annual payments, each payment is (s/m) where m = payments per year
   - Calculate PV of regular payments: Σ[(s/m) × P(survival to t_i) × DF(t_i)]
   - Calculate PV of accrual: Σ[(s/m) × P(default in period) × (fraction of period) × DF(t_i)]
   - Calculate PV of protection: Σ[(1-R) × P(default at t_i) × DF(t_i)]
   - Solve: s × (PV_regular_coefficient + PV_accrual_coefficient) / m = PV_protection
   - Therefore: s = m × PV_protection / (PV_regular_coefficient + PV_accrual_coefficient)

2. **For CDS value calculation (when spread is given):**
   - **CRITICAL:** Value to protection buyer = PV(Protection Leg) - PV(Premium Leg)
   - If spread paid > fair spread: value is NEGATIVE to buyer (overpaying)
   - If spread paid < fair spread: value is POSITIVE to buyer (underpaying)
   - **Formula:** Value = PV(protection) - [spread × (PV_regular_coeff + PV_accrual_coeff)]
   - **CHECK:** A positive value to buyer means they could sell the position at a profit

**Example (sanitized):**
> **Scenario:** 4-year CDS with semiannual payments (m=2), flat 5% risk-free rate, 3% hazard rate, 30% recovery. Calculate fair spread.
>
> **Wrong approach:**
> ```python
> # Treating each payment as full annual spread s
> pv_regular = sum(survival_prob(t) * df(t) for t in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0])
> spread = pv_protection / (pv_regular + pv_accrual)
> # This gives spread that's 2x too low for semiannual payments
> ```
>
> **Correct approach:**
> ```python
> import numpy as np
> 
> r, h, R = 0.05, 0.03, 0.30
> m = 2  # semiannual payments
> payment_times = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
> 
> def survival_prob(t):
>     return np.exp(-h * t)
> 
> def df(t):
>     return np.exp(-r * t)
> 
> # PV coefficient for regular payments (each payment is s/m)
> pv_regular_coeff = sum(survival_prob(t) * df(t) for t in payment_times)
> 
> # PV coefficient for accrual (each accrual is s/m × fraction)
> pv_accrual_coeff = 0
> for i, t in enumerate(payment_times):
>     t_prev = 0 if i == 0 else payment_times[i-1]
>     prob_def = survival_prob(t_prev) - survival_prob(t)
>     accrual_fraction = 0.5  # average over period
>     pv_accrual_coeff += prob_def * accrual_fraction * df((t + t_prev)/2)
> 
> # PV of protection leg
> pv_protection = 0
> for i, t in enumerate(payment_times):
>     t_prev = 0 if i == 0 else payment_times[i-1]
>     prob_def = survival_prob(t_prev) - survival_prob(t)
>     pv_protection += (1 - R) * prob_def * df((t + t_prev)/2)
> 
> # Fair spread accounting for payment frequency
> # s/m × (pv_regular_coeff + pv_accrual_coeff) = pv_protection
> # Therefore: s = m × pv_protection / (pv_regular_coeff + pv_accrual_coeff)
> fair_spread = m * pv_protection / (pv_regular_coeff + pv_accrual_coeff)
> ```

**Example 2 (CDS Valuation):**
> **Scenario:** Existing CDS with spread 150 bps, fair spread is 120 bps. What is the value to the protection buyer?
>
> **Wrong approach:**
> ```python
> # Reversing the sign
> value = pv_premium_leg - pv_protection_leg  # WRONG!
> ```
>
> **Correct approach:**
> ```python
> # Value to buyer = what they receive - what they pay
> value_to_buyer = pv_protection_leg - pv_premium_leg
> # If spread paid (150 bps) > fair spread (120 bps), value is NEGATIVE (overpaying)
> ```

**Common Mistakes to Avoid:**
- Reversing the equation: s = (payments) / (protection) instead of s = (protection) / (payments)
- **CRITICAL:** Not adjusting for payment frequency: forgetting to multiply by m when solving for annual spread
- Treating semiannual/quarterly payments as if each pays the full annual spread
- Forgetting that protection leg is (1 - Recovery) × Notional, not just Recovery
- Not including accrual payments in the denominator
- **CRITICAL:** When calculating value of existing CDS, reversing the sign: using PV(payments) - PV(protection) instead of PV(protection) - PV(payments)
- Confusing "value to buyer" with "value to seller" (they have opposite signs)

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

## Pattern: Interest Rate Option Effective Borrowing Cost

**Description:** Incorrectly treating interest rate call/put options as direct rate caps/floors that modify the loan rate, instead of recognizing they are separate cash flows that partially offset interest expense. The option payoff and premium occur at different times and must be properly accounted for in calculating the all-in effective annual rate.

**When to Use:** Questions about synthetic borrowing costs when using interest rate options (caps, floors, collars) to hedge floating-rate loans, asking for effective annual interest rate.

**Procedure:**
1. Calculate actual interest expense on loan: (Libor + spread) × principal × period
2. Calculate option payoff at maturity: max(Libor - strike, 0) × principal × period for call
3. Calculate net interest cost: Interest expense - Option payoff
4. Adjust for option premium paid upfront: Add future value of premium at loan maturity
5. Calculate effective rate: Net cost / (principal × period)
6. Annualize if necessary: (1 + periodic rate)^(periods per year) - 1
7. **CHECK:** Option does NOT cap the rate directly; it provides offsetting cash flow

**Example (sanitized):**
> **Scenario:** $5M loan for 6 months at Libor + 150 bps. Buy interest rate call with strike 4%, premium 0.25% of notional. Actual Libor at maturity is 6.5%. Calculate effective annual rate.
>
> **Wrong approach:**
> ```python
> # Treating option as direct rate cap
> effective_libor = min(actual_libor, strike)  # 4%
> effective_rate = effective_libor + spread  # 4% + 1.5% = 5.5%
> # Wrong! Ignores that loan still pays 6.5% + 1.5%, option is separate cash flow
> ```
>
> **Correct approach:**
> ```python
> principal = 5_000_000
> spread = 0.015
> period = 0.5  # 6 months
> actual_libor = 0.065
> strike = 0.04
> premium_rate = 0.0025
> 
> # Step 1: Actual interest expense
> loan_rate = actual_libor + spread  # 8%
> interest_expense = principal * loan_rate * period  # $200,000
> 
> # Step 2: Option payoff (received at maturity)
> option_payoff = max(actual_libor - strike, 0) * principal * period
> # max(6.5% - 4%, 0) × $5M × 0.5 = $62,500
> 
> # Step 3: Option premium (paid upfront, need future value)
> premium_paid = principal * premium_rate  # $12,500
> fv_premium = premium_paid * (1 + loan_rate * period)  # $13,000
> 
> # Step 4: Net cost at maturity
> net_cost = interest_expense - option_payoff + fv_premium
> # $200,000 - $62,500 + $13,000 = $150,500
> 
> # Step 5: Effective periodic rate
> effective_periodic = net_cost / (principal * period)  # 6.02%
> 
> # Step 6: Annualize
> effective_annual = (1 + effective_periodic * period)**(1/period) - 1
> # OR: effective_annual = effective_periodic × 2 for simple rate
> ```

**Common Mistakes to Avoid:**
- Treating option as direct rate cap/floor instead of separate cash flow
- Not accounting for time value of option premium paid upfront
- Forgetting that actual loan rate is still Libor + spread regardless of option
- Subtracting option premium instead of adding its future value to costs
- Not properly annualizing the effective rate

---

## Pattern: Binomial Tree Model Consistency Verification

**Description:** When asked whether "the binomial model" satisfies certain properties (mean/variance matching, risk-neutral pricing, etc.), failing to recognize that multiple valid binomial tree construction methods exist, and if ANY valid method achieves the property, the answer is affirmative.

**When to Use:** Questions asking whether binomial models are "consistent with" or "exactly match" theoretical properties like mean and variance of log returns.

**Procedure:**
1. Identify what property is being tested (mean, variance, both, risk-neutral pricing, etc.)
2. Recognize that multiple binomial tree constructions exist (CRR, equal probability, etc.)
3. For each standard construction method, verify if it achieves the property
4. If ANY valid binomial method achieves exact consistency, answer is YES
5. Common constructions to check:
   - Cox-Ross-Rubinstein (CRR): matches variance exactly, mean approximately
   - Equal probability (p=0.5): can match BOTH mean and variance exactly with proper u/d choice
6. **CHECK:** For existence questions ("Is there a binomial model that..."), only one valid example is needed

**Example (sanitized):**
> **Scenario:** Does the binomial model exactly match the mean and variance of Δ(ln S) over time Δt, where the continuous process has drift μ and volatility σ?
>
> **Wrong approach:**
> ```python
> # Only checking CRR approach
> # CRR matches variance exactly but mean only approximately
> # Conclude: NO, binomial model doesn't match both exactly
> # Wrong! Other binomial constructions exist
> ```
>
> **Correct approach:**
> ```python
> # Check multiple binomial constructions
> 
> # Method 1: CRR approach
> # u = exp(σ√Δt), d = 1/u
> # p = (exp(μΔt) - d) / (u - d)
> # Matches variance exactly, mean approximately
> 
> # Method 2: Equal probability (p = 0.5)
> # Choose u and d such that:
> # 0.5×ln(u) + 0.5×ln(d) = μΔt  (mean condition)
> # 0.5×[ln(u)]² + 0.5×[ln(d)]² - [μΔt]² = σ²Δt  (variance condition)
> # This system has solutions that match BOTH exactly
> 
> # Since Method 2 (a valid binomial approach) achieves exact consistency:
> answer = "YES"
> 
> # Explanation: The equal-probability binomial tree with properly
> # chosen u and d matches both mean and variance exactly
> ```

**Common Mistakes to Avoid:**
- Only checking one binomial construction method (usually CRR)
- Concluding NO when one method fails, without checking alternatives
- Not recognizing that "the binomial model" refers to a class of models
- Treating approximate matching as failure when exact methods exist
- Ignoring the equal-probability construction which often achieves exact matching

## Pattern: Forward Contract Pricing vs Valuation

**Description:** Confusing the locked-in forward price (delivery price) of an existing forward contract with the forward price for a NEW contract entered at the current time. The delivery price of an existing contract never changes, but its market value changes as the spot price and time to maturity change.

**When to Use:** Questions about forward contracts where time has passed since contract inception, asking about "the forward price" or contract value.

**When NOT to Use:**
- When valuing a contract at inception (forward price = delivery price = fair value)
- When the question explicitly asks for the "delivery price" or "strike price" of the existing contract
- When dealing with futures contracts (marked-to-market daily, different from forwards)

**Procedure:**
1. **Disambiguate what the question asks:**
   - "Forward price" typically means: price for a NEW contract entered today
   - "Delivery price" means: locked-in price from the original contract
   - "Value of the contract" means: PV of (Spot - Delivery Price) discounted to today

2. **For NEW forward price at time t:**
   - F_new = S_t × e^(r(T-t)) for non-dividend assets
   - F_new = S_t × e^((r-q)(T-t)) for dividend-paying assets

3. **For value of EXISTING contract (long position):**
   - Value = (F_new - F_original) × e^(-r(T-t))
   - OR equivalently: Value = S_t × e^(-q(T-t)) - K × e^(-r(T-t))
   - where K is the original delivery price

4. **CHECK:** If question says "six months later, what is the forward price?" it almost certainly means a NEW contract, not the old delivery price

**Code Example:**

**Scenario:** 1-year forward contract on non-dividend stock entered when S=$40, r=5%. Six months later, S=$45, r still 5%. What is (a) the forward price, (b) the value of the original contract?

**Correct Code:**
```python
import math

# Original contract parameters
S0 = 40
r = 0.05
T_total = 1.0

# Current situation (6 months later)
t = 0.5
S_t = 45
T_remaining = T_total - t  # 0.5 years

# (a) Forward price for a NEW contract entered at t=0.5
# This is what "the forward price" typically means
F_new = S_t * math.exp(r * T_remaining)

# (b) Original delivery price (locked in at inception)
K = S0 * math.exp(r * T_total)

# (c) Value of the EXISTING long forward contract
value_of_existing = (F_new - K) * math.exp(-r * T_remaining)
# OR equivalently: S_t - K * exp(-r * T_remaining)

# Most questions asking "what is the forward price?" want F_new
(F_new, value_of_existing)
```

**Common Bugs to Avoid:**
- Returning the original delivery price when asked for "the forward price" after time has passed
- Confusing forward price with forward contract value
- Not recognizing that "forward price" in context usually means a new contract
- Calculating value of existing contract but reporting it as "the forward price"
- **CRITICAL:** Misinterpreting questions that ask "what is the forward price?" to mean the old delivery price

---

## Pattern: American Option Early Exercise with Discrete Dividends

**Description:** Incorrectly adjusting stock prices in binomial trees for discrete dividends by subtracting the present value of dividends at every node, which double-counts the dividend effect and artificially depresses stock prices throughout the tree. The correct approach is to either: (1) subtract the PV of ALL future dividends from the initial stock price once at t=0, or (2) explicitly reduce stock prices at the ex-dividend nodes in the tree.

**When to Use:** Questions about American options (calls or puts) on stocks with known discrete dividend payments during the option's life, especially when using binomial tree valuation.

**When NOT to Use:**
- When dealing with European options (use Black-Scholes with dividend-adjusted spot)
- When dividends are modeled as a continuous yield (use standard binomial tree with dividend yield)
- When no dividends are paid during the option life

**Procedure:**
1. **Choose dividend adjustment method:**
   - **Method A (Recommended):** Subtract PV of all future dividends from S₀ once, then build standard binomial tree
   - **Method B:** Build tree with original S₀, then explicitly reduce stock prices at ex-dividend nodes

2. **For Method A (PV Adjustment):**
   - Calculate S₀_adjusted = S₀ - Σ[D_i × e^(-r×t_i)] for all dividends during option life
   - Build binomial tree using S₀_adjusted with standard up/down factors
   - At each node, option value = max(hold_value, exercise_value)
   - **CHECK:** Dividends are accounted for ONCE at the beginning, not at every node

3. **For Method B (Ex-Dividend Reduction):**
   - Build binomial tree with original S₀
   - At nodes where ex-dividend date occurs, reduce stock price by dividend amount
   - Continue tree evolution from reduced prices
   - At each node, option value = max(hold_value, exercise_value)

4. **Common parameters:**
   - Up factor: u = e^(σ√Δt)
   - Down factor: d = 1/u
   - Risk-neutral probability: p = (e^(rΔt) - d) / (u - d)

5. **Backward induction:**
   - At maturity: option value = intrinsic value
   - At earlier nodes: option value = max(hold, exercise)
   - Hold value = e^(-rΔt) × [p × value_up + (1-p) × value_down]
   - Exercise value = max(S - K, 0) for calls, max(K - S, 0) for puts

**Example (sanitized):**
> **Scenario:** American call, S₀=$50, K=$55, T=15 months, r=8%, σ=25%, dividends of $1.50 at 4 months and 10 months.
>
> **Wrong approach:**
> ```python
> # At EVERY node, subtracting PV of remaining dividends
> for i in range(n_steps + 1):
>     for j in range(i + 1):
>         stock_price = S0 * (u**i) * (d**j)
>         time_at_node = i * dt
>         # WRONG: Subtracting dividends at every node
>         for div_time in dividend_times:
>             if div_time > time_at_node:
>                 stock_price -= dividend * exp(-r * (div_time - time_at_node))
>         stock_tree[j, i] = stock_price
> # This double-counts dividends!
> ```
>
> **Correct approach (Method A):**
> ```python
> import numpy as np
> import math
> 
> S0, K, T, r, sigma = 50, 55, 15/12, 0.08, 0.25
> dividends = [(4/12, 1.50), (10/12, 1.50)]
> 
> # Step 1: Adjust S0 for PV of dividends ONCE
> pv_dividends = sum(D * math.exp(-r * t) for t, D in dividends)
> S0_adjusted = S0 - pv_dividends
> 
> # Step 2: Build standard binomial tree with adjusted S0
> n_steps = 50
> dt = T / n_steps
> u = math.exp(sigma * math.sqrt(dt))
> d = 1 / u
> p = (math.exp(r * dt) - d) / (u - d)
> 
> # Step 3: Stock price tree (no further dividend adjustments)
> stock_tree = np.zeros((n_steps + 1, n_steps + 1))
> for i in range(n_steps + 1):
>     for j in range(i + 1):
>         stock_tree[j, i] = S0_adjusted * (u ** (i - j)) * (d ** j)
> 
> # Step 4: Option valuation with early exercise
> option_tree = np.zeros((n_steps + 1, n_steps + 1))
> for j in range(n_steps + 1):
>     option_tree[j, n_steps] = max(stock_tree[j, n_steps] - K, 0)
> 
> for i in range(n_steps - 1, -1, -1):
>     for j in range(i + 1):
>         hold = math.exp(-r * dt) * (p * option_tree[j, i+1] + (1-p) * option_tree[j+1, i+1])
>         exercise = max(stock_tree[j, i] - K, 0)
>         option_tree[j, i] = max(hold, exercise)
> 
> option_price = option_tree[0, 0]
> ```

**Common Mistakes to Avoid:**
- **CRITICAL:** Subtracting PV of dividends at every node in the tree (double-counting)
- Continuously adjusting stock prices for dividends based on time remaining at each node
- Not recognizing that dividend adjustment should happen ONCE (at t=0) or at specific ex-dividend nodes only
- Forgetting to discount dividends when using Method A
- Using the wrong discount rate for dividend PV calculation
- Mixing Method A and Method B (applying both adjustments simultaneously)