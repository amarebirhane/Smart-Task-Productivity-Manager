from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.api import deps
from app.crud import task_share_crud, task_crud, user_crud
from app.schemas.task_share_schema import TaskShareCreate, TaskShareResponse, TaskShareUpdate
from app.models.user import User
from app.models.task import Task
from app.models.task_share import TaskShare

router = APIRouter()

@router.post("/share", response_model=TaskShareResponse)
def share_task(
    *,
    db: Session = Depends(deps.get_db),
    share_in: TaskShareCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Share a task with another user.
    """
    # 1. Verify task exists and current user is owner
    task = db.query(Task).filter(Task.id == share_in.task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the task owner can share it")
    
    # 2. Verify share user exists
    target_user = user_crud.get_user(db, user_id=str(share_in.user_id))
    if not target_user:
        raise HTTPException(status_code=404, detail="Target user not found")
        
    # 3. Check if already shared
    existing_share = db.query(TaskShare).filter(
        TaskShare.task_id == share_in.task_id,
        TaskShare.user_id == share_in.user_id
    ).first()
    if existing_share:
        return task_share_crud.update_share_permission(db, existing_share, TaskShareUpdate(permission=share_in.permission))
        
    return task_share_crud.share_task(db, share_in)

@router.get("/task/{task_id}", response_model=List[TaskShareResponse])
def get_task_collaborators(
    task_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get all collaborators for a specific task.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    # Owner or collaborator can see other collaborators
    is_collaborator = db.query(TaskShare).filter(
        TaskShare.task_id == task_id,
        TaskShare.user_id == current_user.id
    ).first()
    
    if task.user_id != current_user.id and not is_collaborator:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    return task_share_crud.get_shares_for_task(db, str(task_id))

@router.delete("/unshare/{share_id}")
def unshare_task(
    share_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Remove a collaborator from a task.
    """
    share = db.query(TaskShare).filter(TaskShare.id == share_id).first()
    if not share:
        raise HTTPException(status_code=404, detail="Share record not found")
        
    task = db.query(Task).filter(Task.id == share.task_id).first()
    
    # Only owner or the collaborator themselves can remove the share
    if task.user_id != current_user.id and share.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    task_share_crud.remove_share(db, share)
    return {"msg": "Task unshared successfully"}
