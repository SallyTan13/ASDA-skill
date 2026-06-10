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

**Description:** When required return (discount rate) is not explicitly given, it must be derived from available market data using relationships: r = (D/P) + g (dividend yield + growth), or from current valuation metrics like P/E ratios combined with growth assumptions. For project evaluation using CAPM, use r = rf + β(rm - rf).

**When to Use:** Valuation problems where discount rate is needed but not stated. Context provides P/E ratios, current prices, dividend yields, or historical growth rates that can be used to back out the required return. For project evaluation with systematic risk, use CAPM when beta, risk-free rate, and market return are provided.

**When NOT to Use:** 
- When the question asks for multiple outputs (e.g., both NPV and another metric) - ensure all requested values are calculated and returned
- When CAPM is used for project evaluation, do not stop at calculating the discount rate; proceed to calculate the full NPV and any other requested metrics

**Procedure:**
1. Identify the type of required return calculation:
   - For equity valuation: r = (D₀/P₀) + g
   - For project evaluation with systematic risk: r = rf + β(rm - rf) (CAPM)
2. If price not given but P/E is: P₀ = EPS × P/E
3. For dividend-based approach:
   - Calculate dividend per share: DPS = Total Dividends / Shares Outstanding
   - Calculate current price per share using P/E and EPS
   - Calculate dividend yield: Yield = DPS / P₀
   - Add historical growth rate: r = Yield + g
4. For CAPM approach:
   - Extract risk-free rate (rf), market return (rm), and beta (β)
   - Calculate: r = rf + β(rm - rf)
5. Use derived r in subsequent valuation calculations (NPV, present value, etc.)
6. **CRITICAL:** If question asks for multiple outputs, ensure ALL are calculated and returned as a tuple
7. Verify reasonableness (typical r ranges: 8-15% for equities, may be higher for risky projects)

**Common Mistakes to Avoid:**
- Assuming a required return without deriving it from given data
- Using total dividends instead of per-share dividends in yield calculation
- Forgetting to add growth rate to dividend yield (r = yield + g, not just yield)
- Using enhanced/future growth rate when deriving current required return (use historical g)
- Not converting P/E and EPS to price before calculating yield
- Skipping reasonableness check (required returns outside 5-20% range are suspicious)
- **Calculating the discount rate but not proceeding to calculate NPV or other requested metrics**
- **Returning only one value when the question explicitly asks for multiple outputs (e.g., NPV AND maximum beta)**

**Example (sanitized):**
> **Scenario:** A project has beta of 1.5, risk-free rate is 6%, market return is 14%. Initial investment is $50M, and it generates $12M annually for 8 years. Calculate the NPV and find the maximum beta before NPV becomes negative.
> 
> **Wrong approach:** Calculate required return using CAPM (r = 0.06 + 1.5 × 0.08 = 0.18), then return only the maximum beta value.
> 
> **Correct approach:** 
> 1. Calculate required return: r = 0.06 + 1.5 × (0.14 - 0.06) = 0.18
> 2. Calculate NPV with initial beta: NPV = -50 + Σ(12/(1.18)^t) for t=1 to 8
> 3. Find maximum beta by solving for beta where NPV = 0
> 4. Return BOTH values as tuple: (npv_initial, max_beta)

---

## Pattern: Multi-Output Project Evaluation

**Description:** When questions ask for multiple related metrics (e.g., NPV at a given discount rate AND a threshold parameter like maximum beta or optimal timing), all requested outputs must be calculated and returned together. This pattern ensures complete answers to multi-part questions.

**When to Use:** Questions that explicitly request multiple outputs such as:
- "Calculate NPV and find the maximum/minimum [parameter]"
- "What is the NPV? What is the optimal [decision variable]?"
- "Compute [metric] for different scenarios and identify which maximizes value"

**Procedure:**
1. Parse the question to identify ALL requested outputs (typically 2-3 related metrics)
2. Calculate the primary metric (e.g., NPV at given parameters)
3. Calculate secondary metrics (e.g., threshold values, optimal decisions)
4. For optimization questions (find maximum/minimum):
   - If finding a threshold: Use binary search or iterative methods to find the parameter value where a condition is met (e.g., NPV = 0)
   - If finding optimal choice: Calculate metric for all options and identify the maximizing/minimizing choice
5. **CRITICAL:** Return ALL requested values in the format that matches the question structure:
   - If two numeric values requested: return as tuple (value1, value2)
   - If numeric value and categorical choice: return the categorical choice (number or label) as the final answer
6. Verify the return statement matches what the question asks for in its final sentence

**Code Example:**

**Scenario:** A project requires $100M investment and generates $25M annually for 6 years. With beta=2.0, rf=5%, rm=12%, calculate the NPV. Also find the maximum beta before NPV becomes negative.

**Correct Code:**
```python
# Project parameters
initial_investment = 100_000_000
annual_cash_flow = 25_000_000
years = 6
rf = 0.05
rm = 0.12
initial_beta = 2.0

# Calculate required return using CAPM
def calculate_required_return(beta):
    return rf + beta * (rm - rf)

# NPV calculation function
def calculate_npv(beta):
    r = calculate_required_return(beta)
    npv = -initial_investment
    for year in range(1, years + 1):
        npv += annual_cash_flow / (1 + r)**year
    return npv

# Part 1: Calculate NPV with initial beta
npv_at_initial_beta = calculate_npv(initial_beta)

# Part 2: Find maximum beta where NPV = 0
def find_max_beta():
    left, right = 0.0, 10.0
    while right - left > 0.001:
        mid = (left + right) / 2
        if calculate_npv(mid) >= 0:
            left = mid
        else:
            right = mid
    return left

max_beta_threshold = find_max_beta()

# Return BOTH requested values as tuple
(npv_at_initial_beta, max_beta_threshold)
```

**Common Mistakes to Avoid:**
- Returning only the final calculated value when multiple outputs are requested
- Returning intermediate calculations instead of the final requested metrics
- Not reading the question's final sentence to determine what format the answer should take
- For optimization questions, returning the metric value instead of the optimal choice (e.g., returning NPV instead of the year that maximizes NPV)

---

## Pattern: Project Abandonment and Optimal Timing

**Description:** When evaluating projects with flexibility to abandon at different time points, calculate NPV for each possible abandonment scenario and identify which timing maximizes firm value. The question asks for the optimal decision (timing), not the NPV value itself.

**When to Use:** Questions asking about:
- "What economic life maximizes value?"
- "When should the project be abandoned?"
- "Which year should the project end to maximize NPV?"
- Context provides salvage values or market values at different time points

**Procedure:**
1. Identify all possible abandonment/termination time points from the question
2. For each time point, calculate complete NPV including:
   - Initial investment and working capital
   - Operating cash flows for the active period
   - Depreciation tax shields
   - Terminal cash flows: salvage value, tax on salvage (gain/loss), NWC recovery
3. Calculate tax implications of salvage:
   - Book value at time t = Initial Investment - (Accumulated Depreciation)
   - Gain/Loss on sale = Salvage Value - Book Value
   - Tax on salvage = (Gain/Loss) × Tax Rate
4. Compare NPVs across all scenarios
5. **CRITICAL:** Return the TIME POINT (year/period) that maximizes NPV, NOT the NPV value itself
6. If question asks "what maximizes value", the answer is the decision variable (timing), not the dollar amount

**Code Example:**

**Scenario:** A manufacturing project requires $20M investment (depreciated straight-line over 5 years) and $1M in NWC. It generates $8M revenue and $3M costs annually. Tax rate is 35%, discount rate is 12%. Equipment market values: Year 1: $16M, Year 2: $12M, Year 3: $8M, Year 4: $4M, Year 5: $0. What economic life maximizes value?

**Correct Code:**
```python
# Project parameters
initial_investment = 20_000_000
nwc = 1_000_000
annual_revenue = 8_000_000
annual_costs = 3_000_000
tax_rate = 0.35
discount_rate = 0.12
project_life = 5

# Market values at different years
market_values = {1: 16_000_000, 2: 12_000_000, 3: 8_000_000, 4: 4_000_000, 5: 0}

def calculate_npv_for_life(economic_life):
    # Annual depreciation
    annual_depreciation = initial_investment / project_life
    
    # Initial cash flow
    cf = [-initial_investment - nwc]
    
    # Operating cash flows
    for year in range(1, economic_life + 1):
        ebit = annual_revenue - annual_costs - annual_depreciation
        tax = ebit * tax_rate
        ocf = ebit - tax + annual_depreciation
        cf.append(ocf)
    
    # Terminal year adjustments
    book_value = initial_investment - (annual_depreciation * economic_life)
    salvage = market_values[economic_life]
    tax_on_salvage = (salvage - book_value) * tax_rate
    
    cf[-1] += salvage - tax_on_salvage + nwc
    
    # Calculate NPV
    npv = sum(cash / (1 + discount_rate)**t for t, cash in enumerate(cf))
    return npv

# Calculate NPV for each possible economic life
npvs = {}
for life in range(1, project_life + 1):
    npvs[life] = calculate_npv_for_life(life)

# Find optimal economic life (the YEAR, not the NPV)
optimal_life = max(npvs, key=npvs.get)

# Return the optimal timing decision
optimal_life
```

**Common Mistakes to Avoid:**
- Returning the NPV value instead of the optimal time period
- Not including all terminal cash flows (salvage, tax on salvage, NWC recovery)
- Forgetting to calculate tax implications of salvage value (gain/loss on sale)
- Using wrong book value calculation (must account for accumulated depreciation)
- Not recovering working capital in terminal year
- Comparing scenarios without proper discounting of all cash flows