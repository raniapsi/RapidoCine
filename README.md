# RapidoCine - IMDb Clone

A modern web application for movies and reviews, built with FastAPI (backend SSR) and Jinja2 templates.

## Features

- 🎬 Browse movies with IMDb ratings
- ⭐ Rate and review movies
- 📝 Comment on movies
- 📚 Create and manage watchlists
- 🔐 User authentication and sessions
- 🔍 Search functionality
- 📱 Responsive design

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Jinja2 templates, HTML, CSS, JavaScript
- **Database**: PostgreSQL (production), SQLite (development)
- **ORM**: SQLAlchemy
- **API**: OMDb API for movie data

## Quick Start

### Using Docker Compose

```bash
# Start all services
docker-compose up -d

# Access the application
open http://localhost:8000
```

### Local Development

```bash
# Install dependencies
pip install -r backend/requirements.txt

# Initialize database
python -m backend.init_db

# Start the server
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

## Deployment

### Kubernetes

This project includes comprehensive Kubernetes support with:

- Production-ready manifests
- Kustomize overlays for dev/prod environments
- Horizontal Pod Autoscaler (HPA)
- Health check endpoints
- CI/CD pipeline with GitHub Actions

**Quick Deploy:**

```bash
# Deploy to development
kubectl apply -k k8s/overlays/dev

# Deploy to production
kubectl apply -k k8s/overlays/prod
```

📖 **Full Kubernetes Documentation**: [docs/KUBERNETES.md](docs/KUBERNETES.md)  
📝 **Quick Reference**: [k8s/README.md](k8s/README.md)

### Traditional Deployment

See [README_ARCHITECTURE.md](README_ARCHITECTURE.md) for detailed architecture and deployment options.

## Documentation

- [Architecture Guide](README_ARCHITECTURE.md) - Detailed application architecture
- [Kubernetes Deployment](docs/KUBERNETES.md) - Complete K8s deployment guide
- [Development Mode](DEV_MODE.md) - Development setup and guidelines

## Environment Variables

```bash
# Required
DATABASE_URL=postgresql://user:password@host:5432/dbname
OMDB_API_KEY=your_omdb_api_key

# Optional
DEBUG=False
SESSION_SECRET_KEY=your_secret_key
```

## API Endpoints

### Public Endpoints
- `GET /` - Home page
- `GET /movies` - All movies
- `GET /movie/{id}` - Movie details
- `GET /health` - Health check (Kubernetes liveness probe)
- `GET /ready` - Readiness check (Kubernetes readiness probe)

### Authentication Required
- `GET /movies/top_rated` - User's top rated movies
- `GET /movies/watchlist` - User's watchlist
- `POST /api/movies/{id}/rating` - Rate a movie
- `POST /api/movies/{id}/comment` - Comment on a movie

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

[License information]

## Support

For issues and questions:
- Create an issue in the GitHub repository
- Check the documentation
- Review the troubleshooting guides
