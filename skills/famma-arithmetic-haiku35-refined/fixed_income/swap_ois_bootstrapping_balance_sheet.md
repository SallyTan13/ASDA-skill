# Fixed Income — Swap Rate Bootstrapping and Balance Sheet Duration

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

## Pattern 1: LIBOR Forward Rate from Swap Rates with OIS Discounting

**Description:** Calculate LIBOR forward rates by bootstrapping from swap rates using OIS (Overnight Indexed Swap) zero rates for discounting. This reflects the post-crisis framework where swap rates represent fixed payments that equal the present value of floating LIBOR payments, discounted at OIS rates (the risk-free rate).

**When to Use:** 
- Question asks for "LIBOR forward rate" for a specific period
- Given OIS zero rates for multiple maturities
- Given swap rates for corresponding maturities
- May also provide known LIBOR rates for earlier periods

**Procedure:**
1. Calculate OIS discount factors: DF_t = 1 / (1 + z_t)^t where z_t is the OIS zero rate for maturity t
2. Identify known LIBOR rates for earlier periods (if provided)
3. Set up the swap rate equation: Swap_Rate × Σ(DF_i) = Σ(LIBOR_i × DF_i)
4. Solve for the unknown LIBOR forward rate by rearranging the equation
5. Express result as a percentage

**Worked Example:**
**Question:** Given OIS zero rates of 2.0%, 2.2%, and 2.4% for 1, 2, and 3 years respectively, a 3-year swap rate of 2.8%, and known LIBOR rates of 2.5% for year 1 and 2.7% for year 2, what is the LIBOR forward rate for the 2- to 3-year period?

```python
# Step 1: Calculate OIS discount factors
ois_1y = 0.020
ois_2y = 0.022
ois_3y = 0.024

df_1 = 1 / (1 + ois_1y)
df_2 = 1 / ((1 + ois_2y) ** 2)
df_3 = 1 / ((1 + ois_3y) ** 3)

# Step 2: Known LIBOR rates
libor_1 = 0.025
libor_2 = 0.027

# Step 3: Swap rate equation
swap_rate_3y = 0.028

# Step 4: Solve for LIBOR forward rate (year 2-3)
# swap_rate × (df_1 + df_2 + df_3) = libor_1 × df_1 + libor_2 × df_2 + libor_3 × df_3
# Rearrange to solve for libor_3:
sum_df = df_1 + df_2 + df_3
left_side = swap_rate_3y * sum_df
known_payments = libor_1 * df_1 + libor_2 * df_2

libor_3 = (left_side - known_payments) / df_3

# Express as percentage
libor_forward_2_to_3 = libor_3 * 100

libor_forward_2_to_3
```

**Common Bugs to Avoid:**
- ❌ Using formula ((1+z3)^3/(1+z2)^2)^(1/1)-1 directly on OIS rates — this gives OIS forward rate, NOT LIBOR forward rate
- ❌ Forgetting to discount using OIS rates instead of LIBOR rates
- ❌ Not using the swap rate equation to link fixed and floating legs
- ❌ Confusing swap rate with LIBOR rate

**CHECK Steps:**
- If given both OIS rates and swap rates, verify you're using OIS for discounting and swap rate in the equation
- Assert that calculated LIBOR forward rate is reasonable (typically within a few percentage points of swap rate)
- Verify sum of (LIBOR_i × DF_i) equals swap_rate × sum(DF_i) when all LIBOR rates are known

## Pattern 2: Balance Sheet Duration with Asset/Liability Classification

**Description:** Calculate weighted average duration of assets or liabilities from a financial institution's balance sheet. Critical step is correctly classifying balance sheet items before applying duration formulas.

**When to Use:**
- Question asks for "duration of assets" or "duration of liabilities"
- Given a balance sheet with multiple items and their durations
- Need to distinguish between assets and liabilities

**Procedure:**
1. Classify each balance sheet item as Asset, Liability, or Equity
   - **Assets**: Loans (all types), securities, receivables, cash, federal funds sold
   - **Liabilities**: Deposits (all types), borrowings, debt, federal funds purchased, certificates of deposit
   - **Equity**: Common stock, retained earnings, capital
2. Filter items based on what the question asks for (assets OR liabilities)
3. Exclude equity from both asset and liability calculations
4. Calculate weighted average duration: Σ(MV_i × Duration_i) / Σ(MV_i)
5. Express result in years

**Worked Example:**
**Question:** A bank has the following balance sheet items with their market values and durations: Cash $50M (duration 0), Consumer loans $400M (duration 0.8), Mortgage loans $600M (duration 8.5), Demand deposits $300M (duration 0), Time deposits $500M (duration 2.0), Long-term debt $200M (duration 7.5), Equity $50M. What is the duration of the liabilities?

```python
# Step 1 & 2: Identify and classify liabilities only
# Assets: Cash, Consumer loans, Mortgage loans
# Liabilities: Demand deposits, Time deposits, Long-term debt
# Equity: Excluded from calculation

liabilities = [
    {'name': 'Demand deposits', 'mv': 300, 'duration': 0},
    {'name': 'Time deposits', 'mv': 500, 'duration': 2.0},
    {'name': 'Long-term debt', 'mv': 200, 'duration': 7.5}
]

# Step 3: Calculate total market value of liabilities
total_mv = sum(item['mv'] for item in liabilities)

# Step 4: Calculate weighted average duration
weighted_duration_sum = sum(item['mv'] * item['duration'] for item in liabilities)
duration_liabilities = weighted_duration_sum / total_mv

duration_liabilities
```

**Common Bugs to Avoid:**
- ❌ Classifying loans as liabilities (loans are ASSETS - money owed TO the institution)
- ❌ Classifying deposits as assets (deposits are LIABILITIES - money the institution owes)
- ❌ Including equity in asset or liability calculations
- ❌ Confusing "federal funds deposits" (liability) with "federal funds sold" (asset)
- ❌ Mixing assets and liabilities in the same calculation

**CHECK Steps:**
- If item name contains "loan", "receivable", "securities", or "cash" → classify as ASSET
- If item name contains "deposit", "borrowing", "debt", or "payable" → classify as LIABILITY
- If item name contains "equity", "capital", or "retained earnings" → EXCLUDE from calculation
- Verify that total MV of selected items matches expected balance sheet category total
- Assert duration result is between min and max individual durations in the category

---

## SKILL.md Entry

```
SKILL_MD_ENTRY: | `fixed_income/swap_ois_bootstrapping_balance_sheet.md` | Fixed Income | Swap Rate Bootstrapping and Balance Sheet Duration | LIBOR Forward Rate from Swap Rates with OIS Discounting, Balance Sheet Duration with Asset/Liability Classification |
```