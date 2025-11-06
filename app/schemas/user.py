from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture: Optional[str] = None

class UserResponse(UserBase):
    id: int
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    created_at: datetime
    followers_count: int = 0
    following_count: int = 0
    posts_count: int = 0

    class Config:
        from_attributes = True