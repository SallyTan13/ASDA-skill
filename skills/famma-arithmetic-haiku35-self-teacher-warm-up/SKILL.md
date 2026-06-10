Here's the generated SKILL.md for arithmetic financial reasoning:

```markdown
---
name: famma-arithmetic-v1
description: Skills for arithmetic financial reasoning (PoT): concept confusion, visual evidence, domain patterns
version: 1.0
---

# Arithmetic Financial Reasoning Skills

This skill set provides comprehensive support for multi-step financial calculations across various domains, focusing on precise computational reasoning and pattern-based problem-solving.

Detailed skill files exist for multiple financial subfields and error types. These files can be precisely loaded using the `load_skill_file` tool with the specific file path.

### File Index

| File Path | Subfield | Error Type | Key Patterns |
|-----------|----------|------------|--------------|
| `fixed_income/missed_multi_step.md` | Fixed Income | Multi-Step Error | Bond Valuation, Term Structure Rate Extraction, Swap Valuation |
| `portfolio_management/missed_multi_step.md` | Portfolio Management | Multi-Step Error | Portfolio Return, Beta Decomposition, Time-Weighted Return |
| `corporate_finance/missed_multi_step.md` | Corporate Finance | Multi-Step Error | NPV Calculation, Merger Metrics, Cash Flow Decomposition |
| `derivatives/wrong_method_selection.md` | Derivatives | Method Selection | Risk-Neutral Valuation, Cross-Currency Valuation |
| `derivatives/missed_multi_step.md` | Derivatives | Multi-Step Error | Derivative Contract Mapping, Risk-Neutral Probability |
| `portfolio_management/wrong_method_selection.md` | Portfolio Management | Method Selection | Portfolio Variance, Risk-Adjusted Performance |
| `equity/missed_multi_step.md` | Equity | Multi-Step Error | Expected Value, Sharpe Ratio, Correlation Calculation |
| `financial_statement_analysis/missed_multi_step.md` | Financial Analysis | Multi-Step Error | Financial Ratio Calculation, Cash Flow Staging |
| `alternative_investments/missed_multi_step.md` | Alternative Investments | Multi-Step Error | DCF Calculation, Portfolio Return Weighting |
| `corporate_finance/concept_confusion.md` | Corporate Finance | Concept Confusion | Synergy Value Calculation, Interest Rate Conversion, Merger Valuation NPV, Cash Flow to Investors, Debt Valuation in Merger |
| `corporate_finance/unit_currency_percent.md` | Corporate Finance | Unit Currency Percent | Probabilistic Valuation with State-Dependent Outcomes, Interest Rate Calculation with Time Value of Money, Effective Annual Rate (EAR) Conversion |
| `corporate_finance/wrong_method_selection.md` | Corporate Finance | Wrong Method Selection | Dividend Growth Valuation Precision, Profitability Index Calculation, Altman Z-Score Precise Calculation, Effective Annual Rate (EAR) Conversion |
| `derivatives/concept_confusion.md` | Derivatives | Concept Confusion | Option Payoff Calculation, Risk-Neutral Price Movement Modeling, Multi-Currency Instrument Valuation, Interest Rate Swap Duration Calculation |
| `economics/missed_multi_step.md` | Economics | Missed Multi Step | Multi-Component Return Decomposition, Systematic Risk-Adjusted Comparative Analysis, Comprehensive Exchange Rate Forecasting, Holistic Balance Sheet Valuation |
| `equity/wrong_method_selection.md` | Equity | Wrong Method Selection | Discrete Probability Distribution Standard Deviation, Information Ratio Calculation |

---

## How to Use

**Step 1: Identify question type**  
Read the question and determine which financial subfield and error type it matches (e.g. by keywords, question format, or domain). Map to one or more entries in the File Index.

**Step 2: Request relevant skill file**  
Use the `load_skill_file` tool with the File Path from the File Index.

**Step 3: Apply pattern from the loaded file**  
1. Find the matching pattern in the skill file  
2. Follow the procedure and copy the code template structure  
3. Replace placeholders with values from the question  
4. Ensure the final line is an expression (not `print()`), so eval() can capture the result  

**Example**  
- *Question:* "Calculate the NPV of a project with initial investment of $100,000 and cash flows of $50,000 for three years at 10% discount rate"  
- *Step 1:* Corporate finance, multi-step calculation  
- *Step 2:* Request `corporate_finance/missed_multi_step.md`  
- *Step 3:* Apply "Multi-Step NPV Calculation Framework"

---

## Critical Code Constraints

**Your code MUST:**  
- End with a variable name or expression (for eval() to capture)  
- Put all imports at the top (e.g. `import numpy as np`)  
- Define every variable before use  
- Use explicit values from the question  

**Your code MUST NOT:**  
- Use `input()` or other interactive functions  
- Use `print()` as the last line (returns None)  
- Use undefined variables  
- Refer to example values without redefining them in code  

**Available libraries:**  
- `import math` — standard library  
- `import numpy as np` — numerical operations  
- `from scipy.stats import norm` — normal distribution  
- `from scipy.optimize import brentq` — root finding  

---

## When NOT to Use

- For problems requiring complex machine learning models
- When dealing with purely qualitative financial analysis
- For problems requiring extensive external data retrieval
- When the problem is more about strategic decision-making than arithmetic calculation
- For problems involving complex legal or regulatory interpretations
```