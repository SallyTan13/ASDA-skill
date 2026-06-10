# SKILL PATTERNS FOR PROGRAM OF THOUGHT (PoT) FINANCIAL REASONING

## Pattern: Answer Option Mapping Verification

**Description:** After computing the correct numerical result, the model fails to properly map it to the corresponding multiple-choice option, often defaulting to "None of the options" despite an exact match existing.

**When to Use:** All multiple-choice questions where computed values must be matched against provided options (A, B, C, D, E).

**Procedure:**
1. Compute the target value using appropriate financial formulas
2. Round the computed value to match the precision shown in options (typically 2 decimal places)
3. **Explicitly compare** the computed value against each option using conditional logic
4. Store the matching option letter in a variable
5. Return both the computed value AND the matched option letter
6. Include a fallback check that verifies a match was found before returning

**Code Example:**

**Scenario:** Calculate return on equity (ROE) and match to options
**Correct Code:**
```python
# Given data
net_income = 125000
shareholders_equity = 850000

# Calculate ROE
roe = (net_income / shareholders_equity) * 100
roe_rounded = round(roe, 2)

# Define available options
options = {
    'A': 14.50,
    'B': 14.71,
    'C': 15.20,
    'D': 15.85
}

# Match computed value to options
matched_option = None
for option_letter, option_value in options.items():
    if abs(roe_rounded - option_value) < 0.01:  # Allow small tolerance
        matched_option = option_letter
        break

# Verification: ensure match was found
if matched_option is None:
    matched_option = 'E'  # None of the options

# Return the matched option (this is what gets evaluated)
matched_option
```

**Common Bugs to Avoid:**
- Computing correct value but returning 'E' without checking options
- Stating the correct answer in comments/explanation but returning wrong option
- Not implementing explicit option-matching logic in code
- Relying on manual inspection instead of programmatic comparison
- Missing tolerance checks for floating-point comparison

---

## Pattern: Cash Flow Sign Convention

**Description:** When reporting cash flow statement items, uses of cash must be reported with negative signs (e.g., –$4,500) rather than positive amounts with descriptive labels, following standard accounting presentation.

**When to Use:** Questions asking to classify balance sheet changes as "source" or "use" of cash, cash flow statement preparation, working capital analysis.

**Procedure:**
1. Formula: Change = Ending Balance - Beginning Balance
2. Calculate the change in the account balance
3. Determine direction: increase in liability/equity = source (positive), decrease = use (negative)
4. **Apply sign convention**: sources are positive, uses are negative
5. Return the signed numerical value (not absolute value with label)

**Code Example:**

**Scenario:** Analyze change in notes payable for cash flow impact
**Correct Code:**
```python
# Balance sheet data
notes_payable_beginning = 75000
notes_payable_ending = 62000

# Calculate change
change_in_notes_payable = notes_payable_ending - notes_payable_beginning

# Determine cash flow impact with proper sign
# Decrease in liability = use of cash (negative)
# Increase in liability = source of cash (positive)
cash_flow_impact = change_in_notes_payable

# For reporting: use negative sign for uses
# Result: -13000 (meaning use of $13,000)
cash_flow_impact
```

**Common Bugs to Avoid:**
- Returning absolute value with text label ("Use of cash: $13,000")
- Inverting the sign convention (making uses positive)
- Using separate classification variable instead of signed number
- Formatting as string instead of numeric value
- Not following standard cash flow statement presentation format

---

## Pattern: Absolute Value vs Directional Change

**Description:** Financial questions about "percentage change" or "change in value" may expect absolute magnitude rather than signed directional values, depending on context (especially in bond/portfolio sensitivity analysis).

**When to Use:** Questions asking for "percentage change," "change in value," or sensitivity analysis where the direction is already implied by context (e.g., "for an increase in yields").

**Procedure:**
1. Calculate the directional change (with appropriate sign)
2. **Check question wording**: if direction is already specified in question ("for an increase"), return absolute value
3. If question asks "what is the change" without specifying direction, return signed value
4. For percentage changes in bond pricing with yield changes, typically report magnitude
5. Return the appropriate format based on context

**Code Example:**

**Scenario:** Calculate percentage change in bond portfolio value when yields increase
**Correct Code:**
```python
import math

# Portfolio parameters
face_value = 8000
maturity = 4.5
current_yield = 0.08
yield_increase = 0.04
new_yield = current_yield + yield_increase

# Calculate prices
current_price = face_value * math.exp(-current_yield * maturity)
new_price = face_value * math.exp(-new_yield * maturity)

# Calculate percentage change (directional)
pct_change_directional = ((new_price - current_price) / current_price) * 100

# Question asks "for a 4% increase in yields" - direction already specified
# Return absolute magnitude of change
pct_change_magnitude = abs(pct_change_directional)
pct_change_rounded = round(pct_change_magnitude, 2)

# Return magnitude (e.g., 18.45, not -18.45)
pct_change_rounded
```

**Common Bugs to Avoid:**
- Always returning signed values without checking question context
- Always returning absolute values without checking if direction matters
- Not recognizing when question wording implies expected format
- Inconsistent handling between "change" and "percentage change"
- Missing that sensitivity analysis often expects magnitude

---

## Pattern: Decimal Precision vs Integer Rounding

**Description:** Financial calculations often require preserving decimal precision in final answers rather than rounding to integers, especially when questions ask to "solve for" or "calculate" without explicitly requesting whole numbers. The precision level must match the expected format for the specific financial metric type.

**When to Use:** Time value of money calculations (solving for years, rates), ratio analysis, yield calculations, any question that doesn't explicitly say "round to nearest whole number."

**Procedure:**
1. Perform the calculation using appropriate formulas
2. **Check question wording**: look for "round to," "nearest," or "approximately"
3. **Determine metric-specific precision defaults**:
   - Percentages and rates: default to 2 decimal places (e.g., 8.71%, not 8.7%)
   - Ratios: default to 2 decimal places
   - Currency: always 2 decimal places
   - Years/periods: 2 decimal places unless context requires integers
4. If multiple choice, match precision to answer options
5. **Verify precision against expected output format** before finalizing
6. Use `round(value, decimal_places)` with appropriate decimal places
7. Never assume financial values should be integers unless explicitly stated

**Code Example:**

**Scenario:** Calculate effective annual rate (EAR) from nominal rate
**Correct Code:**
```python
import math

# Given values
nominal_rate = 0.12
compounding_periods = 4

# Calculate EAR
ear = (1 + nominal_rate / compounding_periods) ** compounding_periods - 1

# Convert to percentage with proper precision
# Rates/percentages default to 2 decimal places
ear_percentage = round(ear * 100, 2)

# Return: 12.55 (NOT 12.6 or 13)
ear_percentage
```

**Common Bugs to Avoid:**
- Assuming years must be integers and applying `round(years)` or `int(years)`
- **Rounding percentages/rates to 1 decimal place when 2 decimals expected** (e.g., 8.7 instead of 8.71)
- Over-rounding when options show decimal precision
- Using integer division when float division is needed
- Not matching precision to answer options in multiple choice
- Rounding too early in multi-step calculations
- **Not applying metric-specific precision defaults** (percentages need 2 decimals by default)
- Inconsistent precision between calculation and final output
## Pattern: Currency Symbol Formatting

**Description:** Monetary value answers require explicit currency symbols (e.g., "$3" not "3") in the final output, even when the calculation itself is numerically correct.

**When to Use:** Questions asking for dollar amounts, prices, values, costs, or any monetary result where the ground truth includes a currency symbol.

**Procedure:**
1. Perform the numerical calculation
2. Round to appropriate decimal places (typically 2 for currency)
3. **Format as currency string** using f-string or string formatting
4. Include dollar sign and comma separators for large amounts
5. Return formatted string (not raw number)

**Code Example:**

**Scenario:** Calculate intrinsic value of a put option
**Correct Code:**
```python
# Option parameters
exercise_price = 95
current_stock_price = 88

# Calculate intrinsic value
intrinsic_value = max(exercise_price - current_stock_price, 0)

# Format as currency with dollar sign
intrinsic_value_formatted = f"${intrinsic_value:,.2f}"

# Return formatted string: "$7.00" (NOT 7)
intrinsic_value_formatted
```

**Common Bugs to Avoid:**
- Returning raw numeric value (3) instead of currency string ("$3")
- Missing dollar sign in output
- Incorrect decimal places for currency (should be 2)
- Not using comma separators for large amounts (e.g., "$1000000" vs "$1,000,000")
- Returning float when string format is expected

---

## Pattern: Final Expression Return (Not Print)

**Description:** PoT code must end with an expression that evaluates to the answer, not a print statement, as the execution environment captures the last expression value.

**When to Use:** All PoT code blocks in financial reasoning tasks.

**Procedure:**
1. Perform all calculations and store in variables
2. Create final result variable with appropriate formatting
3. **Last line must be variable name or expression** (not `print()`)
4. Avoid multiple expressions on last line
5. Ensure the final expression type matches expected answer format

**Code Example:**

**Scenario:** Calculate debt-to-equity ratio
**Correct Code:**
```python
# Balance sheet data
total_debt = 450000
total_equity = 625000

# Calculate ratio
debt_to_equity = total_debt / total_equity
debt_to_equity_rounded = round(debt_to_equity, 2)

# CORRECT: Last line is expression
debt_to_equity_rounded

# WRONG: print(debt_to_equity_rounded)
# WRONG: f"The ratio is {debt_to_equity_rounded}"  # if numeric answer expected
```

**Common Bugs to Avoid:**
- Using `print(result)` on last line instead of `result`
- Ending with assignment (`result = value`) instead of expression (`result`)
- Multiple statements on last line
- Returning string when number expected (or vice versa)
- Not having any return expression at all

---

## Pattern: Multiple Choice Option Tolerance Matching

**Description:** When matching computed values to multiple choice options, implement tolerance-based comparison to handle floating-point precision issues rather than exact equality checks. The tolerance level must be appropriate for the precision of the answer options to avoid both false negatives (rejecting correct matches) and false positives (accepting incorrect matches).

**When to Use:** All multiple-choice questions with numerical answers, especially those involving division, logarithms, or exponential calculations.

**When NOT to Use:** 
- When the computed value is significantly different from all options (e.g., off by more than 1% relative error), indicating a conceptual error rather than rounding
- When options have very high precision (4+ decimal places) and computed value differs in the 3rd or 4th decimal place — this may indicate the need to recalculate rather than force a match

**Procedure:**
1. Compute the target value
2. Round to precision matching the options
3. **Determine appropriate tolerance** based on option precision:
   - For 2 decimal places: use tolerance of 0.01 (1% of unit)
   - For 3 decimal places: use tolerance of 0.001
   - For 4 decimal places: use tolerance of 0.005 (allows for reasonable rounding differences)
4. Iterate through options to find match within tolerance
5. **If no match found, verify calculation is correct** before defaulting to 'E'/'None'
6. Return matched option letter or 'E'/'None' if genuinely no match

**Common Mistakes to Avoid:**
- Using overly strict tolerance (e.g., 0.0001 for 4-decimal options) that rejects valid matches due to minor rounding differences
- Not adjusting tolerance based on the precision level of the answer options
- Forcing a match when the computed value is conceptually wrong (e.g., using wrong formula)
- Defaulting to 'E' without considering that the tolerance may be too strict

**Example (sanitized):**
> **Scenario:** Calculate inventory turnover ratio (COGS/Average Inventory) and match to options with 4 decimal places
> **Wrong approach:** Using tolerance = 0.0001 for options like [2.3456, 2.4123, 2.5789], which rejects computed value 2.9412 when option is 2.9400 (difference of 0.0012)
> **Correct approach:** For 4-decimal options, use tolerance = 0.005 to accommodate reasonable rounding differences: `if abs(computed - option) < 0.005` would correctly match 2.9412 to 2.9400

---
## Pattern: Forward Rate vs Spot Rate Calculation

**Description:** When calculating yields or spot rates from forward rates, correctly apply the compounding relationship over the appropriate time periods.

**When to Use:** Bond pricing with forward rates, yield curve calculations, zero-coupon bond YTM from forward rate tables.

**Procedure:**
1. Formula: (1 + spot_n)^n = (1 + f_0) × (1 + f_1) × ... × (1 + f_{n-1})
2. Identify which forward rates apply to the time period
3. Multiply compound factors for each period
4. Take the nth root to get the spot rate
5. Verify the number of periods matches the bond maturity

**Code Example:**

**Scenario:** Calculate 4-year spot rate from forward rates
**Correct Code:**
```python
# Forward rates for each year
forward_rates = [0.04, 0.05, 0.06, 0.07]  # Years 0, 1, 2, 3

# Calculate compound factor
compound_factor = 1.0
for rate in forward_rates:
    compound_factor *= (1 + rate)

# Solve for spot rate: (1 + spot)^n = compound_factor
n_years = len(forward_rates)
spot_rate = (compound_factor ** (1 / n_years)) - 1

# Convert to percentage
spot_rate_pct = round(spot_rate * 100, 2)

spot_rate_pct
```

**Common Bugs to Avoid:**
- Using wrong number of forward rates (e.g., 4 rates for 3-year bond)
- Averaging forward rates instead of compounding
- Forgetting to subtract 1 after taking nth root
- Using arithmetic mean instead of geometric mean
- Off-by-one errors in period counting

---

## Pattern: Zero-Coupon Bond Pricing with Continuous Compounding

**Description:** When pricing zero-coupon bonds with continuous compounding, use the exponential formula PV = FV × e^(-rt), not discrete compounding.

**When to Use:** Bond pricing problems that specify continuous compounding, questions referencing exponential discounting.

**Procedure:**
1. Formula: PV = FV × e^(-r × t)
2. Import math module for `math.exp()`
3. Ensure rate is in decimal form (not percentage)
4. Multiply rate by time period
5. Apply negative sign in exponent for discounting

**Code Example:**

**Scenario:** Price a zero-coupon bond with continuous compounding
**Correct Code:**
```python
import math

# Bond parameters
face_value = 10000
maturity_years = 7
annual_yield = 0.085  # 8.5%

# Price with continuous compounding: PV = FV * e^(-r*t)
present_value = face_value * math.exp(-annual_yield * maturity_years)
present_value_rounded = round(present_value, 2)

present_value_rounded
```

**Common Bugs to Avoid:**
- Using discrete compounding formula: `FV / (1 + r)^t`
- Forgetting to import math module
- Using positive exponent instead of negative
- Confusing annual rate with periodic rate
- Not converting percentage to decimal

---

## Pattern: Average Balance Calculation for Ratios

**Description:** Financial ratios involving balance sheet items often require averaging beginning and ending balances, not just using the ending balance.

**When to Use:** Days sales outstanding, inventory turnover, receivables turnover, any ratio mixing income statement (flow) with balance sheet (stock) items.

**Procedure:**
1. Formula: Average = (Beginning Balance + Ending Balance) / 2
2. Identify if ratio uses income statement item (annual flow)
3. If mixing flow and stock, use average balance sheet amount
4. Calculate average before computing ratio
5. Verify which year's balances to use

**Code Example:**

**Scenario:** Calculate accounts receivable turnover
**Correct Code:**
```python
# Income statement (flow)
annual_sales = 2400000

# Balance sheet (stock) - need average
accounts_receivable_beginning = 185000
accounts_receivable_ending = 215000

# Calculate average accounts receivable
avg_accounts_receivable = (accounts_receivable_beginning + accounts_receivable_ending) / 2

# Calculate turnover ratio
receivables_turnover = annual_sales / avg_accounts_receivable
receivables_turnover_rounded = round(receivables_turnover, 2)

receivables_turnover_rounded
```

**Common Bugs to Avoid:**
- Using only ending balance instead of average
- Using only beginning balance
- Averaging when both items are flows (not needed)
- Wrong year's balance sheet data
- Not recognizing when averaging is required

---

## Pattern: Verification Before Option Selection

**Description:** Before returning a final answer option, implement explicit verification that the computed value actually matches the selected option, preventing logic errors in the mapping step.

**When to Use:** All multiple-choice questions, especially when complex calculations might introduce edge cases.

**Procedure:**
1. Compute the numerical result
2. Match to options and store selected option letter
3. **Verify**: retrieve the option value and confirm it matches computed value
4. If verification fails, return 'E' or flag error
5. Only return option letter after successful verification

**Code Example:**

**Scenario:** Calculate P/E ratio with verification
**Correct Code:**
```python
# Financial data
market_price = 72
earnings_per_share = 4.25

# Calculate P/E ratio
pe_ratio = market_price / earnings_per_share
pe_ratio_rounded = round(pe_ratio, 2)

# Options
options = {
    'A': 16.50,
    'B': 16.94,
    'C': 17.25,
    'D': 17.88
}

# Match to option
matched_option = None
for letter, value in options.items():
    if abs(pe_ratio_rounded - value) < 0.01:
        matched_option = letter
        break

# VERIFICATION STEP
if matched_option is not None:
    # Confirm the match is correct
    if abs(pe_ratio_rounded - options[matched_option]) < 0.01:
        final_answer = matched_option
    else:
        final_answer = 'E'  # Verification failed
else:
    final_answer = 'E'

final_answer
```

**Common Bugs to Avoid:**
- Skipping verification step entirely
- Returning option without confirming value match
- Not handling case where no option matches
- Verification logic that always passes
- Contradicting computed value with returned option

## Pattern: Bond Price Quote Interpretation

**Description:** Bond prices in financial quotes can be presented in two formats: (1) as a percentage of par value (e.g., 105.312 meaning 105.312% of $1,000 = $1,053.12), or (2) as an absolute dollar price (e.g., 105.312 meaning $105.312). The correct interpretation depends on context clues such as whether the price is above/below 100, the bond's coupon rate relative to market rates, and typical market conventions.

**When to Use:** Bond valuation problems involving yield to maturity (YTM), current yield, or price calculations where a bond price quote is provided.

**Procedure:**
1. **Examine the quoted price magnitude**:
   - If price > 100: likely percentage of par (e.g., 105.312 = 105.312%)
   - If price < 100: could be either format — need additional context
   - If price is very small (e.g., < 50): likely absolute dollar price
2. **Check coupon rate vs. expected market yield**:
   - If coupon rate > expected YTM: bond should trade at premium (price > 100% of par)
   - If coupon rate < expected YTM: bond should trade at discount (price < 100% of par)
3. **Consider market conventions**:
   - Corporate and government bonds typically quoted as percentage of par
   - Zero-coupon bonds may be quoted as absolute prices when deeply discounted
4. **Test both interpretations** if ambiguous:
   - Calculate YTM assuming percentage of par
   - Calculate YTM assuming absolute dollar price
   - Select interpretation that yields reasonable market yield (typically 2%-15% for most bonds)
5. **Verify reasonableness**: The resulting YTM should be economically sensible given the bond's characteristics

**Common Mistakes to Avoid:**
- Automatically assuming all bond prices are percentages of par without checking magnitude
- Not validating that the resulting YTM is economically reasonable
- Ignoring the relationship between coupon rate and price (premium vs. discount)
- Failing to test both interpretations when the format is ambiguous

**Example (sanitized):**
> **Scenario:** A bond quote shows "Price: 108.45" for a 6.5% coupon bond maturing in 8 years with $1,000 face value
> **Wrong approach:** Treating 108.45 as absolute dollar price ($108.45), which would imply an impossibly high YTM of ~60% for a bond trading below face value
> **Correct approach:** Recognize that 108.45 represents 108.45% of par = $1,084.50, which makes sense for a bond trading at premium (price > par when coupon > market yield), yielding a reasonable YTM around 5.2%