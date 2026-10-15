"""Phase 3: give every CVE its official score, its CISA status and a watchlist tag.

Like the scorer it works from the database, not from the stream: the cves table is the cache,
so a CVE is only requested again when it is due, and CVEs stored before this existed are
filled in too.
"""
import asyncio
import logging
import time
from datetime import datetime, timezone

from . import config, db, health, kev, nvd, watchlist

log = logging.getLogger("enricher")

_catalog = {}       # the CISA list, kept between rounds
_catalog_at = None  # when we downloaded it


def kev_catalog():
    """The CISA list, downloaded again when ours is an hour old. An old one beats none."""
    global _catalog, _catalog_at
    if _catalog_at is None or time.monotonic() - _catalog_at > config.KEV_SECONDS:
        try:
            _catalog, _catalog_at = kev.fetch(), time.monotonic()
        except Exception as e:
            log.warning("CISA list not downloaded, using the previous one: %s: %s", type(e).__name__, e)
    return _catalog


def mark_kev(conn, catalog):
    """Returns the number of CVEs that turned out to be on the CISA list."""
    hits = [cve_id for cve_id in db.cves_not_on_kev(conn) if cve_id in catalog]
    for cve_id in hits:
        db.set_kev(conn, cve_id, *catalog[cve_id])
    return len(hits)


def look_up_due(conn, fetch, now=None, pause=config.NVD_PAUSE_SECONDS):
    """Ask the NVD about every CVE that is due. Returns how many were looked up."""
    due = db.cves_due(conn, now or datetime.now(timezone.utc))
    for n, cve_id in enumerate(due):
        if n:
            time.sleep(pause)
        record = fetch(cve_id)
        db.set_nvd(conn, cve_id, now or datetime.now(timezone.utc),
                   **(nvd.parse(record) if record else nvd.NOT_FOUND))
        health.beat(conn, "enricher")  # per lookup: a long list takes longer than the monitor waits
    return len(due)


def tag_watchlist(conn, terms):
    """Tag every CVE again, so a new post or a changed watchlist.txt counts. Returns the changes."""
    changed = 0
    for cve_id, current, texts in db.watchlist_texts(conn):
        # The official record first: a post can name twenty CVEs and one product
        tag = next(((term, via) for via, text in texts.items() if (term := watchlist.find(terms, text))),
                   (None, None))
        if tag != current:
            db.set_watchlist(conn, cve_id, *tag)
            changed += 1
    return changed


def run_once():
    """One round, with its own database connection because it runs in a separate thread."""
    conn = db.connect()
    try:
        new = db.add_new_cves(conn)
        on_kev = mark_kev(conn, kev_catalog())
        try:
            looked_up = look_up_due(conn, nvd.fetch)
        except Exception as e:  # the next round goes on where this one stopped
            looked_up = None
            log.warning("NVD lookups stopped, trying again in %d s: %s: %s",
                        config.ENRICH_SECONDS, type(e).__name__, e)
        tagged = tag_watchlist(conn, watchlist.load())
        health.beat(conn, "enricher")
    finally:
        conn.close()
    if new or on_kev or looked_up or tagged:
        log.info("%d new CVEs, %d looked up in the NVD, %d new on the CISA list, %d watchlist tags changed",
                 new, looked_up or 0, on_kev, tagged)


async def run():
    """Looks up the CVEs that are due, waits ENRICH_SECONDS and starts again, forever.
    A failed round is logged and tried again; it never stops the collector."""
    if not config.NVD_API_KEY:
        log.warning("no NVD_API_KEY in .env: lookups work, but the NVD may slow them down")
    while True:
        try:
            # In a thread, so the collector keeps reading while we wait between two lookups
            await asyncio.to_thread(run_once)
        except Exception as e:
            log.warning("enrichment failed, trying again in %d s: %s: %s",
                        config.ENRICH_SECONDS, type(e).__name__, e)
        await asyncio.sleep(config.ENRICH_SECONDS)
