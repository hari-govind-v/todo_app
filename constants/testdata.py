from models.Models import TaskCreate
from enum import Enum

dummy_data = [
    TaskCreate(id=1, name="Buy groceries", description="Milk, Eggs, Bread", status="pending"),
    TaskCreate(id=2, name="Workout", description="Gym session at 6 PM", status="in_progress"),
    TaskCreate(id=3, name="Read book", description="Finish reading 'Atomic Habits'", status="completed"),
    TaskCreate(id=4, name="Write blog", description="Draft blog post on FastAPI", status="pending"),
]