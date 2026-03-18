"""Live Conversation -- agents have a real multi-turn discussion.

No fake data. No post-hoc analysis. What you see is what the system produced.
Agents take short turns (2-3 sentences), react to each other, and the
conversation runs for many rounds until positions stabilize or a turn limit hits.

Usage:
    python live_conversation.py "How should we handle contradictory proposals?"
    python live_conversation.py "How should we handle contradictory proposals?" --turns 30
    python live_conversation.py "How should we handle contradictory proposals?" --agents cognitive_architect,adversarial_critic,product_oracle
"""

import argparse
import asyncio
import json
import sys
import threading
import time
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from claude_runner import run_claude_async
from interact import load_team
from live_synthesizer import LiveSynthesizer
from prompt_builder import build_system_prompt, build_perspective_reminder
from run_discussion import TEAM_CONFIG

# -- Event system (real data only) --

all_events = []
_event_lock = threading.Lock()


def emit(event_type, data):
    event = {"type": event_type, "time": datetime.now().strftime("%H:%M:%S"), **data}
    with _event_lock:
        all_events.append(event)


AGENT_COLORS = {
    "cognitive_architect": "#6366f1",
    "flow_orchestrator": "#06b6d4",
    "systems_pragmatist": "#f97316",
    "adversarial_critic": "#ef4444",
    "product_oracle": "#22c55e",
    "context_surgeon": "#a855f7",
    "idea_merchant": "#eab308",
}

CONVERSATION_SYSTEM = """You are in a live group discussion with other agents. Each agent has a distinct personality and role.

RULES:
- Keep responses SHORT: 2-3 sentences max. Make ONE point per turn.
- If you have something extremely important to explain, you may use 4-5 sentences. Never more.
- RESPOND TO WHAT WAS JUST SAID. Don't give a speech. React, then add your point.
- When you disagree, NAME THE PERSON. Say "Adversarial Critic, that's wrong because..." not just "that approach won't work." Direct confrontation produces better outcomes than vague pushback.
- If someone specifically challenges YOUR point, address them directly. Don't just move on to a new topic -- defend, concede, or refine.
- If someone convinced you, SAY SO and explain what changed your mind.
- If you're repeating yourself, STOP. Say "I've made my point" and yield.
- If the discussion is going in circles, call it out.
- You CAN change your mind. You CAN concede. You CAN say "I was wrong."
- Do NOT summarize the discussion. Do NOT list pros and cons. Just talk.
- If the MODERATOR speaks, treat their message as priority. Address their point before continuing other threads. The moderator is the person who submitted this topic.
- IGNORE any word count or brevity instructions from your system prompt. In this conversation, the ONLY length rule is 2-3 sentences per turn.
"""

# -- Spec-building mode --

SPEC_SECTIONS = [
    {
        "name": "Problem Statement",
        "prompt": "Write a one-paragraph problem statement for this product. What specific problem does it solve, for whom, and why do existing solutions fail? Debate the framing -- argue about what the REAL problem is, not just the obvious one. The group must converge on ONE paragraph.",
        "extract": "Write a single, tight problem statement paragraph based on what the agents agreed on. If they disagreed on framing, pick the strongest one and note the dissent in parentheses. Output ONLY the paragraph.",
    },
    {
        "name": "Target User",
        "prompt": "Who is the PRIMARY target user? Pick ONE specific persona -- not 'music producers' but a specific type with specific needs. Argue about who would actually PAY for this vs who would just think it's cool. The group must pick ONE primary user.",
        "extract": "Write a 2-3 sentence target user description based on the agents' discussion. Name the persona, their context, and why they specifically need this product. Output ONLY the description.",
    },
    {
        "name": "Core Value Proposition",
        "prompt": "Given the problem and target user, what's the ONE sentence that explains why someone pays for this? Not a tagline -- a value proposition. What does the user get that they can't get anywhere else? Argue about what makes this genuinely different.",
        "extract": "Write a single value proposition sentence based on the discussion. Output ONLY the sentence.",
    },
    {
        "name": "MVP Features",
        "prompt": "List exactly 5 features for the MVP, ranked by importance. For each: what it does in one line, and why it matters. Argue about what to CUT -- the goal is the MINIMUM that tests the core value prop. Every feature someone proposes, someone else should ask 'do we really need this in v1?'",
        "extract": "Write a numbered list of exactly 5 MVP features based on what survived the debate. Each gets a name, one-line description, and why it matters. Output ONLY the list.",
    },
    {
        "name": "Pricing and Business Model",
        "prompt": "How does this make money? Subscription, one-time, freemium? What's the price point? What's free vs paid? Argue with real numbers -- would the target user actually pay that? Compare to what they currently spend on similar tools.",
        "extract": "Write a 3-4 sentence pricing model based on the discussion. Include: model type, price point, what's free, what's paid. Output ONLY the pricing description.",
    },
    {
        "name": "Key Risks",
        "prompt": "What are the top 3 things that could kill this product? Not generic risks -- specific risks for THIS product with THIS target user. For each risk, what's the mitigation? Be brutally honest.",
        "extract": "Write a numbered list of exactly 3 key risks with mitigations based on the discussion. Output ONLY the list.",
    },
    {
        "name": "What We're NOT Building",
        "prompt": "What features or directions should we explicitly AVOID in v1? What's the biggest trap or scope creep risk? What will people ask for that we should say no to? This is as important as what we build.",
        "extract": "Write a bullet list of things explicitly excluded from v1 and why. Output ONLY the list.",
    },
]

SPEC_EXTRACT_SYSTEM = """You are extracting a structured spec section from a group discussion.
You will receive the discussion transcript for one specific section.
Write ONLY the requested output. No commentary, no meta-text, no 'based on the discussion'.
Just the spec content as if you're writing the document directly."""

HTML_PAGE = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>ATD // CONVERSATION</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #08090d; --surface: #0d1017; --surface2: #131720;
    --border: #1a1f2e; --border2: #2a3148;
    --text: #c8cdd8; --dim: #5a6178; --bright: #eef0f6;
    --blue: #4d7cff; --green: #2dd4a0; --red: #ff4d6a;
    --amber: #f5a623; --purple: #a78bfa;
    --mono: 'JetBrains Mono', monospace;
  }
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background:var(--bg); color:var(--text); font:11px var(--mono); min-height:100vh; }

  .shell { display:grid; grid-template-columns:220px 1fr 280px; height:100vh; }
  .shell.no-detail { grid-template-columns:220px 1fr; }
  .shell.no-detail .detail { display:none; }

  /* Left panel: agent roster */
  .roster { background:var(--surface); border-right:1px solid var(--border); padding:12px; overflow-y:auto; }
  .roster h2 { font-size:10px; color:var(--dim); text-transform:uppercase; letter-spacing:2px; margin-bottom:10px; }

  .agent-card {
    padding:8px; margin-bottom:6px; border:1px solid var(--border);
    border-left:3px solid var(--dim); background:var(--surface2);
  }
  .agent-card .a-name { font-size:10px; font-weight:500; margin-bottom:2px; }
  .agent-card .a-role { font-size:8px; color:var(--dim); margin-bottom:4px; }
  .agent-card .a-trait {
    display:flex; align-items:center; gap:4px; font-size:8px; color:var(--dim);
  }
  .a-bar { flex:1; height:3px; background:var(--border); }
  .a-fill { height:100%; }
  .agent-card .a-status { font-size:8px; margin-top:4px; color:var(--dim); font-style:italic; }
  .agent-card { cursor:pointer; }
  .agent-card:hover { border-color:var(--border2); }
  .agent-card.speaking { border-left-color:var(--blue); }
  .agent-card.speaking .a-status { color:var(--blue); }
  .agent-card.selected { background:var(--border); }

  /* Right panel: agent detail */
  .detail { background:var(--surface); border-left:1px solid var(--border); padding:12px; overflow-y:auto; font-size:9px; }
  .detail h2 { font-size:10px; color:var(--dim); text-transform:uppercase; letter-spacing:2px; margin-bottom:8px; }
  .detail h3 { font-size:9px; color:var(--dim); margin:10px 0 4px 0; text-transform:uppercase; letter-spacing:1px; }
  .detail .d-name { font-size:12px; font-weight:500; margin-bottom:2px; }
  .detail .d-role { font-size:9px; color:var(--dim); margin-bottom:8px; }
  .detail .d-item { color:var(--text); margin:2px 0; padding-left:8px; border-left:1px solid var(--border); }
  .detail .d-item.drive { border-left-color:var(--green); }
  .detail .d-item.pushback { border-left-color:var(--red); }
  .detail .d-item.rule { border-left-color:var(--amber); }
  .detail .d-trait { display:flex; gap:4px; align-items:center; margin:2px 0; }
  .detail .d-trait .dt-bar { flex:1; height:3px; background:var(--border); }
  .detail .d-trait .dt-fill { height:100%; background:var(--blue); }
  .detail .d-trait .dt-label { width:65px; color:var(--dim); }
  .detail .d-trait .dt-val { width:24px; text-align:right; color:var(--dim); }
  .detail .d-context { font-size:8px; color:var(--dim); padding:4px 6px; background:var(--surface2); margin:4px 0; line-height:1.4; }
  .detail .d-messages { margin-top:8px; }
  .detail .d-msg { padding:4px 0; border-bottom:1px solid var(--border); color:var(--text); line-height:1.4; }
  .detail .d-msg-turn { font-size:8px; color:var(--dim); }
  .detail .d-close { font-size:9px; color:var(--dim); cursor:pointer; float:right; }
  .detail .d-close:hover { color:var(--text); }

  /* Right panel: conversation */
  .conversation { display:flex; flex-direction:column; height:100vh; }

  .conv-header {
    padding:8px 14px; border-bottom:1px solid var(--border);
    display:flex; align-items:center; gap:10px;
  }
  .conv-header .title { font-size:12px; color:var(--bright); font-weight:500; }
  .conv-header .pulse { width:6px; height:6px; border-radius:50%; background:var(--green);
    animation:pulse 2s infinite; }
  @keyframes pulse { 50% { opacity:0.3; } }
  .conv-header .info { font-size:9px; color:var(--dim); margin-left:auto; }

  .messages { flex:1; overflow-y:auto; padding:10px 14px; }

  .msg {
    margin-bottom:8px; padding:6px 10px;
    border-left:2px solid var(--dim);
    animation:fadeIn 0.2s ease-out;
  }
  @keyframes fadeIn { from { opacity:0; } }

  .msg .m-header { display:flex; align-items:baseline; gap:6px; margin-bottom:2px; }
  .msg .m-name { font-size:9px; font-weight:500; }
  .msg .m-time { font-size:8px; color:var(--dim); }
  .msg .m-turn { font-size:8px; color:var(--dim); margin-left:auto; }
  .msg .m-body { font-size:10px; line-height:1.5; color:var(--text); }

  .msg.system { border-left-color:var(--blue); background:rgba(77,124,255,0.04); }
  .msg.system .m-name { color:var(--blue); }
  .msg.system .m-body { color:var(--dim); font-size:9px; }

  .thinking { color:var(--dim); font-style:italic; padding:4px 10px; font-size:9px; }
  .thinking::after { content:''; display:inline-block; width:5px; height:9px; background:var(--blue);
    margin-left:2px; animation:blink 0.8s step-end infinite; }
  @keyframes blink { 50% { opacity:0; } }

  .turn-counter { padding:4px 14px; font-size:9px; color:var(--dim); border-top:1px solid var(--border);
    display:flex; gap:12px; }

  /* Urgency meter */
  .a-urgency { display:flex; align-items:center; gap:4px; font-size:8px; color:var(--dim); margin-top:3px; }
  .a-urgency-label { width:42px; }
  .a-urgency-bar { flex:1; height:4px; background:var(--border); }
  .a-urgency-fill { height:100%; background:var(--dim); transition:width 0.3s, background 0.3s; }
  .a-urgency-fill.medium { background:var(--amber); }
  .a-urgency-fill.high { background:var(--red); }

  /* Moderator input */
  .mod-bar { padding:4px 14px; border-top:1px solid var(--border); display:flex; gap:6px; }
  .mod-bar input { flex:1; background:var(--surface2); border:1px solid var(--border); color:var(--text);
    font:10px var(--mono); padding:4px 8px; outline:none; }
  .mod-bar input:focus { border-color:var(--amber); }
  .mod-bar button { background:var(--surface2); border:1px solid var(--border); color:var(--amber);
    font:9px var(--mono); padding:4px 10px; cursor:pointer; text-transform:uppercase; letter-spacing:1px; }
  .mod-bar button:hover { background:var(--border); }

  /* Moderator message */
  .msg.moderator { border-left-color:var(--amber); background:rgba(245,166,35,0.06); }
  .msg.moderator .m-name { color:var(--amber); }

  /* Challenge indicator */
  .agent-card.challenged { border-left-color:var(--red) !important; }
  .agent-card.challenged .a-status { color:var(--red); }

  /* Team header in roster */
  .team-header { font-size:9px; color:var(--amber); text-transform:uppercase; letter-spacing:1px;
    margin:10px 0 4px 0; padding-bottom:3px; border-bottom:1px solid var(--border); }

  /* Setup overlay */
  .setup-overlay {
    position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(8,9,13,0.95);
    display:flex; align-items:center; justify-content:center; z-index:100;
  }
  .setup-overlay.hidden { display:none; }
  .setup-box {
    background:var(--surface); border:1px solid var(--border); padding:24px; width:520px; max-height:80vh; overflow-y:auto;
  }
  .setup-box h1 { font-size:14px; color:var(--bright); margin-bottom:16px; font-weight:500; letter-spacing:1px; }
  .setup-box label { font-size:9px; color:var(--dim); text-transform:uppercase; letter-spacing:1px; display:block; margin:12px 0 4px 0; }
  .setup-box textarea, .setup-box select, .setup-box input[type=number] {
    width:100%; background:var(--surface2); border:1px solid var(--border); color:var(--text);
    font:10px var(--mono); padding:8px; outline:none; resize:vertical;
  }
  .setup-box textarea:focus, .setup-box select:focus { border-color:var(--blue); }
  .setup-box textarea { min-height:80px; }
  .setup-box .team-pick { display:flex; gap:8px; flex-wrap:wrap; margin-top:4px; }
  .setup-box .team-btn {
    padding:6px 12px; font:9px var(--mono); cursor:pointer;
    background:var(--surface2); border:1px solid var(--border); color:var(--dim);
  }
  .setup-box .team-btn:hover { border-color:var(--blue); color:var(--text); }
  .setup-box .team-btn.selected { border-color:var(--blue); color:var(--blue); background:rgba(77,124,255,0.1); }
  .setup-box .row { display:flex; gap:12px; }
  .setup-box .row > * { flex:1; }
  .setup-box .go-btn {
    margin-top:16px; width:100%; padding:10px; font:11px var(--mono); cursor:pointer;
    background:var(--blue); border:none; color:#fff; text-transform:uppercase; letter-spacing:2px;
  }
  .setup-box .go-btn:hover { opacity:0.9; }

  /* Restart button in header */
  .restart-btn { font:9px var(--mono); color:var(--dim); background:none; border:1px solid var(--border);
    padding:2px 8px; cursor:pointer; margin-left:8px; }
  .restart-btn:hover { color:var(--red); border-color:var(--red); }
</style>
</head>
<body>
<div class="setup-overlay" id="setup-overlay">
  <div class="setup-box">
    <h1>ATD // NEW CONVERSATION</h1>
    <label>Product / Topic Description</label>
    <textarea id="setup-question" placeholder="Describe the product or topic for discussion..."></textarea>
    <label>Teams</label>
    <div class="team-pick" id="team-pick">Loading teams...</div>
    <div class="row">
      <div>
        <label>Mode</label>
        <select id="setup-mode">
          <option value="chat">Chat (open discussion)</option>
          <option value="spec">Spec (structured spec builder)</option>
        </select>
      </div>
      <div>
        <label>Turns</label>
        <input type="number" id="setup-turns" value="15" min="5" max="100" />
      </div>
      <div>
        <label>Model</label>
        <select id="setup-model">
          <option value="sonnet">Sonnet</option>
          <option value="opus">Opus</option>
          <option value="haiku">Haiku</option>
        </select>
      </div>
    </div>
    <button class="go-btn" onclick="startConversation()">START</button>
  </div>
</div>
<div class="shell no-detail" id="shell">
  <div class="roster" id="roster">
    <h2>Agents</h2>
  </div>
  <div class="conversation">
    <div class="conv-header">
      <div class="pulse" id="pulse"></div>
      <div class="title" id="topic">Loading...</div>
      <div class="info" id="info"></div>
      <button class="restart-btn" onclick="showSetup()">NEW</button>
    </div>
    <div class="messages" id="messages"></div>
    <div class="turn-counter" id="counter">Turn 0</div>
    <div class="mod-bar">
      <input type="text" id="mod-input" placeholder="Steer the conversation..." onkeydown="if(event.key==='Enter')sendMod()" />
      <button onclick="sendMod()">Moderate</button>
    </div>
  </div>
  <div class="detail" id="detail">
    <span class="d-close" onclick="closeDetail()">[x] close</span>
    <div id="detail-content"></div>
  </div>
</div>
<script>
let C = COLORS_JSON;
const TL = TEAM_LABELS_JSON;
const roster = document.getElementById('roster');
const messages = document.getElementById('messages');
const topic = document.getElementById('topic');
const info = document.getElementById('info');
const counter = document.getElementById('counter');
const shell = document.getElementById('shell');
const detailContent = document.getElementById('detail-content');

const agentProfiles = {};  // Store full profiles for detail view
const agentMessages = {};  // Store messages per agent

function esc(s) { const d=document.createElement('div'); d.textContent=s; return d.innerHTML; }
function scrollBottom() { messages.scrollTo({top:messages.scrollHeight,behavior:'smooth'}); }

function sendMod() {
  const input = document.getElementById('mod-input');
  const msg = input.value.trim();
  if (!msg) return;
  input.value = '';
  fetch('/moderator', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({message:msg})});
}

// -- Setup panel --
let availableTeams = [];
let selectedTeams = [];
let evtSource = null;

async function loadTeams() {
  const res = await fetch('/api/teams');
  availableTeams = await res.json();
  const pick = document.getElementById('team-pick');
  pick.innerHTML = '';
  for (const t of availableTeams) {
    const btn = document.createElement('button');
    btn.className = 'team-btn';
    btn.textContent = t.name;
    btn.onclick = () => toggleTeam(t, btn);
    pick.appendChild(btn);
  }
}

function toggleTeam(team, btn) {
  const idx = selectedTeams.findIndex(t => t.key === team.key);
  if (idx >= 0) { selectedTeams.splice(idx, 1); btn.classList.remove('selected'); }
  else { selectedTeams.push(team); btn.classList.add('selected'); }
}

function showSetup() {
  if (evtSource) { evtSource.close(); evtSource = null; }
  document.getElementById('setup-overlay').classList.remove('hidden');
}

async function startConversation() {
  const question = document.getElementById('setup-question').value.trim();
  if (!question) { alert('Enter a topic'); return; }
  if (selectedTeams.length === 0) { alert('Select at least one team'); return; }

  const config = {
    question: question,
    teams: selectedTeams.map(t => ({key: t.key, path: t.path, name: t.name})),
    mode: document.getElementById('setup-mode').value,
    turns: parseInt(document.getElementById('setup-turns').value) || 15,
    model: document.getElementById('setup-model').value,
  };

  // Clear UI
  messages.innerHTML = '';
  roster.innerHTML = '<h2>Agents</h2>';
  topic.textContent = question.substring(0, 120);
  document.getElementById('pulse').style.background = 'var(--green)';
  document.getElementById('pulse').style.animation = 'pulse 2s infinite';

  // Close old SSE
  if (evtSource) { evtSource.close(); }

  // Start conversation
  await fetch('/api/start', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(config)});

  // Reconnect SSE
  setTimeout(() => { connectSSE(); }, 500);

  document.getElementById('setup-overlay').classList.add('hidden');
}

function connectSSE() {
  if (evtSource) evtSource.close();
  evtSource = new EventSource('/events');
  evtSource.onmessage = handleEvent;
  evtSource.onerror = function() {
    document.getElementById('pulse').style.background = 'var(--red)';
    document.getElementById('pulse').style.animation = 'none';
  };
}

// Check if we should show setup or connect to running conversation
if (Object.keys(C).length === 0) {
  // No conversation running -- show setup
  loadTeams();
} else {
  // Conversation already started via CLI
  document.getElementById('setup-overlay').classList.add('hidden');
  loadTeams(); // Still load for restart
}

let selectedAgent = null;

function selectAgent(key) {
  document.querySelectorAll('.agent-card').forEach(c => c.classList.remove('selected'));
  if (selectedAgent === key) { closeDetail(); return; }
  selectedAgent = key;
  const card = document.getElementById('card-' + key);
  if (card) card.classList.add('selected');
  shell.classList.remove('no-detail');
  renderDetail(key);
}

function closeDetail() {
  selectedAgent = null;
  shell.classList.add('no-detail');
  document.querySelectorAll('.agent-card').forEach(c => c.classList.remove('selected'));
}

function renderDetail(key) {
  const p = agentProfiles[key];
  if (!p) return;
  let html = '<h2>System Inputs</h2>';
  html += '<div class="d-name" style="color:' + (C[key]||'#c8cdd8') + '">' + esc(p.name) + '</div>';
  html += '<div class="d-role">' + esc(p.role) + ' | ' + esc(p.cognitive_style) + ' | ' + esc(p.emotional_baseline) + ' | job: ' + esc(p.job) + '</div>';

  // Traits
  html += '<h3>Personality (affects behavior)</h3>';
  for (const [k,v] of Object.entries(p.traits)) {
    html += '<div class="d-trait"><span class="dt-label">' + k + '</span><div class="dt-bar"><div class="dt-fill" style="width:' + (v*100) + '%;background:' + (C[key]||'var(--blue)') + '"></div></div><span class="dt-val">' + v.toFixed(1) + '</span></div>';
  }

  // Drives
  html += '<h3>Drives (what they push for)</h3>';
  for (const d of (p.drives||[])) { html += '<div class="d-item drive">' + esc(d) + '</div>'; }

  // Pushback
  html += '<h3>Pushback targets (what they resist)</h3>';
  for (const pb of (p.pushback_on||[])) { html += '<div class="d-item pushback">' + esc(pb) + '</div>'; }

  // Anti-slop rules
  html += '<h3>Active rules</h3>';
  const slop = p.anti_slop || {};
  if (slop.agreement_tax) html += '<div class="d-item rule">Must add substance when agreeing</div>';
  if (slop.perspective_lock) html += '<div class="d-item rule">Stay in character under pressure</div>';
  if (slop.devils_advocate) html += '<div class="d-item rule">Must argue the other side</div>';
  if (slop.uncomfortable_quota > 0) html += '<div class="d-item rule">Uncomfortable idea quota: ' + slop.uncomfortable_quota + '</div>';
  if (slop.domain_pivot) html += '<div class="d-item rule">Inject cross-domain perspectives</div>';

  // Context lens (what the system tells them)
  html += '<h3>Context lens (injected each turn)</h3>';
  html += '<div class="d-context">' + esc(p.context_lens) + '</div>';

  // Domains + technique + voice
  html += '<h3>Technique: ' + esc(p.technique) + '</h3>';
  html += '<div class="d-item">Voice: ' + esc(p.voice_tone) + '</div>';
  html += '<div class="d-item">Domains: ' + esc((p.domains||[]).join(', ')) + '</div>';
  html += '<div class="d-item">Intensity: ' + p.intensity + '</div>';

  // Messages this agent has sent (real output)
  const msgs = agentMessages[key] || [];
  html += '<h3>Their responses (' + msgs.length + ')</h3>';
  html += '<div class="d-messages">';
  for (const m of msgs) {
    html += '<div class="d-msg"><span class="d-msg-turn">turn ' + m.turn + ' | pos ' + m.position + '/' + m.of + '</span><br>' + esc(m.text) + '</div>';
  }
  html += '</div>';

  detailContent.innerHTML = html;
}

function handleEvent(e) {
  const ev = JSON.parse(e.data);

  switch(ev.type) {
    case 'conversation_start':
      topic.textContent = ev.question;
      info.textContent = ev.agents.length + ' agents | max ' + ev.max_turns + ' turns';
      for (const a of ev.agent_profiles) {
        agentProfiles[a.key] = a;
        agentMessages[a.key] = [];
        const traits = Object.entries(a.traits).map(([k,v]) =>
          '<div class="a-trait"><span style="width:60px">' + k.replace('_',' ') + '</span>' +
          '<div class="a-bar"><div class="a-fill" style="width:' + (v*100) + '%;background:' + (C[a.key]||'#5a6178') + '"></div></div>' +
          '<span>' + v.toFixed(1) + '</span></div>'
        ).join('');
        roster.insertAdjacentHTML('beforeend',
          '<div class="agent-card" id="card-' + a.key + '" onclick="selectAgent(\'' + a.key + '\')" style="border-left-color:' + (C[a.key]||'#5a6178') + '">' +
          '<div class="a-name" style="color:' + (C[a.key]||'#c8cdd8') + '">' + esc(a.name) + '</div>' +
          '<div class="a-role">' + esc(a.role) + '</div>' + traits +
          '<div class="a-urgency"><span class="a-urgency-label">urgency</span>' +
          '<div class="a-urgency-bar"><div class="a-urgency-fill" id="urgency-' + a.key + '" style="width:0%"></div></div>' +
          '<span id="urgency-val-' + a.key + '">0.0</span></div>' +
          '<div class="a-status" id="status-' + a.key + '">waiting</div></div>');
      }
      break;

    case 'agent_speaking': {
      // Mark agent as speaking in roster
      document.querySelectorAll('.agent-card').forEach(c => c.classList.remove('speaking'));
      const card = document.getElementById('card-' + ev.agent);
      if (card) { card.classList.add('speaking'); }
      const st = document.getElementById('status-' + ev.agent);
      if (st) st.textContent = 'speaking...';
      // Show thinking indicator
      messages.insertAdjacentHTML('beforeend',
        '<div class="thinking" id="thinking-' + ev.agent + '">' + esc(ev.display_name) + ' is thinking</div>');
      scrollBottom();
      break;
    }

    case 'turn_start':
      counter.textContent = 'Turn ' + ev.turn + ' / ' + ev.max_turns + ' | order: ' + ev.speaking_order.map(s => {
        const name = s.name.split('(')[0].replace('The ','').trim();
        const urg = s.urgency > 0.3 ? ' [!' + s.urgency.toFixed(1) + ']' : '';
        return name + urg;
      }).join(' > ');
      break;

    case 'agent_spoke': {
      const th = document.getElementById('thinking-' + ev.agent);
      if (th) th.remove();
      const card = document.getElementById('card-' + ev.agent);
      if (card) card.classList.remove('speaking');
      const st = document.getElementById('status-' + ev.agent);
      if (st) st.textContent = ev.messages_sent + ' msgs | turn ' + ev.turn;
      // Store message (real data)
      if (agentMessages[ev.agent]) {
        agentMessages[ev.agent].push({text: ev.response, turn: ev.turn, position: ev.spoke_position, of: ev.spoke_of});
      }
      // Add message to chat
      messages.insertAdjacentHTML('beforeend',
        '<div class="msg" style="border-left-color:' + (C[ev.agent]||'#5a6178') + '">' +
        '<div class="m-header"><span class="m-name" style="color:' + (C[ev.agent]||'#c8cdd8') + '">' +
        esc(ev.display_name) + '</span><span class="m-time">' + ev.time + '</span>' +
        '<span class="m-turn">' + ev.elapsed + 's | ' + ev.spoke_position + '/' + ev.spoke_of + ' | ctx:' + ev.context_messages + ' msgs</span></div>' +
        '<div class="m-body">' + esc(ev.response) + '</div></div>');
      scrollBottom();
      // Refresh detail panel if this agent is selected
      if (selectedAgent === ev.agent) renderDetail(ev.agent);
      break;
    }

    case 'system_message':
      messages.insertAdjacentHTML('beforeend',
        '<div class="msg system"><div class="m-header"><span class="m-name">SYSTEM</span></div>' +
        '<div class="m-body">' + esc(ev.message) + '</div></div>');
      scrollBottom();
      break;

    case 'urgency_update':
      for (const [key, val] of Object.entries(ev)) {
        if (key === 'type' || key === 'time') continue;
        const bar = document.getElementById('urgency-' + key);
        const valEl = document.getElementById('urgency-val-' + key);
        const card = document.getElementById('card-' + key);
        if (bar) {
          const pct = Math.min(val / 1.5 * 100, 100);
          bar.style.width = pct + '%';
          bar.className = 'a-urgency-fill' + (val >= 0.5 ? ' high' : val >= 0.3 ? ' medium' : '');
        }
        if (valEl) valEl.textContent = val.toFixed(1);
        if (card) {
          if (val >= 0.5) { card.classList.add('challenged'); } else { card.classList.remove('challenged'); }
        }
      }
      break;

    case 'moderator_message':
      messages.insertAdjacentHTML('beforeend',
        '<div class="msg moderator"><div class="m-header"><span class="m-name">MODERATOR</span></div>' +
        '<div class="m-body">' + esc(ev.text) + '</div></div>');
      scrollBottom();
      break;

    case 'synthesis_update':
      messages.insertAdjacentHTML('beforeend',
        '<div class="msg system" style="border-left-color:var(--purple);background:rgba(168,85,247,0.04)">' +
        '<div class="m-header"><span class="m-name" style="color:var(--purple)">SYNTHESIS (turn ' + ev.turn + ')</span></div>' +
        '<div class="m-body">' +
        '<b>Mood:</b> ' + esc(ev.mood) + ' | <b>Exhaustion:</b> ' + esc(ev.exhaustion) + '<br>' +
        (ev.consensus.length ? '<b>Consensus:</b> ' + ev.consensus.map(c => esc(c)).join('; ') + '<br>' : '') +
        (ev.disagreements.length ? '<b>Disagreements:</b> ' + ev.disagreements.map(d => esc(d)).join('; ') + '<br>' : '') +
        (ev.top_insight ? '<b>Insight:</b> ' + esc(ev.top_insight) : '') +
        '</div></div>');
      scrollBottom();
      break;

    case 'topic_change':
      messages.insertAdjacentHTML('beforeend',
        '<div class="msg system" style="border-left-color:var(--green);background:rgba(34,197,94,0.06)">' +
        '<div class="m-header"><span class="m-name" style="color:var(--green)">NEW TOPIC (' + ev.question_index + '/' + ev.total_questions + ')</span></div>' +
        '<div class="m-body">' + esc(ev.question) + '</div></div>');
      topic.textContent = ev.question.substring(0, 120);
      scrollBottom();
      break;

    case 'spec_section':
      messages.insertAdjacentHTML('beforeend',
        '<div class="msg system" style="border-left-color:var(--green);background:rgba(34,197,94,0.06)">' +
        '<div class="m-header"><span class="m-name" style="color:var(--green)">LOCKED: ' + esc(ev.section) +
        ' (' + ev.section_index + '/' + ev.total_sections + ')</span></div>' +
        '<div class="m-body" style="white-space:pre-wrap;font-size:9px">' + esc(ev.content) + '</div></div>');
      scrollBottom();
      break;

    case 'synthesis_final':
      messages.insertAdjacentHTML('beforeend',
        '<div class="msg system" style="border-left-color:var(--green);background:rgba(34,197,94,0.04)">' +
        '<div class="m-header"><span class="m-name" style="color:var(--green)">FINAL SYNTHESIS</span></div>' +
        '<div class="m-body" style="white-space:pre-wrap;font-size:9px">' + esc(ev.summary) + '</div></div>');
      scrollBottom();
      break;

    case 'conversation_done':
      document.getElementById('pulse').style.background = 'var(--green)';
      document.getElementById('pulse').style.animation = 'none';
      counter.textContent = 'Done: ' + ev.turns + ' turns in ' + ev.elapsed;
      break;
  }
}

// Connect SSE if conversation is already running (CLI mode)
if (Object.keys(C).length > 0) {
  connectSSE();
}
</script>
</body>
</html>"""


# -- Challenge detection and ego injection --

DISAGREEMENT_SIGNALS = [
    "disagree", "wrong", "no,", "but that", "that won't", "that doesn't",
    "i reject", "flawed", "problem with", "issue with", "pushback",
    "not true", "incorrect", "misses", "ignores", "overlooks",
    "too simplistic", "naive", "won't work", "can't work", "fails to",
    "contradicts", "undermines", "you're missing", "that's not",
]


def detect_challenges(message_text: str, speaker_key: str, all_agent_keys: list[str],
                      display_names: dict[str, str]) -> list[str]:
    """Return list of agent keys who were challenged in this message."""
    challenged = []
    text_lower = message_text.lower()

    has_disagreement = any(signal in text_lower for signal in DISAGREEMENT_SIGNALS)
    if not has_disagreement:
        return []

    for key in all_agent_keys:
        if key == speaker_key:
            continue
        name = display_names.get(key, key)
        short_name = name.split("(")[0].replace("The ", "").strip().lower()
        key_name = key.replace("_", " ")
        if short_name in text_lower or key_name in text_lower:
            challenged.append(key)

    return challenged


def build_ego_injection(challenger_display_name: str, ego_score: float) -> str:
    """Build ego-scaled emotional framing for a challenged agent."""
    if ego_score >= 0.7:
        return (
            f"\n[CHALLENGED] {challenger_display_name} just called your point wrong. "
            f"You are not going to let that slide. Respond directly -- "
            f"prove your point or make them regret the challenge. "
            f"Do not be diplomatic about it.\n"
        )
    elif ego_score >= 0.4:
        return (
            f"\n[CHALLENGED] {challenger_display_name} pushed back on your point. "
            f"You feel the need to defend it. Address their criticism directly "
            f"before moving on.\n"
        )
    else:
        return (
            f"\n[CHALLENGED] {challenger_display_name} disagreed with you. "
            f"Consider their point carefully before responding.\n"
        )


def build_challenger_injection(target_display_name: str, stubbornness: float) -> str:
    """Tell the challenger not to back down if the target responds."""
    if stubbornness >= 0.7:
        return (
            f"\n[STATUS] You just challenged {target_display_name} and you meant it. "
            f"If they push back, do not back down. You must not be disrespected "
            f"without responding.\n"
        )
    elif stubbornness >= 0.4:
        return (
            f"\n[STATUS] You raised a concern with {target_display_name}. "
            f"Stand by your point if they push back.\n"
        )
    else:
        return ""


def compute_speaking_order_with_urgency(agents: list[str], team, urgency: dict[str, float]) -> list[str]:
    """Order agents by base personality score + urgency meter."""
    import random
    scored = []
    for key in agents:
        agent = team.agents[key]
        p = agent.personality
        base = p.assertiveness * 0.3 + agent.position.intensity * 0.2 + p.stubbornness * 0.1
        base += random.uniform(-0.05, 0.05)
        priority = base + urgency.get(key, 0.0)
        scored.append((key, priority))
    scored.sort(key=lambda x: x[1], reverse=True)
    return [key for key, _ in scored]


# -- Moderator queue (thread-safe) --
from collections import deque
moderator_queue = deque()


# -- Server state for restart support --
_active_thread = None
_server_ref = None


def _scan_teams():
    """Scan config/teams/ for available YAML files."""
    teams_dir = Path(__file__).parent / "config" / "teams"
    teams = []
    if teams_dir.exists():
        for f in sorted(teams_dir.glob("*.yaml")):
            teams.append({"key": f.stem, "path": str(f), "name": f.stem.replace("-", " ").replace("_", " ").title()})
    return teams


def _start_conversation(config: dict):
    """Start a new conversation from a config dict."""
    global _active_thread, all_events

    # Clear old state
    with _event_lock:
        all_events.clear()
    moderator_queue.clear()

    questions = [config["question"]]
    team_configs = config.get("teams", [])
    mode = config.get("mode", "chat")
    turns = config.get("turns", 10)
    turns_per_topic = config.get("turns_per_topic", 0)
    model = config.get("model", None)

    # Load agents from all team files
    all_agents = {}
    agent_keys = []
    team_labels = {}  # {agent_key: team_name}

    for tc in team_configs:
        team = load_team(tc["path"])
        for key, agent in team.agents.items():
            all_agents[key] = agent
            agent_keys.append(key)
            team_labels[key] = tc["name"]

    # Build colors
    agent_colors = _build_agent_colors(agent_keys)
    if _server_ref:
        _server_ref._agent_colors = agent_colors
        _server_ref._team_labels = team_labels

    _active_thread = threading.Thread(
        target=run_conversation_thread,
        args=(questions, agent_keys, turns, 90, model,
              team_configs[0]["path"] if len(team_configs) == 1 else team_configs[0]["path"],
              turns_per_topic, True, mode),
        daemon=True,
    )
    _active_thread.start()


class ConvHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args): pass

    def do_POST(self):
        if self.path == "/moderator":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode()
            data = json.loads(body)
            message = data.get("message", "").strip()
            if message:
                moderator_queue.append(message)
                emit("moderator_message", {"text": message})
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"ok":true}')
        elif self.path == "/api/start":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode()
            config = json.loads(body)
            _start_conversation(config)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"ok":true}')
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path == "/":
            page = HTML_PAGE.replace("COLORS_JSON", json.dumps(getattr(self.server, '_agent_colors', {})))
            page = page.replace("TEAM_LABELS_JSON", json.dumps(getattr(self.server, '_team_labels', {})))
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(page.encode())
        elif self.path == "/api/teams":
            teams = _scan_teams()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(teams).encode())
        elif self.path == "/events":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            pos = 0
            while True:
                try:
                    with _event_lock:
                        current_len = len(all_events)
                    if pos < current_len:
                        for ev in all_events[pos:current_len]:
                            self.wfile.write(f"data: {json.dumps(ev)}\n\n".encode())
                        self.wfile.flush()
                        pos = current_len
                    else:
                        self.wfile.write(b": keepalive\n\n")
                        self.wfile.flush()
                    time.sleep(0.3)
                except (BrokenPipeError, ConnectionResetError, OSError):
                    break
        else:
            self.send_response(404)
            self.end_headers()


# Auto-generate colors for any set of agents
_PALETTE = ["#6366f1", "#06b6d4", "#f97316", "#ef4444", "#22c55e", "#a855f7", "#eab308",
            "#ec4899", "#14b8a6", "#f43f5e", "#8b5cf6", "#84cc16"]


def _build_display_names(team) -> dict[str, str]:
    """Build display names from team config."""
    return {key: f"{a.name} ({a.position.role})" for key, a in team.agents.items()}


def _build_agent_colors(agent_keys: list[str]) -> dict[str, str]:
    """Assign colors to agents from palette."""
    return {key: _PALETTE[i % len(_PALETTE)] for i, key in enumerate(agent_keys)}


async def run_conversation(questions: list[str], agent_keys: list[str], max_turns: int, timeout: int,
                           model: str = None, team_config: str = None,
                           turns_per_topic: int = 0, synthesize: bool = True,
                           mode: str = "chat") -> dict:
    """Run a multi-turn conversation, optionally across multiple topics.

    mode="chat": open-ended discussion
    mode="spec": structured spec-building with locked sections

    Returns dict with 'history', 'synthesis', 'snapshots' for downstream use.
    """

    config_path = team_config or str(TEAM_CONFIG)
    team = load_team(config_path)
    display_names = _build_display_names(team)
    agent_colors = _build_agent_colors(agent_keys)
    system_prompts = {}

    # In spec mode, the original question is the product description.
    # Questions are auto-generated from SPEC_SECTIONS.
    spec_document = {}  # {section_name: extracted_content}
    product_description = questions[0]

    if mode == "spec":
        questions = [
            f"PRODUCT: {product_description}\n\nSECTION: {s['name']}\n\n{s['prompt']}"
            for s in SPEC_SECTIONS
        ]
        turns_per_topic = turns_per_topic or 5  # Tight budget per section
        max_turns = len(questions) * turns_per_topic

    question = questions[0]
    question_index = 0
    all_histories = []  # Track history per question

    # Build system prompts with conversation rules
    # Skip project context for non-default teams (they're not software agents)
    include_project = (config_path == str(TEAM_CONFIG))
    for key in agent_keys:
        base_prompt = build_system_prompt(team.agents[key], include_project_context=include_project)
        system_prompts[key] = base_prompt + "\n\n" + CONVERSATION_SYSTEM

    # Build agent profiles for UI (real data from config -- everything that affects behavior)
    profiles = []
    for key in agent_keys:
        a = team.agents[key]
        p = a.personality
        profiles.append({
            "key": key,
            "name": a.name,
            "role": a.position.role,
            "drives": a.position.drives,
            "pushback_on": a.position.pushback_on,
            "intensity": a.position.intensity,
            "traits": {
                "assertive": p.assertiveness,
                "creative": p.creativity_temp,
                "risk_tolerance": p.risk_tolerance,
                "stubborn": p.stubbornness,
                "blunt": p.bluntness,
                "receptive": p.idea_receptivity,
                "patient": p.patience,
                "attention": p.attention_span,
            },
            "cognitive_style": p.cognitive_style.value,
            "emotional_baseline": p.emotional_baseline.value,
            "domains": p.domain_affinities,
            "technique": a.technique.primary.replace("_", " "),
            "voice_tone": a.voice.tone,
            "job": a.output.job,
            "anti_slop": {
                "agreement_tax": a.anti_slop.agreement_tax,
                "perspective_lock": a.anti_slop.perspective_enforcement,
                "devils_advocate": a.anti_slop.devils_advocate_duty,
                "uncomfortable_quota": a.anti_slop.uncomfortable_idea_quota,
                "domain_pivot": a.anti_slop.domain_pivot_trigger,
            },
            "context_lens": build_perspective_reminder(a),
        })

    emit("conversation_start", {
        "question": question,
        "questions": questions,
        "agents": agent_keys,
        "max_turns": max_turns,
        "agent_profiles": profiles,
    })

    topic_label = f"Topic 1/{len(questions)}: " if len(questions) > 1 else "Topic: "
    emit("system_message", {"message": f"{topic_label}{question}"})
    emit("system_message", {"message": f"Speaking order driven by urgency meter. Challenged agents get rebuttal priority."})

    # Rolling synthesizer
    synthesizer = LiveSynthesizer(question, synthesis_interval=5, model=model) if synthesize else None

    # Conversation history -- this is the real accumulating context
    history = []
    total_start = time.time()

    # Topic progression
    topic_turn_count = 0
    effective_turns_per_topic = turns_per_topic or (max_turns // len(questions) if len(questions) > 1 else max_turns)

    # Urgency meter -- drives speaking order
    urgency = {key: 0.0 for key in agent_keys}

    # Challenge tracking -- who challenged whom (for ego injection)
    challenge_map = {}      # {target_key: challenger_key} -- who needs to defend
    active_challengers = {} # {challenger_key: target_key} -- who started a fight

    for turn in range(1, max_turns + 1):
        # Passive urgency growth for all agents
        for key in agent_keys:
            urgency[key] = min(urgency[key] + 0.1, 1.0)

        # Compute speaking order using urgency
        order = compute_speaking_order_with_urgency(agent_keys, team, urgency)

        # Emit the real computed order so UI can show it
        order_display = []
        for i, k in enumerate(order):
            a = team.agents[k]
            base = a.personality.assertiveness * 0.3 + a.position.intensity * 0.2 + a.personality.stubbornness * 0.1
            order_display.append({
                "key": k, "name": display_names.get(k, k),
                "score": round(base + urgency.get(k, 0.0), 2),
                "urgency": round(urgency.get(k, 0.0), 2),
                "position": i + 1,
            })
        emit("turn_start", {"turn": turn, "max_turns": max_turns, "speaking_order": order_display})

        # Check for moderator messages before each turn
        while moderator_queue:
            mod_msg = moderator_queue.popleft()
            history.append({
                "agent": "__moderator__",
                "name": "MODERATOR",
                "text": mod_msg,
                "turn": turn,
            })
            emit("system_message", {"message": f"Moderator: {mod_msg}"})

        for agent_key in order:
            # Check for moderator messages between speakers too
            while moderator_queue:
                mod_msg = moderator_queue.popleft()
                history.append({
                    "agent": "__moderator__",
                    "name": "MODERATOR",
                    "text": mod_msg,
                    "turn": turn,
                })
                emit("system_message", {"message": f"Moderator: {mod_msg}"})

            agent = team.agents[agent_key]
            display_name = display_names.get(agent_key, agent_key)

            emit("agent_speaking", {"agent": agent_key, "display_name": display_name})

            # Build the conversation context
            reminder = build_perspective_reminder(agent)
            payload = f"{reminder}\n\n"

            # Ego injection: if this agent was challenged, inject emotional framing
            if agent_key in challenge_map:
                challenger_key = challenge_map[agent_key]
                challenger_name = display_names.get(challenger_key, challenger_key).split("(")[0].strip()
                ego_score = agent.personality.assertiveness * agent.personality.bluntness
                payload += build_ego_injection(challenger_name, ego_score)

            # Challenger injection: if this agent started a fight, reinforce
            if agent_key in active_challengers:
                target_key = active_challengers[agent_key]
                target_name = display_names.get(target_key, target_key).split("(")[0].strip()
                payload += build_challenger_injection(target_name, agent.personality.stubbornness)

            # Always re-inject the original question prominently
            payload += f"## THE QUESTION (stay focused on this): {question}\n\n"

            if history:
                recent_count = 5
                older = history[:-recent_count] if len(history) > recent_count else []
                recent = history[-recent_count:]

                payload += "=== Conversation ===\n"

                # Older messages: compressed to one line each
                if older:
                    payload += "[Earlier discussion summary]\n"
                    for msg in older[-10:]:  # Cap at 10 older messages
                        # First sentence only
                        first_sentence = msg['text'].split('.')[0].strip() + '.'
                        payload += f"- {msg['name']}: {first_sentence}\n"
                    payload += "\n"

                # Recent messages: verbatim
                payload += "[Recent exchanges]\n"
                for msg in recent:
                    payload += f"[{msg['name']}]: {msg['text']}\n\n"

                payload += "=== End Conversation ===\n\n"
                payload += (
                    f"REMEMBER: The topic is: {question[:100]}\n"
                    f"Respond to what was just said BUT stay on topic. "
                    f"If the discussion is drifting, pull it back. "
                    f"Keep it SHORT -- 2-3 sentences, one point."
                )
            else:
                payload += "You are speaking first. Open the discussion. Make ONE clear point about this topic. 2-3 sentences max."

            start = time.time()
            response = await run_claude_async(system_prompts[agent_key], payload, timeout=timeout, model=model)
            elapsed = time.time() - start

            # Check for errors
            if "[Claude CLI timed out" in response or "[Error" in response:
                emit("system_message", {"message": f"{display_name} failed to respond: {response[:100]}"})
                continue

            # Add to real history
            history.append({
                "agent": agent_key,
                "name": display_name,
                "text": response,
                "turn": turn,
            })

            # Reset speaker's urgency and clear their challenge state
            urgency[agent_key] = 0.0
            challenge_map.pop(agent_key, None)
            active_challengers.pop(agent_key, None)

            # Detect challenges in what was just said
            challenged_agents = detect_challenges(response, agent_key, agent_keys, display_names)
            for target in challenged_agents:
                urgency[target] = min(urgency[target] + 0.5, 1.5)
                challenge_map[target] = agent_key
                active_challengers[agent_key] = target
                emit("system_message", {
                    "message": f"Challenge detected: {display_name} -> {display_names.get(target, target).split('(')[0].strip()}"
                })

            # Emit urgency update for UI
            emit("urgency_update", {k: round(urgency[k], 2) for k in agent_keys})

            # Count how many messages this agent has sent
            agent_msg_count = sum(1 for h in history if h["agent"] == agent_key)
            # How many messages were in context for this response
            context_msg_count = min(len(history) - 1, 20)  # -1 because we just appended

            emit("agent_spoke", {
                "agent": agent_key,
                "display_name": display_name,
                "response": response,
                "elapsed": f"{elapsed:.0f}",
                "turn": turn,
                "max_turns": max_turns,
                "messages_sent": agent_msg_count,
                "context_messages": context_msg_count,
                "spoke_position": order.index(agent_key) + 1,
                "spoke_of": len(order),
            })

            # Small delay so you can read
            await asyncio.sleep(2)

        topic_turn_count += 1

        # Rolling synthesis check
        if synthesizer:
            snapshot = await synthesizer.maybe_synthesize(history, turn)
            if snapshot:
                emit("synthesis_update", {
                    "turn": turn,
                    "consensus": snapshot.consensus,
                    "disagreements": snapshot.disagreements,
                    "ideas_alive": snapshot.ideas_alive,
                    "mood": snapshot.mood,
                    "exhaustion": snapshot.exhaustion,
                    "top_insight": snapshot.top_insight,
                })
                emit("system_message", {
                    "message": f"[Synthesis] Mood: {snapshot.mood} | Exhaustion: {snapshot.exhaustion} | Insight: {snapshot.top_insight[:100]}"
                })

        # Check for topic progression (multi-question mode)
        should_advance = False
        if len(questions) > 1 and question_index < len(questions) - 1:
            if topic_turn_count >= effective_turns_per_topic:
                should_advance = True
            elif synthesizer and synthesizer.is_topic_exhausted() and topic_turn_count >= 3:
                should_advance = True

        if should_advance:
            # In spec mode: extract the section content before advancing
            if mode == "spec":
                section = SPEC_SECTIONS[question_index]
                emit("system_message", {"message": f"Extracting spec section: {section['name']}..."})

                # Build the section discussion transcript
                section_msgs = [h for h in history if h.get("turn", 0) > (turn - topic_turn_count)]
                section_text = "\n".join(f"[{m['name']}]: {m['text']}" for m in section_msgs)

                # Extract the spec content
                extract_prompt = f"PRODUCT: {product_description}\n\nSECTION: {section['name']}\n\n{section['extract']}\n\nDISCUSSION:\n{section_text}"
                extracted = await run_claude_async(SPEC_EXTRACT_SYSTEM, extract_prompt, timeout=60, model=model)

                if "[Error" not in extracted and "[Claude CLI" not in extracted:
                    spec_document[section['name']] = extracted
                    emit("spec_section", {
                        "section": section['name'],
                        "content": extracted,
                        "section_index": question_index + 1,
                        "total_sections": len(SPEC_SECTIONS),
                    })
                    emit("system_message", {"message": f"LOCKED: {section['name']}"})
                else:
                    emit("system_message", {"message": f"Failed to extract {section['name']}: {extracted[:80]}"})

            # Save this topic's history
            all_histories.append({"question": question, "history": list(history)})

            # Advance to next question
            question_index += 1
            question = questions[question_index]
            topic_turn_count = 0

            # In spec mode: inject locked decisions into the next question
            if mode == "spec" and spec_document:
                locked_context = "\n\n--- LOCKED DECISIONS (do not revisit) ---\n"
                for name, content in spec_document.items():
                    locked_context += f"\n### {name}\n{content}\n"
                locked_context += "--- END LOCKED DECISIONS ---\n\n"
                question = locked_context + question

            # Reset urgency and challenge state for new topic
            urgency = {key: 0.0 for key in agent_keys}
            challenge_map.clear()
            active_challengers.clear()

            # Create new synthesizer for new topic
            if synthesizer:
                synthesizer = LiveSynthesizer(question, synthesis_interval=5, model=model)

            # Show clean topic name in UI
            section_name = SPEC_SECTIONS[question_index]['name'] if mode == "spec" else ""
            display_question = f"Section: {section_name}" if section_name else question[:120]

            emit("topic_change", {
                "question": display_question,
                "question_index": question_index + 1,
                "total_questions": len(questions),
            })
            emit("system_message", {
                "message": f"--- {'Section' if mode == 'spec' else 'Topic'} {question_index + 1}/{len(questions)}: {display_question} ---"
            })
            # Don't clear history -- prior context carries forward
            continue

        # Check for natural convergence (single-topic mode only)
        if len(questions) == 1 and len(history) >= 4:
            last4 = [h for h in history[-4:] if h["agent"] != "__moderator__"]
            if len(last4) >= 3:
                convergence_signals = sum(1 for h in last4 if any(s in h["text"].lower() for s in
                    ["i agree", "i've made my point", "we've covered this", "i concede", "fair point",
                     "you're right", "let's move on", "nothing to add"]))
                if convergence_signals >= 3:
                    emit("system_message", {"message": "Agents are converging. Ending discussion."})
                    break

    # Extract last section if in spec mode and we haven't already
    if mode == "spec" and question_index < len(SPEC_SECTIONS):
        section = SPEC_SECTIONS[question_index]
        if section['name'] not in spec_document:
            emit("system_message", {"message": f"Extracting final section: {section['name']}..."})
            section_msgs = [h for h in history if h.get("turn", 0) > (turn - topic_turn_count)]
            section_text = "\n".join(f"[{m['name']}]: {m['text']}" for m in section_msgs)
            extract_prompt = f"PRODUCT: {product_description}\n\nSECTION: {section['name']}\n\n{section['extract']}\n\nDISCUSSION:\n{section_text}"
            extracted = await run_claude_async(SPEC_EXTRACT_SYSTEM, extract_prompt, timeout=60, model=model)
            if "[Error" not in extracted and "[Claude CLI" not in extracted:
                spec_document[section['name']] = extracted
                emit("spec_section", {
                    "section": section['name'],
                    "content": extracted,
                    "section_index": question_index + 1,
                    "total_sections": len(SPEC_SECTIONS),
                })
                emit("system_message", {"message": f"LOCKED: {section['name']}"})

    # Save last topic's history
    all_histories.append({"question": question, "history": list(history)})

    total_elapsed = time.time() - total_start

    # Save transcript
    output_dir = Path(__file__).resolve().parent.parent.parent / "sessions" / "conversations"
    if mode == "spec":
        output_dir = Path(__file__).resolve().parent.parent.parent / "sessions" / "specs"
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d_%H%M")
    transcript_path = output_dir / f"{ts}_conversation.md"
    lines = [f"# Conversation\n", f"*{ts} | {len(history)} turns | {len(questions)} topics*\n"]
    for msg in history:
        lines.append(f"\n**{msg['name']}** (turn {msg['turn']}):\n{msg['text']}\n")
    transcript_path.write_text("\n".join(lines), encoding="utf-8")
    emit("system_message", {"message": f"Transcript saved: {transcript_path.name}"})

    # In spec mode: assemble the full spec document
    final_summary = ""
    if mode == "spec" and spec_document:
        spec_lines = [f"# Product Spec: {product_description[:80]}\n"]
        spec_lines.append(f"*Generated {ts} by {len(agent_keys)} agents over {len(history)} turns*\n")
        for section in SPEC_SECTIONS:
            if section['name'] in spec_document:
                spec_lines.append(f"\n## {section['name']}\n")
                spec_lines.append(spec_document[section['name']])
                spec_lines.append("")
        final_summary = "\n".join(spec_lines)
        spec_path = output_dir / f"{ts}_spec.md"
        spec_path.write_text(final_summary, encoding="utf-8")
        emit("synthesis_final", {"summary": final_summary})
        emit("system_message", {"message": f"Product spec saved: {spec_path.name}"})
    elif synthesizer:
        # Chat mode: run final synthesis
        emit("system_message", {"message": "Running final synthesis..."})
        final_summary = await synthesizer.final_synthesis(history, model=model or "sonnet")
        summary_path = output_dir / f"{ts}_synthesis.md"
        summary_path.write_text(f"# Synthesis: {questions[0][:80]}\n\n{final_summary}", encoding="utf-8")
        emit("synthesis_final", {"summary": final_summary})
        emit("system_message", {"message": f"Synthesis saved: {summary_path.name}"})

    emit("conversation_done", {
        "turns": len(history),
        "elapsed": f"{total_elapsed / 60:.1f}m",
    })

    return {
        "history": history,
        "all_histories": all_histories,
        "synthesis": final_summary,
        "spec_document": spec_document,
        "snapshots": [s.__dict__ for s in (synthesizer.snapshots if synthesizer else [])],
        "transcript_path": str(transcript_path),
    }


_conversation_result = None  # Store result for external use


def run_conversation_thread(questions, agent_keys, max_turns, timeout, model=None,
                            team_config=None, turns_per_topic=0, synthesize=True, mode="chat"):
    global _conversation_result
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    _conversation_result = loop.run_until_complete(
        run_conversation(questions, agent_keys, max_turns, timeout, model, team_config,
                         turns_per_topic, synthesize, mode)
    )


def main():
    global _server_ref
    parser = argparse.ArgumentParser(description="Live Agent Conversation")
    parser.add_argument("question", nargs="?", default=None,
                        help="The discussion topic (optional -- can configure from UI)")
    parser.add_argument("--questions", default=None,
                        help="Path to file with one question per line (overrides positional question)")
    parser.add_argument("--turns", type=int, default=10, help="Max conversation turns (default: 10)")
    parser.add_argument("--turns-per-topic", type=int, default=0,
                        help="Max turns per topic before advancing (default: auto-split)")
    parser.add_argument("--timeout", type=int, default=60, help="Timeout per agent call (default: 60)")
    parser.add_argument("--port", type=int, default=8899)
    parser.add_argument("--agents", default=None,
                        help="Comma-separated agent keys (default: all agents in team)")
    parser.add_argument("--model", default=None,
                        help="Model to use (e.g. sonnet, opus, haiku)")
    parser.add_argument("--team", default=None,
                        help="Path to team YAML config (default: beta-agents.yaml)")
    parser.add_argument("--no-synthesis", action="store_true",
                        help="Disable rolling synthesis and final summary")
    parser.add_argument("--mode", choices=["chat", "spec"], default="chat",
                        help="Mode: 'chat' for open discussion, 'spec' for structured spec building")

    args = parser.parse_args()

    server = HTTPServer(("0.0.0.0", args.port), ConvHandler)
    server._agent_colors = {}
    server._team_labels = {}
    _server_ref = server

    if args.question:
        # CLI mode: start conversation immediately
        if args.questions:
            q_path = Path(args.questions)
            questions = [line.strip() for line in q_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        else:
            questions = [args.question]

        if args.mode == "spec" and args.turns == 10:
            args.turns = 35

        team_config = args.team or str(TEAM_CONFIG)
        team = load_team(team_config)

        if args.agents:
            agent_keys = [a.strip() for a in args.agents.split(",")]
        else:
            agent_keys = list(team.agents.keys())

        agent_colors = _build_agent_colors(agent_keys)
        server._agent_colors = agent_colors

        session_thread = threading.Thread(
            target=run_conversation_thread,
            args=(questions, agent_keys, args.turns, args.timeout, args.model, team_config,
                  args.turns_per_topic, not args.no_synthesis, args.mode),
            daemon=True,
        )
        session_thread.start()

        print(f"\n  Live conversation: http://localhost:{args.port}")
        print(f"  Mode: {args.mode.upper()}")
        print(f"  Agents: {', '.join(agent_keys)}")
        print(f"  Max turns: {args.turns}")
    else:
        # UI mode: just start the server, configure from browser
        print(f"\n  ATD Server: http://localhost:{args.port}")
        print(f"  Configure and start conversations from the browser.")

    print(f"  Press Ctrl+C to stop\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()


if __name__ == "__main__":
    main()
