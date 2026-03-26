export interface SessionStartEvent {
  type: 'session_start';
  time: string;
  brief: string;
  mode: string;
  question_count: number;
  agents: string[];
  display_names: Record<string, string>;
  timeout?: number;
}

export interface AgentProfileEvent {
  type: 'agent_profile';
  time: string;
  key: string;
  name: string;
  role: string;
  traits: Record<string, number>;
  cognitive_style?: string;
  emotional_baseline?: string;
  job?: string;
  drives: string[];
  pushback_on: string[];
  anti_slop: {
    agreement_tax: boolean;
    perspective_lock: boolean;
    devils_advocate: boolean;
    uncomfortable_quota: number;
    domain_pivot: boolean;
  };
  context_lens?: string;
  technique?: string;
  voice_tone?: string;
  intensity?: number;
}

export interface QuestionStartEvent {
  type: 'question_start';
  time: string;
  number: number;
  total: number;
  title: string;
}

export interface RoundStartEvent {
  type: 'round_start';
  time: string;
  round: string;
  agents: string;
}

export interface AgentThinkingEvent {
  type: 'agent_thinking';
  time: string;
  agent: string;
  display_name: string;
  round: string;
  question: number;
}

export interface AgentContextEvent {
  type: 'agent_context';
  time: string;
  agent: string;
  display_name: string;
  round: string;
  question: number;
  system_prompt: string;
  payload: string;
}

export interface AgentResponseEvent {
  type: 'agent_response';
  time: string;
  agent: string;
  display_name: string;
  response: string;
  elapsed: number;
  question: number;
  round: string;
  error?: boolean;
}

export interface SynthesisStartEvent {
  type: 'synthesis_start';
  time: string;
  question: number;
}

export interface SynthesisDoneEvent {
  type: 'synthesis_done';
  time: string;
  question_num: number;
  question_title: string;
  round_context: string;
  system_prompt: string;
  full_doc: string;
  preview: string;
  elapsed: number;
  lines: number;
}

export interface LedgerExtractedEvent {
  type: 'ledger_extracted';
  time: string;
  count: number;
  question: number;
}

export interface QuestionDoneEvent {
  type: 'question_done';
  time: string;
  number: number;
  elapsed: number;
}

export interface QuestionQueuedEvent {
  type: 'question_queued';
  time: string;
  number: number;
  title: string;
}

export interface QuestionFailedEvent {
  type: 'question_failed';
  time: string;
  number: number;
  reason: string;
}

export interface ChallengeEvent {
  type: 'challenge';
  time: string;
  from_name: string;
  target: string;
  target_name: string;
  description: string;
}

export interface BriefStartEvent {
  type: 'brief_start';
  time: string;
}

export interface BriefDoneEvent {
  type: 'brief_done';
  time: string;
  preview: string;
}

export interface SessionDoneEvent {
  type: 'session_done';
  time: string;
  elapsed: string;
  completed: number;
  total: number;
}

export interface ModeratorMessageEvent {
  type: 'moderator_message';
  time: string;
  text: string;
}

// Live conversation mode events
export interface ConversationStartEvent {
  type: 'conversation_start';
  time: string;
  question: string;
  max_turns: number;
  agent_profiles: AgentProfileEvent[];
  agent_colors?: Record<string, string>;
}

export interface AgentSpeakingEvent {
  type: 'agent_speaking';
  time: string;
  agent: string;
  display_name: string;
}

export interface AgentSpokeEvent {
  type: 'agent_spoke';
  time: string;
  agent: string;
  display_name: string;
  response: string;
  elapsed: number;
  turn: number;
  system_prompt: string;
  user_payload: string;
  context_messages: number;
}

export interface TurnStartEvent {
  type: 'turn_start';
  time: string;
  turn: number;
  max_turns: number;
}

export interface UrgencyUpdateEvent {
  type: 'urgency_update';
  time: string;
  [agentKey: string]: string | number;
}

export interface SystemMessageEvent {
  type: 'system_message';
  time: string;
  message: string;
}

export interface SynthesisUpdateEvent {
  type: 'synthesis_update';
  time: string;
  turn: number;
  mood: string;
  exhaustion: string;
  top_insight?: string;
}

export interface ConversationDoneEvent {
  type: 'conversation_done';
  time: string;
  turns: number;
  elapsed: string;
}

export type SSEEvent =
  | SessionStartEvent
  | AgentProfileEvent
  | QuestionStartEvent
  | RoundStartEvent
  | AgentThinkingEvent
  | AgentContextEvent
  | AgentResponseEvent
  | SynthesisStartEvent
  | SynthesisDoneEvent
  | LedgerExtractedEvent
  | QuestionDoneEvent
  | QuestionQueuedEvent
  | QuestionFailedEvent
  | ChallengeEvent
  | BriefStartEvent
  | BriefDoneEvent
  | SessionDoneEvent
  | ModeratorMessageEvent
  | ConversationStartEvent
  | AgentSpeakingEvent
  | AgentSpokeEvent
  | TurnStartEvent
  | UrgencyUpdateEvent
  | SystemMessageEvent
  | SynthesisUpdateEvent
  | ConversationDoneEvent;
