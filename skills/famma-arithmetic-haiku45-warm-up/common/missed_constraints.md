# DETAIL File: Missed Constraints — Explicit Constraints Not Applied

## Pattern: Hedging Instrument Payoff Integration

**Description:** When a derivative instrument (option, swap, futures) is used to hedge a position, the effective cost/return must incorporate the instrument's payoff at expiration, not just the underlying position's standalone calculation.

**When to Use:** Questions involving options, futures, or swaps as hedges where "effective rate," "effective cost," or "net payment" is requested; keywords: "hedging," "protection," "effective borrowing cost."

**Procedure:**
1. Formula: Effective Cost = Base Cost ± Hedge Payoff ± Hedge Premium
2. Calculate the standalone position outcome (loan interest, asset value, etc.)
3. Calculate the hedge instrument's intrinsic payoff: max(S - K, 0) for calls, max(K - S, 0) for puts
4. Adjust for premiums paid or received (reduce benefit by premium cost)
5. Combine to get net effective position
6. Apply any required transformations (annualization, per-share basis, etc.)

**Code Example:**

**Scenario:** A company borrows $10M for 90 days at 90-day LIBOR + 0.75%. They buy an interest rate call option with strike 2.5% for premium $25,000. At loan initiation, 90-day LIBOR is 3.0%. Calculate effective annual borrowing rate.

**Correct Code:**
```python
import math

# Given values
loan_amount = 10_000_000
loan_days = 90
libor_rate = 0.03  # 3.0%
spread = 0.0075  # 0.75%
call_strike = 0.025  # 2.5%
call_premium = 25_000

# Step 1: Calculate base loan rate
base_loan_rate = libor_rate + spread  # 3.75%

# Step 2: Calculate call option payoff
# Call pays off when LIBOR > strike
call_payoff_rate = max(libor_rate - call_strike, 0)  # max(3.0% - 2.5%, 0) = 0.5%

# Step 3: Net interest rate after hedge
net_rate = base_loan_rate - call_payoff_rate  # 3.75% - 0.5% = 3.25%

# Step 4: Calculate interest amount
interest_amount = loan_amount * net_rate * (loan_days / 365)

# Step 5: Add option premium to total cost
total_cost = interest_amount + call_premium

# Step 6: Calculate effective rate including premium
effective_periodic_rate = total_cost / loan_amount

# Step 7: Annualize the effective rate
effective_annual_rate = ((1 + effective_periodic_rate) ** (365 / loan_days) - 1)

effective_annual_rate  # Result as decimal
```

**Common Bugs to Avoid:**
- Ignoring the hedge instrument entirely and calculating only the base position
- Forgetting to incorporate option/futures premium into effective cost
- Applying hedge payoff with wrong sign (subtracting when should add, or vice versa)
- Confusing notional amount with actual cash flows in derivative payoffs

---

## Pattern: Cross-Reference Constraint Retrieval

**Description:** When a question explicitly references a prior question ("as in question 1," "assuming conditions in question 4"), critical parameters from that referenced question must be retrieved and applied, not assumed or defaulted.

**When to Use:** Questions containing phrases like "in question X," "as stated in question Y," "using the result from," "assuming the conditions in question Z."

**Procedure:**
1. Identify the cross-reference phrase and question number
2. Extract ALL parameters from the referenced question (quantities, prices, terms, assumptions)
3. Verify no conflicting information exists in current question
4. Apply retrieved constraints to current calculation
5. Document the source of each critical parameter in comments

**Code Example:**

**Scenario:** Question 1 states: "An investor buys 15 call option contracts (100 shares each) at strike $50." Question 2 asks: "Using the position from question 1, if the stock price at expiration is $58, what is the total payoff?"

**Correct Code:**
```python
# CRITICAL: Retrieved from Question 1
num_contracts = 15  # From Q1: "15 call option contracts"
shares_per_contract = 100  # Standard contract size
strike_price = 50  # From Q1: "strike $50"

# From current question (Question 2)
stock_price_expiration = 58

# Step 1: Calculate per-share intrinsic value
intrinsic_value_per_share = max(stock_price_expiration - strike_price, 0)

# Step 2: Calculate total shares
total_shares = num_contracts * shares_per_contract

# Step 3: Calculate total payoff
total_payoff = intrinsic_value_per_share * total_shares

total_payoff  # 8 * 1500 = 12000
```

**Common Bugs to Avoid:**
- Assuming standard quantities (1 contract, 100 shares) when prior question specifies different amounts
- Treating cross-referenced questions as standalone problems
- Using default values when explicit values exist in referenced question
- Failing to check if current question overrides prior assumptions

---

## Pattern: Missing Parameter Recognition

**Description:** Before applying complex models (Black-Scholes, CAPM, etc.), verify ALL required parameters are explicitly provided or derivable. Do not assume standard values for critical inputs without explicit justification or recognition of the limitation.

**When to Use:** Questions requiring multi-parameter models (option pricing, CAPM, DCF); especially when OCR data may be incomplete or parameters seem missing.

**Procedure:**
1. List ALL required parameters for the model/formula
2. Check each parameter against provided data (context, tables, OCR)
3. If parameter is missing: (a) check if derivable from other data, (b) check if stated as assumption, (c) flag as missing
4. Only proceed if all critical parameters are available or explicitly assumable
5. Document any assumptions made with clear comments

**Code Example:**

**Scenario:** Calculate Black-Scholes call option value. Given: S=$100, K=$95, T=0.25 years, σ=0.35. Risk-free rate not provided.

**Correct Code:**
```python
import math
from scipy.stats import norm

# Given parameters
S = 100  # Stock price
K = 95   # Strike price
T = 0.25 # Time to maturity (years)
sigma = 0.35  # Volatility

# Check for risk-free rate
r = None  # NOT PROVIDED IN QUESTION

# CRITICAL CHECK: Verify all required parameters
required_params = {
    'S': S,
    'K': K, 
    'T': T,
    'sigma': sigma,
    'r': r
}

missing_params = [name for name, val in required_params.items() if val is None]

if missing_params:
    # STOP: Cannot proceed without critical parameter
    error_message = f"Cannot calculate: missing required parameter(s): {missing_params}"
    # In actual implementation, should raise error or return None
    # For demonstration:
    result = None
    print(error_message)
else:
    # Proceed with Black-Scholes calculation
    d1 = (math.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*math.sqrt(T))
    d2 = d1 - sigma*math.sqrt(T)
    call_value = S*norm.cdf(d1) - K*math.exp(-r*T)*norm.cdf(d2)
    result = call_value

result
```

**Common Bugs to Avoid:**
- Assuming "standard" values (e.g., r=5%) without justification
- Proceeding with calculations when critical inputs are missing
- Not checking if missing parameters can be derived from other given data
- Ignoring OCR extraction errors that may hide provided parameters

---

## Pattern: Exchange Ratio Calculation in Mergers

**Description:** In merger problems without explicitly stated exchange terms, shares are exchanged at the ratio of market prices per share (Price_B/Price_A), not at the ratio of total market capitalizations. This determines new shares issued.

**When to Use:** Merger/acquisition questions asking for post-merger EPS, shares outstanding, or dilution where exchange ratio is not explicitly stated; keywords: "merger," "acquisition," "shares exchanged."

**Procedure:**
1. Formula: Exchange Ratio = Price_Target / Price_Acquirer (shares of acquirer per share of target)
2. Extract price per share for both firms (not total market cap)
3. Calculate exchange ratio = Target_Price / Acquirer_Price
4. New shares issued = Target_Shares_Outstanding × Exchange_Ratio
5. Total shares post-merger = Acquirer_Shares + New_Shares_Issued
6. Post-merger EPS = Combined_Earnings / Total_Shares_Post_Merger

**Code Example:**

**Scenario:** Firm A (acquirer) has 1,000 shares at $80/share, earnings $8,000. Firm B (target) has 400 shares at $20/share, earnings $2,400. Calculate post-merger EPS.

**Correct Code:**
```python
# Firm A (Acquirer)
shares_A = 1000
price_A = 80
earnings_A = 8000

# Firm B (Target)
shares_B = 400
price_B = 20
earnings_B = 2400

# Step 1: Calculate exchange ratio (shares of A per share of B)
# CORRECT: Use price ratio, not market cap ratio
exchange_ratio = price_B / price_A  # 20/80 = 0.25

# Step 2: Calculate new shares issued by A
new_shares_issued = shares_B * exchange_ratio  # 400 * 0.25 = 100

# Step 3: Total shares outstanding post-merger
total_shares_post_merger = shares_A + new_shares_issued  # 1000 + 100 = 1100

# Step 4: Combined earnings
combined_earnings = earnings_A + earnings_B  # 8000 + 2400 = 10400

# Step 5: Post-merger EPS
eps_post_merger = combined_earnings / total_shares_post_merger  # 10400/1100 = 9.45

eps_post_merger
```

**Common Bugs to Avoid:**
- Using market cap ratio instead of price ratio: (shares_B × price_B)/(shares_A × price_A)
- Inverting the exchange ratio (using price_A/price_B)
- Forgetting to add newly issued shares to acquirer's original shares
- Assuming 1:1 exchange when prices differ

---

## Pattern: Merger NPV with Premium Extraction

**Description:** Merger NPV equals synergistic benefits minus the premium paid over target's market value. When a question references prior conditions for premium/terms, those must be retrieved; never assume zero premium (acquisition at market value).

**When to Use:** Merger questions asking for NPV to acquirer/bidder; keywords: "NPV of merger," "value to bidder," "net gain," especially with cross-references to prior questions.

**Procedure:**
1. Formula: NPV_to_Bidder = Synergies - Premium_Paid
2. Calculate target's current market value = Shares_Target × Price_Target
3. Extract or calculate acquisition price (from referenced question or stated terms)
4. Premium = Acquisition_Price - Market_Value_Target
5. NPV = Synergies - Premium
6. Verify: if NPV = Synergies, implies zero premium (likely error unless explicitly stated)

**Code Example:**

**Scenario:** Target firm has 2,000 shares at $30/share (market value $60,000). Synergies estimated at $15,000. Bidder offers $35/share. Calculate NPV to bidder.

**Correct Code:**
```python
# Target firm data
shares_target = 2000
price_per_share_target = 30
market_value_target = shares_target * price_per_share_target  # 60,000

# Acquisition terms
offer_price_per_share = 35  # From question or referenced prior question
total_acquisition_cost = shares_target * offer_price_per_share  # 70,000

# Synergies
synergies = 15000

# Step 1: Calculate premium paid over market value
premium_paid = total_acquisition_cost - market_value_target  # 70,000 - 60,000 = 10,000

# Step 2: Calculate NPV to bidder
# NPV = Value gained (synergies) - Cost (premium over market)
npv_to_bidder = synergies - premium_paid  # 15,000 - 10,000 = 5,000

# Verification check
if npv_to_bidder == synergies:
    # Warning: This implies zero premium, verify acquisition terms
    print("WARNING: NPV equals synergies, implying zero premium paid")

npv_to_bidder
```

**Common Bugs to Avoid:**
- Setting NPV = Synergies (ignores premium paid)
- Forgetting to retrieve acquisition terms from referenced questions
- Using market value as acquisition cost (assumes no premium)
- Calculating premium as percentage instead of absolute dollar amount

---

## Pattern: Constraint Hierarchy and Override Rules

**Description:** When explicit problem-specific constraints ("Assume that...", "Given that...") conflict with general context parameters, the explicit constraint takes precedence and overrides the general setup.

**When to Use:** Questions with "Assume that" or "Given that" statements that introduce parameters already mentioned in context; especially common in multi-part problems where assumptions change.

**Procedure:**
1. Parse question for explicit constraint keywords: "Assume," "Given," "Suppose," "If"
2. Extract parameters from explicit constraints
3. Extract parameters from general context
4. For each parameter: explicit constraint > current question > general context
5. Document which source was used for each critical parameter
6. Flag any overrides in comments

**Code Example:**

**Scenario:** Context states: "Portfolio dividend yield is 3% annually." Question asks: "Assume the portfolio dividend yield is 5%. Calculate the forward price for 1-year delivery if spot is $100 and risk-free rate is 4%."

**Correct Code:**
```python
import math

# General context parameters
context_dividend_yield = 0.03  # 3% from context

# Current question parameters
spot_price = 100
risk_free_rate = 0.04  # 4%
time_to_maturity = 1.0  # 1 year

# EXPLICIT CONSTRAINT from question (overrides context)
dividend_yield = 0.05  # "Assume the portfolio dividend yield is 5%"
# NOT using context_dividend_yield = 0.03

# Document the override
# OVERRIDE: Using dividend_yield=5% from explicit assumption,
# not context value of 3%

# Step 1: Calculate forward price
# Formula: F = S * e^((r - q) * T)
forward_price = spot_price * math.exp((risk_free_rate - dividend_yield) * time_to_maturity)

# Verification: forward should be less than spot when q > r
# 5% > 4%, so forward < spot ✓

forward_price  # 100 * e^(-0.01) ≈ 99.00
```

**Common Bugs to Avoid:**
- Using context parameters when question explicitly overrides them
- Not recognizing "Assume that" as a constraint override signal
- Applying general setup values to specific sub-questions with different assumptions
- Missing constraint keywords buried in question text

---

## Pattern: Perfect Markets Constraint Recognition

**Description:** "Perfect markets" or "assuming no market segmentation" is a constraint that implies full integration (correlation = 1.0 with global market), overriding any narrative discussion of segmentation or partial integration models like Singer-Terhaar.

**When to Use:** Asset pricing questions with "perfect markets," "no segmentation," "fully integrated" constraints; especially when context discusses segmentation but question assumes otherwise.

**Procedure:**
1. Scan question for market assumption keywords: "perfect markets," "fully integrated," "no segmentation"
2. If found: use standard formulas (beta = Cov/Var, not correlation-adjusted)
3. If not found but segmentation discussed: check for integration parameter (ρ or degree of integration)
4. Apply appropriate formula based on constraint, not narrative context
5. Document which assumption was applied

**Code Example:**

**Scenario:** Context discusses partial segmentation with ρ=0.40. Question asks: "Assuming perfect markets, calculate beta if Cov(asset, market)=0.0080 and Var(market)=0.0100."

**Correct Code:**
```python
# Context information (narrative discussion)
context_correlation = 0.40  # Discussed for segmented market case
context_std_asset = 0.15
context_std_market = 0.10

# Question data
covariance_asset_market = 0.0080
variance_market = 0.0100

# CONSTRAINT: "Assuming perfect markets"
# Perfect markets => Full integration => Use standard beta formula
# NOT Singer-Terhaar: beta = ρ × (σ_asset / σ_market)

# Step 1: Identify constraint
perfect_markets = True  # From "Assuming perfect markets"

if perfect_markets:
    # Standard beta formula for fully integrated markets
    beta = covariance_asset_market / variance_market
else:
    # Singer-Terhaar for segmented markets (NOT USED HERE)
    beta_segmented = context_correlation * (context_std_asset / context_std_market)
    beta = beta_segmented

# Result
beta  # 0.0080 / 0.0100 = 0.80
```

**Common Bugs to Avoid:**
- Using segmentation formulas (Singer-Terhaar) when "perfect markets" is stated
- Prioritizing narrative context over explicit question constraints
- Applying correlation adjustments when full integration is assumed
- Missing "perfect markets" constraint buried in question preamble

---

## Pattern: Leverage-Adjusted Portfolio Value

**Description:** When a question states "assuming no leverage" or "unleveraged," the portfolio value for calculations must be the equity value (assets - liabilities), not the total leveraged asset value shown in balance sheets.

**When to Use:** Portfolio hedging, duration matching, or risk calculations with "no leverage," "unleveraged," or "equity value" constraints; especially when balance sheet shows both assets and liabilities.

**Procedure:**
1. Extract total assets and total liabilities from balance sheet/exhibit
2. Check for leverage constraint: "no leverage," "unleveraged," "equity basis"
3. If constraint present: Portfolio_Value = Assets - Liabilities (equity value)
4. If constraint absent: Portfolio_Value = Assets (leveraged value)
5. Use adjusted portfolio value for all subsequent calculations (duration hedging, contract sizing, etc.)

**Code Example:**

**Scenario:** Balance sheet shows Assets=$500M, Liabilities=$300M. Question asks: "Assuming no leverage is used, how many futures contracts (each worth $100,000 with duration 6) are needed to reduce portfolio duration from 8 to 5?"

**Correct Code:**
```python
# Balance sheet data
total_assets = 500_000_000  # $500M
total_liabilities = 300_000_000  # $300M

# CONSTRAINT: "Assuming no leverage is used"
use_leverage = False

# Step 1: Determine portfolio value based on constraint
if use_leverage:
    portfolio_value = total_assets  # Leveraged value
else:
    # CORRECT: Use equity value when no leverage
    portfolio_value = total_assets - total_liabilities  # $200M

# Portfolio duration parameters
current_duration = 8
target_duration = 5
duration_change_needed = current_duration - target_duration  # 3

# Futures contract parameters
futures_contract_value = 100_000
futures_duration = 6

# Step 2: Calculate dollar duration to hedge
dollar_duration_to_hedge = portfolio_value * duration_change_needed

# Step 3: Calculate dollar duration per contract
dollar_duration_per_contract = futures_contract_value * futures_duration

# Step 4: Number of contracts
num_contracts = dollar_duration_to_hedge / dollar_duration_per_contract

num_contracts  # (200M * 3) / (100K * 6) = 1000
```

**Common Bugs to Avoid:**
- Using total assets when "no leverage" constraint is stated
- Ignoring liabilities in equity value calculation
- Applying leverage constraint inconsistently across multi-step problems
- Confusing "no leverage" with "no borrowing" (different concepts)

---

## Pattern: Multi-Factor Beta Decomposition

**Description:** When portfolio beta or risk must be calculated from factor sensitivities in a multi-factor model, use the factor loadings (sensitivities) directly, not total variance decomposition, unless specifically asked for variance.

**When to Use:** Questions providing factor sensitivities/loadings (β₁, β₂) and asking for "beta" or "systematic risk exposure"; keywords: "factor sensitivities," "factor loadings," "multi-factor model."

**Procedure:**
1. Identify if question asks for: (a) beta/systematic exposure, or (b) total variance/risk
2. For beta to primary factor (e.g., market): use the factor loading directly
3. For total systematic variance: Var = Σ(βᵢ² × Var(Fᵢ)) + Σ(2βᵢβⱼ × Cov(Fᵢ,Fⱼ)) + Residual²
4. Do not confuse factor sensitivity (beta) with variance contribution
5. If question asks for "beta" without qualification, use primary factor loading

**Code Example:**

**Scenario:** Asset has global equity sensitivity 0.70, global bond sensitivity 0.25. Question asks: "What is the asset's beta?" (Assume equity is primary factor)

**Correct Code:**
```python
# Factor sensitivities (loadings)
equity_sensitivity = 0.70  # Beta to global equity factor
bond_sensitivity = 0.25    # Beta to global bond factor
residual_risk = 0.05       # Idiosyncratic risk (standard deviation)

# Additional data (for variance calculation if needed)
variance_equity_factor = 0.0225  # Var of equity factor
variance_bond_factor = 0.0016    # Var of bond factor
correlation_equity_bond = 0.30

# Question asks: "What is the asset's beta?"
# INTERPRETATION: Beta typically refers to primary market factor (equity)

# CORRECT: Use factor sensitivity directly
beta = equity_sensitivity  # 0.70

# WRONG APPROACH: Calculating total variance and deriving beta
# (Only do this if question specifically asks for total risk/variance)
covariance_equity_bond = (correlation_equity_bond * 
                          (variance_equity_factor ** 0.5) * 
                          (variance_bond_factor ** 0.5))

total_variance = (equity_sensitivity**2 * variance_equity_factor +
                  bond_sensitivity**2 * variance_bond_factor +
                  2 * equity_sensitivity * bond_sensitivity * covariance_equity_bond +
                  residual_risk**2)

# But for "beta" question, return the factor loading
beta  # 0.70
```

**Common Bugs to Avoid:**
- Calculating total variance when question asks for beta
- Using weighted average of factor sensitivities without justification
- Confusing factor loading (beta) with variance contribution
- Not identifying which factor is the "market" or primary factor

---

## Pattern: Annualization with Partial Period Adjustments

**Description:** When converting periodic rates to annual rates or vice versa, account for both the rate period and any time delays before the rate applies. For loans initiated in the future, separate the waiting period from the loan period.

**When to Use:** Interest rate calculations with future start dates, forward rates, or delayed settlements; keywords: "in X days," "effective annual rate," "loan starts in."

**Procedure:**
1. Identify the rate period (e.g., 180-day rate)
2. Identify any delay before rate applies (e.g., "in 60 days")
3. For effective annual rate: EAR = (1 + periodic_rate)^(365/rate_period) - 1
4. Do NOT compound over the delay period unless explicitly calculating forward value
5. The delay affects when the rate is determined, not the annualization formula

**Code Example:**

**Scenario:** In 30 days, a company will borrow at 90-day LIBOR + 1.0%. The 90-day LIBOR in 30 days is expected to be 2.8%. Calculate the effective annual borrowing rate.

**Correct Code:**
```python
import math

# Timing parameters
delay_days = 30  # Loan starts in 30 days
loan_period_days = 90  # 90-day loan

# Rate parameters
libor_90day = 0.028  # 2.8% (the rate in 30 days)
spread = 0.010  # 1.0%

# Step 1: Calculate the periodic rate for the 90-day loan
periodic_rate = libor_90day + spread  # 3.8%

# Step 2: Annualize the 90-day rate
# CORRECT: Annualize based on loan period (90 days), not total time (30+90)
effective_annual_rate = (1 + periodic_rate) ** (365 / loan_period_days) - 1

# WRONG: (1 + periodic_rate) ** (365 / (delay_days + loan_period_days)) - 1
# The delay affects when the rate is set, not the annualization

effective_annual_rate  # (1.038)^(365/90) - 1 ≈ 0.1608 or 16.08%
```

**Common Bugs to Avoid:**
- Including delay period in annualization denominator: 365/(delay + loan_period)
- Confusing rate determination date with rate application period
- Compounding over delay period when calculating effective rate
- Using 360-day convention when 365-day is standard (or vice versa without justification)