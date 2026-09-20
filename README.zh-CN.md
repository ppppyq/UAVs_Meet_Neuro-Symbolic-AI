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

- 文献记录总数：7
- 元数据已核验：6
- 元数据冲突：1
- 已做摘要阅读：5
- 已做全文阅读：2
- 候选条目：2
- 直接 UAV 候选方法：1
- 核心 UAV 方法（已纳入、去重、非撤回）：0
- 撤回/版本关联条目：1
- 待复核分类迁移：1

<!-- END GENERATED:OVERVIEW -->

## 📚 论文列表

每行都由同一数据源生成。筛选状态、元数据、阅读状态与证据状态分开显示。

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
- [相关工作比较](docs/related-work-comparison.md)
- [定位与可检验假设](docs/positioning.md)
- [路线图](docs/roadmap.md)
- [论文大纲](docs/paper-outline.md)
- [第二次迭代报告](docs/iteration-02-report.md)
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
