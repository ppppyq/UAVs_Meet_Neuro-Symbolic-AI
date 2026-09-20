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

## Display categories vs label axes

The five `display_categories` in `data/taxonomy.json` are reader-facing
research themes, not technical entities and not pipeline layers. They exist
for grouping and navigation. The `axes` remain the analytical label system
that describes a paper without forcing one dimension into a single directory
tree.

Display categories:

1. `perception_world_modeling`
2. `reasoning_mission_planning`
3. `navigation_control`
4. `safety_verification`
5. `collaboration_interaction`

Surveys, foundations, benchmark/dataset work, and general architecture
articles are auxiliary unless their central contribution fits a theme.

## Primary and secondary category rules

- `primary_category` is one display-category ID or `null`.
- `secondary_categories` is a deduplicated list of other display-category IDs.
- A primary category must not also appear in `secondary_categories`.
- Primary grouping is the only place a study is counted for unique coverage.
- Secondary assignments are cross-references and do not increase the unique
  study count.
- Null primary and `provisional` classification are allowed when evidence is
  insufficient; no keyword-based automatic assignment is permitted.

Example:

- `p-2409.10196` is primary `perception_world_modeling` because GRiD grounding
  and the probabilistic world model are the central coupling.
- Its SNaC planning appears in `reasoning_mission_planning` and
  `navigation_control` only as secondary cross-references.
