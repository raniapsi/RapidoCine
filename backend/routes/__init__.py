from .movies import router as movies_router
from .users import router as users_router
from .watchlist import router as watchlist_router
from .comments import router as comments_router
from .ratings import router as ratings_router

__all__ = [
    "movies_router",
    "users_router",
    "watchlist_router",
    "comments_router",
    "ratings_router"
]
