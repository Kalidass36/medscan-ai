from pathlib import Path

from app.ocr.basic_ocr import extract_text


def test_prescription_image_exists():
    assert Path("data/prescription.png").exists()


def test_ocr_returns_text():
    text = extract_text("data/prescription.png")
    assert "Amoxicillin" in text


def test_ocr_reads_diagnosis():
    assert "pneumonia" in extract_text("data/prescription.png").lower()