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

- Practicing Git branches
- Practice GitHub collaboration

## Git Workflow

- Pull the latest changes
- Create a feature branch
- Make changes
- Commit changes
- Push the feature branch
- Merge the feature into main

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

### Current Application

The project currently contains two Docker Compose services:

```text
                    Ubuntu VM
                 49.157.47.37
                       |
                  TCP :8080
                       |
                       v
              +----------------+
              |  Web Container |
              |   nginx:alpine |
              |      :80       |
              +----------------+
                       |
                  Docker Network
                       |
                       v
             +-------------------+
             | Backend Container |
             | Python HTTP Server|
             |       :8000       |
             +-------------------+
