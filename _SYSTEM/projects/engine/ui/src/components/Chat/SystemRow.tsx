import Markdown from 'react-markdown';
import type { ChatItem } from '../../types/state';
import { useDashboard } from '../../store/DashboardContext';
import { agentColor } from '../../lib/colors';

interface SystemRowProps {
  item: ChatItem;
}

const STYLES: Record<string, { border: string; nameCls: string; bg: string }> = {
  'system':    { border: 'var(--color-atd-blue)',   nameCls: 'text-atd-blue',   bg: 'rgba(77,124,255,.03)' },
  'q-start':   { border: 'var(--color-atd-purple)', nameCls: 'text-atd-purple', bg: 'rgba(168,85,250,.04)' },
  'round-sep': { border: 'var(--color-border-hi)',  nameCls: 'text-dim',        bg: 'transparent' },
  'synthesis': { border: 'var(--color-atd-purple)', nameCls: 'text-atd-purple', bg: 'rgba(168,85,250,.04)' },
  'challenge': { border: 'var(--color-atd-red)',    nameCls: 'text-atd-red',    bg: 'rgba(255,77,106,.04)' },
  'ok':        { border: 'var(--color-atd-green)',  nameCls: 'text-atd-green',  bg: 'transparent' },
  'err':       { border: 'var(--color-atd-red)',    nameCls: 'text-atd-red',    bg: 'transparent' },
  'moderator': { border: 'var(--color-atd-amber)',  nameCls: 'text-atd-amber',  bg: 'rgba(245,166,35,.06)' },
};

export function SystemRow({ item }: SystemRowProps) {
  const { state, dispatch } = useDashboard();
  const v = STYLES[item.itemType] || STYLES['system'];
  const borderColor = item.color || v.border;

  // Thinking row
  if (item.itemType === 'thinking' && item.agentKey) {
    const c = agentColor(item.agentKey, state.colorOverrides);
    return (
      <div className="px-2.5 py-1 my-0.5 border-l-2" style={{ borderLeftColor: 'var(--color-atd-blue)' }}>
        <div className="flex items-baseline gap-1.5">
          <span className="text-[9px] font-semibold" style={{ color: c }}>{item.displayName}</span>
          <span className="text-[8px] text-dim">{item.meta}</span>
        </div>
        <div className="text-[9px] text-dim italic">thinking<span className="animate-cursor" /></div>
      </div>
    );
  }

  const handleClick = item.synthId
    ? () => dispatch({ type: 'UI_OPEN_SYNTH_INSPECTOR', synthId: item.synthId! })
    : undefined;

  const isQStart = item.itemType === 'q-start';
  const isRoundSep = item.itemType === 'round-sep';
  const useMarkdown = item.itemType === 'synthesis' || item.itemType === 'moderator';

  return (
    <div
      className={`px-2.5 py-1 my-0.5 border-l-2 ${handleClick ? 'cursor-pointer hover:bg-s2' : ''} ${
        state.inspectedId === item.synthId ? 'outline outline-1 outline-atd-amber -outline-offset-1' : ''
      }`}
      style={{ borderLeftColor: borderColor, background: v.bg }}
      onClick={handleClick}
    >
      <div className="flex items-baseline gap-1.5">
        <span className={`text-[9px] font-semibold ${v.nameCls} ${isRoundSep ? 'text-[8px] tracking-[1.5px] uppercase' : ''}`}>
          {item.label}
        </span>
        <span className="text-[8px] text-dim">{item.time}</span>
        {item.meta && (
          <span className="text-[8px] text-dim ml-auto">
            {item.meta}
            {item.clickable && <> &middot; <span className="text-atd-amber">inspect</span></>}
          </span>
        )}
      </div>
      {item.body && (
        isQStart ? (
          <div className="text-bright text-[12px] font-semibold mt-0.5">{item.body}</div>
        ) : useMarkdown ? (
          <div className="md-content text-[9px] text-dim leading-[1.5]">
            <Markdown>{item.body}</Markdown>
          </div>
        ) : (
          <div className={`text-[9px] leading-[1.5] whitespace-pre-wrap break-words ${
            item.itemType === 'challenge' ? 'text-text' : 'text-dim'
          }`}>{item.body}</div>
        )
      )}
    </div>
  );
}
