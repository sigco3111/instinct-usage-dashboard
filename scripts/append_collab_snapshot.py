#!/usr/bin/env python3
"""Append or replace one day's collaboration snapshot in data/collaboration.json.

Usage:
    python3 scripts/append_collab_snapshot.py snapshot.json

snapshot.json shape:
    {
      "date": "2026-11-10",
      "updated_at": "2026-11-10T23:00:00+09:00",   # optional
      "agents": [ ...same shape as the top-level "agents" entries... ]
    }

A snapshot with an existing date is replaced, not duplicated, so rerunning the
daily update for the same day stays idempotent. Past days are never invented:
only dates with actually verified records should be added.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
COLLAB = ROOT / "data" / "collaboration.json"


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    snap = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    for key in ("date", "agents"):
        if key not in snap:
            raise SystemExit(f"missing required key: {key}")

    payload = json.loads(COLLAB.read_text(encoding="utf-8"))
    hist = [h for h in payload.get("history", []) if h.get("date") != snap["date"]]
    hist.append(snap)
    hist.sort(key=lambda h: h["date"])
    payload["history"] = hist

    COLLAB.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"recorded collaboration snapshot {snap['date']} — {len(hist)} day(s) total")


if __name__ == "__main__":
    main()
