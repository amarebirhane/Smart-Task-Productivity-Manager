from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from datetime import datetime
from typing import Optional
from app.utils.sanitization import sanitize_text
from app.schemas.category_schema import CategoryResponse

class TaskBase(BaseModel):
    title: str = Field(..., description="The main headline or title of the task")
    description: Optional[str] = Field(None, description="A detailed explanation of the task objective")
    priority: str = Field(..., description="Task urgency level (e.g., low, medium, high)")
    status: str = Field("pending", description="Current execution state (e.g., pending, in_progress, completed)")
    deadline: Optional[datetime] = Field(None, description="The target completion date and time")
    category_id: Optional[UUID] = Field(None, description="The unique ID of the category this task belongs to")

    @field_validator('title', 'description', mode='before')
    @classmethod
    def sanitize_task_text(cls, v):
        if isinstance(v, str):
            return sanitize_text(v)
        return v

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    deadline: Optional[datetime] = None
    category_id: Optional[UUID] = None
    user_id: Optional[UUID] = None

    @field_validator('title', 'description', mode='before')
    @classmethod
    def sanitize_task_update_text(cls, v):
        if isinstance(v, str):
            return sanitize_text(v)
        return v

class TaskResponse(TaskBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    category: Optional[CategoryResponse] = None

    class Config:
        from_attributes = True
