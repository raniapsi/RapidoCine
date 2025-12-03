from sqlalchemy.orm import Session
from typing import List, Optional
from backend.models import Movie
from backend.schemas import MovieCreate, MovieUpdate


class MovieService:
    """Service pour la gestion des films"""
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Movie]:
        return db.query(Movie).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, movie_id: int) -> Optional[Movie]:
        return db.query(Movie).filter(Movie.id == movie_id).first()
    
    @staticmethod
    def get_by_imdb_id(db: Session, imdb_id: str) -> Optional[Movie]:
        return db.query(Movie).filter(Movie.imdb_id == imdb_id).first()
    
    @staticmethod
    def create(db: Session, movie: MovieCreate) -> Movie:
        db_movie = Movie(**movie.model_dump())
        db.add(db_movie)
        db.commit()
        db.refresh(db_movie)
        return db_movie
    
    @staticmethod
    def update(db: Session, movie_id: int, movie: MovieUpdate) -> Optional[Movie]:
        db_movie = MovieService.get_by_id(db, movie_id)
        if db_movie:
            update_data = movie.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_movie, key, value)
            db.commit()
            db.refresh(db_movie)
        return db_movie
    
    @staticmethod
    def delete(db: Session, movie_id: int) -> bool:
        db_movie = MovieService.get_by_id(db, movie_id)
        if db_movie:
            db.delete(db_movie)
            db.commit()
            return True
        return False
    
    @staticmethod
    def search_by_title(db: Session, title: str) -> List[Movie]:
        return db.query(Movie).filter(Movie.title.ilike(f"%{title}%")).all()
    
    @staticmethod
    def filter_by_year(db: Session, year: int) -> List[Movie]:
        return db.query(Movie).filter(Movie.year == year).all()
    
    @staticmethod
    def filter_by_genre(db: Session, genre: str) -> List[Movie]:
        return db.query(Movie).filter(Movie.genres.ilike(f"%{genre}%")).all()
