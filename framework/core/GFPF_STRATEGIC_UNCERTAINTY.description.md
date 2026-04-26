**Core Practice: Strategic Uncertainty and the Criteria Space**

**Primary Reference (`.kilocode/skill/mode-architect/SKILL.md`)**
According to the "Architect" mode rules (Step 1: `THINK_AND_CLARIFY`), the agent is forbidden from immediately matching a user's problem to a known technical solution. Instead, the agent must form a low-dimensional subspace of CRITERIA (evaluation axes) before searching its weights for answers.

**Grounding in the GRACE Framework**
In GRACE, this practice addresses the fundamental way LLM attention mechanisms work. If an LLM immediately attempts to solve a problem, its attention naturally gravitates toward the most statistically common pattern in its training data (a "local optimum" or "early commitment"). By forcing the agent to artificially prolong a state of "strategic uncertainty," we condition the context window. Generating abstract criteria (e.g., speed vs. memory vs. AI-readability) creates dense semantic anchors. When the model later generates solutions, the attention mechanism is heavily weighted by these abstract constraints, drastically improving the mathematical logic of the generated architecture.

**Rationale**
You cannot execute the "HOLD" phase of the `SUPERPOS_COLLAPSE` protocol if you do not know what you are measuring the hypotheses against. By explicitly defining 3 to 5 key success criteria *first*, the agent establishes a rigorous, mathematically sound foundation for decision-making. It separates the "what we value" from the "how we build it."
