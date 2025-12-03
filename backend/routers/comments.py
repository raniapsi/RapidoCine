from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.schemas import Comment, CommentCreate, CommentUpdate
from backend.services import CommentService

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/", response_model=List[Comment])
def get_comments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Récupérer tous les commentaires"""
    return CommentService.get_all(db, skip=skip, limit=limit)


@router.get("/user/{user_id}", response_model=List[Comment])
def get_comments_by_user(user_id: int, db: Session = Depends(get_db)):
    """Récupérer les commentaires d'un utilisateur"""
    return CommentService.get_by_user(db, user_id)


@router.get("/movie/{movie_id}", response_model=List[Comment])
def get_comments_by_movie(movie_id: int, db: Session = Depends(get_db)):
    """Récupérer les commentaires d'un film"""
    return CommentService.get_by_movie(db, movie_id)


@router.get("/{comment_id}", response_model=Comment)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    """Récupérer un commentaire par son ID"""
    comment = CommentService.get_by_id(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Commentaire non trouvé")
    return comment


@router.post("/", response_model=Comment, status_code=201)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    """Créer un nouveau commentaire"""
    return CommentService.create(db, comment)


@router.put("/{comment_id}", response_model=Comment)
def update_comment(
    comment_id: int,
    comment: CommentUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour un commentaire"""
    updated_comment = CommentService.update(db, comment_id, comment)
    if not updated_comment:
        raise HTTPException(status_code=404, detail="Commentaire non trouvé")
    return updated_comment


@router.delete("/{comment_id}", status_code=204)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    """Supprimer un commentaire"""
    if not CommentService.delete(db, comment_id):
        raise HTTPException(status_code=404, detail="Commentaire non trouvé")
