# Creating evaluation.txt Files: Guide

## 1. Overview

The `evaluation.txt` file is a structured evaluation framework for coding agent trajectory annotation containing:
- **Metadata**: Language, category, difficulty, critical files
- **Rubrics**: 8-10 task-specific criteria with PASS/FAIL grades
- **Overall ratings**: 1-5 quality scores with rationales

**Purpose**: Create reproducible, evidence-based evaluations for coding agent solutions.

---

## 2. Quick Start

### Essential Steps
1. Read problem statement and golden patch
2. Fill metadata (language, category, difficulty, must-read files, must-check tests)
3. Review 4 trajectories (code diffs, test results)
4. Create 8-10 rubrics (at least one per type: correctness, agent behavior, code style, summary)
5. Grade trajectories: PASS/FAIL for each rubric
6. Assign overall ratings: 1-5 with 50-75 word rationales

### Required Inputs
- Problem statement, golden patch, 3-4 agent trajectories, test results

---

## 3. Metadata

### Format
```
Language *
Python

Category *
Bug fixing

Difficulty *
15 min ~ 1 hour

Must-read files *
["/testbed/path/to/file.py"]

Must-check tests *
["/testbed/tests/test_file.py"]
```

### Fields
- **Language**: Python, Rust, JavaScript, TypeScript, Java, C++, C
- **Category**: bug fixing, feature development, system optimization, documentation, refactoring
- **Difficulty**: `0 ~ 15 min`, `15 min ~ 1 hour`, `1 hour ~ 4 hours`
- **Must-read files**: Non-test files from golden patch (absolute paths with /testbed/)
- **Must-check tests**: Test files from golden patch (absolute paths with /testbed/)

---

## 4. Creating Rubrics

### Requirements
- **8-10 rubrics total**
- **At least one of each type**: correctness, agent behavior, code style, summary
- **50-70% MUST_FOLLOW**, 30-50% GOOD_TO_HAVE
- **Criterion**: 8-15 words, specific and testable
- **Rationale**: 8-15 words explaining importance

### Rubric Structure
```json
"rubric_01": {
  "type": "correctness",
  "criterion": "The patch includes blocksize in tokenize call for unique names.",
  "rationale": "Different blocksizes need different task keys to avoid collisions.",
  "importance": "MUST_FOLLOW",
  "is_positive": "true"
}
```

### Types

**Correctness (5-7 rubrics)**: Final code correctness
- Core functionality implemented correctly
- Target test passes (FAIL_TO_PASS)
- No regressions (PASS_TO_PASS)
- Correct parameters/values used

**Agent Behavior (1-2 rubrics)**: Problem-solving approach
- Reads critical files before implementing
- Doesn't over-engineer or modify unrelated files

**Code Style (1-2 rubrics)**: Code quality
- Follows project conventions
- Proper naming and organization

**Summary (1 rubric)**: Explanation quality
- Correctly identifies root cause

### Importance Levels

**MUST_FOLLOW** (50-70%): Critical for correctness
- 0 failures → Rating 4-5
- 1-2 failures → Rating 3
- 3-4 failures → Rating 2
- 5+ failures → Rating 1

**GOOD_TO_HAVE** (30-50%): Quality improvements
- Only affects distinction between ratings 4 and 5

### is_positive Field
- **"true"**: Agent SHOULD do this (PASS = did it)
- **"false"**: Agent SHOULD NOT do this (PASS = avoided it)

### Best Practices

✅ **DO**:
- Use exact function names, parameters, file paths
- Make criteria independently verifiable
- Focus on one aspect per rubric

❌ **DON'T**:
- Write vague criteria ("fixes bug correctly")
- Write tool-specific criteria ("uses grep")
- Combine multiple requirements in one rubric

---

## 5. Grading Trajectories

### Methodology
1. Gather evidence: code diffs, test results, agent actions
2. Apply criterion objectively
3. Assign PASS or FAIL (no partial credit)

### Evidence Sources
- **Code Diffs**: Function signatures, implementation, imports
- **Test Results**: FAIL_TO_PASS, PASS_TO_PASS, PASS_TO_FAIL
- **Agent Actions**: Files read, commands run, files created

### Format
```json
"rubrics_rating": {
  "trace_01": {
    "rubric_01": "PASS",
    "rubric_02": "FAIL",
    ...
  },
  "trace_03": { ... },
  "trace_04": { ... }
}
```

---

## 6. Overall Rating System

### Rating Scale
| Rating | Meaning | MUST_FOLLOW Failures |
|--------|---------|---------------------|
| 5 | Perfect fix | 0 |
| 4 | Good fix, minor issues | 0 (some GOOD_TO_HAVE fail) |
| 3 | Partial fix | 1-2 |
| 2 | Low quality | 3-4 |
| 1 | Wrong/harmful | 5+ |

### Rationale Requirements
- **50-75 words** per trajectory
- Describe what went wrong without referencing rubric numbers
- Mention specific issues (wrong file, wrong logic, test failures)
- State count of MUST_FOLLOW failures at the end

### Format
```json
"overall_rating": {
  "trace_01": {
    "rating": 2,
    "rationale": "Low quality fix that tokenizes block_lists instead of blocksize, causing deterministic naming tests to fail. The agent did not add blocksize parameter or pass it from read_pandas, missing the architectural fix. Wrong value tokenized led to 2 test regressions. Failed 5 MUST_FOLLOW rubrics."
  },
  "trace_03": {
    "rating": 3,
    "rationale": "Partial fix with correct core logic - adds blocksize parameter matching golden patch. However, despite correct csv.py changes, 2 deterministic name tests still failed as regressions. The agent correctly identified root cause but implementation was incomplete. Failed 1 MUST_FOLLOW rubric."
  },
  "trace_04": {
    "rating": 5,
    "rationale": "Perfect implementation matching golden patch. Agent correctly identified task name collision, added blocksize parameter to text_blocks_to_pandas, passed it from read_pandas, and included in tokenize. All tests pass with no regressions. Solution complete and correct. Zero MUST_FOLLOW failures."
  }
}
```

---

## 7. Quality Checklist

### Metadata
- [ ] Language, category, difficulty specified
- [ ] Must-read files = non-test files from golden patch
- [ ] Must-check tests = test files from golden patch
- [ ] All paths absolute with /testbed/

### Rubrics
- [ ] 8-10 rubrics total
- [ ] At least one of each type (correctness, agent behavior, code style, summary)
- [ ] 50-70% MUST_FOLLOW
- [ ] Criteria: 8-15 words, specific
- [ ] Rationales: 8-15 words

### Grading
- [ ] All 4 trajectories graded
- [ ] All rubrics graded for each trajectory
- [ ] PASS or FAIL only

### Overall Rating
- [ ] Rating 1-5 for each trajectory
- [ ] Rationale 50-75 words
- [ ] Describes specific issues without rubric numbers
- [ ] States MUST_FOLLOW failure count

---

## 8. Important Guidelines

### Don't Penalize for Irrelevant Changes
- If an agent modifies test files but all tests pass, don't penalize
- Focus on whether the solution **works correctly**, not whether it matches golden patch exactly
- Extra files/modifications that don't break functionality are acceptable

### Verify Rubric Grades with Evidence
- Always check agent_patch.diff and report.json before grading
- Use traj_search.py to verify agent's understanding (search thoughts/summaries)
- A rubric like "agent identifies root cause" requires checking the trajectory, not just the patch

### Evaluate All 4 Trajectories
- Create evaluation.txt for ALL 4 trajectories
- User will decide which one to exclude after review
- Keep the original trace names (trace_01, trace_02, trace_03, trace_04)

### Rating Should Match Test Results
- If resolved=true in report.json and all tests pass → likely rating 4-5
- If PASS_TO_PASS has failures → check if those are regression rubrics
- Target test passing but regressions = rating 3

---

## 9. Example Rubrics by Type (Reference)

### Correctness
```json
{
  "type": "correctness",
  "criterion": "The patch includes blocksize in tokenize for unique task names.",
  "rationale": "Blocksize determines chunking; different values need different keys.",
  "importance": "MUST_FOLLOW",
  "is_positive": "true"
}
```

```json
{
  "type": "correctness",
  "criterion": "Target test passes after the fix is applied.",
  "rationale": "Validates the bug is actually fixed.",
  "importance": "MUST_FOLLOW",
  "is_positive": "true"
}
```

```json
{
  "type": "correctness",
  "criterion": "No regression tests fail after applying the patch.",
  "rationale": "Ensures existing functionality remains intact.",
  "importance": "MUST_FOLLOW",
  "is_positive": "true"
}
```

### Agent Behavior
```json
{
  "type": "agent behavior",
  "criterion": "Agent reads critical source files before making edits.",
  "rationale": "Understanding existing code prevents incorrect modifications.",
  "importance": "GOOD_TO_HAVE",
  "is_positive": "true"
}
```

```json
{
  "type": "agent behavior",
  "criterion": "Agent does not tokenize blocks or block_lists directly.",
  "rationale": "Tokenizing blocks breaks deterministic naming for same blocksize.",
  "importance": "MUST_FOLLOW",
  "is_positive": "false"
}
```

### Code Style
```json
{
  "type": "code style",
  "criterion": "The fix follows existing code patterns for parameter passing.",
  "rationale": "Consistent style improves maintainability.",
  "importance": "GOOD_TO_HAVE",
  "is_positive": "true"
}
```

### Summary
```json
{
  "type": "summary",
  "criterion": "Agent correctly identifies task name collision as root cause.",
  "rationale": "Understanding root cause demonstrates proper debugging.",
  "importance": "GOOD_TO_HAVE",
  "is_positive": "true"
}
```

---

## 10. Tools

Use `traj_search.py` to analyze trajectories:

```bash
# Get statistics
python traj_search.py trace.traj --stats

# Search for patterns
python traj_search.py trace.traj --search "tokenize"

# View specific steps
python traj_search.py trace.traj --step 5-10

# Get agent thoughts
python traj_search.py trace.traj --thoughts

# Generate evidence
python traj_search.py trace.traj --evidence
```

---

## 11. Complete Example

### Task: dask__dask-6818
Bug: read_csv with different blocksize values incorrectly reuses cached results due to task name collisions.

### Metadata
```
Language *
Python

Category *
Bug fixing

Difficulty *
15 min ~ 1 hour

Must-read files *
["/testbed/dask/dataframe/io/csv.py"]

Must-check tests *
["/testbed/dask/dataframe/io/tests/test_csv.py"]
```

### Rubrics (9 total)
```json
{
  "rubric_01": {
    "type": "correctness",
    "criterion": "The agent includes blocksize in tokenize call for unique task names.",
    "rationale": "Blocksize determines chunking; different values need different keys.",
    "importance": "MUST_FOLLOW",
    "is_positive": "true"
  },
  "rubric_02": {
    "type": "correctness",
    "criterion": "The agent adds blocksize parameter to text_blocks_to_pandas signature.",
    "rationale": "Parameter must exist to be passed through for tokenization.",
    "importance": "MUST_FOLLOW",
    "is_positive": "true"
  },
  "rubric_03": {
    "type": "correctness",
    "criterion": "The agent passes blocksize from read_pandas to text_blocks_to_pandas.",
    "rationale": "Blocksize value must flow from caller to tokenize location.",
    "importance": "MUST_FOLLOW",
    "is_positive": "true"
  },
  "rubric_04": {
    "type": "correctness",
    "criterion": "Target test test_read_csv_has_different_names_based_on_blocksize passes.",
    "rationale": "Validates the core fix for task name collisions.",
    "importance": "MUST_FOLLOW",
    "is_positive": "true"
  },
  "rubric_05": {
    "type": "correctness",
    "criterion": "Deterministic name tests pass without regressions.",
    "rationale": "Same inputs must produce same task names for caching.",
    "importance": "MUST_FOLLOW",
    "is_positive": "true"
  },
  "rubric_06": {
    "type": "correctness",
    "criterion": "Agent does not tokenize blocks or block_lists directly.",
    "rationale": "Tokenizing blocks breaks deterministic naming.",
    "importance": "MUST_FOLLOW",
    "is_positive": "false"
  },
  "rubric_07": {
    "type": "agent behavior",
    "criterion": "Agent reads csv.py to understand tokenization before changes.",
    "rationale": "Understanding existing code is essential for correct fixes.",
    "importance": "GOOD_TO_HAVE",
    "is_positive": "true"
  },
  "rubric_08": {
    "type": "code style",
    "criterion": "Fix follows existing code patterns in csv.py.",
    "rationale": "Consistent style improves maintainability.",
    "importance": "GOOD_TO_HAVE",
    "is_positive": "true"
  },
  "rubric_09": {
    "type": "summary",
    "criterion": "Agent correctly identifies task name collision as root cause.",
    "rationale": "Understanding root cause demonstrates proper debugging.",
    "importance": "GOOD_TO_HAVE",
    "is_positive": "true"
  }
}
```

### Rubrics Rating
```json
{
  "trace_01": {
    "rubric_01": "FAIL",
    "rubric_02": "FAIL",
    "rubric_03": "FAIL",
    "rubric_04": "PASS",
    "rubric_05": "FAIL",
    "rubric_06": "FAIL",
    "rubric_07": "PASS",
    "rubric_08": "FAIL",
    "rubric_09": "PASS"
  },
  "trace_02": {
    "rubric_01": "FAIL",
    "rubric_02": "FAIL",
    "rubric_03": "FAIL",
    "rubric_04": "PASS",
    "rubric_05": "FAIL",
    "rubric_06": "FAIL",
    "rubric_07": "PASS",
    "rubric_08": "FAIL",
    "rubric_09": "PASS"
  },
  "trace_03": {
    "rubric_01": "PASS",
    "rubric_02": "PASS",
    "rubric_03": "PASS",
    "rubric_04": "PASS",
    "rubric_05": "FAIL",
    "rubric_06": "PASS",
    "rubric_07": "PASS",
    "rubric_08": "PASS",
    "rubric_09": "PASS"
  },
  "trace_04": {
    "rubric_01": "PASS",
    "rubric_02": "PASS",
    "rubric_03": "PASS",
    "rubric_04": "PASS",
    "rubric_05": "PASS",
    "rubric_06": "PASS",
    "rubric_07": "PASS",
    "rubric_08": "PASS",
    "rubric_09": "PASS"
  }
}
```

### Overall Rating
```json
{
  "trace_01": {
    "rating": 2,
    "rationale": "Low quality fix that tokenizes block_lists instead of blocksize, causing the target test to pass but breaking deterministic naming tests. The agent did not add blocksize parameter to function signature or pass it from read_pandas, missing the core architectural fix. The wrong value was tokenized leading to 2 test regressions. Failed 5 MUST_FOLLOW rubrics."
  },
  "trace_02": {
    "rating": 2,
    "rationale": "Low quality fix that tokenizes blocks instead of blocksize, identical architectural issues to trace_01. The agent correctly identified the tokenize call as the fix location but chose to tokenize blocks rather than adding proper blocksize parameter flow. This causes test regressions because blocks vary even when blocksize is the same, breaking deterministic task naming. Failed 5 MUST_FOLLOW rubrics."
  },
  "trace_03": {
    "rating": 3,
    "rationale": "Partial fix with correct core logic - adds blocksize parameter and includes it in tokenize call matching golden patch approach. The agent correctly identified the root cause and implemented the proper solution in csv.py. However, despite correct changes, 2 deterministic name tests still failed as regressions. Failed 1 MUST_FOLLOW rubric."
  },
  "trace_04": {
    "rating": 5,
    "rationale": "Perfect implementation matching golden patch approach. The agent correctly identified the task name collision root cause, added blocksize parameter to text_blocks_to_pandas signature, passed it from read_pandas, and included it in tokenize. All tests pass including deterministic naming tests with no regressions. Zero MUST_FOLLOW failures."
  }
}
```
you can use the traj_search.py script for help.