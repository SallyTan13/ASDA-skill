# SKILL PATTERNS FOR DERIVATIVES - UNIT/CURRENCY/PERCENT CONVERSION ERRORS (PoT)

## Pattern: Precision Management in Multi-Step Exponential Discounting

**Description:** Insufficient decimal precision in intermediate calculations involving exponential discount factors (e^(-rt)) leads to compounding rounding errors that accumulate through multi-step formulas, causing final answers to deviate significantly from correct values.

**When to Use:** Put-call parity calculations, bond pricing, CDS valuation, or any derivatives pricing requiring present value calculations with continuous compounding.

**Procedure:**
1. Formula: PV = FV × e^(-r×t) or Put-Call Parity: C - P = S - K×e^(-r×T)
2. Import `math` or `numpy` for exponential functions
3. Store intermediate discount factors with full precision (no manual rounding)
4. Perform all arithmetic operations before any rounding
5. Round only the final result to required decimal places
6. Verify: Check that discount factor is between 0 and 1, closer to 1 for short maturities

**Code Example:**

**Scenario:** Calculate put value using put-call parity where call=$6.50, stock=$92, strike=$95, rate=4.2%, time=0.5 years

**Correct Code:**
```python
import math

# Given values
call_price = 6.50
stock_price = 92
strike_price = 95
risk_free_rate = 0.042
time_to_maturity = 0.5

# Calculate discount factor with full precision
discount_factor = math.exp(-risk_free_rate * time_to_maturity)

# Present value of strike price (full precision)
pv_strike = strike_price * discount_factor

# Put-call parity: P = C - S + K*e^(-rT)
put_price = call_price - stock_price + pv_strike

# Round only at the end
round(put_price, 2)
```

**Common Bugs to Avoid:**
- Rounding discount factor prematurely (e.g., `discount_factor = round(math.exp(-r*t), 4)`)
- Using approximations like `1 - r*t` instead of `math.exp(-r*t)` for discount factors
- Accumulating rounding errors by rounding each intermediate step
- Forgetting to import `math` module for exponential functions

---

## Pattern: Butterfly Spread Profit Calculation Mechanics

**Description:** Incorrectly calculating maximum profit for butterfly spreads by using the full width between outer strikes instead of the half-width (distance from middle strike to either outer strike), leading to 2x overestimation of profit potential.

**When to Use:** Option strategy analysis involving butterfly spreads (long 1 low strike, short 2 middle strikes, long 1 high strike) with calls or puts.

**Procedure:**
1. Formula: Max Profit = (K_middle - K_low) × Multiplier - Net Premium Paid
2. Identify the three strike prices: K_low < K_middle < K_high
3. Calculate net premium: (Premium_low + Premium_high) - (2 × Premium_middle)
4. Verify strikes are equally spaced: K_middle - K_low = K_high - K_middle
5. Maximum profit = Half-width × Multiplier - Net Debit (or + Net Credit)
6. Maximum loss = Net premium paid (for debit spread) or limited to spread width

**Code Example:**

**Scenario:** Butterfly with strikes 100/105/110, call prices $8.20/$5.10/$2.80, multiplier=100

**Correct Code:**
```python
# Strike prices (equally spaced)
strike_low = 100
strike_middle = 105
strike_high = 110

# Call option premiums
call_low = 8.20
call_middle = 5.10
call_high = 2.80

# Contract multiplier
multiplier = 100

# Net premium calculation (buy low, sell 2 middle, buy high)
premium_paid = (call_low + call_high) * multiplier
premium_received = 2 * call_middle * multiplier
net_debit = premium_paid - premium_received

# Maximum profit occurs at middle strike
# Use HALF-width (middle - low), NOT full width (high - low)
half_width = strike_middle - strike_low
max_profit_gross = half_width * multiplier

# Maximum profit = gross profit - net debit paid
max_profit = max_profit_gross - net_debit

max_profit
```

**Common Bugs to Avoid:**
- Using full width `(strike_high - strike_low)` instead of half-width
- Forgetting to multiply by contract multiplier
- Sign errors: treating net credit as net debit or vice versa
- Not verifying equal spacing of strikes before applying formula

---

## Pattern: CDS Spread Output Format and Unit Conversion

**Description:** Confusion about whether to express CDS spreads as decimal fractions (0.0206), percentages (2.06%), or basis points (206 bps), leading to answers that are off by factors of 100 or 10,000. The question context and expected answer format must be carefully analyzed to determine the appropriate output unit.

**When to Use:** Credit default swap pricing, spread calculations, or any question asking for "spread" or "rate" where output format is ambiguous.

**When NOT to Use:** 
- When the question explicitly provides example answers in a specific format (e.g., multiple choice options showing decimals like 0.0206)
- When the question asks "What is the spread?" without additional context clues like "in basis points" or "as a percentage"
- Default to decimal format (0.0206) unless there is EXPLICIT instruction to convert

**Procedure:**
1. Formula: Spread = PV(Expected Payoff) / [PV(Premium Payments) + PV(Accrual Payments)]
2. Perform calculation in decimal form (e.g., 0.0206)
3. **CRITICAL:** Check answer choices or expected format BEFORE converting
4. If answer choices show decimals (0.02xx), return decimal
5. If answer choices show whole numbers (200-300 range), convert to basis points
6. If question explicitly states "in basis points" or "bps", multiply by 10,000
7. If question explicitly states "as a percentage" or "%", multiply by 100
8. **DEFAULT:** When ambiguous, return decimal form (standard for rates)
9. Verify magnitude is reasonable: 0.001 to 0.10 for investment-grade CDS (10-1000 bps)

**Common Mistakes to Avoid:**
- Automatically converting to basis points without checking question requirements or answer format
- Converting to basis points when the ground truth or answer choices clearly expect decimal format
- Mixing units in intermediate calculations (e.g., adding percentages to decimals)
- Reporting 206.33 when answer should be 0.0206 (factor of 10,000 error)
- Not including a sanity check (typical CDS spreads: 10-500 bps for most credits)

**Example (sanitized):**
> **Scenario:** Calculate CDS spread where PV(protection) = 0.0315, PV(premium) = 1.4200, PV(accrual) = 0.1050. Question asks "What is the credit default swap spread?" with no unit specified.
> **Wrong approach:** Automatically multiply by 10,000 to get 206.56 basis points
> **Correct approach:** Calculate spread = 0.0315 / (1.4200 + 0.1050) = 0.0207, return as decimal 0.0207 (default format when unspecified)

---
## Pattern: Bond Accrued Interest Day-Count Precision

**Description:** Errors in calculating accrued interest for bonds due to incorrect identification of the reference coupon period, wrong day-count conventions, or misidentifying which coupon payment is the "last" vs "next" relative to the current date.

**When to Use:** Bond futures pricing, forward bond pricing, or any calculation requiring accrued interest computation for semi-annual or annual coupon bonds.

**Procedure:**
1. Formula: Accrued Interest = (Coupon Payment) × (Days Since Last Coupon / Days in Coupon Period)
2. Identify the last coupon payment date BEFORE current date
3. Identify the next coupon payment date AFTER current date
4. Calculate days between last coupon and current date
5. Calculate total days in the coupon period (last to next)
6. Use appropriate day-count convention (30/360, Actual/Actual, Actual/360)
7. Verify: Accrued interest should be between 0 and full coupon payment

**Code Example:**

**Scenario:** Bond with 6% semi-annual coupon (payments June 1, Dec 1). Current date: August 15. Calculate accrued interest per $100 face value.

**Correct Code:**
```python
from datetime import datetime

# Bond parameters
annual_coupon_rate = 0.06
face_value = 100
coupon_frequency = 2  # semi-annual

# Dates
last_coupon_date = datetime(2022, 6, 1)
current_date = datetime(2022, 8, 15)
next_coupon_date = datetime(2022, 12, 1)

# Semi-annual coupon payment
coupon_payment = (annual_coupon_rate / coupon_frequency) * face_value

# Days calculation (Actual/Actual convention)
days_since_last_coupon = (current_date - last_coupon_date).days
days_in_period = (next_coupon_date - last_coupon_date).days

# Accrued interest
accrued_interest = coupon_payment * (days_since_last_coupon / days_in_period)

# Verification: should be between 0 and coupon_payment
assert 0 <= accrued_interest <= coupon_payment, "Accrued interest out of valid range"

round(accrued_interest, 2)
```

**Common Bugs to Avoid:**
- Counting days from the wrong reference coupon date (e.g., using future coupon as reference)
- Mixing day-count conventions (using 30/360 when Actual/Actual is required)
- Hardcoding days without accounting for leap years or actual calendar days
- Forgetting that current date might be AFTER a coupon payment (need to identify correct period)
- Using 182.5 days for all semi-annual periods instead of actual days

---

## Pattern: Futures Pricing with Carry Costs and Accrued Interest

**Description:** Errors in bond futures pricing by incorrectly handling the relationship between cash bond price, accrued interest at current date, accrued interest at delivery, and the conversion factor in the forward pricing formula.

**When to Use:** Treasury bond futures pricing, cheapest-to-deliver calculations, or quoted futures price calculations involving conversion factors.

**Procedure:**
1. Formula: Futures Price = [(Cash Price + Accrued_now) × e^(r×t) - Accrued_delivery - Coupon_PV] / Conversion Factor
2. Calculate accrued interest at current date
3. Calculate accrued interest at delivery date
4. Account for any coupon payments between current date and delivery (subtract PV)
5. Apply cost-of-carry formula with continuous compounding
6. Divide by conversion factor to get quoted futures price
7. Verify: Futures price should be close to cash price adjusted for carry

**Code Example:**

**Scenario:** Bond futures: cash price=$125, conversion factor=1.15, rate=4%, time to delivery=0.6 years, accrued now=$1.20, accrued at delivery=$2.80, no coupons before delivery

**Correct Code:**
```python
import math

# Given values
cash_price = 125.00
conversion_factor = 1.15
risk_free_rate = 0.04
time_to_delivery = 0.6

# Accrued interest
accrued_interest_now = 1.20
accrued_interest_delivery = 2.80

# No coupon payments between now and delivery
coupon_pv = 0

# Forward price calculation (dirty price basis)
dirty_price_now = cash_price + accrued_interest_now
forward_dirty_price = dirty_price_now * math.exp(risk_free_rate * time_to_delivery)

# Subtract accrued interest at delivery to get forward clean price
forward_clean_price = forward_dirty_price - accrued_interest_delivery - coupon_pv

# Quoted futures price = forward clean price / conversion factor
quoted_futures_price = forward_clean_price / conversion_factor

# Verification: should be positive and reasonable relative to cash price
assert quoted_futures_price > 0, "Futures price must be positive"

round(quoted_futures_price, 2)
```

**Common Bugs to Avoid:**
- Adding accrued interest at delivery instead of subtracting it
- Forgetting to include accrued interest in the initial dirty price
- Applying conversion factor before calculating forward price
- Not accounting for coupon payments received during the holding period
- Using simple interest instead of continuous compounding for carry costs
- Confusing clean price vs dirty price at different calculation stages

---

## Pattern: Survival Probability Aggregation from Unconditional Default Probabilities

**Description:** Incorrectly computing survival probabilities by failing to properly aggregate unconditional default probabilities over time, leading to errors in CDS premium leg valuation.

**When to Use:** CDS pricing, credit risk modeling, or any calculation requiring survival probabilities derived from period-by-period default probabilities.

**Procedure:**
1. Formula: Survival(t) = 1 - Σ(Unconditional Default Prob up to t)
2. Ensure default probabilities are unconditional (not conditional on survival)
3. For each payment date, sum ALL unconditional default probabilities up to that date
4. Survival probability = 1 - cumulative unconditional default probability
5. Verify: Survival probabilities should be monotonically decreasing over time
6. Check: Survival(0) = 1.0, and all survival probs between 0 and 1

**Code Example:**

**Scenario:** Unconditional default probs: 0.8% at 0.5yr, 1.2% at 1.5yr, 1.5% at 2.5yr. Calculate survival probabilities at payment dates 1yr, 2yr, 3yr.

**Correct Code:**
```python
# Unconditional default probabilities (time, probability)
default_events = [
    (0.5, 0.008),
    (1.5, 0.012),
    (2.5, 0.015)
]

# Payment dates where we need survival probabilities
payment_dates = [1.0, 2.0, 3.0]

# Calculate survival probability at each payment date
survival_probs = []

for payment_date in payment_dates:
    # Sum all unconditional default probs up to this payment date
    cumulative_default = sum(
        prob for time, prob in default_events if time <= payment_date
    )
    
    # Survival = 1 - cumulative default
    survival_prob = 1.0 - cumulative_default
    survival_probs.append(survival_prob)
    
# Verification: survival probs should decrease over time
for i in range(1, len(survival_probs)):
    assert survival_probs[i] <= survival_probs[i-1], "Survival probs must decrease"

survival_probs
```

**Common Bugs to Avoid:**
- Treating unconditional probabilities as conditional (multiplying instead of summing)
- Using only the most recent default probability instead of cumulative sum
- Forgetting to filter default events that occur after the payment date
- Not verifying monotonicity of survival probabilities
- Confusing hazard rates with unconditional default probabilities

---

## Pattern: Semi-Annual Payment Adjustment in Spread Calculations

**Description:** Failing to adjust annual spread rates for payment frequency when calculating present values of premium payments in CDS or bond contexts, leading to 2x errors in payment leg valuation. This error manifests in two ways: (1) using full annual spread for each semi-annual payment instead of dividing by frequency, and (2) failing to account for payment frequency when solving for the spread itself in the CDS pricing equation. **CRITICAL:** When solving for spread from cash flows, the frequency adjustment applies ONLY to the premium leg coefficient, NOT to accrual payments, which are already time-weighted by their nature.

**When to Use:** CDS pricing with semi-annual premiums, bond yield calculations, or any derivatives with non-annual payment frequencies where you need to either calculate payments from a given spread OR solve for the spread from given cash flows.

**When NOT to Use:**
- When accrual payments require time-weighted calculations based on actual default timing within the payment period
- When the problem provides explicit accrual payment formulas that differ from the standard approach
- **When solving for CDS spread where accrual payments are already calculated as time-weighted amounts (e.g., default_prob × 0.5 × spread) — in this case, accrual is ALREADY adjusted and should NOT have frequency applied again**
- When dealing with annual payment CDS where payment frequency = 1

**Procedure:**
1. **For calculating payments from spread:** Payment = (Annual Spread × Notional) / Payment Frequency
2. **For solving for spread from cash flows (CRITICAL DISTINCTION):**
   - If accrual payments are calculated as: `default_prob × (time_fraction) × spread × discount`
     - Then: Spread = [PV(Protection)] / [PV(Premium coefficient) + PV(Accrual coefficient)]
     - The accrual coefficient ALREADY includes time-weighting, so NO frequency adjustment needed
   - If accrual payments are calculated per full payment period:
     - Then: Spread = (Payment Frequency) × [PV(Protection) / (PV(Premium) + PV(Accrual))]
3. Identify payment frequency (annual=1, semi-annual=2, quarterly=4)
4. When calculating premium leg PV: Each payment = (s/frequency) × notional × survival × discount
5. **For accrual payments:** Verify if the accrual formula already includes time-weighting (e.g., 0.5 for mid-year default)
   - If YES: Accrual = default_prob × time_fraction × s × discount (NO additional frequency adjustment)
   - If NO: Accrual = (s/frequency) × default_prob × discount
6. Verify: Semi-annual payments should be half the annual spread amount; solved spread should reflect annual rate

**Common Mistakes to Avoid:**
- Using full annual spread for each semi-annual payment (2x error in payment amount)
- **Applying frequency adjustment to accrual payments that are already time-weighted (e.g., multiplying by 2 when accrual already uses 0.5 factor)**
- **Double-counting frequency: If accrual = default_prob × 0.5 × s, this is ALREADY the correct semi-annual accrual — do NOT multiply by 2 when solving for s**
- Not recognizing that "annual spread" means the rate must be divided by frequency for each payment
- Mixing annual and semi-annual conventions in same calculation
- For binary CDS specifically: forgetting that both the payoff structure (full notional vs (1-R)×notional) AND payment frequency affect the calculation

**Example (sanitized):**

> **Scenario 1 - Annual payments with mid-year default:** CDS with annual payments, notional $1M, 5-year term. Default can occur at mid-year (0.5, 1.5, 2.5, etc.). Calculate spread where PV(protection) = $50,000, PV(premium coefficient) = 4.0 (sum of survival × discount), PV(accrual coefficient) = 0.04 (sum of default_prob × 0.5 × discount).
> **Wrong approach:** Spread = 2 × [$50,000 / (4.0 + 0.04)] = 2 × 0.01238 = 0.02476 (incorrectly applying frequency=2 for annual payments)
> **Correct approach:** Payment frequency = 1 (annual). Accrual coefficient already includes 0.5 time-weighting for mid-year defaults. Spread = $50,000 / (4.0 + 0.04) = 0.01238 or 123.8 bps annually. No frequency adjustment needed because payments are annual and accrual is already time-weighted.

> **Scenario 2 - Semi-annual payments with quarterly default:** CDS with semi-annual payments, notional $1M. PV(protection) = $30,000. Premium leg: sum of (survival × discount) = 3.5. Accrual leg: calculated per full semi-annual period (not time-weighted), sum = 0.08. Solve for spread.
> **Wrong approach:** Spread = $30,000 / (3.5 + 0.08) = 0.00838 (forgetting frequency adjustment)
> **Correct approach:** Payment frequency = 2. Accrual is calculated per full period (not time-weighted). Spread = 2 × [$30,000 / (3.5 + 0.08)] = 2 × 0.00838 = 0.01676 or 167.6 bps annually.

---
## Pattern: Interest Rate Collar Application to Floating Rate Loans

**Description:** Incorrectly applying interest rate collar floors and caps by raising the base rate when it falls below the floor, rather than understanding that collars protect the lender (not the borrower) from rate movements. When the floating rate falls below the collar floor, the borrower still pays based on the actual floating rate plus spread, because the collar's floor protects the lender's minimum return.

**When to Use:** Floating rate loan analysis with interest rate collars, cap and floor option strategies, or any scenario involving borrower protection through derivative overlays.

**Procedure:**
1. Identify the floating rate (e.g., LIBOR) for the payment period
2. Identify the collar cap and floor rates
3. Identify the loan spread over the floating rate
4. **CRITICAL LOGIC:** Determine who benefits from collar activation:
   - If floating rate > cap: Borrower pays capped rate + spread (borrower protected from high rates)
   - If floating rate < floor: Borrower pays actual floating rate + spread (lender protected from low rates)
   - If floor ≤ floating rate ≤ cap: Borrower pays actual floating rate + spread
5. Calculate effective rate = min(cap, max(floor, floating_rate)) + spread ONLY if collar protects borrower
6. For zero-cost collars on borrower's loan: Borrower benefits from cap, lender benefits from floor
7. Calculate interest = Principal × Effective Rate × (Days / Day Count Convention)

**Common Mistakes to Avoid:**
- Applying the floor to increase the borrower's rate when floating rate is below floor (incorrect - this would harm the borrower)
- Confusing who is protected by each component (cap protects borrower, floor protects lender)
- Assuming both cap and floor protect the borrower
- Not considering that "zero-cost" means the borrower gives up downside (floor) to get upside protection (cap)
- Mechanically applying max(floor, rate) without understanding the economic purpose

**Example (sanitized):**
> **Scenario:** Company borrows at LIBOR + 75 bps with zero-cost collar (cap 5.00%, floor 2.50%). Current LIBOR is 2.00%. Calculate interest rate paid.
> **Wrong approach:** Apply floor: max(2.50%, 2.00%) = 2.50%, then add spread: 2.50% + 0.75% = 3.25% effective rate
> **Correct approach:** LIBOR (2.00%) is below floor (2.50%), but floor protects lender, not borrower. Borrower pays actual LIBOR + spread: 2.00% + 0.75% = 2.75% effective rate. The collar's floor means the borrower cannot benefit from rates below 2.50% (they would pay 2.50% + 0.75% = 3.25% if LIBOR were even lower), but at 2.00% LIBOR, they pay the actual rate.

**Note:** If LIBOR were 1.50% (below floor), then the floor activates and borrower pays 2.50% + 0.75% = 3.25%. The floor sets a minimum on the floating rate component for the borrower's cost.

## Pattern: Conversion Factor Application in Futures Hedging

**Description:** Incorrectly applying conversion factors when calculating the number of futures contracts needed for hedging, particularly in bond futures where the cheapest-to-deliver bond may have a conversion factor different from 1.0. The conversion factor adjusts for differences between the deliverable bond and the standard futures contract specification. When hedging with futures, the effective BPV per contract must account for this conversion factor.

**When to Use:** Bond futures hedging calculations, immunization strategies using Treasury futures, or any scenario requiring calculation of the number of futures contracts to hedge interest rate risk where a conversion factor is provided.

**Procedure:**
1. Formula: Number of Contracts = Net BPV to Hedge / (BPV per Contract × Conversion Factor)
2. Identify the net BPV exposure that needs to be hedged (typically BPV_assets - BPV_liabilities)
3. Identify the BPV per futures contract (usually given per $100,000 par value)
4. Identify the conversion factor for the cheapest-to-deliver bond
5. Calculate effective BPV per contract = BPV per contract × Conversion Factor
6. Number of contracts = Net BPV exposure / Effective BPV per contract
7. Round to nearest whole number (contracts must be whole units)
8. Verify: The hedge should approximately match the net BPV exposure when multiplied out

**Code Example:**

**Scenario:** Portfolio has asset BPV of $48,000 and liability BPV of $22,000. Five-year T-note futures have BPV of $44.80 per $100,000 par and conversion factor of 0.80. Calculate contracts needed to immunize.

**Correct Code:**
```python
# Given values
bpv_assets = 48_000
bpv_liabilities = 22_000
bpv_per_contract = 44.80  # per $100,000 par value
conversion_factor = 0.80

# Step 1: Calculate net BPV exposure to hedge
net_bpv_exposure = bpv_assets - bpv_liabilities

# Step 2: Calculate effective BPV per contract
# The conversion factor adjusts the futures contract's sensitivity
effective_bpv_per_contract = bpv_per_contract * conversion_factor

# Step 3: Calculate number of contracts needed
num_contracts = net_bpv_exposure / effective_bpv_per_contract

# Step 4: Round to nearest whole number
num_contracts_rounded = round(num_contracts)

# Verification: Check that hedge approximately matches exposure
hedge_bpv = num_contracts_rounded * effective_bpv_per_contract
assert abs(hedge_bpv - net_bpv_exposure) / net_bpv_exposure < 0.05, "Hedge mismatch > 5%"

num_contracts_rounded
```

**Common Bugs to Avoid:**
- Dividing by conversion factor instead of multiplying (inverts the adjustment)
- Ignoring the conversion factor entirely (assumes CF = 1.0)
- Applying conversion factor to the wrong component (e.g., to net BPV instead of BPV per contract)
- Using the conversion factor as a price adjustment rather than a sensitivity adjustment
- Not verifying that the final hedge approximately matches the target exposure

**Example (sanitized):**
> **Scenario:** Need to hedge $26,000 net BPV exposure. Futures contract has BPV of $50 per contract with conversion factor of 0.85. How many contracts?
> **Wrong approach:** Contracts = $26,000 / ($50 / 0.85) = $26,000 / $58.82 = 442 contracts (dividing by CF instead of multiplying)
> **Correct approach:** Effective BPV = $50 × 0.85 = $42.50 per contract. Contracts = $26,000 / $42.50 = 612 contracts. The conversion factor reduces the effective sensitivity of each contract, so more contracts are needed.