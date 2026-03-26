export const PALETTE = [
  '#6366f1', '#06b6d4', '#f97316', '#ef4444', '#22c55e', '#a855f7',
  '#eab308', '#ec4899', '#14b8a6', '#f43f5e', '#3b82f6', '#84cc16',
];

export const MOD_ACTIONS: Record<string, string> = {
  refocus: 'MODERATOR DIRECTIVE: The discussion has drifted. Refocus on the original question. Do not introduce new topics until the current one is resolved.',
  deeper: 'MODERATOR DIRECTIVE: Go deeper on the current thread. Do not move on yet. Challenge assumptions, name specific failure modes, and get concrete.',
  move_on: 'MODERATOR DIRECTIVE: This subtopic is sufficiently explored. Move to the next important unresolved question. Do not rehash what was just discussed.',
  challenge: 'MODERATOR DIRECTIVE: The current direction feels like premature agreement. Push back. What is being assumed without evidence? What failure mode is nobody naming?',
  summarize: 'MODERATOR DIRECTIVE: Before continuing, each of you state in ONE sentence what you believe has been decided so far and what remains unresolved.',
  pause: 'MODERATOR DIRECTIVE: Pause after this speaker. The moderator needs to review before it continues.',
};
