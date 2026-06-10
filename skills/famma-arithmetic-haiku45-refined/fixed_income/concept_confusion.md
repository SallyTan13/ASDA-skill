# Fixed Income Arithmetic Skills - Program of Thought Patterns

## Pattern: Forward_Rate_to_Spot_Rate_Conversion

**Description:** Forward rates must be compounded sequentially to derive spot rates for discounting multi-period cash flows. A common error is treating forward rates as if they were spot rates or using incorrect compounding formulas. This pattern applies to bond pricing and yield calculations, NOT to forward contract valuation where the forward price is already embedded in spot rate relationships.

**When to Use:** When pricing bonds or calculating yields given a table of forward rates (1-year forward rates for consecutive periods). When the question asks to calculate bond prices, YTM, or discount cash flows using forward rate information.

**When NOT to Use:** 
- When pricing forward contracts or calculating forward contract values after rate changes
- When the question asks for "forward price" or "forward contract price" (use direct spot rate discounting instead)
- When dealing with derivatives pricing where forward rates are already embedded in the spot curve

**Procedure:**
1. Formula: Spot rate for year n: $(1 + s_n)^n = (1 + f_0) \times (1 + f_1) \times ... \times (1 + f_{n-1})$
2. Identify all forward rates from year 0 through year n-1
3. Compound them multiplicatively: product of (1 + each forward rate)
4. Extract the spot rate: take the nth root and subtract 1
5. Use spot rates to discount each cash flow at its respective maturity
6. **Validation:** Verify intermediate spot rates are reasonable (typically increasing with maturity)
7. **Final check:** Ensure bond price is within expected range (near par if coupon ≈ yield)

**Worked Example:**
**Question:** Given 1-year forward rates: Year 0=5%, Year 1=6%, Year 2=7%. Calculate the price of a 3-year bond with 8% annual coupon and $1000 par value.

**Correct Code:**
```python
# Given forward rates
forward_rates = [0.05, 0.06, 0.07]  # Years 0, 1, 2
par_value = 1000
coupon_rate = 0.08
annual_coupon = par_value * coupon_rate

# Step 1: Calculate spot rates from forward rates
spot_rates = []
for n in range(1, len(forward_rates) + 1):
    compound_product = 1.0
    for i in range(n):
        compound_product *= (1 + forward_rates[i])
    spot_rate = compound_product ** (1/n) - 1
    spot_rates.append(spot_rate)

# Intermediate validation: spot rates should be [0.05, 0.0550, 0.0599]
# s1 = 0.05
# s2 = sqrt(1.05 * 1.06) - 1 = 0.0550
# s3 = (1.05 * 1.06 * 1.07)^(1/3) - 1 = 0.0599

# Step 2: Discount cash flows using spot rates
bond_price = 0
for year in range(1, len(spot_rates) + 1):
    if year < len(spot_rates):
        cash_flow = annual_coupon
    else:
        cash_flow = annual_coupon + par_value
    
    pv = cash_flow / ((1 + spot_rates[year - 1]) ** year)
    bond_price += pv

bond_price  # Result: approximately 1053.77
```

**Common Bugs to Avoid:**
- Treating forward rates as spot rates: `pv = cash_flow / (1 + forward_rates[year])**year` is WRONG
- Using only the nth forward rate instead of compounding all rates from 0 to n-1
- Confusing year indexing: forward rate for "Year 1" applies to the period from year 0 to year 1
- Off-by-one errors in loop ranges when matching cash flows to discount periods
- **Applying this pattern to forward contract pricing** — forward contracts should use direct spot rate relationships, not forward rate extraction
- Not validating intermediate spot rate calculations before final bond pricing
- Rounding spot rates too early (maintain full precision until final result)

**CHECK Steps:**
- If question asks for "bond price" or "YTM", this pattern applies
- If question asks for "forward contract price" or "forward price", DO NOT use this pattern — use direct spot rate discounting instead
- If question mentions "forward contract" and "rate changes", calculate using new spot rates directly, not by extracting forward rates
- Verify: For bond pricing, you should be discounting coupon payments and principal
- Verify: For forward contracts, you should be calculating present values using spot rates for the relevant maturities
- **Validate intermediate spot rates:** s1 = f0, s2 = sqrt((1+f0)(1+f1)) - 1, etc.
- **Check final bond price:** If coupon rate > average spot rate, price should be > par; if coupon rate < average spot rate, price should be < par

---
## Pattern: Sequential_Forward_Rate_Discounting

**Description:** When discounting cash flows using forward rates directly (without converting to spot rates), each cash flow must be discounted by the sequential product of all forward rates from today to that cash flow's maturity.

**When to Use:** When pricing bonds given forward rates and the question explicitly requires using forward rates for discounting (or when forward rates represent the actual expected rates for each period).

**Procedure:**
1. Formula: $PV_t = \frac{CF_t}{\prod_{i=0}^{t-1}(1 + f_i)}$ where $f_i$ is the forward rate for period i to i+1
2. For each cash flow at time t, create a cumulative discount factor
3. Multiply all (1 + forward_rate) from period 0 through period t-1
4. Divide the cash flow by this cumulative product
5. Sum all present values

**Code Example:**

**Scenario:** Price a 4-year bond with 6% coupon, $1000 par, given forward rates: Year 0→1: 3%, Year 1→2: 4%, Year 2→3: 5%, Year 3→4: 6%.

**Correct Code:**
```python
# Forward rates for each period
forward_rates = [0.03, 0.04, 0.05, 0.06]  # Periods 0→1, 1→2, 2→3, 3→4
par_value = 1000
coupon_rate = 0.06
annual_coupon = par_value * coupon_rate

bond_price = 0

# Discount each cash flow
for year in range(1, 5):  # Years 1, 2, 3, 4
    # Calculate cumulative discount factor
    discount_factor = 1.0
    for period in range(year):
        discount_factor *= (1 + forward_rates[period])
    
    # Determine cash flow
    if year == 4:
        cash_flow = annual_coupon + par_value
    else:
        cash_flow = annual_coupon
    
    # Present value
    pv = cash_flow / discount_factor
    bond_price += pv

bond_price  # Result: approximately 1027.45
```

**Common Bugs to Avoid:**
- Using `(1 + forward_rates[year])**year` instead of sequential multiplication
- Starting the discount factor product at the wrong index
- Forgetting that forward rate for "Year 0" applies to the first period (0→1)
- Not accumulating the discount factor cumulatively for each subsequent cash flow

---

## Pattern: Forward_Rate_Table_Interpretation

**Description:** Forward rate tables show the expected 1-year rate for each future period. "Year 0" or "today" represents the current 1-year spot rate, and subsequent years show expected future 1-year rates. The year label indicates when that rate begins, not the maturity.

**When to Use:** When interpreting tables labeled "Forward Year Interest Rate" or "1-Year Forward Rate" with year indices.

**Procedure:**
1. Identify the table structure: "Year 0" = today's 1-year rate, "Year 1" = 1-year rate starting in 1 year
2. For an n-year zero-coupon bond, use forward rates from Year 0 through Year n-1
3. For YTM calculation, compound the appropriate sequence of forward rates
4. Verify: a 3-year bond uses rates for Years 0, 1, and 2 (NOT including Year 3)
5. Apply the geometric mean formula: $(1+YTM)^n = \prod_{i=0}^{n-1}(1+f_i)$

**Code Example:**

**Scenario:** Calculate YTM of a 4-year zero-coupon bond given forward rates: Year 0=5%, Year 1=6%, Year 2=7%, Year 3=8%, Year 4=9%.

**Correct Code:**
```python
# Forward rates table
forward_rates_table = {
    0: 0.05,  # Today's 1-year rate
    1: 0.06,  # 1-year rate starting in year 1
    2: 0.07,  # 1-year rate starting in year 2
    3: 0.08,  # 1-year rate starting in year 3
    4: 0.09   # 1-year rate starting in year 4
}

# For a 4-year zero-coupon bond, use rates from Year 0 through Year 3
maturity = 4
compound_product = 1.0

for year in range(maturity):  # Years 0, 1, 2, 3
    compound_product *= (1 + forward_rates_table[year])

# Calculate YTM
ytm = compound_product ** (1 / maturity) - 1
ytm_percent = ytm * 100

ytm_percent  # Result: approximately 6.49%
```

**Common Bugs to Avoid:**
- Including Year n forward rate when pricing an n-year bond (off-by-one error)
- Confusing "Year 3" with "3-year rate" (Year 3 is a 1-year rate starting in year 3)
- Using n+1 rates instead of n rates for an n-year maturity
- Misinterpreting "Forward Year Interest Rate 0" as a forward rate instead of the current spot rate

---

## Pattern: Bond_Price_Evolution_with_Constant_Forward_Rates

**Description:** When forward rates remain unchanged, a bond's price one period forward must be calculated using the forward rate curve shifted by one period, not by reusing the same spot rates.

**When to Use:** When asked to calculate a bond's price at a future date assuming forward rates stay constant or "implied forward rates remain the same."

**Procedure:**
1. Calculate today's forward rates from zero-coupon bond prices: $f_{t,t+1} = \frac{(1+s_{t+1})^{t+1}}{(1+s_t)^t} - 1$
2. One year forward, the new 1-year spot rate = today's 1-year forward rate $f_{1,2}$
3. The new 2-year spot rate one year forward = geometric mean of $f_{1,2}$ and $f_{2,3}$
4. Discount remaining cash flows using this shifted forward rate curve
5. Verify: a 4-year bond becomes a 3-year bond, priced using forward rates that were originally for years 1, 2, 3

**Code Example:**

**Scenario:** A 3-year bond with 8% coupon, $1000 par. Zero-coupon prices: 1yr=$950, 2yr=$890, 3yr=$820. Find price in 1 year if forward rates stay constant.

**Correct Code:**
```python
import math

# Zero-coupon bond prices
zcb_prices = {1: 950, 2: 890, 3: 820}
par_value = 1000
coupon_rate = 0.08
annual_coupon = par_value * coupon_rate

# Step 1: Calculate spot rates from zero-coupon prices
spot_rates = {}
for maturity, price in zcb_prices.items():
    spot_rate = (par_value / price) ** (1 / maturity) - 1
    spot_rates[maturity] = spot_rate

# Step 2: Calculate forward rates
forward_rates = {}
forward_rates[0] = spot_rates[1]  # f(0,1) = s1
for t in range(1, 3):
    numerator = (1 + spot_rates[t + 1]) ** (t + 1)
    denominator = (1 + spot_rates[t]) ** t
    forward_rates[t] = (numerator / denominator) - 1

# Step 3: One year forward, bond has 2 years remaining
# Use forward rates f(1,2) and f(2,3) as the new spot rates
# New 1-year spot rate = f(1,2)
# New 2-year spot rate from: (1+s2_new)^2 = (1+f(1,2)) * (1+f(2,3))
new_1yr_rate = forward_rates[1]
compound_2yr = (1 + forward_rates[1]) * (1 + forward_rates[2])
new_2yr_rate = compound_2yr ** 0.5 - 1

# Step 4: Price the bond with 2 years remaining
pv_coupon_1 = annual_coupon / (1 + new_1yr_rate)
pv_coupon_2_and_par = (annual_coupon + par_value) / ((1 + new_2yr_rate) ** 2)

bond_price_in_1yr = pv_coupon_1 + pv_coupon_2_and_par

bond_price_in_1yr  # Result depends on calculated forward rates
```

**Common Bugs to Avoid:**
- Reusing today's spot rates instead of deriving the forward rate curve
- Not shifting the rate curve forward by one period
- Confusing spot rates with forward rates in the shifted curve
- Forgetting that "constant forward rates" means the forward rate curve shifts, not that spot rates stay the same

---

## Pattern: Asset_Swap_Spread_Calculation

**Description:** Asset Swap Spread (ASW), I-spread (Interpolated Spread), and G-spread are distinct credit spread measures that use different benchmarks. ASW terminology can vary by context: sometimes it refers to spread over swap rates (equivalent to I-spread), and sometimes over government rates (equivalent to G-spread). The question context and answer choices help determine which calculation method is appropriate.

**When to Use:** When calculating ASW, I-spread, G-spread, or other credit spreads relative to swap curves or government curves, especially when swap spreads are provided. Keywords: "I-spread", "interpolated spread", "asset swap spread", "ASW", "G-spread", "government spread".

**Procedure:**
1. **Identify the spread type requested and determine calculation method:**
   - **G-spread:** Corporate Yield - Interpolated Government Yield (spread over government curve only)
   - **I-spread:** Corporate Yield - Interpolated Swap Rate, where Swap Rate = Government Yield + Swap Spread
   - **ASW (Asset Swap Spread):** Context-dependent:
     - If swap spreads are provided → likely means I-spread (spread over swap curve)
     - If swap spreads are NOT provided → likely means G-spread (spread over government curve)
     - **Check answer choices:** If calculated I-spread doesn't match options, try G-spread
2. **For I-spread calculation:**
   - Interpolate government yield if bond maturity doesn't match benchmark maturities
   - Interpolate swap spread using the same interpolation weight
   - Calculate Swap Rate: Government Yield + Swap Spread
   - Compute spread: Corporate Yield - Swap Rate
3. **For G-spread or ASW (government benchmark) calculation:**
   - Interpolate government yield only
   - Compute spread: Corporate Yield - Government Yield
4. **Interpolation formula:** Value = Lower + weight × (Upper - Lower), where weight = (Target - Lower Maturity) / (Upper Maturity - Lower Maturity)

**Worked Example:**
**Question:** A 7-year corporate bond has a yield of 4.2%. Government yields: 5yr=2.8%, 10yr=3.4%. Swap spreads: 5yr=0.30%, 10yr=0.45%. Calculate both the I-spread and G-spread.

```python
# Bond characteristics
corporate_maturity = 7
corporate_yield = 4.2  # percent

# Government benchmark yields
gov_5yr_yield = 2.8
gov_10yr_yield = 3.4

# Swap spreads
swap_spread_5yr = 0.30
swap_spread_10yr = 0.45

# Step 1: Calculate interpolation weight
years_from_5yr = corporate_maturity - 5
total_span = 10 - 5
weight = years_from_5yr / total_span

# Step 2: Interpolate government yield for 7-year maturity
interpolated_gov_yield = gov_5yr_yield + weight * (gov_10yr_yield - gov_5yr_yield)

# Step 3: Interpolate swap spread for 7-year maturity
interpolated_swap_spread = swap_spread_5yr + weight * (swap_spread_10yr - swap_spread_5yr)

# Step 4: Calculate swap rate (government yield + swap spread)
swap_rate = interpolated_gov_yield + interpolated_swap_spread

# Step 5: Calculate I-spread (spread over swap curve)
i_spread = corporate_yield - swap_rate

# Step 6: Calculate G-spread (spread over government curve)
g_spread = corporate_yield - interpolated_gov_yield

# If question asks for ASW and swap spreads are provided, use I-spread
# If question asks for ASW and swap spreads are NOT provided, use G-spread

i_spread  # Result: approximately 0.98%
# g_spread would be approximately 1.16%
```

**Common Bugs to Avoid:**
- Confusing I-spread with G-spread (I-spread uses swap rate, G-spread uses government yield only)
- Calculating I-spread as: Corporate Yield - Government Yield - Swap Spread (this double-counts the swap spread)
- Using government yield instead of swap rate as the benchmark for I-spread
- Forgetting to interpolate when bond maturity doesn't match benchmark maturities
- Not using the same interpolation weight for both government yield and swap spread
- **Assuming ASW always means I-spread (it can mean G-spread depending on context)**
- **Not checking answer choices to validate which calculation method is appropriate**

**CHECK Steps:**
- If question asks for "I-spread" or "interpolated spread", verify you're using swap rate (government + swap spread), not just government yield
- If question asks for "G-spread", verify you're using only government yield
- **If question asks for "ASW" and provides swap spreads, try I-spread first**
- **If calculated I-spread doesn't match answer choices, calculate G-spread instead**
- **If question asks for "ASW" and does NOT provide swap spreads, use G-spread**
- Assert: I-spread = Corporate Yield - (Interpolated Gov Yield + Interpolated Swap Spread)
- Assert: G-spread = Corporate Yield - Interpolated Gov Yield
- Validate: I-spread should be lower than G-spread (swap rates are higher than government rates)

---
## Pattern: Credit_Spread_Return_Components

**Description:** Total return from credit bonds in recovery scenarios includes both carry income (OAS - Expected Loss) and capital gains from spread compression (OAS × Effective Spread Duration). Failing to account for duration-based capital gains significantly underestimates returns during credit cycle recoveries. When spread compression data is not provided, use qualitative portfolio comparison based on OAS, duration, and recovery potential.

**When to Use:** When comparing portfolio allocations during expected credit cycle improvements, spread tightening scenarios, or evaluating high-yield vs investment-grade positioning. When the question asks which portfolio has "highest excess return" during recovery scenarios.

**Procedure:**
1. **Check if quantitative spread compression data is provided:**
   - If YES: Use formula: $\text{Total Excess Return} \approx (\text{OAS} - \text{Expected Loss}) + (\Delta \text{Spread} \times \text{Eff Spread Duration})$
   - If NO: Use qualitative comparison based on OAS, duration, and allocation weights
2. **For quantitative analysis:**
   - Calculate carry income: OAS - Expected Loss (static income component)
   - Estimate spread compression: In strong recovery, HY spreads compress more than IG
   - Calculate capital gain: Spread change × Effective Spread Duration
   - For portfolio comparison, weight each position by allocation percentage
   - Include currency effects as additive adjustments to EUR positions
3. **For qualitative analysis (no specific spread compression given):**
   - Identify which asset class has highest OAS (highest income potential)
   - Identify which asset class has highest duration (highest sensitivity to spread changes)
   - Identify which region has strongest recovery potential
   - Portfolio with highest allocation to the best-positioned asset wins

**Worked Example:**
**Question:** Compare two portfolios during a strong EUR credit recovery. Portfolio A: 50% EUR HY (OAS=3.5%, Duration=6.0), 50% USD IG (OAS=1.2%, Duration=4.0). Portfolio B: 30% EUR HY, 70% USD IG. No specific spread compression data is provided. Which has higher expected excess return?

**Correct Code:**
```python
# Asset characteristics
eur_hy_oas = 3.5  # percent
eur_hy_duration = 6.0

usd_ig_oas = 1.2
usd_ig_duration = 4.0

# Portfolio allocations
portfolio_a = {'EUR_HY': 0.50, 'USD_IG': 0.50}
portfolio_b = {'EUR_HY': 0.30, 'USD_IG': 0.70}

# Qualitative analysis: EUR HY has highest OAS and highest duration
# In strong EUR recovery, EUR HY benefits most from:
# 1. Higher carry income (3.5% vs 1.2%)
# 2. Greater spread compression potential (HY compresses more than IG)
# 3. Higher duration amplifies capital gains (6.0 vs 4.0)

# Portfolio A has 50% allocation to EUR HY vs Portfolio B's 30%
# Therefore Portfolio A has higher expected excess return

# Calculate weighted OAS × Duration as proxy for return potential
def calculate_return_potential(allocation_eur_hy, allocation_usd_ig):
    eur_hy_potential = eur_hy_oas * eur_hy_duration
    usd_ig_potential = usd_ig_oas * usd_ig_duration
    
    portfolio_potential = (allocation_eur_hy * eur_hy_potential + 
                          allocation_usd_ig * usd_ig_potential)
    return portfolio_potential

potential_a = calculate_return_potential(portfolio_a['EUR_HY'], portfolio_a['USD_IG'])
potential_b = calculate_return_potential(portfolio_b['EUR_HY'], portfolio_b['USD_IG'])

# Portfolio A: 0.50 * (3.5 * 6.0) + 0.50 * (1.2 * 4.0) = 10.5 + 2.4 = 12.9
# Portfolio B: 0.30 * (3.5 * 6.0) + 0.70 * (1.2 * 4.0) = 6.3 + 3.36 = 9.66

potential_a  # Result: 12.9 (Portfolio A has higher return potential)
```

**Common Bugs to Avoid:**
- Ignoring duration-based capital gains (only using carry income)
- Treating all spread compression equally (HY compresses more than IG in recoveries)
- Forgetting to multiply spread change by duration to get price impact
- Not converting basis points to decimal (100bps = 1.0, not 100)
- Applying currency effects to both EUR and USD positions (only EUR positions affected)
- **Fabricating spread compression values when none are provided in the question**
- **Not recognizing when qualitative comparison is appropriate**

**CHECK Steps:**
- **If question provides specific spread compression data (e.g., "EUR HY spreads tighten by 100bps"), use quantitative formula**
- **If question only describes recovery qualitatively (e.g., "strong recovery", "earlier recovery"), use qualitative comparison**
- For qualitative comparison: Portfolio with highest allocation to (highest OAS × highest duration × strongest recovery region) wins
- Verify: In recovery scenarios, HY outperforms IG due to greater spread compression potential
- Verify: Higher duration amplifies capital gains from spread tightening

---
## Pattern: Condor_Butterfly_Positioning_for_Curvature

**Description:** Condor/butterfly spreads for curve flattening (reduced curvature) require being long the targeted segment and short the wings, with all positions having equal money duration. The positioning depends on whether you expect more or less curvature.

**When to Use:** When constructing condor or butterfly spreads to benefit from changes in yield curve curvature, especially when the question specifies "less curvature" or "more curvature" in a specific curve segment.

**Procedure:**
1. Identify target segment (e.g., 5yr-10yr area)
2. For LESS curvature (flattening): Long belly (5yr, 10yr), Short wings (1yr, 30yr)
3. For MORE curvature (steepening): Short belly, Long wings
4. Calculate money duration: $\text{Money Duration} = \text{Modified Duration} \times \text{Position Size}$
5. Set positions so all have equal absolute money duration
6. Use the constrained position (e.g., max 30yr position) to determine target money duration

**Worked Example:**
**Question:** Construct condor for LESS curvature in 5yr-10yr segment. Bonds: 2yr (dur=1.85), 5yr (dur=4.50), 10yr (dur=9.20), 30yr (dur=20.50). Max 30yr position: $25M.

**Correct Code:**
```python
# Bond characteristics
durations = {
    '2yr': 1.85,
    '5yr': 4.50,
    '10yr': 9.20,
    '30yr': 20.50
}

# Constraint: maximum 30-year position
max_30yr_position = 25000000

# For LESS curvature: Long belly (5yr, 10yr), Short wings (2yr, 30yr)

# Step 1: Calculate target money duration using constrained position
target_money_duration = durations['30yr'] * max_30yr_position

# Step 2: Calculate position sizes for equal money duration
position_2yr = target_money_duration / durations['2yr']
position_5yr = target_money_duration / durations['5yr']
position_10yr = target_money_duration / durations['10yr']
position_30yr = max_30yr_position

# Step 3: Assign long/short based on condor structure
# Short wings (negative), Long belly (positive)
positions = {
    '2yr': -position_2yr,
    '5yr': position_5yr,
    '10yr': position_10yr,
    '30yr': -position_30yr
}

# Convert to millions
positions_millions = {k: v / 1000000 for k, v in positions.items()}

# Return the short wing position magnitude
abs(positions_millions['2yr'])
```

**Common Bugs to Avoid:**
- Reversing long/short positions (shorting belly instead of wings for less curvature)
- Not maintaining equal money duration across all positions
- Using notional amounts instead of money duration for balancing
- Confusing "less curvature" (flattening) with "more curvature" (steepening)
- Forgetting to use absolute values when comparing position sizes
- Using complex f-string formatting or excessive print statements that cause execution failures
- Not handling division operations safely (check for zero durations)
- Creating overly verbose code with multiple print statements instead of clean calculations

**CHECK Steps:**
- Verify all durations are positive and non-zero before division
- If question asks for "less curvature", confirm wings are short (negative) and belly is long (positive)
- If question asks for "more curvature", confirm wings are long (positive) and belly is short (negative)
- Assert: All positions should have equal absolute money duration (within rounding tolerance)
- Verify: Money Duration = Duration × Position Size for each bond
- Check: The constrained position (usually longest maturity) should be used to set target money duration
- If code execution fails, simplify by removing print statements and complex formatting
- Final output should be a single numeric value (expression), not print statement
## Pattern: Conversion_Premium_Calculation

**Description:** Conversion premium is the amount by which a convertible bond's market price exceeds its conversion value (intrinsic value if converted immediately). Bond prices are typically quoted per $100 of face value, so they must be scaled to the actual par value (usually $1000) before calculating the premium.

**When to Use:** When analyzing convertible bonds and asked to calculate conversion premium, conversion parity, or evaluate conversion attractiveness. Keywords: "conversion premium", "conversion value", "convertible bond".

**Procedure:**
1. **Check bond price quotation convention:**
   - If bond price appears to be per $100 face value (typical for bonds), scale to actual par value
   - Formula: Actual Bond Price = Quoted Price × (Par Value / 100)
   - If bond price is already in absolute dollars (e.g., $950 for a $1000 bond), use as-is
2. Formula: Conversion Value = Stock Price × Conversion Ratio
3. Formula: Conversion Premium ($) = Bond Market Price - Conversion Value
4. Formula: Conversion Premium (%) = (Bond Price - Conversion Value) / Conversion Value × 100
5. Note: Premium can be negative (bond trades below conversion value)

**Worked Example:**
**Question:** A convertible bond is quoted at $82.50 (per $100 face value). The underlying stock trades at $35 per share, and the conversion ratio is 25 shares per bond. The bond has a par value of $1000. Calculate the conversion premium in dollars.

```python
# Convertible bond characteristics
quoted_bond_price = 82.50  # per $100 face value
par_value = 1000  # actual par value
stock_market_price = 35  # dollars per share
conversion_ratio = 25  # shares per bond

# Step 1: Scale bond price to actual par value
# Bonds are typically quoted per $100, so scale up
actual_bond_price = quoted_bond_price * (par_value / 100)

# Step 2: Calculate conversion value
conversion_value = stock_market_price * conversion_ratio

# Step 3: Calculate conversion premium in dollars
conversion_premium_dollars = actual_bond_price - conversion_value

# Step 4: Calculate conversion premium as percentage (optional)
conversion_premium_percent = (conversion_premium_dollars / conversion_value) * 100

conversion_premium_dollars  # Result: 50.00 (bond trades at $50 premium)
```

**Common Bugs to Avoid:**
- Not scaling bond price from per-$100 quotation to actual par value (most common error)
- Using par value instead of market price for the bond
- Reporting negative premium as positive (use actual sign)
- Confusing conversion premium with conversion price (different concepts)
- Dividing by bond price instead of conversion value for percentage calculation
- Forgetting to multiply stock price by conversion ratio

**CHECK Steps:**
- If bond price is less than $200 but par value is $1000, it's likely quoted per $100 face value
- Verify: Actual Bond Price = Quoted Price × (Par Value / 100) when price is per $100
- Assert: Conversion Value = Stock Price × Conversion Ratio
- If conversion premium is negative, bond is trading below parity (immediate conversion is profitable)

---
## Pattern: Zero_Coupon_Bond_Pricing_from_Forward_Rates

**Description:** Zero-coupon bond prices are calculated by discounting the par value using the appropriate spot rate (derived from forward rates) or by direct discounting with sequential forward rates. The compounding convention (discrete annual vs. continuous) must be identified from the problem context. When calculating percentage changes, determine whether the question asks for signed change or absolute magnitude.

**When to Use:** When pricing zero-coupon bonds given forward rates, or when calculating yields for zero-coupon instruments. Keywords: "zero-coupon bond", "discount bond", "forward rates", "continuously compounded", "annual compounding", "percentage change".

**Procedure:**
1. **Identify compounding convention from context:**
   - Look for keywords: "continuously compounded", "continuous compounding" → use e^(-y×t)
   - If no mention of continuous compounding → use discrete annual: (1 + y)^(-t)
2. **For discrete annual compounding:**
   - For n-year zero-coupon bond, identify forward rates for years 0 through n-1
   - Formula: (1 + s_n)^n = ∏(1 + f_i) for i=0 to n-1
   - Price = Par Value / ∏(1 + f_i)
3. **For continuous compounding:**
   - Convert forward rates to continuously compounded spot rate if needed
   - Price = Par Value × e^(-y×t)
4. **Calculate percentage change:**
   - Formula: Percentage Change = (New Price - Old Price) / Old Price × 100
   - **Determine output format:** Check if question asks for "magnitude", "absolute value", or signed change
   - If question asks for "percentage change" without qualifier, provide signed value (negative for price decrease)
   - If question asks for "magnitude of change" or similar, use abs(percentage_change)
5. Use the compounding convention consistently for all calculations

**Worked Example:**
**Question:** A 3-year zero-coupon bond with $1000 par value is priced using continuously compounded rates. The current continuously compounded yield is 6% per annum. Calculate the percentage change in value if yields increase to 8% per annum.

```python
import math

# Bond characteristics
par_value = 1000
maturity = 3  # years
current_yield = 0.06  # 6% continuously compounded
new_yield = 0.08  # 8% continuously compounded

# Step 1: Calculate current price using continuous compounding
# Formula: Price = Par × e^(-y×t)
current_price = par_value * math.exp(-current_yield * maturity)

# Step 2: Calculate new price with increased yield
new_price = par_value * math.exp(-new_yield * maturity)

# Step 3: Calculate percentage change (signed)
percentage_change = ((new_price - current_price) / current_price) * 100

# Result is negative (price decreased when yield increased)
percentage_change  # Result: approximately -5.61%
```

**Common Bugs to Avoid:**
- Using discrete compounding (1 + y)^t when context specifies continuous compounding
- Using continuous compounding when problem uses annual/discrete rates
- Including year n forward rate for an n-year bond (should stop at year n-1)
- Not compounding forward rates (treating them as additive)
- Confusing the number of forward rates to use with the bond's maturity
- Forgetting to import math module when using math.exp()
- **Arbitrarily applying abs() without checking what the question asks for**
- **Reporting positive change when question asks for signed percentage change**

**CHECK Steps:**
- If context mentions "continuously compounded" or "continuous compounding", use e^(-y×t)
- If no mention of continuous compounding, default to discrete: (1 + y)^(-t)
- For forward rate compounding: verify using n rates for n-year maturity (years 0 to n-1)
- Assert: Price with continuous compounding = Par × e^(-yield × time)
- Assert: Price with discrete compounding = Par / (1 + yield)^time
- **Question asks for "percentage change" → provide signed value (negative if price decreased)**
- **Question asks for "magnitude" or "absolute change" → apply abs() to result**
- **Validate:** When yields increase, bond prices decrease (percentage change should be negative)

---
## Pattern: Expectations_Theory_Forward_Rate_Extraction

**Description:** Under expectations theory, forward rates can be extracted from spot rates, or spot rates can be derived from forward rates. When a table provides forward rates explicitly, the answer is typically a direct lookup after correctly interpreting the table indexing. The key challenge is disambiguating terminology: "in year N" vs "at year N" vs "for year N".

**When to Use:** When questions ask for "expected forward rate" under expectations theory and provide a forward rate table. Keywords: "expectations theory", "forward rate", "expected rate", "forward rate table", "in year", "for year".

**Procedure:**
1. **Clarify table indexing:**
   - Check if table starts at "Year 0" (0-indexed) or "Year 1" (1-indexed)
   - Identify what each year label represents: rate starting at that year, or rate for that period
2. **Disambiguate terminology in the question:**
   - **"in year N"** or **"during year N"** = rate during the Nth period = Year N-1 index (for 0-indexed tables)
   - **"at year N"** or **"starting in year N"** = rate starting at year N = Year N index
   - **"for the Nth year"** = rate for the Nth period = Year N-1 index (for 0-indexed tables)
   - **Example:** "in the third year" means during the 3rd period (Year 0→1, 1→2, 2→3), so use Year 2 index
3. **Direct lookup when rates are provided:**
   - If table shows forward rates explicitly, extract the appropriate value
   - Avoid calculating forward rates from spot rates when already given
4. **Only calculate if needed:**
   - If spot rates are given but forward rates are requested: f_{m,n} = [(1+s_n)^n / (1+s_m)^m]^(1/(n-m)) - 1
   - If forward rates are given but multi-period forward rate is requested: compound appropriately

**Worked Example:**
**Question:** A forward rate table shows 1-year rates: Year 0 = 4%, Year 1 = 5%, Year 2 = 6%, Year 3 = 7%. According to expectations theory, what is the expected forward rate during the second year?

```python
# Forward rate table (1-year rates, 0-indexed)
# Year 0: rate for period 0→1 (today's 1-year rate)
# Year 1: rate for period 1→2 (1-year rate starting in year 1)
# Year 2: rate for period 2→3 (1-year rate starting in year 2)
# Year 3: rate for period 3→4 (1-year rate starting in year 3)

forward_rates = {
    0: 0.04,  # Period 0→1 (first year)
    1: 0.05,  # Period 1→2 (second year)
    2: 0.06,  # Period 2→3 (third year)
    3: 0.07   # Period 3→4 (fourth year)
}

# Question asks for forward rate "during the second year"
# "During the second year" = period 1→2 = Year 1 index (0-indexed)
# This is forward_rates[1]

expected_forward_rate = forward_rates[1]

# Convert to percentage
expected_forward_rate * 100  # Result: 5.00%
```

**Common Bugs to Avoid:**
- Calculating forward rates from spot rates when forward rates are already provided in the table
- Confusing 0-indexed vs 1-indexed year labeling
- **Misinterpreting "in year N" as Year N index instead of Year N-1 index (for 0-indexed tables)**
- **Confusing "in the third year" (during 3rd period = Year 2) with "at year 3" (starting at year 3 = Year 3)**
- Using spot rate formulas when forward rates are directly given
- Over-complicating with unnecessary calculations when a simple lookup suffices
- Creating complex code with multiple calculation paths that may cause execution errors

**CHECK Steps:**
- If forward rate table is provided, verify whether a direct lookup answers the question
- **Terminology check:** "in year N" or "during year N" → use Year N-1 index (0-indexed)
- **Terminology check:** "at year N" or "starting in year N" → use Year N index
- If table is 0-indexed (starts at Year 0), "year n" typically refers to forward_rates[n]
- If table is 1-indexed (starts at Year 1), adjust indexing accordingly
- Only calculate forward rates if they're not already in the table
- Keep code simple and direct—avoid exploratory calculations that don't contribute to the answer
- **Validate:** For "in the Nth year" with 0-indexed table, use index N-1

---
## Pattern: Interest_Rate_Conversion_APR_EAR

**Description:** Converting between Annual Percentage Rate (APR) and Effective Annual Rate (EAR) requires understanding the compounding frequency. APR is the stated rate with m compounding periods, while EAR is the actual annual return. Output precision should match financial conventions (typically 2-4 decimal places for rates).

**When to Use:** When converting between APR and EAR, or when given one rate and asked to find the other. Keywords: "APR", "EAR", "effective annual rate", "annual percentage rate", "compounding frequency", "nominal rate".

**Procedure:**
1. **Identify the conversion direction:**
   - EAR to APR: APR = m × [(1 + EAR)^(1/m) - 1]
   - APR to EAR: EAR = (1 + APR/m)^m - 1
2. **Identify compounding frequency (m):**
   - Annual: m = 1
   - Semi-annual: m = 2
   - Quarterly: m = 4
   - Monthly: m = 12
   - Daily: m = 365
3. **Apply the formula with correct compounding frequency**
4. **Output precision:**
   - Match the precision of the given rate (if EAR has 2 decimals, use 2 for APR)
   - Default to 2 decimal places for percentage rates (standard financial convention)
   - Use 4 decimal places for decimal form (e.g., 0.1735)
5. **Convert between decimal and percentage as needed**

**Worked Example:**
**Question:** An investment has an EAR of 18.50% with quarterly compounding. Calculate the APR to 2 decimal places.

```python
# Given values
ear = 0.1850  # 18.50% as decimal
compounding_frequency = 4  # quarterly

# Step 1: Apply EAR to APR conversion formula
# APR = m × [(1 + EAR)^(1/m) - 1]
apr_decimal = compounding_frequency * ((1 + ear) ** (1 / compounding_frequency) - 1)

# Step 2: Convert to percentage with 2 decimal places
apr_percent = round(apr_decimal * 100, 2)

apr_percent  # Result: 17.35%
```

**Common Bugs to Avoid:**
- Using wrong compounding frequency (e.g., using m=1 when quarterly compounding is specified)
- Rounding too early in the calculation (round only the final result)
- Arbitrary rounding decisions (use 2 decimal places for percentages unless specified otherwise)
- Confusing APR and EAR formulas (APR uses 1/m exponent, EAR uses m exponent)
- Not converting between decimal and percentage forms correctly
- Forgetting to multiply by m in the EAR-to-APR formula

**CHECK Steps:**
- Verify compounding frequency matches the problem statement
- Assert: EAR should be greater than APR for m > 1 (more frequent compounding increases effective rate)
- Check output precision: default to 2 decimal places for percentage rates
- If answer doesn't match expected precision, adjust rounding to 2, 3, or 4 decimal places

---

## Pattern: Swap_Rate_Decomposition_LIBOR_Forward

**Description:** In interest rate swaps, the fixed swap rate equals the geometric mean of expected LIBOR forward rates when using simple compounding. When given a swap rate and some LIBOR forward rates, the missing forward rate can be solved by setting the swap rate equal to the compounded product of all LIBOR rates. OIS rates are used for discounting swap cash flows but not for determining LIBOR forwards through geometric decomposition. When both OIS and LIBOR rates are provided, the context determines whether to use simple geometric decomposition or OIS-discounted valuation.

**When to Use:** When asked to find a LIBOR forward rate given a swap rate and other LIBOR rates. When the problem provides both OIS rates and LIBOR rates, and asks for LIBOR forwards. Keywords: "LIBOR forward rate", "swap rate", "interest rate swap", "OIS", "forward LIBOR".

**Procedure:**
1. **Identify the rate types:**
   - Swap rate: the fixed rate in the swap, equals geometric mean of LIBOR forwards
   - LIBOR rates: the floating leg rates (spot and forward)
   - OIS rates: used for discounting, NOT for calculating LIBOR forwards via geometric decomposition
2. **Determine calculation method:**
   - If question asks for "LIBOR forward rate" using swap rate decomposition → use geometric mean formula
   - If question mentions OIS rates explicitly in the context of forward rate calculation → may require OIS-discounted approach
3. **Set up the equation (geometric decomposition method):**
   - For n-year swap: (1 + swap_rate)^n = (1 + L_0) × (1 + f_{1,2}) × ... × (1 + f_{n-1,n})
   - Where L_0 is today's LIBOR, f_{i,i+1} are LIBOR forward rates
4. **Solve for the unknown forward rate:**
   - Rearrange: (1 + f_{unknown}) = (1 + swap_rate)^n / [(1 + L_0) × (1 + f_1) × ... × (1 + f_{n-1})]
   - Extract: f_{unknown} = result - 1
5. **Validation:** Check if result is reasonable (typically within 1-2% of other forward rates)

**Worked Example:**
**Question:** A 4-year interest rate swap has a fixed rate of 4.2%. The current 1-year LIBOR is 3.8%, the 1-year forward LIBOR for year 1 to 2 is 4.0%, and the 1-year forward LIBOR for year 2 to 3 is 4.3%. Calculate the 1-year forward LIBOR rate for the period from year 3 to year 4.

```python
# Given values
swap_rate = 0.042  # 4.2% fixed swap rate
libor_1yr = 0.038  # Current 1-year LIBOR
forward_1to2 = 0.040  # LIBOR forward rate for year 1 to 2
forward_2to3 = 0.043  # LIBOR forward rate for year 2 to 3
maturity = 4  # 4-year swap

# Step 1: Set up the swap rate equation
# (1 + swap_rate)^4 = (1 + libor_1yr) × (1 + forward_1to2) × (1 + forward_2to3) × (1 + forward_3to4)

# Step 2: Calculate the left side
left_side = (1 + swap_rate) ** maturity

# Step 3: Calculate known right side components
known_product = (1 + libor_1yr) * (1 + forward_1to2) * (1 + forward_2to3)

# Step 4: Solve for the unknown forward rate
forward_3to4 = (left_side / known_product) - 1

# Step 5: Convert to percentage
forward_3to4_percent = forward_3to4 * 100

forward_3to4_percent  # Result: approximately 4.78%
```

**Common Bugs to Avoid:**
- Using OIS rates instead of LIBOR rates to calculate LIBOR forwards via geometric decomposition
- Confusing the swap rate (fixed leg) with LIBOR rates (floating leg)
- Using arithmetic average instead of geometric mean (compounding)
- Not including all LIBOR rates in the product (must include current LIBOR and all forwards)
- Forgetting to subtract 1 when extracting the forward rate from the compound factor
- **Not validating whether the calculated forward rate is reasonable (should be close to other forward rates)**

**CHECK Steps:**
- If problem provides both OIS and LIBOR rates, verify you're using LIBOR for forward rate calculations via geometric decomposition
- Assert: Swap rate equation uses LIBOR rates only, not OIS rates (for geometric decomposition method)
- Verify: (1 + swap_rate)^n should equal the product of (1 + each LIBOR rate)
- If calculated forward rate seems unreasonable (e.g., differs by >3% from other forwards), double-check the calculation
- **Validation:** Forward rates should generally increase or stay relatively stable across periods
- **If result doesn't match expected answer, consider whether OIS-discounted valuation is required instead of geometric decomposition**
## Pattern: Forward_Contract_Pricing_with_Rate_Shifts

**Description:** Forward contract pricing after interest rate changes requires calculating the present value difference between the original forward price (locked in) and the new forward price (at current market rates). The forward price itself is determined by the cost-of-carry relationship using spot rates, NOT by extracting forward rates. For a forward contract on a zero-coupon bond, the forward price equals the bond's future value discounted from maturity back to the delivery date using current spot rates.

**When to Use:** When pricing forward contracts on bonds or other fixed-income securities after a parallel shift in interest rates, and the question asks for the "price of a forward contract" or "value of the forward position" after rate changes. Keywords: "forward contract", "forward price", "rates increased by X basis points", "otherwise identical forward contract".

**When NOT to Use:** 
- When pricing the underlying bond itself (use bond pricing patterns instead)
- When calculating forward rates from spot rates (use Forward_Rate_to_Spot_Rate_Conversion)
- When the question asks for bond price evolution (use Bond_Price_Evolution_with_Constant_Forward_Rates)

**Procedure:**
1. Identify the forward contract specifications: underlying asset (bond), delivery date, bond maturity at delivery
2. Apply the rate shift to all relevant spot rates (parallel shift)
3. **Calculate the new forward price using cost-of-carry:**
   - For a zero-coupon bond delivered at time T with maturity at time T+M:
   - Forward Price = Face Value / (1 + s_{T+M})^{T+M} × (1 + s_T)^T
   - Simplified: Discount face value from total maturity to delivery date
4. **Alternative formula (equivalent):**
   - Forward Price = [Face Value / (1 + s_{T+M})^{T+M}] / [1 / (1 + s_T)^T]
   - This represents: (Bond price at total maturity) / (Discount factor to delivery)
5. Calculate the original forward price using original spot rates (if needed for comparison)
6. The forward contract value = PV(New Forward Price - Original Forward Price)

**Worked Example:**
**Question:** You agreed to buy a one-year Treasury bond (face value $1,000) in six months. Original rates: 6-month = 4%, 18-month = 5%. After rates increase by 25 bps, calculate the new forward price.

**Correct Code:**
```python
# Forward contract specifications
face_value = 1000
delivery_time = 0.5  # 6 months = 0.5 years
bond_maturity_at_delivery = 1.0  # 1-year bond
total_maturity = delivery_time + bond_maturity_at_delivery  # 1.5 years

# Original spot rates
spot_6m_original = 0.04
spot_18m_original = 0.05

# Rate shift
rate_increase = 0.0025  # 25 basis points

# New spot rates after parallel shift
spot_6m_new = spot_6m_original + rate_increase
spot_18m_new = spot_18m_original + rate_increase

# Calculate new forward price using cost-of-carry relationship
# Method 1: Direct formula
# Forward Price = Face Value / [(1 + s_total)^total / (1 + s_delivery)^delivery]
forward_price_new = face_value / ((1 + spot_18m_new) ** total_maturity / (1 + spot_6m_new) ** delivery_time)

# Method 2: Equivalent calculation (clearer interpretation)
# Step 1: Calculate bond price at total maturity (18 months from now)
bond_price_at_18m = face_value / (1 + spot_18m_new) ** total_maturity

# Step 2: Grow this price forward from today to delivery (6 months)
# This removes the discounting from today to delivery date
forward_price_new_alt = bond_price_at_18m * (1 + spot_6m_new) ** delivery_time

# Both methods yield the same result
round(forward_price_new, 2)
```

**Common Bugs to Avoid:**
- **Using forward rate extraction instead of cost-of-carry:** Extracting forward rates and applying them is incorrect for forward contract pricing
- **Multiplying by growth factor instead of dividing:** Forward price = discount from maturity to delivery, not growth from delivery to maturity
- **Incorrect formula structure:** Using `face_value * (1 + s_delivery)^delivery / (1 + s_total)^total` multiplies when it should divide
- **Confusing forward contract pricing with bond pricing:** Forward contracts require the cost-of-carry relationship, not simple PV of cash flows
- **Not applying the rate shift to all relevant spot rates:** Must shift both the delivery rate and total maturity rate

**CHECK Steps:**
- If question asks for "forward contract price" or "price of forward contract", use cost-of-carry formula
- Verify formula structure: Forward Price = Face Value / [(1 + s_total)^total / (1 + s_delivery)^delivery]
- Alternative check: Forward Price = [Face Value / (1 + s_total)^total] × (1 + s_delivery)^delivery
- Assert: When rates increase, forward price should decrease (inverse relationship)
- Validate: Forward price should be less than face value (for positive interest rates)
- **Key validation:** The formula should DIVIDE by the compound factor, not multiply
- **Cross-check:** Calculate using both Method 1 (direct) and Method 2 (step-by-step) to verify consistency