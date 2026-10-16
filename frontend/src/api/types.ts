export interface HealthResponse {
  status: string;
  version: string;
  timestamp: string;
  environment: string;
  falkordb: {
    connected: boolean;
    host: string;
    port: number;
    graph_name: string;
    total_nodes: number;
  };
}

export interface Citation {
  source_id: string;
  source_title: string;
  source_uri?: string | null;
  chunk_id: string;
  page_number?: number | null;
  excerpt: string;
  timestamp?: string | null;
}

export interface GraphPath {
  start_node: string;
  end_node: string;
  relationships: string[];
  nodes: Array<{ id: string; label: string }>;
  description: string;
}

export interface ChatResponse {
  answer: string;
  citations: Citation[];
  graph_paths: GraphPath[];
  confidence_label: "high" | "medium" | "low" | "insufficient_evidence";
  warnings: string[];
  follow_up_questions: string[];
}

export interface EntityInspectorData {
  id: string;
  name: string;
  category: "Person" | "Team" | "Service" | "Decision" | "Incident" | "Concept";
  description: string;
  properties: {
    created_at: string;
    updated_at: string;
    last_verified_at: string;
    freshness_score: number;
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
    relationship_label: string;
    is_inferred: boolean;
    confidence?: number;
  }>;
}
