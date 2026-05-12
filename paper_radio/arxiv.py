from dataclasses import replace
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from xml.etree import ElementTree

from paper_radio.candidates import CandidatePaths, write_candidate_batch
from paper_radio.org_signals import annotate_trusted_orgs, load_trusted_orgs
from paper_radio.papers import PaperRecord, normalize_arxiv_paper_id, normalize_arxiv_source_id, write_paper_record

ARXIV_API_URL = "https://export.arxiv.org/api/query"
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


def build_arxiv_query_url(categories: list[str], max_results: int, start: int = 0) -> str:
    search_query = " OR ".join(f"cat:{category}" for category in categories)
    query = urlencode(
        {
            "search_query": search_query,
            "start": start,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
    )
    return f"{ARXIV_API_URL}?{query}"


def build_arxiv_id_url(arxiv_ids: list[str]) -> str:
    query = urlencode({"id_list": ",".join(arxiv_ids)})
    return f"{ARXIV_API_URL}?{query}"


def fetch_text(url: str) -> str:
    request = Request(url, headers={"User-Agent": "paper-radio/0.1 (mailto:local@example.invalid)"})
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def _text(entry: ElementTree.Element, tag: str) -> str:
    value = entry.findtext(f"atom:{tag}", default="", namespaces=ATOM_NS)
    return " ".join(value.split())


def _entry_source_id(entry: ElementTree.Element) -> str:
    entry_id = _text(entry, "id")
    source_id = entry_id.rsplit("/", 1)[-1]
    return normalize_arxiv_source_id(source_id)


def _entry_abs_url(source_id: str) -> str:
    return f"https://arxiv.org/abs/{source_id}"


def _entry_pdf_url(source_id: str) -> str:
    return f"https://arxiv.org/pdf/{source_id}"


def _entry_author_affiliations(entry: ElementTree.Element) -> tuple[str, ...]:
    affiliations: list[str] = []
    for author in entry.findall("atom:author", ATOM_NS):
        affiliation = author.findtext("arxiv:affiliation", default="", namespaces=ATOM_NS)
        if affiliation:
            affiliations.append(" ".join(affiliation.split()))
    return tuple(dict.fromkeys(affiliations))


def parse_arxiv_atom(xml_text: str, source_type: str) -> list[PaperRecord]:
    root = ElementTree.fromstring(xml_text)
    papers: list[PaperRecord] = []
    for entry in root.findall("atom:entry", ATOM_NS):
        source_id = _entry_source_id(entry)
        paper_id = normalize_arxiv_paper_id(source_id)
        authors = tuple(
            " ".join((author.findtext("atom:name", default="", namespaces=ATOM_NS) or "").split())
            for author in entry.findall("atom:author", ATOM_NS)
        )
        categories = tuple(
            str(category.attrib["term"])
            for category in entry.findall("atom:category", ATOM_NS)
            if category.attrib.get("term")
        )
        papers.append(
            PaperRecord(
                paper_id=paper_id,
                source="arxiv",
                source_id=source_id,
                title=_text(entry, "title"),
                authors=authors,
                author_affiliations=_entry_author_affiliations(entry),
                abstract=_text(entry, "summary"),
                published_at=_text(entry, "published"),
                updated_at=_text(entry, "updated"),
                categories=categories,
                pdf_url=_entry_pdf_url(source_id),
                abs_url=_entry_abs_url(source_id),
                source_types=(source_type,),
                status="candidate",
            )
        )
    return papers


def fetch_recent_candidates(root: Path, categories: list[str], max_results: int, run_date: str) -> CandidatePaths:
    xml_text = fetch_text(build_arxiv_query_url(categories=categories, max_results=max_results))
    trusted_orgs = load_trusted_orgs(root)
    papers = [
        annotate_trusted_orgs(paper, trusted_orgs)
        for paper in parse_arxiv_atom(xml_text, source_type="arxiv_recent")
    ]
    return write_candidate_batch(root, run_date=run_date, source="arxiv", papers=papers)


def ingest_arxiv_ids(root: Path, arxiv_ids: list[str]) -> list[PaperRecord]:
    xml_text = fetch_text(build_arxiv_id_url(arxiv_ids))
    trusted_orgs = load_trusted_orgs(root)
    papers = [
        annotate_trusted_orgs(replace(paper, source_types=("arxiv",), status="ingested"), trusted_orgs)
        for paper in parse_arxiv_atom(xml_text, source_type="arxiv")
    ]
    for paper in papers:
        write_paper_record(root, paper)
    return papers
