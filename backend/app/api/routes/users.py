from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.crud.user_crud import get_users, get_user, delete_user, update_user
from app.schemas.user_schema import UserResponse, UserUpdateMe, PasswordChange, UserUpdate
from app.schemas.pagination_schema import PaginatedResponse
from app.services.auth_service import auth_service
from app.models.user import User
from fastapi import File, UploadFile
from app.services.storage_service import storage_service
import uuid

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def read_user_me(
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user

@router.put("/me", response_model=UserResponse)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserUpdateMe,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user profile.
    """
    user = update_user(db, db_user=current_user, user_in=UserUpdate(**user_in.model_dump()))
    return user

@router.post("/me/avatar", response_model=UserResponse)
async def upload_avatar(
    *,
    db: Session = Depends(deps.get_db),
    file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Upload own profile avatar.
    """
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Generate unique filename
    extension = file.filename.split(".")[-1]
    filename = f"avatars/{current_user.id}/{uuid.uuid4()}.{extension}"
    
    # Upload to storage
    contents = await file.read()
    success = storage_service.upload_file(contents, filename, file.content_type)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to upload image to storage")
    
    # Generate presigned URL (or public URL if configured)
    url = storage_service.get_presigned_url(filename)
    
    # Update user record
    current_user.profile_image_url = url
    db.commit()
    db.refresh(current_user)
    
    return current_user

@router.patch("/me/password")
def change_password_me(
    *,
    db: Session = Depends(deps.get_db),
    password_in: PasswordChange,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Change own password.
    """
    auth_service.change_password(
        db, user=current_user, old_password=password_in.old_password, new_password=password_in.new_password
    )
    return {"msg": "Password updated successfully"}

@router.get("/", response_model=PaginatedResponse[UserResponse])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_admin_user),
) -> Any:
    """
    Retrieve users. (Admin only)
    """
    users, total = get_users(db, skip=skip, limit=limit)
    import math
    return {
        "items": users,
        "total": total,
        "page": (skip // limit) + 1 if limit > 0 else 1,
        "size": limit,
        "pages": math.ceil(total / limit) if limit > 0 else 1
    }

@router.get("/{user_id}", response_model=UserResponse)
def read_user_by_id(
    user_id: str,
    current_user: User = Depends(deps.get_current_active_admin_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id. (Admin only)
    """
    user = get_user(db, user_id=user_id)
    if user == current_user:
        return user
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    return user

@router.delete("/{user_id}", response_model=UserResponse)
def delete_user_route(
    user_id: str,
    current_user: User = Depends(deps.get_current_active_admin_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Delete a user. (Admin only)
    """
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    delete_user(db, user)
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user_admin(
    *,
    db: Session = Depends(deps.get_db),
    user_id: str,
    user_in: UserUpdate,
    current_user: User = Depends(deps.get_current_active_admin_user),
) -> Any:
    """
    Update a user. (Admin only)
    """
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = update_user(db, db_user=user, user_in=user_in)
    return user
