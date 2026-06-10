# SKILL PATTERNS: Unit/Currency/Percent Conversion Errors in Alternative Investments (PoT)

## Pattern: Multi-Account Portfolio Accrual Equivalent Return Aggregation

**Description:** When computing portfolio-level after-tax returns across accounts with different tax treatments (taxable, tax-deferred, tax-exempt), must correctly convert tax-deferred accounts to accrual equivalent basis using the formula r* = (1+r(1-t_cg))^(1/n) - 1, then weight by account values.

**When to Use:** Questions involving portfolio returns with mixed tax treatment accounts, retirement accounts with deferred taxation, or accrual equivalent return calculations.

**Procedure:**
1. Formula: r_portfolio = Σ(w_i × r_i*) where r_i* is the accrual equivalent return for account i
2. For taxable accounts: r* = r × (1 - t_annual)
3. For tax-deferred accounts: r* = (1 + r(1 - t_cg))^(1/n) - 1, where n is deferral period
4. For tax-exempt accounts: r* = r (no adjustment)
5. Calculate weights: w_i = value_i / total_portfolio_value
6. Return weighted sum as decimal (not percentage)

**Code Example:**

**Scenario:** Portfolio with $800k taxable (10% pre-tax return, 25% annual tax), $500k tax-deferred (6% pre-tax return, 35% capital gains tax, 10-year deferral), $200k tax-exempt (9% return). Calculate accrual equivalent return.

**Correct Code:**
```python
# Account values
taxable_value = 800_000
tax_deferred_value = 500_000
tax_exempt_value = 200_000
total_value = taxable_value + tax_deferred_value + tax_exempt_value

# Returns and tax rates
taxable_return = 0.10
taxable_annual_tax = 0.25
tax_deferred_return = 0.06
tax_deferred_cg_tax = 0.35
deferral_years = 10
tax_exempt_return = 0.09

# Step 1: Calculate accrual equivalent returns
taxable_accrual = taxable_return * (1 - taxable_annual_tax)
tax_deferred_accrual = (1 + tax_deferred_return * (1 - tax_deferred_cg_tax)) ** (1 / deferral_years) - 1
tax_exempt_accrual = tax_exempt_return

# Step 2: Calculate weights
weight_taxable = taxable_value / total_value
weight_tax_deferred = tax_deferred_value / total_value
weight_tax_exempt = tax_exempt_value / total_value

# Step 3: Weighted average
portfolio_return = (weight_taxable * taxable_accrual + 
                   weight_tax_deferred * tax_deferred_accrual + 
                   weight_tax_exempt * tax_exempt_accrual)

portfolio_return  # Result as decimal: ~0.0728
```

**Common Bugs to Avoid:**
- Using simple average instead of weighted average by account values
- Applying wrong formula for tax-deferred: using r*(1-t) instead of (1+r(1-t))^(1/n)-1
- Forgetting to convert final result from decimal to percentage when comparing to options
- Mixing up annual tax rate with capital gains tax rate for different account types
- Using n as total years instead of deferral period for accrual equivalent calculation

---

## Pattern: Human Life Value Present Value with Multi-Component Cash Flows

**Description:** Human life value calculation requires computing present value of future income streams with growth, subtracting expenses, adding employer contributions, then subtracting existing coverage. Must handle percentage-based components correctly and apply discount rate to net cash flows.

**When to Use:** Life insurance needs analysis, human capital valuation, questions mentioning "human life value method" or calculating insurance coverage gaps.

**Procedure:**
1. Formula: Additional Insurance = PV(Net Income Stream) - Existing Coverage
2. Net annual cash flow = Gross Income × (1 - Tax Rate) + Employer Contribution - Attributable Expenses
3. For growing annuity: PV = CF₁ × [(1 - ((1+g)/(1+r))^n) / (r - g)] where g = growth rate, r = discount rate
4. Employer contribution = Gross Income × Contribution Rate
5. Subtract existing life insurance death benefit
6. Return result in same units as income (dollars, not percentages)

**Code Example:**

**Scenario:** Individual age 45, retiring at 60 (15 years). Current income $200k growing 2.5%/year, taxes 28%, employer adds 6% to pension, personal expenses $25k/year, discount rate 5%, existing $300k insurance. Calculate additional insurance needed.

**Correct Code:**
```python
# Input parameters
current_income = 200_000
years_to_retirement = 15
growth_rate = 0.025
tax_rate = 0.28
employer_contribution_rate = 0.06
annual_expenses = 25_000
discount_rate = 0.05
existing_insurance = 300_000

# Step 1: Calculate first year net cash flow
after_tax_income = current_income * (1 - tax_rate)
employer_contribution = current_income * employer_contribution_rate
net_cash_flow_year1 = after_tax_income + employer_contribution - annual_expenses

# Step 2: Present value of growing annuity
# PV = CF1 * [(1 - ((1+g)/(1+r))^n) / (r - g)]
growth_factor = (1 + growth_rate) / (1 + discount_rate)
pv_factor = (1 - growth_factor ** years_to_retirement) / (discount_rate - growth_rate)
pv_income_stream = net_cash_flow_year1 * pv_factor

# Step 3: Subtract existing coverage
additional_insurance_needed = pv_income_stream - existing_insurance

additional_insurance_needed  # Result in dollars: ~1,876,543
```

**Common Bugs to Avoid:**
- Forgetting to add employer contributions to net cash flow (it's part of human capital value)
- Applying tax rate to employer contributions (they go directly to pension, pre-tax)
- Using simple annuity formula instead of growing annuity when income grows
- Subtracting expenses from gross income before applying tax rate (tax applies to gross)
- Not subtracting existing insurance coverage from the calculated present value
- Confusing discount rate with after-tax discount rate (use stated rate unless specified)

---

## Pattern: Multi-Component Liability Aggregation with Percentage-Based Calculations

**Description:** When calculating total liabilities from multiple sources (spending requirements, capital calls, distributions), must correctly identify base values for percentage calculations and ensure all components use consistent units before summation.

**When to Use:** Endowment spending calculations, capital call projections, liquidity needs analysis, questions asking for "total liabilities" or "next 12-month obligations."

**Procedure:**
1. Formula: Total Liabilities = Spending + Capital Calls + Other Obligations
2. Identify base value for each percentage (portfolio value, asset class value, trailing average)
3. Spending rate: typically applied to total portfolio value or trailing average
4. Capital calls: applied only to private/illiquid asset classes (private equity, private real estate)
5. Sum all components in same currency units
6. Verify each component's base is correctly identified from context

**Code Example:**

**Scenario:** Endowment worth $2 billion. Spending rate 5% of portfolio. Private equity 25% of portfolio, private real estate 12% of portfolio, capital calls expected at 18% of private assets NAV. Calculate total 12-month liabilities.

**Correct Code:**
```python
# Portfolio parameters
total_portfolio_value = 2_000_000_000
spending_rate = 0.05

# Private asset allocations
private_equity_allocation = 0.25
private_real_estate_allocation = 0.12
capital_call_rate = 0.18

# Step 1: Calculate spending requirement
spending_liability = total_portfolio_value * spending_rate

# Step 2: Calculate private assets value
private_equity_value = total_portfolio_value * private_equity_allocation
private_real_estate_value = total_portfolio_value * private_real_estate_allocation
total_private_assets = private_equity_value + private_real_estate_value

# Step 3: Calculate capital calls (applied to private assets only)
capital_call_liability = total_private_assets * capital_call_rate

# Step 4: Sum all liabilities
total_liabilities = spending_liability + capital_call_liability

total_liabilities  # Result in dollars: 233,200,000
```

**Common Bugs to Avoid:**
- Applying capital call rate to total portfolio instead of only private asset classes
- Missing asset classes when identifying private investments (must include both PE and real estate)
- Using current portfolio value when spending is based on trailing average (read context carefully)
- Forgetting to convert percentages to decimals before multiplication
- Adding percentages directly instead of computing dollar amounts first
- Including liquid assets in capital call calculations (only applies to private/illiquid investments)
- Returning result in wrong units (millions vs. dollars) relative to answer choices

---

## Pattern: Stress Scenario Portfolio Return with Heterogeneous Asset Classes

**Description:** When calculating expected portfolio return under stress scenarios, must apply asset-specific returns to their allocation weights, handling both positive and negative returns correctly, and ensuring final result matches the requested format (decimal vs. percentage).

**When to Use:** Stress testing, scenario analysis, portfolio expected return calculations with given asset class returns, CVaR or risk metric computations.

**Procedure:**
1. Formula: E(R_portfolio) = Σ(w_i × r_i) where w_i is allocation weight, r_i is expected return
2. Extract allocation weights ensuring they sum to 1.0 (or 100%)
3. Match each asset class to its stress scenario return (may be negative)
4. Multiply each weight by its return (preserve sign)
5. Sum all products to get portfolio-level return
6. Return as decimal unless percentage explicitly requested

**Code Example:**

**Scenario:** Portfolio: 40% stocks (stress return -5%), 30% bonds (stress return 2%), 20% alternatives (stress return -3%), 10% cash (stress return 1.5%). Calculate expected portfolio return under stress.

**Correct Code:**
```python
# Asset allocations (must sum to 1.0)
allocation_stocks = 0.40
allocation_bonds = 0.30
allocation_alternatives = 0.20
allocation_cash = 0.10

# Stress scenario returns (as decimals, can be negative)
return_stocks = -0.05
return_bonds = 0.02
return_alternatives = -0.03
return_cash = 0.015

# Step 1: Verify allocations sum to 1.0
total_allocation = allocation_stocks + allocation_bonds + allocation_alternatives + allocation_cash
assert abs(total_allocation - 1.0) < 0.001, "Allocations must sum to 1.0"

# Step 2: Calculate weighted returns
portfolio_return = (allocation_stocks * return_stocks +
                   allocation_bonds * return_bonds +
                   allocation_alternatives * return_alternatives +
                   allocation_cash * return_cash)

portfolio_return  # Result as decimal: -0.0145 (i.e., -1.45%)
```

**Common Bugs to Avoid:**
- Treating negative returns as positive (sign errors in stress scenarios)
- Using allocation percentages (e.g., 40) instead of decimals (0.40) in multiplication
- Forgetting to include all asset classes in the calculation
- Mismatching asset class names between allocation table and return table
- Converting to percentage prematurely (multiply by 100 only if answer choices are in %)
- Not verifying that allocation weights sum to 100% or 1.0 before calculation

---

## Pattern: Tax-Adjusted Real Estate Cash Flow with Multiple Tax Jurisdictions

**Description:** When calculating after-tax cash flows from international real estate with multiple tax regimes (income tax, capital gains, wealth tax), must apply deduction vs. credit methods correctly and accumulate wealth taxes over holding period.

**When to Use:** Cross-border real estate investments, questions involving multiple tax jurisdictions, deduction method vs. credit method for tax relief, wealth tax calculations.

**Procedure:**
1. Formula: After-tax income = Gross Income × (1 - t_foreign) × (1 - t_domestic) for deduction method
2. Formula: After-tax income = Gross Income × (1 - max(t_foreign, t_domestic)) for credit method
3. For wealth tax: accumulate annually based on cost basis, pay at sale
4. For capital gains: apply both jurisdictions' rates using specified relief method
5. Accumulated wealth tax = Annual Rate × Cost Basis × Years Held
6. Return net proceeds after all taxes

**Code Example:**

**Scenario:** Property cost basis $5M, current value $6M, annual income $400k. Foreign taxes: 30% income, 15% capital gains, 2% annual wealth tax on cost. Domestic taxes: 25% income, 20% capital gains. Deduction method for income, credit method for gains. Held 8 years, then sold. Calculate after-tax sale proceeds.

**Correct Code:**
```python
# Property parameters
cost_basis = 5_000_000
sale_price = 6_000_000
capital_gain = sale_price - cost_basis
years_held = 8

# Tax rates
foreign_income_tax = 0.30
domestic_income_tax = 0.25
foreign_cg_tax = 0.15
domestic_cg_tax = 0.20
foreign_wealth_tax_annual = 0.02

# Step 1: Calculate accumulated wealth tax (paid at sale)
accumulated_wealth_tax = foreign_wealth_tax_annual * cost_basis * years_held

# Step 2: Calculate capital gains tax (credit method - use maximum rate)
effective_cg_tax_rate = max(foreign_cg_tax, domestic_cg_tax)
capital_gains_tax = capital_gain * effective_cg_tax_rate

# Step 3: Calculate total taxes at sale
total_taxes_at_sale = accumulated_wealth_tax + capital_gains_tax

# Step 4: Net proceeds after tax
net_sale_proceeds = sale_price - total_taxes_at_sale

net_sale_proceeds  # Result: 5,000,000
```

**Common Bugs to Avoid:**
- Using credit method formula when deduction method is specified (or vice versa)
- Applying wealth tax to market value instead of cost basis
- Forgetting to accumulate wealth tax over entire holding period
- Paying wealth tax annually instead of at sale (read problem carefully)
- Adding tax rates instead of using max() for credit method
- Applying deduction method as (1 - t1 - t2) instead of (1 - t1)(1 - t2)
- Not distinguishing between income tax treatment and capital gains tax treatment

</budget:token_budget>