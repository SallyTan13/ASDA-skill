Based on the failure cases, I'll extract the distinct skill patterns:

## Pattern: Risk-Adjusted Performance Measurement Precision

**Description:** Financial performance metrics require careful calculation that goes beyond simple return comparisons, involving precise normalization of returns against risk.

**When to Use:** Performance evaluation questions involving Sharpe ratio, Jensen alpha, or other risk-adjusted metrics

**Procedure:**
1. Identify the specific performance metric being used (Sharpe, Jensen, etc.)
2. Carefully calculate excess return by subtracting risk-free rate
3. Normalize excess return by appropriate risk measure (standard deviation, beta)
4. Do NOT rely on raw return or intuitive ranking
5. Verify calculation by checking each component systematically
6. Double-check units and scaling of inputs

**Example (sanitized):**
> **Scenario:** Comparing fund performance with 4% risk-free rate
> **Wrong approach:** Picking fund with highest raw return
> **Correct approach:** 
> - Calculate excess return for each fund
> - Divide excess return by appropriate risk measure
> - Select fund with highest risk-adjusted return ratio

## Pattern: Index Calculation Nuance Detection

**Description:** Index return calculations require careful handling of complex adjustments like stock splits, share outstanding changes, and weighting methodologies.

**When to Use:** Questions involving price-weighted, value-weighted, or other index return calculations

**Procedure:**
1. Identify the specific index weighting methodology
2. Check for potential adjustment events (splits, share changes)
3. Normalize prices/shares before calculating returns
4. Apply correct weighting mechanism
5. Verify calculation matches index construction rules
6. Do NOT use simplistic return averaging

**Example (sanitized):**
> **Scenario:** Technology stock index with recent stock split
> **Wrong approach:** Simple return averaging
> **Correct approach:** 
> - Adjust stock prices for split
> - Calculate weighted returns based on index methodology
> - Verify total index calculation matches construction rules

## Pattern: Probabilistic Statistical Calculation Precision

**Description:** Probability-based statistical calculations require meticulous application of weighted variance and standard deviation formulas.

**When to Use:** Questions involving discrete probability distributions, risk calculations

**Procedure:**
1. Calculate expected value by probability-weighted returns
2. Compute variance using squared deviations from expected value
3. Weight each deviation by its corresponding probability
4. Take square root of variance for standard deviation
5. Verify each computational step
6. Check that probabilities sum to 1.0

**Example (sanitized):**
> **Scenario:** Portfolio return distribution across economic scenarios
> **Wrong approach:** Naive variance calculation
> **Correct approach:**
> - Compute weighted expected return
> - Calculate squared deviations
> - Weight deviations by scenario probabilities
> - Compute standard deviation systematically

## Pattern: Performance Metric Systematic Risk Adjustment

**Description:** Performance metrics like Jensen alpha require precise calculation of expected return based on systematic risk and market risk premium.

**When to Use:** Questions evaluating fund performance relative to market benchmark

**Procedure:**
1. Calculate expected return using CAPM framework
2. Use beta to adjust market risk premium
3. Compare actual return to systematically expected return
4. Compute excess return after risk adjustment
5. Verify each component of calculation
6. Do NOT confuse raw return with risk-adjusted performance

**Example (sanitized):**
> **Scenario:** Mutual fund performance evaluation
> **Wrong approach:** Simple return comparison
> **Correct approach:**
> - Calculate market risk premium
> - Adjust expected return using fund's beta
> - Compare actual return to systematic expectation
> - Compute risk-adjusted excess return

These patterns capture the key reasoning failures across the provided cases, focusing on precise financial calculation techniques and systematic approach to performance evaluation.