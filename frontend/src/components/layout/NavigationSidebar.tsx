import React from 'react';
import { 
  BarChart2, BookOpen, MessageSquare, FileText, Compass, 
  Clock, Activity, Key, Settings, Bot, Layers, HardDrive, User 
} from 'lucide-react';

interface Props {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const NavigationSidebar: React.FC<Props> = ({ activeTab, setActiveTab }) => {
  return (
    <aside className="w-64 bg-slate-950 border-r border-slate-800 flex flex-col justify-between select-none">
      <div className="p-4 space-y-6">
        {/* Brand */}
        <div className="flex items-center gap-3 px-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-cyan-500 to-violet-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
            <Compass className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="font-bold text-sm tracking-tight text-white leading-none">Company Brain</h1>
            <span className="text-[10px] font-mono text-cyan-400 uppercase tracking-widest">FalkorDB Graph</span>
          </div>
        </div>

        {/* ANALYTICS */}
        <div>
          <span className="text-[10px] font-mono uppercase tracking-wider text-slate-500 px-2 font-semibold">Analytics</span>
          <div className="mt-2 space-y-1">
            <button 
              onClick={() => setActiveTab('chat')} 
              className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-medium transition ${activeTab === 'chat' ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/30' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'}`}
            >
              <MessageSquare className="w-4 h-4" />
              <span>Brain Chat</span>
            </button>
            <button 
              onClick={() => setActiveTab('overview')} 
              className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-medium transition ${activeTab === 'overview' ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/30' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'}`}
            >
              <BarChart2 className="w-4 h-4" />
              <span>Overview</span>
            </button>
            <button 
              onClick={() => setActiveTab('knowledge')} 
              className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-medium transition ${activeTab === 'knowledge' ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/30' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'}`}
            >
              <BookOpen className="w-4 h-4" />
              <span>Project Knowledge</span>
            </button>
          </div>
        </div>

        {/* DATA */}
        <div>
          <span className="text-[10px] font-mono uppercase tracking-wider text-slate-500 px-2 font-semibold">Data</span>
          <div className="mt-2 space-y-1">
            <button 
              onClick={() => setActiveTab('graph')} 
              className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-medium transition ${activeTab === 'graph' ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/30' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'}`}
            >
              <Compass className="w-4 h-4 text-cyan-400" />
              <span className="font-semibold text-slate-100">Knowledge Graph</span>
            </button>
            <button 
              onClick={() => setActiveTab('documents')} 
              className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-medium transition ${activeTab === 'documents' ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/30' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'}`}
            >
              <FileText className="w-4 h-4" />
              <span>Documents & ADRs</span>
            </button>
            <button 
              onClick={() => setActiveTab('timeline')} 
              className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-medium transition ${activeTab === 'timeline' ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/30' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'}`}
            >
              <Clock className="w-4 h-4" />
              <span>Decision Timeline</span>
            </button>
            <button 
              onClick={() => setActiveTab('activity')} 
              className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-medium transition ${activeTab === 'activity' ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/30' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'}`}
            >
              <Activity className="w-4 h-4" />
              <span>Graph Activity</span>
            </button>
          </div>
        </div>

        {/* DEVELOPER */}
        <div>
          <span className="text-[10px] font-mono uppercase tracking-wider text-slate-500 px-2 font-semibold">Developer</span>
          <div className="mt-2 space-y-1">
            <button 
              onClick={() => setActiveTab('api')} 
              className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-medium transition ${activeTab === 'api' ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/30' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'}`}
            >
              <Key className="w-4 h-4" />
              <span>API Contracts</span>
            </button>
            <button 
              onClick={() => setActiveTab('integrations')} 
              className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-medium transition ${activeTab === 'integrations' ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/30' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'}`}
            >
              <Layers className="w-4 h-4" />
              <span>FalkorDB & MCP</span>
            </button>
          </div>
        </div>
      </div>

      {/* ACCOUNT / FOOTER */}
      <div className="p-4 border-t border-slate-900 bg-slate-950/80">
        <div className="flex items-center gap-3 px-2 py-1.5 rounded-lg bg-slate-900/60 border border-slate-800">
          <div className="w-7 h-7 rounded-full bg-cyan-600/30 border border-cyan-500/50 flex items-center justify-center text-cyan-400 text-xs font-bold">
            NB
          </div>
          <div className="min-w-0">
            <p className="text-xs font-medium text-slate-200 truncate">Northstar Systems</p>
            <span className="text-[10px] text-emerald-400 font-mono">FalkorDB Track 03</span>
          </div>
        </div>
      </div>
    </aside>
  );
};
