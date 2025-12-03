from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import get_settings
from backend.database import engine, Base
from backend.routers import users_router, movies_router, ratings_router, comments_router, watchlist_router

# Créer les tables
Base.metadata.create_all(bind=engine)

# Configuration
settings = get_settings()

# Initialisation de l'application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API pour la gestion de films et watchlist",
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

# Inclusion des routers
app.include_router(users_router, prefix="/api")
app.include_router(movies_router, prefix="/api")
app.include_router(ratings_router, prefix="/api")
app.include_router(comments_router, prefix="/api")
app.include_router(watchlist_router, prefix="/api")


@app.get("/")
def read_root():
    return {
        "message": "Bienvenue sur RapidoCine API",
        "version": settings.APP_VERSION,
        "docs": "/api/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
