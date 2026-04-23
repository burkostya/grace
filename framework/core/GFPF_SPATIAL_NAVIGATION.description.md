### Pattern: GFPF_SPATIAL_NAVIGATION (XML-DOM for code)

**Description:**
The Spatial Navigation pattern dictates treating the flat text of the source code as a hierarchical XML document. Within this pattern, all logical nodes (algorithmic steps inside functions) are wrapped in paired tags like `# START_BLOCK_[NAME]` and `# END_BLOCK_[NAME]`. 

These are not "human comments," but a specific optimization for the distributed attention mechanisms of LLMs. It has been experimentally proven that the model reads and retains large context much better if it is strictly segmented with XML-like tags. Furthermore, these tags act as reliable "semantic anchors" for navigating directly from execution logs to the necessary code section, and they guarantee the correct operation of automatic code patching (editing) tools.

*Application Example:*
```python
def process_data(data):
    # START_BLOCK_VALIDATION: [Input data validation]
    if not data:
        return False
    # END_BLOCK_VALIDATION
    
    # START_BLOCK_TRANSFORMATION: [Normalization and cleaning]
    processed = [d.strip().lower() for d in data]
    # END_BLOCK_TRANSFORMATION
    
    return processed
```
