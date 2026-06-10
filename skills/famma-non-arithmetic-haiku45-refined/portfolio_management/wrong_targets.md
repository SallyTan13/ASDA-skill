# Skill Patterns for Wrong Targets Error Type

## Pattern: Question Scope Calibration

**Description:** Failure to distinguish between questions asking for a simple direct answer (e.g., "what does X capture?") versus questions requesting comprehensive explanation or justification (e.g., "why does X work this way?"). Models over-explain when brevity is required. Additionally, failure to distinguish between what a tool/method DOES (its primary function or mechanism) versus what CONCLUSIONS or APPLICATIONS can be derived from it.

**When to Use:** 
- When questions use verbs like "capture," "measure," "represent," "intended to" without asking "why," "how," or "explain"
- When questions ask "what is X" or "what does X do" or "effective X" in the context of analytical tools, methods, or frameworks
- When questions ask about correctness of statements describing a tool's function versus its interpretive uses
- When evaluating whether statements about a method describe its CORE MECHANISM versus DOWNSTREAM APPLICATIONS

**Procedure:**
1. Parse the question verb: "what does X capture/measure/represent" asks for the PRIMARY TARGET, not mechanism or applications
2. Check if question includes explanation triggers ("why," "how," "explain," "justify") — if absent, provide only the core definition
3. **For analytical tools/methods: distinguish between PRIMARY FUNCTION (what the tool does mechanically) and SECONDARY USES (what conclusions can be drawn from it)**
4. **Identify whether statements describe the tool's direct output versus interpretations of that output**
5. State the direct object or concept being measured in 1-2 sentences maximum
6. Resist adding theoretical justification, applications, or extended context unless explicitly requested
7. Verify answer directly completes the sentence "X captures [your answer]" or "X does [your answer]" in plain language
8. **When evaluating correctness: a tool's effectiveness is defined by what it DOES, not by what users might CONCLUDE from it**

**Example (sanitized):**
> **Scenario 1:** "What is the Sharpe ratio intended to measure?"
> **Wrong approach:** Explaining risk-adjusted returns, how it's calculated, why it's useful for portfolio comparison, when to use it versus other ratios, its limitations, etc.
> **Correct approach:** "The Sharpe ratio measures risk-adjusted return per unit of total risk." (Direct answer to what it measures, nothing more.)

> **Scenario 2:** "Which statement about effective regression analysis is correct? Statement A: Regression analysis draws conclusions about causation between variables. Statement B: Regression analysis quantifies the statistical relationship between variables."
> **Wrong approach:** Accepting both statements because regression results are often used to infer causation in practice.
> **Correct approach:** "Only Statement B is correct. Regression analysis mechanically quantifies statistical relationships by estimating coefficients that minimize prediction error. While analysts may draw causal conclusions from regression results, the method itself does not establish causation—that requires additional theoretical or experimental validation. The tool's primary function is quantification of relationships, not causal inference."

**Common Mistakes to Avoid:**
- Conflating what a tool mechanically produces with what interpretations users derive from it
- Treating downstream applications or conclusions as equivalent to the tool's core function
- Assuming that because a tool is commonly used for a purpose, that purpose defines the tool's effectiveness
## Pattern: Empirical vs Theoretical Question Distinction

**Description:** Confusion between questions asking about empirical reality ("are X and Y the same in practice?") versus theoretical justification ("why would X and Y differ?"). The former requires a simple yes/no based on observation; the latter requires reasoning.

**When to Use:** Questions containing "in practice," "likely to be," "typically," "usually" combined with comparison words like "same," "different," "equal."

**Procedure:**
1. Identify if question asks about practical reality ("in practice," "likely," "typically") versus theory ("should," "must," "theoretically")
2. For empirical questions: provide direct yes/no answer based on standard practice, with 1-sentence justification
3. Avoid extensive theoretical derivation when question asks about practical observation
4. Remember: parameters in financial models (GARCH, EWMA, etc.) are asset-specific and estimated separately in practice
5. Verify answer addresses "what happens" not "why it happens" for empirical questions

**Example (sanitized):**
> **Scenario:** "In practice, is the correlation coefficient likely to be the same for stocks in different industries?"
> **Wrong approach:** Explaining correlation theory, diversification benefits, systematic vs idiosyncratic risk, portfolio construction principles...
> **Correct approach:** "No. Correlation coefficients are estimated from historical data specific to each pair of stocks, and stocks in different industries have different co-movement patterns."

---

## Pattern: Notation Disambiguation in Context

**Description:** Failure to recognize when mathematical notation in a question refers to a specific technical construct (e.g., β² as a quadratic regression term) rather than the base concept (β as systematic risk measure). Missing that questions about model specification require understanding the statistical testing framework.

**When to Use:** When questions reference squared terms (β², σ²), polynomial relationships, or ask about "effect of [variable]" in regression/model context.

**Procedure:**
1. Check if notation includes transformations (squared, cubed, log, etc.) — these typically indicate regression model terms
2. Recognize that "effect of β²" asks about the coefficient on a quadratic term in a regression model, not about beta itself
3. Connect to the theoretical framework: non-linear relationships in return-beta space imply non-zero coefficients on polynomial terms
4. Recall arbitrage arguments: if SML is linear, then β² coefficient must be zero (no quadratic effect)
5. Answer should address the specific term asked about, not revert to discussing the base variable

**Example (sanitized):**
> **Scenario:** "Researchers test whether returns relate to σ². What should they find about the coefficient on σ²?"
> **Wrong approach:** Explaining that standard deviation measures risk and higher risk should command higher returns...
> **Correct approach:** "The coefficient on σ² should be zero. If returns were quadratic in standard deviation, arbitrage opportunities would exist. The linear risk-return relationship implies only the first-order term (σ) matters, not the squared term."

---

## Pattern: Table Cell Spatial Indexing

**Description:** Failure to systematically locate table cells using both row AND column coordinates when Roman numerals or other markers indicate missing values. Models rely on conceptual pattern-matching rather than precise spatial navigation. Additionally, models may misinterpret numerical values in tables, particularly when comparing Sharpe ratios or other performance metrics.

**When to Use:** Questions asking to "fill in (i), (ii), (iii)..." or similar notation in tables with multiple rows and columns, OR questions requiring comparison of numerical metrics across asset classes in tabular format.

**When NOT to Use:** 
- When the question asks for qualitative assessment of portfolio improvement or asset selection based on multiple criteria (use mean-variance optimization principles instead)
- When numerical comparisons involve standard performance metrics (Sharpe ratios, returns, correlations) that require interpretation rather than just spatial location

**Procedure:**
1. Create explicit row-column mapping: identify which row and which column each notation marker appears in
2. Do NOT assume markers follow sequential order or appear in conceptually related cells
3. For each marker, state: "Marker (X) is at row [name] and column [name]"
4. Apply the appropriate formula/definition for that specific cell intersection
5. Cross-check: if marker appears in multiple cells, verify whether question asks for one value or multiple
6. Special cases: market portfolio correlation with itself = 1.0, market portfolio beta = 1.0, risk-free asset standard deviation = 0
7. **When comparing numerical values (especially Sharpe ratios): verify the sign and magnitude correctly before making comparisons (e.g., 0.998 > 0.026 > -0.055)**

**Common Mistakes to Avoid:**
- Misinterpreting positive Sharpe ratios as inferior to negative ones (a Sharpe ratio of 0.998 is excellent; -0.055 indicates poor risk-adjusted returns)
- Confusing numerical magnitude with ranking when signs differ (positive values always rank higher than negative values for performance metrics)
- Treating data entry anomalies as actual values without sanity-checking against financial principles

**Example (sanitized):**
> **Scenario:** Table shows three investment options with Sharpe ratios: Fund A = 0.85, Fund B = -0.12, Fund C = 0.03. Question asks which fund has the worst risk-adjusted performance.
> **Wrong approach:** Assuming Fund A's 0.85 is "substantially lower" than Fund B's -0.12, or treating the negative sign as irrelevant
> **Correct approach:** "Fund B has the worst risk-adjusted performance with a Sharpe ratio of -0.12. Negative Sharpe ratios indicate returns below the risk-free rate, making them inferior to any positive Sharpe ratio. Fund A (0.85) has the best performance, followed by Fund C (0.03), then Fund B (-0.12)."

---
## Pattern: Single vs Multiple Value Resolution

**Description:** When the same notation marker (e.g., "(vii)") appears in multiple table cells, failing to recognize whether the question asks for one shared value or separate values for each occurrence. Misinterpreting table structure where repeated notation indicates the same value applies to multiple cells.

**When to Use:** When identical notation appears in multiple cells of a table, especially for special entities like risk-free assets where multiple properties share the same value.

**Procedure:**
1. Scan entire table to identify all occurrences of the target notation
2. Check question wording: "value in (X)" (singular) vs "values in (X)" (plural)
3. For singular form: determine if multiple cells with same notation should have identical values (common for risk-free asset: correlation=0, beta=0)
4. If cells are in different columns but same row for a special entity, likely they share the same value
5. Provide single answer when question uses singular "value" even if notation appears multiple times
6. State the value once, optionally noting it applies to multiple cells if helpful for clarity

**Example (sanitized):**
> **Scenario:** Table shows Treasury Bill with notation (viii) in both "Correlation with Market" and "Beta" columns. Question: "What is the value in (viii)?"
> **Wrong approach:** "Correlation = 0 and Beta = 0" (treating as two separate answers)
> **Correct approach:** "0. The notation (viii) appears in both the correlation and beta columns for the Treasury Bill, and both values are 0 for a risk-free asset."

## Pattern: Mean-Variance Portfolio Improvement Assessment

**Description:** When evaluating whether adding a new asset class improves an existing portfolio under mean-variance analysis, models must consider BOTH diversification benefits (correlation) AND risk-adjusted returns (Sharpe ratio). Focusing solely on correlation or misinterpreting Sharpe ratios leads to incorrect asset selection.

**When to Use:** Questions asking which asset is "least likely to improve" or "most likely to improve" a portfolio through mean-variance analysis, especially when provided with correlation matrices and Sharpe ratios.

**Procedure:**
1. Identify the current portfolio composition and its characteristics
2. For each candidate asset, extract TWO key metrics:
   - Correlation with existing portfolio assets (lower is better for diversification)
   - Sharpe ratio (higher is better for risk-adjusted returns)
3. Apply the mean-variance improvement principle: an asset improves the portfolio if it offers:
   - High Sharpe ratio (positive risk-adjusted returns), OR
   - Low correlation with existing assets (diversification benefits), OR
   - Both (optimal case)
4. **Critical: Correctly interpret Sharpe ratio signs:**
   - Positive Sharpe ratio = returns exceed risk-free rate (desirable)
   - Negative Sharpe ratio = returns below risk-free rate (undesirable)
   - Magnitude matters: 0.998 >> 0.026 >> -0.055
5. Rank assets by their combined contribution: assets with negative Sharpe ratios are least likely to improve the portfolio, even if they offer diversification
6. Select the asset with the worst combination of low/negative Sharpe ratio relative to diversification benefit

**Common Mistakes to Avoid:**
- Treating negative Sharpe ratios as superior to positive ones due to numerical confusion
- Focusing only on correlation while ignoring risk-adjusted returns
- Assuming low correlation alone justifies inclusion regardless of performance
- Misreading decimal values (0.998 is nearly 1.0, not nearly 0)

**Example (sanitized):**
> **Scenario:** An equity portfolio considers adding one of three assets: Asset X (correlation 0.15, Sharpe 0.92), Asset Y (correlation 0.11, Sharpe -0.08), Asset Z (correlation 0.10, Sharpe 0.04). Which is least likely to improve the portfolio?
> **Wrong approach:** Selecting Asset X because its Sharpe ratio of 0.92 is "too high" or selecting Asset Z because 0.04 is "low"
> **Correct approach:** "Asset Y is least likely to improve the portfolio. Despite having the second-lowest correlation (0.11), its negative Sharpe ratio (-0.08) indicates it generates returns below the risk-free rate. Mean-variance optimization seeks to maximize risk-adjusted returns; adding an asset with negative Sharpe ratio would reduce portfolio efficiency. Asset X offers both excellent diversification (0.15 correlation) and strong risk-adjusted returns (0.92 Sharpe), while Asset Z provides good diversification (0.10) with modest positive returns (0.04 Sharpe). Both are superior to Asset Y."