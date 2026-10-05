1. **The open question is being answered before the trigger exists, so three months of integration work gets built on a signal nobody emits.** research-engine.md fires on an agent footer value "needs: more-research", but the packet says the running engine has no moderator channel, no phase system, no rolling synthesis, and agents are one-shot `claude -p` calls. The context-assembly template's footer was never compliance-tested (its own "open prerequisite": 50 calls, 90% threshold). In practice the trigger fires unreliably, retries fire on a path that was never measured, and nobody can tell whether a missing research result is a parse failure or a real "no."

2. **Research findings land in a context payload that is already over budget, and the trim logic will delete them first or crowd out the ledger.** The engine trims at ~10k tokens; the template assumes a 4k ceiling and a Section 1-7 layout the engine does not implement (no moderator override, no takeaways, no phase briefing). research-scope-controls allows a 2k output per call and 2 calls per agent; with six agents that is up to 24k tokens of findings per session competing with decisions ledger, previous-doc headings and open questions. At 3 AM the budget enforcer silently trims whichever section is "unprotected", and research is by definition new and unprotected.

3. **Between-round visibility is Position Summary only (3 sentences), so a research result produced mid-round is invisible to every agent who needs it.** Evidence either reaches only later speakers in the same round or gets compressed away before the next round. The finding then never influences the debate, and the ROI signal in scope-controls ("did the agent use it next round") reads zero, which kills the feature.

4. **Research results contaminate the decisions ledger as if they were decisions.** The ledger chains DECIDED/CONTESTED/OPEN forward across questions and has never produced a real ledger before 2026-10-05. An unverified web snippet cited by one persona becomes a DECIDED line and propagates to later questions. Failure mode: a wrong "fact" with no provenance survives into design docs, and the Evaluator (which scores but is read by nothing) never catches it.

5. **Caching and scope controls were designed in isolation from the real call model.** "Cache within a session" and "2 calls per agent per session" assume persistent state; each turn is stateless. The sub-agent itself is a second `claude -p` with web access: its failure, timeout or hallucinated citation has no defined result, only "skip and log," so the debate proceeds as if research never happened.

6. **Solo developer, 17 sessions on disk, none with a real ledger: the integration will be tuned against zero data.** Every number (15k in, 2k out, 204k total) comes from a synthesized panel document, not measurement.

Undecided, author-only:
- Is research output evidence (attached to a claim) or a participant (a speaker)? That choice sets everything else.
- Does research block the turn or arrive a round late?
- Who owns provenance: does a finding ever enter the ledger?
- Should this wait until the ledger demonstrably works across one real multi-question session?
