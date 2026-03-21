---
name: research-driven-problem-solving
description: Structure open-ended research, engineering, and decision tasks into explicit problem framing, prior-work review, gap analysis, formalization, validation, and iteration. Use when a task is under-specified, high-uncertainty, high-stakes, or likely to require revision. Do not use for simple lookup, translation, formatting-only work, or routine mechanical execution.
---

# Research-Driven Problem Solving

Use this skill as a workflow controller for complex tasks.

This skill improves structure. It does not by itself prove literature claims, establish novelty, run experiments, or guarantee correctness. When source-dependent or empirical claims matter, gather direct evidence and cite it.

## Workflow

1. Select `lite` or `full` mode by reading `references/workflow.yaml`.
2. Produce explicit stage outputs. Separate verified facts from assumptions and proposals.
3. If the task depends on prior work, use concrete sources when available. If retrieval is unavailable, say so and keep those claims tentative.
4. If the task involves evaluation, specify metrics, baselines or comparators, and reproducibility notes before drawing conclusions.
5. Stop when success criteria are met or further iteration is not justified.

## Resource loading

- Read [references/workflow.yaml](references/workflow.yaml) for canonical stage definitions, transitions, and quality checks.
- Read [references/system-prompt.md](references/system-prompt.md) when you need a concise execution guide.
- Read [references/standard-output-template.md](references/standard-output-template.md) when the user wants a structured report.
- Read [references/example-research-design.md](references/example-research-design.md) only when a worked example would help choose the right level of detail.

## Output rules

- Always begin with a problem frame.
- Distinguish sourced claims, task-local evidence, assumptions, and recommendations.
- Prefer measurable objectives and validation criteria over purely qualitative claims.
- Do not claim novelty, state-of-the-art performance, or superiority without direct evidence.
- In lite mode, compress adjacent stages instead of skipping them silently.
