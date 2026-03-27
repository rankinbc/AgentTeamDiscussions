### The Cognitive Architect (creativity engine designer)

## Morning Brief: Incremental Assembly with Critic-Extracted Risk Flags

**Core commitment: generate incrementally, assemble at the end.**

After each question completes, generate a micro-brief (3-5 bullets) while the context is narrow and fresh. This sidesteps the 10-doc overflow problem entirely — you never feed everything at once. At session end, a lightweight assembly pass synthesizes micro-briefs into the final document.

**Per-question micro-brief prompt (fed immediately after synthesis):**
```
Given this question: {question}
Design decision reached: {design_doc excerpt, ~500 tokens}
Critic challenges that were NOT resolved: {unresolved_flags}

Generate 3-5 bullets covering:
- What was decided and why it beat alternatives
- The strongest unresolved objection (if any)
- What this decision constrains downstream
```

**Risk flag extraction** happens during critique rounds, not retrospectively. The orchestrator tags any critic turn containing uncertainty markers (`"but what if"`, `"this assumes"`, `"unresolved"`, `"depends on"`) as a candidate flag. The micro-brief prompt receives only those tagged excerpts — not full transcripts.

**Final assembly prompt** receives only the micro-briefs (trivially small) plus session metadata:
```
Synthesize these per-question briefs into one Morning Brief.
Lead with: what surprised us. End with: what's still unresolved.
```

**Fallback**: If final assembly fails, concatenate micro-briefs directly. They're readable as-is. Graceful degradation, not silent failure.

**Why incremental beats all-at-once:** Recency bias works *for* you here. The micro-brief captures the critique energy while it's hot. All-at-once flattens that signal.

### The Flow Orchestrator (mechanical flow designer)

## Flow Orchestrator Response: Cut the Assembly Pass

The incremental approach is correct. The fallback reveals the real answer.

**The Cognitive Architect's own fallback — concatenate micro-briefs directly — is the design.** If micro-briefs are "readable as-is," the final assembly LLM call is pure overhead. It adds a failure mode, a latency spike at session end, and another prompt to maintain. Cut it.

**Exact sequence I'd commit to:**

1. Question N completes → synthesis output written to disk
2. Immediately: feed `{question}` + `{synthesis excerpt, 500 tokens}` to micro-brief prompt
3. Append 3-5 bullet output to `morning_brief.md`
4. Repeat for N+1
5. Session ends → `morning_brief.md` is complete. No assembly step.

**Flag on the risk extraction:** "The orchestrator tags critic turns containing uncertainty markers" is hand-waving. What triggers the scan — after every critic turn? After all critique rounds complete? What's the data structure? I'd simplify: the micro-brief prompt already asks "strongest unresolved objection" — that pulls it forward without regex fragility. Drop the tagging mechanism entirely.

**What this gives you:** Two LLM calls per question (synthesis + micro-brief), zero end-of-session call, graceful degradation built-in, no context overflow ever. The brief is assembled continuously, not retrospectively.

**One open question worth flagging:** If a micro-brief call fails mid-session, do we block or skip? The sequence needs a defined answer before implementation.


<!-- complete -->
