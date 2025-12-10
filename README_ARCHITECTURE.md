# RapidoCine - Application Web de Gestion de Séances de Cinéma

Application web moderne développée avec **FastAPI** (backend) et **HTML/CSS/JavaScript** (frontend), déployée avec Docker et orchestrée avec docker-compose.

## Architecture

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

## Installation et Démarrage

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

##  Fonctionnalités

### Frontend (Interface Web)
- Affichage des statistiques (nombre de films, cinémas, séances)
- Onglets de navigation (Films, Cinémas, Séances)
- Recherche de films par titre
- Recherche de cinémas par ville
- Recherche de séances par date
- Affichage en grille responsive
- Design moderne avec gradient et animations

### Backend (API)
- Architecture en couches (Models, Schemas, Services, Routers)
- Validation des données avec Pydantic
- ORM SQLAlchemy pour PostgreSQL
- CRUD complet pour toutes les entités
- Relations entre tables (Foreign Keys)
- Filtres et recherches avancées
- Documentation automatique (OpenAPI/Swagger)

## Fonctionnalités essentielles

- Gestion CRUD complète pour Films, Cinémas et Séances (création, lecture, mise à jour, suppression).
- Recherche et filtres avancés :
  - Recherche par titre, genre, réalisateur pour les films.
  - Recherche par ville/adresse pour les cinémas.
  - Filtre par date, film ou cinéma pour les séances.

## Plan d'action

1. Préparation (30 min)
   - Créer le repo GitHub + structure initiale (backend/, frontend/, docker-compose.yml).
   - Configurer .env et docker-compose.
2. Backend (1h)
   - Modèles SQLAlchemy + schémas Pydantic.
   - Routes / services pour Films, Cinémas, Séances.
   - Tests rapides des endpoints avec curl / Postman.
3. Frontend (45 min)
   - Pages HTML/CSS/JS : index, films, cinémas, séances, détail film.
   - Connexion aux endpoints API.
4. Intégration & Déploiement (30 min)
   - docker-compose up --build, vérifier reverse-proxy Nginx.
   - Ajustements UI/UX et corrections.
5. Finalisation (15 min)
   - Rédiger livrable et captures d'écran, push final sur GitHub.

## Livrable

1. Schéma de la base de données (description / diagramme rapide)
   - Table: cinemas (id, nom, adresse, ville, code_postal, latitude, longitude)
   - Table: films (id, titre, realisateur, genre, duree, date_sortie, synopsis, affiche_url)
   - Table: seances (id, film_id FK, cinema_id FK, horaire DATETIME, salle, prix NUMERIC, places_disponibles INT)

2. Points de terminaison (extraits clés)
   - Films
     - GET /api/films/ — lister
     - GET /api/films/{id} — détail
     - POST /api/films/ — créer
     - PUT /api/films/{id} — mettre à jour
     - DELETE /api/films/{id} — supprimer
   - Cinémas
     - GET /api/cinemas/, GET /api/cinemas/{id}, POST /api/cinemas/, ...
   - Séances
     - GET /api/seances/, GET /api/seances/{id}, GET /api/seances/film/{film_id}, POST /api/seances/, ...
   - (Option) POST /api/reservations/ — créer réservation (si implémentée)

3. Pages du frontend (ce à quoi ressemblera l'interface)
   - Page d'accueil (dashboard) : statistiques (nombre films, cinémas, séances), recherche globale.
   - Page Films : grille de cartes (affiche, titre, genre, bouton détail).
   - Page Film Détail : synopsis.
   - UI : design moderne, responsive, barre de navigation en haut, recherche visible.

4. Fonctionnalités essentielles (récapitulatif)
   - CRUD complet pour les 3 entités.
   - Recherche & filtres.
   - Visualisation des horaires et disponibilité.

5. Plan d'action (tâches concrètes à rendre)
   - Initialiser repo + README.
   - Implémenter models/schemas et endpoints de base.
   - Construire pages frontend principales (index, films, détails).
   - Tester end-to-end localement et packager en Docker.
   - Pusher sur GitHub et fournir lien.

6. Création repo GitHub (instructions rapides)
   - Créer repository public ou privé : rapidocine-groupX
   - Ajouter README, .gitignore, licence si besoin.
   - Push initial : backend/, frontend/, docker-compose.yml.
   - Partager le lien en fin de séance.

7. Nom de groupe
   - RapidoCine

## 🔧 Configuration

### Variables d'environnement (.env)
```env
APP_NAME=RapidoCine API
APP_VERSION=1.0.0
DEBUG=True
DATABASE_URL=postgresql://rapidocine:rapidocine123@db:5432/rapidocine_db
```

## Bonnes Pratiques Implémentées

### Architecture
**Separation of Concerns** - Models, Schemas, Services, Routers séparés
**Dependency Injection** - Utilisation de `Depends()` pour la session DB
**Configuration centralisée** - Fichier `config.py` avec Pydantic Settings
**Service Layer Pattern** - Logique métier dans les services

### Code Quality
**Type Hints** - Typage Python complet
**Validation** - Schémas Pydantic pour entrées/sorties
**Error Handling** - HTTPException pour erreurs API
**Documentation** - Docstrings et documentation OpenAPI

### DevOps
**Containerization** - Tous les services dockerisés
**Orchestration** - Docker Compose multi-services
**Reverse Proxy** - Nginx pour routage
**Health Checks** - Vérification de l'état de PostgreSQL
**Volumes** - Persistance des données

### Sécurité
**Environment Variables** - Credentials dans .env
**CORS** - Configuration des origines autorisées
**.dockerignore** - Exclusion des fichiers sensibles

## Schéma de l'Infrastructure Réseau

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

## Technologies Utilisées

- **Backend**: FastAPI 0.109, Uvicorn, SQLAlchemy 2.0, Pydantic 2.5
- **Base de données**: PostgreSQL 15
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Proxy**: Nginx Alpine
- **Containerization**: Docker, Docker Compose
- **ORM**: SQLAlchemy avec support async
- **Validation**: Pydantic pour schémas et configuration

## Développement Local (Sans Docker)

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

## Troubleshooting

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
