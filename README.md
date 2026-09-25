1. Problem
Clinical documents often contain unstructured information
that is difficult for software systems to process automatically.

3. Solution
MedScan-AI uses OCR, medical NER, validation and FHIR
generation to transform clinical documents into structured data.


5. Architecture
Document
   ↓
OCR
   ↓
Medical NER
   ↓
Relationship Extraction
   ↓
Validation
   ↓
FHIR
   ↓
Dashboard


7. Technologies
Python
PyTorch
Transformers
Hugging Face
TrOCR
Medical NER
FHIR
FastAPI
Streamlit


9. Features
✓ OCR
✓ Medical entity extraction
✓ Drug/dosage/condition detection
✓ Relationship extraction
✓ Hallucination prevention
✓ Dosage validation
✓ FHIR output
✓ Explainability
✓ REST API
✓ Web dashboardtuned transformers) and authoritative drug resources (RxNorm).

This repository is built with Python and open-source technologies and includes an interactive application, API, tests, and deployment documentation.
