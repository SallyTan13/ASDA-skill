# Equity — Portfolio Management Concept Distinctions

## Pattern: performance_attribution_vs_appraisal

**Description:** Distinguishing between performance attribution (descriptive decomposition of returns into factor contributions) and performance appraisal (evaluative judgment of manager skill/quality). Attribution answers "HOW did returns occur?" while appraisal answers "DOES the manager have skill?"

**When to Use:** Questions about performance evaluation frameworks, manager assessment processes, or distinguishing analytical vs evaluative activities.

**Procedure:**
1. Identify whether the activity is descriptive (breaking down what happened) or evaluative (judging quality/skill)
2. Performance attribution = decomposing returns into sources (market, sector, security selection, timing)
3. Performance appraisal = drawing conclusions about manager ability, skill persistence, or quality
4. Attribution is input to appraisal, but they are distinct processes
5. Attribution is objective decomposition; appraisal involves subjective judgment about skill

**Example (sanitized):**
> **Scenario:** A consultant describes two activities: (1) decomposing portfolio returns into allocation and selection effects, (2) determining whether the manager demonstrates genuine stock-picking ability.
> **Wrong approach:** Treating both as performance attribution since they both analyze returns.
> **Correct approach:** Activity 1 is attribution (descriptive decomposition), Activity 2 is appraisal (evaluative conclusion about skill).

---

## Pattern: error_types_in_manager_selection

**Description:** Understanding Type I errors (rejecting a good manager) vs Type II errors (accepting/retaining a bad manager) in hiring and retention contexts. Post-decision tracking mechanisms typically aim to minimize Type II errors by validating that poor managers aren't kept.

**When to Use:** Questions about manager selection policies, due diligence processes, or error minimization in hiring/firing decisions.

**Procedure:**
1. Define the null hypothesis in the decision context (e.g., "manager is adequate")
2. Type I error = rejecting null when true (firing good manager, not hiring good manager)
3. Type II error = accepting null when false (keeping bad manager, hiring bad manager)
4. Post-hire tracking of rejected candidates = checking for Type II errors in hiring (missed opportunities)
5. Post-hire tracking of retained managers = checking for Type II errors in retention (kept bad managers too long)
6. Most institutional processes prioritize minimizing Type II errors (avoiding bad managers) over Type I

**Example (sanitized):**
> **Scenario:** A firm tracks: (A) candidates they rejected who later performed well elsewhere, (B) hired managers who underperform after 2 years.
> **Wrong approach:** Thinking (A) minimizes Type I errors and (B) minimizes Type II errors.
> **Correct approach:** Both minimize Type II errors: (A) identifies failures to hire good managers (Type II in hiring context), (B) identifies failures to remove bad managers (Type II in retention context).

---

## Pattern: investment_vehicle_selection_by_client_type

**Description:** Matching investment vehicle structure (pooled accounts, mutual funds, ETFs, separately managed accounts) to client characteristics including size, number of investors, customization needs, and investor sophistication.

**When to Use:** Questions about choosing appropriate portfolio structures, investment vehicles, or fund formats for different client segments.

**Procedure:**
1. Identify client characteristics: number of investors, size per investor, sophistication, customization needs
2. Pooled accounts = few large institutional clients, high customization, cost-efficient for large assets
3. Mutual funds = many small/retail investors, standardized strategy, regulatory protections
4. ETFs = broad market access, high liquidity needs, transparent holdings, tax efficiency
5. Separately managed accounts = single high-net-worth client, maximum customization
6. Match vehicle to primary client need (customization vs cost vs liquidity vs simplicity)

**Example (sanitized):**
> **Scenario:** A manager must choose between ETF, mutual fund, or pooled account for 3 pension funds with $500M each seeking customized ESG screens.
> **Wrong approach:** Selecting ETF for cost efficiency and liquidity.
> **Correct approach:** Pooled account is optimal—few large institutional clients with customization needs and sufficient scale for cost efficiency.

---

## Pattern: active_risk_and_correlation_structure

**Description:** Active risk (tracking error) depends on the covariance structure of active positions, not just their magnitude. Replacing correlated positions with less correlated ones increases active risk even if position sizes are unchanged.

**When to Use:** Questions about how portfolio changes affect active risk, tracking error, or when evaluating trade impacts on risk metrics.

**Procedure:**
1. Recognize that active risk = √(active weights' × covariance matrix × active weights)
2. Positions in highly correlated securities provide diversification within the active portfolio
3. Replacing correlated positions (e.g., two stocks in same sector) with uncorrelated positions reduces diversification benefit
4. Lower correlation between active positions → higher active risk (less offsetting)
5. Equal magnitude position changes can increase or decrease active risk depending on correlation changes
6. Consider sector/factor correlations when assessing risk impact of trades

**Example (sanitized):**
> **Scenario:** A portfolio replaces two overweight positions in technology stocks (+2% each) with one overweight in technology (+2%) and one in utilities (+2%).
> **Wrong approach:** Assuming active risk unchanged because total active position magnitude is constant.
> **Correct approach:** Active risk likely increases because tech and utilities are less correlated than two tech stocks, reducing diversification benefit within the active portfolio.

---

## Pattern: probability_specification_in_discrete_distributions

**Description:** Statistical calculations (expected value, variance, standard deviation) for discrete probability distributions require explicit probabilities for each state. Missing or ambiguous probability information invalidates calculations using assumed equal probabilities.

**When to Use:** Questions involving scenario analysis, state-dependent returns, or discrete probability distributions where probabilities may be implicit, missing, or require extraction from context.

**Procedure:**
1. Identify all discrete states/scenarios in the problem
2. Check if probabilities are explicitly provided for each state
3. If probabilities are missing, look for contextual clues (historical frequencies, expert judgments, implied probabilities)
4. Do NOT assume equal probabilities unless explicitly stated or clearly implied
5. For expected value: E(X) = Σ[P(state) × outcome(state)]
6. For variance: Var(X) = Σ[P(state) × (outcome(state) - E(X))²]
7. Verify that probabilities sum to 1.0
8. If probabilities cannot be determined, flag as insufficient information

**Example (sanitized):**
> **Scenario:** Returns are given for three economic scenarios (recession, normal, expansion) but no probabilities are stated. A table elsewhere shows historical frequency: recession 20%, normal 50%, expansion 30%.
> **Wrong approach:** Assuming equal 33.33% probability for each scenario.
> **Correct approach:** Extract probabilities from historical frequency data (20%, 50%, 30%) and use these in expected return and standard deviation calculations.

---

## Pattern: institutional_vs_retail_investment_considerations

**Description:** Institutional investors (pensions, endowments, sovereign wealth) have different needs than retail investors regarding customization, governance, reporting, fee structures, and regulatory requirements.

**When to Use:** Questions comparing investment solutions for different investor types or evaluating appropriateness of investment structures.

**Procedure:**
1. Classify investor as institutional (large, sophisticated, fiduciary duties) or retail (small, less sophisticated, regulatory protections)
2. Institutional priorities: customization, governance rights, cost efficiency at scale, complex reporting
3. Retail priorities: simplicity, liquidity, regulatory protections, standardized products
4. Institutional investors can negotiate terms, access private markets, use derivatives
5. Retail investors need transparent, liquid, regulated products
6. Match solution complexity to investor sophistication and size

**Example (sanitized):**
> **Scenario:** Choosing between a standardized index fund and a customized separate account for a $50M endowment with specific ethical restrictions.
> **Wrong approach:** Recommending the index fund for lower costs and simplicity.
> **Correct approach:** The separate account allows customization for ethical restrictions, and $50M provides sufficient scale for cost-effective implementation—appropriate for institutional needs.

---

## Pattern: factor_exposure_and_diversification_effects

**Description:** Portfolio risk depends on factor exposures and correlations between holdings. Diversification benefit is maximized when holdings have low correlation; concentration in correlated assets (same sector, same factors) reduces diversification.

**When to Use:** Questions about portfolio risk changes from rebalancing, sector rotation, or factor exposure adjustments.

**Procedure:**
1. Identify the factor/sector exposures of positions being added or removed
2. Assess correlation between new and existing positions
3. Replacing highly correlated positions with less correlated ones generally increases portfolio variance
4. Replacing uncorrelated positions with correlated ones generally decreases portfolio variance
5. Consider both systematic (factor) and idiosyncratic correlations
6. Higher concentration in single factors/sectors → higher risk for given position sizes

**Example (sanitized):**
> **Scenario:** A portfolio sells two healthcare stocks and buys one healthcare and one consumer staples stock, maintaining equal total position sizes.
> **Wrong approach:** Concluding risk is unchanged because position magnitudes are equal.
> **Correct approach:** Risk likely increases slightly because healthcare and consumer staples are less correlated than two healthcare stocks, reducing diversification benefit.

---

## Pattern: performance_measurement_framework_components

**Description:** Comprehensive performance evaluation includes multiple components: measurement (calculating returns), attribution (decomposing sources), appraisal (judging skill), and feedback (informing decisions). Each serves distinct purposes.

**When to Use:** Questions about performance evaluation systems, manager assessment frameworks, or components of performance analysis.

**Procedure:**
1. Performance measurement = calculating returns accurately (time-weighted, money-weighted)
2. Performance attribution = decomposing returns into sources (allocation, selection, interaction)
3. Performance appraisal = evaluating whether returns reflect skill vs luck
4. Performance feedback = using results to inform portfolio decisions
5. These are sequential but distinct activities
6. Attribution provides inputs to appraisal but doesn't itself judge quality

**Example (sanitized):**
> **Scenario:** A process includes: (A) calculating quarterly returns, (B) breaking returns into sector allocation and stock selection effects, (C) determining if selection effects are statistically significant.
> **Wrong approach:** Calling all three "performance attribution."
> **Correct approach:** (A) is measurement, (B) is attribution, (C) is appraisal—each serves a different analytical purpose.

---

## Pattern: tracking_error_decomposition

**Description:** Tracking error (active risk) arises from active weights relative to benchmark and depends on the covariance structure of those active positions. It can be decomposed into contributions from different positions or factors.

**When to Use:** Questions about sources of tracking error, how trades affect active risk, or decomposing portfolio risk relative to benchmark.

**Procedure:**
1. Active weight = portfolio weight - benchmark weight for each security
2. Tracking error = standard deviation of (portfolio return - benchmark return)
3. TE² = active weights' × covariance matrix × active weights
4. Contribution to TE from position i depends on its active weight and covariances with other active positions
5. Trades that increase active weights or reduce correlation between active positions increase TE
6. Trades that decrease active weights or increase correlation between active positions decrease TE

**Example (sanitized):**
> **Scenario:** A portfolio has +3% active weight in two energy stocks. It reduces one energy position to +1% and adds +2% to a financial stock.
> **Wrong approach:** Thinking tracking error decreases because total active weight magnitude decreased.
> **Correct approach:** Tracking error likely increases because energy and financials are less correlated than two energy stocks, reducing offsetting effects in the active portfolio.

---

SKILL_MD_ENTRY: | `equity/new_patterns.md` | Equity | Portfolio Management Concept Distinctions | performance_attribution_vs_appraisal, error_types_in_manager_selection, investment_vehicle_selection_by_client_type, active_risk_and_correlation_structure, probability_specification_in_discrete_distributions, institutional_vs_retail_investment_considerations, factor_exposure_and_diversification_effects, performance_measurement_framework_components, tracking_error_decomposition |