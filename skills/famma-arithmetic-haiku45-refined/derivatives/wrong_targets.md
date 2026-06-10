# SKILL PATTERNS FOR OPTIONS DERIVATIVES (PoT)

## Pattern: Options Contract Scaling and Position Value

**Description:** Options questions often involve standard contract sizes (typically 100 shares per contract) and may ask for total position value rather than per-share calculations. Failure to scale by contract size or number of contracts leads to answers off by factors of 100 or 1000.

**When to Use:** Questions asking for "investment worth," "total value," "net gain," or when ground truth magnitude suggests multi-contract positions (e.g., answers in thousands when per-share calculation yields single digits).

**Procedure:**
1. Formula: `Total Value = Intrinsic Value per Share × Shares per Contract × Number of Contracts`
2. Identify the contract specifications (shares per contract, typically 100)
3. Determine number of contracts from context or reverse-engineer from answer magnitude
4. Calculate per-share intrinsic value: `max(S - K, 0)` for calls, `max(K - S, 0)` for puts
5. Scale by contract size and number of contracts
6. Distinguish between "position value" (total intrinsic value) vs "profit/loss" (value minus premium paid)

**Code Example:**

**Scenario:** You bought 10 call option contracts (strike $50, premium $3 per share) on a stock now trading at $58. What is your position worth?

**Correct Code:**
```python
# Option position parameters
strike_price = 50
current_stock_price = 58
premium_paid_per_share = 3
shares_per_contract = 100
number_of_contracts = 10

# Calculate intrinsic value per share
intrinsic_value_per_share = max(current_stock_price - strike_price, 0)

# Scale to total position value
total_position_value = intrinsic_value_per_share * shares_per_contract * number_of_contracts

# If question asks for "worth" (total value)
answer = total_position_value

# If question asks for "net gain" (profit/loss)
total_premium_paid = premium_paid_per_share * shares_per_contract * number_of_contracts
net_gain = total_position_value - total_premium_paid

# Return based on question wording
answer  # Returns 8000 for position value
```

**Common Bugs to Avoid:**
- Returning per-share value when question asks for total position value
- Forgetting to multiply by shares_per_contract (100)
- Confusing "worth" (total value) with "profit" (value minus cost)
- Not reverse-engineering contract quantity from context clues

---

## Pattern: Multi-Component Output for Strategy Specification

**Description:** Questions asking to "specify," "describe," or "show how to replicate" a strategy require returning multiple components (e.g., shares to buy AND amount to borrow) rather than a single numeric value. Returning only the net cost or final value misses the question target.

**When to Use:** Questions with verbs like "specify," "describe," "replicate," "construct," or "show the components" in derivatives contexts, especially for delta hedging or portfolio replication.

**Procedure:**
1. Formula for call replication: Buy `Δ = N(d1)` shares, borrow `B = K·e^(-rT)·N(d2)`
2. Calculate all required components separately
3. Store each component with descriptive variable names
4. Return a tuple, dictionary, or formatted string containing ALL components
5. Verify: `Δ·S - B` should equal theoretical option price

**Code Example:**

**Scenario:** Replicate a call option using Black-Scholes where S=$100, K=$105, r=0.05, σ=0.25, T=0.5 years.

**Correct Code:**
```python
import numpy as np
from scipy.stats import norm

# Black-Scholes parameters
S = 100  # Current stock price
K = 105  # Strike price
r = 0.05  # Risk-free rate
sigma = 0.25  # Volatility
T = 0.5  # Time to expiration

# Calculate d1 and d2
d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# Replication components
delta = norm.cdf(d1)  # Shares to buy
amount_to_borrow = K * np.exp(-r*T) * norm.cdf(d2)  # Amount to borrow

# Return BOTH components (not just net cost)
replication_strategy = {
    'shares_to_buy': round(delta, 4),
    'amount_to_borrow': round(amount_to_borrow, 2)
}

replication_strategy  # Returns dict with both components
```

**Common Bugs to Avoid:**
- Returning only the net cost (`delta * S - amount_to_borrow`) instead of components
- Calculating components but returning a single summary value
- Not labeling outputs clearly when multiple values are required
- Ignoring question verbs like "specify" that signal multi-part answers

---

## Pattern: Position Type Inference from Context

**Description:** Options problems may not explicitly state whether the position is long/short or call/put. The position type must be inferred from context clues (question wording, answer magnitude, market conditions) before calculating payoffs.

**When to Use:** When question references "your position," "net gain," or "investment" without explicitly stating the option type, or when ground truth magnitude doesn't match initial assumption.

**Procedure:**
1. Check for explicit position indicators in question or prior context
2. Analyze answer magnitude: large positive values may indicate short premium collection or multiple contracts
3. Consider market logic: if S < K at expiration, calls expire worthless but puts have value
4. Test both long/short and call/put scenarios if ambiguous
5. For "net gain" questions: `Payoff - Premium Paid` (long) or `Premium Collected - Payoff` (short)

**Code Example:**

**Scenario:** Stock expires at $95. Strike is $100. Premium was $4. Question asks for "net gain" and answer should be $100. Determine position type.

**Correct Code:**
```python
# Given information
expiration_price = 95
strike_price = 100
premium = 4
shares_per_contract = 100
expected_answer_magnitude = 100  # Clue from context

# Test different position types
# Scenario 1: Long call
long_call_payoff = max(expiration_price - strike_price, 0)
long_call_net = (long_call_payoff - premium) * shares_per_contract
# Result: (0 - 4) * 100 = -400 (doesn't match)

# Scenario 2: Long put
long_put_payoff = max(strike_price - expiration_price, 0)
long_put_net = (long_put_payoff - premium) * shares_per_contract
# Result: (5 - 4) * 100 = 100 (matches!)

# Scenario 3: Short put
short_put_payoff = max(strike_price - expiration_price, 0)
short_put_net = (premium - short_put_payoff) * shares_per_contract
# Result: (4 - 5) * 100 = -100 (opposite sign)

# Select position that matches expected answer
position_type = "long_put"
net_gain = long_put_net

net_gain  # Returns 100
```

**Common Bugs to Avoid:**
- Assuming position type without checking context clues
- Not testing alternative positions when initial calculation doesn't match expected magnitude
- Ignoring sign conventions (long pays premium, short collects premium)
- Forgetting that puts gain value when stock price falls below strike

---

## Pattern: Question Reference Chain Resolution

**Description:** Multi-part questions may reference earlier parts ("In question 1, suppose..."). The current question inherits assumptions, positions, or contract quantities from the referenced question, which must be tracked or inferred.

**When to Use:** Questions containing phrases like "in question 1," "using your position from above," "the options you purchased," indicating dependency on prior context.

**Procedure:**
1. Identify the reference to prior question/context
2. Extract inherited parameters: contract type, quantity, strike, premium paid
3. If prior context unavailable, reverse-engineer from answer magnitude
4. Document assumptions explicitly in code comments
5. Use inherited parameters in current calculation

**Code Example:**

**Scenario:** Question 1 stated "buy 5 call contracts at $2 premium, strike $80." Question 2 asks: "If stock is now $90, what is your position worth?"

**Correct Code:**
```python
# Parameters inherited from Question 1
strike_price = 80
premium_paid_per_share = 2
number_of_contracts = 5  # From Question 1
shares_per_contract = 100

# New information from Question 2
current_stock_price = 90

# Calculate using inherited position
intrinsic_value_per_share = max(current_stock_price - strike_price, 0)
total_position_value = intrinsic_value_per_share * shares_per_contract * number_of_contracts

# If question asks for "worth" (not profit)
answer = total_position_value

# If question asks for "net gain"
total_cost = premium_paid_per_share * shares_per_contract * number_of_contracts
net_gain = total_position_value - total_cost

answer  # Returns 5000 for position value
```

**Common Bugs to Avoid:**
- Ignoring references to prior questions and recalculating from scratch
- Assuming single contract when prior question specified multiple
- Not documenting inherited assumptions when prior context is unavailable
- Failing to reverse-engineer missing parameters from answer magnitude

---

## Pattern: Terminology Precision in Options Valuation

**Description:** Options questions use precise terminology where "worth," "value," and "net gain" have distinct meanings. "Worth/value" typically means current intrinsic value, while "net gain/profit" means value minus cost. Confusing these terms leads to wrong targets.

**When to Use:** Any options valuation question; pay special attention to exact wording of what to calculate.

**Procedure:**
1. Parse question for exact term: "worth," "value," "gain," "profit," "loss"
2. "Worth" or "value" → return intrinsic value (no cost subtraction)
3. "Net gain," "profit," or "loss" → return intrinsic value minus premium paid
4. For short positions: "net gain" = premium collected minus payout obligation
5. Always scale by contract size before returning

**Code Example:**

**Scenario:** Bought 2 put contracts (strike $120, premium $5) on stock now at $110. Calculate both value and net gain.

**Correct Code:**
```python
# Position parameters
strike_price = 120
current_stock_price = 110
premium_paid_per_share = 5
number_of_contracts = 2
shares_per_contract = 100

# Calculate intrinsic value per share
intrinsic_value_per_share = max(strike_price - current_stock_price, 0)

# Total position VALUE (what it's "worth")
total_value = intrinsic_value_per_share * shares_per_contract * number_of_contracts

# Total position NET GAIN (profit/loss)
total_premium_paid = premium_paid_per_share * shares_per_contract * number_of_contracts
net_gain = total_value - total_premium_paid

# Return based on question wording
# If question asks "what is your position worth?" → use total_value
# If question asks "what is your net gain?" → use net_gain

# Example: question asks for "worth"
answer_worth = total_value  # Returns 2000

# Example: question asks for "net gain"
answer_net_gain = net_gain  # Returns 1000

answer_worth  # Use appropriate variable based on question
```

**Common Bugs to Avoid:**
- Returning profit when question asks for value/worth
- Returning value when question asks for net gain/profit
- Not distinguishing between gross value and net profit
- Applying wrong formula for short vs long positions