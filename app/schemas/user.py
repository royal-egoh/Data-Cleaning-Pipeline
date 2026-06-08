from pydantic import BaseModel, ConfigDict, EmailStr, model_validator, Field, StrictBool
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(..., max_length=20)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=5)
    
class UserResponse(BaseModel):
    id: str
    username: str
    created_at: datetime
    is_active: bool
    model_config = ConfigDict(from_attributes=True)
    
class UserLogin(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)