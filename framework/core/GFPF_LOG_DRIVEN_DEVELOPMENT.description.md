## GFPF_LOG_DRIVEN_DEVELOPMENT (LDD 2.0 & AI Belief State)

### **Description (Rationale and Theory)**
In traditional development, tests are needed to check invariants (a green/red `assert`). For an AI agent, a "silent" test returning only an `AssertionError` is useless—it deprives the agent of the execution context and forces it to hallucinate about the causes of the error, which often leads to endless debugging cycles ("Anti-Loop").

The Log Driven Development (LDD 2.0) pattern solves this problem by turning logs into a **transport layer for context transfer between agents**. The core idea is to embed structured logs into the code that not merely record facts, but also reflect the "AI Belief State"—that is, how the agent understands the current stage of the business logic. When running tests, these logs are aggregated and outputted so that the testing agent (QA or Debugger) can "read the mind" of the coder-agent and see the exact path of the algorithm up to the point of failure.

---

### Application Example for an Engineer

Imagine an agent is writing an order processing function.

**How NOT to write (standard code):**
```python
def process_order(order_id):
    logger.info(f"Processing order {order_id}")
    order = db.get(order_id)
    if not order:
        raise ValueError("Order not found")
    # ... logic ...
```
*Why this is bad for an agent:* If the test fails, the next agent will only see `ValueError: Order not found` in the traceback. It will not understand in which block this happened and what other data was in the context.

**How to write CORRECTLY (in the LDD 2.0 paradigm):**
```python
def process_order(order_id):
    # START_BLOCK_FETCH_ORDER
    try:
        logger.debug(f"[OrderSys][IMP:5][process_order][FETCH_ORDER][DB_Call] Fetching order from DB [PENDING]")
        order = db.get(order_id)
        if not order:
            logger.critical(f"[OrderSys][IMP:10][process_order][FETCH_ORDER][StateEnrichment] Expected order dict, got None. Local vars: order_id={order_id} [FATAL]")
            raise ValueError("Order not found")
            
        logger.info(f"[BeliefState][IMP:9][process_order][FETCH_ORDER][Verify] Order fetched, expected status is 'NEW', got '{order.status}'. Proceeding to payment. [SUCCESS]")
    # END_BLOCK_FETCH_ORDER
```

And in the test itself (`test_order.py`), the agent will write the assertion in such a way as to extract these logs and show them in the report output. Thus, when you assign the Debug-agent to fix a bug, its context will contain the entire chain of reasoning and the state of variables at the moment of the crash.
