# Literature database

`papers.json` is the single source of truth for paper metadata, screening
state, research-content fields, and taxonomy tags. Generated files are derived
from it and must not be edited as a separate source of truth.

## Record fields

### Basic metadata

- `id`: stable and unique internal ID.
- `work_id`: links different versions or records of the same research work.
- `title`: paper title.
- `authors`: author names in the original order.
- `year`: publication or first-release year.
- `canonical_url`: primary URL for the paper page.
- `arxiv_id`: normalized arXiv identifier without a `v` suffix.
- `doi`: normalized DOI, or `null`.
- `venue`: venue/proceedings information, or `null`.
- `publication_status`: `preprint`, `published`, `withdrawn`, `conflict`, or
  `unknown`.
- `record_type`: `survey`, `dataset`, `benchmark`, `method`, `position`, or
  `other`.
- `code_url`: verified official code URL, or `null`.
- `related_versions`: array of objects with `id` and `relation`.

### Independent status fields

- `metadata_status`: `unverified`, `verified`, or `conflict`.
- `reading_status`: `unread`, `abstract_reviewed`, or `fulltext_reviewed`.
- `human_reviewed`: boolean. Codex must keep this `false`.
- `screening_status`: `candidate`, `included`, or `excluded`.
- `relevance`: `direct_uav`, `transferable`, `related_survey`, or `background`.

### Research-content fields

- `neural_component`
- `symbolic_component`
- `coupling_mechanism`
- `inclusion_rationale`
- `exclusion_reason`
- `taxonomy_tags`: IDs defined in `taxonomy.json`.
- `uav_evidence`: array of `conceptual`, `simulation`,
  `hardware_in_loop`, `real_flight`, `none`, or `unknown`.
- `summary`
- `limitations`
- `evidence`: source URL, version, location, and the judgment it supports.
- `checked_at`: real access date, or `null` if not checked.

## Counting rules

Only a record that is all of the following counts as a core UAV method:

- `screening_status` is `included`;
- `relevance` is `direct_uav`;
- `record_type` is `method`;
- `publication_status` is not `withdrawn`;
- the record has neural, symbolic, coupling, and evidence information.

Different versions of the same `work_id` are counted once.

## Other files

- `taxonomy.json`: proposed multi-axis taxonomy.
- `reference-sources.json`: reference repositories, pages, and their uses. They
  are not research-paper records.
- `search-log.json`: searches that were actually performed, with limitations.
