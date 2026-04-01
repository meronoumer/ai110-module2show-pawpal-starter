import streamlit as st
from pawpal_system import Pet, Owner, Activity, Walk, VetVisit, Feeding, TaskList
from datetime import date, time
import uuid

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# Initialize Owner in session state if not present
if 'owner' not in st.session_state:
    st.session_state.owner = Owner(
        id=str(uuid.uuid4()),
        name="",
        email="",
        password_hash="",
        phone=None,
        pets=[]
    )

owner = st.session_state.owner

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner Information")
owner.name = st.text_input("Owner name", value=owner.name or "Jordan")
owner.email = st.text_input("Email", value=owner.email or "jordan@example.com")

st.subheader("Add a Pet")
pet_name = st.text_input("Pet name", value="Mochi", key="pet_name")
species = st.selectbox("Species", ["dog", "cat", "other"], key="species")
breed = st.text_input("Breed", value="Mixed", key="breed")
age = st.text_input("Age", value="2 years", key="age")
weight = st.number_input("Weight (kg)", min_value=0.1, value=5.0, key="weight")

if st.button("Add Pet"):
    pet = Pet(
        id=str(uuid.uuid4()),
        name=pet_name,
        species=species,
        breed=breed,
        age=age,
        weight=weight,
        photo_url="",
        owner_id=owner.id
    )
    owner.add_pet(pet)
    st.success(f"Added pet: {pet.name}")

if owner.pets:
    st.write("Your Pets:")
    for pet in owner.get_all_pets():
        st.write(f"- {pet.name} ({pet.species}, {pet.age})")

st.markdown("### Tasks")
st.caption("Add tasks for your pets.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_type = st.selectbox("Task Type", ["Walk", "Feeding", "Vet Visit"], key="task_type")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, key="duration")
with col3:
    scheduled_time = st.time_input("Time", value=time(8, 0), key="time")
with col4:
    pet_select = st.selectbox("Pet", [p.name for p in owner.pets] if owner.pets else ["No pets yet"], key="pet_select")

if st.button("Add Task") and owner.pets:
    pet_name_selected = pet_select
    pet = next((p for p in owner.pets if p.name == pet_name_selected), None)
    if pet:
        if task_type == "Walk":
            task = Walk(
                id=str(uuid.uuid4()),
                pet_id=pet.id,
                activity_type="Walk",
                scheduled_date=date.today(),
                scheduled_time=scheduled_time,
                duration_minutes=duration,
                notes="",
                status="Pending",
                route="",
                distance_miles=0.0,
                walker_name=None
            )
        elif task_type == "Feeding":
            task = Feeding(
                id=str(uuid.uuid4()),
                pet_id=pet.id,
                activity_type="Feeding",
                scheduled_date=date.today(),
                scheduled_time=scheduled_time,
                duration_minutes=duration,
                notes="",
                status="Pending",
                food_type="",
                amount_grams=0.0,
                feeding_time="morning"
            )
        elif task_type == "Vet Visit":
            task = VetVisit(
                id=str(uuid.uuid4()),
                pet_id=pet.id,
                activity_type="Vet Visit",
                scheduled_date=date.today(),
                scheduled_time=scheduled_time,
                duration_minutes=duration,
                notes="",
                status="Pending",
                vet_name="",
                clinic_name="",
                reason="",
                diagnosis="",
                next_visit_date=None
            )
        st.session_state.tasks.append(task)
        st.success(f"Added {task_type} for {pet.name}")

if st.session_state.tasks:
    st.write("Current Tasks:")
    for task in st.session_state.tasks:
        pet_name = next((p.name for p in owner.pets if p.id == task.pet_id), "Unknown")
        st.write(f"- {task.activity_type} for {pet_name} at {task.scheduled_time} ({task.status})")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate today's schedule from your tasks.")

if st.button("Generate Schedule"):
    if st.session_state.tasks:
        task_list = TaskList(
            owner_id=owner.id,
            date=date.today(),
            tasks=st.session_state.tasks
        )
        sorted_tasks = task_list.sort_by_time()
        st.write("Today's Schedule:")
        for task in sorted_tasks:
            pet_name = next((p.name for p in owner.pets if p.id == task.pet_id), "Unknown")
            st.write(f"- {task.scheduled_time}: {task.activity_type} for {pet_name} ({task.duration_minutes} min)")
    else:
        st.warning("No tasks to schedule. Add some tasks first.")
