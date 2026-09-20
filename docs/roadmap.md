# Roadmap

## Completed in initialization

- Project structure, AGENTS.md, scope, taxonomy, search protocol, data schema.
- Seven seed arXiv entries verified at metadata/abstract level.
- `validate`, `build`, `check`, `serve`, and optional `check-links` command
  skeleton in `scripts/manage.py`.
- Static site template, tests, and CI workflow.

## Next steps

1. Run full-text review on the two direct UAV candidates.
2. Resolve the NEUROSYMLAND venue conflict from primary sources.
3. Add new papers through `data/papers.json`, then run validation and tests.
4. Expand the bounded seed search only when useful.
5. Fill in author, affiliation, contact, GitHub owner/repo, target venue, and
   license.
6. Compile the LaTeX skeleton if a TeX environment becomes available.
7. Optionally run `python scripts/manage.py check-links` when network access is
   explicitly desired.
