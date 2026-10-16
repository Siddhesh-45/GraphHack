# ADR 001: Selection of PostgreSQL for Payment Ledger

- **Status**: SUPERSEDED (Superseded by ADR 004 on 2026-08-20)
- **Date**: 2025-01-15
- **Author**: Sarah Chen (Staff Backend Engineer)
- **Deciders**: Sarah Chen, Elena Rostova (Director of Engineering)
- **Consulted**: Alex Rivera (Principal Infrastructure Architect)

## Context
Northstar Systems is building its new high-throughput Payment Gateway to process merchant card payments and internal ledger transfers. The ledger database requires strict ACID compliance, serializable transaction isolation, and robust disaster recovery capabilities.

## Decision
We will use **PostgreSQL** (version 16) as the primary relational database for the Payment Gateway ledger.

## Rationale
1. **ACID Guarantees**: PostgreSQL provides proven write-ahead logging (WAL) and MVCC guarantees essential for monetary transactions.
2. **Team Familiarity**: The Core Payments team has deep operational familiarity with PostgreSQL query optimization.
3. **Ecosystem**: Rich tooling for logical replication and point-in-time recovery (PITR).

## Consequences
- Single-region primary with read replicas limits multi-region active-active scalability.
- If international expansion requires multi-region writes, a distributed SQL migration will be necessary.
