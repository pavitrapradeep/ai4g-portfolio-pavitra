"""The SQLite database: schema and the few queries the collector, scorer and enricher need."""
import sqlite3
from datetime import datetime, timedelta, timezone

from . import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS posts (
    id           INTEGER PRIMARY KEY,
    post_key     TEXT NOT NULL UNIQUE,  -- salted hash of the post's URI, which contains the author's name
    source       TEXT NOT NULL,         -- 'mastodon' or 'bluesky'
    server       TEXT NOT NULL,         -- the server we read it from
    home_server  TEXT,                  -- the server the author's account is on (Mastodon only)
    text         TEXT NOT NULL,         -- plain text, @mentions replaced by @user
    created_at   TEXT NOT NULL,         -- when it was posted, UTC
    collected_at TEXT NOT NULL,         -- when we stored it, UTC
    language     TEXT,                  -- as declared by the post itself
    account_hash TEXT NOT NULL,         -- salted hash of the account, to count different accounts
    is_bot       INTEGER                -- Mastodon's bot flag; NULL on Bluesky, which has none
);
CREATE TABLE IF NOT EXISTS post_cves (
    post_id INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    cve_id  TEXT NOT NULL,
    PRIMARY KEY (post_id, cve_id)
);
CREATE INDEX IF NOT EXISTS idx_posts_created ON posts(created_at);
CREATE INDEX IF NOT EXISTS idx_post_cves_cve ON post_cves(cve_id);
CREATE TABLE IF NOT EXISTS state (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS scores (
    post_id   INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    model     TEXT NOT NULL,            -- one row per post per model, so a second model fits in later
    negative  REAL NOT NULL,            -- the alarm score
    neutral   REAL NOT NULL,
    positive  REAL NOT NULL,
    label     TEXT NOT NULL,            -- the highest of the three
    scored_at TEXT NOT NULL,
    PRIMARY KEY (post_id, model)
);
CREATE TABLE IF NOT EXISTS cves (
    cve_id         TEXT PRIMARY KEY,
    first_seen     TEXT NOT NULL,       -- when we stored the first post that names it, UTC
    checked_at     TEXT,                -- last NVD lookup; NULL: not looked up yet
    nvd_status     TEXT,                -- the NVD's own status, or 'Not found' when it does not know the id
    description    TEXT,
    products       TEXT,                -- vendor and product names in the NVD record, one per line
    cvss_score     REAL,                -- NULL: not yet scored
    cvss_version   TEXT,
    cvss_severity  TEXT,
    cvss_source    TEXT NOT NULL DEFAULT 'none',  -- 'nvd', 'cna' or 'none'
    cvss_cna       TEXT,                -- who gave the score when it is not the NVD
    kev            INTEGER NOT NULL DEFAULT 0,    -- 1: on the CISA Known Exploited Vulnerabilities list
    kev_added      TEXT,
    kev_ransomware TEXT,                -- 'Known' or 'Unknown', as CISA gives it
    kev_product    TEXT,
    on_watchlist   INTEGER NOT NULL DEFAULT 0,
    watchlist_term TEXT,                -- the line of watchlist.txt that matched
    watchlist_via  TEXT                 -- where it matched: 'nvd', 'kev' or 'post'
);
"""

# Columns added after phase 1. An existing database gets them on the next start.
NEW_POST_COLUMNS = {
    "detected_language": "TEXT",    # from the text itself; 'und' when there is too little to go on
    "language_confidence": "REAL",  # the detector's own estimate, 0 to 1
    # Why the author's profile looks automated: 'bio' or 'rate' (posts per day). Only the
    # outcome is stored, not the profile. NULL: nothing found, or no profile (Bluesky).
    "profile_hint": "TEXT",
}


def utc_iso(dt):
    """A moment as text in UTC, like 2026-10-11T15:59:01Z. Every time in the database has this form."""
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def connect(path=config.DB_PATH):
    """Opens the database and creates what is missing: the folder, the tables, and columns added
    in a later phase. Safe to call on a database that already exists."""
    if path != ":memory:":
        path.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(path, timeout=30)  # the collector and the scorer both write: wait, do not fail
    conn.execute("PRAGMA journal_mode=WAL")  # lets the dashboard read while we write
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(SCHEMA)
    have = {row[1] for row in conn.execute("PRAGMA table_info(posts)")}
    for column, kind in NEW_POST_COLUMNS.items():
        if column not in have:
            conn.execute(f"ALTER TABLE posts ADD COLUMN {column} {kind}")
    return conn


# Every write below sits in "with conn:", which always ends the transaction. A write that
# changes nothing (a duplicate) would otherwise keep the database locked for other writers.

def insert_post(conn, *, post_key, source, server, home_server, text, created_at,
                language, account_hash, is_bot, cves, profile_hint=None):
    """Store a post and its CVE ids. Returns False if we already had it."""
    with conn:
        cur = conn.execute(
            "INSERT OR IGNORE INTO posts (post_key, source, server, home_server, text, created_at,"
            " collected_at, language, account_hash, is_bot, profile_hint)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (post_key, source, server, home_server, text, utc_iso(created_at),
             utc_iso(datetime.now(timezone.utc)), language, account_hash, is_bot, profile_hint),
        )
        if cur.rowcount == 0:
            return False
        conn.executemany("INSERT INTO post_cves (post_id, cve_id) VALUES (?, ?)",
                         [(cur.lastrowid, cve) for cve in cves])
    return True


def delete_post(conn, post_key):
    """Remove a post its author deleted. Returns True if we had it."""
    with conn:
        cur = conn.execute("DELETE FROM posts WHERE post_key = ?", (post_key,))
    return bool(cur.rowcount)


def posts_without_language(conn):
    """The posts whose language has not been detected yet, oldest first."""
    return conn.execute("SELECT id, text FROM posts WHERE detected_language IS NULL ORDER BY id").fetchall()


def set_language(conn, post_id, language, confidence):
    """Stores the detected language of one post and how sure the detector was."""
    with conn:
        conn.execute("UPDATE posts SET detected_language = ?, language_confidence = ? WHERE id = ?",
                     (language, confidence, post_id))


def posts_without_score(conn, model):
    """The posts this model has not scored yet, oldest first. This is how the scorer catches up."""
    return conn.execute(
        "SELECT id, text FROM posts WHERE id NOT IN (SELECT post_id FROM scores WHERE model = ?)"
        " ORDER BY id", (model,)
    ).fetchall()


def insert_scores(conn, model, rows):
    """Store (post_id, negative, neutral, positive) rows for one model."""
    now = utc_iso(datetime.now(timezone.utc))
    with conn:
        for post_id, negative, neutral, positive in rows:
            label = max((negative, "negative"), (neutral, "neutral"), (positive, "positive"))[1]
            # The author may have deleted the post while the model was busy: then store nothing
            conn.execute(
                "INSERT OR IGNORE INTO scores (post_id, model, negative, neutral, positive, label, scored_at)"
                " SELECT ?, ?, ?, ?, ?, ?, ? WHERE EXISTS (SELECT 1 FROM posts WHERE id = ?)",
                (post_id, model, negative, neutral, positive, label, now, post_id),
            )


def add_new_cves(conn):
    """Give every CVE named in a post its own row. Returns the number of new ones."""
    with conn:
        cur = conn.execute(
            "INSERT OR IGNORE INTO cves (cve_id, first_seen)"
            " SELECT c.cve_id, MIN(p.collected_at) FROM post_cves c JOIN posts p ON p.id = c.post_id"
            " GROUP BY c.cve_id"
        )
    return cur.rowcount


def cves_due(conn, now):
    """CVE ids to look up in the NVD now: new ones first, then the longest not checked.

    A CVE with a score from the NVD itself is final. One without is looked up again, because
    the NVD scores later or never: often while people still post about it, daily after that.
    """
    def ago(hours):
        """The moment this many hours before now, as database text."""
        return utc_iso(now - timedelta(hours=hours))

    return [row[0] for row in conn.execute(
        "SELECT cve_id FROM cves WHERE checked_at IS NULL OR (cvss_source != 'nvd' AND checked_at <"
        "   CASE WHEN (SELECT MAX(p.collected_at) FROM posts p JOIN post_cves c ON c.post_id = p.id"
        "              WHERE c.cve_id = cves.cve_id) >= ? THEN ? ELSE ? END)"
        " ORDER BY checked_at IS NOT NULL, checked_at, cve_id",
        (ago(config.NVD_ACTIVE_HOURS), ago(config.NVD_RECHECK_HOURS), ago(config.NVD_RECHECK_QUIET_HOURS)),
    )]


def set_nvd(conn, cve_id, now, *, nvd_status, description=None, products=None, cvss_score=None,
            cvss_version=None, cvss_severity=None, cvss_source="none", cvss_cna=None):
    """Stores what the NVD said about one CVE and when we asked. Fields the NVD did not give stay empty."""
    with conn:
        conn.execute(
            "UPDATE cves SET checked_at = ?, nvd_status = ?, description = ?, products = ?, cvss_score = ?,"
            " cvss_version = ?, cvss_severity = ?, cvss_source = ?, cvss_cna = ? WHERE cve_id = ?",
            (utc_iso(now), nvd_status, description, products, cvss_score, cvss_version, cvss_severity,
             cvss_source, cvss_cna, cve_id),
        )


def cves_not_on_kev(conn):
    """The ids of the CVEs we have not yet seen on the CISA list."""
    return [row[0] for row in conn.execute("SELECT cve_id FROM cves WHERE kev = 0")]


def set_kev(conn, cve_id, added, ransomware, product):
    """Marks one CVE as on the CISA list, with the date it was added, ransomware use and the product."""
    with conn:
        conn.execute("UPDATE cves SET kev = 1, kev_added = ?, kev_ransomware = ?, kev_product = ?"
                     " WHERE cve_id = ?", (added, ransomware, product, cve_id))


def watchlist_texts(conn):
    """Per CVE: its id, the current tag (term, via) and the texts a watchlist term can match in."""
    return [(row[0], row[1:3], dict(zip(("nvd", "kev", "post"), row[3:]))) for row in conn.execute(
        "SELECT cve_id, watchlist_term, watchlist_via,"
        " COALESCE(description, '') || char(10) || COALESCE(products, ''), COALESCE(kev_product, ''),"
        " COALESCE((SELECT group_concat(p.text, char(10)) FROM posts p JOIN post_cves c ON c.post_id = p.id"
        "           WHERE c.cve_id = cves.cve_id), '')"
        " FROM cves ORDER BY cve_id"
    )]


def set_watchlist(conn, cve_id, term, via):
    """Stores which watchlist term matched one CVE and where it matched; no term clears the tag."""
    with conn:
        conn.execute("UPDATE cves SET on_watchlist = ?, watchlist_term = ?, watchlist_via = ? WHERE cve_id = ?",
                     (int(term is not None), term, via, cve_id))


def get_state(conn, key):
    """Reads one remembered value, such as the Bluesky cursor. None when nothing is stored yet."""
    row = conn.execute("SELECT value FROM state WHERE key = ?", (key,)).fetchone()
    return row[0] if row else None


def set_state(conn, key, value):
    """Remembers one value under a key, replacing the old one. Values are stored as text."""
    with conn:
        conn.execute("INSERT INTO state (key, value) VALUES (?, ?)"
                     " ON CONFLICT(key) DO UPDATE SET value = excluded.value", (key, str(value)))
