# RapidoCine - Application Web de Gestion de Séances de Cinéma

Application web moderne développée avec **FastAPI** (backend) et **HTML/CSS/JavaScript** (frontend), déployée avec Docker et orchestrée avec docker-compose.

## 🏗️ Architecture

### Structure du Projet
```
RapidoCine/
├── backend/                 # API FastAPI
│   ├── models/             # Modèles SQLAlchemy (Cinema, Film, Seance)
│   ├── schemas/            # Schémas Pydantic pour validation
│   ├── services/           # Logique métier
│   ├── routers/            # Routes API (cinemas, films, seances)
│   ├── config.py           # Configuration de l'application
│   ├── database.py         # Configuration base de données
│   ├── main.py             # Point d'entrée FastAPI
│   ├── init_db.py          # Script d'initialisation de la BDD
│   ├── requirements.txt    # Dépendances Python
│   └── Dockerfile          # Image Docker pour l'API
│
├── frontend/               # Interface utilisateur
│   ├── index.html          # Page web principale
│   └── Dockerfile          # Image Docker pour le frontend
│
├── docker-compose.yml      # Orchestration des services
├── nginx.conf              # Configuration du reverse proxy
└── .env                    # Variables d'environnement
```

### Services Docker

1. **db** (PostgreSQL 15) - Base de données
   - Port: 5432
   - User: rapidocine
   - Database: rapidocine_db

2. **api** (FastAPI + Uvicorn) - Backend API
   - Port interne: 8000
   - Documentation: http://localhost/api/docs

3. **web** (Nginx) - Frontend
   - Sert le fichier HTML statique

4. **nginx** - Reverse Proxy
   - Port: 80
   - Route `/` → Frontend
   - Route `/api/` → Backend

### Modèle de Données

#### Cinema
- id, nom, adresse, ville, code_postal, latitude, longitude

#### Film
- id, titre, realisateur, genre, duree, date_sortie, synopsis, affiche_url

#### Seance
- id, film_id, cinema_id, horaire, salle, prix, places_disponibles

## 🚀 Installation et Démarrage

### Prérequis
- Docker Desktop installé
- Docker Compose installé

### Lancer l'application

```powershell
# Construire et démarrer tous les services
docker-compose up --build

# En mode détaché (arrière-plan)
docker-compose up --build -d
```

L'application sera accessible sur **http://localhost** ou **http://127.0.0.1**

### Commandes utiles

```powershell
# Arrêter les services
docker-compose down

# Arrêter et supprimer les volumes (données)
docker-compose down -v

# Voir les logs
docker-compose logs -f

# Voir les logs d'un service spécifique
docker-compose logs -f api
docker-compose logs -f db
```

## 📡 API Endpoints

### Films
- `GET /api/films/` - Liste tous les films
- `GET /api/films/{id}` - Détails d'un film
- `GET /api/films/search?titre=xxx` - Recherche par titre
- `GET /api/films/genre/{genre}` - Filtrer par genre
- `POST /api/films/` - Créer un film
- `PUT /api/films/{id}` - Mettre à jour un film
- `DELETE /api/films/{id}` - Supprimer un film

### Cinémas
- `GET /api/cinemas/` - Liste tous les cinémas
- `GET /api/cinemas/{id}` - Détails d'un cinéma
- `GET /api/cinemas/search?ville=xxx` - Recherche par ville
- `POST /api/cinemas/` - Créer un cinéma
- `PUT /api/cinemas/{id}` - Mettre à jour un cinéma
- `DELETE /api/cinemas/{id}` - Supprimer un cinéma

### Séances
- `GET /api/seances/` - Liste toutes les séances
- `GET /api/seances/{id}` - Détails d'une séance
- `GET /api/seances/film/{film_id}` - Séances d'un film
- `GET /api/seances/cinema/{cinema_id}` - Séances d'un cinéma
- `GET /api/seances/date/{date}` - Séances d'une date (format: YYYY-MM-DD)
- `POST /api/seances/` - Créer une séance
- `PUT /api/seances/{id}` - Mettre à jour une séance
- `DELETE /api/seances/{id}` - Supprimer une séance

### Documentation interactive
- Swagger UI: http://localhost/api/docs
- ReDoc: http://localhost/api/redoc

## 🎯 Fonctionnalités

### Frontend (Interface Web)
- ✅ Affichage des statistiques (nombre de films, cinémas, séances)
- ✅ Onglets de navigation (Films, Cinémas, Séances)
- ✅ Recherche de films par titre
- ✅ Recherche de cinémas par ville
- ✅ Recherche de séances par date
- ✅ Affichage en grille responsive
- ✅ Design moderne avec gradient et animations

### Backend (API)
- ✅ Architecture en couches (Models, Schemas, Services, Routers)
- ✅ Validation des données avec Pydantic
- ✅ ORM SQLAlchemy pour PostgreSQL
- ✅ CRUD complet pour toutes les entités
- ✅ Relations entre tables (Foreign Keys)
- ✅ Filtres et recherches avancées
- ✅ Documentation automatique (OpenAPI/Swagger)

## 🔧 Configuration

### Variables d'environnement (.env)
```env
APP_NAME=RapidoCine API
APP_VERSION=1.0.0
DEBUG=True
DATABASE_URL=postgresql://rapidocine:rapidocine123@db:5432/rapidocine_db
```

### Initialisation de la base de données
Au premier démarrage, la base de données est automatiquement initialisée avec des données de test :
- 3 cinémas à Paris
- 4 films variés
- 10 séances réparties sur plusieurs cinémas

## 🏆 Bonnes Pratiques Implémentées

### Architecture
✅ **Separation of Concerns** - Models, Schemas, Services, Routers séparés
✅ **Dependency Injection** - Utilisation de `Depends()` pour la session DB
✅ **Configuration centralisée** - Fichier `config.py` avec Pydantic Settings
✅ **Service Layer Pattern** - Logique métier dans les services

### Code Quality
✅ **Type Hints** - Typage Python complet
✅ **Validation** - Schémas Pydantic pour entrées/sorties
✅ **Error Handling** - HTTPException pour erreurs API
✅ **Documentation** - Docstrings et documentation OpenAPI

### DevOps
✅ **Containerization** - Tous les services dockerisés
✅ **Orchestration** - Docker Compose multi-services
✅ **Reverse Proxy** - Nginx pour routage
✅ **Health Checks** - Vérification de l'état de PostgreSQL
✅ **Volumes** - Persistance des données

### Sécurité
✅ **Environment Variables** - Credentials dans .env
✅ **CORS** - Configuration des origines autorisées
✅ **.dockerignore** - Exclusion des fichiers sensibles

## 📊 Schéma de l'Infrastructure Réseau

```
                    Internet
                        │
                        ▼
                  [Port 80:80]
                        │
                   ┌────┴────┐
                   │  NGINX  │ (Reverse Proxy)
                   │  Proxy  │
                   └────┬────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
    ┌──────┐      ┌─────────┐     ┌──────┐
    │  WEB │      │   API   │     │  DB  │
    │ :80  │      │  :8000  │     │:5432 │
    └──────┘      └─────────┘     └──────┘
        │               │               │
        └───────────────┴───────────────┘
                        │
              [rapidocine_network]
```

## 🎨 Technologies Utilisées

- **Backend**: FastAPI 0.109, Uvicorn, SQLAlchemy 2.0, Pydantic 2.5
- **Base de données**: PostgreSQL 15
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Proxy**: Nginx Alpine
- **Containerization**: Docker, Docker Compose
- **ORM**: SQLAlchemy avec support async
- **Validation**: Pydantic pour schémas et configuration

## 📝 Développement Local (Sans Docker)

```powershell
# Créer un environnement virtuel
python -m venv venv
.\venv\Scripts\activate

# Installer les dépendances
cd backend
pip install -r requirements.txt

# Configurer PostgreSQL localement
# Modifier DATABASE_URL dans .env

# Initialiser la base de données
python -m backend.init_db

# Lancer le serveur
uvicorn backend.main:app --reload
```

## 🐛 Troubleshooting

### La base de données ne démarre pas
```powershell
# Vérifier les logs
docker-compose logs db

# Supprimer les volumes et recréer
docker-compose down -v
docker-compose up --build
```

### L'API ne se connecte pas à la BDD
```powershell
# Vérifier le health check
docker-compose ps

# Le service db doit être "healthy"
```

### Port 80 déjà utilisé
Modifier dans `docker-compose.yml`:
```yaml
nginx:
  ports:
    - "8080:80"  # Utiliser le port 8080 au lieu de 80
```

## 📄 Licence

Projet académique - Télécom SudParis - CSC 8567

---

**Auteur**: Projet RapidoCine
**Date**: Décembre 2025
