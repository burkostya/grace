### 1. **C.24 Agentic Tool‑Use & Call‑Planning** (Budgeting and stop conditions)
At the core of the Anti-Loop Protocol lies the concept of a limited enactment budget.
* **How it works in FPF:** Pattern `C.24` regulates the `tool-call budget` and `stop/replan condition` for autonomous agents. It requires a clear separation between the planned route and the actual work, so the agent doesn't exhaust resources in an infinite loop.
* **Projection onto Anti-Loop:** The limit of 5 attempts is a strict `enactment budget`. Each test failure is a trigger for a `stop/replan condition`, forcing the agent to re-evaluate the plan, and on the 5th attempt, a "harm gate" (escalation to a human) occurs, preventing further context burnout.

### 2. **A.12 External Transformer & Reflexive Split** (External observer)
The FPF specification forbids "self-magic", where the system evaluates and corrects itself without an external anchor.
* **How it works in FPF:** Pattern `A.12` establishes the `External Transformer Principle` — any change must be triggered by an external entity (`External agent, control loop`). 
* **Projection onto Anti-Loop:** This is exactly why the counter logic is moved to `tests/conftest.py` (architectural isolation). The testing framework (pytest) acts as the external `TransformerRole`. It observes the agent's "work" (`U.Work`) from the outside and forcibly dictates its current state (which attempt it is), preventing the LLM from "independently deciding" that the counter can be reset.

### 3. **C.19 Explore–Exploit Governor (E/E‑LOG) & B.5.2 Abductive Loop** (Changing search policy)
An agent stuck in a loop is trying to apply an exploit strategy where it no longer works.
* **How it works in FPF:** Pattern `C.19` requires an explicit policy for managing the solution pool (`explore-exploit`), determining when to narrow the search and when to forcibly `widen` or `reroute`. Pattern `B.5.2` regulates the abductive loop (hypothesis generation).
* **Projection onto Anti-Loop:** On the 4th attempt, the protocol forcibly switches the agent's `E/E-LOG`. A strict warning is output: *"Consider alternatives (Superposition)"*. The agent is forbidden to continue writing code (Exploit); it is obligated to launch an abductive loop (`U.AbductivePrompt`) and generate 2-3 fundamentally new approaches (Explore).

### 4. **A.15.1 `U.Work`: The Record of Occurrence** (Recording the fact of work)
To make decisions, the agent needs a factual grounding in reality, not illusions from the context window.
* **How it works in FPF:** `U.Work` is an actual, recorded trace in reality (`execution, event, run, actuals, log, occurrence`).
* **Projection onto Anti-Loop:** The `.test_counter.json` file (or any other service tracking file) is the embodiment of `U.Work`. It guarantees that the history of failures is not just text in the chat history (which the LLM might ignore or "forget" due to context fatigue), but a rigid artifact in the file system that dictates the next state.

### 5. **A.21 GateProfilization (OperationalGate)** (Gating and escalation)
The protocol implements a multi-stage gate to assess the quality of work.
* **How it works in FPF:** Patterns `A.21` and `A.6.B` describe the operation of gateways (`OperationalGate`) that aggregate checks and can return `pass|degrade|abstain` states.
* **Projection onto Anti-Loop:** The error counter acts as an `OperationalGate`. If the test passes, the gate opens (`pass`). If there is an error (attempts 1-4), the state degrades (`degrade`), and the agent receives additional checklists or tools. Upon reaching the threshold (5+ attempts), the gate makes an `abstain` decision and escalates the problem to the operator, completely blocking further attempts.

**Summary:**
`GFPF_ANTI_LOOP_PROTOCOL` is not just a "counter in tests". In FPF terms, it is a designed **External Transformer (A.12)** that collects metrics via **U.Work (A.15.1)**, passes them through an **OperationalGate (A.21)** with a set **Enactment Budget (C.24)**, and, if limits are exhausted, forcibly switches the agent's cognitive mode via the **E/E-LOG (C.19)**.
