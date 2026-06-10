# Analysis of Failure Cases

## Pattern: Option Type Inference from Economic Context

**Description:** Questions may not explicitly state the option type (call vs. put) but instead provide economic context clues (e.g., "stock price falls," "exercised at lower price") that indicate which option type is being discussed. Models must infer the option type from the economic rationality of exercise decisions rather than defaulting to the most recently mentioned or more common option type.

**When to Use:** When a question describes option exercise scenarios without explicitly stating "call" or "put," especially when mentioning stock price movements (rising/falling) or exercise at prices significantly different from current market prices.

**Procedure:**
1. Identify whether the question explicitly names the option type (call/put) or only describes an exercise scenario
2. If not explicit, extract economic context clues:
   - "Stock price falls" + exercise → likely PUT option
   - "Stock price rises" + exercise → likely CALL option
   - Exercise at price BELOW current market → likely PUT option
   - Exercise at price ABOVE current market → likely CALL option
3. Apply the economic rationality test: which option type would make exercise profitable in the described scenario?
   - Call options are exercised when stock price > strike price
   - Put options are exercised when stock price < strike price
4. Cross-reference with any tables or context to determine which option type's data should be used
5. Verify: does the inferred option type make economic sense given the described profit/loss outcome?

**Example (sanitized):**
> **Scenario:** A question states "if the stock price drops to $50 and the option is exercised, calculate the gain" when current stock price is $75 and strike prices of $60, $70, $80 are available.
> **Wrong approach:** Assuming it's a call option because calls were discussed earlier, then incorrectly stating the option wouldn't be exercised since $50 < strike prices.
> **Correct approach:** (1) Note "stock price drops" and "exercised at $50" (below current $75), (2) recognize this is economically rational only for a PUT option, (3) select appropriate put option data (e.g., strike $70), (4) calculate gain = $70 - $50 = $20 per share minus premium paid.

---

## Pattern: Compound Option Target Disambiguation

**Description:** Questions about compound options (options on options) involve multiple layers: the underlying asset, the base option, and the compound option itself. When asked about relationships between different compound option types, models must carefully parse which specific combination is being asked about (e.g., "call on put" vs. "call on call") rather than defaulting to previously discussed combinations.

**When to Use:** When questions involve compound options and ask about relationships, formulas, or parity conditions between different compound option types. Trigger phrases: "call on a put," "put on a put," "call on a call," "put on a call," "compound option."

**Procedure:**
1. Identify all option layers mentioned in the question:
   - Layer 1: Underlying asset (stock, index, etc.)
   - Layer 2: Base option type (call or put)
   - Layer 3: Compound option type (call or put on the base option)
2. Parse the question target carefully, word by word:
   - "call on a put" = compound call option where the underlying is a put option
   - "put on a put" = compound put option where the underlying is a put option
   - Note: "on a X" specifies what the base option is
3. Do NOT assume the question asks about the most recently discussed or most common compound option type
4. Map the question's specific compound option types to the correct formulas or relationships
5. Verify: does your answer address the exact compound option combination stated in the question?

**Example (sanitized):**
> **Scenario:** After discussing call-on-call options extensively, a question asks "What is the put-call parity for options on a put option?"
> **Wrong approach:** Providing the parity relationship for call-on-call and put-on-call because those were just discussed.
> **Correct approach:** (1) Identify the question asks about "options on a put," (2) recognize this means both the call and put in the parity are compound options with a PUT as the underlying, (3) use notation where the base option is a put (not a call), (4) derive or state the parity: call-on-put minus put-on-put equals the discounted difference between put price and strike.

---

## Pattern: Perspective Identification in Options Scenarios

**Description:** Options questions can be asked from either the option holder's (buyer's) perspective or the option writer's (seller's) perspective, and these have opposite payoff structures. Contextual clues such as "is able to buy shares at [strike]" (writer's obligation) vs. "has the right to buy" (holder's right) indicate which perspective the question adopts.

**When to Use:** When questions describe option exercise outcomes, profits, or losses without explicitly stating "option holder" or "option writer." Look for phrases describing obligations, being assigned, or specific transaction mechanics.

**Procedure:**
1. Scan the question and context for perspective indicators:
   - Holder/buyer perspective: "has the right to," "exercises the option," "decides to exercise," "profit from exercising"
   - Writer/seller perspective: "is obligated to," "must sell/buy," "is able to buy at [strike] and sell at [market]," "assignment"
2. Identify the cash flow direction described:
   - If the scenario describes buying at strike and selling at market → likely writer's perspective (for calls)
   - If the scenario describes selling at strike after buying at market → likely writer's perspective (for puts)
3. Check for specific numerical examples in ground truth or context that reveal the perspective:
   - "Trader is able to buy 100 shares at $X" suggests writer who must deliver shares
4. Apply the correct payoff formula for the identified perspective:
   - Holder: max(payoff, 0) - premium paid
   - Writer: premium received - max(payoff, 0)
5. Verify: does the profit/loss direction match the expected outcome for the identified perspective?

**Example (sanitized):**
> **Scenario:** "If the stock reaches $120 and the option is exercised, the trader buys shares at $100 and sells them at $120. What is the outcome?"
> **Wrong approach:** Assuming this is the option holder exercising their right, calculating $20 profit minus premium.
> **Correct approach:** (1) Recognize "buys at strike and sells at market" describes the writer's obligation when assigned, (2) identify this is a call writer who must deliver shares, (3) calculate writer's loss = ($120 - $100) × shares - premium received, (4) note the writer has a loss on the stock transaction partially offset by premium.

---

## Pattern: Specific Strike Price Selection from Context

**Description:** When questions provide option pricing tables with multiple strike prices and maturities but don't explicitly specify which option to analyze, models must use contextual clues (previous examples, specific scenarios, or the most relevant/illustrative case) rather than arbitrarily selecting or analyzing all options generically.

**When to Use:** When a question references "the option" or describes a specific scenario (e.g., exercise at a particular stock price) but multiple options are available in the provided tables.

**Procedure:**
1. Check if the question or immediately preceding context specifies a particular strike price, maturity, or option contract
2. If not explicit, look for contextual anchors:
   - A specific stock price mentioned for exercise → select strike price(s) that make economic sense for that scenario
   - Reference to "the option" after a specific example → use that example's parameters
   - Calculation of specific dollar amounts in ground truth → work backward to identify which strike/premium combination produces those amounts
3. When multiple options could apply, prioritize:
   - At-the-money or near-the-money options (strike closest to current stock price) for general examples
   - The option that makes the described scenario most illustrative (e.g., highest strike for maximum loss scenarios)
4. If truly ambiguous, state assumptions clearly: "Using the $X strike option as an example..."
5. Verify: do the numerical results match any specific amounts mentioned in the question or expected answer format?

**Example (sanitized):**
> **Scenario:** Tables show put options with strikes $80, $90, $100 on a stock trading at $95. Question asks "If the stock falls to $70 and the option is exercised, what is the gain?" Ground truth shows a specific dollar amount like "$2,500."
> **Wrong approach:** Generically stating "the gain depends on which option was purchased" without calculating specific values.
> **Correct approach:** (1) Note the ground truth implies a specific option, (2) work backward: $2,500 gain suggests ($100 - $70) × 100 shares = $3,000 intrinsic value minus $500 premium, (3) check tables for $100 strike put with ~$5 premium, (4) provide the specific calculation for that option.