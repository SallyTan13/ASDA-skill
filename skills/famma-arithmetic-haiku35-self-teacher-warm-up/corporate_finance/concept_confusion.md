Based on the comprehensive analysis of the failure cases, here are the key skill patterns:

## Pattern: Synergy Value Calculation

**Description:** Synergy value is not a simple arithmetic operation but requires understanding the incremental value created by combining firms beyond their individual market values.

**When to Use:** Merger and acquisition scenarios involving multiple firms with different financial metrics

**Procedure:**
1. Calculate individual firm market values
2. Estimate potential combined value
3. Subtract individual firm values
4. Consider strategic and operational benefits

**Code Example:**
```python
def calculate_synergy_value(firm1_value, firm1_shares, firm2_value, firm2_shares, strategic_premium=0):
    combined_market_value = (firm1_value + firm2_value)
    synergy_value = combined_market_value * (1 + strategic_premium) - (firm1_value + firm2_value)
    return synergy_value
```

**Common Bugs to Avoid:**
- Treating synergy as a direct numerical value
- Ignoring strategic considerations
- Simplistic addition of firm values

## Pattern: Interest Rate Conversion

**Description:** Effective Annual Rate (EAR) and Annual Percentage Rate (APR) have a specific mathematical relationship dependent on compounding frequency.

**When to Use:** Financial calculations involving interest rates with different compounding periods

**Procedure:**
1. Identify nominal rate (APR)
2. Determine compounding frequency
3. Apply standard conversion formula: EAR = (1 + APR/n)^n - 1
   Where n = number of compounding periods per year

**Code Example:**
```python
def calculate_ear(apr, compounding_periods):
    return (1 + apr/compounding_periods)**compounding_periods - 1
```

**Common Bugs to Avoid:**
- Assuming linear relationship between APR and EAR
- Incorrect compounding period calculation
- Not handling edge cases like infinite compounding

## Pattern: Merger Valuation NPV

**Description:** Merger Net Present Value (NPV) is not simply the synergy value, but requires comprehensive calculation considering acquisition costs, share prices, and incremental value.

**When to Use:** Evaluating potential corporate mergers and acquisitions

**Procedure:**
1. Calculate total acquisition cost
2. Estimate synergy benefits
3. Subtract acquisition cost from synergy benefits
4. Consider present value of future cash flows

**Code Example:**
```python
def calculate_merger_npv(bidder_shares, bidder_price, target_shares, target_price, synergy_value):
    acquisition_cost = bidder_shares * target_shares * target_price
    npv = synergy_value - acquisition_cost
    return npv
```

**Common Bugs to Avoid:**
- Equating synergy value with NPV
- Ignoring acquisition transaction costs
- Oversimplifying valuation calculations

## Pattern: Cash Flow to Investors

**Description:** Cash flows to investors encompass multiple financial transactions, not just dividend payments.

**When to Use:** Analyzing financial statements and investor returns

**Procedure:**
1. Aggregate all cash inflows to investors
2. Include stock issuance proceeds
3. Include dividend payments
4. Subtract any investor-related cash outflows

**Code Example:**
```python
def calculate_investor_cash_flows(stock_proceeds, dividends, stock_repurchases=0):
    return stock_proceeds + dividends - stock_repurchases
```

**Common Bugs to Avoid:**
- Considering only dividend payments
- Ignoring stock issuance
- Not accounting for stock repurchases

## Pattern: Debt Valuation in Merger

**Description:** Merged company debt value depends on combined firm's potential values across economic scenarios, not just original face value.

**When to Use:** Evaluating debt obligations during corporate mergers

**Procedure:**
1. Calculate potential firm values in different scenarios
2. Assess debt serviceability
3. Determine debt value based on probability-weighted scenarios

**Code Example:**
```python
def calculate_merged_debt_value(scenarios, probabilities, debt_value):
    weighted_firm_values = sum(scenario * prob for scenario, prob in zip(scenarios, probabilities))
    return min(weighted_firm_values, debt_value)
```

**Common Bugs to Avoid:**
- Using static debt face value
- Ignoring economic scenario probabilities
- Not considering debt serviceability

These patterns provide a comprehensive framework for solving complex financial reasoning problems using Python, addressing the key failure modes observed in the original cases.