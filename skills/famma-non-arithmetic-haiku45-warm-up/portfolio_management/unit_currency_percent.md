# Skill Patterns for Unit/Currency/Percent Conversion Errors in Portfolio Management

## Pattern: Time-Scale Conversion in Stochastic Processes

**Description:** When converting continuous-time stochastic differential equations between time units (e.g., daily to annual), drift terms scale linearly with the conversion factor while diffusion terms scale with the square root of the conversion factor due to quadratic variation properties of Brownian motion.

**When to Use:** When converting stochastic volatility models, GARCH models, or any SDE between time measurement units (days/years, months/years). Trigger keywords: "time measured in," "convert to annual," "daily to yearly."

**Procedure:**
1. Identify the base time unit (e.g., days) and target time unit (e.g., years) in the stochastic process
2. Calculate the conversion factor N (e.g., 252 trading days per year)
3. For drift terms (dt coefficients): multiply by N to scale linearly
4. For diffusion terms (dz coefficients): multiply by √N to scale with square root
5. Apply transformations: if original is dV = a(V_L - V)dt + ξV dz (daily), then annual form is dV = Na(V_L - V)dt + ξV√N dz
6. Verify dimensional consistency: drift has units of [variance/time], diffusion has units of [variance/√time]

**Example (sanitized):**
> **Scenario:** A mean-reverting process for interest rates is dR = 0.5(0.03 - R)dt + 0.02√R dz when time is in months. Convert to annual measurement.
> **Wrong approach:** Simply use dR = 0.5(0.03 - R)dt + 0.02√R dz without adjustment, or scale both terms by 12.
> **Correct approach:** With 12 months per year, drift scales by 12: 12×0.5 = 6. Diffusion scales by √12: 0.02√12 ≈ 0.0693. Annual form: dR = 6(0.03 - R)dt + 0.0693√R dz.

---

## Pattern: Present Value of Annuity Due with Deferred Target Date

**Description:** When calculating periodic payments for an annuity due (payments at period start) that must accumulate to a future value at a date beyond the last payment, the gap period between final payment and target date requires separate compounding calculation.

**When to Use:** Problems involving education funding, retirement savings with immediate payments starting now but target date years later. Trigger keywords: "starting immediately," "annual payments," "available when," "N years from now."

**Procedure:**
1. Identify payment frequency (n payments), interest rate (r), and two critical dates: last payment date and target future value date
2. Calculate the gap period: g = (target date) - (last payment date). For payments starting immediately over n years to target in year T: g = T - (n-1)
3. Use future value of annuity due formula: FV_at_last_payment = PMT × [(1+r)^n - 1]/r × (1+r)
4. Compound forward through gap period: FV_target = FV_at_last_payment × (1+r)^g
5. Solve for PMT: PMT = FV_target / {[(1+r)^n - 1]/r × (1+r) × (1+r)^g}
6. Verify: last payment occurs at year (n-1), compounds for (T - n + 1) additional years to reach year T

**Example (sanitized):**
> **Scenario:** Need $500,000 in 12 years. Make 4 annual payments starting today, earning 4% annually. Calculate payment amount.
> **Wrong approach:** Use simple annuity due: PMT = $500,000 / [((1.04)^4 - 1)/0.04 × 1.04] = $115,096, ignoring that last payment is at year 3, not year 12.
> **Correct approach:** Last payment at year 3, target at year 12, gap = 9 years. FV at year 3 = PMT × 4.2465 × 1.04. This compounds 9 more years: FV × (1.04)^9 = $500,000. Solving: PMT × 4.4164 × 1.4233 = $500,000, so PMT = $79,571.

---

## Pattern: Percentage-Decimal Unit Consistency in Variance Calculations

**Description:** When variance/covariance and standard deviations are provided in mixed units (percentages vs. decimals), they must be converted to consistent units before calculation, recognizing that variance has squared units.

**When to Use:** Portfolio optimization, minimum variance calculations when standard deviations are given as percentages (e.g., "33%") and covariance as decimal (e.g., "0.001"). Trigger keywords: "standard deviation," "covariance," "variance," with mixed notation.

**Procedure:**
1. Identify the units of all inputs: check if standard deviations are percentages (33%) or decimals (0.33)
2. Identify covariance units: if σ is in %, then Cov should be in (%·%)  = (percentage points)²
3. Convert to consistent basis: either (a) convert % to decimals by dividing by 100, then divide covariance by 10,000, OR (b) keep % as-is and multiply decimal covariance by 10,000
4. For minimum variance portfolio: XA = (σ_B² - Cov_AB) / (σ_A² + σ_B² - 2×Cov_AB), ensuring all terms have identical units
5. Verify dimensional consistency: numerator and denominator must both be in variance units (either decimal² or %²)
6. Cross-check: if covariance seems unusually small relative to variances, suspect unit mismatch

**Example (sanitized):**
> **Scenario:** Stock X: σ = 25%, Stock Y: σ = 40%, Cov(X,Y) = 0.0008. Find minimum variance weights.
> **Wrong approach:** Directly use XA = (0.40² - 0.0008) / (0.25² + 0.40² - 2×0.0008) = (0.16 - 0.0008)/(0.0625 + 0.16 - 0.0016) = 0.1592/0.2209 = 0.72, mixing percentage² and decimal units.
> **Correct approach:** Convert to decimals: σ_X = 0.25, σ_Y = 0.40, Cov = 0.0008 (already matches decimal² units). Calculate: XA = (0.16 - 0.0008)/(0.0625 + 0.16 - 0.0016) = 0.1592/0.2209 = 0.72. OR keep as %: σ_X = 25, σ_Y = 40, Cov = 80 (0.0008×10000). Calculate: XA = (1600 - 80)/(625 + 1600 - 160) = 1520/2065 = 0.74. The first approach is correct.

---

## Pattern: Arithmetic Verification in Multi-Step Financial Calculations

**Description:** After deriving intermediate results through algebraic manipulation, explicitly verify arithmetic operations (especially subtraction and division with percentages) before finalizing answers, as execution errors often occur in the final computational step.

**When to Use:** Any multi-step calculation involving CAPM, portfolio returns, or algebraic systems where intermediate values are substituted back into equations. Always verify when answer seems "close but not exact" to expected result.

**Procedure:**
1. Complete algebraic derivation to obtain intermediate results (e.g., market risk premium = 6.8%)
2. Write out the substitution equation explicitly with all values: "8.54% = Rf + 0.80 × 6.8%"
3. Calculate the product/multiplication term separately: 0.80 × 6.8% = 5.44%
4. Perform the final arithmetic operation with explicit notation: Rf = 8.54% - 5.44%
5. Execute the arithmetic carefully: 8.54 - 5.44 = 3.10, so Rf = 3.10%
6. Verify by substituting back into original equation: 3.10% + 0.80 × 6.8% = 3.10% + 5.44% = 8.54% ✓
7. If verification fails, re-check each arithmetic step rather than adjusting the final answer

**Example (sanitized):**
> **Scenario:** Solving for cost of equity: 14.5% = Rf + 1.2(Rm - Rf) and 10.8% = Rf + 0.7(Rm - Rf). Find Rf.
> **Wrong approach:** Subtract equations: 3.7% = 0.5(Rm - Rf), so (Rm - Rf) = 7.4%. Substitute: 10.8% = Rf + 0.7×7.4%, so 10.8% = Rf + 5.18%, therefore Rf = 6.62% (arithmetic error: 10.8 - 5.18 = 5.62, not 6.62).
> **Correct approach:** After finding (Rm - Rf) = 7.4%, write: 10.8% = Rf + 0.7×7.4%. Calculate: 0.7×7.4 = 5.18. Subtract: Rf = 10.8 - 5.18 = 5.62%. Verify: 5.62% + 0.7×7.4% = 5.62% + 5.18% = 10.80% ✓

---

## Pattern: Confidence Maintenance in Valid Algebraic Derivations

**Description:** When algebraic methods produce unexpected but mathematically sound results, verify the problem setup and calculation steps rather than overriding with intuitive adjustments, as counterintuitive answers may be correct given specific problem parameters.

**When to Use:** When derived answer seems unusually high/low compared to typical market values, but algebraic steps are valid. Trigger: internal doubt about "reasonable" answer magnitude.

**Procedure:**
1. Complete the algebraic derivation following standard formulas (e.g., CAPM, portfolio theory)
2. If result seems unexpected (e.g., market risk premium of 19.2% vs. typical 7-8%), resist immediate adjustment
3. Verify calculation steps: re-check each arithmetic operation and formula application
4. Verify input data: confirm expected returns, betas, and other parameters are correctly extracted from problem
5. Check problem constraints: unusual parameters (high volatility, extreme betas) can produce unusual but valid results
6. Only if verification reveals error should result be changed; otherwise accept the mathematically derived answer
7. Document reasoning: "Result of 19.2% is high but consistent with the given beta differential of 0.25 and return spread of 4.8%"

**Example (sanitized):**
> **Scenario:** Two stocks with E(R_A) = 18%, E(R_B) = 12%, β_A - β_B = 0.4. Find market risk premium using CAPM.
> **Wrong approach:** Calculate (18% - 12%)/0.4 = 15% market risk premium, think "this seems too high for typical markets," then adjust to 8% based on intuition.
> **Correct approach:** Apply CAPM difference formula: E(R_A) - E(R_B) = (β_A - β_B)(Rm - Rf). Substitute: 6% = 0.4(Rm - Rf). Solve: (Rm - Rf) = 15%. Verify inputs are correct. Recognize that the problem's high return spread (6%) combined with moderate beta difference (0.4) mathematically requires a 15% market risk premium. Accept this result as valid for the given parameters, even if atypical.

---

## Pattern: Tax-Adjusted Liquidity Calculation with Capital Gains

**Description:** When calculating available liquidity from asset sales, capital gains taxes must be deducted from gross proceeds based on the difference between sale price and cost basis, not applied to the entire sale amount.

**When to Use:** Problems involving immediate liquidity needs, asset sales for funding goals, buyout offers. Trigger keywords: "available liquidity," "net proceeds," "cost basis," "capital gains tax."

**Procedure:**
1. Calculate gross proceeds: (number of units sold) × (sale price per unit)
2. Identify cost basis per unit (may be $0 for inherited assets with stepped-up basis reset)
3. Calculate total capital gain: (sale price - cost basis) × (number of units sold)
4. Apply capital gains tax rate to the gain only: tax = (capital gain) × (tax rate)
5. Calculate net proceeds from sale: gross proceeds - tax
6. Add any existing liquid assets (cash, equivalents) to net proceeds for total available liquidity
7. Compare total available liquidity to immediate funding needs to determine excess/shortfall

**Example (sanitized):**
> **Scenario:** Sell 200 shares at $50/share, cost basis $10/share, 20% capital gains tax. Have $100,000 cash. Need $8,500 immediately.
> **Wrong approach:** Gross proceeds = $10,000. Apply 20% tax to entire amount: $10,000 × 0.20 = $2,000 tax. Net = $8,000 + $100,000 = $108,000. Excess = $99,500.
> **Correct approach:** Gross proceeds = 200 × $50 = $10,000. Capital gain = (50-10) × 200 = $8,000. Tax = $8,000 × 0.20 = $1,600. Net from sale = $10,000 - $1,600 = $8,400. Total liquidity = $8,400 + $100,000 = $108,400. Excess = $108,400 - $8,500 = $99,900.