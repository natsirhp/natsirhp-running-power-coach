"""Deterministic Norwegian-method + Stryd-power analysis. No LLM here."""
from collections import Counter, defaultdict

RUN_TYPES = {"Run", "VirtualRun", "TrailRun"}

# (upper bound %CP, Stryd zone, Norwegian landmark)
ZONES = [
    (0.80, "Z1 Easy", "below LT1"),
    (0.90, "Z2 Moderate", "LT1 / sub-threshold"),
    (0.95, "Z3 Threshold (low)", "LT1 / sub-threshold"),
    (1.00, "Z3 Threshold (high)", "LT2"),
    (1.05, "Z4 Interval (low)", "LT2"),
    (1.10, "Z4 Interval", "above LT2"),
    (9.99, "Z5 Repetition", "above LT2"),
]
INTENT_EASY = ("easy", "recovery", "long", "regen")


def current_cp(wellness: list):
    """Latest running eFTP from wellness sportInfo."""
    for w in sorted(wellness, key=lambda x: x.get("id", ""), reverse=True):
        for si in w.get("sportInfo") or []:
            if si.get("type") == "Run" and si.get("eftp"):
                return float(si["eftp"])
    return None


def classify(pct: float):
    for ub, z, lm in ZONES:
        if pct < ub:
            return z, lm
    return ZONES[-1][1], ZONES[-1][2]


def band(pct: float) -> str:
    return "below_lt1" if pct < 0.80 else "lt1_lt2" if pct < 1.00 else "above_lt2"


def tsb_state(tsb: float) -> str:
    if tsb > 25: return "very fresh (detraining risk if mid-build)"
    if tsb > 5: return "fresh / race-ready"
    if tsb >= -10: return "neutral / sustainable"
    if tsb >= -30: return "productive overload"
    return "HIGH RISK - back off"


def ramp_state(r):
    if r is None: return "unknown"
    return "aggressive (>5-8/wk)" if r > 5 else "solid (3-5/wk)" if r >= 3 else "conservative (<3/wk)"


def phase(race_date, today):
    if not race_date: return None
    wk = (race_date - today).days / 7
    if wk > 16: return "pre-base (>16 wk out)"
    if wk > 12: return "1 General prep (85-90/10-15/0)"
    if wk > 8: return "1-2 Late base / early build"
    if wk > 4: return "2 Specific prep (75-80/15-20/3-5)"
    if wk > 1: return "3 Pre-competition (70-75/10/15-20)"
    return "4 Race / taper (lowest volume)"


def analyse_run(a: dict, cp: float):
    p = a.get("icu_average_watts")
    if not p or not cp:
        return None
    pct = p / cp
    zone, lm = classify(pct)
    name = (a.get("name") or "")
    intended_easy = any(k in name.lower() for k in INTENT_EASY)
    out = {
        "id": a["id"], "name": name, "date": (a.get("start_date_local") or "")[:10],
        "avg_power": round(p), "pct_cp": round(pct * 100, 1), "zone": zone, "landmark": lm,
        "dist_km": round((a.get("distance") or 0) / 1000, 2),
        "mins": round((a.get("moving_time") or 0) / 60),
        "avg_hr": a.get("average_heartrate"), "load": a.get("icu_training_load"),
        "flags": [],
    }
    if intended_easy and pct >= 0.85:
        out["flags"].append(f"named '{name}' but ran {pct*100:.0f}% CP (too hard for easy)")
    if pct < 0.80 and (a.get("average_heartrate") or 0) and a.get("icu_hr_zones"):
        pass
    return out


def trailing(acts: list, cp: float):
    """Time-weighted band split + same-day threshold doubles over ~28 days."""
    secs, by_day = Counter(), defaultdict(list)
    for a in acts:
        if a.get("type") not in RUN_TYPES or not a.get("icu_average_watts"):
            continue
        pct = a["icu_average_watts"] / cp
        t = a.get("moving_time") or 0
        secs[band(pct)] += t
        if 0.80 <= pct < 1.0:
            by_day[(a.get("start_date_local") or "")[:10]].append(round(pct * 100))
    tot = sum(secs.values()) or 1
    split = {k: round(100 * secs[k] / tot) for k in ("below_lt1", "lt1_lt2", "above_lt2")}
    doubles = {d: v for d, v in by_day.items() if len(v) >= 2}
    grey = split["lt1_lt2"] > 25
    return {"split_pct": split, "doubles": doubles, "grey_zone_drift": grey,
            "run_count": sum(1 for a in acts if a.get("type") in RUN_TYPES)}


def form(wellness: list):
    ws = sorted([w for w in wellness if w.get("ctl") is not None], key=lambda x: x["id"])
    if not ws: return {}
    w = ws[-1]
    rhrs = [x["restingHR"] for x in ws[:-1] if x.get("restingHR")]
    base = sum(rhrs[-14:]) / len(rhrs[-14:]) if rhrs else None
    tsb = w["ctl"] - w["atl"]
    return {"date": w["id"], "ctl": round(w["ctl"], 1), "atl": round(w["atl"], 1),
            "tsb": round(tsb, 1), "tsb_state": tsb_state(tsb),
            "ramp": w.get("rampRate"), "ramp_state": ramp_state(w.get("rampRate")),
            "rhr": w.get("restingHR"), "rhr_baseline": round(base, 1) if base else None,
            "rhr_elevated": bool(w.get("restingHR") and base and w["restingHR"] - base >= 4),
            "sleep_score": w.get("sleepScore")}


def _pace(dist_m, secs):
    if not dist_m or not secs:
        return None
    spk = secs / (dist_m / 1000)
    return f"{int(spk // 60)}:{int(spk % 60):02d}/km"


def analyse_intervals(ivs: list, cp: float, min_secs: int = 60):
    """Rep-by-rep execution check for a structured/threshold session. None if < 2 work reps."""
    if not ivs or not cp:
        return None
    reps, recs = [], []
    for iv in ivs:
        t = iv.get("moving_time") or iv.get("elapsed_time") or 0
        w = iv.get("average_watts")
        if not w or t < min_secs:
            continue
        row = {"secs": t, "watts": round(w), "pct_cp": round(100 * w / cp, 1),
               "hr": iv.get("average_heartrate"), "pace": _pace(iv.get("distance"), t)}
        (reps if (iv.get("type") or "").upper() == "WORK" else recs).append(row)
    if len(reps) < 2:
        return None
    for i, r in enumerate(reps, 1):
        r["rep"] = i
    pcts = [r["pct_cp"] for r in reps]
    mean = sum(pcts) / len(pcts)
    spread = max(pcts) - min(pcts)
    fade = pcts[-1] - pcts[0]
    hrs = [r["hr"] for r in reps if r["hr"]]
    hr_drift = round(hrs[-1] - hrs[0]) if len(hrs) >= 2 else None
    kind = ("sub-threshold (LT1-LT2)" if mean < 95 else "threshold (LT2)" if mean < 105
            else "VO2max / above LT2")
    flags = []
    if any(p >= 100 for p in pcts) and mean < 95:
        flags.append("some reps hit >=100% CP in a sub-threshold session (too hot)")
    if mean < 80:
        flags.append(f"work reps averaged {mean:.0f}% CP: below LT1, little threshold stimulus")
    if spread >= 6:
        flags.append(f"uneven pacing: {spread:.1f}% CP spread across reps")
    if fade <= -3:
        flags.append(f"fading: last rep {abs(fade):.1f}% CP lower than first")
    if fade >= 4:
        flags.append(f"positive split: last rep {fade:.1f}% CP higher than first (went out too easy)")
    if hr_drift is not None and hr_drift >= 8 and abs(fade) < 3:
        flags.append(f"HR drift +{hr_drift} bpm at flat power (fatigue/heat)")
    if recs:
        rec_pct = sum(r["pct_cp"] for r in recs) / len(recs)
        if rec_pct > 70:
            flags.append(f"recoveries averaged {rec_pct:.0f}% CP, too hard to be true recovery")
    return {"n_reps": len(reps), "mean_pct_cp": round(mean, 1), "kind": kind,
            "spread_pct": round(spread, 1), "fade_pct": round(fade, 1), "hr_drift": hr_drift,
            "work_secs": sum(r["secs"] for r in reps), "reps": reps,
            "recovery_pct_cp": round(sum(r["pct_cp"] for r in recs) / len(recs), 1) if recs else None,
            "flags": flags}
