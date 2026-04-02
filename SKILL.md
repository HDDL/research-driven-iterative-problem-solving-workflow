---
name: arps
description: Use for open-ended non-physical problems that require human-like reasoning rather than straight execution. Clarify the real problem, model stakeholders and causes, generate options, compare trade-offs, choose a next action, and validate with both hard evidence and qualitative checks.
---

# ARPS: Adaptive Reasoning and Problem Solving

## Purpose

ARPS is a general problem-solving skill for non-physical problems where the right move is not obvious at the start.

It pushes you toward a human-like solving process:

1. inventory your available capabilities
2. restate the problem in plain language
3. separate facts, assumptions, interpretations, and preferences
4. identify stakeholders, incentives, time horizon, and reversibility
5. build a simple causal model of what is driving the situation
6. retrieve prior cases, analogies, and reusable patterns
7. generate multiple plausible options before committing
8. compare trade-offs instead of optimizing a fake single metric
9. choose one bounded next action
10. reflect on new evidence and update the model

## When to use this skill

Use ARPS when the task is complex, open ended, ambiguous, or multi-constraint, and the user needs reasoning rather than just execution.

Good fits:

- decision support under uncertainty
- research synthesis and problem framing
- planning and prioritization
- diagnosis of confusing failures or stalled progress
- proposal design and roadmap formation
- writing strategy, memo design, and communication planning
- process design, team alignment, and stakeholder coordination
- comparing options with incomplete evidence
- algorithm or system improvement with explicit metrics
- debugging and root-cause analysis

## When not to use this skill

Do not use ARPS when:

- the user only needs a one-shot rewrite, lookup, or direct answer
- the task is primarily physical-world execution
- the task requires certified professional judgment with high stakes and limited safeguards
- the task is purely aesthetic and no criteria can be made explicit at all
- the task depends on deception, manipulation, or hiding trade-offs from stakeholders

## Core philosophy

ARPS treats many hard problems as a mix of five things:

- truth: what is actually happening
- preference: what different people value
- coordination: how different actors can move together
- explanation: what story best accounts for the evidence
- sequencing: what should happen next and in what order

You MUST identify which of these dominates the problem before trying to solve it.

## Human-like operating principles

- Solve the user's underlying problem, not just the surface wording.
- Do not force numerical metrics onto questions that are mostly qualitative.
- Use numbers when they clarify reality, not when they create fake precision.
- Treat disagreement about goals as part of the problem.
- Prefer reversible probes before irreversible commitments.
- Keep at least two live options until one is clearly dominated.
- Distinguish confidence from certainty.
- Do not confuse a polished explanation with a validated one.

## Required outputs

For each invocation, you MUST produce the following structured artifacts.

### A. Problem framing

- task type
- problem restatement
- desired outcome
- decision owner
- stakeholders
- constraints
- known facts
- working assumptions
- unknowns
- success criteria
- dominant risks

### B. Situation model

- problem kind: truth, preference, coordination, explanation, sequencing
- causal hypotheses
- incentives and conflicts
- time horizon
- reversibility
- relevant prior cases or analogies

### C. Candidate options

Each option MUST include:

- option id
- option type
- goal
- why it might work
- expected upside
- expected downside
- scope
- success signal
- validation method
- guardrails
- iteration budget
- failure policy

### D. Validation plan

You MUST define one or more validation modes:

- executable or factual checks when available
- comparative analysis across options
- rubric-based quality review
- scenario walkthroughs
- stakeholder fit checks
- internal consistency checks

### E. Final synthesis

At the end, you MUST summarize:

- what the real problem became after reframing
- what options were considered
- what was recommended and why
- what evidence supports the recommendation
- what was rejected and why
- residual uncertainty
- next action

## Standard workflow

### Step 0: inventory capabilities

Before reasoning about the problem, inventory what you can actually do.

```yaml
capabilities:
  can_run_code: true/false
  can_search_web: true/false
  can_read_files: true/false
  can_write_files: true/false
  can_call_apis: true/false
  can_ask_human: true/false
  available_tools:
    - <tool 1>
    - <tool 2>
  hard_limits:
    - <limit 1>
```

This inventory constrains all downstream steps. Do NOT generate work items that require capabilities you do not have. If a critical capability is missing, note it as a blocker immediately rather than discovering it mid-execution.

### Step 1: orient

Classify the task as one of the following:

- research
- decision
- planning
- diagnosis
- communication
- hybrid

Also identify the dominant problem kind:

- truth
- preference
- coordination
- explanation
- sequencing

### Step 2: reframe the problem

Produce a compact structured framing:

```yaml
problem:
  type: decision
  restatement: <one-sentence restatement>
  desired_outcome: <what good looks like>
  decision_owner: <who decides>
  stakeholders:
    - <stakeholder 1>
  constraints:
    - <constraint 1>
  known_facts:
    - <fact 1>
  working_assumptions:
    - <assumption 1>
  unknowns:
    - <unknown 1>
  risks:
    - <risk 1>
```

The restatement MUST be narrower and more concrete than the original request.

### Step 3: map the situation

Before proposing a solution, separate:

- established facts
- working assumptions
- interpretations
- preferences

Then create a light causal model:

- what seems to drive the current outcome
- which constraints are real versus self-imposed
- which actors or incentives matter most
- what would most change the recommendation

### Step 4: review prior work and analogies

Before proposing changes, identify reusable ideas from:

- local files or project history
- previous attempts and lessons
- analogous cases from nearby domains
- external references if allowed

The purpose is not to write a long survey. The purpose is to avoid naive repetition, recover reusable patterns, and identify distinct strategy families.

### Step 5: generate candidate options

Generate 2 to 4 materially different options.

You MUST include:

- one least-effort option
- one safest reversible option
- one highest-upside option if justified

Do NOT collapse to a single option before comparing alternatives.

### Step 6: evaluate trade-offs

Compare options using the lenses most relevant to the task:

- expected value or likely benefit
- cost and complexity
- reversibility
- downside risk
- stakeholder fit
- time to feedback
- evidence strength
- clarity and communicability

If a real metric exists, use it.

If a real metric does not exist, use a rubric or scenario-based validation and explicitly mark it as qualitative or proxy-based.

### Step 7: choose a bounded next action

You MUST end with one concrete next action, not just abstract analysis.

That next action MUST specify:

- what to do now
- what evidence to collect
- what to preserve
- what would change the recommendation

### Step 8: run and reflect

When execution is possible:

1. establish the current state or baseline
2. make one bounded change
3. collect evidence
4. compare actual versus expected outcome
5. keep, revise, or discard
6. log the lesson

When execution is not possible:

1. run scenario tests
2. stress-test assumptions
3. produce a memo, plan, comparison, or communication artifact
4. state confidence and residual uncertainty explicitly

## Stage transition rules

You MUST follow these rules when moving between stages:

- orient → reframe: ALWAYS. Do not skip reframing.
- reframe → model: when the problem framing is stable. If reframing reveals a fundamentally different problem, re-orient first.
- model → review: when facts, assumptions, and causal hypotheses are separated. If you cannot separate them, stay in model.
- review → options: when you have identified at least one reusable pattern or confirmed that no relevant prior work exists.
- options → evaluate: when at least 2 materially different options exist. If you only have 1, stay in options.
- evaluate → act: when one option is clearly preferred OR when remaining options cannot be further separated without new evidence.
- act → reflect: after the bounded action is taken or a deliverable is produced.
- reflect → any earlier stage: based on failure diagnosis. See failure routing.

You MUST checkpoint before every stage transition.

Backward transitions are normal and expected. Do NOT treat returning to an earlier stage as failure — it means you learned something.

## Long-run autonomy contract

ARPS can guide long-running agents only if the runtime contract is explicit.

Every work item MUST define:

- stop conditions: when the work item is done
- pause conditions: when external input or a dependency is required
- handoff conditions: when to stop autonomous work and escalate to a human
- iteration budget: maximum number of attempts
- evidence budget: maximum new sources to consult
- checkpoint contents: what state to persist
- resume instructions: where to continue from after interruption

Checkpoint contents MUST include:

- active and pending work items
- completed work items
- rejected options with evidence-backed reasons
- last evaluated hypotheses and their current status
- evidence ids and provenance for anything used in the last decision
- full decision log and progress log snapshot
- current terminal condition
- a concrete `resume_pointer`, not just prose

At a minimum, you MUST checkpoint:

- before changing stages
- after completing a work item
- before any irreversible action
- when blocked on an external dependency
- when the current recommendation changes

You MUST terminate or pause in one of these terminal states:

- solved: the problem is answered or the deliverable is complete
- bounded_recommendation_ready: a defensible recommendation exists with explicit trade-offs
- blocked_waiting_for_external_input: cannot proceed without information or decision from a human
- budget_exhausted: iteration or evidence budget is spent
- unsafe_to_continue: further autonomous action carries unacceptable risk

If you cannot name your terminal condition, the task is probably still underspecified.

## Unattended control loop

For long-running autonomous runs, you MUST use the following control loop until a named terminal condition exists:

1. load the latest checkpoint
2. if a terminal condition is already named, stop immediately
3. if any hard budget is exhausted, set `terminal_condition = budget_exhausted`, checkpoint, and stop
4. rebuild the ready queue from pending work items whose pause and handoff conditions are not active
5. if `resume_pointer` exists, try that exact work item before selecting a new one
6. if no ready work item exists and `waiting_on` is external, set `terminal_condition = blocked_waiting_for_external_input`, checkpoint, and stop
7. select exactly one work item attempt using this priority order:
   - reduces the dominant uncertainty
   - has hard validation available
   - has the lowest blast radius
   - unblocks other work items
   - oldest pending item
8. execute one attempt only
9. decrement iteration budget for the attempted work item
10. decrement evidence budget only for truly new sources added to the evidence log
11. if a new external signal arrived, reset the external-signal budget
12. if an external signal is still required and none arrived, decrement the external-signal budget
13. if the external-signal budget reaches zero while an external dependency remains, set `terminal_condition = blocked_waiting_for_external_input`, checkpoint, and stop
14. evaluate material progress markers
15. update confidence, counters, and failure state
16. checkpoint state and evidence
17. route to the next stage or terminal condition

You MUST NOT invent alternate control semantics mid-run.

An external signal means new human input, an independent review, or new external evidence that was not produced by the current run.

Resume integrity is part of the contract:

- `resume_pointer.work_item_id` MUST refer to the active work item or one of the pending work items
- `resume_pointer.checkpoint_namespace` MUST match that work item's namespace exactly
- the saved resume target MUST NOT point at a completed or rejected item unless a new invalidation record explicitly reopens it

## Validation model

ARPS uses dual-track validation.

### Hard validation

Use when available:

- commands and tests
- factual verification
- source comparison
- numerical thresholds
- rule or policy checks

### Soft validation

Use when the problem is partly qualitative:

- rubric-based review
- stakeholder acceptance likelihood
- internal consistency
- scenario walkthroughs
- usefulness and clarity checks

NEVER present soft validation as certainty. Always state that it is qualitative evidence.

Soft validation alone MUST NOT authorize:

- irreversible actions
- high-blast-radius recommendations
- claims that a long-running loop is complete

Before taking such actions, require at least one of:

- external evidence from a new source
- an independent review pass
- an explicit human checkpoint

## Work item types

ARPS can compile work items of these kinds:

- sensemaking
- diagnosis
- research
- option_generation
- evaluation
- planning
- communication
- robustness
- execution

A minimal work item spec:

```yaml
id: O1
kind: evaluation
goal: compare limited beta versus full launch
scope:
  - launch_plan.md
reads:
  - state.current_recommendation
  - artifacts/launch_plan
writes:
  - checkpoints/O1/state.json
  - logs/O1.evidence_log.jsonl
checkpoint_namespace: O1
success_signal: recommendation remains preferred under downside scenario
validation:
  - run scenario review for trust, support load, and learning speed
guardrails:
  - do not assume enterprise readiness without evidence
progress_signals:
  - one option is rejected using new evidence
stop_conditions:
  - one option remains preferred across required scenarios
pause_conditions:
  - required stakeholder input is unavailable
handoff_conditions:
  - recommendation would change product launch timing materially
evidence_budget:
  max_new_sources: 3
checkpoint:
  write:
    - checkpoints/O1/state.json
    - logs/O1.evidence_log.jsonl
  include:
    - active_work_item
    - pending_work_items
    - completed_work_items
    - rejected_options
    - decision_log
    - progress_log
    - evidence_log
    - evidence_sources
    - last_evaluated_hypotheses
    - terminal_condition
    - resume_pointer
resume_instructions: continue from option comparison, not from reframing
iterations: 3
failure_policy: pivot
```

## Failure taxonomy

When repeated failure occurs, categorize using the following taxonomy:

- framing_failure: the problem statement is wrong or too vague
- evidence_failure: facts are missing or unreliable
- causal_failure: the situation model is wrong
- option_failure: all generated options are weak
- tradeoff_failure: cannot rank options because priorities conflict
- stakeholder_failure: key actors or incentives are missing from the model
- communication_failure: the artifact does not land with the audience
- constraint_failure: real limits make the current path infeasible
- execution_failure: the bounded action failed or produced unexpected results
- scope_failure: the problem is too big to solve as one unit

Failure routing:

- framing_failure → restate the problem and redefine success
- evidence_failure → gather better facts or design a better validation path
- causal_failure → revise the situation model
- option_failure → generate a new strategy family
- tradeoff_failure → make the conflict explicit and re-rank priorities
- stakeholder_failure → surface incentives, ownership, and adoption risks
- communication_failure → change the artifact, framing, or audience targeting
- constraint_failure → redesign within real limits
- execution_failure → shrink the step and make it reversible
- scope_failure → split the problem into smaller decisions

### Failure triggers

Repeated failure MUST NOT loop forever. These triggers are mandatory:

- **consecutive_discards >= 3**: if 3 bounded changes in a row are discarded, trigger failure diagnosis
- **no_progress_cycles >= 2**: if 2 full cycles produce no material progress, pause or hand off
- **same_failure_type >= 2**: if the same failure type appears twice in a row, leave the current stage and route per failure taxonomy
- **budget_exhausted**: if the iteration or evidence budget is spent, stop and report
- **soft_validation_only**: if only soft validation remains after all cycles, mark the result provisional until externally checked

### Material progress

Material progress is NOT a vibe. It means at least one of these happened in the current cycle:

- new independent evidence changed the status of a causal hypothesis
- a dominant uncertainty was reduced or resolved
- an option or work item was rejected with an evidence-backed reason
- a blocker was removed
- a hard check or guard newly passed
- the confidence ceiling increased because of new independent evidence

The following DO NOT count as progress:

- restating the same recommendation without new evidence
- rewording the same trade-off argument
- changing stages without adding information
- producing a more polished artifact that does not change decision quality

`progress_log` MUST record one entry per cycle. Use only this closed marker vocabulary:

- new_independent_evidence_changes_hypothesis_status
- new_external_signal_received
- dominant_uncertainty_reduced_or_resolved
- option_or_work_item_rejected_with_evidence_backed_reason
- blocker_removed
- hard_check_or_guard_newly_passes
- confidence_ceiling_increases_from_new_independent_evidence

If a cycle makes no material progress, record that cycle with `markers: []`.
`consecutive_no_progress` MUST equal the number of trailing `progress_log` entries whose markers are empty.

## Human escalation protocol

When you encounter a handoff condition or blocker, you MUST escalate to the human clearly.

### When to escalate

- the task requires domain-certified judgment you cannot provide
- a blocker persists after all escalation levels (reframe → gather evidence → new options → blocker)
- any action is irreversible and only supported by soft validation
- the user's intent is ambiguous and the ambiguity affects objective definition
- constraint violation would be irreversible
- two or more options remain tied and the tie-breaker is a value judgment

### How to escalate

Use this structure:

```
I am blocked on [specific thing].
Reason: [why I cannot resolve this autonomously].
What I need from you: [specific question or decision].
Options if relevant: [A vs B, with trade-offs].
What I will do after your input: [concrete next step].
```

NEVER escalate with vague requests like "what should I do next?" Always provide context, options, and a proposed path.

## Confidence tracking

Track confidence as a discrete level: very_low | low | medium | high | very_high.

### Update rules

Increase confidence when:
- a work item achieves local success
- a critical uncertainty is eliminated
- a guard or constraint check passes for 2+ consecutive iterations
- new confirming evidence arrives from an independent source

Decrease confidence when:
- a guard or constraint check fails
- a result is not reproducible
- evidence contradicts a working assumption
- the same failure type appears twice

Reset confidence to low when:
- the problem is reframed
- the dominant causal hypothesis changes
- the decision owner or primary constraint changes

### Confidence ceilings

NEVER report high or very_high confidence when:
- all validation is soft/qualitative only
- fewer than two independent evidence sources support the recommendation
- a critical unknown remains unresolved
- the problem was reframed in the current cycle

## Parallel execution

When multiple work items are independent (no shared state, no dependency), you MAY execute them in parallel.

Rules:
- you MUST verify independence before parallelizing using explicit `reads` and `writes` sets
- two work items are independent only if their `writes` sets are disjoint and neither item's `reads` set intersects the other's `writes`
- each parallel work item MUST have its own checkpoint
- checkpoint files MUST be namespaced per work item
- if one parallel work item fails, it MUST NOT block others unless a dependency exists
- merge results after all parallel items complete, before moving to the next stage
- maximum concurrent work items: 3 (to prevent context dilution)

## Automation rules

### Automatic by default

You MUST automatically:

- infer a first task type and dominant problem kind
- infer an initial problem framing from context
- separate facts from assumptions when they are mixed together
- inventory your available capabilities before planning actions
- propose candidate options
- propose a validation path
- select a bounded next action
- checkpoint the current state at meaningful transitions
- update lessons after each iteration
- track and update confidence after each work item

### Conservative by default

You MUST NOT:

- pretend that every problem has a clean single metric
- optimize a proxy without naming the proxy gap
- collapse to one option before comparing alternatives
- overfit to one stakeholder while hiding costs to others
- treat elegant prose as evidence
- make irreversible commitments without a strong reason
- continue a loop after no-progress and budget triggers have fired
- generate work items that require capabilities you do not have
- report high confidence on soft validation alone

## Success criteria

Success is hierarchical.

### Local success

A work item succeeds if:

- at least one material progress marker fires
- the chosen validation signals improve or become clearer
- the recommendation becomes more defensible
- the relevant guardrails remain satisfied

### Stage success

A stage succeeds if:

- at least one major uncertainty is reduced
- the next action becomes clearer
- a weak or dominated option is eliminated for a good reason

### Global success

The overall task succeeds if:

- the problem is better framed than when it started
- the final recommendation is supported by the best available evidence
- major constraints and stakeholder realities are acknowledged
- the next action is concrete and justified

## Long-run memory

You MUST persist lessons in reusable forms:

1. case-specific lessons
2. generalized strategy patterns
3. anti-patterns and invalid assumptions

Promote a lesson to a generalized pattern only after it survives across multiple cases.

For unattended runs, you MUST also persist:

- checkpoint state for resumption
- evidence log with timestamps
- evidence provenance for each source used
- blocker and dependency status
- why the current recommendation changed
- what exact step should happen after resume
- when the last external signal arrived
- which dependencies are external rather than internal
- source linkage from each evidence record to the evidence sources it depends on

## Suggested internal state schema

```yaml
state:
  run_id: arps-2026-03-29-001
  task_type: decision
  dominant_problem_kind: coordination
  current_stage: evaluate
  decision_owner: head_of_product
  active_work_item: O2
  current_recommendation: limited_beta
  confidence: medium
  confidence_ceiling: medium  # soft validation only
  dominant_uncertainty: trust_impact_under_real_customer_usage
  capabilities:
    can_run_code: false
    can_search_web: true
    can_read_files: true
    can_ask_human: true
  resume_pointer:
    work_item_id: O2
    attempt_id: A4
    stage: evaluate
    checkpoint_namespace: O2
    next_step: compare the latest stakeholder review against the saved beta guardrails
  pending_work_items:
    - O3
  completed_work_items:
    - O1
  rejected_options:
    - id: O4
      reason: rejected after new evidence showed trust downside exceeded benefit
      evidence_ids:
        - E2
  last_completed_action: compared beta versus broad launch on support risk
  last_checkpoint_at: 2026-03-29T21:00:00+08:00
  last_external_signal_at: 2026-03-29T20:45:00+08:00
  evidence_log:
    - id: E3
      kind: scenario
      summary: beta remains preferred in downside review
      effect_on_confidence: up
      source_ids:
        - SRC3
  evidence_sources:
    - id: SRC3
      kind: stakeholder_review
      provenance: support lead review on 2026-03-29
  last_evaluated_hypotheses:
    - id: H2
      status: active
      supported_by:
        - E3
  decision_log:
    - at: 2026-03-29T20:55:00+08:00
      decision: keep beta path as current recommendation
      because: trust downside remains lower than broad launch
      evidence_ids:
        - E3
  progress_log:
    - cycle: 4
      markers:
        - option_or_work_item_rejected_with_evidence_backed_reason
        - blocker_removed
      evidence_ids:
        - E3
  blockers:
    - waiting for support lead review
  waiting_on:
    - stakeholder_feedback
  waiting_on_external:
    - support_lead_review
  budgets:
    iterations_remaining: 2
    no_progress_cycles_remaining: 1
    external_signal_cycles_remaining: 1
  counters:
    consecutive_no_progress: 1
    consecutive_discards: 0
    repeated_failure_type_count: 0
  failure_mode: stakeholder_failure
  terminal_condition: blocked_waiting_for_external_input
  resume_instructions: request support lead input, then continue evaluation instead of regenerating options
```

## Output style

Prefer concise, structured outputs with explicit distinction between:

- established facts
- working assumptions
- active causal hypotheses
- option trade-offs
- evidence from validation
- recommended next action
- current confidence and confidence ceiling

## Minimal invocation template

When invoked, you MUST return the following sections:

1. Capability inventory
2. Problem framing
3. Situation model
4. Prior cases and reusable ideas
5. Candidate options
6. Recommended next action
7. Validation plan
8. Confidence level, confidence ceiling, and residual uncertainty

## Example invocation

User:

We need to decide whether to launch our AI meeting summary feature broadly this quarter, run a limited beta, or delay until accuracy improves.

Expected ARPS behavior:

- inventory available capabilities (can search web, can read files, cannot run the product code)
- classify as a decision and planning hybrid
- identify that the problem mixes coordination, preference, and sequencing
- surface trust, support burden, learning speed, and enterprise readiness as key trade-offs
- generate at least three launch options
- compare them using evidence strength, downside risk, reversibility, and stakeholder fit
- recommend one bounded next action instead of pretending the decision is already final
- report confidence as medium with a ceiling of medium (no hard validation available)
