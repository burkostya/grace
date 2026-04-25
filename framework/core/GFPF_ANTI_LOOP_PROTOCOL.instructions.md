When developing, modifying, or running tests (in `mode-code` or `mode-debug` mode), you MUST implement and adhere to the `Anti-Loop Protocol` attempt tracking mechanism:

1.  **State Tracking (Counter):** Use a utility file (e.g., `.test_counter.json`) to persistently store the number of failed runs. The counter must reset to 0 **only** upon 100% successful test passage (PASS).
2.  **Architectural Isolation:** The logic for managing the counter (e.g., using `pytest_sessionstart` and `pytest_sessionfinish` hooks) must strictly reside in the configuration file `tests/conftest.py`. It is strictly forbidden to update or increment the counter inside the business logic tests themselves.
3.  **Critical Output Rule (Escalation Path):** If the failed attempt counter is greater than 0, you MUST output the current escalation status to the console every time a test fails:
    * *Attempt 1-2 (Checklist):* Output a list (CHECKLIST) of common typical errors. Implement an Experience Feedback Loop — if a new unique error is encountered, update the checklist for the future.
    * *Attempt 3 (External Help):* Explicitly output a recommendation in the logs to use external MCP tools (e.g., `tavily` to search for documentation on the internet) to break the agent's information vacuum.
    * *Attempt 4 (Reflection):* Output a strict system warning: *"WARNING: Looping risk! Pause and reflect. Are you repeating a failed strategy? Consider alternatives (Superposition)."*. The agent must stop and generate 2-3 alternative approaches before writing new code.
    * *Attempt 5+ (Escalation):* Forced halt. The agent must output *"CRITICAL ERROR: Agent looping detected. STOP. Formulate a help request for an operator."* and cease attempts at independent correction.

This pattern turns "blind" testing scripts into an intelligent monitoring system for the agent's "health," which is critically important in the GRACE architecture. Let me know if you'd like to explore how this protocol integrates with Log Driven Development (LDD)!
