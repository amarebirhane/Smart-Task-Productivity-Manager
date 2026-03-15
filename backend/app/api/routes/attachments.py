import os
import uuid
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.api import deps
from app.crud import attachment_crud
from app.schemas.attachment_schema import AttachmentCreate, AttachmentResponse
from app.models.user import User
from app.models.task import Task
from app.models.task_share import TaskShare
from app.services.storage_service import storage_service

router = APIRouter()

@router.post("/upload/{task_id}", response_model=AttachmentResponse, summary="Upload task attachment")
async def upload_attachment(
    task_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Upload a file attachment to object storage (S3/MinIO).
    """
    # 1. Verify task exists and user has access
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    is_collaborator = db.query(TaskShare).filter(
        TaskShare.task_id == task_id,
        TaskShare.user_id == current_user.id
    ).first()
    if task.user_id != current_user.id and not is_collaborator:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # 2. Upload to Cloud Storage
    file_ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    
    content = await file.read()
    success = storage_service.upload_file(
        file_content=content,
        object_name=unique_filename,
        content_type=file.content_type
    )
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to upload file to storage")
        
    # 3. Save metadata to DB
    attachment_in = AttachmentCreate(
        task_id=task_id,
        file_name=file.filename,
        file_path=unique_filename, # Store object name
        file_type=file.content_type,
        file_size=len(content)
    )
    
    return attachment_crud.create_attachment(db, attachment_in)

@router.get("/task/{task_id}", response_model=List[AttachmentResponse], summary="List task attachments")
def get_task_attachments(
    task_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get all attachments for a task. In production, this would also provide 
    short-lived presigned URLs for secure access.
    """
    attachments = attachment_crud.get_attachments_for_task(db, str(task_id))
    
    # Enrich with presigned URLs
    for att in attachments:
        att.url = storage_service.get_presigned_url(att.file_path)
        
    return attachments

@router.delete("/{attachment_id}", summary="Delete attachment")
def delete_attachment(
    attachment_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Delete an attachment from DB and Cloud Storage.
    """
    attachment = attachment_crud.get_attachment(db, str(attachment_id))
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
        
    task = db.query(Task).filter(Task.id == attachment.task_id).first()
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only task owner can delete attachments")
    
    # Delete from S3
    storage_service.delete_file(attachment.file_path)
    
    # Delete from DB
    attachment_crud.delete_attachment(db, attachment)
    return {"msg": "Attachment deleted successfully"}
