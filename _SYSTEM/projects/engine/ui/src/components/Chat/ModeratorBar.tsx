import { useRef } from 'react';
import { useDashboard } from '../../store/DashboardContext';
import { sendModerator, addQuestion } from '../../lib/api';
import { MOD_ACTIONS } from '../../constants/theme';

export function ModeratorBar() {
  const { dispatch } = useDashboard();
  const modRef = useRef<HTMLInputElement>(null);
  const qRef = useRef<HTMLInputElement>(null);

  const now = () => new Date().toLocaleTimeString('en', { hour: '2-digit', minute: '2-digit', second: '2-digit' });

  const handleSendMod = () => {
    const msg = modRef.current?.value.trim();
    if (!msg) return;
    modRef.current!.value = '';
    sendModerator(msg);
    dispatch({
      type: 'UI_ADD_LOCAL_CHAT',
      item: { id: `mod-${Date.now()}`, itemType: 'moderator', time: now(), label: 'MODERATOR', body: msg, color: 'var(--color-atd-amber)' },
    });
  };

  const handleAddQ = () => {
    const msg = qRef.current?.value.trim();
    if (!msg) return;
    qRef.current!.value = '';
    addQuestion(msg);
    dispatch({
      type: 'UI_ADD_LOCAL_CHAT',
      item: { id: `q-local-${Date.now()}`, itemType: 'system', time: now(), label: 'QUEUED', body: msg, color: 'var(--color-atd-cyan)' },
    });
  };

  const handleAction = (action: string) => {
    const msg = MOD_ACTIONS[action];
    if (!msg) return;
    sendModerator(msg);
    dispatch({
      type: 'UI_ADD_LOCAL_CHAT',
      item: { id: `mod-act-${Date.now()}`, itemType: 'system', time: '', label: `MOD: ${action.toUpperCase().replace('_', ' ')}`, color: 'var(--color-atd-amber)' },
    });
  };

  const ACTIONS = [
    { key: 'refocus', label: 'Refocus' },
    { key: 'deeper', label: 'Go Deeper' },
    { key: 'move_on', label: 'Move On' },
    { key: 'challenge', label: 'Challenge' },
    { key: 'summarize', label: 'Summarize' },
  ];

  const btnCls = "bg-s2 border border-border text-atd-amber text-[9px] px-2 py-[3px] cursor-pointer uppercase tracking-wide whitespace-nowrap hover:bg-border-hi";

  return (
    <div className="shrink-0 px-4 py-1.5 border-t border-border bg-s1">
      <div className="flex gap-1.5 mb-1">
        <input
          ref={modRef}
          className="flex-1 bg-s2 border border-border text-text text-[11px] px-2 py-1 outline-none focus:border-atd-amber"
          placeholder="Steer the conversation — agents will prioritize your message..."
          onKeyDown={(e) => e.key === 'Enter' && handleSendMod()}
        />
        <button className={btnCls} onClick={handleSendMod}>Send</button>
      </div>
      <div className="flex gap-1.5 mb-1">
        <input
          ref={qRef}
          className="flex-1 bg-s2 border border-border text-text text-[11px] px-2 py-1 outline-none opacity-70 focus:opacity-100 focus:border-atd-cyan"
          placeholder="Add a question to the queue (runs after current question)..."
          onKeyDown={(e) => e.key === 'Enter' && handleAddQ()}
        />
        <button className="bg-s2 border border-border text-atd-cyan text-[9px] px-2 py-[3px] cursor-pointer uppercase tracking-wide whitespace-nowrap hover:bg-border-hi" onClick={handleAddQ}>Add Q</button>
      </div>
      <div className="flex gap-1 flex-wrap">
        {ACTIONS.map((a) => (
          <button key={a.key} className={btnCls} onClick={() => handleAction(a.key)}>{a.label}</button>
        ))}
        <button className="bg-s2 border border-border text-atd-red text-[9px] px-2 py-[3px] cursor-pointer uppercase tracking-wide whitespace-nowrap hover:border-atd-red hover:bg-border-hi" onClick={() => handleAction('pause')}>Pause</button>
      </div>
    </div>
  );
}
