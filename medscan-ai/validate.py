from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
DRUGS = None


def _load_drugs():
    global DRUGS
    if DRUGS is None:
        p = BASE / "data" / "drugs.csv"
        if not p.exists():
            DRUGS = set()
        else:
            with open(p, encoding="utf-8") as f:
                DRUGS = set(line.strip().lower() for line in f if line.strip())
    return DRUGS


def validate_relation(relation: dict) -> dict:
    """Validate drug and dosage. Returns dict with flags and messages."""
    drugs = _load_drugs()
    drug = relation.get("drug")
    dosage = relation.get("dosage")
    ok = True
    messages = []
    if not drug:
        ok = False
        messages.append("missing drug")
    else:
        if drug.lower() not in drugs:
            ok = False
            messages.append("unknown drug")

    # check dosage numeric
    if dosage:
        import re
        m = re.search(r"(\d+(?:\.\d+)?)", dosage)
        if m:
            val = float(m.group(1))
            if not (0 < val < 5000):
                ok = False
                messages.append("dosage out of expected range")
        else:
            ok = False
            messages.append("unparsable dosage")

    return {"ok": ok, "messages": messages}
