# RecruiterIQ - Docker Setup Guide

This guide explains how to run the RecruiterIQ application using Docker and Docker Compose.

## Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose (included with Docker Desktop)

## Quick Start

1. **Clone the repository and navigate to the project directory:**
   ```bash
   cd Project-RecruiterIQ
   ```

2. **Create environment file:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` file and update the values as needed (especially `SECRET_KEY` and `ADMIN_PASSWORD` for production).

3. **Build and start all services:**
   ```bash
   docker-compose up -d
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Services

The Docker Compose setup includes three services:

### 1. PostgreSQL Database (`db`)
- **Image:** `postgres:16-alpine`
- **Port:** 5432 (configurable via `DB_PORT` in `.env`)
- **Data:** Persisted in Docker volume `postgres_data`

### 2. Backend API (`backend`)
- **Build:** `./backend/Dockerfile`
- **Port:** 8000 (configurable via `BACKEND_PORT` in `.env`)
- **Technology:** FastAPI + Python 3.11

### 3. Frontend (`frontend`)
- **Build:** `./frontend/Dockerfile`
- **Port:** 3000 (configurable via `FRONTEND_PORT` in `.env`)
- **Technology:** Vue 3 + Vuetify + Nginx

## Docker Commands

### Start services
```bash
docker-compose up -d
```

### Stop services
```bash
docker-compose down
```

### Stop services and remove volumes (⚠️ deletes database data)
```bash
docker-compose down -v
```

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

### Rebuild services after code changes
```bash
# Rebuild all services
docker-compose up -d --build

# Rebuild specific service
docker-compose up -d --build backend
docker-compose up -d --build frontend
```

### Access service shell
```bash
# Backend
docker-compose exec backend sh

# Frontend (nginx)
docker-compose exec frontend sh

# Database
docker-compose exec db psql -U postgres -d recruiteriq
```

### Check service status
```bash
docker-compose ps
```

## Environment Variables

Key environment variables (defined in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_NAME` | recruiteriq | PostgreSQL database name |
| `DB_USERNAME` | postgres | PostgreSQL username |
| `DB_PASSWORD` | postgres | PostgreSQL password |
| `SECRET_KEY` | (default) | JWT secret key (⚠️ change in production!) |
| `ADMIN_EMAIL` | admin@recruiteriq.com | Default admin email |
| `ADMIN_PASSWORD` | admin123 | Default admin password (⚠️ change!) |
| `BACKEND_PORT` | 8000 | Backend API port |
| `FRONTEND_PORT` | 3000 | Frontend port |

## Development Workflow

### Making changes to backend:
1. Edit Python files in `./backend/`
2. Rebuild: `docker-compose up -d --build backend`

### Making changes to frontend:
1. Edit Vue files in `./frontend/src/`
2. Rebuild: `docker-compose up -d --build frontend`

### Database migrations:
The backend automatically creates tables on startup. To reset the database:
```bash
docker-compose down -v  # Remove volumes
docker-compose up -d    # Recreate with fresh database
```

## Production Considerations

1. **Change default secrets:**
   - Update `SECRET_KEY` to a strong random value
   - Change `ADMIN_PASSWORD` to a secure password
   - Use strong `DB_PASSWORD`

2. **Use proper secrets management:**
   - Consider using Docker secrets or environment variable injection
   - Don't commit `.env` file to version control

3. **Enable HTTPS:**
   - Use a reverse proxy (nginx, traefik) with SSL certificates
   - Update CORS settings in backend

4. **Resource limits:**
   - Add resource limits to services in `docker-compose.yml`
   - Example:
     ```yaml
     deploy:
       resources:
         limits:
           cpus: '0.5'
           memory: 512M
     ```

5. **Health checks:**
   - Services include health checks
   - Monitor with `docker-compose ps`

6. **Backups:**
   - Regularly backup the `postgres_data` volume
   - Example: `docker run --rm -v recruiteriq_postgres_data:/data -v $(pwd):/backup ubuntu tar czf /backup/db-backup.tar.gz /data`

## Troubleshooting

### Backend can't connect to database
- Ensure database is healthy: `docker-compose ps`
- Check logs: `docker-compose logs db`
- Verify environment variables are set correctly

### Port already in use
- Change port in `.env` file
- Example: `BACKEND_PORT=8001`

### Services won't start
- Check Docker Desktop is running
- Verify docker-compose version: `docker-compose --version`
- Check logs: `docker-compose logs`

## Network

All services run on an isolated bridge network (`recruiteriq-network`) and can communicate using service names:
- Backend connects to database using hostname `db`
- Services are isolated from other Docker networks

## Volumes

- `postgres_data`: Persists PostgreSQL database data across container restarts

To inspect volumes:
```bash
docker volume ls
docker volume inspect recruiteriq_postgres_data
```
