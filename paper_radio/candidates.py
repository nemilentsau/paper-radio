import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from paper_radio.papers import PaperRecord


@dataclass(frozen=True)
class CandidatePaths:
    json_path: Path
    markdown_path: Path


def _candidate_record(paper: PaperRecord) -> dict[str, Any]:
    data = paper.to_dict()
    data["candidate_score"] = None
    data["decision"] = "untriaged"
    return data


def _render_candidate_markdown(source: str, run_date: str, candidates: list[dict[str, Any]]) -> str:
    lines = [
        f"# {source} Candidates For {run_date}",
        "",
    ]
    for candidate in candidates:
        affiliations = ", ".join(candidate.get("author_affiliations", []))
        trusted_orgs = ", ".join(candidate.get("trusted_orgs", []))
        lines.extend(
            [
                f"## {candidate['paper_id']}: {candidate['title']}",
                "",
                f"- Categories: {', '.join(candidate['categories'])}",
                f"- Authors: {', '.join(candidate['authors'])}",
                f"- Author affiliations: {affiliations or 'unknown'}",
                f"- Trusted org matches: {trusted_orgs or 'none'}",
                f"- Abstract URL: {candidate['abs_url']}",
                f"- PDF URL: {candidate['pdf_url']}",
                "",
                str(candidate["abstract"]),
                "",
            ]
        )
    return "\n".join(lines)


def write_candidate_batch(root: Path, run_date: str, source: str, papers: list[PaperRecord]) -> CandidatePaths:
    output_dir = root / "data" / "candidates" / run_date
    json_path = output_dir / f"{source}.json"
    markdown_path = output_dir / f"{source}.md"
    candidates = [_candidate_record(paper) for paper in papers]
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(candidates, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_path.write_text(_render_candidate_markdown(source, run_date, candidates), encoding="utf-8")
    return CandidatePaths(json_path=json_path, markdown_path=markdown_path)
