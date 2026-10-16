---
name: daily-brief
description: Assemble and email the athlete's morning training brief — today's planned session and why, readiness call, race-plan status, race countdown, and one line of fuel/focus. Pulls from the current week's plan-my-week file, the latest weekly-review, health/vitals-log.md (auto-populated from COROS), and Strava — never invents numbers. Sends itself via email-me. Fully absorbs recovery-check's morning routine, including the injury/medical safety check and overtraining-marker scan (recovery-check itself remains available for on-demand "how should I train today" checks, but no separate scheduled email is needed). Use when the athlete asks for his daily/morning brief, or when this runs on schedule each morning.
---

# daily-brief

A fast, scannable morning ping — five lines, readable on a phone in ten
seconds. Not a report. If a line has nothing real to say, keep it short
rather than padding it.

**Output shape:**
```
**[Weekday, Mon D]** — [N] days to [goal race]

1. Today: [session] — [why, one clause]
2. Readiness: [Go hard / Go easy / Rest] — [one-line reason]
3. Race plan: [latest week grade/status, one line]
4. Countdown: [N] days to [goal race] ([race date])
5. Focus: [one line of fuel or focus for today]
```

---

## Step 1 — Load context

Read, in order:
1. `athlete-profile.md` — HR
   zones, race date, medical/injury constraints, coaching philosophy.
2. The current week's file in
   `training/` — filenames
   are `week-YYYY-MM-DD.md` using the Monday date (see plan-my-week). Pick
   the file whose Monday date is the most recent one on or before today.
   Find today's row in the Week Schedule table and its corresponding
   Session Details section for the one-line "why."
3. The most recent file in
   `reviews/` (by filename
   date) — pull its week grade and the single most relevant line for "where
   you stand vs. plan." This is the freshest real verdict; don't reach back
   further than the latest one.
4. `health/vitals-log.md`
   and any dated flag files in `health/` from the last 7 days, for context
   on anything already being watched (e.g. a sore shoulder). Note if the same
   issue recurs 2+ times this week — that's a trend, not a coincidence
   (recovery-check Step 7).

   Also note whether today's planned session includes Zone 4+ work — needed
   for the medical safety check in Step 2.

   **Before reading it, check whether today's row exists.** If not, pull it
   from COROS and append it — same procedure as recovery-check/SKILL.md
   Step 2 (query `mcp__coros__queryRestingHeartRate`,
   `mcp__coros__querySleepHrv`, `mcp__coros__querySleepOverview`, and
   `mcp__coros__queryRecoveryStatus`; append RHR/HRV/sleep hrs/Sleep
   Score/Recovery % as a new row; never overwrite an existing row). Keep
   this in sync with recovery-check if it ever changes. If the `coros`
   tools are unavailable, don't block — proceed on Strava + trend data alone
   and note in the brief that no vitals were pulled today.

   Sleep duration is "Main Sleep (asleep)" only, and Sleep Score is logged
   exactly as the API returns it — don't ask the athlete for the app's score (it
   matches the COROS app). Fill the Sleep Quality column with the
   score's band (0-59 Low, 60-79 Productive, 80-100 Optimal); never ask
   for it.

---

## Step 2 — Compute readiness + countdown

Run this script. It reuses recovery-check's ACWR and RHR/HRV trend logic
(condensed) and adds the race countdown. Credentials come from `.env`;
never print or display them. **HR zone thresholds below must stay in sync
with recovery-check's — update both if the profile's zones change.**

```python
import os, re, requests
from datetime import datetime, timedelta, date
from dotenv import load_dotenv

ROOT = os.environ.get('ATHLETE_OS_ROOT', os.getcwd())
load_dotenv(f'{ROOT}/.env')

r = requests.post('https://www.strava.com/oauth/token', data={
    'client_id': os.getenv('STRAVA_CLIENT_ID'),
    'client_secret': os.getenv('STRAVA_CLIENT_SECRET'),
    'refresh_token': os.getenv('STRAVA_REFRESH_TOKEN'),
    'grant_type': 'refresh_token'
})
access_token = r.json()['access_token']

ZONES = [(134, 1), (148, 2), (155, 3), (165, 4), (999, 5)]
def zone_weight(avg_hr):
    if not avg_hr:
        return 2
    for upper, w in ZONES:
        if avg_hr < upper:
            return w
    return 5

after = int((datetime.now() - timedelta(days=42)).timestamp())
acts = requests.get(
    'https://www.strava.com/api/v3/athlete/activities',
    headers={'Authorization': f'Bearer {access_token}'},
    params={'after': after, 'per_page': 100}
).json()

daily_load = {}
for a in acts:
    d = a['start_date_local'][:10]
    dur_min = a['moving_time'] / 60
    load = a.get('suffer_score') or dur_min * zone_weight(a.get('average_heartrate'))
    daily_load[d] = daily_load.get(d, 0) + load

today = date.today()
def load_sum(start, end):
    return sum(daily_load.get((today - timedelta(days=i)).isoformat(), 0) for i in range(start, end))

acute = load_sum(1, 8)
chronic_weekly_avg = load_sum(1, 29) / 4
days_with_data = len([d for d in daily_load if (today - date.fromisoformat(d)).days <= 28])
acwr = (acute / chronic_weekly_avg) if chronic_weekly_avg > 0 else None
print(f"ACWR: {round(acwr, 2) if acwr else 'N/A'} (days_with_data={days_with_data}/28)")

vitals_path = f'{ROOT}/health/vitals-log.md'
rows = []
if os.path.exists(vitals_path):
    with open(vitals_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith('|') and 'Date' not in line and not line.startswith('|---') and not set(line) <= set('|- '):
                cols = [c.strip() for c in line.strip('|').split('|')]
                if len(cols) >= 5 and cols[0]:
                    rows.append(cols)

def to_float(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return None

rhr_vals = [(row[0], to_float(row[1])) for row in rows if to_float(row[1]) is not None]
hrv_vals = [(row[0], to_float(row[2])) for row in rows if to_float(row[2]) is not None]

baseline_rhr = (sum(v for _, v in rhr_vals[-30:]) / len(rhr_vals[-30:])) if len(rhr_vals) >= 14 else 55
todays_rhr = dict(rhr_vals).get(today.isoformat())
print(f"RHR baseline: {round(baseline_rhr, 1)}, today: {todays_rhr}, last5: {[v for _, v in rhr_vals[-5:]]}")

if len(hrv_vals) >= 7:
    last7 = [v for _, v in hrv_vals[-7:]]
    mean = sum(last7) / len(last7)
    cv = ((sum((x - mean) ** 2 for x in last7) / len(last7)) ** 0.5) / mean * 100 if mean else None
    print(f"HRV 7d avg: {round(mean, 1)}, CV: {round(cv, 1) if cv else 'N/A'}%, last7: {last7}")
else:
    print(f"HRV: only {len(hrv_vals)} readings logged")

with open(f'{ROOT}/athlete-profile.md') as f:
    profile = f.read()
goal_section = profile.split('## Goal Race')[1].split('##')[0]
race_date = date.fromisoformat(re.search(r'\d{4}-\d{2}-\d{2}', goal_section).group())
print(f"Race date: {race_date}, days to race: {(race_date - today).days}")
print(f"Today formatted: {today.strftime('%a, %b ') + str(today.day)}")
```

Before applying precedence, run recovery-check's two non-numeric checks
(Steps 6–7), condensed:
- **Injury/medical safety check.** If today's planned session includes Zone
  4+ work and the profile lists a medical constraint (e.g. exercise-induced
  asthma), its protocol applies — surface it in the Focus line. If today's self-report or the last 7 days' health/ files
  mention new soreness or pain in a specific area, treat it as real signal
  (the start of the athlete's injury-history record) and feed it into precedence
  rule 1 below, not just a footnote.
- **Overtraining-marker scan.** Beyond ACWR/HRV/RHR: sleep under ~6hr before
  a planned Key/hard session (feeds rule 5), a session that's normally easy
  reported as feeling hard (rising perceived effort — one of the earliest
  overreaching markers per Meeusen 2013), or the same flag recurring 2+ times
  in health/ this week (noted in Step 1). Any of these is worth a line in the
  brief even if the numbers look clean.

Apply recovery-check's precedence (kept in sync — see recovery-check/SKILL.md
Step 8 if this ever needs updating):
1. Injury/medical safety flag (from Step 1's context or today's self-report)
   → **Rest** or hard downgrade. Full override.
2. Sustained HRV suppression (3+ days below baseline) or RHR +5bpm sustained
   (2+ days) → **Go easy** or **Rest**, even if ACWR looks fine.
3. ACWR >1.5 (danger zone) → **Go easy** or **Rest**.
4. ACWR 1.3–1.5 (elevated) → **Go easy** if today was slated hard, otherwise
   proceed as planned, noted as elevated.
5. Short sleep (<6hr) before a planned Key/hard session → downgrade that
   session specifically, don't cancel training over sleep alone.
6. None of the above → match today's plan's own designated intensity —
   **Go hard** only if today's session is tagged `[HARD]` (or is one of the
   week file's own listed hard-carrying sessions, e.g. its Intensity Split
   note), **Go easy** otherwise. Clean vitals and an in-range ACWR clear
   today's session to proceed as written — they don't upgrade an easy or
   moderate day to "hard." A `★ Key Session` marker is a separate tag
   ("don't skip this") and doesn't imply `[HARD]`.

COROS Recovery % (pulled in Step 1) is corroborating context only — cite it
alongside the call but don't let it override the precedence above; same
caveat as recovery-check (it's a proprietary, unpublished metric, not a
peer-reviewed threshold).

If `days_with_data` < 28, or fewer than 7 HRV / 14 RHR readings exist, treat
the ratio/trend as low-confidence context rather than a verdict — same
caveat as recovery-check, don't manufacture false precision.

If today's self-report is stale or missing (no vitals-log row for today or
yesterday), don't pad the brief about it — just base the call on Strava +
trend data silently, same as recovery-check's unattended mode.

---

## Step 3 — Continuity: save real flags only

**Signal, not noise** — same rule as recovery-check. Only write a file when
something real surfaced: ACWR ≥1.3, a sustained HRV/RHR signal, new
soreness/pain, or a sleep-debt downgrade.

- Save to `health/YYYY-MM-DD.md` (today's date), same format recovery-check
  uses:
  ```markdown
  # Recovery Flag — [YYYY-MM-DD]

  **Call:** [Go hard / Go easy / Rest]
  **Flagged:** [what was flagged, one line]
  **Evidence:** [the actual numbers]
  **Action taken:** [what changed vs. the plan, if anything]
  **Watch next:** [what to check tomorrow/this week]
  ```
- If a file for today already exists (e.g. The athlete also ran recovery-check
  manually), append rather than overwrite.
- On a quiet day, don't create a file.

This keeps health/ history unbroken for weekly-review even though the
standalone recovery-check routine no longer runs automatically.

---

## Step 4 — Assemble the five lines

Using Steps 1–2's output, write exactly five lines in the Output shape above:

1. **Today** — session name + duration/effort if notable, and the "why" in
   one clause (not the full paragraph from Session Details).
2. **Readiness** — the call from Step 2, one-line reason with the real
   number that drove it (or "clean across the board" on a quiet day).
3. **Race plan** — the latest weekly-review's grade plus its single most
   relevant line (a flag still open, or a fix that landed).
4. **Countdown** — days to race from the script, race name + date.
5. **Focus** — one line of fuel or training focus for today specifically,
   grounded in the athlete profile's coaching philosophy (Dixon's
   post-workout fueling rule, any medical/injury constraints, today's session
   intensity) — not a generic tip.

Keep the coaching voice: direct, no hedging, no padding a quiet day into a
report.

---

## Step 5 — Send it

Build the email and send via the **email-me** skill:

- Subject: `Your training brief — [Weekday, Mon D]` (e.g. "Your training
  brief — Fri, Jul 10").
- HTML body: the same five lines, simple HTML (a heading + a short list),
  no marketing styling.

```bash
python3 .claude/skills/email-me/send_email.py <<'PAYLOAD'
{"subject": "Your training brief — Fri, Jul 10", "html_body": "<h3>Fri, Jul 10 — 92 days to race day</h3><ul><li>...</li></ul>"}
PAYLOAD
```

(Replace the example subject/body with the real assembled content — never
hardcode a date, always use what Step 2 computed.)

Print the same five lines in the chat too, then confirm in one line that
the email was sent (recipient only — never credentials).
