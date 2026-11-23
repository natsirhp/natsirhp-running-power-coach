"""Thin intervals.icu API client (HTTP Basic auth: user 'API_KEY', password = key)."""
import requests

BASE = "https://intervals.icu/api/v1"


class Intervals:
    def __init__(self, athlete_id: str, api_key: str):
        self.aid = athlete_id
        self.s = requests.Session()
        self.s.auth = ("API_KEY", api_key)

    def _get(self, path: str, **params):
        r = self.s.get(f"{BASE}/athlete/{self.aid}/{path}", params=params, timeout=30)
        r.raise_for_status()
        return r.json()

    def activities(self, oldest: str, newest: str):
        return self._get("activities", oldest=oldest, newest=newest)

    def wellness(self, oldest: str, newest: str):
        return self._get("wellness", oldest=oldest, newest=newest)

    def activity_intervals(self, activity_id: str):
        """Auto/manual detected intervals for one activity (WORK/RECOVERY with power, HR, time)."""
        r = self.s.get(f"{BASE}/activity/{activity_id}/intervals", timeout=30)
        r.raise_for_status()
        d = r.json()
        return d.get("icu_intervals", []) if isinstance(d, dict) else []
