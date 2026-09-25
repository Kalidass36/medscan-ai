# MedScan-AI

MedScan-AI is a free-resources proof-of-concept for extracting medication information from prescriptions and clinical documents, validating entries, and converting them to a minimal FHIR JSON bundle.

Quick start

1. Install system dependency: Tesseract OCR (https://github.com/tesseract-ocr/tesseract). On Windows, install the Tesseract installer and add to PATH.
2. Create a Python virtual environment and install requirements:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

Optional: SciSpacy for improved medical NER

```bash
pip install scispacy
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.1/en_ner_bc5cdr_md-0.5.1.tar.gz
```

OCR options

- Local Tesseract (default): install Tesseract on the machine and ensure it's on PATH. The app will use `pytesseract`.
- Cloud OCR (recommended for Streamlit Community Cloud): the code supports OCR.Space API. Set the `OCR_SPACE_API_KEY` environment variable in the Streamlit app settings, or pass an API key to `image_to_text(..., use_api=True, api_key=...)`. If no key is provided, a limited public key (`helloworld`) will be used but has restrictions.

Basic OCR checkpoint

The first OCR baseline is available at `app/ocr/basic_ocr.py`. It uses the local Tesseract executable through `pytesseract`:

```bash
python -c "from app.ocr.basic_ocr import extract_text; print(extract_text('data/prescription.png'))"
```

On Windows, install Tesseract OCR separately and add its installation directory to `PATH` before running the command. The sample image is `data/prescription.png`.

Example: set the Streamlit secret `OCR_SPACE_API_KEY` in the app settings, then deploy.

Run the Streamlit dashboard locally:

```bash
streamlit run medscan_ai/dashboard.py
```

Run the API locally:

```bash
uvicorn medscan_ai.api:app --reload
```

Project structure

- `medscan_ai/` - package modules
- `data/` - small drug and condition lists used for validation
- `tests/` - unit tests

Notes

- This project uses simple, rule-based NER and validation to stay fully free and offline-friendly. For production use, swap to specialized medical models (SciSpacy, fine-tuned transformers) and authoritative drug resources (RxNorm).

This repository is built with Python and open-source technologies and includes an interactive application, API, tests, and deployment documentation.
