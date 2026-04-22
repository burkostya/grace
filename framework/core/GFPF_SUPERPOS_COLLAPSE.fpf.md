### 1. PROPOSE (Superposition) = Abductive Loop and Open-Ended Search
According to FPF, when faced with uncertainty, we have no right to immediately jump to deduction or execution.
* **Pattern `B.5.2 Abductive Loop`:** During the PROPOSE phase, we force the agent to initiate hypothesis generation ("what could be true?") before the model slides into the most statistically probable but trivial answer (overfit to today's data).
* **Pattern `C.18 NQD-CAL` (Open-Ended Search Calculus):** We create a `CandidateSet`. FPF requires illuminating the solution space, maximizing `Diversity_P` to avoid "single-winner bias" during the early stages of creative search.

*Engineering rationale:* You force the LLM to generate a Pareto front of solutions before its attention mechanism goes "blind" from its own generated response.

### 2. HOLD = Legal Comparison and E/E-LOG
Keeping options in context without an immediate choice is the foundation of comparative governance in FPF.
* **Patterns `A.19.CPM` (Unified Comparison Mechanism) and `A.18 CSLC`:** FPF categorically forbids "hidden scalarization"—when a complex trade-off is implicitly collapsed into a single number or a hasty LLM choice. During the HOLD phase, the agent must explicitly state the properties of each option against given criteria (CSLC: Characteristic, Scale, Level).
* **Pattern `C.19 E/E-LOG` (Explore–Exploit Governor):** The HOLD phase is the explicit management of the "live candidate pool." We deliberately keep the system in Exploration mode until we accumulate enough Evidence (pros and cons).

*Engineering rationale:* Analysis in the HOLD mode creates a powerful "gravitational center" of arguments and facts within the LLM's context window. When it comes to making a choice, the attention mechanism will rely on this structured analytics, rather than on random tokens from the initial prompt.

### 3. COLLAPSE = Decision Theory and Transition to U.Work
Collapse is the crossing of the hard boundary between "Design" and "Run" (execution).
* **Pattern `C.11 Decsn-CAL` (Decision Theory):** Collapse is the application of a `ChoiceRule` to our `OptionSet`. The moment of transition from "probe again" (explore) to "choose now" (exploit) becomes explicit and justified by the evidence gathered in the previous step.
* **Pattern `A.15 Role-Method-Work Alignment`:** While the options were in superposition (PROPOSE and HOLD), we operated with abstract paths—`U.MethodDescription` (recipes, ideas). The collapse and writing of the final code mark the instantiation of `U.Work` (a concrete, dated act of execution that consumes resources). FPF strictly forbids mixing the specification of work with the factual performance of work.

### Fundamental Summary (Architectural Rationale)
In the FPF paradigm, the "Superposition and Collapse" practice protects the **Canonical Reasoning Cycle (`B.5 Canonical Reasoning Cycle`: Explore → Shape → Evidence → Operate)**.
