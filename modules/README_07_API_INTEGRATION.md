# Module 07 — REST API Contract and End-to-End Integration

## Goal
Establish a unified, strongly-typed REST API contract that bridges the React frontend, FastAPI backend services, FalkorDB graph layer, and Gemini LLM. All 10 core endpoints must be strictly validated via Pydantic and documented in OpenAPI standards.

---

## 1. Complete REST API Specifications

### 1. `GET /api/health`
Checks runtime health and database connectivity.
- **Response `200 OK`**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-10-16T01:30:00Z",
  "environment": "development",
  "falkordb": {
    "connected": true,
    "host": "localhost",
    "port": 6379,
    "graph_name": "company_brain",
    "total_nodes": 42
  }
}
```

---

### 2. `POST /api/sources/upload`
Uploads and initiates parsing of a source document (`.pdf`, `.docx`, `.md`, `.txt`, `.json`).
- **Content-Type**: `multipart/form-data`
- **Request Body**: `file: UploadFile`
- **Response `201 Created`**:
```json
{
  "source_id": "doc-northstar-payment-adr-001",
  "title": "ADR 001 — PostgreSQL Selection for Ledger",
  "file_type": "markdown",
  "checksum": "a8f5f167f44f4964e6c998dee827110c",
  "status": "COMPLETED",
  "chunks_created": 6,
  "entities_extracted": 12
}
```

---

### 3. `GET /api/sources`
Retrieves all registered and ingested knowledge sources.
- **Response `200 OK`**:
```json
[
  {
    "source_id": "doc-northstar-payment-adr-001",
    "title": "ADR 001 — PostgreSQL Selection for Ledger",
    "source_type": "markdown",
    "status": "COMPLETED",
    "chunk_count": 6,
    "created_at": "2026-09-15T10:30:00Z"
  }
]
```

---

### 4. `GET /api/sources/{source_id}`
Returns granular metadata, chunks, and extracted entities for a single document.
- **Response `200 OK`**:
```json
{
  "source_id": "doc-northstar-payment-adr-001",
  "title": "ADR 001 — PostgreSQL Selection for Ledger",
  "chunks": [
    {
      "chunk_id": "chk-001",
      "index": 0,
      "page_number": 1,
      "text": "Status: Superseded by ADR 004...",
      "char_offset_start": 0,
      "char_offset_end": 450
    }
  ],
  "linked_entities": [
    {"id": "adr-001", "label": "Decision"},
    {"id": "payment-gateway", "label": "Service"}
  ]
}
```

---

### 5. `POST /api/chat`
Conversational intelligence endpoint for multi-hop questions with citations and graph evidence.
- **Request Body**:
```json
{
  "question": "Who owns Payment Gateway and why was PostgreSQL selected?",
  "conversation_id": "conv-10293",
  "max_hops": 3
}
```
- **Response `200 OK`**:
```json
{
  "answer": "Payment Gateway is owned by Sarah Chen [Source: doc-team-charter, Chunk: chk-012]. PostgreSQL was initially chosen under ADR-001 for ACID compliance [Source: doc-adr-001, Chunk: chk-045], but was later superseded by ADR-004 to CockroachDB [Source: doc-adr-004, Chunk: chk-089].",
  "citations": [
    {
      "source_id": "doc-team-charter",
      "source_title": "Payments Team Charter",
      "chunk_id": "chk-012",
      "excerpt": "Sarah Chen is the designated Tech Lead and Owner of Payment Gateway.",
      "page_number": 2,
      "timestamp": "2026-01-10T09:00:00Z"
    }
  ],
  "graph_paths": [
    {
      "start_node": "sarah-chen",
      "end_node": "payment-gateway",
      "relationships": ["OWNS"],
      "nodes": [{"id": "sarah-chen", "label": "Person"}, {"id": "payment-gateway", "label": "Service"}],
      "description": "Sarah Chen OWNS Payment Gateway"
    }
  ],
  "confidence_label": "high",
  "warnings": ["ADR-001 has been superseded by ADR-004."],
  "follow_up_questions": ["Would you like to view the CockroachDB migration timeline?"]
}
```

---

### 6. `GET /api/graph/search?q={query}&types={types}`
Full-text or entity search across the FalkorDB knowledge graph.
- **Response `200 OK`**:
```json
{
  "query": "payment",
  "total_results": 2,
  "nodes": [
    {"id": "payment-gateway", "label": "Service", "name": "Payment Gateway", "tier": "Tier 1"},
    {"id": "core-payments", "label": "Team", "name": "Core Payments", "department": "FinTech"}
  ],
  "edges": [
    {"source": "core-payments", "target": "payment-gateway", "relation": "SUPPORTED_BY"}
  ]
}
```

---

### 7. `GET /api/graph/entity/{entity_id}`
Returns immediate 1-hop and 2-hop graph neighborhood for an entity.
- **Response `200 OK`**:
```json
{
  "entity": {"id": "payment-gateway", "label": "Service", "name": "Payment Gateway"},
  "neighbors": [
    {"id": "sarah-chen", "label": "Person", "relation": "OWNS", "direction": "inbound"},
    {"id": "auth-service", "label": "Service", "relation": "DEPENDS_ON", "direction": "outbound"}
  ]
}
```

---

### 8. `GET /api/projects/{project_id}/impact?depth={depth}`
Calculates upstream and downstream dependency blast radius.
- **Response `200 OK`**:
```json
{
  "target_service": "auth-service",
  "blast_radius_score": "CRITICAL",
  "affected_nodes": [
    {"service_id": "payment-gateway", "tier": "Tier 1", "hop_distance": 1},
    {"service_id": "billing-engine", "tier": "Tier 2", "hop_distance": 2}
  ]
}
```

---

### 9. `GET /api/decisions/{decision_id}/history`
Returns chronological supersession lineage and status history for an ADR.
- **Response `200 OK`**:
```json
{
  "decision_id": "adr-004",
  "title": "ADR 004 — Migration to CockroachDB",
  "status": "ACTIVE",
  "supersedes": [
    {"id": "adr-001", "title": "ADR 001 — PostgreSQL Selection", "status": "SUPERSEDED"}
  ]
}
```

---

### 10. `POST /api/sync`
Performs delta synchronization on the dataset, updating modified documents without graph duplication.
- **Response `200 OK`**:
```json
{
  "synced_files": 12,
  "updated_files": 1,
  "new_nodes_created": 3,
  "stale_nodes_flagged": 1,
  "status": "SYNCHRONIZATION_COMPLETE"
}
```

---

## 2. Standardized Error Response Model

All API endpoints return consistent, structured JSON errors:

```json
{
  "error_code": "ENTITY_NOT_FOUND",
  "message": "Service with id 'unknown-service' does not exist in FalkorDB.",
  "timestamp": "2026-10-16T01:30:15Z",
  "request_id": "req-98210-af"
}
```

---

## 3. Security, Middleware, and CORS

1. **CORS Middleware**: Bound to configurable origins via `CORS_ORIGINS` in `.env`.
2. **Request ID Middleware**: Injects `X-Request-ID` header into every request and response for end-to-end tracing.
3. **Payload Sanitization**: Rejects uploaded files exceeding 25MB or containing unauthorized file extensions.
4. **Parameterized Queries**: No raw string interpolation into Cypher queries.

---

## 4. Acceptance Criteria
- [x] All 10 endpoints return valid JSON adhering strictly to documented Pydantic schemas.
- [x] Interactive OpenAPI Swagger docs available at `http://localhost:8000/docs`.
- [x] Frontend API client successfully communicates with all endpoints without CORS issues.
- [x] Parameter validation errors return HTTP 422 with actionable error messages.
