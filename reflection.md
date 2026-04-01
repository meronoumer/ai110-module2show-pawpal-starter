# PawPal+ Project Reflection

## 1. System Design

### Actions
Add a Pet : The user can create a profile for their pet by entering details like name, species, breed, age, and a photo. This profile serves as the foundation for all other features.
Schedule a Walk (or Activity) : The user can schedule a walk or other care activity (feeding, vet visit, grooming) for a specific pet, setting a date, time, and duration.
See Today's Tasks : The user can view a daily dashboard showing all upcoming or pending care tasks for the day, so nothing gets missed

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

Owner
The Owner class represents the user of the application. Its primary responsibility is to serve as the top-level entry point into the system. It holds the user's personal information (name, email, phone) and maintains a list of all pets that belong to them. It is responsible for adding and removing pets, and for aggregating a daily dashboard view across all of its pets.
Pet
The Pet class is the central object in the system. It holds all descriptive information about an animal name, species, breed, age, and weight and is responsible for maintaining a list of scheduled activities associated with that pet. It can return its full profile, update its own details, and filter its activities down to just today's tasks.
Activity
The Activity class acts as the base class for all scheduled care events. It holds the common attributes shared by every task: which pet it belongs to, what type of activity it is, when it is scheduled, how long it lasts, any relevant notes, and its current status (Pending, Completed, or Skipped). It is responsible for managing its own lifecycle — marking itself complete, marking itself skipped, and rescheduling itself to a new date or time.
Walk
Walk extends Activity and adds responsibilities specific to physical exercise. It tracks route information, distance covered, and who is performing the walk if not the owner. It is responsible for logging distance and assigning a walker.
Feeding
Feeding extends Activity and handles meal-specific details. It tracks the type of food, portion size, and time of day. It is responsible for logging how much the pet actually ate and updating the food type being tracked.
Vet Visit
Vet Visit extends Activity and manages medical appointment data. It holds the vet's name, clinic, reason for the visit, diagnosis notes, and the date of any follow-up. It is responsible for recording a diagnosis and scheduling a follow-up appointment.
Task List
The Task List class serves as the daily dashboard. It is scoped to a specific owner and a specific date, and holds all Activity objects scheduled for that day. Its responsibility is purely organizational  sorting tasks by time, filtering by pet, and separating pending from completed tasks so the user gets a clear view of their day.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?



## Testing PawPal+