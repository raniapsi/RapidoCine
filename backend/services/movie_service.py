from sqlalchemy.orm import Session
from typing import List, Optional, Dict
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
        """Search movies by title (case-insensitive)"""
        print(f"🔍 Searching movies with title containing: '{title}'")
        if not title or title.strip() == "":
            return []
        results = db.query(Movie).filter(Movie.title.ilike(f"%{title}%")).all()
        print(f"📊 Found {len(results)} movies for '{title}'")
        for movie in results[:5]:  # Print first 5 results
            print(f"   - {movie.title} (ID: {movie.id}, Year: {movie.year})")
        return results
    
    @staticmethod
    def filter_by_year(db: Session, year: int) -> List[Movie]:
        return db.query(Movie).filter(Movie.year == year).all()
    
    @staticmethod
    def filter_by_genre(db: Session, genre: str) -> List[Movie]:
        return db.query(Movie).filter(Movie.genres.ilike(f"%{genre}%")).all()
    
    @staticmethod
    def create_from_imdb_id(db: Session, imdb_id: str) -> Optional[Movie]:
        """
        Créer un film directement depuis un ID IMDb
        """
        from backend.services.movie_fetcher import MovieFetcherService
    
        # Vérifier si le film existe déjà
        existing = MovieService.get_by_imdb_id(db, imdb_id)
        if existing:
            return existing
    
        # Récupérer les données
        fetcher = MovieFetcherService()
        movie_data = fetcher.fetch_movie_by_imdb_id(imdb_id)
    
        if not movie_data:
            return None
    
        # Créer le film
        movie = Movie(
            imdb_id=movie_data["imdb_id"],
            title=movie_data["title"],
            year=movie_data.get("year") if movie_data.get("year") else 2000,
            poster_url=movie_data.get("poster_url"),
            backdrop_url=movie_data.get("backdrop_url"),
            plot=movie_data.get("plot", ""),
            genres=movie_data.get("genres", "")
        )
    
        db.add(movie)
        db.commit()
        db.refresh(movie)
        return movie

    @staticmethod
    def get_recently_added(db: Session, limit: int = 6) -> List[Movie]:
        """Récupérer les films récemment ajoutés"""
        return db.query(Movie).order_by(Movie.id.desc()).limit(limit).all()

    @staticmethod
    def search_external_movies(query: str) -> List[Dict]:
        """
        Rechercher des films sur OMDb (pour auto-complétion)
        """
        from backend.services.movie_fetcher import MovieFetcherService
        fetcher = MovieFetcherService()
        return fetcher.search_movies_autocomplete(query)
    