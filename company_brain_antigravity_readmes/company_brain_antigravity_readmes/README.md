# Company Brain — Master Build Prompt for Antigravity

## 1. Your role

Act as the lead software architect and implementation engineer. Build **Company Brain**, a graph-native organizational intelligence agent for the FalkorDB Graph Hacks **Company Brain** track.

This repository must become a working, integrated application—not a collection of mock screens or disconnected modules. Follow the module READMEs in the `modules/` directory. Read this file first, then implement modules in the order given below.

## 2. Product objective

Build an agent that understands how a fictional or authorized company works by connecting:
- People and their skills
- Teams and membership
- Projects and services
- Documents, chats, tickets, and source records
- Decisions and their rationale
- Incidents and resolutions
- Dependencies and ownership

The agent must answer questions with traceable evidence, explain relevant graph paths, identify owners and potential experts, show decision history, flag conflicting or stale knowledge, and identify potentially affected projects/services.

Example user questions:
- “Who owns the payment service, and what evidence confirms that?”
- “Why did the team choose PostgreSQL?”
- “Who has previously resolved incidents similar to this one?”
- “Which services could be affected if this API changes?”
- “The old decision says X but the newer document says Y. Which is current, and why?”

## 3. Non-negotiable requirements

1. **FalkorDB is the primary graph database.** Graph queries and relationships must materially drive the application’s answers. The product must lose core capabilities if FalkorDB is removed; the graph must not be decorative.
2. Every important answer claim must have evidence, ideally including source title, source ID/URL, excerpt, timestamp, and graph path where applicable.
3. Never fabricate a source, person, relationship, date, owner, decision, or confidence score.
4. Distinguish explicit facts from inferred expertise or inferred relationships.
5. Handle missing, conflicting, and stale evidence honestly. Say when the system cannot determine an answer.
6. Preserve source provenance from ingestion to final response.
7. Build against public, synthetic, or otherwise authorized data only. Do not ingest private, login-protected, paywalled, personal, or restricted data without authorization.
8. Do not commit API keys or credentials.
9. Keep the application understandable and explainable. Avoid unnecessary multi-agent complexity.
10. AI coding tools may be used, but the team must understand, test, verify, and disclose their use according to hackathon rules.

## 4. Finalized technology stack

Use this baseline unless a compatibility check proves an item cannot work. If an item must change, explain why in `docs/TECH_DECISIONS.md` and update all relevant module docs.

### Frontend
- React
- TypeScript
- Vite
- Tailwind CSS
- shadcn/ui where suitable
- `@xyflow/react` for interactive graph exploration
- A typed API client and reusable loading/error/empty states

### Backend
- Python 3.12
- FastAPI
- Pydantic
- Uvicorn
- `python-dotenv`
- pytest

### Knowledge graph and GraphRAG
- FalkorDB as the primary graph database
- Cypher for graph queries and graph algorithms
- FalkorDB GraphRAG SDK (`graphrag-sdk`) for supported ingestion/retrieval functionality
- Use the SDK's documented APIs and verify installed-version compatibility before coding against examples
- Extend with custom graph queries and business logic where needed

### Models
- Use a provider adapter rather than hard-coding model calls throughout the codebase.
- Preferred LLM: a currently available, stable Gemini Flash model supported by the configured provider/SDK.
- Preferred embedding option: a currently supported Gemini embedding model, if compatible with the selected SDK adapter.
- **Do not assume model IDs or SDK support.** At setup, verify model IDs using current official provider documentation and a minimal API smoke test. Store model IDs in environment variables.
- Provide a configurable alternative provider/model where practical. Do not invent model IDs or claim a model works without testing.
- If the selected GraphRAG SDK version does not support the preferred provider directly, implement a small adapter following the documented interface or select a supported model. Do not redesign the graph layer because of a model-provider change.

### Parsing and packaging
- PyMuPDF for PDFs
- python-docx for DOCX
- Markdown and plain-text parsers
- Docker and Docker Compose
- Do not add a separate vector database, Redis, Kafka, or SQL database in the MVP unless a demonstrated requirement demands it. Prefer FalkorDB's graph/vector/full-text capabilities where supported by the installed version.

## 5. Required repository layout

Create and maintain this structure:

```text
company-brain/
├── README.md
├── .env.example
├── .gitignore
├── docker-compose.yml
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   └── src/
├── backend/
│   ├── pyproject.toml or requirements.txt
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── services/
│   │   ├── graph/
│   │   ├── ingestion/
│   │   ├── retrieval/
│   │   └── tests/
├── data/
│   ├── sample/
│   └── README.md
├── docs/
│   ├── ARCHITECTURE.md
│   ├── GRAPH_SCHEMA.md
│   ├── API_CONTRACT.md
│   ├── TECH_DECISIONS.md
│   └── DEMO_SCRIPT.md
└── modules/
    ├── README_00_MASTER.md
    ├── README_01_FOUNDATION.md
    ├── README_02_GRAPH_SCHEMA.md
    ├── README_03_INGESTION.md
    ├── README_04_RETRIEVAL_AGENT.md
    ├── README_05_EVIDENCE_FRESHNESS.md
    ├── README_06_FRONTEND.md
    ├── README_07_API_INTEGRATION.md
    ├── README_08_TESTING_SECURITY.md
    └── README_09_DEPLOYMENT_DEMO.md
```

You may adjust internal filenames when needed, but preserve the logical boundaries and document any changes.

## 6. Implementation order

Implement and verify in this sequence:

1. Foundation and runnable skeleton
2. Graph schema and FalkorDB connection
3. Ingestion pipeline and synthetic dataset
4. Retrieval and Company Brain agent
5. Evidence, freshness, conflicts, and impact analysis
6. Frontend
7. API integration and end-to-end workflow
8. Testing and security hardening
9. Deployment, documentation, and demo

Do not generate the whole project in one uncontrolled pass. Complete each module, run its tests, report what works and what remains, then continue.

## 7. Core user experience

The application should include:
- Company Brain chat
- Source citations with excerpts
- Expandable “why this answer?” evidence panel
- Interactive graph explorer
- Person/team/project/service detail views
- Ownership and expertise results
- Decision history and conflicting-source display
- Dependency impact view
- Ingestion status and source list
- Clear empty, loading, error, and no-evidence states

Do not show fake “live” data, fake citations, or controls that do nothing.

## 8. Minimum data model

Use stable IDs and explicit labels. The shared schema must be documented in `docs/GRAPH_SCHEMA.md`.

Node labels:
- `Person`
- `Team`
- `Project`
- `Service`
- `Document`
- `Chunk`
- `Ticket`
- `ChatMessage`
- `Decision`
- `Incident`
- `Skill`

Relationship types may include:
- `MEMBER_OF`
- `OWNS`
- `WORKED_ON`
- `KNOWS_ABOUT` (only when supported; distinguish inferred from explicit)
- `DEPENDS_ON`
- `SUPPORTED_BY`
- `DECIDED_IN`
- `RESOLVED`
- `MENTIONED_IN`
- `PART_OF`
- `NEXT_CHUNK`
- `SUPERSEDES`
- `RELATED_TO`

Store source and temporal metadata where applicable:
- `id`
- `source_id`
- `source_type`
- `source_uri` or local source reference
- `created_at`
- `updated_at`
- `valid_from`
- `valid_to` or an explicit current/superseded status
- `extraction_method`
- `confidence` only when meaningfully defined
- `evidence_chunk_id`

Do not blindly add all properties to all node types. Define required/optional properties by label.

## 9. API contract baseline

Implement and document at least:
- `GET /api/health`
- `POST /api/sources/upload`
- `GET /api/sources`
- `GET /api/sources/{source_id}`
- `POST /api/chat`
- `GET /api/graph/search?q=...`
- `GET /api/graph/entity/{entity_id}`
- `GET /api/projects/{project_id}/impact`
- `GET /api/decisions/{decision_id}/history`
- `POST /api/sync` (can be a controlled MVP endpoint for reprocessing changed sample sources)

Use Pydantic request/response models. Return consistent error formats. Do not expose raw Cypher execution as a public endpoint.

## 10. Definition of done

The MVP is complete only when:
- A fresh clone can be configured from documented instructions.
- Docker Compose starts the required services.
- A synthetic company dataset can be ingested.
- FalkorDB contains meaningful entities, relationships, chunks, and provenance.
- At least five different question types return evidence-backed answers.
- A user can open a citation and inspect the source excerpt.
- At least one multi-hop query genuinely depends on graph relationships.
- Ownership/decision/dependency features work on the sample data.
- Stale/conflicting source cases are demonstrated and labelled honestly.
- The frontend is connected to the real backend and database.
- Automated tests cover core graph/retrieval/API behavior.
- No secrets are committed.
- README, graph schema, key Cypher queries, setup instructions, and demo script are complete.

## 11. Antigravity working protocol

Before each module:
1. Read this master file and the module README.
2. Inspect existing code before creating or overwriting files.
3. Reuse shared types, models, services, and schema.
4. Implement the smallest complete working slice.
5. Run tests and fix failures.
6. Update module status and docs.
7. Report files changed, commands run, test results, known limitations, and the next dependency.

Never claim tests passed unless they were actually run. Never leave a fake implementation presented as complete. If blocked by missing credentials, implement a clear configuration error and provide a mock-free test using an explicitly labelled deterministic test adapter.

Start by inspecting the repository and implementing **Module 01: Foundation**.
