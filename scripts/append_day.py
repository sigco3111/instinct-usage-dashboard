#!/usr/bin/env python3
"""Append or replace one day's record in data/usage.json, then rebuild.

Usage:
    python3 scripts/append_day.py day.json

day.json shape:
    {
      "date": "2026-10-17",
      "total_percent": 7.2,
      "agents": [{"name": "...", "percent": 1.2}, ...]
    }

A record with an existing date is replaced, not duplicated.
"""
import json
import pathlib
import sys
from datetime import datetime, timezone, timedelta

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "usage.json"
KST = timezone(timedelta(hours=9))


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    new_day = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    for key in ("date", "total_percent", "agents"):
        if key not in new_day:
            raise SystemExit(f"missing required key: {key}")

    payload = json.loads(DATA.read_text(encoding="utf-8"))
    days = [d for d in payload.get("days", []) if d.get("date") != new_day["date"]]
    days.append(new_day)
    days.sort(key=lambda d: d["date"])
    payload["days"] = days
    payload.setdefault("meta", {})["status"] = "live"
    payload["meta"]["updated_at"] = datetime.now(KST).isoformat(timespec="seconds")

    DATA.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"recorded {new_day['date']} ({new_day['total_percent']}%) — {len(days)} day(s) total")


if __name__ == "__main__":
    main()
