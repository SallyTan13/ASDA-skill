# Equity — Risk Decomposition and Portfolio Strategy Concepts

## Pattern 1: statistical_measures_from_discrete_distributions

**Description:** When calculating standard deviation, variance, or expected return from discrete state-contingent outcomes, must correctly apply probability-weighted formulas. Common errors include assuming equal probabilities when not stated, incorrect variance calculation, or confusing sample vs. population formulas.

**When to Use:** Questions involving "calculate standard deviation," "expected return," "variance" with returns given across different economic states, scenarios, or outcomes.

**Procedure:**
1. **Identify probabilities**: If probabilities are given explicitly, use them. If not stated, assume equal probabilities across all states.
2. **Calculate expected return**: E(R) = Σ[P(i) × R(i)] where P(i) is probability of state i and R(i) is return in state i.
3. **Calculate variance**: Var(R) = Σ[P(i) × (R(i) - E(R))²]
4. **Calculate standard deviation**: σ = √Var(R)
5. **Unit check**: Ensure returns are in consistent units (decimals vs. percentages) throughout calculation.
6. **Express answer**: Convert to requested format (typically percentage for standard deviation).

**Example (sanitized):**
> **Scenario:** An asset has returns of 5%, 10%, and 20% in three equally likely economic scenarios. Calculate standard deviation.
> 
> **Wrong approach:** Taking standard deviation of the three numbers directly without probability weighting, or using incorrect variance formula: σ = √[(5² + 10² + 20²)/3] = 12.7%
> 
> **Correct approach:** 
> - E(R) = (1/3)(5%) + (1/3)(10%) + (1/3)(20%) = 11.67%
> - Var(R) = (1/3)(5% - 11.67%)² + (1/3)(10% - 11.67%)² + (1/3)(20% - 11.67%)² = 38.89
> - σ = √38.89 = 6.24%

---

## Pattern 2: active_risk_and_correlation_effects

**Description:** Active risk (tracking error) depends on both active weights and the correlation structure between positions. Replacing highly correlated positions with less correlated ones increases active risk even if position sizes remain constant, because diversification benefits decrease.

**When to Use:** Questions about "active risk," "tracking error," portfolio trades involving sector rotation, or asking how risk changes when replacing positions.

**Procedure:**
1. **Understand active risk formula**: Active Risk² = Σᵢ Σⱼ [wᵢᴬ × wⱼᴬ × Cov(i,j)] where wᴬ represents active weights.
2. **Identify correlation structure**: Determine if positions being replaced are in same sector (high correlation) or different sectors (lower correlation).
3. **Assess offsetting effects**: 
   - Same-sector positions: High correlation means their active risks partially offset
   - Cross-sector positions: Lower correlation means less offsetting, higher combined risk
4. **Direction of change**: Replacing high-correlation pairs with low-correlation pairs increases active risk; the reverse decreases it.
5. **Consider magnitude**: Even with identical active weights, correlation differences drive risk changes.

**Example (sanitized):**
> **Scenario:** A portfolio has two overweight positions in Technology sector stocks (correlation 0.7). Manager replaces one Tech position with a Healthcare overweight of same size. Tech-Healthcare correlation is 0.3.
> 
> **Wrong approach:** "Active weights unchanged, so active risk unchanged."
> 
> **Correct approach:** Original setup had high correlation (0.7) providing offsetting effects. New setup has lower correlation (0.3), reducing diversification benefit. Active risk increases because the covariance term Cov(Tech, Healthcare) < Cov(Tech, Tech), reducing the negative offset in the active risk calculation.

---

## Pattern 3: alpha_beta_separation_vs_core_satellite

**Description:** Alpha/beta separation and core-satellite are distinct portfolio strategies often confused. Alpha/beta separation explicitly separates alpha generation from beta exposure, often across different markets. Core-satellite uses a passive core with active satellites, typically within the same benchmark framework.

**When to Use:** Questions asking to identify portfolio strategy type, especially when describing combinations of active and passive management across markets or asset classes.

**Procedure:**
1. **Identify alpha/beta separation characteristics**:
   - Active management in one market/asset class for alpha generation
   - Passive management in another market/asset class for beta exposure
   - Explicit separation of alpha sources from beta sources
   - Often involves different geographic markets or asset classes
   
2. **Identify core-satellite characteristics**:
   - Large passive "core" position (typically 70-90% of portfolio)
   - Multiple smaller active "satellite" positions around the core
   - Usually within same benchmark or asset class framework
   - Satellites seek to add alpha while core provides stable beta
   
3. **Key distinguisher**: Alpha/beta separation divides by function (alpha vs. beta) across markets; core-satellite divides by size/role within a unified benchmark.

4. **Match description to strategy**: Look for keywords like "separate alpha from beta," "active in one market, passive in another" (alpha/beta separation) vs. "passive core with active positions," "satellites around core" (core-satellite).

**Example (sanitized):**
> **Scenario:** A manager proposes investing 60% in passive emerging market index fund and 40% in actively managed developed market long-short strategy seeking alpha independent of market direction.
> 
> **Wrong approach:** "This is core-satellite because there's a large passive position (60%) and an active position (40%)."
> 
> **Correct approach:** This is alpha/beta separation. The passive EM exposure provides beta, while the developed market long-short explicitly seeks alpha independent of beta. The strategy separates alpha generation (developed markets active) from beta exposure (EM passive) across different markets, which is the defining characteristic of alpha/beta separation.

---

## Pattern 4: multifactor_variance_decomposition

**Description:** In multi-factor models, the proportion of variance explained by a specific factor requires proper decomposition accounting for all factors and their covariances. Cannot simply use single-factor variance ratios when multiple factors are present.

**When to Use:** Questions asking for "proportion of risk explained," "R-squared," "variance contribution" in context of multi-factor models with multiple risk factors.

**Procedure:**
1. **Identify total portfolio variance**: σₚ² (may be given or need to calculate from factor model).

2. **For factor contribution to explained variance**:
   - Systematic variance from factor i: (βᵢ × σᵢ)² where βᵢ is factor loading and σᵢ is factor volatility
   - This is only correct for R² if it's a single-factor model
   
3. **For multi-factor R-squared**:
   - Total systematic variance = Σᵢ Σⱼ [βᵢ × βⱼ × Cov(Fᵢ, Fⱼ)]
   - If factors are uncorrelated: Systematic variance = Σᵢ (βᵢ × σᵢ)²
   - R² = Systematic variance / Total variance
   
4. **For specific factor contribution**:
   - Factor i contribution to R² = (βᵢ × σᵢ)² / σₚ²
   - This represents the proportion of total risk explained by factor i alone
   
5. **Residual variance**: (1 - R²) × σₚ² = idiosyncratic risk

**Example (sanitized):**
> **Scenario:** A portfolio has β_market = 1.2, β_size = 0.3. Market factor σ = 15%, size factor σ = 8%, factors uncorrelated. Portfolio total σ = 22%. What proportion of risk is explained by market factor?
> 
> **Wrong approach:** R² = (1.2 × 15%)² / (22%)² = 67.8% (this is total systematic R², not market-specific)
> 
> **Correct approach:** 
> - Market contribution to variance = (1.2 × 15%)² = 324 basis points²
> - Total variance = (22%)² = 484 basis points²
> - Market factor explains: 324/484 = 67.0% of total risk
> - Note: Total systematic = (1.2×15%)² + (0.3×8%)² = 329.76, R² = 68.1%
> - Market-specific contribution is 67.0%

---

## Pattern 5: tracking_error_aggregation_limitations

**Description:** Tracking errors across multiple managers cannot be aggregated using simple weighted variance formulas without correlation data. When managers track the same benchmark, their tracking errors may offset, making weighted-average approaches incorrect.

**When to Use:** Questions about "aggregate tracking error," "combined tracking error," "portfolio-level tracking error" when multiple managers are involved.

**Procedure:**
1. **Recognize the limitation**: Tracking error is a standard deviation measure. Aggregating standard deviations requires correlation information.

2. **Understand why simple weighting fails**:
   - Portfolio variance = Σᵢ Σⱼ [wᵢ × wⱼ × TE(i) × TE(j) × ρ(i,j)]
   - Without correlations ρ(i,j), cannot calculate aggregate tracking error
   - Weighted average of TEs assumes perfect correlation (ρ=1), which overstates aggregate TE
   
3. **Special cases**:
   - If managers track same benchmark: Likely positive but imperfect correlation, some offsetting
   - If managers track different benchmarks: Correlation structure unknown
   - If managers are independent: Lower aggregate TE than weighted average
   
4. **Correct approach when correlations unknown**:
   - State that aggregate TE cannot be precisely calculated without correlation data
   - Provide bounds: √(Σ wᵢ² × TEᵢ²) ≤ Aggregate TE ≤ Σ(wᵢ × TEᵢ)
   - Lower bound assumes zero correlation; upper bound assumes perfect correlation
   
5. **If asked to evaluate**: Compare available information (e.g., weighted average TE) to target, but note limitations.

**Example (sanitized):**
> **Scenario:** Portfolio has 50% with Manager A (TE = 4%) and 50% with Manager B (TE = 6%), both tracking same benchmark. Target aggregate TE is 4%. Does portfolio meet target?
> 
> **Wrong approach:** Aggregate TE = 0.5(4%) + 0.5(6%) = 5%, exceeds target of 4%.
> 
> **Correct approach:** Cannot calculate precise aggregate TE without correlation between managers. However:
> - Lower bound (zero correlation): √[0.5²(4%)² + 0.5²(6%)²] = 3.6%
> - Upper bound (perfect correlation): 0.5(4%) + 0.5(6%) = 5%
> - Since managers track same benchmark, correlation likely positive but <1
> - Aggregate TE likely between 3.6% and 5%
> - Cannot definitively conclude whether 4% target is met without correlation data
> - If forced to answer: Lower bound of 3.6% suggests target may be achievable

---

SKILL_MD_ENTRY: | `equity/risk_decomposition_concepts.md` | Equity | Risk Decomposition and Portfolio Strategy Concepts | statistical_measures_from_discrete_distributions, active_risk_and_correlation_effects, alpha_beta_separation_vs_core_satellite, multifactor_variance_decomposition, tracking_error_aggregation_limitations |