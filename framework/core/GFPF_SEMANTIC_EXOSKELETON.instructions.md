**1. Block Segmentation**
* **Instruction:** "For complex multi-step algorithms (Complexity > 7), segmentation via START-END code blocks is mandatory. Before a logical step, write `# START_BLOCK_[NAME]: [Brief description]`. After the logic concludes, close it with `# END_BLOCK_[NAME]`".

**2. Natural Code Containment**
* **Instruction:** "Write the algorithm itself (the body of the blocks) as you see fit, adhering to DRY and modularity principles. However, all of this code MUST be placed within semantic transport containers (block tags). This enriches the code with a semantic description for yourself and other agents".

**3. Navigation Invariant ("Top-Down" Strategy & Edit Rules)**
* **Instruction:** "When using the `edit` tool for pinpoint edits, expand the search area by including unique semantic anchors (`# START_BLOCK` / `# END_BLOCK`) in the `oldString` to prevent accidental matches elsewhere in the file".
