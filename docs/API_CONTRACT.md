# API Contract Baseline — Company Brain

## Endpoints

1. `GET /api/health`: Health status & FalkorDB node count.
2. `POST /api/sources/upload`: Multipart document upload.
3. `GET /api/sources`: List of ingested sources.
4. `GET /api/sources/{source_id}`: Granular document and chunk metadata.
5. `POST /api/chat`: Grounded question answering with citations.
6. `GET /api/graph/search?q={query}`: Fulltext & entity graph lookup.
7. `GET /api/graph/entity/{entity_id}`: Graph neighborhood.
8. `GET /api/projects/{project_id}/impact`: Recursive dependency blast radius.
9. `GET /api/decisions/{decision_id}/history`: ADR lineage and supersession history.
10. `POST /api/sync`: Delta dataset synchronization and freshness score re-evaluation.
