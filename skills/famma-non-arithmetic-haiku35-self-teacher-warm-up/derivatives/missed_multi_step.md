Based on the analysis of the failure cases, I'll extract the key skill patterns:

## Pattern: Conditional Expectation in Multi-State Probabilistic Models

**Description:** Correctly computing conditional expectations requires understanding state-specific probability weighting and path-dependent calculations, not uniform averaging.

**When to Use:** Triggered by keywords: conditional expectation, multi-state model, binomial tree, risk-neutral/actual probability

**Procedure:**
1. Identify all possible paths/states from the current decision point
2. For each state, list out ALL possible subsequent values
3. Apply state-specific probability weights EXACTLY as given
4. Compute weighted average for EACH state separately
5. Verify that probabilities sum to 1 for each conditional path
6. Double-check that you're using the correct probability measure (risk-neutral vs actual)

**Example (sanitized):**
> **Scenario:** A stock can move up/down with probabilities p and q. Compute conditional expectation at time t.
> **Wrong approach:** Averaging all paths uniformly
> **Correct approach:** 
> - List paths: (Up, Up), (Up, Down), (Down, Up), (Down, Down)
> - Weight each path by its exact probability
> - Compute state-specific weighted averages

## Pattern: Derivative Hedge Effectiveness Quantitative Decomposition

**Description:** Assessing derivative hedge effectiveness requires systematic tracing of portfolio risk transformation across multiple computational steps, not superficial comparisons.

**When to Use:** Triggered by keywords: portfolio beta adjustment, futures hedge, risk management

**Procedure:**
1. Identify initial portfolio characteristics (initial beta, value)
2. Calculate derivative contract's risk characteristics
3. Compute precise portfolio transformation equations
4. Trace portfolio return vs market return interactions
5. Verify hedge effectiveness through quantitative risk decomposition
6. Check if final portfolio risk matches target risk profile

**Example (sanitized):**
> **Scenario:** Using futures to adjust portfolio risk exposure
> **Wrong approach:** Qualitative assessment of price changes
> **Correct approach:** 
> - Compute exact beta transformation equation
> - Trace portfolio return relative to market return
> - Validate hedge effectiveness through mathematical risk decomposition

## Pattern: Derivative Instrument Notional Principal Calibration

**Description:** Determining derivative notional principal requires precise mathematical calibration to target portfolio characteristics, not simple pro-rata scaling.

**When to Use:** Triggered by keywords: swap notional principal, portfolio duration management

**Procedure:**
1. Identify current portfolio characteristics (value, duration)
2. Define target portfolio characteristics
3. Construct precise mathematical mapping equation
4. Compute derivative instrument parameters
5. Verify that derivative characteristics exactly match target
6. Cross-check calibration through sensitivity analysis

**Example (sanitized):**
> **Scenario:** Using interest rate swap to modify portfolio duration
> **Wrong approach:** Linear scaling of portfolio value
> **Correct approach:**
> - Compute exact duration transformation equation
> - Calculate precise notional principal needed
> - Validate through comprehensive risk matching calculation

## Pattern: Multi-Period Probabilistic Path Expectation Calculation

**Description:** Computing multi-period expectation requires systematically tracing all possible paths, applying correct probability weights, and summing path-specific value combinations.

**When to Use:** Triggered by keywords: multi-period model, path expectation, probabilistic tree

**Procedure:**
1. Map ALL possible paths from initial state
2. Identify value for EACH path combination
3. Compute probability for EACH path precisely
4. Multiply path values by their exact probabilities
5. Sum all path-specific expected values
6. Verify probability weights sum to 1

**Example (sanitized):**
> **Scenario:** Computing expected stock value across multiple periods
> **Wrong approach:** Partial path consideration
> **Correct approach:**
> - Enumerate all possible paths
> - Calculate exact probability for each path
> - Compute weighted sum of path values