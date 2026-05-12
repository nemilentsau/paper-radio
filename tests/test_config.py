import unittest

from paper_radio.config import (
    AUDIO_FORMAT,
    AUDIO_LANGUAGE,
    AUDIO_LENGTH,
    DATA_DIR,
    EPISODES_DIR,
    JOBS_DIR,
    PROJECT_ROOT,
    SCHEMAS_DIR,
    STATUS_VALUES,
)


class ConfigTest(unittest.TestCase):
    def test_project_directories_are_repo_local(self):
        self.assertEqual(DATA_DIR, PROJECT_ROOT / "data")
        self.assertEqual(JOBS_DIR, PROJECT_ROOT / "jobs")
        self.assertEqual(SCHEMAS_DIR, PROJECT_ROOT / "schemas")
        self.assertEqual(EPISODES_DIR, PROJECT_ROOT / "episodes")

    def test_notebooklm_audio_defaults_match_reference_pipeline(self):
        self.assertEqual(AUDIO_FORMAT, "Deep Dive")
        self.assertEqual(AUDIO_LENGTH, "Long")
        self.assertEqual(AUDIO_LANGUAGE, "English")

    def test_status_values_cover_daily_paper_radio_flow(self):
        self.assertIn("ingested", STATUS_VALUES)
        self.assertIn("triaged", STATUS_VALUES)
        self.assertIn("review_ready", STATUS_VALUES)
        self.assertIn("source_dossier_ready", STATUS_VALUES)
        self.assertIn("notebooklm_bundle_ready", STATUS_VALUES)
        self.assertIn("audio_ready", STATUS_VALUES)


if __name__ == "__main__":
    unittest.main()
