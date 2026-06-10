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

**Description:** Swaption valuation requires treating the swap rate as the underlying asset and multiplying the Black's formula payoff by the present value of a basis point (annuity factor). The formula differs for payer vs receiver swaptions: payer swaptions give the right to pay fixed (benefit when rates rise), while receiver swaptions give the right to receive fixed (benefit when rates fall).

**When to Use:** Questions about swaptions (options on interest rate swaps) with given forward swap rate, strike rate, volatility, and swap tenor. Identify whether the swaption is a payer (right to pay fixed) or receiver (right to receive fixed) type.

**Procedure:**
1. Formula: Annuity Factor A = Σ δᵢ × P(0, Tᵢ) for all payment dates
2. Calculate discount factors P(0, Tᵢ) for each swap payment date (from option maturity to end of swap)
3. Compute annuity factor (PV of $1 per period over swap life, starting at option maturity)
4. Apply Black's formula:
   - **Payer swaption**: Value = A × [F₀N(d₁) - K N(d₂)]
   - **Receiver swaption**: Value = A × [K N(-d₂) - F₀N(-d₁)]
5. Where d₁ = [ln(F₀/K) + 0.5σ²T] / (σ√T) and d₂ = d₁ - σ√T
6. Multiply result by notional

**Example (sanitized):**
> **Scenario:** A 2-year option on a 5-year swap with annual payments, notional $10M, strike 5%, forward swap rate 5.5%, volatility 18%, flat discount rate 4.5% continuous.
> 
> **Case A - Payer Swaption (right to PAY 5% fixed):**
> 
> **Wrong approach:** Using receiver formula or forgetting to distinguish payer vs receiver type.
> 
> **Correct approach:**
> 1. Calculate annuity factor for 5 annual payments starting at T=2:
>    - A = Σ(i=1 to 5) exp(-0.045 × (2+i))
>    - A = exp(-0.135) + exp(-0.180) + exp(-0.225) + exp(-0.270) + exp(-0.315)
>    - A ≈ 4.12
> 
> 2. Calculate d₁ and d₂:
>    - d₁ = [ln(0.055/0.05) + 0.5×0.18²×2] / (0.18×√2) ≈ 0.4436
>    - d₂ = 0.4436 - 0.18×√2 ≈ 0.1891
> 
> 3. Apply payer formula:
>    - Value = 10M × 4.12 × [0.055×N(0.4436) - 0.05×N(0.1891)]
>    - Value = 10M × 4.12 × [0.055×0.6714 - 0.05×0.5750]
>    - Value ≈ $644,000
> 
> **Case B - Receiver Swaption (right to RECEIVE 5% fixed):**
> 
> **Correct approach:**
> 1. Same annuity factor: A ≈ 4.12
> 2. Same d₁ ≈ 0.4436, d₂ ≈ 0.1891
> 3. Apply receiver formula (note the sign changes and term swap):
>    - Value = 10M × 4.12 × [0.05×N(-0.1891) - 0.055×N(-0.4436)]
>    - Value = 10M × 4.12 × [0.05×0.4250 - 0.055×0.3286]
>    - Value ≈ $133,000
> 
> **Key insight:** Payer swaptions are more valuable when forward rate > strike (in-the-money to pay fixed at lower rate). Receiver swaptions are more valuable when strike > forward rate.

**Common Mistakes to Avoid:**
- **Using wrong formula for swaption type**: Payer uses [F₀N(d₁) - K N(d₂)], receiver uses [K N(-d₂) - F₀N(-d₁)]
- Confusing payer vs receiver: "right to pay fixed" = payer, "right to receive fixed" = receiver
- Using bond option formula (equation 29.1) instead of swaption-specific formula
- Forgetting to multiply by annuity factor
- Using single discount factor instead of sum over all payment dates
- Discounting annuity payments from time 0 instead of from option maturity (payments start at T_option, not at 0)
- Simply swapping N(d1) and N(d2) without also negating them for receiver swaptions
```

```
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

**Description:** Options on coupon-bearing bonds in Vasicek model require computing the forward bond price (including all coupons paid after option maturity), then applying Black's formula with bond price volatility derived from the integrated variance of the short rate. Critical steps include handling non-integer option maturities, properly separating coupons paid before vs after option maturity, and calculating the complete volatility formula.

**When to Use:** Questions about European options on coupon bonds in short-rate models (Vasicek, Hull-White) with given mean reversion parameters. Especially when option maturity falls between coupon payment dates or when semiannual/quarterly coupons are involved.

**Procedure:**
1. Calculate zero-coupon bond prices P(0,T) using Vasicek formulas:
   - B(t,T) = [1 - exp(-a(T-t))] / a
   - A(t,T) = exp{[B(t,T)-(T-t)][a²b-σ²/2]/a² - σ²B(t,T)²/(4a)}
   - P(t,T) = A(t,T) × exp(-B(t,T) × r_t)

2. Identify all coupon payment dates and separate into:
   - Coupons paid BEFORE option maturity (subtract their PV from spot bond price)
   - Coupons paid AFTER option maturity (included in forward bond price)

3. Calculate spot bond price (dirty price):
   - Spot = Principal×P(0,T_maturity) + Σ(coupons)×P(0,T_coupon) for ALL coupons

4. Calculate forward bond price at option maturity:
   - Forward = [Spot - PV(coupons before option)] / P(0,T_option)
   - This represents the bond's value at T_option, including all remaining coupons

5. Calculate bond price volatility (complete formula):
   - σ_P = σ_r × B(T_option, T_maturity) × √[(1 - exp(-2a×T_option))/(2a)]
   - This integrates the variance of the short rate over [0, T_option]

6. Apply Black's formula:
   - d₁ = [ln(F_bond/K) + 0.5σ_P²] / σ_P
   - d₂ = d₁ - σ_P
   - Call = P(0,T_option) × [F_bond×N(d₁) - K×N(d₂)]

**Example (sanitized):**
> **Scenario:** A 1.75-year call option on a 4-year bond with strike 102. Bond pays 5% semiannual coupons (2.5% every 6 months). Vasicek parameters: a=0.15, b=0.055, σ_r=0.015, r₀=4.8%. Coupon dates at 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0 years.
> 
> **Wrong approach:** Using spot bond price instead of forward, or using σ_r directly as bond volatility, or ignoring the variance integration formula.
> 
> **Correct approach:**
> 
> **Step 1: Calculate zero-coupon bond prices**
> - For T=1.75 (option maturity):
>   - B(0,1.75) = [1-exp(-0.15×1.75)]/0.15 ≈ 1.4892
>   - A(0,1.75) = exp[...] ≈ 1.0821 (using full formula)
>   - P(0,1.75) = 1.0821 × exp(-1.4892×0.048) ≈ 1.0051
> 
> - Similarly calculate P(0,T) for each coupon date and maturity
> 
> **Step 2: Identify coupons before vs after option maturity**
> - Before option (T ≤ 1.75): coupons at 0.5, 1.0, 1.5 years
> - After option (T > 1.75): coupons at 2.0, 2.5, 3.0, 3.5, 4.0 years + principal
> 
> **Step 3: Calculate spot bond price**
> - Spot = 100×P(0,4.0) + 2.5×[P(0,0.5) + P(0,1.0) + ... + P(0,3.5)]
> - Spot ≈ 100.8 (example value)
> 
> **Step 4: Calculate forward bond price**
> - PV(coupons before) = 2.5×[P(0,0.5) + P(0,1.0) + P(0,1.5)] ≈ 7.35
> - Forward = (100.8 - 7.35) / 1.0051 ≈ 93.0
> - This is the bond's value at T=1.75, with 5 remaining coupons + principal
> 
> **Step 5: Calculate bond price volatility (CRITICAL)**
> - B(1.75, 4.0) = [1-exp(-0.15×2.25)]/0.15 ≈ 1.4234
> - Variance integral: [1-exp(-2×0.15×1.75)]/(2×0.15) ≈ 2.8571
> - σ_P = 0.015 × 1.4234 × √2.8571 ≈ 0.0361
> - **NOT** just σ_r × B(T_option, T_maturity) without the square root term!
> 
> **Step 6: Apply Black's formula**
> - d₁ = [ln(93.0/102) + 0.5×0.0361²] / 0.0361 ≈ -2.6854
> - d₂ = -2.6854 - 0.0361 ≈ -2.7215
> - Call = 1.0051 × [93.0×N(-2.6854) - 102×N(-2.7215)]
> - Call ≈ 0.18
> 
> **Key insight:** The volatility formula includes the integral of variance over the option period, not just the B(t,T) function. For non-integer maturities, carefully track which coupons are included in the forward price.

**Common Mistakes to Avoid:**
- **Using spot bond price instead of forward bond price in Black's formula**
- **Incomplete volatility formula**: Must include √[(1-exp(-2a×T_option))/(2a)] term, not just σ_r × B(T_option, T_maturity)
- Forgetting to subtract PV of coupons paid before option maturity when computing forward price
- Using interest rate volatility σ_r instead of bond price volatility σ_P
- Incorrect calculation of B(t,T) function (verify mean reversion parameter a is in correct position)
- When option maturity falls between coupon dates, incorrectly including/excluding boundary coupons
- Not accounting for all coupons between option maturity and bond maturity in forward price calculation
- Discounting forward bond price again (it's already a forward price, just apply Black's formula and discount the option payoff)
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