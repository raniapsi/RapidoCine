from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from backend.config import get_settings
from backend.database import engine, Base
from backend.routers import users_router, movies_router, ratings_router, comments_router, watchlist_router

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

movies_data = [
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

# Include API routers
app.include_router(users_router, prefix="/api")
app.include_router(movies_router, prefix="/api")
app.include_router(ratings_router, prefix="/api")
app.include_router(comments_router, prefix="/api")
app.include_router(watchlist_router, prefix="/api")

# Your frontend routes
@app.get("/")
async def home(request: Request):
    """Home page with carousel and movie list"""
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "popular_movies": movies_data[:8],  
        "featured_movies": movies_data
    })

@app.get("/movie/{movie_id}")
async def movie_detail(request: Request, movie_id: int):
    """Movie detail page"""
    movie = next((m for m in movies_data if m["id"] == movie_id), None)
    if not movie:
        return RedirectResponse("/")
    
    similar_movies = [m for m in movies_data if m["id"] != movie_id][:4]
    
    return templates.TemplateResponse("movie.html", {
        "request": request,
        "movie": movie,
        "similar_movies": similar_movies
    })

@app.get("/movies/{type}")
async def movie_list(request: Request, type: str):
    """Movie list page by type"""
    if type == "top_rated":
        filtered_movies = [m for m in movies_data if m["vote_average"] >= 8.5]
        title = "Top Rated"
    elif type == "wishlist":
        filtered_movies = movies_data[-2:].copy()
        for movie in filtered_movies:
            movie["release_date"] = "2024"
        title = "Your Wishlist"
    else:
        filtered_movies = movies_data
        title = "Popular"
    
    return templates.TemplateResponse("movies.html", {
        "request": request,
        "movies": filtered_movies,
        "list_title": title,
        "type": type
    })

@app.get("/search")
async def search_movies(request: Request, q: Optional[str] = None):
    """Search movies"""
    results = []
    if q:
        results = [m for m in movies_data if q.lower() in m["title"].lower()]
    
    return templates.TemplateResponse("movies.html", {
        "request": request,
        "movies": results,
        "list_title": f"Search Results for '{q}'" if q else "Search",
        "type": "search"
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
async def debug_movies():
    """Debug endpoint to see all movies"""
    return {
        "total_movies": len(movies_data),
        "movies": movies_data,
        "first_8": movies_data[:8]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) 
    