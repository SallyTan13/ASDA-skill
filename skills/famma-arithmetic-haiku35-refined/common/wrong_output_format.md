# SKILL PATTERNS FOR PROGRAM OF THOUGHT: OUTPUT FORMAT ERRORS

## Pattern: Source-Use Cash Flow Classification

**Description:** Cash flow statement analysis requires both directional classification (Source/Use) and signed monetary formatting. Computing only the numerical change without classification and formatting conventions leads to incomplete answers.

**When to Use:** Questions asking to "determine whether [item] is a source or use of cash" or analyzing balance sheet changes for cash flow statements.

**Procedure:**
1. Formula: Change = Current Period Value - Prior Period Value
2. Extract the line item values from both periods (earlier and later)
3. Calculate the change (later - earlier)
4. Apply classification rules:
   - Assets: Increase = Use (negative), Decrease = Source (positive)
   - Liabilities/Equity: Increase = Source (positive), Decrease = Use (negative)
   - Exception: Cash itself follows opposite convention (decrease = source for other activities)
5. Format output as: "{Classification}, ${absolute_value:,}" or "{Classification}, –${absolute_value:,}"

**Code Example:**

**Scenario:** Accounts Receivable increased from $120,000 to $135,000. Determine if this is a source or use of cash.

**Correct Code:**
```python
# Balance sheet values
accounts_receivable_prior = 120000
accounts_receivable_current = 135000

# Calculate change
change = accounts_receivable_current - accounts_receivable_prior

# Classification logic for assets (excluding cash)
if change > 0:
    classification = "Use"
    amount = abs(change)
    result = f"{classification}, –${amount:,}"
elif change < 0:
    classification = "Source"
    amount = abs(change)
    result = f"{classification}, ${amount:,}"
else:
    result = "No change, $0"

result  # Must be expression, not print
```

**Common Bugs to Avoid:**
- Returning only the numerical value without classification label
- Forgetting to use absolute value for the amount display
- Incorrect sign convention (Use should show negative/dash, Source positive)
- Using print() instead of expression on last line
- Not handling the special case for cash (decrease in cash = source)

---

## Pattern: Multiple-Choice Selection from Computational Results

**Description:** When computations identify multiple valid candidates but the question format requires selecting a single multiple-choice answer, the code must map computational results to the answer key structure rather than creating a custom response.

**When to Use:** Multiple-choice questions where computation yields a set of valid items (e.g., "which portfolio(s) is/are on the efficient frontier") but answer options include individual choices and combination options.

**Procedure:**
1. Perform the complete computational analysis (e.g., calculate metrics for all options)
2. Identify all items that meet the criteria
3. Check answer options to see if:
   - Any single option matches one valid result → select that option
   - A combination option (e.g., "A and B") exactly matches your results → select it
   - Multiple individual options are valid but no combination option matches → select the first valid individual option
4. Return the option letter(s) as a string, not a list of results

**Code Example:**

**Scenario:** Calculate Sharpe ratios for 4 portfolios. Options A, B, C are individual portfolios, D says "A and C both maximize Sharpe ratio". Portfolios A and C both have Sharpe ratio 0.85 (highest).

**Correct Code:**
```python
import numpy as np

# Portfolio metrics
portfolios = {
    'A': {'return': 0.12, 'std': 0.15},
    'B': {'return': 0.10, 'std': 0.14},
    'C': {'return': 0.13, 'std': 0.16},
}
risk_free_rate = 0.03

# Calculate Sharpe ratios
sharpe_ratios = {}
for name, metrics in portfolios.items():
    sharpe_ratios[name] = (metrics['return'] - risk_free_rate) / metrics['std']

# Find maximum Sharpe ratio
max_sharpe = max(sharpe_ratios.values())
optimal_portfolios = [k for k, v in sharpe_ratios.items() if abs(v - max_sharpe) < 1e-6]

# Map to answer options
# Options: A, B, C (individual), D (states "A and C")
if len(optimal_portfolios) == 2 and set(optimal_portfolios) == {'A', 'C'}:
    answer = 'D'  # Combination option matches
elif 'A' in optimal_portfolios:
    answer = 'A'  # Select first valid individual
else:
    answer = optimal_portfolios[0]

answer
```

**Common Bugs to Avoid:**
- Returning a list like ['A', 'C'] instead of mapping to the answer key
- Selecting a combination option when it doesn't match the exact set of valid results
- Not checking if combination options exist before defaulting to individual selections
- Using print() instead of returning the answer string

---

## Pattern: Decision Rule Output Formatting

**Description:** Financial decision rules (NPV, PI, IRR, payback) require selecting and naming the chosen alternative, not outputting intermediate numerical comparisons or metric values.

**When to Use:** Questions asking "which project should the firm accept/choose" based on profitability index, NPV, IRR, or other decision criteria.

**Procedure:**
1. Formula: PI = PV(Future Cash Flows) / Initial Investment; NPV = PV(All Cash Flows)
2. Calculate the decision metric for each alternative
3. Apply the decision rule:
   - PI: Select project with highest PI > 1.0
   - NPV: Select project with highest NPV > 0
   - IRR: Select project with highest IRR > required return
4. For mutually exclusive projects, select the single best option
5. Return the project name/identifier as a string (e.g., "Project II", "Project Alpha")

**Code Example:**

**Scenario:** Two projects with 12% required return. Project X: Initial cost $50,000, PV of inflows $58,000. Project Y: Initial cost $30,000, PV of inflows $37,500. Which should be accepted using PI rule?

**Correct Code:**
```python
# Project cash flows
projects = {
    'Project X': {'initial_cost': 50000, 'pv_inflows': 58000},
    'Project Y': {'initial_cost': 30000, 'pv_inflows': 37500}
}

# Calculate profitability index for each
pi_values = {}
for name, data in projects.items():
    pi_values[name] = data['pv_inflows'] / data['initial_cost']

# Apply decision rule: select highest PI > 1.0
acceptable_projects = {k: v for k, v in pi_values.items() if v > 1.0}

if acceptable_projects:
    # Select project with maximum PI
    selected_project = max(acceptable_projects, key=acceptable_projects.get)
    result = selected_project
else:
    result = "Reject all projects"

result  # Returns "Project Y" (PI = 1.25 vs 1.16)
```

**Common Bugs to Avoid:**
- Returning the PI value (e.g., 1.25) instead of the project name
- Returning a comparison result (e.g., PI_X - PI_Y) instead of the decision
- Not checking if any projects meet the acceptance threshold (PI > 1.0)
- Forgetting to handle the case where all projects should be rejected
- Using print() instead of expression on last line

---

## Pattern: Labeled Monetary Output Formatting

**Description:** Financial answers often require specific formatting conventions including currency symbols, thousand separators, decimal precision, and contextual labels, not raw numerical values.

**When to Use:** Any question requesting monetary amounts, especially when context requires interpretation (e.g., "the amount" in cash flow analysis, cost calculations, valuation results).

**Procedure:**
1. Perform the numerical calculation
2. Determine the appropriate sign convention for the context
3. Format with currency symbol and thousand separators
4. Add contextual labels if required by the question format
5. Return formatted string, not raw float

**Code Example:**

**Scenario:** Calculate the net working capital change. Current assets increased by $45,000, current liabilities increased by $28,000.

**Correct Code:**
```python
# Changes in balance sheet items
change_current_assets = 45000
change_current_liabilities = 28000

# Net working capital change
nwc_change = change_current_assets - change_current_liabilities

# Format output with proper conventions
if nwc_change >= 0:
    result = f"${nwc_change:,.0f}"
else:
    result = f"–${abs(nwc_change):,.0f}"

result  # Returns "$17,000"
```

**Common Bugs to Avoid:**
- Returning raw float (17000.0) instead of formatted string ("$17,000")
- Missing thousand separators for readability
- Incorrect negative sign formatting (using "-" instead of "–" or parentheses as per convention)
- Including unnecessary decimal places for whole dollar amounts
- Using print() instead of expression on last line