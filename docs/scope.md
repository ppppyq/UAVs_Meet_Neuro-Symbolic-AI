# Scope and conceptual boundaries

## Working research question

How can neural learning and explicit symbolic representations, reasoning, and
constraints be integrated to support trustworthy UAV autonomy?

The focus is not merely “UAVs that use AI”. For each candidate method, ask:

- What inputs and capabilities does the neural component handle or learn?
- What knowledge does the symbolic component represent, and what is its
  explicit semantics?
- How do the neural and symbolic components interact?
- How does that interaction affect perception, reasoning, planning, execution,
  or assurance?
- What UAV-scenario evidence does the literature provide?
- What experiments or formal assumptions support claims about safety,
  interpretability, and generalization?

## Inclusion threshold for core methods

A candidate method must have traceable evidence for all of the following:

1. a neural-learning component;
2. an explicit symbolic representation, logic, rule set, program, or
   semantically meaningful constraint mechanism;
3. a functional coupling between neural and symbolic components that affects
   learning or inference;
4. a stated relationship to a UAV problem and a described validation scope.

If evidence is missing or insufficient, keep the record as `candidate`,
`background`, or `excluded` and record the reason.

## Explicit boundaries

1. Using an LLM, VLM, VLA, or agent does **not** automatically imply
   neuro-symbolic AI.
2. Using a knowledge graph, scene graph, or semantic map does **not**
   automatically imply neuro-symbolic reasoning.
3. Using MPC, CBF, rule constraints, formal verification, or safety filters does
   **not** automatically constitute a neuro-symbolic system. The record must
   explain the substantive coupling to neural learning.
4. Pure symbolic UAV planning may serve as background or baseline, but it is not
   a core neuro-symbolic method.
5. General robotics or general neuro-symbolic methods may be transferable
   foundations, but they must not be presented as already validated on UAVs.
6. Conceptual frameworks, simulation experiments, hardware-in-the-loop, and
   real flight must remain distinct.
7. Interpretability, constraint satisfaction, runtime monitoring, and formal
   safety guarantees must remain distinct.
8. Bidirectional closed-loop integration is not the only legitimate form;
   one-directional and training-time integration may also qualify if supported
   by evidence.
9. Do not describe LLMs, Agentic AI, Embodied AI, and Neuro-Symbolic AI as
   mutually replacing linear technology generations.
10. Do not claim “first”, “only”, or “uniformly superior” without a systematic,
    evidence-backed search.

## Evidence categories

Keep these categories separate in `uav_evidence`:

- `conceptual`
- `simulation`
- `hardware_in_loop`
- `real_flight`
- `none`
- `unknown`

The absence of a code link is not evidence that code was not released.
