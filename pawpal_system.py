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
        pass

    def update_profile(self):
        pass

    def get_scheduled_activities(self):
        pass

    def get_todays_tasks(self):
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
        pass

    def remove_pet(self, pet_id):
        pass

    def get_all_pets(self):
        pass

    def get_todays_dashboard(self):
        pass

    def update_account(self):
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
        pass

    def mark_skipped(self):
        pass

    def reschedule(self, new_date, new_time):
        pass

    def get_details(self):
        pass


@dataclass
class Walk(Activity):
    route: Optional[str]
    distance_miles: float
    walker_name: Optional[str]

    def log_distance(self, miles):
        pass

    def assign_walker(self, name):
        pass


@dataclass
class VetVisit(Activity):
    vet_name: str
    clinic_name: str
    reason: str
    diagnosis: str
    next_visit_date: Optional[date]

    def record_diagnosis(self, text):
        pass

    def schedule_followup(self, date):
        pass


@dataclass
class Feeding(Activity):
    food_type: str
    amount_grams: float
    feeding_time: str  # morning / afternoon / evening

    def log_portion(self, amount):
        pass

    def update_food_type(self, food):
        pass


@dataclass
class TaskList:
    owner_id: str
    date: date
    tasks: List[Activity]

    def get_pending_tasks(self):
        pass

    def get_completed_tasks(self):
        pass

    def sort_by_time(self):
        pass

    def filter_by_pet(self, pet_id):
        pass
