from app.fhir.formatter import create_fhir_medication_request


def test_fhir_medication_request_shape():
    resource = create_fhir_medication_request("Amoxicillin", "500mg", "pneumonia")
    assert resource["resourceType"] == "MedicationRequest"
    assert resource["status"] == "active"
    assert resource["intent"] == "order"
    assert resource["medicationCodeableConcept"]["text"] == "Amoxicillin"
    assert resource["dosageInstruction"][0]["text"] == "500mg for pneumonia"
    assert resource["reasonCode"][0]["text"] == "pneumonia"