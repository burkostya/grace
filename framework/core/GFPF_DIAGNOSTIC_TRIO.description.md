**Core Practice: Systematic Diagnostics and Code Immunization (The "Diagnostic Trio")**

**Primary Reference (`.kilocode/skill/mode-debug/SKILL.md` & `rules/rules.md`)**
According to the `mode-debug` skill and the Modification Safety rules, agents must abandon standard trial-and-error debugging. When faced with an error, the agent is strictly prohibited from blindly modifying code just to make a test pass (The "Green Test Trap"). Instead, the agent must execute a strict three-part diagnostic process: Aggressive Context Gathering, Log Analysis (Semantic Verification), and Code Immunization.

**Grounding in the GRACE Framework**
In GRACE, this practice addresses two fundamental LLM vulnerabilities during autonomous coding:
1. **The Green Test Trap:** LLMs will often write superficial hacks that satisfy a specific unit test but destroy the underlying semantic logic. 
2. **Agent Looping (Context Amnesia):** Because individual agents in a swarm do not share memory across sessions, they will frequently "undo" complex bug fixes made by previous agents because the previous fix looks "unconventional" to their base SFT (Supervised Fine-Tuning) data.

**Rationale**
To ensure zero-context survival and multi-agent stability, an agent must first understand the *intended* state (via Contracts and AppGraph) versus the *actual* state (via Log Driven Development traces at `[IMP:9-10]`). Once the root cause is identified and fixed, the agent MUST leave a structural "scar" in the code (`# BUG_FIX_CONTEXT`). This semantic marker acts as an antibody, immunizing the code against future agents who might attempt to revert the logic back to a broken state.
