# Corporate Finance — Conceptual vs. Computational Interpretation

## Pattern: conceptual_question_recognition

**Description:** Questions asking "what is the difference" or "what distinguishes" may require conceptual answers (identifying methodological differences, definitions, or characteristics) rather than numerical calculations, even when the topic involves quantitative metrics like WACC, NPV, or IRR.

**When to Use:** 
- Questions contain phrases like "what is the difference between," "what distinguishes," "how do X and Y differ," "what makes X different from Y"
- The question references multiple versions or approaches to the same concept (e.g., "different WACCs," "various NPV methods")
- Context suggests comparison of methodologies, assumptions, or definitions rather than numerical outcomes

**Procedure:**
1. **Identify the question type**: Determine if the question asks "what" (conceptual) vs. "calculate" or "how much" (computational)
2. **Check for methodology indicators**: Look for references to different approaches, methods, or calculation bases (e.g., "book value vs. market value," "nominal vs. real," "target weights")
3. **Assess answer expectations**: If the question asks about differences without requesting a specific numerical result, the answer likely describes the conceptual distinction
4. **Provide the distinguishing feature**: State what methodologically or conceptually separates the approaches, not the numerical outcome of using them
5. **Avoid unnecessary calculations**: Don't compute values unless explicitly asked for a numerical difference

**Example (sanitized):**
> **Scenario:** A question asks "What is the difference between the two cost of equity calculations presented?" where one uses the dividend growth model and another uses CAPM.
> **Wrong approach:** Calculate cost of equity using both methods and report the percentage point difference (e.g., "The difference is 2.3 percentage points").
> **Correct approach:** Identify the methodological distinction: "The difference is the valuation model used—one employs the dividend growth model while the other uses the Capital Asset Pricing Model."

---

## Pattern: perpetuity_with_growth_components

**Description:** NPV calculations for perpetuities with multiple cash flow components, each growing at different rates, require separate valuation of each component using the growing perpetuity formula, with careful attention to real vs. nominal rate conversions.

**When to Use:**
- Project has indefinite life (perpetuity) with ongoing cash flows
- Multiple distinct cash flow categories (e.g., revenues, costs, maintenance) grow at different rates
- Problem provides both real and nominal rates, or real growth rates with inflation
- Question asks for NPV or present value of the perpetual project

**Procedure:**
1. **Convert rates to consistent basis**: If given real rates and inflation, convert to nominal using Fisher equation: (1 + nominal) = (1 + real)(1 + inflation)
2. **Identify all cash flow components**: List each distinct cash flow stream (revenues, variable costs, fixed costs, etc.)
3. **Determine growth rate for each component**: Note which components grow and at what real rate
4. **Calculate nominal growth rates**: For each growing component, convert real growth to nominal: (1 + g_nominal) = (1 + g_real)(1 + inflation)
5. **Apply growing perpetuity formula to each component**: PV = CF₁/(r - g) where CF₁ is the first period cash flow, r is nominal discount rate, g is nominal growth rate
6. **Handle non-growing components**: For fixed perpetual costs, use PV = CF/r (perpetuity without growth)
7. **Sum all present values**: Combine PVs of all components, respecting signs (revenues positive, costs negative)
8. **Subtract initial investment**: NPV = Sum of PVs - Initial outlay

**Example (sanitized):**
> **Scenario:** A manufacturing facility requires $800,000 initial investment and will operate indefinitely. Annual revenue is $400,000 (growing at 2% real), variable costs are $150,000 (growing at 3% real), and fixed costs are $80,000 (no growth). Real discount rate is 8%, inflation is 4%.
> 
> **Wrong approach:** Calculate nominal rate as 8% + 4% = 12%, then use single perpetuity formula with blended growth rate.
> 
> **Correct approach:**
> 1. Nominal discount rate: (1.08)(1.04) = 1.1232, so r = 12.32%
> 2. Revenue nominal growth: (1.02)(1.04) = 1.0608, so g_rev = 6.08%
> 3. Variable cost nominal growth: (1.03)(1.04) = 1.0712, so g_vc = 7.12%
> 4. PV of revenues: 400,000/(0.1232 - 0.0608) = $6,410,256
> 5. PV of variable costs: -150,000/(0.1232 - 0.0712) = -$2,884,615
> 6. PV of fixed costs: -80,000/0.1232 = -$649,351
> 7. Sum of PVs: 6,410,256 - 2,884,615 - 649,351 = $2,876,290
> 8. NPV: 2,876,290 - 800,000 = $2,076,290

---

## Pattern: wacc_weighting_scheme_identification

**Description:** WACC calculations can use different weighting schemes (book value weights, market value weights, or target capital structure weights), and questions may ask about the conceptual basis for these differences rather than numerical WACC values.

**When to Use:**
- Question mentions "different WACCs" or "alternative WACC calculations"
- Context provides multiple sets of weights or valuation bases
- Question asks "what is the difference" or "what distinguishes" rather than "calculate WACC"
- Problem presents book values, market values, and/or target percentages for debt and equity

**Procedure:**
1. **Identify weighting schemes present**: Determine which of the three main schemes are referenced (book value, market value, target)
2. **Recognize the conceptual question**: If asked about "difference," focus on the weighting methodology, not numerical results
3. **State the distinguishing feature**: 
   - Book value weights: Based on accounting/historical values from balance sheet
   - Market value weights: Based on current market prices of debt and equity
   - Target weights: Based on desired/optimal capital structure the firm aims to maintain
4. **Avoid calculation unless requested**: Don't compute WACC values unless the question explicitly asks for numerical comparison

**Example (sanitized):**
> **Scenario:** A firm's balance sheet shows debt of $5M and equity of $10M. Market values are debt $4.8M and equity $18M. The firm's target structure is 30% debt, 70% equity. Question asks: "What differentiates these three WACC calculations?"
> 
> **Wrong approach:** Calculate three WACC values (e.g., 9.2%, 8.7%, 8.9%) and state "The WACCs differ by up to 0.5 percentage points."
> 
> **Correct approach:** "The difference is the weighting scheme used: book value weights use balance sheet values, market value weights use current market prices, and target weights use the firm's desired capital structure proportions."

---

## Pattern: real_vs_nominal_rate_consistency

**Description:** Financial calculations must maintain consistency between real and nominal terms—real cash flows must be discounted at real rates, and nominal cash flows at nominal rates. The Fisher equation links these: (1 + nominal rate) = (1 + real rate)(1 + inflation rate).

**When to Use:**
- Problem provides both real and nominal rates, or real rates with inflation
- Cash flows are described as "real" or adjusted for inflation
- Growth rates are specified as "real growth"
- NPV, IRR, or present value calculations involve multi-period cash flows with inflation

**Procedure:**
1. **Identify what's given**: Determine if rates and cash flows are in real or nominal terms
2. **Choose a consistent framework**: Decide whether to work entirely in real terms or nominal terms
3. **Convert rates if needed**: 
   - To get nominal from real: (1 + r_nominal) = (1 + r_real)(1 + inflation)
   - To get real from nominal: (1 + r_real) = (1 + r_nominal)/(1 + inflation)
4. **Convert growth rates similarly**: Real growth to nominal growth uses same Fisher equation
5. **Adjust cash flows if necessary**: If working in nominal terms with real cash flows, inflate each period's cash flow
6. **Apply discount rate**: Use nominal rate for nominal cash flows, real rate for real cash flows
7. **Verify consistency**: Double-check that all inputs are in the same terms before final calculation

**Example (sanitized):**
> **Scenario:** A project generates $100,000 real cash flow in year 1, growing at 3% real rate. Real discount rate is 7%, inflation is 5%. Calculate NPV over 5 years with $350,000 initial investment.
> 
> **Wrong approach:** Discount real cash flows at nominal rate: (1.07)(1.05) = 12.35%, then NPV = -350,000 + Σ[100,000(1.03)^t / (1.1235)^t]
> 
> **Correct approach (Option 1 - Stay in real terms):**
> Discount real cash flows at real rate: NPV = -350,000 + Σ[100,000(1.03)^t / (1.07)^t] for t=1 to 5
> 
> **Correct approach (Option 2 - Convert to nominal):**
> Convert to nominal: r_nom = 12.35%, g_nom = (1.03)(1.05) - 1 = 8.15%
> Nominal CF₁ = 100,000(1.05) = 105,000
> NPV = -350,000 + Σ[105,000(1.0815)^(t-1) / (1.1235)^t] for t=1 to 5

---

## Pattern: multi_component_cash_flow_aggregation

**Description:** When projects have multiple distinct cash flow components (revenues, various cost categories, taxes, capital expenditures), each must be calculated separately with its own growth rate and timing before aggregating to find total project value.

**When to Use:**
- Project description lists multiple cash flow categories
- Different components have different growth rates, timing, or characteristics
- Question asks for total NPV, project value, or overall cash flow
- Components may include: revenues, fixed costs, variable costs, depreciation tax shields, salvage values, working capital changes

**Procedure:**
1. **List all components**: Create inventory of every cash flow type mentioned
2. **Determine characteristics for each**:
   - Initial value or first-period amount
   - Growth rate (if any)
   - Timing (when it occurs)
   - Whether it's an inflow or outflow
3. **Calculate present value separately**: For each component, compute PV using appropriate formula:
   - Growing perpetuity: PV = CF₁/(r - g)
   - Perpetuity: PV = CF/r
   - Finite annuity: PV = CF × [(1 - (1+r)^-n)/r]
   - Growing annuity: PV = CF₁ × [(1 - ((1+g)/(1+r))^n)/(r - g)]
   - Single cash flow: PV = CF/(1+r)^t
4. **Track signs carefully**: Inflows are positive, outflows are negative
5. **Sum all present values**: Add algebraically, respecting signs
6. **Subtract initial investment**: If calculating NPV, deduct upfront costs
7. **Verify completeness**: Ensure no cash flow component was omitted

**Example (sanitized):**
> **Scenario:** A retail expansion requires $500,000 initial investment. It generates: (1) Sales of $300,000/year growing at 4%, (2) Cost of goods sold at 60% of sales, (3) Fixed operating costs of $50,000/year (no growth), (4) Marketing costs of $20,000/year growing at 2%. Project lasts 10 years, discount rate 10%.
> 
> **Wrong approach:** Calculate net cash flow as 300,000 - 180,000 - 50,000 - 20,000 = 50,000, then treat as simple annuity growing at blended rate.
> 
> **Correct approach:**
> 1. PV of sales: 300,000 × [(1 - (1.04/1.10)^10)/(0.10 - 0.04)] = $2,052,441
> 2. PV of COGS: -180,000 × [(1 - (1.04/1.10)^10)/(0.10 - 0.04)] = -$1,231,465
> 3. PV of fixed costs: -50,000 × [(1 - 1.10^-10)/0.10] = -$307,228
> 4. PV of marketing: -20,000 × [(1 - (1.02/1.10)^10)/(0.10 - 0.02)] = -$143,318
> 5. Sum: 2,052,441 - 1,231,465 - 307,228 - 143,318 = $370,430
> 6. NPV: 370,430 - 500,000 = -$129,570

---

SKILL_MD_ENTRY: | `corporate_finance/new_patterns.md` | Corporate Finance | Conceptual vs. Computational Interpretation | Conceptual question recognition, Perpetuity with growth components, WACC weighting scheme identification, Real vs. nominal rate consistency, Multi-component cash flow aggregation |