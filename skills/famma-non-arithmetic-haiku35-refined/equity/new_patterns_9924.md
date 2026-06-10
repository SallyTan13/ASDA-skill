# Equity — Concept Confusion

## Pattern: institutional_decision_frameworks

**Description:** Questions involving institutional investment decisions (manager selection, portfolio structure choice, risk management approaches) require understanding the specific decision frameworks, error types, and economic trade-offs relevant to institutional contexts, not just general financial theory.

**When to Use:** 
- Questions about manager selection policies, hiring/firing decisions
- Portfolio structure choices (ETF vs mutual fund vs separate/pooled accounts)
- Performance attribution vs performance appraisal distinctions
- Hedge ratio selection and associated risks
- Active risk calculations involving position substitutions
- Keywords: "manager selection," "portfolio structure," "institutional client," "Type I/II error," "attribution," "appraisal," "hedge ratio," "active risk"

**Procedure:**

1. **Identify the institutional decision context:**
   - Manager selection/retention decisions
   - Portfolio structure/vehicle selection
   - Risk management approach selection
   - Performance measurement methodology

2. **For manager selection contexts, correctly map Type I and Type II errors:**
   - Define the null hypothesis clearly (e.g., "manager is acceptable/should be retained")
   - Type I error = rejecting null when true (rejecting good manager, false positive rejection)
   - Type II error = failing to reject null when false (retaining bad manager, false negative rejection)
   - Tracking "managers NOT hired" helps identify missed opportunities (Type II errors)
   - Tracking "managers removed" helps identify wrongful terminations (Type I errors)

3. **Distinguish performance attribution from performance appraisal:**
   - Attribution = mechanical decomposition of returns into components (allocation, selection, interaction)
   - Appraisal/Evaluation = drawing conclusions about manager skill, quality, or future performance
   - Attribution can be done without making judgments about skill
   - Statements claiming attribution requires skill assessment are incorrect

4. **For portfolio structure decisions, evaluate based on client characteristics:**
   - **ETFs:** Best for smaller accounts, retail investors, need for liquidity, tax efficiency
   - **Mutual funds:** Retail-focused, regulatory restrictions for some institutions
   - **Separate/Pooled accounts:** Best for large institutional clients ($100M+), cost-sensitive, customization needs
   - Consider: account size, cost structure (management fees, trading costs, bid-ask spreads), customization, regulatory constraints

5. **For hedge ratio comparisons, distinguish risk types:**
   - **Outcome risk:** Variability of hedged portfolio returns
   - **Estimation/parameter risk:** Dependency on estimated correlations/betas
   - Minimum variance hedge ratios minimize outcome risk but introduce estimation risk
   - One-for-one hedges avoid parameter dependency but may have higher outcome risk
   - "Riskier" can refer to either type—context determines which

6. **For active risk calculations, recognize covariance structure matters:**
   - Active risk = sqrt(w_active' × Σ × w_active)
   - Depends on BOTH active weights AND correlations between positions
   - Replacing positions changes correlation structure even if net weights similar
   - Substituting highly correlated positions (e.g., two auto stocks) with differently correlated positions (e.g., energy and financial) changes active risk
   - Cannot assess active risk impact from weights alone

7. **Apply the correct framework to evaluate answer choices:**
   - Reject answers that reverse error type definitions
   - Reject answers that conflate attribution with appraisal
   - Reject answers that ignore client-specific economics in structure selection
   - Reject answers that ignore estimation risk in hedge strategies
   - Reject answers that treat active risk as simple arithmetic of weights

---

## Example 1: Manager Selection Error Types

> **Scenario:** An investment committee implements two tracking systems: System A tracks all external managers considered but not hired, and System B tracks all hired managers who were subsequently terminated. The committee wants to minimize decision errors.
>
> **Wrong approach:** "System A minimizes Type I errors (wrongly rejecting good managers) and System B minimizes Type II errors (wrongly keeping bad managers)."
>
> **Correct approach:** 
> - Null hypothesis: "Manager is acceptable/should be hired or retained"
> - Type I error = reject null when true = reject acceptable manager
> - Type II error = fail to reject null when false = accept/retain unacceptable manager
> - System A (tracking NOT hired) identifies potentially missed good managers = helps detect Type II errors
> - System B (tracking terminated) identifies potentially wrongful terminations = helps detect Type I errors
> - Both systems actually help minimize Type II errors by reviewing decisions where managers were excluded or removed

---

## Example 2: Attribution vs Appraisal

> **Scenario:** An analyst states: "Performance attribution analysis requires making judgments about whether a manager's security selection reflected genuine skill or luck."
>
> **Wrong approach:** Accept the statement as correct because attribution involves analyzing manager decisions.
>
> **Correct approach:** 
> - Performance attribution is a mechanical decomposition: Return = Allocation effect + Selection effect + Interaction effect
> - This calculation can be done purely mathematically without any skill judgment
> - Performance appraisal/evaluation is where skill judgments occur
> - The statement incorrectly conflates attribution (mechanical) with appraisal (judgmental)
> - Reject the statement as incorrect

---

## Example 3: Portfolio Structure Selection

> **Scenario:** A pension fund with $300 million to invest is highly cost-sensitive and wants broad equity market exposure. Options are: (A) equity index ETF, (B) equity index mutual fund, (C) pooled separate account.
>
> **Wrong approach:** "ETFs are most cost-efficient, so choose A."
>
> **Correct approach:**
> - Client characteristics: large institutional ($300M), cost-sensitive
> - ETF costs: management fee + bid-ask spread + potential tracking error
> - Mutual fund: typically higher fees, may have institutional restrictions
> - Pooled separate account: direct ownership, no bid-ask spreads, no ETF wrapper fees, economies of scale at $300M size
> - For large institutional clients, separate/pooled accounts typically offer lowest all-in costs
> - Choose C (pooled separate account)

---

## Example 4: Hedge Ratio Risk Types

> **Scenario:** An analyst compares two currency hedging approaches: (1) minimum variance hedge ratio based on historical correlation estimates, (2) one-for-one hedge ratio. The analyst states: "The minimum variance approach is riskier because it depends on correlation estimates that may be unstable."
>
> **Wrong approach:** "Minimum variance hedges minimize risk by definition, so the statement is wrong."
>
> **Correct approach:**
> - Distinguish risk types:
>   - Outcome risk: variability of hedged portfolio returns
>   - Estimation/parameter risk: dependency on potentially unstable estimates
> - Minimum variance hedge minimizes outcome risk (given true parameters)
> - But introduces estimation risk (correlation estimates may be wrong or unstable)
> - One-for-one hedge has higher outcome risk but no parameter dependency
> - The statement is correct when "riskier" refers to estimation/parameter risk
> - Accept the statement as accurate

---

## Example 5: Active Risk and Correlation Structure

> **Scenario:** A portfolio replaces a 2% overweight in Company X (tech sector) and 2% overweight in Company Y (tech sector) with a 2% overweight in Company Z (healthcare) and 2% overweight in Company W (utilities). Net active weights by sector change, but total active weight magnitude is similar.
>
> **Question:** What happens to active risk?
>
> **Wrong approach:** "Net active weights are similar, so active risk is unchanged."
>
> **Correct approach:**
> - Active risk = sqrt(w_active' × Σ × w_active)
> - Original: two tech stocks (likely highly correlated with each other)
> - New: healthcare and utilities (likely lower correlation with each other)
> - Correlation structure changed significantly
> - Even with similar weight magnitudes, different correlations mean different active risk
> - Lower correlation between new positions likely increases active risk (less offsetting)
> - Cannot determine active risk impact from weights alone—need covariance structure
> - Active risk most likely increased (or at minimum, changed)

---

## Example 6: Manager Selection Purpose Mapping

> **Scenario:** A firm tracks two metrics: (1) performance of managers who were finalists but not hired, (2) performance of managers who were hired but later fired. What errors do these minimize?
>
> **Wrong approach:** Map based on intuitive labels without defining null hypothesis.
>
> **Correct approach:**
> - Define null: "Manager is acceptable for hiring/retention"
> - Metric 1 (not hired): Reviews rejected candidates
>   - If they performed well, we made Type I error (rejected good manager)
>   - Tracking helps minimize future Type I errors
> - Metric 2 (hired then fired): Reviews termination decisions
>   - If they performed well after firing, we made Type I error (rejected good manager)
>   - Tracking helps minimize future Type I errors
> - Both metrics help minimize Type I errors (wrongful rejections)

---

**SKILL_MD_ENTRY:** | `equity/institutional_decision_frameworks.md` | Equity | Concept Confusion | Manager selection error types, Attribution vs appraisal, Portfolio structure selection, Hedge ratio risk types, Active risk covariance effects |