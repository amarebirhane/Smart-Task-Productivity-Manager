from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.api import deps
from app.models.user import User
from app.models.notification import Notification
from app.schemas.notification_schema import NotificationResponse, NotificationUpdate

router = APIRouter()

@router.get("/", response_model=List[NotificationResponse])
def get_user_notifications(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve notifications for the current user.
    """
    notifications = (
        db.query(Notification)
        .filter(Notification.user_id == current_user.id)
        .order_by(desc(Notification.created_at))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return notifications

@router.put("/{id}/read", response_model=NotificationResponse)
def mark_notification_as_read(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Mark a specific notification as read.
    """
    notification = db.query(Notification).filter(Notification.id == id, Notification.user_id == current_user.id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.is_read = True
    db.commit()
    db.refresh(notification)
    return notification

@router.put("/read-all", response_model=List[NotificationResponse])
def mark_all_notifications_as_read(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Mark all unread notifications as read for the current user.
    """
    unread_notifications = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).all()
    
    for notif in unread_notifications:
        notif.is_read = True
        
    db.commit()
    
    # Return updated list
    return get_user_notifications(db=db, limit=50, current_user=current_user)
