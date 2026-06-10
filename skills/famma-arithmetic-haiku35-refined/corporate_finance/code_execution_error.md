# SKILL PATTERNS FOR CORPORATE FINANCE CODE EXECUTION ERRORS

## Pattern: IRR Calculation with Multiple Sign Changes

**Description:** Computing IRR for non-conventional cash flows (multiple sign changes) requires robust root-finding methods that can detect and return multiple IRRs when they exist. When searching for multiple IRRs, Method A (Polynomial Roots) is preferred as it's guaranteed to find ALL real roots, while Method B (Zero-Crossing Detection) requires a sufficiently wide search range to capture all IRRs. **CRITICAL: All cash flows must have correct signs - initial investments are NEGATIVE, inflows are POSITIVE.**

**When to Use:** Questions asking for IRR when cash flows alternate between positive and negative values, or when asked "how many IRRs are there?" or when given a hint to search within a specific range.

**When NOT to Use:** 
- Questions asking for a single IRR on conventional cash flows (one sign change)
- Questions where all cash flows have the same sign (no IRR exists)
- Questions asking whether to accept/reject a project based on company policy (calculate IRR then compare to hurdle rate)
- **Questions where Year 0 represents an initial investment (should be negative, not positive)**

**Procedure:**
1. Formula: NPV = Σ(CF_t / (1+IRR)^t) = 0, solve for IRR
2. Import numpy and scipy.optimize
3. **CRITICAL: Verify cash flow signs - Year 0 investment must be NEGATIVE**
4. **For multiple IRRs, prefer Method A (Polynomial Roots):**
   - Convert NPV equation to polynomial form
   - Use numpy.roots() to find ALL roots
   - Filter for real, positive roots
5. **If using Method B (Zero-Crossing Detection):**
   - Use WIDE search range (e.g., -0.99 to 10.0 or wider) to capture all IRRs
   - Create dense array (5000+ points) of discount rates
   - Identify sign changes in NPV sequence
   - Use scipy.optimize.brentq on each interval
6. Return count of IRRs or list of IRR values as decimals

**Common Mistakes to Avoid:**
- **Using positive value for Year 0 when it represents an initial investment (must be negative)**
- **Not verifying cash flow signs match the problem context (investments are outflows)**
- Using narrow search range (e.g., -1.0 to 2.0) with Method B - this misses IRRs outside the range
- Using sparse sampling (e.g., 100 points) - this misses roots between sample points
- Checking if NPV ≈ 0 at sample points instead of detecting sign changes
- Missing library imports causing NameError
- Not filtering for positive, real roots

**Example (sanitized):**

> **Scenario:** A project requires initial investment of $50M at Year 0, generates +$120M in Year 1, requires additional investment of -$30M in Year 2. Find how many IRRs exist.
>
> **Wrong approach (incorrect signs):**
> ```python
> # WRONG: Year 0 should be negative for investment
> cash_flows = [50, 120, -30]  # Initial investment shown as positive!
> ```
>
> **Correct approach (Method A - Polynomial Roots):**
> ```python
> import numpy as np
> 
> # Cash flows - CRITICAL: Year 0 investment is NEGATIVE
> cash_flows = [-50, 120, -30]  # Initial outflow is negative
> 
> # Method A: Convert to polynomial and find all roots
> n = len(cash_flows)
> coefficients = []
> for i, cf in enumerate(cash_flows):
>     coefficients.append(cf)
> 
> # Find all roots of polynomial
> roots = np.roots(coefficients)
> 
> # Filter for real, positive IRRs
> irrs = []
> for root in roots:
>     if np.isreal(root):
>         root_val = np.real(root)
>         irr = root_val - 1
>         if irr > 0:
>             irrs.append(irr)
> 
> num_irrs = len(irrs)
> num_irrs  # Returns 2
> ```

---
## Pattern: Multi-Year Capital Budgeting NPV with Dependencies

**Description:** Complex NPV calculations requiring sequential year-by-year computation of operating cash flows, working capital changes, MACRS depreciation, and terminal values. **CRITICAL: When NWC is based on "projected sales increase for the following year," calculate NWC at Year t based on the change from Year t+1 to Year t+2 (forward-looking), not the change from Year t to Year t+1.**

**When to Use:** Questions involving project NPV with working capital requirements, MACRS depreciation schedules, salvage values, and multi-year projections.

**When NOT to Use:**
- Simple NPV calculations without working capital or depreciation
- Questions asking only for IRR (use IRR pattern, though cash flow construction is the same)

**Procedure:**
1. Formula: NPV = Σ(CF_t / (1+r)^t) where CF_t includes OCF, NWC changes, and terminal flows
2. Initialize arrays for revenue, costs, depreciation, NWC, cash flows
3. Compute year-by-year: revenue, operating costs, EBIT, taxes, OCF
4. **Calculate NWC changes - READ TIMING CAREFULLY:**
   - **If "NWC = percentage of revenue":** NWC_t = percentage × Revenue_t
   - **If "NWC = percentage of sales increase for following year":** NWC_t = percentage × (Revenue_{t+1} - Revenue_t)
   - **Year 0 NWC investment based on Year 1 revenue or Year 0→1 change**
5. Apply MACRS depreciation schedule
6. Compute terminal cash flow (salvage + tax adjustment + NWC recovery)
7. Discount all cash flows and sum

**Example (sanitized):**

> **Scenario:** Equipment $120,000, 3-year MACRS, revenues: [Year 1: $80K, Year 2: $95K, Year 3: $88K], costs $40K/year, NWC = 18% of projected sales increase for the following year, salvage 20% of cost, tax 25%, discount 10%
>
> **Wrong approach (backward-looking NWC):**
> ```python
> # WRONG: NWC based on PAST sales change
> nwc_investments = [revenues[0] * 0.18]  # Year 0
> for i in range(1, n_years):
>     nwc_change = (revenues[i] - revenues[i-1]) * 0.18  # WRONG timing
>     nwc_investments.append(nwc_change)
> ```
>
> **Correct approach (forward-looking NWC):**
> ```python
> import numpy as np
> 
> equipment_cost = 120000
> revenues = [80000, 95000, 88000]
> fixed_costs = 40000
> nwc_percent = 0.18
> salvage_percent = 0.20
> tax_rate = 0.25
> discount_rate = 0.10
> macrs_3yr = [0.3333, 0.4445, 0.1481, 0.0741]
> 
> n_years = len(revenues)
> 
> # NWC calculation: "for the following year"
> nwc_investments = []
> 
> # Year 0: Based on Year 1→2 sales increase
> year_0_nwc = (revenues[1] - revenues[0]) * nwc_percent
> nwc_investments.append(year_0_nwc)
> 
> # Year 1: Based on Year 2→3 sales increase
> year_1_nwc = (revenues[2] - revenues[1]) * nwc_percent
> nwc_investments.append(year_1_nwc)
> 
> # Year 2: No following year, so no additional NWC
> nwc_investments.append(0)
> 
> # Depreciation
> depreciation = [equipment_cost * macrs_3yr[i] for i in range(n_years)]
> 
> # Operating cash flows
> ocf = []
> for i in range(n_years):
>     ebit = revenues[i] - fixed_costs - depreciation[i]
>     tax = ebit * tax_rate
>     ocf_year = ebit - tax + depreciation[i]
>     ocf.append(ocf_year)
> 
> # Terminal cash flow
> salvage_value = equipment_cost * salvage_percent
> book_value = equipment_cost - sum(depreciation)
> tax_on_salvage = (salvage_value - book_value) * tax_rate
> nwc_recovery = sum(nwc_investments)
> terminal_cf = salvage_value - tax_on_salvage + nwc_recovery
> 
> # Total cash flows
> cash_flows = [-equipment_cost - nwc_investments[0]]
> for i in range(n_years):
>     if i < n_years - 1:
>         cash_flows.append(ocf[i] - nwc_investments[i+1])
>     else:
>         cash_flows.append(ocf[i] + terminal_cf)
> 
> # NPV
> npv = sum(cf / (1 + discount_rate)**t for t, cf in enumerate(cash_flows))
> npv
> ```

**Common Bugs to Avoid:**
- **Misreading NWC timing: "for the following year" means forward-looking (Year t+1 → t+2), not backward (Year t-1 → t)**
- Off-by-one errors in year indexing
- Forgetting to add back depreciation to OCF
- Not recovering all NWC in terminal year
## Pattern: Profitability Index Calculation

**Description:** Profitability Index requires computing PV of future cash inflows divided by initial investment (absolute value), equivalent to 1 + (NPV / Initial Investment). The numerator must include ALL cash flows except Year 0, properly discounted to present value. Manual PV calculation is required (np.npv is deprecated). **CRITICAL: Do NOT add artificial Year 0 placeholder - use actual cash flow timing from the problem.**

**When to Use:** Questions explicitly asking for "profitability index" or "PI" given a series of cash flows and discount rate.

**When NOT to Use:**
- Questions asking for NPV (use NPV calculation directly)
- Questions asking for IRR (use IRR pattern)
- Questions asking for accept/reject decisions without specifically mentioning PI

**Procedure:**
1. Formula: PI = PV(future inflows) / Initial Investment = 1 + (NPV / |Initial Investment|)
2. **CRITICAL: Manually calculate PV - do NOT use np.npv() (deprecated and removed)**
3. Separate initial investment (Year 0, negative) from future cash flows (Years 1+)
4. **CRITICAL: Match cash flow timing to problem - if Year 1 is first period, start enumeration at 1**
5. Calculate PV of future inflows: Σ(CF_t / (1+r)^t) for t ≥ 1
   - **Use enumerate(future_inflows, start=1) for correct time indexing**
6. Divide by absolute value of initial investment
7. Verify PI > 1 means positive NPV

**Common Mistakes to Avoid:**
- **Using deprecated np.npv() function - it has been removed from NumPy**
- **Always use manual PV calculation with enumerate(future_inflows, start=1)**
- **Adding artificial Year 0 placeholder (e.g., [0, cf1, cf2, ...]) when problem starts at Year 1**
- **Misaligning cash flows with time periods - Year 1 cash flow must be discounted by (1+r)^1**
- Including initial investment in numerator (should only be future inflows)
- Incorrect time indexing: using enumerate() without start=1 discounts Year 1 by (1+r)^0
- Forgetting to take absolute value of initial investment for denominator

**Example (sanitized):**

> **Scenario:** Project X has Year 0: -$8,000, Year 1: $3,500, Year 2: $4,200, Year 3: $2,800, discount rate 12%
>
> **Wrong approach (adding artificial Year 0):**
> ```python
> # WRONG: Adding [0, ...] creates misalignment
> cash_flows = [0, -8000, 3500, 4200, 2800]  # Artificial Year 0!
> future_inflows = cash_flows[2:]  # Now Year 1 is at wrong index
> ```
>
> **Correct approach:**
> ```python
> # Cash flows - use actual timing from problem
> cash_flows = [-8000, 3500, 4200, 2800]  # Year 0, 1, 2, 3
> discount_rate = 0.12
> 
> # Separate initial investment and future inflows
> initial_investment = abs(cash_flows[0])  # 8000 (positive)
> future_inflows = cash_flows[1:]  # [3500, 4200, 2800]
> 
> # CRITICAL: Manual PV calculation with correct time indexing
> # Year 1 cash flow discounted by (1+r)^1, Year 2 by (1+r)^2, etc.
> pv_inflows = sum(cf / (1 + discount_rate)**t 
>                  for t, cf in enumerate(future_inflows, start=1))
> 
> # Profitability Index
> pi = pv_inflows / initial_investment
> 
> pi  # Returns ~1.087
> ```

---
## Pattern: IRR with Standard Cash Flow Sign Convention

**Description:** IRR calculation requires proper cash flow signs and financial libraries. When a question asks for accept/reject decision and explicitly states the company uses IRR rule, calculate IRR and compare to the hurdle rate, returning a boolean or "Yes"/"No" answer.

**When to Use:** 
- Any question asking for IRR or internal rate of return with standard investment pattern
- **Questions asking to accept/reject a project when the question explicitly states the company uses IRR rule/policy**

**When NOT to Use:**
- Questions asking for NPV when no decision rule is specified
- Questions where all cash flows have the same sign (no IRR exists)

**Procedure:**
1. Formula: Find r where NPV = Σ(CF_t / (1+r)^t) = 0
2. Import numpy_financial as npf
3. Construct cash flow array with correct signs (outflows negative, inflows positive)
4. Call npf.irr(cash_flows)
5. **If question asks for accept/reject decision:**
   - Compare IRR to hurdle rate
   - Return "Yes" if IRR > hurdle_rate, else "No"
6. **If question asks only for IRR value:**
   - Return as decimal or multiply by 100 for percentage

**Example (sanitized):**

> **Scenario:** Investment of $15,000 today, receive $6,000 in Year 1, $7,500 in Year 2, $4,500 in Year 3. The company evaluates all projects using the IRR rule. If the required return is 11%, should the company accept?
>
> **Wrong approach:**
> ```python
> # WRONG: Calculates NPV when question asks for IRR decision
> npv = sum(cf / (1.11)**t for t, cf in enumerate([-15000, 6000, 7500, 4500]))
> npv  # Returns numeric NPV, not Yes/No
> ```
>
> **Correct approach:**
> ```python
> import numpy_financial as npf
> 
> # Cash flows with correct sign convention
> cash_flows = [-15000, 6000, 7500, 4500]
> 
> # Calculate IRR
> irr = npf.irr(cash_flows)
> 
> # Question asks for accept/reject using IRR rule
> hurdle_rate = 0.11
> 
> # IRR decision rule: Accept if IRR > required return
> if irr > hurdle_rate:
>     decision = "Yes"
> else:
>     decision = "No"
> 
> decision  # Returns "Yes" or "No"
> ```

**Common Bugs to Avoid:**
- Missing `import numpy_financial as npf` causing NameError
- Using deprecated `numpy.irr()` instead of `numpy_financial.irr()`
- **Calculating NPV when question explicitly states company uses IRR rule**
- **Returning numeric value when question asks for accept/reject decision**
- Incorrect sign convention (initial investment should be negative)

---
## Pattern: IRR with Reversed Cash Flow Signs (Loan/Payment Pattern)

**Description:** When receiving money upfront and making payments later (loan pattern), the initial cash flow is positive and subsequent flows are negative, opposite of typical investment pattern. ALL payment cash flows must be negative. **CRITICAL: Verify the problem context - if it shows negative signs in the data, preserve those signs exactly as given.**

**When to Use:** Questions about loans, offers where you receive money today and pay back later, or any "what is the IRR of this offer" phrasing where you receive funds first.

**When NOT to Use:**
- Standard investment projects (initial outflow, subsequent inflows)
- Questions asking for accept/reject decisions (use NPV comparison instead)
- **When the problem data already shows correct signs (don't reverse them)**

**Procedure:**
1. Formula: NPV = Σ(CF_t / (1+r)^t) = 0, solve for r
2. **CRITICAL: Read the problem data carefully - if signs are already provided, use them as-is**
3. Identify cash flow direction: initial inflow (positive), subsequent outflows (negative)
4. **Verify ALL payment amounts are negative in the cash flow array**
5. Import numpy_financial as npf
6. Construct array: [+initial_amount, -payment1, -payment2, ...]
7. Calculate IRR and return as decimal

**Common Mistakes to Avoid:**
- Reversing all signs (making initial receipt negative)
- **Forgetting negative signs on ANY payment cash flows (all payments must be negative)**
- **Mixing positive and negative signs in payment years (e.g., [12000, -5500, 4200, -3800])**
- **Changing signs when problem data already provides correct signs**
- Missing library import
- Confusing IRR interpretation (this is the interest rate you're paying, not earning)

**Example (sanitized):**

> **Scenario:** Receive $12,000 today, pay $5,500 in Year 1, $4,200 in Year 2, $3,800 in Year 3
>
> **Wrong approach (if data shows negative signs):**
> ```python
> # WRONG: If problem shows "Year 1: -$5,500", don't negate again
> cash_flows = [12000, -(-5500), -(-4200), -(-3800)]  # Double negation!
> ```
>
> **Correct approach:**
> ```python
> import numpy_financial as npf
> 
> # Cash flows: receive money (positive), then make payments (ALL negative)
> cash_flows = [12000, -5500, -4200, -3800]
> 
> # Calculate IRR (this is the cost of the loan)
> irr = npf.irr(cash_flows)
> 
> irr  # Returns decimal (e.g., 0.1456 for 14.56%)
> ```

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

**Description:** When cash flows are blocked and must be reinvested, only POSITIVE cash flows (inflows) are subject to blocking. Each blocked inflow is shifted forward and grows at the reinvestment rate. Negative cash flows (costs) occur as scheduled. **CRITICAL: Use index-based assignment with pre-allocated array, NOT append() operations, to maintain proper time alignment.**

**When to Use:** Questions mentioning "blocked funds," "reinvestment requirement," or mandatory holding periods for foreign investment cash flows.

**Procedure:**
1. Identify which cash flows are blocked (typically only positive inflows)
2. **CRITICAL: Pre-allocate adjusted array with length = original length + 1:**
   ```python
   adjusted_cf = [0] * (len(original_cf) + 1)
   ```
3. Year 0: Keep initial investment unchanged: `adjusted_cf[0] = original_cf[0]`
4. **Use INDEX-BASED assignment (NOT append):**
   - For negative CF: `adjusted_cf[t] = original_cf[t]` (not blocked)
   - For positive CF: `adjusted_cf[t+1] += original_cf[t] * (1 + reinvestment_rate)`
5. Calculate IRR on adjusted cash flow array

**Example (sanitized):**

> **Scenario:** Investment of -$600,000 at Year 0. Year 1: -$150,000 (cost). Year 2: +$250,000 (revenue). Year 3: +$350,000 (revenue). All positive cash flows blocked and reinvested at 6% for one year. Find IRR.
>
> **Wrong approach (using append):**
> ```python
> # WRONG: Using append() creates misaligned array
> adjusted_cf = [original_cf[0]]
> for i in range(1, len(original_cf)):
>     if original_cf[i] < 0:
>         adjusted_cf.append(original_cf[i])
>         adjusted_cf.append(0)  # WRONG: Creates extra element
>     else:
>         adjusted_cf.append(0)
>         adjusted_cf.append(original_cf[i] * 1.06)
> # Result: 7 elements instead of 5, wrong time alignment
> ```
>
> **Correct approach (index-based assignment):**
> ```python
> import numpy_financial as npf
> 
> original_cf = [-600000, -150000, 250000, 350000]
> reinvestment_rate = 0.06
> 
> # Step 1: Pre-allocate array (length = original + 1)
> adjusted_cf = [0] * (len(original_cf) + 1)  # Length 5
> 
> # Step 2: Year 0 unchanged
> adjusted_cf[0] = original_cf[0]  # -600000
> 
> # Step 3: Process each year with INDEX assignment
> for t in range(1, len(original_cf)):
>     if original_cf[t] < 0:
>         # Negative: occurs as scheduled, not blocked
>         adjusted_cf[t] = original_cf[t]
>     else:
>         # Positive: blocked, received next year with growth
>         adjusted_cf[t+1] += original_cf[t] * (1 + reinvestment_rate)
> 
> # Result: [-600000, -150000, 0, 265000, 371000]
> # Year 0: -600000 (initial)
> # Year 1: -150000 (cost, not blocked)
> # Year 2: 0 (Year 2 revenue blocked)
> # Year 3: 265000 (Year 2's 250000 × 1.06)
> # Year 4: 371000 (Year 3's 350000 × 1.06)
> 
> irr = npf.irr(adjusted_cf)
> irr
> ```

**Common Mistakes to Avoid:**
- **Using append() instead of index-based assignment (creates wrong array length)**
- **Not pre-allocating array with correct length (original + 1)**
- Applying blocking to negative cash flows (costs should occur as scheduled)
- Not using += when multiple blocked amounts land in same year

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

**Description:** When asked for IRR after computing NPV on a complex multi-year project, reuse the same cash flow array construction logic but call IRR solver instead of NPV formula. The question context determines which metric to return.

**When to Use:** Questions asking for IRR on projects with working capital, depreciation, and terminal values (same setup as complex NPV questions).

**When NOT to Use:**
- Questions asking only for NPV (return NPV value)
- Questions asking for both NPV and another metric like maximum beta (return tuple of both values)
- Questions asking for accept/reject decisions (compare to hurdle rate)

**Procedure:**
1. Use identical cash flow construction as NPV calculation
2. Build complete cash flow array: [Year 0 outflows, Year 1-n operating CF + adjustments, Terminal CF]
3. Verify cash flow array has correct signs and completeness
4. **If question asks ONLY for IRR:** Import numpy_financial and call npf.irr(cash_flows), return IRR
5. **If question asks for NPV AND another metric:** Calculate both, return tuple (npv, other_metric)
6. **If question asks for accept/reject decision:** Calculate NPV or IRR, compare to threshold, return boolean

**Code Example:**

**Scenario:** Same project as multi-year NPV example, but question asks "what is the IRR?"

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

# Calculate IRR (question asks only for IRR)
irr = npf.irr(cash_flows)

irr  # Return only IRR as decimal
```

**Example for Multiple Metrics:**
```python
# If question asks: "What is the NPV and maximum beta?"
npv = sum(cf / (1 + discount_rate)**t for t, cf in enumerate(cash_flows))
max_beta = find_max_beta()  # Some calculation

(npv, max_beta)  # Return tuple of both values
```

**Common Bugs to Avoid:**
- Inconsistent cash flow construction between NPV and IRR calculations
- Missing terminal cash flow components (salvage, NWC recovery)
- Incorrect initial outflow (should include equipment + initial NWC)
- **Returning only one value when question asks for multiple metrics**
- **Returning numeric value when question asks for boolean decision**
- Runtime errors from incomplete cash flow array
- Not handling IRR calculation failure when no solution exists
## Pattern: IRR Non-Existence Detection for Non-Conventional Cash Flows

**Description:** For non-conventional cash flows, IRR may not exist as a meaningful positive real number. Code must validate that: (1) a real solution exists, (2) the solution is positive, and (3) NPV can actually reach zero for some positive discount rate. This validation is REQUIRED, not optional. Use proper try-except syntax for exception handling.

**When to Use:** Questions asking for IRR when: (1) cash flows have unusual patterns (multiple sign changes or all negative), (2) the answer might be "no real IRR exists" or "IRR does not exist", or (3) when initial cash flows are negative followed by insufficient positive flows.

**Procedure:**
1. Count sign changes in cash flow sequence (Descartes' Rule indicator)
2. **Use proper try-except syntax (NOT try-else):**
   ```python
   try:
       calculated_irr = npf.irr(cash_flows)
   except:
       calculated_irr = None
   ```
3. REQUIRED VALIDATION (all must pass):
   - Check if solver returned a value (not None)
   - Check if value is real (not NaN): `not np.isnan(calculated_irr)`
   - Check if value is POSITIVE: `calculated_irr > 0`
4. If ANY validation fails, return the string `"no real IRR"`
5. If all validations pass, return the IRR as a decimal

**Example (sanitized):**

> **Scenario:** A project has cash flows: Year 0: -$12,000, Year 1: -$8,000, Year 2: +$5,000. Find the IRR.
>
> **Wrong approach (syntax error):**
> ```python
> # WRONG: Python syntax error - try-else is invalid
> try:
>     irr = npf.irr(cash_flows)
> else:  # SyntaxError! Should be 'except:'
>     irr = "no real IRR"
> ```
>
> **Correct approach:**
> ```python
> import numpy as np
> import numpy_financial as npf
> 
> cash_flows = np.array([-12000, -8000, 5000])
> 
> # Step 1: Attempt calculation with CORRECT try-except syntax
> try:
>     calculated_irr = npf.irr(cash_flows)
> except:
>     calculated_irr = None
> 
> # Step 2: REQUIRED validation
> if calculated_irr is None:
>     result = "no real IRR"
> elif np.isnan(calculated_irr):
>     result = "no real IRR"
> elif calculated_irr <= 0:
>     # Negative or zero IRR is not meaningful for investments
>     result = "no real IRR"
> else:
>     # All validations passed
>     result = float(calculated_irr)
> 
> result  # Returns "no real IRR"
> ```

**Common Mistakes to Avoid:**
- **Using try-else instead of try-except (syntax error)**
- **Correct syntax is: try: ... except: ... (not try: ... else: ...)**
- Treating validation as optional rather than required
- Returning negative IRR values instead of "no real IRR"
- Not checking if IRR is positive

---

## Pattern: Present Value Calculation Without Year 0 Investment

**Description:** When calculating present value of a series of future cash flows that do NOT include an initial Year 0 investment, all cash flows start from Year 1 onwards. The time indexing must match the actual year numbers provided in the problem. Do NOT add artificial Year 0 placeholders.

**When to Use:** 
- Questions asking for "present value of these cash flows" when no Year 0 is mentioned
- Problems where the cash flow table starts at Year 1 (not Year 0)
- Questions about valuing future payment streams or revenue projections

**When NOT to Use:**
- Problems that explicitly include Year 0 cash flows
- NPV calculations that include initial investment
- Questions asking for profitability index (use PI pattern)

**Procedure:**
1. Formula: PV = Σ(CF_t / (1+r)^t) for t = 1, 2, 3, ...
2. **CRITICAL: Identify the starting year from the problem (usually Year 1)**
3. **Do NOT add [0, ...] placeholder - use actual cash flows as given**
4. Use enumerate with start parameter matching the first year number
5. Calculate: `sum(cf / (1 + r)**t for t, cf in enumerate(cash_flows, start=first_year))`
6. Return total present value

**Common Mistakes to Avoid:**
- **Adding artificial Year 0 with value 0 (e.g., [0, cf1, cf2, ...]) - this shifts all periods**
- **Using enumerate(cash_flows, start=0) when Year 1 is the first period**
- **Discounting Year 1 cash flow by (1+r)^0 instead of (1+r)^1**
- Confusing PV calculation with NPV (which includes initial investment)

**Example (sanitized):**

> **Scenario:** Calculate present value of cash flows: Year 1: $500, Year 2: $700, Year 3: $900, Year 4: $1,200 at 8% discount rate.
>
> **Wrong approach (adding Year 0 placeholder):**
> ```python
> # WRONG: Adding Year 0 shifts all periods forward
> cash_flows = [0, 500, 700, 900, 1200]  # Artificial Year 0!
> pv = sum(cf / (1.08)**t for t, cf in enumerate(cash_flows, start=1))
> # Now Year 1's $500 is discounted by (1.08)^2 instead of (1.08)^1
> ```
>
> **Correct approach:**
> ```python
> # Cash flows starting from Year 1 (no Year 0)
> cash_flows = [500, 700, 900, 1200]
> discount_rate = 0.08
> 
> # Calculate PV with correct time indexing
> # First cash flow is Year 1, so start=1
> pv = sum(cf / (1 + discount_rate)**t 
>          for t, cf in enumerate(cash_flows, start=1))
> 
> pv  # Returns correct present value
> ```

---

## Pattern: Solving for Missing Cash Flow in PV Equation

**Description:** When given a target present value and asked to find a missing cash flow in a specific year, use root-finding methods with correct time period indexing. The missing cash flow's position in the array must match its actual year number from the problem.

**When to Use:** 
- Questions asking "what is the value of the missing cash flow" given a target PV
- Problems providing all cash flows except one, with a known discount rate and total PV

**When NOT to Use:**
- Questions asking for IRR (use IRR pattern)
- Questions asking for NPV calculation (use NPV pattern)

**Procedure:**
1. **CRITICAL: Identify which year has the missing cash flow from the problem statement**
2. Create cash flow array with placeholder (0 or variable) at the CORRECT index
3. **Verify array indexing: if missing cash flow is "Year 2", it should be at index 2 if Year 0 exists, or index 1 if starting from Year 1**
4. Define NPV function that calculates PV with the unknown as a variable
5. Use root-finding (scipy.optimize.brentq or similar) to solve for the unknown
6. Return the missing cash flow value

**Common Mistakes to Avoid:**
- **Misidentifying which index corresponds to the missing year**
- **Adding artificial Year 0 when problem starts at Year 1 (shifts all indices)**
- **Placing unknown at wrong position in array (e.g., Year 2 at index 1 when Year 0 exists)**
- Not accounting for the sign of the missing cash flow (inflow vs outflow)

**Example (sanitized):**

> **Scenario:** PV is $6,500 at 8% discount. Cash flows: Year 1: -$1,200, Year 2: unknown, Year 3: $2,400, Year 4: $2,600. Find Year 2 cash flow.
>
> **Wrong approach (incorrect indexing):**
> ```python
> # WRONG: Placing unknown at index 1 when it should be at index 2
> cash_flows = [0, -1200, 2400, 2600]  # Added Year 0, shifted everything
> # Now Year 2 unknown is at index 1, but should be at index 2
> ```
>
> **Correct approach:**
> ```python
> from scipy.optimize import brentq
> 
> # Known cash flows (Year 1, 2, 3, 4 - no Year 0)
> # Year 2 is at index 1 in this array
> known_cf = [-1200, None, 2400, 2600]
> discount_rate = 0.08
> target_pv = 6500
> 
> def solve_pv(x):
>     # Create full cash flow array with x as Year 2 value
>     cash_flows = [-1200, x, 2400, 2600]
>     # Calculate PV starting from Year 1
>     pv = sum(cf / (1 + discount_rate)**t 
>              for t, cf in enumerate(cash_flows, start=1))
>     return pv - target_pv
> 
> # Solve for missing cash flow
> missing_cf = brentq(solve_pv, -10000, 10000)
> 
> missing_cf  # Returns Year 2 cash flow value
> ```