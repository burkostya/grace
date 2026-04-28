**1. Phase: AGGRESSIVE CONTEXT GATHERING (The Baseline)**
* **Instruction:** "Do not attempt to fix or verify code in isolation. You must load all modules involved in the trace (using the `AppGraph.xml`). Read their `MODULE_CONTRACT`, `INVARIANTS`, and `RATIONALE` blocks. You must establish a firm understanding of what the code *was intended* to do before evaluating what it *actually* did."

**2. Phase: LOG AUDIT (Bypass the Green Test Trap)**
* **Instruction:** "Never assume the code is correct simply because `pytest` returns green. You must analyze the `app.log` and console outputs. Specifically, hunt for high-importance log markers (`[IMP:7-10]`) that represent the AI's Belief State, data boundary checks, and the true algorithmic flow."

**3. Phase: SEMANTIC VERIFICATION (Trace vs. Contract)**
* **Instruction:** "Compare the actual execution path—as proven by the generated LDD logs—against the promises made in the `START_CONTRACT`. If the logs do not explicitly demonstrate that the core business logic was executed as designed, the code is invalid. If the trace is ambiguous, implement 'Dynamic Probing' (e.g., `[DebugProbe][IMP:10] var_X=...`) to force absolute semantic certainty before finalizing the QA or Debug phase."
