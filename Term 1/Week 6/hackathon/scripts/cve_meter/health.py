"""Phase 4: what keeps the collector going for days without anyone watching.

Only one collector runs at a time (lock). Every part reports that it is still going (beat),
and when one has gone quiet the collector stops itself, so that whatever started it starts a
fresh one. Meanwhile it adds a line to health.csv every few minutes, which is the record that
it ran, and it copies the database to a backup.
"""
import asyncio
import contextlib
import csv
import logging
import os
import sqlite3
from datetime import datetime, timedelta, timezone

from . import config, db

log = logging.getLogger("health")
PARTS = ("mastodon", "bluesky", "scorer", "enricher")
COLUMNS = ("time", "posts", "scored", "cves", "looked_up", "start")
NO_RESTART = 2  # exit code for "starting again will not help"


def lock(path=config.LOCK_PATH):
    """Returns the locked file, or None when another collector holds it.

    The lock lasts as long as the file stays open. The system releases it when the process
    ends, however it ends, so a crash never leaves a lock behind.
    """
    f = open(path, "a")
    try:
        if os.name == "nt":
            import msvcrt
            f.seek(0)
            msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        f.close()
        return None
    return f


def beat(conn, part):
    """Called by a part of the collector every time it has done a piece of work."""
    db.set_state(conn, f"heartbeat_{part}", db.utc_iso(datetime.now(timezone.utc)))


def quiet(conn, started, now):
    """The parts that reported nothing for too long. One that never did counts from the start."""
    limit = db.utc_iso(now - timedelta(seconds=config.QUIET_SECONDS))
    return [part for part in PARTS
            if max(db.get_state(conn, f"heartbeat_{part}") or "", db.utc_iso(started)) < limit]


def record(conn, now, start, path=config.HEALTH_PATH):
    """Add one line to health.csv: the time and how many rows there are."""
    counts = conn.execute(
        "SELECT (SELECT COUNT(*) FROM posts), (SELECT COUNT(DISTINCT post_id) FROM scores),"
        " (SELECT COUNT(*) FROM cves), (SELECT COUNT(*) FROM cves WHERE checked_at IS NOT NULL)"
    ).fetchone()
    new = not path.exists()
    with open(path, "a", newline="", encoding="ascii") as f:
        writer = csv.writer(f)
        if new:
            writer.writerow(COLUMNS)
        writer.writerow([db.utc_iso(now), *counts, int(start)])


def read(path=config.HEALTH_PATH):
    """The lines of health.csv, with the time as a datetime."""
    with open(path, newline="", encoding="ascii") as f:
        return [dict(row, time=datetime.strptime(row["time"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc))
                for row in csv.DictReader(f)]


def stretches(times, gap=2 * config.HEALTH_SECONDS):
    """The periods in which the collector was running, as (first, last) pairs of times from health.csv.

    Lines at most 10 minutes apart belong to the same period, so only time the collector really
    ran is counted towards the 48 hours.
    """
    found = []
    for t in times:
        if found and (t - found[-1][1]).total_seconds() <= gap:
            found[-1][1] = t
        else:
            found.append([t, t])
    return [tuple(stretch) for stretch in found]


def backup(now, source=config.DB_PATH, folder=config.BACKUP_DIR):
    """Copy the database, unless the newest copy is recent enough. Returns the new file or None.

    SQLite's own backup is used because it also takes what is still in the -wal file. A plain
    copy of the .db file can miss most of the data.
    """
    folder.mkdir(exist_ok=True)
    copies = sorted(folder.glob("cve_meter-*.db"))
    if copies and now.timestamp() - copies[-1].stat().st_mtime < config.BACKUP_HOURS * 3600:
        return None
    target = folder / f"cve_meter-{now:%Y%m%d-%H%M}.db"
    with contextlib.closing(sqlite3.connect(source)) as src, contextlib.closing(sqlite3.connect(target)) as dst:
        src.backup(dst)
    for old in copies[:max(0, len(copies) + 1 - config.BACKUPS_KEPT)]:
        old.unlink()
    return target


async def run():
    """Checks every minute whether each part still reports. A part that is silent too long stops the
    collector so it is started again. Every HEALTH_SECONDS it also writes a line to health.csv and
    makes a backup when one is due."""
    conn = db.connect()
    started = datetime.now(timezone.utc)
    recorded = None
    while True:
        now = datetime.now(timezone.utc)
        stuck = quiet(conn, started, now)
        if stuck:
            log.error("%s reported nothing for %d minutes: stopping, so the collector is started again",
                      ", ".join(stuck), config.QUIET_SECONDS // 60)
            os._exit(1)  # not sys.exit: that would wait for the part that is stuck
        if recorded is None or (now - recorded).total_seconds() >= config.HEALTH_SECONDS:
            try:
                record(conn, now, start=recorded is None)
                copy = backup(now)
                if copy:
                    log.info("database copied to %s", copy)
            except Exception as e:  # a full disk, or health.csv open in Excel: keep collecting
                log.warning("health record or backup failed: %s: %s", type(e).__name__, e)
            recorded = now
        await asyncio.sleep(60)
