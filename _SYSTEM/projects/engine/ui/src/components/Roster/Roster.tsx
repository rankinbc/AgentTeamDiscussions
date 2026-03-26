import { useDashboard } from '../../store/DashboardContext';
import { AgentRow } from './AgentRow';

export function Roster() {
  const { state } = useDashboard();

  return (
    <aside className="bg-s1 border-r border-border overflow-y-auto py-2 pb-5 scrollbar-thin">
      <div className="px-3 py-1 pb-2 text-[9px] tracking-[2px] uppercase text-dim">Agents</div>
      {state.agentOrder.map((key, i) => (
        <AgentRow key={key} agentKey={key} index={i} />
      ))}
    </aside>
  );
}
