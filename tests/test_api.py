from fastapi.testclient import TestClient

from app.api.main import app


def test_health_endpoint():
    response = TestClient(app).get("/health")
    assert response.json() == {"status": "healthy", "service": "MedScan-AI"}


def test_example_endpoint():
    response = TestClient(app).get("/api/v1/example")
    assert response.status_code == 200
    assert response.json()["fhir"]["resourceType"] == "MedicationRequest"


def test_process_rejects_unsupported_file():
    response = TestClient(app).post(
        "/api/v1/process",
        files={"file": ("notes.txt", b"not an image", "text/plain")},
    )
    assert response.status_code == 200
    assert response.json()["success"] is False
    assert response.json()["error"] == "Unsupported file format."