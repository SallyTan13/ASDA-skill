Based on the analysis of the failure cases, here are the distinct problem patterns:

## Pattern: Multi-Dimensional Asset Selection Reasoning

**Description:** Financial decision-making requires holistic evaluation of multiple criteria beyond single-dimensional metrics like Sharpe ratio or NPV.

**When to Use:** When selecting investments, asset classes, or projects with complex constraints and multiple evaluation dimensions.

**Procedure:**
1. Create a multi-dimensional evaluation matrix that includes:
   - Primary performance metric (e.g., Sharpe ratio, NPV)
   - Correlation with existing portfolio
   - Strategic fit with investment objectives
   - Specific constraints (budget, liquidity, regulatory limits)

2. Perform a weighted assessment that considers ALL dimensions, not just the most obvious metric

3. Explicitly check and validate each constraint before final selection
   - Budget limits
   - Regulatory requirements
   - Portfolio composition rules

4. Conduct sensitivity analysis to understand trade-offs between different evaluation criteria

**Example (sanitized):**
> **Scenario:** Selecting a new investment for a technology startup's venture fund
> **Wrong approach:** Choosing based solely on projected return
> **Correct approach:** 
> - Calculate risk-adjusted return
> - Assess strategic alignment with existing portfolio
> - Verify investment doesn't exceed risk tolerance
> - Check regulatory and fund-specific constraints

## Pattern: Bottom-Up Liquidity Analysis

**Description:** Portfolio liquidity assessment requires granular decomposition of asset class liquidity by multiplying allocation percentages with specific liquidity classifications.

**When to Use:** Analyzing portfolio liquidity, especially for institutional investors with complex asset allocations.

**Procedure:**
1. Break down each asset class into its liquidity components
   - Identify percentage of liquid/illiquid investments within each class
   - Do NOT assume uniform liquidity within an asset class

2. Calculate weighted liquidity by multiplying:
   (Asset Class Allocation) × (Liquidity Percentage)

3. Aggregate liquidity across all asset classes
   - Sum liquid components
   - Sum illiquid components

4. Compare against explicit liquidity requirements and constraints
   - Minimum liquid investment threshold
   - Maximum illiquid investment limit

5. Recommend reallocation strategies based on precise liquidity calculations

**Example (sanitized):**
> **Scenario:** University endowment reviewing investment portfolio
> **Wrong approach:** Treating asset classes as uniformly liquid/illiquid
> **Correct approach:** 
> - Decompose each asset class into liquid/illiquid percentages
> - Calculate weighted liquidity
> - Verify compliance with liquidity policy

## Pattern: Comprehensive Multi-Step Financial Needs Calculation

**Description:** Complex financial calculations require systematic decomposition of multiple value streams, careful discounting, and holistic consideration of future scenarios.

**When to Use:** Life insurance needs, retirement planning, long-term financial projections

**Procedure:**
1. Identify ALL relevant financial components
   - Immediate cash needs
   - Future living expenses
   - Income replacement
   - Existing capital

2. Apply appropriate discounting methodology
   - Use consistent discount rate
   - Account for expected inflation/expense growth
   - Calculate present value of future cash flows

3. Perform net present value (NPV) calculation
   - Subtract existing capital
   - Consider multiple scenarios

4. Validate assumptions and sensitivity
   - Test different discount rates
   - Consider alternative future scenarios

5. Explicitly state all assumptions and calculation steps

**Example (sanitized):**
> **Scenario:** Calculating retirement savings needs for a young professional
> **Wrong approach:** Simple linear projection of expenses
> **Correct approach:**
> - Decompose immediate and future financial needs
> - Apply consistent discount rate
> - Calculate NPV of future expenses
> - Subtract existing savings
> - Validate assumptions

These patterns capture the key reasoning gaps demonstrated across the failure cases, providing a systematic approach to complex financial decision-making.