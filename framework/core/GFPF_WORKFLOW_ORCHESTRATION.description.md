**Core Practice: The "Phase Activation" Protocol (WORKFLOW ORCHESTRATION)**

**Primary Reference (`.kilocode/rules/rules.md`)**
In the `.kilocode` rulebook, the agent's workflow is strictly divided into independent phases: "Architect" (Design and Planning), "Code" (Implementation and Tests), "Debug" (Diagnostics and Error Correction), and "QA" (Independent Verification). Any agent action within a phase WITHOUT explicitly loading the corresponding protocol is considered a critical rule violation (CRITICAL_RULE_VIOLATION). The model is strictly forbidden to rely on its memory (weights) in matters of task execution methodology.

**Grounding in the GRACE Framework**
In the context of GRACE, this pattern solves the problem of "cognitive overload" and LLM "focus blur." Language models tend to "smear" their efforts if asked to simultaneously plan architecture and write precise code. By isolating tasks into phases, we limit the context solely to the instructions and constraints relevant to the current mode of thinking.

**Rationale**
The rationale for this practice is agent predictability in a multi-agent environment. 
* The **Architect** phase requires maximum breadth of thought (exploring the solution space).
* The **Code** phase requires tunnel vision (100% implementation of the approved plan without attempts to rethink it).
* The **Debug** phase switches the agent into a mode of aggressive context gathering and anomaly hunting via LDD traces.
By separating them, we prevent premature code generation before contracts (`DevelopmentPlan.md`) are agreed upon.
