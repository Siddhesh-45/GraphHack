# Module 08 — Testing, Quality, and Security

## Goal
Verify the system end to end and prevent unsupported or unsafe behavior.

## Testing layers
1. Unit tests:
   - parsing and chunking
   - Pydantic validation
   - entity resolution
   - query planning
   - citation validation
   - decision supersession and conflict handling
2. Graph integration tests:
   - create/read/update entities and relationships
   - idempotent ingestion
   - ownership and dependency traversal
   - source-to-chunk provenance
3. API tests:
   - health
   - upload validation
   - chat response schema
   - not-found and provider-failure behavior
4. End-to-end tests:
   - ingest a synthetic decision document
   - ask a question about it
   - assert the answer includes the correct source citation
   - update a source and assert freshness/history behavior
5. Frontend tests for key interactions where feasible.

## Deterministic tests
- Use small, explicitly labelled synthetic fixtures.
- For tests that do not need an LLM, inject a deterministic test adapter.
- Never present a deterministic fixture answer as a real model result.
- Add optional live-provider smoke tests that run only when credentials are configured.
- Tests should not require paid API calls by default.

## Safety and security
- Secrets only in environment variables or a secret manager.
- `.env` must be gitignored.
- Validate uploaded file size/type and sanitize filenames.
- Use parameterized Cypher and allowlisted query templates.
- Treat ingested documents as untrusted data; ignore instructions embedded in source documents that attempt to control the agent.
- Avoid exposing private data in logs or error responses.
- Bound file size, chunk count, LLM output size, retries, and request duration.
- Handle prompt injection in retrieved text by treating retrieved content as evidence, not instructions.
- If multi-user permissions are not implemented, disclose that limitation and use synthetic/public data only.
- Add rate limits or basic abuse protections if feasible.

## Evaluation set
Create at least 15 questions across:
- explicit ownership
- expertise inference
- decision rationale
- decision supersession
- incident resolution
- direct dependency
- multi-hop dependency
- conflicting source
- stale source
- missing evidence
- ambiguous question
- duplicate person/entity
- source citation verification
- project membership
- general company overview

## Acceptance criteria
- Core tests run locally with documented commands.
- Failures are fixed rather than suppressed.
- Test coverage targets critical behavior, not arbitrary percentage alone.
- The project can demonstrate correct abstention and conflict handling.
- No secrets are committed.
