**Core Practice: Semantic Trace Verification (Avoiding "The Green Test Trap")**

**Primary Reference (`.kilocode/skill/mode-debug/SKILL.md`)**
According to the `mode-debug` skill in the `.kilocode` rulebook, the agent is strictly warned about "The Green Test Trap." The rules explicitly state: "100% PASSED is NOT final proof of correctness." For an autonomous agent, success is defined purely by Semantic Trace Verification—proving that the actual execution path observed in the logs perfectly matches the intended design and contracts.

**Grounding in the GRACE Framework**
In GRACE, this practice is grounded in the observation that LLMs will naturally optimize for the easiest path to a successful output (e.g., writing a test that heavily mocks internal logic, or writing code that coincidentally passes a weak test). Because the agent is the author of both the test and the code, standard Test-Driven Development (TDD) creates a false sense of security. Semantic Trace Verification forces the agent to step outside the binary pass/fail paradigm and audit its own "Belief State."

**Rationale**
The rationale for this practice is to prevent the system from degrading into "illusionary correctness." By forcing the agent to verify the actual execution trace (specifically `[IMP:7-10]` logs which represent deep business logic and AI belief states), we guarantee that the system isn't just taking shortcuts. This practice depends entirely on `GFPF_LOG_DRIVEN_DEVELOPMENT` (to generate the robust trace) and `GFPF_SEMANTIC_EXOSKELETON` (the `START_CONTRACT` to verify against), forming a closed-loop validation system.

