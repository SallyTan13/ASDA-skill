# Alternative Investments — Portfolio Management and Planning Gaps

## Pattern: life_insurance_needs_analysis

**Description:** Life insurance needs analysis using the needs analysis method requires calculating the present value of future living expenses for dependents, then offsetting this with the present value of the surviving spouse's income and existing assets to determine net insurance needs.

**When to Use:** Questions asking to "calculate life insurance needs," "determine insurance coverage," or "needs analysis method" for individuals with dependents and income streams.

**Procedure:**
1. Calculate PV of future living expenses for dependents (typically until children are independent or spouse reaches retirement)
2. Calculate PV of surviving spouse's future income stream
3. Identify existing financial assets available to offset needs
4. Net insurance need = PV(living expenses) - PV(surviving spouse income) - existing assets
5. Perform calculation separately for each spouse if both have coverage needs
6. Key distinction: Surviving spouse income is an OFFSET (reduces needs), not an additional need

**Example (sanitized):**
> **Scenario:** A couple has two children. Spouse A earns $80,000/year, Spouse B earns $50,000/year. Annual living expenses are $60,000. They have $100,000 in savings. Children need support for 15 years. Discount rate is 4%.
> **Wrong approach:** Adding surviving spouse's income to the needs: PV(expenses) + PV(surviving income) + other needs
> **Correct approach:** 
> - For Spouse A: PV(expenses if A dies) - PV(Spouse B's income) - existing assets = insurance need
> - For Spouse B: PV(expenses if B dies) - PV(Spouse A's income) - existing assets = insurance need
> - The surviving spouse's income REDUCES the insurance needed, not increases it

---

## Pattern: rebalancing_band_width_design

**Description:** Rebalancing band widths should be proportional to asset class volatility and inversely proportional to transaction costs. High-volatility assets need wider bands; low-volatility assets need narrower bands. Illiquid assets with high transaction costs need wider bands.

**When to Use:** Questions about "rebalancing policy," "tolerance bands," "rebalancing band adjustment," or evaluating whether current bands are appropriate for asset classes.

**Procedure:**
1. Identify the volatility characteristics of each asset class (cash < bonds < public equity < private equity/alternatives)
2. Identify transaction costs and liquidity (cash is most liquid, private equity least liquid)
3. Apply principle: Band width should increase with volatility
4. Apply principle: Band width should increase with transaction costs/illiquidity
5. Flag mismatches: Low-volatility assets with wide bands (too permissive)
6. Flag mismatches: High-volatility assets with narrow bands (too restrictive, excessive rebalancing)
7. Recommend adjustments: Narrow bands for stable assets, widen bands for volatile/illiquid assets

**Example (sanitized):**
> **Scenario:** Portfolio has: Cash (±5% band), Bonds (±3% band), Public Equity (±4% band), Private Equity (±2% band)
> **Wrong approach:** Identifying assets currently near their band limits as needing adjustment
> **Correct approach:** 
> - Cash has very low volatility but wide (±5%) band → band too wide, should be narrower (e.g., ±2%)
> - Private Equity has high volatility and high transaction costs but narrow (±2%) band → band too narrow, should be wider (e.g., ±6%)
> - The mismatch between volatility/costs and band width indicates need for adjustment, regardless of current allocation position

---

## Pattern: illiquid_asset_rebalancing_mechanisms

**Description:** Portfolios with significant illiquid assets require specialized rebalancing mechanisms because direct rebalancing is costly or impossible. Strategies include calendar rebalancing with wide bands, percent-range rebalancing with asymmetric triggers, or synthetic rebalancing using correlated liquid assets.

**When to Use:** Questions about managing portfolios with private equity, real estate, or other illiquid holdings; concerns about "risk profile drift," "rebalancing illiquid assets," or "maintaining target allocations" with liquidity constraints.

**Procedure:**
1. Recognize that illiquid assets cannot be easily rebalanced due to high transaction costs and limited marketability
2. Identify available rebalancing mechanisms:
   - Calendar rebalancing: Rebalance at fixed intervals (annual, semi-annual) with pre-specified tolerance bands
   - Percent-range rebalancing: Set wider tolerance bands for illiquid assets, trigger rebalancing only when bands are breached
   - Synthetic/automatic rebalancing: Adjust correlated liquid asset positions (e.g., public equity) to offset illiquid asset drift (e.g., private equity)
3. Ensure sufficient liquid assets are maintained to enable rebalancing without forced sales of illiquid positions
4. Recognize that risk profile drift is most dangerous during market stress when correlations increase and liquidity decreases
5. Recommend periodic stress testing to ensure rebalancing capacity under adverse conditions

**Example (sanitized):**
> **Scenario:** An endowment has 30% in private equity (target 25%) and 40% in public equity (target 45%). Market decline has caused drift.
> **Wrong approach:** Recommending immediate sale of private equity to rebalance back to targets
> **Correct approach:** 
> - Direct rebalancing of private equity is impractical due to illiquidity and high costs
> - Use synthetic rebalancing: Reduce public equity exposure below its 45% target to offset the private equity overweight
> - Since private equity and public equity are correlated, underweighting public equity partially hedges the private equity overweight
> - Implement calendar rebalancing with wide bands (e.g., ±5%) for private equity to avoid excessive rebalancing attempts
> - Ensure sufficient cash/liquid assets to meet spending needs without forced liquidations during stress periods

---

## Pattern: liquidity_budget_stress_testing

**Description:** Liquidity budgets establish minimum liquid asset thresholds and maximum illiquid asset limits. When allocation changes move the portfolio closer to these limits, stress testing and enhanced monitoring are required to ensure compliance under adverse market conditions.

**When to Use:** Questions about "liquidity concerns," "stress conditions," "liquidity budget compliance," or evaluating proposed allocation changes that increase illiquid holdings.

**Procedure:**
1. Calculate current liquidity profile under normal conditions (% liquid, semi-liquid, illiquid)
2. Calculate proposed liquidity profile after allocation changes
3. Compare to liquidity budget thresholds (minimum liquid %, maximum illiquid %)
4. If moving closer to limits, identify required actions:
   - Implement periodic stress testing (simulate market declines, redemption requests, funding needs)
   - Enhance monitoring frequency for liquidity metrics
   - Establish contingency plans for liquidity shortfalls
   - Ensure rebalancing mechanisms can function without violating liquidity constraints
5. Recognize that asset liquidity decreases during market stress (semi-liquid may become illiquid)
6. Plan for worst-case scenarios where multiple liquidity demands coincide with reduced asset marketability

**Example (sanitized):**
> **Scenario:** Foundation has liquidity budget requiring ≥30% liquid assets, ≤40% illiquid assets. Current: 45% liquid, 25% illiquid. Proposal: shift 5% from liquid to illiquid. New allocation: 40% liquid, 30% illiquid.
> **Wrong approach:** Approving the change because it still meets the liquidity budget requirements
> **Correct approach:**
> - The proposal moves from 45% to 40% liquid (now at the minimum threshold with no buffer)
> - Under stress conditions, currently semi-liquid assets may become illiquid, potentially violating the 40% illiquid maximum
> - Required actions before implementing:
>   * Conduct stress tests showing liquidity profile under -20%, -30% market declines
>   * Establish monthly (vs. quarterly) monitoring of liquidity metrics
>   * Ensure rebalancing mechanism doesn't require selling illiquid assets during stress
>   * Create contingency funding plan if liquid assets are depleted
> - The reduced margin of safety requires enhanced governance and monitoring

---

## Pattern: bottom_up_liquidity_calculation_verification

**Description:** Bottom-up liquidity analysis multiplies each asset class allocation by its liquidity classification percentages, then aggregates across all asset classes. Verification requires careful arithmetic and cross-checking that all components sum correctly.

**When to Use:** Questions requiring "liquidity analysis," "bottom-up calculation," or determining the portfolio's overall liquidity profile from individual asset class characteristics.

**Procedure:**
1. For each asset class, identify: (a) portfolio allocation %, (b) % classified as liquid, (c) % classified as semi-liquid, (d) % classified as illiquid
2. Verify that for each asset class: %Liquid + %Semi-liquid + %Illiquid = 100%
3. Calculate total liquid: Σ(Asset class allocation × %Liquid) across all asset classes
4. Calculate total semi-liquid: Σ(Asset class allocation × %Semi-liquid) across all asset classes
5. Calculate total illiquid: Σ(Asset class allocation × %Illiquid) across all asset classes
6. Verification check: Total liquid + Total semi-liquid + Total illiquid should equal 100%
7. Compare results to liquidity budget requirements
8. Identify capacity for reallocation if current profile has significant buffer from limits

**Example (sanitized):**
> **Scenario:** Portfolio: 5% Cash (100% liquid), 30% Bonds (100% liquid), 40% Public Equity (60% liquid, 40% semi-liquid), 25% Private Equity (100% illiquid). Liquidity budget requires ≥35% liquid, ≤35% illiquid.
> **Wrong approach:** Estimating or rounding intermediate calculations, leading to arithmetic errors
> **Correct approach:**
> - Liquid = (5% × 100%) + (30% × 100%) + (40% × 60%) + (25% × 0%) = 5% + 30% + 24% + 0% = 59%
> - Semi-liquid = (5% × 0%) + (30% × 0%) + (40% × 40%) + (25% × 0%) = 0% + 0% + 16% + 0% = 16%
> - Illiquid = (5% × 0%) + (30% × 0%) + (40% × 0%) + (25% × 100%) = 0% + 0% + 0% + 25% = 25%
> - Verification: 59% + 16% + 25% = 100% ✓
> - Analysis: 59% liquid >> 35% requirement (24% buffer); 25% illiquid < 35% limit (10% capacity)
> - Conclusion: Significant capacity to shift from liquid to illiquid assets if higher returns are available

---

## Pattern: allocation_change_impact_on_liquidity_profile

**Description:** When portfolio allocations change, the overall liquidity profile shifts based on the liquidity characteristics of the source and destination asset classes. Increasing illiquid assets reduces liquid assets and vice versa, affecting compliance with liquidity budgets.

**When to Use:** Questions about "proposed allocation changes," "impact on liquidity," "reallocation effects," or evaluating whether allocation shifts maintain liquidity budget compliance.

**Procedure:**
1. Identify the proposed allocation change (% moving from asset class X to asset class Y)
2. Determine liquidity classification of source asset class X (% liquid, semi-liquid, illiquid)
3. Determine liquidity classification of destination asset class Y (% liquid, semi-liquid, illiquid)
4. Calculate impact on each liquidity category:
   - Change in liquid = (% shifted × %Liquid_Y) - (% shifted × %Liquid_X)
   - Change in semi-liquid = (% shifted × %Semi-liquid_Y) - (% shifted × %Semi-liquid_X)
   - Change in illiquid = (% shifted × %Illiquid_Y) - (% shifted × %Illiquid_X)
5. Apply changes to current liquidity profile to get new profile
6. Compare new profile to liquidity budget requirements under both normal and stress conditions
7. Assess whether the change increases risk of violating liquidity constraints during market stress

**Example (sanitized):**
> **Scenario:** Current: 50% liquid, 20% semi-liquid, 30% illiquid. Proposal: shift 10% from Bonds (100% liquid) to Real Estate (20% semi-liquid, 80% illiquid). Liquidity budget: ≥40% liquid, ≤40% illiquid.
> **Wrong approach:** Only checking whether the new allocation meets the liquidity budget under normal conditions
> **Correct approach:**
> - Impact on liquid: (10% × 0%) - (10% × 100%) = -10%
> - Impact on semi-liquid: (10% × 20%) - (10% × 0%) = +2%
> - Impact on illiquid: (10% × 80%) - (10% × 0%) = +8%
> - New profile: 40% liquid, 22% semi-liquid, 38% illiquid
> - Normal conditions: Meets requirements (40% ≥ 40% liquid, 38% ≤ 40% illiquid)
> - Stress conditions: If semi-liquid becomes illiquid → 40% liquid, 0% semi-liquid, 60% illiquid
> - Stress analysis: Would violate 40% illiquid limit (60% > 40%)
> - Conclusion: Proposal creates unacceptable risk under stress conditions despite meeting normal requirements

---

SKILL_MD_ENTRY: | `alternative_investments/new_patterns.md` | Alternative Investments | Portfolio Management and Planning Gaps | life_insurance_needs_analysis, rebalancing_band_width_design, illiquid_asset_rebalancing_mechanisms, liquidity_budget_stress_testing, bottom_up_liquidity_calculation_verification, allocation_change_impact_on_liquidity_profile |