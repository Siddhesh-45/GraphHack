# ADR 004: Migration from PostgreSQL to CockroachDB for Ledger Active-Active Replication

- **Status**: ACTIVE
- **Supersedes**: ADR 001 (Selection of PostgreSQL for Payment Ledger)
- **Date**: 2026-08-20
- **Author**: Sarah Chen (Staff Backend Engineer)
- **Deciders**: Sarah Chen, Elena Rostova, Marcus Vance
- **Consulted**: Alex Rivera, Priya Patel

## Context
With Northstar Systems expanding into European and Asia-Pacific markets, cross-region payment authorization latency exceeded 350ms using our single-region PostgreSQL cluster in us-east-1. Furthermore, disaster recovery requirements mandate zero-downtime failover with RPO = 0.

## Decision
We will migrate the Payment Gateway ledger from single-region PostgreSQL to **CockroachDB v24.2** deployed across three multi-region cloud regions (us-east, eu-west, ap-southeast).

## Rationale
1. **Multi-Region Active-Active**: CockroachDB implements Raft consensus per range, allowing local sub-10ms writes for domestic transactions while providing serializable distributed transactions globally.
2. **PostgreSQL Compatibility**: Preserves our existing SQL schema, indexes, and ORM models with minimal application refactoring.
3. **Resilience**: Node loss or region loss is handled autonomously with zero manual operator intervention.

## Consequences
- Requires operational monitoring of Raft range leases and inter-region network round-trip times.
- Supersedes ADR 001 as the official architectural standard for payment ledger storage.
