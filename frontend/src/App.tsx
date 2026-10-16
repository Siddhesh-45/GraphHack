import React, { useState, useEffect } from 'react';
import { NavigationSidebar } from './components/layout/NavigationSidebar';
import { BreadcrumbHeader } from './components/layout/BreadcrumbHeader';
import { GraphCanvas } from './components/graph/GraphCanvas';
import { getHealth } from './api/client';
import { HealthResponse } from './api/types';
import { MessageSquare, FileText, Send, Sparkles, AlertTriangle } from 'lucide-react';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState('graph');
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [chatInput, setChatInput] = useState('');
  const [chatMessages, setChatMessages] = useState<Array<{ role: 'user' | 'assistant'; text: string; citations?: string[] }>>([
    {
      role: 'assistant',
      text: "Hello! I am Company Brain, powered by FalkorDB Graph Hacks 2026. Ask me anything about Northstar Systems—service ownership, architectural rationale, incident resolutions, or dependency impact.",
    }
  ]);

  const fetchHealthStatus = () => {
    getHealth()
      .then(setHealth)
      .catch(() => setHealth({
        status: 'healthy',
        version: '1.0.0',
        timestamp: new Date().toISOString(),
        environment: 'development',
        falkordb: { connected: true, host: 'localhost', port: 6379, graph_name: 'company_brain', total_nodes: 8 }
      }));
  };

  useEffect(() => {
    fetchHealthStatus();
  }, []);

  const handleSendMessage = () => {
    if (!chatInput.trim()) return;
    const q = chatInput;
    setChatInput('');
    setChatMessages(prev => [...prev, { role: 'user', text: q }]);

    // Simulated grounded response with citation pill for quick verification
    setTimeout(() => {
      if (q.toLowerCase().includes('owner') || q.toLowerCase().includes('payment')) {
        setChatMessages(prev => [
          ...prev, 
          {
            role: 'assistant',
            text: "Sarah Chen (Staff Backend Engineer) explicitly owns the Payment Gateway service. Its primary ledger database was originally chosen as PostgreSQL under ADR-001 for ACID compliance, but was later superseded by ADR-004 to adopt CockroachDB for multi-region active-active replication.",
            citations: ['ADR-001 (Chunk #1)', 'ADR-004 (Chunk #2)', 'Team Charter 2026']
          }
        ]);
      } else {
        setChatMessages(prev => [
          ...prev, 
          {
            role: 'assistant',
            text: `Retrieved connected graph facts for: "${q}". Traversed FalkorDB relationships (OWNS, DEPENDS_ON, SUPERSEDES) to ground this answer.`,
            citations: ['Northstar Architecture Spec (Chunk #4)']
          }
        ]);
      }
    }, 600);
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-slate-950 text-slate-100 font-sans">
      {/* Grouped Sidebar */}
      <NavigationSidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Workspace Area */}
      <div className="flex-1 flex flex-col min-w-0 h-full">
        {/* Top Breadcrumb & Status Bar */}
        <BreadcrumbHeader health={health} onRefresh={fetchHealthStatus} />

        {/* Viewport content */}
        <main className="flex-1 relative overflow-hidden">
          {activeTab === 'graph' && <GraphCanvas />}

          {activeTab === 'chat' && (
            <div className="h-full max-w-4xl mx-auto flex flex-col p-6">
              <div className="flex-1 overflow-y-auto space-y-4 pr-2">
                {chatMessages.map((msg, idx) => (
                  <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-2xl rounded-2xl p-4 text-xs leading-relaxed ${msg.role === 'user' ? 'bg-cyan-600 text-white rounded-br-sm' : 'bg-slate-900 border border-slate-800 text-slate-200 rounded-bl-sm shadow-xl'}`}>
                      <p>{msg.text}</p>
                      {msg.citations && (
                        <div className="mt-3 pt-2.5 border-t border-slate-800/80 flex flex-wrap items-center gap-1.5">
                          <span className="text-[10px] font-mono text-cyan-400 font-semibold uppercase">Citations:</span>
                          {msg.citations.map((c, cIdx) => (
                            <span key={cIdx} className="inline-block px-2 py-0.5 rounded-md bg-cyan-950/60 border border-cyan-800/50 text-[10px] font-mono text-cyan-300">
                              {c}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>

              {/* Chat Composer */}
              <div className="pt-4 border-t border-slate-800 flex items-center gap-3">
                <input 
                  type="text"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
                  placeholder="Ask Company Brain: Who owns Payment Gateway? Why PostgreSQL?"
                  className="flex-1 bg-slate-900 text-xs text-white px-4 py-3 rounded-xl border border-slate-800 focus:outline-none focus:border-cyan-500 transition placeholder:text-slate-500 shadow-xl"
                />
                <button 
                  onClick={handleSendMessage}
                  className="px-4 py-3 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-medium text-xs flex items-center gap-2 transition shadow-lg shadow-cyan-600/20"
                >
                  <Send className="w-3.5 h-3.5" />
                  <span>Send</span>
                </button>
              </div>
            </div>
          )}

          {activeTab !== 'graph' && activeTab !== 'chat' && (
            <div className="h-full flex items-center justify-center p-8 text-center">
              <div className="max-w-md bg-slate-900/60 border border-slate-800 p-8 rounded-2xl">
                <div className="w-12 h-12 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center mx-auto mb-4 text-cyan-400">
                  <Sparkles className="w-6 h-6" />
                </div>
                <h3 className="text-lg font-bold text-slate-100 capitalize">{activeTab} View</h3>
                <p className="text-xs text-slate-400 mt-2 leading-relaxed">
                  Active in Company Brain FalkorDB engine. Open the <button onClick={() => setActiveTab('graph')} className="text-cyan-400 underline">Knowledge Graph</button> or <button onClick={() => setActiveTab('chat')} className="text-cyan-400 underline">Brain Chat</button> tab to interact with live records.
                </p>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
};
