# Portfolio Management Concept Confusion: Detailed Skill Patterns

## Pattern: Efficient Frontier Identification

**Description:** A portfolio is on the efficient frontier if it offers the maximum Sharpe ratio among all feasible portfolios, or equivalently, has minimum variance for its return level with no other portfolio offering higher return at the same risk. Verification requires either solving for the tangency portfolio (maximum Sharpe ratio) or constructing the efficient frontier curve and checking if the candidate lies on it.

**When to Use:** Questions asking to identify portfolios on the efficient frontier, optimal portfolio selection, mean-variance optimization problems, or comparing multiple candidate portfolios for efficiency.

**Procedure:**
1. Calculate expected returns, standard deviations, and correlation/covariance matrix for all assets
2. For each candidate portfolio, compute return = Σ(w_i × E[R_i]) and variance = w'Σw
3. **Key decision point:** Choose verification method:
   - **Method A (Sharpe Ratio):** Calculate Sharpe ratio = (Return - Rf) / Std Dev for each candidate; highest Sharpe ratio identifies the tangency portfolio (efficient)
   - **Method B (Minimum Variance):** For each candidate's return level, solve optimization to find minimum variance portfolio; candidate is efficient if its variance equals the minimum
4. If multiple candidates have similar Sharpe ratios (within tolerance), verify by checking dominance: no other candidate has both higher return AND lower risk
5. Return the portfolio with maximum Sharpe ratio or the one that passes both minimum variance and non-dominance tests

**Example (sanitized):**

> **Scenario:** Three candidate portfolios with different allocations between two assets (Asset X and Asset Y). Asset X: E[R]=10%, σ=18%. Asset Y: E[R]=6%, σ=12%. Correlation=0.25. Risk-free rate=3%. Candidates: Portfolio 1 (30% X, 70% Y), Portfolio 2 (45% X, 55% Y), Portfolio 3 (60% X, 40% Y).
>
> **Wrong approach:** Calculate returns and standard deviations, then select the portfolio with highest return, or compare only adjacent portfolios for dominance without checking global optimality.
>
> **Correct approach:**
> 1. Calculate covariance matrix: Cov(X,Y) = 0.25 × 0.18 × 0.12 = 0.0054
> 2. For each candidate, calculate return and standard deviation:
>    - Portfolio 1: Return = 0.30×10% + 0.70×6% = 7.2%, Variance = 0.30²×0.18² + 0.70²×0.12² + 2×0.30×0.70×0.0054 = 0.01296, Std = 11.38%
>    - Portfolio 2: Return = 0.45×10% + 0.55×6% = 7.8%, Variance = 0.01485, Std = 12.19%
>    - Portfolio 3: Return = 0.60×10% + 0.40×6% = 8.4%, Variance = 0.01944, Std = 13.94%
> 3. Calculate Sharpe ratios:
>    - Portfolio 1: (7.2% - 3%) / 11.38% = 0.369
>    - Portfolio 2: (7.8% - 3%) / 12.19% = 0.394
>    - Portfolio 3: (8.4% - 3%) / 13.94% = 0.387
> 4. Portfolio 2 has the highest Sharpe ratio (0.394), making it the tangency portfolio and therefore on the efficient frontier
> 5. Verify: Portfolio 2 is not dominated by others (Portfolio 1 has lower return and lower risk, Portfolio 3 has higher return but much higher risk with lower Sharpe ratio)

**Common Mistakes to Avoid:**
- Comparing only subset of candidates without calculating Sharpe ratios for all options
- Selecting highest return portfolio without considering risk-adjusted performance
- Testing local optimality (minimum variance at return level) without verifying global efficiency via Sharpe ratio
- Forgetting that efficient frontier requires maximum Sharpe ratio, not just non-dominance among given options
- Not using the risk-free rate when Sharpe ratio is the appropriate criterion

---
## Pattern: After-Tax Rebalancing Range with Transaction Costs

**Description:** Capital gains taxes create asymmetric transaction costs that **widen the no-trade corridor** (making rebalancing less frequent), not the rebalancing range itself. The tax on embedded gains increases the cost of rebalancing, making it optimal to tolerate larger deviations before trading. **Critical clarification:** The "after-tax rebalancing range" refers to the wider corridor boundaries (further from target) where rebalancing is triggered, reflecting that taxes make it costlier to rebalance, so you wait longer before acting.

**When to Use:** Questions about rebalancing ranges, corridors, or bands when taxes on capital gains are present; portfolio maintenance with tax considerations; questions asking how taxes affect the optimal rebalancing trigger points.

**When NOT to Use:**
- When the question provides a pre-tax range and asks for after-tax range without volatility data (may require different approach)
- When the context suggests a simpler proportional adjustment rather than volatility-based formula
- When the question is about tax impact on returns rather than rebalancing thresholds

**Procedure:**
1. **Identify what the question is asking:**
   - If asking "how do taxes affect rebalancing frequency" → Taxes widen the no-trade corridor (less frequent rebalancing)
   - If given pre-tax range and asked for after-tax range → Determine if volatility-based formula applies
2. **For volatility-based calculation:**
   - Formula: After-tax corridor half-width = Pre-tax half-width × √(1 + 2τ/(1-τ))
   - Where τ is capital gains tax rate
   - This widens the corridor (boundaries move further from target)
3. **For simple proportional adjustment (when volatility not provided):**
   - Recognize that taxes increase transaction costs
   - After-tax corridor boundaries are further from target than pre-tax
   - The range itself may appear "wider" in absolute terms
4. Apply adjustment to both upper and lower bounds from the target
5. Verify: After-tax corridor should be wider (boundaries further from target) than pre-tax

**Example (sanitized):**

> **Scenario:** Pre-tax rebalancing corridor: rebalance when allocation deviates ±4% from 12% target (range 8%-16%). Capital gains tax 25%, asset volatility 15%.
>
> **Wrong approach:** Apply formula that narrows the range or multiplies by volatility incorrectly.
>
> **Correct approach:**
> 1. Pre-tax half-width = 4%
> 2. Tax adjustment factor = √(1 + 2×0.25/(1-0.25)) = √(1.667) = 1.291
> 3. After-tax half-width = 4% × 1.291 = 5.16%
> 4. After-tax corridor: 12% ± 5.16% = 6.84% to 17.16%
> 5. Interpretation: With taxes, you wait until allocation reaches 6.84% or 17.16% before rebalancing (wider corridor = less frequent rebalancing)

**Common Mistakes to Avoid:**
- Treating tax rate as a simple discount factor on allocation percentages
- Narrowing the corridor instead of widening it (taxes make rebalancing more costly, so corridor widens)
- Applying volatility incorrectly in the tax adjustment calculation
- Not recognizing that "wider corridor" means boundaries are further from target (less frequent rebalancing)
- Confusing the direction of the effect: taxes increase costs → wider no-trade zone → less frequent rebalancing

---
## Pattern: Futures Position Change with Contract Multiplier

**Description:** The dollar change in a futures position depends on the context: (1) For calculating hedge position changes, use hedge ratio = (Portfolio Beta × Portfolio Value) / (Index Level × Multiplier) to find number of contracts, then Position Change = Contracts × Point Change × Multiplier. (2) For calculating the change in an existing or unit futures position, use Position Change = Number of Contracts × Point Change × Multiplier directly without hedge ratio calculation. (3) For rebalancing strategies: When exchanging exposure between asset classes using futures, calculate contracts needed as (Dollar Exposure Change) / (Futures Price × Multiplier), adjusting for beta differences between the portfolio and futures contract.

**When to Use:** Questions about futures position changes, hedging calculations, rebalancing with futures, or determining dollar impact of index movements on futures contracts. **Critical:** Distinguish whether the question asks "how to hedge" (requires hedge ratio), "what is the change in THE futures position" (simple position valuation), or "rebalance exposure" (requires exposure-based calculation).

**When NOT to Use:**
- When beta adjustment requires dividing by futures beta (not multiplying) — see rebalancing context below
- When the question asks for total execution cost rather than futures position sizing

**Procedure:**
1. **Identify question type using these triggers:**
   - **Type A (Hedging):** "Calculate hedge position," "How many contracts needed to hedge," "Establish a hedge," "Protect portfolio using futures"
   - **Type B (Simple Position Change):** "By how much does THE futures position change," "Change in futures position value," "Dollar change for X-point drop" WITHOUT hedging context
   - **Type C (Rebalancing/Exposure Exchange):** "Rebalance exposure," "Exchange X dollars of exposure," "Adjust allocation using futures"
2. **For Type B (Simple Position Change) — DEFAULT to 1 contract:**
   - **Key decision:** If question asks about "the futures position" or "a futures position" without specifying portfolio hedging context, assume 1 contract
   - Position change = 1 × Point Change × Multiplier
   - Portfolio details (if provided) are background context, NOT inputs for hedge ratio
   - **Validation:** Result should be small (thousands, not hundreds of thousands)
3. **For Type A (Hedging):**
   - Calculate contracts = (Portfolio Beta × Portfolio Value) / (Index Level × Multiplier)
   - Position change = Contracts × Point Change × Multiplier
   - **Validation:** Result should be proportional to portfolio size
4. **For Type C (Rebalancing/Exposure Exchange):**
   - Calculate contracts = (Dollar Exposure to Exchange) / (Futures Price × Multiplier)
   - **Beta adjustment:** If portfolio beta differs from futures beta, adjust by dividing by the ratio: contracts = contracts_base × (Portfolio Beta / Futures Beta)
   - **Direction:** Reducing exposure = SELL contracts; Increasing exposure = BUY contracts
5. **CHECK:** Does the result magnitude match the question context? (Type B: small amounts; Type A: large amounts proportional to portfolio)

**Example (sanitized):**

> **Scenario B (Simple Position Change):** An index futures contract has a multiplier of 250. The index is currently at 1,500. For a 100-point drop in the index, by how much does the futures position change? (Background: A portfolio manager holds $5M in equities with beta 1.2.)
>
> **Wrong approach:** Calculate hedge ratio using portfolio details: Contracts = (1.2 × $5M) / (1,500 × 250) = 16 contracts. Position change = 16 × 100 × 250 = $400,000.
>
> **Correct approach:**
> 1. Question asks "by how much does THE futures position change" without asking "how many contracts to hedge"
> 2. This is Type B: simple position valuation, not hedging calculation
> 3. Portfolio details are background context only
> 4. Default to 1 contract: Position change = 1 × 100 × 250 = $25,000
> 5. Verification: Result ($25,000) is reasonable for a single contract; hedge calculation result ($400,000) would only be correct if question asked "how many contracts needed to hedge"
>
> **Scenario A (Hedging):** A portfolio manager wants to hedge a $5M equity portfolio (beta 1.2) using index futures. The index is at 1,500, multiplier 250. How many contracts are needed, and what is the position change for a 100-point drop?
>
> **Correct approach:**
> 1. Question explicitly asks "how many contracts needed to hedge"
> 2. This is Type A: hedge position calculation
> 3. Contracts = (1.2 × $5,000,000) / (1,500 × 250) = 16 contracts
> 4. Position change = 16 × 100 × 250 = $400,000
> 5. Verification: Hedge gain ($400,000) should offset portfolio loss (1.2 × $5M × 100/1,500 ≈ $400,000)

**Common Mistakes to Avoid:**
- Always applying hedge ratio formula when portfolio details are present, even for simple position change questions
- Not distinguishing "THE futures position" (likely 1 contract) from "hedge THE portfolio" (requires hedge ratio)
- Assuming portfolio details must be used in calculation rather than being background context
- Multiplying by futures beta instead of dividing when adjusting for beta differences in rebalancing
- Using wrong beta adjustment direction (multiply vs divide) for rebalancing scenarios

---
## Pattern: Diversification and Idiosyncratic Risk Elimination

**Description:** In a well-diversified portfolio with many assets, idiosyncratic (firm-specific) risk diversifies away to zero, leaving only systematic (market) risk. Portfolio variance approaches β² × Var(Market) as the number of assets increases.

**When to Use:** Questions about portfolio variance with infinite or large number of assets, systematic vs. unsystematic risk, or diversification benefits.

**Procedure:**
1. Formula: Var(R_portfolio) = β² × Var(R_market) for well-diversified portfolio
2. Identify asset beta and market variance
3. Recognize that idiosyncratic variance (Var(ε)) disappears with diversification
4. Calculate only the systematic risk component
5. Do not add the asset-specific variance term

**Code Example:**

**Scenario:** Asset with beta 1.3, market variance 0.0144, idiosyncratic variance 0.0200. Calculate variance of portfolio with infinite number of this asset type.

**Correct Code:**
```python
# Asset and market parameters
asset_beta = 1.3
market_variance = 0.0144
idiosyncratic_variance = 0.0200  # This diversifies away

# For a well-diversified portfolio (infinite assets of this type)
# Only systematic risk remains
# Var(R_portfolio) = beta^2 × Var(R_market)
portfolio_variance = asset_beta**2 * market_variance

# Idiosyncratic variance is NOT included because it diversifies to zero
# Individual asset variance would be: beta^2 × market_var + idiosyncratic_var
# But portfolio variance eliminates the idiosyncratic component

portfolio_variance
```

**Common Bugs to Avoid:**
- Including idiosyncratic variance in diversified portfolio calculations
- Confusing individual asset variance with portfolio variance
- Not recognizing that "infinite number of assets" implies full diversification
- Adding Var(ε) when it should be eliminated through diversification

---

## Pattern: Systematic Risk as Variance Component

**Description:** Systematic risk has two distinct meanings depending on context: (1) In variance decomposition, it refers to Var(R_systematic) = Σ(β_i² × Var(Factor_i)) + covariance terms, representing the volatility from factor exposures. (2) In return attribution with realized factor surprises, it refers to the unexpected return from factors = Σ(β_i × Factor_Surprise_i), NOT variance. **Critical:** Distinguish whether the question asks for "risk" (variance/volatility) or "return contribution" (attribution), regardless of whether factor surprises are provided.

**When to Use:** Questions asking for systematic risk, factor-based risk decomposition, variance attribution, or unexpected returns from factor models. **Key trigger:** The question's REQUEST determines the calculation: "risk," "variance," or "volatility" → variance calculation; "return," "contribution," or "attribution" → return calculation.

**Procedure:**
1. **Identify what the question ASKS FOR (not just what data is provided):**
   - **Request Type A (Risk/Variance):** "systematic risk," "systematic variance," "systematic volatility," "risk from factors"
   - **Request Type B (Return Attribution):** "systematic return," "return contribution," "unexpected return from factors," "factor attribution"
2. **For Type A (Risk/Variance) — even if factor surprises are provided:**
   - **If factor volatilities/variances given:** Use Var(R_sys) = Σ(β_i² × Var(Factor_i)) + covariance terms
   - **If only factor surprises given:** CANNOT calculate variance from single observation; may need to request volatility data or use alternative approach
   - Take square root if standard deviation requested
   - **Validation:** Result should be a percentage (e.g., 15% volatility), not a return value
3. **For Type B (Return Attribution):**
   - Formula: Unexpected Systematic Return = Σ(β_i × [Actual_i - Expected_i])
   - Calculate surprise for each factor = Actual - Expected
   - Multiply each surprise by its beta
   - Sum all contributions (this is a return, not variance)
   - **Validation:** Result should be a return percentage (e.g., 2.5% return), not a volatility measure
4. **CHECK:** Does the question ask for "risk" or "return"? If "risk" but only surprises provided, recognize data limitation

**Example (sanitized):**

> **Scenario A (Risk with Surprises Provided):** A two-factor model has β₁=1.2, β₂=0.8. Last period, Factor 1 had expected return 3% but actual 4.5%; Factor 2 had expected 2% but actual 1.5%. What is the systematic risk of the stock return?
>
> **Wrong approach:** Calculate unexpected return = 1.2 × (4.5% - 3%) + 0.8 × (1.5% - 2%) = 1.8% - 0.4% = 1.4%, and report this as "systematic risk."
>
> **Correct approach:**
> 1. Question asks for "systematic RISK" (variance/volatility concept)
> 2. Only factor surprises provided (single period observations)
> 3. Cannot calculate variance from single observation
> 4. Need factor volatilities (σ₁, σ₂) to calculate systematic variance = β₁² × σ₁² + β₂² × σ₂² + 2×β₁×β₂×Cov(F₁,F₂)
> 5. The 1.4% calculated above is the unexpected systematic RETURN, not risk
> 6. Correct answer requires additional data or clarification
>
> **Scenario B (Return Attribution):** Same setup as above. What is the systematic contribution to unexpected return?
>
> **Correct approach:**
> 1. Question asks for "contribution to unexpected RETURN" (attribution concept)
> 2. Factor surprises: F₁ = 4.5% - 3% = 1.5%, F₂ = 1.5% - 2% = -0.5%
> 3. Unexpected systematic return = 1.2 × 1.5% + 0.8 × (-0.5%) = 1.8% - 0.4% = 1.4%
> 4. This is a return contribution, not a variance
> 5. Verification: Result is a return percentage, appropriate for attribution question

**Common Mistakes to Avoid:**
- Treating factor surprises as if they represent long-term volatility (cannot estimate variance from one observation)
- Using return attribution formula when question explicitly asks for "risk" or "variance"
- Confusing unexpected return (linear in surprises) with systematic variance (quadratic in volatilities)
- Not recognizing that "actual vs. expected" data can be used for return attribution but NOT for variance calculation without additional volatility data
- Reporting a return percentage as if it were a risk/volatility measure

---
## Pattern: Effective Spread Calculation with Quoted Midpoint

**Description:** Effective spread measures execution cost relative to the quoted midpoint (average of best bid and best ask) at the time of each trade. For buy orders: 2 × (execution price - midpoint); for sell orders: 2 × (midpoint - execution price).

**When to Use:** Questions about trading costs, effective spreads, implementation shortfall components, or transaction cost analysis.

**Procedure:**
1. Formula: Effective Spread (buy) = 2 × (Execution Price - Quoted Midpoint)
2. For each trade, identify execution price, best bid, and best ask at trade time
3. Calculate quoted midpoint = (Best Bid + Best Ask) / 2
4. Calculate effective spread for each trade using formula
5. Compute share-volume-weighted average: Σ(shares_i × spread_i) / Σ(shares_i)

**Code Example:**

**Scenario:** Buy 3,000 shares: Trade 1: 2,000 shares at $50.10 (bid $50.00, ask $50.12); Trade 2: 1,000 shares at $50.15 (bid $50.05, ask $50.18).

**Correct Code:**
```python
# Trade execution details
trades = [
    {'shares': 2000, 'exec_price': 50.10, 'bid': 50.00, 'ask': 50.12},
    {'shares': 1000, 'exec_price': 50.15, 'bid': 50.05, 'ask': 50.18}
]

# Calculate effective spread for each trade
effective_spreads = []
for trade in trades:
    # Quoted midpoint at time of trade
    midpoint = (trade['bid'] + trade['ask']) / 2
    
    # Effective spread for buy order: 2 × (execution - midpoint)
    spread = 2 * (trade['exec_price'] - midpoint)
    
    effective_spreads.append({
        'shares': trade['shares'],
        'spread': spread
    })

# Calculate share-volume-weighted effective spread
total_shares = sum(t['shares'] for t in effective_spreads)
weighted_spread = sum(t['shares'] * t['spread'] for t in effective_spreads) / total_shares

round(weighted_spread, 2)
```

**Common Bugs to Avoid:**
- Using arbitrary bid-ask pairs instead of best bid/ask at trade time
- Forgetting the factor of 2 in effective spread formula
- Not weighting by share volume when averaging multiple trades
- Calculating spread as simple (execution - midpoint) without doubling

---

## Pattern: Capital Allocation Line and Complete Portfolio

**Description:** A client's complete portfolio includes both the risky portfolio and risk-free asset (T-bills). Determining the allocation requires either client risk preferences (risk aversion, target return, or target volatility) or solving for the optimal weight using utility maximization.

**When to Use:** Questions about overall portfolio composition, capital allocation decisions, or determining weights in risky vs. risk-free assets.

**Procedure:**
1. Formula: y = (E[R_p] - R_f) / (A × σ_p²) where y is weight in risky portfolio, A is risk aversion
2. Identify risky portfolio return, std dev, and risk-free rate
3. Determine client's constraint (target return, target std dev, or risk aversion parameter)
4. Solve for y (weight in risky portfolio): if target return given, y = (Target - R_f) / (E[R_p] - R_f)
5. Calculate individual asset weights = y × (weight in risky portfolio)

**Code Example:**

**Scenario:** Risky portfolio: 30% Stock A, 70% Stock B, E[R]=14%, σ=20%. T-bills: 4%. Client wants 11% return.

**Correct Code:**
```python
# Portfolio parameters
risky_return = 0.14
risky_std = 0.20
rf_rate = 0.04
stock_a_weight_in_risky = 0.30
stock_b_weight_in_risky = 0.70

# Client target return
target_return = 0.11

# Calculate weight in risky portfolio (y)
# Target return = y × E[R_risky] + (1-y) × R_f
# Solving for y: y = (Target - R_f) / (E[R_risky] - R_f)
weight_risky = (target_return - rf_rate) / (risky_return - rf_rate)
weight_tbills = 1 - weight_risky

# Calculate weights in individual assets
weight_stock_a = weight_risky * stock_a_weight_in_risky
weight_stock_b = weight_risky * stock_b_weight_in_risky

# Complete portfolio composition
complete_portfolio = {
    'T-bills': round(weight_tbills * 100, 1),
    'Stock A': round(weight_stock_a * 100, 1),
    'Stock B': round(weight_stock_b * 100, 1)
}

complete_portfolio
```

**Common Bugs to Avoid:**
- Assuming client invests 100% in risky portfolio without checking constraints
- Not recognizing this as a capital allocation problem requiring y calculation
- Forgetting to scale risky asset weights by y
- Missing that "overall portfolio" includes both risky and risk-free components

---

## Pattern: Confidence Index as Yield Ratio

**Description:** The Confidence Index is defined as the ratio of high-grade bond yields to lower-grade bond yields. It rises when the ratio increases (spread narrows), indicating increased confidence; it falls when the ratio decreases (spread widens). **Critical interpretation:** A falling confidence index (decreasing ratio) means widening credit spreads, which indicates DECREASED investor confidence and increased risk aversion, NOT increased confidence.

**When to Use:** Questions about confidence index, credit spread analysis, or bond market sentiment indicators.

**When NOT to Use:**
- When the question asks only about spread direction without requiring confidence index calculation
- When interpreting spread changes in isolation without the ratio framework

**Procedure:**
1. Formula: Confidence Index = (High-grade yield) / (Lower-grade yield)
2. Calculate confidence index for current period and prior period
3. Compare the two ratios to determine direction
4. **Critical interpretation step:** 
   - Rising index (higher ratio) = narrowing spread = INCREASED confidence
   - Falling index (lower ratio) = widening spread = DECREASED confidence
5. **Verify interpretation consistency:** Widening spreads always mean decreased confidence; narrowing spreads always mean increased confidence

**Code Example:**

**Scenario:** Last year: AAA yield 5%, BBB yield 7%. This year: AAA yield 4.5%, BBB yield 7.5%.

**Correct Code:**
```python
# Yield data
high_grade_yield_last_year = 0.05
low_grade_yield_last_year = 0.07
high_grade_yield_this_year = 0.045
low_grade_yield_this_year = 0.075

# Calculate confidence index for each period
confidence_index_last_year = high_grade_yield_last_year / low_grade_yield_last_year
confidence_index_this_year = high_grade_yield_this_year / low_grade_yield_this_year

# Determine direction
index_change = confidence_index_this_year - confidence_index_last_year
is_rising = index_change > 0

# Calculate credit spread for context
spread_last_year = low_grade_yield_last_year - high_grade_yield_last_year
spread_this_year = low_grade_yield_this_year - high_grade_yield_this_year

# CRITICAL: Ensure interpretation is consistent
# Falling index = widening spread = DECREASED confidence
# Rising index = narrowing spread = INCREASED confidence
direction = 'RISING' if is_rising else 'FALLING'
confidence_interpretation = 'INCREASED' if is_rising else 'DECREASED'
spread_trend = 'narrowing' if is_rising else 'widening'

result = {
    'confidence_index_last_year': round(confidence_index_last_year, 4),
    'confidence_index_this_year': round(confidence_index_this_year, 4),
    'direction': direction,
    'spread_change': round((spread_this_year - spread_last_year) * 100, 2),
    'interpretation': f"Confidence index is {direction}. The credit spread is {spread_trend} (from {spread_last_year*100:.1f}% to {spread_this_year*100:.1f}%), indicating {confidence_interpretation} investor confidence in credit quality."
}

result
```

**Common Mistakes to Avoid:**
- Using spread change instead of yield ratio
- Inverting the ratio (low-grade / high-grade)
- **CRITICAL ERROR:** Stating that widening spreads indicate increased confidence (the opposite is true)
- Confusing the mathematical direction (falling index) with the economic interpretation (decreased confidence)
- Not verifying that spread direction and confidence interpretation are consistent

---
## Pattern: Deduction Method for Foreign Tax

**Description:** Under the deduction method, foreign taxes paid are deducted from taxable income (reducing the tax base), not credited against tax liability. Effective rate = Domestic rate + Foreign rate - (Domestic rate × Foreign rate).

**When to Use:** Questions about international taxation, foreign tax treatment, deduction vs. credit methods, or cross-border investment taxation.

**Procedure:**
1. Formula: Effective Tax Rate = r_d + r_f - (r_d × r_f) where r_d is domestic rate, r_f is foreign rate
2. Identify domestic tax rate and foreign tax rate
3. Calculate combined effect: both taxes apply, but foreign tax reduces domestic tax base
4. Apply formula to get effective rate
5. Verify: effective rate should be higher than either individual rate but less than their sum

**Code Example:**

**Scenario:** Domestic tax 12%, foreign tax 18%. Calculate effective tax rate under deduction method.

**Correct Code:**
```python
# Tax rates
domestic_tax_rate = 0.12
foreign_tax_rate = 0.18

# Under deduction method:
# Foreign tax is deducted from income before calculating domestic tax
# Tax = Foreign_tax + Domestic_tax_on_remaining_income
# Tax = Income × r_f + (Income - Income × r_f) × r_d
# Tax = Income × [r_f + r_d - (r_f × r_d)]

effective_tax_rate = (domestic_tax_rate + foreign_tax_rate - 
                      (domestic_tax_rate * foreign_tax_rate))

# Convert to percentage
effective_rate_percentage = round(effective_tax_rate * 100, 1)

effective_rate_percentage
```

**Common Bugs to Avoid:**
- Treating deduction method as credit method (subtracting foreign tax from liability)
- Taking the maximum of the two rates instead of calculating combined effect
- Simply adding the two rates without adjustment
- Not recognizing that foreign tax reduces the base for domestic tax

---

## Pattern: Delta-Hedged Portfolio Insurance

**Description:** Portfolio insurance using delta-hedging requires maintaining a dynamic allocation between risky assets and risk-free securities that replicates a protective put. The initial allocation is determined by the put option's delta: invest (1 + put_delta) in risky assets and (-put_delta) in risk-free, where put_delta is negative. Equivalently, for a $1 portfolio, invest |put_delta| in risk-free and (1 - |put_delta|) in risky assets. For futures-based insurance, the number of short contracts = (Portfolio value / Futures price) × |Put Delta|, where **Futures price should be calculated without assuming a standard contract multiplier unless explicitly provided**.

**When to Use:** Questions about portfolio insurance with options or futures, dynamic hedging strategies, replicating protective puts, or determining initial allocations for insured portfolios. **Key trigger:** Phrases like "provide insurance by keeping part in risk-free securities" or "replicate protective put through dynamic allocation."

**When NOT to Use:**
- When the question asks for static hedge ratios without option Greeks
- When futures contract specifications (multiplier, contract size) are not provided or cannot be inferred

**Procedure:**
1. Calculate put option delta using Black-Scholes framework:
   - d₁ = [ln(S/K) + (r - q + σ²/2)T] / (σ√T)
   - N(d₁) = cumulative normal distribution of d₁
   - Put Delta = e^(-qT) × [N(d₁) - 1] (negative value between -1 and 0)
2. **For initial allocation percentages:**
   - Risk-free allocation = |Put Delta| × 100%
   - Risky allocation = (1 - |Put Delta|) × 100%
   - Verify: allocations sum to 100%
3. **For futures contracts (alternative implementation):**
   - **Calculate futures price:** F = S × e^((r-q)T) where T is the futures maturity
   - **DO NOT assume a standard multiplier** unless explicitly stated in the problem
   - **Number of contracts calculation depends on contract specification:**
     - If contract multiplier is given: contracts = (Portfolio value / (Futures price × Multiplier)) × |Put Delta|
     - If contract is based on index level: contracts = (Portfolio value / Futures price) × |Put Delta|
   - **Verification:** Check if the result makes sense relative to portfolio size and index level
4. **Validation:** Initial risky allocation should be less than 100% (insurance requires some risk-free position); as protection level increases (higher strike), |put delta| increases, reducing risky allocation

**Example (sanitized):**

> **Scenario:** Portfolio $10M, index at 1200, protect against 10% loss over 6 months. Risk-free rate 4%, dividend yield 2%, volatility 20%. Calculate initial allocation percentages.
>
> **Wrong approach:** Calculate put premium and allocate (Portfolio - Premium) to risky assets, or use hedge ratio without calculating put delta.
>
> **Correct approach:**
> 1. Strike = 1200 × (1 - 0.10) = 1080
> 2. d₁ = [ln(1200/1080) + (0.04 - 0.02 + 0.20²/2) × 0.5] / (0.20 × √0.5)
>    = [0.1054 + 0.02] / 0.1414 = 0.886
> 3. N(d₁) = 0.8123
> 4. Put delta = e^(-0.02×0.5) × (0.8123 - 1) = 0.990 × (-0.1877) = -0.186
> 5. Risk-free allocation = |-0.186| = 18.6%
> 6. Risky allocation = 1 - 0.186 = 81.4%
> 7. Initial portfolio: 81.4% in index, 18.6% in T-bills
>
> **For futures-based implementation (9-month futures):**
> 1. Calculate put delta as above: -0.186
> 2. Futures price (9 months): F = 1200 × e^((0.04-0.02)×0.75) = 1218.1
> 3. **Without explicit multiplier:** contracts = (10,000,000 / 1218.1) × 0.186 ≈ 1,527 contracts
> 4. **With multiplier (e.g., 250):** contracts = (10,000,000 / (1218.1 × 250)) × 0.186 ≈ 6.1 contracts
> 5. Verify which interpretation matches the problem context

**Common Mistakes to Avoid:**
- Calculating put premium and subtracting from portfolio value instead of using delta
- Using call delta or confusing put delta sign conventions
- Not recognizing that delta-hedging requires Black-Scholes option Greeks
- Applying static hedge ratios instead of dynamic delta-based allocation
- Forgetting to take absolute value of put delta when calculating risk-free allocation percentage
- **CRITICAL:** Assuming a standard futures contract multiplier (e.g., 250) when it's not explicitly provided in the problem
- Not calculating the futures price correctly using the cost-of-carry formula F = S × e^((r-q)T)
- Using the wrong time horizon for futures price calculation (should match futures maturity, not insurance period)

---
## Pattern: Arrival Cost Benchmark

**Description:** Arrival cost (also called decision price benchmark) measures execution performance relative to the market price at the time the trading decision was made, capturing all market movement and execution costs from decision to completion. **Critical distinction:** In implementation shortfall analysis, "trading cost" or "execution cost" specifically refers to the cost from order RELEASE (arrival price) to execution, NOT from initial decision. The benchmark depends on which component is being measured: decision cost uses decision price; trading/execution cost uses release/arrival price. **For total execution cost questions:** When the question asks "what is the execution cost for purchasing X shares" with answer options in large dollar amounts, this is asking for total dollars paid (price × shares + commissions), NOT a performance metric in basis points.

**When to Use:** Questions about trade execution analysis, implementation shortfall components, or performance measurement. **Key trigger:** Identify which implementation shortfall component is requested: (1) Decision cost = delay cost from decision to release, (2) Trading/Execution cost = market impact from release to execution, (3) Total implementation shortfall = decision to execution, (4) Total execution cost = total dollars paid.

**When NOT to Use:** 
- When the question asks for "execution cost" with answer options in millions of dollars (this is total dollar cost, not arrival cost)
- When calculating total transaction costs including commissions as a dollar amount
- When the question explicitly asks to include commissions in the cost metric

**Procedure:**
1. **Identify which cost metric is requested using answer options:**
   - **Large dollar amounts (millions):** Total execution cost = Σ(execution_price × shares) + total_commissions
   - **Small percentages or basis points:** Arrival cost or implementation shortfall component
   - **Key decision:** Check answer option magnitudes FIRST to determine metric type
2. **For total execution cost (dollar amounts):**
   - Calculate: Σ(execution_price × shares) + total_commissions
   - Express in dollars
   - DO NOT calculate basis points or use benchmark prices
3. **For arrival cost/implementation shortfall (basis points):**
   - **Decision cost (delay cost):** Benchmark = Decision price (when order was decided)
   - **Trading/Execution cost (market impact):** Benchmark = Release/Arrival price (when order entered market)
   - **Total implementation shortfall:** Benchmark = Decision price
   - Calculate average execution price (volume-weighted across all fills)
   - Cost = [(Avg Execution Price - Benchmark Price) / Benchmark Price] × 10,000
   - Express result in basis points
   - **Do NOT add commissions** — arrival cost measures price impact only
4. **Validation:** Check if the result magnitude matches the answer options

**Example (sanitized):**

> **Scenario:** Bought 50,000 shares across 3 trades: 20,000 at $30.10, 15,000 at $30.25, 15,000 at $30.40. Commission $0.02/share. Decision price $30.00.
>
> **Question A:** "What is the execution cost for purchasing the 50,000 shares?"
> **Options:** A. $1,500,000  B. $1,512,500  C. $1,525,000
> **Interpretation:** Large dollar amounts → Total execution cost requested
> **Correct approach:**
> 1. Answer options are in millions → this is total dollar cost
> 2. Total cost = (20,000×$30.10 + 15,000×$30.25 + 15,000×$30.40) + (50,000×$0.02)
> 3. = $1,511,500 ≈ Option B
> 4. Do NOT calculate basis points or use benchmark prices
>
> **Question B:** "What is the arrival cost for purchasing the 50,000 shares?"
> **Options:** A. 65 bp  B. 78 bp  C. 91 bp
> **Interpretation:** Basis points → Performance metric requested
> **Correct approach:**
> 1. Answer options are in basis points → this is arrival cost metric
> 2. Avg price = (20,000×$30.10 + 15,000×$30.25 + 15,000×$30.40)/50,000 = $30.23
> 3. Arrival cost = ($30.23 - $30.00)/$30.00 × 10,000 = 77 bp ≈ Option B
> 4. Do NOT include commissions in this calculation

**Common Mistakes to Avoid:**
- Using decision price as benchmark when calculating "trading cost" or "execution cost" in implementation shortfall context
- Not distinguishing between decision cost (decision→release) and trading cost (release→execution)
- Adding commissions to execution price when calculating arrival cost or implementation shortfall components
- Confusing "trading cost" (price impact component) with "total execution cost" (includes commissions)
- **CRITICAL:** Not checking answer option magnitudes to determine whether the question asks for total dollar cost or a performance metric in basis points
- Calculating basis points when the question asks for total dollars paid

---
## Pattern: Bond-Yield-Plus-Risk-Premium Method for Equity Returns

**Description:** The bond-yield-plus-risk-premium method estimates equity expected return by adding an equity risk premium to a bond yield. **Critical distinction:** (1) For company-specific estimates, add the equity premium over debt (typically 3-5%) to the company's own bond yield. (2) For industry or market-level estimates, add the market equity risk premium (typically 5-8%) to the risk-free rate (Treasury yield), NOT to corporate bond yields. The method's base rate depends on the scope of the estimate.

**When to Use:** Questions asking to calculate expected equity returns using the bond-yield-plus-risk-premium method, cost of equity estimation. **Key trigger:** Identify the SCOPE of the estimate (company-specific vs. industry/market-level) to determine which base rate and premium to use.

**Procedure:**
1. **Identify the scope of the estimate:**
   - **Scope A (Company-specific):** Question asks for a specific company's equity return AND company's bond yield is provided
   - **Scope B (Industry/Market-level):** Question asks for industry or market equity return, OR only risk-free rate and market equity risk premium are provided
2. **For Scope A (Company-specific):**
   - Base rate = Company's own bond yield
   - Premium = Equity premium over debt (typically 3-5%, may be given or historical average)
   - Formula: Expected Equity Return = Company's Bond Yield + Equity Premium over Debt
   - **Validation:** Result should exceed company's bond yield by 3-5%
3. **For Scope B (Industry/Market-level):**
   - Base rate = Risk-free rate (Treasury yield)
   - Premium = Market equity risk premium (typically 5-8%, may be given or historical average)
   - Formula: Expected Equity Return = Risk-Free Rate + Market Equity Risk Premium
   - **DO NOT use corporate bond yields** for industry/market estimates
   - **Validation:** This is equivalent to CAPM with beta=1
4. **CHECK:** Does the base rate match the scope? Company bonds → company estimate; Treasury rate → industry/market estimate

**Example (sanitized):**

> **Scenario A (Company-specific):** ABC Manufacturing's bonds yield 7.2%. Historical data shows equity returns for manufacturing companies exceed their bond yields by an average of 4.5%. Calculate ABC's expected equity return.
>
> **Correct approach:**
> 1. Scope: Company-specific (ABC's own bonds provided)
> 2. Base rate = ABC's bond yield = 7.2%
> 3. Premium = Equity premium over debt = 4.5%
> 4. Expected equity return = 7.2% + 4.5% = 11.7%
> 5. Verification: Result exceeds bond yield by the typical 3-5% range
>
> **Scenario B (Industry-level):** An analyst is estimating expected return for the technology industry. Risk-free rate is 3.2%, market equity risk premium is 8.1%. Corporate bond yields for tech companies average 5.5%. Calculate expected equity return using bond-yield-plus-risk-premium approach.
>
> **Wrong approach:** Use corporate bond yield as base: 5.5% + 8.1% = 13.6% (double-counting risk by using corporate bonds with market equity risk premium).
>
> **Correct approach:**
> 1. Scope: Industry-level (not company-specific)
> 2. Base rate = Risk-free rate = 3.2% (NOT corporate bond yield)
> 3. Premium = Market equity risk premium = 8.1%
> 4. Expected equity return = 3.2% + 8.1% = 11.3%
> 5. Ignore corporate bond yields (5.5%) — not appropriate for industry-level estimates
> 6. Verification: This is equivalent to CAPM with beta=1 for market/industry estimates

**Common Mistakes to Avoid:**
- Using company bond yield + market equity risk premium (double-counting risk)
- Using risk-free rate + equity premium over debt (wrong base for the premium type)
- Using corporate bond yields for industry/market-level estimates (should use risk-free rate)
- Not recognizing that industry-level estimates require risk-free rate as base
- Confusing the equity premium over debt (3-5%, for company bonds) with market equity risk premium (5-8%, for risk-free rate)
## Pattern: Total Execution Cost vs. Arrival Cost Distinction

**Description:** "Execution cost" has different meanings depending on context: (1) **Total execution cost** = total dollars paid for the trade (price × shares + commissions), used when asking "how much did the trade cost?" (2) **Arrival cost** = basis points measuring price impact relative to decision price, excluding commissions. The question's phrasing and answer options indicate which metric is requested.

**When to Use:** Questions asking about "execution cost" where you must determine whether they want total dollar cost or a performance metric in basis points.

**Procedure:**
1. **Identify the metric requested:**
   - If answer options are large dollar amounts (millions) → Total execution cost (price × shares + commissions)
   - If answer options are small percentages or basis points → Arrival cost or implementation shortfall component
   - If question says "cost of purchasing" or "total cost" → Total dollar cost
   - If question says "arrival cost" or "execution performance" → Basis points metric
2. **For total execution cost:**
   - Calculate: Σ(execution_price × shares) + total_commissions
   - Express in dollars
3. **For arrival cost (performance metric):**
   - Calculate: [(Avg execution price - Decision price) / Decision price] × 10,000
   - Do NOT include commissions
   - Express in basis points
4. **Validation:** Check if your answer magnitude matches the options provided

**Example (sanitized):**

> **Scenario:** Bought 50,000 shares across 3 trades: 20,000 at $30.10, 15,000 at $30.25, 15,000 at $30.40. Commission $0.02/share. Decision price $30.00.
>
> **Question A:** "What is the execution cost for purchasing the 50,000 shares?"
> **Options:** A. $1,500,000  B. $1,512,500  C. $1,525,000
> **Interpretation:** Large dollar amounts → Total execution cost requested
> **Answer:** (20,000×$30.10 + 15,000×$30.25 + 15,000×$30.40) + (50,000×$0.02) = $1,511,500 ≈ Option B
>
> **Question B:** "What is the arrival cost for purchasing the 50,000 shares?"
> **Options:** A. 65 bp  B. 78 bp  C. 91 bp
> **Interpretation:** Basis points → Performance metric requested
> **Answer:** Avg price = $30.23, Arrival cost = ($30.23 - $30.00)/$30.00 × 10,000 = 77 bp ≈ Option B

**Common Mistakes to Avoid:**
- Assuming "execution cost" always means arrival cost in basis points
- Including commissions in arrival cost calculations (they're separate metrics)
- Not checking answer option magnitudes to determine which metric is requested
- Confusing total dollar cost with performance metrics

## Pattern: ICAPM Beta Calculation from Sharpe Ratio

**Description:** When calculating beta for the International Capital Asset Pricing Model (ICAPM), the standard deviation of the global investable market (GIM) must be derived from the Sharpe ratio if not directly provided. The formula is: σ_GIM = (E[R_GIM] - R_f) / Sharpe_GIM. Once the GIM standard deviation is known, beta can be calculated as: β = (ρ × σ_asset) / σ_GIM, where ρ is the correlation between the asset and GIM.

**When to Use:** Questions asking to calculate beta for ICAPM when the GIM Sharpe ratio is provided but the GIM standard deviation is not directly given. Common in international portfolio management and asset allocation contexts.

**When NOT to Use:**
- When GIM standard deviation is directly provided
- When covariance values are given (use β = Cov(asset, GIM) / Var(GIM) instead)
- When using factor models rather than single-index ICAPM

**Procedure:**
1. **Identify the given data:**
   - Asset standard deviation (σ_asset)
   - Correlation with GIM (ρ)
   - GIM Sharpe ratio
   - Risk-free rate (R_f)
   - Expected return on GIM (E[R_GIM])
2. **Calculate GIM standard deviation:**
   - GIM risk premium = E[R_GIM] - R_f
   - σ_GIM = GIM risk premium / Sharpe_GIM
   - **Verify:** σ_GIM should be a reasonable percentage (typically 10-20% for global markets)
3. **Calculate beta:**
   - β = (ρ × σ_asset) / σ_GIM
   - **Verify:** Beta should be positive for assets correlated with the market
4. **Common check:** If a covariance value is provided in the data, it likely represents something else (e.g., covariance between specific assets), not the GIM variance

**Example (sanitized):**

> **Scenario:** Calculate beta for emerging market equities. Data: EM equity std dev = 22%, correlation with GIM = 0.65, GIM Sharpe ratio = 0.40, risk-free rate = 2.5%, GIM expected return = 8.5%. Also provided: covariance with developed markets = 0.0085.
>
> **Wrong approach:** Use the covariance value (0.0085) as GIM standard deviation: β = (0.65 × 0.22) / 0.0085 = 16.8 (unrealistic).
>
> **Correct approach:**
> 1. Calculate GIM risk premium: 8.5% - 2.5% = 6.0%
> 2. Calculate GIM std dev: σ_GIM = 6.0% / 0.40 = 15.0%
> 3. Calculate beta: β = (0.65 × 0.22) / 0.15 = 0.95
> 4. Verify: Beta of 0.95 is reasonable (EM equities slightly less volatile than global market)
> 5. Note: The covariance value (0.0085) is for a different relationship, not GIM variance

**Common Mistakes to Avoid:**
- Using covariance values as standard deviations without checking units
- Forgetting to calculate GIM standard deviation from Sharpe ratio
- Confusing correlation with beta
- Not verifying that calculated standard deviations are in reasonable ranges (percentages, not decimals representing covariances)
- Using the wrong formula when Sharpe ratio is the key input

---

## Pattern: Arbitrage Detection with Portfolio Replication

**Description:** In a one-factor economy with well-diversified portfolios, arbitrage opportunities exist when a portfolio's actual return differs from its Security Market Line (SML) required return. The arbitrage strategy involves creating a replicating portfolio with the same beta using available portfolios, then exploiting the price difference. **Critical:** The direction of the arbitrage depends on whether the portfolio is overpriced (actual return < SML return → SHORT the portfolio) or underpriced (actual return > SML return → LONG the portfolio). The replicating portfolio must have identical beta to isolate the mispricing.

**When to Use:** Questions about arbitrage opportunities in factor models, CAPM violations, or portfolio mispricing when multiple portfolios with different betas are available.

**When NOT to Use:**
- When markets are not well-diversified (idiosyncratic risk matters)
- When transaction costs or constraints prevent arbitrage
- When only one risky portfolio is available (cannot construct replicating portfolio)

**Procedure:**
1. **Establish the Security Market Line (SML):**
   - Identify risk-free rate (R_f) from zero-beta portfolio
   - Calculate market risk premium: (E[R_market] - R_f) / β_market
   - SML formula: E[R] = R_f + β × market_risk_premium
2. **Calculate SML-required return for the candidate portfolio:**
   - E[R_SML] = R_f + β_candidate × market_risk_premium
3. **Compare actual return to SML-required return:**
   - Alpha = Actual return - SML return
   - If alpha ≠ 0, arbitrage opportunity exists
4. **Determine arbitrage direction:**
   - If alpha > 0 (actual > SML): Portfolio is OVERPRICED → SHORT it
   - If alpha < 0 (actual < SML): Portfolio is UNDERPRICED → LONG it
   - **Critical check:** Verify the sign interpretation matches economic logic
5. **Construct replicating portfolio:**
   - Find weights w_A and w_F such that: w_A × β_A + w_F × β_F = β_candidate
   - With risk-free asset (β_F = 0): w_A = β_candidate / β_A
   - Calculate replicating portfolio return: w_A × R_A + w_F × R_F
6. **Execute arbitrage:**
   - If portfolio is overpriced: SHORT candidate, LONG replicating portfolio
   - If portfolio is underpriced: LONG candidate, SHORT replicating portfolio
   - Profit = |Actual return - Replicating return| per unit invested

**Example (sanitized):**

> **Scenario:** One-factor economy. Portfolio A: E[R]=12%, β=1.2. Portfolio F (risk-free): E[R]=6%, β=0. Portfolio E: E[R]=8%, β=0.6. Does arbitrage exist?
>
> **Wrong approach:** Calculate that E is underpriced (8% < 9% SML), then state "SHORT E and LONG replicating portfolio" (backwards direction).
>
> **Correct approach:**
> 1. Risk-free rate = 6%
> 2. Market risk premium = (12% - 6%) / 1.2 = 5%
> 3. SML required return for E: 6% + 0.6 × 5% = 9%
> 4. Actual return for E: 8%
> 5. Alpha = 8% - 9% = -1% (NEGATIVE alpha)
> 6. **Interpretation:** E offers LESS return than SML requires → E is UNDERPRICED
> 7. **Arbitrage direction:** LONG E (buy the underpriced asset), SHORT replicating portfolio
> 8. Replicating portfolio: 50% A + 50% F (beta = 0.5×1.2 = 0.6)
> 9. Replicating return: 0.5×12% + 0.5×6% = 9%
> 10. Arbitrage profit: 9% - 8% = 1% (gain from shorting expensive replicating, buying cheap E)
> 11. **Verification:** We profit by buying the asset that offers less than it should (E at 8%) and shorting the combination that offers more (replicating at 9%)

**Common Mistakes to Avoid:**
- Confusing the sign of alpha with the arbitrage direction (negative alpha means underpriced, so LONG it)
- Stating "SHORT the underpriced portfolio" (should LONG underpriced assets)
- Not constructing a replicating portfolio with identical beta
- Calculating the wrong market risk premium from available portfolios
- Reversing the arbitrage strategy direction based on incorrect interpretation of "underpriced" vs "overpriced"
- **CRITICAL:** Underpriced (actual < SML) means the asset is a bargain → BUY it; Overpriced (actual > SML) means it's expensive → SHORT it