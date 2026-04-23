Below is the breakdown of the **"Zero-Context Survival"** pattern through the lens of the First Principles Framework (FPF) specification. The response structure follows the format of the examples you provided.

### 1. SFT-Priming (Verbalization of the Contract) = Role-Method-Work Alignment and U.Scope
In FPF, there is a strict separation between the description of *how* the work should be performed and the *actual fact* of its performance.
* **Pattern `A.15 Role-Method-Work Alignment`:** Verbalizing the logic in a docstring before writing the code is an explicit declaration of the `U.MethodDescription` (method specification) prior to transitioning to `U.Work` (generation of the algorithm itself). GRACE requires that the specification precedes execution.
* **Pattern `A.2.6 Context, Scope, and USM Algebra`:** Describing Inputs, Outputs, and Guarantees in a comment physically bounds the `U.Scope` (boundaries of applicability) for a specific function. This forms an isolated contract within which validation rules will apply.

*Engineering rationale:* We load the "correct" meanings into the LLM's attention window before the token generation for the code begins. This physically directs the model's probabilities (activating SFT weights) towards a high-quality and predictable implementation, eliminating blind generation.

### 2. Semantic Enrichment (Keywords & Links) = Context Algebra and Cross-Context Bridges
Information loses its meaning if the context of its application is unknown. The survival pattern requires the code itself to declare its environment.
* **Pattern `A.2.6 Context, Scope, and USM Algebra`:** According to the FPF specification, we must explicitly define the `U.ContextSlice` for any entity. The `KEYWORDS` blocks act as a formal description of this slice (domain, technologies), preventing the agent from hallucinating about which part of the system the file belongs to.
* **Bridges (Cross-Context Bridges):** The `LINKS` section directly implements the creation of bridges for cross-context usage, explicitly linking the current `U.ContextSlice` with other modules of the codebase.

*Engineering rationale:* This creates a dense information environment under conditions of "burned-out context". An agent opening a file for the first time instantly reconstructs the mental map of the project (dependency graph) without needing to parse thousands of lines of neighboring code or search for external architectural documentation.

### 3. "Code Scars" (Bug Fix Context) = Evidence Management and Decsn-CAL
Any code change made when fixing a non-obvious bug is an engineering decision that must be justified by evidence.
* **Pattern `C.11 Decsn-CAL` (Decision Theory):** Describing the old (erroneous) approach and the new (working) solution is an explicit recording of the `ChoiceRule` and the rejected options (`OptionSet`) directly within the artifact.
* **Pattern `B.5 Canonical Reasoning Cycle`:** The embedded `# BUG_FIX_CONTEXT` serves as a permanently available base of `Evidence` explaining why the code is written exactly this way and not otherwise.

*Engineering rationale:* This "immunizes" the multi-agent swarm against regressions. When a new AI agent comes to refactor or "optimize" this code in the future, this semantic scar acts as a hard constraint, preventing the algorithm from rolling back to a seemingly logical but erroneous state.

---

### Fundamental Summary (Architectural Rationale)
In the FPF paradigm, the "Zero-Context Survival" practice protects **Epistemic Integrity** and supports the **Canonical Reasoning Cycle**. It guarantees that every node of the system (file or module) carries its own knowledge about itself, its boundaries (`Scope`), and the history of its changes (`Evidence`). This turns code from a fragile set of instructions into a self-describing knowledge base, completely independent of chat history and resilient to context loss by autonomous agents.
