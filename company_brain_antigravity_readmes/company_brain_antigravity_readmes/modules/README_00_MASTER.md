# Module 00 — Orchestration Prompt

## Purpose
Use this file as the project manager prompt for Antigravity. Read `../README.md` first.

## Instructions
- Treat each module README as a binding implementation specification.
- Work in the order: 01 Foundation → 02 Graph Schema → 03 Ingestion → 04 Retrieval Agent → 05 Evidence/Freshness → 06 Frontend → 07 API Integration → 08 Testing/Security → 09 Deployment/Demo.
- Before coding a module, inspect the current repository and dependencies.
- Do not rewrite completed modules without a concrete reason.
- Keep API contracts, graph schema, error shapes, source IDs, and citation structures consistent.
- Build vertical slices that can be run and tested.
- Use FalkorDB for core company reasoning; don't substitute a conventional database or static JSON for graph behavior.
- Never invent credentials, data sources, model IDs, or test results.
- Use synthetic company data in the demo.
- Document all non-obvious decisions in `docs/TECH_DECISIONS.md`.
- Update this module's status at the end of each module.

## Required completion report for every module
1. What was implemented.
2. Files created or modified.
3. Exact commands run.
4. Test results.
5. Screenshots or sample API output when relevant.
6. Known limitations and risks.
7. Whether the module is ready for integration.

## Final integration requirement
The app must support this complete path:
synthetic source files → ingestion → FalkorDB graph + provenance → user question → graph and document retrieval → answer with citations → UI evidence panel.
