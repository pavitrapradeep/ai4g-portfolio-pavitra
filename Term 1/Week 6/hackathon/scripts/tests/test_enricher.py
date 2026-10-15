"""Checks on phase 3: every CVE gets a score with its source, a CISA status and a watchlist tag.

Run from the project root:  python -m unittest discover -s scripts/tests -t scripts
The NVD and CISA answers below are cut-down copies of real ones, so nothing is requested.
"""
import unittest
from datetime import datetime, timedelta, timezone

from cve_meter import db, enricher, kev, nvd, watchlist

NOW = datetime(2026, 10, 11, 12, tzinfo=timezone.utc)
TERMS = ["Citrix", "NetScaler", "Exchange Server", "ESXi"]

# CVE-2025-6543: scored by the vendor (CVSS 4.0) and by the NVD (CVSS 3.1)
CITRIX = {
    "id": "CVE-2025-6543",
    "vulnStatus": "Analyzed",
    "descriptions": [{"lang": "es", "value": "Vulnerabilidad de desbordamiento"},
                     {"lang": "en", "value": "Memory overflow vulnerability in NetScaler ADC"}],
    "affected": [{"source": "secure@citrix.com",
                  "affectedData": [{"vendor": "NetScaler", "product": "ADC"},
                                   {"vendor": "NetScaler", "product": "Gateway"}]}],
    "metrics": {
        "cvssMetricV40": [{"source": "secure@citrix.com", "type": "Secondary",
                           "cvssData": {"version": "4.0", "baseScore": 9.2, "baseSeverity": "CRITICAL"}}],
        "cvssMetricV31": [{"source": "nvd@nist.gov", "type": "Primary",
                           "cvssData": {"version": "3.1", "baseScore": 9.8, "baseSeverity": "CRITICAL"}}],
        "ssvcV203": [{"source": "134c704f-9b21-4f2e-91b3-4a467353bcc0", "ssvcData": {}}],
    },
    "configurations": [{"nodes": [{"cpeMatch": [
        {"criteria": "cpe:2.3:a:citrix:netscaler_application_delivery_controller:*:*:*:*:fips:*:*:*"}]}]}],
}
# A new CVE: only the CNA has scored it, twice, and the NVD has added no products yet
ATLASSIAN = {
    "id": "CVE-2026-21589",
    "vulnStatus": "Awaiting Analysis",
    "descriptions": [{"lang": "en", "value": "This is a vulnerability in Bitbucket Data Center"}],
    "affected": [{"source": "security@atlassian.com",
                  "affectedData": [{"vendor": "Atlassian", "product": "Bamboo Data Center"}]}],
    "metrics": {
        "cvssMetricV31": [{"source": "security@atlassian.com", "type": "Secondary",
                           "cvssData": {"version": "3.1", "baseScore": 8.8, "baseSeverity": "HIGH"}}],
        "cvssMetricV40": [{"source": "security@atlassian.com", "type": "Secondary",
                           "cvssData": {"version": "4.0", "baseScore": 9.3, "baseSeverity": "CRITICAL"}}],
        "ssvcV203": [{"source": "134c704f-9b21-4f2e-91b3-4a467353bcc0", "ssvcData": {}}],
    },
}
UNSCORED = {"id": "CVE-2026-0003", "vulnStatus": "Received", "metrics": {},
            "descriptions": [{"lang": "en", "value": "A flaw in some router"}]}
RECORDS = {r["id"]: r for r in (CITRIX, ATLASSIAN, UNSCORED)}

KEV = kev.parse({"vulnerabilities": [
    {"cveID": "CVE-2025-6543", "dateAdded": "2025-06-30", "knownRansomwareCampaignUse": "Unknown",
     "vendorProject": "Citrix", "product": "NetScaler ADC and Gateway"},
]})


def add_post(conn, key, cves, text="patch now", collected=NOW):
    db.insert_post(
        conn, post_key=key, source="mastodon", server="hachyderm.io", home_server="hachyderm.io",
        text=text, created_at=collected, language="en", account_hash="hash", is_bot=0, cves=cves,
    )
    # insert_post stamps the real time; these tests need to choose it
    conn.execute("UPDATE posts SET collected_at = ? WHERE post_key = ?", (db.utc_iso(collected), key))
    conn.commit()
    db.add_new_cves(conn)


def cve(conn, cve_id, columns):
    return conn.execute(f"SELECT {columns} FROM cves WHERE cve_id = ?", (cve_id,)).fetchone()


class NvdTest(unittest.TestCase):
    def test_the_nvd_score_wins_from_the_cna_score(self):
        self.assertEqual(nvd.best_score(CITRIX), {
            "cvss_score": 9.8, "cvss_version": "3.1", "cvss_severity": "CRITICAL",
            "cvss_source": "nvd", "cvss_cna": None,
        })

    def test_without_an_nvd_score_the_newest_cna_score_is_used(self):
        self.assertEqual(nvd.best_score(ATLASSIAN), {
            "cvss_score": 9.3, "cvss_version": "4.0", "cvss_severity": "CRITICAL",
            "cvss_source": "cna", "cvss_cna": "security@atlassian.com",
        })

    def test_no_score_is_not_yet_scored(self):
        self.assertEqual(nvd.best_score(UNSCORED), {"cvss_source": "none"})
        self.assertEqual(nvd.best_score({"metrics": CITRIX["metrics"] | {"cvssMetricV40": [], "cvssMetricV31": []}}),
                         {"cvss_source": "none"})  # only SSVC left

    def test_cvss_2_keeps_its_severity_outside_the_data(self):
        old = {"metrics": {"cvssMetricV2": [{"source": "nvd@nist.gov", "type": "Primary", "baseSeverity": "HIGH",
                                             "cvssData": {"version": "2.0", "baseScore": 7.5}}]}}
        self.assertEqual(nvd.best_score(old)["cvss_severity"], "HIGH")

    def test_products_come_from_the_cna_and_from_the_cpe_names(self):
        self.assertEqual(nvd.products(CITRIX), [
            "citrix netscaler application delivery controller", "NetScaler ADC", "NetScaler Gateway"])
        self.assertEqual(nvd.parse(CITRIX)["description"], "Memory overflow vulnerability in NetScaler ADC")


class WatchlistTest(unittest.TestCase):
    def test_whole_words_in_any_case(self):
        self.assertEqual(watchlist.find(TERMS, "new #citrix bug"), "Citrix")
        self.assertEqual(watchlist.find(TERMS, "Microsoft Exchange Server 2019"), "Exchange Server")
        self.assertIsNone(watchlist.find(TERMS, "ESXiArgs ransomware"))
        self.assertIsNone(watchlist.find(TERMS, "key exchange servers"))

    def test_the_file_in_the_repository_loads(self):
        terms = watchlist.load()
        self.assertIn("NetScaler", terms)
        self.assertFalse([t for t in terms if t.startswith("#")])


class EnricherTest(unittest.TestCase):
    def setUp(self):
        self.conn = db.connect(":memory:")
        self.asked = []

    def tearDown(self):
        self.conn.close()

    def fetch(self, cve_id):
        self.asked.append(cve_id)
        return RECORDS.get(cve_id)

    def look_up(self, now=NOW):
        self.asked = []
        enricher.look_up_due(self.conn, self.fetch, now, pause=0)
        return self.asked

    def test_every_cve_gets_a_score_with_its_source(self):
        add_post(self.conn, "a", ["CVE-2025-6543", "CVE-2026-21589", "CVE-2026-0003", "CVE-2026-99999"])
        self.look_up()
        self.assertEqual(
            self.conn.execute("SELECT cve_id, cvss_score, cvss_source, nvd_status FROM cves ORDER BY 1").fetchall(),
            [("CVE-2025-6543", 9.8, "nvd", "Analyzed"),
             ("CVE-2026-0003", None, "none", "Received"),
             ("CVE-2026-21589", 9.3, "cna", "Awaiting Analysis"),
             ("CVE-2026-99999", None, "none", "Not found")],  # the NVD does not know it
        )
        self.assertEqual(cve(self.conn, "CVE-2025-6543", "first_seen")[0], db.utc_iso(NOW))

    def test_the_same_cve_is_not_requested_twice(self):
        add_post(self.conn, "a", ["CVE-2025-6543", "CVE-2026-21589"])
        self.assertEqual(len(self.look_up()), 2)
        self.assertEqual(self.look_up(), [])
        add_post(self.conn, "b", ["CVE-2025-6543", "CVE-2026-0003"])  # one known, one new
        self.assertEqual(self.look_up(), ["CVE-2026-0003"])

    def test_a_cve_without_nvd_score_is_looked_up_again_later(self):
        add_post(self.conn, "a", ["CVE-2025-6543", "CVE-2026-21589", "CVE-2026-99999"])
        self.look_up()
        self.assertEqual(self.look_up(NOW + timedelta(hours=1)), [])
        # Two hours on, people still post about them: the two without an NVD score are due
        self.assertEqual(self.look_up(NOW + timedelta(hours=3)), ["CVE-2026-21589", "CVE-2026-99999"])
        # Two days on nobody posts any more: once a day is enough
        self.assertEqual(self.look_up(NOW + timedelta(days=2)), ["CVE-2026-21589", "CVE-2026-99999"])
        self.assertEqual(self.look_up(NOW + timedelta(days=2, hours=3)), [])
        # When the NVD gives its own score, that is the end of it
        RECORDS["CVE-2026-99999"] = dict(CITRIX, id="CVE-2026-99999")
        self.addCleanup(RECORDS.pop, "CVE-2026-99999")
        self.look_up(NOW + timedelta(days=4))
        self.assertEqual(cve(self.conn, "CVE-2026-99999", "cvss_score, cvss_source"), (9.8, "nvd"))
        self.assertEqual(self.look_up(NOW + timedelta(days=9)), ["CVE-2026-21589"])

    def test_a_failed_lookup_is_tried_again(self):
        add_post(self.conn, "a", ["CVE-2025-6543", "CVE-2026-21589"])

        def broken(cve_id):
            if cve_id == "CVE-2026-21589":
                raise ConnectionError("no network")
            return RECORDS[cve_id]

        with self.assertRaises(ConnectionError):
            enricher.look_up_due(self.conn, broken, NOW, pause=0)
        self.assertEqual(self.look_up(), ["CVE-2026-21589"])  # the one that worked is kept

    def test_cisa_status(self):
        add_post(self.conn, "a", ["CVE-2025-6543", "CVE-2026-21589"])
        self.assertEqual(enricher.mark_kev(self.conn, KEV), 1)
        self.assertEqual(enricher.mark_kev(self.conn, KEV), 0)
        self.assertEqual(cve(self.conn, "CVE-2025-6543", "kev, kev_added, kev_ransomware, kev_product"),
                         (1, "2025-06-30", "Unknown", "Citrix NetScaler ADC and Gateway"))
        self.assertEqual(cve(self.conn, "CVE-2026-21589", "kev, kev_added"), (0, None))

    def test_watchlist_tag(self):
        add_post(self.conn, "a", ["CVE-2025-6543"], "CVE-2025-6543 looks bad")
        add_post(self.conn, "b", ["CVE-2026-21589"], "CVE-2026-21589 in Bitbucket")
        add_post(self.conn, "c", ["CVE-2026-0003"], "CVE-2026-0003: patch your ESXi hosts")
        self.look_up()
        self.assertEqual(enricher.tag_watchlist(self.conn, TERMS), 2)
        self.assertEqual(enricher.tag_watchlist(self.conn, TERMS), 0)
        columns = "on_watchlist, watchlist_term, watchlist_via"
        self.assertEqual(cve(self.conn, "CVE-2025-6543", columns), (1, "Citrix", "nvd"))
        self.assertEqual(cve(self.conn, "CVE-2026-0003", columns), (1, "ESXi", "post"))
        self.assertEqual(cve(self.conn, "CVE-2026-21589", columns), (0, None, None))
        # A changed watchlist counts on the next round, and so does a deleted post
        self.assertEqual(enricher.tag_watchlist(self.conn, ["Bitbucket"]), 3)
        self.assertEqual(cve(self.conn, "CVE-2026-21589", columns), (1, "Bitbucket", "nvd"))
        db.delete_post(self.conn, "c")
        enricher.tag_watchlist(self.conn, TERMS)
        self.assertEqual(cve(self.conn, "CVE-2026-0003", columns), (0, None, None))

    def test_watchlist_matches_the_cisa_entry_before_the_nvd_knows_the_cve(self):
        add_post(self.conn, "a", ["CVE-2025-6543"], "CVE-2025-6543")
        enricher.mark_kev(self.conn, KEV)
        enricher.tag_watchlist(self.conn, TERMS)
        self.assertEqual(cve(self.conn, "CVE-2025-6543", "watchlist_term, watchlist_via"), ("Citrix", "kev"))


if __name__ == "__main__":
    unittest.main()
