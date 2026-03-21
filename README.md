# Research-Driven Iterative Problem-Solving Workflow

An evidence-aware workflow and installable Codex skill for handling open-ended research, engineering, and decision problems.

## What this repository provides

This repository publishes the same method in two forms:

- A human-readable workflow specification for GitHub readers
- An installable Codex skill under `skills/research-driven-problem-solving/`

The core idea is simple:

> Academic research is not the endpoint of training itself.
> It is a high-quality environment for developing transferable problem-solving capability.

Instead of jumping directly from a vague task to a method, the workflow enforces a loop:

1. Frame the problem
2. Review prior work
3. Analyze the gap and constraints
4. Formalize the task
5. Attempt a solution
6. Validate with evidence
7. Iterate or stop with justification

## What it is good for

Use this workflow when the task is:

- open-ended rather than fully specified
- high-stakes or structurally complex
- uncertain in data, assumptions, or objectives
- likely to require revision instead of one-pass completion

Typical use cases:

- research planning
- thesis supervision
- engineering diagnosis
- method comparison
- technical proposal design
- policy or management analysis
- decision support under uncertainty

## What it does not replace

This repository improves structure, not ground truth. It does not replace:

- literature retrieval and citation checking
- experiment execution
- statistical testing
- reproducibility work
- domain expertise

If a task requires claims about prior work, novelty, empirical gains, or safety, those claims still need direct evidence.

## Repository layout

- [workflow.yaml](workflow.yaml)
  Machine-readable workflow specification
- [system-prompt.md](system-prompt.md)
  Prompt-oriented execution guide
- [templates/standard-output-template.md](templates/standard-output-template.md)
  Structured report template
- [examples/example-research-design.md](examples/example-research-design.md)
  Minimal worked example
- [skills/research-driven-problem-solving/SKILL.md](skills/research-driven-problem-solving/SKILL.md)
  Installable Codex skill

## Install as a skill

If your environment supports GitHub-based skill installation, publish this repository and install the skill directory:

```text
https://github.com/<your-user>/<your-repo>/tree/main/skills/research-driven-problem-solving
```

The skill bundles the workflow spec, system prompt, template, and example inside its own `references/` folder so it can be distributed independently of the rest of the repository.

## Chinese summary

这个仓库提供了一套面向科研、工程分析与复杂决策任务的通用工作流，并同时打包成可安装的 Codex Skill。它的目标不是替代文献检索、实验执行或领域专家，而是把高不确定性任务组织成可检查、可验证、可迭代的过程：先界定问题，再回顾相关工作，分析差距与约束，完成形式化表达，提出可执行方案，基于证据做验证，并在需要时继续迭代。

## Boundary statement

Do not apply the full workflow blindly to every request.

If a task is simple, fully specified, low-stakes, and has little uncertainty, a direct response is usually better.

This project promotes structure where structure is needed, not complexity for its own sake.

## License

MIT
