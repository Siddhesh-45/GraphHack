import React, { useState, useMemo } from 'react';
import { 
  ReactFlow, 
  MiniMap, 
  Controls, 
  Background, 
  useNodesState, 
  useEdgesState,
  Node,
  Edge,
  BackgroundVariant
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { GraphSearchBar } from './GraphSearchBar';
import { GraphLegendBar } from './GraphLegendBar';
import { EntityInspectorDrawer } from './inspector/EntityInspectorDrawer';
import { EntityInspectorData } from '../../api/types';

// Initial synthetic nodes for demonstration
const initialNodes: Node[] = [
  {
    id: 'payment-gateway',
    position: { x: 420, y: 220 },
    data: { label: 'Payment Gateway (Tier 1)', category: 'Service', color: '#ec4899' },
    style: { background: '#1e1b4b', border: '1px solid #818cf8', borderRadius: '12px', color: '#fff', padding: '12px', width: 180 }
  },
  {
    id: 'sarah-chen',
    position: { x: 140, y: 120 },
    data: { label: 'Sarah Chen (Staff Eng)', category: 'Person', color: '#38bdf8' },
    style: { background: '#082f49', border: '1px solid #38bdf8', borderRadius: '9999px', color: '#fff', padding: '10px 16px', textAlign: 'center' }
  },
  {
    id: 'core-payments',
    position: { x: 120, y: 320 },
    data: { label: 'Core Payments Team', category: 'Team', color: '#f59e0b' },
    style: { background: '#451a03', border: '1px solid #f59e0b', borderRadius: '10px', color: '#fff', padding: '12px', width: 170 }
  },
  {
    id: 'auth-service',
    position: { x: 680, y: 100 },
    data: { label: 'Auth Service (Tier 1)', category: 'Service', color: '#ec4899' },
    style: { background: '#1e1b4b', border: '1px solid #ec4899', borderRadius: '12px', color: '#fff', padding: '12px', width: 170 }
  },
  {
    id: 'billing-engine',
    position: { x: 700, y: 340 },
    data: { label: 'Billing Engine (Tier 2)', category: 'Service', color: '#ec4899' },
    style: { background: '#1e1b4b', border: '1px solid #ec4899', borderRadius: '12px', color: '#fff', padding: '12px', width: 180 }
  },
  {
    id: 'adr-001',
    position: { x: 420, y: 440 },
    data: { label: 'ADR-001: PostgreSQL', category: 'Decision', color: '#ef4444' },
    style: { background: '#450a0a', border: '1px solid #ef4444', borderRadius: '8px', color: '#fff', padding: '10px', width: 170 }
  },
  {
    id: 'adr-004',
    position: { x: 420, y: 50 },
    data: { label: 'ADR-004: CockroachDB', category: 'Decision', color: '#10b981' },
    style: { background: '#064e3b', border: '1px solid #10b981', borderRadius: '8px', color: '#fff', padding: '10px', width: 180 }
  },
  {
    id: 'inc-101',
    position: { x: 200, y: 460 },
    data: { label: 'INC-101: Pool Exhaustion', category: 'Incident', color: '#f97316' },
    style: { background: '#431407', border: '1px solid #f97316', borderRadius: '8px', color: '#fff', padding: '8px 12px', width: 160 }
  }
];

const initialEdges: Edge[] = [
  { id: 'e-sarah-pay', source: 'sarah-chen', target: 'payment-gateway', label: 'OWNS', animated: true, style: { stroke: '#38bdf8', strokeWidth: 2 } },
  { id: 'e-team-pay', source: 'core-payments', target: 'payment-gateway', label: 'SUPPORTED_BY', style: { stroke: '#f59e0b' } },
  { id: 'e-pay-auth', source: 'payment-gateway', target: 'auth-service', label: 'DEPENDS_ON', animated: true, style: { stroke: '#ec4899', strokeWidth: 2 } },
  { id: 'e-pay-bill', source: 'payment-gateway', target: 'billing-engine', label: 'DEPENDS_ON', style: { stroke: '#ec4899' } },
  { id: 'e-adr4-adr1', source: 'adr-004', target: 'adr-001', label: 'SUPERSEDES', animated: true, style: { stroke: '#10b981', strokeWidth: 2 } },
  { id: 'e-pay-adr1', source: 'adr-001', target: 'payment-gateway', label: 'DECIDED_IN', style: { stroke: '#818cf8' } },
  { id: 'e-inc-pay', source: 'inc-101', target: 'payment-gateway', label: 'AFFECTED', style: { stroke: '#f97316' } },
];

export const GraphCanvas: React.FC = () => {
  const [nodes, , onNodesChange] = useNodesState(initialNodes);
  const [edges, , onEdgesChange] = useEdgesState(initialEdges);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedEntity, setSelectedEntity] = useState<EntityInspectorData | null>({
    id: 'payment-gateway',
    name: 'Payment Gateway (Tier 1)',
    category: 'Service',
    description: "Northstar's primary transaction pipeline and active ledger balance. Managed by Sarah Chen.",
    properties: {
      created_at: 'Jan 15, 2025',
      updated_at: 'Aug 20, 2026',
      last_verified_at: '2 days ago',
      freshness_score: 0.94,
      connections_count: 6,
      staleness_status: 'ACTIVE',
      repo_url: 'github.com/northstar/payment-gateway',
      tier: 'Tier 1'
    },
    connected_to: [
      { target_id: 'sarah-chen', target_name: 'Sarah Chen (Staff Eng)', target_category: 'Person', relationship_label: 'OWNS', is_inferred: false },
      { target_id: 'core-payments', target_name: 'Core Payments Team', target_category: 'Team', relationship_label: 'SUPPORTED_BY', is_inferred: false },
      { target_id: 'auth-service', target_name: 'Auth Service (Tier 1)', target_category: 'Service', relationship_label: 'DEPENDS_ON', is_inferred: false },
      { target_id: 'billing-engine', target_name: 'Billing Engine (Tier 2)', target_category: 'Service', relationship_label: 'DEPENDS_ON', is_inferred: false },
      { target_id: 'adr-004', target_name: 'ADR-004 (CockroachDB)', target_category: 'Decision', relationship_label: 'DECIDED_IN', is_inferred: false },
    ]
  });

  const filteredNodes = useMemo(() => {
    if (!searchQuery.trim()) return nodes;
    return nodes.filter(n => 
      (n.data.label as string).toLowerCase().includes(searchQuery.toLowerCase()) ||
      (n.data.category as string).toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [nodes, searchQuery]);

  const onNodeClick = (_: React.MouseEvent, node: Node) => {
    setSelectedEntity({
      id: node.id,
      name: node.data.label as string,
      category: (node.data.category as any) || 'Concept',
      description: `Entity representing ${node.data.label} in the FalkorDB enterprise knowledge graph.`,
      properties: {
        created_at: 'Jan 15, 2025',
        updated_at: 'Aug 20, 2026',
        last_verified_at: 'Just now',
        freshness_score: 0.92,
        connections_count: edges.filter(e => e.source === node.id || e.target === node.id).length,
        staleness_status: 'ACTIVE',
      },
      connected_to: edges
        .filter(e => e.source === node.id || e.target === node.id)
        .map(e => {
          const isSource = e.source === node.id;
          const otherId = isSource ? e.target : e.source;
          const otherNode = nodes.find(n => n.id === otherId);
          return {
            target_id: otherId,
            target_name: (otherNode?.data.label as string) || otherId,
            target_category: (otherNode?.data.category as string) || 'Concept',
            relationship_label: (e.label as string) || 'CONNECTED_TO',
            is_inferred: false,
          };
        })
    });
  };

  return (
    <div className="relative w-full h-full bg-slate-950 overflow-hidden">
      {/* Search & Density Bar */}
      <GraphSearchBar 
        entityCount={nodes.length}
        linkCount={edges.length}
        factCount={nodes.length + edges.length}
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
      />

      {/* Main React Flow Canvas */}
      <ReactFlow
        nodes={filteredNodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={onNodeClick}
        fitView
        className="bg-slate-950"
      >
        <Background variant={BackgroundVariant.Dots} color="#334155" gap={20} size={1} />
        <Controls className="bg-slate-900 border-slate-700 text-white rounded-xl overflow-hidden shadow-2xl" />
        <MiniMap 
          nodeColor={(n) => (n.data?.color as string) || '#38bdf8'} 
          className="bg-slate-900/90 border border-slate-800 rounded-xl overflow-hidden" 
        />
      </ReactFlow>

      {/* Geometric Category Legend Bar */}
      <GraphLegendBar />

      {/* Right Floating Entity Inspector Drawer */}
      <EntityInspectorDrawer 
        entity={selectedEntity} 
        onClose={() => setSelectedEntity(null)} 
        onSelectNeighbor={(id) => {
          const neighbor = nodes.find(n => n.id === id);
          if (neighbor) onNodeClick({} as any, neighbor);
        }}
      />
    </div>
  );
};
