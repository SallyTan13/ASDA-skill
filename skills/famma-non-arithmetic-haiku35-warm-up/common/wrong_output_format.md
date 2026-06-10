# Analysis of Failure Cases

All four cases exhibit the same fundamental error pattern: the model performs correct calculations and reasoning, explicitly identifies the right answer in the explanation, but then outputs a different option letter in the final answer field.

---

## Pattern: Answer-Explanation Consistency Verification

**Description:** The model completes correct calculations and explicitly states the right conclusion in the explanation text, but fails to map this conclusion to the corresponding option letter in the final answer output, resulting in a mismatch between reasoning and submitted answer.

**When to Use:** Apply this verification procedure in all multiple-choice questions after completing calculations and before finalizing the answer output. Critical when questions involve numerical computations followed by option selection.

**Procedure:**
1. Complete all required calculations and identify which option satisfies the question requirements
2. Explicitly write out the conclusion in plain language (e.g., "Fund C has the highest value at X")
3. Create a direct mapping statement: "The conclusion '[specific finding]' corresponds to option [letter]: [option text]"
4. Cross-verify by checking: Does the option letter match the entity/value identified in step 2?
5. Perform reverse validation: Read the selected option letter and confirm it states exactly what your calculation concluded
6. If any mismatch is detected between calculated result and selected option, re-examine the mapping before output
7. Output the option letter that matches your explicit conclusion, not any other letter

**Example (sanitized):**
> **Scenario:** Three investment portfolios (X, Y, Z) are evaluated using a performance metric. After calculation, Portfolio Y scores 0.85, Portfolio X scores 0.72, and Portfolio Z scores 0.91. The question asks which has the highest score. Options are: A. Portfolio X, B. Portfolio Y, C. Portfolio Z.
> 
> **Wrong approach:** Calculate correctly (Z = 0.91 is highest), write in explanation "Portfolio Z has the highest score at 0.91," but output "A" as the final answer without verification.
> 
> **Correct approach:** 
> 1. Calculate: X=0.72, Y=0.85, Z=0.91
> 2. Identify: Portfolio Z has the highest score
> 3. Map explicitly: "Portfolio Z is highest" → check options → Portfolio Z is option C
> 4. Verify: Does option C say "Portfolio Z"? Yes
> 5. Reverse check: If I select C, does it match my conclusion? Yes
> 6. Output: C (with confidence that C matches the calculated winner)

---

## Pattern: Numerical Result to Option Letter Mapping

**Description:** When the answer requires selecting an option that contains a numerical value, the model calculates the correct number but fails to match it to the option containing that exact number, instead selecting a different option with a different value.

**When to Use:** Apply when the question asks for a numerical answer presented as multiple-choice options with different numerical values (percentages, ratios, currency amounts, etc.).

**Procedure:**
1. Complete the numerical calculation and write down the final numeric result explicitly (e.g., "Result = 5.0%")
2. List out each option with its associated value: "A: [value], B: [value], C: [value]"
3. Perform exact matching: identify which option letter contains the calculated value
4. Check for unit consistency: ensure calculated result and option values use the same units (%, decimal, basis points, etc.)
5. Flag any conversion needed: if your result is 0.05 and options show percentages, convert to 5% before matching
6. Create explicit statement: "My calculated result [X] exactly matches option [letter] which states [X]"
7. Verify no other option contains this value (check for uniqueness)
8. Output the option letter identified in step 3, not based on position or any other criterion

**Example (sanitized):**
> **Scenario:** Calculate the required return using given formula. After computation, the result is 7.2%. Options are: A. 5.5%, B. 7.2%, C. 8.1%.
> 
> **Wrong approach:** Calculate 7.2% correctly, write "the answer is 7.2%" in explanation, but output "A" without checking what value option A actually contains.
> 
> **Correct approach:**
> 1. Calculate: Result = 7.2%
> 2. List options: A = 5.5%, B = 7.2%, C = 8.1%
> 3. Match: 7.2% appears in option B
> 4. Units check: Both in percentage form ✓
> 5. Explicit statement: "My result 7.2% matches option B: 7.2%"
> 6. Uniqueness: Only option B has 7.2% ✓
> 7. Output: B