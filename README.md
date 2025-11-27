# 🎬 RapidoCine

Application web de streaming de films avec système de watchlist, commentaires et notes.

## 📋 Description du Projet

RapidoCine est une plateforme web permettant aux utilisateurs de :
- Consulter une bibliothèque de films
- Créer et gérer leur watchlist personnelle
- Noter et commenter les films
- S'authentifier de manière sécurisée

## 🗄️ Base de Données

Le projet utilise PostgreSQL avec le schéma suivant :
- **Users** : Gestion des utilisateurs (id, email, username, password, created_at)
- **Movies** : Catalogue de films (id, title, description, genre, release_date, duration)
- **Watchlist** : Liste de films à regarder par utilisateur (user_id, movie_id, added_at)
- **Comments** : Commentaires sur les films (id, user_id, movie_id, content, created_at)
- **Ratings** : Notes des films (id, user_id, movie_id, score, created_at)

## 🛠️ Stack Technique

### Backend
- **FastAPI** : Framework web moderne et performant
- **SQLAlchemy** : ORM pour la gestion de la base de données
- **PostgreSQL** : Base de données relationnelle
- **Alembic** : Gestion des migrations
- **JWT** : Authentification sécurisée

## 🚀 Installation

### Prérequis
- Python 3.12+
- PostgreSQL 15+
- Git

### Installation locale (WSL/Linux)

1. **Cloner le repository**
```bash
git clone https://github.com/raniapsi/RapidoCine.git
cd RapidoCine
```

2. **Créer l'environnement virtuel**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Installer et configurer PostgreSQL**
```bash
# Installer PostgreSQL
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Démarrer PostgreSQL
sudo service postgresql start

# Créer la base de données et l'utilisateur
sudo -u postgres psql
```

Dans le shell PostgreSQL :
```sql
CREATE DATABASE rapidocine_db;
CREATE USER rapidocine_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE rapidocine_db TO rapidocine_user;
\q
```

5. **Configurer les variables d'environnement**
```bash
cp .env.example .env
# Éditer .env et modifier DATABASE_URL avec vos credentials PostgreSQL
```

6. **Lancer le serveur backend**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

L'application sera accessible sur `http://localhost:8000`
Documentation API : `http://localhost:8000/docs`

## 📁 Structure du Projet

```
RapidoCine/
├── backend/
│   ├── models/          # Modèles SQLAlchemy
│   ├── routes/          # Routes FastAPI
│   ├── schemas/         # Schémas Pydantic
│   ├── database/        # Configuration DB
│   ├── auth/            # Authentification
│   └── main.py          # Point d'entrée
├── docker-compose.yml   # Configuration Docker
├── requirements.txt     # Dépendances Python
├── .env.example         # Template variables d'environnement
└── README.md
```

## 👥 Équipe

Projet RapidoCine

## 📝 Licence

Ce projet est à usage éducatif.
