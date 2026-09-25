from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from app.pipeline.pipeline import run_pipeline


def _make_test_image(path: Path):
    image = Image.new("RGB", (1400, 220), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 48)
    draw.text((30, 70), "Amoxicillin 500mg for pneumonia.", fill="black", font=font)
    image.save(path)


def test_pipeline_image_to_fhir(tmp_path):
    image_path = tmp_path / "prescription.png"
    _make_test_image(image_path)
    result = run_pipeline(image_path)
    assert result["raw_text"].strip()
    assert all(entity["validated"] for entity in result["entities"])
    assert result["relationships"] == [
        {"drug": "Amoxicillin", "dosage": "500mg", "condition": "pneumonia"}
    ]
    assert result["fhir"]["resourceType"] == "MedicationRequest"
