# Synthetic Demo Data

Use only synthetic fictional company data in this directory.

## Required sample corpus
Create a fictional company named `Northstar Systems` with:
- 8–12 fictional employees
- 3 teams
- 3 projects
- 3 services
- 5 architecture/operational decisions, including one superseded decision
- 5 incidents with resolutions
- 10 tickets or chat extracts
- 10–15 source documents in Markdown or JSON

## Required connected scenario
Create one linked story:
- A fictional employee owns or works on a payment service.
- A documented decision explains why the service uses a database.
- An incident links to the service and a prior resolution.
- Another service/project depends on the payment service.
- A later decision supersedes an earlier one.
- Include one contradictory source that cannot be resolved automatically.
- Include one question with no supporting evidence.

Use obvious fictional names and do not imitate real private organizational records. Each record should have stable IDs, dates, source titles, and enough detail to support a graph path and citation.

## Acceptance criteria
The sample data must allow the demo questions in `docs/DEMO_SCRIPT.md` to be answered from graph relationships and source evidence.
