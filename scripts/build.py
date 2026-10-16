#!/usr/bin/env python3
"""data/usage.json + src/index.template.html -> dist/index.html

Reads the usage records and injects them into the dashboard template so the
deployed page is fully static (no runtime fetch). Run after any data change.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "usage.json"
TEMPLATE = ROOT / "src" / "index.template.html"
OUT_DIR = ROOT / "dist"


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    template = TEMPLATE.read_text(encoding="utf-8")
    if "__USAGE_DATA__" not in template:
        raise SystemExit("template placeholder __USAGE_DATA__ not found")
    html = template.replace(
        "__USAGE_DATA__", json.dumps(payload, ensure_ascii=False)
    )
    OUT_DIR.mkdir(exist_ok=True)
    (OUT_DIR / "index.html").write_text(html, encoding="utf-8")
    days = len(payload.get("days", []))
    print(f"built dist/index.html with {days} day record(s)")


if __name__ == "__main__":
    main()
