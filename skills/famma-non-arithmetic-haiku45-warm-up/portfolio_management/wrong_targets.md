# Skill Patterns for Wrong Targets Error Type

## Pattern: Question Scope Calibration

**Description:** Failure to distinguish between questions asking for a simple direct answer (e.g., "what does X capture?") versus questions requesting comprehensive explanation or justification (e.g., "why does X work this way?"). Models over-explain when brevity is required.

**When to Use:** When questions use verbs like "capture," "measure," "represent," "intended to" without asking "why," "how," or "explain."

**Procedure:**
1. Parse the question verb: "what does X capture/measure/represent" asks for the PRIMARY TARGET, not mechanism or applications
2. Check if question includes explanation triggers ("why," "how," "explain," "justify") — if absent, provide only the core definition
3. State the direct object or concept being measured in 1-2 sentences maximum
4. Resist adding theoretical justification, applications, or extended context unless explicitly requested
5. Verify answer directly completes the sentence "X captures [your answer]" in plain language

**Example (sanitized):**
> **Scenario:** "What is the Sharpe ratio intended to measure?"
> **Wrong approach:** Explaining risk-adjusted returns, how it's calculated, why it's useful for portfolio comparison, when to use it versus other ratios, its limitations, etc.
> **Correct approach:** "The Sharpe ratio measures risk-adjusted return per unit of total risk." (Direct answer to what it measures, nothing more.)

---

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

**Description:** Failure to systematically locate table cells using both row AND column coordinates when Roman numerals or other markers indicate missing values. Models rely on conceptual pattern-matching rather than precise spatial navigation.

**When to Use:** Questions asking to "fill in (i), (ii), (iii)..." or similar notation in tables with multiple rows and columns.

**Procedure:**
1. Create explicit row-column mapping: identify which row and which column each notation marker appears in
2. Do NOT assume markers follow sequential order or appear in conceptually related cells
3. For each marker, state: "Marker (X) is at row [name] and column [name]"
4. Apply the appropriate formula/definition for that specific cell intersection
5. Cross-check: if marker appears in multiple cells, verify whether question asks for one value or multiple
6. Special cases: market portfolio correlation with itself = 1.0, market portfolio beta = 1.0, risk-free asset standard deviation = 0

**Example (sanitized):**
> **Scenario:** Table shows assets with columns [Return, Volatility, Beta]. Marker (iii) appears in the Beta column for "Index Fund" row.
> **Wrong approach:** Assuming (iii) is about risk-free asset because previous markers were, or calculating based on wrong row
> **Correct approach:** "(iii) is located at row 'Index Fund' and column 'Beta'. An index fund tracking the market has beta = 1.0 by definition. Therefore (iii) = 1.0"

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