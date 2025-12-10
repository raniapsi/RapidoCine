from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base
from datetime import datetime

# ...existing code...

class Movie(Base):
    __tablename__ = "movie"
    # ...
    comments = relationship("Comment", back_populates="movie")
    ratings = relationship("Rating", back_populates="movie")

class User(Base):
    __tablename__ = "user"
    # ...
    comments = relationship("Comment", back_populates="user")
    ratings = relationship("Rating", back_populates="user")

class Rating(Base):
    __tablename__ = "rating"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    movie_id = Column(Integer, ForeignKey("movie.id"), nullable=False, index=True)
    score = Column(Integer, nullable=False)  # ✅ Integer, pas String!
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="ratings")
    movie = relationship("Movie", back_populates="ratings")
    
    # ...existing code...