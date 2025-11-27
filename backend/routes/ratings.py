from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Rating, Movie
from schemas import RatingCreate, RatingResponse

router = APIRouter(prefix="/ratings", tags=["ratings"])


@router.get("/movie/{movie_id}", response_model=List[RatingResponse])
def get_movie_ratings(movie_id: int, db: Session = Depends(get_db)):
    """Récupérer toutes les notes d'un film"""
    ratings = db.query(Rating).filter(Rating.movie_id == movie_id).all()
    return ratings


@router.post("/{user_id}", response_model=RatingResponse, status_code=status.HTTP_201_CREATED)
def create_or_update_rating(user_id: int, rating: RatingCreate, db: Session = Depends(get_db)):
    """Créer ou mettre à jour une note"""
    # Vérifier si le film existe
    movie = db.query(Movie).filter(Movie.id == rating.movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Film non trouvé")
    
    # Valider le score
    if rating.score < 0 or rating.score > 10:
        raise HTTPException(status_code=400, detail="Le score doit être entre 0 et 10")
    
    # Vérifier si une note existe déjà
    existing_rating = db.query(Rating).filter(
        Rating.user_id == user_id,
        Rating.movie_id == rating.movie_id
    ).first()
    
    if existing_rating:
        # Mettre à jour
        existing_rating.score = rating.score
        db.commit()
        db.refresh(existing_rating)
        return existing_rating
    else:
        # Créer
        db_rating = Rating(
            user_id=user_id,
            movie_id=rating.movie_id,
            score=rating.score
        )
        db.add(db_rating)
        db.commit()
        db.refresh(db_rating)
        return db_rating


@router.delete("/{rating_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rating(rating_id: int, db: Session = Depends(get_db)):
    """Supprimer une note"""
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Note non trouvée")
    
    db.delete(rating)
    db.commit()
    return None
