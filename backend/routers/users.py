from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.schemas import User, UserCreate, UserUpdate, UserLogin
from backend.services import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[User])
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Récupérer tous les utilisateurs"""
    return UserService.get_all(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Récupérer un utilisateur par son ID"""
    user = UserService.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user


@router.get("/username/{username}", response_model=User)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    """Récupérer un utilisateur par son nom d'utilisateur"""
    user = UserService.get_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user


@router.post("/", response_model=User, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Créer un nouvel utilisateur"""
    # Vérifier si le username existe déjà
    if UserService.get_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà utilisé")
    
    # Vérifier si l'email existe déjà
    if UserService.get_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    
    return UserService.create(db, user)


@router.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Authentifier un utilisateur"""
    user = UserService.authenticate(db, credentials.username, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Identifiants incorrects")
    return {"message": "Connexion réussie", "user_id": user.id, "username": user.username}


@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour un utilisateur"""
    updated_user = UserService.update(db, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return updated_user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Supprimer un utilisateur"""
    if not UserService.delete(db, user_id):
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
