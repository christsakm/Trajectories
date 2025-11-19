# Trajectory Search Tool (traj_search.py)

A Python utility for searching and analyzing coding agent trajectory files (.traj).

## Installation

No installation needed! Just run the script with Python 3.6+:

```bash
python traj_search.py [options] <traj_file>
```

## Important Differences from grep/ripgrep

⚠️ **Case Sensitivity**: Searches are **case-INsensitive by default** (opposite of grep)
- ✅ Default behavior: case-insensitive (like `grep -i`)
- Use `--case-sensitive` to make searches case-sensitive
- `-i` flag now supported (but redundant since it's already the default)

**Why?** Trajectory analysis often involves searching for variable names, function names, and error messages that may appear in different cases.

## Quick Start

```bash
# Get statistics about a trajectory
python traj_search.py trace_01_gpt-5/task.traj --stats

# Search for a pattern
python traj_search.py trace_01_gpt-5/task.traj --search "VAR_FLAGS"

# See what files were viewed
python traj_search.py trace_01_gpt-5/task.traj --files-viewed

# 🎯 NEW: Generate evidence for QA and annotation
python traj_search.py trace_01_gpt-5/task.traj --evidence
```

## Features

### 1. View Steps (`--step` / `--steps`)
View specific trajectory steps by number. Supports:
- Single step: `--step 5`
- Range: `--steps 5-10` (inclusive)
- Multiple: `--steps 5,10,15`
- Mixed: `--steps 5,10-15,20`

Display modes:
- **Formatted** (default): Clean, readable output with action, observation, thought
- **Raw** (`--raw`): Full JSON output

```bash
# View a single step
python traj_search.py trace.traj --step 5

# View a range of steps
python traj_search.py trace.traj --steps 5-10

# View multiple specific steps
python traj_search.py trace.traj --steps 5,10,15

# View as raw JSON
python traj_search.py trace.traj --step 5 --raw

# Mixed specification
python traj_search.py trace.traj --steps 0,5-8,15,20-25
```

### 2. Statistics (`--stats`)
Get an overview of the trajectory:
- Total steps
- Files viewed/edited counts
- Tests run count
- Action type summary

```bash
python traj_search.py trace.traj --stats
```

**Output:**
```
=== Trajectory Statistics ===
Total steps: 43
Files viewed: 8
Files edited: 2
Tests run: 0
Steps with thoughts: 2

=== Action Summary ===
  str_replace_editor: 22
  grep: 8
  python: 6
```

### 2. Pattern Search (`--search`)
Search for any regex pattern in the trajectory:

```bash
# Basic search (case-insensitive by default)
python traj_search.py trace.traj --search "VAR_FLAGS"

# Case-insensitive search (explicit, same as default)
python traj_search.py trace.traj --search "var_flags" -i

# Case-sensitive search
python traj_search.py trace.traj --search "VAR_FLAGS" --case-sensitive

# Search specific field only
python traj_search.py trace.traj --search "pytest" --field action

# Count occurrences
python traj_search.py trace.traj --search "nodes.py" --count

# Show context around matches
python traj_search.py trace.traj --search "VAR_FLAGS" --context 2

# Limit results
python traj_search.py trace.traj --search "error" --max-results 5
```

**Fields you can search:**
- `action` - Commands/actions taken by agent
- `observation` - Results/output from actions
- `thought` - Agent's reasoning
- `response` - Agent's responses

### 3. File Analysis

**Files Viewed** (`--files-viewed`)
```bash
python traj_search.py trace.traj --files-viewed
```
Output: List of all files the agent viewed/read

**Files Edited** (`--files-edited`)
```bash
python traj_search.py trace.traj --files-edited
```
Output: List of all files the agent modified

**Tests Run** (`--tests-run`)
```bash
python traj_search.py trace.traj --tests-run
```
Output: List of all test commands executed

### 4. Extract Thoughts (`--thoughts`)
Extract all agent reasoning/thoughts:

```bash
python traj_search.py trace.traj --thoughts

# Limit to first 10 thoughts
python traj_search.py trace.traj --thoughts --max-results 10
```

### 5. Evidence Generation (`--evidence`) ⭐ NEW
**QA Mode**: Generate copy-paste ready evidence for trajectory annotation and quality assurance.

```bash
# Generate all evidence types at once
python traj_search.py trace.traj --evidence

# Generate specific evidence type
python traj_search.py trace.traj --evidence files-modified
python traj_search.py trace.traj --evidence files-viewed
python traj_search.py trace.traj --evidence tests

# Generate search evidence with pattern
python traj_search.py trace.traj --evidence search --evidence-pattern "VAR_FLAGS"
```

**Evidence Types:**

**files-modified**: Shows which files were edited and at what steps
```
=== Files Modified ===
  /testbed/mypy/lookup.py
    Modified at steps: 15, 23, 31
    Total modifications: 3
```

**files-viewed**: Shows which files were viewed, including line numbers when available
```
=== Files Viewed ===
  /testbed/mypy/nodes.py
    Step 42: lines 796-800
    Step 58: (full file)
    Total views: 2
```

**tests**: Shows test execution timeline with pass/fail results
```
=== Test Execution ===
  Total test runs: 3

  Step 8: FAIL (0 passed, 5 failed)
    Command: pytest test-data/unit/check-incremental.test
  Step 15: FAIL (0 passed, 3 failed)
    Command: pytest test-data/unit/check-incremental.test
  Step 22: PASS (5 passed, 0 failed)
    Command: pytest test-data/unit/check-incremental.test
```

**search**: Shows pattern search evidence with step numbers
```
=== Search Pattern: 'VAR_FLAGS' ===
  Found 14 occurrences
  Steps: 5, 12, 18, 23, 29, 31, 35, 42, 47, 51, ... (4 more)

  Sample matches:
    Step 5 (action): grep -r "VAR_FLAGS" /testbed/mypy...
    Step 12 (observation): VAR_FLAGS = ['is_ready', 'is_inferred'...
    Step 42 (action): view /testbed/mypy/nodes.py 796-800...
```

**Use Cases:**
- Verify claims in annotation rationales (e.g., "searched 14 times", "viewed lines 796-800")
- Generate evidence snippets for FULL_4_TRACE_ANALYSIS.md
- Quality assurance for evaluation accuracy
- Quick fact-checking during annotation review

## Common Use Cases for Annotation

### Quick Evidence Generation (Recommended)
```bash
# Generate all evidence at once for annotation
python traj_search.py trace_01.traj --evidence

# Get evidence for a specific claim
python traj_search.py trace_01.traj --evidence search --evidence-pattern "VAR_FLAGS"
python traj_search.py trace_01.traj --evidence files-modified
```

### Did the agent see the critical file?
```bash
# Check if agent viewed nodes.py
python traj_search.py trace_01.traj --search "nodes\.py" --field action --count
```

### How many times did the agent search for VAR_FLAGS?
```bash
python traj_search.py trace_01.traj --search "VAR_FLAGS" --count

# Or get detailed evidence:
python traj_search.py trace_01.traj --evidence search --evidence-pattern "VAR_FLAGS"
```

### What files did the agent investigate?
```bash
python traj_search.py trace_01.traj --files-viewed | grep -E "nodes|lookup|fixup"

# Or get detailed evidence with step numbers:
python traj_search.py trace_01.traj --evidence files-viewed
```

### Did the agent understand the root cause?
```bash
# Search for serialization-related reasoning
python traj_search.py trace_01.traj --search "serializ" --field thought
```

### How many test runs?
```bash
python traj_search.py trace_01.traj --tests-run | wc -l
```

### Compare what different agents viewed
```bash
python traj_search.py trace_01.traj --files-viewed > trace_01_files.txt
python traj_search.py trace_02.traj --files-viewed > trace_02_files.txt
diff trace_01_files.txt trace_02_files.txt
```

## Advanced Examples

### Find when agent first viewed a file
```bash
python traj_search.py trace.traj --search "view.*nodes\.py" --field action
```

### Extract all grep commands
```bash
python traj_search.py trace.traj --search "^grep" --field action
```

### Find error messages
```bash
python traj_search.py trace.traj --search "error|fail|exception" -i
```

### Search for specific function names
```bash
python traj_search.py trace.traj --search "lookup_fully_qualified"
```

## Output Format

Search results show:
- **Step number** in the trajectory
- **Field** where match was found
- **Match context** (with pattern highlighted as `>>> match <<<`)
- **Context steps** (if --context specified)

## Tips

1. **Case-insensitive by default**: No need to worry about case when searching (like `grep -i`)
2. **Use regex** for flexible searching: `--search "VAR_FLAGS|var_flags"`
3. **Combine with grep** for filtering: `python traj_search.py trace.traj --files-viewed | grep test`
4. **Count first** before viewing full results: `--count` flag
5. **Search thoughts** to understand agent reasoning: `--field thought`
6. **Use --context** to see what happened around important events

## Common Errors

**Error: `unrecognized arguments: -i`** (if you're using an older version)
- The tool is case-insensitive by default, so `-i` is not needed
- Update to the latest version to use `-i` (though it's redundant)
- Use `--case-sensitive` if you want case-sensitive search

## Integration with Annotation Workflow

When creating `FULL_4_TRACE_ANALYSIS.md`, use this tool to:

1. **Verify what agents saw:**
   ```bash
   python traj_search.py trace_01.traj --search "VAR_FLAGS" --count
   python traj_search.py trace_02.traj --search "VAR_FLAGS" --count
   ```

2. **Understand their investigation:**
   ```bash
   python traj_search.py trace_01.traj --files-viewed
   ```

3. **Check if they ran tests:**
   ```bash
   python traj_search.py trace_01.traj --tests-run
   ```

4. **Extract key insights:**
   ```bash
   python traj_search.py trace_01.traj --thoughts | grep -i "serializ\|flag"
   ```

This helps you make evidence-based claims like:
- "trace_01 searched for VAR_FLAGS 14 times"
- "trace_03 viewed VAR_FLAGS at lines 796-800"
- "trace_02 never looked at VAR_FLAGS"
