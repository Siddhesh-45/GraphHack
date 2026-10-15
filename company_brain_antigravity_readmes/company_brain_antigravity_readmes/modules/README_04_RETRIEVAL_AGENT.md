# Module 04 — GraphRAG Retrieval and Company Brain Agent

## Goal
Implement the core question-answering system. Answers must rely on graph relationships and source evidence, not on LLM memory alone.

## Main flow
1. Accept a user question and optional conversation context.
2. Classify intent into one or more supported query types:
   - ownership/expertise
   - project/service overview
   - decision rationale/history
   - incident/resolution lookup
   - dependency/impact analysis
   - general company knowledge
   - conflicting or stale facts
3. Build a retrieval plan using an allowlisted set of graph query templates.
4. Retrieve graph facts through FalkorDB and source passages through GraphRAG/vector/full-text retrieval.
5. Merge, deduplicate, and rank evidence while preserving provenance.
6. Validate dates, current/superseded status, source authority, and conflicting claims.
7. Generate a concise answer from retrieved evidence only.
8. Attach citations to claims and return graph paths where useful.
9. If evidence is insufficient, ask a clarifying question or say the answer cannot be determined.
10. Return a structured response to the frontend.

## Required design
- Keep intent classification, query planning, graph execution, evidence assembly, answer generation, and validation in separate services.
- Use the GraphRAG SDK's documented `retrieve()` and/or `completion()` APIs after verifying installed-version signatures.
- Prefer deterministic Cypher templates for high-value company questions. Do not let an LLM execute arbitrary Cypher.
- Keep provider/model settings in configuration.
- Add timeouts, bounded retries, and readable provider errors.
- Limit context size and retrieved result count.
- Include conversation context only when relevant; never allow old chat context to override newer source evidence.

## Response schema
Return at least:
```json
{
  "answer": "string",
  "citations": [
    {
      "source_id": "string",
      "source_title": "string",
      "source_uri": "string or null",
      "chunk_id": "string",
      "excerpt": "string",
      "timestamp": "ISO-8601 or null"
    }
  ],
  "graph_paths": [],
  "confidence_label": "high | medium | low | insufficient_evidence",
  "warnings": [],
  "follow_up_questions": []
}
```
Use a real typed model in code. This JSON is a contract example, not a reason to return fake citations.

## Grounding rules
- Each factual claim should be supported by one or more retrieved sources or graph facts.
- If a source contradicts another, show the conflict and explain the rule used to prefer one; do not silently hide the conflict.
- A newer timestamp does not automatically make a source more authoritative. Consider source type and explicit supersession.
- Do not invent numerical confidence scores. Use calibrated labels unless a scoring method is implemented and evaluated.
- Never imply that a person is an expert based only on a mention.
- Do not expose private or unauthorized information.

## Acceptance criteria
- Supports at least five question types using the sample dataset.
- At least one question requires multi-hop graph traversal.
- Citations open the exact supporting source/chunk.
- A no-evidence query returns an honest abstention.
- Conflicting-source questions identify both sources.
- Tests verify answer schema and citation integrity.
