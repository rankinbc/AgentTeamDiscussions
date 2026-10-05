## What breaks

1. **Research got wired into a context template the engine does not run.** research-engine.md sends findings to the "situation layer" of context-assembly-template.md, which has a 4k ceiling, takeaways, tombstones and a `---signals---` footer. The real engine has none of these: its sections are persona, lens, overlay, brief, ledger, doc headings, open questions and discussion, under a ~10k trimmer (engine facts). Neither design has a research slot.

2. **The research budget and the context budget cannot both hold.** research-scope-controls.md allows 2 calls per agent at 2k output each, so six agents can produce about 24k of findings against a 4k or ~10k per-turn ceiling. If findings are unprotected, the trimmer cuts them first and they are paid for but never seen. If protected, they push out history, breaking research-engine.md's "must not displace discussion history".

3. **Nothing triggers research.** The trigger is `needs: more-research`, but the engine parses no footer and the template's footer has no research field. The template requires a 50-call compliance test before any footer logic, and research-scope-controls.md marks "thinking routine templates" as blocking, though they do not exist.

4. **The round structure wipes out findings before peers see them.** Between rounds, agents see only 3-sentence Position Summaries (engine facts), so a finding from round 1 reaches round 2 only if the requester restates it. That makes the plan's main ROI signal, "did the agent use research next round", near zero or unmeasurable.

5. **Wrong research hardens into DECIDED.** The ledger chains forward across questions (engine facts), and findings are cached only per session (research-engine.md). Truncated or skipped results ("skip and log", 2k cap) can become uncited DECIDED lines that nothing can audit or expire.

6. **The integration design has no owner.** research-scope-controls.md explicitly excludes "result integration", and the file is a chat transcript asking for write permission, not a spec. ROADMAP.md lists Research Engine as V2, puts research-findings context management under Vision, and leaves research out of the critical path.

7. **Nobody could tell whether research helped.** The Evaluator has no grounding dimension and its scores feed back into nothing (engine facts). Sessions run only occasionally and the ledger has been real only since 2026-10-05. A solo developer paying for extra web-enabled `claude -p` calls with no visible gain drops the feature.

## Undecided

- Visibility: does a finding go to the requester only, the current round, or all later rounds and questions?
- Placement: which section findings go in, how many tokens they get, and their cut priority under the real ~10k trimmer.
- Trigger: is it an agent signal, an orchestrator decision, or a pre-discussion research pass driven by the brief?
- Timing: does research block the turn (synchronous), or do results arrive for a later turn?
- Citation: what format and citation lets design docs and the ledger tell sourced claims from opinion?
- Time limits: research-engine.md wants them, but research-scope-controls.md says "no time limits".
- Tool access: how web tools get permission inside a `claude -p` subprocess.
- Caching: whether findings persist across questions and sessions, and how they expire.

## Questions for you

- Is context-assembly-template.md still the target, or is the current engine's assembly the real baseline?
- Would running research before discussion, as brief preparation, satisfy your goal better than mid-turn lookups?
- Should agents see findings that contradict them, or only the synthesis step?
- Can a research-backed claim become DECIDED, and must it carry a source?
- What evidence would convince you research was worth its cost?
- Does research come before or after blind proposals and the phase system?
- Will you allow live web access in unattended sessions?
