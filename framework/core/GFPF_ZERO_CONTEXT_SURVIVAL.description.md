## Core Practice: The "Zero-Context Survival" Protocol (Production-Quality Code with Built-in Documentation)

### Description

**Primary Reference (`.kilocode/rules/rules.md` & "How LLM Thinks" Book, Chapter 13.3)**
According to `.kilocode/rules/rules.md` (Principle 5), code is generated primarily for other autonomous agents and machine parsing; human readability is secondary. The Zero-Context Survival pattern requires that every logical module or file be completely self-sufficient. It must contain embedded semantic documentation (Contracts, Rationale, Module Map) directly within the file.

**Grounding in the GRACE Framework**
In multi-agent systems or with every new AI assistant call, the context "burns out" (is lost). An agent arriving to fix a bug does not see the dialogue history (e.g., your long architectural discussions). The LLM reads the file strictly autoregressively (token by token from left to right). The explicit presence of semantic meta-information at the beginning of a file or function forcefully forms the correct "attention vector" and activates the necessary neural network weights (trained during the SFT stage) **before** it begins to read or modify the algorithm itself.

**Rationale**
* **Elimination of Agent "Blindness":** The file contains its own "contract". The agent immediately understands *what* this code does, what its external dependencies are, and what constraints apply.
* **SFT-Activation (Supervised Fine-Tuning):** Describing the logic in plain words before the code switches the model into a mode it is accustomed to from training (where high-quality code always followed a detailed comment/task description).
* **Protection against Regression:** By leaving semantic "scars" in the code after fixing bugs, you immunize the autonomous swarm (agents) against endless looping and repeating the exact same mistakes in the future.

