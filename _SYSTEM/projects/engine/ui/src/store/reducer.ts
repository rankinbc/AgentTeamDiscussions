import type { DashboardState, ChatItem, ConnectionStatus } from '../types/state';
import type { SSEEvent, AgentProfileEvent } from '../types/events';
import type { AgentProfile, MsgStoreEntry, SynthStoreEntry, ContextStatsEntry } from '../types/agent';

// ── Action types ──────────────────────────────────────────────

export type DashboardAction =
  | { type: 'SSE_EVENT'; event: SSEEvent }
  | { type: 'UI_SELECT_AGENT'; agentKey: string }
  | { type: 'UI_CLOSE_DETAIL' }
  | { type: 'UI_OPEN_INSPECTOR'; msgId: string }
  | { type: 'UI_OPEN_SYNTH_INSPECTOR'; synthId: string }
  | { type: 'UI_CLOSE_INSPECTOR' }
  | { type: 'UI_TOGGLE_LEDGER' }
  | { type: 'UI_SET_LEDGER'; content: string; timestamp: string }
  | { type: 'UI_SET_CONNECTION'; status: ConnectionStatus }
  | { type: 'UI_ADD_LOCAL_CHAT'; item: ChatItem };

// ── Helpers ───────────────────────────────────────────────────

function profileFromEvent(ev: AgentProfileEvent): AgentProfile {
  return {
    key: ev.key,
    name: ev.name,
    role: ev.role,
    traits: ev.traits || {},
    cognitive_style: ev.cognitive_style,
    emotional_baseline: ev.emotional_baseline,
    job: ev.job,
    drives: ev.drives || [],
    pushback_on: ev.pushback_on || [],
    anti_slop: ev.anti_slop || {
      agreement_tax: false, perspective_lock: false, devils_advocate: false,
      uncomfortable_quota: 0, domain_pivot: false,
    },
    context_lens: ev.context_lens,
    technique: ev.technique,
    voice_tone: ev.voice_tone,
    intensity: ev.intensity,
  };
}

function appendChat(state: DashboardState, item: ChatItem): ChatItem[] {
  return [...state.chatItems, item];
}

// ── Reducer ───────────────────────────────────────────────────

export function dashboardReducer(state: DashboardState, action: DashboardAction): DashboardState {
  switch (action.type) {
    case 'UI_SET_CONNECTION':
      return { ...state, connectionStatus: action.status };

    case 'UI_SELECT_AGENT':
      if (state.selectedAgent === action.agentKey) {
        return { ...state, selectedAgent: null };
      }
      return { ...state, selectedAgent: action.agentKey };

    case 'UI_CLOSE_DETAIL':
      return { ...state, selectedAgent: null };

    case 'UI_OPEN_INSPECTOR': {
      const data = state.msgStore[action.msgId];
      if (!data) return state;
      return {
        ...state,
        inspectorOpen: true,
        inspectorData: data,
        inspectedId: action.msgId,
      };
    }

    case 'UI_OPEN_SYNTH_INSPECTOR': {
      const synth = state.synthStore[action.synthId];
      if (!synth) return state;
      const synthData: MsgStoreEntry = {
        agent: 'synthesis',
        displayName: 'Synthesis' + (synth.question_num ? ' Q' + synth.question_num : '') +
          (synth.question_title ? ' \u2014 ' + synth.question_title.substring(0, 40) : ''),
        turn: synth.question_num,
        round: 'synthesis',
        question: synth.question_num,
        systemPrompt: synth.system_prompt,
        payload: synth.round_context,
        response: synth.full_doc,
        elapsed: synth.elapsed,
      };
      return {
        ...state,
        inspectorOpen: true,
        inspectorData: synthData,
        inspectedId: action.synthId,
      };
    }

    case 'UI_CLOSE_INSPECTOR':
      return { ...state, inspectorOpen: false, inspectedId: null };

    case 'UI_TOGGLE_LEDGER':
      return { ...state, ledgerOpen: !state.ledgerOpen };

    case 'UI_SET_LEDGER':
      return { ...state, ledgerContent: action.content, ledgerTimestamp: action.timestamp };

    case 'UI_ADD_LOCAL_CHAT':
      return { ...state, chatItems: appendChat(state, action.item) };

    case 'SSE_EVENT':
      return handleSSEEvent(state, action.event);

    default:
      return state;
  }
}

// ── SSE event handler ─────────────────────────────────────────

function handleSSEEvent(state: DashboardState, ev: SSEEvent): DashboardState {
  switch (ev.type) {
    case 'session_start': {
      const agentProfiles = { ...state.agentProfiles };
      const agentMessages = { ...state.agentMessages };
      for (const k of ev.agents) {
        agentProfiles[k] = agentProfiles[k] || null;
        agentMessages[k] = agentMessages[k] || [];
      }
      return {
        ...state,
        sessionTimeout: ev.timeout || 120,
        agentOrder: ev.agents,
        agentProfiles,
        agentMessages,
        headerTags: [
          { label: ev.brief },
          { label: ev.mode },
          { label: `${ev.question_count} q` },
        ],
        connectionStatus: 'live',
        briefName: ev.brief,
        modeName: ev.mode,
        orchestrator: {
          ...state.orchestrator,
          state: 'running',
          max: ev.question_count || '\u2014',
        },
      };
    }

    case 'agent_profile': {
      const profile = profileFromEvent(ev);
      const agentOrder = state.agentOrder.includes(ev.key)
        ? state.agentOrder
        : [...state.agentOrder, ev.key];
      return {
        ...state,
        agentProfiles: { ...state.agentProfiles, [ev.key]: profile },
        agentMessages: { ...state.agentMessages, [ev.key]: state.agentMessages[ev.key] || [] },
        agentOrder,
      };
    }

    case 'question_start': {
      const item: ChatItem = {
        id: `qs-${ev.number}`,
        itemType: 'q-start',
        time: ev.time || '',
        label: `Q${ev.number} / ${ev.total}`,
        body: ev.title,
      };
      return {
        ...state,
        chatItems: appendChat(state, item),
        orchestrator: { ...state.orchestrator, state: 'running', turn: ev.number },
      };
    }

    case 'round_start': {
      const item: ChatItem = {
        id: `rs-${ev.round}-${Date.now()}`,
        itemType: 'round-sep',
        time: ev.time || '',
        label: ev.round,
        meta: ev.agents || '',
      };
      return { ...state, chatItems: appendChat(state, item) };
    }

    case 'agent_thinking': {
      // Remove existing thinking row for this agent
      const filtered = state.chatItems.filter(c => c.id !== `think-${ev.agent}`);
      const item: ChatItem = {
        id: `think-${ev.agent}`,
        itemType: 'thinking',
        agentKey: ev.agent,
        displayName: ev.display_name,
        time: ev.time || '',
        meta: ev.round || '',
        body: 'thinking',
        color: undefined, // will be derived from agentKey
      };
      const speakerShort = ev.display_name.replace(/^The /, '').split('(')[0].trim();
      return {
        ...state,
        chatItems: [...filtered, item],
        urgencyStartTimes: { ...state.urgencyStartTimes, [ev.agent]: Date.now() },
        orchestrator: { ...state.orchestrator, state: 'thinking', speaker: speakerShort },
      };
    }

    case 'agent_context': {
      const ck = `${ev.agent}::${ev.question}::${ev.round}`;
      return {
        ...state,
        ctxStore: {
          ...state.ctxStore,
          [ck]: { systemPrompt: ev.system_prompt || '', payload: ev.payload || '' },
        },
      };
    }

    case 'agent_context_stats': {
      const ck = `${ev.agent}::${ev.question}::${ev.round}`;
      const entry: ContextStatsEntry = {
        totalTokens: ev.total_tokens,
        budgetTokens: ev.budget_tokens,
        budgetPct: ev.budget_pct,
        sections: ev.sections.map(s => ({
          name: s.name,
          chars: s.chars,
          tokens: s.tokens,
          isProtected: s.is_protected,
        })),
        rescueActions: ev.rescue_actions || [],
      };
      return {
        ...state,
        ctxStatsStore: { ...state.ctxStatsStore, [ck]: entry },
      };
    }

    case 'agent_response': {
      // Remove thinking row
      const filtered = state.chatItems.filter(c => c.id !== `think-${ev.agent}`);
      const mid = `m${state.msgIdCounter}`;
      const ck = `${ev.agent}::${ev.question}::${ev.round}`;
      const ctx = state.ctxStore[ck] || { systemPrompt: '', payload: '' };
      const stats = state.ctxStatsStore[ck];
      const msgEntry: MsgStoreEntry = {
        agent: ev.agent,
        displayName: ev.display_name || ev.agent,
        turn: ev.question,
        round: ev.round || '?',
        question: ev.question,
        systemPrompt: ctx.systemPrompt,
        payload: ctx.payload,
        response: ev.response || '',
        elapsed: ev.elapsed,
        contextStatsKey: ck,
      };
      const tokenMeta = stats ? ` \u00B7 ${stats.totalTokens}tok` : '';
      const chatItem: ChatItem = {
        id: mid,
        itemType: 'message',
        agentKey: ev.agent,
        displayName: ev.display_name,
        time: ev.time || '',
        meta: `${ev.elapsed}s \u00B7 Q${ev.question || '?'} ${ev.round || ''}${tokenMeta}`,
        body: ev.response || '[empty]',
        clickable: true,
      };
      const msgs = [...(state.agentMessages[ev.agent] || []), { text: ev.response, turn: ev.question, elapsed: ev.elapsed }];
      return {
        ...state,
        chatItems: [...filtered, chatItem],
        msgStore: { ...state.msgStore, [mid]: msgEntry },
        agentMessages: { ...state.agentMessages, [ev.agent]: msgs },
        totalMessages: state.totalMessages + 1,
        msgIdCounter: state.msgIdCounter + 1,
        urgencyStartTimes: { ...state.urgencyStartTimes, [ev.agent]: null },
        orchestrator: { ...state.orchestrator, state: 'running', speaker: '\u2014' },
      };
    }

    case 'synthesis_start': {
      const item: ChatItem = {
        id: `synth-start-${Date.now()}`,
        itemType: 'synthesis',
        time: ev.time || '',
        label: 'SYNTHESIS',
        meta: 'compiling...',
      };
      return {
        ...state,
        chatItems: appendChat(state, item),
        orchestrator: { ...state.orchestrator, state: 'thinking', speaker: 'synthesis' },
      };
    }

    case 'synthesis_done': {
      const sid = `synth${state.synthIdCounter}`;
      const synthEntry: SynthStoreEntry = {
        question_num: ev.question_num,
        question_title: ev.question_title || '',
        round_context: ev.round_context || '',
        system_prompt: ev.system_prompt || '',
        full_doc: ev.full_doc || ev.preview || '',
        elapsed: ev.elapsed,
        lines: ev.lines,
      };
      const preview = (ev.preview || '').substring(0, 300) + ((ev.preview || '').length > 300 ? '\u2026' : '');
      const item: ChatItem = {
        id: sid,
        itemType: 'synthesis',
        time: ev.time || '',
        label: 'SYNTHESIS COMPLETE',
        meta: `${ev.lines} lines \u00B7 ${ev.elapsed}s \u00B7 Q${ev.question_num || '?'}`,
        body: preview,
        clickable: true,
        synthId: sid,
      };
      return {
        ...state,
        chatItems: appendChat(state, item),
        synthStore: { ...state.synthStore, [sid]: synthEntry },
        synthIdCounter: state.synthIdCounter + 1,
        orchestrator: { ...state.orchestrator, state: 'running', speaker: '\u2014' },
      };
    }

    case 'ledger_extracted': {
      const item: ChatItem = {
        id: `ledger-${Date.now()}`,
        itemType: 'ok',
        time: ev.time || '',
        label: 'LEDGER',
        meta: `Q${ev.question}`,
        body: `${ev.count} decisions extracted`,
      };
      return { ...state, chatItems: appendChat(state, item) };
    }

    case 'question_done': {
      const item: ChatItem = {
        id: `qd-${ev.number}`,
        itemType: 'ok',
        time: ev.time || '',
        label: `Q${ev.number} DONE`,
        meta: `${ev.elapsed}s`,
      };
      return {
        ...state,
        chatItems: appendChat(state, item),
        orchestrator: { ...state.orchestrator, state: 'running' },
      };
    }

    case 'question_queued': {
      const item: ChatItem = {
        id: `qq-${ev.number}`,
        itemType: 'system',
        time: ev.time || '',
        label: `Q${ev.number} QUEUED`,
        body: ev.title,
        color: 'var(--color-atd-cyan)',
      };
      return { ...state, chatItems: appendChat(state, item) };
    }

    case 'question_failed': {
      const item: ChatItem = {
        id: `qf-${ev.number}`,
        itemType: 'err',
        time: ev.time || '',
        label: `Q${ev.number} FAILED`,
        body: ev.reason,
      };
      return { ...state, chatItems: appendChat(state, item) };
    }

    case 'challenge': {
      const newChallenges = state.orchestrator.challenges + 1;
      const item: ChatItem = {
        id: `ch-${Date.now()}`,
        itemType: 'challenge',
        time: ev.time || '',
        label: 'CHALLENGE',
        body: `${ev.from_name || '?'} \u2192 ${ev.target_name || '?'}: ${ev.description || ''}`,
      };
      return {
        ...state,
        chatItems: appendChat(state, item),
        orchestrator: { ...state.orchestrator, challenges: newChallenges },
      };
    }

    case 'brief_start': {
      const item: ChatItem = {
        id: `brief-start-${Date.now()}`,
        itemType: 'synthesis',
        time: ev.time || '',
        label: 'MORNING BRIEF',
        meta: 'generating...',
      };
      return { ...state, chatItems: appendChat(state, item) };
    }

    case 'brief_done': {
      const preview = (ev.preview || '').substring(0, 400) + ((ev.preview || '').length > 400 ? '\u2026' : '');
      const item: ChatItem = {
        id: `brief-done-${Date.now()}`,
        itemType: 'synthesis',
        time: ev.time || '',
        label: 'MORNING BRIEF READY',
        body: preview,
      };
      return { ...state, chatItems: appendChat(state, item) };
    }

    case 'session_done': {
      const tag = { label: `DONE ${ev.elapsed} \u00B7 ${ev.completed}/${ev.total}`, variant: 'success' as const };
      return {
        ...state,
        headerTags: [...state.headerTags, tag],
        connectionStatus: 'live',
        orchestrator: { ...state.orchestrator, state: 'done' },
      };
    }

    // ── Conversation mode events ──────────────────────────────

    case 'conversation_start': {
      const agentProfiles = { ...state.agentProfiles };
      const agentMessages = { ...state.agentMessages };
      const agentOrder: string[] = [];
      const colorOverrides = { ...state.colorOverrides, ...(ev.agent_colors || {}) };
      for (const a of ev.agent_profiles || []) {
        const profile = profileFromEvent(a as AgentProfileEvent);
        agentProfiles[profile.key] = profile;
        agentMessages[profile.key] = [];
        agentOrder.push(profile.key);
      }
      const item: ChatItem = {
        id: `conv-start-${Date.now()}`,
        itemType: 'q-start',
        time: ev.time || '',
        label: 'CONVERSATION',
        body: ev.question,
      };
      return {
        ...state,
        sessionTimeout: 60,
        connectionStatus: 'live',
        agentProfiles,
        agentMessages,
        agentOrder,
        colorOverrides,
        chatItems: appendChat(state, item),
        orchestrator: { ...state.orchestrator, state: 'running', max: ev.max_turns },
      };
    }

    case 'agent_speaking': {
      const filtered = state.chatItems.filter(c => c.id !== `think-${ev.agent}`);
      const item: ChatItem = {
        id: `think-${ev.agent}`,
        itemType: 'thinking',
        agentKey: ev.agent,
        displayName: ev.display_name,
        time: ev.time || '',
        body: 'thinking',
      };
      const speakerShort = ev.display_name.replace(/^The /, '').split('(')[0].trim();
      return {
        ...state,
        chatItems: [...filtered, item],
        urgencyStartTimes: { ...state.urgencyStartTimes, [ev.agent]: Date.now() },
        orchestrator: { ...state.orchestrator, state: 'thinking', speaker: speakerShort },
      };
    }

    case 'agent_spoke': {
      const filtered = state.chatItems.filter(c => c.id !== `think-${ev.agent}`);
      const mid = `m${state.msgIdCounter}`;
      const msgEntry: MsgStoreEntry = {
        agent: ev.agent,
        displayName: ev.display_name || ev.agent,
        turn: ev.turn,
        round: 'turn',
        question: ev.turn,
        systemPrompt: ev.system_prompt || '',
        payload: ev.user_payload || '',
        response: ev.response || '',
        elapsed: ev.elapsed,
      };
      const chatItem: ChatItem = {
        id: mid,
        itemType: 'message',
        agentKey: ev.agent,
        displayName: ev.display_name,
        time: ev.time || '',
        meta: `turn ${ev.turn} \u00B7 ${ev.elapsed}s \u00B7 ctx:${ev.context_messages || 0}`,
        body: ev.response || '',
        clickable: true,
      };
      const msgs = [...(state.agentMessages[ev.agent] || []), { text: ev.response, turn: ev.turn, elapsed: ev.elapsed }];
      return {
        ...state,
        chatItems: [...filtered, chatItem],
        msgStore: { ...state.msgStore, [mid]: msgEntry },
        agentMessages: { ...state.agentMessages, [ev.agent]: msgs },
        totalMessages: state.totalMessages + 1,
        msgIdCounter: state.msgIdCounter + 1,
        urgencyStartTimes: { ...state.urgencyStartTimes, [ev.agent]: null },
        orchestrator: { ...state.orchestrator, state: 'running', turn: ev.turn, speaker: '\u2014' },
      };
    }

    case 'turn_start':
      return {
        ...state,
        orchestrator: { ...state.orchestrator, state: 'running', turn: ev.turn, max: ev.max_turns },
      };

    case 'urgency_update': {
      // Keys other than type/time are agent keys with urgency values
      const entries = Object.entries(ev).filter(([k]) => k !== 'type' && k !== 'time');
      // We don't store urgency values in state since UrgencyBar uses startTime
      // But we can mark challenged agents
      let orch = state.orchestrator;
      for (const [, v] of entries) {
        if (typeof v === 'number' && v >= 0.5) {
          // Could mark challenged but original code does it via DOM
        }
      }
      return { ...state, orchestrator: orch };
    }

    case 'system_message': {
      const isChallenge = ev.message?.startsWith('Challenge detected:');
      const newChallenges = isChallenge
        ? state.orchestrator.challenges + 1
        : state.orchestrator.challenges;
      const item: ChatItem = {
        id: `sys-${Date.now()}`,
        itemType: isChallenge ? 'challenge' : 'system',
        time: ev.time || '',
        label: isChallenge ? 'CHALLENGE' : 'SYS',
        body: ev.message,
      };
      return {
        ...state,
        chatItems: appendChat(state, item),
        orchestrator: { ...state.orchestrator, challenges: newChallenges },
      };
    }

    case 'synthesis_update': {
      const body = `mood: ${ev.mood} \u00B7 exhaustion: ${ev.exhaustion}${ev.top_insight ? ' \u00B7 ' + ev.top_insight.substring(0, 120) : ''}`;
      const item: ChatItem = {
        id: `synth-upd-${Date.now()}`,
        itemType: 'synthesis',
        time: ev.time || '',
        label: `SYNTHESIS (turn ${ev.turn})`,
        body,
      };
      return { ...state, chatItems: appendChat(state, item) };
    }

    case 'conversation_done': {
      const item: ChatItem = {
        id: `conv-done-${Date.now()}`,
        itemType: 'ok',
        time: ev.time || '',
        label: 'CONVERSATION DONE',
        body: `${ev.turns} turns \u00B7 ${ev.elapsed}`,
      };
      return {
        ...state,
        chatItems: appendChat(state, item),
        orchestrator: { ...state.orchestrator, state: 'done', speaker: '\u2014' },
      };
    }

    case 'moderator_message':
      // Not handled — moderator messages are echoed locally before sending
      return state;

    default:
      return state;
  }
}
