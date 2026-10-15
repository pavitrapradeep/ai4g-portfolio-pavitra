# Ethical reflection

CVE Panic Meter. AI for Good, Hackathon 6: Live Pulse, SDG 9
*Lucas Jansze, Muhammad Iqbal & Pavitra Pradeep*

Our tool reads what real people write about software vulnerabilities and helps a municipal security officer decide which systems get fixed first. Two groups can be harmed by it. The first is the officer and, behind them, the residents whose services depend on the patch decision. The second is the people who wrote the posts and did not ask to be analysed.

We picked the six risks that worry us most. For each we say what can go wrong and for whom, what we did about it, and what we could not solve. The numbers come from our source check on 11 October 2026, from the posts we collected (1,764 posts) and from our test of 100 hand-labelled posts, unless we say otherwise. The problem, the user, the sources and the full test are in the [README](README.md).

## 1. Silence is not safety

Think of a flaw in a system that a Dutch supplier builds for municipalities, such as the software behind the civil registry or social benefits. Almost nobody outside the Netherlands uses it, so nobody on Mastodon or Bluesky writes about it in English. On our dashboard it does not appear at all, or it appears with one post and a low score. If the officer reads that as "no problem", the flaw stays in next month's patch round while it may already be exploited.

This is the most serious risk, because it falls on the systems that matter most to our user and it is invisible: a missing line does not look like a mistake. The stream is English-speaking, Western and technical. Of the 1,764 posts we collected, 1,593 were in English. People on X, LinkedIn or closed channels such as the IBD's own network are not in it. Neither is infosec.exchange, the Mastodon server of the security community, which closed its feeds to readers like us. And the many administrators who read but never post are missing everywhere.

The opposite mistake is smaller. If the tool pushes a vulnerability up the list that turns out to be harmless, the officer loses some time reading the posts, or in the worst case patches earlier than needed.

**What we did.** Every score is shown with the number of posts and the number of different accounts behind it, and a score based on fewer than 5 counted posts or fewer than 3 different accounts is marked "low data". The CISA "known exploited" status and the official score always stand next to the alarm, so a quiet vulnerability that is confirmed exploited still stands out. The dashboard has a fixed warning at the top: "No alarm does not mean no risk." The rule in the README and on the dashboard is that the tool may move a vulnerability up the list, never down. And the watchlist puts products that are common in government first, also when few people post about them.

**What is not solved.** We cannot measure alarm in channels we cannot see. Of the 847 CVEs our posts mention, 800 were marked low data, so "low data" is the normal state, not the exception. The officer still needs the NCSC, the IBD and their suppliers, and for Dutch municipal software those are the only sources that will say anything.

## 2. A few automated accounts write most of the stream

The line on the dashboard looks like the mood of a community. In practice a handful of accounts writes most of it. In our source check, three accounts wrote 90 of the 103 CVE posts in one feed. In the posts we collected, 47 of the 209 accounts look automated, and they wrote 1,325 of the 1,764 posts (75%).

For the officer this means a peak can come from a feed that posts every new CVE in the same alarming words, or from one researcher posting thirty times about their own discovery. Either can push the wrong vulnerability to the top. A vendor promoting its own "branded" vulnerability can do the same on purpose.

**What we did.** We first tried Mastodon's bot flag, but it caught only 9 of 103 posts, and Bluesky has no flag at all. So we wrote our own rules. An account also counts as automated when its name or bio says so (bot, feed, RSS, alerts), when most of its posts have the same form, or when it posts too often: more than 50 times a day since it was made, 3 CVE posts within 2 minutes, or more than 12 CVE posts within 24 hours. Posts from those accounts are left out of every average by default. A switch puts them back, and every post on the dashboard says which rule applied, so the officer can check our guess. One account counts at most 3 times in an average, and the number of different accounts is shown per vulnerability.

**What is not solved.** The limits (50, 12, 3) are a first guess and not measured. A real person who posts a lot during an incident can be marked as automated, and their warning then disappears from the default view at the moment it matters. An unlabelled bot that varies its wording gets through. And coordinated hype by several accounts looks the same as real alarm. Showing alarm next to the official score at least makes such a disagreement visible.

## 3. The model misreads posts, and the number looks precise

The model gives every post a number with two decimals. As downloaded, it was trained on English tweets up to 2021 and was never taught what "RCE", "PoC" or "KEV" mean. It measures general mood, not security alarm. We expected it to go wrong in two directions. It could be too alarmed, because "critical" is the official name of a severity level and a post that only repeats it can come out as negative. Or it could be too calm, because a real warning is often written in a factual tone: "actively exploited, patch now". Those are exactly the posts our user needs.

The test showed that the second direction is the real one. As downloaded, the model found 7 of the 20 posts we had labelled alarmed, and a simple word list without machine learning did much better (F1 0.83 against 0.29). For the officer that would have meant a ranking that looks objective and misses two in three warnings. A missed warning costs more than a false alarm, because of risk 1: a low score is easily read as reassurance.

**What we did.** We tested the model on posts from our own stream that we labelled by hand together, and we fixed the bar before seeing any result: at least 60% of the alarmed posts found, and an F1 score at least 0.15 above the word list. When the model failed, we fine-tuned it on 900 posts from our own stream. It now finds 18 of the 20 alarmed posts and scores just above the word list (F1 0.86 against 0.83). That meets our first condition and not the second, and we say so in the README and on the dashboard, in the panel "How often the model is right". The posts behind every score are one click away, so the officer never has to trust the number alone. A language detector marks posts that are not in English. And we rank vulnerabilities against each other and use no fixed threshold above which something counts as "alarm".

**What is not solved.** The lead over the word list is three posts on a test of 100, so it could be chance. The price of finding more warnings is more false alarms: about one in five of the posts the model calls alarmed is not. Most of the 900 training posts were labelled by an AI assistant with our labelling guide. We checked them by hand and corrected the ones we disagreed with. We labelled the test posts ourselves, as students, not as security officers, and someone with ten years in the field might read a post differently than we did. And the model does not read Dutch, so a Dutch post about a Dutch system is marked but not scored reliably. That is risk 1 again.

We saw what this does in our own data with Japanese, the second-largest language in the stream. The model calls 100 of the 120 Japanese posts alarmed, with an average alarm score of 0.83 against 0.18 for English posts. It cannot read them, so it seems to treat text it does not understand as negative. Most of those posts come from automated accounts and are left out by default. The 18 that count are spread over 13 CVEs, and most of those are marked low data anyway. But a vulnerability that is mostly discussed in Japanese could rise on the officer's list for the wrong reason. The dashboard marks every non-English post. Leaving them out of the averages by default is the step we would take next.

## 4. A model trained in one week

We collected the posts, labelled them, fine-tuned the model and tested it all within the same week in October 2026. The training posts and the test posts come from the same days, the same accounts and the same automated feeds with their fixed form. So "18 of 20" says how well the model reads this week's stream. It says little about how it will read next month's.

The stream will change. Every week brings new CVEs, new product names and new ways of describing an attack. Our week also had its own colour: Microsoft's Patch Tuesday on 13 October fell inside it, and a few vulnerabilities dominated the conversation. A feed that changes the fixed wording of its posts, or a new bot that the model has never seen, can shift the scores without anyone noticing. The same holds for our bot rules, whose limits we chose by looking at this week's accounts.

For the officer the danger is a number that goes stale while it still looks fresh. In a month the dashboard still shows the same test result, but the model behind it may have become worse at finding warnings. The officer trusts the ranking a little more than they should, and the missed warning from risk 3 comes back without a sign.

**What we did.** We say in the README that the result of the second fine-tuning round is flattered because training and test posts come from the same accounts and days, so nobody reads the result as a promise. The test can be repeated: `scripts/run_test.py` runs the model, the second model and the word list on any set of labelled posts and writes the result the dashboard shows. Scores are stored per model, so a retrained model can be compared with the old one on the same posts. And the word list stays on the dashboard as a comparison. It does not learn from a week of posts, so if the model drops below it on new posts, that is a clear sign to retrain. The panel with the test result on the dashboard shows the date of the test and says that the result is only true for that week.

**What is not solved.** Nothing in the tool notices that the model is getting worse. We have not measured how fast the model ages, because we only have this one week. Before real use, someone would have to label a small set of fresh posts every month, about 50, run the test again and retrain when the result drops. Until that is arranged, the test result should be read as "true in October 2026".

## 5. The people in the data

The posts are public, but they were written by real people for their followers, not for our database. Many are researchers who post under their own name. A table of who is alarmed about what, and how often, would be a profile of individual people. It could be used to rank researchers, or by a vendor to see who criticises them.

**What we did.** We store no account names, display names, profile pictures, profile texts or links to the post. The account is replaced by a salted hash before anything is written, only so we can count different accounts, and @mentions in the text become "@user". The post's own address is hashed too, because it contains the author's name. The salt is created on the machine that collects and is in `.gitignore`, so without it nobody can check whether a certain account is in the data. For the bot rules we look at an account's profile, but we store only which rule applied.

We also respect what authors and servers asked for. Mastodon accounts that asked not to be processed (`noindex`, or `#nobot` / `#noindex` in their bio) are skipped, and their posts are never stored. When a Bluesky author deletes a post, Jetstream tells us and we delete our copy. We read the terms of every source first. infosec.exchange requires written permission for scraping and has closed its feeds, so we do not read it, although we first meant to use it as our main server. The collector asks every Mastodon server for its access setting each round and skips a server that closed its feeds, and it sends a contact address with every request so an admin can reach us. The dashboard only listens on the machine it runs on, and the collected posts are shared only through this private repository.

**What is not solved.** A post text can be pasted into a search engine to find its author, and hashing the account does not change that. This is why the dashboard and the data must not be public: the repository holds the post texts in `export/posts.csv`, `evaluation/test_table.csv` and `evaluation/train.csv`, so it has to stay private and be shared only with the people who assess it. If the project were ever published, the post texts would have to be taken out first.

Our deletion and opt-out rules have gaps. Deletions on Mastodon do not reach us, because the hashtag API does not report them, so a post its author deleted stays in our database. Posts stored before we added the opt-out rule are still there too. And posts by infosec.exchange accounts still reach us through federation: 28 of our first 83 Mastodon posts were written there and read by us from mastodon.social or hachyderm.io. The servers we read allow that, but the infosec.exchange admin chose to close the feeds, and we have not asked them whether they mind. Finally, we could not find a terms-of-service document for hachyderm.io, and for Bluesky we read the Jetstream announcement and the developer guidelines, not the full terms of service.

## 6. Trusting the line too much

A chart looks objective. An officer under pressure, who since the Cybersecurity Act has to explain every choice up to the mayor and aldermen, could point at the dashboard: "alarm was low, so we waited". Then the tool becomes a reason to postpone a patch, which is the opposite of what it is for. Residents carry that risk, not the officer.

The second danger is that the score gets reused. A municipality could use it to judge a supplier ("your product is always on top"), or someone could use the posts to follow what individual researchers say.

**What we did.** The README and the dashboard both list what the tool must not be used for: as the only basis for a patch decision or a reason to skip one, to rank or follow individual people, or to claim that an organisation is or is not compromised. The dashboard never gives advice such as "patch now" or "can wait". It shows alarm, the official sources and the posts, and leaves the decision to the officer. When the collector has stopped, the dashboard says in bold that what you see may be out of date, because an old chart that looks live would be worse than no chart. And storing no names makes the second kind of misuse harder.

**What is not solved.** A README cannot stop misuse. In real use this would have to be in the municipality's own rules for the tool. And we have not shown the dashboard to a real security officer, so we do not know how they would read it in a busy week.

## Would we hand this tool to a municipality?

Not as something to rely on. The fine-tuned model finds 18 of the 20 alarmed posts in our test, which is enough to point the officer to the posts worth reading first. But it did not pass the bar we set beforehand: it beats a simple word list by three posts, on a small test, with posts from the same week it was trained on. It can help decide what to read. It cannot decide what to patch.

What we would hand over is the approach. Community alarm next to the official score and the CISA status, never instead of them. The posts behind every number. A count of different accounts and a "low data" mark on everything. A tested accuracy on the dashboard, measured again every month on fresh posts. And the rule that the tool can move a vulnerability up the list, never down. With it comes the honest message that the public stream is thin and mostly automated, that it is silent about the software Dutch municipalities depend on most, and that a model trained on one week of posts has to prove itself again in the next.
