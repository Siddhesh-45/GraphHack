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

## ADR-05: Pydantic BaseSettings with Dual Path Resolution & Graceful Startup Telemetry
- **Status**: Accepted
- **Rationale**: Provides deterministic environment configuration loading whether services are executed from root, backend, or Docker containers. Employs strict Pydantic v2 validation with formatted startup error banners, guarding against invalid ports, invalid environment modes, and illegal chunk configurations.

## ADR-06: FalkorDB Canonical Graph Schema & Parameterized Cypher Service
- **Status**: Accepted
- **Rationale**: Implements 11 canonical node types and 13 typed relationships in FalkorDB with universal entity metadata (`freshness_score`, `staleness_status`, `connections_count`). Enforces idempotent upserts using Cypher `MERGE`, strict parameterization via `$params` to eliminate injection vulnerabilities, native unique constraint initialization via `create_node_unique_constraint`, and bounded multi-hop traversals for blast radius and decision supersession lineage.


