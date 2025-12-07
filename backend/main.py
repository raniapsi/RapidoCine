from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from typing import Optional
from sqlalchemy.orm import Session
from backend.config import get_settings
from backend.database import engine, Base, get_db
from backend.routers import users_router, movies_router, ratings_router, comments_router, watchlist_router
from backend.services import MovieService

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

# Mount static files for frontend
app.mount("/static", StaticFiles(directory="./frontend/static"), name="static")
templates = Jinja2Templates(directory="./frontend/templates")

# Include API routers
app.include_router(users_router, prefix="/api")
app.include_router(movies_router, prefix="/api")
app.include_router(ratings_router, prefix="/api")
app.include_router(comments_router, prefix="/api")
app.include_router(watchlist_router, prefix="/api")


# ========== AUTHENTICATION ROUTES ==========
from fastapi import Form
from backend.services import UserService

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


# ========== FRONTEND ROUTES ==========
@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    """Home page with carousel and movie list"""
    # Récupérer l'utilisateur depuis la session
    current_user = None
    if request.session.get("user_id"):
        current_user = {
            "id": request.session["user_id"],
            "username": request.session["username"]
        }
    
    # Récupérer les films depuis la base de données
    all_movies = MovieService.get_all(db)
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "popular_movies": all_movies,  
        "featured_movies": all_movies,
        "current_user": current_user
    })

movies_data_old = [
    {
        "id": 1,
        "title": "The Shawshank Redemption",
        "original_title": "The Shawshank Redemption",
        "overview": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
        "release_date": "1994-09-23",
        "vote_average": 9.3,
        "vote_count": 2500000,
        "poster_path": "https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/w1280/iNh3BivHyg5sQRPP1KOkzguEX0H.jpg",
        "genres": [{"id": 18, "name": "Drama"}],
        "runtime": 142,
        "tagline": "Fear can hold you prisoner. Hope can set you free.",
        "homepage": "https://www.warnerbros.com/movies/shawshank-redemption",
        "imdb_id": "tt0111161",
        "production_companies": [
            {
                "id": 97,
                "name": "Castle Rock Entertainment",
                "logo_path": "https://image.tmdb.org/t/p/w500/7znWcbDd4PcJzJUlJxYqAlPPykp.png"
            }
        ]
    },
    {
        "id": 2,
        "title": "The Godfather",
        "original_title": "The Godfather", 
        "overview": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
        "release_date": "1972-03-24",
        "vote_average": 9.2,
        "vote_count": 1700000,
        "poster_path": "https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/w1280/tmU7GeKVybMWFButWEGl2M4GeiP.jpg",
        "genres": [{"id": 18, "name": "Drama"}, {"id": 80, "name": "Crime"}],
        "runtime": 175,
        "tagline": "An offer you can't refuse.",
        "homepage": "https://www.paramount.com/movies/godfather",
        "imdb_id": "tt0068646",
        "production_companies": [
            {
                "id": 4,
                "name": "Paramount Pictures",
                "logo_path": "https://image.tmdb.org/t/p/w500/fycMZt242LVjagMByZOLUGbCvv3.png"
            }
        ]
    },
    {
        "id": 3,
        "title": "The Dark Knight",
        "original_title": "The Dark Knight",
        "overview": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
        "release_date": "2008-07-18",
        "vote_average": 9.0,
        "vote_count": 2600000,
        "poster_path": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
        "backdrop_path": "https://media.themoviedb.org/t/p/w1066_and_h600_face/cfT29Im5VDvjE0RpyKOSdCKZal7.jpg",
        "genres": [{"id": 28, "name": "Action"}, {"id": 80, "name": "Crime"}, {"id": 18, "name": "Drama"}],
        "runtime": 152,
        "tagline": "Welcome to a world without rules.",
        "homepage": "https://www.warnerbros.com/movies/dark-knight",
        "imdb_id": "tt0468569",
        "production_companies": [
            {
                "id": 429,
                "name": "DC Comics",
                "logo_path": "https://image.tmdb.org/t/p/w500/2Tc1P3Ac8M479naPp1kYT3izLS5.png"
            }
        ]
    },
    {
        "id": 4,
        "title": "Pulp Fiction",
        "original_title": "Pulp Fiction",
        "overview": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
        "release_date": "1994-10-14",
        "vote_average": 8.9,
        "vote_count": 1900000,
        "poster_path": "https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg",
        "backdrop_path": "https://media.themoviedb.org/t/p/w1066_and_h600_face/suaEOtk1N1sgg2MTM7oZd2cfVp3.jpg",
        "genres": [{"id": 80, "name": "Crime"}, {"id": 18, "name": "Drama"}],
        "runtime": 154,
        "tagline": "Just because you are a character doesn't mean you have character.",
        "homepage": "https://www.miramax.com/movie/pulp-fiction/",
        "imdb_id": "tt0110912",
        "production_companies": [
            {
                "id": 14,
                "name": "Miramax",
                "logo_path": "https://image.tmdb.org/t/p/w500/6p8cfY0qbO5wKIBg0eENyn44qGq.png"
            }
        ]
    },
    {
        "id": 5,
        "title": "Fight Club",
        "original_title": "Fight Club",
        "overview": "An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into much more.",
        "release_date": "1999-10-15",
        "vote_average": 8.8,
        "vote_count": 2100000,
        "poster_path": "https://image.tmdb.org/t/p/w500/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/w1280/hZkgoQYus5vegHoetLkCJzb17zJ.jpg",
        "genres": [{"id": 18, "name": "Drama"}],
        "runtime": 139,
        "tagline": "Mischief. Mayhem. Soap.",
        "homepage": "https://www.foxmovies.com/movies/fight-club",
        "imdb_id": "tt0137523",
        "production_companies": [
            {
                "id": 508,
                "name": "Regency Enterprises",
                "logo_path": "https://image.tmdb.org/t/p/w500/7cxRWzi4LXmVhX4JuhmIuZfCbYO.png"
            }
        ]
    },
    {
        "id": 6,
        "title": "Inception",
        "original_title": "Inception",
        "overview": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
        "release_date": "2010-07-16",
        "vote_average": 8.8,
        "vote_count": 2300000,
        "poster_path": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/w1280/s3TBrRGB1iav7gFOCNx3H31MoES.jpg",
        "genres": [{"id": 28, "name": "Action"}, {"id": 878, "name": "Science Fiction"}, {"id": 53, "name": "Thriller"}],
        "runtime": 148,
        "tagline": "Your mind is the scene of the crime.",
        "homepage": "https://www.warnerbros.com/movies/inception",
        "imdb_id": "tt1375666",
        "production_companies": [
            {
                "id": 923,
                "name": "Legendary Pictures",
                "logo_path": "https://image.tmdb.org/t/p/w500/8Z99GV3a49WQpvoMk55xjhQGDy.png"
            }
        ]
    },
        {
    "id": 7,
    "title": "Parasite",
    "original_title": "기생충",
    "overview": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
    "release_date": "2019-05-30",
    "vote_average": 8.5,
    "vote_count": 1500000,
    "poster_path": "https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg",
    "backdrop_path": "https://image.tmdb.org/t/p/w1280/TU9NIjwzjoKPwQHoHshkFcQUCG.jpg",
    "genres": [{"id": 35, "name": "Comedy"}, {"id": 18, "name": "Drama"}, {"id": 53, "name": "Thriller"}],
    "runtime": 132,
    "tagline": "Act like you own the place.",
    "homepage": "https://www.parasite-movie.com",
    "imdb_id": "tt6751668",
    "production_companies": [
        {
            "id": 7297,
            "name": "CJ Entertainment",
            "logo_path": "https://image.tmdb.org/t/p/w500/5XUJf5P7YqjMc6W5FZ9xxmIYR3t.png"
        }
    ]
    },
    {
    "id": 8,
    "title": "Interstellar",
    "original_title": "Interstellar",
    "overview": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
    "release_date": "2014-11-05",
    "vote_average": 8.4,
    "vote_count": 3100000,
    "poster_path": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
    "backdrop_path": "https://image.tmdb.org/t/p/w1280/rAiYTfKGqDCRIIqo664sY9XZIvQ.jpg",
    "genres": [{"id": 12, "name": "Adventure"}, {"id": 18, "name": "Drama"}, {"id": 878, "name": "Science Fiction"}],
    "runtime": 169,
    "tagline": "Mankind was born on Earth. It was never meant to die here.",
    "homepage": "https://www.warnerbros.com/movies/interstellar",
    "imdb_id": "tt0816692",
    "production_companies": [
        {
            "id": 923,
            "name": "Legendary Pictures",
            "logo_path": "https://image.tmdb.org/t/p/w500/8Z99GV3a49WQpvoMk55xjhQGDy.png"
        }
    ]
    },
    {
    "id": 9,
    "title": "The Matrix",
    "original_title": "The Matrix",
    "overview": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
    "release_date": "1999-03-30",
    "vote_average": 8.2,
    "vote_count": 2200000,
    "poster_path": "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
    "backdrop_path": "https://image.tmdb.org/t/p/w1280/fNG7i7RqMErkcqhohV2a6cV1Ehy.jpg",
    "genres": [{"id": 28, "name": "Action"}, {"id": 878, "name": "Science Fiction"}],
    "runtime": 136,
    "tagline": "Welcome to the Real World.",
    "homepage": "https://www.warnerbros.com/movies/matrix",
    "imdb_id": "tt0133093",
    "production_companies": [
        {
            "id": 79,
            "name": "Village Roadshow Pictures",
            "logo_path": "https://image.tmdb.org/t/p/w500/tfpfNA3F5zD5xTpPSqWqwiqkYPH.png"
        }
    ]
    },
    {
    "id": 10,
    "title": "Forrest Gump",
    "original_title": "Forrest Gump",
    "overview": "The presidencies of Kennedy and Johnson, the events of Vietnam, Watergate, and other historical events unfold through the perspective of an Alabama man with an IQ of 75.",
    "release_date": "1994-07-06",
    "vote_average": 8.5,
    "vote_count": 2300000,
    "poster_path": "https://image.tmdb.org/t/p/w500/saHP97rTPS5eLmrLQEcANmKrsFl.jpg",
    "backdrop_path": "https://media.themoviedb.org/t/p/w1066_and_h600_face/ghgfzbEV7kbpbi1O8eIILKVXEA8.jpg",
    "genres": [{"id": 35, "name": "Comedy"}, {"id": 18, "name": "Drama"}, {"id": 10749, "name": "Romance"}],
    "runtime": 142,
    "tagline": "Life is like a box of chocolates... you never know what you're gonna get.",
    "homepage": "https://www.paramount.com/movies/forrest-gump",
    "imdb_id": "tt0109830",
    "production_companies": [
        {
            "id": 4,
            "name": "Paramount Pictures",
            "logo_path": "https://image.tmdb.org/t/p/w500/fycMZt242LVjagMByZOLUGbCvv3.png"
        }
    ]
    },
    {
    "id": 11,
    "title": "The Lord of the Rings: The Return of the King",
    "original_title": "The Lord of the Rings: The Return of the King",
    "overview": "Gandalf and Aragorn lead the World of Men against Sauron's army to draw his gaze from Frodo and Sam as they approach Mount Doom with the One Ring.",
    "release_date": "2003-12-01",
    "vote_average": 8.5,
    "vote_count": 2100000,
    "poster_path": "https://image.tmdb.org/t/p/w500/rCzpDGLbOoPwLjy3OAm5NUPOTrC.jpg",
    "backdrop_path": "https://media.themoviedb.org/t/p/w1066_and_h600_face/2u7zbn8EudG6kLlBzUYqP8RyFU4.jpg",
    "genres": [{"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}],
    "runtime": 201,
    "tagline": "The eye of the enemy is moving.",
    "homepage": "https://www.warnerbros.com/movies/lord-rings-return-king",
    "imdb_id": "tt0167260",
    "production_companies": [
        {
            "id": 11,
            "name": "New Line Cinema",
            "logo_path": "https://image.tmdb.org/t/p/w500/6FAuASQHybRkZUk08p9PzSs9ezM.png"
        }
    ]
    },
    {
    "id": 12,
    "title": "Whiplash",
    "original_title": "Whiplash",
    "overview": "A promising young drummer enrolls at a cut-throat music conservatory where his dreams of greatness are mentored by an instructor who will stop at nothing to realize a student's potential.",
    "release_date": "2014-10-10",
    "vote_average": 8.5,
    "vote_count": 900000,
    "poster_path": "https://image.tmdb.org/t/p/w500/7fn624j5lj3xTme2SgiLCeuedmO.jpg",
    "backdrop_path": "https://media.themoviedb.org/t/p/w1000_and_h563_face/fzEM34VXnBRy1DdheGEJd4xLezT.jpg",
    "genres": [{"id": 18, "name": "Drama"}, {"id": 10402, "name": "Music"}],
    "runtime": 107,
    "tagline": "The road to greatness can take you to the edge.",
    "homepage": "http://sonyclassics.com/whiplash/",
    "imdb_id": "tt2582802",
    "production_companies": [
        {
            "id": 5,
            "name": "Columbia Pictures",
            "logo_path": "https://image.tmdb.org/t/p/w500/71BqEFAF4V3qjjMPCpLuyJFB9A.png"
        }
    ]
    },
    {
    "id": 13,
    "title": "Spirited Away",
    "original_title": "千と千尋の神隠し",
    "overview": "A young girl, Chihiro, becomes trapped in a strange new world of spirits. When her parents undergo a mysterious transformation, she must call upon the courage she never knew she had to free her family.",
    "release_date": "2001-07-20",
    "vote_average": 8.5,
    "vote_count": 1300000,
    "poster_path": "https://image.tmdb.org/t/p/w500/39wmItIWsg5sZMyRUHLkWBcuVCM.jpg",
    "backdrop_path": "https://media.themoviedb.org/t/p/w1066_and_h600_face/m4TUa2ciEWSlk37rOsjiSIvZDXE.jpg",
    "genres": [{"id": 16, "name": "Animation"}, {"id": 14, "name": "Fantasy"}, {"id": 12, "name": "Adventure"}],
    "runtime": 125,
    "tagline": "The tunnel led Chihiro to a mysterious town...",
    "homepage": "http://movies.disney.com/spirited-away",
    "imdb_id": "tt0245429",
    "production_companies": [
        {
            "id": 10342,
            "name": "Studio Ghibli",
            "logo_path": "https://image.tmdb.org/t/p/w500/9L1SV5lH25Dd0PE1vj4g3dy5Lk.png"
        }
    ]
    },
    {
    "id": 14,
    "title": "The Silence of the Lambs",
    "original_title": "The Silence of the Lambs",
    "overview": "A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer.",
    "release_date": "1991-02-14",
    "vote_average": 8.3,
    "vote_count": 1400000,
    "poster_path": "https://image.tmdb.org/t/p/w500/rplLJ2hPcOQmkFhTqUte0MkEaO2.jpg",
    "backdrop_path": "https://image.tmdb.org/t/p/w1280/mfwq2nMBzArzQ7Y9RKE8SKeeTkg.jpg",
    "genres": [{"id": 80, "name": "Crime"}, {"id": 18, "name": "Drama"}, {"id": 53, "name": "Thriller"}],
    "runtime": 118,
    "tagline": "To enter the mind of a killer she must challenge the mind of a madman.",
    "homepage": "https://www.mgm.com/movies/the-silence-of-the-lambs",
    "imdb_id": "tt0102926",
    "production_companies": [
        {
            "id": 41,
            "name": "Orion Pictures",
            "logo_path": "https://image.tmdb.org/t/p/w500/6bBCE0h7dDsvSgFZJkO1tFJgE3q.png"
        }
    ]
    },
    {
    "id": 15,
    "title": "Avengers: Infinity War",
    "original_title": "Avengers: Infinity War",
    "overview": "The Avengers and their allies must be willing to sacrifice all in an attempt to defeat the powerful Thanos before his blitz of devastation and ruin puts an end to the universe.",
    "release_date": "2018-04-25",
    "vote_average": 8.3,
    "vote_count": 2500000,
    "poster_path": "https://image.tmdb.org/t/p/w500/7WsyChQLEftFiDOVTGkv3hFpyyt.jpg",
    "backdrop_path": "https://media.themoviedb.org/t/p/w1066_and_h600_face/bOGkgRGdhrBYJSLpXaxhXVstddV.jpg",
    "genres": [{"id": 12, "name": "Adventure"}, {"id": 28, "name": "Action"}, {"id": 878, "name": "Science Fiction"}],
    "runtime": 149,
    "tagline": "An entire universe. Once and for all.",
    "homepage": "https://www.marvel.com/movies/avengers-infinity-war",
    "imdb_id": "tt4154756",
    "production_companies": [
        {
            "id": 420,
            "name": "Marvel Studios",
            "logo_path": "https://image.tmdb.org/t/p/w500/hUzeosd33nzE5MCNsZxCGEKTXaQ.png"
        }
    ]
    },
    {
    "id": 16,
    "title": "La La Land",
    "original_title": "La La Land",
    "overview": "While navigating their careers in Los Angeles, a pianist and an actress fall in love while attempting to reconcile their aspirations for the future.",
    "release_date": "2016-12-09",
    "vote_average": 8.0,
    "vote_count": 900000,
    "poster_path": "https://image.tmdb.org/t/p/w500/uDO8zWDhfWwoFdKS4fzkUJt0Rf0.jpg",
    "backdrop_path": "https://media.themoviedb.org/t/p/w1066_and_h600_face/nlPCdZlHtRNcF6C9hzUH4ebmV1w.jpg",
    "genres": [{"id": 35, "name": "Comedy"}, {"id": 18, "name": "Drama"}, {"id": 10402, "name": "Music"}, {"id": 10749, "name": "Romance"}],
    "runtime": 128,
    "tagline": "Here's to the fools who dream.",
    "homepage": "http://www.lalaland.movie/",
    "imdb_id": "tt3783958",
    "production_companies": [
        {
            "id": 2,
            "name": "Walt Disney Pictures",
            "logo_path": "https://image.tmdb.org/t/p/w500/wdrCwmRnLFJhEoH8GSfymY85KHT.png"
        }
    ]
    }
]

@app.get("/movie/{movie_id}")
async def movie_detail(request: Request, movie_id: int, db: Session = Depends(get_db)):
    """Movie detail page"""
    # Récupérer l'utilisateur depuis la session
    current_user = None
    if request.session.get("user_id"):
        current_user = {
            "id": request.session["user_id"],
            "username": request.session["username"]
        }
    
    # Récupérer le film depuis la base de données
    movie = MovieService.get_by_id(db, movie_id)
    if not movie:
        return RedirectResponse("/")
    
    # Récupérer des films similaires (pour l'instant, simplement d'autres films)
    all_movies = MovieService.get_all(db, limit=5)
    similar_movies = [m for m in all_movies if m.id != movie_id][:4]
    
    # Récupérer les commentaires du film
    from backend.services.comment_service import CommentService
    comments = CommentService.get_by_movie(db, movie_id)
    
    return templates.TemplateResponse("movie.html", {
        "request": request,
        "movie": movie,
        "similar_movies": similar_movies,
        "current_user": current_user,
        "comments": comments
    })

@app.post("/movie/{movie_id}/comment")
async def add_comment(
    request: Request,
    movie_id: int,
    content: str = Form(...),
    db: Session = Depends(get_db)
):
    """Ajouter un commentaire"""
    # Vérifier si l'utilisateur est connecté
    if not request.session.get("user_id"):
        return RedirectResponse(f"/movie/{movie_id}?error=login_required", status_code=302)
    
    # Créer le commentaire
    from backend.services.comment_service import CommentService
    from backend.schemas.comment import CommentCreate
    
    comment_data = CommentCreate(
        user_id=request.session["user_id"],
        movie_id=movie_id,
        content=content
    )
    CommentService.create(db, comment_data)
    
    return RedirectResponse(f"/movie/{movie_id}", status_code=302)

@app.get("/movies")
async def movies_page(request: Request, db: Session = Depends(get_db)):
    """Page de tous les films"""
    # Récupérer l'utilisateur depuis la session
    current_user = None
    if request.session.get("user_id"):
        current_user = {
            "id": request.session["user_id"],
            "username": request.session["username"]
        }
    
    # Récupérer tous les films
    all_movies = MovieService.get_all(db)
    
    return templates.TemplateResponse("movies.html", {
        "request": request,
        "movies": all_movies,
        "list_title": "Films",
        "type": "all",
        "current_user": current_user
    })

@app.get("/movies/{type}")
async def movie_list(request: Request, type: str, db: Session = Depends(get_db)):
    """Movie list page by type"""
    # Récupérer l'utilisateur depuis la session
    current_user = None
    if request.session.get("user_id"):
        current_user = {
            "id": request.session["user_id"],
            "username": request.session["username"]
        }
    
    # Récupérer les films selon le type
    if type == "top_rated":
        all_movies = MovieService.get_all(db)
        # Filtrer les films avec une bonne note (à adapter selon votre modèle)
        filtered_movies = all_movies  # TODO: Ajouter un filtre par note si le champ existe
        title = "Top Rated"
    elif type == "watchlist":
        # TODO: Implémenter la récupération de la watchlist de l'utilisateur
        filtered_movies = MovieService.get_all(db, limit=10)
        title = "Your Watchlist"
    else:
        filtered_movies = MovieService.get_all(db)
        title = "Films"
    
    return templates.TemplateResponse("movies.html", {
        "request": request,
        "movies": filtered_movies,
        "list_title": title,
        "type": type,
        "current_user": current_user
    })

@app.get("/search")
async def search_movies(request: Request, q: Optional[str] = None, db: Session = Depends(get_db)):
    """Search movies"""
    # Récupérer l'utilisateur depuis la session
    current_user = None
    if request.session.get("user_id"):
        current_user = {
            "id": request.session["user_id"],
            "username": request.session["username"]
        }
    
    results = []
    if q:
        results = MovieService.search_by_title(db, q)
    
    return templates.TemplateResponse("movies.html", {
        "request": request,
        "movies": results,
        "list_title": f"Search Results for '{q}'" if q else "Search",
        "type": "search",
        "current_user": current_user
    })

# API root
@app.get("/api")
def read_root():
    return {
        "message": "Bienvenue sur RapidoCine API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/debug/movies")
async def debug_movies(db: Session = Depends(get_db)):
    """Debug endpoint to see all movies"""
    all_movies = MovieService.get_all(db)
    return {
        "total_movies": len(all_movies),
        "movies": all_movies,
        "first_8": all_movies[:8]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) 
    