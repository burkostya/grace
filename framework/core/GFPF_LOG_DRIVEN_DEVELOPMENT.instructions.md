### **Instructions (Executable Rules for the Agent)**

To successfully apply LDD 2.0, you must strictly follow these rules when writing code and tests:

1. **Strict Log Line Format:** All logs must be easily parsable using regular expressions. The base template is:
   `f"[{CLASSIFIER}][IMP:{1-10}][{FUNCTION_NAME}][{BLOCK_NAME}][{OPERATION_TYPE}] Description [{STATUS}]"`

2. **Semantic Importance Scale (IMP Scale):** The log's importance level helps the LLM's attention mechanism filter out noise. You must use IMP tags:
   * **[IMP:1-3] (Trace):** Local variable dumps in loops.
   * **[IMP:4-6] (Flow):** Start/end of logical blocks, internal function calls, branching.
   * **[IMP:7-8] (I/O & Boundary):** DB access, API calls, file reads.
   * **[IMP:9-10] (Business Logic & AI Belief):** Hypothesis testing, AAG Goal achievement, critical errors. Here you *must* log your "belief" about how the code should work.

3. **Exception Enrichment:** In complex functions, if a failure occurs (IMP:10 level), you are required to output the context of local variables into the log, so the next debugger-agent immediately sees the state of the data without needing to add print statements.

4. **"Talking" Tests (Native Pytest & LDD):** It is strictly forbidden to make tests in the project "silent". In tests (for example, via the `caplog` fixture in `pytest`), you must filter logs with `IMP:7-10` or `[BLOCK_NAME]` tags and force them to be output to the console.

---

### Example

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
