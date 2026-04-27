**1. Semantic Density over Verbosity**
* **Instruction:** When formulating queries for `codebase_search` or writing tags, abandon conversational sentences. Use a dense set of domain terms. 
* **Example:** Instead of querying "where does the login occur", search using dense keywords: "UserSession Redis auth login KEYWORDS".

**2. Mandatory Contract Enrichment**
* **Instruction:** Whenever you generate a `# START_MODULE_CONTRACT` or `# START_CONTRACT` for a function, you MUST include the `KEYWORDS` and `LINKS` sections.
* **Format:** * `# KEYWORDS: [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...; PATTERN(W): ...]`
    * `# LINKS: [USES_API(X): ...; READS_DATA_FROM(Y): ...]`

**3. Pattern and SFT Priming**
* **Instruction:** Explicitly declare the software design patterns being utilized in the `KEYWORDS` section (e.g., `PATTERN: Factory`, `PATTERN: Iterator`). This guarantees that subsequent modifications by subagents will correctly activate the required SFT weights for that specific pattern, preventing architectural degradation over time.
