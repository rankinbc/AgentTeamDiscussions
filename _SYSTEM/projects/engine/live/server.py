"""Live web dashboard — SSE event stream + HTTP server.

Three-panel layout:
  Left:   Agent roster with personality traits, urgency meters (click for detail panel)
  Center: Chat-style message stream with system event rows (click message for prompt inspector)
  Right:  Agent detail panel (slides in on agent click)

Bottom: Prompt inspector panel (slides up on message click) + moderator input bar
"""

import json
import threading
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

# No hardcoded agent colors — colors are generated client-side from a palette using
# a hash of the agent key, so any team works without config changes.
AGENT_COLORS: dict = {}

_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>ATD // LIVE</title>
<style>
:root {
  --bg:#08090d; --s1:#0d1017; --s2:#131720; --s3:#1a2030;
  --border:#1a1f2e; --border-hi:#2a3148;
  --text:#c8cdd8; --dim:#5a6178; --bright:#eef0f6;
  --green:#2dd4a0; --blue:#4d7cff; --red:#ff4d6a;
  --amber:#f5a623; --purple:#a78bfa; --cyan:#06b6d4;
  --mono:'Cascadia Code','JetBrains Mono','Fira Code',ui-monospace,monospace;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html,body{height:100%;overflow:hidden;}
body{background:var(--bg);color:var(--text);font-family:var(--mono);font-size:11px;line-height:1.5;}

/* ── Shell: three columns ─────────────────────────── */
.shell{display:grid;grid-template-columns:210px 1fr;grid-template-rows:42px 1fr;height:100vh;}
.shell.detail-open{grid-template-columns:210px 1fr 280px;}

/* ── Header ───────────────────────────────────────── */
.hdr{
  grid-column:1/-1;
  display:flex;align-items:center;gap:10px;
  padding:0 14px;
  background:var(--s1);border-bottom:1px solid var(--border);
}
.hdr-logo{font-size:14px;font-weight:700;color:var(--blue);letter-spacing:-.5px;}
.hdr-logo em{color:var(--dim);font-style:normal;font-weight:400;}
.hdr-dot{
  width:7px;height:7px;border-radius:50%;
  background:var(--green);box-shadow:0 0 6px var(--green);
  animation:glow 2s ease-in-out infinite;flex-shrink:0;
}
@keyframes glow{0%,100%{opacity:1;box-shadow:0 0 6px var(--green);}50%{opacity:.3;box-shadow:none;}}
.hdr-tags{display:flex;gap:6px;}
.tag{padding:1px 7px;background:var(--s2);border:1px solid var(--border);border-radius:2px;font-size:10px;color:var(--dim);}
.hdr-orch{
  margin-left:auto;display:flex;gap:12px;font-size:9px;color:var(--dim);align-items:center;
}
.orch-lbl{color:var(--dim);}
.orch-val{color:var(--text);}
.orch-state{color:var(--green);font-weight:600;}
.orch-state.busy{color:var(--amber);}

/* ── Roster (left) ────────────────────────────────── */
.roster{
  background:var(--s1);border-right:1px solid var(--border);
  overflow-y:auto;padding:8px 0 20px;
}
.roster::-webkit-scrollbar{width:3px;}
.roster::-webkit-scrollbar-thumb{background:var(--border-hi);}
.roster-label{padding:8px 12px 4px;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--dim);}

.arow{
  padding:8px 12px;border-left:2px solid transparent;
  cursor:pointer;transition:background .15s;
}
.arow:hover{background:var(--s2);}
.arow.speaking{border-left-color:var(--blue)!important;background:var(--s2);}
.arow.challenged{border-left-color:var(--red)!important;}
.arow.selected{background:var(--s3);}
.arow-name{font-size:11px;font-weight:600;margin-bottom:2px;}
.arow-role{font-size:8px;color:var(--dim);margin-bottom:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.trait-row{display:flex;align-items:center;gap:4px;margin:1px 0;font-size:8px;color:var(--dim);}
.trait-lbl{width:58px;flex-shrink:0;}
.trait-bar{flex:1;height:2px;background:var(--border);}
.trait-fill{height:100%;border-radius:1px;}
.trait-val{width:22px;text-align:right;color:var(--dim);}
.arow-status{font-size:8px;margin-top:4px;color:var(--dim);font-style:italic;}
.arow-urgency{display:flex;align-items:center;gap:4px;margin-top:4px;font-size:8px;color:var(--dim);}
.urg-bar{flex:1;height:3px;background:var(--border);border-radius:2px;overflow:hidden;}
.urg-fill{height:100%;width:0%;background:var(--green);transition:width .25s linear,background .5s;border-radius:2px;}
.urg-time{font-size:8px;color:var(--dim);min-width:28px;text-align:right;}

/* ── Chat panel (center) ──────────────────────────── */
.chat-wrap{display:flex;flex-direction:column;min-height:0;overflow:hidden;}
.messages{flex:1;overflow-y:auto;padding:10px 16px 6px;}
.messages::-webkit-scrollbar{width:4px;}
.messages::-webkit-scrollbar-thumb{background:var(--border-hi);border-radius:2px;}

/* Message rows */
.msg{
  padding:5px 10px;margin:1px 0;
  border-left:2px solid var(--dim);
  cursor:pointer;transition:background .1s;
}
.msg:hover{background:var(--s2);}
.msg.inspected{outline:1px solid var(--amber);outline-offset:-1px;}
.msg-hdr{display:flex;align-items:baseline;gap:6px;margin-bottom:2px;}
.msg-name{font-size:10px;font-weight:600;}
.msg-time{font-size:8px;color:var(--dim);}
.msg-meta{font-size:8px;color:var(--dim);margin-left:auto;}
.msg-body{font-size:11px;line-height:1.55;color:var(--text);white-space:pre-wrap;word-wrap:break-word;}

/* System event rows */
.sys-row{
  padding:3px 10px;margin:2px 0;
  border-left:2px solid var(--blue);
  background:rgba(77,124,255,.03);
}
.sys-row .msg-name{color:var(--blue);font-size:9px;}
.sys-row .msg-body{color:var(--dim);font-size:9px;}

.sys-row.challenge{border-left-color:var(--red);background:rgba(255,77,106,.04);}
.sys-row.challenge .msg-name{color:var(--red);}
.sys-row.challenge .msg-body{color:var(--text);}

.sys-row.synthesis{border-left-color:var(--purple);background:rgba(168,85,250,.04);}
.sys-row.synthesis .msg-name{color:var(--purple);}

.sys-row.round-sep{border-left-color:var(--border-hi);}
.sys-row.round-sep .msg-name{color:var(--dim);font-size:8px;letter-spacing:1.5px;text-transform:uppercase;}

.sys-row.q-start{border-left-color:var(--purple);}
.sys-row.q-start .msg-name{color:var(--purple);}
.sys-row.q-start .msg-body{color:var(--bright);font-size:12px;font-weight:600;}

.sys-row.ok{border-left-color:var(--green);}
.sys-row.ok .msg-name{color:var(--green);}
.sys-row.err{border-left-color:var(--red);}
.sys-row.err .msg-name{color:var(--red);}

.sys-row.thinking-row{border-left-color:var(--blue);}
.sys-row.thinking-row .msg-body{color:var(--dim);font-style:italic;}
.sys-row.thinking-row .msg-body::after{content:'▋';animation:cur 1s step-end infinite;}
@keyframes cur{0%,100%{opacity:1}50%{opacity:0}}

/* Orchestrator bar */
.orch-bar{
  flex-shrink:0;padding:3px 14px;border-top:1px solid var(--border);
  background:var(--s2);font-size:8px;color:var(--dim);
  display:flex;gap:14px;align-items:center;
}

/* Moderator input */
.mod-bar{
  flex-shrink:0;padding:6px 14px;border-top:1px solid var(--border);
  background:var(--s1);
}
.mod-row{display:flex;gap:6px;margin-bottom:4px;}
.mod-input{
  flex:1;background:var(--s2);border:1px solid var(--border);
  color:var(--text);font:11px var(--mono);padding:4px 8px;outline:none;
}
.mod-input:focus{border-color:var(--amber);}
.mod-btn{
  background:var(--s2);border:1px solid var(--border);color:var(--amber);
  font:9px var(--mono);padding:3px 8px;cursor:pointer;text-transform:uppercase;letter-spacing:.5px;white-space:nowrap;
}
.mod-btn:hover{background:var(--border-hi);}
.mod-btn.danger{color:var(--red);}
.mod-btn.danger:hover{border-color:var(--red);}
.mod-actions{display:flex;gap:4px;flex-wrap:wrap;}

/* ── Agent detail panel (right, slides in) ────────── */
.detail{
  background:var(--s1);border-left:1px solid var(--border);
  overflow-y:auto;display:none;padding:0;
}
.detail::-webkit-scrollbar{width:3px;}
.detail::-webkit-scrollbar-thumb{background:var(--border-hi);}
.shell.detail-open .detail{display:block;}
.detail-hdr{
  padding:10px 12px;border-bottom:1px solid var(--border);
  background:var(--s2);position:sticky;top:0;z-index:1;
}
.detail-close{float:right;font-size:9px;color:var(--dim);cursor:pointer;}
.detail-close:hover{color:var(--text);}
.d-section{padding:8px 12px;}
.d-section h3{font-size:8px;text-transform:uppercase;letter-spacing:1.5px;color:var(--dim);margin:10px 0 4px;border-bottom:1px solid var(--border);padding-bottom:3px;}
.d-name{font-size:13px;font-weight:600;margin-bottom:2px;}
.d-role{font-size:9px;color:var(--dim);margin-bottom:6px;}
.d-trait{display:flex;align-items:center;gap:4px;margin:2px 0;}
.dt-lbl{width:70px;font-size:8px;color:var(--dim);}
.dt-bar{flex:1;height:3px;background:var(--border);}
.dt-fill{height:100%;border-radius:1px;}
.dt-val{width:26px;text-align:right;font-size:8px;color:var(--dim);}
.d-item{font-size:9px;color:var(--text);padding:2px 0 2px 8px;border-left:1px solid var(--border);margin:2px 0;line-height:1.4;}
.d-item.drive{border-left-color:var(--green);}
.d-item.pushback{border-left-color:var(--red);}
.d-item.rule{border-left-color:var(--amber);}
.d-context{font-size:8px;color:var(--dim);padding:4px 6px;background:var(--s2);margin:4px 0;line-height:1.4;}
.d-stat{display:flex;justify-content:space-between;font-size:9px;padding:2px 0;}
.d-stat-lbl{color:var(--dim);}
.d-stat-val{color:var(--text);}

/* ── Prompt inspector (slides up from bottom) ─────── */
.inspector{
  position:fixed;bottom:0;left:210px;right:0;
  height:0;overflow:hidden;
  background:var(--s1);border-top:2px solid var(--amber);
  transition:height .2s ease-out;z-index:50;
  display:flex;flex-direction:column;
}
.shell.detail-open ~ .inspector{right:280px;}
.inspector.open{height:42vh;}
.insp-bar{
  flex-shrink:0;display:flex;align-items:center;gap:8px;
  padding:5px 14px;background:var(--s2);border-bottom:1px solid var(--border);
  font-size:9px;text-transform:uppercase;letter-spacing:1.5px;color:var(--amber);
}
.insp-bar-close{margin-left:auto;cursor:pointer;color:var(--dim);}
.insp-bar-close:hover{color:var(--text);}
.insp-tabs{flex-shrink:0;display:flex;padding:0 14px;border-bottom:1px solid var(--border);background:var(--s1);}
.itab{
  padding:5px 12px;font:9px var(--mono);cursor:pointer;
  background:none;border:none;border-bottom:2px solid transparent;
  color:var(--dim);text-transform:uppercase;letter-spacing:.5px;
}
.itab:hover{color:var(--text);}
.itab.active{color:var(--amber);border-bottom-color:var(--amber);}
.insp-body{flex:1;overflow-y:auto;padding:10px 14px;font-size:9px;color:var(--text);white-space:pre-wrap;word-wrap:break-word;line-height:1.55;}
.insp-body::-webkit-scrollbar{width:3px;}
.insp-body::-webkit-scrollbar-thumb{background:var(--border-hi);}
.insp-meta{font-size:8px;color:var(--dim);padding:4px 14px;border-bottom:1px solid var(--border);}

/* ── Ledger panel (slides up from bottom-right) ───── */
.ledger-panel{
  position:fixed;bottom:0;right:0;width:440px;
  height:0;overflow:hidden;
  background:var(--s1);border-top:2px solid var(--purple);border-left:1px solid var(--border);
  transition:height .2s ease-out;z-index:60;
  display:flex;flex-direction:column;
}
.ledger-panel.open{height:55vh;}
.ledger-bar{
  flex-shrink:0;display:flex;align-items:center;gap:8px;
  padding:5px 14px;background:var(--s2);border-bottom:1px solid var(--border);
  font-size:9px;text-transform:uppercase;letter-spacing:1.5px;color:var(--purple);
}
.ledger-bar-close{margin-left:auto;cursor:pointer;color:var(--dim);}
.ledger-bar-close:hover{color:var(--text);}
.ledger-body{flex:1;overflow-y:auto;padding:10px 14px;font-size:9px;color:var(--text);white-space:pre-wrap;word-wrap:break-word;line-height:1.55;}
.ledger-body::-webkit-scrollbar{width:3px;}
.ledger-body::-webkit-scrollbar-thumb{background:var(--border-hi);}
</style>
</head>
<body>
<div class="shell" id="shell">

  <!-- Header -->
  <header class="hdr">
    <div class="hdr-logo">ATD <em>// LIVE</em></div>
    <div class="hdr-dot" id="hdr-dot"></div>
    <div class="hdr-tags" id="hdr-tags"></div>
    <div class="hdr-orch">
      <span class="orch-lbl">state:</span><span class="orch-state" id="orch-state">idle</span>
      <span class="orch-lbl">turn:</span><span class="orch-val" id="orch-turn">0</span>/<span class="orch-val" id="orch-max">—</span>
      <span class="orch-lbl">speaking:</span><span class="orch-val" id="orch-speaker">—</span>
      <span class="orch-lbl">challenges:</span><span class="orch-val" id="orch-challenges">0</span>
      <span class="orch-val" id="hdr-status">connecting...</span>
      <button class="mod-btn" style="font-size:9px;padding:2px 8px;margin-left:4px" onclick="toggleLedger()">Ledger</button>
    </div>
  </header>

  <!-- Roster -->
  <aside class="roster" id="roster">
    <div class="roster-label">Agents</div>
  </aside>

  <!-- Chat -->
  <div class="chat-wrap">
    <div class="messages" id="messages"></div>
    <div class="orch-bar" id="orch-bar">
      <span id="ob-brief">—</span>
      <span id="ob-mode">—</span>
      <span id="ob-msgs">0 messages</span>
    </div>
    <div class="mod-bar">
      <div class="mod-row">
        <input class="mod-input" id="mod-input" placeholder="Steer the conversation — agents will prioritize your message..." onkeydown="if(event.key==='Enter')sendMod()"/>
        <button class="mod-btn" onclick="sendMod()">Send</button>
      </div>
      <div class="mod-row">
        <input class="mod-input" id="q-input" placeholder="Add a question to the discussion queue (runs after current question)..." onkeydown="if(event.key==='Enter')addQuestion()" style="border-color:var(--cyan);opacity:.7"/>
        <button class="mod-btn" style="color:var(--cyan)" onclick="addQuestion()">Add Q</button>
      </div>
      <div class="mod-actions">
        <button class="mod-btn" onclick="modAction('refocus')">Refocus</button>
        <button class="mod-btn" onclick="modAction('deeper')">Go Deeper</button>
        <button class="mod-btn" onclick="modAction('move_on')">Move On</button>
        <button class="mod-btn" onclick="modAction('challenge')">Challenge This</button>
        <button class="mod-btn" onclick="modAction('summarize')">Summarize</button>
        <button class="mod-btn danger" onclick="modAction('pause')">Pause</button>
      </div>
    </div>
  </div>

  <!-- Agent detail panel -->
  <div class="detail" id="detail">
    <div class="detail-hdr">
      <span class="detail-close" onclick="closeDetail()">[×] close</span>
      <div class="d-name" id="det-name">—</div>
      <div class="d-role" id="det-role">—</div>
    </div>
    <div class="d-section" id="det-body"></div>
  </div>

</div>

<!-- Ledger panel -->
<div class="ledger-panel" id="ledger-panel">
  <div class="ledger-bar">
    DECISIONS LEDGER
    <span id="ledger-status" style="color:var(--dim);font-weight:normal;font-size:8px;text-transform:none;letter-spacing:0"></span>
    <span class="ledger-bar-close" onclick="closeLedger()">[×] close</span>
  </div>
  <div class="ledger-body" id="ledger-body">(no session running yet)</div>
</div>

<!-- Prompt inspector -->
<div class="inspector" id="inspector">
  <div class="insp-bar">
    PROMPT INSPECTOR
    <span class="insp-bar-close" onclick="closeInspector()">[×] close</span>
  </div>
  <div class="insp-meta" id="insp-meta"></div>
  <div class="insp-tabs">
    <button class="itab active" onclick="showTab(this,'response')" id="tab-response">Response</button>
    <button class="itab" onclick="showTab(this,'payload')">Context Sent</button>
    <button class="itab" onclick="showTab(this,'system')">System Prompt</button>
  </div>
  <div class="insp-body" id="insp-body"></div>
</div>

<script>
// AGENT_COLORS_JSON may override specific agent colors; all others auto-generated
const _COLOR_OVERRIDES = AGENT_COLORS_JSON;
const _PALETTE = ['#6366f1','#06b6d4','#f97316','#ef4444','#22c55e','#a855f7',
                  '#eab308','#ec4899','#14b8a6','#f43f5e','#3b82f6','#84cc16'];

// ── State ──────────────────────────────────────────────────────
let sessionTimeout = 120;
const agentTimers   = {};
const agentProfiles = {};     // key → {name,role,traits,drives,pushback_on,anti_slop,context_lens,...}
const agentMessages = {};     // key → [{text,turn,elapsed}]
const msgStore      = {};     // msgId → {agent,displayName,turn,systemPrompt,payload,response,elapsed}
const ctxStore      = {};     // ckey → {systemPrompt,payload}
const synthStore    = {};     // sid  → {question_num,question_title,round_context,system_prompt,full_doc,...}
let   synthIdCtr    = 0;
let   inspecting    = null;   // current msg/synth id in inspector
let   selectedAgent = null;
let   totalMessages = 0;
let   totalChallenges = 0;
let   currentTurn  = 0;
let   orchStateVal = 'idle';
let   msgIdCtr     = 0;

const messages  = document.getElementById('messages');
const roster    = document.getElementById('roster');
const hdrTags   = document.getElementById('hdr-tags');
const hdrStatus = document.getElementById('hdr-status');
const hdrDot    = document.getElementById('hdr-dot');
const shell     = document.getElementById('shell');

function esc(s){return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function push(html){messages.insertAdjacentHTML('beforeend',html);messages.scrollTop=messages.scrollHeight;}
function col(k){
  if(_COLOR_OVERRIDES[k]) return _COLOR_OVERRIDES[k];
  // deterministic hash → palette color
  let h=0; for(let i=0;i<k.length;i++) h=(h*31+k.charCodeAt(i))&0x7fffffff;
  return _PALETTE[h % _PALETTE.length];
}
function setOrch(state,extra){
  orchStateVal=state;
  const el=document.getElementById('orch-state');
  if(el){el.textContent=state;el.className='orch-state'+(state!=='idle'&&state!=='done'?' busy':'');}
  if(extra)for(const[k,v]of Object.entries(extra)){const t=document.getElementById('orch-'+k);if(t)t.textContent=v;}
}

// ── Roster: build agent row ───────────────────────────────────
function buildAgentRow(k, displayName, profile){
  const c = col(k);
  const div = document.createElement('div');
  div.className='arow';
  div.id='row-'+k;
  div.style.setProperty('border-left-color', c);
  div.onclick = ()=>selectAgent(k);

  let traitsHtml = '';
  if(profile && profile.traits){
    for(const[name,val] of Object.entries(profile.traits)){
      traitsHtml+=`<div class="trait-row">
        <span class="trait-lbl">${esc(name.replace(/_/g,' '))}</span>
        <div class="trait-bar"><div class="trait-fill" style="width:${val*100}%;background:${c}"></div></div>
        <span class="trait-val">${val.toFixed(1)}</span>
      </div>`;
    }
  }

  div.innerHTML=`
    <div class="arow-name" style="color:${c}">${esc(displayName)}</div>
    <div class="arow-role" id="role-${k}">${esc(profile&&profile.role||'')}</div>
    ${traitsHtml}
    <div class="arow-urgency">
      <div class="urg-bar"><div class="urg-fill" id="urgf-${k}"></div></div>
      <span class="urg-time" id="urgt-${k}"></span>
    </div>
    <div class="arow-status" id="astat-${k}">waiting</div>`;
  roster.appendChild(div);
}

function setAgentStatus(k, status){
  const el=document.getElementById('astat-'+k);
  if(el)el.textContent=status;
}

function startUrgency(k){
  const row=document.getElementById('row-'+k);
  if(row)row.classList.add('speaking');
  setAgentStatus(k,'speaking...');
  const t0=Date.now();
  const iv=setInterval(()=>{
    const sec=(Date.now()-t0)/1000;
    const pct=Math.min(sec/sessionTimeout,1);
    const bar=document.getElementById('urgf-'+k);
    const tim=document.getElementById('urgt-'+k);
    if(bar){bar.style.width=(pct*100)+'%';bar.style.background=pct<.5?'var(--green)':pct<.78?'var(--amber)':'var(--red)';}
    if(tim)tim.textContent=sec.toFixed(0)+'s';
  },200);
  agentTimers[k]={t0,iv};
}

function stopUrgency(k, elapsed, err){
  if(agentTimers[k]){clearInterval(agentTimers[k].iv);delete agentTimers[k];}
  const row=document.getElementById('row-'+k);
  if(row){row.classList.remove('speaking');if(err)row.classList.add('challenged');}
  const bar=document.getElementById('urgf-'+k);
  const tim=document.getElementById('urgt-'+k);
  if(bar){bar.style.width='0%';bar.style.background='var(--green)';}
  if(tim)tim.textContent='';
  setAgentStatus(k, (agentMessages[k]||[]).length+' msgs | '+elapsed+'s');
}

// ── Agent detail panel ────────────────────────────────────────
function selectAgent(k){
  if(selectedAgent===k){closeDetail();return;}
  selectedAgent=k;
  document.querySelectorAll('.arow').forEach(r=>r.classList.remove('selected'));
  const row=document.getElementById('row-'+k);
  if(row)row.classList.add('selected');
  shell.classList.add('detail-open');
  renderDetail(k);
}

function closeDetail(){
  selectedAgent=null;
  shell.classList.remove('detail-open');
  document.querySelectorAll('.arow').forEach(r=>r.classList.remove('selected'));
}

function renderDetail(k){
  const p=agentProfiles[k];
  const c=col(k);
  document.getElementById('det-name').innerHTML=`<span style="color:${c}">${esc(p&&p.name||k)}</span>`;
  document.getElementById('det-role').textContent=p&&p.role||'';
  const body=document.getElementById('det-body');
  if(!p){body.innerHTML='<div style="color:var(--dim);font-size:9px">Profile not yet loaded — waiting for first message</div>';return;}

  let h='';
  h+='<h3>Personality</h3>';
  for(const[n,v] of Object.entries(p.traits||{})){
    h+=`<div class="d-trait"><span class="dt-lbl">${esc(n.replace(/_/g,' '))}</span><div class="dt-bar"><div class="dt-fill" style="width:${v*100}%;background:${c}"></div></div><span class="dt-val">${v.toFixed(2)}</span></div>`;
  }
  if(p.cognitive_style||p.emotional_baseline){
    h+=`<h3>Character</h3>`;
    if(p.cognitive_style) h+=`<div class="d-item">cognitive: ${esc(p.cognitive_style)}</div>`;
    if(p.emotional_baseline) h+=`<div class="d-item">emotional: ${esc(p.emotional_baseline)}</div>`;
    if(p.job) h+=`<div class="d-item">job: ${esc(p.job)}</div>`;
  }
  if((p.drives||[]).length){
    h+='<h3>Drives</h3>';
    for(const d of p.drives) h+=`<div class="d-item drive">${esc(d)}</div>`;
  }
  if((p.pushback_on||[]).length){
    h+='<h3>Pushback on</h3>';
    for(const pb of p.pushback_on) h+=`<div class="d-item pushback">${esc(pb)}</div>`;
  }
  const slop=p.anti_slop||{};
  const rules=[];
  if(slop.agreement_tax) rules.push('Must add substance when agreeing');
  if(slop.perspective_lock) rules.push('Stay in character under pressure');
  if(slop.devils_advocate) rules.push('Argue the other side');
  if(slop.uncomfortable_quota>0) rules.push('Uncomfortable idea quota: '+slop.uncomfortable_quota);
  if(slop.domain_pivot) rules.push('Inject cross-domain perspectives');
  if(rules.length){
    h+='<h3>Active rules</h3>';
    for(const r of rules) h+=`<div class="d-item rule">${esc(r)}</div>`;
  }
  if(p.context_lens){
    h+='<h3>Context lens (injected each turn)</h3>';
    h+=`<div class="d-context">${esc(p.context_lens)}</div>`;
  }
  if(p.technique||p.voice_tone){
    h+='<h3>Technique & voice</h3>';
    if(p.technique) h+=`<div class="d-item">technique: ${esc(p.technique)}</div>`;
    if(p.voice_tone) h+=`<div class="d-item">voice: ${esc(p.voice_tone)}</div>`;
    if(p.intensity!==undefined) h+=`<div class="d-item">intensity: ${p.intensity}</div>`;
  }
  // Session stats
  const msgs=agentMessages[k]||[];
  h+='<h3>Session stats</h3>';
  h+=`<div class="d-stat"><span class="d-stat-lbl">messages</span><span class="d-stat-val">${msgs.length}</span></div>`;
  if(msgs.length) h+=`<div class="d-stat"><span class="d-stat-lbl">last spoke</span><span class="d-stat-val">turn ${msgs[msgs.length-1].turn||'?'}</span></div>`;

  // Recent messages
  if(msgs.length){
    h+='<h3>Recent responses</h3>';
    for(const m of msgs.slice(-5)){
      h+=`<div class="d-item" style="margin-bottom:4px;font-size:8px">`+
        `<span style="color:var(--dim)">turn ${m.turn||'?'} · ${m.elapsed||'?'}s</span><br>`+
        `${esc((m.text||'').substring(0,200))}${(m.text||'').length>200?'…':''}</div>`;
    }
  }
  body.innerHTML=h;
}

// ── Prompt inspector ──────────────────────────────────────────
let inspTab='response';
let inspData={};

function openInspector(mid){
  const d=msgStore[mid];
  if(!d)return;
  inspData=d;
  // Highlight message
  if(inspecting){
    const prev=document.getElementById(inspecting);
    if(prev)prev.classList.remove('inspected');
  }
  inspecting=mid;
  const el=document.getElementById(mid);
  if(el)el.classList.add('inspected');
  // Set meta
  const c=col(d.agent);
  document.getElementById('insp-meta').innerHTML=
    `<span style="color:${c}">${esc(d.displayName)}</span>` +
    ` &nbsp;·&nbsp; turn ${d.turn||'?'}` +
    ` &nbsp;·&nbsp; ${d.elapsed||'?'}s` +
    ` &nbsp;·&nbsp; Q${d.question||'?'} ${d.round||''}`;
  showTab(document.getElementById('tab-response'),'response');
  document.getElementById('inspector').classList.add('open');
}

function closeInspector(){
  document.getElementById('inspector').classList.remove('open');
  if(inspecting){
    const el=document.getElementById(inspecting);
    if(el)el.classList.remove('inspected');
    inspecting=null;
  }
}

function showTab(btn, tab){
  inspTab=tab;
  document.querySelectorAll('.itab').forEach(t=>t.classList.remove('active'));
  btn.classList.add('active');
  const body=document.getElementById('insp-body');
  if(tab==='response') body.textContent=inspData.response||'(no response yet)';
  else if(tab==='payload') body.textContent=inspData.payload||'(no payload captured)';
  else if(tab==='system') body.textContent=inspData.systemPrompt||'(no system prompt captured)';
}

// ── Moderator controls ────────────────────────────────────────
const MOD_ACTIONS={
  refocus:'MODERATOR DIRECTIVE: The discussion has drifted. Refocus on the original question. Do not introduce new topics until the current one is resolved.',
  deeper:'MODERATOR DIRECTIVE: Go deeper on the current thread. Do not move on yet. Challenge assumptions, name specific failure modes, and get concrete.',
  move_on:'MODERATOR DIRECTIVE: This subtopic is sufficiently explored. Move to the next important unresolved question. Do not rehash what was just discussed.',
  challenge:'MODERATOR DIRECTIVE: The current direction feels like premature agreement. Push back. What is being assumed without evidence? What failure mode is nobody naming?',
  summarize:'MODERATOR DIRECTIVE: Before continuing, each of you state in ONE sentence what you believe has been decided so far and what remains unresolved.',
  pause:'MODERATOR DIRECTIVE: Pause after this speaker. The moderator needs to review before it continues.',
};

function sendMod(){
  const inp=document.getElementById('mod-input');
  const msg=inp.value.trim();
  if(!msg)return;
  inp.value='';
  fetch('/moderator',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg})});
  push(`<div class="msg" style="border-left-color:var(--amber);background:rgba(245,166,35,.06)">
    <div class="msg-hdr"><span class="msg-name" style="color:var(--amber)">MODERATOR</span><span class="msg-time">${new Date().toLocaleTimeString('en',{hour:'2-digit',minute:'2-digit',second:'2-digit'})}</span></div>
    <div class="msg-body">${esc(msg)}</div>
  </div>`);
}

function modAction(a){
  const msg=MOD_ACTIONS[a];
  if(!msg)return;
  fetch('/moderator',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg})});
  push(`<div class="sys-row" style="border-left-color:var(--amber)">
    <div class="msg-hdr"><span class="msg-name" style="color:var(--amber)">MOD: ${a.toUpperCase().replace('_',' ')}</span></div>
  </div>`);
}

// ── Synthesis inspector ───────────────────────────────────────
function openSynthInspector(sid){
  const d=synthStore[sid];
  if(!d)return;
  inspData={
    agent:'synthesis',
    displayName:'Synthesis'+(d.question_num?' Q'+d.question_num:'')+(d.question_title?' — '+d.question_title.substring(0,40):''),
    turn:d.question_num,round:'synthesis',question:d.question_num,
    systemPrompt:d.system_prompt,
    payload:d.round_context,
    response:d.full_doc,
    elapsed:d.elapsed,
  };
  if(inspecting){const prev=document.getElementById(inspecting);if(prev)prev.classList.remove('inspected');}
  inspecting=sid;
  const el=document.getElementById(sid);
  if(el)el.classList.add('inspected');
  document.getElementById('insp-meta').innerHTML=
    `<span style="color:var(--purple)">SYNTHESIS</span>`+
    ` &nbsp;·&nbsp; Q${d.question_num||'?'}`+
    ` &nbsp;·&nbsp; ${d.elapsed||'?'}s`+
    ` &nbsp;·&nbsp; ${d.lines||'?'} lines`;
  showTab(document.getElementById('tab-response'),'response');
  document.getElementById('inspector').classList.add('open');
}

// ── Ledger panel ──────────────────────────────────────────────
function toggleLedger(){
  const p=document.getElementById('ledger-panel');
  if(p.classList.contains('open')){closeLedger();}else{p.classList.add('open');fetchLedger();}
}
function closeLedger(){document.getElementById('ledger-panel').classList.remove('open');}
function fetchLedger(){
  fetch('/ledger').then(r=>r.text()).then(t=>{
    document.getElementById('ledger-body').textContent=t||(t===''?'(ledger is empty)':'(no session running)');
    const ts=new Date().toLocaleTimeString('en',{hour:'2-digit',minute:'2-digit',second:'2-digit'});
    document.getElementById('ledger-status').textContent=' · '+ts;
  }).catch(()=>{document.getElementById('ledger-body').textContent='(error reading ledger)';});
}

// ── Question queue ────────────────────────────────────────────
function addQuestion(){
  const inp=document.getElementById('q-input');
  const msg=inp.value.trim();
  if(!msg)return;
  inp.value='';
  fetch('/questions/add',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:msg})});
  push(`<div class="sys-row" style="border-left-color:var(--cyan)">
    <div class="msg-hdr"><span class="msg-name" style="color:var(--cyan)">QUEUED</span><span class="msg-time">${new Date().toLocaleTimeString('en',{hour:'2-digit',minute:'2-digit',second:'2-digit'})}</span></div>
    <div class="msg-body">${esc(msg)}</div>
  </div>`);
}

// ── SSE ───────────────────────────────────────────────────────
const es=new EventSource('/events');
es.onopen=()=>{hdrStatus.textContent='live';};
es.onerror=()=>{
  hdrDot.style.background='var(--red)';hdrDot.style.animation='none';
  hdrStatus.textContent='disconnected';
};
es.onmessage=e=>{try{onEvent(JSON.parse(e.data));}catch(ex){console.error(ex);}};

function onEvent(ev){
  switch(ev.type){

    case 'session_start':
      sessionTimeout=ev.timeout||120;
      hdrTags.innerHTML=
        `<span class="tag">${esc(ev.brief)}</span>`+
        `<span class="tag">${esc(ev.mode)}</span>`+
        `<span class="tag">${ev.question_count} q</span>`;
      hdrStatus.textContent='running';
      document.getElementById('ob-brief').textContent=ev.brief;
      document.getElementById('ob-mode').textContent=ev.mode;
      setOrch('running',{max:ev.question_count||'—'});
      // Build roster (may not have profiles yet — just names)
      const names=ev.display_names||{};
      for(const k of (ev.agents||[])){
        agentProfiles[k]=agentProfiles[k]||null;
        agentMessages[k]=agentMessages[k]||[];
        buildAgentRow(k, names[k]||k, null);
      }
      break;

    case 'agent_profile': {
      agentProfiles[ev.key]=ev;
      agentMessages[ev.key]=agentMessages[ev.key]||[];
      const existingRow=document.getElementById('row-'+ev.key);
      if(existingRow){
        // Rebuild in-place with full profile data
        const c2=col(ev.key);
        let th='';
        if(ev.traits){for(const[n,v] of Object.entries(ev.traits)){th+=`<div class="trait-row"><span class="trait-lbl">${esc(n.replace(/_/g,' '))}</span><div class="trait-bar"><div class="trait-fill" style="width:${v*100}%;background:${c2}"></div></div><span class="trait-val">${v.toFixed(1)}</span></div>`;}}
        existingRow.innerHTML=`
          <div class="arow-name" style="color:${c2}">${esc(ev.name||ev.key)}</div>
          <div class="arow-role" id="role-${ev.key}">${esc(ev.role||'')}</div>
          ${th}
          <div class="arow-urgency"><div class="urg-bar"><div class="urg-fill" id="urgf-${ev.key}"></div></div><span class="urg-time" id="urgt-${ev.key}"></span></div>
          <div class="arow-status" id="astat-${ev.key}">waiting</div>`;
      } else {
        buildAgentRow(ev.key, ev.name||ev.key, ev);
      }
      if(selectedAgent===ev.key) renderDetail(ev.key);
      break;
    }

    case 'question_start':
      currentTurn++;
      setOrch('running',{turn:ev.number});
      push(`<div class="sys-row q-start">
        <div class="msg-hdr">
          <span class="msg-name">Q${ev.number} / ${ev.total}</span>
          <span class="msg-time">${ev.time||''}</span>
        </div>
        <div class="msg-body">${esc(ev.title)}</div>
      </div>`);
      break;

    case 'round_start':
      push(`<div class="sys-row round-sep">
        <div class="msg-hdr">
          <span class="msg-name">${esc(ev.round)}</span>
          <span class="msg-meta">${esc(ev.agents||'')}</span>
        </div>
      </div>`);
      break;

    case 'agent_context': {
      const ck=ev.agent+'::'+ev.question+'::'+ev.round;
      ctxStore[ck]={systemPrompt:ev.system_prompt||'',payload:ev.payload||''};
      break;
    }

    case 'agent_thinking': {
      // Remove old thinking row for this agent if any
      const old=document.getElementById('think-'+ev.agent);
      if(old)old.remove();
      push(`<div class="sys-row thinking-row" id="think-${ev.agent}">
        <div class="msg-hdr">
          <span class="msg-name" style="color:${col(ev.agent)}">${esc(ev.display_name)}</span>
          <span class="msg-meta">${ev.round||''}</span>
        </div>
        <div class="msg-body">thinking</div>
      </div>`);
      startUrgency(ev.agent);
      setOrch('thinking',{speaker:ev.display_name.replace(/^The /,'').split('(')[0].trim()});
      break;
    }

    case 'agent_response': {
      // Remove thinking row
      const th=document.getElementById('think-'+ev.agent);
      if(th)th.remove();
      stopUrgency(ev.agent, ev.elapsed, ev.error);
      totalMessages++;
      document.getElementById('ob-msgs').textContent=totalMessages+' messages';

      // Store for inspector
      const mid='m'+(msgIdCtr++);
      const ck=ev.agent+'::'+ev.question+'::'+ev.round;
      const ctx=ctxStore[ck]||{};
      msgStore[mid]={
        agent:ev.agent, displayName:ev.display_name||ev.agent,
        turn:ev.question, round:ev.round||'?',
        question:ev.question,
        systemPrompt:ctx.systemPrompt||'',
        payload:ctx.payload||'',
        response:ev.response||'',
        elapsed:ev.elapsed,
      };
      if(agentMessages[ev.agent]) agentMessages[ev.agent].push({text:ev.response,turn:ev.question,elapsed:ev.elapsed});
      if(selectedAgent===ev.agent) renderDetail(ev.agent);

      const c=col(ev.agent);
      push(`<div class="msg" id="${mid}" style="border-left-color:${c}" onclick="openInspector('${mid}')">
        <div class="msg-hdr">
          <span class="msg-name" style="color:${c}">${esc(ev.display_name)}</span>
          <span class="msg-time">${ev.time||''}</span>
          <span class="msg-meta">${ev.elapsed}s · Q${ev.question||'?'} ${ev.round||''} · <span style="color:var(--amber)">inspect</span></span>
        </div>
        <div class="msg-body">${esc(ev.response||'[empty]')}</div>
      </div>`);
      setOrch('running',{speaker:'—'});
      break;
    }

    case 'synthesis_start':
      push(`<div class="sys-row synthesis">
        <div class="msg-hdr"><span class="msg-name">SYNTHESIS</span><span class="msg-meta">compiling...</span></div>
      </div>`);
      setOrch('thinking',{speaker:'synthesis'});
      break;

    case 'synthesis_done': {
      const sid='synth'+(synthIdCtr++);
      synthStore[sid]={
        question_num:ev.question_num,
        question_title:ev.question_title||'',
        round_context:ev.round_context||'',
        system_prompt:ev.system_prompt||'',
        full_doc:ev.full_doc||ev.preview||'',
        elapsed:ev.elapsed, lines:ev.lines,
      };
      push(`<div class="sys-row synthesis" id="${sid}" onclick="openSynthInspector('${sid}')" style="cursor:pointer">
        <div class="msg-hdr">
          <span class="msg-name">SYNTHESIS COMPLETE</span>
          <span class="msg-meta">${ev.lines} lines · ${ev.elapsed}s · Q${ev.question_num||'?'} · <span style="color:var(--amber)">inspect</span></span>
        </div>
        <div class="msg-body">${esc((ev.preview||'').substring(0,300))}${(ev.preview||'').length>300?'…':''}</div>
      </div>`);
      setOrch('running',{speaker:'—'});
      break;
    }

    case 'ledger_extracted':
      push(`<div class="sys-row ok">
        <div class="msg-hdr">
          <span class="msg-name">LEDGER</span>
          <span class="msg-meta">Q${ev.question}</span>
        </div>
        <div class="msg-body">${ev.count} decisions extracted</div>
      </div>`);
      if(document.getElementById('ledger-panel').classList.contains('open')) fetchLedger();
      break;

    case 'question_queued':
      push(`<div class="sys-row" style="border-left-color:var(--cyan)">
        <div class="msg-hdr"><span class="msg-name" style="color:var(--cyan)">Q${ev.number} QUEUED</span><span class="msg-time">${ev.time||''}</span></div>
        <div class="msg-body">${esc(ev.title)}</div>
      </div>`);
      break;

    case 'question_done':
      push(`<div class="sys-row ok">
        <div class="msg-hdr">
          <span class="msg-name">Q${ev.number} DONE</span>
          <span class="msg-meta">${ev.elapsed}s</span>
        </div>
      </div>`);
      setOrch('running');
      break;

    case 'question_failed':
      push(`<div class="sys-row err">
        <div class="msg-hdr"><span class="msg-name">Q${ev.number} FAILED</span></div>
        <div class="msg-body">${esc(ev.reason)}</div>
      </div>`);
      break;

    case 'challenge': {
      totalChallenges++;
      setOrch(orchStateVal,{challenges:totalChallenges});
      const tc=document.getElementById('row-'+ev.target);
      if(tc)tc.classList.add('challenged');
      push(`<div class="sys-row challenge">
        <div class="msg-hdr"><span class="msg-name">CHALLENGE</span><span class="msg-time">${ev.time||''}</span></div>
        <div class="msg-body">${esc(ev.from_name||'?')} → ${esc(ev.target_name||'?')}: ${esc(ev.description||'')}</div>
      </div>`);
      break;
    }

    case 'brief_start':
      push(`<div class="sys-row synthesis">
        <div class="msg-hdr"><span class="msg-name">MORNING BRIEF</span><span class="msg-meta">generating...</span></div>
      </div>`);
      break;

    case 'brief_done':
      push(`<div class="sys-row synthesis">
        <div class="msg-hdr"><span class="msg-name">MORNING BRIEF READY</span></div>
        <div class="msg-body">${esc((ev.preview||'').substring(0,400))}${(ev.preview||'').length>400?'…':''}</div>
      </div>`);
      break;

    case 'session_done':
      hdrTags.innerHTML+=`<span class="tag" style="border-color:var(--green);color:var(--green)">DONE ${esc(ev.elapsed)} · ${ev.completed}/${ev.total}</span>`;
      hdrDot.style.background='var(--green)';hdrDot.style.animation='none';
      hdrStatus.textContent='complete';
      setOrch('done');
      break;

    // live_conversation events
    case 'conversation_start':
      sessionTimeout=60;
      hdrStatus.textContent='running';
      if(ev.agent_colors)Object.assign(_COLOR_OVERRIDES,ev.agent_colors);
      setOrch('running',{max:ev.max_turns});
      for(const a of (ev.agent_profiles||[])){
        agentProfiles[a.key]=a;
        agentMessages[a.key]=[];
        buildAgentRow(a.key, a.name||a.key, a);
      }
      push(`<div class="sys-row q-start">
        <div class="msg-hdr"><span class="msg-name">CONVERSATION</span></div>
        <div class="msg-body">${esc(ev.question)}</div>
      </div>`);
      break;

    case 'agent_speaking':
      {const old2=document.getElementById('think-'+ev.agent);if(old2)old2.remove();}
      push(`<div class="sys-row thinking-row" id="think-${ev.agent}">
        <div class="msg-hdr"><span class="msg-name" style="color:${col(ev.agent)}">${esc(ev.display_name)}</span></div>
        <div class="msg-body">thinking</div>
      </div>`);
      startUrgency(ev.agent);
      setOrch('thinking',{speaker:ev.display_name.replace(/^The /,'').split('(')[0].trim()});
      break;

    case 'agent_spoke': {
      const th2=document.getElementById('think-'+ev.agent);if(th2)th2.remove();
      stopUrgency(ev.agent, ev.elapsed, false);
      totalMessages++;
      document.getElementById('ob-msgs').textContent=totalMessages+' messages';
      const mid2='m'+(msgIdCtr++);
      msgStore[mid2]={
        agent:ev.agent,displayName:ev.display_name||ev.agent,
        turn:ev.turn,round:'turn',question:ev.turn,
        systemPrompt:ev.system_prompt||'',payload:ev.user_payload||'',
        response:ev.response||'',elapsed:ev.elapsed,
      };
      if(agentMessages[ev.agent])agentMessages[ev.agent].push({text:ev.response,turn:ev.turn,elapsed:ev.elapsed});
      if(selectedAgent===ev.agent)renderDetail(ev.agent);
      const c2=col(ev.agent);
      push(`<div class="msg" id="${mid2}" style="border-left-color:${c2}" onclick="openInspector('${mid2}')">
        <div class="msg-hdr">
          <span class="msg-name" style="color:${c2}">${esc(ev.display_name)}</span>
          <span class="msg-time">${ev.time||''}</span>
          <span class="msg-meta">turn ${ev.turn} · ${ev.elapsed}s · ctx:${ev.context_messages||0} · <span style="color:var(--amber)">inspect</span></span>
        </div>
        <div class="msg-body">${esc(ev.response||'')}</div>
      </div>`);
      setOrch('running',{turn:ev.turn,speaker:'—'});
      break;
    }

    case 'turn_start':
      setOrch('running',{turn:ev.turn,max:ev.max_turns});
      break;

    case 'urgency_update':
      for(const[k,v] of Object.entries(ev)){
        if(k==='type'||k==='time')continue;
        const bar=document.getElementById('urgf-'+k);
        if(bar){
          const pct=Math.min(v/1.5*100,100);
          bar.style.width=pct+'%';
          bar.style.background=v>=0.5?'var(--red)':v>=0.3?'var(--amber)':'var(--green)';
        }
        if(v>=0.5){const r=document.getElementById('row-'+k);if(r)r.classList.add('challenged');}
      }
      break;

    case 'system_message':
      {
        const isChallenge=ev.message&&ev.message.startsWith('Challenge detected:');
        if(isChallenge){
          totalChallenges++;
          setOrch(orchStateVal,{challenges:totalChallenges});
        }
        push(`<div class="sys-row${isChallenge?' challenge':''}">
          <div class="msg-hdr"><span class="msg-name">${isChallenge?'CHALLENGE':'SYS'}</span><span class="msg-time">${ev.time||''}</span></div>
          <div class="msg-body">${esc(ev.message)}</div>
        </div>`);
      }
      break;

    case 'synthesis_update':
      push(`<div class="sys-row synthesis">
        <div class="msg-hdr"><span class="msg-name">SYNTHESIS (turn ${ev.turn})</span></div>
        <div class="msg-body">mood: ${esc(ev.mood)} · exhaustion: ${esc(ev.exhaustion)}${ev.top_insight?' · '+esc(ev.top_insight.substring(0,120)):''}</div>
      </div>`);
      break;

    case 'conversation_done':
      hdrDot.style.background='var(--green)';hdrDot.style.animation='none';
      hdrStatus.textContent='complete';
      setOrch('done',{speaker:'—'});
      push(`<div class="sys-row ok">
        <div class="msg-hdr"><span class="msg-name">CONVERSATION DONE</span></div>
        <div class="msg-body">${ev.turns} turns · ${esc(ev.elapsed)}</div>
      </div>`);
      break;
  }
}
</script>
</body>
</html>"""


class LiveEmitter:
    """Thread-safe append-only event list. Call emit() from any thread."""

    def __init__(self):
        self._events: list[dict] = []
        self._lock = threading.Lock()
        self._moderator_queue: list[str] = []
        self._question_queue: list[str] = []
        self._session_dir = None

    def set_session_dir(self, path):
        with self._lock:
            self._session_dir = path

    def emit(self, event_type: str, data: dict):
        event = {"type": event_type, "time": datetime.now().strftime("%H:%M:%S"), **data}
        with self._lock:
            self._events.append(event)

    def snapshot_from(self, pos: int) -> tuple[list[dict], int]:
        with self._lock:
            end = len(self._events)
        return self._events[pos:end], end

    def queue_moderator(self, message: str):
        with self._lock:
            self._moderator_queue.append(message)

    def pop_moderator(self) -> str | None:
        with self._lock:
            return self._moderator_queue.pop(0) if self._moderator_queue else None

    def queue_question(self, text: str):
        with self._lock:
            self._question_queue.append(text)

    def pop_question(self) -> str | None:
        with self._lock:
            return self._question_queue.pop(0) if self._question_queue else None


class _LiveHandler(BaseHTTPRequestHandler):

    emitter: "LiveEmitter" = None

    def log_message(self, fmt, *args):
        pass

    def do_GET(self):
        if self.path == "/":
            page = _HTML.replace("AGENT_COLORS_JSON", json.dumps(AGENT_COLORS))
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(page.encode("utf-8"))
        elif self.path == "/events":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            pos = 0
            while True:
                try:
                    new_events, pos = self.emitter.snapshot_from(pos)
                    if new_events:
                        for ev in new_events:
                            self.wfile.write(f"data: {json.dumps(ev)}\n\n".encode())
                        self.wfile.flush()
                    else:
                        self.wfile.write(b": keepalive\n\n")
                        self.wfile.flush()
                    time.sleep(0.4)
                except (BrokenPipeError, ConnectionResetError, OSError):
                    break
        elif self.path == "/ledger":
            text = ""
            try:
                session_dir = self.emitter._session_dir
                if session_dir:
                    from agentteam.session.ledger import get_ledger_path
                    lp = get_ledger_path(session_dir)
                    if lp.exists():
                        text = lp.read_text(encoding="utf-8")
            except Exception:
                pass
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(text.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/moderator":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body)
                msg = data.get("message", "").strip()
                if msg and self.emitter:
                    self.emitter.queue_moderator(msg)
                    self.emitter.emit("moderator_message", {"text": msg})
            except Exception:
                pass
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"ok":true}')
        elif self.path == "/questions/add":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body)
                text = data.get("text", "").strip()
                if text and self.emitter:
                    self.emitter.queue_question(text)
            except Exception:
                pass
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"ok":true}')
        else:
            self.send_response(404)
            self.end_headers()


def start_live_server(emitter: LiveEmitter, port: int = 8899) -> HTTPServer:
    """Start the HTTP server on a daemon thread. Returns the server instance."""

    class BoundHandler(_LiveHandler):
        pass
    BoundHandler.emitter = emitter

    server = HTTPServer(("0.0.0.0", port), BoundHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server
