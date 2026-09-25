from app.validation.validator import FLAGGED, VALIDATED, validate_entity, validate_relation


def test_known_drug_is_validated():
    assert validate_entity("Amoxicillin", "DRUG") == VALIDATED


def test_unknown_drug_is_flagged():
    assert validate_entity("Flurbozine", "DRUG") == FLAGGED


def test_known_and_unknown_dosage():
    assert validate_entity("500mg", "DOSAGE") == VALIDATED
    assert validate_entity("999mg", "DOSAGE") == FLAGGED


def test_relation_checks_dosage_for_drug():
    assert validate_relation("Amoxicillin", "500mg", "pneumonia")["status"] == VALIDATED
    assert validate_relation("Amoxicillin", "999mg", "pneumonia")["status"] == FLAGGED