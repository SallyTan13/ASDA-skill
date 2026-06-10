# Skill Patterns for Financial QA - Equity Analysis

## Pattern: Portfolio Return Calculation by Index Weighting Method

**Description:** Confusion between how different index weighting schemes (price-weighted, value-weighted, equal-weighted) calculate returns, particularly misunderstanding that price-weighted returns depend on absolute price changes (not percentage changes or highest prices), while value-weighted returns depend on market-cap-weighted percentage returns.

**When to Use:** Questions asking which index structure produces the highest/lowest return given stock price and market cap data. Keywords: "price-weighted," "value-weighted," "equal-weighted," "index return," "rebalancing."

**Procedure:**
1. Identify the weighting scheme being evaluated (price-weighted, value-weighted, or equal-weighted)
2. For **price-weighted index**: Calculate return as sum of absolute price changes divided by sum of initial prices: (ΣΔPrice) / (ΣPrice_initial)
3. For **value-weighted index**: Calculate return as weighted average of percentage returns using initial market cap weights: Σ(MarketCap_i / Total_MarketCap) × Return_i
4. For **equal-weighted index**: Calculate return as simple arithmetic average of individual stock returns: (1/n) × ΣReturn_i
5. Compare the calculated returns across all three methods to determine which produces the highest/lowest return
6. Verify: In price-weighted, stocks with higher absolute prices have more influence; in value-weighted, stocks with larger market caps dominate; in equal-weighted, all stocks contribute equally regardless of price or size

**Example (sanitized):**
> **Scenario:** Three stocks in an index: Stock A ($10 → $12, market cap $100M → $120M), Stock B ($50 → $52, market cap $200M → $208M), Stock C ($100 → $110, market cap $300M → $330M). Which weighting produces highest return?
> **Wrong approach:** Assuming price-weighted favors the stock with highest price ($100) or highest percentage gain (20% for Stock A).
> **Correct approach:** Price-weighted return = ($2 + $2 + $10) / ($10 + $50 + $100) = $14/$160 = 8.75%. Value-weighted return = (100/600)×20% + (200/600)×4% + (300/600)×10% = 3.33% + 1.33% + 5% = 9.67%. Equal-weighted = (20% + 4% + 10%)/3 = 11.33%. Equal-weighted produces highest return.

---

## Pattern: Factor Contribution to Portfolio Variance in Multi-Factor Models

**Description:** Misunderstanding how to decompose total portfolio variance to isolate the proportion explained by a single factor in a multi-factor model, incorrectly using (β²×Var(factor))/Var(portfolio) instead of the proper covariance-based calculation.

**When to Use:** Questions asking for the portion/percentage of portfolio risk explained by a specific factor. Keywords: "portion of risk explained," "market factor contribution," "R-squared," "variance decomposition," factor model.

**Procedure:**
1. Identify the factor of interest (e.g., market factor) and its coefficient (β)
2. Locate the variance of the factor and its covariance with the portfolio (or market factor variance if portfolio variance decomposition is given)
3. Calculate the factor's contribution to portfolio variance using: Contribution = β × Cov(factor, portfolio)
4. For the **market factor specifically**, if given factor loadings and covariances: Market contribution = β_market² × Var(market) + β_market × Σ(β_i × Cov(market, factor_i)) for all other factors
5. Calculate total portfolio variance: either given directly as σ²_portfolio, or compute from monthly standard deviation by squaring it
6. Calculate proportion explained: (Factor contribution to variance) / (Total portfolio variance)
7. Convert to percentage and verify it falls within [0%, 100%]

**Example (sanitized):**
> **Scenario:** Portfolio has market factor loading of 1.2, market factor variance of 0.0015, covariance between market and portfolio of 0.0018, and total portfolio variance of 0.0025. What portion of risk is explained by the market factor?
> **Wrong approach:** (1.2² × 0.0015) / 0.0025 = 0.00216 / 0.0025 = 86.4%
> **Correct approach:** Market contribution = 1.2 × 0.0018 = 0.00216. Proportion = 0.00216 / 0.0025 = 86.4%. While the numerical answer may coincidentally match, the correct formula uses β × Cov(market, portfolio), not β² × Var(market). When full covariance matrix is given, use: β_market × [β_market × Var(market) + Σ other covariance terms] / Var(portfolio).

---

## Pattern: Portfolio Tracking Error Aggregation from Multiple Managers

**Description:** Incorrectly calculating combined tracking error across multiple managers using weighted averages instead of the proper variance aggregation formula that requires squaring, weighting, summing, and taking the square root.

**When to Use:** Questions asking whether a portfolio meets tracking error goals when multiple managers with different tracking errors are combined. Keywords: "tracking error," "multiple managers," "portfolio goal," "combined risk."

**Procedure:**
1. Identify each manager's allocation weight (w_i = Investment_i / Total_Investment)
2. Identify each manager's individual tracking error (TE_i)
3. **Assuming zero correlation between managers' active returns** (standard assumption unless stated otherwise), calculate combined tracking error: TE_portfolio = √[Σ(w_i² × TE_i²)]
4. Square each manager's tracking error: TE_i²
5. Multiply each squared tracking error by the squared weight: w_i² × TE_i²
6. Sum all weighted squared tracking errors: Σ(w_i² × TE_i²)
7. Take the square root of the sum to get portfolio tracking error
8. Compare the calculated portfolio tracking error against the stated goal/threshold
9. Verify: Portfolio tracking error is always less than the weighted average of individual tracking errors when managers are uncorrelated

**Example (sanitized):**
> **Scenario:** Portfolio has three managers: Manager X ($60M, 0% TE), Manager Y ($30M, 3% TE), Manager Z ($10M, 5% TE). Total = $100M. Goal: TE < 1.5%. Does it meet the goal?
> **Wrong approach:** Weighted average TE = (60/100)×0% + (30/100)×3% + (10/100)×5% = 0% + 0.9% + 0.5% = 1.4% < 1.5%, so it meets the goal.
> **Correct approach:** TE_portfolio = √[(0.6²×0²) + (0.3²×3²) + (0.1²×5²)] = √[0 + 0.09×9 + 0.01×25] = √[0.81 + 0.25] = √1.06 = 1.03% < 1.5%. Yes, it meets the goal. Note: The correct answer is lower than the weighted average.

---

## Pattern: Portfolio Alpha Aggregation from Multiple Managers

**Description:** Correctly calculating combined expected alpha across multiple managers requires a weighted average using allocation weights, but must be computed accurately and compared against stated thresholds with proper margin assessment.

**When to Use:** Questions asking whether a portfolio meets alpha goals when multiple managers with different expected alphas are combined. Keywords: "expected alpha," "multiple managers," "portfolio goal," "alpha target."

**Procedure:**
1. Identify each manager's allocation weight: w_i = Investment_i / Total_Investment
2. Identify each manager's expected alpha (α_i)
3. Calculate portfolio expected alpha as weighted average: α_portfolio = Σ(w_i × α_i)
4. Multiply each manager's alpha by their weight: w_i × α_i
5. Sum all weighted alphas to get total portfolio alpha
6. Compare the calculated portfolio alpha against the stated goal/threshold
7. Assess whether the portfolio meets the requirement with adequate margin (e.g., if goal is ">0.40%", verify the calculated alpha clearly exceeds this)
8. Verify calculation: Ensure all weights sum to 1.0 and alpha values are in consistent units (percentage points)

**Example (sanitized):**
> **Scenario:** Portfolio has three managers: Manager X ($150M, 0% alpha), Manager Y ($30M, 2% alpha), Manager Z ($20M, 3% alpha). Total = $200M. Goal: alpha > 0.50%. Does it meet the goal?
> **Wrong approach:** Calculating (150×0 + 30×2 + 20×3)/200 = 120/200 = 0.60%, then incorrectly doubting whether 0.60% > 0.50% is sufficient margin.
> **Correct approach:** α_portfolio = (150/200)×0% + (30/200)×2% + (20/200)×3% = 0% + 0.30% + 0.30% = 0.60%. Since 0.60% > 0.50%, the portfolio meets the alpha goal. The margin of 0.10 percentage points (20% above threshold) is adequate.

---

## Pattern: Simultaneous Multi-Criteria Portfolio Goal Assessment

**Description:** When a portfolio must meet multiple goals simultaneously (e.g., both alpha and tracking error thresholds), each criterion must be evaluated independently using the correct aggregation method, then all results must be checked against their respective thresholds before concluding whether the portfolio meets its overall objectives.

**When to Use:** Questions asking whether a portfolio meets its goals when multiple performance criteria are specified. Keywords: "meet goals," "alpha and tracking error," "multiple requirements," "portfolio objectives."

**Procedure:**
1. Identify all stated goals/criteria (e.g., "alpha > X%" AND "tracking error < Y%")
2. For each criterion, apply the appropriate aggregation method:
   - For alpha: use weighted average Σ(w_i × α_i)
   - For tracking error: use variance aggregation √[Σ(w_i² × TE_i²)]
3. Calculate each metric independently and completely
4. Compare each calculated metric against its specific threshold
5. Determine pass/fail for each individual criterion
6. The portfolio meets its goals ONLY if ALL criteria are satisfied simultaneously
7. If any single criterion fails, identify which one(s) failed for the answer
8. Verify: Double-check arithmetic and ensure consistent units across all calculations

**Example (sanitized):**
> **Scenario:** Portfolio with 2 managers must achieve alpha > 0.30% AND tracking error < 2.0%. Manager A: $80M, 0.5% alpha, 1% TE. Manager B: $20M, 1.0% alpha, 4% TE. Does it meet goals?
> **Wrong approach:** Calculating only alpha or only tracking error, or using wrong formulas for either.
> **Correct approach:** (1) Alpha = (80/100)×0.5% + (20/100)×1.0% = 0.4% + 0.2% = 0.6% > 0.30% ✓. (2) TE = √[(0.8²×1²) + (0.2²×4²)] = √[0.64 + 0.16] = √0.80 = 0.89% < 2.0% ✓. Both criteria met, so answer is "Yes."