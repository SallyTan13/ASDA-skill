# Financial Statement Analysis — Cash Collections and Cash Flow Classification

## CODE CONSTRAINTS (MANDATORY)

**Your generated code MUST:**
- ✅ End with variable name or expression (for eval() to capture)
- ✅ Include ALL necessary imports at the top
- ✅ Define ALL variables before use
- ✅ Use explicit values from the question

**Your generated code MUST NOT:**
- ❌ Use input() or any interactive functions
- ❌ Use print() as the last line (returns None)
- ❌ Use variables without defining them first

**Available libraries (must import if used):**
- import math
- import numpy as np
- from scipy.stats import norm
- from scipy.optimize import brentq

## Pattern: Multi-Period Cash Collections from Credit Sales

**Description:** Calculate cash collections for a period when sales are collected over multiple months with specified collection percentages. Uses actual sales figures from the question when available, and only back-calculates from AR when sales figures are not provided.

**When to Use:** 
- Question asks for "cash collections" for a specific period
- Collection pattern spans multiple periods (e.g., 65% current month, 20% next month, 15% two months later)
- Given partial AR information (e.g., "uncollected amount from prior period")
- Need to determine collections from current AND multiple prior periods

**When NOT to Use:**
- Question asks for "liquidating value" or bankruptcy-related calculations
- Question provides actual sales figures for all relevant periods in a sales budget table (use those directly instead of back-calculating)

**Procedure:**
1. **Identify the collection pattern** — Extract all collection percentages and their timing (e.g., 65% in month 0, 20% in month 1, 15% in month 2)
2. **Determine uncollected percentage** — Calculate what portion remains uncollected after each period (100% - collected%)
3. **Check for provided sales figures FIRST** — If the question includes a sales budget table with actual sales amounts for prior periods, use those values directly
4. **Back-calculate original sales ONLY when needed** — If given "uncollected amount" but NO actual sales figure for that period, divide by uncollected percentage to find original sales
5. **Identify all relevant prior periods** — Based on collection pattern, determine how many prior months contribute to current collections
6. **Calculate collections from each period:**
   - Current period sales × current period collection rate
   - Prior period 1 sales × period 1 collection rate (use actual sales if provided, otherwise back-calculate)
   - Prior period 2 sales × period 2 collection rate (use actual sales if provided, otherwise back-calculate)
7. **Sum all collections** — Add collections from all relevant periods

**Worked Example:**

**Question:** A company collects 65% of sales in the month of sale, 20% in the following month, and 15% two months after sale. January sales are $285,000. December sales resulted in $87,750 still uncollected at the end of December. The remaining accounts receivable of $35,050 is from November sales. Calculate cash collections for January.

```python
# Collection pattern: 65% month 0, 20% month 1, 15% month 2
collection_rate_month_0 = 0.65
collection_rate_month_1 = 0.20
collection_rate_month_2 = 0.15

# January sales (current month)
january_sales = 285000

# Back-calculate December sales from uncollected amount
# Uncollected from December = 20% (collected in Jan) + 15% (collected in Feb) = 35%
uncollected_december_amount = 87750
uncollected_december_rate = collection_rate_month_1 + collection_rate_month_2
december_sales = uncollected_december_amount / uncollected_december_rate

# Back-calculate November sales from remaining AR
# Only 15% of November sales remains uncollected (to be collected in January)
uncollected_november_amount = 35050
november_sales = uncollected_november_amount / collection_rate_month_2

# Calculate collections for January
collections_from_january = january_sales * collection_rate_month_0
collections_from_december = december_sales * collection_rate_month_1
collections_from_november = november_sales * collection_rate_month_2

# Total cash collections for January
total_collections = collections_from_january + collections_from_december + collections_from_november

# Round to 2 decimal places
total_collections = round(total_collections, 2)
total_collections
```

**Alternative Example (With Sales Budget Provided):**

**Question:** A company collects 60% of sales in the month of sale, 30% in the following month, and 10% two months after sale. The sales budget shows: January $150,000, February $180,000, March $200,000. Calculate cash collections for March.

```python
# Collection pattern: 60% month 0, 30% month 1, 10% month 2
collection_rate_month_0 = 0.60
collection_rate_month_1 = 0.30
collection_rate_month_2 = 0.10

# Sales figures from budget (use actual provided values)
january_sales = 150000
february_sales = 180000
march_sales = 200000

# Calculate collections for March
collections_from_march = march_sales * collection_rate_month_0
collections_from_february = february_sales * collection_rate_month_1
collections_from_january = january_sales * collection_rate_month_2

# Total cash collections for March
total_collections = collections_from_march + collections_from_february + collections_from_january

# Round to 2 decimal places
total_collections = round(total_collections, 2)
total_collections
```

**Common Bugs to Avoid:**
- **Treating uncollected amount as total sales** — If given "$87,750 uncollected," this is NOT the original sales amount; divide by the uncollected percentage to find original sales
- **Missing collection periods** — If collection pattern spans 3 months, ensure you include collections from current month AND 2 prior months
- **Incorrect uncollected percentage** — Uncollected amount represents ALL remaining collections, not just one period (e.g., 35% = 20% + 15%, not just 20%)
- **Applying wrong collection rate** — Match each prior period to its correct collection rate based on timing (month 1 gets rate for "1 month after," month 2 gets rate for "2 months after")
- **Back-calculating when actual sales are provided** — If the question includes a sales budget table with actual sales figures, use those directly instead of deriving from AR
- **Forgetting current month collections** — Always include collections from the current month's sales (typically the largest component)

**CHECK Steps:**
- If collection pattern has N periods, verify you're collecting from N periods (including current)
- If question provides a sales budget table, verify you're using those actual sales figures, not back-calculating
- If given "uncollected amount" AND no actual sales figure for that period, verify: uncollected_amount / uncollected_rate = original_sales, then original_sales × collection_rate = expected collection
- Assert sum of all collection rates equals 100% (or 1.0)
- Verify each prior period's collection uses the correct time-offset rate
- Verify current month collections are included (current_sales × collection_rate_month_0)
## Pattern: Cash Flow Statement Source/Use Classification (Indirect Method)

**Description:** Classify balance sheet account changes as sources or uses of cash using indirect method logic, where the classification is INVERTED from intuitive thinking.

**When to Use:**
- Question asks whether an item is a "source" or "use" of cash
- Given beginning and ending balance sheet amounts
- Context is cash flow statement preparation or analysis
- Using indirect method reconciliation

**Procedure:**
1. **Calculate the change** — Ending balance - Beginning balance
2. **Apply indirect method classification rules:**
   - **For asset accounts (except cash):** Decrease = Source, Increase = Use
   - **For liability accounts:** Increase = Source, Decrease = Use
   - **For equity accounts:** Increase = Source, Decrease = Use
3. **Determine absolute amount** — Use absolute value of the change
4. **Return classification and amount**

**Worked Example:**

**Question:** Cash decreased from $48,180 to $45,815. Determine whether this is a source or use of cash, and the amount.

```python
# Given balance sheet data
beginning_cash = 48180
ending_cash = 45815

# Calculate change
cash_change = ending_cash - beginning_cash

# For cash account in indirect method reconciliation:
# A decrease in cash = Source (cash freed up from this account)
# An increase in cash = Use (cash tied up in this account)
# This is COUNTER-INTUITIVE but correct for indirect method

if cash_change < 0:
    classification = "Source"
else:
    classification = "Use"

# Amount is absolute value
amount = abs(cash_change)

# Return as tuple or formatted string
result = (classification, amount)
result
```

**Alternative Example (Non-Cash Asset):**

**Question:** Accounts Receivable increased from $120,000 to $135,000. Determine whether this is a source or use of cash, and the amount.

```python
# Given balance sheet data
beginning_ar = 120000
ending_ar = 135000

# Calculate change
ar_change = ending_ar - beginning_ar

# For asset accounts (other than cash):
# An increase = Use (cash tied up in the asset)
# A decrease = Source (cash freed up from the asset)

if ar_change > 0:
    classification = "Use"
else:
    classification = "Source"

# Amount is absolute value
amount = abs(ar_change)

result = (classification, amount)
result
```

**Common Bugs to Avoid:**
- **Using intuitive logic** — "Cash went down so we used it" is WRONG; in indirect method, cash decrease = source
- **Forgetting to take absolute value** — Amount should always be positive; classification carries the direction
- **Mixing direct and indirect method logic** — This pattern applies to indirect method reconciliation only
- **Incorrect asset/liability rules** — Asset increase = use, liability increase = source (opposite directions)

**CHECK Steps:**
- If account is cash and decreased, verify classification = "Source" (counter-intuitive but correct)
- If account is non-cash asset and increased, verify classification = "Use"
- If account is liability and increased, verify classification = "Source"
- Assert amount is always positive (use abs() function)
- Verify you're using indirect method context (not direct method cash flow)

---

SKILL_MD_ENTRY: | `financial_statement_analysis/cash_collections_and_flow_classification.md` | Financial Statement Analysis | Cash Collections and Cash Flow Classification | Multi-Period Cash Collections from Credit Sales, Cash Flow Statement Source/Use Classification (Indirect Method) |