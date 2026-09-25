from app.ner.medical_ner import extract_entities


def test_ner_detects_drug_dosage_condition():
    entities = extract_entities("Amoxicillin 500mg for pneumonia.")
    values = {(entity["word"].lower(), entity["type"]) for entity in entities}
    assert ("amoxicillin", "DRUG") in values
    assert ("500mg", "DOSAGE") in values
    assert ("pneumonia", "CONDITION") in values


def test_ner_detects_spaced_dosage():
    entities = extract_entities("Take 10 mg for pneumonia.")
    assert any(entity["word"] == "10 mg" and entity["type"] == "DOSAGE" for entity in entities)