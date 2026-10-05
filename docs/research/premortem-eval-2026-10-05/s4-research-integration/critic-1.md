1. **The research engine gets built before anything that would carry its results exists.** The ROADMAP critical path lists blind proposals, phases, takeaways and stale detection, and Research Engine is not on it. The engine facts say there is no phase system, no moderator channel, no live synthesis, and no research engine, so there is nothing to attach results to. The unstated assumption is that a "situation layer" exists. In the running code it is a flat list of sections trimmed by a ~10k budget enforcer. The first research integration becomes a special case bolted on, and it gets rewritten when phases arrive.

2. **Research results will be trimmed away or crowd out the discussion.** The idea doc says results must be "concise enough" not to displace history, but it never says which section they belong to or whether they are protected. If they are unprotected, the budget enforcer cuts them. If they are protected, they push out the ledger or discussion history. The context-assembly template contradicts itself: it sets a 4,000-token ceiling while the engine runs at ~10k. Nobody has said which number governs. Research-scope-controls adds 2k output per call and 2 calls per agent per session. Six agents can therefore add up to 24k tokens, which is more than twice the budget.

3. **Findings lose their value at the round boundary.** Between rounds agents see only 3-sentence Position Summaries. A research finding cited in round 1 survives only if the speaker restates it in that summary. Otherwise the critique round debates claims whose evidence is gone, and the ledger records DECIDED lines with no provenance. The docs never say whether findings are persisted, cached per session as the idea doc claims, or re-injected.

4. **The trigger mechanism is unbuilt and unreliable.** The idea doc triggers research from a `needs: more-research` agent signal. That signal depends on the footer, and the template's own open prerequisite is a 50-call compliance test that has not been run. Agents emit this signal in free text. Failures are skipped silently by policy ("skip and log"), so research never fires and nobody notices.

5. **Nothing measures whether research helped.** Research-scope-controls names "did the agent use the result" as the key ROI signal. The Evaluator scores 1-10, and nothing reads those scores back. A solo developer with 17 sessions has no baseline to detect improvement, so the feature is judged on vibes and abandoned.

6. **The research-scope-controls "spec" is not a spec.** It is a chat transcript saying "it looks like I need write permission". It also leaves result integration as an explicit scope exclusion, which is this exact open question, and it lists 2 blocking open items.

**Still undecided (only the author can answer):**
- Do findings go to the system prompt, a protected payload section, or attach to the ledger?
- Which token ceiling is the real one, 4k or 10k?
- Are findings shared across all agents or visible only to the requester?
- Can an agent's research answer contradict a DECIDED ledger line, and who wins?
- Is the solo developer willing to pay roughly 200k extra tokens per session, and for what measurable gain?
