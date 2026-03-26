### The Cognitive Architect (creativity engine designer)

# Context Window Allocation: The Inverted Pyramid

Most designs will front-load identity and starve substance. That's backwards. Here's why, and the budget that follows.

**The core insight from creativity research:** Cognitive diversity in groups comes from *what people are responding to*, not *who they believe they are*. Charlan Nemeth's dissent research shows that exposure to divergent positions — not personality traits — drives novel thinking. For LLMs this is even more true. A 500-token personality description produces less behavioral differentiation than 500 tokens of a rival agent's actual argument.

## The Budget (assuming ~180K usable tokens)

| Category | % | Hard Cap | Rationale |
|---|---|---|---|
| **Substrate** (question + decided facts + prior docs) | 35% | 63K | Non-negotiable. This is what they're reasoning *about*. |
| **Conversation history** (other agents' actual output) | 30% | 54K | The differentiation engine. Recency-weighted, not truncated. |
| **Agent identity** | 10% | 18K | Personality, position, technique, voice. Enough. Beyond this, diminishing returns are severe. |
| **Task framing** (round instructions, output format, anti-slop) | 10% | 18K | The behavioral guardrails. |
| **Private state** (inventory, takeaways, phase memory) | 10% | 18K | Accumulated reasoning. Compressed, not raw. |
| **Reserve** | 5% | 9K | Overflow buffer. Never allocated proactively. |

**The critical mechanism:** Conversation history uses *summarization tiers*. Current round = verbatim. Previous round = key claims + evidence. Earlier rounds = position tags only. This isn't lossy compression — it mirrors how real experts track a debate.

Identity stays lean because **the work differentiates agents, not the bio.**

## Position Summary
I advocate an inverted pyramid where substance and conversation history get 65% of the budget while identity gets only 10%, because LLM behavioral differentiation comes from what agents respond to, not self-description. I reject front-loading identity tokens or giving all categories equal weight. The research is clear: divergent stimuli drive creative output more than personality elaboration, and this applies doubly to LLMs where "identity" is just a prompt prefix competing against the actual reasoning substrate.

### The Flow Orchestrator (mechanical flow designer)

# The Architect's Budget Has No Decision Points

The inverted pyramid is directionally correct but treats allocation as static. It's not. Context needs shift *within a session* based on where you are in the flow.

**Round 1 (blind proposals):** Conversation history is zero. That 30% is wasted empty space. Agent identity and substrate should expand to fill it. This is the one moment identity *does* matter — it's the only differentiator when agents haven't seen each other's work yet.

**Round 2+ (critique/evaluate):** Identity compresses hard, conversation history expands. The Architect's tiered summarization is right here.

**Synthesis:** Prior docs and decided facts dominate. Agent identity drops to near-zero — the synthesizer doesn't need personality, it needs substance.

So the real design isn't a fixed budget. It's three profiles:

| Category | Blind | Reactive | Synthesis |
|---|---|---|---|
| Substrate | 40% | 30% | 45% |
| Conversation | 0% | 40% | 25% |
| Identity | 20% | 8% | 2% |
| Task framing | 15% | 7% | 18% |
| Private state | 15% | 10% | 5% |
| Reserve | 10% | 5% | 5% |

Three static profiles, selected by round type. No runtime calculation. PromptBuilder already knows what round it's building — this is a lookup table, not an algorithm.

The Architect's summarization tiers are the right mechanism for conversation history compression. I'd adopt that directly. But the fixed 30% allocation means Round 1 ships with 54K tokens of nothing, and synthesis gets starved of substrate to feed a personality nobody's reading.

**Implementation:** PromptBuilder gets a `GetBudget(RoundType)` method returning the profile. Three hardcoded dictionaries. Ship it in the same PR as blind proposals since Round 1 already needs the blind profile.

## Position Summary
I advocate phase-aware allocation with three static budget profiles (blind, reactive, synthesis) selected by round type, rather than a single fixed budget. I reject the Architect's flat 30% conversation history allocation because it wastes tokens in Round 1 and over-allocates identity in synthesis. The mechanism is a lookup table in PromptBuilder — no runtime complexity, just acknowledgment that different rounds have different needs.


<!-- complete -->
