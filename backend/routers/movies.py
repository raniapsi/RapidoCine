from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.schemas import Movie, MovieCreate, MovieUpdate
from backend.services import MovieService

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("/", response_model=List[Movie])
def get_movies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Récupérer tous les films"""
    return MovieService.get_all(db, skip=skip, limit=limit)


@router.get("/search", response_model=List[Movie])
def search_movies(
    title: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    """Rechercher des films par titre"""
    return MovieService.search_by_title(db, title)


@router.get("/year/{year}", response_model=List[Movie])
def get_movies_by_year(year: int, db: Session = Depends(get_db)):
    """Filtrer les films par année"""
    return MovieService.filter_by_year(db, year)


@router.get("/genre/{genre}", response_model=List[Movie])
def get_movies_by_genre(genre: str, db: Session = Depends(get_db)):
    """Filtrer les films par genre"""
    return MovieService.filter_by_genre(db, genre)


@router.get("/{movie_id}", response_model=Movie)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    """Récupérer un film par son ID"""
    movie = MovieService.get_by_id(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Film non trouvé")
    return movie


@router.get("/imdb/{imdb_id}", response_model=Movie)
def get_movie_by_imdb(imdb_id: str, db: Session = Depends(get_db)):
    """Récupérer un film par son ID IMDb"""
    movie = MovieService.get_by_imdb_id(db, imdb_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Film non trouvé")
    return movie


@router.post("/", response_model=Movie, status_code=201)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    """Créer un nouveau film"""
    # Vérifier si l'IMDb ID existe déjà
    if MovieService.get_by_imdb_id(db, movie.imdb_id):
        raise HTTPException(status_code=400, detail="Film avec cet IMDb ID existe déjà")
    
    return MovieService.create(db, movie)


@router.put("/{movie_id}", response_model=Movie)
def update_movie(
    movie_id: int,
    movie: MovieUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour un film"""
    updated_movie = MovieService.update(db, movie_id, movie)
    if not updated_movie:
        raise HTTPException(status_code=404, detail="Film non trouvé")
    return updated_movie


@router.delete("/{movie_id}", status_code=204)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    """Supprimer un film"""
    if not MovieService.delete(db, movie_id):
        raise HTTPException(status_code=404, detail="Film non trouvé")
