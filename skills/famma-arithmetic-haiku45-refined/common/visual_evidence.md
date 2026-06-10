# DETAILED SKILL PATTERNS FOR VISUAL EVIDENCE EXTRACTION IN PROGRAM OF THOUGHT

---

## Pattern: OCR_Ambiguity_Resolution_and_Sign_Detection

**Description:** OCR output often contains ambiguous representations of negative signs, missing decimal points, or formatting artifacts (e.g., '%5' vs '-5%', '9' vs '60'). Code must validate extracted values against context clues, expected ranges, and answer options before proceeding with calculations. **However, avoid over-correcting or rounding prematurely when the OCR output is already clear and unambiguous.**

**When to Use:** Any problem involving tabular data extraction from images, especially when dealing with percentage returns, financial metrics, or probability distributions where negative values are plausible **AND where there are clear signs of OCR errors** (unusual formatting, values outside expected ranges, or inconsistencies with answer options).

**When NOT to Use:** 
- When OCR values are clearly formatted and fall within expected ranges for the domain
- When the question asks for precise decimal answers (e.g., "closest to") and premature rounding would reduce accuracy
- When all values in a table are consistently formatted without artifacts
- When attempting to "fix" values would introduce more error than accepting them as-is
- **When calculated results using OCR values as-is already match answer options within reasonable tolerance**
- **When OCR shows standard percentage formatting (e.g., "8%", "13%") without unusual artifacts like "%8" or missing signs**

**Procedure:**
1. Extract raw OCR values into structured data (lists/dicts)
2. **First check if values are already reasonable** - if all values fall within expected ranges and are consistently formatted, skip correction steps
3. **Calculate initial result using OCR values as-is and compare to answer options** - if result matches an option, no correction needed
4. Validate each numeric value against expected ranges (e.g., stock returns typically -50% to +100%) **only if there are outliers or formatting anomalies**
5. Check for outliers that suggest OCR errors (e.g., one value 9% when others are 55-71%)
6. Cross-reference with answer options to detect sign errors or magnitude misreads **only when calculated results don't match any option**
7. When ambiguous, test both interpretations and select the one yielding results matching answer format
8. Document assumptions explicitly in comments
9. **Preserve precision**: Do not round intermediate or final results unless the question explicitly asks for rounded values or the answer options indicate rounding is expected

**Common Mistakes to Avoid:**
- Rounding to "match table format" when the question requires decimal precision (e.g., rounding 12.75% to 12.8% or 20.35 years to 20)
- Applying correction logic to already-clear OCR values, introducing errors where none existed
- Assuming all OCR output needs validation when values are consistently formatted
- Over-interpreting minor formatting differences as errors requiring correction
- **"Correcting" standard percentage formats (e.g., changing "8%" to "23%") when no OCR artifact is present**
- **Reordering table values based on assumed logical ordering when the original OCR may be correct**

**Example (sanitized):**
> **Scenario:** Calculate expected return from returns: State 1: 8%, State 2: 13%, State 3: 12%. All values clearly formatted.
> **Wrong approach:** Assume first value should be higher, "correct" 8% to 18% based on pattern expectations
> **Correct approach:** Use OCR values as-is since they're clearly formatted and within expected ranges (5-20% for stock returns)

---
## Pattern: Table_Column_Alignment_and_Header_Mapping

**Description:** OCR text often loses spatial structure of tables, making it unclear which values belong to which columns. Code must systematically map column headers to data rows, especially when headers are separated from data or when multiple stocks/securities share similar formatting. **Critical: Verify each item appears only once in the correct category (asset vs liability, stock A vs stock B) to avoid double-counting or misclassification.**

**When to Use:** Problems with multi-column tables showing returns, probabilities, or characteristics for multiple securities across different states/scenarios, **or financial statements with distinct categories** (assets vs liabilities, different securities).

**When NOT to Use:**
- When the table structure is simple and unambiguous (single column of values)
- When there's no risk of confusing categories or entities

**Procedure:**
1. Identify column headers explicitly from OCR text
2. Count expected columns and validate against data rows
3. Use consistent indexing (0-based) to map headers to data positions
4. Create structured data (DataFrame or dict) with explicit column names
5. **Verify each data item is classified into exactly one category** - check for duplicate entries across mutually exclusive categories (e.g., an item cannot be both an asset AND a liability)
6. Validate that each row has correct number of values
7. Cross-check extracted values by computing simple aggregates (e.g., probabilities sum to 1.0, assets = liabilities + equity)

**Common Mistakes to Avoid:**
- Classifying the same item in multiple mutually exclusive categories (e.g., "Federal funds deposits" as both asset and liability)
- Not verifying that balance sheet equation holds after data extraction (Assets = Liabilities + Equity)
- Assuming column order without checking if an item logically belongs in that category
- Failing to validate that category totals make sense (e.g., total liabilities should not include asset items)

**Example (sanitized):**
> **Scenario:** Balance sheet shows: Cash $100K, Loans $500K, Deposits $400K, Equity $200K
> **Wrong approach:** Classify "Deposits" as both an asset (deposits made by bank) and liability (deposits from customers) based on name alone
> **Correct approach:** Use context to determine Deposits are customer deposits (liability), verify Assets ($600K) = Liabilities ($400K) + Equity ($200K)

---
## Pattern: Missing_Visual_Data_Detection_and_Handling

**Description:** When critical data is referenced in images that aren't accessible (e.g., "image_2 shows portfolio weights"), code must detect this gap and either halt with clear error message or document assumptions explicitly rather than silently substituting default values.

**When to Use:** Problems referencing multiple images where some contain essential numerical inputs (weights, prices, dates) that cannot be inferred from context.

**Procedure:**
1. Identify all data inputs required for calculation
2. Check which inputs are available from OCR vs. which require visual inspection
3. If critical visual data is missing, raise informative error OR document assumption prominently
4. Never silently substitute default values (e.g., equal weights) without explicit justification
5. If proceeding with assumptions, validate results against answer options to detect assumption errors

**Code Example:**

**Scenario:** Portfolio calculation requires weights from image_2, but only stock data from image_1 is available

**Correct Code:**
```python
# Available data from image_1 (OCR)
stock_data = {
    'Stock_A': {'return': 0.12, 'beta': 0.9, 'std': 0.25},
    'Stock_B': {'return': 0.15, 'beta': 1.2, 'std': 0.30}
}

# Portfolio weights should come from image_2 (NOT AVAILABLE)
portfolio_weights = None  # Explicitly mark as unavailable

# Step 1: Check for missing critical data
if portfolio_weights is None:
    # Option A: Raise error (preferred for exam/grading scenarios)
    # raise ValueError("Portfolio weights from image_2 are required but not available")
    
    # Option B: Document assumption and proceed (only if justified)
    print("WARNING: Portfolio weights not available from image_2")
    print("ASSUMPTION: Using equal weights (50/50) - results may be incorrect")
    portfolio_weights = {'Stock_A': 0.5, 'Stock_B': 0.5}
    assumption_made = True
else:
    assumption_made = False

# Step 2: Proceed with calculation, marking uncertainty
expected_return = sum(
    portfolio_weights[stock] * stock_data[stock]['return'] 
    for stock in ['Stock_A', 'Stock_B']
)

# Step 3: Return result with metadata about assumptions
result = {
    'expected_return': round(expected_return, 4),
    'assumption_made': assumption_made,
    'assumption_details': 'Equal weights assumed due to missing image_2 data' if assumption_made else None
}

result
```

**Common Bugs to Avoid:**
- Silently using default values (equal weights, zero values) without documentation
- Proceeding with calculations when critical inputs are unavailable
- Not flagging when assumptions fundamentally change the answer
- Failing to validate assumed values against answer options
- Not recognizing that missing visual data makes accurate computation impossible

---

## Pattern: Numeric_Value_Range_Validation_for_OCR

**Description:** OCR frequently misreads similar-looking digits (0/6, 1/7, 5/6, 9/0) or decimal positions. Code must validate extracted numbers against domain-specific ranges and cross-check with related values in the same table. **However, validation should not introduce rounding or precision loss when the OCR values are already correct.**

**When to Use:** Any financial calculation using OCR-extracted numbers, especially standard deviations, returns, prices, or percentages where misreads would produce obviously wrong results **AND where there are clear signs of OCR errors** (outliers, inconsistent patterns).

**When NOT to Use:**
- When all extracted values fall within expected ranges and show consistent patterns
- When the question requires high precision and rounding would reduce accuracy
- When validation would involve rounding intermediate results that need to be preserved
- **When the question explicitly asks for fractional time periods (e.g., "years to maturity" in compound interest problems)**
- **When answer options or ground truth show decimal precision (e.g., 10.64 years, 20.35 years)**

**Procedure:**
1. Define expected ranges for each type of value (e.g., stock returns: -50% to +200%, probabilities: 0 to 1, std dev: 0% to 100%)
2. After extraction, check each value against its expected range
3. Compare values within same category (e.g., all stock std devs should be similar magnitude)
4. Flag outliers that differ by >3x from median of similar values
5. When outlier detected, check for common OCR errors (9↔0, 6↔0, missing negative sign)
6. If correction unclear, document the ambiguity
7. **Preserve full precision in calculations** - do not round to "appropriate precision" unless the question explicitly requires it or answer options indicate rounding
8. **For time-based calculations (years, duration), preserve decimal precision unless context clearly indicates integer values are expected**

**Common Mistakes to Avoid:**
- Rounding calculated results to match perceived "table format" when precision is needed (e.g., rounding 12.75% to 12.8%)
- Applying validation logic that introduces precision loss to already-correct values
- Assuming integer values are always appropriate (e.g., years can be fractional in financial calculations)
- **Rounding time periods to whole numbers when financial formulas produce fractional results (e.g., 10.64 years → 11 years)**
- **Assuming "years are typically integers" when compound interest calculations inherently produce fractional time periods**

**Example (sanitized):**
> **Scenario:** Calculate years to maturity: PV=$1,000, FV=$2,500, Rate=8%. Formula gives n = 11.91 years.
> **Wrong approach:** Round to 12 years because "years are typically whole numbers"
> **Correct approach:** Return 11.91 years as calculated, preserving decimal precision since compound interest formulas naturally produce fractional time periods

---
## Pattern: State_Based_Portfolio_Return_Calculation

**Description:** When calculating portfolio statistics across multiple states of nature, must correctly compute portfolio returns for each state first, then aggregate using probabilities. Common error is computing individual security statistics then combining, which ignores correlation structure.

**When to Use:** Problems involving probability distributions across economic states (boom/normal/bust) with portfolio weights and multiple securities.

**Procedure:**
1. Formula: Portfolio return in state i = Σ(weight_j × return_j_i) for all securities j
2. Formula: Expected portfolio return = Σ(probability_i × portfolio_return_i) for all states i
3. Formula: Portfolio variance = Σ(probability_i × (portfolio_return_i - expected_return)²)
4. Extract state probabilities, returns for each security in each state, and portfolio weights
5. Calculate portfolio return for EACH state separately
6. Use state-based portfolio returns to compute expected return and variance
7. Standard deviation = sqrt(variance)

**Code Example:**

**Scenario:** 3 states (boom/normal/bust), 2 stocks, portfolio weights 60% Stock_X, 40% Stock_Y

**Correct Code:**
```python
import numpy as np

# Step 1: Extract data - returns for each stock in each state
states = ['Boom', 'Normal', 'Bust']
probabilities = np.array([0.25, 0.50, 0.25])

returns_stock_x = np.array([0.30, 0.12, -0.10])  # Returns in each state
returns_stock_y = np.array([0.20, 0.08, 0.05])

# Portfolio weights
weight_x = 0.60
weight_y = 0.40

# Step 2: Calculate portfolio return in EACH state
portfolio_returns_by_state = (weight_x * returns_stock_x + 
                              weight_y * returns_stock_y)

# Step 3: Calculate expected portfolio return
expected_portfolio_return = np.sum(probabilities * portfolio_returns_by_state)

# Step 4: Calculate portfolio variance
# Variance = E[(R - E[R])^2] = Σ p_i * (R_i - E[R])^2
portfolio_variance = np.sum(
    probabilities * (portfolio_returns_by_state - expected_portfolio_return)**2
)

# Step 5: Calculate portfolio standard deviation
portfolio_std_dev = np.sqrt(portfolio_variance)

# Step 6: Return results as expression
{
    'expected_return': round(expected_portfolio_return, 4),
    'variance': round(portfolio_variance, 6),
    'std_deviation': round(portfolio_std_dev, 4),
    'portfolio_returns_by_state': portfolio_returns_by_state.tolist()
}
```

**Common Bugs to Avoid:**
- Computing expected returns for individual securities first, then combining (wrong for variance)
- Forgetting to calculate portfolio return separately for each state
- Using individual security variances and covariance formula when state-by-state data is available
- Not squaring deviations when calculating variance
- Confusing variance with standard deviation in final answer

---

## Pattern: Tax_Lot_Accounting_Method_Implementation

**Description:** Tax lot accounting (FIFO, LIFO, HIFO) requires identifying which specific shares are sold based on cost basis ordering rules, then calculating gains/losses and tax liability for those specific lots considering holding period and applicable tax rates.

**When to Use:** Problems involving sale of securities with multiple purchase lots at different prices/dates, tax loss harvesting, or tax-efficient portfolio management.

**Procedure:**
1. Extract all tax lots: purchase date, shares, cost per share, holding period classification
2. Determine applicable tax rates (long-term vs short-term based on holding period)
3. Apply accounting method to select which lots to sell:
   - FIFO: oldest lots first
   - LIFO: newest lots first  
   - HIFO: highest cost basis first (most tax-efficient for gains)
4. For selected lots: proceeds = shares × sale_price, cost_basis = shares × purchase_price
5. Calculate gain/loss = proceeds - cost_basis for each lot
6. Calculate tax = gain × applicable_tax_rate (negative for losses = tax benefit)
7. Sum across all lots sold

**Code Example:**

**Scenario:** Sell 150 shares using HIFO method, 3 available lots with different costs and holding periods

**Correct Code:**
```python
from datetime import datetime

# Step 1: Define tax lots with all required attributes
tax_lots = [
    {'lot_id': 'A', 'purchase_date': '2022-01-15', 'shares': 100, 
     'cost_per_share': 95, 'holding_period': 'long-term'},
    {'lot_id': 'B', 'purchase_date': '2023-03-20', 'shares': 80, 
     'cost_per_share': 110, 'holding_period': 'short-term'},
    {'lot_id': 'C', 'purchase_date': '2023-06-10', 'shares': 120, 
     'cost_per_share': 105, 'holding_period': 'short-term'}
]

# Sale parameters
sale_date = '2023-08-23'
sale_price = 98
shares_to_sell = 150

# Tax rates
tax_rate_long_term = 0.20
tax_rate_short_term = 0.35

# Step 2: Sort lots by cost per share (HIFO = highest first)
sorted_lots = sorted(tax_lots, key=lambda x: x['cost_per_share'], reverse=True)

# Step 3: Select lots to sell using HIFO
lots_to_sell = []
shares_remaining = shares_to_sell

for lot in sorted_lots:
    if shares_remaining <= 0:
        break
    
    shares_from_lot = min(lot['shares'], shares_remaining)
    lots_to_sell.append({
        'lot_id': lot['lot_id'],
        'shares': shares_from_lot,
        'cost_per_share': lot['cost_per_share'],
        'holding_period': lot['holding_period']
    })
    shares_remaining -= shares_from_lot

# Step 4: Calculate tax liability for each lot sold
total_tax_liability = 0

for lot_sold in lots_to_sell:
    # Calculate proceeds and cost basis
    proceeds = lot_sold['shares'] * sale_price
    cost_basis = lot_sold['shares'] * lot_sold['cost_per_share']
    
    # Calculate gain/loss
    gain_loss = proceeds - cost_basis
    
    # Determine applicable tax rate
    tax_rate = (tax_rate_long_term if lot_sold['holding_period'] == 'long-term' 
                else tax_rate_short_term)
    
    # Calculate tax (negative for losses = tax benefit)
    tax = gain_loss * tax_rate
    total_tax_liability += tax

# Step 5: Return result (negative = tax benefit)
{
    'lots_sold': lots_to_sell,
    'total_tax_liability': round(total_tax_liability, 2),
    'interpretation': 'Tax benefit' if total_tax_liability < 0 else 'Tax liability'
}
```

**Common Bugs to Avoid:**
- Not sorting lots correctly for the specified accounting method (HIFO requires descending cost)
- Forgetting to apply different tax rates for long-term vs short-term holdings
- Calculating tax on proceeds instead of gain/loss
- Not recognizing that losses create tax benefits (negative tax liability)
- Selling more shares than available in selected lots
- Fabricating lot data instead of extracting from provided exhibits

---

## Pattern: Covariance_and_Correlation_from_State_Returns

**Description:** When computing portfolio variance or correlation between securities using state-based returns, must use the probability-weighted covariance formula, not assume independence. Correlation requires both covariance and individual standard deviations.

**When to Use:** Problems asking for correlation, portfolio variance with multiple securities, or diversification analysis when state-by-state returns are provided.

**Procedure:**
1. Formula: Cov(X,Y) = Σ p_i × (R_X,i - E[R_X]) × (R_Y,i - E[R_Y])
2. Formula: Corr(X,Y) = Cov(X,Y) / (σ_X × σ_Y)
3. Calculate expected returns for both securities: E[R] = Σ p_i × R_i
4. Calculate standard deviations: σ = sqrt(Σ p_i × (R_i - E[R])²)
5. Calculate covariance using probability-weighted cross-products of deviations
6. Divide covariance by product of standard deviations to get correlation
7. Validate: correlation must be between -1 and +1

**Code Example:**

**Scenario:** Calculate correlation between Security_M and Security_N across 4 states

**Correct Code:**
```python
import numpy as np

# Step 1: Extract state-based data
states = ['State_1', 'State_2', 'State_3', 'State_4']
probabilities = np.array([0.20, 0.30, 0.35, 0.15])

returns_m = np.array([0.15, 0.10, 0.08, 0.05])
returns_n = np.array([0.12, 0.14, 0.09, 0.18])

# Step 2: Calculate expected returns
expected_return_m = np.sum(probabilities * returns_m)
expected_return_n = np.sum(probabilities * returns_n)

# Step 3: Calculate deviations from expected returns
deviations_m = returns_m - expected_return_m
deviations_n = returns_n - expected_return_n

# Step 4: Calculate variances
variance_m = np.sum(probabilities * deviations_m**2)
variance_n = np.sum(probabilities * deviations_n**2)

# Step 5: Calculate standard deviations
std_dev_m = np.sqrt(variance_m)
std_dev_n = np.sqrt(variance_n)

# Step 6: Calculate covariance
# Cov(M,N) = Σ p_i * (R_M,i - E[R_M]) * (R_N,i - E[R_N])
covariance_mn = np.sum(probabilities * deviations_m * deviations_n)

# Step 7: Calculate correlation
correlation_mn = covariance_mn / (std_dev_m * std_dev_n)

# Step 8: Validate result
assert -1.0 <= correlation_mn <= 1.0, f"Invalid correlation: {correlation_mn}"

# Return as expression
{
    'expected_return_m': round(expected_return_m, 4),
    'expected_return_n': round(expected_return_n, 4),
    'std_dev_m': round(std_dev_m, 4),
    'std_dev_n': round(std_dev_n, 4),
    'covariance': round(covariance_mn, 6),
    'correlation': round(correlation_mn, 4)
}
```

**Common Bugs to Avoid:**
- Assuming securities are uncorrelated (covariance = 0) when state data is available
- Using wrong formula for covariance (not probability-weighted)
- Forgetting to calculate deviations from expected returns before multiplying
- Dividing by wrong denominator for correlation (must be product of both std devs)
- Not validating that correlation is in valid range [-1, 1]
- Confusing covariance with correlation in final answer

---

## Pattern: CAPM_Alpha_and_Residual_Risk_Calculation

**Description:** When computing alpha (excess return) and residual variance for securities, must use CAPM to determine required return, then calculate alpha as difference between expected and required return. Residual variance is the squared firm-specific standard deviation, independent of beta.

**When to Use:** Problems involving security analysis, portfolio optimization, or performance evaluation with market benchmarks and beta estimates.

**Procedure:**
1. Formula: Required Return = R_f + β × (R_m - R_f)
2. Formula: Alpha = Expected Return - Required Return
3. Formula: Residual Variance = (Firm-Specific Std Dev)²
4. Extract: risk-free rate, market return, beta, expected return, residual std dev
5. Calculate market risk premium = market return - risk-free rate
6. Calculate required return using CAPM
7. Calculate alpha as difference
8. Calculate residual variance by squaring residual std dev

**Code Example:**

**Scenario:** Calculate alpha and residual variance for 3 securities given market parameters

**Correct Code:**
```python
import pandas as pd

# Step 1: Extract market parameters
risk_free_rate = 0.05  # 5%
market_return = 0.12   # 12%
market_std_dev = 0.18  # Not needed for alpha, but often provided

# Step 2: Extract security-specific data
securities = {
    'Security_X': {'expected_return': 0.14, 'beta': 1.2, 'residual_std': 0.25},
    'Security_Y': {'expected_return': 0.10, 'beta': 0.8, 'residual_std': 0.30},
    'Security_Z': {'expected_return': 0.16, 'beta': 1.5, 'residual_std': 0.22}
}

# Step 3: Calculate market risk premium
market_risk_premium = market_return - risk_free_rate

# Step 4: Calculate required return, alpha, and residual variance for each security
results = []

for sec_name, sec_data in securities.items():
    # CAPM required return
    required_return = risk_free_rate + sec_data['beta'] * market_risk_premium
    
    # Alpha (excess return over CAPM prediction)
    alpha = sec_data['expected_return'] - required_return
    
    # Residual variance (firm-specific risk squared)
    residual_variance = sec_data['residual_std'] ** 2
    
    results.append({
        'Security': sec_name,
        'Expected_Return': sec_data['expected_return'],
        'Beta': sec_data['beta'],
        'Required_Return': round(required_return, 4),
        'Alpha': round(alpha, 4),
        'Residual_Std': sec_data['residual_std'],
        'Residual_Variance': round(residual_variance, 4)
    })

# Step 5: Create results DataFrame
df_results = pd.DataFrame(results)

# Return as expression
df_results.to_dict('records')
```

**Common Bugs to Avoid:**
- Using expected return instead of required return in alpha calculation
- Forgetting to calculate market risk premium before applying CAPM
- Confusing residual standard deviation with residual variance (must square)
- Using total variance instead of firm-specific (residual) variance
- Not recognizing that residual risk is independent of beta/market risk
- Mixing up which securities have positive vs negative alpha

---

## Pattern: Multi_Column_Table_Parsing_with_Spatial_Awareness

**Description:** When OCR text presents tables with multiple columns, the model must systematically identify column headers, count expected columns per row, and validate that extracted values align with the correct column before using them in calculations. Common errors include swapping columns (e.g., Stock A ↔ Stock B, Market ↔ Portfolio) or misaligning header-to-data mappings.

**When to Use:** Any problem with tabular data from images containing 2+ columns representing different entities (stocks, portfolios, projects) where each row contains corresponding values across columns. Trigger keywords: "Stock A", "Stock B", "Market", "Portfolio", "Project I", "Project II", state-based returns, performance metrics.

**Procedure:**
1. **Parse header row:** Extract all column headers and count expected columns (e.g., ["State", "Stock A", "Stock B"] = 3 columns)
2. **Validate row structure:** For each data row, verify token count matches header count
3. **Create column-to-index mapping:** Build explicit dictionary mapping column names to positions (e.g., {"Stock A": 1, "Stock B": 2})
4. **Extract with validation:** When extracting values, always reference by column name through mapping, never by assumed position
5. **Cross-check reasonableness:** Verify extracted values against question context (e.g., if question asks for "Stock B", confirm you're using column index for Stock B)
6. **Return result:** Use extracted values in calculations with clear variable names indicating source column

**Code Example:**

**Scenario:** Table shows returns for two funds (Alpha Fund and Beta Fund) across three economic states with probabilities.

**Correct Code:**
```python
# OCR text: "State Probability Alpha Beta\nBoom 0.3 0.15 0.22\nNormal 0.5 0.08 0.10\nBust 0.2 -0.02 -0.05"

# Step 1: Parse header and establish column mapping
ocr_lines = [
    "State Probability Alpha Beta",
    "Boom 0.3 0.15 0.22",
    "Normal 0.5 0.08 0.10",
    "Bust 0.2 -0.02 -0.05"
]

header = ocr_lines[0].split()
# header = ['State', 'Probability', 'Alpha', 'Beta']

# Step 2: Create explicit column index mapping
col_map = {name: idx for idx, name in enumerate(header)}
# col_map = {'State': 0, 'Probability': 1, 'Alpha': 2, 'Beta': 3}

# Step 3: Parse data rows with validation
data_rows = []
for line in ocr_lines[1:]:
    tokens = line.split()
    if len(tokens) != len(header):
        raise ValueError(f"Row has {len(tokens)} tokens, expected {len(header)}")
    data_rows.append(tokens)

# Step 4: Extract values using column mapping (NOT hardcoded indices)
# Question asks for expected return of Beta Fund
beta_returns = []
probabilities = []

for row in data_rows:
    prob = float(row[col_map['Probability']])
    beta_ret = float(row[col_map['Beta']])  # Explicitly use 'Beta' column
    probabilities.append(prob)
    beta_returns.append(beta_ret)

# Step 5: Calculate expected return
expected_return_beta = sum(p * r for p, r in zip(probabilities, beta_returns))

# Step 6: Return result
expected_return_beta  # 0.108 or 10.8%
```

**Common Bugs to Avoid:**
- **Hardcoded column indices:** Using `row[2]` instead of `row[col_map['Alpha']]` leads to column swaps when OCR order differs from assumption
- **Assuming column order:** Never assume "first column after probability is Stock A" without verifying header
- **Ignoring header validation:** Not checking if header contains expected column names before extraction
- **Cross-column contamination:** Extracting Stock A values when question asks for Stock B due to off-by-one indexing
- **Missing row length validation:** Not verifying each row has same number of tokens as header, causing misalignment
- **Ambiguous variable names:** Using `return_1` and `return_2` instead of `return_alpha` and `return_beta` makes debugging harder

---

## Pattern: OCR_Table_Dash_and_Missing_Value_Interpretation

**Description:** OCR tables may use dashes ('-'), blank cells, or placeholder symbols to indicate missing values that need to be solved for, rather than representing negative signs, zero values, or row labels. Code must distinguish between formatting dashes and actual data before constructing cash flow arrays or data structures.

**When to Use:** Problems involving cash flow tables, time series data, or structured tables where one or more values are unknown and must be calculated. Trigger keywords: "missing cash flow", "find the value", "what is X", tables with dashes or gaps in data cells.

**Procedure:**
1. **Identify table structure:** Parse all rows and columns, noting positions of dashes, blanks, or unusual symbols
2. **Contextualize dashes:** Check if dash appears in a data cell (likely missing value) vs. as a negative sign prefix (e.g., "-$1,500")
3. **Map known vs unknown:** Create separate data structures for known values and placeholder for unknown
4. **Validate against question:** Confirm which value the question asks to solve for matches the identified missing position
5. **Set up equation:** Use present value, NPV, or other relevant formula with unknown as variable
6. **Solve algebraically:** Rearrange equation to isolate unknown value
7. **Return result:** Output the calculated missing value

**Code Example:**

**Scenario:** Present value of cash flows is $5,000 at 8% discount rate. Year 1: $800, Year 2: unknown, Year 3: $1,200.

**Correct Code:**
```python
# OCR text shows: "Year 1: $800, Year 2: -, Year 3: $1,200"
# The dash in Year 2 indicates missing value, NOT negative or zero

# Step 1: Parse and identify missing value position
pv_total = 5000
discount_rate = 0.08

cash_flows = {
    1: 800,
    2: None,  # Dash indicates unknown, not zero or negative
    3: 1200
}

# Step 2: Calculate PV of known cash flows
pv_known = 0
for year, cf in cash_flows.items():
    if cf is not None:
        pv_known += cf / (1 + discount_rate) ** year

# pv_known = 800/1.08 + 1200/1.08^3 = 740.74 + 952.54 = 1693.28

# Step 3: PV of unknown cash flow must equal difference
pv_year_2_needed = pv_total - pv_known

# Step 4: Solve for Year 2 cash flow
# pv_year_2_needed = CF2 / (1 + r)^2
# CF2 = pv_year_2_needed * (1 + r)^2
cf_year_2 = pv_year_2_needed * (1 + discount_rate) ** 2

# Step 5: Return result
cf_year_2  # 3857.49
```

**Common Bugs to Avoid:**
- **Treating dash as negative sign:** Interpreting "-" in data cell as negative value instead of missing placeholder
- **Treating dash as zero:** Assuming missing value is zero and proceeding with calculation
- **Treating dash as year label:** Confusing formatting dash with row identifier, causing year misalignment
- **Not validating solution:** Failing to verify that calculated value produces correct total when substituted back
- **Hardcoding missing position:** Assuming Year 2 is always missing instead of programmatically detecting None/null values

---

## Pattern: Context_Driven_Cash_Flow_Sign_Convention

**Description:** When cash flow tables are presented with context like "payments you must make" or "costs incurred," all values in the table represent outflows (negative) even if not explicitly marked with minus signs. Code must interpret table values based on surrounding narrative context, not just the numeric formatting in the OCR output. **However, when the question asks about current stock price or equity value that already incorporates future cash flows, do not adjust for those cash flows again.**

**When to Use:** NPV, IRR, or cash flow analysis problems where the question text describes the nature of cash flows (e.g., "payments," "costs," "investments required") before presenting a table. Trigger keywords: "must make the following payments", "costs are", "investments required", "cash outflows".

**When NOT to Use:**
- When the question asks for current value that already reflects future cash flows (e.g., "stock price today" when dividends are already reflected in balance sheet equity)
- When cash flows are already explicitly signed in the OCR output
- When dealing with market values that incorporate all future cash flows by definition

**Procedure:**
1. **Parse question context:** Identify phrases describing cash flow nature (inflows vs outflows)
2. **Determine if adjustment is needed:** Check if the question asks for a value that already incorporates the cash flows (e.g., current stock price with dividend in equity) vs. a value that needs cash flow adjustment (e.g., NPV calculation)
3. Identify initial cash flow: Determine if Year 0 is an inflow (loan/offer received) or outflow (investment made)
4. Apply sign convention: If context says "payments you must make," all subsequent values are negative regardless of OCR formatting
5. Validate against answer options: Check if sign convention produces reasonable NPV/IRR compared to expected range
6. Construct cash flow array: Build array with correct signs based on context interpretation
7. Calculate metric: Compute NPV, IRR, or other metric using properly signed cash flows
8. Return result: Output calculated value

**Common Mistakes to Avoid:**
- Adjusting for future cash flows when calculating current value that already incorporates them (e.g., subtracting future dividends from current equity value when equity already reflects the dividend obligation)
- Double-counting cash flows by both including them in current value and adjusting for them separately
- Not recognizing when a balance sheet value already represents the net present value of all future cash flows

**Example (sanitized):**
> **Scenario:** Company equity is $500K, will pay $20K dividend tomorrow. Question asks: "What is the stock price today?"
> **Wrong approach:** Calculate price as (Equity - Dividend) / Shares, then add back dividend per share
> **Correct approach:** Current equity of $500K already includes the cash earmarked for dividends. Stock price today = Equity / Shares. After dividend payment tomorrow, equity will be $480K and stock price will drop by dividend per share.
## Pattern: Missing_Parameter_Detection_in_Formula_Based_Problems

**Description:** When applying formulas requiring multiple inputs (e.g., Black-Scholes, CAPM, Sharpe ratio), code must verify ALL required parameters are explicitly provided in the visual evidence before proceeding. If any parameter is missing from images/tables, code must halt with clear error message rather than assuming default values, as assumptions can lead to dramatically wrong answers.

**When to Use:** Problems involving standard finance formulas (option pricing, performance metrics, portfolio theory) where parameters come from images/tables. Trigger keywords: "given the following information", "using the data in the table", formulas with 3+ required inputs.

**Procedure:**
1. **List required parameters:** Identify all inputs needed for the formula (e.g., Black-Scholes needs S, K, T, σ, r)
2. **Parse visual evidence:** Extract all values explicitly shown in OCR text from images
3. **Map parameters to sources:** Create dictionary linking each required parameter to its source in visual evidence
4. **Detect missing values:** Check if any required parameter has no source in provided data
5. **Halt if incomplete:** If missing parameters detected, raise error with message listing what's missing and where it should be
6. **Validate extracted values:** Cross-check extracted values against expected ranges (e.g., volatility 0-200%, rates 0-30%)
7. **Calculate only if complete:** Proceed with formula only after confirming all parameters sourced from evidence

**Code Example:**

**Scenario:** Calculate Black-Scholes put value. Table shows: Stock price $50, Strike $48, Volatility 35%, Time 3 months. Risk-free rate not provided.

**Correct Code:**
```python
# OCR text: "Stock price: $50, Strike: $48, Volatility: 35%, Time: 3 months"

# Step 1: Define required parameters for Black-Scholes
required_params = ['S', 'K', 'sigma', 'T', 'r']

# Step 2: Parse visual evidence
extracted_data = {
    'S': 50,        # Stock price from table
    'K': 48,        # Strike from table
    'sigma': 0.35,  # Volatility from table
    'T': 0.25,      # Time from table (3 months = 0.25 years)
    'r': None       # Risk-free rate NOT in table
}

# Step 3: Detect missing parameters
missing_params = [param for param in required_params if extracted_data.get(param) is None]

# Step 4: Halt if any parameter missing
if missing_params:
    raise ValueError(
        f"Cannot calculate Black-Scholes value. Missing parameters: {missing_params}. "
        f"These must be provided in the image/table. Do not assume default values."
    )

# Step 5: Only proceed if all parameters present
# (This code won't execute due to missing 'r')
import math
from scipy.stats import norm

S = extracted_data['S']
K = extracted_data['K']
sigma = extracted_data['sigma']
T = extracted_data['T']
r = extracted_data['r']

d1 = (math.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*math.sqrt(T))
d2 = d1 - sigma*math.sqrt(T)
put_value = K*math.exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)

put_value
```

**Common Bugs to Avoid:**
- **Assuming default values:** Using r=0.05 or other "standard" values when parameter not in visual evidence
- **Proceeding with None values:** Allowing calculation to continue with missing parameters, causing runtime errors
- **Not documenting assumptions:** If making assumption, must explicitly state it and explain why (but better to halt)
- **Ignoring validation:** Not checking if extracted values are in reasonable ranges for their parameter type
- **Silent substitution:** Replacing missing values without error message, making debugging impossible
- **Incomplete parameter lists:** Forgetting to check all required inputs before calculation

---

## Pattern: OCR_Percentage_Format_Ambiguity_Resolution

**Description:** OCR may misread percentage values in tables, producing ambiguous formats like "%9" (should be -9%), "9%" vs "60%" (OCR confusion between digits), or missing decimal points. When calculated results don't match any answer option, code must re-examine OCR output for likely percentage misreads and test alternative interpretations.

**When to Use:** Problems with percentage-based tables (returns, probabilities, rates) where initial calculation produces result not matching any answer option, or where OCR shows unusual percentage formatting. Trigger keywords: percentage returns, probability distributions, answer options provided, calculated result doesn't match options.

**Procedure:**
1. **Calculate with initial OCR values:** Perform calculation using values as extracted
2. **Compare to answer options:** Check if result matches any provided option within rounding tolerance
3. **If no match, identify suspects:** Look for OCR values that could be misreads (e.g., "%9" at end of row, single-digit percentages in high-volatility context)
4. **Test alternative interpretations:** Try common OCR errors (9 ↔ -9, 9 ↔ 6, missing decimal point)
5. **Recalculate with alternatives:** Compute result with each alternative interpretation
6. **Select matching interpretation:** Choose interpretation that produces result matching an answer option
7. **Return result with note:** Output answer and document which OCR correction was applied

**Code Example:**

**Scenario:** Expected return calculation. OCR shows returns: Boom 18%, Normal 12%, Recession %9. Probabilities: 0.3, 0.5, 0.2. Answer options: 10.4%, 11.6%, 13.2%.

**Correct Code:**
```python
# OCR text: "Boom 18%, Normal 12%, Recession %9"
# Note: "%9" is unusual formatting - likely OCR error

# Step 1: Parse initial OCR values
probabilities = [0.3, 0.5, 0.2]
returns_initial = [0.18, 0.12, 0.09]  # Interpreting "%9" as 9%

# Step 2: Calculate with initial interpretation
expected_return_initial = sum(p * r for p, r in zip(probabilities, returns_initial))
# Result: 0.123 or 12.3%

# Step 3: Check against answer options
answer_options = [0.104, 0.116, 0.132]
tolerance = 0.002

matches_initial = any(abs(expected_return_initial - opt) < tolerance for opt in answer_options)
# matches_initial = False (12.3% doesn't match any option)

# Step 4: Identify OCR suspect - "%9" is unusual, could be "-9%"
# Test alternative: Recession return is -9% instead of 9%
returns_alternative = [0.18, 0.12, -0.09]

# Step 5: Recalculate with alternative
expected_return_alternative = sum(p * r for p, r in zip(probabilities, returns_alternative))
# Result: 0.104 or 10.4%

# Step 6: Verify match
matches_alternative = any(abs(expected_return_alternative - opt) < tolerance for opt in answer_options)
# matches_alternative = True (matches option 10.4%)

# Step 7: Return corrected result
# Note: OCR "%9" interpreted as -9% based on answer option validation
expected_return_alternative  # 0.104 or 10.4%
```

**Common Bugs to Avoid:**
- **Accepting non-matching results:** Proceeding with answer that doesn't match any option without investigating OCR errors
- **Not testing negative interpretation:** Failing to consider that "%9" or "9" might represent -9% in financial contexts
- **Ignoring answer options:** Not using provided options as validation check for OCR accuracy
- **Random guessing:** Trying arbitrary corrections instead of systematic testing of common OCR errors
- **Not documenting correction:** Returning result without noting which OCR value was reinterpreted
- **Over-correcting:** Changing multiple values when only one is likely misread

## Pattern: Binomial_Tree_Expected_Life_Calculation_for_ESO

**Description:** Employee stock option (ESO) valuation requires computing expected life as a probability-weighted average of all possible exercise times across a binomial tree, accounting for vesting constraints, voluntary exercise probabilities at each node, involuntary exercise due to employee turnover, and final maturity. Cannot be arbitrarily assumed or simplified.

**When to Use:** Problems involving employee stock option valuation with binomial trees showing multiple exercise nodes, vesting periods, employee turnover rates, and voluntary exercise probabilities. Trigger keywords: "expected life", "employee stock option", "vesting", "turnover", "exercise probability", "binomial tree", nodes with exercise decisions.

**Procedure:**
1. Formula: Expected_Life = Σ(probability_of_reaching_time_t × probability_of_exercising_at_t × t) for all possible exercise times t
2. Identify all nodes in the binomial tree where exercise is possible (post-vesting, in-the-money nodes)
3. For each exercise node, calculate the probability of reaching that node (product of branch probabilities along the path)
4. At each node, calculate total exercise probability = voluntary_exercise_prob + (1 - voluntary_exercise_prob) × turnover_rate
5. Calculate probability-weighted time for each exercise scenario
6. Sum across all paths to get expected life, including paths that reach maturity without early exercise
7. Use this expected life in Black-Scholes-Merton formula

**Code Example:**

**Scenario:** A 6-year ESO vests after 2 years. Binomial tree has 3 time steps (t=0, 2, 4, 6 years). At year 4 node (in-the-money), 50% voluntary exercise probability. At year 6 node, 70% voluntary exercise probability. Employee turnover is 3% per step. Up probability is 0.55.

**Correct Code:**
```python
import math

# Tree parameters
T_total = 6  # Total option life
T_vesting = 2  # Vesting period
dt = 2  # Time step
p_up = 0.55  # Probability of up move
p_down = 0.45  # Probability of down move
turnover_per_step = 0.03  # Employee turnover rate

# Exercise probabilities at specific nodes (conditional on reaching node)
exercise_prob_year4 = 0.50  # Voluntary exercise at year 4 node
exercise_prob_year6 = 0.70  # Voluntary exercise at year 6 node

# Calculate expected life by tracking all paths
expected_life = 0.0

# Path 1: Reach year 4 node (up move), exercise there
prob_reach_year4 = p_up  # Probability of reaching the up node at year 4
total_exercise_year4 = exercise_prob_year4 + (1 - exercise_prob_year4) * turnover_per_step
prob_exercise_year4 = prob_reach_year4 * total_exercise_year4
expected_life += prob_exercise_year4 * 4

# Path 2: Reach year 4, don't exercise, continue to year 6 and exercise
prob_continue_from_year4 = prob_reach_year4 * (1 - total_exercise_year4) * (1 - turnover_per_step)
prob_reach_year6_via_year4 = prob_continue_from_year4 * p_up  # Another up move
total_exercise_year6 = exercise_prob_year6 + (1 - exercise_prob_year6) * turnover_per_step
prob_exercise_year6 = prob_reach_year6_via_year4 * total_exercise_year6
expected_life += prob_exercise_year6 * 6

# Path 3: Other paths that reach maturity (simplified for illustration)
# In practice, enumerate all paths through the tree
prob_reach_maturity = 1 - prob_exercise_year4 - prob_exercise_year6  # Remaining probability
expected_life += prob_reach_maturity * 6

# Now use expected life in Black-Scholes
S = 50  # Stock price
K = 50  # Strike price
r = 0.04  # Risk-free rate
sigma = 0.25  # Volatility

d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * expected_life) / (sigma * math.sqrt(expected_life))
d2 = d1 - sigma * math.sqrt(expected_life)
N_d1 = 0.5 * (1 + math.erf(d1 / math.sqrt(2)))
N_d2 = 0.5 * (1 + math.erf(d2 / math.sqrt(2)))
option_value = S * N_d1 - K * math.exp(-r * expected_life) * N_d2

option_value
```

**Common Bugs to Avoid:**
- Arbitrarily assuming expected life (e.g., setting it to 5 years without calculation)
- Ignoring turnover when calculating exercise probability (must add involuntary exercise component)
- Forgetting to weight by path probabilities (must multiply by probability of reaching each node)
- Not accounting for vesting period (cannot exercise before vesting)
- Computing expected life as simple average of node times instead of probability-weighted average
- Missing the compound probability calculation (probability of reaching node × probability of exercising at node)

---

## Pattern: Demonstrative_Reference_Disambiguation_in_Multi_Table_Context

**Description:** When questions use demonstrative references ("this call", "that option", "the bond") in contexts with multiple similar items across multiple tables/images, code must systematically identify which specific item is referenced by examining contextual clues (table proximity, answer option ranges, parameter consistency) rather than defaulting to the first matching item.

**When to Use:** Problems presenting multiple tables/images with similar financial instruments (multiple options with same strike, multiple bonds, multiple stocks) where the question uses demonstrative pronouns without explicit specification. Trigger keywords: "this call", "that put", "the option", "this bond", multiple tables with overlapping parameters.

**Procedure:**
1. Identify all items matching the basic criteria (e.g., all calls with K=85)
2. Check if answer options provide range clues (e.g., options 0.24-1.12 suggest lower volatility, not higher)
3. Compare with reference values mentioned in problem (e.g., "historical volatility is 30%" suggests answer near 0.30)
4. Consider table ordering and proximity to question text (later tables may be the focus)
5. Test calculation with each candidate item and select the one whose result aligns with answer option ranges
6. Document which specific item was selected and why

**Code Example:**

**Scenario:** Two tables show call options. Table 1 has 1-month calls with market price $3.50. Table 2 has 1-year calls with market price $8.50. Question asks "What is the implied volatility of this call?" Historical volatility is 28%. Answer options are A. 0.25, B. 0.29, C. 0.35, D. 0.45.

**Correct Code:**
```python
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.stats import norm

def black_scholes_call(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)

def find_implied_vol(S, K, T, r, market_price):
    def objective(sigma):
        return (black_scholes_call(S, K, T, r, sigma) - market_price)**2
    result = minimize_scalar(objective, bounds=(0.01, 1.0), method='bounded')
    return result.x

# Given parameters
S = 100
K = 100
r = 0.05
historical_vol = 0.28

# Candidate 1: 1-month call from Table 1
T1 = 1/12
market_price_1 = 3.50
implied_vol_1 = find_implied_vol(S, K, T1, r, market_price_1)

# Candidate 2: 1-year call from Table 2
T2 = 1.0
market_price_2 = 8.50
implied_vol_2 = find_implied_vol(S, K, T2, r, market_price_2)

# Disambiguation logic: check which result aligns with answer options and context
# Answer options range 0.25-0.45, historical vol is 0.28
# Candidate closer to historical vol and within option range is likely correct

if abs(implied_vol_2 - historical_vol) < abs(implied_vol_1 - historical_vol):
    selected_vol = implied_vol_2
    selected_option = "1-year call from Table 2"
else:
    selected_vol = implied_vol_1
    selected_option = "1-month call from Table 1"

# Return the disambiguated result
selected_vol
```

**Common Bugs to Avoid:**
- Defaulting to the first matching item without checking alternatives
- Ignoring answer option ranges as disambiguation clues
- Not comparing calculated results against reference values (historical volatility, benchmark rates)
- Failing to document which specific item was selected when multiple candidates exist
- Not testing all candidate items when the question is ambiguous
- Assuming table order implies question focus (later tables may be more relevant)

---

## Pattern: Balance_Sheet_Equation_Validation_Before_Ratio_Analysis

**Description:** Before computing financial ratios from balance sheet data, code must validate that Assets = Liabilities + Equity for each period. When the equation doesn't balance or calculated ratios deviate significantly from answer options, this signals OCR errors, transcription mistakes, or data misalignment requiring correction before proceeding with ratio calculations. **Critical: Ensure each balance sheet item is classified into exactly one category to avoid double-counting. Use item names and contextual clues to determine correct classification, not just position in OCR output.**

**When to Use:** Problems involving balance sheet ratio analysis (market-to-book, debt-to-equity, current ratio) where OCR provides balance sheet data, **especially when multiple items could be ambiguously classified**.

**When NOT to Use:**
- When balance sheet data is clearly presented with unambiguous categories
- When the question doesn't involve balance sheet analysis

**Procedure:**
1. Formula: Assets = Liabilities + Equity (fundamental accounting equation)
2. **Parse OCR carefully to identify item names and their associated values/durations**
3. **Classify each item based on its NAME and financial context, not just OCR position:**
   - Assets: receivables, loans made, cash, securities owned, property
   - Liabilities: deposits from customers, borrowings, debt obligations
   - Equity: capital, retained earnings, shareholders' equity
4. **Verify each item appears in exactly one category** - check that no item is counted as both an asset and a liability
5. Extract total assets, total liabilities, and total equity for each period
6. Verify Assets = Liabilities + Equity for each period (allow small rounding differences < 0.1%)
7. If equation doesn't balance, identify which component is likely incorrect (check for OCR errors in subtotals **or misclassification of items**)
8. Cross-check with prior period values for reasonableness
9. After validation/correction, proceed with ratio calculation
10. If calculated ratio doesn't match any answer option, re-examine balance sheet components for misreads **or misclassifications**

**Common Mistakes to Avoid:**
- Classifying the same item as both an asset and a liability (e.g., "Federal funds deposits" appearing in both categories)
- Not verifying the balance sheet equation before calculating ratios
- Ignoring large discrepancies that indicate classification errors rather than OCR errors
- Proceeding with ratio calculations when the balance sheet doesn't balance
- **Classifying items based solely on OCR position rather than item name and financial context**
- **Assuming "deposits" are always liabilities without checking if they're deposits made BY the bank (asset) or deposits FROM customers (liability)**

**Example (sanitized):**
> **Scenario:** Bank balance sheet shows: "Federal funds deposits $31M duration 0", "Checking deposits $615M duration 0". Question asks for liability duration.
> **Wrong approach:** Include both items as liabilities because they both contain "deposits"
> **Correct approach:** "Federal funds deposits" = deposits the bank made to other banks (ASSET). "Checking deposits" = customer deposits (LIABILITY). Classify based on financial context, not just keyword matching.
## Pattern: Monte_Carlo_Percentile_Interpretation_for_Goal_Probability

**Description:** When Monte Carlo simulation results are presented as percentile outcomes (25th, 50th, 75th percentile portfolio values), the probability of achieving a goal must be interpreted correctly: the Xth percentile means X% of outcomes fall **below** that value, so (100-X)% fall above it. To find the probability of meeting a goal, identify which percentile bracket the goal falls into and calculate the corresponding success probability. **Critical: Do not reorder or "correct" percentile values based on assumed logical ordering - Monte Carlo results may show non-monotonic patterns due to sampling variation or specific risk scenarios.**

**When to Use:** Problems involving Monte Carlo simulation results presented as percentile outcomes (e.g., 25th, 50th, 75th percentile values) where the question asks for the probability of achieving a specific financial goal or target value.

**When NOT to Use:**
- When simulation results are presented as direct probabilities rather than percentiles
- When the question asks for expected values rather than probability of success
- When dealing with confidence intervals rather than percentile outcomes

**Procedure:**
1. Extract the goal/target value from the question (e.g., "gift $1 million in 15 years")
2. Extract the relevant time period's percentile outcomes from the simulation results **as provided in OCR without reordering**
3. **Accept OCR percentile values as-is** - Monte Carlo simulations can produce non-monotonic percentile patterns due to sampling variation, specific risk scenarios, or distribution characteristics
4. **Correctly interpret percentiles**: The Xth percentile means X% of outcomes are ≤ that value, and (100-X)% are > that value
5. Compare the goal value to each percentile outcome to determine which bracket it falls into
6. Calculate probability of success:
   - If goal < 25th percentile value: probability > 75% (more than 75% of outcomes exceed the goal)
   - If 25th percentile < goal < 50th percentile: probability is between 50% and 75%
   - If 50th percentile < goal < 75th percentile: probability is between 25% and 50%
   - If goal > 75th percentile value: probability < 25%
7. For precise probability, interpolate between percentiles if needed
8. Return the probability that matches the answer options

**Common Mistakes to Avoid:**
- **Reversed percentile interpretation**: Thinking "75th percentile means 75% of outcomes are above this value" (WRONG - it means 75% are below, 25% are above)
- Confusing percentile rank with probability of success
- Not checking which percentile bracket the goal falls into before calculating probability
- Returning the percentile value itself instead of the corresponding probability
- **Reordering percentile values based on assumed monotonicity (e.g., assuming 25th < 50th < 75th must always hold) when OCR shows different ordering**
- **"Correcting" OCR percentile values without considering that Monte Carlo results can legitimately show non-standard ordering patterns**

**Example (sanitized):**
> **Scenario:** Monte Carlo simulation shows: 25th percentile = $950K, 50th percentile = $850K, 75th percentile = $1,020K. Goal: $1,000K.
> **Wrong approach:** "Reorder to 25th=$850K, 50th=$950K, 75th=$1,020K because percentiles must be monotonic"
> **Correct approach:** Use OCR values as-is. Goal ($1,000K) falls between 50th ($850K) and 75th ($1,020K), so probability of success is between 25% and 50%. The non-monotonic pattern may reflect specific risk scenarios in the simulation.

---