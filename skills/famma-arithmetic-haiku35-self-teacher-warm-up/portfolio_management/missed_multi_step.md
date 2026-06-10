Based on the comprehensive analysis of the failure cases, I'll outline several key skill patterns. I'll focus on the most critical and generalizable patterns.

## Pattern: Probabilistic Portfolio Return Calculation

**Description:** Systematic method for computing expected portfolio returns that requires precise probability-weighted return calculations across different economic states.

**When to Use:** Multi-asset portfolio problems involving state-based return probabilities, portfolio weighting

**Procedure:**
1. Compute weighted return for each state
2. Sum state-specific weighted returns
3. Validate probability summation to 1.0
4. Handle multiple asset interactions

**Code Example:**

**Scenario:** Computing portfolio return with two stocks across economic states

**Correct Code:**
```python
def portfolio_expected_return(stocks, weights):
    # Validate inputs
    assert abs(sum(weights) - 1.0) < 1e-10, "Weights must sum to 1.0"
    
    # Compute weighted returns per state
    state_returns = [
        sum(stock['returns'][i] * stock['probabilities'][i] * weights[j] 
            for j, stock in enumerate(stocks))
        for i in range(len(stocks[0]['probabilities']))
    ]
    
    # Total portfolio expected return
    return sum(state_returns)
```

**Common Bugs to Avoid:**
- Not checking weight summation
- Ignoring state probabilities
- Hardcoding instead of generalizing
- Mixing up indexing of stocks/states
## Pattern: Beta and Portfolio Risk Decomposition

**Description:** Systematic method for computing portfolio risk characteristics by aggregating individual security betas, returns, and firm-specific risks.

**When to Use:** Portfolio construction problems involving systematic and unsystematic risk, market sensitivity

**Procedure:**
1. Compute weighted average portfolio beta
2. Calculate portfolio expected return
3. Decompose portfolio variance into systematic and unsystematic components
4. Apply market risk model principles

**Code Example:**
```python
def portfolio_risk_decomposition(securities, weights, market_std):
    # Weighted average beta
    portfolio_beta = sum(sec['beta'] * weight for sec, weight in zip(securities, weights))
    
    # Expected portfolio return
    portfolio_return = sum(sec['expected_return'] * weight for sec, weight in zip(securities, weights))
    
    # Systematic risk
    systematic_variance = portfolio_beta**2 * market_std**2
    
    # Unsystematic risk
    unsystematic_variance = sum(
        weight**2 * sec['firm_specific_std']**2 
        for sec, weight in zip(securities, weights)
    )
    
    total_variance = systematic_variance + unsystematic_variance
    total_std = np.sqrt(total_variance)
    
    return {
        'portfolio_beta': portfolio_beta,
        'portfolio_return': portfolio_return,
        'total_std': total_std,
        'systematic_risk': np.sqrt(systematic_variance),
        'unsystematic_risk': np.sqrt(unsystematic_variance)
    }
```

**Common Bugs to Avoid:**
- Incorrect beta weighting
- Neglecting firm-specific risk
- Misunderstanding variance vs standard deviation
- Not considering market risk model assumptions

## Pattern: Time-Weighted Return (TWR) Calculation

**Description:** Precise method for computing investment returns that neutralizes the impact of external cash flows by segmenting return periods.

**When to Use:** Performance measurement problems involving multiple cash inflows/outflows

**Procedure:**
1. Segment investment periods at each cash flow
2. Calculate period-specific returns
3. Geometrically link segment returns
4. Adjust for external cash movements

**Code Example:**
```python
def time_weighted_return(initial_value, cash_flows, end_value):
    # Segment returns calculation
    segment_returns = []
    current_value = initial_value
    
    for flow, new_value in cash_flows:
        # Calculate segment return
        segment_return = (new_value - current_value - flow) / current_value
        segment_returns.append(segment_return)
        current_value = new_value
    
    # Final segment return
    final_segment_return = (end_value - current_value) / current_value
    segment_returns.append(final_segment_return)
    
    # Geometric linking of returns
    twr = np.prod([1 + r for r in segment_returns]) - 1
    
    return twr
```

**Common Bugs to Avoid:**
- Treating all cash flows as part of return
- Using arithmetic mean instead of geometric linking
- Mishandling timing of cash flows
- Not segmenting return periods

These patterns capture the core reasoning skills needed for complex financial calculations, emphasizing systematic decomposition, probabilistic thinking, and precise computational techniques.

## Pattern: Multi-Factor Return Decomposition

**Description:** Systematic method for decomposing stock returns using factor sensitivities and actual vs expected factor movements.

**When to Use:** Factor model return calculations, performance attribution problems

**Procedure:**
1. Start with base expected return
2. Compute factor contributions
3. Sum base return with factor adjustments
4. Handle multiple factor interactions

**Code Example:**

**Scenario:** Computing stock return using macroeconomic factors

**Correct Code:**
```python
def multi_factor_return(base_return, factors):
    # Compute factor contributions
    factor_contributions = sum(
        factor['sensitivity'] * (factor['actual'] - factor['expected'])
        for factor in factors
    )
    
    # Total return is base + factor adjustments
    return base_return + factor_contributions
```

**Common Bugs to Avoid:**
- Ignoring base expected return
- Miscalculating factor sensitivity
- Not handling sign of factor deviations
- Hardcoding number of factors

## Pattern: Portfolio Variance with Correlation

**Description:** Systematic method for computing portfolio variance that requires precise handling of asset correlations, individual variances, and portfolio weights.

**When to Use:** Portfolio risk calculation problems involving multiple correlated assets, scenario-based return analysis

**Procedure:**
1. Calculate expected returns for each scenario
2. Compute variance of individual assets
3. Compute covariance between assets
4. Apply portfolio weight matrix to variance calculation

**Code Example:**

**Scenario:** Computing portfolio variance for two stocks with different returns across economic scenarios

```python
import numpy as np

def portfolio_variance(returns, weights, probabilities):
    # Calculate expected return for each asset
    expected_returns = np.sum(returns * probabilities, axis=0)
    
    # Compute variance for each asset
    variances = np.sum(((returns - expected_returns)**2) * probabilities, axis=0)
    
    # Compute covariance matrix
    covariance_matrix = np.cov(returns.T, aweights=probabilities)
    
    # Portfolio variance calculation
    portfolio_var = np.dot(weights.T, np.dot(covariance_matrix, weights))
    
    return np.sqrt(portfolio_var)  # Return standard deviation
```

**Common Bugs to Avoid:**
- Forgetting to weight probabilities in variance calculation
- Not handling correlation matrix correctly
- Returning variance instead of standard deviation
- Ignoring scenario probabilities

## Pattern: Multi-Factor Return Decomposition with Systematic Risk Estimation

**Description:** Comprehensive method for decomposing portfolio returns using factor sensitivities, risk premiums, and systematic risk calculation.

**When to Use:** Complex return attribution problems involving multiple economic factors, portfolio performance analysis

**Procedure:**
1. Extract factor loadings for each asset
2. Compute factor risk premiums
3. Calculate systematic and unsystematic risk components
4. Aggregate portfolio-level returns

**Code Example:**

**Scenario:** Computing portfolio returns using three-factor model with different factor sensitivities

```python
import numpy as np

def multi_factor_portfolio_return(factor_loadings, factor_premiums, portfolio_weights, risk_free_rate):
    # Compute systematic return component
    systematic_returns = np.dot(factor_loadings, factor_premiums)
    
    # Portfolio systematic return
    portfolio_systematic_return = np.dot(systematic_returns, portfolio_weights)
    
    # Add risk-free rate
    total_portfolio_return = portfolio_systematic_return + risk_free_rate
    
    return total_portfolio_return

def portfolio_systematic_risk(factor_loadings, factor_covariance, portfolio_weights):
    # Compute systematic risk using factor covariance
    systematic_risk = np.sqrt(
        np.dot(portfolio_weights.T, 
               np.dot(factor_covariance, portfolio_weights))
    )
    return systematic_risk
```

**Common Bugs to Avoid:**
- Misaligning factor loadings and risk premiums
- Not accounting for risk-free rate
- Incorrect matrix multiplication in risk calculation
- Overlooking sign conventions in factor returns

These patterns address the systematic computational challenges in portfolio management, focusing on precise risk and return calculations across multiple scenarios and factor models.