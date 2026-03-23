# Research-Driven Iterative Problem-Solving Workflow

An evidence-aware workflow and installable Codex skill for handling open-ended research, engineering, and decision problems.

## Why this exists

This project starts from a simple hypothesis:

many complex problems may share a higher-level problem-solving structure, even when their surface forms look very different.

That does not mean every problem can be solved with one universal method. It means many open-ended research, engineering, and decision tasks may still benefit from a common chain of work:

1. frame the problem
2. review prior work
3. characterize the problem
4. formalize the task
5. attempt a solution
6. evaluate the result
7. diagnose the gap and iterate

The question behind this repository is whether making that structure explicit as a workflow can help an agent perform more reliably on complex tasks, and move from "answering" toward actual problem solving.

This repository is an early iteration of that idea, not a fully validated or production-complete implementation. Feedback, criticism, and contributions are welcome.

## What this optimized variant changes

This version preserves the original seven-stage workflow, but makes it more effective at actually moving a problem forward:

- classify the task as `research`, `engineering`, or `decision`
- name the current critical uncertainty earlier
- require a next justified action before leaving each cycle
- define a validation gate before confidence increases
- treat long analysis as optional, not automatic

The goal is still structured reasoning, but with stronger pressure toward resolution rather than report-writing.

## What this repository provides

This repository publishes the method in two forms:

- a human-readable workflow specification for GitHub readers
- an installable Codex skill under `skills/research-driven-problem-solving/`

The core loop remains:

1. Frame the problem
2. Review prior work
3. Characterize the problem, then analyze the gap and constraints
4. Formalize the task
5. Attempt a solution
6. Validate with evidence
7. Diagnose the result, revise, and loop back as needed

What changes in this optimized version is how each stage behaves: every stage should help choose or refine the next action rather than only expand analysis. In particular, stage 3 now explicitly asks what kind of problem this is structurally, what task features matter, and which features make transfer from prior work fail, while stages 6 and 7 now form an explicit feedback loop: report results, analyze why they missed expectations, choose the dominant cause, and return to the right earlier stage for the next iteration.

## What it is good for

Use this workflow when the task is:

- open-ended rather than fully specified
- high-stakes or structurally complex
- uncertain in data, assumptions, or objectives
- likely to require revision instead of one-pass completion
- blocked by an unclear next step

Typical use cases:

- research planning
- thesis supervision
- engineering diagnosis
- method comparison
- technical proposal design
- policy or management analysis
- decision support under uncertainty

## What it does not replace

This repository improves structure, direction, and validation discipline. It does not replace:

- literature retrieval and citation checking
- experiment execution
- statistical testing
- reproducibility work
- domain expertise

If a task requires claims about prior work, novelty, empirical gains, or safety, those claims still need direct evidence.

## Repository layout

- [workflow.yaml](workflow.yaml)
  Machine-readable workflow specification
- [problem-routing.md](problem-routing.md)
  Heuristics for classifying tasks and choosing the right emphasis
- [system-prompt.md](system-prompt.md)
  Prompt-oriented execution guide
- [templates/standard-output-template.md](templates/standard-output-template.md)
  Structured report template
- [examples/example-research-design.md](examples/example-research-design.md)
  Minimal worked example
- [skills/research-driven-problem-solving/SKILL.md](skills/research-driven-problem-solving/SKILL.md)
  Installable Codex skill

## Install as a skill

If your agent supports local or GitHub-based skills, install the folder at:

```text
skills/research-driven-problem-solving
```

Minimal local install:

```bash
mkdir -p ~/.codex/skills
cp -R skills/research-driven-problem-solving ~/.codex/skills/
```

If your environment uses a different skills directory, copy the same folder there instead.

The installable bundle is self-contained. It includes:

- `SKILL.md`
- `agents/openai.yaml`
- `references/workflow.yaml`
- `references/problem-routing.md`
- `references/system-prompt.md`
- `references/standard-output-template.md`
- `references/example-research-design.md`

That means you can distribute the skill folder independently of the rest of the repository.

## Chinese summary

这个优化版保留了原来的七阶段结构，但加强了三件事：先判断任务类型，再尽早识别当前最关键的不确定性，并且在每一轮都明确下一步动作和验证门槛。这样它不只是把复杂问题讲清楚，也更强调把问题持续推进到可验证的结果。
我做这个项目的一个核心想法是：很多复杂问题虽然表面差异很大，但背后可能共享一种更高层的解决问题结构。如果能把这条结构化链条整理成 workflow，并用它去指导 Agent 工作，也许 Agent 在复杂任务上的表现会更稳定、更接近真正有效的问题求解，而不只是“回答得像”。这仍然只是一个很早期的版本，不是完全落地、已经验证充分的方案，更像一个可迭代的起点，也欢迎大家一起交流和完善。新的第 6、7 步还要求显式记录实验或实践结果、分析未达预期的原因，并决定回到第 2、3、4 或 5 步继续迭代。

## Boundary statement

Do not apply the full workflow blindly to every request.

If a task is simple, fully specified, low-stakes, and has little uncertainty, a direct response is usually better.

This project promotes structure where structure is needed, not complexity for its own sake.

## License

MIT
