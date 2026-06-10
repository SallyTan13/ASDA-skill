## Pattern: Multi-Step Financial Calculation Verification

**Description:** Financial calculations often require systematic decomposition of complex problems into precise, sequential steps, with explicit verification of intermediate and final results.

**When to Use:** Triggered by multi-step financial problems involving statistical calculations, expected value, risk-adjusted returns, or complex financial metrics.

**Procedure:**
1. Decompose the problem into explicit calculation stages
2. Perform each calculation step sequentially
3. Verify intermediate results against problem constraints
4. Check final result against all original problem requirements
5. Validate calculation method matches specific financial context

**Example (sanitized):**
> **Scenario:** Calculating risk-adjusted portfolio performance
> **Wrong approach:** Rushing calculation without checking intermediate steps
> **Correct approach:** 
> - Break down Sharpe ratio into: (Portfolio Return - Risk-Free Rate) / Portfolio Standard Deviation
> - Calculate each component separately
> - Cross-check intermediate calculations
> - Verify final ratio meets problem-specific constraints

## Pattern: Residual Claim Calculation in Equity Valuation

**Description:** Equity value represents the residual financial claim after satisfying fixed obligations, requiring systematic subtraction of prior claims before computing expected value.

**When to Use:** Problems involving corporate finance, project valuation, or scenarios with fixed debt/obligation payments

**Procedure:**
1. Identify total project/firm payoff
2. Locate fixed obligation amount
3. Subtract fixed obligations from total payoff
4. Calculate expected value of remaining residual
5. Verify remaining amount represents shareholder claim

**Example (sanitized):**
> **Scenario:** Evaluating project equity value with preset bondholder payments
> **Wrong approach:** Treating total project payoff as equity value
> **Correct approach:** 
> - Calculate total project payoff across scenarios
> - Subtract mandatory bondholder payment
> - Compute expected value of remaining funds
> - Confirm result represents shareholder residual claim

## Pattern: Holistic Portfolio Performance Evaluation

**Description:** Comprehensive portfolio assessment requires weighted aggregation of performance metrics across multiple managers/investments, not isolated individual evaluation.

**When to Use:** Institutional investment analysis, multi-manager portfolio review

**Procedure:**
1. Collect individual manager performance metrics
2. Weight metrics by investment size/allocation
3. Compute weighted average of key performance indicators
4. Compare aggregate metrics to investment goals
5. Validate performance against comprehensive objectives

**Example (sanitized):**
> **Scenario:** Evaluating institutional investment portfolio performance
> **Wrong approach:** Analyzing each manager in isolation
> **Correct approach:**
> - Calculate weighted alpha across managers
> - Compute aggregate tracking error
> - Compare combined metrics to investment objectives
> - Assess overall portfolio performance holistically

## Pattern: Systematic Risk-Return Trade-off Analysis

**Description:** Evaluating investment opportunities requires systematic comparison of returns normalized by risk, using standardized financial metrics that account for variability and excess returns.

**When to Use:** Comparing investment options with different risk profiles

**Procedure:**
1. Extract return and risk metrics for each option
2. Subtract risk-free rate from returns
3. Normalize excess return by risk measure (e.g., standard deviation)
4. Rank options by risk-adjusted performance metric
5. Verify calculation matches problem-specific constraints

**Example (sanitized):**
> **Scenario:** Comparing mutual fund performance
> **Wrong approach:** Using raw returns without risk normalization
> **Correct approach:**
> - Calculate excess return for each fund
> - Divide excess return by fund's volatility
> - Rank funds by risk-adjusted performance ratio
> - Validate ranking against investment objectives