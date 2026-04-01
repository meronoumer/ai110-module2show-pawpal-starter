"""
PawPal+ Unit Test Suite
=======================

RUN TESTS: python -m pytest tests/test_pawpal.py -v

TEST COVERAGE:
- Core Classes: Pet, Owner, Activity, Walk, VetVisit, Feeding, TaskList
- Class Creation & Attributes: Validates all dataclass fields and defaults
- Method Existence: Confirms all required methods are implemented
- Inheritance: Verifies correct class hierarchy and method availability

ADVANCED SCHEDULING TESTS:
- Priority Sorting: Tasks sorted by priority (High→Medium→Low), then by time
- Conflict Detection: Overlapping task detection and validation
- Time Calculations: End time computation, duration tracking
- Time Budget: Total/pending duration calculations for capacity planning
- Status Filtering: Get tasks by Pending/Completed/Skipped status
- Recurring Tasks: Daily and weekly task generation for next N days
- Pet Filtering: Isolate tasks by specific pet from multi-pet schedules
- Details & Metadata: Task detail formatting with priority and recurrence

TEST COUNT: 29 test cases covering all major features
PASS RATE TARGET: 100%

See TESTING.md for detailed test documentation.
"""

import pytest
from datetime import date, time, datetime, timedelta
from pawpal_system import Pet, Owner, Activity, Walk, VetVisit, Feeding, TaskList


class TestPet:
    def test_pet_creation(self):
        pet = Pet(
            id="pet_001",
            name="Buddy",
            species="Dog",
            breed="Golden Retriever",
            age="3 years",
            weight=25.5,
            photo_url="https://example.com/buddy.jpg",
            owner_id="owner_001"
        )
        assert pet.id == "pet_001"
        assert pet.name == "Buddy"
        assert pet.species == "Dog"
        assert pet.weight == 25.5

    def test_pet_methods_exist(self):
        pet = Pet("1", "Test", "Dog", "Breed", "1 year", 10.0, "url", "owner1")
        # Methods are stubs, just check they exist
        assert hasattr(pet, 'get_profile')
        assert hasattr(pet, 'update_profile')
        assert hasattr(pet, 'get_scheduled_activities')
        assert hasattr(pet, 'get_todays_tasks')


class TestOwner:
    def test_owner_creation(self):
        owner = Owner(
            id="owner_001",
            name="John Doe",
            email="john@example.com",
            password_hash="hash",
            phone="123-456",
            pets=[]
        )
        assert owner.id == "owner_001"
        assert owner.name == "John Doe"
        assert owner.email == "john@example.com"
        assert owner.pets == []

    def test_owner_with_pets(self):
        pet = Pet("1", "Buddy", "Dog", "Breed", "1 year", 10.0, "url", "owner1")
        owner = Owner("owner1", "John", "john@example.com", "hash", "123", [pet])
        assert len(owner.pets) == 1
        assert owner.pets[0].name == "Buddy"

    def test_owner_methods_exist(self):
        owner = Owner("1", "Test", "test@example.com", "hash", None, [])
        assert hasattr(owner, 'add_pet')
        assert hasattr(owner, 'remove_pet')
        assert hasattr(owner, 'get_all_pets')
        assert hasattr(owner, 'get_todays_dashboard')
        assert hasattr(owner, 'update_account')


class TestActivity:
    def test_activity_creation(self):
        activity = Activity(
            id="act_001",
            pet_id="pet_001",
            activity_type="Walk",
            scheduled_date=date.today(),
            scheduled_time=time(10, 0),
            duration_minutes=30,
            notes="Test walk",
            status="Pending"
        )
        assert activity.id == "act_001"
        assert activity.activity_type == "Walk"
        assert activity.status == "Pending"
        assert activity.duration_minutes == 30

    def test_activity_methods_exist(self):
        activity = Activity("1", "pet1", "Walk", date.today(), time(10,0), 30, "notes", "Pending")
        assert hasattr(activity, 'mark_complete')
        assert hasattr(activity, 'mark_skipped')
        assert hasattr(activity, 'reschedule')
        assert hasattr(activity, 'get_details')


class TestWalk:
    def test_walk_inheritance(self):
        walk = Walk(
            id="walk_001",
            pet_id="pet_001",
            activity_type="Walk",
            scheduled_date=date.today(),
            scheduled_time=time(10, 0),
            duration_minutes=30,
            notes="Morning walk",
            status="Pending",
            route="Park",
            distance_miles=2.0,
            walker_name="John"
        )
        # Test inheritance
        assert isinstance(walk, Activity)
        assert walk.route == "Park"
        assert walk.distance_miles == 2.0
        assert walk.walker_name == "John"

    def test_walk_methods_exist(self):
        walk = Walk("1", "pet1", "Walk", date.today(), time(10,0), 30, "notes", "Pending", "route", 1.0, "walker")
        assert hasattr(walk, 'log_distance')
        assert hasattr(walk, 'assign_walker')


class TestVetVisit:
    def test_vet_visit_inheritance(self):
        vet_visit = VetVisit(
            id="vet_001",
            pet_id="pet_001",
            activity_type="Vet Visit",
            scheduled_date=date.today(),
            scheduled_time=time(9, 0),
            duration_minutes=60,
            notes="Checkup",
            status="Pending",
            vet_name="Dr. Smith",
            clinic_name="Clinic",
            reason="Checkup",
            diagnosis="",
            next_visit_date=None
        )
        assert isinstance(vet_visit, Activity)
        assert vet_visit.vet_name == "Dr. Smith"
        assert vet_visit.reason == "Checkup"

    def test_vet_visit_methods_exist(self):
        vet_visit = VetVisit("1", "pet1", "Vet", date.today(), time(9,0), 60, "notes", "Pending", "Dr.", "Clinic", "reason", "", None)
        assert hasattr(vet_visit, 'record_diagnosis')
        assert hasattr(vet_visit, 'schedule_followup')


class TestFeeding:
    def test_feeding_inheritance(self):
        feeding = Feeding(
            id="feed_001",
            pet_id="pet_001",
            activity_type="Feeding",
            scheduled_date=date.today(),
            scheduled_time=time(8, 0),
            duration_minutes=10,
            notes="Breakfast",
            status="Pending",
            food_type="Kibble",
            amount_grams=200.0,
            feeding_time="morning"
        )
        assert isinstance(feeding, Activity)
        assert feeding.food_type == "Kibble"
        assert feeding.amount_grams == 200.0

    def test_feeding_methods_exist(self):
        feeding = Feeding("1", "pet1", "Feeding", date.today(), time(8,0), 10, "notes", "Pending", "food", 100.0, "morning")
        assert hasattr(feeding, 'log_portion')
        assert hasattr(feeding, 'update_food_type')


class TestTaskList:
    def test_task_list_creation(self):
        tasks = [
            Activity("1", "pet1", "Walk", date.today(), time(10,0), 30, "notes", "Pending"),
            Walk("2", "pet1", "Walk", date.today(), time(14,0), 30, "notes", "Pending", "route", 1.0, None)
        ]
        task_list = TaskList(
            owner_id="owner_001",
            date=date.today(),
            tasks=tasks
        )
        assert task_list.owner_id == "owner_001"
        assert len(task_list.tasks) == 2

    def test_task_list_methods_exist(self):
        task_list = TaskList("owner1", date.today(), [])
        assert hasattr(task_list, 'get_pending_tasks')
        assert hasattr(task_list, 'get_completed_tasks')
        assert hasattr(task_list, 'sort_by_time')
        assert hasattr(task_list, 'filter_by_pet')


class TestAdvancedScheduling:
    """Tests for priority sorting, conflict detection, and recurring tasks."""

    def test_priority_field_exists(self):
        """Test that Activity has priority field with default."""
        activity = Activity("1", "pet1", "Walk", date.today(), time(10,0), 30, "notes", "Pending")
        assert hasattr(activity, 'priority')
        assert activity.priority == 2  # Default medium priority

    def test_recurrence_field_exists(self):
        """Test that Activity has recurrence field."""
        activity = Activity("1", "pet1", "Walk", date.today(), time(10,0), 30, "notes", "Pending")
        assert hasattr(activity, 'recurrence')
        assert activity.recurrence is None  # Default no recurrence

    def test_priority_sorting(self):
        """Test sorting tasks by priority then time."""
        today = date.today()
        low_task = Activity("1", "pet1", "Walk", today, time(8,0), 30, "", "Pending", priority=1)
        high_task = Activity("2", "pet1", "Feed", today, time(10,0), 15, "", "Pending", priority=3)
        medium_task = Activity("3", "pet1", "Play", today, time(9,0), 20, "", "Pending", priority=2)
        
        task_list = TaskList("owner1", today, [low_task, high_task, medium_task])
        sorted_tasks = task_list.sort_by_time()
        
        # Should be sorted high (3), medium (2), low (1)
        assert sorted_tasks[0].priority == 3
        assert sorted_tasks[1].priority == 2
        assert sorted_tasks[2].priority == 1

    def test_get_end_time(self):
        """Test calculating end time of an activity."""
        activity = Activity("1", "pet1", "Walk", date.today(), time(10,0), 30, "", "Pending")
        end_time = activity.get_end_time()
        expected_end = datetime.combine(date.today(), time(10,0)) + timedelta(minutes=30)
        assert end_time == expected_end

    def test_conflict_detection_overlapping_tasks(self):
        """Test detecting overlapping tasks on the same day."""
        today = date.today()
        task1 = Activity("1", "pet1", "Walk", today, time(8,0), 30, "", "Pending")  # 8:00-8:30
        task2 = Activity("2", "pet1", "Feed", today, time(8,15), 15, "", "Pending")  # 8:15-8:30 (overlaps)
        
        task_list = TaskList("owner1", today, [task1, task2])
        conflicts = task_list.detect_conflicts()
        
        assert len(conflicts) == 1
        assert conflicts[0] == (task1, task2)

    def test_conflict_detection_no_conflicts(self):
        """Test that non-overlapping tasks don't conflict."""
        today = date.today()
        task1 = Activity("1", "pet1", "Walk", today, time(8,0), 30, "", "Pending")  # 8:00-8:30
        task2 = Activity("2", "pet1", "Feed", today, time(9,0), 15, "", "Pending")  # 9:00-9:15 (no overlap)
        
        task_list = TaskList("owner1", today, [task1, task2])
        conflicts = task_list.detect_conflicts()
        
        assert len(conflicts) == 0

    def test_conflict_detection_different_dates(self):
        """Test that tasks on different dates don't conflict."""
        today = date.today()
        tomorrow = today + timedelta(days=1)
        task1 = Activity("1", "pet1", "Walk", today, time(8,0), 30, "", "Pending")
        task2 = Activity("2", "pet1", "Feed", tomorrow, time(8,0), 15, "", "Pending")
        
        task_list = TaskList("owner1", today, [task1, task2])
        conflicts = task_list.detect_conflicts()
        
        assert len(conflicts) == 0

    def test_get_total_duration(self):
        """Test calculating total duration of all tasks."""
        today = date.today()
        task1 = Activity("1", "pet1", "Walk", today, time(8,0), 30, "", "Pending")
        task2 = Activity("2", "pet1", "Feed", today, time(9,0), 15, "", "Pending")
        task3 = Activity("3", "pet2", "Play", today, time(10,0), 45, "", "Pending")
        
        task_list = TaskList("owner1", today, [task1, task2, task3])
        total = task_list.get_total_duration()
        
        assert total == 90  # 30 + 15 + 45

    def test_get_pending_duration(self):
        """Test calculating duration of only pending tasks."""
        today = date.today()
        task1 = Activity("1", "pet1", "Walk", today, time(8,0), 30, "", "Pending")
        task2 = Activity("2", "pet1", "Feed", today, time(9,0), 15, "", "Completed")
        
        task_list = TaskList("owner1", today, [task1, task2])
        pending = task_list.get_pending_duration()
        
        assert pending == 30

    def test_get_tasks_by_status(self):
        """Test filtering tasks by status."""
        today = date.today()
        task1 = Activity("1", "pet1", "Walk", today, time(8,0), 30, "", "Pending")
        task2 = Activity("2", "pet1", "Feed", today, time(9,0), 15, "", "Completed")
        task3 = Activity("3", "pet1", "Play", today, time(10,0), 20, "", "Pending")
        
        task_list = TaskList("owner1", today, [task1, task2, task3])
        
        pending = task_list.get_tasks_by_status("Pending")
        completed = task_list.get_tasks_by_status("Completed")
        
        assert len(pending) == 2
        assert len(completed) == 1

    def test_recurring_daily_task_generation(self):
        """Test generating recurring daily tasks."""
        today = date.today()
        walk = Walk(
            "1", "pet1", "Walk", today, time(8,0), 30, "Daily walk", "Pending",
            priority=2, recurrence="daily", route="Park", distance_miles=2.0, walker_name=None
        )
        
        task_list = TaskList("owner1", today, [walk])
        new_tasks = task_list.generate_recurring_tasks(3)
        
        assert len(new_tasks) == 3
        assert new_tasks[0].scheduled_date == today + timedelta(days=1)
        assert new_tasks[1].scheduled_date == today + timedelta(days=2)
        assert new_tasks[2].scheduled_date == today + timedelta(days=3)

    def test_recurring_weekly_task_generation(self):
        """Test generating recurring weekly tasks."""
        today = date.today()
        vet_visit = VetVisit(
            "1", "pet1", "Vet Visit", today, time(14,0), 60, "Monthly checkup", "Pending",
            priority=3, recurrence="weekly", vet_name="Dr. Smith", clinic_name="Clinic",
            reason="Checkup", diagnosis="", next_visit_date=None
        )
        
        task_list = TaskList("owner1", today, [vet_visit])
        new_tasks = task_list.generate_recurring_tasks(14)  # 2 weeks
        
        assert len(new_tasks) == 2
        assert new_tasks[0].scheduled_date == today + timedelta(weeks=1)
        assert new_tasks[1].scheduled_date == today + timedelta(weeks=2)

    def test_filter_by_pet_with_multiple_pets(self):
        """Test filtering tasks by specific pet when multiple pets exist."""
        today = date.today()
        task1 = Activity("1", "pet1", "Walk", today, time(8,0), 30, "", "Pending")
        task2 = Activity("2", "pet2", "Feed", today, time(9,0), 15, "", "Pending")
        task3 = Activity("3", "pet1", "Play", today, time(10,0), 20, "", "Pending")
        
        task_list = TaskList("owner1", today, [task1, task2, task3])
        pet1_tasks = task_list.filter_by_pet("pet1")
        pet2_tasks = task_list.filter_by_pet("pet2")
        
        assert len(pet1_tasks) == 2
        assert len(pet2_tasks) == 1
        assert pet1_tasks[0].id == "1"
        assert pet1_tasks[1].id == "3"

    def test_activity_get_details_with_priority_and_recurrence(self):
        """Test that get_details includes priority and recurrence."""
        activity = Activity(
            "1", "pet1", "Walk", date.today(), time(8,0), 30, "notes", "Pending",
            priority=3, recurrence="daily"
        )
        details = activity.get_details()
        
        assert details['priority'] == 3
        assert details['recurrence'] == "daily"