"""Helpers pour l'authentification SSR"""
from fastapi import Request, HTTPException
from typing import Optional, Dict

def get_current_user_from_session(request: Request) -> Optional[Dict]:
    """
    Récupère l'utilisateur connecté depuis la session
    
    Returns:
        Dict avec id et username si connecté, None sinon
    """
    user_id = request.session.get("user_id")
    username = request.session.get("username")
    
    if user_id and username:
        return {
            "id": user_id,
            "username": username
        }
    return None


def require_auth(request: Request) -> Dict:
    """
    Vérifie que l'utilisateur est connecté, sinon raise une exception
    
    À utiliser dans les routes qui nécessitent une authentification
    
    Raises:
        HTTPException: Si l'utilisateur n'est pas connecté
        
    Returns:
        Dict avec id et username de l'utilisateur connecté
    """
    user = get_current_user_from_session(request)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Vous devez être connecté pour accéder à cette page"
        )
    return user


def is_authenticated(request: Request) -> bool:
    """
    Vérifie simplement si l'utilisateur est connecté
    
    Returns:
        True si connecté, False sinon
    """
    return request.session.get("user_id") is not None
