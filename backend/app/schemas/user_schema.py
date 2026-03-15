from pydantic import BaseModel, EmailStr, field_validator, Field
from uuid import UUID
from datetime import datetime
from typing import Optional
from app.utils.sanitization import sanitize_text
import re

class UserBase(BaseModel):
    email: EmailStr = Field(..., description="The unique email address of the user")
    username: str = Field(..., description="The unique username pick by the user")
    first_name: str = Field(..., description="The user's legal first name")
    last_name: str = Field(..., description="The user's legal last name")

    @field_validator('username', 'first_name', 'last_name', mode='before')
    @classmethod
    def sanitize_user_text(cls, v):
        if isinstance(v, str):
            return sanitize_text(v)
        return v

class UserCreate(UserBase):
    password: str

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r"[A-Z]", v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r"[a-z]", v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r"\d", v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError('Password must contain at least one special character')
        return v

class UserUpdate(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None # Admin only should use this normally

    @field_validator('username', 'first_name', 'last_name', mode='before')
    @classmethod
    def sanitize_user_update_text(cls, v):
        if isinstance(v, str):
            return sanitize_text(v)
        return v

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        return UserCreate.validate_password_strength(v)

class UserUpdateMe(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None

class PasswordChange(BaseModel):
    old_password: str
    new_password: str

    @field_validator('new_password')
    @classmethod
    def validate_new_password_strength(cls, v: str) -> str:
        return UserCreate.validate_password_strength(v)

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    token: str
    new_password: str

    @field_validator('new_password')
    @classmethod
    def validate_new_password_strength(cls, v: str) -> str:
        return UserCreate.validate_password_strength(v)

class UserResponse(UserBase):
    id: UUID
    role: str
    is_active: Optional[bool] = True
    is_two_factor_enabled: Optional[bool] = False
    created_at: datetime

    class Config:
        from_attributes = True
