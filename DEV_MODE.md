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

### 3. Initialiser la base de données

```powershell
# Retourner à la racine du projet
cd ..
python -m backend.init_db
```

### 4. Lancer le serveur

```powershell
# Depuis la RACINE du projet (RapidoCine/)
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
