from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.database import get_db
from backend.schemas import Watchlist, WatchlistCreate, WatchlistUpdate
from backend.services import WatchlistService

router = APIRouter(prefix="/watchlist", tags=["Watchlist"])


@router.get("/", response_model=List[Watchlist])
def get_watchlist(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Récupérer toutes les entrées de watchlist"""
    return WatchlistService.get_all(db, skip=skip, limit=limit)


@router.get("/user/{user_id}", response_model=List[Watchlist])
def get_watchlist_by_user(
    user_id: int,
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Récupérer la watchlist d'un utilisateur (filtrable par statut)"""
    return WatchlistService.get_by_user(db, user_id, status)


@router.get("/movie/{movie_id}", response_model=List[Watchlist])
def get_watchlist_by_movie(movie_id: int, db: Session = Depends(get_db)):
    """Récupérer les utilisateurs qui ont ajouté un film à leur watchlist"""
    return WatchlistService.get_by_movie(db, movie_id)


@router.get("/{watchlist_id}", response_model=Watchlist)
def get_watchlist_item(watchlist_id: int, db: Session = Depends(get_db)):
    """Récupérer une entrée de watchlist par son ID"""
    item = WatchlistService.get_by_id(db, watchlist_id)
    if not item:
        raise HTTPException(status_code=404, detail="Entrée non trouvée")
    return item


@router.post("/", response_model=Watchlist, status_code=201)
def add_to_watchlist(watchlist: WatchlistCreate, db: Session = Depends(get_db)):
    """Ajouter ou mettre à jour un film dans la watchlist"""
    return WatchlistService.create(db, watchlist)


@router.put("/{watchlist_id}", response_model=Watchlist)
def update_watchlist(
    watchlist_id: int,
    watchlist: WatchlistUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour le statut d'une entrée de watchlist"""
    updated = WatchlistService.update(db, watchlist_id, watchlist)
    if not updated:
        raise HTTPException(status_code=404, detail="Entrée non trouvée")
    return updated


@router.delete("/{watchlist_id}", status_code=204)
def remove_from_watchlist(watchlist_id: int, db: Session = Depends(get_db)):
    """Retirer un film de la watchlist"""
    if not WatchlistService.delete(db, watchlist_id):
        raise HTTPException(status_code=404, detail="Entrée non trouvée")
