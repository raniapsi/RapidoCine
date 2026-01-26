# Kubernetes Quick Reference

Quick commands for deploying and managing RapidoCine in Kubernetes.

## Deploy

```bash
# Development
kubectl apply -k k8s/overlays/dev

# Production
kubectl apply -k k8s/overlays/prod

# Base (not recommended for direct use)
kubectl apply -k k8s/base
```

## Check Status

```bash
# All resources in namespace
kubectl get all -n rapidocine

# Pods
kubectl get pods -n rapidocine -w

# Services
kubectl get svc -n rapidocine

# Ingress
kubectl get ingress -n rapidocine

# HPA
kubectl get hpa -n rapidocine
```

## View Logs

```bash
# Application logs
kubectl logs -f deployment/rapidocine-app -n rapidocine

# Database logs
kubectl logs -f deployment/postgres -n rapidocine

# All containers in a pod
kubectl logs -f <pod-name> --all-containers -n rapidocine
```

## Debug

```bash
# Describe pod
kubectl describe pod <pod-name> -n rapidocine

# Get events
kubectl get events -n rapidocine --sort-by='.lastTimestamp'

# Execute shell in pod
kubectl exec -it <pod-name> -n rapidocine -- /bin/sh

# Port forward to local
kubectl port-forward svc/rapidocine-app 8000:80 -n rapidocine
```

## Update Deployment

```bash
# Update image
kubectl set image deployment/rapidocine-app \
  rapidocine=ghcr.io/user/rapidocine:v1.0.1 -n rapidocine

# Restart deployment
kubectl rollout restart deployment/rapidocine-app -n rapidocine

# Check rollout status
kubectl rollout status deployment/rapidocine-app -n rapidocine
```

## Rollback

```bash
# View history
kubectl rollout history deployment/rapidocine-app -n rapidocine

# Rollback to previous
kubectl rollout undo deployment/rapidocine-app -n rapidocine

# Rollback to specific revision
kubectl rollout undo deployment/rapidocine-app --to-revision=2 -n rapidocine
```

## Scale

```bash
# Manual scaling
kubectl scale deployment/rapidocine-app --replicas=5 -n rapidocine

# View HPA status
kubectl describe hpa rapidocine-app-hpa -n rapidocine
```

## Secrets

```bash
# View secrets (not values)
kubectl get secrets -n rapidocine

# Decode secret
kubectl get secret rapidocine-secrets -n rapidocine -o jsonpath='{.data.POSTGRES_PASSWORD}' | base64 -d

# Update secret
kubectl create secret generic rapidocine-secrets \
  --from-literal=KEY=VALUE \
  --dry-run=client -o yaml | kubectl apply -f -
```

## Clean Up

```bash
# Delete development environment
kubectl delete -k k8s/overlays/dev

# Delete production environment
kubectl delete -k k8s/overlays/prod

# Delete namespace (removes everything)
kubectl delete namespace rapidocine
```

## Build and Push Image

```bash
# Build
docker build -t rapidocine:latest .

# Tag
docker tag rapidocine:latest ghcr.io/USER/rapidocine:v1.0.0

# Push
docker push ghcr.io/USER/rapidocine:v1.0.0
```

## Local Testing

```bash
# Minikube
minikube start
eval $(minikube docker-env)
docker build -t rapidocine:latest .
kubectl apply -k k8s/overlays/dev

# Kind
kind create cluster
kind load docker-image rapidocine:latest
kubectl apply -k k8s/overlays/dev
```

For detailed documentation, see [docs/KUBERNETES.md](docs/KUBERNETES.md)
