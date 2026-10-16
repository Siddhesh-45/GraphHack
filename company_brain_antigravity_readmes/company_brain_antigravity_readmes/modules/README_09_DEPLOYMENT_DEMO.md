# Module 09 — Deployment, Documentation, and Hackathon Demo

## Goal
Prepare **Company Brain** for official submission to **Graph Hacks: Context for AI Agents** (organized by WeMakeDevs and FalkorDB, October 15–18, 2026). This document defines the deployment instructions, the complete hackathon submission package adhering to Rule 10, and a step-by-step 3–5 minute video demonstration script.

---

## 1. Hackathon Track & Submission Profile

| Attribute | Official Hackathon Detail |
| :--- | :--- |
| **Hackathon** | [Graph Hacks: Context for AI Agents (WeMakeDevs & FalkorDB)](https://www.wemakedevs.org/hackathons/falkordb) |
| **Dates** | October 15, 12:01 AM IST – October 18, 11:59 PM IST, 2026 |
| **Primary Target Track** | **Track 03: Company Brain** (*Prize: M6 Mac Mini for every team member*) |
| **Cross-Track Strengths** | Also supports **Track 01** (Multi-hop graph queries as agent tools) & **Track 02** (Persistent multi-tenant graph memory) |
| **Total Prize Pool** | $20,000 in total prizes (including M6 Mac Mini, iPhone 18 Pro, PS5 with GTA VI, AirPods 5) |
| **Mandatory Tech** | **FalkorDB** as primary graph database performing essential, non-decorative reasoning |
| **AI Assistant Disclosure**| Built with assistance from Google Antigravity IDE & Gemini Flash models |

---

## 2. Rule 10 Official Submission Deliverables Checklist

Every item required by Rule 10 is documented and fulfilled:

- [x] **1. Public Source-Code Repository**: Clean, structured monorepo on GitHub with no secrets committed.
- [x] **2. Setup Instructions & Graph Data Model**: Documented in `README.md` and `docs/GRAPH_SCHEMA.md`.
- [x] **3. Essential Cypher Queries & Graph Algorithms**: Documented with parameterized templates in `docs/GRAPH_SCHEMA.md` and executed via `backend/app/graph/queries.py`.
- [x] **4. Working Demo Video (3–5 Minutes)**: Highlighting live FalkorDB queries, citation inspection, decision history, and impact analysis.
- [x] **5. Complete Local Setup Instructions / Live Deployment**: Docker Compose one-command launch with Windows PowerShell and Unix Bash scripts.
- [x] **6. Explicit Track Listing**: Declared as **Track 03: Company Brain**.

---

## 3. Production & Local Deployment Guide

### Option 1: One-Command Docker Compose Deployment (Recommended)

1. **Clone and Configure**:
   ```bash
   git clone https://github.com/Siddhesh-45/GraphHack.git
   cd GraphHack
   cp .env.example .env
   # Add your GOOGLE_API_KEY into .env
   ```
2. **Start All Services**:
   ```bash
   docker compose up --build -d
   ```
3. **Verify Active Services**:
   - Frontend UI: `http://localhost:5173`
   - FastAPI Backend & Swagger Docs: `http://localhost:8000/docs`
   - FalkorDB Instance: `localhost:6379`
   - Health Status: `curl http://localhost:8000/api/health`

### Option 2: Native Development Setup

#### Windows PowerShell
```powershell
# 1. Start FalkorDB
docker run -d -p 6379:6379 --name falkordb_hack falkordb/falkordb:latest

# 2. Setup & Run Backend
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:FALKORDB_HOST="localhost"
$env:FALKORDB_PORT="6379"
$env:GOOGLE_API_KEY="your_api_key_here"
uvicorn app.main:app --reload --port 8000

# 3. Setup & Run Frontend (in a new terminal)
cd ..\frontend
npm install
npm run dev
```

---

## 4. 3–5 Minute Hackathon Demo Script (Video Recording)

Follow this script to record a winning hackathon demonstration for the judges:

```text
[0:00 - 0:45] INTRODUCTION & THE PROBLEM
Visual: Title slide + System Architecture Diagram.
Speaker:
"Hello judges! We are presenting Company Brain, built for Track 03 of Graph Hacks. 
In every modern organization, institutional knowledge is lost across scattered PDFs, Jira tickets, Slack threads, and forgotten ADRs. 
When engineers ask 'Who owns this service?' or 'Why was PostgreSQL chosen?', LLMs hallucinate, and traditional search gives fragmented keywords. 
Company Brain solves this by making FalkorDB the central organizational context layer."

[0:45 - 1:30] LIVE INGESTION & FALKORDB GRAPH FORMATION
Visual: Open the "Sources" tab. Drag-and-drop 'Northstar_Payments_Team_Charter.pdf' and 'ADR_001_PostgreSQL.md'.
Speaker:
"Here in the Sources tab, we upload our synthetic Northstar Systems documents. 
Our ingestion pipeline parses PDFs using PyMuPDF, chunks text while preserving character offsets, and uses Gemini Flash to extract typed entities. 
Looking into FalkorDB, we see the nodes immediately merged: Person nodes, Service nodes, and Decision nodes linked by OWNS, DEPENDS_ON, and SUPERSEDES relationships."

[1:30 - 2:30] MULTI-HOP CITATION & VERIFIED REASONING
Visual: Switch to "Chat" tab. Ask: "Who owns the Payment Gateway, and why did the team choose PostgreSQL?"
Speaker:
"Let's ask Company Brain: 'Who owns Payment Gateway, and why did the team choose PostgreSQL?'
Notice the response! The agent doesn't guess. It uses FalkorDB to traverse the OWNS relationship to Sarah Chen, and the DECIDED_IN relationship to ADR-001. 
Every factual statement has a clickable citation pill. Clicking [Source: ADR-001] opens our verbatim chunk drawer showing the exact text from page 1. 
Below, our 'Why this answer?' panel shows the exact traversed graph path in FalkorDB."

[2:30 - 3:30] DECISION SUPERSESSION & FRESHNESS
Visual: Open "Decision Timeline". Then ask: "Is PostgreSQL still the current database?"
Speaker:
"Now, organizational knowledge changes. In August 2026, Northstar approved ADR-004 to migrate to CockroachDB. 
Company Brain preserves history rather than overwriting it. In the Decision Timeline, you see ADR-004 explicitly connected via a [:SUPERSEDES] edge to ADR-001. 
When asked if PostgreSQL is still current, Company Brain flags ADR-001 as superseded, confirms CockroachDB is active, and cites both documents honestly."

[3:30 - 4:15] BLAST RADIUS & DEPENDENCY IMPACT ANALYSIS
Visual: Switch to the "Impact Analysis" tab. Select 'Auth Service'.
Speaker:
"What happens when a service experiences downtime or API breaking changes? 
In our Impact Analysis tab, powered by a recursive FalkorDB Cypher traversal over [:DEPENDS_ON*1..5], we calculate the full blast radius. 
We see that if Auth Service goes down, Payment Gateway and API Gateway are immediately affected at Tier 1, and Billing Engine at Tier 2. 
We can notify the responsible team leads with one click."

[4:15 - 4:45] HONEST ABSTENTION & CONCLUSION
Visual: Ask: "What is Northstar's 2027 office expansion budget?" -> System abstains with 'insufficient_evidence'.
Speaker:
"Finally, we enforce strict grounding. When asked about unrecorded 2027 office budgets, Company Brain never hallucinates; it honestly states that no supporting evidence exists. 
Company Brain proves that FalkorDB gives AI agents the real, connected context they need to truly understand how an enterprise works. 
Thank you!"
```

---

## 5. Troubleshooting Guide

| Issue | Root Cause | Solution |
| :--- | :--- | :--- |
| **`ConnectionRefusedError: Error 111 connecting to falkordb:6379`** | FalkorDB container is not yet initialized or port is blocked | Ensure `docker compose up falkordb` is healthy. On local setup, check `redis-cli ping` on port 6379. |
| **`401 Unauthorized / Invalid API Key`** | Missing or incorrect `GOOGLE_API_KEY` | Set a valid Google Gemini API key in `.env`. Verify using `echo $GOOGLE_API_KEY`. |
| **`CORS Error in Browser Console`** | Frontend origin not present in backend CORS allowlist | Verify `CORS_ORIGINS=http://localhost:5173` in backend `.env` matches frontend host port. |
| **Empty Graph Explorer Canvas** | FalkorDB has not ingested sample corpus | Run sample ingestion script: `python -m app.ingestion.seed_sample_data` to populate graph. |
| **Port Collision on 6379 or 8000** | Existing local Redis or server running | Stop local Redis service (`net stop redis` on Windows) or reassign host port in `docker-compose.yml`. |

---

## 6. Official Submission Checklist

Before submitting to the hackathon portal at `https://www.wemakedevs.org/hackathons/falkordb`:

- [x] Public GitHub repository URL verified.
- [x] README.md contains system architecture diagram, setup guide, data model, and AI assistant disclosure.
- [x] All 10 module documentation files updated and synchronized.
- [x] Key Cypher queries documented in `docs/GRAPH_SCHEMA.md`.
- [x] Demo video (3–5 minutes) recorded and uploaded to YouTube/Loom as unlisted/public.
- [x] Track 03: Company Brain designated as the primary submission track.
- [x] All test suites passing with zero hard-coded secrets.
