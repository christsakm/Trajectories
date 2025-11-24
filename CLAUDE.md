# CLAUDE.md

This file provides guidance to Claude Code when working with trajectory annotation in this repository.

## Repository Purpose

This repository contains trajectory data for coding agent evaluation. Each task folder includes:
- Agent trajectories showing different approaches to solving coding problems
- Golden patches (reference solutions)
- Test data and instance metadata
- Your deliverable: evaluation analysis file

The primary workflow is **annotating agent trajectories** using evidence-based rubrics to evaluate coding agent performance.

---

## 🎯 Core Principles

### 1. Evidence-Based Rubrics (CRITICAL)

**All rubrics must be verifiable through concrete evidence:**

- **Code change rubrics** → Verify in `agent_patch.diff` compared to `golden_patch.diff`
- **Agent behavior rubrics** → Verify using `traj_search.py` (files viewed, actions taken)
- **Summary rubrics** → Verify using `traj_search.py --thoughts`

**❌ NEVER create rubrics about test results:**
- ❌ "The target test passes"
- ❌ "No regression tests fail"
- ❌ "All FAIL_TO_PASS tests pass"

**Why?** Test results are in `report.json`, not in the code diff. Rubrics check WHAT'S IN THE CODE, not whether it works.

**✅ Instead, use test results in rating rationales:**
- "Despite correct code changes, 2 tests still failed showing incomplete fix. Failed 1 MUST_FOLLOW rubric."

### 2. Use traj_search.py Extensively

The `traj_search.py` tool is **CRITICAL** for evidence-based evaluation. Use it at every step.

### 3. Single Deliverable Per Task

Create **ONE markdown file** per task folder containing:
- Complete analysis of all 4 traces
- Evidence from traj_search.py
- evaluation.txt JSON sections embedded in markdown

### 4. Evaluate ALL 4 Traces

Always analyze all 4 trajectories. Don't exclude any upfront.

---

## 📂 Repository Structure

```
Trajectories/
├── {task-name}/
│   ├── instance_data.json          # Task metadata and problem statement
│   ├── golden_patch.diff           # Reference solution (what code SHOULD look like)
│   ├── test_patch.diff             # Test changes
│   ├── trace_01_{model}/
│   │   ├── {task-name}.traj        # Full action log (JSON)
│   │   ├── agent_patch.diff        # Agent's code solution
│   │   ├── report.json             # Test results (resolved: true/false)
│   │   └── test_output.txt         # Test execution output
│   ├── trace_02_{model}/
│   ├── trace_03_{model}/
│   ├── trace_04_{model}/
│   └── evaluation_analysis.md      # YOUR DELIVERABLE (with embedded JSON)
```

---

## 🔄 Complete Workflow

### Step 1: Quick Overview with traj_search.py

**Start here - this takes 30 seconds and shows you everything:**

```bash
# Compare all 4 traces instantly
python traj_search.py --compare trace_01/*.traj trace_02/*.traj trace_03/*.traj trace_04/*.traj
```

**Output shows:**
- ✅/❌ Which traces passed/failed
- Loop detection
- Step counts
- Test results
- Patch changes

**Then get detailed info for each trace:**

```bash
# Run summary for each trace
python traj_search.py trace_01/*.traj --summary
python traj_search.py trace_02/*.traj --summary
python traj_search.py trace_03/*.traj --summary
python traj_search.py trace_04/*.traj --summary
```

**Each summary shows:**
- Resolved status (from report.json)
- FAIL_TO_PASS test results
- PASS_TO_PASS test results
- Loop detection
- Patch file changes
- Trajectory stats

### Step 2: Read Task Data

```bash
# Understand the problem
cat instance_data.json

# See what the correct solution looks like
cat golden_patch.diff

# See what test changes were made
cat test_patch.diff
```

### Step 3: Analyze Agent Patches

**Compare each agent's code changes to the golden patch:**

```bash
# Quick summaries
python traj_search.py trace_01/*.traj --diff-summary
python traj_search.py trace_02/*.traj --diff-summary
python traj_search.py trace_03/*.traj --diff-summary
python traj_search.py trace_04/*.traj --diff-summary

# Read actual patches
cat trace_01/agent_patch.diff
cat trace_02/agent_patch.diff
cat trace_03/agent_patch.diff
cat trace_04/agent_patch.diff
```

**For each trace, note:**
- What files were modified?
- What functions/code was changed?
- How does it compare to golden_patch.diff?
- What's missing or wrong?

### Step 4: Gather Evidence for Rubrics

**Use traj_search.py to collect evidence:**

```bash
# Get all evidence at once
python traj_search.py trace_01/*.traj --evidence
python traj_search.py trace_02/*.traj --evidence
python traj_search.py trace_03/*.traj --evidence
python traj_search.py trace_04/*.traj --evidence

# Check what files agents viewed/edited
python traj_search.py trace_01/*.traj --files-viewed
python traj_search.py trace_01/*.traj --files-edited

# Check agent reasoning
python traj_search.py trace_01/*.traj --thoughts
```

### Step 5: Create 8-10 Evidence-Based Rubrics

**Rubric Requirements:**
- Total: 8-10 rubrics always
- At least one of each type: correctness, code style, summary, agent behavior
- 50-70% should be MUST_FOLLOW importance
- Each rubric must be verifiable through evidence

**Rubric Types & Evidence Sources:**

#### Correctness Rubrics (5-7 total) - Check CODE in diff

**✅ Good Examples:**
```json
{
  "criterion": "The patch adds blocksize parameter to text_blocks_to_pandas signature.",
  "rationale": "Parameter must exist to be passed through for tokenization.",
  "type": "correctness",
  "importance": "MUST_FOLLOW",
  "is_positive": "true"
}
```

```json
{
  "criterion": "The patch includes blocksize in tokenize call for unique names.",
  "rationale": "Different blocksizes need different task keys to avoid collisions.",
  "type": "correctness",
  "importance": "MUST_FOLLOW",
  "is_positive": "true"
}
```

```json
{
  "criterion": "The patch modifies write_records in responses.py to return RecordsIngested.",
  "rationale": "Response must be in responses.py where API responses are generated.",
  "type": "correctness",
  "importance": "MUST_FOLLOW",
  "is_positive": "true"
}
```

**❌ Bad Examples (Not in Code Diff):**
```json
{
  "criterion": "The target test passes after the fix",
  // ❌ Test results are in report.json, not the diff
}
```

```json
{
  "criterion": "No regression tests fail",
  // ❌ Test results are not code changes
}
```

**How to Verify:** Compare agent_patch.diff to golden_patch.diff line by line

#### Agent Behavior Rubrics (1-2 total) - Check ACTIONS in trajectory

**✅ Good Examples:**
```json
{
  "criterion": "Agent reads csv.py to understand tokenization before making changes.",
  "rationale": "Understanding existing code prevents incorrect modifications.",
  "type": "agent behavior",
  "importance": "GOOD_TO_HAVE",
  "is_positive": "true"
}
```

```json
{
  "criterion": "Agent does not modify files outside the timestreamwrite directory.",
  "rationale": "Keeps changes focused on affected module, minimizing risk.",
  "type": "agent behavior",
  "importance": "GOOD_TO_HAVE",
  "is_positive": "false"
}
```

**How to Verify:** Use `traj_search.py --evidence files-viewed` and `--evidence files-modified`

#### Code Style Rubrics (1-2 total) - Check CODE in diff

**✅ Good Examples:**
```json
{
  "criterion": "The sorting function is defined at module level not instance.",
  "rationale": "Module-level functions are more reusable and maintainable.",
  "type": "code style",
  "importance": "GOOD_TO_HAVE",
  "is_positive": "true"
}
```

**How to Verify:** Check code structure in agent_patch.diff

#### Summary Rubrics (1 total) - Check EXPLANATION in trajectory

**✅ Good Example:**
```json
{
  "criterion": "Agent correctly identifies task name collision as root cause.",
  "rationale": "Understanding root cause demonstrates proper debugging analysis.",
  "type": "summary",
  "importance": "GOOD_TO_HAVE",
  "is_positive": "true"
}
```

**How to Verify:** Use `traj_search.py --thoughts` to read agent reasoning

### Step 6: Grade All 4 Traces

**For each trace, for each rubric, assign PASS or FAIL:**

**Grading Logic:**
- **Positive rubrics (is_positive: "true")**: PASS if agent did it, FAIL if didn't
- **Negative rubrics (is_positive: "false")**: PASS if agent avoided it, FAIL if did it

**Evidence Sources:**
- Code rubrics: Check agent_patch.diff
- Behavior rubrics: Check traj_search.py evidence
- Summary rubrics: Check traj_search.py --thoughts

**Use report.json for ratings (not rubrics):**
- Check resolved status: `cat trace_01/report.json | grep '"resolved"'`
- This tells you if tests passed, which informs the rating

### Step 7: Assign Overall Ratings (1-5)

**Rating Scale:**

| Rating | Meaning | MUST_FOLLOW Failures | Test Results |
|--------|---------|---------------------|--------------|
| 5 | Perfect | 0 | resolved: true |
| 4 | Good, minor issues | 0 | resolved: true |
| 3 | Partial fix | 1-2 | may be true/false |
| 2 | Low quality | 3-4 | usually false |
| 1 | Wrong/harmful | 5+ | resolved: false |

**Rationale Requirements (50-75 words):**
- Describe specific code issues (wrong file, wrong logic, missing parameters)
- Mention test results from report.json
- NO references to rubric numbers
- State MUST_FOLLOW failure count at end

**✅ Good Example:**
```
"Low quality fix that tokenizes block_lists instead of blocksize parameter, causing deterministic naming tests to fail. The agent did not add blocksize parameter to function signature or pass it from read_pandas, missing the core architectural fix. Tests show resolved: false with 2 FAIL_TO_PASS failures. Failed 5 MUST_FOLLOW rubrics."
```

**❌ Bad Example:**
```
"Failed rubric_01, rubric_03, and rubric_05. Some tests passed but others failed."
// ❌ Too vague, references rubric numbers, doesn't explain what went wrong
```

### Step 8: Create Single Deliverable File

Create one markdown file (e.g., `evaluation_analysis.md`) containing:

1. **Task Overview Section**
2. **Analysis of All 4 Traces** (approach, evidence, findings)
3. **Complete evaluation.txt JSON** (embedded in markdown code blocks)

---

## 📋 Metadata Requirements

Extract from golden_patch.diff:

### Language
Options: Python, Rust, JavaScript, TypeScript, Java, C++, C

### Category
Options: bug fixing, feature development, system optimization, documentation, refactoring

### Difficulty
- `0 ~ 15 min`: Simple one-line fixes
- `15 min ~ 1 hour`: Straightforward fixes requiring 1-2 files
- `1 hour ~ 4 hours`: Complex multi-file changes

### Must-read Files
- Extract non-test files from golden_patch.diff
- Use absolute paths: `/testbed/path/to/file.py`
- Keep minimal (1-3 files)

### Must-check Tests
- Extract test files from golden_patch.diff
- Use absolute paths: `/testbed/tests/test_file.py`

---

## 🛠️ Trajectory Search Tool (traj_search.py)

### Essential Commands

#### 1. --compare (USE THIS FIRST)
```bash
python traj_search.py --compare trace_01/*.traj trace_02/*.traj trace_03/*.traj trace_04/*.traj
```
**Shows:** Instant side-by-side comparison of all traces

#### 2. --summary (USE FOR EACH TRACE)
```bash
python traj_search.py trace_01/*.traj --summary
```
**Shows:**
- ✅/❌ Resolved status (from report.json)
- FAIL_TO_PASS test results (passed/failed)
- PASS_TO_PASS test results
- Loop detection (if agent got stuck)
- Patch changes summary
- Trajectory stats (steps, files viewed/edited, tests run)

#### 3. --diff-summary (QUICK PATCH VIEW)
```bash
python traj_search.py trace_01/*.traj --diff-summary
```
**Shows:** What files changed and how (+/- line counts)

#### 4. --evidence (COMPREHENSIVE EVIDENCE)
```bash
python traj_search.py trace_01/*.traj --evidence
```
**Shows:**
- Files modified (at which steps)
- Files viewed (with line numbers)
- Tests run (with pass/fail)
- Search patterns used

#### 5. --files-viewed / --files-edited
```bash
python traj_search.py trace_01/*.traj --files-viewed
python traj_search.py trace_01/*.traj --files-edited
```

#### 6. --thoughts (AGENT REASONING)
```bash
python traj_search.py trace_01/*.traj --thoughts
```
**Shows:** Agent's internal reasoning (for summary rubrics)

#### 7. --search (PATTERN SEARCH)
```bash
python traj_search.py trace_01/*.traj --search "blocksize" --count
```

### Integration into Workflow

**At Step 1 (Overview):**
```bash
python traj_search.py --compare trace_01/*.traj trace_02/*.traj trace_03/*.traj trace_04/*.traj
```

**At Step 3 (Analyze Patches):**
```bash
python traj_search.py trace_01/*.traj --diff-summary
```

**At Step 4 (Gather Evidence):**
```bash
python traj_search.py trace_01/*.traj --evidence
python traj_search.py trace_01/*.traj --summary
```

**At Step 6 (Verify Rubrics):**
```bash
# Verify code change rubric
python traj_search.py trace_01/*.traj --search "blocksize" --field action

# Verify behavior rubric
python traj_search.py trace_01/*.traj --files-viewed | grep csv.py

# Verify summary rubric
python traj_search.py trace_01/*.traj --thoughts | grep -i "collision"
```

---

## 📝 Rubric Structure (All 5 Fields Required)

```json
{
  "criterion": "8-15 words describing specific, verifiable requirement",
  "rationale": "8-15 words explaining why this matters",
  "type": "correctness|code style|summary|agent behavior",
  "importance": "MUST_FOLLOW|GOOD_TO_HAVE",
  "is_positive": "true|false"
}
```

### Field Guidelines

**criterion** (8-15 words):
- Use exact function names, file paths, parameters
- Must be verifiable through evidence
- ✅ "The patch adds blocksize parameter to text_blocks_to_pandas signature"
- ❌ "The agent fixes the bug correctly"

**rationale** (8-15 words):
- Brief explanation of impact
- ✅ "Parameter must exist to be passed through for tokenization"
- ❌ "This is important because it's required for the fix"

**type**:
- `correctness`: Code works correctly (verify in diff)
- `code style`: Code quality (verify in diff)
- `summary`: Agent explanation (verify with --thoughts)
- `agent behavior`: Agent process (verify with --evidence)

**importance**:
- `MUST_FOLLOW`: Critical for correctness (50-70% of rubrics)
- `GOOD_TO_HAVE`: Quality improvement (30-50% of rubrics)

**is_positive**:
- `"true"`: Agent SHOULD do this (PASS = did it, FAIL = didn't)
- `"false"`: Agent SHOULD NOT do this (PASS = avoided, FAIL = did it)

---

## 🎓 Key Lessons from Good Examples

### 1. Rationales ARE Detailed (50-75 words for overall ratings)

**✅ Good Example:**
> "Low quality fix that tokenizes block_lists instead of blocksize, causing deterministic naming tests to fail. The agent did not add blocksize parameter to function signature or pass it from read_pandas, missing the architectural fix. Wrong value tokenized led to 2 test regressions. Failed 5 MUST_FOLLOW rubrics."

**Include:**
- Specific numbers: "35 steps", "14 tests broken", "2 file edits"
- What failed with context: "tokenizes block_lists instead of blocksize"
- Test results: "resolved: false", "2 FAIL_TO_PASS failures"
- MUST_FOLLOW count: "Failed 5 MUST_FOLLOW rubrics"

### 2. Rubric Rationales ARE Brief (8-15 words)

**✅ Good Example:**
> "Parameter must exist to be passed through for tokenization."

**❌ Bad Example:**
> "This is really important because without this parameter the code won't be able to pass the blocksize value through to the tokenization function which is critical for generating unique task names."

### 3. Must Have At Least ONE Rubric for EACH Type

Required types:
- ✅ Correctness (5-7 rubrics, ~60% of total)
- ✅ Code style (at least 1)
- ✅ Summary (at least 1)
- ✅ Agent behavior (at least 1)

### 4. All Rubrics Must Be Evidence-Based

**Code change rubrics** → agent_patch.diff
**Behavior rubrics** → traj_search.py --evidence
**Summary rubrics** → traj_search.py --thoughts
**Test results** → report.json (for ratings, not rubrics)

---

## 📄 Single File Deliverable Format

Create one markdown file per task (e.g., `evaluation_analysis.md`):

```markdown
# Task Analysis: {task-name}

## Overview

**Problem Statement:**
[Brief description from instance_data.json]

**Golden Patch Summary:**
[What the correct solution does]

## Analysis of All 4 Traces

### trace_01_{model}

**Approach:**
[What the agent did]

**Code Changes:**
[Summary from --diff-summary]

**Evidence from traj_search.py:**
- Resolved: ✅ true
- FAIL_TO_PASS: 3 passed, 0 failed
- Steps: 30
- Loop detected: No

**Key Findings:**
[Specific observations]

### trace_02_{model}

[Same structure]

### trace_03_{model}

[Same structure]

### trace_04_{model}

[Same structure]

## Evaluation

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

### Rubrics

```json
{
  "rubric_01": {
    "criterion": "The patch includes blocksize in tokenize call for unique names.",
    "rationale": "Blocksize determines chunking; different values need different keys.",
    "type": "correctness",
    "importance": "MUST_FOLLOW",
    "is_positive": "true"
  },
  "rubric_02": {
    ...
  },
  ...
}
```

### Rubrics Rating

```json
{
  "trace_01": {
    "rubric_01": "PASS",
    "rubric_02": "FAIL",
    ...
  },
  "trace_02": {
    ...
  },
  "trace_03": {
    ...
  },
  "trace_04": {
    ...
  }
}
```

### Overall Rating

```json
{
  "trace_01": {
    "rating": 2,
    "rationale": "Low quality fix that tokenizes block_lists instead of blocksize, causing deterministic naming tests to fail. The agent did not add blocksize parameter to function signature or pass it from read_pandas, missing the core architectural fix. Tests show resolved: false with 2 FAIL_TO_PASS failures. Failed 5 MUST_FOLLOW rubrics."
  },
  "trace_02": {
    ...
  },
  "trace_03": {
    ...
  },
  "trace_04": {
    ...
  }
}
```
```

---

## ✅ Quality Checklist

Before finalizing your deliverable:

### Evidence Verification
- [ ] Used `--compare` to get overview of all 4 traces
- [ ] Used `--summary` for each trace to get resolved status
- [ ] Used `--diff-summary` to see patch changes
- [ ] Used `--evidence` to gather verifiable claims
- [ ] Checked report.json for test results

### Rubric Quality
- [ ] 8-10 total rubrics
- [ ] At least one of each type (correctness, code style, summary, agent behavior)
- [ ] 50-70% are MUST_FOLLOW
- [ ] All code change rubrics verifiable in agent_patch.diff
- [ ] NO rubrics about "tests passing" (use report.json for ratings instead)
- [ ] All criteria are 8-15 words and specific
- [ ] All rubric rationales are 8-15 words

### Grading Accuracy
- [ ] All 4 traces graded for all rubrics
- [ ] Grades are PASS or FAIL only
- [ ] Each grade is supportable by evidence from diffs or traj_search.py
- [ ] Used report.json to verify test results for ratings

### Rating Quality
- [ ] Each trace has rating 1-5
- [ ] Ratings align with MUST_FOLLOW failures
- [ ] Rating rationales are 50-75 words
- [ ] Rationales mention specific code issues and test results
- [ ] Rationales state MUST_FOLLOW failure count at end
- [ ] NO references to rubric numbers (rubric_01, etc.)

### Metadata Completeness
- [ ] Must-read files extracted from golden_patch.diff (non-test files only)
- [ ] Must-check tests extracted from golden_patch.diff (test files only)
- [ ] All paths use /testbed/ prefix

### Deliverable Format
- [ ] Single markdown file per task
- [ ] Contains analysis of all 4 traces
- [ ] Contains complete evaluation.txt JSON sections
- [ ] Evidence from traj_search.py included

---

## 🚨 Common Mistakes to Avoid

### ❌ Mistake 1: Test Result Rubrics
```json
{
  "criterion": "The target test passes after the fix",
  "type": "correctness"
}
```
**Why wrong:** Tests passing/failing is in report.json, not in the code diff. Rubrics check code, not execution results.

**✅ Instead:** Mention test results in rating rationales, not rubrics.

### ❌ Mistake 2: Vague Rubrics
```json
{
  "criterion": "The agent fixes the bug correctly"
}
```
**Why wrong:** Not specific, not verifiable.

**✅ Instead:** "The patch adds blocksize parameter to text_blocks_to_pandas signature."

### ❌ Mistake 3: Tool-Specific Rubrics
```json
{
  "criterion": "Agent uses grep to search for function definitions"
}
```
**Why wrong:** Focuses on tools, not goals.

**✅ Instead:** "Agent reads csv.py to understand tokenization before changes."

### ❌ Mistake 4: Long Rationales
```json
{
  "rationale": "This is very important because when the parameter doesn't exist the code won't work properly and will fail at runtime when it tries to access a parameter that was never defined in the function signature which means the function will raise an error."
}
```
**Why wrong:** Rubric rationales should be 8-15 words.

**✅ Instead:** "Parameter must exist to be passed through for tokenization."

### ❌ Mistake 5: Missing Evidence
Creating rubrics without checking diffs or using traj_search.py.

**✅ Instead:** Always verify each rubric with concrete evidence before finalizing.

---

## 📚 Reference Examples Structure

When reviewing GOOD_EXAMPLES folder, look for:

1. **How rubrics are written**
   - Specific function/file names
   - Verifiable in code diffs
   - 8-15 word criteria and rationales

2. **How ratings are written**
   - 50-75 words
   - Specific issues mentioned
   - Test results included
   - MUST_FOLLOW count stated

3. **Rubric distribution**
   - ~60% correctness type
   - ~60% MUST_FOLLOW importance
   - All 4 types represented

4. **Evidence usage**
   - Claims backed by diffs
   - Agent actions verified
   - Test results from report.json

---

## 🎯 Quick Start Checklist

When starting a new task:

1. [ ] Run `python traj_search.py --compare trace_01/*.traj trace_02/*.traj trace_03/*.traj trace_04/*.traj`
2. [ ] Run `python traj_search.py trace_XX/*.traj --summary` for each trace
3. [ ] Read `golden_patch.diff`
4. [ ] Read all 4 `agent_patch.diff` files
5. [ ] Run `python traj_search.py trace_XX/*.traj --evidence` for each trace
6. [ ] Create 8-10 evidence-based rubrics (NO test result rubrics)
7. [ ] Grade all 4 traces against all rubrics
8. [ ] Check report.json for test results
9. [ ] Assign ratings 1-5 with 50-75 word rationales
10. [ ] Create single markdown deliverable with embedded JSON

---

## 🔑 Key Principles Summary

1. **Evidence-Based**: All rubrics must be verifiable through diffs or traj_search.py
2. **Code vs Tests**: Rubrics check code (in diffs), ratings use test results (from report.json)
3. **Use traj_search.py**: Essential tool at every step, not optional
4. **All 4 Traces**: Always evaluate all 4, never exclude upfront
5. **Single File**: One markdown deliverable per task with embedded JSON
6. **Specific Language**: Use exact names, paths, parameters (8-15 words)
7. **Complete Coverage**: At least one rubric of each type

---

## Final Notes

Your goal is to create objective, reproducible evaluations that help train better coding agents. Every rubric must be verifiable. Every rating must be justified with specific evidence. Use traj_search.py extensively to gather this evidence and make your evaluation defensible.

Good luck!
