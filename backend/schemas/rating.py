from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class RatingBase(BaseModel):
    user_id: int
    movie_id: int
    score: int = Field(..., ge=1, le=5)


class RatingCreate(RatingBase):
    pass


class RatingUpdate(BaseModel):
    score: int = Field(..., ge=1, le=5)


class Rating(RatingBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
