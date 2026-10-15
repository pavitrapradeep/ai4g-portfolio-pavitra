"""Settings for the collector. Change servers, hashtags and timings here."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT / "data"
DB_PATH = DATA_DIR / "cve_meter.db"
LOG_PATH = DATA_DIR / "collector.log"
SALT_PATH = ROOT / "salt.txt"

CONTACT = os.getenv("CONTACT") or "no contact set"
USER_AGENT = f"cve-panic-meter/0.1 (student project; {CONTACT})"
TIMEOUT = 20

# Chosen in phase 0 (README, "The streams and their terms"). infosec.exchange is left out on purpose:
# its feeds are closed and its terms forbid scraping.
MASTODON_SERVERS = ["mastodon.social", "hachyderm.io"]
MASTODON_TAGS = ["CVE", "infosec", "vulnerability", "PatchTuesday"]
MASTODON_POLL_SECONDS = 300
MASTODON_PAGE_SIZE = 40  # the API's maximum

JETSTREAM_HOSTS = [
    "jetstream2.us-east.bsky.network",
    "jetstream1.us-east.bsky.network",
    "jetstream2.us-west.bsky.network",
    "jetstream1.us-west.bsky.network",
]
JETSTREAM_COLLECTION = "app.bsky.feed.post"
JETSTREAM_SILENCE_SECONDS = 60   # no message for this long: reconnect
JETSTREAM_REPORT_SECONDS = 300   # how often to log counts and save the cursor
JETSTREAM_MAX_BACKOFF = 60

# Phase 2: the sentiment model. The revision is fixed, so everyone scores with the same
# weights and the test in phase 6 can be repeated.
MODEL_A = "cardiffnlp/twitter-roberta-base-sentiment-latest"
MODEL_A_REVISION = "3216a57f2a0d9c45a2e6c20157c20c49fb4bf9c7"
# Phase 6, extra: once scripts/finetune.py has written a fine-tuned twitter-roberta-base-sentiment-latest
# to this folder, the collector scores with it and the dashboard shows its scores. Without the folder
# both use twitter-roberta-base-sentiment-latest as it comes from Hugging Face. Scores are stored per
# model, so a switch overwrites nothing.
# The folder name is the name the scores are stored under: -2 is the second round, trained on 900 posts.
MODEL_FINETUNED_DIR = ROOT / "models" / "model-a-finetuned-2"
if MODEL_FINETUNED_DIR.is_dir():
    PIPELINE_MODEL, PIPELINE_SOURCE, PIPELINE_REVISION = MODEL_FINETUNED_DIR.name, str(MODEL_FINETUNED_DIR), None
else:
    PIPELINE_MODEL, PIPELINE_SOURCE, PIPELINE_REVISION = MODEL_A, MODEL_A, MODEL_A_REVISION
MODEL_MAX_TOKENS = 512
SCORE_BATCH_SIZE = 16
SCORE_SECONDS = 60  # how often the collector looks for posts without a score

# The language detector chooses between these (ISO 639-1 codes). A post in a language that
# is not listed gets the closest one that is, so keep the list broad.
LANGUAGES = ["en", "de", "fr", "es", "nl", "it", "pt", "pl", "sv", "ru", "uk", "tr", "ar",
             "ja", "zh", "ko"]
LANGUAGE_MIN_LETTERS = 20  # fewer letters than this after cleaning: 'und', undetermined

# Phase 3: the official sources per CVE.
ENRICH_SECONDS = 60  # how often the collector looks for CVEs to look up
NVD_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
NVD_API_KEY = os.getenv("NVD_API_KEY")  # personal, one per teammate; works without, but slower
NVD_PAUSE_SECONDS = 6          # between two requests, as the NVD asks
NVD_ACTIVE_HOURS = 24          # a CVE with a post this recent is "active"
NVD_RECHECK_HOURS = 2          # an active CVE without an NVD score is looked up again this often
NVD_RECHECK_QUIET_HOURS = 24   # and one nobody posts about any more this often
KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
KEV_SECONDS = 3600  # download the whole catalog at most this often

# One product name per line. A municipality can replace it with its own software list.
WATCHLIST_PATH = ROOT / "watchlist.txt"

# Phase 4: the continuous run, see docs/workflow.md.
LOCK_PATH = DATA_DIR / "collector.lock"
HEALTH_PATH = DATA_DIR / "health.csv"
BACKUP_DIR = DATA_DIR / "backups"
HEALTH_SECONDS = 300  # one line in health.csv this often
QUIET_SECONDS = 900   # a part that reports nothing for this long is stuck: start again
BACKUP_HOURS = 6      # copy the database this often
BACKUPS_KEPT = 8      # and keep this many copies, two days' worth

# Phase 5: the dashboard. It only reads the database.
ACCOUNT_CAP = 3         # one account counts at most this often in one average
LOW_DATA_POSTS = 5      # an average over fewer counted posts than this,
LOW_DATA_ACCOUNTS = 3   # or over fewer different accounts than this, is marked "low data"
CVE_WINDOW_HOURS = 24   # a CVE's alarm is the average over its posts of this many hours
DASHBOARD_REFRESH_SECONDS = 60
LOCAL_TIMEZONE = "Europe/Amsterdam"  # times on the dashboard; the database stays in UTC
TEST_RESULTS_PATH = ROOT / "evaluation" / "results.json"  # written in phase 6

# Accounts that look automated. Mastodon's bot flag catches few of them and
# Bluesky has none, so the dashboard also looks at how an account behaves. These are starting
# values, not measured ones: check them with scripts/db_status.py against the posts themselves.
BOT_PROFILE_POSTS_PER_DAY = 50  # a Mastodon account that posted more than this per day since it was made
BOT_POSTS_PER_DAY = 12          # more posts about CVEs than this from one account within 24 hours
BOT_TEMPLATE_POSTS = 3          # at least this many posts by one account in the same form,
BOT_TEMPLATE_SHARE = 0.5        # and at least this share of all its posts
BOT_BURST_POSTS = 3             # at least this many posts about CVEs by one account
BOT_BURST_MINUTES = 2           # within this many minutes: nobody types that fast
# Fediverse custom: an account with one of these in its profile does not want to be processed
# by bots. Its posts are not stored.
OPT_OUT_TAGS = ("#nobot", "#noindex")
