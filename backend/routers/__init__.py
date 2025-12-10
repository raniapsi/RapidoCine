from .users import router as users_router
from .movies import router as movies_router
from .ratings import router as ratings_router
from .comments import router as comments_router
from .watchlist import router as watchlist_router

__all__ = ["users_router", "movies_router", "ratings_router", "comments_router", "watchlist_router"]
