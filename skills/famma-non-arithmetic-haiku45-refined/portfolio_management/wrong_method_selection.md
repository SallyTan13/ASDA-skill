# Pattern 1: Underdetermined System Recognition in Multi-Asset CAPM

**Description:** When applying CAPM to multiple securities, failing to recognize that the system of equations may be underdetermined without additional constraints (e.g., identifying the market portfolio composition, having the risk-free rate, or using state-based probability distributions to derive market returns).

**When to Use:** CAPM problems involving multiple securities with beta constraints or relationships, especially when asked to find market risk premium, risk-free rate, or other market parameters. Trigger keywords: "beta difference," "CAPM holds," "market risk premium," state probabilities given.

**Procedure:**
1. Count unknowns vs. equations: List all unknowns (Rf, market risk premium, individual betas if not all given) and available equations (one CAPM equation per security, plus any beta relationship constraints)
2. Check for state-based market return: If state probabilities and individual security returns are provided, the market portfolio return can often be derived as a probability-weighted combination of states or as a portfolio of the given securities
3. Identify if any security IS the market: Check whether one security or portfolio is explicitly or implicitly the market portfolio (correlation = 1, beta = 1)
4. Test for implicit risk-free rate: If a security has zero standard deviation or zero correlation with market, it may be the risk-free asset
5. Use state probabilities when available: Calculate expected returns from state-based data, then use these with beta relationships to form a solvable system
6. Verify solution uniqueness: Before solving, confirm you have enough independent equations; if underdetermined, identify the missing constraint from context

**Example (sanitized):**
> **Scenario:** Two stocks X and Y have expected returns 12% and 18%. Stock X's beta exceeds Stock Y's beta by 0.40. States of economy (recession, normal, boom) with probabilities (0.2, 0.5, 0.3) show returns for both stocks.
> **Wrong approach:** Subtract CAPM equations: E(Rx) - E(Ry) = (βx - βy)(Rm - Rf), solve 0.06 = 0.40(Rm - Rf), conclude market risk premium = 15%
> **Correct approach:** (1) Recognize this has 3 unknowns (Rf, Rm, and the relationship between betas) but only 2 CAPM equations plus 1 beta constraint. (2) Use state probabilities to calculate the market return as a weighted average of the economy states or as a portfolio combination of X and Y. (3) With market return identified, use CAPM equations to solve for Rf. (4) Calculate market risk premium as Rm - Rf.

---

# Pattern 2: Multi-Method Beta Calculation with CAPM Consistency Check

**Description:** Beta can be calculated via correlation formula (ρ × σ_security / σ_market) OR via CAPM rearrangement [β = (E(R) - Rf) / (E(Rm) - Rf)]. Failing to recognize when complete CAPM inputs are available signals that the CAPM method is more direct and should be verified against correlation method for consistency.

**When to Use:** Questions asking for beta when BOTH (1) correlation/standard deviation data AND (2) complete CAPM inputs (expected return, risk-free rate, market return) are provided. Trigger keywords: "expected return," "risk-free asset," "market portfolio," "correlation," "standard deviation."

**Procedure:**
1. Identify available data: Check which inputs are complete—correlation-based (ρ, σ_security, σ_market) vs. CAPM-based (E(R), Rf, E(Rm))
2. Prioritize CAPM when complete: If expected return, risk-free rate, and market return are all given, use β = [E(R) - Rf] / [E(Rm) - Rf] as the primary method
3. Use correlation formula as secondary: Calculate β = ρ × (σ_security / σ_market) as a verification step
4. Check for consistency: Both methods should yield the same beta; if they differ, re-examine which inputs are correct or whether CAPM assumptions hold
5. Resolve discrepancies: If methods disagree, the CAPM-based beta takes precedence when CAPM is stated to hold, as it directly uses equilibrium pricing relationships
6. Verify reasonableness: Confirm beta sign matches correlation sign, and magnitude aligns with relative volatility and return premium

**Example (sanitized):**
> **Scenario:** Stock Z has expected return 15%, standard deviation 0.40, correlation with market 0.60. Market return is 11%, risk-free rate is 4%, market standard deviation is 0.25.
> **Wrong approach:** Calculate β = 0.60 × (0.40 / 0.25) = 0.96, report answer without verification
> **Correct approach:** (1) Note all CAPM inputs available. (2) Calculate via CAPM: β = (0.15 - 0.04) / (0.11 - 0.04) = 0.11 / 0.07 = 1.57. (3) Verify via correlation: β = 0.60 × (0.40 / 0.25) = 0.96. (4) Methods disagree—check problem statement. (5) If "CAPM holds" is stated, use 1.57 as the answer since it satisfies the equilibrium pricing relationship. (6) The discrepancy suggests either data inconsistency or that correlation formula alone is insufficient when CAPM equilibrium is specified.

---

# Pattern 3: State-Based Return Calculation as Market Proxy

**Description:** When state probabilities and security returns across states are provided alongside CAPM questions, the market return is often implicitly defined through these states rather than being an independent given, requiring calculation of expected market return from the state distribution.

**When to Use:** CAPM or portfolio problems where states of economy (recession, normal, boom, etc.) are listed with probabilities and individual security returns, but market return is not directly stated. Trigger keywords: "state of economy," "probability," "return if state occurs," "market portfolio."

**Procedure:**
1. Recognize state data as market information: State probabilities with security returns often implicitly define the market return distribution
2. Calculate market return from states: If not explicitly given, compute E(Rm) = Σ[probability_i × market_return_i] where market return in each state may be a weighted average of available securities
3. Determine market portfolio composition: The market portfolio may be an equal-weighted, value-weighted, or specified combination of the given securities
4. Use calculated market return in CAPM: Apply E(Rm) to CAPM formula β = [E(R) - Rf] / [E(Rm) - Rf] or to find risk premium
5. Cross-validate with beta relationships: If beta differences are given, verify that calculated market return produces consistent betas across securities
6. Check if securities span the market: Confirm whether the given securities are sufficient to represent the market portfolio in the problem context

**Example (sanitized):**
> **Scenario:** Economy has three states (downturn 0.3, stable 0.5, growth 0.2). Stock P returns (-5%, 8%, 20%) and Stock Q returns (2%, 10%, 15%) in these states. Beta of P exceeds beta of Q by 0.30. Find market risk premium.
> **Wrong approach:** Calculate E(Rp) and E(Rq), then use difference with beta difference to solve for market risk premium without identifying market return
> **Correct approach:** (1) Calculate E(Rp) = 0.3(-0.05) + 0.5(0.08) + 0.2(0.20) = 0.065. (2) Calculate E(Rq) = 0.3(0.02) + 0.5(0.10) + 0.2(0.15) = 0.086. (3) Assume market return in each state is weighted average of P and Q (or use other context clues). (4) Calculate E(Rm) from states. (5) Use CAPM with beta difference: [E(Rp) - Rf] / [E(Rm) - Rf] - [E(Rq) - Rf] / [E(Rm) - Rf] = 0.30 to solve for Rf and market risk premium together, or identify Rf from additional constraints.