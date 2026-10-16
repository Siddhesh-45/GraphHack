# Technology Decisions & ADR Log — Company Brain

## ADR-01: Selection of FalkorDB as Primary Graph Database
- **Status**: Accepted
- **Rationale**: Meets FalkorDB Graph Hacks mandatory requirement. Delivers ultra-low latency Cypher traversals on every agent reasoning step, with built-in multigraph and vector capabilities.

## ADR-02: React 18 + Vite + @xyflow/react for Frontend Graph Explorer
- **Status**: Accepted
- **Rationale**: Instant HMR, type-safe React Flow custom node cards, minimap, controls, and glassmorphic UI.

## ADR-03: FastAPI + Python 3.12 for Async Backend
- **Status**: Accepted
- **Rationale**: High-throughput async endpoints, native Pydantic v2 validation, and OpenAPI documentation.

## ADR-04: 6-Factor Composite Freshness & Memory Decay System
- **Status**: Accepted
- **Rationale**: Replaces naive TTL with multi-dimensional scoring (age, recency, source authority, connectivity, supersession, and contradictions).
