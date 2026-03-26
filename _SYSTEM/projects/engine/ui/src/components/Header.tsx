import { useDashboard } from '../store/DashboardContext';

export function Header() {
  const { state, dispatch } = useDashboard();
  const { connectionStatus, orchestrator: orch, headerTags } = state;

  return (
    <header className="col-span-full flex items-center gap-3 px-4 bg-s1 border-b border-border">
      {/* Logo + status */}
      <span className="text-[13px] font-bold text-atd-blue tracking-tight">ATD</span>
      <span className="text-[10px] text-dim font-normal">// LIVE</span>
      <div className={`w-[6px] h-[6px] rounded-full shrink-0 ${
        connectionStatus === 'disconnected' ? 'bg-atd-red' : 'bg-atd-green animate-glow'
      }`} />
      <span className={`text-[9px] ${
        connectionStatus === 'disconnected' ? 'text-atd-red' : connectionStatus === 'live' ? 'text-atd-green' : 'text-dim'
      }`}>
        {connectionStatus === 'connecting' ? 'connecting...' : connectionStatus}
      </span>

      {/* Tags */}
      <div className="flex gap-1.5 ml-1">
        {headerTags.map((tag, i) => (
          <span key={i} className={`px-2 py-px text-[9px] rounded-sm border ${
            tag.variant === 'success'
              ? 'border-atd-green/40 text-atd-green bg-atd-green/5'
              : 'border-border text-dim bg-s2'
          }`}>{tag.label}</span>
        ))}
      </div>

      {/* Stats */}
      <div className="ml-auto flex gap-3 text-[9px] text-dim items-center">
        <span>state: <span className={orch.state === 'idle' || orch.state === 'done' ? 'text-atd-green font-semibold' : 'text-atd-amber font-semibold'}>{orch.state}</span></span>
        <span>turn: <span className="text-text">{orch.turn}/{orch.max}</span></span>
        <span>speaker: <span className="text-text">{orch.speaker}</span></span>
        <span>challenges: <span className={orch.challenges > 0 ? 'text-atd-red' : 'text-text'}>{orch.challenges}</span></span>
        <button
          className="px-2 py-0.5 bg-s2 border border-border text-dim text-[9px] cursor-pointer hover:text-text hover:border-border-hi"
          onClick={() => dispatch({ type: 'UI_TOGGLE_LEDGER' })}
        >Ledger</button>
      </div>
    </header>
  );
}
