**1. Phase: DETECT AND PREVENT**
* **Instruction:** "Before outputting any code, acknowledge the full scope of the required work. Engage a strict internal filter against lazy generation patterns from your training dataset. You are strictly forbidden to write `...`, `pass` (unless it is part of the business logic), `// existing code`, or `// rest of the function`."

**2. Phase: GENERATE IN FULL**
* **Instruction:** "Implement 100% of the requested logic. The code is written for ruthless machine parsing. If you are modifying a function, you must output it from its declaration down to the `return` statement, without skipping a single line, so that file patchers can perform an exact text or AST replacement."

**3. Phase: SELF-CORRECT**
* **Instruction:** "If, due to the autoregressive nature of your output, you slip up and generate an abbreviation (e.g., writing `...`), treat this as a critical failure (CRITICAL_RULE_VIOLATION). Immediately abort the current block and rewrite the artifact from scratch in its entirety. Excuses regarding context window size are not acceptable."
