from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base


class Watchlist(Base):
    __tablename__ = "watchlist"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False, index=True)
    status = Column(String(20), nullable=False)  # TO_WATCH, WATCHING, WATCHED
    added_at = Column(DateTime, nullable=False, server_default=func.now())
    
    # Contrainte : unicité du couple (user_id, movie_id)
    __table_args__ = (
        UniqueConstraint('user_id', 'movie_id', name='unique_user_movie_watchlist'),
    )
    
    # Relations
    user = relationship("User", back_populates="watchlist")
    movie = relationship("Movie", back_populates="watchlist")
