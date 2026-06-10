# Derivatives — Multi-Step Calculation and Answer Mapping Errors

## Pattern 1: Binomial Option Pricing with Multi-Period Trees

**Description:** Failure to correctly apply binomial tree methodology for option pricing, particularly confusing total option life with per-period time steps when calculating risk-neutral probabilities and failing to properly execute backward induction through multiple periods.

**When to Use:** Questions involving binomial trees, multi-step option pricing, risk-neutral valuation, backward induction, or calculating option values with discrete time periods (e.g., "2-step binomial model", "3-month periods", "calculate option value using binomial approach").

**Procedure:**
1. **Identify the time structure:**
   - Total option life (T)
   - Number of periods (n)
   - Per-period time step: Δt = T/n

2. **Calculate per-period parameters:**
   - Up factor: u (given or calculated from volatility)
   - Down factor: d (given or calculated from volatility)
   - Risk-free rate per period: use Δt, NOT T
   - Risk-neutral probability: p = (e^(r×Δt) - d)/(u - d)
   - **CRITICAL:** Always use Δt (period length) in the exponential, not T (total life)

3. **Build the price tree forward:**
   - Start with current asset price S₀
   - Calculate all possible prices at each node through maturity
   - At period i, prices range from S₀×u^i to S₀×d^i

4. **Calculate terminal option values:**
   - For calls: max(S_T - K, 0) at each terminal node
   - For puts: max(K - S_T, 0) at each terminal node

5. **Work backward through the tree:**
   - At each node, option value = e^(-r×Δt) × [p × V_up + (1-p) × V_down]
   - Continue until reaching the initial node
   - **CRITICAL:** Discount by one period (Δt), not the entire remaining time

6. **Verify dimensional consistency:**
   - Check that probabilities are between 0 and 1
   - Ensure all time parameters use consistent units (years, months, etc.)

**Example (sanitized):**
> **Scenario:** A 9-month European call option is priced using a 3-period binomial model. The risk-free rate is 8% per annum, u = 1.15, d = 0.90, current stock price is $50, and strike is $48.
>
> **Wrong approach:** Calculate p = (e^(0.08×0.75) - 0.90)/(1.15 - 0.90) using total option life of 0.75 years, then discount final values by e^(-0.08×0.75).
>
> **Correct approach:** 
> - Δt = 0.75/3 = 0.25 years per period
> - p = (e^(0.08×0.25) - 0.90)/(1.15 - 0.90) = (1.0202 - 0.90)/0.25 = 0.4808
> - Build 3-period tree: S₀=50, then {57.5, 45}, then {66.13, 51.75, 40.5}, then {76.04, 59.51, 46.58, 36.45}
> - Terminal call values: {28.04, 11.51, 0, 0}
> - Work backward period by period, discounting each step by e^(-0.08×0.25) = 0.9802
> - Period 2 values: {e^(-0.08×0.25)×[0.4808×28.04 + 0.5192×11.51], e^(-0.08×0.25)×[0.4808×11.51 + 0.5192×0], 0}
> - Continue to initial node

---

## Pattern 2: Answer Option Mapping Verification

**Description:** Correctly analyzing the financial concepts and identifying the right answer conceptually, but then selecting the wrong option letter due to misalignment between the analysis and the answer choices.

**When to Use:** Multiple-choice questions where you must evaluate several strategies, instruments, or scenarios and select which one meets specific criteria (e.g., "which swap captures the greatest benefit", "which position has the highest risk", "which strategy is most appropriate").

**Procedure:**
1. **Create an explicit mapping table before analysis:**
   - List each answer option with its letter
   - Write a brief identifier for what each option represents
   - Example format:
     ```
     Option A = Strategy 1 (description)
     Option B = Strategy 2 (description)
     Option C = Strategy 3 (description)
     ```

2. **Analyze each strategy/instrument independently:**
   - Evaluate Strategy 1 against the criteria
   - Evaluate Strategy 2 against the criteria
   - Evaluate Strategy 3 against the criteria
   - Record findings for each

3. **Identify which strategy meets the question criteria:**
   - Clearly state: "Strategy X [meets/does not meet] the criteria because..."
   - Use the strategy name/number, not the option letter yet

4. **Map back to option letters explicitly:**
   - State: "Strategy X corresponds to Option [Letter]"
   - Double-check the mapping against your initial table
   - Verify: "The question asks for [criteria], Strategy X satisfies this, Strategy X is Option [Letter]"

5. **Final verification:**
   - Re-read the question stem to confirm what is being asked
   - Confirm your selected option letter matches your conceptual answer
   - Check for negative phrasing ("least likely", "not appropriate", "worst")

**Example (sanitized):**
> **Scenario:** An investor believes interest rates will rise over the next year. Which position would be most appropriate?
> - Option A: Pay fixed in an interest rate swap
> - Option B: Receive fixed in an interest rate swap
> - Option C: Enter a currency swap
>
> **Wrong approach:** 
> - Analyze: "Paying fixed means receiving floating. If rates rise, floating payments increase, so this benefits the investor."
> - Conclude: "Receiving fixed is best" → Select Option B
> - **ERROR:** Confused "paying fixed" with "receiving fixed"
>
> **Correct approach:**
> - **Mapping table:**
>   ```
>   A = Pay fixed, receive floating
>   B = Receive fixed, pay floating  
>   C = Currency swap
>   ```
> - **Analysis:**
>   - Strategy "Pay fixed, receive floating": If rates rise, receive higher floating payments → BENEFITS from rate rise
>   - Strategy "Receive fixed, pay floating": If rates rise, pay higher floating payments → LOSES from rate rise
>   - Strategy "Currency swap": Not directly related to interest rate views
> - **Identify:** "Pay fixed, receive floating" benefits from rising rates
> - **Map back:** "Pay fixed, receive floating" = Option A
> - **Verify:** Question asks for "most appropriate" given rising rate view → Option A
> - **Answer:** A

---

## Pattern 3: Period vs. Total Time Parameter Confusion

**Description:** Using total time to maturity when per-period time steps are required, or vice versa, particularly in multi-step valuation models.

**When to Use:** Any calculation involving discrete time periods where both total time and period length appear (e.g., "quarterly periods over 2 years", "monthly rebalancing", "semi-annual compounding").

**Procedure:**
1. **Extract all time-related information:**
   - Total time horizon (T_total)
   - Frequency or number of periods (n or frequency description)
   - Calculate period length: Δt = T_total / n

2. **Categorize each formula parameter:**
   - **Per-period parameters:** discount factors, growth rates in recursive formulas, probability calculations
   - **Total-period parameters:** final maturity dates, cumulative returns, total time to expiration
   - Create a checklist: "This formula requires [per-period / total] time"

3. **Apply the correct time parameter:**
   - For exponential functions in per-period calculations: use Δt
   - For describing maturity or total duration: use T_total
   - For annualizing: convert using appropriate factor (Δt or 1/Δt)

4. **Dimensional analysis check:**
   - Verify units: if rate is "per annum" and time is in years, they must match
   - Check that probabilities and discount factors are reasonable (between 0 and 1)
   - Ensure periodic calculations compound correctly to total time

**Example (sanitized):**
> **Scenario:** Calculate the forward price of a commodity using a 4-period model over 1 year. The storage cost is 3% per annum, risk-free rate is 5% per annum.
>
> **Wrong approach:** 
> - Use F = S₀ × e^((r+c)×T) with T = 1 year for each period calculation
> - Results in over-compounding
>
> **Correct approach:**
> - Identify: 4 periods over 1 year → Δt = 0.25 years
> - Per-period growth: e^((0.05+0.03)×0.25) = e^0.02 = 1.0202
> - Apply recursively: F₁ = S₀ × 1.0202, F₂ = F₁ × 1.0202, etc.
> - Or equivalently for final value: F₄ = S₀ × e^((0.05+0.03)×1.0) using total time
> - **Key:** Use Δt for per-step calculations, T_total only for final endpoint

---

## Pattern 4: Backward Induction Execution Errors

**Description:** Failing to properly execute backward induction in multi-period valuation, including skipping nodes, using wrong discount factors, or not properly weighting probabilities.

**When to Use:** Questions requiring backward induction through trees or lattices (binomial trees, trinomial trees, dynamic programming in derivatives).

**Procedure:**
1. **Set up the complete tree structure:**
   - Draw or mentally map all nodes at each time step
   - Label each node with coordinates (time period, state)
   - Identify all terminal nodes

2. **Calculate terminal values first:**
   - Apply payoff function at maturity
   - Verify all terminal nodes have values
   - Check boundary conditions (e.g., option payoffs cannot be negative)

3. **Work backward one period at a time:**
   - Start at period T-1 (one period before maturity)
   - For each node at T-1, calculate value from connected nodes at T
   - Complete entire period T-1 before moving to T-2

4. **At each node, apply the valuation formula:**
   - Identify all possible next-period nodes (usually 2 for binomial)
   - Apply: V = e^(-r×Δt) × [p₁×V₁ + p₂×V₂ + ...]
   - For American options: compare with immediate exercise value
   - Record the calculated value at the node

5. **Maintain systematic progression:**
   - Never skip a period
   - Never skip a node within a period
   - Keep track of which nodes have been calculated
   - The final answer is the value at the initial node (t=0)

6. **Verification checks:**
   - Option values should generally decrease as you move backward (time value decays)
   - Values should be continuous (no sudden jumps between adjacent nodes)
   - Initial value should be reasonable relative to current asset price and strike

**Example (sanitized):**
> **Scenario:** Value a 2-period American put option with K=$100, S₀=$100, u=1.2, d=0.8, r=5%, Δt=0.5 years.
>
> **Wrong approach:**
> - Calculate some terminal values
> - Jump directly to initial node using only one path
> - Ignore intermediate nodes
>
> **Correct approach:**
> - **Period 2 (terminal) prices:** 144, 96, 64
> - **Period 2 put values:** max(100-144,0)=0, max(100-96,0)=4, max(100-64,0)=36
> - **Period 1 prices:** 120, 80
> - **Period 1 calculations:**
>   - At S=120: p=(e^0.025-0.8)/(1.2-0.8)=0.5631
>   - Hold value: e^(-0.025)×[0.5631×0 + 0.4369×4] = 1.70
>   - Exercise value: max(100-120,0) = 0
>   - Node value: max(1.70, 0) = 1.70
>   - At S=80: Hold value: e^(-0.025)×[0.5631×4 + 0.4369×36] = 17.54
>   - Exercise value: max(100-80,0) = 20
>   - Node value: max(17.54, 20) = 20 (exercise early)
> - **Period 0:**
>   - V₀ = e^(-0.025)×[0.5631×1.70 + 0.4369×20] = 9.48

---

SKILL_MD_ENTRY: | `derivatives/new_patterns.md` | Derivatives | Multi-Step Calculation and Answer Mapping Errors | Binomial Option Pricing, Answer Option Mapping Verification, Period vs Total Time Confusion, Backward Induction Execution |