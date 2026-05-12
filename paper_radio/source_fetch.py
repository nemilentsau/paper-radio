from collections.abc import Callable
from dataclasses import dataclass, replace
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

from pypdf import PdfReader

from paper_radio.papers import PaperRecord, load_paper_record, write_paper_record

MIN_FULL_TEXT_CHARS = 1000


class SourceFetchError(RuntimeError):
    pass


@dataclass(frozen=True)
class PaperSourcePaths:
    pdf_path: Path
    full_text_path: Path


def _relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def paper_pdf_path(root: Path, paper_id: str) -> Path:
    return root / "data" / "papers" / "pdfs" / f"{paper_id}.pdf"


def paper_full_text_path(root: Path, paper_id: str) -> Path:
    return root / "data" / "papers" / "fulltext" / f"{paper_id}.txt"


def download_pdf_bytes(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "paper-radio/0.1"})
    with urlopen(request, timeout=60) as response:
        data = response.read()
    if not data.startswith(b"%PDF"):
        raise SourceFetchError(f"Downloaded source from {url} is not a PDF")
    return data


def extract_pdf_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    page_text = [page.extract_text() or "" for page in reader.pages]
    return "\n\n".join(text.strip() for text in page_text if text.strip())


def _write_atomic(path: Path, data: bytes | str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    if isinstance(data, bytes):
        temporary_path.write_bytes(data)
    else:
        temporary_path.write_text(data, encoding="utf-8")
    temporary_path.replace(path)


def _validate_full_text(text: str, paper_id: str) -> None:
    if len(text.strip()) < MIN_FULL_TEXT_CHARS:
        raise SourceFetchError(
            f"Extracted full text for {paper_id} is too short; refusing to review abstract-only source"
        )


def fetch_paper_source(
    root: Path,
    paper_id: str,
    fetch_pdf_bytes: Callable[[str], bytes] = download_pdf_bytes,
    extract_pdf_text: Callable[[Path], str] = extract_pdf_text,
) -> PaperSourcePaths:
    paper = load_paper_record(root, paper_id)
    pdf_path = paper_pdf_path(root, paper_id)
    full_text_path = paper_full_text_path(root, paper_id)
    try:
        pdf_bytes = fetch_pdf_bytes(paper.pdf_url)
    except (OSError, URLError, SourceFetchError) as error:
        raise SourceFetchError(f"Failed to fetch PDF for {paper_id} from {paper.pdf_url}: {error}") from error

    _write_atomic(pdf_path, pdf_bytes)
    try:
        full_text = extract_pdf_text(pdf_path)
        _validate_full_text(full_text, paper_id)
    except Exception as error:
        if isinstance(error, SourceFetchError):
            raise
        raise SourceFetchError(f"Failed to extract full text for {paper_id}: {error}") from error

    _write_atomic(full_text_path, full_text.rstrip() + "\n")
    write_paper_record(
        root,
        replace(
            paper,
            local_pdf_path=_relative(root, pdf_path),
            full_text_path=_relative(root, full_text_path),
        ),
    )
    return PaperSourcePaths(pdf_path=pdf_path, full_text_path=full_text_path)


def validate_full_text_source(root: Path, paper: PaperRecord) -> str:
    if not paper.full_text_path:
        raise RuntimeError(f"{paper.paper_id} full-text source is missing; run `fetch-sources` before reviews")
    path = root / paper.full_text_path
    if not path.exists():
        raise RuntimeError(f"{paper.paper_id} full-text source is missing at {paper.full_text_path}")
    text = path.read_text(encoding="utf-8")
    _validate_full_text(text, paper.paper_id)
    return paper.full_text_path


def validate_review_job_sources(root: Path, job: dict[str, object]) -> None:
    if str(job.get("kind", "")) != "review":
        return
    raw_input_paths = job.get("input_paths", [])
    input_paths = [str(path) for path in raw_input_paths] if isinstance(raw_input_paths, list) else []
    full_text_inputs = [path for path in input_paths if path.startswith("data/papers/fulltext/")]
    if not full_text_inputs:
        raise RuntimeError(f"{job.get('job_id', 'review job')} has no full-text source input")
    for input_path in full_text_inputs:
        path = root / input_path
        if not path.exists():
            raise RuntimeError(f"{job.get('job_id', 'review job')} full-text source is missing at {input_path}")
        _validate_full_text(path.read_text(encoding="utf-8"), str(job.get("paper_id", "unknown")))
