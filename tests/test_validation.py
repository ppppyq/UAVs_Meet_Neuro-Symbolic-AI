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
        "display_categories": [
            {
                "id": "cat_perception",
                "display_order": 1,
                "name": "Perception category",
                "name_zh": "感知类",
                "description": "Perception description.",
                "boundary": "Perception boundary.",
                "subdirections": ["Grounding"],
            },
            {
                "id": "cat_reasoning",
                "display_order": 2,
                "name": "Reasoning category",
                "name_zh": "推理类",
                "description": "Reasoning description.",
                "boundary": "Reasoning boundary.",
                "subdirections": [],
            },
        ],
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
                    },
                    {
                        "id": "ambiguous",
                        "name": "Ambiguous",
                        "zh": "歧义",
                        "definition": "Ambiguous.",
                        "inclusion_exclusion": "Include when applicable.",
                    },
                ],
            },
            {
                "id": "symbolic_mechanism",
                "name": "Symbolic mechanism",
                "tags": [
                    {
                        "id": "logic_rules",
                        "name": "Logic rules",
                        "zh": "逻辑规则",
                        "definition": "Logic rules.",
                        "inclusion_exclusion": "Include when applicable.",
                    },
                    {
                        "id": "ambiguous",
                        "name": "Ambiguous",
                        "zh": "歧义",
                        "definition": "Ambiguous.",
                        "inclusion_exclusion": "Include when applicable.",
                    },
                ],
            },
            {
                "id": "uav_task",
                "name": "UAV task",
                "tags": [
                    {
                        "id": "landing",
                        "name": "Landing",
                        "zh": "着陆",
                        "definition": "Landing.",
                        "inclusion_exclusion": "Include when applicable.",
                    }
                ],
            },
        ],
    }


def abstract_item() -> dict:
    return {
        "source_url": "https://arxiv.org/abs/2601.00001",
        "source_kind": "abstract",
        "source_version": "arxiv-abstract",
        "locator": None,
        "supports_fields": ["metadata"],
        "claim": "Abstract page inspected.",
        "attribution": "reviewer_synthesis",
        "accessed_at": "2026-09-20",
    }


def fulltext_item() -> dict:
    return {
        "source_url": "https://arxiv.org/html/2601.00001v1",
        "source_kind": "fulltext",
        "source_version": "arXiv:2601.00001v1",
        "locator": "Sec. III",
        "supports_fields": ["neural_component", "symbolic_component", "coupling_mechanism"],
        "claim": "Full text inspected.",
        "attribution": "reviewer_synthesis",
        "accessed_at": "2026-09-20",
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
        "taxonomy_tags": {
            "functional_position": ["reasoning"],
            "integration_direction": ["neural_to_symbolic"],
        },
        "taxonomy_migration_pending": [],
        "uav_evidence": ["simulation"],
        "summary": "A summary.",
        "limitations": "A limitation.",
        "evidence_legacy": "Abstract page inspected.",
        "evidence_items": [abstract_item()],
        "checked_at": "2026-09-20",
        "bibliography_type": "misc",
        "metadata_conflict_scope": [],
        "primary_category": None,
        "secondary_categories": [],
        "classification_rationale": "Test classification rationale.",
        "classification_evidence_refs": ["https://arxiv.org/abs/2601.00001"],
        "classification_status": "provisional",
    }
    record.update(overrides)
    return record


def included_record(**overrides) -> dict:
    record = base_record(
        screening_status="included",
        reading_status="fulltext_reviewed",
        relevance="direct_uav",
        record_type="method",
        publication_status="preprint",
        metadata_status="verified",
        inclusion_rationale="Meets inclusion threshold after full-text review.",
        evidence_items=[fulltext_item()],
    )
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

    def test_five_display_categories_are_unique_ordered_and_bilingual(self):
        categories = manage.taxonomy_display_categories()
        ids = [item["id"] for item in categories]
        self.assertEqual(
            ids,
            [
                "perception_world_modeling",
                "reasoning_mission_planning",
                "navigation_control",
                "safety_verification",
                "collaboration_interaction",
            ],
        )
        self.assertEqual([item["display_order"] for item in categories], [1, 2, 3, 4, 5])
        self.assertTrue(all(item["name"].strip() for item in categories))
        self.assertTrue(all(item["name_zh"].strip() for item in categories))

    def test_invalid_primary_category_is_rejected(self):
        ok, errors = self.validate_records([base_record(primary_category="missing")])
        self.assertFalse(ok)
        self.assertTrue(any("primary_category" in error for error in errors))

    def test_duplicate_secondary_category_is_rejected(self):
        ok, errors = self.validate_records(
            [base_record(secondary_categories=["cat_perception", "cat_perception"])]
        )
        self.assertFalse(ok)
        self.assertTrue(any("must not contain duplicates" in error for error in errors))

    def test_primary_category_in_secondary_is_rejected(self):
        ok, errors = self.validate_records(
            [
                base_record(
                    primary_category="cat_perception",
                    secondary_categories=["cat_perception"],
                )
            ]
        )
        self.assertFalse(ok)
        self.assertTrue(any("primary_category must not also appear" in error for error in errors))

    def test_null_primary_with_provisional_status_is_allowed(self):
        ok, errors = self.validate_records(
            [
                base_record(
                    primary_category=None,
                    secondary_categories=[],
                    classification_status="provisional",
                )
            ]
        )
        self.assertTrue(ok, errors)

    def test_foundational_resources_are_valid(self):
        errors = manage.validate_foundational_resources()
        self.assertEqual(errors, [])

    def test_foundational_resources_cover_papers_books_and_workshops(self):
        resources = manage.load_foundational_resources()
        resource_types = {resource["resource_type"] for resource in resources}
        self.assertIn("paper", resource_types)
        self.assertIn("book", resource_types)
        self.assertIn("workshop", resource_types)

    def test_foundational_workshop_without_doi_is_allowed(self):
        resources = manage.load_foundational_resources()
        workshop = next(
            resource for resource in resources if resource["resource_type"] == "workshop"
        )
        self.assertIsNone(workshop["doi"])
        self.assertIsNone(workshop["arxiv_id"])
        self.assertTrue(workshop["url"].startswith("https://"))

    def test_invalid_foundational_resource_type_is_rejected(self):
        resources = manage.load_foundational_resources()
        broken = copy.deepcopy(resources)
        broken[0]["resource_type"] = "not-a-type"
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "foundational-resources.json"
        path.write_text(json.dumps({"resources": broken}), encoding="utf-8")
        with mock.patch.object(manage, "FOUNDATIONS_PATH", path):
            errors = manage.validate_foundational_resources()
        self.assertTrue(any("resource_type" in error for error in errors))

    def test_architecture_article_is_not_core_method(self):
        record = base_record(
            record_type="position",
            screening_status="candidate",
            relevance="direct_uav",
        )
        self.assertEqual(manage.count_core_methods([record]), 0)

    def test_cross_theme_secondary_does_not_double_unique_study_count(self):
        first = base_record(
            id="p-one",
            work_id="work-same",
            primary_category="cat_perception",
            secondary_categories=["cat_reasoning"],
        )
        second = base_record(
            id="p-two",
            work_id="work-same",
            arxiv_id="2601.00002",
            primary_category="cat_reasoning",
            secondary_categories=["cat_perception"],
        )
        self.assertEqual(manage.distinct_non_withdrawn_work_ids([first, second]), 1)

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

    def test_cross_axis_taxonomy_tag_is_rejected(self):
        ok, errors = self.validate_records(
            [base_record(taxonomy_tags={"functional_position": ["neural_to_symbolic"]})]
        )
        self.assertFalse(ok)
        self.assertTrue(any("does not belong to axis" in error for error in errors))

    def test_included_without_fulltext_is_rejected(self):
        record = base_record(
            screening_status="included",
            reading_status="fulltext_reviewed",
            evidence_items=[abstract_item()],
        )
        ok, errors = self.validate_records([record])
        self.assertFalse(ok)
        self.assertTrue(any("fulltext evidence" in error for error in errors))

    def test_invalid_types_missing_url_and_dates_are_readable(self):
        record = base_record(
            year="2026",
            canonical_url="not-a-url",
            checked_at="20-09-2026",
            evidence_items=[
                {
                    **abstract_item(),
                    "source_url": None,
                    "accessed_at": "2026/09/20",
                }
            ],
        )
        ok, errors = self.validate_records([record])
        self.assertFalse(ok)
        joined = "\n".join(errors)
        self.assertIn("year must be", joined)
        self.assertIn("canonical_url must be", joined)
        self.assertIn("checked_at must be", joined)
        self.assertIn("accessed_at must be", joined)

    def test_withdrawn_record_cannot_be_included(self):
        record = included_record(publication_status="withdrawn")
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

    def test_related_versions_with_bad_relation_are_rejected(self):
        record = base_record(
            related_versions=[{"id": "p-test", "relation": "not-a-relation"}]
        )
        ok, errors = self.validate_records([record])
        self.assertFalse(ok)
        self.assertTrue(any("relation must be one of" in error for error in errors))

    def test_candidate_is_not_counted_as_core_method(self):
        record = base_record(screening_status="candidate")
        self.assertEqual(manage.count_core_methods([record]), 0)

    def test_same_work_id_is_counted_once(self):
        first = included_record(id="p-new", work_id="work-same")
        second = included_record(id="p-other", work_id="work-same", arxiv_id="2601.00002")
        self.assertEqual(manage.count_core_methods([first, second]), 1)

    def test_withdrawn_version_is_not_counted(self):
        first = included_record(id="p-new", work_id="work-same")
        older = included_record(
            id="p-old",
            work_id="work-same",
            arxiv_id="2601.00002",
            publication_status="withdrawn",
            screening_status="excluded",
            exclusion_reason="Withdrawn version.",
            evidence_items=[abstract_item()],
        )
        self.assertEqual(manage.count_core_methods([first, older]), 1)


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


class MigrationTests(unittest.TestCase):
    def _setup(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        papers_path = root / "papers.json"
        taxonomy_path = root / "taxonomy.json"
        taxonomy_path.write_text(json.dumps(minimal_taxonomy()), encoding="utf-8")
        return papers_path, taxonomy_path

    def test_ambiguous_migration_is_not_guessed(self):
        papers_path, taxonomy_path = self._setup()
        old = base_record()
        old["taxonomy_tags"] = ["reasoning", "ambiguous"]
        old["evidence"] = "Legacy evidence."
        old.pop("evidence_legacy", None)
        old.pop("evidence_items", None)
        old.pop("taxonomy_migration_pending", None)
        old.pop("bibliography_type", None)
        old.pop("metadata_conflict_scope", None)
        papers_path.write_text(json.dumps([old]), encoding="utf-8")

        with mock.patch.object(manage, "PAPERS_PATH", papers_path), mock.patch.object(
            manage, "TAXONOMY_PATH", taxonomy_path
        ):
            result = manage.migrate_data(apply=True)

        self.assertEqual(result["pending_total"], 1)
        migrated = json.loads(papers_path.read_text(encoding="utf-8"))[0]
        self.assertEqual(migrated["taxonomy_tags"], {"functional_position": ["reasoning"]})
        self.assertIn("ambiguous", [item["tag"] for item in migrated["taxonomy_migration_pending"]])

    def test_migration_is_idempotent_and_lossless(self):
        papers_path, taxonomy_path = self._setup()
        old = base_record()
        old["taxonomy_tags"] = ["reasoning", "neural_to_symbolic"]
        old["evidence"] = "Legacy evidence."
        old.pop("evidence_legacy", None)
        old.pop("evidence_items", None)
        old.pop("taxonomy_migration_pending", None)
        old.pop("bibliography_type", None)
        old.pop("metadata_conflict_scope", None)
        papers_path.write_text(json.dumps([old]), encoding="utf-8")

        with mock.patch.object(manage, "PAPERS_PATH", papers_path), mock.patch.object(
            manage, "TAXONOMY_PATH", taxonomy_path
        ):
            manage.migrate_data(apply=True)
            before = papers_path.read_text(encoding="utf-8")
            manage.migrate_data(apply=True)
            after = papers_path.read_text(encoding="utf-8")

        self.assertEqual(before, after)
        migrated = json.loads(before)[0]
        self.assertEqual(migrated["evidence_legacy"], "Legacy evidence.")
        self.assertIn("evidence_items", migrated)
        self.assertIn("bibliography_type", migrated)


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
