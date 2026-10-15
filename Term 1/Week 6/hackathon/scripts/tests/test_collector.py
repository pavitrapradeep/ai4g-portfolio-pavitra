"""Checks on the parts where a mistake would leak a name or lose a post.

Run from the project root:  python -m unittest discover -s scripts/tests -t scripts
"""
import unittest
from datetime import datetime, timezone

from cve_meter import bluesky, clean, db, mastodon

SALT = b"test-salt"

MASTODON_STATUS = {
    "id": "115",
    "uri": "https://infosec.exchange/users/alice/statuses/115",
    "created_at": "2026-10-11T15:59:01.000Z",
    "language": "en",
    "spoiler_text": "",
    "content": (
        '<p><span class="h-card"><a href="https://hachyderm.io/@bob" class="u-url mention">@<span>bob</span></a></span>'
        " cve-2026-12345 is being exploited &amp; "
        '<a href="https://example.com/advisory"><span class="invisible">https://</span>'
        '<span class="ellipsis">example.com/adv</span><span class="invisible">isory</span></a></p>'
        "<p>Patch now</p>"
    ),
    "account": {"url": "https://infosec.exchange/@alice", "bot": False},
}


def bluesky_event(operation, text="New: CVE-2026-0001 and CVE-2026-0002, thanks @carol.bsky.social"):
    commit = {"operation": operation, "collection": "app.bsky.feed.post", "rkey": "3abc"}
    if operation == "create":
        commit["record"] = {"text": text, "langs": ["en"]}
    return {"did": "did:plc:secret123", "time_us": 1_791_000_000_000_000, "kind": "commit", "commit": commit}


class CleanTest(unittest.TestCase):
    def test_html_to_text_keeps_links_whole(self):
        text = clean.html_to_text(MASTODON_STATUS["content"])
        self.assertEqual(text, "@bob cve-2026-12345 is being exploited & https://example.com/advisory Patch now")

    def test_mentions_are_hidden(self):
        self.assertEqual(
            clean.hide_mentions("cc @bob, @alice@infosec.exchange and @carol.bsky.social."),
            "cc @user, @user and @user.",
        )
        self.assertEqual(clean.hide_mentions("see https://hachyderm.io/@bob/123"), "see https://hachyderm.io/@user/123")

    def test_extract_cves(self):
        self.assertEqual(clean.extract_cves("cve-2026-12345, CVE-2026-12345 and CVE-2025-6543"),
                         ["CVE-2025-6543", "CVE-2026-12345"])
        self.assertEqual(clean.extract_cves("EUVD-2026-1234 and CVE-2026-12"), [])

    def test_hash_depends_on_salt(self):
        self.assertEqual(clean.salted_hash(SALT, "x"), clean.salted_hash(SALT, "x"))
        self.assertNotEqual(clean.salted_hash(SALT, "x"), clean.salted_hash(b"other", "x"))


class StoreTest(unittest.TestCase):
    def setUp(self):
        self.conn = db.connect(":memory:")

    def tearDown(self):
        self.conn.close()

    def rows(self):
        return self.conn.execute("SELECT * FROM posts").fetchall()

    def test_mastodon_post_is_stored_once_and_without_names(self):
        self.assertTrue(mastodon.store(self.conn, SALT, "hachyderm.io", MASTODON_STATUS))
        # The same post read from the other server is a duplicate
        self.assertFalse(mastodon.store(self.conn, SALT, "mastodon.social", MASTODON_STATUS))
        (row,) = self.rows()
        stored = " ".join(str(value) for value in row)
        self.assertNotIn("alice", stored)
        self.assertNotIn("bob", stored)
        self.assertIn("infosec.exchange", stored)  # the home server is kept, the name is not
        self.assertEqual(self.conn.execute("SELECT cve_id FROM post_cves").fetchall(), [("CVE-2026-12345",)])

    def test_mastodon_post_without_cve_is_skipped(self):
        status = dict(MASTODON_STATUS, content="<p>EUVD-2026-1234 published</p>")
        self.assertFalse(mastodon.store(self.conn, SALT, "hachyderm.io", status))
        self.assertEqual(self.rows(), [])

    def test_mastodon_post_by_an_account_that_opted_out_is_skipped(self):
        nobot = dict(MASTODON_STATUS["account"],
                     note='<p>Security person. <a href="#" class="hashtag">#<span>NoBot</span></a></p>')
        for account in (nobot, dict(MASTODON_STATUS["account"], noindex=True)):
            self.assertFalse(mastodon.store(self.conn, SALT, "hachyderm.io", dict(MASTODON_STATUS, account=account)))
        self.assertEqual(self.rows(), [])

    def test_mastodon_profile_hint_is_stored_but_not_the_profile(self):
        account = dict(MASTODON_STATUS["account"], display_name="CVE Alerts", note="<p>Feed by alice</p>")
        self.assertTrue(mastodon.store(self.conn, SALT, "hachyderm.io", dict(MASTODON_STATUS, account=account)))
        stored = " ".join(str(value) for value in self.rows()[0])
        self.assertIn("bio", stored)
        self.assertNotIn("Alerts", stored)
        self.assertNotIn("Feed by", stored)

    def test_mastodon_profile_hint(self):
        now = datetime(2026, 10, 11, tzinfo=timezone.utc)
        person = {"display_name": "Alice", "note": "<p>Breaks things, fixes them. #nobots</p>",
                  "created_at": "2022-11-05T00:00:00.000Z", "statuses_count": 9000}
        self.assertIsNone(mastodon.profile_hint(person, now))
        self.assertEqual(mastodon.profile_hint(dict(person, note="<p>Automated posts from NVD</p>"), now), "bio")
        self.assertEqual(mastodon.profile_hint(dict(person, display_name="CVE bot"), now), "bio")
        self.assertIsNone(mastodon.profile_hint(dict(person, display_name="Robotics fan"), now))
        self.assertEqual(mastodon.profile_hint(dict(person, statuses_count=100_000), now), "rate")
        self.assertIsNone(mastodon.profile_hint({"display_name": "Bob"}, now))  # fields left out

    def test_bluesky_create_then_delete(self):
        counts = {"seen": 0, "new": 0, "deleted": 0}
        bluesky.handle(self.conn, SALT, "host", bluesky_event("create"), counts)
        bluesky.handle(self.conn, SALT, "host", bluesky_event("create"), counts)  # replay after reconnect
        bluesky.handle(self.conn, SALT, "host", bluesky_event("create", "no id here"), counts)
        self.assertEqual(counts, {"seen": 3, "new": 1, "deleted": 0})
        stored = " ".join(str(value) for value in self.rows()[0])
        self.assertNotIn("secret123", stored)
        self.assertNotIn("carol", stored)
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM post_cves").fetchone()[0], 2)

        bluesky.handle(self.conn, SALT, "host", bluesky_event("delete"), counts)
        self.assertEqual(counts["deleted"], 1)
        self.assertEqual(self.rows(), [])
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM post_cves").fetchone()[0], 0)


if __name__ == "__main__":
    unittest.main()
