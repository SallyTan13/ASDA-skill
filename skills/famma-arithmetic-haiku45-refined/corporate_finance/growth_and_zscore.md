# Corporate Finance — Growth Rate and Financial Health Metrics

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

## Pattern 1: Altman Z-Score Calculation

**Description:** Calculate the Altman Z-Score to predict bankruptcy risk. The standard 5-factor model is used for publicly traded manufacturing companies, while modified versions exist for private companies and non-manufacturers.

**When to Use:** 
- Question asks for "Z-score" or "Altman Z-score"
- Question provides balance sheet and income statement data
- **Default to standard 5-factor formula UNLESS question explicitly states "private company" or "modified Z-score"**
- If sales/revenue data is provided, use the standard formula

**Procedure:**
1. **Identify the correct formula variant:**
   - Standard (public manufacturing): Z = 1.2×X1 + 1.4×X2 + 3.3×X3 + 0.6×X4 + 1.0×X5
   - Modified (private): Z = 0.717×X1 + 0.847×X2 + 3.107×X3 + 0.420×X4 + 0.998
   - Non-manufacturer: Z = 6.56×X1 + 3.26×X2 + 6.72×X3 + 1.05×X4
2. **Calculate each component:**
   - X1 = Working Capital / Total Assets
   - X2 = Retained Earnings / Total Assets
   - X3 = EBIT / Total Assets
   - X4 = Market Value of Equity / Total Liabilities (or Book Value if private)
   - X5 = Sales / Total Assets
3. **Compute the weighted sum**
4. **Interpret:** Z > 2.99 (safe), 1.81 < Z < 2.99 (grey zone), Z < 1.81 (distress)

**Worked Example:**
**Question:** A company has total assets of $500,000, current assets of $200,000, current liabilities of $80,000, retained earnings of $150,000, EBIT of $75,000, market value of equity of $400,000, total liabilities of $100,000, and sales of $600,000. Calculate the Altman Z-Score.

```python
# Financial data
total_assets = 500000
current_assets = 200000
current_liabilities = 80000
retained_earnings = 150000
ebit = 75000
market_value_equity = 400000
total_liabilities = 100000
sales = 600000

# Calculate working capital
working_capital = current_assets - current_liabilities

# Calculate Z-Score components (standard 5-factor formula)
X1 = working_capital / total_assets
X2 = retained_earnings / total_assets
X3 = ebit / total_assets
X4 = market_value_equity / total_liabilities
X5 = sales / total_assets

# Standard Altman Z-Score formula
z_score = 1.2 * X1 + 1.4 * X2 + 3.3 * X3 + 0.6 * X4 + 1.0 * X5

z_score
```

**Common Bugs to Avoid:**
- Using modified formula when standard should apply (check if sales data is provided)
- Confusing book value with market value of equity for X4
- Using net income instead of EBIT for X3
- Forgetting to calculate working capital (current assets - current liabilities)
- Using total debt instead of total liabilities in X4 denominator

**CHECK Steps:**
- If sales/revenue is provided in the question, use standard 5-factor formula
- If question explicitly mentions "private company" AND no market value is given, consider modified formula
- Verify working capital = current assets - current liabilities (not just current assets)
- Ensure EBIT is used (not net income or operating income alone)

## Pattern 2: Internal Growth Rate vs. Sustainable Growth Rate

**Description:** Calculate the maximum growth rate a company can achieve under different financing constraints. Internal growth assumes NO external financing (no new debt or equity), while sustainable growth assumes NO new equity but debt increases to maintain constant debt-to-equity ratio.

**When to Use:**
- Question asks for "maximum growth without new equity"
- Question mentions "constant debt-equity ratio" → Use Sustainable Growth Rate
- Question mentions "no external financing" or "internal resources only" → Use Internal Growth Rate
- Question asks for "maximum sales increase" with financing constraints

**Procedure:**
1. **Identify the correct formula based on constraints:**
   - **Internal Growth Rate:** g = (ROA × b) / (1 - ROA × b)
     - Used when: NO new debt AND NO new equity
   - **Sustainable Growth Rate:** g = (ROE × b) / (1 - ROE × b)
     - Used when: NO new equity BUT debt maintains constant D/E ratio
2. **Calculate retention ratio (b):**
   - b = 1 - Dividend Payout Ratio
   - OR b = Retained Earnings / Net Income
3. **Calculate ROA or ROE:**
   - ROA = Net Income / Total Assets
   - ROE = Net Income / Total Equity
4. **Apply the appropriate formula**
5. **Calculate dollar increase:** Growth Rate × Current Sales

**Worked Example:**
**Question:** A company has net income of $50,000, total equity of $300,000, current sales of $400,000, and pays out 40% of earnings as dividends. The company maintains a constant debt-equity ratio. What is the maximum increase in sales?

```python
# Financial data
net_income = 50000
total_equity = 300000
current_sales = 400000
dividend_payout_ratio = 0.40

# Calculate retention ratio
retention_ratio = 1 - dividend_payout_ratio

# Calculate ROE (since constant D/E ratio maintained)
roe = net_income / total_equity

# Sustainable growth rate formula (constant D/E ratio)
sustainable_growth_rate = (roe * retention_ratio) / (1 - roe * retention_ratio)

# Maximum sales increase
max_sales_increase = sustainable_growth_rate * current_sales

max_sales_increase
```

**Worked Example 2 (Internal Growth):**
**Question:** A company has net income of $30,000, total assets of $500,000, current sales of $350,000, and retains 65% of earnings. The company will not use any external financing. What is the maximum sales increase?

```python
# Financial data
net_income = 30000
total_assets = 500000
current_sales = 350000
retention_ratio = 0.65

# Calculate ROA (since no external financing)
roa = net_income / total_assets

# Internal growth rate formula (no external financing)
internal_growth_rate = (roa * retention_ratio) / (1 - roa * retention_ratio)

# Maximum sales increase
max_sales_increase = internal_growth_rate * current_sales

max_sales_increase
```

**Common Bugs to Avoid:**
- Using internal growth formula when "constant debt-equity ratio" is mentioned (should use sustainable growth)
- Using sustainable growth formula when "no external financing" is stated (should use internal growth)
- Confusing ROA with ROE (ROA uses total assets, ROE uses equity)
- Forgetting to divide by (1 - ROE × b) or (1 - ROA × b) in the denominator
- Using dividend amount instead of dividend payout ratio
- Calculating growth rate but forgetting to multiply by current sales for dollar increase

**CHECK Steps:**
- If question mentions "constant debt-equity ratio" or "maintains D/E ratio", use ROE and sustainable growth formula
- If question mentions "no external financing" or "internal resources only", use ROA and internal growth formula
- Verify retention ratio + payout ratio = 1
- Ensure growth rate is positive (if negative, check ROE/ROA and retention calculations)
- Confirm final answer is in dollars if question asks for "increase in sales" (not just percentage)

---

## SKILL.md Entry

```
SKILL_MD_ENTRY: | `corporate_finance/growth_and_zscore.md` | Corporate Finance | Growth Rate and Financial Health Metrics | Altman Z-Score Calculation, Internal Growth Rate vs. Sustainable Growth Rate |
```