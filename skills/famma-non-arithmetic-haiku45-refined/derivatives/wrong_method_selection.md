# Skill Patterns for Derivatives - Wrong Method Selection

## Pattern: Futures Beta Adjustment Formula

**Description:** When adjusting portfolio beta using index futures, the correct formula accounts for futures as a leveraged overlay that modifies risk exposure without changing the underlying portfolio value. The denominator remains the original portfolio value, not the sum of portfolio plus futures notional. When multiple tasks are mentioned in the same context (e.g., beta adjustment AND cash equitization), identify the specific question being asked and apply only the relevant calculation.

**When to Use:** Questions involving "adjust beta," "change beta," "target beta," "modify risk exposure," or "number of contracts needed" using futures contracts on equity indices. Also applies when the question asks for contracts to achieve a specific beta adjustment, even when other portfolio activities (cash donations, rebalancing, equitization) are mentioned in the context.

**Procedure:**
1. **Identify the specific question scope:** Determine exactly what is being asked (e.g., "contracts to adjust beta" vs. "contracts to equitize cash" vs. "total contracts for all activities")
2. Extract only the relevant parameters for the specific question:
   - For beta adjustment: current portfolio value (V_p), current beta (β_current), and target beta (β_target)
   - Do NOT include cash awaiting investment, pending donations, or other funds unless the question explicitly asks to incorporate them
3. Extract futures contract specifications: price per contract (F), and futures beta (β_f)
4. Apply the correct beta adjustment formula: N_f = [V_p × (β_target - β_current)] / (F × β_f)
   - The numerator represents the dollar beta change needed
   - The denominator represents the dollar beta contribution per futures contract
5. Do NOT add futures notional value to the portfolio value in any calculation
6. Do NOT treat futures as a cash investment that increases total portfolio size
7. Do NOT combine separate tasks (e.g., adding contracts for cash equitization when only beta adjustment is asked)
8. Verify: The number of contracts should be proportional to the beta change (β_target - β_current), not to the target beta itself
9. Check sign: positive N_f means buy futures (increase beta), negative means sell futures (decrease beta)
10. If the question mentions multiple activities but asks only about one specific task, calculate only for that task

**Example (sanitized):**
> **Scenario:** A $75 million portfolio with beta 1.05 needs adjustment to beta 0.85. The portfolio manager also mentions that a $10 million cash donation will arrive next month and will need to be equitized. Futures contracts are priced at $180,000 with beta 0.95. The question asks: "How many contracts are needed to adjust the portfolio beta?"
> **Wrong approach:** Calculate contracts for both the beta adjustment ($75M) and the cash equitization ($10M), then sum them: [$75M × (0.85 - 1.05)] / ($180,000 × 0.95) + [$10M / ($180,000 × 0.95)] = -88 + 58 = -30 contracts total.
> **Correct approach:** The question asks specifically about adjusting the portfolio beta, not about equitizing the donation. Use only the existing portfolio: N_f = [$75M × (0.85 - 1.05)] / ($180,000 × 0.95) = [$75M × (-0.20)] / $171,000 = -$15M / $171,000 ≈ -88 contracts. Sell 88 contracts to reduce beta from 1.05 to 0.85. The cash donation is contextual information but not part of this specific calculation.

**Common Mistakes to Avoid:**
- Combining multiple portfolio activities (beta adjustment, cash equitization, rebalancing) when the question asks only about one specific task
- Including pending cash donations or uninvested funds in the portfolio value when the question asks to adjust the beta of the existing portfolio
- Calculating "total contracts needed" when the question asks for contracts for a specific purpose
- Failing to identify the precise scope of what is being asked versus what is mentioned for context
## Pattern: Effective Beta Verification from Realized Returns

**Description:** To verify whether a beta adjustment hedge was effective, calculate the effective (realized) beta from actual portfolio and market returns, then compare to the target beta. When futures or other derivatives are used in the hedge, the portfolio return must include the combined effect of both the underlying portfolio and the derivative positions. A hedge that produces offsetting gains may still be ineffective if the realized beta differs significantly from the target.

**When to Use:** Questions asking to evaluate "effectiveness," "success," or "appropriateness" of a completed futures hedge for beta adjustment, especially when actual return data is provided for both the underlying portfolio and derivative positions.

**Procedure:**
1. Identify the actual market/benchmark return (R_m) during the hedge period
2. Determine the total portfolio return (R_p):
   - If only a single portfolio return is given, use that value directly
   - If separate returns are provided for the underlying portfolio and derivative positions:
     a. Calculate the dollar gain/loss from the derivative position
     b. Calculate the dollar gain/loss from the underlying portfolio
     c. Sum the dollar gains/losses to get total portfolio dollar change
     d. Divide by the original portfolio value to get R_p = (Total Dollar Change) / (Portfolio Value)
3. Calculate the effective beta: β_effective = R_p / R_m
4. Compare β_effective to the target beta (β_target) specified in the hedge objective
5. Do NOT evaluate effectiveness based solely on whether the hedge produced gains or losses
6. Do NOT assume effectiveness simply because derivatives moved in the offsetting direction
7. Do NOT use only the underlying portfolio return when derivatives contributed to total performance
8. Determine effectiveness threshold: typically, β_effective should be within a reasonable range of β_target (e.g., ±0.05 to ±0.10 depending on context)
9. If β_effective is significantly above β_target, the hedge was insufficient (under-hedged)
10. If β_effective is significantly below β_target, the hedge was excessive (over-hedged)
11. If β_effective is within the acceptable range of β_target, the hedge was effective

**Example (sanitized):**
> **Scenario:** A $200M portfolio with target beta 0.60 used index futures to reduce systematic risk. During the evaluation period, the underlying equity portfolio declined 3.2% while the market index declined 4.0%. The short futures position generated a gain of $2.4M.
> **Wrong approach:** Calculate β_effective = -3.2% / -4.0% = 0.80, ignoring the futures gains, and conclude the hedge was ineffective because 0.80 > 0.60.
> **Correct approach:** 
> - Underlying portfolio loss: $200M × (-3.2%) = -$6.4M
> - Futures gain: +$2.4M
> - Total portfolio change: -$6.4M + $2.4M = -$4.0M
> - Total portfolio return: -$4.0M / $200M = -2.0%
> - β_effective = -2.0% / -4.0% = 0.50
> - Compare to target of 0.60: Since 0.50 is within reasonable range of 0.60 (difference of 0.10), the hedge was effective at reducing portfolio beta to near the target level.

**Common Mistakes to Avoid:**
- Using only the underlying portfolio return when derivative positions contributed to total performance
- Ignoring the dollar impact of derivative gains/losses when calculating combined portfolio return
- Concluding effectiveness based on whether derivatives generated profits rather than whether target beta was achieved
- Failing to combine all portfolio components before calculating effective beta

---
## Pattern: Futures Notional Exposure vs. Cash Investment

**Description:** Futures contracts provide leveraged notional exposure without requiring full capital outlay. When calculating portfolio modifications using futures, distinguish between the futures' notional value (contract price × multiplier) used for risk calculations and the actual cash required (margin), which does not affect portfolio allocation percentages.

**When to Use:** Any derivative overlay strategy involving "synthetic," "equitize," "modify allocation," or "adjust exposure" using futures, especially when the question involves portfolio weights or total portfolio value.

**Procedure:**
1. Recognize that buying/selling futures does NOT change the cash portfolio value
2. For risk calculations (beta, duration), use the futures notional value: Notional = Contract Price × Number of Contracts
3. For portfolio allocation calculations, keep the original portfolio value unchanged in the denominator
4. When calculating new effective exposure: Effective Exposure = Original Position + (Futures Notional × Futures Risk Parameter)
5. Do NOT add futures notional to total portfolio value when computing allocation percentages
6. Do NOT subtract futures notional from cash positions unless explicitly closing out cash to meet margin
7. Verify: After adding futures overlay, sum of cash positions should remain approximately constant (ignoring small margin requirements)

**Example (sanitized):**
> **Scenario:** $100M portfolio (60% stocks, 40% bonds) uses futures to shift to 55% stocks, 45% bonds. Stock futures price is $300,000, beta 1.10.
> **Wrong approach:** Calculate contracts needed by treating futures as cash: sell $5M stocks, buy $5M bond futures, adding $5M to portfolio total.
> **Correct approach:** Keep portfolio at $100M. To reduce stock exposure by $5M: sell N_f = $5M / ($300,000 × 1.10) ≈ 15 stock futures contracts. Buy corresponding bond futures. Cash positions remain 60/40, but effective exposure becomes 55/45 through futures overlay.

---

## Pattern: Incremental vs. Total Contracts for Portfolio Adjustment

**Description:** When adjusting portfolio characteristics using futures, calculate the incremental number of contracts needed to achieve the change from current to target state, not the total contracts needed to replicate the entire target portfolio.

**When to Use:** Questions involving "adjust," "change," "modify," or "shift" portfolio characteristics (beta, duration, allocation) from one level to another using derivatives.

**Procedure:**
1. Identify the current state (current beta, current allocation, current duration)
2. Identify the target state (target beta, target allocation, target duration)
3. Calculate the incremental change needed: Δ = Target - Current
4. Apply formulas using the incremental change (Δ), not the target level
5. For beta: N_f = [V_p × (β_target - β_current)] / (F × β_f), where the key term is the difference
6. For allocation shifts: calculate contracts based on the dollar amount being shifted, not the target allocation amount
7. Do NOT calculate contracts as if building the entire target portfolio from scratch
8. Verify: If current already equals target, the formula should yield zero contracts

**Example (sanitized):**
> **Scenario:** $80M portfolio, current beta 1.30, target beta 1.10. Futures: $200,000 price, beta 1.00.
> **Wrong approach:** N_f = ($80M × 1.10) / ($200,000 × 1.00) = 440 contracts (building entire 1.10 beta position).
> **Correct approach:** N_f = [$80M × (1.10 - 1.30)] / ($200,000 × 1.00) = [$80M × (-0.20)] / $200,000 = -80 contracts. Sell 80 contracts to reduce beta by 0.20.

## Pattern: Duration-Based Swap Notional Verification

**Description:** When evaluating whether a proposed swap notional principal is correct for a duration adjustment strategy, calculate the theoretically required notional using the duration formula, then compare the calculated value to the proposed value using explicit tolerance thresholds. Small differences may be acceptable due to rounding, but material differences indicate the notional is too high or too low.

**When to Use:** Questions asking to verify, evaluate, or determine if a swap notional principal is "correct," "appropriate," or "most likely correct" for achieving a specific duration target, especially when both a proposed notional and sufficient data to calculate the required notional are provided.

**Procedure:**
1. Extract the given information:
   - Portfolio market value (V_p)
   - Current portfolio duration (D_current)
   - Target portfolio duration (D_target)
   - Swap duration (D_swap) - use negative value for pay-fixed swaps
   - Proposed/recommended notional principal (N_proposed)
2. Calculate the required duration change: ΔD = D_target - D_current
3. Apply the duration-based swap formula: N_calculated = (V_p × ΔD) / D_swap
4. Compare N_calculated to N_proposed:
   - Calculate the difference: Difference = N_proposed - N_calculated
   - Calculate the percentage difference: % Difference = (Difference / N_calculated) × 100%
5. Apply tolerance thresholds to determine correctness:
   - If |% Difference| ≤ 2%: The notional is correct (acceptable rounding)
   - If % Difference > 2%: The notional is too high
   - If % Difference < -2%: The notional is too low
6. Do NOT rationalize material differences as "reasonable" without quantitative justification
7. Do NOT assume expert recommendations are automatically correct without verification
8. Verify the sign: For pay-fixed swaps (reducing duration), notional should be positive; for receive-fixed swaps (increasing duration), notional should be positive but applied differently

**Example (sanitized):**
> **Scenario:** A bond portfolio valued at $500M with duration 7.2 needs to be adjusted to duration 5.0. An analyst recommends using a pay-fixed interest rate swap with duration -3.6 and notional principal of $320M.
> **Wrong approach:** Assume the recommendation is correct because the analyst is experienced, or rationalize that "$320M seems reasonable for this size portfolio."
> **Correct approach:**
> - Duration change needed: ΔD = 5.0 - 7.2 = -2.2
> - Calculate required notional: N_calculated = ($500M × -2.2) / -3.6 = $1,100M / 3.6 = $305.56M
> - Compare to proposed: Difference = $320M - $305.56M = $14.44M
> - Percentage difference: ($14.44M / $305.56M) × 100% = 4.7%
> - Since 4.7% > 2%, the notional of $320M is too high. The correct answer is that the notional is too high.

**Common Mistakes to Avoid:**
- Accepting proposed values without calculating the theoretically required amount
- Rationalizing material differences (>2-3%) as "acceptable" or "reasonable" without quantitative basis
- Confusing the direction of adjustment (increasing vs. decreasing duration) when interpreting swap duration signs
- Using target duration instead of duration change (ΔD) in the numerator