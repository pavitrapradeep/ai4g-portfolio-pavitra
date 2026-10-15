"""The watchlist: product names that matter to our user, matched against what we know of a CVE."""
import re

from . import config


def load(path=config.WATCHLIST_PATH):
    """The terms in the file, one per line. Empty lines and lines starting with # are skipped."""
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    return [line.strip() for line in lines if line.strip() and not line.lstrip().startswith("#")]


def find(terms, text):
    """The first term that is in the text as whole words, in any case. None if there is none."""
    for term in terms:
        # "Exchange Server" must not match "exchange servers", nor "ESXi" match "ESXiArgs"
        if re.search(rf"(?<!\w){re.escape(term)}(?!\w)", text, re.IGNORECASE):
            return term
    return None
