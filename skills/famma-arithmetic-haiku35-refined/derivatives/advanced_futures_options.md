# Derivatives — Advanced Futures and Options Pricing

## CODE CONSTRAINTS (MANDATORY)

**Your generated code MUST:**
- ✅ End with variable name or expression (for eval() to capture)
- ✅ Include ALL necessary imports at the top
- ✅ Define ALL variables before use
- ✅ Use explicit values from the question

**Your generated code MUST NOT:**
- ❌ Use input() or any interactive functions
- ❌ Use print() as the last line (returns None)
- ❌ Use variables without defining them first

**Available libraries (must import if used):**
- import math
- import numpy as np
- from scipy.stats import norm
- from scipy.optimize import brentq

---

## Pattern: Treasury Bond Futures Quoted Price (Cost-of-Carry Model)

**Description:** Calculate the quoted futures price for a Treasury bond futures contract using the cost-of-carry model. This is DIFFERENT from the invoice price at delivery. The quoted futures price accounts for the time value of money, coupons paid during the holding period, and accrued interest at both current and delivery dates.

**When to Use:**
- Question asks for "quoted futures price" or "futures price" (not "invoice price")
- Given: bond spot price, coupon rate, delivery date, risk-free rate, conversion factor
- May involve coupons paid between current date and delivery date

**When NOT to Use:**
- Question asks for "invoice price" (use: Invoice Price = Quoted Futures Price × Conversion Factor + Accrued Interest at Delivery)
- Question asks for cheapest-to-deliver (CTD) bond selection
- Question involves only settlement calculations at delivery

**Procedure:**
1. Calculate accrued interest at current date (AI_current)
2. Calculate accrued interest at delivery date (AI_delivery)
3. Identify any coupons paid between current date and delivery date
4. Calculate present value of coupons paid before delivery: PV_coupons = Coupon × exp(-r × t_coupon)
5. Calculate dirty spot price: Spot_dirty = Spot_clean + AI_current
6. Apply cost-of-carry formula: F_dirty = (Spot_dirty - PV_coupons) × exp(r × T) + AI_delivery
7. Calculate quoted futures price: F_quoted = F_dirty / Conversion_Factor

**Worked Example:**
**Question:** A Treasury bond with 12% annual coupon (paid semi-annually on Feb 4 and Aug 4) is trading at $115 on July 1. A futures contract on this bond matures on Sept 30. The risk-free rate is 10% per annum (continuous). The conversion factor is 1.4. Calculate the quoted futures price.

```python
import math

# Bond parameters
spot_clean = 115.0  # Clean spot price
coupon_rate = 0.12  # Annual coupon rate
coupon_payment = (coupon_rate / 2) * 100  # Semi-annual coupon on $100 face value = 6.0
conversion_factor = 1.4
risk_free_rate = 0.10  # Continuous compounding

# Time calculations (in years)
# Current date: July 1
# Last coupon: Feb 4 (147 days ago, assuming 365-day year)
# Next coupon: Aug 4 (34 days from July 1)
# Delivery date: Sept 30 (91 days from July 1)
# Days between coupons: 181 days (Feb 4 to Aug 4)

days_since_last_coupon_current = 147
days_between_coupons = 181
days_to_delivery = 91
days_to_next_coupon = 34
days_since_last_coupon_delivery = 147 + 91  # 238 days

# Step 1: Accrued interest at current date (July 1)
AI_current = coupon_payment * (days_since_last_coupon_current / days_between_coupons)

# Step 2: Accrued interest at delivery date (Sept 30)
# Note: Aug 4 coupon occurs before Sept 30, so we count from Aug 4
days_from_aug4_to_sept30 = 57
AI_delivery = coupon_payment * (days_from_aug4_to_sept30 / days_between_coupons)

# Step 3: Identify coupons paid before delivery
# Aug 4 coupon (6.0) is paid 34 days from now
time_to_coupon = days_to_next_coupon / 365.0

# Step 4: PV of coupons paid before delivery
PV_coupons = coupon_payment * math.exp(-risk_free_rate * time_to_coupon)

# Step 5: Dirty spot price
spot_dirty = spot_clean + AI_current

# Step 6: Time to delivery
T = days_to_delivery / 365.0

# Step 7: Dirty futures price at delivery
futures_dirty = (spot_dirty - PV_coupons) * math.exp(risk_free_rate * T) + AI_delivery

# Step 8: Quoted futures price
quoted_futures_price = futures_dirty / conversion_factor

# Result
quoted_futures_price
```

**Common Bugs to Avoid:**
- **Using invoice price formula instead of cost-of-carry:** Invoice Price = F_quoted × CF + AI is for settlement, not for calculating F_quoted
- **Ignoring coupons paid during holding period:** Must subtract PV of coupons from spot price
- **Using wrong accrued interest dates:** AI_current uses days since last coupon; AI_delivery must account for coupons paid during holding period
- **Confusing clean vs dirty prices:** Spot price is usually quoted clean; must add AI_current to get dirty price
- **Inventing settlement prices:** Use only values given in the question

**CHECK Steps:**
- If a coupon payment date falls between current date and delivery date, verify PV_coupons is subtracted from spot_dirty
- If delivery date is after a coupon payment, verify AI_delivery is calculated from that coupon date, not the previous one
- Assert quoted_futures_price > 0 (negative futures prices are rare and should be verified)
- Verify conversion_factor is applied as divisor, not multiplier

---

## Pattern: Binomial Tree Model Consistency Verification

**Description:** Verify whether a binomial tree model is exactly consistent with the mean and variance of the logarithmic return of the underlying asset. Different binomial models (Cox-Ross-Rubinstein vs. alternative procedures with p=0.5) have different consistency properties.

**When to Use:**
- Question asks if binomial model is "consistent with" or "matches" mean and variance
- Question mentions "logarithm of stock price" or "log returns"
- Question specifies a particular binomial tree construction method (e.g., "alternative procedure with p=0.5")

**When NOT to Use:**
- Question asks to price an option using binomial tree (use standard option pricing patterns)
- Question asks to construct a binomial tree without verifying consistency
- Question involves only risk-neutral pricing without model validation

**Procedure:**
1. Identify the binomial model type:
   - Cox-Ross-Rubinstein (CRR): u = exp(σ√Δt), d = 1/u, p = [exp(rΔt) - d] / [u - d]
   - Alternative with p=0.5: p = 0.5, u and d chosen to match mean and variance exactly
2. For the alternative procedure with p=0.5:
   - u = exp[(r - q - σ²/2)Δt + σ√Δt]
   - d = exp[(r - q - σ²/2)Δt - σ√Δt]
3. Calculate theoretical mean of log return: μ_theory = (r - q - σ²/2)Δt
4. Calculate theoretical variance of log return: σ²_theory = σ²Δt
5. Calculate binomial model mean: μ_model = p × ln(u) + (1-p) × ln(d)
6. Calculate binomial model variance: σ²_model = p × [ln(u)]² + (1-p) × [ln(d)]² - μ_model²
7. Check if μ_model ≈ μ_theory and σ²_model ≈ σ²_theory (within numerical tolerance)

**Worked Example:**
**Question:** Consider an alternative binomial tree procedure where p=0.5, u = exp[(r - q - σ²/2)Δt + σ√Δt], and d = exp[(r - q - σ²/2)Δt - σ√Δt]. For a stock with r=0.05, q=0.02, σ=0.30, and Δt=0.25, is this model exactly consistent with the mean and variance of ln(S_t/S_0)?

```python
import math

# Parameters
r = 0.05  # Risk-free rate
q = 0.02  # Dividend yield
sigma = 0.30  # Volatility
delta_t = 0.25  # Time step
p = 0.5  # Probability for alternative procedure

# Alternative procedure formulas
drift = (r - q - sigma**2 / 2) * delta_t
volatility_term = sigma * math.sqrt(delta_t)

u = math.exp(drift + volatility_term)
d = math.exp(drift - volatility_term)

# Theoretical mean and variance of log return
mu_theory = (r - q - sigma**2 / 2) * delta_t
var_theory = sigma**2 * delta_t

# Binomial model mean and variance
ln_u = math.log(u)
ln_d = math.log(d)

mu_model = p * ln_u + (1 - p) * ln_d
var_model = p * ln_u**2 + (1 - p) * ln_d**2 - mu_model**2

# Check consistency (within numerical tolerance)
mean_consistent = abs(mu_model - mu_theory) < 1e-10
variance_consistent = abs(var_model - var_theory) < 1e-10

# Result: True if both are consistent
is_consistent = mean_consistent and variance_consistent
is_consistent
```

**Common Bugs to Avoid:**
- **Testing wrong model:** Question may ask about "alternative procedure" but code tests CRR model
- **CRR is only approximately consistent:** CRR matches variance well but mean only approximately (not exactly)
- **Forgetting the drift term in alternative procedure:** u and d must include (r - q - σ²/2)Δt term
- **Using arithmetic returns instead of log returns:** Must use ln(u) and ln(d), not (u-1) and (d-1)

**CHECK Steps:**
- If question mentions "alternative procedure" or "p=0.5", verify you're NOT using CRR formulas
- If question asks "exactly consistent", verify tolerance is very small (< 1e-10)
- Assert 0 < p < 1 and u > 1 > d > 0 (basic binomial tree properties)

---

## Pattern: Rolling Hedge Gain/Loss Calculation

**Description:** Calculate the cumulative gain or loss from a rolling hedge strategy where futures contracts are closed and new contracts are opened at specified dates (stack-and-roll). Each contract period's gain/loss is calculated independently using entry and exit prices.

**When to Use:**
- Question involves "rolling hedge" or "stack and roll" strategy
- Multiple futures contracts with different maturity dates
- Table or data showing futures prices at different dates for different contract months
- Question asks for "total gain" or "gain per unit" from the hedge

**When NOT to Use:**
- Single futures contract held to maturity (use simple futures gain/loss)
- Question asks about optimal hedge ratio (use regression-based hedge ratio)
- Question involves basis risk analysis without calculating actual gains

**Procedure:**
1. Identify all contract periods and their entry/exit dates
2. For each contract period:
   - Entry price = Futures price when contract is opened
   - Exit price = Futures price when contract is closed (at roll date or final settlement)
   - Gain/Loss = (Entry price - Exit price) for short position, or (Exit price - Entry price) for long position
3. Sum all individual contract gains/losses
4. Multiply by position size if needed (contracts × contract size)

**Worked Example:**
**Question:** A company hedges oil price risk using a rolling short futures strategy. It shorts 1,000 barrels using the following contracts: Oct 2021 (opened at $48.20, closed at $47.40), Mar 2022 (opened at $47.00, closed at $46.50), July 2022 (opened at $46.30, closed at $45.90). What is the total gain per barrel?

```python
# Rolling hedge data: (entry_price, exit_price) for each contract period
# Short position: gain when price falls

# Contract 1: Oct 2021
entry_1 = 48.20
exit_1 = 47.40
gain_1 = entry_1 - exit_1  # Short position gains when price falls

# Contract 2: Mar 2022
entry_2 = 47.00
exit_2 = 46.50
gain_2 = entry_2 - exit_2

# Contract 3: July 2022
entry_3 = 46.30
exit_3 = 45.90
gain_3 = entry_3 - exit_3

# Total gain per barrel
total_gain_per_barrel = gain_1 + gain_2 + gain_3

total_gain_per_barrel
```

**Common Bugs to Avoid:**
- **Using next contract's opening price as current contract's exit price:** Each contract has its own exit price at the roll date
- **Using spot price as futures exit price:** Futures prices and spot prices are different; use actual futures prices
- **Confusing long and short positions:** Short gains when price falls (entry - exit); long gains when price rises (exit - entry)
- **Forgetting to sum all periods:** Must add gains/losses from all contract periods

**CHECK Steps:**
- If position is short, verify gain = entry - exit (positive when price falls)
- If position is long, verify gain = exit - entry (positive when price rises)
- Assert number of contract periods matches number of roll dates + 1
- Verify each exit price corresponds to the correct date (not the next contract's opening price)

---

## Pattern: Volatility Smile Qualitative Assessment

**Description:** Assess whether a probability estimate based on the lognormal (Black-Scholes) assumption is "too high" or "too low" when compared to market-implied probabilities from the volatility smile. This is a qualitative assessment based on the shape of the volatility smile and the strike range.

**When to Use:**
- Question asks "would you expect the estimate to be too high or too low"
- Question mentions "volatility smile" or "implied volatility varies with strike"
- Question involves comparing lognormal assumption to market reality
- Keywords: "too high", "too low", "overestimate", "underestimate"

**When NOT to Use:**
- Question asks for numerical probability calculation only (use lognormal distribution)
- Question asks to calculate implied volatility from option prices
- Question involves volatility surface calibration or model fitting

**Procedure:**
1. Calculate the probability using lognormal assumption (if required)
2. Identify the strike range or price range in question
3. Determine if the range is:
   - In-the-money (ITM) / Out-of-the-money (OTM) relative to current price
   - Near-the-money (ATM) or far from ATM
4. Apply volatility smile principles:
   - Volatility smile implies heavier tails than lognormal distribution
   - OTM options have higher implied volatility → higher probability of extreme moves
   - Lognormal assumption UNDERESTIMATES tail probabilities
5. For probability of being in a range:
   - If range includes tail regions (far OTM): Lognormal estimate is TOO LOW
   - If range is centered around ATM: Lognormal estimate may be TOO HIGH (probability mass shifted to tails)

**Worked Example:**
**Question:** Using the lognormal assumption, the probability that EUR/USD will be between 0.85 and 0.90 in 3 months is 11.05%. The current rate is 0.8800. Given that a volatility smile exists in the FX market, would you expect this estimate to be too high or too low?

```python
import math
from scipy.stats import norm

# Part 1: Calculate lognormal probability (for reference)
S0 = 0.8800  # Current exchange rate
K_lower = 0.85
K_upper = 0.90
T = 0.25  # 3 months
r_domestic = 0.05  # Example risk-free rate
r_foreign = 0.03  # Example foreign rate
sigma = 0.12  # Example volatility

# Lognormal calculation
mu = (r_domestic - r_foreign - 0.5 * sigma**2) * T
sigma_T = sigma * math.sqrt(T)

d_lower = (math.log(K_lower / S0) - mu) / sigma_T
d_upper = (math.log(K_upper / S0) - mu) / sigma_T

prob_lognormal = norm.cdf(d_upper) - norm.cdf(d_lower)

# Part 2: Qualitative assessment based on volatility smile
# Current rate: 0.8800
# Range: 0.85 to 0.90
# This range is centered around the current rate (slightly below to slightly above)

# Volatility smile principle:
# - Smile implies heavier tails (higher probability of extreme moves)
# - Probability mass shifts from center to tails
# - For a range near ATM, lognormal OVERESTIMATES probability
# - For tail regions (far OTM), lognormal UNDERESTIMATES probability

# Since 0.85-0.90 is centered around current 0.88 (near ATM region):
assessment = "Too high"

# Return the qualitative assessment
assessment
```

**Common Bugs to Avoid:**
- **Returning numerical probability instead of qualitative answer:** Question asks for "too high" or "too low", not a number
- **Ignoring volatility smile context:** Must consider whether range is in tails or center
- **Reversing the logic:** Lognormal underestimates tails (too low for extreme events), overestimates center (too high for near-ATM ranges)
- **Calculating implied volatility when not needed:** Question asks for qualitative comparison, not implied vol calculation

**CHECK Steps:**
- If range includes far OTM strikes (tails), answer should be "Too low"
- If range is centered around ATM, answer should be "Too high"
- Verify the answer is a string ("Too high" or "Too low"), not a number
- If question provides lognormal probability, use it as context but don't return it as the answer

---

## Pattern: Risk-Neutral Probability Distribution from Option Prices (Breeden-Litzenberger)

**Description:** Calculate the risk-neutral probability distribution of the underlying asset price at maturity using the Breeden-Litzenberger formula. This involves computing probability densities from option prices and then integrating (summing) over intervals to get probabilities for price ranges.

**When to Use:**
- Question asks for "probability" or "probability distribution" from option prices
- Given: option prices at multiple strikes (volatility smile data)
- Question mentions "risk-neutral probability" or "implied probability"
- Question asks for probability of price being in a specific range

**When NOT to Use:**
- Question asks for implied volatility only (use implied vol calculation)
- Question involves only lognormal assumption without market option prices
- Question asks for historical or physical probability (not risk-neutral)

**Procedure:**
1. For each strike K, calculate the risk-neutral probability DENSITY using butterfly spread:
   - g(K) = exp(rT) × [C(K-δ) + C(K+δ) - 2×C(K)] / δ²
   - Where C(K) is call option price at strike K, δ is strike spacing
2. Define intervals: [K₁, K₂], [K₂, K₃], etc.
3. For each interval, calculate probability:
   - P(K₁ < S < K₂) = g(K_mid) × ΔK
   - Where K_mid is midpoint of interval, ΔK is interval width
4. Sum probabilities over all intervals in the desired range

**Worked Example:**
**Question:** Call option prices are: C(0.70)=$0.20, C(0.80)=$0.12, C(0.90)=$0.06, C(1.00)=$0.03, C(1.10)=$0.01, C(1.20)=$0.005, C(1.30)=$0.002. Risk-free rate is 5%, time to maturity is 1 year. Calculate the probability that the price will be between 0.70 and 1.30.

```python
import math

# Given data
strikes = [0.70, 0.80, 0.90, 1.00, 1.10, 1.20, 1.30]
call_prices = [0.20, 0.12, 0.06, 0.03, 0.01, 0.005, 0.002]
r = 0.05
T = 1.0
delta_K = 0.10  # Strike spacing

# Step 1: Calculate probability densities using Breeden-Litzenberger
# g(K) = exp(rT) * [C(K-δ) + C(K+δ) - 2*C(K)] / δ²
discount_factor = math.exp(r * T)
densities = []

for i in range(1, len(strikes) - 1):
    C_minus = call_prices[i - 1]
    C_mid = call_prices[i]
    C_plus = call_prices[i + 1]
    
    density = discount_factor * (C_minus + C_plus - 2 * C_mid) / (delta_K ** 2)
    densities.append(density)

# Densities correspond to strikes[1:-1] = [0.80, 0.90, 1.00, 1.10, 1.20]

# Step 2: Calculate probabilities for each interval
# P(interval) = density × interval_width
probabilities = []

for density in densities:
    prob = density * delta_K
    probabilities.append(prob)

# Step 3: Sum all probabilities for range [0.70, 1.30]
# This includes all intervals from 0.70-0.80, 0.80-0.90, ..., 1.20-1.30
total_probability = sum(probabilities)

total_probability
```

**Common Bugs to Avoid:**
- **Summing densities instead of probabilities:** Must multiply density by interval width before summing
- **Forgetting discount factor:** Breeden-Litzenberger formula includes exp(rT)
- **Wrong interval boundaries:** Density at K corresponds to interval centered at K
- **Using incorrect delta:** δ must match the actual strike spacing in the data

**CHECK Steps:**
- Assert 0 ≤ total_probability ≤ 1 (probabilities must be between 0 and 1)
- If summing over all possible strikes, total probability should be close to 1
- Verify densities are non-negative (negative densities indicate arbitrage or data errors)
- Check that interval widths are correctly applied (multiply, don't just sum densities)

---

## SKILL.md Entry

```
SKILL_MD_ENTRY: | `derivatives/advanced_futures_options.md` | Derivatives | Advanced Futures and Options Pricing | Treasury Bond Futures Quoted Price (Cost-of-Carry Model), Binomial Tree Model Consistency Verification, Rolling Hedge Gain/Loss Calculation, Volatility Smile Qualitative Assessment, Risk-Neutral Probability Distribution from Option Prices (Breeden-Litzenberger) |
```