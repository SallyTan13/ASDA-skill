## Pattern: Multi-Dimensional Financial Valuation

**Description:** Financial valuation requires simultaneously considering multiple interconnected financial elements, including probability-weighted scenarios, debt obligations, and net value calculations.

**When to Use:** Triggered by merger scenarios, company valuation questions, or complex financial analysis involving multiple variables

**Procedure:**
1. Identify ALL relevant financial components:
   - Scenario-based values
   - Probability distributions
   - Debt obligations
   - Equity value

2. Calculate probability-weighted expected value:
   - Multiply each scenario value by its probability
   - Sum these weighted values
   - Do NOT stop at this intermediate calculation

3. Adjust for debt and financial obligations:
   - Subtract outstanding debt claims
   - Verify total value against debt levels
   - Determine net equity value

4. Verify calculation by cross-checking:
   - Confirm all probabilities sum to 1.0
   - Validate debt subtraction logic
   - Ensure no financial elements are overlooked

**Example (sanitized):**
> **Scenario:** A company has three market scenarios with different valuations
> **Wrong approach:** Simply adding scenario values without considering probabilities or debt
> **Correct approach:** 
> - Calculate weighted average: (Scenario1 * Prob1) + (Scenario2 * Prob2) + (Scenario3 * Prob3)
> - Subtract total debt from weighted average
> - Verify final net value against financial constraints

## Pattern: Comprehensive NPV Decision Framework

**Description:** Net Present Value (NPV) analysis requires a holistic evaluation beyond simple positive/negative calculation, considering cash flow timing, tax implications, and strategic constraints.

**When to Use:** Investment decision questions, project evaluation, financial offer analysis

**Procedure:**
1. Map ALL cash flows chronologically:
   - Identify initial investment
   - Catalog ALL periodic cash inflows/outflows
   - Note timing of each cash movement

2. Apply comprehensive discounting:
   - Use appropriate discount rate
   - Discount EACH cash flow to present value
   - Consider tax implications on cash flows

3. Conduct multi-dimensional NPV assessment:
   - Calculate total NPV
   - Analyze cash flow pattern (not just total value)
   - Evaluate liquidity and timing risks
   - Consider strategic constraints beyond pure NPV

4. Verification steps:
   - Check discount rate appropriateness
   - Validate tax calculations
   - Assess early period cash flow challenges
   - Consider qualitative factors beyond quantitative analysis

**Example (sanitized):**
> **Scenario:** Investment opportunity with varied cash flows
> **Wrong approach:** Accepting based on positive NPV alone
> **Correct approach:** 
> - Detailed cash flow discounting
> - Assess early period negative cash flows
> - Consider strategic fit beyond pure financial metrics

## Pattern: Debt Resolution in Merger Scenarios

**Description:** Merger debt resolution requires understanding priority-based allocation mechanisms, not simple pro-rata percentage calculations.

**When to Use:** Merger scenarios involving multiple companies with debt obligations

**Procedure:**
1. Calculate total merged entity value:
   - Sum scenario-specific values
   - Identify total outstanding debt
   - Determine available value for debt resolution

2. Apply debt resolution hierarchy:
   - Prioritize senior debt claims
   - Allocate available value to debt holders
   - Ensure full satisfaction of debt claims within available value

3. Verify allocation logic:
   - Confirm total debt matches original obligations
   - Check that allocation follows legal/financial priority rules
   - Validate no artificial reduction of debt claims

**Example (sanitized):**
> **Scenario:** Company merger with limited combined value
> **Wrong approach:** Arbitrarily reducing debt claims
> **Correct approach:** 
> - Calculate total merged value
> - Allocate full debt claims within available resources
> - Maintain debt claim integrity