# 第三轮迭代报告

日期：2026-09-20

## 1. 本轮目标

本轮在已有仓库的基础上新增五大研究主题与多维方法标签，并至少为每个主题
核验/登记一篇种子文献。主题只用于展示、导航与分组，不替代
`taxonomy.json` 中的分析型标签轴，也不作为纳入/排除的自动判定依据。

## 2. 数据变更

### 2.1 主题定义

`data/taxonomy.json` 新增 `display_categories`，包含五个固定顺序、中英双语
的主题：

1. `perception_world_modeling` / 神经符号感知与世界建模
2. `reasoning_mission_planning` / 神经符号推理与任务规划
3. `navigation_control` / 神经符号导航与控制
4. `safety_verification` / 神经符号安全与验证
5. `collaboration_interaction` / 神经符号协同与交互

同时修复了 `axes` 与 `tags` 中损坏为问号的中文 `zh` 字段。

### 2.2 论文分类字段

`data/papers.json` 每条记录新增：

- `primary_category`：唯一主主题或 `null`；
- `secondary_categories`：去重后的交叉主题列表；
- `classification_rationale`：分类理由；
- `classification_evidence_refs`：用于分类的原文/证据链接；
- `classification_status`：`provisional` 或 `reviewed`。

主主题不能同时出现在次主题中；同一篇文献只在主主题分组中计为一次唯一研究，
次主题只作为交叉引用。

### 2.3 新增种子文献

| ID | 主主题 | 阅读深度 | 状态 |
|---|---|---|---|
| `p-2409.10196` NEUSIS | `perception_world_modeling` | `fulltext_reviewed` | `candidate` |
| `p-2603.27583` LLM-STL 导航 | `navigation_control` | `abstract_reviewed` | `candidate` |
| `p-2603.07824` MINT | `collaboration_interaction` | `fulltext_reviewed` | `candidate` |

NEUSIS 与 MINT 均已读取 HTML 全文并记录证据；LLM-STL 论文的 HTML 全文两次
超时，因此保持摘要级、`provisional` 分类，不标记为全文已读。

## 3. 已有文献的主题分配

- `p-2609.19961`：主主题 `reasoning_mission_planning`，次主题
  `safety_verification`、`collaboration_interaction`。保留
  `record_type=position`，不纳入核心方法计数。
- `p-2607.02277` NEUROSYMLAND：主主题 `safety_verification`，次主题
  `perception_world_modeling`。保留元数据冲突与前置撤回版本关系。
- 综述、背景与撤回版本保留 `primary_category=null`，不重复计入主题覆盖数。

## 4. 生成物

- `README.md` / `README.zh-CN.md`：由原平铺论文表改为五个主题分组，
  并保留生成标记。
- `docs/paper-index.md`：新增的平铺论文索引。
- `docs/category-coverage.md`：新增的主题覆盖与缺口统计。
- `docs/evidence-matrix.md`：证据矩阵新增分类列。
- `docs/taxonomy.md`：补充“展示主题 vs 标签轴”及主/次主题规则。
- `docs/paper-outline.md`：第 5 章映射到五个研究主题。
- `website/`：主题筛选下拉框由 `TAXONOMY_DATA_JSON` 生成，保留任务、
  融合方向、状态筛选，并保留无 JavaScript 表格。
- `paper/references.bib`：继续由已验证数据生成，新记录自动进入引用文件。

## 5. 校验结果

已完成数据校验、测试和生成结果一致性检查。

结果：

- 验证通过：10 条记录、5 个候选、4 篇全文已读、0 篇正式纳入核心方法。
- 43 项测试全部通过。
- 生成文件与数据源同步检查通过。
- 连续两次 `build` 的 `site/` 哈希一致，构建确定。

## 6. 仍未做的事

- 没有将任何候选记录提升为 `included` 核心方法。
- 没有宣称已部署公开网站。
- 没有提交、推送或修改 Git 历史。
- 没有为摘要级论文 `p-2603.27583` 声称已核验全文结论。
- 没有基于标题、关键词或发表状态自动判定主题；所有分类均附书面理由与证据引用。

## 7. 需要人工复核的点

- `p-2603.27583` 的全文、真实飞行实验与安全保证仍需在全文可用后复核。
- `p-2607.02277` 的 venue/DOI 冲突仍需出版方记录确认。
- NEUSIS 官方代码仓库的许可与可复现性尚未完整审计。
- 所有 `human_reviewed` 仍为 `false`。
