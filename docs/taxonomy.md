# Proposed taxonomy v0.1

This taxonomy is a **working proposal**, not an established community consensus
and not a proven original contribution. It may be revised as evidence is read.

The taxonomy uses independent label axes rather than forcing all dimensions into
a single directory tree. A paper may carry multiple tags.

## Axes

### 1. Functional position

- `grounding`
- `representation`
- `reasoning`
- `planning`
- `execution`
- `assurance`

### 2. Integration direction

- `neural_to_symbolic`
- `symbolic_to_neural`
- `bidirectional`
- `other`
- `unknown`

### 3. Symbolic mechanism

- `logic_rules`
- `probabilistic_logic`
- `temporal_logic`
- `symbolic_planning`
- `knowledge_graph`
- `scene_graph`
- `program_representation`
- `constraint_reasoning`
- `other`
- `unknown`

### 4. UAV task

- `navigation`
- `mission_planning`
- `search_and_exploration`
- `landing`
- `inspection`
- `aerial_manipulation`
- `multi_uav_coordination`
- `communication_and_networking`
- `other`

### 5. System and deployment form

- `single_uav`
- `multi_uav`
- `human_uav`
- `edge_cloud`
- `heterogeneous_robots`

## Rules

- Tags support filtering and overview, not the core inclusion decision.
- A tag never replaces a written rationale explaining why a work is a
  neuro-symbolic method.
- Machine-readable definitions are in `data/taxonomy.json`.
