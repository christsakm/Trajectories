# Task Analysis: getmoto__moto-5843

## Overview

**Problem Statement:**
Moto (AWS mock library for testing) fails to validate that Global Secondary Index (GSI) key attributes cannot be NULL when using `put_item`. Real AWS DynamoDB throws a ValidationException when attempting to set a GSI key attribute to NULL, but Moto allows it, creating inconsistent behavior between tests and production.

**Golden Patch Summary:**
The golden patch adds validation in `responses.py` that checks if any GSI key attribute is NULL during put_item operations. Key changes:
- Adds type hints to `get_table()` (returns Table) and `get_empty_keys_on_put()` in models/__init__.py
- Imports Table class in responses.py
- Creates `validate_put_has_gsi_keys_set_to_none()` function in responses.py that iterates through GSI schemas and checks for NULL values
- Calls this validation in put_item() method before the actual item is stored
- Raises MockValidationException with format: "Type mismatch for Index Key {attr} Expected: S Actual: NULL IndexName: {index}"

**Files Changed in Golden Patch:**
- `/testbed/moto/dynamodb/models/__init__.py` (type hints only)
- `/testbed/moto/dynamodb/responses.py` (validation logic)

## Analysis of All 4 Traces

### trace_01_gpt-5-2025-08-07

**Approach:**
Agent implemented validation in the Table class (models/__init__.py) rather than in responses.py. Created a custom exception class and added validation for both GSI and LSI with general type checking.

**Code Changes:**
- Created `InvalidIndexKeyTypeError` exception class in exceptions.py
- Implemented `_validate_index_key_types()` method in Table class
- Validates both GSI and LSI (local secondary indexes)
- Checks for both NULL and general type mismatches
- Added 2 reproduction test files (repro_index_type_validation.py and repro_index_type_validation_success.py)

**Evidence from traj_search.py:**
- ✅ Resolved: true
- ✅ FAIL_TO_PASS: 1 passed, 0 failed
- ✅ PASS_TO_PASS: 32 passed, 0 failed
- Steps: 38
- Files modified: 4 (including 2 test files not in golden)
- Viewed responses.py but chose models/__init__.py implementation

**Key Findings:**
- Functional solution that passes all tests
- Wrong architectural location (models vs responses)
- Added unnecessary custom exception class
- Broader scope (includes LSI validation and general type checking)
- Added test files not required by golden patch

### trace_02_kimi-k2-instruct-0905

**Approach:**
Agent implemented validation in the Table class using `all_indexes()` helper method. Handles None values explicitly and checks for type mismatches.

**Code Changes:**
- Implemented `_validate_index_attributes()` method in Table class
- Uses `all_indexes()` to get both GSI and LSI
- Explicitly handles None values with proper error message
- Also validates general type mismatches beyond NULL
- Modified only models/__init__.py

**Evidence from traj_search.py:**
- ✅ Resolved: true
- ✅ FAIL_TO_PASS: 1 passed, 0 failed
- ✅ PASS_TO_PASS: 32 passed, 0 failed
- Steps: 35
- Files modified: 1 (cleanest patch)
- Viewed responses.py but implemented in models/__init__.py
- Many files created/modified for testing (reproduce.py with 8 modifications)

**Key Findings:**
- Clean, functional solution that passes all tests
- Wrong architectural location (models vs responses)
- No unnecessary exception classes
- Validates both GSI and LSI (broader than golden)
- Includes type mismatch checking beyond NULL

### trace_03_qwen3-coder-480b-a35b-instruct

**Approach:**
Agent implemented focused validation specifically for GSI NULL values in the Table class. Most similar scope to golden patch but wrong location.

**Code Changes:**
- Implemented `_validate_global_index_key_attributes()` method in Table class
- Only checks GSI (matches golden scope)
- Specifically checks for NULL type
- Smallest code change (+22 lines)
- Modified only models/__init__.py

**Evidence from traj_search.py:**
- ✅ Resolved: true
- ✅ FAIL_TO_PASS: 1 passed, 0 failed
- ✅ PASS_TO_PASS: 32 passed, 0 failed
- Steps: 57
- Files modified: 1 in patch
- Ran 7 tests during development
- Viewed responses.py but implemented in models/__init__.py
- Created several test files during debugging

**Key Findings:**
- Functional solution with narrowest scope matching golden intent
- Wrong architectural location (models vs responses)
- No custom exception classes
- Only validates GSI (matches golden)
- Most concise implementation

### trace_04_claude-sonnet-4-20250514

**Approach:**
Agent implemented comprehensive validation in the Table class with custom exception class. Validates both NULL and general type mismatches for GSI only.

**Code Changes:**
- Created `InvalidIndexKeyTypeError` exception class in exceptions.py
- Imported exception in models/__init__.py
- Implemented `_validate_global_index_keys()` method in Table class
- Only checks GSI (matches golden scope)
- Validates both NULL and type mismatches
- Modified 2 files: exceptions.py and models/__init__.py

**Evidence from traj_search.py:**
- ✅ Resolved: true
- ✅ FAIL_TO_PASS: 1 passed, 0 failed
- ✅ PASS_TO_PASS: 32 passed, 0 failed
- Steps: 69 (most thorough)
- Files modified: 2 in patch
- Ran 10 tests during development
- Viewed responses.py but implemented in models/__init__.py
- Created many test files for edge cases

**Key Findings:**
- Functional solution with thorough testing
- Wrong architectural location (models vs responses)
- Added unnecessary custom exception class
- Only validates GSI (matches golden scope)
- Includes comprehensive type validation beyond NULL

## Evaluation

### Metadata

```
Language *
Python

Category *
bug fixing

Difficulty *
15 min ~ 1 hour

Must-read files *
["/testbed/moto/dynamodb/responses.py", "/testbed/moto/dynamodb/models/__init__.py"]

Must-check tests *
["/testbed/tests/test_dynamodb/exceptions/test_dynamodb_exceptions.py"]
```

### Rubrics

```json
{
  "rubric_01": {
    "criterion": "The patch validates GSI key attributes for NULL values in put_item.",
    "rationale": "Core requirement to match AWS behavior rejecting NULL GSI keys.",
    "type": "correctness",
    "importance": "MUST_FOLLOW",
    "is_positive": "true"
  },
  "rubric_02": {
    "criterion": "MockValidationException includes attribute name and index name in error message.",
    "rationale": "Error message must match AWS format for test compatibility.",
    "type": "correctness",
    "importance": "MUST_FOLLOW",
    "is_positive": "true"
  },
  "rubric_03": {
    "criterion": "The validation function is implemented in responses.py not models/__init__.py.",
    "rationale": "Architecture places validation at API layer where put_item is handled.",
    "type": "correctness",
    "importance": "MUST_FOLLOW",
    "is_positive": "true"
  },
  "rubric_04": {
    "criterion": "The patch imports Table class in responses.py for type hints.",
    "rationale": "Required for type annotations in validation function and helper functions.",
    "type": "correctness",
    "importance": "MUST_FOLLOW",
    "is_positive": "true"
  },
  "rubric_05": {
    "criterion": "Type hint added to get_table method signature returning Table type.",
    "rationale": "Improves code maintainability and enables type checking in responses.py.",
    "type": "code style",
    "importance": "MUST_FOLLOW",
    "is_positive": "true"
  },
  "rubric_06": {
    "criterion": "Type hint added to get_empty_keys_on_put with table parameter as Table.",
    "rationale": "Consistent type annotations across validation helper functions in responses.py.",
    "type": "code style",
    "importance": "GOOD_TO_HAVE",
    "is_positive": "true"
  },
  "rubric_07": {
    "criterion": "No custom exception class created specifically for this validation.",
    "rationale": "Golden uses existing MockValidationException keeping code simple and maintainable.",
    "type": "code style",
    "importance": "GOOD_TO_HAVE",
    "is_positive": "false"
  },
  "rubric_08": {
    "criterion": "Agent does not add test files outside official test directory.",
    "rationale": "Test additions belong in test_dynamodb_exceptions.py not as standalone scripts.",
    "type": "agent behavior",
    "importance": "GOOD_TO_HAVE",
    "is_positive": "false"
  },
  "rubric_09": {
    "criterion": "Validation only checks for NULL not general type mismatches.",
    "rationale": "Golden scope is specific to NULL validation for GSI keys.",
    "type": "correctness",
    "importance": "GOOD_TO_HAVE",
    "is_positive": "true"
  },
  "rubric_10": {
    "criterion": "Validation only applies to GSI not LSI local secondary indexes.",
    "rationale": "Issue specifically about global indexes not local secondary indexes.",
    "type": "summary",
    "importance": "GOOD_TO_HAVE",
    "is_positive": "true"
  }
}
```

### Rubrics Rating

```json
{
  "trace_01": {
    "rubric_01": "PASS",
    "rubric_02": "PASS",
    "rubric_03": "FAIL",
    "rubric_04": "FAIL",
    "rubric_05": "FAIL",
    "rubric_06": "FAIL",
    "rubric_07": "FAIL",
    "rubric_08": "FAIL",
    "rubric_09": "FAIL",
    "rubric_10": "FAIL"
  },
  "trace_02": {
    "rubric_01": "PASS",
    "rubric_02": "PASS",
    "rubric_03": "FAIL",
    "rubric_04": "FAIL",
    "rubric_05": "FAIL",
    "rubric_06": "FAIL",
    "rubric_07": "PASS",
    "rubric_08": "PASS",
    "rubric_09": "FAIL",
    "rubric_10": "FAIL"
  },
  "trace_03": {
    "rubric_01": "PASS",
    "rubric_02": "PASS",
    "rubric_03": "FAIL",
    "rubric_04": "FAIL",
    "rubric_05": "FAIL",
    "rubric_06": "FAIL",
    "rubric_07": "PASS",
    "rubric_08": "PASS",
    "rubric_09": "PASS",
    "rubric_10": "PASS"
  },
  "trace_04": {
    "rubric_01": "PASS",
    "rubric_02": "PASS",
    "rubric_03": "FAIL",
    "rubric_04": "FAIL",
    "rubric_05": "FAIL",
    "rubric_06": "FAIL",
    "rubric_07": "FAIL",
    "rubric_08": "PASS",
    "rubric_09": "FAIL",
    "rubric_10": "PASS"
  }
}
```

### Overall Rating

```json
{
  "trace_01": {
    "rating": 2,
    "rationale": "Functional solution that passes all tests but with wrong architectural placement in models instead of responses.py. Missing all type hints required by golden patch and created unnecessary custom exception class InvalidIndexKeyTypeError. Added reproduction test files outside official test directory. Validates both GSI and LSI with general type checking instead of focused NULL validation for GSI. Failed 5 MUST_FOLLOW rubrics."
  },
  "trace_02": {
    "rating": 3,
    "rationale": "Clean functional solution with resolved true and all tests passing. However, implemented validation in models/__init__.py instead of responses.py missing the architectural intent. Missing all type hints and Table import in responses.py. Validates both GSI and LSI with general type mismatches rather than focused NULL check. Good coding practices with no custom exceptions or test files. Failed 4 MUST_FOLLOW rubrics."
  },
  "trace_03": {
    "rating": 3,
    "rationale": "Functional solution with narrowest scope matching golden intent for GSI NULL validation only. Implemented in models/__init__.py instead of responses.py missing architectural requirement. No type hints added to get_table or get_empty_keys_on_put. No Table import in responses.py. Clean implementation without custom exceptions or extra test files. Most concise change at +22 lines. Failed 4 MUST_FOLLOW rubrics."
  },
  "trace_04": {
    "rating": 2,
    "rationale": "Thorough functional solution with comprehensive testing but wrong architectural location in models/__init__.py instead of responses.py. Missing all type hints and Table import in responses.py. Created unnecessary InvalidIndexKeyTypeError exception class. Validates type mismatches beyond NULL requirement though correctly scopes to GSI only. Took 69 steps with extensive testing. Failed 5 MUST_FOLLOW rubrics."
  }
}
```
