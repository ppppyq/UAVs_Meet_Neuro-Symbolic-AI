#!/usr/bin/env python3
"""Maintenance commands for the UAV neuro-symbolic review knowledge base.

This script intentionally uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import http.server
import json
import re
import shutil
import socket
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
WEBSITE_DIR = ROOT / "website"
SITE_DIR = ROOT / "site"
PAPER_DIR = ROOT / "paper"
DOCS_DIR = ROOT / "docs"

PAPERS_PATH = DATA_DIR / "papers.json"
TAXONOMY_PATH = DATA_DIR / "taxonomy.json"
FOUNDATIONS_PATH = DATA_DIR / "foundational-resources.json"
PROJECT_PATH = ROOT / "project.json"
README_EN_PATH = ROOT / "README.md"
README_ZH_PATH = ROOT / "README.zh-CN.md"
BIB_PATH = PAPER_DIR / "references.bib"
EVIDENCE_MATRIX_PATH = DOCS_DIR / "evidence-matrix.md"
PAPER_INDEX_PATH = DOCS_DIR / "paper-index.md"
CATEGORY_COVERAGE_PATH = DOCS_DIR / "category-coverage.md"
FOUNDATIONS_DOC_PATH = DOCS_DIR / "foundations.md"

OVERVIEW_MARKER_START = "<!-- BEGIN GENERATED:OVERVIEW -->"
OVERVIEW_MARKER_END = "<!-- END GENERATED:OVERVIEW -->"
PAPER_TABLE_MARKER_START = "<!-- BEGIN GENERATED:PAPER-TABLE -->"
PAPER_TABLE_MARKER_END = "<!-- END GENERATED:PAPER-TABLE -->"
EVIDENCE_MATRIX_MARKER_START = "<!-- BEGIN GENERATED:EVIDENCE-MATRIX -->"
EVIDENCE_MATRIX_MARKER_END = "<!-- END GENERATED:EVIDENCE-MATRIX -->"
RESEARCH_THEMES_MARKER_START = "<!-- BEGIN GENERATED:RESEARCH-THEMES -->"
RESEARCH_THEMES_MARKER_END = "<!-- END GENERATED:RESEARCH-THEMES -->"
PAPER_INDEX_MARKER_START = "<!-- BEGIN GENERATED:PAPER-INDEX -->"
PAPER_INDEX_MARKER_END = "<!-- END GENERATED:PAPER-INDEX -->"
CATEGORY_COVERAGE_MARKER_START = "<!-- BEGIN GENERATED:CATEGORY-COVERAGE -->"
CATEGORY_COVERAGE_MARKER_END = "<!-- END GENERATED:CATEGORY-COVERAGE -->"
FOUNDATIONS_MARKER_START = "<!-- BEGIN GENERATED:FOUNDATIONS -->"
FOUNDATIONS_MARKER_END = "<!-- END GENERATED:FOUNDATIONS -->"

VALID_METADATA_STATUS = {"unverified", "verified", "conflict"}
VALID_READING_STATUS = {"unread", "abstract_reviewed", "fulltext_reviewed"}
VALID_SCREENING_STATUS = {"candidate", "included", "excluded"}
VALID_RELEVANCE = {"direct_uav", "transferable", "related_survey", "background"}
VALID_RECORD_TYPE = {"survey", "dataset", "benchmark", "method", "position", "other"}
VALID_PUBLICATION_STATUS = {"preprint", "published", "withdrawn", "conflict", "unknown"}
VALID_UAV_EVIDENCE = {"conceptual", "simulation", "hardware_in_loop", "real_flight", "none", "unknown"}
VALID_RELATION = {"supersedes", "superseded_by", "earlier_version", "later_version", "same_work", "other"}
VALID_SOURCE_KIND = {"abstract", "fulltext", "publisher", "official_code"}
VALID_ATTRIBUTION = {"author_reported", "reviewer_synthesis", "unverified"}
VALID_BIBLIOGRAPHY_TYPE = {"article", "inproceedings", "misc", "unpublished", "other"}
VALID_CONFLICT_SCOPE = {"title", "identity", "fulltext", "venue", "doi", "publication_status"}
VALID_CLASSIFICATION_STATUS = {"provisional", "reviewed"}
VALID_RESOURCE_TYPE = {"paper", "book", "workshop", "collection"}
VALID_CONTRIBUTOR_ROLE = {"authors", "editors", "organizers"}
VALID_FOUNDATION_VERIFICATION = {"verified", "unverified"}

REQUIRED_FIELDS = {
    "id",
    "work_id",
    "title",
    "authors",
    "year",
    "canonical_url",
    "arxiv_id",
    "doi",
    "venue",
    "publication_status",
    "record_type",
    "code_url",
    "related_versions",
    "metadata_status",
    "reading_status",
    "human_reviewed",
    "screening_status",
    "relevance",
    "neural_component",
    "symbolic_component",
    "coupling_mechanism",
    "inclusion_rationale",
    "exclusion_reason",
    "taxonomy_tags",
    "taxonomy_migration_pending",
    "uav_evidence",
    "summary",
    "limitations",
    "primary_category",
    "secondary_categories",
    "classification_rationale",
    "classification_evidence_refs",
    "classification_status",
    "evidence_legacy",
    "evidence_items",
    "checked_at",
    "bibliography_type",
    "metadata_conflict_scope",
}

WEBSITE_TOKENS = (
    "{{OVERVIEW_HTML}}",
    "{{PAPER_TABLE_HTML}}",
    "{{PROJECT_INFO_HTML}}",
    "{{FIGURE_SOURCES_HTML}}",
    "{{FOUNDATIONS_HTML}}",
    "{{CATEGORY_CARDS_HTML}}",
    "{{PAPER_DATA_JSON}}",
    "{{TAXONOMY_DATA_JSON}}",
    "{{PROJECT_DATA_JSON}}",
    "{{NOTES_AVAILABLE_JSON}}",
)


class ManageError(Exception):
    """Expected user-facing command error."""


def load_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError as exc:
        raise ManageError(f"{path}: invalid JSON: {exc}") from exc
    except OSError as exc:
        raise ManageError(f"{path}: cannot read: {exc}") from exc


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def normalize_arxiv_id(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    text = re.sub(r"^arxiv:", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^https?://arxiv\.org/abs/", "", text, flags=re.IGNORECASE)
    text = re.sub(r"v\d+$", "", text, flags=re.IGNORECASE)
    return text.strip() or None


def normalize_doi(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    text = re.sub(r"^doi:", "", text, flags=re.IGNORECASE)
    if "doi.org/" in text.lower():
        parsed = urllib.parse.urlparse(text if "://" in text else f"https://{text}")
        text = parsed.path.lstrip("/")
    return text.lower() or None


def is_valid_date(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        dt.date.fromisoformat(value)
        return True
    except ValueError:
        return False


def is_http_url(value: Any, *, required: bool = False) -> bool:
    if value is None:
        return not required
    if not isinstance(value, str):
        return False
    if not value and not required:
        return True
    try:
        parsed = urllib.parse.urlparse(value)
    except ValueError:
        return False
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def is_valid_arxiv_id(value: Any) -> bool:
    normalized = normalize_arxiv_id(value)
    return normalized is not None and bool(re.fullmatch(r"\d{4}\.\d{4,5}", normalized))


def is_valid_doi(value: Any) -> bool:
    normalized = normalize_doi(value)
    return normalized is not None and bool(re.fullmatch(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", normalized))


def taxonomy_axis_map() -> tuple[dict[str, list[str]], set[str]]:
    taxonomy = load_json(TAXONOMY_PATH)
    if not isinstance(taxonomy, dict):
        raise ManageError(f"{TAXONOMY_PATH}: root must be an object")
    axes = taxonomy.get("axes")
    if not isinstance(axes, list) or not axes:
        raise ManageError(f"{TAXONOMY_PATH}: missing non-empty axes array")
    result: dict[str, list[str]] = {}
    all_tags: set[str] = set()
    for axis in axes:
        if not isinstance(axis, dict):
            raise ManageError(f"{TAXONOMY_PATH}: axis must be an object")
        axis_id = axis.get("id")
        if not isinstance(axis_id, str) or not axis_id:
            raise ManageError(f"{TAXONOMY_PATH}: axis id is missing")
        if axis_id in result:
            raise ManageError(f"{TAXONOMY_PATH}: duplicate axis id {axis_id}")
        tags = axis.get("tags")
        if not isinstance(tags, list) or not tags:
            raise ManageError(f"{TAXONOMY_PATH}: axis {axis_id} has no tags")
        tag_ids: list[str] = []
        for tag in tags:
            if not isinstance(tag, dict):
                raise ManageError(f"{TAXONOMY_PATH}: tag in {axis_id} must be an object")
            tag_id = tag.get("id")
            if not isinstance(tag_id, str) or not tag_id:
                raise ManageError(f"{TAXONOMY_PATH}: tag id is missing in {axis_id}")
            if tag_id in tag_ids:
                raise ManageError(f"{TAXONOMY_PATH}: duplicate taxonomy tag id {tag_id} in axis {axis_id}")
            tag_ids.append(tag_id)
            all_tags.add(tag_id)
        result[axis_id] = tag_ids
    return result, all_tags


def taxonomy_display_categories() -> list[dict[str, Any]]:
    taxonomy = load_json(TAXONOMY_PATH)
    if not isinstance(taxonomy, dict):
        raise ManageError(f"{TAXONOMY_PATH}: root must be an object")
    categories = taxonomy.get("display_categories")
    if not isinstance(categories, list) or not categories:
        raise ManageError(f"{TAXONOMY_PATH}: missing non-empty display_categories array")
    result: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    seen_orders: set[int] = set()
    for category in categories:
        if not isinstance(category, dict):
            raise ManageError(f"{TAXONOMY_PATH}: display_categories entry must be an object")
        category_id = category.get("id")
        if not isinstance(category_id, str) or not category_id:
            raise ManageError(f"{TAXONOMY_PATH}: display_categories id is missing")
        if category_id in seen_ids:
            raise ManageError(f"{TAXONOMY_PATH}: duplicate display category id {category_id}")
        seen_ids.add(category_id)
        order = category.get("display_order")
        if not isinstance(order, int) or isinstance(order, bool) or order <= 0:
            raise ManageError(f"{TAXONOMY_PATH}: display category {category_id} display_order must be a positive integer")
        if order in seen_orders:
            raise ManageError(f"{TAXONOMY_PATH}: duplicate display category display_order {order}")
        seen_orders.add(order)
        for key in ("name", "name_zh", "description", "boundary"):
            if not isinstance(category.get(key), str) or not category.get(key).strip():
                raise ManageError(f"{TAXONOMY_PATH}: display category {category_id} requires non-empty {key}")
        subdirections = category.get("subdirections", [])
        if not isinstance(subdirections, list) or not all(
            isinstance(item, str) and item.strip() for item in subdirections
        ):
            raise ManageError(
                f"{TAXONOMY_PATH}: display category {category_id} subdirections must be an array of non-empty strings"
            )
        result.append(category)
    result.sort(key=lambda item: item["display_order"])
    return result


def display_category_ids() -> set[str]:
    return {item["id"] for item in taxonomy_display_categories()}


def load_foundational_resources() -> list[dict[str, Any]]:
    data = load_json(FOUNDATIONS_PATH)
    if not isinstance(data, dict):
        raise ManageError(f"{FOUNDATIONS_PATH}: root must be an object")
    resources = data.get("resources")
    if not isinstance(resources, list) or not resources:
        raise ManageError(f"{FOUNDATIONS_PATH}: missing non-empty resources array")
    return resources


def validate_foundational_resources() -> list[str]:
    errors: list[str] = []
    try:
        resources = load_foundational_resources()
    except ManageError as exc:
        return [str(exc)]

    seen_ids: set[str] = set()
    for index, resource in enumerate(resources):
        location = f"resource {index}"
        if not isinstance(resource, dict):
            errors.append(f"{FOUNDATIONS_PATH}: {location}: expected object")
            continue
        location = f"resource {resource.get('id', index)}"
        required = {
            "id",
            "title",
            "resource_type",
            "year",
            "url",
            "arxiv_id",
            "doi",
            "isbn",
            "venue",
            "publisher",
            "contributors",
            "contributor_role",
            "summary",
            "role",
            "verification_status",
            "evidence",
        }
        missing = sorted(required - set(resource))
        if missing:
            errors.append(f"{FOUNDATIONS_PATH}: {location}: missing fields {', '.join(missing)}")

        resource_id = resource.get("id")
        if not isinstance(resource_id, str) or not resource_id:
            errors.append(f"{FOUNDATIONS_PATH}: {location}: id must be a non-empty string")
        elif resource_id in seen_ids:
            errors.append(f"{FOUNDATIONS_PATH}: {location}: duplicate id {resource_id}")
        else:
            seen_ids.add(resource_id)

        if not isinstance(resource.get("title"), str) or not resource.get("title").strip():
            errors.append(f"{FOUNDATIONS_PATH}: {location}: title must be a non-empty string")
        if resource.get("resource_type") not in VALID_RESOURCE_TYPE:
            errors.append(
                f"{FOUNDATIONS_PATH}: {location}: resource_type must be one of {sorted(VALID_RESOURCE_TYPE)}"
            )
        year = resource.get("year")
        if not isinstance(year, int) or isinstance(year, bool) or year <= 0:
            errors.append(f"{FOUNDATIONS_PATH}: {location}: year must be a positive integer")
        if not is_http_url(resource.get("url"), required=True):
            errors.append(f"{FOUNDATIONS_PATH}: {location}: url must be an http(s) URL")
        if resource.get("arxiv_id") and not is_valid_arxiv_id(resource.get("arxiv_id")):
            errors.append(f"{FOUNDATIONS_PATH}: {location}: invalid arXiv ID {resource.get('arxiv_id')!r}")
        if resource.get("doi") and not is_valid_doi(resource.get("doi")):
            errors.append(f"{FOUNDATIONS_PATH}: {location}: invalid DOI {resource.get('doi')!r}")
        if not resource.get("arxiv_id") and not resource.get("doi") and not resource.get("url"):
            errors.append(f"{FOUNDATIONS_PATH}: {location}: at least one of arxiv_id, doi, or url must be present")

        isbn = resource.get("isbn")
        if not isinstance(isbn, list) or not all(isinstance(item, str) and item.strip() for item in isbn):
            errors.append(f"{FOUNDATIONS_PATH}: {location}: isbn must be an array of non-empty strings")
        if not isinstance(resource.get("venue"), str) or not resource.get("venue").strip():
            errors.append(f"{FOUNDATIONS_PATH}: {location}: venue must be a non-empty string")
        if resource.get("publisher") is not None and (
            not isinstance(resource.get("publisher"), str) or not resource.get("publisher").strip()
        ):
            errors.append(f"{FOUNDATIONS_PATH}: {location}: publisher must be a non-empty string or null")

        contributors = resource.get("contributors")
        if not isinstance(contributors, list) or not contributors or not all(
            isinstance(item, str) and item.strip() for item in contributors
        ):
            errors.append(f"{FOUNDATIONS_PATH}: {location}: contributors must be a non-empty array of strings")
        if resource.get("contributor_role") not in VALID_CONTRIBUTOR_ROLE:
            errors.append(
                f"{FOUNDATIONS_PATH}: {location}: contributor_role must be one of {sorted(VALID_CONTRIBUTOR_ROLE)}"
            )
        if not isinstance(resource.get("summary"), str) or not resource.get("summary").strip():
            errors.append(f"{FOUNDATIONS_PATH}: {location}: summary must be a non-empty string")
        if not isinstance(resource.get("role"), str) or not resource.get("role").strip():
            errors.append(f"{FOUNDATIONS_PATH}: {location}: role must be a non-empty string")
        if resource.get("verification_status") not in VALID_FOUNDATION_VERIFICATION:
            errors.append(
                f"{FOUNDATIONS_PATH}: {location}: verification_status must be one of {sorted(VALID_FOUNDATION_VERIFICATION)}"
            )

        evidence = resource.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            errors.append(f"{FOUNDATIONS_PATH}: {location}: evidence must be a non-empty array")
            continue
        for item in evidence:
            if not isinstance(item, dict):
                errors.append(f"{FOUNDATIONS_PATH}: {location}: evidence entries must be objects")
                continue
            for key in ("source_url", "source_kind", "source_version", "claim", "accessed_at"):
                if key not in item:
                    errors.append(f"{FOUNDATIONS_PATH}: {location}: evidence entry missing {key}")
            if not is_http_url(item.get("source_url"), required=True):
                errors.append(f"{FOUNDATIONS_PATH}: {location}: evidence source_url must be an http(s) URL")
            if item.get("source_kind") not in VALID_SOURCE_KIND:
                errors.append(
                    f"{FOUNDATIONS_PATH}: {location}: invalid evidence source_kind {item.get('source_kind')!r}"
                )
            if not isinstance(item.get("source_version"), str) or not item.get("source_version").strip():
                errors.append(f"{FOUNDATIONS_PATH}: {location}: evidence source_version must be non-empty")
            if not isinstance(item.get("claim"), str) or not item.get("claim").strip():
                errors.append(f"{FOUNDATIONS_PATH}: {location}: evidence claim must be non-empty")
            if not is_valid_date(item.get("accessed_at")):
                errors.append(f"{FOUNDATIONS_PATH}: {location}: evidence accessed_at must be a valid ISO date")

    return errors


def validate_data() -> tuple[bool, list[str]]:
    errors: list[str] = []
    try:
        papers = load_json(PAPERS_PATH)
        axis_map, _ = taxonomy_axis_map()
        category_ids = display_category_ids()
    except ManageError as exc:
        return False, [str(exc)]

    if not isinstance(papers, list):
        return False, [f"{PAPERS_PATH}: root must be an array"]

    seen_ids: set[str] = set()
    seen_arxiv: dict[str, str] = {}
    seen_doi: dict[str, str] = {}
    records_by_id: dict[str, dict[str, Any]] = {}

    for index, record in enumerate(papers):
        location = f"record {index}" if not isinstance(record, dict) else f"record {record.get('id', index)}"
        if not isinstance(record, dict):
            errors.append(f"{PAPERS_PATH}: {location}: expected object")
            continue

        missing = sorted(REQUIRED_FIELDS - set(record))
        if missing:
            errors.append(f"{PAPERS_PATH}: {location}: missing fields {', '.join(missing)}")

        record_id = record.get("id")
        if not isinstance(record_id, str) or not record_id:
            errors.append(f"{PAPERS_PATH}: {location}: id must be a non-empty string")
            record_id = None
        elif record_id in seen_ids:
            errors.append(f"{PAPERS_PATH}: {location}: duplicate id {record_id}")
        else:
            seen_ids.add(record_id)
            records_by_id[record_id] = record

        if not isinstance(record.get("work_id"), str) or not record.get("work_id"):
            errors.append(f"{PAPERS_PATH}: {location}: work_id must be a non-empty string")

        if not isinstance(record.get("title"), str) or not record.get("title").strip():
            errors.append(f"{PAPERS_PATH}: {location}: title must be a non-empty string")

        authors = record.get("authors")
        if not isinstance(authors, list) or not all(isinstance(a, str) for a in authors):
            errors.append(f"{PAPERS_PATH}: {location}: authors must be an array of strings")
        elif not authors and record.get("metadata_status") != "unverified":
            errors.append(f"{PAPERS_PATH}: {location}: authors cannot be empty for a verified/conflict record")

        year = record.get("year")
        if isinstance(year, bool):
            errors.append(f"{PAPERS_PATH}: {location}: year must be a positive integer or null, not boolean")
        elif year is None:
            if record.get("metadata_status") != "unverified":
                errors.append(f"{PAPERS_PATH}: {location}: year can only be null for an unverified record")
        elif not isinstance(year, int) or year <= 0:
            errors.append(f"{PAPERS_PATH}: {location}: year must be a positive integer or null")

        if not is_http_url(record.get("canonical_url"), required=True):
            errors.append(f"{PAPERS_PATH}: {location}: canonical_url must be a non-empty http(s) URL")
        if not is_http_url(record.get("code_url"), required=False):
            errors.append(f"{PAPERS_PATH}: {location}: code_url must be an http(s) URL or null")

        enum_checks = [
            ("metadata_status", record.get("metadata_status"), VALID_METADATA_STATUS),
            ("reading_status", record.get("reading_status"), VALID_READING_STATUS),
            ("screening_status", record.get("screening_status"), VALID_SCREENING_STATUS),
            ("relevance", record.get("relevance"), VALID_RELEVANCE),
            ("record_type", record.get("record_type"), VALID_RECORD_TYPE),
            ("publication_status", record.get("publication_status"), VALID_PUBLICATION_STATUS),
            ("bibliography_type", record.get("bibliography_type"), VALID_BIBLIOGRAPHY_TYPE),
        ]
        for field_name, value, allowed in enum_checks:
            if value not in allowed:
                errors.append(
                    f"{PAPERS_PATH}: {location}: {field_name} must be one of {sorted(allowed)}, got {value!r}"
                )

        if not isinstance(record.get("human_reviewed"), bool):
            errors.append(f"{PAPERS_PATH}: {location}: human_reviewed must be a boolean")

        arxiv_id = record.get("arxiv_id")
        doi = record.get("doi")
        if not arxiv_id and not doi:
            errors.append(f"{PAPERS_PATH}: {location}: at least one of arxiv_id or doi must be present")
        if arxiv_id and not is_valid_arxiv_id(arxiv_id):
            errors.append(f"{PAPERS_PATH}: {location}: invalid arXiv ID {arxiv_id!r}")
        if doi and not is_valid_doi(doi):
            errors.append(f"{PAPERS_PATH}: {location}: invalid DOI {doi!r}")

        normalized_arxiv = normalize_arxiv_id(arxiv_id)
        normalized_doi = normalize_doi(doi)
        if normalized_arxiv:
            if normalized_arxiv in seen_arxiv and seen_arxiv[normalized_arxiv] != record_id:
                errors.append(
                    f"{PAPERS_PATH}: {location}: duplicate normalized arXiv ID {normalized_arxiv} "
                    f"(also used by {seen_arxiv[normalized_arxiv]})"
                )
            elif normalized_arxiv not in seen_arxiv:
                seen_arxiv[normalized_arxiv] = record_id or ""
        if normalized_doi:
            if normalized_doi in seen_doi and seen_doi[normalized_doi] != record_id:
                errors.append(
                    f"{PAPERS_PATH}: {location}: duplicate normalized DOI {normalized_doi} "
                    f"(also used by {seen_doi[normalized_doi]})"
                )
            elif normalized_doi not in seen_doi:
                seen_doi[normalized_doi] = record_id or ""

        related_versions = record.get("related_versions")
        if not isinstance(related_versions, list):
            errors.append(f"{PAPERS_PATH}: {location}: related_versions must be an array")
        else:
            for rel in related_versions:
                if not isinstance(rel, dict):
                    errors.append(f"{PAPERS_PATH}: {location}: related_versions entries must be objects")
                    continue
                rel_id = rel.get("id")
                relation = rel.get("relation")
                if not isinstance(rel_id, str) or not rel_id:
                    errors.append(f"{PAPERS_PATH}: {location}: related_versions entry has invalid id")
                if relation not in VALID_RELATION:
                    errors.append(
                        f"{PAPERS_PATH}: {location}: related_versions relation must be one of {sorted(VALID_RELATION)}"
                    )
                if rel_id == record_id:
                    errors.append(f"{PAPERS_PATH}: {location}: related_versions cannot reference itself")

        taxonomy_tags = record.get("taxonomy_tags")
        if not isinstance(taxonomy_tags, dict):
            errors.append(f"{PAPERS_PATH}: {location}: taxonomy_tags must be an object keyed by taxonomy axis id")
        else:
            for axis_id, tags in taxonomy_tags.items():
                if axis_id not in axis_map:
                    errors.append(f"{PAPERS_PATH}: {location}: unknown taxonomy axis {axis_id!r}")
                    continue
                if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
                    errors.append(f"{PAPERS_PATH}: {location}: taxonomy_tags[{axis_id}] must be an array of strings")
                    continue
                for tag in tags:
                    if tag not in axis_map[axis_id]:
                        errors.append(
                            f"{PAPERS_PATH}: {location}: taxonomy tag {tag!r} does not belong to axis {axis_id}"
                        )

        pending = record.get("taxonomy_migration_pending")
        if not isinstance(pending, list):
            errors.append(f"{PAPERS_PATH}: {location}: taxonomy_migration_pending must be an array")
        else:
            for item in pending:
                if not isinstance(item, dict) or not isinstance(item.get("tag"), str):
                    errors.append(f"{PAPERS_PATH}: {location}: taxonomy_migration_pending entries must be objects with a tag")

        primary_category = record.get("primary_category")
        if primary_category is not None:
            if not isinstance(primary_category, str) or primary_category not in category_ids:
                errors.append(
                    f"{PAPERS_PATH}: {location}: primary_category must be null or a valid display category id, got {primary_category!r}"
                )

        secondary_categories = record.get("secondary_categories")
        if not isinstance(secondary_categories, list) or not all(
            isinstance(item, str) for item in secondary_categories
        ):
            errors.append(f"{PAPERS_PATH}: {location}: secondary_categories must be an array of strings")
        else:
            if len(secondary_categories) != len(set(secondary_categories)):
                errors.append(f"{PAPERS_PATH}: {location}: secondary_categories must not contain duplicates")
            for category_id in secondary_categories:
                if category_id not in category_ids:
                    errors.append(
                        f"{PAPERS_PATH}: {location}: unknown secondary category {category_id!r}"
                    )
            if primary_category in secondary_categories:
                errors.append(
                    f"{PAPERS_PATH}: {location}: primary_category must not also appear in secondary_categories"
                )

        rationale = record.get("classification_rationale")
        if not isinstance(rationale, str) or not rationale.strip():
            errors.append(f"{PAPERS_PATH}: {location}: classification_rationale must be a non-empty string")

        evidence_refs = record.get("classification_evidence_refs")
        if not isinstance(evidence_refs, list) or not all(
            isinstance(item, str) and item.strip() for item in evidence_refs
        ):
            errors.append(
                f"{PAPERS_PATH}: {location}: classification_evidence_refs must be an array of non-empty strings"
            )

        classification_status = record.get("classification_status")
        if classification_status not in VALID_CLASSIFICATION_STATUS:
            errors.append(
                f"{PAPERS_PATH}: {location}: classification_status must be one of {sorted(VALID_CLASSIFICATION_STATUS)}"
            )

        evidence = record.get("uav_evidence")
        if not isinstance(evidence, list):
            errors.append(f"{PAPERS_PATH}: {location}: uav_evidence must be an array")
        else:
            for item in evidence:
                if item not in VALID_UAV_EVIDENCE:
                    errors.append(f"{PAPERS_PATH}: {location}: invalid uav_evidence value {item!r}")
            if "none" in evidence and len(evidence) > 1:
                errors.append(f"{PAPERS_PATH}: {location}: uav_evidence 'none' cannot be combined with other values")

        evidence_items = record.get("evidence_items")
        if not isinstance(evidence_items, list):
            errors.append(f"{PAPERS_PATH}: {location}: evidence_items must be an array")
        else:
            has_fulltext_item = False
            for item in evidence_items:
                if not isinstance(item, dict):
                    errors.append(f"{PAPERS_PATH}: {location}: evidence_items entries must be objects")
                    continue
                for key in (
                    "source_url",
                    "source_kind",
                    "source_version",
                    "locator",
                    "supports_fields",
                    "claim",
                    "attribution",
                    "accessed_at",
                ):
                    if key not in item:
                        errors.append(f"{PAPERS_PATH}: {location}: evidence_items entry missing {key}")
                if not is_http_url(item.get("source_url"), required=True):
                    errors.append(f"{PAPERS_PATH}: {location}: evidence_items source_url must be an http(s) URL")
                if item.get("source_kind") not in VALID_SOURCE_KIND:
                    errors.append(f"{PAPERS_PATH}: {location}: invalid evidence_items source_kind {item.get('source_kind')!r}")
                if item.get("attribution") not in VALID_ATTRIBUTION:
                    errors.append(f"{PAPERS_PATH}: {location}: invalid evidence_items attribution {item.get('attribution')!r}")
                if not isinstance(item.get("claim"), str) or not item.get("claim").strip():
                    errors.append(f"{PAPERS_PATH}: {location}: evidence_items claim must be a non-empty string")
                supports = item.get("supports_fields")
                if not isinstance(supports, list) or not supports or not all(isinstance(x, str) and x for x in supports):
                    errors.append(f"{PAPERS_PATH}: {location}: evidence_items supports_fields must be a non-empty array of strings")
                if item.get("source_kind") == "fulltext":
                    has_fulltext_item = True
                    if not isinstance(item.get("locator"), str) or not item.get("locator").strip():
                        errors.append(f"{PAPERS_PATH}: {location}: fulltext evidence requires a non-empty locator")
                    if not isinstance(item.get("source_version"), str) or not item.get("source_version").strip():
                        errors.append(f"{PAPERS_PATH}: {location}: fulltext evidence requires source_version")
                if not is_valid_date(item.get("accessed_at")):
                    errors.append(f"{PAPERS_PATH}: {location}: evidence_items accessed_at must be a valid ISO date")

            if record.get("reading_status") == "fulltext_reviewed" and not has_fulltext_item:
                errors.append(
                    f"{PAPERS_PATH}: {location}: reading_status=fulltext_reviewed requires at least one evidence item with source_kind=fulltext"
                )

        checked_at = record.get("checked_at")
        if checked_at is not None and not is_valid_date(checked_at):
            errors.append(f"{PAPERS_PATH}: {location}: checked_at must be a valid ISO date or null")
        if record.get("metadata_status") == "unverified" and checked_at is not None:
            errors.append(f"{PAPERS_PATH}: {location}: an unverified record cannot have checked_at")
        if record.get("metadata_status") in {"verified", "conflict"} and not is_valid_date(checked_at):
            errors.append(f"{PAPERS_PATH}: {location}: a verified/conflict record requires checked_at")

        conflict_scope = record.get("metadata_conflict_scope")
        if record.get("metadata_status") == "conflict":
            if not isinstance(conflict_scope, list) or not conflict_scope:
                errors.append(f"{PAPERS_PATH}: {location}: metadata_status=conflict requires metadata_conflict_scope")
            else:
                for scope in conflict_scope:
                    if scope not in VALID_CONFLICT_SCOPE:
                        errors.append(f"{PAPERS_PATH}: {location}: invalid metadata_conflict_scope value {scope!r}")
        elif conflict_scope not in (None, []):
            errors.append(f"{PAPERS_PATH}: {location}: metadata_conflict_scope should be null/empty unless metadata_status=conflict")

        if record.get("publication_status") == "withdrawn" and record.get("screening_status") == "included":
            errors.append(f"{PAPERS_PATH}: {location}: a withdrawn record cannot be included")
        if record.get("screening_status") == "excluded" and not (
            isinstance(record.get("exclusion_reason"), str) and record.get("exclusion_reason").strip()
        ):
            errors.append(f"{PAPERS_PATH}: {location}: excluded records require a non-empty exclusion_reason")

        if record.get("screening_status") == "included":
            if record.get("relevance") != "direct_uav":
                errors.append(f"{PAPERS_PATH}: {location}: included records must have relevance=direct_uav")
            if record.get("record_type") != "method":
                errors.append(f"{PAPERS_PATH}: {location}: included records must have record_type=method")
            if record.get("reading_status") != "fulltext_reviewed":
                errors.append(f"{PAPERS_PATH}: {location}: included core method requires reading_status=fulltext_reviewed")
            if record.get("publication_status") in {"withdrawn", "conflict"}:
                errors.append(f"{PAPERS_PATH}: {location}: included core method cannot use withdrawn/conflict publication_status")
            if record.get("metadata_status") == "conflict":
                scope = set(conflict_scope or [])
                if scope & {"title", "identity", "fulltext"}:
                    errors.append(
                        f"{PAPERS_PATH}: {location}: included core method cannot have unresolved title/identity/fulltext conflict"
                    )
            for field in ("neural_component", "symbolic_component", "coupling_mechanism", "inclusion_rationale"):
                value = record.get(field)
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"{PAPERS_PATH}: {location}: included core method requires non-empty {field}")
            if not any(
                isinstance(item, dict)
                and item.get("source_kind") == "fulltext"
                and isinstance(item.get("locator"), str)
                and item.get("locator").strip()
                for item in evidence_items
            ):
                errors.append(f"{PAPERS_PATH}: {location}: included core method requires fulltext evidence with a locator")

    for record in papers:
        if not isinstance(record, dict):
            continue
        location = f"record {record.get('id', '?')}"
        for rel in record.get("related_versions", []):
            if not isinstance(rel, dict):
                continue
            rel_id = rel.get("id")
            relation = rel.get("relation")
            if rel_id and rel_id not in records_by_id:
                errors.append(f"{PAPERS_PATH}: {location}: related_versions points to missing id {rel_id}")
            if rel_id and rel_id in records_by_id:
                reciprocal = None
                for other_rel in records_by_id[rel_id].get("related_versions", []):
                    if isinstance(other_rel, dict) and other_rel.get("id") == record.get("id"):
                        reciprocal = other_rel.get("relation")
                        break
                if reciprocal:
                    compatible = {
                        "supersedes": {"superseded_by"},
                        "superseded_by": {"supersedes"},
                        "earlier_version": {"later_version"},
                        "later_version": {"earlier_version"},
                        "same_work": {"same_work"},
                        "other": None,
                    }.get(relation)
                    if compatible is not None and reciprocal not in compatible:
                        errors.append(
                            f"{PAPERS_PATH}: {location}: conflicting related_versions relation "
                            f"{relation!r} with {rel_id}.{reciprocal!r}"
                        )

    errors.extend(validate_foundational_resources())
    return (not errors), errors


def count_core_methods(papers: list[dict[str, Any]]) -> int:
    seen_work_ids: set[str] = set()
    count = 0
    for record in papers:
        conflict_scope = set(record.get("metadata_conflict_scope") or [])
        if (
            record.get("screening_status") == "included"
            and record.get("relevance") == "direct_uav"
            and record.get("record_type") == "method"
            and record.get("reading_status") == "fulltext_reviewed"
            and record.get("publication_status") not in {"withdrawn", "conflict"}
            and not (conflict_scope & {"title", "identity", "fulltext"})
        ):
            work_id = str(record.get("work_id") or record.get("id"))
            if work_id not in seen_work_ids:
                seen_work_ids.add(work_id)
                count += 1
    return count


def distinct_non_withdrawn_work_ids(papers: list[dict[str, Any]]) -> int:
    return len(
        {
            str(record.get("work_id") or record.get("id"))
            for record in papers
            if record.get("publication_status") != "withdrawn"
        }
    )


def distinct_primary_work_ids(
    papers: list[dict[str, Any]], category_id: str | None = None
) -> int:
    return len(
        {
            str(record.get("work_id") or record.get("id"))
            for record in papers
            if record.get("publication_status") != "withdrawn"
            and (
                category_id is None
                or record.get("primary_category") == category_id
            )
        }
    )


def papers_stats(papers: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "total": len(papers),
        "metadata_verified": sum(1 for r in papers if r.get("metadata_status") == "verified"),
        "metadata_conflict": sum(1 for r in papers if r.get("metadata_status") == "conflict"),
        "abstract_reviewed": sum(1 for r in papers if r.get("reading_status") == "abstract_reviewed"),
        "fulltext_reviewed": sum(1 for r in papers if r.get("reading_status") == "fulltext_reviewed"),
        "candidates": sum(1 for r in papers if r.get("screening_status") == "candidate"),
        "included": sum(1 for r in papers if r.get("screening_status") == "included"),
        "direct_uav_candidates": sum(
            1
            for r in papers
            if r.get("screening_status") == "candidate"
            and r.get("relevance") == "direct_uav"
            and r.get("record_type") == "method"
        ),
        "core_methods": count_core_methods(papers),
        "withdrawn": sum(1 for r in papers if r.get("publication_status") == "withdrawn"),
        "migration_pending": sum(
            1 for r in papers if r.get("taxonomy_migration_pending")
        ),
        "unique_seed_studies": distinct_non_withdrawn_work_ids(papers),
    }


def markdown_escape(value: Any) -> str:
    text = "" if value is None else str(value)
    text = text.replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")
    return text.strip()


def bibtex_escape(value: Any) -> str:
    text = "" if value is None else str(value)
    replacements = {
        "&": "\\&",
        "%": "\\%",
        "#": "\\#",
        "_": "\\_",
        "$": "\\$",
        "{": "\\{",
        "}": "\\}",
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text


def bibtex_key(record: dict[str, Any]) -> str:
    key = str(record.get("id") or "paper")
    key = re.sub(r"[^A-Za-z0-9]+", "_", key).strip("_")
    return key or "paper"


def preferred_work_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_work: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        if record.get("metadata_status") not in {"verified", "conflict"}:
            continue
        if record.get("publication_status") == "withdrawn":
            continue
        by_work.setdefault(str(record.get("work_id") or record.get("id")), []).append(record)
    preferred: list[dict[str, Any]] = []
    for work_records in by_work.values():
        priority = {"published": 0, "preprint": 1, "unknown": 2, "conflict": 3}
        work_records.sort(key=lambda r: (priority.get(r.get("publication_status"), 9), r.get("year", 0)))
        preferred.append(work_records[0])
    preferred.sort(key=lambda r: str(r.get("id") or ""))
    return preferred


def render_bibtex(records: list[dict[str, Any]]) -> str:
    entries: list[str] = []
    keys: dict[str, str] = {}
    for record in preferred_work_records(records):
        key = bibtex_key(record)
        normalized_key = key.lower()
        if normalized_key in keys:
            raise ManageError(
                f"BibTeX key conflict after normalization: {key} from {record.get('id')} and {keys[normalized_key]}"
            )
        keys[normalized_key] = record.get("id", key)

        authors = " and ".join(bibtex_escape(a) for a in record.get("authors", []))
        title = bibtex_escape(record.get("title", ""))
        year = record.get("year", "")
        arxiv_id = record.get("arxiv_id") or ""
        canonical_url = record.get("canonical_url") or ""
        doi = record.get("doi") or ""
        code_url = record.get("code_url") or ""
        venue = record.get("venue") or ""
        bibliography_type = record.get("bibliography_type") or "misc"
        note_parts: list[str] = []
        if code_url:
            note_parts.append(f"Code: {bibtex_escape(code_url)}")
        if record.get("metadata_status") == "conflict":
            scope = record.get("metadata_conflict_scope") or []
            if scope:
                note_parts.append(
                    "Metadata conflict: " + ", ".join(bibtex_escape(str(item)) for item in scope)
                )
        note = ", ".join(note_parts)

        if bibliography_type == "article":
            lines = [f"@article{{{key},", f"  title = {{{title}}},"]
            if authors:
                lines.append(f"  author = {{{authors}}},")
            lines.append(f"  year = {{{year}}},")
            if venue:
                lines.append(f"  journal = {{{bibtex_escape(venue)}}},")
            if doi:
                lines.append(f"  doi = {{{bibtex_escape(doi)}}},")
            if canonical_url:
                lines.append(f"  url = {{{bibtex_escape(canonical_url)}}},")
            if note:
                lines.append(f"  note = {{{note}}},")
            lines.append("}")
            entries.append("\n".join(lines))
            continue

        if bibliography_type == "inproceedings":
            lines = [f"@inproceedings{{{key},", f"  title = {{{title}}},"]
            if authors:
                lines.append(f"  author = {{{authors}}},")
            lines.append(f"  year = {{{year}}},")
            if venue:
                lines.append(f"  booktitle = {{{bibtex_escape(venue)}}},")
            if doi:
                lines.append(f"  doi = {{{bibtex_escape(doi)}}},")
            if canonical_url:
                lines.append(f"  url = {{{bibtex_escape(canonical_url)}}},")
            if note:
                lines.append(f"  note = {{{note}}},")
            lines.append("}")
            entries.append("\n".join(lines))
            continue

        lines = [f"@misc{{{key},", f"  title = {{{title}}},"]
        if authors:
            lines.append(f"  author = {{{authors}}},")
        if year:
            lines.append(f"  year = {{{year}}},")
        if arxiv_id:
            lines.append(f"  eprint = {{{bibtex_escape(arxiv_id)}}},")
            lines.append("  archivePrefix = {arXiv},")
        if doi:
            lines.append(f"  doi = {{{bibtex_escape(doi)}}},")
        if venue and record.get("publication_status") != "preprint":
            lines.append(f"  howpublished = {{{bibtex_escape(venue)}}},")
        if canonical_url:
            lines.append(f"  url = {{{bibtex_escape(canonical_url)}}},")
        if note:
            lines.append(f"  note = {{{note}}},")
        lines.append("}")
        entries.append("\n".join(lines))

    return "\n\n".join(entries) + ("\n" if entries else "")


def taxonomy_display_tags(record: dict[str, Any]) -> list[str]:
    tags = record.get("taxonomy_tags") or {}
    if not isinstance(tags, dict):
        return []
    return [f"{axis}:{tag}" for axis, values in tags.items() for tag in values]


def category_name(category: dict[str, Any], language: str) -> str:
    if language == "zh":
        return category.get("name_zh") or category.get("name") or category.get("id") or ""
    return category.get("name") or category.get("id") or ""


def category_name_for_id(category_id: str, language: str = "en") -> str:
    for category in taxonomy_display_categories():
        if category.get("id") == category_id:
            return category_name(category, language)
    return category_id


def category_cell(record: dict[str, Any]) -> str:
    primary = record.get("primary_category")
    secondary = record.get("secondary_categories") or []
    names: list[str] = []
    if primary:
        names.append(category_name_for_id(primary))
    names.extend(category_name_for_id(item) for item in secondary if item != primary)
    return ", ".join(names)


def theme_primary_records(
    papers: list[dict[str, Any]], category_id: str
) -> list[dict[str, Any]]:
    return [record for record in papers if record.get("primary_category") == category_id]


def theme_secondary_records(
    papers: list[dict[str, Any]], category_id: str
) -> list[dict[str, Any]]:
    return [
        record
        for record in papers
        if category_id in (record.get("secondary_categories") or [])
        and record.get("primary_category") != category_id
    ]


def publication_label(record: dict[str, Any]) -> str:
    status = record.get("publication_status") or ""
    if status == "published" and record.get("venue"):
        return f"Published ({record.get('venue')})"
    if status == "published":
        return "Published"
    return str(status or "unknown").replace("_", " ")


def paper_links_markdown(record: dict[str, Any]) -> str:
    parts: list[str] = []
    if record.get("canonical_url"):
        parts.append(f"[paper]({record['canonical_url']})")
    else:
        parts.append("\u2014")
    if record.get("code_url"):
        parts.append(f"[code]({record['code_url']})")
    else:
        parts.append("code: \u2014 / not verified")
    return " \u00b7 ".join(parts)


def compact_theme_table_markdown(records: list[dict[str, Any]]) -> str:
    if not records:
        return ""
    headers = ["Paper", "Neural\u2013Symbolic Coupling", "UAV Task", "Evidence / Review", "Publication", "Links"]
    lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for record in records:
        title = markdown_escape(record.get("title"))
        canonical = record.get("canonical_url") or ""
        if canonical:
            paper_cell = f"[{title}]({canonical})"
        else:
            paper_cell = title
        tags = record.get("taxonomy_tags") or {}
        task = ", ".join(tags.get("uav_task", [])) or "\u2014"
        evidence = (
            f"{record.get('reading_status') or ''} / {', '.join(record.get('uav_evidence', [])) or '\u2014'}"
        )
        lines.append(
            "| "
            + " | ".join(
                [
                    paper_cell,
                    markdown_escape(record.get("coupling_mechanism") or "\u2014"),
                    markdown_escape(task),
                    markdown_escape(evidence),
                    markdown_escape(publication_label(record)),
                    paper_links_markdown(record),
                ]
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def research_theme_section_markdown(
    papers: list[dict[str, Any]], category: dict[str, Any], language: str
) -> str:
    category_id = category["id"]
    primary = theme_primary_records(papers, category_id)
    secondary = theme_secondary_records(papers, category_id)
    parts: list[str] = []
    parts.append(f"### {category_name(category, language)}")
    parts.append("")
    parts.append(category.get("description") or "")
    parts.append("")
    parts.append(f"**Boundary:** {category.get('boundary') or ''}")
    subdirections = category.get("subdirections") or []
    if subdirections:
        parts.append("")
        parts.append("**Subdirections:** " + "; ".join(subdirections))

    reviewed = [record for record in primary if record.get("screening_status") == "included"]
    candidates = [
        record
        for record in primary
        if record.get("screening_status") == "candidate"
        and record.get("relevance") == "direct_uav"
        and record.get("record_type") == "method"
    ]
    perspectives = [
        record
        for record in primary
        if record not in reviewed
        and record not in candidates
        and record.get("screening_status") != "excluded"
    ]

    if reviewed:
        parts.append("")
        parts.append("#### Reviewed core methods")
        parts.append("")
        parts.append(compact_theme_table_markdown(reviewed))
    if candidates:
        parts.append("")
        parts.append("#### Candidate methods")
        parts.append("")
        parts.append(compact_theme_table_markdown(candidates))
    if perspectives:
        parts.append("")
        parts.append("#### Related architectures / perspectives")
        parts.append("")
        parts.append(compact_theme_table_markdown(perspectives))
    if secondary:
        parts.append("")
        parts.append("#### Cross-theme links")
        parts.append("")
        parts.append(
            ", ".join(
                f"`{record.get('id')}`" for record in secondary
            )
            + " appear in a different primary theme and are listed here for cross-reference only."
        )
    if not (reviewed or candidates or perspectives):
        parts.append("")
        parts.append("_No seed method is currently assigned to this primary theme._")
    return "\n".join(parts)


def auxiliary_records(papers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [record for record in papers if not record.get("primary_category")]


def auxiliary_section_markdown(papers: list[dict[str, Any]]) -> str:
    records = auxiliary_records(papers)
    parts = ["### Surveys, Foundations & System Architectures", ""]
    if not records:
        parts.append("_No auxiliary records._")
        return "\n".join(parts)
    headers = ["Paper", "Role", "Reading", "Status", "Links"]
    lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for record in records:
        title = markdown_escape(record.get("title"))
        canonical = record.get("canonical_url") or ""
        paper_cell = f"[{title}]({canonical})" if canonical else title
        role = markdown_escape(record.get("record_type") or "")
        lines.append(
            "| "
            + " | ".join(
                [
                    paper_cell,
                    role,
                    markdown_escape(record.get("reading_status") or ""),
                    markdown_escape(record.get("screening_status") or ""),
                    paper_links_markdown(record),
                ]
            )
            + " |"
        )
    parts.append("\n".join(lines) + "\n")
    return "\n".join(parts)


def research_themes_markdown(papers: list[dict[str, Any]], language: str) -> str:
    categories = taxonomy_display_categories()
    parts: list[str] = []
    aux = auxiliary_section_markdown(papers)
    if aux:
        parts.append(aux)
        parts.append("")
    for category in categories:
        parts.append(research_theme_section_markdown(papers, category, language))
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def category_coverage_markdown(papers: list[dict[str, Any]]) -> str:
    stats = papers_stats(papers)
    categories = taxonomy_display_categories()
    lines: list[str] = []
    lines.append(f"- Unique seed studies (non-withdrawn, distinct `work_id`): **{stats['unique_seed_studies']}**")
    lines.append(f"- Formally included core methods (deduplicated): **{stats['core_methods']}**")
    fulltext_work_ids = {
        str(record.get("work_id") or record.get("id"))
        for record in papers
        if record.get("reading_status") == "fulltext_reviewed"
        and record.get("publication_status") != "withdrawn"
    }
    abstract_work_ids = {
        str(record.get("work_id") or record.get("id"))
        for record in papers
        if record.get("reading_status") == "abstract_reviewed"
        and record.get("publication_status") != "withdrawn"
    }
    lines.append(f"- Full-text reviewed unique works: **{len(fulltext_work_ids)}**")
    lines.append(f"- Abstract-reviewed unique works: **{len(abstract_work_ids)}**")
    direct_candidates = [
        record
        for record in papers
        if record.get("screening_status") == "candidate"
        and record.get("relevance") == "direct_uav"
        and record.get("record_type") == "method"
        and record.get("publication_status") != "withdrawn"
    ]
    candidate_work_ids = {str(record.get("work_id") or record.get("id")) for record in direct_candidates}
    lines.append(f"- Direct UAV candidate methods (distinct `work_id`, non-withdrawn): **{len(candidate_work_ids)}**")
    architecture_work_ids = {
        str(record.get("work_id") or record.get("id"))
        for record in papers
        if record.get("relevance") == "direct_uav"
        and record.get("record_type") == "position"
        and record.get("publication_status") != "withdrawn"
    }
    lines.append(f"- Direct UAV architectures / perspectives (distinct `work_id`): **{len(architecture_work_ids)}**")
    lines.append("")
    lines.append("Primary assignments are mutually exclusive; secondary assignments are cross-references and do not add a study to more than one primary theme.")
    lines.append("")
    lines.append("| Display category | Primary unique works | Reading depth | Included core methods | Candidate methods | Perspectives | Gap note |")
    lines.append("|---|---|---|---|---|---|---|")
    for category in categories:
        category_id = category["id"]
        primary_ids = {
            str(record.get("work_id") or record.get("id"))
            for record in papers
            if record.get("primary_category") == category_id
            and record.get("publication_status") != "withdrawn"
        }
        included_ids = {
            str(record.get("work_id") or record.get("id"))
            for record in papers
            if record.get("primary_category") == category_id
            and record.get("screening_status") == "included"
            and record.get("record_type") == "method"
        }
        candidate_ids = {
            str(record.get("work_id") or record.get("id"))
            for record in papers
            if record.get("primary_category") == category_id
            and record.get("screening_status") == "candidate"
            and record.get("record_type") == "method"
        }
        perspective_ids = {
            str(record.get("work_id") or record.get("id"))
            for record in papers
            if record.get("primary_category") == category_id
            and record.get("record_type") == "position"
        }
        fulltext_count = len(
            {
                str(record.get("work_id") or record.get("id"))
                for record in papers
                if record.get("primary_category") == category_id
                and record.get("reading_status") == "fulltext_reviewed"
                and record.get("publication_status") != "withdrawn"
            }
        )
        abstract_count = len(
            {
                str(record.get("work_id") or record.get("id"))
                for record in papers
                if record.get("primary_category") == category_id
                and record.get("reading_status") == "abstract_reviewed"
                and record.get("publication_status") != "withdrawn"
            }
        )
        reading_depth = f"fulltext={fulltext_count}, abstract={abstract_count}"
        gap = ""
        if not primary_ids:
            gap = "no primary seed"
        elif not included_ids:
            gap = "no formally included core method"
        elif not candidate_ids and not perspective_ids:
            gap = "coverage is included-only"
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_escape(category_name(category, "en")),
                    str(len(primary_ids)),
                    reading_depth,
                    str(len(included_ids)),
                    str(len(candidate_ids)),
                    str(len(perspective_ids)),
                    gap,
                ]
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def resource_contributor_label(resource: dict[str, Any]) -> str:
    role = resource.get("contributor_role") or "contributors"
    labels = {
        "authors": "Authors",
        "editors": "Editors",
        "organizers": "Organizers",
    }
    return labels.get(role, role.replace("_", " ").capitalize())


def resource_links_markdown(resource: dict[str, Any]) -> str:
    links: list[str] = []
    if resource.get("doi"):
        links.append(f"[DOI](https://doi.org/{resource['doi']})")
    if resource.get("arxiv_id"):
        links.append(f"[arXiv](https://arxiv.org/abs/{resource['arxiv_id']})")
    if resource.get("url") and not resource.get("doi") and not resource.get("arxiv_id"):
        links.append(f"[page]({resource['url']})")
    isbn = resource.get("isbn") or []
    if isbn:
        links.append("ISBN " + ", ".join(markdown_escape(item) for item in isbn))
    return " \u00b7 ".join(links) if links else "\u2014"


def resource_venue_label(resource: dict[str, Any]) -> str:
    venue = resource.get("venue") or ""
    publisher = resource.get("publisher") or ""
    if publisher and publisher.lower() not in venue.lower():
        return f"{venue}; {publisher}" if venue else publisher
    return venue


def foundations_section_markdown(
    resources: list[dict[str, Any]], resource_type: str, language: str
) -> str:
    records = [resource for resource in resources if resource.get("resource_type") == resource_type]
    if not records:
        return ""
    titles = {
        "paper": "Foundational papers",
        "book": "Books and edited collections",
        "workshop": "Workshops and community resources",
        "collection": "Collections and special issues",
    }
    if language == "zh":
        titles = {
            "paper": "基础论文",
            "book": "书籍与编著",
            "workshop": "Workshop 与社区资源",
            "collection": "专辑与特刊",
        }
    lines = [f"### {titles.get(resource_type, resource_type)}", ""]
    if not records:
        return ""
    headers = ["Resource", "Contributors", "Year", "Venue / Publisher", "Links"]
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("|" + "---|" * len(headers))
    for resource in records:
        contributors = ", ".join(resource.get("contributors") or [])
        venue = resource_venue_label(resource)
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_escape(resource.get("title")),
                    markdown_escape(f"{resource_contributor_label(resource)}: {contributors}"),
                    str(resource.get("year") or ""),
                    markdown_escape(venue),
                    resource_links_markdown(resource),
                ]
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def foundations_markdown(language: str) -> str:
    resources = load_foundational_resources()
    parts: list[str] = []
    intro = (
        "These resources provide background, book-length references, and community "
        "venues. They are auxiliary: they are not counted as UAV paper records or "
        "core methods."
    )
    if language == "zh":
        intro = (
            "以下资源用于提供理论基础、书籍参考和社区信息。它们是辅助性资源，"
            "不计入 UAV 文献记录或核心方法统计。"
        )
    parts.append(intro)
    parts.append("")
    for resource_type in ("paper", "book", "workshop", "collection"):
        section = foundations_section_markdown(resources, resource_type, language)
        if section:
            parts.append(section)
    return "\n".join(parts).rstrip() + "\n"


def foundations_cards_html() -> str:
    resources = load_foundational_resources()
    groups = [
        ("paper", "Foundational papers"),
        ("book", "Books and edited collections"),
        ("workshop", "Workshops and community resources"),
        ("collection", "Collections and special issues"),
    ]
    blocks: list[str] = []
    for resource_type, title in groups:
        records = [resource for resource in resources if resource.get("resource_type") == resource_type]
        if not records:
            continue
        cards: list[str] = []
        for resource in records:
            contributors = ", ".join(resource.get("contributors") or [])
            venue = resource_venue_label(resource)
            link_parts: list[str] = []
            if resource.get("doi"):
                link_parts.append(
                    f'<a class="pill-link" href="https://doi.org/{html.escape(str(resource["doi"]))}" rel="noopener noreferrer">DOI</a>'
                )
            if resource.get("arxiv_id"):
                link_parts.append(
                    f'<a class="pill-link" href="https://arxiv.org/abs/{html.escape(str(resource["arxiv_id"]))}" rel="noopener noreferrer">arXiv</a>'
                )
            if resource.get("url") and not resource.get("doi") and not resource.get("arxiv_id"):
                link_parts.append(
                    f'<a class="pill-link" href="{html.escape(str(resource["url"]))}" rel="noopener noreferrer">page</a>'
                )
            cards.append(
                '<article class="foundation-card">'
                f'<span class="status-pill">{html.escape(resource_type)}</span>'
                f"<h3>{html.escape(resource.get('title') or '')}</h3>"
                f"<p>{html.escape(resource.get('summary') or '')}</p>"
                '<div class="foundation-meta">'
                f"<span>{html.escape(resource_contributor_label(resource))}: {html.escape(contributors)}</span>"
                f"<span>{html.escape(str(resource.get('year') or ''))}</span>"
                f"<span>{html.escape(venue)}</span>"
                "</div>"
                f'<div class="paper-actions">{"".join(link_parts)}</div>'
                "</article>"
            )
        blocks.append(f"<h3>{html.escape(title)}</h3>" f'<div class="foundation-grid">{"".join(cards)}</div>')
    return "".join(blocks)


def project_info_cards_html(project: dict[str, Any]) -> str:
    authors = ", ".join(str(a) for a in project.get("authors") or [])
    affiliations = "; ".join(str(a) for a in project.get("affiliations") or [])
    github_url = project.get("github_url") or ""
    license_name = project.get("license") or ""
    status = str(project.get("status") or "not specified")
    chips = [
        ("Authors", authors or "not specified"),
        ("Affiliation", affiliations or "not specified"),
        ("Repository", github_url or "not specified"),
        ("License", license_name or "not specified"),
        ("Status", status),
    ]
    return '<div class="hero-meta">' + "".join(
        f'<span class="meta-chip"><strong>{html.escape(label)}</strong> {html.escape(value)}</span>'
        for label, value in chips
    ) + "</div>"


def foundations_html() -> str:
    resources = load_foundational_resources()
    groups = [
        ("paper", "Foundational papers"),
        ("book", "Books and edited collections"),
        ("workshop", "Workshops and community resources"),
        ("collection", "Collections and special issues"),
    ]
    blocks: list[str] = []
    for resource_type, title in groups:
        records = [resource for resource in resources if resource.get("resource_type") == resource_type]
        if not records:
            continue
        rows: list[str] = []
        for resource in records:
            contributors = ", ".join(resource.get("contributors") or [])
            venue = resource_venue_label(resource)
            link_parts: list[str] = []
            if resource.get("doi"):
                link_parts.append(
                    f'<a href="https://doi.org/{html.escape(str(resource["doi"]))}" rel="noopener noreferrer">DOI</a>'
                )
            if resource.get("arxiv_id"):
                link_parts.append(
                    f'<a href="https://arxiv.org/abs/{html.escape(str(resource["arxiv_id"]))}" rel="noopener noreferrer">arXiv</a>'
                )
            if resource.get("url") and not resource.get("doi") and not resource.get("arxiv_id"):
                link_parts.append(
                    f'<a href="{html.escape(str(resource["url"]))}" rel="noopener noreferrer">page</a>'
                )
            links = " \u00b7 ".join(link_parts) or "\u2014"
            rows.append(
                "<tr>"
                f"<td>{html.escape(resource.get('title') or '')}</td>"
                f"<td>{html.escape(resource_contributor_label(resource))}: "
                f"{html.escape(contributors)}</td>"
                f"<td>{html.escape(str(resource.get('year') or ''))}</td>"
                f"<td>{html.escape(venue)}</td>"
                f"<td>{links}</td>"
                "</tr>"
            )
        blocks.append(
            f"<h3>{html.escape(title)}</h3>"
            '<div class="table-wrap"><table><thead><tr>'
            "<th>Resource</th><th>Contributors</th><th>Year</th>"
            "<th>Venue / Publisher</th><th>Links</th>"
            "</tr></thead><tbody>"
            + "".join(rows)
            + "</tbody></table></div>"
        )
    return "\n".join(blocks)


def overview_markdown(papers: list[dict[str, Any]], language: str) -> str:
    stats = papers_stats(papers)
    if language == "zh":
        return (
            f"- 文献记录总数：{stats['total']}\n"
            f"- 元数据已核验：{stats['metadata_verified']}\n"
            f"- 元数据冲突：{stats['metadata_conflict']}\n"
            f"- 已做摘要阅读：{stats['abstract_reviewed']}\n"
            f"- 已做全文阅读：{stats['fulltext_reviewed']}\n"
            f"- 候选条目：{stats['candidates']}\n"
            f"- 直接 UAV 候选方法：{stats['direct_uav_candidates']}\n"
            f"- 核心 UAV 方法（已纳入、去重、非撤回）：{stats['core_methods']}\n"
            f"- 唯一种子研究（去重、非撤回）：{stats['unique_seed_studies']}\n"
            f"- 撤回/版本关联条目：{stats['withdrawn']}\n"
            f"- 待复核分类迁移：{stats['migration_pending']}\n"
        )
    return (
        f"- Total records: {stats['total']}\n"
        f"- Metadata verified: {stats['metadata_verified']}\n"
        f"- Metadata conflicts: {stats['metadata_conflict']}\n"
        f"- Abstract-reviewed: {stats['abstract_reviewed']}\n"
        f"- Full-text reviewed: {stats['fulltext_reviewed']}\n"
        f"- Candidate records: {stats['candidates']}\n"
        f"- Direct UAV candidate methods: {stats['direct_uav_candidates']}\n"
        f"- Core UAV methods (included, deduplicated, non-withdrawn): {stats['core_methods']}\n"
        f"- Unique seed studies (deduplicated, non-withdrawn): {stats['unique_seed_studies']}\n"
        f"- Withdrawn/version-linked records: {stats['withdrawn']}\n"
        f"- Taxonomy migration pending: {stats['migration_pending']}\n"
    )


def paper_table_markdown(records: list[dict[str, Any]]) -> str:
    headers = [
        "ID",
        "Category",
        "Title",
        "Authors",
        "Year",
        "Type",
        "Screening",
        "Metadata",
        "Reading",
        "UAV evidence",
        "Canonical URL",
    ]
    lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for record in records:
        authors = ", ".join(record.get("authors", []))
        canonical = record.get("canonical_url") or ""
        canonical_cell = f"[{markdown_escape(canonical)}]({canonical})" if canonical else ""
        row = [
            markdown_escape(record.get("id")),
            markdown_escape(category_cell(record)),
            markdown_escape(record.get("title")),
            markdown_escape(authors),
            str(record.get("year") or ""),
            markdown_escape(record.get("record_type")),
            markdown_escape(record.get("screening_status")),
            markdown_escape(record.get("metadata_status")),
            markdown_escape(record.get("reading_status")),
            ", ".join(markdown_escape(item) for item in record.get("uav_evidence", [])),
            canonical_cell,
        ]
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines) + "\n"


def category_cards_html(papers: list[dict[str, Any]]) -> str:
    categories = taxonomy_display_categories()
    cards: list[str] = []
    for index, category in enumerate(categories, start=1):
        category_id = category["id"]
        primary_count = distinct_primary_work_ids(papers, category_id)
        subdirections = "".join(
            f'<span class="tag">{html.escape(item)}</span>'
            for item in category.get("subdirections") or []
        )
        cards.append(
            '<article class="theme-card" data-theme="'
            + html.escape(category_id)
            + '" tabindex="0" role="button" aria-label="Filter papers by '
            + html.escape(category.get("name") or category_id)
            + '">'
            f'<span class="theme-index">{index}</span>'
            f"<h3>{html.escape(category.get('name') or category_id)}</h3>"
            f'<div class="theme-name-zh">{html.escape(category.get("name_zh") or "")}</div>'
            f'<div class="theme-description">{html.escape(category.get("description") or "")}</div>'
            f'<div class="theme-boundary">{html.escape(category.get("boundary") or "")}</div>'
            f'<div class="theme-subdirections">{subdirections}</div>'
            f'<div class="theme-count">{primary_count} primary work{"s" if primary_count != 1 else ""}</div>'
            "</article>"
        )
    return "".join(cards)


def overview_html(papers: list[dict[str, Any]]) -> str:
    stats = papers_stats(papers)
    foundations = load_foundational_resources()
    values = [
        (str(stats["total"]), "Tracked records"),
        (str(stats["unique_seed_studies"]), "Unique seed studies"),
        (str(stats["fulltext_reviewed"]), "Full-text reviewed"),
        (str(stats["candidates"]), "Candidate records"),
        (str(stats["core_methods"]), "Included core methods"),
        (str(stats["direct_uav_candidates"]), "Direct UAV candidates"),
        (str(len(foundations)), "Foundational resources"),
        (str(len(taxonomy_display_categories())), "Display themes"),
    ]
    cards = "".join(
        '<div class="stat-card">'
        f'<span class="stat-value">{html.escape(value)}</span>'
        f'<span class="stat-label">{html.escape(label)}</span>'
        "</div>"
        for value, label in values
    )
    return cards


def evidence_summary(record: dict[str, Any]) -> str:
    items = record.get("evidence_items") or []
    return "; ".join(
        f"{item.get('source_kind')}:{item.get('locator') or 'no-locator'}" for item in items
    )


def note_file_exists(record: dict[str, Any]) -> bool:
    record_id = record.get("id")
    if not isinstance(record_id, str) or not record_id:
        return False
    return (ROOT / "notes" / "papers" / f"{record_id}.md").exists()


def note_link_html(record: dict[str, Any]) -> str:
    if not note_file_exists(record):
        return ""
    record_id = html.escape(record.get("id") or "")
    url = f"https://github.com/ppppyq/UAVs_Meet_Neuro-Symbolic-AI/blob/master/notes/papers/{record_id}.md"
    return f'<a href="{html.escape(url)}" rel="noopener noreferrer">note</a>'


def evidence_links_html(record: dict[str, Any]) -> str:
    links: list[str] = []
    for item in record.get("evidence_items") or []:
        source_url = item.get("source_url")
        if not source_url:
            continue
        label_parts = [str(item.get("source_kind") or "evidence")]
        locator = item.get("locator")
        if locator:
            label_parts.append(str(locator))
        label = html.escape(": ".join(label_parts))
        links.append(
            f'<a href="{html.escape(str(source_url))}" rel="noopener noreferrer">{label}</a>'
        )
    return " ".join(links) if links else "—"


def version_conflict_hint(record: dict[str, Any]) -> str:
    parts: list[str] = []
    conflicts = record.get("metadata_conflict_scope") or []
    if conflicts:
        parts.append("conflict:" + ",".join(str(item) for item in conflicts))
    for rel in record.get("related_versions") or []:
        if isinstance(rel, dict):
            parts.append(f"{rel.get('relation')}:{rel.get('id')}")
    if record.get("publication_status") == "withdrawn":
        parts.append("withdrawn")
    return "; ".join(parts) if parts else ""


def paper_card_html(record: dict[str, Any]) -> str:
    title = html.escape(record.get("title") or "")
    authors = html.escape(", ".join(record.get("authors", [])))
    screening = record.get("screening_status") or ""
    summary = record.get("summary") or record.get("classification_rationale") or ""
    tags = "".join(
        f'<span class="tag">{html.escape(tag)}</span>' for tag in taxonomy_display_tags(record)
    )
    canonical = record.get("canonical_url") or ""
    code = record.get("code_url") or ""
    links: list[str] = []
    if canonical:
        links.append(
            f'<a class="pill-link" href="{html.escape(canonical)}" rel="noopener noreferrer">paper</a>'
        )
    if code:
        links.append(
            f'<a class="pill-link" href="{html.escape(code)}" rel="noopener noreferrer">code</a>'
        )
    else:
        links.append('<span class="pill-link muted">code: not verified</span>')
    evidence = evidence_links_html(record)
    if evidence and evidence != "\u2014":
        links.append(evidence)
    note = note_link_html(record)
    if note:
        links.append(note)
    version_hint = version_conflict_hint(record)
    if version_hint:
        links.append(f'<span class="pill-link muted">{html.escape(version_hint)}</span>')
    meta_parts = [
        f"<span>{authors}</span>",
        f"<span>{html.escape(str(record.get('year') or ''))}</span>",
        f"<span>{html.escape(record.get('record_type') or '')}</span>",
        f"<span>{html.escape(category_cell(record))}</span>",
    ]
    return (
        '<article class="paper-card">'
        '<div class="paper-card-head">'
        f"<h3>{title}</h3>"
        f'<span class="status-pill {html.escape(screening)}">{html.escape(screening)}</span>'
        "</div>"
        f'<div class="paper-meta">{"".join(meta_parts)}</div>'
        f'<p class="paper-summary">{html.escape(summary)}</p>'
        f'<div class="tag-list">{tags}</div>'
        f'<div class="paper-actions">{"".join(links)}</div>'
        "</article>"
    )


def paper_cards_html(records: list[dict[str, Any]]) -> str:
    cards = "".join(paper_card_html(record) for record in records)
    return f'<div class="paper-grid">{cards}</div>'


def paper_table_html(records: list[dict[str, Any]]) -> str:
    headers = [
        "Title",
        "Category",
        "Authors",
        "Year",
        "Type",
        "Screening",
        "Metadata",
        "Reading",
        "Relevance",
        "Version/conflict",
        "UAV evidence",
        "Evidence and notes",
        "Links",
    ]
    head = "".join(f"<th>{html.escape(value)}</th>" for value in headers)
    rows: list[str] = []
    for record in records:
        title = html.escape(record.get("title") or "")
        tags = "".join(
            f'<span class="tag">{html.escape(tag)}</span>' for tag in taxonomy_display_tags(record)
        )
        title_cell = f'{title}<br><span class="tag-list">{tags}</span>'
        authors = html.escape(", ".join(record.get("authors", [])))
        canonical = record.get("canonical_url") or ""
        code = record.get("code_url") or ""
        canonical_link = (
            f'<a href="{html.escape(canonical)}" rel="noopener noreferrer">original</a>'
            if canonical
            else "—"
        )
        code_link = (
            f'<a href="{html.escape(code)}" rel="noopener noreferrer">code</a>' if code else "—"
        )
        links = f"{canonical_link} · {code_link}"
        screening = record.get("screening_status") or ""
        metadata = record.get("metadata_status") or ""
        relevance = record.get("relevance") or ""
        version_hint = html.escape(version_conflict_hint(record))
        evidence_notes = " ".join(
            part for part in [evidence_links_html(record), note_link_html(record)] if part
        )
        row = "".join(
            [
                "<tr>",
                f"<td>{title_cell}</td>",
                f"<td>{html.escape(category_cell(record))}</td>",
                f"<td>{authors}</td>",
                f"<td>{html.escape(str(record.get('year') or ''))}</td>",
                f"<td>{html.escape(record.get('record_type') or '')}</td>",
                f'<td><span class="status {html.escape(screening)}">{html.escape(screening)}</span></td>',
                f'<td><span class="status {html.escape(metadata)}">{html.escape(metadata)}</span></td>',
                f"<td>{html.escape(record.get('reading_status') or '')}</td>",
                f"<td>{html.escape(relevance)}</td>",
                f"<td>{version_hint}</td>",
                f"<td>{html.escape(', '.join(record.get('uav_evidence', [])))}</td>",
                f"<td>{evidence_notes}</td>",
                f"<td>{links}</td>",
                "</tr>",
            ]
        )
        rows.append(row)
    return (
        '<div class="table-wrap"><table>'
        f"<thead><tr>{head}</tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table></div>"
    )


def project_info_html(project: dict[str, Any]) -> str:
    authors = ", ".join(str(a) for a in project.get("authors") or [])
    affiliations = "; ".join(str(a) for a in project.get("affiliations") or [])
    github_url = project.get("github_url") or ""
    license_name = project.get("license") or ""
    items = [
        ("Authors", authors or "not specified"),
        ("Affiliations", affiliations or "not specified"),
        ("Repository", github_url or "not specified"),
        ("License", license_name or "not specified"),
        ("Status", str(project.get("status") or "not specified")),
    ]
    rows = "".join(
        f"<dt>{html.escape(label)}</dt><dd>{html.escape(value)}</dd>" for label, value in items
    )
    return f"<dl>\n{rows}\n</dl>\n"


def figure_sources_html() -> str:
    figures_dir = ROOT / "assets" / "figures"
    if not figures_dir.exists():
        return '<p class="status-note">No editable figure sources were found in assets/figures/.</p>'
    blocks: list[str] = []
    for path in sorted(figures_dir.glob("*.mmd")):
        name = html.escape(path.name)
        source = html.escape(path.read_text(encoding="utf-8").strip())
        blocks.append(
            f'<h3>{name}</h3><pre class="mermaid-source"><code>{source}</code></pre>'
        )
    return "\n".join(blocks) if blocks else '<p class="status-note">No .mmd figure sources were found.</p>'


def notes_available_map(records: list[dict[str, Any]]) -> dict[str, bool]:
    result: dict[str, bool] = {}
    for record in records:
        record_id = record.get("id")
        if isinstance(record_id, str):
            result[record_id] = note_file_exists(record)
    return result


def evidence_matrix_markdown(records: list[dict[str, Any]]) -> str:
    headers = [
        "ID",
        "Category",
        "Screening",
        "Neural component",
        "Symbolic mechanism",
        "Coupling",
        "Task",
        "Validation evidence",
        "Evidence locations",
        "Limitations",
    ]
    lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for record in records:
        tags = record.get("taxonomy_tags") or {}
        task = ", ".join(tags.get("uav_task", []))
        symbolic = ", ".join(tags.get("symbolic_mechanism", []))
        locations = "; ".join(
            f"{item.get('source_kind')}:{item.get('locator') or 'no-locator'}" for item in record.get("evidence_items", [])
        )
        row = [
            markdown_escape(record.get("id")),
            markdown_escape(category_cell(record)),
            markdown_escape(record.get("screening_status")),
            markdown_escape(record.get("neural_component")),
            symbolic,
            markdown_escape(record.get("coupling_mechanism")),
            task,
            ", ".join(record.get("uav_evidence", [])),
            locations,
            markdown_escape(record.get("limitations")),
        ]
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines) + "\n"


def apply_generated_block(text: str, start: str, end: str, content: str, path_label: str) -> str:
    start_count = text.count(start)
    end_count = text.count(end)
    if start_count != 1 or end_count != 1:
        raise ManageError(
            f"{path_label}: expected exactly one marker pair "
            f"{start!r}/{end!r}, found starts={start_count}, ends={end_count}"
        )
    start_pos = text.index(start) + len(start)
    end_pos = text.index(end)
    if end_pos < start_pos:
        raise ManageError(f"{path_label}: generated markers are out of order")
    return text[:start_pos] + "\n\n" + content + "\n" + text[end_pos:]


def generate_readme(papers: list[dict[str, Any]], source: Path, target: Path, language: str) -> None:
    text = source.read_text(encoding="utf-8")
    text = apply_generated_block(
        text,
        OVERVIEW_MARKER_START,
        OVERVIEW_MARKER_END,
        overview_markdown(papers, language),
        str(source),
    )
    text = apply_generated_block(
        text,
        RESEARCH_THEMES_MARKER_START,
        RESEARCH_THEMES_MARKER_END,
        research_themes_markdown(papers, language),
        str(source),
    )
    text = apply_generated_block(
        text,
        FOUNDATIONS_MARKER_START,
        FOUNDATIONS_MARKER_END,
        foundations_markdown(language),
        str(source),
    )
    write_text(target, text)


def generate_paper_index(papers: list[dict[str, Any]], output_path: Path) -> None:
    source = PAPER_INDEX_PATH
    text = source.read_text(encoding="utf-8")
    text = apply_generated_block(
        text,
        PAPER_INDEX_MARKER_START,
        PAPER_INDEX_MARKER_END,
        paper_table_markdown(papers),
        str(source),
    )
    write_text(output_path, text)


def generate_category_coverage(papers: list[dict[str, Any]], output_path: Path) -> None:
    source = CATEGORY_COVERAGE_PATH
    text = source.read_text(encoding="utf-8")
    text = apply_generated_block(
        text,
        CATEGORY_COVERAGE_MARKER_START,
        CATEGORY_COVERAGE_MARKER_END,
        category_coverage_markdown(papers),
        str(source),
    )
    write_text(output_path, text)


def generate_foundations_doc(output_path: Path) -> None:
    content = (
        "# Foundations, books, and workshops\n\n"
        "This file is generated from `data/foundational-resources.json` by "
        "`scripts/manage.py build`. These resources are auxiliary and are not "
        "counted as UAV paper records or core methods.\n\n"
        + foundations_markdown("en")
    )
    write_text(output_path, content)


def generate_evidence_matrix(papers: list[dict[str, Any]], output_path: Path) -> None:
    source = EVIDENCE_MATRIX_PATH
    text = source.read_text(encoding="utf-8")
    text = apply_generated_block(
        text,
        EVIDENCE_MATRIX_MARKER_START,
        EVIDENCE_MATRIX_MARKER_END,
        evidence_matrix_markdown(papers),
        str(source),
    )
    write_text(output_path, text)


def json_for_script(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True).replace("</", "<\\/")


def generate_site(papers: list[dict[str, Any]], output_dir: Path) -> None:
    template = (WEBSITE_DIR / "template.html").read_text(encoding="utf-8")
    taxonomy = load_json(TAXONOMY_PATH)
    project = load_json(PROJECT_PATH)
    rendered = (
        template.replace("{{OVERVIEW_HTML}}", overview_html(papers))
        .replace("{{PAPER_TABLE_HTML}}", paper_cards_html(papers))
        .replace("{{PROJECT_INFO_HTML}}", project_info_cards_html(project))
        .replace("{{FIGURE_SOURCES_HTML}}", figure_sources_html())
        .replace("{{FOUNDATIONS_HTML}}", foundations_cards_html())
        .replace("{{CATEGORY_CARDS_HTML}}", category_cards_html(papers))
        .replace("{{PAPER_DATA_JSON}}", json_for_script(papers))
        .replace("{{TAXONOMY_DATA_JSON}}", json_for_script(taxonomy))
        .replace("{{PROJECT_DATA_JSON}}", json_for_script(project))
        .replace("{{NOTES_AVAILABLE_JSON}}", json_for_script(notes_available_map(papers)))
    )
    unreplaced = [token for token in WEBSITE_TOKENS if token in rendered]
    if unreplaced:
        raise ManageError(f"website template still contains placeholders: {', '.join(unreplaced)}")
    write_text(output_dir / "index.html", rendered)

    static_source = WEBSITE_DIR / "static"
    static_target = output_dir / "static"
    static_target.mkdir(parents=True, exist_ok=True)
    for path in sorted(static_source.rglob("*")):
        if path.is_file():
            relative = path.relative_to(static_source)
            destination = static_target / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, destination)


def generate_tracked(papers: list[dict[str, Any]], output_root: Path) -> None:
    generate_readme(papers, README_EN_PATH, output_root / "README.md", "en")
    generate_readme(papers, README_ZH_PATH, output_root / "README.zh-CN.md", "zh")
    write_text(output_root / "paper" / "references.bib", render_bibtex(papers))
    generate_evidence_matrix(papers, output_root / "docs" / "evidence-matrix.md")
    generate_paper_index(papers, output_root / "docs" / "paper-index.md")
    generate_category_coverage(papers, output_root / "docs" / "category-coverage.md")
    generate_foundations_doc(output_root / "docs" / "foundations.md")


def generate_all(papers: list[dict[str, Any]], output_root: Path) -> None:
    generate_tracked(papers, output_root)
    generate_site(papers, output_root / "site")


def build_project() -> None:
    papers = load_json(PAPERS_PATH)
    generate_all(papers, ROOT)


def output_file_map(output_root: Path) -> dict[str, bytes]:
    if not output_root.exists():
        return {}
    result: dict[str, bytes] = {}
    for path in sorted(output_root.rglob("*")):
        if path.is_file():
            result[str(path.relative_to(output_root)).replace("\\", "/")] = path.read_bytes()
    return result


def check_local_markdown_links(root: Path, errors: list[str]) -> None:
    link_re = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
    for path in sorted(root.rglob("*.md")):
        if "site" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for _, target in link_re.findall(text):
            target = target.strip().split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"{path}: local markdown link target does not exist: {target}")


def check_local_html_links(root: Path, errors: list[str]) -> None:
    attr_re = re.compile(r"(?:href|src)=[\"']([^\"']+)[\"']")
    for path in sorted(root.rglob("*.html")):
        text = path.read_text(encoding="utf-8")
        for target in attr_re.findall(text):
            target = target.split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "javascript:", "data:")):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"{path}: local HTML link target does not exist: {target}")


def compare_file_maps(expected: dict[str, bytes], actual: dict[str, bytes], label: str) -> list[str]:
    errors: list[str] = []
    expected_paths = set(expected)
    actual_paths = set(actual)
    for missing in sorted(expected_paths - actual_paths):
        errors.append(f"{label}: missing generated file: {missing}")
    for stale in sorted(actual_paths - expected_paths):
        errors.append(f"{label}: unexpected generated file (stale or manually added): {stale}")
    for path in sorted(expected_paths & actual_paths):
        if expected[path] != actual[path]:
            errors.append(f"{label}: generated file is out of sync: {path}")
    return errors


def compare_tracked() -> tuple[bool, list[str]]:
    papers = load_json(PAPERS_PATH)
    errors: list[str] = []
    with tempfile.TemporaryDirectory() as temp_dir:
        output_root = Path(temp_dir)
        generate_tracked(papers, output_root)
        expected = output_file_map(output_root)
    actual = {
        "README.md": README_EN_PATH.read_bytes(),
        "README.zh-CN.md": README_ZH_PATH.read_bytes(),
        "paper/references.bib": BIB_PATH.read_bytes(),
        "docs/evidence-matrix.md": EVIDENCE_MATRIX_PATH.read_bytes(),
        "docs/paper-index.md": PAPER_INDEX_PATH.read_bytes(),
        "docs/category-coverage.md": CATEGORY_COVERAGE_PATH.read_bytes(),
        "docs/foundations.md": FOUNDATIONS_DOC_PATH.read_bytes(),
    }
    errors.extend(compare_file_maps(expected, actual, "tracked generated output"))
    check_local_markdown_links(ROOT, errors)
    return (not errors), errors


def compare_expected_with_actual() -> tuple[bool, list[str]]:
    papers = load_json(PAPERS_PATH)
    errors: list[str] = []
    with tempfile.TemporaryDirectory() as temp_dir:
        output_root = Path(temp_dir)
        generate_all(papers, output_root)
        expected = output_file_map(output_root)
    actual = {f"site/{path}": content for path, content in output_file_map(ROOT / "site").items()}
    actual.update(
        {
            "README.md": README_EN_PATH.read_bytes(),
            "README.zh-CN.md": README_ZH_PATH.read_bytes(),
            "paper/references.bib": BIB_PATH.read_bytes(),
            "docs/evidence-matrix.md": EVIDENCE_MATRIX_PATH.read_bytes(),
            "docs/paper-index.md": PAPER_INDEX_PATH.read_bytes(),
            "docs/category-coverage.md": CATEGORY_COVERAGE_PATH.read_bytes(),
            "docs/foundations.md": FOUNDATIONS_DOC_PATH.read_bytes(),
        }
    )
    errors.extend(compare_file_maps(expected, actual, "generated output"))
    check_local_markdown_links(ROOT, errors)
    check_local_html_links(SITE_DIR, errors)
    return (not errors), errors


def migrate_taxonomy_tag(axis_map: dict[str, list[str]], tag: str) -> tuple[list[str], list[dict[str, str]]]:
    owners = [axis for axis, tags in axis_map.items() if tag in tags]
    if len(owners) == 1:
        return owners, []
    if len(owners) == 0:
        return [], [{"tag": tag, "reason": "tag not present in taxonomy"}]
    return [], [{"tag": tag, "reason": f"ambiguous across axes: {', '.join(owners)}"}]


def migrate_data(apply: bool = False) -> dict[str, Any]:
    papers = load_json(PAPERS_PATH)
    if not isinstance(papers, list):
        raise ManageError(f"{PAPERS_PATH}: root must be an array")
    axis_map, _ = taxonomy_axis_map()
    category_ids = display_category_ids()
    before = len(papers)
    changed = 0
    pending_total = 0
    for record in papers:
        if not isinstance(record, dict):
            raise ManageError(f"{PAPERS_PATH}: non-object record")
        record_changed = False
        old_tags = record.get("taxonomy_tags")
        if isinstance(old_tags, list):
            new_tags: dict[str, list[str]] = {}
            pending: list[dict[str, str]] = []
            for tag in old_tags:
                owners, notes = migrate_taxonomy_tag(axis_map, str(tag))
                for owner in owners:
                    new_tags.setdefault(owner, [])
                    if tag not in new_tags[owner]:
                        new_tags[owner].append(tag)
                pending.extend(notes)
            for axis in new_tags:
                new_tags[axis].sort()
            record["taxonomy_tags"] = new_tags
            record["taxonomy_migration_pending"] = record.get("taxonomy_migration_pending", []) + pending
            pending_total += len(pending)
            record_changed = True
        elif not isinstance(old_tags, dict):
            raise ManageError(f"{PAPERS_PATH}: record {record.get('id')}: cannot migrate taxonomy_tags {old_tags!r}")

        if "evidence" in record and "evidence_legacy" not in record:
            record["evidence_legacy"] = record.get("evidence")
            record_changed = True
        record.pop("evidence", None)
        if "evidence_items" not in record:
            item = {
                "source_url": record.get("canonical_url"),
                "source_kind": "abstract",
                "source_version": "arxiv-abstract",
                "locator": None,
                "supports_fields": ["metadata"],
                "claim": record.get("evidence_legacy") or "Seed metadata inspected at abstract level.",
                "attribution": "unverified" if record.get("metadata_status") == "unverified" else "reviewer_synthesis",
                "accessed_at": record.get("checked_at"),
            }
            record["evidence_items"] = [item]
            record_changed = True

        if "bibliography_type" not in record:
            record["bibliography_type"] = "misc"
            if record.get("record_type") == "survey" and record.get("publication_status") == "published":
                record["bibliography_type"] = "article"
            if record.get("record_type") == "method" and "NeurIPS" in str(record.get("venue") or ""):
                record["bibliography_type"] = "inproceedings"
            record_changed = True
        if "metadata_conflict_scope" not in record:
            if record.get("metadata_status") == "conflict":
                record["metadata_conflict_scope"] = ["venue", "doi", "publication_status"]
            else:
                record["metadata_conflict_scope"] = []
            record_changed = True

        if "primary_category" not in record:
            record["primary_category"] = None
            record_changed = True
        elif record["primary_category"] not in category_ids and record["primary_category"] is not None:
            raise ManageError(
                f"{PAPERS_PATH}: record {record.get('id')}: unknown primary_category {record['primary_category']!r}"
            )

        if "secondary_categories" not in record:
            record["secondary_categories"] = []
            record_changed = True
        elif isinstance(record["secondary_categories"], list):
            deduped: list[str] = []
            seen_secondary: set[str] = set()
            for category_id in record["secondary_categories"]:
                if category_id not in category_ids:
                    raise ManageError(
                        f"{PAPERS_PATH}: record {record.get('id')}: unknown secondary category {category_id!r}"
                    )
                if category_id not in seen_secondary:
                    deduped.append(category_id)
                    seen_secondary.add(category_id)
            if deduped != record["secondary_categories"]:
                record["secondary_categories"] = deduped
                record_changed = True

        if "classification_rationale" not in record:
            if record.get("exclusion_reason"):
                rationale = f"Auxiliary/excluded record: {record['exclusion_reason']}"
            elif record.get("inclusion_rationale"):
                rationale = f"Tentative classification from existing evidence: {record['inclusion_rationale']}"
            else:
                rationale = "Not yet classified into a UAV display theme."
            record["classification_rationale"] = rationale
            record_changed = True

        if "classification_evidence_refs" not in record:
            refs = [
                item.get("source_url")
                for item in record.get("evidence_items", [])
                if isinstance(item, dict) and item.get("source_url")
            ]
            record["classification_evidence_refs"] = refs
            record_changed = True

        if "classification_status" not in record:
            record["classification_status"] = "provisional"
            record_changed = True

        if record.get("primary_category") in record.get("secondary_categories", []):
            raise ManageError(
                f"{PAPERS_PATH}: record {record.get('id')}: primary_category must not appear in secondary_categories"
            )

        changed += int(record_changed)

    result = {
        "before": before,
        "after": len(papers),
        "changed": changed,
        "pending_total": pending_total,
        "records": papers,
    }
    if apply:
        write_text(PAPERS_PATH, json.dumps(papers, ensure_ascii=False, indent=2) + "\n")
    return result


def print_errors(title: str, errors: Iterable[str]) -> None:
    print(title)
    for error in errors:
        print(f"  - {error}")


def command_validate() -> int:
    ok, errors = validate_data()
    if not ok:
        print_errors("Validation failed:", errors)
        return 1
    papers = load_json(PAPERS_PATH)
    stats = papers_stats(papers)
    print("Validation passed.")
    foundations = load_foundational_resources()
    print(
        "  records={} candidates={} fulltext_reviewed={} core_methods={} unique_seed_studies={} foundations={} migration_pending={}".format(
            stats["total"],
            stats["candidates"],
            stats["fulltext_reviewed"],
            stats["core_methods"],
            stats["unique_seed_studies"],
            len(foundations),
            stats["migration_pending"],
        )
    )
    return 0


def command_migrate(apply: bool) -> int:
    result = migrate_data(apply=apply)
    print(
        "Migration {}: before={} after={} changed={} pending={}".format(
            "applied" if apply else "dry-run",
            result["before"],
            result["after"],
            result["changed"],
            result["pending_total"],
        )
    )
    if apply:
        print("Migration applied to papers.json. Run validate next.")
    else:
        print("Dry run only; no files changed.")
    return 0


def command_build() -> int:
    ok, errors = validate_data()
    if not ok:
        print_errors("Cannot build; validation failed:", errors)
        return 1
    try:
        build_project()
    except ManageError as exc:
        print(f"Build failed: {exc}")
        return 1
    print("Build completed.")
    return 0


def command_check(tracked_only: bool = False) -> int:
    ok, validation_errors = validate_data()
    if not ok:
        print_errors("Check failed; validation errors:", validation_errors)
        return 1
    try:
        ok, sync_errors = compare_tracked() if tracked_only else compare_expected_with_actual()
    except ManageError as exc:
        print(f"Check failed: {exc}")
        return 1
    if not ok:
        mode = "tracked generated files" if tracked_only else "generated files and local links"
        print_errors(f"Check failed; {mode} are out of sync:", sync_errors)
        return 1
    mode = "tracked generated files" if tracked_only else "generated files and local links"
    print(f"Check passed; {mode} are in sync.")
    return 0


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:
        return


def command_serve(port: int) -> int:
    ok, errors = validate_data()
    if not ok:
        print_errors("Cannot serve; validation failed:", errors)
        return 1
    try:
        build_project()
    except ManageError as exc:
        print(f"Cannot build site for preview: {exc}")
        return 1
    if not (SITE_DIR / "index.html").exists():
        print(f"Missing generated site entry: {SITE_DIR / 'index.html'}")
        return 1
    handler = lambda *args, **kwargs: QuietHandler(*args, directory=str(SITE_DIR), **kwargs)
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    print(f"Serving {SITE_DIR} at http://127.0.0.1:{port}/")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
    finally:
        server.server_close()
    return 0


def fetch_link_status(url: str) -> tuple[str, Any]:
    headers = {
        "User-Agent": "UAVs-Meet-Neuro-Symbolic-AI-Link-Check/0.1",
        "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
    }
    request = urllib.request.Request(url, headers=headers, method="HEAD")
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=12) as response:
                return str(url), response.status
        except urllib.error.HTTPError as exc:
            if exc.code == 405 and request.get_method() == "HEAD":
                request = urllib.request.Request(url, headers=headers, method="GET")
                continue
            if exc.code in {429, 500, 502, 503, 504} and attempt < 2:
                time.sleep(0.5 * (attempt + 1))
                continue
            return str(url), exc.code
        except (urllib.error.URLError, TimeoutError, socket.timeout) as exc:
            last_error = exc
            if attempt < 2:
                time.sleep(0.5 * (attempt + 1))
                continue
        except Exception as exc:  # keep the command resilient
            last_error = exc
            break
    reason = getattr(last_error, "reason", str(last_error) if last_error else "unknown")
    return str(url), f"error:{reason}"


def command_check_links() -> int:
    papers = load_json(PAPERS_PATH)
    references = load_json(DATA_DIR / "reference-sources.json")
    urls: list[tuple[str, str]] = []
    for record in papers:
        if record.get("canonical_url"):
            urls.append((record.get("id", "paper"), record["canonical_url"]))
        if record.get("code_url"):
            urls.append((record.get("id", "paper"), record["code_url"]))
    if isinstance(references, list):
        for source in references:
            if isinstance(source, dict) and source.get("url"):
                urls.append((source.get("id", "reference"), source["url"]))

    deduped: list[tuple[str, str]] = []
    seen: set[str] = set()
    for label, url in urls:
        if url not in seen:
            seen.add(url)
            deduped.append((label, url))

    print("Checking external links (this may take a while)...")
    for index, (label, url) in enumerate(deduped):
        _, status = fetch_link_status(url)
        print(f"{label}\t{status}\t{url}")
        if index < len(deduped) - 1:
            time.sleep(0.2)
    print("Link check finished. Results are informational and do not modify paper statuses.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Maintain the UAV neuro-symbolic review knowledge base.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate", help="Validate JSON data, enums, IDs, tags, and status consistency.")
    subparsers.add_parser("build", help="Generate README blocks, evidence matrix, references.bib, and the static site.")
    check_parser = subparsers.add_parser("check", help="Validate data and check generated outputs against source data.")
    check_parser.add_argument("--tracked-only", action="store_true", help="Only check tracked generated files; site/ is not required.")
    subparsers.add_parser("check-links", help="Optionally check external links over the network.")
    migrate_parser = subparsers.add_parser("migrate-data", help="Migrate legacy flat taxonomy/evidence fields.")
    migrate_parser.add_argument("--apply", action="store_true", help="Write migrated data; default is dry-run.")
    serve_parser = subparsers.add_parser("serve", help="Build and serve the generated site locally.")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port to bind on 127.0.0.1 (default: 8000).")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "validate":
        return command_validate()
    if args.command == "build":
        return command_build()
    if args.command == "check":
        return command_check(tracked_only=args.tracked_only)
    if args.command == "check-links":
        return command_check_links()
    if args.command == "migrate-data":
        return command_migrate(apply=args.apply)
    if args.command == "serve":
        return command_serve(args.port)
    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
