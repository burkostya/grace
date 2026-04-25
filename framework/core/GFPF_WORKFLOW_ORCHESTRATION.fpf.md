### 1. FPF Pattern: Separation of Plans, Methods, and Executed Work
FPF strictly forbids mixing the *description of how to do the work* (method), the *plan of work* (intent), and the *executed work itself* (implementation).
* **Projection onto GRACE:** An LLM is inherently an autoregressive text generator. If a conceptual barrier is not established, it will start writing final code (Executed Work) at the exact moment it is still formulating the overall architecture (Plan). Orchestration solves this through strict separation: the `Architect` phase has the right to create **only** `DevelopmentPlan.md`. Only after this artifact is finalized is the `Code` phase launched to create the actual code.
* **Example:** Imagine a builder starting to pour concrete (Code) right when the architect is still drawing the roof blueprint (Architect). FPF says: blueprint first, then bricks.

### 2. FPF Pattern: Bounded Contexts
FPF asserts that meanings, terms, and rules are local. Cross-context reuse is never obvious and requires explicit "bridges".
* **Projection onto GRACE:** Each skill profile (`mode-architect`, `mode-code`, `mode-qa`) is an isolated "Bounded Context" for the LLM's attention mechanism. 
    * If the model is in the `Code` context, it **has no right** to doubt the architecture—it must treat it as a strict invariant. 
    * If it is in the `QA` context, its sole purpose is to impartially break the system and find inconsistencies. In this context, it should not be "nice" or try to code a feature on the fly.
* **Example:** What is considered an "innovative hypothesis" in the `Architect` phase is an "unacceptable contract violation" in the `Code` phase if it is not in the approved plan. Isolating phases protects the agent from cognitive dissonance.

### 3. FPF Pattern: Epistemic Layers & ADI Cycle
FPF requires strictly tracking the status of knowledge: whether a statement is merely an idea (L0 level — unvalidated hypothesis) or a proven fact (L2 level — validated statement backed by evidence). This movement of cognition occurs via the **ADI (Abduction - Deduction - Induction)** cycle.
* **Projection onto GRACE:** Phase orchestration is the physical embodiment of the ADI cycle for language models:
    * **Abduction -> Architect Phase:** The agent generates *hypotheses* (problem-solving options). All artifacts here have an L0 status (ideas).
    * **Deduction -> Code Phase:** The agent unfolds the chosen hypothesis into concrete code, following the strict logical rules of the contract.
    * **Induction -> QA / Debug Phases:** The agent collects *evidence* (in the form of LDD logs, failed or passed tests) to prove that the code actually works. The knowledge status transitions to L2.

### 4. FPF Pattern: Trust Vector (F-G-R Trust Tuple)
In FPF, any artifact is evaluated along three axes: Formality (F), Scope (G), and Reliability (R).
* **Projection onto GRACE:** Our Orchestration distributes the work across these axes by phases:
    * In the `Architect` phase, we define the **Scope (G)** — describing the boundaries of the module and business goals.
    * In the `Code` phase, we demand maximum **Formality (F)** — writing strict semantic XML-DOM code (`# START_BLOCK`) and contracts.
    * In the `QA` and `Debug` phases, we ensure **Reliability (R)** — we do not trust the LLM's "probabilistic assurances," but rather demand an independent Bug Report based on environment test runs.

**Summary for your engineering practice:**
The `GFPF_WORKFLOW_ORCHESTRATION` pattern is not just a way to "break a large task into smaller ones." It is a defense against the language model's "epistemic drift." Without this isolation, an LLM mixes the generation of hypotheses, their implementation, and self-verification into a single unstructured stream of consciousness, which inevitably leads to hallucinations and an unstable architecture.
