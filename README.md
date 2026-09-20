# 🚁 UAVs Meet Neuro-Symbolic AI 🧠

Where learned aerial perception meets explicit, auditable reasoning for
trustworthy autonomy.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](pyproject.toml)
[![Status](https://img.shields.io/badge/Status-manuscript--in--preparation-orange.svg)](#-project-overview)
[![Data driven](https://img.shields.io/badge/Data-JSON--driven-green.svg)](data/papers.json)

> **Working title:** *UAVs Meet Neuro-Symbolic AI: Foundations, Taxonomy, and
> Perspectives for Trustworthy Aerial Autonomy*
>
> **Authors:** Yuqi Ping
>
> **Affiliation:** Harbin Institute of Technology, Shenzhen
>
> **Repository:** [ppppyq/UAVs_Meet_Neuro-Symbolic-AI](https://github.com/ppppyq/UAVs_Meet_Neuro-Symbolic-AI)

---

## 🌐 Project overview

This repository is a lightweight, reproducible literature-review engineering
workspace for **neuro-symbolic UAV autonomy**. It is not a completed systematic
review and not an experimental system, and it does not claim novelty or
exhaustiveness.

The central idea is deliberately narrow:

> Using an LLM, agent, knowledge graph, controller, constraint function, or
> formal verifier does **not** automatically make a UAV system
> neuro-symbolic AI.

Instead, the project tracks whether a paper documents:

- a neural-learning component;
- an explicit symbolic representation, logic, program, or semantically
  meaningful constraint mechanism;
- a functional coupling between the two that affects learning or inference;
- a stated UAV problem and a described validation scope;
- separate evidence for conceptual, simulation, hardware-in-the-loop, and
  real-flight results.

## 🎯 Research question

> How can neural learning and explicit symbolic representations, reasoning, and
> constraints be integrated to support trustworthy UAV autonomy?

## 🧭 Scope and boundaries

The review focuses on **neuro-symbolic UAV autonomy**, not every UAV system
that uses AI. Inclusion and exclusion rules are documented in
[docs/scope.md](docs/scope.md).

Conceptual frameworks, simulation, hardware-in-the-loop, and real-flight
evidence are tracked separately. A failed network access is not proof that a
paper does not exist, and a small seed set is not an exhaustive search.

## 🧠 Proposed taxonomy

The taxonomy is `Proposed taxonomy v0.1`, not an established consensus and not
a proven original contribution. It uses five independent label axes:

| Axis | Purpose |
|---|---|
| ⚙️ Functional position | Where neural and symbolic components participate in the UAV autonomy stack. |
| 🔁 Integration direction | The dominant direction of information or influence between neural and symbolic components. |
| 🧩 Symbolic mechanism | The kind of explicit symbolic knowledge representation or inference mechanism. |
| 🛰️ UAV task | The aerial autonomy task or application domain. |
| 🧱 System and deployment | The system composition and deployment configuration. |

See [docs/taxonomy.md](docs/taxonomy.md) and
[data/taxonomy.json](data/taxonomy.json).

## 📊 Current evidence status

The numbers below are generated from [data/papers.json](data/papers.json).
They separate metadata verification, abstract review, full-text review,
version provenance, and candidate screening.

<!-- BEGIN GENERATED:OVERVIEW -->

- Total records: 10
- Metadata verified: 9
- Metadata conflicts: 1
- Abstract-reviewed: 6
- Full-text reviewed: 4
- Candidate records: 5
- Direct UAV candidate methods: 4
- Core UAV methods (included, deduplicated, non-withdrawn): 0
- Unique seed studies (deduplicated, non-withdrawn): 9
- Withdrawn/version-linked records: 1
- Taxonomy migration pending: 1

<!-- END GENERATED:OVERVIEW -->

## 📚 Neuro-symbolic UAV research themes

The five display themes below are generated from `data/taxonomy.json` and
`data/papers.json`. Primary assignments are mutually exclusive; secondary
categories are cross-references only and do not inflate the unique study count.
The full, flat paper list is in [docs/paper-index.md](docs/paper-index.md).

<!-- BEGIN GENERATED:RESEARCH-THEMES -->

### Surveys, Foundations & System Architectures

| Paper | Role | Reading | Status | Links |
|---|---|---|---|---|
| [UAVs Meet LLMs: Overviews and Perspectives Toward Agentic Low-Altitude Mobility](https://arxiv.org/abs/2501.02341) | survey | abstract_reviewed | excluded | [paper](https://arxiv.org/abs/2501.02341) · [code](https://github.com/Hub-Tian/UAVs_Meet_LLMs) |
| [UAVs Meet Agentic AI: A Multidomain Survey of Autonomous Aerial Intelligence and Agentic UAVs](https://arxiv.org/abs/2506.08045) | survey | abstract_reviewed | excluded | [paper](https://arxiv.org/abs/2506.08045) · code: — / not verified |
| [Human-Inspired Neuro-Symbolic World Modeling and Logic Reasoning for Interpretable Safe UAV Landing Site Assessment](https://arxiv.org/abs/2510.22204) | method | abstract_reviewed | excluded | [paper](https://arxiv.org/abs/2510.22204) · code: — / not verified |
| [Neurosymbolic AI: The 3rd Wave](https://arxiv.org/abs/2012.05876) | position | abstract_reviewed | excluded | [paper](https://arxiv.org/abs/2012.05876) · code: — / not verified |
| [DeepProbLog: Neural Probabilistic Logic Programming](https://arxiv.org/abs/1805.10872) | method | abstract_reviewed | excluded | [paper](https://arxiv.org/abs/1805.10872) · [code](https://github.com/ML-KULeuven/deepproblog) |


### Neuro-Symbolic Perception & World Modeling

Methods where neural perception grounds explicit symbols or maintains a probabilistic/semantic world model used by symbolic reasoning.

**Boundary:** Use when perception and world-state maintenance are functionally coupled to symbolic structure. Exclude standalone detectors or purely latent world models without explicit symbolic semantics.

**Subdirections:** Symbol grounding and scene graphs; Probabilistic and semantic world models; Multimodal perception for UAV search

#### Candidate methods

| Paper | Neural–Symbolic Coupling | UAV Task | Evidence / Review | Publication | Links |
|---|---|---|---|---|---|
| [NEUSIS: A Compositional Neuro-Symbolic Framework for Autonomous Perception, Reasoning, and Planning in Complex UAV Search Missions](https://arxiv.org/abs/2409.10196) | GRiD neural perception produces noisy symbolic detections and attributes; the probabilistic world model reasons over and accumulates those symbols, then SNaC consumes the updated belief map for hierarchical planning. | search_and_exploration, navigation | fulltext_reviewed / simulation | preprint | [paper](https://arxiv.org/abs/2409.10196) · [code](https://github.com/ControlNet/NEUSIS) |


#### Cross-theme links

`p-2607.02277` appear in a different primary theme and are listed here for cross-reference only.

### Neuro-Symbolic Reasoning & Mission Planning

Methods that combine explicit logic, constraints, probabilistic logic, or symbolic planning with learned components for mission-level reasoning and task sequencing.

**Boundary:** Use for explicit symbolic inference or mission/task planning. Exclude low-level trajectory optimization without a discrete symbolic model.

**Subdirections:** Logic and constraint reasoning; Task planning and goal management; Uncertainty-aware reasoning

#### Related architectures / perspectives

| Paper | Neural–Symbolic Coupling | UAV Task | Evidence / Review | Publication | Links |
|---|---|---|---|---|---|
| [Neuro-Symbolic Agentic AI for Networked Low-Altitude UAVs](https://arxiv.org/abs/2609.19961) | Neural grounding feeds an agentic symbolic planning and verification loop; execution/connectivity feedback updates task state and triggers sensing or replanning. | communication_and_networking, mission_planning | fulltext_reviewed / conceptual, simulation | preprint | [paper](https://arxiv.org/abs/2609.19961) · code: — / not verified |


#### Cross-theme links

`p-2409.10196`, `p-2603.27583`, `p-2603.07824` appear in a different primary theme and are listed here for cross-reference only.

### Neuro-Symbolic Navigation & Control

Methods that couple learned perception/language interfaces with symbolic specifications, constraints, planners, or control structures for motion-level UAV navigation.

**Boundary:** Use for motion-level navigation and control where symbolic structure shapes or guards learned behavior. Exclude pure end-to-end control without explicit semantics.

**Subdirections:** Natural-language to formal specification; Constraint-guided trajectory synthesis; Safe motion planning

#### Candidate methods

| Paper | Neural–Symbolic Coupling | UAV Task | Evidence / Review | Publication | Links |
|---|---|---|---|---|---|
| [LLM-Enabled Low-Altitude UAV Natural Language Navigation via Signal Temporal Logic Specification Translation and Repair](https://arxiv.org/abs/2603.27583) | The LLM translates natural language into STL; MILP synthesizes trajectories from those specifications, and infeasibility diagnosis feeds back into LLM-guided semantic repair. | navigation | abstract_reviewed / simulation, real_flight | preprint | [paper](https://arxiv.org/abs/2603.27583) · code: — / not verified |


#### Cross-theme links

`p-2409.10196` appear in a different primary theme and are listed here for cross-reference only.

### Neuro-Symbolic Safety & Verification

Methods focused on safety constraints, verification, monitoring, shielding, or assurance evidence tied to neural-symbolic integration.

**Boundary:** Use when assurance is explicitly coupled to learned components. Exclude standalone formal methods on fixed purely symbolic models.

**Subdirections:** Runtime monitoring and shielding; Landing and safety assessment; Formal verification of learned components

#### Candidate methods

| Paper | Neural–Symbolic Coupling | UAV Task | Evidence / Review | Publication | Links |
|---|---|---|---|---|---|
| [NEUROSYMLAND: Neuro-Symbolic Landing-Site Assessment for Robust and Edge-Deployable UAV Autonomy](https://arxiv.org/abs/2607.02277) | Neural perception populates the PSSG; deterministic symbolic rules then evaluate candidate landing regions over that explicit representation. The runtime does not query the LLM; LLM-assisted authoring occurs offline before deployment. | landing | fulltext_reviewed / simulation, hardware_in_loop | conflict | [paper](https://arxiv.org/abs/2607.02277) · [code](https://github.com/Janus117/NeuroSymbolicLand) |


#### Cross-theme links

`p-2609.19961`, `p-2603.27583` appear in a different primary theme and are listed here for cross-reference only.

### Neuro-Symbolic Collaboration & Interaction

Methods where explicit symbolic structure supports human-UAV, multi-UAV, or networked collaboration and information exchange.

**Boundary:** Use when collaboration/interaction is central to the neuro-symbolic method, not merely a deployment label.

**Subdirections:** Human-UAV knowledge interaction; Multi-UAV coordination; Networked and edge-cloud autonomy

#### Candidate methods

| Paper | Neural–Symbolic Coupling | UAV Task | Evidence / Review | Publication | Links |
|---|---|---|---|---|---|
| [Reasoning Knowledge-Gap in Drone Planning via LLM-based Active Elicitation](https://arxiv.org/abs/2603.07824) | The VLM identifies semantic uncertainty; MINT represents it as a symbolic tree; the LLM chooses a binary query; the human answer prunes the tree and updates the semantic map and plan. | navigation, search_and_exploration | fulltext_reviewed / simulation, real_flight | preprint | [paper](https://arxiv.org/abs/2603.07824) · code: — / not verified |


#### Cross-theme links

`p-2609.19961` appear in a different primary theme and are listed here for cross-reference only.

<!-- END GENERATED:RESEARCH-THEMES -->

## 🗂 Repository layout

| Path | Purpose |
|---|---|
| `data/papers.json` | Single source of truth for paper metadata, status, research content, and evidence. |
| `data/taxonomy.json` | Machine-readable proposed multi-axis taxonomy. |
| `data/search-log.json` | Searches and full-text resource accesses actually performed. |
| `docs/` | Scope, taxonomy, positioning, related work, roadmap, and iteration reports. |
| `notes/papers/` | Per-paper full-text reading notes. |
| `website/` and `site/` | Static project website source and generated output. |
| `paper/` | LaTeX manuscript skeleton and generated `references.bib`. |
| `scripts/manage.py` | Validation, migration, build, check, and local serve commands. |

## 🚀 Quick start

Use Python 3.11 or newer. In the current local environment, the default
`python` is Python 3.10, so Windows commands use `py -3.14`.

```powershell
py -3.14 scripts/manage.py validate
py -3.14 -m unittest discover -s tests -v
py -3.14 scripts/manage.py check --tracked-only
py -3.14 scripts/manage.py build
py -3.14 scripts/manage.py check
py -3.14 scripts/manage.py serve
```

`serve` binds to `127.0.0.1:8000` by default. Press `Ctrl+C` to stop.

## 🧾 How to contribute

Contributions should preserve evidence provenance and avoid fabricating
metadata. For a paper suggestion, open an issue using the provided template.
See [CONTRIBUTING.md](CONTRIBUTING.md) and
[data/README.md](data/README.md).

## 🔗 Useful documents

- [Scope and boundaries](docs/scope.md)
- [Search protocol](docs/search-protocol.md)
- [Proposed taxonomy](docs/taxonomy.md)
- [Display-category coverage](docs/category-coverage.md)
- [Flat paper index](docs/paper-index.md)
- [Related-work comparison](docs/related-work-comparison.md)
- [Positioning and testable hypotheses](docs/positioning.md)
- [Roadmap](docs/roadmap.md)
- [Paper outline](docs/paper-outline.md)
- [Iteration 02 report](docs/iteration-02-report.md)
- [Iteration 03 report](docs/iteration-03-report.md)
- [Compiled manuscript](paper/main.pdf)

## 🙏 Reference sources and acknowledgements

The repository is informed by adjacent UAV survey and repository projects.
They are used for organization and boundary comparison, not copied as original
content:

- Hub-Tian/UAVs_Meet_LLMs
- Hub-Tian/UAVs_Meet_Embodied-Intelligence
- UAVs Meet Agentic AI survey
- Neuro-Symbolic Agentic AI for Networked Low-Altitude UAVs
- NeuroSymLand / NEUROSYMLAND and its withdrawn predecessor
- Neurosymbolic AI: The 3rd Wave
- DeepProbLog

Detailed provenance is in [data/reference-sources.json](data/reference-sources.json)
and [data/papers.json](data/papers.json).

## 📜 License

This repository uses the MIT License. See [LICENSE](LICENSE) and
[LICENSE-NOTES.md](LICENSE-NOTES.md).

---

> Maintained as a reproducible literature-review workspace. If you use or
> extend it, please keep evidence provenance and do not promote a record to
> full-text-reviewed or included without actual evidence.
