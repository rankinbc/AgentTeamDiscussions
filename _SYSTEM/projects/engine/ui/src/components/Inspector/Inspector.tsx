import { useState } from 'react';
import Markdown from 'react-markdown';
import { useDashboard } from '../../store/DashboardContext';
import { agentColor } from '../../lib/colors';

type InspTab = 'response' | 'payload' | 'system';

export function Inspector() {
  const { state, dispatch } = useDashboard();
  const [activeTab, setActiveTab] = useState<InspTab>('response');
  const { inspectorOpen, inspectorData: data, selectedAgent } = state;

  if (!data) return null;

  const color = data.agent === 'synthesis'
    ? 'var(--color-atd-purple)'
    : agentColor(data.agent, state.colorOverrides);

  const tabContent = activeTab === 'response'
    ? data.response || '(no response yet)'
    : activeTab === 'payload'
    ? data.payload || '(no payload captured)'
    : data.systemPrompt || '(no system prompt captured)';

  const tabs: { key: InspTab; label: string }[] = [
    { key: 'response', label: 'Response' },
    { key: 'payload', label: 'Context Sent' },
    { key: 'system', label: 'System Prompt' },
  ];

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

      {/* Body — render markdown for response tab, plain text for context/system */}
      <div className="flex-1 overflow-y-auto px-4 py-2 text-[10px] text-text leading-[1.6] scrollbar-thin">
        {activeTab === 'response' ? (
          <div className="md-content">
            <Markdown>{tabContent}</Markdown>
          </div>
        ) : (
          <pre className="whitespace-pre-wrap break-words text-[9px]">{tabContent}</pre>
        )}
      </div>
    </div>
  );
}
