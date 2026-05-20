import json
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from paper_radio.papers import PaperRecord


@dataclass(frozen=True)
class CandidatePaths:
    json_path: Path
    markdown_path: Path


def _candidate_record(paper: PaperRecord, metadata: Mapping[str, Any] | None = None) -> dict[str, Any]:
    data = paper.to_dict()
    data["candidate_score"] = None
    data["decision"] = "untriaged"
    if metadata:
        data.update(metadata)
    return data


def _render_candidate_markdown(source: str, run_date: str, candidates: list[dict[str, Any]]) -> str:
    lines = [
        f"# {source} Candidates For {run_date}",
        "",
    ]
    for candidate in candidates:
        affiliations = ", ".join(candidate.get("author_affiliations", []))
        trusted_orgs = ", ".join(candidate.get("trusted_orgs", []))
        applied_domain = str(candidate.get("applied_domain_label", ""))
        applied_score = candidate.get("applied_domain_score")
        matched_keywords = ", ".join(candidate.get("matched_applied_keywords", []))
        matched_workflow_terms = ", ".join(candidate.get("matched_workflow_terms", []))
        lines.extend(
            [
                f"## {candidate['paper_id']}: {candidate['title']}",
                "",
                f"- Categories: {', '.join(candidate['categories'])}",
                f"- Authors: {', '.join(candidate['authors'])}",
                f"- Author affiliations: {affiliations or 'unknown'}",
                f"- Trusted org matches: {trusted_orgs or 'none'}",
                *(
                    [
                        f"- Applied domain: {applied_domain}",
                        f"- Applied-domain score: {applied_score}",
                        f"- Matched LLM/domain keywords: {matched_keywords or 'none'}",
                        f"- Matched workflow terms: {matched_workflow_terms or 'none'}",
                    ]
                    if applied_domain
                    else []
                ),
                f"- Abstract URL: {candidate['abs_url']}",
                f"- PDF URL: {candidate['pdf_url']}",
                "",
                str(candidate["abstract"]),
                "",
            ]
        )
    return "\n".join(lines)


def write_candidate_batch(
    root: Path,
    run_date: str,
    source: str,
    papers: list[PaperRecord],
    metadata_by_paper_id: Mapping[str, Mapping[str, Any]] | None = None,
) -> CandidatePaths:
    output_dir = root / "data" / "candidates" / run_date
    json_path = output_dir / f"{source}.json"
    markdown_path = output_dir / f"{source}.md"
    candidates = [
        _candidate_record(paper, (metadata_by_paper_id or {}).get(paper.paper_id))
        for paper in papers
    ]
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(candidates, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_path.write_text(_render_candidate_markdown(source, run_date, candidates), encoding="utf-8")
    return CandidatePaths(json_path=json_path, markdown_path=markdown_path)
