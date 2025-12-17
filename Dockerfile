FROM python:3.11-slim

WORKDIR /app

# Copier les fichiers de dépendances
COPY backend/requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code
COPY backend ./backend
COPY frontend ./frontend
