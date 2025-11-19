# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This repository contains trajectory data for coding agent evaluation. Each task folder includes:
- Agent trajectories showing different approaches to solving coding problems
- Golden patches (reference solutions)
- Test data and instance metadata
- Evaluation forms with rubrics and ratings

The primary workflow is **annotating agent trajectories** using structured rubrics to evaluate coding agent performance.

## 🎓 Key Lessons from Good Examples

**CRITICAL UPDATES based on reviewing actual good examples:**

1. **✅ Rationales ARE detailed (2-4 sentences)** - NOT "1-2 concise sentences"
   - Include specific numbers: "35 steps", "14 tests broken", "7 test runs"
   - Reference failed rubrics: "Fails rubric_05 (scope creep), rubric_07 (no pytest)"
   - Explain WHY rubrics failed with context

2. **❌ DO NOT penalize for test/reproduction files**
   - Good examples show agents leaving repro scripts with rating 5/5
   - Focus rubrics on: correctness, scope, testing behavior, code organization
   - NOT on: file cleanup, leftover test scripts

3. **✅ Must have at least ONE rubric for EACH type**
   - Correctness (40-50%)
   - Code style (at least 1)
   - Summary (at least 1)
   - Agent behavior (at least 1)

4. **✅ Specific failures ARE mentioned in rationales**
   - "validates both GSI and LSI when only GSI was required"
   - "broke 14 existing tests because list order carries semantic meaning"
   - "modified a documentation file unnecessarily"

## Repository Structure

```
Trajectories/
├── Coding Agent Rubrics Data Annotation Guideline (v2).md  # Main annotation guide
├── {task-name}/                                            # One folder per task
│   ├── instance_data.json                                  # Task metadata and test info
│   ├── golden_patch.diff                                   # Reference solution
│   ├── test_patch.diff                                     # Test changes
│   ├── evaluation.txt                                 # YOUR DELIVERABLE
│   ├── trace_01_{model}/                                   # Agent trajectory 1
│   │   ├── {task-name}.traj                               # Full action log (JSON)
│   │   ├── agent_patch.diff                               # Agent's solution
│   │   ├── report.json                                    # Test results
│   │   └── test_output.txt                                # Test execution output
│   ├── trace_02_{model}/
│   ├── trace_03_{model}/
│   └── trace_04_{model}/
```

## Quality Standards (Critical!)

**These are the most important rules for high-quality annotations:**

1. **Difficulty**: Be realistic - include investigation time, not just implementation
   - ❌ "0 ~ 15 min" for a one-line fix that requires investigation
   - ✅ "15 min ~ 1 hour" for same fix (investigation + implementation)

2. **Must-read files**: Keep minimal - ONLY files essential for the CORRECT fix
   - ❌ Include files agents might explore but aren't needed for correct solution
   - ✅ Only include files the golden patch modifies or must be understood

3. **Rationales**: 2-4 detailed sentences explaining what went wrong
   - ✅ **DO** include specific failure reasons: "validates both GSI and LSI when only GSI was required (rubric_05 - scope creep)"
   - ✅ **DO** include relevant counts/numbers: "7 test runs", "35 steps", "breaks 14 existing tests"
   - ✅ **DO** explain which rubrics failed and why: "Fails 2 rubrics: leaves repro script (rubric_05), doesn't run pytest (rubric_07)"
   - ❌ **DON'T** compare traces: "better code organization compared to trace_01"
   - ❌ **DON'T** use overly specific evidence: "viewed VAR_FLAGS at lines 796-800 in step 42"
   - ✅ **Example**: "Clean implementation that fixes the bug (35 steps). Fails 2 rubrics: validates LSI unnecessarily (rubric_05 - scope creep), doesn't run pytest (rubric_07). Despite cleanup gaps, core fix is correct."

4. **Test/Repro Files**: DO NOT penalize for leaving reproduction or test scripts
   - ❌ "leaves 5 test files in the final patch" - NOT a standard rubric criterion
   - ✅ Focus rubrics on correctness, scope, testing behavior, code organization instead
   - 📝 Good examples show agents leaving repro scripts with perfect ratings

5. **Rubric Coverage**: Must have at least ONE rubric for EACH type
   - ✅ Correctness (40-50% of total)
   - ✅ Code style (at least 1)
   - ✅ Summary (at least 1)
   - ✅ Agent behavior (at least 1)

## Core Annotation Workflow

### Step 1: Read Task Data
```bash
# Start by reading these files in order:
cat {task-name}/instance_data.json     # Problem statement, tests
cat {task-name}/golden_patch.diff      # Reference solution
cat {task-name}/test_patch.diff        # Test additions
```

### Step 2: Analyze ALL 4 Trajectories
- **Read all 4 agent patches**: `trace_*/agent_patch.diff`
- **Read test results**: `trace_*/report.json`
- **Examine trajectory files**: `trace_*/*.traj` (check what agents searched for, viewed)
- **Grade ALL 4 traces** against your rubrics
- **Calculate ratings for ALL 4 traces**

### Step 3: Present Full Analysis and Select 3
- **Show complete evaluation JSON for ALL 4 trajectories**:
  - Full `rubrics_rating` JSON block with all 4 traces
  - Full `overall_rating` JSON block with all 4 traces
  - Similarity analysis between traces
- **Ask user to confirm selection** of which 3 to include
- **Selection criteria**: Exclude the trace most similar to another (diversity)
- Common pattern: If trace_01 and trace_04 use similar approaches, exclude one
- **User makes final decision** on which trace to exclude

### Step 4: Create Two Deliverable Files

You will create **exactly 2 files**:

#### File 1: `FULL_4_TRACE_ANALYSIS.md`
Contains complete analysis of ALL 4 traces:
- Task metadata
- All rubrics definitions
- Individual analysis of each trace (approach, test results, trajectory findings)
- Complete rubrics_rating JSON for all 4 traces
- Complete overall_rating JSON for all 4 traces
- Similarity analysis and recommendation

#### File 2: `evaluation.txt`
Contains only the **3 selected traces** (after user confirms selection):
- Task metadata
- Rubrics definitions
- Rubrics rating for only 3 traces
- Overall rating for only 3 traces

---

The `evaluation.txt` must follow this exact structure:

```
Evaluation Form - EVALUATED
Language *
{Python|Rust|JavaScript|TypeScript|Java|C++|C}

Category *
{bug fixing|feature development|system optimization|documentation|refactoring}

Difficulty *
{0 ~ 15 min|15 min ~ 1 hour|1 hour ~ 4 hours}
(Be realistic - include investigation time, not just implementation time)

Must-read files *
[
  "/testbed/path/to/file1.py"
]
(Keep minimal - ONLY files essential for the CORRECT fix, not files agents might explore)

Must-check tests *
[
  "/testbed/tests/test_file.py"
]

Rubrics *
{
  "rubric_01": {
    "type": "{correctness|code style|summary|agent behavior}",
    "criterion": "Specific requirement...",
    "rationale": "Why this matters...",
    "importance": "{MUST_FOLLOW|GOOD_TO_HAVE}",
    "is_positive": "{true|false}"
  },
  ...
}

Rubrics rating *
{
  "trace_01": {
    "rubric_01": "{PASS|FAIL}",
    ...
  },
  ...
}

Overall rating *
{
  "trace_01": {
    "rating": {1-5},
    "rationale": "2-4 detailed sentences. Include specific failure reasons, relevant counts, and which rubrics failed. NO trace comparisons. NO overly specific evidence (line/step numbers)."
  },
  ...
}
```

**Rationale Writing Rules (Based on Good Examples):**
- ✅ **DO**: Mention specific numbers: "35 steps", "7 test runs", "14 tests broken"
- ✅ **DO**: Reference which rubrics failed: "Fails 2 rubrics: rubric_05 (scope creep), rubric_07 (no pytest)"
- ✅ **DO**: Explain WHY rubrics failed with context
- ✅ **DO**: Describe the approach quality: "most efficient", "overly conservative", "comprehensive"
- ✅ **DO**: Write 2-4 sentences for sufficient detail
- ❌ **DON'T**: Compare traces: "better than trace_01"
- ❌ **DON'T**: Use overly specific evidence: "viewed at lines 796-800 in step 42"

## Critical Rubric Requirements

**MUST FOLLOW THESE RULES:**

1. **40-50% must be "correctness" type rubrics** (highest priority)
2. **5-10 total rubrics** - quality over quantity
3. **At least ONE rubric for EACH type**:
   - ✅ Correctness (40-50% of total, 4-5 rubrics)
   - ✅ Code style (at least 1 rubric)
   - ✅ Summary (at least 1 rubric)
   - ✅ Agent behavior (at least 1 rubric)
4. **Binary grading only**: PASS or FAIL (no partial credit)
5. **Task-specific criteria** - avoid generic statements like "agent should fix the bug"
   - ❌ Bad: "The agent must fix the issue"
   - ✅ Good: "The patch must add 'from_module_getattr' to VAR_FLAGS in nodes.py:797"
6. **Harness-agnostic** - describe goals, not tools
   - ❌ Bad: "Agent should run grep at least once"
   - ✅ Good: "Agent must inspect the base class before implementing derived class"
7. **Use trace names**: `trace_01`, `trace_02`, `trace_03` (NOT full folder names)
8. **DO NOT penalize for test/repro files** - Good examples show agents leaving reproduction scripts with perfect ratings
   - ❌ Bad: "The agent leaves 5 test files in the final patch"
   - ✅ Good: Focus on correctness, scope, testing behavior, code organization instead

## Rating Scale

| Score | Meaning |
|-------|---------|
| 5 | Perfect fix, no regressions, clean code |
| 4 | Good fix, minor issues |
| 3 | Some mistakes, partial fix |
| 2 | Low quality, multiple MUST_FOLLOW failures |
| 1 | Wrong, harmful, or nonsense solution |

### Rationale Examples

**❌ BAD - Compares traces:**
> "While the helper function shows better code organization compared to trace_01, the solution still fails the two most critical MUST_FOLLOW rubrics."

**❌ BAD - Too specific with evidence (line numbers, step numbers):**
> "The agent viewed VAR_FLAGS at lines 796-800 in step 42 during investigation..."

**✅ GOOD - Detailed with specific failures, counts, and reasons (from actual good examples):**
> "Clean, efficient solution that successfully fixes the bug with all tests passing. Most concise implementation at only 35 steps and 2 file edits. Uses MockValidationException directly without custom exception class. Fails 2 rubrics: validates both GSI and LSI using all_indexes() when only GSI was required (rubric_05 - scope creep), and doesn't run pytest tests (rubric_07 - no test-based verification). The minimalist approach is elegant but over-engineers the validation scope and skips test verification."

**✅ GOOD - Mentions specific failures with context:**
> "The agent implemented a sorting function but took an overly conservative approach by only sorting the $defs section rather than comprehensively sorting the entire schema structure. This caused the main test_by_alias to fail since properties were not sorted. The agent also modified a documentation file unnecessarily and defined the function as an instance method rather than at module level. With 5 MUST_FOLLOW failures including not fixing the target test, this is a low-quality solution that doesn't solve the core problem."

**✅ GOOD - Includes relevant numbers and rubric references:**
> "The agent fixed the main test_by_alias successfully but took an overly aggressive approach by sorting list items based on their JSON string representation. This broke 14 existing tests because list order often carries semantic meaning in JSON schemas (tuple types, discriminated unions, enum values). While the core sorting logic is sound, the failure to recognize that list order matters resulted in significant regressions."

**Key Principles from Good Examples:**
1. ✅ DO mention specific numbers: "35 steps", "14 tests broken", "7 test runs"
2. ✅ DO reference which rubrics failed: "rubric_05", "rubric_07"
3. ✅ DO explain WHY rubrics failed: "scope creep", "no test-based verification"
4. ✅ DO describe the approach: "overly conservative", "most efficient"
5. ❌ DON'T compare to other traces: "better than trace_01"
6. ❌ DON'T use overly specific evidence: "step 42", "lines 796-800"

## How to Verify Test Results

```bash
# Check if trace passed or failed:
cat trace_01_*/report.json | grep '"resolved"'

# For Python tasks, look for:
# "resolved": true  → tests passed
# "resolved": false → tests failed
```

## Trajectory Search Tool (traj_search.py)

**📖 See `TRAJ_SEARCH_README.md` for full documentation**

Use the **`traj_search.py`** utility to search and analyze trajectory files:

```bash
# Get overall statistics
python traj_search.py trace_01_*/*.traj --stats

# Search for specific patterns (e.g., VAR_FLAGS)
python traj_search.py trace_01_*/*.traj --search "VAR_FLAGS"

# Count occurrences
python traj_search.py trace_01_*/*.traj --search "VAR_FLAGS" --count

# See what files the agent viewed
python traj_search.py trace_01_*/*.traj --files-viewed

# See what files the agent edited
python traj_search.py trace_01_*/*.traj --files-edited

# Extract agent thoughts/reasoning
python traj_search.py trace_01_*/*.traj --thoughts

# 🎯 NEW: Generate evidence for QA and annotation
python traj_search.py trace_01_*/*.traj --evidence
python traj_search.py trace_01_*/*.traj --evidence files-modified
python traj_search.py trace_01_*/*.traj --evidence search --evidence-pattern "VAR_FLAGS"
```

**Essential Analysis Patterns:**

```bash
# Did the agent see VAR_FLAGS?
python traj_search.py trace_01_*/*.traj --search "VAR_FLAGS" --count

# Which files did they investigate?
python traj_search.py trace_01_*/*.traj --files-viewed | grep -E "nodes|lookup"

# Compare what different traces viewed
for trace in trace_0{1,2,3,4}_*; do
    echo "=== $trace ==="
    python traj_search.py $trace/*.traj --files-viewed
done
```

**🎯 Quality Assurance with Evidence Generation:**

The `--evidence` flag generates copy-paste ready evidence for annotation:

```bash
# Generate all evidence types (files modified, viewed, tests, searches)
python traj_search.py trace_01_*/*.traj --evidence

# Use evidence to verify claims:
# - "Agent modified lookup.py at steps X, Y, Z"
# - "Agent viewed VAR_FLAGS at lines 796-800"
# - "Tests passed after 3 attempts"
```

## Workflow: Present All 4 Trajectories First

**IMPORTANT**: Always analyze and present results for ALL 4 trajectories before finalizing the evaluation form.

### Recommended Presentation Format:

```markdown
## Analysis of All 4 Trajectories

### trace_01_gpt-5-2025-08-07
- **Approach**: [Brief description]
- **Tests**: PASS/FAIL
- **Key findings**: [What agent searched for, viewed, etc.]
- **Rubric Results**: X PASS, Y FAIL
- **Rating**: X/5

[... Same for trace_02, trace_03, trace_04 ...]

---

## Complete Evaluation JSON (All 4 Traces)

### Rubrics Rating (All 4)
```json
{
  "trace_01": { "rubric_01": "PASS", ... },
  "trace_02": { "rubric_01": "FAIL", ... },
  "trace_03": { "rubric_01": "FAIL", ... },
  "trace_04": { "rubric_01": "PASS", ... }
}
```

### Overall Rating (All 4)
```json
{
  "trace_01": { "rating": 4, "rationale": "..." },
  "trace_02": { "rating": 1, "rationale": "..." },
  "trace_03": { "rating": 2, "rationale": "..." },
  "trace_04": { "rating": 4, "rationale": "..." }
}
```

---

## Similarity Analysis & Recommendation
- **trace_01 vs trace_04**: HIGH similarity because [reasons]
- **Recommendation**: Exclude trace_XX
- **Rationale**: [Why this trace should be excluded]
```

Then ask the user: "Based on the complete evaluation above, should we exclude trace_XX and include traces YY, YY, YY? Or would you prefer a different selection?"

## Common Annotation Pitfalls

1. **Don't skip analyzing trace_04** - Always analyze all 4, then decide which to exclude
2. **Don't use full folder names in JSON** - Use `trace_01` not `trace_01_gpt-5-2025-08-07`
3. **Don't skip reading .traj files** - They reveal if the agent saw the answer but chose wrong path
4. **Don't make rubrics too easy** - If all traces PASS all rubrics, rubrics are too weak
5. **Don't ignore golden patch** - It shows the intended minimal solution
6. **Don't forget MUST vs GOOD_TO_HAVE** - MUST_FOLLOW failures should heavily impact rating

## Annotation Quality Checklist

Before finalizing `evaluation.txt`:

- [ ] Read all 4 traces' patches and reports
- [ ] Examined .traj files for all 4 traces
- [ ] Created 5-10 rubrics with 40-50% correctness type
- [ ] **At least ONE rubric for EACH type (correctness, code style, summary, agent behavior)**
- [ ] All rubrics are task-specific (mention actual files/functions)
- [ ] **NO rubrics about leaving test/repro files** (not a standard criterion)
- [ ] **Graded all rubrics PASS/FAIL for ALL 4 traces**
- [ ] **Calculated overall ratings for ALL 4 traces**
- [ ] **Presented complete `rubrics_rating` JSON for all 4 traces to user**
- [ ] **Presented complete `overall_rating` JSON for all 4 traces to user**
- [ ] **Provided similarity analysis and recommendation for which trace to exclude**
- [ ] **User confirmed which 3 traces to include in final form**
- [ ] Created final evaluation.txt with only the 3 selected traces
- [ ] Overall ratings align with rubric failures
- [ ] Used correct trace names (`trace_01` not `trace_01_gpt-5...`)
- [ ] **Rating rationales are 2-4 detailed sentences**
- [ ] **Rationales mention specific failures: which rubrics failed and WHY**
- [ ] **Rationales include relevant numbers: "35 steps", "7 test runs", "14 tests broken"**
- [ ] **Rationales DON'T compare traces or use overly specific evidence (line/step numbers)**

## Deliverables: Exactly 2 Files

For each task, you create **exactly 2 files**:

1. **`FULL_4_TRACE_ANALYSIS.md`** - Full analysis of all 4 traces (presented to user first)
2. **`evaluation.txt`** - Final submission with only 3 selected traces (after user confirms)

## Reference Examples

### Good Examples (Study These!)

**GOOD_EXAMPLES/** folder contains high-quality annotations to learn from:

1. **`getmoto__moto-6510/evaluation.txt`** - Feature development
   - Shows agents leaving repro scripts with rating 5/5
   - Clean rubrics focused on correctness, not file cleanup
   - Rationales: concise but complete

2. **`pydantic__pydantic-6043/evaluation.txt`** - System optimization
   - Shows detailed rationales mentioning specific failures
   - "broke 14 existing tests", "modified documentation file unnecessarily"
   - Ratings 2-4 showing quality gradient

3. **`iterative__dvc-1809/evaluation.txt`** - Feature development
   - Multiple MUST_FOLLOW failures properly graded
   - Rationales explain WHY rubrics failed

4. **`facebookresearch__hydra-1915/evaluation.txt`** - Bug fixing
   - Shows rubric about code organization (custom exception vs. not)
   - Ratings 2-4 with clear differentiation

### Your Reference Example

See `python__mypy-10430/` for a complete annotation from this workflow:

1. **`FULL_4_TRACE_ANALYSIS.md`** ⭐
   - Shows all 4 traces analyzed
   - Includes rubrics, metadata, full JSON evaluations
   - Similarity analysis and recommendation
   - User sees this first to decide which 3 to keep

2. **`evaluation.txt`** ✅
   - Contains only the 3 selected traces
   - Final deliverable after user confirmation
   - Follows exact required format

**Workflow**: Create FULL_4_TRACE_ANALYSIS.md → Present to user → User confirms selection → Create evaluation.txt with 3 traces

**Key Reminders:**
- ✅ Rationales should be 2-4 detailed sentences
- ✅ Include specific failure reasons from failed rubrics
- ✅ Must have at least one rubric for each type (correctness, code style, summary, agent behavior)
- ❌ Don't penalize for leaving test/repro files