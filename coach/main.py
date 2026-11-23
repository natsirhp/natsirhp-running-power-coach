"""Post-run check-in: fire once per NEW run on intervals.icu."""
import json, os, sys
from datetime import date, datetime, timedelta
from pathlib import Path

from . import analysis as an
from .intervals import Intervals
from .llm import coach_note

STATE = Path(os.environ.get("STATE_FILE", "state/last_activity.txt"))


def build_facts(acts, wellness, race_date, today, target=None):
    cp = an.current_cp(wellness)
    runs = sorted([a for a in acts if a.get("type") in an.RUN_TYPES],
                  key=lambda a: a.get("start_date_local", ""))
    if not runs or not cp:
        return None
    last = target or runs[-1]
    run = an.analyse_run(last, cp)
    if not run:
        return None
    return {"cp_watts": cp, "run": run, "form": an.form(wellness),
            "trailing_28d": an.trailing(acts, cp),
            "phase": an.phase(race_date, today),
            "race_date": str(race_date) if race_date else None}


def main(force=False):
    aid, key = os.environ["INTERVALS_ATHLETE_ID"], os.environ["INTERVALS_API_KEY"]
    rd = os.environ.get("RACE_DATE")
    race_date = datetime.strptime(rd, "%Y-%m-%d").date() if rd else None
    today = date.today()
    api = Intervals(aid, key)
    old, new = str(today - timedelta(days=28)), str(today)
    acts, wellness = api.activities(old, new), api.wellness(old, new)
    facts = build_facts(acts, wellness, race_date, today)
    if not facts:
        print("No run with power data; nothing to do."); return 0
    seen = STATE.read_text().strip() if STATE.exists() else ""
    if facts["run"]["id"] == seen and not force:
        print("No new activity."); return 0
    note = coach_note(facts)
    print(note)
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(facts["run"]["id"] + "\n")
    out = os.environ.get("NOTE_FILE")
    if out:
        Path(out).write_text(f"### {facts['run']['name']} - {facts['run']['date']}\n\n{note}\n")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(force="--force" in sys.argv))
    except Exception as e:  # secrets are never in these messages
        import traceback
        resp = getattr(e, "response", None)
        msg = f"{type(e).__name__}: {e}"
        if resp is not None:
            msg += f" (HTTP {resp.status_code} from {resp.url.split('?')[0]})"
        msg = msg.replace(os.environ.get("INTERVALS_API_KEY", "\0"), "***")
        Path("error.txt").write_text(msg + "\n\n" + traceback.format_exc()[-1200:].replace(
            os.environ.get("INTERVALS_API_KEY", "\0"), "***"))
        print(msg, file=sys.stderr)
        sys.exit(1)
