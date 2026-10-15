# Module 01 — Repository Foundation and Runtime

## Goal
Create a clean, runnable monorepo foundation for Company Brain. Do not implement advanced GraphRAG behavior yet.

## Stack
- Frontend: React, TypeScript, Vite, Tailwind CSS, shadcn/ui where useful.
- Backend: Python 3.12, FastAPI, Pydantic, Uvicorn.
- Database: FalkorDB through Docker Compose.
- Tests: pytest; frontend test tooling may be added when needed.
- Packaging: Docker Compose.

## Tasks
1. Inspect the current repository before changing files.
2. Create the repository structure defined in the root README.
3. Create backend application entry point and `GET /api/health`.
4. Create frontend shell with navigation for Chat, Graph Explorer, Sources, and Decisions.
5. Add shared configuration via environment variables and `.env.example`.
6. Add `.gitignore` for `.env`, virtual environments, node_modules, caches, uploads, and generated files.
7. Add Docker Compose services for FalkorDB, backend, and frontend. Use health checks and service dependencies where supported.
8. Add startup instructions for Windows PowerShell and Unix-like shells.
9. Ensure errors are readable and configuration is validated at startup.
10. Create `docs/ARCHITECTURE.md` and `docs/TECH_DECISIONS.md`.

## Environment variables
At minimum document:
- `FALKORDB_HOST`
- `FALKORDB_PORT`
- `FALKORDB_USERNAME` (optional if the chosen deployment needs it)
- `FALKORDB_PASSWORD` (optional if the chosen deployment needs it)
- `FALKORDB_GRAPH`
- `GOOGLE_API_KEY` or the selected provider key
- `LLM_MODEL`
- `EMBEDDING_MODEL`
- `APP_ENV`
- `CORS_ORIGINS`

Do not commit actual keys. Use placeholders only.

## Acceptance criteria
- Backend starts and `GET /api/health` returns a structured healthy response.
- Frontend loads and shows a functional shell, not a static screenshot.
- FalkorDB starts through Docker Compose.
- Configuration errors explain which variable is missing without printing secrets.
- A clean setup can be followed from the docs.
- No feature is labelled complete when it is only a placeholder.

## Out of scope
- Real document ingestion
- Graph schema implementation
- Agent reasoning
