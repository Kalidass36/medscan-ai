import json
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = BASE / "outputs" / "medication_request.json"


def create_fhir_medication_request(drug, dosage, condition):
    """Create a FHIR MedicationRequest resource as a JSON-compatible dict."""
    return {
        "resourceType": "MedicationRequest",
        "status": "active",
        "intent": "order",
        "medicationCodeableConcept": {
            "text": drug,
        },
        "subject": {
            "reference": "Patient/patient-001",
        },
        "dosageInstruction": [
            {
                "text": f"{dosage} for {condition}",
            }
        ],
        "reasonCode": [
            {
                "text": condition,
            }
        ],
    }


def save_medication_request(resource, output_path=DEFAULT_OUTPUT):
    """Save a FHIR MedicationRequest resource to a formatted JSON file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(resource, indent=2) + "\n", encoding="utf-8")
    return output_path