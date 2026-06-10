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

**Description:** Confusion about whether to express CDS spreads as decimal fractions (0.0206), percentages (2.06%), or basis points (206 bps), leading to answers that are off by factors of 100 or 10,000.

**When to Use:** Credit default swap pricing, spread calculations, or any question asking for "spread" or "rate" where output format is ambiguous.

**Procedure:**
1. Formula: Spread = PV(Expected Payoff) / [PV(Premium Payments) + PV(Accrual Payments)]
2. Perform calculation in decimal form (e.g., 0.0206)
3. Check question context for expected format: "basis points," "percent," or raw decimal
4. Apply conversion: decimal × 100 = percent; decimal × 10,000 = basis points
5. If unclear, provide decimal form (standard for rates) and verify magnitude is reasonable (typically 0.001 to 0.10 for investment-grade CDS)

**Code Example:**

**Scenario:** CDS calculation yields spread of 0.0315 in decimal form; question asks for "the spread"

**Correct Code:**
```python
import numpy as np

# Assume calculations yield these present values
pv_expected_payoff = 0.0428
pv_premium_payments = 1.2850
pv_accrual_payments = 0.0720

# Calculate spread as decimal
spread_decimal = pv_expected_payoff / (pv_premium_payments + pv_accrual_payments)

# Determine output format based on question requirements
# Default: return as decimal (per annum rate)
spread_output = spread_decimal

# If question specifies "basis points":
# spread_output = spread_decimal * 10000

# If question specifies "percentage":
# spread_output = spread_decimal * 100

# Return in appropriate format (here: decimal)
round(spread_output, 4)
```

**Common Bugs to Avoid:**
- Automatically converting to basis points without checking question requirements
- Mixing units in intermediate calculations (e.g., adding percentages to decimals)
- Reporting 206.33 when answer should be 0.0206 (factor of 10,000 error)
- Not including a sanity check (typical CDS spreads: 10-500 bps for most credits)

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

**Description:** Failing to adjust annual spread rates for payment frequency when calculating present values of premium payments in CDS or bond contexts, leading to 2x errors in payment leg valuation.

**When to Use:** CDS pricing with semi-annual premiums, bond yield calculations, or any derivatives with non-annual payment frequencies.

**Procedure:**
1. Formula: Payment = (Annual Spread × Notional) / Payment Frequency
2. Identify payment frequency (annual=1, semi-annual=2, quarterly=4)
3. Divide annual spread by frequency to get per-period payment
4. Multiply by survival probability and discount factor for each period
5. Sum across all payment dates for total PV
6. Verify: Semi-annual payments should be half the annual spread amount

**Code Example:**

**Scenario:** CDS with annual spread s, semi-annual payments at 0.5yr and 1.0yr, survival probs 0.98 and 0.95, discount factors 0.975 and 0.951

**Correct Code:**
```python
# CDS parameters (spread is per annum)
# We're calculating PV as a function of spread s
payment_frequency = 2  # semi-annual
notional = 1.0  # normalized

# Payment dates and probabilities
payment_data = [
    {'time': 0.5, 'survival': 0.98, 'discount': 0.975},
    {'time': 1.0, 'survival': 0.95, 'discount': 0.951}
]

# Calculate PV of premium payments per unit spread
pv_per_unit_spread = 0

for payment in payment_data:
    # Semi-annual payment = (s * notional) / 2
    # PV = payment * survival_prob * discount_factor
    # Since payment = s/2, we calculate coefficient of s
    payment_coefficient = notional / payment_frequency
    pv_contribution = payment_coefficient * payment['survival'] * payment['discount']
    pv_per_unit_spread += pv_contribution

# This gives us the PV coefficient: PV = pv_per_unit_spread * s
# For s = 0.05 (5% annual spread):
annual_spread = 0.05
pv_premium_payments = pv_per_unit_spread * annual_spread

round(pv_per_unit_spread, 4)
```

**Common Bugs to Avoid:**
- Using full annual spread for each semi-annual payment (2x error)
- Forgetting to divide by payment frequency
- Mixing annual and semi-annual conventions in same calculation
- Not adjusting accrual payments for payment frequency
- Assuming all derivatives use annual payments without checking

<budget_used>
Tokens used: 7133
</budget_used>