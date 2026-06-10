# SKILL PATTERNS FOR CORPORATE FINANCE CODE EXECUTION ERRORS

## Pattern: IRR Calculation with Multiple Sign Changes

**Description:** Computing IRR for non-conventional cash flows (multiple sign changes) requires robust root-finding methods that can detect and return multiple IRRs when they exist, rather than failing silently or returning only one solution.

**When to Use:** Questions asking for IRR when cash flows alternate between positive and negative values, or when asked "how many IRRs are there?"

**Procedure:**
1. Formula: NPV = Σ(CF_t / (1+IRR)^t) = 0, solve for IRR
2. Import numpy_financial or scipy.optimize (numpy.irr is deprecated)
3. Ensure initial investment is negative, subsequent flows have correct signs
4. For multiple IRRs: use numpy.roots on polynomial coefficients or test multiple initial guesses
5. Return IRR as decimal (convert to percentage if needed)

**Code Example:**

**Scenario:** Project with cash flows: Year 0: -$50,000, Year 1: $132,000, Year 2: -$66,000
**Correct Code:**
```python
import numpy as np
import numpy_financial as npf

# Cash flows with proper sign convention
cash_flows = [-50000, 132000, -66000]

# Method 1: Using numpy_financial (returns one IRR)
try:
    irr_single = npf.irr(cash_flows)
except:
    irr_single = None

# Method 2: Finding all IRRs using polynomial roots
# NPV equation: -50000 + 132000/(1+r) - 66000/(1+r)^2 = 0
# Multiply by (1+r)^2: -50000(1+r)^2 + 132000(1+r) - 66000 = 0
coefficients = [-50000, 132000 - 2*50000, -50000 - 66000]
# Correct form: [-50000, 32000, -116000]
coefficients_correct = [-66000, 132000, -50000]  # ascending powers
roots = np.roots(coefficients_correct[::-1])  # descending powers for np.roots

# Filter for real, positive roots
irrs = [r.real - 1 for r in roots if abs(r.imag) < 1e-10 and r.real > 0]

# Result: number of IRRs and their values
num_irrs = len(irrs)
irrs  # Returns list of IRR values as decimals
```

**Common Bugs to Avoid:**
- Using deprecated `numpy.irr()` instead of `numpy_financial.irr()`
- Missing library imports causing NameError
- Incorrect sign convention (initial investment must be negative)
- Not checking for multiple roots when cash flows change sign more than once
- Returning None instead of handling calculation errors gracefully

---

## Pattern: Multi-Year Capital Budgeting NPV with Dependencies

**Description:** Complex NPV calculations requiring sequential year-by-year computation of operating cash flows, working capital changes, MACRS depreciation, and terminal values with proper variable scoping and data structures.

**When to Use:** Questions involving project NPV with working capital requirements, MACRS depreciation schedules, salvage values, and multi-year projections.

**Procedure:**
1. Formula: NPV = Σ(CF_t / (1+r)^t) where CF_t includes OCF, NWC changes, and terminal flows
2. Initialize arrays/lists for each component (revenue, costs, depreciation, NWC, cash flows)
3. Compute year-by-year: revenue, operating costs, EBIT, taxes, OCF
4. Calculate NWC changes (current year NWC - previous year NWC)
5. Apply MACRS depreciation schedule (lookup table)
6. Compute terminal cash flow (salvage value + tax on salvage + NWC recovery)
7. Discount all cash flows and sum

**Code Example:**

**Scenario:** Equipment cost $100,000, 3-year MACRS, units: [5000, 6000, 5500], price $50/unit, variable cost $30/unit, fixed costs $25,000/year, NWC = 20% of next year's sales increase, salvage 25% of cost, tax rate 30%, discount rate 12%
**Correct Code:**
```python
import numpy as np

# Inputs
equipment_cost = 100000
units = [5000, 6000, 5500]
price = 50
variable_cost = 30
fixed_costs = 25000
nwc_percent = 0.20
salvage_percent = 0.25
tax_rate = 0.30
discount_rate = 0.12
macrs_3yr = [0.3333, 0.4445, 0.1481, 0.0741]  # 3-year MACRS

# Initialize
n_years = len(units)
revenues = [u * price for u in units]
var_costs = [u * variable_cost for u in units]
depreciation = [equipment_cost * macrs_3yr[i] for i in range(n_years)]

# Working capital calculation
sales_changes = [revenues[0]] + [revenues[i] - revenues[i-1] for i in range(1, n_years)]
nwc = [0] * (n_years + 1)
nwc[0] = revenues[0] * nwc_percent  # Initial NWC
for i in range(1, n_years):
    if i < n_years:
        nwc[i] = nwc[i-1] + sales_changes[i] * nwc_percent if i < n_years - 1 else nwc[i-1]
nwc_changes = [nwc[i] - nwc[i-1] for i in range(1, n_years + 1)]

# Operating cash flows
ocf = []
for i in range(n_years):
    ebit = revenues[i] - var_costs[i] - fixed_costs - depreciation[i]
    tax = ebit * tax_rate
    ocf_year = ebit - tax + depreciation[i]  # Add back depreciation
    ocf.append(ocf_year)

# Terminal cash flow (year 3)
salvage_value = equipment_cost * salvage_percent
book_value = equipment_cost - sum(depreciation)
tax_on_salvage = (salvage_value - book_value) * tax_rate
terminal_cf = salvage_value - tax_on_salvage + nwc[n_years - 1]  # Recover NWC

# Total cash flows
cash_flows = [-equipment_cost - nwc[0]]  # Year 0
for i in range(n_years):
    if i < n_years - 1:
        cash_flows.append(ocf[i] - nwc_changes[i])
    else:
        cash_flows.append(ocf[i] + terminal_cf)

# NPV calculation
npv = sum(cf / (1 + discount_rate)**t for t, cf in enumerate(cash_flows))
npv
```

**Common Bugs to Avoid:**
- Off-by-one errors in year indexing (mixing 0-indexed and 1-indexed)
- Forgetting to add back depreciation to OCF (non-cash expense)
- Incorrect NWC recovery (should add back all NWC in terminal year)
- Not accounting for tax on salvage value (salvage - book value)
- Using print() instead of expression on last line

---

## Pattern: Profitability Index Calculation

**Description:** Profitability Index requires computing PV of future cash inflows divided by initial investment (absolute value), equivalent to 1 + (NPV / Initial Investment), not NPV / Initial Investment.

**When to Use:** Questions explicitly asking for "profitability index" or "PI" given a series of cash flows and discount rate.

**Procedure:**
1. Formula: PI = PV(future inflows) / Initial Investment = 1 + (NPV / |Initial Investment|)
2. Separate initial investment (Year 0, negative) from future cash flows (Years 1+)
3. Calculate PV of future inflows only: Σ(CF_t / (1+r)^t) for t ≥ 1
4. Divide by absolute value of initial investment
5. Verify PI > 1 means positive NPV

**Code Example:**

**Scenario:** Project with Year 0: -$5,000, Year 1: $2,200, Year 2: $2,500, Year 3: $1,800, discount rate 10%
**Correct Code:**
```python
# Cash flows
cash_flows = [-5000, 2200, 2500, 1800]
discount_rate = 0.10

# Separate initial investment and future inflows
initial_investment = abs(cash_flows[0])  # 5000 (positive)
future_inflows = cash_flows[1:]  # [2200, 2500, 1800]

# Calculate PV of future inflows
pv_inflows = sum(cf / (1 + discount_rate)**t for t, cf in enumerate(future_inflows, start=1))

# Profitability Index
pi = pv_inflows / initial_investment

# Alternative method using NPV
npv = sum(cf / (1 + discount_rate)**t for t, cf in enumerate(cash_flows))
pi_alternative = 1 + (npv / initial_investment)

pi  # Should equal pi_alternative
```

**Common Bugs to Avoid:**
- Using NPV / Initial Investment instead of (PV of inflows) / Initial Investment
- Including initial investment in numerator (should only be future inflows)
- Forgetting to take absolute value of initial investment for denominator
- Incorrect time indexing (Year 1 cash flow should be discounted by (1+r)^1, not (1+r)^0)

---

## Pattern: IRR with Standard Cash Flow Sign Convention

**Description:** IRR calculation fails when cash flow signs are incorrect or required libraries are missing; initial investment must be negative, and proper financial libraries must be imported.

**When to Use:** Any question asking for IRR or internal rate of return with a standard investment pattern (initial outflow, subsequent inflows or mixed flows).

**Procedure:**
1. Formula: Find r where NPV = Σ(CF_t / (1+r)^t) = 0
2. Import numpy_financial as npf (or use scipy.optimize)
3. Construct cash flow array with correct signs (outflows negative, inflows positive)
4. Call npf.irr(cash_flows) 
5. Return as decimal or multiply by 100 for percentage

**Code Example:**

**Scenario:** Investment of $8,000 today, receive $3,500 in Year 1, $4,200 in Year 2, $2,800 in Year 3
**Correct Code:**
```python
import numpy_financial as npf

# Cash flows with correct sign convention
cash_flows = [-8000, 3500, 4200, 2800]

# Calculate IRR
irr = npf.irr(cash_flows)

# Convert to percentage
irr_percent = irr * 100

irr  # Returns decimal (e.g., 0.1523 for 15.23%)
```

**Common Bugs to Avoid:**
- Missing `import numpy_financial as npf` causing NameError
- Using deprecated `numpy.irr()` instead of `numpy_financial.irr()`
- Incorrect sign convention (initial investment should be negative)
- Forgetting to convert percentage inputs to decimals
- Using print() instead of returning expression

---

## Pattern: IRR with Reversed Cash Flow Signs (Loan/Payment Pattern)

**Description:** When receiving money upfront and making payments later (loan pattern), the initial cash flow is positive and subsequent flows are negative, opposite of typical investment pattern.

**When to Use:** Questions about loans, offers where you receive money today and pay back later, or any "what is the IRR of this offer" phrasing.

**Procedure:**
1. Formula: NPV = Σ(CF_t / (1+r)^t) = 0, solve for r
2. Identify cash flow direction: initial inflow (positive), subsequent outflows (negative)
3. Import numpy_financial as npf
4. Construct array: [+initial_amount, -payment1, -payment2, ...]
5. Calculate IRR and return as decimal

**Code Example:**

**Scenario:** Receive $12,000 today, pay $5,500 in Year 1, $4,200 in Year 2, $3,800 in Year 3
**Correct Code:**
```python
import numpy_financial as npf

# Cash flows: receive money (positive), then make payments (negative)
cash_flows = [12000, -5500, -4200, -3800]

# Calculate IRR (this is the cost of the loan)
irr = npf.irr(cash_flows)

# Convert to percentage
irr_percent = irr * 100

irr  # Returns decimal (e.g., 0.1456 for 14.56%)
```

**Common Bugs to Avoid:**
- Reversing all signs (making initial receipt negative)
- Forgetting negative signs on payment cash flows
- Missing library import
- Confusing IRR interpretation (this is the interest rate you're paying, not earning)

---

## Pattern: Continuous Compounding EAR to APR Conversion

**Description:** Converting effective annual rate (EAR) to annual percentage rate (APR) under continuous compounding requires the natural logarithm formula, with proper handling of percentage-to-decimal conversion.

**When to Use:** Questions asking for APR given EAR when compounding frequency is "infinite" or "continuous."

**Procedure:**
1. Formula: APR = ln(1 + EAR) when compounding is continuous
2. Import math or numpy for natural logarithm function
3. Convert EAR from percentage to decimal (divide by 100)
4. Apply formula: apr = ln(1 + ear_decimal)
5. Return as decimal or convert to percentage

**Code Example:**

**Scenario:** Given EAR of 14.2% with continuous compounding, find APR
**Correct Code:**
```python
import math

# Given EAR as percentage
ear_percent = 14.2

# Convert to decimal
ear_decimal = ear_percent / 100  # 0.142

# Apply continuous compounding formula
apr_decimal = math.log(1 + ear_decimal)  # ln(1.142)

# Convert to percentage if needed
apr_percent = apr_decimal * 100

apr_decimal  # Returns ~0.1329 (13.29%)
```

**Common Bugs to Avoid:**
- Missing `import math` or `import numpy as np` for log function
- Using log10 instead of natural log (ln)
- Forgetting to convert percentage input to decimal before calculation
- Not adding 1 to EAR before taking logarithm
- Returning nan due to invalid input (negative or missing values)

---

## Pattern: IRR with Blocked Funds and Reinvestment

**Description:** When cash flows are blocked and must be reinvested for a period, adjust each cash flow by shifting it forward in time and applying the reinvestment rate before calculating IRR.

**When to Use:** Questions mentioning "blocked funds," "reinvestment requirement," or mandatory holding periods for foreign investment cash flows.

**Procedure:**
1. Formula: Adjusted CF_t = Original CF_t × (1 + reinvestment_rate), received at t+1
2. Create new cash flow array with shifted timing
3. Each positive cash flow (except initial) moves forward one year and grows by reinvestment rate
4. Initial investment stays at Year 0
5. Calculate IRR on adjusted cash flows

**Code Example:**

**Scenario:** Investment -$600,000 at Year 0, then $180,000, $240,000, $280,000, $150,000 in Years 1-4; all inflows blocked and reinvested at 3% for one year
**Correct Code:**
```python
import numpy_financial as npf

# Original cash flows
original_cf = [-600000, 180000, 240000, 280000, 150000]
reinvestment_rate = 0.03

# Adjust for blocked funds (each inflow delayed 1 year, grows at 3%)
# Year 0: -600000 (unchanged)
# Year 1: 0 (original 180000 is blocked)
# Year 2: 180000 * 1.03 (Year 1 released) + 0 (Year 2 blocked)
# Continue pattern...

adjusted_cf = [original_cf[0]]  # Year 0
adjusted_cf.append(0)  # Year 1 (first inflow blocked)

for i in range(1, len(original_cf)):
    if i < len(original_cf) - 1:
        adjusted_cf.append(original_cf[i] * (1 + reinvestment_rate))
    else:
        # Last year: previous blocked + current blocked
        adjusted_cf.append(original_cf[i] * (1 + reinvestment_rate))

# Simpler approach: shift all inflows forward one period
adjusted_cf_simple = [original_cf[0]] + [0]
for i in range(1, len(original_cf)):
    adjusted_cf_simple.append(original_cf[i] * (1 + reinvestment_rate))

# Calculate IRR on adjusted cash flows
irr = npf.irr(adjusted_cf_simple)
irr
```

**Common Bugs to Avoid:**
- Not shifting cash flow timing (applying reinvestment rate without delay)
- Applying reinvestment to initial investment (should only affect inflows)
- Incorrect array indexing when building adjusted cash flow sequence
- Forgetting to multiply by (1 + rate) for the reinvestment growth

---

## Pattern: External Financing Needed (EFN) Calculation

**Description:** EFN calculation requires projecting assets proportionally to sales growth, computing addition to retained earnings using constant payout ratio, and finding the financing gap.

**When to Use:** Questions asking for "external financing needed," "additional funds needed," or "EFN" given pro forma projections.

**Procedure:**
1. Formula: EFN = (Assets/Sales) × ΔSales - (PM × Projected Sales × Retention Ratio) - ΔDebt
2. Calculate sales growth rate: (New Sales - Old Sales) / Old Sales
3. Project new assets: Old Assets × (1 + growth rate) if assets scale with sales
4. Calculate payout ratio: Dividends / Net Income
5. Project new net income: Old NI × (1 + growth rate)
6. Calculate addition to retained earnings: New NI × (1 - payout ratio)
7. EFN = Increase in Assets - Addition to Retained Earnings

**Code Example:**

**Scenario:** Sales $50,000 → $58,000; Assets $120,000 (proportional); NI $9,000; Dividends $3,000; Debt and Equity not proportional
**Correct Code:**
```python
# Current values
current_sales = 50000
projected_sales = 58000
current_assets = 120000
current_ni = 9000
dividends = 3000

# Calculate growth rate
sales_growth = (projected_sales - current_sales) / current_sales

# Project new assets (proportional to sales)
projected_assets = current_assets * (1 + sales_growth)
increase_in_assets = projected_assets - current_assets

# Calculate payout ratio
payout_ratio = dividends / current_ni
retention_ratio = 1 - payout_ratio

# Project new net income (proportional to sales)
projected_ni = current_ni * (1 + sales_growth)

# Addition to retained earnings
addition_to_re = projected_ni * retention_ratio

# External financing needed (assuming no new debt)
efn = increase_in_assets - addition_to_re

efn
```

**Common Bugs to Avoid:**
- Not recognizing which items are proportional vs. fixed
- Using old net income instead of projected net income
- Forgetting to multiply by retention ratio (1 - payout ratio)
- Incorrect calculation of asset increase (should be new - old)
- Variable naming errors causing undefined references

---

## Pattern: Acquisition Gain with Gordon Growth Model

**Description:** Calculating acquisition NPV requires computing the present value of the target's future dividends using the Gordon Growth Model with the post-acquisition growth rate and required return, then subtracting the total purchase price. Sign convention is critical: PV of future cash flows is positive, purchase cost is negative, and NPV = PV - Cost.

**When to Use:** Questions about merger/acquisition NPV, gain from acquisition, or "what would the NPV be if we offer $X per share" with dividend growth rates and synergies.

**Procedure:**
1. Formula: NPV = PV_target - Purchase_Cost, where PV_target = D₁ / (r - g) using Gordon Growth Model
2. Calculate next year's dividend: D₁ = Current_Dividend × (1 + new_growth_rate)
3. Determine required return (r) from target's current valuation: r = (D₁_old / Current_Price) + old_growth_rate
4. Calculate PV of target with new growth rate: PV = D₁_new / (r - g_new)
5. Calculate total purchase cost: Cost = Offer_per_share × Shares_outstanding
6. Compute NPV: NPV = PV - Cost (positive NPV means value created)

**Code Example:**

**Scenario:** Target company has 500,000 shares, current dividend of $300,000, current stock price $15, and dividends growing at 3%. Acquirer believes they can increase growth to 5% and offers $18 per share. What is the NPV?

**Correct Code:**
```python
import numpy as np

# Target company data
shares_outstanding = 500_000
current_dividend = 300_000
current_price = 15
old_growth_rate = 0.03
new_growth_rate = 0.05
offer_per_share = 18

# Step 1: Calculate dividend per share
dividend_per_share = current_dividend / shares_outstanding

# Step 2: Calculate required return from current valuation
# Current price = D1 / (r - g), so r = (D1 / P) + g
d1_old = dividend_per_share * (1 + old_growth_rate)
required_return = (d1_old / current_price) + old_growth_rate

# Step 3: Calculate PV with new growth rate
d1_new = dividend_per_share * (1 + new_growth_rate)
pv_per_share = d1_new / (required_return - new_growth_rate)
total_pv = pv_per_share * shares_outstanding

# Step 4: Calculate total purchase cost
total_cost = offer_per_share * shares_outstanding

# Step 5: Calculate NPV (PV minus Cost)
npv = total_pv - total_cost

npv
```

**Common Bugs to Avoid:**
- Sign error: subtracting PV from cost (NPV = Cost - PV) instead of (NPV = PV - Cost)
- Using old growth rate instead of new growth rate when calculating PV of synergies
- Forgetting to multiply per-share values by total shares outstanding
- Using current dividend instead of next year's dividend (D₁) in Gordon Growth Model
- Not deriving required return from target's current market valuation
## Pattern: Complex NPV with IRR Calculation on Same Project

**Description:** When asked for IRR after computing NPV on a complex multi-year project, reuse the same cash flow array construction logic but call IRR solver instead of NPV formula.

**When to Use:** Questions asking for IRR on projects with working capital, depreciation, and terminal values (same setup as complex NPV questions).

**Procedure:**
1. Use identical cash flow construction as NPV calculation
2. Build complete cash flow array: [Year 0 outflows, Year 1-n operating CF + adjustments, Terminal CF]
3. Verify cash flow array has correct signs and completeness
4. Import numpy_financial and call npf.irr(cash_flows)
5. Return IRR as decimal

**Code Example:**

**Scenario:** Same project as multi-year NPV example, but calculate IRR instead
**Correct Code:**
```python
import numpy_financial as npf

# [Use same setup as Pattern 2 to build cash_flows array]
equipment_cost = 100000
# ... [all intermediate calculations] ...
# Resulting in cash_flows array

cash_flows = [-equipment_cost - nwc[0]]
for i in range(n_years):
    if i < n_years - 1:
        cash_flows.append(ocf[i] - nwc_changes[i])
    else:
        cash_flows.append(ocf[i] + terminal_cf)

# Calculate IRR instead of NPV
irr = npf.irr(cash_flows)

# Convert to percentage
irr_percent = irr * 100

irr
```

**Common Bugs to Avoid:**
- Inconsistent cash flow construction between NPV and IRR calculations
- Missing terminal cash flow components (salvage, NWC recovery)
- Incorrect initial outflow (should include equipment + initial NWC)
- Runtime errors from incomplete cash flow array
- Not handling IRR calculation failure when no solution exists

## Pattern: IRR Non-Existence Detection for Non-Conventional Cash Flows

**Description:** For non-conventional cash flows with multiple sign changes, IRR may not exist (no real solution to NPV=0). Code must detect this case by catching numerical solver failures or checking Descartes' Rule of Signs, then return a meaningful message rather than crashing.

**When to Use:** Questions asking for IRR when cash flows have unusual patterns (e.g., negative, positive, negative) or when the answer might be "no real IRR exists" or "IRR does not exist."

**Procedure:**
1. Check number of sign changes in cash flow sequence using Descartes' Rule
2. If 0 sign changes: no IRR exists (all same sign)
3. If 1 sign change: unique IRR exists (use standard solver)
4. If 2+ sign changes: multiple or no real IRRs possible (requires robust handling)
5. Attempt IRR calculation with try-except block to catch solver failures
6. If solver fails or returns complex numbers, return "no real IRR" message

**Code Example:**

**Scenario:** A project has cash flows: Year 0: -$15,000, Year 1: +$40,000, Year 2: -$28,000. Find the IRR.

**Correct Code:**
```python
import numpy as np
from numpy_financial import irr

# Cash flows with multiple sign changes
cash_flows = np.array([-15000, 40000, -28000])

# Count sign changes (Descartes' Rule)
sign_changes = 0
for i in range(1, len(cash_flows)):
    if cash_flows[i] * cash_flows[i-1] < 0:
        sign_changes += 1

# Attempt IRR calculation with error handling
try:
    calculated_irr = irr(cash_flows)
    
    # Check if result is real (not NaN or complex)
    if np.isnan(calculated_irr) or not np.isreal(calculated_irr):
        result = "no real IRR"
    else:
        result = float(calculated_irr)
except:
    result = "no real IRR"

# Additional validation: check if NPV equation has real roots
# For this pattern, if sign_changes >= 2, verify solution exists
if sign_changes >= 2 and isinstance(result, str):
    result = "no real IRR"

result
```

**Common Bugs to Avoid:**
- Not catching exceptions when IRR solver fails on non-conventional cash flows
- Returning NaN or error object instead of meaningful "no real IRR" message
- Assuming IRR always exists for any cash flow pattern
- Not checking if returned value is real vs. complex or NaN
- Using simple root-finding without validating that real solution exists
- Printing error messages instead of returning a string result that can be evaluated