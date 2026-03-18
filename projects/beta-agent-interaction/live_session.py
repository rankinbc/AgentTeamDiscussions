"""Live Session UI -- watch agent discussions in real time.

Runs a session and streams events to a web dashboard via Server-Sent Events.

Usage:
    python live_session.py brief.md
    python live_session.py brief.md --mode ideas --port 8080
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
from queue import Empty  # noqa: F401 -- used in handler

sys.path.insert(0, str(Path(__file__).parent))

# Global event list -- append-only, clients track their own read position
all_events = []
_event_lock = threading.Lock()


def emit(event_type: str, data: dict):
    """Push an event to the SSE stream."""
    event = {"type": event_type, "time": datetime.now().strftime("%H:%M:%S"), **data}
    with _event_lock:
        all_events.append(event)


# -- Monkey-patch the run_discussion module to emit events --

import run_discussion as rd
from claude_runner import run_claude_async as _original_run_claude
from prompt_builder import build_system_prompt, build_context_lens, filter_prior_rounds, build_perspective_reminder
from interact import load_team
from run_discussion import (
    EXPERIMENT_MODES, AGENT_DISPLAY_NAMES, parse_brief, slugify,
    format_transcript, extract_open_questions, synthesize, TEAM_CONFIG,
    COUNTER_PROPOSE_INSTRUCTION, PROPOSE_ROLES,
)
from session_runner import (
    create_session_dir, write_with_marker, read_ledger, extract_ledger_section,
    extract_ledger_from_doc, append_to_ledger, write_session_status,
    load_session_status, generate_morning_brief, hash_question_list,
    MORNING_BRIEF_SYSTEM, MORNING_BRIEF_PROMPT,
)

import shutil


INTERACTION_ANALYSIS_PROMPT = (
    "You are an interaction analyst. Read the agent responses and produce THREE sections.\n\n"
    "SECTION 1 - EVENTS (one per line):\n"
    "EVENT | ICON | Agent1 -> Agent2 | description (max 15 words)\n"
    "Icons: agreed, disagreed, challenged, proposed, conceded, built_on, ignored, reframed\n"
    "Max 6 events.\n\n"
    "SECTION 2 - AGENT STATES (one per line):\n"
    "STATE | AgentName | mood_word | one-sentence internal monologue\n"
    "mood_word: confident, frustrated, curious, skeptical, excited, defensive, bored, energized\n\n"
    "SECTION 3 - IDEAS (one per line):\n"
    "IDEA | AgentName | magnitude (1-10) | short idea name (3-6 words) | status\n"
    "magnitude: how strongly this agent holds/pushes this idea (1=mentioned, 5=advocating, 10=will die on this hill)\n"
    "status: new (just proposed), rising (gaining support), falling (lost ground), held (unchanged), killed (abandoned)\n"
    "Extract every concrete proposal, mechanism, or design choice an agent made or defended.\n"
    "Also track ideas from PREVIOUS rounds that agents referenced -- show if magnitude changed.\n\n"
    "Output ONLY these tagged lines. No headers, no explanation, no blank lines."
)


async def analyze_round_interactions(round_responses: dict, round_name: str, timeout: int) -> tuple[list[dict], list[dict], list[dict]]:
    """Analyze agent interactions in a round. Returns (events, agent_states, ideas)."""
    text = ""
    for key, resp in round_responses.items():
        name = AGENT_DISPLAY_NAMES.get(key, key)
        text += f"### {name}\n{resp[:1500]}\n\n"

    try:
        response = await run_claude_async(
            INTERACTION_ANALYSIS_PROMPT,
            f"Round: {round_name.upper()}\n\n{text}",
            timeout=min(timeout, 60),
        )
        events = []
        states = []
        ideas = []
        icon_map = {
            "agreed": "handshake", "disagreed": "swords", "challenged": "target",
            "proposed": "bulb", "conceded": "flag", "built_on": "link",
            "ignored": "skip", "reframed": "refresh",
        }
        for line in response.strip().split("\n"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) < 3:
                continue
            tag = parts[0].lower()
            if tag == "event" and len(parts) >= 4:
                events.append({
                    "icon": icon_map.get(parts[1].lower(), "dot"),
                    "agents": parts[2],
                    "description": parts[3],
                })
            elif tag == "state" and len(parts) >= 4:
                states.append({
                    "agent": parts[1],
                    "mood": parts[2],
                    "thought": parts[3] if len(parts) > 3 else "",
                })
            elif tag == "idea" and len(parts) >= 5:
                try:
                    mag = int(parts[2])
                except ValueError:
                    mag = 5
                ideas.append({
                    "agent": parts[1],
                    "magnitude": max(1, min(10, mag)),
                    "name": parts[3],
                    "status": parts[4] if len(parts) > 4 else "new",
                })
        return events[:6], states, ideas
    except Exception:
        return [], [], []


AGENT_COLORS = {
    "cognitive_architect": "#6366f1",
    "flow_orchestrator": "#06b6d4",
    "systems_pragmatist": "#f97316",
    "adversarial_critic": "#ef4444",
    "product_oracle": "#22c55e",
    "context_surgeon": "#a855f7",
    "idea_merchant": "#eab308",
}

HTML_PAGE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>ATD // LIVE</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Space+Grotesk:wght@400;600;700&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #08090d; --surface: #0d1017; --surface-raised: #131720;
    --border: #1a1f2e; --border-active: #2a3148;
    --text: #c8cdd8; --text-dim: #5a6178; --text-bright: #eef0f6;
    --accent-blue: #4d7cff; --accent-green: #2dd4a0; --accent-red: #ff4d6a;
    --accent-amber: #f5a623; --accent-purple: #a78bfa;
    --glow-blue: rgba(77,124,255,0.15); --glow-green: rgba(45,212,160,0.12);
    --glow-red: rgba(255,77,106,0.12);
    --mono: 'JetBrains Mono', 'Cascadia Code', 'Fira Code', monospace;
    --sans: 'Space Grotesk', system-ui, sans-serif;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: var(--bg); color: var(--text); font-family: var(--mono);
    font-size: 13px; line-height: 1.5; min-height: 100vh;
    background-image:
      repeating-linear-gradient(0deg, transparent, transparent 1px, rgba(255,255,255,0.008) 1px, rgba(255,255,255,0.008) 2px);
  }

  /* Scanline overlay */
  body::after {
    content: ''; position: fixed; inset: 0; pointer-events: none; z-index: 9999;
    background: repeating-linear-gradient(0deg, transparent 0px, transparent 2px, rgba(0,0,0,0.03) 2px, rgba(0,0,0,0.03) 4px);
  }

  .shell { max-width: 1400px; margin: 0 auto; padding: 12px 16px; }

  /* Header bar */
  .header {
    display: flex; align-items: center; gap: 12px;
    padding: 12px 0; border-bottom: 1px solid var(--border); margin-bottom: 6px;
  }
  .header .logo {
    font-family: var(--sans); font-weight: 700; font-size: 18px;
    color: var(--accent-blue); letter-spacing: -0.5px;
  }
  .header .logo span { color: var(--text-dim); font-weight: 400; }
  .header .pulse {
    width: 8px; height: 8px; border-radius: 50%; background: var(--accent-green);
    box-shadow: 0 0 8px var(--accent-green);
    animation: pulse 2s ease-in-out infinite;
  }
  @keyframes pulse { 0%,100% { opacity:1; box-shadow: 0 0 8px var(--accent-green); } 50% { opacity:0.4; box-shadow: none; } }

  .header .status-text { color: var(--text-dim); font-size: 11px; margin-left: auto; }

  .meta-bar {
    display: flex; gap: 16px; padding: 8px 0 14px 0; font-size: 11px;
    color: var(--text-dim); border-bottom: 1px solid var(--border); margin-bottom: 16px;
  }
  .meta-bar .tag {
    background: var(--surface-raised); padding: 2px 8px; border-radius: 3px;
    border: 1px solid var(--border);
  }

  /* Question block */
  .q-block {
    margin: 14px 0 8px 0; padding: 6px 10px;
    background: var(--surface); border: 1px solid var(--border-active);
    border-left: 3px solid var(--accent-purple);
    font-family: var(--sans); font-size: 12px; font-weight: 600;
    color: var(--text-bright);
  }
  .q-block .q-num { color: var(--accent-purple); font-family: var(--mono); font-size: 9px; font-weight: 400; }

  /* Round label */
  .round-tag {
    display: inline-block; margin: 8px 0 4px 0; padding: 2px 8px;
    font-size: 9px; text-transform: uppercase; letter-spacing: 2px;
    color: var(--text-dim); background: var(--surface); border: 1px solid var(--border);
  }

  /* Round grid -- agents side by side */
  .round-grid {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 6px; margin: 4px 0;
  }

  /* Agent cards */
  .agent {
    background: var(--surface); border: 1px solid var(--border);
    padding: 8px 10px;
    border-left: 3px solid var(--text-dim);
    animation: slideIn 0.25s ease-out;
    transition: border-color 0.3s;
  }
  @keyframes slideIn { from { opacity:0; transform: translateX(-8px); } to { opacity:1; transform: none; } }

  .agent-hdr {
    display: flex; align-items: baseline; gap: 6px; margin-bottom: 3px;
  }
  .agent-hdr .name { font-weight: 500; font-size: 10px; }
  .agent-hdr .elapsed { font-size: 9px; color: var(--text-dim); margin-left: auto; }

  .agent-body {
    color: var(--text); font-size: 10px; line-height: 1.55;
    white-space: pre-wrap; word-wrap: break-word;
    max-height: 180px; overflow-y: auto;
  }
  .agent-body::-webkit-scrollbar { width: 3px; }
  .agent-body::-webkit-scrollbar-thumb { background: var(--border-active); }

  /* Interaction feed */
  .interactions {
    display: flex; flex-wrap: wrap; gap: 4px; margin: 6px 0; padding: 6px 0;
    border-top: 1px solid var(--border); border-bottom: 1px solid var(--border);
  }
  .ix-event {
    display: inline-flex; align-items: center; gap: 4px;
    font-size: 9px; color: var(--text-dim); padding: 2px 8px;
    background: var(--surface-raised); border: 1px solid var(--border);
    animation: slideIn 0.3s ease-out;
  }
  .ix-icon { font-size: 11px; }
  .ix-agents { color: var(--accent-blue); font-weight: 500; }
  .ix-desc { color: var(--text); }

  .agent-body.waiting {
    color: var(--text-dim);
  }
  .agent-body.waiting::after {
    content: ''; display: inline-block; width: 6px; height: 12px;
    background: var(--accent-blue); margin-left: 2px;
    animation: blink 0.8s step-end infinite;
  }
  @keyframes blink { 50% { opacity: 0; } }

  /* Synthesis */
  .synth {
    background: var(--surface); border: 1px solid rgba(77,124,255,0.3);
    border-left: 3px solid var(--accent-blue); margin: 6px 0; padding: 8px 10px;
    box-shadow: inset 0 0 20px var(--glow-blue);
  }
  .synth .agent-hdr .name { color: var(--accent-blue); font-size: 10px; }
  .synth .agent-body { font-size: 10px; max-height: 150px; }

  /* Ledger */
  .ledger-tag {
    display: inline-block; margin: 4px 0; padding: 2px 8px;
    font-size: 9px; color: var(--accent-amber); background: rgba(245,166,35,0.08);
    border: 1px solid rgba(245,166,35,0.2);
  }

  /* Brief */
  .brief {
    background: var(--surface); border: 1px solid rgba(45,212,160,0.3);
    border-left: 3px solid var(--accent-green); margin: 8px 0; padding: 8px 10px;
    box-shadow: inset 0 0 20px var(--glow-green);
  }
  .brief .agent-hdr .name { color: var(--accent-green); font-size: 10px; }
  .brief .agent-body { font-size: 10px; max-height: 200px; }

  /* Status bars */
  .q-done {
    padding: 4px 10px; font-size: 9px; color: var(--accent-green);
    border-left: 3px solid var(--accent-green); background: rgba(45,212,160,0.04);
    margin: 3px 0;
  }
  .q-fail {
    padding: 4px 10px; font-size: 9px; color: var(--accent-red);
    border-left: 3px solid var(--accent-red); background: var(--glow-red);
    margin: 3px 0;
  }
  .error-text { color: var(--accent-red); }

  /* Agent state mood badges */
  .mood-badge {
    display: inline-block; padding: 1px 6px; font-size: 8px; border-radius: 2px;
    text-transform: uppercase; letter-spacing: 1px; margin-left: 6px;
  }
  .mood-confident { background: rgba(45,212,160,0.15); color: var(--accent-green); border: 1px solid rgba(45,212,160,0.3); }
  .mood-frustrated { background: rgba(255,77,106,0.15); color: var(--accent-red); border: 1px solid rgba(255,77,106,0.3); }
  .mood-curious { background: rgba(77,124,255,0.15); color: var(--accent-blue); border: 1px solid rgba(77,124,255,0.3); }
  .mood-skeptical { background: rgba(245,166,35,0.15); color: var(--accent-amber); border: 1px solid rgba(245,166,35,0.3); }
  .mood-excited { background: rgba(168,85,247,0.15); color: var(--accent-purple); border: 1px solid rgba(168,85,247,0.3); }
  .mood-defensive { background: rgba(255,77,106,0.1); color: #ff8fa3; border: 1px solid rgba(255,77,106,0.2); }
  .mood-bored { background: rgba(90,97,120,0.2); color: var(--text-dim); border: 1px solid var(--border); }
  .mood-energized { background: rgba(45,212,160,0.1); color: #5eead4; border: 1px solid rgba(45,212,160,0.2); }

  /* Thought tooltip on agent card hover */
  .agent { position: relative; }
  .agent-thought {
    display: none; position: absolute; top: -4px; left: 50%; transform: translate(-50%, -100%);
    background: #1a1f2e; border: 1px solid var(--accent-blue); padding: 6px 10px;
    font-size: 9px; color: var(--text); z-index: 100; white-space: nowrap;
    max-width: 400px; white-space: normal; pointer-events: none;
  }
  .agent-thought::after {
    content: ''; position: absolute; bottom: -5px; left: 50%; transform: translateX(-50%);
    border-left: 5px solid transparent; border-right: 5px solid transparent;
    border-top: 5px solid var(--accent-blue);
  }
  .agent:hover .agent-thought { display: block; }

  /* Countdown */
  .countdown {
    text-align: center; padding: 8px; font-size: 11px; color: var(--text-dim);
    border: 1px dashed var(--border); margin: 6px 0;
  }
  .countdown .cd-num { color: var(--accent-blue); font-size: 14px; font-weight: 600; }

  /* Agent roster panel */
  .roster {
    display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px;
    padding: 12px 0; border-bottom: 1px solid var(--border);
  }
  .roster-card {
    background: var(--surface); border: 1px solid var(--border);
    padding: 10px 12px; min-width: 200px; flex: 1;
    position: relative;
  }
  .roster-card .r-name {
    font-weight: 500; font-size: 12px; margin-bottom: 2px;
  }
  .roster-card .r-role {
    font-size: 10px; color: var(--text-dim); margin-bottom: 8px;
  }
  .roster-card .r-traits {
    display: flex; flex-direction: column; gap: 3px;
  }
  .r-trait {
    display: flex; align-items: center; gap: 6px; font-size: 9px;
  }
  .r-trait .r-label { color: var(--text-dim); width: 70px; text-align: right; }
  .r-trait .r-bar {
    flex: 1; height: 4px; background: var(--border); border-radius: 2px; overflow: hidden;
  }
  .r-trait .r-fill {
    height: 100%; border-radius: 2px; transition: width 0.5s ease;
  }
  .r-trait .r-val { color: var(--text-dim); width: 24px; text-align: right; }

  .roster-card .r-ideas {
    margin-top: 6px; display: flex; flex-direction: column; gap: 2px;
  }
  .idea-row {
    display: flex; align-items: center; gap: 4px; font-size: 8px;
  }
  .idea-name { color: var(--text); flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .idea-mag {
    display: flex; gap: 1px;
  }
  .idea-mag .pip {
    width: 4px; height: 8px; background: var(--border);
  }
  .idea-mag .pip.filled { background: var(--accent-amber); }
  .idea-mag .pip.filled.high { background: var(--accent-red); }
  .idea-status {
    font-size: 7px; padding: 0 3px; border-radius: 2px;
  }
  .idea-status.new { color: var(--accent-green); }
  .idea-status.rising { color: var(--accent-blue); }
  .idea-status.falling { color: var(--accent-red); }
  .idea-status.held { color: var(--text-dim); }
  .idea-status.killed { color: var(--accent-red); text-decoration: line-through; }

  /* Tooltip for idea details */
  .roster-card { position: relative; }
  .idea-detail-tooltip {
    display: none; position: absolute; bottom: 100%; left: 0; right: 0;
    background: #1a1f2e; border: 1px solid var(--accent-amber);
    padding: 6px 8px; font-size: 9px; color: var(--text);
    z-index: 100; max-height: 200px; overflow-y: auto;
  }
  .roster-card:hover .idea-detail-tooltip.has-ideas { display: block; }
</style>
</head>
<body>
<div class="shell">
  <div class="header">
    <div class="logo">ATD <span>// LIVE</span></div>
    <div class="pulse" id="pulse"></div>
    <div class="status-text" id="clock"></div>
  </div>
  <div class="meta-bar" id="meta">
    <span class="tag">Connecting...</span>
  </div>
  <div id="stream"></div>
</div>
<script>
setInterval(() => {
  const c = document.getElementById('clock');
  if (c) c.textContent = new Date().toLocaleTimeString();
}, 1000);

const stream = document.getElementById('stream');
const meta = document.getElementById('meta');
const pulse = document.getElementById('pulse');

function esc(s) {
  const d = document.createElement('div'); d.textContent = s; return d.innerHTML;
}

function add(html) {
  stream.insertAdjacentHTML('beforeend', html);
  window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
}

const C = AGENT_COLORS_JSON;
const agentIdeas = {};  // Track ideas per agent: {agentKey: [{name, magnitude, status}]}

// Map agent display names to roster keys for lookup
const nameToKey = {};

function renderIdeas(agentKey) {
  const container = document.getElementById('ideas-' + agentKey);
  const tooltip = document.getElementById('tooltip-' + agentKey);
  if (!container || !agentIdeas[agentKey]) return;
  const ideas = agentIdeas[agentKey];
  let html = '';
  let tooltipHtml = '';
  for (const idea of ideas) {
    // Magnitude bar (10 pips)
    let pips = '';
    for (let i = 1; i <= 10; i++) {
      const filled = i <= idea.magnitude;
      const high = idea.magnitude >= 8 && filled;
      pips += '<div class="pip' + (filled ? ' filled' : '') + (high ? ' high' : '') + '"></div>';
    }
    html += '<div class="idea-row"><span class="idea-name">' + esc(idea.name) + '</span><div class="idea-mag">' + pips + '</div><span class="idea-status ' + idea.status + '">' + idea.status + '</span></div>';
    tooltipHtml += '<div><strong>' + esc(idea.name) + '</strong> (mag: ' + idea.magnitude + '/10, ' + idea.status + ')</div>';
  }
  container.innerHTML = html;
  if (tooltip && ideas.length > 0) {
    tooltip.innerHTML = tooltipHtml;
    tooltip.classList.add('has-ideas');
  }
}

function buildRoster(profiles) {
  if (!profiles) return;
  let html = '<div class="roster" id="roster">';
  const traitColors = {
    assertiveness: '#ef4444', creativity: '#a855f7', risk_tolerance: '#f97316',
    stubbornness: '#6366f1', idea_receptivity: '#22c55e', bluntness: '#ff4d6a',
    patience: '#06b6d4', attention_span: '#eab308'
  };
  for (const [key, p] of Object.entries(profiles)) {
    nameToKey[p.name] = key;
    // Also map partial names for fuzzy matching from analysis
    const shortName = p.name.replace('The ', '');
    nameToKey[shortName] = key;
    const bars = Object.entries(p.traits).map(([t, v]) =>
      `<div class="r-trait">
        <span class="r-label">${t.replace('_',' ')}</span>
        <div class="r-bar"><div class="r-fill" style="width:${v*100}%;background:${traitColors[t]||'#4d7cff'}"></div></div>
        <span class="r-val">${v.toFixed(1)}</span>
      </div>`
    ).join('');
    html += `<div class="roster-card" id="roster-${key}" style="border-top: 2px solid ${p.color}">
      <div class="r-name" style="color:${p.color}">${esc(p.name)}</div>
      <div class="r-role">${esc(p.role)} | ${esc(p.style)} | ${esc(p.mood)}</div>
      <div class="r-traits">${bars}</div>
      <div class="r-ideas" id="ideas-${key}"></div>
      <div class="idea-detail-tooltip" id="tooltip-${key}"></div>
    </div>`;
  }
  html += '</div>';
  stream.insertAdjacentHTML('beforebegin', html);
}

function findAgentKey(displayName) {
  // Try exact match first, then partial
  if (nameToKey[displayName]) return nameToKey[displayName];
  for (const [name, key] of Object.entries(nameToKey)) {
    if (displayName.includes(name) || name.includes(displayName)) return key;
  }
  return null;
}

const src = new EventSource('/events');

src.onmessage = function(e) {
  const ev = JSON.parse(e.data);

  switch(ev.type) {
    case 'session_start':
      meta.innerHTML = `<span class="tag">${esc(ev.brief)}</span><span class="tag">${esc(ev.mode)}</span><span class="tag">${ev.question_count} questions</span><span class="tag">${ev.time}</span>`;
      buildRoster(ev.profiles);
      break;

    case 'question_start':
      add(`<div class="q-block"><span class="q-num">Q${ev.number}/${ev.total}</span> ${esc(ev.title)}</div>`);
      break;

    case 'round_start':
      add(`<div class="round-tag">${esc(ev.round)} &mdash; ${esc(ev.agents)}</div><div class="round-grid" id="grid-${ev.round}-${Date.now()}"></div>`);
      break;

    case 'agent_thinking': {
      // Find the most recent round-grid and append to it
      const grids = document.querySelectorAll('.round-grid');
      const grid = grids[grids.length - 1];
      if (grid) {
        grid.insertAdjacentHTML('beforeend', `<div class="agent" id="agent-${ev.agent}" style="border-left-color: ${C[ev.agent] || 'var(--text-dim)'}">
          <div class="agent-hdr">
            <span class="name" style="color: ${C[ev.agent] || 'var(--text)'}">${esc(ev.display_name)}</span>
            <span class="elapsed" id="timer-${ev.agent}"></span>
          </div>
          <div class="agent-body waiting">analyzing</div>
        </div>`);
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
      }
      break;
    }
      break;

    case 'agent_response': {
      const card = document.getElementById('agent-' + ev.agent);
      if (card) {
        const body = card.querySelector('.agent-body');
        body.classList.remove('waiting');
        body.textContent = ev.response;
        const timer = document.getElementById('timer-' + ev.agent);
        if (timer) timer.textContent = ev.elapsed + 's';
        if (ev.error) body.classList.add('error-text');
      }
      break;
    }

    case 'synthesis_start':
      add(`<div class="synth" id="synthesis">
        <div class="agent-hdr"><span class="name">SYNTHESIS</span><span class="elapsed" id="timer-synth"></span></div>
        <div class="agent-body waiting">compiling design doc</div>
      </div>`);
      break;

    case 'synthesis_done': {
      const s = document.getElementById('synthesis');
      if (s) {
        const body = s.querySelector('.agent-body');
        body.classList.remove('waiting');
        body.textContent = ev.preview;
        const t = document.getElementById('timer-synth');
        if (t) t.textContent = ev.elapsed + 's | ' + ev.lines + ' lines';
      }
      break;
    }

    case 'ideas_update': {
      for (const idea of ev.ideas) {
        const key = findAgentKey(idea.agent);
        if (!key) continue;
        if (!agentIdeas[key]) agentIdeas[key] = [];
        // Update existing idea or add new
        const existing = agentIdeas[key].find(i => i.name.toLowerCase() === idea.name.toLowerCase());
        if (existing) {
          existing.magnitude = idea.magnitude;
          existing.status = idea.status;
        } else {
          agentIdeas[key].push({ name: idea.name, magnitude: idea.magnitude, status: idea.status });
        }
        // Sort by magnitude descending
        agentIdeas[key].sort((a, b) => b.magnitude - a.magnitude);
        // Keep top 8
        agentIdeas[key] = agentIdeas[key].slice(0, 8);
        renderIdeas(key);
      }
      break;
    }

    case 'agent_states': {
      for (const st of ev.states) {
        // Find the agent card by matching name
        const cards = document.querySelectorAll('.agent');
        for (const card of cards) {
          const nameEl = card.querySelector('.name');
          if (nameEl && nameEl.textContent.includes(st.agent.split('(')[0].trim().substring(0,15))) {
            // Add mood badge
            const hdr = card.querySelector('.agent-hdr');
            const existing = hdr.querySelector('.mood-badge');
            if (existing) existing.remove();
            const moodClass = 'mood-' + st.mood.toLowerCase().replace(/[^a-z]/g,'');
            hdr.insertAdjacentHTML('beforeend', '<span class="mood-badge ' + moodClass + '">' + esc(st.mood) + '</span>');
            // Add thought tooltip
            let tooltip = card.querySelector('.agent-thought');
            if (!tooltip) {
              card.insertAdjacentHTML('afterbegin', '<div class="agent-thought"></div>');
              tooltip = card.querySelector('.agent-thought');
            }
            if (st.thought) tooltip.textContent = st.thought;
          }
        }
      }
      break;
    }

    case 'countdown': {
      const cdId = 'cd-' + Date.now();
      add('<div class="countdown" id="' + cdId + '">Next: <strong>' + esc(ev.next_round) + '</strong> in <span class="cd-num">' + ev.seconds + '</span>s</div>');
      let remaining = ev.seconds;
      const cdInterval = setInterval(() => {
        remaining--;
        const el = document.querySelector('#' + cdId + ' .cd-num');
        if (el) el.textContent = remaining;
        if (remaining <= 0) {
          clearInterval(cdInterval);
          const cdEl = document.getElementById(cdId);
          if (cdEl) cdEl.remove();
        }
      }, 1000);
      break;
    }

    case 'interactions': {
      const iconMap = {
        handshake: '\\u{1F91D}', swords: '\\u2694\\uFE0F', target: '\\u{1F3AF}',
        bulb: '\\u{1F4A1}', flag: '\\u{1F3F3}\\uFE0F', link: '\\u{1F517}',
        skip: '\\u23ED\\uFE0F', refresh: '\\u{1F504}', dot: '\\u25CF'
      };
      let html = '<div class="interactions">';
      for (const ix of ev.events) {
        const icon = iconMap[ix.icon] || '\u25CF';
        html += `<div class="ix-event"><span class="ix-icon">${icon}</span><span class="ix-agents">${esc(ix.agents)}</span><span class="ix-desc">${esc(ix.description)}</span></div>`;
      }
      html += '</div>';
      add(html);
      break;
    }

    case 'ledger_extracted':
      add(`<div class="ledger-tag">${ev.count} decisions extracted</div>`);
      break;

    case 'question_done':
      add(`<div class="q-done">Q${ev.number} complete &mdash; ${ev.elapsed}s</div>`);
      break;

    case 'question_failed':
      add(`<div class="q-fail">Q${ev.number} ${esc(ev.status)}: ${esc(ev.reason)}</div>`);
      break;

    case 'brief_start':
      add(`<div class="brief" id="brief">
        <div class="agent-hdr"><span class="name">MORNING BRIEF</span></div>
        <div class="agent-body waiting">generating</div>
      </div>`);
      break;

    case 'brief_done': {
      const b = document.getElementById('brief');
      if (b) {
        const body = b.querySelector('.agent-body');
        body.classList.remove('waiting');
        body.textContent = ev.preview;
      }
      break;
    }

    case 'session_done':
      meta.innerHTML += `<span class="tag" style="border-color: var(--accent-green); color: var(--accent-green);">DONE ${ev.elapsed} | ${ev.completed}/${ev.total}</span>`;
      pulse.style.background = 'var(--accent-green)';
      pulse.style.animation = 'none';
      break;
  }
};

src.onerror = function() {
  pulse.style.background = 'var(--accent-red)';
  pulse.style.boxShadow = '0 0 8px var(--accent-red)';
  pulse.style.animation = 'none';
};
</script>
</body>
</html>"""


class LiveHandler(BaseHTTPRequestHandler):
    """HTTP handler serving the dashboard and SSE stream."""

    def log_message(self, format, *args):
        pass  # Suppress access logs

    def do_GET(self):
        if self.path == "/":
            page = HTML_PAGE.replace("AGENT_COLORS_JSON", json.dumps(AGENT_COLORS))
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(page.encode())

        elif self.path == "/events":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            # Per-client read position -- start at 0 to replay all events
            pos = 0
            while True:
                try:
                    with _event_lock:
                        current_len = len(all_events)
                    if pos < current_len:
                        # Send all new events since last read
                        for ev in all_events[pos:current_len]:
                            self.wfile.write(f"data: {json.dumps(ev)}\n\n".encode())
                        self.wfile.flush()
                        pos = current_len
                    else:
                        # No new events, send keepalive
                        self.wfile.write(b": keepalive\n\n")
                        self.wfile.flush()
                    time.sleep(0.5)
                except (BrokenPipeError, ConnectionResetError, OSError):
                    break
        else:
            self.send_response(404)
            self.end_headers()


async def run_live_session(brief_path, sessions_root, mode_name, timeout):
    """Run a session with live event emission."""
    decisions_text, all_questions = parse_brief(brief_path)
    q_hash = hash_question_list(all_questions)
    mode = EXPERIMENT_MODES[mode_name]

    session_dir = create_session_dir(sessions_root, brief_path.stem)
    shutil.copy2(TEAM_CONFIG, session_dir / "config-snapshot.yaml")

    team = load_team(str(TEAM_CONFIG))
    system_prompts = {key: build_system_prompt(agent) for key, agent in team.agents.items()}

    mode_agents = set()
    for agents in mode["groups"].values():
        mode_agents.update(agents)

    questions_dir = session_dir / "questions"
    questions_dir.mkdir(exist_ok=True)

    status = {"questions": {}, "question_hash": q_hash, "mode": mode_name, "brief": brief_path.name}
    write_session_status(session_dir, status)

    # Build agent profiles for the UI
    agent_profiles = {}
    for key in sorted(mode_agents):
        if key in team.agents:
            a = team.agents[key]
            p = a.personality
            agent_profiles[key] = {
                "name": a.name,
                "role": a.position.role,
                "color": AGENT_COLORS.get(key, "#94a3b8"),
                "traits": {
                    "assertiveness": p.assertiveness,
                    "creativity": p.creativity_temp,
                    "risk_tolerance": p.risk_tolerance,
                    "stubbornness": p.stubbornness,
                    "idea_receptivity": p.idea_receptivity,
                    "bluntness": p.bluntness,
                    "patience": p.patience,
                    "attention_span": p.attention_span,
                },
                "style": p.cognitive_style.value,
                "mood": p.emotional_baseline.value,
                "domains": p.domain_affinities[:4],
                "job": a.output.job,
            }

    emit("session_start", {
        "brief": brief_path.name,
        "mode": f"{mode_name} -- {mode['description']}",
        "question_count": len(all_questions),
        "agents": sorted(mode_agents),
        "profiles": agent_profiles,
    })

    ledger_text = ""
    prior_specs = ""
    accumulated_open_questions = []
    total_start = time.time()

    for question in all_questions:
        q_num = question["number"]
        q_title = question["title"]
        slug = slugify(q_title)
        filename = f"{q_num:02d}-{slug}"
        q_key = f"q{q_num}"

        emit("question_start", {"number": q_num, "total": len(all_questions), "title": q_title})
        q_start = time.time()

        groups = mode["groups"]
        round_labels = list(groups.keys())
        agent_roles = mode.get("agent_roles", {})
        round_responses = {}
        accumulated_discussion = ""
        failed = False

        for round_name in round_labels:
            agents = groups[round_name]
            agent_names = ", ".join(AGENT_DISPLAY_NAMES.get(a, a) for a in agents)
            display_name = "counter-propose" if round_name == "counter" else round_name

            emit("round_start", {"round": display_name.upper(), "agents": agent_names})

            try:
                oq_text = ""
                if accumulated_open_questions:
                    oq_lines = [f"- [from Q{oq['from_q']}] {oq['text']}" for oq in accumulated_open_questions]
                    oq_text = "\n".join(oq_lines)

                round_inst = COUNTER_PROPOSE_INSTRUCTION if round_name == "counter" else ""

                # Callbacks for live UI updates
                def on_agent_start(agent_key):
                    emit("agent_thinking", {"agent": agent_key, "display_name": AGENT_DISPLAY_NAMES.get(agent_key, agent_key)})

                def on_agent_done(agent_key, response, elapsed):
                    is_error = "[Claude CLI timed out" in response or "[Error" in response
                    emit("agent_response", {
                        "agent": agent_key,
                        "display_name": AGENT_DISPLAY_NAMES.get(agent_key, agent_key),
                        "response": response[:2000],
                        "elapsed": f"{elapsed:.0f}",
                        "error": is_error,
                    })

                r_start = time.time()
                responses = await rd.run_round(
                    agents=agents,
                    system_prompts=system_prompts,
                    team=team,
                    question=question,
                    decisions=decisions_text + "\n\n" + ledger_text if ledger_text else decisions_text,
                    prior_rounds=accumulated_discussion,
                    prior_specs=prior_specs[-6000:] if prior_specs else "",
                    open_questions=oq_text,
                    timeout=timeout,
                    round_instruction=round_inst,
                    agent_roles=agent_roles if round_name in ("propose", "counter") else None,
                    sequential=True,
                    on_agent_start=on_agent_start,
                    on_agent_done=on_agent_done,
                )
                r_elapsed = time.time() - r_start

                round_responses[round_name] = responses

                for key, resp in responses.items():
                    name = AGENT_DISPLAY_NAMES.get(key, key)
                    label = "COUNTER-PROPOSAL" if round_name == "counter" else round_name.upper()
                    accumulated_discussion += f"[{label} - {name}]\n{resp}\n\n"

                # Analyze interactions (real system analysis)
                interactions, agent_states, ideas = await analyze_round_interactions(responses, round_name, timeout)
                if interactions:
                    emit("interactions", {"round": round_name, "events": interactions})
                if agent_states:
                    emit("agent_states", {"round": round_name, "states": agent_states})
                if ideas:
                    emit("ideas_update", {"round": round_name, "ideas": ideas})

                # Delay between rounds for readability
                next_idx = round_labels.index(round_name) + 1
                next_name = round_labels[next_idx] if next_idx < len(round_labels) else "synthesis"
                emit("countdown", {"seconds": 20, "next_round": next_name})
                await asyncio.sleep(20)

            except Exception as e:
                emit("question_failed", {"number": q_num, "status": "failed", "reason": str(e)})
                status["questions"][q_key] = {"status": "failed", "title": q_title, "reason": str(e)[:200]}
                write_session_status(session_dir, status)
                failed = True
                break

        if failed:
            continue

        # Synthesis
        emit("synthesis_start", {})
        s_start = time.time()
        try:
            design_doc = await synthesize(
                question, round_responses, round_labels, decisions_text,
                prior_specs[-6000:] if prior_specs else "", "", timeout,
            )
            s_elapsed = time.time() - s_start

            if not design_doc or len(design_doc.strip()) < 50:
                raise RuntimeError("Empty synthesis")

            emit("synthesis_done", {
                "preview": design_doc[:500] + "..." if len(design_doc) > 500 else design_doc,
                "elapsed": f"{s_elapsed:.0f}",
                "lines": len(design_doc.split("\n")),
            })

            # Write files
            q_elapsed = time.time() - q_start
            header = (
                f"# {q_title}\n\n"
                f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | "
                f"Question {q_num} | {q_elapsed:.0f}s | Mode: {mode_name}*\n\n"
            )
            write_with_marker(questions_dir / f"{filename}.md", header + design_doc)
            transcript = format_transcript(question, round_responses)
            write_with_marker(questions_dir / f"{filename}-transcript.md", transcript)

            # Ledger extraction
            ledger_section = extract_ledger_section(design_doc)
            if not ledger_section:
                ledger_section = await extract_ledger_from_doc(design_doc, q_num, q_title, timeout)

            if ledger_section:
                decided_count = ledger_section.count("- DECIDED:")
                append_to_ledger(session_dir, ledger_section, q_num)
                ledger_text = read_ledger(session_dir)
                emit("ledger_extracted", {"count": decided_count})
            else:
                fallback = f"### Q{q_num}: {q_title[:40]}\n- DECIDED: See design doc for details\n"
                append_to_ledger(session_dir, fallback, q_num)
                ledger_text = read_ledger(session_dir)

            # Extract open questions and chain
            new_oqs = extract_open_questions(design_doc)
            for oq in new_oqs:
                accumulated_open_questions.append({"from_q": q_num, "text": oq})
            prior_specs = design_doc[:3000]

            status["questions"][q_key] = {
                "status": "complete", "title": q_title,
                "elapsed_seconds": round(q_elapsed), "file": f"{filename}.md",
            }
            write_session_status(session_dir, status)

            emit("question_done", {"number": q_num, "elapsed": f"{q_elapsed:.0f}"})

        except Exception as e:
            emit("question_failed", {"number": q_num, "status": "failed", "reason": str(e)[:200]})
            status["questions"][q_key] = {"status": "failed", "title": q_title, "reason": str(e)[:200]}
            write_session_status(session_dir, status)

    # Morning Brief
    emit("brief_start", {})
    ledger_text = read_ledger(session_dir)
    try:
        brief_content = await generate_morning_brief(session_dir, ledger_text, status, timeout)
        brief_content = (
            f"# Morning Brief: {session_dir.name}\n\n"
            f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"
            f"{brief_content}"
        )
        emit("brief_done", {"preview": brief_content[:1000]})
    except Exception:
        brief_content = f"# Morning Brief (raw ledger)\n\n{ledger_text}"
        emit("brief_done", {"preview": brief_content[:1000]})

    write_with_marker(session_dir / "summary.md", brief_content)

    total_elapsed = time.time() - total_start
    completed = sum(1 for q in status["questions"].values() if q.get("status") == "complete")

    status["session_complete"] = True
    status["total_elapsed_seconds"] = round(total_elapsed)
    write_session_status(session_dir, status)

    emit("session_done", {
        "elapsed": f"{total_elapsed / 60:.1f}m",
        "completed": completed,
        "total": len(all_questions),
        "session_dir": str(session_dir),
    })


def run_session_thread(brief_path, sessions_root, mode_name, timeout):
    """Run the async session in a new event loop on a background thread."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_live_session(brief_path, sessions_root, mode_name, timeout))


def main():
    parser = argparse.ArgumentParser(description="Live Agent Discussion Dashboard")
    parser.add_argument("brief", help="Path to the discussion brief")
    parser.add_argument("--mode", choices=list(EXPERIMENT_MODES.keys()), default="compete")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--port", type=int, default=8899)
    parser.add_argument("--sessions-dir", default=None)

    args = parser.parse_args()

    brief_path = Path(args.brief)
    if not brief_path.is_absolute():
        brief_path = Path.cwd() / brief_path
    if not brief_path.exists():
        print(f"ERROR: Brief not found: {brief_path}")
        sys.exit(1)

    if args.sessions_dir:
        sessions_root = Path(args.sessions_dir)
    else:
        sessions_root = Path(__file__).resolve().parent.parent.parent / "sessions"
    sessions_root.mkdir(parents=True, exist_ok=True)

    # Start session in background thread
    session_thread = threading.Thread(
        target=run_session_thread,
        args=(brief_path, sessions_root, args.mode, args.timeout),
        daemon=True,
    )
    session_thread.start()

    # Start web server
    server = HTTPServer(("0.0.0.0", args.port), LiveHandler)
    print(f"\n  Live dashboard: http://localhost:{args.port}")
    print(f"  Brief: {brief_path.name}")
    print(f"  Mode: {args.mode}")
    print(f"  Press Ctrl+C to stop\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()


if __name__ == "__main__":
    main()
