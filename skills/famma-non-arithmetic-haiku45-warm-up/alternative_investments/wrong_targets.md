# Skill Patterns for Wrong Targets Error Type

## Pattern: Missing Context Detection

**Description:** The model attempts to answer questions referencing entities (people, policies, concerns) not present in the provided context, fabricating plausible responses instead of recognizing information gaps.

**When to Use:** When questions reference specific named individuals, their concerns, or specific policies/frameworks. Trigger keywords: "Discuss [Person's] concerns," "actions [Person] should take," "relevance of [specific policy]."

**Procedure:**
1. Extract all named entities from the question (people, specific policies, frameworks)
2. Search the provided context for each entity explicitly
3. If any entity is NOT found in context, flag as "insufficient information provided"
4. Check if the question assumes knowledge from earlier case sections not included in current context
5. If context is incomplete, state: "The question references [entity] whose concerns/details are not provided in the given context"
6. Only proceed with answering if all referenced entities and their relevant attributes are explicitly present

**Example (sanitized):**
> **Scenario:** Question asks "Discuss how Martinez's liquidity framework addresses the board's concerns" but context only describes a pension fund's asset allocation without mentioning Martinez or any liquidity framework.
> **Wrong approach:** Fabricate a general answer about liquidity frameworks and how they typically address board concerns about illiquid investments.
> **Correct approach:** (1) Identify "Martinez" and "liquidity framework" as key entities, (2) Search context and find neither mentioned, (3) Conclude: "The question references Martinez and a specific liquidity framework that are not described in the provided context. Cannot answer without this information."

---

## Pattern: Sequential Multi-Part Question Tracking

**Description:** In case studies with multiple sequential questions, the model continues answering a previous question instead of recognizing when the question has shifted to a new task or analysis requirement.

**When to Use:** When working through case studies with multiple questions. Trigger phrases: "Discuss the elements of [analysis]," "Identify which," followed by different analytical tasks.

**Procedure:**
1. Read the complete question stem and identify the PRIMARY verb (discuss, calculate, identify, analyze)
2. Identify the SPECIFIC SUBJECT of analysis requested (e.g., "elements of Bookman's analysis" vs. "asset classes needing rebalancing")
3. Check if the question introduces NEW analytical requirements not mentioned in prior questions
4. If the question asks about "elements of [person's] analysis," the answer should describe the METHODOLOGY and CALCULATIONS performed, not just conclusions
5. Map the question requirements to specific data/exhibits: what calculations or procedures are needed?
6. Verify your answer directly addresses the question's subject, not a related but different topic from earlier in the case

**Example (sanitized):**
> **Scenario:** Part A asks "Which asset classes need rebalancing band adjustment?" Part B asks "Discuss the elements of the manager's liquidity analysis and conclusions."
> **Wrong approach:** Continue discussing rebalancing bands and which assets are out of range.
> **Correct approach:** (1) Recognize Part B shifted to liquidity analysis, (2) Describe the methodology: multiply each asset allocation by liquidity classification percentages, (3) Show calculations: liquid % = (cash × 100%) + (bonds × 100%) + ..., (4) State conclusions: current liquid allocation vs. policy limits and capacity for changes.

---

## Pattern: Core Value Proposition Identification

**Description:** The model lists multiple features and benefits of a financial product instead of identifying the single primary market niche or problem it solves.

**When to Use:** When questions ask "What market niche is filled," "What problem does this solve," or "What is the primary purpose." Trigger keywords: "niche," "gap," "purpose," "addresses what need."

**Procedure:**
1. List all features mentioned in the product description
2. For each feature, ask: "What investor problem does this solve?"
3. Identify which problem is UNIQUE or CENTRAL to this product's design (not generic benefits like "liquidity" or "returns")
4. Distinguish between the core problem (e.g., "storage burden") and secondary benefits (e.g., "inflation hedge," "accessibility")
5. Formulate answer as: "[Product] fills the niche for investors who want [core benefit] without [core problem]"
6. Verify: Can the answer be stated in one clear sentence? If requiring multiple paragraphs, you're likely listing features rather than identifying the niche

**Example (sanitized):**
> **Scenario:** A structured note offers principal protection with equity upside participation, issued by a major bank.
> **Wrong approach:** List all benefits: "capital preservation, equity exposure, credit quality, tax efficiency, customization options..."
> **Correct approach:** (1) Core feature = principal protection + equity participation, (2) Problem solved = investors want equity exposure but cannot tolerate downside risk, (3) Answer: "Fills the niche for risk-averse investors seeking equity market participation with downside protection."

---

## Pattern: Stakeholder-Specific Concern Mapping

**Description:** When questions ask about addressing specific stakeholder concerns, the model provides generic risk management actions instead of mapping proposed changes to the PARTICULAR concerns expressed by that stakeholder.

**When to Use:** When questions ask to "address [person's] concerns," "alleviate concerns about," or "discuss relevance to concerns." Trigger: specific concerns are stated earlier in the context.

**Procedure:**
1. Locate where the stakeholder's concerns are explicitly stated in the context
2. Extract each distinct concern as a separate item (e.g., "liquidity profile risk," "risk profile drift")
3. For each concern, identify what specific aspect of the proposal creates or exacerbates it
4. Map mitigation actions directly to each concern: "For concern X, action Y addresses it by Z mechanism"
5. Distinguish between concerns about PROCESS (e.g., spending policy design) vs. OUTCOMES (e.g., return levels)
6. Verify each stated concern has a corresponding mitigation action in your answer

**Example (sanitized):**
> **Scenario:** CFO expresses two concerns: (1) increased allocation to private equity reduces liquidity for debt service, (2) illiquid assets make rebalancing costly during stress periods. Proposal increases PE from 15% to 25%.
> **Wrong approach:** List generic actions: "enhance due diligence, improve risk framework, stress testing..."
> **Correct approach:** (1) Concern 1 (liquidity): Ensure liquid assets remain above minimum threshold even under stress; establish credit facility as backup, (2) Concern 2 (rebalancing): Implement automatic rebalancing using correlated public equity positions; set pre-specified tolerance bands before increasing PE allocation.

---

## Pattern: Policy Mechanism vs. Policy Outcome Distinction

**Description:** The model confuses questions about HOW a policy works (mechanism/design) with questions about WHETHER a policy achieves goals (outcomes/adequacy).

**When to Use:** When questions ask about "relevance of policy," "policy design," or "how policy addresses." Trigger keywords: "spending policy," "rebalancing policy," "relevance to concerns."

**Procedure:**
1. Determine if the question asks about policy DESIGN/MECHANISM (how it works, what rules it follows) or policy OUTCOMES (whether returns are sufficient, risks are acceptable)
2. If asking about "relevance" or "how policy addresses concerns," focus on the policy's structural features and their functional purpose
3. For spending policies: identify the formula type (geometric smoothing, simple rule), its countercyclical properties, and how these interact with the concern
4. Connect policy mechanism to the specific concern: "Policy feature X creates effect Y, which [addresses/conflicts with] concern Z"
5. Avoid discussing whether returns are adequate unless the question specifically asks about return sufficiency
6. Verify: Does your answer explain HOW the policy operates, not just whether outcomes are good/bad?

**Example (sanitized):**
> **Scenario:** Foundation uses a spending rule: 70% of prior year spending adjusted for inflation + 30% of 5-year average portfolio value × 4.5%. Question asks about relevance to concerns about volatile distributions.
> **Wrong approach:** Discuss whether expected returns (7.2%) are sufficient to support the 4.5% spending rate and maintain purchasing power.
> **Correct approach:** (1) Identify this as a geometric smoothing rule, (2) Explain the 70/30 weighting dampens year-to-year volatility in distributions, (3) Note the smoothing creates predictable spending patterns even during market stress, (4) Connect: This directly addresses distribution volatility concerns by design, though it means lower spending in strong markets and higher spending in weak markets.