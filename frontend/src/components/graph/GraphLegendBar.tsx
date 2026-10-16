import React from 'react';

export const GraphLegendBar: React.FC = () => {
  return (
    <div className="absolute bottom-4 left-4 z-20 flex items-center gap-2 bg-slate-900/90 backdrop-blur-md px-4 py-2 rounded-xl border border-slate-800 text-xs text-slate-300 font-medium shadow-2xl">
      <span className="text-[10px] font-mono uppercase text-slate-500 font-bold mr-1">Legend:</span>
      
      <div className="flex items-center gap-1.5 px-2 py-0.5 rounded-md hover:bg-slate-800/60 cursor-pointer">
        <span className="w-2.5 h-2.5 rounded-full border border-cyan-400 bg-cyan-400/20" />
        <span className="text-[11px] text-cyan-300">Concept</span>
      </div>

      <div className="flex items-center gap-1.5 px-2 py-0.5 rounded-md hover:bg-slate-800/60 cursor-pointer">
        <span className="w-2.5 h-2.5 rounded-full border border-blue-400 bg-blue-400/20" />
        <span className="text-[11px] text-blue-300">Person</span>
      </div>

      <div className="flex items-center gap-1.5 px-2 py-0.5 rounded-md hover:bg-slate-800/60 cursor-pointer">
        <span className="w-2.5 h-2.5 rotate-45 border border-amber-400 bg-amber-400/20" />
        <span className="text-[11px] text-amber-300">Team / Process</span>
      </div>

      <div className="flex items-center gap-1.5 px-2 py-0.5 rounded-md hover:bg-slate-800/60 cursor-pointer">
        <span className="w-2.5 h-2.5 rounded-sm border border-pink-400 bg-pink-400/20" />
        <span className="text-[11px] text-pink-300">Service / Tool</span>
      </div>

      <div className="flex items-center gap-1.5 px-2 py-0.5 rounded-md hover:bg-slate-800/60 cursor-pointer">
        <span className="w-2.5 h-2.5 rotate-45 border border-violet-400 bg-violet-400/20" />
        <span className="text-[11px] text-violet-300">Decision / Event</span>
      </div>

      <div className="flex items-center gap-1.5 px-2 py-0.5 rounded-md hover:bg-slate-800/60 cursor-pointer">
        <span className="w-2.5 h-2.5 rounded-full border border-slate-400 bg-slate-400/20" />
        <span className="text-[11px] text-slate-300">Document / Chunk</span>
      </div>
    </div>
  );
};
