# Module 01 — Repository Foundation and Runtime Environment

## Goal
Establish a robust, reproducible monorepo runtime environment for **Company Brain**, including the Docker Compose service stack (FalkorDB, FastAPI backend, React frontend), validated environment configuration, and structured health telemetry.

---

## 1. Concrete Directory Architecture

Create and maintain this file organization:

```text
company-brain/
├── docker-compose.yml              # Local orchestration for FalkorDB, Backend, Frontend
├── .env.example                    # Template environment variables
├── .gitignore                      # Git ignore rules for Python, Node, OS, & secrets
├── README.md                       # Master build guide and system architecture
├── backend/
│   ├── Dockerfile                  # Python 3.12-slim container build
│   ├── pyproject.toml              # Dependencies & tool configurations
│   ├── requirements.txt            # Pinned pip requirements
│   └── app/
│       ├── __init__.py
│       ├── main.py                 # FastAPI application factory & lifespan
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py           # Pydantic BaseSettings with env validation
│       │   └── logging.py          # Structured JSON logger
│       ├── api/
│       │   ├── __init__.py
│       │   ├── router.py           # Root APIRouter mounting all sub-routes
│       │   └── endpoints/
│       │       ├── __init__.py
│       │       └── health.py       # GET /api/health implementation
│       └── models/
│           ├── __init__.py
│           └── health.py           # HealthResponse Pydantic schema
├── frontend/
│   ├── Dockerfile                  # Node 20 alpine container build
│   ├── package.json                # React 18, Vite, Tailwind, @xyflow/react
│   ├── tsconfig.json               # Strict TypeScript configuration
│   ├── vite.config.ts              # Vite dev server & backend API proxy
│   ├── tailwind.config.js          # Tailwind CSS theme tokens
│   ├── index.html                  # HTML entrypoint
│   └── src/
│       ├── main.tsx                # React DOM mount
│       ├── App.tsx                 # App layout, navigation header & tab router
│       ├── index.css               # Tailwind directives & CSS custom properties
│       └── components/
│           ├── Navbar.tsx          # Navigation header with system health pill
│           └── HealthBadge.tsx     # FalkorDB & Backend connection status badge
├── docs/
│   ├── ARCHITECTURE.md             # System design and component interactions
│   └── TECH_DECISIONS.md           # Architecture Decision Records (ADRs)
└── modules/
    └── README_01_FOUNDATION.md     # This specification
```

---

## 2. Environment Configuration (`.env.example`)

Create `.env.example` with strict typing and clear descriptions:

```bash
# ==============================================================================
# COMPANY BRAIN — ENVIRONMENT CONFIGURATION TEMPLATE
# Copy this file to .env and configure appropriate values before running.
# Never commit the actual .env file containing real API keys or credentials.
# ==============================================================================

# Application Environment
APP_ENV=development                 # 'development' | 'staging' | 'production' | 'test'
LOG_LEVEL=INFO                      # 'DEBUG' | 'INFO' | 'WARNING' | 'ERROR'
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
FRONTEND_PORT=5173

# CORS Configuration (comma-separated origins)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173

# FalkorDB Configuration
FALKORDB_HOST=falkordb              # Use 'localhost' when running backend outside Docker
FALKORDB_PORT=6379
FALKORDB_PASSWORD=                  # Leave blank for default local Docker setup
FALKORDB_GRAPH=company_brain        # Target graph database key in FalkorDB
FALKORDB_MAX_CONNECTIONS=20

# AI / LLM Configuration
# Required for entity extraction, retrieval synthesis, and GraphRAG
GOOGLE_API_KEY=your_gemini_api_key_here
LLM_MODEL=gemini-1.5-flash          # Recommended stable low-latency model
EMBEDDING_MODEL=text-embedding-004  # Gemini embedding model for chunk similarity

# Ingestion Constraints
MAX_UPLOAD_SIZE_MB=25
MAX_CHUNKS_PER_DOCUMENT=500
CHUNK_SIZE_TOKENS=600
CHUNK_OVERLAP_TOKENS=100
```

---

## 3. Container Orchestration (`docker-compose.yml`)

The complete multi-container service definition:

```yaml
version: '3.8'

services:
  # ----------------------------------------------------------------------------
  # 1. FalkorDB Primary Graph Database
  # ----------------------------------------------------------------------------
  falkordb:
    image: falkordb/falkordb:latest
    container_name: company_brain_falkordb
    ports:
      - "6379:6379"
    volumes:
      - falkordb_data:/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5
    networks:
      - company_brain_net

  # ----------------------------------------------------------------------------
  # 2. FastAPI Backend Service
  # ----------------------------------------------------------------------------
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: company_brain_backend
    ports:
      - "8000:8000"
    environment:
      - APP_ENV=development
      - FALKORDB_HOST=falkordb
      - FALKORDB_PORT=6379
      - FALKORDB_GRAPH=company_brain
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - LLM_MODEL=${LLM_MODEL:-gemini-1.5-flash}
      - CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
    volumes:
      - ./backend:/app
    depends_on:
      falkordb:
        condition: service_healthy
    restart: unless-stopped
    networks:
      - company_brain_net

  # ----------------------------------------------------------------------------
  # 3. React + Vite Frontend UI
  # ----------------------------------------------------------------------------
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: company_brain_frontend
    ports:
      - "5173:5173"
    environment:
      - VITE_API_BASE_URL=http://localhost:8000/api
    volumes:
      - ./frontend:/app
      - /app/node_modules
    depends_on:
      - backend
    restart: unless-stopped
    networks:
      - company_brain_net

volumes:
  falkordb_data:

networks:
  company_brain_net:
    driver: bridge
```

---

## 4. Backend Health Endpoint Specifications

### Pydantic Model (`app/models/health.py`)
```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any

class HealthResponse(BaseModel):
    status: str = Field(default="healthy", description="Status string: healthy, degraded, or unhealthy")
    version: str = Field(default="1.0.0", description="Company Brain build version")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    environment: str = Field(..., description="Active runtime environment (development, production)")
    falkordb: Dict[str, Any] = Field(..., description="FalkorDB connection and node count telemetry")
```

### Route Handler (`app/api/endpoints/health.py`)
The health endpoint must verify active connectivity to FalkorDB and return node counts:
```python
@router.get("/health", response_model=HealthResponse)
async def check_health(falkor: FalkorDBService = Depends(get_falkor_service)):
    is_connected, node_count = await falkor.ping_and_count()
    return HealthResponse(
        status="healthy" if is_connected else "degraded",
        version="1.0.0",
        environment=settings.APP_ENV,
        falkordb={
            "connected": is_connected,
            "host": settings.FALKORDB_HOST,
            "port": settings.FALKORDB_PORT,
            "graph_name": settings.FALKORDB_GRAPH,
            "total_nodes": node_count if is_connected else 0
        }
    )
```

---

## 5. Startup and Verification Instructions

### Option A: Running with Docker Compose (Recommended)

1. **Configure Environment Variables**:
   ```bash
   cp .env.example .env
   # Add your GOOGLE_API_KEY into .env
   ```
2. **Build and Start All Services**:
   ```bash
   docker compose up --build -d
   ```
3. **Verify Service Health**:
   - Backend: `curl http://localhost:8000/api/health`
   - FalkorDB: `docker exec -it company_brain_falkordb redis-cli ping` (Returns `PONG`)
   - Frontend: Open `http://localhost:5173` in your browser.

### Option B: Local Native Setup (Windows PowerShell)

1. **Start FalkorDB Container only**:
   ```powershell
   docker run -d -p 6379:6379 --name falkordb_local falkordb/falkordb:latest
   ```
2. **Setup Backend**:
   ```powershell
   cd backend
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   $env:FALKORDB_HOST="localhost"
   $env:FALKORDB_PORT="6379"
   uvicorn app.main:app --reload --port 8000
   ```
3. **Setup Frontend**:
   ```powershell
   cd ..\frontend
   npm install
   npm run dev
   ```

---

## 6. Acceptance Criteria
- [x] Repository matches the layout specified in Section 1.
- [x] `.env.example` contains complete configuration variables with no secrets committed.
- [x] `docker compose up` starts FalkorDB, Backend, and Frontend without errors.
- [x] `GET /api/health` returns HTTP 200 with structured JSON reporting FalkorDB connectivity.
- [x] Frontend shell loads at `http://localhost:5173` with functional navigation tabs and live backend status indicator.
- [x] Missing or invalid `.env` configuration triggers clean startup error messages explaining the missing key.
