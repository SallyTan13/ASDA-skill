# SKILL PATTERNS FOR CORPORATE FINANCE ARITHMETIC (Program of Thought)

## Pattern: Credit Policy NPV with Perpetuity Valuation

**Description:** Credit policy changes create perpetual incremental cash flows that must be valued using perpetuity formulas (CF/r), not single-period analysis. The receivables buildup is a one-time investment that must be compared against the present value of perpetual benefits.

**When to Use:** Questions about changing credit terms, payment policies, or sales conditions that affect ongoing cash flows and working capital requirements.

**Procedure:**
1. Formula: NPV = (Incremental Monthly Profit / r) - Receivables Investment
2. Calculate incremental monthly profit from increased sales: ΔUnits × (Price - Cost)
3. Value this as a perpetuity: PV = Monthly CF / Monthly Rate
4. Calculate one-time receivables investment: New Monthly Sales × Cost per Unit (or full price depending on context)
5. NPV = PV of perpetuity - Initial investment
6. Return NPV (positive means accept the policy change)

**Code Example:**

**Scenario:** A company considers changing from cash sales to net-30-day terms. Current sales: 800 units/month at $500/unit with $350 cost. New policy: 850 units/month. Required return: 1.2% per month.

**Correct Code:**
```python
# Given data
price_per_unit = 500
cost_per_unit = 350
current_units = 800
new_units = 850
monthly_rate = 0.012

# Step 1: Calculate incremental monthly profit
incremental_units = new_units - current_units
contribution_margin = price_per_unit - cost_per_unit
incremental_monthly_profit = incremental_units * contribution_margin

# Step 2: Value incremental profit as perpetuity
pv_incremental_profit = incremental_monthly_profit / monthly_rate

# Step 3: Calculate receivables investment (one-time outflow)
# Under net-30 terms, we tie up one month of sales at cost
receivables_investment = new_units * cost_per_unit

# Step 4: Calculate NPV
npv = pv_incremental_profit - receivables_investment

# Return the NPV
npv
```

**Common Bugs to Avoid:**
- Calculating single-period benefit instead of perpetuity value (dividing by rate)
- Using contribution margin instead of cost for receivables investment
- Forgetting that receivables buildup is a one-time outflow, not recurring
- Using annual rate when cash flows are monthly (must convert or use consistent periods)

---

## Pattern: Gordon Growth Model with Market-Implied Discount Rate

**Description:** When valuing a company with different growth assumptions, first extract the market's implied discount rate using current price, current dividends, and current growth expectations, then apply this rate to the new growth scenario.

**When to Use:** Acquisition valuation questions where you need to find maximum price to pay, given market data (P/E ratios, current prices) and synergy-driven growth rate changes.

**Procedure:**
1. Formula: P = D₀(1+g)/(r-g) or equivalently P = D₁/(r-g)
2. Calculate current market price: EPS × P/E ratio
3. Calculate dividend per share: Total Dividends / Shares Outstanding
4. Solve for implied r using current market price and current growth: r = [D₀(1+g_current)/P_current] + g_current
5. Apply this r to new growth scenario: P_new = D₀(1+g_new)/(r-g_new)
6. Return the new price per share

**Code Example:**

**Scenario:** Target company has 500,000 shares, $300,000 annual dividends, $600,000 earnings, P/E of 12. Market expects 3% growth. Acquirer believes synergies will increase growth to 5%. Find max price per share.

**Correct Code:**
```python
# Given data
shares_outstanding = 500_000
total_dividends = 300_000
total_earnings = 600_000
pe_ratio = 12
current_growth = 0.03
synergy_growth = 0.05

# Step 1: Calculate per-share metrics
dividend_per_share = total_dividends / shares_outstanding
eps = total_earnings / shares_outstanding

# Step 2: Calculate current market price
current_price = eps * pe_ratio

# Step 3: Extract market-implied discount rate
# Using Gordon Model: P = D0(1+g)/(r-g)
# Rearranging: r = [D0(1+g)/P] + g
d1_current = dividend_per_share * (1 + current_growth)
implied_r = (d1_current / current_price) + current_growth

# Step 4: Value with synergy growth rate
d1_synergy = dividend_per_share * (1 + synergy_growth)
max_price_per_share = d1_synergy / (implied_r - synergy_growth)

# Return maximum price per share
max_price_per_share
```

**Common Bugs to Avoid:**
- Using formula r = 1/PE + g (incorrect simplification)
- Deriving discount rate from the new growth scenario instead of current market conditions
- Using earnings instead of dividends in Gordon Growth Model
- Forgetting to multiply dividend by (1+g) to get D₁

---

## Pattern: Acquirer's Discount Rate in Acquisition Valuation

**Description:** In acquisition analysis, use the acquirer's required rate of return (cost of equity) as the discount rate when the question explicitly asks for the acquirer's valuation perspective or maximum price the acquirer should pay. The acquirer's opportunity cost determines valuation from their perspective.

**When to Use:** 
- Acquisition questions where the acquirer has different risk profile or cost of capital than the target
- Questions explicitly asking "what should the acquirer pay" or "from the acquirer's perspective"
- When acquirer's financial data (P/E, dividend policy, growth) is provided to establish their required return

**When NOT to Use:**
- When calculating gain from a revised growth assumption (use target's market-implied rate)
- When question asks about target's value or NPV without specifying acquirer's perspective
- When only target's financial data is provided in detail

**Procedure:**
1. Formula: P = D₀(1+g)/(r_acquirer - g)
2. Determine acquirer's required return from their own market data (P/E ratio, dividend yield, growth rate)
3. Use relationship: r = (Payout Ratio / P/E) + g_acquirer
4. Use target's dividend per share and the synergy-adjusted growth rate
5. Apply acquirer's discount rate: Max Price = D₀(1+g_synergy)/(r_acquirer - g_synergy)
6. Return the valuation per share

**Worked Example:**

**Question:** An acquirer has a P/E of 16, pays 35% of earnings as dividends, and expects 5% growth. A target pays $1.20/share dividends, currently grows at 4%, and synergies would enable 7% growth. What is the maximum price per share the acquirer should pay?

```python
# Acquirer data
acquirer_pe = 16
acquirer_payout_ratio = 0.35
acquirer_growth = 0.05

# Target data
target_dividend_per_share = 1.20
target_current_growth = 0.04
synergy_growth = 0.07

# Step 1: Calculate acquirer's required return
# Using relationship: r = Payout/P/E + g
acquirer_required_return = (acquirer_payout_ratio / acquirer_pe) + acquirer_growth

# Step 2: Value target using acquirer's discount rate and synergy growth
# Gordon Model: P = D0(1+g)/(r-g)
d1_target = target_dividend_per_share * (1 + synergy_growth)
max_price_per_share = d1_target / (acquirer_required_return - synergy_growth)

# Return maximum price
max_price_per_share
```

**Common Bugs to Avoid:**
- Using this pattern when question asks about "gain from revised growth" (should use target's rate)
- Back-solving for discount rate from target's current price when acquirer's rate is needed
- Mixing growth rates (using current growth to derive r, then applying same r to different growth)
- Applying acquirer's rate when only target's market data is provided
- Ignoring context clues about whose perspective the valuation represents

**CHECK Steps:**
- Verify question explicitly asks for acquirer's perspective or maximum price to pay
- Confirm acquirer's financial data (P/E, payout, growth) is provided in the problem
- If question mentions "gain" or "revised growth assumptions," consider using target's rate instead
- Ensure you're not mixing acquirer's discount rate derivation with target's market valuation
## Pattern: Acquisition NPV Calculation

**Description:** NPV of an acquisition equals the present value of the target under post-acquisition conditions minus the total acquisition cost. Must use correct discount rate derived from pre-acquisition market conditions.

**When to Use:** Questions asking for NPV of an acquisition offer, whether to proceed with a takeover, or value creation from a merger.

**Procedure:**
1. Formula: NPV = PV(Target with Synergies) - Acquisition Cost
2. Calculate current market price using target's P/E and EPS
3. Derive discount rate from current price, dividends, and current growth: r = [D₀(1+g_current)/P_current] + g_current
4. Calculate PV with synergy growth: PV = [D₀(1+g_synergy)/(r-g_synergy)] × Shares
5. Calculate acquisition cost: Offer Price × Shares Outstanding
6. NPV = PV - Acquisition Cost

**Code Example:**

**Scenario:** Target has 400,000 shares, $240,000 dividends, $480,000 earnings, P/E of 11. Market expects 3.5% growth. Acquirer offers $14/share and expects 5.5% growth from synergies.

**Correct Code:**
```python
# Target data
shares_outstanding = 400_000
total_dividends = 240_000
total_earnings = 480_000
pe_ratio = 11
current_growth = 0.035
synergy_growth = 0.055

# Acquisition terms
offer_price_per_share = 14

# Step 1: Calculate per-share metrics
dividend_per_share = total_dividends / shares_outstanding
eps = total_earnings / shares_outstanding

# Step 2: Calculate current market price
current_price = eps * pe_ratio

# Step 3: Extract discount rate from current market conditions
d1_current = dividend_per_share * (1 + current_growth)
discount_rate = (d1_current / current_price) + current_growth

# Step 4: Calculate PV of target with synergy growth
d1_synergy = dividend_per_share * (1 + synergy_growth)
value_per_share_with_synergy = d1_synergy / (discount_rate - synergy_growth)
total_pv_with_synergy = value_per_share_with_synergy * shares_outstanding

# Step 5: Calculate acquisition cost
acquisition_cost = offer_price_per_share * shares_outstanding

# Step 6: Calculate NPV
npv = total_pv_with_synergy - acquisition_cost

# Return NPV
npv
```

**Common Bugs to Avoid:**
- Calculating NPV as (synergy value - current market value) instead of (synergy value - acquisition cost)
- Using earnings instead of dividends in Gordon Growth Model
- Applying synergy growth rate when deriving the discount rate (should use current growth)
- Forgetting to multiply per-share values by shares outstanding for total NPV

---

## Pattern: Acquisition Gain with Growth Rate Adjustments

**Description:** Acquisition gain is the difference between the PV of the target with synergies and the acquisition cost. When growth assumptions change, recalculate using the same discount rate but updated growth. The gain represents the incremental value from the revised synergy scenario compared to the acquisition price paid.

**When to Use:** Questions asking for gain/value creation when growth rate assumptions are revised (e.g., "consultants think 5% is more realistic than 6%").

**When NOT to Use:** 
- When the question asks for NPV of the acquisition itself (use Acquisition NPV Calculation pattern instead)
- When comparing different acquisition offers or prices
- When the acquirer's discount rate is explicitly different from the target's market-implied rate

**Procedure:**
1. Formula: Gain = [D₀(1+g_revised)/(r-g_revised)] × Shares - Acquisition Cost
2. **CRITICAL**: Derive discount rate from TARGET's current market conditions (not acquirer's)
3. Use TARGET's P/E ratio and current growth to extract r: r = [D₀(1+g_current)/P_current] + g_current
4. Apply revised growth rate to calculate new PV using this same discount rate
5. Determine acquisition cost (if not explicitly given, use current market value: P/E × EPS × Shares)
6. Calculate gain: PV_revised - Acquisition Cost
7. Return the gain (can be positive or negative)

**Worked Example:**

**Question:** A target company has 500,000 shares, $400,000 annual dividends, $800,000 earnings, and a P/E ratio of 12. The market expects 3% growth. An acquirer initially projected 7% synergy growth but consultants revised it to 5%. What is the gain from acquisition?

```python
# Target company data
shares_outstanding = 500_000
total_dividends = 400_000
total_earnings = 800_000
pe_ratio = 12
current_market_growth = 0.03
revised_synergy_growth = 0.05

# Step 1: Calculate per-share metrics
dividend_per_share = total_dividends / shares_outstanding
eps = total_earnings / shares_outstanding

# Step 2: Calculate current market price
current_market_price = eps * pe_ratio

# Step 3: Extract TARGET's market-implied discount rate
# Using current market conditions (current growth rate)
d1_current = dividend_per_share * (1 + current_market_growth)
target_discount_rate = (d1_current / current_market_price) + current_market_growth

# Step 4: Calculate PV with REVISED synergy growth
# Use the same discount rate derived from target's market
d1_revised = dividend_per_share * (1 + revised_synergy_growth)
value_per_share_revised = d1_revised / (target_discount_rate - revised_synergy_growth)
total_pv_revised = value_per_share_revised * shares_outstanding

# Step 5: Calculate acquisition cost (current market value if not specified)
acquisition_cost = current_market_price * shares_outstanding

# Step 6: Calculate gain
gain = total_pv_revised - acquisition_cost

# Return gain
gain
```

**Common Bugs to Avoid:**
- **Using acquirer's discount rate instead of target's market-implied rate** (most common error in Q⁻)
- Recalculating discount rate with the revised growth (should keep original r from current market)
- Comparing revised value to original synergy value instead of acquisition cost
- Using total dividends instead of dividend per share in Gordon Model
- Forgetting that gain measures value above acquisition cost, not above current market value
- Deriving discount rate from acquirer's P/E when target's market data is available

**CHECK Steps:**
- Verify discount rate is derived from TARGET's current market price and current growth expectations
- Confirm acquisition cost uses either: (a) explicitly stated offer price, or (b) current market value (P/E × EPS × Shares)
- Ensure the same discount rate is used for both original and revised growth scenarios
- Validate that gain = PV(revised growth) - Acquisition Cost, not PV(revised) - PV(original)
- If acquirer's P/E is mentioned but question asks about target's value change, use target's implied rate

---
## Pattern: Altman Z-Score Variant Selection

**Description:** Altman Z-Score has multiple variants with different coefficients: original Z (public manufacturers), Z' (private manufacturers), and Z'' (private non-manufacturers/service). When sales data is missing, use Z'' which excludes the sales/assets ratio.

**When to Use:** Credit risk assessment questions for private companies, especially when sales data is not provided in the financial information.

**Procedure:**
1. Formula (Z'' for private firms without sales): Z'' = 6.56X₁ + 3.26X₂ + 6.72X₃ + 1.05X₄
2. X₁ = Working Capital / Total Assets
3. X₂ = Retained Earnings / Total Assets
4. X₃ = EBIT / Total Assets
5. X₄ = Book Value of Equity / Total Liabilities
6. Calculate each ratio, multiply by coefficient, sum for Z-score

**Code Example:**

**Scenario:** Private company has: Total Assets $85,000, EBIT $9,500, Net Working Capital $5,100, Book Equity $22,000, Retained Earnings $18,500, Total Liabilities $63,000. No sales data available.

**Correct Code:**
```python
# Financial data
total_assets = 85_000
ebit = 9_500
net_working_capital = 5_100
book_value_equity = 22_000
retained_earnings = 18_500
total_liabilities = 63_000

# Step 1: Calculate Z-score components
x1 = net_working_capital / total_assets
x2 = retained_earnings / total_assets
x3 = ebit / total_assets
x4 = book_value_equity / total_liabilities

# Step 2: Apply Z'' coefficients (for private firms without sales)
# Z'' = 6.56*X1 + 3.26*X2 + 6.72*X3 + 1.05*X4
z_score = (6.56 * x1) + (3.26 * x2) + (6.72 * x3) + (1.05 * x4)

# Return Z-score
z_score
```

**Common Bugs to Avoid:**
- Using Z' coefficients (0.717, 0.847, 3.107, 0.420, 0.998) when sales data is missing
- Estimating sales from EBIT margin assumptions instead of using Z''
- Using original Z-Score for private companies (requires public market data)
- Confusing retained earnings with net income in X₂ calculation

---

## Pattern: Dividend vs Earnings in Valuation Models

**Description:** Gordon Growth Model and dividend discount models require dividend cash flows, not earnings. Always use dividends per share (or total dividends) as the cash flow input, even when earnings data is provided.

**When to Use:** Any valuation question using dividend discount model, Gordon Growth Model, or constant growth valuation formulas.

**Procedure:**
1. Formula: P = D₀(1+g)/(r-g) where D is dividends, NOT earnings
2. Calculate dividend per share: Total Dividends / Shares Outstanding
3. Never substitute earnings for dividends in the numerator
4. If payout ratio is given, can derive: D = Earnings × Payout Ratio
5. Apply growth to dividends: D₁ = D₀(1+g)

**Code Example:**

**Scenario:** Company has 600,000 shares, $900,000 earnings, $360,000 dividends. Required return 10%, growth 4%. Find value per share.

**Correct Code:**
```python
# Given data
shares_outstanding = 600_000
total_earnings = 900_000
total_dividends = 360_000
required_return = 0.10
growth_rate = 0.04

# Step 1: Calculate dividend per share (NOT earnings per share)
dividend_per_share = total_dividends / shares_outstanding

# Step 2: Calculate next year's dividend
d1 = dividend_per_share * (1 + growth_rate)

# Step 3: Apply Gordon Growth Model using DIVIDENDS
value_per_share = d1 / (required_return - growth_rate)

# Return value per share
value_per_share
```

**Common Bugs to Avoid:**
- Using earnings instead of dividends in Gordon Growth Model
- Calculating EPS and applying it directly to valuation formula
- Forgetting that only dividends are cash flows to equity holders in this model
- Using total values instead of per-share values inconsistently

---

## Pattern: Receivables Investment in Credit Policy

**Description:** When extending credit terms, the receivables investment represents capital tied up. For cost-based analysis, use cost per unit; for full revenue analysis, use price per unit. Context determines which is appropriate.

**When to Use:** Credit policy changes, working capital investment calculations, or questions about financing receivables buildup.

**Procedure:**
1. Identify what capital is "tied up" - typically the cost of goods sold
2. Calculate monthly receivables: Units Sold per Month × Cost per Unit
3. For net-30 terms, investment = 1 month of sales at cost
4. For net-60 terms, investment = 2 months of sales at cost
5. This is a one-time investment (outflow) at policy change

**Code Example:**

**Scenario:** Company sells 1,000 units/month at $600/unit with $420 cost. Changing from cash to net-30 terms. Calculate receivables investment.

**Correct Code:**
```python
# Given data
units_per_month = 1_000
price_per_unit = 600
cost_per_unit = 420
credit_period_months = 1  # net-30 = 1 month

# Step 1: Calculate receivables investment
# Use COST per unit (capital tied up in production)
receivables_investment = units_per_month * cost_per_unit * credit_period_months

# Return investment amount
receivables_investment
```

**Common Bugs to Avoid:**
- Using contribution margin instead of cost for investment calculation
- Using price per unit when cost per unit is appropriate (overstates investment)
- Treating receivables as recurring cost instead of one-time investment
- Forgetting to adjust for credit period length (30 days vs 60 days)