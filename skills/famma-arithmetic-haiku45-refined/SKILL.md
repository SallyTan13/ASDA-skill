```markdown
---
name: famma-arithmetic-v1
description: Skills for arithmetic financial reasoning (PoT): concept confusion, visual evidence, domain patterns
version: 1.0
---

# Financial Arithmetic Reasoning Skills (Program of Thought)

This skill set provides code patterns and procedures for solving quantitative finance problems across corporate finance, derivatives, portfolio management, fixed income, equity, financial statement analysis, economics, and alternative investments. It addresses common error types including concept confusion, visual evidence misinterpretation, wrong method selection, code execution errors, unit/currency/percentage handling, and output format issues.

## Available Skill Files

Detailed skill files are organized by financial subfield and error type. Each file contains specific patterns with procedures, code templates, and worked examples. To access a skill file, use the `load_skill_file` tool with the exact file path from the File Index below.

### File Index

| File Path | Subfield | Error Type | Key Patterns |
|-----------|----------|------------|--------------|
| `common/visual_evidence.md` | Cross-subfield | Visual evidence | OCR_Ambiguity_Resolution_and_Sign_Detection, Table_Column_Alignment_and_Header_Mapping, Missing_Visual_Data_Detection_and_Handling, Numeric_Value_Range_Validation_for_OCR, State_Based_Portfolio_Return_Calculation, Tax_Lot_Accounting_Method_Implementation, Covariance_and_Correlation_from_State_Returns, CAPM_Alpha_and_Residual_Risk_Calculation, Multi_Column_Table_Parsing_with_Spatial_Awareness, OCR_Table_Dash_and_Missing_Value_Interpretation, Context_Driven_Cash_Flow_Sign_Convention, Missing_Parameter_Detection_in_Formula_Based_Problems, OCR_Percentage_Format_Ambiguity_Resolution, Binomial_Tree_Expected_Life_Calculation_for_ESO, Demonstrative_Reference_Disambiguation_in_Multi_Table_Context, Balance_Sheet_Equation_Validation_Before_Ratio_Analysis, Monte_Carlo_Percentile_Interpretation_for_Goal_Probability |
| `common/wrong_output_format.md` | Cross-subfield | Output format | Answer Option Mapping Verification, Cash Flow Sign Convention, Absolute Value vs Directional Change, Decimal Precision vs Integer Rounding, Currency Symbol Formatting, Final Expression Return (Not Print), Multiple Choice Option Tolerance Matching, Forward Rate vs Spot Rate Calculation, Zero-Coupon Bond Pricing with Continuous Compounding, Average Balance Calculation for Ratios, Verification Before Option Selection, Bond Price Quote Interpretation |
| `common/missed_constraints.md` | Cross-subfield | Constraint handling | Hedging Instrument Payoff Integration, Cross-Reference Constraint Retrieval, Missing Parameter Recognition, Exchange Ratio Calculation in Mergers, Merger NPV with Premium Extraction, Constraint Hierarchy and Override Rules, Perfect Markets Constraint Recognition, Leverage-Adjusted Portfolio Value, Multi-Factor Beta Decomposition, Annualization with Partial Period Adjustments |
| `corporate_finance/concept_confusion.md` | Corporate finance | Concept confusion | Merger Share Price with No Synergy, Deriving Required Return from P/E Ratio in Dividend Discount Model, Acquisition NPV with Synergy and Share Exchange, Risky Debt Valuation with State-Contingent Payoffs, Limited Liability and Equity as a Call Option, Geometric Mean for Multi-Period Returns, Stock Dividend Accounting Mechanics, Blocked Funds and Reinvestment in International Capital Budgeting, Credit Policy NPV as Perpetuity Valuation, New Equity Issuance and Dilution Effects on NPV, Synergy Value vs. Acquisition Premium in M&A, Merger Exchange Ratio and Post-Merger Ownership, Combined Firm Value in Independent State-Contingent Scenarios, Cash Flow from Assets Formula Structure, Target Required Return from Current Market Valuation, Stock-for-Stock Acquisition NPV with Synergy, Cash Flow to Creditors Calculation, Non-Conventional Cash Flow IRR Existence, Cash Flow from the Firm vs Net Change in Cash, Working Capital Based on Following Period Sales, Implied Volatility from Option Pricing (Merton Model), Homemade Leverage and Arbitrage in Modigliani-Miller Framework, Project NPV with Abandonment Options and Economic Life Optimization, Synergy Value Interpretation in Zero-Premium Mergers |
| `corporate_finance/code_execution_error.md` | Corporate finance | Code execution | IRR Multiple Root Detection with Polynomial Methods, Cash Flow to Creditors - Long-term Debt Only, IRR Calculation with Deprecated NumPy Functions, Cash Flow Sign Convention in IRR Problems, PoT Final Expression Requirement, Explicit vs. Derived Capital Expenditure, NPV-Based Project Acceptance Decision, Operating Cash Flow Calculation from Income Statement, Present Value of Future Cash Flows (No Initial Investment), Profitability Index with Multiple Outflows, Multi-Year Project IRR with Complex Cash Flows |
| `corporate_finance/wrong_method_selection.md` | Corporate finance | Method selection | Credit Policy NPV with Perpetuity Valuation, Gordon Growth Model with Market-Implied Discount Rate, Acquirer's Discount Rate in Acquisition Valuation, Acquisition NPV Calculation, Acquisition Gain with Growth Rate Adjustments, Altman Z-Score Variant Selection, Dividend vs Earnings in Valuation Models, Receivables Investment in Credit Policy |
| `derivatives/concept_confusion.md` | Derivatives | Concept confusion | Risk-Neutral Drift for Non-Traded Assets, Bond Futures Pricing with Cost-of-Carry, Option Delta at Expiration, Bear Put Spread Payoff Calculation, Equity Futures Rebalancing with Beta Adjustment, Employee Stock Option Expected Life, Implied Volatility with Jump Risk, Swaption Pricing with Annuity Factor, Quanto Derivative Currency Denomination, Coupon Bond Option Decomposition, Risky Debt Valuation from Firm Value, Heavy-Tailed Distribution Probability Regions, Risk-Neutral Probability Derivation in Jump Models, CDS Cash Flow Directionality, Binary vs Standard CDS Payoff Structure, Cross-Currency Basis Swap Mechanics, Straddle Breakeven vs Profitability Regions, Heavy-Tailed Distribution Probability Mass Allocation, Bond Option Strike Price Convention (Cash vs Quoted), Interest Rate Option Effective Borrowing Cost, Binomial Tree Model Consistency Verification, Forward Contract Pricing vs Valuation, American Option Early Exercise with Discrete Dividends |
| `derivatives/code_execution_error.md` | Derivatives | Code execution | Futures Hedge Ratio with Conversion Factor Adjustment, Black-Scholes Option Pricing with Correct Output Alignment, Rolling Futures Hedge Gain/Loss Calculation, CDS Valuation with Premium and Accrual Components, Breeden-Litzenberger Probability Density from Option Prices, Vasicek Model Bond Option Pricing, Option Time Value Decomposition, Commodity Futures Option Valuation (Black-76 Model), Forward and Futures Pricing with Continuous Compounding, Portfolio Insurance with Index Options - Contract Multiplier Adjustment |
| `derivatives/unit_currency_percent.md` | Derivatives | Unit/currency/percent | Precision Management in Multi-Step Exponential Discounting, Butterfly Spread Profit Calculation Mechanics, CDS Spread Output Format and Unit Conversion, Bond Accrued Interest Day-Count Precision, Futures Pricing with Carry Costs and Accrued Interest, Survival Probability Aggregation from Unconditional Default Probabilities, Semi-Annual Payment Adjustment in Spread Calculations, Interest Rate Collar Application to Floating Rate Loans, Conversion Factor Application in Futures Hedging |
| `derivatives/wrong_method_selection.md` | Derivatives | Method selection | Net Capex Growth Projection in DCF Models, Merton Model Implied Volatility Inversion, Interest Rate Swap Duration Calculation, Notional Principal Calculation for Duration Hedging, Currency Swap All-In Cost Calculation, Swaption Valuation for Future Borrowing |
| `derivatives/wrong_targets.md` | Derivatives | Target identification | Options Contract Scaling and Position Value, Multi-Component Output for Strategy Specification, Position Type Inference from Context, Question Reference Chain Resolution, Terminology Precision in Options Valuation |
| `portfolio_management/concept_confusion.md` | Portfolio management | Concept confusion | Efficient Frontier Identification, After-Tax Rebalancing Range with Transaction Costs, Futures Position Change with Contract Multiplier, Diversification and Idiosyncratic Risk Elimination, Systematic Risk as Variance Component, Effective Spread Calculation with Quoted Midpoint, Capital Allocation Line and Complete Portfolio, Confidence Index as Yield Ratio, Deduction Method for Foreign Tax, Delta-Hedged Portfolio Insurance, Arrival Cost Benchmark, Bond-Yield-Plus-Risk-Premium Method for Equity Returns, Total Execution Cost vs. Arrival Cost Distinction, ICAPM Beta Calculation from Sharpe Ratio, Arbitrage Detection with Portfolio Replication |
| `portfolio_management/code_execution_error.md` | Portfolio management | Code execution | Portfolio Variance and Standard Deviation with Explicit Weights, Covariance and Correlation Calculation from Probability Distributions, Multi-Factor Model Return Attribution, Brinson-Fachler Attribution Analysis, Black-Scholes-Merton Option Pricing with Dividends, Variable Return and Answer Verification, Table Data Extraction and Column Mapping, Multiple-Choice Answer Mapping and Validation, Answer Format Detection and Conversion, OCR Ambiguity Resolution with Robust Error Handling, EWMA Volatility and Covariance Updates |
| `portfolio_management/unit_currency_percent.md` | Portfolio management | Unit/currency/percent | Weighted Average vs. Scalar Multiplication in Portfolio Returns, Premature Rounding in Multi-Step Variance Calculations, Algebraic Errors in System of Linear Equations, Percentage-as-Decimal Output Convention Ambiguity, Portfolio Variance with Correlated Factors, Sign Convention in Share Repurchase Effects, Variance Unit Scaling (Basis Points vs. Decimal), Percentage Input Ambiguity in Tables, Real Return Calculation (Fisher Equation), Equal Weights Assumption Verification |
| `portfolio_management/wrong_method_selection.md` | Portfolio management | Method selection | Futures Contract Value Change Calculation, Information Ratio with CAPM Alpha, Bivariate GARCH Correlation Update, Contract-Based vs Portfolio-Based Calculations |
| `fixed_income/concept_confusion.md` | Fixed income | Concept confusion | Forward_Rate_to_Spot_Rate_Conversion, Sequential_Forward_Rate_Discounting, Forward_Rate_Table_Interpretation, Bond_Price_Evolution_with_Constant_Forward_Rates, Asset_Swap_Spread_Calculation, Credit_Spread_Return_Components, Condor_Butterfly_Positioning_for_Curvature, Conversion_Premium_Calculation, Zero_Coupon_Bond_Pricing_from_Forward_Rates, Expectations_Theory_Forward_Rate_Extraction, Interest_Rate_Conversion_APR_EAR, Swap_Rate_Decomposition_LIBOR_Forward, Forward_Contract_Pricing_with_Rate_Shifts |
| `fixed_income/unit_currency_percent.md` | Fixed income | Unit/currency/percent | Spot Rate vs Forward Rate Discounting, Coupon Payment Calculation (Par vs Market Price), Dollar Duration Rebalancing Algebra, Weighted Average Duration of Liabilities, Rate Compounding and Period Alignment, Output Format Verification (PoT-Specific), Zero-Coupon Bond Yield to Maturity Calculation |
| `equity/code_execution_error.md` | Equity | Code execution | Probability-Weighted Variance and Standard Deviation, Correlation Coefficient from Probability Distributions, Expected Return Calculation with Verification, Answer Validation Against Multiple Choice Options, Numerical Consistency Between Code and Explanation, Expected Value of Prices (Non-Return Calculations) |
| `equity/unit_currency_percent.md` | Equity | Unit/currency/percent | Beta-Adjusted Futures Contract Calculation, Decimal-to-Percentage Unit Consistency, Covariance and Correlation Calculation with Equal Probabilities, Financial Result Precision and Format |
| `financial_statement_analysis/concept_confusion.md` | Financial statement analysis | Concept confusion | Ambiguous_Ratio_Terminology_Resolution, Average_vs_Ending_Balance_Selection, Accounts_Receivable_Aging_Backward_Calculation, Lockbox_PV_Capitalization_vs_Daily_Benefit, Cash_Change_Source_Use_Inversion, Multi_Interpretation_Ratio_Systematic_Testing, Return_On_Equity_Balance_Convention, Collection_Period_Direct_vs_Turnover_Method, Operating_vs_Net_Profit_Context_Clues, Turnover_Ratio_Option_Matching, Bankruptcy_Liquidation_Priority_Waterfall |
| `financial_statement_analysis/code_execution_error.md` | Financial statement analysis | Code execution | Cash Flow Statement Source vs Use Classification, International Number Format Disambiguation, Per-Share Metric Calculation with Share Count Verification, Financial Statement Data Extraction with Unit Consistency |
| `economics/concept_confusion.md` | Economics | Concept confusion | Labor Force Component Double-Counting in GDP Growth Models, Dornbusch Overshooting vs Interest Rate Parity Confusion, Arbitrage Portfolio Identification from Problem Context, Human Capital Discount Rate Selection, Multi-Component Return Aggregation Context Sensitivity |
| `economics/wrong_method_selection.md` | Economics | Method selection | Real Estate Return Decomposition with Cap Rate Changes, Singer-Terhaar Model with Integration Weighting, Multi-Component Return Decomposition Verification, Basis Points and Percentage Conversion, Beta Calculation from Correlation and Volatility, Weighted Average vs. Additive Adjustment |
| `alternative_investments/concept_confusion.md` | Alternative investments | Concept confusion | Tax-Deferred Account Accrual Equivalent Return, Human Life Value with Employer Benefits, Mutually Exclusive Projects with Scale Differences, Endowment Spending Based on Trailing Average, Multi-Period Cash Flow Present Value with Growth, Asset Allocation Percentage Verification |
| `alternative_investments/code_execution_error.md` | Alternative investments | Code execution | Output Verification and Answer Extraction, Depreciation Tax Shield in Operating Cash Flow, Terminal Value with Asset Sale and Tax Effects, Abandonment Option NPV Comparison |
| `derivatives/futures_rebalancing_roc_valuation.md` | Derivatives | Futures Contract Adjustment, DCF Valuation | Asset Allocation Rebalancing with Risk-Adjusted Futures, Two-Stage DCF Valuation with Return on Capital Constraints |
| `economics/real_estate_expected_return_cap_rate.md` | Real Estate | Expected Return with Cap Rate Changes | Cap rate compression/expansion, NOI growth, total return decomposition |
| `derivatives/merton_model_debt_valuation.md` | Derivatives | Merton Model Debt Valuation, Terminal Value with ROC Constraints, Option Position Inference | Risky Debt Valuation Using Merton Model, Terminal Value with Return on Capital Constraints, Option Position Inference from Context |
| `corporate_finance/growth_and_zscore.md` | Corporate Finance | Growth Rate and Financial Health Metrics | Altman Z-Score Calculation, Internal Growth Rate vs. Sustainable Growth Rate |

## How to Use

**Step 1: Identify question type**  
Read the question carefully and determine:
- Financial subfield (corporate finance, derivatives, portfolio management, fixed income, equity, financial statement analysis, economics, alternative investments)
- Error type likely to occur (concept confusion, visual evidence, code execution, unit/currency/percent, method selection, output format, constraint handling)
- Keywords or question structure that match patterns in the File Index

**Step 2: Request relevant skill file(s)**  
Use the `load_skill_file` tool with the exact File Path from the File Index table. You may request multiple files if the question spans multiple error types or subfields.

**Step 3: Apply pattern from the loaded file**  
1. Scan the loaded skill file for the pattern that best matches your question
2. Read the pattern's procedure section to understand the conceptual approach
3. Copy the code template structure from the pattern
4. Replace all placeholders with actual values from the question
5. Ensure the final line is a variable name or expression (NOT `print()`) so `eval()` can capture the result
6. Verify your answer against multiple-choice options if provided

**Example**  
- **Question:** "Based on Exhibit 2, which portfolio lies on the efficient frontier? A) Portfolio X, B) Portfolio Y, C) Portfolio Z"
- **Step 1:** Subfield = portfolio management; Error type = visual evidence (chart reading) + concept confusion (efficient frontier definition)
- **Step 2:** Request `common/visual_evidence.md` and `portfolio_management/concept_confusion.md`
- **Step 3:** Apply "Multi_Column_Table_Parsing_with_Spatial_Awareness" to extract portfolio returns and standard deviations from Exhibit 2, then apply "Efficient Frontier Identification" pattern to check mean-variance dominance. Code ends with `answer = "B"` (not `print("B")`).

## Critical Code Constraints (ALWAYS FOLLOW)

**Your code MUST:**  
- End with a variable name or expression (for `eval()` to capture the result)
- Put all imports at the top (e.g. `import numpy as np`, `from scipy.stats import norm`)
- Define every variable before use with explicit values from the question
- Use consistent units throughout (convert percentages to decimals, align time periods)
- Include intermediate verification steps for multi-step calculations

**Your code MUST NOT:**  
- Use `input()` or other interactive functions
- Use `print()` as the last line (this returns `None` instead of the answer)
- Reference undefined variables or assume values not given in the question
- Use example values from the pattern without redefining them for the current question
- Mix units (e.g. annual rates with monthly periods) without explicit conversion

**Available libraries:**  
- `import math` — standard mathematical functions (sqrt, exp, log, etc.)
- `import numpy as np` — numerical operations, arrays, linear algebra
- `from scipy.stats import norm` — normal distribution CDF/PDF (for Black-Scholes, VaR, etc.)
- `from scipy.optimize import brentq, fsolve` — root finding (for IRR, implied volatility, etc.)
- `from scipy.optimize import minimize` — optimization (for portfolio problems)

## When NOT to Use

- **Qualitative questions** — If the question asks for conceptual explanations, regulatory interpretations, or ethical judgments without numerical calculation, these skills do not apply.
- **Pure formula lookup** — If the question only requires stating a formula without computation (e.g. "What is the formula for WACC?"), use conceptual knowledge instead.
- **Data unavailable** — If critical numerical inputs are missing and cannot be derived from the question or exhibits, flag the missing data rather than assuming values.
- **Non-financial domains** — These patterns are specific to finance; do not apply them to physics, engineering, or other quantitative domains.
- **Symbolic math required** — If the question asks for algebraic derivation or proof rather than numerical answer, these computational patterns are insufficient.

```