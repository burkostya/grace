**Phase 1: AGGRESSIVE CONTEXT GATHERING (Greedy Reading)**
* **Instruction:** "Do not guess the cause of the error from the traceback alone. You MUST load all modules mentioned in the stack trace, along with their dependencies mapped in `AppGraph.xml`. Read the `MODULE_CONTRACT`, `INVARIANTS`, and `RATIONALE` blocks of the failing components to understand how the code was *intended* to work before you attempt to fix it."

**Phase 2: LDD LOG ANALYSIS AND HYPOTHESIS (Semantic Verification)**
* **Instruction:** "Do not rely solely on `pytest` outputs. You must analyze the application logs (`app.log`), specifically looking for High-Importance tags `[IMP:7-10]`. Locate the 'AI Belief State' log right before the failure and compare it to the documented Contracts. Explicitly formulate a hypothesis about where the semantic logic diverged from the structural expectation *before* writing any code."

**Phase 3: IMPLEMENTATION AND IMMUNIZATION (The "Scar")**
* **Instruction:** "Once the fix is applied, you MUST immunize the code. Inside the specific `# START_BLOCK` where the fix was made, inject a mandatory comment in the format: `# BUG_FIX_CONTEXT: [Explain why the old approach failed, and why this specific fix was chosen]`. Finally, update the `CHANGE_SUMMARY` and verify that the new LDD traces accurately reflect the corrected logic. 100% test passing is irrelevant if the semantic trace does not match the contract."
