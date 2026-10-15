# Module 05 — Evidence, Decision History, Freshness, and Impact Analysis

## Goal
Make Company Brain trustworthy over time. Implement evidence inspection, decision history, stale-source warnings, conflict handling, and dependency analysis.

## A. Evidence and explainability
- Store source ID, source type, source title, URI/path, chunk ID, excerpt, page/offset when available, timestamps, and extraction method.
- Connect decisions and extracted facts to supporting chunks.
- Provide a “Why this answer?” payload showing evidence and relevant graph paths.
- Verify citation IDs exist before returning them.
- Never render an invented URL or citation as a real source.

## B. Decision history
- Represent decisions as nodes with title, outcome, rationale, status, decision date, and source references.
- Use `SUPERSEDES` or an equivalent explicit relationship to represent replacement.
- Preserve prior decisions instead of deleting them.
- If there are competing decisions without a clear supersession relationship, label the state as conflicting/uncertain.
- Create queries for current decision, decision timeline, and evidence behind the decision.

## C. Freshness and synchronization
- Track source checksum, last modified time where available, last ingestion time, and processing status.
- Detect changed sample sources and reprocess them idempotently.
- Detect removed sources and mark associated facts as potentially stale or retracted according to a documented policy; do not blindly delete historical decisions.
- Flag facts whose source is old, missing, superseded, or not revalidated.
- Do not label a fact “stale” based only on age unless a configured policy supports that label. Use “last verified” where appropriate.

## D. Conflicting knowledge
- Identify incompatible facts about ownership, project status, architecture, or decisions.
- Compare source authority, timestamps, explicit supersession, and directness of evidence.
- Keep both supporting records available to the user.
- If there is no defensible resolution, present the conflict and request human confirmation.

## E. Expertise and ownership
- Prefer explicit `OWNS` records for ownership.
- Estimate expertise from relevant work history, incident resolutions, authored decisions, and skills only when supported by evidence.
- Clearly label inferred expertise as inferred.
- Provide reasons and supporting sources for ranked suggestions.
- Never imply that a person is available, on call, or responsible now unless the source confirms it.

## F. Impact analysis
- Use graph traversal over `DEPENDS_ON` and relevant project/service relationships.
- Return the traversal path and distinguish direct from indirect dependencies.
- Label results as “potentially affected”, not confirmed breakage.
- Include the assumptions and evidence for each affected node.

## Acceptance criteria
- A new decision can supersede an old decision without deleting history.
- The UI/API can show evidence behind a claim.
- Changed source fixture updates the graph without duplication.
- Conflicts are surfaced instead of silently overwritten.
- Impact query returns path and dependency depth.
- Unit tests cover temporal ordering, conflict policy, and provenance integrity.
