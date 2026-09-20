import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import manage  # noqa: E402


def sample_records():
    return [
        {
            "id": "p-escape",
            "work_id": "work-escape",
            "title": "A & B | C <D> # _ %",
            "authors": ["Author One", "Author & Two"],
            "year": 2026,
            "canonical_url": "https://example.org/paper?a=1&b=2",
            "arxiv_id": "2601.00001",
            "doi": "10.1000/example",
            "venue": None,
            "publication_status": "preprint",
            "record_type": "method",
            "code_url": None,
            "related_versions": [],
            "metadata_status": "verified",
            "reading_status": "abstract_reviewed",
            "human_reviewed": False,
            "screening_status": "candidate",
            "relevance": "direct_uav",
            "neural_component": "Neural <component>.",
            "symbolic_component": "Symbolic rules.",
            "coupling_mechanism": "Neural output to rules.",
            "inclusion_rationale": "Candidate.",
            "exclusion_reason": None,
            "taxonomy_tags": ["reasoning"],
            "uav_evidence": ["simulation"],
            "summary": "Summary with <html> & | characters.",
            "limitations": "Limited.",
            "evidence": "Example page.",
            "checked_at": "2026-09-20",
        }
    ]


class GenerationTests(unittest.TestCase):
    def test_markdown_escape(self):
        self.assertEqual(manage.markdown_escape("a|b\\c\nd"), "a\\|b\\\\c d")

    def test_bibtex_escape(self):
        self.assertEqual(manage.bibtex_escape("a&b_c%d#e{f}"), r"a\&b\_c\%d\#e\{f\}")

    def test_paper_table_html_escapes_text(self):
        html_text = manage.paper_table_html(sample_records())
        self.assertIn("A &amp; B", html_text)
        self.assertIn("&lt;D&gt;", html_text)
        self.assertNotIn("A & B | C <D>", html_text)

    def test_render_bibtex_excludes_withdrawn_and_conflict(self):
        records = [
            dict(
                sample_records()[0],
                id="p-verified",
                work_id="work-a",
                metadata_status="verified",
            ),
            dict(
                sample_records()[0],
                id="p-withdrawn",
                work_id="work-b",
                publication_status="withdrawn",
            ),
            dict(
                sample_records()[0],
                id="p-conflict",
                work_id="work-c",
                metadata_status="conflict",
            ),
        ]
        bib = manage.render_bibtex(records)
        self.assertIn("p_verified", bib)
        self.assertNotIn("p_withdrawn", bib)
        self.assertNotIn("p_conflict", bib)

    def test_bibtex_key_is_sanitized(self):
        self.assertEqual(manage.bibtex_key({"id": "p-2501.02341"}), "p_2501_02341")

    def test_generate_all_is_deterministic(self):
        papers = manage.load_json(manage.PAPERS_PATH)
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            first_root = Path(first)
            second_root = Path(second)
            manage.generate_all(papers, first_root)
            manage.generate_all(papers, second_root)
            first_files = sorted(p.relative_to(first_root) for p in first_root.rglob("*") if p.is_file())
            second_files = sorted(p.relative_to(second_root) for p in second_root.rglob("*") if p.is_file())
            self.assertEqual(first_files, second_files)
            for relative in first_files:
                self.assertEqual(
                    (first_root / relative).read_bytes(),
                    (second_root / relative).read_bytes(),
                )

    def test_generate_all_to_temp_does_not_modify_project_files(self):
        before_readme = manage.README_EN_PATH.read_bytes()
        before_bib = manage.BIB_PATH.read_bytes()
        papers = manage.load_json(manage.PAPERS_PATH)
        with tempfile.TemporaryDirectory() as tmp:
            manage.generate_all(papers, Path(tmp))
        self.assertEqual(manage.README_EN_PATH.read_bytes(), before_readme)
        self.assertEqual(manage.BIB_PATH.read_bytes(), before_bib)


if __name__ == "__main__":
    unittest.main()
