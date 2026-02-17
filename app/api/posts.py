from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.user import User
from ..models.post import Post, Comment, Like
from ..schemas import post as post_schema
from ..services import file as file_service
from .users import get_current_user
import json

router = APIRouter()

@router.post("/", response_model=post_schema.Post)
def create_post(
    title: str = Form(...),
    content: str = Form(...),
    tags: Optional[str] = Form(None),
    featured_image: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    image_path = None
    if featured_image:
        image_path = file_service.save_post_image(featured_image)
    
    new_post = Post(
        title=title,
        content=content,
        tags=tags,
        user_id=current_user.id,
        featured_image=image_path
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/", response_model=List[post_schema.Post])
def list_posts(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    posts = db.query(Post).order_by(Post.created_at.desc()).offset(skip).limit(limit).all()
    # Add manual like count if needed, but here we'll assume it's retrieved via relationship
    for post in posts:
        post.likes_count = len(post.likes)
    return posts

@router.post("/{post_id}/comment", response_model=post_schema.Comment)
def create_comment(
    post_id: int,
    comment_in: post_schema.CommentBase,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_comment = Comment(
        post_id=post_id,
        user_id=current_user.id,
        content=comment_in.content
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.post("/{post_id}/like")
def toggle_like(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    like = db.query(Like).filter(Like.post_id == post_id, Like.user_id == current_user.id).first()
    if like:
        db.delete(like)
        db.commit()
        return {"liked": False}
    else:
        new_like = Like(post_id=post_id, user_id=current_user.id)
        db.add(new_like)
        db.commit()
        return {"liked": True}
        
@router.get("/{post_id}", response_model=post_schema.Post)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.likes_count = len(post.likes)
    return post
