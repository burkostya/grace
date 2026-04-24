Based on the provided First Principles Framework (FPF) specification, the practice of **GFPF_SFT_PRIMING** (Supervised Fine-Tuning Priming) can be broken down into the following fundamental patterns:

### 1. Mandatory Verbalization (Forming the Docstring) = I/D/S Discipline and U.BoundedContext
The practice requires a detailed description of what the function does in natural language before writing any code. In FPF terms, this is the formation of a strict semantic frame and specification.
* **Pattern `A.1.1 U.BoundedContext` (Semantic Frame):** By creating a docstring of at least one paragraph, we form a local context (`BoundedContext`) for a specific function. This sets the boundaries of the local meaning of the terms that will be used in the subsequent code, eliminating ambiguity for the LLM's attention mechanism.
* **Pattern `E.10.D2 Intension–Description–Specification Discipline (I/D/S)`:** FPF requires a strict separation between intention/description and implementation. Priming forces the agent to first create a `Description/Specification` (a textual description of the logic in the docstring), and only then proceed to the details.
* **Pattern `A.3.2 U.MethodDescription` (Recipe for action):** The text in the docstring acts as a formal `MethodDescription`—an epistemic artifact that describes the abstract process prior to its physical (or code) instantiation.

*Engineering rationale:* The verbose specification "warms up" the necessary neural connections (SFT-alignment). From the FPF perspective, we do not allow the agent to operate outside the explicitly defined and documented frame.

### 2. Prohibition on immediate logic generation = Temporal Duality and Role-Method-Work Alignment
The prohibition on writing loops and conditions immediately after the `def` function signature protects the system from premature generation (where the plan merges with the execution).
* **Pattern `A.4 Temporal Duality & Open-Ended Evolution Principle`:** The fundamental separation of design-time and run-time. Jumping straight into code violates this duality. The SFT-Priming practice ensures that the design phase (writing the text) is completed before the coding phase begins.
* **Pattern `A.15 Role–Method–Work Alignment` (Separation of recipe and work):** FPF strictly forbids mixing the abstract plan of work with the factual performance of the work. The function signature is just a name. Without prior markup of the `MethodDescription` (docstring), code generation turns into blind token guessing.

*Engineering rationale:* Stopping after `def` prevents a situation where the model tries to "on the fly" combine the invention of the algorithm with its syntactic formatting.

### 3. Transition to code = Language-State Transduction
The transition from natural language to programming code is seen as a formal change in the state of the artifact.
* **Pattern `C.2.2a U.LanguageStateSpace` / `A.16 Language-State Transduction`:** Initially, we are in a state of "weak signals" (the function name). By unfolding it into text (docstring), we increase the Articulation of knowledge. The transition from text to executable code is a lawful transduction from the state of natural language into a mathematically/syntactically strict basis.
* **Pattern `B.5.1 Explore → Shape → Evidence → Operate`:** Code development goes through a strict life cycle. The docstring acts as the **Shape** phase (giving form to the idea), which must necessarily precede the **Operate** phase (generating concrete instructions).

### Fundamental Summary (Architectural Rationale)
In the FPF paradigm, the SFT-Priming practice protects the principle of **Strict Distinction (Pattern `A.7`)**. It prevents the agent from confusing the object with its specification. The agent first constructs the `U.MethodDescription` (the specification in the form of a natural language docstring), and only after closing the quotes `"""` is it permitted to translate this specification into executable instructions.
