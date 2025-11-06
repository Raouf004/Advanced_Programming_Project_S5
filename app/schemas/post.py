from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.user import UserResponse

class PostCreate(BaseModel):
    content: str
    image_url: Optional[str] = None

class PostUpdate(BaseModel):
    content: Optional[str] = None
    image_url: Optional[str] = None

class PostResponse(BaseModel):
    id: int
    content: str
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    author: UserResponse
    likes_count: int = 0
    comments_count: int = 0
    is_liked: bool = False

    class Config:
        from_attributes = True