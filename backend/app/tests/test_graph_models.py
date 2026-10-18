import pytest
from datetime import datetime, timezone
from app.models.graph import (
    StalenessStatus,
    IncidentSeverity,
    DecisionStatus,
    DependencyType,
    RelationshipType,
    PersonNode,
    TeamNode,
    ProjectNode,
    ServiceNode,
    DocumentNode,
    ChunkNode,
    TicketNode,
    ChatMessageNode,
    DecisionNode,
    IncidentNode,
    SkillNode,
    MemberOfRel,
    OwnsRel,
    WorkedOnRel,
    KnowsAboutRel,
    DependsOnRel,
    SupportedByRel,
    DecidedInRel,
    ResolvedRel,
    MentionedInRel,
    PartOfRel,
    NextChunkRel,
    SupersedesRel,
    RelatedToRel,
    ServiceOwnershipResult,
    OwnerRecord,
    TeamOwnerRecord,
    InferredExpertRecord,
    DependencyPathResult,
    DecisionLineageResult,
    IncidentResolutionResult,
    UpsertEntityResult,
)


def test_person_node_creation():
    person = PersonNode(
        id="sarah-chen",
        name="Sarah Chen",
        email="sarah.chen@northstar.internal",
        role="Staff Backend Engineer",
        department="Core Infrastructure",
        seniority="Staff",
        skills=["Distributed Systems", "Go", "FalkorDB"]
    )
    assert person.id == "sarah-chen"
    assert person.freshness_score == 1.0
    assert person.staleness_status == StalenessStatus.ACTIVE
    assert person.connections_count == 0
    assert "FalkorDB" in person.skills


def test_team_node_creation():
    team = TeamNode(
        id="core-payments",
        name="Core Payments Team",
        department="Engineering",
        slack_channel="#core-payments",
        lead_person_id="sarah-chen"
    )
    assert team.id == "core-payments"
    assert team.department == "Engineering"


def test_service_node_creation():
    service = ServiceNode(
        id="payment-gateway",
        name="Payment Gateway",
        tier="Tier 1",
        repo_url="github.com/northstar/payment-gateway",
        language="Go",
        active_version="v2.14.0"
    )
    assert service.tier == "Tier 1"
    assert service.active_version == "v2.14.0"


def test_project_node_creation():
    proj = ProjectNode(
        id="multi-region-2026",
        name="Multi-Region Active-Active Expansion",
        status="IN_PROGRESS"
    )
    assert proj.status == "IN_PROGRESS"


def test_document_and_chunk_node_creation():
    doc = DocumentNode(
        id="doc-adr-004",
        title="ADR-004: Multi-region CockroachDB",
        source_type="markdown",
        uri="docs/adr/ADR-004.md",
        checksum="a1b2c3d4e5"
    )
    assert doc.source_type == "markdown"

    chunk = ChunkNode(
        id="chunk-adr-004-1",
        source_id="doc-adr-004",
        text="CockroachDB was selected to replace single-region PostgreSQL...",
        chunk_index=0,
        page_number=1,
        char_offset_start=0,
        char_offset_end=450
    )
    assert chunk.source_id == "doc-adr-004"
    assert chunk.chunk_index == 0


def test_decision_node_creation():
    dec = DecisionNode(
        id="adr-004",
        title="ADR-004: Multi-region CockroachDB",
        status=DecisionStatus.ACCEPTED,
        rationale="Support multi-region active-active transaction isolation.",
        superseded_by_id=None
    )
    assert dec.status == DecisionStatus.ACCEPTED
    assert "multi-region" in dec.rationale.lower()


def test_incident_node_creation():
    inc = IncidentNode(
        id="inc-101",
        title="INC-101: Connection Pool Exhaustion",
        severity=IncidentSeverity.SEV1,
        occurred_at=datetime.now(timezone.utc)
    )
    assert inc.severity == IncidentSeverity.SEV1


def test_ticket_chat_and_skill_nodes():
    ticket = TicketNode(id="eng-402", title="Upgrade FalkorDB client", status="OPEN")
    chat = ChatMessageNode(
        id="msg-901",
        channel="#incidents",
        timestamp=datetime.now(timezone.utc),
        text="Mitigation applied, connection pool expanded."
    )
    skill = SkillNode(id="graph-databases", name="Graph Databases", category="Data")

    assert ticket.id == "eng-402"
    assert chat.channel == "#incidents"
    assert skill.category == "Data"


def test_all_13_relationships():
    now = datetime.now(timezone.utc)
    
    r1 = MemberOfRel(role="Tech Lead", is_lead=True)
    r2 = OwnsRel(is_primary=True, assigned_at=now)
    r3 = WorkedOnRel(contribution_type="design")
    r4 = KnowsAboutRel(is_inferred=True, confidence=0.88, reason="Author of 3 ADRs")
    r5 = DependsOnRel(dependency_type=DependencyType.SYNC, criticality="high")
    r6 = SupportedByRel(tier="Tier 1")
    r7 = DecidedInRel(impact_level="critical")
    r8 = ResolvedRel(lead_resolver=True, resolution_summary="Restarted pool")
    r9 = MentionedInRel(frequency=4, sentiment="neutral")
    r10 = PartOfRel(index=2, section_heading="Architecture")
    r11 = NextChunkRel(sequence=1)
    r12 = SupersedesRel(superseded_date=now, reason="Multi-region scale requirements")
    r13 = RelatedToRel(strength=0.95)

    assert r1.is_lead is True
    assert r2.is_primary is True
    assert r4.confidence == 0.88
    assert r5.dependency_type == DependencyType.SYNC
    assert r12.reason == "Multi-region scale requirements"
    assert r13.strength == 0.95


def test_query_result_schemas():
    ownership = ServiceOwnershipResult(
        service_id="payment-gateway",
        service_name="Payment Gateway",
        tier="Tier 1",
        explicit_owners=[OwnerRecord(id="p1", name="Sarah Chen", role="Staff Eng")],
        owning_teams=[TeamOwnerRecord(id="t1", name="Core Payments", department="Engineering")],
        inferred_experts=[InferredExpertRecord(id="p2", name="Alex Rivera", confidence=0.9)]
    )
    assert len(ownership.explicit_owners) == 1
    assert len(ownership.owning_teams) == 1
    assert len(ownership.inferred_experts) == 1

    dep_path = DependencyPathResult(
        source_service="payment-gateway",
        dependent_service="auth-service",
        dependent_name="Auth Service",
        depth=1,
        traversal_path=["payment-gateway", "auth-service"]
    )
    assert dep_path.depth == 1
    assert len(dep_path.traversal_path) == 2

    lineage = DecisionLineageResult(
        decision_id="adr-004",
        title="CockroachDB",
        status="ACCEPTED",
        rationale="Scale",
        superseded_prior_decisions=[
            {"id": "adr-001", "title": "Postgres", "status": "SUPERSEDED", "date": "2025-01-10"}
        ]
    )
    assert len(lineage.superseded_prior_decisions) == 1
    assert lineage.superseded_prior_decisions[0].id == "adr-001"
