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
# ⭐ NEW: Get comprehensive summary (RECOMMENDED - check this FIRST!)
python traj_search.py trace_01_gpt-5/task.traj --summary

# ⭐ NEW: Compare multiple traces side-by-side
python traj_search.py --compare trace_01.traj trace_02.traj trace_03.traj trace_04.traj

# ⭐ NEW: See what changed in the patch
python traj_search.py trace_01_gpt-5/task.traj --diff-summary

# Get statistics about a trajectory
python traj_search.py trace_01_gpt-5/task.traj --stats

# Search for a pattern
python traj_search.py trace_01_gpt-5/task.traj --search "VAR_FLAGS"

# See what files were viewed
python traj_search.py trace_01_gpt-5/task.traj --files-viewed

# Generate evidence for QA and annotation
python traj_search.py trace_01_gpt-5/task.traj --evidence
```

## Features

### 0. ⭐ NEW: Comprehensive Summary (`--summary`) **USE THIS FIRST!**

Get everything you need in one command: trajectory stats + report.json results + patch info + loop detection.

```bash
python traj_search.py trace_01.traj --summary
```

**Output Example (Passing Trace):**
```
=== Trace Summary ===
Status: ✅ RESOLVED (from report.json)
Tests: 3 FAIL_TO_PASS passed, 0 failed

=== Test Results ===
FAIL_TO_PASS passed:
  ✅ dask/dataframe/tests/test_dataframe.py::test_apply_convert_dtype[True]
  ✅ dask/dataframe/tests/test_dataframe.py::test_apply_convert_dtype[None]
  ✅ dask/dataframe/tests/test_dataframe.py::test_apply_convert_dtype[False]

PASS_TO_PASS: 602 passed, 0 failed

=== Trajectory Stats ===
Total Steps: 67
Files Viewed: 8
Files Edited: 8
Tests Run: 12

=== Patch Info ===
Agent Patch: ✅ EXISTS
Files Modified in Patch: 1
  dask/dataframe/core.py (+0, -3)

=== Loop Detection ===
✅ No loops detected
```

**Output Example (Failed Trace with Loop):**
```
=== Trace Summary ===
Status: ❌ NOT RESOLVED (from report.json)
Tests: 0 FAIL_TO_PASS passed, 3 failed

FAIL_TO_PASS failed:
  ❌ test1
  ❌ test2
  ❌ test3

=== Loop Detection ===
⚠️  LOOP DETECTED
Pattern: view /testbed/dask/dataframe/core.py 807-850
Repeated: 115 times (steps 35-149)
Status: Agent appears stuck in infinite loop
```

**Why use this first?**
- Immediately shows if agent succeeded or failed
- Catches loops automatically
- Shows actual test results from report.json
- One command instead of multiple checks

### 0b. ⭐ NEW: Patch Summary (`--diff-summary`)

Quick summary of what changed in the patch:

```bash
python traj_search.py trace_01.traj --diff-summary
```

**Output:**
```
=== Patch Summary ===
Files modified: 1

dask/dataframe/core.py:
  Lines changed: +0 additions, -3 deletions
  Change type: DELETION
```

### 0c. ⭐ NEW: Compare Traces (`--compare`)

Compare multiple traces side-by-side to see which passed/failed:

```bash
python traj_search.py --compare trace_01.traj trace_02.traj trace_03.traj trace_04.traj
```

**Output:**
```
=== Comparison: 4 Traces ===

Metric                    | trace_01 | trace_02 | trace_03 | trace_04
----------------------------------------------------------------------
Resolved                  | ✅       | ❌       | ✅       | ✅
Steps                     | 30       | 151      | 79       | 67
Files Modified (patch)    | 1        | 1        | 1        | 1
Tests Run                 | 1        | 0        | 10       | 12
FAIL_TO_PASS Passed       | 3        | 0        | 3        | 3
FAIL_TO_PASS Failed       | 0        | 3        | 0        | 0
Loops Detected            | No       | Yes (115)| No       | No
Patch Changes (+/-)       | +15/-3   | +11/-0   | +2/-1    | +0/-3
```

**Benefits:**
- Instant overview of all traces
- Immediately spot failures
- Compare efficiency (steps)
- Identify stuck agents (loops)

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
- "trace_02 never looked at VAR_FLAGS"

## ⚠️ CRITICAL: Always Verify Test Results

**IMPORTANT**: The trajectory file (.traj) does NOT contain the final test results. You MUST check `report.json` in the trace directory to verify if the agent succeeded.

### Why This Matters

1. **agent_patch.diff can exist but the agent may have FAILED**
2. **--stats shows test commands run, NOT whether they passed**
3. **An agent can run tests and still fail all of them**

### Mandatory Verification Steps

**ALWAYS do this for EVERY trace:**

```bash
# 1. Check report.json for resolved status
cat trace_01/report.json | grep '"resolved"'

# 2. Check FAIL_TO_PASS test results
cat trace_01/report.json | grep -A 10 '"FAIL_TO_PASS"'
```

**What to look for in report.json:**

```json
{
  "resolved": true,  // ✅ Agent succeeded
  "tests_status": {
    "FAIL_TO_PASS": {
      "success": ["test1", "test2"],  // ✅ These tests now pass
      "failure": []  // ✅ No failures
    }
  }
}
```

**FAILURE indicators:**

```json
{
  "resolved": false,  // ❌ Agent FAILED
  "tests_status": {
    "FAIL_TO_PASS": {
      "success": [],  // ❌ No tests passed
      "failure": ["test1", "test2"]  // ❌ Tests still failing
    }
  }
}
```

### Common Mistakes to Avoid

❌ **WRONG**: "trace_02 has agent_patch.diff, so it must have fixed something"
✅ **CORRECT**: Check report.json first - trace_02 shows `"resolved": false`

❌ **WRONG**: "--stats shows 0 tests run, so agent didn't try"
✅ **CORRECT**: Some agents run tests but don't show them in trajectory stats

❌ **WRONG**: "PASS_TO_PASS tests passed, so the agent succeeded"
✅ **CORRECT**: Check FAIL_TO_PASS tests - those are the ones that need to pass

### Detecting Stuck Agents

Watch for these red flags in trajectories:

```bash
# Check if agent is stuck viewing same file repeatedly
python traj_search.py trace.traj --search "view.*core\.py.*807-850" --field action --count

# If count is >50, agent is likely stuck in a loop
```

**Example of stuck behavior:**
- Steps 36-149: All viewing lines 807-850 of core.py
- 100+ identical view commands = infinite loop
- Agent never moved past analysis phase

## Annotation Workflow

Your job is to create FULL_4_TRACE_ANALYSIS.md and evaluation.txt files for task folders.

### Step-by-Step Process

1. **⭐ FIRST: Use --compare to get instant overview**
   ```bash
   python traj_search.py --compare trace_01/*.traj trace_02/*.traj trace_03/*.traj trace_04/*.traj
   ```
   This immediately shows which passed/failed, with loops and test counts!

2. **For each trace: Run --summary**
   ```bash
   python traj_search.py trace_01/*.traj --summary
   python traj_search.py trace_02/*.traj --summary
   python traj_search.py trace_03/*.traj --summary
   python traj_search.py trace_04/*.traj --summary
   ```
   Each summary shows:
   - ✅/❌ Resolved status
   - Which tests passed/failed
   - Loop detection
   - Patch changes

3. **Alternative: Manual check of report.json files (old way)**
   ```bash
   for trace in trace_*; do
     echo "=== $trace ==="
     cat $trace/report.json | grep '"resolved"'
   done
   ```

4. **For PASSING traces: Analyze their approach**
   ```bash
   python traj_search.py trace_01.traj --evidence
   python traj_search.py trace_01.traj --diff-summary
   python traj_search.py trace_01.traj --files-viewed
   ```

5. **For FAILING traces: Already have the info!**
   The --summary command already told you:
   - Whether there's a loop
   - Which tests failed
   - What the patch changed

   Additional investigation if needed:
   ```bash
   # Check what they tried
   python traj_search.py trace_02.traj --files-edited

   # Check their reasoning
   python traj_search.py trace_02.traj --thoughts --max-results 5
   ```

6. **Compare all patches quickly**
   ```bash
   python traj_search.py trace_01/*.traj --diff-summary
   python traj_search.py trace_02/*.traj --diff-summary
   python traj_search.py trace_03/*.traj --diff-summary
   python traj_search.py trace_04/*.traj --diff-summary
   ```
   Then compare with golden_patch.diff

7. **Write FULL_4_TRACE_ANALYSIS.md**
   - Use info from --compare and --summary
   - Include pass/fail status for each trace
   - Explain what each trace did (even failed ones)
   - Compare approaches
   - Rank traces

8. **Write evaluation.txt**
   - See GOOD_EXAMPLES for format
   - Include rubrics that test must-have vs nice-to-have
   - Rate each trace with clear rationale
   - Failed traces should get rating 1

### Cross-Verification Checklist

Before finalizing analysis:

- [ ] **Run --compare on all traces** (instant overview)
- [ ] **Run --summary on each trace** (get complete info)
- [ ] Verified resolved status matches test results (from --summary)
- [ ] Checked which FAIL_TO_PASS tests passed/failed (from --summary)
- [ ] Read agent_patch.diff for all traces (or use --diff-summary)
- [ ] Compared patches to golden_patch.diff
- [ ] Detected any infinite loops (automatic in --summary)
- [ ] Verified file modification claims with --files-edited
- [ ] Counted test runs with --tests-run
- [ ] Cross-referenced trajectory evidence with report.json (done by --summary)

---

## ✅ IMPLEMENTED: New Features

The following features have been implemented and are ready to use:

### ✅ 1. `--summary` Command - **USE THIS FIRST!**

Combines trajectory + report.json + patch analysis + loop detection in ONE command.

**Status**: ✅ IMPLEMENTED AND TESTED

See examples in section 0 above.

### ✅ 2. `--diff-summary` Command

Quick summary of patch changes without reading full diff.

**Status**: ✅ IMPLEMENTED AND TESTED

See examples in section 0b above.

### ✅ 3. `--compare` Command

Compare multiple traces side-by-side with instant overview.

**Status**: ✅ IMPLEMENTED AND TESTED

See examples in section 0c above.

---

## 🔧 Remaining Proposed Improvements

These would be nice to have but aren't critical now:

### 2. Enhanced `--stats --with-results`

Enhance existing --stats to show test results inline.

**Why not needed now:** `--summary` already does this better.

### 4. `--verify` Command

Cross-check trajectory vs report.json for mismatches.

**Why not needed now:** `--summary` automatically shows discrepancies.

---

## Results & Benefits

These new features **solve the exact problems from this session**:

✅ **`--summary` immediately shows** `"resolved": false` for trace_02
✅ **Automatic loop detection** flagged trace_02's 115-step loop
✅ **`--compare` makes** pass/fail comparison obvious upfront
✅ **`--diff-summary` shows** what changed without reading full patches

**Verified on real data (dask__dask-10212):**
- trace_01: ✅ 30 steps, resolved
- trace_02: ❌ 151 steps, loop detected, NOT resolved
- trace_03: ✅ 79 steps, resolved
- trace_04: ✅ 67 steps, resolved

**Result:** Analysis that would take 20+ minutes of manual checking now takes 30 seconds with 2 commands.
- the trace names must be "trace_01" etc.
- you can use the @agent-evaluation-rubric-generator and @agent-rubric-grader for help.
- dont mention line numbers.
- in Must-read files and Must-check tests only add the files changed in the gold pr