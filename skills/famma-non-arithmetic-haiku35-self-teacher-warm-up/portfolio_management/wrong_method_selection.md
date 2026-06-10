Based on the comprehensive analysis of the failure cases, here are the key skill patterns:

## Pattern: Conditional Probability Precision

**Description:** Financial models often require precise calculation of joint probabilities by correctly matching specific conditions and their corresponding probabilities.

**When to Use:** Triggered by keywords like "probability of", "joint event", "conditional probability" in financial scenarios

**Procedure:**
1. Identify the specific condition (e.g., market state)
2. Find the exact probability of that specific condition
3. Find the probability of the secondary event GIVEN that specific condition
4. Multiply these probabilities to calculate joint probability
5. Verify by checking that probabilities sum to 1 and are between 0-1

**Example:**
> **Scenario:** A stock has different performance probabilities across economic states
> **Wrong approach:** Multiplying random probabilities without matching conditions
> **Correct approach:** 
> - Neutral market probability: 0.50
> - Stock poor performance in neutral market: 0.30
> - Joint probability: 0.50 * 0.30 = 0.15

## Pattern: Risk Attribution Method Selection

**Description:** Choosing the correct risk attribution approach requires deep understanding of the portfolio manager's specific strategy and risk management techniques.

**When to Use:** When evaluating portfolio management strategies, especially with sector-specific or risk-controlled approaches

**Procedure:**
1. Analyze the manager's primary risk management strategy
2. Map the strategy's key characteristics to risk attribution methods
3. Consider:
   - Sector exposure control
   - Idiosyncratic risk management
   - Portfolio construction principles
4. Select the most aligned risk attribution method
5. Verify by checking if the method captures the manager's key risk management goals

**Example:**
> **Scenario:** Manager focusing on sector timing with risk concentration limits
> **Wrong approach:** Using generic total risk contribution
> **Correct approach:** Select method that breaks down factor and specific risk contributions

## Pattern: CAPM Consistency Verification

**Description:** Capital Asset Pricing Model (CAPM) requires consistent relationships between expected returns, beta, risk-free rate, and market risk premium.

**When to Use:** Analyzing portfolio returns, beta calculations, risk-return trade-offs

**Procedure:**
1. Verify beta's relationship to expected return
2. Check consistency with market risk premium
3. Validate standard deviation proportionality
4. Use CAPM formula: E(R) = Rf + β[E(Rm) - Rf]
5. Cross-check multiple parameters for logical coherence
6. Flag inconsistent scenarios that violate CAPM assumptions

**Example:**
> **Scenario:** Portfolio with unusual return-risk combination
> **Wrong approach:** Accepting any return-risk pairing
> **Correct approach:** Systematically verify CAPM consistency across multiple parameters

## Pattern: Performance Metric Precision

**Description:** Different performance metrics capture distinct aspects of investment performance, requiring precise understanding of their specific meanings and applications.

**When to Use:** Evaluating investment manager performance, comparing different investment strategies

**Procedure:**
1. Identify the specific performance evaluation criteria
2. Match criteria to appropriate performance metrics
3. Understand each metric's unique characteristics:
   - Sharpe Ratio: Risk-adjusted return
   - Treynor Measure: Return per unit of systematic risk
   - Information Ratio: Active return relative to tracking error
4. Select metric that most directly addresses the evaluation goal
5. Verify by cross-referencing metric with specific performance objectives

**Example:**
> **Scenario:** Assessing manager's active management skill
> **Wrong approach:** Using generic performance metrics
> **Correct approach:** Select Information Ratio to measure active return efficiency

These patterns capture the key reasoning gaps observed in the financial reasoning failure cases, providing structured approaches to solving complex financial analysis problems.