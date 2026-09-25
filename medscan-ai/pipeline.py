from .ocr import image_to_text
try:
    from .ner_scispacy import extract_entities as extract_entities
except Exception:
    from .ner import extract_entities
from .rel_extract import link_entities
from .validate import validate_relation
from .fhir_converter import to_fhir_medication_request


def process_image(image_path_or_bytes, patient_id="example-patient"):
    text = image_to_text(image_path_or_bytes)
    entities = extract_entities(text)
    relations = link_entities(entities)
    validations = [validate_relation(r) for r in relations]
    fhir = to_fhir_medication_request(patient_id, relations)
    return {
        "text": text,
        "entities": entities,
        "relations": relations,
        "validations": validations,
        "fhir": fhir,
    }
