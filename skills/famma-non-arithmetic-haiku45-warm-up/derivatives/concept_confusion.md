# Skill Patterns for Derivatives Concept Confusion Errors

## Pattern: Hedging Instrument Type vs. Hedging Objective

**Description:** Confusing the means (type of derivative instrument) with the end (achieving the hedging objective). Any instrument that effectively offsets the target risk meets the hedging objective, regardless of whether it's a forward, future, option, or swap.

**When to Use:** When evaluating whether different derivative strategies meet a stated hedging objective; trigger keywords: "hedge," "meet the objective," "protect against," "manage risk"

**Procedure:**
1. Identify the specific risk exposure to be hedged (e.g., short currency position, interest rate rise, equity price decline)
2. For each proposed strategy, determine whether it offsets the identified risk exposure, regardless of instrument type
3. Forwards/futures provide complete hedges by locking in prices; options provide asymmetric protection with premium cost
4. Do NOT eliminate strategies solely because they use forwards instead of options or vice versa
5. Verify: Does the strategy reduce or eliminate the stated risk? If yes, it meets the hedging objective

**Example (sanitized):**
> **Scenario:** A Canadian company has a payable of 1 million GBP due in 3 months and wants to hedge currency risk. Three strategies are proposed: (1) Buy GBP forward, (2) Buy GBP call option, (3) Enter currency swap to receive GBP.
> **Wrong approach:** Only strategies 2 and 3 meet the objective because they use derivatives with optionality or exchange features.
> **Correct approach:** All three strategies hedge the GBP exposure. Strategy 1 locks in the exchange rate completely. Strategy 2 provides upside if GBP weakens while protecting against strengthening. Strategy 3 exchanges cash flows to obtain GBP. Each effectively manages the currency risk through different mechanisms.

---

## Pattern: Currency Hedging Mechanics for Foreign Investments

**Description:** Misunderstanding that when investing in a foreign asset, shorting the foreign currency amount (principal × exchange rate) creates a synthetic quanto effect where foreign-denominated gains translate directly to domestic gains without additional exchange rate hedging needed on the gains themselves.

**When to Use:** When analyzing currency hedging strategies for foreign investments; trigger keywords: "invest in foreign index," "currency exposure," "hedge exchange rate risk," "short foreign currency"

**Procedure:**
1. Calculate the foreign currency amount obtained: domestic investment × exchange rate = foreign currency amount
2. If shorting exactly this foreign currency amount, recognize this creates a matched hedge
3. Understand that gains/losses in foreign currency (ΔS foreign units) are automatically converted to domestic currency (ΔS domestic units) because the short position neutralizes the conversion
4. Do NOT assume that gains require separate dynamic hedging when the short matches the investment amount
5. Verify: Investment of X domestic = XQ foreign, short XQ foreign → net position has no currency exposure on both principal and gains

**Example (sanitized):**
> **Scenario:** A U.S. investor puts $10,000 into a Japanese index when USD/JPY = 100, obtaining 1,000,000 yen. They simultaneously short 1,000,000 yen. If the index gains 50,000 yen, what is the dollar gain?
> **Wrong approach:** The 50,000 yen gain needs separate hedging because exchange rates fluctuate, so the dollar value is uncertain.
> **Correct approach:** The short yen position of 1,000,000 exactly offsets currency exposure. The 50,000 yen gain translates to $500 gain regardless of exchange rate movements because the short position neutralizes the conversion effect. Dollar gain = yen gain / initial rate = 50,000/100 = $500.

---

## Pattern: Swap Directionality for Exposure Management

**Description:** Reversing the mechanics of swaps: RECEIVING an asset return creates LONG/INCREASED exposure to that asset, while PAYING an asset return creates SHORT/DECREASED exposure. To reduce exposure, you must pay the return; to increase exposure, you must receive the return.

**When to Use:** When using swaps to rebalance portfolios or adjust asset allocation; trigger keywords: "equity swap," "rebalance," "increase/decrease allocation," "pay/receive return"

**Procedure:**
1. Identify the current allocation and the target allocation for each asset class
2. Determine which exposures need to increase and which need to decrease
3. For exposures to INCREASE: enter swap to RECEIVE that asset's return (and typically pay LIBOR or another benchmark)
4. For exposures to DECREASE: enter swap to PAY that asset's return (and typically receive LIBOR or another benchmark)
5. Verify: Receiving equity returns = adding equity exposure; paying equity returns = reducing equity exposure

**Example (sanitized):**
> **Scenario:** A pension fund has 70% stocks and 30% bonds, wants to shift to 60% stocks and 40% bonds. What swap structure achieves this?
> **Wrong approach:** Pay LIBOR and receive equity returns to reduce equity exposure; pay LIBOR and receive bond returns to increase bond exposure.
> **Correct approach:** To reduce equity from 70% to 60%, PAY equity returns and RECEIVE LIBOR. To increase bonds from 30% to 40%, RECEIVE bond returns and PAY LIBOR. The combination: (1) equity swap paying equity/receiving LIBOR, (2) bond swap receiving bonds/paying LIBOR.

---

## Pattern: Interest Rate Swap Impact on Market Value vs. Cash Flow Risk

**Description:** Failing to distinguish that swaps affect market value risk and cash flow risk differently depending on the original liability type. For floating-rate debt, a pay-fixed swap eliminates cash flow uncertainty but INCREASES market value risk (because floating debt has low duration, converting to fixed increases duration).

**When to Use:** When evaluating how interest rate swaps affect risk profiles; trigger keywords: "swap," "market value risk," "cash flow risk," "floating-rate," "fixed-rate"

**Procedure:**
1. Identify the original liability type: floating-rate or fixed-rate
2. Determine the swap structure: pay-fixed/receive-floating or pay-floating/receive-fixed
3. For floating-rate debt + pay-fixed swap: REDUCES cash flow risk (payments become predictable), INCREASES market value risk (low duration becomes high duration)
4. For fixed-rate debt + pay-floating swap: INCREASES cash flow risk (payments become variable), REDUCES market value risk (high duration becomes low duration)
5. Verify: Floating-rate instruments have minimal market value sensitivity; converting them to fixed increases this sensitivity

**Example (sanitized):**
> **Scenario:** A company has a $100M floating-rate loan (LIBOR + 1%) and enters a swap paying 4% fixed, receiving LIBOR. How does this affect market value risk and cash flow risk?
> **Wrong approach:** The swap reduces both market value risk and cash flow risk by converting to fixed payments.
> **Correct approach:** Cash flow risk is REDUCED because net payments are now fixed at 5% (4% swap + 1% spread). Market value risk is INCREASED because the original floating-rate loan had low duration (minimal value change with rates), but the synthetic fixed-rate position has higher duration (value changes significantly with rate movements).

---

## Pattern: Covered Call vs. Protective Put Floor Establishment

**Description:** Misunderstanding that only protective puts establish a true minimum value (floor) for a position, while covered calls provide limited downside cushion equal only to the premium received but do not create a floor (losses continue below strike minus premium).

**When to Use:** When comparing option strategies for downside protection; trigger keywords: "covered call," "protective put," "minimum value," "establish floor," "downside protection"

**Procedure:**
1. For protective put (long stock + long put): minimum value = put strike price (definitive floor regardless of how far stock falls)
2. For covered call (long stock + short call): downside cushion = premium received only; losses continue below (stock price - premium)
3. Covered calls do NOT establish a minimum value; they reduce cost basis but provide unlimited downside exposure minus premium
4. Protective puts DO establish minimum value at the strike price
5. Verify: If stock falls to zero, protective put holder receives strike; covered call holder loses (initial price - premium)

**Example (sanitized):**
> **Scenario:** An investor holds stock at $50. Strategy A: buy $45 put for $2. Strategy B: sell $55 call for $2. Which establishes a minimum portfolio value?
> **Wrong approach:** Both establish minimum values because both involve options that modify the risk profile.
> **Correct approach:** Only Strategy A (protective put) establishes a minimum value of $45 regardless of how far the stock falls. Strategy B (covered call) provides $2 cushion but no floor—if stock falls to $30, the portfolio value is $32 ($30 + $2 premium), not a fixed minimum. The covered call reduces losses but doesn't create a floor.

---

## Pattern: Short Option Gamma Sign

**Description:** Confusing the gamma sign between long and short option positions. Long options (buying calls or puts) have POSITIVE gamma (benefit from large moves). Short options (selling calls or puts, including short straddles) have NEGATIVE gamma (lose from large moves in either direction).

**When to Use:** When identifying option strategies from Greek exposures; trigger keywords: "gamma," "short straddle," "long straddle," "option seller," "Greek exposures"

**Procedure:**
1. Recall: Gamma measures convexity—how delta changes as the underlying moves
2. LONG options (buyer): positive gamma (delta becomes more favorable with movement)
3. SHORT options (seller): negative gamma (delta becomes less favorable with movement)
4. Short straddle (sell call + sell put): negative gamma, positive theta, negative vega, near-zero delta
5. Long straddle (buy call + buy put): positive gamma, negative theta, positive vega, near-zero delta
6. Verify: Option sellers want stability (negative gamma = hurt by large moves); buyers want movement (positive gamma = benefit from large moves)

**Example (sanitized):**
> **Scenario:** A strategy has: delta ≈ 0, gamma = -0.05, theta = +0.02, vega = -0.30. Identify the position.
> **Wrong approach:** Positive theta and negative vega suggest short volatility, and near-zero delta suggests straddle, so this could be either long or short straddle depending on other factors.
> **Correct approach:** NEGATIVE gamma definitively indicates SHORT options. Combined with near-zero delta, positive theta, and negative vega, this is a SHORT STRADDLE (sold both call and put). The negative gamma means the position loses when the underlying moves significantly in either direction, characteristic of option sellers.

---

## Pattern: Payer vs. Receiver Swaption Definitions

**Description:** Confusing the definitions of payer and receiver swaptions. A PAYER swaption gives the right to PAY FIXED and RECEIVE FLOATING. A RECEIVER swaption gives the right to RECEIVE FIXED and PAY FLOATING. The name refers to what you do with the fixed rate.

**When to Use:** When analyzing swaption strategies for interest rate hedging; trigger keywords: "payer swaption," "receiver swaption," "pay fixed," "receive fixed," "exercise rate"

**Procedure:**
1. PAYER swaption = right to enter swap where holder PAYS fixed rate and RECEIVES floating rate
2. RECEIVER swaption = right to enter swap where holder RECEIVES fixed rate and PAYS floating rate
3. To hedge against rising rates (for a borrower): buy PAYER swaption (locks in maximum fixed rate to pay)
4. To hedge against falling rates (for a lender): buy RECEIVER swaption (locks in minimum fixed rate to receive)
5. When calculating net interest after swaption exercise, account for BOTH the original loan rate AND the swap cash flows
6. Verify: Payer swaption exercised when market fixed rates > strike; net rate = original floating + (floating received - fixed paid) = original spread + strike

**Example (sanitized):**
> **Scenario:** A company will borrow at LIBOR + 0.75% in 2 months. They buy a payer swaption with strike 2.5% to receive LIBOR. If exercised, what is the net rate?
> **Wrong approach:** The payer swaption allows receiving LIBOR and paying 2.5%, so this is actually a receiver swaption, not a payer swaption.
> **Correct approach:** A payer swaption correctly gives the right to PAY 2.5% fixed and RECEIVE LIBOR. Net interest = (LIBOR + 0.75% on loan) + (LIBOR received - 2.5% paid on swap) = 0.75% + 2.5% = 3.25%, not 2.5%. The swaption caps the fixed component but the spread remains.

---

## Pattern: Market Price of Risk Under Numeraire Changes

**Description:** Incorrectly assuming that changing numeraire always results in zero market price of risk (as in traditional risk-neutral measure). When changing to a foreign currency bond numeraire or other non-standard numeraires, the market price of risk equals the correlation-weighted volatility components from the numeraire change, NOT zero.

**When to Use:** When pricing derivatives under different numeraire measures, especially cross-currency; trigger keywords: "change of numeraire," "market price of risk," "currency B bond," "risk-neutral world," "forward measure"

**Procedure:**
1. Traditional risk-neutral world (domestic money market numeraire): market price of risk = 0 for all variables
2. When changing to foreign currency bond numeraire: market price of risk ≠ 0
3. The market price of dz-risk under foreign bond numeraire = ρ_{SP}σ_P + ρ_{FS}σ_F, where P = bond price volatility, F = exchange rate volatility, ρ = correlations
4. This reflects combined interest rate risk and currency risk from the numeraire change
5. Do NOT apply single-currency risk-neutral principles to cross-currency numeraire changes
6. Verify: Cross-currency numeraire changes introduce drift terms from correlation structure between asset, foreign rates, and FX

**Example (sanitized):**
> **Scenario:** An asset S denominated in currency A follows dS = μS dt + σ dz. What is the market price of dz-risk when using a currency B zero-coupon bond as numeraire?
> **Wrong approach:** In any risk-neutral world defined by a bond numeraire, the market price of risk is zero by definition.
> **Correct approach:** Under currency B bond numeraire, market price of dz-risk = ρ_{SB}σ_B + ρ_{SQ}σ_Q, where B represents the bond price dynamics and Q represents the exchange rate. This is NOT zero because the numeraire change from currency A to B introduces correlation-based drift adjustments. Only in the domestic traditional risk-neutral world is the market price of risk zero.

---

## Pattern: Complete Hedging Requires Offsetting All Risk Components

**Description:** Failing to recognize that earning the risk-free rate requires eliminating ALL sources of risk through offsetting positions. For foreign investments, this means hedging BOTH equity/asset risk AND currency risk. Derivative positions must offset (not amplify) existing exposures.

**When to Use:** When evaluating hedging strategies to achieve risk-free returns; trigger keywords: "earn risk-free rate," "fully hedged," "eliminate risk," "foreign investment," "currency and equity exposure"

**Procedure:**
1. Identify ALL risk components in the current position (e.g., equity risk, currency risk, interest rate risk)
2. For each risk component, determine the existing exposure direction (long/short)
3. Design hedge positions that OFFSET each exposure: if long equity, sell equity futures/forwards; if long foreign currency, sell foreign currency
4. Verify each hedge: does it move opposite to the existing exposure?
5. Check that no hedge INCREASES an existing exposure (e.g., buying more of a currency you're already long)
6. Confirm: When all risks are offset, the position earns the domestic risk-free rate

**Example (sanitized):**
> **Scenario:** A U.S. investor holds unhedged Japanese stocks (long equity, long yen exposure). Three strategies: (1) Sell yen, buy Japanese stock futures; (2) Sell yen, sell Japanese stock futures; (3) Buy yen, sell Japanese stock futures. Which earns the U.S. risk-free rate?
> **Wrong approach:** Strategy 3 hedges by buying yen (to hedge currency) and selling stocks (to hedge equity), creating a balanced position.
> **Correct approach:** Strategy 2 is correct. The investor is LONG yen (unhedged foreign stocks), so must SELL yen to hedge currency risk. The investor is LONG Japanese equity, so must SELL Japanese stock futures to hedge equity risk. Strategy 3 INCREASES yen exposure (buying more yen when already long) rather than hedging it. Only Strategy 2 offsets both risks completely.

---

## Pattern: Compound Option Put-Call Parity Structure

**Description:** Failing to derive compound option put-call parity by recognizing that at the first expiration T₁, the underlying asset is itself an option, and the parity relationship must account for the value of receiving vs. not receiving that underlying option at strike K₁.

**When to Use:** When deriving or applying put-call parity for compound options; trigger keywords: "compound option," "call on call," "put on put," "put-call parity," "option on option"

**Procedure:**
1. Recall standard put-call parity: C - P = S - K·e^(-rT)
2. For compound options, the "underlying asset" at T₁ is an option (call or put) with value p
3. At T₁, call on call holder can pay K₁ to receive option worth p; put on call holder can sell option for K₁ if p < K₁
4. Compound option put-call parity: (call on call) - (put on call) = p - K₁·e^(-rT₁), or equivalently: (call on call) + K₁·e^(-rT₁) = (put on call) + p
5. For call on put and put on put, replace p with p_put (the value of the underlying put option)
6. Verify: The relationship equates two portfolios with identical payoffs at T₁

**Example (sanitized):**
> **Scenario:** A call on a call is worth $5, the strike K₁ = $10, risk-free rate = 2%, T₁ = 1 year. The underlying call option is currently worth $12. What is the put on call worth?
> **Wrong approach:** Use standard put-call parity: P = C - S + K·e^(-rT) = 5 - 12 + 10·e^(-0.02) = $2.80.
> **Correct approach:** Use compound option parity: call_on_call + K₁·e^(-rT₁) = put_on_call + p. Therefore: put_on_call = 5 + 10·e^(-0.02·1) - 12 = 5 + 9.80 - 12 = $2.80. The structure is similar but recognizes p (current option value) as the "underlying asset" in the compound option context.

## Pattern: Short Put Delta Sign and Directional Exposure

**Description:** Confusing the delta sign of short put positions. A SHORT put has POSITIVE delta (bullish exposure) because the position profits when the underlying rises, while a LONG put has negative delta (bearish exposure). Selling a put creates synthetic long exposure to the underlying.

**When to Use:** When analyzing option positions from Greek exposures or determining directional exposure from option strategies; trigger keywords: "short put," "delta," "Greek exposures," "option position," "directional exposure"

**Procedure:**
1. Identify whether the option position is long (bought) or short (sold)
2. For PUT options: long puts have negative delta (bearish), short puts have positive delta (bullish)
3. For CALL options: long calls have positive delta (bullish), short calls have negative delta (bearish)
4. Remember: selling/writing options reverses the delta sign compared to buying
5. Match the Greek profile (delta, gamma, theta, vega signs) to identify the strategy

**Example (sanitized):**
> **Scenario:** A position shows positive delta, negative gamma, positive theta, and negative vega. Determine if this could be a short put.
> **Wrong approach:** "A short put has negative delta because puts are bearish instruments, so this can't be a short put."
> **Correct approach:** "A short put has POSITIVE delta (bullish exposure - profits when underlying rises), negative gamma (loses from large moves), positive theta (benefits from time decay), and negative vega (profits from volatility decrease). This matches the Greek profile exactly, so this is a short put position."

## Pattern: Independent Evaluation of Multi-Part Derivative Claims

**Description:** Failing to evaluate each component of a multi-part derivative statement independently. When a question asks whether multiple aspects (e.g., swap type AND effect on risk) are correct, each claim must be assessed separately - one being wrong doesn't automatically make related claims wrong if they describe independent effects.

**When to Use:** When questions ask about correctness of multiple related but independent claims about derivative strategies; trigger keywords: "is correct with regard to," "YES/NO for both," "type AND effect," "strategy AND impact"

**Procedure:**
1. Identify all separate claims being made in the statement (e.g., swap direction, effect on risk, cost implications)
2. Evaluate each claim independently based on its own merits
3. For each claim, determine if it's factually correct regardless of other claims
4. Only mark a claim as wrong if the specific statement itself is incorrect, not because a related claim is wrong
5. Combine evaluations only at the final step to select the answer option

**Example (sanitized):**
> **Scenario:** An analyst states: "We should enter a receive-fixed swap to hedge floating-rate debt. This will reduce our interest rate sensitivity." Evaluate if the analyst is correct about (1) swap type and (2) effect on sensitivity.
> **Wrong approach:** "The swap type is wrong (should be pay-fixed), so the sensitivity claim must also be wrong. Answer: both NO."
> **Correct approach:** "Evaluate independently: (1) Swap type: WRONG - should pay-fixed to hedge floating debt. (2) Sensitivity effect: CORRECT - a pay-fixed swap does reduce interest rate sensitivity by converting floating to fixed. Answer: swap type NO, sensitivity YES."