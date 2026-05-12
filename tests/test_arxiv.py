import unittest
from urllib.parse import parse_qs, urlparse

from paper_radio.arxiv import build_arxiv_query_url, parse_arxiv_atom

SAMPLE_ATOM = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
  <entry>
    <id>http://arxiv.org/abs/2604.01694v2</id>
    <updated>2026-04-04T00:00:00Z</updated>
    <published>2026-04-03T00:00:00Z</published>
    <title>MiCA Learns More Knowledge Than LoRA and Full Fine-Tuning</title>
    <summary>
      A compact PEFT method is evaluated on knowledge injection tasks.
    </summary>
    <author><name>Sten Rüdiger</name></author>
    <author><name>Sebastian Raschka</name></author>
    <category term="cs.LG" />
    <category term="cs.CL" />
    <link href="http://arxiv.org/abs/2604.01694v2" rel="alternate" type="text/html"/>
    <link title="pdf" href="http://arxiv.org/pdf/2604.01694v2" rel="related" type="application/pdf"/>
  </entry>
  <entry>
    <id>http://arxiv.org/abs/2604.09999v1</id>
    <updated>2026-04-04T00:00:00Z</updated>
    <published>2026-04-04T00:00:00Z</published>
    <title>A Benchmark Theater Paper</title>
    <summary>Results look large but the baselines are stale.</summary>
    <author><name>Example Author</name></author>
    <category term="cs.AI" />
    <link href="http://arxiv.org/abs/2604.09999v1" rel="alternate" type="text/html"/>
    <link title="pdf" href="http://arxiv.org/pdf/2604.09999v1" rel="related" type="application/pdf"/>
  </entry>
</feed>
"""


class ArxivTest(unittest.TestCase):
    def test_build_arxiv_query_url_uses_categories_and_submitted_date_sort(self):
        url = build_arxiv_query_url(categories=["cs.LG", "cs.CL"], max_results=50)
        parsed = urlparse(url)
        query = parse_qs(parsed.query)

        self.assertIn("https://export.arxiv.org/api/query?", url)
        self.assertEqual(query["search_query"], ["cat:cs.LG OR cat:cs.CL"])
        self.assertEqual(query["max_results"], ["50"])
        self.assertEqual(query["sortBy"], ["submittedDate"])
        self.assertEqual(query["sortOrder"], ["descending"])

    def test_parse_arxiv_atom_returns_paper_records(self):
        papers = parse_arxiv_atom(SAMPLE_ATOM, source_type="arxiv_recent")

        self.assertEqual([paper.paper_id for paper in papers], ["arxiv-2604.01694", "arxiv-2604.09999"])
        self.assertEqual(papers[0].source_id, "2604.01694")
        self.assertEqual(papers[0].authors, ("Sten Rüdiger", "Sebastian Raschka"))
        self.assertEqual(papers[0].categories, ("cs.LG", "cs.CL"))
        self.assertEqual(papers[0].pdf_url, "https://arxiv.org/pdf/2604.01694")
        self.assertEqual(papers[0].abs_url, "https://arxiv.org/abs/2604.01694")
        self.assertEqual(papers[0].source_types, ("arxiv_recent",))
        self.assertEqual(papers[0].status, "candidate")


if __name__ == "__main__":
    unittest.main()
