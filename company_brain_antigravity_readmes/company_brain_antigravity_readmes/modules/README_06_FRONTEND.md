# Module 06 — Frontend UI and Interactive Knowledge Graph Explorer

## Goal
Build an enterprise-grade, high-performance React application using TypeScript, Tailwind CSS, and `@xyflow/react`, inspired by industry-leading state-of-the-art knowledge graph explorers (e.g., SharedMemoryAI). The UI delivers a dark-mode glassmorphic workspace featuring a multi-section sidebar, canvas control header with live graph metrics, custom geometric nodes, and a rich slide-over **Entity Inspector Drawer** displaying properties, freshness decay, and categorized `CONNECTED TO` relationship lists.

---

## 1. Reference Architecture & Layout Blueprint

The application interface follows a premier enterprise design system with four distinct zones:

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ TOP BREADCRUMB BAR: Northstar Systems / Core Platform / Knowledge Graph  │  83 Items · Gemini Flash │ [DOCS] [⟳] [↗] │
├─────────────────┬────────────────────────────────────────────────────────────────────────────┬───────────────┤
│ SIDEBAR         │ GRAPH EXPLORER CANVAS (@xyflow/react)                                      │ ENTITY        │
│                 │                                                                            │ INSPECTOR     │
│ [ANALYTICS]     │ [● 464 Entities] [● 649 Links] [● 649 Facts]  [Q Search Graph...       ]   │ DRAWER        │
│ • Overview      │ ────────────────────────────────────────────────────────────────────────── │               │
│ • Knowledge     │                                                                            │ [Node Title]  │
│ • Brain Chat    │                (Person) ──OWNS──► (Service)                                │ [Category]    │
│                 │                   │                  │                                     │               │
│ [DATA]          │                   │             DEPENDS_ON                                 │ Description   │
│ • Documents     │               MEMBER_OF              │                                     │               │
│ • Instructions  │                   ▼                  ▼                                     │ PROPERTIES    │
│ • Knowledge     │                (Team) ◄──OWNS─── (Service)                                 │ • Created     │
│   Graph (Active)│                                      │                                     │ • Updated     │
│ • Timeline      │                                 DECIDED_IN                                 │ • Freshness   │
│ • Activity      │                                      ▼                                     │ • Connections │
│                 │                                  (Decision)                                │               │
│ [DEVELOPER]     │                                      │                                     │ CONNECTED TO  │
│ • API Keys      │                                  SUPERSEDES                                │ • Node A (rel)│
│ • Setup         │                                      ▼                                     │ • Node B (rel)│
│ • Agents        │                                  (Decision)                                │ • Node C (rel)│
│                 │ ────────────────────────────────────────────────────────────────────────── │               │
│ [ACCOUNT]       │ LEGEND:  ○ Concept  ○ Person  ⬡ Team/Process  △ Service/Tool  ◇ Decision   │ [Close ✕]     │
└─────────────────┴────────────────────────────────────────────────────────────────────────────┴───────────────┘
```

---

## 2. Component Hierarchy & File Structure

```text
frontend/src/
├── App.tsx                               # Master shell with routing & layout state
├── index.css                             # Tailwind directives, theme variables, glassmorphism
├── api/
│   ├── client.ts                         # Strongly-typed Axios / Fetch client
│   └── types.ts                          # TypeScript interfaces matching backend models
├── components/
│   ├── layout/
│   │   ├── NavigationSidebar.tsx         # Grouped sidebar (Analytics, Data, Developer, Account)
│   │   ├── BreadcrumbHeader.tsx          # Tenant / Graph path, model badge, action buttons
│   │   └── TopStatusBar.tsx              # Live FalkorDB connectivity badge
│   ├── graph/
│   │   ├── GraphCanvas.tsx               # Main @xyflow/react interactive canvas wrapper
│   │   ├── GraphSearchBar.tsx            # Live search input with entity/link/fact counters
│   │   ├── GraphLegendBar.tsx            # Bottom category toggle pills with geometric icons
│   │   ├── nodes/                        # Custom React Flow geometric node cards
│   │   │   ├── PersonNode.tsx            # Blue circle: Employee name, role, team badge
│   │   │   ├── ServiceNode.tsx           # Pink/Emerald triangle: Service name, tier, repo
│   │   │   ├── TeamNode.tsx              # Yellow/Orange hexagon: Team name, department
│   │   │   ├── DecisionNode.tsx          # Violet diamond: ADR title, status (Active/Superseded)
│   │   │   ├── IncidentNode.tsx          # Red diamond: Severity tag, resolution status
│   │   │   └── ChunkNode.tsx             # Dark rounded card: Text snippet with offset tag
│   │   ├── edges/
│   │   │   ├── TypedGraphEdge.tsx        # Styled edges with animated dashed/solid lines & labels
│   │   └── inspector/
│   │       ├── EntityInspectorDrawer.tsx # Floating glassmorphic right inspector card
│   │       ├── EntityPropertiesList.tsx  # Created, Updated, 6-Factor Freshness, Connections
│   │       └── ConnectedToList.tsx       # Interactive neighbor links with relationship badges
│   ├── chat/
│   │   ├── ChatContainer.tsx             # Message history stream with citation pills
│   │   ├── CitationDrawer.tsx            # Slide-over panel showing verbatim chunk excerpts
│   │   └── EvidencePanel.tsx             # "Why this answer?" graph path visualizer
│   ├── timeline/
│   │   └── DecisionTimeline.tsx          # Chronological ADR timeline with supersession links
│   └── sources/
│       ├── SourceUploader.tsx            # Drag-and-drop file upload zone
│       └── SourceListTable.tsx           # Ingestion status, chunk count, checksum
```

---

## 3. Knowledge Graph Canvas & Controls

### Live Metric Counters & Search Bar (`components/graph/GraphSearchBar.tsx`)
Displays instantaneous graph density indicators matching the reference UI:
- `● {stats.total_entities} Entities`
- `● {stats.total_links} Links`
- `● {stats.total_facts} Facts`
- Real-time entity filter input with debounce.

### Bottom Geometric Legend Bar (`components/graph/GraphLegendBar.tsx`)
Color-coded category pills matching the reference:
- `○ Concept / Skill`: Cyan (`#06b6d4`)
- `○ Person`: Blue (`#3b82f6`)
- `⬡ Team / Process`: Yellow/Amber (`#f59e0b`)
- `△ Service / Tool`: Pink/Purple (`#ec4899`)
- `◇ Decision / Event`: Red/Orange (`#ef4444`)
- `○ Document / Chunk`: Slate (`#64748b`)

---

## 4. Entity Inspector Drawer (`components/graph/inspector/`)

When any node is clicked on the canvas, the **Entity Inspector Drawer** opens as a floating glassmorphism card on the right side of the canvas.

### Inspector Layout & TypeScript Interface

```typescript
export interface EntityInspectorData {
  id: string;
  name: string;
  category: "Person" | "Team" | "Service" | "Decision" | "Incident" | "Concept";
  description: string;
  properties: {
    created_at: string;
    updated_at: string;
    last_verified_at: string;
    freshness_score: number;      // 0.0 to 1.0 (6-factor composite decay score)
    connections_count: number;
    staleness_status: "ACTIVE" | "STALE_UNVERIFIED" | "SUPERSEDED";
    repo_url?: string;
    tier?: string;
    author?: string;
  };
  connected_to: Array<{
    target_id: string;
    target_name: string;
    target_category: string;
    relationship_label: string;  // e.g., "OWNS", "DEPENDS_ON", "SUPERSEDES", "RESOLVED"
    is_inferred: boolean;
    confidence?: number;
  }>;
}
```

### Visual Inspector Component (`EntityInspectorDrawer.tsx`)
```tsx
import React from 'react';
import { EntityInspectorData } from '../../api/types';
import { X, ExternalLink, ShieldCheck, Clock, GitFork } from 'lucide-react';

interface Props {
  entity: EntityInspectorData | null;
  onClose: () => void;
  onSelectNeighbor: (entityId: string) => void;
}

export const EntityInspectorDrawer: React.FC<Props> = ({ entity, onClose, onSelectNeighbor }) => {
  if (!entity) return null;

  return (
    <div className="absolute right-6 top-6 w-96 max-h-[85vh] overflow-y-auto bg-slate-900/90 backdrop-blur-xl border border-slate-700/60 rounded-2xl shadow-2xl p-6 text-white z-30 transition-all duration-300">
      {/* Header */}
      <div className="flex items-start justify-between gap-4">
        <div>
          <span className="inline-block px-2.5 py-0.5 rounded-full text-xs font-mono font-medium tracking-wide bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 mb-2">
            {entity.category}
          </span>
          <h3 className="text-xl font-bold tracking-tight text-slate-100">{entity.name}</h3>
        </div>
        <button onClick={onClose} className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition">
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* Description */}
      <p className="mt-4 text-sm leading-relaxed text-slate-300 bg-slate-950/40 p-3.5 rounded-xl border border-slate-800/80">
        {entity.description || "No formal description recorded."}
      </p>

      {/* Properties Section */}
      <div className="mt-6">
        <h4 className="text-xs font-mono uppercase tracking-wider text-slate-400 mb-3">Properties</h4>
        <div className="grid grid-cols-2 gap-2 text-xs">
          <div className="bg-slate-950/30 p-2.5 rounded-lg border border-slate-800">
            <span className="text-slate-500 block">Created</span>
            <span className="font-medium text-slate-200">{entity.properties.created_at}</span>
          </div>
          <div className="bg-slate-950/30 p-2.5 rounded-lg border border-slate-800">
            <span className="text-slate-500 block">Updated</span>
            <span className="font-medium text-slate-200">{entity.properties.updated_at}</span>
          </div>
          <div className="bg-slate-950/30 p-2.5 rounded-lg border border-slate-800">
            <span className="text-slate-500 block">Connections</span>
            <span className="font-medium text-cyan-400">{entity.properties.connections_count}</span>
          </div>
          <div className="bg-slate-950/30 p-2.5 rounded-lg border border-slate-800">
            <span className="text-slate-500 block">Freshness Score</span>
            <span className={`font-semibold ${entity.properties.freshness_score >= 0.8 ? 'text-emerald-400' : 'text-amber-400'}`}>
              {(entity.properties.freshness_score * 100).toFixed(0)}%
            </span>
          </div>
        </div>
      </div>

      {/* Connected To Section */}
      <div className="mt-6">
        <h4 className="text-xs font-mono uppercase tracking-wider text-slate-400 mb-3">
          Connected To ({entity.connected_to.length})
        </h4>
        <div className="space-y-2">
          {entity.connected_to.map((link, idx) => (
            <div 
              key={idx}
              onClick={() => onSelectNeighbor(link.target_id)}
              className="flex items-center justify-between p-2.5 rounded-xl bg-slate-950/40 hover:bg-slate-800/60 border border-slate-800/80 transition cursor-pointer group"
            >
              <div className="flex items-center gap-2.5 min-w-0">
                <span className="w-2 h-2 rounded-full bg-cyan-400 shrink-0 group-hover:scale-125 transition" />
                <span className="text-xs font-medium text-slate-200 truncate group-hover:text-cyan-300">
                  {link.target_name}
                </span>
              </div>
              <span className="text-[11px] font-mono text-slate-400 bg-slate-900 px-2 py-0.5 rounded border border-slate-700/50 shrink-0">
                {link.relationship_label.toLowerCase().replace('_', ' ')}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
```

---

## 5. Navigation Sidebar Grouping

The sidebar provides structured enterprise routing across 4 functional tiers:

1. **ANALYTICS**:
   - `Overview`: Global dashboard with node growth, graph health, and recent queries.
   - `Project Knowledge`: Ingested repositories, systems, and architectural domains.
   - `Memory Chat`: Verified multi-hop chat assistant with inline citations and "Why this answer?" panel.
2. **DATA**:
   - `Documents`: Multi-format source manager (PDF, DOCX, MD, JSON).
   - `Instructions`: Standard operating procedures and organizational runbooks.
   - `Knowledge Graph`: Interactive `@xyflow/react` graph canvas with search and inspector.
   - `Timeline`: Chronological decision history and supersession trees.
   - `Activity`: Audit trail of ingestion runs and graph mutations.
3. **DEVELOPER**:
   - `API Keys`: FalkorDB and Gemini Flash credentials.
   - `Setup`: One-command Docker Compose setup and environment checks.
   - `Agents`: Model Context Protocol (MCP) agent configuration.
   - `Integrations`: Slack, Jira, GitHub, and custom webhooks.
   - `Usage`: Token metrics, FalkorDB memory consumption, and query latencies.
4. **ACCOUNT**:
   - Active user profile, role badge (`Enterprise Plan`), and tenant switcher.

---

## 6. Acceptance Criteria
- [x] Layout features the multi-tier navigation sidebar, top breadcrumb bar, and graph canvas.
- [x] Top control bar shows live counters for Entities, Links, and Facts with a real-time search filter.
- [x] Canvas supports geometric node cards with category-specific glowing colors and icons.
- [x] Clicking any node opens the floating Entity Inspector Drawer displaying metadata, properties, 6-factor freshness score, and categorized `CONNECTED TO` links.
- [x] Clicking a neighbor node in the `CONNECTED TO` list smoothly pans and centers the graph canvas on that neighbor.
