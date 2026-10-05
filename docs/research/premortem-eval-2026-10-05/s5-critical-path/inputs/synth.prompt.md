You are merging three independent pre-mortem reviews of the same plan into one report for the author.

Context packet (for checking claims): /tmp/claude-0/-home-user-AgentTeamDiscussions/becad465-8ac4-5b35-8ce1-917ff04320fe/scratchpad/premortem/s5-critical-path/packet.md
Review 1: /tmp/claude-0/-home-user-AgentTeamDiscussions/becad465-8ac4-5b35-8ce1-917ff04320fe/scratchpad/premortem/s5-critical-path/critic-1.md
Review 2: /tmp/claude-0/-home-user-AgentTeamDiscussions/becad465-8ac4-5b35-8ce1-917ff04320fe/scratchpad/premortem/s5-critical-path/critic-2.md
Review 3: /tmp/claude-0/-home-user-AgentTeamDiscussions/becad465-8ac4-5b35-8ce1-917ff04320fe/scratchpad/premortem/s5-critical-path/critic-3.md

Rules:
- You are a reporter, not a fourth reviewer: do not add findings of your own.
- Merge duplicates; rank by how many reviewers raised it and how costly the failure is.
- Drop findings that are generic or contradicted by the packet.
- Where reviewers disagree, keep both sides in one item.
- Do not name or describe the reviewers or say how many there were; write as a single report.

## Output format (exactly these three sections, at most 700 words in total)

## What breaks
Numbered, most important first. Each item: one bold sentence stating the failure, then 1-3 sentences on why,
citing the document or fact.

## Undecided
Bulleted decisions the plan needs but has not made.

## Questions for you
Bulleted questions only the author can answer, each one sentence.
