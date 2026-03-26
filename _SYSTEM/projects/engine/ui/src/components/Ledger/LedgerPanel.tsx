import { useEffect } from 'react';
import Markdown from 'react-markdown';
import { useDashboard } from '../../store/DashboardContext';
import { fetchLedger } from '../../lib/api';

export function LedgerPanel() {
  const { state, dispatch } = useDashboard();
  const { ledgerOpen, ledgerContent, ledgerTimestamp } = state;

  useEffect(() => {
    if (!ledgerOpen) return;
    fetchLedger().then((text) => {
      const ts = new Date().toLocaleTimeString('en', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
      dispatch({ type: 'UI_SET_LEDGER', content: text || '(ledger is empty)', timestamp: ts });
    }).catch(() => {
      dispatch({ type: 'UI_SET_LEDGER', content: '(error reading ledger)', timestamp: '' });
    });
  }, [ledgerOpen, dispatch]);

  return (
    <div className={`fixed bottom-0 right-0 w-[480px] overflow-hidden bg-s1 border-t-2 border-atd-purple border-l border-border transition-all duration-200 ease-out z-[60] flex flex-col ${
      ledgerOpen ? 'h-[55vh]' : 'h-0'
    }`}>
      <div className="shrink-0 flex items-center gap-2 px-4 py-1 bg-s2 border-b border-border text-[9px] uppercase tracking-[1.5px] text-atd-purple">
        DECISIONS LEDGER
        {ledgerTimestamp && <span className="text-dim text-[8px] normal-case tracking-normal">{ledgerTimestamp}</span>}
        <span className="ml-auto cursor-pointer text-dim hover:text-text" onClick={() => dispatch({ type: 'UI_TOGGLE_LEDGER' })}>[x] close</span>
      </div>
      <div className="flex-1 overflow-y-auto px-4 py-2 text-[10px] text-text leading-[1.6] scrollbar-thin">
        <div className="md-content">
          <Markdown>{ledgerContent || '(no session running yet)'}</Markdown>
        </div>
      </div>
    </div>
  );
}
