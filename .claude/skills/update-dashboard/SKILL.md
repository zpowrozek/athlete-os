---
name: update-dashboard
description: Regenerate dashboard.html's dynamic content (readiness call, today's session, this week's sessions, volume/vert charts, pace trends, Coach's Take, hero stats) from current Strava, training/, reviews/, races/, and health/ data, while preserving its existing design. Runs automatically each morning as a scheduled task. Use when the athlete asks to refresh, update, or rebuild the dashboard.
---

# update-dashboard

Rebuilds the *data* in `dashboard.html`, never its CSS, layout, or chart
functions. The file is a single self-contained page; this skill edits its
dynamic regions in place so it reflects today instead of whatever day it was
last written.

## What stays untouched

- The `<style>` block and the structural HTML/classes.
- The `<script>` block's chart builders: `buildBarChart`, `buildTrendChart`,
  `buildRadialGauge`, `buildDonut`, and the live countdown
  (`RACE_START` / `updateCountdown`). Changing the race date is a deliberate
  one-off edit when the goal race in `athlete-profile.md` changes, not part of
  a routine refresh.
- The page structure: a `.row.cols-split` (0.5fr / 1.5fr) wrapping two
  `.col-stack` columns.
  - **Left column:** hero overview → Today's Session → weekly volume → weekly
    vert.
  - **Right column:** Paces vs. A-Goal → Today's Readiness Call → This Week's
    Sessions.
- The column-balancing classes. The volume/vert cards carry `card-chart`
  (they grow to fill slack) and the This Week's Sessions card carries
  `card-fill` (its rows space out to fill slack), so neither column is left
  with an empty gap at any window width. Keep both.
- `buildTrendChart` sizes its viewBox to the SVG's measured pixel size and
  thins x-labels by evenly spaced indices. Don't switch it to a fixed viewBox
  with `preserveAspectRatio="none"` (distorts text) or to modulo-based label
  thinning (labels can collide).

## What gets refreshed

1. **Topbar** `Built` date and the footer date/source line.
2. **Hero:** countdown label/sub-line (race name, date, start time from the
   profile), block-progress "Day X of N" plus the progress ring's
   `stroke-dasharray` (first value = `(day / total) * 125.66`), phase label,
   Total Training Hours, today's ACWR, latest week grade, and the
   `buildDonut('hero-donut', ...)` discipline split.
3. **Today's Session card:** full actionable detail for today only, as a
   `.today-steps` list (`<li><b>label</b><span>value</span></li>`):
   - Strength day: one row per exercise, value = sets×reps.
   - Swim/bike/run day: one row per segment (Warmup, Main set, Recovery,
     Cooldown) with the concrete numbers (duration, HR range, pace, RPM).
   - Rest day: skip the card or say so in one line. Don't invent steps.
   - Double day: cap at ~10 rows; merge warmups and keep each value under
     ~32 characters (values are `nowrap` in a narrow column).
   One short `pace-note` line carries the "why". All other reasoning belongs
   in Coach's Take.
4. **Weekly volume and vert bar charts** (`buildBarChart` data arrays): last
   6 Mon–Sun weeks, current week tagged `inProgress: true`.
5. **Paces vs. A-Goal card:** per discipline, current pace/speed, longest
   distance vs. race distance, one short latest-session note, and a
   `buildTrendChart` line covering the whole block since the profile's
   "Training started" date. Points are **weekly averages** (Mon-start bins,
   label `M/D`), skipping weeks with no sessions in that discipline. The goal
   is a dashed line only; the value is stated in the `.trend-head`.
6. **Readiness card:** the call, a short evidence paragraph, the
   `buildRadialGauge('gauge-acwr', ...)` value, and a one-clause "watch next"
   note. Lead with the ACWR number and band, then only the numbers that drove
   the call, one clause each. COROS Sleep Score / Recovery % may appear as
   corroborating context, never as the driver.
7. **This Week's Sessions:** one row per Mon–Sun day. Actual Strava stats for
   completed days, plan text from the week file for upcoming days, today's
   row highlighted. Terse factual lines only; today's row says "Full detail
   in the Today's Session card."
8. **Coach's Take:** an overview paragraph, up to 4 framework insights, and
   tips, written fresh from this week's data. Name the framework (Seiler
   polarized intensity, Gabbett & Hulin ACWR, Friel aerobic decoupling,
   race-dossier math, etc.). If nothing notable happened, say so plainly.

---

## Step 1 — Gather data

Read, in order:
1. `athlete-profile.md`: zones, A-goal paces, race date/time, training start
   date.
2. The current week's file in `training/` (Monday-dated filename, the most
   recent one on or before today): Week Schedule table + Session Details.
3. The most recent file in `reviews/`: latest grade and headline.
4. `health/vitals-log.md` and any dated flag files from the last 7 days.
5. The goal race's dossier in `races/`, for Coach's Take when relevant.
6. Strava, live, via the same OAuth pattern recovery-check and daily-brief
   use (credentials from `.env`; never print or display them):
   - Activities for the last ~8 weeks, for the bar charts.
   - All activities since the training start date, for the trend charts and
     Total Training Hours.
   - This week's activities day by day, for the session list.

## Step 2 — Compute

- **ACWR + readiness call:** identical method and precedence ladder as
  recovery-check. Reuse that logic; see
  `.claude/skills/recovery-check/SKILL.md` and keep both in sync. This skill
  only *reads* `health/vitals-log.md`; pulling from COROS and appending rows
  is recovery-check/daily-brief's job.
- **Block progress:** day number = today − block start + 1, out of the
  block's total days (`training/plan.md` has the start/end and phase
  boundaries).
- **Total Training Hours:** sum `moving_time` since the profile's "Training
  started" date. Include only Strava `type` in {Swim, Ride, Run,
  WeightTraining}, plus `Workout` only when its name contains
  swim/bike/run (devices sometimes mislabel swims). Exclude Hike, Walk, Golf
  and other incidental activity.
- **Weekly volume/vert:** Mon–Sun bins of hours and elevation gain (ft),
  same type filter.
- **Pace units:** swim min/100yd (convert meters via
  `round(meters * 1.09361 / 25) * 25` for a 25 yd pool), bike mph, run
  min/mi.

## Step 3 — Edit dashboard.html in place

Use targeted edits, not a full rewrite. For each section above, find its
block by its HTML comment or class (e.g. `<!-- WEEKLY SCHEDULE -->`, the
`buildBarChart(...)` calls) and replace only that block's content, keeping
the same classes so the CSS still applies. Re-read the file first; don't
assume its shape hasn't drifted from a manual edit.

Sanity-check before writing:
- `RACE_START` still matches the goal race in `athlete-profile.md`.
- Every session row's day/date matches the current week's actual dates.
- Numbers that appear in more than one place (ACWR in the hero, gauge and
  readiness text; the week grade) agree with each other.

## Step 4 — Wrap up

- Unattended (scheduled) run: no chat output needed; leave the file updated.
  If today's vitals are missing, say so in the readiness card rather than
  blocking.
- On-demand run: one-line confirmation of what changed (notably the
  readiness call), not a rehash of the page.
- Never write to `athlete-profile.md`, `training/`, `reviews/`, or
  `health/`. This skill only reads them and writes to `dashboard.html`.
