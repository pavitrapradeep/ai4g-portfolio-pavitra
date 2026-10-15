"""Phase 6, extra: fine-tune a sentiment model on labelled posts.

Run from the project root, on a machine with some memory to spare (a laptop is enough):
    python scripts/finetune.py
Reads evaluation/train.csv (post_id, text, label). Without options it starts from
cardiffnlp/twitter-xlm-roberta-base-sentiment and writes to models/model-b-finetuned/. The command
for cardiffnlp/twitter-roberta-base-sentiment-latest, the one the collector uses, is in
docs/workflow.md, section 9. Copy the folder it wrote to the machine that runs the test;
run_test.py scores every folder in models/ next to the other models.

The model keeps its three outputs: alarmed is trained as its negative, neutral as neutral and
reassuring as positive, so the rest of the pipeline reads it like any other sentiment model.
One post in seven is kept apart to watch the training with; it is not the test.
"""
import argparse
import csv
import random
from pathlib import Path

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from cve_meter import config, evaluation, sentiment

TO_MODEL = {"alarmed": "negative", "neutral": "neutral", "reassuring": "positive"}

parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
parser.add_argument("--train", type=Path, default=evaluation.EVALUATION_DIR / "train.csv")
parser.add_argument("--out", type=Path, default=evaluation.MODELS_DIR / "model-b-finetuned")
parser.add_argument("--base", default=evaluation.MODEL_B, help="the model to start from")
parser.add_argument("--revision", default=evaluation.MODEL_B_REVISION)
parser.add_argument("--epochs", type=int, default=4)
parser.add_argument("--batch", type=int, default=8)
parser.add_argument("--rate", type=float, default=2e-5)
parser.add_argument("--max-tokens", type=int, default=256, help="longer posts are cut off while training")
parser.add_argument("--limit", type=int, help="use only this many posts, to try the script out")
args = parser.parse_args()

random.seed(6)
torch.manual_seed(6)
device = "cuda" if torch.cuda.is_available() else "cpu"

with args.train.open(newline="", encoding="utf-8-sig") as f:
    rows = [(sentiment.prepare(row["text"]), row["label"]) for row in csv.DictReader(f)
            if row["label"] in TO_MODEL]
random.shuffle(rows)
rows = rows[:args.limit] if args.limit else rows
check, train = rows[:len(rows) // 7], rows[len(rows) // 7:]
print(f"{len(train)} posts to train on, {len(check)} to watch with, on {device}")

tokenizer = AutoTokenizer.from_pretrained(args.base, revision=args.revision)
model = AutoModelForSequenceClassification.from_pretrained(
    args.base, revision=args.revision).to(device)
label_id = {name.lower(): i for name, i in model.config.label2id.items()}


def batches(posts):
    """Cuts the posts into groups of the batch size and gives each group as model input with its
    labels as numbers."""
    for start in range(0, len(posts), args.batch):
        part = posts[start:start + args.batch]
        inputs = tokenizer([text for text, _ in part], padding=True, truncation=True,
                           max_length=args.max_tokens, return_tensors="pt").to(device)
        yield inputs, torch.tensor([label_id[TO_MODEL[label]] for _, label in part], device=device)


steps = args.epochs * -(-len(train) // args.batch)
optimizer = torch.optim.AdamW(model.parameters(), lr=args.rate, weight_decay=0.01)
schedule = torch.optim.lr_scheduler.LinearLR(optimizer, start_factor=1.0, end_factor=0.0, total_iters=steps)
alarmed = label_id["negative"]
for epoch in range(1, args.epochs + 1):
    model.train()
    random.shuffle(train)
    total = 0.0
    for inputs, labels in batches(train):
        loss = model(**inputs, labels=labels).loss
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        schedule.step()
        optimizer.zero_grad()
        total += loss.item() * len(labels)
    model.eval()
    pairs = []
    with torch.no_grad():
        for inputs, labels in batches(check):
            pairs += zip(labels.tolist(), model(**inputs).logits.argmax(dim=1).tolist())
    found = sum(1 for truth, guess in pairs if truth == guess == alarmed)
    called = sum(1 for _, guess in pairs if guess == alarmed)
    real = sum(1 for truth, _ in pairs if truth == alarmed)
    print(f"epoch {epoch}: loss {total / len(train):.3f}; of the {real} alarmed posts kept apart "
          f"{found} found, {called - found} false alarms")

args.out.mkdir(parents=True, exist_ok=True)
model.save_pretrained(args.out)
tokenizer.save_pretrained(args.out)
print(f"Wrote {args.out}")
