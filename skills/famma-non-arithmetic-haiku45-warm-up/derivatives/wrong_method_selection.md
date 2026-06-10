# Skill Patterns for Derivatives - Wrong Method Selection

## Pattern: Futures Beta Adjustment Formula

**Description:** When adjusting portfolio beta using index futures, the correct formula accounts for futures as a leveraged overlay that modifies risk exposure without changing the underlying portfolio value. The denominator remains the original portfolio value, not the sum of portfolio plus futures notional.

**When to Use:** Questions involving "adjust beta," "change beta," "target beta," or "modify risk exposure" using futures contracts on equity indices.

**Procedure:**
1. Identify the current portfolio value (V_p), current beta (β_current), and target beta (β_target)
2. Extract futures contract specifications: price per contract (F), and futures beta (β_f)
3. Apply the correct beta adjustment formula: N_f = [V_p × (β_target - β_current)] / (F × β_f)
   - The numerator represents the dollar beta change needed
   - The denominator represents the dollar beta contribution per futures contract
4. Do NOT add futures notional value to the portfolio value in any calculation
5. Do NOT treat futures as a cash investment that increases total portfolio size
6. Verify: The number of contracts should be proportional to the beta change (β_target - β_current), not to the target beta itself
7. Check sign: positive N_f means buy futures (increase beta), negative means sell futures (decrease beta)

**Example (sanitized):**
> **Scenario:** A $50 million portfolio with beta 0.90 needs adjustment to beta 1.15. Futures contracts are priced at $250,000 with beta 1.05.
> **Wrong approach:** Calculate as ($50M × 1.15 + contracts × $250K × 1.05) / ($50M + contracts × $250K) = 1.15, treating futures as additional capital.
> **Correct approach:** N_f = [$50M × (1.15 - 0.90)] / ($250,000 × 1.05) = [$50M × 0.25] / $262,500 = $12.5M / $262,500 ≈ 48 contracts. The portfolio value stays $50M; futures provide leveraged beta exposure.

---

## Pattern: Effective Beta Verification from Realized Returns

**Description:** To verify whether a beta adjustment hedge was effective, calculate the effective (realized) beta from actual portfolio and market returns, then compare to the target beta. A hedge that produces offsetting gains may still be ineffective if the realized beta differs significantly from the target.

**When to Use:** Questions asking to evaluate "effectiveness," "success," or "appropriateness" of a completed futures hedge for beta adjustment, especially when actual return data is provided.

**Procedure:**
1. Identify the actual portfolio return (R_p) and actual market/benchmark return (R_m) during the hedge period
2. Calculate the effective beta: β_effective = R_p / R_m
3. Compare β_effective to the target beta (β_target) specified in the hedge objective
4. Do NOT evaluate effectiveness based solely on whether the hedge produced gains or losses
5. Do NOT assume effectiveness simply because futures moved in the offsetting direction
6. Determine effectiveness threshold: typically, β_effective should be within a reasonable range of β_target (e.g., ±0.05 to ±0.10 depending on context)
7. If β_effective is significantly above β_target, the hedge was insufficient (under-hedged)
8. If β_effective is significantly below β_target, the hedge was excessive (over-hedged)

**Example (sanitized):**
> **Scenario:** Portfolio with target beta 0.80 declined 4.8% when market declined 3.0%. Futures position generated offsetting gains.
> **Wrong approach:** Conclude the hedge was effective because futures produced gains that partially offset portfolio losses.
> **Correct approach:** Calculate β_effective = -4.8% / -3.0% = 1.60. Compare to target of 0.80. Since 1.60 >> 0.80, the hedge was ineffective—the portfolio remained far more volatile than intended despite the offsetting gains.

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