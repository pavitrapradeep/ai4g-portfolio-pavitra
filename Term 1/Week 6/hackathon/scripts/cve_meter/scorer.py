"""Phase 2: give every stored post a detected language and a sentiment score.

It works from the database, not from the stream: whatever has no score yet gets one. That
covers posts stored before this existed and posts stored while the model was not running.
"""
import asyncio
import functools
import logging

from . import config, db, health, language, sentiment

log = logging.getLogger("scorer")


def detect_pending(conn, detect):
    """Returns the number of posts that got a language."""
    posts = db.posts_without_language(conn)
    for post_id, text in posts:
        db.set_language(conn, post_id, *detect(text))
    return len(posts)


def score_pending(conn, model, classify):
    """Returns the number of posts that got a score."""
    posts = db.posts_without_score(conn, model)
    for start in range(0, len(posts), config.SCORE_BATCH_SIZE):
        batch = posts[start:start + config.SCORE_BATCH_SIZE]
        scores = classify([text for _, text in batch])
        db.insert_scores(conn, model, [(post_id, *score) for (post_id, _), score in zip(batch, scores)])
        health.beat(conn, "scorer")  # per batch: a backlog can take longer than the monitor waits
    return len(posts)


@functools.cache
def _tools():
    """Loads the language detector and the sentiment model. Cached: loading takes seconds,
    so it happens once per run."""
    log.info("loading the language detector and %s", config.PIPELINE_MODEL)
    return language.load(), sentiment.load(config.PIPELINE_SOURCE, config.PIPELINE_REVISION)


def run_once():
    """One round, with its own database connection because it runs in a separate thread."""
    detect, classify = _tools()
    conn = db.connect()
    try:
        detected = detect_pending(conn, detect)
        scored = score_pending(conn, config.PIPELINE_MODEL, classify)
        health.beat(conn, "scorer")
    finally:
        conn.close()
    if detected or scored:
        log.info("%d posts scored, %d languages detected", scored, detected)
    return scored


async def run():
    """Scores the posts that have no score yet, waits SCORE_SECONDS and starts again, forever.
    A failed round is logged and tried again."""
    while True:
        try:
            # In a thread, so the collector keeps reading while the model is busy
            await asyncio.to_thread(run_once)
        except Exception as e:
            log.warning("scoring failed, trying again in %d s: %s: %s", config.SCORE_SECONDS, type(e).__name__, e)
        await asyncio.sleep(config.SCORE_SECONDS)
