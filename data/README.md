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
- `evidence_legacy`: human-readable evidence summary kept for provenance.
- `evidence_items`: structured source entries with `source_url`, `source_kind`,
  `source_version`, `locator`, `supports_fields`, `claim`, `attribution`, and
  `accessed_at`.
- `checked_at`: real access date, or `null` if not checked.
- `taxonomy_tags`: object keyed by taxonomy axis ID. Each value is an array of
  tag IDs defined for that axis.
- `taxonomy_migration_pending`: unresolved legacy-tag migrations with a reason.
- `bibliography_type`: `article`, `inproceedings`, `misc`, `unpublished`, or
  `other`. BibTeX generation uses this explicit field rather than inferring
  type from `record_type` or venue keywords.
- `metadata_conflict_scope`: non-empty when `metadata_status` is `conflict`;
  otherwise `null` or `[]`.

### Display-category fields

- `primary_category`: one `display_categories` ID from `taxonomy.json`, or
  `null` for auxiliary records.
- `secondary_categories`: zero or more additional `display_categories` IDs,
  deduplicated and never containing the primary category.
- `classification_rationale`: written reason for the assignment.
- `classification_evidence_refs`: source URLs or locator references used for
  the assignment.
- `classification_status`: `provisional` or `reviewed`.

## Counting rules

Only a record that is all of the following counts as a core UAV method:

- `screening_status` is `included`;
- `relevance` is `direct_uav`;
- `record_type` is `method`;
- `publication_status` is not `withdrawn`;
- the record has neural, symbolic, coupling, and evidence information.

Different versions of the same `work_id` are counted once.

## Other files

- `taxonomy.json`: proposed multi-axis taxonomy plus five reader-facing
  `display_categories`.
- `reference-sources.json`: reference repositories, pages, and their uses. They
  are not research-paper records.
- `search-log.json`: searches that were actually performed, with limitations.
