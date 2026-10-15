"""Checks on phase 4: one collector at a time, a stuck part is noticed, and the record and the
backup say what really happened.

Run from the project root:  python -m unittest discover -s scripts/tests -t scripts
"""
import sqlite3
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from cve_meter import config, db, health

NOW = datetime(2026, 10, 10, 12, tzinfo=timezone.utc)


def minutes(n):
    return timedelta(minutes=n)


class HealthTest(unittest.TestCase):
    def setUp(self):
        self.conn = db.connect(":memory:")
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.folder = Path(folder.name)

    def tearDown(self):
        self.conn.close()

    def test_a_second_collector_does_not_get_the_lock(self):
        first = health.lock(self.folder / "collector.lock")
        self.assertIsNotNone(first)
        self.assertIsNone(health.lock(self.folder / "collector.lock"))
        first.close()  # what the system does when the first collector ends
        again = health.lock(self.folder / "collector.lock")
        self.assertIsNotNone(again)
        again.close()

    def test_a_part_that_stops_reporting_is_noticed(self):
        limit = timedelta(seconds=config.QUIET_SECONDS)
        # Just started: nothing has reported yet, and nothing is late yet
        self.assertEqual(health.quiet(self.conn, NOW, NOW + limit - minutes(1)), [])
        # A part that never reports is late once the limit has passed since the start
        self.assertEqual(health.quiet(self.conn, NOW, NOW + limit + minutes(1)), list(health.PARTS))
        # A report from a run before this one does not count as late straight away
        db.set_state(self.conn, "heartbeat_scorer", db.utc_iso(NOW - timedelta(days=1)))
        self.assertEqual(health.quiet(self.conn, NOW, NOW + minutes(1)), [])
        for part in ("mastodon", "bluesky", "enricher"):
            db.set_state(self.conn, f"heartbeat_{part}", db.utc_iso(NOW + limit))
        self.assertEqual(health.quiet(self.conn, NOW, NOW + limit + minutes(1)), ["scorer"])
        health.beat(self.conn, "scorer")  # the real time, long after NOW
        self.assertNotIn("scorer", health.quiet(self.conn, NOW, NOW + limit + minutes(1)))

    def test_the_record_counts_analysed_posts_and_starts(self):
        path = self.folder / "health.csv"
        health.record(self.conn, NOW, start=True, path=path)
        for key in ("a", "b"):
            db.insert_post(self.conn, post_key=key, source="bluesky", server="host", home_server=None,
                           text="CVE-2026-0001", created_at=NOW, language="en", account_hash="hash",
                           is_bot=None, cves=["CVE-2026-0001"])
        db.insert_scores(self.conn, "model a", [(1, 0.7, 0.2, 0.1)])
        db.insert_scores(self.conn, "model b", [(1, 0.6, 0.3, 0.1)])  # a second model is not a second post
        db.add_new_cves(self.conn)
        health.record(self.conn, NOW + minutes(5), start=False, path=path)
        first, second = health.read(path)
        self.assertEqual(first, {"time": NOW, "posts": "0", "scored": "0", "cves": "0", "looked_up": "0", "start": "1"})
        self.assertEqual(second, {"time": NOW + minutes(5), "posts": "2", "scored": "1", "cves": "1",
                                  "looked_up": "0", "start": "0"})

    def test_only_time_the_collector_ran_is_counted(self):
        times = [NOW, NOW + minutes(5), NOW + minutes(6),  # restarted after a minute
                 NOW + minutes(11), NOW + minutes(40), NOW + minutes(45)]  # then off for half an hour
        self.assertEqual(health.stretches(times),
                         [(NOW, NOW + minutes(11)), (NOW + minutes(40), NOW + minutes(45))])
        self.assertEqual(health.stretches([]), [])

    def test_the_backup_holds_what_is_still_in_the_wal_file(self):
        source = self.folder / "data" / "cve_meter.db"
        conn = db.connect(source)
        self.addCleanup(conn.close)
        db.set_state(conn, "key", "value")
        copies = self.folder / "backups"
        now = datetime.now(timezone.utc)  # the real time: the age of a copy is read from the file
        copy = health.backup(now, source, copies)
        check = sqlite3.connect(copy)
        self.addCleanup(check.close)
        self.assertEqual(check.execute("SELECT value FROM state").fetchall(), [("value",)])
        self.assertIsNone(health.backup(now + minutes(5), source, copies))  # the copy is recent enough

    def test_old_backups_are_removed(self):
        source = self.folder / "data" / "cve_meter.db"
        db.connect(source).close()
        copies = self.folder / "backups"
        copies.mkdir()
        for day in range(1, config.BACKUPS_KEPT + 3):
            (copies / f"cve_meter-202609{day:02}-0000.db").touch()
        # Those files are from "now" for the system, so ask from a time when they are old
        health.backup(datetime.now(timezone.utc) + timedelta(hours=config.BACKUP_HOURS + 1), source, copies)
        left = sorted(p.name for p in copies.iterdir())
        self.assertEqual(len(left), config.BACKUPS_KEPT)
        self.assertNotIn("cve_meter-20260901-0000.db", left)
        self.assertEqual(left[-2], f"cve_meter-202609{config.BACKUPS_KEPT + 2:02}-0000.db")


if __name__ == "__main__":
    unittest.main()
