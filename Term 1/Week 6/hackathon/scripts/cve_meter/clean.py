"""Text cleaning and pseudonymisation. Everything here runs before a post is stored."""
import hashlib
import hmac
import html
import re
import secrets

CVE_RE = re.compile(r"CVE-\d{4}-\d{4,}", re.IGNORECASE)
# @name, @name.bsky.social and @name@server.example
MENTION_RE = re.compile(r"@\w+(?:[.-]\w+)*(?:@\w+(?:[.-]\w+)*)?")


def html_to_text(content):
    """Turn Mastodon's HTML into plain text."""
    text = re.sub(r"<br\s*/?>|</p>", "\n", content)
    # Mastodon splits a link over several <span>s, so tags are removed without a space
    text = html.unescape(re.sub(r"<[^>]+>", "", text))
    return re.sub(r"\s+", " ", text).strip()


def hide_mentions(text):
    """Replaces every @name in a text with '@user', so no account name is stored."""
    return MENTION_RE.sub("@user", text)


def extract_cves(text):
    """All different CVE ids in the text, in upper case."""
    return sorted({m.upper() for m in CVE_RE.findall(text)})


def load_salt(path):
    """Read the secret salt, or create it on the first run. It never goes into the repository."""
    if not path.exists():
        path.write_text(secrets.token_hex(32), encoding="ascii")
    return path.read_text(encoding="ascii").strip().encode("ascii")


def salted_hash(salt, value):
    """Same value gives the same hash, but without the salt nobody can check a guess."""
    return hmac.new(salt, value.encode("utf-8"), hashlib.sha256).hexdigest()
