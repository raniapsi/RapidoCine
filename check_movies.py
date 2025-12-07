"""Script pour vérifier les films dans la base de données"""
from backend.database import SessionLocal
from backend.models import Movie

db = SessionLocal()
movies = db.query(Movie).all()

print(f"\n{'='*60}")
print(f"📊 VÉRIFICATION DES FILMS DANS LA BASE DE DONNÉES")
print(f"{'='*60}\n")

print(f"Nombre total de films: {len(movies)}\n")

if movies:
    print("Liste des films:")
    print("-" * 60)
    for movie in movies:
        print(f"{movie.id}. {movie.title} ({movie.year})")
        print(f"   IMDb ID: {movie.imdb_id}")
        print(f"   Genres: {movie.genres}")
        print(f"   Description: {movie.plot[:80] if movie.plot else 'N/A'}...")
        print()
    
    print(f"{'='*60}")
    print("✅ Ces films viennent de l'API OMDb si vous voyez 10 films")
    print("   avec des descriptions complètes en anglais.")
    print(f"{'='*60}\n")
else:
    print("❌ Aucun film trouvé dans la base de données!")
    print("   Exécutez: python backend/init_db.py\n")

db.close()
