from typing import Optional
from pydantic import BaseModel, UUID4
from datetime import datetime

class NotificationBase(BaseModel):
    message: str
    is_read: Optional[bool] = False

class NotificationCreate(NotificationBase):
    user_id: UUID4

class NotificationUpdate(BaseModel):
    is_read: bool

class NotificationResponse(NotificationBase):
    id: UUID4
    user_id: UUID4
    created_at: datetime

    class Config:
        from_attributes = True
