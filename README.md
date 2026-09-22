# 🚁 UAVs Meet Neuro-Symbolic AI 🧠

Where learned aerial perception meets explicit, auditable reasoning for
trustworthy autonomy.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Website](https://img.shields.io/badge/Read-online_survey-236b71.svg)](https://ppppyq.github.io/UAVs_Meet_Neuro-Symbolic-AI/)
[![Status](https://img.shields.io/badge/Status-manuscript--in--preparation-orange.svg)](#-project-overview)
[![Data driven](https://img.shields.io/badge/Data-JSON--driven-green.svg)](data/papers.json)

> **Working title:** *UAVs Meet Neuro-Symbolic AI: Foundations, Taxonomy, and
> Perspectives for Trustworthy Aerial Autonomy*
>
> **Authors:** Yuqi Ping
>
> **Affiliation:** Harbin Institute of Technology, Shenzhen
>
> **Website:** [UAVs Meet Neuro-Symbolic AI](https://ppppyq.github.io/UAVs_Meet_Neuro-Symbolic-AI/)

---

[English](README.md) · [简体中文](README.zh-CN.md)

[Read the survey online](https://ppppyq.github.io/UAVs_Meet_Neuro-Symbolic-AI/) — explore the foundations and five research directions.

[Literature round log (2026-09-22, Chinese)](docs/literature-review.md) documents search scope, reading depth and evidence boundaries.

This survey follows the same six-part structure as the website: neuro-symbolic
AI foundations, followed by five research directions. The directions follow
`Proposed taxonomy v0.1`, a working proposal. Primary assignments are mutually
exclusive; secondary assignments are cross-references and do not inflate the
unique study count. See the [full paper index](docs/paper-index.md) for all records.

<!-- BEGIN GENERATED:README-NAV -->

## Contents

1. [Neuro-Symbolic AI Foundations](#foundations)
2. [Neuro-Symbolic Perception & World Modeling](#theme-perception_world_modeling)
3. [Neuro-Symbolic Reasoning & Mission Planning](#theme-reasoning_mission_planning)
4. [Neuro-Symbolic Navigation & Control](#theme-navigation_control)
5. [Neuro-Symbolic Safety & Verification](#theme-safety_verification)
6. [Neuro-Symbolic Collaboration & Interaction](#theme-collaboration_interaction)

<!-- END GENERATED:README-NAV -->

<a id="foundations"></a>

## 1. Neuro-Symbolic AI Foundations

<!-- BEGIN GENERATED:FOUNDATIONS -->

These resources provide background, book-length references, and community venues. They are auxiliary: they are not counted as UAV paper records or core methods.

### Literature synthesis · 2026-09-22

A bounded, source-checked literature round, not an exhaustive systematic review. Full-text, selected-passage and abstract-only evidence remain distinct; all records are awaiting human review.

This review treats a system as neuro-symbolic when a learned component is functionally coupled to an explicit representation with interpretable semantics: logical facts, executable programs, task automata or constraints. Three useful starting points are DeepProbLog's neural predicates and probabilistic inference, Logic Tensor Networks' differentiable logical grounding, and Scallop's relational programs with provenance-based reasoning.

[DeepProbLog: Neural Probabilistic Logic Programming](https://arxiv.org/abs/1805.10872) / [Logic Tensor Networks](https://openaccess.city.ac.uk/id/eprint/27580/) / [Scallop: A Language for Neurosymbolic Programming](https://pldi23.sigplan.org/details/pldi-2023-pldi/61/Scallop-A-Language-for-Neurosymbolic-Programming)

These mechanisms answer different questions. A query probability, a fuzzy truth degree and a temporal specification's satisfaction are not interchangeable measures of confidence or safety. A UAV pipeline must explain how perception becomes a symbol, what inference changes an action, and which assumptions make that inference meaningful. Merely using an LLM, graph or optimizer does not establish this connection.

[DeepProbLog: Neural Probabilistic Logic Programming](https://arxiv.org/abs/1805.10872) / [Logic Tensor Networks](https://openaccess.city.ac.uk/id/eprint/27580/) / [Scallop: A Language for Neurosymbolic Programming](https://pldi23.sigplan.org/details/pldi-2023-pldi/61/Scallop-A-Language-for-Neurosymbolic-Programming)

The present UAV sample mainly integrates pretrained neural modules with explicit reasoning at inference time. It does not establish a general advantage for end-to-end differentiable neuro-symbolic training. Foundational tools are therefore explanatory references, not extra UAV benchmark results; the selected introductory readings for LTN and Scallop are not marked as full-text reviews.

[NEUSIS: A Compositional Neuro-Symbolic Framework for Autonomous Perception, Reasoning, and Planning in Complex UAV Search Missions](https://arxiv.org/abs/2409.10196) / [Probabilistic Mission Design for Neuro-Symbolic Unmanned Aircraft Systems](https://arxiv.org/abs/2501.01439) / [Scallop: A Language for Neurosymbolic Programming](https://pldi23.sigplan.org/details/pldi-2023-pldi/61/Scallop-A-Language-for-Neurosymbolic-Programming)

**Open question:** How should perception calibration, logical semantics and runtime assumptions be exposed together so that a claimed guarantee can be audited?

### Foundational papers

| Resource | Contributors | Year | Venue / Publisher | Links |
|---|---|---|---|---|
| Neural-Symbolic Learning and Reasoning: A Survey and Interpretation | Authors: Tarek R. Besold, Artur d'Avila Garcez, Sebastian Bader, Howard Bowman, Pedro Domingos, Pascal Hitzler, Kai-Uwe Kuehnberger, Luis C. Lamb, Daniel Lowd, Priscila Machado Vieira Lima, Leo de Penning, Gadi Pinkas, Hoifung Poon, Gerson Zaverucha | 2017 | arXiv preprint | [arXiv](https://arxiv.org/abs/1711.03902) |
| Neurosymbolic Programming | Authors: Swarat Chaudhuri, Kevin Ellis, Oleksandr Polozov, Rishabh Singh, Armando Solar-Lezama, Yisong Yue | 2021 | Foundations and Trends in Programming Languages, 7(3), 158-243; Now Publishers | [DOI](https://doi.org/10.1561/2500000049) |
| Neuro-symbolic artificial intelligence: Current trends | Authors: Md Kamruzzaman Sarker, Lu Zhou, Aaron Eberhart, Pascal Hitzler | 2022 | AI Communications, 34(3), 197-209; SAGE Publications | [DOI](https://doi.org/10.3233/aic-210084) |
| Logic Tensor Networks | Authors: Samy Badreddine, Artur d'Avila Garcez, Luciano Serafini, Michael Spranger | 2022 | Artificial Intelligence 303, 103649; Elsevier | [DOI](https://doi.org/10.1016/j.artint.2021.103649) · [arXiv](https://arxiv.org/abs/2012.13635) |
| Scallop: A Language for Neurosymbolic Programming | Authors: Ziyang Li, Jiani Huang, Mayur Naik | 2023 | Proceedings of the ACM on Programming Languages 7 (PLDI), 1463–1487 | [DOI](https://doi.org/10.1145/3591280) · [arXiv](https://arxiv.org/abs/2304.04812) |

### Books and edited collections

| Resource | Contributors | Year | Venue / Publisher | Links |
|---|---|---|---|---|
| Neuro-Symbolic Artificial Intelligence: The State of the Art | Editors: Pascal Hitzler, Md Kamruzzaman Sarker | 2021 | Frontiers in Artificial Intelligence and Applications; IOS Press | [DOI](https://doi.org/10.3233/faia342) · ISBN 9781643682440, 9781643682457 |
| Compendium of Neurosymbolic Artificial Intelligence | Editors: Pascal Hitzler, Md Kamruzzaman Sarker, Aaron Eberhart | 2023 | Frontiers in Artificial Intelligence and Applications; IOS Press | [DOI](https://doi.org/10.3233/faia369) · ISBN 9781643684062, 9781643684079 |
| Handbook on Neurosymbolic AI and Knowledge Graphs | Editors: Pascal Hitzler, Abhilekha Dalal, Mohammad Saeid Mahdavinejad, Sanaz Saki Norouzi | 2025 | Frontiers in Artificial Intelligence and Applications; IOS Press | [DOI](https://doi.org/10.3233/faia400) · ISBN 9781643685786, 9781643685793 |
| Neurosymbolic AI: Foundations and Applications | Editors: Alvaro Velasquez, Shankar Sastry, Pradeep Ravikumar, Houbing Song, Sandeep Neema | 2026 | Wiley | [DOI](https://doi.org/10.1002/9781394302406) · ISBN 9781394302376, 9781394302406 |

### Workshops and community resources

| Resource | Contributors | Year | Venue / Publisher | Links |
|---|---|---|---|---|
| ICRA'25 Workshop on Foundation Models and Neuro-Symbolic AI for Robotics | Organizers: Chen Wang, Lu Gan, Yunzhu Li, Jiajun Wu, Ayoung Kim, Letizia Gionfrida, Luigi Palmieri, Alexander Gray | 2025 | ICRA 2025, Atlanta, GA, USA | [page](https://sairlab.org/icra25/) |

### Related surveys and screening context

These paper-database records have no primary research-direction assignment. They retain background and screening provenance, not included core UAV methods. They are counted separately from the auxiliary resources above.

| Paper | Role | Reading | Status | Links |
|---|---|---|---|---|
| [UAVs Meet LLMs: Overviews and Perspectives Toward Agentic Low-Altitude Mobility](https://arxiv.org/abs/2501.02341) | survey | abstract_reviewed | excluded | [paper](https://arxiv.org/abs/2501.02341) · [code](https://github.com/Hub-Tian/UAVs_Meet_LLMs) |
| [UAVs Meet Agentic AI: A Multidomain Survey of Autonomous Aerial Intelligence and Agentic UAVs](https://arxiv.org/abs/2506.08045) | survey | abstract_reviewed | excluded | [paper](https://arxiv.org/abs/2506.08045) · code: — / not verified |
| [Human-Inspired Neuro-Symbolic World Modeling and Logic Reasoning for Interpretable Safe UAV Landing Site Assessment](https://arxiv.org/abs/2510.22204) | method | abstract_reviewed | excluded | [paper](https://arxiv.org/abs/2510.22204) · code: — / not verified |
| [Neurosymbolic AI: The 3rd Wave](https://arxiv.org/abs/2012.05876) | position | abstract_reviewed | excluded | [paper](https://arxiv.org/abs/2012.05876) · code: — / not verified |
| [DeepProbLog: Neural Probabilistic Logic Programming](https://arxiv.org/abs/1805.10872) | method | abstract_reviewed | excluded | [paper](https://arxiv.org/abs/1805.10872) · [code](https://github.com/ML-KULeuven/deepproblog) |


<!-- END GENERATED:FOUNDATIONS -->

<!-- BEGIN GENERATED:RESEARCH-THEMES -->

<a id="theme-perception_world_modeling"></a>

## 2. Neuro-Symbolic Perception & World Modeling

Methods where neural perception grounds explicit symbols or maintains a probabilistic/semantic world model used by symbolic reasoning.

**Boundary:** Use when perception and world-state maintenance are functionally coupled to symbolic structure. Exclude standalone detectors or purely latent world models without explicit symbolic semantics.

**Subdirections:** Symbol grounding and scene graphs; Probabilistic and semantic world models; Multimodal perception for UAV search

### Literature synthesis · 2026-09-22

A bounded, source-checked literature round, not an exhaustive systematic review. Full-text, selected-passage and abstract-only evidence remain distinct; all records are awaiting human review.

The key interface is the conversion of uncertain visual observations into persistent entities, relations and world-state estimates that a planner can query. NEUSIS combines neural grounding with programmatic interfaces, a filtered world model and constraint-based search planning. Its symbolic layer therefore affects what is searched and how observations are reconciled, rather than serving only as a descriptive graph.

[NEUSIS: A Compositional Neuro-Symbolic Framework for Autonomous Perception, Reasoning, and Planning in Complex UAV Search Missions](https://arxiv.org/abs/2409.10196)

NEUSIS is evaluated in AirSim/HAMERITT simulation and starts with ground-truth occupancy and bird's-eye maps. Its reported search measure concerns correctly localized entities, not a flight-safety rate; false reports require separate scrutiny. SayPlan offers a transferable hierarchical scene-graph and plan-validation pattern, but its mobile-manipulation evidence is not UAV evidence and only selected method passages were inspected here.

[NEUSIS: A Compositional Neuro-Symbolic Framework for Autonomous Perception, Reasoning, and Planning in Complex UAV Search Missions](https://arxiv.org/abs/2409.10196) / [SayPlan: Grounding Large Language Models using 3D Scene Graphs for Scalable Robot Task Planning](https://proceedings.mlr.press/v229/rana23a.html)

Together these studies motivate a world model that records both semantic structure and the provenance and uncertainty of observations. Robustness to stale maps, uncertain pose and moving objects remains a deployment question, rather than a consequence of adding a scene graph.

[NEUSIS: A Compositional Neuro-Symbolic Framework for Autonomous Perception, Reasoning, and Planning in Complex UAV Search Missions](https://arxiv.org/abs/2409.10196) / [SayPlan: Grounding Large Language Models using 3D Scene Graphs for Scalable Robot Task Planning](https://proceedings.mlr.press/v229/rana23a.html)

**Open question:** Can a planner detect and repair an incorrect symbolic world state without relying on an accurate initial map?


### Reviewed core methods

| Paper | Neural–Symbolic Coupling | UAV Task | Evidence / Review | Publication | Links |
|---|---|---|---|---|---|
| [NEUSIS: A Compositional Neuro-Symbolic Framework for Autonomous Perception, Reasoning, and Planning in Complex UAV Search Missions](https://arxiv.org/abs/2409.10196) | GRiD neural perception produces noisy symbolic detections and attributes; the probabilistic world model reasons over and accumulates those symbols, then SNaC consumes the updated belief map for hierarchical planning. | search_and_exploration, navigation | fulltext_reviewed / simulation | preprint | [paper](https://arxiv.org/abs/2409.10196) · [code](https://github.com/ControlNet/NEUSIS) |


### Transferable robotics methods

| Paper | Neural–Symbolic Coupling | UAV Task | Evidence / Review | Publication | Links |
|---|---|---|---|---|---|
| [SayPlan: Grounding Large Language Models using 3D Scene Graphs for Scalable Robot Task Planning](https://proceedings.mlr.press/v229/rana23a.html) | Symbolic graph search restricts context; simulator feedback rejects infeasible actions and drives LLM replanning. | — | abstract_reviewed / none | Published (Conference on Robot Learning (CoRL), PMLR 229:23-72, 2023) | [paper](https://proceedings.mlr.press/v229/rana23a.html) · code: — / not verified |


### Cross-theme links

`p-2607.02277`, `p-2501.01439` appear in a different primary theme and are listed here for cross-reference only.

<a id="theme-reasoning_mission_planning"></a>

## 3. Neuro-Symbolic Reasoning & Mission Planning

Methods that combine explicit logic, constraints, probabilistic logic, or symbolic planning with learned components for mission-level reasoning and task sequencing.

**Boundary:** Use for explicit symbolic inference or mission/task planning. Exclude low-level trajectory optimization without a discrete symbolic model.

**Subdirections:** Logic and constraint reasoning; Task planning and goal management; Uncertainty-aware reasoning

### Literature synthesis · 2026-09-22

A bounded, source-checked literature round, not an exhaustive systematic review. Full-text, selected-passage and abstract-only evidence remain distinct; all records are awaiting human review.

Two routes emerge: probabilistic inference over mission rules, and translation of language into executable task specifications. ProMis combines uncertain geospatial relations and neural change-detection outputs in hybrid probabilistic logic programs, producing a probabilistic mission landscape. AutoTAMP instead translates instructions into signal temporal logic and iteratively checks and repairs task-and-motion plans.

[Probabilistic Mission Design for Neuro-Symbolic Unmanned Aircraft Systems](https://arxiv.org/abs/2501.01439) / [AutoTAMP: Autoregressive Task and Motion Planning with LLMs as Translators and Checkers](https://arxiv.org/abs/2306.06531)

ProMis provides offline map-based computational case studies, not a closed-loop flight demonstration. Pointwise rule satisfaction is neither a trajectory-wide collision probability nor legal authorization to fly. AutoTAMP's principal evaluation is in 2D domains; its supplemental 3D drone example omits the semantic-checking step, while physical demonstrations use ground robots. It remains a UAV candidate here despite full-text reading.

[Probabilistic Mission Design for Neuro-Symbolic Unmanned Aircraft Systems](https://arxiv.org/abs/2501.01439) / [AutoTAMP: Autoregressive Task and Motion Planning with LLMs as Translators and Checkers](https://arxiv.org/abs/2306.06531)

The synthesis is that a well-formed logical plan can still encode the wrong human intent or an outdated environment. Reviews should separate translation fidelity, logical feasibility, motion feasibility and execution outcome, and report the feedback connecting those stages.

[Probabilistic Mission Design for Neuro-Symbolic Unmanned Aircraft Systems](https://arxiv.org/abs/2501.01439) / [AutoTAMP: Autoregressive Task and Motion Planning with LLMs as Translators and Checkers](https://arxiv.org/abs/2306.06531)

**Open question:** How can semantic translation errors and changing mission rules be detected before a feasible but unintended plan is executed?


### Reviewed core methods

| Paper | Neural–Symbolic Coupling | UAV Task | Evidence / Review | Publication | Links |
|---|---|---|---|---|---|
| [Probabilistic Mission Design for Neuro-Symbolic Unmanned Aircraft Systems](https://arxiv.org/abs/2501.01439) | Neural probabilities become logic facts; inference produces a spatial field of modeled requirement satisfaction. | mission_planning | fulltext_reviewed / conceptual | Published (IEEE Transactions on Intelligent Transportation Systems 26(12), 22751-22760 (2025)) | [paper](https://arxiv.org/abs/2501.01439) · [code](https://github.com/HRI-EU/ProMis) |


### Candidate methods

| Paper | Neural–Symbolic Coupling | UAV Task | Evidence / Review | Publication | Links |
|---|---|---|---|---|---|
| [AutoTAMP: Autoregressive Task and Motion Planning with LLMs as Translators and Checkers](https://arxiv.org/abs/2306.06531) | Planner trajectories and syntax feedback guide repeated LLM translation; STL constrains joint task/motion synthesis. | mission_planning, navigation | fulltext_reviewed / simulation | Published (IEEE International Conference on Robotics and Automation (ICRA), 2024) | [paper](https://arxiv.org/abs/2306.06531) · code: — / not verified |


### Related architectures / perspectives

| Paper | Neural–Symbolic Coupling | UAV Task | Evidence / Review | Publication | Links |
|---|---|---|---|---|---|
| [Neuro-Symbolic Agentic AI for Networked Low-Altitude UAVs](https://arxiv.org/abs/2609.19961) | Neural grounding feeds an agentic symbolic planning and verification loop; execution/connectivity feedback updates task state and triggers sensing or replanning. | communication_and_networking, mission_planning | fulltext_reviewed / conceptual, simulation | preprint | [paper](https://arxiv.org/abs/2609.19961) · code: — / not verified |


### Cross-theme links

`p-2409.10196`, `p-2603.27583`, `p-2603.07824`, `p-2312.14950`, `p-2307.06135`, `p-simultech-2026-solver-selection` appear in a different primary theme and are listed here for cross-reference only.

<a id="theme-navigation_control"></a>

## 4. Neuro-Symbolic Navigation & Control

Methods that couple learned perception/language interfaces with symbolic specifications, constraints, planners, or control structures for motion-level UAV navigation.

**Boundary:** Use for motion-level navigation and control where symbolic structure shapes or guards learned behavior. Exclude pure end-to-end control without explicit semantics.

**Subdirections:** Natural-language to formal specification; Constraint-guided trajectory synthesis; Safe motion planning

### Literature synthesis · 2026-09-22

A bounded, source-checked literature round, not an exhaustive systematic review. Full-text, selected-passage and abstract-only evidence remain distinct; all records are awaiting human review.

Explicit specifications can connect learned behavior to continuous motion in different ways. Verified Compositions of Neural Network Controllers decomposes a co-safe LTL task into automaton transitions and uses reachable-set analysis to select admissible neural-controller compositions. LLM-STL Navigation translates language into STL constraints for trajectory optimization, with diagnosis and constrained repair when a request is infeasible.

[Verified Compositions of Neural Network Controllers for Temporal Logic Control Objectives](https://arxiv.org/abs/2209.06130) / [LLM-Enabled Low-Altitude UAV Natural Language Navigation via Signal Temporal Logic Specification Translation and Repair](https://arxiv.org/abs/2603.27583)

The controller-composition study uses numerical UAV dynamics and provides no real-flight evidence; its guarantee depends on the dynamics, initial-state set and sound reachable-set approximation. LLM-STL reports simulation and an outdoor DJI Matrice 300 RTK demonstration. Its formula exact-match accuracy measures translation, not flight safety, and the demonstration does not establish a broad operational success rate.

[Verified Compositions of Neural Network Controllers for Temporal Logic Control Objectives](https://arxiv.org/abs/2209.06130) / [LLM-Enabled Low-Altitude UAV Natural Language Navigation via Signal Temporal Logic Specification Translation and Repair](https://arxiv.org/abs/2603.27583)

These are complementary evidence patterns: formal reasoning under stated assumptions and physical demonstration under specific conditions. A useful comparison must include specification semantics, model mismatch, solver latency, fallback behavior and the scope of any relaxed constraint.

[Verified Compositions of Neural Network Controllers for Temporal Logic Control Objectives](https://arxiv.org/abs/2209.06130) / [LLM-Enabled Low-Altitude UAV Natural Language Navigation via Signal Temporal Logic Specification Translation and Repair](https://arxiv.org/abs/2603.27583)

**Open question:** Can specification satisfaction survive perception delay, dynamics mismatch and onboard compute limits without silently weakening safety constraints?


### Reviewed core methods

| Paper | Neural–Symbolic Coupling | UAV Task | Evidence / Review | Publication | Links |
|---|---|---|---|---|---|
| [LLM-Enabled Low-Altitude UAV Natural Language Navigation via Signal Temporal Logic Specification Translation and Repair](https://arxiv.org/abs/2603.27583) | The LLM proposes STL; solver conflicts guide temporal/predicate repair while the optimization layer chooses relaxation magnitudes. | navigation | fulltext_reviewed / simulation, real_flight | preprint | [paper](https://arxiv.org/abs/2603.27583) · code: — / not verified |
| [Verified Compositions of Neural Network Controllers for Temporal Logic Control Objectives](https://arxiv.org/abs/2209.06130) | Automaton search accepts neural-controller sequences only when their reachable sets satisfy each reach-avoid transition. | navigation | fulltext_reviewed / simulation | Published (2022 IEEE 61st Conference on Decision and Control, 4004-4009) | [paper](https://arxiv.org/abs/2209.06130) · code: — / not verified |


### Cross-theme links

`p-2409.10196`, `p-2306.06531`, `p-2409.10283` appear in a different primary theme and are listed here for cross-reference only.

<a id="theme-safety_verification"></a>

## 5. Neuro-Symbolic Safety & Verification

Methods focused on safety constraints, verification, monitoring, shielding, or assurance evidence tied to neural-symbolic integration.

**Boundary:** Use when assurance is explicitly coupled to learned components. Exclude standalone formal methods on fixed purely symbolic models.

**Subdirections:** Runtime monitoring and shielding; Landing and safety assessment; Formal verification of learned components

### Literature synthesis · 2026-09-22

A bounded, source-checked literature round, not an exhaustive systematic review. Full-text, selected-passage and abstract-only evidence remain distinct; all records are awaiting human review.

Safety evidence should identify the object being checked: an action precondition, a landing decision, a reachable state set or a temporal trajectory specification. Neural-controller composition and LLM-STL contribute cross-theme examples of reachability and specification constraints. Neither makes all upstream perception or language interpretation correct by construction.

[Verified Compositions of Neural Network Controllers for Temporal Logic Control Objectives](https://arxiv.org/abs/2209.06130) / [LLM-Enabled Low-Altitude UAV Natural Language Navigation via Signal Temporal Logic Specification Translation and Repair](https://arxiv.org/abs/2603.27583)

NeuroSymLand remains a reviewed candidate with unresolved publication-venue provenance; its symbolic landing-decision pipeline should not be promoted to a general closed-loop flight guarantee. ASMA is an adjacent published vision-language navigation method with adaptive CBF/MPC safety constraints. It remains abstract-reviewed: the semantic coupling and assumptions need a full-text audit, and CBF/MPC use alone does not satisfy this review's inclusion rule.

[NEUROSYMLAND: Neuro-Symbolic Landing-Site Assessment for Robust and Edge-Deployable UAV Autonomy](https://arxiv.org/abs/2607.02277) / [ASMA: An Adaptive Safety Margin Algorithm for Vision-Language Drone Navigation via Scene-Aware Control Barrier Functions](https://arxiv.org/abs/2409.10283)

The current sample does not support a ranking of these methods by a common safety score. A useful assurance account separates semantic correctness, conditional mathematical guarantees, runtime monitoring and measured violations, including failures outside the assumed environment.

[Verified Compositions of Neural Network Controllers for Temporal Logic Control Objectives](https://arxiv.org/abs/2209.06130) / [LLM-Enabled Low-Altitude UAV Natural Language Navigation via Signal Temporal Logic Specification Translation and Repair](https://arxiv.org/abs/2603.27583) / [NEUROSYMLAND: Neuro-Symbolic Landing-Site Assessment for Robust and Edge-Deployable UAV Autonomy](https://arxiv.org/abs/2607.02277)

**Open question:** Which failures remain outside each guarantee, and can the runtime detect those assumption violations early enough to trigger a safe fallback?


### Candidate methods

| Paper | Neural–Symbolic Coupling | UAV Task | Evidence / Review | Publication | Links |
|---|---|---|---|---|---|
| [NEUROSYMLAND: Neuro-Symbolic Landing-Site Assessment for Robust and Edge-Deployable UAV Autonomy](https://arxiv.org/abs/2607.02277) | Neural perception populates the PSSG; deterministic symbolic rules then evaluate candidate landing regions over that explicit representation. The runtime does not query the LLM; LLM-assisted authoring occurs offline before deployment. | landing | fulltext_reviewed / simulation, hardware_in_loop | conflict | [paper](https://arxiv.org/abs/2607.02277) · [code](https://github.com/Janus117/NeuroSymbolicLand) |
| [ASMA: An Adaptive Safety Margin Algorithm for Vision-Language Drone Navigation via Scene-Aware Control Barrier Functions](https://arxiv.org/abs/2409.10283) | Learned landmark navigation is constrained by a depth-based adaptive safety layer. | navigation | abstract_reviewed / simulation | Published (IEEE Robotics and Automation Letters 10(9), 9232–9239) | [paper](https://arxiv.org/abs/2409.10283) · code: — / not verified |


### Cross-theme links

`p-2609.19961`, `p-2603.27583`, `p-2501.01439`, `p-2209.06130` appear in a different primary theme and are listed here for cross-reference only.

<a id="theme-collaboration_interaction"></a>

## 6. Neuro-Symbolic Collaboration & Interaction

Methods where explicit symbolic structure supports human-UAV, multi-UAV, or networked collaboration and information exchange.

**Boundary:** Use when collaboration/interaction is central to the neuro-symbolic method, not merely a deployment label.

**Subdirections:** Human-UAV knowledge interaction; Multi-UAV coordination; Networked and edge-cloud autonomy

### Literature synthesis · 2026-09-22

A bounded, source-checked literature round, not an exhaustive systematic review. Full-text, selected-passage and abstract-only evidence remain distinct; all records are awaiting human review.

Human–UAV interaction and multi-UAV coordination require different evidence. TypeFly compiles language into MiniSpec programs with explicit skills, conditions, bounded loops and feedback-triggered replanning, evaluated on an indoor Tello. MINT maintains an explicit hypothesis tree and asks questions where alternative interpretations would change the flight path, using human answers to prune the task state.

[TypeFly: Flying Drones with Large Language Model](https://arxiv.org/abs/2312.14950) / [Reasoning Knowledge-Gap in Drone Planning via LLM-based Active Elicitation](https://arxiv.org/abs/2603.07824)

TypeFly's constrained program execution is not a collision-avoidance proof. MINT combines simulation with a small physical ambiguity-resolution study; reduced query count does not itself establish reduced human cognitive load, and truthful answers are assumed. Its publication is in the AAAI Spring Symposium Series, not the main AAAI conference.

[TypeFly: Flying Drones with Large Language Model](https://arxiv.org/abs/2312.14950) / [Reasoning Knowledge-Gap in Drone Planning via LLM-based Active Elicitation](https://arxiv.org/abs/2603.07824)

For team-level coordination, Learning-Guided Symbolic Solver Selection proposes a Double-DQN meta-controller selecting symbolic assignment solvers with feasibility filtering. Only the official abstract and publication metadata were checked because the full text required login. It is a candidate lead, not evidence for verified fleet-wide safety or real-flight scalability.

[Learning-Guided Symbolic Solver Selection for Dynamic Multi-UAV Missions in Simulation](https://www.insticc.org/node/TechnicalProgram/simultech/2026/presentationDetails/149518)

**Open question:** How should uncertainty, communication cost and disagreement be represented when moving from a single operator and UAV to multiple humans and aircraft?


### Reviewed core methods

| Paper | Neural–Symbolic Coupling | UAV Task | Evidence / Review | Publication | Links |
|---|---|---|---|---|---|
| [Reasoning Knowledge-Gap in Drone Planning via LLM-based Active Elicitation](https://arxiv.org/abs/2603.07824) | The VLM identifies semantic uncertainty; MINT represents it as a symbolic tree; the LLM chooses a binary query; the human answer prunes the tree and updates the semantic map and plan. | navigation, search_and_exploration | fulltext_reviewed / simulation, real_flight | Published (Proceedings of the AAAI Symposium Series 8(1), 127-131 (2026)) | [paper](https://arxiv.org/abs/2603.07824) · code: — / not verified |
| [TypeFly: Flying Drones with Large Language Model](https://arxiv.org/abs/2312.14950) | Neural outputs become executable programs; the interpreter invokes skills and requests replanning using updated observations. | navigation, search_and_exploration | fulltext_reviewed / real_flight | preprint | [paper](https://arxiv.org/abs/2312.14950) · code: — / not verified |


### Candidate methods

| Paper | Neural–Symbolic Coupling | UAV Task | Evidence / Review | Publication | Links |
|---|---|---|---|---|---|
| [Learning-Guided Symbolic Solver Selection for Dynamic Multi-UAV Missions in Simulation](https://www.insticc.org/node/TechnicalProgram/simultech/2026/presentationDetails/149518) | A learned meta-controller selects a solver; its candidate assignment is checked and evaluated in simulation. | multi_uav_coordination | abstract_reviewed / simulation | Published (SIMULTECH 2026, pp. 595–607) | [paper](https://www.insticc.org/node/TechnicalProgram/simultech/2026/presentationDetails/149518) · code: — / not verified |


### Cross-theme links

`p-2609.19961`, `p-2306.06531` appear in a different primary theme and are listed here for cross-reference only.

<!-- END GENERATED:RESEARCH-THEMES -->

---

## 🌐 Project overview

This repository is a living literature survey of **neuro-symbolic UAV autonomy**.
It is not a completed systematic
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

- Total records: 17
- Metadata verified: 16
- Metadata conflicts: 1
- Abstract-reviewed: 8
- Full-text reviewed: 9
- Candidate records: 6
- Direct UAV candidate methods: 4
- Core UAV methods (included, deduplicated, non-withdrawn): 6
- Unique seed studies (deduplicated, non-withdrawn): 16
- Withdrawn/version-linked records: 1
- Taxonomy migration pending: 1

<!-- END GENERATED:OVERVIEW -->

## 🗂 Research materials

| Path | Purpose |
|---|---|
| `data/papers.json` | Single source of truth for paper metadata, status, research content, and evidence. |
| `data/taxonomy.json` | Machine-readable proposed multi-axis taxonomy. |
| `data/search-log.json` | Searches and full-text resource accesses actually performed. |
| `docs/` | Scope, taxonomy, positioning, related work, roadmap, and generated coverage documents. |
| `notes/papers/` | Per-paper full-text reading notes. |
| `paper/` | LaTeX manuscript skeleton and generated `references.bib`. |

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
- [Foundations, books and workshops](docs/foundations.md)
- [Flat paper index](docs/paper-index.md)
- [Related-work comparison](docs/related-work-comparison.md)
- [Positioning and testable hypotheses](docs/positioning.md)
- [Roadmap](docs/roadmap.md)
- [Paper outline](docs/paper-outline.md)
- [LaTeX manuscript source](paper/main.tex)

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
