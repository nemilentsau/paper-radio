from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

from paper_radio.arxiv import build_arxiv_query_url, fetch_text, parse_arxiv_atom
from paper_radio.candidates import CandidatePaths, write_candidate_batch
from paper_radio.org_signals import annotate_trusted_orgs, load_trusted_orgs
from paper_radio.papers import PaperRecord


@dataclass(frozen=True)
class AppliedDomainPreset:
    name: str
    label: str
    categories: tuple[str, ...]
    keywords: tuple[str, ...]
    workflow_terms: tuple[str, ...]


APPLIED_DOMAIN_PRESETS: dict[str, AppliedDomainPreset] = {
    "bio_medicine": AppliedDomainPreset(
        name="bio_medicine",
        label="Bio, medicine, and clinical workflows",
        categories=("q-bio.QM", "q-bio.GN", "q-bio.NC", "cs.CL", "cs.AI", "cs.CV", "stat.ML"),
        keywords=(
            "large language model",
            "llm",
            "clinical",
            "ehr",
            "medical",
            "radiology",
            "biomedical",
            "rag",
            "retrieval",
            "foundation model",
            "multimodal",
        ),
        workflow_terms=(
            "diagnosis",
            "decision support",
            "evidence",
            "extraction",
            "workflow",
            "expert",
            "patient",
            "records",
            "literature",
        ),
    ),
    "chemistry_materials": AppliedDomainPreset(
        name="chemistry_materials",
        label="Chemistry and materials workflows",
        categories=("physics.chem-ph", "cond-mat.mtrl-sci", "cs.LG", "stat.ML"),
        keywords=(
            "large language model",
            "llm",
            "molecule",
            "materials",
            "chemistry",
            "reaction",
            "synthesis",
            "lab",
            "agent",
            "foundation model",
        ),
        workflow_terms=("protocol", "experiment", "optimization", "planning", "screening", "property", "design"),
    ),
    "finance_modeling": AppliedDomainPreset(
        name="finance_modeling",
        label="Finance and economic modeling workflows",
        categories=("q-fin.CP", "q-fin.EC", "q-fin.GN", "q-fin.PM", "q-fin.RM", "econ.EM", "stat.ML", "cs.AI"),
        keywords=(
            "large language model",
            "llm",
            "financial",
            "finance",
            "forecasting",
            "portfolio",
            "risk",
            "market",
            "backtesting",
            "economic",
            "econometric",
            "agent",
        ),
        workflow_terms=("forecast", "backtest", "regime", "portfolio", "risk", "analyst", "market", "trading"),
    ),
    "scientific_discovery": AppliedDomainPreset(
        name="scientific_discovery",
        label="Scientific literature and discovery workflows",
        categories=("cs.CL", "cs.AI", "cs.DL", "cs.IR", "stat.ML", "q-bio.QM"),
        keywords=(
            "large language model",
            "llm",
            "scientific discovery",
            "literature review",
            "hypothesis generation",
            "evidence synthesis",
            "knowledge discovery",
            "research agent",
            "foundation model",
            "retrieval",
            "rag",
        ),
        workflow_terms=("hypothesis", "evidence", "literature", "systematic review", "experiment", "expert", "search"),
    ),
}


def get_applied_domain_preset(name: str) -> AppliedDomainPreset:
    try:
        return APPLIED_DOMAIN_PRESETS[name]
    except KeyError as error:
        choices = ", ".join(sorted(APPLIED_DOMAIN_PRESETS))
        raise ValueError(f"Unknown applied-domain preset {name!r}. Expected one of: {choices}") from error


def _folded_text(paper: PaperRecord) -> str:
    return f"{paper.title}\n{paper.abstract}".casefold()


def _matched_terms(text: str, terms: tuple[str, ...]) -> list[str]:
    return [term for term in terms if term.casefold() in text]


def score_applied_domain_candidate(paper: PaperRecord, preset: AppliedDomainPreset) -> dict[str, Any]:
    text = _folded_text(paper)
    matched_keywords = _matched_terms(text, preset.keywords)
    matched_workflow_terms = _matched_terms(text, preset.workflow_terms)
    score = len(matched_keywords) * 2 + len(matched_workflow_terms)
    return {
        "applied_domain": preset.name,
        "applied_domain_label": preset.label,
        "applied_domain_score": score,
        "matched_applied_keywords": matched_keywords,
        "matched_workflow_terms": matched_workflow_terms,
        "application_signal": "workflow_terms_present" if matched_workflow_terms else "llm_keyword_only",
        "source_query_categories": list(preset.categories),
    }


def rank_applied_domain_candidates(
    papers: list[PaperRecord],
    preset: AppliedDomainPreset,
    min_score: int = 2,
) -> list[tuple[PaperRecord, dict[str, Any]]]:
    scored = [(paper, score_applied_domain_candidate(paper, preset)) for paper in papers]
    filtered = [
        (paper, metadata)
        for paper, metadata in scored
        if int(metadata["applied_domain_score"]) >= min_score
    ]
    return sorted(
        filtered,
        key=lambda item: (
            int(item[1]["applied_domain_score"]),
            item[0].updated_at,
            item[0].published_at,
        ),
        reverse=True,
    )


def fetch_applied_domain_candidates(
    root: Path,
    preset_name: str,
    max_results: int,
    run_date: str,
    keep_results: int = 10,
    min_score: int = 2,
) -> CandidatePaths:
    preset = get_applied_domain_preset(preset_name)
    xml_text = fetch_text(build_arxiv_query_url(categories=list(preset.categories), max_results=max_results))
    trusted_orgs = load_trusted_orgs(root)
    papers = [
        annotate_trusted_orgs(
            replace(paper, source_types=("arxiv_applied_domain", f"applied_domain:{preset.name}")),
            trusted_orgs,
        )
        for paper in parse_arxiv_atom(xml_text, source_type="arxiv_applied_domain")
    ]
    ranked = rank_applied_domain_candidates(papers, preset, min_score=min_score)[:keep_results]
    selected_papers = [paper for paper, _metadata in ranked]
    metadata_by_paper_id = {paper.paper_id: metadata for paper, metadata in ranked}
    return write_candidate_batch(
        root,
        run_date=run_date,
        source=f"arxiv_applied_{preset.name}",
        papers=selected_papers,
        metadata_by_paper_id=metadata_by_paper_id,
    )
