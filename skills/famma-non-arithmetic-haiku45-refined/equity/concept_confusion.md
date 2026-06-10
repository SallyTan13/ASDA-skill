# Skill Patterns for Equity Concept Confusion Failures

## Pattern: Hypothesis Testing Framework in Manager Selection

**Description:** Confusion about how Type I and Type II errors map to manager hiring/firing decisions stems from misidentifying the null hypothesis. In manager selection, the null hypothesis is typically "manager has skill/should be retained," making Type I error = rejecting a good manager (false rejection) and Type II error = retaining a bad manager (false acceptance).

**When to Use:** Questions involving manager selection policies, performance evaluation frameworks, Type I/II error terminology, or cost-benefit analysis of hiring/firing decisions.

**Procedure:**
1. Identify the null hypothesis in the decision context (typically H₀: manager is good/has skill)
2. Define Type I error as rejecting H₀ when true (firing/not hiring a good manager)
3. Define Type II error as failing to reject H₀ when false (hiring/retaining a bad manager)
4. Map tracking systems to error types: tracking rejected candidates identifies potential Type I errors; tracking removed managers identifies potential Type II errors
5. Note that minimizing one error type typically increases the other (tradeoff relationship)
6. Verify by checking which error the policy statement explicitly aims to reduce

**Example (sanitized):**
> **Scenario:** A pension fund maintains a database of (A) managers who passed screening but weren't hired, and (B) managers who were terminated for poor performance. The fund states it prioritizes avoiding retention of underperforming managers.
> **Wrong approach:** Database A tracks Type I errors (rejected good managers), Database B tracks Type II errors (kept bad managers).
> **Correct approach:** Null hypothesis = "manager has skill." Type I = rejecting skilled manager. Type II = accepting unskilled manager. Database A helps identify Type I errors (we can see if rejected managers performed well). Database B helps identify Type II errors (we hired them, then had to fire them). The fund's priority to avoid retaining poor managers means minimizing Type II errors, so both databases serve this goal by learning from past mistakes.

---

## Pattern: Top-Down vs Bottom-Up Investment Strategy Classification

**Description:** Confusion between top-down (macro-to-micro: asset class → sector → country → security) and bottom-up (security-specific analysis regardless of macro factors) approaches. Top-down strategies use sector rotation and geographic allocation; bottom-up strategies use stock-specific valuation metrics like GARP.

**When to Use:** Questions asking which investment methods align with stated portfolio strategies, or requiring classification of fundamental analysis approaches as top-down or bottom-up.

**Procedure:**
1. Identify the stated investment approach (top-down or bottom-up)
2. Classify each method: top-down methods include country/geographic allocation, sector/industry rotation, asset class timing; bottom-up methods include GARP, stock-specific DCF, individual company fundamental analysis
3. Top-down proceeds hierarchically: macro environment → sectors/countries → industries → securities
4. Bottom-up focuses on individual security characteristics independent of macro/sector views
5. Match methods to the stated approach and eliminate mismatches
6. Verify by checking if the method requires macro-level allocation decisions (top-down) or company-specific analysis (bottom-up)

**Example (sanitized):**
> **Scenario:** A fund uses a top-down strategy based on economic analysis. Which is NOT used: (A) sector rotation, (B) value investing based on P/B ratios, (C) country allocation?
> **Wrong approach:** Top-down means fundamental analysis, so value investing (B) fits; country allocation is macro-level, so doesn't fit.
> **Correct approach:** Top-down = macro-to-micro hierarchy. (A) Sector rotation fits (macro sector view). (C) Country allocation fits (macro geographic view). (B) Value investing via P/B is bottom-up stock selection based on individual security characteristics. Answer: B.

---

## Pattern: Investment Style Classification via Valuation Metrics

**Description:** Investment style (value/growth/market-oriented) is defined by systematic preference for specific valuation characteristics, not by the general practice of seeking undervalued securities. Value style requires low valuation multiples (P/E, P/B); growth style requires high growth rates; market-oriented style shows no systematic valuation bias and evaluates securities across the entire spectrum. Style consistency is demonstrated through portfolio beta exposures across value and growth indices, where higher betas on value indices with lower betas on growth indices indicate value style adherence.

**When to Use:** Questions asking to classify manager style as value/growth/market-oriented based on portfolio construction methodology or security selection criteria, OR questions asking which manager adheres to stated style based on portfolio characteristics and index betas.

**When NOT to Use:**
- When the question asks about information ratios or efficiency metrics (these measure skill/efficiency, not style consistency)
- When comparing multiple criteria including both style adherence AND performance efficiency (must evaluate both dimensions separately)
- **When the policy explicitly requires BOTH efficiency (information ratio) AND style consistency as joint criteria for manager selection (must evaluate both and select the manager that best balances both requirements)**

**Procedure:**
1. Identify the manager's security selection criteria and any explicit valuation metric preferences
2. Value style indicators: systematically favors low P/E, low P/B, high dividend yield
3. Growth style indicators: systematically favors high earnings growth, high revenue growth, regardless of current valuation
4. Market-oriented indicators: no systematic valuation bias, evaluates across value and growth spectrum, focuses on intrinsic value regardless of multiples
5. Key distinction: buying below intrinsic value is universal rational investing; style is determined by which types of stocks (value vs growth characteristics) are systematically preferred
6. If manager explicitly ignores traditional valuation ratios or shows no systematic preference, classify as market-oriented
7. **For style consistency verification:** Examine portfolio betas across value and growth indices. Value managers should show higher betas on value indices (0.95-1.1) and lower betas on growth indices (0.3-0.5). Growth managers should show the opposite pattern. Inconsistent beta patterns indicate style drift.
8. **When evaluating manager selection with multiple criteria:** If policy requires BOTH style consistency AND efficiency (information ratio), evaluate both criteria separately:
   - Calculate or compare information ratios to assess efficiency
   - Analyze beta patterns to assess style consistency
   - **Select the manager that demonstrates BOTH adequate efficiency AND strong style consistency, prioritizing the criterion most emphasized in the policy statement**
   - **If one manager has superior efficiency but poor style consistency, while another has moderate efficiency but excellent style consistency, favor the manager with better style consistency when the policy explicitly requires consistent adherence to stated style**

**Common Mistakes to Avoid:**
- Focusing exclusively on style consistency while ignoring explicit efficiency requirements in the policy
- **Selecting the manager with highest information ratio when they exhibit clear style drift or inconsistency with stated style**
- Assuming high information ratio alone determines manager selection when style adherence is also required
- Failing to recognize that a manager with excellent efficiency but poor style consistency may not meet policy requirements
- Ignoring that policy statements often require multiple criteria to be satisfied simultaneously
- **Prioritizing efficiency over style consistency when the policy explicitly states managers must "consistently adhere to stated style"**

**Example (sanitized):**
> **Scenario:** A policy requires managers to (1) demonstrate efficiency in delivering active return relative to tracking error, and (2) consistently adhere to stated style. Three managers: Manager X (IR 0.30, value style stated, betas: small-cap value 0.98, small-cap growth 0.35, large-cap value 1.08, large-cap growth 0.40). Manager Y (IR 0.55, value style stated, betas: small-cap value 1.02, small-cap growth 0.45, large-cap value 1.12, large-cap growth 0.42). Manager Z (IR 0.80, growth style stated, betas: small-cap value 1.05, small-cap growth 0.50, large-cap value 0.95, large-cap growth 0.38).
> **Wrong approach:** Manager Z has the highest information ratio (0.80), so select Z for superior efficiency despite stated growth style.
> **Correct approach:** (1) Evaluate efficiency: Manager Z has highest IR (0.80), Manager Y has moderate IR (0.55), Manager X has lowest IR (0.30). (2) Evaluate style consistency: Manager X shows clear value style (high value betas 0.98-1.08, low growth betas 0.35-0.40) consistent with stated style. Manager Y shows clear value style (high value betas 1.02-1.12, low growth betas 0.42-0.45) consistent with stated style. Manager Z states growth style but shows betas inconsistent with growth orientation (growth betas 0.38-0.50 are low, value betas 0.95-1.05 are comparable or higher), indicating style drift. (3) The policy explicitly requires "consistently adhere to stated style," making style consistency a critical requirement. (4) Manager Y demonstrates BOTH adequate efficiency (IR 0.55, second highest) AND excellent style consistency (clear value beta pattern matching stated style). (5) While Manager Z has superior efficiency, the style drift violates the explicit policy requirement. Answer: Manager Y best meets both policy criteria.

---
## Pattern: Index Construction Methods and Factor Model Assumptions

**Description:** Index replication method selection depends on index size, factor structure, and cost constraints. Full replication holds all securities (practical for small indices); stratified sampling groups by uncorrelated factors and samples within strata (optimal when factors are independent); optimization minimizes tracking error (used when factors are correlated or constraints exist).

**When to Use:** Questions about selecting index construction/replication techniques, especially when factor model assumptions (correlated vs uncorrelated factors) are mentioned.

**Procedure:**
1. Identify index characteristics: number of securities, factor structure assumptions, cost/liquidity constraints
2. Full replication: practical when index has <100-200 securities, provides exact tracking
3. Stratified sampling: optimal when (a) index is large (>500 securities), (b) factors are uncorrelated/independent, (c) cost efficiency is important; groups securities by independent factors and samples within each group
4. Optimization: used when factors are correlated, constraints exist, or tracking error minimization with fewer holdings is needed
5. Match the stated factor assumption: "uncorrelated factors" → stratified sampling; "correlated factors" → optimization
6. Verify by checking if the method aligns with both the index size and the factor independence assumption

**Example (sanitized):**
> **Scenario:** A fund will replicate a 1500-stock index. The construction technique assumes factors explaining returns are uncorrelated. Choose: (A) full replication, (B) stratified sampling, (C) optimization.
> **Wrong approach:** Passive replication always uses full replication for accuracy.
> **Correct approach:** 1500 stocks makes full replication costly. Uncorrelated factors assumption indicates stratified sampling is optimal: group stocks by independent factors (size, sector, etc.), sample within each stratum. This maintains factor exposures while reducing holdings and costs. Answer: B (stratified sampling).

---

## Pattern: Performance Attribution as Descriptive vs Evaluative Tool

**Description:** Performance attribution mechanically decomposes returns into components (allocation effect, selection effect, interaction effect) but does not inherently draw conclusions about manager quality. Conclusions about skill require human interpretation of attribution results in context with other information.

**When to Use:** Questions about the purpose or characteristics of performance attribution analysis, or what attribution does vs does not accomplish.

**Procedure:**
1. Distinguish between what attribution does (descriptive decomposition) and what it does not do (evaluative judgment)
2. Attribution mechanically breaks returns into: allocation effects (sector/asset class weights), selection effects (security choices within categories), interaction effects
3. Attribution shows HOW performance was achieved (which decisions contributed to returns)
4. Attribution does NOT automatically conclude whether decisions were skillful, lucky, or appropriate for the mandate
5. Quality/skill assessment requires interpreting attribution results with additional context: consistency over time, risk-adjusted metrics, alignment with stated strategy
6. Verify statements: "explains how performance was achieved" = correct; "draws conclusions about quality" = incorrect (requires additional interpretation)

**Example (sanitized):**
> **Scenario:** Evaluate two statements: (1) Attribution draws conclusions about manager decision quality, (2) Attribution explains performance by decomposing returns into components.
> **Wrong approach:** Both are correct because attribution analyzes decisions and their outcomes.
> **Correct approach:** Attribution mechanically decomposes returns (allocation + selection + interaction effects), showing which decisions contributed how much. This explains HOW performance occurred (statement 2 = correct). However, attribution itself doesn't conclude if decisions were good/bad—that requires interpreting results with additional context like consistency, risk, and mandate alignment (statement 1 = incorrect). Answer: Only statement 2 is correct.

---

## Pattern: Hedge Ratio Risk: Minimum Variance vs One-to-One

**Description:** Minimum variance hedge ratios minimize ex-post portfolio variance but introduce estimation risk and model risk because they depend on estimated correlations between asset and currency returns. One-to-one hedges avoid estimation risk but may over/under-hedge. Each approach has different risk profiles.

**When to Use:** Questions comparing hedge ratio approaches, discussing hedge effectiveness, or evaluating statements about hedging risks and parameter dependencies.

**Procedure:**
1. Identify the two hedge approaches: minimum variance (optimized based on correlation estimates) vs one-to-one (simple direct hedge)
2. Minimum variance hedge: minimizes variance IF parameters are known correctly, but introduces estimation risk (correlation must be estimated), model risk (assumes stable relationships), and parameter uncertainty
3. One-to-one hedge: no parameter estimation needed, avoids estimation risk, but may not minimize variance (could over-hedge or under-hedge depending on true correlation)
4. Risk comparison: minimum variance has lower ex-post variance under perfect information but higher overall risk due to estimation error; one-to-one has potentially higher variance but no estimation risk
5. Recognize that "minimum variance" refers to the objective function, not the total risk including estimation uncertainty
6. Verify: statements claiming minimum variance is "riskier due to correlation dependence" can be correct when accounting for estimation risk

**Example (sanitized):**
> **Scenario:** Compare statements: (1) Minimum variance hedge is riskier than one-to-one because it depends on correlation estimates, (2) Buying currency options provides downside protection with upside potential but costs more than forwards.
> **Wrong approach:** Minimum variance minimizes risk by definition, so (1) is wrong; (2) is correct.
> **Correct approach:** Minimum variance minimizes variance only if correlation is known perfectly. In practice, correlation must be estimated, introducing estimation risk and parameter uncertainty. This additional risk can make minimum variance riskier overall than one-to-one hedge which requires no estimation. Statement (1) = correct. Statement (2) correctly describes option payoff (asymmetric protection) and cost (premium vs zero-cost forward) = correct. Both statements are correct.

---

## Pattern: Investment Vehicle Selection by Investor Type and Scale

**Description:** Optimal investment vehicle (ETF, mutual fund, pooled/separate account) depends on investor type, investment scale, and cost structure. Large institutional investors (>$50-100M) typically benefit from pooled/separate accounts due to lower all-in costs, customization, and tax efficiency, despite ETFs having lower expense ratios for smaller investors.

**When to Use:** Questions asking to select investment structure for specific client types, especially when investor size, cost sensitivity, and institutional vs retail classification are mentioned.

**Procedure:**
1. Identify investor characteristics: type (institutional vs retail), investment size, cost sensitivity, customization needs
2. ETFs: optimal for retail and smaller institutional investors (<$50M), offer low expense ratios, liquidity, tax efficiency via in-kind redemptions
3. Mutual funds: higher expense ratios than ETFs, suitable for retail investors needing active management or specific strategies
4. Pooled/separate accounts: optimal for large institutional investors (>$50-100M), offer lowest all-in costs at scale (no ETF creation/redemption costs, no bid-ask spreads), direct ownership, greater customization, tax optimization
5. Cost analysis at scale: for large amounts, separate account fees < (ETF expense ratio + trading costs + bid-ask spreads)
6. Verify by matching vehicle to investor size threshold and total cost structure, not just expense ratios

**Example (sanitized):**
> **Scenario:** Four institutional clients will invest $200M total in an index fund. They are very cost-sensitive. Choose: (A) ETF, (B) mutual fund, (C) pooled account.
> **Wrong approach:** Cost-sensitive investors prefer ETFs due to lowest expense ratios.
> **Correct approach:** $200M is large institutional scale. At this size, pooled/separate accounts offer lower total costs: (1) no ETF bid-ask spreads, (2) no creation/redemption costs, (3) direct ownership reduces intermediary fees, (4) customization reduces tracking error costs. Despite higher stated management fees, all-in costs are lower than ETF structure for this scale. Answer: C (pooled account).

---

## Pattern: Active Risk Changes from Paired Trades

**Description:** Active risk depends on both the magnitude of active positions AND the correlation structure between those positions. Eliminating a within-sector pair (high correlation, positions offset significantly) and creating a cross-sector pair (low correlation, positions offset less) increases net active risk even if position magnitudes are equal.

**When to Use:** Questions about how specific trades affect portfolio active risk/tracking error, especially involving paired long-short positions or sector rotations.

**Procedure:**
1. Identify the trades: what positions were eliminated and what positions were created
2. For eliminated positions: assess correlation structure (same sector = high correlation, positions partially offset risk)
3. For new positions: assess correlation structure (different sectors = lower correlation, positions offset less risk)
4. Active risk formula: depends on active weights AND correlation between positions: σ²(active) = Σw²σ² + ΣΣwᵢwⱼρᵢⱼσᵢσⱼ
5. High correlation pairs: long and short positions offset more (lower net risk); low correlation pairs: positions offset less (higher net risk)
6. Compare net effect: replacing high-correlation pair with low-correlation pair of equal magnitude increases active risk
7. Verify by checking if diversification of active bets across uncorrelated factors increases rather than decreases active risk

**Example (sanitized):**
> **Scenario:** A fund eliminates a +2%/-2% pair in two technology stocks and creates a +2%/-2% pair with one energy stock and one financial stock. Effect on active risk?
> **Wrong approach:** Equal offsetting positions maintain zero net exposure, so active risk unchanged.
> **Correct approach:** Original pair: both tech stocks, high correlation (~0.7), positions partially offset, net risk moderate. New pair: energy vs financial, lower correlation (~0.3), positions offset less, net risk higher. Even though magnitudes are equal and net exposure is zero in both cases, the lower correlation in the new pair means less risk cancellation. Active risk increases. Answer: increased.

---

## Pattern: Core-Satellite Strategy Benchmark Alignment

**Description:** Core-satellite strategies combine a passive core (tracking the investor's benchmark) with active satellite positions (which may track different benchmarks to capture specific opportunities). Satellites are not required to share the investor's benchmark; the defining feature is passive core + active satellites, where satellites aim for alpha generation.

**When to Use:** Questions evaluating whether a portfolio structure qualifies as core-satellite, especially when multiple benchmarks are mentioned or satellite funds track different indices than the investor's stated benchmark.

**Procedure:**
1. Identify the investor's personal benchmark (the reference for overall performance evaluation)
2. Identify each portfolio component's characteristics: expected alpha, tracking risk, benchmark
3. Core component: low/zero expected alpha, low/zero tracking risk relative to its benchmark, provides broad market exposure (may be aligned with investor's benchmark or a highly correlated proxy)
4. Satellite components: positive expected alpha, higher tracking risk, actively managed (may track different benchmarks to capture specific opportunities)
5. Core-satellite is valid if: (a) one component is passive/low-risk core, (b) other components are active satellites seeking alpha, (c) combined portfolio addresses investor's objectives
6. Benchmark mismatch between satellites and investor's benchmark does NOT invalidate core-satellite structure if the core provides appropriate market exposure
7. Verify by checking for presence of passive core + active satellites, not benchmark uniformity

**Example (sanitized):**
> **Scenario:** An investor's benchmark is Index A. They invest in three funds benchmarked to Index B (highly correlated with A): Fund 1 (5% alpha, 8% tracking risk), Fund 2 (2% alpha, 4% tracking risk), Fund 3 (0% alpha, 0% tracking risk). Is this core-satellite?
> **Wrong approach:** Not core-satellite because funds track Index B, not the investor's Index A benchmark.
> **Correct approach:** Fund 3 has 0% alpha and 0% tracking risk = passive core (tracks Index B, which is highly correlated with Index A). Funds 1 and 2 have positive alpha and tracking risk = active satellites. This is a valid core-satellite structure: passive core provides market exposure, active satellites seek alpha. The technical benchmark difference (A vs B) doesn't invalidate the structure when indices are highly correlated. Answer: Correct core-satellite characterization.

---

## Pattern: Bond Covenant Payments and Stockholder Indifference

**Description:** Bond covenants specify fixed payment obligations (not state-contingent) that apply when conditions are met. To find the payment making stockholders indifferent between projects, equate expected equity values where equity = max(project payoff - bond payment, 0) due to limited liability, and solve for the covenant payment amount.

**When to Use:** Questions involving agency costs between bondholders and stockholders, bond covenants designed to align incentives, or finding payment amounts that create indifference between project choices.

**Procedure:**
1. Calculate expected equity value for the baseline project: E[max(payoff - original bond payment, 0)] across all states
2. For the alternative project with covenant payment X: equity in each state = max(payoff - X, 0)
3. Calculate expected equity value for alternative project: E[max(payoff - X, 0)]
4. Set the two expected equity values equal (indifference condition)
5. Solve for X (the covenant payment that creates indifference)
6. Verify that X is a single fixed amount (not state-dependent) and that limited liability (max function) is properly applied in all states
7. Check that the solution makes economic sense: covenant payment should be higher than original payment to offset the benefit stockholders get from choosing riskier project

**Example (sanitized):**
> **Scenario:** Two projects with equal probability states. Project L: pays $4,000 (bad) or $4,200 (good). Project H: pays $3,000 (bad) or $5,000 (good). Original bond payment = $3,800. Find covenant payment X for Project H that makes stockholders indifferent.
> **Wrong approach:** Average the payoffs and set equal.
> **Correct approach:** Project L equity: bad state = max(4000-3800, 0) = 200; good state = max(4200-3800, 0) = 400. E[equity_L] = 0.5(200) + 0.5(400) = 300. Project H equity with payment X: bad state = max(3000-X, 0); good state = max(5000-X, 0). Set E[equity_H] = 300: 0.5×max(3000-X, 0) + 0.5×max(5000-X, 0) = 300. If X > 3000: 0.5(0) + 0.5(5000-X) = 300 → 5000-X = 600 → X = 4,400. Verify: bad equity = 0, good equity = 600, expected = 300 ✓. Answer: $4,400.

---

## Pattern: Alpha-Beta Separation vs Core-Satellite Strategies

**Description:** Alpha-beta separation explicitly decouples alpha generation from beta exposure using separate vehicles: alpha is generated independently (often via market-neutral long-short strategies) while beta exposure is obtained through passive instruments (index futures/ETFs). This differs from core-satellite, which combines passive core with active satellites typically in the SAME market.

**When to Use:** Questions asking to classify portfolio structures that combine active strategies in one market with passive index exposure in a different market, or when "portable alpha" concepts are involved.

**Procedure:**
1. Identify the components: (a) alpha-generating strategy and its market, (b) beta exposure strategy and its market
2. Alpha-beta separation indicators: (a) alpha generated via market-neutral or long-short strategy (zero or low beta), (b) beta exposure obtained via passive index instrument, (c) alpha and beta are from DIFFERENT markets or sources
3. Core-satellite indicators: (a) passive core in primary market, (b) active satellites in same or related markets, (c) both components contribute to exposure in the target market
4. Key distinction: alpha-beta separation allows "portable alpha" where alpha from Market A is combined with beta from Market B; core-satellite keeps both components in the same market
5. Match the structure: if combining market-neutral active strategy (alpha) with passive index in different market (beta) → alpha-beta separation
6. Verify by checking if alpha and beta are explicitly separated and sourced independently

**Example (sanitized):**
> **Scenario:** A manager combines a long-short equity strategy in Market A (generates alpha, market-neutral) with a passive index fund tracking Market B. Classify as: (A) completeness fund, (B) core-satellite, (C) alpha-beta separation.
> **Wrong approach:** Passive index + active strategy = core-satellite structure.
> **Correct approach:** Alpha source: long-short strategy in Market A (market-neutral, generates alpha independently). Beta source: passive index in Market B (provides market exposure). These are DIFFERENT markets with explicitly separated alpha and beta. This is alpha-beta separation (portable alpha): alpha from Market A is "ported" to beta exposure in Market B. Core-satellite would have both components in the same market. Answer: C (alpha-beta separation).

---

## Pattern: Index Return Calculation by Weighting Scheme

**Description:** Index returns depend on the weighting methodology. Price-weighted indices return = average of price changes. Value-weighted indices return = change in total market capitalization. Equal-weighted indices return = arithmetic average of individual stock returns. The weighting scheme determines which stocks contribute most to index performance.

**When to Use:** Questions asking which index structure produces the highest/lowest return given specific stock performance data, or comparing returns across different weighting methodologies.

**Procedure:**
1. Identify available data: individual stock prices, price changes, market caps, market cap changes
2. Price-weighted return: (Σ price changes) / (Σ initial prices) or average of percentage price changes weighted by price
3. Value-weighted return: (total ending market cap - total beginning market cap) / total beginning market cap = Σ(weight_i × return_i) where weight_i = market cap proportion
4. Equal-weighted return: arithmetic average of individual stock returns = (Σ returns) / n
5. Calculate each return type using the provided data
6. Compare results to determine which weighting scheme produces highest/lowest return
7. Verify by checking that weights sum to 1.0 and that the calculation matches the weighting definition

**Example (sanitized):**
> **Scenario:** Three stocks. Stock A: price $10→$11 (10% return), market cap $100B→$110B. Stock B: price $20→$22 (10% return), market cap $50B→$55B. Stock C: price $5→$6 (20% return), market cap $25B→$30B. Which weighting produces highest return?
> **Wrong approach:** Equal-weighted captures Stock C's 20% return best.
> **Correct approach:** Equal-weighted: (10% + 10% + 20%)/3 = 13.33%. Price-weighted: focus on price levels, Stock B dominates (price $20 vs $10 vs $5), return ≈ (1+2+1)/(10+20+5) = 11.4%. Value-weighted: (110+55+30-100-50-25)/(100+50+25) = 20/175 = 11.4%. Actually recalculate value-weighted properly: initial = 175, final = 195, return = 20/175 = 11.4%. Equal-weighted = 13.33% is highest. Answer: equal-weighted.

---

## Pattern: Manager Selection Error Type Identification via Null Hypothesis

**Description:** In manager selection contexts, correctly identifying Type I and Type II errors requires first establishing the null hypothesis. When the null is "manager has skill/should be hired," Type I error = rejecting a skilled manager (opportunity cost), Type II error = hiring/retaining an unskilled manager (direct cost). Tracking systems reveal which errors occurred.

**When to Use:** Questions about manager evaluation frameworks, databases tracking hired/rejected/terminated managers, or policies designed to minimize specific error types.

**Procedure:**
1. Establish the null hypothesis in manager selection: typically H₀ = "manager has skill" or "manager should be hired/retained"
2. Define errors relative to null: Type I = reject H₀ when true (don't hire/fire a good manager); Type II = fail to reject H₀ when false (hire/keep a bad manager)
3. Map tracking databases to errors: tracking non-hired managers who passed screening → reveals Type I errors if they perform well; tracking terminated managers → reveals Type II errors (we hired them, then had to fire them)
4. Identify policy objectives: "minimize cost of firing good managers" → minimize Type I; "avoid retaining poor performers" → minimize Type II
5. Note the tradeoff: stricter hiring criteria reduce Type II but increase Type I; looser criteria reduce Type I but increase Type II
6. Verify by checking if the error classification aligns with the cost structure and decision framework described

**Example (sanitized):**
> **Scenario:** A fund tracks (Database 1) managers who passed initial screening but weren't hired, and (Database 2) managers who were hired then terminated for underperformance. The fund states it prioritizes avoiding the cost of retaining poor managers. Which errors do the databases address?
> **Wrong approach:** Database 1 = Type I (rejected good managers), Database 2 = Type II (kept bad managers).
> **Correct approach:** H₀ = manager has skill. Type I = reject skilled manager. Type II = accept unskilled manager. Database 1 tracks non-hired managers; if they perform well, we made a Type I error (rejected skilled manager). Database 2 tracks hired-then-fired managers; these are Type II errors (we accepted unskilled managers, then had to terminate). The fund's priority to avoid retaining poor managers means minimizing Type II errors. Both databases help identify past errors to improve future decisions. Answer: Database 1 addresses Type I, Database 2 addresses Type II.

## Pattern: Fundamental vs Quantitative Management Style Classification

**Description:** Fundamental management is characterized by bottom-up, security-specific analysis where portfolio managers conduct deep research into individual companies' business models, competitive positions, and financial statements to build conviction-based portfolios with relatively concentrated holdings. This differs from quantitative approaches that use systematic factor scoring, large-scale screening, or model-driven allocation across many securities, even when those quantitative approaches incorporate fundamental data inputs.

**When to Use:** Questions asking to identify which manager uses fundamental management, classify active management styles, compare investment approaches across multiple managers, or evaluate statements about fundamental vs quantitative investing. Trigger keywords: "fundamental management," "bottom-up analysis," "conviction-based," "financial statement analysis," "quantitative approach," "factor-based strategy," "screening," "systematic," "model-driven allocation," "proprietary software for screening," "optimization-based."

**When NOT to Use:** 
- When comparing portfolio characteristics (number of holdings, rebalancing frequency, risk perspective) between fundamental and quantitative strategies rather than identifying management style
- When the question focuses on operational differences (rebalancing schedules, portfolio turnover) rather than the core analytical approach
- When evaluating whether a strategy is top-down vs bottom-up (use the Top-Down vs Bottom-Up pattern instead)
- **When the question asks to select a manager based on multiple criteria including BOTH style classification (fundamental vs quantitative) AND other requirements like efficiency or policy adherence (must evaluate all criteria)**

**Procedure:**
1. Identify key characteristics of fundamental management: deep company-specific research, financial statement analysis, understanding of competitive landscape/business models, conviction-based position sizing, typically smaller number of holdings (concentrated portfolios)
2. Distinguish from quantitative approaches: systematic factor scoring, model-driven allocation, large-scale screening (hundreds/thousands of securities), optimization-based portfolio construction, software-driven security selection
3. Critical distinction: using fundamental data (financial models, accounting information) does NOT make an approach fundamental if the process is systematic screening or model-driven allocation rather than conviction-based selection
4. Look for evidence of individual security research depth AND conviction-based portfolio construction as the PRIMARY driver, not just as inputs to systematic processes
5. Red flags for quantitative (not fundamental): screening large universes (1000+ securities), optimization algorithms determining weights, factor-based ranking systems, software-driven selection processes
6. When comparing operational characteristics: quantitative strategies typically hold MORE stocks (broader factor exposure), rebalance MORE frequently (systematic rules), and focus on portfolio-level risk (factor models); fundamental strategies typically hold FEWER stocks (conviction-based), rebalance LESS frequently (discretionary timing), and emphasize company-specific analysis
7. Select the manager whose process emphasizes security-level fundamental analysis with conviction-based positioning, regardless of sophisticated analytical tools used

**Common Mistakes to Avoid:**
- Confusing use of fundamental data inputs (financial models, accounting information) with fundamental management style
- Assuming that detailed financial modeling automatically indicates fundamental management (quantitative approaches also use detailed models)
- Ignoring the portfolio construction process: conviction-based concentrated portfolios vs. systematic optimization across many securities
- Overlooking screening scale: analyzing 1000+ companies systematically is quantitative, not fundamental
- Incorrectly assuming quantitative strategies hold fewer stocks (they typically hold more due to systematic factor exposure across broad universes)
- Confusing rebalancing frequency with management style identification (this is an operational characteristic, not a style classifier)

**Example (sanitized):**
> **Scenario:** Three managers: Manager A's sector teams analyze 20-30 companies per sector through competitive analysis and financial statement review, selecting 5-8 highest conviction stocks per sector based on business quality assessments. Manager B screens 2,000 companies using proprietary models, builds detailed DCF models on 80+ firms, and uses quantitative risk optimization to determine final portfolio weights across 60 positions. Manager C ranks all securities by three factors (P/E, ROE, sales growth) and constructs an optimized 300-stock portfolio.
> **Wrong approach:** Selecting Manager B because they build detailed financial models and analyze fundamental data, equating analytical sophistication or use of fundamental inputs with fundamental management style.
> **Correct approach:** (1) Manager A conducts deep company-specific analysis (competitive landscape, financial statements) to build conviction-based concentrated portfolios—this is fundamental management. (2) Manager B uses systematic screening (2,000 companies) and quantitative optimization to determine allocations—this is quantitative/systematic despite using fundamental data as inputs. (3) Manager C uses pure factor scoring and optimization—clearly quantitative. (4) The key distinction: Manager A's process is conviction-driven selection; Manager B's process is model-driven allocation. (5) Select Manager A as most consistent with fundamental management.
## Pattern: Specialist Inventory Management and Order Book Imbalance

**Description:** Market specialists/dealers should increase inventory when buy orders significantly exceed sell orders (indicating upward price pressure and future selling opportunities at higher prices) and decrease inventory when sell orders exceed buy orders (indicating downward price pressure). The inventory decision is based on anticipated profitable liquidation, not on difficulty of current execution.

**When to Use:** Questions about specialist/dealer inventory decisions, market-making strategies, or limit order book analysis. Trigger keywords: "specialist," "market maker," "inventory," "limit order book," "bid-ask," "order imbalance."

**Procedure:**
1. Analyze the limit order book to identify imbalances: compare total quantity and depth of buy orders vs sell orders
2. Determine price pressure direction: excess buy orders → upward pressure; excess sell orders → downward pressure
3. Apply inventory strategy: when buy orders dominate, increase inventory to sell later at higher prices as demand pushes prices up
4. When sell orders dominate, decrease inventory to avoid holding securities that will decline in value
5. Recognize that strong buying pressure creates profitable inventory accumulation opportunities, not selling difficulties

**Example (sanitized):**
> **Scenario:** A specialist sees a limit order book with 3,000 shares of buy orders at prices $48-$49.50 (below last trade of $50) and only 800 shares of sell orders at prices $50.50-$55 (above last trade). 
> **Wrong approach:** Concluding the specialist should decrease inventory because strong buying pressure means difficulty selling accumulated shares, viewing excess demand as a risk rather than opportunity.
> **Correct approach:** (1) Identify order imbalance: 3,000 buy shares vs 800 sell shares indicates much stronger demand. (2) Recognize price pressure: excess buying will push prices upward. (3) Apply inventory strategy: increase inventory now by selling to buyers at current prices. (4) Plan to profit: as continued buying pressure drives prices higher toward the sparse sell orders, liquidate accumulated inventory at higher prices. (5) Conclude: increase inventory to capitalize on the upward price pressure from the demand imbalance.

---

## Pattern: Activist Investor Stake Size and Regulatory Thresholds

**Description:** Activist investors typically take stakes of 5-10% (less than 10%) in target companies due to regulatory disclosure requirements, capital efficiency, and strategic considerations. Stakes exceeding 10% trigger additional regulatory burdens and are generally avoided unless control is necessary. This is a factual characteristic independent of investment time horizon or tactics used.

**When to Use:** Questions about activist investing characteristics, typical stake sizes, regulatory considerations in activist campaigns, or evaluating statements about activist investor behavior. Trigger keywords: "activist investor," "stake size," "ownership percentage," "10% threshold," "disclosure requirements."

**Procedure:**
1. Recall that activist investors typically take stakes of 5-10%, generally remaining below 10%
2. Recognize that exceeding 10% ownership triggers additional SEC disclosure requirements (Schedule 13D within 10 days, more frequent updates)
3. Understand that staying below 10% allows capital efficiency (influencing multiple companies with smaller stakes) and strategic flexibility
4. Note that 10%+ stakes are taken only when control or board majority is specifically needed
5. When evaluating statements about activist investing, verify stake size claims against the typical <10% pattern

**Example (sanitized):**
> **Scenario:** A manager states that activist investors focusing on governance issues "typically take stakes greater than 10% of target companies' outstanding equity and use tactics like seeking board representation and proxy contests."
> **Wrong approach:** Focusing on time horizon claims or tactics similarity while accepting the stake size claim as reasonable, or assuming that seeking board representation requires >10% ownership.
> **Correct approach:** (1) Identify the factual claim about stake sizes (>10%). (2) Recall that activist investors typically take stakes of 5-10%, staying below 10% to avoid additional regulatory burdens. (3) Recognize that board representation and proxy contests can be pursued effectively with <10% stakes through coalition-building and shareholder support. (4) Conclude the statement is incorrect because activists typically take stakes less than 10%, not greater than 10%. (5) The tactics described (board representation, proxy contests) are correct, but the stake size characterization is factually wrong.

## Pattern: Systematic Risk Measurement via Beta Calculation

**Description:** Systematic risk (market risk) is measured by beta, which quantifies a security's sensitivity to market movements. Beta = Cov(Stock Return, Market Return) / Var(Market Return). Higher beta means higher systematic risk. Total volatility, expected return levels, and return ranges do NOT measure systematic risk—they reflect total risk including unsystematic (diversifiable) risk. Counter-cyclical stocks (high returns in recessions) typically have low or negative beta despite high volatility.

**When to Use:** Questions asking which security has the most/least systematic risk, comparing systematic risk across securities, identifying market sensitivity, or evaluating beta-related statements. Trigger keywords: "systematic risk," "market risk," "beta," "sensitivity to market movements," "which stock has the most systematic risk," "compare systematic risk," "non-diversifiable risk."

**Procedure:**
1. Recall that systematic risk = beta, measuring sensitivity to market/economic conditions
2. If beta values are provided directly, compare them (higher beta = higher systematic risk)
3. If calculating beta from return data: beta = Cov(Stock, Market) / Var(Market)
4. If inferring beta qualitatively: analyze how returns vary with economic states—stocks with returns positively correlated with economic expansion (high in boom, low in recession) have positive beta; counter-cyclical stocks (high in recession, low in boom) have low/negative beta
5. DO NOT use expected return levels, total return volatility, or return ranges as proxies for systematic risk—these measure total risk, not systematic risk
6. Recognize that stable, positively correlated returns across economic states indicate higher systematic risk than volatile but counter-cyclical returns
7. Verify by checking correlation with market/economic conditions, not total variability

**Example (sanitized):**
> **Scenario:** Three stocks with returns across economic states. Stock X: 8% (recession), 12% (normal), 15% (boom). Stock Y: 20% (recession), 14% (normal), 10% (boom). Stock Z: 5% (recession), 18% (normal), 25% (boom). Which has the most systematic risk?
> **Wrong approach:** Stock Y has the widest return range (20% to 10%) and highest expected return, so it has the most systematic risk.
> **Correct approach:** (1) Systematic risk = beta = sensitivity to market/economic conditions. (2) Stock X: returns increase with economic expansion (8%→12%→15%), positively correlated with market, moderate positive beta. (3) Stock Y: returns DECREASE with economic expansion (20%→14%→10%), counter-cyclical, negative beta, LOW systematic risk despite high volatility. (4) Stock Z: returns strongly increase with economic expansion (5%→18%→25%), highly positively correlated with market, HIGH positive beta. (5) Stock Z has the most systematic risk (highest beta) because its returns are most sensitive to economic/market conditions. Answer: Stock Z.

**Common Mistakes to Avoid:**
- Using expected return levels as a proxy for systematic risk (high expected return ≠ high systematic risk)
- Using total return volatility or return range as a measure of systematic risk (volatility includes unsystematic risk)
- Confusing dramatic return variation with systematic risk (counter-cyclical stocks can be highly volatile but have low systematic risk)
- Failing to analyze correlation with market/economic conditions (the defining characteristic of systematic risk)

## Pattern: Index Weighting Methodologies and Small-Cap Bias

**Description:** Different index weighting schemes create different biases toward company size. Equal-weighted indices systematically overweight small-cap stocks because each stock receives the same weight regardless of market capitalization, giving small companies disproportionate representation relative to their economic significance. Value-weighted (market-cap weighted) indices naturally weight by company size, avoiding small-cap bias. Price-weighted indices weight by share price, which has no systematic relationship to market capitalization (small-cap stocks can have high or low prices).

**When to Use:** Questions about selecting index weighting methodologies when avoiding small-cap bias is a stated requirement, or comparing how different weighting schemes affect portfolio composition by company size.

**Procedure:**
1. Identify the stated requirement regarding company size bias (e.g., "not be biased towards small-capitalization stocks")
2. Evaluate equal-weighted indices: Each stock receives 1/n weight regardless of market cap, systematically overweighting small-cap stocks relative to their market value
3. Evaluate value-weighted indices: Stocks weighted by market capitalization (price × shares outstanding), naturally reflecting company size without small-cap bias
4. Evaluate price-weighted indices: Stocks weighted by share price alone; no systematic relationship to market cap (a $100 stock could be small-cap or large-cap depending on shares outstanding)
5. Match weighting scheme to requirement: To avoid small-cap bias, eliminate equal-weighted indices; value-weighted indices are optimal for market-cap proportional representation
6. Recognize that equal-weighting is the MOST biased toward small-caps, as it gives a $1B company the same weight as a $100B company

**Common Mistakes to Avoid:**
- Assuming price-weighted indices are biased toward small-cap stocks (share price ≠ market capitalization)
- Failing to recognize that equal-weighting systematically overweights smaller companies
- Confusing "equal treatment" (equal-weighted) with "no bias" (equal-weighting creates the strongest small-cap bias)
- Thinking that value-weighting creates small-cap bias (it actually reflects market cap proportionally)

**Example (sanitized):**
> **Scenario:** An investor wants to create a passive index portfolio and states the key requirement is that the weighting method "not be biased towards small-capitalization stocks." Three options: equal-weighted, value-weighted, price-weighted.
> **Wrong approach:** Equal-weighted treats all stocks equally, so it has no bias. Price-weighted might bias toward high-priced small-cap stocks.
> **Correct approach:** (1) Equal-weighted gives each stock 1/n weight regardless of size, systematically overweighting small-caps (a $1B company gets same weight as $100B company). (2) Value-weighted weights by market cap, proportionally representing company size without small-cap bias. (3) Price-weighted weights by share price, which has no systematic relationship to market cap. (4) To avoid small-cap bias, equal-weighted is LEAST appropriate because it creates the strongest small-cap overweight. Answer: Equal-weighted least likely meets the requirement.

---

## Pattern: Systematic Risk Identification via Return Patterns Across Economic States

**Description:** Systematic risk (market risk/beta) measures a security's sensitivity to market or economic conditions, not total return volatility. Securities with returns that increase during economic expansion and decrease during recession have positive beta (high systematic risk). Securities with counter-cyclical returns (high in recession, low in expansion) have low or negative beta (low systematic risk) despite potentially high total volatility. Beta = Cov(Stock, Market) / Var(Market), reflecting correlation with economic/market conditions.

**When to Use:** Questions asking which security has the most/least systematic risk, comparing market sensitivity across securities, or identifying beta when return data across economic states is provided. Trigger keywords: "systematic risk," "market risk," "beta," "which stock has the most systematic risk," "riskier" in context of market sensitivity.

**Procedure:**
1. Recall that systematic risk = beta = sensitivity to market/economic conditions, NOT total volatility
2. Examine return patterns across economic states (recession, normal, boom/expansion)
3. Identify pro-cyclical stocks: returns increase with economic expansion (low in recession → high in boom) = positive beta = HIGH systematic risk
4. Identify counter-cyclical stocks: returns decrease with economic expansion (high in recession → low in boom) = negative or low beta = LOW systematic risk
5. Calculate or infer beta: stocks with strongest positive correlation to economic conditions have highest systematic risk
6. DO NOT use expected return levels, total return ranges, or return volatility as proxies for systematic risk—these measure total risk including unsystematic (diversifiable) risk
7. The stock with returns most positively correlated with economic expansion has the MOST systematic risk
8. Verify by checking: Does the stock perform better in good economic times and worse in bad times? If yes → high systematic risk

**Common Mistakes to Avoid:**
- Using total return volatility or return range as a measure of systematic risk (volatility includes unsystematic risk)
- Assuming high expected return indicates high systematic risk (return level ≠ market sensitivity)
- Confusing dramatic return variation with systematic risk (counter-cyclical stocks can be highly volatile but have LOW systematic risk)
- Failing to analyze correlation with economic/market conditions (the defining characteristic of systematic risk)
- Selecting the stock with highest volatility when asked for "most systematic risk" without checking correlation with market

**Example (sanitized):**
> **Scenario:** Three stocks with returns across economic states. Stock X: 8% (recession), 12% (normal), 15% (boom). Stock Y: 20% (recession), 14% (normal), 10% (boom). Stock Z: 5% (recession), 18% (normal), 25% (boom). Which has the most systematic risk?
> **Wrong approach:** Stock Y has the widest return range (20% to 10%) and highest recession return, so it has the most systematic risk.
> **Correct approach:** (1) Systematic risk = beta = sensitivity to market/economic conditions. (2) Stock X: returns increase with economic expansion (8%→12%→15%), positively correlated with market, moderate positive beta. (3) Stock Y: returns DECREASE with economic expansion (20%→14%→10%), counter-cyclical, negative beta, LOW systematic risk despite high volatility. (4) Stock Z: returns strongly increase with economic expansion (5%→18%→25%), highly positively correlated with market, HIGH positive beta. (5) Stock Z has the most systematic risk (highest beta) because its returns are most sensitive to economic/market conditions. Answer: Stock Z.