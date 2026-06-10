```markdown
---
name: famma-non-arithmetic-v1
description: Skills for non-arithmetic financial reasoning covering concept confusion, visual evidence interpretation, and domain-specific patterns
version: 1.0
---

# Financial Non-Arithmetic Reasoning Skills

This skill set addresses non-computational errors in financial analysis, including concept confusion, visual evidence misinterpretation, constraint violations, and target misidentification across all CFA exam topics.

## Available Skill Files

You have access to detailed skill files for each financial subfield. **Request files as needed** using the `load_skill_file` tool.

### File Index

| File Path | Subfield | Error Type | Key Patterns |
|-----------|----------|------------|--------------|
| `common/visual_evidence.md` | Cross-subfield | Visual evidence misread | OCR_Data_Reconstruction_and_Structured_Comparison, Multi_Image_Reference_Tracking, Portfolio_Context_Specific_Risk_Relevance, Visual_Scatter_Plot_Dispersion_Assessment, Bloomberg_Terminal_Field_Location_and_Missing_Data_Recognition, Date_Format_Truncation_and_Contextual_Year_Inference, Order_Book_Sequential_Liquidity_Consumption, Cash_Flow_Sign_Convention_from_Perspective_Keywords, Visual_Label_to_Answer_Choice_Mapping |
| `common/wrong_output_format.md` | Cross-subfield | Output format errors | Answer-Explanation Consistency Verification, Numerical Result to Option Letter Mapping |
| `common/missed_constraints.md` | Cross-subfield | Constraint violations | Policy Constraint Verification in Tactical Asset Allocation, Missing Parameter Detection for Formula Application, Probability-Weighted Statistics for Discrete Distributions, Capital Rationing with Indivisible Projects, Currency-Adjusted Returns in Tactical Asset Allocation |
| `portfolio_management/concept_confusion.md` | Portfolio management | Concept confusion | Directional Interpretation of Spread and Execution Metrics, Price-Return Inversion in CAPM Mispricing Analysis, Arrival Price Algorithm Purpose and Urgency Characteristics, Arbitrage vs. CAPM Mispricing Distinction, Implementation Shortfall Components for Trader Performance Evaluation, Opportunity Cost in Partial Fill Scenarios, Hurdle Rate Misapplication and Project Selection Errors, Goals-Based Allocation Applicability to Institutions, GIPS Composite Construction Requirements, Multi-Stage Time Horizon Identification, Asset Allocation Heuristic Characteristics, Monte Carlo Simulation Capabilities for Complex Distributions, Mean-Variance Dominance vs. Risk-Return Trade-offs, Market Segmentation as Investment Opportunity, High-Frequency Data and Asynchronism Bias, Counterparty Risk in Derivative and Structured Transactions, Factor Attribution Contribution Interpretation, Risk Attribution Framework Selection, CAPM Feasibility Constraints, Systematic Risk versus Total Risk Measurement, Correlation versus Beta in Regression Analysis, Investment Style In-Favor/Out-of-Favor Identification, Asymmetric Fee Structure Risk Incentives, Return Attribution Component Alignment with Strategy, Market Efficiency Evidence Interpretation from CAR Studies, Behavioral Bias Linkage to Investment Factors, Collateral Posting Direction in Derivative Transactions, Pension Plan Risk Tolerance Impact of Distribution Options, Type I vs Type II Errors in Manager Evaluation Context, Systematic Risk Calculation from Return Distributions, Drawdown Duration vs Recovery Time Distinction, Beta Formula Directional Relationship, GIPS Private Equity Valuation Hierarchy, Brinson-Fachler Allocation Effect Calculation, Capture Ratios and Return Profile Convexity, Fixed Income Attribution Curve Effect vs Sector Allocation, Custom Benchmark Investability Requirement, Market Efficiency Evidence from CAR Event Studies, Performance Attribution Definition Validation, Resampling Methodology Technical Critique Evaluation, Sharpe Ratio Calculation Verification, Beta Formula Application for Missing Values, Asset-Liability Management vs Performance Measurement Benchmark Selection, Brinson-Fachler Attribution Analysis, Multi-Manager Portfolio Risk Aggregation, Risk-Based Approach Diversification Estimation Direction, Marginal Security Selection for Diversified Portfolios, Risk-Based Approach Diversification Estimation Direction, Marginal Security Selection for Diversified Portfolios |
| `portfolio_management/unit_currency_percent.md` | Portfolio management | Unit/scale errors | Time-Scale Conversion in Stochastic Processes, After-Tax Proceeds from Asset Sales with Cost Basis, Present Value of Annuity Due vs. Lump Sum Requirements, Precision Requirements in Portfolio Optimization, Percentage vs. Decimal in Variance Calculations, Leverage Effects on Returns - Arithmetic vs. Compound, Performance Measure Calculations - Following Through to Final Answer |
| `portfolio_management/wrong_targets.md` | Portfolio management | Target misidentification | Question Framework Mismatch Detection, Table Cell Reference Navigation, Answer Option to Source Text Mapping |
| `equity/concept_confusion.md` | Equity | Concept confusion | Price-Weighted Index Divisor Adjustment, Implicit Trading Costs vs. Explicit Costs, Type I vs. Type II Errors in Manager Selection, Top-Down vs. Bottom-Up Investment Approaches, Investment Style Classification Based on Metrics, Risk Neutrality and Utility Maximization, Equity Value as Residual Claim, Quantitative Investment Process Hierarchy, Performance Attribution vs. Performance Appraisal, Portfolio vs. Individual Security Returns, Minimum Variance Hedge vs. Naive Hedge, Institutional Client Cost Structure Selection, Active Risk and Correlation Structure in Portfolio Positions, Equity Value with Limited Liability and State-Contingent Payoffs, Long-Short Strategy Alpha Scaling, Firm Value vs. Equity Value Maximization, Fundamental Management vs. Quantitative/Top-Down Approaches, Specialist/Market Maker Inventory Management, ESG Activist Investor Characteristics, Growth vs. Value Investor Risk Sensitivities, Index Weighting Schemes and Size Bias, Portfolio Construction Building Blocks - Alpha Skills vs. Factor Weighting, Systematic Risk Calculation from State-Contingent Returns, Expected Return and Standard Deviation Across Economic States, CAPM Pricing Interpretation and Investment Recommendations, Beta Formula Application for Missing Values, Table Value Extraction and Numerical Comparison |
| `derivatives/concept_confusion.md` | Derivatives | Concept confusion | Currency Pair Reciprocity and Hedging Direction, Option Exercise Logic and Payoff Asymmetry, Interest Rate Swap Impact on Market Value vs Cash Flow Risk, Covered Call vs Protective Put Floor Establishment, Piecewise Function Continuity at Boundary Conditions, Numeraire Change and Correlation-Adjusted Risk Pricing, Short Straddle Greek Signature Recognition, Duration Matching in Interest Rate Hedging, Swap Payoff Evaluation Under Relative Performance Expectations, Swaption Exercise and Net Rate Calculation with Loan Spreads, No-Arbitrage Equivalence for Identical Payoffs, Traditional vs Foreign Risk-Neutral Measure Distinction, Swap Direction for Portfolio Rebalancing, Risk-Free Return Requires Complete Risk Elimination, Option Intrinsic Value Lower Bounds and Mispricing Detection, Volatility Smile vs Skew Pattern Recognition, Interest Rate Swap Cash Flow vs Market Value Sensitivity, Swaption Type Selection for Existing Swap Positions, Duration-Based Swap Notional Principal Calculation, Beta Adjustment Effectiveness Verification, Maximum Profit Calculation for Option Strategies |
| `derivatives/wrong_targets.md` | Derivatives | Target misidentification | Distinguishing Derivative Payoff from Underlying Asset Price, Identifying Multiple Conditional Expectations as Separate Targets, Distinguishing Formula Structure from Specific Applications, Matching Option Type Across Compound Structures, Verifying Arithmetic in Weighted Averages |
| `fixed_income/concept_confusion.md` | Fixed income | Concept confusion | Cross-Hedge Correlation Logic, Multiple Liability Immunization Convexity Requirements, Callable Bond Performance in Declining Rate Environments, Benchmark Selection for Market Risk Matching, Interest Rate Swap Directional Positioning, Option Asymmetry in Hedging Strategies, Tracking Error from Spread Duration Contribution, Reinvestment Risk and Cash Flow Yield Relationship, Liability Type Classification by Certainty, Zero-Coupon Bond Hold-to-Maturity Return Certainty, Total Return Framework for Secondary Market Trades, Barbell vs. Bullet Convexity Comparison, Expected Excess Return Calculation in Credit Markets, Covered Interest Rate Parity and Forward Hedging Decision, Identifying Correct vs. Incorrect Statements in Structured Products, Single-Period Immunization Complete Requirements, Contingent Claim Risk in Mortgage-Backed Securities, Call Probability Assessment for Callable Bonds, Risk Premium Approach to Expected Return Calculation |
| `alternative_investments/concept_confusion.md` | Alternative investments | Concept confusion | Risk Tolerance Translation to Product Features, Incremental IRR Necessity Conditions, Primitive vs. Derivative Asset Classification, Inflation Hedge Asset Characteristics, Deflationary Impact on Asset Classes, Return Enhancement vs. Diversification Benefits, Human Capital Lifecycle Valuation, Due Diligence Distinctions by Investor Type, Needs Analysis Insurance Calculation Logic, Marginal Diversification vs. Incremental Return, Convertible Preferred Stock Participation Rights in Private Equity, Probate Process vs. Non-Probate Transfers, Rebalancing Band Width Optimization vs. Current Allocation Status, IPS Constraint Parameters vs. Tactical Investment Decisions, Concentration Risk Mitigation with Ownership Retention, High-Water Mark Performance Fee Mechanics |
| `alternative_investments/wrong_targets.md` | Alternative investments | Target misidentification | Analysis: Alternative Investments Wrong Target Errors, Question Target Misidentification in Multi-Actor Scenarios, Negation-Based Question Logic Confusion, Case Study Scope Boundary Misrecognition, Mechanism vs. Outcome Confusion in "Relevance" Questions, Asset Liquidation Optimization |
| `corporate_finance/concept_confusion.md` | Corporate finance | Concept confusion | Debt Aggregation in Mergers, Debt as Contingent Claim with Absolute Priority, Independent State Variables in Mergers, Firm Value vs. Asset Value with Debt, Wealth Transfer Requires Risky Debt, Cash Flow to Stockholders Formula, Expected Firm Value with Identical Expected Assets, Incremental IRR Direction for Mutually Exclusive Projects, Arbitrage Strategy Selection Under M&M Propositions |
| `economics/concept_confusion.md` | Economics | Concept confusion | Exchange Rate Quotation Directionality, Monetary Policy Trilemma (Impossible Trinity), Currency Risk Premium and Bond Yield Direction, GDP Growth and Equity Returns Causality |
| `portfolio_management/conceptual_inversions.md` | Portfolio Management | Conceptual Inversions and Multi-Step Logic | CAPM Pricing Direction Inversion, Risk-Adjusted Hurdle Rate Misapplication, Joint Probability vs. Conditional Probability Confusion, High-Water Mark Cumulative Recovery Logic, Discrete-to-Continuous Time Scaling in Stochastic Models, Return-Price Relationship in Overvaluation, Multi-Period Fee Structure Impact Analysis, Conditional vs. Marginal Probability in Scenario Analysis, Project Selection with Heterogeneous Risk, Time-Scale Transformation in Volatility Models |
| `fixed_income/quantitative_metrics.md` | Fixed Income | Quantitative Yield Curve and Portfolio Metrics | Butterfly_Spread_Calculation_and_Sign_Convention, Zero_Coupon_Bond_Portfolio_Convexity_Calculation, Bloomberg_Terminal_Yield_Field_Extraction, Yield_Curve_Position_Interpretation, Duration_Matched_Portfolio_Convexity_Comparison, Convexity_Present_Value_Weighting_Error, Yield_Data_Source_Hierarchy_on_Terminal_Displays, Portfolio_Duration_Calculation_Simple_Weighted_Average |
| `equity/new_patterns_9924.md` | equity | Capability gap | (new patterns) |
| `derivatives/binomial_mechanics.md` | Derivatives | Binomial Model Mechanics | Multi-Period Binomial Tree Navigation, Risk-Neutral Pricing Formula Construction, Multi-Period Backward Induction, Risk-Neutral Probability Calculation, Binomial Tree State Labeling, Futures Contract Beta Adjustment, Derivative vs. Underlying Payoff Distinction, Complete Formula Assembly, Conditional Expectation Time Indexing |
| `alternative_investments/context_and_methodology_gaps.md` | Alternative Investments | Context and Methodology Gaps | missing_context_detection, liquidity_budget_analysis, least_accurate_statement_logic, spending_policy_smoothing_mechanisms, investment_policy_element_interconnections, benchmark_bias_applicability |
| `corporate_finance/npv_and_capital_budgeting.md` | Corporate Finance | NPV Calculation and Capital Budgeting | npv_cash_flow_identification, after_tax_cash_flow_with_depreciation, real_vs_nominal_rate_conversion, project_comparison_with_alternatives, wacc_methodology_distinction, perpetuity_with_multiple_growth_rates, acquisition_valuation_with_synergies |
| `economics/build_up_calculations.md` | Economics | Build-Up Approach Calculations | Risk Premium Build-Up, Tobin's q Calculation, Component Identification |
| `equity/portfolio_management_concepts.md` | Equity | Concept Confusion | Performance attribution vs. evaluation, Type I/II errors in governance, Hedge ratio estimation risk, Investment vehicle selection, Active risk from sector rebalancing, Statistical error frameworks, Descriptive vs. normative analysis, Correlation and diversification |
| `alternative_investments/new_patterns.md` | Alternative Investments | Portfolio Management and Planning Gaps | life_insurance_needs_analysis, rebalancing_band_width_design, illiquid_asset_rebalancing_mechanisms, liquidity_budget_stress_testing, bottom_up_liquidity_calculation_verification, allocation_change_impact_on_liquidity_profile |

## How to Use

### Step 1: Identify the Question Type
Read the question and determine:
- Which financial subfield? (portfolio management, derivatives, fixed income, equity, alternative investments, corporate finance, economics)
- What type of error is likely? (concept confusion, visual evidence, constraint violation, target misidentification, unit/format errors)

### Step 2: Request the Relevant Skill File
Use the `load_skill_file` tool to request the appropriate file based on the File Index above.

### Step 3: Apply the Pattern
1. Find the matching pattern in the loaded skill file
2. Follow the reasoning steps provided
3. Verify your answer against the pattern's key insights

### Example

**Question**: "Based on Figure 1, which portfolio lies on the efficient frontier?"

**Step 1**: This is a portfolio management question involving visual evidence (reading a chart).

**Step 2**: Request `common/visual_evidence.md` for chart reading patterns, and `portfolio_management/concept_confusion.md` for efficient frontier concepts.

**Step 3**: Apply the "Visual_Scatter_Plot_Dispersion_Assessment" pattern from visual_evidence.md to correctly read the chart values, then apply the "Mean-Variance Dominance vs. Risk-Return Trade-offs" pattern to identify the efficient frontier.

## When NOT to Use

- **Pure arithmetic calculations**: Use computational skills instead (e.g., NPV, IRR, duration calculations)
- **Formula derivations**: These skills focus on concept application, not mathematical proofs
- **Memorization questions**: Direct recall of definitions without reasoning
- **Questions with complete, unambiguous information**: These skills address interpretation challenges, not straightforward applications
- **Real-time market data analysis**: These patterns are based on exam-style structured scenarios

## Coverage Summary

- **8 skill files** covering cross-subfield patterns (visual evidence, constraints, output format)
- **14 subfield-specific files** addressing concept confusion and target misidentification
- **200+ distinct patterns** across portfolio management, derivatives, fixed income, equity, alternative investments, corporate finance, and economics
- **120+ documented cases** with detailed reasoning chains
```