# Derivatives — Binomial Model Mechanics

## Pattern: Multi-Period Binomial Tree Navigation

**Description:** When working with multi-period binomial trees, correctly identify which future states are reachable from a given current state by tracing valid paths through the tree structure. Conditional expectations are calculated as weighted averages of reachable future values, not as values at individual nodes.

**When to Use:** Questions involving conditional expectations, option pricing, or state-dependent calculations in binomial models with 2+ periods; keywords include "conditional on," "given state," "at time t," "backward induction."

**Procedure:**
1. Draw or visualize the complete binomial tree with all nodes labeled by time period and state
2. Identify the conditioning state (e.g., "given H at time 1" means starting from the H node at t=1)
3. From the conditioning node, trace forward exactly one period to identify all directly reachable states
4. For each reachable state, note the associated value (stock price, option payoff, etc.)
5. Use only these reachable values in subsequent calculations (expectations, pricing, etc.)
6. Calculate conditional expectations as weighted averages: E_t[X|state] = p̃×X(up) + q̃×X(down), using the reachable values
7. Verify that the number of reachable states matches the branching factor (typically 2 in binomial models)
8. **Critical check:** Confirm that your final answer is the calculated expectation (a weighted average), NOT a value from any single node in the tree

**Example (sanitized):**
> **Scenario:** A two-period binomial tree has S₀=100, with up factor u=1.2 and down factor d=0.9. Calculate E₁[S₂|Up at t=1] with p̃=0.6.
> **Wrong approach:** Reporting E₁[S₂|Up] = 144 (the value at the UU node) instead of calculating the expectation.
> **Correct approach:** From S₁(Up)=120, the reachable states are S₂(UU)=144 and S₂(UD)=108. Calculate the expectation: E₁[S₂|Up] = 0.6×144 + 0.4×108 = 129.6. This is a weighted average, not a single node value.

**Common Mistakes to Avoid:**
- Confusing individual node values with conditional expectations (expectations are weighted averages, not single values)
- Using values from unreachable states in conditional expectation calculations
- Reporting a node value when the question asks for an expectation

---
## Pattern: Risk-Neutral Pricing Formula Construction

**Description:** The risk-neutral pricing formula for a derivative must use the derivative's payoff values V(state), not the underlying asset's values S(state), and must include both the discounting factor and the risk-neutral expectation. When deriving the formula algebraically, recognize that multiplying equations by probabilities and adding them creates the expectation term.

**When to Use:** Questions asking to "write down the pricing formula," "express V₀ in terms of," "derive the no-arbitrage price," or asking about algebraic manipulation steps in deriving pricing formulas; context involves risk-neutral probabilities p̃ and q̃.

**Procedure:**
1. Identify what is being priced (the derivative V, not the underlying S)
2. **If deriving from equations:** Recognize that multiplying the first equation by p̃ and the second by q̃, then adding, creates a weighted sum p̃V₁(H) + q̃V₁(T)
3. **Identify this weighted sum as the risk-neutral expectation:** Ẽ[V₁] = p̃V₁(H) + q̃V₁(T)
4. Apply the discount factor: V₀ = (1+r)⁻¹ × Ẽ[V₁]
5. Combine into the complete formula: V₀ = (1+r)⁻¹[p̃V₁(H) + q̃V₁(T)]
6. **Special case check:** If V₁ = S₁ by definition (derivative replicates the underlying), recognize that V₀ must equal S₀ by the no-arbitrage principle
7. Verify that V appears in the formula, not S (unless V=S by definition, in which case V₀=S₀)
8. Check that both components are present: discount factor AND expectation term

**Example (sanitized):**
> **Scenario:** Given two equations from replication: V₀ = ΔS₀ + B and V₁(H) = ΔS₁(H) + B(1+r). Multiply the first by p̃ and second by q̃=1-p̃, then add. What function of V₁(H), V₁(T) results?
> **Wrong approach:** Stating the result is (1+r)S₀ or another expression involving S.
> **Correct approach:** 
> - Multiplying and adding creates: p̃V₁(H) + q̃V₁(T) (the expectation term)
> - This must be discounted: (1+r)⁻¹[p̃V₁(H) + q̃V₁(T)]
> - This is the complete risk-neutral pricing formula for V₀

**Example 2 (special case):**
> **Scenario:** Price a derivative where V₁ = S₁ (pays the stock price) using risk-neutral pricing.
> **Wrong approach:** V₀ = (1+r)⁻¹[p̃uS₀ + q̃dS₀] as the final answer.
> **Correct approach:** While the formula V₀ = (1+r)⁻¹[p̃S₁(H) + q̃S₁(T)] is correct, recognize that since this derivative replicates the stock, V₀ = S₀ by no-arbitrage. The formula simplifies to S₀.

**Common Mistakes to Avoid:**
- Using underlying prices S instead of derivative payoffs V in the pricing formula
- Forgetting the discount factor when writing the complete formula
- Not recognizing that p̃V₁(H) + q̃V₁(T) is the expectation term when deriving algebraically
- Missing the special case where V=S implies V₀=S₀
## Pattern: Multi-Period Backward Induction

**Description:** Option pricing in multi-period binomial models requires working backward from expiration, calculating option values at each node using the risk-neutral formula applied to the next period's values. All terminal nodes must be calculated first, then systematically work backward through each intermediate layer.

**When to Use:** Questions about option values before expiration in binomial models with 2+ periods; keywords include "two-period," "multi-step," "European option," "American option."

**Procedure:**
1. **Start at the final period (expiration):** Calculate terminal payoffs at ALL nodes in the final period
2. **Verify tree structure:** Identify whether the tree is recombining (UD = DU) or non-recombining, and count the total number of terminal nodes
3. **Move backward one period at a time:** Work through each layer systematically
4. **At each node in period t:** Calculate option value using V_t = (1+r)⁻¹[p̃V_{t+1}(up) + q̃V_{t+1}(down)]
5. **For American options:** Compare continuation value to immediate exercise value and take the maximum
6. **Continue backward until reaching time 0:** Process each intermediate layer completely before moving to the previous period
7. **The value at the root node is the option price:** V₀ is your final answer
8. **Verification check:** Ensure you've calculated values at all nodes in each period before moving backward

**Example (sanitized):**
> **Scenario:** A 2-period European call with strike K=100. Stock prices: S₀=100, S₁(U)=120, S₁(D)=80, S₂(UU)=144, S₂(UD)=96, S₂(DD)=64. Find V₀ with r=0.05 and p̃=0.6.
> **Wrong approach:** Calculating V₀ directly from terminal values without computing intermediate nodes.
> **Correct approach:** 
> - **Step 1 (Terminal payoffs):** V₂(UU)=44, V₂(UD)=0, V₂(DD)=0
> - **Step 2 (Period 1 nodes):** V₁(U) = (1.05)⁻¹[0.6×44 + 0.4×0] = 25.14; V₁(D) = (1.05)⁻¹[0.6×0 + 0.4×0] = 0
> - **Step 3 (Period 0):** V₀ = (1.05)⁻¹[0.6×25.14 + 0.4×0] = 14.37

**Common Mistakes to Avoid:**
- Skipping intermediate nodes and trying to price directly from terminal values
- Not calculating all terminal nodes before starting backward induction
- Forgetting to verify the tree structure (recombining vs. non-recombining)

---
## Pattern: Risk-Neutral Probability Calculation

**Description:** Risk-neutral probabilities are derived from the no-arbitrage condition, not from real-world probabilities, using the formula p̃ = (1+r-d)/(u-d) where u and d are the up and down factors.

**When to Use:** Questions requiring calculation of risk-neutral probabilities in binomial models; context includes interest rate r, up factor u, down factor d.

**Procedure:**
1. Identify the risk-free rate r (per period)
2. Identify the up factor u (S_up/S_current)
3. Identify the down factor d (S_down/S_current)
4. Calculate p̃ = (1+r-d)/(u-d)
5. Calculate q̃ = 1-p̃
6. Verify that 0 < p̃ < 1 (otherwise arbitrage exists)
7. Use these probabilities for all pricing calculations, ignoring any stated "real-world" probabilities

**Example (sanitized):**
> **Scenario:** Stock can go up by 15% or down by 10% each period. Risk-free rate is 3% per period. Find p̃.
> **Wrong approach:** Assuming p̃ = 0.5 or using historical frequency of up moves.
> **Correct approach:** u=1.15, d=0.90, r=0.03. Therefore p̃ = (1.03-0.90)/(1.15-0.90) = 0.13/0.25 = 0.52.

---

## Pattern: Binomial Tree State Labeling

**Description:** Properly label binomial tree nodes with both time index and state path to avoid confusion when identifying values for calculations.

**When to Use:** Any multi-period binomial problem; especially important when calculating conditional expectations or pricing path-dependent derivatives.

**Procedure:**
1. Label the initial node as S₀ or V₀
2. At time 1, label nodes as S₁(U) and S₁(D) for up and down states
3. At time 2, label nodes as S₂(UU), S₂(UD), S₂(DU), S₂(DD) based on the path taken
4. Note that in recombining trees, S₂(UD) = S₂(DU), but they represent different paths
5. When extracting values for calculations, use the state labels to ensure correct identification
6. For conditional expectations, only use states consistent with the conditioning path

**Example (sanitized):**
> **Scenario:** Calculate E₁[S₂|D] in a two-period tree where S₀=50, S₁(U)=60, S₁(D)=40, S₂(UU)=72, S₂(UD)=S₂(DU)=48, S₂(DD)=32.
> **Wrong approach:** Using all S₂ values: E₁[S₂|D] = 0.5×72 + 0.5×32 = 52.
> **Correct approach:** Given D at time 1 (S₁=40), only S₂(DU)=48 and S₂(DD)=32 are reachable. Therefore E₁[S₂|D] = 0.5×48 + 0.5×32 = 40.

---

## Pattern: Futures Contract Beta Adjustment

**Description:** When using futures to adjust portfolio beta, calculate the combined beta as a weighted average of the existing portfolio beta and the futures position beta, weighted by their respective market values.

**When to Use:** Questions about adjusting portfolio beta using futures contracts; keywords include "beta objective," "futures overlay," "target beta," "equity futures."

**Procedure:**
1. Identify the current portfolio value (V_portfolio) and its beta (β_portfolio)
2. Identify the futures position notional value (V_futures) and the futures beta (β_futures, typically ≈1 for equity index futures)
3. Calculate the beta-weighted contribution of the portfolio: V_portfolio × β_portfolio
4. Calculate the beta-weighted contribution of futures: V_futures × β_futures
5. Calculate the combined beta: β_combined = (V_portfolio × β_portfolio + V_futures × β_futures) / (V_portfolio + V_futures)
6. Compare β_combined to the target beta to determine if the objective is met
7. Note: For long futures, V_futures > 0; for short futures, V_futures < 0

**Example (sanitized):**
> **Scenario:** A $100M portfolio with β=0.8 wants to achieve β=1.0. They buy $25M notional of index futures (β=1.0). Is the target met?
> **Wrong approach:** Assuming the new beta is simply 1.0 because futures have β=1.0.
> **Correct approach:** β_combined = (100×0.8 + 25×1.0)/(100+25) = 105/125 = 0.84. The target of 1.0 is not met; beta is still below target.

---

## Pattern: Derivative vs. Underlying Payoff Distinction

**Description:** Clearly distinguish between the underlying asset's value S and the derivative's value V at each node; they are equal only in special cases (e.g., when the derivative is the underlying itself).

**When to Use:** Any derivative pricing problem; especially important when writing pricing formulas or calculating expectations.

**Procedure:**
1. Identify what is being priced: the derivative (V) or the underlying (S)
2. If pricing a derivative, determine its payoff function (e.g., max(S-K, 0) for a call)
3. Calculate the derivative's value at each node using its payoff function
4. Use V values (not S values) in the pricing formula
5. Only substitute V=S when the derivative's payoff equals the underlying by definition
6. Double-check that the formula uses the correct symbol (V or S) based on what is being priced

**Example (sanitized):**
> **Scenario:** Price a derivative that pays V₁(U)=10 and V₁(D)=4 when the underlying is S₁(U)=50 and S₁(D)=30.
> **Wrong approach:** V₀ = (1+r)⁻¹[p̃×50 + q̃×30] — uses underlying values.
> **Correct approach:** V₀ = (1+r)⁻¹[p̃×10 + q̃×4] — uses derivative payoffs.

---

## Pattern: Complete Formula Assembly

**Description:** When asked to write a pricing formula, include all components: discount factor, risk-neutral probabilities, and payoff values, assembled in the correct order.

**When to Use:** Questions asking to "write down," "express," or "derive" a pricing formula; often follows a derivation or algebraic manipulation.

**Procedure:**
1. Identify the time period being priced (typically t=0 for current price)
2. Identify the payment time (typically t=1 or expiration)
3. Write the discount factor: (1+r)⁻ⁿ where n is the number of periods
4. Write the risk-neutral expectation: [p̃×payoff(up) + q̃×payoff(down)]
5. Combine: Price = (1+r)⁻ⁿ[p̃×payoff(up) + q̃×payoff(down)]
6. Verify all components are present: discount, probabilities, and payoffs
7. Ensure the formula is self-contained (defines all variables or uses standard notation)

**Example (sanitized):**
> **Scenario:** After deriving equations for a one-period binomial model, write the formula for V₀.
> **Wrong approach:** V₀ = (1+r)⁻¹ — missing the expectation term.
> **Correct approach:** V₀ = (1+r)⁻¹[p̃V₁(H) + q̃V₁(T)] — includes both discount and expectation.

---

## Pattern: Conditional Expectation Time Indexing

**Description:** Conditional expectations are indexed by the time at which the conditioning information is known; E_t[X] means the expectation of X based on information available at time t.

**When to Use:** Questions involving conditional expectations with time subscripts; notation like E₁[S₂] or Ẽ_t[V_{t+1}].

**Procedure:**
1. Identify the time subscript on the expectation operator (e.g., E₁ means conditioning on time-1 information)
2. Identify the state at that conditioning time (e.g., "given H" or "given Up")
3. From that specific state at the conditioning time, identify all reachable states in the next period
4. Calculate the expectation using only those reachable states
5. Recognize that different conditioning states at the same time will yield different conditional expectations
6. Report all required conditional expectations separately (e.g., E₁[S₂|U] and E₁[S₂|D] are both needed)

**Example (sanitized):**
> **Scenario:** Find E₁[S₂|Up] and E₁[S₂|Down] where S₁(Up)=110, S₁(Down)=90, and from each state the stock can go up 10% or down 10%.
> **Wrong approach:** Calculating a single expectation E[S₂] = 0.25×121 + 0.5×99 + 0.25×81 = 100.
> **Correct approach:** E₁[S₂|Up] = 0.5×121 + 0.5×99 = 110 (from 110, can reach 121 or 99). E₁[S₂|Down] = 0.5×99 + 0.5×81 = 90 (from 90, can reach 99 or 81). Two separate values.

---

SKILL_MD_ENTRY: | `derivatives/binomial_mechanics.md` | Derivatives | Binomial Model Mechanics | Multi-Period Tree Navigation, Risk-Neutral Pricing Formula, Backward Induction, Risk-Neutral Probability Calculation, Futures Beta Adjustment, Derivative vs. Underlying Distinction, Conditional Expectation Time Indexing |