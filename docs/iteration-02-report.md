# Iteration 02 report

Date: 2026-09-20

This iteration continued from the existing repository; it did not re-initialize
the project and did not commit, push, reset, reinitialize, or rename the
branch. Uncommitted user changes were preserved.

## What changed

### CI and maintenance tooling

- `.github/workflows/checks.yml` no longer uses `cache: pip`, because that
  cache setting caused the earlier `Post Set up Python` failure.
- Python matrix changed to `3.11` and `3.13`.
- `scripts/manage.py` now implements:
  - structured `taxonomy_tags` by axis;
  - structured `evidence_items` plus legacy `evidence_legacy`;
  - explicit `bibliography_type`;
  - `metadata_conflict_scope`;
  - stricter validation for included records, URLs, dates, cross-axis tags,
    full-text evidence, and metadata conflicts;
  - `check --tracked-only` for README/BibTeX/evidence-matrix without requiring
    `site/`;
  - full generated-output comparison including static site files;
  - BibTeX selection from `bibliography_type` rather than `record_type` or
    venue keywords;
  - generated website injection of paper, taxonomy, project, and note data.

### Data and evidence

- `project.json` now records version `0.2.0` and data schema `0.2.0`, with
  author `Yuqi Ping`, affiliation `Harbin Institute of Technology, Shenzhen`,
  GitHub repository, and MIT license. Contact email and target venue remain
  `null`.
- `data/taxonomy.json` has `schema_version: 0.2.0`.
- `data/papers.json` was migrated and then updated from full-text review:
  - `p-2609.19961` is now `record_type=position` and
    `reading_status=fulltext_reviewed`. It is an architecture/use-case article
    with no standalone quantitative benchmark, HIL, or real-flight validation.
  - `p-2607.02277` is now `reading_status=fulltext_reviewed` and has the
    verified code URL `https://github.com/Janus117/NeuroSymbolicLand`. Its
    neural/symbolic/coupling, summary, limitations, and full-text evidence were
    updated. It reports 61 successful assessments out of 72 simulated scenarios
    and 100 hardware-in-the-loop profiling trials, with no real-flight
    validation. Venue/DOI metadata remains in conflict.
  - `p-2510.22204` remains withdrawn and shares `work_id=work-neurosymland`.
  - `p-2501.02341` was corrected to `abstract_reviewed` because its full text
    was not re-read in this iteration.
- `data/search-log.json` now records the actual full-text resource accesses and
  the honest status of bounded candidate discovery: two direct UAV candidates
  are currently under review, not a completed 6-12 candidate search.

### Documentation and notes

- Added full-text reading notes:
  - `notes/papers/p-2609.19961.md`
  - `notes/papers/p-2607.02277.md`
- Added `docs/positioning.md` with three testable contribution hypotheses.
- Updated `docs/related-work-comparison.md` to separate "full text reviewed and
  not found" from "unconfirmed".
- Added this report.

### Website

- Filters are generated from `TAXONOMY_DATA_JSON` instead of hardcoded tag
  arrays.
- The static and no-JS tables show screening, metadata, reading, version and
  conflict hints, evidence links, and note links when note files exist.
- Project author/repository/license information is generated from
  `project.json`.
- Mermaid source blocks are loaded from `assets/figures/*.mmd`; the page does
  not claim static SVG rendering.

### Paper

- Removed `\nocite{*}`.
- Added actual `\cite` keys only where evidence exists.
- Updated all section files from the full-text findings.
- Regenerated `paper/references.bib` from the data schema.
- Compiled `paper/main.pdf` with `pdflatex` and `bibtex`; the final log has no
  undefined references.

## Verification performed

Validation, tests, and generated-output consistency checks completed successfully.

Result:

- Validation passed with `records=7 candidates=2 fulltext_reviewed=2
  core_methods=0 migration_pending=1`.
- Test suite passed: 36 tests.
- Tracked-only and full generated-output checks passed.
- Build was repeated and `check` remained in sync.

## Not done

- No new database search was executed beyond the seed set and full-text reads.
- The bounded candidate target of roughly 6-12 is not yet reached.
- No record was promoted to `included`.
- The `p-2607.02277` venue/DOI conflict remains unresolved.
- No commit, push, deploy, or branch reset was performed.
