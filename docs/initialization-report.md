# Initialization report

Generated manually for the initialization, not by a build script.

## Environment

- Working directory: project root.
- Git: initialized locally; no commit, push, remote, or global configuration
  changes were made.
- Python: project targets Python 3.11+; local checks should use `py -3.14`
  because the default `python` in this environment resolves to Python 3.10.

## Seed verification

Seven arXiv entries were inspected at metadata/abstract level on 2026-09-20:

- 2501.02341
- 2506.08045
- 2609.19961
- 2607.02277
- 2510.22204
- 2012.05876
- 1805.10872

## Known conflicts and provenance

- `2607.02277` has a metadata conflict: the arXiv `Comments` field says
  “Accepted to the IROS 2026”, while the `Journal reference` field points to
  FSE/PACMPL and DOI `10.1145/3808153`. It is kept as `metadata_status=conflict`.
- `2510.22204` is withdrawn and points to `2607.02277`. Both records share
  `work_id=work-neurosymland` and are not counted as separate core methods.

## Not completed

- No systematic database search beyond the seed set.
- No full-text review; all current reading states are `abstract_reviewed`.
- No core UAV method is yet `included`.
- No LaTeX compilation was performed.
- Author, affiliation, contact, GitHub owner/repo, target venue, and license are
  not yet provided.
