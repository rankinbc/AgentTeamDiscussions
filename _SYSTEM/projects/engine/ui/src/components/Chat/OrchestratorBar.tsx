import { useDashboard } from '../../store/DashboardContext';

export function OrchestratorBar() {
  const { state } = useDashboard();
  return (
    <div className="shrink-0 px-4 py-[3px] border-t border-border bg-s2 text-[8px] text-dim flex gap-3 items-center">
      <span>{state.briefName}</span>
      <span>{state.modeName}</span>
      <span>{state.totalMessages} messages</span>
    </div>
  );
}
