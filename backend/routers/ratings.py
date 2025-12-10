from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.schemas import Rating, RatingCreate, RatingUpdate
from backend.services import RatingService

router = APIRouter(prefix="/ratings", tags=["Ratings"])


@router.get("/", response_model=List[Rating])
def get_ratings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Récupérer toutes les notes"""
    return RatingService.get_all(db, skip=skip, limit=limit)


@router.get("/user/{user_id}", response_model=List[Rating])
def get_ratings_by_user(user_id: int, db: Session = Depends(get_db)):
    """Récupérer les notes d'un utilisateur"""
    return RatingService.get_by_user(db, user_id)


@router.get("/movie/{movie_id}", response_model=List[Rating])
def get_ratings_by_movie(movie_id: int, db: Session = Depends(get_db)):
    """Récupérer les notes d'un film"""
    return RatingService.get_by_movie(db, movie_id)


@router.get("/movie/{movie_id}/average")
def get_average_rating(movie_id: int, db: Session = Depends(get_db)):
    """Récupérer la note moyenne d'un film"""
    avg = RatingService.get_average_rating(db, movie_id)
    if avg is None:
        return {"movie_id": movie_id, "average": None, "message": "Aucune note"}
    return {"movie_id": movie_id, "average": avg}


@router.get("/{rating_id}", response_model=Rating)
def get_rating(rating_id: int, db: Session = Depends(get_db)):
    """Récupérer une note par son ID"""
    rating = RatingService.get_by_id(db, rating_id)
    if not rating:
        raise HTTPException(status_code=404, detail="Note non trouvée")
    return rating


@router.post("/", response_model=Rating, status_code=201)
def create_rating(rating: RatingCreate, db: Session = Depends(get_db)):
    """Créer ou mettre à jour une note"""
    return RatingService.create(db, rating)


@router.put("/{rating_id}", response_model=Rating)
def update_rating(
    rating_id: int,
    rating: RatingUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour une note"""
    updated_rating = RatingService.update(db, rating_id, rating)
    if not updated_rating:
        raise HTTPException(status_code=404, detail="Note non trouvée")
    return updated_rating


@router.delete("/{rating_id}", status_code=204)
def delete_rating(rating_id: int, db: Session = Depends(get_db)):
    """Supprimer une note"""
    if not RatingService.delete(db, rating_id):
        raise HTTPException(status_code=404, detail="Note non trouvée")
