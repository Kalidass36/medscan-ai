import datetime


def to_fhir_medication_request(patient_id: str, relations: list) -> dict:
    """Convert extracted relations into a minimal FHIR-like JSON structure.

    This produces a simplified MedicationRequest bundle with conditions.
    """
    now = datetime.datetime.utcnow().isoformat()
    med_requests = []
    for r in relations:
        med = {
            "resourceType": "MedicationRequest",
            "status": "active",
            "intent": "order",
            "authoredOn": now,
            "subject": {"reference": f"Patient/{patient_id}"},
            "medicationCodeableConcept": {"text": r.get("drug")},
            "dosageInstruction": [{"text": r.get("dosage")}] if r.get("dosage") else [],
            "reasonReference": [{"display": r.get("condition")} ] if r.get("condition") else [],
        }
        med_requests.append(med)

    bundle = {
        "resourceType": "Bundle",
        "type": "collection",
        "entry": [{"resource": m} for m in med_requests],
    }
    return bundle
