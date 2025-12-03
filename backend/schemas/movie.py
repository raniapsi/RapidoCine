from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MovieBase(BaseModel):
    imdb_id: str = Field(..., max_length=20)
    title: str = Field(..., max_length=200)
    year: int = Field(..., gt=1800, lt=2100)
    poster_url: Optional[str] = Field(None, max_length=255)
    plot: Optional[str] = None
    genres: Optional[str] = Field(None, max_length=255)


class MovieCreate(MovieBase):
    pass


class MovieUpdate(BaseModel):
    imdb_id: Optional[str] = Field(None, max_length=20)
    title: Optional[str] = Field(None, max_length=200)
    year: Optional[int] = Field(None, gt=1800, lt=2100)
    poster_url: Optional[str] = Field(None, max_length=255)
    plot: Optional[str] = None
    genres: Optional[str] = Field(None, max_length=255)


class Movie(MovieBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
