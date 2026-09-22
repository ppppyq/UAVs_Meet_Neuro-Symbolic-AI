import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import manage  # noqa: E402


def sample_record(**overrides):
    record = {
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
        "taxonomy_tags": {
            "functional_position": ["reasoning"],
            "integration_direction": ["neural_to_symbolic"],
        },
        "taxonomy_migration_pending": [],
        "uav_evidence": ["simulation"],
        "summary": "Summary with <html> & | characters.",
        "limitations": "Limited.",
        "evidence_legacy": "Example page.",
        "evidence_items": [
            {
                "source_url": "https://example.org/paper",
                "source_kind": "abstract",
                "source_version": "arxiv-abstract",
                "locator": None,
                "supports_fields": ["metadata"],
                "claim": "Example page inspected.",
                "attribution": "reviewer_synthesis",
                "accessed_at": "2026-09-20",
            }
        ],
        "checked_at": "2026-09-20",
        "bibliography_type": "misc",
        "metadata_conflict_scope": [],
    }
    record.update(overrides)
    return record


class GenerationTests(unittest.TestCase):
    def test_markdown_escape(self):
        self.assertEqual(manage.markdown_escape("a|b\\c\nd"), "a\\|b\\\\c d")

    def test_bibtex_escape(self):
        self.assertEqual(manage.bibtex_escape("a&b_c%d#e{f}"), r"a\&b\_c\%d\#e\{f\}")

    def test_bibtex_key_is_sanitized(self):
        self.assertEqual(manage.bibtex_key({"id": "p-2501.02341"}), "p_2501_02341")

    def test_paper_table_html_escapes_text(self):
        html_text = manage.paper_table_html([sample_record()])
        self.assertIn("A &amp; B", html_text)
        self.assertIn("&lt;D&gt;", html_text)
        self.assertNotIn("A & B | C <D>", html_text)

    def test_json_for_script_escapes_closing_script(self):
        text = manage.json_for_script({"s": "</script><script>alert(1)</script>"})
        self.assertNotIn("</script><script>", text)
        self.assertIn("<\\/script>", text)

    def test_foundations_markdown_contains_book_and_workshop(self):
        text = manage.foundations_markdown("en")
        self.assertIn("Neurosymbolic AI: Foundations and Applications", text)
        self.assertIn("ICRA'25 Workshop", text)
        self.assertIn("not counted as UAV paper records", text)

    def test_foundations_html_contains_links_and_headings(self):
        text = manage.foundations_html()
        self.assertIn("Foundational papers", text)
        self.assertIn("Books and edited collections", text)
        self.assertIn("Workshops and community resources", text)
        self.assertIn("https://doi.org/10.1002/9781394302406", text)
        self.assertIn("https://sairlab.org/icra25/", text)

    def test_render_bibtex_excludes_withdrawn(self):
        records = [
            sample_record(id="p-verified", work_id="work-a", metadata_status="verified"),
            sample_record(
                id="p-withdrawn",
                work_id="work-b",
                publication_status="withdrawn",
            ),
        ]
        bib = manage.render_bibtex(records)
        self.assertIn("p_verified", bib)
        self.assertNotIn("p_withdrawn", bib)

    def test_bibtex_type_is_explicit_not_inferred_from_method_or_neurips(self):
        records = [
            sample_record(
                id="p-misc",
                work_id="work-a",
                record_type="method",
                venue="Advances in Neural Information Processing Systems 31 (NeurIPS 2018)",
                bibliography_type="misc",
            ),
            sample_record(
                id="p-article",
                work_id="work-b",
                arxiv_id="2601.00002",
                record_type="survey",
                publication_status="published",
                venue="Information Fusion",
                bibliography_type="article",
            ),
        ]
        bib = manage.render_bibtex(records)
        self.assertIn("@misc{p_misc", bib)
        self.assertNotIn("@inproceedings{p_misc", bib)
        self.assertIn("@article{p_article", bib)

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

    def test_bilingual_readmes_follow_six_part_structure_and_keep_all_records(self):
        papers = manage.load_json(manage.PAPERS_PATH)
        categories = manage.taxonomy_display_categories()
        for language, source in (("en", manage.README_EN_PATH), ("zh", manage.README_ZH_PATH)):
            with self.subTest(language=language), tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp) / source.name
                manage.generate_readme(papers, source, target, language)
                text = target.read_text(encoding="utf-8")
                numbered_headings = re.findall(r"^## (\d+)\. (.+)$", text, re.MULTILINE)
                self.assertEqual([number for number, _ in numbered_headings], [str(i) for i in range(1, 7)])
                self.assertEqual([title for _, title in numbered_headings[1:]], [manage.category_name(category, language) for category in categories])
                navigation = text.split(manage.README_NAV_MARKER_START)[1].split(manage.README_NAV_MARKER_END)[0]
                anchors = re.findall(r"\]\(#([^)]+)\)", navigation)
                self.assertEqual(anchors, ["foundations"] + ["theme-" + category["id"] for category in categories])
                for anchor in anchors:
                    self.assertEqual(text.count(f'<a id="{anchor}"></a>'), 1)
                foundations = text.split(manage.FOUNDATIONS_MARKER_START)[1].split(manage.FOUNDATIONS_MARKER_END)[0]
                themes = text.split(manage.RESEARCH_THEMES_MARKER_START)[1].split(manage.RESEARCH_THEMES_MARKER_END)[0]
                self.assertLess(text.index(manage.FOUNDATIONS_MARKER_START), text.index(manage.RESEARCH_THEMES_MARKER_START))
                for record in papers:
                    title = manage.markdown_escape(record["title"])
                    self.assertIn(title, themes if record.get("primary_category") else foundations)
                self.assertNotIn("Surveys, Foundations & System Architectures", themes)
                first = target.read_bytes()
                manage.generate_readme(papers, target, target, language)
                self.assertEqual(first, target.read_bytes())

    def test_no_js_and_js_table_content_are_both_present(self):
        papers = [sample_record()]
        html_table = manage.paper_table_html(papers)
        with tempfile.TemporaryDirectory() as tmp:
            manage.generate_site(papers, Path(tmp))
            rendered = (Path(tmp) / "papers.html").read_text(encoding="utf-8")
        self.assertIn("<table>", html_table)
        self.assertIn("paper-card", rendered)
        self.assertIn("status-pill candidate", rendered)
        self.assertIn("abstract_reviewed", rendered)
        self.assertIn("candidate", rendered)
        self.assertIn("A &amp; B", rendered)
        self.assertIn("__PAPER_DATA__", rendered)

    def test_project_config_is_reflected_in_site(self):
        papers = [sample_record()]
        project = {
            "project_name": "Test Project",
            "authors": ["Yuqi Ping"],
            "affiliations": ["Harbin Institute of Technology, Shenzhen"],
            "github_url": "https://github.com/ppppyq/UAVs_Meet_Neuro-Symbolic-AI",
            "license": "MIT",
            "status": "manuscript-in-preparation",
        }
        with tempfile.TemporaryDirectory() as tmp:
            project_path = Path(tmp) / "project.json"
            project_path.write_text(json.dumps(project), encoding="utf-8")
            out = Path(tmp) / "site"
            with mock.patch.object(manage, "PROJECT_PATH", project_path):
                manage.generate_site(papers, out)
            rendered = (out / "about.html").read_text(encoding="utf-8")
        self.assertIn("Yuqi Ping", rendered)
        self.assertIn("Harbin Institute of Technology, Shenzhen", rendered)
        self.assertIn("MIT", rendered)

    def test_pages_separate_content_and_category_links_work_without_javascript(self):
        papers = manage.load_json(manage.PAPERS_PATH)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manage.generate_site(papers, root)
            home = (root / "index.html").read_text(encoding="utf-8")
            self.assertNotIn('class="paper-card"', home)
            self.assertNotIn('id="foundations"', home)
            self.assertNotIn('id="framework"', home)
            self.assertIn('href="themes.html"', home)
            themes = (root / "themes.html").read_text(encoding="utf-8")
            for category in manage.taxonomy_display_categories():
                filename = "theme-" + category["id"] + ".html"
                self.assertIn('href="' + filename + '"', themes)
                self.assertTrue((root / filename).exists())
            errors = []
            manage.check_local_html_links(root, errors)
            self.assertEqual(errors, [])
            for slug in ("themes", "papers", "foundations", "about"):
                content = (root / (slug + ".html")).read_text(encoding="utf-8")
                self.assertNotIn("{{", content)

    def test_main_menu_has_foundations_and_five_direct_theme_links(self):
        papers = manage.load_json(manage.PAPERS_PATH)
        categories = manage.taxonomy_display_categories()
        menu_routes = ["foundations"] + ["theme-" + category["id"] for category in categories]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manage.generate_site(papers, root)
            for path in root.glob("*.html"):
                content = path.read_text(encoding="utf-8")
                menu = content.split('<div class="nav-links" id="page-links">', 1)[1].split('</div>', 1)[0]
                self.assertEqual(menu.count('<a '), 6)
                for route in menu_routes:
                    self.assertIn('href="' + route + '.html"', menu)
                if path.stem in menu_routes:
                    self.assertIn('href="' + path.name + '" aria-current="page"', menu)
                    self.assertEqual(menu.count('aria-current="page"'), 1)
                else:
                    self.assertNotIn('aria-current="page"', menu)

    def test_retired_framework_is_removed_on_incremental_build(self):
        papers = manage.load_json(manage.PAPERS_PATH)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "framework.html").write_text("Old generated framework page", encoding="utf-8")
            (root / "keep.txt").write_text("Unrelated file", encoding="utf-8")
            manage.generate_site(papers, root)
            self.assertFalse((root / "framework.html").exists())
            self.assertTrue((root / "keep.txt").exists())
            for path in root.glob("*.html"):
                content = path.read_text(encoding="utf-8")
                for retired in ("framework.html", "Proposed framework", "Editable Mermaid", "assets/figures/", "mermaid-source"):
                    self.assertNotIn(retired, content)

    def test_theme_page_includes_primary_and_secondary_assignments_only(self):
        categories = manage.taxonomy_display_categories()
        first, second = categories[0]["id"], categories[1]["id"]
        papers = [
            sample_record(id="primary", title="Primary match", primary_category=first),
            sample_record(id="secondary", title="Secondary match", primary_category=second, secondary_categories=[first]),
            sample_record(id="unrelated", title="Unrelated record", primary_category=second),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            manage.generate_site(papers, Path(tmp))
            text = (Path(tmp) / ("theme-" + first + ".html")).read_text(encoding="utf-8")
            self.assertIn("Primary match", text)
            self.assertIn("Secondary match", text)
            self.assertNotIn("Unrelated record", text)
            self.assertEqual(text.count('class="paper-card"'), 2)
            self.assertIn("Showing 2 of 2 papers.", text)


class CheckGenerationTests(unittest.TestCase):
    def _write_readme_sources(self, root: Path):
        en = (
            "<!-- BEGIN GENERATED:README-NAV -->\n"
            "old\n"
            "<!-- END GENERATED:README-NAV -->\n"
            "<!-- BEGIN GENERATED:OVERVIEW -->\n"
            "old\n"
            "<!-- END GENERATED:OVERVIEW -->\n"
            "<!-- BEGIN GENERATED:RESEARCH-THEMES -->\n"
            "old\n"
            "<!-- END GENERATED:RESEARCH-THEMES -->\n"
            "<!-- BEGIN GENERATED:FOUNDATIONS -->\n"
            "old\n"
            "<!-- END GENERATED:FOUNDATIONS -->\n"
        )
        zh = en
        (root / "README.md").write_text(en, encoding="utf-8")
        (root / "README.zh-CN.md").write_text(zh, encoding="utf-8")
        (root / "docs").mkdir(parents=True, exist_ok=True)
        (root / "docs" / "evidence-matrix.md").write_text(
            "<!-- BEGIN GENERATED:EVIDENCE-MATRIX -->\n"
            "old\n"
            "<!-- END GENERATED:EVIDENCE-MATRIX -->\n",
            encoding="utf-8",
        )
        (root / "docs" / "paper-index.md").write_text(
            "<!-- BEGIN GENERATED:PAPER-INDEX -->\n"
            "old\n"
            "<!-- END GENERATED:PAPER-INDEX -->\n",
            encoding="utf-8",
        )
        (root / "docs" / "category-coverage.md").write_text(
            "<!-- BEGIN GENERATED:CATEGORY-COVERAGE -->\n"
            "old\n"
            "<!-- END GENERATED:CATEGORY-COVERAGE -->\n",
            encoding="utf-8",
        )

    def _make_tracked_fixture(self, records):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        self._write_readme_sources(root)
        (root / "paper").mkdir(parents=True, exist_ok=True)
        papers_path = root / "data" / "papers.json"
        taxonomy_path = root / "data" / "taxonomy.json"
        foundations_path = root / "data" / "foundational-resources.json"
        papers_path.parent.mkdir(parents=True, exist_ok=True)
        papers_path.write_text(json.dumps(records), encoding="utf-8")
        taxonomy_path.write_text(json.dumps(manage.load_json(manage.TAXONOMY_PATH)), encoding="utf-8")
        foundations_path.write_text(
            json.dumps(manage.load_json(manage.FOUNDATIONS_PATH)), encoding="utf-8"
        )
        return root, papers_path, taxonomy_path, foundations_path

    def test_check_tracked_only_works_without_site(self):
        records = [sample_record()]
        root, papers_path, taxonomy_path, foundations_path = self._make_tracked_fixture(records)
        readme_en = root / "README.md"
        readme_zh = root / "README.zh-CN.md"
        bib = root / "paper" / "references.bib"
        evidence = root / "docs" / "evidence-matrix.md"
        paper_index = root / "docs" / "paper-index.md"
        category_coverage = root / "docs" / "category-coverage.md"
        foundations_doc = root / "docs" / "foundations.md"
        with (
            mock.patch.object(manage, "ROOT", root),
            mock.patch.object(manage, "PAPERS_PATH", papers_path),
            mock.patch.object(manage, "TAXONOMY_PATH", taxonomy_path),
            mock.patch.object(manage, "README_EN_PATH", readme_en),
            mock.patch.object(manage, "README_ZH_PATH", readme_zh),
            mock.patch.object(manage, "BIB_PATH", bib),
            mock.patch.object(manage, "EVIDENCE_MATRIX_PATH", evidence),
            mock.patch.object(manage, "PAPER_INDEX_PATH", paper_index),
            mock.patch.object(manage, "CATEGORY_COVERAGE_PATH", category_coverage),
            mock.patch.object(manage, "FOUNDATIONS_PATH", foundations_path),
            mock.patch.object(manage, "FOUNDATIONS_DOC_PATH", foundations_doc),
        ):
            manage.generate_tracked(records, root)
            ok, errors = manage.compare_tracked()
        self.assertTrue(ok, errors)
        self.assertFalse((root / "site").exists())

    def test_data_changed_without_regeneration_makes_check_fail(self):
        records = [sample_record()]
        root, papers_path, taxonomy_path, foundations_path = self._make_tracked_fixture(records)
        readme_en = root / "README.md"
        readme_zh = root / "README.zh-CN.md"
        bib = root / "paper" / "references.bib"
        evidence = root / "docs" / "evidence-matrix.md"
        paper_index = root / "docs" / "paper-index.md"
        category_coverage = root / "docs" / "category-coverage.md"
        foundations_doc = root / "docs" / "foundations.md"
        with (
            mock.patch.object(manage, "ROOT", root),
            mock.patch.object(manage, "PAPERS_PATH", papers_path),
            mock.patch.object(manage, "TAXONOMY_PATH", taxonomy_path),
            mock.patch.object(manage, "README_EN_PATH", readme_en),
            mock.patch.object(manage, "README_ZH_PATH", readme_zh),
            mock.patch.object(manage, "BIB_PATH", bib),
            mock.patch.object(manage, "EVIDENCE_MATRIX_PATH", evidence),
            mock.patch.object(manage, "PAPER_INDEX_PATH", paper_index),
            mock.patch.object(manage, "CATEGORY_COVERAGE_PATH", category_coverage),
            mock.patch.object(manage, "FOUNDATIONS_PATH", foundations_path),
            mock.patch.object(manage, "FOUNDATIONS_DOC_PATH", foundations_doc),
        ):
            manage.generate_tracked(records, root)
            changed = json.loads(papers_path.read_text(encoding="utf-8"))
            changed[0]["title"] = "Changed title"
            papers_path.write_text(json.dumps(changed), encoding="utf-8")
            ok, errors = manage.compare_tracked()
        self.assertFalse(ok)
        self.assertTrue(any("out of sync" in error for error in errors))

    def test_full_check_does_not_modify_files_and_includes_new_static_files(self):
        records = [sample_record()]
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        self._write_readme_sources(root)
        (root / "paper").mkdir(parents=True, exist_ok=True)
        papers_path = root / "data" / "papers.json"
        taxonomy_path = root / "data" / "taxonomy.json"
        foundations_path = root / "data" / "foundational-resources.json"
        project_path = root / "project.json"
        website_dir = root / "website"
        site_dir = root / "site"
        papers_path.parent.mkdir(parents=True, exist_ok=True)
        papers_path.write_text(json.dumps(records), encoding="utf-8")
        taxonomy_path.write_text(json.dumps(manage.load_json(manage.TAXONOMY_PATH)), encoding="utf-8")
        foundations_path.write_text(
            json.dumps(manage.load_json(manage.FOUNDATIONS_PATH)), encoding="utf-8"
        )
        project_path.write_text(json.dumps(manage.load_json(manage.PROJECT_PATH)), encoding="utf-8")
        (website_dir / "static").mkdir(parents=True, exist_ok=True)
        shutil.copytree(manage.WEBSITE_DIR / "pages", website_dir / "pages")
        shutil.copytree(manage.WEBSITE_DIR / "partials", website_dir / "partials")
        (website_dir / "template.html").write_text(
            "{{PAGE_CONTENT}}{{NAVIGATION_HTML}}"
            "{{PAPER_DATA_JSON}}{{TAXONOMY_DATA_JSON}}{{PROJECT_DATA_JSON}}{{NOTES_AVAILABLE_JSON}}",
            encoding="utf-8",
        )
        (website_dir / "static" / "app.js").write_text("// app", encoding="utf-8")
        (website_dir / "static" / "extra.css").write_text("/* extra */", encoding="utf-8")

        readme_en = root / "README.md"
        readme_zh = root / "README.zh-CN.md"
        bib = root / "paper" / "references.bib"
        evidence = root / "docs" / "evidence-matrix.md"
        paper_index = root / "docs" / "paper-index.md"
        category_coverage = root / "docs" / "category-coverage.md"
        foundations_doc = root / "docs" / "foundations.md"

        def snapshot():
            return {
                str(p.relative_to(root)): p.read_bytes()
                for p in sorted(root.rglob("*"))
                if p.is_file()
            }

        with (
            mock.patch.object(manage, "ROOT", root),
            mock.patch.object(manage, "PAPERS_PATH", papers_path),
            mock.patch.object(manage, "TAXONOMY_PATH", taxonomy_path),
            mock.patch.object(manage, "PROJECT_PATH", project_path),
            mock.patch.object(manage, "WEBSITE_DIR", website_dir),
            mock.patch.object(manage, "SITE_DIR", site_dir),
            mock.patch.object(manage, "README_EN_PATH", readme_en),
            mock.patch.object(manage, "README_ZH_PATH", readme_zh),
            mock.patch.object(manage, "BIB_PATH", bib),
            mock.patch.object(manage, "EVIDENCE_MATRIX_PATH", evidence),
            mock.patch.object(manage, "PAPER_INDEX_PATH", paper_index),
            mock.patch.object(manage, "CATEGORY_COVERAGE_PATH", category_coverage),
            mock.patch.object(manage, "FOUNDATIONS_PATH", foundations_path),
            mock.patch.object(manage, "FOUNDATIONS_DOC_PATH", foundations_doc),
        ):
            manage.generate_all(records, root)
            before = snapshot()
            ok, errors = manage.compare_expected_with_actual()
            after = snapshot()

        self.assertTrue(ok, errors)
        self.assertEqual(before, after)
        self.assertTrue((site_dir / "static" / "extra.css").exists())


if __name__ == "__main__":
    unittest.main()
