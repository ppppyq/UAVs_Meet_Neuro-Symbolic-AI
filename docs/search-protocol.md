# Search protocol

This document describes reusable discovery queries and search practice. It is a
planning document, not a claim that all these searches have already been
completed. Actual searches are logged in `data/search-log.json`.

## Candidate queries

### Direct neuro-symbolic UAV search

```text
("UAV" OR "drone" OR "quadrotor" OR "aerial robot")
AND
("neuro-symbolic" OR "neurosymbolic" OR "neural-symbolic")
```

### Symbolic structure + learning

```text
("UAV" OR "drone")
AND
("symbolic planning" OR "temporal logic" OR "knowledge graph")
AND
("learning" OR "neural" OR "language model")
```

### Runtime assurance + learned components

```text
("UAV" OR "drone")
AND
("runtime verification" OR "shielding" OR "formal verification")
AND
("neural" OR "reinforcement learning")
```

These queries are discovery aids only. A hit does not automatically satisfy the
inclusion criteria in `docs/scope.md`.

## Search practice

1. Keep a bounded seed-search pass for this initialization.
2. Prefer original arXiv pages, publisher pages, proceedings pages, and official
   author repositories for verification.
3. Log date, entry point, query, screening notes, and limitations.
4. Do not claim exhaustiveness from a small seed set.
5. If network access fails, record the limitation rather than pretending the
   search completed.
