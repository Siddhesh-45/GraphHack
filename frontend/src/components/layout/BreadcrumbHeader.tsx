import React from 'react';
import { RefreshCw, ExternalLink, Zap, Terminal } from 'lucide-react';
import { HealthResponse } from '../../api/types';
import { HealthBadge } from '../HealthBadge';

interface Props {
  health: HealthResponse | null;
  onRefresh: () => void;
}

export const BreadcrumbHeader: React.FC<Props> = ({ health, onRefresh }) => {
  return (
    <header className="h-14 border-b border-slate-800 bg-slate-950/80 backdrop-blur-md px-6 flex items-center justify-between">
      {/* Breadcrumbs */}
      <div className="flex items-center gap-2 text-xs">
        <span className="text-slate-400 hover:text-slate-200 cursor-pointer">Northstar_Systems</span>
        <span className="text-slate-600">/</span>
        <span className="text-slate-400 hover:text-slate-200 cursor-pointer">Core_Platform</span>
        <span className="text-slate-600">/</span>
        <span className="font-semibold text-slate-100 flex items-center gap-1.5">
          Knowledge Graph
        </span>
        <span className="text-slate-600">·</span>
        <span className="text-slate-400 font-mono text-[11px]">
          FalkorDB Graph · Gemini Flash
        </span>
      </div>

      {/* Action controls */}
      <div className="flex items-center gap-3">
        {/* Reusable HealthBadge */}
        <HealthBadge health={health} onRefresh={onRefresh} />

        {/* Refresh button */}
        <button 
          onClick={onRefresh}
          className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-900 border border-slate-800 transition"
          title="Refresh Graph State"
        >
          <RefreshCw className="w-4 h-4" />
        </button>

        {/* Docs button */}
        <a 
          href="http://localhost:8000/docs" 
          target="_blank" 
          rel="noreferrer"
          className="flex items-center gap-1.5 text-xs font-medium px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700/60 transition"
        >
          <Terminal className="w-3.5 h-3.5 text-cyan-400" />
          <span>API Docs</span>
        </a>
      </div>
    </header>
  );
};
