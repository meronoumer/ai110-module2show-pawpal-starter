from dataclasses import dataclass
from typing import List, Optional
from datetime import date, time


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
        pass

    def update_profile(self):
        """Edits name, age, weight, etc."""
        pass

    def get_scheduled_activities(self):
        """Returns all activities for this pet."""
        pass

    def get_todays_tasks(self):
        """Filters activities to today only."""
        pass


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
        pass

    def remove_pet(self, pet_id):
        """Removes a pet."""
        pass

    def get_all_pets(self):
        """Returns full list of their pets."""
        pass

    def get_todays_dashboard(self):
        """Aggregates all tasks across all pets for today."""
        pass

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

    def mark_complete(self):
        """Sets status to Completed."""
        pass

    def mark_skipped(self):
        """Sets status to Skipped."""
        pass

    def reschedule(self, new_date, new_time):
        """Updates date/time."""
        pass

    def get_details(self):
        """Returns full activity info."""
        pass


@dataclass
class Walk(Activity):
    route: Optional[str]
    distance_miles: float
    walker_name: Optional[str]

    def log_distance(self, miles):
        """Records how far the walk was."""
        pass

    def assign_walker(self, name):
        """Assigns a walker other than the owner."""
        pass


@dataclass
class VetVisit(Activity):
    vet_name: str
    clinic_name: str
    reason: str
    diagnosis: str
    next_visit_date: Optional[date]

    def record_diagnosis(self, text):
        """Saves the vet's notes."""
        pass

    def schedule_followup(self, date):
        """Creates a follow-up vet visit."""
        pass


@dataclass
class Feeding(Activity):
    food_type: str
    amount_grams: float
    feeding_time: str  # morning / afternoon / evening

    def log_portion(self, amount):
        """Records how much was actually eaten."""
        pass

    def update_food_type(self, food):
        """Changes the food being tracked."""
        pass


@dataclass
class TaskList:
    owner_id: str
    date: date
    tasks: List[Activity]

    def get_pending_tasks(self):
        """Returns only incomplete tasks."""
        pass

    def get_completed_tasks(self):
        """Returns finished tasks."""
        pass

    def sort_by_time(self):
        """Orders tasks chronologically."""
        pass

    def filter_by_pet(self, pet_id):
        """Shows tasks for one pet only."""
        pass
