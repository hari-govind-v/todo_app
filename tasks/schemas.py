from pydantic import BaseModel
from enum import Enum


class TaskStatusDTO(BaseModel):
    status: str

class TaskBaseDTO(BaseModel):
    name: str
    description: str
    status: str

class TaskCreateDTO(TaskBaseDTO):
    id: int
    name: str
    description: str
    status: str
    user_id: int 