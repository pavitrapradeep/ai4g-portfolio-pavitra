"""The sentiment model: a pre-trained transformer from Hugging Face that runs on this machine.

The weights (about 500 MB) are downloaded once and cached. After that no internet is needed.
"""
import re

from . import config

LINK_RE = re.compile(r"https?://\S+")


def prepare(text):
    """The model card: links become 'http', as in the tweets the model was trained on.

    User names are already '@user' in the database.
    """
    return LINK_RE.sub("http", text)


def load(model=config.MODEL_A, revision=config.MODEL_A_REVISION):
    """Returns a function that takes texts and gives (negative, neutral, positive) for each."""
    import transformers  # imported here: it takes seconds and the tests do not need it
    from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

    transformers.logging.set_verbosity_error()  # keep its load report out of the collector log
    transformers.logging.disable_progress_bar()

    def parts(local_only):
        """The model weights and its tokenizer, from the local cache only or with a download."""
        return (AutoModelForSequenceClassification.from_pretrained(model, revision=revision, local_files_only=local_only),
                AutoTokenizer.from_pretrained(model, revision=revision, local_files_only=local_only))

    try:
        weights, tokenizer = parts(local_only=True)  # from the cache, without contacting Hugging Face
    except OSError:
        weights, tokenizer = parts(local_only=False)  # the first time: download
    # top_k=None: all three probabilities, not only the winning label
    pipe = pipeline("sentiment-analysis", model=weights, tokenizer=tokenizer, top_k=None, device=-1)

    def classify(texts):
        """Runs the texts through the model in batches and gives (negative, neutral, positive) per text.
        Texts longer than the model can read are cut off."""
        results = pipe([prepare(t) for t in texts], batch_size=config.SCORE_BATCH_SIZE,
                       truncation=True, max_length=config.MODEL_MAX_TOKENS)
        rows = []
        for result in results:
            p = {item["label"].lower(): item["score"] for item in result}
            rows.append((p["negative"], p["neutral"], p["positive"]))
        return rows

    return classify
