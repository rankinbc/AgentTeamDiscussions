import { useDashboard } from '../../store/DashboardContext';
import { agentColor } from '../../lib/colors';
import { TraitBar } from '../Roster/TraitBar';

export function DetailPanel() {
  const { state, dispatch } = useDashboard();
  const { selectedAgent } = state;
  if (!selectedAgent) return null;

  const profile = state.agentProfiles[selectedAgent];
  const color = agentColor(selectedAgent, state.colorOverrides);
  const msgs = state.agentMessages[selectedAgent] || [];

  const slop = profile?.anti_slop;
  const rules: string[] = [];
  if (slop) {
    if (slop.agreement_tax) rules.push('Must add substance when agreeing');
    if (slop.perspective_lock) rules.push('Stay in character under pressure');
    if (slop.devils_advocate) rules.push('Argue the other side');
    if (slop.uncomfortable_quota > 0) rules.push(`Uncomfortable idea quota: ${slop.uncomfortable_quota}`);
    if (slop.domain_pivot) rules.push('Inject cross-domain perspectives');
  }

  return (
    <div className="bg-s1 border-l border-border overflow-y-auto scrollbar-thin">
      {/* Header */}
      <div className="px-3 py-2.5 border-b border-border bg-s2 sticky top-0 z-10">
        <span className="float-right text-[9px] text-dim cursor-pointer hover:text-text" onClick={() => dispatch({ type: 'UI_CLOSE_DETAIL' })}>
          [x] close
        </span>
        <div className="text-[13px] font-semibold mb-0.5" style={{ color }}>{profile?.name || selectedAgent}</div>
        <div className="text-[9px] text-dim">{profile?.role || ''}</div>
      </div>

      {!profile ? (
        <div className="px-3 py-4 text-[9px] text-dim">Profile not yet loaded</div>
      ) : (
        <div className="px-3 py-2">
          {/* Personality */}
          <Section title="Personality">
            {Object.entries(profile.traits || {}).map(([name, val]) => (
              <TraitBar key={name} label={name.replace(/_/g, ' ')} value={val} color={color} compact={false} />
            ))}
          </Section>

          {/* Character */}
          {(profile.cognitive_style || profile.emotional_baseline || profile.job) && (
            <Section title="Character">
              {profile.cognitive_style && <Item>cognitive: {profile.cognitive_style}</Item>}
              {profile.emotional_baseline && <Item>emotional: {profile.emotional_baseline}</Item>}
              {profile.job && <Item>job: {profile.job}</Item>}
            </Section>
          )}

          {/* Drives */}
          {profile.drives.length > 0 && (
            <Section title="Drives">
              {profile.drives.map((d, i) => <Item key={i} variant="drive">{d}</Item>)}
            </Section>
          )}

          {/* Pushback */}
          {profile.pushback_on.length > 0 && (
            <Section title="Pushback on">
              {profile.pushback_on.map((p, i) => <Item key={i} variant="pushback">{p}</Item>)}
            </Section>
          )}

          {/* Active rules */}
          {rules.length > 0 && (
            <Section title="Active rules">
              {rules.map((r, i) => <Item key={i} variant="rule">{r}</Item>)}
            </Section>
          )}

          {/* Context lens */}
          {profile.context_lens && (
            <Section title="Context lens">
              <div className="text-[8px] text-dim px-1.5 py-1 bg-s2 my-1 leading-[1.4] rounded">{profile.context_lens}</div>
            </Section>
          )}

          {/* Technique */}
          {(profile.technique || profile.voice_tone) && (
            <Section title="Technique & voice">
              {profile.technique && <Item>technique: {profile.technique}</Item>}
              {profile.voice_tone && <Item>voice: {profile.voice_tone}</Item>}
              {profile.intensity !== undefined && <Item>intensity: {profile.intensity}</Item>}
            </Section>
          )}

          {/* Stats */}
          <Section title="Session stats">
            <Stat label="messages" value={String(msgs.length)} />
            {msgs.length > 0 && <Stat label="last spoke" value={`turn ${msgs[msgs.length - 1].turn ?? '?'}`} />}
          </Section>

          {/* Recent */}
          {msgs.length > 0 && (
            <Section title="Recent responses">
              {msgs.slice(-5).map((m, i) => (
                <div key={i} className="text-[8px] border-l border-border pl-2 my-1 leading-[1.4]">
                  <span className="text-dim">turn {m.turn ?? '?'} &middot; {m.elapsed ?? '?'}s</span>
                  <br />
                  {(m.text || '').substring(0, 200)}{(m.text || '').length > 200 ? '...' : ''}
                </div>
              ))}
            </Section>
          )}
        </div>
      )}
    </div>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="mb-2">
      <h3 className="text-[8px] uppercase tracking-[1.5px] text-dim mt-2 mb-1 border-b border-border pb-0.5">{title}</h3>
      {children}
    </div>
  );
}

function Item({ children, variant }: { children: React.ReactNode; variant?: 'drive' | 'pushback' | 'rule' }) {
  const borderColor = variant === 'drive' ? 'var(--color-atd-green)' : variant === 'pushback' ? 'var(--color-atd-red)' : variant === 'rule' ? 'var(--color-atd-amber)' : 'var(--color-border)';
  return (
    <div className="text-[9px] text-text py-0.5 pl-2 border-l my-0.5 leading-[1.4]" style={{ borderLeftColor: borderColor }}>{children}</div>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between text-[9px] py-0.5">
      <span className="text-dim">{label}</span>
      <span className="text-text">{value}</span>
    </div>
  );
}
