# Skill Patterns for Unit/Currency/Percent Conversion Errors in Portfolio Management

## Pattern: Time-Scale Conversion in Stochastic Processes

**Description:** When converting stochastic differential equations or volatility models from one time unit to another (e.g., daily to annual), both drift and diffusion terms must be scaled appropriately, and discrete-time models must be expressed in continuous-time differential form.

**When to Use:** Questions involving volatility models, GARCH processes, or stochastic equations where time measurement units change (keywords: "when time is measured in," "convert to annual," "daily to yearly").

**Procedure:**
1. Identify the original time unit (e.g., days) and target time unit (e.g., years) in the stochastic process
2. Determine the conversion factor N (e.g., 252 trading days per year)
3. For the drift term: multiply by N to scale linearly with time periods
4. For the diffusion/volatility term: multiply by √N to scale with the square root of time
5. Convert discrete-time difference equations (ΔV) to continuous-time differential form (dV = drift·dt + volatility·dz)
6. Verify dimensional consistency: drift should have units of [variance/target time unit], diffusion should have units of [variance/√target time unit]

**Example (sanitized):**
> **Scenario:** A mean-reverting variance model is given as V(t+1) = 0.05(0.04 - V(t)) + 0.3√V(t)·Z in daily terms. Convert to monthly terms (assume 21 trading days per month).
> **Wrong approach:** Simply stating the same equation with "monthly" label, or only scaling one term.
> **Correct approach:** (1) Identify N=21, (2) Scale drift: 21×0.05=1.05, (3) Scale diffusion: 0.3×√21≈1.374, (4) Express in differential form: dV = 1.05(0.04-V)dt + 1.374√V·dz where t is now in months.

---

## Pattern: After-Tax Proceeds from Asset Sales with Cost Basis

**Description:** When calculating net liquidity from selling appreciated assets, capital gains tax must be applied to the gain (sale price minus cost basis), not to the gross proceeds. The available cash is gross proceeds minus tax on gains.

**When to Use:** Questions about liquidity from asset sales, portfolio liquidation, or funding requirements where assets have appreciated (keywords: "cost basis," "capital gains tax," "net proceeds," "available liquidity").

**Procedure:**
1. Identify the sale price (gross proceeds) of the asset
2. Identify the cost basis (original purchase price or tax basis) per unit
3. Calculate the capital gain per unit: gain = sale price - cost basis
4. Apply the capital gains tax rate to the gain only: tax = gain × tax rate
5. Calculate net proceeds per unit: net = sale price - tax = cost basis + gain×(1 - tax rate)
6. Multiply by number of units sold to get total available liquidity
7. Add any existing cash or liquid assets to determine total liquidity available
8. Subtract immediate funding requirements to find excess or shortfall

**Example (sanitized):**
> **Scenario:** An investor sells 500 shares at $20/share with a cost basis of $2/share. Capital gains tax is 30%. What net proceeds are available?
> **Wrong approach:** $20 × 500 = $10,000 net proceeds (ignoring tax entirely).
> **Correct approach:** (1) Sale price = $20, cost basis = $2, (2) Gain = $20 - $2 = $18, (3) Tax = $18 × 0.30 = $5.40 per share, (4) Net per share = $20 - $5.40 = $14.60, (5) Total net = $14.60 × 500 = $7,300 available.

---

## Pattern: Present Value of Annuity Due vs. Lump Sum Requirements

**Description:** When funding a future goal through periodic payments starting immediately (annuity due), the first payment required is NOT the future value divided by number of payments, but rather the payment that—when invested with compounding—will grow to the target amount.

**When to Use:** Questions about education funding, retirement savings, or any goal requiring periodic contributions to reach a future target (keywords: "annual payments starting immediately," "payments starting now," "savings fund," "annuity due").

**Procedure:**
1. Identify the future value target (FV), number of payments (n), and interest rate (r)
2. Recognize if payments start immediately (annuity due) vs. end of period (ordinary annuity)
3. For annuity due, use the formula: Payment = FV / [((1+r)^n - 1)/r × (1+r)]
4. For ordinary annuity, use: Payment = FV / [((1+r)^n - 1)/r]
5. Calculate the first payment amount as the immediate liquidity requirement
6. Do NOT treat the future value as an immediate lump-sum need unless explicitly stated
7. Verify: the payment amount × number of periods should be less than FV due to compounding

**Example (sanitized):**
> **Scenario:** Need $500,000 in 10 years for a goal. Plan to make 10 annual payments starting today into an account earning 4% annually. What is the immediate payment needed?
> **Wrong approach:** Treating $500,000 as immediate need, or calculating $500,000/10 = $50,000 per payment.
> **Correct approach:** (1) FV = $500,000, n = 10, r = 0.04, (2) Annuity due formula, (3) Payment = $500,000 / [((1.04)^10 - 1)/0.04 × 1.04] = $500,000 / 12.486 ≈ $40,045, (4) Immediate need is $40,045, not $500,000.

---

## Pattern: Precision Requirements in Portfolio Optimization

**Description:** Portfolio optimization problems (minimum variance, efficient frontier) require maintaining full numerical precision through all algebraic steps, as small differences in weights (e.g., 0.78 vs 0.80) meaningfully impact portfolio characteristics.

**When to Use:** Questions involving portfolio weight optimization, minimum variance portfolios, or efficient frontier calculations (keywords: "minimize variance," "optimal weights," "portfolio optimization," "find weights such that").

**Procedure:**
1. Set up the optimization equation with full symbolic precision (e.g., σ²p = w²A·σ²A + w²B·σ²B + 2wA·wB·Cov(A,B))
2. Apply the constraint (e.g., wA + wB = 1, so wB = 1 - wA)
3. Substitute to get a single-variable equation
4. Take the derivative and set equal to zero: dσ²p/dwA = 0
5. Solve algebraically WITHOUT rounding intermediate terms (keep variances, covariances in exact form)
6. Only round the final answer to the precision requested (typically 4 decimal places for weights)
7. Verify: substitute weights back into variance formula and confirm it's a minimum (second derivative > 0)
8. Check constraint: weights sum to 1.0000 within rounding tolerance

**Example (sanitized):**
> **Scenario:** Stock X has σ=20%, Stock Y has σ=40%, Cov(X,Y)=0.006. Find minimum variance portfolio weights.
> **Wrong approach:** Rounding variances to σ²X≈0.04, σ²Y≈0.16 early, then solving to get wX≈0.8.
> **Correct approach:** (1) σ²p = w²X(0.04) + (1-wX)²(0.16) + 2wX(1-wX)(0.006), (2) Expand fully, (3) dσ²p/dwX = 0.08wX - 0.32(1-wX) + 0.012(1-2wX) = 0, (4) Solve: 0.08wX - 0.32 + 0.32wX + 0.012 - 0.024wX = 0, (5) 0.368wX = 0.308, (6) wX = 0.8370, wY = 0.1630 (precise to 4 decimals).

---

## Pattern: Percentage vs. Decimal in Variance Calculations

**Description:** Standard deviations are often given as percentages (e.g., 33%) but must be converted to decimals (0.33) before squaring to obtain variance for use in portfolio calculations, and covariances must match the same scale.

**When to Use:** Any portfolio variance, standard deviation, or covariance calculation where inputs are given as percentages (keywords: "standard deviation %," "expected return %," "covariance," "portfolio variance").

**Procedure:**
1. Identify all inputs given as percentages (standard deviations, returns)
2. Convert percentages to decimals by dividing by 100 (e.g., 33% → 0.33)
3. Square standard deviations to get variances: σ² = (σ/100)² if σ is in percent form
4. Verify covariance units match: if given as 0.001, confirm whether this is already in decimal² form
5. Perform all calculations in consistent decimal form
6. Convert final results back to percentages only if requested
7. Double-check: variance of 33% should be 0.1089, not 1089 or 0.0011

**Example (sanitized):**
> **Scenario:** Asset M has σ=25%, Asset N has σ=50%, Cov(M,N)=0.008. Calculate portfolio variance with wM=0.6, wN=0.4.
> **Wrong approach:** σ²p = (0.6)²(25)² + (0.4)²(50)² + 2(0.6)(0.4)(0.008) = 225 + 400 + 0.00384 (mixing scales).
> **Correct approach:** (1) Convert: σM=0.25, σN=0.50, (2) σ²M=0.0625, σ²N=0.25, (3) σ²p = (0.6)²(0.0625) + (0.4)²(0.25) + 2(0.6)(0.4)(0.008) = 0.0225 + 0.04 + 0.00384 = 0.06634, (4) σp = 25.76% if converting back.