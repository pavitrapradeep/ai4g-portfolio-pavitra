"""Phase 6: the baseline without machine learning. A post is alarmed when it contains an alarm
phrase, reassuring when it contains a reassuring one, and neutral otherwise.

The lists hold what security people say when they warn or wave something off. Fix them before
the labels are compared with anything: changing them after seeing the results would make the
comparison worthless.
"""
import re

ALARM = [
    "actively exploited", "active exploitation", "exploited in the wild",
    "under attack", "under active attack", "being exploited", "zero-day", "0-day", "zero day",
    "patch now", "patch immediately", "update now", "update immediately", "upgrade now",
    "upgrade immediately", "asap", "urgent", "emergency", "ransomware", "mass exploitation",
    "no patch", "unpatched", "cisa kev",
]
REASSURING = [
    "not exploitable", "not exploited", "none exploited", "no exploitation", "no known exploitation",
    "no evidence of exploitation", "low impact", "low severity", "low risk", "overhyped", "overblown",
    "false positive", "not affected", "unaffected", "only if", "nothing to worry",
]


def pattern(phrases):
    """One regular expression that finds any of the phrases, in upper or lower case."""
    # Whole words, so "asap" does not match inside another word; spaces and hyphens are alike
    parts = [re.escape(phrase).replace(r"\ ", r"[\s-]+").replace(r"\-", r"[\s-]?") for phrase in phrases]
    return re.compile(r"(?<!\w)(?:" + "|".join(parts) + r")(?!\w)", re.IGNORECASE)


ALARM_RE = pattern(ALARM)
REASSURING_RE = pattern(REASSURING)


def classify(text):
    """'alarmed', 'neutral' or 'reassuring'. Alarm wins when a post has both kinds of phrase,
    except where the alarm phrase is part of the reassuring one ("no exploitation in the wild")."""
    calm = REASSURING_RE.search(text)
    if ALARM_RE.search(REASSURING_RE.sub(" ", text)):
        return "alarmed"
    return "reassuring" if calm else "neutral"
