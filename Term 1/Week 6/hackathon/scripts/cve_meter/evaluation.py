"""Phase 6: the honest test. Turning our labels into one reference per post, and counting how
often a model agrees with it.

Nothing here loads a model or reads a file, so it can be tested without either.
"""
from collections import Counter

from . import config

MODEL_B = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
MODEL_B_REVISION = "f2f1202b1bdeb07342385c3f807f9c07cd8f5cf8"  # fixed, like that of twitter-roberta-base-sentiment-latest
EVALUATION_DIR = config.ROOT / "evaluation"
MODELS_DIR = config.ROOT / "models"  # one folder per fine-tuned model, written by scripts/finetune.py

LABELS = ("alarmed", "neutral", "reassuring")
SKIP = "skip"
SHORT = {"a": "alarmed", "n": "neutral", "r": "reassuring", "s": SKIP}
# The model's three outputs, in the order sentiment.load() gives them
FROM_MODEL = ("alarmed", "neutral", "reassuring")


def clean_label(value):
    """What someone typed in the label column as one of LABELS or SKIP, or None when it is neither."""
    value = (value or "").strip().lower()
    value = SHORT.get(value, value)
    return value if value in LABELS or value == SKIP else None


def reference(labels):
    """One post's labels from every labeller -> (reference, all agreed).

    The reference is the label more than half of them chose, or None: then the post is left out
    of the scores. A 'skip' is a vote like any other, and a post most of us skipped is left out too.
    """
    label, votes = Counter(labels).most_common(1)[0]
    agreed = votes == len(labels)
    if votes * 2 <= len(labels) or label == SKIP:
        return None, agreed
    return label, agreed


def score(pairs):
    """(reference, predicted) pairs -> accuracy, and precision, recall and F1 for alarmed.

    A value is None when there is nothing to divide by: no post was called alarmed, or none was.
    """
    pairs = list(pairs)
    hits = sum(1 for truth, guess in pairs if truth == guess == "alarmed")
    called = sum(1 for _, guess in pairs if guess == "alarmed")
    real = sum(1 for truth, _ in pairs if truth == "alarmed")
    precision = hits / called if called else None
    recall = hits / real if real else None
    f1 = 2 * precision * recall / (precision + recall) if precision and recall else (0.0 if real and called else None)
    return {
        "posts": len(pairs),
        "alarmed": real,
        "accuracy": sum(1 for truth, guess in pairs if truth == guess) / len(pairs) if pairs else None,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


def confusion(pairs):
    """Counts per (reference, predicted), for the table in the report."""
    counts = Counter(pairs)
    return {truth: {guess: counts[(truth, guess)] for guess in LABELS} for truth in LABELS}


def good_enough(model, wordlist, recall=0.60, margin=0.15):
    """The two conditions we fixed before the test (README, "When is it good enough?")."""
    if model["recall"] is None or model["f1"] is None:
        return False
    return model["recall"] >= recall and model["f1"] >= (wordlist["f1"] or 0.0) + margin
