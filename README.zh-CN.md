# 🚁 UAVs Meet Neuro-Symbolic AI 🧠

让无人机的学习式感知与显式、可审计的推理相遇，服务于可信自主性。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](pyproject.toml)
[![Status](https://img.shields.io/badge/Status-manuscript--in--preparation-orange.svg)](#-项目概览)
[![Data driven](https://img.shields.io/badge/Data-JSON--driven-green.svg)](data/papers.json)

> **暂定标题：** *UAVs Meet Neuro-Symbolic AI: Foundations, Taxonomy, and
> Perspectives for Trustworthy Aerial Autonomy*
>
> **作者：** Yuqi Ping
>
> **单位：** Harbin Institute of Technology, Shenzhen
>
> **仓库：** [ppppyq/UAVs_Meet_Neuro-Symbolic-AI](https://github.com/ppppyq/UAVs_Meet_Neuro-Symbolic-AI)

---

## 🌐 项目概览

这是一个轻量、可复现的文献综述工程工作区，主题是**神经符号 UAV 自主性**。它
不是已完成的系统综述，也不是实验系统，并且不声称首创或穷尽。

核心判断标准是有意收紧的：

> 使用 LLM、Agent、知识图谱、控制器、约束函数或形式化验证器，并不自动等同于
> 神经符号 AI。

项目实际追踪一篇论文是否记录：

- 神经学习组件；
- 显式符号表示、逻辑、程序或具有明确语义的约束机制；
- 神经与符号之间的功能耦合，且该耦合影响学习或推理；
- 明确的 UAV 问题与验证范围；
- 概念、仿真、硬件在环与真实飞行证据的分开记录。

## 🎯 工作性研究问题

> 神经学习与显式符号表示、推理和约束如何集成，以支持可信的 UAV 自主性？

## 🧭 研究边界

本项目关注“神经符号 UAV 自主性”，而不是所有“使用了 AI 的 UAV”。纳入与
排除规则见 [docs/scope.md](docs/scope.md)。网络访问失败不能证明论文不存在，
小型种子集也不等于穷尽检索。

## 🧠 暂定分类体系

分类体系为 `Proposed taxonomy v0.1`，不是学界共识，也不是已证明的原创贡献。
它采用五个相互独立的标签轴：

| 轴 | 作用 |
|---|---|
| ⚙️ 功能位置 | 神经与符号组件在 UAV 自主栈中的位置。 |
| 🔁 融合方向 | 神经与符号组件之间的主导信息或影响方向。 |
| 🧩 符号机制 | 显式符号知识表示或推理机制。 |
| 🛰️ UAV 任务 | 面向的空中自主任务或应用领域。 |
| 🧱 系统与部署 | 系统组成与部署形态。 |

详见 [docs/taxonomy.md](docs/taxonomy.md) 和
[data/taxonomy.json](data/taxonomy.json)。

## 📊 当前证据状态

以下数字由 [data/papers.json](data/papers.json) 生成，分离元数据核验、摘要阅读、
全文阅读、版本来源与候选筛选。

<!-- BEGIN GENERATED:OVERVIEW -->

- 文献记录总数：10
- 元数据已核验：9
- 元数据冲突：1
- 已做摘要阅读：6
- 已做全文阅读：4
- 候选条目：5
- 直接 UAV 候选方法：4
- 核心 UAV 方法（已纳入、去重、非撤回）：0
- 唯一种子研究（去重、非撤回）：9
- 撤回/版本关联条目：1
- 待复核分类迁移：1

<!-- END GENERATED:OVERVIEW -->

## 📚 神经符号 UAV 研究主题

以下五个展示主题由 `data/taxonomy.json` 与 `data/papers.json` 生成。主主题
互斥，次主题仅作交叉引用，不会增加唯一研究计数。平铺论文列表见
[docs/paper-index.md](docs/paper-index.md)。

<!-- BEGIN GENERATED:RESEARCH-THEMES -->

### Surveys, Foundations & System Architectures

| Paper | Role | Reading | Status | Links |
|---|---|---|---|---|
| [UAVs Meet LLMs: Overviews and Perspectives Toward Agentic Low-Altitude Mobility](https://arxiv.org/abs/2501.02341) | survey | abstract_reviewed | excluded | [paper](https://arxiv.org/abs/2501.02341) · [code](https://github.com/Hub-Tian/UAVs_Meet_LLMs) |
| [UAVs Meet Agentic AI: A Multidomain Survey of Autonomous Aerial Intelligence and Agentic UAVs](https://arxiv.org/abs/2506.08045) | survey | abstract_reviewed | excluded | [paper](https://arxiv.org/abs/2506.08045) · code: — / not verified |
| [Human-Inspired Neuro-Symbolic World Modeling and Logic Reasoning for Interpretable Safe UAV Landing Site Assessment](https://arxiv.org/abs/2510.22204) | method | abstract_reviewed | excluded | [paper](https://arxiv.org/abs/2510.22204) · code: — / not verified |
| [Neurosymbolic AI: The 3rd Wave](https://arxiv.org/abs/2012.05876) | position | abstract_reviewed | excluded | [paper](https://arxiv.org/abs/2012.05876) · code: — / not verified |
| [DeepProbLog: Neural Probabilistic Logic Programming](https://arxiv.org/abs/1805.10872) | method | abstract_reviewed | excluded | [paper](https://arxiv.org/abs/1805.10872) · [code](https://github.com/ML-KULeuven/deepproblog) |


### 神经符号感知与世界建模

Methods where neural perception grounds explicit symbols or maintains a probabilistic/semantic world model used by symbolic reasoning.

**Boundary:** Use when perception and world-state maintenance are functionally coupled to symbolic structure. Exclude standalone detectors or purely latent world models without explicit symbolic semantics.

**Subdirections:** Symbol grounding and scene graphs; Probabilistic and semantic world models; Multimodal perception for UAV search

#### Candidate methods

| Paper | Neural–Symbolic Coupling | UAV Task | Evidence / Review | Publication | Links |
|---|---|---|---|---|---|
| [NEUSIS: A Compositional Neuro-Symbolic Framework for Autonomous Perception, Reasoning, and Planning in Complex UAV Search Missions](https://arxiv.org/abs/2409.10196) | GRiD neural perception produces noisy symbolic detections and attributes; the probabilistic world model reasons over and accumulates those symbols, then SNaC consumes the updated belief map for hierarchical planning. | search_and_exploration, navigation | fulltext_reviewed / simulation | preprint | [paper](https://arxiv.org/abs/2409.10196) · [code](https://github.com/ControlNet/NEUSIS) |


#### Cross-theme links

`p-2607.02277` appear in a different primary theme and are listed here for cross-reference only.

### 神经符号推理与任务规划

Methods that combine explicit logic, constraints, probabilistic logic, or symbolic planning with learned components for mission-level reasoning and task sequencing.

**Boundary:** Use for explicit symbolic inference or mission/task planning. Exclude low-level trajectory optimization without a discrete symbolic model.

**Subdirections:** Logic and constraint reasoning; Task planning and goal management; Uncertainty-aware reasoning

#### Related architectures / perspectives

| Paper | Neural–Symbolic Coupling | UAV Task | Evidence / Review | Publication | Links |
|---|---|---|---|---|---|
| [Neuro-Symbolic Agentic AI for Networked Low-Altitude UAVs](https://arxiv.org/abs/2609.19961) | Neural grounding feeds an agentic symbolic planning and verification loop; execution/connectivity feedback updates task state and triggers sensing or replanning. | communication_and_networking, mission_planning | fulltext_reviewed / conceptual, simulation | preprint | [paper](https://arxiv.org/abs/2609.19961) · code: — / not verified |


#### Cross-theme links

`p-2409.10196`, `p-2603.27583`, `p-2603.07824` appear in a different primary theme and are listed here for cross-reference only.

### 神经符号导航与控制

Methods that couple learned perception/language interfaces with symbolic specifications, constraints, planners, or control structures for motion-level UAV navigation.

**Boundary:** Use for motion-level navigation and control where symbolic structure shapes or guards learned behavior. Exclude pure end-to-end control without explicit semantics.

**Subdirections:** Natural-language to formal specification; Constraint-guided trajectory synthesis; Safe motion planning

#### Candidate methods

| Paper | Neural–Symbolic Coupling | UAV Task | Evidence / Review | Publication | Links |
|---|---|---|---|---|---|
| [LLM-Enabled Low-Altitude UAV Natural Language Navigation via Signal Temporal Logic Specification Translation and Repair](https://arxiv.org/abs/2603.27583) | The LLM translates natural language into STL; MILP synthesizes trajectories from those specifications, and infeasibility diagnosis feeds back into LLM-guided semantic repair. | navigation | abstract_reviewed / simulation, real_flight | preprint | [paper](https://arxiv.org/abs/2603.27583) · code: — / not verified |


#### Cross-theme links

`p-2409.10196` appear in a different primary theme and are listed here for cross-reference only.

### 神经符号安全与验证

Methods focused on safety constraints, verification, monitoring, shielding, or assurance evidence tied to neural-symbolic integration.

**Boundary:** Use when assurance is explicitly coupled to learned components. Exclude standalone formal methods on fixed purely symbolic models.

**Subdirections:** Runtime monitoring and shielding; Landing and safety assessment; Formal verification of learned components

#### Candidate methods

| Paper | Neural–Symbolic Coupling | UAV Task | Evidence / Review | Publication | Links |
|---|---|---|---|---|---|
| [NEUROSYMLAND: Neuro-Symbolic Landing-Site Assessment for Robust and Edge-Deployable UAV Autonomy](https://arxiv.org/abs/2607.02277) | Neural perception populates the PSSG; deterministic symbolic rules then evaluate candidate landing regions over that explicit representation. The runtime does not query the LLM; LLM-assisted authoring occurs offline before deployment. | landing | fulltext_reviewed / simulation, hardware_in_loop | conflict | [paper](https://arxiv.org/abs/2607.02277) · [code](https://github.com/Janus117/NeuroSymbolicLand) |


#### Cross-theme links

`p-2609.19961`, `p-2603.27583` appear in a different primary theme and are listed here for cross-reference only.

### 神经符号协同与交互

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

## 🧭 基础论文、书籍与 workshop

这里列出神经符号 AI 的基础论文、书籍和社区资源。它们属于辅助材料，不计入
UAV 文献记录或核心方法统计。详见 [docs/foundations.md](docs/foundations.md)。

<!-- BEGIN GENERATED:FOUNDATIONS -->

以下资源用于提供理论基础、书籍参考和社区信息。它们是辅助性资源，不计入 UAV 文献记录或核心方法统计。

### 基础论文

| Resource | Contributors | Year | Venue / Publisher | Links |
|---|---|---|---|---|
| Neural-Symbolic Learning and Reasoning: A Survey and Interpretation | Authors: Tarek R. Besold, Artur d'Avila Garcez, Sebastian Bader, Howard Bowman, Pedro Domingos, Pascal Hitzler, Kai-Uwe Kuehnberger, Luis C. Lamb, Daniel Lowd, Priscila Machado Vieira Lima, Leo de Penning, Gadi Pinkas, Hoifung Poon, Gerson Zaverucha | 2017 | arXiv preprint | [arXiv](https://arxiv.org/abs/1711.03902) |
| Neurosymbolic Programming | Authors: Swarat Chaudhuri, Kevin Ellis, Oleksandr Polozov, Rishabh Singh, Armando Solar-Lezama, Yisong Yue | 2021 | Foundations and Trends in Programming Languages, 7(3), 158-243; Now Publishers | [DOI](https://doi.org/10.1561/2500000049) |
| Neuro-symbolic artificial intelligence: Current trends | Authors: Md Kamruzzaman Sarker, Lu Zhou, Aaron Eberhart, Pascal Hitzler | 2022 | AI Communications, 34(3), 197-209; SAGE Publications | [DOI](https://doi.org/10.3233/aic-210084) |

### 书籍与编著

| Resource | Contributors | Year | Venue / Publisher | Links |
|---|---|---|---|---|
| Neuro-Symbolic Artificial Intelligence: The State of the Art | Editors: Pascal Hitzler, Md Kamruzzaman Sarker | 2021 | Frontiers in Artificial Intelligence and Applications; IOS Press | [DOI](https://doi.org/10.3233/faia342) · ISBN 9781643682440, 9781643682457 |
| Compendium of Neurosymbolic Artificial Intelligence | Editors: Pascal Hitzler, Md Kamruzzaman Sarker, Aaron Eberhart | 2023 | Frontiers in Artificial Intelligence and Applications; IOS Press | [DOI](https://doi.org/10.3233/faia369) · ISBN 9781643684062, 9781643684079 |
| Handbook on Neurosymbolic AI and Knowledge Graphs | Editors: Pascal Hitzler, Abhilekha Dalal, Mohammad Saeid Mahdavinejad, Sanaz Saki Norouzi | 2025 | Frontiers in Artificial Intelligence and Applications; IOS Press | [DOI](https://doi.org/10.3233/faia400) · ISBN 9781643685786, 9781643685793 |
| Neurosymbolic AI: Foundations and Applications | Editors: Alvaro Velasquez, Shankar Sastry, Pradeep Ravikumar, Houbing Song, Sandeep Neema | 2026 | Wiley | [DOI](https://doi.org/10.1002/9781394302406) · ISBN 9781394302376, 9781394302406 |

### Workshop 与社区资源

| Resource | Contributors | Year | Venue / Publisher | Links |
|---|---|---|---|---|
| ICRA'25 Workshop on Foundation Models and Neuro-Symbolic AI for Robotics | Organizers: Chen Wang, Lu Gan, Yunzhu Li, Jiajun Wu, Ayoung Kim, Letizia Gionfrida, Luigi Palmieri, Alexander Gray | 2025 | ICRA 2025, Atlanta, GA, USA | [page](https://sairlab.org/icra25/) |

<!-- END GENERATED:FOUNDATIONS -->

## 🗂 仓库结构

| 路径 | 用途 |
|---|---|
| `data/papers.json` | 论文元数据、状态、研究内容与证据的单一数据源。 |
| `data/taxonomy.json` | 机器可读的暂定多轴分类体系。 |
| `data/search-log.json` | 实际执行的检索与全文资源访问记录。 |
| `docs/` | 范围、分类、定位、相关工作、路线图与迭代报告。 |
| `notes/papers/` | 单篇论文的全文阅读笔记。 |
| `website/` 与 `site/` | 静态项目网站源码与生成结果。 |
| `paper/` | LaTeX 手稿骨架与生成的 `references.bib`。 |
| `scripts/manage.py` | 校验、迁移、构建、检查与本地预览命令。 |

## 🚀 快速开始

请使用 Python 3.11 或更新版本。当前本地环境中默认 `python` 为 Python 3.10，
因此 Windows 下使用 `py -3.14`。

```powershell
py -3.14 scripts/manage.py validate
py -3.14 -m unittest discover -s tests -v
py -3.14 scripts/manage.py check --tracked-only
py -3.14 scripts/manage.py build
py -3.14 scripts/manage.py check
py -3.14 scripts/manage.py serve
```

`serve` 默认绑定 `127.0.0.1:8000`，按 `Ctrl+C` 停止。

## 🧾 如何贡献

贡献应保留证据来源，避免编造元数据。提出论文建议时，请使用提供的 Issue 模板。
详见 [CONTRIBUTING.md](CONTRIBUTING.md) 和 [data/README.md](data/README.md)。

## 🔗 常用文档

- [范围与边界](docs/scope.md)
- [检索协议](docs/search-protocol.md)
- [暂定分类体系](docs/taxonomy.md)
- [主题覆盖统计](docs/category-coverage.md)
- [基础论文、书籍与 workshop](docs/foundations.md)
- [平铺论文索引](docs/paper-index.md)
- [相关工作比较](docs/related-work-comparison.md)
- [定位与可检验假设](docs/positioning.md)
- [路线图](docs/roadmap.md)
- [论文大纲](docs/paper-outline.md)
- [第二次迭代报告](docs/iteration-02-report.md)
- [第三次迭代报告](docs/iteration-03-report.md)
- [已编译手稿](paper/main.pdf)

## 🙏 参考来源与致谢

本项目参考了相邻 UAV 综述/仓库项目。它们仅作为组织方式与边界比较的参考数据，
不复制其正文、图示或独创分类并宣称原创：

- Hub-Tian/UAVs_Meet_LLMs
- Hub-Tian/UAVs_Meet_Embodied-Intelligence
- UAVs Meet Agentic AI 综述
- Neuro-Symbolic Agentic AI for Networked Low-Altitude UAVs
- NeuroSymLand / NEUROSYMLAND 及其撤回的前一版本
- Neurosymbolic AI: The 3rd Wave
- DeepProbLog

来源追溯见 [data/reference-sources.json](data/reference-sources.json) 和
[data/papers.json](data/papers.json)。

## 📜 许可证

本仓库使用 MIT License。见 [LICENSE](LICENSE) 和
[LICENSE-NOTES.md](LICENSE-NOTES.md)。

---

> 这是一个可复现的文献综述工作区。如果你使用或扩展它，请保留证据来源，不要
> 在没有实际证据的情况下把记录标记为全文已读或已纳入。
