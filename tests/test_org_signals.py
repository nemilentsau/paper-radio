import json
import tempfile
import unittest
from pathlib import Path

from paper_radio.org_signals import TrustedOrg, annotate_trusted_orgs, load_trusted_orgs, match_trusted_orgs
from paper_radio.papers import PaperRecord


class OrgSignalsTest(unittest.TestCase):
    def test_match_trusted_orgs_uses_case_insensitive_aliases(self):
        orgs = [
            TrustedOrg(name="Trusted AI Lab", aliases=("Trusted AI Lab", "TAIL")),
            TrustedOrg(name="Other Lab", aliases=("Other Lab",)),
        ]

        matches = match_trusted_orgs(
            ["Department of ML, trusted ai lab", "TAIL research group", "Unknown University"],
            orgs,
        )

        self.assertEqual(matches, ("Trusted AI Lab",))

    def test_load_trusted_orgs_returns_empty_when_config_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(load_trusted_orgs(Path(tmp)), ())

    def test_load_trusted_orgs_reads_project_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config_path = root / "config" / "trusted-orgs.json"
            config_path.parent.mkdir(parents=True)
            config_path.write_text(
                json.dumps(
                    {
                        "trusted_orgs": [
                            {
                                "name": "Trusted AI Lab",
                                "aliases": ["Trusted AI Lab", "TAIL"],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            orgs = load_trusted_orgs(root)

            self.assertEqual(orgs, (TrustedOrg(name="Trusted AI Lab", aliases=("Trusted AI Lab", "TAIL")),))

    def test_annotate_trusted_orgs_adds_matches_to_paper_record(self):
        paper = PaperRecord(
            paper_id="arxiv-2604.01694",
            source="arxiv",
            source_id="2604.01694",
            title="MiCA Learns More Knowledge Than LoRA and Full Fine-Tuning",
            authors=("Sten Rüdiger",),
            author_affiliations=("Trusted AI Lab",),
            abstract="A compact PEFT method is evaluated on knowledge injection tasks.",
            published_at="2026-04-03T00:00:00Z",
            updated_at="2026-04-04T00:00:00Z",
            categories=("cs.LG",),
            pdf_url="https://arxiv.org/pdf/2604.01694",
            abs_url="https://arxiv.org/abs/2604.01694",
            source_types=("arxiv_recent",),
            status="candidate",
        )

        annotated = annotate_trusted_orgs(paper, [TrustedOrg(name="Trusted AI Lab", aliases=("Trusted AI Lab",))])

        self.assertEqual(annotated.trusted_orgs, ("Trusted AI Lab",))


if __name__ == "__main__":
    unittest.main()
