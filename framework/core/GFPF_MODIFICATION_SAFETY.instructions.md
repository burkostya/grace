**1. "Read before edit" (Indentation Integrity Protection)**
* **Instruction:** "Never try to guess the exact indentation or phrasing of existing code from memory. BEFORE calling a targeted editing tool (`edit`), you MUST call the read tool (`read`) on the target file. Copy the `oldString` block exactly as it is returned by the system."

**2. Use of Anchors (Protection Against Multiple Matches)**
* **Instruction:** "If you are modifying a common string of code (e.g., `return result`) that might occur multiple times in the file, you must expand the `oldString` capture to include unique GRACE semantic anchors. For example, capture the adjacent `# START_BLOCK_[NAME]` tags or the function declaration to guarantee the uniqueness of the replaced fragment."

**3. "Scar on Code" (Immunization Against Cyclic Refactoring)**
* **Instruction:** "When fixing a complex logical bug inside a block, you MUST add a special comment `# BUG_FIX_CONTEXT: [reason why the old approach didn't work, and why the current one was chosen]` right above the fixed logic. This protects this specific section from 'blind' refactoring by other agents in the future."

**Example of proper usage (Scar on Code):**
```python
# START_BLOCK_VERIFY_DEPENDENCIES: [Iteration and safe import spec checking]
for lib_name in all_libs:
    try:
        spec = importlib.util.find_spec(lib_name)
        # BUG_FIX_CONTEXT: Previously caught ImportError, but find_spec can throw ValueError on malformed paths. Expanded to Exception.
        is_installed = spec is not None
        # ...
```
