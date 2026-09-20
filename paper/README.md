# Paper skeleton

This directory contains a generic LaTeX skeleton for the working paper. It is
not tied to a proprietary publisher template and does not contain invented
author or submission metadata.

Files:

- `main.tex`: top-level article document with modular section inputs.
- `references.bib`: generated from verified records in `data/papers.json` by
  `scripts/manage.py build`.
- `sections/`: placeholder section files for the planned outline.

## Compile later

If a TeX environment is available, try:

```powershell
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

No LaTeX compilation was performed during initialization.
