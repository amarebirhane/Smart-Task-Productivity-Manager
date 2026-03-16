from pydantic import BaseModel, Field
from typing import Optional

class SettingBase(BaseModel):
    key: str = Field(..., description="Unique configuration key (e.g., SITE_NAME)")
    value: str = Field(..., description="The currently assigned value for this setting")
    description: Optional[str] = Field(None, description="Human-readable explanation of the setting's purpose")
    is_public: bool = Field(False, description="Whether this setting is exposed to non-administrator users")

class SettingCreate(SettingBase):
    pass

class SettingUpdate(BaseModel):
    value: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None

class SettingResponse(SettingBase):
    class Config:
        from_attributes = True
