from sqlalchemy import Column, Integer, ForeignKey, DateTime, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base


class Rating(Base):
    __tablename__ = "ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False, index=True)
    score = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    
    # Contrainte : score entre 1 et 5
    __table_args__ = (
        CheckConstraint('score >= 1 AND score <= 5', name='check_rating_score'),
        UniqueConstraint('user_id', 'movie_id', name='unique_user_movie_rating'),
    )
    
    # Relations
    user = relationship("User", back_populates="ratings")
    movie = relationship("Movie", back_populates="ratings")
