interface TraitBarProps {
  label: string;
  value: number;
  color: string;
  compact?: boolean;
}

export function TraitBar({ label, value, color, compact = true }: TraitBarProps) {
  return (
    <div className="flex items-center gap-1 my-px text-[8px] text-dim">
      <span className={compact ? 'w-[58px] shrink-0' : 'w-[70px] shrink-0'}>{label}</span>
      <div className="flex-1 h-[2px] bg-border rounded-sm">
        <div className="h-full rounded-sm" style={{ width: `${value * 100}%`, background: color }} />
      </div>
      <span className={`${compact ? 'w-[22px]' : 'w-[26px]'} text-right`}>
        {compact ? value.toFixed(1) : value.toFixed(2)}
      </span>
    </div>
  );
}
