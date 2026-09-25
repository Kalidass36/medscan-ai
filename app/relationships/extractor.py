import re


SENTENCE_RE = re.compile(r"[^.!?\n]+(?:[.!?]+|$)")


def _entity_value(entity, *keys):
    for key in keys:
        value = entity.get(key)
        if value:
            return value
    return None


def _sentence_entities(entities, start, end):
    selected = []
    for entity in entities:
        entity_start = entity.get("start")
        if entity_start is None or start <= entity_start < end:
            selected.append(entity)
    return sorted(selected, key=lambda entity: entity.get("start", start))


def extract_relationships(entities, text):
    """Extract drug-dosage-condition triples within individual sentences."""
    relationships = []
    for sentence_match in SENTENCE_RE.finditer(text):
        sentence_start = sentence_match.start()
        sentence_end = sentence_match.end()
        sentence_entities = _sentence_entities(entities, sentence_start, sentence_end)
        drugs = [
            entity for entity in sentence_entities
            if _entity_value(entity, "type", "label") == "DRUG"
        ]
        dosages = [
            entity for entity in sentence_entities
            if _entity_value(entity, "type", "label") == "DOSAGE"
        ]
        conditions = [
            entity for entity in sentence_entities
            if _entity_value(entity, "type", "label") == "CONDITION"
        ]

        for drug in drugs:
            drug_start = drug.get("start", sentence_start)
            dosage = next((item for item in dosages if item.get("start", 0) > drug_start), None)
            condition = next((item for item in conditions if item.get("start", 0) > drug_start), None)
            if dosage is None or condition is None:
                continue
            relationships.append(
                {
                    "drug": _entity_value(drug, "word", "text"),
                    "dosage": _entity_value(dosage, "word", "text"),
                    "condition": _entity_value(condition, "word", "text"),
                }
            )
    return relationships