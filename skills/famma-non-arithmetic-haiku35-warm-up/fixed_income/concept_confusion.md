# Skill Patterns for Fixed Income Concept Confusion Errors

## Pattern: Cross-Hedge Correlation Logic

**Description:** Cross-hedges work by exploiting correlation between the substitute hedging instrument and the original exposure being hedged, not correlation between either currency and the target currency. The substitute must move in tandem with the original exposure to effectively offset risk.

**When to Use:** Questions involving cross-hedging, proxy hedging, or using alternative instruments when direct hedging markets are illiquid. Keywords: "cross hedge," "inactive market," "alternative currency," "proxy."

**Procedure:**
1. Identify the original exposure being hedged (e.g., NOK currency risk from a Norwegian bond investment)
2. Identify the substitute hedging instrument (e.g., SEK forward contract)
3. Recognize that the cross-hedge effectiveness depends on correlation between the original exposure and the substitute (NOK and SEK), NOT between either currency and the target currency (USD)
4. When NOK depreciates against USD, SEK must move similarly (high NOK-SEK correlation) for the SEK forward to offset losses
5. The correlation to the target currency is irrelevant—what matters is whether the two non-target currencies move together
6. Select the answer that identifies high correlation between the exposure currency and the substitute hedging currency

**Example (sanitized):**
> **Scenario:** A UK investor holds Brazilian real (BRL) bonds but finds the BRL forward market illiquid. They consider using Mexican peso (MXN) forwards to hedge back to GBP.
> **Wrong approach:** The hedge works if both BRL and MXN are highly correlated with GBP, ensuring movements track the target currency.
> **Correct approach:** The hedge works if BRL and MXN are highly correlated with each other. When BRL depreciates against GBP, MXN typically moves similarly if correlation is high, making MXN forward gains/losses offset BRL exposure changes. GBP correlation is irrelevant.

---

## Pattern: Multiple Liability Immunization Convexity Requirements

**Description:** For immunizing multiple liabilities, asset portfolio convexity must be greater than or equal to liability convexity to ensure asset value changes exceed liability value changes under any yield curve shift. Lower asset convexity than liability convexity violates immunization conditions.

**When to Use:** Questions about immunization portfolios for multiple liabilities, duration matching with convexity constraints. Keywords: "immunization," "multiple liabilities," "convexity," "duration matching."

**Procedure:**
1. Identify the liability portfolio's convexity measure
2. For each candidate asset portfolio, compare its convexity to the liability convexity
3. Recognize that asset convexity < liability convexity creates structural risk: non-parallel yield shifts can cause asset values to change less than liability values
4. The correct immunization portfolio must have: (a) matched duration, (b) convexity ≥ liability convexity, and (c) similar cash flow yield
5. Portfolios with convexity below the liability convexity fail to meet immunization requirements
6. Do not penalize portfolios for having higher convexity—this provides a cushion against yield curve risk

**Example (sanitized):**
> **Scenario:** A pension fund has liabilities with duration 6.2 years and convexity 28.5. Three portfolios all have duration 6.2: Portfolio X (convexity 26.1), Portfolio Y (convexity 30.2), Portfolio Z (convexity 45.8).
> **Wrong approach:** Portfolio Z fails because its convexity (45.8) deviates most from the liability convexity (28.5).
> **Correct approach:** Portfolio X fails because its convexity (26.1) is below the liability convexity (28.5). When yields shift non-parallel, Portfolio X's value changes will be smaller than liability changes, creating funding risk. Portfolios Y and Z meet requirements because their higher convexity provides protection.

---

## Pattern: Callable Bond Performance in Declining Rate Environments

**Description:** Callable bonds underperform bullet bonds when interest rates decline because issuers exercise call options to refinance at lower rates, limiting investor price appreciation and creating reinvestment risk. The embedded call option works against bondholders in falling rate scenarios.

**When to Use:** Questions about callable bond performance expectations, interest rate scenarios, embedded option impacts. Keywords: "callable bonds," "declining rates," "secular decline," "outperform," "embedded options."

**Procedure:**
1. Identify the interest rate scenario (rising, falling, or stable)
2. Recognize that callable bonds contain an embedded short call option position for investors
3. In declining rate environments: issuers are more likely to call bonds to refinance at lower rates
4. When bonds are called, investors face: (a) limited price appreciation (capped near call price), (b) reinvestment risk at lower prevailing rates
5. Bullet bonds without call features capture full price appreciation as rates fall
6. Therefore, callable bonds underperform bullets when rates decline; they may outperform when rates rise (call option has no value, but higher coupon compensates)
7. Putable bonds provide protection when rates rise (investors can put bonds back), not when rates fall

**Example (sanitized):**
> **Scenario:** An analyst expects a prolonged period of declining interest rates and evaluates whether callable corporate bonds will outperform non-callable bonds.
> **Wrong approach:** Callable bonds will outperform because the embedded options provide flexibility in changing rate environments.
> **Correct approach:** Callable bonds will underperform. As rates decline, issuers will call the bonds to refinance at lower rates. Investors lose potential price appreciation (capped at call price) and must reinvest proceeds at the new lower rates. Non-callable bonds capture full price gains from falling rates.

---

## Pattern: Benchmark Selection for Market Risk Matching

**Description:** When selecting bond benchmarks, market risk matching requires similar duration and interest rate sensitivity between portfolio and benchmark, not directional forecasts about total return potential. Confusing duration's role as a risk measure with return forecasting leads to incorrect benchmark selection criteria.

**When to Use:** Questions about benchmark bond index selection criteria, portfolio-benchmark matching, duration considerations. Keywords: "benchmark selection," "market risk," "duration," "similar characteristics."

**Procedure:**
1. Identify stated criteria for benchmark selection in the question
2. Recognize that market risk matching means the portfolio and benchmark should have similar sensitivity to interest rate changes (duration, convexity)
3. Duration is a risk measure (price sensitivity to rate changes), not a return forecasting tool
4. Statements like "longer duration = greater return potential because rates are low" confuse risk measurement with directional betting
5. Correct market risk criterion: portfolio and benchmark durations should be similar to ensure comparable interest rate exposure
6. Income risk matching requires similar cash flow patterns and maturity structures for stable, comparable income streams
7. Reject criteria that use duration to make return forecasts rather than match risk characteristics

**Example (sanitized):**
> **Scenario:** A manager selects a benchmark and states: "Market risk is properly matched because both have duration near 7 years. The longer duration provides greater return potential given current low rates."
> **Wrong approach:** Accept the statement because duration matching ensures similar market risk.
> **Correct approach:** The market risk statement is incorrect. While duration matching (7 years) is correct for risk matching, the claim about "greater return potential from longer duration given low rates" is a directional forecast, not a risk-matching criterion. Duration measures sensitivity, not expected returns.

---

## Pattern: Interest Rate Swap Directional Positioning

**Description:** Receive-fixed swaps create long duration exposure (equivalent to owning bonds), while pay-fixed swaps create short duration exposure (equivalent to shorting bonds). In rising rate environments, pay-fixed positions profit; in falling rate environments, receive-fixed positions profit.

**When to Use:** Questions about using swaps to express interest rate views, duration adjustment via swaps, bear/bull flattening strategies. Keywords: "receive-fixed," "pay-fixed," "swap," "duration," "bear flattening," "rising rates."

**Procedure:**
1. Identify the interest rate scenario or view (rates rising, falling, steepening, flattening)
2. Understand swap mechanics: receive-fixed = long bond position (gains when rates fall), pay-fixed = short bond position (gains when rates rise)
3. For bear flattening (short rates rise more than long rates): profit by being short the short end (pay-fixed on short maturity) and long the long end (receive-fixed on long maturity)
4. For bull flattening (short rates fall more than long rates): opposite positioning
5. Match the swap position to the rate view: rising rates → pay-fixed, falling rates → receive-fixed
6. Verify the maturity of the swap matches the part of the curve where the view is expressed

**Example (sanitized):**
> **Scenario:** A manager expects short-term rates to rise significantly while long-term rates remain stable (bear flattening). Which swap position benefits?
> **Wrong approach:** Enter a receive-fixed swap on short maturities to hedge against rising rates.
> **Correct approach:** Enter a pay-fixed swap on short maturities. Pay-fixed means paying fixed and receiving floating, equivalent to shorting a bond. When short rates rise, the fixed payments become relatively cheaper, generating profit. Receive-fixed would create long exposure that loses value when rates rise.

---

## Pattern: Option Asymmetry in Hedging Strategies

**Description:** Protective puts provide asymmetric payoffs (limited downside, unlimited upside), making them superior when directional views are uncertain. Covered calls limit upside potential in exchange for premium income. Swaps provide symmetric linear exposure without asymmetry.

**When to Use:** Questions comparing hedging alternatives (swaps vs. options), evaluating statements about protective puts or covered calls. Keywords: "protective put," "covered call," "hedging," "upside," "downside protection."

**Procedure:**
1. Identify the hedging alternatives being compared (swaps, protective puts, covered calls)
2. Recognize the payoff profiles: (a) swaps = linear/symmetric, (b) protective puts = limited downside + unlimited upside, (c) covered calls = limited upside + full downside
3. Protective puts are advantageous when uncertain about direction: they hedge downside risk while preserving upside if the view is wrong
4. Covered calls generate premium income but sacrifice upside potential—the "cost" is opportunity cost, not cash premium
5. Swaps efficiently modify duration but provide no asymmetry or protection if the view reverses
6. Evaluate statements about "more upside if wrong" (favors protective puts) vs. "no premium cost" (misleading for covered calls—upside is sacrificed)

**Example (sanitized):**
> **Scenario:** A manager expects rates to rise but wants protection if wrong. Three alternatives: (1) pay-fixed swap, (2) buy protective put on bonds, (3) write covered call on bonds.
> **Wrong approach:** The swap is best because it directly adjusts duration without option premium costs.
> **Correct approach:** The protective put is best for uncertain views. It limits losses if rates rise (put gains value) while preserving gains if rates fall instead (put expires worthless, bond appreciates). The swap has symmetric exposure with no protection if wrong. The covered call limits upside if rates fall.

---

## Pattern: Tracking Error from Spread Duration Contribution

**Description:** In duration-matched fixed-income portfolios, tracking error primarily arises from differences in contribution to spread duration (sector weight × sector duration), not from simple sector weight differences. Spread duration contribution measures exposure to credit spread changes.

**When to Use:** Questions about tracking error sources, portfolio-benchmark comparison, sector allocation impacts. Keywords: "tracking error," "spread duration," "contribution," "sector allocation."

**Procedure:**
1. Locate the contribution to spread duration for each sector in both portfolio and benchmark
2. Calculate the absolute difference in spread duration contribution for each sector
3. Recognize that spread duration contribution = sector weight × sector duration × sector spread
4. The sector with the largest difference in spread duration contribution poses the most tracking error risk
5. Do not focus solely on weight differences—a small weight difference in a high-duration sector can create more tracking error than a large weight difference in a low-duration sector
6. Sectors with zero spread (Treasuries) contribute zero to spread duration regardless of weight differences

**Example (sanitized):**
> **Scenario:** Portfolio vs. Benchmark: Treasuries (25% vs. 28%, duration 4.0, spread contribution 0 vs. 0), Corporates (50% vs. 48%, duration 6.5, spread contribution 1.95 vs. 2.34), MBS (25% vs. 24%, duration 3.2, spread contribution 0.80 vs. 0.77).
> **Wrong approach:** MBS has the smallest weight difference, so it poses least tracking error.
> **Correct approach:** Corporates pose the most tracking error. The spread duration contribution difference is 0.39 (2.34 - 1.95) for corporates vs. 0.03 (0.80 - 0.77) for MBS. Despite similar weight allocations, the corporates' higher duration and larger spread contribution difference create greater tracking error exposure.

---

## Pattern: Reinvestment Risk and Cash Flow Yield Relationship

**Description:** Cash flow reinvestment risk is inversely related to cash flow yield. Lower cash flow yield means interim cash flows (coupons) will be reinvested at lower rates, creating higher reinvestment risk and greater uncertainty in achieving target returns.

**When to Use:** Questions comparing portfolios for immunization, reinvestment risk assessment, cash flow yield interpretation. Keywords: "reinvestment risk," "cash flow yield," "immunization," "interim cash flows."

**Procedure:**
1. Identify the cash flow yield for each portfolio being compared
2. Recognize that cash flow yield represents the internal rate of return assuming all cash flows are reinvested at that rate
3. Lower cash flow yield = higher reinvestment risk because: (a) interim coupons must be reinvested at the lower rate to achieve the target return, (b) any deviation from this reinvestment rate has larger impact
4. Higher cash flow yield = lower reinvestment risk because the portfolio is less dependent on favorable reinvestment rates
5. For immunization purposes, compare cash flow yields: the portfolio with lower yield has higher reinvestment risk
6. Do not confuse maturity structure with reinvestment risk—focus on the yield at which cash flows must be reinvested

**Example (sanitized):**
> **Scenario:** Two duration-matched portfolios: Portfolio A (cash flow yield 2.8%), Portfolio B (cash flow yield 3.6%). Which has higher reinvestment risk?
> **Wrong approach:** Portfolio B has higher reinvestment risk because its higher yield means more cash flows to reinvest.
> **Correct approach:** Portfolio A has higher reinvestment risk. Its lower cash flow yield (2.8%) means interim coupons must be reinvested at this lower rate to achieve the target return. If actual reinvestment rates differ, Portfolio A's return is more sensitive to the deviation. Portfolio B's higher yield (3.6%) reduces dependence on favorable reinvestment conditions.

---

## Pattern: Liability Type Classification by Certainty

**Description:** Fixed-income liabilities are classified by certainty of amount and timing: Type I (known amount, known timing), Type II (known amount, uncertain timing), Type III (uncertain amount). Deterministic payment schedules with fixed amounts and dates are Type I.

**When to Use:** Questions about liability classification, asset-liability management, immunization strategy selection. Keywords: "liability type," "known amount," "known timing," "payment schedule."

**Procedure:**
1. Examine the liability payment schedule for amount certainty and timing certainty
2. Type I: both amount and timing are known (e.g., fixed bond payments on fixed dates)
3. Type II: amount is known but timing is uncertain (e.g., callable bonds where call date is uncertain)
4. Type III: amount is uncertain (e.g., defined benefit pension with unknown future salary growth)
5. For fixed-rate bonds with no embedded options and specified maturity dates, both amount and timing are deterministic → Type I
6. Do not confuse declining payment amounts with uncertainty—if the schedule specifies exact amounts on exact dates, it remains Type I

**Example (sanitized):**
> **Scenario:** A company has debt obligations of $5 million due in Year 1, $4 million in Year 2, and $3 million in Year 3. The bonds have no call provisions. Classify the liabilities.
> **Wrong approach:** Type II because the amounts decline over time, suggesting some uncertainty in the payment structure.
> **Correct approach:** Type I. Both the amounts ($5M, $4M, $3M) and timing (Year 1, 2, 3) are known with certainty. The declining amounts are part of the predetermined schedule. No embedded options create timing uncertainty, and amounts are contractually fixed.

---

## Pattern: Zero-Coupon Bond Hold-to-Maturity Return Certainty

**Description:** Zero-coupon bonds held to maturity have locked-in returns regardless of subsequent yield changes because there are no interim cash flows to reinvest and no mark-to-market risk at maturity. Only bonds sold before maturity face price risk from yield changes.

**When to Use:** Questions about zero-coupon bond strategies, buy-and-hold vs. rolldown strategies, impact of yield changes on returns. Keywords: "zero-coupon," "hold to maturity," "buy-and-hold," "yield changes," "rolldown."

**Procedure:**
1. Identify whether the bond is held to maturity or sold before maturity
2. For zero-coupon bonds held to maturity: the return equals the initial yield-to-maturity regardless of subsequent yield movements
3. No reinvestment risk exists (no coupons to reinvest) and no price risk at maturity (bond pays face value)
4. For bonds sold before maturity (rolldown strategies): returns are affected by yield changes because the bond must be sold at prevailing market prices
5. When yields rise after purchase: hold-to-maturity returns unchanged, sell-before-maturity returns decrease (lower sale price)
6. When yields fall after purchase: hold-to-maturity returns unchanged, sell-before-maturity returns increase (higher sale price)

**Example (sanitized):**
> **Scenario:** Two strategies with 1-year horizon: (A) buy 1-year zero at 2% yield, hold to maturity; (B) buy 3-year zero at 3% yield, sell after 1 year. If yields rise 1% across the curve, how do returns change?
> **Wrong approach:** Both strategies' returns decrease because rising yields reduce bond prices.
> **Correct approach:** Strategy A's return is unchanged at 2%—the 1-year zero held to maturity pays face value regardless of yield changes. Strategy B's return decreases because the 3-year bond (now 2-year) must be sold at a lower price reflecting the higher yield environment. Only the rolldown strategy faces mark-to-market risk.

---

## Pattern: Total Return Framework for Secondary Market Trades

**Description:** All secondary market bond trades should be evaluated in a total return framework (price change + coupon income + reinvestment + currency effects), not solely on yield or spread pickup. Evaluating trades only on yield enhancement ignores price appreciation/depreciation potential.

**When to Use:** Questions about evaluating bond trades, yield pickup trades, credit trades, total return analysis. Keywords: "secondary market," "yield pickup," "spread pickup," "total return," "trade evaluation."

**Procedure:**
1. Identify the type of secondary market trade being evaluated (yield pickup, credit-upside, curve-adjustment, etc.)
2. Recognize that modern fixed-income management evaluates all trades on total return = (ending price - beginning price + coupon income) / beginning price
3. Yield or spread pickup alone is insufficient because it ignores: (a) potential price changes from yield curve shifts, (b) credit spread changes, (c) currency movements
4. A bond with higher yield may have lower total return if its price declines more than the yield advantage
5. Reject statements that certain trade types should be evaluated "solely on yield" or "in the context of additional yield"
6. Apply total return framework consistently across all trade types for proper comparison

**Example (sanitized):**
> **Scenario:** An analyst evaluates two trades: (1) credit-upside trade expecting rating upgrade, (2) yield pickup trade swapping into higher-yielding sector. The analyst says credit trades use total return but yield pickup trades should focus on additional yield.
> **Wrong approach:** Accept the distinction—yield pickup trades are simpler and should focus on yield enhancement.
> **Correct approach:** Both trades require total return evaluation. The yield pickup trade must consider: will the higher yield compensate for potential price decline if spreads widen? Total return = yield advantage - price change from spread/curve movements. Evaluating only on yield ignores the risk that spread widening could produce negative total returns despite higher yield.

---

## Pattern: Barbell vs. Bullet Convexity Comparison

**Description:** Barbell portfolios (combining short and long maturities) typically have higher convexity than bullet portfolios (single intermediate maturity) with the same duration. The dispersion of cash flows around the duration point increases convexity, and long-maturity bonds' high convexity dominates when weighted by present value.

**When to Use:** Questions comparing portfolio convexity, barbell vs. bullet strategies, immunization portfolio selection. Keywords: "barbell," "bullet," "convexity," "duration matching," "cash flow dispersion."

**Procedure:**
1. Identify the portfolio structures: barbell (short + long maturities) vs. bullet (intermediate maturity)
2. Recognize that convexity measures the curvature of the price-yield relationship (second derivative)
3. For equal-duration portfolios: convexity increases with cash flow dispersion around the duration point
4. Barbell portfolios have cash flows concentrated at short and long maturities → high dispersion → high convexity
5. Bullet portfolios have cash flows concentrated near the duration point → low dispersion → low convexity
6. The long-maturity bond in a barbell has very high convexity that dominates the weighted average, even though the short bond has low convexity
7. Calculate portfolio convexity as present-value-weighted average of individual bond convexities

**Example (sanitized):**
> **Scenario:** Portfolio X: 50% in 2-year bonds (convexity 3) + 50% in 10-year bonds (convexity 80), duration 6. Portfolio Y: 100% in 6-year bonds (convexity 35), duration 6. Which has higher convexity?
> **Wrong approach:** Portfolio Y has higher convexity because the 2-year bonds in Portfolio X have very low convexity (3), pulling down the average.
> **Correct approach:** Portfolio X (barbell) has higher convexity. The present-value-weighted average convexity is dominated by the 10-year bond's high convexity (80). The dispersion of cash flows (2-year and 10-year vs. concentrated at 6-year) creates higher curvature in the price-yield relationship, resulting in convexity well above Portfolio Y's 35.

## Pattern: Expected Excess Return Calculation in Credit Markets

**Description:** Expected excess return from credit securities equals the option-adjusted spread (OAS) minus expected loss (probability of default × loss given default), not the absolute spread level. Higher spreads do not automatically mean higher excess returns if expected losses are proportionally high.

**When to Use:** Questions involving credit portfolio optimization, comparing bonds across rating categories, active credit allocation decisions, or evaluating risk-adjusted returns. Keywords: "excess return," "OAS," "expected loss," "POD," "LGD," "credit allocation," "rating categories."

**Procedure:**
1. For each credit security or rating category, identify the OAS and expected loss (POD × LGD)
2. Calculate expected excess return = OAS - Expected Loss for each option
3. If spread duration differs across securities, calculate excess return per unit of duration = (OAS - Expected Loss) / Spread Duration
4. Select the portfolio allocation that maximizes the weighted average expected excess return
5. Verify that higher absolute spreads are not being confused with higher excess returns—the net compensation after losses is what matters

**Example (sanitized):**
> **Scenario:** Three bond categories: Category X (OAS 0.80%, Expected Loss 0.08%, Duration 6), Category Y (OAS 1.50%, Expected Loss 0.60%, Duration 5), Category Z (OAS 2.40%, Expected Loss 2.10%, Duration 4). Which 50-50 allocation maximizes excess return?
> **Wrong approach:** Choose Y and Z because they have higher absolute spreads (1.50% and 2.40%), assuming higher spreads mean better returns.
> **Correct approach:** Calculate excess returns: X = 0.80% - 0.08% = 0.72%, Y = 1.50% - 0.60% = 0.90%, Z = 2.40% - 2.10% = 0.30%. Category X and Y provide the highest excess returns. A 50-50 allocation between X and Y maximizes expected excess return at 0.81% average.

---

## Pattern: Covered Interest Rate Parity and Forward Hedging Decision

**Description:** When hedging foreign currency exposure with forward contracts, the hedged return equals the foreign asset return plus the forward premium/discount, which is approximated by the interest rate differential (domestic rate - foreign rate), not the expected spot rate change. The hedging decision compares hedged return to unhedged expected return.

**When to Use:** Questions about currency hedging decisions, forward contract usage, comparing hedged vs. unhedged returns, international bond investments. Keywords: "currency hedge," "forward contract," "hedged return," "interest rate differential," "forward premium," "covered interest parity."

**Procedure:**
1. Calculate unhedged expected return = foreign asset return + expected currency appreciation/depreciation
2. Calculate forward premium/discount ≈ domestic risk-free rate - foreign risk-free rate
3. Calculate hedged return = foreign asset return + forward premium/discount (or equivalently: foreign asset return - (foreign rate - domestic rate))
4. Compare hedged return to unhedged expected return
5. Hedge if hedged return > unhedged expected return; do not hedge if hedged return < unhedged expected return
6. Do not confuse expected spot rate changes with forward rate pricing—forward rates are determined by interest rate differentials, not spot expectations

**Example (sanitized):**
> **Scenario:** Foreign bond yields 6.5%, foreign risk-free rate 2.5%, domestic risk-free rate 0.4%, expected currency depreciation -0.3%. Should you hedge?
> **Wrong approach:** Hedged return = 6.5% - 0.3% = 6.2%, so hedge to lock in this return.
> **Correct approach:** Unhedged expected return = 6.5% - 0.3% = 6.2%. Forward discount ≈ 2.5% - 0.4% = 2.1%. Hedged return = 6.5% - 2.1% = 4.4%. Since 6.2% > 4.4%, do not hedge—the unhedged position offers higher expected return.

---

## Pattern: Identifying Correct vs. Incorrect Statements in Structured Products

**Description:** When asked which statement is "correct" or which person is "most likely correct," evaluate the factual accuracy of each statement about bond structures, not which strategy is most advantageous. Putable bonds protect against both interest rate rises AND credit deterioration (allowing early redemption), while callable bonds are disadvantageous during high volatility (issuer likely to call).

**When to Use:** Questions asking to identify correct statements, evaluate advisor recommendations, or assess accuracy of claims about embedded options. Keywords: "most likely correct," "which statement," "putable bonds," "callable bonds," "embedded options," "protect against."

**Procedure:**
1. Read the question carefully to determine if it asks for factual correctness vs. strategic advantage
2. For each statement, evaluate its technical accuracy independent of strategic merit
3. For putable bonds: verify they protect against BOTH rising rates (put at par) AND credit events (early redemption option)
4. For callable bonds: verify they are disadvantageous to holders during high volatility (issuer more likely to call) and limit upside
5. For bullet structures: verify they represent bonds without embedded options, often used in barbell strategies
6. Select the statement that is factually accurate, even if other options describe more profitable strategies

**Example (sanitized):**
> **Scenario:** An advisor states: "Callable bonds benefit investors during high volatility. Putable bonds protect against rate rises but not credit events. Bullet bonds are used in barbell strategies."
> **Wrong approach:** Choose callable bonds because they offer spread premiums and seem advantageous.
> **Correct approach:** Evaluate accuracy: Callable statement is FALSE (callables hurt investors in high volatility). Putable statement is FALSE (putables DO protect against credit events). Bullet statement is TRUE (bullets are used in barbells). The correct answer is the bullet statement.

---

## Pattern: Single-Period Immunization Complete Requirements

**Description:** Single-period immunization requires three conditions, not just two: (1) duration of assets equals investment horizon, (2) present value of assets equals present value of liabilities, and (3) convexity is minimized or cash flows are concentrated around the horizon date. Omitting the convexity/dispersion requirement leaves the portfolio vulnerable to non-parallel yield curve shifts.

**When to Use:** Questions about immunization strategy requirements, necessary conditions for liability matching, single-period immunization setup, or evaluating immunization proposals. Keywords: "immunization," "necessary conditions," "single-period," "investment horizon," "duration matching," "sufficient conditions."

**Procedure:**
1. Verify that duration of asset portfolio equals the liability duration or investment horizon
2. Verify that present value of assets equals present value of liabilities (or yield to maturity equals target yield)
3. Check if convexity minimization or cash flow concentration is mentioned—this is the third critical requirement
4. Recognize that duration matching alone only protects against small parallel shifts in the yield curve
5. Understand that minimizing convexity (or minimizing dispersion of cash flows around the horizon) protects against larger and non-parallel shifts
6. If the proposal omits convexity considerations, it is incomplete and incorrect

**Example (sanitized):**
> **Scenario:** A manager proposes immunization by: (1) matching portfolio duration to the 5-year horizon, and (2) ensuring yield to maturity equals the 3.5% target. Is this sufficient?
> **Wrong approach:** Yes, these two conditions ensure immunization will work.
> **Correct approach:** No, the proposal is incomplete. While duration matching and yield matching are necessary, the manager must also minimize convexity or concentrate cash flows around year 5. Without this third condition, non-parallel yield curve shifts could cause the portfolio to miss its target value. The proposal is incorrect regarding bond portfolio characteristics.

---

## Pattern: Contingent Claim Risk in Mortgage-Backed Securities

**Description:** Mortgage-backed securities contain embedded prepayment options (contingent claims) that create negative convexity and asymmetric risk profiles distinct from general interest rate risk. Prepayment risk represents a contingent claim that borrowers hold against MBS holders, not simply interest rate sensitivity.

**When to Use:** Questions about risks in MBS portfolios, distinguishing types of risk in fixed-income securities, embedded option identification, or convexity concerns with mortgage securities. Keywords: "mortgage-backed securities," "MBS," "prepayment," "negative convexity," "contingent claim," "embedded option."

**Procedure:**
1. Recognize that MBS contain embedded call options (prepayment options) held by borrowers
2. Understand that prepayment risk is a contingent claim risk, not merely interest rate risk
3. Identify that prepayment accelerates when rates fall (borrowers refinance), creating negative convexity
4. Distinguish contingent claim risk (option-like payoffs) from general interest rate risk (duration-based sensitivity)
5. Note that cap risk applies to floating-rate securities with explicit caps, not MBS
6. When MBS convexity concerns are raised, recognize the underlying issue is the contingent claim embedded in the prepayment option

**Example (sanitized):**
> **Scenario:** A portfolio manager notes substantial MBS holdings and recommends reallocation to match convexity with liabilities. What risk is being addressed?
> **Wrong approach:** Interest rate risk, because MBS are sensitive to rate changes and convexity relates to duration.
> **Correct approach:** Contingent claim risk. MBS contain embedded prepayment options (borrowers can refinance when rates fall), which are contingent claims. This creates negative convexity—when rates fall, prepayments accelerate and limit upside. The manager's concern about convexity matching specifically addresses the asymmetric, option-like behavior of MBS, which is contingent claim risk, not general interest rate risk.