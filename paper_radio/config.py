from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
PAPERS_DIR = DATA_DIR / "papers"
REVIEWS_DIR = DATA_DIR / "reviews"
JOBS_DIR = PROJECT_ROOT / "jobs"
SCHEMAS_DIR = PROJECT_ROOT / "schemas"
EPISODES_DIR = PROJECT_ROOT / "episodes"

AUDIO_FORMAT = "Deep Dive"
AUDIO_LENGTH = "Long"
AUDIO_LANGUAGE = "English"
AUDIO_PROMPT = (
    "Generate an extended, rigorous research conversation for a serious technical listener. Focus on claim versus "
    "evidence, baseline quality, missing ablations, evaluation cleanliness, and what would make the result more "
    "credible. Keep the tone concrete and critical without inventing facts beyond the provided sources."
)

STATUS_VALUES = (
    "not_started",
    "ingested",
    "triaged",
    "review_queued",
    "review_ready",
    "episode_planned",
    "source_dossier_queued",
    "source_dossier_ready",
    "notebooklm_bundle_ready",
    "audio_requested",
    "audio_ready",
    "failed",
    "manual_action_required",
)
