import { useRef, useEffect } from 'react';
import { useDashboard } from '../../store/DashboardContext';
import { MessageRow } from './MessageRow';
import { SystemRow } from './SystemRow';
import { OrchestratorBar } from './OrchestratorBar';
import { ModeratorBar } from './ModeratorBar';

export function ChatPanel() {
  const { state } = useDashboard();
  const messagesRef = useRef<HTMLDivElement>(null);
  const userScrolledUp = useRef(false);

  const handleScroll = () => {
    const el = messagesRef.current;
    if (!el) return;
    userScrolledUp.current = el.scrollHeight - el.scrollTop - el.clientHeight > 40;
  };

  useEffect(() => {
    if (!userScrolledUp.current && messagesRef.current) {
      messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
    }
  }, [state.chatItems.length]);

  return (
    <div className="flex flex-col min-h-0 overflow-hidden">
      <div ref={messagesRef} className="flex-1 overflow-y-auto px-4 pt-2 pb-1 scrollbar-thin" onScroll={handleScroll}>
        {state.chatItems.map((item) =>
          item.itemType === 'message'
            ? <MessageRow key={item.id} item={item} />
            : <SystemRow key={item.id} item={item} />
        )}
      </div>
      <OrchestratorBar />
      <ModeratorBar />
    </div>
  );
}
