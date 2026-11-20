# The Norwegian Double-Threshold Method

Practical reference for coaching against this framework. Percentages and
zones below are commonly-cited heuristics used by coaches and platforms
(TrainingPeaks, intervals.icu, Stryd community) -- treat them as guidance,
not lab-verified numbers for this specific athlete.

## The two landmarks

- **LT1** (~2.0 mmol/L blood lactate): the point where lactate first
  starts rising above baseline in a controlled way. Below it = full
  aerobic balance ("Zone 1"). LT1 pace is roughly marathon pace for a
  trained runner. Heart-rate proxy: ~78-82% of HRmax.
- **LT2** (~4.0 mmol/L): the point where lactate clearance starts losing
  the battle -- the outer edge of sustainable "hard" effort, sustainable
  for minutes not hours. LT2 pace is roughly half-marathon effort.
  Heart-rate proxy: ~88-92% of HRmax.

## Three-zone model

| Zone | Definition | Feel | Role |
|---|---|---|---|
| Zone 1 | Below LT1 | Easy, conversational | Aerobic base: mitochondria, capillaries, fat oxidation |
| Zone 2 | LT1-LT2 | Comfortably hard, sustainable only "for a while" | Used sparingly -- the "grey zone" |
| Zone 3 | Above LT2 | Hard, lactate accumulating | Precision threshold/interval work |

The core polarized/Norwegian insight: elite distance runners spend ~80% of
volume in Zone 1 and concentrate quality work at the two threshold
landmarks rather than drifting in the moderate middle. Time spent
comfortably-hard-but-not-precise (upper Zone 2 without control) costs
recovery without delivering either the Zone 1 aerobic adaptations or the
Zone 3 threshold-ceiling adaptations. Coaches call this the "trap of
mediocrity" or "grey zone" -- flag it when you see a lot of runs sitting
there with no clear purpose.

## Double-threshold days

Instead of one hard LT2 tempo run, do **two lactate-controlled sessions in
one day**, both held deliberately just below LT2 (roughly 2.0-3.0 mmol/L,
upper Zone 1 / lower Zone 2), separated by several hours. Because neither
session is maximal, the athlete recovers between them and can repeat the
pattern multiple times a week -- so total weekly threshold *volume* ends up
far higher than a single-session model allows. The discipline is entirely
about **not** going too hard on either session.

What to look for in the data: two sessions on the same calendar date, both
landing in the LT1-to-low-LT2 power range (roughly 80-95% CP -- see the
power-zones reference), both moderate duration rather than all-out. If a
"double" shows one session spiking well above LT2, that's not a Norwegian
double-threshold day, it's just two hard workouts -- worth flagging as
likely to blunt recovery.

## Macrocycle phases

Use a goal race date (ask once, remember it) to figure out which phase the
athlete is probably in, then calibrate advice accordingly.

| Phase | Duration | Zone 1 / Zone 2(LT1-LT2) / Zone 3(>LT2) | Focus |
|---|---|---|---|
| 1. General prep (base) | 12-16 wk out | 85-90% / 10-15% / ~0% | Aerobic volume; intro double-threshold conservatively, 1x/week |
| 2. Specific prep (build) | 8-12 wk out | 75-80% / 15-20% / 3-5% | Two threshold sessions/week at genuine LT2; peak mileage |
| 3. Pre-competition (sharpen) | 4-6 wk out | 70-75% / 10% / 15-20% | Volume drops, vVO2max/interval work enters, race-simulation |
| 4. Race / taper | Final 1-3 wk | 70% / 10% / 20% | Lowest volume of the year; racing is the hard training |

Common error to flag: adding *more* volume or intensity when a recent
session or race went badly. The fix for a bad session is almost always
recovery and patience, not more work -- especially if form (below) is
already deeply negative.

## Reading fatigue and form

Using intervals.icu's `ctl` (fitness), `atl` (fatigue), and
`rampRate` (weekly CTL change):

- **Form (TSB) = ctl - atl**
  - `> +25`: very fresh -- fine right before a race, a warning sign of
    detraining if it happens mid-build.
  - `+5 to +25`: fresh, race-ready.
  - `-10 to +5`: neutral, sustainable training state.
  - `-30 to -10`: productive overload -- normal during a hard training
    block, but shouldn't sit here indefinitely without a lighter week.
  - `< -30`: high risk zone -- flag it. Recommend an easy day or two
    rather than piling on.
- **Ramp rate**: sustained `> 5-8 CTL/week` is an aggressive ramp with
  elevated injury/illness risk; `3-5/week` is a solid, sustainable build;
  `< 3/week` is conservative/maintenance.
- **Resting HR and sleep**: an elevated resting HR (several beats above
  the athlete's recent baseline) or a run of poor sleep scores alongside a
  negative TSB is a stronger signal to back off than either alone.

Combine these signals rather than reacting to any single number in
isolation -- e.g. a big negative TSB during a planned hard build week with
normal resting HR and good sleep is very different from the same TSB with
elevated resting HR and poor sleep.
