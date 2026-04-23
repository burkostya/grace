## Core Practice: The "Semantic Exoskeleton & Spatial Navigation" Protocol (XML-DOM for Code)

### Description

**Primary Reference (`.kilocode/rules/rules.md`)**
According to the rulebook, the agent must treat the flat text of the source code as a hierarchical XML document. ALL logical nodes (functions, loops, complex branches, contracts) must be wrapped in paired comment-tags (e.g., `# START_BLOCK_NAME` ... `# END_BLOCK_NAME`).

**Grounding in the GRACE Framework**
This rule is grounded in the physics of the transformer's attention mechanism. It has been experimentally determined that LLMs read, retain, and modify large volumes of context best when it is segmented with paired XML-like tags. In GRACE, code is written primarily for other autonomous agents and machine parsing; human readability is secondary.

**Rationale**
The rationale is twofold:
1. **Distributed Attention:** The tags act as anchors for your distributed attention mechanisms, preventing the model from getting lost within a complex algorithm or losing focus.
2. **Pinpoint Navigation and Patching:** These tags are utilized for navigation from logs directly to the code epicenter (Log Driven Development), as well as for ensuring code patchers operate more correctly. The code itself remains natural (Natural Code) but resides within these semantic transport containers.
