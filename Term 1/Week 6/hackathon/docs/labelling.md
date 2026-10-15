# Labelling guide

Written before any comparison with a model was made. We read it and agreed
on the rules *before* labelling. The rules do not change after that; a rule we turn out to need
later goes in the report as a weakness of the guide.

## What we label

Every post gets one label. You see the text and nothing else: no
source, no account, no model score. We label together, in one sitting: one label per post. Where
we do not agree at once, we discuss the post with the rules below in hand.

The question is always the same: **how does this post sound to a security officer who reads
only this post?** Judge the text. Do not open the link, and do not use what you happen to know
about the CVE from elsewhere.

| Label | Type | Meaning |
|---|---|---|
| `alarmed` | `a` | The post warns of danger now or presses the reader to act |
| `neutral` | `n` | The post announces or describes a vulnerability, without pressing |
| `reassuring` | `r` | The post says the risk is small, contained or over |
| `skip` | `s` | You cannot read it (a language none of us reads, or no sentence left) |

## Rules, in this order

1. **A severity word or score is not alarm.** "CRITICAL", "High (8.8)", "CVSS 10.0", 🔴 and 🚨
   are labels on a scale. A post that has only these is `neutral`.
2. **What an attacker could do is not alarm.** "Allows remote attackers to execute code" is in
   almost every CVE description. `neutral`.
3. **`alarmed` needs at least one of these in the text:**
   - a. the flaw is being exploited now or was very recently ("exploited in the wild", "under
     active attack", "attackers are probing", "used by ransomware groups", "added to CISA KEV");
   - b. an urgent call to act: "patch now", "update immediately", "ASAP", "isolate", "remove";
   - c. there is no fix *and* the post treats that as a problem to act on now ("no patch, vendor
     silent, block the interface", "end of life, replace it").
4. **Calm advice is not an urgent call.** "Update to 4.8.2", "restrict access until patched",
   "monitor vendor updates", "fixed in 2.6.0" are `neutral`.
5. **`reassuring` needs the post to say so itself:** "no exploitation confirmed", "none
   exploited", "only if Redis is enabled", "low impact", "overhyped". A fix being available is
   not reassuring on its own (rule 4).
6. **Mixed messages.** If the post reports exploitation (3a), it is `alarmed`, whatever else it
   says. Otherwise take what the post ends on or spends most words on, and write `mixed` in the
   note column.
7. **Old exploitation in a profile is not alarm.** "The group is suspected to have exploited
   CVE-2023-…" in a description of a ransomware group is `neutral`.
8. **Cut-off posts** ("…"): judge what is there.
9. **Other languages:** label it if you can read it well enough to apply rules 1 to 7.
   Otherwise `skip`.

## Examples from our own stream

| Post (shortened) | Label | Rule |
|---|---|---|
| "🔴 CVE-2026-108860 - Critical (9.1) BotSharp through 5.2.0 contains an authentication bypass vulnerability that allows unauthenticated…" | neutral | 1, 2 |
| "CVE Alert: CVE-2026-108853 - UnicomAI - Wanwu - https://…" | neutral | 1 |
| "🚨 CVE-2026-66086 — CVSS 9.8 CRITICAL In the modem OTA stack, there is a possible stack-based buffer overflow…" | neutral | 1 |
| "🔴 EXPLOITED AhsayCBS backup servers are under active attack. … The latest version has no patch. Fix: restrict the console…" | alarmed | 3a |
| "A critical Nginx UI RCE vulnerability is publicly disclosed with PoC exploit code. Admins must patch now…" | alarmed | 3b |
| "CVE-2026-108576 — TOZED X300 … No patch. Vendor silent. … Block diagnostic interfaces. Evaluate replacement." | alarmed | 3c |
| "CVE-2026-47483 in NVIDIA DCGM Exporter lets unauthenticated attackers crash GPU monitoring. … Patch to 4.8.2." | neutral | 4 |
| "CVE-2023-25996 and CVE-2026-107863 affect two WooCommerce plugins. … None exploited." | reassuring | 5 |
| "CRITICAL RCE in WatchGuard Fireware OS … No known in-the-wild attacks, but update ASAP." | alarmed, note `mixed` | 6 |
| "Brain Cipher emerged in July 2024. … suspected to have exploited CVE-2023-28252" | neutral | 7 |

## Labels to train on

The 100 posts in `evaluation/labels_team.csv` are the test: we labelled them and no model is trained on them. For the
fine-tuning experiment we needed more posts than we could label in the time we had. An AI
assistant (Claude) labelled 365 older Mastodon posts with this guide, from the text only, and
marked the 16 it doubted. We checked those labels by hand and corrected the ones we disagreed with. They are used to train
with and never to measure with.

For the second round 535 posts were added, labelled with the same guide, which makes 900. All
900 are in `evaluation/train.csv`, with the label, a `doubt` column and an `origin` column that
says which batch a post came from (`backfill_1` is the 365 of the first round).

**Second round.** To get more posts to train on, 535 more posts were labelled with this guide:
301 posts from our collector and 234 more of the older Mastodon posts. The training set is 900
posts. The 100 test posts are never trained on.

## Where this guide is thin

Found while labelling:

- **"Update now" from news accounts.** Rule 3b makes "MediaTek bulletin fixes 31 flaws. Update
  now." alarmed, while the same news with "Update to 4.8.2" is neutral. One word decides. Two
  posts about the same OTRS flaw from one account came out differently for this reason.
- **Exploitation reported in a flat tone.** A news digest that says "two flaws are actively
  exploited" is `alarmed` by rule 3a, although it does not sound alarmed. This is a choice: for
  our user the content matters more than the tone. It will count against the sentiment model,
  which hears tone.
- **Rule 3c against rule 4.** "No patch yet — limit exposure, monitor vendor" sits between them.
- About one post in five was a borderline case under these rules. Those are the labels to
  trust least.
