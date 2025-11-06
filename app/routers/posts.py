from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database import get_db
from app.models.user import User
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.utils.dependencies import get_current_user, get_post_response

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("", response_model=PostResponse)
def create_post(
    post: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_post = Post(
        content=post.content,
        image_url=post.image_url,
        user_id=current_user.id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    return get_post_response(db_post, current_user, db)

@router.get("", response_model=List[PostResponse])
def get_feed(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    following_ids = [user.id for user in current_user.following]
    following_ids.append(current_user.id)
    
    posts = (
        db.query(Post)
        .filter(Post.user_id.in_(following_ids))
        .order_by(Post.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    return [get_post_response(post, current_user, db) for post in posts]

@router.get("/{post_id}", response_model=PostResponse)
def get_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return get_post_response(post, current_user, db)

@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post_update: PostUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to update this post"
        )
    
    if post_update.content is not None:
        post.content = post_update.content
    if post_update.image_url is not None:
        post.image_url = post_update.image_url
    
    post.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(post)
    
    return get_post_response(post, current_user, db)

@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to delete this post"
        )
    
    db.delete(post)
    db.commit()
    
    return {"message": "Post deleted successfully"}

@router.post("/{post_id}/like")
def like_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if current_user in post.likes:
        raise HTTPException(status_code=400, detail="Post already liked")
    
    post.likes.append(current_user)
    db.commit()
    
    return {"message": "Post liked successfully"}

@router.delete("/{post_id}/like")
def unlike_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if current_user not in post.likes:
        raise HTTPException(status_code=400, detail="Post not liked")
    
    post.likes.remove(current_user)
    db.commit()
    
    return {"message": "Post unliked successfully"}