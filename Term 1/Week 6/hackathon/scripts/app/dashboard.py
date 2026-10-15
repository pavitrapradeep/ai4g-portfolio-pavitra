"""Phase 5: the dashboard. It only reads the database; the collector keeps writing meanwhile.

Run from the project root:  streamlit run scripts/app/dashboard.py
"""
import html
import json
import sys
from contextlib import closing
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import altair as alt
import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cve_meter import config, metrics  # noqa: E402

LOCAL = ZoneInfo(config.LOCAL_TIMEZONE)
INK, MUTED, RULE, PAPER, ALARM = "#17191c", "#5c6066", "#d9d7d1", "#fbfaf7", "#b42318"
WINNER = "background-color: #f6dcd8; font-weight: 650"  # the best row in the test table
RANGES = {"24 hours": 24, "3 days": 72, "7 days": 168}
SCORE_FROM = {"nvd": "NVD", "cna": "Vendor", "none": "No score yet"}
NO_SCORE_X = -1  # where CVEs without a score sit in the plot, left of the 0 to 10 scale
MAX_POSTS_SHOWN = 50
NOTHING = (None, None, None)  # nothing clicked yet
LOW_DATA = (f"Low data: fewer than {config.LOW_DATA_POSTS} counted posts or fewer than "
            f"{config.LOW_DATA_ACCOUNTS} different accounts.")

st.set_page_config(page_title="CVE Panic Meter", layout="wide")
st.markdown(f"""<style>
.block-container {{ max-width: 1180px; padding-top: 2.5rem; padding-bottom: 4rem; }}
.stMainBlockContainer h1 {{ font-size: 1.75rem; font-weight: 650; letter-spacing: 0; padding: 0 0 0.25rem; }}
.stMainBlockContainer h2 {{ font-size: 1.15rem; font-weight: 650; letter-spacing: 0; padding: 2rem 0 0.25rem; }}
.stMainBlockContainer h3 {{ font-size: 1rem; font-weight: 650; letter-spacing: 0; padding: 1rem 0 0.5rem; }}
.note {{ color: {MUTED}; font-size: 0.9rem; margin: 0 0 0.75rem; max-width: 46rem; }}
.limit {{ border-top: 1px solid {INK}; border-bottom: 1px solid {INK}; padding: 0.75rem 0; margin: 1rem 0 0;
          max-width: 46rem; }}
.facts {{ margin: 0 0 1rem; max-width: 46rem; }}
.facts div {{ display: flex; gap: 1rem; padding: 0.25rem 0; border-bottom: 1px solid {RULE}; }}
.facts dt {{ color: {MUTED}; flex: 0 0 9rem; }}
.facts dd {{ margin: 0; }}
.post {{ border-top: 1px solid {RULE}; padding: 0.75rem 0; max-width: 46rem; }}
.post p {{ margin: 0.25rem 0 0; overflow-wrap: anywhere; }}
.post .meta {{ color: {MUTED}; font-size: 0.85rem; display: flex; flex-wrap: wrap; gap: 0 1rem; }}
.post .alarm {{ color: {INK}; font-weight: 650; font-variant-numeric: tabular-nums; }}
.post .left-out {{ color: {ALARM}; }}
</style>""", unsafe_allow_html=True)


def local(moment):
    """The same moment in the reader's own time zone (the database keeps UTC)."""
    return moment.astimezone(LOCAL)


def clock(moment):
    """A local time without its zone, which is how the charts want it: they draw what they get."""
    return local(moment).replace(tzinfo=None)


def ago(moment, now):
    """How long ago a moment was, in words: minutes up to two hours, then hours, then days."""
    minutes = int((now - moment).total_seconds() // 60)
    if minutes < 1:
        return "less than a minute ago"
    if minutes < 120:
        return f"{minutes} min ago"
    return f"{minutes // 60} hours ago" if minutes < 48 * 60 else f"{minutes // 1440} days ago"


def note(text):
    """Writes one line of small grey explanation text on the page."""
    st.markdown(f'<p class="note">{text}</p>', unsafe_allow_html=True)


def remember(widget, kind):
    """Called after a click in a chart or the table: whatever was clicked last is what we show."""
    chosen = st.session_state[widget].selection
    if kind == "row":
        value = st.session_state.table_order[chosen.rows[0]] if chosen.rows else None
    else:
        value = chosen["pick"][0][kind] if chosen["pick"] else None
    if value:
        st.session_state.picked = ("hour" if kind == "hour" else "cve", value, widget)


def hour_charts(hours, now, span, picked):
    """The alarm line with the post counts under it, on the same hours."""
    # One row per hour in the chosen period, also for hours without posts, so a quiet hour shows as a
    # gap in the line and an empty bar instead of disappearing from the chart
    end = metrics.hour_of(now)
    start = end - timedelta(hours=span - 1)
    rows = []
    for n in range(span):
        hour = start + timedelta(hours=n)
        found = hours.get(hour)
        rows.append({
            "hour": f"{local(hour):%Y-%m-%d %H:%M}", "time": clock(hour),
            "alarm": found["alarm"] if found else None, "posts": found["posts"] if found else 0,
            "counted": found["counted"] if found else 0, "accounts": found["accounts"] if found else 0,
            "data": "" if not found else "Low data" if found["low_data"] else "Enough data",
            "picked": picked[:2] == ("hour", f"{local(hour):%Y-%m-%d %H:%M}"),
        })
    frame = pd.DataFrame(rows)
    # Clicking a point or a bar selects that hour; show_selection() then lists its posts
    pick = alt.selection_point(name="pick", fields=["hour"], on="click")
    x = alt.X("time:T", title=None, scale=alt.Scale(domain=[clock(start - timedelta(minutes=30)),
                                                            clock(end + timedelta(minutes=30))]),
              axis=alt.Axis(format="%a %H:%M", labelColor=MUTED, grid=False))
    # What you see when you hover over a point or a bar
    tips = [alt.Tooltip("hour:N", title="Hour"), alt.Tooltip("alarm:Q", title="Average alarm", format=".2f"),
            alt.Tooltip("posts:Q", title="Posts"), alt.Tooltip("counted:Q", title="Counted"),
            alt.Tooltip("accounts:Q", title="Different accounts"), alt.Tooltip("data:N", title="Basis")]

    def y(field, title, **more):
        """A vertical axis in the page's colours. The fixed width keeps the two charts lined up."""
        return alt.Y(field, title=title, axis=alt.Axis(minExtent=44, maxExtent=44, labelColor=MUTED,
                                                       titleColor=MUTED, gridColor=RULE, **more))

    # Top chart: the average alarm per hour as a line, with a point on every hour that has posts.
    # An open point means low data, a big point is the hour that was clicked
    line = alt.Chart(frame).mark_line(color=ALARM, strokeWidth=1.5).encode(
        x=x, y=y("alarm:Q", "Average alarm", values=[0, 0.2, 0.4, 0.6, 0.8, 1]).scale(domain=[0, 1]))
    dots = alt.Chart(frame).transform_filter("isValid(datum.alarm)").mark_point(
        stroke=ALARM, strokeWidth=1.5, opacity=1).encode(
        x=x, y=alt.Y("alarm:Q"), tooltip=tips,
        fill=alt.condition("datum.data == 'Low data'", alt.value(PAPER), alt.value(ALARM)),
        size=alt.condition("datum.picked", alt.value(260), alt.value(70))).add_params(pick)
    # Bottom chart: the number of posts per hour, so a peak based on five posts looks different
    # from one based on two hundred
    bars = alt.Chart(frame).mark_bar().encode(
        x=x, y=y("posts:Q", "Posts", tickMinStep=1), tooltip=tips,
        color=alt.condition("datum.picked", alt.value(INK), alt.value("#a3a5a8"))).add_params(pick)
    return (line + dots).properties(height=230), bars.properties(height=110)


def score_plot(rows, picked):
    """The official score against the alarm. CVEs without a score get their own column on the left."""
    frame = pd.DataFrame([{
        "cve": row["cve_id"], "alarm": row["alarm"], "posts": row["posts"], "accounts": row["accounts"],
        "x": NO_SCORE_X if row["cvss_score"] is None else row["cvss_score"],
        "score": "none" if row["cvss_score"] is None else f"{row['cvss_score']:.1f}",
        "from": SCORE_FROM[row["cvss_source"]],
        "data": "Low data" if row["low_data"] else "Enough data",
        "cisa": "Known exploited" if row["kev"] else "Not listed",
        "picked": picked[:2] == ("cve", row["cve_id"]),
    } for row in rows])
    pick = alt.selection_point(name="pick", fields=["cve"], on="click")
    axis = dict(labelColor=MUTED, titleColor=MUTED, gridColor=RULE)
    points = alt.Chart(frame).mark_point(stroke=INK, strokeWidth=1.5, opacity=1).encode(
        x=alt.X("x:Q", title="Official CVSS score", scale=alt.Scale(domain=[-2, 10.3]),
                axis=alt.Axis(values=[0, 2, 4, 6, 8, 10], **axis)),
        y=alt.Y("alarm:Q", title="Alarm, last 24 hours", scale=alt.Scale(domain=[0, 1]),
                axis=alt.Axis(values=[0, 0.2, 0.4, 0.6, 0.8, 1], **axis)),
        shape=alt.Shape("from:N", title="Score from", scale=alt.Scale(
            domain=list(SCORE_FROM.values()), range=["circle", "square", "diamond"])),
        fill=alt.condition("datum.data == 'Low data'", alt.value(PAPER), alt.value(INK)),
        size=alt.condition("datum.picked", alt.value(320), alt.value(90)),
        tooltip=[alt.Tooltip("cve:N", title="CVE"), alt.Tooltip("alarm:Q", title="Alarm", format=".2f"),
                 alt.Tooltip("score:N", title="CVSS"), alt.Tooltip("from:N", title="Score from"),
                 alt.Tooltip("cisa:N", title="CISA list"), alt.Tooltip("posts:Q", title="Posts"),
                 alt.Tooltip("accounts:Q", title="Different accounts"), alt.Tooltip("data:N", title="Basis")],
    ).add_params(pick)
    divider = alt.Chart(pd.DataFrame({"x": [-0.25]})).mark_rule(color=RULE).encode(x="x:Q")
    label = alt.Chart(pd.DataFrame({"x": [NO_SCORE_X], "y": [1], "text": ["No score yet"]})).mark_text(
        color=MUTED, dy=-8).encode(x="x:Q", y="y:Q", text="text:N")
    return (divider + label + points).properties(height=340)


def cve_table(rows):
    """Turns the CVE rows from metrics into the table on the page, with a readable name per column."""
    return pd.DataFrame([{
        "CVE": row["cve_id"],
        "Alarm": row["alarm"],
        "Posts": row["posts"],
        "Accounts": row["accounts"],
        "Basis": "Low data" if row["low_data"] else "Enough data",
        "CVSS": row["cvss_score"],
        "Score from": SCORE_FROM[row["cvss_source"]],
        "CISA list": f"Known exploited, {row['kev_added']}" if row["kev"] else "Not listed",
        "Watchlist": row.get("watchlist_term") or "",
    } for row in rows])


def facts(pairs):
    """Shows name and value pairs as a short list of facts. The names are escaped, the values may hold HTML."""
    st.markdown('<dl class="facts">' + "".join(
        f"<div><dt>{html.escape(name)}</dt><dd>{value}</dd></div>" for name, value in pairs) + "</dl>",
        unsafe_allow_html=True)


def show_posts(posts):
    """The posts themselves, most alarmed first. Accounts get a number here, never a name or hash."""
    used = {post["id"] for post in metrics.counted(posts)}
    numbers = {}
    for post in posts:
        numbers.setdefault(post["account"], len(numbers) + 1)
    posts = sorted(posts, key=lambda post: -post["negative"])
    for post in posts[:MAX_POSTS_SHOWN]:
        meta = [f'<span class="alarm">Alarm {post["negative"]:.2f}</span>',
                f"neutral {post['neutral']:.2f}, positive {post['positive']:.2f}",
                f"{local(post['created_at']):%a %d %b %H:%M}", post["source"].capitalize(),
                f"account {numbers[post['account']]}"]
        if post["automated"]:
            meta.append(f"looks automated because {metrics.AUTOMATED_REASONS[post['automated']]}")
        if post["language"] != "en":
            meta.append(f"language {post['language'] or 'unknown'}: the model only reads English")
        if post["id"] not in used:
            meta.append(f'<span class="left-out">not counted: this account already counts '
                        f"{config.ACCOUNT_CAP} times</span>")
        st.markdown(f'<div class="post"><div class="meta">{"".join(f"<span>{m}</span>" for m in meta)}</div>'
                    f"<p>{html.escape(post['text'])}</p></div>", unsafe_allow_html=True)
    if len(posts) > MAX_POSTS_SHOWN:
        note(f"Showing the {MAX_POSTS_SHOWN} most alarmed of {len(posts)} posts.")


def show_selection(picked, widgets, posts, hours, alarms, cves, now):
    """The posts behind what was clicked, right under the chart or table it was clicked in."""
    kind, value, widget = picked
    # Only the chart or table that was clicked shows the posts, right under itself
    if widget not in widgets:
        return
    # Find the posts behind the click: those written in that hour, or those about that CVE
    if kind == "hour":
        hour = datetime.strptime(value, "%Y-%m-%d %H:%M").replace(tzinfo=LOCAL).astimezone(timezone.utc)
        chosen = [post for post in posts if metrics.hour_of(post["created_at"]) == hour]
        found = hours.get(hour)
        st.subheader(f"Posts written on {local(hour):%A %d %B}, {local(hour):%H:%M} to "
                     f"{local(hour + timedelta(hours=1)):%H:%M}", anchor=False)
    else:
        chosen = [post for post in metrics.recent(posts, now) if value in post["cves"]]
        found = alarms.get(value)
        official = cves.get(value, {})
        st.subheader(f"Posts about {value}, last {config.CVE_WINDOW_HOURS} hours", anchor=False)
    if st.button("Hide these posts", key=f"hide_{widget}"):
        st.session_state.picked = NOTHING
        st.rerun(scope="fragment")
    # The selection can be empty when a switch (such as counting automated accounts) changed since the click
    if not found:
        note("No posts for this selection with the current settings.")
        return
    # The facts above the posts: the average alarm and how many posts and accounts it is based on
    pairs = [("Average alarm", f"{found['alarm']:.2f}" + (". " + LOW_DATA if found["low_data"] else "")),
             ("Based on", f"{found['counted']} of {found['posts']} posts counted, from {found['accounts']} "
                          f"different account{'s' if found['accounts'] != 1 else ''}")]
    # For a CVE, also what the official sources say, so alarm and official score stand side by side
    if kind == "cve":
        score = official.get("cvss_score")
        by = {"nvd": "given by the NVD",
              "cna": "given by the vendor or another CVE numbering authority, not by the NVD"}
        pairs += [
            ("Official score", "Not yet scored" if score is None else
             f"{score:.1f} {html.escape(official.get('cvss_severity') or '')}, "
             f"{html.escape(by[official['cvss_source']])}"),
            ("CISA list", f"Known to be exploited, added {official['kev_added']}"
             + (". Used in ransomware" if official.get("kev_ransomware") == "Known" else "")
             if official.get("kev") else "Not listed. That is no proof it is not exploited"),
        ]
        if official.get("watchlist_term"):
            pairs.append(("Watchlist", html.escape(official["watchlist_term"])))
        if official.get("description"):
            pairs.append(("NVD description", html.escape(official["description"])))
        pairs.append(("More", f'<a href="https://nvd.nist.gov/vuln/detail/{value}">This CVE at the NVD</a>'))
    # The facts first, then the posts themselves, so the user can judge the posts for themselves
    facts(pairs)
    show_posts(chosen)


def reliability():
    """The panel with the test results. Reads evaluation/results.json, written by scripts/run_test.py,
    and says so when there is no test yet."""
    st.header("How often the model is right")
    if not config.TEST_RESULTS_PATH.exists():
        note("Not tested yet. We are labelling posts from this stream by hand and will compare the model with "
             "our labels. Until that is done, read every alarm score as unverified and open the posts.")
        return
    results = json.loads(config.TEST_RESULTS_PATH.read_text(encoding="utf-8"))
    # The date matters: the stream changes, so a test result goes stale (ETHICS.md, risk 4)
    tested = (f" on {datetime.fromisoformat(results['tested']).strftime('%d %B %Y').lstrip('0')},"
              if results.get("tested") else "")
    note(f"Tested{tested} on {results['posts']} posts from this stream that we labelled by hand. "
         "The stream changes, so this result is only true for that week. "
         "Precision: of the posts called alarmed, the share that really were. "
         "Recall: of the really alarmed posts, the share that was found. "
         "The coloured row has the highest F1 score.")
    table = pd.DataFrame(results["models"])
    best = pd.to_numeric(table["F1 alarmed"], errors="coerce").idxmax()  # "n/a" counts as no score
    st.dataframe(table.style.apply(lambda row: [WINNER if row.name == best else ""] * len(row), axis=1),
                 hide_index=True, width="content")
    if results.get("note"):
        note(html.escape(results["note"]))


@st.fragment(run_every=config.DASHBOARD_REFRESH_SECONDS)
def page():
    """Builds the whole page from top to bottom: loads the posts and CVEs once, then draws the status
    line, the charts, the CVE table, the posts and the test results."""
    # 1. Read everything once from the database (read-only, so the collector can keep writing)
    now = datetime.now(timezone.utc)
    with closing(metrics.connect()) as conn:
        everything = metrics.load_posts(conn)
        cves = metrics.load_cves(conn)
        reported = metrics.last_report(conn)

    # 2. Title and status line: how many posts, how old the newest one is, and a bold warning when the
    # collector has stopped, because an old chart that looks live is worse than no chart
    st.title("CVE Panic Meter")
    note("How alarmed public posts about software vulnerabilities sound, on Mastodon and Bluesky. "
         "Alarm runs from 0 to 1: it is the chance a sentiment model gives that a post is negative.")
    if not everything:
        note("No analysed posts yet. Start the collector and come back in a few minutes.")
        return
    status = (f"{len(everything)} posts analysed. Newest post written {ago(everything[-1]['created_at'], now)}. "
              f"This page reloads every {config.DASHBOARD_REFRESH_SECONDS} seconds.")
    if reported is None or (now - reported).total_seconds() > config.QUIET_SECONDS:
        status += (" <strong>The collector is not running" +
                   (f": it last reported {ago(reported, now)}" if reported else "") +
                   ". What you see may be out of date.</strong>")
    note(status)
    # 3. The fixed warning that silence is not safety (ETHICS.md, risk 1)
    st.markdown('<p class="limit"><strong>No alarm does not mean no risk.</strong> Software that few people '
                "post about in English stays quiet here even when it is vulnerable, and that includes most "
                "systems built for Dutch municipalities. Use this page to move a vulnerability up your list, "
                "never down.</p>", unsafe_allow_html=True)

    # 4. The switch for automated accounts (off by default), and the numbers every part below uses
    bots = sum(1 for post in everything if post["automated"])
    with_bots = st.toggle(
        f"Count posts from accounts that look automated ({bots} posts)", key="with_bots",
        help="An account looks automated when " + ", when ".join(metrics.AUTOMATED_REASONS.values()) +
             ". These rules are a first guess: open the posts to check them.")
    posts = everything if with_bots else metrics.without_bots(everything)
    hours = metrics.per_hour(posts)
    alarms = metrics.per_cve(posts, now)
    picked = st.session_state.get("picked", NOTHING)

    # 5. Alarm per hour: the line and the bars; a click shows the posts of that hour
    st.header("Alarm per hour")
    note(f"The line is the average alarm of the posts written in that hour, the bars are how many there were. "
         f"An open circle means low data. One account counts at most {config.ACCOUNT_CAP} times per hour. "
         f"Times are Dutch time. Click a point or a bar to read the posts of that hour.")
    span = RANGES[st.segmented_control("Period", list(RANGES), default="3 days", key="span",
                                       label_visibility="collapsed") or "3 days"]
    line, bars = hour_charts(hours, now, span, picked)
    st.altair_chart(line, key="hour_line", on_select=lambda: remember("hour_line", "hour"))
    st.altair_chart(bars, key="hour_bars", on_select=lambda: remember("hour_bars", "hour"))
    show_selection(picked, ("hour_line", "hour_bars"), posts, hours, alarms, cves, now)

    # 6. The table of vulnerabilities from the last 24 hours: watchlist first, then by alarm
    st.header(f"Vulnerabilities, last {config.CVE_WINDOW_HOURS} hours")
    rows = metrics.ranked(alarms, cves)
    listed = sum(1 for row in rows if row["on_watchlist"])
    note(f"{len(rows)} vulnerabilities were named in posts. {listed} of them "
         f"{'matches' if listed == 1 else 'match'} the watchlist of software that is common in government, and "
         f"those come first. Then the ones with enough data, by alarm. {LOW_DATA} "
         "Tick a row to read the posts about that vulnerability.")
    if st.toggle("Only the watchlist", key="only_watchlist"):
        rows = [row for row in rows if row["on_watchlist"]]
    if rows:
        st.session_state.table_order = [row["cve_id"] for row in rows]
        st.dataframe(
            cve_table(rows), key="table", hide_index=True, height=38 + 35 * min(len(rows), 10),
            on_select=lambda: remember("table", "row"), selection_mode="single-row",
            column_config={"Alarm": st.column_config.NumberColumn(format="%.2f"),
                           "CVSS": st.column_config.NumberColumn(format="%.1f"),
                           "Accounts": st.column_config.NumberColumn(help="Different accounts")})
        show_selection(picked, ("table",), posts, hours, alarms, cves, now)

        # 7. The scatter plot of official score against alarm, built from the same rows as the table
        st.header("Official score against alarm")
        note("Each mark is one vulnerability from the table. Look at the corners: high alarm with a low or "
             "missing score, or a high score that nobody is alarmed about. A filled mark has enough data, "
             "an open one has low data. Click a mark to read the posts.")
        st.altair_chart(score_plot(rows, picked), key="plot", on_select=lambda: remember("plot", "cve"))
        show_selection(picked, ("plot",), posts, hours, alarms, cves, now)
    else:
        note("No vulnerabilities to show with these settings.")

    # 8. How often the model is right: the result of our test
    reliability()

    # 9. What the tool must not be used for, as in the README

    st.header("What this must not be used for")
    st.markdown("""
- As the only basis for a patch decision, or as a reason to skip or postpone a patch.
- To rank, follow or judge individual people. Account names are not stored.
- To claim that an organisation is or is not compromised.

It is one extra signal next to the NCSC, the IBD, vendor advisories and a vulnerability scanner.
""")


page()
