**1. SFT-Priming (Verbalization of the contract before implementation)**
* **Instruction:** "Never start writing the code for a function or algorithm blindly. Before implementation, you MUST verbalize the logic in a docstring contract (minimum 1 paragraph). This is necessary for model priming. Describe: what the block does, what data it expects (Inputs), what it returns (Outputs), and what guarantees (Guarantees) it provides."
* **Example implementation:**
  ```python
  # FUNCTION_CONTRACT:
  # Input: user_id (positive int)
  # Output: Token (if successful) or None (if error)
  # Guarantees: The request is executed in constant time to protect against timing attacks.
  def authenticate(user_id: int) -> Optional[Token]:
      ...
  ```

**2. Semantic Enrichment (Keywords & Links)**
* **Instruction:** "Every generated module must contain `KEYWORDS` (domain, concepts, technologies) and `LINKS` (connections with other modules) sections in its header (inside the semantic exoskeleton). With minimal token cost, this provides the agent with a dense semantic context for the correct correlation of meanings."
* **Example implementation:**
  ```python
  # KEYWORDS: [DOMAIN: E-commerce; CONCEPT: Idempotency; TECH: Stripe API, async_pg]
  # LINKS: [USES_API(Stripe), READS_DATA_FROM(UsersDB)]
  ```

**3. "Code Scars" (Bug Fix Context)**
* **Instruction:** "When using the `edit` tool to fix complex or non-obvious bugs, you MUST add a semantic anchor `# BUG_FIX_CONTEXT: [...]` to the code. Explain why the old (seemingly logical) approach did not work, and why the current one was chosen. This is critically important so that AI in the future does not 'optimize' the fix back into a bug."
* **Example implementation:**
  ```python
  # BUG_FIX_CONTEXT: Issue #156
  # Previous approach: Executed the payment before checking idempotency.
  # Problem: A race condition occurred, leading to double charges.
  # Fix: The idempotency key check occurs STRICTLY BEFORE any mutations in the DB.
  existing_tx = check_idempotency(tx_key)
  ...
  ```
