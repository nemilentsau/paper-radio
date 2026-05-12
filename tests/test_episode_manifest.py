import json
import tempfile
import unittest
from pathlib import Path

from paper_radio.episode_manifest import create_episode_manifest
from paper_radio.papers import PaperRecord, write_paper_record


class EpisodeManifestTest(unittest.TestCase):
    def test_create_episode_manifest_from_stored_paper_records(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_paper_record(
                root,
                PaperRecord(
                    paper_id="arxiv-2604.01694",
                    source="arxiv",
                    source_id="2604.01694",
                    title="MiCA Learns More Knowledge Than LoRA and Full Fine-Tuning",
                    authors=("Sten Rüdiger",),
                    abstract="A compact PEFT method is evaluated on knowledge injection tasks.",
                    published_at="2026-04-03T00:00:00Z",
                    updated_at="2026-04-04T00:00:00Z",
                    categories=("cs.LG",),
                    pdf_url="https://arxiv.org/pdf/2604.01694",
                    abs_url="https://arxiv.org/abs/2604.01694",
                    source_types=("arxiv",),
                    status="ingested",
                ),
            )

            manifest_path = create_episode_manifest(
                root=root,
                episode_path="episodes/2026-05-12/01_peft",
                title="PEFT papers with stale baselines",
                episode_type="comparison",
                paper_ids=["arxiv-2604.01694"],
            )

            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["episode_id"], "episode-2026-05-12-01-peft")
            self.assertEqual(manifest["title"], "PEFT papers with stale baselines")
            self.assertEqual(manifest["episode_type"], "comparison")
            self.assertEqual(manifest["paper_ids"], ["arxiv-2604.01694"])
            self.assertEqual(
                manifest["paper_titles"],
                {"arxiv-2604.01694": "MiCA Learns More Knowledge Than LoRA and Full Fine-Tuning"},
            )
            self.assertEqual(
                manifest["paper_paths"],
                {"arxiv-2604.01694": "data/papers/arxiv-2604.01694.md"},
            )


if __name__ == "__main__":
    unittest.main()
