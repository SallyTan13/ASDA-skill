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
| `common/visual_evidence.md` | Cross-subfield | Visual evidence misread | Column-to-Data Alignment in Tables, Order Book Depth and Sequential Execution Logic, Numerical Proximity Matching in Multiple Choice, Complete Table Scanning for Optimization, Multi-Image Evidence Integration, Context-Level vs. Item-Level Interpretation, Visual Dispersion Assessment in Scatter Plots, Cost Basis Extraction and Loss Recognition, Bloomberg Terminal Date Notation Decoding, OCR vs. Visual Diagram Conflict Resolution, Financial Terminal Field Systematic Scanning, Table Sign Convention and Cash Flow Direction, Options Intrinsic Value and Time Value Anomaly Detection, Question Scope Identification and Missing Value Disambiguation, Inventory Management and Shortage Cost Assessment, Tax Efficiency and Embedded Gain Assessment |
| `common/missed_constraints.md` | Cross-subfield | Missed constraints | IPS_Policy_Limits_Constraint, Missing_Critical_Parameter_Recognition, Event_Timing_And_Prospective_Application, Tax_Status_Constraint_Recognition |
| `portfolio_management/concept_confusion.md` | Portfolio management | Concept confusion | Price Movement Direction in Trade Execution, Tax Efficiency and Embedded Gains Analysis, Security Pricing Direction vs Return Relationship in CAPM, Arbitrage Existence in Single-Index Models, Implementation Shortfall Components for Trader Performance, Opportunity Cost in Trade Execution, Hurdle Rate Bias in Project Selection, Credit Spread Interpretation for Tactical Allocation, Efficient Frontier Dominance Testing, Goals-Based Allocation Institutional Application, GIPS Composite Construction Requirements, IPS Statement Appropriateness vs Temporal Stability, Multi-Stage Time Horizon Definition, Favorable vs Unfavorable Execution Relative to Benchmarks, Embedded Gains and Tax Liability for New Investors, High-Water Mark Fee Impact Timing, Heuristic vs Optimization Terminology, Returns-Based Benchmark Definition, Structural Inefficiency Repeatability Conditions, Asset Class Specification vs Performance Evaluation, Leveraged Recapitalization vs Shareholder Risk Mitigation, ASC 715 Pension Asset Recognition and Service Cost Treatment, Limit Order Execution Mechanics and Price Constraints, High-Touch vs Algorithmic Execution for Exchange-Traded Derivatives, GIPS Verification Requirements vs Compliance Claims, Mean-Variance Dominance Definition, Asynchronous Trading Effect on Correlation Estimates, Counterparty Risk in Equity Monetization Strategies, Ex-Post Alpha Measurement in CAPM Framework, Factor Attribution for Value Creation Opportunities, Risk Attribution Approach Selection for Factor-Timing Strategies, CAPM Validity and Portfolio Possibility, Systematic Risk Measurement via Beta Calculation, Security Selection Attribution with Portfolio Weights, Loss Aversion vs Mental Accounting in Disposition Effect, Asymmetric Performance Fees and Risk-Taking Incentives, Semi-Strong EMH and Post-Event CAR Interpretation, Behavioral Investor Type Classification in Behavioral Alpha Framework, Drawdown Duration Interpretation for Recovery Assessment, GIPS Private Equity Valuation Hierarchy Standards, Brinson-Fachler Allocation Effect Directional Logic, Custom Benchmark Investability and Practical Replicability, CAPM Data Sufficiency for SML Positioning, Performance Measure Selection for Manager Skill Assessment, Core-Satellite Strategy Benchmark Alignment, Stock Selection for Well-Diversified Portfolio Additions, Implicit Trading Cost Drivers in Active Strategies, Arrival Price Algorithm Characteristics, Capture Ratios and Return Profile Interpretation, Individual Risk Aversion vs Risk Appetite Interpretation, Institutional Portfolio Structure Selection for Cost-Sensitive Clients, Asset Class Selection for Concentrated Portfolios, Risk Aversion and Utility Maximization, Resampled Mean-Variance Optimization Characteristics |
| `portfolio_management/unit_currency_percent.md` | Portfolio management | Unit/currency/percent errors | Time-Scale Conversion in Stochastic Processes, Present Value of Annuity Due with Deferred Target Date, Percentage-Decimal Unit Consistency in Variance Calculations, Arithmetic Verification in Multi-Step Financial Calculations, Confidence Maintenance in Valid Algebraic Derivations, Tax-Adjusted Liquidity Calculation with Capital Gains |
| `fixed_income/concept_confusion.md` | Fixed income | Concept confusion | Interest Rate Parity and Currency Hedging Decisions, Immunization Structural Requirements vs Duration Matching, Benchmark Selection Criteria vs Market Views, Duration Effects vs Convexity Effects in Yield Changes, Swap Direction and Duration Impact, Options Asymmetry and Hedging Objectives, Tracking Error Sources in Fixed Income, Rolling Yield vs Leveraged Portfolio Returns, Credit Deterioration and Optimal Positioning, Liability Type Classification by Certainty Dimensions, Expected Excess Return Under Stable vs Stressed Credit Conditions, Structural Bond Features and Interest Rate Environments, Hedged vs Unhedged Currency Return Definitions, Callable Bond Structural Analysis Accuracy, Hedged Return Calculation Using Interest Rate Parity, Floating-Rate Note Effective Maturity and Yield Calculation, Callable Bond Preference and Interest Rate Environments |
| `equity/concept_confusion.md` | Equity | Concept confusion | Hypothesis Testing Framework in Manager Selection, Top-Down vs Bottom-Up Investment Strategy Classification, Investment Style Classification via Valuation Metrics, Index Construction Methods and Factor Model Assumptions, Performance Attribution as Descriptive vs Evaluative Tool, Hedge Ratio Risk: Minimum Variance vs One-to-One, Investment Vehicle Selection by Investor Type and Scale, Active Risk Changes from Paired Trades, Core-Satellite Strategy Benchmark Alignment, Bond Covenant Payments and Stockholder Indifference, Alpha-Beta Separation vs Core-Satellite Strategies, Index Return Calculation by Weighting Scheme, Manager Selection Error Type Identification via Null Hypothesis, Fundamental vs Quantitative Management Style Classification, Specialist Inventory Management and Order Book Imbalance, Activist Investor Stake Size and Regulatory Thresholds, Systematic Risk Measurement via Beta Calculation, Index Weighting Methodologies and Small-Cap Bias, Systematic Risk Identification via Return Patterns Across Economic States |
| `equity/unit_currency_percent.md` | Equity | Unit/currency/percent errors | Price-Weighted Index Divisor Adjustment After Stock Splits, Arithmetic Self-Contradiction and Verification Failure, Decimal Precision in Squared Terms and Products, Individual Stock Returns with Stock Splits |
| `equity/wrong_method_selection.md` | Equity | Wrong method selection | Portfolio Return Calculation by Index Weighting Method, Factor Contribution to Portfolio Variance in Multi-Factor Models, Portfolio Tracking Error Aggregation from Multiple Managers, Portfolio Alpha Aggregation from Multiple Managers, Simultaneous Multi-Criteria Portfolio Goal Assessment |
| `derivatives/concept_confusion.md` | Derivatives | Concept confusion | Hedging Instrument Type vs. Hedging Objective, Currency Hedging Mechanics for Foreign Investments, Swap Directionality for Exposure Management, Interest Rate Swap Impact on Market Value vs. Cash Flow Risk, Covered Call vs. Protective Put Floor Establishment, Short Option Gamma Sign, Payer vs. Receiver Swaption Definitions, Market Price of Risk Under Numeraire Changes, Complete Hedging Requires Offsetting All Risk Components, Compound Option Put-Call Parity Structure, Short Put Delta Sign and Directional Exposure, Independent Evaluation of Multi-Part Derivative Claims, Minimum Variance Hedge Ratio Risk Characteristics, At-the-Money and Special Strike Price Option Valuation, Option Exercise Loss Calculation, In-the-Money vs. Out-of-the-Money Option Classification, Volatility Smile and Tail Probability Estimation |
| `derivatives/unit_currency_percent.md` | Derivatives | Unit/currency/percent errors | Multi-Step Binomial Tree Arithmetic Verification, Forward Price Calculation with Coupon Adjustment, Duration-Based Swap Notional Verification, Conditional Expectation Path Probability Calculation, Final Answer Transcription Verification |
| `derivatives/wrong_method_selection.md` | Derivatives | Wrong method selection | Futures Beta Adjustment Formula, Effective Beta Verification from Realized Returns, Futures Notional Exposure vs. Cash Investment, Incremental vs. Total Contracts for Portfolio Adjustment, Duration-Based Swap Notional Verification |
| `alternative_investments/concept_confusion.md` | Alternative investments | Concept confusion | Spending_Flexibility_Risk_Capacity_in_Annuities, Incremental_IRR_Necessity_Conditions, Primitive_vs_Derivative_Asset_Classification, Equity_Hedge_Strategy_Market_Condition_Matching, Probate_Exposure_by_Transfer_Mechanism, Benchmark_Bias_Types_in_Alternative_Investments, Portfolio_Diversification_Marginal_Contribution_Analysis, Human_Capital_Relative_Value_Career_Progression, Risk_Based_Approach_Diversification_Assessment, Private_Equity_Capital_Structure_Exit_Scenarios, Suitability_Concern_Contextual_Identification, Rebalancing_Band_Width_Volatility_Matching, Private_Equity_Exit_Strategy_Return_Realization, Counterparty_Risk_Terminology_in_Equity_Monetization, Tax_Deferral_in_Equity_Monetization_Strategies, Asymmetric_Fee_Structure_Risk_Incentive_Comparison, Type_I_vs_Type_II_Error_Classification_in_Manager_Selection, Asymmetric_Fee_Structure_Risk_Incentive_Comparison, Type_I_vs_Type_II_Error_Classification_in_Manager_Selection |
| `economics/concept_confusion.md` | Economics | Concept confusion | Business Cycle Phase and Equity Return Timing, Growth Trend Adjustment by Market Development Status, International Finance Trilemma and Monetary Policy Independence, Currency Risk and Bond Yield Direction Under Peg Stress, GDP Growth vs. Equity Returns Causality, Tobin's Q Directional Interpretation, Real Yield Convergence Across Countries, Currency Appreciation Expectations and Relative Bond Yields, Top-Down vs. Bottom-Up Cyclical Turn Detection, Post-Recession Forecast Optimism Comparison, Yardeni vs. Fed Model Risk Premium Measurement, Yardeni vs. Fed Model Required Return Assumptions, Earnings Growth Rate Measurement Consistency Across Models, Discount Rate vs. Growth Rate Estimation Difficulty in Developing Markets, Corporate Profit Trends vs. GDP Growth Consistency, Economic Data Accuracy Challenges in Developing Markets, Top-Down and Bottom-Up Convergence Expectation, Purchasing Power Parity and Exchange Rate Quotation Direction, Asset Performance Under Inflation Transition Scenarios |
| `corporate_finance/concept_confusion.md` | Corporate finance | Concept confusion | Earnings_Dilution_vs_Value_Dilution, Incremental_IRR_Decision_Rule_Application, Equity_as_Residual_Claim_in_Leverage, Debt_Market_Value_in_Distress, Cash_Flow_to_Stockholders_Comprehensive_Measure, Bond_Covenant_Payment_Indifference_Calculation, Bond_Covenant_Payment_Consistency_Verification |
| `corporate_finance/wrong_targets.md` | Corporate finance | Wrong targets | Reference-Dependent Question Interpretation, Qualitative vs. Quantitative Question Targets, Enterprise Value vs. Equity Value Disambiguation, NPV Decision Rule to Binary Answer Mapping, Debt Value in Default Scenarios, Independent Projects vs. Mutually Exclusive Selection, Rental Income Tax Treatment in NPV Analysis |
| `alternative_investments/wrong_targets.md` | Alternative Investments | Wrong Targets | Missing Context Detection, Sequential Multi-Part Question Tracking, Core Value Proposition Identification, Stakeholder-Specific Concern Mapping, Policy Mechanism vs. Policy Outcome Distinction |
| `common/wrong_output_format.md` | Common | Wrong Output Format | Answer-Explanation Alignment Failure, Calculated-vs-Selected Answer Mismatch, Verbosity Mismatch with Ground Truth Format |
| `derivatives/wrong_targets.md` | Derivatives | Wrong Targets | Option Type Inference from Economic Context, Compound Option Target Disambiguation, Perspective Identification in Options Scenarios, Specific Strike Price Selection from Context |
| `portfolio_management/wrong_method_selection.md` | Portfolio Management | Wrong Method Selection | Underdetermined System Recognition in Multi-Asset CAPM, Multi-Method Beta Calculation with CAPM Consistency Check, State-Based Return Calculation as Market Proxy |
| `portfolio_management/wrong_targets.md` | Portfolio Management | Wrong Targets | Question Scope Calibration, Empirical vs Theoretical Question Distinction, Notation Disambiguation in Context, Table Cell Spatial Indexing, Single vs Multiple Value Resolution, Mean-Variance Portfolio Improvement Assessment |
| `equity/new_patterns.md` | Equity | Portfolio Management Concept Distinctions | performance_attribution_vs_appraisal, error_types_in_manager_selection, investment_vehicle_selection_by_client_type, active_risk_and_correlation_structure, probability_specification_in_discrete_distributions, institutional_vs_retail_investment_considerations, factor_exposure_and_diversification_effects, performance_measurement_framework_components, tracking_error_decomposition |
| `derivatives/new_patterns.md` | Derivatives | Multi-Step Calculation and Answer Mapping Errors | Binomial Option Pricing, Answer Option Mapping Verification, Period vs Total Time Confusion, Backward Induction Execution |
| `alternative_investments/new_patterns.md` | Alternative Investments | Liquidity and Insurance Planning Analysis | Bottom_Up_Liquidity_Classification_Analysis, Life_Insurance_Needs_Analysis_Method, Liquidity_Management_Framework_For_Illiquid_Allocations, Partial_Liquidity_Classification_Aggregation, Growing_Annuity_Time_Horizon_Selection, Liquidity_Stress_Testing_Requirements |
| `corporate_finance/new_patterns.md` | Corporate Finance | Conceptual vs. Computational Interpretation | Conceptual question recognition, Perpetuity with growth components, WACC weighting scheme identification, Real vs. nominal rate consistency, Multi-component cash flow aggregation |
| `fixed_income/tax_exempt_liquidation.md` | Fixed Income | Tax-Exempt Liquidation Strategy | Tax-exempt liquidation decisions, Investment view hierarchy, Equal proceeds tiebreaker |
| `equity/risk_decomposition_concepts.md` | Equity | Risk Decomposition and Portfolio Strategy Concepts | statistical_measures_from_discrete_distributions, active_risk_and_correlation_effects, alpha_beta_separation_vs_core_satellite, multifactor_variance_decomposition, tracking_error_aggregation_limitations |
| `alternative_investments/incremental_analysis_necessity.md` | Alternative Investments | Incremental Analysis Necessity | Determining when incremental IRR/NPV analysis is required vs. unnecessary, Incremental analysis decision framework for mutually exclusive projects |

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

## Pattern: Time-Scale Conversion in Stochastic Processes

**Description:** When converting stochastic differential equations (SDEs) from one time unit to another (e.g., daily to yearly), drift and diffusion terms scale differently. Drift terms scale linearly with the time unit multiplier, while diffusion terms scale with the square root of the time unit multiplier. This pattern addresses the systematic conversion of continuous-time stochastic processes across time scales.

**When to Use:**
- Question explicitly asks for a stochastic model "when time is measured in [different unit]"
- Converting between daily/monthly/yearly time scales in continuous-time models
- Brownian motion increments dz or Wiener processes appear in the equation
- Parameters are defined for one time scale but answer requires another

**Procedure:**
1. **Identify the base SDE structure:** Write the equation in standard form dX = μ(X,t)dt + σ(X,t)dz
2. **Determine the time unit conversion factor k:** If converting from smaller to larger units (e.g., daily to yearly with 252 trading days), k = 252; if converting from larger to smaller, k = 1/252
3. **Scale the drift term:** Multiply the entire drift coefficient μ(X,t) by k → k·μ(X,t)dt
4. **Scale the diffusion term:** Multiply the entire diffusion coefficient σ(X,t) by √k → σ(X,t)√k·dz
5. **Keep structural parameters unchanged:** Parameters like mean-reversion levels (V_L), volatility coefficients (ξ), and functional forms remain the same
6. **Verify dimensional consistency:** Check that dt and dz terms have correct time-scale dimensions

**Example (sanitized):**
> **Scenario:** A mean-reverting interest rate model is given as dr = 0.5(0.03 - r)dt + 0.02√r dz when time is measured in months. Express the model when time is measured in years.
> 
> **Wrong approach:** "The parameters need to be rescaled: the mean reversion speed becomes 0.5/12 and volatility becomes 0.02/√12, giving dr = (0.5/12)(0.03 - r)dt + (0.02/√12)√r dz"
> 
> **Correct approach:**
> 1. Base SDE: dr = 0.5(0.03 - r)dt + 0.02√r dz (monthly)
> 2. Conversion factor: k = 12 (12 months per year)
> 3. Scale drift: 0.5(0.03 - r) → 12 × 0.5(0.03 - r) = 6(0.03 - r)
> 4. Scale diffusion: 0.02√r → 0.02√r × √12 = 0.02√12 √r
> 5. Yearly model: dr = 6(0.03 - r)dt + 0.02√12 √r dz
> 6. The long-run mean (0.03) and structural form remain unchanged

**Common Mistakes to Avoid:**
- Rescaling parameters (α, β, ω) instead of scaling the drift/diffusion terms directly
- Applying the same scaling factor to both drift and diffusion (they scale differently: k vs √k)
- Changing the long-run equilibrium values or mean-reversion targets
- Forgetting that dz already incorporates √dt, so diffusion terms only need √k multiplier
- Treating discrete-time and continuous-time conversions identically

---

## Pattern: Conditional Expectation Path Probability Calculation

**Description:** Computing conditional expectations in binomial trees for sums of random variables across multiple time periods requires careful path-by-path analysis. When calculating E[X_t + X_s | state at time r] where r < t < s, variables at intermediate times become deterministic along specific paths, while later variables remain random. The expectation must account for the joint path structure, not just marginal distributions.

**When to Use:**
- Question asks for E[S_i + S_j | information at time k] where k < i < j in a binomial tree
- Computing expected values of sums, products, or functions of variables at different future times
- Conditional expectation involves multiple random variables that evolve sequentially
- The conditioning information specifies a particular node/state in the tree

**Procedure:**
1. **Identify the conditioning state:** Determine the specific node at time t where conditioning occurs (e.g., state H at time 1)
2. **Map all paths forward:** From the conditioning state, enumerate all possible paths to the latest time period involved
3. **For each complete path, compute the sum/function:**
   - Variables at earlier times are deterministic along each specific path
   - Only the final variable in the sum remains random at intermediate nodes
   - Calculate the path-specific value of the entire expression
4. **Assign path probabilities:** Multiply the conditional probabilities along each path (e.g., p^k × q^(n-k) for k up-moves)
5. **Compute weighted average:** Sum all path-specific values weighted by their probabilities
6. **Verify using linearity (if applicable):** For sums, check E[X + Y | state] = E[X | state] + E[Y | state], but compute each term carefully with proper conditioning

**Example (sanitized):**
> **Scenario:** In a 3-period binomial tree with up probability p = 0.6 and down probability q = 0.4, stock prices are S_0 = 100, up factor u = 1.2, down factor d = 0.9. Compute E_1[S_2 + S_3](U) where U denotes the up-state at time 1.
> 
> **Wrong approach:** "E_1[S_2](U) = 0.6(144) + 0.4(108) = 129.6, and E_1[S_3](U) = 0.6²(172.8) + 2(0.6)(0.4)(129.6) + 0.4²(97.2) = 145.15, so E_1[S_2 + S_3](U) = 274.75"
> 
> **Correct approach:**
> 1. Conditioning state: At time 1, state U has S_1 = 120
> 2. Paths from U:
>    - Path UU: S_2 = 144, then UUU (S_3 = 172.8) or UUD (S_3 = 129.6)
>    - Path UD: S_2 = 108, then UDU (S_3 = 129.6) or UDD (S_3 = 97.2)
> 3. Path-specific sums:
>    - UUU: S_2 + S_3 = 144 + 172.8 = 316.8
>    - UUD: S_2 + S_3 = 144 + 129.6 = 273.6
>    - UDU: S_2 + S_3 = 108 + 129.6 = 237.6
>    - UDD: S_2 + S_3 = 108 + 97.2 = 205.2
> 4. Path probabilities: p² = 0.36, pq = 0.24, qp = 0.24, q² = 0.16
> 5. E_1[S_2 + S_3](U) = 0.36(316.8) + 0.24(273.6) + 0.24(237.6) + 0.16(205.2) = 114.05 + 65.66 + 57.02 + 32.83 = 269.56
> 6. Verification: E_1[S_2](U) = 0.6(144) + 0.4(108) = 129.6; E_1[S_3](U) requires conditioning through S_2 states

**Common Mistakes to Avoid:**
- Computing E[S_2] and E[S_3] separately without recognizing that S_2 is deterministic along each path to S_3
- Treating S_2 + S_3 as independent when they share the same path history
- Using marginal probabilities instead of joint path probabilities
- Forgetting that from a given state at time t, the value at time t+1 is deterministic along each branch
- Applying linearity of expectation without properly conditioning each term on the same information set