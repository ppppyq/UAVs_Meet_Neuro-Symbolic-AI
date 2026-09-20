#!/usr/bin/env python3
"""Maintenance commands for the UAV neuro-symbolic review knowledge base.

This script intentionally uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import html
import http.server
import json
import os
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

PAPERS_PATH = DATA_DIR / "papers.json"
TAXONOMY_PATH = DATA_DIR / "taxonomy.json"
README_EN_PATH = ROOT / "README.md"
README_ZH_PATH = ROOT / "README.zh-CN.md"
BIB_PATH = PAPER_DIR / "references.bib"

OVERVIEW_MARKER_START = "<!-- BEGIN GENERATED:OVERVIEW -->"
OVERVIEW_MARKER_END = "<!-- END GENERATED:OVERVIEW -->"
PAPER_TABLE_MARKER_START = "<!-- BEGIN GENERATED:PAPER-TABLE -->"
PAPER_TABLE_MARKER_END = "<!-- END GENERATED:PAPER-TABLE -->"

VALID_METADATA_STATUS = {"unverified", "verified", "conflict"}
VALID_READING_STATUS = {"unread", "abstract_reviewed", "fulltext_reviewed"}
VALID_SCREENING_STATUS = {"candidate", "included", "excluded"}
VALID_RELEVANCE = {"direct_uav", "transferable", "related_survey", "background"}
VALID_RECORD_TYPE = {"survey", "dataset", "benchmark", "method", "position", "other"}
VALID_PUBLICATION_STATUS = {"preprint", "published", "withdrawn", "conflict", "unknown"}
VALID_UAV_EVIDENCE = {"conceptual", "simulation", "hardware_in_loop", "real_flight", "none", "unknown"}
VALID_RELATION = {"supersedes", "superseded_by", "earlier_version", "later_version", "same_work", "other"}

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
    "uav_evidence",
    "summary",
    "limitations",
    "evidence",
    "checked_at",
}


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


def is_http_url(value: Any) -> bool:
    if not value:
        return True
    if not isinstance(value, str):
        return False
    try:
        parsed = urllib.parse.urlparse(value)
    except ValueError:
        return False
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def collect_taxonomy_tags() -> tuple[set[str], set[str]]:
    taxonomy = load_json(TAXONOMY_PATH)
    if not isinstance(taxonomy, dict):
        raise ManageError(f"{TAXONOMY_PATH}: root must be an object")
    axes = taxonomy.get("axes")
    if not isinstance(axes, list) or not axes:
        raise ManageError(f"{TAXONOMY_PATH}: missing non-empty axes array")
    axis_ids: set[str] = set()
    tag_ids: set[str] = set()
    tag_axis: dict[str, str] = {}
    for axis in axes:
        if not isinstance(axis, dict):
            raise ManageError(f"{TAXONOMY_PATH}: axis must be an object")
        axis_id = axis.get("id")
        if not isinstance(axis_id, str) or not axis_id:
            raise ManageError(f"{TAXONOMY_PATH}: axis id is missing")
        if axis_id in axis_ids:
            raise ManageError(f"{TAXONOMY_PATH}: duplicate axis id {axis_id}")
        axis_ids.add(axis_id)
        tags = axis.get("tags")
        if not isinstance(tags, list) or not tags:
            raise ManageError(f"{TAXONOMY_PATH}: axis {axis_id} has no tags")
        for tag in tags:
            if not isinstance(tag, dict):
                raise ManageError(f"{TAXONOMY_PATH}: tag in {axis_id} must be an object")
            tag_id = tag.get("id")
            if not isinstance(tag_id, str) or not tag_id:
                raise ManageError(f"{TAXONOMY_PATH}: tag id is missing in {axis_id}")
            if tag_id in tag_axis and tag_axis[tag_id] == axis_id:
                raise ManageError(f"{TAXONOMY_PATH}: duplicate taxonomy tag id {tag_id} in axis {axis_id}")
            tag_axis.setdefault(tag_id, axis_id)
            tag_ids.add(tag_id)
    return axis_ids, tag_ids


def validate_data() -> tuple[bool, list[str]]:
    errors: list[str] = []
    try:
        papers = load_json(PAPERS_PATH)
        _, taxonomy_tags = collect_taxonomy_tags()
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
        if not isinstance(authors, list) or not authors or not all(isinstance(a, str) and a.strip() for a in authors):
            errors.append(f"{PAPERS_PATH}: {location}: authors must be a non-empty array of strings")

        if not isinstance(record.get("year"), int) or record.get("year") <= 0:
            errors.append(f"{PAPERS_PATH}: {location}: year must be a positive integer")

        if not is_http_url(record.get("canonical_url")):
            errors.append(f"{PAPERS_PATH}: {location}: canonical_url must be an http(s) URL")
        if not is_http_url(record.get("code_url")):
            errors.append(f"{PAPERS_PATH}: {location}: code_url must be an http(s) URL or null")

        enum_checks = [
            ("metadata_status", record.get("metadata_status"), VALID_METADATA_STATUS),
            ("reading_status", record.get("reading_status"), VALID_READING_STATUS),
            ("screening_status", record.get("screening_status"), VALID_SCREENING_STATUS),
            ("relevance", record.get("relevance"), VALID_RELEVANCE),
            ("record_type", record.get("record_type"), VALID_RECORD_TYPE),
            ("publication_status", record.get("publication_status"), VALID_PUBLICATION_STATUS),
        ]
        for field_name, value, allowed in enum_checks:
            if value not in allowed:
                errors.append(
                    f"{PAPERS_PATH}: {location}: {field_name} must be one of {sorted(allowed)}, got {value!r}"
                )

        if not isinstance(record.get("human_reviewed"), bool):
            errors.append(f"{PAPERS_PATH}: {location}: human_reviewed must be a boolean")

        related_versions = record.get("related_versions")
        if not isinstance(related_versions, list):
            errors.append(f"{PAPERS_PATH}: {location}: related_versions must be an array")
        else:
            for rel in related_versions:
                if not isinstance(rel, dict):
                    errors.append(f"{PAPERS_PATH}: {location}: related_versions entries must be objects")
                    continue
                if not isinstance(rel.get("id"), str) or not rel.get("id"):
                    errors.append(f"{PAPERS_PATH}: {location}: related_versions entry has invalid id")
                if rel.get("relation") not in VALID_RELATION:
                    errors.append(
                        f"{PAPERS_PATH}: {location}: related_versions relation must be one of {sorted(VALID_RELATION)}"
                    )

        tags = record.get("taxonomy_tags")
        if not isinstance(tags, list):
            errors.append(f"{PAPERS_PATH}: {location}: taxonomy_tags must be an array")
        else:
            for tag in tags:
                if not isinstance(tag, str) or tag not in taxonomy_tags:
                    errors.append(f"{PAPERS_PATH}: {location}: unknown taxonomy tag {tag!r}")

        evidence = record.get("uav_evidence")
        if not isinstance(evidence, list):
            errors.append(f"{PAPERS_PATH}: {location}: uav_evidence must be an array")
        else:
            for item in evidence:
                if item not in VALID_UAV_EVIDENCE:
                    errors.append(f"{PAPERS_PATH}: {location}: invalid uav_evidence value {item!r}")
            if "none" in evidence and len(evidence) > 1:
                errors.append(f"{PAPERS_PATH}: {location}: uav_evidence 'none' cannot be combined with other values")

        arxiv = normalize_arxiv_id(record.get("arxiv_id"))
        doi = normalize_doi(record.get("doi"))
        if arxiv:
            if arxiv in seen_arxiv and seen_arxiv[arxiv] != record_id:
                errors.append(
                    f"{PAPERS_PATH}: {location}: duplicate normalized arXiv ID {arxiv} "
                    f"(also used by {seen_arxiv[arxiv]})"
                )
            elif arxiv not in seen_arxiv:
                seen_arxiv[arxiv] = record_id or ""
        if doi:
            if doi in seen_doi and seen_doi[doi] != record_id:
                errors.append(
                    f"{PAPERS_PATH}: {location}: duplicate normalized DOI {doi} "
                    f"(also used by {seen_doi[doi]})"
                )
            elif doi not in seen_doi:
                seen_doi[doi] = record_id or ""

        if record.get("publication_status") == "withdrawn" and record.get("screening_status") == "included":
            errors.append(f"{PAPERS_PATH}: {location}: a withdrawn record cannot be included")

        if record.get("screening_status") == "included":
            if record.get("relevance") != "direct_uav":
                errors.append(f"{PAPERS_PATH}: {location}: included records must have relevance=direct_uav")
            if record.get("record_type") != "method":
                errors.append(f"{PAPERS_PATH}: {location}: included records must have record_type=method")
            for field in ("neural_component", "symbolic_component", "coupling_mechanism", "evidence"):
                value = record.get(field)
                if not isinstance(value, str) or not value.strip():
                    errors.append(
                        f"{PAPERS_PATH}: {location}: included core method requires non-empty {field}"
                    )

    for record in papers:
        if not isinstance(record, dict):
            continue
        location = f"record {record.get('id', '?')}"
        for rel in record.get("related_versions", []):
            if isinstance(rel, dict) and rel.get("id") and rel["id"] not in records_by_id:
                errors.append(f"{PAPERS_PATH}: {location}: related_versions points to missing id {rel['id']}")

    return (not errors), errors


def count_core_methods(papers: list[dict[str, Any]]) -> int:
    seen_work_ids: set[str] = set()
    count = 0
    for record in papers:
        if (
            record.get("screening_status") == "included"
            and record.get("relevance") == "direct_uav"
            and record.get("record_type") == "method"
            and record.get("publication_status") != "withdrawn"
        ):
            work_id = str(record.get("work_id") or record.get("id"))
            if work_id not in seen_work_ids:
                seen_work_ids.add(work_id)
                count += 1
    return count


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


def render_bibtex(records: list[dict[str, Any]]) -> str:
    entries: list[str] = []
    for record in records:
        if record.get("metadata_status") != "verified":
            continue
        if record.get("publication_status") == "withdrawn":
            continue

        key = bibtex_key(record)
        authors = " and ".join(bibtex_escape(a) for a in record.get("authors", []))
        title = bibtex_escape(record.get("title", ""))
        year = record.get("year", "")
        arxiv_id = record.get("arxiv_id") or ""
        canonical_url = record.get("canonical_url") or ""
        doi = record.get("doi") or ""
        code_url = record.get("code_url") or ""
        note_parts: list[str] = []
        if code_url:
            note_parts.append(f"Code: {bibtex_escape(code_url)}")
        note = ", ".join(note_parts)

        if record.get("publication_status") == "published" and record.get("record_type") == "method":
            if "NeurIPS" in str(record.get("venue") or ""):
                entry_type = "inproceedings"
                venue_field = "booktitle"
            else:
                entry_type = "article"
                venue_field = "journal"
            lines = [f"@{entry_type}{{{key},", f"  title = {{{title}}},"]
            if authors:
                lines.append(f"  author = {{{authors}}},")
            lines.append(f"  year = {{{year}}},")
            if record.get("venue"):
                lines.append(f"  {venue_field} = {{{bibtex_escape(record.get('venue'))}}},")
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
        lines.append(f"  year = {{{year}}},")
        if arxiv_id:
            lines.append(f"  eprint = {{{bibtex_escape(arxiv_id)}}},")
            lines.append("  archivePrefix = {arXiv},")
        if doi:
            lines.append(f"  doi = {{{bibtex_escape(doi)}}},")
        if record.get("venue"):
            lines.append(f"  howpublished = {{{bibtex_escape(record.get('venue'))}}},")
        if canonical_url:
            lines.append(f"  url = {{{bibtex_escape(canonical_url)}}},")
        if note:
            lines.append(f"  note = {{{note}}},")
        lines.append("}")
        entries.append("\n".join(lines))

    return "\n\n".join(entries) + ("\n" if entries else "")


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
            f"- 撤回/版本关联条目：{stats['withdrawn']}\n"
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
        f"- Withdrawn/version-linked records: {stats['withdrawn']}\n"
    )


def paper_table_markdown(records: list[dict[str, Any]]) -> str:
    headers = ["ID", "Title", "Authors", "Year", "Type", "Screening", "Relevance", "UAV evidence", "Canonical URL"]
    lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for record in records:
        authors = ", ".join(record.get("authors", []))
        canonical = record.get("canonical_url") or ""
        canonical_cell = f"[{markdown_escape(canonical)}]({canonical})" if canonical else ""
        row = [
            markdown_escape(record.get("id")),
            markdown_escape(record.get("title")),
            markdown_escape(authors),
            str(record.get("year") or ""),
            markdown_escape(record.get("record_type")),
            markdown_escape(record.get("screening_status")),
            markdown_escape(record.get("relevance")),
            ", ".join(markdown_escape(item) for item in record.get("uav_evidence", [])),
            canonical_cell,
        ]
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines) + "\n"


def overview_html(papers: list[dict[str, Any]]) -> str:
    stats = papers_stats(papers)
    rows = [
        ("Total records", str(stats["total"])),
        ("Metadata verified", str(stats["metadata_verified"])),
        ("Metadata conflicts", str(stats["metadata_conflict"])),
        ("Abstract-reviewed", str(stats["abstract_reviewed"])),
        ("Full-text reviewed", str(stats["fulltext_reviewed"])),
        ("Candidate records", str(stats["candidates"])),
        ("Direct UAV candidate methods", str(stats["direct_uav_candidates"])),
        ("Core UAV methods", str(stats["core_methods"])),
        ("Withdrawn records", str(stats["withdrawn"])),
    ]
    items = "\n".join(
        f"<dt>{html.escape(label)}</dt><dd>{html.escape(value)}</dd>" for label, value in rows
    )
    return f"<dl>\n{items}\n</dl>\n"


def paper_table_html(records: list[dict[str, Any]]) -> str:
    headers = ["Title", "Authors", "Year", "Type", "Status", "Relevance", "UAV evidence", "Links"]
    head = "".join(f"<th>{html.escape(value)}</th>" for value in headers)
    rows: list[str] = []
    for record in records:
        title = html.escape(record.get("title") or "")
        tags = "".join(
            f'<span class="tag">{html.escape(tag)}</span>' for tag in record.get("taxonomy_tags", [])
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
        status = record.get("screening_status") or ""
        row = "".join(
            [
                "<tr>",
                f"<td>{title_cell}</td>",
                f"<td>{authors}</td>",
                f"<td>{html.escape(str(record.get('year') or ''))}</td>",
                f"<td>{html.escape(record.get('record_type') or '')}</td>",
                f'<td><span class="status {html.escape(status)}">{html.escape(status)}</span></td>',
                f"<td>{html.escape(record.get('relevance') or '')}</td>",
                f"<td>{html.escape(', '.join(record.get('uav_evidence', [])))}</td>",
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
        PAPER_TABLE_MARKER_START,
        PAPER_TABLE_MARKER_END,
        paper_table_markdown(papers),
        str(source),
    )
    write_text(target, text)


def generate_site(papers: list[dict[str, Any]], output_dir: Path) -> None:
    template = (WEBSITE_DIR / "template.html").read_text(encoding="utf-8")
    paper_json = json.dumps(papers, ensure_ascii=False, sort_keys=True)
    paper_json = paper_json.replace("</", "<\\/")
    rendered = (
        template.replace("{{OVERVIEW_HTML}}", overview_html(papers))
        .replace("{{PAPER_TABLE_HTML}}", paper_table_html(papers))
        .replace("{{PAPER_DATA_JSON}}", paper_json)
    )
    if "{{" in rendered or "}}" in rendered:
        raise ManageError("website template still contains unreplaced placeholders")
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


def generate_all(papers: list[dict[str, Any]], output_root: Path) -> None:
    generate_readme(papers, README_EN_PATH, output_root / "README.md", "en")
    generate_readme(papers, README_ZH_PATH, output_root / "README.zh-CN.md", "zh")
    write_text(output_root / "paper" / "references.bib", render_bibtex(papers))
    generate_site(papers, output_root / "site")


def build_project() -> None:
    papers = load_json(PAPERS_PATH)
    generate_all(papers, ROOT)


def relative_local_path(path: Path, root: Path) -> str | None:
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return None


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


def compare_expected_with_actual() -> tuple[bool, list[str]]:
    papers = load_json(PAPERS_PATH)
    errors: list[str] = []
    with tempfile.TemporaryDirectory() as temp_dir:
        output_root = Path(temp_dir)
        generate_all(papers, output_root)

        expected_files = [
            output_root / "README.md",
            output_root / "README.zh-CN.md",
            output_root / "paper" / "references.bib",
            output_root / "site" / "index.html",
            output_root / "site" / "static" / "style.css",
            output_root / "site" / "static" / "app.js",
        ]
        actual_files = [
            README_EN_PATH,
            README_ZH_PATH,
            BIB_PATH,
            SITE_DIR / "index.html",
            SITE_DIR / "static" / "style.css",
            SITE_DIR / "static" / "app.js",
        ]
        for expected, actual in zip(expected_files, actual_files):
            if not actual.exists():
                errors.append(f"missing generated file: {actual}")
                continue
            expected_bytes = expected.read_bytes()
            actual_bytes = actual.read_bytes()
            if expected_bytes != actual_bytes:
                errors.append(f"generated file is out of sync: {actual}")

        for path in expected_files:
            if path.exists() and not path.is_file():
                errors.append(f"expected output is not a file: {path}")

    check_local_markdown_links(ROOT, errors)
    check_local_html_links(SITE_DIR, errors)
    return (not errors), errors


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
    print(f"  records={stats['total']} candidates={stats['candidates']} core_methods={stats['core_methods']}")
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


def command_check() -> int:
    ok, validation_errors = validate_data()
    if not ok:
        print_errors("Check failed; validation errors:", validation_errors)
        return 1
    try:
        ok, sync_errors = compare_expected_with_actual()
    except ManageError as exc:
        print(f"Check failed: {exc}")
        return 1
    if not ok:
        print_errors("Check failed; generated files are out of sync or local links are broken:", sync_errors)
        return 1
    print("Check passed; generated files are in sync and local links are present.")
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


def fetch_link_status(url: str) -> tuple[str, int | None]:
    headers = {
        "User-Agent": "UAVs-Meet-Neuro-Symbolic-AI-Link-Check/0.1",
        "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
    }
    request = urllib.request.Request(url, headers=headers, method="HEAD")
    status = None
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=12) as response:
                return str(url), response.status
        except urllib.error.HTTPError as exc:
            status = exc.code
            if exc.code in {405, 403, 429, 500, 502, 503, 504}:
                last_error = exc
                if exc.code == 405:
                    request = urllib.request.Request(url, headers=headers, method="GET")
                if attempt < 2 and exc.code in {429, 500, 502, 503, 504}:
                    time.sleep(0.5 * (attempt + 1))
                    continue
                return str(url), status
            return str(url), status
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
    subparsers.add_parser("build", help="Generate README blocks, references.bib, and the static site.")
    subparsers.add_parser("check", help="Validate data and check generated outputs against source data.")
    subparsers.add_parser("check-links", help="Optionally check external links over the network.")
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
        return command_check()
    if args.command == "check-links":
        return command_check_links()
    if args.command == "serve":
        return command_serve(args.port)
    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
