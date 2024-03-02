from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional


# Shared properties
class UserBase(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: str | None = None


class UserInDBBase(UserBase):
    id: int | None = None
    model_config = ConfigDict(from_attributes=True)


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
