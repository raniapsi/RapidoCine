from .user import User, UserCreate, UserUpdate, UserLogin
from .movie import Movie, MovieCreate, MovieUpdate
from .rating import Rating, RatingCreate, RatingUpdate
from .comment import Comment, CommentCreate, CommentUpdate
from .watchlist import Watchlist, WatchlistCreate, WatchlistUpdate, WatchlistStatus

__all__ = [
    "User", "UserCreate", "UserUpdate", "UserLogin",
    "Movie", "MovieCreate", "MovieUpdate",
    "Rating", "RatingCreate", "RatingUpdate",
    "Comment", "CommentCreate", "CommentUpdate",
    "Watchlist", "WatchlistCreate", "WatchlistUpdate", "WatchlistStatus"
]
