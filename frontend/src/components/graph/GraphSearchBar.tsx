import React from 'react';
import { Search, Filter } from 'lucide-react';

interface Props {
  entityCount: number;
  linkCount: number;
  factCount: number;
  searchQuery: string;
  setSearchQuery: (q: string) => void;
}

export const GraphSearchBar: React.FC<Props> = ({ 
  entityCount, 
  linkCount, 
  factCount, 
  searchQuery, 
  setSearchQuery 
}) => {
  return (
    <div className="absolute top-4 left-4 z-20 flex items-center gap-3">
      {/* Metrics pills */}
      <div className="flex items-center gap-2 bg-slate-900/90 backdrop-blur-md px-3 py-1.5 rounded-xl border border-slate-800 text-xs font-mono">
        <span className="flex items-center gap-1.5 text-cyan-400">
          <span className="w-2 h-2 rounded-full bg-cyan-400" />
          {entityCount} Entities
        </span>
        <span className="text-slate-700">|</span>
        <span className="flex items-center gap-1.5 text-violet-400">
          <span className="w-2 h-2 rounded-full bg-violet-400" />
          {linkCount} Links
        </span>
        <span className="text-slate-700">|</span>
        <span className="flex items-center gap-1.5 text-emerald-400">
          <span className="w-2 h-2 rounded-full bg-emerald-400" />
          {factCount} Facts
        </span>
      </div>

      {/* Search Bar */}
      <div className="relative">
        <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
        <input 
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search entities, services, ADRs..."
          className="w-72 bg-slate-900/90 backdrop-blur-md text-xs text-white pl-9 pr-4 py-2 rounded-xl border border-slate-800 focus:outline-none focus:border-cyan-500 transition placeholder:text-slate-500 shadow-xl"
        />
      </div>
    </div>
  );
};
