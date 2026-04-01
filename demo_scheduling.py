"""
Demonstration of advanced scheduling features in PawPal+
Includes: priority sorting, conflict detection, recurring tasks, and duration tracking
"""

from pawpal_system import *
from datetime import date, time, timedelta
import uuid

def demo():
    print("=== PawPal+ Advanced Scheduling Demo ===\n")

    # Create owner and pets
    owner = Owner(
        id=str(uuid.uuid4()),
        name="Sarah",
        email="sarah@example.com",
        password_hash="hashed",
        phone="555-1234",
        pets=[]
    )

    dog = Pet(
        id="dog_001",
        name="Max",
        species="Dog",
        breed="Labrador",
        age="3 years",
        weight=32.0,
        photo_url="",
        owner_id=owner.id
    )

    cat = Pet(
        id="cat_001",
        name="Whiskers",
        species="Cat",
        breed="Tabby",
        age="2 years",
        weight=5.5,
        photo_url="",
        owner_id=owner.id
    )

    owner.add_pet(dog)
    owner.add_pet(cat)

    # Create tasks with different priorities and times
    today = date.today()
    
    # High priority vet visit
    vet_visit = VetVisit(
        id="task_001",
        pet_id=dog.id,
        activity_type="Vet Visit",
        scheduled_date=today,
        scheduled_time=time(14, 0),  # 2 PM
        duration_minutes=60,
        notes="Annual checkup",
        status="Pending",
        priority=3,  # High priority
        recurrence=None,
        vet_name="Dr. Smith",
        clinic_name="Pet Clinic",
        reason="Annual checkup",
        diagnosis="",
        next_visit_date=None
    )

    # Morning walk with recurrence
    walk1 = Walk(
        id="task_002",
        pet_id=dog.id,
        activity_type="Walk",
        scheduled_date=today,
        scheduled_time=time(8, 0),  # 8 AM
        duration_minutes=30,
        notes="Morning exercise",
        status="Pending",
        priority=2,  # Medium
        recurrence="daily",  # This is a recurring task!
        route="Park loop",
        distance_miles=2.0,
        walker_name=None
    )

    # Feeding task for cat
    feeding = Feeding(
        id="task_003",
        pet_id=cat.id,
        activity_type="Feeding",
        scheduled_date=today,
        scheduled_time=time(8, 15),  # 8:15 AM - CONFLICTS with walk (ends at 8:30)
        duration_minutes=10,
        notes="Breakfast",
        status="Pending",
        priority=2,
        recurrence=None,
        food_type="Premium cat food",
        amount_grams=100.0,
        feeding_time="morning"
    )

    # Another walk
    walk2 = Walk(
        id="task_004",
        pet_id=dog.id,
        activity_type="Walk",
        scheduled_date=today,
        scheduled_time=time(18, 0),  # 6 PM
        duration_minutes=30,
        notes="Evening walk",
        status="Pending",
        priority=1,  # Low priority
        recurrence=None,
        route="Around block",
        distance_miles=1.5,
        walker_name=None
    )

    # Create task list
    task_list = TaskList(
        owner_id=owner.id,
        date=today,
        tasks=[vet_visit, walk1, feeding, walk2]
    )

    print(f"Owner: {owner.name}")
    print(f"Pets: {', '.join([p.name for p in owner.pets])}\n")

    # ===== Feature 1: Sorting by Priority + Time =====
    print("--- Feature 1: Sort by Priority (High→Low) then by Time ---")
    sorted_tasks = task_list.sort_by_time()
    for task in sorted_tasks:
        pet_name = next((p.name for p in owner.pets if p.id == task.pet_id), "Unknown")
        priority_label = {1: "Low", 2: "Medium", 3: "High"}[task.priority]
        print(f"{task.scheduled_time.strftime('%H:%M')} | {priority_label:6} | {task.activity_type:10} | {pet_name:10} ({task.status})")
    print()

    # ===== Feature 2: Conflict Detection =====
    print("--- Feature 2: Detect Task Conflicts ---")
    conflicts = task_list.detect_conflicts()
    if conflicts:
        print(f"Found {len(conflicts)} conflict(s):")
        for task1, task2 in conflicts:
            pet1 = next((p.name for p in owner.pets if p.id == task1.pet_id), "Unknown")
            pet2 = next((p.name for p in owner.pets if p.id == task2.pet_id), "Unknown")
            end1 = task1.get_end_time()
            print(f"  ⚠️  {task1.activity_type} ({pet1}) ends at {end1.strftime('%H:%M')}")
            print(f"      overlaps with {task2.activity_type} ({pet2}) at {task2.scheduled_time.strftime('%H:%M')}")
            print()
    else:
        print("✓ No conflicts detected!")
    print()

    # ===== Feature 3: Time Budget Tracking =====
    print("--- Feature 3: Daily Time Budget ---")
    total_mins = task_list.get_total_duration()
    pending_mins = task_list.get_pending_duration()
    completed_mins = sum(t.duration_minutes for t in task_list.get_completed_tasks())
    
    print(f"Total time scheduled: {total_mins} minutes ({total_mins / 60:.1f} hours)")
    print(f"Pending tasks: {pending_mins} minutes")
    print(f"Completed tasks: {completed_mins} minutes")
    print()

    # ===== Feature 4: Filter by Pet =====
    print("--- Feature 4: Filter Tasks by Pet ---")
    for pet in owner.pets:
        pet_tasks = task_list.filter_by_pet(pet.id)
        if pet_tasks:
            print(f"{pet.name}'s tasks:")
            for task in pet_tasks:
                print(f"  - {task.scheduled_time.strftime('%H:%M')} {task.activity_type} ({task.status})")
        else:
            print(f"{pet.name}: No tasks")
    print()

    # ===== Feature 5: Recurring Tasks =====
    print("--- Feature 5: Generate Recurring Tasks (7 days) ---")
    recurring_new_tasks = task_list.generate_recurring_tasks(7)
    if recurring_new_tasks:
        print(f"Generated {len(recurring_new_tasks)} recurring task instances:")
        for task in recurring_new_tasks[:5]:  # Show first 5
            pet_name = next((p.name for p in owner.pets if p.id == task.pet_id), "Unknown")
            print(f"  - {task.scheduled_date} at {task.scheduled_time.strftime('%H:%M')}: {task.activity_type} for {pet_name}")
        if len(recurring_new_tasks) > 5:
            print(f"  ... and {len(recurring_new_tasks) - 5} more")
    else:
        print("No recurring tasks to generate")
    print()

    # ===== Feature 6: Status Filtering =====
    print("--- Feature 6: Get Tasks by Status ---")
    for status in ["Pending", "Completed", "Skipped"]:
        status_tasks = task_list.get_tasks_by_status(status)
        print(f"{status}: {len(status_tasks)} task(s)")
    print()

    # ===== Feature 7: Mark Task Complete and Recalculate =====
    print("--- Feature 7: Update Task Status and Recalculate ---")
    print(f"Before mark_complete(): pending = {task_list.get_pending_duration()} mins")
    walk2.mark_complete()
    print(f"After marking {walk2.activity_type} complete: pending = {task_list.get_pending_duration()} mins")
    print()

    print("=== Demo Complete ===")

if __name__ == "__main__":
    demo()
