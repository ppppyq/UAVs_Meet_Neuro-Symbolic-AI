# Foundations, books, and workshops

These resources are drawn from `data/foundational-resources.json`. They are auxiliary and are not counted as UAV paper records or core methods.

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
