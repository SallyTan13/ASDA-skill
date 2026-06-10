# Derivatives — Merton Model Debt Valuation

## CODE CONSTRAINTS (MANDATORY)

**Your generated code MUST:**
- ✅ End with variable name or expression (for eval() to capture)
- ✅ Include ALL necessary imports at the top
- ✅ Define ALL variables before use
- ✅ Use explicit values from the question

**Your generated code MUST NOT:**
- ❌ Use input() or any interactive functions
- ❌ Use print() as the last line (returns None)
- ❌ Use variables without defining them first

**Available libraries (must import if used):**
- import math
- import numpy as np
- from scipy.stats import norm
- from scipy.optimize import brentq

## Pattern: Risky Debt Valuation Using Merton Model

**Description:** Values risky corporate debt using the Merton structural model, where equity is treated as a call option on firm assets with strike price equal to debt face value. Debt value is derived as the difference between total firm value and equity value, or by directly pricing debt as a risk-free bond minus a put option on firm assets.

**When to Use:**
- Question provides firm value, equity value, debt face value, and volatility measures
- Asked to find market value of risky debt (not book value)
- Context involves option-theoretic approach to capital structure
- Given firm volatility or equity volatility with leverage information
- No discrete state probabilities provided (continuous distribution assumed)

**Procedure:**
1. **Identify given parameters:**
   - V = Total firm value (market value of assets)
   - E = Market value of equity
   - F = Face value of debt (strike price)
   - T = Time to maturity of debt
   - r = Risk-free rate
   - σ_V = Firm volatility OR σ_E = Equity volatility

2. **If only equity volatility is given, derive firm volatility:**
   - Use iterative approach or the relationship: σ_E = (V/E) × N(d1) × σ_V
   - Alternatively, if leverage is low, approximate: σ_V ≈ (E/V) × σ_E

3. **Calculate d1 and d2 for Black-Scholes framework:**
   - d1 = [ln(V/F) + (r + 0.5×σ_V²)×T] / (σ_V × √T)
   - d2 = d1 - σ_V × √T

4. **Value equity as call option on firm assets:**
   - E_theoretical = V × N(d1) - F × e^(-r×T) × N(d2)
   - (If E is given, this serves as validation)

5. **Calculate debt value:**
   - **Method 1 (Direct):** D = V - E
   - **Method 2 (Put-Call Parity):** D = F × e^(-r×T) - Put_value
   - Where Put_value = F × e^(-r×T) × N(-d2) - V × N(-d1)
   - Equivalently: D = V × N(d1) + F × e^(-r×T) × N(-d2)

6. **Validate results:**
   - Debt value should be less than face value for risky debt
   - Debt value should be less than firm value
   - E + D should equal V

**Worked Example:**

**Question:** A firm has total assets worth $15,000 million and equity valued at $6,500 million. The face value of zero-coupon debt maturing in 3 years is $10,000 million. The firm's asset volatility is 25% per year, and the risk-free rate is 4%. What is the market value of the debt?

```python
import math
from scipy.stats import norm

# Given parameters
V = 15000  # Firm value (million)
E = 6500   # Equity market value (million)
F = 10000  # Face value of debt (million)
T = 3      # Time to maturity (years)
sigma_V = 0.25  # Firm volatility
r = 0.04   # Risk-free rate

# Calculate d1 and d2
d1 = (math.log(V / F) + (r + 0.5 * sigma_V**2) * T) / (sigma_V * math.sqrt(T))
d2 = d1 - sigma_V * math.sqrt(T)

# Value equity as call option (for validation)
N_d1 = norm.cdf(d1)
N_d2 = norm.cdf(d2)
E_theoretical = V * N_d1 - F * math.exp(-r * T) * N_d2

# Calculate debt value using Method 1 (most direct)
D = V - E

# Alternative: Method 2 using put-call parity (validation)
D_alternative = V * N_d1 + F * math.exp(-r * T) * (1 - N_d2)

# Return debt value
D
```

**Common Bugs to Avoid:**
- **Using improvised credit spread formulas** — Don't create ad-hoc formulas like `spread = leverage × volatility × correlation`. Use proper Merton model framework.
- **Forgetting to convert equity volatility to firm volatility** — If given σ_E, must derive σ_V using the relationship σ_E = (V/E) × N(d1) × σ_V (requires iteration or approximation).
- **Using book value instead of market value** — Merton model requires market values for V and E, not accounting values.
- **Incorrect d1/d2 calculation** — Ensure ln(V/F) not ln(F/V), and use firm volatility not equity volatility.
- **Valuing debt as risk-free** — Don't use D = F × e^(-r×T); this ignores default risk.
- **Sign errors in put-call parity** — Remember: D = F×e^(-rT) - [F×e^(-rT)×N(-d2) - V×N(-d1)]

**CHECK Steps:**
- If debt value > face value, verify calculation (should only occur if r < 0 or extreme parameters)
- Assert D < V (debt cannot exceed total firm value)
- Assert D < F for typical risky debt (market value below face value due to default risk)
- If E is given, verify V = E + D (balance sheet identity)
- If equity volatility is used, check that derived firm volatility is lower: σ_V < σ_E (leverage amplifies equity risk)
- Validate that N(d1) and N(d2) are between 0 and 1
- If T is very small or V >> F, debt value should approach F×e^(-r×T) (low default risk)

---

## Pattern: Terminal Value with Return on Capital Constraints

**Description:** Calculates terminal value in DCF models when the terminal period has an explicit return on capital (ROC) constraint. The sustainable growth rate and ROC together determine the reinvestment rate, which affects free cash flow available for distribution.

**When to Use:**
- DCF valuation with explicit terminal growth rate AND return on capital
- Question states "return on capital is X% after year N"
- Need to calculate terminal value with growth constraints
- Given both WACC and ROC in terminal period
- Terminal FCFF cannot be derived by simply growing prior year FCFF

**Procedure:**
1. **Identify terminal period parameters:**
   - g = Terminal growth rate (perpetual)
   - ROC = Return on capital in terminal period
   - WACC = Weighted average cost of capital
   - Year N operating income or NOPAT

2. **Calculate implied reinvestment rate:**
   - Reinvestment Rate = g / ROC
   - This is the fraction of NOPAT that must be reinvested to achieve growth g

3. **Determine terminal period NOPAT:**
   - If given directly, use it
   - If given operating income: NOPAT = Operating Income × (1 - Tax Rate)
   - If need to project: NOPAT_terminal = NOPAT_N × (1 + g)

4. **Calculate terminal free cash flow:**
   - FCFF_terminal = NOPAT_terminal × (1 - Reinvestment Rate)
   - Equivalently: FCFF_terminal = NOPAT_terminal × (1 - g/ROC)
   - This represents cash available after required reinvestment

5. **Calculate terminal value:**
   - TV = FCFF_terminal / (WACC - g)
   - This is the value at the START of the terminal period

6. **Discount to present value:**
   - PV(TV) = TV / (1 + WACC)^N
   - Add to PV of explicit forecast period cash flows

**Worked Example:**

**Question:** A company has Year 5 NOPAT of $800 million. After Year 5, the company will grow at 4% perpetually with a return on capital of 12%. The WACC is 9% and tax rate is 30%. What is the terminal value at the end of Year 5?

```python
# Given parameters
NOPAT_5 = 800  # Year 5 NOPAT (million)
g = 0.04       # Terminal growth rate
ROC = 0.12     # Return on capital in terminal period
WACC = 0.09    # Weighted average cost of capital

# Calculate reinvestment rate
reinvestment_rate = g / ROC

# Calculate Year 6 NOPAT (first year of terminal period)
NOPAT_6 = NOPAT_5 * (1 + g)

# Calculate terminal FCFF (Year 6)
FCFF_terminal = NOPAT_6 * (1 - reinvestment_rate)

# Calculate terminal value at end of Year 5
TV = FCFF_terminal / (WACC - g)

# Return terminal value
TV
```

**Common Bugs to Avoid:**
- **Growing Year N FCFF directly at g** — This ignores that reinvestment needs change with ROC. Must calculate NOPAT first, then apply reinvestment rate.
- **Using wrong year for NOPAT** — Terminal value formula uses Year N+1 cash flow (first year of perpetuity), not Year N.
- **Forgetting to apply (1 + g) to NOPAT** — If given Year 5 NOPAT, Year 6 NOPAT = Year 5 × (1 + g).
- **Confusing ROC with ROIC or ROE** — Return on Capital is specifically return on invested capital, not equity.
- **Using reinvestment rate from forecast period** — Terminal period reinvestment rate = g/ROC may differ from explicit forecast period.
- **Incorrect perpetuity formula** — TV = CF / (WACC - g), not CF / WACC.

**CHECK Steps:**
- Assert reinvestment_rate < 1 (cannot reinvest more than 100% of NOPAT)
- Assert g < ROC (growth cannot exceed return on capital sustainably)
- Assert g < WACC (growth must be less than discount rate for finite value)
- If ROC = WACC, verify that value creation logic is consistent
- Validate that FCFF_terminal > 0 (positive free cash flow)
- Check that terminal value is reasonable relative to explicit period cash flows
- If reinvestment_rate > 0.5, verify this makes economic sense (high growth scenario)

---

## Pattern: Option Position Inference from Context

**Description:** Determines the specific option position (long/short call/put, combinations, number of contracts) from contextual clues when not explicitly stated. Uses question wording, payoff patterns, and given data to infer the position.

**When to Use:**
- Question asks "your profit/loss" or "your net gain" without stating position
- Given option premiums and expiration prices but position unclear
- Need to work backwards from payoff to determine position
- Multiple option types mentioned but specific position ambiguous
- Question provides partial information requiring position inference

**Procedure:**
1. **Scan for explicit position indicators:**
   - Words like "you bought", "you sold", "you wrote", "you hold"
   - If found, use explicit position directly

2. **Check for implicit clues:**
   - "You paid premium" → Long position
   - "You received premium" → Short position
   - "Maximum loss is limited" → Long position or spread
   - "Unlimited upside" → Long call or short put

3. **Analyze given data for position hints:**
   - If only call premium given → likely call position
   - If only put premium given → likely put position
   - If both given → likely combination (straddle, strangle, etc.)
   - If multiple strikes → likely spread strategy

4. **Infer number of contracts:**
   - If payoff is in thousands but premium in dollars → likely 100 shares per contract
   - Standard option contract = 100 shares
   - If result should be in thousands, multiply by contracts × 100

5. **Calculate payoff for inferred position:**
   - Long Call: max(0, S_T - K) - Premium
   - Long Put: max(0, K - S_T) - Premium
   - Short Call: Premium - max(0, S_T - K)
   - Short Put: Premium - max(0, K - S_T)

6. **Validate against expected result magnitude:**
   - If calculated result is off by factor of 100, adjust for contract size
   - If sign is wrong, reconsider long vs short position

**Worked Example:**

**Question:** You are considering options on a stock currently at $100. A call with strike $100 costs $4.50, and a put with strike $100 costs $3.70. At expiration, the stock is at $104. If you bought 100 put contracts, what is your net gain?

```python
# Given parameters
S_0 = 100      # Initial stock price
S_T = 104      # Stock price at expiration
K_put = 100    # Put strike price
put_premium = 3.70  # Premium per share
num_contracts = 100  # Number of contracts
shares_per_contract = 100  # Standard contract size

# Inferred position: Long put (explicitly stated "bought")
# Calculate put payoff per share
put_payoff_per_share = max(0, K_put - S_T)

# Net profit per share
net_per_share = put_payoff_per_share - put_premium

# Total net gain (accounting for contracts and shares)
total_net_gain = net_per_share * num_contracts * shares_per_contract

# Return total net gain
total_net_gain
```

**Common Bugs to Avoid:**
- **Assuming position without evidence** — Don't default to "long straddle" or any position without textual support.
- **Ignoring contract multiplier** — Options typically control 100 shares; forgetting this causes 100× errors.
- **Misinterpreting "your" vs "the"** — "Your gain" implies you hold position; "the gain" might be asking about general payoff.
- **Wrong long/short direction** — "Wrote option" = short, "bought option" = long.
- **Combining positions incorrectly** — If question mentions multiple options, verify whether it's asking about one, both, or a specific combination.
- **Using wrong strike price** — If multiple strikes given, match to the option type being analyzed.

**CHECK Steps:**
- If result magnitude seems off by 100×, verify contract size multiplier
- If result is negative when question implies profit, reconsider position direction
- Assert payoff logic matches option type: calls profit when S_T > K, puts profit when S_T < K
- If question mentions "premium paid", verify it's subtracted from payoff (long position)
- If question mentions "premium received", verify it's added to payoff (short position)
- Cross-check: for long positions, maximum loss = premium paid
- Validate that inferred position is consistent with all given information

---

SKILL_MD_ENTRY: | `derivatives/merton_model_debt_valuation.md` | Derivatives | Merton Model Debt Valuation, Terminal Value with ROC Constraints, Option Position Inference | Risky Debt Valuation Using Merton Model, Terminal Value with Return on Capital Constraints, Option Position Inference from Context |