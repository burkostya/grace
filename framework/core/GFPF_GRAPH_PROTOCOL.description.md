**Core Practice: The XML Knowledge Graph Protocol (SEMANTIC CODEBASE MAPPING)**

**Primary Reference (`.kilocode/skill/graph-protocol/SKILL.md` & `.kilocode/rules/rules.md`)**
According to the GRACE rules in the KiloCode environment, the agent must generate and maintain a hierarchical project knowledge graph in XML format (`AppGraph.xml`). This serves as the primary map for "Top-Down" navigation (Top-Down Strategy).

**Grounding in the GRACE Framework**
Unlike a human's IDE, an LLM perceives a project as a flat set of tokens. This practice is grounded in the principle of *Spatial Navigation (XML-DOM for Code)*. It has been experimentally proven that the attention mechanisms of large language models are excellent at reading structures wrapped in paired XML tags. Placing the project architecture into an XML tree with cross-links translates an abstract file system into a semantic graph (Knowledge Graph) that the LLM can efficiently parse.

**Rationale**
The main goal of this practice is to give agents the ability to "see" dependencies between files before they start writing code. Without this protocol, agents operate blindly, losing context when working with large codebases. The use of standardized unique tag names (e.g., `<utils_load_data_FUNC>`) and cross-references (`<Link TARGET="...">`) provides a reliable mechanism for referential integrity within the LLM's context window.
