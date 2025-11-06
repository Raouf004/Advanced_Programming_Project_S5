from pydantic import BaseModel
from datetime import datetime
from app.schemas.user import UserResponse

class CommentCreate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    author: UserResponse

    class Config:
        from_attributes = True