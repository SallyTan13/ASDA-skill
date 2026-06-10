# Pattern 1: Policy Constraint Verification in Tactical Asset Allocation

**Description:** When making tactical asset allocation (TAA) recommendations, the model must verify that proposed changes remain within the strategic asset allocation (SAA) policy limits (upper and lower bounds) specified in the Investment Policy Statement, not just optimize for highest expected returns.

**When to Use:** Questions involving tactical asset allocation, portfolio rebalancing, or asset class weight adjustments where policy limits, IPS constraints, or allocation ranges are provided.

**Procedure:**
1. Identify the current allocation for each relevant asset class
2. Locate the policy limits (lower bound and upper bound) for each asset class from the IPS or strategic allocation table
3. Calculate the available room for adjustment: (upper limit - current allocation) for increases, (current allocation - lower limit) for decreases
4. Rank asset classes by expected excess returns or other optimization criteria
5. For each proposed increase, verify: current allocation + proposed change ≤ upper limit
6. For each proposed decrease, verify: current allocation - proposed change ≥ lower limit
7. If the highest-return option violates constraints, select the next-best feasible alternative that stays within all policy boundaries
8. Confirm the final recommendation satisfies all constraints before answering

**Example (sanitized):**
> **Scenario:** A pension fund has current allocations: Equities 40%, Bonds 35%, Real Estate 25%. Policy limits are: Equities [30%-50%], Bonds [25%-45%], Real Estate [15%-30%]. Short-term forecasts show Equities +4%, Bonds +1%, Real Estate +3%.
> **Wrong approach:** Recommend increasing Equities (highest return at +4%) and decreasing Bonds (lowest return at +1%) without checking constraints.
> **Correct approach:** (1) Check Equities: current 40%, upper limit 50%, room to increase = 10%. (2) Check Bonds: current 35%, lower limit 25%, room to decrease = 10%. (3) Verify proposed shift of 10% from Bonds to Equities: Equities would be 50% (at limit ✓), Bonds would be 25% (at limit ✓). (4) Confirm this is feasible and recommend the shift.

---

# Pattern 2: Missing Parameter Detection for Formula Application

**Description:** Before applying financial formulas or models, verify that all required parameters are explicitly provided in the question. If mandatory inputs are missing, the correct answer is that insufficient data is given, not an approximation or qualitative judgment.

**When to Use:** Questions asking to calculate specific metrics (SML position, Sharpe ratio, beta-adjusted returns) or apply models (CAPM, Gordon Growth, etc.) that have well-defined required inputs.

**Procedure:**
1. Identify the formula or model required by the question (e.g., SML requires CAPM: E(R) = Rf + β(Rm - Rf))
2. List all mandatory parameters for that formula (e.g., risk-free rate, beta, market return)
3. Systematically check the provided data for each required parameter
4. If any mandatory parameter is missing and cannot be derived from given information, stop calculation
5. Select "insufficient data" or equivalent option if available
6. Do NOT make qualitative judgments, assumptions about missing values, or proceed with partial calculations when core parameters are absent
7. Document which specific parameter(s) are missing in your reasoning

**Example (sanitized):**
> **Scenario:** Portfolio X has return of 9%, beta of 0.8. Market return is 12%. Question asks: Does Portfolio X lie above or below the SML?
> **Wrong approach:** Since beta is less than 1 and return (9%) is less than market return (12%), conclude it's below the SML.
> **Correct approach:** (1) SML requires CAPM: E(R) = Rf + β(Rm - Rf). (2) Given: return = 9%, β = 0.8, Rm = 12%. (3) Missing: risk-free rate (Rf). (4) Cannot calculate expected return without Rf. (5) Answer: Insufficient data given.

---

# Pattern 3: Probability-Weighted Statistics for Discrete Distributions

**Description:** When calculating statistics (mean, variance, standard deviation) for discrete probability distributions presented in state-of-economy or scenario tables, probability weights must be applied to each outcome. If probabilities are not explicitly stated, apply the equal probability convention across all states.

**When to Use:** Questions requiring calculation of expected return, variance, or standard deviation from scenario tables, state-of-economy tables, or discrete outcome distributions where probabilities may or may not be explicitly provided.

**Procedure:**
1. Identify all possible outcomes (states) and their associated values (returns, cash flows)
2. Check if probabilities are explicitly provided for each state
3. If probabilities are missing, apply equal probability convention: P(each state) = 1/n where n = number of states
4. Calculate expected value (mean): E(X) = Σ[P(i) × X(i)] for all states i
5. Calculate variance: Var(X) = Σ[P(i) × (X(i) - E(X))²] for all states i
6. Calculate standard deviation: SD(X) = √Var(X)
7. Verify that probabilities sum to 1.0 before finalizing calculation
8. Do NOT use simple arithmetic mean or unweighted variance formulas for probability distributions

**Example (sanitized):**
> **Scenario:** Stock returns in three states: Recession 5%, Normal 10%, Boom 20%. No probabilities given. Calculate standard deviation.
> **Wrong approach:** Mean = (5% + 10% + 20%)/3 = 11.67%. Variance = [(5-11.67)² + (10-11.67)² + (20-11.67)²]/3. SD = √Variance.
> **Correct approach:** (1) Three states, no probabilities given → use equal probabilities: P = 1/3 each. (2) E(R) = (1/3)(5%) + (1/3)(10%) + (1/3)(20%) = 11.67%. (3) Var = (1/3)(5-11.67)² + (1/3)(10-11.67)² + (1/3)(20-11.67)² = 38.89. (4) SD = √38.89 = 6.24%.

---

# Pattern 4: Capital Rationing with Indivisible Projects

**Description:** Under capital budget constraints with indivisible projects, the optimal solution requires evaluating all feasible combinations of projects that fit within the budget to maximize total NPV, not simply selecting the single project with highest individual NPV.

**When to Use:** Capital budgeting questions with explicit budget constraints where projects are stated as "not divisible" or "mutually exclusive groups" and multiple projects could potentially fit within the budget.

**Procedure:**
1. Calculate NPV for each individual project using the given discount rate
2. Note the initial investment required for each project
3. Identify the budget constraint amount
4. Enumerate all feasible combinations of projects where total initial investment ≤ budget
5. For each feasible combination, calculate the total NPV (sum of individual project NPVs)
6. Calculate total initial investment for each combination to confirm budget feasibility
7. Select the combination with the highest total NPV that satisfies the budget constraint
8. Verify that no other feasible combination yields higher total NPV before finalizing

**Example (sanitized):**
> **Scenario:** Budget = $500k. Project X: cost $300k, NPV $80k. Project Y: cost $250k, NPV $60k. Project Z: cost $250k, NPV $55k. Projects are indivisible.
> **Wrong approach:** Select Project X because it has the highest individual NPV ($80k).
> **Correct approach:** (1) Feasible combinations: {X alone: $300k, NPV $80k}, {Y alone: $250k, NPV $60k}, {Z alone: $250k, NPV $55k}, {Y+Z: $500k, NPV $115k}. (2) X+Y ($550k) and X+Z ($550k) exceed budget. (3) Highest total NPV is Y+Z combination at $115k. (4) Select Projects Y and Z.

## Pattern: Policy Constraint Verification in Tactical Asset Allocation

**Description:** When making tactical asset allocation (TAA) recommendations, the model must verify that proposed changes remain within the strategic asset allocation (SAA) policy limits (upper and lower bounds) specified in the Investment Policy Statement, not just optimize for highest expected returns. TAA decisions should incorporate all relevant factors including return forecasts, currency impacts, and market conditions that affect net expected returns.

**When to Use:** Questions involving tactical asset allocation, portfolio rebalancing, or asset class weight adjustments where policy limits, IPS constraints, or allocation ranges are provided.

**When NOT to Use:** 
- Questions about tactical shifts based on short-term forecasts where currency impacts or other adjustment factors significantly affect net returns
- Scenarios where the question asks about "most likely" allocation shifts based on forecast differentials rather than optimal allocation within constraints
- Cases where multiple factors (currency, hedging, market conditions) must be integrated before determining tactical shifts

**Procedure:**
1. Identify the current allocation for each relevant asset class
2. Locate the policy limits (lower bound and upper bound) for each asset class from the IPS or strategic allocation table
3. **Before calculating adjustment room, identify all factors affecting net expected returns:**
   - Currency impacts on foreign-denominated assets
   - Hedging costs or benefits
   - Transaction costs or other frictions
4. Calculate net expected returns incorporating all relevant factors
5. Calculate the available room for adjustment: (upper limit - current allocation) for increases, (current allocation - lower limit) for decreases
6. Rank asset classes by net expected returns or other optimization criteria after adjustments
7. For each proposed increase, verify: current allocation + proposed change ≤ upper limit
8. For each proposed decrease, verify: current allocation - proposed change ≥ lower limit
9. If the highest-return option violates constraints, select the next-best feasible alternative that stays within all policy boundaries
10. Confirm the final recommendation satisfies all constraints before answering

**Common Mistakes to Avoid:**
- Comparing long-term vs. short-term forecasts mechanically without considering currency or other adjustment factors
- Ignoring currency headwinds/tailwinds when assets are denominated in foreign currencies
- Focusing solely on gross returns without calculating net returns after all relevant impacts

**Example (sanitized):**
> **Scenario:** A pension fund has current allocations: Equities 40%, Bonds 35%, Real Estate 25%. Policy limits are: Equities [30%-50%], Bonds [25%-45%], Real Estate [15%-30%]. Short-term forecasts show Equities +4%, Bonds +1%, Real Estate +3%.
> **Wrong approach:** Recommend increasing Equities (highest return at +4%) and decreasing Bonds (lowest return at +1%) without checking constraints.
> **Correct approach:** (1) Check Equities: current 40%, upper limit 50%, room to increase = 10%. (2) Check Bonds: current 35%, lower limit 25%, room to decrease = 10%. (3) Verify proposed shift of 10% from Bonds to Equities: Equities would be 50% (at limit ✓), Bonds would be 25% (at limit ✓). (4) Confirm this is feasible and recommend the shift.

---

## Pattern: Currency-Adjusted Returns in Tactical Asset Allocation

**Description:** When evaluating tactical asset allocation shifts for portfolios with international exposure, currency forecasts must be incorporated into net expected returns before comparing asset classes. Assets denominated in foreign currencies face currency headwinds or tailwinds that can significantly alter their attractiveness relative to domestic-currency assets.

**When to Use:** 
- Tactical asset allocation questions involving international or multi-currency portfolios
- Scenarios where currency forecasts are explicitly provided alongside asset class return forecasts
- Questions asking about "most likely" tactical shifts when some assets have foreign currency exposure
- Cases where assets are valued in different currencies or have different currency hedging characteristics

**Procedure:**
1. Identify which asset classes have foreign currency exposure vs. domestic currency denomination
2. Locate the currency forecast (e.g., USD Index forecast, specific currency pair forecasts)
3. For each asset class, determine net expected return:
   - **Foreign-currency assets:** Gross return forecast + currency impact (negative if domestic currency strengthening, positive if weakening)
   - **Domestic-currency assets:** Gross return forecast (no currency adjustment)
   - **Hedged assets:** Gross return forecast - hedging cost (if applicable)
4. Rank asset classes by net expected returns after currency adjustments
5. Identify which asset classes have positive forecast differentials (short-term net return > long-term outlook or strategic expectation)
6. Recommend increasing weightings in asset classes with highest net expected returns and positive differentials
7. Recommend decreasing weightings in asset classes with lowest net expected returns or negative differentials

**Common Mistakes to Avoid:**
- Comparing gross returns without adjusting for currency impacts
- Ignoring currency forecasts when they are explicitly provided
- Treating all asset classes equally when some have foreign currency exposure and others don't
- Mechanically comparing long-term vs. short-term forecasts without incorporating currency effects

**Example (sanitized):**
> **Scenario:** A global fund has 50% foreign equities, 30% domestic bonds, 20% commodities (USD-priced). Short-term forecasts: Foreign equities +10%, Domestic bonds +3%, Commodities +6%. Currency forecast: Domestic currency expected to strengthen +4% vs. foreign currencies.
> **Wrong approach:** Recommend increasing foreign equities because they have the highest gross return (+10%).
> **Correct approach:** (1) Calculate net returns: Foreign equities = 10% - 4% = 6% net; Domestic bonds = 3% (no adjustment); Commodities = 6% (USD-priced, no adjustment). (2) Rank by net returns: Commodities (6%) and Foreign equities (6%) tie for highest, Domestic bonds lowest (3%). (3) Given currency headwind on foreign equities, recommend increasing commodities and potentially reducing domestic bonds, while being cautious about foreign equities despite high gross returns.