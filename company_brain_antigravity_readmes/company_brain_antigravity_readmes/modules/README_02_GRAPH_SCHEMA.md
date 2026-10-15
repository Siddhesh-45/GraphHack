# Module 02 — FalkorDB Connection, Graph Schema, and Query Service

## Goal
Build the canonical company graph model and reusable graph access layer. FalkorDB must be central to core product behavior.

## Requirements
1. Implement a reusable FalkorDB connection/service with connection lifecycle handling.
2. Verify the exact client API against the installed version. Do not copy incompatible examples from older SDK releases.
3. Define stable node labels:
   `Person`, `Team`, `Project`, `Service`, `Document`, `Chunk`, `Ticket`, `ChatMessage`, `Decision`, `Incident`, `Skill`.
4. Define relationship types:
   `MEMBER_OF`, `OWNS`, `WORKED_ON`, `KNOWS_ABOUT`, `DEPENDS_ON`, `SUPPORTED_BY`, `DECIDED_IN`, `RESOLVED`, `MENTIONED_IN`, `PART_OF`, `NEXT_CHUNK`, `SUPERSEDES`, `RELATED_TO`.
5. Define typed Pydantic models for graph entities, relationships, source metadata, and graph search results.
6. Use stable IDs and safe Cypher parameterization. Never concatenate untrusted user strings into executable Cypher.
7. Use `MERGE` or equivalent idempotent upsert patterns where appropriate to avoid duplicate records on re-ingestion.
8. Create schema documentation with node properties, relationship direction, cardinality assumptions, and provenance rules.
9. Add graph query functions for:
   - entity lookup by ID/name
   - person/team/project/service ownership
   - project contributors
   - dependencies of a service/project
   - decisions linked to a project/service
   - incidents and their resolutions
   - source chunks linked to entities/decisions
   - superseded/current decisions
10. Keep all application queries in a dedicated graph/query service, not inside route handlers.

## Temporal and provenance rules
- Explicit facts must retain source IDs and supporting chunk IDs.
- Inferred knowledge must be marked as inferred and retain evidence.
- Ownership can change over time; do not overwrite history without recording the change.
- Decision history must support old and superseding decisions.
- Avoid a universal `RELATES_TO` relationship when a meaningful typed edge exists.

## Safety
- Do not expose arbitrary Cypher execution via public API.
- Restrict graph labels and relationship types to a controlled allowlist.
- Validate IDs and inputs.

## Acceptance criteria
- Integration test creates nodes and edges in FalkorDB and reads them back.
- Re-running seed/upsert does not duplicate entities.
- Ownership, decision, and dependency queries return expected results on fixtures.
- `docs/GRAPH_SCHEMA.md` includes example Cypher queries and a diagram.
