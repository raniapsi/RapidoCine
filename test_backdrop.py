"""Script pour tester le fonctionnement de TMDb"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from backend.services.movie_fetcher import MovieFetcherService

def test_backdrop_fetching():
    print("🧪 Test de récupération des backdrops...")
    
    fetcher = MovieFetcherService()
    
    # Test avec un film spécifique
    test_imdb_id = "tt0133093"  # The Matrix
    
    print(f"1. Test de la clé TMDb...")
    print(f"   Clé TMDb configurée: {'✅ OUI' if fetcher.tmdb_key else '❌ NON'}")
    
    print(f"\n2. Appel API TMDb pour {test_imdb_id}...")
    try:
        import requests
        url = f"https://api.themoviedb.org/3/find/{test_imdb_id}"
        params = {
            "api_key": fetcher.tmdb_key,
            "external_source": "imdb_id"
        }
        response = requests.get(url, params=params, timeout=10)
        print(f"   Statut HTTP: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            movie_results = data.get("movie_results", [])
            print(f"   Résultats trouvés: {len(movie_results)}")
            
            if movie_results:
                movie = movie_results[0]
                print(f"   Titre: {movie.get('title')}")
                print(f"   Backdrop_path: {movie.get('backdrop_path')}")
                print(f"   Poster_path: {movie.get('poster_path')}")
                
                # Construire l'URL complète
                if movie.get("backdrop_path"):
                    backdrop_url = f"https://image.tmdb.org/t/p/w1280{movie['backdrop_path']}"
                    print(f"   🔗 Backdrop URL: {backdrop_url}")
                    
                    # Tester si l'image est accessible
                    img_response = requests.head(backdrop_url, timeout=5)
                    print(f"   Image accessible: {'✅ OUI' if img_response.status_code == 200 else '❌ NON'}")
        else:
            print(f"   ❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    print(f"\n3. Test complet avec MovieFetcherService...")
    movie_data = fetcher.fetch_movie_by_imdb_id(test_imdb_id)
    
    if movie_data:
        print(f"   ✅ Film récupéré: {movie_data['title']}")
        print(f"   📍 Poster URL: {movie_data.get('poster_url', 'N/A')}")
        print(f"   🖼️  Backdrop URL: {movie_data.get('backdrop_url', 'N/A')}")
        
        if movie_data.get("backdrop_url"):
            # Tester l'accès à l'image
            try:
                import requests
                response = requests.head(movie_data["backdrop_url"], timeout=5)
                print(f"   🌐 Backdrop accessible: {'✅ OUI' if response.status_code == 200 else '❌ NON'}")
            except:
                print(f"   🌐 Backdrop accessible: ❌ ERREUR")
        else:
            print(f"   🚨 BACKDROP MANQUANT!")
            
        # Afficher toutes les clés disponibles
        print(f"\n   📋 Clés disponibles dans movie_data:")
        for key in movie_data.keys():
            print(f"      - {key}: {str(movie_data[key])[:50]}...")
    else:
        print(f"   ❌ Échec de récupération du film")

if __name__ == "__main__":
    test_backdrop_fetching()