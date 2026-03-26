import { PALETTE } from '../constants/theme';

export function agentColor(key: string, overrides: Record<string, string> = {}): string {
  if (overrides[key]) return overrides[key];
  let h = 0;
  for (let i = 0; i < key.length; i++) {
    h = (h * 31 + key.charCodeAt(i)) & 0x7fffffff;
  }
  return PALETTE[h % PALETTE.length];
}
