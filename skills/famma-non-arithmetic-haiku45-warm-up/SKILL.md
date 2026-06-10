```yaml
---
name: famma-non-arithmetic-v1
description: Skills for non-arithmetic financial reasoning covering concept confusion, visual evidence interpretation, and domain-specific patterns across portfolio management, derivatives, fixed income, equity, alternatives, economics, and corporate finance
version: 1.0
---
```

# Financial Non-Arithmetic Reasoning Skills

This skill set addresses **conceptual errors, visual evidence misinterpretation, and domain-specific reasoning patterns** in financial analysis. It covers seven major subfields and common cross-cutting error types.

## Available Skill Files

You have access to detailed skill files for each financial subfield. **Request files as needed** using the `load_skill_file` tool.

### File Index

| File Path | Subfield | Error Type | Key Patterns |
|-----------|----------|------------|--------------|
| `common/visual_evidence.md` | Cross-subfield | Visual evidence misread | Column-to-Data Alignment in Tables, Order Book Depth and Sequential Execution Logic, Numerical Proximity Matching in Multiple Choice, Complete Table Scanning for Optimization, Multi-Image Evidence Integration, Context-Level vs. Item-Level Interpretation, Visual Dispersion Assessment in Scatter Plots, Cost Basis Extraction and Loss Recognition, Bloomberg Terminal Date Notation Decoding, OCR vs. Visual Diagram Conflict Resolution, Financial Terminal Field Systematic Scanning, Table Sign Convention and Cash Flow Direction |
| `common/missed_constraints.md` | Cross-subfield | Missed constraints | IPS_Policy_Limits_Constraint, Missing_Critical_Parameter_Recognition, Event_Timing_And_Prospective_Application, Tax_Status_Constraint_Recognition |
| `portfolio_management/concept_confusion.md` | Portfolio management | Concept confusion | Price Movement Direction in Trade Execution, Tax Efficiency and Embedded Gains Analysis, Security Pricing Direction vs Return Relationship in CAPM, Arbitrage Existence in Single-Index Models, Implementation Shortfall Components for Trader Performance, Opportunity Cost in Trade Execution, Hurdle Rate Bias in Project Selection, Credit Spread Interpretation for Tactical Allocation, Efficient Frontier Dominance Testing, Goals-Based Allocation Institutional Application, GIPS Composite Construction Requirements, IPS Statement Appropriateness vs Temporal Stability, Multi-Stage Time Horizon Definition, Favorable vs Unfavorable Execution Relative to Benchmarks, Embedded Gains and Tax Liability for New Investors, High-Water Mark Fee Impact Timing, Heuristic vs Optimization Terminology, Returns-Based Benchmark Definition, Structural Inefficiency Repeatability Conditions, Asset Class Specification vs Performance Evaluation, Leveraged Recapitalization vs Shareholder Risk Mitigation, ASC 715 Pension Asset Recognition and Service Cost Treatment, Limit Order Execution Mechanics and Price Constraints, High-Touch vs Algorithmic Execution for Exchange-Traded Derivatives, GIPS Verification Requirements vs Compliance Claims, Mean-Variance Dominance Definition, Asynchronous Trading Effect on Correlation Estimates, Counterparty Risk in Equity Monetization Strategies, Ex-Post Alpha Measurement in CAPM Framework, Factor Attribution for Value Creation Opportunities, Risk Attribution Approach Selection for Factor-Timing Strategies, CAPM Validity and Portfolio Possibility, Systematic Risk Measurement via Beta Calculation, Security Selection Attribution with Portfolio Weights, Loss Aversion vs Mental Accounting in Disposition Effect, Asymmetric Performance Fees and Risk-Taking Incentives, Semi-Strong EMH and Post-Event CAR Interpretation, Behavioral Investor Type Classification in Behavioral Alpha Framework, Drawdown Duration Interpretation for Recovery Assessment, GIPS Private Equity Valuation Hierarchy Standards, Brinson-Fachler Allocation Effect Directional Logic, Custom Benchmark Investability and Practical Replicability |
| `portfolio_management/unit_currency_percent.md` | Portfolio management | Unit/currency/percent errors | Time-Scale Conversion in Stochastic Processes, Present Value of Annuity Due with Deferred Target Date, Percentage-Decimal Unit Consistency in Variance Calculations, Arithmetic Verification in Multi-Step Financial Calculations, Confidence Maintenance in Valid Algebraic Derivations, Tax-Adjusted Liquidity Calculation with Capital Gains |
| `fixed_income/concept_confusion.md` | Fixed income | Concept confusion | Interest Rate Parity and Currency Hedging Decisions, Immunization Structural Requirements vs Duration Matching, Benchmark Selection Criteria vs Market Views, Duration Effects vs Convexity Effects in Yield Changes, Swap Direction and Duration Impact, Options Asymmetry and Hedging Objectives, Tracking Error Sources in Fixed Income, Rolling Yield vs Leveraged Portfolio Returns, Credit Deterioration and Optimal Positioning, Liability Type Classification by Certainty Dimensions, Expected Excess Return Under Stable vs Stressed Credit Conditions, Structural Bond Features and Interest Rate Environments, Hedged vs Unhedged Currency Return Definitions, Callable Bond Structural Analysis Accuracy, Hedged Return Calculation Using Interest Rate Parity, Floating-Rate Note Effective Maturity and Yield Calculation, Callable Bond Preference and Interest Rate Environments |
| `equity/concept_confusion.md` | Equity | Concept confusion | Hypothesis Testing Framework in Manager Selection, Top-Down vs Bottom-Up Investment Strategy Classification, Investment Style Classification via Valuation Metrics, Index Construction Methods and Factor Model Assumptions, Performance Attribution as Descriptive vs Evaluative Tool, Hedge Ratio Risk: Minimum Variance vs One-to-One, Investment Vehicle Selection by Investor Type and Scale, Active Risk Changes from Paired Trades, Core-Satellite Strategy Benchmark Alignment, Bond Covenant Payments and Stockholder Indifference, Alpha-Beta Separation vs Core-Satellite Strategies, Index Return Calculation by Weighting Scheme, Manager Selection Error Type Identification via Null Hypothesis, Fundamental vs Quantitative Management Style Classification, Specialist Inventory Management and Order Book Imbalance, Activist Investor Stake Size and Regulatory Thresholds |
| `equity/unit_currency_percent.md` | Equity | Unit/currency/percent errors | Price-Weighted Index Divisor Adjustment After Stock Splits, Arithmetic Self-Contradiction and Verification Failure, Decimal Precision in Squared Terms and Products |
| `equity/wrong_method_selection.md` | Equity | Wrong method selection | Portfolio Return Calculation by Index Weighting Method, Factor Contribution to Portfolio Variance in Multi-Factor Models, Portfolio Tracking Error Aggregation from Multiple Managers, Portfolio Alpha Aggregation from Multiple Managers, Simultaneous Multi-Criteria Portfolio Goal Assessment |
| `derivatives/concept_confusion.md` | Derivatives | Concept confusion | Hedging Instrument Type vs. Hedging Objective, Currency Hedging Mechanics for Foreign Investments, Swap Directionality for Exposure Management, Interest Rate Swap Impact on Market Value vs. Cash Flow Risk, Covered Call vs. Protective Put Floor Establishment, Short Option Gamma Sign, Payer vs. Receiver Swaption Definitions, Market Price of Risk Under Numeraire Changes, Complete Hedging Requires Offsetting All Risk Components, Compound Option Put-Call Parity Structure, Short Put Delta Sign and Directional Exposure, Independent Evaluation of Multi-Part Derivative Claims |
| `derivatives/unit_currency_percent.md` | Derivatives | Unit/currency/percent errors | Multi-Step Binomial Tree Arithmetic Verification, Forward Price Calculation with Coupon Adjustment, Duration-Based Swap Notional Verification, Conditional Expectation Path Probability Calculation, Final Answer Transcription Verification |
| `derivatives/wrong_method_selection.md` | Derivatives | Wrong method selection | Futures Beta Adjustment Formula, Effective Beta Verification from Realized Returns, Futures Notional Exposure vs. Cash Investment, Incremental vs. Total Contracts for Portfolio Adjustment |
| `alternative_investments/concept_confusion.md` | Alternative investments | Concept confusion | Spending_Flexibility_Risk_Capacity_in_Annuities, Incremental_IRR_Necessity_Conditions, Primitive_vs_Derivative_Asset_Classification, Equity_Hedge_Strategy_Market_Condition_Matching, Probate_Exposure_by_Transfer_Mechanism, Benchmark_Bias_Types_in_Alternative_Investments, Portfolio_Diversification_Marginal_Contribution_Analysis, Human_Capital_Relative_Value_Career_Progression, Risk_Based_Approach_Diversification_Assessment, Private_Equity_Capital_Structure_Exit_Scenarios, Suitability_Concern_Contextual_Identification, Rebalancing_Band_Width_Volatility_Matching, Private_Equity_Exit_Strategy_Return_Realization |
| `economics/concept_confusion.md` | Economics | Concept confusion | Business Cycle Phase and Equity Return Timing, Growth Trend Adjustment by Market Development Status, International Finance Trilemma and Monetary Policy Independence, Currency Risk and Bond Yield Direction Under Peg Stress, GDP Growth vs. Equity Returns Causality, Tobin's Q Directional Interpretation, Real Yield Convergence Across Countries, Currency Appreciation Expectations and Relative Bond Yields, Top-Down vs. Bottom-Up Cyclical Turn Detection, Post-Recession Forecast Optimism Comparison, Yardeni vs. Fed Model Risk Premium Measurement, Yardeni vs. Fed Model Required Return Assumptions, Earnings Growth Rate Measurement Consistency Across Models, Discount Rate vs. Growth Rate Estimation Difficulty in Developing Markets, Corporate Profit Trends vs. GDP Growth Consistency, Economic Data Accuracy Challenges in Developing Markets, Top-Down and Bottom-Up Convergence Expectation |
| `corporate_finance/concept_confusion.md` | Corporate finance | Concept confusion | Earnings_Dilution_vs_Value_Dilution, Incremental_IRR_Decision_Rule_Application, Equity_as_Residual_Claim_in_Leverage, Debt_Market_Value_in_Distress, Cash_Flow_to_Stockholders_Comprehensive_Measure |
| `corporate_finance/wrong_targets.md` | Corporate finance | Wrong targets | Reference-Dependent Question Interpretation, Qualitative vs. Quantitative Question Targets, Enterprise Value vs. Equity Value Disambiguation, NPV Decision Rule to Binary Answer Mapping, Debt Value in Default Scenarios |
| `alternative_investments/wrong_targets.md` | Alternative Investments | Wrong Targets | Missing Context Detection, Sequential Multi-Part Question Tracking, Core Value Proposition Identification, Stakeholder-Specific Concern Mapping, Policy Mechanism vs. Policy Outcome Distinction |
| `common/wrong_output_format.md` | Common | Wrong Output Format | Answer-Explanation Alignment Failure, Calculated-vs-Selected Answer Mismatch, Verbosity Mismatch with Ground Truth Format |
| `derivatives/wrong_targets.md` | Derivatives | Wrong Targets | Option Type Inference from Economic Context, Compound Option Target Disambiguation, Perspective Identification in Options Scenarios, Specific Strike Price Selection from Context |
| `portfolio_management/wrong_method_selection.md` | Portfolio Management | Wrong Method Selection | Underdetermined System Recognition in Multi-Asset CAPM, Multi-Method Beta Calculation with CAPM Consistency Check, State-Based Return Calculation as Market Proxy |
| `portfolio_management/wrong_targets.md` | Portfolio Management | Wrong Targets | Question Scope Calibration, Empirical vs Theoretical Question Distinction, Notation Disambiguation in Context, Table Cell Spatial Indexing, Single vs Multiple Value Resolution |

## How to Use

### Step 1: Identify the Question Type
Read the question and determine:
- **Which financial subfield?** (portfolio management, derivatives, fixed income, equity, alternatives, economics, corporate finance)
- **What type of error is likely?** (concept confusion, visual evidence, missed constraints, unit errors, wrong method, wrong target)

### Step 2: Request the Relevant Skill File
Use the `load_skill_file` tool to request the appropriate file based on the File Index above.

### Step 3: Apply the Pattern
1. Find the matching pattern in the loaded skill file
2. Follow the reasoning steps provided in the pattern
3. Verify your answer against the pattern's key insights and common error modes

### Example

**Question**: "Based on Exhibit 2, which portfolio lies on the efficient frontier?"

**Step 1**: This is a **portfolio management** question involving **visual evidence** (reading a chart/table).

**Step 2**: Request two files:
- `common/visual_evidence.md` for systematic chart/table reading patterns
- `portfolio_management/concept_confusion.md` for efficient frontier conceptual understanding

**Step 3**: 
1. Apply the "Complete Table Scanning for Optimization" pattern from `visual_evidence.md` to extract all portfolio risk-return coordinates accurately
2. Apply the "Mean-Variance Dominance Definition" pattern from `concept_confusion.md` to identify which portfolios are dominated
3. Verify that the selected portfolio has no other portfolio with both higher return AND lower risk

## When NOT to Use

- **Pure arithmetic calculations** without conceptual ambiguity (use standard calculation methods)
- **Straightforward formula application** where the formula choice is obvious
- **Questions with complete, unambiguous information** requiring only mechanical computation
- **Simple fact recall** without reasoning or interpretation requirements
- **Questions where visual evidence is clear and unambiguous** with no potential for misreading