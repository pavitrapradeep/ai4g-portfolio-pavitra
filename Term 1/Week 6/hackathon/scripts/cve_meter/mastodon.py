"""Mastodon: ask each server for the newest posts under each hashtag, every few minutes."""
import asyncio
import logging
import re
from datetime import datetime, timezone
from urllib.parse import urlparse

import requests

from . import clean, config, db, health

log = logging.getLogger("mastodon")
HEADERS = {"User-Agent": config.USER_AGENT}
# Words with which feeds and bots describe themselves in their name or bio
BOT_WORDS_RE = re.compile(r"\b(?:bot|feed|rss|automated|auto-?posts?|alerts?)\b", re.IGNORECASE)


def feeds_open(server):
    """Since Mastodon 4.5 a server can close its hashtag feeds. Respect that setting."""
    try:
        r = requests.get(f"https://{server}/api/v2/instance", headers=HEADERS, timeout=config.TIMEOUT)
        access = r.json()["configuration"].get("timelines_access", {}).get("hashtag_feeds")
    except Exception as e:
        log.warning("%s: could not read the access setting (%s), trying anyway", server, type(e).__name__)
        return True
    # Older servers do not have the setting; their feeds are public. Newer ones give one
    # value for posts by their own users ("local") and one for posts from other servers.
    if access is None:
        return True
    values = list(access.values()) if isinstance(access, dict) else [access]
    if "public" in values:
        return True
    log.warning("%s: hashtag feeds are '%s', skipping this server", server, access)
    return False


def fetch_tag(server, tag):
    """Asks one server for the newest public posts with one hashtag (one page, the API's maximum)."""
    r = requests.get(f"https://{server}/api/v1/timelines/tag/{tag}",
                     params={"limit": config.MASTODON_PAGE_SIZE}, headers=HEADERS, timeout=config.TIMEOUT)
    r.raise_for_status()
    return r.json()


def opted_out(account):
    """The author asked not to be indexed, or wrote #nobot or #noindex in their profile."""
    bio = clean.html_to_text(account.get("note") or "")
    return bool(account.get("noindex")) or any(
        re.search(rf"{re.escape(tag)}(?!\w)", bio, re.IGNORECASE) for tag in config.OPT_OUT_TAGS)


def profile_hint(account, now=None):
    """Why the profile looks automated: 'bio', 'rate' or None. Only this outcome is stored."""
    if BOT_WORDS_RE.search(f"{account.get('display_name') or ''} {clean.html_to_text(account.get('note') or '')}"):
        return "bio"
    try:
        made = datetime.fromisoformat(account["created_at"])
        days = max(((now or datetime.now(timezone.utc)) - made).total_seconds() / 86400, 1)
        if account["statuses_count"] / days > config.BOT_PROFILE_POSTS_PER_DAY:
            return "rate"
    except (KeyError, TypeError, ValueError):
        pass  # a server that leaves the fields out tells us nothing
    return None


def store(conn, salt, server, status):
    """Store one status if it names a CVE. Returns True if it was new."""
    account = status["account"]
    if opted_out(account):
        return False
    text = clean.html_to_text(status["content"])
    if status.get("spoiler_text"):  # the content warning often holds the CVE id
        text = f"{status['spoiler_text']} {text}"
    cves = clean.extract_cves(text)
    if not cves:
        return False
    return db.insert_post(
        conn,
        post_key=clean.salted_hash(salt, status["uri"]),  # same uri on every server: skips duplicates
        source="mastodon",
        server=server,
        home_server=urlparse(account["url"]).hostname,
        text=clean.hide_mentions(text),
        created_at=datetime.fromisoformat(status["created_at"]),
        language=status.get("language"),
        account_hash=clean.salted_hash(salt, account["url"]),
        is_bot=int(bool(account.get("bot"))),
        cves=cves,
        profile_hint=profile_hint(account),
    )


async def run(conn, salt):
    """Every MASTODON_POLL_SECONDS: asks each open server for each hashtag and stores the posts that
    name a CVE. Warns when one page was not enough, because posts were then missed."""
    log.info("polling %s for #%s every %d s", ", ".join(config.MASTODON_SERVERS),
             " #".join(config.MASTODON_TAGS), config.MASTODON_POLL_SECONDS)
    newest = {}  # (server, tag) -> highest status id seen, to notice when one page was not enough
    while True:
        # Asked again every round: a server can close its feeds, or open them, while we run
        servers = [s for s in config.MASTODON_SERVERS if await asyncio.to_thread(feeds_open, s)]
        if not servers:
            log.error("no Mastodon server with open hashtag feeds, asking again in %d s",
                      config.MASTODON_POLL_SECONDS)
        new = 0
        for server in servers:
            for tag in config.MASTODON_TAGS:
                try:
                    statuses = await asyncio.to_thread(fetch_tag, server, tag)
                    new += sum(store(conn, salt, server, s) for s in statuses)
                except Exception as e:
                    log.warning("%s #%s failed: %s: %s", server, tag, type(e).__name__, e)
                    continue
                if statuses:
                    ids = [int(s["id"]) for s in statuses]
                    seen = newest.get((server, tag))
                    if seen and min(ids) > seen:
                        log.warning("%s #%s: more than %d new posts since the last poll, some were missed",
                                    server, tag, config.MASTODON_PAGE_SIZE)
                    newest[(server, tag)] = max(ids)
                await asyncio.sleep(1)
        total = conn.execute("SELECT COUNT(*) FROM posts WHERE source = 'mastodon'").fetchone()[0]
        log.info("%d new posts with a CVE id (%d stored in total)", new, total)
        health.beat(conn, "mastodon")
        await asyncio.sleep(config.MASTODON_POLL_SECONDS)
