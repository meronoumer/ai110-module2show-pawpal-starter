# PawPal+ Testing Guide

## Running Tests

To run all tests for the PawPal+ scheduling system:

```bash
python -m pytest tests/test_pawpal.py -v
```

For more detailed output with print statements:

```bash
python -m pytest tests/test_pawpal.py -v -s
```

To run tests with coverage information:

```bash
python -m pytest tests/test_pawpal.py --cov=pawpal_system
```

---

## Test Coverage Overview

The test suite provides comprehensive coverage of the PawPal+ system with **25+ test cases** organized into the following categories:

### 1. **Core Class Tests**

#### TestPet
- ✅ **test_pet_creation**: Verifies Pet instance creation with all required attributes
- ✅ **test_pet_methods_exist**: Confirms all Pet methods are implemented

#### TestOwner
- ✅ **test_owner_creation**: Tests Owner instantiation and default values
- ✅ **test_owner_with_pets**: Verifies pet list management
- ✅ **test_owner_methods_exist**: Ensures all Owner methods exist

#### TestActivity
- ✅ **test_activity_creation**: Validates Activity initialization
- ✅ **test_activity_methods_exist**: Checks method availability

#### TestWalk, TestVetVisit, TestFeeding
- ✅ **test_*_inheritance**: Confirms proper inheritance from Activity class
- ✅ **test_*_methods_exist**: Validates subclass-specific methods

#### TestTaskList
- ✅ **test_task_list_creation**: Tests TaskList initialization
- ✅ **test_task_list_methods_exist**: Verifies all task list methods

---

### 2. **Advanced Scheduling Tests** (TestAdvancedScheduling)

#### Priority-Based Sorting
- ✅ **test_priority_field_exists**: Confirms priority attribute exists with default value
- ✅ **test_priority_sorting**: Verifies tasks sort by priority (high→low) then by time

#### Time Calculations
- ✅ **test_get_end_time**: Validates end time calculation for activities with duration

#### Conflict Detection - Overlapping Tasks
- ✅ **test_conflict_detection_overlapping_tasks**: Detects when tasks overlap in time
- ✅ **test_conflict_detection_no_conflicts**: Confirms non-overlapping tasks pass
- ✅ **test_conflict_detection_different_dates**: Ensures different dates don't conflict

#### Time Budget Tracking
- ✅ **test_get_total_duration**: Calculates total scheduled time across all tasks
- ✅ **test_get_pending_duration**: Sums duration of only incomplete tasks

#### Status Filtering
- ✅ **test_get_tasks_by_status**: Filters tasks by status (Pending, Completed, Skipped)

#### Recurring Task Generation
- ✅ **test_recurring_daily_task_generation**: Creates daily recurring instances
- ✅ **test_recurring_weekly_task_generation**: Creates weekly recurring instances

#### Pet-Based Filtering
- ✅ **test_filter_by_pet_with_multiple_pets**: Isolates tasks by specific pet
- ✅ **test_activity_get_details_with_priority_and_recurrence**: Validates detail formatting

---

## Test Data Patterns

### Common Test Scenarios

1. **Single Pet, Multiple Tasks**: Tests with one pet and various activities
2. **Multiple Pets**: Tests with 3+ pets to ensure filtering accuracy
3. **Same-Day Tasks**: Multiple tasks on `date.today()`
4. **Cross-Day Tasks**: Activities spanning different dates
5. **Status Variations**: Mix of Pending, Completed, and Skipped tasks
6. **Priority Levels**: Low (1), Medium (2), High (3) priority combinations

### Time Ranges Used

- **Morning (8:00 AM)**: Feeding, walks
- **Midday (2:00 PM)**: Vet visits, playtime
- **Evening (6:00 PM)**: Exercise, training
- **Duration**: 10-60 minutes per activity

---

## What Each Test Category Validates

| Category | Purpose | Key Assertions |
|----------|---------|-----------------|
| **Core Classes** | Data model integrity | Attributes, inheritance, method existence |
| **Sorting** | Schedule organization | Correct order by priority then time |
| **Conflicts** | Schedule feasibility | Overlapping detection, same-date validation |
| **Time Budget** | Owner capacity | Total/pending duration calculations |
| **Filtering** | Data access | Pet-based and status-based filtering |
| **Recurrence** | Task automation | Daily/weekly instance generation |

---

## Example Test Run Output

```
====== test session starts ======
tests/test_pawpal.py::TestPet::test_pet_creation PASSED
tests/test_pawpal.py::TestPet::test_pet_methods_exist PASSED
tests/test_pawpal.py::TestOwner::test_owner_creation PASSED
tests/test_pawpal.py::TestOwner::test_owner_with_pets PASSED
tests/test_pawpal.py::TestOwner::test_owner_methods_exist PASSED
tests/test_pawpal.py::TestActivity::test_activity_creation PASSED
tests/test_pawpal.py::TestActivity::test_activity_methods_exist PASSED
tests/test_pawpal.py::TestWalk::test_walk_inheritance PASSED
tests/test_pawpal.py::TestWalk::test_walk_methods_exist PASSED
tests/test_pawpal.py::TestVetVisit::test_vet_visit_inheritance PASSED
tests/test_pawpal.py::TestVetVisit::test_vet_visit_methods_exist PASSED
tests/test_pawpal.py::TestFeeding::test_feeding_inheritance PASSED
tests/test_pawpal.py::TestFeeding::test_feeding_methods_exist PASSED
tests/test_pawpal.py::TestTaskList::test_task_list_creation PASSED
tests/test_pawpal.py::TestTaskList::test_task_list_methods_exist PASSED
tests/test_pawpal.py::TestAdvancedScheduling::test_priority_field_exists PASSED
tests/test_pawpal.py::TestAdvancedScheduling::test_recurrence_field_exists PASSED
tests/test_pawpal.py::TestAdvancedScheduling::test_priority_sorting PASSED
tests/test_pawpal.py::TestAdvancedScheduling::test_get_end_time PASSED
tests/test_pawpal.py::TestAdvancedScheduling::test_conflict_detection_overlapping_tasks PASSED
tests/test_pawpal.py::TestAdvancedScheduling::test_conflict_detection_no_conflicts PASSED
tests/test_pawpal.py::TestAdvancedScheduling::test_conflict_detection_different_dates PASSED
tests/test_pawpal.py::TestAdvancedScheduling::test_get_total_duration PASSED
tests/test_pawpal.py::TestAdvancedScheduling::test_get_pending_duration PASSED
tests/test_pawpal.py::TestAdvancedScheduling::test_get_tasks_by_status PASSED
tests/test_pawpal.py::TestAdvancedScheduling::test_recurring_daily_task_generation PASSED
tests/test_pawpal.py::TestAdvancedScheduling::test_recurring_weekly_task_generation PASSED
tests/test_pawpal.py::TestAdvancedScheduling::test_filter_by_pet_with_multiple_pets PASSED
tests/test_pawpal.py::TestAdvancedScheduling::test_activity_get_details_with_priority_and_recurrence PASSED

====== 29 passed in 0.35s ======
```

---

## Test Files

- **`tests/test_pawpal.py`**: Main unit test suite for all classes and methods
- **`demo_scheduling.py`**: Interactive demo showing all features in action
- **`main.py`**: Comprehensive example with sorting, filtering, and conflict detection

---

## Quick Test Checklist

Before committing code, run:

```bash
# Run all tests
python -m pytest tests/test_pawpal.py -v

# Run demo to see system in action
python demo_scheduling.py

# Run main to see sorting and filtering
python main.py
```

All tests should pass ✅ before deployment.
