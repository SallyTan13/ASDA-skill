# Financial Reasoning Skills Detail File

## Pattern: Discrete Probability Distribution Standard Deviation

**Description:** Correctly computing standard deviation for a discrete probability distribution requires calculating the expected return (weighted mean) first, then computing variance by summing probability-weighted squared deviations from that mean.

**When to Use:** Financial scenarios involving multiple economic states with associated probabilities and returns, typically in investment performance analysis.

**Procedure:**
1. Formula: σ = √[Σ(P(i) * (R(i) - E(R))²)]
   - P(i): Probability of each state
   - R(i): Return in each state
   - E(R): Expected return (weighted mean)

2. Calculate Expected Return:
   - Multiply each return by its probability
   - Sum these weighted returns

3. Compute Variance:
   - Subtract expected return from each state's return
   - Square these deviations
   - Weight by state probabilities
   - Sum the weighted squared deviations

4. Take square root of variance to get standard deviation

**Code Example:**
```python
def calculate_std_dev(states, probabilities, returns):
    # Calculate expected return
    expected_return = sum(p * r for p, r in zip(probabilities, returns))
    
    # Calculate variance
    variance = sum(p * ((r - expected_return) ** 2) 
                   for p, r in zip(probabilities, returns))
    
    # Return standard deviation
    return (variance ** 0.5)

# Example usage
states = ['Recession', 'Normal', 'Boom']
probabilities = [0.30, 0.55, 0.15]
returns = [0.06, 0.07, 0.11]

std_dev = calculate_std_dev(probabilities, returns)
```

**Common Bugs to Avoid:**
- Forgetting to weight deviations by probabilities
- Calculating simple average instead of weighted average
- Not squaring deviations before summing
- Incorrect order of operations
- Failing to take square root of variance

## Pattern: Information Ratio Calculation

**Description:** Information ratio measures risk-adjusted active return by dividing excess return by tracking error, providing a standardized performance metric for investment portfolios.

**When to Use:** Comparing portfolio performance against a benchmark, especially in active management contexts.

**Procedure:**
1. Formula: Information Ratio = (Portfolio Return - Benchmark Return) / Tracking Error

2. Calculate Excess Return:
   - Subtract risk-free or benchmark return from portfolio return

3. Compute Tracking Error:
   - Use residual standard deviation of portfolio returns

4. Divide excess return by tracking error

**Code Example:**
```python
def calculate_information_ratio(portfolio_return, benchmark_return, tracking_error):
    # Ensure tracking error is not zero to avoid division by zero
    if tracking_error == 0:
        raise ValueError("Tracking error cannot be zero")
    
    # Calculate excess return
    excess_return = portfolio_return - benchmark_return
    
    # Calculate information ratio
    info_ratio = excess_return / tracking_error
    
    return info_ratio

# Example usage
portfolio_return = 0.12  # 12%
benchmark_return = 0.10  # 10%
tracking_error = 0.02    # 2%

info_ratio = calculate_information_ratio(portfolio_return, benchmark_return, tracking_error)
```

**Common Bugs to Avoid:**
- Forgetting to subtract benchmark return
- Using incorrect benchmark (e.g., risk-free rate vs market return)
- Division by zero if tracking error is zero
- Misinterpreting tracking error calculation
- Not converting percentages correctly

## Verification Principles

1. Always validate inputs (non-zero denominators, valid ranges)
2. Use type hints and input validation
3. Include error handling for edge cases
4. Verify units and percentage conversions
5. Add sanity checks for reasonable output ranges