# Skill Patterns for Visual Evidence Errors in Financial QA

## Pattern: OCR_Data_Reconstruction_and_Structured_Comparison

**Description:** Models fail to reconstruct complete structured data from fragmented OCR output and systematically compare all data points to apply financial principles like dominance, ranking, or elimination.

**When to Use:** When OCR text contains tabular financial data (returns, risks, prices, quantities) that must be compared across multiple entities to determine relationships like dominance, optimality, or ranking.

**Procedure:**
1. Parse OCR output to extract all numeric values and their associated labels (portfolio names, metrics like return/risk/price)
2. Reconstruct the complete data table with rows and columns clearly identified, filling in any obvious patterns if data appears incomplete
3. For each comparison question (e.g., efficient frontier, dominance, best/worst), systematically compare ALL pairs or entities rather than stopping at the first observation
4. Apply the relevant financial principle (e.g., portfolio A dominates B if A has higher return AND lower/equal risk, or equal return AND lower risk)
5. Verify that your conclusion is based on complete pairwise comparisons, not partial data

**Example (sanitized):**
> **Scenario:** OCR shows fragmented text: "Fund P: ret 8%, std 12% / Fund Q: ret 10%, std 12% / Fund R: ret 8%, std 15%"
> **Wrong approach:** Concluding "cannot determine" because data looks incomplete
> **Correct approach:** (1) Reconstruct table with 3 funds and 2 metrics each, (2) Compare P vs Q: Q dominates P (higher return, same risk), (3) Compare P vs R: P dominates R (same return, lower risk), (4) Compare Q vs R: Q dominates R (higher return, lower risk), (5) Conclude R cannot be efficient as it's dominated by both P and Q

---

## Pattern: Multi_Image_Reference_Tracking

**Description:** Models fail to track multiple image references in questions and match explicit image callouts (e.g., "table below <image_2>") to the correct data source, often defaulting to the first available image.

**When to Use:** When question text explicitly references specific images by number/position (e.g., "image_2", "table below", "following figure") and context contains multiple images or tables.

**Procedure:**
1. Identify all image references in the question text, noting explicit callouts like "image_2", "table below", "following chart"
2. Map each image reference to its position in the context (first image, second image, etc.)
3. When the question asks about specific data, use ONLY the image explicitly referenced, not the first or most prominent image
4. If an image reference is ambiguous, check if the question's data requirements (column names, metrics, entities) match only one of the available images
5. Cross-verify that extracted data matches the question's domain (e.g., if asking about "poor performance probability", look for probability distributions, not return percentages)

**Example (sanitized):**
> **Scenario:** Context shows <image_1> with bond yields and <image_2> with equity performance categories. Question: "Using the data in image_2, what is the probability of high growth?"
> **Wrong approach:** Extracting yield data from image_1 because it appears first
> **Correct approach:** (1) Question explicitly references image_2, (2) Locate image_2 in context, (3) Extract probability distribution for performance categories from image_2, (4) Find "high growth" probability value

---

## Pattern: Portfolio_Context_Specific_Risk_Relevance

**Description:** Models misunderstand which risk metrics matter based on portfolio diversification context—specifically, failing to recognize that specific/idiosyncratic risk is irrelevant when adding to well-diversified portfolios.

**When to Use:** When questions ask about adding securities to "well-diversified" or "diversified" portfolios and data shows both systematic risk (beta) and specific/idiosyncratic risk.

**Procedure:**
1. Identify the portfolio context: is it well-diversified, concentrated, or unspecified?
2. If well-diversified: specific risk is already eliminated through diversification, so focus on systematic risk (beta), expected return, or contribution to portfolio objectives
3. If concentrated or building from scratch: both specific and systematic risk matter
4. For well-diversified portfolios, do NOT prioritize low specific risk as a selection criterion—it provides no marginal benefit
5. Compare securities based on systematic risk-return tradeoffs or other portfolio-level metrics

**Example (sanitized):**
> **Scenario:** Adding to a well-diversified portfolio. Stock M: beta 1.2, high specific risk. Stock N: beta 1.2, low specific risk.
> **Wrong approach:** Choosing Stock N because it has lower specific risk
> **Correct approach:** (1) Portfolio is well-diversified, so specific risk is already diversified away, (2) Both stocks have identical beta (systematic risk), (3) Specific risk difference is irrelevant to portfolio risk, (4) Choose based on other factors like expected return, liquidity, or costs—not specific risk

---

## Pattern: Visual_Scatter_Plot_Dispersion_Assessment

**Description:** Models incorrectly assess the tightness of data point clustering around regression lines when comparing scatter plots, leading to wrong R² comparisons.

**When to Use:** When questions ask to compare R², goodness of fit, or correlation strength across multiple scatter plots or regression charts.

**Procedure:**
1. For each scatter plot, identify the regression line (usually drawn through the data)
2. Assess vertical distance of data points from the regression line—smaller average distance means higher R²
3. Compare the relative spread: tighter clustering (points closer to line) = higher R², wider spread = lower R²
4. Be careful with visual illusions: check axis scales, as different scales can make the same spread appear different
5. If charts show different axis ranges, mentally normalize to compare actual proportional spread
6. Verify chart labels match the entities being compared (Stock A vs Stock B)

**Example (sanitized):**
> **Scenario:** Two charts show regression lines. Chart 1 has points scattered ±5 units from line. Chart 2 has points scattered ±2 units from line.
> **Wrong approach:** Claiming Chart 1 has higher R² because the line looks steeper
> **Correct approach:** (1) Measure vertical spread from regression line in each chart, (2) Chart 2 has tighter clustering (±2 vs ±5), (3) Tighter clustering means higher R², (4) Chart 2's security has higher R²

---

## Pattern: Bloomberg_Terminal_Field_Location_and_Missing_Data_Recognition

**Description:** Models attempt to infer missing financial metrics from Bloomberg screenshots rather than recognizing that specific fields have designated locations and "NOT PRICED" or blank fields indicate unavailable data. Additionally, models may apply faulty rounding logic when matching extracted values to multiple-choice options, selecting psychologically appealing round numbers over mathematically closest values.

**When to Use:** When questions ask for specific metrics (yield, price, spread, 52-week high/low, etc.) from Bloomberg terminal screenshots.

**When NOT to Use:** 
- When the exact value is clearly visible and the question requires selecting the numerically closest answer choice (use standard numerical comparison instead)
- When the question asks for calculations or derived metrics rather than direct field extraction

**Procedure:**
1. Identify the specific metric requested (redemption yield, current price, spread, 52-week high, etc.)
2. Locate the designated field area for that metric on Bloomberg displays (yields typically in pricing sections, ratings in credit sections, price statistics in stock data sections)
3. Extract the EXACT numeric value shown in the field (e.g., "52Wk High 7/19/1999 USD 10034" means $100.34)
4. Check if the field shows "NOT PRICED", "N/A", is blank, or contains actual data
5. If the field is missing or marked unavailable, do NOT infer the value from other attributes (security type, issuance date, ratings)
6. **When matching to answer choices:** Calculate the absolute difference between the extracted value and each option, then select the option with the SMALLEST absolute difference (e.g., $100.34 is closer to $100.75 [diff: $0.41] than to $100.00 [diff: $0.34])
7. Only conclude "cannot be determined" if data is truly unavailable, not when exact matching requires standard numerical comparison

**Common Mistakes to Avoid:**
- Selecting round numbers ($100.00) over mathematically closer values ($100.75) when the extracted value is $100.34
- Applying psychological rounding preferences instead of calculating absolute differences
- Confusing "field extraction" tasks with "closest match selection" tasks—both require precision but the latter needs explicit numerical comparison

**Example (sanitized):**
> **Scenario:** Bloomberg screenshot shows "52-Week High: $87.63" and answer choices are A) $87.50, B) $88.00, C) $87.25, D) $87.75
> **Wrong approach:** Selecting B ($88.00) because it's a round number close to $87.63
> **Correct approach:** (1) Extract exact value: $87.63, (2) Calculate differences: |87.63-87.50|=0.13, |87.63-88.00|=0.37, |87.63-87.25|=0.38, |87.63-87.75|=0.12, (3) Select D ($87.75) as it has the smallest absolute difference (0.12)

---

**Summary of Changes:**
- Added explicit guidance on numerical comparison when matching extracted values to answer choices
- Added "When NOT to Use" section to prevent over-application to straightforward extraction-and-match scenarios
- Added step 6 with concrete formula for selecting closest answer choice
- Added "Common Mistakes to Avoid" section highlighting the Q⁻ regression pattern (faulty rounding logic)
- Added example demonstrating correct numerical comparison methodology
- Preserved all original functionality that made Q⁺ cases work (field location identification, "NOT PRICED" recognition, no inference from other fields)
## Pattern: Date_Format_Truncation_and_Contextual_Year_Inference

**Description:** Models misinterpret truncated date formats (e.g., "6/30/2" for "6/30/02" or "6/30/2002") by taking them literally rather than applying contextual reasoning about document dates and security lifecycles.

**When to Use:** When financial documents show dates with truncated or abbreviated year formats, especially in Bloomberg terminals, trade confirmations, or historical documents.

**Procedure:**
1. Identify the document date or screenshot timestamp (often at bottom of Bloomberg screens)
2. When encountering truncated years (e.g., "6/30/2", "12/15/7"), determine the century context from the document date
3. Apply financial logic: active securities cannot have maturity dates in the past if the document shows current data (ratings, outstanding amounts, next call dates)
4. For dates in the 1990s-2000s era, "2" likely means "02" (2002), not year 2 AD or an already-passed date
5. Calculate time-to-maturity from document date to interpreted maturity date to verify reasonableness
6. Cross-check with other temporal fields (first settle date, announce date) to confirm century interpretation

**Example (sanitized):**
> **Scenario:** Bloomberg screenshot dated "15-Mar-98" shows bond with "MATURITY DT 3/15/8" and active "NEXT CALL DT 3/15/3"
> **Wrong approach:** Interpreting maturity as March 15, year 8 AD, concluding bond has matured
> **Correct approach:** (1) Document is from 1998, (2) "3/15/8" in this context means 3/15/08 (2008), (3) Next call "3/15/3" means 3/15/03 (2003), (4) Bond matures in 10 years (1998→2008), (5) Status is "active with ~10 years to maturity"

---

## Pattern: Order_Book_Sequential_Liquidity_Consumption

**Description:** Models treat market orders in isolation rather than recognizing that order books consume liquidity sequentially, requiring subsequent orders to fill at progressively worse prices.

**When to Use:** When questions ask about "next" market order fills, order book depth, or sequential trade execution in limit order books.

**Procedure:**
1. Identify the current best bid and best ask prices in the limit order book
2. For the first market buy order, it fills at the best ask price up to available quantity
3. For the NEXT market buy order (or if quantity exceeds best ask), recognize that the best ask level is now exhausted
4. The next order must fill at the second-best ask price (next price level up in the sell orders)
5. Continue this sequential consumption logic for each subsequent order
6. Verify the question asks for "next" or "subsequent" order, not the first order

**Example (sanitized):**
> **Scenario:** Order book shows: Sell orders at $20.10 (100 shares), $20.15 (200 shares), $20.25 (150 shares). Question: "At what price would the next market buy order be filled?"
> **Wrong approach:** Answering $20.10 (the current best ask)
> **Correct approach:** (1) Current best ask is $20.10 for 100 shares, (2) "Next" implies the $20.10 level is consumed, (3) After $20.10 is exhausted, next level is $20.15, (4) The next market buy order fills at $20.15

---

## Pattern: Cash_Flow_Sign_Convention_from_Perspective_Keywords

**Description:** Models fail to correctly assign positive/negative signs to cash flows based on perspective keywords like "offered", "receive", "must pay", "make payments", leading to incorrect NPV calculations.

**When to Use:** When questions present cash flow scenarios with natural language descriptions (not just tables) using terms like "offered today", "payments you must make", "receive", "pay out".

**Procedure:**
1. Identify the perspective: are you the receiver or payer? Keywords: "you receive/offered to you" = inflow (+), "you pay/must make payment" = outflow (-)
2. For initial amounts: "offered $X today" or "receive $X now" = positive inflow at t=0
3. For subsequent amounts: "payments you must make" or "you must pay" = negative outflows (even if shown as positive numbers in tables)
4. Carefully read the question setup: if it says "offered $X but must make the following payments", ALL subsequent values are outflows (-)
5. Apply correct signs before discounting: NPV = Initial_Inflow - PV(Payment_1) - PV(Payment_2) - ...
6. Verify that the sign convention makes economic sense: accepting money today (+) and paying it back later (-) should often yield negative NPV if payments exceed initial amount

**Example (sanitized):**
> **Scenario:** "You receive $5,000 today but must make payments of $2,000 in year 1, $2,500 in year 2, and $1,000 in year 3."
> **Wrong approach:** NPV = $5,000 + PV($2,000) + PV($2,500) + PV($1,000) = large positive number
> **Correct approach:** (1) "Receive today" = +$5,000 inflow, (2) "Must make payments" = all subsequent amounts are outflows, (3) NPV = +$5,000 - PV($2,000) - PV($2,500) - PV($1,000), (4) Calculate with correct signs to get true NPV

---

## Pattern: Visual_Label_to_Answer_Choice_Mapping

**Description:** Models fail to map visual evidence labels (Portfolio A, Stock X, Chart 1) to answer choices or ground truth references, treating them as independent namespaces rather than recognizing they must correspond.

**When to Use:** When visual evidence uses one labeling system (A/B, X/Y, Chart 1/2) but the question or answer choices use different labels, requiring explicit mapping.

**Procedure:**
1. Extract all entity labels from visual evidence (e.g., Portfolio A, Portfolio B from table)
2. Extract all entity labels from question and answer choices (e.g., Stock X, Stock Y)
3. Recognize that these labels must map to each other—they refer to the same entities with different names
4. Use contextual clues to establish mapping: position (first in table = first mentioned), attributes (high risk portfolio = Stock X), or explicit statements
5. Before selecting an answer, verify which visual label corresponds to which answer choice label
6. If mapping is ambiguous, check if the question provides additional context (e.g., "Stock X has high specific risk" maps to "Portfolio A: High specific risk")

**Example (sanitized):**
> **Scenario:** Table shows "Option 1: Return 8%, Risk 10%" and "Option 2: Return 6%, Risk 12%". Question asks: "Which investment, Alpha or Beta, has better risk-adjusted returns?" with context stating "Alpha is the higher-return option."
> **Wrong approach:** Answering based on Option 1 vs Option 2 labels without mapping to Alpha/Beta
> **Correct approach:** (1) Visual shows Option 1 and Option 2, (2) Question asks about Alpha and Beta, (3) Context states "Alpha is higher-return option", (4) Map: Alpha = Option 1 (8% return), Beta = Option 2 (6% return), (5) Calculate risk-adjusted returns for Alpha and Beta using mapped data