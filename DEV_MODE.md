# RapidoCine - Mode Développement (Sans Docker)

## Installation

### 1. Créer un environnement virtuel

```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
```

### 2. Installer les dépendances

```powershell
pip install -r requirements.txt
```

### 4. Initialiser la base de données

```powershell
python -m backend.init_db
```

Cette commande va :
- Créer la base de données SQLite
- Créer 3 utilisateurs de test (alice, bob, charlie)
- Récupérer 10 films depuis l'API OMDb

### 5. Lancer le serveur

#### b. Obtenir une clé OMDb API

1. Rendez-vous sur [http://www.omdbapi.com/apikey.aspx](http://www.omdbapi.com/apikey.aspx)
2. Choisissez le plan **FREE** (1000 requêtes/jour)
3. Entrez votre email
4. Vérifiez votre email et activez la clé
5. Copiez votre clé API dans `.env` pour `OMDB_API_KEY`

Votre fichier `.env` devrait ressembler à :

```env
APP_NAME=RapidoCine
DATABASE_URL=sqlite:///./rapidocine.db
CORS_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
OMDB_API_KEY=1ba53e51
```

### 4. Initialiser la base de données

```powershell
python -m backend.init_db
```

### 4. Lancer le serveur

```powershell
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

## Accès

- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/api/docs
- **Health check**: http://localhost:8000/health

## Frontend

Pour tester le frontend, ouvrez simplement `frontend/index.html` dans votre navigateur.

**Note**: Modifiez dans `index.html` la ligne:
```javascript
const API_URL = 'http://localhost:8000/api';
```

## Identifiants de test

- Username: `alice` | Password: `password123`
- Username: `bob` | Password: `password123`
- Username: `charlie` | Password: `password123`

## Structure de la base de données

En mode développement, on utilise **SQLite** (fichier `rapidocine.db`) au lieu de PostgreSQL.
