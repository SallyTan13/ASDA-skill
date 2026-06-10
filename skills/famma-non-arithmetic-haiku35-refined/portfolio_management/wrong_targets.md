# Pattern Analysis: Wrong Targets Error Type

## Pattern: Question Framework Mismatch Detection

**Description:** The model fails to recognize when a question imposes a specific analytical framework or structured response format (e.g., "for each criterion," "identify one difference per category") and instead treats it as an open-ended question, leading to incomplete or incorrectly structured answers.

**When to Use:** When questions contain structural phrases like "for each," "identify one [item] per [category]," or reference a table/framework with multiple distinct dimensions that must all be addressed.

**Procedure:**
1. Parse the question for structural indicators: "for each," "per category," "in each case," or references to multi-row/multi-column frameworks
2. Identify the complete set of categories/dimensions that must be addressed (count them explicitly)
3. Before answering, create a checklist of all required response elements based on the framework
4. For each required element, locate the relevant data in the source material
5. Structure your response to explicitly address each element separately (use labels, bullet points, or clear segmentation)
6. Verify that your response count matches the required element count before finalizing
7. Check that you haven't provided a general comparison when specific per-category mappings were requested

**Example (sanitized):**
> **Scenario:** Question asks: "For each investment objective (Growth, Income, Preservation), identify one portfolio characteristic that differs between Fund X and Fund Y." A table shows 8 different characteristics across both funds.
> **Wrong approach:** Answering "Fund X focuses on equities while Fund Y focuses on bonds" — this is a general difference but doesn't map specific characteristics to each of the three objectives.
> **Correct approach:** (1) Recognize three objectives require three separate answers. (2) For Growth objective: identify relevant characteristic difference (e.g., equity allocation: Fund X 80% vs Fund Y 40%). (3) For Income objective: identify different characteristic (e.g., dividend yield: Fund X 2% vs Fund Y 5%). (4) For Preservation objective: identify third characteristic (e.g., cash holdings: Fund X 5% vs Fund Y 20%). (5) Verify all three objectives addressed with distinct characteristics.

---

## Pattern: Table Cell Reference Navigation

**Description:** The model fails to correctly map alphanumeric or symbolic references (like Roman numerals, letters in parentheses) to their corresponding positions in a table structure, leading to answering about the wrong cell or data point.

**When to Use:** When questions reference specific table cells using notation like (i), (ii), (v), or ask to "fill in missing values" with symbolic placeholders in a structured table.

**Procedure:**
1. Before attempting to solve, create an explicit mental or written map of all symbolic references to their table positions (row and column)
2. For each reference, write down: reference symbol → row label → column label → what the cell represents
3. Check if any references point to cells with definitional constraints (e.g., correlation of an asset with itself = 1, standard deviation of risk-free asset = 0)
4. Apply these definitional constraints first before attempting calculations
5. For calculation-based cells, identify which other cells are needed as inputs and verify you're using the correct mapped values
6. Double-check that your answer corresponds to the originally requested reference symbol, not a different one you encountered during calculation
7. Verify your answer makes logical sense for what that specific cell represents (e.g., correlations must be between -1 and 1)

**Example (sanitized):**
> **Scenario:** Table shows Asset A, Asset B, and Market Portfolio with columns for Return, Volatility, and Correlation with Market. Cells marked (i), (ii), (iii). Question asks: "What is the value in (ii)?" where (ii) is in the "Correlation with Market" column for the Market Portfolio row.
> **Wrong approach:** Calculating Asset B's volatility because it's also missing, without checking which cell (ii) actually refers to.
> **Correct approach:** (1) Map (ii) → Market Portfolio row → Correlation with Market column. (2) Recognize this is correlation of market with itself. (3) Apply definitional constraint: correlation of any variable with itself = 1. (4) Answer: 1. (5) Verify: this makes sense as correlations range from -1 to 1, and self-correlation is always 1.

---

## Pattern: Answer Option to Source Text Mapping

**Description:** The model fails to rigorously verify whether answer option terminology exactly matches concepts explicitly defined in the source material, leading to selection of distractor options that use plausible-sounding but non-existent terms.

**When to Use:** When questions ask "which is LEAST accurate," "which is NOT mentioned," or require identifying mismatches between options and source text, especially when options use similar terminology to source concepts.

**Procedure:**
1. Extract the exact terminology used in the source text for the relevant concepts (write them down verbatim)
2. For each answer option, identify the key term or concept it references
3. Attempt to find an exact or synonymous match between the option's term and the source text terminology
4. Mark options as: (a) explicitly present in source, (b) paraphrased but clearly present, or (c) not found in source
5. For "least accurate" or "NOT mentioned" questions, prioritize options marked as (c) — terms not found in source
6. If all options appear in source, then evaluate the accuracy of the descriptions/definitions provided for each
7. Verify your selected answer by confirming the source text does NOT support it (for negative questions) or DOES support it (for positive questions)
8. Beware of distractor options that combine real terminology in incorrect ways or use plausible-sounding variants of actual terms

**Example (sanitized):**
> **Scenario:** Source text describes "three pillars of risk management: risk identification, risk measurement, and risk monitoring." Question asks: "Which is LEAST accurately described?" Options: A. risk governance, B. risk measurement, C. risk monitoring.
> **Wrong approach:** Selecting B or C because they appear in the text, assuming the question asks which description is inaccurate rather than which term doesn't match the source.
> **Correct approach:** (1) List exact terms from source: "risk identification," "risk measurement," "risk monitoring." (2) Check each option: A uses "risk governance" (not in source list), B uses "risk measurement" (exact match), C uses "risk monitoring" (exact match). (3) For "least accurately described," option A references a concept not in the original three pillars. (4) Answer: A. (5) Verify: source never mentions "risk governance" as one of the three pillars.