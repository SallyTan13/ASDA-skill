# Portfolio Management — Capital Allocation and Tax Methods

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

## Pattern 1: Capital Allocation Between Risky and Risk-Free Assets

**Description:** Calculate the allocation proportions when a client invests in both a risky portfolio and a risk-free asset (T-bills). The client's complete portfolio consists of a weight in the risk-free asset and the remaining weight proportionally distributed across the risky assets according to their weights in the risky portfolio.

**When to Use:**
- Question asks for "investment proportions" or "client portfolio allocation" including T-bills
- Given a risky portfolio with asset weights and need to find complete portfolio weights
- Context mentions both risky assets and risk-free assets (T-bills, Treasury securities)
- NOT when matching portfolio volatility to market (M² measure)

**Procedure:**
1. Identify the weight allocated to the risk-free asset (y_rf) - may be given directly or calculated
2. Calculate the weight in the risky portfolio: y_risky = 1 - y_rf
3. For each risky asset i with weight w_i in the risky portfolio:
   - Client's allocation to asset i = y_risky × w_i
4. Verify all weights sum to 100%

**Worked Example:**
**Question:** A client allocates 25% to T-bills. The risky portfolio consists of: Stock A (30%), Stock B (45%), Stock C (25%). What are the investment proportions in the client's complete portfolio?

```python
# Step 1: Identify allocation to risk-free asset
weight_tbills = 0.25

# Step 2: Calculate allocation to risky portfolio
weight_risky_portfolio = 1 - weight_tbills  # 0.75

# Step 3: Risky asset weights in the risky portfolio
risky_weights = {
    'Stock_A': 0.30,
    'Stock_B': 0.45,
    'Stock_C': 0.25
}

# Step 4: Calculate client's allocation to each risky asset
client_allocation = {}
client_allocation['T_bills'] = weight_tbills

for asset, weight_in_risky in risky_weights.items():
    client_allocation[asset] = weight_risky_portfolio * weight_in_risky

# Convert to percentages for output
result = {k: round(v * 100, 1) for k, v in client_allocation.items()}
result
# {'T_bills': 25.0, 'Stock_A': 22.5, 'Stock_B': 33.8, 'Stock_C': 18.8}
```

**Common Bugs to Avoid:**
- Using M² measure or volatility matching when no market standard deviation is provided
- Hallucinating parameters (like market volatility) that don't exist in the context
- Forgetting to multiply risky asset weights by the risky portfolio allocation
- Not including the risk-free asset in the final allocation

**CHECK Steps:**
- Verify all weights sum to 1.0 (or 100%)
- If risky portfolio weights are given, ensure they sum to 1.0 before applying
- Assert that weight_risky_portfolio = 1 - weight_tbills
- Check that each risky asset weight = (1 - weight_rf) × weight_in_risky_portfolio

---

## Pattern 2: International Tax Methods (Exemption, Deduction, Credit)

**Description:** Calculate effective tax rates under different international taxation systems when income is earned in multiple jurisdictions. Three main methods exist: exemption (only foreign tax applies), deduction (home country taxes worldwide income with foreign tax as deduction), and credit (home country taxes worldwide income with credit for foreign taxes paid).

**When to Use:**
- Question involves taxation of foreign-source income
- Multiple tax jurisdictions mentioned (home country and foreign country)
- Terms like "exemption method," "deduction method," or "credit method" appear
- Need to calculate effective tax rate on international income

**Procedure:**
1. Identify the taxation method (exemption, deduction, or credit)
2. Extract tax rates: home country rate (t_home) and foreign country rate (t_foreign)
3. Apply the appropriate formula:
   - **Exemption Method:** Effective rate = t_foreign (only foreign country taxes)
   - **Deduction Method:** Effective rate = t_foreign + t_home × (1 - t_foreign)
   - **Credit Method:** Effective rate = max(t_home, t_foreign)
4. Convert to percentage if needed

**Worked Example:**
**Question:** An investor faces a home country tax rate of 20% and a foreign country tax rate of 12%. Calculate the effective tax rate under: (a) exemption method, (b) deduction method, (c) credit method.

```python
# Step 1: Define tax rates
t_home = 0.20
t_foreign = 0.12

# Step 2: Calculate under each method

# (a) Exemption Method: Only foreign tax applies
exemption_rate = t_foreign

# (b) Deduction Method: Foreign tax paid first, then home country taxes the net
# Effective rate = t_foreign + t_home × (1 - t_foreign)
deduction_rate = t_foreign + t_home * (1 - t_foreign)

# (c) Credit Method: Home country taxes worldwide income but credits foreign tax
# Effective rate = max(t_home, t_foreign)
credit_rate = max(t_home, t_foreign)

# Convert to percentages
results = {
    'exemption': round(exemption_rate * 100, 1),
    'deduction': round(deduction_rate * 100, 1),
    'credit': round(credit_rate * 100, 1)
}
results
# {'exemption': 12.0, 'deduction': 27.6, 'credit': 20.0}
```

**Common Bugs to Avoid:**
- Confusing deduction method with credit method (deduction can result in higher total tax)
- Under deduction method, simply adding the two rates (should be: t_foreign + t_home × (1 - t_foreign))
- Under credit method, adding rates instead of taking the maximum
- Syntax errors like missing assignment operators or malformed variable names

**CHECK Steps:**
- For exemption method: verify effective rate equals foreign rate only
- For deduction method: verify effective rate ≥ max(t_home, t_foreign) when both rates are positive
- For credit method: verify effective rate = max(t_home, t_foreign)
- Assert all tax rates are between 0 and 1 (or 0% and 100%)

---

## Pattern 3: Bond-Yield-Plus-Risk-Premium Method

**Description:** Estimate expected equity return by adding an equity risk premium to a government bond yield. This method uses the risk-free rate (proxied by government bonds like Treasury securities) as the base, NOT corporate bond yields.

**When to Use:**
- Question asks to estimate expected return using "bond-yield-plus-risk-premium method"
- Given both government bond yields and equity risk premiums
- Context includes Treasury yields, government bond yields, or risk-free rates
- May also have corporate bond yields as distractors

**Procedure:**
1. Identify the government bond yield (Treasury, sovereign bonds) - this is the base rate
2. Identify the equity risk premium (may be given directly or need to be calculated)
3. Calculate: Expected Equity Return = Government Bond Yield + Equity Risk Premium
4. DO NOT use corporate bond yields (AA, BBB, etc.) as the base

**Worked Example:**
**Question:** The 10-year Treasury yield is 4.2%, the AA corporate bond yield is 5.8%, and the equity risk premium is 7.5%. Using the bond-yield-plus-risk-premium method, estimate the expected equity return.

```python
# Step 1: Identify the correct base yield (government bond, NOT corporate)
treasury_yield = 0.042  # 10-year Treasury
corporate_yield = 0.058  # AA corporate bond (DO NOT USE)

# Step 2: Identify equity risk premium
equity_risk_premium = 0.075

# Step 3: Calculate expected equity return
# CORRECT: Use government bond yield as base
expected_return = treasury_yield + equity_risk_premium

# Convert to percentage
result = round(expected_return * 100, 1)
result
# 11.7
```

**Common Bugs to Avoid:**
- Using corporate bond yield instead of government bond yield as the base (most common error)
- Confusing this method with CAPM or other equity return estimation methods
- Adding risk premium to the wrong yield when multiple yields are provided
- Not converting percentages correctly

**CHECK Steps:**
- Verify the base yield is from government bonds (Treasury, sovereign), not corporate bonds
- If multiple bond yields given, identify which is the government/risk-free rate
- Assert expected_return = government_bond_yield + equity_risk_premium
- Check that equity risk premium is positive (typically 3-10%)

---

SKILL_MD_ENTRY: | `portfolio_management/capital_allocation_tax_methods.md` | Portfolio Management | Capital Allocation and Tax Methods | Capital Allocation Between Risky and Risk-Free Assets, International Tax Methods (Exemption/Deduction/Credit), Bond-Yield-Plus-Risk-Premium Method |