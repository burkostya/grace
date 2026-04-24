**Core Practice: Generation Completeness (Zero Tolerance for Abbreviations)**

**Primary Reference (`.kilocode/rules/rules.md`)**
According to the `.kilocode` rulebook, the agent (LLM) is strictly prohibited from using any forms of abbreviations (e.g., "...", "pass", "etc."). If the model finds that it has generated an abbreviation or skipped logic, it must immediately stop and regenerate the artifact in its entirety.

**Grounding in the GRACE Framework**
Within GRACE, this practice is grounded in the concept of *Cognitive Alignment*. Historically, during the SFT (Supervised Fine-Tuning) phase, LLMs are trained to generate responses for human engineers, causing the models to become "lazy" and truncate long code sections with comments like `// existing code remains unchanged`. However, in the GRACE paradigm, the agent writes code *exclusively* for other autonomous agents and machine parsing. Another agent or a code patcher physically lacks the "human intuition" to understand what is hidden behind an ellipsis.

**Rationale**
Any syntactic abbreviation, no matter how small, instantly breaks the autonomous agent swarm pipeline. Missing context requires putting a "Human-in-the-loop" to manually restore the code. 100% full artifact generation is a "zero-tolerance" baseline, ensuring that a machine interface or the next agent can correctly interpret, assemble, and execute the code.
