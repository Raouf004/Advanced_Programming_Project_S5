from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.utils.dependencies import get_current_user, get_user_response

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
def get_current_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_user_response(current_user, db)

@router.put("/me", response_model=UserResponse)
def update_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name
    if user_update.bio is not None:
        current_user.bio = user_update.bio
    if user_update.profile_picture is not None:
        current_user.profile_picture = user_update.profile_picture
    
    db.commit()
    db.refresh(current_user)
    
    return get_user_response(current_user, db)

@router.get("/{username}", response_model=UserResponse)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return get_user_response(user, db)

@router.post("/{username}/follow")
def follow_user(
    username: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_to_follow = db.query(User).filter(User.username == username).first()
    if not user_to_follow:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_to_follow == current_user:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")
    
    if user_to_follow in current_user.following:
        raise HTTPException(status_code=400, detail="Already following this user")
    
    current_user.following.append(user_to_follow)
    db.commit()
    
    return {"message": "Successfully followed user"}

@router.delete("/{username}/follow")
def unfollow_user(
    username: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_to_unfollow = db.query(User).filter(User.username == username).first()
    if not user_to_unfollow:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_to_unfollow not in current_user.following:
        raise HTTPException(status_code=400, detail="Not following this user")
    
    current_user.following.remove(user_to_unfollow)
    db.commit()
    
    return {"message": "Successfully unfollowed user"}

@router.get("/{username}/followers", response_model=List[UserResponse])
def get_followers(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return [get_user_response(follower, db) for follower in user.followers]

@router.get("/{username}/following", response_model=List[UserResponse])
def get_following(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return [get_user_response(followed, db) for followed in user.following]