import Markdown from 'react-markdown';
import type { ChatItem } from '../../types/state';
import { useDashboard } from '../../store/DashboardContext';
import { agentColor } from '../../lib/colors';

interface MessageRowProps {
  item: ChatItem;
}

export function MessageRow({ item }: MessageRowProps) {
  const { state, dispatch } = useDashboard();
  const color = item.agentKey ? agentColor(item.agentKey, state.colorOverrides) : 'var(--color-dim)';
  const isInspected = state.inspectedId === item.id;

  return (
    <div
      className={`px-2.5 py-1.5 my-px border-l-2 cursor-pointer transition-colors hover:bg-s2 ${
        isInspected ? 'outline outline-1 outline-atd-amber -outline-offset-1 bg-s2' : ''
      }`}
      style={{ borderLeftColor: color }}
      onClick={() => dispatch({ type: 'UI_OPEN_INSPECTOR', msgId: item.id })}
    >
      <div className="flex items-baseline gap-1.5 mb-1">
        <span className="text-[10px] font-semibold" style={{ color }}>{item.displayName}</span>
        <span className="text-[8px] text-dim">{item.time}</span>
        <span className="text-[8px] text-dim ml-auto">
          {item.meta} &middot; <span className="text-atd-amber">inspect</span>
        </span>
      </div>
      <div className="md-content text-[11px] leading-[1.6] text-text">
        <Markdown>{item.body || ''}</Markdown>
      </div>
    </div>
  );
}
