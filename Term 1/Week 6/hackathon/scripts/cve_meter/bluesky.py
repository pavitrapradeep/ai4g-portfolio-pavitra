"""Bluesky: keep a connection open to Jetstream, which pushes every new public post."""
import asyncio
import json
import logging
import time
from datetime import datetime, timezone

import websockets

from . import clean, config, db, health

log = logging.getLogger("bluesky")
CURSOR_KEY = "jetstream_cursor"
CURSOR_REWIND_US = 5_000_000  # go back 5 s on reconnect; duplicates are skipped anyway


def handle(conn, salt, host, event, counts):
    """Store a new post that names a CVE, or remove a post its author deleted."""
    commit = event.get("commit")
    if event.get("kind") != "commit" or not commit or commit.get("collection") != config.JETSTREAM_COLLECTION:
        return
    # The URI contains the account id, so we only ever keep its hash
    post_key = clean.salted_hash(salt, f"at://{event['did']}/{commit['collection']}/{commit['rkey']}")
    if commit["operation"] == "delete":
        # Bluesky's developer guidelines: delete what the user deleted
        counts["deleted"] += db.delete_post(conn, post_key)
    elif commit["operation"] == "create":
        counts["seen"] += 1
        record = commit.get("record", {})
        text = record.get("text", "")
        cves = clean.extract_cves(text)
        if not cves:
            return
        counts["new"] += db.insert_post(
            conn,
            post_key=post_key,
            source="bluesky",
            server=host,
            home_server=None,
            text=clean.hide_mentions(" ".join(text.split())),
            # Jetstream's own clock; the post's createdAt is filled in by the author's app
            created_at=datetime.fromtimestamp(event["time_us"] / 1_000_000, timezone.utc),
            language=",".join(record.get("langs") or []) or None,
            account_hash=clean.salted_hash(salt, event["did"]),
            is_bot=None,
            cves=cves,
        )


async def listen(conn, salt, host):
    """Read from one server until the connection breaks."""
    url = f"wss://{host}/subscribe?wantedCollections={config.JETSTREAM_COLLECTION}"
    cursor = db.get_state(conn, CURSOR_KEY)
    if cursor:  # continue where we stopped, so a short break loses nothing
        url += f"&cursor={int(cursor) - CURSOR_REWIND_US}"
    counts = {"seen": 0, "new": 0, "deleted": 0}
    last_report = time.monotonic()
    async with websockets.connect(url, user_agent_header=config.USER_AGENT,
                                  open_timeout=config.TIMEOUT, max_size=None) as ws:
        log.info("connected to %s%s", host, " (resuming from saved position)" if cursor else "")
        while True:
            raw = await asyncio.wait_for(ws.recv(), config.JETSTREAM_SILENCE_SECONDS)
            event = json.loads(raw)
            handle(conn, salt, host, event, counts)
            if time.monotonic() - last_report > config.JETSTREAM_REPORT_SECONDS:
                db.set_state(conn, CURSOR_KEY, event["time_us"])
                health.beat(conn, "bluesky")
                total = conn.execute("SELECT COUNT(*) FROM posts WHERE source = 'bluesky'").fetchone()[0]
                log.info("%d new posts with a CVE id out of %d read, %d deleted (%d stored in total)",
                         counts["new"], counts["seen"], counts["deleted"], total)
                counts = {"seen": 0, "new": 0, "deleted": 0}
                last_report = time.monotonic()


async def run(conn, salt):
    """Keeps the Bluesky stream open forever. When a connection breaks it moves to the next server
    and waits twice as long each time (at most a minute), starting over once a connection held."""
    backoff = 1
    attempt = 0
    while True:
        host = config.JETSTREAM_HOSTS[attempt % len(config.JETSTREAM_HOSTS)]
        started = time.monotonic()
        health.beat(conn, "bluesky")  # still trying counts: a restart does not bring the network back
        try:
            await listen(conn, salt, host)
        except Exception as e:
            log.warning("%s: connection lost (%s), next server in %d s", host, type(e).__name__, backoff)
        if time.monotonic() - started > config.JETSTREAM_SILENCE_SECONDS:
            backoff = 1  # it worked for a while, so this is not a server that keeps refusing us
        await asyncio.sleep(backoff)
        backoff = min(backoff * 2, config.JETSTREAM_MAX_BACKOFF)
        attempt += 1
