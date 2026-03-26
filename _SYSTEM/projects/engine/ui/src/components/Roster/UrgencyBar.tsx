import { useState, useEffect } from 'react';

interface UrgencyBarProps {
  startTime: number | null;
  sessionTimeout: number;
}

export function UrgencyBar({ startTime, sessionTimeout }: UrgencyBarProps) {
  const [elapsed, setElapsed] = useState(0);

  useEffect(() => {
    if (startTime === null) { setElapsed(0); return; }
    const iv = setInterval(() => setElapsed((Date.now() - startTime) / 1000), 200);
    return () => clearInterval(iv);
  }, [startTime]);

  const pct = startTime ? Math.min(elapsed / sessionTimeout, 1) : 0;
  const barColor = pct < 0.5 ? 'var(--color-atd-green)' : pct < 0.78 ? 'var(--color-atd-amber)' : 'var(--color-atd-red)';

  return (
    <div className="flex items-center gap-1 mt-1 text-[8px] text-dim">
      <div className="flex-1 h-[3px] bg-border rounded-sm overflow-hidden">
        <div
          className="h-full rounded-sm transition-[width] duration-200 ease-linear"
          style={{ width: `${pct * 100}%`, background: barColor }}
        />
      </div>
      <span className="min-w-[28px] text-right">{startTime ? `${elapsed.toFixed(0)}s` : ''}</span>
    </div>
  );
}
