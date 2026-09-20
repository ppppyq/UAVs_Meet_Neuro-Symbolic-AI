# Contributing

This repository is a literature-review knowledge base. Contributions should
preserve evidence provenance and avoid fabricating metadata.

## Data changes

1. Add or update records in `data/papers.json`.
2. Add any new taxonomy tag to `data/taxonomy.json`.
3. Record actually performed searches in `data/search-log.json`.
4. Keep `human_reviewed` false unless a human reviewer explicitly updates it.
5. Do not mark `fulltext_reviewed` unless the full text was actually read.
6. Run:

```powershell
python scripts/manage.py validate
python -m unittest discover -s tests -v
python scripts/manage.py build
python scripts/manage.py check
```

## Evidence rules

- Prefer original paper pages, publishers, proceedings pages, and official
  author repositories.
- Record the source URL, version, and section/page location for technical
  judgments.
- Use `null` or `unknown` for unconfirmed fields.
- Do not turn “code not found” into “authors did not release code”.
- Do not mix simulation, hardware-in-the-loop, and real-flight evidence.

## Generated files

Do not hand-edit the generated blocks in README files, `paper/references.bib`,
or `site/`. Regenerate them with `scripts/manage.py build`.

## Suggestions

For a paper suggestion, open an issue using the paper-suggestion template.
Include a canonical URL and the evidence that supports the suggestion.
