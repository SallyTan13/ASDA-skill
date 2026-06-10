# SKILL PATTERNS FOR ALTERNATIVE INVESTMENTS - CODE EXECUTION ERRORS

## Pattern: IRR Calculation with Proper Library Import and Cash Flow Sign Convention

**Description:** IRR calculations fail when numpy_financial or scipy libraries are not imported, or when initial investment cash flows are not represented as negative values. The code must properly structure cash flow arrays with correct signs before applying IRR functions.

**When to Use:** Questions asking to calculate or compare Internal Rate of Return (IRR) for investment projects, especially when selecting between mutually exclusive projects based on IRR criteria.

**Procedure:**
1. Formula: IRR is the discount rate r where NPV = 0, i.e., Σ(CF_t / (1+r)^t) = 0
2. Import required library (numpy_financial preferred, or scipy.optimize as fallback)
3. Structure cash flows as list/array with initial investment as NEGATIVE value
4. Apply IRR function to each project's cash flow array
5. Compare IRR values and return the appropriate result based on question requirements

**Code Example:**

**Scenario:** Two projects with different cash flows. Project Alpha: initial cost $500,000, returns $200,000, $250,000, $180,000 over 3 years. Project Beta: initial cost $300,000, returns $120,000, $150,000, $100,000 over 3 years. Which has higher IRR?

**Correct Code:**
```python
import numpy_financial as npf

# Define cash flows with negative initial investment
cash_flows_alpha = [-500000, 200000, 250000, 180000]
cash_flows_beta = [-300000, 120000, 150000, 100000]

# Calculate IRR for each project
irr_alpha = npf.irr(cash_flows_alpha)
irr_beta = npf.irr(cash_flows_beta)

# Compare and return project name
result = "Alpha" if irr_alpha > irr_beta else "Beta"
result
```

**Common Bugs to Avoid:**
- Missing import statement (numpy_financial or scipy.optimize)
- Initial investment as positive instead of negative (violates cash flow convention)
- Using print() instead of expression on last line in PoT mode
- Returning numeric IRR value when question asks for project name/decision
- Incorrect array indexing or structure when extracting data from tables

---

## Pattern: NPV Comparison for Mutually Exclusive Projects with Named Output

**Description:** When comparing NPV of mutually exclusive projects, the code must calculate NPV for EACH project separately, compare the values, and return the PROJECT NAME (string) corresponding to the highest NPV, not the numeric NPV value itself.

**When to Use:** Questions asking "which project should be taken/accepted based on NPV" when multiple mutually exclusive investment options are presented with their cash flows and a discount rate.

**Procedure:**
1. Formula: NPV = Σ(CF_t / (1+r)^t) where r is discount rate, CF_t is cash flow at time t
2. Extract discount rate and cash flows for each project from the problem
3. Calculate NPV for each project using the discount rate (initial investment as negative)
4. Compare NPV values across all projects
5. Return the NAME/IDENTIFIER of the project with highest NPV as a string

**Code Example:**

**Scenario:** Project X has cash flows [-800000, 400000, 350000, 300000] and Project Y has cash flows [-600000, 250000, 280000, 320000]. Discount rate is 12%. Which project should be selected?

**Correct Code:**
```python
# Define parameters
discount_rate = 0.12
cash_flows_x = [-800000, 400000, 350000, 300000]
cash_flows_y = [-600000, 250000, 280000, 320000]

# Calculate NPV for Project X
npv_x = sum(cf / (1 + discount_rate)**t for t, cf in enumerate(cash_flows_x))

# Calculate NPV for Project Y
npv_y = sum(cf / (1 + discount_rate)**t for t, cf in enumerate(cash_flows_y))

# Return project name with higher NPV
selected_project = "Project X" if npv_x > npv_y else "Project Y"
selected_project
```

**Common Bugs to Avoid:**
- Returning numeric NPV value instead of project name when question asks "which project"
- Calculating only one project's NPV instead of comparing all options
- Using print() statement instead of expression for final output
- Forgetting to make initial investment negative in cash flow array
- Incorrect discount factor calculation (using wrong exponent or base)

---

## Pattern: Robust Cash Flow Array Construction from Tabular Data

**Description:** When extracting cash flows from tables (especially OCR text), explicitly construct separate arrays for each project with proper indexing, ensuring Year 0 represents initial investment (negative) and subsequent years represent returns (positive).

**When to Use:** Questions presenting investment project data in tabular format with multiple years and multiple projects, requiring extraction and structuring of cash flows before financial calculations.

**Procedure:**
1. Identify the structure: rows (years) vs columns (projects) in the table
2. Extract Year 0 cash flow as initial investment (convert to negative)
3. Extract subsequent year cash flows as positive returns
4. Create separate named arrays/lists for each project
5. Verify array length matches number of time periods
6. Apply financial calculations (NPV, IRR, etc.) to structured arrays

**Code Example:**

**Scenario:** Table shows Project M and Project N. Year 0: M=$400,000, N=$250,000 (investments). Year 1: M=$180,000, N=$110,000. Year 2: M=$220,000, N=$140,000. Calculate NPV at 9% discount rate for both.

**Correct Code:**
```python
# Extract and structure cash flows with correct signs
# Year 0 is investment (negative), Years 1-2 are returns (positive)
project_m_flows = [-400000, 180000, 220000]
project_n_flows = [-250000, 110000, 140000]

discount_rate = 0.09

# Calculate NPV for Project M
npv_m = sum(cf / (1 + discount_rate)**t for t, cf in enumerate(project_m_flows))

# Calculate NPV for Project N
npv_n = sum(cf / (1 + discount_rate)**t for t, cf in enumerate(project_n_flows))

# Return both NPVs for comparison
{"Project M NPV": npv_m, "Project N NPV": npv_n}
```

**Common Bugs to Avoid:**
- Mixing up row/column orientation when extracting from tables
- Forgetting to negate Year 0 investment values
- Hardcoding array indices without verifying table structure
- Misaligning cash flows with time periods (off-by-one errors)
- Not handling currency symbols or comma separators in numeric strings

---

## Pattern: Decision Output Format Matching Question Requirements

**Description:** Financial decision questions require different output formats: some need numeric values, others need categorical decisions (project names, "accept/reject"), and others need boolean comparisons. The final line must match the expected answer type.

**When to Use:** Any capital budgeting or investment selection question where the answer is a decision or recommendation rather than a pure numeric calculation.

**Procedure:**
1. Parse the question to identify output type: numeric value, project name, yes/no decision, or comparison
2. Perform all necessary calculations (NPV, IRR, payback period, etc.)
3. Apply decision rule (e.g., highest NPV, IRR > hurdle rate, payback < threshold)
4. Format output to match question type (string for names, boolean for yes/no, numeric for values)
5. Ensure last line is an expression (not print) that evaluates to the answer

**Code Example:**

**Scenario:** Three questions about the same project with cash flows [-150000, 60000, 70000, 50000] and 10% discount rate. Q1: "What is the NPV?" Q2: "Should the project be accepted?" Q3: "Which has higher NPV, this project or doing nothing?"

**Correct Code:**
```python
# Common calculation
cash_flows = [-150000, 60000, 70000, 50000]
discount_rate = 0.10
npv = sum(cf / (1 + discount_rate)**t for t, cf in enumerate(cash_flows))

# Q1: Numeric output
# npv

# Q2: Decision output (accept if NPV > 0)
# "accept" if npv > 0 else "reject"

# Q3: Comparison output
# "project" if npv > 0 else "do nothing"
```

**Common Bugs to Avoid:**
- Using print() instead of expression for final answer
- Returning numeric value when question asks for categorical decision
- Returning project name when question asks for numeric metric
- Case sensitivity in string outputs (check if answer expects lowercase/uppercase)
- Not handling tie-breaking rules when values are equal