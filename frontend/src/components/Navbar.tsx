import React from 'react';
import { HealthBadge } from './HealthBadge';
import { HealthResponse } from '../api/types';
import { RefreshCw, Terminal, Network, MessageSquare, Files, GitFork, AlertOctagon } from 'lucide-react';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  health: HealthResponse | null;
  onRefresh: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  activeTab,
  setActiveTab,
  health,
  onRefresh,
}) => {
  const tabs = [
    { id: 'graph', label: 'Graph Explorer', icon: Network },
    { id: 'chat', label: 'Brain Chat', icon: MessageSquare },
    { id: 'sources', label: 'Sources', icon: Files },
    { id: 'decisions', label: 'Decisions', icon: GitFork },
    { id: 'impact', label: 'Impact', icon: AlertOctagon },
  ];

  return (
    <header className="h-16 border-b border-slate-800 bg-slate-950/90 backdrop-blur-md px-6 flex items-center justify-between z-20">
      {/* Brand & Track */}
      <div className="flex items-center gap-6">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-600 to-indigo-600 flex items-center justify-center shadow-lg shadow-cyan-600/20 border border-cyan-400/30">
            <Network className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-sm tracking-tight text-white">Company Brain</span>
              <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-cyan-950/80 text-cyan-400 border border-cyan-800/50">
                v1.0.0
              </span>
            </div>
            <span className="text-[11px] text-slate-400 block -mt-0.5 font-mono">
              FalkorDB Graph Hacks · Track 03
            </span>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="hidden md:flex items-center gap-1 bg-slate-900/80 p-1 rounded-xl border border-slate-800/80">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                  isActive
                    ? 'bg-cyan-600 text-white shadow-md shadow-cyan-600/30 font-semibold'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Right Controls: Health Pill, Refresh, Docs */}
      <div className="flex items-center gap-3">
        <HealthBadge health={health} onRefresh={onRefresh} />

        <button
          onClick={onRefresh}
          className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-900 border border-slate-800 transition"
          title="Refresh System Health"
        >
          <RefreshCw className="w-4 h-4" />
        </button>

        <a
          href="http://localhost:8000/docs"
          target="_blank"
          rel="noreferrer"
          className="flex items-center gap-1.5 text-xs font-medium px-3 py-2 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700/60 transition shadow-sm"
        >
          <Terminal className="w-3.5 h-3.5 text-cyan-400" />
          <span>API Docs</span>
        </a>
      </div>
    </header>
  );
};
