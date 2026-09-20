# Benchmark plan

This is a future evaluation design, **not** a set of executed experiments.

## Proposed evaluation dimensions

- Task success rate and constraint-violation rate.
- Logical consistency of symbolic decisions.
- Propagation of perception errors into symbolic reasoning.
- Distribution shift and compositional generalization.
- End-to-end, reasoning, and planning latency.
- Onboard computation, memory, and energy/resource overhead.
- Interpretability evidence, not only qualitative claims.
- Runtime-monitoring coverage and missed-violation behavior.
- Evidence differences among simulation, hardware-in-the-loop, and real flight.

## Comparability rules

- Different papers may use different simulators, scenarios, metrics, and
  hardware; results may not be directly comparable.
- Do not draw a numerical leaderboard without a controlled, documented
  comparison.
- Do not fill in fictional results when data are unavailable.

## Maturity state

- No benchmark has been implemented or executed in this initialization.
- The benchmark plan should be revisited after full-text review identifies a
  comparable set of tasks and metrics.
