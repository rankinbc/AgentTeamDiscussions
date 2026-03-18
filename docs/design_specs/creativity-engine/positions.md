# Positional Framing -- Agents Who ARE Stakeholders

**Status:** Draft - discovered during PRD creation
**Date:** 2026-03-17

---

## Concept

The biggest difference between "an LLM considering a stakeholder's perspective" and "an agent who IS that stakeholder" is **self-interest**. When an agent IS the target customer, they don't analyze the customer's needs abstractly -- they feel frustrated when the product doesn't solve THEIR problem. They argue from personal stakes, not intellectual exercise.

Position creates authentic motivation. Motivation creates real disagreement. Real disagreement creates better specs.

---

## Position vs Personality

**Personality** is HOW an agent thinks (assertive, creative, analytical).
**Position** is WHY an agent cares and WHAT they're optimizing for.

The same personality with different positions produces completely different outputs:
- An assertive analytical agent AS the customer: "This doesn't solve my actual problem. I don't care about your feature roadmap, I care about whether this works Tuesday morning."
- An assertive analytical agent AS the investor: "The TAM analysis doesn't hold up. Show me the unit economics or I'm out."

---

## Core Position Types

### The Customer (multiple variants)
The person who will USE this product. Has a real problem they need solved. Doesn't care about technical elegance, business model, or the team's vision -- cares about whether it WORKS for them.

**Variants:**
- **The Power User:** Wants depth, configurability, advanced features. "Give me the API, not the wizard."
- **The Casual User:** Wants simplicity. "I don't have time to learn this. Does it just work?"
- **The Frustrated Switcher:** Coming from a competitor product. Has specific complaints and expectations. "My current tool does X terribly. If yours does too, I'm gone."
- **The Reluctant Adopter:** Doesn't want a new tool. Needs to be convinced. "What I have works fine. Why should I change?"
- **The Budget Customer:** Price-sensitive. "I'll use the free tier forever unless you give me a reason to pay."

**What drives them:** Solving their problem. Period.
**What they push back on:** Features that don't serve them, complexity, price, anything that smells like "we built this for us, not for you."

### The Investor / Business Mind
Cares about market size, unit economics, competitive moat, and whether this is a business or a hobby.

**What drives them:** Return on investment, scalable growth, defensibility.
**What they push back on:** "Cool but niche" ideas, products without clear monetization, features that don't move business metrics, "build it and they will come" thinking.

### The Competitor
IS a competing product trying to beat this one. Thinks about what would make THEM lose, what gaps they see, what they'd copy immediately.

**What drives them:** Maintaining their market position. Finding the idea's weaknesses.
**What they push back on:** Nothing -- they actively try to find every vulnerability. "If I saw this launch, I'd immediately do X to counter it."

### The Regulator / Compliance
Cares about what could go wrong legally, ethically, or in terms of public trust. Not adversarial -- genuinely concerned about harm.

**What drives them:** Preventing harm, ensuring compliance, protecting vulnerable users.
**What they push back on:** Privacy shortcuts, accessibility gaps, Terms of Service assumptions, "we'll figure out compliance later."

### The Builder / Developer
The person who has to implement this. Cares about feasibility, maintainability, technical debt, and whether the specs are clear enough to actually build.

**What drives them:** Clean specs they can ship. Not getting stuck on ambiguous requirements.
**What they push back on:** Vague requirements, "it should be intuitive" without defining interactions, scope creep, technically impossible demands disguised as features.

### The Support / Operations
The person who has to keep this running and handle user complaints. Sees every edge case and failure mode.

**What drives them:** Reliability, debuggability, clear error states, documentation.
**What they push back on:** Features that will generate support tickets, unclear error handling, "happy path only" thinking, lack of admin tools.

### The Skeptic / Market Cynic
Has seen a thousand products like this fail. Not negative for the sake of it -- genuinely experienced with what doesn't work and why.

**What drives them:** Honesty about market reality. Preventing the team from building something nobody wants.
**What they push back on:** Assumptions about user behavior, "if we build it they will come," ignoring existing solutions, underestimating competition.

### The End User's Boss
The person who APPROVES the purchase but doesn't USE the product. Cares about team productivity, cost justification, reporting.

**What drives them:** ROI they can report to THEIR boss. Reduced risk.
**What they push back on:** Products that are great for individual users but can't justify their cost organizationally.

---

## Position Intensity

Not all positions are held with equal conviction. A **position intensity** (0.0 - 1.0) determines how strongly the agent filters everything through their stakeholder lens:

- **Low (0.1-0.3):** Considers the position but can step outside it. "As a customer I'd want X, but I can see why the business needs Y."
- **High (0.7-1.0):** Everything is through this lens. "I don't care about your business model. Does it solve my problem or not?" This creates authentic friction.

---

## Position + Personality Combinations

Some combinations are particularly valuable:

| Position | Personality Combo | Why It Works |
|---|---|---|
| Customer + high assertiveness + high stubbornness | Won't let the team forget who they're building for. Blocks feature creep that doesn't serve users. |
| Investor + analytical + skeptical | Keeps the business honest. Every claim needs evidence. |
| Competitor + high creativity temp + lateral thinking | Finds attack vectors nobody expected. "I'd copy your feature but do it with AI and undercut your price." |
| Builder + systematic + high attention span | Forces specs to be precise. "What happens when the user does X and then Y? You haven't defined that." |
| Skeptic + high stubbornness + narrative style | Tells the story of how this fails. Compelling enough to shift the group. |

---

## Positional Conflict Matrix

Certain positions naturally conflict. This is the engine of productive disagreement:

| Position A | Position B | Natural Tension |
|---|---|---|
| Customer | Investor | "Make it free" vs "Make it profitable" |
| Customer | Builder | "It should just work" vs "That's technically infeasible" |
| Investor | Builder | "Ship faster" vs "Ship correctly" |
| Visionary (from team) | Skeptic | "This will change everything" vs "No it won't" |
| Customer | Regulator | "I want full control of my data" vs "We need to retain it for compliance" |
| Power User | Casual User | "Give me more options" vs "This is already too complex" |

These conflicts don't need to be manufactured -- they emerge naturally from the positions. The key is casting agents with positions that will genuinely clash on the core decisions the discussion needs to make.

---

## Position Assignment Strategy

For a given AgentTeamDiscussion, the positions should be chosen based on what the idea needs stress-tested:

- **Consumer product idea:** Heavy customer variants (power user, casual, switcher), investor, competitor
- **Enterprise/B2B idea:** End user, end user's boss, builder, compliance, investor
- **Technical tool idea:** Builder (multiple variants), power user, support/ops, skeptic
- **Marketplace/platform idea:** Both sides of the market as customers, investor, regulator, competitor

The human user defines positions in the client team YAML. A BackgroundAgent (Director) can also suggest adding positions mid-discussion if gaps emerge.
