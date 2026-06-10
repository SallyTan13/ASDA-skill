# Real Estate — Expected Return with Cap Rate Changes

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

## Pattern: Real Estate Expected Return with Cap Rate Compression/Expansion

**Description:** Calculate the expected total return for real estate investments when both Net Operating Income (NOI) growth and cap rate changes occur. The total return consists of income return (current cap rate) plus capital appreciation. Cap rate changes create a multiplicative effect on property values because the same NOI capitalized at a different rate produces a different property value.

**When to Use:**
- Question provides current cap rate and expected future cap rate
- Question provides expected NOI growth rate
- Question asks for total expected return or holding period return
- Real estate property valuation context with income-producing properties

**Procedure:**
1. **Identify the income component**: Current cap rate represents the income return
2. **Calculate the capital appreciation component**:
   - Property value changes due to both NOI growth AND cap rate changes
   - Formula: Capital Appreciation = (1 + NOI_growth) / (End_cap_rate / Beginning_cap_rate) - 1
   - This accounts for the multiplicative effect: higher NOI capitalized at a different rate
3. **Calculate total expected return**: Income Return + Capital Appreciation
4. **Alternative formula**: Expected Return = Beginning_cap_rate + [(1 + NOI_growth) × (Beginning_cap_rate / End_cap_rate) - 1]

**Worked Example:**

**Question:** An industrial property has a current cap rate of 5.2%. The NOI is expected to grow by 3.0% over the next year. Market cap rates for similar properties are expected to compress to 4.9%. What is the expected total return?

```python
# Define the given parameters
current_cap_rate = 0.052  # Current capitalization rate (income return)
noi_growth = 0.030  # Expected NOI growth rate
end_cap_rate = 0.049  # Expected future cap rate

# Step 1: Income return component
income_return = current_cap_rate

# Step 2: Capital appreciation component
# When cap rates compress (decrease), property values increase
# The property value appreciation accounts for both NOI growth and cap rate change
cap_rate_ratio = end_cap_rate / current_cap_rate
capital_appreciation = (1 + noi_growth) / cap_rate_ratio - 1

# Step 3: Total expected return
expected_return = income_return + capital_appreciation

# Convert to percentage for final answer
expected_return_pct = expected_return * 100

# Return the result
expected_return_pct
```

**Alternative Calculation Method:**
```python
# Same inputs
current_cap_rate = 0.052
noi_growth = 0.030
end_cap_rate = 0.049

# Direct formula: R = cap_rate + [(1 + g) × (cap_0 / cap_1) - 1]
expected_return = current_cap_rate + ((1 + noi_growth) * (current_cap_rate / end_cap_rate) - 1)

expected_return_pct = expected_return * 100
expected_return_pct
```

**Common Bugs to Avoid:**
- **WRONG: Simple additive approach** — Do NOT calculate as: cap_rate + NOI_growth + cap_rate_change. This ignores the multiplicative effect of cap rate changes on property values.
- **WRONG: Ignoring cap rate direction** — Cap rate compression (decrease) increases property values; cap rate expansion (increase) decreases property values. The formula automatically handles this through the ratio.
- **WRONG: Using percentage points instead of rates** — If cap rate goes from 4.6% to 4.45%, the change is NOT -0.15 to add directly; use the ratio method (0.0445/0.046).
- **WRONG: Forgetting the income component** — Total return includes BOTH the current cap rate (income) AND the capital appreciation from NOI growth and cap rate changes.

**CHECK Steps:**
- If cap rates compress (decrease), verify that expected return > current cap rate + NOI growth (cap rate compression adds extra appreciation)
- If cap rates expand (increase), verify that expected return < current cap rate + NOI growth (cap rate expansion reduces total return)
- Assert that the capital appreciation component properly reflects the multiplicative relationship: `capital_appreciation ≈ (1 + noi_growth) / (end_cap_rate / beginning_cap_rate) - 1`
- Verify units: all rates should be in decimal form (0.05 not 5) before calculation, convert to percentage only for final answer
- Cross-check: If NOI growth = 0 and cap rates unchanged, expected return should equal current cap rate

---

**SKILL.md Entry:**

```
SKILL_MD_ENTRY: | `economics/real_estate_expected_return_cap_rate.md` | Real Estate | Expected Return with Cap Rate Changes | Cap rate compression/expansion, NOI growth, total return decomposition |
```