# DETAILED SKILL PATTERNS FOR CORPORATE FINANCE (Program of Thought)

---

## Pattern: Merger Share Price with No Synergy

**Description:** When calculating post-merger share price with no synergy gains, must preserve total market value and account for share exchange ratios based on relative market values, not simply add shares or use earnings per share as price.

**When to Use:** Questions about post-merger share prices, merger valuations, or "no synergy" scenarios involving two firms combining.

**Procedure:**
1. Formula: Post-merger price = Combined Market Value / New Total Shares Outstanding
2. Calculate pre-merger market values: Market Value = Shares × Price per Share
3. Determine exchange ratio: ratio = (Target Market Value) / (Acquirer Price per Share)
4. Calculate new shares outstanding: New Shares = Acquirer Shares + (Target Shares × Exchange Ratio) OR New Shares = Acquirer Shares + Shares Issued
5. Calculate combined market value: Combined MV = Acquirer MV + Target MV (no synergy)
6. Compute post-merger price: Price = Combined MV / New Shares

**Code Example:**

**Scenario:** Firm Alpha has 500 shares at $80/share. Firm Beta has 200 shares at $30/share. Alpha acquires Beta with no synergy. What is Alpha's post-merger share price if Beta shareholders receive Alpha shares at market value?

**Correct Code:**
```python
# Pre-merger values
alpha_shares = 500
alpha_price = 80
beta_shares = 200
beta_price = 30

# Calculate market values
alpha_market_value = alpha_shares * alpha_price  # 40,000
beta_market_value = beta_shares * beta_price      # 6,000

# Exchange ratio: Beta shareholders get Alpha shares worth Beta's market value
# Number of Alpha shares issued = Beta Market Value / Alpha Price
new_alpha_shares_issued = beta_market_value / alpha_price  # 75 shares

# Total shares after merger
total_shares_post_merger = alpha_shares + new_alpha_shares_issued  # 575

# Combined market value (no synergy)
combined_market_value = alpha_market_value + beta_market_value  # 46,000

# Post-merger share price
post_merger_price = combined_market_value / total_shares_post_merger

post_merger_price  # 80.0 (preserved value)
```

**Common Bugs to Avoid:**
- Confusing EPS with share price (earnings/shares ≠ market price)
- Simply adding shares without considering exchange ratios
- Forgetting that market value must be preserved in no-synergy mergers
- Using book values instead of market values

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

**Description:** Stock dividends transfer value from retained earnings to equity accounts. The amount transferred = (shares issued) × (market price), with par value going to common stock and the remainder to capital surplus.

**When to Use:** Questions about stock dividend effects on equity accounts, changes in common stock, or capital surplus calculations.

**Procedure:**
1. Formula: Total Transfer = New Shares × Market Price per Share
2. Calculate shares outstanding: Common Stock / Par Value per Share
3. Calculate new shares issued: Outstanding Shares × Dividend Percentage
4. Calculate total value transferred: New Shares × Market Price
5. Calculate addition to common stock: New Shares × Par Value
6. Calculate addition to capital surplus: Total Transfer - Addition to Common Stock
7. Retained earnings decreases by total transfer amount

**Code Example:**

**Scenario:** Firm has 200,000 shares ($1 par) outstanding, market price $40. Declares 10% stock dividend. What is the value of new common stock (at par)?

**Correct Code:**
```python
# Current equity structure
common_stock_account = 200000  # $1 par × 200,000 shares
par_value_per_share = 1
market_price_per_share = 40
stock_dividend_percentage = 0.10

# Calculate shares outstanding
shares_outstanding = common_stock_account / par_value_per_share  # 200,000

# New shares issued
new_shares_issued = shares_outstanding * stock_dividend_percentage  # 20,000

# Value of new common stock (at par value, added to common stock account)
new_common_stock_par_value = new_shares_issued * par_value_per_share

# Total value transferred from retained earnings
total_transfer = new_shares_issued * market_price_per_share  # 800,000

# Addition to capital surplus
addition_to_capital_surplus = total_transfer - new_common_stock_par_value

new_common_stock_par_value  # 20,000 (this is what goes to common stock account)
```

**Common Bugs to Avoid:**
- Confusing total market value transferred with par value addition to common stock
- Using market value as the "new common stock" value (should use par value)
- Forgetting that capital surplus receives the difference (market - par)
- Not recognizing that total owners' equity remains unchanged

---

## Pattern: Blocked Funds and Reinvestment in International Capital Budgeting

**Description:** When cash flows are "blocked and reinvested for one year," each cash flow is delayed by exactly one period and grows at the reinvestment rate for that single period only, not compounded until project end.

**When to Use:** Questions about international projects with blocked funds, mandatory reinvestment requirements, or foreign exchange restrictions.

**Procedure:**
1. Formula: Adjusted CF(t) = Original CF(t-1) × (1 + reinvestment rate), received at time t
2. Identify which cash flows are blocked (typically all except initial investment)
3. Shift each blocked cash flow forward by one period
4. Multiply each shifted cash flow by (1 + reinvestment rate) for the one-year delay
5. Create new cash flow timeline with adjusted amounts and timing
6. Calculate NPV or IRR using the adjusted cash flows

**Code Example:**

**Scenario:** Project has cash flows: Year 0: -$500,000, Year 1: $200,000, Year 2: $300,000. All positive flows blocked and reinvested at 3% for one year. Calculate adjusted cash flows.

**Correct Code:**
```python
# Original cash flows
cf_0 = -500000  # Not blocked (initial investment)
cf_1 = 200000   # Blocked
cf_2 = 300000   # Blocked

reinvestment_rate = 0.03

# Adjusted cash flows (blocked flows delayed by 1 year, earn reinvestment rate)
adjusted_cf_0 = cf_0  # -500,000 (not affected)
adjusted_cf_1 = 0     # Original year 1 flow is blocked
adjusted_cf_2 = cf_1 * (1 + reinvestment_rate)  # 206,000 (year 1 flow received in year 2)
adjusted_cf_3 = cf_2 * (1 + reinvestment_rate)  # 309,000 (year 2 flow received in year 3)

# For IRR calculation
import numpy as np
adjusted_cash_flows = [adjusted_cf_0, adjusted_cf_1, adjusted_cf_2, adjusted_cf_3]
irr = np.irr(adjusted_cash_flows)

irr  # Calculate IRR on adjusted flows
```

**Common Bugs to Avoid:**
- Compounding each cash flow from original period to project end (wrong interpretation)
- Not shifting cash flows forward by exactly one period
- Applying reinvestment rate multiple times to the same cash flow
- Forgetting that initial investment is typically not blocked

---

## Pattern: Credit Policy NPV as Perpetuity Valuation

**Description:** Changes in credit policy create perpetual changes in monthly cash flows. NPV = (Change in Monthly CF / Monthly Required Return) - Initial Investment in Accounts Receivable, not just the monthly benefit.

**When to Use:** Questions about credit policy changes, net 30 terms, or evaluating switch from cash to credit sales.

**Procedure:**
1. Formula: NPV = (ΔMonthly CF / r_monthly) - Initial AR Investment
2. Calculate monthly contribution under each policy: (Price - Cost) × Units
3. Calculate change in monthly contribution: New - Old
4. Calculate initial investment in AR: (New Price × New Units) × (Days/365) × (Cost/Price)
5. Or simpler: AR Investment = (New Monthly Sales) × (Cost/Price) if net 30
6. Calculate PV of perpetual cash flow change: ΔMonthly CF / r_monthly
7. Subtract initial AR investment to get NPV

**Code Example:**

**Scenario:** Current policy: $50 price, $35 cost, 800 units/month. New policy (net 30): $52 price, $36 cost, 850 units/month. Required return 0.8% per month. Find NPV.

**Correct Code:**
```python
# Current policy (all cash)
current_price = 50
current_cost = 35
current_units = 800

# New policy (net 30 days)
new_price = 52
new_cost = 36
new_units = 850

# Required return
monthly_required_return = 0.008

# Monthly contribution under each policy
current_monthly_contribution = (current_price - current_cost) * current_units  # 12,000
new_monthly_contribution = (new_price - new_cost) * new_units  # 13,600

# Change in monthly contribution
change_in_monthly_contribution = new_monthly_contribution - current_monthly_contribution  # 1,600

# Initial investment in accounts receivable (net 30 = 1 month of cost of goods sold)
# AR investment = monthly sales × (cost/price) for net 30
monthly_sales_new = new_price * new_units  # 44,200
ar_investment = monthly_sales_new * (new_cost / new_price)  # 30,600

# PV of perpetual cash flow change
pv_perpetual_cash_flows = change_in_monthly_contribution / monthly_required_return  # 200,000

# NPV
npv = pv_perpetual_cash_flows - ar_investment

npv  # 169,400
```

**Common Bugs to Avoid:**
- Treating monthly benefit as one-time gain instead of perpetuity
- Forgetting to divide by required return to get PV of perpetuity
- Not subtracting initial AR investment (upfront cost)
- Using full sales value instead of cost for AR investment
- Confusing operational analysis with NPV calculation

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

**Description:** Synergy value is the incremental value created by combining firms (cost savings, revenue enhancements). Acquisition premium is what the acquirer pays above target's standalone market value. For a rational deal, synergy must exceed premium.

**When to Use:** Questions about "what synergy must exist," merger justification, or reconciling acquisition decisions with premiums paid.

**Procedure:**
1. Formula: Synergy Value = Combined Firm Value - (Acquirer Standalone + Target Standalone)
2. Calculate target's standalone market value: Shares × Price (or P/E × Earnings)
3. Calculate acquirer's standalone market value similarly
4. Calculate acquisition cost (cash paid or shares issued × acquirer price)
5. Calculate premium: Cost - Target Standalone Value
6. For deal to be rational: Synergy Value ≥ Premium
7. Post-merger combined value reflects expected synergies in market valuation

**Code Example:**

**Scenario:** Acquirer worth $5,000,000 offers $1,800,000 for target worth $1,500,000. What minimum synergy justifies this? What does market value suggest if combined firm trades at $6,500,000?

**Correct Code:**
```python
# Standalone values
acquirer_standalone_value = 5000000
target_standalone_value = 1500000

# Acquisition terms
acquisition_cost = 1800000

# Premium paid
premium = acquisition_cost - target_standalone_value  # 300,000

# Minimum synergy needed to justify premium
minimum_synergy_needed = premium  # 300,000

# If combined firm market value is observed
combined_market_value = 6500000

# Implied synergy from market valuation
implied_synergy = combined_market_value - (acquirer_standalone_value + target_standalone_value)

# Reconciliation: Deal is justified if implied_synergy >= premium
is_deal_justified = implied_synergy >= premium

implied_synergy  # 0 (market sees no synergy, deal destroys value)
```

**Common Bugs to Avoid:**
- Confusing premium with synergy (premium is cost, synergy is benefit)
- Thinking premium equals synergy (synergy must exceed premium for value creation)
- Not recognizing that market value reflects expected synergies
- Forgetting that negative synergy (value destruction) is possible

---

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

**Description:** When two firms merge and face independent state-contingent outcomes, the combined firm's value in each scenario is the sum of individual firm values in their respective states, creating a matrix of possible outcomes.

**When to Use:** Questions about merger values with independent economic states, portfolio effects, or diversification benefits in mergers.

**Procedure:**
1. Formula: Combined Value(state_A, state_B) = Firm_A_Value(state_A) + Firm_B_Value(state_B)
2. Identify all possible states for each firm and their probabilities
3. Create outcome matrix: all combinations of states
4. Calculate combined firm value for each combination
5. Calculate joint probability: P(state_A) × P(state_B) if independent
6. Calculate expected combined value: Σ [Joint Probability × Combined Value]
7. For specific scenarios, identify the relevant state combination

**Code Example:**

**Scenario:** Firm A has boom (0.6, $400k) or recession (0.4, $200k). Firm B has boom (0.5, $300k) or recession (0.5, $150k). States are independent. What is combined value in A-boom, B-recession?

**Correct Code:**
```python
# Firm A states
prob_a_boom = 0.6
value_a_boom = 400000
prob_a_recession = 0.4
value_a_recession = 200000

# Firm B states
prob_b_boom = 0.5
value_b_boom = 300000
prob_b_recession = 0.5
value_b_recession = 150000

# Specific scenario: A-boom, B-recession
combined_value_a_boom_b_recession = value_a_boom + value_b_recession  #

## Pattern: Cash Flow from Assets Formula Structure

**Description:** Cash Flow from Assets (CFA) must be calculated using the correct formula: CFA = Operating Cash Flow - Net Capital Spending - Change in Net Working Capital, where OCF = EBIT + Depreciation - Taxes (not starting from Net Income). Starting from Net Income double-counts the interest expense effect and produces incorrect results.

**When to Use:** Questions asking for "cash flow from assets," "cash flow to the firm," or requiring calculation of total cash generated by firm operations independent of financing structure.

**Procedure:**
1. Formula: CFA = OCF - NCS - ΔNWC, where OCF = EBIT + Depreciation - Taxes
2. Calculate Operating Cash Flow using EBIT (not Net Income) to exclude financing effects
3. Calculate Net Capital Spending = Ending NFA - Beginning NFA + Depreciation
4. Calculate Change in Net Working Capital = (Ending CA - Ending CL) - (Beginning CA - Beginning CL)
5. Combine: CFA = OCF - NCS - ΔNWC

**Code Example:**

**Scenario:** A firm has EBIT of $5,000, depreciation of $1,200, tax rate of 30%, net fixed assets increased from $40,000 to $41,500, current assets increased from $20,000 to $22,000, and current liabilities increased from $8,000 to $8,500.

**Correct Code:**
```python
# Given values
ebit = 5000
depreciation = 1200
tax_rate = 0.30
nfa_beginning = 40000
nfa_ending = 41500
current_assets_beginning = 20000
current_assets_ending = 22000
current_liabilities_beginning = 8000
current_liabilities_ending = 8500

# Step 1: Calculate Operating Cash Flow (OCF)
# OCF = EBIT + Depreciation - Taxes
taxes = ebit * tax_rate
ocf = ebit + depreciation - taxes

# Step 2: Calculate Net Capital Spending (NCS)
# NCS = Ending NFA - Beginning NFA + Depreciation
ncs = nfa_ending - nfa_beginning + depreciation

# Step 3: Calculate Change in Net Working Capital (ΔNWC)
nwc_beginning = current_assets_beginning - current_liabilities_beginning
nwc_ending = current_assets_ending - current_liabilities_ending
change_in_nwc = nwc_ending - nwc_beginning

# Step 4: Calculate Cash Flow from Assets
cash_flow_from_assets = ocf - ncs - change_in_nwc

cash_flow_from_assets
```

**Common Bugs to Avoid:**
- Starting from Net Income instead of EBIT (Net Income already includes interest, which should be excluded from operating cash flow)
- Forgetting to add back depreciation when calculating Net Capital Spending
- Calculating change in working capital as change in current assets minus change in current liabilities (incorrect) instead of change in (CA - CL)
- Using wrong sign conventions (NCS and ΔNWC should be subtracted from OCF)

---

## Pattern: Target Required Return from Current Market Valuation

**Description:** To value an acquisition target with changed assumptions (e.g., different growth rate), first derive the target's required return from its current market price using the Gordon Growth Model in reverse: r = (D1/P0) + g_current. Then use this r to revalue the target with new growth assumptions. Do NOT use the acquirer's cost of equity or earnings yield.

**When to Use:** Acquisition valuation questions where growth rate assumptions change, scenarios asking "what if growth rate is X instead of Y," or when revaluing a target under different scenarios.

**Procedure:**
1. Formula: r = (D1/P0) + g, where D1 = D0 × (1 + g)
2. Calculate target's current price per share = P/E ratio × EPS
3. Calculate target's dividend per share = Total Dividends / Shares Outstanding
4. Derive required return: r = [Dividend per share × (1 + current_growth)] / Current Price + current_growth
5. Revalue with new growth: New Value = [Dividend × (1 + new_growth)] / (r - new_growth)

**Code Example:**

**Scenario:** Target firm has 500,000 shares, earnings of $600,000, dividends of $300,000, P/E ratio of 12, current expected growth of 3%, and acquirer believes growth will be 5%.

**Correct Code:**
```python
# Given values
target_shares = 500000
target_earnings = 600000
target_dividends = 300000
target_pe_ratio = 12
current_growth = 0.03
new_growth = 0.05

# Step 1: Calculate target's current market metrics
target_eps = target_earnings / target_shares
target_current_price = target_pe_ratio * target_eps
target_dividend_per_share = target_dividends / target_shares

# Step 2: Derive target's required return from current valuation
# Using Gordon Growth Model: P0 = D1 / (r - g)
# Rearranging: r = D1/P0 + g
d1_current = target_dividend_per_share * (1 + current_growth)
required_return = (d1_current / target_current_price) + current_growth

# Step 3: Revalue target with new growth assumption
d1_new = target_dividend_per_share * (1 + new_growth)
new_value_per_share = d1_new / (required_return - new_growth)

# Step 4: Calculate total new value
total_new_value = new_value_per_share * target_shares

total_new_value
```

**Common Bugs to Avoid:**
- Using acquirer's P/E ratio or earnings yield as the discount rate for the target
- Not deriving the required return from target's current market price
- Forgetting to use D1 (next year's dividend) instead of D0 in Gordon Growth Model
- Applying the wrong growth rate when calculating D1 (should use the growth rate corresponding to the valuation scenario)

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

**Description:** Cash Flow to Creditors = Interest Paid - Net New Borrowing, where Net New Borrowing = Ending Long-term Debt - Beginning Long-term Debt (the change in debt balance). Gross new debt issued does NOT equal net new borrowing when debt repayments also occur.

**When to Use:** Questions about "cash flow to creditors," "cash flow to bondholders," or analyzing how much cash the firm paid to or received from debt holders.

**Procedure:**
1. Formula: Cash Flow to Creditors = Interest Paid - Net New Borrowing
2. Calculate Net New Borrowing = Ending LT Debt - Beginning LT Debt
3. Subtract net new borrowing from interest paid
4. Negative result means firm received net cash from creditors; positive means firm paid net cash to creditors

**Code Example:**

**Scenario:** A firm paid $250 in interest, had beginning long-term debt of $3,000, ending long-term debt of $3,400, and issued $600 in new bonds during the year.

**Correct Code:**
```python
# Given values
interest_paid = 250
beginning_lt_debt = 3000
ending_lt_debt = 3400
# Note: new bonds issued (600) is given but NOT directly used

# Step 1: Calculate net new borrowing from balance sheet change
net_new_borrowing = ending_lt_debt - beginning_lt_debt

# Step 2: Calculate cash flow to creditors
# CFC = Interest Paid - Net New Borrowing
cash_flow_to_creditors = interest_paid - net_new_borrowing

cash_flow_to_creditors
```

**Common Bugs to Avoid:**
- Using gross new debt issued instead of net new borrowing (change in debt balance)
- Forgetting that net new borrowing accounts for both new issuance AND repayments
- Incorrect sign interpretation (negative CFC means firm received cash from creditors)
- Not recognizing that the balance sheet change captures the net effect automatically

---

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