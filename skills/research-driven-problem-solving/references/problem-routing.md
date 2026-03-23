# Problem Routing Guide

Use this guide to decide how the same workflow should behave for different task types.

## Research

Use this route when the answer depends mainly on:

- prior work
- evidence quality
- citation strength
- claim boundaries

Default emphasis:

- find the strongest relevant sources, not the longest source list
- identify which claim actually matters for the decision
- describe the task characteristics that make this case different from prior work
- state what evidence would weaken the current conclusion

## Engineering

Use this route when the answer depends mainly on:

- code behavior
- system state
- reproducibility
- debugging or implementation choices

Default emphasis:

- reproduce before theorizing
- isolate the main blocker
- describe the failure shape and system conditions that define the problem
- prefer the smallest test or change that can generate signal

## Decision

Use this route when the answer depends mainly on:

- choosing among alternatives
- tradeoffs
- reversibility
- downside risk

Default emphasis:

- compare a small number of realistic options
- make criteria explicit before recommending
- describe the decision structure, including reversibility and downside asymmetry
- say what would change the recommendation later

## Shared rule

Regardless of route, always name:

- the problem type
- the critical uncertainty
- the result gap after each iteration
- the dominant cause of the current shortfall
- the stage to return to next
- the next justified action
- the validation gate for continuing
