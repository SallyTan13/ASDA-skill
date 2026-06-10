# Corporate Finance — NPV Calculation and Capital Budgeting

## Pattern: npv_cash_flow_identification

**Description:** Failure to correctly identify, sign, and discount cash flows in NPV problems, including distinguishing between inflows and outflows, recognizing initial receipts vs. future obligations, and properly structuring the NPV calculation.

**When to Use:** Questions asking "should you accept this offer?", "what is the NPV?", or presenting scenarios with mixed cash flows (receiving money now but making payments later, or vice versa).

**Procedure:**
1. **Identify all cash flows and their timing:**
   - List every monetary amount mentioned
   - Assign each to a specific time period (Year 0, Year 1, etc.)
   - Note what each represents (receipt, payment, revenue, cost)

2. **Determine correct signs:**
   - Cash INFLOWS (receipts, revenues, salvage values) = POSITIVE
   - Cash OUTFLOWS (payments, costs, investments) = NEGATIVE
   - Initial investment or payment made = NEGATIVE at Year 0
   - Initial receipt or loan received = POSITIVE at Year 0

3. **Structure the NPV formula:**
   - NPV = CF₀ + CF₁/(1+r) + CF₂/(1+r)² + ... + CFₙ/(1+r)ⁿ
   - Where CF₀ is the net cash flow at Year 0 (can be positive or negative)
   - Apply the discount rate to all future cash flows only

4. **Calculate and interpret:**
   - Sum all discounted cash flows
   - If NPV > 0, accept the project/offer
   - If NPV < 0, reject the project/offer

**Example (sanitized):**
> **Scenario:** A vendor offers you $5,000 today if you agree to pay $2,000 in one year and $3,500 in two years. The discount rate is 8%.
> **Wrong approach:** Treating the $5,000 as an outflow or ignoring it; treating future payments as positive values; discounting the Year 0 amount.
> **Correct approach:** NPV = +$5,000 - $2,000/1.08 - $3,500/1.08² = +$5,000 - $1,852 - $3,001 = +$147. Since NPV > 0, accept the offer.

---

## Pattern: after_tax_cash_flow_with_depreciation

**Description:** Failure to properly calculate after-tax operating cash flows and depreciation tax shields in capital budgeting, including separating operating cash flows from tax effects and recognizing that depreciation is a non-cash expense that creates tax savings.

**When to Use:** Capital budgeting questions involving tax rates, depreciation schedules, operating revenues/costs, and project evaluation decisions.

**Procedure:**
1. **Calculate annual operating cash flow (OCF):**
   - OCF = (Revenue - Operating Costs) × (1 - Tax Rate) + Depreciation × Tax Rate
   - Alternative: OCF = (Revenue - Operating Costs - Depreciation) × (1 - Tax Rate) + Depreciation
   - Both formulas yield the same result

2. **Identify all depreciable assets:**
   - Initial equipment/building costs
   - Modifications or improvements
   - Each may have different depreciation schedules

3. **Calculate annual depreciation:**
   - Straight-line: Cost / Useful Life
   - Apply to each depreciable asset separately
   - Sum total annual depreciation

4. **Handle terminal cash flows:**
   - Salvage value (if any) = cash inflow
   - Book value at disposal = Original Cost - Accumulated Depreciation
   - Tax on gain/loss = (Salvage Value - Book Value) × Tax Rate
   - Terminal restoration costs = outflow, but create tax shield
   - Net terminal CF = Salvage Value - Tax on Gain + Tax Shield on Costs

5. **Calculate NPV:**
   - Year 0: Initial investment (negative)
   - Years 1-n: After-tax operating cash flows
   - Year n: Add terminal cash flows
   - Discount all at the required rate of return

**Example (sanitized):**
> **Scenario:** A machine costs $100,000, generates $40,000 annual revenue and $15,000 annual costs for 5 years. Straight-line depreciation to zero. Tax rate 30%. Discount rate 10%.
> **Wrong approach:** Ignoring depreciation tax shield; treating depreciation as a cash outflow; not adjusting terminal values for taxes.
> **Correct approach:** Annual depreciation = $100,000/5 = $20,000. OCF = ($40,000 - $15,000) × 0.7 + $20,000 × 0.3 = $17,500 + $6,000 = $23,500. NPV = -$100,000 + $23,500 × PVIFA(10%, 5 years) = -$100,000 + $89,079 = -$10,921. Reject.

---

## Pattern: real_vs_nominal_rate_conversion

**Description:** Confusion between real and nominal discount rates, and failure to properly adjust cash flows for inflation when calculating NPV, especially in perpetuity problems with growth rates.

**When to Use:** Questions mentioning both inflation rates and real growth rates, or asking for NPV with "real" or "nominal" rates specified, particularly in perpetual cash flow scenarios.

**Procedure:**
1. **Understand the Fisher equation:**
   - (1 + Nominal Rate) = (1 + Real Rate) × (1 + Inflation Rate)
   - Nominal Rate ≈ Real Rate + Inflation Rate (approximation)
   - Use exact formula for precision

2. **Identify what's given:**
   - Are cash flows in real or nominal terms?
   - Is the discount rate real or nominal?
   - Are growth rates real or nominal?

3. **Apply consistency principle:**
   - Real cash flows must be discounted at real rates
   - Nominal cash flows must be discounted at nominal rates
   - NEVER mix real and nominal

4. **For growing perpetuities:**
   - If cash flows grow at real rate g_real and inflation is i:
   - Nominal growth rate = (1 + g_real) × (1 + i) - 1
   - PV = CF₁ / (r_nominal - g_nominal)
   - Where CF₁ is the Year 1 cash flow in nominal terms

5. **For multiple components with different growth rates:**
   - Calculate PV of each component separately
   - Each component: PV = CF₁ / (r - g) where r and g are both real or both nominal
   - Sum all component PVs

**Example (sanitized):**
> **Scenario:** A project generates Year 1 revenue of $100,000 (nominal) growing at 2% real rate. Costs are $60,000 (nominal) growing at 1% real rate. Inflation is 3%. Nominal discount rate is 12%.
> **Wrong approach:** Using real growth rates with nominal discount rate directly; inflating Year 0 values when Year 1 values are already given.
> **Correct approach:** Nominal growth for revenue = (1.02)(1.03) - 1 = 5.06%. Nominal growth for costs = (1.01)(1.03) - 1 = 4.03%. PV of revenues = $100,000/(0.12 - 0.0506) = $1,441,441. PV of costs = $60,000/(0.12 - 0.0403) = $753,769. NPV = $1,441,441 - $753,769 = $687,672.

---

## Pattern: project_comparison_with_alternatives

**Description:** Failure to properly compare mutually exclusive projects or alternatives by calculating complete NPVs for each option, including the "do nothing" or alternative use scenarios, and misunderstanding when incremental IRR analysis is necessary versus when direct NPV comparison suffices.

**When to Use:** Questions asking "which project should you choose?", "which use would you recommend?", "which alternative is best?", or presenting multiple investment alternatives including rental, sale, or alternative use options. Also applies to questions asking whether incremental IRR analysis is necessary for mutually exclusive projects.

**When NOT to Use:** 
- Questions about acquisition decisions where the comparison is between "acquire" vs. "don't acquire" rather than between multiple mutually exclusive uses of an asset
- Questions where the decision involves evaluating a single target company's value under different growth scenarios (these require valuation analysis, not project comparison)
- Situations where the question asks about different valuation approaches or growth assumptions for the same project rather than comparing distinct alternatives

**Procedure:**
1. **Identify all alternatives:**
   - List every option explicitly mentioned
   - Include implicit alternatives (rent vs. own, sell vs. use, lease vs. operate, etc.)
   - Recognize that "do nothing" or "alternative use" may be an option
   - **CRITICAL:** Do not skip any alternative, especially rental or passive income options

2. **Calculate complete NPV for each alternative:**
   - Use the same discount rate for all alternatives
   - Include all relevant cash flows for each option (revenues, costs, tax effects, terminal values)
   - Ensure time horizons are comparable (adjust if needed)
   - Apply after-tax cash flow calculations where applicable
   - **VERIFICATION STEP:** Double-check all arithmetic, especially when calculating total market values or aggregate figures (multiply per-share values by number of shares, or use total earnings/dividends for company-level analysis)

3. **For rental or alternative use options:**
   - Calculate PV of rental income stream (use annuity formula if constant, or sum if varying)
   - Subtract any costs associated with that alternative
   - This becomes the opportunity cost of other uses
   - **Do not ignore this step even if rental seems less attractive initially**

4. **Determine if incremental IRR analysis is necessary:**
   - Compare NPV rankings with IRR rankings (if IRRs are given or calculated)
   - **Incremental IRR is necessary ONLY if:** NPV and IRR rankings conflict for mutually exclusive projects
   - **Incremental IRR is NOT necessary if:** NPV rankings agree with IRR rankings, or if NPV clearly identifies the best project
   - Different scales or investment sizes alone do NOT require incremental IRR if NPV rankings are clear

5. **Make the decision:**
   - Select the alternative with the highest NPV (this is always the correct decision rule)
   - If all NPVs are negative, choose the least negative (or reject all if possible)
   - IRR is only a supplementary metric; NPV is the primary decision criterion
   - Consider qualitative factors only after quantitative analysis

6. **Common pitfalls to avoid:**
   - Don't compare IRRs when projects have different scales or timing without checking NPV first
   - Don't ignore the opportunity cost of alternative uses (especially rental income)
   - Don't forget to include all terminal values and restoration costs
   - Don't assume incremental IRR is needed just because projects differ in size
   - **Don't confuse per-share or per-unit values with total company or project values**
   - **Always verify that your calculated values make economic sense in magnitude**

**Common Mistakes to Avoid:**
- Failing to evaluate all alternatives mentioned in the problem, particularly rental or passive income options
- Assuming incremental IRR analysis is required whenever projects have different scales, without first checking if NPV and IRR rankings conflict
- Selecting projects based on IRR alone when NPV provides a clear ranking
- **Making arithmetic errors when scaling from per-share to total values or vice versa**
- **Applying project comparison methodology to acquisition valuation problems that require different analytical frameworks**

**Example (sanitized):**
> **Scenario:** A warehouse can be used for Manufacturing Project M (initial investment $800,000, annual after-tax cash flows $120,000 for 12 years, IRR 12%), Manufacturing Project N (initial investment $500,000, annual after-tax cash flows $85,000 for 12 years, IRR 14%), or rented to a third party for $75,000/year for 12 years. Discount rate is 10%.
> **Wrong approach:** Choosing Project N because it has higher IRR; ignoring the rental option entirely; assuming incremental IRR analysis is necessary because projects have different initial investments.
> **Correct approach:** 
> - NPV of Project M = -$800,000 + $120,000 × PVIFA(10%, 12) = -$800,000 + $817,692 = $17,692
> - NPV of Project N = -$500,000 + $85,000 × PVIFA(10%, 12) = -$500,000 + $579,254 = $79,254
> - NPV of Rental = $75,000 × PVIFA(10%, 12) = $75,000 × 6.8137 = $511,028
> - Compare all three: Rental ($511,028) > Project N ($79,254) > Project M ($17,692)
> - **Decision:** Recommend rental option
> - **Incremental IRR analysis:** NOT necessary because NPV clearly ranks all alternatives, and both NPV and IRR agree that Project N dominates Project M among the manufacturing options

---
## Pattern: wacc_methodology_distinction

**Description:** Confusing questions about WACC calculation methodology (which weighting scheme to use) with questions asking for numerical WACC computation, and failing to recognize when the question seeks conceptual understanding rather than calculation.

**When to Use:** Questions asking "what is the difference between WACCs?", "which weights should be used?", or presenting multiple sets of values (book, market, target) without explicitly asking for calculation.

**Procedure:**
1. **Identify the question type:**
   - Is it asking for a numerical WACC value? → Calculate
   - Is it asking about differences, approaches, or which method? → Conceptual answer
   - Keywords: "difference between", "which approach", "what distinguishes"

2. **Recognize the three WACC weighting schemes:**
   - **Book value weights:** Based on accounting values from balance sheet
   - **Market value weights:** Based on current market prices of debt and equity
   - **Target weights:** Based on management's desired capital structure

3. **Understand when each is appropriate:**
   - Market value weights: Most theoretically correct, reflects current opportunity costs
   - Target weights: Used when company is moving toward a desired structure
   - Book value weights: Easier to calculate but less accurate

4. **For conceptual questions:**
   - Answer focuses on the methodology, not numbers
   - Explain which weighting scheme differs or why
   - Don't perform calculations unless explicitly requested

5. **For calculation questions:**
   - Determine which weights to use based on context
   - Calculate WACC = (E/V) × r_e + (D/V) × r_d × (1 - T_c)
   - Where E/V and D/V are the chosen weights

**Example (sanitized):**
> **Scenario:** A company has book value debt of $500M, market value debt of $480M, book value equity of $300M, and market value equity of $720M. Management targets 40% debt. Question asks: "What is the difference between the WACCs?"
> **Wrong approach:** Calculating WACC with book weights (62.5% debt) and market weights (40% debt) and subtracting the results.
> **Correct approach:** The difference refers to the three weighting methodologies: book value weights (62.5% debt, 37.5% equity), market value weights (40% debt, 60% equity), and target weights (40% debt, 60% equity). The answer is "the different weighting schemes" or "the choice between book, market, and target capital structure weights."

---

## Pattern: perpetuity_with_multiple_growth_rates

**Description:** Incorrectly applying perpetuity formulas when different cash flow components grow at different rates, or failing to properly separate and value each component independently.

**When to Use:** NPV problems involving perpetual cash flows where revenues, costs, or other components have different growth rates specified.

**Procedure:**
1. **Decompose cash flows into components:**
   - Identify each component (revenues, operating costs, maintenance, etc.)
   - Note the growth rate for each component
   - Ensure you're using Year 1 values (not Year 0)

2. **Calculate PV of each growing perpetuity:**
   - For each component: PV = CF₁ / (r - g)
   - Where CF₁ is the Year 1 cash flow
   - r is the discount rate
   - g is the growth rate for that component
   - Ensure r and g are both real or both nominal

3. **Apply correct signs:**
   - Revenues and inflows: positive PV
   - Costs and outflows: negative PV
   - Net PV = Sum of all component PVs

4. **Handle initial investment:**
   - Subtract Year 0 investment from the sum of perpetuity PVs
   - NPV = -Initial Investment + PV(Revenues) - PV(Costs) - PV(Other Outflows)

5. **Common errors to avoid:**
   - Don't inflate Year 1 values by growth rates (they're already Year 1)
   - Don't use a single growth rate for all components
   - Don't forget that costs reduce NPV (negative contribution)

**Example (sanitized):**
> **Scenario:** Initial investment $500,000. Year 1 revenues $200,000 growing at 3%. Year 1 costs $80,000 growing at 4%. Discount rate 10%.
> **Wrong approach:** Net cash flow = $200,000 - $80,000 = $120,000. PV = $120,000/(0.10 - 0.03) = $1,714,286. NPV = -$500,000 + $1,714,286 = $1,214,286. (Wrong because uses single growth rate)
> **Correct approach:** PV(revenues) = $200,000/(0.10 - 0.03) = $2,857,143. PV(costs) = $80,000/(0.10 - 0.04) = $1,333,333. NPV = -$500,000 + $2,857,143 - $1,333,333 = $1,023,810.

---

SKILL_MD_ENTRY: | `corporate_finance/npv_and_capital_budgeting.md` | Corporate Finance | NPV Calculation and Capital Budgeting | npv_cash_flow_identification, after_tax_cash_flow_with_depreciation, real_vs_nominal_rate_conversion, project_comparison_with_alternatives, wacc_methodology_distinction, perpetuity_with_multiple_growth_rates |

## Pattern: acquisition_valuation_with_synergies

**Description:** Failure to properly value acquisition targets by comparing the target's standalone value with its value including synergies, and incorrectly applying project comparison frameworks to acquisition decisions that require valuation-based analysis.

**When to Use:** Questions about whether to acquire another company, especially when synergies (growth rate improvements, cost savings, economies of scale) are mentioned, or when comparing different acquisition scenarios with varying assumptions about post-acquisition performance.

**Procedure:**
1. **Calculate the target's standalone value:**
   - Use current market metrics (P/E ratio, market price per share, shares outstanding)
   - Total market value = Share price × Shares outstanding
   - Or: Total market value = (Earnings / Shares outstanding) × P/E ratio × Shares outstanding = Earnings × P/E ratio
   - Apply dividend discount model if perpetual growth is mentioned: Value = D₁ / (r - g)
   - Where D₁ is next year's expected dividend, r is required return, g is growth rate

2. **Estimate the required return (cost of equity):**
   - If not given, derive from current market conditions
   - Using dividend growth model: r = (D₁/P₀) + g
   - Where P₀ is current price, D₁ is expected dividend, g is growth rate
   - Ensure you use per-share values consistently or total values consistently

3. **Calculate value with synergies:**
   - Apply the enhanced growth rate or cost savings from synergies
   - Value with synergies = D₁ / (r - g_enhanced)
   - Compare this to the standalone value
   - The difference represents the value creation from synergies

4. **Determine acquisition attractiveness:**
   - If value with synergies > current market value: acquisition creates value
   - Consider the acquisition premium that would need to be paid
   - Maximum price to pay = Value with synergies (to break even on the acquisition)
   - For value creation, pay less than the synergy-enhanced value

5. **Compare different acquisition scenarios (if applicable):**
   - Calculate value under each scenario's assumptions
   - The scenario with highest value creation is preferred
   - Ensure all scenarios use consistent methodology and discount rates

**Common Mistakes to Avoid:**
- Confusing per-share values with total company values (e.g., treating total earnings as price per share)
- Applying project NPV comparison methodology to acquisition valuation problems
- Forgetting to account for the acquisition premium in the analysis
- Using inconsistent growth rates or discount rates across scenarios
- Miscalculating the cost of equity or required return

**Example (sanitized):**
> **Scenario:** Target Corp has 500,000 shares outstanding, earnings of $1,000,000, dividends of $400,000, and a P/E ratio of 12. Current growth rate is 3%, but the acquirer believes synergies will increase growth to 5%. Should the acquisition proceed?
> **Wrong approach:** Calculating standalone value as $1,000,000 × 12 = $12 million, then comparing growth rates without proper valuation.
> **Correct approach:** 
> - Current market value = Earnings × P/E = $1,000,000 × 12 = $12,000,000
> - EPS = $1,000,000 / 500,000 = $2.00
> - DPS = $400,000 / 500,000 = $0.80
> - Current price per share = EPS × P/E = $2.00 × 12 = $24
> - Cost of equity: r = (D₁/P₀) + g = ($0.80 × 1.03 / $24) + 0.03 = 0.0343 + 0.03 = 6.43%
> - Value with 5% growth = ($400,000 × 1.05) / (0.0643 - 0.05) = $420,000 / 0.0143 = $29,370,629
> - Value creation = $29,370,629 - $12,000,000 = $17,370,629
> - **Decision:** Yes, pursue acquisition as synergies create substantial value, but ensure acquisition price is below $29.4 million to capture some of this value creation.