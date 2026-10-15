"""Checks on phase 6: the scores count right, and the word list finds what it should.

Run from the project root:  python -m unittest discover -s scripts/tests -t scripts
"""
import unittest

from cve_meter import evaluation, wordlist


class Scores(unittest.TestCase):
    def test_reference_is_the_majority(self):
        self.assertEqual(evaluation.reference(["alarmed", "alarmed", "neutral"]), ("alarmed", False))
        self.assertEqual(evaluation.reference(["neutral"] * 3), ("neutral", True))
        self.assertEqual(evaluation.reference(["alarmed", "neutral", "reassuring"]), (None, False))
        self.assertEqual(evaluation.reference(["skip", "skip", "neutral"]), (None, False))

    def test_labels_as_typed(self):
        self.assertEqual(evaluation.clean_label(" A "), "alarmed")
        self.assertEqual(evaluation.clean_label("Reassuring"), "reassuring")
        self.assertIsNone(evaluation.clean_label("panic"))

    def test_precision_and_recall_for_alarmed(self):
        pairs = ([("alarmed", "alarmed")] * 3 + [("alarmed", "neutral")] * 1
                 + [("neutral", "alarmed")] * 2 + [("neutral", "neutral")] * 4)
        result = evaluation.score(pairs)
        self.assertAlmostEqual(result["precision"], 3 / 5)
        self.assertAlmostEqual(result["recall"], 3 / 4)
        self.assertAlmostEqual(result["f1"], 2 / 3)
        self.assertAlmostEqual(result["accuracy"], 0.7)

    def test_a_model_that_never_says_alarmed(self):
        result = evaluation.score([("alarmed", "neutral"), ("neutral", "neutral")])
        self.assertIsNone(result["precision"])
        self.assertEqual(result["recall"], 0)
        self.assertFalse(evaluation.good_enough(result, {"f1": 0.0}))

    def test_good_enough_needs_both_conditions(self):
        self.assertTrue(evaluation.good_enough({"recall": 0.7, "f1": 0.6}, {"f1": 0.4}))
        self.assertFalse(evaluation.good_enough({"recall": 0.5, "f1": 0.6}, {"f1": 0.4}))
        self.assertFalse(evaluation.good_enough({"recall": 0.7, "f1": 0.5}, {"f1": 0.4}))


class WordList(unittest.TestCase):
    def test_alarm_and_reassurance(self):
        self.assertEqual(wordlist.classify("CVE-2026-1 is actively exploited, patch now"), "alarmed")
        self.assertEqual(wordlist.classify("Exploited in-the-wild since May"), "alarmed")
        self.assertEqual(wordlist.classify("CVE-2026-1: buffer overflow in Product 2, CVSS 9.8"), "neutral")
        self.assertEqual(wordlist.classify("Not exploitable in the default configuration"), "reassuring")

    def test_reassurance_that_contains_an_alarm_phrase(self):
        self.assertEqual(wordlist.classify("No exploitation in the wild so far"), "reassuring")

    def test_whole_words_only(self):
        self.assertEqual(wordlist.classify("The Asaph library has a parsing bug"), "neutral")


if __name__ == "__main__":
    unittest.main()
