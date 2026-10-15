"""Checks on phase 5: the averages on the dashboard count what we say they count.

Run from the project root:  python -m unittest discover -s scripts/tests -t scripts
"""
import sqlite3
import tempfile
import unittest
from contextlib import closing
from datetime import datetime, timedelta, timezone
from pathlib import Path

from cve_meter import config, db, metrics

NOW = datetime(2026, 10, 10, 12, 30, tzinfo=timezone.utc)


def post(account, negative, minutes_ago=0, cves=("CVE-2026-0001",), is_bot=False, post_id=None, text="",
         profile_hint=None):
    return {"id": post_id or id(object()), "account": account, "negative": negative, "text": text,
            "created_at": NOW - timedelta(minutes=minutes_ago), "cves": list(cves), "is_bot": is_bot,
            "profile_hint": profile_hint}


FEED = ["CVE-2026-{n} (CVSS 9.{n}): Buffer overflow in Product {n} https://example.com/{n} #cve #infosec",
        "CVE-2026-{n} (CVSS 7.{n}): SQL injection in the admin panel of App {n} https://example.com/{n} #cve #infosec"]
HUMAN = ["Patching CVE-2026-1111 tonight, the vendor advisory is vague",
         "Is anyone else seeing exploitation of CVE-2026-2222? Our logs are full of it",
         "Good writeup on CVE-2026-3333 here https://example.com/blog",
         "CVE-2026-4444 again. Third emergency patch this month, I am tired"]


class SummaryTest(unittest.TestCase):
    def test_one_account_counts_at_most_a_few_times(self):
        loud = [post("loud", 1.0, minutes_ago=n) for n in range(10)]
        others = [post("a", 0.0), post("b", 0.0), post("c", 0.0)]
        result = metrics.summary(loud + others)
        self.assertEqual(result["posts"], 13)
        self.assertEqual(result["counted"], config.ACCOUNT_CAP + 3)
        self.assertAlmostEqual(result["alarm"], config.ACCOUNT_CAP / (config.ACCOUNT_CAP + 3))

    def test_the_newest_posts_of_an_account_are_the_ones_that_count(self):
        posts = [post("a", 0.9, minutes_ago=50, post_id=1)] + \
                [post("a", 0.1, minutes_ago=n, post_id=10 + n) for n in range(config.ACCOUNT_CAP)]
        self.assertNotIn(1, [p["id"] for p in metrics.counted(posts)])

    def test_few_posts_is_low_data(self):
        posts = [post(account, 0.5) for account in "abcd"]
        self.assertTrue(metrics.summary(posts)["low_data"])
        self.assertFalse(metrics.summary(posts + [post("e", 0.5)])["low_data"])

    def test_few_accounts_is_low_data(self):
        posts = [post("a", 0.5, minutes_ago=n) for n in range(3)] + [post("b", 0.5, minutes_ago=n) for n in range(3)]
        self.assertEqual(metrics.summary(posts)["counted"], 6)
        self.assertTrue(metrics.summary(posts)["low_data"])

    def test_posts_capped_away_do_not_make_enough_data(self):
        posts = [post("a", 0.5, minutes_ago=n) for n in range(10)] + [post("b", 0.5), post("c", 0.5)]
        self.assertEqual(metrics.summary(posts)["counted"], config.ACCOUNT_CAP + 2)
        self.assertEqual(metrics.summary(posts)["low_data"], config.ACCOUNT_CAP + 2 < config.LOW_DATA_POSTS)

    def test_without_bots_keeps_posts_that_have_no_flag(self):
        posts = metrics.mark_automated([post("a", 0.5, is_bot=True), post("b", 0.5, text="x"),
                                        dict(post("c", 0.5, text="y"), is_bot=False)])
        self.assertEqual([p["account"] for p in metrics.without_bots(posts)], ["b", "c"])


class AutomationTest(unittest.TestCase):
    def test_a_feed_is_found_by_the_form_of_its_posts(self):
        feed = [post("feed", 0.3, minutes_ago=n * 60, text=FEED[n % 2].format(n=1000 + n)) for n in range(4)]
        human = [post("human", 0.6, minutes_ago=n * 60, text=text) for n, text in enumerate(HUMAN)]
        self.assertEqual(metrics.automation(feed + human), {"feed": "template"})

    def test_a_few_posts_in_the_same_form_among_many_others_are_not_a_feed(self):
        same = [post("a", 0.5, minutes_ago=n * 180, text=f"New: CVE-2026-{1000 + n} patch now") for n in range(3)]
        other = [post("a", 0.5, minutes_ago=600 + n * 180, text=f"{text} ({n})")
                 for n, text in enumerate(HUMAN * 2)]
        self.assertEqual(metrics.automation(same + other), {})

    def test_shortened_links_count_as_links(self):
        self.assertEqual(metrics.form("CVE-2026-1 is out nvd.nist.gov/vuln/detai..."),
                         metrics.form("CVE-2026-2 is out https://nvd.nist.gov/vuln/detail/CVE-2026-2"))

    def test_many_posts_within_a_day_is_automated(self):
        many = config.BOT_POSTS_PER_DAY + 1
        busy = [post("busy", 0.5, minutes_ago=n * 60, text=f"{HUMAN[n % 4]} {n}") for n in range(many)]
        # The same number of posts, but never more than BOT_POSTS_PER_DAY of them within 24 hours
        gap = 24 * 60 // config.BOT_POSTS_PER_DAY + 30
        spread = [post("spread", 0.5, minutes_ago=n * gap, text=f"{HUMAN[n % 4]} {n}") for n in range(many)]
        self.assertEqual(metrics.automation(busy + spread), {"busy": "volume"})

    def test_several_posts_within_minutes_is_automated(self):
        minutes = config.BOT_BURST_MINUTES
        thread = [post("thread", 0.5, minutes_ago=500 + n * minutes / 2, text=text) for n, text in enumerate(HUMAN[:3])]
        # One post fewer in the same time, and three posts that take just too long
        pair = [post("pair", 0.5, minutes_ago=n * minutes, text=text) for n, text in enumerate(HUMAN[:2])]
        slow = [post("slow", 0.5, minutes_ago=n * (minutes / 2 + 1), text=text) for n, text in enumerate(HUMAN[:3])]
        self.assertEqual(metrics.automation(thread + pair + slow), {"thread": "burst"})

    def test_the_strongest_reason_is_given(self):
        posts = [post("a", 0.5, is_bot=True, profile_hint="bio", text="x"),
                 post("b", 0.5, profile_hint="rate", text="x"), post("b", 0.5, profile_hint="bio", text="y"),
                 post("c", 0.5, profile_hint="rate", text="x")]
        self.assertEqual(metrics.automation(posts), {"a": "flag", "b": "bio", "c": "rate"})

    def test_every_post_of_an_automated_account_is_marked(self):
        posts = metrics.mark_automated([post("a", 0.5, minutes_ago=50, text="x"), post("a", 0.5, is_bot=True,
                                                                                        text="y")])
        self.assertEqual([p["automated"] for p in posts], ["flag", "flag"])


class GroupingTest(unittest.TestCase):
    def test_per_hour_groups_by_the_hour_the_post_was_written(self):
        hours = metrics.per_hour([post("a", 0.2, minutes_ago=10), post("b", 0.4, minutes_ago=20),
                                  post("c", 0.8, minutes_ago=40)])
        self.assertEqual(list(hours), [NOW.replace(hour=11, minute=0), NOW.replace(minute=0)])
        self.assertAlmostEqual(hours[NOW.replace(minute=0)]["alarm"], 0.3)

    def test_per_cve_uses_only_the_last_24_hours(self):
        alarms = metrics.per_cve([post("a", 0.9, minutes_ago=25 * 60), post("b", 0.1, minutes_ago=60)], NOW)
        self.assertEqual(alarms["CVE-2026-0001"]["posts"], 1)
        self.assertAlmostEqual(alarms["CVE-2026-0001"]["alarm"], 0.1)

    def test_a_post_counts_for_every_cve_it_names(self):
        alarms = metrics.per_cve([post("a", 0.6, cves=("CVE-2026-0001", "CVE-2026-0002"))], NOW)
        self.assertEqual(sorted(alarms), ["CVE-2026-0001", "CVE-2026-0002"])

    def test_ranking_puts_the_watchlist_first_and_low_data_last(self):
        enough = [post(account, 0.2, cves=("CVE-2026-0002",)) for account in "abcde"]
        alarms = metrics.per_cve([post("a", 0.9, cves=("CVE-2026-0001",)), *enough,
                                  post("a", 0.1, cves=("CVE-2026-0003",))], NOW)
        rows = metrics.ranked(alarms, {"CVE-2026-0003": {"on_watchlist": 1, "watchlist_term": "Citrix"}})
        self.assertEqual([row["cve_id"] for row in rows], ["CVE-2026-0003", "CVE-2026-0002", "CVE-2026-0001"])
        self.assertEqual(rows[2]["cvss_source"], "none")  # a CVE the enricher has not seen yet


class DatabaseTest(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.path = Path(folder.name) / "test.db"
        conn = db.connect(self.path)
        db.insert_post(conn, post_key="k1", source="mastodon", server="s", home_server="s",
                       text="CVE-2026-0001 and CVE-2026-0002 are exploited", created_at=NOW, language="en",
                       account_hash="a", is_bot=1, cves=["CVE-2026-0001", "CVE-2026-0002"])
        db.insert_post(conn, post_key="k2", source="bluesky", server="s", home_server=None, text="not scored yet",
                       created_at=NOW, language="en", account_hash="b", is_bot=None, cves=[])
        db.insert_scores(conn, config.PIPELINE_MODEL, [(1, 0.7, 0.2, 0.1)])
        db.add_new_cves(conn)
        conn.close()
        self.conn = metrics.connect(self.path)
        self.addCleanup(self.conn.close)

    def test_only_scored_posts_are_loaded(self):
        posts = metrics.load_posts(self.conn)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]["cves"], ["CVE-2026-0001", "CVE-2026-0002"])
        self.assertEqual((posts[0]["created_at"], posts[0]["negative"], posts[0]["is_bot"]), (NOW, 0.7, True))

    def test_loaded_posts_are_marked(self):
        self.assertEqual(metrics.load_posts(self.conn)[0]["automated"], "flag")

    def test_a_database_from_before_the_profile_hint_still_loads(self):
        with closing(sqlite3.connect(self.path)) as conn:
            conn.execute("ALTER TABLE posts DROP COLUMN profile_hint")
        with closing(metrics.connect(self.path)) as conn:
            self.assertIsNone(metrics.load_posts(conn)[0]["profile_hint"])

    def test_the_dashboard_cannot_write(self):
        with self.assertRaises(Exception):
            self.conn.execute("DELETE FROM posts")

    def test_cves_come_with_their_official_fields(self):
        cves = metrics.load_cves(self.conn)
        self.assertEqual(cves["CVE-2026-0001"]["cvss_source"], "none")
        self.assertIsNone(metrics.last_report(self.conn))


if __name__ == "__main__":
    unittest.main()
