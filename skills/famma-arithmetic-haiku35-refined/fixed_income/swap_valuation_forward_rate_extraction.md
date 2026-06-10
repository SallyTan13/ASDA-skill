# Fixed Income — Interest Rate Swap Valuation and Forward Rate Extraction

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

## Pattern 1: Extracting Forward Rates from Spot Rates

**Description:** Calculate implied forward rates from spot rates using the expectations hypothesis. The relationship is: (1 + s_n)^n = (1 + s_m)^m × (1 + f_{m,n})^{n-m}, where f_{m,n} is the forward rate from period m to period n.

**When to Use:** 
- Question asks for "expected future interest rate" under expectations hypothesis
- Given spot rates or zero-coupon bond yields for different maturities
- Need to find the rate for a period starting in the future (e.g., "1-year rate 3 years from now")

**Procedure:**
1. Identify the spot rates: s_m for the earlier maturity and s_n for the later maturity
2. For zero-coupon bonds, YTM equals the spot rate (no conversion needed)
3. Apply the forward rate formula: f_{m,n} = [(1 + s_n)^n / (1 + s_m)^m]^(1/(n-m)) - 1
4. The forward rate f_{m,n} represents the rate from year m to year n

**Worked Example:**
**Question:** Given spot rates: 1-year = 5%, 2-year = 6%, 3-year = 7%, 4-year = 7.5%. What is the expected 1-year interest rate 3 years from now according to the expectations hypothesis?

```python
# Given spot rates (as decimals)
s1 = 0.05
s2 = 0.06
s3 = 0.07
s4 = 0.075

# We need the 1-year forward rate starting in year 3 (i.e., from year 3 to year 4)
# This is f_{3,4}: the rate from period 3 to period 4

# Using the relationship: (1 + s4)^4 = (1 + s3)^3 × (1 + f_{3,4})^1
# Solve for f_{3,4}: f_{3,4} = [(1 + s4)^4 / (1 + s3)^3] - 1

forward_rate_3_to_4 = ((1 + s4)**4 / (1 + s3)**3) - 1

# Convert to percentage
forward_rate_3_to_4_pct = forward_rate_3_to_4 * 100

forward_rate_3_to_4_pct
```

**Common Bugs to Avoid:**
- ❌ Using wrong exponents: calculating ((1+s3)^1/(1+s2)^2)-1 instead of [(1+s4)^4/(1+s3)^3]-1
- ❌ Converting YTM to spot rates for zero-coupon bonds (they're already equal)
- ❌ Confusing the period notation: "1-year rate 3 years from now" means f_{3,4}, not f_{2,3}

**CHECK Steps:**
- Verify that n > m (later maturity > earlier maturity)
- Forward rates should generally be positive for normal yield curves
- If spot curve is upward sloping, forward rates should be higher than spot rates

## Pattern 2: Interest Rate Swap Valuation

**Description:** Calculate the market value of an existing interest rate swap by finding the present value difference between fixed and floating legs. Swaps exchange interest payments only (no principal exchange except in currency swaps).

**When to Use:**
- Question asks for "value of a swap" or "mark-to-market value"
- Given fixed rate, notional principal, and current market rates (spot or forward rates)
- Need to value an existing swap after initiation

**Procedure:**
1. **Bootstrap forward rates if needed:** If given swap rates, extract implied forward LIBOR rates using the swap pricing equation
2. **Calculate discount factors:** Compound forward rates sequentially: DF_n = 1 / [(1 + f_1) × (1 + f_2) × ... × (1 + f_n)]
3. **Value fixed leg:** PV_fixed = Σ [Fixed_Rate × Notional × DF_i] for each period i
4. **Value floating leg:** PV_float = Σ [Forward_LIBOR_i × Notional × DF_i] for each period i
5. **Calculate swap value:** If receiving fixed: Value = PV_fixed - PV_float; If paying fixed: Value = PV_float - PV_fixed

**Worked Example:**
**Question:** What is the value of a 3-year swap where 4% is received and LIBOR is paid on a principal of $100 million? Given: 1-year LIBOR = 3%, 2-year swap rate = 3.5%, 3-year swap rate = 4%. All rates are annually compounded.

```python
# Given information
notional = 100_000_000  # $100 million
fixed_rate = 0.04  # 4% received
libor_1y = 0.03  # 1-year LIBOR

# Given swap rates (for bootstrapping)
swap_2y = 0.035
swap_3y = 0.04

# Step 1: Bootstrap forward LIBOR rates
# For 1-year: we have it directly
f1 = libor_1y

# For 2-year forward (1y1y): use 2-year swap equation
# swap_2y = (f1 × DF1 + f2 × DF2) / (DF1 + DF2)
# where DF1 = 1/(1+f1), DF2 = 1/[(1+f1)(1+f2)]
# Solving: swap_2y × [1/(1+f1) + 1/((1+f1)(1+f2))] = f1/(1+f1) + f2/((1+f1)(1+f2))

df1 = 1 / (1 + f1)
# From swap equation: swap_2y × (DF1 + DF2) = f1 × DF1 + f2 × DF2
# Rearranging: f2 = [(swap_2y × (DF1 + DF2) - f1 × DF1) / DF2] × (1+f1)(1+f2)
# Simpler: (1+f2) = (1+f1) × [1 + swap_2y] / [1 + swap_2y - (swap_2y - f1)/(1 + 1/(1+f1))]
# Direct formula: f2 = [(1+swap_2y)^2 / (1+f1)] - 1

f2 = ((1 + swap_2y)**2 / (1 + f1)) - 1

# For 3-year forward (2y1y): use 3-year swap equation
# Similar bootstrapping: f3 = [(1+swap_3y)^3 / ((1+f1)(1+f2))] - 1

f3 = ((1 + swap_3y)**3 / ((1 + f1) * (1 + f2))) - 1

# Step 2: Calculate discount factors by compounding forward rates
df1 = 1 / (1 + f1)
df2 = 1 / ((1 + f1) * (1 + f2))
df3 = 1 / ((1 + f1) * (1 + f2) * (1 + f3))

# Step 3: Value the fixed leg (receiving 4%)
# Fixed payments: 4% × $100M each year
pv_fixed = fixed_rate * notional * (df1 + df2 + df3)

# Step 4: Value the floating leg (paying LIBOR)
# Floating payments based on forward LIBORs
pv_float = notional * (f1 * df1 + f2 * df2 + f3 * df3)

# Step 5: Calculate swap value (receiving fixed, paying floating)
swap_value = pv_fixed - pv_float

# Express in millions
swap_value_millions = swap_value / 1_000_000

swap_value_millions
```

**Common Bugs to Avoid:**
- ❌ Adding rates instead of compounding: DF should be 1/[(1+f1)×(1+f2)×(1+f3)], NOT 1/(1+f1+f2+f3)
- ❌ Including principal repayment in swap legs (swaps only exchange interest, not principal)
- ❌ Incorrectly bootstrapping forward rates (must use proper swap pricing equation)
- ❌ Confusing which leg is received vs. paid (sign matters!)

**CHECK Steps:**
- Verify discount factors are decreasing: DF1 > DF2 > DF3 (time value of money)
- If swap rate equals fixed rate at initiation, value should be near zero
- If receiving fixed and rates have fallen, swap value should be positive
- Assert that all forward rates are positive for normal market conditions

---

**SKILL.md Entry:**

```
SKILL_MD_ENTRY: | `fixed_income/swap_valuation_forward_rate_extraction.md` | Fixed Income | Interest Rate Swap Valuation and Forward Rate Extraction | Pattern 1: Extracting Forward Rates from Spot Rates, Pattern 2: Interest Rate Swap Valuation |
```