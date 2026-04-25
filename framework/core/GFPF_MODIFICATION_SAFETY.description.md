**Core Practice: "Modification Safety and Code Scarring" Protocol**

**Primary Reference (`.kilocode/rules/rules.md`)**
According to the "Navigation and Analysis" section in `rules.md`, the agent must follow strict rules when modifying existing code using editing tools (such as `edit`). The main principles of this protocol are "Read before edit" and the "Scar on Code" rule.

**Grounding in the GRACE Framework**
In multi-agent systems (Swarm), code is maintained by different agents who do not share a single chat history. When an agent fixes a complex bug, it changes an "obvious" but incorrect path to a "non-obvious" but working one. If no semantic trace is left, the next agent performing a refactoring might "optimize" the code back, reintroducing the bug and creating an infinite loop of system degradation. Targeted string replacement tools are also prone to indentation hallucinations, causing syntax errors in Python.

**Rationale**
This pattern serves two purposes:
1. Guaranteeing the surgical precision of `replace` operations via mandatory prior retrieval of the actual tokens and indentation from the file.
2. Using `# BUG_FIX_CONTEXT` comments as "scars" that transfer the bug fix context to future agent instances (Zero-Context Survival), thereby immunizing the codebase against repeating the same errors.
