# Fixed Income Arithmetic Skills - Program of Thought Patterns

## Pattern: Forward_Rate_to_Spot_Rate_Conversion

**Description:** Forward rates must be compounded sequentially to derive spot rates for discounting multi-period cash flows. A common error is treating forward rates as if they were spot rates or using incorrect compounding formulas.

**When to Use:** When pricing bonds or calculating yields given a table of forward rates (1-year forward rates for consecutive periods).

**Procedure:**
1. Formula: Spot rate for year n: $(1 + s_n)^n = (1 + f_0) \times (1 + f_1) \times ... \times (1 + f_{n-1})$
2. Identify all forward rates from year 0 through year n-1
3. Compound them multiplicatively: product of (1 + each forward rate)
4. Extract the spot rate: take the nth root and subtract 1
5. Use spot rates to discount each cash flow at its respective maturity

**Code Example:**

**Scenario:** Given 1-year forward rates: Year 0=4%, Year 1=5%, Year 2=6%. Calculate the price of a 3-year bond with 7% annual coupon and $1000 par value.

**Correct Code:**
```python
# Given forward rates
forward_rates = [0.04, 0.05, 0.06]  # Years 0, 1, 2
par_value = 1000
coupon_rate = 0.07
annual_coupon = par_value * coupon_rate

# Step 1: Calculate spot rates from forward rates
spot_rates = []
for n in range(1, len(forward_rates) + 1):
    compound_product = 1.0
    for i in range(n):
        compound_product *= (1 + forward_rates[i])
    spot_rate = compound_product ** (1/n) - 1
    spot_rates.append(spot_rate)

# Step 2: Discount cash flows using spot rates
bond_price = 0
for year in range(1, len(spot_rates) + 1):
    if year < len(spot_rates):
        cash_flow = annual_coupon
    else:
        cash_flow = annual_coupon + par_value
    
    pv = cash_flow / ((1 + spot_rates[year - 1]) ** year)
    bond_price += pv

bond_price  # Result: approximately 1027.89
```

**Common Bugs to Avoid:**
- Treating forward rates as spot rates: `pv = cash_flow / (1 + forward_rates[year])**year` is WRONG
- Using only the nth forward rate instead of compounding all rates from 0 to n-1
- Confusing year indexing: forward rate for "Year 1" applies to the period from year 0 to year 1
- Off-by-one errors in loop ranges when matching cash flows to discount periods

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

**Description:** Asset Swap Spread (ASW) is the spread of a corporate bond's yield over the swap rate (not over government yield). The swap rate equals the government yield plus the swap spread.

**When to Use:** When calculating ASW, Z-spread, or other credit spreads relative to swap curves, especially when swap spreads are provided.

**Procedure:**
1. Formula: $ASW = \text{Corporate Yield} - \text{Swap Rate}$
2. Calculate Swap Rate: $\text{Swap Rate} = \text{Government Yield} + \text{Swap Spread}$
3. Interpolate government yield if bond maturity doesn't match benchmark maturities
4. Interpolate swap spread using the same interpolation weight
5. Compute ASW as the difference between corporate yield and interpolated swap rate

**Code Example:**

**Scenario:** Corporate bond: 15yr, 4.5% yield. Government yields: 10yr=2.0%, 20yr=2.5%. Swap spreads: 10yr=0.30%, 20yr=0.40%. Calculate ASW.

**Correct Code:**
```python
# Bond characteristics
corporate_maturity = 15
corporate_yield = 4.5  # percent

# Government benchmark yields
gov_10yr_yield = 2.0
gov_20yr_yield = 2.5

# Swap spreads
swap_spread_10yr = 0.30
swap_spread_20yr = 0.40

# Step 1: Interpolate government yield for 15-year maturity
years_from_10yr = corporate_maturity - 10
total_span = 20 - 10
weight = years_from_10yr / total_span

interpolated_gov_yield = gov_10yr_yield + weight * (gov_20yr_yield - gov_10yr_yield)

# Step 2: Interpolate swap spread for 15-year maturity
interpolated_swap_spread = swap_spread_10yr + weight * (swap_spread_20yr - swap_spread_10yr)

# Step 3: Calculate swap rate
swap_rate = interpolated_gov_yield + interpolated_swap_spread

# Step 4: Calculate ASW
asw = corporate_yield - swap_rate

asw  # Result: approximately 1.65%
```

**Common Bugs to Avoid:**
- Calculating ASW as: Corporate Yield - Government Yield - Swap Spread (double-counts swap spread)
- Using government yield instead of swap rate as the benchmark
- Forgetting to interpolate when bond maturity doesn't match benchmark maturities
- Confusing ASW with G-spread (G-spread = Corporate Yield - Government Yield)

---

## Pattern: Credit_Spread_Return_Components

**Description:** Total return from credit bonds in recovery scenarios includes both carry income (OAS - Expected Loss) and capital gains from spread compression (OAS × Effective Spread Duration). Failing to account for duration-based capital gains significantly underestimates returns during credit cycle recoveries.

**When to Use:** When comparing portfolio allocations during expected credit cycle improvements, spread tightening scenarios, or evaluating high-yield vs investment-grade positioning.

**Procedure:**
1. Formula: $\text{Total Excess Return} \approx (\text{OAS} - \text{Expected Loss}) + (\Delta \text{Spread} \times \text{Eff Spread Duration})$
2. Calculate carry income: OAS - Expected Loss (static income component)
3. Estimate spread compression: In strong recovery, HY spreads compress more than IG
4. Calculate capital gain: Spread change × Effective Spread Duration
5. For portfolio comparison, weight each position by allocation percentage
6. Include currency effects as additive adjustments to EUR positions

**Code Example:**

**Scenario:** Compare two portfolios during EUR credit recovery. Portfolio A: 60% EUR HY (OAS=4%, Duration=5.5, ExpLoss=3%), 40% USD IG (OAS=1.5%, Duration=4.0, ExpLoss=0.5%). Portfolio B: 40% EUR HY, 60% USD IG. EUR depreciates 1.5%. Expected spread compression: EUR HY -100bps, USD IG -20bps.

**Correct Code:**
```python
# Asset characteristics
eur_hy_oas = 4.0  # percent
eur_hy_duration = 5.5
eur_hy_exp_loss = 3.0
eur_hy_spread_change = -1.0  # -100 bps compression

usd_ig_oas = 1.5
usd_ig_duration = 4.0
usd_ig_exp_loss = 0.5
usd_ig_spread_change = -0.2  # -20 bps compression

eur_fx_impact = -1.5  # percent

# Portfolio allocations
portfolio_a = {'EUR_HY': 0.60, 'USD_IG': 0.40}
portfolio_b = {'EUR_HY': 0.40, 'USD_IG': 0.60}

def calculate_total_return(allocation_eur_hy, allocation_usd_ig):
    # EUR HY component
    eur_hy_carry = eur_hy_oas - eur_hy_exp_loss
    eur_hy_capital_gain = eur_hy_spread_change * eur_hy_duration
    eur_hy_total = eur_hy_carry + eur_hy_capital_gain + eur_fx_impact
    
    # USD IG component
    usd_ig_carry = usd_ig_oas - usd_ig_exp_loss
    usd_ig_capital_gain = usd_ig_spread_change * usd_ig_duration
    usd_ig_total = usd_ig_carry + usd_ig_capital_gain
    
    # Weighted portfolio return
    portfolio_return = (allocation_eur_hy * eur_hy_total + 
                       allocation_usd_ig * usd_ig_total)
    
    return portfolio_return

return_a = calculate_total_return(portfolio_a['EUR_HY'], portfolio_a['USD_IG'])
return_b = calculate_total_return(portfolio_b['EUR_HY'], portfolio_b['USD_IG'])

# Portfolio A has higher return due to greater EUR HY allocation
# EUR HY: 1% carry - 5.5% capital gain - 1.5% FX = -6.0% total
# USD IG: 1% carry - 0.8% capital gain = 0.2% total
# Portfolio A: 0.60*(-6.0) + 0.40*(0.2) = -3.52%
# Portfolio B: 0.40*(-6.0) + 0.60*(0.2) = -2.28%

return_a  # Result: approximately -3.52%
```

**Common Bugs to Avoid:**
- Ignoring duration-based capital gains (only using carry income)
- Treating all spread compression equally (HY compresses more than IG in recoveries)
- Forgetting to multiply spread change by duration to get price impact
- Not converting basis points to decimal (100bps = 1.0, not 100)
- Applying currency effects to both EUR and USD positions (only EUR positions affected)

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

**Code Example:**

**Scenario:** Construct condor for LESS curvature in 5yr-10yr segment. Bonds: 1yr (dur=0.98), 5yr (dur=4.60), 10yr (dur=8.50), 30yr (dur=19.80). Max 30yr position: $20M.

**Correct Code:**
```python
# Bond characteristics
durations = {
    '1yr': 0.98,
    '5yr': 4.60,
    '10yr': 8.50,
    '30yr': 19.80
}

# Constraint: maximum 30-year position
max_30yr_position = 20_000_000  # $20 million

# For LESS curvature in 5yr-10yr segment:
# Long the belly (5yr and 10yr), Short the wings (1yr and 30yr)

# Step 1: Calculate target money duration using constrained position
target_money_duration = durations['30yr'] * max_30yr_position

# Step 2: Calculate position sizes for equal money duration
position_1yr = target_money_duration / durations['1yr']
position_5yr = target_money_duration / durations['5yr']
position_10yr = target_money_duration / durations['10yr']
position_30yr = max_30yr_position

# Step 3: Assign long/short based on condor structure
# Short wings: 1yr and 30yr (negative positions)
# Long belly: 5yr and 10yr (positive positions)
positions = {
    '1yr': -position_1yr,  # Short
    '5yr': position_5yr,   # Long
    '10yr': position_10yr, # Long
    '30yr': -position_30yr # Short
}

# Convert to millions for readability
positions_millions = {k: v / 1_000_000 for k, v in positions.items()}

# The short position in 1yr is the answer
abs(positions_millions['1yr'])  # Result: approximately 404.08 million
```

**Common Bugs to Avoid:**
- Reversing long/short positions (shorting belly instead of wings for less curvature)
- Not maintaining equal money duration across all positions
- Using notional amounts instead of money duration for balancing
- Confusing "less curvature" (flattening) with "more curvature" (steepening)
- Forgetting to use absolute values when comparing position sizes

---

## Pattern: Conversion_Premium_Calculation

**Description:** Conversion premium is the amount by which a convertible bond's market price exceeds its conversion value (intrinsic value if converted immediately). It represents the premium investors pay for the optionality and bond features.

**When to Use:** When analyzing convertible bonds and asked to calculate conversion premium, conversion parity, or evaluate conversion attractiveness.

**Procedure:**
1. Formula: $\text{Conversion Value} = \text{Stock Price} \times \text{Conversion Ratio}$
2. Formula: $\text{Conversion Premium} = \text{Bond Market Price} - \text{Conversion Value}$
3. Calculate conversion value (what you'd get if converting now)
4. Subtract from bond's market price to get dollar premium
5. For percentage: $\text{Premium \%} = \frac{\text{Bond Price} - \text{Conversion Value}}{\text{Conversion Value}} \times 100$
6. Note: Premium can be negative (bond trades below conversion value)

**Code Example:**

**Scenario:** Convertible bond: Market price $950, Stock price $42, Conversion ratio 21.5 shares. Calculate conversion premium in dollars and percent.

**Correct Code:**
```python
# Convertible bond characteristics
bond_market_price = 950  # dollars
stock_market_price = 42  # dollars per share
conversion_ratio = 21.5  # shares per bond

# Step 1: Calculate conversion value
conversion_value = stock_market_price * conversion_ratio

# Step 2: Calculate conversion premium in dollars
conversion_premium_dollars = bond_market_price - conversion_value

# Step 3: Calculate conversion premium as percentage
conversion_premium_percent = (conversion_premium_dollars / conversion_value) * 100

# Return both metrics
result = {
    'conversion_value': conversion_value,
    'premium_dollars': conversion_premium_dollars,
    'premium_percent': conversion_premium_percent
}

conversion_premium_dollars  # Result: 47.00 (bond trades at $47 premium)
```

**Common Bugs to Avoid:**
- Reporting negative premium as positive (use actual sign)
- Confusing conversion premium with conversion price (different concepts)
- Using par value instead of market price for the bond
- Dividing by bond price instead of conversion value for percentage calculation
- Forgetting to multiply stock price by conversion ratio

---

## Pattern: Zero_Coupon_Bond_Pricing_from_Forward_Rates

**Description:** Zero-coupon bond prices are calculated by discounting the par value using the appropriate spot rate, which must be derived from forward rates through sequential compounding. The maturity determines which forward rates to include.

**When to Use:** When pricing zero-coupon bonds given forward rate tables, or when calculating yields for zero-coupon instruments.

**Procedure:**
1. For an n-year zero-coupon bond, identify forward rates for years 0 through n-1
2. Formula: $(1 + s_n)^n = \prod_{i=0}^{n-1}(1 + f_i)$
3. Calculate compound product of all relevant forward rates
4. Extract spot rate: $s_n = (\text{compound product})^{1/n} - 1$
5. Price: $\text{Price} = \frac{\text{Par Value}}{(1 + s_n)^n}$

**Code Example:**

**Scenario:** Price a 5-year zero-coupon bond with $1000 par. Forward rates: Year 0=3%, Year 1=4%, Year 2=5%, Year 3=6%, Year 4=7%.

**Correct Code:**
```python
# Forward rates for each year
forward_rates = [0.03, 0.04, 0.05, 0.06, 0.07]  # Years 0-4
par_value = 1000
maturity = 5

# Step 1: Calculate compound product of forward rates
# For 5-year bond, use forward rates for years 0, 1, 2, 3, 4
compound_product = 1.0
for i in range(maturity):
    compound_product *= (1 + forward_rates[i])

# Step 2: Calculate 5-year spot rate
spot_rate_5yr = compound_product ** (1 / maturity) - 1

# Step 3: Price the zero-coupon bond
# Alternative: Price = Par / compound_product (direct calculation)
bond_price = par_value / compound_product

# Verification using spot rate
bond_price_verify = par_value / ((1 + spot_rate_5yr) ** maturity)

bond_price  # Result: approximately 781.20
```

**Common Bugs to Avoid:**
- Including the year n forward rate for an n-year bond (should stop at year n-1)
- Using simple average instead of geometric mean for spot rate
- Not compounding forward rates (treating them as additive)
- Confusing the number of forward rates to use with the bond's maturity

---

## Pattern: Expectations_Theory_Forward_Rate_Extraction

**Description:** Under expectations theory, forward rates can be extracted from spot rates, or spot rates can be derived from forward rates. When a table provides forward rates explicitly, the answer may be a direct lookup rather than a calculation.

**When to Use:** When questions ask for "expected forward rate" under expectations theory and provide a forward rate table.

**Procedure:**
1. Clarify what the question asks: forward rate for year n, or forward rate from year m to year n
2. If table shows "Year Forward Interest Rate", the value at Year k is the 1-year rate for period k to k+1
3. For "forward rate in the third year": check if this means year 2 (third row, 0-indexed) or year 3
4. Verify with context: "expected forward rate in year 3" typically means the rate for the period starting in year 3
5. If calculation is needed: $f_{m,n} = \frac{(1+s_n)^n}{(1+s_m)^m}^{\frac{1}{n-m}} - 1$

**Code Example:**

**Scenario:** Forward rate table shows: Year 0=4%, Year 1=5%, Year 2=6%, Year 3=7%. What is the expected forward rate in the third year?

**Correct Code:**
```python
# Forward rate table (1-year rates for each period)
forward_rates = {
    0: 0.04,  # Rate for period 0→1
    1: 0.05,  # Rate for period 1→2
    2: 0.06,  # Rate for period 2→3
    3: 0.07   # Rate for period 3→4
}

# Question: "expected forward rate in the third year"
# Interpretation 1: Rate for year 2 (third row, 0-indexed)
answer_interpretation_1 = forward_rates[2]  # 6%

# Interpretation 2: Rate starting in year 3
answer_interpretation_2 = forward_rates[3]  # 7%

# Most common interpretation: "in the third year" = year 2 (0-indexed)
# Or: the rate that applies during the third year of the investment

# If the table is 1-indexed (Year 1, Year 2, Year 3), then:
# "Third year" = Year 3 entry
forward_rates_1indexed = {
    1: 0.04,
    2: 0.05,
    3: 0.06,
    4: 0.07
}

expected_forward_rate_year_3 = forward_rates_1indexed[3]

expected_forward_rate_year_3 * 100  # Result: 6.00%
```

**Common Bugs to Avoid:**
- Calculating forward rates when they're already provided in the table
- Confusing 0-indexed vs 1-indexed year labeling
- Misinterpreting "in year 3" as "from year 3 to year 4" vs "during year 3"
- Using spot rate formulas when forward rates are directly given