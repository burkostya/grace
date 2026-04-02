# XML Knowledge Graph Generation Prompt

**Objective:**

Create a hierarchical and networked knowledge graph based on the provided project codebase in XML format. The graph should serve as a high-level semantic map for a RAG AI agent, assisting in navigation, understanding code structure, dependencies, and control flows.

**General Graph Structure:**

1.  Wrap the entire graph in a root `<KnowledgeGraph>` tag.
2.  The first child element should describe the project as a whole, e.g., `<PROJECT_NAME_Version_Info>`. It must contain global `keywords`, `terms`, and `annotation` for the entire project, as well as a `<BusinessScenarios>` section.

**Rules for Graph Elements:**

**I. Tag Naming and `TARGET` in `<Link>`:**

1.  **Uniqueness:** Each tag name must be unique within the document.
2.  **Formatting:**
    *   Replace dots (`.`) with underscores (`_`).
    *   Add a type suffix to the tag name: `_py` (module), `_CLASS` (class), `_FUNC` (function), `_METHOD` (method).
    *   Example: `utils.load_data` -> `<utils_load_data_FUNC>`.
3.  **Attributes:** Use `FILE="..."` for modules and `NAME="..."` for other entities to store original names.

**II. Entity Tag Structure:**

1.  **`TYPE` Attribute:** Mandatory (e.g., `DATA_PROCESSING_MODULE`, `IS_CLASS_OF_MODULE`, `IS_METHOD_OF_CLASS`).
2.  **Child Elements:** `<keywords>`, `<terms>`, `<annotation>`.
3.  **Hierarchy:** Entities are nested hierarchically (module -> class -> method).
4.  **Relationships (`<CrossLinks>`):**
    *   Use the tag `<Link TARGET="Unique_Tag_Name" TYPE="RELATIONSHIP_TYPE" .../>`.
    *   Relationship types: `CALLS_METHOD`, `CREATES_INSTANCE_OF`, `SENDS_EVENT_TO`, etc.

**III. Global `<ProjectCrossLinks>` Section:**

*   At the end of the graph, inside the project's root tag, a global `<ProjectCrossLinks TYPE="MODULE_INTERACTIONS_OVERVIEW">` section can be added to describe high-level interactions between modules.
