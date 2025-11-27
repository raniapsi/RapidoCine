from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Movie Schemas
class MovieBase(BaseModel):
    title: str
    description: Optional[str] = None
    genre: Optional[str] = None
    release_date: Optional[datetime] = None
    duration: Optional[int] = None


class MovieCreate(MovieBase):
    pass


class MovieResponse(MovieBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Watchlist Schemas
class WatchlistBase(BaseModel):
    movie_id: int


class WatchlistCreate(WatchlistBase):
    pass


class WatchlistResponse(BaseModel):
    id: int
    user_id: int
    movie_id: int
    added_at: datetime
    movie: Optional[MovieResponse] = None

    class Config:
        from_attributes = True


# Comment Schemas
class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    movie_id: int


class CommentResponse(CommentBase):
    id: int
    user_id: int
    movie_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Rating Schemas
class RatingBase(BaseModel):
    score: float


class RatingCreate(RatingBase):
    movie_id: int


class RatingResponse(RatingBase):
    id: int
    user_id: int
    movie_id: int
    created_at: datetime

    class Config:
        from_attributes = True
