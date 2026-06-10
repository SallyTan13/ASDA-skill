Based on the comprehensive analysis of the failure cases, I'll produce skill patterns that address the key conceptual and implementation gaps:

## Pattern: Option Payoff Calculation

**Description:** Correctly computing the intrinsic value of options at expiration, accounting for strike price and market price relationships.

**When to Use:** Options valuation problems, especially at expiration, involving call options with strike and market prices

**Procedure:**
1. Compute intrinsic value as max(0, market_price - strike_price)
2. Multiply result by contract multiplier (typically 100 shares)
3. Subtract initial option premium if calculating net gain

**Code Example:**
```python
def calculate_call_option_value(market_price, strike_price, contract_size=100):
    intrinsic_value = max(0, market_price - strike_price)
    return intrinsic_value * contract_size
```

**Common Bugs to Avoid:**
- Subtracting option premium incorrectly
- Not using max() to handle out-of-the-money scenarios
- Forgetting contract size multiplier

## Pattern: Risk-Neutral Price Movement Modeling

**Description:** Precisely modeling underlying asset price movements in derivative pricing, ensuring statistical properties match theoretical expectations.

**When to Use:** Binomial/trinomial option pricing models, derivatives modeling with stochastic processes

**Procedure:**
1. Match mean: (r - q - σ²/2)Δt
2. Match variance: σ²Δt
3. Use risk-neutral probabilities
4. Ensure symmetry in up/down movements

**Code Example:**
```python
import math

def create_binomial_tree_parameters(r, q, sigma, dt):
    u = math.exp((r - q + sigma**2/2) * dt + sigma * math.sqrt(dt))
    d = math.exp((r - q + sigma**2/2) * dt - sigma * math.sqrt(dt))
    p = 0.5  # Risk-neutral probability
    return u, d, p
```

**Common Bugs to Avoid:**
- Incorrect volatility scaling
- Misunderstanding risk-neutral probabilities
- Not accounting for dividend yield

## Pattern: Multi-Currency Instrument Valuation

**Description:** Handling complex financial instruments involving multiple currencies, correlations, and exchange rate interactions.

**When to Use:** International derivatives, cross-currency swaps, multi-currency financial modeling

**Procedure:**
1. Track exchange rates and correlations
2. Use numeraire change principles
3. Apply correlation-adjusted growth rates
4. Verify consistency of small variations

**Code Example:**
```python
def validate_multi_currency_change(index_change, fx_change, correlation):
    # Simple validation of small variations
    return (abs(index_change/index_change) <= 0.1 and 
            abs(fx_change/fx_change) <= 0.1)
```

**Common Bugs to Avoid:**
- Ignoring correlation effects
- Assuming linear relationships
- Not checking variation scales

## Pattern: Interest Rate Swap Duration Calculation

**Description:** Understanding swap duration as a measure of interest rate sensitivity, recognizing its typically negative sign.

**When to Use:** Interest rate derivative valuation, risk management of fixed income instruments

**Procedure:**
1. Compute bond equivalent duration
2. Recognize negative sign for pay-fixed swaps
3. Use absolute value for comparison
4. Verify against market benchmarks

**Code Example:**
```python
def swap_duration(bond_duration, swap_type='pay_fixed'):
    return -bond_duration if swap_type == 'pay_fixed' else bond_duration
```

**Common Bugs to Avoid:**
- Misinterpreting sign conventions
- Not distinguishing pay-fixed vs receive-fixed
- Ignoring directional price sensitivity

These patterns capture the core conceptual and implementation challenges across the failure cases, providing generalizable strategies for solving complex financial arithmetic problems using Python.