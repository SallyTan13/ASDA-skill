# Skill Patterns for Visual Evidence Errors in Financial QA

## Pattern: Column-to-Data Alignment in Tables

**Description:** When extracting values from multi-column tables, models may misalign column headers with data rows, reading values from the wrong column. This occurs especially when similar numerical values appear across columns or when column headers are spatially distant from data cells. In factor attribution or comparison tables with paired columns (e.g., Portfolio vs. Benchmark), correctly identifying which value belongs to which entity and calculating differences with proper signs is critical.

**When to Use:** Any question requiring extraction of specific values from tabular data with multiple columns (e.g., "Calculate X for Stock B," "What is the return in state Y?", "Compare portfolio factor exposure to benchmark")

**Procedure:**
1. Identify the exact column header(s) mentioned in the question (e.g., "Stock B," "Limit Sell Orders", "Portfolio", "Benchmark")
2. Trace vertically from the header to locate the correct column position in the table
3. For each required row, move horizontally from the row label to intersect with the identified column
4. Extract the value at the intersection point and label it explicitly with both row and column identifiers (e.g., "Stock B Bear return = 0.108", "Portfolio HML = 0.17")
5. **For comparison tables (Portfolio vs. Benchmark, Scenario A vs. B):**
   - Extract both values: "Portfolio [Factor] = X, Benchmark [Factor] = Y"
   - Calculate difference with explicit formula: "Difference = Portfolio - Benchmark = X - Y = Z"
   - Interpret the sign: positive difference = overweight/higher exposure, negative = underweight/lower exposure
6. Before proceeding with calculations, verify all extracted values by stating: "From column [X], row [Y]: value = [Z]"
7. Cross-check that the number of extracted values matches the expected count for the calculation
8. For multi-step calculations using table values, re-verify each extracted value before final computation

**Example (sanitized):**
> **Scenario:** A factor attribution table shows Portfolio and Benchmark columns with factor sensitivities. SMB row shows Portfolio=0.15, Benchmark=0.22. Question asks: "What is the portfolio's SMB exposure relative to benchmark?"
> **Wrong approach:** Reading Portfolio value (0.15) and stating it as the relative exposure, or confusing which column is Portfolio vs. Benchmark
> **Correct approach:** (1) Identify target columns: "Portfolio" and "Benchmark", (2) Locate SMB row, (3) Extract: "Portfolio SMB = 0.15, Benchmark SMB = 0.22", (4) Calculate difference: "Portfolio - Benchmark = 0.15 - 0.22 = -0.07", (5) Interpret: "Portfolio is underweight SMB by 0.07 relative to benchmark", (6) Verify extraction: checked both values from correct columns

**Common Mistakes to Avoid:**
- Confusing which column represents Portfolio vs. Benchmark in side-by-side comparisons
- Stating a single value when the question requires a difference or comparison
- Reversing the sign of differences (Benchmark - Portfolio instead of Portfolio - Benchmark)
- Misaligning rows when similar numerical values appear in adjacent cells

---
## Pattern: Order Book Depth and Sequential Execution Logic

**Description:** In limit order book questions, "next" order execution implies movement through price levels sequentially, not just identifying the current best bid/ask. The term "next" must be interpreted based on the relationship between the last trade price and current order book state. When the last trade price differs from the best quote, the best quote level remains available unless explicitly stated otherwise. The procedure must distinguish between: (1) last trade AT best quote (suggests consumption), (2) last trade BELOW best ask or ABOVE best bid (best quote still available), and (3) no recent trade context (use current best quote).

**When to Use:** Questions about order execution in limit order books containing phrases like "next market order," "following trade," or providing context about recent transaction prices

**Procedure:**
1. Identify the order direction (buy orders execute against asks; sell orders execute against bids)
2. Locate the best available price level for that direction in the current order book: "Best ask = [price] with [quantity] shares" or "Best bid = [price] with [quantity] shares"
3. **Check for contextual clues about recent trades:**
   - If "last trade at price X" is mentioned, extract X
   - Compare X to the best quote for the relevant side
4. **Apply the sequential execution logic based on last trade position:**
   - **Case A:** If last trade price X EQUALS the best quote → the best level may be consumed → consider moving to the second-best price level
   - **Case B:** If last trade price X is BETWEEN the best quote and second-best quote (e.g., last trade $50.00, best ask $50.25) → best quote level is still available → use best quote
   - **Case C:** If last trade price X is BEYOND the best quote (e.g., last trade $49.50, best ask $50.25) → best quote level is still available → use best quote
   - **Case D:** If no recent trade context is provided → use current best quote
5. **For "next" order interpretation:**
   - If the question context suggests the best level is consumed (Case A), state: "Best [bid/ask] at [price1] appears consumed; next level is [price2]"
   - If the best level remains available (Cases B, C, D), state: "Best [bid/ask] at [price1] remains available for next order"
6. State explicitly: "Last trade at [X], best [bid/ask] at [Y], relationship: [X vs Y], conclusion: next order executes at [Z]"
7. Verify the interpretation by checking if the answer makes sense given the market context (e.g., price should worsen only if best level is truly consumed)

**Example (sanitized):**
> **Scenario:** Order book shows best bid $72.00 (500 shares), best ask $72.25 (400 shares). Last trade occurred at $72.10. Question: "At what price will the next market buy order execute?"
> **Wrong approach:** Concluding the best ask at $72.25 is consumed because there was a recent trade, and moving to the next ask level at $72.50
> **Correct approach:** (1) Market buy executes against asks, (2) Best ask = $72.25 with 400 shares, (3) Last trade at $72.10, (4) Compare: $72.10 < $72.25 (last trade is BELOW best ask), (5) Apply Case B logic: last trade between bid and ask suggests best ask level is still available, (6) Conclusion: "Last trade at $72.10, best ask at $72.25, relationship: last trade < best ask, therefore best ask level remains available", (7) Answer: Next market buy order executes at $72.25

**Common Mistakes to Avoid:**
- Assuming any recent trade automatically consumes the best quote level without comparing the trade price to the quote price
- Failing to distinguish between last trade AT, BELOW, or ABOVE the relevant best quote
- Interpreting "next" as always meaning "second-best level" regardless of whether the best level is actually consumed

---
## Pattern: Numerical Proximity Matching in Multiple Choice

**Description:** When the true value falls between multiple-choice options without an exact match, select the option with minimum absolute difference from the true value. However, for financial data with decimal precision, apply standard rounding conventions before pure distance matching: values should round to the nearest standard increment (e.g., 0.25 for quarter-dollar pricing, 0.01 for percentage points) rather than truncating to whole numbers. **Critical constraint:** When multiple options fall within standard rounding tolerance, prioritize the option that matches standard rounding convention over the option with absolute minimum distance.

**When to Use:** Multiple-choice questions where extracted numerical values don't exactly match any option (trigger: true value falls between two consecutive options)

**Procedure:**
1. Extract the true value from the source (e.g., from terminal display, table, or calculation)
2. Identify the decimal precision of the true value (e.g., 100.34 has 2 decimal places)
3. Examine the options to identify their precision levels and standard increments (e.g., whole dollars, quarter-dollars, cents)
4. **Determine the standard rounding convention for the data type:**
   - For stock prices: identify if quarter-dollar increments (0.25) or other standard increments are used
   - For percentages: round to displayed precision level
   - For rates: follow market convention (e.g., basis points vs. percentage points)
5. **Apply standard rounding to the true value:**
   - Round the true value to the nearest standard increment: "True value [V] rounds to [R] using [increment] rounding"
   - Example: 100.34 with quarter-dollar rounding → 100.25 (nearest quarter below) or 100.50 (nearest quarter above)
6. **Calculate absolute differences for all options:**
   - For each option: |option - true_value|
   - Create a comparison table: Option A: diff = X, Option B: diff = Y, etc.
7. **Apply the selection hierarchy:**
   - **Priority 1:** If an option exactly matches the standard-rounded value [R], select it
   - **Priority 2:** If multiple options are within standard rounding tolerance (e.g., ±0.50 for quarter-dollar pricing), select the one that best aligns with rounding convention
   - **Priority 3:** If no option is within rounding tolerance, select the option with minimum absolute difference
8. **Verification step:** State "True value [V] with precision [P] rounds to [R] using [convention]; option [X] selected because [exact match / within rounding tolerance / minimum distance = D]"

**Example (sanitized):**
> **Scenario:** Terminal displays stock price = 85.67. Options: A. 85.75, B. 85.50, C. 86.00, D. 85.00
> **Wrong approach:** Selecting D (85.00) because it's a "round number," or selecting B (85.50) purely by minimum distance without considering rounding convention
> **Correct approach:** (1) True value = 85.67, (2) Precision = 2 decimal places, (3) Options show quarter-dollar increments (85.00, 85.50, 85.75, 86.00), (4) Standard rounding: quarter-dollar increments (0.25), (5) Round 85.67 to nearest quarter: 85.67 is between 85.50 and 85.75; distance to 85.50 = 0.17, distance to 85.75 = 0.08 → rounds to 85.75, (6) Calculate differences: |85.75-85.67|=0.08, |85.50-85.67|=0.17, |86.00-85.67|=0.33, |85.00-85.67|=0.67, (7) Apply hierarchy: Option A (85.75) matches standard-rounded value, (8) Verification: "True value 85.67 rounds to 85.75 using quarter-dollar convention; option A selected as exact match to rounded value", (9) Answer: A (85.75)

**Common Mistakes to Avoid:**
- Selecting the option with absolute minimum distance when another option matches standard rounding convention
- Truncating decimal values to whole numbers instead of rounding to nearest standard increment
- Ignoring the precision conventions of financial instruments (quarter-dollar pricing for stocks, basis points for bonds)
- Selecting based on "round number" heuristics rather than calculating actual differences and applying rounding rules

---
## Pattern: Complete Table Scanning for Optimization

**Description:** When finding maximum or minimum values across table rows, models may terminate scanning prematurely after finding a locally optimal value, missing the true optimum in unexamined rows.

**When to Use:** Questions requiring identification of "highest," "lowest," "best," or "worst" values from tabular data with multiple rows

**Procedure:**
1. Identify the target column for comparison (e.g., "Expected Return")
2. Initialize tracking: "Current max/min = None"
3. Scan EVERY row sequentially, stating: "Row [i]: value = [V], current best = [B]"
4. For each row, compare and update: if seeking maximum and V > B, update B = V
5. After scanning ALL rows, state: "Scanned [N] rows total, final optimum = [value] in row [X]"
6. Verify the count: confirm that the number of rows examined equals the total rows in the table

**Example (sanitized):**
> **Scenario:** Table with 5 investment options showing returns: Opt1=8%, Opt2=12%, Opt3=15%, Opt4=18%, Opt5=10%. Question: "Which has the highest return?"
> **Wrong approach:** Stopping at Opt3 (15%) without checking remaining rows
> **Correct approach:** (1) Target column: Return, (2) Row 1: 8% (current max=8%), (3) Row 2: 12% (update max=12%), (4) Row 3: 15% (update max=15%), (5) Row 4: 18% (update max=18%), (6) Row 5: 10% (max remains 18%), (7) Scanned 5/5 rows, maximum = 18% in Option 4

---

## Pattern: Multi-Image Evidence Integration

**Description:** When questions reference multiple images (e.g., "use image_1 and image_2"), each image may contain complementary information required for the complete solution. Models may anchor on the first visible image and fail to process subsequent images that contain critical data structures.

**When to Use:** Questions explicitly referencing multiple images/tables (trigger phrases: "image_1 and image_2," "use the following tables," "based on Exhibit A and Exhibit B")

**Procedure:**
1. Parse the question to identify all referenced images/exhibits by number or name
2. For each referenced image, extract its content type (e.g., "image_1: return scenarios," "image_2: probability distributions")
3. Map question requirements to images: "To answer [X], I need [data type Y] which should be in [image Z]"
4. Process images in logical order based on dependency (e.g., if image_2 provides conditional probabilities needed to interpret image_1 values, process image_2 first)
5. Before calculating, verify: "I have extracted [data A] from image_1 and [data B] from image_2"
6. If an image mentioned in the question has not been used, explicitly check whether it contains missing information

**Example (sanitized):**
> **Scenario:** Question: "Using table_1 and table_2, calculate the weighted average cost." Table_1 shows costs per unit; table_2 shows quantity weights.
> **Wrong approach:** Using only table_1 costs and assuming equal weights
> **Correct approach:** (1) Identify references: table_1 (costs), table_2 (weights), (2) Extract from table_1: Cost_A=50, Cost_B=75, (3) Extract from table_2: Weight_A=0.6, Weight_B=0.4, (4) Verify both tables used, (5) Calculate: 50×0.6 + 75×0.4 = 60

---

## Pattern: Context-Level vs. Item-Level Interpretation

**Description:** Models may misinterpret whether a table/comparison represents portfolio-level aggregates or individual security characteristics, leading to incorrect application of diversification principles and risk logic.

**When to Use:** Questions about adding securities to existing portfolios or comparing investment choices where the table shows characteristics labeled as "Portfolio A/B" but context suggests individual securities

**Procedure:**
1. Read the question stem carefully to identify the decision context: "adding to a portfolio" vs. "choosing between portfolios"
2. Examine table labels: if labeled "Portfolio X" but question asks about "which stock," recognize the mismatch
3. Reinterpret table rows as individual securities being compared, not complete portfolios
4. Apply the appropriate financial logic: for well-diversified portfolios, specific risk is already eliminated, so focus on systematic risk contributions
5. State the reinterpretation: "Although labeled Portfolio A/B, these represent individual securities being evaluated for addition"
6. Verify logic: if the question involves diversification, confirm that your reasoning accounts for the existing portfolio's diversification status

**Example (sanitized):**
> **Scenario:** Table shows "Fund X: Beta=1.2, Specific Risk=High" and "Fund Y: Beta=1.2, Specific Risk=Low". Question: "Which should be added to a well-diversified portfolio?"
> **Wrong approach:** Choosing Fund Y because low specific risk is always better
> **Correct approach:** (1) Context: adding to well-diversified portfolio, (2) In well-diversified portfolios, specific risk is already diversified away, (3) Both have identical beta=1.2 (systematic risk), (4) Specific risk of individual additions is irrelevant when portfolio is already diversified, (5) Investor should be indifferent, or choose based on other factors (cost, liquidity)

---

## Pattern: Visual Dispersion Assessment in Scatter Plots

**Description:** When comparing residual variance or firm-specific risk across regression plots, models may incorrectly assess which dataset shows greater vertical scatter around the fitted line, potentially due to visual anchoring on slope, horizontal spread, or scale differences. Accurate assessment requires systematic quantitative estimation of vertical deviations across multiple points, with mandatory cross-validation to prevent visual misidentification. **Critical enhancement:** The procedure now includes explicit anti-bias measures and requires unanimous agreement across all validation checks before finalizing conclusions.

**When to Use:** Questions asking to compare "firm-specific risk," "residual variance," "unexplained variation," "scatter around regression line," or "R²" across multiple scatter plots

**When NOT to Use:** 
- When comparing systematic risk (beta/slope) rather than firm-specific risk (scatter)
- When only one scatter plot is provided
- When the question asks about correlation direction rather than strength
- **When visual quality is poor or plots are ambiguous — defer to explicit numerical data if available**

**Procedure:**
1. Identify that firm-specific risk corresponds to vertical deviation from the regression line (residuals), not slope or R²
2. **Normalize for scale differences:** Check if both plots use the same y-axis scale; if not, note the scale difference and adjust measurements accordingly
3. **Anti-bias preparation:** Before measuring, explicitly note potential visual illusions:
   - Steep slopes can create illusion of tight fit
   - Dense clustering in one region may mask overall dispersion
   - Outliers can distort perception of average scatter
   - **Different axis scales can create false impressions of relative scatter**
   - State: "I will measure systematically to avoid these biases"
4. For each plot, select 5-7 representative points distributed across the x-axis range (low, low-mid, center, mid-high, high values)
5. **For each selected point, measure vertical distance systematically:**
   - Identify the point's x-coordinate
   - Find the corresponding y-value on the regression line at that x-coordinate
   - Calculate vertical distance = |actual y - predicted y|
   - Record: "Plot [A/B], Point [i]: vertical distance = [d]"
   - **Double-check measurement by comparing to adjacent points for consistency**
6. Calculate average vertical deviation for each plot: "Plot A: vertical distances [d1, d2, d3, d4, d5], average ≈ [avg_A]; Plot B: vertical distances [e1, e2, e3, e4, e5], average ≈ [avg_B]"
7. **Preliminary conclusion:** "Based on average deviation, Plot [X] appears to have [higher/lower] scatter"
8. **Cross-validation (MANDATORY - ALL CHECKS MUST AGREE):**
   - **Check 1:** Identify the point furthest from the line in each plot and compare these maximum deviations: "Plot A max = [M_A], Plot B max = [M_B]"
   - **Check 2:** Count the number of points that fall within 1 unit (or appropriate threshold) of the regression line for each plot: "Plot A: [N_A] points within threshold, Plot B: [N_B] points within threshold" (higher count = tighter fit = higher R²)
   - **Check 3:** Visually assess the "band width" around each regression line: "Plot A band width ≈ [W_A], Plot B band width ≈ [W_B]" (narrower band = higher R²)
   - **Check 4:** Verify no systematic bias by checking scatter above vs. below the line is roughly symmetric
   - **Check 5 (NEW):** Re-examine the plots with fresh perspective, asking "Which plot shows points MORE TIGHTLY clustered around the line?" without referencing prior measurements
   - **Consensus requirement:** State "Cross-validation results: Check 1 suggests [X], Check 2 suggests [Y], Check 3 suggests [Z], Check 4 confirms [no bias], Check 5 confirms [W]"
   - **If ANY cross-validation check conflicts with preliminary conclusion:** STOP and re-examine the visual data carefully. Re-measure points from scratch, verify you are measuring VERTICAL distances (not diagonal or horizontal), and identify the source of discrepancy before proceeding
   - **If 2+ checks conflict:** State "Visual assessment is ambiguous; deferring to explicit numerical data if available, otherwise selecting based on majority of validation checks with low confidence"
9. **Visual check for systematic bias (explicit enumeration):**
   - NOT confusing steep slope (high beta) with high scatter
   - NOT confusing wide horizontal spread with vertical dispersion
   - NOT confusing outliers in one direction with overall scatter
   - NOT confusing dense clustering in one region with overall dispersion pattern
   - **NOT misidentifying which plot is which (verify plot labels before concluding)**
   - State: "Verified: not confusing [slope/horizontal spread/outliers/regional clustering/plot identity] with vertical scatter"
10. **Final verification with unanimous agreement:** State "Plot [X] shows [tighter/looser] clustering than Plot [Y] based on: (1) average vertical deviation [A vs B], (2) maximum deviation [C vs D], (3) points within threshold [E vs F], (4) visual band width [G vs H], (5) fresh visual assessment [confirms X], (6) ALL CHECKS AGREE or [specify conflicts and resolution]"
11. State conclusion with R² relationship: "Plot [X] has [higher/lower] R² than Plot [Y] because it shows [less/more] vertical scatter, confirmed by [unanimous/majority] agreement across validation checks"

**Example (sanitized):**
> **Scenario:** Two scatter plots with regression lines. Initial visual impression suggests Plot P has tighter fit.
> **Wrong approach:** Concluding Plot P has higher R² based on quick visual assessment without systematic measurement and cross-validation, or misidentifying which plot shows tighter clustering
> **Correct approach:** (1) Firm-specific risk = vertical scatter; higher scatter = lower R², (2) Both plots use same y-axis scale (0-50), (3) Anti-bias note: "Will measure systematically to avoid slope/clustering/scale illusions", (4) Select 5 points across each plot's x-range, (5) Plot P measurements: Point 1: distance=3.2, Point 2: distance=2.8, Point 3: distance=3.5, Point 4: distance=2.9, Point 5: distance=3.1, (6) Plot P average = 3.1; Plot Q measurements: Point 1: distance=1.8, Point 2: distance=2.1, Point 3: distance=1.9, Point 4: distance=2.0, Point 5: distance=1.7, (7) Plot Q average = 1.9, (8) Preliminary: "Plot Q appears to have lower scatter (1.9 vs 3.1)", (9) Cross-validation: Check 1: Plot P max=3.5, Plot Q max=2.1 (Q tighter); Check 2: Plot P has 1/5 within 2.5 units, Plot Q has 5/5 within 2.5 units (Q tighter); Check 3: Plot P band width ≈6 units, Plot Q band width ≈3 units (Q tighter); Check 4: Both plots show symmetric scatter; Check 5: Fresh look confirms Q has tighter clustering, (10) Consensus: "ALL checks agree Plot Q has tighter fit", (11) Visual bias check: "Verified not confusing slope with scatter, confirmed plot identities", (12) Final verification: "Plot Q shows tighter clustering than Plot P based on: (1) average deviation 1.9 vs 3.1, (2) max deviation 2.1 vs 3.5, (3) points within threshold 5/5 vs 1/5, (4) band width 3 vs 6, (5) fresh visual confirms Q tighter, (6) ALL CHECKS AGREE", (13) Conclusion: Plot Q has higher R² than Plot P because it shows less vertical scatter, confirmed by unanimous agreement across all validation checks

**Common Mistakes to Avoid:**
- Confusing slope steepness (beta/systematic risk) with vertical scatter (firm-specific risk)
- Making quick visual judgments without systematic point-by-point measurement
- Anchoring on outliers rather than assessing overall average dispersion
- Failing to perform cross-validation checks that could reveal visual misidentification
- **Proceeding with a conclusion when cross-validation checks conflict with each other**
- **Misidentifying which plot corresponds to which label (Stock A vs Stock B)**
- Stating conclusions about scatter without explicitly connecting to R² (higher scatter = lower R²)
- Measuring horizontal spread instead of vertical deviation from the fitted line
- **Trusting initial visual impression without systematic measurement verification**

---
## Pattern: Cost Basis Extraction and Loss Recognition

**Description:** When calculating gains/losses on asset sales, models may fabricate "adjusted basis" values not present in source tables or fail to correctly handle situations where cost basis exceeds market value (loss positions), particularly for real estate.

**When to Use:** Questions involving capital gains calculations, after-tax proceeds, or net cash from asset sales where both cost basis and sale price are provided in tables

**Procedure:**
1. Locate the cost basis in the provided table under columns labeled "Cost Basis," "Book Value," or "Original Cost"
2. Extract the exact value without adjustment: "Cost basis from table = [value]"
3. Identify the sale price or current market value from the question or table
4. Calculate gain/loss: Sale Price - Cost Basis (negative result = loss)
5. If result is negative, recognize this as a capital loss (may reduce taxes or have no tax impact)
6. Do NOT create "adjusted basis" figures unless explicitly provided or calculated from documented adjustments (improvements, depreciation)
7. Verify: "Using table cost basis [X], sale price [Y], gain/loss = Y - X = [Z]"

**Example (sanitized):**
> **Scenario:** Table shows Property: Market Value=$800K, Cost Basis=$950K. Question: "Calculate after-tax proceeds from sale at market value (20% tax rate)."
> **Wrong approach:** Using an "adjusted basis" of $850K, calculating gain of -$50K
> **Correct approach:** (1) Cost basis from table = $950K, (2) Sale price = $800K, (3) Gain/loss = $800K - $950K = -$150K (loss), (4) Capital loss: no tax owed (may create tax benefit), (5) After-tax proceeds = $800K - $0 = $800K

---

## Pattern: Bloomberg Terminal Date Notation Decoding

**Description:** Bloomberg terminals from the 1990s-2000s use abbreviated date formats where single-digit year suffixes represent years in the following decade (e.g., in a 1997 terminal, "6/30/2" means June 30, 2002, not 2000).

**When to Use:** Questions about Bloomberg terminal screenshots showing dates with abbreviated year formats (trigger: dates shown as "MM/DD/Y" where Y is a single digit)

**Procedure:**
1. Identify the terminal screenshot date (usually shown at bottom: "12-Dec-97")
2. Locate the target date field (e.g., "MATURITY DT 6/30/2")
3. Extract the single-digit year suffix (e.g., "2")
4. Apply Bloomberg convention: add the digit to the next decade boundary from terminal date
5. For terminal date in 1997, year suffix "2" means 2002 (1990s terminal → 2000s decade)
6. Calculate time difference using the full four-digit year
7. Verify: "Terminal date [YYYY], maturity [MM/DD/YYYY], time to maturity = [X] years"

**Example (sanitized):**
> **Scenario:** Terminal dated "15-Mar-98" shows "MATURITY DT 3/15/5". Question: "How many years until maturity?"
> **Wrong approach:** Interpreting "3/15/5" as March 15, 2000 (2 years)
> **Correct approach:** (1) Terminal date: March 1998, (2) Maturity shown: 3/15/5, (3) Year suffix "5" with 1998 terminal → 2005, (4) Full date: March 15, 2005, (5) Time to maturity: 2005 - 1998 = 7 years

---

## Pattern: OCR vs. Visual Diagram Conflict Resolution

**Description:** When OCR-extracted text conflicts with the structural logic of visual diagrams (e.g., binomial trees, flowcharts), prioritize the diagram's mathematical consistency over potentially erroneous OCR values.

**When to Use:** Questions involving structured diagrams (binomial trees, decision trees, network flows) where OCR provides numerical values that may conflict with the diagram's inherent mathematical relationships

**Procedure:**
1. Extract values from both OCR text and visual diagram structure
2. Check for conflicts: compare OCR values against the diagram's mathematical rules (e.g., in binomial trees: down-move should be < current value)
3. If conflict detected, verify the diagram's structural logic: "In binomial tree, if S1(T)=2 and down-factor applies, S2(TT) should equal [calculated value]"
4. Test OCR value against the pattern: does it follow the multiplicative structure, symmetry, or other inherent rules?
5. If OCR value violates structural logic, flag it as likely OCR error and use diagram-implied value
6. State the resolution: "OCR shows [X], but diagram structure implies [Y]; using [Y] based on [structural rule]"
7. Proceed with calculations using the structurally consistent values

**Example (sanitized):**
> **Scenario:** Binomial tree shows S0=100, S1(up)=120, S1(down)=80. OCR text lists "S2(down-down)=80" but diagram structure shows it should be 64 (80×0.8).
> **Wrong approach:** Using OCR value S2(DD)=80 in calculations
> **Correct approach:** (1) OCR: S2(DD)=80, (2) Diagram structure: down-factor = 80/100 = 0.8, (3) Expected S2(DD) = 80×0.8 = 64, (4) Conflict detected: OCR=80 vs. structure=64, (5) Structural logic: binomial tree requires consistent multiplicative factors, (6) Resolution: Use S2(DD)=64 based on diagram structure, (7) Flag: "OCR value 80 appears to be error; using structurally consistent value 64"

---

## Pattern: Financial Terminal Field Systematic Scanning

**Description:** When answering questions about specific values from financial terminal screenshots, models may substitute domain knowledge or plausibility reasoning instead of systematically scanning for explicitly displayed fields, leading to fabricated answers. After extracting the value, the procedure must include explicit verification that the selected answer option matches the extracted value before finalizing the response. **Critical addition:** The final answer selection must be explicitly cross-checked against the reasoning conclusion to prevent reasoning-to-answer mismatches.

**When to Use:** Any question asking "what is the [specific field]" from a Bloomberg/Reuters/financial terminal screenshot (trigger: "as shown on the display," "according to the terminal")

**When NOT to Use:**
- **When the question asks to "fill in missing value (X)" in a separate data table (not asking about terminal display)**
- When the question requires calculation rather than direct field extraction
- When the question asks for interpretation rather than displayed values

**Procedure:**
1. Identify the exact field name requested (e.g., "redemption yield," "52-week high," "beta")
2. List common field labels for that metric (e.g., redemption yield might appear as: "YTM," "Yield," "Red Yield," "Yld to Mat")
3. Systematically scan the terminal screenshot for these labels, moving section by section (header → left column → right column → bottom)
4. If field is found, extract the adjacent value exactly as displayed: "Field [X] shows value = [Y]"
5. **For multiple-choice questions:**
   - Compare the extracted value [Y] to each answer option
   - Apply the Numerical Proximity Matching pattern if no exact match exists
   - State explicitly: "Extracted value [Y] matches/is closest to option [Z]"
   - **Verification step:** Before finalizing, confirm "Selected answer option [Z] corresponds to extracted value [Y]"
6. **For qualitative/categorical questions (e.g., "what is the status"):**
   - Extract the relevant value or date from the terminal
   - Perform any necessary calculations (e.g., time until maturity)
   - State the calculated result: "Calculated value = [C]"
   - Map the calculated result to answer options: "Value [C] corresponds to option [O] because [reasoning]"
   - **Critical cross-check:** Re-read the selected option text and verify it matches the stated conclusion
7. If field is NOT found after complete scan, state: "The field [X] is not visible in the provided screenshot"
8. Do NOT infer, estimate, or calculate the value based on other visible fields unless explicitly instructed
9. **Final mandatory verification (MUST PERFORM):**
   - Re-state the reasoning conclusion: "Based on analysis, the answer should be [conclusion]"
   - Re-read the selected answer option: "Selected option [X] states: [full text of option]"
   - Confirm alignment: "Option [X] matches conclusion: [YES/NO]"
   - If NO, identify the correct option that matches the conclusion

**Example (sanitized):**
> **Scenario:** Terminal dated 15-Jan-2000 shows "MATURITY DT 3/15/3". Question: "What is the maturity status?" Options: A. Matured, B. Within 1 year, C. 1-5 years, D. Over 5 years
> **Wrong approach:** Correctly calculating maturity as March 15, 2003 (~3 years away, within 1-5 years), but then selecting option B (within 1 year) due to final selection error
> **Correct approach:** (1) Target field: maturity date, (2) Scan terminal: found "MATURITY DT 3/15/3", (3) Extract: 3/15/3, (4) Apply Bloomberg date convention: terminal date 2000, suffix "3" → 2003, (5) Calculate: March 2003 - January 2000 = ~3 years, (6) Map to options: 3 years falls in "1-5 years" range = option C, (7) **Final verification:** "Based on analysis, maturity is in ~3 years, which corresponds to '1-5 years range'", (8) Re-read option C: "1-5 years", (9) Confirm: "Option C matches conclusion: YES", (10) Answer: C

**Common Mistakes to Avoid:**
- Extracting the correct value but selecting a different answer option due to lack of final verification
- Calculating or inferring values instead of reading displayed fields
- Stopping the scan prematurely before checking all terminal sections
- Confusing similar field names (e.g., "Current Yield" vs. "Yield to Maturity")
- **Completing correct reasoning but selecting an answer option that contradicts the stated conclusion**
- **Applying this pattern to questions about separate data tables rather than terminal displays**

---
## Pattern: Table Sign Convention and Cash Flow Direction

**Description:** Financial tables use various conventions for indicating cash outflows (negative signs, parentheses, red text). Failure to correctly parse these signs leads to misaligned values in incremental analysis and NPV calculations.

**When to Use:** Questions involving cash flow analysis, incremental comparisons, or NPV calculations where tables show both inflows and outflows

**Procedure:**
1. Identify the sign convention used in the table (check for: minus signs "-", parentheses "()", color coding, or explicit labels like "outflow")
2. For each cash flow value, explicitly note its direction: "Year 0: -$950 (outflow)" or "Year 1: $700 (inflow)"
3. When extracting for calculations, preserve the sign: create a list with signs included [−950, 700, 550, 130]
4. For incremental analysis (Project A - Project B), subtract each corresponding year: Year_i(incremental) = CF_i(A) - CF_i(B)
5. Verify sign logic: initial investment incremental should be negative if Project A requires more upfront capital
6. Before final calculation, state: "Cash flows with signs: [list all values with +/− explicitly shown]"

**Example (sanitized):**
> **Scenario:** Table shows Project X: Year 0=(1200), Year 1=800, Year 2=600. Project Y: Year 0=(2000), Year 1=1400, Year 2=900. Question: "Calculate incremental IRR of Y over X."
> **Wrong approach:** Using Year 0 values as 1200 and 2000 (ignoring parentheses indicating outflows)
> **Correct approach:** (1) Sign convention: parentheses = outflows, (2) Project X: [-1200, 800, 600], (3) Project Y: [-2000, 1400, 900], (4) Incremental (Y-X): Year 0: -2000-(-1200)=-800, Year 1: 1400-800=600, Year 2: 900-600=300, (5) Incremental cash flows: [-800, 600, 300], (6) Solve for IRR of [-800, 600, 300]

## Pattern: Options Intrinsic Value and Time Value Anomaly Detection

**Description:** Options mispricing can occur through two distinct mechanisms: (1) trading below intrinsic value for in-the-money options, which violates arbitrage-free pricing, and (2) time value anomalies where longer-dated options are priced lower than shorter-dated options with identical strikes and moneyness. Models may focus on one type while missing the other, or incorrectly compare options with different moneyness levels.

**When to Use:** Questions asking to identify mispriced options from a table showing multiple strike prices, expiration dates, and last prices, especially when the current stock price is provided

**Procedure:**
1. **Extract key information:**
   - Current stock price: S = [value]
   - For each option, extract: Strike (K), Expiration, Type (Call/Put), Last Price (P)
2. **Check intrinsic value violations (arbitrage opportunities):**
   - For calls: Intrinsic Value = max(0, S - K)
   - For puts: Intrinsic Value = max(0, K - S)
   - **Rule:** Option price must be ≥ Intrinsic Value
   - Flag any option where P < Intrinsic Value as "clearly mispriced"
3. **Check time value anomalies (same strike, same moneyness):**
   - Group options by strike price and type (call/put)
   - Within each group, identify moneyness: ITM (in-the-money), ATM (at-the-money), OTM (out-of-the-money)
   - **Rule for same moneyness:** Longer expiration should have price ≥ shorter expiration
   - Calculate time value = Price - Intrinsic Value for each option
   - Flag if a longer-dated option has lower total price than a shorter-dated option with identical strike and moneyness
4. **Avoid false positives:**
   - Do NOT compare options with different strikes
   - Do NOT compare calls to puts
   - Do NOT flag time value differences between ITM and OTM options as anomalies (different moneyness = different pricing dynamics)
   - Do NOT expect linear time decay (time value increases non-linearly with time)
5. **Verify findings:**
   - State: "Option [X] is mispriced because [specific violation]"
   - For intrinsic value violations: "Price [P] < Intrinsic Value [IV], creating arbitrage opportunity"
   - For time value anomalies: "Option [A] expires [date1] priced at [P1], but option [B] expires [date2] priced at [P2], violating time value ordering for same strike and moneyness"

**Common Mistakes to Avoid:**
- Comparing options with different strikes or moneyness levels and concluding mispricing
- Expecting time value to increase linearly with time (it increases with square root of time)
- Identifying an option as mispriced based solely on "seems too high/low" without checking specific pricing rules
- Missing intrinsic value violations while focusing only on relative comparisons
- Confusing time value (extrinsic value) with total option price

**Example (sanitized):**
> **Scenario:** Stock trading at $75. March 70 call = $4.50, April 70 call = $6.20, July 70 call = $8.10. March 70 put = $0.40, July 70 put = $2.80, October 70 put = $2.50.
> **Wrong approach:** Concluding April call is mispriced because it's "too much higher" than March call, or missing the October put anomaly
> **Correct approach:** (1) Stock = $75, (2) Check intrinsic values: March 70 call intrinsic = max(0, 75-70) = $5.00, but price = $4.50 → **MISPRICED** (below intrinsic value), (3) All puts are OTM (intrinsic = 0), prices > 0, no intrinsic violations, (4) Time value check for 70 puts (all OTM): March put = $0.40, July put = $2.80, October put = $2.50 → October < July despite longer expiration → **MISPRICED** (time value anomaly), (5) April call ($6.20) vs March call ($4.50): difference of $1.70 for one additional month is reasonable given time value decay patterns, NOT mispriced, (6) Answer: March 70 call (intrinsic value violation) and October 70 put (time value anomaly)

---

**Summary of Changes:**
1. **REFINED** "Visual Dispersion Assessment in Scatter Plots" with mandatory cross-validation steps and explicit R² relationship
2. **NEW** "Options Intrinsic Value and Time Value Anomaly Detection" pattern to handle options mispricing questions systematically

These changes fix Q⁻ regressions while preserving Q⁺ correctness by adding guards and systematic validation without modifying the core logic that makes Q⁺ work.

## Pattern: Question Scope Identification and Missing Value Disambiguation

**Description:** When questions ask to "fill in missing value(s)" in tables with multiple blanks labeled (i), (ii), (iii), etc., models may misinterpret the scope by either: (1) attempting to solve ALL missing values when only ONE specific value is requested, or (2) solving the WRONG missing value due to misreading the question. This pattern ensures correct identification of which specific value(s) the question requests before proceeding with calculations.

**When to Use:** Questions containing phrases like "fill in the missing value in (X)" or "what is the value of (Y)" where a table contains multiple missing values with different labels

**Procedure:**
1. **Parse the question carefully** to identify the EXACT missing value(s) requested:
   - Look for specific references: "in (v)", "in (viii)", "for entry (ii)"
   - Note if the question asks for ONE value or MULTIPLE values
   - If the question says "fill in (v)" it means ONLY (v), not all missing values
2. **Locate the target position** in the table:
   - Identify which row and column contains the requested label
   - State explicitly: "Question asks for value (X), which is located in [row Y, column Z]"
3. **Identify the financial concept** for that specific position:
   - What does this cell represent? (e.g., "correlation of market with itself", "standard deviation of risk-free asset")
   - State: "Position (X) represents [concept]"
4. **Apply domain knowledge** for that specific concept:
   - Use definitional relationships (e.g., correlation with self = 1.0, risk-free std dev = 0)
   - Use formulas if calculation is required (e.g., beta = correlation × σ_security / σ_market)
5. **Verify the answer** makes sense for that position:
   - Check units and magnitude
   - Confirm consistency with other table values
6. **State the final answer** with explicit reference: "The missing value in (X) is [value]"

**Example (sanitized):**
> **Scenario:** Table shows securities data with missing values labeled (i) through (viii). Market portfolio row shows: Expected Return=0.12, Std Dev=0.20, Correlation=(iv), Beta=(v). Risk-free asset row shows: Expected Return=0.05, Std Dev=(vi), Correlation=(vii), Beta=(viii). Question asks: "Fill in the missing value in (v)."
> **Wrong approach:** Attempting to solve all missing values (i) through (viii), or solving for (vi) instead of (v)
> **Correct approach:** (1) Question asks specifically for value (v), (2) Locate (v): market portfolio row, beta column, (3) Concept: beta of market portfolio with itself, (4) Apply domain knowledge: by definition, the market portfolio has beta = 1.0 relative to itself, (5) Verify: beta=1.0 is consistent with market portfolio being the benchmark, (6) Answer: "The missing value in (v) is 1.0"

**Common Mistakes to Avoid:**
- Solving all missing values when only one is requested
- Solving the wrong missing value due to misreading the question
- Confusing similar labels (e.g., (v) vs (vi), (ii) vs (iii))
- Providing multiple answers when a single value is requested

---

## Pattern: Inventory Management and Shortage Cost Assessment

**Description:** Shortage costs arise when a company lacks sufficient inventory to meet customer demand. Models may incorrectly assess shortage risk by confusing inventory turnover rates with shortage vulnerability—higher turnover indicates FASTER depletion and GREATER shortage risk, not lower risk. The assessment must consider both the inventory-to-sales ratio and recent inventory changes that signal management's response to shortage concerns.

**When to Use:** Questions asking which company is "more likely to incur shortage costs" or "faces greater stockout risk" when comparing inventory positions across multiple firms

**Procedure:**
1. **Extract inventory and sales data** for each company:
   - Current year inventory: [value]
   - Prior year inventory: [value]
   - Cost of goods sold (COGS) or Sales: [value]
2. **Calculate inventory turnover** for each company:
   - Inventory Turnover = COGS / Average Inventory (or COGS / Current Inventory)
   - State: "Company A turnover = [X]x, Company B turnover = [Y]x"
3. **Interpret turnover correctly:**
   - **Higher turnover = faster inventory depletion = GREATER shortage risk** (less buffer)
   - **Lower turnover = slower inventory depletion = LOWER shortage risk** (more buffer)
   - State: "Company [X] with higher turnover ([value]) depletes inventory faster, indicating tighter inventory management"
4. **Analyze inventory trends:**
   - Calculate year-over-year inventory change: (Current - Prior) / Prior
   - **Significant inventory increases** suggest management is building buffer, possibly in response to past shortages or anticipated demand
   - State: "Company [X] increased inventory by [Y]%, suggesting [interpretation]"
5. **Assess relative shortage risk:**
   - Company with HIGHER turnover + INCREASING inventory = likely experienced or anticipates shortages
   - Company with LOWER turnover + STABLE/DECREASING inventory = comfortable with current levels
6. **State conclusion:** "Company [X] is more likely to incur shortage costs because: (1) higher inventory turnover ([A]x vs [B]x) indicates faster depletion, (2) recent inventory increase of [C]% suggests management response to shortage concerns"

**Example (sanitized):**
> **Scenario:** Company Alpha has inventory of $800K, COGS of $2,400K (turnover = 3.0x), and inventory increased 30% from prior year. Company Beta has inventory of $600K, COGS of $1,200K (turnover = 2.0x), and inventory decreased 5% from prior year. Question: "Which company is more likely to incur shortage costs?"
> **Wrong approach:** Concluding Beta faces greater shortage risk because it has lower absolute inventory, or concluding Alpha is safer because it increased inventory
> **Correct approach:** (1) Alpha turnover = 2,400/800 = 3.0x; Beta turnover = 1,200/600 = 2.0x, (2) Alpha has HIGHER turnover, meaning faster inventory depletion and tighter management, (3) Alpha's 30% inventory increase signals management is building buffer, likely due to past shortage concerns or anticipated demand, (4) Beta's lower turnover and declining inventory suggests comfortable inventory position, (5) Conclusion: Alpha is more likely to incur shortage costs because its higher turnover (3.0x vs 2.0x) indicates faster depletion and tighter inventory margins, and the significant inventory build-up suggests management is responding to shortage risk

**Common Mistakes to Avoid:**
- Confusing higher inventory turnover with lower shortage risk (opposite is true)
- Interpreting inventory increases as indicating safety rather than response to shortage concerns
- Focusing only on absolute inventory levels without considering turnover rates
- Ignoring the relationship between turnover speed and buffer adequacy

---

## Pattern: Tax Efficiency and Embedded Gain Assessment

**Description:** When evaluating mutual funds for tax efficiency "going forward," the primary determinant is the embedded gain ratio (unrealized gains as percentage of assets), which represents future tax liabilities. Models may incorrectly overweight secondary factors like capital loss carryforwards or absolute gain amounts, failing to recognize that the embedded gain PERCENTAGE is the dominant factor for future tax efficiency.

**When to Use:** Questions asking which investment is "most tax efficient going forward" when comparing funds with different embedded gains, asset bases, and potential tax attributes

**Procedure:**
1. **Extract key data** for each fund:
   - Total assets: [value]
   - Embedded gains (unrealized capital gains): [value]
   - Capital gains distributions (if any): [value]
   - Capital losses (if any): [value]
2. **Calculate embedded gain ratio** for each fund:
   - Embedded Gain Ratio = Embedded Gains / Total Assets
   - State: "Fund A: [X]% embedded gain, Fund B: [Y]% embedded gain, Fund C: [Z]% embedded gain"
3. **Interpret embedded gain ratio:**
   - **Lower ratio = more tax efficient going forward** (less future tax burden)
   - This ratio represents the percentage of the fund that will eventually trigger taxes when distributed
4. **Assess secondary factors** (only if embedded gain ratios are very close):
   - Capital loss carryforwards can offset SOME future gains, but do not eliminate the embedded gain burden
   - Calculate net embedded position: Embedded Gains - Capital Losses
   - Recalculate ratio if losses are substantial: (Embedded Gains - Losses) / Total Assets
5. **Apply decision hierarchy:**
   - **Primary criterion:** Select fund with LOWEST embedded gain ratio
   - **Secondary criterion:** If ratios differ by <2 percentage points, consider loss carryforwards as tiebreaker
   - **Do NOT:** Let loss carryforwards override a significantly lower embedded gain ratio
6. **State conclusion:** "Fund [X] is most tax efficient going forward because it has the lowest embedded gain ratio of [Y]%, meaning [interpretation]"

**Example (sanitized):**
> **Scenario:** Fund P has $5M assets, $500K embedded gains (10% ratio), $0 losses. Fund Q has $4M assets, $600K embedded gains (15% ratio), $150K capital losses. Fund R has $6M assets, $900K embedded gains (15% ratio), $0 losses. Question: "Which fund is most tax efficient going forward?"
> **Wrong approach:** Selecting Fund Q because its capital losses provide tax benefits, despite having a higher embedded gain ratio than Fund P
> **Correct approach:** (1) Calculate ratios: Fund P = 500K/5M = 10%, Fund Q = 600K/4M = 15%, Fund R = 900K/6M = 15%, (2) Fund P has lowest embedded gain ratio at 10%, (3) Assess Fund Q's losses: net embedded position = 600K - 150K = 450K, adjusted ratio = 450K/4M = 11.25%, still higher than Fund P's 10%, (4) Apply hierarchy: Fund P has lowest ratio (10% vs 11.25% vs 15%), (5) Conclusion: "Fund P is most tax efficient going forward because it has the lowest embedded gain ratio of 10%, meaning only 10% of the fund represents future tax liabilities, compared to 11.25% for Fund Q (after loss offset) and 15% for Fund R"

**Common Mistakes to Avoid:**
- Overweighting capital loss carryforwards relative to embedded gain ratios
- Comparing absolute dollar amounts of gains rather than ratios to asset base
- Selecting based on past distributions rather than future tax burden
- Ignoring that loss carryforwards only partially offset embedded gains, not eliminate them
- Confusing "tax efficient going forward" with "has generated tax benefits historically"