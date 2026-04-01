import pytest
from datetime import date, time
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