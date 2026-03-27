import { useState } from 'react';
import Markdown from 'react-markdown';
import { useDashboard } from '../../store/DashboardContext';
import { agentColor } from '../../lib/colors';
import type { ContextStatsEntry } from '../../types/agent';

type InspTab = 'response' | 'payload' | 'system' | 'context';

export function Inspector() {
  const { state, dispatch } = useDashboard();
  const [activeTab, setActiveTab] = useState<InspTab>('response');
  const { inspectorOpen, inspectorData: data, selectedAgent } = state;

  if (!data) return null;

  const color = data.agent === 'synthesis'
    ? 'var(--color-atd-purple)'
    : agentColor(data.agent, state.colorOverrides);

  const stats: ContextStatsEntry | undefined = data.contextStatsKey
    ? state.ctxStatsStore[data.contextStatsKey]
    : undefined;

  const tabs: { key: InspTab; label: string }[] = [
    { key: 'response', label: 'Response' },
    { key: 'payload', label: 'Context Sent' },
    { key: 'system', label: 'System Prompt' },
    { key: 'context', label: stats ? `Context · ${stats.totalTokens}tok` : 'Context' },
  ];

  const textContent = activeTab === 'payload'
    ? data.payload || '(no payload captured)'
    : activeTab === 'system'
    ? data.systemPrompt || '(no system prompt captured)'
    : '';

  return (
    <div
      className={`fixed bottom-0 overflow-hidden bg-s1 border-t-2 border-atd-amber transition-all duration-200 ease-out z-50 flex flex-col ${
        inspectorOpen ? 'h-[42vh]' : 'h-0'
      }`}
      style={{ left: '220px', right: selectedAgent ? '300px' : '0' }}
    >
      {/* Header bar */}
      <div className="shrink-0 flex items-center gap-2 px-4 py-1 bg-s2 border-b border-border text-[9px] uppercase tracking-[1.5px] text-atd-amber">
        PROMPT INSPECTOR
        <span className="ml-auto cursor-pointer text-dim hover:text-text" onClick={() => dispatch({ type: 'UI_CLOSE_INSPECTOR' })}>
          [x] close
        </span>
      </div>

      {/* Meta info */}
      <div className="text-[9px] text-dim px-4 py-1 border-b border-border flex gap-2">
        <span style={{ color }}>{data.displayName}</span>
        <span>turn {data.turn ?? '?'}</span>
        <span>{data.elapsed ?? '?'}s</span>
        <span>Q{data.question ?? '?'} {data.round || ''}</span>
      </div>

      {/* Tabs */}
      <div className="shrink-0 flex px-4 border-b border-border bg-s1">
        {tabs.map((t) => (
          <button
            key={t.key}
            className={`px-3 py-1 text-[9px] cursor-pointer bg-transparent border-b-2 uppercase tracking-wide ${
              activeTab === t.key ? 'text-atd-amber border-atd-amber' : 'text-dim border-transparent hover:text-text'
            }`}
            onClick={() => setActiveTab(t.key)}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* Body */}
      <div className="flex-1 overflow-y-auto px-4 py-2 text-[10px] text-text leading-[1.6] scrollbar-thin">
        {activeTab === 'response' ? (
          <div className="md-content">
            <Markdown>{data.response || '(no response yet)'}</Markdown>
          </div>
        ) : activeTab === 'context' ? (
          <ContextTab stats={stats} />
        ) : (
          <pre className="whitespace-pre-wrap break-words text-[9px]">{textContent}</pre>
        )}
      </div>
    </div>
  );
}

function ContextTab({ stats }: { stats: ContextStatsEntry | undefined }) {
  if (!stats) {
    return <p className="text-dim text-[9px]">No context telemetry available for this turn.</p>;
  }

  const budgetPct = Math.round(stats.budgetPct * 100);
  const budgetColor = budgetPct >= 90 ? 'text-red-400' : budgetPct >= 70 ? 'text-yellow-400' : 'text-atd-green';

  return (
    <div className="space-y-3">
      {/* Budget summary row */}
      <div className="flex gap-4 text-[9px] pb-2 border-b border-border">
        <span className="text-dim">total</span>
        <span className="font-mono">{stats.totalTokens} tok</span>
        <span className="text-dim">budget</span>
        <span className="font-mono">{stats.budgetTokens} tok</span>
        <span className="text-dim">used</span>
        <span className={`font-mono font-bold ${budgetColor}`}>{budgetPct}%</span>
      </div>

      {/* Section table */}
      <table className="w-full text-[9px] border-collapse">
        <thead>
          <tr className="text-dim text-left">
            <th className="pb-1 pr-4 font-normal">section</th>
            <th className="pb-1 pr-4 font-normal text-right">chars</th>
            <th className="pb-1 pr-4 font-normal text-right">tokens</th>
            <th className="pb-1 font-normal text-right">% budget</th>
          </tr>
        </thead>
        <tbody>
          {stats.sections.map((s) => {
            const pct = stats.budgetTokens > 0 ? Math.round((s.tokens / stats.budgetTokens) * 100) : 0;
            return (
              <tr key={s.name} className="border-t border-border/40">
                <td className="py-0.5 pr-4 font-mono">
                  {s.name}
                  {s.isProtected && <span className="ml-1 text-dim">[P]</span>}
                </td>
                <td className="py-0.5 pr-4 text-right font-mono text-dim">{s.chars.toLocaleString()}</td>
                <td className="py-0.5 pr-4 text-right font-mono">{s.tokens}</td>
                <td className="py-0.5 text-right font-mono text-dim">{pct}%</td>
              </tr>
            );
          })}
        </tbody>
      </table>

      {/* Rescue actions */}
      {stats.rescueActions.length > 0 && (
        <div className="pt-2 border-t border-border space-y-1">
          <div className="text-[9px] text-yellow-400 uppercase tracking-wide">rescue actions</div>
          {stats.rescueActions.map((a, i) => (
            <div key={i} className="text-[9px] text-dim font-mono">{a}</div>
          ))}
        </div>
      )}
    </div>
  );
}
