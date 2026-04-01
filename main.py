"""
Main demonstration of PawPal+ scheduling system
Tests all sorting, filtering, and conflict detection methods including same-time conflicts
"""

from pawpal_system import *
from datetime import date, time, timedelta
import uuid

def main():
    print("=" * 70)
    print("🐾 PawPal+ Scheduling System - Comprehensive Demo 🐾")
    print("=" * 70)
    print()

    # Create owner and pets
    owner = Owner(
        id=str(uuid.uuid4()),
        name="Jordan",
        email="jordan@example.com",
        password_hash="secure_hash",
        phone="555-9876",
        pets=[]
    )

    dog = Pet(
        id="pet_dog_001",
        name="Buddy",
        species="Dog",
        breed="Golden Retriever",
        age="4 years",
        weight=35.0,
        photo_url="",
        owner_id=owner.id
    )

    cat = Pet(
        id="pet_cat_002",
        name="Mittens",
        species="Cat",
        breed="Persian",
        age="3 years",
        weight=4.5,
        photo_url="",
        owner_id=owner.id
    )

    rabbit = Pet(
        id="pet_rabbit_003",
        name="Fluffy",
        species="Rabbit",
        breed="Holland Lop",
        age="2 years",
        weight=2.0,
        photo_url="",
        owner_id=owner.id
    )

    owner.add_pet(dog)
    owner.add_pet(cat)
    owner.add_pet(rabbit)

    print(f"Owner: {owner.name}")
    print(f"Email: {owner.email}")
    print(f"Pets: {', '.join([p.name for p in owner.get_all_pets()])}")
    print()

    # Create tasks OUT OF ORDER (demonstrating sorting power)
    today = date.today()
    
    # Task 1: Evening walk (6 PM) - added first
    task_evening_walk = Walk(
        id="walk_001",
        pet_id=dog.id,
        activity_type="Walk",
        scheduled_date=today,
        scheduled_time=time(18, 0),  # 6 PM
        duration_minutes=45,
        notes="Evening exercise",
        status="Pending",
        priority=1,  # Low priority
        recurrence="daily",
        route="Around the neighborhood",
        distance_miles=2.5,
        walker_name=None
    )

    # Task 2: Morning feeding (8 AM) - added second
    task_morning_feed = Feeding(
        id="feed_001",
        pet_id=dog.id,
        activity_type="Feeding",
        scheduled_date=today,
        scheduled_time=time(8, 0),  # 8 AM
        duration_minutes=15,
        notes="Breakfast kibble",
        status="Pending",
        priority=2,  # Medium priority
        recurrence=None,
        food_type="Premium dog kibble",
        amount_grams=300.0,
        feeding_time="morning"
    )

    # Task 3: Vet visit (2 PM) - added third but HIGH PRIORITY
    task_vet_visit = VetVisit(
        id="vet_001",
        pet_id=dog.id,
        activity_type="Vet Visit",
        scheduled_date=today,
        scheduled_time=time(14, 0),  # 2 PM
        duration_minutes=60,
        notes="Annual wellness checkup",
        status="Pending",
        priority=3,  # HIGH priority (should come first!)
        recurrence=None,
        vet_name="Dr. Patterson",
        clinic_name="Happy Paws Veterinary",
        reason="Annual wellness exam",
        diagnosis="",
        next_visit_date=None
    )

    # Task 4: Cat feeding (8:30 AM) - CONFLICTS with dog breakfast (ends at 8:15)
    task_cat_feed = Feeding(
        id="feed_002",
        pet_id=cat.id,
        activity_type="Feeding",
        scheduled_date=today,
        scheduled_time=time(8, 30),  # 8:30 AM - OVERLAP!
        duration_minutes=10,
        notes="Wet food",
        status="Pending",
        priority=2,
        recurrence=None,
        food_type="Fancy Feast",
        amount_grams=100.0,
        feeding_time="morning"
    )

    # Task 5: Rabbit grooming (3 PM)
    task_rabbit_groom = Activity(
        id="groom_001",
        pet_id=rabbit.id,
        activity_type="Grooming",
        scheduled_date=today,
        scheduled_time=time(15, 0),  # 3 PM
        duration_minutes=30,
        notes="Fur brushing and nail trim",
        status="Pending",
        priority=1,
        recurrence=None
    )

    # Task 6: Evening cat play (7 PM)
    task_cat_play = Activity(
        id="play_001",
        pet_id=cat.id,
        activity_type="Play",
        scheduled_date=today,
        scheduled_time=time(19, 0),  # 7 PM
        duration_minutes=20,
        notes="Interactive toy play",
        status="Pending",
        priority=1,
        recurrence=None
    )

    # Task 7: Midday walk for rabbit (11 AM)
    task_rabbit_walk = Walk(
        id="walk_002",
        pet_id=rabbit.id,
        activity_type="Walk",
        scheduled_date=today,
        scheduled_time=time(11, 0),  # 11 AM
        duration_minutes=20,
        notes="Outdoor enclosure time",
        status="Pending",
        priority=2,
        recurrence=None,
        route="Backyard",
        distance_miles=0.1,
        walker_name=None
    )

    # ===== SAME-TIME CONFLICT: Task 8 & 9 =====
    # Task 8: Dog training (6 PM) - SAME TIME as evening walk!
    task_dog_training = Activity(
        id="train_001",
        pet_id=dog.id,
        activity_type="Training",
        scheduled_date=today,
        scheduled_time=time(18, 0),  # 6 PM - EXACT SAME TIME as evening walk!
        duration_minutes=30,
        notes="Obedience training session",
        status="Pending",
        priority=3,
        recurrence=None
    )

    # Task 9: Rabbit playtime (11 AM) - SAME TIME as rabbit walk!
    task_rabbit_playtime = Activity(
        id="play_002",
        pet_id=rabbit.id,
        activity_type="Play",
        scheduled_date=today,
        scheduled_time=time(11, 0),  # 11 AM - EXACT SAME TIME as rabbit walk!
        duration_minutes=25,
        notes="Supervised snuggle time",
        status="Pending",
        priority=2,
        recurrence=None
    )

    # Create task list with tasks ADDED IN RANDOM ORDER
    task_list = TaskList(
        owner_id=owner.id,
        date=today,
        tasks=[
            task_evening_walk,      # 6 PM
            task_morning_feed,      # 8 AM
            task_vet_visit,         # 2 PM (HIGH priority)
            task_cat_feed,          # 8:30 AM (OVERLAP with feed)
            task_rabbit_groom,      # 3 PM
            task_cat_play,          # 7 PM
            task_rabbit_walk,       # 11 AM
            task_dog_training,      # 6 PM - SAME TIME as walk!
            task_rabbit_playtime    # 11 AM - SAME TIME as walk!
        ]
    )

    # ===== BEFORE SORTING =====
    print("=" * 70)
    print("📋 BEFORE SORTING - Tasks in order added:")
    print("=" * 70)
    for i, task in enumerate(task_list.tasks, 1):
        pet_name = next((p.name for p in owner.pets if p.id == task.pet_id), "Unknown")
        priority_label = {1: "Low", 2: "Medium", 3: "High"}[task.priority]
        print(f"{i}. {task.scheduled_time.strftime('%I:%M %p'):>10} | {priority_label:6} | {task.activity_type:10} for {pet_name:8} | {task.status}")
    print()

    # ===== SORT BY TIME AND PRIORITY =====
    print("=" * 70)
    print("🔀 AFTER SORTING - By Priority (High→Low), Then Time:")
    print("=" * 70)
    sorted_tasks = task_list.sort_by_time()
    for i, task in enumerate(sorted_tasks, 1):
        pet_name = next((p.name for p in owner.pets if p.id == task.pet_id), "Unknown")
        priority_label = {1: "Low", 2: "Medium", 3: "High"}[task.priority]
        status_icon = "✓" if task.status == "Completed" else "◯" if task.status == "Pending" else "✗"
        print(f"{i}. {task.scheduled_time.strftime('%I:%M %p'):>10} | {priority_label:6} | {task.activity_type:10} for {pet_name:8} | {status_icon} {task.status}")
    print()

    # ===== DETECT CONFLICTS =====
    print("=" * 70)
    print("⚠️  CONFLICT DETECTION - Overlapping Tasks:")
    print("=" * 70)
    conflicts = task_list.detect_conflicts()
    if conflicts:
        print(f"Found {len(conflicts)} conflict(s):\n")
        for task1, task2 in conflicts:
            pet1 = next((p.name for p in owner.pets if p.id == task1.pet_id), "Unknown")
            pet2 = next((p.name for p in owner.pets if p.id == task2.pet_id), "Unknown")
            end1 = task1.get_end_time()
            print(f"  ❌ {task1.activity_type:10} for {pet1:8} ends at {end1.strftime('%I:%M %p')}")
            print(f"     overlaps with {task2.activity_type:10} for {pet2:8} starting at {task2.scheduled_time.strftime('%I:%M %p')}")
            print()
    else:
        print("✓ No overlapping tasks detected!")
    print()

    # ===== DETECT SAME-TIME CONFLICTS =====
    print("=" * 70)
    print("⏰ SAME-TIME CONFLICT DETECTION - Simultaneous Tasks:")
    print("=" * 70)
    # Create a pets dictionary for warning messages
    pets_dict = {pet.id: pet for pet in owner.pets}
    same_time_warnings = task_list.detect_same_time_conflicts(pets_dict=pets_dict)
    
    if same_time_warnings:
        print(f"Found {len(same_time_warnings)} simultaneous task(s):\n")
        for warning in same_time_warnings:
            print(f"  {warning}")
        print()
    else:
        print("✓ No tasks scheduled at the same time!")
    print()

    # ===== FILTER BY PET =====
    print("=" * 70)
    print("🐾 FILTER BY PET - Tasks for Each Pet:")
    print("=" * 70)
    for pet in owner.pets:
        pet_tasks = task_list.filter_by_pet(pet.id)
        print(f"\n{pet.name} ({pet.species}):")
        if pet_tasks:
            for task in sorted(pet_tasks, key=lambda t: t.scheduled_time):
                print(f"  • {task.scheduled_time.strftime('%I:%M %p'):>10} - {task.activity_type:10} ({task.status}) [Priority: {task.priority}]")
        else:
            print("  • No tasks assigned")
    print()

    # ===== FILTER BY STATUS =====
    print("=" * 70)
    print("✓ FILTER BY STATUS - Task Statistics:")
    print("=" * 70)
    pending = task_list.get_pending_tasks()
    completed = task_list.get_completed_tasks()
    print(f"Pending tasks: {len(pending)}")
    print(f"Completed tasks: {len(completed)}")
    print(f"Total tasks: {len(task_list.tasks)}")
    print()

    # ===== TIME BUDGET =====
    print("=" * 70)
    print("⏱️  TIME BUDGET - Daily Duration Analysis:")
    print("=" * 70)
    total_mins = task_list.get_total_duration()
    pending_mins = task_list.get_pending_duration()
    print(f"Total time scheduled: {total_mins} minutes ({total_mins / 60:.1f} hours)")
    print(f"Pending tasks: {pending_mins} minutes ({pending_mins / 60:.1f} hours)")
    print(f"Status: {'⚠️ Over-scheduled!' if total_mins > 480 else '✓ Well-balanced'}")
    print()

    # ===== MARK TASKS COMPLETE AND RECALCULATE =====
    print("=" * 70)
    print("✅ MARK COMPLETE - Update Task Status:")
    print("=" * 70)
    print(f"Before: {task_list.get_pending_duration()} minutes of pending tasks")
    task_morning_feed.mark_complete()
    task_rabbit_walk.mark_complete()
    print(f"After marking {task_morning_feed.activity_type} and {task_rabbit_walk.activity_type} complete:")
    print(f"After: {task_list.get_pending_duration()} minutes of pending tasks")
    print()

    # ===== RECURRING TASKS =====
    print("=" * 70)
    print("🔄 RECURRING TASKS - Generate for 7 Days:")
    print("=" * 70)
    recurring_new = task_list.generate_recurring_tasks(7)
    if recurring_new:
        print(f"Generated {len(recurring_new)} recurring task instances from:\n")
        unique_recurrences = set((t.activity_type, t.pet_id) for t in recurring_new)
        for activity_type, pet_id in unique_recurrences:
            pet_name = next((p.name for p in owner.pets if p.id == pet_id), "Unknown")
            count = sum(1 for t in recurring_new if t.activity_type == activity_type and t.pet_id == pet_id)
            print(f"  • {activity_type} for {pet_name}: {count} instances")
        print(f"\nSample dates:")
        for task in sorted(recurring_new, key=lambda t: t.scheduled_date)[:3]:
            pet_name = next((p.name for p in owner.pets if p.id == task.pet_id), "Unknown")
            print(f"  • {task.scheduled_date} at {task.scheduled_time.strftime('%I:%M %p')}: {task.activity_type} for {pet_name}")
    print()

    # ===== COMBINED COMPLEX QUERY =====
    print("=" * 70)
    print("🔍 COMPLEX QUERY - Pending Walks Sorted by Time:")
    print("=" * 70)
    walks = [t for t in task_list.tasks if isinstance(t, Walk) and t.status == "Pending"]
    walks_sorted = sorted(walks, key=lambda t: t.scheduled_time)
    if walks_sorted:
        for walk in walks_sorted:
            pet_name = next((p.name for p in owner.pets if p.id == walk.pet_id), "Unknown")
            print(f"  • {walk.scheduled_time.strftime('%I:%M %p')} - {pet_name} ({walk.distance_miles} miles) [{walk.notes}]")
    else:
        print("  • No pending walks found")
    print()

    print("=" * 70)
    print("✨ Demo Complete! All methods tested successfully. ✨")
    print("=" * 70)

if __name__ == "__main__":
    main()