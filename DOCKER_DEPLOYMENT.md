# 🐳 Docker Deployment Guide

This guide explains how to deploy the Autonomous Learning Agent using Docker and Docker Compose.

## Prerequisites

- Docker Desktop installed ([Get Docker](https://www.docker.com/products/docker-desktop))
- Docker Compose (included with Docker Desktop)

## Quick Start

### 1. Configure Environment Variables

Create a `.env` file in the root directory:

```env
# Groq API Key (Required)
GROQ_API_KEY=your_groq_api_key_here

# JWT Secret Key (Generate with: python -c "import secrets; print(secrets.token_hex(32))")
SECRET_KEY=your_secure_secret_key_here
```

### 2. Build and Run

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode (background)
docker-compose up -d --build
```

### 3. Access the Application

- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **MongoDB**: localhost:27017

### 4. Stop the Application

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (clears database)
docker-compose down -v
```

## Services Overview

The Docker Compose setup includes three services:

1. **MongoDB** (Port 27017)
   - Database for user data and learning progress
   - Data persisted in Docker volume `mongodb_data`

2. **Backend** (Port 8000)
   - FastAPI server with AI learning engine
   - Connects to MongoDB
   - Requires Groq API key

3. **Frontend** (Port 80)
   - React application served by Nginx
   - Communicates with backend API

## MongoDB Access

Default MongoDB credentials (change in production):
- Username: `admin`
- Password: `changeme123`

Connect using MongoDB Compass:
```
mongodb://admin:changeme123@localhost:27017/?authSource=admin
```

## Development vs Production

### Development Mode

The current `docker-compose.yml` is configured for development with:
- Hot reload enabled for backend
- Volume mounts for live code updates
- Debug logging

### Production Mode

For production deployment:

1. **Update MongoDB credentials** in `docker-compose.yml`
2. **Use strong SECRET_KEY**
3. **Remove volume mounts** for backend
4. **Disable debug/reload** in backend command
5. **Use environment-specific settings**

## Docker Commands Cheat Sheet

```bash
# View running containers
docker ps

# View logs
docker-compose logs

# View logs for specific service
docker-compose logs backend
docker-compose logs frontend

# Follow logs in real-time
docker-compose logs -f

# Rebuild a specific service
docker-compose build backend

# Restart a service
docker-compose restart backend

# Execute command in running container
docker-compose exec backend bash
docker-compose exec mongodb mongosh

# Remove all stopped containers and unused images
docker system prune -a
```

## Troubleshooting

### Port Already in Use

If port 80 or 8000 is in use:

1. Stop conflicting services
2. Or modify ports in `docker-compose.yml`:
   ```yaml
   frontend:
     ports:
       - "3000:80"  # Access at localhost:3000
   
   backend:
     ports:
       - "8080:8000"  # Access at localhost:8080
   ```

### MongoDB Connection Issues

- Ensure MongoDB container is running: `docker ps`
- Check logs: `docker-compose logs mongodb`
- Verify credentials in backend environment variables

### Backend Not Starting

- Check if GROQ_API_KEY is set
- View error logs: `docker-compose logs backend`
- Ensure all dependencies are in requirements.txt

## Production Deployment with Docker

### Using Docker on VPS (DigitalOcean, AWS, etc.)

1. **Set up VPS** with Docker installed
2. **Clone repository** on the server
3. **Update docker-compose.yml** for production:
   - Change MongoDB credentials
   - Set strong SECRET_KEY
   - Configure proper domain/URLs
4. **Run with production settings**:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

### Using Docker Registry

1. **Build and tag images**:
   ```bash
   docker build -t yourusername/learning-agent-backend:latest ./backend
   docker build -t yourusername/learning-agent-frontend:latest ./frontend
   ```

2. **Push to Docker Hub**:
   ```bash
   docker push yourusername/learning-agent-backend:latest
   docker push yourusername/learning-agent-frontend:latest
   ```

3. **Deploy from registry** on any server with Docker

## Next Steps

- Review [DEPLOYMENT.md](DEPLOYMENT.md) for cloud platform deployment options
- Set up monitoring and logging
- Configure backup for MongoDB data
- Set up SSL/HTTPS with reverse proxy (nginx/Traefik)
- Implement CI/CD pipeline for automated deployments

## Support

For issues with Docker deployment:
1. Check container logs
2. Verify environment variables
3. Ensure all services are running
4. Review Docker and Docker Compose documentation
