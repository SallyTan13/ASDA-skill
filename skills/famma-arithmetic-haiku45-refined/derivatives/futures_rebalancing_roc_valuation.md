# Derivatives — Futures Contract Adjustment for Portfolio Rebalancing

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

## Pattern: Asset Allocation Rebalancing with Risk-Adjusted Futures

**Description:** When rebalancing a portfolio by reducing one asset class and increasing another using futures contracts, you must adjust for risk characteristics (beta for equities, duration for bonds) to match the economic exposure being transferred. A simple dollar-for-dollar calculation will produce incorrect hedge ratios.

**When to Use:**
- Portfolio rebalancing involves selling/buying futures to shift allocation
- Question provides beta values for equity positions and futures
- Question provides duration values for bond positions and futures
- Need to calculate number of futures contracts to buy or sell
- The goal is to match risk exposure, not just notional value

**Procedure:**

1. **Identify the dollar amount being reallocated** from one asset class to another
2. **For equity futures rebalancing:**
   - Formula: `Number of contracts = (Dollar change × Portfolio beta) / (Futures price × Futures beta)`
   - If reducing equity exposure: sell contracts (positive number means sell)
   - If increasing equity exposure: buy contracts (negative number means buy)
3. **For bond futures rebalancing:**
   - Formula: `Number of contracts = (Dollar change × Portfolio duration) / (Futures price × Futures duration)`
   - If reducing bond exposure: sell contracts
   - If increasing bond exposure: buy contracts
4. **Round to nearest whole number** (cannot trade fractional contracts)
5. **Verify direction:** Selling equity futures reduces equity exposure; buying bond futures increases bond exposure

**Worked Example:**

**Question:** A portfolio manager wants to shift $30 million from equities to bonds. The equity portfolio has a beta of 1.20, and the S&P 500 futures (beta 1.05) are trading at $350,000 per contract. The bond portfolio has a duration of 6.5 years, and Treasury futures (duration 5.2 years) are trading at $125,000 per contract. How many equity futures should be sold and bond futures purchased?

```python
# Step 1: Define the rebalancing amount
dollar_shift = 30_000_000  # $30 million

# Step 2: Calculate equity futures to sell (reducing equity exposure)
equity_portfolio_beta = 1.20
equity_futures_beta = 1.05
equity_futures_price = 350_000

equity_contracts = (dollar_shift * equity_portfolio_beta) / (equity_futures_price * equity_futures_beta)
equity_contracts_rounded = round(equity_contracts)

# Step 3: Calculate bond futures to buy (increasing bond exposure)
bond_portfolio_duration = 6.5
bond_futures_duration = 5.2
bond_futures_price = 125_000

bond_contracts = (dollar_shift * bond_portfolio_duration) / (bond_futures_price * bond_futures_duration)
bond_contracts_rounded = round(bond_contracts)

# Result: (contracts to sell, contracts to buy)
result = (equity_contracts_rounded, bond_contracts_rounded)
result
```

**Common Bugs to Avoid:**
- **Bug 1: Dollar-for-dollar calculation** — Using `dollar_shift / futures_price` ignores beta/duration mismatch and produces incorrect hedge ratios
- **Bug 2: Forgetting to adjust for portfolio risk characteristics** — Must multiply by portfolio beta/duration in numerator
- **Bug 3: Forgetting to adjust for futures risk characteristics** — Must multiply by futures beta/duration in denominator
- **Bug 4: Wrong direction** — Selling equity futures reduces equity exposure; buying bond futures increases bond exposure
- **Bug 5: Using notional value instead of price** — Use the actual futures contract price, not the underlying index value

**CHECK Steps:**
- If rebalancing FROM equities TO bonds, verify equity contracts > 0 (sell) and bond contracts > 0 (buy)
- If portfolio beta > futures beta, verify equity contracts > (dollar_shift / futures_price)
- If portfolio duration > futures duration, verify bond contracts > (dollar_shift / futures_price)
- Assert `equity_contracts * equity_futures_price * equity_futures_beta ≈ dollar_shift * equity_portfolio_beta` (within rounding)
- Assert `bond_contracts * bond_futures_price * bond_futures_duration ≈ dollar_shift * bond_portfolio_duration` (within rounding)

---

## Pattern: Two-Stage DCF Valuation with Return on Capital Constraints

**Description:** In two-stage DCF models, when a return on capital (ROC) constraint is specified for the terminal period, it determines the reinvestment rate through the relationship: Reinvestment Rate = g / ROC. This affects the terminal free cash flow calculation, as only the portion of NOPAT not reinvested becomes free cash flow.

**When to Use:**
- Two-stage or multi-stage DCF valuation problem
- Question specifies a return on capital (ROC) or return on invested capital (ROIC) for the stable/terminal period
- Need to calculate terminal value or enterprise value
- The stable growth rate (g) is given for the terminal period

**Procedure:**

1. **High-growth period (Years 1 to N):**
   - Project EBIT/NOPAT using stated growth rates
   - Calculate FCFF = NOPAT - Net Investment (or use given FCFF projections)
   - Discount each year's FCFF to present value

2. **Terminal period (Year N+1 onwards):**
   - Calculate terminal NOPAT = Last year NOPAT × (1 + g)
   - **Key step:** Calculate reinvestment rate = g / ROC
   - Calculate terminal FCFF = Terminal NOPAT × (1 - Reinvestment rate) = Terminal NOPAT × (1 - g/ROC)
   - Calculate terminal value = Terminal FCFF / (WACC - g)
   - Discount terminal value to present value

3. **Enterprise value = PV(High-growth FCFFs) + PV(Terminal value)**

4. **Firm value = Enterprise value + Cash - Debt** (if calculating equity value)

**Worked Example:**

**Question:** A firm has NOPAT of $500 million and is expected to grow at 15% for 3 years. After year 3, growth stabilizes at 4% with return on capital of 12%. WACC is 9%. What is the enterprise value?

```python
# Step 1: High-growth period projections
nopat_0 = 500  # million
high_growth_rate = 0.15
stable_growth_rate = 0.04
roc_terminal = 0.12
wacc = 0.09
high_growth_years = 3

# Assume reinvestment rate in high-growth = g/ROC = 15%/15% = 100% (all reinvested)
# This means FCFF = 0 during high growth (common simplification)
# Or use given FCFF if provided

# For this example, assume FCFF given or calculated separately
# Let's assume reinvestment rate = 60% during high growth
reinvestment_high = 0.60

pv_high_growth = 0
nopat = nopat_0
for year in range(1, high_growth_years + 1):
    nopat = nopat * (1 + high_growth_rate)
    fcff = nopat * (1 - reinvestment_high)
    pv_high_growth += fcff / ((1 + wacc) ** year)

# Step 2: Terminal period
nopat_terminal = nopat * (1 + stable_growth_rate)

# Key calculation: reinvestment rate constrained by ROC
reinvestment_terminal = stable_growth_rate / roc_terminal

# Terminal FCFF
fcff_terminal = nopat_terminal * (1 - reinvestment_terminal)

# Terminal value at end of year 3
terminal_value = fcff_terminal / (wacc - stable_growth_rate)

# PV of terminal value
pv_terminal = terminal_value / ((1 + wacc) ** high_growth_years)

# Step 3: Enterprise value
enterprise_value = pv_high_growth + pv_terminal
enterprise_value
```

**Common Bugs to Avoid:**
- **Bug 1: Ignoring ROC constraint** — Simply using Terminal FCFF = Last FCFF × (1 + g) without adjusting for reinvestment
- **Bug 2: Wrong reinvestment rate** — Using high-growth reinvestment rate in terminal period instead of g/ROC
- **Bug 3: Applying ROC to wrong period** — ROC constraint typically applies to stable/terminal period, not high-growth
- **Bug 4: Confusing NOPAT with FCFF** — NOPAT is before reinvestment; FCFF is after reinvestment
- **Bug 5: Wrong terminal value timing** — Terminal value is at END of last high-growth year, needs appropriate discounting

**CHECK Steps:**
- If ROC = 15% and g = 5%, verify reinvestment rate = 5%/15% = 33.33%
- If reinvestment rate = 33.33%, verify FCFF = 66.67% of NOPAT
- Assert `reinvestment_rate = stable_growth_rate / roc_terminal`
- Assert `terminal_value > 0` (if WACC > g, which must be true for perpetuity)
- If ROC < g, the model is invalid (cannot sustain growth above return on capital indefinitely)

---

SKILL_MD_ENTRY: | `derivatives/futures_rebalancing_roc_valuation.md` | Derivatives | Futures Contract Adjustment, DCF Valuation | Asset Allocation Rebalancing with Risk-Adjusted Futures, Two-Stage DCF Valuation with Return on Capital Constraints |