"""Language detection from the text itself. The language a post declares is often just the
app's default, and the sentiment model only reads English."""
import re

from . import clean, config

UNDETERMINED = "und"
# Links, CVE ids, '@user' and '#' say nothing about the language
NOISE_RE = re.compile(rf"https?://\S+|{clean.CVE_RE.pattern}|@user|#", re.IGNORECASE)


def strip_noise(text):
    """Removes the parts of a post that are in no language, so the detector judges only the words."""
    return " ".join(NOISE_RE.sub(" ", text).split())


def load(languages=config.LANGUAGES):
    """Returns a function that takes a text and gives (language code, confidence)."""
    from lingua import IsoCode639_1, Language, LanguageDetectorBuilder

    detector = LanguageDetectorBuilder.from_languages(
        *[Language.from_iso_code_639_1(getattr(IsoCode639_1, code.upper())) for code in languages]
    ).build()

    def detect(text):
        """The language of one text as a two-letter code, with the detector's confidence.
        A text with too few letters is undetermined."""
        text = strip_noise(text)
        if sum(c.isalpha() for c in text) < config.LANGUAGE_MIN_LETTERS:
            return UNDETERMINED, None
        best = detector.compute_language_confidence_values(text)[0]
        return best.language.iso_code_639_1.name.lower(), best.value

    return detect
