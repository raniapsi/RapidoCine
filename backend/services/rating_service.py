from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from backend.models import Rating
from backend.schemas import RatingCreate, RatingUpdate


class RatingService:
    """Service pour la gestion des notes"""
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Rating]:
        return db.query(Rating).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, rating_id: int) -> Optional[Rating]:
        return db.query(Rating).filter(Rating.id == rating_id).first()
    
    @staticmethod
    def get_by_user_and_movie(db: Session, user_id: int, movie_id: int) -> Optional[Rating]:
        return db.query(Rating).filter(
            Rating.user_id == user_id,
            Rating.movie_id == movie_id
        ).first()
    
    @staticmethod
    def create(db: Session, rating: RatingCreate) -> Rating:
        # Vérifier si une note existe déjà
        existing = RatingService.get_by_user_and_movie(db, rating.user_id, rating.movie_id)
        if existing:
            # Mettre à jour la note existante
            existing.score = rating.score
            db.commit()
            db.refresh(existing)
            return existing
        
        db_rating = Rating(**rating.model_dump())
        db.add(db_rating)
        db.commit()
        db.refresh(db_rating)
        return db_rating
    
    @staticmethod
    def update(db: Session, rating_id: int, rating: RatingUpdate) -> Optional[Rating]:
        db_rating = RatingService.get_by_id(db, rating_id)
        if db_rating:
            db_rating.score = rating.score
            db.commit()
            db.refresh(db_rating)
        return db_rating
    
    @staticmethod
    def delete(db: Session, rating_id: int) -> bool:
        db_rating = RatingService.get_by_id(db, rating_id)
        if db_rating:
            db.delete(db_rating)
            db.commit()
            return True
        return False
    
    @staticmethod
    def get_by_user(db: Session, user_id: int) -> List[Rating]:
        return db.query(Rating).filter(Rating.user_id == user_id).all()
    
    @staticmethod
    def get_by_movie(db: Session, movie_id: int) -> List[Rating]:
        return db.query(Rating).filter(Rating.movie_id == movie_id).all()
    
    @staticmethod
    def get_average_rating(db: Session, movie_id: int) -> Optional[float]:
        result = db.query(func.avg(Rating.score)).filter(Rating.movie_id == movie_id).scalar()
        return round(result, 2) if result else None
