import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class PaperPaths:
    json_path: Path
    markdown_path: Path


@dataclass(frozen=True)
class PaperRecord:
    paper_id: str
    source: str
    source_id: str
    title: str
    authors: tuple[str, ...]
    abstract: str
    published_at: str
    updated_at: str
    categories: tuple[str, ...]
    pdf_url: str
    abs_url: str
    source_types: tuple[str, ...]
    status: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "paper_id": self.paper_id,
            "source": self.source,
            "source_id": self.source_id,
            "title": self.title,
            "authors": list(self.authors),
            "abstract": self.abstract,
            "published_at": self.published_at,
            "updated_at": self.updated_at,
            "categories": list(self.categories),
            "pdf_url": self.pdf_url,
            "abs_url": self.abs_url,
            "source_types": list(self.source_types),
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PaperRecord":
        return cls(
            paper_id=str(data["paper_id"]),
            source=str(data["source"]),
            source_id=str(data["source_id"]),
            title=str(data["title"]),
            authors=tuple(str(author) for author in data["authors"]),
            abstract=str(data["abstract"]),
            published_at=str(data["published_at"]),
            updated_at=str(data["updated_at"]),
            categories=tuple(str(category) for category in data["categories"]),
            pdf_url=str(data["pdf_url"]),
            abs_url=str(data["abs_url"]),
            source_types=tuple(str(source_type) for source_type in data["source_types"]),
            status=str(data["status"]),
        )


def normalize_arxiv_source_id(arxiv_id: str) -> str:
    cleaned = arxiv_id.strip()
    cleaned = cleaned.removeprefix("arxiv:")
    cleaned = re.sub(r"v\d+$", "", cleaned)
    return cleaned


def normalize_arxiv_paper_id(arxiv_id: str) -> str:
    source_id = normalize_arxiv_source_id(arxiv_id)
    return f"arxiv-{source_id.replace('/', '-')}"


def paper_json_path(root: Path, paper_id: str) -> Path:
    return root / "data" / "papers" / f"{paper_id}.json"


def paper_markdown_path(root: Path, paper_id: str) -> Path:
    return root / "data" / "papers" / f"{paper_id}.md"


def render_paper_markdown(paper: PaperRecord) -> str:
    authors = ", ".join(paper.authors)
    categories = ", ".join(paper.categories)
    source_types = ", ".join(paper.source_types)
    return "\n".join(
        [
            f"# {paper.title}",
            "",
            "## Metadata",
            f"- Paper ID: {paper.paper_id}",
            f"- Source: {paper.source}",
            f"- Source ID: {paper.source_id}",
            f"- Authors: {authors}",
            f"- Published: {paper.published_at}",
            f"- Updated: {paper.updated_at}",
            f"- Categories: {categories}",
            f"- Source signals: {source_types}",
            f"- Abstract URL: {paper.abs_url}",
            f"- PDF URL: {paper.pdf_url}",
            "",
            "## Abstract",
            paper.abstract,
            "",
        ]
    )


def write_paper_record(root: Path, paper: PaperRecord) -> PaperPaths:
    json_path = paper_json_path(root, paper.paper_id)
    markdown_path = paper_markdown_path(root, paper.paper_id)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(paper.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_path.write_text(render_paper_markdown(paper), encoding="utf-8")
    return PaperPaths(json_path=json_path, markdown_path=markdown_path)


def load_paper_record(root: Path, paper_id: str) -> PaperRecord:
    return PaperRecord.from_dict(json.loads(paper_json_path(root, paper_id).read_text(encoding="utf-8")))
