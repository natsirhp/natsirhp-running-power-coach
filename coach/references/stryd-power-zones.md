# Stryd Power Zones & Mapping to the Norwegian Method

## Critical Power (CP)

Stryd's Critical Power is the highest running power an athlete can sustain
in near-steady-state without accumulating fatigue (roughly a 30-70 minute
effort). It auto-updates from recent training (an initial estimate appears
after ~3 runs; a rolling ~90-day window refines it). On intervals.icu, the
current estimate shows up as `eftp` inside the `sportInfo` entry for
`"type": "Run"` in the athlete's latest wellness record. **Always use the
most recent eFTP** when computing %CP -- it drifts as fitness changes, and
using a stale value will misclassify every run.

`%CP = average_power_for_the_run / current_running_eFTP`

## The five zones (approximate %CP ranges)

These are the commonly-used community defaults; if the athlete's own Stryd
app shows different personalized boundaries, defer to those.

| Zone | Name | ~%CP | Typical use |
|---|---|---|---|
| 1 | Easy | < 80% | Recovery runs, long-run aerobic base |
| 2 | Moderate | 80-90% | Marathon-pace work, tempo, sub-threshold |
| 3 | Threshold | 90-100% | Cruise intervals, 10K effort, classic tempo |
| 4 | Interval | 100-110% | 5K pace, vVO2max intervals |
| 5 | Repetition | 110%+ | Short reps, strides, sprints |

## Correlating power zones to LT1/LT2

Power zones are a practical, always-available proxy for the lactate
landmarks in `references/norwegian-method.md` -- not a lab measurement, so
hold the mapping loosely and adjust based on how a session actually felt
(HR drift, perceived effort) when the two disagree:

- **Below LT1** (full aerobic, Zone 1 in the three-zone lactate model) ≈
  **Stryd Zone 1**, roughly < 80% CP.
- **LT1 / Norwegian "sub-threshold"** (the controlled 2.0-3.0 mmol/L zone
  used for double-threshold days) ≈ **Stryd Zone 2 to low Zone 3**, roughly
  80-95% CP. This is also approximately marathon-pace power for a runner
  who is fit relative to their CP.
- **LT2 / classic threshold** (~4 mmol/L, half-marathon effort) ≈ **upper
  Stryd Zone 3 to low Zone 4**, roughly 95-105% CP.
- **vVO2max / interval work** (above LT2, aerobic ceiling) ≈ **Stryd Zone
  4-5**, roughly 105-115%+ CP.
- **Neuromuscular speed / R-pace** (sprints, strides) ≈ **Stryd Zone 5+**,
  115%+ CP -- run by feel more than by exact power target.

## Using this in analysis

For any run: divide average power by current eFTP, find the row above,
and you have both a Stryd zone label and an approximate Norwegian
landmark. Two things worth calling out explicitly when they show up:

- **Mismatch between intent and execution.** If an activity is named
  "Easy" or "Recovery" but %CP lands at 85%+ (Zone 2 or higher), the
  athlete likely ran the easy day too hard -- a very common and very
  costly error, since it steals recovery from Zone 1 without producing a
  real threshold stimulus.
- **Grey-zone drift over the trailing window.** If a meaningful share of
  recent runs sit in the 80-95% CP band without being an intentional
  marathon-pace or double-threshold session, that's the "trap of
  mediocrity" from the Norwegian reference -- worth naming directly.

Power output is also sensitive to terrain, wind, and (for treadmill/virtual
runs) calibration -- if HR looks inconsistent with the power-implied zone
for a given run (e.g. high HR at a Zone 1 power), mention that discrepancy
rather than trusting power blindly.
