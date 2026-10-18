import pytest
from datetime import datetime, timezone
from app.graph.connection import get_graph_connection
from app.graph.queries import GraphQueryService

TEST_GRAPH = "test_company_brain_m02"


@pytest.fixture(scope="module")
def graph_service():
    conn = get_graph_connection()
    service = GraphQueryService(conn)
    # Ensure test graph is clean before running tests
    try:
        conn.get_client().select_graph(TEST_GRAPH).delete()
    except Exception:
        pass

    # Initialize constraints & indexes on test graph
    conn.init_schema(graph_name=TEST_GRAPH)
    yield service

    # Cleanup after test module finishes
    try:
        conn.get_client().select_graph(TEST_GRAPH).delete()
    except Exception:
        pass


def test_schema_initialization_idempotence(graph_service):
    """Calling init_schema multiple times must succeed cleanly without throwing."""
    res1 = graph_service.connection.init_schema(graph_name=TEST_GRAPH)
    assert res1["total_canonical_labels"] == 11
    assert res1["graph"] == TEST_GRAPH

    res2 = graph_service.connection.init_schema(graph_name=TEST_GRAPH)
    assert res2["total_canonical_labels"] == 11


def test_upsert_entity_idempotency_and_constraints(graph_service):
    """Test idempotent entity node upsert and unique constraint enforcement."""
    # 1. Create a service node
    res1 = graph_service.upsert_entity(
        label="Service",
        properties={
            "id": "payment-gateway",
            "name": "Payment Gateway",
            "tier": "Tier 1",
            "repo_url": "github.com/northstar/payment-gateway"
        },
        graph_name=TEST_GRAPH
    )
    assert res1.id == "payment-gateway"
    assert res1.label == "Service"

    # 2. Re-upserting same ID must update without creating duplicates
    res2 = graph_service.upsert_entity(
        label="Service",
        properties={
            "id": "payment-gateway",
            "name": "Payment Gateway (Active)",
            "tier": "Tier 1",
            "repo_url": "github.com/northstar/payment-gateway-v2"
        },
        graph_name=TEST_GRAPH
    )
    assert res2.id == "payment-gateway"

    # Verify count is strictly 1
    query_res = graph_service.connection.query(
        "MATCH (s:Service {id: 'payment-gateway'}) RETURN count(s) AS c, s.name AS name",
        graph_name=TEST_GRAPH
    )
    assert query_res.result_set[0][0] == 1
    assert query_res.result_set[0][1] == "Payment Gateway (Active)"


def test_upsert_and_query_service_ownership(graph_service):
    """Test service ownership lookup with explicit and inferred owners."""
    # Create Person, Team, and link them
    graph_service.upsert_entity(
        label="Person",
        properties={
            "id": "sarah-chen",
            "name": "Sarah Chen",
            "email": "sarah@northstar.internal",
            "role": "Staff Backend Engineer"
        },
        graph_name=TEST_GRAPH
    )
    graph_service.upsert_entity(
        label="Person",
        properties={
            "id": "alex-rivera",
            "name": "Alex Rivera",
            "email": "alex@northstar.internal",
            "role": "Senior SRE"
        },
        graph_name=TEST_GRAPH
    )
    graph_service.upsert_entity(
        label="Team",
        properties={
            "id": "core-payments",
            "name": "Core Payments Team",
            "department": "Engineering"
        },
        graph_name=TEST_GRAPH
    )

    # Add relationships
    # Explicit Person Owner
    graph_service.upsert_relationship(
        source_label="Person",
        source_id="sarah-chen",
        target_label="Service",
        target_id="payment-gateway",
        rel_type="OWNS",
        properties={"is_primary": True},
        graph_name=TEST_GRAPH
    )
    # Owning Team
    graph_service.upsert_relationship(
        source_label="Team",
        source_id="core-payments",
        target_label="Service",
        target_id="payment-gateway",
        rel_type="OWNS",
        properties={"is_primary": True},
        graph_name=TEST_GRAPH
    )
    # Inferred Domain Expert
    graph_service.upsert_relationship(
        source_label="Person",
        source_id="alex-rivera",
        target_label="Service",
        target_id="payment-gateway",
        rel_type="KNOWS_ABOUT",
        properties={"is_inferred": True, "confidence": 0.88, "reason": "Mitigated INC-101"},
        graph_name=TEST_GRAPH
    )

    # Query ownership
    ownership = graph_service.get_service_ownership("payment-gateway", graph_name=TEST_GRAPH)
    assert ownership is not None
    assert ownership.service_name == "Payment Gateway (Active)"
    assert len(ownership.explicit_owners) == 1
    assert ownership.explicit_owners[0].name == "Sarah Chen"
    assert len(ownership.owning_teams) == 1
    assert ownership.owning_teams[0].name == "Core Payments Team"
    assert len(ownership.inferred_experts) == 1
    assert ownership.inferred_experts[0].name == "Alex Rivera"


def test_multi_hop_blast_radius(graph_service):
    """Test recursive dependency traversal and ordered depth tracking."""
    # Create chain: payment-gateway -> auth-service -> user-db
    graph_service.upsert_entity(
        label="Service",
        properties={"id": "auth-service", "name": "Auth Service", "tier": "Tier 1"},
        graph_name=TEST_GRAPH
    )
    graph_service.upsert_entity(
        label="Service",
        properties={"id": "user-db", "name": "User DB Cluster", "tier": "Tier 2"},
        graph_name=TEST_GRAPH
    )

    graph_service.upsert_relationship(
        source_label="Service",
        source_id="payment-gateway",
        target_label="Service",
        target_id="auth-service",
        rel_type="DEPENDS_ON",
        properties={"criticality": "high"},
        graph_name=TEST_GRAPH
    )
    graph_service.upsert_relationship(
        source_label="Service",
        source_id="auth-service",
        target_label="Service",
        target_id="user-db",
        rel_type="DEPENDS_ON",
        properties={"criticality": "critical"},
        graph_name=TEST_GRAPH
    )

    paths = graph_service.get_dependency_blast_radius("payment-gateway", max_depth=5, graph_name=TEST_GRAPH)
    assert len(paths) == 2
    # First hop
    assert paths[0].dependent_service == "auth-service"
    assert paths[0].depth == 1
    assert paths[0].traversal_path == ["payment-gateway", "auth-service"]
    # Second hop
    assert paths[1].dependent_service == "user-db"
    assert paths[1].depth == 2
    assert paths[1].traversal_path == ["payment-gateway", "auth-service", "user-db"]


def test_decision_lineage_and_supersession(graph_service):
    """Test ADR supersession chaining (ADR-004 supersedes ADR-001)."""
    graph_service.upsert_entity(
        label="Decision",
        properties={
            "id": "adr-001",
            "title": "ADR-001: PostgreSQL Database",
            "status": "SUPERSEDED",
            "rationale": "Initial ACID relational storage.",
            "decision_date": "2025-01-10"
        },
        graph_name=TEST_GRAPH
    )
    graph_service.upsert_entity(
        label="Decision",
        properties={
            "id": "adr-004",
            "title": "ADR-004: Multi-region CockroachDB",
            "status": "ACCEPTED",
            "rationale": "Adopt CockroachDB for multi-region active-active transaction isolation.",
            "decision_date": "2026-03-15"
        },
        graph_name=TEST_GRAPH
    )

    # Link newer -> older with SUPERSEDES
    graph_service.upsert_relationship(
        source_label="Decision",
        source_id="adr-004",
        target_label="Decision",
        target_id="adr-001",
        rel_type="SUPERSEDES",
        properties={"reason": "Single-region Postgres reached replication limits"},
        graph_name=TEST_GRAPH
    )

    # Audit ADR-004: Should show ADR-001 as superseded prior decision
    lineage_004 = graph_service.get_decision_lineage("adr-004", graph_name=TEST_GRAPH)
    assert lineage_004 is not None
    assert lineage_004.status == "ACCEPTED"
    assert len(lineage_004.superseded_prior_decisions) == 1
    assert lineage_004.superseded_prior_decisions[0].id == "adr-001"
    assert len(lineage_004.superseded_by_newer_decisions) == 0

    # Audit ADR-001: Should show ADR-004 as newer superseding decision
    lineage_001 = graph_service.get_decision_lineage("adr-001", graph_name=TEST_GRAPH)
    assert lineage_001 is not None
    assert lineage_001.status == "SUPERSEDED"
    assert len(lineage_001.superseded_prior_decisions) == 0
    assert len(lineage_001.superseded_by_newer_decisions) == 1
    assert lineage_001.superseded_by_newer_decisions[0].id == "adr-004"


def test_incident_resolutions_and_resolvers(graph_service):
    """Test incident linking and resolver discovery."""
    graph_service.upsert_entity(
        label="Incident",
        properties={
            "id": "inc-101",
            "title": "INC-101: Connection Pool Exhaustion",
            "severity": "SEV-1",
            "occurred_at": "2026-04-12T10:15:00Z"
        },
        graph_name=TEST_GRAPH
    )
    # Incident affected payment-gateway
    graph_service.upsert_relationship(
        source_label="Incident",
        source_id="inc-101",
        target_label="Service",
        target_id="payment-gateway",
        rel_type="AFFECTED",
        graph_name=TEST_GRAPH
    )
    # Alex Rivera resolved inc-101
    graph_service.upsert_relationship(
        source_label="Person",
        source_id="alex-rivera",
        target_label="Incident",
        target_id="inc-101",
        rel_type="RESOLVED",
        properties={"lead_resolver": True, "resolution_summary": "Expanded connection pool"},
        graph_name=TEST_GRAPH
    )

    resolutions = graph_service.get_incident_resolutions("payment-gateway", graph_name=TEST_GRAPH)
    assert len(resolutions) == 1
    assert resolutions[0].incident_id == "inc-101"
    assert resolutions[0].resolver_id == "alex-rivera"
    assert resolutions[0].resolver_name == "Alex Rivera"


def test_count_graph_metrics(graph_service):
    """Verify total nodes and edge counting."""
    nodes, edges = graph_service.count_graph_metrics(graph_name=TEST_GRAPH)
    assert nodes >= 6  # Sarah, Alex, Core Payments, Payment Gateway, Auth, User DB, ADRs, Incident
    assert edges >= 6
