Based on the comprehensive analysis of the failure cases, I'll extract the key skill patterns. I'll focus on the most generalizable and impactful patterns across the derivatives and financial modeling scenarios.

## Pattern: Multi-Step Financial Reasoning Decomposition

**Description:** Complex financial derivative problems require systematic decomposition into precise computational steps with clear tracking of intermediate variables and explicit calculation stages.

**When to Use:** Derivative pricing, portfolio rebalancing, option valuation, risk management scenarios involving multiple calculation stages

**Procedure:**
1. Identify all input variables and their sources
2. Break down calculation into discrete, verifiable steps
3. Use intermediate variables to track computational progress
4. Validate each computational stage before final result
5. Ensure final output matches expected financial logic

**Code Example:**

**Scenario:** Portfolio futures contract rebalancing calculation

**Correct Code:**
```python
def calculate_futures_contracts(portfolio_value, target_allocation, contract_multiplier, contract_price):
    # Step 1: Calculate current allocation deviation
    allocation_diff = target_allocation - current_allocation
    
    # Step 2: Compute required contract quantity
    contracts_needed = (portfolio_value * allocation_diff) / (contract_multiplier * contract_price)
    
    # Step 3: Round to nearest whole contract
    return round(contracts_needed, 0)
```

**Common Bugs to Avoid:**
- Skipping intermediate validation steps
- Not handling floating point contract quantities
- Ignoring contract multiplier effects
- Failing to round to whole contract quantities
## Pattern: Derivative Contract Quantity Mapping

**Description:** Precise translation of portfolio allocation targets into derivative contract quantities requires comprehensive mapping of market values, contract specifications, and risk exposures.

**When to Use:** Portfolio rebalancing, hedging strategies involving futures or options contracts

**Procedure:**
1. Calculate current portfolio exposure
2. Determine target exposure
3. Compute exposure differential
4. Map differential to contract specifications
5. Calculate precise contract quantities

**Code Example:**

**Scenario:** Mapping portfolio beta adjustment to futures contracts

**Correct Code:**
```python
def map_portfolio_futures(portfolio_value, current_beta, target_beta, futures_beta, futures_price):
    # Step 1: Calculate beta exposure change
    beta_differential = target_beta - current_beta
    
    # Step 2: Compute notional exposure adjustment
    exposure_adjustment = portfolio_value * beta_differential
    
    # Step 3: Calculate contract quantity
    contract_quantity = exposure_adjustment / (futures_beta * futures_price)
    
    return round(contract_quantity, 0)
```

**Common Bugs to Avoid:**
- Ignoring contract beta specifications
- Not accounting for portfolio market value
- Failing to round to whole contract quantities
- Overlooking sign conventions in exposure adjustments
## Pattern: Risk-Neutral Probability Distribution Extraction

**Description:** Converting option volatility surfaces into discrete probability distributions requires precise mathematical transformation and careful integration techniques.

**When to Use:** Implied volatility analysis, risk-neutral probability estimation from option pricing data

**Procedure:**
1. Extract option price data
2. Compute implied volatilities
3. Construct risk-neutral probability density
4. Validate distribution properties
5. Normalize probability estimates

**Code Example:**

**Scenario:** Extracting risk-neutral probabilities from option prices

**Correct Code:**
```python
def extract_risk_neutral_probabilities(option_prices, strike_prices):
    # Step 1: Compute implied volatilities
    implied_vols = [compute_implied_volatility(price, strike) 
                    for price, strike in zip(option_prices, strike_prices)]
    
    # Step 2: Transform to probability density
    prob_density = [vol_to_probability(vol) for vol in implied_vols]
    
    # Step 3: Normalize probabilities
    total_prob = sum(prob_density)
    normalized_probs = [p/total_prob for p in prob_density]
    
    return normalized_probs
```

**Common Bugs to Avoid:**
- Improper volatility transformation
- Failing to normalize probability distribution
- Ignoring boundary conditions
- Not handling edge cases in option pricing

These refined patterns address the systematic computational challenges observed across the derivative pricing and portfolio management cases.