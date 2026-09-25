from PIL import Image
import io
import os
import base64

try:
    import pytesseract
except Exception:
    pytesseract = None

try:
    import requests
except Exception:
    requests = None


def _ocr_space_api(image_bytes: bytes, apikey: str = None, language: str = "eng") -> str:
    """Call OCR.Space API and return parsed text.

    If `apikey` is None, uses the public 'helloworld' key (limited).
    """
    if requests is None:
        raise RuntimeError("requests is required for OCR.Space API calls")
    url = "https://api.ocr.space/parse/image"
    apikey = apikey or os.environ.get("OCR_SPACE_API_KEY", "helloworld")
    files = {"file": ("image", image_bytes)}
    data = {"apikey": apikey, "language": language, "isOverlayRequired": False}
    resp = requests.post(url, files=files, data=data, timeout=60)
    resp.raise_for_status()
    j = resp.json()
    parsed = []
    for r in j.get("ParsedResults") or []:
        parsed.append(r.get("ParsedText") or "")
    return "\n".join(parsed).strip()


def image_to_text(image_path_or_bytes, use_api: bool = False, api_key: str = None) -> str:
    """Extract text from an image using either local Tesseract or OCR.Space API.

    Args:
        image_path_or_bytes: path to image file or bytes-like object
        use_api: when True, try OCR.Space API first
        api_key: optional OCR.Space API key (overrides OCR_SPACE_API_KEY env var)

    Returns:
        Extracted text (str)
    """
    # Normalize to bytes
    if isinstance(image_path_or_bytes, (bytes, bytearray)):
        img_bytes = bytes(image_path_or_bytes)
    else:
        # assume path-like
        with open(image_path_or_bytes, "rb") as f:
            img_bytes = f.read()

    # Prefer API if requested
    if use_api:
        try:
            return _ocr_space_api(img_bytes, apikey=api_key)
        except Exception:
            # fallback to local OCR
            pass

    # Local pytesseract fallback
    if pytesseract is None:
        # No local OCR available — try API as last resort
        return _ocr_space_api(img_bytes, apikey=api_key)

    img = Image.open(io.BytesIO(img_bytes))
    text = pytesseract.image_to_string(img)
    return text.strip()
