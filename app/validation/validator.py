from .knowledge_base import KNOWN_CONDITIONS, KNOWN_DRUGS


VALIDATED = "VALIDATED"
FLAGGED = "FLAGGED"
SAFETY_NOTICE = "For research and demonstration only. Not a substitute for professional medical advice."


def _normalize(value):
    return " ".join(str(value).strip().lower().split())


def _normalize_dosage(value):
    return _normalize(value).replace(" ", "")


def validate_entity(entity_text, entity_type):
    """Return VALIDATED only for entities present in the medical knowledge base."""
    value = _normalize(entity_text)
    kind = _normalize(entity_type)

    if kind in {"drug", "chemical", "chemicals"}:
        return VALIDATED if value in KNOWN_DRUGS else FLAGGED
    if kind in {"condition", "disease", "diseases"}:
        return VALIDATED if value in KNOWN_CONDITIONS else FLAGGED
    if kind in {"dosage", "dose"}:
        dosage = _normalize_dosage(entity_text)
        known_dosages = {
            _normalize_dosage(item)
            for drug in KNOWN_DRUGS.values()
            for item in drug["common_dosages"]
        }
        return VALIDATED if dosage in known_dosages else FLAGGED
    return FLAGGED


def validate_relation(drug, dosage, condition):
    """Validate a complete extracted relationship against the knowledge base."""
    drug_key = _normalize(drug)
    drug_status = validate_entity(drug, "drug")
    dosage_status = validate_entity(dosage, "dosage")
    condition_status = validate_entity(condition, "condition")
    dosage_known_for_drug = (
        drug_key in KNOWN_DRUGS
        and _normalize_dosage(dosage)
        in {_normalize_dosage(item) for item in KNOWN_DRUGS[drug_key]["common_dosages"]}
    )
    return {
        "status": VALIDATED
        if drug_status == dosage_status == condition_status == VALIDATED and dosage_known_for_drug
        else FLAGGED,
        "drug": drug_status,
        "dosage": dosage_status if dosage_known_for_drug else FLAGGED,
        "condition": condition_status,
    }