"""Phase 6: compare our labels with twitter-roberta-base-sentiment-latest, twitter-xlm-roberta-base-sentiment,
the fine-tuned versions of both and the word list.

Run from the project root, after our labels_<name>.csv is in evaluation/ (one file, as we
label together; with more files the reference is the label most of them chose):
    python scripts/run_test.py
Writes evaluation/test_table.csv (every post with our labels, the reference, every output and
where they disagree) and evaluation/results.json (read by the dashboard), and prints the table for the README.

    python scripts/run_test.py --trial some_labels.csv
runs the same comparison against one other file of labels, to try the scripts out. A trial
writes to evaluation/trial/ and not to results.json, unless --dashboard is given: then the
panel on the dashboard shows the trial, and says that it is one.
"""
import argparse
import csv
import json
import sys
from datetime import date
from pathlib import Path

from cve_meter import config, evaluation, metrics, sentiment, wordlist

parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
parser.add_argument("--dir", type=Path, default=evaluation.EVALUATION_DIR)
parser.add_argument("--trial", type=Path, help="one file with post_id and label, instead of our own labels")
parser.add_argument("--dashboard", action="store_true", help="with --trial: show the trial on the dashboard")
parser.add_argument("--skip-model-b", action="store_true", help="skip twitter-xlm-roberta-base-sentiment, when its weights are not downloaded yet")
args = parser.parse_args()

# The fine-tuned models by the name of their folder in models/, as the tables show them: named
# after the exact model they started from
FINE_TUNED = {
    "model-a-finetuned": f"{config.MODEL_A}, fine-tuned round 1 (365 posts)",
    "model-a-finetuned-2": f"{config.MODEL_A}, fine-tuned round 2 (900 posts)",
    "model-b-finetuned": f"{evaluation.MODEL_B}, fine-tuned round 1 (365 posts)",
    "model-b-finetuned-2": f"{evaluation.MODEL_B}, fine-tuned round 2 (900 posts)",
}


def shown(folder_name):
    """The name a fine-tuned model gets in the tables, from the name of its folder."""
    return FINE_TUNED.get(folder_name, f"Fine-tuned ({folder_name})")


def read_labels(path):
    """post_id -> label, for the rows that have one. Stops at a label it does not know."""
    labels = {}
    with path.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            if not (row.get("label") or "").strip():
                continue
            label = evaluation.clean_label(row["label"])
            if label is None:
                sys.exit(f"{path.name}, post {row['post_id']}: '{row['label']}' is not a label. "
                         f"Use {', '.join(evaluation.LABELS)} or {evaluation.SKIP}.")
            labels[int(row["post_id"])] = label
    return labels


if args.trial:
    labellers = {args.trial.stem: read_labels(args.trial)}
    out = args.dir / "trial"
else:
    labellers = {path.stem.removeprefix("labels_"): read_labels(path)
                 for path in sorted(args.dir.glob("labels_*.csv"))}
    out = args.dir
    if not labellers:
        sys.exit(f"Found no labels_<name>.csv in {args.dir}.")
names = list(labellers)

posts = {post["id"]: post for post in metrics.load_posts(metrics.connect())}

# Only the posts every labeller did: a post one of us forgot has no fair reference
ids = sorted(set.intersection(*(set(labels) for labels in labellers.values())) & set(posts))
missing = len(set.union(*(set(labels) for labels in labellers.values()))) - len(ids)
texts = [posts[post_id]["text"] for post_id in ids]


def run_model(name, revision):
    """Loads one model and gives its label for every test post: the label with the highest of the three scores."""
    classify = sentiment.load(name, revision)
    return [evaluation.FROM_MODEL[max(range(3), key=row.__getitem__)] for row in classify(texts)]


outputs = {config.MODEL_A: run_model(config.MODEL_A, config.MODEL_A_REVISION)}
if not args.skip_model_b:
    outputs[evaluation.MODEL_B] = run_model(evaluation.MODEL_B, evaluation.MODEL_B_REVISION)
for folder in sorted(evaluation.MODELS_DIR.glob("*/")):  # e.g. models/model-b-finetuned
    outputs[shown(folder.name)] = run_model(str(folder), None)
outputs["Word list"] = [wordlist.classify(text) for text in texts]
# The model the collector scores with: its alarm score is the one in the database
in_use = config.MODEL_A if config.PIPELINE_MODEL == config.MODEL_A else shown(config.PIPELINE_MODEL)

rows = []
for i, post_id in enumerate(ids):
    truth, agreed = evaluation.reference([labellers[name][post_id] for name in names])
    labels = {name: output[i] for name, output in outputs.items()}
    rows.append({"post_id": post_id, "language": posts[post_id]["language"],
                 "automated": posts[post_id]["automated"] or "", "text": " ".join(texts[i].split()),
                 **{f"label_{name}": labellers[name][post_id] for name in names},
                 "reference": truth or "", "all_agreed": int(agreed),
                 **labels,
                 # Where they disagree: the outputs that differ from our label, and the two downloaded models
                 # (twitter-roberta-base-sentiment-latest against twitter-xlm-roberta-base-sentiment)
                 "disagrees_with_us": "; ".join(name for name, label in labels.items() if truth and label != truth),
                 "roberta_vs_xlm_roberta": "" if evaluation.MODEL_B not in labels else
                                           "same" if labels[config.MODEL_A] == labels[evaluation.MODEL_B] else "different",
                 "alarm_score": round(posts[post_id]["negative"], 3)})
used = [row for row in rows if row["reference"]]

out.mkdir(parents=True, exist_ok=True)
with (out / "test_table.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)


def pairs(name, subset):
    """(our label, this model's label) for every post in the subset, ready to be counted."""
    return [(row["reference"], row[name]) for row in subset]


def show(value):
    """A score with two decimals, or 'n/a' when it cannot be calculated."""
    return "n/a" if value is None else f"{value:.2f}"


scores = {name: evaluation.score(pairs(name, used)) for name in outputs}

print(f"{len(rows)} posts labelled by {', '.join(names)}"
      + (f" ({missing} left out: not labelled by everyone)" if missing else ""))
if len(names) > 1:
    print(f"All agreed on {sum(row['all_agreed'] for row in rows)} of {len(rows)}; "
          f"{len(rows) - len(used)} left out of the scores (no majority, or skipped)")
alarmed = sum(1 for row in used if row["reference"] == "alarmed")
print(f"Reference: {alarmed} alarmed, {sum(1 for row in used if row['reference'] == 'neutral')} neutral, "
      f"{sum(1 for row in used if row['reference'] == 'reassuring')} reassuring"
      + ("" if alarmed >= 20 else "  <- fewer than 20 alarmed: label more, as the method says"))

print("\n| | Posts | Accuracy against our labels | Precision alarmed | Recall alarmed | F1 alarmed |\n|---|---|---|---|---|---|")
for name, s in scores.items():
    print(f"| {name} | {s['posts']} | {show(s['accuracy'])} | {show(s['precision'])} | "
          f"{show(s['recall'])} | {show(s['f1'])} |")

for name in outputs:
    print(f"\n{name}, reference down, output across ({', '.join(evaluation.LABELS)})")
    for truth, counts in evaluation.confusion(pairs(name, used)).items():
        print(f"  {truth:11}" + "".join(f"{counts[guess]:6}" for guess in evaluation.LABELS))

baseline = scores["Word list"]
print("\nGood enough by our two conditions (recall 0.60 or more, F1 at least 0.15 above the word list)?")
for name in outputs:
    if name != "Word list":
        print(f"  {name}: {'yes' if evaluation.good_enough(scores[name], baseline) else 'no'}")

print(f"\nWhere {in_use} was most sure and wrong (candidates for the three failures):")
wrong = [row for row in used if row[in_use] != row["reference"]]
for row in sorted(wrong, key=lambda row: abs(row["alarm_score"] - 0.5), reverse=True)[:8]:
    print(f"  post {row['post_id']}: we say {row['reference']}, the model says {row[in_use]} "
          f"(alarm score {row['alarm_score']}): {row['text'][:110]}")

if not args.trial or args.dashboard:
    results = {
        "posts": len(used),
        "tested": date.today().isoformat(),
        "models": [{"Model": name, "Posts": s["posts"], "Accuracy": show(s["accuracy"]),
                    "Precision alarmed": show(s["precision"]), "Recall alarmed": show(s["recall"]),
                    "F1 alarmed": show(s["f1"])} for name, s in scores.items()],
        "note": (f"We all chose the same label for {sum(row['all_agreed'] for row in rows)} of {len(rows)} posts. "
                 if len(names) > 1 else "") + f"{alarmed} of the posts in the test are alarmed.",
    }
    if args.trial:
        results["note"] = (f"Trial run, not the test described in the README. {alarmed} of the posts are alarmed. "
                           "The word list was written after reading these posts, so its score is flattering.")
    config.TEST_RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    config.TEST_RESULTS_PATH.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nWrote {config.TEST_RESULTS_PATH}")
print(f"Wrote {out / 'test_table.csv'}")
