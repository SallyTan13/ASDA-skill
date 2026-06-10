# Portfolio Management — Conceptual Inversions and Multi-Step Logic

## Pattern: CAPM Pricing Direction Inversion

**Description:** When expected return is below CAPM required return, the security is overpriced (not underpriced) because investors are accepting insufficient compensation for risk, implying the current price is too high. This pattern applies to security valuation and investment decisions, NOT to solving for CAPM parameters.

**When to Use:** Questions about CAPM pricing, security valuation, buy/sell recommendations based on expected vs. required returns where the risk-free rate and market return are GIVEN.

**When NOT to Use:** 
- Questions asking to SOLVE for CAPM parameters (risk-free rate, market return, beta) from given security data
- Questions requiring simultaneous equation solving using multiple securities
- Questions where you need to CALCULATE the risk-free rate or market risk premium from observed returns
- Reverse-engineering problems where parameters are unknown

**Procedure:**
1. **Verify this is a valuation problem:** Confirm that risk-free rate, market return, and beta are GIVEN, and you need to determine if a security is fairly priced
2. Calculate CAPM required return: r_required = r_f + β(r_m - r_f)
3. Compare expected return to required return
4. Apply inverse pricing logic:
   - If expected return < required return → security is OVERPRICED → SELL
   - If expected return > required return → security is UNDERPRICED → BUY
5. Reasoning: Lower expected return means investors are paying too much (high price) for insufficient future cash flows

**Common Mistakes to Avoid:**
- Applying this pattern to parameter-solving problems where you need to find the risk-free rate or market return
- Using CAPM pricing logic when the question asks "what is the risk-free rate?" or "what is the market return?"
- Confusing valuation problems (given parameters, find if overpriced) with calibration problems (given prices/returns, find parameters)
- Over-applying the conceptual inversion framework to algebraic equation-solving tasks

**Example (sanitized):**
> **Scenario:** Stock A has β=1.2, expected return=9%, risk-free rate=3%, market return=8%. Should you buy or sell?
> **Wrong approach:** This is a parameter-solving problem requiring simultaneous equations
> **Correct approach:** This is a valuation problem. Required return = 3% + 1.2(8%-3%) = 9%. Since expected equals required, fairly priced. If expected were 8%, the stock would be OVERPRICED (investors accepting 8% when they should demand 9%, meaning they're paying too much), so SELL.

> **Counter-example (when NOT to use this pattern):**
> **Scenario:** Two securities are correctly priced. Security X: β=1.3, E(R)=11%. Security Y: β=0.9, E(R)=8%. What is the risk-free rate?
> **Wrong approach:** Apply pricing inversion logic to determine over/undervaluation
> **Correct approach:** This is a parameter calibration problem. Set up simultaneous CAPM equations: 11% = rf + 1.3(rm - rf) and 8% = rf + 0.9(rm - rf). Solve algebraically by subtracting equations to find the market risk premium, then substitute back to find rf. The pricing inversion pattern does NOT apply here.
## Pattern: Risk-Adjusted Hurdle Rate Misapplication

**Description:** Using a firm's overall cost of capital as a hurdle rate can incorrectly accept high-risk projects with returns above the overall rate but below their project-specific required returns.

**When to Use:** Capital budgeting questions involving multiple projects with different risk levels, CAPM-based project evaluation, hurdle rate selection.

**Procedure:**
1. Calculate project-specific required returns using CAPM: r_j = r_f + β_j(r_m - r_f)
2. Identify or calculate firm's overall cost of capital (WACC or weighted average of project returns)
3. For each project, compare IRR to both rates:
   - Correct decision: Accept if IRR > project-specific required return
   - Incorrect decision with overall rate: Accept if IRR > overall cost of capital
4. Identify projects where: overall cost of capital < IRR < project-specific required return
5. These projects are INCORRECTLY ACCEPTED when using overall rate (they don't compensate for their specific risk)

**Example (sanitized):**
> **Scenario:** Firm WACC = 10%. Project X: β=1.5, IRR=11%, CAPM required=12%. Project Y: β=0.8, IRR=9%, CAPM required=8%.
> **Wrong approach:** Both projects have IRR > WACC (10%), so accept both
> **Correct approach:** Project X should be REJECTED (IRR 11% < required 12%). Using WACC incorrectly accepts X. Project Y should be ACCEPTED (IRR 9% > required 8%). Project X is the incorrectly accepted project.

---

## Pattern: Joint Probability vs. Conditional Probability Confusion

**Description:** Joint probability P(A and B) requires multiplying P(A) × P(B|A), not using P(A) alone or P(B|A) alone.

**When to Use:** Scenario analysis with multiple conditions, probability trees, questions asking for "probability of both X and Y occurring."

**Procedure:**
1. Identify the two events: Event A (e.g., economic state) and Event B (e.g., asset performance)
2. Find P(A) = marginal probability of Event A
3. Find P(B|A) = conditional probability of Event B given Event A
4. Calculate joint probability: P(A and B) = P(A) × P(B|A)
5. Do NOT use P(A) alone or P(B|A) alone as the answer

**Example (sanitized):**
> **Scenario:** P(Recession) = 0.30. Given recession, P(Stock declines) = 0.70. What is P(Recession AND Stock declines)?
> **Wrong approach:** Answer is 0.30 (just the recession probability) or 0.70 (just the conditional probability)
> **Correct approach:** P(Recession AND Stock declines) = 0.30 × 0.70 = 0.21 or 21%

---

## Pattern: High-Water Mark Cumulative Recovery Logic

**Description:** High-water marks require fund value to exceed the previous peak before performance fees apply, creating cumulative effects across multiple periods where underperformance must be recovered.

**When to Use:** Performance fee calculations, hedge fund compensation, questions about fee impacts across multiple years with varying returns.

**Procedure:**
1. Identify the initial high-water mark (starting NAV or first period peak)
2. Track cumulative fund value across periods
3. For each period:
   - If current value > previous high-water mark: performance fees apply, update high-water mark
   - If current value ≤ previous high-water mark: NO performance fees, high-water mark unchanged
4. After underperformance, the fund must recover back above the previous peak before fees resume
5. The first period AFTER recovery where value exceeds the old peak is when fees are affected

**Example (sanitized):**
> **Scenario:** Fund starts at $100M (Year 0). Year 1: +20% → $120M (fees apply, HWM=$120M). Year 2: -10% → $108M (no fees, HWM stays $120M). Year 3: +15% → $124.2M. Which year is affected by HWM?
> **Wrong approach:** Year 2 is affected because performance declined
> **Correct approach:** Year 3 is affected. In Year 2, fund is below HWM so no performance fees anyway. In Year 3, fund exceeds the Year 1 HWM ($124.2M > $120M), so performance fees resume. Year 3 is the first year where the HWM provision affects fee calculation (fees are charged only on the gain above $120M, not the full Year 3 return).

---

## Pattern: Discrete-to-Continuous Time Scaling in Stochastic Models

**Description:** Converting discrete-time models (e.g., GARCH) to continuous-time SDEs requires scaling parameters by the number of periods per unit time and transforming difference equations to differential equations.

**When to Use:** Questions asking for continuous-time versions of discrete models, time-scale conversions (daily to annual), stochastic differential equation formulations.

**Procedure:**
1. Identify the discrete model and its time unit (e.g., daily GARCH)
2. Identify the target time unit (e.g., annual) and scaling factor N (e.g., 252 trading days/year)
3. Convert discrete differences to differentials:
   - Δt → dt
   - Discrete increments → continuous differentials (dV, dz)
4. Scale drift terms by N: coefficient × N
5. Scale diffusion terms by √N: volatility × √N
6. Transform mean-reversion structure: (target - current) becomes drift toward long-run mean
7. Write as SDE: dX = [drift with N scaling]dt + [diffusion with √N scaling]dz

**Example (sanitized):**
> **Scenario:** Daily variance model: V_t = 0.001 + 0.08(r_{t-1}²) + 0.90V_{t-1}. Convert to annual continuous-time SDE.
> **Wrong approach:** Just write dV = 0.001dt + 0.08(r²)dt + 0.90Vdt
> **Correct approach:** 
> 1. Recognize mean-reverting structure: V_t - V_{t-1} ≈ -α(V_{t-1} - V_L) where V_L = 0.001/(1-0.08-0.90) = long-run variance, α = 1-0.90 = 0.10
> 2. Scale to annual: dV = 252α(V_L - V)dt + ξV√252 dz
> 3. Result: dV = 25.2(V_L - V)dt + ξV×15.87 dz (where ξ is volatility parameter)

---

## Pattern: Return-Price Relationship in Overvaluation

**Description:** When a security's expected return is insufficient relative to its risk, the market price is too high (overvalued), not too low, because price and required return are inversely related.

**When to Use:** Questions about fair value, overvaluation/undervaluation, investment recommendations based on return adequacy.

**Procedure:**
1. Determine required return for the security's risk level
2. Determine expected return from the security
3. Apply inverse price-return logic:
   - Expected return < Required return → Current price is TOO HIGH → Overvalued
   - Expected return > Required return → Current price is TOO LOW → Undervalued
4. Reasoning: Price = PV(Future Cash Flows) / Discount Rate. If discount rate should be higher (required return > expected), then current price is too high for those cash flows
5. Investment action: Sell overvalued, Buy undervalued

**Example (sanitized):**
> **Scenario:** Bond offers 5% yield. Given its risk, it should offer 6%. Is it overvalued or undervalued?
> **Wrong approach:** It's undervalued because it's not offering enough return
> **Correct approach:** It's OVERVALUED. The bond is priced to yield only 5% when it should yield 6%. This means investors are paying too much (high price) for the bond's cash flows. To yield 6%, the price must be LOWER. Current high price = overvaluation. Recommendation: SELL.

---

## Pattern: Multi-Period Fee Structure Impact Analysis

**Description:** Performance-based fee structures with provisions like high-water marks, hurdle rates, or clawbacks create path-dependent effects where fee calculations in one period depend on cumulative performance history.

**When to Use:** Questions about fee calculations across multiple periods, identifying which periods are affected by fee provisions, comparing fee structures.

**Procedure:**
1. Map out the complete performance history period by period
2. Calculate cumulative fund value at each period end
3. Identify the fee provision type:
   - High-water mark: fees only on gains above previous peak
   - Hurdle rate: fees only on returns above minimum threshold
   - Clawback: fees returned if subsequent underperformance
4. For each period, determine:
   - Does the provision constraint bind? (e.g., is fund below HWM?)
   - Are fees affected (reduced/eliminated) by the provision?
5. Identify the specific period where the provision changes fee calculation vs. baseline

**Example (sanitized):**
> **Scenario:** Fund with 20% performance fee and 5% hurdle rate. Year 1: 8% return. Year 2: 3% return. Year 3: 7% return. Which years are affected by hurdle rate?
> **Wrong approach:** All years are affected because the hurdle exists
> **Correct approach:** Year 1: 8% > 5%, so fees on (8%-5%)=3% excess. Year 2: 3% < 5%, so NO performance fees (affected - fees eliminated). Year 3: 7% > 5%, so fees on 2% excess. Years 2 and 3 show the hurdle rate's impact - Year 2 eliminates fees, Year 3 reduces fee base.

---

## Pattern: Conditional vs. Marginal Probability in Scenario Analysis

**Description:** In multi-stage scenarios, probabilities must be properly conditioned on prior events; marginal probabilities alone are insufficient for sequential or joint outcomes.

**When to Use:** Decision trees, scenario analysis with dependencies, questions about "given that X occurred, what is probability of Y?"

**Procedure:**
1. Identify whether question asks for:
   - Marginal P(A): probability of A regardless of other events
   - Conditional P(B|A): probability of B given A occurred
   - Joint P(A and B): probability both occur
2. For conditional probability: use only the branch where condition is met
3. For joint probability: multiply along the path: P(A) × P(B|A) × P(C|A,B)...
4. For marginal probability: sum across all paths leading to the event
5. Do not confuse P(A) with P(A|B) or P(A and B)

**Example (sanitized):**
> **Scenario:** P(Bull market) = 0.6, P(Bear market) = 0.4. Given bull, P(Stock up) = 0.8. Given bear, P(Stock up) = 0.3. What is P(Stock up)?
> **Wrong approach:** Answer is 0.8 (the conditional probability given bull market)
> **Correct approach:** This asks for marginal P(Stock up) across all scenarios: P(Stock up) = P(Bull)×P(Up|Bull) + P(Bear)×P(Up|Bear) = 0.6×0.8 + 0.4×0.3 = 0.48 + 0.12 = 0.60 or 60%

---

## Pattern: Project Selection with Heterogeneous Risk

**Description:** When projects have different risk profiles, using a single hurdle rate (like WACC) systematically biases selection toward high-risk projects and against low-risk projects.

**When to Use:** Capital budgeting with multiple projects, divisional cost of capital, risk-adjusted performance evaluation.

**Procedure:**
1. Calculate risk-adjusted required return for each project using CAPM or other risk model
2. Calculate firm's overall hurdle rate (WACC or average)
3. Classify each project:
   - High-risk: β > β_firm, required return > WACC
   - Low-risk: β < β_firm, required return < WACC
4. Identify selection errors with single hurdle rate:
   - High-risk projects with IRR between WACC and project-required return: incorrectly ACCEPTED
   - Low-risk projects with IRR between project-required return and WACC: incorrectly REJECTED
5. Correct approach: compare each IRR to its project-specific required return

**Example (sanitized):**
> **Scenario:** WACC = 12%. Project A: β=1.5, required=15%, IRR=13%. Project B: β=0.5, required=8%, IRR=10%.
> **Wrong approach:** Using WACC: Accept A (13%>12%), Reject B (10%<12%)
> **Correct approach:** Project A should be REJECTED (13%<15% required). Project B should be ACCEPTED (10%>8% required). Using WACC incorrectly accepts the risky Project A (it doesn't compensate for its high risk) and incorrectly rejects the safe Project B (it provides adequate return for its low risk).

---

## Pattern: Time-Scale Transformation in Volatility Models

**Description:** Volatility and variance scale differently with time: variance scales linearly with time, volatility (standard deviation) scales with square root of time.

**When to Use:** Converting between time periods (daily/monthly/annual), scaling risk measures, continuous-time model calibration.

**Procedure:**
1. Identify source time unit and target time unit
2. Calculate scaling factor N (e.g., 252 days per year, 12 months per year)
3. For variance: σ²_annual = N × σ²_period
4. For volatility: σ_annual = √N × σ_period
5. In stochastic models:
   - Drift terms scale by N
   - Diffusion terms scale by √N
6. Verify dimensional consistency: dt has units of time, dz is dimensionless

**Example (sanitized):**
> **Scenario:** Daily volatility = 1.5%. What is annual volatility (252 trading days)?
> **Wrong approach:** Annual volatility = 252 × 1.5% = 378%
> **Correct approach:** Annual volatility = √252 × 1.5% = 15.87 × 1.5% ≈ 23.8%. Variance scales linearly (daily variance × 252 = annual variance), but volatility scales by square root.

---

SKILL_MD_ENTRY: | `portfolio_management/conceptual_inversions.md` | Portfolio Management | Conceptual Inversions and Multi-Step Logic | CAPM Pricing Direction, Risk-Adjusted Hurdle Rates, Joint Probability, High-Water Mark Logic, Time-Scale Transformations, Return-Price Inversion, Multi-Period Fee Analysis, Conditional Probability, Heterogeneous Risk Selection, Volatility Scaling |