from pydantic import BaseModel

class UserReadDTO(BaseModel):
    id: int
    username: str

class UserCreateDTO(BaseModel):
    username: str
    password: str