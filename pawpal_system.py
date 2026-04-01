from dataclasses import dataclass
from typing import List, Optional, Tuple
from datetime import date, time, datetime, timedelta


@dataclass
class Pet:
    id: str
    name: str
    species: str
    breed: str
    age: str  # e.g., "2 years" or "6 months"
    weight: float
    photo_url: str
    owner_id: str

    def get_profile(self):
        """Returns all pet details."""
        return {
            "id": self.id,
            "name": self.name,
            "species": self.species,
            "breed": self.breed,
            "age": self.age,
            "weight": self.weight,
            "photo_url": self.photo_url,
            "owner_id": self.owner_id
        }

    def update_profile(self):
        """Edits name, age, weight, etc."""
        pass

    def get_scheduled_activities(self):
        """Returns all activities for this pet."""
        # Placeholder: in real impl, query activities by pet_id
        return []

    def get_todays_tasks(self):
        """Filters activities to today only."""
        # Placeholder
        return []


@dataclass
class Owner:
    id: str
    name: str
    email: str
    password_hash: str
    phone: Optional[str]
    pets: List[Pet]

    def add_pet(self, pet):
        """Adds a new pet to their profile."""
        self.pets.append(pet)

    def remove_pet(self, pet_id):
        """Removes a pet."""
        self.pets = [p for p in self.pets if p.id != pet_id]

    def get_all_pets(self):
        """Returns full list of their pets."""
        return self.pets

    def get_todays_dashboard(self):
        """Aggregates all tasks across all pets for today."""
        # Placeholder: return a TaskList with sample activities
        from datetime import date
        activities = []  # In real impl, query activities for today
        return TaskList(owner_id=self.id, date=date.today(), tasks=activities)

    def update_account(self):
        """Edits personal info."""
        pass


@dataclass
class Activity:
    id: str
    pet_id: str
    activity_type: str
    scheduled_date: date
    scheduled_time: time
    duration_minutes: int
    notes: str
    status: str  # Pending / Completed / Skipped
    priority: int = 2  # 1=low, 2=medium, 3=high
    recurrence: Optional[str] = None  # None, "daily", "weekly"

    def mark_complete(self):
        """Sets status to Completed."""
        self.status = "Completed"

    def mark_skipped(self):
        """Sets status to Skipped."""
        self.status = "Skipped"

    def reschedule(self, new_date, new_time):
        """Updates date/time."""
        self.scheduled_date = new_date
        self.scheduled_time = new_time

    def get_details(self):
        """Returns full activity info."""
        return {
            "id": self.id,
            "pet_id": self.pet_id,
            "activity_type": self.activity_type,
            "scheduled_date": self.scheduled_date,
            "scheduled_time": self.scheduled_time,
            "duration_minutes": self.duration_minutes,
            "notes": self.notes,
            "status": self.status,
            "priority": self.priority,
            "recurrence": self.recurrence
        }

    def get_end_time(self):
        """Returns the end time of this activity as a datetime."""
        dt = datetime.combine(self.scheduled_date, self.scheduled_time)
        return dt + timedelta(minutes=self.duration_minutes)


@dataclass
class Walk(Activity):
    route: Optional[str] = None
    distance_miles: float = 0.0
    walker_name: Optional[str] = None

    def log_distance(self, miles):
        """Records how far the walk was."""
        self.distance_miles = miles

    def assign_walker(self, name):
        """Assigns a walker other than the owner."""
        self.walker_name = name


@dataclass
class VetVisit(Activity):
    vet_name: str = ""
    clinic_name: str = ""
    reason: str = ""
    diagnosis: str = ""
    next_visit_date: Optional[date] = None

    def record_diagnosis(self, text):
        """Saves the vet's notes."""
        self.diagnosis = text

    def schedule_followup(self, followup_date):
        """Creates a follow-up vet visit."""
        self.next_visit_date = followup_date


@dataclass
class Feeding(Activity):
    food_type: str = ""
    amount_grams: float = 0.0
    feeding_time: str = "morning"

    def log_portion(self, amount):
        """Records how much was actually eaten."""
        self.amount_grams = amount

    def update_food_type(self, food):
        """Changes the food being tracked."""
        self.food_type = food


@dataclass
class TaskList:
    owner_id: str
    date: date
    tasks: List[Activity]

    def get_pending_tasks(self):
        """Returns only incomplete tasks."""
        return [t for t in self.tasks if t.status == "Pending"]

    def get_completed_tasks(self):
        """Returns finished tasks."""
        return [t for t in self.tasks if t.status == "Completed"]

    def get_tasks_by_status(self, status):
        """Returns tasks with a specific status."""
        return [t for t in self.tasks if t.status == status]

    def sort_by_time(self):
        """Orders tasks chronologically by priority (high first), then by time."""
        self.tasks.sort(key=lambda t: (-t.priority, t.scheduled_time))
        return self.tasks

    def filter_by_pet(self, pet_id):
        """Shows tasks for one pet only."""
        return [t for t in self.tasks if t.pet_id == pet_id]

    def get_total_duration(self):
        """Returns total duration in minutes for all tasks."""
        return sum(t.duration_minutes for t in self.tasks)

    def get_pending_duration(self):
        """Returns total duration for pending tasks only."""
        return sum(t.duration_minutes for t in self.get_pending_tasks())

    def detect_conflicts(self) -> List[Tuple[Activity, Activity]]:
        """Detects overlapping tasks and returns list of conflicting pairs."""
        conflicts = []
        sorted_tasks = sorted(self.tasks, key=lambda t: (t.scheduled_date, t.scheduled_time))
        
        for i in range(len(sorted_tasks)):
            for j in range(i + 1, len(sorted_tasks)):
                task1 = sorted_tasks[i]
                task2 = sorted_tasks[j]
                
                # Skip if different dates
                if task1.scheduled_date != task2.scheduled_date:
                    break  # No more conflicts for this date
                
                # Get end times
                end1 = task1.get_end_time()
                start2 = datetime.combine(task2.scheduled_date, task2.scheduled_time)
                
                # Check overlap: if task1 ends after task2 starts, there's a conflict
                if end1 > start2:
                    conflicts.append((task1, task2))
        
        return conflicts

    def detect_same_time_conflicts(self, pets_dict: Optional[dict] = None) -> List[str]:
        """
        Lightweight conflict detection: identifies tasks scheduled at the same time.
        Returns list of warning messages (non-blocking).
        
        Args:
            pets_dict: Optional dict mapping pet_id to Pet object for pet names in warnings
        
        Returns:
            List of warning messages about simultaneous tasks (empty if no conflicts)
        """
        warnings = []
        sorted_tasks = sorted(self.tasks, key=lambda t: (t.scheduled_date, t.scheduled_time))
        
        for i in range(len(sorted_tasks)):
            task1 = sorted_tasks[i]
            
            # Find all tasks with the same date and start time
            for j in range(i + 1, len(sorted_tasks)):
                task2 = sorted_tasks[j]
                
                # Stop checking if we've moved past this date
                if task2.scheduled_date != task1.scheduled_date:
                    break
                
                # Check if tasks start at exactly the same time
                if task1.scheduled_time == task2.scheduled_time:
                    # Create a user-friendly warning message
                    pet1_name = "Unknown Pet"
                    pet2_name = "Unknown Pet"
                    
                    if pets_dict:
                        pet1_name = pets_dict.get(task1.pet_id, Pet("", "", "", "", "", 0.0, "", "")).name
                        pet2_name = pets_dict.get(task2.pet_id, Pet("", "", "", "", "", 0.0, "", "")).name
                    
                    warning = (
                        f"⚠️  SIMULTANEOUS TASKS: {task1.activity_type} for {pet1_name} and "
                        f"{task2.activity_type} for {pet2_name} are both scheduled at "
                        f"{task1.scheduled_time.strftime('%I:%M %p')} on {task1.scheduled_date}"
                    )
                    warnings.append(warning)
        
        return warnings

    def generate_recurring_tasks(self, num_days: int) -> List[Activity]:
        """Generates recurring tasks for the next num_days days."""
        new_tasks = []
        recurring_tasks = [t for t in self.tasks if t.recurrence]
        
        for task in recurring_tasks:
            if task.recurrence == "daily":
                for day_offset in range(1, num_days + 1):
                    new_date = self.date + timedelta(days=day_offset)
                    # Create a new task (simplified: copy attributes)
                    new_task_dict = task.get_details()
                    new_task_dict['scheduled_date'] = new_date
                    new_task_dict['id'] = f"{task.id}_day{day_offset}"  # Unique ID
                    # Reconstruct task (this is simplified; in production, use proper copy)
                    new_tasks.append(self._create_task_from_dict(new_task_dict))
            
            elif task.recurrence == "weekly":
                for week_offset in range(1, num_days // 7 + 1):
                    new_date = self.date + timedelta(weeks=week_offset)
                    new_task_dict = task.get_details()
                    new_task_dict['scheduled_date'] = new_date
                    new_task_dict['id'] = f"{task.id}_week{week_offset}"
                    new_tasks.append(self._create_task_from_dict(new_task_dict))
        
        return new_tasks

    def _create_task_from_dict(self, task_dict):
        """Helper to reconstruct a task from a dictionary."""
        activity_type = task_dict.get('activity_type', 'Activity')
        
        if activity_type == 'Walk':
            return Walk(
                id=task_dict['id'], pet_id=task_dict['pet_id'], 
                activity_type='Walk', scheduled_date=task_dict['scheduled_date'],
                scheduled_time=task_dict['scheduled_time'], duration_minutes=task_dict['duration_minutes'],
                notes=task_dict.get('notes', ''), status=task_dict.get('status', 'Pending'),
                priority=task_dict.get('priority', 2), recurrence=task_dict.get('recurrence'),
                route='', distance_miles=0.0, walker_name=None
            )
        elif activity_type == 'Feeding':
            return Feeding(
                id=task_dict['id'], pet_id=task_dict['pet_id'],
                activity_type='Feeding', scheduled_date=task_dict['scheduled_date'],
                scheduled_time=task_dict['scheduled_time'], duration_minutes=task_dict['duration_minutes'],
                notes=task_dict.get('notes', ''), status=task_dict.get('status', 'Pending'),
                priority=task_dict.get('priority', 2), recurrence=task_dict.get('recurrence'),
                food_type='', amount_grams=0.0, feeding_time='morning'
            )
        elif activity_type == 'Vet Visit':
            return VetVisit(
                id=task_dict['id'], pet_id=task_dict['pet_id'],
                activity_type='Vet Visit', scheduled_date=task_dict['scheduled_date'],
                scheduled_time=task_dict['scheduled_time'], duration_minutes=task_dict['duration_minutes'],
                notes=task_dict.get('notes', ''), status=task_dict.get('status', 'Pending'),
                priority=task_dict.get('priority', 2), recurrence=task_dict.get('recurrence'),
                vet_name='', clinic_name='', reason='', diagnosis='', next_visit_date=None
            )
        else:
            return Activity(
                id=task_dict['id'], pet_id=task_dict['pet_id'],
                activity_type=task_dict.get('activity_type', 'Activity'),
                scheduled_date=task_dict['scheduled_date'], scheduled_time=task_dict['scheduled_time'],
                duration_minutes=task_dict['duration_minutes'], notes=task_dict.get('notes', ''),
                status=task_dict.get('status', 'Pending'), priority=task_dict.get('priority', 2),
                recurrence=task_dict.get('recurrence')
            )
