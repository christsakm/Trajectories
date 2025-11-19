# Guidelines

# **Trajectory Rubrics Annotation Guidelines**

# **Step 1: Understand the Task**

Before annotating anything, read the **problem statement** carefully.

You should understand:

* What the bug is OR what feature needs to be added

* What the correct behavior should look like

* Which files and tests belong to the task

* Whether a correct (golden) reference exists

  * If not, you infer correctness from tests \+ problem description.

Think of this step as **figuring out the judging criteria** before grading anything.

---

# **Step 2: Fill Task Metadata**

Every annotation must start with **metadata**, which describes the task itself.

### **What to fill out:**

### **1\. Language**

Choose one: `Python`, `Rust`, `JavaScript`, `TypeScript`, `Java`, `C++`, `C`.

### **2\. Category**

Choose one:

* bug fixing

* feature development

* system optimization

* documentation

* refactoring

### **3\. Difficulty**

Estimate based on how long an experienced engineer would need:

* `0 ~ 15 min`

* `15 min ~ 1 hour`

* `1 hour ~ 4 hours`

### **4\. Must-read files**

List absolutely essential files **the agent MUST read** to solve the task.

Format (absolute paths starting with `/testbed`):

`"must_read_files": [`  
  `"/testbed/src/module_x.py",`  
  `"/testbed/src/utils/helpers.py"`  
`]`

### **5\. Must-check tests**

List the tests required to confirm correctness \+ detect regressions.

`"must_check_tests": [`  
  `"/testbed/tests/test_feature_x.py",`  
  `"/testbed/tests/integration/"`  
`]`

---

# **Step 3: Select 3 trajectories**

# **Step 3: Create Task-Specific Rubrics**

This is the **most important part** of your job as an annotator.

Rubrics define **how you evaluate** each trajectory.

You must create **5–10 high-quality rubrics** based on:

* The task

* The codebase

* The core logic that must be implemented

* The common pitfalls

* The correctness criteria

* The agent’s required behavior (exploration, reproduction, testing, etc.)  
* Golden patch  
* 3 agent patches.

---

# **How to create good rubrics**

## **RULE 1 — Rubrics must distinguish between good and bad trajectories**

If all trajectories PASS all rubrics → the rubrics are too weak.

## **RULE 2 — 40–50% rubrics must be Correctness (highest priority)**

Examples:

* Patch fixes the failing test

* Implementation matches expected behavior

* Adds necessary unit tests

* Does not introduce regressions

## **RULE 3 — Rubrics must be binary**

Each rubric must be graded as:

`PASS or FAIL`

No partial credit.

## **RULE 4 — Rubrics must be *task-specific***

Avoid generic rubrics like:

“The agent should fix the bug.”  
 This is too vague.

Instead:

“The patch ensures `apply` does not dequeue operators when used with `adjoint` (verified by passing test `test_apply_plus_dequeuing`).”

## **RULE 5 — Rubrics must be harness-agnostic**

Don’t write rubrics about tools like “agent should run grep at least once.”  
 Instead describe the *goal*:

“Agent must inspect the base class before implementing the derived class.”

## **RULE 6 — Don’t write trick rubrics that only one solution can satisfy**

Good rubrics should be passable by **all correct approaches**.

## **RULE 7 — Universal rules only if absolutely necessary**

Use **UNIVERSAL** type sparingly, only when repo-specific rubric is impossible.

Examples (valid universal rubrics):

* Agent should not hallucinate code

* Agent should not skip reproducing the issue

* Agent should not claim a fix works without testing

---

# **Rubric Structure (Every rubric MUST include these fields)**

### **Required fields:**

* **criterion** — clear, specific requirement

* **is\_positive** — `"true"` (agent SHOULD do) or `"false"` (agent SHOULD NOT do)

* **type** — one of:

  * correctness

  * code style

  * summary

  * agent behavior

* **importance** — one of:

  * MUST\_FOLLOW

  * GOOD\_TO\_HAVE

  * UNIVERSAL

* **rationale** — why it matters

### **Example rubric:**

`"rubric_01": {`  
  `"criterion": "The agent must reproduce the failing test before editing any code.",`  
  `"is_positive": "true",`  
  `"type": "agent behavior",`  
  `"importance": "MUST_FOLLOW",`  
  `"rationale": "Reproducing the bug ensures the agent understands the failing scenario and avoids incorrect assumptions."`  
`}`

---

# **Step 4: Review the Trajectories**

For each trajectory:

* Read the **code diffs**

* Read the **agent’s reasoning/actions**

* Check **test results** (either provided or in report.json)

* Note:

  * What was done well

  * Any mistakes

  * Any regressions

  * Whether the issue was reproduced

  * Whether unrelated code was touched

Your goal: fully understand what the agent did and why.

---

# **Step 5: Grade Each Trajectory Against Rubrics**

For each trajectory and each rubric:

* Assign **PASS** or **FAIL**

* Use evidence from:

  * code diffs

  * test results

  * agent actions

Example:

`"rubrics_rating": {`  
  `"trace_01": {`  
    `"rubric_01": "PASS",`  
    `"rubric_02": "FAIL",`  
    `"rubric_03": "PASS"`  
  `}`  
`}`

---

# **Step 6: Assign the Overall Rating (1–5)**

Use rubric results \+ your qualitative judgment.

### **Rating meaning:**

| Score | Meaning |
| ----- | ----- |
| **5** | Perfect fix, no regressions, clean code |
| **4** | Good fix, minor issues |
| **3** | Some mistakes, partial fix |
| **2** | Low quality, multiple MUST\_FOLLOW failures |
| **1** | Wrong, harmful, or nonsense solution |

### **Overall rating example:**

`"overall_rating": {`  
  `"trace_01": {`  
`“rating”: 4,`  
  `"rationale": "Correct fix with minor code style issues; all relevant tests pass."`  
`}`  
`}`

---

# **Step 7: Final Output Package**

For each task, your final output must contain:

1. **Metadata**

2. **Rubrics**

3. **Rubrics rating for selected trajectories**

4. **Overall rating with rationales**

This forms the full annotation.

# Labeling Tool

# Video explaining the process:

1. Video link:[Annotation Workflow.mp4](https://drive.google.com/file/d/1kLxVUQrnZYcv1f2xyYFDsjj0ra7i_ecy/view?usp=sharing)  
2. Missed in the video:  
   1. You’ll see 4 trajectories, and you only choose 3 based on diversity  
   2. Find the 2 that look like each other the most, and ignore one of them.  
   3. Traces:  
      1. trace\_01\_{model\_name}  
      2. trace\_02\_{model\_name}  
      3. trace\_03\_{model\_name}  
      4. trace\_04\_{model\_name}

# Review Dimensions

| Dimension | Focus Area (What is being evaluated) | Score | Grading Criteria |
| ----- | ----- | ----- | ----- |
| **1\. Task Metadata Accuracy** | Completion and accuracy of **Step 2: Fill Task Metadata** (Language, Category, Difficulty, Must-read files, Must-check tests). | **5** | All metadata fields are accurately filled and fully compliant with all formatting requirements (e.g., correct absolute paths for files/tests, correct difficulty range). |
|  |  | **4** | All metadata fields are filled, but there are one or two minor errors (e.g., a slight over/underestimation of difficulty, a small formatting issue). |
|  |  | **3** | Most fields are correctly filled, but 1-2 critical fields (like `must_read_files` or `must_check_tests`) have significant inaccuracies or are incomplete. |
|  |  | **2** | Multiple critical metadata fields are missing or contain major errors that would hinder the agent's work (e.g., incorrect file paths, wrong language/category). |
|  |  | **1** | Metadata is largely incomplete, incorrect, or missing, making the task unusable. |
| **2\. Rubric Quality and Compliance** | Quality and adherence to **Step 3: Create Task-Specific Rubrics** rules (5–10 rubrics, Binary, Task-Specific, Correctness percentage, Required fields). | **5** | 5–10 rubrics created. All rubrics are binary, task-specific (Rule 4), harness-agnostic (Rule 5), and correctly use the required fields. **Correctness** type rubrics account for 40–50% of the total (Rule 2). Rubrics effectively distinguish between good and bad trajectories (Rule 1). |
|  |  | **4** | 5–10 rubrics created. Rubrics are generally high quality, but one rule is slightly violated (e.g., slightly outside the 40-50% Correctness range, or one rubric is slightly vague). |
|  |  | **3** | Rubrics meet the minimum quantity but contain 1-2 generic or "trick" rubrics (Rule 4, Rule 6), or the importance/type fields are occasionally misused. |
|  |  | **2** | Too few (\<5) or too many (\>10) rubrics. Multiple rubrics are generic, or the basic structure (Required Fields) is missing for several entries. |
|  |  | **1** | Rubrics are non-existent, completely generic, or fundamentally fail to define an evaluation standard. |
| **3\. Trajectory Grading Accuracy** | Accuracy in assigning **PASS/FAIL** grades in **Step 5: Grade Each Trajectory Against Rubrics**. | **5** | All PASS/FAIL grades across all trajectories are objectively and correctly assigned based on the provided code diffs, agent actions, and test results (using evidence). |
|  |  | **4** | Grades are mostly correct, with only one ambiguous or highly subjective grading decision across all rubrics/trajectories. |
|  |  | **3** | There are a few clear instances of misgrading (1-3) where a PASS should have been a FAIL or vice-versa, indicating a misunderstanding of the trajectory or the rubric. |
|  |  | **2** | Numerous misgradings (4-6) are present, or a clear pattern of bias is observed (e.g., consistently grading against an agent's correct approach). |
|  |  | **1** | The grading of trajectories is largely irrelevant to the rubric criteria or is completely missing. |
| **4\. Overall Rating Justification** | Correctness and quality of the final rating in **Step 6: Assign the Overall Rating (1–5)**, including the rationale. | **5** | The 1–5 overall score is a perfectly logical aggregation of the rubric results and correctly aligns with the documented **Rating Meaning** (Perfect, Good, etc.). The rationale is concise, clear, and fully supports the assigned score. |
|  |  | **4** | The overall score is justifiable but the rationale could be more concise or is missing one minor detail supporting the score. |
|  |  | **3** | The overall score is one point off from the aggregation of rubric scores, or the rationale is vague and fails to clearly explain the rating choice. |
|  |  | **2** | The overall score is significantly mismatched with the rubric results or the rationale is misleading/incorrect. |
|  |  | **1** | The overall rating is missing or the rationale demonstrates a complete lack of understanding of the trajectory's performance. |

# Prompts

# Note: these prompts were one-shotted and not tested thoroughly; you still have the responsibility to double-check the results.

# Rubrics Generation:

Download the deliverable and give the prompt to curser

````
You are an expert Rubric Annotator specializing in evaluating the performance of coding agents. Your task is to generate 5-10 high-quality, task-specific rubrics based on the provided problem statement, a correct 'golden' patch, and three sample agent trajectories.

**Goal:** Generate 5-10 detailed, task-specific rubrics in the exact JSON format specified below.

**Annotation Guidelines & Rules:**

1.  **Rubric Quantity:** You must create between 5 and 10 rubrics.
2.  **Binary Scoring:** Each rubric must be designed for a strict **PASS** or **FAIL** grade only.
3.  **Correctness Priority:** 40% to 50% of the total rubrics must be of the \`\`\`correctness\`\`\` **type**.
4.  **Task-Specificity:** Rubrics **must** be task-specific. Avoid generic statements like "The agent fixes the bug." Instead, describe the specific fix, implementation, or expected behavior (e.g., "The patch correctly handles null pointer exception in the file x.c").
5.  **Harness-Agnostic:** Do not write rubrics about tool usage (e.g., "agent should run grep"). Describe the *goal* (e.g., "Agent must inspect the base class before implementing the derived class").
6.  **Distinguish Trajectories:** The set of rubrics must be able to distinguish between the good and bad sample trajectories provided.
7.  **No Universal Type:** The **type** and **importance** fields **must not** use the value \`\`\`universal\`\`\`.

**Required Rubric Structure:**

Every rubric must be a JSON object with the following fields and allowed values:

*   **"criterion"**: (string) A clear, specific requirement.
*   **"is_positive"**: (string) "true" (agent SHOULD do) or "false" (agent SHOULD NOT do).
*   **"type"**: (string) Choose one: \`\`\`correctness\`\`\`, \`\`\`code style\`\`\`, \`\`\`summary\`\`\`, or \`\`\`agent behavior\`\`\`.
*   **"importance"**: (string) Choose one: \`\`\`MUST_FOLLOW\`\`\` or \`\`\`GOOD_TO_HAVE\`\`\`.
*   **"rationale"**: (string) A brief explanation of why this specific rubric matters for the task.

**Input Data (Placeholders to be filled):**

1.  **Task Data:**
@instance_data.json
2.  **Golden Reference Patch:**
	@golden_patch.diff
3.  **Agent Trajectory 1:**
	@trajectory_file1
4.  **Agent Trajectory 2:**
@trajectory_file2
4.  **Agent Trajectory 3:**
@trajectory_file3

**Output Format:**

```json
{
  "rubric_01": {
    "criterion": "...",
    "is_positive": "...",
    "type": "...",
    "importance": "...",
    "rationale": "..."
  },
  "rubric_02": {
    "criterion": "...",
    "is_positive": "...",
    "type": "...",
    "importance": "...",
    "rationale": "..."
  },
  // ... up to rubric_10
}

Example:
problem_statement:Timestream Write has the wrong response returned
Expectation for response
The AWS documentation for timestream-write.client.write_records states that the response should be a dictionary of the form:

{
    'RecordsIngested': {
        'Total': 123,
        'MemoryStore': 123,
        'MagneticStore': 123
    }
}
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write.html#TimestreamWrite.Client.write_records

Actual response
Printing the response results in:

{'ResponseMetadata': {'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'amazon.com'}, 'RetryAttempts': 0}}
Testcase
import boto3
import os
import pytest

from my_thing.main import MyClass
from moto import mock_timestreamwrite

@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    yield

@pytest.fixture
def ts_client(aws_credentials):
    with mock_timestreamwrite():
        conn = boto3.client("timestream-write")
        yield conn

@pytest.fixture
def create_ts_table(ts_client):
    ts_client.create_database(DatabaseName='ts_test_db')
    ts_client.create_table(DatabaseName='ts_test_db', TableName='ts_test_table')
    yield

def test_ts_write(ts_client, create_ts_table):
    my_object = MyClass()
    event = {} # appropriate dict here
    result = my_object.ts_write(event, 'ts_test_db', 'ts_test_table')
    assert result is True
def ts_write(self, event: dict, ts_db_name: str, ts_table_name: str) -> bool:
        ts_client = boto3.client("timestream-write")
        response = ts_client.write_records(
                DatabaseName = ts_db_name,
                TableName=ts_table_name,
                Records=[
                    {
                        "Dimensions": [
                            {"Name": "Account_Id", "Value": event["Payload"]["detail"]["Account_id"]},
                            {"Name": "Type", "Value": event["Payload"]["detail-type"]},
                        ],
                        "MeasureName": event["Payload"]["detail"]["measure_name"],
                        "MeasureValue": str(event["Payload"]["detail"]["measure_value"]),
                        "MeasureValueType": "DOUBLE",
                        "Time": str(event["Timestamp"]),
                        "TimeUnit": "SECONDS"
                    }])
        
        if response["RecordsIngested"]["Total"] > 0:
            self.logger.info("Wrote event to timestream records")
            return True
        else:
            self.logger.error("Failed to write to timestream records")
            return False
This then fails in the testing with an KeyError instead of matching the expectation set by the AWS spec.

golden_patch:
From 1f1b01a0cf9638e28dde0dd25a0fb0f15fcf3c6d Mon Sep 17 00:00:00 2001
From: Brian Pandola <bpandola@gmail.com>
Date: Fri, 18 Mar 2022 19:34:19 -0700
Subject: [PATCH] Update Response for TimestreamWrite:WriteRecords

The botocore `WriteRecordsResponse` model was updated to include `RecordsIngested` a few months ago.[1]

* Include `RecordsIngested` in the `moto` response
* Use sample records from AWS documentation in `test_write_records`

[1]:https://github.com/boto/botocore/commit/4a2fc7f7c042b6f20b10b4d9c0454dae173c9969
---
 moto/timestreamwrite/responses.py             |  9 ++-
 .../test_timestreamwrite_table.py             | 60 +++++++++++++------
 2 files changed, 51 insertions(+), 18 deletions(-)

diff --git a/moto/timestreamwrite/responses.py b/moto/timestreamwrite/responses.py
index c63d9c6b4d86..9da11edfa357 100644
--- a/moto/timestreamwrite/responses.py
+++ b/moto/timestreamwrite/responses.py
@@ -85,7 +85,14 @@ def write_records(self):
         table_name = self._get_param("TableName")
         records = self._get_param("Records")
         self.timestreamwrite_backend.write_records(database_name, table_name, records)
-        return "{}"
+        resp = {
+            "RecordsIngested": {
+                "Total": len(records),
+                "MemoryStore": len(records),
+                "MagneticStore": 0,
+            }
+        }
+        return json.dumps(resp)
 
     def describe_endpoints(self):
         resp = self.timestreamwrite_backend.describe_endpoints()
diff --git a/tests/test_timestreamwrite/test_timestreamwrite_table.py b/tests/test_timestreamwrite/test_timestreamwrite_table.py
index bc255a0eb15d..8dad6ddae00b 100644
--- a/tests/test_timestreamwrite/test_timestreamwrite_table.py
+++ b/tests/test_timestreamwrite/test_timestreamwrite_table.py
@@ -1,3 +1,4 @@
+import time
 import boto3
 import sure  # noqa # pylint: disable=unused-import
 from moto import mock_timestreamwrite, settings
@@ -176,33 +177,58 @@ def test_write_records():
     ts.create_database(DatabaseName="mydatabase")
     ts.create_table(DatabaseName="mydatabase", TableName="mytable")
 
-    ts.write_records(
+    # Sample records from https://docs.aws.amazon.com/timestream/latest/developerguide/code-samples.write.html
+    dimensions = [
+        {"Name": "region", "Value": "us-east-1"},
+        {"Name": "az", "Value": "az1"},
+        {"Name": "hostname", "Value": "host1"},
+    ]
+
+    cpu_utilization = {
+        "Dimensions": dimensions,
+        "MeasureName": "cpu_utilization",
+        "MeasureValue": "13.5",
+        "MeasureValueType": "DOUBLE",
+        "Time": str(time.time()),
+    }
+
+    memory_utilization = {
+        "Dimensions": dimensions,
+        "MeasureName": "memory_utilization",
+        "MeasureValue": "40",
+        "MeasureValueType": "DOUBLE",
+        "Time": str(time.time()),
+    }
+
+    sample_records = [cpu_utilization, memory_utilization]
+
+    resp = ts.write_records(
         DatabaseName="mydatabase",
         TableName="mytable",
-        Records=[{"Dimensions": [], "MeasureName": "mn1", "MeasureValue": "mv1"}],
-    )
+        Records=sample_records,
+    ).get("RecordsIngested", {})
+    resp["Total"].should.equal(len(sample_records))
+    (resp["MemoryStore"] + resp["MagneticStore"]).should.equal(resp["Total"])
 
     if not settings.TEST_SERVER_MODE:
         from moto.timestreamwrite.models import timestreamwrite_backends
 
         backend = timestreamwrite_backends["us-east-1"]
         records = backend.databases["mydatabase"].tables["mytable"].records
-        records.should.equal(
-            [{"Dimensions": [], "MeasureName": "mn1", "MeasureValue": "mv1"}]
-        )
+        records.should.equal(sample_records)
+
+        disk_utilization = {
+            "Dimensions": dimensions,
+            "MeasureName": "disk_utilization",
+            "MeasureValue": "100",
+            "MeasureValueType": "DOUBLE",
+            "Time": str(time.time()),
+        }
+        sample_records.append(disk_utilization)
 
         ts.write_records(
             DatabaseName="mydatabase",
             TableName="mytable",
-            Records=[
-                {"Dimensions": [], "MeasureName": "mn2", "MeasureValue": "mv2"},
-                {"Dimensions": [], "MeasureName": "mn3", "MeasureValue": "mv3"},
-            ],
-        )
-        records.should.equal(
-            [
-                {"Dimensions": [], "MeasureName": "mn1", "MeasureValue": "mv1"},
-                {"Dimensions": [], "MeasureName": "mn2", "MeasureValue": "mv2"},
-                {"Dimensions": [], "MeasureName": "mn3", "MeasureValue": "mv3"},
-            ]
+            Records=[disk_utilization],
         )
+        records.should.equal(sample_records)


Rubrics:
rubric_01:
  criterion: The agent should reproduce the issue before making any edits to fix the issue. In the repro script, it should show the KeyError of RecordsIngested not being in the response.
  is_positive: true
  type: agent_behavior
  importance: MUST_FOLLOW
rubric_02:
  criterion: In the final patch, the agent should not assign 0 value to "MagneticStore" without any explanation or comments.
  is_positive: false
  type: code_style
  importance: MUST_FOLLOW
rubric_03:
  criterion: The agent should add an additional test to cover the original issue in which different keys including RecordsIngested, Total, MemoryStore and MagneticStore should be checked as per the AWS specification.
  is_positive: true
  type: agent_behavior
  importance: MUST_FOLLOW
rubric_04:
  criterion: The agent should not run existing tests or the new tests more than 3 times as the difficulty is on the easier end.
  is_positive: false
  type: agent_behavior
  importance: GOOD_TO_HAVE
rubric_05:
  criterion: The agent should only edit moto/timestreamwrite/responses.py and test files to fix the issue without changing other files.
  is_positive: true
  type: correctness
  importance: GOOD_TO_HAVE

````

# Rubrics Rating:

Here is a prompt designed for **Step 5: Grade Each Trajectory Against Rubrics** and **Step 6: Assign the Overall Rating (1-5)**, using the generated rubrics and agent trajectories as input.

**LLM Prompt for Grading Trajectories and Assigning Overall Rating**

````
You are an expert Rubric Grader. Your task is to evaluate three provided coding agent trajectories against a set of predetermined rubrics. For each trajectory, you must assign a PASS or FAIL for every rubric and then determine an Overall Rating from 1 to 5 with a supporting rationale.

**Goal:** Generate the required JSON structures for \`\`\`rubrics_rating\`\`\` and \`\`\`overall_rating\`\`\` based on the analysis of the trajectories against the rubrics.

**Grading Rules (from the Guideline):**

1.  **Rubric Grading (Step 5):**
    *   For every rubric and every trajectory, assign a binary grade: **PASS** or **FAIL**.
    *   Base your grade on concrete evidence from the trajectory: the code diffs, agent actions, and test results.

2.  **Overall Rating (Step 6):**
    *   Assign a single score from 1 to 5 for each trajectory.
    *   Your score must reflect the aggregation of the rubric results and your qualitative judgment, according to the scale below.
    *   Provide a brief, clear rationale (1-3 sentences) explaining the rating.

| Score | Meaning |
| :---: | :---: |
| **5** | Perfect fix, no regressions, clean code |
| **4** | Good fix, minor issues |
| **3** | Some mistakes, partial fix |
| **2** | Low quality, multiple MUST_FOLLOW failures |
| **1** | Wrong, harmful, or nonsense solution |

**Input Data (Placeholders to be filled):**

1.  **Rubrics (JSON from Step 3):**
    
2.  **Agent Trajectory 1 (Full Trace):**
    
3.  **Agent Trajectory 2 (Full Trace):**
    
4.  **Agent Trajectory 3 (Full Trace):**
    
**Output Format (Merge \`\`\`overall_rating\`\`\` and \`\`\`rubrics_rating\`\`\`):**

```json
{
  "rubrics_rating": {
    "trace_01": {
      "rubric_01": "PASS",
      "rubric_2": "FAIL",
      // ... all rubrics
    },
    "trace_02": {
      "rubric_01": "...",
      // ... all rubrics
    },
    "trace_03": {
      "rubric_01": "...",
      // ... all rubrics
    }
  },
  "overall_rating": {
    "trace_01": {
"rating": 4,
    "rationale": "A few sentences justifying the rating based on the rubric results and the 1-5 scale."
},
    "trace_02": {
"rating": 3,
    "rationale": "A few sentences justifying the rating based on the rubric results and the 1-5 scale."
},
    "trace_03": {
"rating": 1,
    "rationale": "A few sentences justifying the rating based on the rubric results and the 1-5 scale."
  }
}
Save to a file called ratings.json
````

# Vendor guidelines 2

**Vendor guidelines 2.0**

Table of contents

**[TL;DR (vendors)	1](#tl;dr-\(vendors\))**

[**Step-by-step guidance	2**](#step-by-step-guidance)

[**Delivery schema	5**](#delivery-schema)

[**Pilot instances/tasks	7**](#pilot-instances/tasks)

[Selection of 20	7](#selection-of-20)

[Selection of 197	7](#selection-of-197)

[**Example rubrics	10**](#example-rubrics)

[A. Bug Fixing	10](#a.-bug-fixing)

[B. Feature Development	10](#b.-feature-development)

[C. Unit Test Tasks	11](#c.-unit-test-tasks)

[D. Code Refactoring Tasks	11](#d.-code-refactoring-tasks)

[E. System Optimization	12](#e.-system-optimization)

[**Full examples	13**](#full-examples)

[Example 1	13](#example-1)

[Example 2	15](#example-2)

## **TL;DR (vendors)** {#tl;dr-(vendors)}

- **Goal:** Given a codebase and environment, generate coding agent trajectories using multiple LLMs, then design rubrics and grade each trajectory.  
  - **Inputs**   
    - Guidelines (this document)  
    - [Codebase](https://github.com/SWE-Gym/SWE-Gym)   
      - Pilot 1: Selection of [20 instance/tasks](#selection-of-20)   
      - Pilot 2: Selection of [197 instances/tasks](#selection-of-197)  
    - [Execution environment](https://hub.docker.com/search?q=xingyaoww%2Fsweb.eval.x86_64)  
  - **Outputs**  
    - Golden reference answer (e.g., code patch) if doesn’t exist  
    - Metadata including language, category, difficulty, must\_read\_files and must\_check\_tests  
    - 3 model-generated coding agent trajectories per task (from Qwen, Kimi, Claude, or GPT-5)  
    - Rubrics   
    - Grading of trajectories based on created rubrics

## 

## **Step-by-step guidance** {#step-by-step-guidance}

1. **Check provided inputs**  
2. **Identify a golden reference answer if doesn’t exists**   
3. **Annotate task metadata**  
   1. **Language**: Python, Rust, JavaScript, TypeScript, Java, C++, C  
   2. **Category**: bug fixing, feature development, system optimization, documentation, refactoring   
   3. **Difficulty** based on estimation on human hours for a person who is familiar with the codebase   
      1. 0 \~ 15 min  
      2. 15 min \~ 1 hour  
      3. 1 hour \~ 4 hours  
   4. **Must-read files:** files that the agent must view to fix the issue or implement the new feature. Annotate in a list with absolute path starting with repo work\_idr (e.g., /testbed) \- \[“path\_1”, “path\_2”, “path\_3”, ….\]  
   5. **Must-check tests:** tests that the agent must run to ensure that no regression is introduced. Annotate in a list with absolute path starting with repo work\_idr (e.g., /testbed) \- \[“path\_1”, “path\_2”, “path\_3”, ….\]. This can be either a folder or specific test paths.   
4. **Generate code trajectories**   
   1. Generate code trajectories using the specified LLMs (Qwen, Kimi, Claude, GPT-5).  
   2. Each trajectory should include the sequence of agent actions (tool calls, code edits, etc.) and the resulting code diffs.  
   3. Ensure each trajectory is complete and reproducible in the provided environment.  
5. **Select trajectories for annotation**  
   1. From the generated trajectories, select 3 for annotation and grading.  
   2. Ensure the selected trajectories represent a range of approaches and quality.  
6. **Analyze each trajectory**  
   1. Review the code changes and agent actions.  
   2. Execute the code in the provided environment to verify outcomes.  
   3. Note any issues, strengths, or unique aspects of each trajectory.  
7. **Create task-specific rubrics**  
   1. Design **5–10 high-quality rubrics for the task**, tailored to the codebase and requirements.   
      1. The rubrics should effectively distinguish the provided trajectories and the rank of scores after simple aggregation aligns with the rank of preference among the trajectories. Avoid rubrics that yield perfect ratings for all provided rollouts (in this case we should use harder tasks).  
      2. Quality is more important than quantity.  
      3. The rubrics should be agnostic to harnesses (e.g., tools, etc.)  
      4. Avoid writing rubrics that only apply to one of the possible good solutions. A good rubric should be passable by all feasible solutions.  
      5. If a rubric is to check whether generated unit tests cover certain code paths, concrete code paths need to be listed in the rubric instead of just vague rubric as “the agent needs to cover critical code paths”;  
   2. **Rubrics should be binary**: PASS or FAIL.  
   3. **Each rubric must include**:  
      1. **Criterion**: Clear, specific, and actionable.  
      2. **Type**:  
         1. **Correctness (most important, should be 40-50% of all criteria)**  
            1. Scope: final agent generated code  
            2. Desc: this type of rubrics should indicate whether the solution is correct or not including whether the generated patch fixes the bug, adds the correct unit tests or implements the correct feature.   
         2. **Code style**   
            1. Scope: final agent generated code  
            2. Desc: this type covers code style such as code formats, comments, syntax, etc. Example rubrics can include having proper comments at the place where logic is complex for readability.  
         3. **Summary**  
            1. Scope: final agent summary at the end of a trace  
            2. Desc: this covers the quality of the summary from the agent. The summary should be concise, at point but with necessary details.  
         4. **Agent behavior**   
            1. Scope: trajectory that includes intermediate tool calls  
            2. Desc: this category focuses on judging overall agent behavior (e.g., repo exploration and verification before submitting) other than final agent generated output and summary.  
               1. Examples can be whether the agent has viewed critical files before making an edit (e.g., the implementation of a base class before implementing a new child class) or the agent greps for certain keywords in the codebase.  
               2. Other examples include whether the agent efficiently uses tools (e.g., grep and read for a range precisely instead of viewing multiple times or the whole file) or whether there is a doom loop in the trace.    
         5. **~~Universal~~**   
            1. ~~The agent should try to reproduce the issue before making any edits;~~  
            2. ~~The agent should not hallucinate about code contents;~~  
            3. ~~The agent should not make assumptions about certain logic is correct without testing by executing code;~~   
            4. ~~The agent should add relevant new tests to cover the bugs to be fixed.~~   
      3. **is\_positive**: Indicate positive (SHOULD) or negative (SHOULD NOT) behavior.  
      4. **Importance**: MUST\_FOLLOW, GOOD\_TO\_HAVE, or UNIVERSAL.  
         1. MUST\_FOLLOW and GOOD\_TO\_HAVE rubrics should be repo and codebase specific.   
         2. UNIVERSAL rules are usable to other tasks and should only be provided as a negative criterion when it’s impossible to make it specific to the repo and task. We should avoid universal general criteria as much as we can.   
      5. **Rationale**: Brief explanation of why the rubric matters.  
8. **Grade each trajectory against rubrics**  
   1. Assign PASS or FAIL for each rubric.  
   2. Provide an overall rating (1–5 scale) based on aggregate rubric scores and overall preference.  
      1. 5 \- Perfect  
      2. 4 \- Good  
      3. 3 \- Okay  
      4. 2 \- Low Quality   
      5. 1 \- Bad  
   3. Write a brief rationale explaining the rating.

## 

## **Delivery schema** {#delivery-schema}

```
{
"rubrics": {
	"rubric_1": {
		"criterion": "xxxx",
		"is_positive": "true",
		"type": "correctness",
		"importance": "MUST_FOLLOW",
},
	"rubric_2": {
		"criterion": "yyyy",
		"is_positive": "false",
"type": "agent_behavior",
		"importance": "GOOD_TO_HAVE",
},
	"rubric_3": {
		"criterion": "zzzz",
		"is_positive": "false",
		"type": "summary",
		"importance": "UNIVERSAL",
},
....
},
"overall_rating": {
	"trace_1": 5,
	"rationale_1": "a few sentences",
	"trace_2": 3,
"rationale_2": "a few sentences",
	"trace_3", 2,
	"rationale_3": "a few sentences",
},
"rubrics_rating": {
	"trace_1": {
"rubric_1": "PASS",
"rubric_2": "PASS",
"rubric_3": "FAIL",
},
....
},
"metadata": {
	"language": "javascript",
	"category": "bug_fixing",
	"difficulty": "> 4 hours",
	"must_read_files": [
		"path_1.py",
		"path_2.md",
],
"must_check_tests": [
	"test_path_1.py",
	"test_paht_2.py",
],
},
}
```

## 

## **Pilot instances/tasks** {#pilot-instances/tasks}

### Selection of 20 {#selection-of-20}

\[  
    'Project-MONAI\_\_MONAI-2436',  
    'Project-MONAI\_\_MONAI-4943',  
    'bokeh\_\_bokeh-12867',  
    'bokeh\_\_bokeh-13370',  
    'conan-io\_\_conan-13721',  
    'conan-io\_\_conan-14532',  
    'dask\_\_dask-7092',  
    'dask\_\_dask-10750',  
    'facebookresearch\_\_hydra-1671',  
    'facebookresearch\_\_hydra-1915',  
    'getmoto\_\_moto-5348',  
    'getmoto\_\_moto-6510',  
    'iterative\_\_dvc-1809',  
    'iterative\_\_dvc-3992',  
    'pydantic\_\_pydantic-6043',  
    'pydantic\_\_pydantic-8437',  
    'pydantic\_\_pydantic-9111',  
    'python\_\_mypy-11207',  
    'python\_\_mypy-14064',  
    'python\_\_mypy-16670'  
\]

### Selection of 197 {#selection-of-197}

\['Project-MONAI\_\_MONAI-1116', 'Project-MONAI\_\_MONAI-1684', 'Project-MONAI\_\_MONAI-1946', 'Project-MONAI\_\_MONAI-2061', 'Project-MONAI\_\_MONAI-2178', 'Project-MONAI\_\_MONAI-2436', 'Project-MONAI\_\_MONAI-2553', 'Project-MONAI\_\_MONAI-2696', 'Project-MONAI\_\_MONAI-2955', 'Project-MONAI\_\_MONAI-3107', 'Project-MONAI\_\_MONAI-3125', 'Project-MONAI\_\_MONAI-3143', 'Project-MONAI\_\_MONAI-3358', 'Project-MONAI\_\_MONAI-3393', 'Project-MONAI\_\_MONAI-3690', 'Project-MONAI\_\_MONAI-3711', 'Project-MONAI\_\_MONAI-4736', 'Project-MONAI\_\_MONAI-4943', 'Project-MONAI\_\_MONAI-4972', 'Project-MONAI\_\_MONAI-4991', 'Project-MONAI\_\_MONAI-5129', 'Project-MONAI\_\_MONAI-5182', 'Project-MONAI\_\_MONAI-5223', 'Project-MONAI\_\_MONAI-5248', 'Project-MONAI\_\_MONAI-5416', 'Project-MONAI\_\_MONAI-5856', 'Project-MONAI\_\_MONAI-6147', 'Project-MONAI\_\_MONAI-6405', 'Project-MONAI\_\_MONAI-6446', 'Project-MONAI\_\_MONAI-646', 'Project-MONAI\_\_MONAI-6735', 'Project-MONAI\_\_MONAI-6774', 'Project-MONAI\_\_MONAI-6969', 'Project-MONAI\_\_MONAI-7542', 'bokeh\_\_bokeh-12841', 'bokeh\_\_bokeh-12867', 'bokeh\_\_bokeh-13147', 'bokeh\_\_bokeh-13370', 'bokeh\_\_bokeh-13491', 'conan-io\_\_conan-13230', 'conan-io\_\_conan-13721', 'conan-io\_\_conan-14378', 'conan-io\_\_conan-14532', 'conan-io\_\_conan-16103', 'dask\_\_dask-10149', 'dask\_\_dask-10211', 'dask\_\_dask-10212', 'dask\_\_dask-10422', 'dask\_\_dask-10506', 'dask\_\_dask-10750', 'dask\_\_dask-10846', 'dask\_\_dask-6626', 'dask\_\_dask-6742', 'dask\_\_dask-6749', 'dask\_\_dask-6818', 'dask\_\_dask-6978', 'dask\_\_dask-6992', 'dask\_\_dask-7048', 'dask\_\_dask-7056', 'dask\_\_dask-7092', 'dask\_\_dask-7125', 'dask\_\_dask-7145', 'dask\_\_dask-7230', 'dask\_\_dask-8040', 'dask\_\_dask-8685', 'dask\_\_dask-8687', 'dask\_\_dask-8805', 'dask\_\_dask-8820', 'dask\_\_dask-8860', 'dask\_\_dask-8925', 'dask\_\_dask-9240', 'dask\_\_dask-9250', 'dask\_\_dask-9528', 'dask\_\_dask-9653', 'facebookresearch\_\_hydra-1404', 'facebookresearch\_\_hydra-1671', 'facebookresearch\_\_hydra-1735', 'facebookresearch\_\_hydra-1783', 'facebookresearch\_\_hydra-1915', 'facebookresearch\_\_hydra-2062', 'getmoto\_\_moto-4799', 'getmoto\_\_moto-4833', 'getmoto\_\_moto-4896', 'getmoto\_\_moto-4950', 'getmoto\_\_moto-4951', 'getmoto\_\_moto-5124', 'getmoto\_\_moto-5136', 'getmoto\_\_moto-5164', 'getmoto\_\_moto-5347', 'getmoto\_\_moto-5348', 'getmoto\_\_moto-5384', 'getmoto\_\_moto-5620', 'getmoto\_\_moto-5718', 'getmoto\_\_moto-5725', 'getmoto\_\_moto-5745', 'getmoto\_\_moto-5837', 'getmoto\_\_moto-5843', 'getmoto\_\_moto-5862', 'getmoto\_\_moto-5885', 'getmoto\_\_moto-5968', 'getmoto\_\_moto-5991', 'getmoto\_\_moto-6082', 'getmoto\_\_moto-6159', 'getmoto\_\_moto-6185', 'getmoto\_\_moto-6226', 'getmoto\_\_moto-6408', 'getmoto\_\_moto-6469', 'getmoto\_\_moto-6510', 'getmoto\_\_moto-6637', 'getmoto\_\_moto-6641', 'getmoto\_\_moto-6736', 'getmoto\_\_moto-6743', 'getmoto\_\_moto-6746', 'getmoto\_\_moto-6784', 'getmoto\_\_moto-6828', 'getmoto\_\_moto-6885', 'getmoto\_\_moto-6920', 'getmoto\_\_moto-7012', 'getmoto\_\_moto-7029', 'getmoto\_\_moto-7081', 'getmoto\_\_moto-7085', 'getmoto\_\_moto-7102', 'getmoto\_\_moto-7212', 'getmoto\_\_moto-7273', 'getmoto\_\_moto-7317', 'getmoto\_\_moto-7328', 'getmoto\_\_moto-7331', 'getmoto\_\_moto-7335', 'getmoto\_\_moto-7390', 'getmoto\_\_moto-7434', 'getmoto\_\_moto-7524', 'getmoto\_\_moto-7567', 'getmoto\_\_moto-7580', 'getmoto\_\_moto-7635', 'iterative\_\_dvc-1661', 'iterative\_\_dvc-1684', 'iterative\_\_dvc-1781', 'iterative\_\_dvc-1785', 'iterative\_\_dvc-1809', 'iterative\_\_dvc-1829', 'iterative\_\_dvc-1841', 'iterative\_\_dvc-1942', 'iterative\_\_dvc-1944', 'iterative\_\_dvc-1992', 'iterative\_\_dvc-2231', 'iterative\_\_dvc-2254', 'iterative\_\_dvc-3524', 'iterative\_\_dvc-3727', 'iterative\_\_dvc-3992', 'iterative\_\_dvc-4005', 'iterative\_\_dvc-4034', 'iterative\_\_dvc-4166', 'iterative\_\_dvc-4309', 'iterative\_\_dvc-4323', 'iterative\_\_dvc-4613', 'iterative\_\_dvc-4785', 'iterative\_\_dvc-4961', 'iterative\_\_dvc-5004', 'iterative\_\_dvc-5160', 'iterative\_\_dvc-6519', 'iterative\_\_dvc-6799', 'iterative\_\_dvc-9646', 'pydantic\_\_pydantic-4911', 'pydantic\_\_pydantic-5624', 'pydantic\_\_pydantic-6043', 'pydantic\_\_pydantic-6212', 'pydantic\_\_pydantic-6283', 'pydantic\_\_pydantic-8352', 'pydantic\_\_pydantic-8437', 'pydantic\_\_pydantic-8511', 'pydantic\_\_pydantic-8965', 'pydantic\_\_pydantic-9082', 'pydantic\_\_pydantic-9111', 'pydantic\_\_pydantic-9193', 'python\_\_mypy-10154', 'python\_\_mypy-10430', 'python\_\_mypy-10458', 'python\_\_mypy-11207', 'python\_\_mypy-11213', 'python\_\_mypy-11220', 'python\_\_mypy-11292', 'python\_\_mypy-11329', 'python\_\_mypy-11420', 'python\_\_mypy-11717', 'python\_\_mypy-12741', 'python\_\_mypy-14064', 'python\_\_mypy-14178', 'python\_\_mypy-14739', 'python\_\_mypy-15045', 'python\_\_mypy-15208', 'python\_\_mypy-15490', 'python\_\_mypy-15976', 'python\_\_mypy-15996', 'python\_\_mypy-16670', 'python\_\_mypy-16966', 'python\_\_mypy-9454', 'python\_\_mypy-9663'\]

## 

## **Example rubrics** {#example-rubrics}

**Note: Rubrics must be specifically tailored to the actual codebase and task \- the demonstration below is mainly for inspiration.** 

### A. Bug Fixing {#a.-bug-fixing}

Positive Criteria:

* \[agent behavior\] Reproduces the bug \- steps to reproduce are clear and complete  
  * Showing the exact error message in repro as shown in the original issue  
* \[summary\] Identifies root cause \- correctly diagnoses the underlying issue  
  * Explain clearly in the summary about the root cause  
* \[correctness\] Implements effective fix \- Solution addresses the root cause and resolves the bug  
  * The bug and certain edge cases need to be fixed  
* \[agent behavior\] Updates/adds relevant tests \- Tests are updated or added to cover the bug and prevent recurrence  
* \[code style\] Clear documentation \- Fix and reasoning are documented for future maintainers

Negative Criteria:

* \[correctness\] Misses root cause \- Fix does not address the actual underlying issue  
  * Can list certain tricky root causes that are hard to identify   
* \[correctness\] Introduces new issues \- The fix causes new bugs or breaks existing functionality  
  * Can list out certain regression that agents made while fixing the issue

### B. Feature Development {#b.-feature-development}

Positive Criteria:

* \[agent behavior\] Clarifies requirements \- Feature requirements are fully understood and documented  
* \[summary\] Design soundness \- Solution is well-architected, maintainable, and scalable  
* \[correctness\] Implements feature correctly \- Feature works as intended and meets all requirements  
  * List out certain requirements and provide a way for verification if possible  
* \[agent behavior\] Comprehensive testing \- All new functionality is thoroughly tested  
* \[code style\]  Clear documentation \- Feature and design decisions are documented

Negative Criteria:

* \[correctness\] Misses requirements \- Feature does not meet stated requirements  
  * If certain requirements are hard to meet (missed by reference agents)  
* \[correctness\] Breaks existing functionality \- Feature causes regressions or breaks other parts of the system  
  * List out certain functionality that the new feature may break

### C. Unit Test Tasks {#c.-unit-test-tasks}

Positive Criteria:

* \[correctness\] Test Coverage Completeness: All critical code paths are tested  
  * Provide critical code paths in rubrics  
* \[correctness\] Edge Case Handling: Tests include boundary conditions and error scenarios  
  * Provide concrete edge cases in rubrics  
* \[correctness\] Assertion Accuracy: Test assertions correctly validate expected behavior  
  * Provide descriptions of the behaviors  in rubrics  
* \[code style\] Test Organization: Clear structure and naming conventions  
  * Certain tests are written in specific files   
* \[code style\] Mock Usage: Appropriate use of mocks and stubs where needed  
* \[correctness\] Performance Considerations: Tests execute efficiently  
* \[code style\] Documentation Quality: Clear test descriptions and comments  
* \[code style\] Maintainability: Tests are easy to update as code evolves

Negative Criteria:

* \[correctness\] Flaky Tests: Tests that fail intermittently  
  * If certain tests can be flaky, list it out and label in criteria that it should be executed multiple times  
* \[code style\] Over-Testing: Excessive testing of trivial functionality

### D. Code Refactoring Tasks {#d.-code-refactoring-tasks}

Positive Criteria:

* \[correctness\] Functional Preservation: Refactored code maintains original functionality  
* \[code style\] Code Quality Improvement: Measurable improvement in readability/maintainability  
* Performance Impact: Refactoring doesn't degrade performance  
* \[code style\] Variable/Method Naming: Clear, descriptive identifiers  
* \[code style\] Code Style Consistency: Adherence to project style guidelines  
* \[code style\] Comment Quality: Improved or maintained documentation

Negative Criteria

* \[correctness\] Scope Creep:   
  * Unnecessary changes beyond refactoring scope  
  * Unnecessary complexity added  
* \[correctness\] Regression Introduction: New bugs introduced during refactoring

### E. System Optimization {#e.-system-optimization}

Positive Criteria:

* \[correctness\] Diagnoses bottlenecks \- Correctly identifies key performance issues  
* \[correctness\] Implements effective optimization \- Chosen optimizations yield measurable improvements  
* \[summary\] Reports before/after metrics \- Performance metrics are clearly documented before and after optimization  
* \[correctness\]  Maintains stability \- No regressions or instability introduced  
* \[code style\] Clear documentation \- Optimization steps and rationale are documented

Negative Criteria:

* \[correctness\] Misses bottleneck \- Optimization does not address the actual performance issue  
* \[correctness\] Degrades system stability \- Optimization causes instability or regressions

## 

## **Full examples** {#full-examples}

### Example 1 {#example-1}

Traces not shown here.   
The problem is getmoto\_\_moto-4950 from the SWE-GYM dataset.

```json
{
	"metadata": {
	"language": "python",
	"category": "bug_fixing",
	"difficulty": "15 min~1 hour",
"must_read_files": [
		"/testbed/moto/timestreamwrite/responses.py",
		"/testbed/moto/timestreamwrite/models.py",
],
"must_check_tests": [
	"/testbed/tests/test_timestreamwrite/",
"/testbed/tests/test_timestreamwrite/test_timestreamwrite_table.py",
"/testbed/tests/test_timestreamwrite/test_timestreamwrite_database.py",
],
},
"rubrics": {
	"rubric_1": {
		"criterion": "The agent should reproduce the issue before making any edits to fix the issue. In the repro script, it should show the KeyError of RecordsIngested not being in the response.",
		"is_positive": "true",
"type": "agent_behavior",
		"importance": "MUST_FOLLOW",
},
	"rubric_2": {
		"criterion": "In the final patch, the agent should not assign 0 value to "MagneticStore" without any explanation or comments.",
		"is_positive": "false",
		"type": "code_style",
		"importance": "MUST_FOLLOW",
},
	"rubric_3": {
		"criterion": "The agent should add an additional test to cover the original issue in which different keys including RecordsIngested, Total, MemoryStore and MagneticStore should be checked as per the AWS specification.",
		"is_positive": "true",
		"type": "agent_behavior",
		"importance": "MUST_FOLLOW",
},
	"rubric_4": {
		"criterion": "The agent should not run existing tests or the new tests more than 3 times as the difficulty is on the easier end.",
		"is_positive": "false",
		"type": "agent_behavior",
		"importance": "GOOD_TO_HAVE",
},
"rubric_5": {
		"criterion": "The agent should only edit moto/timestreamwrite/responses.py and test files to fix the issue without changing other files.",
		"is_positive": "true",
		"type": "correctness",
		"importance": "GOOD_TO_HAVE",
},
},
"overall_rating": {
	"trace_1": 4,
	"rational_1": “a few sentences to justify”,
	"trace_2": 5,
"rational_2": “a few sentences to justify”,
	"trace_3": 3,
"rational_3": “a few sentences to justify”,
"trace_4": 4,
"rational_4": “a few sentences to justify”,
},
"rubrics_rating": {
	"trace_1": {
"rubric_1": "PASS",
"rubric_2": "PASS",
"rubric_3": "PASS",
"rubric_4": "FAIL",
"rubric_5": "FAIL",
},
	"trace_2": {
"rubric_1": "PASS",
"rubric_2": "PASS",
"rubric_3": "PASS",
"rubric_4": "PASS",
"rubric_5": "FAIL",
},
	"trace_3": {
"rubric_1": "PASS",
"rubric_2": "FAIL",
"rubric_3": "FAIL",
"rubric_4": "FAIL",
"rubric_5": "FAIL",
},
"trace_4": {
"rubric_1": "PASS",
"rubric_2": "FAIL",
"rubric_3": "FAIL",
"rubric_4": "PASS",
"rubric_5": "FAIL",
},
},
}

```

### Example 2 {#example-2}

Traces not shown here.   
The problem is getmoto\_\_moto-5212 from the SWE-GYM dataset.

```json
{
"metadata": {
        "language": "python",
        "category": "bug_fixing",
        "difficulty": "1 hour ~ 4 hours",
  "must_read_files": [
		"/testbed/moto/a.py",
		"/testbed/moto/b.py",
  ],
  "must_check_tests": [
"/testbed/moto/test_xx/test_subnets.py",
		"/testbed/moto/test_xx/test_vpcs.py",
  ],
 }
"rubrics": {
"rubric_1": {
"criterion": "The solution modifies the create_vpc method in vpcs.py to ensure it never create a default VPC, regardless of existing VPCs.",
"is_positive": "true",
"type": "correctness",
 	"importance": "MUST_FOLLOW"
},
"rubric_2": {
"criterion": "In the solution, the EC2Backend initialization in init.py is updated to create an initial default VPC with CIDR '172.31.0.0/16' and is_default=True",
"is_positive": "true",
       "type": "correctness",
       "importance": "MUST_FOLLOW"
},
"rubric_3": {
       "criterion": "Any iteration over self.vpcs.values() in init.py is corrected for Python 3 compatibility, avoiding deprecated methods like .values()[0] to access the first VPC safely.",
       "is_positive": "true",
       "type": "code_style",
       "importance": "MUST_FOLLOW"
},
"rubric_4": {
        "criterion": "The solution implements a separate mechanism (e.g., new create_default_vpc method or inline logic) for default VPC creation that is distinct from the general create_vpc call.",
        "is_positive": "true",
        "type": "code_style",
        "importance": "GOOD_TO_FOLLOW"
},
"rubric_5": {
         "criterion": "A response handler for the CreateDefaultVpc API action is added in responses/vpcs.py, correctly delegating to the backend's default VPC creation logic to support AWS API.",
         "is_positive": "true",
         "type": "correctness",
         "importance": "GOOD_TO_FOLLOW"
},
"rubric_6": {
         "criterion": "Default VPC creation includes provisioning of AWS-standard associated resources: a main route table (via create_route_table with main=True) and a default network ACL (via create_network_acl with default=True).",
         "is_positive": "true",
         "type": "correctness",
         "importance": "GOOD_TO_FOLLOW"
},
"rubric_7": {
           "criterion": "The default VPC creation does not introduce non-standard elements, such as custom tags (e.g., Name='Default VPC'), IPv6 CIDR blocks, or invalid CIDR validation that deviates from AWS defaults.",
           "is_positive": "false",
           "type": "code_style",
           "importance": "GOOD_TO_FOLLOW"
},
"rubric_8": {
           "criterion": "The agent creates and executes a reproduction script matching the issue's repro code to verify the bug before changes, confirms the fix post-implementation, and removes the script prior to submission.",
           "is_positive": "true",
           "type": "agent_behavior",
           "importance": "MUST_FOLLOW"
},
"rubric_9": {
           "criterion": "The agent runs pytest on relevant test suites (e.g., test_vpcs.py and test_subnets.py, targeting key tests like test_default_vpc, test_non_default_vpc, and test_default_subnet) to validate no regressions.",
           "is_positive": "true",
           "type": "agent_behavior",
           "importance": "GOOD_TO_FOLLOW"
},
"rubric_10": {
            "criterion": "The final summary concisely details modified files, core changes (e.g., is_default fix, initialization update), verification outcomes (e.g., repro and tests pass), and AWS compliance, avoiding irrelevant details like unrelated warnings.",
            "is_positive": "true",
            "type": "summary",
            "importance": "MUST_FOLLOW"
}
},
"overall_rating": {
"trace_1": 5,
"rational_1": “a few sentences to justify”,
       "trace_2": 4,
"rational_2": “a few sentences to justify”,
       "trace_3": 3,
"rational_3": “a few sentences to justify”,
       "trace_4": 2,
"rational_4": “a few sentences to justify”,

},
    "rating": {
        "trace_1": {
            "rubric_1": "PASS",
            "rubric_2": "PASS",
            "rubric_3": "PASS",
            "rubric_4": "PASS",
            "rubric_5": "PASS",
            "rubric_6": "PASS",
            "rubric_7": "PASS",
            "rubric_8": "PASS",
            "rubric_9": "PASS",
            "rubric_10": "PASS"
        },
        "trace_2": {
            "rubric_1": "PASS",
            "rubric_2": "PASS",
            "rubric_3": "PASS",
            "rubric_4": "PASS",
            "rubric_5": "FAIL",
            "rubric_6": "PASS",
            "rubric_7": "PASS",
            "rubric_8": "PASS",
            "rubric_9": "PASS",
            "rubric_10": "PASS"
        },
        "trace_3": {
            "rubric_1": "PASS",
            "rubric_2": "PASS",
            "rubric_3": "FAIL",
            "rubric_4": "FAIL",
            "rubric_5": "FAIL",
            "rubric_6": "FAIL",
            "rubric_7": "PASS",
            "rubric_8": "PASS",
            "rubric_9": "PASS",
            "rubric_10": "PASS"
        },
        "trace_4": {
            "rubric_1": "PASS",
            "rubric_2": "PASS",
            "rubric_3": "FAIL",
            "rubric_4": "PASS",
            "rubric_5": "FAIL",
            "rubric_6": "PASS",
            "rubric_7": "FAIL",
            "rubric_8": "PASS",
            "rubric_9": "PASS",
            "rubric_10": "PASS"
        }
    },
}

```

