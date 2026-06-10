# Alternative Investments — Liquidity and Insurance Planning Analysis

## Pattern: Bottom_Up_Liquidity_Classification_Analysis

**Description:** Liquidity analysis requires treating asset classes with partial liquidity classifications (e.g., 50% liquid, 50% semi-liquid) by multiplying each allocation by its respective liquidity percentages and aggregating across all classes, not treating classifications as binary. Liquidity categories are mutually exclusive—each portion of an asset class contributes to exactly ONE liquidity category.

**When to Use:** 
- Questions involving "liquidity budget," "liquidity classification," or "bottom-up liquidity analysis"
- Scenarios with asset classes having multiple liquidity categories (liquid, semi-liquid, illiquid)
- When determining compliance with liquidity thresholds or constraints
- Portfolio reallocation decisions based on liquidity capacity

**When NOT to Use:**
- When asset classes have only single liquidity classifications (100% in one category)
- When the question asks only about rebalancing bands without liquidity analysis
- When liquidity percentages within an asset class don't sum to 100% (data error)

**Procedure:**
1. **Identify all asset classes** and their portfolio allocation percentages
2. **Extract liquidity classifications** for each asset class across all categories (liquid, semi-liquid, illiquid)
   - **CRITICAL:** Verify that percentages within each asset class sum to 100% (mutually exclusive categories)
3. **Calculate weighted contributions** for each liquidity category separately:
   - Liquid% = Σ(allocation_i × %Liquid_i) across all asset classes
   - Semi-liquid% = Σ(allocation_i × %Semi-liquid_i) across all asset classes
   - Illiquid% = Σ(allocation_i × %Illiquid_i) across all asset classes
   - **DO NOT double-count:** Each asset class portion contributes to exactly ONE category
4. **Verify total:** Liquid% + Semi-liquid% + Illiquid% must equal 100%
5. **Compare results** to liquidity budget requirements or constraints
6. **Determine capacity** for reallocation by calculating distance from thresholds
7. **Make recommendations** based on whether current allocations exceed minimums or fall below maximums

**Common Mistakes to Avoid:**
- **Double-counting liquidity categories:** If an asset class is 50% liquid and 50% semi-liquid, do NOT add 50% to both liquid AND semi-liquid totals separately and then sum them again. Each 50% contributes to its respective category only once.
- **Treating partial classifications as additive:** An asset that is 50% liquid contributes (allocation × 50%) to the liquid category, not the full allocation amount
- **Ignoring the semi-liquid category:** When three categories exist, all three must be calculated separately
- **Failing to verify the 100% sum:** If your calculated liquidity percentages don't sum to 100%, you've made a calculation error

**Example (sanitized):**
> **Scenario:** A foundation has a liquidity budget requiring minimum 25% liquid assets and maximum 35% illiquid assets. Current portfolio: Bonds 20% (100% liquid), Equities 50% (60% liquid, 40% semi-liquid), Private Equity 30% (100% illiquid).
> 
> **Wrong approach:** "Equities are 60% liquid, so I add 50% × 60% = 30% to liquid. Equities are also 40% semi-liquid, so I add another 50% × 40% = 20% to liquid. Total liquid = 20% + 30% + 20% = 70%."
> 
> **Correct approach:** 
> - Liquid = (20% × 100%) + (50% × 60%) + (30% × 0%) = 20% + 30% + 0% = 50%
> - Semi-liquid = (20% × 0%) + (50% × 40%) + (30% × 0%) = 0% + 20% + 0% = 20%
> - Illiquid = (20% × 0%) + (50% × 0%) + (30% × 100%) = 0% + 0% + 30% = 30%
> - Verification: 50% + 20% + 30% = 100% ✓
> - The 50% liquid allocation exceeds the 25% minimum by 25 percentage points, and the 30% illiquid is 5 percentage points below the 35% maximum, providing capacity to shift toward illiquid assets.

---
## Pattern: Life_Insurance_Needs_Analysis_Method

**Description:** The needs analysis method for life insurance calculates required coverage by determining the present value of a surviving spouse's living expenses from current age to life expectancy (not retirement), adding immediate cash needs, and subtracting available capital and the present value of the survivor's future income.

**When to Use:**
- Questions asking to "calculate life insurance needs" or "determine insurance coverage amount"
- Scenarios involving "needs analysis method" or "human life value"
- When given living expenses, income projections, ages, and life expectancy assumptions
- Individual or family insurance planning contexts

**Procedure:**
1. **Calculate PV of survivor's living expenses:**
   - Identify annual living expenses needed by survivor
   - Determine time horizon: years from current age to life expectancy (typically age 85-90), NOT to retirement
   - Use growing annuity formula if expenses grow with inflation: PV = PMT × [(1 - ((1+g)/(1+r))^n) / (r-g)]
   - Where: PMT = annual expense, g = growth rate, r = discount rate, n = years to life expectancy
2. **Add immediate cash needs:**
   - Funeral/final expenses
   - Debt payoff requirements
   - Education funding needs
   - Emergency reserves
3. **Subtract available capital:**
   - Current investment assets
   - Existing life insurance
   - Other liquid assets
4. **Subtract PV of survivor's future income:**
   - Calculate years of income (from current age to retirement)
   - Use appropriate present value formula for income stream
   - Account for income growth if applicable
5. **Sum components:** Insurance Need = PV(Living Expenses) + Cash Needs - Available Capital - PV(Survivor Income)

**Example (sanitized):**
> **Scenario:** Calculate insurance needs for a 40-year-old spouse. Survivor needs $60,000 annually until age 85, growing at 2%. Discount rate 5%. Immediate needs: $50,000. Available capital: $200,000. Survivor's income: $40,000/year for 25 years until retirement (no growth), discounted at 5%.
> 
> **Wrong approach:** "Calculate living expenses PV for 25 years until retirement at age 65."
> 
> **Correct approach:**
> - Years to life expectancy: 85 - 40 = 45 years (not 25 years to retirement)
> - PV(Living Expenses) = $60,000 × [(1 - ((1.02/1.05)^45)) / (0.05-0.02)] = $60,000 × 28.57 = $1,714,200
> - Cash Needs = $50,000
> - Available Capital = $200,000
> - PV(Survivor Income) = $40,000 × [(1 - (1/1.05)^25) / 0.05] = $40,000 × 14.09 = $563,600
> - Insurance Need = $1,714,200 + $50,000 - $200,000 - $563,600 = $1,000,600

---

## Pattern: Liquidity_Management_Framework_For_Illiquid_Allocations

**Description:** When increasing illiquid asset allocations, portfolio managers must implement comprehensive liquidity management frameworks including stress testing protocols, rebalancing mechanisms (calendar-based, percent-range, or automatic adjustments), and ongoing monitoring to prevent risk profile drift during market stress periods.

**When to Use:**
- Questions about "increasing illiquid allocations," "liquidity concerns," or "rebalancing illiquid portfolios"
- Scenarios involving shifts from liquid to illiquid assets
- When stakeholders express concerns about liquidity risk or portfolio drift
- Discussion of liquidity budgeting compliance under stress conditions

**Procedure:**
1. **Assess liquidity profile impact:**
   - Calculate how proposed allocation changes affect liquid, semi-liquid, and illiquid percentages
   - Evaluate under both normal and stress conditions
   - Verify continued compliance with liquidity budget minimums/maximums
2. **Implement stress testing protocols:**
   - Test portfolio liquidity under adverse market scenarios
   - Identify potential liquidity shortfalls during stress periods
   - Establish monitoring frequency (more frequent when near threshold limits)
   - Create contingency plans for liquidity needs
3. **Design rebalancing mechanisms:**
   - **Calendar rebalancing:** Set fixed intervals (quarterly, annually) for rebalancing
   - **Percent-range rebalancing:** Establish tolerance bands (e.g., ±3%) for asset class weights
   - **Automatic rebalancing:** Use liquid public market allocations correlated to illiquid private markets to adjust exposure without trading illiquid assets
   - Document pre-specified rules and thresholds
4. **Address risk profile drift:**
   - Recognize that illiquid assets have high rebalancing costs
   - Ensure sufficient liquid assets remain for rebalancing during stress
   - Establish systematic discipline for maintaining risk targets
   - Monitor relative valuations across asset classes
5. **Ongoing monitoring requirements:**
   - Track actual vs. target allocations continuously
   - Review liquidity classifications periodically (assets may become less liquid in stress)
   - Adjust rebalancing mechanisms as portfolio composition changes
   - Document compliance with liquidity framework

**Example (sanitized):**
> **Scenario:** A pension fund proposes shifting 8% from public equities (liquid) to private real estate (illiquid). Current allocation: 45% liquid, 30% semi-liquid, 25% illiquid. Liquidity budget requires minimum 35% liquid, maximum 35% illiquid. CFO concerned about liquidity risk and portfolio drift.
> 
> **Wrong approach:** "The shift keeps us within limits (37% liquid, 33% illiquid), so no additional actions needed."
> 
> **Correct approach:**
> - **Liquidity impact:** New allocation would be 37% liquid, 30% semi-liquid, 33% illiquid—close to the 35% illiquid maximum, reducing flexibility
> - **Stress testing:** Implement quarterly stress tests to ensure liquidity remains adequate if market conditions deteriorate; increase monitoring frequency given proximity to threshold
> - **Rebalancing mechanism:** Adopt percent-range rebalancing with ±2% tolerance bands; alternatively, use liquid equity futures correlated to private real estate to adjust exposure without selling illiquid holdings
> - **Risk drift prevention:** Establish automatic rebalancing triggers when allocations breach tolerance bands; maintain sufficient liquid assets (target 40% liquid buffer) to enable rebalancing during stress without forced sales of illiquid assets
> - **Documentation:** Create written rebalancing policy with pre-specified rules, review quarterly, and adjust if portfolio approaches liquidity constraints

---

## Pattern: Partial_Liquidity_Classification_Aggregation

**Description:** Asset classes often have split liquidity profiles (e.g., 40% liquid, 30% semi-liquid, 30% illiquid). Proper aggregation requires calculating each category's contribution separately and summing across all asset classes, recognizing that percentages within each asset class must sum to 100% and that each portion contributes to exactly one mutually exclusive liquidity category.

**When to Use:**
- Asset classes with multiple liquidity classifications
- Portfolio-level liquidity reporting
- Verification of liquidity budget compliance
- Scenarios where not all holdings within an asset class have identical liquidity

**When NOT to Use:**
- When all asset classes have 100% classification in a single category
- When calculating other portfolio metrics unrelated to liquidity
- When liquidity data is incomplete or inconsistent

**Procedure:**
1. **Verify classification completeness:** For each asset class, ensure liquidity percentages sum to 100% (Liquid% + Semi-liquid% + Illiquid% = 100%)
2. **Calculate category contributions separately:** For each liquidity category, multiply portfolio allocation by classification percentage
   - **CRITICAL:** Each calculation produces ONE number that goes into ONE category only
   - Example: If Equities are 50% of portfolio and 60% liquid, then (50% × 60%) = 30% contributes ONLY to the liquid category
3. **Aggregate across asset classes:** Sum all contributions within each liquidity category
   - Liquid total = sum of all liquid contributions
   - Semi-liquid total = sum of all semi-liquid contributions  
   - Illiquid total = sum of all illiquid contributions
4. **Validate results:** Total portfolio liquidity percentages should sum to 100%
   - If not 100%, recheck calculations for errors
5. **Interpret capacity:** Compare to requirements to determine reallocation capacity

**Common Mistakes to Avoid:**
- **Treating categories as overlapping:** Liquid, semi-liquid, and illiquid are mutually exclusive—an asset's portion cannot be counted in multiple categories
- **Confusing asset-level and portfolio-level percentages:** A 50% liquid classification within an asset class means only that portion contributes to portfolio liquid percentage
- **Omitting the semi-liquid category:** When three categories exist, calculate all three separately
- **Arithmetic errors in aggregation:** Double-check that each asset class contribution is added to the correct category exactly once

**Example (sanitized):**
> **Scenario:** Portfolio has three asset classes: Cash 5% (100% liquid), Stocks 60% (50% liquid, 30% semi-liquid, 20% illiquid), Hedge Funds 35% (0% liquid, 40% semi-liquid, 60% illiquid).
> 
> **Wrong approach:** "Stocks are 50% liquid, so I count the full 60% allocation as liquid since it has some liquid portion."
> 
> **Correct approach:**
> - Liquid = (5% × 100%) + (60% × 50%) + (35% × 0%) = 5% + 30% + 0% = 35%
>   - Cash contributes 5% to liquid
>   - Stocks contribute 30% to liquid (not 60%)
>   - Hedge Funds contribute 0% to liquid
> - Semi-liquid = (5% × 0%) + (60% × 30%) + (35% × 40%) = 0% + 18% + 14% = 32%
>   - Stocks contribute 18% to semi-liquid
>   - Hedge Funds contribute 14% to semi-liquid
> - Illiquid = (5% × 0%) + (60% × 20%) + (35% × 60%) = 0% + 12% + 21% = 33%
>   - Stocks contribute 12% to illiquid
>   - Hedge Funds contribute 21% to illiquid
> - Verification: 35% + 32% + 33% = 100% ✓
## Pattern: Growing_Annuity_Time_Horizon_Selection

**Description:** When calculating present value of future expenses (especially for life insurance or retirement planning), the time horizon must extend to life expectancy or end of need period, not to an intermediate milestone like retirement age, unless expenses cease at that milestone.

**When to Use:**
- Life insurance needs analysis
- Retirement income planning
- Long-term expense projections
- Any scenario involving living expenses beyond a career endpoint

**Procedure:**
1. **Identify the expense stream:** What costs need to be covered (living expenses, healthcare, etc.)?
2. **Determine when expenses END:** 
   - For survivor living expenses: life expectancy (typically age 85-90)
   - For retirement income: life expectancy from retirement date
   - NOT the retirement age unless expenses stop at retirement
3. **Calculate time horizon:** Years from current age (or start date) to expense end date
4. **Apply growing annuity formula:** PV = PMT × [(1 - ((1+g)/(1+r))^n) / (r-g)]
   - n = years to expense end (not years to retirement)
   - PMT = annual expense amount
   - g = growth rate (inflation)
   - r = discount rate
5. **Verify logic:** Ask "Will this person still need money after retirement?" If yes, use life expectancy

**Example (sanitized):**
> **Scenario:** A 35-year-old needs insurance to cover spouse's $70,000 annual living expenses (growing at 3%) until age 85. Discount rate 6%. Spouse plans to retire at 65.
> 
> **Wrong approach:** "Time horizon is 30 years (age 35 to retirement at 65)."
> 
> **Correct approach:**
> - Expenses continue until death at age 85, not just to retirement at 65
> - Time horizon: 85 - 35 = 50 years
> - PV = $70,000 × [(1 - ((1.03/1.06)^50)) / (0.06-0.03)]
> - PV = $70,000 × [(1 - 0.2281) / 0.03] = $70,000 × 25.73 = $1,801,100
> - Using wrong 30-year horizon would give: $70,000 × 19.60 = $1,372,000 (significantly understated)

---

## Pattern: Liquidity_Stress_Testing_Requirements

**Description:** Liquidity budgets must be tested under both normal and stress conditions. Stress scenarios typically assume reduced liquidity classifications (assets become less liquid), increased withdrawal needs, and correlation of liquidity constraints with market downturns.

**When to Use:**
- Evaluating proposed allocation changes
- Periodic portfolio reviews
- Risk management assessments
- When portfolios approach liquidity threshold limits

**Procedure:**
1. **Define stress scenarios:**
   - Market downturn (e.g., -30% equity decline)
   - Liquidity reclassification (semi-liquid becomes illiquid)
   - Increased withdrawal needs (e.g., 50% higher than normal)
   - Combination scenarios (multiple stresses simultaneously)
2. **Recalculate liquidity profile under stress:**
   - Apply stress assumptions to asset classifications
   - Adjust for potential asset value changes
   - Account for correlation effects (illiquid assets often decline when liquidity needed most)
3. **Test against liquidity budget:**
   - Verify minimum liquid requirements still met
   - Confirm maximum illiquid limits not breached
   - Assess margin of safety
4. **Determine monitoring frequency:**
   - Portfolios near limits: monthly or quarterly testing
   - Portfolios with comfortable margins: annual testing
   - After significant allocation changes: immediate testing
5. **Document results and actions:**
   - Record stress test assumptions and outcomes
   - Identify potential violations or concerns
   - Establish contingency plans if stress scenarios materialize

**Example (sanitized):**
> **Scenario:** Portfolio currently 40% liquid, 25% semi-liquid, 35% illiquid (at maximum illiquid limit). Stress scenario: 50% of semi-liquid assets reclassified as illiquid during market crisis.
> 
> **Wrong approach:** "Current allocation meets requirements, so we're compliant."
> 
> **Correct approach:**
> - **Normal conditions:** 40% liquid, 25% semi-liquid, 35% illiquid ✓
> - **Stress conditions:** 
>   - Liquid: 40% (unchanged)
>   - Semi-liquid: 25% × 50% = 12.5% (half reclassified)
>   - Illiquid: 35% + 12.5% = 47.5% (exceeds 40% maximum limit) ✗
> - **Conclusion:** Portfolio violates liquidity budget under stress; reduce illiquid allocation to 30% in normal conditions to maintain 42.5% maximum under stress (30% + 50% of 25% = 42.5%), providing small buffer
> - **Monitoring:** Implement quarterly stress testing given proximity to limits

---

SKILL_MD_ENTRY: | `alternative_investments/new_patterns.md` | Alternative Investments | Liquidity and Insurance Planning Analysis | Bottom_Up_Liquidity_Classification_Analysis, Life_Insurance_Needs_Analysis_Method, Liquidity_Management_Framework_For_Illiquid_Allocations, Partial_Liquidity_Classification_Aggregation, Growing_Annuity_Time_Horizon_Selection, Liquidity_Stress_Testing_Requirements |