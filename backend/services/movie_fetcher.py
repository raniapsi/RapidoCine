"""
Service pour récupérer les films depuis l'API OMDb
"""
import requests
from typing import Optional, Dict, List
from backend.config import get_settings

settings = get_settings()


class MovieFetcherService:
    """Service pour interagir avec l'API OMDb"""
    
    BASE_URL = "http://www.omdbapi.com/"
    
    @staticmethod
    def fetch_movie_by_title(title: str) -> Optional[Dict]:
        """
        Récupérer un film par son titre depuis OMDb
        
        Args:
            title: Le titre du film à rechercher
            
        Returns:
            Dict avec les données du film ou None si non trouvé
        """
        try:
            params = {
                "apikey": settings.OMDB_API_KEY,
                "t": title,
                "plot": "full"
            }
            
            response = requests.get(MovieFetcherService.BASE_URL, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("Response") == "True":
                return MovieFetcherService._transform_omdb_to_movie(data)
            else:
                print(f"Film non trouvé: {title} - {data.get('Error')}")
                return None
                
        except Exception as e:
            print(f"Erreur lors de la récupération du film '{title}': {str(e)}")
            return None
    
    @staticmethod
    def fetch_movie_by_imdb_id(imdb_id: str) -> Optional[Dict]:
        """
        Récupérer un film par son ID IMDb
        
        Args:
            imdb_id: L'ID IMDb du film (ex: tt0111161)
            
        Returns:
            Dict avec les données du film ou None si non trouvé
        """
        try:
            params = {
                "apikey": settings.OMDB_API_KEY,
                "i": imdb_id,
                "plot": "full"
            }
            
            response = requests.get(MovieFetcherService.BASE_URL, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("Response") == "True":
                return MovieFetcherService._transform_omdb_to_movie(data)
            else:
                print(f"Film non trouvé avec ID {imdb_id}: {data.get('Error')}")
                return None
                
        except Exception as e:
            print(f"Erreur lors de la récupération du film ID '{imdb_id}': {str(e)}")
            return None
    
    @staticmethod
    def search_movies(query: str) -> List[Dict]:
        """
        Rechercher des films par mot-clé
        
        Args:
            query: Le terme de recherche
            
        Returns:
            Liste de films trouvés
        """
        try:
            params = {
                "apikey": settings.OMDB_API_KEY,
                "s": query,
                "type": "movie"
            }
            
            response = requests.get(MovieFetcherService.BASE_URL, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("Response") == "True":
                return data.get("Search", [])
            else:
                print(f"Aucun résultat pour: {query}")
                return []
                
        except Exception as e:
            print(f"Erreur lors de la recherche '{query}': {str(e)}")
            return []
    
    @staticmethod
    def _transform_omdb_to_movie(omdb_data: Dict) -> Dict:
        """
        Transformer les données OMDb au format de notre base de données
        
        Args:
            omdb_data: Les données brutes de OMDb
            
        Returns:
            Dict formaté pour notre modèle Movie
        """
        # Conversion de la note (OMDb utilise /10, nous aussi)
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
        
        # Conversion de la durée (format "142 min" -> 142)
        try:
            runtime_str = omdb_data.get("Runtime", "0 min").split()[0]
            runtime = int(runtime_str)
        except (ValueError, TypeError, IndexError):
            runtime = 0
        
        # URL du poster (OMDb fournit directement l'URL)
        poster_url = omdb_data.get("Poster")
        if poster_url == "N/A":
            poster_url = None
        
        # Genres (format "Drama, Crime" -> liste)
        genres_str = omdb_data.get("Genre", "")
        genres = [g.strip() for g in genres_str.split(",") if g.strip()]
        
        # Construction de l'objet film
        movie_data = {
            "title": omdb_data.get("Title"),
            "original_title": omdb_data.get("Title"),
            "overview": omdb_data.get("Plot", ""),
            "release_date": omdb_data.get("Released", ""),
            "vote_average": vote_average,
            "vote_count": vote_count,
            "poster_path": poster_url,
            "backdrop_path": poster_url,  # OMDb ne fournit pas de backdrop séparé
            "runtime": runtime,
            "tagline": omdb_data.get("Plot", "")[:100] if omdb_data.get("Plot") else "",
            "homepage": None,
            "imdb_id": omdb_data.get("imdbID"),
            "genres": genres,
            "year": omdb_data.get("Year", ""),
            "director": omdb_data.get("Director", ""),
            "actors": omdb_data.get("Actors", ""),
            "country": omdb_data.get("Country", ""),
            "language": omdb_data.get("Language", ""),
            "awards": omdb_data.get("Awards", ""),
        }
        
        return movie_data
