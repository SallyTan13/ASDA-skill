# Skill Patterns for Missed Constraints Error Type

## Pattern: IPS_Policy_Limits_Constraint

**Description:** Tactical asset allocation (TAA) decisions must operate within the strategic asset allocation (SAA) policy limits defined in the Investment Policy Statement. TAA involves bounded optimization where adjustments can only occur within permitted ranges, not unconstrained maximization of expected returns.

**When to Use:** Questions involving tactical asset allocation, portfolio rebalancing, or asset class weight adjustments where policy limits, IPS constraints, or upper/lower bounds are mentioned.

**Procedure:**
1. Identify all policy constraints: locate the strategic asset allocation table showing current weights, target weights, lower limits, and upper limits for each asset class
2. Calculate available adjustment room: for each asset class, determine how much the allocation can increase (upper limit minus current weight) or decrease (current weight minus lower limit)
3. Rank opportunities by expected excess return while noting the maximum feasible adjustment for each asset class
4. Select the combination that maximizes expected return subject to: (a) staying within policy limits, (b) achieving the required net change in allocation
5. Verify that the proposed allocation does not violate any stated constraint, even if it appears to offer higher returns
6. Reject any option that requires exceeding upper limits or going below lower limits, regardless of return forecasts

**Example (sanitized):**
> **Scenario:** A pension fund has current allocation: Equities 40% (policy range 30-50%), Bonds 50% (policy range 40-60%), Alternatives 10% (policy range 5-15%). Expected excess returns: Equities +6%, Bonds +2%, Alternatives +8%.
> **Wrong approach:** Maximize Alternatives (highest return at +8%) by increasing to 20% and reducing Bonds to 40%, ignoring that Alternatives' upper limit is 15%.
> **Correct approach:** (1) Check constraints: Alternatives can only increase to 15% (max +5% from current 10%). (2) Equities can increase to 50% (max +10% from current 40%). (3) Best feasible strategy: increase Equities to 50% (+10% × 6% = 0.6% contribution) and Alternatives to 15% (+5% × 8% = 0.4% contribution), decrease Bonds to 35% (still above 30% lower limit). (4) Verify all allocations sum to 100% and stay within ranges.

---

## Pattern: Missing_Critical_Parameter_Recognition

**Description:** When a formula or model requires specific input parameters that are not provided in the problem data, recognize data insufficiency as a valid answer state rather than assuming typical values or estimating missing parameters.

**When to Use:** Questions involving CAPM, SML, valuation models, or any formula-based calculation where "insufficient data" is an answer option; trigger when key parameters (risk-free rate, growth rate, etc.) are absent.

**Procedure:**
1. Identify the required formula or model for the question (e.g., CAPM for SML positioning)
2. List all mandatory parameters for the formula (e.g., CAPM requires: risk-free rate, beta, market return)
3. Check the provided data systematically against the parameter list
4. If any mandatory parameter is missing and cannot be derived from given information, flag data insufficiency
5. Do NOT assume typical values, industry averages, or estimates for missing critical parameters
6. Select "insufficient data" as the answer when mandatory parameters are absent, even if partial analysis seems possible
7. Only proceed with calculation if all required parameters are explicitly provided or can be definitively derived

**Example (sanitized):**
> **Scenario:** Portfolio X has return 9%, beta 0.8. Market portfolio has return 12%, beta 1.0. Question asks whether Portfolio X lies above, below, or on the SML.
> **Wrong approach:** Assume risk-free rate of 3% (typical value), calculate expected return = 3% + 0.8(12% - 3%) = 10.2%, conclude Portfolio X is below SML since 9% < 10.2%.
> **Correct approach:** (1) SML requires: E(R) = Rf + β[E(Rm) - Rf]. (2) Given: Portfolio return = 9%, β = 0.8, Market return = 12%. (3) Missing: Rf (risk-free rate). (4) Cannot calculate expected return without Rf. (5) Answer: Insufficient data given.

---

## Pattern: Event_Timing_And_Prospective_Application

**Description:** Corporate actions (splits, dividends, mergers) and index adjustments affect calculations prospectively from the event date, not retroactively. Historical period calculations should use only the data valid during that specific period without incorporating future events.

**When to Use:** Questions involving index returns, stock splits, dividend adjustments, or any time-series calculation where corporate actions occur; trigger phrases: "period t0 to t1," "splits in the last period," "between time X and Y."

**Procedure:**
1. Identify the calculation period clearly (start date and end date)
2. Identify all corporate actions and their effective dates
3. Determine whether each corporate action occurs before, during, or after the calculation period
4. For events occurring after the period end: exclude them entirely from the calculation
5. For events occurring during the period: apply them only from the event date forward within that period
6. For price-weighted indices with splits: adjust the divisor prospectively from the split date, not retroactively
7. Calculate returns using only the prices and adjustments valid at the period start and end dates
8. Verify that no future events have been incorrectly incorporated into historical period calculations

**Example (sanitized):**
> **Scenario:** Calculate return of a price-weighted index from Jan 1 to Jun 30. Stock A: $80 (Jan 1), $90 (Jun 30). Stock B: $120 (Jan 1), $130 (Jun 30). Stock C: $60 (Jan 1), $70 (Jun 30), then splits 2-for-1 on Jul 15.
> **Wrong approach:** Adjust Stock C's Jun 30 price to $35 (70/2) to account for the split, calculate index as (90 + 130 + 35)/3 = 85, compare to initial (80 + 120 + 60)/3 = 86.67, return = -1.93%.
> **Correct approach:** (1) Calculation period: Jan 1 to Jun 30. (2) Split date: Jul 15 (after period end). (3) Use unadjusted prices: Jan 1 index = (80 + 120 + 60)/3 = 86.67; Jun 30 index = (90 + 130 + 70)/3 = 96.67. (4) Return = (96.67 - 86.67)/86.67 = 11.54%. (5) The split affects Jul 15 onward, not the Jan-Jun period.

---

## Pattern: Tax_Status_Constraint_Recognition

**Description:** Tax-exempt entities (foundations, endowments, pension funds, certain trusts) do not pay income taxes or capital gains taxes. Investment decisions for these entities should ignore tax optimization and focus solely on economic factors such as valuation, risk, and return objectives.

**When to Use:** Questions involving portfolio decisions for foundations, endowments, or any entity explicitly described as "tax-exempt"; trigger when tax rates are provided but client status indicates tax exemption.

**Procedure:**
1. Identify the client's tax status explicitly from the problem statement (look for "tax-exempt," "foundation," "endowment," "pension fund")
2. If the client is tax-exempt, immediately flag that all tax-related data (income tax rates, capital gains tax rates, tax loss harvesting) is irrelevant to the decision
3. Eliminate any answer options or reasoning based on tax efficiency, after-tax returns, or tax consequences
4. Focus decision criteria on: (a) investment views (overvalued vs. undervalued), (b) risk-return characteristics, (c) liquidity needs, (d) strategic fit
5. For liquidation decisions: sell overvalued assets first, retain undervalued assets, regardless of embedded gains or losses
6. Verify that the final recommendation is based purely on economic factors, not tax considerations
7. Double-check that tax-exempt status hasn't been overlooked when tax data is prominently displayed in exhibits

**Example (sanitized):**
> **Scenario:** A university endowment (tax-exempt) needs $10 million cash. Two bonds available: Bond A (market value $10M, $500K capital gain, viewed as overvalued), Bond B (market value $10M, $500K capital loss, viewed as undervalued). Capital gains tax rate is 25%.
> **Wrong approach:** Calculate after-tax proceeds: Bond A yields $10M - ($500K × 25%) = $9.875M; Bond B yields $10M + ($500K × 25% tax benefit) = $10.125M. Recommend selling Bond B for higher after-tax proceeds.
> **Correct approach:** (1) Client is tax-exempt endowment. (2) Tax rates are irrelevant; both bonds provide exactly $10M in proceeds. (3) Decision based on investment view: Bond A is overvalued (should sell), Bond B is undervalued (should retain). (4) Recommend selling Bond A to meet cash needs while preserving undervalued assets.