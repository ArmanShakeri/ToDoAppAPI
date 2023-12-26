from typing import Optional
from pydantic import BaseModel


class Task(BaseModel):
    id: int
    title: str
    description: str
    done: bool


class UpdatedTask(BaseModel):
    id: Optional[int]
    title: str
    description: str
    done: bool
