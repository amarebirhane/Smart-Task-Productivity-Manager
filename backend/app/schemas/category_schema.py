from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from typing import Optional
from app.utils.sanitization import sanitize_text

class CategoryBase(BaseModel):
    name: str = Field(..., description="Unique name for the category")

    @field_validator('name', mode='before')
    @classmethod
    def sanitize_category_name(cls, v):
        if isinstance(v, str):
            return sanitize_text(v)
        return v

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Updated name for the category")

    @field_validator('name', mode='before')
    @classmethod
    def sanitize_category_update_name(cls, v):
        if isinstance(v, str):
            return sanitize_text(v)
        return v

class CategoryResponse(CategoryBase):
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True
