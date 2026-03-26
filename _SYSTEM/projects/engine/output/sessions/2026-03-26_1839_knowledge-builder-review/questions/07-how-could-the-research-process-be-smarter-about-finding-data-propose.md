### The Cognitive Architect (creativity engine designer)

The research process has a category error at its foundation. It treats mechanical data extraction as **information retrieval** when it's actually **hypothesis testing**.

Every UNKNOWN and INFERRED tag in the knowledge base is an implicit hypothesis: *"We believe this value is X, but haven't confirmed it."* Right now, those tags sit dormant until a human triggers a new research wave. That's backwards. The system should be continuously generating *testable claims* and routing them to the cheapest verification method available.

Here's the mechanism I'd build:

**The Claim Verification Stack** — ordered by cost, not quality:

1. **ROM + emulator memory watch** (cheapest, most precise): For any numeric claim — damage values, timing windows, spawn rates — a research agent with emulator access can set memory breakpoints and run controlled inputs. One hour of structured playtesting with memory watching produces more ROM_VERIFIED claims than a week of guide-reading.

2. **TAS/speedrun community mining** (underused goldmine): TAS authors are scientists. They've empirically isolated mechanics, frame-counted animations, and documented edge cases that no FAQ author noticed. Their knowledge lives in TASVideos encode notes, Discord pins, and submission text — structured but unmined.

3. **Disassembly-first for structural unknowns**: When a system's *existence* is uncertain (does this game have hidden stats?), disassembly gives you the answer before any playtesting begins.

The shift: research agents don't "go find data." They receive a prioritized queue of unverified claims, select the cheapest verification method, and return upgraded provenance tiers.

Everything else — guides, FAQs, wikis — becomes *seed data* that generates the hypothesis queue, not the final authority.

## Position Summary
I advocate reframing research as structured hypothesis-testing against a prioritized claim queue, with emulator memory-watching and TAS community archives as the primary precision sources. I reject guide-reading as a primary research method — it belongs at the bottom of the verification stack as hypothesis generator, not source of truth. The reason: LLM agents doing open-ended search optimize for coverage; agents executing specific testable claims against memory addresses optimize for precision, which is what behavioral assertion files actually require.

### The Flow Orchestrator (mechanical flow designer)

The Cognitive Architect's proposal is intellectually coherent but operationally unspecified at every decision point that matters.

**The queue has no defined producer.** "Receive a prioritized queue of unverified claims" — who builds it, when, and by what rule? The UNKNOWN/INFERRED tags already exist in the knowledge base. If the queue is just "scan for those tags and sort by... what?" — that's a script, not an architecture. Write the script. If it's something more complex, specify what.

**"Select the cheapest verification method" is a hand-wave.** The agent decides? By what logic? The verification stack ordering (emulator → TAS → disassembly) is a sensible heuristic, but "select cheapest" requires knowing: does an emulator setup exist? Is there a TAS for this game? Is the ROM disassembled? Those are preconditions, not givens. The agent needs a decision tree with explicit fallback paths, or this collapses into open-ended search with extra steps.

**TAS community mining is not a deterministic workflow.** "Discord pins and submission text" — how does an agent access Discord? Which servers? What's the failure mode when a server is private or archived? This belongs in a conventions document as a *source hint*, not as a pipeline stage.

The actual minimum improvement: add a `verification_method` field to UNKNOWN tags at write time, populated by the researcher who created the unknown. That researcher knows which verification approach applies. No new queue, no new routing layer.

## Position Summary
I advocate annotating UNKNOWN tags at creation time with a `verification_method` hint — the researcher who surfaces an unknown knows what would resolve it, and that knowledge should not be discarded. I reject the claim-queue-as-new-architecture proposal because it adds a production layer with undefined producers, undefined prioritization rules, and non-deterministic source access. The existing wave-gate pipeline is the right structure; it needs better field discipline, not a new orchestration tier.


<!-- complete -->
