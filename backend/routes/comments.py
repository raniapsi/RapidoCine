from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Comment, Movie
from schemas import CommentCreate, CommentResponse

router = APIRouter(prefix="/comments", tags=["comments"])


@router.get("/movie/{movie_id}", response_model=List[CommentResponse])
def get_movie_comments(movie_id: int, db: Session = Depends(get_db)):
    """Récupérer tous les commentaires d'un film"""
    comments = db.query(Comment).filter(Comment.movie_id == movie_id).all()
    return comments


@router.post("/{user_id}", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(user_id: int, comment: CommentCreate, db: Session = Depends(get_db)):
    """Créer un nouveau commentaire"""
    # Vérifier si le film existe
    movie = db.query(Movie).filter(Movie.id == comment.movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Film non trouvé")
    
    db_comment = Comment(
        user_id=user_id,
        movie_id=comment.movie_id,
        content=comment.content
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    """Supprimer un commentaire"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Commentaire non trouvé")
    
    db.delete(comment)
    db.commit()
    return None
