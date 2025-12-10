from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CommentBase(BaseModel):
    user_id: int
    movie_id: int
    content: str = Field(..., min_length=1)


class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    content: str = Field(..., min_length=1)


class Comment(CommentBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
