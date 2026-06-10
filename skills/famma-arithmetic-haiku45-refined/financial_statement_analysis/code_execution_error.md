# SKILL PATTERNS FOR FINANCIAL STATEMENT ANALYSIS (PoT)

## Pattern: Cash Flow Statement Source vs Use Classification

**Description:** When analyzing changes in balance sheet items for cash flow impact, correctly classify increases/decreases in assets and liabilities as sources or uses of cash, and apply proper sign conventions for reporting.

**When to Use:** Questions asking whether a balance sheet item change is a "source" or "use" of cash, cash flow statement construction, working capital analysis.

**Procedure:**
1. Formula: Change = Ending Balance - Beginning Balance
2. Extract the balance sheet values for both periods (earlier and later)
3. Calculate the change (later period - earlier period)
4. Apply classification rules:
   - Assets: Decrease = Source (positive), Increase = Use (negative)
   - Liabilities: Increase = Source (positive), Decrease = Use (negative)
   - Equity: Increase = Source (positive), Decrease = Use (negative)
5. Return classification and the change amount with appropriate sign

**Code Example:**

**Scenario:** Inventory increased from $85,000 to $92,000. Determine if this is a source or use of cash.

**Correct Code:**
```python
# Balance sheet values
inventory_beginning = 85_000
inventory_ending = 92_000

# Calculate change
change = inventory_ending - inventory_beginning

# Inventory is an ASSET
# Asset increase = Use of cash (negative for cash flow)
# Asset decrease = Source of cash (positive for cash flow)
if change > 0:
    classification = "Use"
    cash_flow_impact = -change  # Negative impact on cash
elif change < 0:
    classification = "Source"
    cash_flow_impact = -change  # Positive impact on cash (double negative)
else:
    classification = "No impact"
    cash_flow_impact = 0

# Return as tuple or formatted string
(classification, cash_flow_impact)
```

**Correct Code (Liabilities):**
```python
# Accounts Payable decreased from $80,000 to $65,000
accounts_payable_beginning = 80_000
accounts_payable_ending = 65_000

# Calculate change
change = accounts_payable_ending - accounts_payable_beginning

# Accounts Payable is a LIABILITY
# Liability decrease = Use of cash (we paid down debt)
# Liability increase = Source of cash (we borrowed/delayed payment)
if change < 0:
    classification = "Use"
    amount = abs(change)
elif change > 0:
    classification = "Source"
    amount = abs(change)
else:
    classification = "No impact"
    amount = 0

# Final answer
(classification, change)  # Returns ("Use", -15000)
```

**Common Bugs to Avoid:**
- Confusing asset vs liability rules (they work in opposite directions)
- Reporting only absolute values without proper sign for cash flow impact
- Using print() instead of returning the value as an expression
- Forgetting that "Use" means negative cash flow (cash outflow)

---

## Pattern: International Number Format Disambiguation

**Description:** Financial statements may use different decimal/thousands separators (European: 130.000 = 130k vs American: 130,000 = 130k). Must validate extracted numbers against contextual clues like par value, market cap, or ratio reasonableness.

**When to Use:** When extracting numerical data from OCR'd financial statements, especially when dealing with share counts, and when calculated ratios seem unreasonable compared to answer options.

**Procedure:**
1. Extract the raw number from OCR text
2. Identify ambiguous formatting (periods vs commas as separators)
3. Cross-validate using contextual financial relationships:
   - Common Stock $ / Shares = Par Value per Share (typically $0.01 to $10)
   - Market Cap = Stock Price × Shares Outstanding (reasonableness check)
   - Calculate ratio with both interpretations and compare to answer options
4. Choose the interpretation that produces financially reasonable results

**Code Example:**

**Scenario:** OCR extracts "Common stock 45.000 shares" and "$90,000" common stock value. Stock price is $25. Calculate P/E ratio given net income of $180,000.

**Correct Code:**
```python
# OCR extracted values
common_stock_value = 90_000
shares_text = "45.000"  # Ambiguous format
stock_price = 25
net_income = 180_000

# Parse both possible interpretations
shares_interpretation_1 = 45_000  # American: 45,000 shares
shares_interpretation_2 = 45  # European: 45.000 = 45 thousand = 45,000

# Validation 1: Par value check
# Par value = Common Stock $ / Shares
par_value_1 = common_stock_value / shares_interpretation_1  # $2.00
par_value_2 = common_stock_value / shares_interpretation_2  # $2,000

# Par value of $2.00 is reasonable; $2,000 is not
# This suggests interpretation 1 is correct

# Validation 2: Calculate ratio with both and check reasonableness
eps_1 = net_income / shares_interpretation_1  # $4.00
pe_ratio_1 = stock_price / eps_1  # 6.25

eps_2 = net_income / shares_interpretation_2  # $4,000
pe_ratio_2 = stock_price / eps_2  # 0.00625

# P/E ratio of 6.25 is reasonable; 0.00625 is not
# Confirms interpretation 1

shares_outstanding = shares_interpretation_1
eps = net_income / shares_outstanding
pe_ratio = stock_price / eps

pe_ratio  # Returns 6.25
```

**Correct Code (with answer option validation):**
```python
# When answer options are available, use them for validation
net_income = 180_000
stock_price = 25
common_stock_value = 90_000
answer_options = [4.74, 6.63, 5.21, 5.00]

# Try different share count interpretations
possible_shares = [45, 450, 4_500, 45_000, 450_000]

results = []
for shares in possible_shares:
    par_value = common_stock_value / shares
    eps = net_income / shares
    pe_ratio = stock_price / eps
    
    # Check if par value is reasonable (typically $0.01 to $100)
    # Check if P/E ratio matches any answer option (within 5% tolerance)
    par_reasonable = 0.01 <= par_value <= 100
    matches_option = any(abs(pe_ratio - opt) / opt < 0.05 for opt in answer_options)
    
    results.append({
        'shares': shares,
        'par_value': par_value,
        'pe_ratio': pe_ratio,
        'valid': par_reasonable and matches_option
    })

# Select the valid interpretation
valid_result = [r for r in results if r['valid']][0]
valid_result['pe_ratio']
```

**Common Bugs to Avoid:**
- Blindly accepting OCR output without validation
- Not checking par value reasonableness (should be small, typically < $100)
- Ignoring answer options as validation clues
- Not considering regional number formatting conventions
- Failing to cross-check with multiple financial relationships

---

## Pattern: Per-Share Metric Calculation with Share Count Verification

**Description:** When calculating per-share metrics (EPS, P/E, P/B), verify share count accuracy by reconciling common stock dollar value with implied par value, and validate final ratios against expected ranges or answer options.

**When to Use:** Questions involving EPS, P/E ratio, P/B ratio, dividend per share, or any metric requiring shares outstanding.

**Procedure:**
1. Formula: EPS = Net Income / Shares Outstanding; P/E = Stock Price / EPS
2. Extract net income, stock price, shares outstanding, and common stock $ value
3. Verify shares outstanding: Par Value = Common Stock $ / Shares (should be reasonable, typically $0.01-$10)
4. Calculate EPS = Net Income / Shares Outstanding
5. Calculate target ratio (e.g., P/E = Price / EPS)
6. Sanity check: Compare result to typical ranges or answer options

**Code Example:**

**Scenario:** Net income is $450,000, stock price is $28, common stock value is $200,000, shares listed as "40.000". Answer options for P/E are [5.5, 7.2, 8.9, 12.4].

**Correct Code:**
```python
# Financial data
net_income = 450_000
stock_price = 28
common_stock_value = 200_000
shares_raw = "40.000"  # Ambiguous

# Parse possible share counts
shares_option_1 = 40_000  # If period is thousands separator
shares_option_2 = 40  # If period is decimal (40 shares total - unlikely)

# Verify with par value check
par_value_1 = common_stock_value / shares_option_1  # $5.00
par_value_2 = common_stock_value / shares_option_2  # $5,000

# Par value of $5.00 is typical; $5,000 is unreasonable
shares_outstanding = shares_option_1

# Calculate EPS
eps = net_income / shares_outstanding  # $11.25

# Calculate P/E ratio
pe_ratio = stock_price / eps  # 2.49

# Validation: Check against answer options
answer_options = [5.5, 7.2, 8.9, 12.4]
closest_option = min(answer_options, key=lambda x: abs(x - pe_ratio))

# If no match, reconsider share count
# Perhaps shares are in thousands: 40.000 = 40,000 already considered
# Or perhaps common stock includes additional paid-in capital

# Return calculated ratio
pe_ratio  # 2.49
```

**Correct Code (with error detection):**
```python
# More robust version with validation
net_income = 450_000
stock_price = 28
common_stock_value = 200_000
answer_options = [5.5, 7.2, 8.9, 12.4]

# Try multiple interpretations
interpretations = [
    ('40 shares', 40),
    ('40 thousand shares', 40_000),
    ('Infer from par $5', common_stock_value / 5),  # Assume $5 par
    ('Infer from par $1', common_stock_value / 1),  # Assume $1 par
]

for description, shares in interpretations:
    if shares <= 0:
        continue
    
    par_value = common_stock_value / shares
    eps = net_income / shares
    pe_ratio = stock_price / eps
    
    # Check if par value is reasonable AND P/E matches options
    par_reasonable = 0.01 <= par_value <= 100
    matches_option = any(abs(pe_ratio - opt) / opt < 0.10 for opt in answer_options)
    
    if par_reasonable and matches_option:
        # Found valid interpretation
        final_pe_ratio = pe_ratio
        break

final_pe_ratio  # Returns the validated P/E ratio
```

**Common Bugs to Avoid:**
- Not validating share count against par value reasonableness
- Ignoring answer options as a validation mechanism
- Confusing shares outstanding with authorized shares
- Not considering that "common stock" line may include par value only (not APIC)
- Using print() instead of expression for final answer
- Failing to handle ambiguous number formats (European vs American notation)

---

## Pattern: Financial Statement Data Extraction with Unit Consistency

**Description:** When extracting values from financial statements, ensure consistent units (thousands, millions) and validate that extracted values maintain accounting equation balance (Assets = Liabilities + Equity).

**When to Use:** All financial statement analysis questions, especially when OCR provides raw text that may include unit indicators or formatting inconsistencies.

**Procedure:**
1. Identify unit indicators in the statement header ("in thousands", "in millions", "$000")
2. Extract all relevant values with consistent unit conversion
3. Validate using accounting equation: Total Assets = Total Liabilities + Total Equity
4. If validation fails, recheck unit interpretation or OCR errors
5. Perform calculations with validated values

**Code Example:**

**Scenario:** Balance sheet shows "Assets: Cash 125, Inventory 340, Total 465" and "Liabilities 200, Equity 250, Total 450". Header says "in thousands". Calculate current ratio.

**Correct Code:**
```python
# Extract values (in thousands per header)
unit_multiplier = 1_000

cash = 125 * unit_multiplier
inventory = 340 * unit_multiplier
total_assets = 465 * unit_multiplier

current_liabilities = 200 * unit_multiplier
equity = 250 * unit_multiplier
total_liabilities_equity = 450 * unit_multiplier

# Validation: Check accounting equation
# Total Assets should equal Total Liabilities + Equity
accounting_equation_valid = abs(total_assets - total_liabilities_equity) <= 1_000  # Allow $1k rounding

if not accounting_equation_valid:
    # Recheck: maybe OCR error or different unit interpretation
    # In this case: 465 ≠ 450, difference of 15k
    # This suggests possible OCR error or missing line item
    pass

# Assume current liabilities are given (or extract from statement)
# Calculate current ratio
current_assets = cash + inventory  # 465k
current_ratio = current_assets / current_liabilities

current_ratio  # Returns 2.325
```

**Correct Code (with comprehensive validation):**
```python
# More robust extraction with validation
def validate_balance_sheet(assets, liabilities, equity, tolerance=0.01):
    """Validate accounting equation within tolerance percentage"""
    total_assets = sum(assets.values())
    total_liab_equity = sum(liabilities.values()) + sum(equity.values())
    
    difference = abs(total_assets - total_liab_equity)
    relative_error = difference / total_assets if total_assets > 0 else 0
    
    return relative_error <= tolerance

# Extract with units
unit_multiplier = 1_000  # "in thousands"

assets = {
    'cash': 125 * unit_multiplier,
    'accounts_receivable': 0,  # Not listed
    'inventory': 340 * unit_multiplier,
}

liabilities = {
    'accounts_payable': 200 * unit_multiplier,
}

equity = {
    'common_stock': 150 * unit_multiplier,
    'retained_earnings': 100 * unit_multiplier,
}

# Validate before calculation
is_valid = validate_balance_sheet(assets, liabilities, equity, tolerance=0.05)

if is_valid:
    current_assets = assets['cash'] + assets['inventory']
    current_liabilities = liabilities['accounts_payable']
    current_ratio = current_assets / current_liabilities
else:
    # Handle validation failure
    current_ratio = None

current_ratio  # Returns validated result or None
```

**Common Bugs to Avoid:**
- Mixing units (some values in thousands, others in actual dollars)
- Not reading statement headers for unit indicators
- Failing to validate accounting equation before calculations
- Ignoring small discrepancies that indicate OCR or extraction errors
- Not handling missing values (assuming zero vs flagging as error)