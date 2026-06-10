# DETAILED SKILL PATTERNS FOR CORPORATE FINANCE (PoT)

## Pattern: IRR Multiple Root Detection with Polynomial Methods

**Description:** When cash flows change sign multiple times, the NPV polynomial can have multiple real IRR solutions. Grid-based sign-change detection may miss closely-spaced roots due to insufficient resolution or overly aggressive duplicate filtering.

**When to Use:** Questions asking "how many IRRs" or "find all IRRs" with non-conventional cash flow patterns (multiple sign changes), especially when a search range is specified.

**Procedure:**
1. Formula: NPV(r) = Σ(CF_t / (1+r)^t) = 0; solve for all r in specified range
2. Use fine grid resolution (≥10,000 points per 50% range) to detect all sign changes
3. Apply bisection/Newton method to refine each detected root
4. Filter duplicates with strict tolerance (≤1e-5) to avoid merging distinct roots
5. Verify each IRR by checking |NPV(r)| < 1e-6
6. Return count as integer expression

**Code Example:**

**Scenario:** Cash flows: Year 0: -$5,000, Year 1: $15,000, Year 2: $18,000, Year 3: -$20,000. Find number of IRRs between 10% and 80%.

**Correct Code:**
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

# Return count
len(unique_irrs)
```

**Common Bugs to Avoid:**
- Using too coarse grid (e.g., 1000 points) that skips over closely-spaced roots
- Duplicate threshold too large (e.g., 0.001) merging distinct IRRs
- Not verifying NPV ≈ 0 for each candidate root
- Returning list instead of integer count

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

**Description:** `numpy.irr()` was deprecated in NumPy 1.18 and removed in 1.20+. Modern code must use `numpy_financial.irr()` or root-finding methods from scipy.

**When to Use:** Any IRR calculation in Program of Thought solutions requiring numerical methods.

**Procedure:**
1. Formula: Find r where NPV(r) = Σ(CF_t / (1+r)^t) = 0
2. Import `numpy_financial` (preferred) or `scipy.optimize`
3. Use `npf.irr(cash_flows)` or `scipy.optimize.newton()` with NPV function
4. Verify result is reasonable (not NaN, within expected range)
5. Return IRR as decimal or percentage as required

**Code Example:**

**Scenario:** Cash flows: [-10000, 3000, 4000, 5000]. Calculate IRR.

**Correct Code:**
```python
import numpy_financial as npf

# Define cash flows (Year 0 is first element)
cash_flows = [-10000, 3000, 4000, 5000]

# Calculate IRR using numpy_financial
irr_decimal = npf.irr(cash_flows)

# Convert to percentage
irr_percentage = irr_decimal * 100

irr_percentage
```

**Alternative with scipy:**
```python
from scipy.optimize import newton

cash_flows = [-10000, 3000, 4000, 5000]

def npv(rate):
    return sum(cf / (1 + rate)**t for t, cf in enumerate(cash_flows))

# Find root starting from 10% guess
irr_decimal = newton(npv, 0.10)
irr_percentage = irr_decimal * 100

irr_percentage
```

**Common Bugs to Avoid:**
- Using `np.irr()` which no longer exists
- Not importing `numpy_financial` separately (it's not in base numpy)
- Forgetting to handle cases where IRR doesn't exist (check for NaN)
- Wrong initial guess in Newton method causing convergence failure

---

## Pattern: Cash Flow Sign Convention in IRR Problems

**Description:** IRR calculations require correct sign convention: cash inflows (money received) are positive, cash outflows (payments made) are negative. Reversing signs produces incorrect or negative IRR values.

**When to Use:** Any IRR or NPV calculation where cash flows involve both receipts and payments.

**Procedure:**
1. Identify direction of each cash flow from context
2. Money received/inflows → positive values
3. Money paid/investments/outflows → negative values
4. Initial investment at t=0 is typically negative
5. Verify signs before calculation: total inflows should exceed outflows for positive IRR

**Code Example:**

**Scenario:** You receive $8,000 today but must pay $2,500 in year 1, $3,000 in year 2, and $4,000 in year 3. Find IRR.

**Correct Code:**
```python
import numpy_financial as npf

# Correct sign convention:
# Year 0: receive $8,000 → POSITIVE
# Year 1-3: make payments → NEGATIVE
cash_flows = [8000, -2500, -3000, -4000]

# Calculate IRR
irr_decimal = npf.irr(cash_flows)
irr_percentage = irr_decimal * 100

irr_percentage
```

**Common Bugs to Avoid:**
- Reversing all signs (making receipts negative, payments positive)
- Treating initial receipt as negative investment
- Inconsistent signs within the same problem
- Not reading context carefully to determine flow direction

---

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

**Description:** When evaluating project acceptance using a required return rate, calculate NPV at that rate and accept if NPV > 0, regardless of whether the question mentions IRR rule.

**When to Use:** Questions asking "should company accept project" given cash flows and a required/appropriate return rate.

**Procedure:**
1. Formula: NPV = Σ(CF_t / (1+r)^t) where r = required return
2. Extract all cash flows (t=0 to t=n)
3. Extract required return rate
4. Calculate NPV using required return as discount rate
5. Decision: accept if NPV > 0, reject if NPV < 0
6. Return boolean (True/False) or NPV value as appropriate

**Code Example:**

**Scenario:** Cash flows: Year 0: -$100,000, Year 1: $40,000, Year 2: $50,000, Year 3: $35,000. Required return = 11%. Should company accept?

**Correct Code:**
```python
# Extract values
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
- Forgetting that Year 0 cash flow is not discounted (t=0)

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