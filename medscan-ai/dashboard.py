import streamlit as st
from io import BytesIO
from .pipeline import process_image
import json


st.set_page_config(page_title="MedScan-AI", layout="centered")

st.title("MedScan-AI")
st.write("Upload a prescription or clinical document image (PNG/JPG/PDF).")
st.warning("For research and demonstration only. Not a substitute for professional medical advice.")

uploaded = st.file_uploader("Upload image", type=["png", "jpg", "jpeg", "tiff", "pdf"])

if uploaded is not None:
    data = uploaded.read()
    with st.spinner("Processing..."):
        res = process_image(data)

    st.subheader("OCR Text")
    st.text_area("text", res["text"], height=200)

    st.subheader("Entities")
    st.json(res["entities"])

    st.subheader("Relations")
    st.json(res["relations"])

    st.subheader("Validation")
    st.json(res["validations"])

    st.subheader("FHIR Bundle")
    st.json(res["fhir"])

    # download
    st.download_button("Download FHIR JSON", data=json.dumps(res["fhir"], indent=2), file_name="medscan_fhir.json", mime="application/json")
