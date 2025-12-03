from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base


class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    imdb_id = Column(String(20), unique=True, nullable=False, index=True)
    title = Column(String(200), nullable=False, index=True)
    year = Column(Integer, nullable=False)
    poster_url = Column(String(255), nullable=True)
    plot = Column(Text, nullable=True)
    genres = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    
    # Relations
    ratings = relationship("Rating", back_populates="movie", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="movie", cascade="all, delete-orphan")
    watchlist = relationship("Watchlist", back_populates="movie", cascade="all, delete-orphan")
