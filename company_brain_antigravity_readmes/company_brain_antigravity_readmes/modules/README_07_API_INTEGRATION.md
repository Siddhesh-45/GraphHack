# Module 07 — API Contract and End-to-End Integration

## Goal
Connect frontend, backend, ingestion, graph, retrieval, and evidence modules into one coherent workflow.

## Required endpoints
- `GET /api/health`
- `POST /api/sources/upload`
- `GET /api/sources`
- `GET /api/sources/{source_id}`
- `POST /api/chat`
- `GET /api/graph/search?q=...`
- `GET /api/graph/entity/{entity_id}`
- `GET /api/projects/{project_id}/impact`
- `GET /api/decisions/{decision_id}/history`
- `POST /api/sync`

Document exact request/response schemas in `docs/API_CONTRACT.md`. Use Pydantic models for backend validation and TypeScript types for frontend responses.

## Chat request
At minimum:
- `question: string`
- optional `conversation_id`
- optional bounded conversation context if implemented

## Chat response
At minimum:
- `answer`
- `citations[]`
- `graph_paths[]`
- `confidence_label`
- `warnings[]`
- `follow_up_questions[]`

Citations must refer to actual source records/chunks. Include stable source IDs and the excerpt required to substantiate the answer.

## Integration tasks
1. Connect upload UI to ingestion endpoint.
2. Poll or refresh source status after upload.
3. Connect chat UI to the real retrieval endpoint.
4. Connect graph explorer to graph search/entity endpoints.
5. Connect impact view to graph-based impact endpoint.
6. Connect decision timeline to history endpoint.
7. Configure CORS using an explicit environment variable.
8. Add request IDs and useful structured logs without logging API keys or sensitive document text.
9. Use consistent error responses, status codes, and timeout handling.
10. Add an end-to-end test from seeded/ingested source through question to citation.

## Security requirements
- Validate uploaded file type and size.
- Sanitize filenames and store uploads safely.
- Do not expose arbitrary graph query execution.
- Do not trust frontend-supplied source IDs without backend validation.
- Avoid logging secrets, authorization headers, or complete sensitive prompts.
- If authentication is out of MVP scope, state that clearly in documentation and keep the demo data synthetic.

## Acceptance criteria
- A user uploads a sample document and sees ingestion status.
- The ingested document can be queried through chat.
- Answer citations resolve to source details.
- Graph Explorer displays related nodes from FalkorDB.
- Impact and decision history endpoints return real graph-derived data.
- API schemas are documented and exercised by tests.
