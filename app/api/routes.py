import tempfile
from pathlib import Path

from fastapi import APIRouter, File, UploadFile

from app.api.schemas import HealthResponse, ProcessResponse
from app.fhir.formatter import create_fhir_medication_request
from app.pipeline.pipeline import run_pipeline


router = APIRouter()
SUPPORTED_FORMATS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".pdf"}


@router.get("/health", response_model=HealthResponse)
def health():
    return {"status": "healthy", "service": "MedScan-AI"}


@router.post("/api/v1/process", response_model=ProcessResponse)
async def process_document(file: UploadFile = File(...)):
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in SUPPORTED_FORMATS:
        return ProcessResponse(success=False, error="Unsupported file format.")

    data = await file.read()
    if not data:
        return ProcessResponse(success=False, error="Unable to process document.")

    temporary_file = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
    temporary_file.write(data)
    temporary_file.close()
    try:
        result = run_pipeline(temporary_file.name)
        return ProcessResponse(success=True, **result)
    except ValueError as error:
        return ProcessResponse(success=False, error=str(error))
    except Exception:
        return ProcessResponse(success=False, error="Unable to process document.")
    finally:
        Path(temporary_file.name).unlink(missing_ok=True)


@router.get("/api/v1/example")
def example():
    fhir = create_fhir_medication_request("Amoxicillin", "500mg", "pneumonia")
    return {
        "success": True,
        "raw_text": "Amoxicillin 500mg for pneumonia.",
        "entities": [
            {"word": "Amoxicillin", "type": "DRUG", "confidence": 1.0, "validated": True},
            {"word": "500mg", "type": "DOSAGE", "confidence": 0.99, "validated": True},
            {"word": "pneumonia", "type": "CONDITION", "confidence": 1.0, "validated": True},
        ],
        "relationships": [
            {"drug": "Amoxicillin", "dosage": "500mg", "condition": "pneumonia"}
        ],
        "validation": [],
        "fhir": fhir,
    }