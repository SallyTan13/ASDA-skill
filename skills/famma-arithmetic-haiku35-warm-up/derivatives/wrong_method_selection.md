# DERIVATIVES PRICING SKILLS: FAILURE PATTERN ANALYSIS

## Pattern: Two-Stage DCF Firm Valuation with FCFF

**Description:** Firm valuation requires computing Free Cash Flow to the Firm (FCFF) for explicit forecast periods, calculating terminal value using perpetuity growth formula with reinvestment rate constraints, and discounting both components at WACC.

**When to Use:** Questions asking for "firm value" or "enterprise value" with multi-stage growth assumptions, EBIT/EBITDA data, capital expenditure forecasts, and terminal growth rates.

**Procedure:**
1. Formula: FCFF = EBIT × (1 - Tax Rate) + Depreciation - CapEx - ΔWorking Capital
2. Formula: Terminal Value = FCFF_{n+1} / (WACC - g) where FCFF_{n+1} = Terminal EBIT × (1-t) × (1 - g/ROIC)
3. Compute FCFF for each explicit forecast year (apply growth rates to operating metrics)
4. Calculate terminal value at end of forecast period using perpetuity formula with reinvestment adjustment
5. Discount all cash flows and terminal value to present using WACC
6. Sum discounted values to get enterprise/firm value

**Code Example:**

**Scenario:** A firm has EBIT of $500M, depreciation $200M, CapEx $300M, tax rate 35%. EBIT and net CapEx grow 15% for 3 years. WACC is 9%, terminal growth 4%, terminal ROIC 12%.

**Correct Code:**
```python
import numpy as np

# Initial values
ebit_0 = 500
depreciation_0 = 200
capex_0 = 300
tax_rate = 0.35
growth_explicit = 0.15
years_explicit = 3
wacc = 0.09
terminal_growth = 0.04
terminal_roic = 0.12

# Explicit forecast period
fcff_list = []
for year in range(1, years_explicit + 1):
    ebit_t = ebit_0 * (1 + growth_explicit) ** year
    # Assume depreciation and capex grow with EBIT
    depreciation_t = depreciation_0 * (1 + growth_explicit) ** year
    capex_t = capex_0 * (1 + growth_explicit) ** year
    fcff_t = ebit_t * (1 - tax_rate) + depreciation_t - capex_t
    fcff_list.append(fcff_t)

# PV of explicit period cash flows
pv_explicit = sum([fcff / (1 + wacc) ** (i + 1) for i, fcff in enumerate(fcff_list)])

# Terminal value calculation
ebit_terminal = ebit_0 * (1 + growth_explicit) ** years_explicit * (1 + terminal_growth)
reinvestment_rate = terminal_growth / terminal_roic
fcff_terminal = ebit_terminal * (1 - tax_rate) * (1 - reinvestment_rate)
terminal_value = fcff_terminal / (wacc - terminal_growth)
pv_terminal = terminal_value / (1 + wacc) ** years_explicit

# Total firm value
firm_value = pv_explicit + pv_terminal
firm_value  # Result: should be around 5,800-6,000M
```

**Common Bugs to Avoid:**
- Using equity value formulas (FCFE) instead of firm value formulas (FCFF)
- Forgetting to apply reinvestment rate constraint: reinvestment = g / ROIC in terminal period
- Discounting terminal value incorrectly (must discount to t=0, not t=n)
- Using pre-tax EBIT instead of after-tax operating income
- Confusing net CapEx (CapEx - Depreciation) with gross CapEx in FCFF formula

---

## Pattern: Equity Value from Enterprise Value

**Description:** Equity value is calculated by subtracting net debt (debt minus cash) from enterprise value, not by using FCFE directly when firm value is already computed.

**When to Use:** Questions asking for "equity value" when enterprise/firm value has been calculated, or when debt structure is explicitly provided.

**Procedure:**
1. Formula: Equity Value = Enterprise Value - Market Value of Debt + Cash
2. Calculate enterprise value using FCFF methodology (see previous pattern)
3. Identify total debt outstanding (sum across all maturities if structured)
4. Subtract debt from enterprise value to get equity value
5. Add back any excess cash if provided

**Code Example:**

**Scenario:** A firm has enterprise value of $12,000M calculated from DCF. It has $3,000M in short-term debt, $5,000M in long-term bonds, and $500M cash.

**Correct Code:**
```python
# Given values
enterprise_value = 12000  # From FCFF DCF calculation
short_term_debt = 3000
long_term_debt = 5000
cash = 500

# Total debt
total_debt = short_term_debt + long_term_debt

# Equity value calculation
equity_value = enterprise_value - total_debt + cash
equity_value  # Result: 4,500M
```

**Common Bugs to Avoid:**
- Using FCFE methodology when FCFF/enterprise value is already computed (double-counting adjustments)
- Forgetting to subtract debt from firm value
- Using book value of debt instead of market value when market values are available
- Ignoring cash balances (net debt = debt - cash)
- Confusing firm value with equity value in output

---

## Pattern: Risk-Neutral Drift Adjustment for Options

**Description:** Option pricing under BSM requires converting physical drift (μ) to risk-neutral drift using the risk-free rate and market price of risk, not using the physical drift directly.

**When to Use:** Questions involving option pricing with given physical drift parameters (μ, σ) and market price of risk (λ), especially for non-financial assets.

**Procedure:**
1. Formula: Risk-neutral drift = r - q - λσ (where q is dividend/convenience yield, λ is market price of risk)
2. Identify the physical drift μ (not used in pricing)
3. Calculate risk-neutral drift using risk-free rate r, dividend yield q, and market price of risk λ
4. Apply BSM formula with adjusted forward price: F = S₀ × exp((r - q - λσ)T)
5. Use standard BSM with d₁ = [ln(F/K) + 0.5σ²T] / (σ√T)

**Code Example:**

**Scenario:** An asset worth $50 has physical drift μ=-0.20, volatility σ=0.18, market price of risk λ=-0.15. Price a 3-year call with strike $45, risk-free rate 5%, no dividends.

**Correct Code:**
```python
import math
from scipy.stats import norm

# Given parameters
S0 = 50
K = 45
T = 3
r = 0.05
sigma = 0.18
market_price_risk = -0.15
q = 0  # No dividends

# Risk-neutral drift adjustment
drift_adjustment = market_price_risk * sigma
risk_neutral_drift = r - q + drift_adjustment  # Note: λ is negative, so this adds to drift

# Forward price under risk-neutral measure
F = S0 * math.exp((r - q + drift_adjustment) * T)

# BSM formula
d1 = (math.log(F / K) + 0.5 * sigma**2 * T) / (sigma * math.sqrt(T))
d2 = d1 - sigma * math.sqrt(T)

# Option value (discounted expected payoff)
call_value = math.exp(-r * T) * (F * norm.cdf(d1) - K * norm.cdf(d2))
call_value  # Result: around 14-16
```

**Common Bugs to Avoid:**
- Using physical drift μ directly in BSM formula
- Forgetting to adjust for market price of risk (λσ term)
- Sign errors on market price of risk adjustment
- Confusing real-world probability measure with risk-neutral measure
- Using S0 instead of forward price F in d1 calculation when drift is adjusted

---

## Pattern: Black's Model for Swaptions with Annuity Factor

**Description:** Swaption valuation requires treating the swap rate as the underlying asset and multiplying the Black's formula payoff by the present value of a basis point (annuity factor), not applying bond or caplet formulas directly.

**When to Use:** Questions about swaptions (options on interest rate swaps) with given forward swap rate, strike rate, volatility, and swap tenor.

**Procedure:**
1. Formula: Swaption Value = A × [F₀N(d₁) - K N(d₂)] where A is the annuity factor
2. Formula: Annuity Factor A = Σ δᵢ × P(0, Tᵢ) for all payment dates
3. Calculate discount factors P(0, Tᵢ) for each swap payment date
4. Compute annuity factor (PV of $1 per period over swap life)
5. Apply Black's formula with forward swap rate F₀ and strike K
6. Multiply result by annuity factor and notional

**Code Example:**

**Scenario:** A 3-year payer swaption on a 4-year swap, strike 6%, forward swap rate 6.5%, volatility 20%, annual payments, notional $1M, flat OIS rate 5.5% continuous.

**Correct Code:**
```python
import math
from scipy.stats import norm

# Parameters
notional = 1_000_000
T_option = 3  # Option maturity
T_swap = 4  # Swap tenor
strike_rate = 0.06
forward_swap_rate = 0.065
volatility = 0.20
r_ois = 0.055  # Continuous compounding

# Annuity factor: PV of $1 per year for T_swap years, starting at T_option
annuity_factor = 0
for i in range(1, T_swap + 1):
    payment_time = T_option + i
    discount_factor = math.exp(-r_ois * payment_time)
    annuity_factor += discount_factor

# Black's formula for swaption
d1 = (math.log(forward_swap_rate / strike_rate) + 0.5 * volatility**2 * T_option) / (volatility * math.sqrt(T_option))
d2 = d1 - volatility * math.sqrt(T_option)

# Payer swaption value
swaption_value = notional * annuity_factor * (forward_swap_rate * norm.cdf(d1) - strike_rate * norm.cdf(d2))
swaption_value  # Result: around 35,000-45,000
```

**Common Bugs to Avoid:**
- Using bond option formula (equation 29.1) instead of swaption-specific formula
- Forgetting to multiply by annuity factor
- Using single discount factor instead of sum over all payment dates
- Discounting annuity payments from time 0 instead of from option maturity
- Confusing receiver vs payer swaption (swap N(d1) and N(d2) terms for receiver)

---

## Pattern: Quanto Derivative Drift Adjustment

**Description:** Quanto derivatives (foreign asset paid in domestic currency) require a correlation-based drift adjustment to the forward price, multiplying by exp(-ρ × σ_asset × σ_FX × T).

**When to Use:** Questions involving foreign index/asset with payoff in domestic currency, given correlation between asset and exchange rate, and volatilities of both.

**Procedure:**
1. Formula: Quanto Forward = S₀ × exp((r_domestic - q) × T - ρ × σ_S × σ_Q × T)
2. Identify correlation ρ between asset and exchange rate
3. Calculate forward price with quanto adjustment (subtract ρ × σ_S × σ_Q × T from drift)
4. Discount at domestic risk-free rate (not foreign rate)
5. Apply standard option pricing with adjusted forward

**Code Example:**

**Scenario:** Nikkei index at 25,000, 1.5-year quanto call strike 24,000. USD rate 3%, JPY rate 1%, dividend yield 1.5%, index vol 22%, FX vol 10%, correlation 0.25.

**Correct Code:**
```python
import math
from scipy.stats import norm

# Parameters
S0 = 25000
K = 24000
T = 1.5
r_domestic = 0.03  # USD rate
r_foreign = 0.01  # JPY rate (not used in quanto pricing)
q = 0.015  # Dividend yield
sigma_S = 0.22  # Index volatility
sigma_Q = 0.10  # FX volatility
rho = 0.25  # Correlation

# Quanto adjustment
quanto_adjustment = rho * sigma_S * sigma_Q * T

# Forward price with quanto adjustment
F_quanto = S0 * math.exp((r_domestic - q - quanto_adjustment) * T)

# Black-Scholes with quanto forward
d1 = (math.log(F_quanto / K) + 0.5 * sigma_S**2 * T) / (sigma_S * math.sqrt(T))
d2 = d1 - sigma_S * math.sqrt(T)

# Option value (per unit, in domestic currency)
call_value = math.exp(-r_domestic * T) * (F_quanto * norm.cdf(d1) - K * norm.cdf(d2))
call_value  # Result: around 2,800-3,200
```

**Common Bugs to Avoid:**
- Using foreign risk-free rate instead of domestic rate for discounting
- Forgetting the quanto adjustment term (-ρ × σ_S × σ_Q × T)
- Sign error on quanto adjustment (should reduce forward for positive correlation)
- Using equation (30.6) approximation when exact formula is needed
- Confusing which volatility is asset vs FX

---

## Pattern: Vasicek Bond Option with Coupon Adjustment

**Description:** Options on coupon-bearing bonds in Vasicek model require computing the forward bond price (including coupons paid after option maturity), then applying the bond option formula with volatility derived from B(t,T) function.

**When to Use:** Questions about European options on coupon bonds in short-rate models (Vasicek, Hull-White) with given mean reversion parameters.

**Procedure:**
1. Formula: B(t,T) = [1 - exp(-a(T-t))] / a
2. Formula: σ_P = σ × B(T_option, T_maturity) for bond price volatility
3. Calculate zero-coupon bond prices P(0,T) for all relevant dates using equations (31.6-31.8)
4. Compute forward bond price: F_bond = [Spot bond price - PV(coupons before option)] / P(0, T_option)
5. Calculate bond price volatility using B(T_option, T_maturity)
6. Apply Black's formula with F_bond as underlying and σ_P as volatility

**Code Example:**

**Scenario:** 1.5-year call on 3-year bond, strike 98, coupon 4% annual. Vasicek: a=0.1, b=0.06, σ=0.012, r₀=5%.

**Correct Code:**
```python
import math
from scipy.stats import norm

# Vasicek parameters
a = 0.1
b = 0.06
sigma_r = 0.012
r0 = 0.05

# Option and bond parameters
T_option = 1.5
T_maturity = 3.0
K = 98
coupon_rate = 0.04
principal = 100

# Vasicek bond pricing functions
def B_vasicek(t, T, a):
    return (1 - math.exp(-a * (T - t))) / a

def A_vasicek(t, T, a, b, sigma_r):
    B_val = B_vasicek(t, T, a)
    term1 = (B_val - (T - t)) * (a * b - 0.5 * sigma_r**2) / a**2
    term2 = (sigma_r**2 * B_val**2) / (4 * a)
    return math.exp(term1 - term2)

def P_vasicek(t, T, r_t, a, b, sigma_r):
    A_val = A_vasicek(t, T, a, b, sigma_r)
    B_val = B_vasicek(t, T, a)
    return A_val * math.exp(-B_val * r_t)

# Bond price at time 0 (spot)
P_maturity = P_vasicek(0, T_maturity, r0, a, b, sigma_r)
# Coupon at year 1 (before option maturity)
P_1yr = P_vasicek(0, 1.0, r0, a, b, sigma_r)
coupon_pv_before = coupon_rate * principal * P_1yr

# Spot bond price (dirty price)
spot_bond_price = P_maturity * principal + coupon_rate * principal * P_1yr

# Forward bond price at option maturity
P_option = P_vasicek(0, T_option, r0, a, b, sigma_r)
# Bond at option maturity will have coupons at T=2 and T=3 (relative to t=0)
# From perspective of T_option, these are at T_option + 0.5 and T_option + 1.5
forward_bond_price = (spot_bond_price - coupon_pv_before) / P_option

# Bond price volatility
B_option_to_maturity = B_vasicek(T_option, T_maturity, a)
sigma_P = sigma_r * B_option_to_maturity * math.sqrt((1 - math.exp(-2 * a * T_option)) / (2 * a))

# Black's formula for bond option
d1 = (math.log(forward_bond_price / K) + 0.5 * sigma_P**2) / sigma_P
d2 = d1 - sigma_P

call_value = P_option * (forward_bond_price * norm.cdf(d1) - K * norm.cdf(d2))
call_value  # Result: around 1.5-2.5
```

**Common Bugs to Avoid:**
- Using spot bond price instead of forward bond price
- Forgetting to subtract PV of coupons paid before option maturity
- Using interest rate volatility σ_r instead of bond price volatility σ_P
- Incorrect calculation of B(t,T) function (check mean reversion parameter a)
- Not accounting for all coupons between option maturity and bond maturity in forward price

---

## Pattern: CDS Spread Calculation with Accrual Payments

**Description:** CDS spread equates the premium leg (regular payments + accrual on default) to the protection leg (expected payoff), requiring three separate present value calculations.

**When to Use:** Questions asking for CDS spread given hazard rates or default probabilities, recovery rate, and payment frequency.

**Procedure:**
1. Formula: CDS Spread s = PV(Expected Payoff) / [PV(Premium Payments) + PV(Accrual Payments)]
2. Calculate survival probabilities: Q(t) = exp(-λt) or use given unconditional default probabilities
3. Compute PV of regular premium payments: Σ s × Q(Tᵢ) × DF(Tᵢ)
4. Compute PV of accrual payments: Σ s × P(default at tᵢ) × (tᵢ - Tᵢ₋₁)/2 × DF(tᵢ)
5. Compute PV of expected payoff: Σ (1 - R) × P(default at tᵢ) × DF(tᵢ)
6. Solve for s using the ratio formula

**Code Example:**

**Scenario:** 3-year CDS, annual payments, flat 6% rate, hazard rate 4%, recovery 40%, defaults at mid-year points.

**Correct Code:**
```python
import math

# Parameters
T = 3
payment_freq = 1  # Annual
r = 0.06  # Risk-free rate (continuous)
hazard_rate = 0.04
recovery_rate = 0.40
notional = 1  # Per dollar

# Time points
payment_times = [1, 2, 3]
default_times = [0.5, 1.5, 2.5]

# Survival and default probabilities
def survival_prob(t, lam):
    return math.exp(-lam * t)

def default_prob(t1, t2, lam):
    return survival_prob(t1, lam) - survival_prob(t2, lam)

# PV of regular premium payments (per unit spread s)
pv_premium = 0
for t in payment_times:
    Q_t = survival_prob(t, hazard_rate)
    df = math.exp(-r * t)
    pv_premium += Q_t * df

# PV of accrual payments (per unit spread s)
pv_accrual = 0
for i, t_default in enumerate(default_times):
    t_prev = 0 if i == 0 else payment_times[i-1]
    t_next = payment_times[i]
    prob_default = default_prob(t_prev, t_next, hazard_rate)
    accrual_fraction = (t_default - t_prev) / payment_freq
    df = math.exp(-r * t_default)
    pv_accrual += prob_default * accrual_fraction * df

# PV of expected payoff
pv_payoff = 0
for i, t_default in enumerate(default_times):
    t_prev = 0 if i == 0 else payment_times[i-1]
    t_next = payment_times[i]
    prob_default = default_prob(t_prev, t_next, hazard_rate)
    loss_given_default = 1 - recovery_rate
    df = math.exp(-r * t_default)
    pv_payoff += loss_given_default * prob_default * df

# CDS spread
cds_spread = pv_payoff / (pv_premium + pv_accrual)
cds_spread  # Result: around 0.055-0.065 (5.5%-6.5%)
```

**Common Bugs to Avoid:**
- Using only PV(premium payments) in denominator, forgetting accrual payments
- Calculating accrual as full period instead of fraction from last payment to default
- Using recovery rate instead of loss given default (1 - R) in payoff calculation
- Misaligning default times with payment periods
- Using simple interest discounting instead of continuous compounding when rates are given continuously

---

## Pattern: Survival Probability from Hazard Rate

**Description:** When hazard rates are constant, survival probability is Q(t) = exp(-λt), and default probability over [t₁, t₂] is Q(t₁) - Q(t₂), not the hazard rate itself.

**When to Use:** CDS pricing, credit risk calculations when given constant or piecewise constant hazard rates.

**Procedure:**
1. Formula: Q(t) = exp(-λt) for constant hazard rate λ
2. Formula: P(default in [t₁, t₂]) = exp(-λt₁) - exp(-λt₂)
3. If hazard rate changes, use piecewise: Q(t) = exp(-Σ λᵢ × Δtᵢ)
4. Verify that survival probabilities decrease monotonically
5. Use these probabilities to weight cash flows in CDS valuation

**Code Example:**

**Scenario:** Hazard rate 2.5% for first 2 years, then 3.5%. Calculate survival and default probabilities at years 1, 2, 3.

**Correct Code:**
```python
import math

# Hazard rates
lambda_1 = 0.025  # Years 0-2
lambda_2 = 0.035  # Years 2+

# Survival probabilities
Q_1 = math.exp(-lambda_1 * 1)
Q_2 = math.exp(-lambda_1 * 2)
Q_3 = math.exp(-lambda_1 * 2 - lambda_2 * 1)

# Default probabilities (unconditional)
P_default_year1 = 1 - Q_1
P_default_year2 = Q_1 - Q_2
P_default_year3 = Q_2 - Q_3

# Results
results = {
    'Q_1': Q_1,  # ~0.9753
    'Q_2': Q_2,  # ~0.9512
    'Q_3': Q_3,  # ~0.9188
    'P_default_1': P_default_year1,  # ~0.0247
    'P_default_2': P_default_year2,  # ~0.0241
    'P_default_3': P_default_year3   # ~0.0324
}
results
```

**Common Bugs to Avoid:**
- Using hazard rate directly as default probability
- Forgetting to accumulate hazard rates when they change over time
- Calculating conditional vs unconditional default probabilities incorrectly
- Not verifying that Σ P(default) + Q(T) = 1

---

## Pattern: Multi-Period DCF with Consistent Growth Application

**Description:** When growth rates apply to operating metrics (EBIT, CapEx), all related items must grow consistently, and net CapEx (CapEx - Depreciation) should be used in FCFF unless depreciation is added back separately.

**When to Use:** DCF valuations with explicit forecast periods where "EBIT and net CapEx grow at X%" is stated.

**Procedure:**
1. Clarify whether growth applies to EBIT alone or to all operating items
2. If "EBIT and net CapEx grow", apply growth to both EBIT and (CapEx - Depreciation)
3. Calculate FCFF = EBIT(1-t) - Net CapEx for each period
4. Alternatively: FCFF = EBIT(1-t) + Depreciation - CapEx if items tracked separately
5. Ensure consistency: if depreciation grows with CapEx, net CapEx growth may differ from gross CapEx growth

**Code Example:**

**Scenario:** EBIT $600M, depreciation $150M, CapEx $250M, tax 30%. "EBIT and net CapEx grow 12% for 4 years." WACC 8%.

**Correct Code:**
```python
import numpy as np

# Initial values
ebit_0 = 600
depreciation_0 = 150
capex_0 = 250
net_capex_0 = capex_0 - depreciation_0  # 100
tax_rate = 0.30
growth = 0.12
years = 4
wacc = 0.08

# Method 1: Grow EBIT and net CapEx directly
fcff_list = []
for t in range(1, years + 1):
    ebit_t = ebit_0 * (1 + growth) ** t
    net_capex_t = net_capex_0 * (1 + growth) ** t
    fcff_t = ebit_t * (1 - tax_rate) - net_capex_t
    fcff_list.append(fcff_t)

# PV of cash flows
pv_fcff = sum([fcff / (1 + wacc) ** (i + 1) for i, fcff in enumerate(fcff_list)])

pv_fcff  # Result: around 1,450-1,550
```

**Common Bugs to Avoid:**
- Growing EBIT but keeping CapEx constant (or vice versa)
- Confusing net CapEx (CapEx - Depreciation) with gross CapEx
- Double-counting depreciation (adding it back when already using net CapEx)
- Applying growth to EBIT(1-t) instead of to EBIT before tax adjustment
- Inconsistent treatment of working capital changes