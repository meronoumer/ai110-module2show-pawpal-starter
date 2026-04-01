from pawpal_system import *
from datetime import date, time

def main():
    print("=== PawPal Today's Schedule ===\n")

    # Create an Owner
    owner = Owner(
        id="owner_001",
        name="Alice Johnson",
        email="alice@example.com",
        password_hash="secure_hash",
        phone="555-987-6543",
        pets=[]  # Will add pets below
    )

    # Create two Pets
    pet1 = Pet(
        id="pet_001",
        name="Max",
        species="Dog",
        breed="Labrador",
        age="2 years",
        weight=30.0,
        photo_url="https://example.com/max.jpg",
        owner_id=owner.id
    )

    pet2 = Pet(
        id="pet_002",
        name="Whiskers",
        species="Cat",
        breed="Siamese",
        age="1 year",
        weight=8.5,
        photo_url="https://example.com/whiskers.jpg",
        owner_id=owner.id
    )

    # Add pets to owner
    owner.pets = [pet1, pet2]

    # Create three Tasks (Activities) with different times
    task1 = Walk(
        id="task_001",
        pet_id=pet1.id,
        activity_type="Walk",
        scheduled_date=date.today(),
        scheduled_time=time(8, 0),  # 8:00 AM
        duration_minutes=30,
        notes="Morning walk",
        status="Pending",
        route="Neighborhood",
        distance_miles=1.5,
        walker_name=None
    )

    task2 = Feeding(
        id="task_002",
        pet_id=pet2.id,
        activity_type="Feeding",
        scheduled_date=date.today(),
        scheduled_time=time(12, 0),  # 12:00 PM
        duration_minutes=15,
        notes="Lunch feeding",
        status="Pending",
        food_type="Cat kibble",
        amount_grams=100.0,
        feeding_time="afternoon"
    )

    task3 = VetVisit(
        id="task_003",
        pet_id=pet1.id,
        activity_type="Vet Visit",
        scheduled_date=date.today(),
        scheduled_time=time(15, 30),  # 3:30 PM
        duration_minutes=60,
        notes="Checkup appointment",
        status="Pending",
        vet_name="Dr. Brown",
        clinic_name="Pet Health Clinic",
        reason="Annual checkup",
        diagnosis="",
        next_visit_date=None
    )

    # Collect today's tasks
    todays_tasks = [task1, task2, task3]

    # Sort tasks by scheduled time
    todays_tasks.sort(key=lambda t: t.scheduled_time)

    # Print Today's Schedule
    print(f"Owner: {owner.name}")
    print(f"Pets: {', '.join([p.name for p in owner.pets])}")
    print(f"Date: {date.today()}")
    print("\nToday's Schedule:")
    print("-" * 50)

    for task in todays_tasks:
        pet_name = next((p.name for p in owner.pets if p.id == task.pet_id), "Unknown Pet")
        print(f"{task.scheduled_time.strftime('%I:%M %p')} - {task.activity_type} for {pet_name}")
        print(f"  Duration: {task.duration_minutes} minutes")
        print(f"  Notes: {task.notes}")
        print(f"  Status: {task.status}")
        if isinstance(task, Walk):
            print(f"  Route: {task.route}, Distance: {task.distance_miles} miles")
        elif isinstance(task, Feeding):
            print(f"  Food: {task.food_type}, Amount: {task.amount_grams}g, Time: {task.feeding_time}")
        elif isinstance(task, VetVisit):
            print(f"  Vet: {task.vet_name} at {task.clinic_name}, Reason: {task.reason}")
        print()

if __name__ == "__main__":
    main()