import type { AgentProfile, AgentMessageEntry, MsgStoreEntry, SynthStoreEntry } from './agent';

export type ConnectionStatus = 'connecting' | 'live' | 'disconnected';

export interface OrchestratorState {
  state: string;
  turn: number;
  max: number | string;
  speaker: string;
  challenges: number;
}

export interface TagInfo {
  label: string;
  variant?: 'default' | 'success';
}

export type ChatItemType =
  | 'message'
  | 'system'
  | 'q-start'
  | 'round-sep'
  | 'thinking'
  | 'synthesis'
  | 'challenge'
  | 'ok'
  | 'err'
  | 'moderator';

export interface ChatItem {
  id: string;
  itemType: ChatItemType;
  agentKey?: string;
  displayName?: string;
  time: string;
  label?: string;
  meta?: string;
  body?: string;
  color?: string;
  clickable?: boolean;
  synthId?: string;
}

export interface DashboardState {
  connectionStatus: ConnectionStatus;
  sessionTimeout: number;
  agentProfiles: Record<string, AgentProfile | null>;
  agentMessages: Record<string, AgentMessageEntry[]>;
  agentOrder: string[];
  chatItems: ChatItem[];
  msgStore: Record<string, MsgStoreEntry>;
  ctxStore: Record<string, { systemPrompt: string; payload: string }>;
  synthStore: Record<string, SynthStoreEntry>;
  totalMessages: number;
  orchestrator: OrchestratorState;
  headerTags: TagInfo[];
  colorOverrides: Record<string, string>;
  // Urgency tracking: agentKey → start timestamp (Date.now())
  urgencyStartTimes: Record<string, number | null>;
  // UI panel state
  selectedAgent: string | null;
  inspectorOpen: boolean;
  inspectorData: MsgStoreEntry | null;
  inspectedId: string | null;
  ledgerOpen: boolean;
  ledgerContent: string;
  ledgerTimestamp: string;
  briefName: string;
  modeName: string;
  // Counters
  msgIdCounter: number;
  synthIdCounter: number;
}

export const initialState: DashboardState = {
  connectionStatus: 'connecting',
  sessionTimeout: 120,
  agentProfiles: {},
  agentMessages: {},
  agentOrder: [],
  chatItems: [],
  msgStore: {},
  ctxStore: {},
  synthStore: {},
  totalMessages: 0,
  orchestrator: { state: 'idle', turn: 0, max: '\u2014', speaker: '\u2014', challenges: 0 },
  headerTags: [],
  colorOverrides: {},
  urgencyStartTimes: {},
  selectedAgent: null,
  inspectorOpen: false,
  inspectorData: null,
  inspectedId: null,
  ledgerOpen: false,
  ledgerContent: '',
  ledgerTimestamp: '',
  briefName: '\u2014',
  modeName: '\u2014',
  msgIdCounter: 0,
  synthIdCounter: 0,
};
