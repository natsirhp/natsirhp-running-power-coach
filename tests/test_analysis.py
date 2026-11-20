from datetime import date
from coach import analysis as an
from coach.main import build_facts

W = [{"id": f"2026-11-{d:02d}", "ctl": 50, "atl": 55, "rampRate": 3.5, "restingHR": 48,
      "sportInfo": [{"type": "Run", "eftp": 300}]} for d in range(1, 20)]
W.append({"id": "2026-11-20", "ctl": 52, "atl": 70, "rampRate": 6, "restingHR": 55,
          "sportInfo": [{"type": "Run", "eftp": 300}]})
A = [{"id": "i1", "type": "Run", "name": "Easy run", "start_date_local": "2026-11-20T07:00:00",
      "icu_average_watts": 270, "moving_time": 3000, "distance": 9000},
     {"id": "i0", "type": "Run", "name": "Sub-T", "start_date_local": "2026-11-18T07:00:00",
      "icu_average_watts": 275, "moving_time": 2400}]

def test_cp_and_zone():
    assert an.current_cp(W) == 300
    assert an.classify(0.90)[0].startswith("Z3")

def test_easy_too_hard_flag():
    f = build_facts(A, W, date(2027, 3, 1), date(2026, 11, 20))
    assert f["run"]["pct_cp"] == 90.0 and f["run"]["flags"]
    assert f["form"]["tsb"] == -18 and f["form"]["rhr_elevated"]
    assert f["trailing_28d"]["grey_zone_drift"]
