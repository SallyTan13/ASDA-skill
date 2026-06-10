Based on the comprehensive analysis of the failure cases, I'll outline the key skill patterns:

## Pattern: Multi-Step Financial Calculation Decomposition

**Description:** Complex financial calculations require systematic decomposition into clear, sequential steps with explicit intermediate calculations and careful tracking of financial parameters.

**When to Use:** Questions involving net wealth, life insurance needs, portfolio returns, or multi-variable financial modeling

**Procedure:**
1. Identify all input variables
2. Create systematic calculation workflow
3. Break complex calculations into modular steps
4. Apply appropriate financial formulas
5. Verify intermediate and final results

**Code Example:**
```python
def calculate_net_wealth(assets, liabilities):
    # Systematic asset tracking
    total_assets = sum([
        assets['liquid_cash'],
        assets['investments'],
        assets['real_estate'],
        assets['retirement_accounts']
    ])
    
    # Systematic liability tracking
    total_liabilities = sum([
        liabilities['mortgage'],
        liabilities['credit_lines'],
        liabilities['loans']
    ])
    
    # Clear net wealth calculation
    net_wealth = total_assets - total_liabilities
    
    return net_wealth
```

**Common Bugs to Avoid:**
- Skipping intermediate calculation steps
- Not handling different asset/liability types
- Forgetting to convert units
- Ignoring tax implications

## Pattern: Discounted Cash Flow (DCF) Systematic Calculation

**Description:** Investment project evaluation requires consistent methodology for converting future cash flows to present value using a standard discount rate.

**When to Use:** NPV, IRR calculations, project selection scenarios

**Procedure:**
1. Extract all cash flows by year
2. Apply consistent discount rate
3. Discount each cash flow individually
4. Sum discounted cash flows
5. Compare project values

**Code Example:**
```python
def calculate_npv(cash_flows, discount_rate):
    # Validate inputs
    assert len(cash_flows) > 0, "Cash flow list cannot be empty"
    
    # Systematic discounting
    discounted_flows = [
        flow / ((1 + discount_rate) ** year) 
        for year, flow in enumerate(cash_flows)
    ]
    
    # Sum discounted cash flows
    net_present_value = sum(discounted_flows)
    
    return net_present_value
```

**Common Bugs to Avoid:**
- Incorrect discount rate application
- Mishandling initial investment (year 0)
- Not accounting for project constraints
- Ignoring sign conventions for cash flows

## Pattern: Portfolio Return Weighted Calculation

**Description:** Portfolio-level returns require weighted averaging across different account types with distinct tax treatments.

**When to Use:** Multi-account portfolio return calculations with varying tax implications

**Procedure:**
1. Identify account types and values
2. Calculate pre-tax returns for each account
3. Apply tax adjustments
4. Weight returns by account value
5. Compute portfolio-level return

**Code Example:**
```python
def calculate_portfolio_return(accounts):
    # Systematic return calculation
    weighted_returns = [
        account['value'] * (
            account['pre_tax_return'] * (1 - account['tax_rate'])
        )
        for account in accounts
    ]
    
    total_portfolio_value = sum(
        account['value'] for account in accounts
    )
    
    portfolio_return = sum(weighted_returns) / total_portfolio_value
    
    return portfolio_return
```

**Common Bugs to Avoid:**
- Forgetting tax adjustments
- Incorrect weighting
- Not handling different account types
- Ignoring account-specific tax rules

## Pattern: Human Capital Valuation Method

**Description:** Life insurance needs calculation requires projecting future income streams, accounting for taxes, expenses, and applying appropriate discounting.

**When to Use:** Life insurance coverage determination for income-generating professionals

**Procedure:**
1. Project future earnings
2. Apply tax adjustments
3. Subtract family expenses
4. Discount projected cash flows
5. Determine insurance coverage gap

**Code Example:**
```python
def calculate_life_insurance_need(
    annual_income, 
    years_to_retirement, 
    tax_rate, 
    annual_expenses,
    discount_rate
):
    # Project future earnings
    future_earnings = [
        annual_income * (1.03 ** year) * (1 - tax_rate)
        for year in range(years_to_retirement)
    ]
    
    # Subtract annual expenses
    net_earnings = [
        max(earning - annual_expenses, 0)
        for earning in future_earnings
    ]
    
    # Discount net earnings
    discounted_earnings = [
        flow / ((1 + discount_rate) ** year)
        for year, flow in enumerate(net_earnings)
    ]
    
    total_insurance_need = sum(discounted_earnings)
    
    return total_insurance_need
```

**Common Bugs to Avoid:**
- Oversimplifying income projection
- Ignoring tax implications
- Not accounting for family expenses
- Using incorrect discount rates

These patterns provide systematic approaches to solving complex financial calculations by breaking down problems into clear, modular steps with explicit calculation methodologies.