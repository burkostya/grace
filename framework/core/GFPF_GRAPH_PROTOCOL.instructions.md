**1. General Graph Structure**
* **Instruction:** "Always wrap the knowledge graph in a root `<KnowledgeGraph>` tag. The first child element must contain general project information (e.g., `<PROJECT_NAME_Version_Info>`), including `<keywords>`, `<terms>`, `<annotation>`, and `<BusinessScenarios>` tags."

**2. Tag Naming Standards**
* **Instruction:** "Tag names must be absolutely unique. Replace dots with underscores. You must use suffixes to type the entities: `_py` (for modules/files), `_CLASS` (for classes), `_FUNC` (for functions), or `_METHOD` (for methods). For example: the file `core.py` becomes `<core_py>`, and a `parse` function inside it becomes `<core_parse_FUNC>`."

**3. Attributes and Cross-Links**
* **Instruction:** "Every entity must have a `TYPE` attribute (e.g., `TYPE="BUSINESS_LOGIC"`). For modules, specify the physical path using `FILE="..."`. To link nodes, use a `<CrossLinks>` block with child `<Link TARGET="Unique_Tag_Name" TYPE="RELATIONSHIP_TYPE" />` elements (e.g., `TYPE="CALLS_FUNCTION"` or `USES_API`)."
