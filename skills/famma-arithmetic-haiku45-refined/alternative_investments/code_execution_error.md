# SKILL PATTERNS FOR ALTERNATIVE INVESTMENTS (Program of Thought)

## Pattern: Output Verification and Answer Extraction

**Description:** Code may execute correctly and produce the right values, but the final answer extraction logic fails to properly select or return the correct result, leading to a mismatch between computed values and the stated answer.

**When to Use:** Any question requiring selection between alternatives (mutually exclusive projects, optimal choices) where comparison logic determines the final answer.

**Procedure:**
1. Compute all candidate values (NPVs, IRRs, etc.)
2. Store results in clearly labeled variables with descriptive names
3. Implement comparison logic explicitly with comments
4. Return BOTH the computed values AND the selection result
5. Verify the selection logic matches the decision criterion (e.g., "higher NPV is better")

**Code Example:**

**Scenario:** Compare two investment options with different cash flows. Option A has NPV of $45,000 and Option B has NPV of $52,000. Select the better option.

**Correct Code:**
```python
# Calculate NPVs (assume already computed)
npv_option_a = 45000
npv_option_b = 52000

# Store results with clear labels
results = {
    'Option A NPV': npv_option_a,
    'Option B NPV': npv_option_b
}

# Explicit comparison with decision rule
# Rule: Select option with HIGHER NPV
if npv_option_a > npv_option_b:
    selected_option = "Option A"
    selected_npv = npv_option_a
else:
    selected_option = "Option B"
    selected_npv = npv_option_b

# Return both computed values and selection for verification
{
    'NPV_Option_A': npv_option_a,
    'NPV_Option_B': npv_option_b,
    'Selected_Option': selected_option,
    'Selected_NPV': selected_npv,
    'Reason': f"{selected_option} has higher NPV"
}
```

**Common Bugs to Avoid:**
- Inverting comparison logic (using `<` instead of `>` for maximization)
- Hardcoding answer before comparison executes
- Returning only the selection without showing computed values for verification
- Using ambiguous variable names that don't clearly map to answer choices
- Failing to validate that the returned answer matches the comparison result

---

## Pattern: Depreciation Tax Shield in Operating Cash Flow

**Description:** When calculating operating cash flows for capital budgeting, the depreciation tax shield (Depreciation × Tax Rate) must be added to after-tax operating income, as depreciation is a non-cash expense that reduces taxable income.

**When to Use:** NPV calculations, project valuation, abandonment analysis, or any capital budgeting problem involving depreciation and taxes.

**Procedure:**
1. Formula: OCF = (Revenue - Cash Costs - Depreciation) × (1 - Tax Rate) + Depreciation
2. Alternative Formula: OCF = (Revenue - Cash Costs) × (1 - Tax Rate) + Depreciation × Tax Rate
3. Calculate annual depreciation (straight-line: Initial Investment / Project Life)
4. Compute EBIT = Revenue - Cash Costs - Depreciation
5. Calculate after-tax EBIT = EBIT × (1 - Tax Rate)
6. Add back depreciation to get operating cash flow
7. Verify that depreciation appears in both tax calculation and cash flow adjustment

**Code Example:**

**Scenario:** A project requires $200,000 initial investment, depreciated straight-line over 5 years. Annual revenue is $120,000, operating costs are $50,000, tax rate is 35%, discount rate is 12%.

**Correct Code:**
```python
# Project parameters
initial_investment = 200000
project_life = 5
annual_revenue = 120000
annual_operating_costs = 50000
tax_rate = 0.35
discount_rate = 0.12

# Calculate annual depreciation
annual_depreciation = initial_investment / project_life

# Method 1: Traditional OCF calculation
ebit = annual_revenue - annual_operating_costs - annual_depreciation
tax_on_ebit = ebit * tax_rate
net_income = ebit - tax_on_ebit
operating_cash_flow = net_income + annual_depreciation

# Method 2: Alternative formula (should give same result)
ocf_alternative = ((annual_revenue - annual_operating_costs) * (1 - tax_rate) + 
                   annual_depreciation * tax_rate)

# Verify both methods match
assert abs(operating_cash_flow - ocf_alternative) < 0.01, "OCF calculation mismatch"

# Calculate NPV
npv = -initial_investment
for year in range(1, project_life + 1):
    npv += operating_cash_flow / (discount_rate + 1) ** year

{
    'Annual_Depreciation': annual_depreciation,
    'EBIT': ebit,
    'Net_Income': net_income,
    'Depreciation_Tax_Shield': annual_depreciation * tax_rate,
    'Operating_Cash_Flow': operating_cash_flow,
    'NPV': round(npv, 2)
}
```

**Common Bugs to Avoid:**
- Forgetting to add back depreciation after calculating after-tax income
- Treating depreciation as a cash outflow (it's non-cash)
- Omitting depreciation from EBIT calculation (needed for correct taxes)
- Double-counting depreciation tax benefit
- Using book depreciation for cash flow instead of tax depreciation

---

## Pattern: Terminal Value with Asset Sale and Tax Effects

**Description:** When a project ends (including early abandonment), terminal cash flow includes asset sale proceeds, tax on gain/loss from sale, and recovery of net working capital. Book value must be tracked to calculate taxable gain.

**When to Use:** Abandonment option analysis, project termination scenarios, salvage value calculations, or any problem involving asset disposal.

**Procedure:**
1. Formula: Terminal CF = Sale Proceeds - Tax on Gain + NWC Recovery
2. Calculate book value at disposal: Initial Cost - Accumulated Depreciation
3. Calculate gain/loss on sale: Market Value - Book Value
4. Calculate tax effect: (Market Value - Book Value) × Tax Rate
5. After-tax sale proceeds: Market Value - Tax on Gain (or + Tax Benefit if loss)
6. Add recovered net working capital (fully recoverable)
7. Discount terminal value to present at the appropriate year

**Code Example:**

**Scenario:** Equipment cost $300,000, depreciated straight-line over 4 years. After 2 years, market value is $180,000. NWC investment was $40,000. Tax rate is 30%.

**Correct Code:**
```python
# Asset and project parameters
initial_cost = 300000
project_life = 4
abandonment_year = 2
market_value_at_sale = 180000
nwc_investment = 40000
tax_rate = 0.30
discount_rate = 0.15

# Calculate depreciation and book value
annual_depreciation = initial_cost / project_life
accumulated_depreciation = annual_depreciation * abandonment_year
book_value_at_sale = initial_cost - accumulated_depreciation

# Calculate gain/loss on sale
gain_on_sale = market_value_at_sale - book_value_at_sale

# Calculate tax on gain (negative if loss, creating tax benefit)
tax_on_gain = gain_on_sale * tax_rate

# Calculate after-tax proceeds from sale
after_tax_sale_proceeds = market_value_at_sale - tax_on_gain

# Total terminal cash flow
terminal_cash_flow = after_tax_sale_proceeds + nwc_investment

# Present value of terminal cash flow
pv_terminal_cf = terminal_cash_flow / (1 + discount_rate) ** abandonment_year

{
    'Book_Value_at_Sale': book_value_at_sale,
    'Market_Value': market_value_at_sale,
    'Gain_on_Sale': gain_on_sale,
    'Tax_on_Gain': tax_on_gain,
    'After_Tax_Sale_Proceeds': after_tax_sale_proceeds,
    'NWC_Recovery': nwc_investment,
    'Total_Terminal_CF': terminal_cash_flow,
    'PV_Terminal_CF': round(pv_terminal_cf, 2)
}
```

**Common Bugs to Avoid:**
- Using market value as book value (ignoring accumulated depreciation)
- Forgetting to include tax effect on asset sale
- Treating all asset sales as taxable gains (losses create tax benefits)
- Omitting NWC recovery from terminal cash flow
- Discounting terminal value by wrong number of periods
- Using wrong depreciation method to calculate book value

---

## Pattern: Abandonment Option NPV Comparison

**Description:** When evaluating optimal project life with abandonment options, calculate NPV for each possible termination year, including operating cash flows up to that year plus terminal value, then select the year with maximum NPV.

**When to Use:** Questions about optimal economic life, abandonment analysis, or when market values are provided for multiple years.

**Procedure:**
1. Create a function to calculate NPV given abandonment year
2. For each potential abandonment year: sum discounted operating CFs + discounted terminal value
3. Terminal value includes: after-tax sale proceeds + NWC recovery
4. Store NPV for each abandonment scenario in a dictionary
5. Identify maximum NPV and corresponding optimal year
6. Return all NPVs for transparency and verification

**Code Example:**

**Scenario:** Project with 3-year life, initial investment $100,000, NWC $15,000, annual OCF $45,000, discount rate 10%. Market values: Year 1: $80,000, Year 2: $55,000, Year 3: $20,000. Tax rate 25%.

**Correct Code:**
```python
# Project parameters
initial_investment = 100000
nwc = 15000
annual_ocf = 45000
discount_rate = 0.10
tax_rate = 0.25
max_life = 3

# Market values at each year-end
market_values = {1: 80000, 2: 55000, 3: 20000}

# Depreciation schedule (straight-line over max life)
annual_depreciation = initial_investment / max_life

def calculate_npv_with_abandonment(abandon_year):
    """Calculate NPV if project is abandoned at specified year"""
    # Initial outlay
    npv = -(initial_investment + nwc)
    
    # Operating cash flows for years 1 to abandon_year
    for year in range(1, abandon_year + 1):
        npv += annual_ocf / (1 + discount_rate) ** year
    
    # Terminal value at abandonment year
    book_value = initial_investment - (annual_depreciation * abandon_year)
    market_value = market_values[abandon_year]
    gain_on_sale = market_value - book_value
    tax_on_gain = gain_on_sale * tax_rate
    terminal_cf = market_value - tax_on_gain + nwc
    
    npv += terminal_cf / (1 + discount_rate) ** abandon_year
    
    return npv

# Calculate NPV for each abandonment option
npv_results = {}
for year in range(1, max_life + 1):
    npv_results[year] = calculate_npv_with_abandonment(year)

# Find optimal abandonment year
optimal_year = max(npv_results, key=npv_results.get)
max_npv = npv_results[optimal_year]

{
    'NPV_Abandon_Year_1': round(npv_results[1], 2),
    'NPV_Abandon_Year_2': round(npv_results[2], 2),
    'NPV_Abandon_Year_3': round(npv_results[3], 2),
    'Optimal_Economic_Life': optimal_year,
    'Maximum_NPV': round(max_npv, 2)
}
```

**Common Bugs to Avoid:**
- Forgetting to include initial investment and NWC in Year 0 cash flow
- Omitting operating cash flows before abandonment
- Incorrectly calculating book value at different abandonment years
- Not updating accumulated depreciation based on abandonment year
- Failing to discount terminal value to present
- Using same terminal value for all abandonment scenarios