from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.task_share import TaskShare
from app.schemas.task_share_schema import TaskShareCreate, TaskShareUpdate

def share_task(db: Session, share: TaskShareCreate):
    db_share = TaskShare(**share.model_dump())
    db.add(db_share)
    db.commit()
    db.refresh(db_share)
    return db_share

def get_shares_for_task(db: Session, task_id: str) -> List[TaskShare]:
    return db.query(TaskShare).filter(TaskShare.task_id == task_id).all()

def get_shares_for_user(db: Session, user_id: str) -> List[TaskShare]:
    return db.query(TaskShare).filter(TaskShare.user_id == user_id).all()

def update_share_permission(db: Session, db_share: TaskShare, share_in: TaskShareUpdate):
    update_data = share_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_share, field, value)
    db.commit()
    db.refresh(db_share)
    return db_share

def remove_share(db: Session, db_share: TaskShare):
    db.delete(db_share)
    db.commit()
    return True
