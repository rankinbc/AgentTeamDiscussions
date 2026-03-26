### Q1: What does V1 session management actually do today?
- DECIDED: D1: Atomic writes for session.json (V1 blocker)
- DECIDED: D2: Quarantine suspicious ledger extractions with visible surfacing
- DECIDED: D3: Completion marker pattern is adequate for V1
- DECIDED: D4: Ledger-to-brief desync is a known gap, not a V1 blocker
- DECIDED: D5: Discussion coherence after crash recovery is a synthesis quality problem
- DECIDED: D6: Unbounded round queueing is operational, not architectural

### Q2: What is the current agent system capable of?
- DECIDED: D1: Speaking order rotation is a V1 fix
- DECIDED: D2: The six-layer agent model is an authoring model, not a runtime model
- DECIDED: D3: Context accumulation dominates agent identity by Round 2
- DECIDED: D4: Audit transcript content before redesigning agent layers
- DECIDED: D5: Add per-agent contribution visibility to session output
- DECIDED: D6: Defer personality-to-cognitive-strategy migration
- DECIDED: D7: Anti-slop layer has marginal effect and should not expand

### Q3: Which of the 39 proposed features are finishing V1 work vs b
- DECIDED: D1: Enumerate before classifying
- DECIDED: D2: Extract V1 features mechanically from the codebase
- DECIDED: D3: Measurement before mechanism remains the single ordering constraint
- DECIDED: D4: Score features by visible output improvement
- DECIDED: D5: Atomic writes for session.json is the single gating feature

### Q4: What are the load-bearing architectural constraints V2 must 
- DECIDED: D1: Measure the three mechanical constraints before designing V2 features
- DECIDED: D2: The Claude CLI subprocess boundary is the true flexibility ceiling
- DECIDED: D3: Code-seam rigidity is real but magnitude is unknown
- DECIDED: D4: Context homogenization is an unproven hypothesis, not a confirmed constraint
- DECIDED: D5: Synthesis quality is the user-facing constraint that binds all others
- DECIDED: D6: Round structure rigidity is a latency multiplier, not an architectural wall

### Q5: What should V2 absolutely NOT try to change about V1?
- DECIDED: D1: Freeze the Claude CLI subprocess boundary
- DECIDED: D2: Freeze the session output file structure
- DECIDED: D3: Freeze the context budget priority order until measured
- DECIDED: D4: Do not freeze round execution sequence
- DECIDED: D5: Do not freeze the manifest format or persistence mechanics with blanket protections
- DECIDED: D6: Do not freeze the prompt template structure
- DECIDED: D7: Measurement of context utilization is the first required measurement

<!-- complete -->
