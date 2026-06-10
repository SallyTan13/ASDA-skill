# DETAILED SKILL PATTERNS FOR ALTERNATIVE INVESTMENTS (PoT)

## Pattern: Tax-Deferred Account Accrual Equivalent Return

**Description:** When calculating accrual equivalent returns for tax-deferred accounts where taxes are paid only at liquidation (not annually), must use the future value approach with end-period taxation, then convert to equivalent annual rate, not simply reduce the pre-tax return by the tax rate.

**When to Use:** Questions involving tax-deferred retirement accounts, accrual equivalent returns, portfolio returns with mixed tax treatment (taxable, tax-deferred, tax-exempt accounts).

**Procedure:**
1. **Formula for tax-deferred accrual equivalent:** r* = [(1 + r_pretax)^n × (1 - t_final)]^(1/n) - 1
2. Identify account types: taxable (annual tax), tax-deferred (end-period tax), tax-exempt (no tax)
3. For taxable accounts: r_after_tax = r_pretax × (1 - t_annual)
4. For tax-deferred accounts: Calculate FV with deferred tax, then annualize back to equivalent rate
5. For tax-exempt accounts: r_after_tax = r_pretax
6. Weight by account values to get portfolio accrual equivalent return

**Code Example:**

**Scenario:** Portfolio has $500k taxable (10% pretax return, 25% annual tax), $300k tax-deferred (8% pretax return, 35% tax at year 10), $200k tax-exempt (9% pretax return). Calculate 10-year accrual equivalent return.

**Correct Code:**
```python
# Account values and returns
taxable_value = 500_000
tax_deferred_value = 300_000
tax_exempt_value = 200_000
total_value = taxable_value + tax_deferred_value + tax_exempt_value

taxable_pretax_return = 0.10
tax_deferred_pretax_return = 0.08
tax_exempt_pretax_return = 0.09

# Tax rates
annual_tax_rate = 0.25
deferred_tax_rate = 0.35
holding_period = 10

# Taxable account: annual taxation
taxable_after_tax_annual = taxable_pretax_return * (1 - annual_tax_rate)

# Tax-deferred account: accrual equivalent with end-period taxation
# FV factor after tax = (1 + r)^n × (1 - t)
# Accrual equivalent = [(1 + r)^n × (1 - t)]^(1/n) - 1
fv_factor_after_tax = ((1 + tax_deferred_pretax_return) ** holding_period) * (1 - deferred_tax_rate)
tax_deferred_accrual_equivalent = (fv_factor_after_tax ** (1 / holding_period)) - 1

# Tax-exempt account: no taxation
tax_exempt_after_tax_annual = tax_exempt_pretax_return

# Weighted average accrual equivalent return
weighted_accrual_equivalent = (
    (taxable_value / total_value) * taxable_after_tax_annual +
    (tax_deferred_value / total_value) * tax_deferred_accrual_equivalent +
    (tax_exempt_value / total_value) * tax_exempt_after_tax_annual
)

round(weighted_accrual_equivalent * 100, 2)  # Convert to percentage
```

**Common Bugs to Avoid:**
- Treating deferred tax as annual tax: r × (1 - t) instead of proper accrual formula
- Forgetting to annualize: using (1+r)^n × (1-t) directly without taking nth root
- Mixing up tax rates: using annual tax rate for deferred accounts
- Not weighting by account values when combining multiple account types

---

## Pattern: Human Life Value with Employer Benefits

**Description:** When calculating Human Life Value for life insurance needs or holistic balance sheets, employer contributions to retirement plans (pension, 401k) are part of total compensation that benefits the family and must be ADDED to the after-tax income stream. Additionally, existing pension account balances must be included as separate assets in holistic balance sheet calculations. **CRITICAL: For economic/holistic balance sheets, human capital (present value of future earnings) must be included in total assets; for traditional balance sheets, only tangible assets are included.**

**When to Use:** Life insurance needs calculation using Human Life Value method, holistic balance sheet preparation, economic balance sheet calculations, questions involving employer pension contributions, total compensation analysis, retirement account valuations, questions explicitly mentioning "economic balance sheet" or "net wealth."

**When NOT to Use:** 
- Questions asking specifically for "traditional balance sheet" or "tangible assets only"
- Questions that explicitly exclude human capital from the calculation
- When the question context does NOT mention economic balance sheets or human capital concepts

**Procedure:**
1. **Identify balance sheet type:**
   - **Economic/Holistic balance sheet:** Include human capital (PV of future earnings) in assets
   - **Traditional balance sheet:** Include only tangible/financial assets (exclude human capital)
   - **Key indicators:** Look for terms like "economic balance sheet," "human capital," "net wealth," or context discussing human capital concepts
2. **For Human Life Value calculation:** HLV = PV of [After-tax income + Employer contributions - Personal expenses attributable to insured]
3. Calculate gross income for each future year (with growth rate)
4. Subtract income/payroll taxes to get after-tax income
5. **ADD employer pension/retirement contributions** (they benefit the family through retirement savings)
6. Subtract only personal expenses attributable to the insured individual
7. Discount each year's net income to present value
8. Sum all PV amounts to get total Human Life Value
9. **For economic/holistic balance sheets:** 
   - Assets = Tangible assets + Human capital (PV of future earnings) + Existing pension balances
   - Net wealth = Total assets - Total liabilities
10. **For traditional balance sheets:**
   - Assets = Tangible assets + Existing pension balances (exclude human capital)
   - Net wealth = Total assets - Total liabilities
11. Additional insurance needed = HLV - Current coverage

**Common Mistakes to Avoid:**
- **Excluding human capital from economic balance sheets** - when context discusses economic vs traditional balance sheets, human capital must be included
- **Including human capital in traditional balance sheets** - traditional balance sheets only include tangible/financial assets
- Subtracting employer contributions instead of adding them - they benefit the family through retirement savings
- Treating employer contributions like taxes (they're not a reduction in family wealth)
- Confusing "income taxes" with "total deductions" - only taxes reduce take-home pay
- Forgetting to add existing pension/retirement account balances to holistic balance sheets
- Assuming pension values are already included in traditional assets without verifying the asset breakdown
- Not growing employer contributions at the same rate as salary
- Using simple PV formula instead of year-by-year calculation when income/expenses grow
- Forgetting to subtract existing life insurance coverage from HLV to get additional need

**Example (sanitized):**

> **Scenario A (Economic Balance Sheet):** Individual age 45, current salary $200k, tax rate 28%, employer match 6% of salary. Tangible assets: $1.5M (home $600k, investments $900k). Liabilities: $400k mortgage. PV of future earnings: $2.8M. Calculate net wealth for economic balance sheet.
>
> **Wrong approach:** 
> ```python
> # WRONG: Excludes human capital from economic balance sheet
> tangible_assets = 1_500_000
> liabilities = 400_000
> net_wealth = tangible_assets - liabilities  # = 1,100,000
> # This understates economic net wealth
> ```
>
> **Correct approach:**
> ```python
> # Economic balance sheet includes human capital
> tangible_assets = 1_500_000
> human_capital_pv = 2_800_000  # PV of future earnings
> total_assets = tangible_assets + human_capital_pv
> 
> liabilities = 400_000
> net_wealth = total_assets - liabilities  # = 3,900,000
> ```
>
> **Scenario B (Life Insurance Need):** Same individual, retiring in 20 years, salary growing 3%/year, personal expenses $25k/year (growing 2%/year), discount rate 5%. Current life insurance $500k. Calculate additional insurance needed.
>
> **Correct approach:**
> ```python
> current_salary = 200_000
> years_to_retirement = 20
> salary_growth = 0.03
> tax_rate = 0.28
> employer_match_rate = 0.06
> personal_expenses_initial = 25_000
> expense_growth = 0.02
> discount_rate = 0.05
> 
> hlv = 0
> for year in range(1, years_to_retirement + 1):
>     future_salary = current_salary * ((1 + salary_growth) ** year)
>     after_tax_income = future_salary * (1 - tax_rate)
>     
>     # CRITICAL: Add employer contribution (benefits family)
>     employer_contribution = future_salary * employer_match_rate
>     
>     future_expenses = personal_expenses_initial * ((1 + expense_growth) ** year)
>     net_income_to_family = after_tax_income + employer_contribution - future_expenses
>     
>     pv = net_income_to_family / ((1 + discount_rate) ** year)
>     hlv += pv
> 
> current_coverage = 500_000
> additional_insurance = hlv - current_coverage
> ```
## Pattern: Mutually Exclusive Projects with Scale Differences

**Description:** For mutually exclusive projects with significantly different initial investments, IRR alone can give incorrect rankings because it ignores scale effects. Must use NPV at the given discount rate or perform incremental IRR analysis.

**When to Use:** Capital budgeting decisions with mutually exclusive projects, questions explicitly stating "mutually exclusive," projects with different initial investment scales.

**Procedure:**
1. **Decision Rule:** For mutually exclusive projects, use NPV, not IRR
2. **Formula:** NPV = Σ [CF_t / (1 + r)^t] where r is the discount rate
3. Calculate NPV for each project at the given discount rate
4. Select the project with the highest positive NPV
5. IRR can be calculated for reference, but NPV determines the choice
6. Alternative: Calculate incremental IRR (IRR of larger - smaller project) and compare to discount rate

**Code Example:**

**Scenario:** Two mutually exclusive projects, discount rate 12%. Project A: Initial cost $400k, cash flows $250k, $180k, $120k (years 1-3). Project B: Initial cost $850k, cash flows $380k, $420k, $350k (years 1-3).

**Correct Code:**
```python
import numpy as np

# Project cash flows (Year 0 is negative for initial investment)
project_a_cashflows = np.array([-400_000, 250_000, 180_000, 120_000])
project_b_cashflows = np.array([-850_000, 380_000, 420_000, 350_000])

discount_rate = 0.12

# Calculate NPV for each project (CORRECT method for mutually exclusive)
def calculate_npv(cashflows, rate):
    npv = 0
    for t, cf in enumerate(cashflows):
        npv += cf / ((1 + rate) ** t)
    return npv

npv_a = calculate_npv(project_a_cashflows, discount_rate)
npv_b = calculate_npv(project_b_cashflows, discount_rate)

# Decision: Select project with higher NPV
if npv_a > npv_b and npv_a > 0:
    selected_project = "Project A"
    selected_npv = npv_a
elif npv_b > npv_a and npv_b > 0:
    selected_project = "Project B"
    selected_npv = npv_b
else:
    selected_project = "Neither (both have negative NPV)"
    selected_npv = max(npv_a, npv_b)

# For reference, can also calculate IRR (but don't use for decision)
from numpy_financial import irr
irr_a = irr(project_a_cashflows)
irr_b = irr(project_b_cashflows)

# Return the decision
selected_project
```

**Common Bugs to Avoid:**
- Using IRR to rank mutually exclusive projects with different scales
- Selecting higher IRR without checking NPV when projects are mutually exclusive
- Forgetting that Year 0 cash flow is typically negative (initial investment)
- Not checking if both projects have positive NPV before selecting
- Ignoring the scale difference (e.g., 20% return on $100k vs 15% return on $1M)

---

## Pattern: Endowment Spending Based on Trailing Average

**Description:** Endowment spending policies often use a trailing multi-year average of endowment value (not current value) to smooth volatility. Must identify the averaging period and apply spending rate to the averaged value, not the current market value.

**When to Use:** Endowment spending calculations, questions mentioning "trailing average," "5-year average," "smoothed spending," endowment liability calculations.

**Procedure:**
1. **Formula:** Annual Spending = Spending Rate × Trailing N-Year Average Value
2. Identify the trailing period (e.g., 5-year average)
3. If historical values not given, use current value as proxy but note the limitation
4. Calculate total liabilities = Spending + Capital Calls + Other Commitments
5. For capital calls: Apply percentage to relevant asset class NAV (e.g., private equity + real estate)
6. Verify asset allocation percentages sum to 100% or close to it

**Code Example:**

**Scenario:** Endowment current value $2B, spending rate 4.5% on trailing 5-year average. Assume 5-year average is 95% of current value (typical during growth period). Private equity 18%, private real estate 12% of current value. Capital calls expected at 25% of private assets NAV. Calculate 12-month liabilities.

**Correct Code:**
```python
# Endowment parameters
current_endowment_value = 2_000_000_000
spending_rate = 0.045
trailing_average_factor = 0.95  # 5-year average as % of current value

# Asset allocation
private_equity_allocation = 0.18
private_real_estate_allocation = 0.12

# Capital call rate
capital_call_rate = 0.25

# Calculate spending based on trailing average (NOT current value)
trailing_5year_average_value = current_endowment_value * trailing_average_factor
annual_spending = trailing_5year_average_value * spending_rate

# Calculate private assets NAV
private_equity_value = current_endowment_value * private_equity_allocation
private_real_estate_value = current_endowment_value * private_real_estate_allocation
total_private_assets_nav = private_equity_value + private_real_estate_value

# Calculate capital calls
capital_calls = total_private_assets_nav * capital_call_rate

# Total 12-month liabilities
total_liabilities = annual_spending + capital_calls

# Convert to millions for reporting
total_liabilities_millions = total_liabilities / 1_000_000

round(total_liabilities_millions, 0)
```

**Common Bugs to Avoid:**
- Applying spending rate to current value instead of trailing average
- Ignoring the "trailing average" language in the problem statement
- Calculating capital calls on total endowment instead of just private assets
- Using wrong asset classes for capital calls (only private equity and private real estate typically have capital calls)
- Forgetting to convert final answer to millions when options are in millions
- Miscalculating private assets NAV by using wrong allocation percentages

---

## Pattern: Multi-Period Cash Flow Present Value with Growth

**Description:** When cash flows grow at a constant rate and are discounted at a different rate, must calculate year-by-year PV (not use simple annuity formula) unless using the growing annuity formula correctly. Each period's cash flow grows, then is discounted separately.

**When to Use:** Growing income streams, salary projections with annual increases, any multi-period valuation with different growth and discount rates.

**Procedure:**
1. **Growing Annuity Formula:** PV = PMT × [1 - ((1+g)/(1+r))^n] / (r - g), where g ≠ r
2. **Year-by-year approach (safer):** For each year t: PV_t = CF_0 × (1+g)^t / (1+r)^t
3. Identify: initial cash flow (CF_0), growth rate (g), discount rate (r), number of periods (n)
4. If g = r, use special case: PV = n × CF_0 / (1 + r)
5. Sum all individual PV amounts
6. Verify: later years should have smaller PV due to discounting

**Code Example:**

**Scenario:** Calculate PV of 20-year salary stream. Starting salary $150k, growing 3.5%/year, discount rate 6%. Need PV of after-tax portion (assume 32% tax rate).

**Correct Code:**
```python
# Parameters
initial_salary = 150_000
growth_rate = 0.035
discount_rate = 0.06
years = 20
tax_rate = 0.32

# Calculate after-tax initial salary
initial_after_tax_salary = initial_salary * (1 - tax_rate)

# Method 1: Year-by-year calculation (most reliable)
pv_salary_stream = 0
for year in range(1, years + 1):
    # Salary in future year (grows each year)
    future_salary = initial_after_tax_salary * ((1 + growth_rate) ** year)
    
    # Discount back to present
    pv_of_year = future_salary / ((1 + discount_rate) ** year)
    
    pv_salary_stream += pv_of_year

# Method 2: Growing annuity formula (use only if g ≠ r)
# PV = PMT × [1 - ((1+g)/(1+r))^n] / (r - g)
if growth_rate != discount_rate:
    pv_formula = initial_after_tax_salary * (
        (1 - ((1 + growth_rate) / (1 + discount_rate)) ** years) / 
        (discount_rate - growth_rate)
    )
else:
    # Special case when g = r
    pv_formula = years * initial_after_tax_salary / (1 + discount_rate)

# Both methods should give same result
round(pv_salary_stream, 0)
```

**Common Bugs to Avoid:**
- Using ordinary annuity formula when cash flows grow
- Applying growth rate incorrectly (compounding from year 0 instead of year 1)
- Confusing growth rate with discount rate in the formula
- Not handling the special case when g = r (formula breaks down)
- Starting loop at year 0 instead of year 1 for future cash flows
- Forgetting to apply tax rate or other adjustments before calculating PV

---

## Pattern: Asset Allocation Percentage Verification

**Description:** Before performing calculations with asset allocation percentages, verify they sum to 100% (or very close). Misreading allocation tables or using wrong values can cascade through all subsequent calculations.

**When to Use:** Any problem involving portfolio allocation, asset class weights, rebalancing scenarios, liability calculations based on asset values.

**Procedure:**
1. Extract all asset allocation percentages from exhibits/tables
2. Sum all percentages and verify total ≈ 100% (allow for rounding)
3. If total ≠ 100%, check for missing asset classes or misread values
4. Calculate dollar values: Asset Value = Total Portfolio × Allocation %
5. Use dollar values (not percentages) for subsequent calculations
6. Cross-check: sum of all asset dollar values should equal total portfolio value

**Code Example:**

**Scenario:** Portfolio $3B with allocations: Equities 42%, Bonds 28%, Alternatives 22%, Cash 8%. Calculate value of alternatives and verify total.

**Correct Code:**
```python
# Portfolio parameters
total_portfolio_value = 3_000_000_000

# Asset allocations (from exhibit)
equities_allocation = 0.42
bonds_allocation = 0.28
alternatives_allocation = 0.22
cash_allocation = 0.08

# STEP 1: Verify allocations sum to 100%
total_allocation = (equities_allocation + bonds_allocation + 
                   alternatives_allocation + cash_allocation)

# Check if total is approximately 1.0 (100%)
allocation_check = abs(total_allocation - 1.0) < 0.01  # Allow 1% tolerance

if not allocation_check:
    # Flag potential data error
    allocation_error = f"Warning: Allocations sum to {total_allocation*100:.1f}%"
else:
    allocation_error = "Allocations verified"

# STEP 2: Calculate dollar values
equities_value = total_portfolio_value * equities_allocation
bonds_value = total_portfolio_value * bonds_allocation
alternatives_value = total_portfolio_value * alternatives_allocation
cash_value = total_portfolio_value * cash_allocation

# STEP 3: Verify sum of values equals total
calculated_total = equities_value + bonds_value + alternatives_value + cash_value
value_check = abs(calculated_total - total_portfolio_value) < 1000  # Allow rounding

# Return alternatives value in millions
alternatives_value / 1_000_000
```

**Common Bugs to Avoid:**
- Not verifying allocation percentages sum to 100% before calculations
- Misreading decimal vs percentage (0.42 vs 42%)
- Using outdated "current" allocation instead of "target" allocation (or vice versa)
- Forgetting to include all asset classes listed in the exhibit
- Rounding errors when converting between percentages and decimals
- Not cross-checking that calculated asset values sum to total portfolio value