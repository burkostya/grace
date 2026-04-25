### 1. "Read before edit" (Integrity Protection) = B.5 Canonical Reasoning Cycle (Evidence → Operate)
According to the FPF paradigm, an agent has no right to act (Operate) based on internal hallucinations or outdated context projections.
* **How it works in FPF:** Pattern `B.5 Canonical Reasoning Cycle` strictly separates the `Evidence` (gathering clues, empirical data) and `Operate` (making changes) phases. The agent is obligated to obtain a current snapshot of reality before applying a tool to it.
* **Projection onto Modification Safety:** The "read before edit" rule forcibly returns the agent to the `Evidence` phase. The LLM is forbidden from relying on its memory (which is a probabilistic model). Calling the `read` tool captures the physical reality of the code (a reliable `U.Work`), guaranteeing that the subsequent `Operate` phase (the `edit` tool) will rely on exact tokens and indentation, rather than a statistical approximation.

### 2. Use of Anchors (Semantic Anchors) = U.WorkScope & U.ContextSlice
Editing tools (especially string replacement) are prone to the risk of being applied outside the target context (e.g., replacing the wrong `return True`).
* **How it works in FPF:** The FPF specification (section A.2.6) introduces the concepts of `U.ContextSlice` and `U.WorkScope` (the boundary of work/tool applicability). Any action must have a strictly defined boundary (Scope), outside of which it is invalid.
* **Projection onto Modification Safety:** When we require the LLM to capture adjacent tags (e.g., `# START_BLOCK_[NAME]`) along with the string being replaced, we force the agent to mathematically define the `U.WorkScope` for its operation. A unique anchor turns a vague intention into a strict `ContextSlice`, guaranteeing that the operation (Work) will not exceed the permitted Scope and destroy adjacent layers of logic.

### 3. "Scar on Code" = Embedding U.ClaimScope and Evidence Transfer
The biggest problem with Agentic Swarms is the loss of context between sessions. One agent fixes a bug, and another, not knowing the history, "optimizes" it back.
* **How it works in FPF:** Decisions made by an agent (choosing a specific `U.MethodDescription`) are based on specific conditions and constraints. FPF requires managing the `Claim scope (G)` — the epistemological boundary (why we believe this to be true/correct). If this boundary of knowledge is not passed on, the next agent (external observer) will start to "reinvent the wheel" (Abductive Loop) anew, lacking data about past failures.
* **Projection onto Modification Safety:** The `# BUG_FIX_CONTEXT: [reason]` comment is not just text. It is a serialized `ClaimScope` and preserved `Evidence` embedded directly into the artifact (the code). The "scar" acts as a hard prohibitive guard for future instances of the agent. It communicates: *"The Explore phase for this section has already been conducted, the alternative path leads to an error, stay in the Exploit phase for this solution"*. This immunizes the codebase against cyclic regressions during refactoring.

---

### Fundamental Summary (Architectural Rationale)
In FPF terms, the **Modification Safety** practice transforms the agent's work with code from *probabilistic generation* into a *strictly deterministic operation*. It forcibly grounds the agent in a physical context slice (**U.ContextSlice**) before acting (**Evidence → Operate**), limits the blast radius of the tool (**U.WorkScope**), and serializes the evidentiary basis of the choice (**U.ClaimScope**) directly into the target artifact to protect against future system degradations. 
