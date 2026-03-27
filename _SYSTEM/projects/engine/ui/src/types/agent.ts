export interface AntiSlop {
  agreement_tax: boolean;
  perspective_lock: boolean;
  devils_advocate: boolean;
  uncomfortable_quota: number;
  domain_pivot: boolean;
}

export interface AgentProfile {
  key: string;
  name: string;
  role: string;
  traits: Record<string, number>;
  cognitive_style?: string;
  emotional_baseline?: string;
  job?: string;
  drives: string[];
  pushback_on: string[];
  anti_slop: AntiSlop;
  context_lens?: string;
  technique?: string;
  voice_tone?: string;
  intensity?: number;
}

export interface AgentMessageEntry {
  text: string;
  turn: number;
  elapsed: number;
}

export interface MsgStoreEntry {
  agent: string;
  displayName: string;
  turn: number;
  round: string;
  question: number;
  systemPrompt: string;
  payload: string;
  response: string;
  elapsed: number;
  contextStatsKey?: string;
}

export interface ContextSectionStat {
  name: string;
  chars: number;
  tokens: number;
  isProtected: boolean;
}

export interface ContextStatsEntry {
  totalTokens: number;
  budgetTokens: number;
  budgetPct: number;
  sections: ContextSectionStat[];
  rescueActions: string[];
}

export interface SynthStoreEntry {
  question_num: number;
  question_title: string;
  round_context: string;
  system_prompt: string;
  full_doc: string;
  elapsed: number;
  lines: number;
}
