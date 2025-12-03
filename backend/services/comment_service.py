from sqlalchemy.orm import Session
from typing import List, Optional
from backend.models import Comment
from backend.schemas import CommentCreate, CommentUpdate


class CommentService:
    """Service pour la gestion des commentaires"""
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Comment]:
        return db.query(Comment).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, comment_id: int) -> Optional[Comment]:
        return db.query(Comment).filter(Comment.id == comment_id).first()
    
    @staticmethod
    def create(db: Session, comment: CommentCreate) -> Comment:
        db_comment = Comment(**comment.model_dump())
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment
    
    @staticmethod
    def update(db: Session, comment_id: int, comment: CommentUpdate) -> Optional[Comment]:
        db_comment = CommentService.get_by_id(db, comment_id)
        if db_comment:
            db_comment.content = comment.content
            db.commit()
            db.refresh(db_comment)
        return db_comment
    
    @staticmethod
    def delete(db: Session, comment_id: int) -> bool:
        db_comment = CommentService.get_by_id(db, comment_id)
        if db_comment:
            db.delete(db_comment)
            db.commit()
            return True
        return False
    
    @staticmethod
    def get_by_user(db: Session, user_id: int) -> List[Comment]:
        return db.query(Comment).filter(Comment.user_id == user_id).all()
    
    @staticmethod
    def get_by_movie(db: Session, movie_id: int) -> List[Comment]:
        return db.query(Comment).filter(Comment.movie_id == movie_id).order_by(Comment.created_at.desc()).all()
