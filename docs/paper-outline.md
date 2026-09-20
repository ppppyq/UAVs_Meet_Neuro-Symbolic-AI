# Paper outline

Working title: *UAVs Meet Neuro-Symbolic AI: Foundations, Taxonomy, and
Perspectives for Trustworthy Aerial Autonomy*

Status: manuscript in preparation.

## 1. Introduction and Research Questions

- Questions: Why trustworthiness matters for UAV autonomy; why neither neural
  learning alone nor symbolic reasoning alone is sufficient; what the working
  research question is.
- Evidence: motivation from verified adjacent surveys and direct UAV candidates.
- Planned table/figure: proposed autonomy stack overview.
- Gap: no completed systematic review or novelty claim yet.

## 2. Review Methodology and Scope

- Questions: What is included, excluded, and why; how metadata, screening, and
  evidence quality are separated.
- Evidence: inclusion criteria, search protocol, search log, version tracking.
- Planned table/figure: PRISMA-like or lightweight screening flow.
- Gap: only seed-level searches have been performed.

## 3. Foundations and Conceptual Boundaries

- Questions: What counts as neural learning, symbolic representation/reasoning,
  and functional coupling; what does not automatically qualify.
- Evidence: `docs/scope.md`; general foundations such as Neurosymbolic AI: The
  3rd Wave and DeepProbLog.
- Planned table/figure: concept-boundary table.
- Gap: full-text synthesis of foundation papers not yet completed.

## 4. Taxonomy of Neuro-Symbolic UAV Systems

- Questions: How to organize methods without collapsing dimensions into one
  tree; how tags support comparison.
- Evidence: `data/taxonomy.json`; tagged candidate records.
- Planned table/figure: multi-axis taxonomy diagram.
- Gap: taxonomy is proposed v0.1 and may change with more evidence.

## 5. Methods Across the UAV Autonomy Stack

- Questions: How neuro-symbolic integration appears in grounding,
  representation, reasoning, planning, execution, and assurance.
- Evidence: included direct UAV methods, with coupling and validation scope.
- Planned table/figure: method table by functional position and coupling
  direction.
- Gap: no method has yet been promoted to `included` after full-text review.

## 6. Evaluation, Benchmarks, and Evidence Quality

- Questions: What evidence exists for safety, interpretability, generalization,
  and resource feasibility; what cannot be compared across environments.
- Evidence: `uav_evidence`, limitations, benchmark plan.
- Planned table/figure: evidence-quality matrix.
- Gap: no benchmark execution; no numerical ranking is justified.

## 7. Open Challenges and Research Opportunities

- Questions: Which gaps are evidenced by current candidates rather than assumed.
- Evidence: limitations recorded per paper plus explicit research directions.
- Planned table/figure: challenge-to-evidence map.
- Gap: requires more full-text and systematic search evidence.

## 8. Conclusion

- Questions: What can be stated now and what remains open.
- Evidence: only conclusions supported by reviewed material.
- Planned table/figure: none or a compact summary.
- Gap: no final conclusion until the review matures.

## Writing strategy

Do not rewrite the same content three times under “integration mechanism”,
“task”, and “knowledge representation”. Use main sections plus multi-axis
comparison tables.
