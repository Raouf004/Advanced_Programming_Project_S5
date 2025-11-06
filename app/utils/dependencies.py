from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.config import get_settings

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    
    return user

def get_user_response(user: User, db: Session) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "bio": user.bio,
        "profile_picture": user.profile_picture,
        "created_at": user.created_at,
        "followers_count": len(user.followers),
        "following_count": len(user.following),
        "posts_count": len(user.posts)
    }

def get_post_response(post, current_user: User, db: Session) -> dict:
    is_liked = current_user in post.likes if current_user else False
    return {
        "id": post.id,
        "content": post.content,
        "image_url": post.image_url,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
        "author": get_user_response(post.author, db),
        "likes_count": len(post.likes),
        "comments_count": len(post.comments),
        "is_liked": is_liked
    }