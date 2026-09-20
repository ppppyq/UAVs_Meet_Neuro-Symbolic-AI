import copy
import json
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


def minimal_taxonomy() -> dict:
    return {
        "version": "v0.1",
        "status": "proposed",
        "axes": [
            {
                "id": "functional_position",
                "name": "Functional position",
                "tags": [
                    {
                        "id": "reasoning",
                        "name": "Reasoning",
                        "zh": "推理",
                        "definition": "Reasoning.",
                        "inclusion_exclusion": "Include when applicable.",
                    },
                    {
                        "id": "assurance",
                        "name": "Assurance",
                        "zh": "保证",
                        "definition": "Assurance.",
                        "inclusion_exclusion": "Include when applicable.",
                    },
                ],
            },
            {
                "id": "integration_direction",
                "name": "Integration direction",
                "tags": [
                    {
                        "id": "neural_to_symbolic",
                        "name": "Neural to symbolic",
                        "zh": "神经到符号",
                        "definition": "Neural to symbolic.",
                        "inclusion_exclusion": "Include when applicable.",
                    }
                ],
            },
        ],
    }


def base_record(**overrides) -> dict:
    record = {
        "id": "p-test",
        "work_id": "work-test",
        "title": "Test Paper",
        "authors": ["Alice Example"],
        "year": 2026,
        "canonical_url": "https://arxiv.org/abs/2601.00001",
        "arxiv_id": "2601.00001",
        "doi": None,
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
        "neural_component": "A neural network.",
        "symbolic_component": "Explicit logical rules.",
        "coupling_mechanism": "Neural outputs feed logical rules.",
        "inclusion_rationale": "Candidate.",
        "exclusion_reason": None,
        "taxonomy_tags": ["reasoning", "neural_to_symbolic"],
        "uav_evidence": ["simulation"],
        "summary": "A summary.",
        "limitations": "A limitation.",
        "evidence": "arXiv page.",
        "checked_at": "2026-09-20",
    }
    record.update(overrides)
    return record


class ValidationTests(unittest.TestCase):
    def make_data_files(self, records):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        papers_path = root / "papers.json"
        taxonomy_path = root / "taxonomy.json"
        papers_path.write_text(json.dumps(records), encoding="utf-8")
        taxonomy_path.write_text(json.dumps(minimal_taxonomy()), encoding="utf-8")
        return papers_path, taxonomy_path

    def validate_records(self, records):
        papers_path, taxonomy_path = self.make_data_files(records)
        with mock.patch.object(manage, "PAPERS_PATH", papers_path), mock.patch.object(
            manage, "TAXONOMY_PATH", taxonomy_path
        ):
            ok, errors = manage.validate_data()
        return ok, errors

    def test_seed_data_is_valid(self):
        ok, errors = manage.validate_data()
        self.assertTrue(ok, errors)

    def test_empty_library_is_valid_and_has_no_core_methods(self):
        ok, errors = self.validate_records([])
        self.assertTrue(ok, errors)
        self.assertEqual(manage.count_core_methods([]), 0)

    def test_invalid_enum_is_rejected(self):
        ok, errors = self.validate_records([base_record(metadata_status="bogus")])
        self.assertFalse(ok)
        self.assertTrue(any("metadata_status" in error for error in errors))

    def test_duplicate_id_is_rejected(self):
        records = [
            base_record(id="p-same"),
            base_record(id="p-same", arxiv_id="2601.00002", work_id="work-2"),
        ]
        ok, errors = self.validate_records(records)
        self.assertFalse(ok)
        self.assertTrue(any("duplicate id" in error for error in errors))

    def test_duplicate_normalized_arxiv_id_is_rejected(self):
        records = [
            base_record(id="p-one", arxiv_id="2601.00001"),
            base_record(
                id="p-two",
                work_id="work-2",
                arxiv_id="https://arxiv.org/abs/2601.00001v2",
            ),
        ]
        ok, errors = self.validate_records(records)
        self.assertFalse(ok)
        self.assertTrue(any("duplicate normalized arXiv ID" in error for error in errors))

    def test_duplicate_normalized_doi_is_rejected(self):
        records = [
            base_record(id="p-one", doi="10.1000/XYZ"),
            base_record(id="p-two", work_id="work-2", doi="https://doi.org/10.1000/xyz"),
        ]
        ok, errors = self.validate_records(records)
        self.assertFalse(ok)
        self.assertTrue(any("duplicate normalized DOI" in error for error in errors))

    def test_unknown_taxonomy_tag_is_rejected(self):
        ok, errors = self.validate_records([base_record(taxonomy_tags=["not_a_real_tag"])])
        self.assertFalse(ok)
        self.assertTrue(any("unknown taxonomy tag" in error for error in errors))

    def test_included_core_method_requires_evidence(self):
        record = base_record(
            screening_status="included",
            relevance="direct_uav",
            record_type="method",
            evidence=None,
        )
        ok, errors = self.validate_records([record])
        self.assertFalse(ok)
        self.assertTrue(any("requires non-empty evidence" in error for error in errors))

    def test_withdrawn_record_cannot_be_included(self):
        record = base_record(
            screening_status="included",
            publication_status="withdrawn",
        )
        ok, errors = self.validate_records([record])
        self.assertFalse(ok)
        self.assertTrue(any("withdrawn record cannot be included" in error for error in errors))

    def test_related_version_must_exist(self):
        record = base_record(
            related_versions=[{"id": "p-missing", "relation": "supersedes"}]
        )
        ok, errors = self.validate_records([record])
        self.assertFalse(ok)
        self.assertTrue(any("points to missing id" in error for error in errors))

    def test_candidate_is_not_counted_as_core_method(self):
        record = base_record(screening_status="candidate")
        self.assertEqual(manage.count_core_methods([record]), 0)

    def test_duplicate_work_id_is_counted_once(self):
        included = base_record(id="p-new", screening_status="included")
        older = base_record(
            id="p-old",
            work_id=included["work_id"],
            screening_status="included",
            publication_status="withdrawn",
        )
        self.assertEqual(manage.count_core_methods([included, older]), 1)

    def test_related_versions_with_bad_relation_are_rejected(self):
        record = base_record(
            related_versions=[{"id": "p-test", "relation": "not-a-relation"}]
        )
        ok, errors = self.validate_records([record])
        self.assertFalse(ok)
        self.assertTrue(any("relation must be one of" in error for error in errors))


class NormalizationTests(unittest.TestCase):
    def test_arxiv_id_normalization(self):
        self.assertEqual(
            manage.normalize_arxiv_id("https://arxiv.org/abs/2501.02341v2"),
            "2501.02341",
        )
        self.assertEqual(manage.normalize_arxiv_id("arXiv:1805.10872"), "1805.10872")
        self.assertIsNone(manage.normalize_arxiv_id(None))

    def test_doi_normalization(self):
        self.assertEqual(
            manage.normalize_doi("https://doi.org/10.1016/J.INFFUS.2025.103158"),
            "10.1016/j.inffus.2025.103158",
        )
        self.assertEqual(manage.normalize_doi("doi:10.1145/3808153"), "10.1145/3808153")


class MarkerTests(unittest.TestCase):
    def test_missing_marker_is_reported(self):
        with self.assertRaises(manage.ManageError):
            manage.apply_generated_block(
                "no markers",
                manage.OVERVIEW_MARKER_START,
                manage.OVERVIEW_MARKER_END,
                "content",
                "test",
            )

    def test_unpaired_marker_is_reported(self):
        text = f"{manage.OVERVIEW_MARKER_START}\ncontent"
        with self.assertRaises(manage.ManageError):
            manage.apply_generated_block(
                text,
                manage.OVERVIEW_MARKER_START,
                manage.OVERVIEW_MARKER_END,
                "content",
                "test",
            )

    def test_duplicate_marker_is_reported(self):
        text = (
            f"{manage.OVERVIEW_MARKER_START}\n{manage.OVERVIEW_MARKER_END}\n"
            f"{manage.OVERVIEW_MARKER_START}\n{manage.OVERVIEW_MARKER_END}"
        )
        with self.assertRaises(manage.ManageError):
            manage.apply_generated_block(
                text,
                manage.OVERVIEW_MARKER_START,
                manage.OVERVIEW_MARKER_END,
                "content",
                "test",
            )


if __name__ == "__main__":
    unittest.main()
