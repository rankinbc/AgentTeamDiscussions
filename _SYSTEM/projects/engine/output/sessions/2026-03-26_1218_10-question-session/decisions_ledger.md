### Q1: What is the critical path for V2?
- DECIDED: Critical Path for V2
- DECIDED: 1. Blind Proposals Ship First
- DECIDED: 2. Manifest Versioning Is Mandatory Co-Delivery, Not a Blocker
- DECIDED: 3. Phase System Comes Second
- DECIDED: 4. Stale Detection Requires Phases
- DECIDED: 5. Anti-Sycophancy Is Validation, Not Architecture
- DECIDED: 6. BIT System Is Independent

### Q2: Should V2 be built as incremental upgrades to V1 or as a par
- DECIDED: DECIDED: Prompt Output Snapshots Are the Non-Negotiable First Deliverable
- DECIDED: DECIDED: PromptBuilder Is the Migration Entry Point, Not the Round Loop
- DECIDED: DECIDED: Blind Proposals Ship Through PromptBuilder Modification First
- DECIDED: DECIDED: The Migration Pattern Emerges From Feature Delivery, Not Upfront Design
- DECIDED: DECIDED: Every V2 Change Is Measured Against Output Quality
- DECIDED: DECIDED: BIT System and Key Takeaways Layer On Top Independently

### Q3: The context window is the hardest constraint. How should V2 
- DECIDED: DECIDED: Priority-Queue Eviction, Not Percentage Budgets
- DECIDED: DECIDED: Hardcoded Eviction Order (Last-Cut to First-Cut)
- DECIDED: DECIDED: Conversation History Uses Tiered Summarization
- DECIDED: DECIDED: Round Type Determines Available Budget, Not a Profile Lookup
- DECIDED: DECIDED: Agent Identity Hard-Capped at 800 Tokens Per Agent
- DECIDED: DECIDED: Instrument V1 Before Tuning V2

### Q4: What V2 features should be behind feature flags vs always-on
- DECIDED: DECIDED: Two Session-Level Feature Flags Only
- DECIDED: DECIDED: Feature Flags Live in session.json, Checked in PromptBuilder
- DECIDED: DECIDED: Ego Simulation and Graduated Resistance Intensity Are Team YAML Configuration, Not Session Flags
- DECIDED: DECIDED: Anti-Coordination Scoring Ships Always-On as Instrumentation
- DECIDED: DECIDED: Tiered Summarization Ships Always-On
- DECIDED: DECIDED: All Mechanical V2 Changes Ship Without Flags
- DECIDED: DECIDED: Flags Are Per-Session, Never Mid-Session
- DECIDED: DECIDED: Validate 800-Token Agent Cap Before Shipping

### Q5: How should we validate that V2 mechanisms actually work?
- DECIDED: DECIDED: Paired Human Comparison Is the Validation Framework
- DECIDED: DECIDED: Prompt Output Snapshots Are the Prerequisite
- DECIDED: DECIDED: The Evaluation Question Is "Did V2 Surface a Perspective V1 Missed?"
- DECIDED: DECIDED: Five Paired Runs Before Declaring Success or Failure
- DECIDED: DECIDED: No Automated Divergence Scoring in V2
- DECIDED: DECIDED: No Runtime Instrumentation for Validation
- DECIDED: DECIDED: Anti-Coordination Scoring (Already Decided Always-On) Provides the Only Automated Signal
- DECIDED: DECIDED: Contrarianism Detection Is a Human Judgment Call, Not an Automated Check
- DECIDED: DECIDED: No Formal Experimental Design at N < 20
- DECIDED: DECIDED: Measurement Infrastructure Is a Spreadsheet

### Q6: What is the right testing strategy for a system where correc
- DECIDED: DECIDED: Two-Layer Testing Strategy — Mechanical and Human, No Middle Layer
- DECIDED: DECIDED: Mechanical Tests Cover V2 Prompt Assembly, Not Prompt Effectiveness
- DECIDED: DECIDED: Specific Mechanical Test Targets for V2
- DECIDED: DECIDED: All Quality Validation Uses Paired Human Comparison
- DECIDED: DECIDED: No Temporal Regression Detection in V2
- DECIDED: DECIDED: No Structural Prompt Content Assertions Beyond Template Correctness
- DECIDED: DECIDED: No LLM-as-Judge, No Embedding Metrics, No Automated Quality Scoring

### Q7: The Claude CLI subprocess model vs SDK migration.
- DECIDED: DECIDED: SDK Migration Ships Last, After All V2 Prompt Features Are Validated
- DECIDED: DECIDED: Token Measurement Uses Character-Based Heuristics With Safety Margins, Not SDK Token Counting
- DECIDED: DECIDED: 800-Token Agent Identity Cap Is Validated Offline, Not At Runtime
- DECIDED: DECIDED: Tiered Summarization Triggers On Round Boundaries, Not Token Thresholds
- DECIDED: DECIDED: Context Eviction Uses Padded Character Estimates Until Data Says Otherwise
- DECIDED: DECIDED: Partial SDK Extraction Is Not a Valid Intermediate Step
- DECIDED: DECIDED: V1 Retry Mechanism Is Sufficient For V2 Validation

### Q8: How do we handle the personality system transition?
- DECIDED: DECIDED: Swap Test Is the Mandatory Gate Before Any Personality Transition Work
- DECIDED: DECIDED: The Detection Threshold Is Blind Identification
- DECIDED: DECIDED: If Personality Is Decorative, Write BITs Fresh Without Migration
- DECIDED: DECIDED: If Personality Is Load-Bearing, Use Sequential Single-Agent Compression
- DECIDED: DECIDED: V1 Agent YAML Files Are Preserved as Rollback, Not Deleted
- DECIDED: DECIDED: No A/B Testing of Personality Systems
- DECIDED: DECIDED: Personality Transition Does Not Block the Critical Path
- DECIDED: DECIDED: Round Structure and Positional Context Are Acknowledged as Potentially Dominant Factors

### Q9: Concurrency and scaling: what does reliable overnight operat
- DECIDED: DECIDED: Sequential Execution With Halt-on-Failure Is the Complete Overnight Model
- DECIDED: DECIDED: Retry With Exponential Backoff and Jitter, Capped at 120 Seconds
- DECIDED: DECIDED: No External Watchdog Process, No Heartbeat File
- DECIDED: DECIDED: Session Duration Cap in defaults.yaml
- DECIDED: DECIDED: Human-Readable Completion Report Is the Only New Artifact
- DECIDED: DECIDED: No Runtime Quality Validation
- DECIDED: DECIDED: No Skip-and-Advance Behavior
- DECIDED: DECIDED: No New Monitoring Infrastructure

### Q10: What is the minimum viable V2?
- DECIDED: DECIDED: Round-Type Prompt Differentiation Is the Highest-Priority V2 Change
- DECIDED: DECIDED: Blind Proposals Ship as a Real PromptBuilder Change, Not a Prompt-Instruction Test
- DECIDED: DECIDED: Overnight Completion Report Is the Third Minimum-Viable Change
- DECIDED: DECIDED: Tiered Summarization Is Not Minimum-Viable
- DECIDED: DECIDED: BIT System and Personality Transition Are Not in the Minimum-Viable Set
- DECIDED: DECIDED: Prompt Output Snapshots Remain the Prerequisite for All V2 Validation

<!-- complete -->
