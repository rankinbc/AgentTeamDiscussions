import { useDashboard } from '../../store/DashboardContext';
import { agentColor } from '../../lib/colors';
import { TraitBar } from './TraitBar';
import { UrgencyBar } from './UrgencyBar';

interface AgentRowProps {
  agentKey: string;
  index: number;
}

export function AgentRow({ agentKey }: AgentRowProps) {
  const { state, dispatch } = useDashboard();
  const profile = state.agentProfiles[agentKey];
  const msgs = state.agentMessages[agentKey] || [];
  const isSpeaking = state.urgencyStartTimes[agentKey] != null;
  const isSelected = state.selectedAgent === agentKey;
  const color = agentColor(agentKey, state.colorOverrides);
  const startTime = state.urgencyStartTimes[agentKey] ?? null;

  let statusText = 'waiting';
  if (isSpeaking) statusText = 'speaking...';
  else if (msgs.length > 0) statusText = `${msgs.length} msgs | ${msgs[msgs.length - 1].elapsed}s`;

  return (
    <div
      className={`px-3 py-2 border-l-2 cursor-pointer transition-colors hover:bg-s2 ${
        isSpeaking ? '!border-l-atd-blue bg-s2' : ''
      } ${isSelected ? 'bg-s3' : ''}`}
      style={{ borderLeftColor: isSpeaking ? undefined : color }}
      onClick={() => dispatch({ type: 'UI_SELECT_AGENT', agentKey })}
    >
      <div className="text-[11px] font-semibold mb-0.5" style={{ color }}>{profile?.name || agentKey}</div>
      <div className="text-[8px] text-dim mb-1 truncate">{profile?.role || ''}</div>
      {profile?.traits && Object.entries(profile.traits).map(([name, val]) => (
        <TraitBar key={name} label={name.replace(/_/g, ' ')} value={val} color={color} />
      ))}
      <UrgencyBar startTime={startTime} sessionTimeout={state.sessionTimeout} />
      <div className="text-[8px] mt-1 text-dim italic">{statusText}</div>
    </div>
  );
}
