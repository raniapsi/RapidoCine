from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes import (
    movies_router,
    users_router,
    watchlist_router,
    comments_router,
    ratings_router
)

# Créer les tables dans la base de données
Base.metadata.create_all(bind=engine)

# Initialiser l'application FastAPI
app = FastAPI(
    title="RapidoCine API",
    description="API pour l'application de streaming de films RapidoCine",
    version="1.0.0"
)

# Configuration CORS
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routes
app.include_router(movies_router)
app.include_router(users_router)
app.include_router(watchlist_router)
app.include_router(comments_router)
app.include_router(ratings_router)


# Route de base
@app.get("/")
def read_root():
    return {
        "message": "Bienvenue sur l'API RapidoCine",
        "version": "1.0.0",
        "documentation": "/docs"
    }


# Route de santé
@app.get("/health")
def health_check():
    return {"status": "healthy"}

