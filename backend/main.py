from fastapi import FastAPI, Request, HTTPException, Depends, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from typing import Optional
from sqlalchemy.orm import Session, aliased
from sqlalchemy import func, desc, case, cast, Integer
from backend.config import get_settings
from backend.database import engine, Base, get_db
from backend.routers import users_router, movies_router, ratings_router, comments_router, watchlist_router
from backend.services import MovieService, UserService
from backend.services.rating_service import RatingService
import random
from pathlib import Path  # <-- ajout
import httpx  # <-- ajout pour les requêtes HTTP
import os
from dotenv import load_dotenv

load_dotenv()  # Charger les variables d'environnement

# DEBUG TEMPORAIRE
print(f" OMDB_API_KEY loaded: {os.getenv('OMDB_API_KEY', 'NOT FOUND')}")

# Créer les tables
Base.metadata.create_all(bind=engine)

# Configuration
settings = get_settings()

# Initialisation de l'application
app = FastAPI(
    title="RapidoCine - Integrated",
    version="1.0.0",
    description="IMDB Clone with full features",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configuration Sessions (AVANT CORS pour priorité)
app.add_middleware(
    SessionMiddleware,
    secret_key="votre-cle-secrete-changez-moi-en-production",  # TODO: Mettre dans .env
    session_cookie="rapidocine_session",
    max_age=86400,  # 24 heures
    same_site="lax",
    https_only=False  # True en production avec HTTPS
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for frontend (chemins ABSOLUS, robustes)
BASE_DIR = Path(__file__).resolve().parents[1]
STATIC_DIR = BASE_DIR / "frontend" / "static"
TEMPLATES_DIR = BASE_DIR / "frontend" / "templates"

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Include API routers
app.include_router(users_router, prefix="/api")
app.include_router(movies_router, prefix="/api")
app.include_router(ratings_router, prefix="/api")
app.include_router(comments_router, prefix="/api")
app.include_router(watchlist_router, prefix="/api")


# ========== FRONTEND ROUTES ==========

async def enrich_movies_with_imdb(movies: list) -> list:
    """Enrichit les films avec leur note IMDb et les trie par note décroissante."""
    enriched = []
    for movie in movies:
        imdb_rating = None
        if movie.imdb_id:
            imdb_rating = await fetch_imdb_rating(movie.imdb_id)
        setattr(movie, 'imdb_rating_5', round(imdb_rating / 2, 1) if imdb_rating else None)
        setattr(movie, 'imdb_rating_10', imdb_rating)
        enriched.append(movie)
    
    # Trier par note IMDb décroissante (les films sans note à la fin)
    enriched.sort(key=lambda m: (m.imdb_rating_10 is None, -(m.imdb_rating_10 or 0)))
    return enriched

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    """Serves the main index.html page with a featured movie."""
    current_user = None
    if request.session.get("user_id"):
        current_user = {
            "id": request.session["user_id"],
            "username": request.session["username"]
        }
    
    all_movies = MovieService.get_all(db)
    
    # Sélectionner quelques films populaires avec poster pour le carrousel
    popular_movies = [m for m in all_movies if m.plot and m.poster_url]
    featured_movies = random.sample(popular_movies, min(len(popular_movies), 5)) if popular_movies else []

    # Préparer la wishlist de l'utilisateur connecté
    watchlist_ids = []
    if current_user:
        from backend.models import Watchlist
        watchlist_ids = [row[0] for row in db.query(Watchlist.movie_id).filter(Watchlist.user_id == current_user["id"]).all()]

    return templates.TemplateResponse("index.html", {
        "request": request,
        "current_user": current_user,
        "movies": all_movies,
        "popular_movies": popular_movies,
        "featured_movies": featured_movies,
        "watchlist_ids": watchlist_ids,
        "api_url": "/api"
    })


# ========== AUTHENTICATION ROUTES ==========
@app.get("/login")
async def login_page(request: Request):
    """Page de connexion"""
    # Rediriger si déjà connecté
    if request.session.get("user_id"):
        return RedirectResponse("/", status_code=302)
    
    return templates.TemplateResponse("login.html", {
        "request": request,
        "error": request.query_params.get("error")
    })

@app.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Traiter la connexion"""
    from backend.models import User
    
    # Récupérer l'utilisateur
    user = db.query(User).filter(User.username == username).first()
    
    if not user or not UserService.verify_password(password, user.password_hash):
        return RedirectResponse("/login?error=invalid", status_code=302)
    
    # Créer la session
    request.session["user_id"] = user.id
    request.session["username"] = user.username
    
    return RedirectResponse("/", status_code=302)

@app.get("/register")
async def register_page(request: Request):
    """Page d'inscription"""
    # Rediriger si déjà connecté
    if request.session.get("user_id"):
        return RedirectResponse("/", status_code=302)
    
    return templates.TemplateResponse("register.html", {
        "request": request,
        "error": request.query_params.get("error")
    })

@app.post("/register")
async def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Traiter l'inscription"""
    from backend.models import User
    
    # Vérifier si username existe déjà
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return RedirectResponse("/register?error=username_exists", status_code=302)
    
    # Vérifier si email existe déjà
    existing_email = db.query(User).filter(User.email == email).first()
    if existing_email:
        return RedirectResponse("/register?error=email_exists", status_code=302)
    
    # Créer l'utilisateur
    new_user = User(
        username=username,
        email=email,
        password_hash=UserService.hash_password(password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Créer la session automatiquement
    request.session["user_id"] = new_user.id
    request.session["username"] = new_user.username
    
    return RedirectResponse("/", status_code=302)

@app.get("/logout")
async def logout(request: Request):
    """Déconnexion"""
    request.session.clear()
    return RedirectResponse("/login", status_code=302)


@app.get("/movies", response_class=HTMLResponse)
async def all_movies_page(request: Request, db: Session = Depends(get_db)):
    """Page showing all movies sorted by IMDb rating."""
    current_user = None
    if request.session.get("user_id"):
        current_user = {
            "id": request.session["user_id"],
            "username": request.session["username"]
        }
    
    all_movies = MovieService.get_all(db)
    
    # Enrichir et trier par note IMDb
    sorted_movies = await enrich_movies_with_imdb(all_movies)

    # Ajouter watchlist_ids
    watchlist_ids = []
    if request.session.get("user_id"):
        from backend.models import Watchlist
        watchlist_ids = [row[0] for row in db.query(Watchlist.movie_id).filter(Watchlist.user_id == request.session["user_id"]).all()]

    return templates.TemplateResponse("movies.html", {
        "request": request, 
        "movies": sorted_movies,
        "list_title": "Tous les films (triés par note IMDb)",
        "title": "Films",
        "current_user": current_user,
        "watchlist_ids": watchlist_ids,
        "show_imdb_rating": True  # Afficher les notes IMDb
    })

@app.get("/movies/{type}", response_class=HTMLResponse)
async def movie_list(request: Request, type: str, db: Session = Depends(get_db)):
    """Movie list page by type"""
    # Récupérer l'utilisateur depuis la session
    current_user = None
    if request.session.get("user_id"):
        current_user = {
            "id": request.session["user_id"],
            "username": request.session["username"]
        }

    # watchlist_ids pour toutes les variantes
    watchlist_ids = []
    if current_user:
        from backend.models import Watchlist
        watchlist_ids = [row[0] for row in db.query(Watchlist.movie_id).filter(Watchlist.user_id == current_user["id"]).all()]

    if type == "top_rated":
        # Exiger une connexion
        if not current_user:
            return RedirectResponse(url="/login", status_code=303)

        # Import models locally to avoid circular imports
        from backend.models import Rating, Movie

        # latest rating row per movie for this user
        latest_q = (
            db.query(
                Rating.movie_id.label("movie_id"),
                func.max(Rating.id).label("latest_id")
            )
            .filter(Rating.user_id == current_user["id"])
            .group_by(Rating.movie_id)
            .subquery()
        )
        Rlatest = aliased(Rating)
        # LEFT OUTER JOIN to include unrated movies, order: rated first (NULL last), then score desc, then title asc
        rows = (
            db.query(
                Movie,
                Rlatest.score.label("user_score"),
            )
            .outerjoin(latest_q, latest_q.c.movie_id == Movie.id)
            .outerjoin(Rlatest, Rlatest.id == latest_q.c.latest_id)
            .order_by(
                Rlatest.score.is_(None),  # NULL last
                Rlatest.score.desc(),      # 5, 4, 3, 2, 1
                Movie.title.asc()
            )
            .all()
        )
        filtered_movies = []
        for M, s in rows:
            setattr(M, "user_rating", int(s) if s is not None else None)
            filtered_movies.append(M)

        return templates.TemplateResponse("movies.html", {
            "request": request,
            "movies": filtered_movies,
            "list_title": "Mon Classement",
            "title": "Mon Classement",
            "current_user": current_user,
            "watchlist_ids": watchlist_ids,
            "show_imdb_rating": False  # PAS de notes IMDb dans Mon Classement
        })

    elif type == "watchlist":
        if not current_user:
            return RedirectResponse(url="/login", status_code=303)
        
        from backend.models import Watchlist, Movie
        
        watchlist_movies = (
            db.query(Movie)
            .join(Watchlist, Watchlist.movie_id == Movie.id)
            .filter(Watchlist.user_id == current_user["id"])
            .order_by(Movie.title)
            .all()
        )
        
        # PAS d'enrichissement IMDb pour la watchlist
        
        return templates.TemplateResponse("movies.html", {
            "request": request,
            "movies": watchlist_movies,
            "list_title": "Ma Watchlist",
            "title": "Ma Watchlist",
            "current_user": current_user,
            "watchlist_ids": watchlist_ids,
            "show_imdb_rating": False  # PAS de notes IMDb dans la watchlist
        })

    # default: all movies sorted by IMDb
    all_movies = MovieService.get_all(db)
    sorted_movies = await enrich_movies_with_imdb(all_movies)
    return templates.TemplateResponse("movies.html", {
        "request": request,
        "movies": sorted_movies,
        "list_title": "Films (triés par note IMDb)",
        "title": "Films",
        "current_user": current_user,
        "watchlist_ids": watchlist_ids,
        "show_imdb_rating": True  # Afficher les notes IMDb
    })

@app.get("/top-rated", response_class=HTMLResponse)
async def top_rated_page(request: Request, db: Session = Depends(get_db)):
    """Top rated page showing ONLY movies rated by CURRENT USER, ordered by THEIR score desc"""
    
    # ✅ Vérifier authentification
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    current_user = {
        "id": user_id,
        "username": request.session["username"]
    }

    from backend.models import Rating, Movie

   
    # Prendre la DERNIÈRE note par film (au cas où l'utilisateur aurait changé sa note)
    latest_q = (
        db.query(
            Rating.movie_id.label("movie_id"),
            func.max(Rating.id).label("latest_id")
        )
        .filter(Rating.user_id == user_id)  
        .group_by(Rating.movie_id)
        .subquery()
    )
    
    Rlatest = aliased(Rating)
    
    # JOIN pour récupérer les films avec la dernière note
    rows = (
        db.query(
            Movie,
            Rlatest.score.label("user_score")
        )
        .join(latest_q, latest_q.c.movie_id == Movie.id)
        .join(Rlatest, Rlatest.id == latest_q.c.latest_id)
        .all()
    )

  
    rated_movies = [{"movie": M, "rating": int(s)} for M, s in rows]
    rated_movies.sort(key=lambda x: (-x["rating"], x["movie"].title))

    return templates.TemplateResponse("top_rated.html", {
        "request": request,
        "rated_movies": rated_movies,
        "current_user": current_user
    })

@app.get("/movie/{movie_id}", response_class=HTMLResponse)
async def movie_page(request: Request, movie_id: int, db: Session = Depends(get_db)):
    # Récupérer l'utilisateur depuis la session
    current_user = None
    if request.session.get("user_id"):
        current_user = {
            "id": request.session["user_id"],
            "username": request.session["username"]
        }

    # Récupérer le film
    movie = MovieService.get_by_id(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    # Récupérer les commentaires (avec l'utilisateur si relation configurée)
    from backend.models import Comment  # éviter import circulaire en haut
    comments = db.query(Comment)\
                 .filter(Comment.movie_id == movie_id)\
                 .order_by(Comment.created_at.desc())\
                 .all()

    # watchlist_ids pour l'état du cœur sur la page détail
    watchlist_ids = []
    if current_user:
        from backend.models import Watchlist
        watchlist_ids = [row[0] for row in db.query(Watchlist.movie_id).filter(Watchlist.user_id == current_user["id"]).all()]

    # Fournir l'URL de l'API au frontend
    api_url = "/api"

    return templates.TemplateResponse("movie.html", {
        "request": request,
        "movie": movie,
        "comments": comments,
        "current_user": current_user,
        "api_url": api_url,
        "watchlist_ids": watchlist_ids
    })

@app.post("/movie/{movie_id}/comment")
async def post_movie_comment(request: Request, movie_id: int, db: Session = Depends(get_db)):
    # Vérifier authentification
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    form = await request.form()
    content = (form.get("content") or "").strip()
    if not content:
        return RedirectResponse(url=f"/movie/{movie_id}", status_code=303)

    # Insérer le commentaire
    from backend.models import Comment
    comment = Comment(user_id=user_id, movie_id=movie_id, content=content)
    db.add(comment)
    db.commit()

    return RedirectResponse(url=f"/movie/{movie_id}", status_code=303)

# ========== RATING API FOR MOVIE PAGE (session-based) ==========
@app.get("/api/movies/{movie_id}/rating")
async def api_get_movie_rating(movie_id: int, request: Request, db: Session = Depends(get_db)):
    from backend.models import Rating
    
    avg, count = db.query(func.avg(cast(Rating.score, Integer)), func.count(Rating.id))\
                   .filter(Rating.movie_id == movie_id).one()
    
    user_rating = None
    if request.session.get("user_id"):
        r = db.query(Rating).filter(
            Rating.movie_id == movie_id,
            Rating.user_id == request.session["user_id"]
        ).first()
        user_rating = int(r.score) if r else None
    
    return {
        "average": float(avg) if avg is not None else None,
        "count": int(count or 0),
        "user_rating": user_rating
    }

@app.post("/api/movies/{movie_id}/rating")
async def api_set_movie_rating(movie_id: int, request: Request, db: Session = Depends(get_db)):
    # Require session login for web rating
    user_id = request.session.get("user_id")
    if not user_id:
        return HTMLResponse(status_code=401, content='{"error":"unauthorized"}', media_type="application/json")

    data = await request.json()
    try:
        value = int(data.get("rating", 0))
    except Exception:
        value = 0
    if value < 1 or value > 5:
        return HTMLResponse(status_code=400, content='{"error":"rating must be between 1 and 5"}', media_type="application/json")

    from backend.models import Rating
    r = db.query(Rating).filter(Rating.movie_id == movie_id, Rating.user_id == user_id).first()
    if r:
        r.score = value
    else:
        r = Rating(movie_id=movie_id, user_id=user_id, score=value)
        db.add(r)
    db.commit()

    avg, count = db.query(func.avg(Rating.score), func.count(Rating.id))\
                   .filter(Rating.movie_id == movie_id).one()
    return {
        "average": float(avg) if avg is not None else None,
        "count": int(count or 0),
        "user_rating": value
    }

@app.post("/api/web/watchlist/toggle")
async def toggle_watchlist(request: Request, db: Session = Depends(get_db)):
    """Toggle un film dans la watchlist (utilisateur de la session)."""
    user_id = request.session.get("user_id")
    if not user_id:
        return HTMLResponse(status_code=401, content='{"error":"unauthorized"}', media_type="application/json")
    data = await request.json()
    try:
        movie_id = int(data.get("movie_id", 0))
    except Exception:
        movie_id = 0
    if not movie_id:
        return HTMLResponse(status_code=400, content='{"error":"movie_id required"}', media_type="application/json")

    from backend.models import Watchlist
    existing = db.query(Watchlist).filter(
        Watchlist.user_id == user_id,
        Watchlist.movie_id == movie_id
    ).first()

    if existing:
        db.delete(existing)
        db.commit()
        return {"active": False}
    else:
        w = Watchlist(user_id=user_id, movie_id=movie_id, status="planned")
        db.add(w)
        db.commit()
        return {"active": True}

@app.get("/api/movies/{movie_id}/debug")
async def api_debug_movie(movie_id: int, db: Session = Depends(get_db)):
    """DEBUG: Affiche TOUS les attributs du film pour identifier le bon champ."""
    m = MovieService.get_by_id(db, movie_id)
    if not m:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Récupérer tous les attributs du modèle
    all_attrs = {}
    for key in dir(m):
        if not key.startswith('_'):
            try:
                val = getattr(m, key, None)
                if not callable(val):
                    all_attrs[key] = str(val)[:100] if val is not None else None
            except:
                pass
    
    return {
        "movie_id": m.id,
        "title": m.title,
        "all_attributes": all_attrs
    }

# Cache simple en mémoire pour les notes IMDb (évite de spammer l'API)
IMDB_RATING_CACHE = {}

async def fetch_imdb_rating(imdb_id: str) -> float:
    """Récupère la note IMDb depuis l'API OMDB avec cache."""
    if not imdb_id:
        return None
    
    # Vérifier le cache
    if imdb_id in IMDB_RATING_CACHE:
        return IMDB_RATING_CACHE[imdb_id]
    
    # Récupérer la clé API depuis l'environnement
    OMDB_API_KEY = os.getenv("OMDB_API_KEY")
    
    if not OMDB_API_KEY:
        print("⚠️  OMDB_API_KEY manquante dans .env")
        return None
    
    try:
        url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}"
        print(f"🔍 Fetching IMDb rating for {imdb_id} with key {OMDB_API_KEY[:4]}****")
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            print(f"📡 Response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Response data: {data}")
                
                if data.get("Response") == "True" and "imdbRating" in data:
                    rating = float(data["imdbRating"])
                    print(f"Rating found: {rating}")
                    IMDB_RATING_CACHE[imdb_id] = rating
                    return rating
                else:
                    print(f"Invalid response: {data}")
            else:
                print(f"HTTP Error {response.status_code}")
    except Exception as e:
        print(f"Erreur OMDB pour {imdb_id}: {e}")
    
    return None

@app.get("/api/movies/{movie_id}/imdb")
async def api_get_imdb_rating(movie_id: int, db: Session = Depends(get_db)):
    """Récupère la note IMDb d'un film (sur 10 et convertie sur 5)."""
    movie = MovieService.get_by_id(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if not movie.imdb_id:
        return {
            "movie_id": movie_id,
            "imdb_id": None,
            "imdb_rating_10": None,
            "imdb_rating_5": None,
            "source": "no_imdb_id"
        }
    
    rating_10 = await fetch_imdb_rating(movie.imdb_id)
    rating_5 = round(rating_10 / 2, 1) if rating_10 else None
    
    return {
        "movie_id": movie_id,
        "imdb_id": movie.imdb_id,
        "imdb_rating_10": rating_10,
        "imdb_rating_5": rating_5,
        "source": "omdb_live" if rating_10 else "unavailable"
    }

