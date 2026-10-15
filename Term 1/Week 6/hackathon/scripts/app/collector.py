"""The collector. Reads Mastodon and Bluesky and stores every post that names a CVE (phase 1),
scores each stored post with the sentiment model (phase 2), looks up each CVE in the NVD,
the CISA list and the watchlist (phase 3) and keeps a record of its own health (phase 4).

Run from the project root, with the project's own Python:  .venv/bin/python scripts/app/collector.py
(on Windows: .venv\\Scripts\\python.exe scripts/app/collector.py). Stop with Ctrl+C. It can be started
again at any time; posts it already has are skipped, and posts without a score and CVEs
without a lookup are caught up. How it keeps itself going: docs/workflow.md.
"""
import asyncio
import importlib.util
import logging
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cve_meter import bluesky, clean, config, db, enricher, health, mastodon, scorer  # noqa: E402


async def main():
    """Opens the database and runs the five parts side by side: the two readers, the scorer, the
    enricher and the health check. If one of them crashes, the whole collector stops so it is started again."""
    conn = db.connect()
    salt = clean.load_salt(config.SALT_PATH)
    logging.info("collector started, database: %s", config.DB_PATH)
    try:
        await asyncio.gather(mastodon.run(conn, salt), bluesky.run(conn, salt), scorer.run(),
                             enricher.run(), health.run())
    except Exception:
        logging.exception("collector crashed")
        os._exit(1)  # not sys.exit: that would wait for the lookups that are under way


if __name__ == "__main__":
    config.DATA_DIR.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(), logging.FileHandler(config.LOG_PATH, encoding="utf-8")],
    )
    for noisy in ("websockets", "httpx", "httpx2", "huggingface_hub"):
        logging.getLogger(noisy).setLevel(logging.WARNING)
    # Two collectors on one database lock each other out, and a collector that cannot score
    # stores posts nobody analyses. Both look fine from the outside, so neither may start.
    lock = health.lock()
    if lock is None:
        logging.error("another collector is already running on this database, not starting a second one")
        sys.exit(health.NO_RESTART)
    missing = [m for m in ("lingua", "torch", "transformers") if importlib.util.find_spec(m) is None]
    if missing:
        logging.error("%s not installed in %s. Start the collector with the project's own Python"
                      " (.venv), or run: pip install -r requirements.txt", ", ".join(missing), sys.executable)
        sys.exit(health.NO_RESTART)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("collector stopped")
