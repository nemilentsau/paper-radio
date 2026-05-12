import json
from dataclasses import dataclass, replace
from pathlib import Path

from paper_radio.papers import PaperRecord


@dataclass(frozen=True)
class TrustedOrg:
    name: str
    aliases: tuple[str, ...]


def load_trusted_orgs(root: Path, config_path: Path = Path("config/trusted-orgs.json")) -> tuple[TrustedOrg, ...]:
    resolved_config_path = config_path if config_path.is_absolute() else root / config_path
    if not resolved_config_path.exists():
        return ()
    data = json.loads(resolved_config_path.read_text(encoding="utf-8"))
    return tuple(
        TrustedOrg(
            name=str(org["name"]),
            aliases=tuple(str(alias) for alias in org.get("aliases", [org["name"]])),
        )
        for org in data.get("trusted_orgs", [])
    )


def match_trusted_orgs(
    affiliations: list[str] | tuple[str, ...],
    orgs: list[TrustedOrg] | tuple[TrustedOrg, ...],
) -> tuple[str, ...]:
    normalized_affiliations = [affiliation.casefold() for affiliation in affiliations]
    matches: list[str] = []
    for org in orgs:
        aliases = tuple(alias.casefold() for alias in org.aliases)
        if any(alias in affiliation for affiliation in normalized_affiliations for alias in aliases):
            matches.append(org.name)
    return tuple(dict.fromkeys(matches))


def annotate_trusted_orgs(
    paper: PaperRecord,
    orgs: list[TrustedOrg] | tuple[TrustedOrg, ...],
) -> PaperRecord:
    trusted_orgs = match_trusted_orgs(paper.author_affiliations, orgs)
    return replace(paper, trusted_orgs=trusted_orgs)
