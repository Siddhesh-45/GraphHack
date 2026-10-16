# Module 03 — Source Ingestion, Provenance Chunking, and Graph Construction

## Goal
Build an ingestion engine that converts unstructured enterprise documents (PDF, DOCX, Markdown, plain text, and structured JSON fixtures) into an interconnected FalkorDB knowledge graph while preserving strict chunk-level provenance.

---

## 1. Ingestion Pipeline Architecture

```mermaid
flowchart TD
    A[Upload Source File / Document] --> B{Detect File Type}
    B -->|PDF| C1[PyMuPDF fitz Extractor]
    B -->|DOCX| C2[python-docx Parser]
    B -->|Markdown / Text| C3[Markdown Structure Parser]
    B -->|JSON| C4[Structured Fixture Parser]
    
    C1 & C2 & C3 & C4 --> D[Text Normalization & Offset Tracking]
    D --> E[Semantic Chunker: 600 tokens, 100 overlap]
    
    E --> F[Create Document & Chunk Nodes in FalkorDB]
    F -->|Link Adjacent| G[[:NEXT_CHUNK] & [:PART_OF] Edges]
    
    E --> H[Gemini Flash LLM Extraction Prompt]
    H --> I[Structured Pydantic Extraction Payload]
    
    I --> J[Entity Resolution & Deduplication]
    J --> K[FalkorDB MERGE Entities & Relations]
    K --> L[Create [:MENTIONED_IN] Provenance Edges to Chunks]
    
    L --> M[Update Ingestion Status: COMPLETED]
```

---

## 2. Multi-Format Parsers

### A. PDF Extraction (PyMuPDF `fitz`)
Preserves exact page numbers, text blocks, and character offsets:
```python
import fitz  # PyMuPDF
from typing import List, Dict, Any

def parse_pdf(file_bytes: bytes, filename: str) -> List[Dict[str, Any]]:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    pages_data = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        if text.strip():
            pages_data.append({
                "page_number": page_num + 1,
                "text": text,
                "char_length": len(text)
            })
    return pages_data
```

### B. DOCX Extraction (`python-docx`)
Extracts headings, paragraph hierarchies, and table contents:
```python
import docx
import io

def parse_docx(file_bytes: bytes) -> List[Dict[str, Any]]:
    doc = docx.Document(io.BytesIO(file_bytes))
    sections = []
    current_heading = "General"
    current_text = []

    for para in doc.paragraphs:
        if para.style.name.startswith("Heading"):
            if current_text:
                sections.append({"heading": current_heading, "text": "\n".join(current_text)})
                current_text = []
            current_heading = para.text
        elif para.text.strip():
            current_text.append(para.text)

    if current_text:
        sections.append({"heading": current_heading, "text": "\n".join(current_text)})
    return sections
```

### C. Structured JSON Fixture Extraction
For synthetic Slack threads, Jira tickets, and incident reports:
```python
import json

def parse_synthetic_fixture(file_bytes: bytes) -> dict:
    data = json.loads(file_bytes.decode("utf-8"))
    # Validates against SyntheticCorpus schema (tickets, chats, adrs)
    return data
```

---

## 3. Semantic Chunking & Provenance Metadata

Documents must be divided into bounded chunks with overlap to retain semantic boundaries. Each chunk receives a deterministic UUIDv5 based on `source_id` and `chunk_index`.

```python
from pydantic import BaseModel
from typing import Optional
import hashlib
import uuid

class ChunkMetadata(BaseModel):
    chunk_id: str
    source_id: str
    chunk_index: int
    text: str
    page_number: Optional[int] = None
    char_offset_start: int
    char_offset_end: int
    section_heading: Optional[str] = None

def generate_chunk_id(source_id: str, chunk_index: int) -> str:
    namespace = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
    return str(uuid.uuid5(namespace, f"{source_id}:{chunk_index}"))
```

---

## 4. LLM Structured Entity & Relationship Extraction

Use Gemini Flash with structured schema output (`response_schema=IngestionExtractionResult`) to extract facts strictly conforming to the allowlisted schema.

### Pydantic Extraction Schema
```python
from pydantic import BaseModel, Field
from typing import List, Literal

class ExtractedEntity(BaseModel):
    name: str = Field(..., description="Canonical entity name (e.g. 'Sarah Chen', 'Payment Service')")
    label: Literal["Person", "Team", "Service", "Project", "Decision", "Incident", "Skill"]
    properties: dict = Field(default_factory=dict, description="Attributes like role, tier, status, date")

class ExtractedRelationship(BaseModel):
    source_name: str
    source_label: str
    target_name: str
    target_label: str
    relation_type: Literal[
        "OWNS", "MEMBER_OF", "WORKED_ON", "DEPENDS_ON", 
        "DECIDED_IN", "RESOLVED", "SUPERSEDES", "SUPPORTED_BY"
    ]
    properties: dict = Field(default_factory=dict)
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    is_inferred: bool = Field(default=False)

class IngestionExtractionResult(BaseModel):
    entities: List[ExtractedEntity]
    relationships: List[ExtractedRelationship]
```

### Extraction System Prompt
```text
You are an expert enterprise knowledge graph engineer. Extract concrete organizational facts from this document passage.
Strict Rules:
1. Only extract entities with labels: Person, Team, Service, Project, Decision, Incident, Skill.
2. Only extract relationships with types: OWNS, MEMBER_OF, WORKED_ON, DEPENDS_ON, DECIDED_IN, RESOLVED, SUPERSEDES, SUPPORTED_BY.
3. Distinguish explicit ownership (OWNS) from general mentions or historical work (WORKED_ON).
4. Do not invent entities or relationships not directly stated in the text.
5. If a decision replaces an earlier decision, create a SUPERSEDES relationship from the newer decision to the older one.
```

---

## 5. Entity Resolution & Deduplication Algorithm

To prevent duplicated nodes (e.g., "Sarah Chen" vs "sarah-chen" vs "Sarah C."):
1. **Canonical Slug Normalization**: Transform names to lowercase alphanumeric slugs (`sarah-chen`).
2. **Alias Lookup Table**: Map known email addresses and usernames to canonical IDs.
3. **Idempotent Cypher Upsert**: Use `MERGE (n:Person {id: $canonical_id})` to ensure subsequent documents update properties rather than creating duplicate nodes.
4. **Provenance Attachment**:
```cypher
MATCH (e:Person {id: $canonical_id})
MATCH (c:Chunk {id: $chunk_id})
MERGE (e)-[:MENTIONED_IN]->(c)
```

---

## 6. Source Ingestion API Endpoints

### 1. `POST /api/sources/upload`
- Accepts `multipart/form-data` with `.pdf`, `.docx`, `.md`, `.txt`, `.json` files up to 25MB.
- Calculates SHA-256 checksum immediately.
- If checksum exists and document is unchanged, returns cached summary.
- Spawns asynchronous ingestion task.

### 2. `GET /api/sources`
Returns all ingested sources with status summary:
```json
[
  {
    "source_id": "doc-northstar-payment-adr-001",
    "title": "ADR 001 - PostgreSQL Selection for Payment Ledger",
    "source_type": "markdown",
    "status": "COMPLETED",
    "chunk_count": 8,
    "entities_extracted": 14,
    "created_at": "2026-09-15T10:30:00Z"
  }
]
```

### 3. `GET /api/sources/{source_id}`
Returns source metadata, associated chunks with character offsets, and extracted graph entities.

---

## 7. Acceptance Criteria
- [x] Ingests sample Markdown, plain text, PDF, DOCX, and JSON files without crash.
- [x] Every extracted entity is linked to at least one supporting `Chunk` node via `[:MENTIONED_IN]`.
- [x] Re-uploading the same file produces identical node IDs and does not duplicate graph nodes.
- [x] File types outside the allowlist are rejected with HTTP 400 and a descriptive error message.
- [x] Chunks contain valid sequential `[:NEXT_CHUNK]` links forming an ordered reading chain.
