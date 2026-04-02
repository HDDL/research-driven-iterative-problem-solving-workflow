# ARPS Skill Package

This package contains ARPS v0.7 — a general skill for non-physical problem solving designed to guide AI agents toward human-like reasoning.

## Design principles

- reframe the real problem before solving it
- inventory agent capabilities before planning actions
- separate facts, assumptions, and preferences
- model stakeholders, incentives, and causes
- generate multiple options before committing
- compare trade-offs with both hard and soft validation
- choose a bounded next action with explicit confidence
- track confidence with ceilings and update rules
- checkpoint at every meaningful transition for long-run autonomy
- escalate to humans with structured context, not vague requests
- terminate in a named state, never in an open loop

## Files

- `SKILL.md`: main skill definition and operating rules (imperative voice, agent-ready)
- `workflow.yaml`: machine-readable workflow, state, and routing contract
- `templates/task_spec.yaml`: generic template for new cases
- `examples/product_launch_decision_example.yaml`: decision and planning example
- `examples/cross_team_alignment_example.yaml`: coordination and communication example
- `examples/api_latency_diagnosis_example.yaml`: engineering diagnosis example
- `examples/runtime_samples/sample_state.json`: minimal valid runtime checkpoint sample
- `examples/runtime_samples/sample_evidence_log.jsonl`: matching evidence log sample
- `scripts/validate_runtime_state.py`: validates a `state.json` checkpoint and optional `evidence_log.jsonl`
- `scripts/check_runtime_samples.sh`: runs the validator against the bundled runtime samples
- `skills/research-driven-problem-solving/`: installable skill bundle mirroring the latest ARPS package

## v0.7 changes from v0.6

- tightened `checkpoint.include` so checkpoints preserve `evidence_log`, not just evidence ids
- added validator checks for closed-vocabulary material progress markers
- tied `consecutive_no_progress` to trailing empty `progress_log` cycles
- cross-validated `resume_pointer` against active/pending work items and checkpoint namespace
- strengthened evidence-trail expectations with provenance or source linkage on evidence records
- updated bundled examples and runtime samples to satisfy the stricter runtime contract

## v0.6 changes from v0.5

- converted all language to imperative voice (MUST/NEVER/WILL) for agent compliance
- added Step 0: capability inventory — agent enumerates what it can do before planning
- added explicit stage transition rules with conditions and fallbacks
- added confidence tracking with update rules and ceilings
- added failure trigger thresholds (consecutive discards, no-progress cycles, etc.)
- added parallel execution policy for independent work items
- added structured human escalation protocol with message template
- added engineering diagnosis example to cover technical problem types
- added `agent_capabilities` section to task spec template
- added `confidence_ceiling` to state schema and recommendation
- removed old ML-specific traffic example
- added an explicit unattended control loop for work-item selection, checkpointing, and stage advancement
- operationalized material progress with evidence-backed markers and non-examples
- expanded checkpoint and resume state with decision trace, rejected options, and evidence provenance
- fixed the diagnosis example so it ends in a named terminal state
- made external-signal budgets enforceable in the runtime loop
- added structured resume-pointer and checkpoint snapshot requirements to align state, template, and validator
- added machine-checkable `reads` / `writes` contracts and namespaced checkpoints for parallel work items
- aligned all examples with `agent_capabilities`, confidence fields, and the tightened runtime contract

## Recommended use

Use `SKILL.md` as the human-readable skill definition and `workflow.yaml` as the routing and state contract.

If you want to install this from the repository as a Codex-style skill, use `skills/research-driven-problem-solving/`.

The three examples cover decision-making, cross-team coordination, and engineering diagnosis — testing whether ARPS handles judgment, trade-offs, technical root-cause analysis, and coordination without collapsing into fake precision.

To validate a checkpoint snapshot, run:

`python scripts/validate_runtime_state.py state.json [evidence_log.jsonl]`

The script checks the required top-level state fields, nested checkpoint structures, resume-pointer integrity, closed-vocabulary progress markers, and JSONL evidence records when a log path is provided.

To smoke-test the bundled samples, run:

`bash scripts/check_runtime_samples.sh`

## Suggested acceptance test

A run should be considered successful only if:

1. the agent inventories its capabilities before generating work items
2. the reframed problem is sharper than the original request
3. at least two materially different options are considered
4. the final recommendation explains both evidence and trade-offs
5. residual uncertainty is named explicitly
6. confidence level and ceiling are reported with justification
7. the next action is concrete, bounded, and defensible
8. a checkpoint is written at each meaningful state transition
9. the run can resume from checkpoint without redoing a completed work item
10. no-progress detection halts, pauses, or hands off the run after the configured limit
11. the run ends in a named terminal state rather than an open-ended loop
12. qualitative-only conclusions remain marked provisional unless externally checked
13. human escalation uses the structured template, never vague requests
14. no work item requires a capability the agent does not have
15. checkpoint state includes decision trace, evidence provenance, and a concrete resume pointer
16. material progress is justified by at least one operational progress marker, not by restating the same recommendation
17. `progress_log` markers come only from the allowed vocabulary and trailing empty cycles match `consecutive_no_progress`
18. `resume_pointer` points to an active or pending work item and matches its checkpoint namespace
19. checkpoint snapshots preserve the full `evidence_log`, not only evidence identifiers
