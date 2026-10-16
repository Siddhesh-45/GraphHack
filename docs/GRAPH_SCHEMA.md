# Graph Data Model & Schema — Company Brain

## 1. Node Types
- `Person`: Employee or contractor (`id`, `name`, `email`, `role`, `department`).
- `Team`: Engineering organizational team (`id`, `name`, `department`).
- `Service`: Microservice or infrastructure system (`id`, `name`, `tier`, `repo_url`).
- `Project`: Roadmap project or initiative (`id`, `name`, `status`).
- `Decision`: Architecture Decision Record (`id`, `title`, `status`, `decision_date`, `rationale`).
- `Incident`: Production incident (`id`, `title`, `severity`, `occurred_at`, `resolved_at`).
- `Document`: Ingested source artifact (`id`, `title`, `source_type`, `checksum`, `uri`).
- `Chunk`: Text passage with offset tracking (`id`, `source_id`, `text`, `page_number`, `char_offset_start`).
- `Ticket`: Issue or task (`id`, `title`, `status`, `created_at`).
- `ChatMessage`: Slack / Teams extract (`id`, `channel`, `timestamp`, `text`).
- `Skill`: Technical capability or domain (`id`, `name`, `category`).

---

## 2. Core Cypher Queries

### Service Ownership Lookup
```cypher
MATCH (s:Service {id: $service_id})
OPTIONAL MATCH (p:Person)-[:OWNS]->(s)
OPTIONAL MATCH (t:Team)-[:OWNS]->(s)
RETURN s.name, collect(p.name) AS explicit_owners, collect(t.name) AS teams
```

### Decision Supersession Chain
```cypher
MATCH (d:Decision {id: $decision_id})
OPTIONAL MATCH (d)-[:SUPERSEDES*1..5]->(prior:Decision)
RETURN d.title AS active_decision, collect(prior.title) AS superseded_history
```

### Multi-Hop Blast Radius Traversal
```cypher
MATCH path = (root:Service {id: $service_id})-[:DEPENDS_ON*1..5]->(dep:Service)
RETURN root.id, dep.id, dep.tier, length(path) AS depth
ORDER BY depth ASC
```
