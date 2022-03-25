from typing import Optional, List, Union
from uuid import UUID

from pydantic import BaseModel, EmailStr
from datetime import date

# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_onboarding: Optional[bool] = False
    is_email_validation: Optional[bool] = False
    full_name: Optional[str] = None

class UserCreate(UserBase):
    email: EmailStr
    password: str
    is_onboarding: Optional[bool] = False
    is_email_validation: Optional[bool] = False

class UserUpdate(UserBase):
    password: Optional[str] = None
    is_superuser: Optional[bool] = False


class UserInDBBase(UserBase):
    id: Optional[UUID] = None

    class Config:
        orm_mode = True

# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
