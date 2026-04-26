**1. Phase: SKELETON (Top-Down Planning)**
* **Instruction:** "When creating any architectural plan, business requirement, or system specification, you must NOT start writing the detailed content immediately. First, instantiate the `$START_DOCUMENT_PLAN` block. List all sections, use cases, and goals as a bulleted index. Only proceed to generate the body after this entire skeleton is complete in your output."

**2. Phase: BOUNDING (Semantic Context Switching)**
* **Instruction:** "Wrap every discrete logical section of your document in explicit `$START_[NAME]` and `$END_[NAME]` tags. Treat these tags as absolute boundaries. When generating content inside a block, do not reference or begin writing implementation details that belong in a different section."

**3. Phase: CONTRACTING (Explicit Intent Declaration)**
* **Instruction:** "For every major architectural decision, feature, or requirement block, begin with a `$START_CONTRACT`. You must explicitly declare the `PURPOSE` (what it does), the `RATIONALE` (why this approach was chosen over alternatives), and `ACCEPTANCE_CRITERIA` (how a future agent will test it). Never assume the 'Why' is obvious."
