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

- Total records: 7
- Metadata verified: 6
- Metadata conflicts: 1
- Abstract-reviewed: 5
- Full-text reviewed: 2
- Candidate records: 2
- Direct UAV candidate methods: 1
- Core UAV methods (included, deduplicated, non-withdrawn): 0
- Withdrawn/version-linked records: 1
- Taxonomy migration pending: 1

<!-- END GENERATED:OVERVIEW -->

## 📚 Paper list

Each row is generated from the same source of truth. Screening, metadata,
reading, and evidence status are shown separately.

<!-- BEGIN GENERATED:PAPER-TABLE -->

| ID | Title | Authors | Year | Type | Screening | Metadata | Reading | UAV evidence | Canonical URL |
|---|---|---|---|---|---|---|---|---|---|
| p-2501.02341 | UAVs Meet LLMs: Overviews and Perspectives Toward Agentic Low-Altitude Mobility | Yonglin Tian, Fei Lin, Yiduo Li, Tengchao Zhang, Qiyao Zhang, Xuan Fu, Jun Huang, Xingyuan Dai, Yutong Wang, Chunwei Tian, Bai Li, Yisheng Lv, Levente Kovács, Fei-Yue Wang | 2025 | survey | excluded | verified | abstract_reviewed | conceptual | [https://arxiv.org/abs/2501.02341](https://arxiv.org/abs/2501.02341) |
| p-2506.08045 | UAVs Meet Agentic AI: A Multidomain Survey of Autonomous Aerial Intelligence and Agentic UAVs | Ranjan Sapkota, Konstantinos I. Roumeliotis, Manoj Karkee | 2025 | survey | excluded | verified | abstract_reviewed | conceptual | [https://arxiv.org/abs/2506.08045](https://arxiv.org/abs/2506.08045) |
| p-2609.19961 | Neuro-Symbolic Agentic AI for Networked Low-Altitude UAVs | Yuqi Ping, Tianhao Liang, Nanchi Su, Guangyu Lei, Junwei Wu, Qinyu Zhang, Tingting Zhang | 2026 | position | candidate | verified | fulltext_reviewed | conceptual, simulation | [https://arxiv.org/abs/2609.19961](https://arxiv.org/abs/2609.19961) |
| p-2607.02277 | NEUROSYMLAND: Neuro-Symbolic Landing-Site Assessment for Robust and Edge-Deployable UAV Autonomy | Weixian Qian, Tianyi Yang, Sebastian Schroder, Yao Deng, Jiaohong Yao, Xiao Cheng, Richard Han, Xi Zheng | 2026 | method | candidate | conflict | fulltext_reviewed | simulation, hardware_in_loop | [https://arxiv.org/abs/2607.02277](https://arxiv.org/abs/2607.02277) |
| p-2510.22204 | Human-Inspired Neuro-Symbolic World Modeling and Logic Reasoning for Interpretable Safe UAV Landing Site Assessment | Weixian Qian, Tianyi Yang, Sebastian Schroder, Yao Deng, Jiaohong Yao, Xiao Cheng, Richard Han, Xi Zheng | 2025 | method | excluded | verified | abstract_reviewed | simulation, hardware_in_loop | [https://arxiv.org/abs/2510.22204](https://arxiv.org/abs/2510.22204) |
| p-2012.05876 | Neurosymbolic AI: The 3rd Wave | Artur d'Avila Garcez, Luis C. Lamb | 2020 | position | excluded | verified | abstract_reviewed | none | [https://arxiv.org/abs/2012.05876](https://arxiv.org/abs/2012.05876) |
| p-1805.10872 | DeepProbLog: Neural Probabilistic Logic Programming | Robin Manhaeve, Sebastijan Dumančić, Angelika Kimmig, Thomas Demeester, Luc De Raedt | 2018 | method | excluded | verified | abstract_reviewed | none | [https://arxiv.org/abs/1805.10872](https://arxiv.org/abs/1805.10872) |

<!-- END GENERATED:PAPER-TABLE -->

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
- [Related-work comparison](docs/related-work-comparison.md)
- [Positioning and testable hypotheses](docs/positioning.md)
- [Roadmap](docs/roadmap.md)
- [Paper outline](docs/paper-outline.md)
- [Iteration 02 report](docs/iteration-02-report.md)
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
