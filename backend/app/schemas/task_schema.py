from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import field_validator
from app.utils.sanitization import sanitize_text
from app.schemas.category_schema import CategoryResponse

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str
    status: str = "pending"
    deadline: Optional[datetime] = None
    category_id: Optional[UUID] = None

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
