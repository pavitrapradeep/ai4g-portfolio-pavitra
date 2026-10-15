# How it actually works

What happens between someone posting about a vulnerability and a number on our dashboard, and
how we know whether that number can be trusted. Written so that each of us can explain every
step in the presentation. The practical part (where it runs, which command) is at the end.

## 1. One post, from start to finish

Take this post. It is made up, but the numbers below are what our models really give for it.

> Heads up @alice@infosec.example: CVE-2026-12345 in Citrix NetScaler is being exploited in the
> wild. Patch now! https://example.org/advisory #CVE

| Step | What happens to it |
|---|---|
| Fetch | It carries `#CVE`, so it shows up when we ask mastodon.social for the newest posts under that hashtag. |
| Filter | The text is searched for the pattern `CVE-` + four digits + `-` + four or more digits. It finds `CVE-2026-12345`, so the post is kept. Without a CVE id it would be thrown away here. |
| Hide the person | `@alice@infosec.example` becomes `@user`. The author's account address is replaced by a hash. The author's name is never written to disk. |
| Store | One row in `posts` with the text and the time, one row in `post_cves` linking it to `CVE-2026-12345`. |
| Language | A language detector reads the text without links, CVE ids and hashtags: English, 73% sure. |
| Score | The link becomes the word `http` (the model was trained that way) and the text goes through the model. Out come three probabilities that add up to 1. |
| Look up | `CVE-2026-12345` is new to us, so it is looked up in the NVD and the CISA list. "Citrix NetScaler" is on our watchlist, so the CVE gets that tag. |
| Show | Within a minute the post counts in the average of its hour and of its CVE on the dashboard. |

What the models say about this post:

| | negative | neutral | positive | Result |
|---|---|---|---|---|
| `twitter-roberta-base-sentiment-latest` as downloaded | 0.57 | 0.41 | 0.02 | alarm score 0.57 |
| `twitter-roberta-base-sentiment-latest` fine-tuned (the one the collector runs) | 1.00 | 0.00 | 0.00 | alarm score 1.00 |
| Word list | | | | alarmed, because of "exploited in the wild" and "patch now" |

And for a plain announcement, "CVE-2026-23456 (CVSS 9.8 CRITICAL): buffer overflow in
ExampleCMS before 4.2 allows remote code execution": `twitter-roberta-base-sentiment-latest` gives 0.31 negative, the
fine-tuned model 0.00, the word list says neutral. This is the difference the fine-tuning made:
the original model hears "critical" and "overflow" as somewhat negative, the fine-tuned one has
learned that an announcement in a fixed form is not alarm.

**The alarm score of a post is the probability the model gives to "negative".** Nothing else.
Everything on the dashboard is an average of that one number over a group of posts.

## 2. Collecting

The two sources work in opposite ways.

**Mastodon: we ask.** Every 5 minutes the collector asks two servers (mastodon.social and
hachyderm.io) for the newest 40 posts under each of four hashtags (`#CVE`, `#infosec`,
`#vulnerability`, `#PatchTuesday`). That is 8 requests per round, without a key. Most of what
comes back we already have or has no CVE id; only the rest is stored. Before each round the
collector reads the server's own setting and skips a server that has closed its hashtag feeds.
If more than 40 new posts appeared under one hashtag within 5 minutes, we miss some, and the
log says so.

**Bluesky: we listen.** The collector keeps one connection open to Jetstream, Bluesky's public
stream, which sends every new public post of the whole network: more than 2,000 a minute. We
read all of them and keep only those with a CVE id, a few per 5 minutes. Every 5 minutes the
collector saves how far it has read. After a break it asks Jetstream to continue from that
point, so a short outage loses nothing. If an author deletes a post, Jetstream tells us and we
delete our copy.

**What both do before storing:**

- The same post seen on two Mastodon servers is stored once. Each post gets a key made from its
  address, and the database refuses a key it already has.
- Mastodon accounts that ask not to be indexed (the `noindex` setting, or `#nobot` / `#noindex`
  in the profile) are skipped entirely.
- The account becomes a salted hash. The same account always gives the same hash, so we can
  count "how many different accounts", but nobody can turn the hash back into a name, and
  without our secret `salt.txt` nobody can check a guess either.
- For Mastodon we also keep three hints about automation: the server's own bot flag, whether
  the profile calls itself a bot or feed, and whether the account has posted more than 50 times
  a day since it was made. Only the outcome is stored, not the profile.

## 3. The model

A sentiment model is a neural network that has read a great many texts with a label and has
learned which patterns of words go with which label. Ours is
`cardiffnlp/twitter-roberta-base-sentiment-latest`: trained on about 124 million tweets, then
taught three labels (negative, neutral, positive).

What happens when a post is scored:

1. The text is cut into tokens, pieces of words the model knows. At most 512; anything longer is
   cut off.
2. The tokens go through the network, which looks at every token in the context of all the
   others. That is how it can tell "not exploited" from "exploited".
3. The last layer gives three numbers, one per label, which are turned into probabilities that
   add up to 1.

It runs on the processor of the machine the collector is on, about a second per post. Nothing is sent to Hugging Face or
any other service; the model file is downloaded once.

The scorer does not sit in the stream. Once a minute it asks the database "which posts have no
score from the current model yet?" and scores those, 16 at a time. That is why the collector
can be stopped and started without losing or doubling anything, and why switching to the
fine-tuned model scored all the older posts again by itself.

**Why "negative" and not something made for security?** No such model exists ready-made. We
use general mood as a stand-in for alarm, and the honest test (section 6) measures how good that
stand-in is. Section 7 is our attempt to make it better.

**Posts that are not in English** get a score too, but the model cannot read them. The
dashboard marks them.

## 4. From scores to the numbers on the dashboard

The dashboard stores nothing. Every time it reloads (once a minute) it reads all scored posts
and calculates everything again. The steps, in order:

**Step 1: set automated accounts aside.** A feed that posts every new CVE in the same form
would drown out the people. An account counts as automated for the first reason that applies:

| Reason | Rule |
|---|---|
| flag | Mastodon marks it as a bot |
| bio | its name or profile contains bot, feed, rss, automated or alerts |
| rate | more than 50 posts a day since the account was made |
| template | at least 3 of its posts, and at least half of them, have the same form |
| burst | 3 posts about CVEs within 2 minutes |
| volume | more than 12 posts about CVEs within 24 hours |

"The same form" means: replace every CVE id, link and number by a placeholder, then compare the
first three and the last three words. A feed writes "CVE-… (CVSS …): <title> https://… #cve"
every time; the title changes, the start and end do not. By default these accounts are left
out; a switch on the dashboard counts them in.

**Step 2: group.** For the line chart, posts are grouped by the hour they were posted. For the
table, by CVE over the last 24 hours. A post that names three CVEs counts for all three.

**Step 3: cap per account.** Within one group an account counts at most 3 times (its newest 3
posts). Otherwise one researcher who posts thirty times about their own find decides the line.

**Step 4: average.** The alarm of the group is the plain average of the alarm scores that are
left. Example: an hour with five posts scoring 1.00, 0.90, 0.10, 0.00 and 0.00 has alarm 0.40.

**Step 5: say how much it rests on.** A group with fewer than 5 counted posts or fewer than 3
different accounts is marked "low data". It is still shown, because a single worried post can
be the one that matters, but it sorts below the groups with enough data.

**Step 6: order the table.** Watchlist CVEs first, then enough data before low data, then the
highest alarm.

Clicking a point or a row shows the posts behind it, so the user can always read what the
number is made of.

## 5. The official sources

For every CVE that appears in a post, once a minute:

- **NVD.** One request per CVE gives the description, the affected products and the CVSS score.
  A record can hold several scores. We take the NVD's own if there is one, otherwise the
  vendor's, and the dashboard says which. Many new CVEs have no score yet: those are looked up
  again every 2 hours while people still post about them, and once a day after that. A score
  from the NVD itself is final and is never requested again. We wait 6 seconds between two
  requests, as the NVD asks.
- **CISA.** The list of vulnerabilities known to be exploited is one file. We download it once
  an hour and check every CVE against it.
- **Watchlist.** `watchlist.txt` holds product names a municipality cares about. A CVE gets the
  tag when a name appears, as whole words, in the NVD description or product list, in the CISA
  entry, or in a post about it, in that order.

This is what gives the alarm its meaning. Alarm alone is noise. Alarm next to "no official
score yet" and "on the watchlist" is the case our user wants to see first: people who know are
worried, and the official sources have not caught up.

## 6. The honest test

The question: when the model says "alarmed", is it right, and how many alarmed posts does it
miss?

The test is 100 posts from our own stream that we labelled by hand. Every model labels the same
100 posts (its label is the highest of its three probabilities), and 20 of those posts are
alarmed according to our own labels. How we labelled them, the bar we set beforehand and the
results are in the [README](../README.md#the-honest-test). Here is what the counting means.

The four numbers, with the model the collector uses (`twitter-roberta-base-sentiment-latest`, fine-tuned in the second round)
as the example:

| Number | Question it answers | Example |
|---|---|---|
| Accuracy | Of all posts, how often did the model pick our label? | 94 of 100: 0.94 |
| Precision | Of the posts the model called alarmed, how many really were? | it called 22 alarmed, 18 were: 0.82 |
| Recall | Of the posts that really were alarmed, how many did it find? | 18 of 20: 0.90 |
| F1 | One number that is only high when precision and recall both are | 0.86 |

Accuracy alone misleads: most posts are neutral, so a model that always says "neutral" scores
high on accuracy and finds no alarm at all. That is why we look at precision and recall for
alarmed.

**The word list** is the comparison without machine learning: a post is alarmed when it
contains one of 23 phrases such as "exploited in the wild", "zero-day" or "patch now",
reassuring when it contains one of 16 such as "not affected" or "low severity", and neutral
otherwise. We fixed the lists before looking at any result. The full lists are in
[`wordlist.py`](../scripts/cve_meter/wordlist.py).

The results of all models on these 100 posts are in the [README](../README.md#results) and on
the dashboard.

## 7. Fine-tuning

Fine-tuning continues the training of the downloaded model on our own kind of text, so that
"negative" moves towards what we mean by "alarmed".

1. **More posts.** We fetched a week of older Mastodon posts, once, with the same
   rules as the collector, into a separate database. Posts the collector already had were left
   out, so nothing we test on is in the training set.
2. **Labels.** 365 posts got a label. These were made by an AI assistant with our labelling
   guide. We checked those labels by hand and corrected the ones we disagreed with.
3. **Train.** `scripts/finetune.py` shows the model the posts in groups of 8, compares its
   answer with the label, and nudges all its weights a little towards the right answer. Four
   rounds over all posts. One post in seven is kept apart to watch whether it is still
   improving. Alarmed is trained as the model's "negative", neutral as "neutral", reassuring as
   "positive", so the rest of our code does not have to change.
4. **Test.** The 100 test posts, which the model never saw.
5. **Second round.** The same steps with more training posts: 234 more of the older Mastodon
   posts and 301 posts from our collector, labelled with the same guide. Together with the 365
   of the first round that makes 900, with every text that is also in the test left out. We
   trained both models again on those 900 and tested them on the same 100.

The result is a new folder with model files, the same size as the original. The collector uses
it when the folder `models/model-a-finetuned-2/` (the second round) exists and the original model
A when it does not (`config.py`). Scores are stored per model, so all sets are in the database.

The results of both rounds, and what limits them, are in the [README](../README.md#results).
The two rounds are tested on the same 100 posts; what differs is the training data. In the
second round the same accounts are in the training set and in the test, which makes it easier.

## 8. How it keeps running

- **Heartbeat.** Each of the four parts (Mastodon, Bluesky, scorer, lookups) writes the time
  into the database whenever it has done work. If one is silent for 15 minutes, the collector
  stops itself on purpose and is started again by whatever runs it.
- **The record.** Every 5 minutes one line goes to `data/health.csv`: the time and how many
  posts, scores and CVEs there are. A stopped collector writes nothing, so this file shows when
  the collector really ran. It is our evidence for the 48 hours. Post times cannot be: a quiet
  hour looks the same as a collector that is off.
- **How the hours are counted.** The time between two lines counts when they are at most 10
  minutes apart. A restart takes seconds and costs nothing.
- **Backups.** Every 6 hours the database is copied to `data/backups/`; the newest 8 are kept.
- **One at a time.** A second collector on the same database sees the lock and refuses to start.

## 9. Where it runs and what to type

**The code** is in this repository; everyone pushes to `main`. **The running tool** is two
programs on one machine that stays on: the collector and the dashboard. That machine does not
update itself: new code only goes live after a pull and a restart there. **The data** is on that
machine; what we submit is exported to `export/`.

| Path | What | In git? |
|---|---|---|
| `scripts/app/` | The two programs: `collector.py` and `dashboard.py` | yes |
| `scripts/cve_meter/` | All the logic; every setting and threshold named above is in `config.py` | yes |
| `scripts/*.py` | Things we run by hand: `db_status.py`, `run_test.py`, `finetune.py` | yes |
| `scripts/tests/` | Unit tests, no network and no model needed | yes |
| `evaluation/` | Our 100 labels, the test results and the 900 posts we trained on (`train.csv`) | yes |
| `docs/` | The labelling guide and this page | yes |
| `rubric/` | The assignment and the rubric from school | yes |
| `export/` | The collected data as CSV: posts, CVEs, the record of the run | yes |
| `data/` | Database, log, `health.csv`, backups | **no** |
| `models/` | Fine-tuned models, about 500 MB each | **no** |
| `.env`, `salt.txt` | NVD key and contact address; the salt for hashing accounts | **no**, never |

Which file does what:

| File in `scripts/cve_meter/` | Section above |
|---|---|
| `mastodon.py`, `bluesky.py`, `clean.py` | 2. Collecting |
| `sentiment.py`, `scorer.py`, `language.py` | 3. The model |
| `metrics.py` | 4. From scores to numbers |
| `enricher.py`, `nvd.py`, `kev.py`, `watchlist.py` | 5. The official sources |
| `evaluation.py`, `wordlist.py` | 6. The honest test |
| `health.py` | 8. How it keeps running |
| `db.py` | The four tables: `posts`, `post_cves`, `scores` (one row per post per model), `cves` |

From the project root:

| I want to | Command |
|---|---|
| run the tests | `python -m unittest discover -s scripts/tests -t scripts` |
| run the collector | `python scripts/app/collector.py` |
| see what is stored, and how far the 48 hours and 300 posts are | `python scripts/db_status.py` |
| fine-tune `twitter-roberta-base-sentiment-latest` again | `python scripts/finetune.py --base cardiffnlp/twitter-roberta-base-sentiment-latest --revision 3216a57f2a0d9c45a2e6c20157c20c49fb4bf9c7 --out models/model-a-finetuned-2` |
| read the log | open `data/collector.log` |
| run the dashboard | `streamlit run scripts/app/dashboard.py` |
| repeat the test | `python scripts/run_test.py` |

The data we submit is in `export/`: CSV files made from a copy in `data/backups/`, never from
`cve_meter.db` itself while the collector runs. The proof of the 48 hours is `export/health.csv`;
the "The run" part of `db_status.py` adds it up on the machine that collects.
