# Skill Patterns for Derivatives Concept Confusion Errors

## Pattern: Currency Pair Reciprocity and Hedging Direction

**Description:** Failure to recognize that options on reciprocal currency pairs (e.g., EUR/GBP vs GBP/EUR) provide equivalent hedging outcomes when properly structured, and confusion about which direction protects against which currency movement.

**When to Use:** When evaluating currency hedging strategies involving options on different currency pair quotations (e.g., "short EUR position," "EUR/GBP vs GBP/EUR options").

**Procedure:**
1. Identify the underlying exposure: determine which currency you are long/short
2. Determine the risk direction: a short EUR position (long GBP) loses when EUR strengthens (GBP weakens)
3. Recognize reciprocal equivalence: a call on GBP/EUR (right to buy EUR with GBP) = put on EUR/GBP (right to sell EUR for GBP)
4. For each hedging instrument, verify it provides protection in the loss scenario identified in step 2
5. Test all strategies systematically rather than dismissing options based on superficial differences in quotation

**Example (sanitized):**
> **Scenario:** An investor has a short position in Japanese yen (JPY) and considers three hedges: (1) forward contract selling USD/JPY, (2) buying a USD/JPY call option, (3) buying a JPY/USD put option.
> **Wrong approach:** Dismissing strategy 3 as "less directly aligned" because it's quoted in the reciprocal currency pair.
> **Correct approach:** Short JPY means long USD exposure, which loses if JPY strengthens. Strategy 1: forward locks in rate ✓. Strategy 2: USD/JPY call protects if JPY weakens (wrong direction) ✗. Strategy 3: JPY/USD put = right to sell JPY for USD at fixed rate = protects if JPY strengthens ✓. Strategies 1 and 3 hedge correctly.

---

## Pattern: Option Exercise Logic and Payoff Asymmetry

**Description:** Confusion about when options are exercised (calls when S > K, puts when S < K) and which option type is relevant for a given price movement scenario, leading to incorrect loss calculations.

**When to Use:** When analyzing option exercise decisions, calculating losses/gains from option positions, or determining which option type applies to a specific market scenario (trigger: "if stock price falls/rises," "option is exercised when").

**Procedure:**
1. Identify the price movement direction in the scenario (stock rises/falls relative to strike)
2. Determine which option type would be exercised in that scenario: calls exercised only when S > K (buy below market), puts exercised only when S < K (sell above market)
3. If the scenario involves a price below the strike, only put options are relevant for exercise analysis
4. Calculate loss as: premium paid + (intrinsic loss if exercised) for the correct option type
5. Verify: never apply call option logic to scenarios where price < strike, and vice versa

**Example (sanitized):**
> **Scenario:** An investor considers a $50 strike option. If the stock falls to $40 and an option is exercised, what is the loss?
> **Wrong approach:** Using a call option premium ($8) and calculating loss as $8 + ($50 - $40) = $18, assuming the call would be exercised.
> **Correct approach:** At $40 (below $50 strike), only a put option would be exercised. If a put was purchased for $6 premium, the loss is the premium paid ($6) since the put provides protection. A call option at $40 would simply expire worthless (loss = $8 premium only). The question context determines which option type is being analyzed.

---

## Pattern: Interest Rate Swap Impact on Market Value vs Cash Flow Risk

**Description:** Misunderstanding that converting floating-rate debt to fixed-rate via swaps has asymmetric effects: it reduces cash flow risk but INCREASES market value risk, not reduces both.

**When to Use:** When evaluating the risk management impact of interest rate swaps on floating-rate liabilities (trigger: "swap to convert floating to fixed," "market value risk," "cash flow risk").

**Procedure:**
1. Identify the original liability structure (floating-rate debt has minimal market value sensitivity to rate changes)
2. Understand cash flow risk: floating-rate payments create uncertainty → pay-fixed swap REDUCES this by fixing payments ✓
3. Understand market value risk: floating-rate debt has low duration/rate sensitivity → converting to fixed INCREASES duration → INCREASES market value risk ✗
4. Recognize the asymmetry: swaps reduce ONE type of risk while increasing the OTHER
5. Verify: a pay-fixed/receive-floating swap does NOT reduce market value risk for a floating-rate borrower

**Example (sanitized):**
> **Scenario:** A company has $100M floating-rate debt (LIBOR + 1%) and enters a 5-year pay-fixed (4%) receive-LIBOR swap.
> **Wrong approach:** Claiming the swap reduces both market value risk and cash flow risk because it "stabilizes" the position.
> **Correct approach:** Cash flow risk: floating payments are now fixed at 5% (4% swap + 1% spread) → uncertainty eliminated → REDUCED ✓. Market value risk: original floating debt had ~zero duration; swap adds ~4.5 years duration → position now sensitive to rate changes → INCREASED ✗. The swap trades cash flow certainty for market value exposure.

---

## Pattern: Covered Call vs Protective Put Floor Establishment

**Description:** Confusion about which option strategies provide true downside protection: protective puts create a definitive floor by guaranteeing a minimum sale price, while covered calls only provide limited downside cushion equal to the premium received and do NOT protect against significant losses—they are income-generation strategies, not loss-protection strategies.

**When to Use:** When evaluating option strategies for downside protection, assessing claims about "protecting gains," or comparing covered calls vs protective puts (trigger: "covered call," "protective put," "protect gains," "downside protection," "hedge against losses").

**Procedure:**
1. Identify the baseline position (e.g., long stock) and the option overlay being considered
2. For covered calls (long stock + short call): recognize this provides only premium income as cushion, leaves most downside exposed, and caps upside—it is NOT a protection strategy
3. For protective puts (long stock + long put): recognize this guarantees a minimum sale price (strike price) regardless of how far the stock falls—this IS true protection
4. When evaluating "protection" claims, check if the strategy establishes a floor value (protective put does, covered call does not)
5. Distinguish between income generation (covered call) and loss protection (protective put) as fundamentally different objectives

**Example (sanitized):**
> **Scenario:** An investor holds shares worth $100 and wants to "protect gains." Advisor suggests: (A) covered calls provide protection by limiting losses, or (B) protective puts provide protection but require premium payment.
> **Wrong approach:** Accepting that covered calls "provide protection" because they generate premium income and limit some risk.
> **Correct approach:** (1) Covered call (long stock + short call) generates premium but leaves investor exposed to losses below (stock price - premium); if stock falls to $50, investor loses ~$50 minus small premium. (2) Protective put (long stock + long put at $95 strike) guarantees minimum value of $95 regardless of stock price. (3) Only protective put provides true "protection of gains"—covered call is income strategy, not protection strategy. (4) Advisor is incorrect about covered calls.

---
## Pattern: Piecewise Function Continuity at Boundary Conditions

**Description:** Failure to recognize that well-defined piecewise pricing formulas (like barrier options with H≤K vs H≥K) must be continuous at boundary points, meaning both formulas yield identical values when evaluated at the boundary.

**When to Use:** When comparing two different formulas that apply to different parameter ranges with a shared boundary point (trigger: "two formulas," "when H = K," "H ≤ K vs H ≥ K").

**Procedure:**
1. Identify the boundary condition where the two formula domains meet (e.g., H = K)
2. Recognize that properly constructed piecewise functions in finance must be continuous (no jumps in value)
3. Substitute the boundary value into both formulas
4. Simplify each expression algebraically at the boundary
5. Verify that both formulas produce the same numerical result at the boundary (if not, there's an arbitrage opportunity or formula error)

**Example (sanitized):**
> **Scenario:** A derivative has pricing formula F₁ when X ≤ 100 and formula F₂ when X ≥ 100. Question: Are F₁ and F₂ equal when X = 100?
> **Wrong approach:** Claiming they are different because they use "different mathematical approaches" for different conditions.
> **Correct approach:** At X = 100 (the boundary), both formulas must apply simultaneously. For no-arbitrage, the derivative cannot have two different prices at the same parameter value. Substitute X = 100 into both F₁ and F₂; if properly constructed, they will simplify to identical values. This continuity is required for well-defined pricing functions.

---

## Pattern: Numeraire Change and Correlation-Adjusted Risk Pricing

**Description:** Failure to recognize that changing numeraire (especially to foreign currency bonds) requires incorporating correlation-weighted volatility components from all risk sources affecting the asset-numeraire ratio, not just the asset's own drift.

**When to Use:** When changing pricing measure to a foreign currency zero-coupon bond numeraire or analyzing cross-currency derivative pricing (trigger: "numeraire equal to," "currency B bond," "market price of risk in new measure").

**Procedure:**
1. Identify all stochastic components: asset price process, exchange rate process, foreign bond price process
2. Recognize that the new measure's market price of risk must account for how each component affects the asset/numeraire ratio
3. Include correlation terms: market price of risk = Σ(ρᵢⱼ σⱼ) for all correlated risk sources
4. For foreign bond numeraire: include both exchange rate risk (ρ_FX σ_FX) and foreign bond price risk (ρ_bond σ_bond)
5. Verify: this is NOT a simple single-currency adjustment; multi-dimensional risk structure must be preserved

**Example (sanitized):**
> **Scenario:** Asset S (in currency A) follows dS = μS dt + σS dz. Find market price of risk when numeraire is a currency B zero-coupon bond.
> **Wrong approach:** Calculating λ = (μS - rB)/σS as if it's a simple single-currency risk adjustment.
> **Correct approach:** The asset/numeraire ratio involves: (1) S dynamics in currency A, (2) exchange rate A/B dynamics, (3) currency B bond price dynamics. Market price of risk must include: λ = ρ_SQ σ_Q + ρ_SF σ_F, where Q represents bond price risk and F represents FX risk. Each correlation-weighted volatility component contributes to the total risk premium in the new measure.

---

## Pattern: Short Straddle Greek Signature Recognition

**Description:** Misidentifying option strategies by focusing on individual Greeks rather than recognizing that a short straddle's defining characteristic is SMALL/near-zero delta (from offsetting call/put deltas) combined with negative gamma, positive theta, and negative vega.

**When to Use:** When identifying option strategies from Greek exposures, especially distinguishing short straddles from other short volatility strategies (trigger: "Greek exposures," "straddle," "delta/gamma/theta/vega signs").

**Procedure:**
1. Recall short straddle structure: sell ATM call + sell ATM put at same strike
2. Identify the delta signature: short call (negative delta) + short put (positive delta) ≈ near-zero or SMALL net delta (key distinguishing feature)
3. Verify other Greeks for short straddle: negative gamma (short options), positive theta (time decay benefit), negative vega (short volatility)
4. Compare delta magnitude: "positive delta" suggests directional bias (not a straddle); "small delta" suggests balanced offsetting (straddle characteristic)
5. Eliminate strategies with large positive/negative delta as they cannot be straddles

**Example (sanitized):**
> **Scenario:** Three strategies show Greeks: (X) delta=+0.6, gamma=-0.3, theta=+0.5, vega=-0.8; (Y) delta=+0.05, gamma=-0.4, theta=+0.6, vega=-0.9; (Z) delta=-0.5, gamma=-0.2, theta=+0.4, vega=-0.7.
> **Wrong approach:** Selecting X because "positive theta and negative vega indicate short options."
> **Correct approach:** Short straddle requires near-zero delta from offsetting positions. X has delta=+0.6 (directional bias, likely ratio spread or short put-heavy). Y has delta=+0.05 (small, near-zero) with negative gamma, positive theta, negative vega → matches short straddle ✓. Z has delta=-0.5 (directional, likely short call-heavy). Answer: Y.

---

## Pattern: Duration Matching in Interest Rate Hedging

**Description:** Failure to match the duration/maturity of the hedging instrument to the hedged asset, leading to ineffective hedges when short-term rate instruments are used to hedge long-term rate exposure.

**When to Use:** When selecting interest rate hedging instruments for bonds or rate-sensitive positions (trigger: "hedge 10-year bond," "interest rate futures," "Eurodollar futures," "bond futures").

**Procedure:**
1. Identify the duration/maturity of the asset being hedged (e.g., 10-year Treasury bond)
2. Recognize that effective hedging requires sensitivity to the SAME segment of the yield curve
3. Match instrument to exposure: long-term bonds → hedge with bond futures or long-term swaps; short-term rates → hedge with Eurodollar or short-term instruments
4. Evaluate each option: 90-day Eurodollar futures hedge short-term rate risk (ineffective for 10-year bond); bond futures hedge long-term rate risk (effective for 10-year bond)
5. Verify: duration mismatch creates basis risk and reduces hedge effectiveness

**Example (sanitized):**
> **Scenario:** A portfolio manager holds a 7-year corporate bond (duration 6.2) and expects rates to rise. Options: (A) sell bond futures (duration ~8), (B) enter receive-fixed 7-year swap, (C) sell 90-day Eurodollar futures.
> **Wrong approach:** Selecting C because "Eurodollar futures hedge interest rate risk and are liquid."
> **Correct approach:** The 7-year bond is sensitive to long-term rates. Option A: bond futures have similar duration → effective hedge ✓. Option B: 7-year swap duration matches bond → effective hedge ✓. Option C: 90-day Eurodollar futures hedge short-term rate changes; when long-term rates rise, short-term rates may not move proportionally → duration mismatch → ineffective hedge ✗. Answer: A or B.

---

## Pattern: Swap Payoff Evaluation Under Relative Performance Expectations

**Description:** Failure to correctly evaluate which swap strategy captures economic benefit by not systematically checking whether each swap's receive leg outperforms its pay leg under the stated market view.

**When to Use:** When evaluating swap strategies based on relative performance forecasts between indices and rates (trigger: "swap strategies," "receive/pay," "market view that X will outperform Y").

**Procedure:**
1. Clearly state the market view with inequality relationships (e.g., small-cap > Libor > mid-cap)
2. For each swap, identify what you receive and what you pay
3. Determine the expected outcome: receive leg performance - pay leg performance
4. Positive outcome = profit from view; negative outcome = loss from view
5. Identify which swap has the LEAST benefit (most negative or least positive outcome)
6. Verify by checking all three relationships systematically

**Example (sanitized):**
> **Scenario:** Market view: Index A will return 8%, Index B will return 3%, Libor will be 5%. Three swaps: (1) receive Libor, pay Index B; (2) receive Index B, pay Index A; (3) receive Index A, pay Libor.
> **Wrong approach:** Dismissing swap 1 as "least aligned" without calculating expected payoffs.
> **Correct approach:** Swap 1: receive 5% - pay 3% = +2% benefit ✓. Swap 2: receive 3% - pay 8% = -5% loss ✗ (loses when A outperforms B as expected). Swap 3: receive 8% - pay 5% = +3% benefit ✓. Swap 2 has the least (most negative) benefit under the stated view. Answer: Swap 2.

---

## Pattern: Swaption Exercise and Net Rate Calculation with Loan Spreads

**Description:** Confusion about how swaption exercise affects net borrowing costs, specifically failing to recognize that the swap hedges only the floating rate component (e.g., LIBOR) and does NOT eliminate the credit spread on the underlying loan.

**When to Use:** When calculating net interest payments after swaption exercise on floating-rate loans with spreads (trigger: "payer swaption," "net interest payment," "LIBOR + spread," "excluding swaption premium").

**Procedure:**
1. Identify the original loan structure: floating rate (e.g., LIBOR) + fixed credit spread
2. Understand payer swaption mechanics: gives right to enter swap paying fixed rate, receiving floating rate
3. When exercised, calculate the net position: (pay fixed on swap) + (receive LIBOR on swap) + (pay LIBOR + spread on loan)
4. Simplify: LIBOR terms cancel → net payment = fixed swap rate + loan spread
5. Verify: the swaption does NOT eliminate the credit spread; net rate ≠ swap rate alone

**Example (sanitized):**
> **Scenario:** Company borrows at LIBOR + 0.75%. Purchases payer swaption with 4% exercise rate, receive LIBOR. If exercised, what is the net rate (excluding premium)?
> **Wrong approach:** Claiming net rate = 4% because "the swap fixes the rate at 4%."
> **Correct approach:** Original loan: pay LIBOR + 0.75%. Swap when exercised: pay 4% fixed, receive LIBOR. Combined position: pay 4% (swap) + receive LIBOR (swap) + pay LIBOR (loan) + pay 0.75% (loan spread) = pay 4% + 0.75% = 4.75% net rate. The 0.75% credit spread remains. Answer: 4.75%, not 4%.

---

## Pattern: No-Arbitrage Equivalence for Identical Payoffs

**Description:** Failure to recognize that when a derivative's payoff is identical to the underlying asset itself, the no-arbitrage principle requires them to have the same price, superseding formula-based calculation.

**When to Use:** When valuing derivatives whose payoffs exactly replicate the underlying asset or when asked to price V₁ = S₁ (trigger: "derivative security pays off the stock price," "V₁ = S₁," "European call with K = 0").

**Procedure:**
1. Identify the derivative's payoff structure at maturity (e.g., V₁ = S₁)
2. Compare to the underlying asset's payoff (S₁)
3. Recognize identical payoffs → must have identical prices to prevent arbitrage
4. Apply no-arbitrage logic: if V₀ < S₀, buy derivative and short stock (risk-free profit); if V₀ > S₀, short derivative and buy stock (risk-free profit)
5. Conclude: V₀ = S₀ without needing to apply risk-neutral pricing formulas
6. Verify: this principle overrides mechanical formula application when payoffs are identical

**Example (sanitized):**
> **Scenario:** In a binomial model, a derivative pays V₁ = 2S₁ (twice the stock price) at maturity. Stock is currently $50. What is V₀?
> **Wrong approach:** Applying risk-neutral pricing formula: V₀ = (1+r)⁻¹[p·V₁(H) + q·V₁(T)] with specific probabilities.
> **Correct approach:** The derivative payoff V₁ = 2S₁ is exactly twice the stock payoff in ALL states. By no-arbitrage, holding 2 shares replicates the derivative perfectly. Therefore, V₀ = 2S₀ = 2($50) = $100. No need for risk-neutral probabilities; the replication argument gives the price directly.

---

## Pattern: Traditional vs Foreign Risk-Neutral Measure Distinction

**Description:** Incorrectly generalizing that "traditional risk-neutral world" always means zero market price of risk, without recognizing that when the numeraire is a foreign currency instrument, the market price of risk includes non-zero correlation and volatility terms.

**When to Use:** When changing to risk-neutral measures with different numeraires, especially foreign currency bonds (trigger: "traditional risk-neutral world for currency B," "market price of risk," "numeraire").

**Procedure:**
1. Distinguish between domestic traditional risk-neutral (numeraire = domestic money market) and foreign risk-neutral (numeraire = foreign currency instrument)
2. In domestic traditional risk-neutral: market price of risk = 0 for all variables ✓
3. In foreign currency numeraire measure: market price of risk ≠ 0; includes correlation terms between asset and exchange rate/foreign rates
4. Apply Girsanov theorem correctly: drift adjustment depends on numeraire choice
5. For foreign bond numeraire: market price of dz-risk = ρ_exchange·σ_exchange (not zero)

**Example (sanitized):**
> **Scenario:** Asset in USD follows dS = 0.08S dt + 0.2S dz. Find market price of risk in EUR risk-neutral world (numeraire = EUR zero-coupon bond).
> **Wrong approach:** "In risk-neutral world, market price of risk = 0 for all variables."
> **Correct approach:** This is NOT the traditional (USD) risk-neutral world. The numeraire is a EUR bond, making this a foreign currency measure. The market price of dz-risk must account for USD/EUR exchange rate correlation: λ = ρ_S,FX · σ_FX, where FX is the USD/EUR rate. If ρ = 0.6 and σ_FX = 0.15, then λ = 0.6 × 0.15 = 0.09, not zero.

## Pattern: Swap Direction for Portfolio Rebalancing

**Description:** Failure to recognize that swaps modify existing portfolio allocations, requiring opposite positions to the desired change: to reduce exposure to an asset class, pay that asset's return (synthetic short); to increase exposure, receive that asset's return (synthetic long).

**When to Use:** When using swaps to adjust portfolio allocations or rebalance between asset classes without selling/buying the underlying assets (trigger: "rebalance portfolio," "reduce allocation from X% to Y%," "increase allocation," "equity swap," "pay/receive return on index").

**Procedure:**
1. Identify the current portfolio allocation and the target allocation for each asset class
2. Determine the direction of change needed: if reducing exposure, you need a synthetic short position; if increasing exposure, you need a synthetic long position
3. For synthetic short (reduce exposure): enter swap to PAY the return on that asset class
4. For synthetic long (increase exposure): enter swap to RECEIVE the return on that asset class
5. Verify the swap positions: reducing equity from 65% to 60% requires PAYING equity return; increasing bonds from 35% to 40% requires RECEIVING bond return

**Example (sanitized):**
> **Scenario:** Portfolio has 70% stocks (beta 1.2) and 30% bonds (duration 5.0). Manager wants to rebalance to 65% stocks and 35% bonds using swaps with notional value $50M.
> **Wrong approach:** Assuming that to gain bond exposure, you pay Libor and receive bond return, and to maintain stock exposure, you pay Libor and receive stock return.
> **Correct approach:** (1) Current: 70% stocks, target: 65% stocks → need to REDUCE stock exposure by 5%. (2) Current: 30% bonds, target: 35% bonds → need to INCREASE bond exposure by 5%. (3) To reduce stock exposure: PAY stock index return (synthetic short). (4) To increase bond exposure: RECEIVE bond index return (synthetic long). (5) Correct swaps: equity swap pays stock return/receives Libor; bond swap receives bond return/pays Libor.

---

## Pattern: Risk-Free Return Requires Complete Risk Elimination

**Description:** Failure to recognize that earning the risk-free rate of return requires eliminating ALL sources of risk exposure (market risk, currency risk, etc.), not just hedging one risk factor while leaving others exposed.

**When to Use:** When evaluating hedging strategies intended to achieve risk-free returns or when asked which strategy results in earning the domestic risk-free rate (trigger: "earn risk-free rate," "hedging strategy," "eliminate risk," "foreign equity position," "currency and market risk").

**Procedure:**
1. Identify all sources of risk in the position (e.g., foreign equity has both currency risk and equity market risk)
2. For each proposed hedging strategy, systematically check which risk sources remain after the hedge
3. Recognize that earning risk-free rate requires: (a) eliminating currency risk through FX forwards/futures, AND (b) eliminating market risk through equity futures/forwards
4. Partial hedges (e.g., only currency hedge, only equity hedge) leave residual risk and cannot achieve risk-free return
5. Select the strategy that eliminates ALL identified risk sources

**Example (sanitized):**
> **Scenario:** Portfolio holds foreign stocks worth €10M. Three hedging strategies: (A) sell foreign currency, (B) sell foreign currency AND sell foreign stock index, (C) buy foreign currency and sell foreign stock index. Which earns domestic risk-free rate?
> **Wrong approach:** Choosing (A) because hedging currency risk alone converts foreign exposure to domestic terms.
> **Correct approach:** (1) Foreign stock position has TWO risks: currency risk (€ vs $) and equity market risk (foreign stock index). (2) Strategy A: hedges currency only, leaves equity market risk → cannot earn risk-free rate. (3) Strategy B: hedges BOTH currency (sell €) AND equity market (sell stock index) → eliminates all risk → earns risk-free rate. (4) Strategy C: wrong currency direction, increases currency risk. (5) Only Strategy B achieves risk-free return.

---

## Pattern: Option Intrinsic Value Lower Bounds and Mispricing Detection

**Description:** Failure to apply fundamental option pricing boundaries: call options must be worth at least max(0, S - K) and put options must be worth at least max(0, K - S), where violations indicate mispricing regardless of time value or volume considerations.

**When to Use:** When identifying mispriced options given current stock/underlying price and option prices, or when evaluating whether option prices violate no-arbitrage conditions (trigger: "mispriced options," "option prices," "current stock price," "identify which options").

**Procedure:**
1. Identify the current underlying price (S) and each option's strike price (K)
2. For each call option: calculate intrinsic value = max(0, S - K); if market price < intrinsic value, the call is mispriced
3. For each put option: calculate intrinsic value = max(0, K - S); if market price < intrinsic value, the put is mispriced
4. Systematically check BOTH calls and puts across all strikes—don't focus only on one option type
5. Ignore volume, time to expiration, or other factors when checking lower bound violations—these are strict no-arbitrage conditions

**Example (sanitized):**
> **Scenario:** Stock at $85. Options with strike $80: March call at $2.50, March put at $0.60, October call at $9.00, October put at $3.50. Which are mispriced?
> **Wrong approach:** Focusing on volume or time value, concluding March call and October call are mispriced based on "unusual characteristics."
> **Correct approach:** (1) Stock = $85, Strike = $80. (2) March call intrinsic value = max(0, 85-80) = $5; market price = $2.50 < $5 → MISPRICED (violates lower bound). (3) October call intrinsic value = $5; market price = $9.00 > $5 → OK. (4) March put intrinsic value = max(0, 80-85) = $0; market price = $0.60 → OK (can have time value). (5) October put intrinsic value = $0; market price = $3.50 → OK. (6) Mispriced: March call only... wait, check if October put should be near zero for deep OTM—actually, with time value it's acceptable. Re-examine: March call definitely mispriced. Check October put more carefully: for OTM put with 9 months to expiration, $3.50 might be reasonable time value OR might violate upper bounds. Focus on clear violations: March call is definitely mispriced.

---

## Pattern: Volatility Smile vs Skew Pattern Recognition

**Description:** Confusion between volatility smile (symmetric U-shaped pattern where implied volatility is higher for both deep ITM and deep OTM options relative to ATM options) and volatility skew (monotonic pattern where implied volatility consistently increases or decreases across strike prices in one direction).

**When to Use:** When analyzing implied volatility patterns across different strike prices or identifying whether options exhibit smile or skew (trigger: "implied volatility," "volatility smile," "volatility skew," "strike prices," "exercise prices").

**Procedure:**
1. Organize implied volatility data by strike price from lowest to highest
2. Identify the at-the-money (ATM) strike (closest to current underlying price)
3. Check the pattern: (a) Volatility smile: IV decreases as strikes approach ATM from both sides, creating U-shape (high IV for deep ITM and deep OTM, low IV for ATM). (b) Volatility skew: IV consistently increases or decreases monotonically across strikes
4. For smile: verify symmetry—both tails (low and high strikes) have elevated IV relative to center
5. For skew: verify monotonic trend—IV moves consistently in one direction without reversing

**Example (sanitized):**
> **Scenario:** Index at 10,000. Call implied volatilities: strike 9,500 → 8%, strike 9,750 → 11%, strike 10,000 → 13%, strike 10,250 → 14%. Put implied volatilities: strike 9,500 → 19%, strike 9,750 → 17%, strike 10,000 → 15%, strike 10,250 → 14%. Pattern?
> **Wrong approach:** Seeing some variation and concluding it's a smile because IV changes across strikes.
> **Correct approach:** (1) ATM strike ≈ 10,000 (current index level). (2) Call IV pattern: 8% → 11% → 13% → 14% (consistently INCREASING as strikes rise). (3) Put IV pattern: 19% → 17% → 15% → 14% (consistently DECREASING as strikes rise). (4) No U-shape: low strikes have low call IV but high put IV; high strikes have high call IV but low put IV. (5) This is monotonic change = SKEW, not smile. (6) Smile would require both low and high strikes to have elevated IV relative to ATM.

---

## Pattern: Interest Rate Swap Cash Flow vs Market Value Sensitivity

**Description:** Misunderstanding that interest rate swaps used to convert floating-rate to fixed-rate exposure stabilize cash flows but do NOT reduce the overall interest rate sensitivity (duration) of the combined position, because the swap itself has offsetting interest rate sensitivity that maintains net exposure.

**When to Use:** When evaluating the impact of receive-floating/pay-fixed swaps on interest rate sensitivity or duration of the overall position (trigger: "interest rate swap," "reduce sensitivity," "interest rate sensitivity," "overall position," "duration of position").

**Procedure:**
1. Identify the original position (e.g., floating-rate liability) and its interest rate characteristics
2. Identify the proposed swap (e.g., receive-floating/pay-fixed) and recognize it converts cash flows from floating to fixed
3. Distinguish between two separate effects: (a) Cash flow stabilization: swap DOES stabilize cash flows by converting floating payments to fixed. (b) Interest rate sensitivity: swap does NOT reduce overall sensitivity because the swap's market value changes with interest rates in the opposite direction of the liability
4. Recognize that the combined position (liability + swap) has similar interest rate sensitivity to a fixed-rate liability, not reduced sensitivity
5. Conclude: swap achieves cash flow hedging but maintains (or even increases) market value sensitivity to interest rates

**Example (sanitized):**
> **Scenario:** Company has floating-rate debt (duration -0.2). Analyst proposes receive-floating/pay-fixed swap (duration of swap = -3.0) to "reduce interest rate sensitivity of overall position."
> **Wrong approach:** Agreeing that the swap reduces sensitivity because it hedges the floating-rate exposure.
> **Correct approach:** (1) Original position: floating-rate debt has low duration (-0.2), low sensitivity to rate changes. (2) Swap: receive-floating/pay-fixed has duration -3.0, meaning swap value falls when rates rise. (3) Cash flow effect: swap converts floating payments to fixed → stabilizes cash flows ✓. (4) Sensitivity effect: combined duration ≈ -0.2 + (-3.0) = -3.2, HIGHER sensitivity than original -0.2. (5) The swap does NOT reduce interest rate sensitivity; it increases it while stabilizing cash flows. (6) Analyst is incorrect about reducing sensitivity.

---

## Pattern: Swaption Type Selection for Existing Swap Positions

**Description:** Confusion about which swaption type hedges an existing swap position: a payer swaption (right to enter pay-fixed swap) hedges against RISING rates for those expecting to enter pay-fixed swaps, while a receiver swaption (right to enter receive-fixed swap) hedges existing pay-fixed positions against FALLING rates.

**When to Use:** When selecting swaptions to hedge or cancel existing swap positions, or when evaluating which swaption protects against specific rate movements (trigger: "payer swaption," "receiver swaption," "hedge swap," "protect against falling/rising rates," "existing pay-fixed position").

**Procedure:**
1. Identify the existing or anticipated swap position (pay-fixed or receive-fixed)
2. Identify the rate movement concern (rising rates or falling rates)
3. Apply the matching rule: (a) If you have/will have a pay-fixed swap and rates fall → you're paying above-market rates → need RECEIVER swaption to offset. (b) If you anticipate needing a pay-fixed swap and rates rise → you'll pay above-target rates → need PAYER swaption to lock in rate
4. Verify the direction: payer swaption benefits from rising rates (lets you enter pay-fixed at predetermined rate); receiver swaption benefits from falling rates (lets you enter receive-fixed at predetermined rate)
5. Check the hedge logic: the swaption should allow you to enter a position that offsets your existing exposure

**Example (sanitized):**
> **Scenario:** Company has entered a pay-fixed swap at 4%. Concerned that rates might fall to 2%, making their 4% payment unfavorable. Which swaption provides protection?
> **Wrong approach:** Selecting payer swaption because they have a pay-fixed position.
> **Correct approach:** (1) Existing position: pay-fixed at 4%. (2) Concern: rates fall to 2% → company pays 4% while market pays 2% → unfavorable. (3) Need to offset: if rates fall, want ability to enter receive-fixed swap at predetermined rate. (4) RECEIVER swaption gives right to enter receive-fixed swap → if rates fall to 2%, exercise swaption to receive (say) 3.5% fixed → offsets some of the 4% payment. (5) Payer swaption would give right to enter ANOTHER pay-fixed swap → makes position worse, not better. (6) Correct answer: receiver swaption, not payer swaption.