---
name: mode-code
description: MANDATORY MODE for code implementation and testing. Must be invoked to execute the Development Plan, ensure 100% test coverage, and apply semantic markup.
---

**Code Mode Main Workflow**

Your primary goal in this mode is to **execute**, not plan. You implement solutions designed in `Architect` mode, create testing infrastructure, and ensure technical and semantic completeness of the code.

**PRIMARY TASK CLASSIFICATION:**
To ensure correct Attention mechanism operation and activation of relevant rule sections, you **MUST** explicitly output the following parameters in the console in your very first message:
1. `"PROJECT_TYPE_DEFINED: [Lesson | Plugin System]"` (depends on whether you are in a lesson/app folder or working with a shared plugin/microservice architecture).
2. `"TASK_TYPE_DEFINED: [Code and Tests | Tests Only]"` (depends on Orchestrator/Architect instructions).
3. As you follow the steps below, if you encounter a `# START_SECTION_...` block and its `# TRIGGER` matches your classification, you **MUST** write to the console (logging your cognitive process): `[ROUTING] Section activated: <SECTION_NAME>`. If a trigger indicates skipping a step, write: `[ROUTING] Step <N> SKIPPED according to section <SECTION_NAME>`.

**Step-by-step Workflow:**

*   **Step 0: `INITIALIZE_TODO` (Tasks Initialization)**
    *   **Goal:** Formulate a clear action plan based on Architect instructions.
    *   **Actions:**
        1. You **MUST** call `todowrite` in the very first message (after `[ROUTING]` classification).
        2. The task list should include these steps if not already provided by the architect:
            - `[ ] STUDY_THE_PLAN: Review DevelopmentPlan.md and business_requirements.md`
            - `[ ] VERIFY_ENVIRONMENT: Check library versions via test_lib.py`
            - `[ ] IMPLEMENT_CODE: Implement logic with semantic markup and LDD logging`
            - `[ ] IMPLEMENT_TESTS: Create tests in the root tests/ folder with Anti-Loop Protocol (conftest.py) and log output IMP:7-10`
            - `[ ] VERIFY_TESTS: Run tests and achieve 100% PASS`
            - `[ ] FINAL_AUDIT: Perform final log audit for logical errors`
            - `[ ] LAUNCHER_DESIGN: Create/update a reliable entry point (run_lesson_X.py)`
            - `[ ] UPDATE_THE_GRAPH: Update AppGraph.xml after successful testing`

*   **Step 1: `STUDY_THE_PLAN` (Artifact Review)**
    *   **Goal:** Fully immerse yourself in the task context.
    *   **Actions:**
        1. Your first duty is to find and study `DevelopmentPlan.md`, `business_requirements.md`, and `requirements.txt`. (Note: in plugin architecture, these files may have a module prefix and reside in the `plans/` folder, e.g., `plans/import_csv_req.md`). Use `read` to study files.
        2. Do not start writing code until you understand the architectural design and Data Flow.

*   **Step 2: `VERIFY_ENVIRONMENT` (Environment Check)**
    *   **Goal:** Ensure library versions are correct.
    *   **Actions:**
        1. Find the `test_lib.py` script and execute it (`bash`). If it doesn't exist, create and run it to check versions of requested libraries.
        2. **Version Hypothesis:** If you encounter errors using libraries that seem logically correct, check if the installed versions differ from those you were trained on. Study existing code in the project to understand how to use them. If no examples are available, **MUST** request up-to-date snippets via the `Context7` MCP server.
        3. **Priority to Reliable Libraries.** Your training was particularly thorough on libraries used for internal LLM calculators. These high-reliability libraries should be prioritized: math, random, statistics, decimal, datetime, time, re, os, sys, csv, json, sqlite3, xml.etree.ElementTree, configparser, pickle, base64, hashlib, collections, itertools, functools, logging, argparse, typing, uuid, zipfile, tarfile, gzip, zlib, shutil, tempfile, numpy, pandas, scipy, sklearn, matplotlib, seaborn, h5py, openpyxl, requests, lxml, PIL, reportlab, sympy, dateutil, pytz.

*   **Step 3: `IMPLEMENT_THE_CODE` (Implementation and Semantic Encapsulation)**
    
    # START_SECTION_SKIP_LOGIC
    # TRIGGER: TASK_TYPE_DEFINED: Tests Only
    Step 3 is SKIPPED. You proceed directly to Step 4 for testing existing code.
    # END_SECTION_SKIP_LOGIC

    # START_SECTION_WRITE_CODE
    # TRIGGER: TASK_TYPE_DEFINED: Code and Tests
    *   **Goal:** Write working code that can be maintained by another isolated AI agent in the future.
    *   **Generation Principles and SFT Correlation:**
        1. **SFT Priming (Docstrings):** Remember that during SFT, you were trained to generate function code directly from docstrings. To activate the most reliable weights, you **MUST** first write a detailed docstring (at least 1 paragraph) describing the logic, and only then proceed to code.
        2. **Keywords & Patterns:** Using `KEYWORDS` (e.g., `PATTERN(X): Singleton`) is also an SFT pattern. Correct task classification significantly improves generation quality.
        3. **Resolving Markup Conflicts:** If code generation results in syntax errors (especially indentation), it might be due to paired tag conflicts with SFT patterns. In this case, **try temporarily removing paired tags inside the function body** to ensure compatibility with clean code SFT patterns.
        4. **Segmentation Criterion:** For simple algorithms (Complexity <= 7), you can omit block-level comments inside the function. For complex algorithms (Complexity > 7), use segmentation to improve attention correlation between logs and code steps.
        5. **Zero-Context Survival:** Use `CONTRACT`, `KEYWORDS`, and `RATIONALE` sections. An agent coming to fix your code will only see the file itself.
        6. **Semantic Exoskeleton (XML-DOM):** Wrap logical nodes in paired tags `# START_BLOCK...` / `# END_BLOCK...`.
        7. **Log Driven Development (LDD):** Use strict log format `[IMP:1-10]`. Record "AI Belief State" at `[IMP:9-10]`.
        8. **Semantic Distillation:** Markdown plans are CoT (Chain of Thought). You **MUST** extract business requirements from `.md` files and transfer them to `# START_CONTRACT` and `# START_RATIONALE` tags directly in the code.
    # END_SECTION_WRITE_CODE

*   **Step 4: `IMPLEMENT_TESTS` (Testing Infrastructure and Telemetry)**
    *   **Goal:** Create tests that generate context for fixes and prevent agent looping.
    *   **Actions (Common for all modes):**
        1. **Backend and Log Selection (LDD Telemetry):** Write `pytest` tests in the root `tests/` folder. Use native imports. **STRICTLY FORBIDDEN** to use `subprocess.run` for business logic testing. Tests MUST include console output of results and selection of critical log lines via `[IMP:7-10]`. **To ensure log output to console, use explicit print statements for filtered logs or configure caplog output to stdout.** 100% PASSED is not final proof; the true criterion is Semantic Trace Verification.
        2. **Zero Hardcode Rule and `tmp_path`:** Forbidden to use hardcoded paths or `sys.path.append`. Always use the built-in `tmp_path` fixture for all test files.
        3. **Anti-Loop Protocol:** When creating/modifying tests, you **MUST** implement an attempt tracking mechanism.
            *   **Attempt Counter:** Use `.test_counter.json` to store failed run counts. Counter resets to 0 only at 100% PASS.
            *   **CRITICAL OUTPUT RULE:** You **MUST** output a checklist and attempt status **EVERY TIME** the test runs if the attempt counter > 0.
            *   **TEST ARCHITECTURE (Anti-Loop Safety):**
                - **FORBIDDEN** to call `update_test_counter(False)` (increment) inside test files if using session hooks.
                - **conftest.py:** Session hook logic (`pytest_sessionstart`, `pytest_sessionfinish`) and counter management must be in `tests/conftest.py`.
                - **PRIORITY CALL:** Always run tests via `python -m pytest [test_path] -s -v`.
            *   **Attempt 1-2 (Checklist):** On failure, output a `CHECKLIST` of common errors.
                **Experience Feedback Loop:** You **MUST** add new items to the `CHECKLIST` based on encountered errors.
            *   **Attempt 3 (External Help):** Output: "Use MCP `tavily` or `Context 7` to find a solution online."
            *   **Attempt 4 (Reflection):** Output: "WARNING: Looping risk! Pause and reflect. Are you repeating a failed strategy? Consider alternatives (Superposition)."
            *   **Attempt 5+ (Escalation):** Output: "CRITICAL ERROR: Agent looping detected. STOP. Formulate a help request for an operator."
        4. **UI (Headless Testing):** Emulate controller calls without starting the server.
        5. **Mandatory Semantic Markup in Tests.** Same rules as main code.
        6. **Test Atomicity.** Create atomic tests for individual functional elements.
        7. **Integration Test.** Also have a full-scenario pass test.
        8. **One-Shot Example (LDD + Anti-Loop):**
            ```python
            # START_FUNCTION_test_backend_logic
            # START_CONTRACT:
            # PURPOSE: Verify business logic and LDD trace trajectory.
            # INPUTS: caplog (pytest fixture)
            # KEYWORDS:[PATTERN(7): LDD; CONCEPT(8): Telemetry]
            # COMPLEXITY_SCORE: 5
            # END_CONTRACT
            def test_backend_logic(caplog):
                """
                Test verifies not just the function result, but the presence of 
                corresponding log entries with correct importance levels (IMP).
                """
                # IMPORTANT: Set log capture level
                caplog.set_level("INFO")
                
                # START_BLOCK_EXECUTION:[Call business logic]
                df = calculate_trig(A=2.0, B=1.0, x_min=-2, x_max=2)
                # END_BLOCK_EXECUTION

                # START_BLOCK_LDD_TELEMETRY: [Output trajectory slice for agent]
                # IMPORTANT: Printing logs [IMP:7-10] is done BEFORE business asserts 
                # so that on failure, the agent still sees the algorithm trajectory.
                found_log = False
                print("\n--- LDD TRAJECTORY (IMP:7-10) ---")
                for record in caplog.records:
                    if "[IMP:" in record.message:
                        try:
                            imp_level = int(record.message.split("[IMP:")[1].split("]")[0])
                            if imp_level >= 7:
                                print(record.message)
                            if imp_level >= 9 and "calculate_trig" in record.message:
                                found_log = True
                        except (IndexError, ValueError):
                            continue
                # END_BLOCK_LDD_TELEMETRY

                # START_BLOCK_VERIFICATION:[Business checks and anti-illusion]
                assert not df.empty, "Error: Business logic returned empty result"
                
                # Anti-Illusion: 100% PASSED without reading [IMP:9] logs is a failure.
                assert found_log, "Critical LDD Error: Business logic failed to output control log [IMP:9]-calculate_trig"
                # END_BLOCK_VERIFICATION
            # END_FUNCTION_test_backend_logic
            ```

    # START_SECTION_LESSON_TESTS
    # TRIGGER: PROJECT_TYPE_DEFINED: Lesson
    In simple lessons, it is allowed to create a test DB and schema (CREATE TABLE) directly inside the test using `tmp_path`.
    # END_SECTION_LESSON_TESTS

    # START_SECTION_PLUGIN_TESTS
    # TRIGGER: PROJECT_TYPE_DEFINED: Plugin System
    For integration projects, follow SWE practices:
    - **Read-Only vs Ephemeral Data:** Put reference files in `tests/test_data/`. Create isolated DBs via plugin calls (e.g., `init_db(tmp_path)`).
    - **Dependency Injection (DI) > Mocks:** Avoid `unittest.mock.patch` for internal state. Pass paths explicitly.
    - **Invariant Testing (ETL):** Verify logical invariants.
    - **SWE Heuristics:** Isolate parsing logic. Test with static Data-Driven Fixtures.
    # END_SECTION_PLUGIN_TESTS

*   **Step 5: `CHECK_LOG` (Final Log Audit)**
    *   **Goal:** Check the log for logical errors that tests might have missed.
    *   **Actions:** Read the entire log and conclude if the app works correctly.

*   **Step 5.1: `LAUNCHER_DESIGN` (Reliable Launch Patterns)**
    
    # START_SECTION_LAUNCHER
    # TRIGGER: PROJECT_TYPE_DEFINED: Lesson
    *   **Goal:** Create an entry point (e.g., run_lesson_X.py) resistant to environment issues.
    *   **Actions:**
        1. **Lazy Import:** Import heavy libraries (gradio, numpy) inside `main()`.
        2. **Interrupt Handling:** Wrap server start in `try-except KeyboardInterrupt`.
        3. **Interactivity:** Set `inbrowser=True` in `ui.launch()`.
        4. **Log Duplication:** Configure `logging` to output to both file and `stdout`.
    # END_SECTION_LAUNCHER

    # START_SECTION_SKIP_LAUNCHER
    # TRIGGER: PROJECT_TYPE_DEFINED: Plugin System
    Step `LAUNCHER_DESIGN` is SKIPPED. Isolated plugins don't need their own entry point.
    # END_SECTION_SKIP_LAUNCHER

*   **Step 5: `PREPARE_TEST_GUIDE` (QA Artifact)**
    *   **Goal:** Prepare a semantic bridge for an independent QA tester.
    *   **Actions:**
        1. Create `tests/test_guide.md`.
        2. Describe required input data, SQL queries for verification, and expected `[IMP:9-10]` log markers.

*   **Step 6: `UPDATE_THE_GRAPH` (Finalize Architectural Map)**
    *   **Goal:** Keep `AppGraph.xml` up to date.
    *   **CRITICAL RULE:** Updating `AppGraph.xml` is strictly the final step after passing all tests. To update AppGraph.xml, you MUST first load the mandatory skill('graph-protocol').

