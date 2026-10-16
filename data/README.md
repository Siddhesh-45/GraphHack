# Northstar Systems — Synthetic Corporate Knowledge Corpus

## Overview
This directory contains the authorized synthetic dataset for **Northstar Systems**, a fictional enterprise FinTech platform. In compliance with **FalkorDB Graph Hacks Rule 6**, this dataset contains zero private, personal, paywalled, or restricted information. It is explicitly designed to test graph traversals, decision lineage, contradictory knowledge, stale data, and multi-hop blast radius impact analysis.

---

## 1. Synthetic Enterprise Entity Roster

### A. Employees (`Person` Nodes)
1. **Sarah Chen** (`sarah-chen`): Staff Backend Engineer, Tech Lead for Core Payments (`MEMBER_OF` Core Payments, `OWNS` Payment Gateway).
2. **Alex Rivera** (`alex-rivera`): Principal Infrastructure Architect (`MEMBER_OF` Platform Engineering, `OWNS` Auth Service & API Gateway, resolver of Incident INC-101).
3. **Marcus Vance** (`marcus-vance`): Senior Distributed Systems Engineer (`MEMBER_OF` Core Payments, `OWNS` Billing Engine).
4. **Priya Patel** (`priya-patel`): Lead Security Compliance Engineer (`MEMBER_OF` Security & Compliance).
5. **David Kim** (`david-kim`): Senior Backend Engineer (`MEMBER_OF` Platform Engineering, historical contributor to Notification Service).
6. **Elena Rostova** (`elena-rostova`): Engineering Director (`MEMBER_OF` Core Payments, signatory on Architecture Decision Records).

### B. Teams (`Team` Nodes)
1. **Core Payments** (`core-payments`): FinTech transactions, ledger integrity, billing infrastructure. Lead: Elena Rostova.
2. **Platform Engineering** (`platform-engineering`): Microservice gateways, authentication clusters, Kubernetes infrastructure. Lead: Alex Rivera.
3. **Security & Compliance** (`security-compliance`): PCI-DSS adherence, token rotation, audit readiness. Lead: Priya Patel.

### C. Services & Dependencies (`Service` Nodes & `DEPENDS_ON` Edges)
- **API Gateway** (`api-gateway`, Tier 1): Public ingress gateway.
  - `DEPENDS_ON` ➔ **Auth Service** (synchronous gRPC)
  - `DEPENDS_ON` ➔ **Payment Gateway** (synchronous REST)
- **Auth Service** (`auth-service`, Tier 1): JWT issuance, SSO token verification.
- **Payment Gateway** (`payment-gateway`, Tier 1): Processes payments, writes ledger entries.
  - `DEPENDS_ON` ➔ **Auth Service** (token validation)
  - `DEPENDS_ON` ➔ **Billing Engine** (asynchronous Kafka events)
- **Billing Engine** (`billing-engine`, Tier 2): Invoicing, recurring billing, merchant settlements.
  - `DEPENDS_ON` ➔ **Notification Service** (asynchronous webhook)
- **Notification Service** (`notification-service`, Tier 3): Customer emails and push notifications.

---

## 2. Architecture Decision Records (`Decision` Nodes & `SUPERSEDES` Edges)

1. **ADR-001 (Jan 15, 2025)**: *Selection of PostgreSQL for Payment Ledger*.
   - **Status**: `SUPERSEDED`
   - **Rationale**: ACID compliance, rich SQL relational semantics, proven reliability.
   - **Author**: Sarah Chen
2. **ADR-002 (Mar 10, 2025)**: *Adoption of gRPC for Inter-Service Auth Checks*.
   - **Status**: `ACTIVE`
   - **Rationale**: Sub-millisecond latency, strict protobuf contracts.
   - **Author**: Alex Rivera
3. **ADR-003 (Nov 05, 2025)**: *Kafka Event Bus for Asynchronous Billing Ingestion*.
   - **Status**: `ACTIVE`
   - **Rationale**: Decoupling payment authorization from invoice batching.
   - **Author**: Marcus Vance
4. **ADR-004 (Aug 20, 2026)**: *Migration from PostgreSQL to CockroachDB for Ledger Active-Active Replication*.
   - **Status**: `ACTIVE`
   - **Relationship**: `(adr-004)-[:SUPERSEDES {reason: "International multi-region latency and zero downtime failover"}]->(adr-001)`
   - **Author**: Sarah Chen & Elena Rostova
5. **ADR-005 (Oct 02, 2026)**: *FalkorDB as the Primary Knowledge Graph Context Store*.
   - **Status**: `ACTIVE`
   - **Rationale**: Sub-millisecond Cypher traversals on every agent reasoning loop, native multigraph support.
   - **Author**: Alex Rivera

---

## 3. Production Incidents (`Incident` Nodes)

1. **INC-101 (May 14, 2026)**: *SEV-1 Payment Gateway Timeouts*.
   - **Root Cause**: Database connection pool exhaustion under sudden traffic spike.
   - **Mitigation**: Connection pool resizing and circuit breaker tuning.
   - **Resolver**: Sarah Chen (`RESOLVED` INC-101)
2. **INC-102 (Sep 02, 2026)**: *SEV-2 Auth Service Token Invalidation Failures*.
   - **Root Cause**: Asymmetric JWT key rotation mismatch during blue-green deployment.
   - **Mitigation**: Key caching grace period implemented.
   - **Resolver**: Alex Rivera (`RESOLVED` INC-102)

---

## 4. Controlled Anomaly Scenarios for Benchmark Testing

1. **Contradictory Knowledge Scenario**:
   - `Doc A (Legacy Charter)`: States David Kim is the primary owner of Notification Service.
   - `Doc B (Recent Runbook)`: States Priya Patel took over Notification Service as interim owner.
   - **System Behavior**: Flags ownership conflict visibly, cites both documents, and prompts for human confirmation.
2. **Stale Knowledge Scenario**:
   - `Legacy_Billing_Runbook.md`: Last modified in January 2024 (> 2 years old, unverified).
   - **System Behavior**: Flags document as `STALE_UNVERIFIED` and warns the user before applying commands.
3. **Missing Evidence Scenario**:
   - Question: *"What is Northstar's 2027 office expansion budget?"*
   - **System Behavior**: Honestly abstains with `confidence_label: "insufficient_evidence"` rather than hallucinating.
