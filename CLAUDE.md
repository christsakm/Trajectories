# Creating evaluation.txt Files: Comprehensive Guide

## 1. Overview & Purpose

The `evaluation.txt` file is a critical component of coding agent trajectory annotation. It serves as a structured evaluation framework that defines:

- **Task metadata**: Language, category, difficulty, and critical files
- **Evaluation rubrics**: Specific, task-tailored criteria for assessing agent performance
- **Trajectory grading**: Binary PASS/FAIL assessments for each rubric across multiple agent trajectories
- **Overall ratings**: Holistic 1-5 quality scores with detailed rationales

This file enables systematic, objective evaluation of coding agent solutions by creating clear, testable criteria before reviewing agent trajectories. The rubrics distinguish between high-quality and low-quality solutions while remaining agnostic to specific agent implementations or tooling.

**Purpose**: Create reproducible, evidence-based evaluations that train and assess coding agents on real-world software engineering tasks.

---

## 2. Quick Start Guide

### Essential Steps Checklist

1. **Understand the task**: Read problem statement, identify bug/feature requirements
2. **Review golden patch**: Understand the correct solution approach
3. **Fill metadata**: Language, category, difficulty, must-read files, must-check tests
4. **Review 3-4 trajectories**: Understand what agents did (code diffs, actions, test results)
5. **Create 7-10 rubrics**: Task-specific, binary criteria (40-60% correctness type)
6. **Grade trajectories**: Assign PASS/FAIL for each rubric on each trajectory
7. **Assign overall ratings**: 1-5 scale with detailed rationales
8. **Validate**: Check formatting, specificity, and coverage

### Required Inputs

- Problem statement (issue description)
- Golden reference patch (correct solution)
- 3-4 agent trajectories (code diffs, actions, test results)
- Test suite results (FAIL_TO_PASS and PASS_TO_PASS tests)

### Expected Output

A complete `evaluation.txt` file containing:
- Metadata (5 fields)
- Rubrics (7-10 task-specific criteria)
- Rubrics rating (PASS/FAIL for each trajectory)
- Overall rating (1-5 score with rationale for each trajectory)

---

## 3. Metadata Section

The metadata section provides essential context about the task. All fields are required and follow strict formatting rules.

### 3.1 Language

**Options**: Python, Rust, JavaScript, TypeScript, Java, C++, C

**Selection criteria**: Primary language of the files being modified

```json
"language": "Python"
```

### 3.2 Category

**Options**:
- `bug fixing`: Fixing broken functionality, handling errors, correcting behavior
- `feature development`: Adding new capabilities, parameters, or functionality
- `system optimization`: Performance improvements, efficiency enhancements
- `documentation`: Adding/updating docs, comments, or examples
- `refactoring`: Code restructuring without changing behavior

**Examples**:
- Bug fixing: Fixing KeyError, correcting calculation logic, handling None values
- Feature development: Adding new parameter, implementing new API endpoint

```json
"category": "bug fixing"
```

### 3.3 Difficulty

**Options**:
- `0 ~ 15 min`: Simple one-line fixes, obvious solutions
- `15 min ~ 1 hour`: Straightforward fixes requiring understanding 1-2 files
- `1 hour ~ 4 hours`: Complex fixes requiring multi-file changes or deep understanding

**Estimation basis**: Time for an experienced engineer **familiar with the codebase** to solve

```json
"difficulty": "15 min ~ 1 hour"
```

### 3.4 Must-read Files

**Definition**: Files the agent MUST view to understand and solve the task

**Format**: Absolute paths starting with `/testbed/`, JSON array of strings

**Selection criteria**:
- Files containing the bug/feature location
- Files defining interfaces or base classes needed for understanding
- Configuration files critical to the fix

**Typically**: 1-2 files for simple tasks, 2-3 for complex tasks

```json
"must_read_files": [
  "/testbed/moto/timestreamwrite/responses.py",
  "/testbed/moto/timestreamwrite/models.py"
]
```

### 3.5 Must-check Tests

**Definition**: Tests that MUST run to verify correctness and detect regressions

**Format**: Absolute paths starting with `/testbed/`, can be files or directories

**Selection criteria**:
- Tests that verify the specific bug fix or new feature
- Regression test suites for the affected module
- Integration tests if the change affects multiple components

```json
"must_check_tests": [
  "/testbed/tests/test_timestreamwrite/test_timestreamwrite_table.py",
  "/testbed/tests/test_timestreamwrite/"
]
```

---

## 4. Creating Rubrics

This is the **most critical section**. Rubrics define how you evaluate agent performance and must be:
- **Specific**: Target exact code patterns, functions, parameters
- **Binary**: PASS or FAIL only, no partial credit
- **Task-specific**: Tailored to this exact problem and codebase
- **Testable**: Can be objectively verified from code/tests/actions

### 4.1 Rubric Structure

Every rubric requires exactly 5 fields:

```json
"rubric_01": {
  "criterion": "The patch specifies stacklevel=2 when calling warnings.warn()",
  "type": "correctness",
  "importance": "MUST_FOLLOW",
  "is_positive": "true",
  "rationale": "The stacklevel parameter ensures the warning points to user code, not library internals, making it easier for users to identify where changes are needed."
}
```

**Field descriptions**:

1. **criterion** (string): Clear, specific requirement to evaluate
   - Use exact function names, parameter names, values
   - Reference specific files or code locations
   - Be concrete, not vague

2. **type** (string): Category of the rubric
   - Options: `correctness`, `agent behavior`, `code style`, `summary`
   - See section 4.2 for detailed breakdown

3. **importance** (string): Priority level
   - `MUST_FOLLOW`: Critical for correctness/functionality
   - `GOOD_TO_HAVE`: Quality improvements, style, optimization
   - See section 4.3 for decision criteria

4. **is_positive** (string): "true" or "false"
   - "true": Agent SHOULD do this (PASS = did it, FAIL = didn't)
   - "false": Agent SHOULD NOT do this (PASS = avoided it, FAIL = did it)
   - See section 4.6 for usage patterns

5. **rationale** (string): Explanation of why this criterion matters
   - Explain WHAT it checks, WHY it's important, IMPACT on users/system
   - See section 4.5 for writing guidelines

### 4.2 Rubric Types Breakdown

#### Correctness (40-60% of all rubrics)

**Scope**: Final agent-generated code

**Purpose**: Verify the solution is functionally correct

**Common criteria**:
- Core functionality is implemented correctly
- Target test passes (FAIL_TO_PASS)
- No regressions in existing tests (PASS_TO_PASS)
- Edge cases are handled (None checks, type validation)
- Correct parameters/values are used
- Behavior matches specifications

**Examples from GOOD_EXAMPLES**:

```json
{
  "type": "correctness",
  "criterion": "The patch uses __qualname__ instead of __name__ when converting a type to a string",
  "importance": "MUST_FOLLOW",
  "is_positive": "true",
  "rationale": "Using __name__ for types fails for nested classes (e.g., A.B becomes 'B' instead of 'A.B'). The __qualname__ attribute correctly includes the full qualified name including the parent class, which is essential for nested class resolution."
}
```

```json
{
  "type": "correctness",
  "criterion": "The patch properly handles the None default value of toolbar_options before performing operations like 'in' checks or .update() method calls",
  "importance": "MUST_FOLLOW",
  "is_positive": "true",
  "rationale": "The toolbar_options parameter defaults to None in the function signature. Code must check if toolbar_options is not None before using 'in' operator or calling .update() to avoid TypeError at runtime."
}
```

#### Agent Behavior (15-30% of all rubrics)

**Scope**: Entire trajectory including intermediate tool calls and actions

**Purpose**: Evaluate agent's problem-solving approach and efficiency

**Common criteria**:
- Reproduces the issue before fixing
- Reads critical files before implementation
- Doesn't modify unrelated files (scope control)
- Doesn't over-engineer solutions
- Creates appropriate tests
- Efficient tool usage (not excessive file reads or test runs)

**Examples from GOOD_EXAMPLES**:

```json
{
  "type": "agent behavior",
  "criterion": "The agent should reproduce the issue before making any edits. The reproduction script should demonstrate the KeyError when accessing RecordsIngested in the response.",
  "importance": "MUST_FOLLOW",
  "is_positive": "true",
  "rationale": "Reproducing the bug ensures the agent understands the failing scenario and avoids incorrect assumptions about the root cause."
}
```

```json
{
  "type": "agent behavior",
  "criterion": "The agent should not create new template files, sitecustomize.py, or other infrastructure files unrelated to the YAML plot parsing functionality",
  "importance": "MUST_FOLLOW",
  "is_positive": "false",
  "rationale": "Creating new files beyond what's needed for the fix adds unnecessary complexity and deviates from the minimal change approach."
}
```

#### Code Style (10-20% of all rubrics)

**Scope**: Final agent-generated code

**Purpose**: Evaluate code quality, readability, and maintainability

**Common criteria**:
- Proper variable/function naming
- Appropriate comments and documentation
- Code organization patterns
- Follows project conventions
- Module-level vs instance method placement
- Type hints and annotations

**Examples from GOOD_EXAMPLES**:

```json
{
  "type": "code style",
  "criterion": "The sorting function is defined at the module level as a standalone function rather than as an instance method of GenerateJsonSchema",
  "importance": "GOOD_TO_HAVE",
  "is_positive": "true",
  "rationale": "Module-level functions are more reusable and can be called from multiple places. The golden patch demonstrates this pattern for better code organization."
}
```

```json
{
  "type": "code style",
  "criterion": "The agent provides a clear and concise docstring for the num_workers parameter in the WSIReader class",
  "importance": "GOOD_TO_HAVE",
  "is_positive": "true",
  "rationale": "Proper documentation helps users understand the purpose and usage of the new parameter."
}
```

#### Summary (0-10% of all rubrics)

**Scope**: Final agent summary at the end of the trace

**Purpose**: Evaluate explanation quality and understanding

**Common criteria**:
- Correctly explains root cause
- Concise but complete description
- Mentions key changes and files
- Avoids irrelevant details
- Demonstrates understanding

**Examples from GOOD_EXAMPLES**:

```json
{
  "type": "summary",
  "criterion": "The agent correctly explains that the root cause is toolbar properties being passed both explicitly and through **toolbar_options unpacking, causing duplicate keyword arguments",
  "importance": "GOOD_TO_HAVE",
  "is_positive": "true",
  "rationale": "Clear understanding and explanation of the root cause demonstrates proper debugging analysis and helps future maintainers understand why the change was necessary."
}
```

### 4.3 Importance Levels

#### MUST_FOLLOW (50-70% of rubrics)

**Definition**: Critical requirements that define solution success

**Typical count**: 5-7 rubrics per evaluation

**When to use**:
- Core functionality must work correctly
- Target test must pass
- No critical regressions
- No major bugs introduced
- Correct architectural approach
- Essential edge case handling

**Impact on rating**:
- 0 failures → Rating 4 or 5
- 1-2 failures → Rating 3
- 3-4 failures → Rating 2
- 5+ failures → Rating 1

**Examples**:
- "The patch fixes the failing test test_apply_plus_dequeuing"
- "The implementation does not break any PASS_TO_PASS tests"
- "The agent reproduces the issue before making changes"

#### GOOD_TO_HAVE (30-50% of rubrics)

**Definition**: Quality improvements and best practices

**Typical count**: 2-5 rubrics per evaluation

**When to use**:
- Code style and formatting
- Documentation quality
- Optimization opportunities
- Avoiding unnecessary changes
- Clean implementation patterns

**Impact on rating**:
- Only affects distinction between ratings 4 and 5
- Many failures here can lower rating from 5 to 4
- Minimal impact on ratings 1-3

**Examples**:
- "The patch includes comments explaining the fix rationale"
- "Variable names are descriptive and follow project conventions"
- "The agent doesn't modify files outside the affected module"

### 4.4 Writing Criteria: Best Practices

#### ✅ DO: Be Specific

**Bad** (too vague):
```json
"criterion": "The agent fixes the bug correctly"
```

**Good** (specific and testable):
```json
"criterion": "The patch specifies stacklevel=2 when calling warnings.warn() to ensure the warning points to the user's code"
```

---

**Bad** (generic):
```json
"criterion": "The code handles edge cases"
```

**Good** (concrete):
```json
"criterion": "The patch checks if toolbar_options is not None before calling .update() or using 'in' operator"
```

#### ✅ DO: Use Exact Names and Values

Include:
- Exact function names: `warnings.warn()`, `create_vpc()`, `__qualname__`
- Exact parameter names: `stacklevel=2`, `is_default=True`, `num_workers`
- Exact file paths: `moto/timestreamwrite/responses.py`
- Exact test names: `test_write_records`, `test_default_vpc`
- Exact error types: `KeyError`, `TypeError`, `AttributeError`

**Example**:
```json
"criterion": "The write_records method in responses.py returns a JSON response with RecordsIngested containing Total, MemoryStore, and MagneticStore keys"
```

#### ✅ DO: Make Rubrics Independently Verifiable

Each rubric should be checkable through:
- Code inspection (grep for specific patterns)
- Test results (specific test passed/failed)
- Agent action logs (specific file was read)

**Example**:
```json
"criterion": "The patch adds num_workers parameter to the __init__ method of WSIReader class and passes it to self.client initialization",
"rationale": "This can be verified by checking the WSIReader.__init__ signature and the self.client instantiation call."
```

#### ✅ DO: Focus on One Aspect Per Rubric

**Bad** (multiple things):
```json
"criterion": "The patch fixes the bug, adds tests, and doesn't break existing functionality"
```

**Good** (split into 3 rubrics):
```json
"rubric_01": {
  "criterion": "The patch returns RecordsIngested dictionary from write_records endpoint"
},
"rubric_02": {
  "criterion": "The patch adds test validating RecordsIngested keys are present"
},
"rubric_03": {
  "criterion": "The patch does not break any existing tests in test_timestreamwrite/"
}
```

#### ❌ DON'T: Write Tool-Specific Criteria

**Bad** (harness-specific):
```json
"criterion": "The agent runs grep at least once to search for function definitions"
```

**Good** (goal-oriented):
```json
"criterion": "The agent identifies and reads the base class implementation before modifying the derived class"
```

#### ❌ DON'T: Write "Trick" Rubrics

Avoid rubrics that only one specific solution can pass while other valid solutions fail.

**Bad** (only one valid approach):
```json
"criterion": "The fix must be in checkmember.py file, not checkexpr.py"
```

Only use this if it's architecturally wrong to fix in checkexpr.py, and explain why in rationale:

**Acceptable** (if architecturally justified):
```json
"criterion": "The fix should be in checkmember.py where method attribute access is handled, not in checkexpr.py expression checking phase",
"rationale": "Adding logic in checkexpr.py indicates misunderstanding of codebase architecture. Type attribute access belongs in the member checking phase."
```

#### ❌ DON'T: Write Rubrics That All Trajectories Pass

If all 3-4 trajectories pass a rubric, it's not discriminating and may not be useful.

**Exception**: Core correctness rubrics that define minimum requirements (e.g., "test passes") are valid even if all trajectories pass.

### 4.5 Writing Rationales

Great rationales answer three questions:

1. **WHAT**: What does this rubric check?
2. **WHY**: Why does this matter?
3. **IMPACT**: What's the consequence if this criterion isn't met?

#### Formula: Technical Explanation + User/System Impact

**Example 1** (from dask__dask-10750):
```json
"rationale": "The stacklevel parameter ensures that the warning traceback points to the user's call site rather than the internal library code, making it easier for users to identify where they need to make changes."
```
- WHAT: stacklevel parameter in warnings
- WHY: Points to correct location in traceback
- IMPACT: Users can find their code that needs changes

**Example 2** (from bokeh__bokeh-13370):
```json
"rationale": "When users explicitly provide toolbar_options, those values must override defaults or computed values from merging individual plot toolbars. This respects user intent and matches expected API behavior."
```
- WHAT: toolbar_options override precedence
- WHY: User-provided values should win
- IMPACT: Respects user intent, matches API expectations

**Example 3** (from hydra__hydra-1915):
```json
"rationale": "Using __name__ for types fails for nested classes (e.g., A.B becomes 'B' instead of 'A.B'). The __qualname__ attribute correctly includes the full qualified name including the parent class, which is essential for nested class resolution."
```
- WHAT: __qualname__ vs __name__ difference
- WHY: __name__ fails for nested classes
- IMPACT: Nested class names are incorrectly resolved

#### Length Guidelines

- **Minimum**: 1 sentence (for obvious criteria)
- **Optimal**: 2-3 sentences (technical explanation + impact)
- **Maximum**: 4 sentences (only for complex technical contexts)

#### Avoid

- Circular rationales: "This is important because it's required"
- Vague justifications: "This improves code quality"
- Restating the criterion: "This matters because the patch should do X" (when criterion is "patch does X")

### 4.6 Positive vs Negative Criteria (is_positive)

#### is_positive: "true" (Agent SHOULD do this)

**Grading logic**:
- **PASS**: Agent did this ✓
- **FAIL**: Agent didn't do this ✗

**Common patterns**:
- Implementing required functionality
- Adding necessary parameters
- Handling edge cases
- Writing tests
- Reading critical files

**Examples**:
```json
{
  "criterion": "The patch specifies stacklevel=2 when calling warnings.warn()",
  "is_positive": "true"
}
// PASS if stacklevel=2 is present, FAIL if missing
```

```json
{
  "criterion": "The agent reproduces the bug before making any edits",
  "is_positive": "true"
}
// PASS if reproduction script exists, FAIL if no reproduction
```

#### is_positive: "false" (Agent SHOULD NOT do this)

**Grading logic**:
- **PASS**: Agent avoided this ✓
- **FAIL**: Agent did this (bad) ✗

**Common patterns**:
- Over-engineering (unnecessary complexity)
- Scope creep (modifying unrelated files)
- Breaking existing behavior
- Adding unnecessary features
- Incorrect patterns

**Examples**:
```json
{
  "criterion": "The patch does not add null checks or fallback logic for __module__ attribute",
  "is_positive": "false"
}
// PASS if no null checks added, FAIL if unnecessary null checks present
```

```json
{
  "criterion": "The agent should not create new template files, sitecustomize.py, or other infrastructure files",
  "is_positive": "false"
}
// PASS if no extra files created, FAIL if unnecessary files exist
```

**Use negative criteria for**:
- Common over-engineering patterns you observe in trajectories
- Scope creep prevention
- Detecting incorrect architectural choices
- Preventing anti-patterns

**Typical distribution**: 60-80% positive criteria, 20-40% negative criteria

### 4.7 Rubric Templates by Task Type

#### Bug Fixing Tasks (Standard Pattern)

**Template for 8 rubrics** (5 MUST_FOLLOW, 3 GOOD_TO_HAVE):

```json
{
  "rubric_01": {
    "criterion": "The agent reproduces the issue before making edits, showing [specific error]",
    "type": "agent behavior",
    "importance": "MUST_FOLLOW",
    "is_positive": "true",
    "rationale": "Reproduction ensures understanding of the failure scenario"
  },
  "rubric_02": {
    "criterion": "The patch implements [specific fix in specific file/function]",
    "type": "correctness",
    "importance": "MUST_FOLLOW",
    "is_positive": "true",
    "rationale": "This is the core fix that resolves the bug"
  },
  "rubric_03": {
    "criterion": "The patch handles edge case [specific case like None values]",
    "type": "correctness",
    "importance": "MUST_FOLLOW",
    "is_positive": "true",
    "rationale": "Edge case handling prevents runtime errors in production"
  },
  "rubric_04": {
    "criterion": "The failing test [test_name] passes after the fix",
    "type": "correctness",
    "importance": "MUST_FOLLOW",
    "is_positive": "true",
    "rationale": "Validates that the bug is actually fixed"
  },
  "rubric_05": {
    "criterion": "The patch does not break existing tests in [test directory]",
    "type": "correctness",
    "importance": "MUST_FOLLOW",
    "is_positive": "true",
    "rationale": "Ensures no regressions are introduced"
  },
  "rubric_06": {
    "criterion": "The patch includes [specific pattern from golden patch]",
    "type": "code style",
    "importance": "GOOD_TO_HAVE",
    "is_positive": "true",
    "rationale": "Follows the established pattern for consistency"
  },
  "rubric_07": {
    "criterion": "The agent does not modify files outside [specific module/directory]",
    "type": "agent behavior",
    "importance": "GOOD_TO_HAVE",
    "is_positive": "false",
    "rationale": "Keeps changes focused and minimizes risk"
  },
  "rubric_08": {
    "criterion": "The summary correctly explains the root cause as [specific explanation]",
    "type": "summary",
    "importance": "GOOD_TO_HAVE",
    "is_positive": "true",
    "rationale": "Demonstrates understanding for future maintenance"
  }
}
```

#### Feature Development Tasks (Standard Pattern)

**Template for 8 rubrics** (5 MUST_FOLLOW, 3 GOOD_TO_HAVE):

```json
{
  "rubric_01": {
    "criterion": "The patch adds [parameter/field] to [specific class/function]",
    "type": "correctness",
    "importance": "MUST_FOLLOW",
    "is_positive": "true",
    "rationale": "This is the core feature requirement"
  },
  "rubric_02": {
    "criterion": "The implementation uses the new [parameter] in [specific location]",
    "type": "correctness",
    "importance": "MUST_FOLLOW",
    "is_positive": "true",
    "rationale": "The parameter must actually affect behavior"
  },
  "rubric_03": {
    "criterion": "The patch adds tests verifying [specific new functionality]",
    "type": "correctness",
    "importance": "MUST_FOLLOW",
    "is_positive": "true",
    "rationale": "New features require test coverage"
  },
  "rubric_04": {
    "criterion": "The new feature is backward compatible / does not break existing tests",
    "type": "correctness",
    "importance": "MUST_FOLLOW",
    "is_positive": "true",
    "rationale": "Maintains stability for existing users"
  },
  "rubric_05": {
    "criterion": "The agent does not create unnecessary [files/modules]",
    "type": "agent behavior",
    "importance": "MUST_FOLLOW",
    "is_positive": "false",
    "rationale": "Minimal change approach reduces complexity"
  },
  "rubric_06": {
    "criterion": "The new parameter has appropriate documentation/docstring",
    "type": "code style",
    "importance": "GOOD_TO_HAVE",
    "is_positive": "true",
    "rationale": "Helps users understand the new feature"
  },
  "rubric_07": {
    "criterion": "Variable/parameter names are descriptive and follow project conventions",
    "type": "code style",
    "importance": "GOOD_TO_HAVE",
    "is_positive": "true",
    "rationale": "Maintains code readability and consistency"
  },
  "rubric_08": {
    "criterion": "The agent does not over-engineer with [specific unnecessary pattern]",
    "type": "agent behavior",
    "importance": "GOOD_TO_HAVE",
    "is_positive": "false",
    "rationale": "Simpler solutions are easier to maintain"
  }
}
```

### 4.8 Common Pitfalls to Avoid

#### ❌ Pitfall 1: Vague Criteria

**Bad**:
```json
"criterion": "The fix works correctly"
```

**Fix**: Be specific about what "works" means:
```json
"criterion": "The write_records endpoint returns a response with RecordsIngested.Total equal to the number of records written"
```

#### ❌ Pitfall 2: Unmeasurable Criteria

**Bad**:
```json
"criterion": "The code is clean and well-organized"
```

**Fix**: Define what clean/organized means:
```json
"criterion": "The sorting function is defined at module level rather than as an instance method"
```

#### ❌ Pitfall 3: Multiple Requirements in One Rubric

**Bad**:
```json
"criterion": "The patch fixes the bug, adds tests, and updates documentation"
```

**Fix**: Split into separate rubrics for each requirement

#### ❌ Pitfall 4: Rubrics That Don't Distinguish Trajectories

If all trajectories get the same grade (all PASS or all FAIL), the rubric isn't useful for discrimination.

**Exception**: Core requirements like "the test passes" are valid even if all trajectories pass.

#### ❌ Pitfall 5: Tool-Specific Requirements

**Bad**:
```json
"criterion": "The agent uses grep to search for function definitions"
```

**Fix**: Focus on the goal, not the tool:
```json
"criterion": "The agent reads the base class implementation before implementing the derived class"
```

---

## 5. Grading Trajectories

After creating rubrics, evaluate each trajectory against every rubric with binary PASS/FAIL grades.

### 5.1 Grading Methodology

**For each trajectory, for each rubric**:

1. **Gather evidence**:
   - Read code diffs (what was changed)
   - Check test results (what passed/failed)
   - Review agent actions (what was read, run, created)

2. **Apply criterion**:
   - Does the evidence show the criterion was met?
   - Be objective and literal

3. **Assign grade**:
   - **PASS**: Evidence clearly shows criterion met
   - **FAIL**: Evidence shows criterion not met OR no evidence criterion was met

4. **Document reasoning** (mentally or in notes):
   - What evidence led to this grade?
   - Can you point to specific lines/files/tests?

### 5.2 Grading Positive Criteria (is_positive: "true")

**Logic**: Did the agent DO this thing?

**PASS**: Yes, clear evidence in code/tests/actions
**FAIL**: No, no evidence OR opposite observed

**Example rubric**:
```json
{
  "criterion": "The patch specifies stacklevel=2 when calling warnings.warn()",
  "is_positive": "true"
}
```

**Grading**:
- **PASS**: Code shows `warnings.warn(..., stacklevel=2)`
- **FAIL**: Code shows `warnings.warn(...)` without stacklevel OR stacklevel has different value

### 5.3 Grading Negative Criteria (is_positive: "false")

**Logic**: Did the agent AVOID doing this bad thing?

**PASS**: No evidence of the bad thing, agent avoided it
**FAIL**: Evidence shows agent did the bad thing

**Example rubric**:
```json
{
  "criterion": "The agent does not modify files outside moto/timestreamwrite/",
  "is_positive": "false"
}
```

**Grading**:
- **PASS**: All modified files are in moto/timestreamwrite/
- **FAIL**: At least one modified file is outside moto/timestreamwrite/

### 5.4 Evidence Sources

#### Code Diffs
- Function signatures, parameters, return values
- Implementation logic, conditionals, loops
- Import statements, class definitions
- Comments, docstrings

#### Test Results
- Which tests passed (FAIL_TO_PASS)
- Which tests still pass (PASS_TO_PASS)
- Which tests broke (PASS_TO_FAIL)
- Test names and their assertions

#### Agent Actions
- Files read (did agent read must-read files?)
- Commands run (did agent reproduce the bug?)
- Files created (did agent create unnecessary files?)
- Sequence of actions (did agent read before implementing?)

### 5.5 Handling Ambiguous Cases

**Principle**: When in doubt, default to FAIL

**Exception**: If the rubric itself is poorly written or ambiguous, revise the rubric rather than guessing

**Common ambiguous scenarios**:

1. **Partial implementation**:
   - If rubric says "handles all edge cases" but only some are handled → FAIL
   - If rubric says "handles None values" and it does → PASS

2. **Different but valid approach**:
   - If rubric is too specific to one solution → Revise rubric to accept all valid approaches
   - If approach is architecturally different but works → Depends on rubric wording

3. **Test evidence missing**:
   - If rubric says "test X passes" but test wasn't run → Check if test file exists in trajectory
   - If test file was deleted or never run → Usually FAIL

### 5.6 Grading Format

```json
"rubrics_rating": {
  "trace_01": {
    "rubric_01": "PASS",
    "rubric_02": "FAIL",
    "rubric_03": "PASS",
    "rubric_04": "PASS",
    "rubric_05": "FAIL",
    "rubric_06": "PASS",
    "rubric_07": "FAIL",
    "rubric_08": "PASS"
  },
  "trace_02": {
    "rubric_01": "PASS",
    "rubric_02": "PASS",
    ...
  },
  "trace_03": {
    ...
  }
}
```

**Important**: Grade all rubrics for all selected trajectories (typically 3 out of 4)

---

## 6. Overall Rating System

After grading rubrics, assign an overall rating (1-5) for each trajectory with a detailed rationale.

### 6.1 Rating Scale

| Rating | Meaning | Typical Rubric Performance |
|--------|---------|---------------------------|
| **5** | Perfect fix, no regressions, clean code | All MUST_FOLLOW pass, all/most GOOD_TO_HAVE pass |
| **4** | Good fix, minor issues | All MUST_FOLLOW pass, some GOOD_TO_HAVE fail |
| **3** | Some mistakes, partial fix | 1-2 MUST_FOLLOW fail, or many GOOD_TO_HAVE fail |
| **2** | Low quality, multiple MUST_FOLLOW failures | 3-4 MUST_FOLLOW fail |
| **1** | Wrong, harmful, or nonsense solution | 5+ MUST_FOLLOW fail, or critical failures |

### 6.2 Rating Decision Framework

**Step 1**: Count MUST_FOLLOW failures
- 0 failures → Rating will be 4 or 5
- 1-2 failures → Rating will be 3
- 3-4 failures → Rating will be 2
- 5+ failures → Rating will be 1

**Step 2**: Consider GOOD_TO_HAVE failures (only if MUST_FOLLOW count suggests 4 or 5)
- Few/no GOOD_TO_HAVE failures → Rating 5
- Several GOOD_TO_HAVE failures → Rating 4

**Step 3**: Consider severity
- Did target test pass? (critical)
- Are there regressions? (critical)
- Is the approach fundamentally wrong? (drops rating)
- Are failures minor style issues? (less impact)

**Step 4**: Adjust based on holistic view
- Does the solution work in practice?
- Is it maintainable?
- Does it match golden patch approach?

### 6.3 Rating Examples from GOOD_EXAMPLES

#### Rating 5 (Perfect)

**Example from getmoto__moto-6510**:
```json
{
  "rating": 5,
  "rationale": "Perfect implementation. The patch correctly adds the RecordsIngested response structure with all required fields (Total, MemoryStore, MagneticStore). All tests pass, including the new test validating the response format. The implementation matches the AWS API specification exactly. No regressions introduced."
}
```

**Characteristics**:
- All MUST_FOLLOW: PASS
- All/most GOOD_TO_HAVE: PASS
- Clean implementation
- No regressions
- Matches golden patch

#### Rating 4 (Good)

**Example from dask__dask-10750**:
```json
{
  "rating": 4,
  "rationale": "Good fix with correct implementation of FutureWarning with stacklevel=2 parameter. All core functionality works correctly and tests pass. However, the agent ran tests more than necessary (minor inefficiency) and made small modifications to files outside the primary scope, though these don't affect correctness."
}
```

**Characteristics**:
- All MUST_FOLLOW: PASS
- Some GOOD_TO_HAVE: FAIL (efficiency, scope)
- Solution works correctly
- Minor style or process issues

#### Rating 3 (Partial)

**Example from pydantic__pydantic-6043**:
```json
{
  "rating": 3,
  "rationale": "Partial fix that implements sorting but with issues. The core sorting functionality is present but the approach causes 8 test regressions (PASS_TO_FAIL), exceeding the acceptable threshold of 5. The sorting logic may be too aggressive or change semantic meaning in some edge cases. Additionally, the implementation location differs from the golden patch pattern."
}
```

**Characteristics**:
- 1-2 MUST_FOLLOW: FAIL
- Multiple GOOD_TO_HAVE: FAIL
- Core functionality mostly works
- Some regressions or bugs

#### Rating 2 (Low Quality)

**Example from iterative__dvc-1809**:
```json
{
  "rating": 2,
  "rationale": "Low quality fix with multiple critical failures. While it attempts to add the dir_info field, the implementation is incorrect (uses string 'dir_info' instead of actual directory information structure), doesn't pass the target test, and modifies multiple unrelated files including test infrastructure. Fails 4 MUST_FOLLOW rubrics including not fixing the core issue."
}
```

**Characteristics**:
- 3-4 MUST_FOLLOW: FAIL
- Core functionality broken or wrong
- Multiple critical issues
- May have some correct elements

#### Rating 1 (Wrong/Harmful)

**Example from project-monai__monai-4943**:
```json
{
  "rating": 1,
  "rationale": "Fundamentally incorrect solution. The patch doesn't add the num_workers parameter to WSIReader class at all, instead modifying unrelated configuration files and test infrastructure. Completely misunderstands the task requirements. Fails 6 out of 7 MUST_FOLLOW rubrics. The target test cannot pass as the required functionality is not implemented."
}
```

**Characteristics**:
- 5+ MUST_FOLLOW: FAIL
- Solution doesn't work
- Wrong approach or location
- May cause harm or break functionality

### 6.4 Writing Rating Rationales

**Structure** (2-4 sentences):

1. **Opening assessment**: Overall quality (Perfect/Good/Partial/Low quality/Wrong)
2. **What works**: Positive aspects, passed rubrics
3. **What fails**: Specific failures with rubric references and impact
4. **Quantification**: Count of MUST_FOLLOW vs GOOD_TO_HAVE failures

**Formula**:
```
[Assessment]. [Positive aspects]. [Specific failures with impact]. [Quantification if helpful].
```

**Example template**:
```
"Good fix that correctly implements [core feature]. All core functionality works and tests pass. However, [specific failure 1] and [specific failure 2], failing [N] GOOD_TO_HAVE rubrics related to [category]."
```

**Best practices**:

✅ **DO**:
- Start with clear assessment (Perfect/Good/Partial/Low/Wrong)
- Reference specific rubric failures
- Explain impact of failures (breaks tests, wrong approach, etc.)
- Mention both positives and negatives
- Be concise but complete

❌ **DON'T**:
- Be vague ("some issues")
- Omit critical failures
- Only mention positives or only negatives
- Use subjective language ("seems like", "probably")
- Write long essays (keep to 2-4 sentences)

**More examples**:

```json
{
  "rating": 4,
  "rationale": "Correct implementation that adds deprecation warnings with proper FutureWarning type and stacklevel=2 parameter. The target test passes and no regressions are introduced. Minor issue: the agent modified core.py unnecessarily (failing 1 GOOD_TO_HAVE scope rubric), but this doesn't affect correctness."
}
```

```json
{
  "rating": 3,
  "rationale": "Partial fix that adds the required response fields but with implementation issues. The RecordsIngested structure is present but uses hardcoded values instead of len(records), failing 2 MUST_FOLLOW rubrics. Tests pass but the implementation doesn't match AWS specification for MagneticStore counting."
}
```

```json
{
  "rating": 2,
  "rationale": "Low quality attempt that misunderstands the root cause. The patch modifies toolbar creation logic but doesn't remove the **toolbar_options unpacking that causes duplicate kwargs. Fails 4 MUST_FOLLOW rubrics including not fixing the target test. Over-engineers with unnecessary helper functions."
}
```

### 6.5 Overall Rating Format

```json
"overall_rating": {
  "trace_01": {
    "rating": 4,
    "rationale": "Good fix that correctly implements the core functionality. All MUST_FOLLOW rubrics pass. However, fails 2 GOOD_TO_HAVE rubrics related to code organization and efficiency."
  },
  "trace_02": {
    "rating": 5,
    "rationale": "Perfect implementation matching the golden patch exactly. All rubrics pass with clean, minimal changes and comprehensive test coverage."
  },
  "trace_03": {
    "rating": 3,
    "rationale": "Partial fix with correct core logic but introduces 3 test regressions (exceeds threshold). Fails 1 MUST_FOLLOW and 3 GOOD_TO_HAVE rubrics."
  }
}
```

---

## 7. Complete Workflow Example

Let's walk through creating an evaluation.txt for `getmoto__moto-6510` (simplified):

### 7.1 Understanding the Task

**Problem**: AWS Timestream write_records endpoint returns empty response instead of RecordsIngested structure

**Expected behavior**: Response should include:
```json
{
  "RecordsIngested": {
    "Total": 123,
    "MemoryStore": 123,
    "MagneticStore": 0
  }
}
```

### 7.2 Fill Metadata

```json
"metadata": {
  "language": "Python",
  "category": "bug fixing",
  "difficulty": "15 min ~ 1 hour",
  "must_read_files": [
    "/testbed/moto/timestreamwrite/responses.py"
  ],
  "must_check_tests": [
    "/testbed/tests/test_timestreamwrite/test_timestreamwrite_table.py"
  ]
}
```

**Reasoning**:
- Python project
- Fixing missing response field (bug fixing)
- Simple fix in one file (15 min ~ 1 hour)
- Must read responses.py (where write_records response is generated)
- Must check test_timestreamwrite_table.py (contains write_records tests)

### 7.3 Review Golden Patch

Golden patch shows:
- Modified `write_records` method in responses.py
- Changed return from `"{}"` to JSON with RecordsIngested
- Uses `len(records)` for Total and MemoryStore
- Sets MagneticStore to 0

### 7.4 Review Trajectories

**Trace 1**: Correct implementation, matches golden patch
**Trace 2**: Correct but uses hardcoded values instead of len(records)
**Trace 3**: Adds response but in wrong location (models.py instead of responses.py)

### 7.5 Create Rubrics (7 rubrics)

```json
"rubrics": {
  "rubric_01": {
    "criterion": "The patch modifies the write_records method in moto/timestreamwrite/responses.py to return a JSON response containing RecordsIngested",
    "type": "correctness",
    "importance": "MUST_FOLLOW",
    "is_positive": "true",
    "rationale": "The response must be in responses.py where API responses are generated, not in models.py or other files."
  },
  "rubric_02": {
    "criterion": "The RecordsIngested dictionary includes all three required keys: Total, MemoryStore, and MagneticStore",
    "type": "correctness",
    "importance": "MUST_FOLLOW",
    "is_positive": "true",
    "rationale": "AWS API specification requires all three fields in the response structure."
  },
  "rubric_03": {
    "criterion": "The Total field is set to len(records) to reflect the actual number of records written",
    "type": "correctness",
    "importance": "MUST_FOLLOW",
    "is_positive": "true",
    "rationale": "The count must be dynamic based on actual records, not hardcoded, to match AWS behavior."
  },
  "rubric_04": {
    "criterion": "The test_write_records test passes after the patch",
    "type": "correctness",
    "importance": "MUST_FOLLOW",
    "is_positive": "true",
    "rationale": "Validates the fix resolves the original issue."
  },
  "rubric_05": {
    "criterion": "The patch does not break existing tests in test_timestreamwrite/",
    "type": "correctness",
    "importance": "MUST_FOLLOW",
    "is_positive": "true",
    "rationale": "Ensures no regressions in Timestream write functionality."
  },
  "rubric_06": {
    "criterion": "The response is properly formatted as JSON using json.dumps()",
    "type": "code style",
    "importance": "GOOD_TO_HAVE",
    "is_positive": "true",
    "rationale": "Ensures proper JSON serialization consistent with other responses in the codebase."
  },
  "rubric_07": {
    "criterion": "The agent does not modify files outside moto/timestreamwrite/ directory",
    "type": "agent behavior",
    "importance": "GOOD_TO_HAVE",
    "is_positive": "false",
    "rationale": "Keeps changes focused on the affected module, minimizing risk."
  }
}
```

### 7.6 Grade Trajectories

```json
"rubrics_rating": {
  "trace_01": {
    "rubric_01": "PASS",  // Modified responses.py ✓
    "rubric_02": "PASS",  // All 3 keys present ✓
    "rubric_03": "PASS",  // Uses len(records) ✓
    "rubric_04": "PASS",  // Test passes ✓
    "rubric_05": "PASS",  // No regressions ✓
    "rubric_06": "PASS",  // Uses json.dumps() ✓
    "rubric_07": "PASS"   // No external modifications ✓
  },
  "trace_02": {
    "rubric_01": "PASS",  // Modified responses.py ✓
    "rubric_02": "PASS",  // All 3 keys present ✓
    "rubric_03": "FAIL",  // Hardcoded values, not len(records) ✗
    "rubric_04": "PASS",  // Test passes ✓
    "rubric_05": "PASS",  // No regressions ✓
    "rubric_06": "PASS",  // Uses json.dumps() ✓
    "rubric_07": "PASS"   // No external modifications ✓
  },
  "trace_03": {
    "rubric_01": "FAIL",  // Modified models.py not responses.py ✗
    "rubric_02": "PASS",  // All 3 keys present ✓
    "rubric_03": "FAIL",  // Wrong location affects implementation ✗
    "rubric_04": "FAIL",  // Test doesn't pass (wrong location) ✗
    "rubric_05": "PASS",  // No regressions ✓
    "rubric_06": "FAIL",  // Wrong file location ✗
    "rubric_07": "PASS"   // Only modified timestreamwrite/ ✓
  }
}
```

### 7.7 Assign Overall Ratings

```json
"overall_rating": {
  "trace_01": {
    "rating": 5,
    "rationale": "Perfect implementation. The patch correctly adds RecordsIngested response with all required fields using dynamic len(records) values. Matches golden patch exactly with proper JSON formatting and no regressions."
  },
  "trace_02": {
    "rating": 4,
    "rationale": "Good implementation with all structural elements correct and tests passing. However, uses hardcoded values instead of len(records) for Total and MemoryStore (fails 1 MUST_FOLLOW rubric), which doesn't match actual AWS behavior for variable record counts."
  },
  "trace_03": {
    "rating": 2,
    "rationale": "Low quality fix due to architectural misunderstanding. Implements response in models.py instead of responses.py where API responses belong. This causes the test to fail as the response generation layer doesn't receive the structure. Fails 3 MUST_FOLLOW rubrics including core correctness."
  }
}
```

---

## 8. Quality Checklist

Before submitting your evaluation.txt, verify:

### 8.1 Metadata Completeness

- [ ] Language is specified and correct
- [ ] Category accurately describes the task type
- [ ] Difficulty estimation is reasonable for someone familiar with codebase
- [ ] Must-read files are absolute paths starting with /testbed/
- [ ] Must-read files are actually essential (1-3 files typically)
- [ ] Must-check tests are absolute paths starting with /testbed/
- [ ] Must-check tests cover the fix and regressions

### 8.2 Rubrics Quality

- [ ] Total count is 7-10 rubrics
- [ ] 40-60% are type "correctness"
- [ ] 50-70% are importance "MUST_FOLLOW"
- [ ] Each rubric has all 5 required fields
- [ ] Criteria are specific and testable (use exact names/values)
- [ ] No vague criteria ("fixes bug", "works correctly")
- [ ] No tool-specific criteria ("runs grep", "uses bash")
- [ ] No "trick" rubrics that only one solution can pass
- [ ] Rationales explain WHAT, WHY, and IMPACT
- [ ] is_positive is used correctly (true = should do, false = should not do)
- [ ] Rubrics distinguish between the provided trajectories
- [ ] Not all trajectories pass all rubrics (unless all are perfect)

### 8.3 Grading Accuracy

- [ ] All selected trajectories (typically 3) are graded
- [ ] All rubrics are graded for each trajectory
- [ ] Grades are PASS or FAIL only (no other values)
- [ ] Each grade is supportable by evidence (code/tests/actions)
- [ ] Positive criteria: PASS = did it, FAIL = didn't do it
- [ ] Negative criteria: PASS = avoided it, FAIL = did it
- [ ] Grading is consistent across trajectories

### 8.4 Overall Rating Quality

- [ ] Each trajectory has a rating (1-5) and rationale
- [ ] Ratings align with rubric results (see rating framework in 6.2)
- [ ] Rating 5: All/nearly all rubrics pass
- [ ] Rating 4: All MUST_FOLLOW pass, some GOOD_TO_HAVE fail
- [ ] Rating 3: 1-2 MUST_FOLLOW fail
- [ ] Rating 2: 3-4 MUST_FOLLOW fail
- [ ] Rating 1: 5+ MUST_FOLLOW fail or critical failure
- [ ] Rationales are 2-4 sentences
- [ ] Rationales mention specific rubric failures
- [ ] Rationales explain impact of failures

### 8.5 Format Validation

- [ ] Valid JSON structure
- [ ] Consistent rubric naming (rubric_01, rubric_02, ...)
- [ ] Consistent trace naming (trace_01, trace_02, ...)
- [ ] All string values are properly quoted
- [ ] All fields use correct types (strings for most, integer for rating)
- [ ] No trailing commas in JSON
- [ ] Proper nesting of objects

---

## 9. Reference Examples

The GOOD_EXAMPLES directory contains 9 excellent evaluation.txt files you can reference:

### 9.1 Bug Fixing Examples

1. **bokeh__bokeh-13370**
   - Complex TypeScript + Python dual-file bug
   - Focus: Dict merge precedence, None handling
   - Rubrics: 10 (6 MUST_FOLLOW, 4 GOOD_TO_HAVE)
   - Use for: Multi-language bugs, API precedence issues

2. **dask__dask-10750**
   - Deprecation warning implementation
   - Focus: Warning parameters (stacklevel, category)
   - Rubrics: 9 (5 MUST_FOLLOW, 4 GOOD_TO_HAVE)
   - Use for: Warning/logging tasks, parameter correctness

3. **facebookresearch__hydra-1915**
   - Nested class name resolution (__qualname__ vs __name__)
   - Focus: Python language features, over-engineering detection
   - Rubrics: 10 (6 MUST_FOLLOW, 4 GOOD_TO_HAVE)
   - Use for: Language-specific bugs, preventing over-engineering

4. **pydantic__pydantic-6043**
   - JSON schema sorting for deterministic output
   - Focus: Semantic preservation, acceptable regression thresholds
   - Rubrics: 10 (5 MUST_FOLLOW, 5 GOOD_TO_HAVE)
   - Use for: Sorting/ordering tasks, regression management

5. **python__mypy-16670**
   - Type system bug with staticmethod on generic classes
   - Focus: Type parameter propagation, architectural correctness
   - Rubrics: 9 (6 MUST_FOLLOW, 3 GOOD_TO_HAVE)
   - Use for: Type system bugs, architectural location importance

### 9.2 Feature Development Examples

6. **getmoto__moto-6510**
   - Adding RecordsIngested to API response
   - Focus: API structure, field completeness
   - Rubrics: 7 (5 MUST_FOLLOW, 2 GOOD_TO_HAVE)
   - Use for: Simple API additions, response structure tasks

7. **iterative__dvc-1809**
   - Adding dir_info field to cache entry
   - Focus: Data structure additions, scope control
   - Rubrics: 7 (5 MUST_FOLLOW, 2 GOOD_TO_HAVE)
   - Use for: Data structure modifications, simple features

8. **iterative__dvc-3992**
   - Adding YAML plot file parsing
   - Focus: Minimal changes, code reuse, preventing over-engineering
   - Rubrics: 10 (5 MUST_FOLLOW, 5 GOOD_TO_HAVE)
   - Use for: File parsing, emphasizing minimal approach

9. **project-monai__monai-4943**
   - Adding num_workers parameter for multi-threading
   - Focus: Parameter threading, test coverage
   - Rubrics: 9 (7 MUST_FOLLOW, 2 GOOD_TO_HAVE)
   - Use for: Threading/concurrency, parameterized testing

### 9.3 When to Use Each Example

**For your task is**:
- **Simple bug fix** → Reference: getmoto__moto-6510, iterative__dvc-1809
- **Complex bug fix** → Reference: bokeh__bokeh-13370, python__mypy-16670
- **API/structure addition** → Reference: getmoto__moto-6510, project-monai__monai-4943
- **Feature with file processing** → Reference: iterative__dvc-3992
- **Type system / language feature** → Reference: facebookresearch__hydra-1915, python__mypy-16670
- **Warning/deprecation** → Reference: dask__dask-10750
- **Need many negative rubrics** → Reference: iterative__dvc-3992, facebookresearch__hydra-1915

---

## 10. Appendix: Rubric Library

A collection of excellent rubrics from the 9 GOOD_EXAMPLES, organized by type.

### 10.1 Correctness Rubrics

#### Core Functionality

```json
{
  "criterion": "The patch uses __qualname__ instead of __name__ when converting a type to a string",
  "type": "correctness",
  "importance": "MUST_FOLLOW",
  "is_positive": "true",
  "rationale": "Using __name__ for types fails for nested classes (e.g., A.B becomes 'B' instead of 'A.B'). The __qualname__ attribute correctly includes the full qualified name including the parent class, which is essential for nested class resolution."
}
```

```json
{
  "criterion": "The patch properly handles the None default value of toolbar_options before performing operations like 'in' checks or .update() method calls",
  "type": "correctness",
  "importance": "MUST_FOLLOW",
  "is_positive": "true",
  "rationale": "The toolbar_options parameter defaults to None in the function signature. Code must check if toolbar_options is not None before using 'in' operator or calling .update() to avoid TypeError at runtime."
}
```

#### Test Results

```json
{
  "criterion": "The failing test test_issue_13370 passes after the patch",
  "type": "correctness",
  "importance": "MUST_FOLLOW",
  "is_positive": "true",
  "rationale": "This test specifically validates the bug fix. It must pass to confirm the issue is resolved."
}
```

```json
{
  "criterion": "The patch does not break existing tests - no more than 5 tests transition from PASS to FAIL",
  "type": "correctness",
  "importance": "MUST_FOLLOW",
  "is_positive": "true",
  "rationale": "The implementation must maintain backward compatibility. Breaking many existing tests indicates the sorting is too aggressive, incorrect, or changes semantic meaning of schemas."
}
```

#### Parameter/Value Correctness

```json
{
  "criterion": "The patch specifies stacklevel=2 when calling warnings.warn() to ensure the warning points to the user's code",
  "type": "correctness",
  "importance": "MUST_FOLLOW",
  "is_positive": "true",
  "rationale": "The stacklevel parameter ensures that the warning traceback points to the user's call site rather than the internal library code, making it easier for users to identify where they need to make changes."
}
```

```json
{
  "criterion": "The Total field in RecordsIngested is set to len(records) to reflect the actual number of records written",
  "type": "correctness",
  "importance": "MUST_FOLLOW",
  "is_positive": "true",
  "rationale": "The count must be dynamic based on actual records, not hardcoded, to match AWS behavior."
}
```

#### Architectural Correctness

```json
{
  "criterion": "The fix is implemented in checkmember.py where method attribute access is handled, not in checkexpr.py",
  "type": "correctness",
  "importance": "MUST_FOLLOW",
  "is_positive": "true",
  "rationale": "Adding logic in checkexpr.py indicates misunderstanding of the codebase architecture. Type attribute access belongs in the member checking phase."
}
```

#### API Structure

```json
{
  "criterion": "The RecordsIngested dictionary includes all three required keys: Total, MemoryStore, and MagneticStore",
  "type": "correctness",
  "importance": "MUST_FOLLOW",
  "is_positive": "true",
  "rationale": "AWS API specification requires all three fields in the response structure."
}
```

#### Data Structure

```json
{
  "criterion": "The dir_info field stores actual directory information (file count, size) as a dictionary, not just a string literal 'dir_info'",
  "type": "correctness",
  "importance": "MUST_FOLLOW",
  "is_positive": "true",
  "rationale": "The field must contain meaningful data about directory contents to be useful for cache invalidation decisions."
}
```

#### Function Propagation

```json
{
  "criterion": "The expand_type_by_instance function is updated to handle staticmethod in addition to classmethod",
  "type": "correctness",
  "importance": "MUST_FOLLOW",
  "is_positive": "true",
  "rationale": "Staticmethods accessed through parameterized generic classes need their type variables expanded by the instance, similar to classmethods. This is the core fix that resolves the type checking error."
}
```

### 10.2 Agent Behavior Rubrics

#### Reproduction

```json
{
  "criterion": "The agent reproduces the issue before making edits, showing the KeyError when accessing RecordsIngested in the response",
  "type": "agent behavior",
  "importance": "MUST_FOLLOW",
  "is_positive": "true",
  "rationale": "Reproducing the bug ensures the agent understands the failing scenario and avoids incorrect assumptions about the root cause."
}
```

#### Scope Control

```json
{
  "criterion": "The agent does not modify files outside the moto/timestreamwrite/ directory",
  "type": "agent behavior",
  "importance": "GOOD_TO_HAVE",
  "is_positive": "false",
  "rationale": "Keeps changes focused on the affected module, minimizing risk and making the change easier to review."
}
```

```json
{
  "criterion": "The agent should not edit unrelated files such as bokeh/core/properties.py or files in bokeh/models/ beyond GridPlot",
  "type": "agent behavior",
  "importance": "GOOD_TO_HAVE",
  "is_positive": "false",
  "rationale": "Modifying files outside the scope of the fix increases the risk of introducing regressions and makes the change harder to review."
}
```

#### Over-Engineering Prevention

```json
{
  "criterion": "The patch does not add null checks or fallback logic for __module__ attribute",
  "type": "agent behavior",
  "importance": "GOOD_TO_HAVE",
  "is_positive": "false",
  "rationale": "Adding unnecessary null checks for __module__ indicates over-engineering. The golden patch demonstrates such checks are not needed, and adding them suggests misunderstanding of when __module__ can be None."
}
```

```json
{
  "criterion": "The agent should not create new template files, sitecustomize.py, or other infrastructure files unrelated to YAML plot parsing",
  "type": "agent behavior",
  "importance": "MUST_FOLLOW",
  "is_positive": "false",
  "rationale": "Creating new files beyond what's needed for the fix adds unnecessary complexity and deviates from the minimal change approach."
}
```

#### Code Reuse

```json
{
  "criterion": "The agent reuses the existing _find_data function instead of reimplementing JSON/YAML parsing logic",
  "type": "agent behavior",
  "importance": "GOOD_TO_HAVE",
  "is_positive": "true",
  "rationale": "The _find_data function already exists and works correctly for JSON; reusing it for YAML ensures consistency and avoids code duplication."
}
```

#### Test Coverage

```json
{
  "criterion": "The agent adds parameterized tests covering both 'read whole image' and 'read region' scenarios with num_workers parameter",
  "type": "agent behavior",
  "importance": "MUST_FOLLOW",
  "is_positive": "true",
  "rationale": "Both reading modes must work correctly with multi-threading. Parameterized tests ensure comprehensive coverage without code duplication."
}
```

#### Reading Critical Files

```json
{
  "criterion": "The agent reads the base class implementation before implementing the derived class",
  "type": "agent behavior",
  "importance": "GOOD_TO_HAVE",
  "is_positive": "true",
  "rationale": "Understanding the base class interface and patterns ensures the derived class implementation is consistent and correct."
}
```

### 10.3 Code Style Rubrics

#### Function Placement

```json
{
  "criterion": "The sorting function is defined at the module level as a standalone function rather than as an instance method of GenerateJsonSchema",
  "type": "code style",
  "importance": "GOOD_TO_HAVE",
  "is_positive": "true",
  "rationale": "Module-level functions are more reusable and can be called from multiple places. The golden patch demonstrates this pattern for better code organization."
}
```

#### Documentation

```json
{
  "criterion": "The agent provides a clear and concise docstring for the num_workers parameter in the WSIReader class",
  "type": "code style",
  "importance": "GOOD_TO_HAVE",
  "is_positive": "true",
  "rationale": "Proper documentation helps users understand the purpose and usage of the new parameter."
}
```

#### Code Format

```json
{
  "criterion": "The response is properly formatted as JSON using json.dumps()",
  "type": "code style",
  "importance": "GOOD_TO_HAVE",
  "is_positive": "true",
  "rationale": "Ensures proper JSON serialization consistent with other responses in the codebase."
}
```

#### Pattern Consistency

```json
{
  "criterion": "The warning message format matches the pattern used elsewhere in the codebase for deprecation warnings",
  "type": "code style",
  "importance": "GOOD_TO_HAVE",
  "is_positive": "true",
  "rationale": "Consistent messaging helps users recognize deprecation warnings and understand the migration path."
}
```

#### Consolidation

```json
{
  "criterion": "The patch consolidates the type-to-string conversion logic instead of having duplicate if-else chains",
  "type": "code style",
  "importance": "GOOD_TO_HAVE",
  "is_positive": "true",
  "rationale": "Reducing code duplication improves maintainability. The golden patch demonstrates consolidating the logic into a single __qualname__ access."
}
```

### 10.4 Summary Rubrics

#### Root Cause Explanation

```json
{
  "criterion": "The agent correctly explains that the root cause is toolbar properties being passed both explicitly and through **toolbar_options unpacking, causing duplicate keyword arguments",
  "type": "summary",
  "importance": "GOOD_TO_HAVE",
  "is_positive": "true",
  "rationale": "Clear understanding and explanation of the root cause demonstrates proper debugging analysis and helps future maintainers understand why the change was necessary."
}
```

#### Conciseness

```json
{
  "criterion": "The final summary is concise (under 200 words) and focuses on the core changes without extensive debugging process details",
  "type": "summary",
  "importance": "GOOD_TO_HAVE",
  "is_positive": "true",
  "rationale": "Concise summaries are easier to read and understand. The debugging process details are less important than the final solution."
}
```

#### Accuracy

```json
{
  "criterion": "The summary accurately describes which files were modified and what the key changes were",
  "type": "summary",
  "importance": "GOOD_TO_HAVE",
  "is_positive": "true",
  "rationale": "Accurate summaries help reviewers and future maintainers quickly understand the scope and nature of the changes."
}
```

### 10.5 Complex/Compound Rubrics

#### Precedence Handling

```json
{
  "criterion": "When toolbar_options is provided, its values override the defaults or computed values from merging individual plot toolbars, rather than the reverse",
  "type": "correctness",
  "importance": "MUST_FOLLOW",
  "is_positive": "true",
  "rationale": "When users explicitly provide toolbar_options, those values must override defaults or computed values from merging individual plot toolbars. This respects user intent and matches expected API behavior."
}
```

#### Behavior Preservation

```json
{
  "criterion": "The patch adds deprecation warnings but does not change the actual behavior of the function",
  "type": "correctness",
  "importance": "MUST_FOLLOW",
  "is_positive": "true",
  "rationale": "The golden patch only adds a deprecation warning but does not change behavior. Changing behavior would break backward compatibility - behavior changes should come in a future version after deprecation period."
}
```

#### Multi-file Consistency

```json
{
  "criterion": "The fix correctly handles both TypeScript (gridplot.ts) and Python (gridplot.py) files with consistent logic",
  "type": "correctness",
  "importance": "MUST_FOLLOW",
  "is_positive": "true",
  "rationale": "Bokeh uses both TypeScript for browser code and Python for server code. The fix must be consistent across both to ensure proper functionality."
}
```

---

## Final Notes

Creating high-quality evaluation.txt files requires:

1. **Deep understanding** of the task and golden patch
2. **Careful rubric design** that is specific, testable, and task-tailored
3. **Objective grading** based on clear evidence
4. **Thoughtful rating** that reflects both rubric results and overall quality

**Remember**:
- Quality over quantity (7 excellent rubrics > 10 mediocre ones)
- Specificity is key (exact names, values, files)
- Negative rubrics catch over-engineering (essential for agent training)
- Rationales must explain WHAT, WHY, and IMPACT
- Ratings must align with rubric performance

Use the 9 GOOD_EXAMPLES as references and templates. Good luck!
- please make the trace rationales a bit more detailed. We should include the failure reason of the failed rubrics in it.
there should be at least one rubric for each type i.e. correctness, code style, summary and agent behavior.

```

please make the trace rationales a bit more detailed. We should include the failure reason of the failed rubrics in it.
there should be at least one rubric for each type i.e. correctness, code style, summary and agent behavior.

8-10 rubrics always.

for Must-read files and Must-check tests what you should do is look at the golden patch and split the filenames into (test,nontest) and include them in the appropriate array.

each trace rationale must be around 50-75 words.

each rubric rationale must be around 5-15 words.

each rubric criterion must be around 5-15 words.
