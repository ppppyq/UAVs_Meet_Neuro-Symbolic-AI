# 🚁 UAVs Meet Neuro-Symbolic AI 🧠

让无人机的学习式感知与显式、可审计的推理相遇，服务于可信自主性。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Website](https://img.shields.io/badge/Read-online_survey-236b71.svg)](https://ppppyq.github.io/UAVs_Meet_Neuro-Symbolic-AI/)
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

[English](README.md) · [简体中文](README.zh-CN.md)

[在线阅读综述](https://ppppyq.github.io/UAVs_Meet_Neuro-Symbolic-AI/)：浏览神经符号 AI 基础与五个研究方向。

[本轮检索记录（2026-09-22）](docs/literature-review.md)说明检索范围、阅读深度和证据边界。

本综述与网页采用相同的六部分结构：先介绍神经符号 AI 基础，再展开五个研究方向。
方向划分采用 `Proposed taxonomy v0.1`，属于工作性提议。主方向互斥，次方向仅作
交叉引用，不会增加唯一研究计数。完整记录见[论文索引](docs/paper-index.md)。

<!-- BEGIN GENERATED:README-NAV -->

## 阅读导航

1. [神经符号 AI 基础](#foundations)
2. [神经符号感知与世界建模](#theme-perception_world_modeling)
3. [神经符号推理与任务规划](#theme-reasoning_mission_planning)
4. [神经符号导航与控制](#theme-navigation_control)
5. [神经符号安全与验证](#theme-safety_verification)
6. [神经符号协同与交互](#theme-collaboration_interaction)

<!-- END GENERATED:README-NAV -->

<a id="foundations"></a>

## 1. 神经符号 AI 基础

<!-- BEGIN GENERATED:FOUNDATIONS -->

以下资源用于提供理论基础、书籍参考和社区信息。它们是辅助性资源，不计入 UAV 文献记录或核心方法统计。

### 文献综述 · 2026-09-22

本轮为有限范围的来源核查与文献扩展，并非穷尽式系统综述。全文、选段与摘要证据分别标记；所有记录均尚待人工复核。

本综述将神经符号系统理解为：学习组件与具有明确语义的表示发生实际功能耦合，例如逻辑事实、可执行程序、任务自动机或约束。三个基础入口分别是 DeepProbLog 的神经谓词与概率推理、Logic Tensor Networks 的可微逻辑接地，以及 Scallop 基于溯源语义的关系程序推理。

[DeepProbLog: Neural Probabilistic Logic Programming](https://arxiv.org/abs/1805.10872) / [Logic Tensor Networks](https://openaccess.city.ac.uk/id/eprint/27580/) / [Scallop: A Language for Neurosymbolic Programming](https://pldi23.sigplan.org/details/pldi-2023-pldi/61/Scallop-A-Language-for-Neurosymbolic-Programming)

这些机制回答的问题并不相同：查询概率、模糊真值与时序规格满足性，不能互换成同一种置信度或安全指标。面向 UAV，需要说明感知如何成为符号、推理如何改变动作，以及推理依赖哪些假设。仅使用 LLM、图结构或优化器，并不足以说明这一耦合。

[DeepProbLog: Neural Probabilistic Logic Programming](https://arxiv.org/abs/1805.10872) / [Logic Tensor Networks](https://openaccess.city.ac.uk/id/eprint/27580/) / [Scallop: A Language for Neurosymbolic Programming](https://pldi23.sigplan.org/details/pldi-2023-pldi/61/Scallop-A-Language-for-Neurosymbolic-Programming)

本轮 UAV 样本主要在推理阶段连接预训练神经模块与显式推理，并不能证明端到端可微神经符号训练普遍更优。基础工具用于解释方法，不应被计作额外 UAV 实验结果；LTN 与 Scallop 本轮只阅读了选定的导论段落，未标为全文审阅。

[NEUSIS: A Compositional Neuro-Symbolic Framework for Autonomous Perception, Reasoning, and Planning in Complex UAV Search Missions](https://arxiv.org/abs/2409.10196) / [Probabilistic Mission Design for Neuro-Symbolic Unmanned Aircraft Systems](https://arxiv.org/abs/2501.01439) / [Scallop: A Language for Neurosymbolic Programming](https://pldi23.sigplan.org/details/pldi-2023-pldi/61/Scallop-A-Language-for-Neurosymbolic-Programming)

**开放问题:** 如何同时公开感知校准、逻辑语义与运行假设，使系统声称的保证能够被核查？

### 基础论文

| Resource | Contributors | Year | Venue / Publisher | Links |
|---|---|---|---|---|
| Neural-Symbolic Learning and Reasoning: A Survey and Interpretation | Authors: Tarek R. Besold, Artur d'Avila Garcez, Sebastian Bader, Howard Bowman, Pedro Domingos, Pascal Hitzler, Kai-Uwe Kuehnberger, Luis C. Lamb, Daniel Lowd, Priscila Machado Vieira Lima, Leo de Penning, Gadi Pinkas, Hoifung Poon, Gerson Zaverucha | 2017 | arXiv preprint | [arXiv](https://arxiv.org/abs/1711.03902) |
| Neurosymbolic Programming | Authors: Swarat Chaudhuri, Kevin Ellis, Oleksandr Polozov, Rishabh Singh, Armando Solar-Lezama, Yisong Yue | 2021 | Foundations and Trends in Programming Languages, 7(3), 158-243; Now Publishers | [DOI](https://doi.org/10.1561/2500000049) |
| Neuro-symbolic artificial intelligence: Current trends | Authors: Md Kamruzzaman Sarker, Lu Zhou, Aaron Eberhart, Pascal Hitzler | 2022 | AI Communications, 34(3), 197-209; SAGE Publications | [DOI](https://doi.org/10.3233/aic-210084) |
| Logic Tensor Networks | Authors: Samy Badreddine, Artur d'Avila Garcez, Luciano Serafini, Michael Spranger | 2022 | Artificial Intelligence 303, 103649; Elsevier | [DOI](https://doi.org/10.1016/j.artint.2021.103649) · [arXiv](https://arxiv.org/abs/2012.13635) |
| Scallop: A Language for Neurosymbolic Programming | Authors: Ziyang Li, Jiani Huang, Mayur Naik | 2023 | Proceedings of the ACM on Programming Languages 7 (PLDI), 1463–1487 | [DOI](https://doi.org/10.1145/3591280) · [arXiv](https://arxiv.org/abs/2304.04812) |

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

### 相关综述与筛选背景

以下条目来自论文数据库，尚未分配主研究方向。保留这些条目是为了提供背景和筛选来源，不代表已纳入的 UAV 核心方法。它们与上面的辅助资源单独统计。

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

## 2. 神经符号感知与世界建模

Methods where neural perception grounds explicit symbols or maintains a probabilistic/semantic world model used by symbolic reasoning.

**边界:** Use when perception and world-state maintenance are functionally coupled to symbolic structure. Exclude standalone detectors or purely latent world models without explicit symbolic semantics.

**子方向：** Symbol grounding and scene graphs; Probabilistic and semantic world models; Multimodal perception for UAV search

### 文献综述 · 2026-09-22

本轮为有限范围的来源核查与文献扩展，并非穷尽式系统综述。全文、选段与摘要证据分别标记；所有记录均尚待人工复核。

这一方向的关键接口，是把不确定的视觉观测转成可持续更新、可供规划器查询的实体、关系和世界状态。NEUSIS 将神经接地、程序化接口、滤波世界模型和约束搜索规划连接起来，符号层实际影响搜索目标和观测融合，而不只是保存一张描述性图。

[NEUSIS: A Compositional Neuro-Symbolic Framework for Autonomous Perception, Reasoning, and Planning in Complex UAV Search Missions](https://arxiv.org/abs/2409.10196)

NEUSIS 的证据来自 AirSim/HAMERITT 仿真，初始占据图与俯视地图使用真值。其搜索指标衡量正确定位的实体，不能解释为飞行安全率，误报也需要另行考察。SayPlan 提供了可迁移的层级场景图与计划验证思路，但移动操作机器人实验不等于 UAV 实验，本轮也只检查了其部分方法段落。

[NEUSIS: A Compositional Neuro-Symbolic Framework for Autonomous Perception, Reasoning, and Planning in Complex UAV Search Missions](https://arxiv.org/abs/2409.10196) / [SayPlan: Grounding Large Language Models using 3D Scene Graphs for Scalable Robot Task Planning](https://proceedings.mlr.press/v229/rana23a.html)

这些工作提示，世界模型应同时记录语义结构、观测来源及其不确定性。过期地图、位姿误差与动态目标下的稳健性，仍需面向部署单独验证，不能由“使用场景图”直接推出。

[NEUSIS: A Compositional Neuro-Symbolic Framework for Autonomous Perception, Reasoning, and Planning in Complex UAV Search Missions](https://arxiv.org/abs/2409.10196) / [SayPlan: Grounding Large Language Models using 3D Scene Graphs for Scalable Robot Task Planning](https://proceedings.mlr.press/v229/rana23a.html)

**开放问题:** 在没有准确初始地图时，规划器能否发现并修复错误的符号世界状态？


### 已纳入的核心方法

| Paper | Neural–Symbolic Coupling | UAV Task | Evidence / Review | Publication | Links |
|---|---|---|---|---|---|
| [NEUSIS: A Compositional Neuro-Symbolic Framework for Autonomous Perception, Reasoning, and Planning in Complex UAV Search Missions](https://arxiv.org/abs/2409.10196) | GRiD neural perception produces noisy symbolic detections and attributes; the probabilistic world model reasons over and accumulates those symbols, then SNaC consumes the updated belief map for hierarchical planning. | search_and_exploration, navigation | fulltext_reviewed / simulation | preprint | [paper](https://arxiv.org/abs/2409.10196) · [code](https://github.com/ControlNet/NEUSIS) |


### 可迁移的机器人方法

| Paper | Neural–Symbolic Coupling | UAV Task | Evidence / Review | Publication | Links |
|---|---|---|---|---|---|
| [SayPlan: Grounding Large Language Models using 3D Scene Graphs for Scalable Robot Task Planning](https://proceedings.mlr.press/v229/rana23a.html) | Symbolic graph search restricts context; simulator feedback rejects infeasible actions and drives LLM replanning. | — | abstract_reviewed / none | Published (Conference on Robot Learning (CoRL), PMLR 229:23-72, 2023) | [paper](https://proceedings.mlr.press/v229/rana23a.html) · code: — / not verified |


### 跨方向引用

`p-2607.02277`, `p-2501.01439` 的主方向归属在其他章节，此处仅作交叉引用。

<a id="theme-reasoning_mission_planning"></a>

## 3. 神经符号推理与任务规划

Methods that combine explicit logic, constraints, probabilistic logic, or symbolic planning with learned components for mission-level reasoning and task sequencing.

**边界:** Use for explicit symbolic inference or mission/task planning. Exclude low-level trajectory optimization without a discrete symbolic model.

**子方向：** Logic and constraint reasoning; Task planning and goal management; Uncertainty-aware reasoning

### 文献综述 · 2026-09-22

本轮为有限范围的来源核查与文献扩展，并非穷尽式系统综述。全文、选段与摘要证据分别标记；所有记录均尚待人工复核。

本轮可归纳出两条路线：对任务规则进行概率推理，以及把语言指令翻译成可执行任务规格。ProMis 在混合概率逻辑程序中结合不确定地理关系与神经变化检测输出，生成概率任务地图；AutoTAMP 则将指令转为信号时序逻辑，并通过检查与反馈迭代修复任务和运动计划。

[Probabilistic Mission Design for Neuro-Symbolic Unmanned Aircraft Systems](https://arxiv.org/abs/2501.01439) / [AutoTAMP: Autoregressive Task and Motion Planning with LLMs as Translators and Checkers](https://arxiv.org/abs/2306.06531)

ProMis 提供的是离线地图计算案例，未展示闭环飞行；逐点规则满足概率既不是整条轨迹的碰撞概率，也不构成实际飞行许可。AutoTAMP 的主要评估来自二维任务域，补充的三维无人机示例省略语义检查，实物演示使用地面机器人。因此，即使已阅读全文，本综述仍将其保留为 UAV 候选方法。

[Probabilistic Mission Design for Neuro-Symbolic Unmanned Aircraft Systems](https://arxiv.org/abs/2501.01439) / [AutoTAMP: Autoregressive Task and Motion Planning with LLMs as Translators and Checkers](https://arxiv.org/abs/2306.06531)

由此可见，形式合法的逻辑计划仍可能误解人的意图，或基于过期环境。综述与实验应分别报告翻译忠实度、逻辑可行性、运动可行性和执行结果，并说明这些阶段之间如何反馈。

[Probabilistic Mission Design for Neuro-Symbolic Unmanned Aircraft Systems](https://arxiv.org/abs/2501.01439) / [AutoTAMP: Autoregressive Task and Motion Planning with LLMs as Translators and Checkers](https://arxiv.org/abs/2306.06531)

**开放问题:** 如何在一个可行但偏离意图的计划被执行之前，检测语义翻译错误与任务规则变化？


### 已纳入的核心方法

| Paper | Neural–Symbolic Coupling | UAV Task | Evidence / Review | Publication | Links |
|---|---|---|---|---|---|
| [Probabilistic Mission Design for Neuro-Symbolic Unmanned Aircraft Systems](https://arxiv.org/abs/2501.01439) | Neural probabilities become logic facts; inference produces a spatial field of modeled requirement satisfaction. | mission_planning | fulltext_reviewed / conceptual | Published (IEEE Transactions on Intelligent Transportation Systems 26(12), 22751-22760 (2025)) | [paper](https://arxiv.org/abs/2501.01439) · [code](https://github.com/HRI-EU/ProMis) |


### 候选方法

| Paper | Neural–Symbolic Coupling | UAV Task | Evidence / Review | Publication | Links |
|---|---|---|---|---|---|
| [AutoTAMP: Autoregressive Task and Motion Planning with LLMs as Translators and Checkers](https://arxiv.org/abs/2306.06531) | Planner trajectories and syntax feedback guide repeated LLM translation; STL constrains joint task/motion synthesis. | mission_planning, navigation | fulltext_reviewed / simulation | Published (IEEE International Conference on Robotics and Automation (ICRA), 2024) | [paper](https://arxiv.org/abs/2306.06531) · code: — / not verified |


### 相关架构与观点

| Paper | Neural–Symbolic Coupling | UAV Task | Evidence / Review | Publication | Links |
|---|---|---|---|---|---|
| [Neuro-Symbolic Agentic AI for Networked Low-Altitude UAVs](https://arxiv.org/abs/2609.19961) | Neural grounding feeds an agentic symbolic planning and verification loop; execution/connectivity feedback updates task state and triggers sensing or replanning. | communication_and_networking, mission_planning | fulltext_reviewed / conceptual, simulation | preprint | [paper](https://arxiv.org/abs/2609.19961) · code: — / not verified |


### 跨方向引用

`p-2409.10196`, `p-2603.27583`, `p-2603.07824`, `p-2312.14950`, `p-2307.06135`, `p-simultech-2026-solver-selection` 的主方向归属在其他章节，此处仅作交叉引用。

<a id="theme-navigation_control"></a>

## 4. 神经符号导航与控制

Methods that couple learned perception/language interfaces with symbolic specifications, constraints, planners, or control structures for motion-level UAV navigation.

**边界:** Use for motion-level navigation and control where symbolic structure shapes or guards learned behavior. Exclude pure end-to-end control without explicit semantics.

**子方向：** Natural-language to formal specification; Constraint-guided trajectory synthesis; Safe motion planning

### 文献综述 · 2026-09-22

本轮为有限范围的来源核查与文献扩展，并非穷尽式系统综述。全文、选段与摘要证据分别标记；所有记录均尚待人工复核。

显式规格以不同方式连接学习行为与连续运动。Verified Compositions of Neural Network Controllers 将共安全 LTL 任务分解为自动机迁移，再用可达集分析选择满足要求的神经控制器组合。LLM-STL Navigation 将语言转为用于轨迹优化的 STL 约束，并在请求不可行时进行诊断与受限修复。

[Verified Compositions of Neural Network Controllers for Temporal Logic Control Objectives](https://arxiv.org/abs/2209.06130) / [LLM-Enabled Low-Altitude UAV Natural Language Navigation via Signal Temporal Logic Specification Translation and Repair](https://arxiv.org/abs/2603.27583)

控制器组合研究使用数值 UAV 动力学实验，没有实飞证据；其保证依赖动力学模型、初始状态集合及可靠的可达集外包络。LLM-STL 报告了仿真与 DJI Matrice 300 RTK 户外演示，但公式精确匹配率衡量的是翻译表现，不能替代飞行安全率，单项演示也不能证明广泛运行条件下的成功率。

[Verified Compositions of Neural Network Controllers for Temporal Logic Control Objectives](https://arxiv.org/abs/2209.06130) / [LLM-Enabled Low-Altitude UAV Natural Language Navigation via Signal Temporal Logic Specification Translation and Repair](https://arxiv.org/abs/2603.27583)

这两类工作提供互补的证据：一类在给定假设下开展形式推理，另一类在特定条件下展示物理执行。比较时应同时考察规格语义、模型失配、求解延迟、回退行为，以及约束放松的范围。

[Verified Compositions of Neural Network Controllers for Temporal Logic Control Objectives](https://arxiv.org/abs/2209.06130) / [LLM-Enabled Low-Altitude UAV Natural Language Navigation via Signal Temporal Logic Specification Translation and Repair](https://arxiv.org/abs/2603.27583)

**开放问题:** 在感知延迟、动力学失配和机载算力约束下，能否保持规格满足性，而不隐式削弱安全约束？


### 已纳入的核心方法

| Paper | Neural–Symbolic Coupling | UAV Task | Evidence / Review | Publication | Links |
|---|---|---|---|---|---|
| [LLM-Enabled Low-Altitude UAV Natural Language Navigation via Signal Temporal Logic Specification Translation and Repair](https://arxiv.org/abs/2603.27583) | The LLM proposes STL; solver conflicts guide temporal/predicate repair while the optimization layer chooses relaxation magnitudes. | navigation | fulltext_reviewed / simulation, real_flight | preprint | [paper](https://arxiv.org/abs/2603.27583) · code: — / not verified |
| [Verified Compositions of Neural Network Controllers for Temporal Logic Control Objectives](https://arxiv.org/abs/2209.06130) | Automaton search accepts neural-controller sequences only when their reachable sets satisfy each reach-avoid transition. | navigation | fulltext_reviewed / simulation | Published (2022 IEEE 61st Conference on Decision and Control, 4004-4009) | [paper](https://arxiv.org/abs/2209.06130) · code: — / not verified |


### 跨方向引用

`p-2409.10196`, `p-2306.06531`, `p-2409.10283` 的主方向归属在其他章节，此处仅作交叉引用。

<a id="theme-safety_verification"></a>

## 5. 神经符号安全与验证

Methods focused on safety constraints, verification, monitoring, shielding, or assurance evidence tied to neural-symbolic integration.

**边界:** Use when assurance is explicitly coupled to learned components. Exclude standalone formal methods on fixed purely symbolic models.

**子方向：** Runtime monitoring and shielding; Landing and safety assessment; Formal verification of learned components

### 文献综述 · 2026-09-22

本轮为有限范围的来源核查与文献扩展，并非穷尽式系统综述。全文、选段与摘要证据分别标记；所有记录均尚待人工复核。

安全证据首先需要明确验证对象：动作前置条件、着陆决策、可达状态集合，还是轨迹时序规格。神经控制器组合与 LLM-STL 分别提供可达性分析与规格约束的跨方向案例，但二者都不能自动保证上游感知或语言理解始终正确。

[Verified Compositions of Neural Network Controllers for Temporal Logic Control Objectives](https://arxiv.org/abs/2209.06130) / [LLM-Enabled Low-Altitude UAV Natural Language Navigation via Signal Temporal Logic Specification Translation and Repair](https://arxiv.org/abs/2603.27583)

NeuroSymLand 保留为已阅读全文的候选工作，其发表场所来源冲突尚未解决；符号着陆决策流程也不能直接提升为通用闭环飞行保证。ASMA 是采用自适应 CBF/MPC 安全约束的已发表视觉语言导航相关研究，本轮仍属于摘要级审阅：其语义耦合与假设需要全文核查，单独采用 CBF/MPC 不满足本综述的核心纳入标准。

[NEUROSYMLAND: Neuro-Symbolic Landing-Site Assessment for Robust and Edge-Deployable UAV Autonomy](https://arxiv.org/abs/2607.02277) / [ASMA: An Adaptive Safety Margin Algorithm for Vision-Language Drone Navigation via Scene-Aware Control Barrier Functions](https://arxiv.org/abs/2409.10283)

当前样本不支持用一个统一安全分数对这些方法排名。更有价值的安全论证，应区分语义正确性、附带假设的数学保证、运行监测和实际观测到的违规，并报告超出环境假设时的失效。

[Verified Compositions of Neural Network Controllers for Temporal Logic Control Objectives](https://arxiv.org/abs/2209.06130) / [LLM-Enabled Low-Altitude UAV Natural Language Navigation via Signal Temporal Logic Specification Translation and Repair](https://arxiv.org/abs/2603.27583) / [NEUROSYMLAND: Neuro-Symbolic Landing-Site Assessment for Robust and Edge-Deployable UAV Autonomy](https://arxiv.org/abs/2607.02277)

**开放问题:** 哪些失效不在现有保证范围内？运行系统能否及时检测假设被破坏，并触发安全回退？


### 候选方法

| Paper | Neural–Symbolic Coupling | UAV Task | Evidence / Review | Publication | Links |
|---|---|---|---|---|---|
| [NEUROSYMLAND: Neuro-Symbolic Landing-Site Assessment for Robust and Edge-Deployable UAV Autonomy](https://arxiv.org/abs/2607.02277) | Neural perception populates the PSSG; deterministic symbolic rules then evaluate candidate landing regions over that explicit representation. The runtime does not query the LLM; LLM-assisted authoring occurs offline before deployment. | landing | fulltext_reviewed / simulation, hardware_in_loop | conflict | [paper](https://arxiv.org/abs/2607.02277) · [code](https://github.com/Janus117/NeuroSymbolicLand) |
| [ASMA: An Adaptive Safety Margin Algorithm for Vision-Language Drone Navigation via Scene-Aware Control Barrier Functions](https://arxiv.org/abs/2409.10283) | Learned landmark navigation is constrained by a depth-based adaptive safety layer. | navigation | abstract_reviewed / simulation | Published (IEEE Robotics and Automation Letters 10(9), 9232–9239) | [paper](https://arxiv.org/abs/2409.10283) · code: — / not verified |


### 跨方向引用

`p-2609.19961`, `p-2603.27583`, `p-2501.01439`, `p-2209.06130` 的主方向归属在其他章节，此处仅作交叉引用。

<a id="theme-collaboration_interaction"></a>

## 6. 神经符号协同与交互

Methods where explicit symbolic structure supports human-UAV, multi-UAV, or networked collaboration and information exchange.

**边界:** Use when collaboration/interaction is central to the neuro-symbolic method, not merely a deployment label.

**子方向：** Human-UAV knowledge interaction; Multi-UAV coordination; Networked and edge-cloud autonomy

### 文献综述 · 2026-09-22

本轮为有限范围的来源核查与文献扩展，并非穷尽式系统综述。全文、选段与摘要证据分别标记；所有记录均尚待人工复核。

人机交互与多机协同需要不同的验证证据。TypeFly 将语言编译为 MiniSpec 程序，显式表示技能、条件、有界循环与反馈重规划，并在室内 Tello 上评估。MINT 维护显式假设树，在不同解释会改变飞行路径时发起询问，再用人的回答剪枝任务状态。

[TypeFly: Flying Drones with Large Language Model](https://arxiv.org/abs/2312.14950) / [Reasoning Knowledge-Gap in Drone Planning via LLM-based Active Elicitation](https://arxiv.org/abs/2603.07824)

TypeFly 的受限程序执行并不构成避碰证明。MINT 的证据包括仿真与小规模实物歧义消解实验；询问次数减少本身不能证明人的认知负担降低，方法也假设回答可信。其发表场所是 AAAI Spring Symposium Series，而非 AAAI 主会。

[TypeFly: Flying Drones with Large Language Model](https://arxiv.org/abs/2312.14950) / [Reasoning Knowledge-Gap in Drone Planning via LLM-based Active Elicitation](https://arxiv.org/abs/2603.07824)

多机层面，Learning-Guided Symbolic Solver Selection 提出由 Double DQN 元控制器选择符号分配求解器，并结合可行性筛选。由于全文需要登录，本轮仅核对官方摘要与发表信息，因此它是候选线索，不能用来证明已验证的机群安全性或实飞扩展性。

[Learning-Guided Symbolic Solver Selection for Dynamic Multi-UAV Missions in Simulation](https://www.insticc.org/node/TechnicalProgram/simultech/2026/presentationDetails/149518)

**开放问题:** 从单人单机扩展到多人多机时，应如何表达不确定性、通信成本和意图分歧？


### 已纳入的核心方法

| Paper | Neural–Symbolic Coupling | UAV Task | Evidence / Review | Publication | Links |
|---|---|---|---|---|---|
| [Reasoning Knowledge-Gap in Drone Planning via LLM-based Active Elicitation](https://arxiv.org/abs/2603.07824) | The VLM identifies semantic uncertainty; MINT represents it as a symbolic tree; the LLM chooses a binary query; the human answer prunes the tree and updates the semantic map and plan. | navigation, search_and_exploration | fulltext_reviewed / simulation, real_flight | Published (Proceedings of the AAAI Symposium Series 8(1), 127-131 (2026)) | [paper](https://arxiv.org/abs/2603.07824) · code: — / not verified |
| [TypeFly: Flying Drones with Large Language Model](https://arxiv.org/abs/2312.14950) | Neural outputs become executable programs; the interpreter invokes skills and requests replanning using updated observations. | navigation, search_and_exploration | fulltext_reviewed / real_flight | preprint | [paper](https://arxiv.org/abs/2312.14950) · code: — / not verified |


### 候选方法

| Paper | Neural–Symbolic Coupling | UAV Task | Evidence / Review | Publication | Links |
|---|---|---|---|---|---|
| [Learning-Guided Symbolic Solver Selection for Dynamic Multi-UAV Missions in Simulation](https://www.insticc.org/node/TechnicalProgram/simultech/2026/presentationDetails/149518) | A learned meta-controller selects a solver; its candidate assignment is checked and evaluated in simulation. | multi_uav_coordination | abstract_reviewed / simulation | Published (SIMULTECH 2026, pp. 595–607) | [paper](https://www.insticc.org/node/TechnicalProgram/simultech/2026/presentationDetails/149518) · code: — / not verified |


### 跨方向引用

`p-2609.19961`, `p-2306.06531` 的主方向归属在其他章节，此处仅作交叉引用。

<!-- END GENERATED:RESEARCH-THEMES -->

---

## 🌐 项目概览

这是一个持续更新的文献综述，主题是**神经符号 UAV 自主性**。它
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

- 文献记录总数：17
- 元数据已核验：16
- 元数据冲突：1
- 已做摘要阅读：8
- 已做全文阅读：9
- 候选条目：6
- 直接 UAV 候选方法：4
- 核心 UAV 方法（已纳入、去重、非撤回）：6
- 唯一种子研究（去重、非撤回）：16
- 撤回/版本关联条目：1
- 待复核分类迁移：1

<!-- END GENERATED:OVERVIEW -->

## 🗂 研究资料

| 路径 | 用途 |
|---|---|
| `data/papers.json` | 论文元数据、状态、研究内容与证据的单一数据源。 |
| `data/taxonomy.json` | 机器可读的暂定多轴分类体系。 |
| `data/search-log.json` | 实际执行的检索与全文资源访问记录。 |
| `docs/` | 范围、分类、定位、相关工作、路线图与生成的覆盖文档。 |
| `notes/papers/` | 单篇论文的全文阅读笔记。 |
| `paper/` | LaTeX 手稿骨架与生成的 `references.bib`。 |

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
- [LaTeX 手稿源文件](paper/main.tex)

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
