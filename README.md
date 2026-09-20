# UAVs Meet Neuro-Symbolic AI

**Working title:** UAVs Meet Neuro-Symbolic AI: Foundations, Taxonomy, and
Perspectives for Trustworthy Aerial Autonomy

**Status:** manuscript in preparation. This repository is a lightweight
literature-review engineering workspace, not a completed systematic review and
not an experimental system.

Repository: <https://github.com/ppppyq/UAVs_Meet_Neuro-Symbolic-AI>

## Working research question

How can neural learning and explicit symbolic representations, reasoning, and
constraints be integrated to support trustworthy UAV autonomy?

## Research boundaries

The project is about neuro-symbolic UAV autonomy, not every UAV system that
uses AI. Using an LLM, agent, knowledge graph, MPC, CBF, or formal verifier is
not automatically neuro-symbolic AI. The exact inclusion and exclusion rules
are in [docs/scope.md](docs/scope.md).

Conceptual frameworks, simulation, hardware-in-the-loop, and real-flight
evidence are tracked separately. Author, affiliation, GitHub owner/repository,
target venue, and license are not yet provided and are intentionally left as
`null`/TODO.

## Proposed taxonomy

The taxonomy is `Proposed taxonomy v0.1`, not an established consensus. It uses
five independent label axes:

- functional position;
- integration direction;
- symbolic mechanism;
- UAV task;
- system and deployment form.

See [docs/taxonomy.md](docs/taxonomy.md) and
[data/taxonomy.json](data/taxonomy.json).

## Current evidence status

The seed set was inspected at metadata/abstract level. No paper has been
promoted to `included` after full-text review, so the current core UAV method
count is zero. Verified metadata and abstract-level candidates are shown
separately below.

<!-- BEGIN GENERATED:OVERVIEW -->

- Total records: 7
- Metadata verified: 6
- Metadata conflicts: 1
- Abstract-reviewed: 7
- Full-text reviewed: 0
- Candidate records: 2
- Direct UAV candidate methods: 2
- Core UAV methods (included, deduplicated, non-withdrawn): 0
- Withdrawn/version-linked records: 1

<!-- END GENERATED:OVERVIEW -->

## Paper list

<!-- BEGIN GENERATED:PAPER-TABLE -->

| ID | Title | Authors | Year | Type | Screening | Relevance | UAV evidence | Canonical URL |
|---|---|---|---|---|---|---|---|---|
| p-2501.02341 | UAVs Meet LLMs: Overviews and Perspectives Toward Agentic Low-Altitude Mobility | Yonglin Tian, Fei Lin, Yiduo Li, Tengchao Zhang, Qiyao Zhang, Xuan Fu, Jun Huang, Xingyuan Dai, Yutong Wang, Chunwei Tian, Bai Li, Yisheng Lv, Levente Kovács, Fei-Yue Wang | 2025 | survey | excluded | related_survey | conceptual | [https://arxiv.org/abs/2501.02341](https://arxiv.org/abs/2501.02341) |
| p-2506.08045 | UAVs Meet Agentic AI: A Multidomain Survey of Autonomous Aerial Intelligence and Agentic UAVs | Ranjan Sapkota, Konstantinos I. Roumeliotis, Manoj Karkee | 2025 | survey | excluded | related_survey | conceptual | [https://arxiv.org/abs/2506.08045](https://arxiv.org/abs/2506.08045) |
| p-2609.19961 | Neuro-Symbolic Agentic AI for Networked Low-Altitude UAVs | Yuqi Ping, Tianhao Liang, Nanchi Su, Guangyu Lei, Junwei Wu, Qinyu Zhang, Tingting Zhang | 2026 | method | candidate | direct_uav | conceptual, simulation | [https://arxiv.org/abs/2609.19961](https://arxiv.org/abs/2609.19961) |
| p-2607.02277 | NEUROSYMLAND: Neuro-Symbolic Landing-Site Assessment for Robust and Edge-Deployable UAV Autonomy | Weixian Qian, Tianyi Yang, Sebastian Schroder, Yao Deng, Jiaohong Yao, Xiao Cheng, Richard Han, Xi Zheng | 2026 | method | candidate | direct_uav | simulation, hardware_in_loop | [https://arxiv.org/abs/2607.02277](https://arxiv.org/abs/2607.02277) |
| p-2510.22204 | Human-Inspired Neuro-Symbolic World Modeling and Logic Reasoning for Interpretable Safe UAV Landing Site Assessment | Weixian Qian, Tianyi Yang, Sebastian Schroder, Yao Deng, Jiaohong Yao, Xiao Cheng, Richard Han, Xi Zheng | 2025 | method | excluded | direct_uav | simulation, hardware_in_loop | [https://arxiv.org/abs/2510.22204](https://arxiv.org/abs/2510.22204) |
| p-2012.05876 | Neurosymbolic AI: The 3rd Wave | Artur d'Avila Garcez, Luis C. Lamb | 2020 | position | excluded | background | none | [https://arxiv.org/abs/2012.05876](https://arxiv.org/abs/2012.05876) |
| p-1805.10872 | DeepProbLog: Neural Probabilistic Logic Programming | Robin Manhaeve, Sebastijan Dumančić, Angelika Kimmig, Thomas Demeester, Luc De Raedt | 2018 | method | excluded | background | none | [https://arxiv.org/abs/1805.10872](https://arxiv.org/abs/1805.10872) |

<!-- END GENERATED:PAPER-TABLE -->

## Local usage

Use Python 3.11 or newer.

```powershell
python scripts/manage.py validate
python -m unittest discover -s tests -v
python scripts/manage.py build
python scripts/manage.py check
python scripts/manage.py serve
```

The website is generated into `site/`. `serve` binds to `127.0.0.1:8000` by
default; stop it with `Ctrl+C`.

To add or update a paper, edit `data/papers.json`, update `taxonomy.json` if a
new tag is needed, then run the validation and build commands above. See
[data/README.md](data/README.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

## Reference sources and acknowledgements

The repository is informed by adjacent UAV survey/repository projects. They are
used as reference data for organization and boundary comparison, not copied as
original content:

- Hub-Tian/UAVs_Meet_LLMs
- Hub-Tian/UAVs_Meet_Embodied-Intelligence
- UAVs Meet Agentic AI survey
- Neuro-Symbolic Agentic AI for Networked Low-Altitude UAVs
- NEUROSYMLAND and its withdrawn predecessor
- Neurosymbolic AI: The 3rd Wave
- DeepProbLog

Detailed provenance is in `data/reference-sources.json` and
`data/papers.json`.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

This repository uses the MIT License. See [LICENSE](LICENSE) and
[LICENSE-NOTES.md](LICENSE-NOTES.md).
