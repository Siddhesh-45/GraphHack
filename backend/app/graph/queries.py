import logging
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timezone
from app.graph.connection import FalkorDBConnectionService, get_graph_connection
from app.models.graph import (
    ServiceOwnershipResult,
    OwnerRecord,
    TeamOwnerRecord,
    InferredExpertRecord,
    DependencyPathResult,
    DecisionLineageResult,
    PriorDecisionSummary,
    IncidentResolutionResult,
    UpsertEntityResult,
)

logger = logging.getLogger(__name__)


class GraphQueryService:
    """
    High-performance parameterized Cypher service layer on FalkorDB.
    All Cypher statements strictly use $params to guarantee injection immunity.
    """
    def __init__(self, connection: Optional[FalkorDBConnectionService] = None):
        self.connection = connection or get_graph_connection()

    def upsert_entity(
        self,
        label: str,
        properties: Dict[str, Any],
        graph_name: Optional[str] = None
    ) -> UpsertEntityResult:
        """
        Idempotently create or update an entity node using Cypher MERGE.
        Maintains created_at and updated_at ISO timestamps.
        """
        entity_id = properties.get("id")
        if not entity_id:
            raise ValueError("Entity properties dictionary must contain an 'id' field")

        now_iso = datetime.now(timezone.utc).isoformat()
        props_copy = dict(properties)
        props_copy["now_iso"] = now_iso

        # Build dynamic property setters parameterized cleanly
        set_clauses_create = [
            f"n.{k} = ${k}" for k in props_copy if k not in ("id", "now_iso", "created_at", "updated_at")
        ]
        set_clauses_create.append("n.created_at = $now_iso")
        set_clauses_create.append("n.updated_at = $now_iso")

        set_clauses_match = [
            f"n.{k} = ${k}" for k in props_copy if k not in ("id", "now_iso", "created_at", "updated_at")
        ]
        set_clauses_match.append("n.updated_at = $now_iso")

        on_create_str = ", ".join(set_clauses_create) if set_clauses_create else "n.created_at = $now_iso"
        on_match_str = ", ".join(set_clauses_match) if set_clauses_match else "n.updated_at = $now_iso"

        cypher = f"""
        MERGE (n:{label} {{id: $id}})
        ON CREATE SET {on_create_str}
        ON MATCH SET {on_match_str}
        RETURN n.id AS id
        """

        res = self.connection.query(cypher, props_copy, graph_name=graph_name)
        upserted_id = res.result_set[0][0] if (res and res.result_set) else entity_id
        action = "created" if (res and getattr(res, "nodes_created", 0) > 0) else "updated"

        return UpsertEntityResult(id=upserted_id, label=label, action=action)

    def upsert_relationship(
        self,
        source_label: str,
        source_id: str,
        target_label: str,
        target_id: str,
        rel_type: str,
        properties: Optional[Dict[str, Any]] = None,
        graph_name: Optional[str] = None
    ) -> bool:
        """
        Idempotently link two existing entity nodes via a typed directed relationship.
        """
        params: Dict[str, Any] = {
            "source_id": source_id,
            "target_id": target_id,
            "now_iso": datetime.now(timezone.utc).isoformat(),
        }

        rel_props = properties or {}
        set_clauses = ["r.updated_at = $now_iso"]
        for k, v in rel_props.items():
            param_key = f"prop_{k}"
            params[param_key] = v
            set_clauses.append(f"r.{k} = ${param_key}")

        on_create_str = ", ".join(["r.created_at = $now_iso"] + set_clauses)
        on_match_str = ", ".join(set_clauses)

        cypher = f"""
        MATCH (s:{source_label} {{id: $source_id}}), (t:{target_label} {{id: $target_id}})
        MERGE (s)-[r:{rel_type}]->(t)
        ON CREATE SET {on_create_str}
        ON MATCH SET {on_match_str}
        RETURN type(r) AS rel_type
        """

        res = self.connection.query(cypher, params, graph_name=graph_name)
        return bool(res and res.result_set)

    def get_service_ownership(
        self,
        service_id: str,
        graph_name: Optional[str] = None
    ) -> Optional[ServiceOwnershipResult]:
        """
        Retrieve both explicit contractual owners (Person & Team) and inferred experts for a service.
        """
        cypher = """
        MATCH (s:Service {id: $service_id})
        OPTIONAL MATCH (p_explicit:Person)-[:OWNS]->(s)
        OPTIONAL MATCH (t:Team)-[:OWNS]->(s)
        OPTIONAL MATCH (p_inferred:Person)-[k:KNOWS_ABOUT]->(s)
        RETURN 
            s.id AS service_id,
            s.name AS service_name,
            s.tier AS tier,
            [p in collect(DISTINCT p_explicit) WHERE p IS NOT NULL | {
                id: p.id,
                name: p.name,
                role: p.role,
                type: "explicit_owner"
            }] AS explicit_owners,
            [tm in collect(DISTINCT t) WHERE tm IS NOT NULL | {
                id: tm.id,
                name: tm.name,
                department: tm.department
            }] AS owning_teams,
            [pi in collect(DISTINCT p_inferred) WHERE pi IS NOT NULL | {
                id: pi.id,
                name: pi.name,
                role: pi.role,
                confidence: coalesce(pi.confidence, 0.75),
                reason: coalesce(pi.reason, "Inferred domain activity"),
                type: "inferred_expert"
            }] AS inferred_experts
        """
        res = self.connection.query(cypher, {"service_id": service_id}, graph_name=graph_name)
        if not res or not res.result_set:
            return None

        row = res.result_set[0]
        svc_id, svc_name, svc_tier, owners_raw, teams_raw, experts_raw = row

        explicit_owners = [
            OwnerRecord(
                id=o["id"],
                name=o["name"],
                role=o.get("role"),
                type=o.get("type", "explicit_owner")
            )
            for o in owners_raw if isinstance(o, dict) and o.get("id")
        ]

        owning_teams = [
            TeamOwnerRecord(
                id=t["id"],
                name=t["name"],
                department=t.get("department", "Engineering")
            )
            for t in teams_raw if isinstance(t, dict) and t.get("id")
        ]

        inferred_experts = [
            InferredExpertRecord(
                id=e["id"],
                name=e["name"],
                role=e.get("role"),
                confidence=float(e.get("confidence", 0.75)),
                reason=e.get("reason"),
                type="inferred_expert"
            )
            for e in experts_raw if isinstance(e, dict) and e.get("id")
        ]

        return ServiceOwnershipResult(
            service_id=svc_id,
            service_name=svc_name,
            tier=svc_tier,
            explicit_owners=explicit_owners,
            owning_teams=owning_teams,
            inferred_experts=inferred_experts,
        )

    def get_dependency_blast_radius(
        self,
        service_id: str,
        max_depth: int = 5,
        graph_name: Optional[str] = None
    ) -> List[DependencyPathResult]:
        """
        Recursive multi-hop traversal along [:DEPENDS_ON] edges up to max_depth.
        Returns ordered blast radius paths from shallowest to deepest.
        """
        clamped_depth = max(1, min(max_depth, 10))
        cypher = f"""
        MATCH path = (root:Service {{id: $service_id}})-[:DEPENDS_ON*1..{clamped_depth}]->(dep:Service)
        RETURN 
            root.id AS source_service,
            dep.id AS dependent_service,
            dep.name AS dependent_name,
            dep.tier AS tier,
            length(path) AS depth,
            [node in nodes(path) | node.id] AS traversal_path
        ORDER BY depth ASC
        """
        res = self.connection.query(cypher, {"service_id": service_id}, graph_name=graph_name)
        if not res or not res.result_set:
            return []

        results: List[DependencyPathResult] = []
        for row in res.result_set:
            src, dep_id, dep_name, tier, depth, path = row
            results.append(DependencyPathResult(
                source_service=src,
                dependent_service=dep_id,
                dependent_name=dep_name,
                tier=tier,
                depth=depth,
                traversal_path=list(path) if isinstance(path, (list, tuple)) else []
            ))
        return results

    def get_decision_lineage(
        self,
        decision_id: str,
        max_depth: int = 4,
        graph_name: Optional[str] = None
    ) -> Optional[DecisionLineageResult]:
        """
        Trace decision supersession lineage: find older ADRs superseded by this decision,
        and find newer ADRs that supersede this decision.
        """
        clamped_depth = max(1, min(max_depth, 8))
        cypher = f"""
        MATCH (target:Decision {{id: $decision_id}})
        OPTIONAL MATCH (target)-[:SUPERSEDES*1..{clamped_depth}]->(prior:Decision)
        OPTIONAL MATCH (newer:Decision)-[:SUPERSEDES*1..{clamped_depth}]->(target)
        RETURN 
            target.id AS decision_id,
            target.title AS title,
            target.status AS status,
            target.rationale AS rationale,
            target.decision_date AS decision_date,
            [p in collect(DISTINCT prior) WHERE p IS NOT NULL | {{
                id: p.id,
                title: p.title,
                status: p.status,
                date: p.decision_date
            }}] AS superseded_prior_decisions,
            [n in collect(DISTINCT newer) WHERE n IS NOT NULL | {{
                id: n.id,
                title: n.title,
                status: n.status,
                date: n.decision_date
            }}] AS superseded_by_newer_decisions
        """
        res = self.connection.query(cypher, {"decision_id": decision_id}, graph_name=graph_name)
        if not res or not res.result_set:
            return None

        row = res.result_set[0]
        d_id, title, status, rationale, date, prior_raw, newer_raw = row

        prior_decisions = [
            PriorDecisionSummary(
                id=p["id"],
                title=p["title"],
                status=p["status"],
                date=str(p.get("date")) if p.get("date") else None
            )
            for p in prior_raw if isinstance(p, dict) and p.get("id")
        ]

        newer_decisions = [
            PriorDecisionSummary(
                id=n["id"],
                title=n["title"],
                status=n["status"],
                date=str(n.get("date")) if n.get("date") else None
            )
            for n in newer_raw if isinstance(n, dict) and n.get("id")
        ]

        return DecisionLineageResult(
            decision_id=d_id,
            title=title,
            status=status,
            rationale=rationale,
            decision_date=str(date) if date else None,
            superseded_prior_decisions=prior_decisions,
            superseded_by_newer_decisions=newer_decisions,
        )

    def get_incident_resolutions(
        self,
        service_id: str,
        limit: int = 10,
        graph_name: Optional[str] = None
    ) -> List[IncidentResolutionResult]:
        """
        Discover past incidents affecting a service and the engineers who resolved them.
        """
        clamped_limit = max(1, min(limit, 50))
        cypher = """
        MATCH (s:Service {id: $service_id})<-[:AFFECTED]-(i:Incident)<-[:RESOLVED]-(p:Person)
        RETURN 
            i.id AS incident_id,
            i.title AS incident_title,
            i.severity AS severity,
            i.occurred_at AS occurred_at,
            p.id AS resolver_id,
            p.name AS resolver_name,
            p.role AS resolver_role
        ORDER BY i.occurred_at DESC
        LIMIT $limit
        """
        res = self.connection.query(
            cypher,
            {"service_id": service_id, "limit": clamped_limit},
            graph_name=graph_name
        )
        if not res or not res.result_set:
            return []

        results: List[IncidentResolutionResult] = []
        for row in res.result_set:
            inc_id, inc_title, sev, occ, res_id, res_name, res_role = row
            results.append(IncidentResolutionResult(
                incident_id=inc_id,
                incident_title=inc_title,
                severity=sev,
                occurred_at=str(occ) if occ else None,
                resolver_id=res_id,
                resolver_name=res_name,
                resolver_role=res_role
            ))
        return results

    def count_graph_metrics(self, graph_name: Optional[str] = None) -> Tuple[int, int]:
        """
        Return (total_nodes, total_edges) in the active graph.
        """
        res_nodes = self.connection.query("MATCH (n) RETURN count(n) AS c", graph_name=graph_name)
        total_nodes = res_nodes.result_set[0][0] if (res_nodes and res_nodes.result_set) else 0

        res_edges = self.connection.query("MATCH ()-[r]->() RETURN count(r) AS c", graph_name=graph_name)
        total_edges = res_edges.result_set[0][0] if (res_edges and res_edges.result_set) else 0

        return int(total_nodes), int(total_edges)


_graph_query_instance: Optional[GraphQueryService] = None


def get_graph_query_service() -> GraphQueryService:
    global _graph_query_instance
    if _graph_query_instance is None:
        _graph_query_instance = GraphQueryService()
    return _graph_query_instance
