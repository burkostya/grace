---
type: meta_protocol
version: 1.1
---
# GFPF (GRACE First Principles Framework) Framework Meta-Protocol

<description>
This file defines the meta-rules for agents interacting with the framework directory. It dictates how to name practices and how to parse the knowledge base.
</description>

<naming-convention>
1. All core techniques MUST start with `GFPF_` (GRACE First Principles Framework).
2. Followed by short, LLM-descriptive tokens in SNAKE_CASE and CAPITALS.
3. Examples: 
   - `GFPF_SUPERPOS_COLLAPSE`
   - `GFPF_SEMANTIC_EXOSKELETON`
</naming-convention>

<agent-directives>
- When learning a concept, read the `*.description.md` file.
- When executing a task, strictly bind your context to the `*.instructions.md` file.
- When evaluating architectural compliance, cross-reference with `*.fpf.md`.
</agent-directives>
