# DETAILED SKILL PATTERNS FOR CORPORATE FINANCE (Program of Thought)

---

## Pattern: Merger Share Price with No Synergy

**Description:** When calculating post-merger share price with no synergy gains, must preserve total market value and account for share exchange ratios. The exchange ratio creates dilution effects that must be solved simultaneously: the post-merger price depends on total shares, but shares issued depend on the price at which they're valued. This requires solving the system: (1) New Shares × Post-Merger Price = Target Market Value, and (2) Post-Merger Price = Combined Market Value / (Acquirer Shares + New Shares).

**When to Use:** Questions about post-merger share prices, merger valuations, or "no synergy" scenarios involving two firms combining.

**Procedure:**
1. Calculate pre-merger market values: MV = Shares × Price per Share for both firms
2. Calculate combined market value (no synergy): Combined MV = Acquirer MV + Target MV
3. Solve for shares issued using the simultaneous equations:
   - Let x = new shares issued to target
   - Post-merger price P = Combined MV / (Acquirer Shares + x)
   - Target shareholders must receive: x × P = Target MV
   - Substituting: x × [Combined MV / (Acquirer Shares + x)] = Target MV
   - Solving: x = (Target MV × Acquirer Shares) / (Combined MV - Target MV)
4. Calculate post-merger price: Price = Combined MV / (Acquirer Shares + New Shares)
5. Verify: New shares × Post-merger price should equal Target's pre-merger market value

**Worked Example:**
**Question:** Company A has 900 shares trading at $64/share. Company B has 60 shares trading at $60/share. A acquires B in a stock-for-stock merger with no synergy. What is A's post-merger share price?

```python
# Step 1: Calculate pre-merger market values
a_shares = 900
a_price = 64
b_shares = 60
b_price = 60

a_market_value = a_shares * a_price  # 57,600
b_market_value = b_shares * b_price  # 3,600

# Step 2: Combined market value (no synergy)
combined_market_value = a_market_value + b_market_value  # 61,200

# Step 3: Solve for shares issued to B shareholders
# Using formula: x = (Target MV × Acquirer Shares) / (Combined MV - Target MV)
new_shares_issued = (b_market_value * a_shares) / (combined_market_value - b_market_value)
# = (3,600 × 900) / (61,200 - 3,600) = 3,240,000 / 57,600 = 56.25

# Step 4: Calculate total post-merger shares
total_shares_post_merger = a_shares + new_shares_issued  # 956.25

# Step 5: Post-merger share price
post_merger_price = combined_market_value / total_shares_post_merger
# = 61,200 / 956.25 = 64.0

# Step 6: Verify B shareholders receive fair value
b_shareholder_value = new_shares_issued * post_merger_price  # Should equal 3,600
verification = abs(b_shareholder_value - b_market_value) < 0.01

post_merger_price  # 64.0
```

**Common Bugs to Avoid:**
- Using a fixed exchange ratio without solving for dilution effects (leads to circular dependency)
- Calculating new shares as Target MV / Acquirer Pre-Merger Price (ignores dilution)
- Not recognizing that post-merger price may differ from acquirer's pre-merger price when target is material
- Forgetting to verify that target shareholders receive value equal to their pre-merger market value

**CHECK Steps:**
- Verify: (New shares issued × Post-merger price) should equal Target's pre-merger market value
- Assert: Post-merger price equals acquirer's pre-merger price ONLY when target is very small OR when the formula naturally produces this result
- If target is material (>5% of combined value), expect post-merger price to differ from acquirer's pre-merger price
- Total market value should equal sum of pre-merger market values (no synergy assumption)

---
## Pattern: Deriving Required Return from P/E Ratio in Dividend Discount Model

**Description:** P/E ratio is NOT the inverse of required return. In a constant growth DDM, the relationship is P/E = (payout ratio × (1+g))/(r-g), requiring algebraic manipulation to extract r.

**When to Use:** Questions requiring calculation of required return from P/E ratio, especially in acquisition NPV or valuation contexts with growth rates.

**Procedure:**
1. Formula: r = (D₁/P₀) + g, where D₁ = next year's dividend, P₀ = current price
2. Alternative: From P/E = (payout × (1+g))/(r-g), solve for r
3. Calculate payout ratio: payout = Dividends / Earnings
4. Calculate EPS: EPS = Earnings / Shares
5. Calculate Price: Price = P/E × EPS
6. Calculate D₁: D₁ = (Dividends / Shares) × (1 + g)
7. Solve for r: r = (D₁ / Price) + g

**Code Example:**

**Scenario:** A firm has P/E = 15, earnings = $600,000, shares = 100,000, dividends = $240,000, and expected growth = 5%. Find required return.

**Correct Code:**
```python
# Given values
pe_ratio = 15
earnings = 600000
shares_outstanding = 100000
dividends = 240000
growth_rate = 0.05

# Calculate per-share values
eps = earnings / shares_outstanding  # 6.0
dividend_per_share = dividends / shares_outstanding  # 2.4
price_per_share = pe_ratio * eps  # 90.0

# Calculate next year's dividend
d1 = dividend_per_share * (1 + growth_rate)  # 2.52

# Required return using dividend discount model
required_return = (d1 / price_per_share) + growth_rate

required_return  # 0.078 or 7.8%
```

**Common Bugs to Avoid:**
- Using r = 1/P/E (fundamentally wrong relationship)
- Forgetting to grow dividend to next period (D₁, not D₀)
- Using acquirer's P/E to value target (should use target's own metrics)
- Ignoring growth rate in the calculation

---

## Pattern: Acquisition NPV with Synergy and Share Exchange

**Description:** Acquisition NPV = (Target Value with Synergy) - (Cost of Acquisition). When paying with shares, cost = (shares issued) × (acquirer's price), and target value must reflect incremental cash flows at appropriate discount rate.

**When to Use:** Questions about acquisition NPV, merger value creation, or "what synergy is needed" scenarios.

**Procedure:**
1. Formula: NPV = PV(Target with Synergy) - Cost
2. Calculate target's standalone value using its own required return
3. Calculate synergy value (PV of incremental cash flows)
4. Calculate total target value: Standalone + Synergy
5. Calculate cost: If cash, use cash amount; if shares, use (shares issued × acquirer price)
6. Compute NPV: Total Target Value - Cost

**Code Example:**

**Scenario:** Target has earnings of $400,000, growth of 4%, dividends of $200,000. Acquirer believes growth will increase to 6% (synergy). Acquirer offers 50,000 shares worth $45 each. Target's required return is 10%. Find NPV.

**Correct Code:**
```python
# Target standalone metrics
target_dividends = 200000
standalone_growth = 0.04
target_required_return = 0.10

# With synergy
synergy_growth = 0.06

# Acquirer offer
shares_offered = 50000
acquirer_price = 45

# Target standalone value (perpetuity with growth)
d1_standalone = target_dividends * (1 + standalone_growth)
target_standalone_value = d1_standalone / (target_required_return - standalone_growth)

# Target value with synergy
d1_with_synergy = target_dividends * (1 + synergy_growth)
target_value_with_synergy = d1_with_synergy / (target_required_return - synergy_growth)

# Cost of acquisition
cost = shares_offered * acquirer_price

# NPV
npv = target_value_with_synergy - cost

npv  # 530,000 - 2,250,000 = -1,720,000 (negative, bad deal)
```

**Common Bugs to Avoid:**
- Confusing premium paid with synergy value (premium is what you pay above market, synergy is value created)
- Using wrong discount rate (should use target's required return, not acquirer's)
- Forgetting to account for share dilution effects
- Not distinguishing between standalone value and value with synergy

---

## Pattern: Risky Debt Valuation with State-Contingent Payoffs

**Description:** Risky debt value equals the expected present value of what bondholders actually receive, which is min(Firm Value, Face Value) in each state, not simply the face value.

**When to Use:** Questions about debt value in merger scenarios, bankruptcy analysis, or state-contingent firm valuations.

**Procedure:**
1. Formula: Debt Value = Σ [Probability(state) × min(Firm Value(state), Face Value)]
2. Identify all economic states and their probabilities
3. Determine firm value in each state
4. Calculate bondholder payoff in each state: min(Firm Value, Debt Face Value)
5. Compute expected value: probability-weighted sum of payoffs
6. This is the market value of debt (may differ from face value)

**Code Example:**

**Scenario:** A firm has debt with face value $100,000. In boom (prob=0.6), firm value is $180,000. In recession (prob=0.4), firm value is $75,000. What is debt value?

**Correct Code:**
```python
# Debt characteristics
debt_face_value = 100000

# State 1: Boom
prob_boom = 0.6
firm_value_boom = 180000

# State 2: Recession
prob_recession = 0.4
firm_value_recession = 75000

# Bondholder payoffs (limited by firm value in default)
debt_payoff_boom = min(firm_value_boom, debt_face_value)  # 100,000
debt_payoff_recession = min(firm_value_recession, debt_face_value)  # 75,000

# Expected value of debt
debt_value = (prob_boom * debt_payoff_boom) + (prob_recession * debt_payoff_recession)

debt_value  # 90,000 (less than face value due to default risk)
```

**Common Bugs to Avoid:**
- Using face value as debt value without considering default risk
- Allowing negative equity values (equity = max(0, Firm Value - Debt))
- Forgetting that debt holders have priority in bankruptcy
- Not accounting for state probabilities in expected value calculation

---

## Pattern: Limited Liability and Equity as a Call Option

**Description:** Equity value cannot be negative due to limited liability. In any state of the world, equity value = max(0, Firm Value - Debt Face Value). When firm value is less than debt obligations, equity holders receive zero (not a negative amount), and debt holders absorb the loss.

**When to Use:** Questions about equity value in leveraged firms, merger scenarios with debt, bankruptcy analysis, or state-contingent valuations where firm value may fall below debt.

**Procedure:**
1. Formula: Equity Value = max(0, Firm Value - Debt Face Value)
2. For each possible state, calculate firm value
3. For each state, calculate equity value using the max function
4. Never allow equity value to be negative
5. When firm value < debt, equity = 0 and debt holders receive only the firm value

**Code Example:**

**Scenario:** A merged firm has total debt of $800,000. In a bad state, firm value is $600,000. In a good state, firm value is $1,200,000.

**Correct Code:**
```python
# Given values
total_debt = 800000
firm_value_bad_state = 600000
firm_value_good_state = 1200000

# Calculate equity value in each state
# Equity = max(0, Firm Value - Debt)
equity_value_bad_state = max(0, firm_value_bad_state - total_debt)
equity_value_good_state = max(0, firm_value_good_state - total_debt)

# Calculate debt value in each state
# Debt receives min(Firm Value, Debt Face Value)
debt_value_bad_state = min(firm_value_bad_state, total_debt)
debt_value_good_state = min(firm_value_good_state, total_debt)

# Return equity values
(equity_value_bad_state, equity_value_good_state)
```

**Common Bugs to Avoid:**
- Allowing equity value to be negative (violates limited liability)
- Calculating equity as Firm Value - Debt without the max(0, ...) wrapper
- Forgetting that when equity is zero, debt holders only receive the firm value (not full face value)
- Confusing book value of equity with market value in distress scenarios

---
## Pattern: Geometric Mean for Multi-Period Returns

**Description:** For calculating average investment returns over multiple periods, use geometric mean (compound growth rate), not arithmetic mean, to account for compounding effects.

**When to Use:** Questions asking for "average return" over multiple years, especially with volatile returns or when calculating compound growth rates.

**Procedure:**
1. Formula: Geometric Mean = [(1+r₁) × (1+r₂) × ... × (1+rₙ)]^(1/n) - 1
2. Convert percentage returns to decimal form
3. Add 1 to each return to get growth factors
4. Multiply all growth factors together
5. Take the nth root (where n = number of periods)
6. Subtract 1 and convert back to percentage

**Code Example:**

**Scenario:** An investment has returns of 15%, -10%, 25%, 8% over four years. Calculate average return.

**Correct Code:**
```python
# Returns over 4 years (as decimals)
returns = [0.15, -0.10, 0.25, 0.08]

# Convert to growth factors (1 + return)
growth_factors = [1 + r for r in returns]

# Calculate product of all growth factors
product = 1
for factor in growth_factors:
    product *= factor

# Number of periods
n = len(returns)

# Geometric mean
geometric_mean = product ** (1/n) - 1

geometric_mean  # 0.0876 or 8.76%
```

**Alternative using numpy:**
```python
import numpy as np

returns = [0.15, -0.10, 0.25, 0.08]
growth_factors = [1 + r for r in returns]
geometric_mean = np.prod(growth_factors) ** (1/len(returns)) - 1

geometric_mean  # 0.0876
```

**Common Bugs to Avoid:**
- Using arithmetic mean (sum/n) for multi-period returns
- Forgetting to convert returns to growth factors (1 + r)
- Not subtracting 1 at the end
- Using arithmetic mean when returns are volatile (overstates true average)

---

## Pattern: Stock Dividend Accounting Mechanics

**Description:** Stock dividends transfer value from retained earnings to equity accounts. The amount transferred = (shares issued) × (market price), with par value going to common stock and the remainder to capital surplus. When asked for "new common stock," this typically refers to the TOTAL common stock account balance after the dividend, not just the incremental addition.

**When to Use:** Questions about stock dividend effects on equity accounts, changes in common stock account balance, or capital surplus calculations.

**Procedure:**
1. Calculate current shares outstanding: Common Stock Account / Par Value per Share
2. Calculate new shares issued: Outstanding Shares × Dividend Percentage
3. Calculate total value transferred from RE: New Shares × Market Price
4. Calculate addition to common stock account: New Shares × Par Value
5. Calculate new total common stock account: Old Common Stock + Addition
6. Calculate addition to capital surplus: Total Transfer - Addition to Common Stock
7. Note: "New common stock" or "value of new common stock" = NEW TOTAL common stock account balance

**Worked Example:**
**Question:** A firm has common stock account of $150,000 (par value $2/share), market price $35/share, and declares a 15% stock dividend. What is the value of the common stock account after the dividend?

```python
# Step 1: Current equity structure
common_stock_account_old = 150000
par_value_per_share = 2
market_price_per_share = 35
stock_dividend_percentage = 0.15

# Step 2: Calculate current shares outstanding
shares_outstanding = common_stock_account_old / par_value_per_share  # 75,000

# Step 3: New shares issued
new_shares_issued = shares_outstanding * stock_dividend_percentage  # 11,250

# Step 4: Total value transferred from retained earnings
total_transfer = new_shares_issued * market_price_per_share  # 393,750

# Step 5: Addition to common stock account (at par value)
addition_to_common_stock = new_shares_issued * par_value_per_share  # 22,500

# Step 6: NEW TOTAL common stock account balance
common_stock_account_new = common_stock_account_old + addition_to_common_stock  # 172,500

# Step 7: Addition to capital surplus (market value - par value)
addition_to_capital_surplus = total_transfer - addition_to_common_stock  # 371,250

# The answer to "What is the value of new common stock?" is the NEW TOTAL account balance
common_stock_account_new  # 172,500
```

**Common Bugs to Avoid:**
- Returning only the incremental addition (new shares × par) instead of total account balance
- Using market value as the "common stock" value (should use par value for the account)
- Confusing "new common stock" (total account) with "addition to common stock" (increment)
- Forgetting that total owners' equity remains unchanged (just reclassified between accounts)

**CHECK Steps:**
- Verify: Total equity (Common Stock + Capital Surplus + RE) remains constant
- If question asks for "new common stock" or "value of new common stock," return the TOTAL account balance
- If question asks for "addition to common stock," return only the increment
- Assert: Addition to common stock = New shares × Par value

---
## Pattern: Blocked Funds and Reinvestment in International Capital Budgeting

**Description:** When cash flows are "blocked and reinvested for one year," each cash flow is delayed by exactly one period and grows at the reinvestment rate for that single period only, not compounded until project end. This pattern applies when the question explicitly asks for NPV or cash flows UNDER THE BLOCKED FUNDS SCENARIO, not when blocked funds are merely mentioned as context.

**When to Use:** 
- Questions explicitly asking for "NPV with blocked funds," "adjusted cash flows," or "IRR considering blocked funds reinvestment"
- Problems where the blocking mechanism is the PRIMARY focus of the calculation
- Scenarios asking "what is the effect of blocked funds on project value"

**When NOT to Use:** 
- When blocked funds are mentioned in context but the question asks for "the IRR of the project" or "project NPV" without specifying to adjust for blocking
- When the question asks for standard project evaluation metrics and blocked funds are descriptive background
- When cash flows are already provided in adjusted form
- When the problem asks to compare blocked vs. unblocked scenarios (calculate both, don't assume adjustment)

**Procedure:**
1. **Verify adjustment is required**: Check if question explicitly asks for blocked funds adjustment or if it's just contextual information
2. Formula: Adjusted CF(t) = Original CF(t-1) × (1 + reinvestment rate), received at time t
3. Identify which cash flows are blocked (typically all except initial investment)
4. Shift each blocked cash flow forward by one period
5. Multiply each shifted cash flow by (1 + reinvestment rate) for the one-year delay
6. Create new cash flow timeline with adjusted amounts and timing
7. Calculate NPV or IRR using the adjusted cash flows

**Worked Example:**
**Question:** A project in Country X has cash flows: Year 0: -$200,000, Year 1: $80,000, Year 2: $100,000. The government requires all positive cash flows be reinvested for one year at 3%. Calculate the NPV of the project under these blocked funds conditions using a 12% discount rate.

```python
import numpy_financial as npf

# Original cash flows
cf_0 = -200000  # Not blocked (initial investment)
cf_1 = 80000    # Blocked
cf_2 = 100000   # Blocked

reinvestment_rate = 0.03
discount_rate = 0.12

# Adjusted cash flows (blocked flows delayed by 1 year, earn reinvestment rate)
adjusted_cf_0 = cf_0  # -200,000 (not affected)
adjusted_cf_1 = 0     # Original year 1 flow is blocked
adjusted_cf_2 = cf_1 * (1 + reinvestment_rate)  # 82,400 (year 1 flow received in year 2)
adjusted_cf_3 = cf_2 * (1 + reinvestment_rate)  # 103,000 (year 2 flow received in year 3)

# Calculate NPV on adjusted flows
adjusted_cash_flows = [adjusted_cf_0, adjusted_cf_1, adjusted_cf_2, adjusted_cf_3]
npv_blocked = npf.npv(discount_rate, adjusted_cash_flows)

npv_blocked  # Calculate NPV with blocked funds adjustment
```

**Common Bugs to Avoid:**
- Applying blocked funds adjustment when question asks for standard "project IRR" without specifying adjustment
- Compounding each cash flow from original period to project end (wrong interpretation)
- Not shifting cash flows forward by exactly one period
- Applying reinvestment rate multiple times to the same cash flow
- Forgetting that initial investment is typically not blocked
- **Adjusting cash flows when blocked funds are merely contextual information, not the calculation focus**

**CHECK Steps:**
- **CRITICAL**: Verify question explicitly asks for blocked funds adjustment (keywords: "considering blocked funds," "with reinvestment requirement," "adjusted for blocking")
- If question asks for "the IRR" or "the NPV" without mentioning adjustment, use ORIGINAL cash flows
- If blocked funds are mentioned but question doesn't specify adjustment, calculate standard metrics first
- Only apply adjustment if problem explicitly requires it or asks to compare scenarios
- Assert: Each positive cash flow is delayed by exactly 1 period and grows by (1 + reinvestment_rate)

---

These refinements preserve all Q⁺ patterns while adding safeguards against the Q⁻ failure modes. The key changes are:

1. **Working Capital pattern**: Clarified that initial NWC is separate from percentage-based additions, preventing double-counting
2. **Blocked Funds pattern**: Added strict "When NOT to Use" conditions to prevent over-application when blocked funds are contextual rather than requiring adjustment
## Pattern: Credit Policy NPV as Perpetuity Valuation

**Description:** Changes in credit policy create perpetual changes in monthly cash flows. When switching from cash to credit sales, there are TWO effects: (1) incremental profit from volume increase, and (2) opportunity cost from delaying payment on existing sales. NPV = (PV of Net Monthly Benefit) - (Incremental AR Investment), where AR investment represents ALL receivables at cost (both existing and new sales volumes).

**When to Use:** Questions about credit policy changes, net 30 terms, evaluating switch from cash to credit sales, or comparing different credit term scenarios.

**Procedure:**
1. Calculate monthly contribution under OLD policy: (Price - Cost) × Units
2. Calculate monthly contribution under NEW policy: (Price - Cost) × Units
3. Calculate GROSS change in monthly contribution: New Contribution - Old Contribution
4. Calculate opportunity cost on existing sales (if switching from cash to credit):
   - Opportunity Cost = Old Monthly Contribution × (Credit Period in Months) × Monthly Required Return
5. Calculate NET monthly benefit: Gross Change - Opportunity Cost
6. Calculate TOTAL receivables investment under new policy:
   - AR = (New Monthly Sales in Dollars) × (Credit Period in Months) × (Cost/Price ratio)
   - For net 30 terms: Credit Period = 1 month
7. Calculate incremental AR investment: New AR - Old AR (Old AR = 0 if currently cash sales)
8. Calculate PV of perpetual net benefit: Net Monthly Benefit / Monthly Required Return
9. NPV = PV of perpetual benefit - Incremental AR investment

**Worked Example:**
**Question:** A firm currently sells 800 units/month at $50 (cost $30) for cash. A new policy offers net 30 terms, expecting to sell 900 units/month at $52 (cost $32). Required return is 1.2% per month. Find NPV.

```python
# Step 1: Current policy (cash sales)
current_price = 50
current_cost = 30
current_units = 800
current_monthly_contribution = (current_price - current_cost) * current_units  # 16,000

# Step 2: New policy (net 30)
new_price = 52
new_cost = 32
new_units = 900
new_monthly_contribution = (new_price - new_cost) * new_units  # 18,000

# Step 3: Gross change in monthly contribution
gross_change = new_monthly_contribution - current_monthly_contribution  # 2,000

# Step 4: Opportunity cost on existing sales (delayed by 1 month)
# When switching from cash to credit, existing sales now take 1 month to collect
credit_period_months = 1
monthly_required_return = 0.012
opportunity_cost = current_monthly_contribution * credit_period_months * monthly_required_return
# = 16,000 × 1 × 0.012 = 192

# Step 5: Net monthly benefit
net_monthly_benefit = gross_change - opportunity_cost  # 2,000 - 192 = 1,808

# Step 6: Total AR investment under new policy (at cost)
new_monthly_sales_dollars = new_price * new_units  # 46,800
new_ar_investment = new_monthly_sales_dollars * credit_period_months * (new_cost / new_price)
# = 46,800 × 1 × (32/52) = 28,800

# Step 7: Incremental AR investment (from zero under cash sales)
current_ar_investment = 0
incremental_ar_investment = new_ar_investment - current_ar_investment  # 28,800

# Step 8: PV of perpetual net benefit
pv_perpetual_benefit = net_monthly_benefit / monthly_required_return
# = 1,808 / 0.012 = 150,666.67

# Step 9: NPV
npv = pv_perpetual_benefit - incremental_ar_investment
# = 150,666.67 - 28,800 = 121,866.67

npv  # 121,866.67
```

**Common Bugs to Avoid:**
- Ignoring opportunity cost when switching from cash to credit (only counting volume increase)
- Using total new AR instead of incremental AR when firm already has receivables
- Treating monthly benefit as one-time gain instead of perpetuity
- Using sales value instead of cost basis for AR investment
- Not recognizing that delaying payment on existing sales has an opportunity cost

**CHECK Steps:**
- If switching from cash to credit, must include opportunity cost = (Old contribution × Credit period × Required return)
- AR investment = (Monthly sales in $) × (Credit period in months) × (Cost/Price)
- For net 30 terms, credit period = 1 month
- Verify: Net monthly benefit = Gross change - Opportunity cost (if applicable)
- If both policies involve credit, only the CHANGE in AR is relevant (no opportunity cost on existing AR)

---
## Pattern: New Equity Issuance and Dilution Effects on NPV

**Description:** When a firm issues new equity to fund an investment, the number of shares outstanding increases by (Investment Amount / Current Stock Price). Book value per share after the transaction equals Total Equity (including new investment) divided by Total Shares (including new shares issued), not the original share count.

**When to Use:** Questions about book value per share after equity issuance, dilution analysis, or scenarios involving "financed with a new equity issue."

**Procedure:**
1. Formula: New Shares Issued = Investment Amount / Current Stock Price
2. Calculate current book value (total equity) = Total Assets - Total Liabilities
3. Calculate new total equity = Current Equity + Investment Amount
4. Calculate new total shares = Current Shares + New Shares Issued
5. New book value per share = New Total Equity / New Total Shares

**Code Example:**

**Scenario:** A firm with 100,000 shares outstanding, stock price of $50, total assets of $8,000,000, and total liabilities of $3,000,000 issues new equity to finance a $2,000,000 investment.

**Correct Code:**
```python
# Given values
current_shares = 100000
stock_price = 50
total_assets = 8000000
total_liabilities = 3000000
investment_amount = 2000000

# Step 1: Calculate current book value (equity)
current_equity = total_assets - total_liabilities

# Step 2: Calculate new shares issued
new_shares_issued = investment_amount / stock_price

# Step 3: Calculate new total shares
new_total_shares = current_shares + new_shares_issued

# Step 4: Calculate new total equity (book value)
new_total_equity = current_equity + investment_amount

# Step 5: Calculate new book value per share
new_book_value_per_share = new_total_equity / new_total_shares

new_book_value_per_share
```

**Common Bugs to Avoid:**
- Forgetting to increase share count when equity is issued (treating it like retained earnings)
- Dividing new equity by old share count instead of new share count
- Confusing market value per share with book value per share
- Not recognizing that "financed with new equity issue" means issuing shares at current market price

---
## Pattern: Synergy Value vs. Acquisition Premium in M&A

**Description:** Synergy value is the incremental value created by combining firms (PV of cost savings, revenue enhancements). Acquisition premium is what the acquirer pays above target's standalone market value. For a value-creating deal, synergy must exceed premium. The NPV to the acquirer = Synergy Value - Premium Paid.

**When to Use:** Questions about "what synergy must exist," merger justification, NPV of acquisition, or reconciling acquisition decisions with premiums paid.

**Procedure:**
1. Calculate target's standalone market value: Shares × Price (or using DDM/P/E)
2. Calculate target's value WITH synergy: Use improved growth rate or cost savings in valuation model
3. Calculate synergy value: Target with Synergy - Target Standalone
4. Calculate acquisition cost (cash paid or shares issued × acquirer price)
5. Calculate premium: Cost - Target Standalone Value
6. Calculate NPV to acquirer: Synergy Value - Premium
7. For NPV = 0 (break-even), Synergy Value = Premium (minimum synergy needed)

**Worked Example:**
**Question:** Target has market value of $2,000,000 (current growth 3%). Acquirer believes synergy will increase growth to 6%, valuing target at $2,400,000 with synergy. Acquirer offers $2,200,000 cash. What is the NPV and minimum synergy needed?

```python
# Step 1: Target standalone value
target_standalone_value = 2000000

# Step 2: Target value with synergy (calculated using improved growth)
target_value_with_synergy = 2400000

# Step 3: Synergy value created
synergy_value = target_value_with_synergy - target_standalone_value  # 400,000

# Step 4: Acquisition cost
acquisition_cost = 2200000

# Step 5: Premium paid above standalone value
premium = acquisition_cost - target_standalone_value  # 200,000

# Step 6: NPV to acquirer
npv_to_acquirer = synergy_value - premium  # 200,000

# Step 7: Minimum synergy needed (for NPV = 0)
minimum_synergy_needed = premium  # 200,000

# Interpretation: Deal creates value because synergy (400k) > premium (200k)
npv_to_acquirer  # 200,000
```

**Common Bugs to Avoid:**
- Confusing premium with synergy (premium is what you pay extra, synergy is value created)
- Thinking premium equals synergy (synergy must EXCEED premium for value creation)
- Calculating NPV as synergy value alone (must subtract premium/cost)
- Not recognizing that market value of combined firm reflects EXPECTED synergies

**CHECK Steps:**
- Verify: If NPV > 0, then Synergy > Premium (value-creating deal)
- If NPV = 0, then Synergy = Premium (break-even, minimum synergy needed)
- If NPV < 0, then Synergy < Premium (value-destroying deal)
- Assert: Synergy Value = (Target with improvements) - (Target standalone)
## Pattern: Merger Exchange Ratio and Post-Merger Ownership

**Description:** In stock-for-stock mergers, the exchange ratio determines how many acquirer shares target shareholders receive. This ratio is based on relative market values, and post-merger ownership fractions determine value distribution.

**When to Use:** Questions about share exchange ratios, post-merger ownership percentages, or value distribution in stock mergers.

**Procedure:**
1. Formula: Exchange Ratio = (Target Price / Acquirer Price) or (Target Value / Acquirer Price per Share)
2. Calculate each firm's market value: Shares × Price
3. Determine exchange ratio from offer terms or relative values
4. Calculate new shares issued: Target Shares × Exchange Ratio
5. Calculate total post-merger shares: Acquirer Shares + New Shares Issued
6. Calculate ownership fractions: Old Acquirer % = Acquirer Shares / Total Shares
7. Verify value distribution matches ownership fractions

**Code Example:**

**Scenario:** Acquirer has 200,000 shares at $30. Target has 50,000 shares at $18. Acquirer offers 1 share for every 2 target shares. What are post-merger ownership percentages?

**Correct Code:**
```python
# Acquirer characteristics
acquirer_shares = 200000
acquirer_price = 30

# Target characteristics
target_shares = 50000
target_price = 18

# Exchange ratio (given in offer)
exchange_ratio = 1 / 2  # 1 acquirer share for 2 target shares

# Alternative: calculate from relative prices
implied_exchange_ratio = target_price / acquirer_price  # 0.6 (market-based)

# New shares issued to target shareholders
new_shares_issued = target_shares * exchange_ratio  # 25,000

# Total shares post-merger
total_shares_post_merger = acquirer_shares + new_shares_issued  # 225,000

# Ownership percentages
acquirer_ownership_pct = acquirer_shares / total_shares_post_merger  # 0.8889 or 88.89%
target_ownership_pct = new_shares_issued / total_shares_post_merger  # 0.1111 or 11.11%

# Verify: does target get fair value?
acquirer_market_value = acquirer_shares * acquirer_price  # 6,000,000
target_market_value = target_shares * target_price  # 900,000
combined_value = acquirer_market_value + target_market_value  # 6,900,000

target_receives = new_shares_issued * acquirer_price  # 750,000
# Target gets $750k but worth $900k - unfavorable deal for target

target_ownership_pct  # 0.1111
```

**Common Bugs to Avoid:**
- Confusing exchange ratio with ownership percentage
- Not checking if exchange ratio is fair based on relative market values
- Forgetting to add new shares to calculate total post-merger shares
- Assuming equal ownership without considering relative firm sizes

---

## Pattern: Combined Firm Value in Independent State-Contingent Scenarios

**Description:** When two firms merge and face independent state-contingent outcomes, the combined firm's value in each scenario is the sum of individual firm values in their respective states. For MERGED ENTITY equity valuation, apply limited liability AFTER combining firm values and total debt: Merged Equity = max(0, Combined Firm Value - Total Debt Face Value). Do NOT sum individual equity values calculated separately.

**When to Use:** Questions about merger values with independent economic states, "merged entity stock value," "combined firm equity value," or equity valuation in specific state combinations after merger.

**When NOT to Use:** When calculating individual firm equity values before merger, or when debt should be evaluated separately for each firm (e.g., when firms remain legally separate entities).

**Procedure:**
1. Formula: Combined Firm Value(state_A, state_B) = Firm_A_Value(state_A) + Firm_B_Value(state_B)
2. Identify all possible states for each firm and their probabilities
3. Create outcome matrix: all combinations of states
4. Calculate combined firm value for each combination
5. **For merged entity equity**: Calculate total debt face value = Debt_A + Debt_B
6. **Apply limited liability at merged entity level**: Equity = max(0, Combined Firm Value - Total Debt Face Value)
7. Calculate joint probability: P(state_A) × P(state_B) if independent
8. Calculate expected combined value: Σ [Joint Probability × Combined Value]

**Worked Example:**
**Question:** Firm X has boom (0.7, $500k) or recession (0.3, $250k) with debt of $200k. Firm Y has boom (0.6, $400k) or recession (0.4, $180k) with debt of $150k. States are independent. What is merged equity value in X-boom, Y-recession?

```python
# Firm X states and debt
prob_x_boom = 0.7
value_x_boom = 500000
prob_x_recession = 0.3
value_x_recession = 250000
debt_x = 200000

# Firm Y states and debt
prob_y_boom = 0.6
value_y_boom = 400000
prob_y_recession = 0.4
value_y_recession = 180000
debt_y = 150000

# Specific scenario: X-boom, Y-recession
combined_firm_value = value_x_boom + value_y_recession  # 680,000

# Total debt of merged entity
total_debt_face_value = debt_x + debt_y  # 350,000

# Equity value of merged entity (limited liability applied to combined entity)
merged_equity_value = max(0, combined_firm_value - total_debt_face_value)
# = max(0, 680,000 - 350,000) = 330,000

# WRONG approach (for comparison): summing individual equity values
# x_equity_boom = max(0, 500000 - 200000) = 300,000
# y_equity_recession = max(0, 180000 - 150000) = 30,000
# sum_individual = 330,000 (happens to match in this case, but conceptually wrong)

merged_equity_value  # 330,000
```

**Common Bugs to Avoid:**
- Calculating individual firm equity values separately then summing (conceptually wrong for merged entity)
- Applying limited liability at individual firm level before merger instead of at merged entity level
- Using individual debt payoffs min(Firm Value, Debt) instead of total debt face value for merged entity
- Confusing "merged entity stock value" with "sum of individual equity values before merger"

**CHECK Steps:**
- If question asks for "merged entity stock value" or "combined firm equity," apply limited liability AFTER combining firm values and total debt
- Verify: Merged Equity = max(0, Combined Firm Value - Total Debt Face Value), NOT sum of individual equity values
- For merged entity, debt holders have claim on combined assets, equity holders get the residual
- If calculating expected value across all states, ensure joint probabilities sum to 1.0

---
## Pattern: Cash Flow from Assets Formula Structure

**Description:** Cash Flow from Assets (CFA) must be calculated using the correct formula: CFA = Operating Cash Flow - Net Capital Spending - Change in Net Working Capital, where OCF = EBIT + Depreciation - Taxes. When actual taxes from the income statement are provided, use those actual taxes rather than calculating taxes as EBIT × tax rate. The EBIT(1-T) + Depreciation formula is algebraically equivalent but can lead to errors when tax rates are approximate or when actual taxes differ from EBIT × statutory rate.

**When to Use:** Questions asking for "cash flow from assets," "cash flow to the firm," or requiring calculation of total cash generated by firm operations independent of financing structure.

**Procedure:**
1. Formula: CFA = OCF - NCS - ΔNWC
2. Calculate Operating Cash Flow:
   - If actual taxes from income statement are provided: OCF = EBIT + Depreciation - Actual Taxes
   - If only tax rate is given: OCF = EBIT(1 - Tax Rate) + Depreciation
3. Calculate Net Capital Spending = Ending NFA - Beginning NFA + Depreciation
4. Calculate Change in Net Working Capital = (Ending CA - Ending CL) - (Beginning CA - Beginning CL)
5. Combine: CFA = OCF - NCS - ΔNWC

**Worked Example:**
**Question:** A firm has EBIT of $4,500, depreciation of $1,000, actual taxes paid of $1,350 (from income statement), net fixed assets increased from $35,000 to $36,200, current assets increased from $18,000 to $19,500, and current liabilities increased from $7,000 to $7,800.

```python
# Given values
ebit = 4500
depreciation = 1000
actual_taxes = 1350  # From income statement
nfa_beginning = 35000
nfa_ending = 36200
current_assets_beginning = 18000
current_assets_ending = 19500
current_liabilities_beginning = 7000
current_liabilities_ending = 7800

# Step 1: Calculate Operating Cash Flow (OCF)
# Use actual taxes from income statement
ocf = ebit + depreciation - actual_taxes
# = 4500 + 1000 - 1350 = 4150

# Step 2: Calculate Net Capital Spending (NCS)
# NCS = Ending NFA - Beginning NFA + Depreciation
ncs = nfa_ending - nfa_beginning + depreciation
# = 36200 - 35000 + 1000 = 2200

# Step 3: Calculate Change in Net Working Capital (ΔNWC)
nwc_beginning = current_assets_beginning - current_liabilities_beginning
nwc_ending = current_assets_ending - current_liabilities_ending
change_in_nwc = nwc_ending - nwc_beginning
# = (19500 - 7800) - (18000 - 7000) = 11700 - 11000 = 700

# Step 4: Calculate Cash Flow from Assets
cash_flow_from_assets = ocf - ncs - change_in_nwc
# = 4150 - 2200 - 700 = 1250

cash_flow_from_assets  # 1250
```

**Common Bugs to Avoid:**
- Starting from Net Income instead of EBIT (Net Income already includes interest, which should be excluded)
- Using EBIT × tax_rate when actual taxes from income statement are provided (can differ due to tax credits, NOLs, etc.)
- Forgetting to add back depreciation when calculating Net Capital Spending
- Calculating change in working capital as (ΔCA - ΔCL) instead of Δ(CA - CL)
- Using wrong sign conventions (NCS and ΔNWC should be subtracted from OCF)

**CHECK Steps:**
- If income statement provides actual taxes paid, use those instead of EBIT × tax_rate
- Verify: OCF = EBIT + Depreciation - Taxes (using actual taxes if available)
- Alternative formula OCF = EBIT(1-T) + Depreciation is equivalent only when Taxes = EBIT × T exactly
- Assert: NCS = Ending NFA - Beginning NFA + Depreciation (depreciation must be added back)

---
## Pattern: Target Required Return from Current Market Valuation

**Description:** To value an acquisition target with changed assumptions (e.g., different growth rate), first derive the target's required return from its current market price using the Gordon Growth Model in reverse: r = (D1/P0) + g_current. Then use this SAME r to revalue the target with new growth assumptions. The target's required return reflects its risk profile and is independent of who acquires it. Do NOT use the acquirer's cost of equity, P/E ratio, or earnings yield.

**When to Use:** Acquisition valuation questions where growth rate assumptions change, scenarios asking "what if growth rate is X instead of Y," revaluing a target under different scenarios, or "what is the value of the target to the acquirer."

**Procedure:**
1. Calculate target's current market value per share = P/E ratio × EPS (or Shares × Price if given)
2. Calculate target's dividend per share = Total Dividends / Shares Outstanding
3. Derive target's required return using Gordon Growth Model:
   - r = [Dividend per share × (1 + current_growth)] / Current Price + current_growth
   - This r reflects the target's risk and is used for ALL valuations of this target
4. Revalue with new growth assumption:
   - New Value per Share = [Dividend per share × (1 + new_growth)] / (r - new_growth)
5. Calculate total new value = New Value per Share × Target Shares

**Worked Example:**
**Question:** Target firm has 400,000 shares, earnings of $500,000, dividends of $250,000, P/E ratio of 10, current expected growth of 4%. Acquirer believes growth will be 6% due to synergies. What is the value of the target to the acquirer?

```python
# Given values
target_shares = 400000
target_earnings = 500000
target_dividends = 250000
target_pe_ratio = 10
current_growth = 0.04
new_growth = 0.06

# Step 1: Calculate target's current market metrics
target_eps = target_earnings / target_shares  # 1.25
target_current_price = target_pe_ratio * target_eps  # 12.50
target_dividend_per_share = target_dividends / target_shares  # 0.625

# Step 2: Derive target's required return from current valuation
# Using Gordon Growth Model: P0 = D1 / (r - g)
# Rearranging: r = D1/P0 + g
d1_current = target_dividend_per_share * (1 + current_growth)  # 0.65
target_required_return = (d1_current / target_current_price) + current_growth
# = (0.65 / 12.50) + 0.04 = 0.052 + 0.04 = 0.092 or 9.2%

# Step 3: Revalue target with new growth assumption using SAME required return
d1_new = target_dividend_per_share * (1 + new_growth)  # 0.6625
new_value_per_share = d1_new / (target_required_return - new_growth)
# = 0.6625 / (0.092 - 0.06) = 0.6625 / 0.032 = 20.703125

# Step 4: Calculate total new value
total_new_value = new_value_per_share * target_shares
# = 20.703125 × 400,000 = 8,281,250

total_new_value  # 8,281,250
```

**Common Bugs to Avoid:**
- Using acquirer's P/E ratio, cost of equity, or earnings yield as the discount rate for the target
- Not deriving the required return from target's current market price
- Forgetting to use D1 (next year's dividend) instead of D0 in Gordon Growth Model
- Applying the wrong growth rate when calculating D1 (use growth rate for the specific scenario being valued)
- Thinking "value to acquirer" means using acquirer's discount rate (NO - target's risk determines its discount rate)

**CHECK Steps:**
- ALWAYS derive target's required return from its own current market valuation
- Verify: r = (D1/P0) + g, where D1 = D0 × (1 + g_current)
- The target's required return is used for ALL valuations of that target, regardless of acquirer
- If question provides acquirer's cost of equity, it is a distractor - do NOT use it for target valuation
- Assert: Target's required return reflects target's risk profile, not acquirer's

---
## Pattern: Stock-for-Stock Acquisition NPV with Synergy

**Description:** In stock-for-stock M&A, NPV to acquirer = Synergy Value - Premium Paid, where Synergy = PV(incremental cash flows from growth improvement) and Premium = (Shares Offered × Acquirer Price) - Target Standalone Value. Must derive target's required return from its own current valuation, not use acquirer's cost of equity.

**When to Use:** Acquisition NPV questions involving stock payment, share exchange offers, or scenarios comparing value creation with different payment methods.

**Procedure:**
1. Calculate target's current value = Target Shares × Target P/E × Target EPS
2. Derive target's required return: r = [Target DPS × (1 + g_old)] / Target Price + g_old
3. Calculate target value with synergy = [Target DPS × (1 + g_new)] / (r - g_new) × Target Shares
4. Calculate cost of acquisition = Shares Offered × Acquirer Stock Price
5. NPV = Target Value with Synergy - Cost of Acquisition

**Code Example:**

**Scenario:** Acquirer offers 150,000 shares (price $40) for target with 400,000 shares, EPS of $2, P/E of 11, dividends of $400,000, current growth 3%, expected synergy growth 5%.

**Correct Code:**
```python
# Given values
acquirer_stock_price = 40
shares_offered = 150000
target_shares = 400000
target_eps = 2
target_pe = 11
target_total_dividends = 400000
current_growth = 0.03
synergy_growth = 0.05

# Step 1: Calculate target's current market value
target_current_price = target_pe * target_eps
target_current_value = target_current_price * target_shares
target_dps = target_total_dividends / target_shares

# Step 2: Derive target's required return
d1_current = target_dps * (1 + current_growth)
target_required_return = (d1_current / target_current_price) + current_growth

# Step 3: Calculate target value with synergy
d1_synergy = target_dps * (1 + synergy_growth)
target_value_per_share_synergy = d1_synergy / (target_required_return - synergy_growth)
target_total_value_synergy = target_value_per_share_synergy * target_shares

# Step 4: Calculate cost of acquisition
cost_of_acquisition = shares_offered * acquirer_stock_price

# Step 5: Calculate NPV
npv_acquisition = target_total_value_synergy - cost_of_acquisition

npv_acquisition
```

**Common Bugs to Avoid:**
- Using acquirer's cost of equity to discount target's cash flows
- Not deriving target's required return from its current market valuation
- Calculating cost as shares offered times target price (should be acquirer price)
- Forgetting that synergy value is the difference in target value with vs. without synergy, not just the new value

---

## Pattern: Cash Flow to Creditors Calculation

**Description:** Cash Flow to Creditors = Interest Paid - Net New Borrowing, where Net New Borrowing = Ending Long-term Debt - Beginning Long-term Debt (the change in debt balance from the balance sheet). This represents the net cash flow FROM the firm TO creditors. Positive CFC means firm paid net cash to creditors; negative means firm received net cash from creditors. Gross new debt issued is NOT used directly - the balance sheet change captures the net effect.

**When to Use:** Questions about "cash flow to creditors," "cash flow to bondholders," or analyzing how much cash the firm paid to or received from debt holders. Also when calculating "cash flows from the firm" as CFC + CFS.

**Procedure:**
1. Formula: Cash Flow to Creditors = Interest Paid - Net New Borrowing
2. Calculate Net New Borrowing = Ending LT Debt - Beginning LT Debt (from balance sheet)
3. If interest paid is given, subtract net new borrowing from interest paid
4. If interest paid is NOT given (or zero), CFC = -Net New Borrowing
5. Interpret sign: Positive CFC = net cash to creditors; Negative CFC = net cash from creditors

**Worked Example:**
**Question:** A firm paid $300 in interest, had beginning long-term debt of $4,000, ending long-term debt of $4,500. Calculate cash flow to creditors.

```python
# Given values
interest_paid = 300
beginning_lt_debt = 4000
ending_lt_debt = 4500

# Step 1: Calculate net new borrowing from balance sheet change
net_new_borrowing = ending_lt_debt - beginning_lt_debt
# = 4500 - 4000 = 500

# Step 2: Calculate cash flow to creditors
# CFC = Interest Paid - Net New Borrowing
cash_flow_to_creditors = interest_paid - net_new_borrowing
# = 300 - 500 = -200

# Interpretation: Negative CFC means firm received net cash FROM creditors
# (Borrowed $500, paid $300 interest, net inflow of $200)

cash_flow_to_creditors  # -200
```

**Common Bugs to Avoid:**
- Using gross new debt issued instead of net new borrowing (balance sheet change)
- Forgetting that net new borrowing accounts for both new issuance AND repayments automatically
- Incorrect sign interpretation (negative CFC means firm received cash from creditors, not paid)
- When interest is not given or zero, forgetting that CFC = -Net New Borrowing
- Not recognizing that the balance sheet change captures the net effect of all debt transactions

**CHECK Steps:**
- Net new borrow
## Pattern: Non-Conventional Cash Flow IRR Existence

**Description:** IRR is only guaranteed to exist and be unique for conventional cash flows (one sign change: negative followed by positives). For non-conventional cash flows (multiple sign changes), Descartes' Rule of Signs indicates 0, 1, or multiple real IRRs may exist. Must check sign changes before attempting numerical solution.

**When to Use:** IRR calculation questions with unusual cash flow patterns, multiple sign changes, or when numerical methods fail to converge or produce unexpected results.

**Procedure:**
1. Count sign changes in cash flow sequence
2. If 0 sign changes: no IRR exists (all same sign)
3. If 1 sign change: unique IRR exists (conventional)
4. If 2+ sign changes: 0, 1, or multiple IRRs possible (non-conventional)
5. For non-conventional: check if NPV changes sign over reasonable rate range; if not, no real IRR exists

**Code Example:**

**Scenario:** Project has cash flows: Year 0: -$15,000, Year 1: -$20,000, Year 2: $10,000 (two sign changes).

**Correct Code:**
```python
import numpy as np

# Given cash flows
cash_flows = [-15000, -20000, 10000]

# Step 1: Count sign changes
sign_changes = 0
for i in range(len(cash_flows) - 1):
    if cash_flows[i] * cash_flows[i + 1] < 0:
        sign_changes += 1

# Step 2: Check if conventional (1 sign change)
if sign_changes == 1:
    # Conventional: calculate IRR
    irr = np.irr(cash_flows)
    result = f"IRR = {irr:.4f}"
elif sign_changes == 0:
    result = "No IRR exists (no sign changes)"
else:
    # Non-conventional: check if real IRR exists
    # Test NPV at various rates
    test_rates = np.linspace(-0.5, 2.0, 100)
    npvs = [np.npv(r, cash_flows) for r in test_rates]
    
    # Check if NPV crosses zero
    if any(npvs[i] * npvs[i+1] < 0 for i in range(len(npvs)-1)):
        # At least one IRR exists, but may be multiple
        result = "Multiple IRRs possible (non-conventional cash flows)"
    else:
        result = "No real IRR exists"

result
```

**Common Bugs to Avoid:**
- Assuming IRR always exists for any cash flow pattern
- Using numerical methods without checking for non-conventional cash flows first
- Not recognizing that multiple sign changes can lead to multiple or no real IRRs
- Reporting a single IRR from numerical solver when multiple IRRs exist

---

## Pattern: Cash Flow from the Firm vs Net Change in Cash

**Description:** "Cash flows from the firm" means cash distributed TO capital providers (dividends + interest + net debt repayment), NOT the net change in the firm's cash balance. It represents what investors receive from the firm, calculated as Operating Cash Flow - Net Capital Spending - Change in NWC, or equivalently as Cash Flow to Creditors + Cash Flow to Stockholders.

**When to Use:** Questions asking for "cash flows from the firm," "total cash distributed to investors," or distinguishing between cash generated by operations vs. cash position changes.

**Procedure:**
1. Formula: CF from Firm = CF to Creditors + CF to Stockholders
2. OR: CF from Firm = Operating Cash Flow - Net Capital Spending - Δ NWC
3. CF to Creditors = Interest Paid - Net New Borrowing
4. CF to Stockholders = Dividends Paid - Net New Equity Issued
5. Do NOT calculate as operating + investing + financing cash flows (that gives net change in cash)

**Code Example:**

**Scenario:** Firm paid $12,000 dividends, $8,000 interest, issued $5,000 new stock, borrowed $15,000 net, purchased $20,000 fixed assets, and had $3,000 increase in NWC. Operating cash flow was $35,000.

**Correct Code:**
```python
# Given values
dividends_paid = 12000
interest_paid = 8000
new_stock_issued = 5000
net_new_borrowing = 15000
fixed_asset_purchases = 20000
change_in_nwc = 3000
operating_cash_flow = 35000

# Method 1: CF to Creditors + CF to Stockholders
cf_to_creditors = interest_paid - net_new_borrowing
cf_to_stockholders = dividends_paid - new_stock_issued
cash_flow_from_firm_method1 = cf_to_creditors + cf_to_stockholders

# Method 2: OCF - Net Capital Spending - Δ NWC
# (Assuming net capital spending = fixed asset purchases for simplicity)
cash_flow_from_firm_method2 = operating_cash_flow - fixed_asset_purchases - change_in_nwc

# Both methods should give same result
cash_flow_from_firm_method1
```

**Common Bugs to Avoid:**
- Confusing "cash flow from the firm" with net change in cash position
- Treating it as operating + investing + financing cash flows (statement of cash flows approach)
- Forgetting to subtract net new equity and net new debt (these are cash FROM investors TO firm, not from firm to investors)
- Not recognizing that this measures what investors receive, not what the firm retains

## Pattern: Working Capital Based on Following Period Sales

**Description:** In capital budgeting, when working capital requirements are specified as a percentage of "the following year's sales increase," the NWC investment at time t must be calculated based on the DOLLAR SALES INCREASE (not total sales) from period t to period t+1. The initial NWC investment is stated separately and should NOT be added to the first period's calculation unless explicitly required. Sales always means revenue (units × price per unit) unless explicitly stated otherwise.

**When to Use:** Questions stating NWC is "based on next year's sales increase," "following period's sales increase," "percentage of projected sales increase," or similar forward-looking working capital requirements based on CHANGES in sales.

**When NOT to Use:** 
- When NWC is stated as a percentage of total sales (not sales increase)
- When initial NWC is given as a separate fixed amount and the percentage applies only to incremental changes
- When the problem provides a complete NWC schedule rather than a calculation rule

**Procedure:**
1. Identify the NWC percentage and what it's based on (e.g., "15% of following year's sales increase")
2. **Distinguish initial NWC from incremental NWC**: If problem states "requires $X in NWC to start AND additional NWC equal to Y% of sales increase," treat these separately
3. Calculate dollar sales (revenue) for each period: Sales[t] = Units[t] × Price[t]
4. Calculate sales INCREASES: ΔSales[t] = Sales[t+1] - Sales[t]
5. For each period t from 0 to n-1: 
   - If t=0 and initial NWC is stated: NWC_investment[0] = Initial_NWC_stated
   - Additional NWC[t] = percentage × ΔSales[t] (based on INCREASE to next period)
6. At project end (period n): Recover all accumulated NWC
7. Calculate net NWC cash flow for each period as the change in total NWC required
8. Subtract NWC investments from operating cash flows in NPV calculation

**Worked Example:**
**Question:** A 3-year project requires $100,000 in initial NWC. Additional NWC must be 10% of the following year's sales increase. Projected sales: Year 1: $500,000, Year 2: $600,000, Year 3: $650,000. Calculate NWC investments.

```python
# Step 1: Project parameters
sales = [0, 500000, 600000, 650000]  # Year 0 has no sales
initial_nwc = 100000
nwc_percentage = 0.10
n_periods = 3

# Step 2: Calculate sales increases
sales_increases = []
for t in range(n_periods):
    increase = sales[t + 1] - sales[t]
    sales_increases.append(increase)

# Step 3: Calculate NWC requirements
# Year 0: Initial NWC (stated separately)
nwc_required = [initial_nwc]

# Years 1-2: Additional NWC based on following year's sales increase
for t in range(n_periods - 1):
    additional_nwc = nwc_percentage * sales_increases[t + 1]
    nwc_required.append(additional_nwc)

# Year 3: No future sales, so no additional NWC needed
nwc_required.append(0)

# Step 4: Calculate NWC investments (changes in total NWC)
total_nwc = [initial_nwc]  # Start with initial NWC
nwc_investment = [initial_nwc]  # Year 0 investment

for t in range(1, n_periods + 1):
    if t < n_periods:
        total_nwc.append(total_nwc[t-1] + nwc_required[t])
        nwc_investment.append(nwc_required[t])
    else:
        # Year 3: Recover all NWC
        total_nwc.append(0)
        nwc_investment.append(-total_nwc[t-1])

# Year 0: -100,000 (initial)
# Year 1: -10,000 (10% of 600k-500k = 100k increase)
# Year 2: -5,000 (10% of 650k-600k = 50k increase)
# Year 3: +115,000 (recover all)

nwc_investment  # [-100000, -10000, -5000, 115000]
```

**Common Bugs to Avoid:**
- Adding initial NWC to the first period's percentage calculation (double-counting)
- Using total sales instead of sales INCREASE for the percentage calculation
- Calculating NWC based on current period instead of following period's sales increase
- Forgetting that "additional NWC" means ON TOP OF initial NWC, not replacing it
- Not distinguishing between "requires $X to start AND Y% of increases" vs. "requires Y% of sales"

**CHECK Steps:**
- Verify: If problem states "requires $X in NWC to start AND additional NWC equal to Y%", Year 0 investment = $X only
- If NWC is based on "following year's sales increase," calculate ΔSales[t+1] = Sales[t+1] - Sales[t]
- Sum of all NWC investments should equal zero (what goes in must come out)
- Initial NWC should NOT be multiplied by the percentage unless explicitly stated
- Assert: Additional NWC[t] = percentage × (Sales[t+1] - Sales[t]), not percentage × Sales[t+1]

---
## Pattern: Implied Volatility from Option Pricing (Merton Model)

**Description:** In a leveraged firm, equity can be viewed as a call option on firm value with strike price equal to debt face value. The relationship between equity volatility (σ_E) and firm value volatility (σ_V) is: σ_E = (V/E) × N(d1) × σ_V, where N(d1) is from the Black-Scholes model. This requires iterative solution to extract σ_V from observed σ_E.

**When to Use:** Questions asking for "implied standard deviation in firm value," "firm volatility from equity volatility," or scenarios involving equity as a call option on firm assets.

**Procedure:**
1. Calculate firm value: V = Market value of equity + Market value of debt
2. Calculate equity value: E = Shares × Stock price
3. Identify debt face value and time to maturity
4. Use observed equity volatility (σ_E) from market data
5. Set up Merton model: σ_E = (V/E) × N(d1) × σ_V
6. Solve iteratively for σ_V (firm volatility) using numerical methods
7. d1 = [ln(V/D) + (r + 0.5×σ_V²)×T] / (σ_V × √T)

**Worked Example:**
**Question:** A firm has equity value of $500M (volatility 60%), debt face value of $300M maturing in 1 year, risk-free rate 5%. Estimate firm value volatility.

```python
import math
from scipy.stats import norm
from scipy.optimize import fsolve

# Step 1: Given values
equity_value = 500  # millions
equity_volatility = 0.60
debt_face_value = 300  # millions
time_to_maturity = 1.0
risk_free_rate = 0.05

# Step 2: Initial estimate of firm value (equity + debt at face value)
firm_value_initial = equity_value + debt_face_value  # 800

# Step 3: Define function to solve for firm volatility
def merton_equation(sigma_v):
    V = firm_value_initial
    E = equity_value
    D = debt_face_value
    T = time_to_maturity
    r = risk_free_rate
    
    # Calculate d1
    d1 = (math.log(V / D) + (r + 0.5 * sigma_v**2) * T) / (sigma_v * math.sqrt(T))
    
    # Calculate N(d1)
    n_d1 = norm.cdf(d1)
    
    # Merton relationship: σ_E = (V/E) × N(d1) × σ_V
    implied_equity_vol = (V / E) * n_d1 * sigma_v
    
    # Return difference from observed equity volatility
    return implied_equity_vol - equity_volatility

# Step 4: Solve for firm volatility
firm_volatility = fsolve(merton_equation, 0.30)[0]  # Initial guess 30%

firm_volatility  # Approximately 0.375 or 37.5%
```

**Common Bugs to Avoid:**
- Using simple portfolio variance formula instead of option pricing relationship
- Treating equity volatility and firm volatility as directly proportional
- Forgetting that leverage amplifies equity volatility relative to firm volatility
- Not using iterative solution (the relationship is non-linear)

**CHECK Steps:**
- Verify: Firm volatility should be LOWER than equity volatility (leverage amplifies equity risk)
- Assert: σ_E = (V/E) × N(d1) × σ_V should hold for the solution
- If V/E ratio is high (low leverage), σ_V should be close to σ_E

---

## Pattern: Homemade Leverage and Arbitrage in Modigliani-Miller Framework

**Description:** In M&M world without taxes, investors can replicate levered equity returns by borrowing personally against unlevered equity (homemade leverage). When comparing strategies, the final answer format must match the question's expected response type - return boolean True/False only if question explicitly asks for a yes/no decision, otherwise return descriptive string "Yes" or "No".

**When to Use:** Questions about homemade leverage, M&M arbitrage opportunities, or comparing levered vs. unlevered equity investment strategies where investor can borrow at specified rates.

**When NOT to Use:** When question asks for numerical NPV, return values, or detailed financial metrics rather than a yes/no decision.

**Procedure:**
1. Calculate Strategy 1 (buy levered equity): Initial cost and annual return
2. Calculate Strategy 2 (buy unlevered equity + borrow): Match initial net cost by borrowing
3. Borrowing amount = Unlevered investment - Levered investment (to equalize initial costs)
4. Calculate net return for Strategy 2: Equity earnings - Interest on borrowing
5. Compare returns: Difference = Strategy 2 return - Strategy 1 return
6. **Format answer based on question type**: If question asks "Can he increase..." or similar yes/no format, return string "Yes" or "No" (NOT boolean True/False)

**Code Example:**

**Scenario:** Levered firm has equity worth $200k earning $20k/year. Unlevered firm has equity worth $300k earning $30k/year. Investor can borrow at 5%. Can investor increase return by using homemade leverage to match $200k net cost?

**Correct Code:**
```python
# Strategy 1: Buy levered equity
levered_equity_value = 200000
levered_annual_earnings = 20000

# Strategy 2: Buy unlevered equity and borrow
unlevered_equity_value = 300000
unlevered_annual_earnings = 30000
borrowing_rate = 0.05

# Match initial net costs
borrowing_amount = unlevered_equity_value - levered_equity_value  # 100,000

# Calculate returns
strategy1_return = levered_annual_earnings  # 20,000
strategy2_earnings = unlevered_annual_earnings  # 30,000
strategy2_interest = borrowing_amount * borrowing_rate  # 5,000
strategy2_net_return = strategy2_earnings - strategy2_interest  # 25,000

# Compare
difference = strategy2_net_return - strategy1_return  # 5,000
can_increase = difference > 0

# Return string format for yes/no questions (NOT boolean)
answer = "Yes" if can_increase else "No"
answer
```

**Common Bugs to Avoid:**
- Returning boolean True/False instead of string "Yes"/"No" when question expects text answer
- Not matching initial net costs between strategies (borrowing amount must equalize upfront investment)
- Forgetting to subtract interest cost from unlevered equity earnings in Strategy 2
- Using wrong borrowing rate (should use investor's borrowing rate, not firm's debt rate)

**CHECK Steps:**
- Verify: Net initial cost of Strategy 2 = Unlevered investment - Borrowing = Strategy 1 cost
- If question asks "Can he/she increase..." or "Is it possible to...", return string "Yes" or "No"
- If question asks for numerical value or detailed comparison, return appropriate numeric/dict format
- Assert: Borrowing amount = Unlevered equity investment - Levered equity investment

---

## Pattern: Project NPV with Abandonment Options and Economic Life Optimization

**Description:** When evaluating optimal project life with abandonment options, calculate NPV for each possible abandonment year including operating cash flows, after-tax salvage proceeds, and NWC recovery. Return results in a format that matches the question's requirements - use labeled dictionary for comprehensive reporting, simple numeric/text for specific queries.

**When to Use:** Questions about optimal economic life, abandonment analysis, or comparing NPVs across different project durations with equipment salvage values.

**When NOT to Use:** Standard NPV calculations without abandonment options or when question asks only for a single NPV value.

**Procedure:**
1. Calculate annual operating cash flow: OCF = (Revenue - Costs - Depreciation) × (1 - Tax) + Depreciation
2. For each abandonment year t:
   - Sum discounted operating cash flows from year 1 to t
   - Calculate book value at year t: Initial Investment - (Depreciation × t)
   - Calculate after-tax salvage: Market Value - Tax × (Market Value - Book Value)
   - Add discounted terminal value: (After-tax salvage + NWC recovery) / (1 + r)^t
3. Compare NPVs across all abandonment scenarios
4. **Format output based on question requirements**: If question asks to "compute NPVs" for multiple scenarios, return labeled dictionary; if asking "what economic life maximizes value", can return just the optimal year

**Code Example:**

**Scenario:** Project requires $100k initial investment, $20k NWC, generates $50k annual OCF. Depreciation is $25k/year. Market values: Year 1: $80k, Year 2: $60k, Year 3: $30k. Tax rate 30%, discount rate 12%. Find optimal life.

**Correct Code:**
```python
# Given parameters
initial_investment = 100000
nwc = 20000
annual_ocf = 50000
annual_depreciation = 25000
tax_rate = 0.30
discount_rate = 0.12
market_values = {1: 80000, 2: 60000, 3: 30000}

def calculate_npv_abandonment(year):
    npv = -initial_investment - nwc
    
    # Operating cash flows
    for t in range(1, year + 1):
        npv += annual_ocf / (1 + discount_rate) ** t
    
    # Terminal value
    book_value = initial_investment - (annual_depreciation * year)
    market_value = market_values[year]
    gain_on_sale = market_value - book_value
    tax_on_gain = gain_on_sale * tax_rate
    after_tax_salvage = market_value - tax_on_gain
    terminal_value = after_tax_salvage + nwc
    npv += terminal_value / (1 + discount_rate) ** year
    
    return npv

# Calculate for all scenarios
results = {
    f'NPV if abandoned after Year {y}': round(calculate_npv_abandonment(y), 2)
    for y in [1, 2, 3]
}

# Find optimal
optimal_year = max(range(1, 4), key=lambda y: calculate_npv_abandonment(y))
results['Optimal Economic Life (years)'] = optimal_year
results['Maximum NPV'] = round(calculate_npv_abandonment(optimal_year), 2)

# Return labeled dictionary for comprehensive reporting
results
```

**Common Bugs to Avoid:**
- Returning unlabeled tuple instead of dictionary when question asks to "compute NPVs" for multiple scenarios
- Forgetting to include NWC recovery in terminal value
- Not calculating after-tax salvage value (must account for gain/loss on sale)
- Using market value directly without adjusting for tax on gain/loss

**CHECK Steps:**
- If question asks to "compute NPVs" or "calculate NPVs for different scenarios," return dictionary with labeled keys
- If question asks only "what economic life maximizes value," can return just the optimal year or simple statement
- Verify: Terminal value = After-tax salvage + NWC recovery
- Assert: After-tax salvage = Market Value - Tax × (Market Value - Book Value)
- Ensure output format matches question requirements (dictionary vs. tuple vs. single value)

## Pattern: Synergy Value Interpretation in Zero-Premium Mergers

**Description:** When an acquirer pays exactly the target's standalone market value (zero premium), the question "What synergy value must the acquirer believe exists?" has two interpretations: (1) Minimum synergy needed for NPV ≥ 0 is zero, OR (2) Implied synergy belief equals the target's market value (making total perceived value = 2× standalone value). Context determines which interpretation applies.

**When to Use:** Questions asking "what synergy must exist" or "what synergy value does acquirer believe" in merger scenarios where the acquisition price exactly equals target's standalone market value.

**Procedure:**
1. Calculate target's standalone market value
2. Calculate acquisition cost (cash paid or shares issued × acquirer price)
3. Calculate premium: Cost - Standalone Value
4. If premium = 0, determine question intent:
   - "Minimum synergy needed" → Answer: $0 (NPV = Synergy - Premium = Synergy - 0 ≥ 0)
   - "What synergy value justifies the deal" → Answer: Target's market value (acquirer believes combined value = 2× standalone)
5. For non-zero premium: Minimum synergy = Premium (for NPV = 0)

**Worked Example:**
**Question:** Target has market value of $5,000,000. Acquirer offers exactly $5,000,000 in cash. What synergy value must the acquirer believe exists to justify proceeding with this acquisition?

```python
# Step 1: Target standalone value
target_standalone_value = 5000000

# Step 2: Acquisition cost
acquisition_cost = 5000000

# Step 3: Premium paid
premium = acquisition_cost - target_standalone_value  # 0

# Step 4: Interpret based on question context
# Question asks "what synergy value justifies proceeding"
# This implies: what does acquirer BELIEVE synergy is worth?

if premium == 0:
    # Zero premium case: two interpretations
    minimum_synergy_needed = 0  # For NPV ≥ 0
    
    # If acquirer proceeds at zero premium, they must believe synergy exists
    # Otherwise, why acquire? Implied belief: synergy = target value
    implied_synergy_belief = target_standalone_value
    
    result = {
        'Premium Paid': premium,
        'Minimum Synergy Needed (for NPV=0)': minimum_synergy_needed,
        'Implied Synergy Belief (to justify deal)': implied_synergy_belief,
        'Interpretation': 'Acquirer believes synergy equals target market value, making total value = 2× standalone'
    }
else:
    # Non-zero premium case
    minimum_synergy_needed = premium
    result = {
        'Premium Paid': premium,
        'Minimum Synergy Needed (for NPV=0)': minimum_synergy_needed
    }

result
```

**Common Bugs to Avoid:**
- Confusing "minimum synergy needed" with "what synergy acquirer believes exists"
- Assuming zero premium means zero synergy belief (ignores why acquirer would proceed)
- Not distinguishing between NPV break-even analysis and implied valuation beliefs
- Treating all synergy questions identically without considering context

**CHECK Steps:**
- If premium = 0 and question asks "minimum synergy needed," answer is $0
- If premium = 0 and question asks "what synergy justifies the deal" or "what does acquirer believe," answer is target's market value
- For any premium > 0, minimum synergy needed = premium (for NPV = 0)
- Verify: NPV = Synergy Value - Premium

---