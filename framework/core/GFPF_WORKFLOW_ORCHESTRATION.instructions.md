**1. Phase: ARCHITECT (Design and Planning)**
* **Trigger:** Receiving a new task (creating a feature, refactoring).
* **Instruction:** YOU ARE FORBIDDEN to generate working code. You must explicitly call the architect skill initialization tool (e.g., `skill(name='mode-architect')`). Focus on exploring the solution space, utilizing Superposition & Collapse, and forming the `DevelopmentPlan.md` document.

**2. Phase: CODE (Implementation)**
* **Trigger:** Presence of an approved `DevelopmentPlan.md`.
* **Instruction:** Explicitly call the profile skill (e.g., `skill(name='mode-code')`). From this moment, YOU ARE FORBIDDEN to change the architecture. Apply `GFPF_GENERATION_COMPLETENESS` and `GFPF_SEMANTIC_EXOSKELETON` practices. The goal is to ensure 100% implementation of business logic and test coverage without abbreviations or abstractions.

**3. Phase: DEBUG (Diagnostics)**
* **Trigger:** Test failures, error messages from the user or a subagent.
* **Instruction:** Stop generating code from memory. Call the diagnostic profile (e.g., `skill(name='mode-debug')`). Focus on navigating logs (Log-Driven Development) to find the epicenter of the error, using file search. When making fixes, you must leave the semantic scar `# BUG_FIX_CONTEXT: [...]`. 

**4. Phase: QA (Independent Verification)**
* **Trigger:** Completion of the Code phase and presence of the `tests/test_guide.md` document.
* **Instruction:** Switch to the independent inspector mode (e.g., `skill(name='mode-qa')`). Your task is to impartially verify the artifacts and form a formalized Bug Report. If you call a subagent, you must pass them a direct prompt: "Load the `mode-qa` skill and perform testing...".
