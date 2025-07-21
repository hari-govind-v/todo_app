from pydantic import BaseModel
from enum import Enum


class TaskStatus(BaseModel):
    status: str

class TaskBase(BaseModel):
    name: str
    description: str
    status: str

class TaskCreate(TaskBase):
    id: int
    name: str
    description: str
    status: str
    user_id: int 