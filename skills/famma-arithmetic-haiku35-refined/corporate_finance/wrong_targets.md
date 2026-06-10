# SKILL PATTERNS FOR FINANCIAL DECISION-MAKING QUESTIONS (PoT Mode)

## Pattern: Binary Decision Output for Threshold Comparison

**Description:** Questions asking "should the company accept?" or "can the investor increase return?" require yes/no answers, not intermediate numerical calculations. The code must compute the decision metric, compare against the threshold, and return a boolean or categorical string.

**When to Use:** Questions containing "should accept/reject", "can increase", "is it worthwhile", or any phrasing requesting a recommendation based on comparing a calculated metric to a hurdle rate or alternative value.

**When NOT to Use:** 
- When the question asks for the numerical value itself (e.g., "What is the NPV?")
- When manual NPV calculation is required due to library limitations
- When the baseline already provides the correct numerical answer that can be interpreted

**Procedure:**
1. Formula: Decision = (Metric > Threshold) for maximization problems, or (Metric < Threshold) for minimization
2. Compute the decision metric (NPV, IRR, return difference, etc.) using the correct library function
3. **CRITICAL:** Use `numpy_financial.npv()` or manual calculation, NOT `numpy.npv()` (which doesn't exist)
4. Compare the metric to the given threshold or alternative
5. Return "Yes" or "No" (or True/False) as the final expression, NOT the intermediate numerical value

**Common Mistakes to Avoid:**
- **Using `np.npv()` instead of `npf.npv()` or manual calculation** — NumPy does not have an npv() function; use numpy_financial or calculate manually
- Returning the numerical metric (npv, irr) instead of the decision string
- Using print() instead of expression on last line
- Forgetting to implement the comparison logic (metric vs threshold)
- Incorrect comparison operator (using < when should use >)

**Code Example:**

**Scenario:** A project has cash flows of [-50000, 20000, 25000, 18000]. The required return is 11%. Should the project be accepted based on NPV rule?

**Correct Code (Option 1 - using numpy_financial):**
```python
import numpy as np
import numpy_financial as npf

# Cash flows: negative for outflows, positive for inflows
cash_flows = np.array([-50000, 20000, 25000, 18000])
required_return = 0.11

# Calculate NPV using numpy_financial
npv = npf.npv(required_return, cash_flows)

# Decision rule: Accept if NPV > 0
decision = "Yes" if npv > 0 else "No"

decision  # Return the decision, NOT npv
```

**Correct Code (Option 2 - manual calculation):**
```python
import numpy as np

# Cash flows: negative for outflows, positive for inflows
cash_flows = np.array([-50000, 20000, 25000, 18000])
required_return = 0.11

# Calculate NPV manually
npv = sum(cf / (1 + required_return)**t for t, cf in enumerate(cash_flows))

# Decision rule: Accept if NPV > 0
decision = "Yes" if npv > 0 else "No"

decision  # Return the decision, NOT npv
```

**Example (sanitized):**
> **Scenario:** Should a company accept a project with initial cost $100K and returns of $40K, $50K, $35K over 3 years at 12% discount rate?
> **Wrong approach:** Using `np.npv(0.12, cash_flows)` which causes execution failure because numpy.npv doesn't exist
> **Correct approach:** Import numpy_financial and use `npf.npv(0.12, cash_flows)` OR calculate NPV manually with discount formula, then compare to zero and return "Yes"/"No"
## Pattern: Mutually Exclusive Project Selection

**Description:** When choosing between mutually exclusive projects, the answer is the project name with the highest NPV (or other metric), not the NPV value itself. The code must compute metrics for ALL alternatives and return the categorical identifier of the best option.

**When to Use:** Questions asking "which project should you choose?", "which alternative is better?", or presenting multiple mutually exclusive investment options requiring selection of one.

**Procedure:**
1. Formula: Best_Project = argmax(NPV_i) for all projects i
2. Compute the decision metric (typically NPV) for each project separately
3. Compare all metrics and identify the maximum (or minimum for cost problems)
4. Return the project name/identifier as a string, NOT the numerical metric value

**Code Example:**

**Scenario:** Project Alpha has cash flows [-100000, 45000, 50000, 40000] and Project Beta has [-120000, 55000, 60000, 45000]. Both require 10% return. Which should be chosen?

**Correct Code:**
```python
import numpy as np

# Project cash flows
alpha_cf = np.array([-100000, 45000, 50000, 40000])
beta_cf = np.array([-120000, 55000, 60000, 45000])
discount_rate = 0.10

# Calculate NPV for each project
npv_alpha = np.npv(discount_rate, alpha_cf)
npv_beta = np.npv(discount_rate, beta_cf)

# Select project with highest NPV
if npv_alpha > npv_beta:
    selected_project = "Project Alpha"
else:
    selected_project = "Project Beta"

selected_project  # Return project name, NOT npv value
```

**Common Bugs to Avoid:**
- Returning max(npv_alpha, npv_beta) instead of the project identifier
- Computing only one project's NPV instead of all alternatives
- Using print() instead of expression for final answer
- Hardcoding project names from original question (use generic identifiers)

---

## Pattern: IRR Decision Rule Implementation

**Description:** IRR-based accept/reject decisions require computing the IRR, comparing it to the hurdle rate, and returning a categorical decision. The IRR itself is an intermediate value, not the answer.

**When to Use:** Questions stating "the company evaluates projects by applying the IRR rule" or "using IRR, should the project be accepted?" with a given discount/hurdle rate.

**Procedure:**
1. Formula: IRR is the rate r where NPV = Σ(CF_t / (1+r)^t) = 0
2. Compute IRR using numpy.irr or by solving NPV equation
3. Compare IRR to the hurdle rate: Accept if IRR > hurdle_rate
4. Return "Yes" or "No" based on comparison, NOT the IRR value

**Code Example:**

**Scenario:** A project has cash flows [-30000, 12000, 15000, 10000]. The hurdle rate is 8%. Using IRR rule, should it be accepted?

**Correct Code:**
```python
import numpy_financial as npf
import numpy as np

# Cash flows
cash_flows = np.array([-30000, 12000, 15000, 10000])
hurdle_rate = 0.08

# Calculate IRR
irr = npf.irr(cash_flows)

# IRR decision rule: Accept if IRR > hurdle rate
decision = "Yes" if irr > hurdle_rate else "No"

decision  # Return decision, NOT irr value
```

**Common Bugs to Avoid:**
- Returning the IRR percentage instead of accept/reject decision
- Using deprecated numpy.irr instead of numpy_financial.irr
- Forgetting to compare IRR to hurdle rate
- Incorrect comparison (using >= when context requires >)
- Not handling multiple IRR cases for non-conventional cash flows

---

## Pattern: Implied Value Inference from Transaction Terms

**Description:** Questions asking "what must [party] feel is the value of X?" require reverse-engineering the implicit assumption from transaction terms, not forward calculation. The answer is often a qualitative description of the valuation logic, not a single number.

**When to Use:** Questions containing "what must [party] believe", "what is the implied value", "explain how this can be reconciled", or asking to infer assumptions from observed transaction prices.

**Procedure:**
1. Formula: Implied_Synergy = Premium_Paid - Standalone_Value (for M&A contexts)
2. Calculate the total consideration paid in the transaction
3. Calculate the standalone market value of the target
4. Compute the premium/difference as the implied synergy or value assumption
5. Return a descriptive string explaining the valuation logic, not just the number

**Code Example:**

**Scenario:** Acquirer pays $500M for Target with standalone market value of $420M. What synergy value must Acquirer believe exists?

**Correct Code:**
```python
# Transaction terms
total_consideration = 500_000_000
target_standalone_value = 420_000_000

# Calculate implied synergy
implied_synergy = total_consideration - target_standalone_value

# The answer is the interpretation, not just the number
answer = f"At least ${implied_synergy:,.0f} in synergy value"

answer  # Return descriptive answer
```

**Common Bugs to Avoid:**
- Returning only the numerical difference without context
- Computing forward valuation instead of reverse-engineering the assumption
- Ignoring the "explain how reconciled" part of multi-part questions
- Not considering that answer may require qualitative reasoning beyond pure calculation
- Forgetting to account for all components of consideration (cash + stock)

---

## Pattern: Comparative Strategy Analysis with Constraints

**Description:** Questions asking "can investor increase return by switching strategies?" require computing returns for BOTH strategies under stated constraints (e.g., same initial cost), then comparing them to return a yes/no answer.

**When to Use:** Questions with "can [party] increase [metric] by", "which strategy yields higher", or comparing two investment approaches with explicit constraints on initial investment or leverage.

**Procedure:**
1. Formula: Strategy_A_Return vs Strategy_B_Return under constraint C
2. Calculate the return/payoff for the current strategy
3. Calculate the return/payoff for the alternative strategy, applying all constraints
4. Compare the two returns
5. Return "Yes" if alternative is better, "No" otherwise

**Code Example:**

**Scenario:** Investor can earn 5% on Strategy A with $100K investment. Strategy B requires $120K but earns 7%. If investor borrows $20K at 4% to make initial costs equal, can they increase dollar return with Strategy B?

**Correct Code:**
```python
# Strategy A (baseline)
investment_a = 100_000
return_rate_a = 0.05
dollar_return_a = investment_a * return_rate_a

# Strategy B (with borrowing to equalize initial cost)
investment_b = 120_000
return_rate_b = 0.07
borrowing = 20_000
borrowing_rate = 0.04

# Net return for Strategy B after interest expense
gross_return_b = investment_b * return_rate_b
interest_expense = borrowing * borrowing_rate
net_return_b = gross_return_b - interest_expense

# Compare strategies
can_increase = "Yes" if net_return_b > dollar_return_a else "No"

can_increase  # Return yes/no decision
```

**Common Bugs to Avoid:**
- Returning the dollar difference instead of yes/no answer
- Forgetting to apply the constraint (equal initial cost, same leverage, etc.)
- Computing only one strategy's return
- Not accounting for financing costs when borrowing is involved
- Comparing gross returns when net returns should be compared

---

## Pattern: Multi-Part Question Target Identification

**Description:** Complex questions may ask for calculations AND explanations. The final answer target must match what the question explicitly requests in its last sentence, which may be qualitative rather than quantitative.

**When to Use:** Questions with multiple sentences, especially those ending with "Explain how...", "What does this imply about...", or requesting interpretation after calculation.

**Procedure:**
1. Parse the question to identify the final requested output format
2. Perform all necessary intermediate calculations
3. If question asks for explanation/interpretation, formulate a descriptive answer
4. Return the answer in the format requested (number, decision, explanation, or project name)

**Code Example:**

**Scenario:** "Calculate the payback period. Does this meet the company's 3-year threshold? Explain why this metric may be misleading."

**Correct Code:**
```python
import numpy as np

# Cash flows
cash_flows = np.array([-100000, 35000, 40000, 45000, 30000])

# Calculate payback period
cumulative = 0
payback_period = 0
for i, cf in enumerate(cash_flows[1:], 1):
    cumulative += cf
    if cumulative >= abs(cash_flows[0]):
        payback_period = i
        break

# Check threshold
meets_threshold = "Yes" if payback_period <= 3 else "No"

# The question asks for explanation (last part)
explanation = f"Payback is {payback_period} years ({meets_threshold} to threshold). This metric ignores time value of money and cash flows beyond payback, potentially rejecting positive-NPV projects."

explanation  # Return the explanation, not just the number
```

**Common Bugs to Avoid:**
- Returning the first calculated value instead of the final requested output
- Ignoring the "explain" portion of multi-part questions
- Providing only quantitative answer when qualitative interpretation is requested
- Not reading the complete question to identify the true target