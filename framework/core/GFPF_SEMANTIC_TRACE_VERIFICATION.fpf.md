In FPF, the goal is to rigorously connect what we *claim* a system can do with actual, auditable *evidence* of its execution within a specific scope. Here is how the GRACE Semantic Trace Verification technique maps directly to FPF patterns:

### 1. `U.ClaimScope (G)`: The Semantic Contract
In FPF, a claim (`G`) defines the epistemic boundary of what we assert to be true about a system.
* **GRACE Mapping:** The `START_CONTRACT`, `INVARIANTS`, and `RATIONALE` blocks form the `U.ClaimScope`. When the agent writes the contract, it is formally defining the *Claim Scope*—asserting that the module will transform specific inputs into outputs while maintaining specific states.

### 2. `U.WorkScope`: The Actual Execution (Capability)
In FPF, the work scope represents the actual operational capability of the target system. 
* **GRACE Mapping:** "The Green Test Trap" is an illusion where a binary test pass creates a false assumption that the `U.WorkScope` fully covers the `U.ClaimScope`. An AI might write a test that mocks internal logic, meaning the actual `U.WorkScope` (the real capability) is dangerously narrow, even if the test passes.

### 3. Evidence Collection & Freshness (R)
FPF requires continuous or specific evidence to prove that the Work Scope covers the Target Slice. 
* **GRACE Mapping:** A simple "test passed" console output is considered *low-fidelity evidence*. The LDD traces—specifically the high-importance `[IMP:7-10]` markers that log business logic and the AI's "Belief State"—serve as the high-fidelity **Evidence (R)**. Generating these traces provides the necessary *evidence freshness* to prove the algorithm actually executed the steps claimed in the contract.

### 4. Scope-Sensitive Guards (The Verification Algebra)
FPF dictates the use of guards with patterns like `Scope covers TargetSlice`.
* **GRACE Mapping:** The act of *Semantic Verification* (Step 4 of the Debug protocol) is the implementation of an FPF Guard. The agent is instructed to perform the following mental algebra: 
    * *Does the Evidence (LDD logs) prove that the `U.WorkScope` (actual execution path) covers the `U.ClaimScope` (the contract) for this `U.ContextSlice` (the specific test run)?* * If the trace is missing or ambiguous, the Guard fails, and the agent must use "Dynamic Probing" to gather deeper evidence before the claim can be assured.

**Summary in FPF Terms:**
Semantic Trace Verification is an **Assurance Pattern** that prevents capability hallucinations. It mandates that assertions about a system (`U.ClaimScope`) cannot be validated by weak binary tests, but must be guarded by deep, auditable execution traces (**Evidence**) proving that the system's true capability (`U.WorkScope`) successfully covers the intended constraints.
