

- DECIDED: No summarization scheme ships until empirical instrumentation confirms degradation is real and measurable
- DECIDED: Primary constraint is tokens, not turns — all limits sized in tokens; turn count is a proxy metric only
- DECIDED: Default behavior is hard token limit — pass full history up to a fixed ceiling, then hard-stop with no compression or summarization
- DECIDED: System prompt and agent role configuration are never truncated under any strategy
- DECIDED: Most recent 8 turns are always preserved verbatim; everything outside that window is dropped entirely
- DECIDED: Verbatim window size (8 turns) is configurable in config/defaults.yaml, not hardcoded
- DECIDED: Role-differentiated memory is an experiment mode, not infrastructure — not promoted to baseline until uniform-summary baseline is proven insufficient
- DECIDED: Truncation triggers on token count at context construction time, not on turn count
- DECIDED: A structured truncation event is logged: turn, tokens_before, tokens_after, turns_dropped
- DECIDED: Five metrics collected unconditionally per call: input_tokens_per_call, turn_number, truncation_fired, turns_dropped, session_total_cost
- DECIDED: Cost-per-session is a first-class metric; the token cost inflection point is the calibration target for limit sizing
- DECIDED: Degradation is defined by three observable output failures: contradiction of prior commitment, re-litigated closure, or missing constraint — not inferred from token counts alone
- DECIDED: Escalation path if degradation confirmed is: Step 1 uniform summary baseline, Step 2 role-differentiated summarization as experiment mode
- DECIDED: Summarization fallback fires to hard-limit behavior if summarization call times out or returns malformed output
- DECIDED: All tunable truncation values live in config/defaults.yaml with token_limit: 80000, verbatim_window_turns: 8, summarization_timeout: 30, log_token_usage: true
- OPEN: At what turn count do current discussions empirically hit the context ceiling?
- OPEN: What is the average token cost per agent turn across current experiment modes?
- OPEN: Does Morning Brief quality hold through 40-turn sessions under current unconstrained behavior?

<!-- complete -->
