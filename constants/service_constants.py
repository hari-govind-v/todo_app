from tasks.schemas import TaskCreateDTO
from enum import Enum

dummy_data = [
    TaskCreateDTO(id=1, name="Buy groceries", description="Milk, Eggs, Bread", status="pending"),
    TaskCreateDTO(id=2, name="Workout", description="Gym session at 6 PM", status="in_progress"),
    TaskCreateDTO(id=3, name="Read book", description="Finish reading 'Atomic Habits'", status="completed"),
    TaskCreateDTO(id=4, name="Write blog", description="Draft blog post on FastAPI", status="pending"),
]