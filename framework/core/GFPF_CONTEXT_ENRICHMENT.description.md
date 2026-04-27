**Core Practice: Context Enrichment (RAG Optimization & SFT Activation)**

**Primary Reference (`.kilocode/rules/rules.md`)**
According to the `.kilocode` rulebook, relying on standard human-readable code and sparse comments is insufficient for a multi-agent system. The rules mandate the use of explicit `KEYWORDS` and `LINKS` metadata sections (e.g., `USES_API(X)`, `READS_DATA_FROM(Y)`) injected directly into the semantic transport containers of the code.

**Grounding in the GRACE Framework**
In standard Software Engineering (SWE), code is written for compilers and human developers. In GRACE, code is a dataset consumed by Large Language Models via Retrieval-Augmented Generation (RAG). When an LLM searches a massive codebase using a vector database, standard code syntax often lacks the semantic "density" required for accurate retrieval. 

By injecting dense semantic markers (`KEYWORDS` and `LINKS`) into the code's `CONTRACT` blocks, we artificially inflate the semantic weight of the text chunk. This practice achieves three critical LLM-native goals:
1.  **Semantic Correlation:** It establishes relationships between modules without the computational overhead of building a full Abstract Syntax Tree (AST) or Call Graph.
2.  **Chunk Enrichment (RAG Optimization):** It drastically improves semantic search accuracy. A query for "database authentication" will precisely hit the code chunk tagged with `[DOMAIN(8): Auth; TECH(9): Redis]`, avoiding irrelevant matches.
3.  **SFT Activation:** Tagging code with architectural patterns (e.g., `[PATTERN(X): Singleton]`) acts as a prompt-priming mechanism, activating the specific neural weights acquired during the model's Supervised Fine-Tuning (SFT) phase, significantly improving code generation quality.

**Rationale**
The assumption that metadata is "overhead" is a human-centric fallacy. For an AI swarm, this minimal token consumption provides instant cognitive alignment. It ensures "Zero-Context Survival," allowing an agent dropped blindly into a file to instantly understand its architectural role, dependencies, and intended patterns without needing the chat history of the agent who originally wrote it.
