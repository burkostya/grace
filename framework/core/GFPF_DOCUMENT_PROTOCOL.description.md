### 1. Top-Down Detailization (The $DOCUMENT_PLAN)
According to FPF and GRACE, an LLM must never begin detailing a complex solution without first mapping the entire territory.
* **Pattern `Cognitive Priming`:** By forcing the generation of a `$DOCUMENT_PLAN` (a table of contents or high-level schema) at the very top of a document, we "prime" the LLM's context window. 
* **Engineering rationale:** Because LLMs are autoregressive, the tokens they have already generated heavily influence the next tokens. If the LLM generates a complete structural skeleton first, its attention mechanism will constantly refer back to this skeleton while generating the heavy body text later, drastically reducing the probability of "hallucinations" or context drift.

### 2. Semantic Context Switchers (The $START and $END Tags)
Just as `GFPF_SPATIAL_NAVIGATION` uses XML-DOM for code, the Document Protocol uses rigid tags for prose.
* **Pattern `Semantic Segmentation`:** The use of `$START_SECTION_NAME` and `$END_SECTION_NAME` acts as a hard boundary for the LLM's attention.
* **Engineering rationale:** These tags act as a localized "focus mode." When the agent is inside a `$START_...` block, the tags signal to the model's weights that the scope is strictly limited to the current topic, preventing it from prematurely bleeding information from or into other sections.

### 3. Explicit Intent Definition (The Contract)
Before any artifact, use case, or requirement is described, its meta-properties must be declared.
* **Pattern `Artifact Contract`:** Every major block must have a `PURPOSE`, `RATIONALE`, and `ACCEPTANCE_CRITERIA` defined.
* **FPF alignment:** This aligns with the `U.MethodDescription` concept. FPF forbids mixing *what* is being built with *why* it is being built. By explicitly stating the `RATIONALE` (Why) and `PURPOSE` (What), we protect the design from future autonomous agents who might otherwise refactor the code incorrectly because they lacked the business context.

### Fundamental Summary (Architectural Rationale)
The Document Protocol is the application of the `GFPF_SEMANTIC_EXOSKELETON` to natural language processing. It treats project plans and requirements not as human-readable prose, but as an API for the LLM's cognitive engine—structuring thought *before* execution.
