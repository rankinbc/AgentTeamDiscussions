export async function sendModerator(message: string): Promise<void> {
  await fetch('/moderator', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  });
}

export async function addQuestion(text: string): Promise<void> {
  await fetch('/questions/add', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  });
}

export async function fetchLedger(): Promise<string> {
  const res = await fetch('/ledger');
  return res.text();
}

export interface BriefInfo {
  filename: string;
  name: string;
  content: string;
}

export interface AgentInfo {
  key: string;
  name: string;
  role: string;
  traits: Record<string, number>;
  drives: string[];
}

export async function fetchBriefs(): Promise<BriefInfo[]> {
  const res = await fetch('/api/briefs');
  return res.json();
}

export interface TeamInfo {
  name: string;
  displayName: string;
  agentCount: number;
  agents: string[];
  modes: string[];
  defaultMode: string;
}

export async function fetchAgents(): Promise<AgentInfo[]> {
  const res = await fetch('/api/agents');
  return res.json();
}

export async function fetchTeams(): Promise<TeamInfo[]> {
  const res = await fetch('/api/teams');
  return res.json();
}

export async function startSession(topic: string, agentKeys: string[], team?: string): Promise<{ status: string; title: string }> {
  const res = await fetch('/api/session/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ topic, agentKeys, team }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.error || 'Failed to start session');
  }
  return res.json();
}

export async function stopSession(): Promise<void> {
  const res = await fetch('/api/session/stop', { method: 'POST' });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.error || 'Failed to stop session');
  }
}
