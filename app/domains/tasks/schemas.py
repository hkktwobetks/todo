from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class TaskRead(BaseModel):
    id: int
    title: str
    status: str
    due_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    status: str = Field("todo", pattern="^(todo|in_progress|done)$")
    due_at: Optional[datetime] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    status: Optional[str] = Field(None, pattern="^(todo|in_progress|done)$")
    due_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class TaskPage(BaseModel):
    items: list[TaskRead]
    total: int
    limit: int
    offset: int

    model_config = ConfigDict(from_attributes=True)