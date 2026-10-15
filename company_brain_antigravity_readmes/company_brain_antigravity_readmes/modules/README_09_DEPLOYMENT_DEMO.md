# Module 09 — Deployment, Documentation, and Hackathon Demo

## Goal
Make the project reproducible for judges and provide the required submission artifacts.

## Deployment
- Provide Docker Compose for the required local stack.
- Include health checks and startup order.
- Document ports and environment variables.
- Explain how to start, stop, reset, and inspect logs.
- Include a clear local fallback if hosted deployment is not available.
- Never put credentials in Dockerfiles, compose files, or tracked `.env` files.
- Pin or constrain dependencies to tested versions where practical.
- Include a small synthetic dataset and seed/ingestion instructions.

## Documentation
Root README must contain:
1. Project name and track: Company Brain.
2. Problem statement and target users.
3. Features and limitations.
4. Architecture diagram.
5. Technology stack.
6. Graph data model and relationship direction.
7. Important Cypher queries and graph algorithms.
8. Model/provider configuration.
9. Installation and environment setup.
10. Run, test, and troubleshooting instructions.
11. Demo workflow.
12. AI coding assistant disclosure where applicable.
13. Team contributions if relevant.

Also maintain:
- `docs/ARCHITECTURE.md`
- `docs/GRAPH_SCHEMA.md`
- `docs/API_CONTRACT.md`
- `docs/TECH_DECISIONS.md`
- `docs/DEMO_SCRIPT.md`

## Demo storyline (3–5 minutes)
Use a fictional company with synthetic records.

1. Show source documents, tickets, and decision records.
2. Ingest them and show ingestion status.
3. Ask who owns a service and show source evidence.
4. Ask why an architecture decision was made and open the original source.
5. Ask a multi-hop question about an incident and a related dependency.
6. Add or update a decision document and run synchronization.
7. Ask again and show updated current knowledge plus historical record.
8. Demonstrate a conflicting or unsupported question and show the system's honest warning/abstention.
9. Briefly show FalkorDB graph nodes/relationships and the key Cypher query.

## Submission checklist
- Public source-code repository.
- Setup README and graph data model.
- Important Cypher queries/graph algorithms.
- Demo video showing a working project.
- Live deployment or complete local setup instructions.
- Explicit track listing.
- AI coding assistant disclosure if used.
- Confirm that all submitted data is public, synthetic, or otherwise authorized.
- Ensure the team can explain graph schema, query logic, architecture, and technical choices.

## Acceptance criteria
- A fresh user can follow setup instructions without undocumented manual steps.
- Demo works from a clean start.
- All claims in demo are reproducible with the included synthetic data.
- Known limitations are clearly stated.
