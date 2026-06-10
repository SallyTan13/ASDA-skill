Based on the comprehensive analysis of the failure cases, here are the key skill patterns:

## Pattern: Probabilistic Expected Value Calculation

**Description:** Systematic method for computing expected value by multiplying each scenario's probability with its corresponding outcome and summing across all states.

**When to Use:** Financial scenarios involving probabilistic outcomes, stock returns, project valuations with multiple economic states

**Procedure:**
1. Identify all possible economic states
2. Determine probability for each state
3. Multiply each state's probability by its corresponding outcome
4. Sum the weighted outcomes

**Code Example:**

**Scenario:** Investment returns across different market conditions

**Correct Code:**
```python
def calculate_expected_value(states, probabilities, outcomes):
    return sum(prob * outcome for prob, outcome in zip(probabilities, outcomes))

# Example usage
states = ['Boom', 'Normal', 'Recession']
probabilities = [0.30, 0.50, 0.20]
outcomes = [18, 12, 9]

expected_return = calculate_expected_value(probabilities, outcomes)
```

**Common Bugs to Avoid:**
- Forgetting to multiply probabilities with outcomes
- Using incorrect probability weights
- Not verifying that probabilities sum to 1
- Hardcoding values instead of using flexible functions
## Pattern: Portfolio Return Calculation

**Description:** Computing portfolio return by multiplying each asset's return by its portfolio weight across different economic states.

**When to Use:** Multi-asset portfolio analysis, asset allocation questions involving different economic scenarios.

**Procedure:**
1. Verify portfolio weights sum to 1.0
2. Compute weighted return for each state
3. Sum weighted returns across states
4. Validate result's reasonableness

**Code Example:**
```python
def calculate_portfolio_return(asset_returns, asset_weights, state_probs):
    # Sanity checks
    assert len(asset_returns) == len(asset_weights)
    assert abs(sum(asset_weights) - 1.0) < 1e-10
    
    # State-by-state portfolio return
    portfolio_returns = [
        sum(ret * weight for ret, weight in zip(state_returns, asset_weights))
        for state_returns in zip(*asset_returns)
    ]
    
    # Probability-weighted portfolio return
    expected_portfolio_return = sum(
        ret * prob for ret, prob in zip(portfolio_returns, state_probs)
    )
    
    return expected_portfolio_return
```

**Common Bugs to Avoid:**
- Misaligning asset returns with weights
- Incorrect probability handling
- Not accounting for all economic states

## Pattern: Correlation Coefficient Calculation

**Description:** Computing stock correlation by calculating covariance and normalizing by individual stock standard deviations.

**When to Use:** Financial analysis requiring correlation between asset returns across economic states.

**Procedure:**
1. Calculate expected returns for each stock
2. Compute deviations from expected returns
3. Calculate covariance using joint probabilities
4. Normalize by stock standard deviations

**Code Example:**
```python
def calculate_correlation(stock1_returns, stock2_returns, state_probs):
    # Expected returns
    e1 = sum(ret * prob for ret, prob in zip(stock1_returns, state_probs))
    e2 = sum(ret * prob for ret, prob in zip(stock2_returns, state_probs))
    
    # Deviations
    dev1 = [ret - e1 for ret in stock1_returns]
    dev2 = [ret - e2 for ret in stock2_returns]
    
    # Covariance
    covariance = sum(d1 * d2 * prob 
                     for d1, d2, prob in zip(dev1, dev2, state_probs))
    
    # Standard deviations
    var1 = sum((d**2) * prob for d, prob in zip(dev1, state_probs))
    var2 = sum((d**2) * prob for d, prob in zip(dev2, state_probs))
    
    correlation = covariance / (var1**0.5 * var2**0.5)
    return correlation
```

**Common Bugs to Avoid:**
- Incorrect variance calculation
- Mishandling probability weights
- Not centering returns around expected value

These patterns capture the core reasoning skills needed for probabilistic financial calculations, focusing on systematic approaches to expected value, portfolio return, and correlation computation.

## Pattern: Sharpe Ratio Calculation

**Description:** Systematic method for computing risk-adjusted investment performance by calculating excess return normalized by portfolio risk.

**When to Use:** Comparing investment performance across different assets or portfolios, evaluating risk-adjusted returns

**Procedure:**
1. Calculate portfolio's excess return (Portfolio Return - Risk-Free Rate)
2. Divide excess return by portfolio's standard deviation
3. Higher Sharpe ratio indicates better risk-adjusted performance

**Code Example:**

**Scenario:** Comparing mutual fund performance

**Correct Code:**
```python
def calculate_sharpe_ratio(portfolio_return, risk_free_rate, portfolio_std_dev):
    excess_return = portfolio_return - risk_free_rate
    return excess_return / portfolio_std_dev

# Example usage
risk_free_rate = 0.06
fund_returns = [0.24, 0.12, 0.22]
fund_std_devs = [0.30, 0.10, 0.20]

sharpe_ratios = [calculate_sharpe_ratio(ret, risk_free_rate, std_dev) 
                 for ret, std_dev in zip(fund_returns, fund_std_devs)]
```

**Common Bugs to Avoid:**
- Using raw returns instead of excess returns
- Incorrect risk-free rate application
- Not handling zero or negative standard deviations
- Forgetting to vectorize calculations for multiple funds

## Pattern: Covariance Calculation for Financial Returns

**Description:** Systematic method for computing covariance between asset returns across different economic states.

**When to Use:** Analyzing correlation between stock returns, portfolio diversification assessment

**Procedure:**
1. Calculate expected returns for each stock
2. Compute deviations from mean returns
3. Multiply deviations across stocks
4. Weight by state probabilities

**Code Example:**

**Scenario:** Stock returns across market conditions

**Correct Code:**
```python
def calculate_covariance(states_prob, stock_a_returns, stock_b_returns):
    # Calculate mean returns
    mean_a = sum(prob * ret for prob, ret in zip(states_prob, stock_a_returns))
    mean_b = sum(prob * ret for prob, ret in zip(states_prob, stock_b_returns))
    
    # Calculate covariance
    covariance = sum(
        prob * (a_ret - mean_a) * (b_ret - mean_b) 
        for prob, a_ret, b_ret in zip(states_prob, stock_a_returns, stock_b_returns)
    )
    
    return covariance

# Example usage
states_prob = [1/3, 1/3, 1/3]
stock_a_returns = [0.108, 0.126, 0.064]
stock_b_returns = [0.067, 0.113, 0.276]

covariance = calculate_covariance(states_prob, stock_a_returns, stock_b_returns)
```

**Common Bugs to Avoid:**
- Incorrect probability weighting
- Not centering returns around their means
- Confusing correlation with covariance
- Hardcoding state probabilities

These refined and new patterns address the systematic errors observed in the missed multi-step equity skill file, providing structured approaches to probabilistic financial calculations.