import os
import shutil
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

router = APIRouter()

# Ensure upload directory exists
UPLOAD_DIR = "app/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload/{task_id}", response_model=AttachmentResponse)
async def upload_attachment(
    task_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Upload a file attachment for a specific task.
    """
    # 1. Verify task exists and user has access (owner or collaborator)
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    # Check permissions: owner or collaborator
    is_collaborator = db.query(TaskShare).filter(
        TaskShare.task_id == task_id,
        TaskShare.user_id == current_user.id
    ).first()
    if task.user_id != current_user.id and not is_collaborator:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # 2. Save physical file
    file_ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # 3. Save metadata to DB
    file_size = os.path.getsize(file_path)
    
    attachment_in = AttachmentCreate(
        task_id=task_id,
        file_name=file.filename,
        file_path=file_path,
        file_type=file.content_type,
        file_size=file_size
    )
    
    return attachment_crud.create_attachment(db, attachment_in)

@router.get("/task/{task_id}", response_model=List[AttachmentResponse])
def get_task_attachments(
    task_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get all attachments linked to a task.
    """
    return attachment_crud.get_attachments_for_task(db, str(task_id))

@router.delete("/{attachment_id}")
def delete_attachment(
    attachment_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Delete an attachment.
    """
    attachment = attachment_crud.get_attachment(db, str(attachment_id))
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
        
    task = db.query(Task).filter(Task.id == attachment.task_id).first()
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only task owner can delete attachments")
        
    attachment_crud.delete_attachment(db, attachment)
    return {"msg": "Attachment deleted successfully"}
