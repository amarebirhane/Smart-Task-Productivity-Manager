from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class AttachmentBase(BaseModel):
    task_id: UUID = Field(..., description="The unique ID of the task this attachment belongs to")
    file_name: str = Field(..., description="The original name of the uploaded file")
    file_type: str = Field(..., description="The MIME type of the file (e.g., image/png, application/pdf)")
    file_size: int = Field(..., description="The size of the file in bytes")

class AttachmentCreate(AttachmentBase):
    file_path: str

class AttachmentResponse(AttachmentBase):
    id: UUID = Field(..., description="Unique persistent identifier for the attachment")
    file_path: str = Field(..., description="Internal storage path of the file")
    url: Optional[str] = Field(None, description="Temporary presigned URL for direct file access")
    uploaded_at: datetime = Field(..., description="Timestamp of when the file was uploaded")

    model_config = ConfigDict(from_attributes=True)
