# Skill Patterns for Visual Evidence Errors in Financial QA

## Pattern: Column-to-Data Alignment in Tables

**Description:** When extracting values from multi-column tables, models may misalign column headers with data rows, reading values from the wrong column. This occurs especially when similar numerical values appear across columns or when column headers are spatially distant from data cells.

**When to Use:** Any question requiring extraction of specific values from tabular data with multiple columns (e.g., "Calculate X for Stock B," "What is the return in state Y?")

**Procedure:**
1. Identify the exact column header(s) mentioned in the question (e.g., "Stock B," "Limit Sell Orders")
2. Trace vertically from the header to locate the correct column position in the table
3. For each required row, move horizontally from the row label to intersect with the identified column
4. Extract the value at the intersection point and label it explicitly (e.g., "Stock B Bear return = 0.108")
5. Before proceeding with calculations, verify all extracted values by stating: "From column [X], row [Y]: value = [Z]"
6. Cross-check that the number of extracted values matches the expected count for the calculation

**Example (sanitized):**
> **Scenario:** A table shows quarterly revenues for Division P and Division Q across Q1-Q4. Question asks: "What is the average revenue for Division Q?"
> **Wrong approach:** Reading Division P's column values (120, 135, 140, 150) instead of Division Q's values
> **Correct approach:** (1) Identify target column: "Division Q", (2) Trace to column position (rightmost data column), (3) Extract Division Q values row-by-row: Q1=95, Q2=110, Q3=105, Q4=125, (4) State extraction: "Division Q revenues: [95, 110, 105, 125]", (5) Calculate average = (95+110+105+125)/4 = 108.75

---

## Pattern: Order Book Depth and Sequential Execution Logic

**Description:** In limit order book questions, "next" order execution implies movement through price levels sequentially, not just identifying the current best bid/ask. Contextual clues like "last trade at price X" combined with "next order" indicate the best price may be consumed or unavailable.

**When to Use:** Questions about order execution in limit order books containing phrases like "next market order," "following trade," or providing context about recent transaction prices

**Procedure:**
1. Identify the order direction (buy orders execute against asks; sell orders execute against bids)
2. Locate the best available price level for that direction in the current order book
3. Check for contextual clues: if "last trade at price X" is mentioned and X equals the best price, consider whether that level is consumed
4. If the question asks for "next" execution after a reference trade, move to the second-best price level
5. State explicitly: "Best ask is [price1] with [quantity] shares; next level is [price2] with [quantity] shares"
6. Verify the interpretation by checking if the answer makes sense given the market context (e.g., price should be worse than the best quote for "next" orders)

**Example (sanitized):**
> **Scenario:** Order book shows best bid $48.50 (200 shares), best ask $48.75 (300 shares). Last trade occurred at $48.75. Question: "At what price will the next market buy order execute?"
> **Wrong approach:** Answering $48.75 (current best ask)
> **Correct approach:** (1) Market buy executes against asks, (2) Best ask = $48.75, (3) Last trade at $48.75 suggests this level may be consumed, (4) Next ask level = $49.00, (5) Answer: $49.00 for the next market buy order

---

## Pattern: Numerical Proximity Matching in Multiple Choice

**Description:** When the true value falls between multiple-choice options without an exact match, select the option with minimum absolute difference from the true value, not the nearest round number or value obtained by directional rounding.

**When to Use:** Multiple-choice questions where extracted numerical values don't exactly match any option (trigger: true value falls between two consecutive options)

**Procedure:**
1. Extract the true value from the source (e.g., from terminal display, table, or calculation)
2. Calculate absolute difference for each option: |option - true_value|
3. Create a comparison table: Option A: diff = X, Option B: diff = Y, etc.
4. Select the option with the smallest absolute difference
5. Do NOT apply rounding rules (round up/down) or assume "closest round number" heuristics
6. Verify: State "True value [V] is closest to option [X] with difference [D]"

**Example (sanitized):**
> **Scenario:** Calculated beta = 1.237. Options: A. 1.50, B. 1.20, C. 1.00, D. 1.25
> **Wrong approach:** Choosing B (1.20) as the "nearest round number" or D (1.25) by rounding to nearest 0.25
> **Correct approach:** (1) True value = 1.237, (2) Calculate differences: |1.50-1.237|=0.263, |1.20-1.237|=0.037, |1.00-1.237|=0.237, |1.25-1.237|=0.013, (3) Minimum difference = 0.013 for option D, (4) Answer: D (1.25)

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

**Description:** When comparing residual variance or firm-specific risk across regression plots, models may incorrectly assess which dataset shows greater vertical scatter around the fitted line, potentially due to visual anchoring on slope or horizontal spread.

**When to Use:** Questions asking to compare "firm-specific risk," "residual variance," "unexplained variation," or "scatter around regression line" across multiple scatter plots

**Procedure:**
1. Identify that firm-specific risk corresponds to vertical deviation from the regression line (residuals), not slope or R²
2. For each plot, focus exclusively on the vertical distance of points from their respective fitted lines
3. Systematically examine multiple points along each regression line: at low, medium, and high x-values
4. Estimate average vertical deviation for each plot: "Plot A: typical vertical distance ≈ [value], Plot B: typical vertical distance ≈ [value]"
5. Compare the magnitudes: larger average vertical deviation = higher firm-specific risk
6. Verify by checking extreme points: which plot has points furthest from its line in the vertical direction?

**Example (sanitized):**
> **Scenario:** Two scatter plots with regression lines. Stock M has points tightly clustered around a steep line. Stock N has points widely dispersed around a flatter line.
> **Wrong approach:** Concluding Stock M has higher risk because of steeper slope (confusing beta with residual variance)
> **Correct approach:** (1) Firm-specific risk = vertical scatter, not slope, (2) Stock M: points within ±2 units vertically from line, (3) Stock N: points within ±8 units vertically from line, (4) Stock N shows greater vertical dispersion, (5) Answer: Stock N has higher firm-specific risk

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

**Description:** When answering questions about specific values from financial terminal screenshots, models may substitute domain knowledge or plausibility reasoning instead of systematically scanning for explicitly displayed fields, leading to fabricated answers.

**When to Use:** Any question asking "what is the [specific field]" from a Bloomberg/Reuters/financial terminal screenshot (trigger: "as shown on the display," "according to the terminal")

**Procedure:**
1. Identify the exact field name requested (e.g., "redemption yield," "52-week high," "beta")
2. List common field labels for that metric (e.g., redemption yield might appear as: "YTM," "Yield," "Red Yield," "Yld to Mat")
3. Systematically scan the terminal screenshot for these labels, moving section by section (header → left column → right column → bottom)
4. If field is found, extract the adjacent value exactly as displayed
5. If field is NOT found after complete scan, state: "The field [X] is not visible in the provided screenshot"
6. Do NOT infer, estimate, or calculate the value based on other visible fields unless explicitly instructed
7. Verify: "Field [X] located in [section], value displayed = [Y]"

**Example (sanitized):**
> **Scenario:** Terminal screenshot shows various bond fields. Question: "What is the yield to maturity shown on the terminal?"
> **Wrong approach:** Calculating YTM from coupon rate and price, or stating "typical YTM for this type of bond would be 5.5%"
> **Correct approach:** (1) Target field: Yield to Maturity, (2) Possible labels: "YTM," "Yield," "Yld to Mat," (3) Scan header section: no match, (4) Scan left column: found "YTM 4.375", (5) Extract value: 4.375%, (6) Answer: "The yield to maturity shown is 4.375%"

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