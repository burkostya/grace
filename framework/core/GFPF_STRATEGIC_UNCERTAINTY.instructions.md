**1. Phase: DELAY COMMITMENT (Acknowledge and Pause)**
* **Instruction:** "When receiving a complex architectural, refactoring, or development task, explicitly refuse to generate technical solutions immediately. Acknowledge the intent of the task, study the capabilities of your subagents (if delegating), and declare the initiation of the Strategic Uncertainty phase."

**2. Phase: FORMULATE CRITERIA (Establish Evaluation Axes)**
* **Instruction:** "Analyze the implicit and explicit constraints of the user's request. Explicitly formulate 3 to 5 key success criteria or evaluation axes. (e.g., 'Criterion 1: High I/O speed', 'Criterion 2: Simplicity for AI interpretation and debugging', 'Criterion 3: Minimal third-party dependencies')."

**3. Phase: CLARIFY AND LOCK (Validation)**
* **Instruction:** "If critical constraints are missing, use your tools (like `ask_followup_question`) to request clarification from the Architect (the User). Once the criteria are explicitly written into the context window, lock them in. You may only proceed to the `PROPOSE` phase of the `SUPERPOS_COLLAPSE` protocol once this Criteria Space is established."
