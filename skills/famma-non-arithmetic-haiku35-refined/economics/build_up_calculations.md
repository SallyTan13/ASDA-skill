# Economics — Build-Up Approach Calculations

## Pattern: risk_premium_build_up

**Description:** Questions requiring the build-up (risk premium) approach to calculate expected returns by summing a base rate plus multiple risk premiums, or questions involving asset-based valuation ratios that require careful identification of numerator and denominator components from financial statements.

**When to Use:** 
- Questions asking to "calculate expected return using the risk premium approach" or "build-up method"
- Questions mentioning summation of risk-free rate, term premium, credit premium, liquidity premium
- Questions asking to calculate or interpret "Tobin's q" or similar asset-based valuation metrics
- Questions requiring derivation of market value or replacement value of equity from balance sheet data
- Keywords: "build-up approach", "risk premium approach", "Tobin's q", "replacement value", "market value of equity"

---

## Sub-Pattern 1: Risk Premium Build-Up for Expected Returns

**Procedure:**

1. **Identify the base rate** — Locate the risk-free rate or benchmark rate (typically government bond yield of similar maturity)

2. **Identify all applicable risk premiums** — Common premiums include:
   - Term premium (maturity risk premium)
   - Credit premium (default risk premium based on credit rating)
   - Liquidity premium (compensation for illiquidity)
   - Equity risk premium (for stocks)
   - Other specific premiums mentioned in the question

3. **Sum all components** — Expected Return = Base Rate + Premium₁ + Premium₂ + ... + Premiumₙ

4. **Match units and time periods** — Ensure all rates are expressed in the same units (%, basis points) and refer to the same time horizon

5. **Select the answer** — Choose the option that matches your calculated sum

**Example (sanitized):**

> **Scenario:** An analyst needs to estimate the expected return on a 5-year A-rated corporate bond. The 5-year government bond yields 2.5%. The term premium for 5-year bonds is 0.3%, the credit premium for A-rated bonds is 1.2%, and the liquidity premium is 0.4%.
>
> **Wrong approach:** Using only risk-free rate + credit premium = 2.5% + 1.2% = 3.7%, ignoring other premiums
>
> **Correct approach:** 
> - Base rate (risk-free): 2.5%
> - Term premium: 0.3%
> - Credit premium: 1.2%
> - Liquidity premium: 0.4%
> - Expected return = 2.5% + 0.3% + 1.2% + 0.4% = 4.4%

---

## Sub-Pattern 2: Tobin's q Calculation and Interpretation

**Procedure:**

1. **Recall the correct formula** — Tobin's q = (Market Value of Equity + Market Value of Debt) / (Replacement Value of Equity + Replacement Value of Debt)
   - Alternative simplified form when focusing on equity: q = Market Value of Equity / Replacement Value of Equity

2. **Identify market value of equity** — This is typically given as:
   - Share price × Number of shares outstanding
   - Or directly stated as market capitalization

3. **Identify market value of debt** — Use book value of debt as proxy if market value not given (common assumption)

4. **Calculate replacement value of equity** — This requires balance sheet analysis:
   - Replacement Value of Equity = Replacement Value of Total Assets - Book Value of Liabilities
   - Replacement Value of Total Assets may be given directly or need adjustment from book values
   - If only book values given, look for adjustments or revaluation information

5. **Calculate Tobin's q** — Divide total market value by total replacement value

6. **Interpret the ratio:**
   - q > 1: Market values assets above replacement cost → Market may be overvalued or company has intangible value
   - q < 1: Market values assets below replacement cost → Market may be undervalued or company destroying value
   - q ≈ 1: Market fairly valued relative to replacement cost

**Example (sanitized):**

> **Scenario:** A company has 100 million shares outstanding trading at $25 per share. Book value of debt is $500 million. The replacement value of total assets is $3,000 million, and book value of total liabilities is $800 million.
>
> **Wrong approach:** 
> - Using q = Market Value of Total Assets / Replacement Value of Total Assets
> - Or confusing book value of equity with replacement value of equity
>
> **Correct approach:**
> - Market value of equity = 100M × $25 = $2,500M
> - Market value of debt = $500M (using book value as proxy)
> - Total market value = $2,500M + $500M = $3,000M
> - Replacement value of equity = $3,000M (replacement assets) - $800M (liabilities) = $2,200M
> - Replacement value of debt = $500M (book value)
> - Total replacement value = $2,200M + $500M = $2,700M
> - Tobin's q = $3,000M / $2,700M = 1.11
> - Interpretation: q > 1 suggests market values the company above replacement cost

---

## Sub-Pattern 3: Component Identification in Multi-Factor Models

**Procedure:**

1. **Read the question stem carefully** — Identify which specific approach or formula is requested

2. **List all components mentioned in exhibits** — Create a mental or written checklist of available data points

3. **Match components to formula requirements** — Ensure each term in the formula has a corresponding data point

4. **Watch for common traps:**
   - Confusing "market value" with "book value"
   - Confusing "total assets" with "equity"
   - Confusing "replacement value" with "historical cost"
   - Missing one or more premiums in build-up calculations
   - Using wrong maturity benchmark (e.g., 10-year rate for 5-year bond)

5. **Verify units and consistency** — Check that all inputs use compatible units (%, basis points, currency)

6. **Calculate systematically** — Work through the formula step-by-step, documenting each component

**Example (sanitized):**

> **Scenario:** Calculate the required return on equity using a build-up approach. Given: risk-free rate = 3%, equity risk premium = 6%, size premium = 2%, company-specific risk premium = 1.5%.
>
> **Wrong approach:** Using only risk-free rate + equity risk premium = 3% + 6% = 9%
>
> **Correct approach:**
> - Identify all components: risk-free rate, equity risk premium, size premium, company-specific premium
> - Sum all: 3% + 6% + 2% + 1.5% = 12.5%
> - This is the complete build-up approach for required return on equity

---

## Sub-Pattern 4: Balance Sheet Adjustments for Valuation Metrics

**Procedure:**

1. **Identify what needs to be calculated** — Determine if you need market value, book value, or replacement value

2. **For replacement value of equity:**
   - Start with replacement value of total assets (may require adjustments from book value)
   - Subtract book value of total liabilities (or market value if available)
   - Result = Replacement value of equity

3. **For market value of equity:**
   - Use share price × shares outstanding
   - Or market capitalization if directly provided

4. **For book value of equity:**
   - Total assets - Total liabilities (from balance sheet)
   - Or shareholders' equity directly from balance sheet

5. **Common adjustments to watch for:**
   - Intangible assets may need to be excluded
   - Asset revaluations may be provided
   - Off-balance-sheet items may need inclusion
   - Preferred equity may need separate treatment

6. **Apply to the valuation formula** — Use the correctly calculated components in the ratio

**Example (sanitized):**

> **Scenario:** Calculate price-to-replacement-value ratio. Market cap = $5,000M. Balance sheet shows: Total assets (book) = $4,000M, Total liabilities = $2,500M. Replacement value of assets is 120% of book value.
>
> **Wrong approach:** Using book value of equity in denominator: $5,000M / ($4,000M - $2,500M) = 3.33
>
> **Correct approach:**
> - Market value of equity = $5,000M (given as market cap)
> - Replacement value of assets = $4,000M × 1.20 = $4,800M
> - Replacement value of equity = $4,800M - $2,500M = $2,300M
> - Price-to-replacement-value = $5,000M / $2,300M = 2.17

---

## Key Distinctions to Remember

**Build-Up vs. CAPM:**
- Build-up: Sum of base rate + multiple specific premiums
- CAPM: Risk-free rate + Beta × Market risk premium

**Tobin's q vs. Price-to-Book:**
- Tobin's q: Market value / Replacement value (economic concept)
- Price-to-Book: Market value / Book value (accounting concept)

**Expected Return vs. Expected Excess Return:**
- Expected return: Absolute return (includes risk-free rate)
- Expected excess return: Return above benchmark (e.g., OAS - expected loss)

**Market Value vs. Replacement Value:**
- Market value: What investors currently pay (market price × quantity)
- Replacement value: Cost to recreate assets at current prices

---

SKILL_MD_ENTRY: | `economics/build_up_calculations.md` | Economics | Build-Up Approach Calculations | Risk Premium Build-Up, Tobin's q Calculation, Component Identification |