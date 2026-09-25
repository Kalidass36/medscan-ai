# Deploy to Streamlit Community Cloud

1. Create a GitHub repository and push this project.
2. Ensure `requirements.txt` is present at repo root (already included).
3. Add a `streamlit_app.py` file at repo root (already included) that imports `medscan_ai.dashboard`.
4. On https://share.streamlit.io click "New app" → connect your GitHub repo → choose branch and `streamlit_app.py` as the main file.
5. Configure secrets (if any) in the Streamlit app settings. No secrets are required for offline demo.

Notes:
- Make sure Tesseract is available in the runtime if you rely on `pytesseract`. Streamlit Community Cloud does not include Tesseract by default. For fully cloud-native OCR, consider switching to a hosted OCR API or pre-processing images locally before upload.
- For best NER in cloud, install the SciSpacy model in `requirements.txt` or use a smaller model to reduce build time.
