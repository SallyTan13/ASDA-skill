# SKILL PATTERNS FOR CORPORATE FINANCE CONCEPT CONFUSION (PoT)

## Pattern: Sign Convention in NPV and Cash Flow Calculations

**Description:** NPV and cash flow metrics are signed values that convey economic meaning (positive = value creation, negative = value destruction). Failing to preserve signs or incorrectly treating inflows/outflows leads to economically meaningless results.

**When to Use:** NPV calculations, cash flow to creditors/stockholders, any metric where direction of cash flow matters (keywords: "NPV", "cash flow to", "net present value", "should accept/reject")

**Procedure:**
1. Formula: NPV = Σ[CFt / (1+r)^t] where CF signs matter: inflows are positive, outflows are negative
2. Identify cash flow direction: money received = positive, money paid = negative
3. For cash flow to creditors: Interest Paid - Net New Borrowing (where borrowing = ending debt - beginning debt)
4. Preserve signs through all calculations; never take absolute value
5. Return the signed result as-is (negative NPV means reject project)

**Code Example:**

**Scenario:** Calculate NPV of a project requiring $50,000 initial investment, generating $20,000 in year 1, $25,000 in year 2, and $18,000 in year 3 at 8% discount rate.

**Correct Code:**
```python
# Cash flows with proper signs: outflow negative, inflows positive
cf_0 = -50000  # Initial investment (outflow)
cf_1 = 20000
cf_2 = 25000
cf_3 = 18000
r = 0.08

# NPV calculation preserving signs
npv = cf_0 + cf_1/(1+r)**1 + cf_2/(1+r)**2 + cf_3/(1+r)**3

# Result: npv (approximately 4,139.45, positive means accept)
npv
```

**Common Bugs to Avoid:**
- Taking `abs()` of final NPV, destroying economic meaning
- Treating initial investment as positive instead of negative outflow
- Using `print(npv)` instead of expression `npv` on last line
- Reversing sign convention (inflows negative, outflows positive)

---

## Pattern: Cash Flow to Creditors with Net Borrowing

**Description:** Cash flow to creditors represents net cash paid OUT to debt holders, calculated as interest paid MINUS net new borrowing. New borrowing reduces cash flow to creditors because the firm receives cash FROM creditors. Net new borrowing = New debt issued - Debt repaid = Ending debt - Beginning debt (from balance sheet).

**When to Use:** Questions asking for "cash flow to creditors" or "cash flow to bondholders" given interest paid and debt changes (keywords: "cash flow to creditors", "raised in new long-term debt", "interest paid", "long-term debt" balance sheet changes)

**Procedure:**
1. Formula: Cash_Flow_to_Creditors = Interest_Paid - Net_New_Borrowing
2. Calculate net new borrowing from balance sheet: Ending_LT_Debt - Beginning_LT_Debt
3. Or use given information: New_Debt_Issued - Debt_Repaid
4. Subtract net new borrowing from interest paid (borrowing is cash FROM creditors, reducing net payment TO them)
5. Return the result (can be negative if firm borrowed more than it paid in interest)

**Code Example:**

**Scenario:** A firm paid $42,000 in interest during the year. Long-term debt was $380,000 at the beginning of the year and $510,000 at the end. What is the cash flow to creditors?

**Correct Code:**
```python
# Given data
interest_paid = 42000
beginning_lt_debt = 380000
ending_lt_debt = 510000

# Calculate net new borrowing
net_new_borrowing = ending_lt_debt - beginning_lt_debt  # 130000

# Cash flow to creditors
cash_flow_to_creditors = interest_paid - net_new_borrowing  # 42000 - 130000

cash_flow_to_creditors  # -88000 (negative means firm received net cash from creditors)
```

**Common Bugs to Avoid:**
- Adding net new borrowing instead of subtracting (wrong sign convention)
- Using only interest paid without considering debt changes
- Calculating net new borrowing as beginning minus ending (reversed)
- Treating negative result as an error (negative is valid when firm borrows more than it pays)
- Forgetting that "cash flow TO creditors" means from firm's perspective (outflow)

---
## Pattern: Merger NPV with Acquisition Premium

**Description:** In merger NPV calculations, NPV to the acquirer equals the value created (synergies) minus the premium paid above target's current market value. The cost is only the excess payment over market value, not the total cash paid. Total cost = Premium paid = Cash_Paid - Target_Market_Value.

**When to Use:** Merger/acquisition NPV questions with synergy values and target market prices (keywords: "NPV of merger", "NPV of acquisition", "synergistic benefits", "value of synergies", "acquire for", "bidding firm")

**Procedure:**
1. Formula: NPV_to_Acquirer = Synergy_Value - Premium_Paid
2. Calculate target's standalone market value: Target_Shares × Target_Price_per_Share
3. If cash offer given: Premium = Cash_Paid - Target_Market_Value
4. If premium not explicitly given, it must be inferred from context or calculated
5. Return NPV (value created minus value transferred to target shareholders)

**Code Example:**

**Scenario:** Firm A is acquiring Firm B, which has 5,000 shares trading at $32 per share. The synergies from the merger are valued at $18,000. If the question asks about NPV assuming conditions where a premium is paid (e.g., "assuming the conditions in question 4" where a premium was calculated), and that premium was determined to be $10,500, what is the NPV?

**Correct Code:**
```python
# Given data
target_shares = 5000
target_price_per_share = 32
synergy_value = 18000
premium_paid = 10500  # From previous question/context

# Calculate target market value
target_market_value = target_shares * target_price_per_share  # 160000

# NPV to acquirer
npv_to_acquirer = synergy_value - premium_paid  # 18000 - 10500

npv_to_acquirer  # 7500
```

**Common Bugs to Avoid:**
- Returning synergy value as NPV without subtracting premium (ignoring cost to acquirer)
- Using total cash paid instead of premium over market value
- Forgetting that target shareholders capture part of synergy value through premium
- Not recognizing that NPV can be negative if premium exceeds synergies
- Confusing total value created (synergies) with value captured by acquirer (NPV)

---
## Pattern: Stock-for-Stock Merger Post-Merger Share Price

**Description:** In stock mergers with no synergies, post-merger share price equals combined market value divided by total shares outstanding after merger. Must account for dilution from new shares issued.

**When to Use:** Merger questions asking for "share price after merger" with stock exchange ratios (keywords: "shares of A for shares of B", "post-merger price", "no synergies")

**Procedure:**
1. Formula: Post-Merger Price = (Market Value A + Market Value B) / Total Shares After Merger
2. Calculate pre-merger market values: Price × Shares for each firm
3. Calculate new shares issued = Target Shares / Exchange Ratio
4. Total shares after = Acquirer Shares + New Shares Issued
5. Post-merger price = Combined Market Value / Total Shares After

**Code Example:**

**Scenario:** Firm A has 1,200 shares at $50/share. Firm B has 400 shares at $15/share. A offers 1 share of A for every 4 shares of B. No synergies.

**Correct Code:**
```python
# Pre-merger data
a_shares = 1200
a_price = 50
b_shares = 400
b_price = 15
exchange_ratio = 4  # 4 shares of B get 1 share of A

# Pre-merger market values
market_value_a = a_shares * a_price
market_value_b = b_shares * b_price

# New shares issued to B shareholders
new_shares_issued = b_shares / exchange_ratio

# Total shares after merger
total_shares_after = a_shares + new_shares_issued

# Combined market value (no synergies)
combined_value = market_value_a + market_value_b

# Post-merger share price
post_merger_price = combined_value / total_shares_after

# Result: (60000 + 6000) / (1200 + 100) = 66000 / 1300 = 50.77
post_merger_price
```

**Common Bugs to Avoid:**
- Returning exchange ratio instead of share price
- Forgetting to add new shares issued to denominator
- Using only acquirer's shares in denominator
- Incorrectly calculating new shares (multiplying instead of dividing by exchange ratio)

---

## Pattern: Credit Policy Change with Receivables Buildup

**Description:** Switching from cash to credit sales creates two effects: (1) one-time upfront cost of receivables buildup (PV of one period's sales under new policy), and (2) perpetual incremental profit stream. NPV = PV(perpetual incremental profits) - Initial receivables investment.

**When to Use:** Credit policy change questions with cash vs. credit terms, unit sales changes, and required returns (keywords: "change in credit policy", "net one month", "receivables buildup")

**Procedure:**
1. Formula: NPV = [Incremental Monthly Profit / r] - Initial Receivables Investment
2. Calculate incremental monthly profit = (New Units - Old Units) × (Price - Cost)
3. Calculate initial receivables = (New Units × Cost) × [1 / (1 + r)] for one period credit
4. Calculate PV of perpetuity = Incremental Profit / r (where r is per-period rate)
5. NPV = PV of perpetuity - Initial receivables

**Code Example:**

**Scenario:** Current: 800 units/month cash sales at $100, cost $65. New: 880 units/month, net one month terms. Required return 0.8% per month.

**Correct Code:**
```python
# Current and new policy data
price = 100
cost = 65
current_units = 800
new_units = 880
r_monthly = 0.008

# Incremental monthly profit (perpetual)
incremental_units = new_units - current_units
incremental_profit_monthly = incremental_units * (price - cost)

# PV of perpetual incremental profits
pv_perpetuity = incremental_profit_monthly / r_monthly

# Initial receivables buildup (one month of new sales at cost)
# Discounted back one period since payment delayed
initial_receivables = (new_units * cost) / (1 + r_monthly)

# NPV of policy change
npv_policy = pv_perpetuity - initial_receivables

# Result: (80 * 35 / 0.008) - (880 * 65 / 1.008) = 350000 - 56746.03 = 293253.97
npv_policy
```

**Common Bugs to Avoid:**
- Returning only monthly incremental profit, not NPV
- Forgetting to discount initial receivables investment
- Using price instead of cost for receivables buildup
- Not recognizing perpetuity structure of ongoing profits

---

## Pattern: Zero-NPV Acquisition and P/E Ratio Preservation

**Description:** When NPV of acquisition is zero, no value is created/destroyed, so the post-merger P/E ratio equals the acquirer's pre-merger P/E ratio. Zero NPV means market values the combined entity at the same multiple as the acquirer alone.

**When to Use:** Merger questions asking for P/E ratio given NPV=0 condition (keywords: "if NPV is zero", "what P/E ratio", "indifferent")

**Procedure:**
1. Concept: NPV = 0 implies Post-Merger P/E = Acquirer's Pre-Merger P/E
2. Extract acquirer's pre-merger P/E from given data
3. Recognize that zero NPV means no synergies or exactly fair price paid
4. Return acquirer's P/E (no calculation needed beyond identifying it)

**Code Example:**

**Scenario:** Acquirer has P/E of 15.2, target has P/E of 9.8. If NPV of acquisition is zero, what is post-merger P/E?

**Correct Code:**
```python
# Given P/E ratios
acquirer_pe = 15.2
target_pe = 9.8

# When NPV = 0, no value created/destroyed
# Post-merger P/E equals acquirer's pre-merger P/E
post_merger_pe = acquirer_pe

# Result: 15.2
post_merger_pe
```

**Common Bugs to Avoid:**
- Calculating weighted average of P/E ratios
- Using target's P/E ratio
- Attempting complex calculations when answer is conceptual
- Confusing with EPS dilution calculations

---

## Pattern: Gordon Growth Model for Acquisition Valuation

**Description:** Maximum acquisition price per share uses dividend discount model with POST-ACQUISITION growth rate. Value = D1/(r-g) where g is the NEW growth rate acquirer expects to achieve, and r is derived from target's current valuation.

**When to Use:** Acquisition valuation with dividend growth rates, especially when acquirer expects to change growth rate (keywords: "maximum price", "growth rate will increase to", "willing to pay")

**Procedure:**
1. Formula: Max Price = D1 / (r - g_new), where D1 = D0 × (1 + g_new)
2. Calculate current required return: r = (D0 × (1 + g_old) / P0) + g_old
3. Calculate next year's dividend with NEW growth: D1 = Current Dividend × (1 + g_new)
4. Apply Gordon model with new growth: Max Price = D1 / (r - g_new)
5. Verify r > g_new for model validity

**Code Example:**

**Scenario:** Target pays $2.50 dividend, currently $35/share with 3% growth. Acquirer expects to achieve 5% growth. What's max price per share?

**Correct Code:**
```python
# Target's current data
current_dividend = 2.50
current_price = 35
current_growth = 0.03
new_growth = 0.05  # Acquirer's expected growth

# Derive required return from current market price
# P0 = D1 / (r - g) => r = (D1/P0) + g
d1_current = current_dividend * (1 + current_growth)
required_return = (d1_current / current_price) + current_growth

# Calculate D1 with NEW growth rate
d1_new = current_dividend * (1 + new_growth)

# Maximum price using new growth rate
max_price_per_share = d1_new / (required_return - new_growth)

# Result: 2.625 / (0.1036 - 0.05) = 2.625 / 0.0536 = 48.97
max_price_per_share
```

**Common Bugs to Avoid:**
- Using old growth rate in valuation formula
- Not updating D1 with new growth rate
- Calculating required return incorrectly
- Using target's P/E ratio instead of dividend model

---

## Pattern: Investment NPV with Market-to-Book Ratio

**Description:** When a new investment maintains the same P/E and ROE as existing firm, NPV = Investment × (M/B - 1). This reflects that market values each dollar of book equity at M/B ratio, so investing at book creates value of (M/B - 1) per dollar.

**When to Use:** Investment decisions where new project has "same P/E" or "same ROE" as firm, with equity financing (keywords: "same P/E ratio", "same ROE", "new equity issue")

**Procedure:**
1. Formula: NPV = Investment Amount × (Market-to-Book Ratio - 1)
2. Calculate book value of equity = Total Assets - Total Liabilities
3. Calculate market value of equity = Stock Price × Shares Outstanding
4. Calculate M/B ratio = Market Value / Book Value
5. NPV = Investment × (M/B - 1)

**Code Example:**

**Scenario:** Firm has stock price $42, 80,000 shares, total assets $4,200,000, liabilities $1,800,000. Considering $900,000 investment with same P/E and ROE, financed with equity.

**Correct Code:**
```python
# Firm data
stock_price = 42
shares_outstanding = 80000
total_assets = 4200000
total_liabilities = 1800000
investment_amount = 900000

# Book value of equity
book_value_equity = total_assets - total_liabilities

# Market value of equity
market_value_equity = stock_price * shares_outstanding

# Market-to-book ratio
market_to_book = market_value_equity / book_value_equity

# NPV when investment maintains same multiples
npv_investment = investment_amount * (market_to_book - 1)

# Result: 900000 * (3360000/2400000 - 1) = 900000 * 0.4 = 360000
npv_investment
```

**Common Bugs to Avoid:**
- Calculating ROE or P/E explicitly when M/B shortcut applies
- Using market value in denominator of M/B ratio
- Forgetting to subtract 1 from M/B ratio
- Not recognizing when this pattern applies (same multiples condition)

---

## Pattern: Equity as Residual Claim with Limited Liability

**Description:** Equity value in each state equals max(0, Firm_Value - Debt_Face_Value), not simply the difference. Limited liability means equity cannot be negative; shareholders walk away if firm value falls below debt obligations, leaving equity value at zero.

**When to Use:** State-contingent valuation with debt, especially when firm value can fall below debt face value (keywords: "equity value", "stock value", "states of economy", "bond outstanding", "after merger", "limited liability")

**Procedure:**
1. Formula: Equity_Value_in_State = max(0, Firm_Value_in_State - Total_Debt_Face_Value)
2. For each economic state, calculate firm value minus total debt
3. If result is negative, equity value is zero (limited liability)
4. If result is positive, that is the equity value
5. For expected equity value, probability-weight across states

**Code Example:**

**Scenario:** A merged company has total debt of $1,200,000. In a worst-case state (probability 0.15), combined firm value is $800,000. In a base state (probability 0.60), firm value is $1,500,000. In a best state (probability 0.25), firm value is $2,100,000. What is the equity value in the worst-case state?

**Correct Code:**
```python
# Given data
total_debt_face_value = 1200000
worst_case_firm_value = 800000
worst_case_probability = 0.15

# Equity value in worst-case state (limited liability)
equity_value_worst = max(0, worst_case_firm_value - total_debt_face_value)

# Detailed: 800000 - 1200000 = -400000, but max(0, -400000) = 0

equity_value_worst  # 0

# For expected equity value across all states:
states = [
    {'probability': 0.15, 'firm_value': 800000},
    {'probability': 0.60, 'firm_value': 1500000},
    {'probability': 0.25, 'firm_value': 2100000}
]

expected_equity_value = sum(
    state['probability'] * max(0, state['firm_value'] - total_debt_face_value)
    for state in states
)
# 0.15*0 + 0.60*300000 + 0.25*900000 = 0 + 180000 + 225000 = 405000
```

**Common Bugs to Avoid:**
- Calculating Firm_Value - Debt without max(0, ...) wrapper (allowing negative equity)
- Returning negative equity values (violates limited liability principle)
- Forgetting that shareholders lose only their investment, not more
- Not applying max() function in each state separately before probability weighting
- Confusing equity value (residual after debt) with firm value (total enterprise value)
## Pattern: Risky Debt Valuation in Merger Context

**Description:** When firm value can fall below debt face value, debt value equals the probability-weighted expected value of what bondholders actually receive in each state: min(Firm_Value, Face_Value) in each state. Debt is a contingent claim whose value depends on default risk.

**When to Use:** Debt valuation with state-contingent firm values where firm value may be less than debt face value (keywords: "value of debt", "bond outstanding", "states of economy", "face value", "operate separately")

**Procedure:**
1. Formula: Debt_Value = Σ[Probability_i × min(Firm_Value_i, Face_Value)]
2. For each economic state, determine bondholders' payoff: min(firm value in that state, face value)
3. Multiply each payoff by its probability
4. Sum across all states to get expected debt value
5. Return the total expected value

**Code Example:**

**Scenario:** A firm has debt with face value $200,000. In a boom state (probability 0.60), firm value is $350,000. In a recession state (probability 0.40), firm value is $150,000. What is the debt value?

**Correct Code:**
```python
# Given data
face_value = 200000
states = [
    {'probability': 0.60, 'firm_value': 350000},  # Boom
    {'probability': 0.40, 'firm_value': 150000}   # Recession
]

# Calculate expected debt value considering default risk
debt_value = sum(
    state['probability'] * min(state['firm_value'], face_value)
    for state in states
)

debt_value  # 0.60 * 200000 + 0.40 * 150000 = 180000
```

**Common Bugs to Avoid:**
- Returning face value without considering default risk (assuming debt always pays in full)
- Using max() instead of min() for bondholders' payoff
- Forgetting to probability-weight the payoffs
- Not recognizing that in default states, bondholders receive only the firm value (not face value)

---
## Pattern: Stock-for-Stock Acquisition NPV with Growth Rate Changes

**Description:** NPV of stock acquisition = PV(Target with Synergies) - Market Value of Shares Offered. Must value target using POST-ACQUISITION growth rate and subtract cost based on acquirer's current share price.

**When to Use:** Stock-for-stock mergers with growth rate changes and specific share exchange offers (keywords: "offer X shares", "growth rate will increase", "stock exchange")

**Procedure:**
1. Formula: NPV = [D1_target / (r - g_new)] × Shares_target - (Price_acquirer × Shares_offered)
2. Calculate target's required return from current valuation
3. Value target with NEW growth rate using Gordon model
4. Calculate cost = Acquirer's share price × Shares offered
5. NPV = Target value with synergies - Cost of shares offered

**Code Example:**

**Scenario:** Target: 60,000 shares, $1.20 dividend, $18/share, 3% growth. Acquirer: $55/share, expects to grow target at 4%. Offers 22,000 acquirer shares.

**Correct Code:**
```python
# Target data
target_shares = 60000
target_dividend = 1.20
target_price = 18
target_growth_old = 0.03
target_growth_new = 0.04  # With synergies

# Acquirer data
acquirer_price = 55
shares_offered = 22000

# Target's required return (from current market price)
d1_old = target_dividend * (1 + target_growth_old)
required_return = (d1_old / target_price) + target_growth_old

# Target value with new growth rate
d1_new = target_dividend * (1 + target_growth_new)
value_per_share_new = d1_new / (required_return - target_growth_new)
total_target_value_new = value_per_share_new * target_shares

# Cost of acquisition (market value of shares offered)
cost_of_acquisition = acquirer_price * shares_offered

# NPV of acquisition
npv_acquisition = total_target_value_new - cost_of_acquisition

# Result: (1.248 / 0.0986) * 60000 - (55 * 22000) = 759,635 - 1,210,000 = -450,365
npv_acquisition
```

**Common Bugs to Avoid:**
- Using target's current value instead of value with synergies
- Valuing shares offered at target's price instead of acquirer's price
- Not updating dividend growth rate in valuation
- Confusing number of shares offered with exchange ratio

## Pattern: Ex-Dividend Date Stock Price Calculation

**Description:** Stock price "today" (cum-dividend, before ex-dividend date) includes the value of the declared dividend, while "tomorrow" (ex-dividend date) the price drops by the dividend amount. The current equity value on the balance sheet represents the cum-dividend market value.

**When to Use:** Questions asking for stock price "today" or "before ex-dividend" when a dividend has been declared but not yet paid (keywords: "ex dividend tomorrow", "declared dividend", "stock selling for today", "before ex-dividend")

**Procedure:**
1. Formula: Price_today = Total_Equity_Value / Shares_Outstanding (dividend already reflected in equity value)
2. If asked for ex-dividend price: Price_ex_dividend = Price_today - Dividend_per_share
3. Do NOT add dividend to equity value (it's already included in market value balance sheet)
4. Return the price as a float

**Code Example:**

**Scenario:** A company has total equity market value of $850,000 and 20,000 shares outstanding. It declares a $2.00 per share dividend. The stock goes ex-dividend tomorrow. What is the stock price today?

**Correct Code:**
```python
# Given data
equity_value = 850000  # Market value already includes dividend obligation
shares_outstanding = 20000
dividend_per_share = 2.00

# Today's price (cum-dividend) - equity value already reflects this
price_today = equity_value / shares_outstanding

# If asked for ex-dividend price (tomorrow):
# price_ex_dividend = price_today - dividend_per_share

price_today  # 42.50
```

**Common Bugs to Avoid:**
- Adding dividend to equity value (double-counting: equity value on market balance sheet already reflects cum-dividend price)
- Calculating ex-dividend price when asked for "today" price
- Subtracting dividend from equity value before dividing by shares
- Confusing cum-dividend (before ex-date) with ex-dividend (on/after ex-date) terminology

---

## Pattern: Cash Flow to Investors (Total Distribution)

**Description:** Cash flow to investors represents the total net cash distributed to ALL capital providers (both equity and debt holders). It equals dividends paid plus cash flow to creditors, or equivalently, dividends minus net new borrowing plus interest paid. Proceeds from financing reduce cash flow to investors.

**When to Use:** Questions asking for "cash flows to investors" or "cash flows from the firm to investors" given financing activities and distributions (keywords: "cash flows to investors", "proceeds from borrowing", "proceeds from stock", "payment of dividends")

**Procedure:**
1. Formula: Cash_Flow_to_Investors = Dividends_Paid - Net_New_Borrowing (when interest not given)
2. Or: Cash_Flow_to_Investors = Dividends_Paid + Interest_Paid - Net_New_Borrowing
3. Net new borrowing = Proceeds from debt issuance - Debt repayment
4. Proceeds from stock issuance are NOT cash flows to investors (they're cash FROM investors)
5. Return the net cash outflow to investors (can be negative if firm raised more than it paid out)

**Code Example:**

**Scenario:** A firm paid dividends of $25,000, paid interest of $8,000, issued new long-term debt for $30,000, and repaid $5,000 of existing debt. What is the cash flow to investors?

**Correct Code:**
```python
# Given data
dividends_paid = 25000
interest_paid = 8000
new_debt_issued = 30000
debt_repaid = 5000

# Calculate net new borrowing (cash FROM creditors)
net_new_borrowing = new_debt_issued - debt_repaid  # 25000

# Cash flow to creditors
cash_flow_to_creditors = interest_paid - net_new_borrowing  # 8000 - 25000 = -17000

# Total cash flow to investors
cash_flow_to_investors = dividends_paid + cash_flow_to_creditors  # 25000 - 17000 = 8000

# Alternative direct calculation:
# cash_flow_to_investors = dividends_paid + interest_paid - net_new_borrowing

cash_flow_to_investors  # 8000
```

**Common Bugs to Avoid:**
- Returning only dividends (ignoring cash flows to creditors)
- Adding proceeds from borrowing instead of subtracting (proceeds are cash FROM investors, not TO investors)
- Including proceeds from stock issuance as cash to investors (it's cash FROM equity investors)
- Confusing "to investors" (outflow from firm) with "from investors" (inflow to firm)

---

## Pattern: Gordon Growth Model for Stock Valuation with Required Return Estimation

**Description:** When valuing a stock using the Gordon Growth Model with a changed growth rate, first estimate the required return from current market conditions, then apply the new growth rate. The model is P = D₁/(r - g), where D₁ is next year's dividend, r is required return, and g is growth rate.

**When to Use:** Stock valuation questions with dividend growth rates, especially when growth rate changes or maximum price calculations are needed (keywords: "growth rate", "willing to pay", "maximum price", "constant growth", "dividend")

**Procedure:**
1. Formula: P = D₁ / (r - g), where D₁ = D₀ × (1 + g)
2. Calculate current dividend per share: Total_Dividends / Shares_Outstanding
3. If current price known, solve for required return: r = (D₁ / P₀) + g_current
4. Apply new growth rate with estimated r: P_new = D₀ × (1 + g_new) / (r - g_new)
5. Return the maximum price or valuation

**Code Example:**

**Scenario:** A company has 500,000 shares outstanding, pays total dividends of $280,000, and trades at $45 per share. Current growth rate is 3%. If an acquirer believes it can increase growth to 6%, and uses the current market's required return, what is the maximum price per share to pay?

**Correct Code:**
```python
# Given data
shares_outstanding = 500000
total_dividends = 280000
current_price = 45
current_growth_rate = 0.03
new_growth_rate = 0.06

# Calculate current dividend per share
dividend_per_share = total_dividends / shares_outstanding  # 0.56

# Estimate required return from current market conditions
# P0 = D1 / (r - g), so r = D1/P0 + g
next_dividend_current = dividend_per_share * (1 + current_growth_rate)
required_return = (next_dividend_current / current_price) + current_growth_rate

# Calculate maximum price with new growth rate
next_dividend_new = dividend_per_share * (1 + new_growth_rate)
maximum_price = next_dividend_new / (required_return - new_growth_rate)

maximum_price  # Should be higher than current price due to higher growth
```

**Common Bugs to Avoid:**
- Using current dividend D₀ instead of next dividend D₁ in the numerator
- Applying new growth rate without first estimating required return from current conditions
- Forgetting to convert growth rates to decimals (6% = 0.06)
- Using total dividends instead of per-share dividends
- Not recognizing that r must be greater than g for the model to work

---

## Pattern: Cash Flow from Assets Comprehensive Calculation

**Description:** Cash Flow from Assets (CFFA) equals Operating Cash Flow minus Net Capital Spending minus Change in Net Working Capital. It represents cash generated by assets available to all investors, requiring three distinct components to be calculated and combined.

**When to Use:** Questions asking for "cash flow from assets" or "cash flow from the firm's assets" given income statements and balance sheets (keywords: "cash flow from assets", "CFFA", "calculate cash flow from assets")

**Procedure:**
1. Formula: CFFA = OCF - NCS - Change_in_NWC
2. Calculate OCF = EBIT + Depreciation - Taxes (or Net Income + Interest + Depreciation)
3. Calculate NCS = Ending_Net_Fixed_Assets - Beginning_Net_Fixed_Assets + Depreciation
4. Calculate Change_in_NWC = (Ending_CA - Ending_CL) - (Beginning_CA - Beginning_CL), excluding cash and notes payable
5. Return CFFA (can be negative if reinvestment exceeds cash generation)

**Code Example:**

**Scenario:** A firm has EBIT of $85,000, depreciation of $22,000, taxes of $28,900. Net fixed assets increased from $340,000 to $365,000. Current assets (excluding cash) increased from $95,000 to $108,000. Current liabilities (excluding notes payable) increased from $42,000 to $48,000. Calculate cash flow from assets.

**Correct Code:**
```python
# Given data
ebit = 85000
depreciation = 22000
taxes = 28900
beginning_nfa = 340000
ending_nfa = 365000
beginning_ca_ex_cash = 95000  # Current assets excluding cash
ending_ca_ex_cash = 108000
beginning_cl_ex_notes = 42000  # Current liabilities excluding notes payable
ending_cl_ex_notes = 48000

# Step 1: Operating Cash Flow
ocf = ebit + depreciation - taxes  # 85000 + 22000 - 28900 = 78100

# Step 2: Net Capital Spending
ncs = (ending_nfa - beginning_nfa) + depreciation  # (365000 - 340000) + 22000 = 47000

# Step 3: Change in Net Working Capital
beginning_nwc = beginning_ca_ex_cash - beginning_cl_ex_notes  # 95000 - 42000 = 53000
ending_nwc = ending_ca_ex_cash - ending_cl_ex_notes  # 108000 - 48000 = 60000
change_in_nwc = ending_nwc - beginning_nwc  # 60000 - 53000 = 7000

# Cash Flow from Assets
cffa = ocf - ncs - change_in_nwc  # 78100 - 47000 - 7000 = 24100

cffa  # 24100
```

**Common Bugs to Avoid:**
- Calculating only one component (e.g., OCF) and treating it as CFFA
- Forgetting to add depreciation back in NCS calculation
- Including cash in current assets or notes payable in current liabilities for NWC
- Wrong signs: NCS and Change in NWC should be subtracted (they represent uses of cash)
- Using change in gross fixed assets instead of net fixed assets plus depreciation

---

## Pattern: External Financing Needed with Retained Earnings

**Description:** External Financing Needed (EFN) equals the increase in assets minus the increase in spontaneous liabilities minus retained earnings (additions to equity from profits). Retained earnings are an internal source of financing that reduces external financing requirements.

**When to Use:** Questions asking for "external financing needed" with pro forma projections where no dividends are paid or retention ratio is given (keywords: "external financing needed", "EFN", "no dividends", "projected sales", "proportional to sales")

**Procedure:**
1. Formula: EFN = Increase_in_Assets - Increase_in_Spontaneous_Liabilities - Retained_Earnings
2. Calculate projected assets: Assets × (Projected_Sales / Current_Sales) if proportional
3. Calculate increase in assets: Projected_Assets - Current_Assets
4. Debt typically doesn't change spontaneously (unless stated otherwise)
5. Calculate retained earnings: Projected_Net_Income × (1 - Dividend_Payout_Ratio)
6. If no dividends paid, retained earnings = full projected net income
7. Return EFN

**Code Example:**

**Scenario:** A firm has sales of $12,000, assets of $28,000, costs of $9,500, debt of $13,000, and equity of $15,000. Assets and costs are proportional to sales. Debt and equity are not. No dividends are paid. Next year's sales are projected to be $14,400. What is the external financing needed?

**Correct Code:**
```python
# Given data
current_sales = 12000
current_assets = 28000
current_costs = 9500
current_debt = 13000
current_equity = 15000
projected_sales = 14400
dividend_payout_ratio = 0  # No dividends paid

# Calculate projected values (assets and costs proportional to sales)
sales_growth_factor = projected_sales / current_sales  # 1.2
projected_assets = current_assets * sales_growth_factor  # 28000 * 1.2 = 33600
projected_costs = current_costs * sales_growth_factor  # 9500 * 1.2 = 11400

# Calculate projected net income (no taxes given, so NI = Sales - Costs)
projected_net_income = projected_sales - projected_costs  # 14400 - 11400 = 3000

# Retained earnings (internal financing)
retained_earnings = projected_net_income * (1 - dividend_payout_ratio)  # 3000 * 1 = 3000

# Increase in assets
increase_in_assets = projected_assets - current_assets  # 33600 - 28000 = 5600

# Debt doesn't change spontaneously (stated in problem)
increase_in_debt = 0

# External financing needed
efn = increase_in_assets - increase_in_debt - retained_earnings  # 5600 - 0 - 3000

efn  # 2600
```

**Common Bugs to Avoid:**
- Not subtracting retained earnings from the financing gap (treating all equity growth as external)
- Forgetting that "no dividends" means retention ratio = 100%
- Assuming debt increases proportionally when problem states it doesn't
- Including interest expense without being given interest rate information
- Calculating increase in equity as external financing (equity increases from both retained earnings and external issuance)

---

## Pattern: Merged Company Valuation with Probability-Weighted States

**Description:** When valuing a merged company with state-contingent values, calculate the probability-weighted expected value across all economic states. Merged firm value in each state equals the sum of individual firm values in that state (assuming no synergies).

**When to Use:** Merger valuation questions with multiple economic states and probabilities (keywords: "value of merged company", "states of the economy", "probability", "combined value", "after merger")

**Procedure:**
1. Formula: Merged_Value = Σ[Probability_i × (Firm1_Value_i + Firm2_Value_i)]
2. For each economic state, sum the values of both firms
3. Multiply each combined value by its probability
4. Sum across all states to get expected merged firm value
5. Do NOT subtract debt (debt is a claim on value, not a reduction when valuing the entity)

**Code Example:**

**Scenario:** Firm X and Firm Y are merging. In a boom state (probability 0.70), Firm X is worth $420,000 and Firm Y is worth $310,000. In a recession state (probability 0.30), Firm X is worth $180,000 and Firm Y is worth $120,000. What is the value of the merged company?

**Correct Code:**
```python
# Given data
states = [
    {'probability': 0.70, 'firm_x': 420000, 'firm_y': 310000},  # Boom
    {'probability': 0.30, 'firm_x': 180000, 'firm_y': 120000}   # Recession
]

# Calculate expected value of merged company
merged_value = sum(
    state['probability'] * (state['firm_x'] + state['firm_y'])
    for state in states
)

# Detailed calculation:
# Boom: 0.70 * (420000 + 310000) = 0.70 * 730000 = 511000
# Recession: 0.30 * (180000 + 120000) = 0.30 * 300000 = 90000
# Total: 511000 + 90000 = 601000

merged_value  # 601000
```

**Common Bugs to Avoid:**
- Calculating value for only one state without probability weighting
- Subtracting debt from firm values (debt is a claim, not a reduction of entity value)
- Forgetting to sum both firms' values in each state before weighting
- Using only one firm's value or averaging incorrectly
- Not recognizing that this is an expected value calculation requiring all states

---