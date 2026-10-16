# System Architecture — Company Brain

## Overview
**Company Brain** is a graph-native organizational intelligence system built for the FalkorDB Graph Hacks (Track 03: Company Brain). It connects unstructured institutional data (documents, ADRs, tickets, chat extracts) with a deterministic FalkorDB graph layer, enabling multi-hop question answering with verifiable citations.

---

## 1. High-Level Architecture Diagram

```text
┌─────────────────────────────────┐
│     MULTIMODAL INGESTION        │
│  PDF, DOCX, Markdown, JSON      │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│    PARSING & PROVENANCE         │
│  PyMuPDF & docx -> Offsets      │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│     FALKORDB KNOWLEDGE GRAPH    │
│  11 Nodes, 13 Edges, Vectors    │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│     AI REASONING LAYER          │
│  Gemini Flash + Cypher Engine   │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│     FASTAPI REST LAYER          │
│  10 Strongly Typed Endpoints    │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│     REACT 18 + @xyflow/react    │
│  Graph Explorer + Verified Chat │
└─────────────────────────────────┘
```

---

## 2. Component Breakdown

1. **Ingestion Engine (`backend/app/ingestion/`)**:
   - Parses PDFs with PyMuPDF, extracting page numbers and character bounding offsets.
   - Extracts semantic sections from DOCX and Markdown documents.
   - Preserves strict chunk provenance via `[:PART_OF]` and `[:NEXT_CHUNK]` relationships.
2. **FalkorDB Knowledge Graph (`backend/app/graph/`)**:
   - Operates as the central source of truth for organizational relationships.
   - Executes parameterized Cypher templates for entity lookup, ownership, blast radius analysis, and decision lineage.
3. **Retrieval & Reasoning Agent (`backend/app/retrieval/`)**:
   - Classifies incoming natural language questions into 6 supported intent categories.
   - Merges graph paths with verbatim chunk evidence.
   - Evaluates freshness, staleness, and contradictions using a 6-factor composite scoring algorithm.
4. **Interactive UI (`frontend/src/`)**:
   - Built on React 18, Vite, Tailwind CSS, and `@xyflow/react`.
   - Features dark mode with custom geometric node styling, live graph metric counters, and a floating Entity Inspector Drawer.
