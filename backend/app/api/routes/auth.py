from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api import deps
from app.services.auth_service import auth_service
from app.services.audit_service import audit_service
from app.schemas.user_schema import UserCreate, UserResponse, PasswordResetRequest, PasswordReset

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
) -> Any:
    """
    Create new user.
    """
    return auth_service.register_new_user(db, user_in)

@router.post("/login")
def login(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = auth_service.authenticate_user(
        db, identifier=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Incorrect email/username or password"
        )
    
    if user.is_two_factor_enabled:
        return {"msg": "2FA required", "2fa_required": True, "user_id": str(user.id)}

    audit_service.log(db, user_id=user.id, username=user.username, action="login")
    return auth_service.create_login_token(str(user.id))

@router.post("/logout")
def logout(
    db: Session = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_active_user)
) -> Any:
    """
    Log out the current user.
    """
    audit_service.log(db, user_id=current_user.id, username=current_user.username, action="logout")
    return {"msg": "Logged out successfully"}

@router.post("/2fa/setup")
def setup_2fa(
    db: Session = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_active_user)
) -> Any:
    """
    Setup 2FA for the current user.
    """
    secret = auth_service.setup_2fa(db, current_user)
    # Generate provisioning URI for QR code
    from app.core.config import settings
    provisioning_uri = f"otpauth://totp/{settings.PROJECT_NAME}:{current_user.email}?secret={secret}&issuer={settings.PROJECT_NAME}"
    return {"secret": secret, "provisioning_uri": provisioning_uri}

@router.post("/2fa/verify")
def verify_2fa_setup(
    db: Session = Depends(deps.get_db),
    code: str = Query(...),
    current_user: Any = Depends(deps.get_current_active_user)
) -> Any:
    """
    Verify and enable 2FA.
    """
    if auth_service.verify_2fa(current_user, code):
        current_user.is_two_factor_enabled = True
        db.commit()
        audit_service.log(db, user_id=current_user.id, username=current_user.username, action="2fa_enabled")
        return {"msg": "2FA enabled successfully"}
    raise HTTPException(status_code=400, detail="Invalid 2FA code")

@router.post("/2fa/login")
def login_2fa(
    db: Session = Depends(deps.get_db),
    user_id: str = Query(...),
    code: str = Query(...)
) -> Any:
    """
    Login with 2FA code.
    """
    from app.crud.user_crud import get_user
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if auth_service.verify_2fa(user, code):
        audit_service.log(db, user_id=user.id, username=user.username, action="login_2fa")
        return auth_service.create_login_token(str(user.id))
    
    audit_service.log(db, user_id=user.id, username=user.username, action="2fa_login_failed")
    raise HTTPException(status_code=400, detail="Invalid 2FA code")

@router.post("/password-reset/request")
def request_password_reset(
    data: PasswordResetRequest
) -> Any:
    """
    Generate a password reset token. In a real app, this would be emailed.
    """
    token = auth_service.create_password_reset_token(data.email)
    return {"msg": "Password reset token generated", "token": token}

@router.post("/password-reset/reset")
def reset_password(
    data: PasswordReset,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Reset password using a token.
    """
    auth_service.reset_password(db, token=data.token, new_password=data.new_password)
    return {"msg": "Password updated successfully"}
