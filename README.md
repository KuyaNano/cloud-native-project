# Cloud Native Project

My journey into cloud engineering, DevOps, and cloud infrastructure.

## Goals

- Learn Git
- Learn Docker
- Learn CloudSigma
- Learn Terraform
- Learn Kubernetes
- Learn Cloud Security

## Current Focus

- Docker and container networking
- Reverse proxy architecture
- Preparing the application for cloud deployment

## Git Workflow

- Pull the latest changes
- Create a feature branch
- Make changes
- Commit changes
- Push the feature branch
- Merge the feature into main
- Delete the feature branch after merging

## Current Project Status

### Completed

- Git fundamentals and GitHub workflow
- Feature branches and pull requests
- Merge conflict resolution
- Docker installation and container fundamentals
- Dockerfiles and image versioning
- Docker Compose
- Multi-container networking
- Docker service discovery
- Port publishing and `ports` vs `expose`
- Nginx reverse proxy
- `/api/` routing from Nginx to the backend
- Backend health checks
- Compose dependency and readiness with `service_healthy`

### Current Application

The project currently contains two Docker Compose services:

```text
                    Ubuntu VM
                 Host VM
                       |
                  TCP :8080
                       |
                       v
              +----------------+
              | Nginx Web      |
              | nginx:alpine   |
              |      :80       |
              +-------+--------+
                      |
             +--------+--------+
             |                 |
             v                 v
          /                  /api/
     Frontend HTML             |
                               v
                    Docker Network
                               |
                               v
                     +-------------------+
                     | Backend Container |
                     | Python HTTP Server|
                     |       :8000       |
                     +-------------------+

```
## Next Steps

- Environment variables and configuration management
- Docker volumes
- PostgreSQL
- Redis
- More production-style Compose architecture
- CloudSigma deployment
- Terraform infrastructure as code
- Kubernetes
- Kubernetes security
- High availability and scaling
- CI/CD and GitOps
- Observability
- Security scanning and supply-chain security
- Backups and disaster recovery
