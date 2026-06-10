# Economics — Real Estate Expected Return with Cap Rate Changes

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

## Pattern: Real Estate Expected Return Decomposition

**Description:** Calculate the expected return on real estate investments by decomposing it into three components: (1) income return from current capitalization rate, (2) income growth from NOI (Net Operating Income) growth, and (3) capital appreciation from cap rate compression or expansion.

**When to Use:**
- Question asks for "expected return" on real estate or property investments
- Given current cap rate, expected/future cap rate, and NOI growth rate
- Context mentions "capitalization rate changes" or "cap rate compression/expansion"
- Need to estimate total return from income-producing real estate

**When NOT to Use:**
- Simple cap rate calculations without cap rate changes (use basic income return only)
- Direct property valuation questions (use NOI/cap rate formula)
- REIT equity returns (may use different models)

**Procedure:**
1. **Identify the three components:**
   - Current capitalization rate (income return)
   - NOI growth rate (income growth)
   - Cap rate change effect (capital appreciation/depreciation)

2. **Calculate cap rate change component:**
   - Formula: (Current Cap Rate - Expected Cap Rate) / Current Cap Rate
   - This represents the percentage change in property value from cap rate movement
   - Compression (cap rate decreases) → positive capital appreciation
   - Expansion (cap rate increases) → negative capital depreciation

3. **Sum all three components:**
   - Expected Return = Current Cap Rate + NOI Growth Rate + Cap Rate Change Component

4. **Convert to percentage if needed**

**Worked Example:**

**Question:** A real estate portfolio has a current capitalization rate of 5.2%, expected NOI growth of 3.0% annually, and the cap rate is expected to compress to 4.8% over the holding period. What is the expected annual return?

```python
# Define the three components
current_cap_rate = 0.052  # 5.2%
noi_growth_rate = 0.030   # 3.0%
expected_cap_rate = 0.048 # 4.8%

# Component 1: Income return (current cap rate)
income_return = current_cap_rate

# Component 2: Income growth (NOI growth)
income_growth = noi_growth_rate

# Component 3: Capital appreciation from cap rate compression
# Formula: (Current Cap Rate - Expected Cap Rate) / Current Cap Rate
cap_rate_change_component = (current_cap_rate - expected_cap_rate) / current_cap_rate

# Total expected return
expected_return = income_return + income_growth + cap_rate_change_component

# Convert to percentage
expected_return_percent = expected_return * 100

expected_return_percent
```

**Common Bugs to Avoid:**
- **Incomplete formula:** Only adding current cap rate + NOI growth without the cap rate change component (misses capital appreciation)
- **Wrong cap rate change formula:** Using simple subtraction (current - expected) instead of the ratio formula
- **Sign confusion:** Forgetting that cap rate compression (decrease) creates positive returns, expansion (increase) creates negative returns
- **Mixing up current vs expected:** Using expected cap rate as the income return instead of current cap rate
- **Double-counting:** Adding cap rate change as absolute difference when it should be relative to current cap rate

**CHECK Steps:**
- If cap rate decreases (compression), verify cap_rate_change_component > 0 (positive capital appreciation)
- If cap rate increases (expansion), verify cap_rate_change_component < 0 (negative capital depreciation)
- Assert that income_return uses current_cap_rate, not expected_cap_rate
- Verify all three components are included in final calculation
- If expected_return seems too low (close to just cap_rate + NOI_growth), check if cap rate change component was omitted

---

# Economics — Factor Model Arbitrage Detection

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

## Pattern: Single-Factor APT Arbitrage Opportunity

**Description:** Identify arbitrage opportunities in a factor model economy by comparing portfolios with identical factor exposures (betas) but different expected returns. In equilibrium, portfolios with the same systematic risk should have the same expected return.

**When to Use:**
- Question mentions "one-factor economy," "factor model," or "APT" (Arbitrage Pricing Theory)
- Given multiple portfolios/assets with factor loadings (betas) and expected returns
- Asked to identify "arbitrage opportunity" or check if "arbitrage exists"
- Portfolios have same factor exposure but different expected returns

**When NOT to Use:**
- CAPM equilibrium problems (use security market line analysis)
- Multi-factor models (requires different approach for multiple betas)
- Questions about constructing factor portfolios from scratch
- Market efficiency tests without specific factor structure

**Procedure:**
1. **Identify factor model structure:**
   - Extract factor loadings (betas) for each portfolio/asset
   - Extract expected returns for each portfolio/asset
   - Note: In factor models, E(R) = α + β₁F₁ + β₂F₂ + ... where F represents factor premiums

2. **Find portfolios with identical factor exposures:**
   - Compare betas across portfolios
   - Portfolios with same beta should have same expected return in equilibrium

3. **Check for return discrepancies:**
   - If two portfolios have identical betas but different expected returns → arbitrage exists
   - The arbitrage profit = difference in expected returns

4. **Construct arbitrage strategy:**
   - Long the portfolio with higher expected return
   - Short the portfolio with lower expected return (same amount)
   - Since betas match, factor risk cancels out (zero net factor exposure)
   - Profit = return differential with zero net investment and zero risk

**Worked Example:**

**Question:** In a one-factor economy, Portfolio A has a beta of 0.8 and expected return of 10%, while Portfolio B has a beta of 0.8 and expected return of 9.5%. Does an arbitrage opportunity exist? If so, what is the arbitrage profit?

```python
# Portfolio characteristics
beta_A = 0.8
expected_return_A = 0.10  # 10%

beta_B = 0.8
expected_return_B = 0.095  # 9.5%

# Check if betas are identical
betas_match = (beta_A == beta_B)

# Calculate return differential
return_differential = expected_return_A - expected_return_B

# Arbitrage exists if same beta but different returns
arbitrage_exists = betas_match and (return_differential != 0)

# Arbitrage strategy: Long A, Short B (equal amounts)
# Since betas match, net factor exposure = 0
# Profit per dollar invested
arbitrage_profit_percent = return_differential * 100 if arbitrage_exists else 0

arbitrage_profit_percent
```

**Common Bugs to Avoid:**
- **Using CAPM instead of factor model:** Applying security market line when question specifies "factor model" or "one-factor economy"
- **Ignoring identical betas:** Not recognizing that same factor exposure with different returns creates arbitrage
- **Incorrect arbitrage construction:** Forgetting to match position sizes or factor exposures
- **Missing the zero-risk property:** Not recognizing that matched betas create a risk-free arbitrage
- **Confusing with equilibrium pricing:** Trying to solve for risk-free rate or factor premium when question asks about arbitrage between existing portfolios

**CHECK Steps:**
- If betas are identical, verify that return_differential is calculated correctly
- Assert that arbitrage strategy has zero net factor exposure (long_beta - short_beta = 0)
- If arbitrage_exists = True, verify arbitrage_profit > 0 (should be positive for long higher-return portfolio)
- Check that the question mentions "factor model" or "one-factor economy" (not CAPM)
- Verify you're comparing portfolios, not trying to derive equilibrium parameters

---

## SKILL.md Entries:

```
SKILL_MD_ENTRY: | `economics/real_estate_expected_return.md` | Economics | Real Estate Expected Return | Real Estate Expected Return Decomposition |
```

```
SKILL_MD_ENTRY: | `economics/factor_model_arbitrage.md` | Economics | Factor Model Arbitrage | Single-Factor APT Arbitrage Opportunity |
```