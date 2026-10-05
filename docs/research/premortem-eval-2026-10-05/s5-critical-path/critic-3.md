1. **The path ships three invisible-to-the-user mechanisms (stale detection, anti-sycophancy measurement, manifest versioning) and the Morning Brief reader never notices any of them.** From the user's perspective, the moment that matters is the 10 PM idea turning into a brief worth reading. The roadmap's own stated rule is "start with what changes what the user reads", yet steps 2, 5 and 6 are schema, measurement and signals. The retention question is whether the brief got better, and nothing after step 1 is wired to that.

2. **Measurement-only features feed nothing, so they die as dead telemetry.** The engine facts say the Evaluator already scores 7 and 10 dimensions and "nothing reads those scores back". Anti-sycophancy detection (step 6) is explicitly "measurement only" and would repeat the pattern. The roadmap's own open question, "how does evaluation feed back into agent behavior", is unanswered, and step 6 is built before anyone answers it. Would the user tune this or ignore it? Ignore it.

3. **Blind proposals is treated as a 1-2 day win, but its value is unproven against the actual output.** Between rounds agents already see only 3-sentence Position Summaries, so context is partly suppressed already. Nobody has said what the user would read differently. Without a before/after comparison on the 17 existing sessions, there is no way to tell whether the "highest immediate user value" claim held. Three months on, the likely verdict is "same brief, plus a flag".

4. **Phase system is estimated at 2-3 days but is the largest unknown, and steps 4 and 5 depend on it.** Takeaways "at phase boundaries" and stale detection "across phase boundaries" both need phases. The engine has no phase system and no moderator channel, and the transition trigger (time, convergence or round count) is an open question. The 2-3 day estimate looks like the planning-fallacy number that slips and stalls steps 4-6 behind it. The implementation-gaps doc itself calls phases "Large" and defers them.

5. **The plan contradicts itself on which context the build rests on.** The gaps doc describes `live_conversation.py` chat mode with voting side-channels, orchestrator cadence and footers. The engine is C# with fixed rounds and one synthesis call. The roadmap was written against a different architecture. Key takeaway voting (blocking, 5 calls per proposal) has no home in a round-based engine. Expect rework discovered mid-build.

6. **The ledger never produced real output before 2026-10-05, so the foundation is untested.** Takeaways, stale detection and drift all assume trustworthy DECIDED / CONTESTED / OPEN chaining. With no real ledger ever generated, the first sessions will surface bugs in the ledger, not the roadmap items.

**What only the author can answer:**
- What does the user actually do with a Morning Brief, and which single change would they notice first?
- Is the target a single-sitting overnight run or multi-phase sessions?
- Which of the roadmap's phase-trigger options is acceptable, and does the Evaluator get to change persona behavior?
- Is the BIT "parallel track" real capacity for a solo developer, or a distraction from the critical path?
