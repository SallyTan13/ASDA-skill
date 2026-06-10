# Skill Patterns for Derivatives Concept Confusion Errors

## Pattern: Currency Pair Reciprocity and Hedging Direction

**Description:** Failure to recognize that options on reciprocal currency pairs (e.g., EUR/GBP vs GBP/EUR) provide equivalent hedging outcomes when properly structured, and confusion about which direction protects against which currency movement. Critical error: not verifying that the option's profit direction matches the required hedge direction by explicitly checking that the option profits in the SAME scenario where the underlying position LOSES.

**When to Use:** When evaluating currency hedging strategies involving options on different currency pair quotations (e.g., "short EUR position," "EUR/GBP vs GBP/EUR options").

**Procedure:**
1. Identify the underlying exposure: determine which currency you are long/short
2. Determine the LOSS scenario explicitly: a short EUR position (long GBP) loses when EUR strengthens (GBP weakens) - write this down clearly
3. Recognize reciprocal equivalence: a call on GBP/EUR (right to buy EUR with GBP) = put on EUR/GBP (right to sell EUR for GBP)
4. For EACH hedging instrument, determine its PROFIT scenario:
   - For calls: profit when the base currency (first in pair) strengthens
   - For puts: profit when the base currency (first in pair) weakens
   - Example: GBP/EUR call profits when GBP strengthens (EUR weakens)
   - Example: EUR/GBP put profits when EUR weakens
5. **CRITICAL VERIFICATION STEP**: For each option, explicitly compare its profit scenario to the loss scenario from step 2:
   - Write: "Option profits when [scenario X]"
   - Write: "Position loses when [scenario Y]"
   - Ask: "Is scenario X the SAME as scenario Y?"
   - If YES → valid hedge ✓
   - If NO → invalid hedge ✗
6. Example verification for short EUR position:
   - Loss scenario: EUR strengthens
   - GBP/EUR call: profits when GBP strengthens (EUR weakens) → EUR weakens ≠ EUR strengthens → NOT a valid hedge ✗
   - EUR/GBP put: profits when EUR weakens → EUR weakens ≠ EUR strengthens → NOT a valid hedge ✗
   - EUR/GBP call: profits when EUR strengthens → EUR strengthens = EUR strengthens → VALID hedge ✓
7. Test all strategies systematically using this explicit comparison before accepting any as valid hedges

**Example (sanitized):**
> **Scenario:** An investor has a short position in Japanese yen (JPY) and considers three hedges: (1) forward contract selling CAD/JPY, (2) buying a JPY/CAD call option, (3) buying a CAD/JPY put option.
> **Wrong approach:** Accepting strategy 2 because "it involves JPY and provides some protection."
> **Correct approach:** (1) Short JPY means long CAD exposure. (2) Loss scenario: position loses if JPY strengthens (CAD weakens). (3) Strategy 1: forward locks in rate ✓. (4) Strategy 2: JPY/CAD call = right to buy CAD with JPY. Profit scenario: profits when JPY strengthens (can buy more CAD per JPY). Verification: "JPY strengthens" = "JPY strengthens" → SAME scenario → CORRECT hedge ✓. (5) Strategy 3: CAD/JPY put = right to sell CAD for JPY at fixed rate. Profit scenario: profits when CAD/JPY falls (JPY strengthens). Verification: "JPY strengthens" = "JPY strengthens" → SAME scenario → CORRECT hedge ✓. (6) All three strategies hedge correctly because their profit scenarios match the loss scenario.

**Common Mistakes to Avoid:**
- Assuming any option on a relevant currency pair provides hedging without checking profit direction
- Confusing "right to buy X with Y" with "protection against X strengthening"
- Not explicitly writing out and comparing the loss scenario vs profit scenario for each option
- Rejecting reciprocal pair options without systematic verification of profit direction

---
## Pattern: Option Exercise Logic and Payoff Asymmetry

**Description:** Confusion about when options are exercised (calls when S > K, puts when S < K) and which option type is relevant for a given price movement scenario, leading to incorrect loss calculations. Critical: when stock price falls below strike, ONLY put options are exercised; when stock price rises above strike, ONLY call options are exercised. The loss calculation must account for the full exercise payoff, not just the premium paid.

**When to Use:** When analyzing option exercise decisions, calculating losses/gains from option positions, or determining which option type applies to a specific market scenario (trigger: "if stock price falls/rises," "option is exercised when," "stock price is $X," "how much is the loss," "calculate loss when price," "there is a loss," "loss when exercised," "stock price falls and option is exercised").

**Procedure:**
1. Identify the price movement direction in the scenario (stock rises/falls relative to strike)
2. Determine which option type would be exercised in that scenario: calls exercised only when S > K (buy below market), puts exercised only when S < K (sell above market)
3. If the scenario involves a price below the strike, only put options are relevant for exercise analysis; if price above strike, only call options are relevant
4. Identify the relevant strike price (K) and the option premium paid for the CORRECT option type
5. **Calculate the FULL loss from exercise, not just the premium:**
   - For put exercised (S < K) by the WRITER: loss = (K - S) - premium received = intrinsic loss minus premium cushion
   - For put exercised (S < K) by the BUYER: gain = (K - S) - premium paid (can be negative if premium > intrinsic value)
   - For call exercised (S > K) by the WRITER: loss = (S - K) - premium received
   - For call exercised (S > K) by the BUYER: gain = (S - K) - premium paid
6. Determine perspective: is the question asking about the option buyer's or writer's loss?
7. **Critical verification:** The loss is NOT simply the premium paid; it includes the intrinsic value at exercise minus the premium
8. For multiple contracts, multiply the per-contract loss by the number of contracts

**Example (sanitized):**
> **Scenario:** An investor writes 10 put options with strike $120 at a premium of $8 per contract (contract size 100 shares). The stock falls to $95 and the puts are exercised. What is the total loss to the writer?
> **Wrong approach:** Calculating loss as just the premium: 10 × 100 × $8 = $8,000, or claiming the writer profits by $8,000.
> **Correct approach:** (1) Stock at $95, strike at $120 → price is BELOW strike. (2) Put options are exercised (not calls). (3) Writer perspective: must buy stock at $120 when market is $95. (4) Intrinsic loss per share = $120 - $95 = $25. (5) Premium received per share = $8 (provides partial offset). (6) Net loss per share = $25 - $8 = $17. (7) Total loss = 10 contracts × 100 shares × $17 = $17,000. (8) The loss is NOT just the premium; it's the full exercise obligation minus premium received.

**Common Mistakes to Avoid:**
- Applying call option logic when stock price falls below strike price
- Calculating losses using only the premium paid/received, ignoring the exercise intrinsic value
- Confusing the option buyer's position with the writer's position
- Not checking which option type would actually be exercised at the stated price level
- Treating the premium as the maximum loss for option writers (this only applies to buyers)

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

**Description:** Confusion about which option strategies provide true downside protection: protective puts create a definitive floor by guaranteeing a minimum sale price, while covered calls only provide limited downside cushion equal to the premium received and do NOT protect against significant losses—they are income-generation strategies, not loss-protection strategies. Critical error: claiming covered calls "establish a minimum value" or "create a floor."

**When to Use:** When evaluating option strategies for downside protection, assessing claims about "protecting gains," "establishing minimum value," "creating a floor," or comparing covered calls vs protective puts (trigger: "covered call," "protective put," "protect gains," "downside protection," "hedge against losses," "establish minimum value," "floor," "minimum portfolio value," "least likely correct regarding," "comment about using options," "manage risk").

**Procedure:**
1. Identify the baseline position (e.g., long stock) and the option overlay being considered
2. For covered calls (long stock + short call): recognize this provides only premium income as cushion, leaves most downside exposed, and caps upside—it is NOT a protection strategy and does NOT establish a floor
3. For protective puts (long stock + long put): recognize this guarantees a minimum sale price (strike price) regardless of how far the stock falls—this IS true protection and DOES establish a floor
4. When evaluating "protection" or "minimum value" claims, check if the strategy establishes a floor value (protective put does, covered call does not)
5. Distinguish between income generation (covered call) and loss protection (protective put) as fundamentally different objectives
6. **Test each claim systematically:** if statement says covered calls "establish minimum value" or "create a floor," this is INCORRECT and should be identified as the least correct statement
7. **For multiple-choice questions asking "least likely correct":** the statement claiming covered calls establish minimum value is the answer, even if other statements have minor issues

**Example (sanitized):**
> **Scenario:** An investor holds shares worth $80 and considers strategies. Advisor makes three claims: (1) "Covered calls establish a minimum portfolio value," (2) "Protective puts reduce volatility," (3) "Covered calls enhance returns if prices remain stable." Which is least correct?
> **Wrong approach:** Accepting claim 1 because "covered calls provide some downside cushion from the premium."
> **Correct approach:** (1) Covered call (long stock + short $85 call for $3 premium): if stock falls to $40, investor loses $40 per share minus $3 premium = $37 loss. No minimum value is established—losses continue below $77. (2) Protective put (long stock + long $75 put for $4 premium): if stock falls to $40, investor can sell at $75 via put, establishing minimum value = $71. (3) Claim 1 is INCORRECT: covered calls do NOT establish minimum value. (4) Claims 2 and 3 are generally correct (puts do reduce volatility, covered calls do provide income if stable). (5) Answer: Claim 1 is least correct.

**Common Mistakes to Avoid:**
- Claiming covered calls establish a minimum value or floor (they do not)
- Confusing limited premium cushion with true downside protection
- Treating income generation strategies (covered calls) as equivalent to protection strategies (protective puts)
- Not testing claims about "minimum value" by checking what happens in severe downside scenarios
- Focusing on secondary issues (like return enhancement nuances) when a fundamental error about floor establishment exists

---
## Pattern: Piecewise Function Continuity at Boundary Conditions

**Description:** Failure to recognize that well-defined piecewise pricing formulas (like barrier options with H≤K vs H≥K, or standard options when strike equals spot/forward price) must be continuous at boundary points, meaning both formulas yield identical values when evaluated at the boundary. At special boundary conditions (e.g., K = S₀, K = F), option pricing formulas often simplify significantly. Critical: "strike corresponds to cash price" means K equals the CURRENT bond/asset price, not the forward price or exercise price from other contexts.

**When to Use:** When comparing two different formulas that apply to different parameter ranges with a shared boundary point, or when asked to value options at special parameter values where simplification occurs (trigger: "two formulas," "when H = K," "H ≤ K vs H ≥ K," "strike price equals," "strike corresponds to," "when K = S," "boundary condition," "special case," "strike corresponds to cash price," "strike corresponds to the cash price of the bond").

**Procedure:**
1. **Identify what "corresponds to" means in context:**
   - "Strike corresponds to cash price" → K = current spot/cash price (S₀ or B₀)
   - "Strike corresponds to forward price" → K = forward price (F)
   - "Strike corresponds to exercise price" → K = specified exercise price from problem setup
   - Default: if not specified, "cash price" means CURRENT price, not forward or other reference
2. Identify the boundary condition where the two formula domains meet (e.g., H = K) or where a special parameter relationship exists (e.g., K = S₀, K = F)
3. Recognize that properly constructed piecewise functions in finance must be continuous (no jumps in value)
4. For boundary conditions between two formulas: substitute the boundary value into both formulas and verify they produce identical results
5. For special parameter values (K = S₀, K = F): recognize these often represent at-the-money or forward-at-the-money conditions where formulas may simplify
6. **Critical verification:** When question asks "when strike corresponds to cash price," use K = current bond/asset price from the problem data, NOT the exercise price or forward price
7. Simplify each expression algebraically at the boundary
8. Verify that both formulas produce the same numerical result at the boundary (if not, there's an arbitrage opportunity or formula error)

**Example (sanitized):**
> **Scenario:** A commodity option pricing model uses formula F₁ for strikes below the spot price and formula F₂ for strikes above the spot price. The commodity's current spot price is $85, and the forward price is $90. Question asks: "What is the option value when the strike price corresponds to the commodity's cash price?"
> **Wrong approach:** Using K = $90 (forward price) because "forward price is a common reference in derivatives."
> **Correct approach:** (1) "Cash price" means current spot price = $85, not forward price = $90. (2) The question asks for option value at K = $85 (the spot/cash price). (3) At K = S₀ = $85, this is an at-the-money spot condition. (4) Determine which formula applies: K = $85 is the boundary between F₁ and F₂. (5) Both formulas should yield the same value at K = $85 (continuity). (6) Calculate using either formula at the boundary. (7) Key insight: "corresponds to cash price" always means current spot/cash price unless explicitly stated otherwise.

**Common Mistakes to Avoid:**
- Confusing "cash price," "spot price," "forward price," and "exercise price" when identifying boundary conditions
- Applying formulas mechanically without recognizing special parameter relationships
- Not checking whether the question asks about current price, forward price, or another reference point
- Assuming "strike corresponds to" always means the forward price rather than checking context
- Using the exercise price from problem setup when the question specifically asks about "cash price"

---
## Pattern: Numeraire Change and Correlation-Adjusted Risk Pricing

**Description:** Failure to recognize that changing numeraire (especially to foreign currency bonds) requires incorporating correlation-weighted volatility components from all risk sources affecting the asset-numeraire ratio, not just the asset's own drift. The market price of risk is a SUM of multiple correlation-weighted terms. When asked for the market price of a SPECIFIC Brownian motion (dz), identify which risk source that Brownian motion represents and provide only that component.

**When to Use:** When changing pricing measure to a foreign currency zero-coupon bond numeraire or analyzing cross-currency derivative pricing with explicit questions about "market price of risk in new measure," "drift adjustment under foreign measure," "risk-neutral pricing with foreign numeraire," or "market price of dz-risk" where dz is associated with a specific risk source.

**When NOT to Use:** 
- When the question asks about approximate portfolio tracking or hedging (e.g., "changes in value by approximately ΔS")
- When simple currency conversion and basic hedging principles can answer the question
- When the question focuses on practical portfolio construction rather than theoretical pricing measures
- When no explicit mention of numeraire change, measure change, or drift adjustment appears

**Procedure:**
1. Verify the question explicitly involves numeraire change or measure change (not just cross-currency exposure)
2. **Identify what is being asked for:**
   - If question asks for "market price of risk" (general) → provide the complete sum
   - If question asks for "market price of dz-risk" or "market price of dz_X-risk" → identify which risk source dz_X represents and provide only that component
3. Identify all stochastic components affecting the asset/numeraire ratio:
   - Asset price process (S) with Brownian motion dz_S
   - Exchange rate process (F) with Brownian motion dz_F
   - Foreign bond price process (P or Q) with Brownian motion dz_P or dz_Q
4. **Map Brownian motions to risk sources:**
   - dz_S → asset price risk
   - dz_F → exchange rate risk
   - dz_P or dz_Q → foreign bond price risk
5. Recognize that the COMPLETE market price of risk is a MULTI-TERM SUM: λ_total = Σ(ρᵢⱼ σⱼ) for all correlated risk sources
6. For foreign bond numeraire, construct the complete formula:
   - Term 1 (foreign bond component): correlation between asset and foreign bond price × foreign bond volatility = ρ_SP · σ_P (or ρ_SQ · σ_Q)
   - Term 2 (FX component): correlation between asset and exchange rate × FX volatility = ρ_SF · σ_F
   - Total: λ_total = ρ_SP · σ_P + ρ_SF · σ_F
7. **Select the appropriate answer based on what was asked:**
   - If asked for market price of dz_P-risk (or dz_Q-risk) → provide only Term 1: ρ_SP · σ_P
   - If asked for market price of dz_F-risk → provide only Term 2: ρ_SF · σ_F
   - If asked for market price of dz_S-risk or general market price of risk → provide the complete sum
8. Verify each subscript: S = asset, P or Q = foreign bond price, F = exchange rate (foreign/domestic)
9. Apply to drift adjustment: the new drift under the foreign measure is adjusted by -λσ_S

**Common Mistakes to Avoid:**
- Applying complex numeraire change formulas to simple hedging questions that ask about approximate tracking
- Including only the exchange rate term and omitting the foreign bond price term when the complete sum is needed
- Providing the complete sum when only a specific component is requested
- Not identifying which Brownian motion corresponds to which risk source
- Treating the market price of risk as a single correlation-weighted component instead of recognizing it has multiple components

**Example (sanitized):**
> **Scenario:** Asset S (in GBP) follows dS = μS dt + σ_S S dz_S. Numeraire is a CHF zero-coupon bond with price Q following dQ = rQ dt + σ_Q Q dz_Q. Correlation between S and CHF bond price: ρ_SQ = 0.3, bond volatility σ_Q = 0.06. Correlation between S and GBP/CHF rate: ρ_SF = 0.5, FX volatility σ_F = 0.08. Question asks: "What is the market price of dz_Q-risk?"
> **Wrong approach:** Calculating λ = ρ_SF · σ_F = 0.5 × 0.08 = 0.04 (providing the FX component when asked for bond component).
> **Correct approach:** (1) Question asks specifically for "market price of dz_Q-risk" → need only the component associated with dz_Q. (2) Map Brownian motions: dz_Q is the Brownian motion for the foreign bond price Q. (3) The market price of dz_Q-risk is the correlation between S and Q times the volatility of Q. (4) Answer: λ_Q = ρ_SQ · σ_Q = 0.3 × 0.06 = 0.018. (5) Note: If asked for complete market price of dz_S-risk, would provide sum: 0.018 + 0.04 = 0.058.
```

```
## Pattern: Short Straddle Greek Signature Recognition

**Description:** Misidentifying option strategies by focusing on individual Greeks rather than recognizing that a short straddle's defining characteristic is SMALL/near-zero delta (from offsetting call/put deltas) combined with negative gamma, positive theta, and negative vega. Critical: positive delta (not small/near-zero) ELIMINATES short straddle as a possibility.

**When to Use:** When identifying option strategies from Greek exposures, especially distinguishing short straddles from other short volatility strategies (trigger: "Greek exposures," "straddle," "delta/gamma/theta/vega signs," "identify strategy," "most likely a," "Strategy X is").

**Procedure:**
1. Recall short straddle structure: sell ATM call + sell ATM put at same strike
2. Identify the delta signature: short call (negative delta) + short put (positive delta) ≈ near-zero or SMALL net delta (key distinguishing feature, typically |delta| < 0.10)
3. Apply the delta elimination rule FIRST: if delta is significantly positive (> +0.15) or significantly negative (< -0.15), ELIMINATE short straddle from consideration immediately
4. Verify other Greeks only after delta check: negative gamma (short options), positive theta (time decay benefit), negative vega (short volatility)
5. For strategies with large positive delta: consider short put, bull spread, or ratio spreads
6. For strategies with large negative delta: consider short call, bear spread, or ratio spreads
7. Only if delta is small/near-zero AND other Greeks match: conclude short straddle

**Example (sanitized):**
> **Scenario:** Three strategies show Greeks: (X) delta=+0.55, gamma=-0.3, theta=+0.5, vega=-0.8; (Y) delta=+0.08, gamma=-0.4, theta=+0.6, vega=-0.9; (Z) delta=-0.45, gamma=-0.2, theta=+0.4, vega=-0.7. Which is most likely a short straddle?
> **Wrong approach:** Selecting X because "positive theta and negative vega indicate short options, matching straddle characteristics."
> **Correct approach:** (1) Short straddle requires near-zero delta from offsetting positions. (2) Strategy X: delta = +0.55 (large positive) → ELIMINATE immediately; this indicates directional bias (likely short put or bull spread). (3) Strategy Y: delta = +0.08 (small, near-zero) → passes delta test ✓; gamma = -0.4 (negative) ✓, theta = +0.6 (positive) ✓, vega = -0.9 (negative) ✓ → all characteristics match short straddle. (4) Strategy Z: delta = -0.45 (large negative) → ELIMINATE; directional bias (likely short call or bear spread). (5) Answer: Y is the short straddle. (6) Key insight: delta magnitude is the PRIMARY filter; other Greeks are secondary confirmation.

**Common Mistakes to Avoid:**
- Identifying strategies based on gamma/theta/vega without first checking delta magnitude
- Accepting large positive or negative delta as compatible with short straddle
- Not applying the delta elimination rule as the first step in strategy identification
- Confusing "positive delta with negative gamma" (could be many strategies) with "small delta with negative gamma" (straddle signature)
## Pattern: Duration Matching in Interest Rate Hedging

**Description:** Failure to match the duration/maturity of the hedging instrument to the hedged asset, leading to ineffective hedges when short-term rate instruments are used to hedge long-term rate exposure. Additionally, failure to recognize the directional requirement: to hedge a LONG position against RISING rates requires SELLING/SHORTING the hedging instrument; to hedge a SHORT position or gain exposure requires BUYING/GOING LONG the hedging instrument.

**When to Use:** When selecting interest rate hedging instruments for bonds or rate-sensitive positions, or when determining the direction of a hedge based on market view (trigger: "hedge 10-year bond," "interest rate futures," "Eurodollar futures," "bond futures," "view on domestic interest rates," "hedge against rising rates," "protect against rate increase," "most likely would").

**Procedure:**
1. Identify the duration/maturity of the asset being hedged (e.g., 10-year Treasury bond)
2. Recognize that effective hedging requires sensitivity to the SAME segment of the yield curve
3. Match instrument to exposure: long-term bonds → hedge with bond futures or long-term swaps; short-term rates → hedge with Eurodollar or short-term instruments
4. **Determine the directional requirement:**
   - LONG bond position + expect RISING rates → SELL bond futures (short position profits when rates rise, bond prices fall)
   - LONG bond position + expect FALLING rates → BUY bond futures or enter receive-fixed swap (gain additional exposure)
   - SHORT bond position + expect FALLING rates → BUY bond futures (hedge against price increase)
5. **Critical directional check:**
   - To profit from FALLING prices (rising rates): SELL/SHORT futures
   - To profit from RISING prices (falling rates): BUY/LONG futures
   - Never confuse "buying futures to short the market" - buying futures is a LONG position that profits from price increases
6. Evaluate each option for BOTH duration match AND directional correctness
7. **Apply elimination logic:**
   - Eliminate options with duration mismatch (e.g., 90-day Eurodollar for 10-year bond)
   - Eliminate options with wrong direction (e.g., receive-fixed swap when hedging against rising rates)
8. Verify: duration mismatch creates basis risk; wrong direction creates additional exposure instead of hedge

**Example (sanitized):**
> **Scenario:** A portfolio manager holds a 7-year corporate bond (duration 6.2) and expects rates to rise. Options: (A) sell bond futures (duration ~8), (B) enter receive-fixed 7-year swap, (C) sell 90-day Eurodollar futures.
> **Wrong approach:** Selecting B because "a 7-year swap matches the bond's maturity and provides rate protection."
> **Correct approach:** (1) Position: LONG 7-year bond. (2) Market view: rates will RISE (bond prices will FALL). (3) Hedge requirement: need instrument that PROFITS when rates rise. (4) Option A: sell bond futures → duration match ✓, directional match ✓ (short futures profit when rates rise). (5) Option B: receive-fixed swap → duration match ✓, but WRONG direction ✗ (receive-fixed INCREASES rate exposure, doesn't hedge). (6) Option C: 90-day Eurodollar → duration mismatch ✗ (short-term vs 7-year). (7) Answer: A (sell bond futures).

**Common Mistakes to Avoid:**
- Matching duration but getting the direction wrong (e.g., receive-fixed swap to hedge rising rates)
- Confusing "hedge against rising rates" with "gain exposure to falling rates"
- **Believing that buying futures creates a short position or profits from price declines**
- Not recognizing that receive-fixed swaps INCREASE rate sensitivity rather than reduce it
- Selecting short-term instruments (Eurodollar futures) for long-term bond hedges
- Assuming any swap with matching maturity provides a hedge without checking pay/receive direction
```

```
## Pattern: Swap Payoff Evaluation Under Relative Performance Expectations

**Description:** Failure to correctly evaluate which swap strategy captures economic benefit by not systematically checking whether each swap's receive leg outperforms its pay leg under the stated market view, and not identifying the swap with the MINIMUM (most negative or least positive) benefit.

**When to Use:** When evaluating swap strategies based on relative performance forecasts between indices and rates (trigger: "swap strategies," "receive/pay," "market view that X will outperform Y," "least likely to capture benefit").

**Procedure:**
1. Clearly state the market view with inequality relationships (e.g., small-cap > Libor > mid-cap)
2. For each swap, identify what you receive and what you pay
3. Calculate the expected net benefit: receive leg performance - pay leg performance
4. Record all calculated benefits numerically (e.g., Swap 1: +2%, Swap 2: -5%, Swap 3: +3%)
5. When asked for "least benefit" or "least likely to capture benefit": select the swap with the MINIMUM value (most negative, or if all positive, the smallest positive)
6. When asked for "greatest benefit": select the swap with the MAXIMUM value
7. Verify by checking all three relationships systematically and comparing final numerical results

**Example (sanitized):**
> **Scenario:** Market view: Index A will return 12%, Index B will return 4%, Libor will be 7%. Three swaps: (1) receive Libor, pay Index B; (2) receive Index B, pay Index A; (3) receive Index A, pay Libor. Which swap captures the LEAST benefit?
> **Wrong approach:** Identifying that Swap 2 loses money and stopping there without comparing all swaps numerically.
> **Correct approach:** Swap 1: receive 7% - pay 4% = +3% benefit. Swap 2: receive 4% - pay 12% = -8% benefit (loss). Swap 3: receive 12% - pay 7% = +5% benefit. Comparing: +3%, -8%, +5%. The MINIMUM is -8% (Swap 2). Answer: Swap 2 has the least benefit.

**Common Mistakes to Avoid:**
- Stopping after identifying one negative outcome without comparing all swaps numerically
- Confusing "least benefit" with "no benefit" or "negative benefit only"
- Not explicitly comparing the magnitude of all calculated benefits to find the minimum

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
1. Identify the numeraire explicitly: what instrument defines the risk-neutral measure?
2. Apply the numeraire classification rule:
   - If numeraire = domestic money market account → domestic traditional risk-neutral → λ = 0 for all variables ✓
   - If numeraire = foreign currency bond/money market → foreign currency measure → λ ≠ 0 (includes correlation terms)
3. For foreign currency numeraire (e.g., "traditional risk-neutral world for currency B" when pricing currency A assets):
   - Recognize this is NOT the domestic risk-neutral world
   - Market price of dz-risk = ρ_S,FX · σ_FX (correlation between asset and exchange rate × FX volatility)
   - This accounts for how exchange rate movements affect the asset/numeraire ratio
4. Apply Girsanov theorem with correct drift adjustment: drift changes by -λσ when changing measure
5. Verify: "traditional risk-neutral for currency B" means using currency B instruments as numeraire, making it a foreign measure from currency A's perspective

**Example (sanitized):**
> **Scenario:** Asset in GBP follows dS = 0.10S dt + 0.25S dz. Find market price of risk in CHF risk-neutral world (numeraire = CHF zero-coupon bond). Correlation between S and GBP/CHF exchange rate is 0.5, FX volatility is 0.12.
> **Wrong approach:** "In risk-neutral world, market price of risk = 0 for all variables."
> **Correct approach:** (1) Numeraire = CHF bond → this is a foreign currency measure, not domestic GBP risk-neutral. (2) "Traditional risk-neutral for CHF" means CHF bond numeraire, which is foreign from GBP asset's perspective. (3) Market price of dz-risk must account for GBP/CHF exchange rate correlation: λ = ρ_S,FX · σ_FX = 0.5 × 0.12 = 0.06, not zero. (4) The drift adjustment in the new measure is -λσ = -0.06 × 0.25 = -0.015.

**Common Mistakes to Avoid:**
- Assuming λ = 0 whenever "risk-neutral" is mentioned without checking the numeraire
- Ignoring that "traditional risk-neutral for currency B" implies a foreign currency numeraire when the asset is denominated in currency A
- Forgetting to include correlation-weighted volatility terms for foreign currency measures

---
## Pattern: Swap Direction for Portfolio Rebalancing

**Description:** Failure to recognize that swaps modify existing portfolio allocations, requiring opposite positions to the desired change: to reduce exposure to an asset class, pay that asset's return (synthetic short); to increase exposure, receive that asset's return (synthetic long). Critical: the swap direction must match the DIRECTION OF CHANGE needed, not the final target allocation.

**When to Use:** When using swaps to adjust portfolio allocations or rebalance between asset classes without selling/buying the underlying assets (trigger: "rebalance portfolio," "reduce allocation from X% to Y%," "increase allocation," "equity swap," "pay/receive return on index").

**When NOT to Use:**
- When the question asks about general characteristics of swaps without specifying a rebalancing direction
- When discussing interest rate swaps for duration management (use the Interest Rate Swap patterns instead)
- When the context involves hedging strategies rather than portfolio rebalancing
- When asked about "characteristics of swaps that could accomplish" rather than "which specific swap positions to take"

**Procedure:**
1. Identify the current portfolio allocation and the target allocation for each asset class
2. Determine the direction of change needed: if reducing exposure, you need a synthetic short position; if increasing exposure, you need a synthetic long position
3. For synthetic short (reduce exposure): enter swap to PAY the return on that asset class
4. For synthetic long (increase exposure): enter swap to RECEIVE the return on that asset class
5. Verify the swap positions: reducing equity from 65% to 60% requires PAYING equity return; increasing bonds from 35% to 40% requires RECEIVING bond return
6. **When asked about "characteristics" of swaps for rebalancing without specifying direction:** recognize that BOTH equity swaps AND interest rate swaps (receiving LIBOR) may be needed together to accomplish full rebalancing across asset classes
7. **For questions asking about swap characteristics (plural):** consider that the complete rebalancing strategy may involve multiple swap types working together

**Common Mistakes to Avoid:**
- Assuming both swaps should receive index returns when rebalancing involves both increases and decreases
- Confusing the direction of the swap with the final target allocation
- Applying specific pay/receive directions when the question asks about general swap characteristics
- Not distinguishing between "what swaps would accomplish rebalancing" (requires specific directions) and "characteristics of swaps that could be used" (general description)
- Focusing only on equity swaps when both equity and interest rate swaps may be needed for complete rebalancing

**Example (sanitized):**
> **Scenario:** Portfolio has 70% stocks (beta 1.2) and 30% bonds (duration 5.0). Manager wants to rebalance to 65% stocks and 35% bonds using swaps with notional value $50M.
> **Wrong approach:** Assuming that to gain bond exposure, you pay Libor and receive bond return, and to maintain stock exposure, you pay Libor and receive stock return.
> **Correct approach:** (1) Current: 70% stocks, target: 65% stocks → need to REDUCE stock exposure by 5%. (2) Current: 30% bonds, target: 35% bonds → need to INCREASE bond exposure by 5%. (3) To reduce stock exposure: PAY stock index return (synthetic short). (4) To increase bond exposure: RECEIVE bond index return (synthetic long). (5) Correct swaps: equity swap pays stock return/receives Libor; bond swap receives bond return/pays Libor.
```

```
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

**Description:** Failure to apply fundamental option pricing boundaries: call options must be worth at least max(0, S - K) and put options must be worth at least max(0, K - S), where violations indicate mispricing. Additionally, failure to identify excessive time value premiums in deep out-of-the-money options using clear quantitative criteria. Critical: puts are in-the-money when K > S (strike above spot); puts are out-of-the-money when K < S (strike below spot).

**When to Use:** When identifying mispriced options given current stock/underlying price and option prices, or when evaluating whether option prices violate no-arbitrage conditions, or when determining if options are in-the-money or out-of-the-money (trigger: "mispriced options," "option prices," "current stock price," "identify which options," "in the money," "out of the money").

**When NOT to Use:**
- When discussing option strategies without reference to specific prices
- When the question asks about theoretical pricing models rather than arbitrage bounds
- **When asked simple yes/no questions about whether options are in-the-money or out-of-the-money (use basic ITM/OTM definitions only)**

**Procedure:**
1. **For simple ITM/OTM questions (no mispricing analysis needed):**
   - Calls are ITM when S > K, OTM when S < K
   - Puts are ITM when K > S, OTM when S < K
   - Answer directly without further analysis
2. **For mispricing analysis, proceed with full procedure:**
3. Identify the current underlying price (S) and each option's strike price (K)
4. **For EACH call option systematically:** 
   - Calculate intrinsic value = max(0, S - K)
   - If market price < intrinsic value → MISPRICED (lower bound violation) ✗
   - Call is in-the-money when S > K, out-of-the-money when S < K
   - For deep OTM calls (S < K - 5% of S): check time value criteria in step 5
5. **For EACH put option systematically:** 
   - Calculate intrinsic value = max(0, K - S)
   - If market price < intrinsic value → MISPRICED (lower bound violation) ✗
   - Put is in-the-money when K > S (strike above spot), out-of-the-money when K < S (strike below spot)
   - For deep OTM puts (S > K + 5% of S): check time value criteria in step 5
6. **Create a systematic checklist - mark each option:**
   - Option name | Type | ITM/OTM | Intrinsic | Market | Lower bound OK? | Time value check needed?
7. **Apply time value criteria for deep OTM options:**
   - Calculate: Time Value = Market Price - Intrinsic Value
   - Calculate: Time Value % = (Time Value / Strike Price) × 100%
   - For options with 3-6 months to expiration:
     - If OTM by 3-5% and Time Value % > 4% → likely MISPRICED ✗
     - If OTM by 5-10% and Time Value % > 3% → likely MISPRICED ✗
     - If OTM by >10% and Time Value % > 2% → likely MISPRICED ✗
   - For options with 6-12 months to expiration, increase thresholds by 1-2%
   - For options with <3 months, decrease thresholds by 1-2%
8. **Enforce systematic checking:**
   - DO NOT stop after finding one mispriced option
   - Check ALL calls completely, then check ALL puts completely
   - Mark each option as "OK" or "MISPRICED" on your checklist
9. Identify ALL mispriced options from your checklist

**Common Mistakes to Avoid:**
- Confusing the in-the-money condition for puts: puts are ITM when K > S (not when K < S)
- Stating that puts are in-the-money when the strike is below the current stock price (this is backwards)
- **Providing contradictory answers where reasoning says "No" but answer says "Yes"**
- **Over-analyzing simple ITM/OTM questions with complex mispricing procedures**
- Only checking lower bound violations and missing excessive time value in deep OTM options
- Focusing on calls only and not systematically checking puts
- Accepting high premiums on deep OTM options without applying quantitative time value criteria
- Stopping after finding one mispriced option without checking all remaining options

**Example (sanitized):**
> **Scenario:** Stock at $105. Options with strike $100: April call at $4.50, April put at $0.60, November call at $11.00, November put at $5.20. Time to expiration: April = 2 months, November = 8 months. Which are mispriced?
> **Wrong approach:** Checking only calls and concluding April call is mispriced.
> **Correct approach:** (1) Stock = $105, Strike = $100. (2) Create checklist. (3) April call: intrinsic = max(0, 105-100) = $5; market = $4.50 < $5 → MISPRICED (lower bound violation) ✗. (4) November call: intrinsic = $5; market = $11.00; time value = $6.00; time value % = 6.0%. ITM by $5, long-dated → OK ✓. (5) April put: intrinsic = max(0, 100-105) = $0; market = $0.60. OTM by $5 (5% of stock), 2 months to expiration. Time value % = 0.6%. Short-dated OTM → OK ✓. (6) November put: intrinsic = $0; market = $5.20. Deep OTM (stock at $105, strike $100 = 5% OTM), 8 months to expiration. Time value % = 5.2%. For 5% OTM with 6-12 months, threshold is ~5% → borderline but likely MISPRICED ✗. (7) Mispriced options: April call (lower bound violation) and November put (excessive OTM premium).
```

```
## Pattern: Volatility Smile vs Skew Pattern Recognition

**Description:** Confusion between volatility smile (symmetric U-shaped pattern where implied volatility is higher for both deep ITM and deep OTM options relative to ATM options) and volatility skew (monotonic pattern where implied volatility consistently increases or decreases across strike prices in one direction). Critical: when volatility reverts from smile to skew, the strategy must target the options that will lose their elevated implied volatility—typically the wings (OTM options on both sides).

**When to Use:** When analyzing implied volatility patterns across different strike prices, identifying whether options exhibit smile or skew, or designing strategies to profit from changes in volatility structure (trigger: "implied volatility," "volatility smile," "volatility skew," "strike prices," "exercise prices," "revert to normal profile").

**When NOT to Use:**
- When the question only asks about identifying current volatility patterns without trading strategies
- When discussing general option Greeks without reference to volatility structure

**Procedure:**
1. Organize implied volatility data by strike price from lowest to highest
2. Identify the at-the-money (ATM) strike (closest to current underlying price)
3. Check the pattern: (a) Volatility smile: IV decreases as strikes approach ATM from both sides, creating U-shape (high IV for deep ITM and deep OTM, low IV for ATM). (b) Volatility skew: IV consistently increases or decreases monotonically across strikes
4. For smile: verify symmetry—both tails (low and high strikes) have elevated IV relative to center
5. For skew: verify monotonic trend—IV moves consistently in one direction without reversing
6. When designing strategies to profit from smile-to-skew reversion: identify which options are currently overpriced (the wings in a smile) and will lose value when reverting to skew—these should be SOLD

**Common Mistakes to Avoid:**
- Confusing ATM-focused strategies (straddles) with wing-focused strategies (selling OTM options on both sides)
- Assuming smile-to-skew reversion requires selling ATM options when it actually requires selling the overpriced wings
- Describing a strategy as "selling ATM calls and buying ATM puts" when the goal is to profit from volatility normalization (this is contradictory and doesn't capture the smile-to-skew trade)
- Not recognizing that smile-to-skew reversion means the elevated IV at the extremes (OTM calls and OTM puts) will decline

**Example (sanitized):**
> **Scenario:** Index at 10,000. Call implied volatilities: strike 9,500 → 8%, strike 9,750 → 11%, strike 10,000 → 13%, strike 10,250 → 14%. Put implied volatilities: strike 9,500 → 19%, strike 9,750 → 17%, strike 10,000 → 15%, strike 10,250 → 14%. Pattern?
> **Wrong approach:** Seeing some variation and concluding it's a smile because IV changes across strikes.
> **Correct approach:** (1) ATM strike ≈ 10,000 (current index level). (2) Call IV pattern: 8% → 11% → 13% → 14% (consistently INCREASING as strikes rise). (3) Put IV pattern: 19% → 17% → 15% → 14% (consistently DECREASING as strikes rise). (4) No U-shape: low strikes have low call IV but high put IV; high strikes have high call IV but low put IV. (5) This is monotonic change = SKEW, not smile. (6) Smile would require both low and high strikes to have elevated IV relative to ATM.

---
## Pattern: Interest Rate Swap Cash Flow vs Market Value Sensitivity

**Description:** Misunderstanding that interest rate swaps used to convert floating-rate to fixed-rate exposure stabilize cash flows but do NOT reduce the overall interest rate sensitivity (duration) of the combined position, because the swap itself has offsetting interest rate sensitivity that maintains or increases net exposure. Critical: this pattern applies when evaluating the OVERALL position (liability + swap), not when discussing the swap's impact on individual risk components.

**When to Use:** When evaluating the impact of receive-floating/pay-fixed swaps on interest rate sensitivity or duration of the overall position (trigger: "interest rate swap," "reduce sensitivity," "interest rate sensitivity," "overall position," "duration of position," "combined position").

**When NOT to Use:**
- When the question asks specifically about cash flow risk only (swaps DO reduce cash flow risk)
- When the question asks about market value risk only (swaps DO increase market value risk)
- When asked to identify which statement is "most accurate" about counterparty risk or other non-duration aspects

**Procedure:**
1. Identify the original position (e.g., floating-rate liability) and its interest rate characteristics
2. Identify the proposed swap (e.g., receive-floating/pay-fixed) and recognize it converts cash flows from floating to fixed
3. Distinguish between two separate effects: (a) Cash flow stabilization: swap DOES stabilize cash flows by converting floating payments to fixed. (b) Interest rate sensitivity: swap does NOT reduce overall sensitivity because the swap's market value changes with interest rates in the opposite direction of the liability
4. Recognize that the combined position (liability + swap) has similar interest rate sensitivity to a fixed-rate liability, not reduced sensitivity
5. Conclude: swap achieves cash flow hedging but maintains (or even increases) market value sensitivity to interest rates
6. When asked which statement is incorrect: focus on whether the claim is about "reducing both risks" or "reducing overall sensitivity"

**Common Mistakes to Avoid:**
- Applying this pattern when the question asks about specific risk types (cash flow vs market value) rather than overall sensitivity
- Confusing "reduces cash flow risk" (correct) with "reduces overall interest rate sensitivity" (incorrect)
- Using this pattern to evaluate counterparty risk statements (different domain)
- Not distinguishing between statements about individual risk components vs. combined position sensitivity

**Example (sanitized):**
> **Scenario:** Company has $100M floating-rate debt (duration -0.2). Analyst proposes receive-floating/pay-fixed swap (duration of swap = -3.0) to "reduce interest rate sensitivity of overall position."
> **Wrong approach:** Agreeing that the swap reduces sensitivity because it hedges the floating-rate exposure.
> **Correct approach:** (1) Original position: floating-rate debt has low duration (-0.2), low sensitivity to rate changes. (2) Swap: receive-floating/pay-fixed has duration -3.0, meaning swap value falls when rates rise. (3) Cash flow effect: swap converts floating payments to fixed → stabilizes cash flows ✓. (4) Sensitivity effect: combined duration ≈ -0.2 + (-3.0) = -3.2, HIGHER sensitivity than original -0.2. (5) The swap does NOT reduce interest rate sensitivity; it increases it while stabilizing cash flows. (6) Analyst is incorrect about reducing sensitivity.
## Pattern: Swaption Type Selection for Existing Swap Positions

**Description:** Confusion about which swaption type hedges or cancels an existing swap position. Critical distinction: (1) To HEDGE against adverse rate movements: payer swaption hedges anticipated pay-fixed needs against rising rates; receiver swaption hedges existing pay-fixed positions against falling rates. (2) To CANCEL/OFFSET an existing position: you need the OPPOSITE swaption type—receiver swaption to offset pay-fixed, payer swaption to offset receive-fixed. When evaluating multiple statements, explicitly verify EACH statement's recommendation against these rules.

**When to Use:** When selecting swaptions to hedge, cancel, or offset existing swap positions, or when evaluating which swaption protects against specific rate movements, or when assessing the correctness of multiple statements about swaption strategies (trigger: "payer swaption," "receiver swaption," "hedge swap," "protect against falling/rising rates," "existing pay-fixed position," "cancel swap," "offset swap," "which statement is least/most correct").

**Procedure:**
1. Identify the objective: (a) HEDGE against adverse rate movements, or (b) CANCEL/OFFSET an existing position
2. For HEDGING scenarios:
   - If you have/will have a pay-fixed swap and rates fall → you're paying above-market rates → need RECEIVER swaption to offset
   - If you anticipate needing a pay-fixed swap and rates rise → you'll pay above-target rates → need PAYER swaption to lock in rate
3. For CANCELING/OFFSETTING scenarios:
   - If you have an existing pay-fixed swap → need RECEIVER swaption (right to receive fixed) to create offsetting receive-fixed position
   - If you have an existing receive-fixed swap → need PAYER swaption (right to pay fixed) to create offsetting pay-fixed position
4. Verify the direction: 
   - Payer swaption = right to PAY fixed = benefits from rising rates = offsets receive-fixed positions
   - Receiver swaption = right to RECEIVE fixed = benefits from falling rates = offsets pay-fixed positions
5. Check the logic: matching swaption types to existing positions (payer-to-payer, receiver-to-receiver) COMPOUNDS exposure, not cancels it
6. **When evaluating multiple statements:**
   - Create a verification table with columns: Statement | Existing Position | Recommended Swaption | Correct Swaption | Match?
   - For EACH statement, explicitly identify: (a) what swap position exists, (b) what swaption is recommended, (c) what swaption should be used based on steps 2-4
   - Mark each statement as CORRECT or INCORRECT
   - When asked for "least correct" → select the INCORRECT statement
   - When asked for "most correct" → select the CORRECT statement
7. **Double-check your verification:**
   - If statement recommends payer swaption for pay-fixed position → INCORRECT (compounds exposure)
   - If statement recommends receiver swaption for pay-fixed position → CORRECT (offsets exposure)
   - If statement recommends payer swaption for receive-fixed position → CORRECT (offsets exposure)
   - If statement recommends receiver swaption for receive-fixed position → INCORRECT (compounds exposure)

**Example (sanitized):**
> **Scenario:** Company has entered a pay-fixed swap at 4.5%. Three statements: (1) "Purchase a receiver swaption to protect against falling rates." (2) "Purchase a payer swaption to protect against falling rates." (3) "Enter a new receive-fixed swap to cancel the position." Which statement is LEAST correct?
> **Wrong approach:** Selecting statement 3 because "entering a new swap introduces basis risk."
> **Correct approach:** (1) Create verification table. (2) Statement 1: Existing = pay-fixed, Recommended = receiver swaption, Correct = receiver swaption (to offset pay-fixed), Match = YES → CORRECT ✓. (3) Statement 2: Existing = pay-fixed, Recommended = payer swaption, Correct = receiver swaption (to offset pay-fixed), Match = NO → INCORRECT ✗. Payer swaption would create ANOTHER pay-fixed position, compounding exposure. (4) Statement 3: Entering receive-fixed swap directly offsets pay-fixed → CORRECT ✓ (though may have basis risk, it achieves the cancellation objective). (5) Statement 2 is LEAST correct because it recommends the wrong swaption type that would compound rather than offset the exposure. (6) Answer: Statement 2.

**Common Mistakes to Avoid:**
- Confusing hedging against rate movements with canceling/offsetting existing positions
- Assuming matching swaption types (payer-to-payer) provide protection or cancellation
- Not explicitly verifying EACH statement when multiple statements are presented
- Selecting answers based on secondary considerations (like basis risk) without first checking if the fundamental swaption type is correct
- Not distinguishing between "protect against falling rates" (receiver swaption for existing pay-fixed) and "cancel pay-fixed position" (also receiver swaption, but different reasoning)
```
## Pattern: Duration-Based Swap Notional Principal Calculation

**Description:** Failure to correctly calculate the notional principal required for an interest rate swap to achieve a target duration adjustment, leading to incorrect validation of proposed swap sizes. The notional must be calculated using the duration adjustment formula, and the comparison logic must correctly map calculated vs proposed values to answer choices.

**When to Use:** When evaluating or calculating the notional principal for interest rate swaps intended to adjust portfolio duration (trigger: "notional principal," "duration adjustment," "reduce duration from X to Y," "interest rate swap," "verify notional").

**Procedure:**
1. Identify the current portfolio duration (D_current) and target duration (D_target)
2. Calculate the required duration change: ΔD = D_current - D_target (always positive for duration reduction)
3. Identify the swap's duration (D_swap) - typically provided or calculated from swap maturity
4. Apply the notional principal formula: NP_calculated = (Portfolio Market Value × ΔD) / |D_swap|
   - Note: Use absolute value of swap duration since we're calculating magnitude
5. Compare the calculated notional to the proposed/recommended notional
6. **Apply correct comparison logic:**
   - If NP_calculated < NP_proposed → proposed notional is TOO HIGH (excessive) → Answer: "No, it is too high" or similar
   - If NP_calculated > NP_proposed → proposed notional is TOO LOW (insufficient) → Answer: "No, it is too low" or similar
   - If NP_calculated ≈ NP_proposed (within 2-3%) → Answer: "Yes" or "Correct"
7. **Map to answer choices carefully:**
   - "Too high" means the proposed amount exceeds what's needed
   - "Too low" means the proposed amount is less than what's needed
   - Double-check the answer choice wording matches your conclusion
8. Verify: do NOT validate by simply comparing duration values; the formula must be applied

**Common Mistakes to Avoid:**
- Reversing the comparison logic (saying "too high" when calculated > proposed)
- Not using absolute value of swap duration in calculations
- Confusing which value is calculated vs which is proposed
- Selecting the wrong answer choice due to misreading the comparison result

**Example (sanitized):**
> **Scenario:** Portfolio worth $800M has duration 8.5. Manager wants to reduce duration to 5.0 using a 6-year interest rate swap with duration -4.2. Proposed notional: $680M. Is this correct?
> **Wrong approach:** Comparing 8.5 - 5.0 = 3.5 to swap duration 4.2 and concluding the notional "seems reasonable."
> **Correct approach:** (1) Current duration = 8.5, target = 5.0, so ΔD = 3.5. (2) Swap duration = -4.2, use |4.2| = 4.2. (3) Required notional = ($800M × 3.5) / 4.2 = $2,800M / 4.2 = $667M. (4) Proposed notional = $680M. (5) Comparison: $667M (calculated) < $680M (proposed). (6) Since calculated < proposed, the proposed notional is TOO HIGH. (7) Answer: No, it is too high.

---
## Pattern: Beta Adjustment Effectiveness Verification

**Description:** When futures contracts are used to adjust portfolio beta, the effectiveness must be verified by calculating the realized beta from actual portfolio and market returns, not just by checking if the hedge was implemented. The effective beta is calculated as (Portfolio Return) / (Market Return), and this must be compared to the target beta using clear quantitative thresholds to determine if the adjustment was successful. This pattern applies to BOTH retrospective evaluation (was it effective?) and prospective validation (will it be effective?).

**When to Use:** When evaluating whether a futures-based beta adjustment strategy was effective, or when asked to assess the success of a hedging strategy that aimed to change portfolio beta, or when validating whether a proposed futures position will achieve a target beta (trigger: "effectiveness of futures transaction," "adjust portfolio beta," "effective beta," "target beta," "portfolio return vs market return," "will result in beta objective," "most likely attain," "achieve the target," "beta will be above/below target").

**Procedure:**
1. Identify the original portfolio beta, target beta, and the futures position taken (or proposed)
2. **For prospective validation (will it work?):**
   - Calculate required number of contracts: N = (Target Beta - Current Beta) × Portfolio Value / (Futures Beta × Futures Price × Multiplier)
   - Compare calculated N to proposed N
   - If proposed N < calculated N → beta will be BELOW target (under-hedged)
   - If proposed N > calculated N → beta will be ABOVE target (over-hedged)
   - If proposed N ≈ calculated N (within 5%) → will likely ATTAIN target
3. **For retrospective evaluation (did it work?):**
   - Obtain the actual portfolio return (R_p) and market return (R_m) during the period
   - Calculate effective beta: Effective Beta = R_p / R_m
   - Apply effectiveness thresholds (see step 4)
4. **Apply clear effectiveness thresholds:**
   - Calculate the difference: |Effective Beta - Target Beta|
   - If difference ≤ 0.10 → hedge was EFFECTIVE (within reasonable tolerance)
   - If 0.10 < difference ≤ 0.20 → hedge was PARTIALLY EFFECTIVE
   - If difference > 0.20 → hedge was INEFFECTIVE
5. Determine the direction of error:
   - If effective beta > target beta → hedge was insufficient (under-hedged)
   - If effective beta < target beta → hedge was excessive (over-hedged)
6. **For prospective questions:** select answer based on whether calculated contracts match proposed contracts
7. **For retrospective questions:** select answer based on effectiveness threshold criteria

**Common Mistakes to Avoid:**
- Assuming the hedge was effective just because futures contracts were sold
- Not calculating the effective beta from actual returns (retrospective) or required contracts (prospective)
- Confusing the target beta with the effective beta
- Making calculation errors when dividing portfolio return by market return (especially with negative values)
- Using vague criteria like "close to target" instead of quantitative thresholds
- Not distinguishing between prospective validation (will it work?) and retrospective evaluation (did it work?)
- Accepting that a hedge "will attain the objective" without verifying the contract calculation

**Example (sanitized):**
> **Scenario (Prospective):** Portfolio with $50M and beta 0.80 needs adjustment to target beta 1.20 using S&P 500 futures (beta 1.0, price $250,000). Manager proposes 60 contracts. Will this attain the objective?
> **Wrong approach:** Assuming 60 contracts will work because "it's a reasonable number for a $50M portfolio."
> **Correct approach:** (1) Calculate required contracts: N = (1.20 - 0.80) × $50M / (1.0 × $250,000) = 0.40 × $50M / $250,000 = 80 contracts. (2) Proposed = 60 contracts, Required = 80 contracts. (3) 60 < 80 → under-hedged. (4) The beta will be BELOW the target (insufficient contracts). (5) Answer: No, because the beta will be below the target.

---

## Pattern: Maximum Profit Calculation for Option Strategies

**Description:** Failure to calculate the maximum profit of option strategies numerically when the question explicitly asks for profit limits. Instead of performing the required arithmetic, focusing on qualitative features like "protection" or "upside potential" that don't answer the specific question about maximum profit.

**When to Use:** When asked about "maximum profit," "maximum gain," "profit cap," or similar quantitative profit limits for option strategies (trigger: "maximum profit," "offers a maximum," "profit of €X per share," "profit cap").

**Procedure:**
1. Identify all components of the strategy: stock purchase price, option strikes, premiums paid/received
2. Determine the price level at which maximum profit occurs (typically at the short option's strike for covered calls/collars)
3. Calculate maximum profit using the formula:
   - For covered call/collar: (Short Call Strike - Stock Purchase Price) + (Call Premium Received - Put Premium Paid)
   - For bull spread: (Higher Strike - Lower Strike) - Net Premium Paid
   - For bear spread: (Higher Strike - Lower Strike) - Net Premium Paid
4. Verify the calculation by checking what happens at the optimal price level
5. Express the result as a per-share amount
6. Compare to answer choices numerically

**Example (sanitized):**
> **Scenario:** Buy stock at $45, buy put at $42 strike for $1.20 premium, sell call at $50 strike for $0.80 premium. What is maximum profit per share?
> **Wrong approach:** "This strategy provides downside protection below $42 and limits upside above $50, so it offers protection characteristics."
> **Correct approach:** (1) Stock purchase: $45. (2) Put premium paid: $1.20. (3) Call premium received: $0.80. (4) Net premium: -$1.20 + $0.80 = -$0.40. (5) Maximum profit occurs when stock reaches $50 (short call strike). (6) Profit = ($50 - $45) - $0.40 = $5.00 - $0.40 = $4.60 per share. (7) Answer: Maximum profit is $4.60 per share.

**Common Mistakes to Avoid:**
- Describing qualitative features (protection, upside potential) when asked for numerical profit
- Forgetting to subtract net premium paid from the strike difference
- Not identifying the price level where maximum profit occurs
- Confusing maximum profit with breakeven or protection levels
```