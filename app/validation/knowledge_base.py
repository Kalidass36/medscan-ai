import json
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]
DATA = json.loads((BASE / "data" / "knowledge_base.json").read_text(encoding="utf-8"))
KNOWN_DRUGS = DATA["drugs"]
KNOWN_CONDITIONS = set(DATA["conditions"])