# Is `_SYSTEM/projects/engine/conversation/state.py` still needed?

*Generated: 2026-03-26 01:25 | Question 5 | 170s | Mode: default*

## Decisions

**Diff and read before any consolidation decision.** The engine copy of `conversation/state.py` is not a shim. It contains real logic: `_truncated_history()` with engine-specific config keys, `should_trigger_uncomfortable_idea()` with anti-slop quota behavior, and `build_agent_payload()` with discussion prompt phrasing. Delete-and-redirect without reading the library counterpart is unsafe.

**The single blocking read is `agentteam/conversation/state.py`.** Two questions must be answered from that file before any consolidation path is chosen:
1. Does it contain `should_trigger_uncomfortable_idea()` or equivalent anti-slop quota logic?
2. Does its `_truncated_history()` pull from the same config keys (`multi_history_truncation_threshold`, `multi_history_keep_first`, `multi_history_keep_last`) via the same `defaults()["conversation"]` call pattern?

**The config coupling is load-bearing.** The engine copy imports `from config_loader import defaults` — the engine's config loader, not the library's. Any consolidation path that redirects imports to the library copy must confirm that the library copy resolves config from a compatible source with identical key names. A mismatch produces silent truncation behavior drift. The Morning Brief acceptance criterion (writes, non-empty) does not catch this.

**The anti-slop behavior is user-facing.** `should_trigger_uncomfortable_idea()` reads `self.agent.anti_slop.uncomfortable_idea_quota` from `AgentConfig`, a library type. The trigger logic is in the engine file. If the library copy has no equivalent, redirecting imports to the library is a feature deletion with no observable failure signal. Sessions will complete normally; output will silently lose uncomfortable idea injection over time.

**"Thin subclass" is not an acceptable resolution path.** It is deferred architectural debt with inheritance coupling. It is explicitly rejected as a consolidation option.

**Decision tree, conditioned on the blocking read:**

- **Library copy has both behaviors, identical config keys** → redirect engine imports to library, delete engine copy, single commit.
- **Library copy has both behaviors, different config keys** → align config keys first (engine config YAML + library call site), confirm session runner resolves correctly, then redirect and delete.
- **Library copy is missing `should_trigger_uncomfortable_idea()`** → anti-slop logic must be migrated to the library before any deletion. Engine copy remains until migration is complete and confirmed.
- **Library copy has hardcoded truncation thresholds or no config pull** → engine copy is load-bearing on truncation behavior. Config-driven truncation must be promoted to the library before consolidation proceeds.
- **Drift with no clear ownership** → hard stop, human review before any action.

**Field-level identity is not semantic identity.** A field present in both files with the same name does not confirm equivalent behavior. Caller context and lifecycle position must be verified. Shared field names are not a consolidation signal.

**Acceptance criterion.** After any redirect or deletion: a completed `--no-session` run with no import errors, path resolution failures, or config key resolution failures clears the smoke test. If doubt remains — particularly around truncation behavior or anti-slop injection frequency — the Morning Brief acceptance criterion (full session, writes non-empty with characteristic idea diversity) applies.

**No changes are authorized until the blocking read is complete.** The consolidation path, commit scope, and sequencing are all downstream of what `agentteam/conversation/state.py` actually contains.
<!-- complete -->
