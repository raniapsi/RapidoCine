from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class WatchlistStatus(str, Enum):
    TO_WATCH = "TO_WATCH"
    WATCHING = "WATCHING"
    WATCHED = "WATCHED"


class WatchlistBase(BaseModel):
    user_id: int
    movie_id: int
    status: WatchlistStatus


class WatchlistCreate(WatchlistBase):
    pass


class WatchlistUpdate(BaseModel):
    status: WatchlistStatus


class Watchlist(WatchlistBase):
    id: int
    added_at: datetime
    
    class Config:
        from_attributes = True
