import os
import shutil
from pathlib import Path

from PIL import Image
import pytesseract


def _configure_tesseract():
    configured_path = os.environ.get("TESSERACT_CMD")
    if configured_path:
        pytesseract.pytesseract.tesseract_cmd = configured_path
        return

    executable = shutil.which("tesseract")
    if not executable:
        for candidate in (
            Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe"),
            Path(r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"),
        ):
            if candidate.is_file():
                executable = str(candidate)
                break

    if executable:
        pytesseract.pytesseract.tesseract_cmd = executable


def extract_text(image_path):
    """Extract text from an image file using the local Tesseract engine."""
    _configure_tesseract()
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)