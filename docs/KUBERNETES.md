# Kubernetes Deployment Guide for RapidoCine

This guide covers deploying RapidoCine to Kubernetes using the provided manifests and Kustomize overlays.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Architecture Overview](#architecture-overview)
- [Quick Start](#quick-start)
- [Local Development with Minikube/Kind](#local-development-with-minikubekind)
- [Deployment Options](#deployment-options)
- [Configuration](#configuration)
- [Secrets Management](#secrets-management)
- [Monitoring and Observability](#monitoring-and-observability)
- [CI/CD Pipeline](#cicd-pipeline)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- Kubernetes cluster (v1.24+)
- `kubectl` CLI tool installed
- `kustomize` installed (or use `kubectl apply -k`)
- Docker registry access (for custom images)
- NGINX Ingress Controller installed in your cluster
- (Optional) cert-manager for TLS certificates
- (Optional) Metrics Server for HPA

## Architecture Overview

RapidoCine consists of the following components:

- **Frontend/Backend**: FastAPI SSR application (port 8000)
- **Database**: PostgreSQL 15 (port 5432)
- **Storage**: Persistent volume for database data
- **Ingress**: NGINX Ingress for external access
- **Autoscaling**: HPA based on CPU/Memory metrics

### Kubernetes Resources

```
k8s/
├── base/                          # Base Kubernetes manifests
│   ├── namespace.yaml             # Namespace definition
│   ├── configmap.yaml             # Application configuration
│   ├── secret.yaml                # Sensitive data (DO NOT commit real secrets)
│   ├── postgres-pvc.yaml          # Database persistent volume claim
│   ├── postgres-deployment.yaml   # PostgreSQL deployment
│   ├── postgres-service.yaml      # PostgreSQL service
│   ├── app-deployment.yaml        # RapidoCine application deployment
│   ├── app-service.yaml           # Application service
│   ├── app-hpa.yaml               # Horizontal Pod Autoscaler
│   ├── ingress.yaml               # Ingress configuration
│   └── kustomization.yaml         # Kustomize base configuration
└── overlays/                      # Environment-specific overlays
    ├── dev/                       # Development environment
    │   ├── kustomization.yaml
    │   ├── deployment-patch.yaml
    │   └── ingress-patch.yaml
    └── prod/                      # Production environment
        ├── kustomization.yaml
        ├── deployment-patch.yaml
        └── ingress-patch.yaml
```

## Quick Start

### 1. Build and Push Docker Image

```bash
# Build the Docker image
docker build -t rapidocine:latest .

# Tag for your registry
docker tag rapidocine:latest ghcr.io/YOUR_USERNAME/rapidocine:latest

# Push to registry
docker push ghcr.io/YOUR_USERNAME/rapidocine:latest
```

### 2. Update Image Reference

Edit `k8s/base/kustomization.yaml` and update the image reference:

```yaml
images:
  - name: rapidocine
    newName: ghcr.io/YOUR_USERNAME/rapidocine
    newTag: latest
```

### 3. Update Secrets

**⚠️ IMPORTANT**: Never commit real secrets to Git!

Create secrets using kubectl:

```bash
kubectl create secret generic rapidocine-secrets \
  --from-literal=POSTGRES_DB=rapidocine_db \
  --from-literal=POSTGRES_USER=rapidocine \
  --from-literal=POSTGRES_PASSWORD=YOUR_STRONG_PASSWORD \
  --from-literal=OMDB_API_KEY=YOUR_OMDB_API_KEY \
  --from-literal=SESSION_SECRET_KEY=$(openssl rand -hex 32) \
  -n rapidocine --dry-run=client -o yaml > k8s/base/secret.yaml
```

### 4. Deploy to Kubernetes

Using kubectl with Kustomize:

```bash
# Deploy base configuration
kubectl apply -k k8s/base

# Or deploy development overlay
kubectl apply -k k8s/overlays/dev

# Or deploy production overlay
kubectl apply -k k8s/overlays/prod
```

### 5. Verify Deployment

```bash
# Check pods
kubectl get pods -n rapidocine

# Check services
kubectl get svc -n rapidocine

# Check ingress
kubectl get ingress -n rapidocine

# View logs
kubectl logs -f deployment/rapidocine-app -n rapidocine
```

## Local Development with Minikube/Kind

### Using Minikube

```bash
# Start Minikube
minikube start --cpus=4 --memory=8192

# Enable ingress addon
minikube addons enable ingress
minikube addons enable metrics-server

# Build image directly in Minikube
eval $(minikube docker-env)
docker build -t rapidocine:latest .

# Deploy
kubectl apply -k k8s/overlays/dev

# Get Minikube IP and add to /etc/hosts
echo "$(minikube ip) rapidocine-dev.example.com" | sudo tee -a /etc/hosts

# Access the application
open http://rapidocine-dev.example.com
```

### Using Kind

```bash
# Create Kind cluster
cat <<EOF | kind create cluster --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
EOF

# Install NGINX Ingress Controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

# Wait for ingress controller
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s

# Load image to Kind
kind load docker-image rapidocine:latest

# Deploy
kubectl apply -k k8s/overlays/dev

# Add to /etc/hosts
echo "127.0.0.1 rapidocine-dev.example.com" | sudo tee -a /etc/hosts

# Access the application
open http://rapidocine-dev.example.com
```

## Deployment Options

### Development Environment

```bash
kubectl apply -k k8s/overlays/dev
```

Features:
- DEBUG mode enabled
- 1 replica
- Lower resource limits
- Development domain

### Production Environment

```bash
kubectl apply -k k8s/overlays/prod
```

Features:
- DEBUG mode disabled
- 3 replicas
- Higher resource limits
- Production domain with TLS

## Configuration

### Environment Variables

Configure via ConfigMap (`k8s/base/configmap.yaml`):

- `DEBUG`: Enable/disable debug mode

Configure via Secret (`k8s/base/secret.yaml`):

- `POSTGRES_DB`: Database name
- `POSTGRES_USER`: Database user
- `POSTGRES_PASSWORD`: Database password
- `OMDB_API_KEY`: OMDB API key
- `SESSION_SECRET_KEY`: Session encryption key

### Resource Limits

Adjust in deployment patches:

```yaml
# Development (k8s/overlays/dev/deployment-patch.yaml)
resources:
  requests:
    cpu: "50m"
    memory: "128Mi"
  limits:
    cpu: "500m"
    memory: "256Mi"

# Production (k8s/overlays/prod/deployment-patch.yaml)
resources:
  requests:
    cpu: "200m"
    memory: "512Mi"
  limits:
    cpu: "2000m"
    memory: "1Gi"
```

## Secrets Management

### Using kubectl create secret

```bash
kubectl create secret generic rapidocine-secrets \
  --from-literal=POSTGRES_PASSWORD=$(openssl rand -base64 32) \
  --from-literal=SESSION_SECRET_KEY=$(openssl rand -hex 32) \
  --from-literal=OMDB_API_KEY=your-api-key \
  -n rapidocine
```

## Monitoring and Observability

### Health Checks

The application exposes health check endpoints:

- `/health`: Liveness probe (application running)
- `/ready`: Readiness probe (database connected)

### Prometheus Metrics

The deployment includes Prometheus annotations:

```yaml
annotations:
  prometheus.io/scrape: "true"
  prometheus.io/port: "8000"
  prometheus.io/path: "/metrics"
```

## CI/CD Pipeline

The project includes a GitHub Actions workflow (`.github/workflows/deploy-k8s.yml`) that:

1. Builds and pushes Docker images to GitHub Container Registry
2. Deploys to development environment on push to `develop` branch
3. Deploys to production environment on version tags (e.g., `v1.0.0`)

### Setup Instructions

1. **Configure Repository Secrets**:
   - `KUBE_CONFIG_DEV`: Base64-encoded kubeconfig for dev cluster
   - `KUBE_CONFIG_PROD`: Base64-encoded kubeconfig for prod cluster

   ```bash
   # Encode kubeconfig
   cat ~/.kube/config | base64 -w 0
   ```

2. **Enable GitHub Container Registry**:
   - Ensure packages write permission is enabled
   - Images will be pushed to `ghcr.io/YOUR_USERNAME/rapidocine`

3. **Trigger Deployment**:
   ```bash
   # Deploy to development
   git push origin develop

   # Deploy to production
   git tag v1.0.0
   git push origin v1.0.0
   ```

## Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl get pods -n rapidocine

# Describe pod for events
kubectl describe pod <pod-name> -n rapidocine

# Check logs
kubectl logs <pod-name> -n rapidocine
```

### Database Connection Issues

```bash
# Check if PostgreSQL is running
kubectl get pods -n rapidocine -l app=postgres

# Test database connection
kubectl run -it --rm psql-test --image=postgres:15-alpine --restart=Never -- \
  psql -h postgres.rapidocine.svc.cluster.local -U rapidocine -d rapidocine_db
```

### Ingress Not Working

```bash
# Check ingress controller is installed
kubectl get pods -n ingress-nginx

# Check ingress resource
kubectl get ingress -n rapidocine
kubectl describe ingress rapidocine-ingress -n rapidocine

# Check service endpoints
kubectl get endpoints -n rapidocine
```

## Production Checklist

Before deploying to production:

- [ ] Use strong, randomly generated passwords for all secrets
- [ ] Configure TLS/SSL certificates (cert-manager + Let's Encrypt)
- [ ] Set appropriate resource requests and limits
- [ ] Configure backup strategy for PostgreSQL
- [ ] Set up monitoring and alerting (Prometheus + Grafana)
- [ ] Configure log aggregation (ELK, Loki, etc.)
- [ ] Review and adjust HPA settings based on load testing
- [ ] Configure network policies for pod-to-pod communication
- [ ] Set up disaster recovery plan
- [ ] Configure pod disruption budgets for high availability

## Additional Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kustomize Documentation](https://kustomize.io/)
- [NGINX Ingress Controller](https://kubernetes.github.io/ingress-nginx/)
- [cert-manager](https://cert-manager.io/)
