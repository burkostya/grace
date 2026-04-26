## GFPF_GRAPH_PROTOCOL - XML Knowledge Graph Protocol

> **Type:** Architectural (A)  
> **Status:** Stable  
> **Normativity:** Normative

### GFPF_GRAPH_PROTOCOL:1 - Problem frame
Autonomous LLM agents face severe cognitive limitations when navigating large, multi-file codebases because they only ingest a flat sequence of tokens. They naturally lack the spatial orientation that human developers rely on via IDE file explorers and visual dependency trees.

### GFPF_GRAPH_PROTOCOL:2 - Problem
Without a centralized, hierarchical map of the project, agents lose spatial orientation, suffer from context-window amnesia, and make "blind" edits. This leads to hallucinated dependencies and breaking changes across unseen or unreferenced modules.

### GFPF_GRAPH_PROTOCOL:3 - Forces
| Force | Tension |
|-------|---------|
| **LLM Attention Limits vs. Codebase Size** | Agents cannot load an entire project into their context window, but they require global context to make local changes safely. |
| **Hierarchical Relations vs. Flat Text** | Code dependencies form a complex network (graph), but LLMs process text as a sequential linear stream. |
| **Machine Readability vs. Expressiveness** | The map must be rigidly formatted for predictable machine parsing, yet remain expressive enough to capture business logic semantics. |

### GFPF_GRAPH_PROTOCOL:4 - Solution
Require the agent to generate and reference a centralized `AppGraph.xml` knowledge graph before writing code or modifying architecture. Wrap the entire project in an XML projection using strictly named, unique tags (e.g., `<core_logic_py>`, `<process_data_FUNC>`) equipped with semantic `TYPE` attributes and explicit cross-link references (`<CrossLinks><Link TARGET="..." TYPE="..."/></CrossLinks>`). 

### GFPF_GRAPH_PROTOCOL:5 - Archetypal Grounding
* **Tell**: The architecture establishes a semantic, XML-DOM-based codebase map to properly distribute the LLM's attention vectors.
* **Show**: As defined in the `graph-protocol` skill, the graph guarantees unique entity parsing by replacing dots with underscores and appending strict suffixes like `_py`, `_CLASS`, and `_METHOD`.
* **Show**: GRACE strictly instructs the agent to use a "Top-Down Strategy," starting every architectural exploration with `AppGraph.xml` to identify target modules before attempting to read individual files.

### GFPF_GRAPH_PROTOCOL:6 - Bias‑Annotation
This explicitly mitigates **local optimum bias** (where an LLM confidently changes one file while ignoring affected dependent files) and prevents **hallucinated dependencies** (where the model attempts to guess the location of a module instead of checking the deterministic map).

### GFPF_GRAPH_PROTOCOL:7 - Conformance Checklist
- [ ] The root element is exactly `<KnowledgeGraph>`.
- [ ] The first child element describes the project as a whole (e.g., `<PROJECT_NAME_Version_Info>`) and encapsulates `<keywords>`, `<terms>`, and `<annotation>`.
- [ ] Tag names are globally unique and formatted with typological suffixes.
- [ ] Cross-module dependencies are explicitly mapped using the `<Link TARGET="Unique_Tag_Name" TYPE="RELATIONSHIP_TYPE" />` schema.

### GFPF_GRAPH_PROTOCOL:8 - Common Anti‑Patterns and How to Avoid Them
* **Using JSON instead of XML:** Do not use flat JSON. It is an experimental fact that LLM attention mechanisms perform significantly better with explicit, paired opening and closing XML-like tags for segmenting large contexts.
* **Generic tag naming:** Naming tags simply `<file>` or `<function>` breaks spatial uniqueness. You must use `<core_logic_py>` to create an unambiguous semantic anchor for the agent.

### GFPF_GRAPH_PROTOCOL:9 - Consequences
The agent gains reliable "Top-Down" navigational capabilities, drastically reducing the risk of context-window exhaustion and blind architectural breaks. However, it introduces mandatory maintenance overhead: the graph must be meticulously updated during every structural refactoring.

### GFPF_GRAPH_PROTOCOL:10 - Rationale
XML was selected over Markdown or JSON because it generates a natural Document Object Model (DOM) tree. Aligning with the "Spatial Navigation (XML-DOM for Code)" principle, paired tags serve as a highly visible "semantic exoskeleton". This structure maps effectively to the multi-head attention mechanisms inherent to Transformer models, supplying the agent with a durable spatial representation of an otherwise invisible architecture.

### GFPF_GRAPH_PROTOCOL:11 - SoTA‑Echoing
This protocol operationalizes contemporary Agentic RAG practices and Knowledge Graph integrations for LLMs (e.g., GraphRAG) by moving away from primitive lexical chunking toward fully typed, relationship-aware retrieval mechanisms.

### GFPF_GRAPH_PROTOCOL:12 - Relations
* **Enables:** `GFPF_DEVPLAN_PROTOCOL` (The Development Plan's draft code graph strictly demands this exact XML graph schema).
* **Realizes:** `GFPF_SPATIAL_NAVIGATION` (Applying XML-DOM structures to orient codebase exploration).

### GFPF_GRAPH_PROTOCOL:End
