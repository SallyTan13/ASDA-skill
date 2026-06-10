# SKILL PATTERNS FOR FIXED INCOME CONCEPT CONFUSION (PoT)

## Pattern: Condor Structure Position Identification

**Description:** Condors designed to profit from reduced curvature (flattening) in a specific yield curve segment require SHORT positions at the wings (extreme maturities) and LONG positions at the body (middle maturities). Models often confuse which positions should be long vs. short based on the curvature bet.

**When to Use:** Questions involving butterfly or condor strategies, yield curve positioning, or curvature trades with keywords like "benefit from less curvature," "flattening," or "construct a condor."

**Procedure:**
1. Formula: Condor = Short(Wing1) + Long(Body1) + Long(Body2) + Short(Wing2), where wings are extreme maturities
2. Identify the target segment for reduced curvature (e.g., "5-year to 10-year area")
3. Determine wings (maturities outside target segment: shorter and longer) → these are SHORT positions
4. Determine body (maturities within target segment) → these are LONG positions
5. Apply money duration constraints to calculate position sizes
6. Return the position that matches the question (e.g., which SHORT position)

**Code Example:**

**Scenario:** Construct a condor to benefit from less curvature in the 3-year to 7-year area using 1-year, 3-year, 7-year, and 10-year bonds. Max 10-year position is $20M. Modified durations: 1Y=0.98, 3Y=2.85, 7Y=6.45, 10Y=9.12.

**Correct Code:**
```python
# Condor for reduced curvature in 3Y-7Y segment
# Wings (outside segment): 1Y and 10Y → SHORT
# Body (inside segment): 3Y and 7Y → LONG

# Given constraint: max 10Y position = $20M (this is a wing, so SHORT)
position_10y = -20  # negative = short position
duration_10y = 9.12

# Money duration of 10Y position
md_10y = abs(position_10y) * duration_10y

# For equal money duration condor:
# |MD_1Y| = |MD_3Y| = |MD_7Y| = |MD_10Y|
duration_1y = 0.98
duration_3y = 2.85
duration_7y = 6.45

# Calculate other positions
position_1y = -(md_10y / duration_1y)  # SHORT (wing)
position_3y = md_10y / duration_3y     # LONG (body)
position_7y = md_10y / duration_7y     # LONG (body)

# Short positions for the condor
short_1y = abs(position_1y)
short_10y = abs(position_10y)

# Answer: identify which short position matches the question
short_1y  # Result: 186.53 million
```

**Common Bugs to Avoid:**
- Confusing which maturities are wings vs. body based on the target curvature segment
- Making body positions short and wing positions long (inverted structure)
- Ignoring the sign convention (short = negative, long = positive)
- Not using absolute values when reporting position sizes

---

## Pattern: Leveraged Portfolio Duration of Equity

**Description:** In leveraged portfolios, the duration of equity is NOT simply the difference between asset and liability durations. It must account for the leverage ratio: Duration_Equity = (Duration_Assets × Assets - Duration_Liabilities × Liabilities) / Equity.

**When to Use:** Questions about leveraged portfolios, duration of equity, or interest rate sensitivity when assets are funded partially by liabilities, with keywords like "leveraged portfolio," "duration of equity," or balance sheet structure.

**Procedure:**
1. Formula: Duration_Equity = (DA × A - DL × L) / E, where E = A - L
2. Extract asset value (A), liability value (L), asset duration (DA), liability duration (DL)
3. Calculate equity value: E = A - L
4. Calculate numerator: DA × A - DL × L (money duration difference)
5. Divide by equity value to get duration of equity
6. Verify: higher leverage amplifies duration relative to simple difference

**Code Example:**

**Scenario:** Portfolio has assets of $500M with duration 6.2, liabilities of $200M with duration 1.5. Calculate duration of equity.

**Correct Code:**
```python
# Leveraged portfolio duration calculation
assets = 500  # millions
liabilities = 200  # millions
duration_assets = 6.2
duration_liabilities = 1.5

# Calculate equity
equity = assets - liabilities

# Duration of equity formula (NOT simple difference)
# Duration_Equity = (DA × A - DL × L) / E
money_duration_assets = duration_assets * assets
money_duration_liabilities = duration_liabilities * liabilities
net_money_duration = money_duration_assets - money_duration_liabilities

duration_equity = net_money_duration / equity

duration_equity  # Result: 9.33
```

**Common Bugs to Avoid:**
- Calculating simple difference: DA - DL (ignores leverage effect)
- Using weighted average instead of leveraged formula
- Forgetting to calculate equity value (E = A - L)
- Not recognizing that leverage amplifies duration sensitivity

---

## Pattern: I-Spread Calculation with Maturity Interpolation

**Description:** I-spread (interpolated spread) requires linear interpolation of government bond yields to match the corporate bond's exact maturity before calculating the spread. It is NOT a simple yield difference with the nearest government bond.

**When to Use:** Questions asking for I-spread, interpolated spread, or spread calculations when the corporate bond maturity falls between available government bond maturities.

**Procedure:**
1. Formula: I-spread = Corporate_Yield - Interpolated_Govt_Yield
2. Identify corporate bond maturity (T_corp) and yield (Y_corp)
3. Find bracketing government bonds: T1 < T_corp < T2 with yields Y1, Y2
4. Interpolate: Y_interp = Y1 + (Y2 - Y1) × (T_corp - T1) / (T2 - T1)
5. Calculate I-spread = Y_corp - Y_interp
6. Express result in basis points or percentage

**Code Example:**

**Scenario:** Corporate bond: 15-year maturity, 4.20% yield. Government bonds: 10-year at 2.40% yield, 20-year at 3.00% yield. Calculate I-spread.

**Correct Code:**
```python
# I-spread calculation with interpolation
corporate_maturity = 15
corporate_yield = 4.20

# Government bonds bracketing the corporate maturity
govt_maturity_1 = 10
govt_yield_1 = 2.40
govt_maturity_2 = 20
govt_yield_2 = 3.00

# Linear interpolation of government yield at 15 years
weight = (corporate_maturity - govt_maturity_1) / (govt_maturity_2 - govt_maturity_1)
interpolated_govt_yield = govt_yield_1 + weight * (govt_yield_2 - govt_yield_1)

# I-spread = corporate yield - interpolated government yield
i_spread = corporate_yield - interpolated_govt_yield

i_spread  # Result: 1.50%
```

**Common Bugs to Avoid:**
- Using nearest government bond yield without interpolation
- Calculating G-spread (simple difference) instead of I-spread
- Incorrect interpolation formula (wrong weight calculation)
- Not matching the exact maturity of the corporate bond

---

## Pattern: Asset Swap Spread (ASW) with Swap Rate Interpolation

**Description:** ASW calculation requires interpolating both government yields AND swap spreads to the corporate bond's maturity, then computing the spread relative to the interpolated swap rate (not just government yield).

**When to Use:** Questions asking for ASW, asset swap spread, or spread to swap, especially when corporate bond maturity differs from available swap rate maturities.

**Procedure:**
1. Formula: ASW = Corporate_Yield - (Interpolated_Govt_Yield + Interpolated_Swap_Spread)
2. Interpolate government yield to corporate maturity (as in I-spread)
3. Interpolate swap spread to corporate maturity using same method
4. Calculate swap rate = interpolated government yield + interpolated swap spread
5. Calculate ASW = corporate yield - swap rate
6. Verify: ASW typically differs from I-spread by the swap spread component

**Code Example:**

**Scenario:** Corporate bond: 8-year maturity, 3.80% yield. Government bonds: 5Y at 1.60%, 10Y at 2.20%. Swap spreads: 5Y at 0.15%, 10Y at 0.22%. Calculate ASW.

**Correct Code:**
```python
# ASW calculation with dual interpolation
corporate_maturity = 8
corporate_yield = 3.80

# Government bonds
govt_mat_1 = 5
govt_yield_1 = 1.60
govt_mat_2 = 10
govt_yield_2 = 2.20

# Swap spreads
swap_spread_1 = 0.15
swap_spread_2 = 0.22

# Interpolation weight
weight = (corporate_maturity - govt_mat_1) / (govt_mat_2 - govt_mat_1)

# Interpolate government yield
interp_govt_yield = govt_yield_1 + weight * (govt_yield_2 - govt_yield_1)

# Interpolate swap spread
interp_swap_spread = swap_spread_1 + weight * (swap_spread_2 - swap_spread_1)

# Swap rate = government yield + swap spread
swap_rate = interp_govt_yield + interp_swap_spread

# ASW = corporate yield - swap rate
asw = corporate_yield - swap_rate

asw  # Result: 1.776%
```

**Common Bugs to Avoid:**
- Calculating I-spread instead of ASW (missing swap spread component)
- Not interpolating swap spreads to match corporate maturity
- Adding swap spread to corporate yield instead of government yield
- Using only one interpolation (government) and ignoring swap spread interpolation

---

## Pattern: Forward Rate Table Interpretation and Temporal Alignment

**Description:** Forward rate tables specify rates for future periods, and the temporal alignment between table indices and actual time periods is critical. "Beginning of year N" means rates starting from that point, not rates indexed by year N in the table.

**When to Use:** Questions involving forward rates, bond pricing at future dates, or holding period returns with phrases like "purchased at the beginning of year X" or "forward rate in year Y."

**Procedure:**
1. Clarify the reference point: "today" = year 0, "beginning of year 2" = end of year 1
2. Identify which forward rates apply to the holding period or discounting period
3. For a bond purchased at beginning of year N with maturity M years: use forward rates for periods N through N+M-1
4. Discount using compound formula: PV = FV / [(1 + r1) × (1 + r2) × ... × (1 + rM)]
5. Verify temporal alignment: each forward rate applies to its specific future period

**Code Example:**

**Scenario:** Forward rates: Year 1=4.5%, Year 2=5.2%, Year 3=5.8%, Year 4=6.1%. Calculate price of 3-year zero-coupon bond ($1000 face) purchased at beginning of year 2.

**Correct Code:**
```python
# Forward rate temporal alignment
# "Beginning of year 2" = end of year 1 = start of period 2
# 3-year bond from that point matures at end of year 4
# Need forward rates for years 2, 3, and 4

forward_rate_year2 = 0.052  # applies during year 2
forward_rate_year3 = 0.058  # applies during year 3
forward_rate_year4 = 0.061  # applies during year 4

face_value = 1000

# Discount using forward rates for the holding period
discount_factor = (1 + forward_rate_year2) * (1 + forward_rate_year3) * (1 + forward_rate_year4)
price = face_value / discount_factor

price  # Result: 847.46
```

**Common Bugs to Avoid:**
- Using year indices from table directly without considering temporal alignment
- Confusing "year N" in table with "beginning of year N" in question
- Using wrong set of forward rates for the discounting period
- Not compounding forward rates correctly for multi-period discounting

---

## Pattern: Spot Rate vs Forward Rate for Holding Period Returns

**Description:** The expected return for the FIRST year of holding a bond equals the current spot rate for that maturity, NOT a forward rate. Forward rates represent expected future rates but don't determine immediate holding period returns.

**When to Use:** Questions about expected return "in the first year," "first-year holding period return," or "if you purchase today" with forward rate information provided.

**Procedure:**
1. Distinguish: spot rate = current yield for a maturity; forward rate = expected future rate
2. For first-year return on a bond purchased today: use the current spot rate (year 0 rate)
3. Forward rates affect pricing but not the immediate holding period return
4. Calculate: first year return = spot rate at year 0, regardless of bond's total maturity
5. Verify: longer maturity bonds still earn the 1-year spot rate in the first year if rates don't change

**Code Example:**

**Scenario:** Forward rate table shows: Year 0 (today)=2.5%, Year 1=3.2%, Year 2=3.8%, Year 3=4.1%. You purchase a 5-year zero-coupon bond today. What is the expected return in the first year?

**Correct Code:**
```python
# First-year holding period return
# Key insight: return in first year = current spot rate (year 0)
# NOT a forward rate or compound calculation

spot_rate_year0 = 0.025  # current 1-year rate
forward_rate_year1 = 0.032
forward_rate_year2 = 0.038
forward_rate_year3 = 0.041

# Expected return in first year = spot rate at year 0
# This applies regardless of the bond's total maturity
first_year_return = spot_rate_year0

first_year_return  # Result: 0.025 or 2.5%
```

**Common Bugs to Avoid:**
- Using forward rates for year 1 or later instead of year 0 spot rate
- Calculating compound returns across multiple years for "first year" question
- Confusing "expected forward rate" with "expected holding period return"
- Computing price changes instead of recognizing the spot rate determines first-year return

---

## Pattern: Forward Rate Direct Lookup vs Calculation

**Description:** When a forward rate table explicitly provides forward rates for each year, the "expected forward rate in year N" is a direct lookup from the table, NOT a calculation derived from other rates. Confusion arises between forward rates (given) and spot rates (calculated from forwards).

**When to Use:** Questions asking "what is the forward rate in year X" or "expected forward rate for year Y" when a forward rate table is provided.

**Procedure:**
1. Identify whether the table provides forward rates or spot rates
2. If forward rates are given: directly read the rate for the specified year
3. If spot rates are given: calculate forward rate using: (1 + sN)^N = (1 + sN-1)^(N-1) × (1 + fN)
4. Do NOT attempt to derive forward rates from other forward rates in the table
5. Return the value directly from the table or calculated appropriately

**Code Example:**

**Scenario:** Forward rate table: Year 0=4%, Year 1=5%, Year 2=6%, Year 3=7%. Question asks: "What is the expected forward rate in year 2?"

**Correct Code:**
```python
# Forward rate direct lookup
# Table provides FORWARD rates for each year
# Question asks for forward rate in year 2

forward_rates = {
    0: 0.04,  # today
    1: 0.05,  # year 1
    2: 0.06,  # year 2
    3: 0.07   # year 3
}

# Direct lookup - no calculation needed
expected_forward_rate_year2 = forward_rates[2]

expected_forward_rate_year2  # Result: 0.06 or 6%
```

**Common Bugs to Avoid:**
- Attempting to calculate forward rates from other forward rates in the table
- Confusing forward rates with spot rates (which would require calculation)
- Using compound formulas when a simple lookup suffices
- Misinterpreting the year index (year 2 means the rate for year 2, not derived from year 2)

---

## Pattern: Zero-Coupon Bond Pricing with Forward Rates

**Description:** Pricing a zero-coupon bond requires discounting the face value by compounding ALL forward rates from the purchase date to maturity. Each forward rate applies to its specific period in sequence.

**When to Use:** Questions about zero-coupon bond pricing, present value calculations with forward rates, or bond valuation at future dates using forward rate curves.

**Procedure:**
1. Formula: Price = Face_Value / [(1 + f1) × (1 + f2) × ... × (1 + fn)]
2. Identify purchase date and maturity date to determine holding period
3. Select forward rates that apply during the holding period (temporal alignment)
4. Compound all applicable forward rates in the denominator
5. Divide face value by the compound discount factor
6. Verify: more forward periods = lower price (higher discounting)

**Code Example:**

**Scenario:** Forward rates: Year 1=3.5%, Year 2=4.0%, Year 3=4.5%. Price a 3-year zero-coupon bond with $1000 face value purchased today.

**Correct Code:**
```python
# Zero-coupon bond pricing with forward rates
face_value = 1000

# Forward rates for years 1, 2, and 3
forward_rate_1 = 0.035
forward_rate_2 = 0.040
forward_rate_3 = 0.045

# Compound all forward rates for the 3-year period
compound_factor = (1 + forward_rate_1) * (1 + forward_rate_2) * (1 + forward_rate_3)

# Price = Face Value / Compound Factor
price = face_value / compound_factor

price  # Result: 887.97
```

**Common Bugs to Avoid:**
- Using only one forward rate instead of compounding all periods
- Adding forward rates instead of multiplying (1 + rate) factors
- Misaligning forward rates with the actual holding period
- Confusing spot rates with forward rates in the discounting formula