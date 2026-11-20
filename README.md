# Running Power Coach

Post-run coaching agent: **Norwegian double-threshold method** + **Stryd power** (%CP), fed by the intervals.icu API.
Runs on GitHub Actions every 2h; when a new run appears it computes %CP/zone, form (CTL/ATL/TSB), ramp rate,
28-day LT1/LT2 distribution, double-threshold days and macrocycle phase, asks Claude to write a ~150-word coach's
note, and posts it as a GitHub Issue (you get notified by GitHub mobile/email).

## Setup
Repo -> Settings -> Secrets and variables -> Actions:
- Secrets: `INTERVALS_ATHLETE_ID`, `INTERVALS_API_KEY` (intervals.icu -> Settings -> Developer), `ANTHROPIC_API_KEY` (optional; without it a plain numeric summary is posted)
- Variable: `RACE_DATE` (YYYY-MM-DD) for phase-aware advice

Local: `pip install -r requirements.txt && pytest && python -m coach.main --force`

Logic lives in `coach/analysis.py` (deterministic); the LLM only phrases it using `coach/references/*.md`.
