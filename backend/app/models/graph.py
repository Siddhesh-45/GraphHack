from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict


# ==============================================================================
# Enumerations
# ==============================================================================

class StalenessStatus(str, Enum):
    ACTIVE = "ACTIVE"
    STALE_UNVERIFIED = "STALE_UNVERIFIED"
    SUPERSEDED = "SUPERSEDED"


class EntityCategory(str, Enum):
    PERSON = "Person"
    TEAM = "Team"
    SERVICE = "Service"
    PROJECT = "Project"
    DECISION = "Decision"
    INCIDENT = "Incident"
    DOCUMENT = "Document"
    CHUNK = "Chunk"
    TICKET = "Ticket"
    CHAT_MESSAGE = "ChatMessage"
    SKILL = "Skill"


class IncidentSeverity(str, Enum):
    SEV1 = "SEV-1"
    SEV2 = "SEV-2"
    SEV3 = "SEV-3"
    SEV4 = "SEV-4"


class DecisionStatus(str, Enum):
    PROPOSED = "PROPOSED"
    ACCEPTED = "ACCEPTED"
    SUPERSEDED = "SUPERSEDED"
    REJECTED = "REJECTED"
    DEPRECATED = "DEPRECATED"


class DependencyType(str, Enum):
    SYNC = "sync"
    ASYNC = "async"
    DB = "db"
    EVENT = "event"


class RelationshipType(str, Enum):
    MEMBER_OF = "MEMBER_OF"
    OWNS = "OWNS"
    WORKED_ON = "WORKED_ON"
    KNOWS_ABOUT = "KNOWS_ABOUT"
    DEPENDS_ON = "DEPENDS_ON"
    SUPPORTED_BY = "SUPPORTED_BY"
    DECIDED_IN = "DECIDED_IN"
    RESOLVED = "RESOLVED"
    MENTIONED_IN = "MENTIONED_IN"
    PART_OF = "PART_OF"
    NEXT_CHUNK = "NEXT_CHUNK"
    SUPERSEDES = "SUPERSEDES"
    RELATED_TO = "RELATED_TO"


# ==============================================================================
# Base Node & Universal Entity Metadata
# ==============================================================================

class BaseGraphNode(BaseModel):
    """
    Universal entity metadata automatically maintained on all Company Brain nodes.
    """
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    id: str = Field(..., description="Unique slug or alphanumeric identifier for the node")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="ISO-8601 creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="ISO-8601 last mutation timestamp"
    )
    last_verified_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp of most recent document re-ingestion or verification"
    )
    freshness_score: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Composite freshness score between 0.0 (stale) and 1.0 (fresh)"
    )
    connections_count: int = Field(
        default=0,
        ge=0,
        description="Degree centrality: total active relationships connected to this node"
    )
    staleness_status: StalenessStatus = Field(
        default=StalenessStatus.ACTIVE,
        description="Current operational or superseded state"
    )


# ==============================================================================
# 11 Canonical Node Specifications
# ==============================================================================

class PersonNode(BaseGraphNode):
    """Employee, engineer, or contractor within the organization."""
    name: str = Field(..., description="Full legal or preferred display name")
    email: str = Field(..., description="Corporate email address")
    role: Optional[str] = Field(default=None, description="Current role or job title")
    department: Optional[str] = Field(default=None, description="Department or business unit")
    seniority: Optional[str] = Field(default=None, description="Seniority level: Junior, Senior, Staff, Principal")
    skills: List[str] = Field(default_factory=list, description="Canonical skills or competencies")


class TeamNode(BaseGraphNode):
    """Organizational engineering or cross-functional team."""
    name: str = Field(..., description="Team title, e.g. Core Payments Team")
    department: str = Field(..., description="Parent division or department")
    slack_channel: Optional[str] = Field(default=None, description="Primary discussion channel")
    lead_person_id: Optional[str] = Field(default=None, description="ID of the Team Lead Person")


class ProjectNode(BaseGraphNode):
    """Discrete initiative, roadmap milestone, or strategic project."""
    name: str = Field(..., description="Project name")
    status: str = Field(default="IN_PROGRESS", description="Current execution status")
    start_date: Optional[datetime] = Field(default=None, description="Kickoff date")
    target_date: Optional[datetime] = Field(default=None, description="Target release date")
    lead_id: Optional[str] = Field(default=None, description="ID of project lead Person")


class ServiceNode(BaseGraphNode):
    """Microservice, operational application, or storage engine."""
    name: str = Field(..., description="Service identifier or title")
    tier: str = Field(default="Tier 2", description="Operational criticality (Tier 1, Tier 2, Tier 3)")
    repo_url: Optional[str] = Field(default=None, description="VCS repository URL")
    language: Optional[str] = Field(default=None, description="Primary runtime or language")
    active_version: Optional[str] = Field(default=None, description="Current production release tag")


class DocumentNode(BaseGraphNode):
    """Ingested source artifact (PDF, DOCX, Markdown, etc.)."""
    title: str = Field(..., description="Document file title or display name")
    source_type: str = Field(..., description="Source format: pdf, docx, markdown, slack")
    uri: Optional[str] = Field(default=None, description="Location URI, path, or URL")
    checksum: Optional[str] = Field(default=None, description="SHA-256 hash for deduplication")
    file_size_bytes: Optional[int] = Field(default=None, description="Size in bytes")
    mime_type: Optional[str] = Field(default=None, description="MIME content type")


class ChunkNode(BaseGraphNode):
    """Granular text passage extracted for vector and GraphRAG retrieval."""
    source_id: str = Field(..., description="ID of the parent Document node")
    text: str = Field(..., description="Verbatim extracted text content")
    chunk_index: int = Field(..., description="0-indexed ordinal within the parent document")
    page_number: Optional[int] = Field(default=None, description="1-indexed source document page")
    char_offset_start: Optional[int] = Field(default=None, description="Starting character index")
    char_offset_end: Optional[int] = Field(default=None, description="Ending character index")


class TicketNode(BaseGraphNode):
    """Jira ticket, GitHub issue, or incident mitigation task."""
    title: str = Field(..., description="Ticket summary")
    status: str = Field(default="OPEN", description="OPEN, IN_PROGRESS, RESOLVED, CLOSED")
    priority: Optional[str] = Field(default="P2", description="P0, P1, P2, P3")
    resolution_notes: Optional[str] = Field(default=None, description="Resolution notes")
    reporter_id: Optional[str] = Field(default=None, description="Person ID of the reporter")


class ChatMessageNode(BaseGraphNode):
    """Slack, Teams, or conversation thread extract."""
    channel: str = Field(..., description="Channel name or thread ID")
    timestamp: datetime = Field(..., description="Message posted timestamp")
    text: str = Field(..., description="Verbatim message content")
    thread_ts: Optional[str] = Field(default=None, description="Root parent thread identifier")
    sender_person_id: Optional[str] = Field(default=None, description="Sender Person ID")


class DecisionNode(BaseGraphNode):
    """Architecture Decision Record (ADR) or key design determination."""
    title: str = Field(..., description="ADR title (e.g. ADR-004: Multi-region CockroachDB)")
    status: DecisionStatus = Field(default=DecisionStatus.ACCEPTED, description="Lifecycle status")
    decision_date: Optional[datetime] = Field(default=None, description="Date decision was formalized")
    rationale: str = Field(..., description="Core architectural justification")
    superseded_by_id: Optional[str] = Field(default=None, description="ID of the replacing Decision node if any")
    context: Optional[str] = Field(default=None, description="Problem framing and alternatives considered")
    consequences: Optional[str] = Field(default=None, description="Positive and negative trade-offs")


class IncidentNode(BaseGraphNode):
    """Production outage, post-mortem event, or operational alert."""
    title: str = Field(..., description="Incident title (e.g. INC-101: Connection Pool Exhaustion)")
    severity: IncidentSeverity = Field(default=IncidentSeverity.SEV2, description="Severity rating")
    occurred_at: datetime = Field(..., description="Timestamp when outage initiated")
    resolved_at: Optional[datetime] = Field(default=None, description="Timestamp when service recovered")
    root_cause: Optional[str] = Field(default=None, description="Diagnosed root cause")
    postmortem_url: Optional[str] = Field(default=None, description="Link to post-mortem document")


class SkillNode(BaseGraphNode):
    """Technical competency, technology stack, or domain subject."""
    name: str = Field(..., description="Skill label, e.g. Distributed Systems, FalkorDB")
    category: str = Field(default="Engineering", description="Domain: Backend, Frontend, DevOps, Data")
    description: Optional[str] = Field(default=None, description="Competency description")
    canonical_keywords: List[str] = Field(default_factory=list, description="Synonyms and keywords")


# ==============================================================================
# 13 Canonical Relationship Specifications
# ==============================================================================

class BaseGraphRelationship(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class MemberOfRel(BaseGraphRelationship):
    """Person -> Team"""
    role: Optional[str] = Field(default=None, description="Role within team")
    joined_date: Optional[datetime] = Field(default=None)
    is_lead: bool = Field(default=False, description="Whether person is team lead")


class OwnsRel(BaseGraphRelationship):
    """Person/Team -> Service/Project"""
    is_primary: bool = Field(default=True, description="Primary accountable owner")
    assigned_at: Optional[datetime] = Field(default=None)
    source_id: Optional[str] = Field(default=None, description="Document proving ownership")


class WorkedOnRel(BaseGraphRelationship):
    """Person -> Service/Project"""
    role: Optional[str] = Field(default=None)
    last_active_at: Optional[datetime] = Field(default=None)
    contribution_type: Optional[str] = Field(default="code", description="code, review, spec, design")


class KnowsAboutRel(BaseGraphRelationship):
    """Person -> Skill/Service (Inferred subject-matter expertise)"""
    is_inferred: bool = Field(default=True, description="Inferred via graph activity")
    confidence: float = Field(default=0.8, ge=0.0, le=1.0, description="Calculated confidence")
    reason: Optional[str] = Field(default=None, description="Rationale for inferred expertise")


class DependsOnRel(BaseGraphRelationship):
    """Service -> Service"""
    dependency_type: DependencyType = Field(default=DependencyType.SYNC, description="sync, async, db, event")
    criticality: str = Field(default="high", description="high, medium, low")


class SupportedByRel(BaseGraphRelationship):
    """Service -> Team"""
    tier: Optional[str] = Field(default="Tier 1", description="Support tier")
    on_call_schedule: Optional[str] = Field(default=None, description="PagerDuty schedule tag")


class DecidedInRel(BaseGraphRelationship):
    """Decision -> Service/Project"""
    impact_level: Optional[str] = Field(default="critical", description="Impact rating")


class ResolvedRel(BaseGraphRelationship):
    """Person -> Incident"""
    lead_resolver: bool = Field(default=True, description="Primary mitigation engineer")
    resolution_summary: Optional[str] = Field(default=None, description="Summary of action taken")


class MentionedInRel(BaseGraphRelationship):
    """Any Entity -> Chunk"""
    frequency: int = Field(default=1, ge=1, description="Mentions in chunk")
    sentiment: Optional[str] = Field(default="neutral", description="positive, neutral, negative")


class PartOfRel(BaseGraphRelationship):
    """Chunk -> Document"""
    index: int = Field(..., description="Sequential index within document")
    section_heading: Optional[str] = Field(default=None, description="Section heading")


class NextChunkRel(BaseGraphRelationship):
    """Chunk -> Chunk"""
    sequence: int = Field(default=1, description="Sequential edge offset")


class SupersedesRel(BaseGraphRelationship):
    """Decision (Newer) -> Decision (Older)"""
    superseded_date: Optional[datetime] = Field(default=None, description="Date of invalidation")
    reason: Optional[str] = Field(default=None, description="Justification for superseding prior ADR")


class RelatedToRel(BaseGraphRelationship):
    """Any Entity -> Any Entity"""
    relationship_note: Optional[str] = Field(default=None)
    strength: float = Field(default=1.0, ge=0.0, le=1.0)


# ==============================================================================
# Query Result Transfer Schemas
# ==============================================================================

class OwnerRecord(BaseModel):
    id: str
    name: str
    role: Optional[str] = None
    type: str = "explicit_owner"


class TeamOwnerRecord(BaseModel):
    id: str
    name: str
    department: str


class InferredExpertRecord(BaseModel):
    id: str
    name: str
    role: Optional[str] = None
    confidence: float = 0.5
    reason: Optional[str] = None
    type: str = "inferred_expert"


class ServiceOwnershipResult(BaseModel):
    service_id: str
    service_name: str
    tier: Optional[str] = None
    explicit_owners: List[OwnerRecord] = Field(default_factory=list)
    owning_teams: List[TeamOwnerRecord] = Field(default_factory=list)
    inferred_experts: List[InferredExpertRecord] = Field(default_factory=list)


class DependencyPathResult(BaseModel):
    source_service: str
    dependent_service: str
    dependent_name: str
    tier: Optional[str] = None
    depth: int
    traversal_path: List[str]


class PriorDecisionSummary(BaseModel):
    id: str
    title: str
    status: str
    date: Optional[str] = None


class DecisionLineageResult(BaseModel):
    decision_id: str
    title: str
    status: str
    rationale: str
    decision_date: Optional[str] = None
    superseded_prior_decisions: List[PriorDecisionSummary] = Field(default_factory=list)
    superseded_by_newer_decisions: List[PriorDecisionSummary] = Field(default_factory=list)


class IncidentResolutionResult(BaseModel):
    incident_id: str
    incident_title: str
    severity: str
    occurred_at: Optional[str] = None
    resolver_id: str
    resolver_name: str
    resolver_role: Optional[str] = None


class UpsertEntityResult(BaseModel):
    id: str
    label: str
    action: str  # "created" or "updated"
