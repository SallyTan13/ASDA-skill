# Analysis of Failure Cases

## Pattern: Multi-Step Binomial Tree Arithmetic Verification

**Description:** When computing option prices using binomial trees with multiple time steps, arithmetic errors compound through backward induction. Models correctly apply the risk-neutral pricing framework but fail to verify intermediate node values and final discounted results with sufficient numerical precision.

**When to Use:** Binomial option pricing problems requiring backward induction through multiple periods; trigger keywords: "two-step," "multi-period," "binomial tree," "work backwards," "risk-neutral probability"

**Procedure:**
1. Calculate risk-neutral probability p = (e^(rΔt) - d)/(u - d) and verify it lies in (0,1)
2. Construct the complete tree: compute ALL terminal stock prices (e.g., S·u², S·u·d, S·d²)
3. Calculate ALL terminal option payoffs using the payoff formula (e.g., max(K-S,0) for puts)
4. Perform backward induction ONE step at a time: for each node, compute V = e^(-rΔt)[p·V_up + (1-p)·V_down]
5. **Verification step:** After computing each node value, independently recalculate it to confirm accuracy before proceeding
6. **Final check:** Verify the present value by re-computing from scratch using the final formula to catch accumulated rounding errors
7. Round only at the final answer, maintaining at least 4 decimal places in intermediate calculations

**Example (sanitized):**
> **Scenario:** A 6-month option with two 3-month periods, S₀=$50, u=1.08, d=0.95, r=0.06, K=$52 (put option)
> **Wrong approach:** Computing p=0.52, then calculating node values as $3.20 (up) and $8.50 (down), yielding final value $5.85 without verifying intermediate steps
> **Correct approach:** (1) p = (e^0.015 - 0.95)/(1.08-0.95) = 0.5038; (2) Terminal prices: $58.32, $51.30, $45.13; (3) Terminal payoffs: $0, $0.70, $6.87; (4) Up-node at t=3mo: e^(-0.015)[0.5038×0 + 0.4962×0.70] = $0.34; Down-node: e^(-0.015)[0.5038×0.70 + 0.4962×6.87] = $3.70; (5) Verify up-node: 0.985×0.347 = $0.34 ✓; (6) Present value: e^(-0.015)[0.5038×0.34 + 0.4962×3.70] = $1.98; (7) Independent check confirms $1.98

---

## Pattern: Forward Price Calculation with Coupon Adjustment

**Description:** When pricing bond options using Black's model, errors occur in computing the forward bond price when coupons are paid during the option's life. The present value of coupons must be subtracted from the spot bond price before dividing by the discount factor.

**When to Use:** European bond option pricing with Black's model when coupons are paid before expiration; trigger keywords: "bond option," "coupon paid," "forward bond price," "Black's model," "cash price"

**Procedure:**
1. Identify all coupons paid during the option's life (from now until option expiration T)
2. Calculate present value of each coupon: I = Σ(Coupon × e^(-r×t_i)) where t_i is time to each coupon payment
3. Compute forward bond price: F_B = (B₀ - I) / P(0,T) where P(0,T) = e^(-r×T)
4. **Verification:** Check that F_B > B₀ - I (forward should exceed spot minus coupons for positive rates)
5. Calculate d₁ = [ln(F_B/K) + (σ²/2)T] / (σ√T) maintaining full precision
6. Calculate d₂ = d₁ - σ√T
7. Look up N(d₁) and N(d₂) using accurate normal distribution tables (at least 4 decimal places)
8. Apply Black's formula: p = P(0,T)[K·N(-d₂) - F_B·N(-d₁)] for puts
9. **Final verification:** Recalculate using the complete formula in one pass to verify each component

**Example (sanitized):**
> **Scenario:** 10-month put option on bond, B₀=$950, K=$940, σ=12%, r=7%, coupon of $40 in 4 months
> **Wrong approach:** Using F_B = 950/e^(-0.07×10/12) = $1006 without adjusting for the coupon
> **Correct approach:** (1) I = 40×e^(-0.07×4/12) = $39.08; (2) F_B = (950-39.08)/e^(-0.07×10/12) = 910.92/0.9435 = $965.55; (3) Verify: 965.55 > 910.92 ✓; (4) d₁ = [ln(965.55/940) + 0.0072×10/12]/(0.12×√(10/12)) = 0.2348; (5) d₂ = 0.1251; (6) N(-d₂)=0.4502, N(-d₁)=0.4072; (7) p = 0.9435×[940×0.4502 - 965.55×0.4072] = $28.64

---

## Pattern: Duration-Based Swap Notional Verification

**Description:** When using interest rate swaps to adjust portfolio duration, the notional principal calculation requires precise application of the formula NP = (MV × ΔD) / D_swap. Models accept incorrect results when the computed value differs materially from the stated answer without performing independent verification arithmetic.

**When to Use:** Duration management with interest rate swaps; trigger keywords: "duration," "interest rate swap," "notional principal," "pay-fixed," "receive-fixed"

**Procedure:**
1. Identify target duration (D_target), current portfolio duration (D_current), and portfolio market value (MV)
2. Calculate required duration change: ΔD = D_target - D_current (note the sign)
3. Identify swap duration (D_swap) — use absolute value and note that pay-fixed swaps have negative duration impact
4. Apply formula: NP = (MV × |ΔD|) / |D_swap|
5. **Critical verification:** Independently compute NP using the formula with exact values (no premature rounding)
6. Compare computed NP with any stated value: if difference exceeds 2%, flag as likely incorrect
7. Check directional consistency: pay-fixed to reduce duration (ΔD < 0), receive-fixed to increase duration (ΔD > 0)
8. Verify magnitude reasonableness: NP should be similar to MV (typically 0.5× to 2× MV for typical duration adjustments)

**Example (sanitized):**
> **Scenario:** Portfolio MV=$500M, D_current=7.2, D_target=4.0, swap D_swap=-3.1 (pay-fixed), stated NP=$550M
> **Wrong approach:** Accepting $550M as "reasonable" because it's close to portfolio value without calculating
> **Correct approach:** (1) ΔD = 4.0 - 7.2 = -3.2; (2) |ΔD| = 3.2; (3) |D_swap| = 3.1; (4) NP = (500 × 3.2) / 3.1 = 1600/3.1 = $516.13M; (5) Stated value $550M differs by $33.87M (6.6% error); (6) Conclusion: stated notional is too high; (7) Correct answer is approximately $516M

---

## Pattern: Conditional Expectation Path Probability Calculation

**Description:** When computing conditional expectations in multi-period binomial models under actual (non-risk-neutral) probabilities, errors occur in tracking all possible paths from the conditioning state and correctly weighting each path's contribution by its compound probability.

**When to Use:** Computing expectations conditional on reaching a specific state in binomial trees with given actual probabilities; trigger keywords: "conditional expectation," "given state," "actual probability," "E[·|state]," "binomial model"

**Procedure:**
1. Identify the conditioning state (e.g., "state H at time 1") and all future time points in the expectation
2. Draw or enumerate ALL possible paths from the conditioning state to each future time point
3. For each path, calculate compound probability: multiply p or q for each step (e.g., path H→HH→HHT has probability p×p×q)
4. For each complete path, identify the values of all random variables in the expectation (e.g., S₂ and S₃)
5. Calculate expectation as: E = Σ[probability of path × (sum of values on that path)]
6. **Verification step:** Confirm probabilities sum to 1 across all paths from the conditioning state
7. Maintain exact fractions (e.g., 2/3, 1/3) throughout calculation; convert to decimal only for final answer
8. **Arithmetic check:** Recalculate the weighted sum independently to verify

**Example (sanitized):**
> **Scenario:** At state A (time 1), compute E[X₂ + X₃|A] with p=3/4, q=1/4; paths: A→AA (X₂=10, then AAA: X₃=20 or AAB: X₃=12) and A→AB (X₂=6, then ABA: X₃=12 or ABB: X₃=8)
> **Wrong approach:** E = (3/4)(10+16) + (1/4)(6+10) = 23.5, incorrectly averaging terminal values
> **Correct approach:** (1) Four paths: AAA (prob 9/16), AAB (prob 3/16), ABA (prob 3/16), ABB (prob 1/16); (2) Verify: 9/16+3/16+3/16+1/16=1 ✓; (3) E = (9/16)(10+20) + (3/16)(10+12) + (3/16)(6+12) + (1/16)(6+8) = (9/16)×30 + (3/16)×22 + (3/16)×18 + (1/16)×14 = 270/16 + 66/16 + 54/16 + 14/16 = 404/16 = 25.25; (4) Independent check: 16.875 + 4.125 + 3.375 + 0.875 = 25.25 ✓

---

## Pattern: Final Answer Transcription Verification

**Description:** After completing multi-step calculations correctly, errors occur when transcribing or rounding the final numerical result. The computed intermediate value (e.g., 30.67) is incorrectly reported as a different rounded value (e.g., 28) without justification.

**When to Use:** All numerical problems requiring final answer reporting, especially after complex calculations; trigger keywords: any problem requiring a specific numerical answer

**Procedure:**
1. Complete all calculation steps maintaining full precision (at least 4 decimal places)
2. Before reporting the final answer, write down the exact computed value (e.g., "computed value = 30.6667")
3. Check problem statement for rounding instructions (e.g., "round to nearest integer," "two decimal places")
4. If no rounding specified, check answer choices or ground truth format to determine appropriate precision
5. Apply rounding rule consistently: for "nearest integer," use standard rounding (0.5 rounds up)
6. **Critical check:** Compare rounded answer to computed value; if difference exceeds one rounding unit, re-examine calculation
7. State final answer explicitly: "Final answer: [value] [units]"
8. **Verification:** Does the final answer make economic/financial sense given the problem context?

**Example (sanitized):**
> **Scenario:** Calculated portfolio value = 1247.83, problem asks for "value in thousands"
> **Wrong approach:** Reporting 1200 or 1250 without clear rounding justification
> **Correct approach:** (1) Exact computed value = 1247.83; (2) Problem asks for "thousands" with no decimal specification; (3) Check if answer choices are in whole thousands (e.g., 1200, 1240, 1250); (4) If choices are 1240, 1250, 1260, round 1247.83 to nearest 10 → 1250; (5) If no choices given, report as 1248 (nearest whole thousand); (6) Verify: 1248 differs from 1247.83 by 0.17, within one rounding unit ✓; (7) Final answer: 1248 thousand or $1,248,000