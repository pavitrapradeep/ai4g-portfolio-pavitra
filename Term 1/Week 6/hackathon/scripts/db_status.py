"""Show what the collector has stored so far.

Run from the project root:  python scripts/db_status.py
Prints counts only: no post texts and no accounts.
"""
import sqlite3
import sys
from collections import Counter
from datetime import datetime, timezone

from cve_meter import config, health, metrics

HOURS = 12
TIME = "%Y-%m-%dT%H:%M:%SZ"

if not config.DB_PATH.exists():
    sys.exit(f"No database yet at {config.DB_PATH}. Start the collector first.")
conn = sqlite3.connect(config.DB_PATH)

print("Per source")
print(f"  {'source':10} {'posts':>6} {'accounts':>9} {'bot flag':>9}  first collected       last collected")
for row in conn.execute(
    "SELECT source, COUNT(*), COUNT(DISTINCT account_hash), COALESCE(SUM(is_bot), 0),"
    " MIN(collected_at), MAX(collected_at) FROM posts GROUP BY source"
):
    print(f"  {row[0]:10} {row[1]:6} {row[2]:9} {row[3]:9}  {row[4]}  {row[5]}")

total, cves = conn.execute(
    "SELECT (SELECT COUNT(*) FROM posts), (SELECT COUNT(DISTINCT cve_id) FROM post_cves)"
).fetchone()
print(f"\nTotal: {total} posts about {cves} different CVEs")

print("\nMastodon posts per home server")
for server, n in conn.execute(
    "SELECT home_server, COUNT(*) FROM posts WHERE source = 'mastodon'"
    " GROUP BY home_server ORDER BY 2 DESC LIMIT 8"
):
    print(f"  {server:28} {n:5}")

print(f"\nStored per hour (UTC, by time of collection), last {HOURS} hours with data")
rows = conn.execute(
    "SELECT substr(collected_at, 1, 13), SUM(source = 'mastodon'), SUM(source = 'bluesky')"
    " FROM posts GROUP BY 1 ORDER BY 1 DESC LIMIT ?", (HOURS,)
).fetchall()
print(f"  {'hour':14} {'mastodon':>9} {'bluesky':>8}")
for hour, mastodon, bluesky in reversed(rows):
    print(f"  {hour.replace('T', ' ')}h {mastodon:9} {bluesky:8}")

tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
if "scores" in tables:  # a database from before phase 2 has no scores yet
    print("\nSentiment scores per model")
    print(f"  {'posts':>6} {'negative':>9} {'neutral':>8} {'positive':>9} {'mean alarm':>11}  model")
    for row in conn.execute(
        "SELECT COUNT(*), SUM(label = 'negative'), SUM(label = 'neutral'), SUM(label = 'positive'),"
        " AVG(negative), model FROM scores GROUP BY model"
    ):
        print(f"  {row[0]:6} {row[1]:9} {row[2]:8} {row[3]:9} {row[4]:11.2f}  {row[5]}")
    unscored = conn.execute(
        "SELECT COUNT(*) FROM posts WHERE id NOT IN (SELECT post_id FROM scores)"
    ).fetchone()[0]
    print(f"  Posts without any score: {unscored}")

    print("\nDetected language ('und' = too little text, '-' = not checked yet)")
    for lang, n in conn.execute(
        "SELECT COALESCE(detected_language, '-'), COUNT(*) FROM posts GROUP BY 1 ORDER BY 2 DESC"
    ):
        print(f"  {lang:4} {n:5}")

if "cves" in tables:  # a database from before phase 3 has no CVE table yet
    known, waiting, kev, watch = conn.execute(
        "SELECT COUNT(*), COALESCE(SUM(checked_at IS NULL), 0), COALESCE(SUM(kev), 0),"
        " COALESCE(SUM(on_watchlist), 0) FROM cves"
    ).fetchone()
    print(f"\nOfficial sources: {known} CVEs, {waiting} not looked up yet, "
          f"{kev} on the CISA list, {watch} on the watchlist")
    print("  CVSS score from")
    for source, n, mean in conn.execute(
        "SELECT cvss_source, COUNT(*), AVG(cvss_score) FROM cves WHERE checked_at IS NOT NULL"
        " GROUP BY 1 ORDER BY 2 DESC"
    ):
        label = {"nvd": "the NVD", "cna": "a CNA", "none": "not yet scored"}[source]
        print(f"    {label:15} {n:5}" + (f"   mean {mean:.1f}" if mean is not None else ""))
    for term, via, n in conn.execute(
        "SELECT watchlist_term, watchlist_via, COUNT(*) FROM cves WHERE on_watchlist"
        " GROUP BY 1, 2 ORDER BY 3 DESC"
    ):
        print(f"  watchlist: {term:22} {n:4}  (matched in: {via})")

print("\nMost mentioned CVEs")
for cve, posts, accounts in conn.execute(
    "SELECT c.cve_id, COUNT(*), COUNT(DISTINCT p.account_hash) FROM post_cves c"
    " JOIN posts p ON p.id = c.post_id GROUP BY c.cve_id ORDER BY 2 DESC LIMIT 5"
):
    print(f"  {cve:18} {posts:4} posts by {accounts} accounts")

if "scores" in tables:
    posts = metrics.load_posts(conn)
    print(f"\nAccounts that look automated (of {len(posts)} analysed posts)")
    print(f"  {'accounts':>8} {'posts':>6}  reason")
    for reason, text in metrics.AUTOMATED_REASONS.items():
        own = [post for post in posts if post["automated"] == reason]
        print(f"  {len({post['account'] for post in own}):8} {len(own):6}  {text}")
    # To tune the rules in config.py: if these still look like feeds, the rules are too loose
    human = Counter(post["account"] for post in posts if not post["automated"])
    print("  Busiest accounts that look human: " +
          (", ".join(f"{n} posts" for _, n in human.most_common(5)) or "none"))

# Phase 4: is it still running, and how far are the 48 hours?
now = datetime.now(timezone.utc)
print("\nThe run")
if "state" in tables:
    beats = dict(conn.execute("SELECT key, value FROM state WHERE key LIKE 'heartbeat_%'"))
    for part in health.PARTS:
        last = beats.get(f"heartbeat_{part}")
        ago = (f"{(now - datetime.strptime(last, TIME).replace(tzinfo=timezone.utc)).total_seconds() / 60:.0f}"
               " min ago") if last else "never"
        print(f"  {part:9} last reported {ago}")
if config.HEALTH_PATH.exists() and (lines := health.read()):
    idle = (now - lines[-1]["time"]).total_seconds() / 60
    print(f"  The collector is {'running' if idle < 2 * config.HEALTH_SECONDS / 60 else 'NOT RUNNING'}:"
          f" last line in health.csv {idle:.0f} min ago")
    runs = health.stretches([line["time"] for line in lines])
    hours = sum((last - first).total_seconds() for first, last in runs) / 3600
    print(f"  Hours collected since {lines[0]['time']:%Y-%m-%d %H:%M} UTC: {hours:.1f} of the 48 we need")
else:
    print("  No health.csv yet: the collector has not run since phase 4")
if "scores" in tables:
    analysed = conn.execute("SELECT COUNT(DISTINCT post_id) FROM scores").fetchone()[0]
    print(f"  Analysed posts: {analysed} of the 300 we need")
