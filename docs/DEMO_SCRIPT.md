# Hackathon Demo Script (3–5 Minutes) — Company Brain

Built for **FalkorDB Graph Hacks 2026 (Track 03: Company Brain)**.

```text
[0:00 - 0:45] INTRODUCTION & THE PROBLEM
- Problem: Organizations lose institutional context across PDFs, Slack, and Jira.
- Solution: Company Brain uses FalkorDB as the primary context layer.

[0:45 - 1:30] LIVE INGESTION & FALKORDB GRAPH FORMATION
- Show upload of Northstar Systems ADRs and Team Charters.
- Verify real-time entity extraction and Cypher MERGE queries.

[1:30 - 2:30] MULTI-HOP QUESTION & VERIFIED CITATIONS
- Ask: "Who owns Payment Gateway, and why PostgreSQL?"
- Show Sarah Chen ownership and ADR-001 citation pill.
- Open verbatim chunk drawer with page offsets.

[2:30 - 3:30] DECISION SUPERSESSION & FRESHNESS DECAY
- Ask: "Is PostgreSQL still active?"
- Show ADR-004 superseding ADR-001 and 6-factor freshness decay score.

[3:30 - 4:15] BLAST RADIUS IMPACT ANALYSIS
- Select Auth Service.
- Traverse recursive [:DEPENDS_ON*1..5] to calculate downstream blast radius.

[4:15 - 4:45] HONEST ABSTENTION & CONCLUSION
- Ask unrecorded budget question -> System abstains with 'insufficient_evidence'.
- Conclude demo.
```
