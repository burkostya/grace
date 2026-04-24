## Pattern: GFPF_SFT_PRIMING (Supervised Fine-Tuning Priming)

### Description
**GFPF_SFT_PRIMING** is a cognitive practice of aligning the model's current context with the patterns of its initial training. During the SFT (Supervised Fine-Tuning) phase, language models are usually trained to generate function code directly from its textual description (docstring).

If an agent starts writing complex code immediately after the function signature, it relies on an "empty" context, leading to hallucinations or suboptimal solutions. The SFT-Priming practice forces the agent to *first* verbally detail the logic in natural language (at least 1 paragraph) inside the docstring, and only then generate executable code. The text acts as a semantic trigger, activating the necessary neural pathways for high-quality code generation.

