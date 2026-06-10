# Fixed Income — Tax-Exempt Liquidation Strategy

## Pattern: tax_exempt_liquidation_decision

**Description:** When tax-exempt entities (foundations, endowments, pension funds) need to liquidate bond positions to meet cash needs, tax considerations are irrelevant. The optimal liquidation strategy should prioritize selling overvalued securities while retaining undervalued ones to align with investment thesis and maximize long-term portfolio value.

**When to Use:** 
- Question involves tax-exempt entities (foundations, endowments, qualified pension plans)
- Multiple bond positions available for sale
- Need to select which bond(s) to liquidate
- Investment views provided (overvalued, undervalued, fairly valued)
- Keywords: "tax-exempt," "foundation," "endowment," "optimal strategy," "cash needs," "liquidation"

**Procedure:**

1. **Verify Tax-Exempt Status**
   - Identify entity type: foundation, endowment, qualified pension plan, charitable trust
   - Confirm tax-exempt status eliminates capital gains tax considerations
   - Disregard any tax calculations or after-tax return comparisons

2. **Calculate Gross Liquidation Proceeds**
   - For each bond: Proceeds = Market Price × Par Value / 100
   - Do NOT adjust for taxes (entity is tax-exempt)
   - Verify which bonds provide sufficient proceeds to meet cash requirement

3. **Apply Investment View Hierarchy**
   - **First Priority:** Sell overvalued securities (trim positions trading above fair value)
   - **Second Priority:** Sell fairly valued securities (neutral impact)
   - **Last Priority:** Retain undervalued securities (preserve positions with upside potential)
   - Rationale: Liquidation is an opportunity to rebalance toward better valuations

4. **Consider Secondary Factors (if investment views are equal)**
   - Liquidity: Prefer selling more liquid bonds
   - Duration management: Align with portfolio duration targets
   - Credit quality: Consider risk management objectives
   - Sector/issuer diversification: Maintain desired exposures

5. **Validate the Decision**
   - Confirm selected bond(s) generate required cash
   - Verify decision aligns with stated investment thesis
   - Check that tax considerations were NOT applied

**Example (sanitized):**

> **Scenario:** A university endowment (tax-exempt) needs to raise $5 million to fund scholarships. The portfolio manager has three corporate bonds available for sale:
> - Bond X: Par $5M, Market Price 102, Manager's view: Overvalued by 3%
> - Bond Y: Par $5M, Market Price 101, Manager's view: Fairly valued
> - Bond Z: Par $5M, Market Price 103, Manager's view: Undervalued by 2%
>
> All three bonds would generate sufficient proceeds (>$5M). Which should be sold?

> **Wrong approach:** 
> "Bond X has the lowest market price at 102, so selling it minimizes the capital gain. We should sell Bond X to minimize tax impact."
> 
> **Error:** Tax-exempt entities don't pay capital gains taxes. This reasoning is irrelevant.

> **Wrong approach 2:**
> "Bond Z has the highest market price at 103, generating $5.15M in proceeds. Sell Bond Z to maximize cash received."
> 
> **Error:** All three bonds meet the cash requirement. The decision should be based on investment merit, not marginal cash differences.

> **Correct approach:** 
> 1. Recognize the endowment is tax-exempt → taxes are irrelevant
> 2. Calculate proceeds: Bond X = $5.1M, Bond Y = $5.05M, Bond Z = $5.15M (all sufficient)
> 3. Apply investment view hierarchy:
>    - Bond X: Overvalued → SELL (trim overpriced position)
>    - Bond Y: Fairly valued → Neutral
>    - Bond Z: Undervalued → RETAIN (preserve position with upside)
> 4. **Answer: Sell Bond X** — liquidation provides opportunity to exit overvalued position while meeting cash needs

---

## Pattern: tax_exempt_vs_taxable_decision_framework

**Description:** Distinguish between decision frameworks for taxable versus tax-exempt investors when evaluating bond strategies. Tax-exempt entities ignore after-tax calculations and focus purely on pre-tax economics and investment views.

**When to Use:**
- Question specifies investor tax status
- Comparison between different investor types
- Need to determine relevant decision criteria
- Keywords: "foundation," "taxable investor," "after-tax," "tax-exempt"

**Procedure:**

1. **Identify Investor Tax Status**
   - Tax-exempt: Foundations, endowments, qualified pension plans, charitable organizations
   - Taxable: Individuals, corporations, taxable trusts, hedge funds

2. **Select Appropriate Decision Framework**
   
   **For Tax-Exempt Entities:**
   - Use pre-tax yields and returns
   - Ignore capital gains/losses tax implications
   - Focus on: investment views, liquidity, duration, credit quality
   - Liquidation decisions based on valuation and portfolio strategy
   
   **For Taxable Entities:**
   - Use after-tax yields and returns
   - Consider capital gains tax on appreciated positions
   - Tax-loss harvesting opportunities
   - Holding period implications (short-term vs long-term gains)
   - Tax-equivalent yield comparisons

3. **Apply Consistent Framework**
   - Do not mix tax and non-tax considerations inappropriately
   - If entity is tax-exempt, completely eliminate tax calculations
   - If entity is taxable, incorporate all relevant tax effects

**Example (sanitized):**

> **Scenario:** Two portfolio managers discuss selling a bond trading at 105 (par 100, cost basis 98):
> - Manager A works for a private foundation (tax-exempt)
> - Manager B works for a high-net-worth individual (40% capital gains tax rate)
>
> Both believe the bond is overvalued. Should they both sell?

> **Wrong approach:**
> "Both managers face the same decision. The bond is overvalued, so both should sell immediately."
>
> **Error:** Ignores the tax consequence for Manager B's client, who would realize a $7 gain per $100 par and pay $2.80 in taxes.

> **Correct approach:**
> 
> **Manager A (Foundation - Tax-Exempt):**
> - Proceeds from sale: $105 per $100 par
> - Tax impact: $0 (tax-exempt)
> - Net proceeds: $105
> - Decision: Sell if overvalued (no tax friction)
> 
> **Manager B (Taxable Individual):**
> - Proceeds from sale: $105 per $100 par
> - Capital gain: $105 - $98 = $7
> - Tax: $7 × 40% = $2.80
> - Net proceeds: $105 - $2.80 = $102.20
> - Decision: Must weigh degree of overvaluation against tax cost
>   - If bond is only slightly overvalued, tax cost may exceed benefit
>   - If bond is significantly overvalued, sell despite tax
> 
> **Conclusion:** Manager A has a clearer sell decision due to absence of tax friction. Manager B must perform cost-benefit analysis including tax impact.

---

## Pattern: liquidation_with_equal_proceeds

**Description:** When multiple bonds generate equal (or sufficient) proceeds to meet cash needs for a tax-exempt entity, the tiebreaker should be investment merit—sell the least attractive holdings first.

**When to Use:**
- Multiple liquidation candidates available
- All candidates meet cash requirement
- Tax-exempt investor (proceeds are equal on pre-tax and after-tax basis)
- Investment views differ across candidates

**Procedure:**

1. **Confirm Sufficiency of Proceeds**
   - Calculate liquidation value for each candidate
   - Verify each option meets or exceeds cash requirement
   - Recognize that "which generates more cash" is not the deciding factor if all are sufficient

2. **Rank by Investment Attractiveness**
   - Most attractive: Undervalued securities (highest expected return)
   - Neutral: Fairly valued securities
   - Least attractive: Overvalued securities (lowest expected return)

3. **Apply Liquidation Priority**
   - **Sell first:** Overvalued positions (exit poor valuations)
   - **Sell second:** Fairly valued positions (neutral impact)
   - **Sell last:** Undervalued positions (preserve best opportunities)

4. **Optimize Portfolio Through Liquidation**
   - View forced liquidation as portfolio rebalancing opportunity
   - Improve overall portfolio quality by trimming weakest positions
   - Retain positions with best risk-adjusted return prospects

**Example (sanitized):**

> **Scenario:** A pension fund (tax-exempt) must raise exactly $10 million. Three bonds are available:
> - Bond A: Can generate $10.2M, Investment view: Trading 5% above fair value
> - Bond B: Can generate $10.3M, Investment view: Trading at fair value  
> - Bond C: Can generate $10.1M, Investment view: Trading 4% below fair value
>
> Which bond should be sold?

> **Wrong approach:**
> "Sell Bond B because it generates the most cash ($10.3M), maximizing proceeds."
>
> **Error:** All three bonds meet the $10M requirement. The extra $100K-$300K is immaterial compared to the investment implications of which position to exit.

> **Wrong approach 2:**
> "Sell Bond C because it generates the least cash ($10.1M), minimizing the position reduction."
>
> **Error:** This retains the overvalued Bond A while selling the undervalued Bond C—exactly backwards from an investment perspective.

> **Correct approach:**
> 1. All three bonds generate sufficient proceeds (>$10M)
> 2. Rank by investment merit:
>    - Bond A: Overvalued (least attractive to hold)
>    - Bond B: Fairly valued (neutral)
>    - Bond C: Undervalued (most attractive to hold)
> 3. Apply liquidation priority: Sell the least attractive position
> 4. **Answer: Sell Bond A**
>    - Exits overvalued position
>    - Retains undervalued Bond C with 4% upside potential
>    - Improves overall portfolio valuation profile

> **Key Insight:** When proceeds are adequate across options, liquidation becomes a portfolio optimization decision, not a cash maximization decision.

---

SKILL_MD_ENTRY: | `fixed_income/tax_exempt_liquidation.md` | Fixed Income | Tax-Exempt Liquidation Strategy | Tax-exempt liquidation decisions, Investment view hierarchy, Equal proceeds tiebreaker |