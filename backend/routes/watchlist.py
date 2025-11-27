from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Watchlist, Movie
from schemas import WatchlistCreate, WatchlistResponse

router = APIRouter(prefix="/watchlist", tags=["watchlist"])


@router.get("/{user_id}", response_model=List[WatchlistResponse])
def get_user_watchlist(user_id: int, db: Session = Depends(get_db)):
    """Récupérer la watchlist d'un utilisateur"""
    watchlist = db.query(Watchlist).filter(Watchlist.user_id == user_id).all()
    return watchlist


@router.post("/{user_id}", response_model=WatchlistResponse, status_code=status.HTTP_201_CREATED)
def add_to_watchlist(user_id: int, item: WatchlistCreate, db: Session = Depends(get_db)):
    """Ajouter un film à la watchlist"""
    # Vérifier si le film existe
    movie = db.query(Movie).filter(Movie.id == item.movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Film non trouvé")
    
    # Vérifier si le film n'est pas déjà dans la watchlist
    existing = db.query(Watchlist).filter(
        Watchlist.user_id == user_id,
        Watchlist.movie_id == item.movie_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Film déjà dans la watchlist")
    
    # Ajouter à la watchlist
    watchlist_item = Watchlist(user_id=user_id, movie_id=item.movie_id)
    db.add(watchlist_item)
    db.commit()
    db.refresh(watchlist_item)
    return watchlist_item


@router.delete("/{user_id}/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_watchlist(user_id: int, movie_id: int, db: Session = Depends(get_db)):
    """Retirer un film de la watchlist"""
    item = db.query(Watchlist).filter(
        Watchlist.user_id == user_id,
        Watchlist.movie_id == movie_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Film non trouvé dans la watchlist")
    
    db.delete(item)
    db.commit()
    return None
