# Paper note template

Use one file per paper under `notes/papers/`, named with the paper `id`.

```yaml
id: null
title: null
reading_depth: unread # unread | abstract_reviewed | fulltext_reviewed
reviewer: TODO
date: null
```

## 1. Neural part

What is the neural/learning component? What inputs does it consume and what
capability does it learn?

## 2. Symbolic part

What explicit knowledge representation, logic, rules, program, or constraint
mechanism is used? What are its semantics?

## 3. Coupling

How do the neural and symbolic components interact? Which direction(s) are
documented, and when does coupling occur (training time, runtime, or both)?

## 4. UAV validation

What UAV scenario, simulator, hardware-in-the-loop setup, or real-flight
evidence is reported? Keep evidence categories separate.

## 5. Limitations

Which conclusions are still limited by assumptions, scenario coverage, metrics,
or unverified metadata?

## 6. Source and evidence

List the exact URL, version, and section/page location for each important
technical judgment.
