# Docker & Docker Compose Hands-On Lab

This document records the Docker and Docker Compose portion of my cloud-native engineering learning project.

The goal is not only to make the application work, but to understand **why each component exists, how the components communicate, and how the same concepts will later map to Kubernetes**.

---

## 1. Environment

Learning workstation:

* OS: Ubuntu 24.04 LTS
* Architecture: x86_64
* Docker: 29.x
* Docker Compose: 2.x

The Ubuntu VM is a **cloud-engineering workstation/lab environment**, not the eventual production application server.

---

# Part 1 — Docker Fundamentals

## 2. Verify the Linux environment

```bash
uname -a
lsb_release -a
```

### Why?

Before installing infrastructure software, verify the operating system and architecture. Cloud engineering often involves troubleshooting compatibility between the OS, CPU architecture, packages, and container images.

---

## 3. Check available disk space

```bash
lsblk
df -h /
```

The VM storage was increased to approximately 100 GB because container images, build caches, logs, and future Kubernetes tooling can consume significant disk space.

### Why?

Container images are stored locally. Development environments can accumulate many images and build layers.

---

# Part 2 — Installing and Testing Docker

## 4. Verify Docker

```bash
docker --version
```

Docker was successfully installed.

Example:

```text
Docker version 29.1.3
```

---

## 5. Verify the Docker daemon

```bash
sudo systemctl status docker
```

The Docker service should show:

```text
Active: active (running)
```

### Why?

The Docker CLI communicates with the Docker daemon. If the daemon is not running, commands such as `docker run` and `docker build` cannot work.

---

## 6. Allow the current user to run Docker

```bash
sudo usermod -aG docker $USER
newgrp docker
```

Verify:

```bash
docker ps
```

### Why?

By default, access to the Docker socket requires elevated privileges. Adding the user to the `docker` group allows Docker commands without `sudo`.

### Security note

Membership in the Docker group is highly privileged and can effectively provide root-level control over the host.

This is acceptable for this learning workstation, but it should be treated as privileged access.

---

# Part 3 — First Docker Container

## 7. Run `hello-world`

```bash
docker run hello-world
```

Docker downloads the image if it does not already exist, creates a container, starts it, and runs the application's command.

Expected output includes:

```text
Hello from Docker!
```

Check containers:

```bash
docker ps -a
```

Check images:

```bash
docker images
```

### Important distinction

An **image** is the packaged application template.

A **container** is a running or stopped instance created from an image.

Conceptually:

```text
Image
  |
  +----> Container 1
  |
  +----> Container 2
  |
  +----> Container 3
```

---

# Part 4 — Build a Simple Web Application

## 8. Create the application

Location:

```text
app/
└── index.html
```

The application contains a simple HTML page.

Test the application without Docker:

```bash
python3 -m http.server 8080
```

From another terminal:

```bash
curl http://localhost:8080
```

### Why test before Docker?

This establishes a baseline.

If the application works outside Docker but fails inside Docker, the problem is probably related to the containerization configuration rather than the application itself.

This is an important troubleshooting technique:

```text
Application
   ↓
Test application
   ↓
Containerize
   ↓
Test container
   ↓
Compose
   ↓
Test multi-container system
```

---

# Part 5 — Dockerfile

## 9. Create the web Dockerfile

```dockerfile
FROM nginx:alpine

COPY index.html /usr/share/nginx/html/index.html

EXPOSE 80
```

### Explanation

### `FROM`

```dockerfile
FROM nginx:alpine
```

Uses Nginx on Alpine Linux as the base image.

### `COPY`

```dockerfile
COPY index.html /usr/share/nginx/html/index.html
```

Copies the application into the Nginx document root.

### `EXPOSE`

```dockerfile
EXPOSE 80
```

Documents that the application listens on port 80 inside the container.

`EXPOSE` does **not** automatically publish the port to the host.

---

# Part 6 — Build the Web Image

## 10. Build version 1.0

```bash
docker build -t cloud-native-app:1.0 .
```

Verify:

```bash
docker images
```

The resulting image was:

```text
cloud-native-app:1.0
```

### Why use tags?

The tag identifies a version of the image.

For example:

```text
cloud-native-app:1.0
cloud-native-app:1.1
```

This allows multiple versions to exist simultaneously.

---

# Part 7 — Run the Web Container

## 11. Start version 1.0

```bash
docker run -d \
  --name cloud-native-app \
  -p 8080:80 \
  cloud-native-app:1.0
```

Test:

```bash
curl http://localhost:8080
```

### Port mapping

```text
-p 8080:80
```

means:

```text
Host port 8080
       |
       v
Container port 80
```

So:

```text
localhost:8080 → Nginx:80
```

---

# Part 8 — Container Logs

## 12. View logs

```bash
docker logs cloud-native-app
```

Nginx logs showed successful HTTP requests such as:

```text
"GET / HTTP/1.1" 200
```

### Why?

Logs are one of the first places to look when troubleshooting a containerized application.

---

# Part 9 — Enter a Running Container

## 13. Open a shell inside the container

```bash
docker exec -it cloud-native-app sh
```

Then:

```bash
ls /usr/share/nginx/html
```

The application files were visible inside the container.

Exit:

```bash
exit
```

### Why?

`docker exec` is useful for troubleshooting and understanding what actually exists inside a running container.

It should generally be used for investigation rather than modifying production containers manually.

---

# Part 10 — Application Versioning

## 14. Create version 1.1

The HTML application was changed to display:

```text
Hello from my cloud-native application v1.1!
```

Then a new image was built:

```bash
docker build -t cloud-native-app:1.1 .
```

Both versions could then exist:

```text
cloud-native-app:1.0
cloud-native-app:1.1
```

### Important lesson

Changing the source file does not automatically change an existing container.

The existing container was created from the old image.

The new application version required a new image.

Conceptually:

```text
Source code v1.0
       ↓
Image v1.0
       ↓
Container v1.0


Source code v1.1
       ↓
Image v1.1
       ↓
Container v1.1
```

---

# Part 11 — Run Multiple Versions

Version 1.1 was started on another host port:

```bash
docker run -d \
  --name cloud-native-app-v11 \
  -p 8081:80 \
  cloud-native-app:1.1
```

Now:

```text
localhost:8080 → version 1.0
localhost:8081 → version 1.1
```

This demonstrated that multiple containers can run from different image versions simultaneously.

---

# Part 12 — Container Lifecycle

Useful commands learned:

```bash
docker ps
docker ps -a
docker stop <container>
docker start <container>
docker rm <container>
docker logs <container>
docker exec -it <container> sh
```

### Meaning

`docker ps`

Shows running containers.

`docker ps -a`

Shows running and stopped containers.

`docker stop`

Stops a running container.

`docker start`

Starts an existing stopped container.

`docker rm`

Removes a stopped container.

---

# Part 13 — Docker Compose

## 13. Install Compose

Verify:

```bash
docker compose version
```

Docker Compose was installed using:

```bash
sudo apt update
sudo apt install docker-compose-v2
```

---

# Part 14 — First Compose Application

## 14. Create `compose.yaml`

Initial version:

```yaml
services:
  web:
    image: cloud-native-app:1.1
    ports:
      - "8080:80"
```

Start:

```bash
docker compose up -d
```

Check:

```bash
docker compose ps
```

Test:

```bash
curl http://localhost:8080
```

Stop:

```bash
docker compose down
```

### Why Compose?

Instead of manually running multiple `docker run` commands, Compose allows the desired application architecture to be declared in YAML.

---

# Part 15 — Create the Backend

## 15. Backend application

Location:

```text
app/backend/app.py
```

The backend is a simple Python HTTP server listening on port 8000.

It returns:

```json
{
  "service": "backend",
  "status": "healthy"
}
```

---

# Part 16 — Test Backend Before Docker

Run:

```bash
python3 app.py
```

Expected:

```text
Backend listening on port 8000
```

From another terminal:

```bash
curl http://localhost:8000
```

Expected:

```json
{"service": "backend", "status": "healthy"}
```

### Why?

Again, the application was verified before containerization.

---

# Part 17 — Backend Dockerfile

## 17. Create backend image definition

```dockerfile
FROM python:3.12-alpine

WORKDIR /app

COPY app.py .

EXPOSE 8000

CMD ["python3", "app.py"]
```

### Explanation

```dockerfile
FROM python:3.12-alpine
```

Provides Python using a lightweight Alpine-based image.

```dockerfile
WORKDIR /app
```

Sets the working directory inside the container.

```dockerfile
COPY app.py .
```

Copies the Python application into the image.

```dockerfile
EXPOSE 8000
```

Documents the application's internal port.

```dockerfile
CMD ["python3", "app.py"]
```

Defines the default process started when the container runs.

---

# Part 18 — Build Backend Image

```bash
docker build -t cloud-native-backend:1.0 .
```

Verify:

```bash
docker images
```

The image:

```text
cloud-native-backend:1.0
```

was successfully created.

---

# Part 19 — Run Backend Container

The backend was independently tested using:

```bash
docker run -d \
  --name cloud-native-backend \
  -p 8000:8000 \
  cloud-native-backend:1.0
```

Test:

```bash
curl http://localhost:8000
```

Expected:

```json
{"service": "backend", "status": "healthy"}
```

This proved that the backend works correctly inside Docker.

The standalone container was then stopped and removed before moving it into Compose.

---

# Part 20 — Multi-Service Docker Compose

## 20. Current `compose.yaml`

```yaml
services:
  web:
    image: cloud-native-app:1.1
    ports:
      - "8080:80"
    depends_on:
      - backend

  backend:
    image: cloud-native-backend:1.0
    expose:
      - "8000"
```

---

# Part 21 — Start Both Services

```bash
docker compose up -d
```

Check:

```bash
docker compose ps
```

Expected architecture:

```text
web
  |
  |
backend
```

The web service is published to the host:

```text
localhost:8080
```

The backend is not published to the host.

---

# Part 22 — `ports` vs `expose`

The web service uses:

```yaml
ports:
  - "8080:80"
```

This publishes the container port to the host.

```text
Host :8080
    ↓
Web container :80
```

The backend uses:

```yaml
expose:
  - "8000"
```

This documents the internal service port without publishing it to the host.

Therefore:

```text
Host → backend:8000
```

is not the intended architecture.

Instead:

```text
web → backend:8000
```

is allowed through the Compose network.

---

# Part 23 — Docker Compose Service Discovery

## 23. Test communication between services

From inside the web container:

```bash
docker compose exec web wget -qO- http://backend:8000
```

The response:

```json
{"service": "backend", "status": "healthy"}
```

### What happened?

The web container contacted:

```text
http://backend:8000
```

The word `backend` is the **Compose service name**.

Compose provides networking and DNS for services on the same Compose network.

Therefore:

```text
backend
   ↓
backend container IP
```

We did not need to know the backend container's IP address.

---

# Part 24 — Current Architecture

At this point the application looks like:

```text
                         Docker Compose network
                 ┌─────────────────────────────────┐
                 │                                 │
                 │   ┌──────────────┐              │
                 │   │     web      │              │
                 │   │    Nginx     │              │
                 │   │     :80      │              │
                 │   └──────┬───────┘              │
                 │          │                      │
                 │          │ backend:8000         │
                 │          ▼                      │
                 │   ┌──────────────┐              │
                 │   │   backend    │              │
                 │   │    Python    │              │
                 │   │    :8000     │              │
                 │   └──────────────┘              │
                 │                                 │
                 └─────────────────────────────────┘
                            ▲
                            │
                         :8080
                            │
                         Ubuntu
```

The host accesses:

```text
http://localhost:8080
```

The web container accesses the backend using:

```text
http://backend:8000
```

The backend does not need to expose port 8000 to the host.

---

# Part 25 — Important Concepts Learned

## Images

Immutable packaged application environments.

Example:

```text
cloud-native-app:1.1
```

## Containers

Runtime instances of images.

Example:

```text
app-web-1
```

## Dockerfile

Instructions for building an image.

## Ports

Control how network traffic enters/leaves containers.

## Compose

Defines and manages multiple related containers.

## Compose services

Logical application components such as:

```text
web
backend
```

## Compose networking

Allows services to communicate using service names:

```text
backend:8000
```

## `depends_on`

Controls startup ordering.

It does **not** guarantee that a service is ready to accept traffic.

Health checks will be introduced later.

---

# Part 26 — Kubernetes Connection

These Docker Compose concepts will map to Kubernetes later.

| Docker Compose        | Kubernetes                        |
| --------------------- | --------------------------------- |
| Service               | Deployment/Pod + Service          |
| Container             | Container inside Pod              |
| `ports`               | Service/Ingress networking        |
| Compose DNS           | Kubernetes Service DNS            |
| `depends_on`          | Probes/readiness/startup behavior |
| Compose network       | Kubernetes cluster networking     |
| Environment variables | ConfigMap/Secret                  |
| Compose replicas      | Deployment replicas               |
| `healthcheck`         | Kubernetes probes                 |

One particularly important connection is:

```text
Docker Compose:

backend:8000
```

Later becomes conceptually similar to:

```text
backend-service:8000
```

in Kubernetes.

The major difference is that Kubernetes provides a much more powerful control plane for scheduling, scaling, healing, rolling deployments, security, and high availability.

---

# Part 27 — Useful Commands Reference

### Docker

```bash
docker images
docker ps
docker ps -a
docker build -t <image>:<tag> .
docker run
docker stop <container>
docker start <container>
docker rm <container>
docker logs <container>
docker exec -it <container> sh
```

### Docker Compose

```bash
docker compose up -d
docker compose ps
docker compose logs
docker compose logs -f
docker compose exec <service> <command>
docker compose down
docker compose build
docker compose pull
```

---

# Current Learning Status

Completed:

* Docker installation
* Docker daemon
* Docker permissions
* Images
* Containers
* Dockerfiles
* Image tagging/versioning
* Port mapping
* Container lifecycle
* Container logs
* `docker exec`
* Docker Compose
* Compose services
* Compose networks
* Service discovery
* Multi-container application

Next:

* Nginx reverse proxy
* `/api/` → `backend:8000`
* Backend health checks
* Compose dependency/readiness
* Environment variables
* Volumes
* PostgreSQL
* Redis
* More production-style Compose architecture
* Eventually transition these concepts to Kubernetes
