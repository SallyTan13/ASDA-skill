# Corporate Finance — Sustainable Growth and Financial Constraint Analysis

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

## Pattern 1: Sustainable Growth Rate with Financing Constraints

**Description:** Calculate the maximum growth rate a company can achieve while maintaining its current financial structure without issuing new equity. This pattern uses the internal growth formula when debt-equity ratio is held constant.

**When to Use:**
- Question asks for "maximum sustainable growth" or "maximum increase in sales"
- Constraints include "no new equity issued" or "without external equity financing"
- May mention "maintaining debt-equity ratio" or "constant capital structure"
- Given: ROE (or components to calculate it), retention rate/payout ratio, current sales

**Procedure:**
1. Calculate ROE if not given directly (Net Income / Total Equity)
2. Calculate retention rate: b = 1 - Payout Ratio (or use given retention rate)
3. Apply sustainable growth formula: SGR = (ROE × b) / (1 - ROE × b)
4. Calculate maximum sales increase: ΔSales = Current Sales × SGR
5. Verify that SGR < 1 (if SGR ≥ 1, the formula breaks down - indicates unlimited growth potential)

**Worked Example:**
**Question:** A company has current sales of $50,000, ROE of 15%, and pays out 40% of earnings as dividends. What is the maximum increase in sales sustainable without issuing new equity?

```python
# Given values
current_sales = 50000
roe = 0.15
payout_ratio = 0.40

# Step 1: Calculate retention rate
retention_rate = 1 - payout_ratio  # 0.60

# Step 2: Calculate sustainable growth rate
# Formula: SGR = (ROE × b) / (1 - ROE × b)
numerator = roe * retention_rate
sgr = numerator / (1 - numerator)

# Step 3: Calculate maximum sales increase
max_sales_increase = current_sales * sgr

# Result
max_sales_increase  # Should be approximately $4,736.84
```

**Common Bugs to Avoid:**
- ❌ Using incorrect formula: SGR = ROE × b × (1 + D/E) — this is for different growth scenarios
- ❌ Using simple multiplication: ΔSales = ROE × Retention × Sales — ignores compounding constraint
- ❌ Forgetting to convert payout ratio to retention rate (b = 1 - payout ratio)
- ❌ Confusing internal growth rate (no external financing) with sustainable growth rate (no equity financing)

**CHECK Steps:**
- Verify retention_rate = 1 - payout_ratio (should be between 0 and 1)
- Verify SGR is positive and typically less than 0.30 (30%) for most companies
- If SGR > 1.0, recheck formula application — this suggests the company can grow infinitely, which is unrealistic
- Cross-check: Higher ROE or higher retention should increase sustainable growth

---

## Pattern 2: Altman Z-Score Variant Selection

**Description:** Calculate bankruptcy prediction scores using the appropriate Altman Z-Score formula variant based on company type (public manufacturing, private, non-manufacturing/service).

**When to Use:**
- Question asks for "Z-score" or "Altman Z-score"
- Given financial statement data (working capital, retained earnings, EBIT, equity, assets, liabilities, sales)
- Need to assess financial distress or bankruptcy risk
- Company type matters: public vs private, manufacturing vs service

**Procedure:**
1. Identify company type from context (public/private, manufacturing/service/emerging market)
2. Select appropriate formula variant:
   - **Original Z-Score** (public manufacturing): 5 variables including market value of equity
   - **Z'-Score** (private manufacturing): 4 variables, uses book value of equity
   - **Z''-Score** (non-manufacturing/service): 4 variables, excludes sales/assets ratio
3. Calculate required financial ratios from balance sheet and income statement
4. Apply coefficients specific to the chosen variant
5. Interpret: Z > 2.99 (safe), 1.81 < Z < 2.99 (grey zone), Z < 1.81 (distress zone)

**Worked Example:**
**Question:** Calculate the Z'-score for a private manufacturing company with: Total Assets = $8,000, Current Assets = $3,500, Current Liabilities = $1,800, Retained Earnings = $2,200, EBIT = $950, Total Equity (book value) = $4,500, Total Liabilities = $3,500.

```python
# Given financial data for private company
total_assets = 8000
current_assets = 3500
current_liabilities = 1800
retained_earnings = 2200
ebit = 950
book_value_equity = 4500
total_liabilities = 3500

# Step 1: Calculate working capital
working_capital = current_assets - current_liabilities

# Step 2: Calculate financial ratios
x1 = working_capital / total_assets  # Working Capital / Total Assets
x2 = retained_earnings / total_assets  # Retained Earnings / Total Assets
x3 = ebit / total_assets  # EBIT / Total Assets
x4 = book_value_equity / total_liabilities  # Book Value Equity / Total Liabilities

# Step 3: Apply Z'-Score formula for private companies
# Z' = 0.717*X1 + 0.847*X2 + 3.107*X3 + 0.420*X4 + 0.998
z_prime_score = (0.717 * x1) + (0.847 * x2) + (3.107 * x3) + (0.420 * x4) + 0.998

# Result
z_prime_score  # Should be approximately 2.85
```

**Formula Variants Reference:**

**Original Z-Score (Public Manufacturing):**
```
Z = 1.2*X1 + 1.4*X2 + 3.3*X3 + 0.6*X4 + 1.0*X5
X1 = Working Capital / Total Assets
X2 = Retained Earnings / Total Assets
X3 = EBIT / Total Assets
X4 = Market Value of Equity / Total Liabilities
X5 = Sales / Total Assets
```

**Z'-Score (Private Companies):**
```
Z' = 0.717*X1 + 0.847*X2 + 3.107*X3 + 0.420*X4 + 0.998
X1 = Working Capital / Total Assets
X2 = Retained Earnings / Total Assets
X3 = EBIT / Total Assets
X4 = Book Value of Equity / Total Liabilities
(Note: No X5 sales component, uses book value not market value)
```

**Z''-Score (Non-Manufacturing/Service/Emerging Markets):**
```
Z'' = 6.56*X1 + 3.26*X2 + 6.72*X3 + 1.05*X4
X1 = Working Capital / Total Assets
X2 = Retained Earnings / Total Assets
X3 = EBIT / Total Assets
X4 = Book Value of Equity / Total Liabilities
(Note: Different coefficients, no constant term)
```

**Common Bugs to Avoid:**
- ❌ Using wrong formula variant (e.g., public company formula for private company)
- ❌ Missing the constant term (0.998 in Z'-Score)
- ❌ Using market value of equity when book value is required (or vice versa)
- ❌ Calculating only 4 components when 5 are needed (original Z-Score)
- ❌ Using incorrect coefficients (they differ significantly across variants)

**CHECK Steps:**
- If company is private or no market value given, use Z'-Score (book value variant)
- If company is service/non-manufacturing, use Z''-Score (no sales component)
- Verify all ratios are calculated with consistent denominators (usually Total Assets or Total Liabilities)
- Z-scores typically range from -4 to +8; values outside this suggest calculation error
- If Sales data is missing, cannot use original Z-Score (must use Z' or Z'')

---

## Pattern 3: Merger Synergy Valuation Conceptual Analysis

**Description:** Determine the implied synergy value or minimum synergy required to justify a merger/acquisition based on the premium paid over market value. This is often a conceptual question about valuation principles rather than pure calculation.

**When to Use:**
- Question asks "what must [party] believe/feel about synergy value"
- Question asks to "explain how" a decision can be reconciled
- Given: acquisition price, target's market value, and need to justify the premium
- Expected answer is conceptual (e.g., "the market value" or "synergy must exceed premium")
- Keywords: "synergy," "merger," "acquisition premium," "justify," "reconcile"

**Procedure:**
1. Identify the acquisition premium: Premium = Offer Price - Target Market Value
2. Apply synergy principle: For a rational acquisition, Synergy Value ≥ Premium Paid
3. Determine what the acquirer must believe:
   - Minimum synergy = Premium paid
   - If question asks for "the value," answer is often the target's market value (as synergy baseline)
   - If question asks "can this be justified," check if stated/implied synergy ≥ premium
4. For conceptual questions, return the principle rather than calculating a specific number

**Worked Example:**
**Question:** Company A offers $85 million for Company B, which has a current market value of $70 million. What minimum synergy value must Company A believe exists to justify this acquisition?

```python
# Given values
offer_price = 85_000_000
target_market_value = 70_000_000

# Step 1: Calculate premium paid
premium = offer_price - target_market_value

# Step 2: Minimum synergy to justify acquisition
# For rational acquisition: Synergy Value >= Premium
minimum_synergy = premium

# Step 3: Interpretation
# The acquirer must believe synergy is at least equal to the premium
# Otherwise, they are overpaying (destroying shareholder value)

# Result
minimum_synergy  # $15,000,000
```

**Conceptual Framework:**
- **Synergy Sources:** Cost savings, revenue enhancements, tax benefits, market power
- **Valuation Principle:** Combined Value = Value(A) + Value(B) + Synergy - Premium
- **Rationality Check:** If Synergy < Premium, the acquisition destroys value for the acquirer
- **Market Value Baseline:** The target's market value represents its standalone value; synergy is the incremental value from combination

**Common Bugs to Avoid:**
- ❌ Attempting complex NPV calculations when question asks for conceptual understanding
- ❌ Returning numerical zero or near-zero when answer should be "the market value" (conceptual)
- ❌ Confusing synergy value with combined company value
- ❌ Ignoring that questions asking "what must [party] believe" expect qualitative reasoning

**CHECK Steps:**
- If question uses "believe," "feel," "must think," or "explain how" → likely conceptual
- If ground truth answer is text (not a number) → return conceptual explanation
- Verify: Synergy value should be positive and typically 10-30% of target value for realistic deals
- If calculated synergy is negative or near-zero, reconsider whether this is a conceptual question

---

SKILL_MD_ENTRY: | `corporate_finance/sustainable_growth_and_constraints.md` | Corporate Finance | Sustainable Growth and Financial Constraint Analysis | Sustainable Growth Rate with Financing Constraints, Altman Z-Score Variant Selection, Merger Synergy Valuation Conceptual Analysis |