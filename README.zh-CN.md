# UAVs Meet Neuro-Symbolic AI

**暂定标题：** UAVs Meet Neuro-Symbolic AI: Foundations, Taxonomy, and
Perspectives for Trustworthy Aerial Autonomy

**状态：** 论文撰写中（manuscript in preparation）。本仓库是一个轻量的文献综述
工程工作区，不是已完成的系统综述，也不是实验系统。

仓库地址：<https://github.com/ppppyq/UAVs_Meet_Neuro-Symbolic-AI>

## 工作性研究问题

神经学习与显式符号表示、推理和约束如何集成，以支持可信的 UAV 自主性？

## 研究边界

本项目关注“神经符号 UAV 自主性”，而不是所有“使用了 AI 的 UAV”。使用 LLM、
Agent、知识图谱、MPC、CBF 或形式化验证器，并不自动等同于神经符号 AI。具体纳入
与排除规则见 [docs/scope.md](docs/scope.md)。

概念框架、仿真、硬件在环和真实飞行证据分别记录。作者、单位、GitHub
用户/仓库、目标期刊和许可证尚未提供，均以 `null`/TODO 保留，不自行编造。

## 暂定分类体系

分类体系为 `Proposed taxonomy v0.1`，不是学界共识。它采用五个相互独立的标签轴：

- 功能位置；
- 融合方向；
- 符号机制；
- UAV 任务；
- 系统与部署形式。

详见 [docs/taxonomy.md](docs/taxonomy.md) 和
[data/taxonomy.json](data/taxonomy.json)。

## 当前证据状态

种子条目仅完成了元数据/摘要层面的核验。尚未有论文在全文阅读后被提升为
`included`，因此当前核心 UAV 方法数量为零。已核验元数据与摘要级候选会在下方
分开展示。

<!-- BEGIN GENERATED:OVERVIEW -->

- 文献记录总数：7
- 元数据已核验：6
- 元数据冲突：1
- 已做摘要阅读：7
- 已做全文阅读：0
- 候选条目：2
- 直接 UAV 候选方法：2
- 核心 UAV 方法（已纳入、去重、非撤回）：0
- 撤回/版本关联条目：1

<!-- END GENERATED:OVERVIEW -->

## 论文列表

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

## 本地运行

请使用 Python 3.11 或更新版本。

```powershell
python scripts/manage.py validate
python -m unittest discover -s tests -v
python scripts/manage.py build
python scripts/manage.py check
python scripts/manage.py serve
```

网站生成到 `site/`。`serve` 默认只绑定 `127.0.0.1:8000`，按 `Ctrl+C` 关闭。

新增或更新论文时，请编辑 `data/papers.json`；若需要新标签，同时更新
`data/taxonomy.json`，然后运行上述校验与构建命令。字段说明见
[data/README.md](data/README.md)，贡献方式见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 参考来源与致谢

本项目参考了相邻 UAV 综述/仓库项目。它们仅作为组织方式和边界比较的参考数据，
不复制其正文、图示或独创分类并宣称原创：

- Hub-Tian/UAVs_Meet_LLMs
- Hub-Tian/UAVs_Meet_Embodied-Intelligence
- UAVs Meet Agentic AI 综述
- Neuro-Symbolic Agentic AI for Networked Low-Altitude UAVs
- NEUROSYMLAND 及其撤回的前一版本
- Neurosymbolic AI: The 3rd Wave
- DeepProbLog

来源追溯见 `data/reference-sources.json` 和 `data/papers.json`。

## 贡献方式

见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可证

本仓库使用 MIT License。见 [LICENSE](LICENSE) 和
[LICENSE-NOTES.md](LICENSE-NOTES.md)。
