# RapidoCine - Application Web de Films et Critiques

Application web moderne de type IMDb clone, développée avec **FastAPI** (backend SSR) et **Jinja2** (templates), utilisant **SQLite** en développement et **PostgreSQL** en production.

## Architecture

### Architecture SSR (Server-Side Rendering)

```
┌────────────────────────────────────────┐
│         DÉVELOPPEMENT LOCAL             │
├────────────────────────────────────────┤
│                                        │
│  Browser → http://localhost:8000      │
│      │                                 │
│      ├─→ GET / → FastAPI SSR          │
│      │           └─ templates/        │
│      │               index.html       │
│      │                                 │
│      ├─→ GET /login                   │
│      │   └─ templates/login.html      │
│      │                                 │
│      ├─→ GET /api/* → API REST        │
│      │                                 │
│      └─→ /static/* → CSS/JS/Images    │
│                                        │
│  FastAPI:8000 ← Serveur unique         │
│      ↓                                 │
│  SQLite (rapidocine.db)                │
│                                        │
└────────────────────────────────────────┘
```

### Structure du Projet
```
RapidoCine/
├── backend/                    # API FastAPI + SSR
│   ├── models/                # Modèles SQLAlchemy (ORM)
│   │   ├── user.py           # Utilisateurs
│   │   ├── movie.py          # Films
│   │   ├── rating.py         # Notes
│   │   ├── comment.py        # Commentaires
│   │   └── watchlist.py      # Liste de films
│   │
│   ├── schemas/              # Schémas Pydantic (validation)
│   │   ├── user.py
│   │   ├── movie.py
│   │   ├── rating.py
│   │   ├── comment.py
│   │   └── watchlist.py
│   │
│   ├── services/             # Logique métier
│   │   ├── user_service.py
│   │   ├── movie_service.py
│   │   ├── movie_fetcher.py  # OMDb API
│   │   ├── rating_service.py
│   │   ├── comment_service.py
│   │   └── watchlist_service.py
│   │
│   ├── routers/              # Routes API REST
│   │   ├── users.py
│   │   ├── movies.py
│   │   ├── ratings.py
│   │   ├── comments.py
│   │   └── watchlist.py
│   │
│   ├── config.py             # Configuration (Pydantic Settings)
│   ├── database.py           # SQLAlchemy setup
│   ├── main.py               # Point d'entrée FastAPI (SSR + API)
│   ├── init_db.py            # Script d'init BDD (10 films OMDb)
│   └── requirements.txt      # Dépendances Python
│
├── frontend/                 # Templates et static files
│   ├── templates/           # Jinja2 templates (SSR)
│   │   ├── base.html       # Template parent
│   │   ├── index.html      # Page d'accueil
│   │   ├── login.html      # Connexion
│   │   ├── register.html   # Inscription
│   │   ├── movies.html     # Liste films
│   │   └── movie.html      # Détail film + commentaires
│   │
│   └── static/             # Assets statiques
│       ├── css/           # Styles
│       ├── js/            # Scripts (rating.js, carousel.js)
│       └── images/        # Logos, assets
│
├── .env                    # Variables d'environnement
├── .env.example           # Template .env
├── .gitignore
├── DEV_MODE.md           # Guide développement
├── rapidocine.db         # Base SQLite (dev)
└── README.md
```


##  Installation et Démarrage

### Prérequis
- Python 3.11+
- pip (gestionnaire de paquets Python)

### Installation

**1. Cloner le repository**
```bash
git clone https://github.com/raniapsi/RapidoCine.git
cd RapidoCine
```

**2. Créer un environnement virtuel**
```bash
# Windows
cd backend
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
cd backend
python3 -m venv venv
source venv/bin/activate
```

**3. Installer les dépendances**
```bash
pip install -r requirements.txt
```

**4. Configurer les variables d'environnement**
```bash
# Copier le template
cp .env.example .env

# Éditer .env et ajouter votre clé OMDb
# OMDB_API_KEY=votre_cle_ici
```

**5. Initialiser la base de données**
```bash
# Depuis la racine du projet
python -m backend.init_db
```

Cette commande va :
- Créer `rapidocine.db` (SQLite)
- Créer 3 utilisateurs de test (alice, bob, charlie)
- Importer 10 films depuis OMDb API

**6. Lancer le serveur**
```bash
# Depuis la racine du projet
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Accès à l'application

- **Application** : http://localhost:8000
- **API Documentation** : http://localhost:8000/api/docs
- **Health Check** : http://localhost:8000/health

### Identifiants de test

| Username | Password    |
|----------|-------------|
| alice    | password123 |
| bob      | password123 |
| charlie  | password123 |

## 📡 Routes de l'Application

### Routes SSR (Server-Side Rendering)

**Pages publiques :**
- `GET /` - Page d'accueil (carousel + liste films)
- `GET /movies` - Liste de tous les films
- `GET /movies/top_rated` - Films classés par note
- `GET /movies/watchlist` - Watchlist de l'utilisateur
- `GET /movie/{id}` - Détail d'un film (+ commentaires)
- `GET /search?q=...` - Recherche de films

**Authentification :**
- `GET /login` - Page de connexion
- `POST /login` - Traiter la connexion
- `GET /register` - Page d'inscription
- `POST /register` - Traiter l'inscription
- `GET /logout` - Déconnexion

**Actions utilisateur :**
- `POST /movie/{id}/comment` - Ajouter un commentaire

### API REST Endpoints

**Movies (Films) :**
- `GET /api/movies/` - Liste tous les films
- `GET /api/movies/{id}` - Détails d'un film
- `GET /api/movies/search?title=...` - Recherche par titre
- `POST /api/movies/fetch-from-omdb` - Importer depuis OMDb
- `GET /api/movies/omdb/search?query=...` - Recherche OMDb

**Users (Utilisateurs) :**
- `GET /api/users/` - Liste utilisateurs
- `GET /api/users/{id}` - Détails utilisateur
- `POST /api/users/` - Créer utilisateur
- `POST /api/users/login` - Connexion API

**Ratings (Notes) :**
- `GET /api/ratings/` - Liste toutes les notes
- `GET /api/ratings/user/{user_id}` - Notes d'un utilisateur
- `GET /api/ratings/movie/{movie_id}` - Notes d'un film
- `POST /api/ratings/` - Créer/Mettre à jour une note
- `GET /api/web/rating/{movie_id}` - Note de l'utilisateur connecté

**Comments (Commentaires) :**
- `GET /api/comments/` - Liste tous les commentaires
- `GET /api/comments/user/{user_id}` - Commentaires d'un utilisateur
- `GET /api/comments/movie/{movie_id}` - Commentaires d'un film
- `POST /api/comments/` - Créer un commentaire

**Watchlist :**
- `GET /api/watchlist/` - Liste toutes les entrées
- `GET /api/watchlist/user/{user_id}` - Watchlist d'un utilisateur
- `POST /api/watchlist/` - Ajouter à la watchlist
- `DELETE /api/watchlist/{id}` - Retirer de la watchlist
- `POST /api/web/watchlist/toggle` - Toggle watchlist (UI)

### Documentation interactive
- **Swagger UI** : http://localhost:8000/api/docs
- **ReDoc** : http://localhost:8000/api/redoc


##  Fonctionnalités essentielles

### Fonctionnalités détaillées

#### Authentification

* Inscription : username, nom, prénom, adresse
* Connexion / Déconnexion : username, password
* Une fois connecté, la déconnexion est disponible sur toutes les pages.

#### Page d’accueil

* Affichage des films disponibles
* Ajout d’un film en favoris (watchlist)

#### Page film

* Filtrer par genre (action, comédie, etc.)
* Aperçu des films classés par note IMDb
* Aperçu des notes attribuées par l’ensemble des utilisateurs IMDb (via une API IMDb)

#### Page d’un film

* Aperçu de la description du film
* Attribution de notes
* Visualisation de trois classements :

  * Celui de l’utilisateur
  * Celui de tous les utilisateurs de RapidoCiné
  * Celui d’IMDb
* Possibilité de publier des commentaires sur le film
* Consultation de tous les commentaires du film par les autres utilisateurs de RapidoCiné

#### Page "Mon classement"

* Affichage des films classés selon les notes attribuées par l’utilisateur

#### Page watchlist

* Tous les films mis en favoris par l’utilisateur y sont affichés


##  Plan d'action

1. Préparation 
   - Créer le repo GitHub + structure initiale (backend/, frontend/, docker-compose.yml).
   - Configurer .env et docker-compose.
2. Backend 
   - Modèles SQLAlchemy + schémas Pydantic.
   - Routes / services pour Films, Cinémas, Séances.
   - Tests rapides des endpoints avec curl / Postman.
3. Frontend 
   - Pages HTML/CSS/JS : index, films, cinémas, séances, détail film.
   - Connexion aux endpoints API.

##  Livrable

### 1. Schéma de la base de données

#### Structure des tables

**Table `users` (Utilisateurs)**
```sql
id              INTEGER      PRIMARY KEY
username        VARCHAR(50)  NOT NULL UNIQUE
password_hash   VARCHAR(255) NOT NULL
email           VARCHAR(100) NOT NULL UNIQUE
created_at      DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
```

**Table `movies` (Films)**
```sql
id              INTEGER       PRIMARY KEY
imdb_id         VARCHAR(20)   NOT NULL UNIQUE
title           VARCHAR(200)  NOT NULL
year            INTEGER       NOT NULL
poster_url      VARCHAR(255)  
plot            TEXT          
genres          VARCHAR(255)  
created_at      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP
```

**Table `ratings` (Notes)**
```sql
id              INTEGER   PRIMARY KEY
user_id         INTEGER   NOT NULL → FOREIGN KEY (users.id)
movie_id        INTEGER   NOT NULL → FOREIGN KEY (movies.id)
score           INTEGER   NOT NULL (1-5)
created_at      DATETIME  NOT NULL DEFAULT CURRENT_TIMESTAMP

CONSTRAINT unique_user_movie: UNIQUE(user_id, movie_id)
```

**Table `comments` (Commentaires)**
```sql
id              INTEGER   PRIMARY KEY
user_id         INTEGER   NOT NULL → FOREIGN KEY (users.id)
movie_id        INTEGER   NOT NULL → FOREIGN KEY (movies.id)
content         TEXT      NOT NULL
created_at      DATETIME  NOT NULL DEFAULT CURRENT_TIMESTAMP
```

**Table `watchlist` (Liste de films)**
```sql
id              INTEGER      PRIMARY KEY
user_id         INTEGER      NOT NULL → FOREIGN KEY (users.id)
movie_id        INTEGER      NOT NULL → FOREIGN KEY (movies.id)
status          VARCHAR(20)  NOT NULL DEFAULT 'want_to_watch'
added_at        DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP

CONSTRAINT unique_user_movie_watchlist: UNIQUE(user_id, movie_id)
```

#### Diagramme des relations

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│    USERS     │         │    MOVIES    │_________│   RATINGS    │
├──────────────┤         ├──────────────┤         ├──────────────┤
│ id (PK)      │◄────┐   │ id (PK)      │◄────┐   │ id (PK)      │
│ username     │     │   │ imdb_id      │     │   │ user_id (FK) │
│ password_hash│     │   │ title        │     │   │ movie_id(FK) │
│ email        │     │   │ year         │     │   │ score (1-5)  │
│ created_at   │     │   │ poster_url   │     │   │ created_at   │
└──────────────┘     │   │ plot         │     │   └──────────────┘
       ▲             │   │ genres       │     │
       │             │   │ created_at   │     │
       │             │   └──────────────┘     │
       │             │          ▲             │
       │             │          │             │
       │             │          │             │
┌──────┴───────┐    │   ┌──────┴───────┐    │
│   COMMENTS   │    │   │  WATCHLIST   │    │
├──────────────┤    │   ├──────────────┤    │
│ id (PK)      │    │   │ id (PK)      │    │
│ user_id (FK) ├────┘   │ user_id (FK) ├────┘
│ movie_id(FK) ├────────│ movie_id(FK) ├
│ content      │        │ status       │        
│ created_at   │        │ added_at     │        
└──────────────┘        └──────────────┘        

```

#### Relations entre tables

- **users → ratings** : Un utilisateur peut noter plusieurs films (1:N)
- **users → comments** : Un utilisateur peut commenter plusieurs films (1:N)
- **users → watchlist** : Un utilisateur peut avoir plusieurs films en watchlist (1:N)
- **movies → ratings** : Un film peut avoir plusieurs notes (1:N)
- **movies → comments** : Un film peut avoir plusieurs commentaires (1:N)
- **movies → watchlist** : Un film peut être dans plusieurs watchlists (1:N)

#### Contraintes d'intégrité

- **UNIQUE(user_id, movie_id)** sur `ratings` : Un utilisateur ne peut noter qu'une fois le même film
- **UNIQUE(user_id, movie_id)** sur `watchlist` : Un film ne peut être qu'une fois dans la watchlist d'un utilisateur
- **CASCADE ON DELETE** : Suppression en cascade des notes/commentaires/watchlist si user ou movie supprimé

### 2. Points de terminaison (extraits clés)

#### Films
- `GET /api/movies/` — Lister tous les films
- `GET /api/movies/{id}` — Détail d'un film
- `GET /api/movies/search?title=...` — Rechercher par titre
- `POST /api/movies/fetch-from-omdb` — Importer depuis OMDb API
- `DELETE /api/movies/{id}` — Supprimer un film

#### Utilisateurs
- `GET /api/users/` — Lister tous les utilisateurs
- `GET /api/users/{id}` — Détail d'un utilisateur
- `POST /api/users/` — Créer un utilisateur
- `POST /api/users/login` — Connexion

#### Notes (Ratings)
- `GET /api/ratings/` — Lister toutes les notes
- `GET /api/ratings/movie/{movie_id}` — Notes d'un film
- `POST /api/ratings/` — Créer/Mettre à jour une note
- `GET /api/web/rating/{movie_id}` — Note de l'utilisateur connecté

#### Commentaires
- `GET /api/comments/movie/{movie_id}` — Commentaires d'un film
- `POST /api/comments/` — Créer un commentaire

#### Watchlist
- `GET /api/watchlist/user/{user_id}` — Watchlist d'un utilisateur
- `POST /api/web/watchlist/toggle` — Ajouter/Retirer de la watchlist

### 3. Pages du frontend (interface utilisateur)

- **Page d'accueil (`/`)** : 
  - Carousel de films avec posters
  - Grille de films responsive
  - Filtres par genre
  - Statistiques (nombre de films)

- **Page de connexion (`/login`)** : 
  - Formulaire username/password
  - Lien vers inscription
  - Redirection après authentification

- **Page d'inscription (`/register`)** : 
  - Formulaire username/email/password
  - Validation côté client et serveur

- **Page liste films (`/movies`)** : 
  - Grille de cartes avec poster + titre + genres
  - Bouton détail pour chaque film
  - Filtrage en temps réel

- **Page détail film (`/movie/{id}`)** : 
  - Poster haute résolution
  - Synopsis complet
  - Genres, année, IMDb ID
  - Note IMDb + note moyenne utilisateurs
  - Système de notation 5 étoiles
  - Bouton watchlist (cœur)
  - Section commentaires avec formulaire

- **Page watchlist (`/movies/watchlist`)** : 
  - Liste personnelle de l'utilisateur
  - Boutons pour retirer des films

**Design** : Interface moderne avec gradients, animations CSS, responsive, navigation claire

### 4. Fonctionnalités essentielles (récapitulatif)

- **CRUD complet** : 5 entités (users, movies, ratings, comments, watchlist)
- **Authentification sécurisée** : Sessions avec cookies, hash bcrypt
- **Import automatique** : 10 films depuis OMDb API au démarrage
- **Recherche & filtres** : Par titre et par genre
- **Système de notation** : 5 étoiles interactives avec persistance
- **Commentaires** : Publication et affichage chronologique
- **Watchlist personnelle** : Toggle avec feedback visuel
- **Enrichissement OMDb** : Notes IMDb, posters, synopsis en anglais
- **API REST documentée** : Swagger UI + ReDoc automatique
- **SSR performant** : Jinja2 pour rendu côté serveur

### 5. Plan d'action (tâches concrètes réalisées)

 **Phase 1 : Initialisation**
- Repository GitHub créé et structuré (backend/, frontend/)
- Configuration .env avec OMDb API key
- SQLite configuré pour développement

 **Phase 2 : Backend**
- 5 modèles SQLAlchemy avec relations (users, movies, ratings, comments, watchlist)
- 5 routeurs API REST (30+ endpoints)
- Script init_db.py pour import automatique 10 films

 **Phase 3 : Frontend**
- 7 templates Jinja2 (base, index, login, register, movies, movie, top_rated)
- CSS moderne avec gradients et animations
- JavaScript vanilla (rating.js, carousel.js)
- Design responsive

 **Phase 4 : Intégration**
- OMDb API intégrée (MovieFetcherService)
- Système de sessions (SessionMiddleware)
- Tests manuels de tous les endpoints
- Watchlist connectée frontend ↔ backend
- Documentation Swagger UI générée automatiquement

### 6. Repository GitHub

**Nom** : `RapidoCine`  
**URL** : https://github.com/raniapsi/RapidoCine  
**Visibilité** : Public  

**Contenu du repository** :
- `backend/` : API FastAPI + modèles + services + routeurs
- `frontend/` : Templates Jinja2 + static files (CSS/JS)
- `.env.example` : Template de configuration
- `DEV_MODE.md` : Guide développement détaillé
- `README.md` : Documentation utilisateur
- `README_ARCHITECTURE.md` : Documentation technique (ce fichier)
- `.gitignore` : Python, SQLite, venv, __pycache__

### 7. Nom de groupe

**RapidoCine** - Projet CSC 8567 Télécom SudParis

## 🔧 Configuration

### Variables d'environnement (.env)

```env
# Application
DATABASE_URL=sqlite:///./rapidocine.db
DEBUG=True
OMDB_API_KEY=code_cle  # ← Remplacez par votre vraie clé
CORS_ORIGINS=["http://localhost","http://localhost:8000","http://localhost:3000"]

# Base de données (SQLite en développement)
DATABASE_URL=sqlite:///./rapidocine.db

# API OMDb (clé gratuite sur http://www.omdbapi.com/apikey.aspx)
OMDB_API_KEY=votre_cle_api_ici

# CORS (origines autorisées)
CORS_ORIGINS=http://localhost,http://localhost:8000,http://127.0.0.1
```

### Obtenir une clé OMDb API (gratuit)

1. Rendez-vous sur http://www.omdbapi.com/apikey.aspx
2. Choisissez le plan **FREE** (1000 requêtes/jour)
3. Entrez votre email
4. Vérifiez votre email et activez la clé
5. Copiez la clé dans votre fichier `.env`

##  Flux de Données

```
┌─────────────────────────────────────────────┐
│           ARCHITECTURE SSR                  │
├─────────────────────────────────────────────┤
│                                             │
│  1. Browser → FastAPI :8000                 │
│     GET /movie/1                            │
│                                             │
│  2. FastAPI → MovieService                  │
│     get_by_id(1)                            │
│                                             │
│  3. MovieService → SQLite                   │
│     SELECT * FROM movies WHERE id=1         │
│                                             │
│  4. SQLite → MovieService                   │
│     {id:1, title:"Matrix", ...}             │
│                                             │
│  5. FastAPI → Jinja2                        │
│     templates.TemplateResponse(             │
│       "movie.html",                         │
│       {"movie": movie_data}                 │
│     )                                       │
│                                             │
│  6. Jinja2 → Browser                        │
│     HTML complet rendu côté serveur         │
│                                             │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│         INTERACTION AJAX (Ratings)          │
├─────────────────────────────────────────────┤
│                                             │
│  1. Click étoile → rating.js                │
│                                             │
│  2. fetch('/api/ratings/', {                │
│       method: 'POST',                       │
│       body: {user_id, movie_id, score}      │
│     })                                      │
│                                             │
│  3. FastAPI → RatingService.create()        │
│                                             │
│  4. Response JSON {user_rating: 4, ...}     │
│                                             │
│  5. rating.js → Update UI (★★★★☆)         │
│                                             │
└─────────────────────────────────────────────┘
```

##  Technologies Utilisées

### Backend
- **Framework** : FastAPI 0.109 (async/await)
- **Serveur ASGI** : Uvicorn
- **ORM** : SQLAlchemy 2.0
- **Validation** : Pydantic 2.5
- **Templates** : Jinja2 3.1
- **Sessions** : Starlette SessionMiddleware
- **Passwords** : bcrypt
- **HTTP Client** : httpx (requêtes OMDb)
- **Configuration** : python-dotenv

### Base de données
- **Développement** : SQLite 3
- **Production** : PostgreSQL 15 (optionnel)

### Frontend
- **Templates** : Jinja2 (SSR)
- **HTML** : HTML5 sémantique
- **CSS** : CSS3 Vanilla (gradients, animations)
- **JavaScript** : Vanilla JS (rating.js, carousel.js)
- **Icons** : Font Awesome 6

### API Externe
- **OMDb API** : Import automatique films
  - Base URL : http://www.omdbapi.com/
  - Limite gratuite : 1000 req/jour
  - Données : titre, année, poster, synopsis, genres, IMDb ID

##  Commandes Utiles


### Tester l'API

```bash
# Lister les films
curl http://localhost:8000/api/movies/

# Rechercher un film
curl "http://localhost:8000/api/movies/search?title=Matrix"

# Créer un utilisateur
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"test123"}'
```

##  Troubleshooting

### Erreur `ModuleNotFoundError: No module named 'fastapi'`

```bash
# Vérifier que l'environnement virtuel est activé
which python  # doit pointer vers venv/bin/python

# Réinstaller les dépendances
pip install -r backend/requirements.txt
```

### Erreur `OMDb API key invalid`

1. Vérifiez que votre clé est dans `.env`
2. Vérifiez que vous avez activé la clé via l'email reçu
3. Vérifiez que vous n'avez pas dépassé 1000 requêtes/jour

```bash
# Tester la clé manuellement
curl "http://www.omdbapi.com/?apikey=VOTRE_CLE&t=Matrix"
```

### La base de données est vide

```bash
# Supprimer et réinitialiser
rm rapidocine.db
python -m backend.init_db
```

### Port 8000 déjà utilisé

```bash
# Trouver le processus
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# Tuer le processus ou changer de port
uvicorn backend.main:app --reload --port 8001
```

### Les templates ne se rechargent pas

Uvicorn avec `--reload` recharge uniquement le code Python, pas les templates.
Rafraîchissez manuellement le navigateur (Ctrl+R).

### Erreur CORS en développement

Vérifiez `backend/config.py` :
```python
CORS_ORIGINS: list = ["http://localhost:8000", "*"]
```

## Licence

Projet académique - Télécom SudParis - CSC 8567

---

**Auteur**: Projet RapidoCine
**Date**: Décembre 2025