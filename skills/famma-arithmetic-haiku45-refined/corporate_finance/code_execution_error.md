# DETAILED SKILL PATTERNS FOR CORPORATE FINANCE (PoT)

## Pattern: IRR Multiple Root Detection with Polynomial Methods

**Description:** When cash flows change sign multiple times, the NPV polynomial can have multiple real IRR solutions. Grid-based sign-change detection may miss closely-spaced roots due to insufficient resolution or overly aggressive duplicate filtering. This pattern is specifically for counting IRRs, not for general IRR calculation.

**When to Use:** Questions explicitly asking "how many IRRs" or "find all IRRs" with non-conventional cash flow patterns (multiple sign changes), especially when a search range is specified.

**When NOT to Use:** 
- Questions asking for "the IRR" (singular) or "compute the IRR" without asking for count
- Questions asking for IRR and other metrics (NPV, PI, etc.) together
- Conventional cash flow patterns (single sign change)

**Procedure:**
1. Formula: NPV(r) = Σ(CF_t / (1+r)^t) = 0; solve for all r in specified range
2. Use fine grid resolution (≥10,000 points per 50% range) to detect all sign changes
3. Apply bisection/Newton method to refine each detected root
4. Filter duplicates with strict tolerance (≤1e-5) to avoid merging distinct roots
5. **Verify each IRR with adaptive tolerance that accounts for both cash flow magnitude AND numerical precision**
6. Return count as integer expression

**Worked Example:**

**Question:** Cash flows: Year 0: -$5,000, Year 1: $15,000, Year 2: $18,000, Year 3: -$20,000. Find number of IRRs between 10% and 80%.

```python
import numpy as np

# Define cash flows
cash_flows = [-5000, 15000, 18000, -20000]

# NPV function
def npv(rate, cfs):
    return sum(cf / (1 + rate)**t for t, cf in enumerate(cfs))

# Fine grid search (20,000 points for 70% range = 0.0035% spacing)
search_rates = np.linspace(0.10, 0.80, 20000)
npv_values = [npv(r, cash_flows) for r in search_rates]

# Detect sign changes
irr_candidates = []
for i in range(len(npv_values) - 1):
    if npv_values[i] * npv_values[i + 1] < 0:
        # Bisection refinement
        low, high = search_rates[i], search_rates[i + 1]
        while high - low > 1e-8:
            mid = (low + high) / 2
            if npv(mid, cash_flows) * npv(low, cash_flows) < 0:
                high = mid
            else:
                low = mid
        irr_candidates.append((low + high) / 2)

# Remove duplicates with strict threshold
unique_irrs = []
for irr in irr_candidates:
    if all(abs(irr - existing) > 1e-5 for existing in unique_irrs):
        unique_irrs.append(irr)

# Verify with adaptive tolerance for large cash flows
max_cf = max(abs(cf) for cf in cash_flows)
# Use relative tolerance: 0.01% of max cash flow, with floor at 1e-6
tolerance = max(1e-6, max_cf * 1e-4)

verified_irrs = []
for irr in unique_irrs:
    if abs(npv(irr, cash_flows)) < tolerance:
        verified_irrs.append(irr)

# Return count
len(verified_irrs)
```

**Common Bugs to Avoid:**
- Using too coarse grid (e.g., 1000 points) that skips over closely-spaced roots
- Duplicate threshold too large (e.g., 0.001) merging distinct IRRs
- **Tolerance too strict for large cash flows: use `max(1e-6, max_cf * 1e-4)` not `max_cf * 1e-9`**
- **For cash flows in millions, NPV residuals may be in thousands due to floating-point precision**
- Returning list instead of integer count
- Applying this pattern when question asks for single IRR value

**CHECK Steps:**
- If question asks "how many IRRs", use this pattern and return integer count
- If question asks "compute the IRR" or "what is the IRR", use numpy_financial.irr() instead
- **Adaptive tolerance: `tolerance = max(1e-6, max(abs(cf) for cf in cash_flows) * 1e-4)`**
- **For large cash flows (>$1M), expect NPV residuals up to 0.01% of max cash flow**

---
## Pattern: Cash Flow to Creditors - Long-term Debt Only

**Description:** Cash flow to creditors measures payments to long-term debt holders (interest paid minus net new long-term borrowing), excluding short-term operating liabilities like notes payable or accounts payable.

**When to Use:** Questions asking for "cash flow to creditors" or "cash flow to bondholders" given balance sheets and income statements.

**Procedure:**
1. Formula: Cash Flow to Creditors = Interest Paid - Net New Long-term Borrowing
2. Extract interest paid from income statement
3. Calculate net new long-term borrowing = Long-term Debt(end) - Long-term Debt(beginning)
4. Do NOT include short-term notes payable, accounts payable, or other current liabilities
5. Return result (positive = net payment to creditors; negative = net borrowing from creditors)

**Code Example:**

**Scenario:** Interest paid = $850. Long-term debt 2019 = $12,000, 2020 = $15,500. Short-term notes payable decreased by $200. Calculate cash flow to creditors.

**Correct Code:**
```python
# Extract values
interest_paid = 850
long_term_debt_beginning = 12000
long_term_debt_end = 15500

# Calculate net new long-term borrowing (ONLY long-term debt)
net_new_borrowing = long_term_debt_end - long_term_debt_beginning

# Cash flow to creditors
cash_flow_to_creditors = interest_paid - net_new_borrowing

cash_flow_to_creditors
```

**Common Bugs to Avoid:**
- Including short-term notes payable or accounts payable in debt calculation
- Confusing "creditors" with all liabilities (creditors = long-term debt holders)
- Sign error: subtracting interest instead of adding it
- Including current portion of long-term debt separately

---

## Pattern: IRR Calculation with Deprecated NumPy Functions

**Description:** `numpy.irr()` was deprecated in NumPy 1.18 and removed in 1.20+. Modern code must use `numpy_financial.irr()` or root-finding methods from scipy. This is for calculating a single IRR value, not counting multiple IRRs. When no real IRR exists, `npf.irr()` returns NaN, which must be detected and handled appropriately.

**When to Use:** Questions asking for "the IRR" or "compute the IRR" (singular) in Program of Thought solutions requiring numerical methods.

**When NOT to Use:**
- Questions asking "how many IRRs" (use IRR Multiple Root Detection pattern instead)
- Questions asking for IRR count or all IRR values
- **Questions mentioning blocked funds, reinvestment rates, or foreign cash flows UNLESS they explicitly ask to "adjust for" or "account for" these factors**

**Procedure:**
1. Formula: Find r where NPV(r) = Σ(CF_t / (1+r)^t) = 0
2. **Use ORIGINAL cash flows from the problem unless question explicitly asks to adjust them**
3. Import `numpy_financial` (preferred) or `scipy.optimize`
4. Use `npf.irr(cash_flows)` or `scipy.optimize.newton()` with NPV function
5. **Check if result is NaN using `math.isnan()` - indicates no real IRR exists**
6. **If NaN, return string "no real IRR" instead of numeric value**
7. If valid, verify result is reasonable (within expected range, typically -100% to +500%)
8. Return IRR as decimal or percentage as required by question, or "no real IRR" message

**Worked Example:**

**Question:** Cash flows: Year 0: -$15,000, Year 1: $8,000, Year 2: $9,000, Year 3: $6,000. Calculate IRR.

```python
import numpy_financial as npf
import math

# Define cash flows (Year 0 is first element)
cash_flows = [-15000, 8000, 9000, 6000]

# Calculate IRR using numpy_financial
irr_decimal = npf.irr(cash_flows)

# Check if IRR exists (npf.irr returns NaN if no real solution)
if math.isnan(irr_decimal):
    result = "no real IRR"
else:
    # Convert to percentage
    result = irr_decimal * 100

result
```

**Common Bugs to Avoid:**
- Using `np.irr()` which no longer exists
- Not importing `numpy_financial` separately (it's not in base numpy)
- **Not checking for NaN result - returning invalid numeric value when IRR doesn't exist**
- **Returning NaN directly instead of meaningful "no real IRR" message**
- Wrong initial guess in Newton method causing convergence failure
- Using this pattern when question asks "how many IRRs"
- **Assuming Year 0 is always negative without verifying from question context**
- **Adjusting cash flows for blocked funds/reinvestment when question only asks for "the IRR" without explicit adjustment instruction**

**CHECK Steps:**
- **CRITICAL: After calculating IRR, check `math.isnan(irr_decimal)` - if True, return "no real IRR"**
- If question asks for IRR count, use IRR Multiple Root Detection pattern instead
- Verify cash flow signs match question context (don't assume Year 0 is negative)
- **If context mentions blocked funds/reinvestment but question asks "what is the IRR", use ORIGINAL cash flows**
- **Only adjust cash flows if question explicitly says "adjust for", "account for", or "considering the blocked funds"**
- If IRR is valid (not NaN), verify it's in reasonable range (typically -100% to +500%)
- For cash flows with multiple sign changes, consider if multiple IRRs might exist
## Pattern: Cash Flow Sign Convention in IRR Problems

**Description:** IRR calculations require correct sign convention: cash inflows (money received) are positive, cash outflows (payments made) are negative. Reversing signs produces incorrect or negative IRR values. Signs must be determined from explicit context clues in the question, NOT assumed based on position (Year 0 is not always negative).

**When to Use:** Any IRR or NPV calculation where cash flows involve both receipts and payments.

**Procedure:**
1. **Read question carefully for explicit context about cash flow direction**
2. **Look for keywords: "receive", "payment", "invest", "cost", "revenue", "must pay"**
3. Money received/inflows/revenues → positive values
4. Money paid/investments/costs/outflows → negative values
5. **DO NOT assume Year 0 is always negative - verify from context**
6. **If question shows values without context (e.g., from OCR table), preserve original signs**
7. Verify signs before calculation: total inflows should exceed outflows for positive IRR

**Code Example:**

**Scenario:** You receive $8,000 today but must pay $2,500 in year 1, $3,000 in year 2, and $4,000 in year 3. Find IRR.

**Correct Code:**
```python
import numpy_financial as npf
import math

# Correct sign convention based on EXPLICIT context:
# "receive $8,000 today" → POSITIVE
# "must pay" in years 1-3 → NEGATIVE
cash_flows = [8000, -2500, -3000, -4000]

# Calculate IRR
irr_decimal = npf.irr(cash_flows)

# Check if IRR exists
if math.isnan(irr_decimal):
    result = "no real IRR"
else:
    result = irr_decimal * 100

result
```

**Common Bugs to Avoid:**
- Reversing all signs (making receipts negative, payments positive)
- **Assuming Year 0 is always negative investment without checking context**
- **Changing signs from OCR/table data when no context indicates direction**
- Treating initial receipt as negative investment
- Inconsistent signs within the same problem
- Not reading context carefully to determine flow direction

**CHECK Steps:**
- **Before adjusting signs, verify question contains explicit context clues (keywords like "receive", "pay", "invest")**
- **If values come from table/OCR without context, preserve original signs as shown**
- If question says "you receive" → positive; "you pay/invest" → negative
- If question says "initial investment" or "initial cost" → negative Year 0
- Verify at least one positive and one negative cash flow exists (required for IRR)
- After sign assignment, check if pattern makes economic sense
## Pattern: PoT Final Expression Requirement

**Description:** Program of Thought evaluation requires the last line to be an evaluable expression (variable, calculation, or boolean) that produces the answer, NOT a print statement, formatted string, or function call with no return.

**When to Use:** Every PoT solution, especially when answer requires yes/no decision or formatted output.

**Procedure:**
1. Perform all calculations and store in variables
2. Create final answer variable with appropriate type (bool for yes/no, float for numeric)
3. Last line must be bare variable name or simple expression
4. Do NOT use print(), f-strings, or return statements (not in function context)
5. Verify last line evaluates to expected answer type

**Code Example:**

**Scenario:** Project has NPV of $15,000 at 12% discount rate. Should company accept if required return is 12%?

**Correct Code:**
```python
# Calculate NPV
cash_flows = [-50000, 25000, 30000, 20000]
discount_rate = 0.12

npv = sum(cf / (1 + discount_rate)**t for t, cf in enumerate(cash_flows))

# Decision rule: accept if NPV > 0
should_accept = npv > 0

# CORRECT: Last line is evaluable expression
should_accept
```

**Common Bugs to Avoid:**
- Ending with `print(should_accept)` → returns None
- Ending with `f"Accept: {should_accept}"` → returns string, not boolean
- Ending with function definition instead of function call
- Returning intermediate calculation instead of final answer

---

## Pattern: Explicit vs. Derived Capital Expenditure

**Description:** When a question explicitly provides capital expenditure or asset purchase amounts, use the given value directly rather than deriving it from balance sheet changes, which may include other adjustments (disposals, revaluations).

**When to Use:** Cash flow from assets calculations when new fixed asset purchases are explicitly stated in the problem.

**Procedure:**
1. Check if question provides explicit CapEx or "purchased $X in new fixed assets"
2. If provided, use this value directly as capital_expenditures
3. Do NOT calculate CapEx as (Δ Net Fixed Assets + Depreciation) when explicit value given
4. Formula: Cash Flow from Assets = OCF - CapEx - Δ NWC
5. Use given CapEx in formula, not derived value

**Code Example:**

**Scenario:** Company purchased $5,000 in new equipment. Depreciation = $1,200. Net fixed assets increased from $20,000 to $23,500. OCF = $12,000. Δ NWC = $800. Find cash flow from assets.

**Correct Code:**
```python
# Given values
operating_cash_flow = 12000
new_fixed_assets_purchased = 5000  # EXPLICIT value given
change_in_nwc = 800

# DO NOT calculate CapEx from balance sheet when explicit value provided
# Wrong: capex = (23500 - 20000) + 1200 = 4700
# Correct: Use given purchase amount

capital_expenditures = new_fixed_assets_purchased

# Cash flow from assets
cash_flow_from_assets = operating_cash_flow - capital_expenditures - change_in_nwc

cash_flow_from_assets
```

**Common Bugs to Avoid:**
- Ignoring explicit CapEx and calculating from Δ Net Fixed Assets + Depreciation
- Defining variable for given CapEx but not using it
- Assuming balance sheet change always equals purchases (ignores disposals)
- Double-counting depreciation in CapEx calculation

---

## Pattern: NPV-Based Project Acceptance Decision

**Description:** When evaluating project acceptance using a required return rate, calculate NPV at that rate and accept if NPV > 0. This pattern applies when there IS an initial investment at Year 0.

**When to Use:** Questions asking "should company accept project" given cash flows with initial investment and a required/appropriate return rate.

**When NOT to Use:**
- Questions asking only for "present value" without initial investment
- Questions asking for IRR or profitability index
- Cash flow tables showing only future years (Year 1, 2, 3...) without Year 0

**Procedure:**
1. Formula: NPV = Σ(CF_t / (1+r)^t) where r = required return, t starts at 0
2. Extract all cash flows including Year 0 (typically negative initial investment)
3. Extract required return rate
4. Calculate NPV using required return as discount rate
5. Decision: accept if NPV > 0, reject if NPV < 0
6. Return boolean (True/False) or NPV value as appropriate

**Worked Example:**

**Question:** Cash flows: Year 0: -$100,000, Year 1: $40,000, Year 2: $50,000, Year 3: $35,000. Required return = 11%. Should company accept?

```python
# Extract values (Year 0 is first element)
cash_flows = [-100000, 40000, 50000, 35000]
required_return = 0.11

# Calculate NPV at required return rate
npv = sum(cf / (1 + required_return)**t for t, cf in enumerate(cash_flows))

# Decision rule: accept if NPV > 0
should_accept = npv > 0

should_accept
```

**Common Bugs to Avoid:**
- Calculating IRR when question asks about specific required return
- Returning formatted string instead of boolean
- Using wrong discount rate (e.g., IRR instead of required return)
- Treating Year 1 as t=0 when Year 0 initial investment exists
- Confusing with present value calculation (which has no Year 0)

**CHECK Steps:**
- If cash flows include Year 0 (initial investment), use enumerate starting at t=0
- If only future years shown (Year 1, 2, 3...), use Present Value pattern instead
- Verify Year 0 cash flow is NOT discounted (division by (1+r)^0 = 1)

---
## Pattern: Operating Cash Flow Calculation from Income Statement

**Description:** Operating Cash Flow (OCF) is calculated as Net Income + Depreciation, or alternatively as EBIT + Depreciation - Taxes. Depreciation is added back because it's a non-cash expense.

**When to Use:** Cash flow from assets calculations requiring OCF when given income statement with depreciation.

**Procedure:**
1. Formula: OCF = Net Income + Depreciation, or OCF = EBIT(1 - Tax Rate) + Depreciation
2. If Net Income given: add back depreciation directly
3. If only EBIT given: calculate taxes on (EBIT - Interest), then NI = EBIT - Interest - Taxes, then add depreciation
4. Verify depreciation is non-zero and properly extracted
5. Return OCF for use in cash flow from assets formula

**Code Example:**

**Scenario:** Sales = $50,000, COGS = $20,000, Depreciation = $3,000, Interest = $1,500, Tax rate = 35%. Calculate OCF.

**Correct Code:**
```python
# Extract values
sales = 50000
cogs = 20000
depreciation = 3000
interest = 1500
tax_rate = 0.35

# Calculate EBIT
ebit = sales - cogs - depreciation

# Calculate taxable income
taxable_income = ebit - interest

# Calculate taxes
taxes = taxable_income * tax_rate

# Calculate net income
net_income = taxable_income - taxes

# Calculate operating cash flow
operating_cash_flow = net_income + depreciation

operating_cash_flow
```

**Common Bugs to Avoid:**
- Forgetting to add back depreciation (treating it as cash expense)
- Subtracting depreciation twice
- Calculating taxes on EBIT instead of (EBIT - Interest)
- Using wrong tax base (revenue instead of taxable income)

## Pattern: Present Value of Future Cash Flows (No Initial Investment)

**Description:** Calculate the present value of a series of future cash flows when there is NO initial investment at Year 0. All cash flows occur in future periods (Year 1 onwards) and must be discounted back to present value.

**When to Use:** Questions asking for "present value" of cash flows where the table shows Year 1, 2, 3, etc. (no Year 0), or when context clearly indicates all cash flows are future receipts/payments.

**When NOT to Use:**
- NPV calculations with initial investment at Year 0
- Questions explicitly showing Year 0 cash flow in the data
- IRR calculations (which require at least one negative and one positive cash flow)

**Procedure:**
1. Formula: PV = Σ(CF_t / (1+r)^t) for t = 1, 2, 3, ...
2. Identify that Year 1 is the FIRST cash flow (t=1, not t=0)
3. Extract discount rate from question
4. Calculate PV by discounting each cash flow: CF_t / (1+r)^t
5. Sum all discounted cash flows
6. Return total present value

**Worked Example:**

**Question:** Cash flows: Year 1: $500, Year 2: $750, Year 3: $1,000, Year 4: $1,200. What is the present value at 15% discount rate?

```python
# Define cash flows starting at Year 1
cash_flows = [500, 750, 1000, 1200]

# Discount rate
discount_rate = 0.15

# Calculate present value
# Year 1 is t=1, Year 2 is t=2, etc.
present_value = sum(cf / (1 + discount_rate)**(t+1) for t, cf in enumerate(cash_flows))

# Alternative clearer approach:
present_value = 0
for year in range(1, len(cash_flows) + 1):
    cf = cash_flows[year - 1]
    present_value += cf / (1 + discount_rate)**year

present_value
```

**Common Bugs to Avoid:**
- Using `enumerate()` starting at t=0, treating first cash flow as Year 0 (not discounted)
- Confusing this with NPV calculation (which includes Year 0 initial investment)
- Off-by-one errors in time period indexing
- Not discounting the first cash flow (Year 1 must be discounted by (1+r)^1)

**CHECK Steps:**
- If table shows "Year 1, 2, 3..." (no Year 0), all cash flows are future and need discounting
- If question says "present value" (not NPV), there's likely no initial investment
- Verify first cash flow is discounted: CF_1 / (1+r)^1, not CF_1 / (1+r)^0
- Use `(t+1)` with enumerate, or explicit year indexing starting at 1

---

## Pattern: Profitability Index with Multiple Outflows

**Description:** Profitability Index (PI) measures the ratio of present value of future cash flows to initial investment. When there are cash outflows in multiple periods (not just Year 0), ALL future cash flows (both positive and negative) must be included in the numerator.

**When to Use:** Questions asking for "profitability index" or "PI" given a series of cash flows.

**When NOT to Use:**
- NPV calculations (different formula)
- IRR calculations
- When question asks for benefit-cost ratio with different definition

**Procedure:**
1. Formula: PI = PV(all future cash flows) / Initial Investment
2. Identify initial investment (typically Year 0, always negative)
3. Calculate PV of ALL future cash flows (Years 1, 2, 3...), including negative ones
4. PV of future CFs = Σ(CF_t / (1+r)^t) for t ≥ 1
5. PI = PV of future cash flows / |Initial Investment|
6. Return PI value (accept if PI > 1)

**Worked Example:**

**Question:** Cash flows: Year 0: -$2,000, Year 1: -$1,000, Year 2: $1,500, Year 3: $2,000. Discount rate = 10%. Calculate profitability index.

```python
# Define cash flows
cash_flows = [-2000, -1000, 1500, 2000]
discount_rate = 0.10

# Initial investment (Year 0, absolute value)
initial_investment = abs(cash_flows[0])

# Calculate PV of ALL future cash flows (including negative ones)
pv_future_cash_flows = sum(
    cash_flows[t] / (1 + discount_rate)**t 
    for t in range(1, len(cash_flows))
)

# Calculate Profitability Index
profitability_index = pv_future_cash_flows / initial_investment

profitability_index
```

**Common Bugs to Avoid:**
- Excluding negative cash flows from future periods (Year 1, 2, 3...)
- Only summing positive cash flows in the numerator
- Including Year 0 in the numerator calculation
- Dividing by signed initial investment instead of absolute value
- Confusing PI with NPV (NPV includes initial investment in sum, PI separates it)

**CHECK Steps:**
- Verify ALL cash flows from Year 1 onwards are included in PV calculation
- Do NOT filter out negative cash flows in future periods
- Initial investment should be absolute value in denominator
- PI > 1 indicates positive NPV; PI < 1 indicates negative NPV

---

## Pattern: Multi-Year Project IRR with Complex Cash Flows

**Description:** Calculate IRR for projects with multiple years of operations involving revenues, costs, depreciation, taxes, working capital changes, and terminal values. Requires building complete cash flow timeline from operating activities, investments, and recoveries.

**When to Use:** Questions asking for IRR of projects with detailed operational data (unit sales, prices, costs, depreciation schedules, working capital, salvage values).

**When NOT to Use:**
- Simple cash flow series already provided
- Questions asking for NPV only
- Questions asking for IRR count (multiple roots)

**Procedure:**
1. Calculate annual operating cash flows: OCF = (Revenue - Costs - Depreciation) × (1 - Tax) + Depreciation
2. Calculate working capital investments for each year
3. Calculate capital expenditures (equipment purchases)
4. Calculate terminal cash flows (salvage value, working capital recovery)
5. Build complete cash flow timeline: CF_t = OCF_t - CapEx_t - ΔNWC_t + Terminal_t
6. Use numpy_financial.irr() on complete cash flow array
7. Return IRR as percentage

**Worked Example:**

**Question:** Project requires $50,000 equipment (5-year straight-line depreciation, $5,000 salvage). Annual revenue $30,000, costs $12,000. Initial NWC $8,000, recovered at end. Tax rate 30%. Find IRR.

```python
import numpy_financial as npf

# Given data
equipment_cost = 50000
salvage_value = 5000
project_life = 5
annual_revenue = 30000
annual_costs = 12000
initial_nwc = 8000
tax_rate = 0.30

# Calculate annual depreciation
annual_depreciation = (equipment_cost - salvage_value) / project_life

# Calculate annual operating cash flow
ebit = annual_revenue - annual_costs - annual_depreciation
taxes = ebit * tax_rate
ocf = ebit - taxes + annual_depreciation  # Add back depreciation

# Build cash flow timeline
cash_flows = []

# Year 0: Initial investment
cf_0 = -equipment_cost - initial_nwc
cash_flows.append(cf_0)

# Years 1-4: Operating cash flow only
for year in range(1, project_life):
    cash_flows.append(ocf)

# Year 5: Operating cash flow + salvage + NWC recovery
cf_5 = ocf + salvage_value + initial_nwc
cash_flows.append(cf_5)

# Calculate IRR
irr_decimal = npf.irr(cash_flows)
irr_percentage = irr_decimal * 100

irr_percentage
```

**Common Bugs to Avoid:**
- Forgetting to add back depreciation to get OCF (depreciation is non-cash)
- Not recovering working capital at project end
- Calculating taxes on revenue instead of EBIT
- Double-counting NWC recovery (don't add cumulative investments, just recover initial + incremental)
- Index errors when building cash flow array (ensure correct length)
- Not including after-tax salvage value in terminal cash flow

**CHECK Steps:**
- Verify OCF calculation: (Revenue - Costs - Depreciation) × (1 - Tax) + Depreciation
- Verify Year 0 includes all initial investments (equipment + NWC)
- Verify final year includes salvage value and NWC recovery
- Check cash flow array length = project_life + 1 (Year 0 through Year N)
- If code fails, check for index out of bounds errors in array construction