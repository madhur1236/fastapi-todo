from pydantic import BaseModel
from datetime import datetime

class ToDoBase(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

class ToDoCreate(ToDoBase):
    pass

class ToDoUpdate(ToDoBase):
    pass

class ToDo(ToDoBase):
    id:int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    class Config:
        from_attributes = True

