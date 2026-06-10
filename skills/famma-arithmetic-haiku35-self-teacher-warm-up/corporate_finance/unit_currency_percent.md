## Pattern: Probabilistic Valuation with State-Dependent Outcomes

**Description:** Calculating expected value across multiple economic states by applying probability-weighted valuations, especially for debt or asset valuation under uncertainty.

**When to Use:** Corporate finance scenarios involving multi-state economic models, merger analysis, or contingent valuation problems

**Procedure:**
1. Identify all possible economic states
2. Extract probabilities for each state
3. Calculate state-specific values
4. Compute weighted average using probability * value

**Code Example:**

**Scenario:** Investment valuation across economic scenarios

```python
def calculate_expected_debt_value(states):
    """
    Calculate expected debt value across economic states
    
    Args:
    states (list): [(probability, value), ...]
    
    Returns:
    float: Probability-weighted expected value
    """
    expected_value = sum(
        prob * value for prob, value in states
    )
    return round(expected_value, 2)

# Example usage
debt_states = [
    (0.6, 290000),  # Boom state
    (0.4, 110000)   # Recession state
]

expected_debt = calculate_expected_debt_value(debt_states)
# Returns weighted average across states
```

**Common Bugs to Avoid:**
- Forgetting to multiply by probabilities
- Using raw values without weighting
- Incorrect rounding or precision
- Mishandling state probabilities

## Pattern: Interest Rate Calculation with Time Value of Money

**Description:** Solving for unknown interest rates by algebraically rearranging present/future value formulas, handling compounding and time periods.

**When to Use:** Financial problems involving solving for unknown rates, present/future value calculations

**Procedure:**
1. Identify known variables (PV, FV, n)
2. Rearrange standard TVM formula
3. Use logarithmic transformation
4. Solve for rate with precise mathematical approach

**Code Example:**

```python
import math

def solve_interest_rate(present_value, future_value, years):
    """
    Solve for interest rate using algebraic rearrangement
    
    Formula: r = (FV/PV)^(1/n) - 1
    """
    rate = (future_value / present_value) ** (1/years) - 1
    return round(rate, 4)

# Example usage
rate = solve_interest_rate(242, 345, 4)
# Correctly handles rate calculation
```

**Common Bugs to Avoid:**
- Direct division instead of logarithmic approach
- Incorrect exponent handling
- Forgetting to subtract 1 in rate calculation
- Improper rounding

## Pattern: Effective Annual Rate (EAR) Conversion

**Description:** Precise conversion of Annual Percentage Rate (APR) to Effective Annual Rate (EAR) accounting for compounding frequency.

**When to Use:** Financial problems involving interest rate conversions, especially with multiple compounding periods

**Procedure:**
1. Identify APR and compounding frequency
2. Use standard EAR formula: EAR = (1 + APR/m)^m - 1
3. Handle special cases like continuous compounding
4. Round to appropriate decimal places

**Code Example:**

```python
import math

def calculate_ear(apr, compounds_per_year):
    """
    Calculate Effective Annual Rate
    
    Args:
    apr (float): Annual Percentage Rate
    compounds_per_year (int): Frequency of compounding
    
    Returns:
    float: Effective Annual Rate
    """
    ear = (1 + apr/compounds_per_year)**compounds_per_year - 1
    return round(ear, 4)

# Example usage
quarterly_ear = calculate_ear(0.067, 4)  # 6.7% APR, quarterly compounding
```

**Common Bugs to Avoid:**
- Using simple interest instead of compound interest formula
- Incorrect compounding frequency handling
- Forgetting to subtract 1 in EAR calculation
- Imprecise rounding