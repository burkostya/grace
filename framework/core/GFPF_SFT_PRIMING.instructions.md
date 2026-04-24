### Instructions (For the Agent)

**1. Prohibition on immediate logic generation:**
* When creating a new function or a complex code block, it is strictly forbidden to proceed with writing executable instructions (loops, conditions) immediately after declaring the signature `def FunctionName(...):`.

**2. Mandatory verbalization (Docstring Priming):**
* Immediately after the function signature, you must open a docstring block and describe in detail, in natural language, what this function does.
* The description must be **at least 1 full paragraph** long.
* The description must explicitly mention the main algorithmic steps, data structures, and business logic.

**3. Transition to code:**
* Only after closing the docstring block are you allowed to start generating the target code. The generated code must be a logical continuation and implementation of what was described in the text paragraph above.
