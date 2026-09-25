from typing import List, Dict, Optional


def link_entities(entities: List[Dict]) -> List[Dict]:
    """Link drugs to nearest dosage and condition by text distance.

    Returns list of relations: {drug, dosage, condition}
    """
    drugs = [e for e in entities if e["label"] == "DRUG"]
    dosages = [e for e in entities if e["label"] == "DOSAGE"]
    conds = [e for e in entities if e["label"] == "CONDITION"]

    relations = []
    for d in drugs:
        # find nearest dosage
        dosage = _nearest(d, dosages)
        condition = _nearest(d, conds)
        relations.append({"drug": d["text"], "dosage": dosage["text"] if dosage else None, "condition": condition["text"] if condition else None})
    return relations


def _nearest(target: Dict, candidates: List[Dict]) -> Optional[Dict]:
    if not candidates:
        return None
    best = None
    best_dist = None
    for c in candidates:
        dist = abs(c["start"] - target["start"])
        if best is None or dist < best_dist:
            best = c
            best_dist = dist
    return best
