import React from 'react';
import { HealthResponse } from '../api/types';
import { Database, Server, CheckCircle2, AlertCircle } from 'lucide-react';

interface Props {
  health: HealthResponse | null;
  onRefresh?: () => void;
}

export const HealthBadge: React.FC<Props> = ({ health }) => {
  const isHealthy = health?.status === 'healthy';
  const falkorConnected = health?.falkordb?.connected ?? false;
  const nodeCount = health?.falkordb?.total_nodes ?? 0;

  return (
    <div className="flex items-center gap-2">
      {/* Backend & DB Health Pill */}
      <div 
        className={`flex items-center gap-2 px-3 py-1 rounded-full text-xs font-mono border transition-all ${
          isHealthy
            ? 'bg-emerald-950/40 text-emerald-300 border-emerald-500/40 shadow-sm shadow-emerald-900/20'
            : 'bg-amber-950/40 text-amber-300 border-amber-500/40'
        }`}
        title={`Backend: ${health?.environment || 'unknown'} | FalkorDB: ${falkorConnected ? 'Connected' : 'Disconnected'} (${nodeCount} nodes)`}
      >
        <span className="relative flex h-2 w-2">
          {isHealthy && (
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
          )}
          <span className={`relative inline-flex rounded-full h-2 w-2 ${isHealthy ? 'bg-emerald-400' : 'bg-amber-400'}`} />
        </span>

        <span className="font-medium">
          {isHealthy ? 'FalkorDB Online' : 'FalkorDB Connecting'}
        </span>

        {falkorConnected && (
          <span className="text-[10px] bg-emerald-900/60 text-emerald-200 px-1.5 py-0.2 rounded border border-emerald-700/50">
            {nodeCount} nodes
          </span>
        )}
      </div>
    </div>
  );
};
