# Fixed Income — Quantitative Yield Curve and Portfolio Metrics

## Pattern: Butterfly_Spread_Calculation_and_Sign_Convention

**Description:** Butterfly spread measures the curvature of the yield curve by comparing the middle maturity yield to the average of short and long maturity yields. The sign convention is critical: a negative butterfly indicates the curve is more curved (convex) than linear interpolation would suggest.

**When to Use:** Questions involving "butterfly spread," "yield curve curvature," "butterfly position," or comparing three points on a yield curve with short, intermediate, and long maturities.

**Procedure:**
1. Identify three yield curve points: short-term yield (S), intermediate-term yield (M), and long-term yield (L)
2. Apply the butterfly spread formula: **Butterfly Spread = 2 × M - (S + L)**
3. Note the sign convention:
   - Negative butterfly: middle yield is lower than linear interpolation (curve is bowed downward/convex)
   - Positive butterfly: middle yield is higher than linear interpolation (curve is bowed upward/concave)
   - Zero butterfly: yields lie on a straight line
4. Convert to basis points if needed (multiply decimal by 10,000)
5. Verify the maturity spacing is approximately symmetric (e.g., 2-5-10 years, not 1-3-10 years) for standard butterfly interpretation

**Example (sanitized):**
> **Scenario:** A yield curve shows: 2-year at 2.50%, 5-year at 3.00%, 10-year at 3.75%. Calculate the butterfly spread.
> **Wrong approach:** (2.50% + 3.75%) - 2 × 3.00% = 6.25% - 6.00% = 0.25% = 25 bps
> **Correct approach:** 2 × 3.00% - (2.50% + 3.75%) = 6.00% - 6.25% = -0.25% = **-25 bps**. The negative value indicates the curve is more convex than a straight line between the 2-year and 10-year points.

---

## Pattern: Zero_Coupon_Bond_Portfolio_Convexity_Calculation

**Description:** Portfolio convexity for zero-coupon bonds requires calculating individual bond convexities using the maturity-squared formula with yield adjustment, then taking the present-value-weighted average. The full formula includes a denominator adjustment for yield, and using the simplified formula without this adjustment leads to significant errors. Qualitative reasoning about "dispersion" without quantitative calculation often leads to incorrect conclusions.

**When to Use:** Questions comparing convexity between portfolios containing zero-coupon bonds, especially barbell vs. bullet comparisons, or when asked "which portfolio has higher/lower convexity."

**When NOT to Use:** Questions asking for duration comparisons or "highest/lowest duration" - these require duration calculations, not convexity analysis. Do NOT confuse duration questions with convexity questions even when the same portfolio structures (barbell, bullet) are mentioned.

**Procedure:**
1. **VERIFY THE QUESTION TYPE FIRST:**
   - If the question asks about "duration" or "modified duration," this is NOT a convexity question
   - Only proceed with convexity calculation if the question explicitly asks about "convexity"
   - Duration and convexity are different metrics requiring different calculations

2. For each zero-coupon bond, calculate convexity using the FULL formula:
   - **Convexity = (Maturity)² / (1 + y)²**
   - Where y is the yield to maturity (as a decimal)
   - Do NOT use the simplified formula Convexity ≈ (Maturity)² unless explicitly performing a rough directional comparison
   - The yield adjustment is critical for accurate numerical comparisons
   
3. Calculate present value (PV) of each bond:
   - **PV = Face Value / (1 + y)^Maturity**
   - Use the specific yield for each bond
   
4. Calculate portfolio weights based on present values:
   - **Weight_i = PV_i / Total_PV**
   - Weights must sum to 1.0
   
5. Calculate weighted portfolio convexity:
   - **Portfolio Convexity = Σ(Weight_i × Convexity_i)**
   - Apply the full convexity formula from step 2, not the simplified version
   
6. Compare the calculated portfolio convexities numerically:
   - The portfolio with the lower numerical convexity value has "smaller" or "lower" convexity
   - The portfolio with the higher numerical convexity value has "greater" or "higher" convexity
   
7. **ANSWER THE ACTUAL QUESTION:**
   - If asked "which has highest convexity," select the portfolio with the highest calculated value
   - Do NOT second-guess or reinterpret the question after completing correct calculations
   - The question means what it says - trust your mathematical results
   
8. Formula selection guidance:
   - Use FULL formula (with yield adjustment): When comparing specific portfolios with numerical precision required
   - Use simplified formula (without yield adjustment): Only for quick directional insights or when yields are not provided
   - When in doubt, use the full formula for accuracy
   
9. Remember: For equal-duration portfolios, barbells generally have higher convexity than bullets, but the magnitude depends on the specific maturities, yields, and present values

**Common Mistakes to Avoid:**
- Using the simplified formula Convexity ≈ (Maturity)² when numerical precision is required
- Forgetting to divide by (1 + y)² in the convexity calculation
- Applying different formulas to different portfolios in the same comparison
- Confusing "smaller convexity" with "higher convexity" when interpreting numerical results
- **Applying convexity analysis to duration questions - these are completely different metrics**
- **Second-guessing correct calculations by reinterpreting what the question "really means"**
- **Changing your answer after correct analysis due to confusion about terminology**

**Example (sanitized):**
> **Scenario:** Portfolio X: $5,000 face value 2-year zero, $8,000 face value 12-year zero, both at 8% yield. Portfolio Y: 100% in 7-year zero at 8% yield with same total market value. Which has smaller convexity?
> **Wrong approach:** "Using simplified formula: Portfolio X convexity ≈ weight × 2² + weight × 12². Portfolio Y convexity ≈ 7² = 49. Just compare these directly."
> **Correct approach:** 
> - Calculate PVs: 2-year PV = 5,000/(1.08)² = 4,286.69; 12-year PV = 8,000/(1.08)¹² = 3,175.79
> - Total PV = 7,462.48; Weights: 2-year = 57.4%, 12-year = 42.6%
> - Use FULL formula with yield adjustment:
>   - 2-year convexity = 2²/(1.08)² = 4/1.1664 = 3.43
>   - 12-year convexity = 12²/(1.08)² = 144/1.1664 = 123.46
> - Portfolio X: 0.574 × 3.43 + 0.426 × 123.46 = 1.97 + 52.59 = **54.56**
> - Portfolio Y: 7²/(1.08)² = 49/1.1664 = **42.01**
> - Portfolio Y has **smaller convexity** (42.01 < 54.56). Using the simplified formula without yield adjustment would give incorrect values and potentially wrong comparison.

---
## Pattern: Bloomberg_Terminal_Yield_Field_Extraction

**Description:** When extracting yield data from Bloomberg terminal displays, specific field labels indicate where redemption yield (YTM) is located. "NOT PRICED" or blank yield fields mean the security is not actively traded and yield cannot be inferred from other characteristics. However, Bloomberg displays may show yield information in multiple locations, and for non-standard securities (floating rate notes, structured products), yield may appear in alternative fields or calculated sections rather than the primary yield field.

**When to Use:** Questions showing Bloomberg terminal screenshots asking for "redemption yield," "yield to maturity," "YTM," or similar yield metrics.

**Procedure:**
1. Identify the security type from the Bloomberg display:
   - Check for "CPN TYPE" field: FIXED, FLOATING, ZERO, STEP, etc.
   - Floating rate notes and structured products may display yield differently than fixed-rate bonds
   
2. Locate the primary yield field on the Bloomberg display:
   - Common labels: "Yield," "YTM," "Redemption Yield," "YLD TO MTY"
   - Typically appears in the upper section near price, coupon, and maturity
   
3. If primary yield field shows "NOT PRICED" or is blank, systematically check alternative yield locations:
   - Right side panel: Look for calculated yield fields or analytics section
   - Lower sections: Check for "Calculated Yield," "Indicative Yield," "Model Yield"
   - For floating rate notes: Look for "Spread," "Discount Margin," or "All-in Yield"
   - Scan ALL numerical values on screen that could represent yield (typically 0-20% range)
   
4. Check for data availability indicators:
   - "NOT PRICED" in primary field does NOT mean yield is unavailable elsewhere
   - Green/white text: live market data
   - Yellow/amber text: delayed or indicative data
   
5. For floating rate notes specifically:
   - Redemption yield may be calculated based on spread over reference rate
   - Look for fields showing total return or effective yield
   - May appear as "Yield" in a different section than fixed-rate bonds
   
6. If multiple yield values appear, prioritize based on question context:
   - "Redemption yield" → YTM or yield to maturity date
   - "Yield to Worst" → for callable bonds
   - "Current Yield" → coupon/price (less comprehensive)
   
7. Only conclude yield is unavailable after checking:
   - Primary yield field
   - All alternative yield fields
   - Calculated/analytics sections
   - Spread-based yields (for floating rate notes)
   
8. Read the exact numerical value displayed, including decimal places

**Example (sanitized):**
> **Scenario:** A Bloomberg screen shows a floating rate corporate note with Coupon Type: FLOATING, Reference Rate: LIBOR+150, Maturity: 2028. The primary "Yield" field displays "NOT PRICED," but in the analytics section on the right side, a field labeled "Calc Yld" shows 4.825%.
> **Wrong approach:** "The yield field shows 'NOT PRICED,' so the yield cannot be determined. I'll select an arbitrary answer or conclude data is unavailable."
> **Correct approach:** For floating rate securities, the primary yield field may show "NOT PRICED" because these securities don't have a fixed yield like traditional bonds. However, Bloomberg calculates an effective yield based on the current reference rate plus spread. Systematically scan the entire display for alternative yield fields. The "Calc Yld" field in the analytics section shows **4.825%**, which represents the redemption yield for this floating rate note.

**Common Mistakes to Avoid:**
- Concluding yield is unavailable after only checking the primary "Yield" field
- Failing to recognize that floating rate notes display yield differently than fixed-rate bonds
- Not systematically scanning the entire Bloomberg screen for alternative yield fields
- Assuming "NOT PRICED" in one field means no yield data exists anywhere on the display
```

---

```
## Pattern: Yield_Curve_Position_Interpretation

**Description:** Understanding how butterfly spreads and other yield curve metrics relate to trading positions and portfolio positioning requires recognizing that the calculation convention determines whether positive or negative values indicate specific curve shapes.

**When to Use:** Questions about "butterfly position," "curve positioning," "yield curve trades," or interpreting the meaning of calculated butterfly spreads in a portfolio context.

**Procedure:**
1. Calculate the butterfly spread using: 2 × M - (S + L)
2. Interpret the sign in context:
   - **Negative butterfly spread**: The curve is more convex (bowed) than linear
     - Middle rates are lower relative to wings
     - A "long butterfly" position profits from this (long middle, short wings)
   - **Positive butterfly spread**: The curve is more concave (humped) than linear
     - Middle rates are higher relative to wings
     - A "short butterfly" position profits from this (short middle, long wings)
3. For portfolio positioning:
   - If holding a barbell (short + long maturities): benefits from curve flattening or negative butterfly
   - If holding a bullet (middle maturity): benefits from curve steepening or positive butterfly
4. Changes in butterfly spread indicate:
   - Increasing (more positive): curve becoming more humped
   - Decreasing (more negative): curve becoming more bowed/convex

**Example (sanitized):**
> **Scenario:** A manager holds 2-year, 5-year, and 10-year bonds. The butterfly spread is calculated as -15 bps. What does this indicate?
> **Wrong approach:** "Negative means the position is losing money."
> **Correct approach:** The -15 bps butterfly spread indicates the 5-year yield is 15 bps lower than the average of 2-year and 10-year yields, meaning the curve is more convex (bowed downward) than a straight line. This is a descriptive measure of curve shape, not a profit/loss indicator. A portfolio overweighted in 5-year bonds would benefit if this negative butterfly becomes more negative (curve becomes more bowed).

---

## Pattern: Duration_Matched_Portfolio_Convexity_Comparison

**Description:** When comparing portfolios with identical durations, the portfolio with greater dispersion of cash flows (wider maturity spread) generally has higher convexity, but this must be verified through calculation for zero-coupon bonds using present-value weighting.

**When to Use:** Questions explicitly stating portfolios have "same duration" or "duration-matched" and asking to compare convexity, especially for barbell vs. bullet structures.

**Procedure:**
1. Verify that durations are stated as equal or calculate to confirm
2. For zero-coupon bond portfolios:
   - Calculate individual convexities: Convexity_i ≈ (Maturity_i)²
   - Weight by present value (market value) proportions
   - Sum to get portfolio convexity
3. For coupon-bearing bonds, use the full convexity formula or approximation
4. General rule (verify with calculation):
   - Barbell (short + long maturities) → higher convexity
   - Bullet (concentrated in middle maturity) → lower convexity
   - Ladder (evenly distributed) → intermediate convexity
5. The convexity difference provides value in volatile rate environments:
   - Higher convexity → better performance in large rate changes (either direction)
   - Lower convexity → less sensitivity to rate volatility

**Example (sanitized):**
> **Scenario:** Portfolio A: 40% in 1-year zero, 60% in 8-year zero. Portfolio B: 100% in 5-year zero. Both have 5-year duration. Compare convexity.
> **Wrong approach:** "Both have the same duration, so convexity should be similar."
> **Correct approach:** 
> - Portfolio A: Convexity ≈ 0.4 × (1²) + 0.6 × (8²) = 0.4 + 38.4 = 38.8
> - Portfolio B: Convexity ≈ 1.0 × (5²) = 25.0
> - Portfolio A has **higher convexity** (38.8 > 25.0) due to greater dispersion of maturities, even though durations are equal.

---

## Pattern: Convexity_Present_Value_Weighting_Error

**Description:** A common error in portfolio convexity calculation is using face value or equal weighting instead of present value (market value) weighting. For zero-coupon bonds with different maturities, present values differ significantly even with equal face values.

**When to Use:** Questions about portfolio convexity where bond amounts are given in face value terms (e.g., "$1 million face value of each bond") or when weights are not explicitly provided.

**Procedure:**
1. If face values are given, calculate present values:
   - PV = Face Value / (1 + y)^Maturity
   - Use the yield for each specific bond
2. Calculate market value weights:
   - Weight_i = PV_i / Σ(PV_i)
   - Weights must sum to 1.0
3. Note that shorter-maturity bonds have higher present values (closer to face value):
   - 1-year zero at 5% yield: PV ≈ 0.952 × Face
   - 10-year zero at 5% yield: PV ≈ 0.614 × Face
4. Apply weights to individual convexities:
   - Portfolio Convexity = Σ(Weight_i × Convexity_i)
5. Recognize that equal face value barbells are NOT equally weighted by market value:
   - Short-term bond has higher market value weight
   - This reduces the portfolio convexity compared to equal market value weighting

**Example (sanitized):**
> **Scenario:** A portfolio holds $100 face value of a 2-year zero and $100 face value of a 10-year zero, both yielding 4%. Calculate portfolio convexity.
> **Wrong approach:** "Equal face values mean 50/50 weighting. Convexity = 0.5 × (2²) + 0.5 × (10²) = 2 + 50 = 52."
> **Correct approach:**
> - PV of 2-year: 100/(1.04)² = 92.46
> - PV of 10-year: 100/(1.04)¹⁰ = 67.56
> - Total PV: 160.02
> - Weight of 2-year: 92.46/160.02 = 57.8%
> - Weight of 10-year: 67.56/160.02 = 42.2%
> - Portfolio Convexity = 0.578 × 4 + 0.422 × 100 = 2.31 + 42.2 = **44.5** (not 52)

---

## Pattern: Yield_Data_Source_Hierarchy_on_Terminal_Displays

**Description:** Bloomberg and other terminal displays may show multiple yield values for the same security (current yield, YTM, YTW, stripped yield, etc.). Understanding which yield to use requires recognizing the hierarchy and context of the question.

**When to Use:** Terminal screenshots showing multiple yield fields, or questions asking for specific yield types like "redemption yield," "yield to worst," or "current yield."

**Procedure:**
1. Identify the specific yield requested:
   - "Redemption yield" = Yield to Maturity (YTM)
   - "Yield to worst" = lowest yield among all call/put scenarios
   - "Current yield" = Annual coupon / Current price
   - "Stripped yield" = zero-coupon equivalent yield
2. Locate the corresponding field on the display:
   - YTM typically labeled: "Yield," "YTM," "Yld to Mat"
   - YTW typically labeled: "Yield to Worst," "YTW"
   - Current yield: "Current Yld," "Curr Yld"
3. Priority hierarchy when "yield" is requested without specification:
   - First: Yield to Maturity (most comprehensive for non-callable bonds)
   - Second: Yield to Worst (for callable/putable bonds)
   - Last: Current Yield (incomplete measure, ignores capital gains/losses)
4. Check for data quality indicators:
   - Green/white text: live market data
   - Yellow/amber text: delayed or indicative data
   - "NOT PRICED": no data available
5. If the primary yield field is unavailable, check for:
   - Indicative yields (model-based estimates)
   - Comparable security yields
   - Do NOT substitute coupon rate for yield

**Example (sanitized):**
> **Scenario:** A Bloomberg screen shows: Current Yld: 5.20%, YTM: 5.45%, YTW: 5.10%. The question asks for "the yield of the security."
> **Wrong approach:** "The first yield shown is 5.20%, so that's the answer."
> **Correct approach:** When "yield" is requested without specification, use Yield to Maturity (YTM) as the most comprehensive measure. The answer is **5.45%**. Current yield (5.20%) only considers coupon income, while YTM includes capital gains/losses to maturity.

---

SKILL_MD_ENTRY: | `fixed_income/quantitative_metrics.md` | Fixed Income | Quantitative Yield Curve and Portfolio Metrics | Butterfly_Spread_Calculation_and_Sign_Convention, Zero_Coupon_Bond_Portfolio_Convexity_Calculation, Bloomberg_Terminal_Yield_Field_Extraction, Yield_Curve_Position_Interpretation, Duration_Matched_Portfolio_Convexity_Comparison, Convexity_Present_Value_Weighting_Error, Yield_Data_Source_Hierarchy_on_Terminal_Displays |

## Pattern: Portfolio_Duration_Calculation_Simple_Weighted_Average

**Description:** Portfolio duration is calculated as the weighted average of individual bond durations, where weights are based on market values (present values). This is a straightforward calculation that does NOT require convexity analysis or complex formulas. Duration measures interest rate sensitivity, while convexity measures the curvature of the price-yield relationship - these are distinct metrics.

**When to Use:** Questions asking for "modified duration," "portfolio duration," "highest/lowest duration," or comparing duration across portfolio alternatives (bullet, barbell, equal-weight, etc.).

**Procedure:**
1. Identify the portfolio structures and their composition:
   - Bullet: concentrated in one maturity
   - Barbell: split between short and long maturities
   - Equal-weight: distributed across multiple maturities
   - Custom: any specified allocation

2. For each portfolio, calculate weighted average duration:
   - **Portfolio Duration = Σ(Weight_i × Duration_i)**
   - Where Weight_i is the proportion invested in bond i
   - Duration_i is the modified duration of bond i (usually provided in the data)

3. If weights are given as "equally" or "equal weights":
   - Equal weights means each position has weight = 1/n where n is number of positions
   - Example: "equally in 2-year and 9-year" means 50% each
   - Example: "equally in 2-year, 4.5-year, and 9-year" means 33.33% each

4. If market values or present values are provided instead of weights:
   - Calculate weights: Weight_i = Market_Value_i / Total_Market_Value
   - Then apply weighted average formula

5. Compare portfolio durations numerically:
   - Highest duration = largest numerical value
   - Lowest duration = smallest numerical value

6. Select the answer that matches your calculation:
   - If asked "highest duration," choose the portfolio with the largest calculated duration
   - Do NOT reinterpret the question or second-guess your correct calculation
   - Trust the mathematics

**Common Mistakes to Avoid:**
- Confusing duration with convexity - these are different metrics
- Using convexity formulas when the question asks about duration
- Second-guessing correct calculations by reinterpreting what "portfolio alternative" means
- Changing your answer after correct analysis due to misunderstanding terminology
- Forgetting that "equally" means equal weights, not equal market values

**Example (sanitized):**
> **Scenario:** Three portfolio strategies are available:
> - Strategy A (Bullet): 100% in 5-year bonds with duration 4.5
> - Strategy B (Barbell): 50% in 2-year bonds (duration 1.9) and 50% in 10-year bonds (duration 8.8)
> - Strategy C (Equal-weight): 33.33% each in 2-year (duration 1.9), 5-year (duration 4.5), and 10-year (duration 8.8)
> Which strategy has the highest modified duration?
> 
> **Wrong approach:** "This involves barbell and bullet portfolios, so I should use convexity analysis. Let me calculate convexity for each..." OR "The barbell has highest duration at 5.35, but the question asks for 'strategy' so maybe it means something else..."
> 
> **Correct approach:**
> - Strategy A duration: 1.0 × 4.5 = 4.5
> - Strategy B duration: 0.5 × 1.9 + 0.5 × 8.8 = 0.95 + 4.4 = 5.35
> - Strategy C duration: 0.333 × 1.9 + 0.333 × 4.5 + 0.333 × 8.8 = 0.633 + 1.499 + 2.930 = 5.06
> - Strategy B has the **highest modified duration** at 5.35. This is the answer - no reinterpretation needed.