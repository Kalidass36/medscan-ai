import re
from pathlib import Path
from typing import List, Dict


def _load_list(path: Path) -> List[str]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


BASE = Path(__file__).resolve().parents[1]
DRUGS = set(_load_list(BASE / "data" / "drugs.csv"))
CONDITIONS = set(_load_list(BASE / "data" / "conditions.txt"))


DOSAGE_RE = re.compile(r"\b(\d+(?:\.\d+)?\s*(?:mg|g|ml|mcg|IU))\b", re.I)


def extract_entities(text: str) -> List[Dict]:
    """Simple rule-based entity extractor.

    Returns a list of entities with `text`, `label`, `start`.
    """
    text_lower = text.lower()
    entities = []

    # Drugs (from list)
    for drug in DRUGS:
        idx = text_lower.find(drug.lower())
        if idx != -1:
            entities.append({"text": text[idx: idx + len(drug)], "label": "DRUG", "start": idx})

    # Conditions (from list)
    for cond in CONDITIONS:
        idx = text_lower.find(cond.lower())
        if idx != -1:
            entities.append({"text": text[idx: idx + len(cond)], "label": "CONDITION", "start": idx})

    # Dosages
    for m in DOSAGE_RE.finditer(text):
        entities.append({"text": m.group(1), "label": "DOSAGE", "start": m.start(1)})

    # sort by position
    entities.sort(key=lambda e: e["start"])
    return entities
