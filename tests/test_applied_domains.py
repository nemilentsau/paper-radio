import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from paper_radio.applied_domains import (
    APPLIED_DOMAIN_PRESETS,
    fetch_applied_domain_candidates,
    rank_applied_domain_candidates,
    score_applied_domain_candidate,
)
from paper_radio.papers import PaperRecord

SAMPLE_APPLIED_ATOM = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/abs/2605.11111v1</id>
    <updated>2026-05-20T00:00:00Z</updated>
    <published>2026-05-19T00:00:00Z</published>
    <title>Clinical RAG Agents for Radiology Evidence Workflows</title>
    <summary>
      We evaluate a large language model retrieval workflow for clinical radiology evidence extraction
      with expert comparison.
    </summary>
    <author><name>Example Clinician</name></author>
    <category term="cs.CL" />
  </entry>
  <entry>
    <id>http://arxiv.org/abs/2605.22222v1</id>
    <updated>2026-05-19T00:00:00Z</updated>
    <published>2026-05-18T00:00:00Z</published>
    <title>A Generic Optimization Benchmark</title>
    <summary>No language model or domain workflow signal appears here.</summary>
    <author><name>Example Author</name></author>
    <category term="cs.LG" />
  </entry>
</feed>
"""


def make_paper(title: str, abstract: str) -> PaperRecord:
    return PaperRecord(
        paper_id="arxiv-2605.11111",
        source="arxiv",
        source_id="2605.11111",
        title=title,
        authors=("Example Author",),
        abstract=abstract,
        published_at="2026-05-19T00:00:00Z",
        updated_at="2026-05-20T00:00:00Z",
        categories=("cs.CL",),
        pdf_url="https://arxiv.org/pdf/2605.11111",
        abs_url="https://arxiv.org/abs/2605.11111",
        source_types=("arxiv_applied_domain",),
        status="candidate",
    )


class AppliedDomainsTest(unittest.TestCase):
    def test_score_applied_domain_candidate_records_keywords_and_workflow_terms(self):
        preset = APPLIED_DOMAIN_PRESETS["bio_medicine"]
        paper = make_paper(
            "Clinical RAG Agents for Radiology Evidence Workflows",
            "A large language model extracts evidence from EHR notes for expert decision support.",
        )

        metadata = score_applied_domain_candidate(paper, preset)

        self.assertEqual(metadata["applied_domain"], "bio_medicine")
        self.assertGreaterEqual(metadata["applied_domain_score"], 6)
        self.assertIn("clinical", metadata["matched_applied_keywords"])
        self.assertIn("evidence", metadata["matched_workflow_terms"])
        self.assertEqual(metadata["application_signal"], "workflow_terms_present")

    def test_rank_applied_domain_candidates_filters_weak_domain_vocab(self):
        preset = APPLIED_DOMAIN_PRESETS["bio_medicine"]
        strong = make_paper(
            "Clinical RAG Agents for Radiology Evidence Workflows",
            "A large language model retrieval workflow extracts medical evidence for expert review.",
        )
        weak = make_paper("A Generic Benchmark", "A baseline model is tested on unrelated tasks.")

        ranked = rank_applied_domain_candidates([weak, strong], preset, min_score=2)

        self.assertEqual([paper.paper_id for paper, _metadata in ranked], ["arxiv-2605.11111"])

    def test_fetch_applied_domain_candidates_writes_filtered_metadata_batch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with patch("paper_radio.applied_domains.fetch_text", return_value=SAMPLE_APPLIED_ATOM):
                paths = fetch_applied_domain_candidates(
                    root,
                    preset_name="bio_medicine",
                    max_results=20,
                    keep_results=10,
                    min_score=2,
                    run_date="2026-05-20",
                )

            candidates = json.loads(paths.json_path.read_text(encoding="utf-8"))
            markdown = paths.markdown_path.read_text(encoding="utf-8")

        self.assertEqual(paths.json_path.name, "arxiv_applied_bio_medicine.json")
        self.assertEqual([candidate["paper_id"] for candidate in candidates], ["arxiv-2605.11111"])
        self.assertEqual(candidates[0]["applied_domain"], "bio_medicine")
        self.assertIn("arxiv_applied_domain", candidates[0]["source_types"])
        self.assertIn("Clinical RAG Agents", markdown)
        self.assertIn("Applied-domain score", markdown)


if __name__ == "__main__":
    unittest.main()
