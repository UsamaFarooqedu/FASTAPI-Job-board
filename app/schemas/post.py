from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    post_id: int

class Comment(CommentBase):
    id: int
    post_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class PostBase(BaseModel):
    title: str
    content: str
    tags: Optional[str] = None

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    user_id: int
    featured_image: Optional[str] = None
    additional_images: Optional[List[str]] = None
    pdf_attachments: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime
    comments: List[Comment] = []
    likes_count: int = 0

    class Config:
        from_attributes = True
