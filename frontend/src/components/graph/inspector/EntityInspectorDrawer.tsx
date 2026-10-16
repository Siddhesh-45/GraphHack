import React from 'react';
import { EntityInspectorData } from '../../../api/types';
import { X, ExternalLink, ShieldCheck, Clock, GitFork, ArrowUpRight } from 'lucide-react';

interface Props {
  entity: EntityInspectorData | null;
  onClose: () => void;
  onSelectNeighbor: (entityId: string) => void;
}

export const EntityInspectorDrawer: React.FC<Props> = ({ entity, onClose, onSelectNeighbor }) => {
  if (!entity) return null;

  return (
    <div className="absolute right-6 top-6 w-96 max-h-[82vh] overflow-y-auto bg-slate-900/95 backdrop-blur-xl border border-slate-700/60 rounded-2xl shadow-2xl p-6 text-white z-30 transition-all duration-300 select-none">
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
      <p className="mt-4 text-xs leading-relaxed text-slate-300 bg-slate-950/60 p-3.5 rounded-xl border border-slate-800/80">
        {entity.description || "The Payment Gateway Service manages Northstar's primary transaction pipeline and active ledger balance."}
      </p>

      {/* Properties Section */}
      <div className="mt-5">
        <h4 className="text-[11px] font-mono uppercase tracking-wider text-slate-400 mb-2.5 font-semibold">Properties</h4>
        <div className="grid grid-cols-2 gap-2 text-xs">
          <div className="bg-slate-950/40 p-2.5 rounded-lg border border-slate-800">
            <span className="text-slate-500 text-[10px] block font-mono">Created</span>
            <span className="font-medium text-slate-200">{entity.properties.created_at || 'Jan 15, 2025'}</span>
          </div>
          <div className="bg-slate-950/40 p-2.5 rounded-lg border border-slate-800">
            <span className="text-slate-500 text-[10px] block font-mono">Last Verified</span>
            <span className="font-medium text-slate-200">{entity.properties.last_verified_at || '2 days ago'}</span>
          </div>
          <div className="bg-slate-950/40 p-2.5 rounded-lg border border-slate-800">
            <span className="text-slate-500 text-[10px] block font-mono">Connections</span>
            <span className="font-medium text-cyan-400">{entity.properties.connections_count || 14}</span>
          </div>
          <div className="bg-slate-950/40 p-2.5 rounded-lg border border-slate-800">
            <span className="text-slate-500 text-[10px] block font-mono">Freshness (6-Factor)</span>
            <span className={`font-semibold ${entity.properties.freshness_score >= 0.8 ? 'text-emerald-400' : 'text-amber-400'}`}>
              {((entity.properties.freshness_score || 0.94) * 100).toFixed(0)}% (Active)
            </span>
          </div>
        </div>
      </div>

      {/* Connected To Section */}
      <div className="mt-5">
        <h4 className="text-[11px] font-mono uppercase tracking-wider text-slate-400 mb-2.5 font-semibold">
          Connected To ({entity.connected_to.length || 5})
        </h4>
        <div className="space-y-2">
          {(entity.connected_to.length > 0 ? entity.connected_to : [
            { target_id: 'sarah-chen', target_name: 'Sarah Chen (Staff Eng)', target_category: 'Person', relationship_label: 'OWNS', is_inferred: false },
            { target_id: 'auth-service', target_name: 'Auth Service (Tier 1)', target_category: 'Service', relationship_label: 'DEPENDS_ON', is_inferred: false },
            { target_id: 'billing-engine', target_name: 'Billing Engine (Tier 2)', target_category: 'Service', relationship_label: 'DEPENDS_ON', is_inferred: false },
            { target_id: 'adr-004', target_name: 'ADR-004 (CockroachDB)', target_category: 'Decision', relationship_label: 'DECIDED_IN', is_inferred: false },
            { target_id: 'inc-101', target_name: 'INC-101 Outage Resolution', target_category: 'Incident', relationship_label: 'AFFECTED', is_inferred: false },
          ]).map((link, idx) => (
            <div 
              key={idx}
              onClick={() => onSelectNeighbor(link.target_id)}
              className="flex items-center justify-between p-2.5 rounded-xl bg-slate-950/50 hover:bg-slate-800/80 border border-slate-800/80 transition cursor-pointer group"
            >
              <div className="flex items-center gap-2.5 min-w-0">
                <span className="w-2 h-2 rounded-full bg-cyan-400 shrink-0 group-hover:scale-125 transition" />
                <span className="text-xs font-medium text-slate-200 truncate group-hover:text-cyan-300">
                  {link.target_name}
                </span>
              </div>
              <span className="text-[10px] font-mono text-cyan-400/90 bg-cyan-950/40 px-2 py-0.5 rounded border border-cyan-800/40 shrink-0">
                {link.relationship_label.toLowerCase().replace('_', ' ')}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
