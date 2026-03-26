### The Cognitive Architect (creativity engine designer)

## Incremental Fragment Architecture

The fundamental error in brief generation is treating it as end-of-session compression. That's the wrong mental model. What you actually want is **progressive crystallization** — the brief *accretes* during the session, not after it.

**The mechanism:**

After each question resolves, a lightweight extractor runs on that question's transcript and design doc. It produces a **Brief Fragment**: one key decision (with confidence signal), one surviving tension that critique didn't resolve, and any risk flags that critics raised but evaluators didn't dismiss. Fragments are ~100 tokens each. Cheap. Reliable. Composable.

At session end, the Morning Brief assembles from **fragments + decisions.json**, not raw design docs. Context problem solved structurally, not by truncation heuristics.

**The prompt:**

```
You are synthesizing a product design session for a human who will 
read this over coffee. They need: what got decided, what's still 
uncertain, and what could go wrong. 

Inputs: [N fragments] + [decisions.json]
Sections: Decisions Made | Open Tensions | Risk Watch List

Be specific. Skip process. Surface the one thing they need to 
worry about first.
```

**Risk flag extraction** should happen *during* critique rounds — critics emit structured flags (`RISK: [type] [description]`), evaluators vote to dismiss or elevate. Only elevated flags reach the brief.

**Fallback:** fragments concatenated with headers. Ugly but readable. The session never returns nothing.

The insight from distributed cognition research: synthesis quality comes from *representation diversity across time*, not volume at the end.

### The Flow Orchestrator (mechanical flow designer)

## Agree on fragments. Cut the risk flag protocol.

The Cognitive Architect is right that end-of-session compression is the wrong model. Fragments solve the context problem structurally. I'll take that.

But the risk flag mechanism — critics emitting `RISK: [type]`, evaluators voting to dismiss or elevate — is a new sub-protocol bolted onto the critique round. That's scope. Cut it.

**The actual sequence, minimal:**

**After each question resolves:**
1. Fragment extractor runs on `transcript.md` + `design_doc.md` for that question
2. One LLM call. Output: `{decision: str, tension: str}` — two fields, nothing more
3. Append to `fragments.jsonl`

Risk flags are already in the design doc. They don't need a separate extraction pipeline.

**At session end:**
1. Load all fragments from `fragments.jsonl` + `decisions.json`
2. Single LLM call → `morning_brief.md`

**The prompt (lean version):**
```
Synthesize this product design session for a human reading over coffee.

Decisions: [decisions.json]
Key fragments: [N x {decision, tension}]

Output:
## What Got Decided
## What's Still Open  
## The One Thing To Watch

Be specific. 300 words max.
```

**Fallback if the call fails:** write fragments to `morning_brief.md` with section headers. User gets something readable. Session never exits empty.

**Decision point I need answered:** Does the fragment extractor run inline (blocking question N+1) or async? If questions chain forward and Q2 needs Q1's design doc, the fragment extraction can run async after the design doc is written — it doesn't block Q2's context assembly.

That ordering matters. Flag it now.


<!-- complete -->
