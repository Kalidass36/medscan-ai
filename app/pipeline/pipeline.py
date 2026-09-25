from pathlib import Path

from app.fhir.formatter import create_fhir_medication_request
from app.ner.medical_ner import extract_entities
from app.ocr.basic_ocr import extract_text
from app.relationships.extractor import extract_relationships
from app.validation.validator import VALIDATED, validate_entity, validate_relation


BASE = Path(__file__).resolve().parents[2]
DEFAULT_IMAGE = BASE / "data" / "prescription.png"


def _validated_entities(entities):
    result = []
    for entity in entities:
        item = dict(entity)
        item["validated"] = (
            validate_entity(entity["word"], entity["type"]) == VALIDATED
        )
        result.append(item)
    return result


def run_pipeline(image_path, verbose=False):
    """Run OCR, medical NER, relationships, validation, and FHIR generation."""
    if verbose:
        print("Step 1: OCR")
    raw_text = extract_text(image_path)
    if not raw_text.strip():
        raise ValueError("No readable text detected.")

    if verbose:
        print("Step 2: Medical NER")
    entities = _validated_entities(extract_entities(raw_text))

    if verbose:
        print("Step 3: Relationship extraction")
    relationships = extract_relationships(entities, raw_text)

    if verbose:
        print("Step 4: Validation")
    validation = []
    validated_relationships = []
    for relationship in relationships:
        status = validate_relation(
            relationship["drug"],
            relationship["dosage"],
            relationship["condition"],
        )
        validation.append({**relationship, **status})
        if status["status"] == VALIDATED:
            validated_relationships.append(relationship)

    if verbose:
        print("Step 5: FHIR generation")
    fhir = None
    if validated_relationships:
        relationship = validated_relationships[0]
        fhir = create_fhir_medication_request(
            relationship["drug"],
            relationship["dosage"],
            relationship["condition"],
        )

    if verbose:
        print("Pipeline complete!")
    return {
        "raw_text": raw_text,
        "entities": entities,
        "relationships": relationships,
        "validation": validation,
        "fhir": fhir,
    }


if __name__ == "__main__":
    run_pipeline(DEFAULT_IMAGE, verbose=True)