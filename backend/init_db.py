"""Script d'initialisation de la base de données avec des données de test"""
import sys
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.database import SessionLocal, engine, Base
from backend.models import User, Movie, Rating, Comment, Watchlist
from backend.services import UserService
from backend.services.movie_fetcher import MovieFetcherService  # Import correct


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
            # Option: supprimer et recréer pour les tests
            # db.query(Movie).delete()
            # db.commit()
            # print("Anciens films supprimés, recréation...")
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
        
        # Créer des films depuis OMDb API + TMDb
        print("📥 Récupération des films depuis APIs (OMDb + TMDb)...")
        
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
            "tt0108052",
            "tt0114369",  # Se7en
            "tt0099685",  # Goodfellas
            "tt0102926",  # The Silence of the Lambs
            "tt0088763",  # Back to the Future
            "tt0118799",  # Life Is Beautiful
            "tt0120815",  # Saving Private Ryan
            "tt0076759",  # Star Wars: Episode IV - A New Hope
            "tt0103064",  # Terminator 2: Judgment Day
            "tt0082971",  # Raiders of the Lost Ark
            "tt0095765",  # Cinema Paradiso
            "tt0047478",  # Seven Samurai
            "tt0038650",  # It's a Wonderful Life
            "tt0056058",  # Harakiri
            "tt0110413",  # Léon: The Professional
            "tt0021749",  # City Lights
            "tt0095327",  # Grave of the Fireflies
            "tt0081505",  # The Shining
            "tt0054215",  # Psycho
            "tt0047396",  # Rear Window
            "tt0078748",  # Alien
            "tt0087843",  # Once Upon a Time in America
            "tt0110357",  # The Lion King
            "tt0209144",  # Memento
            "tt0120586",  # American History X
            "tt0080684",  # Star Wars: Episode V - The Empire Strikes Back
            "tt0114814",  # The Usual Suspects
            "tt0057012",  # Dr. Strangelove
            "tt0078788",  # Apocalypse Now
            "tt0043014",  # Sunset Boulevard
            "tt0093058",  # Full Metal Jacket
            "tt1853728",  # Django Unchained
            "tt0407887",  # The Departed
            "tt0482571",  # The Prestige
            "tt0112573",  # Braveheart
            "tt0114709",  # Toy Story
            "tt0245429",  # Spirited Away
            "tt0172495",  # Gladiator
            "tt0120689",  # The Green Mile
            "tt0317248",  # City of God
            "tt0086190",  # Star Wars: Episode VI - Return of the Jedi
            "tt0105236",  # Reservoir Dogs
            "tt1675434",  # The Intouchables
            "tt0060196",  # The Good, the Bad and the Ugly
            "tt0052357",  # Vertigo
            "tt0027977",  # Modern Times
            "tt0064116",
            "tt0107290",  # Jurassic Park (1993) - Classique Spielberg
            "tt0119217",  # Good Will Hunting (1997) - Drame brillant
            "tt0120382",  # The Truman Show (1998) - Satire géniale
            "tt0253474",  # The Pianist (2002) - Chef-d'œuvre historique
            "tt0268978",  # A Beautiful Mind (2001) - Drame biographique
            "tt0289879",  # The Butterfly Effect (2004) - Sci-fi psychologique
            "tt0364569", 
            "tt0758758",
        ]
        
        # CRÉER L'INSTANCE DU FETCHER
        movie_fetcher = MovieFetcherService()
        
        movies = []
        for imdb_id in imdb_ids:
            try:
                # APPEL CORRECT : utiliser l'instance
                movie_data = movie_fetcher.fetch_movie_by_imdb_id(imdb_id)
                if movie_data:
                    # Utiliser l'année déjà extraite par le fetcher
                    year = movie_data.get("year")
                    
                    movie = Movie(
                        imdb_id=movie_data["imdb_id"],
                        title=movie_data["title"],
                        year=year if year else 2000,
                        poster_url=movie_data.get("poster_url"),
                        backdrop_url=movie_data.get("backdrop_url"),  # NOUVEAU!
                        plot=movie_data.get("plot", ""),
                        genres=movie_data.get("genres", "")
                    )
                    db.add(movie)
                    movies.append(movie)
            except Exception as e:
                import traceback
                traceback.print_exc()
        
        # Si aucun film n'a pu être récupéré depuis les APIs
        if not movies:
            print("⚠️  Échec de récupération depuis les APIs, utilisation de données de secours...")
            # Même les fallback devraient avoir des backdrops maintenant
            movies_fallback = [
                Movie(
                    imdb_id="tt0133093",
                    title="The Matrix",
                    year=1999,
                    poster_url="https://image.tmdb.org/t/p/w500/pEoqbqtLc4CcwDUDqxmEDSWpWTZ.jpg",  # Poster TMDb
                    backdrop_url="https://image.tmdb.org/t/p/w1280/tlm8UkiQsitc8rSuIAscQDCnP8d.jpg",  # Backdrop TMDb
                    plot="Un pirate informatique apprend la vraie nature de sa réalité et son rôle dans la guerre contre ses contrôleurs.",
                    genres="Action, Sci-Fi"
                ),
                Movie(
                    imdb_id="tt0111161",
                    title="The Shawshank Redemption",
                    year=1994,
                    poster_url="https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
                    backdrop_url="https://image.tmdb.org/t/p/w1280/kXfqcdQKsToO0OUXHtrrN2dbJA4.jpg",
                    plot="Deux hommes emprisonnés se lient d'amitié sur plusieurs années.",
                    genres="Drama"
                ),
                # ... ajouter les autres avec backdrops
            ]
            
            for movie in movies_fallback:
                db.add(movie)
            movies = movies_fallback
        
        db.commit()
        
        # [Le reste de votre code pour ratings, comments, watchlist reste identique]
        # Créer des notes
        ratings_data = [
            {"user_id": 1, "movie_id": 1, "score": 5},
            # ... votre code existant
        ]
        
        for rating_data in ratings_data:
            rating = Rating(**rating_data)
            db.add(rating)
        db.commit()
        
        # Créer des commentaires
        comments_data = [
            {"user_id": 1, "movie_id": 1, "content": "Un chef-d'œuvre absolu ! Les effets spéciaux ont révolutionné le cinéma."},
            # ... votre code existant
        ]
        
        for comment_data in comments_data:
            comment = Comment(**comment_data)
            db.add(comment)
        db.commit()
        
        # Créer des watchlists
        watchlist_data = [
            {"user_id": 1, "movie_id": 4, "status": "TO_WATCH"},
            # ... votre code existant
        ]
        
        for wl_data in watchlist_data:
            watchlist = Watchlist(**wl_data)
            db.add(watchlist)
        db.commit()
        
        # VÉRIFICATION FINALE
        print("\n" + "="*50)
        print("✅ Base de données initialisée avec succès!")
        print(f"   - {len(users)} utilisateurs créés")
        print(f"   - {len(movies)} films créés")
        
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