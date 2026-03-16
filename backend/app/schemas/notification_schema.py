from typing import Optional
from pydantic import BaseModel, UUID4, Field
from datetime import datetime

class NotificationBase(BaseModel):
    message: str = Field(..., description="The content of the notification message")
    is_read: Optional[bool] = Field(False, description="Status indicating if the notification has been viewed")

class NotificationCreate(NotificationBase):
    user_id: UUID4

class NotificationUpdate(BaseModel):
    is_read: bool

class NotificationResponse(NotificationBase):
    id: UUID4 = Field(..., description="Unique persistent identifier for the notification")
    user_id: UUID4 = Field(..., description="The ID of the user who receives this notification")
    created_at: datetime = Field(..., description="Timestamp of when the notification was generated")

    class Config:
        from_attributes = True
