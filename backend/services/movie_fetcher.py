"""
Service pour récupérer les films depuis les APIs OMDB et TMDb
Utilise OMDB pour les données texte et TMDb pour les images HD
"""
import requests
import os
import time
from typing import Optional, Dict, List
from backend.config import get_settings

settings = get_settings()


class MovieFetcherService:
    """Service hybride OMDB + TMDb"""
    
    def __init__(self):
        self.omdb_key = settings.OMDB_API_KEY  # Votre clé: 2b098366
        self.tmdb_key = os.getenv("TMDB_API_KEY", "1b3f624058e45e0bc6160e397b1336e3")  # Votre clé TMDb
    
    def fetch_movie_by_imdb_id(self, imdb_id: str) -> Optional[Dict]:
        """
        Récupère un film par son ID IMDb
        - Données texte depuis OMDB
        - Images HD depuis TMDb
        """
        print(f"🔍 Récupération du film {imdb_id}...")
        
        # 1. Récupérer données de base depuis OMDB
        omdb_data = self._fetch_omdb_data(imdb_id)
        if not omdb_data:
            print(f"❌ Échec OMDB pour {imdb_id}")
            return None
        
        # 2. Extraire les données texte d'OMDB
        movie_data = self._transform_omdb_to_movie(omdb_data)
        
        # 3. Récupérer images HD depuis TMDb
        self._enhance_with_tmdb_images(imdb_id, movie_data)
        
        print(f"✅ Film récupéré: {movie_data['title']}")
        return movie_data
    
    def _fetch_omdb_data(self, imdb_id: str) -> Optional[Dict]:
        """Récupère les données depuis OMDB API"""
        try:
            url = "http://www.omdbapi.com/"
            params = {
                "apikey": self.omdb_key,
                "i": imdb_id,
                "plot": "full"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get("Response") == "True":
                return data
            else:
                print(f"❌ OMDB error: {data.get('Error')}")
                return None
                
        except Exception as e:
            print(f"⚠️ Erreur OMDB: {e}")
            return None
    
    def _enhance_with_tmdb_images(self, imdb_id: str, movie_data: Dict):
        """Améliore les images avec TMDb (poster + backdrop HD)"""
        if not self.tmdb_key:
            print("⚠️  Clé TMDb non configurée, images limitées")
            return
        
        try:
            # Petite pause pour éviter rate limiting
            time.sleep(0.3)
            
            # Chercher film sur TMDb par IMDb ID
            url = f"https://api.themoviedb.org/3/find/{imdb_id}"
            params = {
                "api_key": self.tmdb_key,
                "external_source": "imdb_id",
                "language": "fr-FR"
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                movie_results = data.get("movie_results", [])
                
                if movie_results:
                    tmdb_movie = movie_results[0]
                    
                    # Mettre à jour les URLs d'images avec TMDb HD
                    base_url = "https://image.tmdb.org/t/p"
                    
                    # Backdrop HD (w1280 pour votre site)
                    backdrop_path = tmdb_movie.get("backdrop_path")
                    if backdrop_path:
                        movie_data["backdrop_url"] = f"{base_url}/w1280{backdrop_path}"
                        print(f"   🖼️  Backdrop TMDb ajouté")
                    
                    # Poster HD (w500 pour bonne qualité)
                    poster_path = tmdb_movie.get("poster_path")
                    if poster_path:
                        movie_data["poster_url"] = f"{base_url}/w500{poster_path}"
                        print(f"   🎬  Poster TMDb HD ajouté")
                    
                    # Ajouter aussi la note TMDb si intéressé
                    movie_data["tmdb_rating"] = tmdb_movie.get("vote_average")
                    movie_data["tmdb_votes"] = tmdb_movie.get("vote_count")
                else:
                    print(f"   ℹ️  Aucun résultat TMDb pour {imdb_id}")
            else:
                print(f"   ⚠️  Erreur TMDb HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ⚠️  Exception TMDb: {e}")
            # On continue sans TMDb, on garde les images OMDB
    
    def _transform_omdb_to_movie(self, omdb_data: Dict) -> Dict:
        """Transformer les données OMDB au format de notre base de données"""
        # Conversion de la note
        try:
            vote_average = float(omdb_data.get("imdbRating", "0"))
        except (ValueError, TypeError):
            vote_average = 0.0
        
        # Conversion du nombre de votes
        try:
            vote_count_str = omdb_data.get("imdbVotes", "0").replace(",", "")
            vote_count = int(vote_count_str)
        except (ValueError, TypeError):
            vote_count = 0
        
        # Conversion de la durée
        try:
            runtime_str = omdb_data.get("Runtime", "0 min").split()[0]
            runtime = int(runtime_str)
        except (ValueError, TypeError, IndexError):
            runtime = 0
        
        # URL du poster (OMDB - sera peut-être remplacé par TMDb)
        poster_url = omdb_data.get("Poster")
        if poster_url == "N/A":
            poster_url = None
        
        # Genres
        genres_str = omdb_data.get("Genre", "")
        genres = [g.strip() for g in genres_str.split(",") if g.strip()]
        
        # Extraction de l'année
        year_str = omdb_data.get("Year", "")
        try:
            year = int(year_str[:4]) if year_str else None
        except (ValueError, TypeError):
            year = None
        
        # Construction de l'objet film
        return {
            "imdb_id": omdb_data.get("imdbID"),
            "title": omdb_data.get("Title"),
            "year": year,
            "poster_url": poster_url,  # Provisoire - sera amélioré par TMDb
            "backdrop_url": None,  # Sera rempli par TMDb si disponible
            "plot": omdb_data.get("Plot", ""),
            "genres": ", ".join(genres),  # Format pour votre modèle Movie
            "runtime": runtime,
            "director": omdb_data.get("Director", ""),
            "actors": omdb_data.get("Actors", ""),
            "country": omdb_data.get("Country", ""),
            "language": omdb_data.get("Language", ""),
            "awards": omdb_data.get("Awards", ""),
            "imdb_rating": omdb_data.get("imdbRating"),
            "metascore": omdb_data.get("Metascore"),
            "box_office": omdb_data.get("BoxOffice"),
        }
    
    # Garder vos méthodes existantes pour la compatibilité
    def fetch_movie_by_title(self, title: str) -> Optional[Dict]:
        """Récupérer un film par son titre (utilisation OMDB seulement pour la recherche)"""
        try:
            url = "http://www.omdbapi.com/"
            params = {
                "apikey": self.omdb_key,
                "t": title,
                "plot": "short"
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data.get("Response") == "True":
                movie_data = self._transform_omdb_to_movie(data)
                # Essayer d'améliorer avec TMDb si on a l'ID
                if movie_data.get("imdb_id"):
                    self._enhance_with_tmdb_images(movie_data["imdb_id"], movie_data)
                return movie_data
            return None
        except Exception as e:
            print(f"Erreur recherche par titre: {e}")
            return None
    
    def search_movies(self, query: str) -> List[Dict]:
        """Rechercher des films (OMDB seulement pour les résultats rapides)"""
        try:
            url = "http://www.omdbapi.com/"
            params = {
                "apikey": self.omdb_key,
                "s": query,
                "type": "movie"
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data.get("Response") == "True":
                return data.get("Search", [])
            return []
        except Exception as e:
            print(f"Erreur recherche: {e}")
            return []


# Instance globale pour faciliter l'utilisation
movie_fetcher = MovieFetcherService()