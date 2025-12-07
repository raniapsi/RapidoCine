"""Script d'initialisation de la base de données avec des données de test"""
import sys
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.database import SessionLocal, engine, Base
from backend.models import User, Movie, Rating, Comment, Watchlist
from backend.services import UserService
from backend.services.movie_fetcher import MovieFetcherService


def init_db():
    """Initialiser la base de données avec des données de test"""
    
    # Créer les tables
    Base.metadata.create_all(bind=engine)
    
    # Créer une session
    db = SessionLocal()
    
    try:
        # Vérifier si des données existent déjà
        if db.query(User).count() > 0:
            print("La base de données contient déjà des données.")
            return
        
        # Créer des utilisateurs
        users_data = [
            {"username": "alice", "email": "alice@example.com", "password": "password123"},
            {"username": "bob", "email": "bob@example.com", "password": "password123"},
            {"username": "charlie", "email": "charlie@example.com", "password": "password123"},
        ]
        
        users = []
        for user_data in users_data:
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                password_hash=UserService.hash_password(user_data["password"])
            )
            db.add(user)
            users.append(user)
        db.commit()
        
        # Créer des films depuis OMDb API
        print("📥 Récupération des films depuis OMDb API...")
        
        # Liste des IDs IMDb de films populaires à importer
        imdb_ids = [
            "tt0133093",  # The Matrix
            "tt0111161",  # The Shawshank Redemption
            "tt0068646",  # The Godfather
            "tt0468569",  # The Dark Knight
            "tt0816692",  # Interstellar
            "tt0110912",  # Pulp Fiction
            "tt0109830",  # Forrest Gump
            "tt1375666",  # Inception
            "tt0137523",  # Fight Club
            "tt0167260",  # The Lord of the Rings: The Return of the King
        ]
        
        movies = []
        for imdb_id in imdb_ids:
            try:
                movie_data = MovieFetcherService.fetch_movie_by_imdb_id(imdb_id)
                if movie_data:
                    # Extraire l'année du champ year (peut être "1999" ou "1999-2001")
                    year_str = movie_data.get("year", "0")
                    try:
                        year = int(year_str[:4]) if year_str else None
                    except (ValueError, TypeError):
                        year = None
                    
                    movie = Movie(
                        imdb_id=movie_data["imdb_id"],
                        title=movie_data["title"],
                        year=year,
                        poster_url=movie_data["poster_path"],
                        plot=movie_data["overview"],
                        genres=", ".join(movie_data.get("genres", []))
                    )
                    db.add(movie)
                    movies.append(movie)
                    print(f"   ✓ {movie_data['title']} ({year or 'N/A'})")
                else:
                    print(f"   ✗ Impossible de récupérer le film avec ID {imdb_id}")
            except Exception as e:
                print(f"   ✗ Erreur pour {imdb_id}: {str(e)}")
        
        # Si aucun film n'a pu être récupéré depuis OMDb, utiliser des données de fallback
        if not movies:
            print("⚠️  Échec de récupération depuis OMDb, utilisation de données de secours...")
            movies_fallback = [
                Movie(
                    imdb_id="tt0133093",
                    title="The Matrix",
                    year=1999,
                    poster_url="https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg",
                    plot="Un pirate informatique apprend la vraie nature de sa réalité et son rôle dans la guerre contre ses contrôleurs.",
                    genres="Action, Sci-Fi"
                ),
                Movie(
                    imdb_id="tt0111161",
                    title="The Shawshank Redemption",
                    year=1994,
                    poster_url="https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_SX300.jpg",
                    plot="Deux hommes emprisonnés se lient d'amitié sur plusieurs années.",
                    genres="Drama"
                ),
                Movie(
                    imdb_id="tt0068646",
                    title="The Godfather",
                    year=1972,
                    poster_url="https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg",
                    plot="Le patriarche vieillissant d'une dynastie du crime organisé transfère le contrôle de son empire clandestin à son fils réticent.",
                    genres="Crime, Drama"
                ),
                Movie(
                    imdb_id="tt0468569",
                    title="The Dark Knight",
                    year=2008,
                    poster_url="https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_SX300.jpg",
                    plot="Lorsque la menace connue sous le nom de Joker fait des ravages sur les habitants de Gotham, Batman doit accepter l'un des plus grands tests psychologiques.",
                    genres="Action, Crime, Drama"
                ),
                Movie(
                    imdb_id="tt0816692",
                    title="Interstellar",
                    year=2014,
                    poster_url="https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg",
                    plot="Une équipe d'explorateurs voyage à travers un trou de ver dans l'espace pour assurer la survie de l'humanité.",
                    genres="Adventure, Drama, Sci-Fi"
                )
            ]
            
            for movie in movies_fallback:
                db.add(movie)
            movies = movies_fallback
        
        db.commit()
        
        # Créer des notes
        ratings_data = [
            {"user_id": 1, "movie_id": 1, "score": 5},
            {"user_id": 1, "movie_id": 2, "score": 5},
            {"user_id": 1, "movie_id": 3, "score": 4},
            {"user_id": 2, "movie_id": 1, "score": 4},
            {"user_id": 2, "movie_id": 4, "score": 5},
            {"user_id": 2, "movie_id": 5, "score": 5},
            {"user_id": 3, "movie_id": 2, "score": 5},
            {"user_id": 3, "movie_id": 3, "score": 5},
            {"user_id": 3, "movie_id": 5, "score": 4},
        ]
        
        for rating_data in ratings_data:
            rating = Rating(**rating_data)
            db.add(rating)
        db.commit()
        
        # Créer des commentaires
        comments_data = [
            {"user_id": 1, "movie_id": 1, "content": "Un chef-d'œuvre absolu ! Les effets spéciaux ont révolutionné le cinéma."},
            {"user_id": 2, "movie_id": 1, "content": "Incroyable film, je l'ai regardé 5 fois et je découvre toujours quelque chose de nouveau."},
            {"user_id": 1, "movie_id": 2, "content": "L'un des meilleurs films dramatiques de tous les temps. Très émouvant."},
            {"user_id": 3, "movie_id": 2, "content": "Morgan Freeman et Tim Robbins sont parfaits dans ce film."},
            {"user_id": 2, "movie_id": 4, "content": "Heath Ledger a donné la meilleure performance de Joker jamais vue !"},
            {"user_id": 3, "movie_id": 5, "content": "Visuellement époustouflant avec une histoire profonde sur l'amour et le temps."},
        ]
        
        for comment_data in comments_data:
            comment = Comment(**comment_data)
            db.add(comment)
        db.commit()
        
        # Créer des watchlists
        watchlist_data = [
            {"user_id": 1, "movie_id": 4, "status": "TO_WATCH"},
            {"user_id": 1, "movie_id": 5, "status": "TO_WATCH"},
            {"user_id": 2, "movie_id": 2, "status": "WATCHED"},
            {"user_id": 2, "movie_id": 3, "status": "TO_WATCH"},
            {"user_id": 3, "movie_id": 1, "status": "WATCHED"},
            {"user_id": 3, "movie_id": 4, "status": "WATCHING"},
        ]
        
        for wl_data in watchlist_data:
            watchlist = Watchlist(**wl_data)
            db.add(watchlist)
        db.commit()
        
        print("✅ Base de données initialisée avec succès!")
        print(f"   - {len(users)} utilisateurs créés")
        print(f"   - {len(movies)} films créés")
        print(f"   - {len(ratings_data)} notes créées")
        print(f"   - {len(comments_data)} commentaires créés")
        print(f"   - {len(watchlist_data)} entrées de watchlist créées")
        print("\n📝 Identifiants de test:")
        print("   - Username: alice | Password: password123")
        print("   - Username: bob | Password: password123")
        print("   - Username: charlie | Password: password123")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
