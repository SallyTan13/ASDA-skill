I'll help you create a comprehensive skill pattern document based on the failure cases. I'll focus on extracting the most critical and generalizable patterns from the fixed income reasoning failures.

## Pattern: Multi-Step Bond Valuation with Forward Rates

**Description:** Systematically decomposing bond valuation by sequentially discounting cash flows using time-varying forward interest rates, addressing complex multi-period discounting challenges.

**When to Use:** Bond pricing questions involving multiple coupon payments, varying interest rates, and complex discounting requirements across different time periods.

**Procedure:**
1. Extract forward rates for each period
2. Identify all cash flows (coupons and principal)
3. Discount each cash flow using its corresponding period-specific forward rate
4. Sum the discounted cash flows to determine bond price

**Code Example:**

**Scenario:** Pricing a 3-year bond with 5% annual coupon, $1000 par value

**Correct Code:**
```python
def bond_price_forward_rates(par_value, coupon_rate, forward_rates):
    # Validate input lengths
    cash_flows = [par_value * coupon_rate] * 2 + [par_value + par_value * coupon_rate]
    
    # Discount each cash flow with corresponding forward rate
    discounted_flows = [
        flow / ((1 + rate) ** (idx + 1)) 
        for idx, (flow, rate) in enumerate(zip(cash_flows, forward_rates))
    ]
    
    return sum(discounted_flows)

# Example usage
forward_rates = [0.05, 0.07, 0.09]  # Year 1, 2, 3 forward rates
price = bond_price_forward_rates(1000, 0.05, forward_rates)
```

**Common Bugs to Avoid:**
- Forgetting to match cash flows with corresponding forward rates
- Using simple average rates instead of period-specific rates
- Not handling different compounding conventions
- Incorrect indexing of forward rates
## Pattern: Term Structure Rate Extraction

**Description:** Systematically extracting implied forward rates or yields from a term structure of zero-coupon bond rates using precise bootstrapping and compounding techniques.

**When to Use:** Questions involving deriving implied future interest rates, forward rates, or yield to maturity from a given yield curve.

**Procedure:**
1. Collect zero-coupon rates for different maturities
2. Apply compounding formula to derive implied forward rates
3. Use iterative methods for precise rate extraction
4. Validate rate consistency across periods

**Code Example:**
```python
def extract_forward_rate(spot_rates, start_year, end_year):
    """
    Calculate forward rate between specific years using spot rates
    
    Args:
        spot_rates (list): Zero-coupon rates for consecutive years
        start_year (int): Starting year of forward rate
        end_year (int): Ending year of forward rate
    
    Returns:
        float: Implied forward rate
    """
    # Ensure valid indices
    if start_year < 0 or end_year >= len(spot_rates):
        raise ValueError("Invalid year indices")
    
    # Forward rate calculation using compounding principle
    forward_rate = (
        (1 + spot_rates[end_year]) ** (end_year + 1) / 
        (1 + spot_rates[start_year]) ** (start_year + 1) 
    ) ** (1 / (end_year - start_year)) - 1
    
    return forward_rate
```

**Common Bugs to Avoid:**
- Incorrect indexing of spot rates
- Not handling zero or negative rates
- Misunderstanding compounding conventions
- Failing to validate rate consistency
## Pattern: Swap Valuation with Differential Cash Flows

**Description:** Decomposing interest rate swap valuation by separately computing present values of fixed and floating payment streams and calculating their net difference.

**When to Use:** Interest rate swap pricing questions involving multiple payment periods and different rate conventions.

**Procedure:**
1. Identify fixed and floating payment streams
2. Compute present value of each stream using appropriate discount rates
3. Calculate net present value difference
4. Consider currency and compounding effects

**Code Example:**
```python
def swap_valuation(notional, fixed_rate, floating_rates, discount_rates):
    """
    Calculate swap value by comparing fixed vs floating payment streams
    
    Args:
    - notional: Principal amount
    - fixed_rate: Constant payment rate
    - floating_rates: List of floating rates per period
    - discount_rates: Corresponding discount rates
    """
    fixed_stream_pv = sum([
        notional * fixed_rate * (1 / (1 + dr)) 
        for dr in discount_rates
    ])
    
    floating_stream_pv = sum([
        notional * rate * (1 / (1 + dr)) 
        for rate, dr in zip(floating_rates, discount_rates)
    ])
    
    return floating_stream_pv - fixed_stream_pv
```

**Common Bugs to Avoid:**
- Treating swap as single cash flow
- Ignoring time value of money
- Not handling different rate conventions
- Forgetting to discount each cash flow

These patterns capture the core reasoning challenges in the fixed income reasoning failures, providing systematic approaches to solving complex financial arithmetic problems.

Would you like me to elaborate on any of these patterns or generate additional skill patterns?

## Pattern: Term Structure Rate Interpolation and Yield Curve Analysis

**Description:** Extracting precise yields and rates by interpolating between given forward rate points and constructing a comprehensive term structure.

**When to Use:** Questions involving yield curve extraction, maturity-specific rate determination, and multi-period rate analysis.

**Procedure:**
1. Collect forward rates across different periods
2. Interpolate between known rate points
3. Compute geometric average or weighted interpolation
4. Validate rate consistency

**Code Example:**

**Scenario:** Calculating 2-year yield to maturity from forward rates

**Correct Code:**
```python
def calculate_yield_to_maturity(forward_rates, target_maturity):
    # Compute geometric average of forward rates
    compounded_rate = 1.0
    for i, rate in enumerate(forward_rates[:target_maturity], 1):
        compounded_rate *= (1 + rate)
    
    # Convert to yield to maturity
    ytm = (compounded_rate ** (1/target_maturity)) - 1
    return ytm * 100  # Convert to percentage

# Example: forward rates [0.046, 0.049, 0.052, 0.055]
forward_rates = [0.046, 0.049, 0.052, 0.055]
two_year_ytm = calculate_yield_to_maturity(forward_rates, 2)
# Returns interpolated 2-year yield to maturity
```

**Common Bugs to Avoid:**
- Using arithmetic mean instead of geometric compounding
- Not handling zero or negative rates
- Incorrect indexing of forward rates
- Failing to convert to percentage representation

These refined and new patterns address the systematic challenges observed in the fixed income calculation cases, providing robust frameworks for multi-step bond valuation and rate interpolation.

## Pattern: Duration-Based Futures Hedging

**Description:** Precise calculation of futures contracts needed to adjust portfolio duration to a target level, accounting for portfolio composition and futures contract characteristics.

**When to Use:** Portfolio management scenarios requiring interest rate risk management through futures contracts.

**Procedure:**
1. Calculate current portfolio duration
2. Determine target duration gap
3. Use futures contract characteristics (conversion factor, duration)
4. Compute required number of contracts

**Code Example:**
```python
def calculate_futures_hedge(
    portfolio_value, 
    current_duration, 
    target_duration, 
    futures_duration, 
    futures_conversion_factor
):
    """
    Calculate number of futures contracts for duration hedging
    
    Args:
        portfolio_value (float): Total portfolio value
        current_duration (float): Current portfolio duration
        target_duration (float): Desired portfolio duration
        futures_duration (float): Duration of futures contract
        futures_conversion_factor (float): Conversion factor for futures
    
    Returns:
        int: Number of futures contracts to sell/buy
    """
    duration_gap = target_duration - current_duration
    
    # Futures contract adjustment calculation
    contracts = (
        (portfolio_value * duration_gap) / 
        (futures_duration * futures_conversion_factor * 100000)
    )
    
    return round(abs(contracts))
```

**Common Bugs to Avoid:**
- Ignoring conversion factors
- Not rounding contract quantities
- Failing to handle different portfolio compositions
- Misinterpreting duration adjustment direction