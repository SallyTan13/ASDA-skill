# Equity — Portfolio Management Concept Confusion

## Pattern: performance_attribution_vs_evaluation

**Description:** Performance attribution is a descriptive decomposition tool that breaks down returns into component sources (allocation, selection, interaction effects), while performance evaluation draws conclusions about manager skill or quality. Attribution shows WHERE returns came from; evaluation determines WHETHER decisions were good.

**When to Use:** Questions involving performance attribution analysis, manager evaluation, distinguishing between descriptive analysis and qualitative judgment, or statements claiming attribution "evaluates quality" or "draws conclusions about skill."

**Procedure:**
1. Identify whether the statement describes attribution (decomposition) or evaluation (judgment)
2. Recognize that attribution decomposes returns into: allocation effects, selection effects, interaction effects, currency effects, etc.
3. Understand that attribution is value-neutral—it shows sources without judging quality
4. Evaluation requires additional context: benchmarks, risk-adjusted metrics, consistency, process quality
5. Reject statements claiming attribution inherently evaluates skill or draws quality conclusions
6. Accept that attribution provides inputs FOR evaluation but is not evaluation itself

**Example (sanitized):**
> **Scenario:** An analyst states: "Performance attribution analysis determines whether a portfolio manager has superior stock-picking ability."
> **Wrong approach:** Accepting this as correct because attribution shows selection effects
> **Correct approach:** Recognizing this confuses attribution (showing selection contributed X%) with evaluation (determining if X% represents skill vs. luck). Attribution reveals the selection effect magnitude but doesn't conclude whether it demonstrates ability.

---

## Pattern: type_i_vs_type_ii_errors_in_governance

**Description:** In manager selection and monitoring contexts, Type I errors involve rejecting good managers (false positive for poor quality), while Type II errors involve retaining poor managers (false negative for poor quality). Governance systems are designed to minimize specific error types based on organizational priorities and consequences.

**When to Use:** Questions about manager hiring/firing policies, due diligence databases, monitoring systems, or governance frameworks that track rejected candidates or terminated managers.

**Procedure:**
1. Define the decision context: hiring (accept/reject candidate) or monitoring (retain/fire manager)
2. Identify Type I error: rejecting a good manager or not hiring a qualified candidate
3. Identify Type II error: retaining a poor manager or hiring an unqualified candidate
4. Determine which error the policy/system is designed to minimize
5. Recognize that tracking rejected candidates helps avoid Type II errors (by improving future screening to catch poor candidates)
6. Recognize that tracking fired managers helps avoid Type II errors (by improving monitoring to catch poor performers earlier)
7. Understand that both databases serve the same error-minimization purpose from a policy design perspective

**Example (sanitized):**
> **Scenario:** A pension fund maintains a database of all external managers who were terminated for underperformance. The purpose is to minimize which type of error?
> **Wrong approach:** Concluding it minimizes Type I errors because it tracks rejected (fired) managers
> **Correct approach:** Recognizing the database helps improve future monitoring processes to catch underperformers sooner, thereby minimizing Type II errors (retaining poor managers too long). The tracking of past mistakes informs better future detection.

---

## Pattern: hedge_ratio_estimation_risk

**Description:** Minimum variance hedge ratios depend on correlation estimates between assets, introducing estimation risk when correlations are uncertain or unstable. Direct 1:1 hedges avoid this estimation risk but may not minimize variance. The choice involves trading off variance minimization against estimation risk.

**When to Use:** Questions comparing hedging strategies, minimum variance hedges, direct hedges, currency hedging decisions, or statements about hedge ratio risk and correlation dependence.

**Procedure:**
1. Identify the hedging approach: minimum variance (correlation-based) vs. direct (1:1)
2. Recognize minimum variance hedges require estimating correlations/betas
3. Understand that correlation estimates introduce estimation risk—actual correlations may differ
4. Recognize direct hedges (1:1 ratio) avoid estimation risk but may not minimize variance
5. Evaluate whether estimation risk outweighs variance reduction benefits
6. Consider that unstable or uncertain correlations increase estimation risk
7. Conclude that direct hedges can be less risky when correlation estimates are unreliable

**Example (sanitized):**
> **Scenario:** An investor can hedge foreign currency exposure using either a minimum variance hedge ratio (based on historical correlation between asset returns and currency movements) or a direct 1:1 hedge. Which approach has less estimation risk?
> **Wrong approach:** Selecting minimum variance hedge because it's "optimal" for reducing variance
> **Correct approach:** Recognizing the direct 1:1 hedge has less estimation risk because it doesn't depend on correlation estimates that may be incorrect. While minimum variance may reduce variance more IF correlations are stable, it introduces risk that the correlation estimate is wrong.

---

## Pattern: investment_vehicle_selection_by_client_type

**Description:** The optimal investment vehicle (ETF, mutual fund, pooled account, separate account) depends on client type (retail vs. institutional), investment size, customization needs, and cost structure. Large institutional investors often benefit from pooled or separate accounts despite ETF cost advantages for smaller investors.

**When to Use:** Questions about choosing between ETFs, mutual funds, pooled accounts, or separate accounts for different client types or investment sizes, or comparing all-in costs across vehicle structures.

**Procedure:**
1. Identify client type: retail (individual) vs. institutional (pension, endowment, foundation)
2. Assess investment size: small (<$10M), medium ($10-100M), large (>$100M)
3. Evaluate customization needs: standard exposure vs. specific constraints/preferences
4. Compare all-in costs including: management fees, trading costs, administrative costs, tax efficiency
5. For retail/small investors: ETFs typically offer low costs and liquidity; mutual funds offer diversification
6. For large institutional investors: pooled accounts or separate accounts often have lower all-in costs due to economies of scale and negotiated fees
7. Consider that ETF advantages (low expense ratios, liquidity) may be offset by trading costs and lack of customization for large institutions
8. Select vehicle based on total cost and customization fit, not just expense ratios

**Example (sanitized):**
> **Scenario:** A $300 million corporate pension fund needs broad equity market exposure. Should it use ETFs or a pooled account?
> **Wrong approach:** Selecting ETFs because they have lower expense ratios than actively managed funds
> **Correct approach:** Recognizing that for a $300M institutional investor, a pooled account likely offers lower all-in costs through negotiated fees, economies of scale, and reduced trading costs, plus potential for customization. ETF advantages apply more to smaller investors where scale economies aren't available.

---

## Pattern: active_risk_from_sector_rebalancing

**Description:** Active risk (tracking error) depends on both position sizes and correlation structure. Rebalancing from within-sector positions to cross-sector positions typically increases active risk because cross-sector positions have lower correlations, even if position magnitudes are similar.

**When to Use:** Questions about active risk changes from portfolio rebalancing, sector rotation trades, or comparing within-sector vs. cross-sector active positions.

**Procedure:**
1. Identify the rebalancing: what positions are closed and what positions are opened
2. Determine if closed positions were within-sector (same sector) or cross-sector (different sectors)
3. Determine if new positions are within-sector or cross-sector
4. Recognize that within-sector positions (e.g., two auto stocks) have higher correlations
5. Recognize that cross-sector positions (e.g., energy vs. financials) have lower correlations
6. Understand that lower correlations between active positions increase active risk (less offsetting)
7. Even if position magnitudes are equal, moving from within-sector to cross-sector increases active risk
8. Calculate or reason about correlation impact: lower correlation → less diversification of active bets → higher tracking error

**Example (sanitized):**
> **Scenario:** A portfolio closes two overweight positions in technology stocks (+2% each) and opens two new overweight positions (+2% each) in healthcare and utilities. How does active risk change?
> **Wrong approach:** Concluding active risk is unchanged because total overweight magnitude is the same (4%)
> **Correct approach:** Recognizing that the two technology stocks were highly correlated (within-sector), while healthcare and utilities have lower correlation (cross-sector). The lower correlation between new positions means less offsetting, increasing active risk despite equal position sizes.

---

## Pattern: statistical_error_framework_in_decisions

**Description:** Decision-making frameworks involve Type I errors (false positives—rejecting true null hypothesis) and Type II errors (false negatives—accepting false null hypothesis). In investment contexts, the null hypothesis and error consequences must be clearly defined to classify errors correctly.

**When to Use:** Questions about hypothesis testing in investment decisions, manager selection errors, risk management false alarms, or any decision framework with accept/reject outcomes.

**Procedure:**
1. Define the null hypothesis clearly (e.g., "manager is qualified" or "manager is unqualified")
2. Identify Type I error: rejecting a true null hypothesis
3. Identify Type II error: failing to reject a false null hypothesis
4. Map to investment context: what are consequences of each error type?
5. Determine which error the policy/system prioritizes minimizing
6. Recognize that error classification depends on how the null hypothesis is framed
7. For manager selection: if H0 = "candidate is qualified," Type I = rejecting good candidate, Type II = hiring bad candidate
8. For manager monitoring: if H0 = "manager is performing adequately," Type I = firing good manager, Type II = retaining poor manager

**Example (sanitized):**
> **Scenario:** An investment committee uses a strict screening process that rejects many manager candidates to ensure only high-quality managers are hired. This approach primarily seeks to minimize which error type?
> **Wrong approach:** Concluding Type I errors are minimized because many candidates are rejected
> **Correct approach:** Defining H0 = "candidate is qualified." Strict screening increases Type I errors (rejecting qualified candidates) but minimizes Type II errors (hiring unqualified candidates). The committee prioritizes avoiding bad hires (Type II) at the cost of potentially rejecting some good candidates (Type I).

---

## Pattern: descriptive_vs_normative_analysis

**Description:** Descriptive analysis explains what happened or describes current state without making judgments, while normative analysis evaluates what should happen or whether outcomes are good/bad. Many analytical tools are purely descriptive but are often confused with normative evaluation.

**When to Use:** Questions distinguishing between explanation and evaluation, analysis and judgment, or tools that describe versus tools that prescribe.

**Procedure:**
1. Identify whether the tool/analysis describes facts or makes value judgments
2. Descriptive: explains sources, breaks down components, shows relationships, measures outcomes
3. Normative: evaluates quality, recommends actions, judges performance, assesses appropriateness
4. Recognize that descriptive tools provide inputs for normative decisions but don't make them
5. Performance attribution, factor decomposition, variance analysis = descriptive
6. Performance evaluation, manager ratings, investment recommendations = normative
7. Reject statements claiming descriptive tools inherently make normative judgments
8. Accept that normative conclusions require additional context beyond descriptive analysis

**Example (sanitized):**
> **Scenario:** A risk decomposition analysis shows that 60% of portfolio variance comes from equity exposure and 40% from credit exposure. Does this analysis evaluate whether the risk allocation is appropriate?
> **Wrong approach:** Yes, because it shows the risk sources and their magnitudes
> **Correct approach:** No, this is purely descriptive—it shows WHERE risk comes from but doesn't evaluate WHETHER this allocation is appropriate for the investor's objectives. Evaluation requires comparing to risk tolerance, return objectives, and constraints.

---

## Pattern: correlation_structure_and_diversification

**Description:** Diversification benefits depend on correlation structure, not just number of positions. Low correlations between positions provide diversification; high correlations reduce diversification even with many positions. Changes in correlation structure affect portfolio risk more than changes in position count.

**When to Use:** Questions about diversification effects, correlation impact on risk, comparing portfolios with different correlation structures, or risk changes from rebalancing.

**Procedure:**
1. Identify the correlation structure: within-group (high correlation) vs. across-group (low correlation)
2. Recognize that diversification benefit = f(correlation), not just f(number of holdings)
3. High correlation positions (e.g., same sector) provide limited diversification
4. Low correlation positions (e.g., different sectors/asset classes) provide greater diversification
5. When rebalancing, assess correlation change: increasing correlation → less diversification → higher risk
6. Decreasing correlation → more diversification → lower risk (all else equal)
7. For active risk: lower correlation between active bets → less offsetting → higher tracking error
8. Consider that equal-weighted positions with different correlations have different risk contributions

**Example (sanitized):**
> **Scenario:** Portfolio A holds 10 stocks all in the financial sector. Portfolio B holds 10 stocks across 10 different sectors. Both are equal-weighted. Which has better diversification?
> **Wrong approach:** They have equal diversification because both hold 10 stocks
> **Correct approach:** Portfolio B has better diversification because cross-sector holdings have lower correlations than within-sector holdings. The correlation structure, not position count, determines diversification benefit.

---

SKILL_MD_ENTRY: | `equity/portfolio_management_concepts.md` | Equity | Concept Confusion | Performance attribution vs. evaluation, Type I/II errors in governance, Hedge ratio estimation risk, Investment vehicle selection, Active risk from sector rebalancing, Statistical error frameworks, Descriptive vs. normative analysis, Correlation and diversification |