import re
from pathlib import Path


DOSAGE_RE = re.compile(
    r"\b(\d+(?:\.\d+)?\s*(?:mg|g|ml|mcg|iu|tablet|tablets))\b",
    re.IGNORECASE,
)
LABEL_MAP = {
    "CHEMICAL": "DRUG",
    "CHEMICALS": "DRUG",
    "DRUG": "DRUG",
    "DISEASE": "CONDITION",
    "DISEASES": "CONDITION",
    "CONDITION": "CONDITION",
}

BASE = Path(__file__).resolve().parents[2]
_MODEL = None
_MODEL_ATTEMPTED = False


def _load_terms(filename):
    path = BASE / "data" / filename
    if not path.exists():
        return []
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _load_medical_model():
    global _MODEL, _MODEL_ATTEMPTED
    if _MODEL_ATTEMPTED:
        return _MODEL

    _MODEL_ATTEMPTED = True
    try:
        import spacy

        _MODEL = spacy.load("en_ner_bc5cdr_md")
    except Exception:
        _MODEL = None
    return _MODEL


def _entity(word, entity_type, confidence, start=None):
    result = {
        "word": word,
        "type": entity_type,
        "confidence": round(float(confidence), 3),
    }
    if start is not None:
        result["start"] = start
    return result


def _fallback_entities(text):
    entities = []
    lowered = text.lower()
    for term in _load_terms("drugs.csv"):
        for match in re.finditer(rf"\b{re.escape(term)}\b", text, re.IGNORECASE):
            entities.append(_entity(text[match.start():match.end()], "DRUG", 1.0, match.start()))
    for term in _load_terms("conditions.txt"):
        for match in re.finditer(rf"\b{re.escape(term)}\b", text, re.IGNORECASE):
            entities.append(_entity(text[match.start():match.end()], "CONDITION", 1.0, match.start()))
    return entities


def extract_entities(text):
    """Extract normalized medical entities from medical text."""
    entities = []
    model = _load_medical_model()
    if model is not None:
        for entity in model(text).ents:
            entity_type = LABEL_MAP.get(entity.label_.upper(), entity.label_.upper())
            if entity_type in {"DRUG", "CONDITION"}:
                entities.append(_entity(entity.text, entity_type, 0.9, entity.start_char))
    entities.extend(_fallback_entities(text))

    for match in DOSAGE_RE.finditer(text):
        entities.append(_entity(match.group(1), "DOSAGE", 0.99, match.start(1)))

    unique = {(item["start"], item["type"]): item for item in entities}
    return sorted(unique.values(), key=lambda item: item["start"])