from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class TaskShareBase(BaseModel):
    task_id: UUID
    user_id: UUID
    permission: str = "read" # read, write

class TaskShareCreate(TaskShareBase):
    pass

class TaskShareUpdate(BaseModel):
    permission: Optional[str] = None

class TaskShareResponse(TaskShareBase):
    id: UUID
    shared_at: datetime

    model_config = ConfigDict(from_attributes=True)
