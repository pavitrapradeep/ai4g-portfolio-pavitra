"""Phase 5: the numbers on the dashboard, calculated from what the collector stored.

Nothing here writes. An alarm is always the average of the model's negative probability over
a group of posts: the posts of one hour, or the posts about one CVE in the last 24 hours.
"""
import re
import sqlite3
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from statistics import fmean

from . import clean, config

TIME = "%Y-%m-%dT%H:%M:%SZ"
# Why an account looks automated, strongest reason first
AUTOMATED_REASONS = {
    "flag": "it is marked as a bot on Mastodon",
    "bio": "its profile says it is a bot or a feed",
    "rate": f"it posted more than {config.BOT_PROFILE_POSTS_PER_DAY} times a day since it was made",
    "template": "it writes its posts in one fixed form",
    "burst": f"it posted {config.BOT_BURST_POSTS} times about CVEs within {config.BOT_BURST_MINUTES} minutes",
    "volume": f"it posted about CVEs more than {config.BOT_POSTS_PER_DAY} times within 24 hours",
}
# Full links, and the shortened ones Bluesky puts in the text ("nvd.nist.gov/vuln/detai...")
LINK_RE = re.compile(r"https?://\S+|\b[\w.-]+\.[a-z]{2,}/\S*", re.IGNORECASE)
NUMBER_RE = re.compile(r"\d+(?:[.,]\d+)*")


def parse_time(value):
    """Turns a time from the database (text, UTC) back into a moment we can calculate with."""
    return datetime.strptime(value, TIME).replace(tzinfo=timezone.utc)


def connect(path=config.DB_PATH):
    """Open the database read-only, so the dashboard can never get in the collector's way."""
    return sqlite3.connect(f"{path.as_uri()}?mode=ro", uri=True)


def load_posts(conn, model=config.PIPELINE_MODEL):
    """Every scored post as a dict, oldest first, with the CVE ids it names."""
    cves = defaultdict(list)
    for post_id, cve_id in conn.execute("SELECT post_id, cve_id FROM post_cves ORDER BY cve_id"):
        cves[post_id].append(cve_id)
    # Added after phase 5: a database the collector has not opened since has no such column yet
    columns = {row[1] for row in conn.execute("PRAGMA table_info(posts)")}
    hint = "p.profile_hint" if "profile_hint" in columns else "NULL"
    return mark_automated([
        {"id": row[0], "text": row[1], "created_at": parse_time(row[2]), "source": row[3],
         "is_bot": bool(row[4]), "language": row[5], "account": row[6],
         "negative": row[7], "neutral": row[8], "positive": row[9], "profile_hint": row[10],
         "cves": cves[row[0]]}
        for row in conn.execute(
            "SELECT p.id, p.text, p.created_at, p.source, p.is_bot, p.detected_language, p.account_hash,"
            f" s.negative, s.neutral, s.positive, {hint} FROM posts p JOIN scores s ON s.post_id = p.id"
            " WHERE s.model = ? ORDER BY p.created_at, p.id", (model,)
        )
    ])


def load_cves(conn):
    """What the official sources say, per CVE id."""
    columns = ("description", "cvss_score", "cvss_severity", "cvss_source", "cvss_cna", "kev",
               "kev_added", "kev_ransomware", "on_watchlist", "watchlist_term")
    return {row[0]: dict(zip(columns, row[1:]))
            for row in conn.execute(f"SELECT cve_id, {', '.join(columns)} FROM cves")}


def last_report(conn):
    """When a part of the collector last said it was still going, or None."""
    row = conn.execute("SELECT MAX(value) FROM state WHERE key LIKE 'heartbeat_%'").fetchone()
    return parse_time(row[0]) if row[0] else None


def form(text):
    """The shape of a post: CVE ids, links and numbers made alike, then its first and last three words.

    A feed writes "CVE-2026-1234 (CVSS 9.8): <title> https://... #cve" every time; the title
    changes, the start and the end do not.
    """
    text = NUMBER_RE.sub("0", clean.CVE_RE.sub("cve", LINK_RE.sub("link", text.lower())))
    words = text.split()
    return tuple(words[:3]), tuple(words[-3:])


def busiest_day(times):
    """The most posts within any 24 hours."""
    times = sorted(times)
    most = start = 0
    for end, moment in enumerate(times):
        while moment - times[start] > timedelta(hours=24):
            start += 1
        most = max(most, end - start + 1)
    return most


def burst(times, posts=config.BOT_BURST_POSTS, minutes=config.BOT_BURST_MINUTES):
    """Whether this many posts ever came within this many minutes."""
    times = sorted(times)
    return any(later - first <= timedelta(minutes=minutes) for first, later in zip(times, times[posts - 1:]))


def automation(posts):
    """Per account that looks automated, the strongest reason (a key of AUTOMATED_REASONS).

    Accounts that look human are left out. Judged over all posts given, so pass all of them,
    not one hour's worth.
    """
    # Group the posts per (hashed) account: every rule looks at all posts of one account together
    by_account = defaultdict(list)
    for post in posts:
        by_account[post["account"]].append(post)
    reasons = {}
    for account, own in by_account.items():
        # What the collector noted from the Mastodon profile ('bio' or 'rate'); Bluesky posts have none
        hints = {post.get("profile_hint") for post in own}
        # How many of this account's posts share its most common form (see form() above)
        forms = Counter(form(post["text"]) for post in own).most_common(1)[0][1]
        # The rules are checked from the most certain to the least certain; the first that fits is the
        # reason the dashboard shows, so an account gets one reason even when several apply
        if any(post["is_bot"] for post in own):
            reasons[account] = "flag"  # the account itself says it is a bot (Mastodon's bot flag)
        elif "bio" in hints:
            reasons[account] = "bio"  # its name or bio uses a word such as bot, feed, RSS or alerts
        elif "rate" in hints:
            reasons[account] = "rate"  # more than 50 posts a day since the account was made
        elif forms >= config.BOT_TEMPLATE_POSTS and forms >= config.BOT_TEMPLATE_SHARE * len(own):
            reasons[account] = "template"  # at least 3 posts, and half of all its posts, in the same form
        elif burst(post["created_at"] for post in own):
            reasons[account] = "burst"  # 3 CVE posts within 2 minutes: nobody types that fast
        elif busiest_day(post["created_at"] for post in own) > config.BOT_POSTS_PER_DAY:
            reasons[account] = "volume"  # more than 12 CVE posts within 24 hours
        # No rule fits: the account looks human and is left out of the result
    return reasons


def mark_automated(posts):
    """Give every post an "automated" key: the reason its account looks automated, or None."""
    reasons = automation(posts)
    for post in posts:
        post["automated"] = reasons.get(post["account"])
    return posts


def without_bots(posts):
    """The posts of accounts that do not look automated. Needs mark_automated first."""
    return [post for post in posts if not post["automated"]]


def counted(posts, cap=config.ACCOUNT_CAP):
    """The posts that count towards an average: of every account only its newest few.

    Without this one researcher who posts thirty times about their own find carries the line.
    """
    seen = defaultdict(int)
    keep = []
    for post in sorted(posts, key=lambda post: (post["created_at"], post["id"]), reverse=True):
        seen[post["account"]] += 1
        if seen[post["account"]] <= cap:
            keep.append(post)
    return keep


def summary(posts):
    """The alarm of one group of posts, and how much it rests on."""
    used = counted(posts)
    accounts = len({post["account"] for post in posts})
    return {
        "alarm": fmean(post["negative"] for post in used),
        "posts": len(posts),
        "counted": len(used),
        "accounts": accounts,
        "low_data": len(used) < config.LOW_DATA_POSTS or accounts < config.LOW_DATA_ACCOUNTS,
    }


def hour_of(moment):
    """The start of the hour a moment falls in, used to group posts per hour."""
    return moment.replace(minute=0, second=0, microsecond=0)


def per_hour(posts):
    """A summary per hour that has posts, keyed by the start of the hour (UTC)."""
    groups = defaultdict(list)
    for post in posts:
        groups[hour_of(post["created_at"])].append(post)
    return {hour: summary(group) for hour, group in sorted(groups.items())}


def recent(posts, now, hours=config.CVE_WINDOW_HOURS):
    """The posts written in the last so many hours before now."""
    return [post for post in posts if now - timedelta(hours=hours) <= post["created_at"] <= now]


def per_cve(posts, now):
    """A summary per CVE over its posts of the last 24 hours. A post counts for every CVE it names."""
    groups = defaultdict(list)
    for post in recent(posts, now):
        for cve_id in post["cves"]:
            groups[cve_id].append(post)
    return {cve_id: summary(group) for cve_id, group in groups.items()}


def ranked(alarms, cves):
    """One row per CVE for the table: its alarm next to the official sources.

    The watchlist comes first, then the CVEs with enough data, then the highest alarm. Low data
    goes down and not out: a single worried post can still be the one that matters.
    """
    unknown = {"cvss_score": None, "cvss_source": "none", "kev": 0, "on_watchlist": 0}
    rows = [{"cve_id": cve_id, **unknown, **cves.get(cve_id, {}), **alarm} for cve_id, alarm in alarms.items()]
    return sorted(rows, key=lambda row: (not row["on_watchlist"], row["low_data"], -row["alarm"],
                                         -row["posts"], row["cve_id"]))
