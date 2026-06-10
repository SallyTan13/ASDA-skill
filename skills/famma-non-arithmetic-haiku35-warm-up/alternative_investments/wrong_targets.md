# Pattern Analysis: Alternative Investments Wrong Target Errors

## Pattern: Question Target Misidentification in Multi-Actor Scenarios

**Description:** Model fails to distinguish between different stakeholders' concerns in complex case studies, answering about general portfolio metrics instead of the specific concern raised by the named individual (e.g., answering about "board concerns" when asked about "Brodka's concerns").

**When to Use:** When questions reference specific individuals by name and ask about "their concerns," "their perspective," or actions to address "their" issues. Trigger keywords: "[Name]'s concerns," "discuss relevance to [Name]," "actions to alleviate [Name]'s concerns."

**Procedure:**
1. Identify the specific person named in the question (e.g., "Brodka's concerns" vs. "board's concerns")
2. Scan the context for statements, objections, or perspectives explicitly attributed to that individual
3. If the named person is not in the visible context, infer their likely concerns based on their role and the portfolio changes being discussed (e.g., risk officer would focus on liquidity/rebalancing, not just returns)
4. Match your answer scope to the specific concern domain: if asked about "spending policy relevance," discuss spending policy mechanics, not portfolio statistics
5. Verify that your answer addresses the mechanism or relationship asked about (e.g., "how does X relate to Y") rather than just describing outcomes
6. Cross-check: Does your answer explain the connection between the two concepts in the question, or does it only discuss one of them?

**Example (sanitized):**
> **Scenario:** A foundation increases allocation to private equity from 15% to 25%. The CFO raises concerns about liquidity management. Question asks: "Discuss actions the portfolio manager should take to address the CFO's liquidity concerns."
> **Wrong approach:** Discussing how the new allocation improves expected returns from 6.5% to 7.2% and reduces probability of capital erosion.
> **Correct approach:** (1) Identify CFO's specific concern = liquidity, not returns. (2) Address liquidity directly: implement stress testing of liquid asset coverage under drawdown scenarios, establish rebalancing bands to prevent drift when illiquid assets can't be adjusted, ensure liquid reserves exceed capital call commitments plus spending needs. (3) Verify answer focuses on liquidity management mechanisms, not performance metrics.

---

## Pattern: Negation-Based Question Logic Confusion

**Description:** Model misinterprets "least accurate," "NOT correct," or "EXCEPT" questions as asking for category differences rather than identifying factually incorrect statements, leading to selection of true statements that differ in type rather than false statements.

**When to Use:** Questions containing "least accurate," "least likely," "NOT," "EXCEPT," or "which is incorrect." Trigger keywords: "least accurate," "NOT correct," "EXCEPT," "which limitation is least accurate."

**Procedure:**
1. Recognize that "least accurate" = "most false" = identify the incorrect statement, regardless of whether it's framed as benefit/limitation/characteristic
2. Reframe the question: "Which statement is factually wrong?" rather than "Which statement is different in category?"
3. Evaluate each option independently for factual correctness against the context or domain knowledge
4. Mark each option as TRUE or FALSE based on facts, not based on whether it represents a benefit vs. limitation
5. Select the FALSE statement (or if all true, select the least supported by evidence)
6. Verification: Confirm the selected answer contains a factual error or unsupported claim, not just a different categorization

**Example (sanitized):**
> **Scenario:** Context states: "Risk parity approaches provide diversification benefits and integrated risk measurement. However, they may be sensitive to correlation estimates and can underestimate tail risk." Question: "Which statement about risk parity is least accurate? A) Provides integrated risk measurement B) Sensitive to correlation estimates C) Eliminates tail risk entirely"
> **Wrong approach:** Selecting A because it's a benefit while B and C are limitations, making it "different."
> **Correct approach:** (1) Recognize "least accurate" = identify the false claim. (2) Evaluate: A is TRUE (stated benefit), B is TRUE (stated limitation), C is FALSE (claims elimination, but context says it underestimates tail risk, not eliminates it). (3) Select C as the factually incorrect statement.

---

## Pattern: Case Study Scope Boundary Misrecognition

**Description:** Model treats missing character names or scenario details as question errors rather than recognizing that exam case studies often span multiple related sub-scenarios, and questions may reference portions not shown in the immediate excerpt but inferable from the core theme.

**When to Use:** When questions reference individuals, scenarios, or concerns not explicitly named in the visible context, especially in multi-part case studies. Trigger: unfamiliar names in questions but thematically consistent concerns.

**Procedure:**
1. When encountering unfamiliar names/scenarios, do NOT immediately conclude the question is unanswerable
2. Identify the core theme and structural changes in the visible context (e.g., "increasing illiquid allocation from X% to Y%")
3. Infer the natural concerns that would arise from such changes based on financial principles (e.g., more illiquidity → liquidity management concerns, rebalancing difficulty concerns)
4. Map the unfamiliar character to a likely role based on their concern type (liquidity concerns → risk officer, spending policy concerns → treasurer/CFO)
5. Answer based on the financial principles relevant to the inferred concern, grounded in the visible context's core changes
6. Verification: Does your answer address predictable consequences of the portfolio changes described, even if the specific character wasn't introduced?

**Example (sanitized):**
> **Scenario:** Visible context shows a pension fund increasing real estate allocation from 8% to 18%. Question asks: "Discuss how Martinez should address Thompson's concerns about valuation frequency."
> **Wrong approach:** "Cannot answer because Martinez and Thompson are not mentioned in the context."
> **Correct approach:** (1) Core change = increased illiquid real estate. (2) Infer natural concern = illiquid assets have infrequent valuations, causing stale pricing and difficulty in risk monitoring. (3) Thompson likely = risk oversight role. Martinez likely = portfolio manager. (4) Answer: Martinez should implement more frequent appraisals, use transaction-based pricing indices for interim estimates, and apply volatility adjustments to account for appraisal smoothing in risk calculations.

---

## Pattern: Mechanism vs. Outcome Confusion in "Relevance" Questions

**Description:** When asked about "relevance of X to Y" or "how X relates to Y," model provides outcome statistics or general benefits instead of explaining the causal mechanism or structural relationship between the two specific concepts.

**When to Use:** Questions asking "discuss the relevance of [Policy/Feature X] to [Concern Y]," "how does X address Y," or "relationship between X and Y." Trigger keywords: "relevance," "relationship," "how does X relate to."

**Procedure:**
1. Identify the two specific concepts being linked (e.g., "spending policy" and "liquidity concerns")
2. Recognize that the question asks for the CONNECTION/MECHANISM, not just describing each concept separately
3. Explain HOW the first concept affects, constrains, or interacts with the second concept through specific mechanisms
4. Avoid substituting portfolio statistics (returns, Sharpe ratios, volatility) for mechanism explanations unless those statistics directly demonstrate the mechanism
5. Structure answer: "X relates to Y because [mechanism]. Specifically, when [condition in X], it causes [effect on Y] through [pathway]."
6. Verification: Does your answer explain a causal or structural link, or does it just list facts about X and facts about Y separately?

**Example (sanitized):**
> **Scenario:** An endowment uses a smoothing rule that averages the past 3 years' values to set spending. The endowment is increasing illiquid investments. Question: "Discuss the relevance of the spending policy to concerns about illiquidity."
> **Wrong approach:** "The spending policy supports a 5% distribution rate. The new allocation improves returns from 7% to 7.5% and maintains adequate coverage."
> **Correct approach:** "The smoothing rule creates COUNTERCYCLICAL liquidity demands. When markets decline, the smoothed value declines more slowly than current value, requiring HIGHER percentage withdrawals from a smaller liquid asset base. With increased illiquid holdings, this mismatch intensifies: the policy mandates distributions that may exceed available liquid assets during downturns, since illiquid positions cannot be readily sold. This mechanism directly links the spending formula design to liquidity stress under the proposed allocation."