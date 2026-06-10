# SKILL PATTERNS FOR CORPORATE FINANCE PROGRAM OF THOUGHT

## Pattern: Formula Selection Based on Company Type (Public vs Private)

**Description:** Financial formulas often have different versions depending on company characteristics (public/private, size, industry). The Altman Z-score has distinct formulas for public companies (original) versus private companies (Z'-score) with different coefficients and variable definitions.

**When to Use:** When calculating credit risk scores, bankruptcy prediction models, or any financial metric where the question context specifies company type (private company, closely-held, non-public, etc.).

**Procedure:**
1. Formula (Private Company Z'-score): Z' = 0.717×X1 + 0.847×X2 + 3.107×X3 + 0.420×X4 + 0.998×X5
   - X1 = Working Capital / Total Assets
   - X2 = Retained Earnings / Total Assets
   - X3 = EBIT / Total Assets
   - X4 = Book Value of Equity / Total Liabilities (NOT market value)
   - X5 = Sales / Total Assets
2. Identify company type from context (look for keywords: "private company", "public company", "traded")
3. Select appropriate formula variant based on company type
4. Extract all required financial statement items
5. Calculate each ratio component separately for clarity
6. Apply correct coefficients to each ratio
7. Return final score as expression

**Code Example:**

**Scenario:** A private manufacturing company has: Total Assets = $500,000, EBIT = $45,000, Net Working Capital = $80,000, Book Value of Equity = $200,000, Retained Earnings = $120,000, Total Liabilities = $300,000, Sales = $600,000. Calculate the Z-score.

**Correct Code:**
```python
# Financial data
total_assets = 500000
ebit = 45000
net_working_capital = 80000
book_value_equity = 200000
retained_earnings = 120000
total_liabilities = 300000
sales = 600000

# Private company Z'-score ratios
x1 = net_working_capital / total_assets
x2 = retained_earnings / total_assets
x3 = ebit / total_assets
x4 = book_value_equity / total_liabilities  # Book value for private companies
x5 = sales / total_assets

# Private company Z'-score coefficients
z_score_private = (0.717 * x1 + 
                   0.847 * x2 + 
                   3.107 * x3 + 
                   0.420 * x4 + 
                   0.998 * x5)

z_score_private
```

**Common Bugs to Avoid:**
- Using public company coefficients (1.2, 1.4, 3.3, 0.6, 1.0) for private companies
- Using market value of equity instead of book value for X4 in private company formula
- Forgetting that X5 requires Sales data (not provided in some abbreviated statements)
- Using print() instead of returning expression on last line

---

## Pattern: Gordon Growth Model for Company Valuation

**Description:** When valuing a company or stock with constant dividend growth, use the Gordon Growth Model (Dividend Discount Model): V = D₁ / (r - g), where D₁ is next year's dividend, r is required return, and g is growth rate. This requires projecting dividends forward and determining the appropriate discount rate.

**When to Use:** Questions asking for "value of company", "valuation", "what is [company] worth" when context includes dividend information and expected growth rates. Trigger phrases: "constant growth", "perpetual growth", "dividends grow at X%".

**Procedure:**
1. Formula: V = D₁ / (r - g), where D₁ = D₀ × (1 + g)
2. Extract current dividend (D₀) from financial statements
3. Identify the growth rate (g) to apply (may differ from historical rate due to synergies/changes)
4. Calculate next period dividend: D₁ = D₀ × (1 + g)
5. Determine required return (r) using: current P/E ratio, dividend yield, CAPM, or given rate
   - If not given: r = (D₀/P₀) + g, where P₀ = EPS × P/E ratio
6. Verify r > g (model only valid when required return exceeds growth rate)
7. Apply formula: V = D₁ / (r - g)
8. Return total company value as expression

**Code Example:**

**Scenario:** A target company currently pays $350,000 in annual dividends with 750,000 shares outstanding. Current EPS is $1.50, P/E ratio is 9, and dividends historically grew at 3%. An acquirer believes they can increase growth to 4.5%. What is the company value?

**Correct Code:**
```python
# Current financial data
current_dividend = 350000
shares_outstanding = 750000
current_eps = 1.50
current_pe_ratio = 9
historical_growth = 0.03
new_growth_rate = 0.045

# Calculate current stock price
current_price_per_share = current_eps * current_pe_ratio

# Calculate current required return using dividend yield + growth
dividend_per_share = current_dividend / shares_outstanding
current_dividend_yield = dividend_per_share / current_price_per_share
required_return = current_dividend_yield + historical_growth

# Project next year's dividend with new growth rate
next_year_dividend = current_dividend * (1 + new_growth_rate)

# Gordon Growth Model valuation
company_value = next_year_dividend / (required_return - new_growth_rate)

company_value
```

**Common Bugs to Avoid:**
- Using D₀ instead of D₁ in numerator (must project dividend forward one period)
- Forgetting to convert growth rates from percentages (use 0.05 not 5)
- Using wrong growth rate (question may specify different rate than historical)
- Not deriving required return when not explicitly given
- Division by zero or negative denominator when r ≤ g (check validity)
- Calculating per-share value when total company value is requested

---

## Pattern: NPV of Stock-for-Stock Acquisitions

**Description:** For acquisitions paid with acquirer stock, NPV = (Value of Target with Synergies) - (Cost to Acquirer). Cost equals shares offered × acquirer's current market price per share. Target value requires discounting enhanced cash flows (often using Gordon Growth Model with improved growth rate).

**When to Use:** Acquisition questions where payment is in shares (not cash), asking for NPV, value creation, or whether deal is beneficial. Keywords: "offer X shares in exchange", "stock-for-stock", "share exchange", "NPV of acquisition".

**Procedure:**
1. Formula: NPV = V_target_with_synergies - Cost_to_acquirer
2. Calculate acquirer's price per share: P_acquirer = EPS_acquirer × PE_acquirer
3. Calculate cost: Cost = Shares_offered × P_acquirer
4. Value target with synergies using Gordon Growth Model:
   - D₁ = Target_current_dividend × (1 + enhanced_growth_rate)
   - Determine r using target's current metrics
   - V_target = D₁ / (r - g_enhanced)
5. Calculate NPV = V_target - Cost
6. Return NPV as expression (positive means value-creating deal)

**Code Example:**

**Scenario:** Acquirer Corp has 2,000,000 shares, EPS of $3.20, P/E of 12. Target Inc has current dividends of $600,000, historical growth of 3%, P/E of 8, and EPS of $1.10. Acquirer offers 300,000 shares and expects to increase Target's growth to 5%. Calculate NPV.

**Correct Code:**
```python
# Acquirer data
acquirer_shares = 2000000
acquirer_eps = 3.20
acquirer_pe = 12

# Target data
target_dividend = 600000
target_historical_growth = 0.03
target_pe = 8
target_eps = 1.10
target_shares = 1000000

# Acquisition terms
shares_offered = 300000
enhanced_growth = 0.05

# Step 1: Calculate acquirer's stock price
acquirer_price_per_share = acquirer_eps * acquirer_pe

# Step 2: Calculate cost to acquirer
cost_to_acquirer = shares_offered * acquirer_price_per_share

# Step 3: Determine target's required return
target_current_price = target_eps * target_pe
target_dividend_per_share = target_dividend / target_shares
target_dividend_yield = target_dividend_per_share / target_current_price
required_return = target_dividend_yield + target_historical_growth

# Step 4: Value target with enhanced growth (Gordon Growth Model)
next_year_dividend = target_dividend * (1 + enhanced_growth)
target_value_with_synergies = next_year_dividend / (required_return - enhanced_growth)

# Step 5: Calculate NPV
npv_acquisition = target_value_with_synergies - cost_to_acquirer

npv_acquisition
```

**Common Bugs to Avoid:**
- Using target's stock price to calculate cost (must use acquirer's price)
- Valuing target without synergies (use enhanced growth rate, not historical)
- Calculating cost as shares_offered × target_price (wrong reference point)
- Forgetting to project dividends forward one period (D₁ not D₀)
- Using wrong P/E ratio (acquirer's vs target's) for price calculations
- Not verifying that required_return > enhanced_growth before division

---

## Pattern: Internal Growth Rate vs Sustainable Growth Rate

**Description:** Internal Growth Rate (IGR) applies when NO external equity is issued: IGR = (ROA × b) / (1 - ROA × b). Sustainable Growth Rate (SGR) applies when debt-equity ratio is maintained through proportional financing: SGR = (ROE × b) / (1 - ROE × b). The choice depends on financing constraints specified in the question.

**When to Use:** Questions about maximum sales growth, sustainable expansion, or growth limits. Keywords: "no new equity", "no external equity", "internal financing only" → use IGR. Keywords: "maintain debt-equity ratio", "constant capital structure" → use SGR.

**Procedure:**
1. Formulas:
   - IGR = (ROA × b) / (1 - ROA × b)
   - SGR = (ROE × b) / (1 - ROE × b)
   - Where b = retention ratio = 1 - dividend payout ratio
2. Identify financing constraint from question (no new equity → IGR; maintain D/E → SGR)
3. Calculate retention ratio: b = 1 - (Dividends / Net Income)
4. For IGR: Calculate ROA = Net Income / Total Assets
5. For SGR: Calculate ROE = Net Income / Total Equity
6. Apply appropriate formula based on constraint
7. Calculate maximum sales increase: ΔSales = Current Sales × growth_rate
8. Return dollar increase as expression

**Code Example:**

**Scenario:** A company has Sales of $80,000, Net Income of $22,000, Total Assets of $200,000, Total Equity of $120,000, and pays 40% of earnings as dividends. The company maintains constant debt-equity ratio. What is the maximum sales increase?

**Correct Code:**
```python
# Financial data
sales = 80000
net_income = 22000
total_assets = 200000
total_equity = 120000
dividend_payout_ratio = 0.40

# Calculate retention ratio
retention_ratio = 1 - dividend_payout_ratio

# Identify constraint: "maintain debt-equity ratio" → use SGR
# Calculate ROE
roe = net_income / total_equity

# Sustainable Growth Rate formula
sgr = (roe * retention_ratio) / (1 - roe * retention_ratio)

# Maximum sales increase
max_sales_increase = sales * sgr

max_sales_increase
```

**Alternative Scenario (Internal Growth):** Same company but "no new equity is issued":

```python
# Same financial data as above
sales = 80000
net_income = 22000
total_assets = 200000
total_equity = 120000
dividend_payout_ratio = 0.40

# Calculate retention ratio
retention_ratio = 1 - dividend_payout_ratio

# Identify constraint: "no new equity" → use IGR
# Calculate ROA
roa = net_income / total_assets

# Internal Growth Rate formula
igr = (roa * retention_ratio) / (1 - roa * retention_ratio)

# Maximum sales increase
max_sales_increase = sales * igr

max_sales_increase
```

**Common Bugs to Avoid:**
- Using ROE when question specifies "no new equity" (should use ROA for IGR)
- Using ROA when question says "maintain debt-equity ratio" (should use ROE for SGR)
- Confusing payout ratio with retention ratio (b = 1 - payout, not payout itself)
- Forgetting to multiply growth rate by current sales to get dollar increase
- Using wrong denominator in ROA (Total Assets) vs ROE (Total Equity)
- Applying simplified formula g = ROE × b without checking if ROE × b < 1 (formula breaks down at high values)

---

## Pattern: Required Return Derivation from Market Data

**Description:** When required return (discount rate) is not explicitly given, it must be derived from available market data using relationships: r = (D/P) + g (dividend yield + growth), or from current valuation metrics like P/E ratios combined with growth assumptions.

**When to Use:** Valuation problems where discount rate is needed but not stated. Context provides P/E ratios, current prices, dividend yields, or historical growth rates that can be used to back out the required return.

**Procedure:**
1. Formula: r = (D₀/P₀) + g, where D₀ is current dividend, P₀ is current price, g is growth rate
2. If price not given but P/E is: P₀ = EPS × P/E
3. Calculate dividend per share: DPS = Total Dividends / Shares Outstanding
4. Calculate current price per share using P/E and EPS
5. Calculate dividend yield: Yield = DPS / P₀
6. Add historical growth rate: r = Yield + g
7. Use derived r in subsequent valuation calculations
8. Verify reasonableness (typical r ranges: 8-15% for equities)

**Code Example:**

**Scenario:** A company has 500,000 shares outstanding, EPS of $2.40, P/E ratio of 11, total annual dividends of $480,000, and historical growth of 4%. You need to value a project using this company's required return.

**Correct Code:**
```python
# Market data
shares_outstanding = 500000
eps = 2.40
pe_ratio = 11
total_dividends = 480000
historical_growth = 0.04

# Step 1: Calculate current stock price
current_price_per_share = eps * pe_ratio

# Step 2: Calculate dividend per share
dividend_per_share = total_dividends / shares_outstanding

# Step 3: Calculate dividend yield
dividend_yield = dividend_per_share / current_price_per_share

# Step 4: Derive required return
required_return = dividend_yield + historical_growth

# Verification check
if required_return < 0.05 or required_return > 0.20:
    # Flag unusual values for review
    pass

required_return
```

**Common Bugs to Avoid:**
- Assuming a required return without deriving it from given data
- Using total dividends instead of per-share dividends in yield calculation
- Forgetting to add growth rate to dividend yield (r = yield + g, not just yield)
- Using enhanced/future growth rate when deriving current required return (use historical g)
- Not converting P/E and EPS to price before calculating yield
- Skipping reasonableness check (required returns outside 5-20% range are suspicious)