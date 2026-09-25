"""SciSpacy-enabled NER with fallback to rule-based extractor.

This module tries to load the `en_ner_bc5cdr_md` model (chemicals/diseases).
If unavailable it falls back to the simple list+regex extractor in `ner.py`.
"""
import re
from typing import List, Dict


DOSAGE_RE = re.compile(r"\b(\d+(?:\.\d+)?\s*(?:mg|g|ml|mcg|iu))\b", re.I)


def _dosages_in_text(text: str):
    for m in DOSAGE_RE.finditer(text):
        yield {"text": m.group(1), "label": "DOSAGE", "start": m.start(1)}


try:
    import spacy
    # try to load the BC5CDR NER model (chemicals + diseases)
    try:
        NLP = spacy.load("en_ner_bc5cdr_md")
        MODEL_NAME = "en_ner_bc5cdr_md"
    except Exception:
        # fallback to a general scispacy model if BC5CDR isn't installed
        try:
            NLP = spacy.load("en_core_sci_sm")
            MODEL_NAME = "en_core_sci_sm"
        except Exception:
            NLP = None
            MODEL_NAME = None
except Exception:
    NLP = None
    MODEL_NAME = None


def extract_entities(text: str) -> List[Dict]:
    """Return entities in same format as the rule-based extractor.

    If a SciSpacy model is available it maps `CHEMICAL`->`DRUG`, `DISEASE`->`CONDITION`.
    Dosages are always extracted by regex.
    """
    entities: List[Dict] = []
    if NLP:
        doc = NLP(text)
        for ent in doc.ents:
            label = ent.label_.upper()
            if label in ("CHEMICAL", "CHEMICALS"):
                mapped = "DRUG"
            elif label in ("DISEASE", "DISEASES"):
                mapped = "CONDITION"
            else:
                # unknown label — include as raw
                mapped = label
            entities.append({"text": ent.text, "label": mapped, "start": ent.start_char})

    # add regex dosages
    for d in _dosages_in_text(text):
        entities.append(d)

    # if no NLP model loaded, fall back to rule-based extractor from ner.py
    if not NLP:
        try:
            from .ner import extract_entities as _fallback

            return _fallback(text)
        except Exception:
            return entities

    # sort by position
    entities.sort(key=lambda e: e["start"])
    return entities
