---
name: fuel-and-pace
description: Build a race-day fueling (carbs/fluid/sodium) and pacing plan for a specific race, grounded in carbohydrate oxidation research, sweat/sodium science, and course-specific pacing. Use when the athlete asks for a fueling plan, nutrition plan, pacing plan, or race-day plan for a race in races/.
---

# fuel-and-pace

You are building the athlete's race-day fueling and pacing plan. This is not a generic
nutrition template — it is course-specific, athlete-specific math, with every
number traceable to either his own data or a labeled estimate.

---

## The science this skill is built on

Bake these into every calculation. Don't re-derive them from scratch or
"vibes" — use the numbers below and cite them in the output.

### Carbohydrate oxidation ceiling

- **A single carb source (glucose/maltodextrin alone) oxidizes at a hard
  ceiling of ~60 g/hr.** More than that isn't absorbed — it sits in the gut
  and causes GI distress. This ceiling is set by intestinal transporter
  saturation (SGLT1), not muscle demand.
  *Jeukendrup, A.E. (2010), "Carbohydrate and exercise performance: the role
  of multiple transportable carbohydrates," Scand J Med Sci Sports; Jeukendrup
  (2008) Eur J Sport Sci review.*
- **A glucose:fructose mix (roughly 2:1 or 1:0.8) raises the ceiling to
  ~90–105 g/hr**, because fructose uses a separate transporter (GLUT5) that
  doesn't compete with glucose's SGLT1 pathway — the two absorb in parallel.
  Studies pushing 120–144 g/hr glucose+fructose blends have measured
  exogenous oxidation up to ~105 g/hr, a ~65% increase over single-source.
  *Jeukendrup (2010) above; O'Brien & Rowlands studies on glucose-fructose
  ratios, e.g. PMC9560939 (120 g/hr fructose-maltodextrin).*
- **Duration sets the target tier** (IOC/ACSM consensus):
  - < 45 min: no carbs needed during exercise.
  - 45–75 min: small amounts / mouth rinse only.
  - 1–2.5 hr: 30–60 g/hr, single source is fine.
  - > 2.5–3 hr: up to 90 g/hr, **requires** a glucose:fructose blend to hit —
    a single source physically can't deliver it.
  *Burke, L.M. et al. (2011), "Carbohydrates for training and competition,"
  J Sports Sci (IOC consensus statement).*
- **Gut tolerance is trainable and is often the real limiter, not the
  formula.** An untrained gut caps out around 30–45 g/hr regardless of the
  ceiling above; a gut trained over 6–8 weeks of repeated high-carb long
  sessions can reach 90–120 g/hr. When a personal tolerance number is lower
  than the duration-tier target, **the personal number wins** — flag the gap
  and note it as a training-block action item, not a race-day one.
  *Cermak, N.M. & van Loon, L.J.C. (2013), Sports Med, "The Use of
  Carbohydrates During Exercise as an Ergogenic Aid"; Gatorade Sports Science
  Institute, "Training the Gut for Athletes."*
- **Running tolerates carbs worse than cycling at the same intake** — the
  mechanical bounce of running slows gastric emptying and raises GI distress
  risk versus the same g/hr on the bike. Default to the lower end of the
  target range on the run leg specifically. (Practical/coaching-consensus
  heuristic, not a single controlled-trial number — flag it as such if it
  materially changes the plan.)

### Fluid

- **Sweat rate is individual and only loosely tied to body weight** — don't
  invent a body-weight formula. Endurance athletes average **~1.28 ± 0.57
  L/hr**, but the real range runs roughly 0.5–2.5+ L/hr. Use self-report
  (light/average/heavy sweater) plus a heat/humidity modifier as the estimate,
  and always prefer a measured number if the athlete has one.
  *Baker, L.B. (2017), "Sweating Rate and Sweat Sodium Concentration in
  Athletes: A Review of Methodology and Intra/Interindividual Variability,"
  Sports Med.*
- **Measurement protocol** (give this back to the athlete as the "how to get the
  real number" line): nude body weight before exercise, then again after,
  toweled dry. Sweat rate (L/hr) = (weight lost in kg + fluid drunk in L −
  urine in L) ÷ hours exercised. Best done on a long Zone 2 session in
  race-like conditions.
- **Don't target 100% replacement during exercise.** Overdrinking beyond
  sweat losses is a real risk (exercise-associated hyponatremia), not just a
  theoretical one. Target replacing roughly **75–100% of estimated sweat
  loss**, never more than the sweat rate itself. Post-race rehydration is
  different — replace ~150% of body weight lost within 6 hours after.
  *Sawka, M.N. et al. (2007), ACSM Position Stand, "Exercise and Fluid
  Replacement," Med Sci Sports Exerc.*

### Sodium

- **Sweat sodium concentration ranges ~200–2,000 mg/L**, roughly 3x
  individual variability — this is the single biggest reason sodium plans
  can't be one-size-fits-all. Population average is roughly ~950 mg/L, but a
  "salty sweater" (visible white salt crust on skin, clothes, or a hat; salt
  stinging the eyes) can run 1,200–2,000+ mg/L, while a low-sodium sweater can
  be under 700 mg/L.
  *Baker, L.B. et al. (2019), "Normative data for sweating rate, sweat sodium
  concentration, and sweat sodium loss in athletes," J Sports Sci; Baker
  (2017) above.*
- **Sodium target (mg/hr) = sweat rate (L/hr) × sweat sodium concentration
  (mg/L) × fluid-replacement fraction.** Unlike fluid, there's no
  "overdrinking" analog for sodium at these intakes — match losses within the
  fluid you're actually planning to drink. ACSM recommends 0.5–0.7 g of
  sodium per liter of fluid consumed during exercise >1 hr, both for
  palatability/retention and to guard against hyponatremia in heavy sweaters.
  *Sawka et al. (2007) above.*
- If the computed target exceeds ~1,000–1,500 mg/hr, flag it explicitly —
  that's the point where sodium capsules/tabs on top of drink mix usually
  become necessary, because you can't dissolve enough salt in a drinkable
  volume of fluid to hit it from drink mix alone.

### Heat, altitude, and duration modifiers

- **Heat increases both sweat/sodium losses and carbohydrate utilization** —
  dehydration and heat stress independently increase reliance on
  carbohydrate (vs. fat) for fuel, on top of the obvious fluid/sodium bump.
  Bump the fluid and sodium estimates up (roughly +20–30%) for conditions
  above ~75°F / high humidity; hold or slightly increase the carb target
  rather than assuming heat makes you need less food.
  *Systematic review, "The Effect of Heat Stress and Dehydration on
  Carbohydrate Use During Endurance Exercise" (PMC12559103).*
- **Altitude (unacclimatized, roughly >1,500–2,000 m / ~5,000+ ft) cuts
  exogenous glucose oxidation by 30–50%** versus sea level, because gut blood
  flow and absorption are impaired, even though the body's total reliance on
  carbohydrate as a fuel source goes up. Practical effect: lean harder on
  glucose:fructose blends (never single-source) and expect more GI risk at
  altitude, not less.
  *Substrate oxidation at terrestrial altitude with 13C-glucose/fructose
  (PMC5256160).*
  For courses at or near sea level (roughly under ~3,000 ft), state plainly
  that altitude is not a physiological factor — don't manufacture an
  adjustment that isn't needed.
- **Longer duration compounds gut risk, not just carb need.** As total race
  time climbs past ~3 hours, GI distress becomes more likely at any given
  g/hr, which is the practical argument for gut-training and glucose:fructose
  blends before race day, not just on race day.

### Pacing

- **The single most common failure mode in Olympic-distance racing is
  starting the swim and bike too hard and having nothing left for the run.**
  Sustained, even effort beats "go hard, hang on."
  *MyProCoach, "How to Pace an Olympic Distance Triathlon."*
- **Bike pacing should target even effort, not even speed**, especially on
  rolling/hilly courses — easing off on climbs costs disproportionate time,
  and grinding climbs at even speed torches glycogen you need for the run.
  If power data exists, target a Variability Index (actual/normalized power)
  of 1.00–1.04 on flat courses, up to 1.00–1.06 on hilly ones; without a
  power meter, use HR-zone or perceived-effort caps per segment instead —
  don't let HR spike on climbs relative to the flat-road target zone.
  *D3 Multisport, "Bike Pacing In A Triathlon"; bestbikesplit.com, "Olympic
  Triathlon Bike Pacing Plan."*
- **Grade-adjust the run similarly**: hold effort/HR zone, not pace, on any
  climbs or technical/unpaved sections — let pace slow rather than let effort
  spike, especially late in a race on fatigued legs.

---

## Step 1 — Load context

Read, in order:
1. `athlete-profile.md` — for
   body weight, HR zones, medical/health constraints, and current paces.
2. The relevant race dossier in
   `races/` — for course
   profile (distances, elevation gain per leg, surface), altitude, expected
   conditions (temperature, humidity, water temp), cutoffs, and target
   splits (A/B/C goals) if they exist.

If there's more than one file in `races/`, ask which race this run is for.

**If body weight isn't in athlete-profile.md, stop and ask before doing any
math** — it's the one input nothing else can substitute for.

---

## Step 2 — Ask what the athlete knows

Ask directly (conversationally or via structured question — whichever fits):
- Gut carb tolerance: has he tested a specific g/hr in training, or is it
  unknown?
- Salty/heavy sweater self-assessment: visible salt marks on skin, clothes,
  or hat after a sweaty session? Stinging eyes?
- Measured sweat rate, if he has one from a real test.
- What products he currently uses (gels, drink mix, chews, real food) and
  their carb/sodium content per serving, if known.
- Heat tolerance: does he struggle, manage okay, or handle heat well in
  training?
- Any past fueling disasters (GI distress, bonking, cramping) worth knowing
  about.

Take whatever he gives you as ground truth over any estimate below.

---

## Step 3 — Estimate what's missing

For anything unknown, estimate from body weight + race conditions using the
ranges in the science section above. Rules for estimating:

- **Never stall waiting on a number he doesn't have.** Estimate, label it
  clearly as `(estimated)`, and give one line on how to measure the real
  version later.
- Sweat rate: use the light/average/heavy/very-heavy tiers, adjusted for the
  race's expected temperature/humidity, anchored to the Baker (2017)
  ~1.28 L/hr average if he's unsure which tier he's in.
- Sweat sodium: use the self-reported salt-marks answer to place him in the
  low/average/high mg/L band; default to the ~950 mg/L population average if
  totally unknown.
- Gut carb tolerance: if untested, estimate conservatively (30–45 g/hr) for
  an athlete without a deliberate gut-training history, unless his training
  history says otherwise (e.g., already fueling long rides successfully at
  higher rates).
- Heat/altitude modifiers: apply per the science section based on the race
  dossier's actual conditions and elevation — don't apply an altitude
  correction to a sea-level race.

---

## Step 4 — Build the fueling plan

Compute, and show the math for each:

1. **Fluid target (mL or oz/hr)** = sweat rate × 0.75–1.0 replacement
   fraction, capped at the sweat rate itself, adjusted for heat.
2. **Sodium target (mg/hr)** = sweat rate (L/hr) × sweat sodium concentration
   (mg/L) × the same replacement fraction used for fluid. Flag if it clears
   ~1,000–1,500 mg/hr (capsules needed on top of drink mix).
3. **Carb target (g/hr)**, per segment — swim (almost always none, note
   pre-race fueling separately), bike, run — using the duration tier for
   that segment's expected time, capped at his personal gut tolerance
   (estimated or known), and requiring a glucose:fructose blend if the
   target exceeds ~60 g/hr.
4. **Timeline**: translate g/hr and mL/hr into an actual "at minute X, take
   Y" schedule using his stated or assumed products (gel size, drink mix
   concentration), mapped onto the course's aid-station spacing if the
   dossier has it.
5. **Pre-race fueling**: morning-of carb loading guidance, timed to the
   race's actual start time from the dossier.
6. **Post-race**: point back to the standing profile rule — carb + protein
   within 30 minutes of finishing.

---

## Step 5 — Build the pacing plan

Using the course profile from the dossier (per-leg distance, elevation gain,
surface, altitude) and his current paces/zones from athlete-profile.md:

1. Break the bike and run into segments where the course profile changes
   materially (climbs, technical/unpaved sections, flat stretches).
2. Assign an effort target (HR zone or RPE) per segment, not a fixed pace —
   hold zone on climbs and technical terrain, let pace vary.
3. Note where fueling and pacing interact: e.g., the segment right before a
   hard effort or technical section is when the next carb dose should land,
   not mid-climb.
4. Flag anything at the edge of his cutoffs (from the dossier) so pacing and
   fueling aren't optimized independently of whether he actually clears the
   swim/bike cutoff.
5. Respect any medical constraint in athlete-profile.md (e.g. an asthma
   rule): any effort-zone pacing
   target must still pass the breathing-distress check.

---

## Step 6 — Show your work

In the output, for every number show:
- **Input source**: "yours" (with what he told you) vs. "estimated" (with
  the one-line "how to measure this for real" note).
- **The formula used**, not just the result.
- **Anything at a limit**: gut tolerance below what duration calls for,
  sodium above the drinkable-volume ceiling, pacing that's tight against a
  cutoff.

If he corrects an input, recompute everything downstream of it — don't patch
just the one number.

---

## Step 7 — Save the plan

Save to
`races/[race-date]-[race-name]-fuel-pace-plan.md`
(race date, not today's date — this is a plan for that day).

The saved file should clearly mark, right in the tables, which numbers are
his and which are estimates — he should be able to scan it later and know
exactly what to go dial in with a real sweat test or gut-training block, per
the "how to measure this" notes.
