# Pattern: Price-Weighted Index Divisor Adjustment After Stock Splits

**Description:** When a stock split occurs in a price-weighted index, the new divisor must be calculated by preserving the index value immediately before the split, not by using a ratio of price sums. The correct approach requires setting (post-split price sum)/(new divisor) equal to the pre-split index value.

**When to Use:** Questions involving price-weighted indices, stock splits, divisor adjustments, or index continuity maintenance. Keywords: "divisor," "price-weighted index," "stock split," "adjust."

**Procedure:**
1. Calculate the pre-split index value: sum all stock prices immediately before the split, then divide by the current divisor
2. Identify which stock(s) underwent splits and determine the post-split prices (typically price divided by split ratio, e.g., 2-for-1 split halves the price)
3. Calculate the post-split price sum: add all stock prices using the new split-adjusted prices
4. Solve for the new divisor using the continuity equation: (post-split price sum) / (new divisor) = (pre-split index value)
5. Verify: compute the index using the new divisor and confirm it equals the pre-split index value, ensuring no artificial jump due to the split

**Example (sanitized):**
> **Scenario:** Three stocks in a price-weighted index have prices of $80, $60, and $120 with divisor 3. The third stock splits 3-for-1.
> **Wrong approach:** New divisor = 3 × (80+60+40)/(80+60+120) = 3 × (180/260) = 2.08
> **Correct approach:** (1) Pre-split index = (80+60+120)/3 = 86.67, (2) Post-split prices: 80, 60, 40, (3) Post-split sum = 180, (4) Solve 180/D = 86.67 → D = 2.08. Wait, this matches! Let me recalculate: Actually 180/86.67 = 2.077, so new divisor ≈ 2.08.

---

# Pattern: Arithmetic Self-Contradiction and Verification Failure

**Description:** When performing multi-step calculations (especially variance, standard deviation, or utility functions), models may correctly execute arithmetic but then override correct results with unjustified "more precise" values, or correctly compute all intermediate values but fail at the final comparison/selection step.

**When to Use:** Questions requiring variance/standard deviation calculations, utility comparisons, or any multi-option selection based on computed metrics. Keywords: "calculate," "standard deviation," "variance," "which investment," "select."

**Procedure:**
1. Perform all calculations step-by-step with explicit intermediate values shown
2. For each calculation, write down the result immediately and label it clearly
3. Before stating a "more precise" or "corrected" value, explicitly show the mathematical justification (additional decimal places, different formula, etc.)
4. For comparison problems, create a summary table listing all computed values side-by-side
5. Identify the maximum/minimum by direct numerical comparison of the summary values
6. Cross-check: verify the selected option actually corresponds to the identified max/min value
7. Never override a correctly calculated result without explicit mathematical evidence that the original was wrong

**Example (sanitized):**
> **Scenario:** Calculate utility U = E(r) - 2σ² for three portfolios: A (E=0.10, σ=0.15), B (E=0.12, σ=0.18), C (E=0.14, σ=0.20). Select the best.
> **Wrong approach:** U_A = 0.10 - 2(0.0225) = 0.055, U_B = 0.12 - 2(0.0324) = 0.0552, U_C = 0.14 - 2(0.04) = 0.06. Portfolio C has the highest utility... wait, using more precise calculations, Portfolio B is actually best.
> **Correct approach:** (1) U_A = 0.10 - 2(0.15²) = 0.10 - 0.045 = 0.055, (2) U_B = 0.12 - 2(0.18²) = 0.12 - 0.0648 = 0.0552, (3) U_C = 0.14 - 2(0.20²) = 0.14 - 0.08 = 0.06, (4) Summary: U_A=0.055, U_B=0.0552, U_C=0.06, (5) Maximum is 0.06, (6) This corresponds to Portfolio C. Answer: C.

---

# Pattern: Decimal Precision in Squared Terms and Products

**Description:** When formulas involve squaring decimal values (especially in variance, standard deviation, or utility functions), maintain sufficient decimal precision throughout calculations and verify that squared values are computed correctly before using them in subsequent operations.

**When to Use:** Calculations involving σ², variance formulas, utility functions with quadratic terms, or any formula requiring squaring of decimal probabilities or percentages. Keywords: "variance," "standard deviation," "utility," "squared."

**Procedure:**
1. When squaring a decimal value, write out the operation explicitly: (0.XX)² = 0.YYYY
2. Maintain at least 4-6 decimal places in intermediate squared values before rounding
3. For variance calculations: compute each (x - μ)² term separately and verify the squared deviation before multiplying by probability
4. For products involving squared terms: perform the multiplication step-by-step (e.g., A/2 × σ² = [A/2] × [σ²])
5. Sum all weighted components and show the intermediate sum before taking square roots or making final comparisons
6. Verification: for comparison problems, recalculate the top 2-3 candidates to confirm ranking

**Example (sanitized):**
> **Scenario:** Calculate variance for returns: 40% probability of 8%, 60% probability of 12%. Mean = 0.4(0.08) + 0.6(0.12) = 0.104.
> **Wrong approach:** Variance = 0.4(0.08-0.104)² + 0.6(0.12-0.104)² = 0.4(0.000576) + 0.6(0.000256) ≈ 0.00038
> **Correct approach:** (1) Mean = 0.032 + 0.072 = 0.104, (2) First deviation: (0.08-0.104)² = (-0.024)² = 0.000576, (3) Second deviation: (0.12-0.104)² = (0.016)² = 0.000256, (4) Weighted: 0.4(0.000576) = 0.0002304, (5) Weighted: 0.6(0.000256) = 0.0001536, (6) Variance = 0.0002304 + 0.0001536 = 0.000384.