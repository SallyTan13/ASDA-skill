# Alternative Investments — Context and Methodology Gaps

## Pattern 1: missing_context_detection

**Description:** Questions reference specific entities, concerns, analyses, or statements that are not present in the provided context material, making them unanswerable without additional information.

**When to Use:** 
- Question asks to "discuss [Person]'s concerns/views/analysis" but Person is not mentioned in context
- Question references "the analysis" or "the statement" when no such analysis/statement exists in materials
- Question asks about specific recommendations, objections, or positions attributed to named individuals absent from context
- Keywords: "expressed concerns," "his/her analysis," "their recommendation," "as stated by"

**Procedure:**
1. Extract all named entities (people, organizations) referenced in the question
2. Search the provided context for each entity by name
3. If a key entity is mentioned in the question but absent from context, flag as unanswerable
4. Check if the question asks about specific attributes (concerns, views, analysis) of the missing entity
5. If yes, state: "Cannot answer - the question references [Entity]'s [attribute] but [Entity] is not mentioned in the provided materials"
6. Do not attempt to infer or fabricate what the missing entity might have said/done

**Example (sanitized):**
> **Scenario:** A question asks "Evaluate Martinez's objections to the proposed hedge fund allocation" but the context only discusses general hedge fund characteristics without mentioning Martinez.
> 
> **Wrong approach:** Attempting to answer by discussing general objections to hedge funds or assuming what Martinez might object to based on common concerns.
> 
> **Correct approach:** "This question cannot be answered from the provided context. Martinez is referenced in the question but does not appear in the source material. Without knowing Martinez's specific objections, no evaluation can be performed."

---

## Pattern 2: liquidity_budget_analysis

**Description:** Bottom-up liquidity analysis requires multiplying each asset class allocation by its liquidity classification percentages, aggregating across all classes, and comparing results to policy constraints.

**When to Use:**
- Questions about liquidity budget implementation or monitoring
- Analyzing whether a portfolio meets liquidity requirements or limits
- Determining capacity to shift from liquid to illiquid investments
- Keywords: "liquidity budget," "liquidity classification," "liquid requirement," "illiquid limit," "bottom-up analysis"

**Procedure:**
1. Identify all asset classes in the portfolio with their percentage allocations
2. For each asset class, determine the liquidity classification breakdown (% Liquid, % Semi-liquid, % Illiquid)
3. Calculate liquid allocation: Sum of (Asset Class Weight × % Liquid) across all classes
4. Calculate semi-liquid allocation: Sum of (Asset Class Weight × % Semi-liquid) across all classes
5. Calculate illiquid allocation: Sum of (Asset Class Weight × % Illiquid) across all classes
6. Compare calculated allocations to policy requirements:
   - Minimum liquid requirement (typically 20-30%)
   - Maximum illiquid limit (typically 30-40%)
7. Determine capacity: If liquid > minimum and illiquid < maximum, capacity exists to shift toward illiquid
8. Recommend reallocation if capacity exists and illiquid investments offer return premium

**Example (sanitized):**
> **Scenario:** A foundation has: 5% cash (100% liquid), 30% bonds (100% liquid), 45% public equity (60% liquid, 40% semi-liquid), 15% private equity (100% illiquid), 5% real estate (50% semi-liquid, 50% illiquid). Policy requires minimum 25% liquid and maximum 35% illiquid.
> 
> **Wrong approach:** Simply adding up asset class weights that seem liquid (5% + 30% = 35% liquid) without considering partial liquidity classifications.
> 
> **Correct approach:** 
> - Liquid = (5% × 100%) + (30% × 100%) + (45% × 60%) + (15% × 0%) + (5% × 0%) = 62%
> - Illiquid = (5% × 0%) + (30% × 0%) + (45% × 0%) + (15% × 100%) + (5% × 50%) = 17.5%
> - Result: 62% liquid exceeds 25% minimum; 17.5% illiquid is below 35% maximum
> - Conclusion: Significant capacity exists to increase illiquid allocation by up to 17.5 percentage points

---

## Pattern: least_accurate_statement_logic

**Description:** "Least accurate" or "least appropriate" questions require identifying the FALSE or INCORRECT statement among options, not the least important or least relevant true statement. In benchmark bias contexts, "least likely exists" means the bias that is LEAST PROBLEMATIC or LEAST APPLICABLE to the specific investment structure, not the bias that is most commonly discussed.

**When to Use:**
- Question asks "which is least accurate," "least appropriate," "least likely," or "least correct"
- Question asks "which bias least likely exists" or "which issue is least likely"
- Multiple statements are provided as answer choices
- Keywords: "least accurate," "least appropriate," "NOT correct," "EXCEPT," "least likely," "least likely exists"

**When NOT to Use:**
- When the question asks for the "most important" or "most relevant" factor (this requires ranking by significance, not identifying false statements)
- When all options are technically true but differ in degree of applicability (requires contextual judgment, not error detection)

**Procedure:**
1. Recognize that "least accurate" means "most false" or "incorrect," not "least important"
2. For "least likely exists" questions, identify which issue/bias is LEAST APPLICABLE or MOST MITIGATED in the given context
3. Evaluate each statement independently for factual accuracy OR contextual applicability
4. Identify statements that are TRUE/CORRECT (these are accurate, even if minor points)
5. Identify statements that are FALSE/INCORRECT (contain errors, reversals, or misstatements)
6. For benchmark bias questions, identify which bias is LEAST PROBLEMATIC given the specific investment structure:
   - Consider structural mitigations (e.g., fund-of-funds reduces survivorship bias)
   - Consider inherent characteristics (e.g., private equity naturally has infrequent pricing)
   - Distinguish between "commonly discussed" and "actually problematic"
7. The FALSE statement OR the least applicable/most mitigated issue is the answer
8. Common error patterns to check:
   - Directional reversals (overestimation vs. underestimation)
   - Opposite relationships (positive vs. negative correlation)
   - Inverted causality (cause and effect switched)
   - Incorrect limitations stated as benefits, or vice versa
   - Confusing "standard characteristic" with "not a bias/problem"

**Common Mistakes to Avoid:**
- Selecting an option because it's a "standard consideration" or "well-known characteristic" — this doesn't mean it's NOT a bias or NOT problematic
- Confusing "commonly discussed" with "most problematic" — the question asks which is LEAST likely to exist/be problematic
- Ignoring structural mitigations (e.g., diversification through fund-of-funds structure reduces certain biases)
- Treating all biases as equally applicable without considering the specific investment context

**Example (sanitized):**
> **Scenario:** Question asks "Which benchmark bias is least likely to exist for a real estate fund-of-funds investment?"
> - A: Survivorship bias (only successful properties reported)
> - B: Appraisal smoothing (infrequent valuations create lag)
> - C: Selection bias (manager cherry-picks comparable properties)
> 
> **Wrong approach:** Selecting B because appraisal smoothing is a "well-known characteristic" of real estate, even though it's highly problematic for this investment type.
> 
> **Correct approach:** 
> - Statement A: Survivorship bias is MITIGATED by fund-of-funds structure (diversification across multiple managers reduces impact of failed properties)
> - Statement B: Appraisal smoothing is HIGHLY APPLICABLE (real estate valuations are infrequent, creating significant lag and smoothing effects)
> - Statement C: Selection bias is APPLICABLE (individual managers may select favorable comparables)
> - Answer: A is least likely to exist because the fund-of-funds structure specifically mitigates survivorship bias, while the other biases remain highly relevant to real estate investments

---
## Pattern 4: spending_policy_smoothing_mechanisms

**Description:** Endowment spending policies using geometric smoothing rules (e.g., Yale formula) create countercyclical spending patterns that stabilize distributions across market cycles, affecting both spending predictability and risk tolerance for illiquid investments.

**When to Use:**
- Questions about endowment spending policy design and its investment implications
- Analyzing relationship between spending rules and illiquidity tolerance
- Evaluating concerns about allocation shifts toward illiquid assets
- Keywords: "spending policy," "smoothing rule," "geometric smoothing," "Yale formula," "countercyclical," "spending rate stability"

**Procedure:**
1. Identify the spending policy formula structure (typically: weighted average of prior spending adjusted for inflation and percentage of current market value)
2. Recognize smoothing effect: Policy dampens year-to-year spending volatility
3. Understand countercyclical nature:
   - Strong returns → Lower spending rate (spending grows slower than portfolio)
   - Weak returns → Higher spending rate (spending declines slower than portfolio)
4. Connect to illiquidity concerns:
   - Smoothing reduces need for emergency liquidity during market stress
   - Higher spending rates during weak markets may conflict with illiquid asset lockups
   - Predictable spending aids planning but doesn't eliminate liquidity needs
5. Evaluate whether smoothing policy supports or conflicts with proposed allocation changes
6. Consider time horizon: Smoothing works over multi-year periods, not immediate crises

**Example (sanitized):**
> **Scenario:** A university uses spending policy: 70% × (prior year spending × 1.03) + 30% × (5% × current market value). Investment committee proposes increasing private equity from 15% to 25%. A trustee expresses concern about liquidity.
> 
> **Wrong approach:** Dismissing the concern because the endowment has a long time horizon, without analyzing how the spending policy interacts with illiquidity.
> 
> **Correct approach:** "The spending policy incorporates geometric smoothing that creates countercyclical distributions. During market downturns, the policy maintains higher spending rates (30% weight on current value means spending doesn't fall as fast as portfolio). This countercyclical feature is relevant to the liquidity concern because: (1) it reduces but doesn't eliminate the need for liquidity during stress periods, (2) the 70% weight on prior spending provides some stability, but (3) a 25% illiquid allocation combined with potential 5%+ annual spending during weak markets requires careful liquidity buffer management. The smoothing policy supports moderate illiquidity but doesn't make liquidity concerns irrelevant."

---

## Pattern 5: investment_policy_element_interconnections

**Description:** Investment policy elements (return objectives, risk tolerance, liquidity requirements, spending rules) are interconnected, and changes to one element have implications for others that must be explicitly analyzed.

**When to Use:**
- Questions asking about "relevance" of one policy element to concerns about another
- Analyzing how spending policy relates to allocation decisions
- Evaluating whether risk tolerance supports liquidity constraints
- Keywords: "relevance to," "implications for," "relationship between," "how does [X] affect [Y]"

**Procedure:**
1. Identify the two policy elements being connected in the question
2. Map the logical chain between them:
   - How does Element A mechanically affect Element B?
   - What constraints does Element A place on Element B?
   - What flexibility does Element A provide for Element B?
3. Consider both direct and indirect connections:
   - Direct: Spending rate directly determines minimum liquidity needs
   - Indirect: Spending smoothing indirectly affects illiquidity tolerance
4. Evaluate whether the connection supports or conflicts with proposed actions
5. Quantify when possible (e.g., 5% spending + 3% operations = 8% annual liquidity need)
6. State the relevance explicitly: "Element A is relevant to the concern about Element B because [specific mechanism]"

**Example (sanitized):**
> **Scenario:** A foundation's investment policy includes: (1) 7% annual spending rate, (2) target 20% allocation to private equity, (3) minimum 30% liquid assets requirement. Question asks about relevance of spending rate to concerns about increasing private equity to 30%.
> 
> **Wrong approach:** Discussing private equity returns and diversification benefits without connecting to the 7% spending rate.
> 
> **Correct approach:** "The 7% spending rate is directly relevant to concerns about increasing illiquid private equity allocation. The spending rate creates an annual 7% liquidity demand. Combined with potential capital calls from private equity (which could add another 5-10% liquidity need in commitment-heavy years), the total liquidity requirement could reach 12-17% annually. The current 30% liquid asset minimum provides a buffer, but increasing private equity from 20% to 30% would reduce this buffer. The high spending rate makes the portfolio more sensitive to illiquidity risk because there's less flexibility to defer distributions during capital call periods. The relevance is that spending policy and illiquidity tolerance must be jointly managed—a 7% spending rate constrains how much illiquidity the portfolio can prudently accept."

---

SKILL_MD_ENTRY: | `alternative_investments/context_and_methodology_gaps.md` | Alternative Investments | Context and Methodology Gaps | missing_context_detection, liquidity_budget_analysis, least_accurate_statement_logic, spending_policy_smoothing_mechanisms, investment_policy_element_interconnections |

## Pattern: benchmark_bias_applicability

**Description:** Benchmark bias questions asking "which bias least likely exists" require evaluating which measurement or reporting bias is LEAST PROBLEMATIC for the specific investment structure, not which bias is least commonly discussed or least theoretically relevant.

**When to Use:**
- Questions about benchmark biases in alternative investments
- Questions asking "which bias least likely exists" or "which bias is least applicable"
- Context involves specific investment structures (fund-of-funds, direct investment, etc.)
- Keywords: "benchmark bias," "least likely exists," "measurement bias," "reporting bias"

**Procedure:**
1. Identify all potential biases listed in the answer choices
2. Understand what each bias means:
   - Survivorship bias: Only successful investments/funds are included in performance data
   - Infrequent pricing/transactions: Illiquid assets valued infrequently, creating stale prices
   - Vintage year effect: Performance varies by investment year due to market conditions
   - Backfill bias: Historical data added retroactively, often only for successful funds
3. Analyze the specific investment structure in the context:
   - Fund-of-funds: Diversification reduces survivorship bias impact
   - Direct investment: Full exposure to all biases
   - Secondary market: May reduce vintage year effects
4. Determine which bias is MOST MITIGATED by the structure:
   - Structural mitigations (diversification, professional management)
   - Natural characteristics that reduce bias impact
5. Determine which biases are INHERENT and UNAVOIDABLE:
   - Private equity: Always has infrequent pricing (illiquid by nature)
   - Alternative investments: Often have survivorship bias in reported data
6. Select the bias that is LEAST PROBLEMATIC (most mitigated) as the answer
7. Do NOT confuse "standard characteristic" with "not a bias" — if something is inherent to the asset class, it's MORE likely to exist, not less

**Common Mistakes to Avoid:**
- Selecting a bias because it's a "standard consideration" — this means it DOES exist and is problematic
- Ignoring structural mitigations that reduce specific biases
- Treating all biases as equally applicable without analyzing the investment structure
- Confusing theoretical relevance with practical applicability

**Example (sanitized):**
> **Scenario:** A family office is investing in a private equity fund-of-funds. Question asks: "Which benchmark bias least likely exists?"
> - A: Survivorship bias
> - B: Infrequent market transactions
> - C: Backfill bias
> 
> **Wrong approach:** Selecting B because infrequent transactions are a "well-known feature" of private equity, reasoning that it's not really a "bias" but just a characteristic.
> 
> **Correct approach:**
> - Survivorship bias: MITIGATED by fund-of-funds structure — diversification across 20+ underlying funds means the impact of any single failed investment is reduced; professional fund managers track all investments, not just survivors
> - Infrequent transactions: HIGHLY APPLICABLE — private equity is inherently illiquid with quarterly or less frequent valuations, creating significant stale pricing issues
> - Backfill bias: APPLICABLE — performance databases often add historical data only for successful funds
> - Answer: A (survivorship bias) is least likely to be problematic because the fund-of-funds structure specifically mitigates this bias through diversification and professional oversight, while the other biases remain inherent to private equity investments