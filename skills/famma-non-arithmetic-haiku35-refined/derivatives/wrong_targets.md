# Skill Patterns for Derivatives Wrong Target Errors

## Pattern: Distinguishing Derivative Payoff from Underlying Asset Price

**Description:** Models confuse the derivative security's payoff function V(·) with the underlying asset's price S(·), leading to incorrect formula substitution when pricing derivatives.

**When to Use:** When questions ask for derivative pricing formulas, risk-neutral valuation, or replication strategies. Trigger keywords: "derivative security," "payoff," "option value," "pricing formula."

**Procedure:**
1. Identify whether the question asks about the underlying asset (stock, bond) or a derivative written on that asset
2. Recognize that derivative payoffs V₁(H) and V₁(T) are FUNCTIONS of underlying prices S₁(H) and S₁(T), not the prices themselves
3. When applying risk-neutral pricing, use V₁(·) for derivative payoffs, not S₁(·)
4. Verify: if the question mentions "derivative security that pays V₁" or "option with payoff," the formula must contain V terms, not S terms
5. Check that your answer addresses the derivative's value, not the underlying asset's expected price

**Example (sanitized):**
> **Scenario:** Given a binomial model with stock prices 120 (up) and 80 (down), price a call option with strike 100 using risk-neutral probabilities π=0.6, (1-π)=0.4, and interest rate r=0.05.
> **Wrong approach:** C₀ = (1/1.05)[0.6×120 + 0.4×80] = 100.95 (using stock prices directly)
> **Correct approach:** First compute payoffs: V₁(up) = max(120-100, 0) = 20, V₁(down) = max(80-100, 0) = 0. Then C₀ = (1/1.05)[0.6×20 + 0.4×0] = 11.43 (using derivative payoffs)

---

## Pattern: Identifying Multiple Conditional Expectations as Separate Targets

**Description:** When questions ask for conditional expectations given different information sets or states, models incorrectly return a single value instead of recognizing that each conditioning state requires a separate answer.

**When to Use:** When questions contain multiple conditioning scenarios (e.g., "given H" and "given T"), use plural forms ("expectations"), or ask for state-dependent values. Trigger keywords: "conditional expectation," "based on information at time t," "E[·](H), E[·](T)."

**Procedure:**
1. Parse the question for ALL distinct conditioning states or information sets mentioned
2. Count how many separate values are requested (look for notation like E[·](H), E[·](T) or multiple scenarios listed)
3. For each conditioning state, compute the expectation independently using only paths consistent with that state
4. Format the answer to include ALL requested values, clearly labeled by their conditioning state
5. Verify: the number of values in your answer matches the number of distinct conditioning states in the question

**Example (sanitized):**
> **Scenario:** In a two-period model, compute E[X₂|ω₁] where ω₁ can be state A or state B.
> **Wrong approach:** E[X₂|ω₁] = 0.5×15 + 0.5×5 = 10 (returning single value)
> **Correct approach:** E[X₂|A] = 0.5×15 + 0.5×7 = 11, and E[X₂|B] = 0.5×5 + 0.5×3 = 4. Answer: E[X₂|A]=11, E[X₂|B]=4 (two separate values)

---

## Pattern: Distinguishing Formula Structure from Specific Applications

**Description:** Models confuse the general form of a formula (the operator or structure) with a specific result obtained by applying that formula to particular inputs, especially when questions ask "what is the function" versus "what is the value."

**When to Use:** When questions ask for "the formula," "the function," "the expression," or "write down" a relationship. Trigger keywords: "what is it exactly," "write down," "the formula for," "express as."

**Procedure:**
1. Determine if the question asks for a FORMULA/EXPRESSION (symbolic form with variables) or a COMPUTED VALUE (numerical result)
2. If asking for a formula: identify all free variables that should remain symbolic in the answer
3. If the question references "previous equations" or "general case," ensure your answer maintains the same level of generality
4. Do not substitute specific values or simplify to a special case unless explicitly requested
5. Verify: if the question says "function of X, Y," your answer must contain X and Y as variables, not replaced with specific instances

**Example (sanitized):**
> **Scenario:** Multiply equation (1) by weight w and equation (2) by (1-w), then add them. What function of A and B results?
> **Wrong approach:** Returning "5" (a specific numerical result from substituting particular values)
> **Correct approach:** w×A + (1-w)×B (the general weighted sum expression maintaining variables A and B)

---

## Pattern: Matching Option Type Across Compound Structures

**Description:** In compound options (options on options), models fail to track whether the underlying option is a call or put, leading to incorrect parity relationships or formula selection when the question specifies different combinations.

**When to Use:** When dealing with compound options, nested derivatives, or parity relationships involving multiple option types. Trigger keywords: "call on a call," "put on a put," "call on a put," "compound option."

**Procedure:**
1. Parse the question to identify BOTH levels: (a) the outer option type (call or put), (b) the inner/underlying option type (call or put)
2. Create a clear notation: write "outer(inner)" to track the structure (e.g., "call on put" vs "call on call")
3. When applying formulas or parity relationships, verify that both the outer and inner types match the question's specification
4. For parity relationships, check that the underlying option variable (e.g., p for call, p' for put) corresponds to the correct option type
5. Before finalizing, re-read the question and confirm your answer addresses the exact combination requested

**Example (sanitized):**
> **Scenario:** Given put-call parity for a call on a call: cc + K₁e^(-rT) = pc + c, derive the relationship for a call on a put.
> **Wrong approach:** Using the same formula with c (call price) as the underlying
> **Correct approach:** Replace c with p (put price) since the underlying is now a put: cp_put + K₁e^(-rT) = pp_put + p, where p is the underlying put price

---

## Pattern: Verifying Arithmetic in Weighted Averages

**Description:** When computing expectations or weighted averages with given probabilities, models make arithmetic errors in multiplication or addition, particularly when probabilities are 0.5 or simple fractions.

**When to Use:** When calculating expected values, risk-neutral expectations, or any probability-weighted sums. Trigger keywords: "expectation," "weighted average," "probability," "E[·]."

**Procedure:**
1. Write out the full expectation formula explicitly: E[X] = p₁×x₁ + p₂×x₂ + ...
2. Perform each multiplication separately and write intermediate results
3. Sum the products step-by-step, showing each addition
4. Double-check arithmetic: for p=0.5, verify that 0.5×a + 0.5×b = (a+b)/2
5. Verify the final result makes intuitive sense (e.g., should be between min and max values if probabilities are positive)

**Example (sanitized):**
> **Scenario:** Compute E[Y] where Y=20 with probability 0.5 and Y=6 with probability 0.5.
> **Wrong approach:** E[Y] = 0.5×20 + 0.5×6 = 10 + 3 = 8 (arithmetic error)
> **Correct approach:** E[Y] = 0.5×20 + 0.5×6 = 10 + 3 = 13, or equivalently (20+6)/2 = 26/2 = 13