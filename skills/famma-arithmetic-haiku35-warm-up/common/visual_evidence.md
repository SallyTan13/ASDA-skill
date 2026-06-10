# SKILL PATTERNS FOR VISUAL EVIDENCE AND TABLE PARSING IN FINANCIAL CALCULATIONS

## Pattern: Table Structure Parsing and Row-Column Alignment

**Description:** When extracting data from tables presented via OCR, correctly identify header rows, map ordinal positions (e.g., "first row", "third row") to actual data rows, maintain proper column-to-value alignment, and handle non-standard formatting (e.g., '%9' instead of '9%') to avoid extracting values from wrong cells or misinterpreting malformed data.

**When to Use:** Questions referencing specific rows/columns in tables (e.g., "Find the APR for the second row"), questions asking for values under specific column headers (e.g., "Moderate Growth"), or when OCR text contains formatting anomalies like reversed percentage symbols or misaligned values.

**Procedure:**
1. Parse OCR text to identify table structure: headers, row labels, and data cells
2. Create explicit mapping between column headers and their positional indices
3. For each data extraction, verify: (a) correct row identified by label/position, (b) correct column identified by header name, (c) value format is valid (handle '%9' → '9%' corrections)
4. Extract the specific cell value using both row and column identifiers
5. Convert extracted string to numeric type, handling percentage conversions appropriately

**Code Example:**

**Scenario:** Extract quarterly return for Product B under "Q2 Sales" from a table with products as rows and quarters as columns.

**Correct Code:**
```python
# OCR text: "Product | Q1 Sales | Q2 Sales | Q3 Sales\nA | 12% | 15% | %8\nB | 20% | 18% | 14%"

# Step 1: Parse table structure
table_text = """Product | Q1 Sales | Q2 Sales | Q3 Sales
A | 12% | 15% | %8
B | 20% | 18% | 14%"""

lines = [line.strip() for line in table_text.split('\n')]
headers = [h.strip() for h in lines[0].split('|')]

# Step 2: Build data dictionary with explicit row-column mapping
data = {}
for line in lines[1:]:
    parts = [p.strip() for p in line.split('|')]
    row_label = parts[0]
    data[row_label] = {}
    for i, value in enumerate(parts[1:], start=1):
        # Step 3: Handle malformed percentages
        if value.startswith('%'):
            value = value[1:] + '%'
        data[row_label][headers[i]] = value

# Step 4: Extract specific cell using row and column identifiers
product = 'B'
quarter = 'Q2 Sales'
value_str = data[product][quarter]

# Step 5: Convert to numeric
value_numeric = float(value_str.rstrip('%')) / 100

# For equally-weighted portfolio of A and B under Q2:
value_a = float(data['A']['Q2 Sales'].rstrip('%')) / 100
value_b = float(data['B']['Q2 Sales'].rstrip('%')) / 100
portfolio_return = 0.5 * value_a + 0.5 * value_b

portfolio_return * 100  # Result: 16.5
```

**Common Bugs to Avoid:**
- Hardcoding column indices without verifying header alignment (e.g., assuming column 2 is always "Moderate Growth")
- Not handling reversed percentage formatting ('%9' vs '9%') before numeric conversion
- Confusing row position (1st, 2nd, 3rd) with row index (0, 1, 2) when headers occupy first line
- Using string matching on partial header names that may match multiple columns
- Failing to strip whitespace from parsed cell values before conversion

---
## Pattern: Backward Calculation from EAR to APR

**Description:** When a table provides EAR (Effective Annual Rate) and compounding frequency but asks for APR (Annual Percentage Rate), apply the inverse formula that solves backward from EAR rather than forward from APR.

**When to Use:** Questions asking for APR when given EAR and compounding frequency (monthly, quarterly, daily, etc.), typically in interest rate conversion problems.

**Procedure:**
1. Formula: APR = m × ((1 + EAR)^(1/m) - 1), where m = compounding periods per year
2. Extract EAR value and compounding frequency from correct table row
3. Map compounding frequency to m: Monthly=12, Quarterly=4, Daily=365, Weekly=52
4. Apply formula and return result in decimal or percentage form as requested

**Code Example:**

**Scenario:** Given EAR of 12.5% with quarterly compounding, find APR
**Correct Code:**
```python
# Given data
ear = 0.125  # 12.5%
compounding_frequency = "Quarterly"

# Step 1: Map frequency to periods per year
frequency_map = {
    "Monthly": 12,
    "Quarterly": 4,
    "Semiannually": 2,
    "Weekly": 52,
    "Daily": 365
}
m = frequency_map[compounding_frequency]

# Step 2: Apply backward formula
apr = m * ((1 + ear) ** (1 / m) - 1)

# Result as decimal
apr  # 0.11894...
```

**Common Bugs to Avoid:**
- Using forward formula APR/m when backward calculation is needed
- Misidentifying which value is EAR vs APR in the table
- Not converting percentage strings to decimals before calculation
- Incorrect mapping of compounding frequency to m value

---

## Pattern: Continuous Compounding EAR Calculation

**Description:** When compounding frequency is "Infinite" or "Continuous", use the exponential formula EAR = e^(APR) - 1 instead of discrete compounding formulas.

**When to Use:** Questions involving continuous compounding, infinite compounding frequency, or when table explicitly shows "Infinite" as compounding type.

**Procedure:**
1. Formula: EAR = e^(APR) - 1 for continuous compounding
2. Identify rows with "Infinite" or "Continuous" compounding
3. Extract corresponding APR value (ensure it's in decimal form)
4. Import math module and use math.exp() function
5. Return result in requested format

**Code Example:**

**Scenario:** Calculate EAR for 7.5% APR with continuous compounding
**Correct Code:**
```python
import math

# Given data
apr = 0.075  # 7.5%
compounding_type = "Infinite"

# Step 1: Check if continuous compounding
if compounding_type in ["Infinite", "Continuous"]:
    # Step 2: Apply continuous compounding formula
    ear = math.exp(apr) - 1
else:
    # Handle discrete compounding (not shown here)
    pass

# Result
ear  # 0.07788...
```

**Common Bugs to Avoid:**
- Using discrete compounding formula (1 + APR/m)^m - 1 for infinite compounding
- Forgetting to import math module
- Not subtracting 1 from e^APR
- Confusing APR and EAR positions in the formula

---

## Pattern: Time Value of Money with Logarithmic Solving

**Description:** When solving for unknown number of years in present value/future value problems, use logarithmic transformation of the compound interest formula: n = ln(FV/PV) / ln(1 + r).

**When to Use:** Questions asking to "solve for unknown number of years" given present value, future value, and interest rate in time-value tables.

**Procedure:**
1. Formula: n = ln(FV/PV) / ln(1 + r)
2. Extract PV, FV, and interest rate from correct table row
3. Validate that FV > PV for positive time periods
4. Import math module for logarithm function
5. Apply formula and return years as decimal

**Code Example:**

**Scenario:** Find years needed for $2,500 to grow to $8,000 at 9% annual rate
**Correct Code:**
```python
import math

# Given data from table row
present_value = 2500
future_value = 8000
interest_rate = 0.09  # 9%

# Step 1: Validate data
assert future_value > present_value, "FV must be greater than PV"

# Step 2: Apply logarithmic formula
years = math.log(future_value / present_value) / math.log(1 + interest_rate)

# Result
years  # 12.98...
```

**Common Bugs to Avoid:**
- Using natural log for both numerator and denominator (correct approach)
- Reversing FV and PV in the ratio
- Not converting percentage rates to decimals
- Extracting values from wrong table row due to indexing errors

---

## Pattern: Rolling Hedge Cumulative Gain Calculation

**Description:** When calculating gains from rolling futures hedges across multiple contract periods, sum the individual gains/losses from each contract segment, tracking entry and exit prices for each rolled position.

**When to Use:** Questions about rolling hedges, stack-and-roll strategies, or cumulative gains from multiple sequential futures contracts.

**Procedure:**
1. Identify all contract periods in the rolling sequence
2. For each contract: extract entry price and exit price from table
3. Calculate gain per contract: (Entry Price - Exit Price) for short positions, opposite for long
4. Sum all individual contract gains to get total gain per unit
5. Multiply by contract size if needed for total dollar gain

**Code Example:**

**Scenario:** Calculate total gain from rolling short hedge across three contracts
**Correct Code:**
```python
# Contract data: [(entry_price, exit_price), ...]
contracts = [
    (52.30, 51.80),  # First contract: short at 52.30, cover at 51.80
    (51.50, 50.90),  # Second contract: short at 51.50, cover at 50.90
    (50.70, 50.20)   # Third contract: short at 50.70, cover at 50.20
]

# Step 1: Calculate gain for each contract segment
gains = []
for entry, exit in contracts:
    # For short position: gain when price falls
    gain_per_unit = entry - exit
    gains.append(gain_per_unit)

# Step 2: Sum all gains
total_gain_per_unit = sum(gains)

# Result
total_gain_per_unit  # 1.60
```

**Common Bugs to Avoid:**
- Reversing sign convention for short vs long positions
- Missing one or more contract segments in the rolling sequence
- Using spot prices instead of futures prices at roll dates
- Not aligning entry/exit prices with correct time periods

---

## Pattern: Employee Stock Option Expected Life Calculation

**Description:** Calculate expected life of employee stock options by tracing probability-weighted paths through a binomial tree, accounting for voluntary exercise, forfeiture due to turnover, and vesting constraints.

**When to Use:** Questions asking for "expected life" of employee stock options to use in Black-Scholes-Merton, or when binomial trees include exercise probabilities and turnover rates.

**Procedure:**
1. Build probability tree with: voluntary exercise probabilities, turnover rates, vesting periods
2. For each path to terminal nodes, calculate probability of reaching that node
3. Determine exercise/forfeiture time for each path
4. Compute weighted average: Expected Life = Σ(probability × time)
5. Use this expected life (not stated maturity) as time parameter in BSM

**Code Example:**

**Scenario:** Calculate expected life from simplified tree with 2 periods
**Correct Code:**
```python
# Tree structure: time steps at 0, 2, 4 years
# Probabilities: voluntary exercise, turnover rate
time_steps = [0, 2, 4]
vesting_time = 2

# Node data: (time, voluntary_exercise_prob, turnover_rate, in_the_money)
nodes = [
    (2, 0.0, 0.05, False),   # Node at t=2, not vested yet
    (4, 0.40, 0.05, True),   # Node at t=4, ITM
    (4, 0.0, 0.05, False)    # Node at t=4, OTM
]

# Path probabilities and exercise times
paths = [
    (0.50, 4, 0.40 + 0.60 * 0.05),  # Up path: 50% prob, exercises at t=4
    (0.50, 4, 0.05)                  # Down path: 50% prob, forfeits at t=4
]

# Calculate expected life
expected_life = 0
for path_prob, time, exercise_prob in paths:
    expected_life += path_prob * time * exercise_prob

# Simplified calculation
expected_life = 4 * (0.50 * 0.425 + 0.50 * 0.05)

# Result
expected_life  # ~0.95 (simplified example)
```

**Common Bugs to Avoid:**
- Using stated maturity instead of probability-weighted expected life
- Not accounting for forfeiture due to employee turnover
- Ignoring vesting constraints in early exercise decisions
- Failing to combine voluntary exercise and forced exercise probabilities

---

## Pattern: Implied Volatility from Option Prices

**Description:** When asked for "implied standard deviation" or "implied volatility", use numerical methods (e.g., Newton-Raphson, bisection) to solve for the volatility parameter that makes Black-Scholes price equal the observed market price.

**When to Use:** Questions asking for "implied volatility", "implied standard deviation", or when given option market prices and asked to find the volatility parameter.

**Procedure:**
1. Identify the specific option: strike, maturity, type (call/put), market price
2. Extract other BSM inputs: spot price, strike, time, risk-free rate, dividends
3. Implement BSM formula or use scipy.optimize
4. Solve for σ such that BSM_price(σ) = market_price
5. Return implied volatility in decimal form

**Code Example:**

**Scenario:** Find implied volatility for call option with market price $5.50
**Correct Code:**
```python
import math
from scipy.stats import norm
from scipy.optimize import brentq

def black_scholes_call(S, K, T, r, sigma):
    """Calculate Black-Scholes call option price"""
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)

# Given data
S = 85        # Stock price
K = 90        # Strike price
T = 0.25      # 3 months = 0.25 years
r = 0.038     # 3.8% risk-free rate
market_price = 5.50

# Objective function: difference between model and market price
def objective(sigma):
    return black_scholes_call(S, K, T, r, sigma) - market_price

# Solve for implied volatility using bisection
implied_vol = brentq(objective, 0.01, 2.0)

# Result
implied_vol  # ~0.35 (example)
```

**Common Bugs to Avoid:**
- Using wrong option from table when "this call" is ambiguous
- Not converting time to years (e.g., months to years)
- Forgetting to import scipy or math modules
- Using historical volatility instead of solving for implied volatility

---

## Pattern: OCR Text Validation and Malformed Data Handling

**Description:** Validate OCR-extracted numeric values for formatting errors (e.g., '%9' instead of '9%', missing values, misaligned decimals, symbols before numbers) and apply correction rules before performing calculations. Implement systematic checks for common OCR errors including reversed symbols, missing decimal points, and character substitution.

**When to Use:** All problems using OCR text from images, especially when tables contain percentage values, decimal numbers, or when data appears incomplete or malformed. Trigger on any OCR input before numeric conversion.

**Procedure:**
1. Extract raw OCR text and identify all numeric fields
2. Apply pattern matching to detect common OCR errors: reversed symbols ('%9'), missing decimals ('125' vs '1.25'), character substitutions ('O' vs '0')
3. Implement correction rules: move misplaced symbols, validate decimal placement, convert characters
4. Validate corrected values against expected ranges (e.g., percentages between 0-100)
5. Flag or handle any values that cannot be reliably corrected

**Code Example:**

**Scenario:** OCR extracted "Return: %15, Rate: 3.5O%, Loss: -9" from a financial table. Correct and convert to numeric values.

**Correct Code:**
```python
import re

# Raw OCR text with common errors
ocr_values = {
    'return': '%15',      # Reversed percentage
    'rate': '3.5O%',      # Letter O instead of zero
    'loss': '-9'          # Missing percentage sign
}

def correct_ocr_percentage(value_str):
    """Correct common OCR errors in percentage values"""
    # Step 1: Handle reversed percentage symbol
    if value_str.startswith('%'):
        value_str = value_str[1:] + '%'
    
    # Step 2: Replace common character substitutions
    value_str = value_str.replace('O', '0').replace('o', '0')
    
    # Step 3: Ensure percentage symbol exists if numeric
    if '%' not in value_str and re.match(r'^-?\d+\.?\d*$', value_str):
        value_str = value_str + '%'
    
    # Step 4: Extract numeric value
    numeric_str = value_str.rstrip('%').strip()
    numeric_value = float(numeric_str) / 100
    
    return numeric_value

# Apply corrections
corrected_return = correct_ocr_percentage(ocr_values['return'])
corrected_rate = correct_ocr_percentage(ocr_values['rate'])
corrected_loss = correct_ocr_percentage(ocr_values['loss'])

# Validation: check if values are in reasonable range
assert -1.0 <= corrected_return <= 2.0, "Return out of reasonable range"
assert 0 <= corrected_rate <= 0.5, "Rate out of reasonable range"

corrected_return  # Result: 0.15 (15%)
```

**Common Bugs to Avoid:**
- Converting OCR text to numeric without checking for formatting errors first
- Not handling reversed symbols ('%9' treated as invalid rather than corrected to '9%')
- Missing character substitution corrections (O/0, l/1, S/5 confusion)
- Assuming all percentage values have '%' symbol when OCR may drop it
- Not validating corrected values against reasonable ranges before use in calculations
- Failing to preserve negative signs during correction process
## Pattern: Missing Data Detection and Handling

**Description:** Detect incomplete or missing values in probability distributions or tables, and either flag the problem as unsolvable, apply appropriate imputation methods, or infer missing values from constraints (e.g., probabilities sum to 1).

**When to Use:** When tables contain empty cells, incomplete data rows, or when probability distributions don't sum to expected values.

**Procedure:**
1. Parse table and identify all cells, marking empty/missing ones
2. Check constraints: probabilities sum to 1, all required fields present
3. If missing data can be inferred (e.g., last probability = 1 - sum of others), compute it
4. If missing data cannot be inferred and is critical, flag as unsolvable
5. Document assumptions if imputation is used

**Code Example:**

**Scenario:** Handle missing return value in probability distribution
**Correct Code:**
```python
# Probability distribution with missing value
states = [
    {'prob': 0.15, 'return_A': 0.08, 'return_B': 0.08},
    {'prob': 0.20, 'return_A': 0.13, 'return_B': 0.07},
    {'prob': 0.15, 'return_A': 0.12, 'return_B': 0.05},
    {'prob': 0.30, 'return_A': 0.14, 'return_B': None},  # Missing value
    {'prob': 0.20, 'return_A': 0.16, 'return_B': 0.11}
]

# Step 1: Check for missing values
missing_data = []
for i, state in enumerate(states):
    if state['return_B'] is None:
        missing_data.append(i)

# Step 2: Determine if calculation can proceed
if missing_data:
    # Check if we can infer from context or if it's critical
    critical_missing = True  # In this case, we need all returns for expected value
    
    if critical_missing:
        result = "Cannot calculate: missing return value in state 4"
    else:
        # Proceed with available data (if appropriate)
        pass
else:
    # Calculate expected return
    expected_return_B = sum(s['prob'] * s['return_B'] for s in states)
    result = expected_return_B

result  # Error message or calculated value
```

**Common Bugs to Avoid:**
- Proceeding with calculations when critical data is missing
- Not checking if probabilities sum to 1.0
- Assuming missing values are zero without justification
- Not documenting or flagging data quality issues

---

## Pattern: Portfolio Expected Return and Standard Deviation with Correlation

**Description:** Calculate portfolio expected return as weighted average of asset returns, and portfolio standard deviation using the full covariance formula that accounts for correlation between assets.

**When to Use:** Questions asking for portfolio expected return and standard deviation given individual asset returns, standard deviations, weights, and correlation or covariance.

**Procedure:**
1. Formula (Expected Return): E(Rp) = Σ(wi × E(Ri))
2. Formula (Std Dev): σp = √(wA²σA² + wB²σB² + 2wAwBρABσAσB) for two assets
3. Calculate expected return for each asset from probability distribution
4. Calculate standard deviation for each asset
5. Compute covariance or use given correlation
6. Apply portfolio variance formula and take square root

**Code Example:**

**Scenario:** Two-asset portfolio with 30% in A, 70% in B
**Correct Code:**
```python
import math

# Asset A statistics
E_A = 0.12      # Expected return 12%
sigma_A = 0.18  # Standard deviation 18%
w_A = 0.30      # Weight 30%

# Asset B statistics
E_B = 0.09      # Expected return 9%
sigma_B = 0.12  # Standard deviation 12%
w_B = 0.70      # Weight 70%

# Correlation between A and B
rho_AB = 0.25

# Step 1: Portfolio expected return
E_portfolio = w_A * E_A + w_B * E_B

# Step 2: Portfolio variance
var_portfolio = (w_A**2 * sigma_A**2 + 
                 w_B**2 * sigma_B**2 + 
                 2 * w_A * w_B * rho_AB * sigma_A * sigma_B)

# Step 3: Portfolio standard deviation
sigma_portfolio = math.sqrt(var_portfolio)

# Results
result = (E_portfolio, sigma_portfolio)
result  # (0.099, 0.1089...)
```

**Common Bugs to Avoid:**
- Forgetting the correlation term (2wAwBρσAσB) in variance formula
- Not squaring weights and standard deviations in variance calculation
- Forgetting to take square root of variance to get standard deviation
- Using correlation when covariance is given (or vice versa) without conversion

---

## Pattern: Alpha Calculation in CAPM Framework

**Description:** Calculate Jensen's alpha as the difference between actual expected return and CAPM-predicted return: α = E(R) - [Rf + β(E(Rm) - Rf)].

**When to Use:** Questions asking for "alpha values" given expected returns, betas, risk-free rate, and market return.

**Procedure:**
1. Formula: α = E(R) - [Rf + β × (E(Rm) - Rf)]
2. Extract risk-free rate (often from T-bills row)
3. Extract market return (often from passive equity portfolio)
4. For each asset: extract expected return and beta
5. Calculate CAPM expected return, then subtract from actual expected return

**Code Example:**

**Scenario:** Calculate alpha for stock with 15% expected return, beta 1.2
**Correct Code:**
```python
# Market data
rf = 0.08           # Risk-free rate 8%
market_return = 0.16  # Market return 16%

# Stock data
expected_return = 0.15  # Expected return 15%
beta = 1.2              # Beta 1.2

# Step 1: Calculate CAPM expected return
capm_return = rf + beta * (market_return - rf)

# Step 2: Calculate alpha
alpha = expected_return - capm_return

# Result
alpha  # -0.016 or -1.6%
```

**Common Bugs to Avoid:**
- Using wrong values for risk-free rate or market return from table
- Forgetting to subtract risk-free rate in market risk premium
- Confusing alpha with excess return (excess return = R - Rf)
- Not converting percentages to decimals consistently

## Pattern: Labor-Based GDP Growth Component Selection

**Description:** When calculating aggregate GDP growth using the labor-based approach, correctly identify that labor force growth already incorporates participation rate changes, and that the formula requires only labor quantity growth (labor force growth) plus labor quality growth (productivity growth), avoiding double-counting of participation rate as a separate additive term.

**When to Use:** Questions asking to forecast GDP growth using "labor-based method" or "labor-based approach" when given macroeconomic data including labor force growth, labor force participation growth, and labor productivity growth.

**Procedure:**
1. Formula: GDP Growth ≈ Labor Force Growth + Labor Productivity Growth
2. Identify "Growth in potential labor force" (or similar) as the labor quantity component - this already reflects participation rate changes
3. Identify "Growth in labor productivity" as the labor quality component
4. Do NOT add "Growth in labor force participation" as a separate term (it's already embedded in labor force growth)
5. Sum only the two components: labor force growth + productivity growth

**Code Example:**

**Scenario:** Given 10-year forecast data: Growth in potential labor force = 1.5%, Growth in labor productivity = 1.2%, Growth in labor force participation = 0.4%, Growth in real consumer spending = 2.8%. Calculate GDP growth using labor-based method.

**Correct Code:**
```python
# Given macroeconomic data
labor_force_growth = 1.5  # Already incorporates participation changes
labor_productivity_growth = 1.2
labor_participation_growth = 0.4  # Do NOT use - already in labor force growth
consumer_spending_growth = 2.8  # Not part of labor-based formula

# Labor-based GDP growth formula
# GDP Growth = Labor Quantity Growth + Labor Quality Growth
gdp_growth = labor_force_growth + labor_productivity_growth

gdp_growth  # Result: 2.7
```

**Common Bugs to Avoid:**
- Adding labor force participation growth as a third independent term (double-counting)
- Confusing "potential labor force growth" with "labor force participation growth"
- Including non-labor components like consumer spending growth in the labor-based formula
- Using total factor productivity (TFP) instead of labor productivity in this specific formula
- Forgetting that the labor-based approach is a decomposition, not a sum of all available growth metrics

---

## Pattern: Monte Carlo Percentile Interpretation for Goal Achievement

**Description:** When interpreting Monte Carlo simulation results presented as percentiles, recognize that the Nth percentile value represents the outcome where N% of scenarios fall below that value, meaning the probability of exceeding that value is (100-N)%. To determine probability of meeting a goal, find which percentile bracket contains the goal amount and interpolate or identify the corresponding success probability.

**When to Use:** Questions asking for "probability of success" or "probability of meeting goals" when given Monte Carlo simulation results displayed as percentile outcomes (e.g., 25th%, 50th%, 75th% portfolio values).

**Procedure:**
1. Identify the goal amount (target value to achieve)
2. Locate which percentile values bracket the goal amount in the simulation results
3. Recognize inverse relationship: if goal falls at Nth percentile, probability of success = (100 - N)%
4. If goal is between two percentiles, determine which it's closer to or use interpolation
5. Return the probability as a percentage

**Code Example:**

**Scenario:** Monte Carlo simulation for retirement goal of $850,000 in Year 15 shows: 25th percentile = $900,000, 50th percentile = $800,000, 75th percentile = $750,000. What is probability of meeting the goal?

**Correct Code:**
```python
# Monte Carlo simulation results (percentiles)
percentile_25 = 900000  # 25% of outcomes are below this
percentile_50 = 800000  # 50% of outcomes are below this
percentile_75 = 750000  # 75% of outcomes are below this

goal_amount = 850000

# Step 1: Determine which percentile bracket contains the goal
# Goal of 850,000 falls between 50th (800k) and 25th (900k) percentiles

# Step 2: Since goal is between 50th and 25th percentiles,
# probability of success is between 50% and 75%

# Step 3: Closer to 25th percentile value (900k), so closer to 75% probability
# For exact interpolation:
if goal_amount >= percentile_25:
    probability = 100 - 25  # At or above 25th percentile
elif goal_amount >= percentile_50:
    # Linear interpolation between 50th and 25th
    range_values = percentile_25 - percentile_50
    range_prob = 25 - 50  # -25 percentage points
    position = (goal_amount - percentile_50) / range_values
    probability = 50 + position * abs(range_prob)
else:
    probability = 50  # Below 50th percentile

probability  # Result: ~68.75, closest to 75%
```

**Common Bugs to Avoid:**
- Treating percentile rank as probability of success directly (25th percentile ≠ 25% success)
- Forgetting the inverse relationship: lower percentile rank = higher probability of exceeding
- Comparing goal to percentile values without considering which direction indicates success
- Not recognizing that "meeting goal" means portfolio value ≥ goal (exceeding the percentile threshold)
- Ignoring interpolation when goal falls between reported percentiles

---