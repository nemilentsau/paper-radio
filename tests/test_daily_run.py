import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from paper_radio.candidates import CandidatePaths
from paper_radio.daily_run import run_daily
from paper_radio.episode_planning import EpisodeJobPlan
from paper_radio.papers import PaperRecord, write_paper_record
from paper_radio.triage_planning import TriageJobPlan
from paper_radio.triage_promotion import TriagePromotionResult


def make_paper(paper_id: str) -> PaperRecord:
    source_id = paper_id.removeprefix("arxiv-")
    return PaperRecord(
        paper_id=paper_id,
        source="arxiv",
        source_id=source_id,
        title=f"Paper {paper_id}",
        authors=("Ada Lovelace",),
        abstract="A paper abstract.",
        published_at="2026-05-13T00:00:00Z",
        updated_at="2026-05-13T00:00:00Z",
        categories=("cs.LG",),
        pdf_url=f"https://arxiv.org/pdf/{source_id}",
        abs_url=f"https://arxiv.org/abs/{source_id}",
        source_types=("arxiv_recent",),
        status="candidate",
    )


class DailyRunTest(unittest.TestCase):
    def write_candidates(self, root: Path, run_date: str, paper_ids: list[str]) -> Path:
        candidate_dir = root / "data" / "candidates" / run_date
        candidate_dir.mkdir(parents=True)
        candidate_path = candidate_dir / "arxiv.json"
        candidate_path.write_text(
            json.dumps([make_paper(paper_id).to_dict() for paper_id in paper_ids]),
            encoding="utf-8",
        )
        (candidate_dir / "arxiv.md").write_text("# candidates\n", encoding="utf-8")
        return candidate_path

    def write_triage_manifest(self, root: Path, paper_ids: list[str]) -> None:
        jobs = [
            {
                "job_id": f"triage-{paper_id}",
                "kind": "triage",
                "paper_id": paper_id,
                "candidate": make_paper(paper_id).to_dict(),
                "input_paths": ["data/candidates/2026-05-13/arxiv.json"],
                "output_path": f"data/triage/{paper_id}.json",
                "schema_path": "schemas/triage-record.schema.json",
            }
            for paper_id in paper_ids
        ]
        manifest = root / "jobs" / "triage.jsonl"
        manifest.parent.mkdir(parents=True)
        manifest.write_text("\n".join(json.dumps(job) for job in jobs) + "\n", encoding="utf-8")

    def test_run_daily_reuses_candidates_runs_missing_triage_and_builds_one_episode(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            candidate_path = self.write_candidates(root, "2026-05-13", ["arxiv-2605.00001", "arxiv-2605.00002"])
            self.write_triage_manifest(root, ["arxiv-2605.00001", "arxiv-2605.00002"])
            triage_dir = root / "data" / "triage"
            triage_dir.mkdir(parents=True)
            (triage_dir / "arxiv-2605.00001.json").write_text('{"paper_id":"arxiv-2605.00001"}', encoding="utf-8")
            for paper_id in ["arxiv-2605.00001", "arxiv-2605.00002"]:
                write_paper_record(root, make_paper(paper_id))

            def fake_promote(*args, **kwargs):
                self.assertEqual(kwargs["paper_ids"], ["arxiv-2605.00001", "arxiv-2605.00002"])
                return TriagePromotionResult(
                    promoted_paper_ids=["arxiv-2605.00001", "arxiv-2605.00002"],
                    skipped_paper_ids=[],
                    unrecognized_paper_ids=[],
                )

            def fake_fetch(root: Path, paper_id: str):
                paper = make_paper(paper_id)
                pdf_path = root / "data" / "papers" / "pdfs" / f"{paper_id}.pdf"
                text_path = root / "data" / "papers" / "fulltext" / f"{paper_id}.txt"
                pdf_path.parent.mkdir(parents=True, exist_ok=True)
                text_path.parent.mkdir(parents=True, exist_ok=True)
                pdf_path.write_bytes(b"%PDF fake")
                text_path.write_text("x" * 1200, encoding="utf-8")
                write_paper_record(
                    root,
                    PaperRecord.from_dict(
                        {
                            **paper.to_dict(),
                            "local_pdf_path": pdf_path.relative_to(root).as_posix(),
                            "full_text_path": text_path.relative_to(root).as_posix(),
                        }
                    ),
                )

            with (
                patch("paper_radio.daily_run.fetch_recent_candidates") as fetch_candidates,
                patch("paper_radio.daily_run.write_triage_job_manifest") as plan_triage,
                patch("paper_radio.daily_run.run_job") as run_job,
                patch("paper_radio.daily_run.promote_triage_results", side_effect=fake_promote),
                patch("paper_radio.daily_run.fetch_paper_source", side_effect=fake_fetch) as fetch_source,
                patch("paper_radio.daily_run.write_episode_job_manifests") as plan_episode,
                patch("paper_radio.daily_run.run_episode", return_value=[["episode"]]) as run_episode,
            ):
                plan_triage.return_value = TriageJobPlan(
                    job_ids=["triage-arxiv-2605.00001", "triage-arxiv-2605.00002"]
                )
                plan_episode.return_value = EpisodeJobPlan(
                    review_job_ids=["review-arxiv-2605.00001", "review-arxiv-2605.00002"],
                    source_dossier_job_id="episode-2026-05-13-01-frontier-ml-roundup-dossier",
                )

                report = run_daily(
                    root=root,
                    run_date="2026-05-13",
                    categories=["cs.LG"],
                    max_results=2,
                    episode_slug="01_frontier_ml_roundup",
                    title="Daily frontier ML",
                    episode_type="frontier_ml_roundup",
                    agent="codex",
                )

            fetch_candidates.assert_not_called()
            self.assertEqual([call.args[1] for call in run_job.call_args_list], ["triage-arxiv-2605.00002"])
            self.assertEqual(fetch_source.call_count, 2)
            run_episode.assert_called_once_with("episodes/2026-05-13/01_frontier_ml_roundup", "codex", root=root)
            self.assertEqual(report.candidate_path, candidate_path)
            self.assertEqual(report.promoted_paper_ids, ["arxiv-2605.00001", "arxiv-2605.00002"])
            self.assertEqual(report.triage_job_ids_run, ["triage-arxiv-2605.00002"])
            self.assertEqual(report.episode_path, Path("episodes/2026-05-13/01_frontier_ml_roundup"))

    def test_run_daily_fresh_removes_run_date_candidates_episode_and_candidate_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_candidates(root, "2026-05-13", ["arxiv-2605.00001"])
            (root / "episodes" / "2026-05-13" / "01_frontier_ml_roundup").mkdir(parents=True)
            for path in [
                root / "data" / "triage" / "arxiv-2605.00001.json",
                root / "data" / "papers" / "arxiv-2605.00001.json",
                root / "data" / "papers" / "arxiv-2605.00001.md",
                root / "data" / "papers" / "pdfs" / "arxiv-2605.00001.pdf",
                root / "data" / "papers" / "fulltext" / "arxiv-2605.00001.txt",
                root / "data" / "reviews" / "arxiv-2605.00001.json",
            ]:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("stale", encoding="utf-8")

            def fake_fetch_candidates(root: Path, categories: list[str], max_results: int, run_date: str):
                candidate_path = self.write_candidates(root, run_date, ["arxiv-2605.00001"])
                return CandidatePaths(json_path=candidate_path, markdown_path=candidate_path.with_suffix(".md"))

            def fake_promote(*args, **kwargs):
                write_paper_record(root, make_paper("arxiv-2605.00001"))
                return TriagePromotionResult(
                    promoted_paper_ids=["arxiv-2605.00001"],
                    skipped_paper_ids=[],
                    unrecognized_paper_ids=[],
                )

            with (
                patch("paper_radio.daily_run.fetch_recent_candidates", side_effect=fake_fetch_candidates),
                patch("paper_radio.daily_run.write_triage_job_manifest") as plan_triage,
                patch("paper_radio.daily_run.run_job"),
                patch("paper_radio.daily_run.promote_triage_results", side_effect=fake_promote),
                patch("paper_radio.daily_run.fetch_paper_source"),
                patch("paper_radio.daily_run.write_episode_job_manifests") as plan_episode,
                patch("paper_radio.daily_run.run_episode", return_value=[]),
            ):
                def fake_plan_triage(root: Path, candidate_path: Path):
                    self.write_triage_manifest(root, ["arxiv-2605.00001"])
                    return TriageJobPlan(job_ids=["triage-arxiv-2605.00001"])

                plan_triage.side_effect = fake_plan_triage
                plan_episode.return_value = EpisodeJobPlan(
                    review_job_ids=["review-arxiv-2605.00001"],
                    source_dossier_job_id="episode-2026-05-13-01-frontier-ml-roundup-dossier",
                )
                run_daily(
                    root=root,
                    run_date="2026-05-13",
                    categories=["cs.LG"],
                    max_results=1,
                    episode_slug="01_frontier_ml_roundup",
                    title="Daily frontier ML",
                    episode_type="frontier_ml_roundup",
                    agent="codex",
                    fresh=True,
                )

            self.assertFalse((root / "data" / "reviews" / "arxiv-2605.00001.json").exists())
            self.assertFalse((root / "data" / "papers" / "fulltext" / "arxiv-2605.00001.txt").exists())


if __name__ == "__main__":
    unittest.main()
