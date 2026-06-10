# SKILL PATTERNS: Unit/Currency/Percent Conversion Errors in Alternative Investments (PoT)

## Pattern: Multi-Account Portfolio Accrual Equivalent Return Aggregation

**Description:** When computing portfolio-level after-tax returns across accounts with different tax treatments (taxable, tax-deferred, tax-exempt), must correctly convert tax-deferred accounts to accrual equivalent basis. The accrual equivalent return represents the constant annual return that would produce the same after-tax terminal wealth as the tax-deferred account. Critical: the tax-deferred formula must account for growth at the full pre-tax rate with tax only at the end. **After calculation, compare result to answer options and select the closest match.**

**When to Use:** Questions involving portfolio returns with mixed tax treatment accounts, retirement accounts with deferred taxation, or accrual equivalent return calculations.

**When NOT to Use:**
- Single account type portfolios (no need for accrual equivalent conversion)
- Questions asking for simple weighted average returns without tax considerations
- Pre-tax return calculations

**Procedure:**
1. Formula: r_portfolio = Σ(w_i × r_i*) where r_i* is the accrual equivalent return for account i
2. For taxable accounts: r* = r × (1 - t_annual)
3. For tax-deferred accounts: r* = [(1 + r)^n × (1 - t_distribution)]^(1/n) - 1, where n is deferral period
   - This accounts for growth at rate r each year, with tax t_distribution applied only at distribution
   - The formula structure: (Future Value after tax)^(1/n) - 1
   - NOT: (1 + r × (1 - t))^(1/n) - 1 (this incorrectly applies tax to annual returns)
4. For tax-exempt accounts: r* = r (no adjustment)
5. Calculate weights: w_i = value_i / total_portfolio_value
6. Calculate weighted sum as decimal
7. **Convert to percentage if answer options are in percentage format (multiply by 100)**
8. **Compare calculated result to answer options and select the closest match**
9. Validation: tax-deferred accrual equivalent should be between taxable rate and pre-tax rate

**Example (sanitized):**

> **Scenario:** Portfolio with three accounts: $600k taxable account (8% pre-tax return, 30% annual tax), $400k tax-deferred account (9% pre-tax return, 25% capital gains tax, 15-year deferral), $300k tax-exempt account (7% return). Calculate accrual equivalent return. Answer options: A. 6.2%, B. 6.4%, C. 6.6%
>
> **Wrong approach:** Returning raw decimal without selecting answer
> - Calculate: 0.0636
> - Return: 0.0636 (fails to match to options)
>
> **Correct approach:**
> 1. Taxable account accrual equivalent: r* = 0.08 × (1 - 0.30) = 0.056 or 5.6%
> 2. Tax-deferred account accrual equivalent:
>    - Future value factor: (1.09)^15 = 3.6425
>    - After-tax terminal value factor: 3.6425 × (1 - 0.25) = 2.7319
>    - Accrual equivalent: 2.7319^(1/15) - 1 = 0.0701 or 7.01%
> 3. Tax-exempt account accrual equivalent: r* = 0.07 or 7%
> 4. Calculate weights: w_taxable = 0.4615, w_deferred = 0.3077, w_exempt = 0.2308
> 5. Weighted average: 0.4615 × 0.056 + 0.3077 × 0.0701 + 0.2308 × 0.07 = 0.0636
> 6. Convert to percentage: 6.36%
> 7. **Compare to options: |6.36 - 6.2| = 0.16, |6.36 - 6.4| = 0.04, |6.36 - 6.6| = 0.24**
> 8. **Select closest: Option B (6.4%)**

**Common Mistakes to Avoid:**
- Using r*(1-t) as the growth rate instead of recognizing tax is deferred to the end
- Formula error: (1 + r(1-t))^(1/n) - 1 instead of [(1+r)^n × (1-t)]^(1/n) - 1
- Not validating that tax-deferred accrual equivalent falls between taxable and pre-tax rates
- Using simple average instead of weighted average by account values
- Mixing up annual tax rate with capital gains tax rate for different account types
- **Returning raw calculated value without comparing to answer options**
- **Not converting to percentage when answer options are in percentage format**
- Applying the distribution tax rate to the annual return instead of to the final accumulated value

---
## Pattern: Human Life Value Present Value with Multi-Component Cash Flows

**Description:** Human life value calculation requires computing present value of future income streams with growth, subtracting expenses, adding employer contributions, then subtracting existing coverage. Use the **standard human life value method**: calculate PV of after-tax earnings attributable to dependents, add employer pension contributions, subtract existing insurance. Do NOT include survival probabilities, occupational volatility adjustments, or separate financial goals (education, vacation homes) unless explicitly required by the question.

**When to Use:** Life insurance needs analysis, human capital valuation, questions mentioning "human life value method" or calculating insurance coverage gaps.

**When NOT to Use:**
- Questions asking for needs analysis method (different from human life value method)
- Estate planning questions focused on wealth transfer rather than income replacement
- Questions that explicitly request inclusion of specific financial goals beyond income replacement

**Procedure:**
1. Formula: Additional Insurance = PV(Net Income Stream) - Existing Coverage
2. Net annual cash flow = [Gross Income × (1 - Tax Rate) - Personal Expenses Attributable to Insured] + Employer Contribution
3. For growing annuity: PV = CF₁ × [(1 - ((1+g)/(1+r))^n) / (r - g)] where g = growth rate, r = discount rate
4. Employer contribution = Gross Income × Contribution Rate (added to net cash flow, not taxed)
5. If tax on insurance proceeds investment income is mentioned:
   - Adjust discount rate: r_after_tax = r × (1 - t_proceeds)
   - This reflects that proceeds will be invested and earnings taxed
6. Subtract existing life insurance death benefit
7. **Do NOT include**: survival probabilities, occupational volatility, separate financial goals (education, vacation, charitable donations) unless question explicitly requires them
8. Return result in same units as income (dollars, not percentages)

**Example (sanitized):**

> **Scenario:** Individual age 40, retiring at 65 (25 years). Current income $150k growing 3%/year, taxes 25%, employer adds 8% to retirement plan, personal expenses $20k/year, discount rate 5%, existing $250k insurance. Tax on investment income from insurance proceeds is 18%. Calculate additional insurance needed using human life value method.
>
> **Wrong approach:** Adding complexity not in standard method
> - Include survival probabilities: 0.995 declining by 0.001/year
> - Add occupational volatility adjustment to discount rate
> - Include future obligations: $350k education + $325k vacation home + $400k charity
> - Result: Overly complex calculation deviating from standard method
>
> **Correct approach:**
> 1. Calculate first year net cash flow:
>    - After-tax income: $150,000 × (1 - 0.25) = $112,500
>    - Subtract personal expenses: $112,500 - $20,000 = $92,500
>    - Add employer contribution: $92,500 + ($150,000 × 0.08) = $104,500
> 2. Adjust discount rate for tax on insurance proceeds investment income:
>    - After-tax discount rate: 5% × (1 - 0.18) = 4.1%
> 3. Calculate PV using growing annuity formula:
>    - PV = $104,500 × [(1 - (1.03/1.041)^25) / (0.041 - 0.03)]
>    - PV = $104,500 × 22.89 = $2,392,005
> 4. Subtract existing coverage:
>    - Additional insurance = $2,392,005 - $250,000 = $2,142,005

**Common Mistakes to Avoid:**
- Adding survival probabilities or mortality adjustments (not part of standard human life value method)
- Including occupational volatility adjustments to discount rate
- Adding separate financial goals (education, vacation, charity) to insurance calculation
- Grossing up final insurance amount by dividing by (1 - tax_on_proceeds)
- Not distinguishing between tax on insurance proceeds vs. tax on investment income from proceeds
- Forgetting to add employer contributions to net cash flow
- Applying tax rate to employer contributions (they go directly to pension, pre-tax)
- Subtracting expenses from gross income before applying tax rate (tax applies to gross)
- **Overcomplicating with factors not specified in the human life value method**
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

**Description:** When calculating after-tax cash flows from international real estate with multiple tax regimes (income tax, capital gains, wealth tax), must apply deduction vs. credit methods correctly and accumulate wealth taxes over holding period. Critical: For income from property owned by residents of one country but located in another, BOTH jurisdictions may tax the income. The deduction method means the home country taxes the after-foreign-tax amount, NOT that foreign tax eliminates home country tax.

**When to Use:** Cross-border real estate investments, questions involving multiple tax jurisdictions, deduction method vs. credit method for tax relief, wealth tax calculations, annual lease income from foreign properties owned by residents of another country.

**When NOT to Use:** 
- Single jurisdiction real estate (no double taxation)
- Questions asking only about capital gains at sale (use capital gains procedures only)
- When the problem explicitly states tax treaties eliminate double taxation
- Domestic real estate with no foreign tax implications

**Procedure:**
1. **For annual income with deduction method:**
   - After-tax income = Gross Income × (1 - t_foreign) × (1 - t_domestic)
   - This applies BOTH taxes sequentially: foreign tax first, then domestic tax on the net
2. **For annual income with credit method:**
   - After-tax income = Gross Income × (1 - max(t_foreign, t_domestic))
   - Only the higher tax rate applies
3. **For wealth tax:** 
   - Accumulate annually based on cost basis
   - Pay at sale: Accumulated wealth tax = Annual Rate × Cost Basis × Years Held
4. **For capital gains with credit method:**
   - Apply max(t_foreign_cg, t_domestic_cg) to the gain
5. **For capital gains with deduction method:**
   - Apply both rates sequentially: Gain × (1 - t_foreign_cg) × (1 - t_domestic_cg)
6. **Verification checks:**
   - With deduction method, effective tax rate should be higher than either single rate
   - With credit method, effective tax rate equals the maximum of the two rates
   - Read problem carefully to identify which method applies to income vs. capital gains (may differ)

**Code Example:**

**Scenario:** Property cost basis $5M, current value $6M, annual income $400k. Foreign taxes: 30% income, 15% capital gains, 2% annual wealth tax on cost. Domestic taxes: 25% income, 20% capital gains. Deduction method for income, credit method for gains. Calculate: (a) annual after-tax income, (b) after-tax sale proceeds if held 8 years then sold.

**Wrong approach for annual income:**
```python
# WRONG: Only applying foreign tax, ignoring domestic tax
after_tax_income = 400_000 * (1 - 0.30)  # = 280,000
# This ignores that the owner is a domestic resident subject to domestic tax
```

**Correct Code:**
```python
# Property parameters
cost_basis = 5_000_000
current_value = 6_000_000
annual_income = 400_000
years_held = 8

# Tax rates
foreign_income_tax = 0.30
domestic_income_tax = 0.25
foreign_cg_tax = 0.15
domestic_cg_tax = 0.20
foreign_wealth_tax_annual = 0.02

# Part (a): Annual after-tax income (deduction method)
# Step 1: Apply foreign income tax first
after_foreign_tax = annual_income * (1 - foreign_income_tax)
# Step 2: Apply domestic tax to the after-foreign-tax amount
annual_after_tax_income = after_foreign_tax * (1 - domestic_income_tax)
# Equivalent: annual_income * (1 - 0.30) * (1 - 0.25) = 400,000 * 0.70 * 0.75 = 210,000

# Part (b): After-tax sale proceeds
# Step 1: Calculate capital gain
sale_price = current_value * 1.30  # Assume 30% appreciation
capital_gain = sale_price - cost_basis

# Step 2: Calculate accumulated wealth tax (paid at sale)
accumulated_wealth_tax = foreign_wealth_tax_annual * cost_basis * years_held

# Step 3: Calculate capital gains tax (credit method - use maximum rate)
effective_cg_tax_rate = max(foreign_cg_tax, domestic_cg_tax)
capital_gains_tax = capital_gain * effective_cg_tax_rate

# Step 4: Net proceeds after all taxes
total_taxes_at_sale = accumulated_wealth_tax + capital_gains_tax
net_sale_proceeds = sale_price - total_taxes_at_sale

annual_after_tax_income  # Result: 210,000
```

**Common Mistakes to Avoid:**
- **CRITICAL:** Applying only foreign tax on income when owner is resident of another country (must apply both with deduction method)
- Using credit method formula when deduction method is specified (or vice versa)
- Confusing which method applies: income may use deduction while capital gains use credit (read carefully)
- Applying wealth tax to market value instead of cost basis
- Forgetting to accumulate wealth tax over entire holding period
- Paying wealth tax annually in cash flow instead of at sale (read problem carefully)
- Adding tax rates instead of using max() for credit method
- Applying deduction method as (1 - t1 - t2) instead of (1 - t1)(1 - t2)
- Not distinguishing between income tax treatment and capital gains tax treatment
- Assuming foreign tax eliminates domestic tax obligation (only true with credit method at lower foreign rate)

---