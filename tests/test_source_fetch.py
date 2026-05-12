import tempfile
import unittest
from pathlib import Path

from paper_radio.papers import PaperRecord, load_paper_record, write_paper_record
from paper_radio.source_fetch import SourceFetchError, fetch_paper_source, paper_full_text_path, paper_pdf_path


def make_paper() -> PaperRecord:
    return PaperRecord(
        paper_id="arxiv-2605.10933",
        source="arxiv",
        source_id="2605.10933",
        title="DECO: Sparse Mixture-of-Experts with Dense-Comparable Performance on End-Side Devices",
        authors=("Chenyang Song",),
        abstract="A sparse MoE abstract.",
        published_at="2026-05-11T17:58:28Z",
        updated_at="2026-05-11T17:58:28Z",
        categories=("cs.LG",),
        pdf_url="https://arxiv.org/pdf/2605.10933",
        abs_url="https://arxiv.org/abs/2605.10933",
        source_types=("arxiv_recent",),
        status="triaged",
    )


class SourceFetchTest(unittest.TestCase):
    def test_fetch_paper_source_writes_pdf_full_text_and_updates_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_paper_record(root, make_paper())

            result = fetch_paper_source(
                root,
                "arxiv-2605.10933",
                fetch_pdf_bytes=lambda url: b"%PDF-1.7 fake",
                extract_pdf_text=lambda path: "full paper text " * 100,
            )

            paper = load_paper_record(root, "arxiv-2605.10933")
            self.assertEqual(result.pdf_path, paper_pdf_path(root, "arxiv-2605.10933"))
            self.assertEqual(result.full_text_path, paper_full_text_path(root, "arxiv-2605.10933"))
            self.assertEqual(result.pdf_path.read_bytes(), b"%PDF-1.7 fake")
            self.assertIn("full paper text", result.full_text_path.read_text(encoding="utf-8"))
            self.assertEqual(paper.local_pdf_path, "data/papers/pdfs/arxiv-2605.10933.pdf")
            self.assertEqual(paper.full_text_path, "data/papers/fulltext/arxiv-2605.10933.txt")

    def test_fetch_paper_source_raises_and_leaves_no_full_text_when_pdf_download_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_paper_record(root, make_paper())

            def fail_fetch(url: str) -> bytes:
                raise OSError("temporary DNS failure")

            with self.assertRaisesRegex(SourceFetchError, "Failed to fetch PDF"):
                fetch_paper_source(
                    root,
                    "arxiv-2605.10933",
                    fetch_pdf_bytes=fail_fetch,
                    extract_pdf_text=lambda path: "full paper text " * 100,
                )

            self.assertFalse(paper_full_text_path(root, "arxiv-2605.10933").exists())


if __name__ == "__main__":
    unittest.main()
