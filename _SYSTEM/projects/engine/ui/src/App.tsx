import { useRef, useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import Markdown from 'react-markdown';
import { useDashboard } from './store/DashboardContext';
import { useSSE } from './hooks/useSSE';
import { agentColor } from './lib/colors';
import { sendModerator, addQuestion, fetchLedger, stopSession } from './lib/api';
import { MOD_ACTIONS } from './constants/theme';
import type { ChatItem } from './types/state';

// ─── Utilities ───────────────────────────────────────────────

function timeNow() {
  return new Date().toLocaleTimeString('en', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
}

// ─── Urgency Bar (self-ticking) ──────────────────────────────

function UrgencyBar({ startTime, timeout }: { startTime: number | null; timeout: number }) {
  const [elapsed, setElapsed] = useState(0);
  useEffect(() => {
    if (!startTime) { setElapsed(0); return; }
    const iv = setInterval(() => setElapsed((Date.now() - startTime) / 1000), 200);
    return () => clearInterval(iv);
  }, [startTime]);

  const pct = startTime ? Math.min(elapsed / timeout, 1) : 0;
  const color = pct < 0.5 ? 'var(--green)' : pct < 0.78 ? 'var(--amber)' : 'var(--red)';

  return (
    <div className="urg-wrap">
      <div className="urg-track">
        <div className="urg-fill" style={{ width: `${pct * 100}%`, background: color }} />
      </div>
      <span>{startTime ? `${elapsed.toFixed(0)}s` : ''}</span>
    </div>
  );
}

// ─── Dashboard ───────────────────────────────────────────────

function Dashboard() {
  const { state, dispatch } = useDashboard();
  useSSE(dispatch);

  const { connectionStatus: conn, orchestrator: orch, headerTags, selectedAgent } = state;
  const messagesRef = useRef<HTMLDivElement>(null);
  const scrolledUp = useRef(false);
  const modRef = useRef<HTMLInputElement>(null);
  const qRef = useRef<HTMLInputElement>(null);
  const [inspTab, setInspTab] = useState<'response' | 'payload' | 'system'>('response');
  const navigate = useNavigate();
  const doStop = async () => {
    try {
      await stopSession();
      navigate('/');
    } catch {}
  };

  // Auto-scroll
  const handleScroll = useCallback(() => {
    const el = messagesRef.current;
    if (el) scrolledUp.current = el.scrollHeight - el.scrollTop - el.clientHeight > 40;
  }, []);

  useEffect(() => {
    if (!scrolledUp.current && messagesRef.current) {
      messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
    }
  }, [state.chatItems.length]);

  // Moderator
  const doSendMod = () => {
    const msg = modRef.current?.value.trim();
    if (!msg) return;
    modRef.current!.value = '';
    sendModerator(msg);
    dispatch({ type: 'UI_ADD_LOCAL_CHAT', item: { id: `mod-${Date.now()}`, itemType: 'moderator', time: timeNow(), label: 'MODERATOR', body: msg, color: 'var(--amber)' } });
  };
  const doAddQ = () => {
    const msg = qRef.current?.value.trim();
    if (!msg) return;
    qRef.current!.value = '';
    addQuestion(msg);
    dispatch({ type: 'UI_ADD_LOCAL_CHAT', item: { id: `q-${Date.now()}`, itemType: 'system', time: timeNow(), label: 'QUEUED', body: msg, color: 'var(--cyan)' } });
  };
  const doAction = (a: string) => {
    const msg = MOD_ACTIONS[a];
    if (!msg) return;
    sendModerator(msg);
    dispatch({ type: 'UI_ADD_LOCAL_CHAT', item: { id: `ma-${Date.now()}`, itemType: 'system', time: '', label: `MOD: ${a.toUpperCase().replace('_', ' ')}`, color: 'var(--amber)' } });
  };

  // Ledger
  useEffect(() => {
    if (!state.ledgerOpen) return;
    fetchLedger().then(t => dispatch({ type: 'UI_SET_LEDGER', content: t || '(empty)', timestamp: timeNow() }))
      .catch(() => dispatch({ type: 'UI_SET_LEDGER', content: '(error)', timestamp: '' }));
  }, [state.ledgerOpen, dispatch]);

  // Inspector data
  const insp = state.inspectorData;
  const inspContent = insp
    ? inspTab === 'response' ? insp.response || '(none)' : inspTab === 'payload' ? insp.payload || '(none)' : insp.systemPrompt || '(none)'
    : '';
  const inspColor = insp ? (insp.agent === 'synthesis' ? 'var(--purple)' : agentColor(insp.agent, state.colorOverrides)) : '';

  // Detail panel
  const detailProfile = selectedAgent ? state.agentProfiles[selectedAgent] : null;
  const detailMsgs = selectedAgent ? state.agentMessages[selectedAgent] || [] : [];
  const detailColor = selectedAgent ? agentColor(selectedAgent, state.colorOverrides) : '';

  const orchStateClass = (orch.state === 'idle' || orch.state === 'done') ? 'state-val idle' : 'state-val active';

  // Render a chat item
  const renderItem = (item: ChatItem) => {
    if (item.itemType === 'message') {
      const c = item.agentKey ? agentColor(item.agentKey, state.colorOverrides) : 'var(--dim)';
      const isInsp = state.inspectedId === item.id;
      return (
        <div key={item.id} className={`msg ${isInsp ? 'inspected' : ''}`} style={{ borderLeftColor: c }}
          onClick={() => dispatch({ type: 'UI_OPEN_INSPECTOR', msgId: item.id })}>
          <div className="msg-hdr">
            <span className="msg-name" style={{ color: c }}>{item.displayName}</span>
            <span className="msg-time">{item.time}</span>
            <span className="msg-meta">{item.meta} &middot; <span className="inspect-link">inspect</span></span>
          </div>
          <div className="msg-body md"><Markdown>{item.body || ''}</Markdown></div>
        </div>
      );
    }

    // Thinking row
    if (item.itemType === 'thinking') {
      const c = item.agentKey ? agentColor(item.agentKey, state.colorOverrides) : 'var(--blue)';
      return (
        <div key={item.id} className="sys thinking">
          <div className="msg-hdr">
            <span className="msg-name" style={{ color: c }}>{item.displayName}</span>
            <span className="msg-meta">{item.meta}</span>
          </div>
          <div className="msg-body">thinking</div>
        </div>
      );
    }

    // System rows
    const clsMap: Record<string, string> = {
      'q-start': 'q-start', 'round-sep': 'round-sep', 'synthesis': 'synthesis',
      'challenge': 'challenge', 'ok': 'ok', 'err': 'err', 'moderator': 'moderator', 'system': '',
    };
    const cls = clsMap[item.itemType] || '';
    const borderStyle = item.color ? { borderLeftColor: item.color } : {};
    const isSynthClick = item.synthId ? () => dispatch({ type: 'UI_OPEN_SYNTH_INSPECTOR', synthId: item.synthId! }) : undefined;

    return (
      <div key={item.id} className={`sys ${cls} ${isSynthClick ? 'cursor-pointer' : ''} ${state.inspectedId === item.synthId ? 'inspected' : ''}`}
        style={{ ...borderStyle, cursor: isSynthClick ? 'pointer' : undefined }} onClick={isSynthClick}>
        <div className="msg-hdr">
          <span className="msg-name">{item.label}</span>
          <span className="msg-time">{item.time}</span>
          {item.meta && <span className="msg-meta">{item.meta}{item.clickable && <> &middot; <span className="inspect-link">inspect</span></>}</span>}
        </div>
        {item.body && (
          item.itemType === 'q-start'
            ? <div className="msg-body">{item.body}</div>
            : (item.itemType === 'synthesis' || item.itemType === 'moderator')
              ? <div className="msg-body md"><Markdown>{item.body}</Markdown></div>
              : <div className="msg-body">{item.body}</div>
        )}
      </div>
    );
  };

  // Anti-slop rules
  const slopRules: string[] = [];
  if (detailProfile?.anti_slop) {
    const s = detailProfile.anti_slop;
    if (s.agreement_tax) slopRules.push('Must add substance when agreeing');
    if (s.perspective_lock) slopRules.push('Stay in character under pressure');
    if (s.devils_advocate) slopRules.push('Argue the other side');
    if (s.uncomfortable_quota > 0) slopRules.push(`Uncomfortable idea quota: ${s.uncomfortable_quota}`);
    if (s.domain_pivot) slopRules.push('Inject cross-domain perspectives');
  }

  return (
    <>
      {/* ─── Shell ─── */}
      <div className={`shell ${selectedAgent ? 'detail-open' : ''}`}>

        {/* ─── Header ─── */}
        <header className="hdr">
          <div className="hdr-logo">ATD <span>// LIVE</span></div>
          <div className={`status-dot ${conn === 'disconnected' ? 'off' : ''}`} />
          <span style={{ fontSize: 10, color: conn === 'disconnected' ? 'var(--red)' : conn === 'live' ? 'var(--green)' : 'var(--dim)' }}>
            {conn === 'connecting' ? 'connecting...' : conn}
          </span>
          {headerTags.map((t, i) => <span key={i} className={`tag ${t.variant === 'success' ? 'ok' : ''}`}>{t.label}</span>)}
          <div className="hdr-stats">
            <span>state: <span className={orchStateClass}>{orch.state}</span></span>
            <span>turn: <span className="val">{orch.turn}/{orch.max}</span></span>
            <span>speaker: <span className="val">{orch.speaker}</span></span>
            <span>challenges: <span className="val" style={{ color: orch.challenges > 0 ? 'var(--red)' : undefined }}>{orch.challenges}</span></span>
            <button className="hdr-btn" onClick={() => dispatch({ type: 'UI_TOGGLE_LEDGER' })}>Ledger</button>
            {conn === 'live' && (
              <button className="hdr-btn danger" onClick={doStop}>Stop</button>
            )}
          </div>
        </header>

        {/* ─── Roster ─── */}
        <div className="roster">
          <div className="roster-title">Agents</div>
          {state.agentOrder.map(k => {
            const p = state.agentProfiles[k];
            const msgs = state.agentMessages[k] || [];
            const speaking = state.urgencyStartTimes[k] != null;
            const sel = selectedAgent === k;
            const c = agentColor(k, state.colorOverrides);
            let status = 'waiting';
            if (speaking) status = 'speaking...';
            else if (msgs.length) status = `${msgs.length} msgs | ${msgs[msgs.length - 1].elapsed}s`;

            return (
              <div key={k} className={`agent-row ${speaking ? 'speaking' : ''} ${sel ? 'selected' : ''}`}
                style={{ borderLeftColor: speaking ? undefined : c }}
                onClick={() => dispatch({ type: 'UI_SELECT_AGENT', agentKey: k })}>
                <div className="agent-name" style={{ color: c }}>{p?.name || k}</div>
                <div className="agent-role">{p?.role || ''}</div>
                {p?.traits && Object.entries(p.traits).map(([n, v]) => (
                  <div key={n} className="trait-row">
                    <span className="trait-lbl">{n.replace(/_/g, ' ')}</span>
                    <div className="trait-bar"><div className="trait-fill" style={{ width: `${v * 100}%`, background: c }} /></div>
                    <span className="trait-val">{v.toFixed(1)}</span>
                  </div>
                ))}
                <UrgencyBar startTime={state.urgencyStartTimes[k] ?? null} timeout={state.sessionTimeout} />
                <div className="agent-status">{status}</div>
              </div>
            );
          })}
        </div>

        {/* ─── Chat ─── */}
        <div className="chat-wrap">
          <div ref={messagesRef} className="messages" onScroll={handleScroll}>
            {state.chatItems.map(renderItem)}
          </div>
          <div className="orch-bar">
            <span>{state.briefName}</span>
            <span>{state.modeName}</span>
            <span>{state.totalMessages} messages</span>
          </div>
          <div className="mod-bar">
            <div className="mod-row">
              <input ref={modRef} className="mod-input" placeholder="Steer the conversation — agents will prioritize your message..."
                onKeyDown={e => e.key === 'Enter' && doSendMod()} />
              <button className="mod-btn" onClick={doSendMod}>Send</button>
            </div>
            <div className="mod-row">
              <input ref={qRef} className="mod-input q-input" placeholder="Add a question to the queue..."
                onKeyDown={e => e.key === 'Enter' && doAddQ()} />
              <button className="mod-btn cyan" onClick={doAddQ}>Add Q</button>
            </div>
            <div className="mod-actions">
              <button className="mod-btn" onClick={() => doAction('refocus')}>Refocus</button>
              <button className="mod-btn" onClick={() => doAction('deeper')}>Go Deeper</button>
              <button className="mod-btn" onClick={() => doAction('move_on')}>Move On</button>
              <button className="mod-btn" onClick={() => doAction('challenge')}>Challenge</button>
              <button className="mod-btn" onClick={() => doAction('summarize')}>Summarize</button>
              <button className="mod-btn danger" onClick={() => doAction('pause')}>Pause</button>
            </div>
          </div>
        </div>

        {/* ─── Detail Panel ─── */}
        <div className="detail">
          {selectedAgent && (
            <>
              <div className="detail-hdr">
                <span className="detail-close" onClick={() => dispatch({ type: 'UI_CLOSE_DETAIL' })}>[x] close</span>
                <div className="d-name" style={{ color: detailColor }}>{detailProfile?.name || selectedAgent}</div>
                <div className="d-role">{detailProfile?.role || ''}</div>
              </div>
              {!detailProfile ? (
                <div className="d-section" style={{ color: 'var(--dim)', fontSize: 10 }}>Profile not loaded yet</div>
              ) : (
                <div className="d-section">
                  <h3>Personality</h3>
                  {Object.entries(detailProfile.traits || {}).map(([n, v]) => (
                    <div key={n} className="d-trait">
                      <span className="d-trait-lbl">{n.replace(/_/g, ' ')}</span>
                      <div className="d-trait-bar"><div className="d-trait-fill" style={{ width: `${v * 100}%`, background: detailColor }} /></div>
                      <span className="d-trait-val">{v.toFixed(2)}</span>
                    </div>
                  ))}

                  {(detailProfile.cognitive_style || detailProfile.emotional_baseline || detailProfile.job) && <>
                    <h3>Character</h3>
                    {detailProfile.cognitive_style && <div className="d-item">cognitive: {detailProfile.cognitive_style}</div>}
                    {detailProfile.emotional_baseline && <div className="d-item">emotional: {detailProfile.emotional_baseline}</div>}
                    {detailProfile.job && <div className="d-item">job: {detailProfile.job}</div>}
                  </>}

                  {detailProfile.drives.length > 0 && <>
                    <h3>Drives</h3>
                    {detailProfile.drives.map((d, i) => <div key={i} className="d-item drive">{d}</div>)}
                  </>}

                  {detailProfile.pushback_on.length > 0 && <>
                    <h3>Pushback on</h3>
                    {detailProfile.pushback_on.map((p, i) => <div key={i} className="d-item pushback">{p}</div>)}
                  </>}

                  {slopRules.length > 0 && <>
                    <h3>Active rules</h3>
                    {slopRules.map((r, i) => <div key={i} className="d-item rule">{r}</div>)}
                  </>}

                  {detailProfile.context_lens && <>
                    <h3>Context lens</h3>
                    <div className="d-context">{detailProfile.context_lens}</div>
                  </>}

                  {(detailProfile.technique || detailProfile.voice_tone) && <>
                    <h3>Technique & voice</h3>
                    {detailProfile.technique && <div className="d-item">technique: {detailProfile.technique}</div>}
                    {detailProfile.voice_tone && <div className="d-item">voice: {detailProfile.voice_tone}</div>}
                    {detailProfile.intensity !== undefined && <div className="d-item">intensity: {detailProfile.intensity}</div>}
                  </>}

                  <h3>Session stats</h3>
                  <div className="d-stat"><span className="d-stat-lbl">messages</span><span className="d-stat-val">{detailMsgs.length}</span></div>
                  {detailMsgs.length > 0 && <div className="d-stat"><span className="d-stat-lbl">last spoke</span><span className="d-stat-val">turn {detailMsgs[detailMsgs.length - 1].turn ?? '?'}</span></div>}

                  {detailMsgs.length > 0 && <>
                    <h3>Recent responses</h3>
                    {detailMsgs.slice(-5).map((m, i) => (
                      <div key={i} className="d-item" style={{ fontSize: 9 }}>
                        <span style={{ color: 'var(--dim)' }}>turn {m.turn ?? '?'} &middot; {m.elapsed ?? '?'}s</span><br />
                        {(m.text || '').substring(0, 200)}{(m.text || '').length > 200 ? '...' : ''}
                      </div>
                    ))}
                  </>}
                </div>
              )}
            </>
          )}
        </div>
      </div>

      {/* ─── Inspector ─── */}
      <div className={`inspector ${state.inspectorOpen ? 'open' : ''}`}>
        {insp && <>
          <div className="insp-bar">
            PROMPT INSPECTOR
            <span className="insp-close" onClick={() => dispatch({ type: 'UI_CLOSE_INSPECTOR' })}>[x] close</span>
          </div>
          <div className="insp-meta">
            <span style={{ color: inspColor }}>{insp.displayName}</span>
            {' \u00B7 turn '}{insp.turn ?? '?'}
            {' \u00B7 '}{insp.elapsed ?? '?'}s
            {' \u00B7 Q'}{insp.question ?? '?'} {insp.round || ''}
          </div>
          <div className="insp-tabs">
            {(['response', 'payload', 'system'] as const).map(t => (
              <button key={t} className={`itab ${inspTab === t ? 'active' : ''}`}
                onClick={() => setInspTab(t)}>
                {t === 'response' ? 'Response' : t === 'payload' ? 'Context Sent' : 'System Prompt'}
              </button>
            ))}
          </div>
          <div className="insp-body">
            {inspTab === 'response'
              ? <div className="md"><Markdown>{inspContent}</Markdown></div>
              : <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word', margin: 0, background: 'none', fontSize: 11 }}>{inspContent}</pre>
            }
          </div>
        </>}
      </div>

      {/* ─── Ledger ─── */}
      <div className={`ledger ${state.ledgerOpen ? 'open' : ''}`}>
        <div className="ledger-bar">
          DECISIONS LEDGER
          {state.ledgerTimestamp && <span style={{ color: 'var(--dim)', fontSize: 9, textTransform: 'none', letterSpacing: 0 }}> &middot; {state.ledgerTimestamp}</span>}
          <span className="insp-close" onClick={() => dispatch({ type: 'UI_TOGGLE_LEDGER' })}>[x] close</span>
        </div>
        <div className="ledger-body md">
          <Markdown>{state.ledgerContent || '(no session running)'}</Markdown>
        </div>
      </div>
    </>
  );
}

export { Dashboard };
