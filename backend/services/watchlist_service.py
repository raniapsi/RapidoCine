from sqlalchemy.orm import Session
from typing import List, Optional
from backend.models import Watchlist
from backend.schemas import WatchlistCreate, WatchlistUpdate


class WatchlistService:
    """Service pour la gestion des watchlists"""
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Watchlist]:
        return db.query(Watchlist).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, watchlist_id: int) -> Optional[Watchlist]:
        return db.query(Watchlist).filter(Watchlist.id == watchlist_id).first()
    
    @staticmethod
    def get_by_user_and_movie(db: Session, user_id: int, movie_id: int) -> Optional[Watchlist]:
        return db.query(Watchlist).filter(
            Watchlist.user_id == user_id,
            Watchlist.movie_id == movie_id
        ).first()
    
    @staticmethod
    def create(db: Session, watchlist: WatchlistCreate) -> Watchlist:
        # Vérifier si l'entrée existe déjà
        existing = WatchlistService.get_by_user_and_movie(db, watchlist.user_id, watchlist.movie_id)
        if existing:
            # Mettre à jour le statut
            existing.status = watchlist.status
            db.commit()
            db.refresh(existing)
            return existing
        
        db_watchlist = Watchlist(**watchlist.model_dump())
        db.add(db_watchlist)
        db.commit()
        db.refresh(db_watchlist)
        return db_watchlist
    
    @staticmethod
    def update(db: Session, watchlist_id: int, watchlist: WatchlistUpdate) -> Optional[Watchlist]:
        db_watchlist = WatchlistService.get_by_id(db, watchlist_id)
        if db_watchlist:
            db_watchlist.status = watchlist.status
            db.commit()
            db.refresh(db_watchlist)
        return db_watchlist
    
    @staticmethod
    def delete(db: Session, watchlist_id: int) -> bool:
        db_watchlist = WatchlistService.get_by_id(db, watchlist_id)
        if db_watchlist:
            db.delete(db_watchlist)
            db.commit()
            return True
        return False
    
    @staticmethod
    def get_by_user(db: Session, user_id: int, status: Optional[str] = None) -> List[Watchlist]:
        query = db.query(Watchlist).filter(Watchlist.user_id == user_id)
        if status:
            query = query.filter(Watchlist.status == status)
        return query.all()
    
    @staticmethod
    def get_by_movie(db: Session, movie_id: int) -> List[Watchlist]:
        return db.query(Watchlist).filter(Watchlist.movie_id == movie_id).all()
