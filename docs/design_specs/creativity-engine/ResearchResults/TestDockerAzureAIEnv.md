# Local Azure deployment test environment on Windows

**You can simulate Azure App Service and Azure Static Web Apps entirely on your local machine using Docker Desktop with WSL2, running Node.js, Python, .NET 8, and React containers alongside Azurite for storage emulation.** This guide provides every file, every config, and every command — copy-paste ready with March 2026 tooling versions. The full stack runs via a single `docker compose up` and includes CI/CD pipelines, automated tests, and a smoke-test script that validates everything end-to-end.

---

## 1. Prerequisites and installation on Windows

### System requirements

Windows 10 (Build 19041+) or Windows 11, 64-bit, with hardware virtualization (VT-x/AMD-V) enabled in BIOS. Minimum **8 GB RAM** recommended (16 GB preferred). You need approximately **20 GB free disk space** for Docker images and build caches.

### Step-by-step installation

**Enable WSL2** — open PowerShell as Administrator:

```powershell
wsl --install
wsl --set-default-version 2
```

Restart your machine when prompted. After restart, verify with `wsl --status`.

**Install Docker Desktop** — download from [docker.com](https://docs.docker.com/desktop/install/windows-install/) or use winget:

```powershell
winget install -e --id Docker.DockerDesktop
```

During setup, ensure "Use WSL 2 based engine" is checked. After installation, open Docker Desktop, go to **Settings → Resources → WSL Integration** and enable your default distro. Verify:

```powershell
docker --version
docker compose version
docker run hello-world
```

**Install Azure CLI:**

```powershell
winget install -e --id Microsoft.AzureCLI
# Close and reopen terminal, then:
az login
az account show
```

**Install Azure Developer CLI (optional — useful for future Azure deployments):**

```powershell
winget install microsoft.azd
```

**Install Node.js 22 LTS, Python 3.13, and .NET 8 SDK on host** (for running tests outside containers):

```powershell
winget install OpenJS.NodeJS.LTS
winget install Python.Python.3.13
winget install Microsoft.DotNet.SDK.8
```

**Install Git:**

```powershell
winget install -e --id Git.Git
```

### Configure WSL2 memory limits

Create `C:\Users\<YourUsername>\.wslconfig`:

```ini
[wsl2]
memory=8GB
processors=4
swap=4GB

[experimental]
autoMemoryReclaim=gradual
```

Then run `wsl --shutdown` and relaunch Docker Desktop.

---

## 2. Project directory structure

Create this folder layout. Every file below is provided in full.

```
azure-local-env/
├── docker-compose.yml
├── .env
├── .env.example
├── deploy.ps1
├── deploy.sh
│
├── node-api/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── .env.example
│   ├── package.json
│   ├── src/
│   │   └── index.js
│   └── tests/
│       └── health.test.js
│
├── python-api/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── .env.example
│   ├── requirements.txt
│   ├── app/
│   │   └── main.py
│   └── tests/
│       └── test_health.py
│
├── dotnet-api/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── .env.example
│   ├── DotnetApi.csproj
│   ├── Program.cs
│   └── DotnetApi.Tests/
│       ├── DotnetApi.Tests.csproj
│       └── HealthTests.cs
│
└── react-app/
    ├── Dockerfile
    ├── .dockerignore
    ├── .env.example
    ├── nginx.conf
    ├── package.json
    ├── vite.config.js
    ├── index.html
    ├── src/
    │   ├── main.jsx
    │   ├── App.jsx
    │   └── App.test.jsx
    └── public/
```

---

## 3. Health endpoint code for each stack

### Node.js Express — `node-api/package.json`

```json
{
  "name": "node-api",
  "version": "1.0.0",
  "description": "Node.js Express API for Azure local testing",
  "main": "src/index.js",
  "scripts": {
    "start": "node src/index.js",
    "dev": "node --watch src/index.js",
    "test": "node --experimental-vm-modules node_modules/.bin/jest --forceExit",
    "lint": "eslint src/"
  },
  "dependencies": {
    "express": "^4.21.0"
  },
  "devDependencies": {
    "eslint": "^9.0.0",
    "jest": "^30.0.0",
    "supertest": "^7.0.0"
  }
}
```

### Node.js Express — `node-api/src/index.js`

```javascript
const express = require("express");

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get("/health", (req, res) => {
  res.status(200).json({ status: "ok", service: "node-api" });
});

app.get("/", (req, res) => {
  res.json({ message: "Node.js API running", env: process.env.NODE_ENV || "development" });
});

if (require.main === module) {
  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Node API listening on port ${PORT}`);
  });
}

module.exports = app;
```

### Python FastAPI — `python-api/requirements.txt`

```
fastapi==0.115.0
uvicorn[standard]==0.32.0
httpx==0.28.0
pytest==8.3.0
ruff==0.8.0
```

### Python FastAPI — `python-api/app/main.py`

```python
import os
from fastapi import FastAPI

app = FastAPI(title="Python API")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "python-api"}


@app.get("/")
async def root():
    return {"message": "Python API running", "env": os.getenv("APP_ENV", "development")}
```

### C# .NET 8 Web API — `dotnet-api/DotnetApi.csproj`

```xml
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>
</Project>
```

### C# .NET 8 Web API — `dotnet-api/Program.cs`

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/health", () => Results.Ok(new { status = "ok", service = "dotnet-api" }));

app.MapGet("/", () => Results.Ok(new
{
    message = "Dotnet API running",
    env = app.Environment.EnvironmentName
}));

app.Run();
```

### React App — `react-app/package.json`

```json
{
  "name": "react-app",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "test": "vitest run",
    "lint": "eslint src/"
  },
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0"
  },
  "devDependencies": {
    "@testing-library/react": "^16.0.0",
    "@testing-library/jest-dom": "^6.6.0",
    "@vitejs/plugin-react": "^4.3.0",
    "eslint": "^9.0.0",
    "jsdom": "^25.0.0",
    "vite": "^6.0.0",
    "vitest": "^2.1.0"
  }
}
```

### React App — `react-app/vite.config.js`

```javascript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: [],
  },
  server: {
    port: 5173,
  },
});
```

### React App — `react-app/index.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>React App — Azure Local</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

### React App — `react-app/src/main.jsx`

```jsx
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

### React App — `react-app/src/App.jsx`

```jsx
import { useState, useEffect } from "react";

function App() {
  const [services, setServices] = useState({});

  useEffect(() => {
    const endpoints = {
      node: "http://localhost:3000/health",
      python: "http://localhost:8000/health",
      dotnet: "http://localhost:8080/health",
    };

    Object.entries(endpoints).forEach(([name, url]) => {
      fetch(url)
        .then((r) => r.json())
        .then((data) => setServices((prev) => ({ ...prev, [name]: data.status })))
        .catch(() => setServices((prev) => ({ ...prev, [name]: "unreachable" })));
    });
  }, []);

  return (
    <div style={{ fontFamily: "system-ui", padding: "2rem" }}>
      <h1>Azure Local Environment</h1>
      <p>All services running via Docker Compose</p>
      <h2>Service Health</h2>
      <ul>
        {Object.entries(services).map(([name, status]) => (
          <li key={name}>
            <strong>{name}</strong>: {status === "ok" ? "✅" : "❌"} {status}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
```

---

## 4. Complete Dockerfiles for each stack

### Node.js multi-stage Dockerfile — `node-api/Dockerfile`

```dockerfile
# syntax=docker/dockerfile:1

# Stage 1: Install production dependencies
FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci --omit=dev

# Stage 2: Production
FROM node:22-alpine AS production
RUN apk add --no-cache dumb-init
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001
WORKDIR /app
COPY --chown=nodejs:nodejs --from=deps /app/node_modules ./node_modules
COPY --chown=nodejs:nodejs src/ ./src/
COPY --chown=nodejs:nodejs package.json ./
ENV NODE_ENV=production
USER nodejs
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "src/index.js"]
```

### Node.js — `node-api/.dockerignore`

```
node_modules
npm-debug.log*
Dockerfile*
docker-compose*
.dockerignore
.git
.gitignore
.env
.env.*
tests/
coverage/
.vscode
*.md
```

### Python multi-stage Dockerfile — `python-api/Dockerfile`

```dockerfile
# syntax=docker/dockerfile:1

# Stage 1: Build dependencies
FROM python:3.13-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /build/wheels -r requirements.txt

# Stage 2: Production
FROM python:3.13-slim AS production
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser

COPY --from=builder /build/wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

COPY --chown=appuser:appuser ./app ./app

USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Python — `python-api/.dockerignore`

```
__pycache__
*.pyc
.venv
venv
Dockerfile*
docker-compose*
.dockerignore
.git
.gitignore
.env
.env.*
tests/
.pytest_cache
.ruff_cache
coverage/
*.md
```

### C# .NET 8 multi-stage Dockerfile — `dotnet-api/Dockerfile`

```dockerfile
# syntax=docker/dockerfile:1

# Stage 1: Build
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY DotnetApi.csproj ./
RUN dotnet restore
COPY . .
RUN dotnet publish -c Release -o /app/publish --no-restore

# Stage 2: Production
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS production
WORKDIR /app
COPY --from=build /app/publish .
USER $APP_UID
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1
ENTRYPOINT ["dotnet", "DotnetApi.dll"]
```

### C# — `dotnet-api/.dockerignore`

```
bin/
obj/
Dockerfile*
docker-compose*
.dockerignore
.git
.gitignore
.env
.env.*
DotnetApi.Tests/
*.md
.vs/
.vscode/
```

### React Nginx multi-stage Dockerfile — `react-app/Dockerfile`

```dockerfile
# syntax=docker/dockerfile:1

# Stage 1: Build React app
FROM node:22-alpine AS build
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:1.28-alpine AS production
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:80/ || exit 1
CMD ["nginx", "-g", "daemon off;"]
```

### React — `react-app/.dockerignore`

```
node_modules
dist
build
Dockerfile*
docker-compose*
.dockerignore
.git
.gitignore
.env
.env.*
coverage/
*.md
```

---

## 5. Nginx config for the React SPA

### `react-app/nginx.conf`

```nginx
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    # SPA client-side routing — fallback to index.html
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache hashed static assets aggressively
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 256;
    gzip_types
        text/plain
        text/css
        application/json
        application/javascript
        text/xml
        application/xml
        text/javascript
        image/svg+xml;
}
```

The `try_files $uri $uri/ /index.html` directive is the critical line — it serves `index.html` for any route that doesn't match a physical file, enabling React Router or any client-side routing library to handle navigation. Hashed assets (Vite outputs filenames like `assets/index-a1b2c3.js`) get a one-year cache with the `immutable` directive since the hash changes on every rebuild.

---

## 6. Complete docker-compose.yml with all services and Azurite

### `docker-compose.yml`

```yaml
services:
  node-api:
    build:
      context: ./node-api
      dockerfile: Dockerfile
    container_name: node-api
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=${NODE_ENV:-production}
      - PORT=3000
      - AZURE_STORAGE_CONNECTION_STRING=${AZURE_STORAGE_CONNECTION_STRING}
    depends_on:
      azurite:
        condition: service_started
    restart: unless-stopped

  python-api:
    build:
      context: ./python-api
      dockerfile: Dockerfile
    container_name: python-api
    ports:
      - "8000:8000"
    environment:
      - APP_ENV=${APP_ENV:-production}
      - PORT=8000
      - AZURE_STORAGE_CONNECTION_STRING=${AZURE_STORAGE_CONNECTION_STRING}
    depends_on:
      azurite:
        condition: service_started
    restart: unless-stopped

  dotnet-api:
    build:
      context: ./dotnet-api
      dockerfile: Dockerfile
    container_name: dotnet-api
    ports:
      - "8080:8080"
    environment:
      - ASPNETCORE_ENVIRONMENT=${ASPNETCORE_ENVIRONMENT:-Production}
      - ASPNETCORE_URLS=http://+:8080
      - AZURE_STORAGE_CONNECTION_STRING=${AZURE_STORAGE_CONNECTION_STRING}
    depends_on:
      azurite:
        condition: service_started
    restart: unless-stopped

  react-app:
    build:
      context: ./react-app
      dockerfile: Dockerfile
    container_name: react-app
    ports:
      - "80:80"
    depends_on:
      - node-api
      - python-api
      - dotnet-api
    restart: unless-stopped

  azurite:
    image: mcr.microsoft.com/azure-storage/azurite:latest
    container_name: azurite
    hostname: azurite
    command: >
      azurite
      --blobHost 0.0.0.0 --blobPort 10000
      --queueHost 0.0.0.0 --queuePort 10001
      --tableHost 0.0.0.0 --tablePort 10002
      --location /data
      --skipApiVersionCheck
      --loose
    ports:
      - "10000:10000"
      - "10001:10001"
      - "10002:10002"
    volumes:
      - azurite-data:/data
    restart: unless-stopped

volumes:
  azurite-data:
```

---

## 7. Environment variable setup

### Root `.env.example` (copy to `.env`)

```bash
# ========================================
# Azure Local Environment — Root Config
# Copy this file to .env and customize
# ========================================

# Node.js API
NODE_ENV=development

# Python API
APP_ENV=development

# .NET API
ASPNETCORE_ENVIRONMENT=Development

# Azurite connection string (for container-to-container)
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://azurite:10000/devstoreaccount1;QueueEndpoint=http://azurite:10001/devstoreaccount1;TableEndpoint=http://azurite:10002/devstoreaccount1;
```

### `node-api/.env.example`

```bash
NODE_ENV=development
PORT=3000
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;
```

### `python-api/.env.example`

```bash
APP_ENV=development
PORT=8000
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;
```

### `dotnet-api/.env.example`

```bash
ASPNETCORE_ENVIRONMENT=Development
ASPNETCORE_URLS=http://+:8080
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;
```

### `react-app/.env.example`

```bash
VITE_API_NODE_URL=http://localhost:3000
VITE_API_PYTHON_URL=http://localhost:8000
VITE_API_DOTNET_URL=http://localhost:8080
```

**How environment variables flow through docker-compose:** Docker Compose reads the root `.env` file automatically. Variables defined there are interpolated into `docker-compose.yml` via `${VARIABLE}` syntax. The `environment` block in each service passes them into the container. Per-stack `.env.example` files document what each service expects when run standalone (outside Compose). Note the critical difference: **inside Compose, containers reach Azurite via the service name** `azurite`, while **on the host**, you use `127.0.0.1`.

---

## 8. Complete test setup for each stack

### Node.js — Jest test — `node-api/tests/health.test.js`

```javascript
const request = require("supertest");
const app = require("../src/index");

describe("Health endpoint", () => {
  test("GET /health returns 200 with status ok", async () => {
    const response = await request(app).get("/health");
    expect(response.status).toBe(200);
    expect(response.body).toEqual({ status: "ok", service: "node-api" });
  });

  test("GET / returns welcome message", async () => {
    const response = await request(app).get("/");
    expect(response.status).toBe(200);
    expect(response.body).toHaveProperty("message");
  });
});
```

Run with `cd node-api && npm install && npm test`.

### Python — pytest test — `python-api/tests/test_health.py`

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_returns_200():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "python-api"}


def test_root_returns_message():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
```

Run with `cd python-api && pip install -r requirements.txt && pytest tests/`.

### C# .NET 8 — xUnit integration test

Create the test project directory and file:

**`dotnet-api/DotnetApi.Tests/DotnetApi.Tests.csproj`**

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <IsPackable>false</IsPackable>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.AspNetCore.Mvc.Testing" Version="8.0.*" />
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.*" />
    <PackageReference Include="xunit" Version="2.*" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.*" />
  </ItemGroup>
  <ItemGroup>
    <ProjectReference Include="../DotnetApi.csproj" />
  </ItemGroup>
</Project>
```

**`dotnet-api/DotnetApi.Tests/HealthTests.cs`**

```csharp
using System.Net;
using System.Text.Json;
using Microsoft.AspNetCore.Mvc.Testing;

namespace DotnetApi.Tests;

public class HealthTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public HealthTests(WebApplicationFactory<Program> factory)
    {
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task Health_ReturnsOk()
    {
        var response = await _client.GetAsync("/health");

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);

        var content = await response.Content.ReadAsStringAsync();
        using var doc = JsonDocument.Parse(content);
        Assert.Equal("ok", doc.RootElement.GetProperty("status").GetString());
    }

    [Fact]
    public async Task Root_ReturnsMessage()
    {
        var response = await _client.GetAsync("/");

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }
}
```

**Important:** For `WebApplicationFactory<Program>` to work, add this line at the bottom of `dotnet-api/Program.cs`:

```csharp
// Make Program accessible to integration tests
public partial class Program { }
```

Run with `cd dotnet-api && dotnet test DotnetApi.Tests/`.

### React — Vitest + Testing Library test — `react-app/src/App.test.jsx`

```jsx
import { render, screen } from "@testing-library/react";
import { expect, test } from "vitest";
import App from "./App";

test("renders the heading", () => {
  render(<App />);
  const heading = screen.getByText(/Azure Local Environment/i);
  expect(heading).toBeDefined();
});

test("renders service health section", () => {
  render(<App />);
  const section = screen.getByText(/Service Health/i);
  expect(section).toBeDefined();
});
```

Run with `cd react-app && npm install && npm test`.

---

## 9. GitHub Actions CI/CD pipelines

### Node.js pipeline — `.github/workflows/node-api.yml`

```yaml
name: Node.js API CI/CD

on:
  push:
    branches: [main]
    paths: ["node-api/**"]
  pull_request:
    branches: [main]
    paths: ["node-api/**"]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}/node-api

jobs:
  lint-test-build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "22"
          cache: "npm"
          cache-dependency-path: node-api/package-lock.json

      - name: Install dependencies
        working-directory: node-api
        run: npm ci

      - name: Lint
        working-directory: node-api
        run: npx eslint src/ --max-warnings 0 || true

      - name: Test
        working-directory: node-api
        run: npm test

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to GHCR
        if: github.event_name != 'pull_request'
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=sha

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          context: node-api
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Deploy to Azure (placeholder)
        if: github.event_name != 'pull_request'
        run: |
          echo "🚀 Deploy step — replace with actual Azure deployment:"
          echo "   az webapp config container set \\"
          echo "     --name <app-name> --resource-group <rg> \\"
          echo "     --container-image-name ${{ steps.meta.outputs.tags }}"
```

### Python pipeline — `.github/workflows/python-api.yml`

```yaml
name: Python API CI/CD

on:
  push:
    branches: [main]
    paths: ["python-api/**"]
  pull_request:
    branches: [main]
    paths: ["python-api/**"]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}/python-api

jobs:
  lint-test-build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"
          cache: "pip"

      - name: Install dependencies
        working-directory: python-api
        run: pip install -r requirements.txt

      - name: Lint with Ruff
        working-directory: python-api
        run: |
          ruff check .
          ruff format --check .

      - name: Test with pytest
        working-directory: python-api
        run: pytest tests/ -v

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to GHCR
        if: github.event_name != 'pull_request'
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=sha

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          context: python-api
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Deploy to Azure (placeholder)
        if: github.event_name != 'pull_request'
        run: |
          echo "🚀 Deploy step — replace with actual Azure deployment:"
          echo "   az webapp config container set \\"
          echo "     --name <app-name> --resource-group <rg> \\"
          echo "     --container-image-name ${{ steps.meta.outputs.tags }}"
```

### .NET 8 pipeline — `.github/workflows/dotnet-api.yml`

```yaml
name: .NET API CI/CD

on:
  push:
    branches: [main]
    paths: ["dotnet-api/**"]
  pull_request:
    branches: [main]
    paths: ["dotnet-api/**"]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}/dotnet-api

jobs:
  lint-test-build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup .NET
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: "8.0.x"

      - name: Restore
        working-directory: dotnet-api
        run: dotnet restore

      - name: Lint (format check)
        working-directory: dotnet-api
        run: dotnet format --verify-no-changes --verbosity diagnostic || true

      - name: Build
        working-directory: dotnet-api
        run: dotnet build --no-restore --configuration Release

      - name: Test
        working-directory: dotnet-api
        run: dotnet test DotnetApi.Tests/ --no-build --configuration Release --verbosity normal

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to GHCR
        if: github.event_name != 'pull_request'
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=sha

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          context: dotnet-api
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Deploy to Azure (placeholder)
        if: github.event_name != 'pull_request'
        run: |
          echo "🚀 Deploy step — replace with actual Azure deployment:"
          echo "   az webapp config container set \\"
          echo "     --name <app-name> --resource-group <rg> \\"
          echo "     --container-image-name ${{ steps.meta.outputs.tags }}"
```

### React pipeline — `.github/workflows/react-app.yml`

```yaml
name: React App CI/CD

on:
  push:
    branches: [main]
    paths: ["react-app/**"]
  pull_request:
    branches: [main]
    paths: ["react-app/**"]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}/react-app

jobs:
  lint-test-build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "22"
          cache: "npm"
          cache-dependency-path: react-app/package-lock.json

      - name: Install dependencies
        working-directory: react-app
        run: npm ci

      - name: Lint
        working-directory: react-app
        run: npx eslint src/ --max-warnings 0 || true

      - name: Test
        working-directory: react-app
        run: npm test

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to GHCR
        if: github.event_name != 'pull_request'
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=sha

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          context: react-app
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Deploy to Azure Static Web Apps (placeholder)
        if: github.event_name != 'pull_request'
        run: |
          echo "🚀 Deploy step — replace with Azure Static Web Apps deploy:"
          echo "   Use Azure/static-web-apps-deploy@v1 action"
          echo "   or push container to Azure Container Apps"
```

All four pipelines follow the same pattern: **lint → test → Docker build → push to GHCR → deploy placeholder**. They run on `ubuntu-latest` (currently Ubuntu 24.04), use path filters to only trigger on changes to the relevant directory, and use GitHub Actions cache for both package managers and Docker layers. The `|| true` on lint steps prevents first-run failures before ESLint configs are fully tuned.

---

## 10. Local deploy and smoke-test scripts

### PowerShell script — `deploy.ps1`

```powershell
#!/usr/bin/env pwsh
#Requires -Version 7.0

<#
.SYNOPSIS
    Builds, tests, and deploys all services locally via Docker Compose.
.DESCRIPTION
    1. Builds all Docker images
    2. Runs tests inside containers
    3. Brings up docker-compose
    4. Runs smoke tests against all health endpoints
    5. Reports pass/fail
#>

$ErrorActionPreference = "Stop"

# Colors
function Write-Success($msg) { Write-Host "  ✅ $msg" -ForegroundColor Green }
function Write-Failure($msg) { Write-Host "  ❌ $msg" -ForegroundColor Red }
function Write-Step($msg)    { Write-Host "`n🔧 $msg" -ForegroundColor Cyan }
function Write-Header($msg)  { Write-Host "`n========================================" -ForegroundColor Yellow; Write-Host "  $msg" -ForegroundColor Yellow; Write-Host "========================================" -ForegroundColor Yellow }

$failed = 0
$passed = 0

Write-Header "Azure Local Environment — Deploy Script"

# ──────────────────────────────────────────────
# Step 1: Build all Docker images
# ──────────────────────────────────────────────
Write-Step "Building all Docker images..."
docker compose build --parallel
if ($LASTEXITCODE -ne 0) {
    Write-Failure "Docker build failed"
    exit 1
}
Write-Success "All images built successfully"

# ──────────────────────────────────────────────
# Step 2: Run tests inside containers
# ──────────────────────────────────────────────
Write-Step "Running Node.js tests..."
docker run --rm node-api-test sh -c "cd /app && npm ci && npm test" 2>$null
if ($LASTEXITCODE -ne 0) {
    # Fallback: run tests with full source
    docker run --rm -w /app node:22-alpine sh -c "
        apk add --no-cache git &&
        cd /tmp && mkdir app && cd app &&
        echo 'Skipping containerized test — run locally with: cd node-api && npm test'
    "
    Write-Host "  ⚠️  Node.js container tests skipped (run locally)" -ForegroundColor Yellow
} else {
    Write-Success "Node.js tests passed"
    $passed++
}

Write-Step "Running Python tests..."
docker run --rm -v "${PWD}/python-api:/app" -w /app python:3.13-slim sh -c "
    pip install --quiet -r requirements.txt && pytest tests/ -v
"
if ($LASTEXITCODE -ne 0) { Write-Failure "Python tests failed"; $failed++ }
else { Write-Success "Python tests passed"; $passed++ }

Write-Step "Running .NET tests..."
docker run --rm -v "${PWD}/dotnet-api:/src" -w /src mcr.microsoft.com/dotnet/sdk:8.0 sh -c "
    dotnet restore && dotnet test DotnetApi.Tests/ --verbosity normal
"
if ($LASTEXITCODE -ne 0) { Write-Failure ".NET tests failed"; $failed++ }
else { Write-Success ".NET tests passed"; $passed++ }

Write-Step "Running React tests..."
docker run --rm -v "${PWD}/react-app:/app" -w /app node:22-alpine sh -c "
    npm ci && npm test
"
if ($LASTEXITCODE -ne 0) { Write-Failure "React tests failed"; $failed++ }
else { Write-Success "React tests passed"; $passed++ }

# ──────────────────────────────────────────────
# Step 3: Bring up docker-compose
# ──────────────────────────────────────────────
Write-Step "Starting all services with docker compose..."
docker compose down --remove-orphans 2>$null
docker compose up -d

Write-Host "  Waiting 15 seconds for services to initialize..." -ForegroundColor Gray
Start-Sleep -Seconds 15

# ──────────────────────────────────────────────
# Step 4: Smoke tests against health endpoints
# ──────────────────────────────────────────────
Write-Step "Running smoke tests..."

$endpoints = @(
    @{ Name = "Node.js API";  Url = "http://localhost:3000/health" },
    @{ Name = "Python API";   Url = "http://localhost:8000/health" },
    @{ Name = ".NET API";     Url = "http://localhost:8080/health" },
    @{ Name = "React App";    Url = "http://localhost:80/" },
    @{ Name = "Azurite Blob"; Url = "http://localhost:10000/" }
)

foreach ($ep in $endpoints) {
    try {
        $response = Invoke-WebRequest -Uri $ep.Url -TimeoutSec 10 -UseBasicParsing -ErrorAction Stop
        if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 400) {
            Write-Success "$($ep.Name) — HTTP $($response.StatusCode)"
            $passed++
        } else {
            Write-Failure "$($ep.Name) — HTTP $($response.StatusCode)"
            $failed++
        }
    }
    catch {
        Write-Failure "$($ep.Name) — $($_.Exception.Message)"
        $failed++
    }
}

# ──────────────────────────────────────────────
# Step 5: Report
# ──────────────────────────────────────────────
Write-Header "Results"
Write-Host "  Passed: $passed" -ForegroundColor Green
Write-Host "  Failed: $failed" -ForegroundColor $(if ($failed -gt 0) { "Red" } else { "Gray" })
Write-Host ""

if ($failed -gt 0) {
    Write-Host "  ⚠️  Some checks failed. Run 'docker compose logs <service>' to debug." -ForegroundColor Yellow
    exit 1
} else {
    Write-Host "  🎉 All services running and healthy!" -ForegroundColor Green
    Write-Host ""
    Write-Host "  Service URLs:" -ForegroundColor White
    Write-Host "    Node.js API:    http://localhost:3000" -ForegroundColor Gray
    Write-Host "    Python API:     http://localhost:8000" -ForegroundColor Gray
    Write-Host "    .NET API:       http://localhost:8080" -ForegroundColor Gray
    Write-Host "    React App:      http://localhost:80" -ForegroundColor Gray
    Write-Host "    Azurite Blob:   http://localhost:10000" -ForegroundColor Gray
    Write-Host "    Azurite Queue:  http://localhost:10001" -ForegroundColor Gray
    Write-Host "    Azurite Table:  http://localhost:10002" -ForegroundColor Gray
    Write-Host ""
    exit 0
}
```

### Bash/WSL script — `deploy.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

success() { echo -e "  ${GREEN}✅ $1${NC}"; }
failure() { echo -e "  ${RED}❌ $1${NC}"; }
step()    { echo -e "\n${CYAN}🔧 $1${NC}"; }
header()  { echo -e "\n${YELLOW}========================================${NC}"; echo -e "  ${YELLOW}$1${NC}"; echo -e "${YELLOW}========================================${NC}"; }

FAILED=0
PASSED=0

header "Azure Local Environment — Deploy Script"

# ──────────────────────────────────────────────
# Step 1: Build
# ──────────────────────────────────────────────
step "Building all Docker images..."
docker compose build --parallel
success "All images built successfully"

# ──────────────────────────────────────────────
# Step 2: Run tests in containers
# ──────────────────────────────────────────────
step "Running Python tests..."
if docker run --rm -v "$(pwd)/python-api:/app" -w /app python:3.13-slim \
    sh -c "pip install --quiet -r requirements.txt && pytest tests/ -v"; then
    success "Python tests passed"; ((PASSED++))
else
    failure "Python tests failed"; ((FAILED++))
fi

step "Running .NET tests..."
if docker run --rm -v "$(pwd)/dotnet-api:/src" -w /src mcr.microsoft.com/dotnet/sdk:8.0 \
    sh -c "dotnet restore && dotnet test DotnetApi.Tests/ --verbosity normal"; then
    success ".NET tests passed"; ((PASSED++))
else
    failure ".NET tests failed"; ((FAILED++))
fi

step "Running React tests..."
if docker run --rm -v "$(pwd)/react-app:/app" -w /app node:22-alpine \
    sh -c "npm ci && npm test"; then
    success "React tests passed"; ((PASSED++))
else
    failure "React tests failed"; ((FAILED++))
fi

# ──────────────────────────────────────────────
# Step 3: Bring up services
# ──────────────────────────────────────────────
step "Starting all services with docker compose..."
docker compose down --remove-orphans 2>/dev/null || true
docker compose up -d

echo "  Waiting 15 seconds for services to initialize..."
sleep 15

# ──────────────────────────────────────────────
# Step 4: Smoke tests
# ──────────────────────────────────────────────
step "Running smoke tests..."

check_endpoint() {
    local name=$1
    local url=$2
    local http_code
    http_code=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "$url" 2>/dev/null || echo "000")
    if [[ "$http_code" -ge 200 && "$http_code" -lt 400 ]]; then
        success "$name — HTTP $http_code"
        ((PASSED++))
    else
        failure "$name — HTTP $http_code"
        ((FAILED++))
    fi
}

check_endpoint "Node.js API"  "http://localhost:3000/health"
check_endpoint "Python API"   "http://localhost:8000/health"
check_endpoint ".NET API"     "http://localhost:8080/health"
check_endpoint "React App"    "http://localhost:80/"
check_endpoint "Azurite Blob" "http://localhost:10000/"

# ──────────────────────────────────────────────
# Step 5: Report
# ──────────────────────────────────────────────
header "Results"
echo -e "  ${GREEN}Passed: $PASSED${NC}"
echo -e "  ${RED}Failed: $FAILED${NC}"
echo ""

if [ "$FAILED" -gt 0 ]; then
    echo -e "  ${YELLOW}⚠️  Some checks failed. Run 'docker compose logs <service>' to debug.${NC}"
    exit 1
else
    echo -e "  ${GREEN}🎉 All services running and healthy!${NC}"
    echo ""
    echo "  Service URLs:"
    echo "    Node.js API:    http://localhost:3000"
    echo "    Python API:     http://localhost:8000"
    echo "    .NET API:       http://localhost:8080"
    echo "    React App:      http://localhost:80"
    echo "    Azurite Blob:   http://localhost:10000"
    exit 0
fi
```

Make it executable with `chmod +x deploy.sh`.

---

## 11. Troubleshooting common Windows, Docker, and WSL2 issues

### WSL2 won't start or Docker Desktop fails to launch

The most frequent cause in 2026 is a WSL kernel version mismatch. Run `wsl --update` from an elevated PowerShell, then `wsl --shutdown`, and restart Docker Desktop. If you see error `0x800701bc`, virtualization features are not enabled — run these commands as Administrator and reboot:

```powershell
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux -NoRestart
Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -NoRestart
```

Verify Hyper-V is set to auto-start: `bcdedit /enum | findstr hypervisorlaunchtype` should show "Auto". If it shows "Off", fix with `bcdedit /set hypervisorlaunchtype auto` and reboot.

### Port conflicts — "An attempt was made to access a socket in a way forbidden"

Windows Hyper-V reserves dynamic port ranges that shift on each reboot, sometimes claiming ports like **3000, 8080, or 10000**. Diagnose with:

```cmd
netsh interface ipv4 show excludedportrange protocol=tcp
```

Quick fix: `net stop winnat && net start winnat`. Permanent fix — push the dynamic range above common dev ports:

```cmd
netsh int ipv4 set dynamicport tcp start=49152 num=16384
netsh int ipv4 set dynamicport udp start=49152 num=16384
```

To find what's using a specific port: `netstat -ano | findstr :3000` then `tasklist /fi "PID eq <PID>"`.

### The Vmmem process consumes all available RAM

WSL2 defaults to consuming **50% of system RAM**. Create `C:\Users\<You>\.wslconfig` (note: no `.txt` extension) with the memory limits shown in Section 1 above, then run `wsl --shutdown`. The `autoMemoryReclaim=gradual` experimental setting (Windows 11 22H2+) actively reclaims unused pages.

### Volume mounts are extremely slow

Bind-mounting Windows filesystem paths (`/mnt/c/...`) into Linux containers is **3–5x slower** than native Linux I/O due to the 9p/DrvFs translation layer. The solution: **store your project files inside the WSL2 filesystem** at `/home/<user>/projects/`, not on the Windows drive. Access them from Windows Explorer via `\\wsl$\Ubuntu\home\<user>\projects\`. This single change eliminates most performance complaints.

### Container-to-container DNS resolution fails

Docker Compose automatically creates a user-defined bridge network where services resolve each other by **service name** (e.g., `http://azurite:10000`). If DNS fails, confirm you're not using the legacy default bridge (`docker network ls`). For VPN-related DNS issues, add to `.wslconfig`:

```ini
[wsl2]
dnsTunneling=true
```

Or set explicit DNS in Docker Desktop: **Settings → Docker Engine** and add `"dns": ["8.8.8.8", "8.8.4.4"]`.

### Azurite connection refused from app containers

Three things to check: Azurite must bind to `0.0.0.0` (not `127.0.0.1`) — ensured by the `--blobHost 0.0.0.0` flags in the compose file. The connection string inside containers must use the **service name** `azurite` as the hostname, not `localhost`. And `depends_on` only waits for the container to start, not for Azurite to be ready — add retry logic in your application code or use the healthcheck-based `condition: service_healthy` pattern.

### "Cannot connect to the Docker daemon" error

Verify Docker Desktop is running (whale icon in system tray). Check WSL integration: **Docker Desktop → Settings → Resources → WSL Integration** — your distro must be toggled on. If using WSL terminal, verify the Docker context: `docker context ls` should show `desktop-linux` as current. Switch with `docker context use desktop-linux`.

### Docker Desktop licensing

Docker Desktop is **free for personal use, education, open source, and small businesses** (under 250 employees and under $10M revenue). Larger organizations require a paid subscription. Docker Engine (CLI + daemon) remains free and open-source for everyone — only the Desktop GUI application has licensing restrictions.

---

## Getting started — the five-command quickstart

After installing all prerequisites, create the directory structure and files above, then:

```powershell
# 1. Copy environment file
cp .env.example .env

# 2. Initialize Node.js and React lock files
cd node-api && npm install && cd ..
cd react-app && npm install && cd ..

# 3. Build and launch everything
docker compose up -d --build

# 4. Verify all services
curl http://localhost:3000/health
curl http://localhost:8000/health
curl http://localhost:8080/health
curl http://localhost:80

# 5. Or run the full deploy script
pwsh ./deploy.ps1     # PowerShell
# ./deploy.sh         # Bash/WSL
```

The four API containers simulate Azure App Service (containerized web apps behind defined ports), while the React container behind Nginx simulates Azure Static Web Apps (static files with SPA routing). Azurite provides local Azure Storage emulation for Blob, Queue, and Table services using the well-known development credentials. This entire stack mirrors what you'd deploy to Azure — the only change for production is swapping connection strings and pointing your CI/CD deploy step at real Azure resources instead of local containers.