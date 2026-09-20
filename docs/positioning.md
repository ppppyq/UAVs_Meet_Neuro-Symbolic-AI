# Positioning and testable hypotheses

This document records working contribution hypotheses. They are not findings
and not a claim of novelty. Each hypothesis must be tested against evidence in
`data/papers.json`, the reading notes, and the documented search protocol.

## Current working position

The project is a literature-review engineering artifact rather than a new
flight algorithm or a new neural-symbolic model. Its candidate value is in
making review claims reproducible: separating metadata verification, abstract
review, full-text review, version provenance, evidence location, and
multi-axis taxonomy.

## Hypothesis 1: Coupling evidence is a more stable inclusion boundary than "uses AI"

For direct UAV neuro-symbolic work, a record should be eligible only when it
documents a functional coupling between an explicit neural-learning component
and an explicit symbolic representation/reasoning component. The testable
claim is that tagging by taxonomy alone does not distinguish a real
neuro-symbolic method from an adjacent agentic, LLM, or rule-constrained UAV
system.

How to test:

- Compare inclusion decisions before and after applying the coupling rule.
- Check whether any record would be promoted on tags alone but excluded once
  neural/symbolic/coupling evidence is required.
- Record counterexamples in `data/papers.json` and `docs/scope.md`.

## Hypothesis 2: Evidence type changes the claim, not just the label

Simulation, hardware-in-the-loop, and real-flight evidence support different
conclusions. The testable claim is that a generated evidence matrix can
separate "successful simulated assessments" from "safe real-flight landing"
and prevent cross-level aggregation.

How to test:

- Keep the NeuroSymLand metric as "61 successful assessments out of 72
  simulated scenarios" and do not relabel it as real-flight safety.
- Generate `docs/evidence-matrix.md` and verify no row mixes `simulation`
  and `real_flight` without explicit separation.

## Hypothesis 3: Version and metadata conflicts must not inflate core-method counts

Withdrawn, superseded, or conflict-status versions of the same work should be
counted once and only after full-text review. The testable claim is that
`count_core_methods` remains zero until a record is promoted to `included`
with full-text evidence and no unresolved title/identity/fulltext conflict.

How to test:

- Run `python scripts/manage.py validate`.
- Run the generated `core_methods` statistic before and after adding a
  duplicated version.
- Ensure `p-2510.22204` and `p-2607.02277` are not counted as two methods.

## Current status

No hypothesis has been accepted as a finding. The project currently has no
`included` core UAV method because no candidate has yet passed the full
inclusion threshold without unresolved metadata conflict.
