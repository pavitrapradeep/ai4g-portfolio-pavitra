"""Checks on phase 2: every post gets a score, once, and scoring never blocks the collector.

Run from the project root:  python -m unittest discover -s scripts/tests -t scripts
The sentiment model is replaced by a stand-in here, so nothing is downloaded.
"""
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from cve_meter import db, language, scorer, sentiment

MODEL = "stand-in"


def add_post(conn, key, text="CVE-2026-0001 is being exploited"):
    return db.insert_post(
        conn, post_key=key, source="mastodon", server="hachyderm.io", home_server="hachyderm.io",
        text=text, created_at=datetime(2026, 10, 11, tzinfo=timezone.utc), language="en",
        account_hash="hash", is_bot=0, cves=["CVE-2026-0001"],
    )


def classify(texts):
    """Calls a text alarmed when it says 'exploited'."""
    return [(0.7, 0.2, 0.1) if "exploited" in t else (0.1, 0.8, 0.1) for t in texts]


class TextTest(unittest.TestCase):
    def test_links_become_http(self):
        self.assertEqual(sentiment.prepare("@user see https://example.com/a?b=1 and http://x.test."),
                         "@user see http and http")

    def test_noise_is_removed_before_detecting(self):
        self.assertEqual(language.strip_noise("#CVE cve-2026-12345 @user patch https://example.com now"),
                         "CVE patch now")

    def test_detector(self):
        detect = language.load(["en", "de", "nl"])
        self.assertEqual(detect("This vulnerability is being actively exploited, patch now")[0], "en")
        self.assertEqual(detect("Kritische Sicherheitslücke wird aktiv ausgenutzt, bitte sofort patchen")[0], "de")
        self.assertEqual(detect("CVE-2026-12345 https://example.com #CVE"), ("und", None))


class ScorerTest(unittest.TestCase):
    def setUp(self):
        self.conn = db.connect(":memory:")

    def tearDown(self):
        self.conn.close()

    def test_every_post_is_scored_once(self):
        add_post(self.conn, "a")
        add_post(self.conn, "b", "CVE-2026-0001 published")
        self.assertEqual(scorer.score_pending(self.conn, MODEL, classify), 2)
        self.assertEqual(scorer.score_pending(self.conn, MODEL, classify), 0)
        add_post(self.conn, "c")
        self.assertEqual(scorer.score_pending(self.conn, MODEL, classify), 1)
        self.assertEqual(
            self.conn.execute("SELECT negative, label FROM scores ORDER BY post_id").fetchall(),
            [(0.7, "negative"), (0.1, "neutral"), (0.7, "negative")],
        )
        # A second model scores the same posts again, next to the first
        self.assertEqual(scorer.score_pending(self.conn, "other", classify), 3)

    def test_language_is_detected_once(self):
        add_post(self.conn, "a")
        self.assertEqual(scorer.detect_pending(self.conn, lambda text: ("und", None)), 1)
        self.assertEqual(scorer.detect_pending(self.conn, lambda text: ("en", 0.9)), 0)

    def test_deleted_post_takes_its_score_along(self):
        add_post(self.conn, "a")
        scorer.score_pending(self.conn, MODEL, classify)
        db.delete_post(self.conn, "a")
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM scores").fetchone()[0], 0)

    def test_post_deleted_while_scoring_is_skipped(self):
        add_post(self.conn, "a")

        def slow_classify(texts):
            db.delete_post(self.conn, "a")
            return classify(texts)

        scorer.score_pending(self.conn, MODEL, slow_classify)
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM scores").fetchone()[0], 0)


class TwoWritersTest(unittest.TestCase):
    def test_a_write_that_changes_nothing_does_not_lock_the_database(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "test.db"
            collector, other = db.connect(path), db.connect(path)
            try:
                other.execute("PRAGMA busy_timeout = 100")
                add_post(collector, "a")
                self.assertFalse(add_post(collector, "a"))            # duplicate
                self.assertFalse(db.delete_post(collector, "never"))  # delete of a post we never had
                scorer.score_pending(other, MODEL, classify)          # raised "database is locked" before
                self.assertEqual(other.execute("SELECT COUNT(*) FROM scores").fetchone()[0], 1)
            finally:
                collector.close()
                other.close()


if __name__ == "__main__":
    unittest.main()
